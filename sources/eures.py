"""
EURES (portail européen sur la mobilité de l'emploi) — offres en France EXIGEANT LE TURC.

Le moteur de recherche public du portail (europa.eu/eures/portal/jv-se) accepte un filtre
« langue requise » : on demande les offres situées en France (locationCodes ["fr"]) dont une
langue requise est le turc (isoCode "tr" ; le niveau C2 est cumulatif et renvoie tous les niveaux).
Ce n'est pas une API documentée : c'est le service public qu'utilise le site lui-même (robots.txt
l'autorise). Usage poli : 1 à 3 requêtes par scan.

Les offres françaises d'EURES viennent pour l'essentiel de France Travail : l'identifiant EURES,
décodé en base64, contient le numéro d'offre France Travail (ex. « 215TBZW 9 »), conservé dans
contact_info pour le dédoublonnage.
"""
import base64
import datetime
from typing import Dict, List, Optional

from models import JobOpportunity
from .common import clean_text, http_get, http_post, now_str, to_iso_date

SOURCE = "EURES (France Travail)"
SEARCH_URL = "https://europa.eu/eures/api/jv-searchengine/public/jv-search/search"
DETAIL_URL = "https://europa.eu/eures/portal/jv-se/jv-details/{id}?lang=fr"
# Fiche complète : langues exigées / souhaitées avec niveau, ville exacte
DETAIL_API = "https://europa.eu/eures/api/jv-searchengine/public/jv/id/{id}?requestLang=fr"
HEADERS = {
    "Content-Type": "application/json",
    "Origin": "https://europa.eu",
    "Referer": "https://europa.eu/eures/portal/jv-se/search?lang=fr",
}
PER_PAGE = 50
MAX_PAGES = 3

# Codes NUTS 2021 : départements d'Île-de-France (NUTS 3) et régions (NUTS 1)
NUTS_IDF = {
    "FR101": "Paris", "FR102": "Seine-et-Marne", "FR103": "Yvelines", "FR104": "Essonne",
    "FR105": "Hauts-de-Seine", "FR106": "Seine-Saint-Denis", "FR107": "Val-de-Marne", "FR108": "Val-d'Oise",
}
NUTS_REGIONS = {
    "FR1": "Île-de-France", "FRB": "Centre-Val de Loire", "FRC": "Bourgogne-Franche-Comté", "FRD": "Normandie",
    "FRE": "Hauts-de-France", "FRF": "Grand Est", "FRG": "Pays de la Loire", "FRH": "Bretagne",
    "FRI": "Nouvelle-Aquitaine", "FRJ": "Occitanie", "FRK": "Auvergne-Rhône-Alpes",
    "FRL": "Provence-Alpes-Côte d'Azur", "FRM": "Corse", "FRY": "Outre-mer",
}


def _body(page: int) -> Dict:
    return {
        "resultsPerPage": PER_PAGE, "page": page, "sortSearch": "MOST_RECENT", "keywords": [],
        "publicationPeriod": None, "occupationUris": [], "skillUris": [], "requiredExperienceCodes": [],
        "positionScheduleCodes": [], "sectorCodes": [], "educationAndQualificationLevelCodes": [],
        "positionOfferingCodes": [], "locationCodes": ["fr"], "euresFlagCodes": [], "otherBenefitsCodes": [],
        "requiredLanguages": [{"isoCode": "tr", "level": "C2"}], "minNumberPost": None,
        "sessionId": "fransais",
    }


def place_from_nuts(codes: List[str]) -> (str, str):
    """(city, location) lisibles à partir des codes NUTS ; city = département IDF si connu."""
    code = next((c for c in codes if c and c.upper().startswith("FR")), "")
    code = code.upper()
    if code in NUTS_IDF:
        dept = NUTS_IDF[code]
        return dept, f"{dept}, Île-de-France, France"
    region = NUTS_REGIONS.get(code[:3], "")
    return "", f"{region}, France" if region else "France"


