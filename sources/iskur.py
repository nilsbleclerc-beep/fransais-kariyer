"""
İŞKUR (Türkiye İş Kurumu, https://esube.iskur.gov.tr) — offres publiques « Yurtdışı », pays = FRANSA.

Accès (vérifié le 29/10/2026) :
- robots.txt de esube.iskur.gov.tr : « Allow: / » (seul /Meslek/ViewMeslekDetayPopUp.aspx/ est interdit).
- La recherche publique AcikIsIlanAra.aspx est un formulaire ASP.NET (postback, aucune donnée personnelle) :
  « Çalışma Yeri » = Yurtdışı et « Ülke » = FRANSA (valeurs relues dans le formulaire à chaque passage).
  Le 29/10/2026 : 0 offre à l'étranger au total (25 448 en Turquie) — la source est « à surveiller ».
- Résultats : tableau #ctl04_ctlGridAcikIslerListeDetail ; par ligne : intitulé (meslek), n° d'ilan,
  « Çalışma Yeri : … », date limite de candidature (« Son Başvuru Tarihi »), nombre de postes.
  Nom de l'employeur masqué hors connexion.
- Détail public : AcikIsIlanDetay.aspx?uiID=<n°> (description « İş Tanımı », « Nitelik ve Beceriler », meslek).
  Pas de date de publication publique : posted_at reste vide (quality.py exige alors une URL vérifiée).
Pas d'anti-bot ni de géoblocage constatés.

Fiabilité : pays = filtre structuré du site ; une ligne dont le lieu est une province turque est rejetée.
"""
import datetime
import re
from typing import Dict, List, Optional, Tuple

from models import JobOpportunity
from .common import clean_text, http_get, http_post, now_str, to_iso_date
from .gurbetilan import detect_language_requirements, extract_visa_evidence, lines_text, snippet_of, utc_now_iso

SOURCE = "İŞKUR (Yurtdışı › Fransa)"
BASE = "https://esube.iskur.gov.tr"
SEARCH_URL = BASE + "/Istihdam/AcikIsIlanAra.aspx"
DETAIL_URL = BASE + "/Istihdam/AcikIsIlanDetay.aspx?uiID={}"
SEARCH_TARGET = "ctl04$ctlAcikIsPageCommand$CommandItem_Search"
NEXT_TARGET = "ctl04$ctlDataPagerDetay$btnNext"
MAX_PAGES = 5
DELAY = 2.0
_TR_HEADERS = {"Accept-Language": "tr-TR,tr;q=0.9"}


def tr_lower(s: str) -> str:
    return (s or "").replace("I", "ı").replace("İ", "i").lower()


def city_title(s: str) -> str:
    """Nom de ville française écrit en capitales turques : « PARİS » -> « Paris », « NICE » -> « Nice »."""
    low = (s or "").replace("İ", "i").replace("ı", "i").lower()
    return re.sub(r"[^\W\d_]+", lambda m: m.group(0)[:1].upper() + m.group(0)[1:], low)


def form_fields(soup) -> Dict[str, str]:
    """Champs à renvoyer au postback : hidden/text + valeur sélectionnée de chaque <select>."""
    data = {}
    for i in soup.find_all("input"):
        if i.get("name") and i.get("type") in ("hidden", "text"):
            data[i["name"]] = i.get("value", "")
    for sel in soup.find_all("select"):
        if not sel.get("name"):
            continue
        o = sel.find("option", selected=True) or sel.find("option")
        data[sel["name"]] = o.get("value", "") if o else ""
    return data


def _option_value(soup, select_id_suffix: str, label: str) -> Optional[str]:
    sel = soup.find("select", id=re.compile(re.escape(select_id_suffix) + "$"))
    if not sel:
        return None
    for o in sel.find_all("option"):
        if tr_lower(o.get_text(strip=True)) == tr_lower(label):
            return o.get("value")
    return None


