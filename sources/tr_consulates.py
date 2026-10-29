"""
Missions diplomatiques turques en France (mfa.gov.tr) — annonces de RECRUTEMENT de personnel local
(« Türk Uyruklu Sözleşmeli Sekreter », « Mahalli Sekreter Alım İlanı », « Personel alımı »…).

Accès (vérifié le 29/10/2026) :
- 5 sites : ambassade et consulat général à Paris, consulats généraux à Lyon, Strasbourg et Marseille.
  robots.txt absent (404) : aucune restriction. Pas d'anti-bot.
- Liste : /Mission/Announcements (page unique, toutes les annonces depuis des années, ~4,5 Mo). La langue
  dépend de l'en-tête Accept-Language : on demande le turc (les annonces de recrutement sont en turc).
  Chaque <li><a href="/Mission/ShowAnnouncement/<id>"> porte .ks-announcement-header (titre),
  .ks-announcement-from (mission) et .ks-announcement-date (jj.mm.aaaa).
- Détail : /Mission/ShowAnnouncement/<id> -> #applicationHeader (titre), .ks-announcement-content (texte).
On garde les titres de recrutement (Sözleşmeli|Sekreter|Alım İlanı|Personel…), pas les résultats d'examen
(« Sonuç »). Le 29/10/2026 : aucune annonce ouverte (dernières : Marseille 06/2025, Paris 11/2023).

Fiabilité : date = date affichée par la mission (fiable) ; lieu = ville de la mission (en France).
Ces postes exigent en général une résidence légale en France et un examen : quality.py le signale.
"""
import datetime
import re
from typing import Dict, List, Optional, Tuple

from models import JobOpportunity
from .common import clean_text, http_get, now_str, to_iso_date
from .gurbetilan import detect_language_requirements, extract_visa_evidence, lines_text, snippet_of, utc_now_iso

SOURCE = "Missions turques en France (mfa.gov.tr)"
# (hôte, nom de la mission, ville du poste)
MISSIONS = [
    ("paris-be.mfa.gov.tr", "T.C. Paris Büyükelçiliği", "Paris"),
    ("paris-bk.mfa.gov.tr", "T.C. Paris Başkonsolosluğu", "Paris"),
    ("lyon-bk.mfa.gov.tr", "T.C. Lyon Başkonsolosluğu", "Lyon"),
    ("strazburg-bk.mfa.gov.tr", "T.C. Strazburg Başkonsolosluğu", "Strasbourg"),
    ("marsilya-bk.mfa.gov.tr", "T.C. Marsilya Başkonsolosluğu", "Marseille"),
]
MAX_AGE_DAYS = 60
DELAY = 2.0
_TR_HEADERS = {"Accept-Language": "tr-TR,tr;q=0.9"}

# Titres d'annonces de recrutement (pas « NATO Genel Sekreteri… » ni « …Personeli Hk. »)
RECRUIT_RE = re.compile(
    r"sözleşmeli\s+(?:sekreter|personel|uzman|memur|tercüman)|mahalli\s+(?:sekreter|personel|eleman)|"
    r"(?:sekreter|personel|eleman|uzman|tercüman|şoför|aşçı)\s+(?:alım|alımı|temini)\b|alım\s+ilanı|"
    r"(?:sekreter|personel)\s+sınav|istihdam\s+edilecek|recrutement|recrute", re.I)
# Communiqués de presse (« No: 164, … », « SC-11, … »), résultats d'examen, listes, convocations : pas des offres
NOT_OFFER_RE = re.compile(r"^\s*(?:no\s*:\s*\d|sc-\d)|genel\s+sekreter|sonu[cç]|kazanan|başarılı\s+olan|"
                          r"\blistesi\b|résultat|aday\s+meslek\s+memur", re.I)


def is_recruitment_title(title: str) -> bool:
    return bool(RECRUIT_RE.search(title or "")) and not NOT_OFFER_RE.search(title or "")