def ft_offer_number(eures_id: str) -> str:
    """Numéro d'offre France Travail contenu dans l'identifiant EURES (base64), sinon ""."""
    try:
        raw = base64.b64decode(eures_id + "=" * (-len(eures_id) % 4)).decode("ascii", "ignore")
    except (ValueError, TypeError):
        return ""
    return raw.split()[0] if raw.strip() else ""


def map_job(jv: Dict) -> Optional[JobOpportunity]:
    jid = jv.get("id")
    if not jid:
        return None
    tr = (jv.get("translations") or {}).get("fr") or {}
    title = clean_text(tr.get("title") or jv.get("title") or "", limit=200)
    description = clean_text(tr.get("description") or jv.get("description") or "")
    if not title:
        return None
    codes = (jv.get("locationMap") or {}).get("FR") or []
    city, location = place_from_nuts(codes)
    posted = jv.get("creationDate")
    ft_num = ft_offer_number(jid)
    return JobOpportunity(
        title=title,
        title_fr=title,
        company=((jv.get("employer") or {}).get("name") or "Employeur non communiqué").strip(),
        location=location,
        url=DETAIL_URL.format(id=jid),
        source=SOURCE,
        snippet=description[:300],
        snippet_fr=description[:300],
        description=description,
        source_type="official_api",
        kind="offer",
        country="FR",
        city=city,
        posted_at=to_iso_date(posted) if posted else "",
        # Le filtre de recherche garantit que le turc fait partie des langues requises
        language_requirements=["tr:required"],
        contact_info=f"Offre France Travail n° {ft_num}" if ft_num else "",
        discovered_at=now_str(),
    )


def enrich_from_detail(job: JobOpportunity, eures_id: str) -> None:
    """Complète les langues (exigé → « fr:b2 », souhaité → « fr:preferred ») et la ville depuis la fiche."""
    resp = http_get(DETAIL_API.format(id=eures_id), headers={**HEADERS, "Accept": "application/json"}, delay=0.5)
    if resp is None or resp.status_code != 200:
        return
    try:
        data = resp.json() or {}
    except ValueError:
        return
    profiles = data.get("jvProfiles") or {}
    prof = profiles.get("fr") or next(iter(profiles.values()), {})
    reqs = []
    for lang in prof.get("positionLanguages") or []:
        code = (lang.get("languageCode") or "").lower()
        if not code:
            continue
        if lang.get("requiredSkillLevel"):
            reqs.append(f"{code}:{lang['requiredSkillLevel'].lower()}")
        elif lang.get("desiredSkillLevel"):
            reqs.append(f"{code}:preferred")
    if reqs:
        job.language_requirements = reqs
    loc = next(iter(prof.get("locations") or []), {}) or {}
    city = (loc.get("cityName") or "").strip()
    if city:
        job.city = city
        job.location = f"{city}, {job.location}" if job.location != "France" else f"{city}, France"


def fetch(profile: dict = None) -> List[JobOpportunity]:
    out: List[JobOpportunity] = []
    seen = set()
    max_age = int((profile or {}).get("max_age_days", 45))
    cutoff = (datetime.date.today() - datetime.timedelta(days=max_age)).isoformat()
    try:
        for page in range(1, MAX_PAGES + 1):
            resp = http_post(SEARCH_URL, json=_body(page), headers=HEADERS)
            if resp is None or resp.status_code != 200:
                print(f"[-] EURES p{page} : HTTP {getattr(resp, 'status_code', 'réseau')}")
                break
            data = resp.json() or {}
            jvs = data.get("jvs") or []
            for jv in jvs:
                job = map_job(jv)
                if job and job.url not in seen:
                    seen.add(job.url)
                    # Fiche détaillée seulement pour les offres assez récentes (les autres seront écartées)
                    if job.posted_at and job.posted_at >= cutoff:
                        enrich_from_detail(job, jv["id"])
                    out.append(job)
            if page == 1:
                print(f"[i] EURES : {data.get('numberRecords')} offres en France exigeant le turc")
            if len(jvs) < PER_PAGE:
                break
        print(f"[+] EURES : {len(out)} offres")
    except Exception as e:  # noqa: BLE001 — une source ne doit jamais faire tomber le scan
        print(f"[-] EURES : erreur {e}")
    return out
