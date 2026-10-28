"""
Offres publiées par les ATS publics des groupes turcs présents en France (companies_data.TURKISH_COMPANIES_IN_FRANCE).

Audit live du 28/10/2026 (seules les entreprises à listing public machine-lisible sont dans ATS_CONFIG) :
- Trendyol ............ Lever  api.lever.co/v0/postings/trendyol?mode=json  (champ `country` structuré)
- Ekol -> DFDS ........ Teamtailor jobs.dfds.com/jobs.json (JSON Feed + schema.org JobPosting, addressCountry)
                        (l'activité internationale d'Ekol a été reprise par DFDS ; offres DFDS France = Calais/Dieppe)
- Pladis / Godiva ..... Workday pladis.wd3.myworkdayjobs.com (facette Location_Country, détail jobPostingInfo.country)
Non branchées (pas de listing public exploitable) :
- Beko Europe : bekoeurope.com/careers -> 404 ; Beko France publie via job boards (France Travail, Wizbii) ;
  kockariyerim.com = portail Koç (Turquie). Lever/Greenhouse/SmartRecruiters/Ashby/Recruitee : aucun compte.
- Turkish Airlines : careers.turkishairlines.com sans liste ; candidature apply.turkishairlines.com derrière login.
- Barsan, Vestel (vestelkariyer.com : login), Eczacıbaşı/VitrA, Çimsa/Kordsa (Sabancı), Şahinler, ISKO :
  portails RH turcs sans flux public ni ATS standard détecté ; Şişecam (403), Ekol.com (403) -> non contournés.
- Bleckmann (ex-Netlog/Horoz) : pages /vacancies HTML sans poste en France.
Règle : on ne garde que les postes dont le lieu STRUCTURÉ est la France.
"""
import datetime
import re
from typing import Dict, List, Optional

from models import JobOpportunity
from .common import http_get, http_post, now_str, to_iso_date
from .gurbetilan import detect_language_requirements, extract_visa_evidence, lines_text, snippet_of, utc_now_iso

SOURCE = "ATS groupes turcs"
DELAY = 1.0
MAX_FEED_PAGES = 5

# {entreprise lisible: (type d'ATS, identifiant)}
ATS_CONFIG: Dict[str, tuple] = {
    "Trendyol": ("lever", "trendyol"),
    "DFDS France (ex-Ekol Lojistik)": ("teamtailor_feed", "https://jobs.dfds.com"),
    "Pladis (Yıldız Holding)": ("workday", ("pladis", "wd3", "pladis_Careers")),
    "Godiva (Yıldız Holding)": ("workday", ("pladis", "wd3", "Godiva_Careers")),
}

_FR_WORDS = re.compile(r"\b(?:france|fransa|paris|lyon|marseille|toulouse|lille|nantes|bordeaux|strasbourg|nice)\b", re.I)


def _make(company: str, ats: str, title: str, url: str, city: str, posted: str, description: str,
          contact: str = "") -> JobOpportunity:
    snippet = snippet_of(description)
    return JobOpportunity(
        title=title, title_fr=title, company=company,
        location=f"{city}, France" if city else "France", city=city or "France", country="FR",
        url=url, source=f"{company} ({ats})", source_type="ats", kind="offer",
        snippet=snippet, snippet_fr=snippet, description=description,
        posted_at=posted, verified_at=utc_now_iso(), discovered_at=now_str(),
        contact_info=contact or url, language_requirements=detect_language_requirements(description),
        visa_evidence=extract_visa_evidence(description), visa_sponsorship="",
    )


# ------------------------------------------------------------------ Lever -----------------------
def map_lever(p: Dict, company: str) -> Optional[JobOpportunity]:
    cats = p.get("categories") or {}
    country = (p.get("country") or "").upper()
    locs = cats.get("allLocations") or [cats.get("location") or ""]
    if country and country != "FR":
        return None
    if not country and not any(_FR_WORDS.search(l or "") for l in locs):
        return None
    parts = [p.get("openingPlain") or "", p.get("descriptionBodyPlain") or p.get("descriptionPlain") or ""]
    for lst in p.get("lists") or []:
        parts.append(f"{lst.get('text', '')}\n{lines_text(lst.get('content', ''))}")
    parts.append(p.get("additionalPlain") or "")
    desc = lines_text("\n".join(x for x in parts if x))
    meta = " | ".join(x for x in (cats.get("commitment"), p.get("workplaceType"), cats.get("team")) if x)
    city = next((l for l in locs if l), "")
    return _make(company, "Lever", (p.get("text") or "").strip(), p.get("hostedUrl") or "", city,
                 to_iso_date(p.get("createdAt")), (meta + "\n" + desc).strip(), p.get("applyUrl") or "")


def fetch_lever(company: str, ident: str) -> List[JobOpportunity]:
    r = http_get(f"https://api.lever.co/v0/postings/{ident}", params={"mode": "json"}, delay=DELAY)
    if r is None or r.status_code != 200:
        print(f"[-] {company} Lever -> {getattr(r, 'status_code', 'réseau')}")
        return []
    return [j for j in (map_lever(p, company) for p in r.json()) if j and j.url and j.title]