def parse_list(html: str, host: str) -> List[Dict]:
    """Annonces de la page /Mission/Announcements : url, titre, date (YYYY-MM-DD)."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html or "", "html.parser")
    out, seen = [], set()
    for a in soup.find_all("a", href=re.compile(r"/Mission/ShowAnnouncement/\d+")):
        head = a.find(class_="ks-announcement-header")
        date = a.find(class_="ks-announcement-date")
        if not head:
            continue
        url = a["href"] if a["href"].startswith("http") else f"https://{host}{a['href']}"
        if url in seen:
            continue
        seen.add(url)
        out.append({"url": url, "title": clean_text(head.get_text(" ", strip=True), limit=300),
                    "date": to_iso_date(date.get_text(" ", strip=True) if date else "")})
    return out


def parse_detail(html: str, item: Dict, mission: str, city: str,
                 today: Optional[datetime.date] = None) -> Tuple[Optional[JobOpportunity], str]:
    """Annonce -> (JobOpportunity | None, raison du rejet)."""
    from bs4 import BeautifulSoup
    today = today or datetime.date.today()
    soup = BeautifulSoup(html or "", "html.parser")
    head = soup.find(id="applicationHeader")
    title = clean_text(head.get_text(" ", strip=True) if head else item.get("title", ""), limit=300)
    if not title:
        return None, "sans titre"
    if not is_recruitment_title(title):
        return None, "pas une annonce de recrutement"
    body = soup.find(class_="ks-announcement-content")
    # Texte collé depuis Word : on recolle les lignes coupées en milieu de phrase
    description = re.sub(r"\n(?=[a-zçğıöşü(“\"])", " ", lines_text(str(body))) if body else ""
    if not description:
        return None, "texte vide"
    date_el = soup.find(class_="ks-announcement-date")
    posted = to_iso_date(date_el.get_text(" ", strip=True) if date_el else "") or item.get("date", "")
    if not posted:
        return None, "date inconnue"
    age = (today - datetime.date.fromisoformat(posted)).days
    if age > MAX_AGE_DAYS:
        return None, f"trop ancienne ({posted})"
    snippet = snippet_of(description)
    return JobOpportunity(
        title=title,
        title_fr=title,
        company=mission,
        location=f"{city}, France",
        city=city,
        country="FR",
        url=item["url"],
        source=SOURCE,
        source_type="official_api",
        kind="offer",
        snippet=snippet,
        snippet_fr=snippet,
        description=description,
        posted_at=posted,
        verified_at=utc_now_iso(),
        discovered_at=now_str(),
        contact_info=f"Dossier à déposer selon l'annonce ({mission})",
        language_requirements=detect_language_requirements(description),
        visa_evidence=extract_visa_evidence(description),
        visa_sponsorship="",
    ), ""


def fetch(profile: dict = None) -> List[JobOpportunity]:
    jobs: List[JobOpportunity] = []
    rejected: Dict[str, int] = {}
    today = datetime.date.today()
    for host, mission, city in MISSIONS:
        try:
            r = http_get(f"https://{host}/Mission/Announcements", headers=_TR_HEADERS, delay=DELAY)
            if r is None or r.status_code != 200:
                print(f"[-] {mission} : liste -> {getattr(r, 'status_code', 'réseau')}")
                continue
            for item in parse_list(r.text, host):
                if not is_recruitment_title(item["title"]):
                    continue
                if item["date"] and (today - datetime.date.fromisoformat(item["date"])).days > MAX_AGE_DAYS:
                    rejected["trop ancienne"] = rejected.get("trop ancienne", 0) + 1
                    continue
                d = http_get(item["url"], headers=_TR_HEADERS, delay=DELAY)
                if d is None or d.status_code != 200:
                    rejected["détail inaccessible"] = rejected.get("détail inaccessible", 0) + 1
                    continue
                job, why = parse_detail(d.text, item, mission, city, today)
                if job:
                    jobs.append(job)
                else:
                    key = why.split(" (")[0]
                    rejected[key] = rejected.get(key, 0) + 1
                    print(f"    Missions TR rejet : {why} — {item['url']}")
        except Exception as e:  # ne jamais lever
            print(f"[-] {mission} : {e}")
    print(f"[+] Missions turques en France : {len(jobs)} annonces de recrutement ; rejets : {rejected}")
    return jobs
