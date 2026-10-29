"""
Yenibiriş (https://www.yenibiris.com) — job board turc, filtre PAYS = Fransa.

Accès (vérifié le 29/10/2026) :
- robots.txt autorise /is-ilanlari/* et /is-ilani/* (interdit *q=*, /api/, comptes…) : on n'utilise que l'URL
  de rubrique /is-ilanlari/fransa, jamais la recherche ?q=.
- /is-ilanlari/fransa applique le vrai filtre pays du site (facette « Ülke : Fransa (N) »). Quand il n'y a rien,
  la page affiche « Fransa iş ilanı bulunamamıştır. » et aucune carte (0 annonce le 29/10/2026).
- Cartes `div.listViewRows` : a.gtmTitle (URL /is-ilani/<slug>/<id>), .gtmCompanyName, .gtmLocation, date relative.
- Détail : JSON-LD schema.org/JobPosting (datePosted, validThrough, jobLocation.address.addressLocality/
  addressRegion, hiringOrganization) + texte complet dans `.mainInfos`.
Cloudflare passif (200 sans défi) ; en cas de 403/défi, on renvoie [] (pas de contournement).

Fiabilité : date = datePosted (fiable) ; pays = filtre structuré de la liste, revérifié sur la fiche (une fiche
située en Turquie est rejetée).
"""
import datetime
import html as htmllib
import json
import re
from typing import Dict, List, Optional, Tuple

from models import JobOpportunity
from .common import clean_text, http_get, now_str, to_iso_date
from .gurbetilan import detect_language_requirements, extract_visa_evidence, lines_text, snippet_of, utc_now_iso

SOURCE = "Yenibiriş (Ülke › Fransa)"
BASE = "https://www.yenibiris.com"
LIST_URL = BASE + "/is-ilanlari/fransa"
MAX_AGE_DAYS = 60
DELAY = 2.0

_FRANCE_RE = re.compile(r"\b(?:fransa|france)\b", re.I)
_TURKEY_RE = re.compile(r"\b(?:t[üu]rkiye|turkey|kktc|istanbul|i̇stanbul|ankara|izmir|i̇zmir)\b", re.I)
_EMPTY_RE = re.compile(r"iş ilanı bulunamamıştır", re.I)


def _jsonld_jobposting(html: str) -> Dict:
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            data = json.loads(m.group(1), strict=False)
        except ValueError:
            continue
        for d in (data if isinstance(data, list) else [data]):
            if isinstance(d, dict) and d.get("@type") == "JobPosting":
                return d
    return {}


def parse_list(html: str) -> List[Dict]:
    """Cartes de la liste : url, titre, entreprise, lieu (texte affiché)."""
    from bs4 import BeautifulSoup
    if _EMPTY_RE.search(html or ""):
        return []
    soup = BeautifulSoup(html, "html.parser")
    out, seen = [], set()
    for row in soup.select("div.listViewRows"):
        a = row.select_one("a.gtmTitle[href]")
        if not a or "/is-ilani/" not in a["href"]:
            continue
        url = a["href"] if a["href"].startswith("http") else BASE + a["href"]
        if url in seen:
            continue
        seen.add(url)
        comp = row.select_one(".gtmCompanyName")
        loc = row.select_one(".gtmLocation")
        out.append({
            "url": url,
            "title": (a.get("title") or a.get_text(" ", strip=True)).strip(),
            "company": ((comp.get("title") or comp.get_text(" ", strip=True)) if comp else "").strip(),
            "location": ((loc.get("title") or loc.get_text(" ", strip=True)) if loc else "").strip(),
        })
    return out


def _city_of(*places: str) -> str:
    """« Fransa - Paris » / « Paris, Fransa » -> « Paris » ; "" si seul le pays est indiqué."""
    for p in places:
        parts = [x.strip() for x in re.split(r"[-,/|]", p or "") if x.strip()]
        rest = [x for x in parts if not _FRANCE_RE.fullmatch(x) and not _TURKEY_RE.search(x)]
        if rest:
            return rest[-1]
    return ""