def turkish_provinces(soup) -> List[str]:
    """Liste des 81 provinces lue dans le menu « İl » du formulaire (en minuscules turques)."""
    sel = soup.find("select", id=re.compile(r"ctlIl$"))
    if not sel:
        return []
    return [tr_lower(o.get_text(strip=True)) for o in sel.find_all("option") if o.get("value")]


def search_payload(form_soup) -> Optional[Dict[str, str]]:
    """Postback « Ara » avec Çalışma Yeri = Yurtdışı et Ülke = FRANSA ; None si le formulaire a changé."""
    yer = _option_value(form_soup, "ctlCalismaYeri", "Yurtdışı")
    ulke = _option_value(form_soup, "ctlUlke", "FRANSA")
    if yer is None or ulke is None:
        return None
    data = form_fields(form_soup)
    data.update({"ctl04$ctlCalismaYeri": yer, "ctl04$ctlUlke": ulke,
                 "__EVENTTARGET": SEARCH_TARGET, "__EVENTARGUMENT": ""})
    return data


def parse_results(html: str) -> List[Dict]:
    """Lignes du tableau de résultats : ilan_no, title, workplace, deadline (YYYY-MM-DD), positions."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    grid = soup.find("table", id=re.compile(r"ctlGridAcikIslerListeDetail$"))
    out = []
    if not grid:
        return out
    for tr in grid.find_all("tr"):
        a = tr.find("a", id=re.compile(r"_flag_\d+$"))
        if not a:
            continue
        no = re.search(r"_flag_(\d+)$", a["id"]).group(1)
        get = lambda suffix: (tr.find("span", id=re.compile(suffix + "$")).get_text(" ", strip=True)
                              if tr.find("span", id=re.compile(suffix + "$")) else "")
        yer = re.search(r"Çalışma Yeri\s*:\s*([^)]+)\)?", get("ctlCalismaYeriDL"))
        out.append({
            "ilan_no": no,
            "title": a.get_text(" ", strip=True),
            "workplace": yer.group(1).strip() if yer else "",
            "deadline": to_iso_date(get("ctlSonBasvuruTarihi")),
            "positions": get("Label9"),
            "employer_type": get("ctlIsverenTurDL"),
        })
    return out


def has_next_page(html: str) -> bool:
    return NEXT_TARGET.replace("$", "_") in (html or "") or f"__doPostBack(&#39;{NEXT_TARGET}" in (html or "")


def parse_detail(html: str, row: Dict, provinces: List[str],
                 today: Optional[datetime.date] = None) -> Tuple[Optional[JobOpportunity], str]:
    """Ligne de résultat + fiche publique -> (JobOpportunity | None, raison du rejet)."""
    from bs4 import BeautifulSoup
    today = today or datetime.date.today()
    title = clean_text(row.get("title", ""), limit=300)
    if not title:
        return None, "sans titre"
    workplace = row.get("workplace", "")
    parts = [p.strip() for p in workplace.split("/") if p.strip()]
    if parts and tr_lower(parts[0]) in provinces:
        return None, f"hors France ({workplace})"
    if row.get("deadline") and row["deadline"] < today.isoformat():
        return None, f"expirée (son başvuru {row['deadline']})"

    soup = BeautifulSoup(html or "", "html.parser")
    blocks = []
    for label, suffix in (("İş Tanımı", "ctlGenelSartlar"), ("Nitelik ve Beceriler", "ctlGenelSartlar2"),
                          ("Özel Şartlar", "ctlOzelSartlarText")):
        el = soup.find(id=re.compile(r"ctlIsIlanBilgileri_" + suffix + "$"))
        txt = lines_text(str(el)) if el else ""
        if txt:
            blocks.append(f"{label} :\n{txt}")
    meslek = soup.find(id=re.compile(r"repeaterMeslek_ctl\d+_ctlMeslekLabel$"))
    if meslek and meslek.get_text(strip=True):
        blocks.append(f"Meslek : {meslek.get_text(' ', strip=True)}")
    if not blocks:
        return None, "fiche vide ou inaccessible"
    extra = [f"Çalışma yeri : {workplace or 'Fransa'}"]
    if row.get("deadline"):
        extra.append(f"Son başvuru tarihi : {row['deadline']}")
    if row.get("positions"):
        extra.append(f"Açık pozisyon : {row['positions']}")
    description = "\n".join(blocks + extra)

    city_parts = [p for p in parts if tr_lower(p) not in ("fransa", "france")]
    city = city_title(city_parts[-1]) if city_parts else "France"
    snippet = snippet_of(blocks[0].split(":", 1)[-1])
    return JobOpportunity(
        title=title,
        title_fr=title,
        company="Employeur via İŞKUR (nom visible après connexion)",
        location=f"{city}, France" if city != "France" else "France",
        city=city,
        country="FR",
        url=DETAIL_URL.format(row["ilan_no"]),
        source=SOURCE,
        source_type="official_api",
        kind="offer",
        snippet=snippet,
        snippet_fr=snippet,
        description=description,
        posted_at="",
        verified_at=utc_now_iso(),
        discovered_at=now_str(),
        contact_info="Candidature sur esube.iskur.gov.tr (connexion e-Devlet / T.C. Kimlik No)",
        language_requirements=detect_language_requirements(description),
        visa_evidence=extract_visa_evidence(description),
        visa_sponsorship="",
    ), ""


def fetch(profile: dict = None) -> List[JobOpportunity]:
    from bs4 import BeautifulSoup
    jobs: List[JobOpportunity] = []
    rejected: Dict[str, int] = {}
    today = datetime.date.today()
    try:
        r = http_get(SEARCH_URL, headers=_TR_HEADERS, delay=DELAY)
        if r is None or r.status_code != 200:
            print(f"[-] İŞKUR : formulaire -> {getattr(r, 'status_code', 'réseau')}")
            return []
        form = BeautifulSoup(r.text, "html.parser")
        provinces = turkish_provinces(form)
        payload = search_payload(form)
        if payload is None:
            print("[-] İŞKUR : formulaire modifié (options Yurtdışı/FRANSA introuvables)")
            return []
        rows, seen = [], set()
        for page in range(1, MAX_PAGES + 1):
            res = http_post(SEARCH_URL, data=payload, headers=_TR_HEADERS, delay=DELAY)
            if res is None or res.status_code != 200:
                print(f"[-] İŞKUR : résultats p.{page} -> {getattr(res, 'status_code', 'réseau')}")
                break
            page_rows = [x for x in parse_results(res.text) if x["ilan_no"] not in seen]
            if not page_rows:
                break
            for x in page_rows:
                seen.add(x["ilan_no"])
            rows.extend(page_rows)
            if not has_next_page(res.text):
                break
            payload = form_fields(BeautifulSoup(res.text, "html.parser"))
            payload.update({"__EVENTTARGET": NEXT_TARGET, "__EVENTARGUMENT": ""})
        for row in rows:
            d = http_get(DETAIL_URL.format(row["ilan_no"]), headers=_TR_HEADERS, delay=DELAY)
            if d is None or d.status_code != 200:
                rejected["détail inaccessible"] = rejected.get("détail inaccessible", 0) + 1
                continue
            job, why = parse_detail(d.text, row, provinces, today)
            if job:
                jobs.append(job)
            else:
                key = why.split(" (")[0]
                rejected[key] = rejected.get(key, 0) + 1
                print(f"    İŞKUR rejet : {why} — n° {row['ilan_no']}")
    except Exception as e:  # ne jamais lever
        print(f"[-] İŞKUR : {e}")
    print(f"[+] İŞKUR : {len(jobs)} offres en France ; rejets : {rejected}")
    return jobs