# ------------------------------------------------------------------ Teamtailor (JSON Feed) ------
def map_teamtailor(item: Dict, company: str) -> Optional[JobOpportunity]:
    jp = item.get("_jobposting") or {}
    locs = jp.get("jobLocation") or []
    if isinstance(locs, dict):
        locs = [locs]
    fr = [((l.get("address") or {}).get("addressLocality") or "") for l in locs
          if ((l.get("address") or {}).get("addressCountry") or "").upper() in ("FR", "FRANCE")]
    if not fr:
        return None
    desc = lines_text(jp.get("description") or item.get("content_html") or "")
    org = (jp.get("hiringOrganization") or {}).get("name") or company
    name = company if org.lower() in company.lower() else f"{org} ({company})"
    return _make(name, "Teamtailor", (item.get("title") or jp.get("title") or "").strip(), item.get("url") or "",
                 " / ".join(dict.fromkeys(c for c in fr if c)), to_iso_date(item.get("date_published") or jp.get("datePosted")),
                 desc)


def fetch_teamtailor_feed(company: str, base: str) -> List[JobOpportunity]:
    jobs, url = [], base.rstrip("/") + "/jobs.json"
    for _ in range(MAX_FEED_PAGES):
        r = http_get(url, delay=DELAY)
        if r is None or r.status_code != 200:
            print(f"[-] {company} Teamtailor -> {getattr(r, 'status_code', 'réseau')}")
            break
        data = r.json()
        jobs += [j for j in (map_teamtailor(it, company) for it in data.get("items", [])) if j and j.url and j.title]
        url = data.get("next_url")
        if not url or not data.get("items"):
            break
    return jobs


# ------------------------------------------------------------------ Workday ---------------------
def map_workday(info: Dict, company: str) -> Optional[JobOpportunity]:
    country = info.get("country") or (info.get("jobRequisitionLocation") or {}).get("country") or {}
    if (country.get("alpha2Code") or "").upper() not in ("", "FR") or (country.get("descriptor") or "").lower() not in ("france", ""):
        return None
    if not country:
        return None
    end = info.get("endDate") or ""
    if end and end < datetime.date.today().isoformat():
        return None
    city = (info.get("location") or "").split(" - ")[-1].strip()
    meta = " | ".join(x for x in (info.get("timeType"), info.get("timeLeftToApply")) if x)
    desc = lines_text(info.get("jobDescription") or "")
    return _make(company, "Workday", (info.get("title") or "").strip(), info.get("externalUrl") or "", city,
                 to_iso_date(info.get("startDate")), (meta + "\n" + desc).strip())


def fetch_workday(company: str, ident: tuple) -> List[JobOpportunity]:
    tenant, dc, site = ident
    base = f"https://{tenant}.{dc}.myworkdayjobs.com/wday/cxs/{tenant}/{site}"
    hdr = {"Accept": "application/json", "Content-Type": "application/json"}
    r = http_post(base + "/jobs", json={"appliedFacets": {}, "limit": 1, "offset": 0, "searchText": ""}, headers=hdr, delay=DELAY)
    if r is None or r.status_code != 200:
        print(f"[-] {company} Workday -> {getattr(r, 'status_code', 'réseau')}")
        return []
    fr_ids = [v["id"] for f in r.json().get("facets", []) if f.get("facetParameter") == "Location_Country"
              for v in f.get("values", []) if (v.get("descriptor") or "").lower() == "france"]
    if not fr_ids:
        return []  # aucun poste en France aujourd'hui
    jobs, offset = [], 0
    while offset < 200:
        r = http_post(base + "/jobs", json={"appliedFacets": {"Location_Country": fr_ids}, "limit": 20, "offset": offset,
                                            "searchText": ""}, headers=hdr, delay=DELAY)
        if r is None or r.status_code != 200:
            break
        postings = r.json().get("jobPostings", [])
        for p in postings:
            d = http_get(base + p.get("externalPath", ""), headers=hdr, delay=DELAY)
            if d is not None and d.status_code == 200:
                j = map_workday(d.json().get("jobPostingInfo") or {}, company)
                if j and j.url and j.title:
                    jobs.append(j)
        if len(postings) < 20:
            break
        offset += 20
    return jobs


HANDLERS = {"lever": fetch_lever, "teamtailor_feed": fetch_teamtailor_feed, "workday": fetch_workday}


def fetch(profile: dict = None) -> List[JobOpportunity]:
    jobs: List[JobOpportunity] = []
    for company, (ats, ident) in ATS_CONFIG.items():
        try:
            found = HANDLERS[ats](company, ident)
            print(f"[+] {company} ({ats}) : {len(found)} offres en France")
            jobs += found
        except Exception as e:  # ne jamais lever
            print(f"[-] {company} ({ats}) : {e}")
    return jobs