def parse_detail(html: str, url: str, card: Optional[Dict] = None,
                 today: Optional[datetime.date] = None) -> Tuple[Optional[JobOpportunity], str]:
    """Fiche -> (JobOpportunity | None, raison du rejet)."""
    from bs4 import BeautifulSoup
    card = card or {}
    today = today or datetime.date.today()
    jp = _jsonld_jobposting(html)
    soup = BeautifulSoup(html, "html.parser")
    title = clean_text(htmllib.unescape(jp.get("title") or card.get("title", "")), limit=300)
    if not title:
        return None, "sans titre"
    main = soup.select_one(".mainInfos")
    description = lines_text(str(main)) if main else lines_text(htmllib.unescape(jp.get("description") or ""))

    addr = {}
    loc = jp.get("jobLocation")
    if isinstance(loc, list):
        loc = loc[0] if loc else {}
    if isinstance(loc, dict):
        addr = loc.get("address") or {}
    locality = htmllib.unescape(str(addr.get("addressLocality") or "")).strip()
    region = htmllib.unescape(str(addr.get("addressRegion") or addr.get("addressCountry") or "")).strip()
    places = f"{locality} {region} {card.get('location', '')}"
    if _TURKEY_RE.search(places) and not _FRANCE_RE.search(places):
        return None, f"hors France ({(locality + ' ' + region).strip() or card.get('location', '')})"
    # La liste est filtrée par pays = Fransa ; sans carte, la fiche doit elle-même citer la France
    if not card and not _FRANCE_RE.search(places):
        return None, "pays non confirmé"

    posted = to_iso_date(jp.get("datePosted"))
    if not posted:
        return None, "date inconnue"
    age = (today - datetime.date.fromisoformat(posted)).days
    if age > MAX_AGE_DAYS:
        return None, f"trop ancienne ({posted})"
    valid = to_iso_date(jp.get("validThrough"))
    if valid and valid < today.isoformat():
        return None, f"expirée (validThrough {valid})"

    city = _city_of(card.get("location", ""), locality, region) or "France"
    org = jp.get("hiringOrganization")
    company = (org.get("name") if isinstance(org, dict) else org) or card.get("company") or "Employeur (Yenibiriş)"
    company = clean_text(htmllib.unescape(str(company)), limit=200)
    snippet = snippet_of(description)
    return JobOpportunity(
        title=title,
        title_fr=title,
        company=company,
        location=f"{city}, France" if city != "France" else "France",
        city=city,
        country="FR",
        url=url,
        source=SOURCE,
        source_type="board",
        kind="offer",
        snippet=snippet,
        snippet_fr=snippet,
        description=description,
        posted_at=posted,
        verified_at=utc_now_iso(),
        discovered_at=now_str(),
        contact_info="Candidature via Yenibiriş (compte requis)",
        language_requirements=detect_language_requirements(description),
        visa_evidence=extract_visa_evidence(description),
        visa_sponsorship="",
    ), ""


def fetch(profile: dict = None) -> List[JobOpportunity]:
    jobs: List[JobOpportunity] = []
    rejected: Dict[str, int] = {}
    today = datetime.date.today()
    try:
        r = http_get(LIST_URL, delay=DELAY)
        if r is None or r.status_code != 200:
            print(f"[-] Yenibiriş : liste -> {getattr(r, 'status_code', 'réseau')}")
            return []
        cards = parse_list(r.text)
        for card in cards:
            d = http_get(card["url"], delay=DELAY)
            if d is None or d.status_code != 200:
                rejected["détail inaccessible"] = rejected.get("détail inaccessible", 0) + 1
                continue
            job, why = parse_detail(d.text, card["url"], card, today)
            if job:
                jobs.append(job)
            else:
                key = why.split(" (")[0]
                rejected[key] = rejected.get(key, 0) + 1
                print(f"    Yenibiriş rejet : {why} — {card['url']}")
    except Exception as e:  # ne jamais lever
        print(f"[-] Yenibiriş : {e}")
    print(f"[+] Yenibiriş : {len(jobs)} offres en France ; rejets : {rejected}")
    return jobs
