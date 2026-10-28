"""
GurbetIlan (https://www.gurbetilan.com) — petites annonces d'emploi de la diaspora turque, rubrique France.

Liste : /is-ilanlari/fransa/ (+ /page/N/), cartes `article.cpchild-job-card` (date jj.mm.aaaa, pays, ville).
Détail : chaque annonce /ads/<slug>/ porte un JSON-LD schema.org/JobPosting (datePosted, validThrough,
jobLocation.address.addressCountry) + la description complète. robots.txt n'interdit ni /is-ilanlari/ ni /ads/.
La candidature passe par un compte GurbetIlan (bouton « Giriş Yap ve Başvur ») : pas de contact public,
sauf téléphone/e-mail écrit dans le texte.

Fiabilité : date = datePosted (fiable, mise en ligne) ; pays = addressCountry structuré (FR exigé) ;
ville = préfixe du titre (« Nevers – … ») plus précis que addressLocality (souvent « Paris » par défaut).

Ce module expose aussi les détecteurs partagés par les sources turques :
`detect_language_requirements(text)` et `extract_visa_evidence(text)`.
"""
import datetime
import json
import re
from typing import Dict, List, Optional, Tuple

from models import JobOpportunity
from .common import clean_text, http_get, now_str, to_iso_date

SOURCE = "GurbetIlan France"
BASE = "https://www.gurbetilan.com"
LIST_URL = BASE + "/is-ilanlari/fransa/"
MAX_PAGES = 5
MAX_AGE_DAYS = 60
DELAY = 1.5

# --------------------------------------------------------------------------------------------
# Détecteurs partagés (langues, visa)
# --------------------------------------------------------------------------------------------
_LANG_WORDS = {
    "tr": r"türkçe\w*|turkish|turcophones?|turc|turque",
    "fr": r"fransızca\w*|french|français|francais|française|francophone",
    "en": r"ingilizce\w*|english|anglais|anglophone",
}
_ANY_LANG = re.compile(r"\b(?:" + "|".join(_LANG_WORDS.values()) + r"|almanca\w*|german|allemand|arapça\w*|arabic|arabe|flamanca\w*|néerlandais|dutch|ispanyolca\w*|spanish|espagnol|italyanca\w*|rusça\w*)\b", re.I)

# (niveau, motif) — l'ordre départage deux mots-clés à égale distance
_LEVELS: List[Tuple[str, str]] = [
    ("none", r"(?:bilme(?:k|si)?\s+)?(?:şart|gerekli|zorunlu)\s+değil\w*|bilmeyen|gerekmez|gerekmiyor|aranmaz|non\s+(?:requis|exigée?|obligatoire)|pas\s+(?:nécessaire|obligatoire|exigée?|requis)|not\s+(?:required|necessary|mandatory)|no|sans|aucune?"),
    ("fluent", r"ana\s?dil\w*|anadil\w*|akıcı|akici|hakim|ileri(?:\s+(?:seviye|düzey)\w*)?|çok\s+iyi|iyi\s+derecede|courante?|couramment|maîtrise|maitrise|bilingue|fluent(?:ly)?|native|natif|native-level|C1|C2"),
    ("intermediate", r"orta(?:\s+(?:seviye|düzey)\w*)?|intermédiaire|intermediate|conversational|B1|B2|bon\s+niveau|iyi"),
    ("basic", r"temel|başlangıç|baslangic|notions?|basic|basique|débutant|elementary|A1|A2"),
    ("preferred", r"tercih\w*|souhaitée?|appréciée?|un\s+plus|atout|preferred|nice\s+to\s+have|is\s+a\s+plus|avantage\w*|bonus"),
    ("required", r"bilen|bilmek|bilmeli|konuşan|konusan|konuşabilen|şart|zorunlu|gerekli|exigée?|requise?|obligatoire|required|mandatory|speaking|speaker|parlant|turcophones?|francophone|anglophone"),
]
_LEVEL_RE = [(lvl, re.compile(r"(?<!\w)(?:" + pat + r")(?!\w)", re.I)) for lvl, pat in _LEVELS]
_RANK = {"fluent": 5, "intermediate": 4, "required": 3, "basic": 2, "preferred": 1, "none": 0}


_LANG_OF = [(lang, re.compile(r"^(?:" + w + r")$", re.I)) for lang, w in _LANG_WORDS.items()]
_CONJ_ONLY = re.compile(r"^[\s,/&+-]*(?:ve|veya|ya\s+da|ile|and|or|et|ou)?[\s,/&+-]*$", re.I)
_CLAUSE_SPLIT = re.compile(r"[.;!?\n•()]")


def _levels_in(window: str, from_end: bool) -> List[Tuple[int, int, str]]:
    out = []
    for order, (lvl, rx) in enumerate(_LEVEL_RE):
        for m in rx.finditer(window):
            dist = (len(window) - m.end()) if from_end else m.start()
            out.append((dist, order, lvl))
    return out


def _pick(after: List[Tuple[int, int, str]], before: List[Tuple[int, int, str]]) -> Optional[str]:
    allm = after + before
    if not allm:
        return None
    lvls = {x[2] for x in allm}
    if "none" in lvls:          # « Fransızca bilmek şart değil », « français non requis »
        return "none"
    if "preferred" in {x[2] for x in after} or ("preferred" in lvls and not after):
        return "preferred"      # « İngilizce bilmek tercih sebebidir », « anglais apprécié »
    return min(allm)[2]


def detect_language_requirements(text: str) -> List[str]:
    """Exigences de langue explicites dans le texte (tr/fr/en), ex. ["tr:required", "fr:fluent"].

    Pour chaque mention de langue : mots-clés de niveau dans la même proposition (avant/après, sans
    franchir une autre langue) ; « none »/« preferred » l'emportent, sinon le plus proche.
    « Türkçe ve Fransızca dillerine hakim » : la langue coordonnée hérite du niveau suivant.
    tr est réduit à required / preferred / none. Rien n'est renvoyé pour une langue sans niveau explicite.
    """
    text = text or ""
    mentions = []
    for m in _ANY_LANG.finditer(text):
        lang = next((lg for lg, rx in _LANG_OF if rx.match(m.group(0))), None)
        mentions.append((m.start(), m.end(), lang, m.group(0).lower()))
    levels: List[Optional[str]] = [None] * len(mentions)
    for i in range(len(mentions) - 1, -1, -1):
        s, e, lang, word = mentions[i]
        nxt_start = mentions[i + 1][0] if i + 1 < len(mentions) else len(text)
        prv_end = mentions[i - 1][1] if i > 0 else 0
        raw_after = text[e:min(nxt_start, e + 45)]
        after = re.split(r"[,]", _CLAUSE_SPLIT.split(raw_after)[0])[0]
        before = _CLAUSE_SPLIT.split(text[max(prv_end, s - 30):s])[-1]
        lvl = _pick(_levels_in(after, False), _levels_in(before, True))
        if lvl is None and i + 1 < len(mentions) and nxt_start <= e + 45 and _CONJ_ONLY.match(text[e:nxt_start]):
            lvl = levels[i + 1]
        if lvl is None and (word.startswith("turcophone") or word in ("francophone", "anglophone")):
            lvl = "required"
        levels[i] = lvl
    # « Fluent French and English » : la langue coordonnée hérite du niveau précédent
    for i in range(1, len(mentions)):
        if levels[i] is None and levels[i - 1] and _CONJ_ONLY.match(text[mentions[i - 1][1]:mentions[i][0]]):
            levels[i] = levels[i - 1]
    found: Dict[str, str] = {}
    for (s, e, lang, word), lvl in zip(mentions, levels):
        if not lang or not lvl:
            continue
        if lang == "tr" and lvl in ("fluent", "intermediate", "basic"):
            lvl = "required"
        prev_lvl = found.get(lang)
        if prev_lvl is None or (lvl != "none" and _RANK[lvl] > _RANK[prev_lvl]):
            found[lang] = lvl
    return [f"{k}:{found[k]}" for k in ("tr", "fr", "en") if k in found]


_VISA_RE = re.compile(
    r"(?<!\w)(?:vize\w*|visas?|relocation|relocalisation|relocate|sponsor\w*|çalışma\s+izn\w*|calisma\s+izn\w*|"
    r"work\s+permit\w*|titre\s+de\s+séjour|permis\s+de\s+travail|oturum\s+izn\w*|taşınma\s+deste\w*|"
    r"yurt\s?dışından\s+(?:başvuru|aday)\w*)(?!\w)", re.I)


def extract_visa_evidence(text: str, limit: int = 300) -> str:
    """Extrait exact (phrase) de l'annonce qui parle de visa / relocation / sponsor ; "" sinon."""
    text = text or ""
    m = _VISA_RE.search(text)
    if not m:
        return ""
    start = max(text.rfind(c, 0, m.start()) for c in ".!?\n•") + 1
    ends = [i for i in (text.find(c, m.end()) for c in ".!?\n•") if i != -1]
    end = min(ends) + 1 if ends else len(text)
    sentence = text[start:end].strip()
    if len(sentence) > limit:
        a = max(0, m.start() - start - limit // 2)
        sentence = sentence[a: a + limit].strip()
    return sentence


def snippet_of(text: str, limit: int = 300) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:.-") + "…"


def lines_text(html_or_text: str, limit: int = 8000) -> str:
    """Comme clean_text mais conserve les retours à la ligne (puces, sections) pour l'extraction de phrases."""
    txt = re.sub(r"<\s*(?:br|/p|/li|/h\d|/div)\s*/?>", "\n", html_or_text or "", flags=re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"&nbsp;|&#160;|\xa0", " ", txt)
    txt = txt.replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">")
    lines = [re.sub(r"[ \t\r\f\v]+", " ", ln).strip() for ln in txt.split("\n")]
    return "\n".join(ln for ln in lines if ln)[:limit]


def utc_now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------------------------
# GurbetIlan
# --------------------------------------------------------------------------------------------
# Annonce d'une personne qui CHERCHE du travail
_SEEKER_RE = re.compile(r"\biş\s+ar[ıi]yorum|\bis\s+ariyorum|\biş\s+arıyor\b|\bişe\s+ihtiyacım|çalışabilirim\b|\bcherche\s+(?:un\s+)?(?:emploi|travail|job)\b|\bje\s+cherche\b|\blooking\s+for\s+(?:a\s+)?(?:job|work)\b", re.I)
# Annonce non-emploi (immobilier, vente, cession…)
_NONJOB_RE = re.compile(r"\b(?:satılık|satilik|kiralık|kiralik|devren|kiraya|satıyorum|satiyorum|ev\s+arkadaşı|oda\s+kiral\w*|à\s+vendre|à\s+louer|appartement|fonds\s+de\s+commerce)\b", re.I)
_EXPIRED_RE = re.compile(r"süresi\s+(?:doldu|dolmuş)|yayından\s+kaldırıl|ilan\s+kapan|annonce\s+expirée|this\s+ad\s+has\s+expired", re.I)
# Lieu de travail explicitement hors de France (« Brüksel'de faaliyet gösteren… »)
_FOREIGN_RE = re.compile(
    r"\b(?:brüksel|bruksel|belçika|belcika|anvers|anvers|liège|almanya|berlin|köln|koln|münih|frankfurt|hamburg|stuttgart|"
    r"hollanda|amsterdam|rotterdam|isviçre|isvicre|cenevre|zürih|zurih|basel|avusturya|viyana|ingiltere|londra|lüksemburg|"
    r"luksemburg|türkiye|turkiye|istanbul|i̇stanbul|ankara|izmir|i̇zmir|bursa|antalya)['’]?(?:de|da|te|ta|deki|daki|teki|taki)\b", re.I)
_PHONE_RE = re.compile(r"(?:\+33|0033|\b0)\s?[1-9](?:[\s.-]?\d{2}){4}\b")
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_JOB_WORDS = re.compile(r"aran|ar[ıi]yor|personel|eleman|usta|ustası|işçi|garson|şoför|sofor|kasiyer|aşçı|asci|için|icin", re.I)


def _jsonld_jobposting(html: str) -> Dict:
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            data = json.loads(m.group(1))
        except ValueError:
            continue
        for d in (data if isinstance(data, list) else data.get("@graph", [data]) if isinstance(data, dict) else []):
            if isinstance(d, dict) and d.get("@type") == "JobPosting":
                return d
    return {}


def parse_list(html: str) -> List[Dict]:
    """Cartes de la liste : url, date (YYYY-MM-DD), pays, ville, titre."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for card in soup.select("article.cpchild-job-card"):
        a = card.find("a", href=True)
        if not a or "/ads/" not in a["href"]:
            continue
        get = lambda cls: (card.find(class_=cls).get_text(" ", strip=True) if card.find(class_=cls) else "")
        out.append({
            "url": a["href"],
            "date": to_iso_date(get("cpchild-job-time")),
            "country": get("cpchild-job-country"),
            "city": get("cpchild-job-city"),
            "title": get("cpchild-job-title"),
        })
    return out


def city_from_title(title: str) -> str:
    """« Nevers – Dış Cephe … » -> « Nevers » ; "" si le titre ne commence pas par un lieu."""
    m = re.match(r"^\s*(.{2,40}?)\s+[–—\-:|]\s+\S", title or "")
    if not m:
        return ""
    cand = m.group(1).strip()
    if _JOB_WORDS.search(cand) or len(cand.split()) > 4:
        return ""
    return cand


def parse_detail(html: str, url: str, card: Optional[Dict] = None, today: Optional[datetime.date] = None) -> Tuple[Optional[JobOpportunity], str]:
    """Annonce -> (JobOpportunity | None, raison du rejet)."""
    from bs4 import BeautifulSoup
    card = card or {}
    today = today or datetime.date.today()
    jp = _jsonld_jobposting(html)
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    title = clean_text(jp.get("title") or (h1.get_text(" ", strip=True) if h1 else "") or card.get("title", ""), limit=300)
    desc_el = soup.select_one(".cpchild-single-description")
    description = lines_text(desc_el.get_text("\n", strip=True) if desc_el else (jp.get("description") or ""))
    feats = " | ".join(
        f"{f.select_one('.cpchild-feature-label').get_text(strip=True)}: {f.select_one('.cpchild-feature-value').get_text(strip=True)}"
        for f in soup.select(".cpchild-feature-item")
        if f.select_one(".cpchild-feature-label") and f.select_one(".cpchild-feature-value"))
    if not title:
        return None, "sans titre"

    addr = {}
    loc = jp.get("jobLocation")
    if isinstance(loc, list):
        loc = loc[0] if loc else {}
    if isinstance(loc, dict):
        addr = loc.get("address") or {}
    country = (addr.get("addressCountry") or "").upper()
    if isinstance(addr.get("addressCountry"), dict):
        country = (addr["addressCountry"].get("name") or "").upper()
    if country and country not in ("FR", "FRANCE", "FRANSA"):
        return None, f"hors France ({country})"
    if not country and card.get("country", "").lower() not in ("fransa", "france"):
        return None, "pays inconnu"

    posted = to_iso_date(jp.get("datePosted")) or card.get("date", "")
    if not posted:
        return None, "date inconnue"
    try:
        age = (today - datetime.date.fromisoformat(posted)).days
    except ValueError:
        return None, "date illisible"
    if age > MAX_AGE_DAYS:
        return None, f"trop ancienne ({posted})"
    valid = to_iso_date(jp.get("validThrough"))
    if valid and valid < today.isoformat():
        return None, f"expirée (validThrough {valid})"
    page_text = soup.get_text(" ", strip=True)
    if _EXPIRED_RE.search(page_text):
        return None, "marquée expirée"

    head = title + " " + description[:300]
    if _SEEKER_RE.search(head):
        return None, "demande d'emploi (iş arıyorum)"
    if _NONJOB_RE.search(title):
        return None, "annonce non-emploi"

    locality = (addr.get("addressLocality") or card.get("city") or "").strip()
    city = city_from_title(title) or locality
    # Lieu de travail annoncé ailleurs qu'en France sans que la France/la ville soit citée dans le texte
    fm = _FOREIGN_RE.search(description)
    if fm:
        fr_mentioned = re.search(r"\b(?:fransa|france|paris)\b", description, re.I) or (
            city and re.search(r"\b" + re.escape(city.split()[0]) + r"\b", description, re.I))
        if not fr_mentioned:
            return None, f"lieu ambigu (« {fm.group(0)} » dans le texte)"
    if not city:
        return None, "ville inconnue"

    contacts = sorted(set(_PHONE_RE.findall(description) + _EMAIL_RE.findall(description)))
    contact = ", ".join(contacts) if contacts else "Candidature via le compte GurbetIlan (bouton « Giriş Yap ve Başvur »)"
    full = (feats + "\n" + description).strip() if feats else description
    snippet = snippet_of(description)
    return JobOpportunity(
        title=title,
        title_fr=title,
        company="Annonceur GurbetIlan (non nommé)",
        location=f"{city}, France",
        city=city,
        country="FR",
        url=url,
        source=SOURCE,
        source_type="community",
        kind="offer",
        snippet=snippet,
        snippet_fr=snippet,
        description=full,
        posted_at=posted,
        verified_at=utc_now_iso(),
        discovered_at=now_str(),
        contact_info=contact,
        language_requirements=detect_language_requirements(full),
        visa_evidence=extract_visa_evidence(full),
        visa_sponsorship="",
    ), ""


def fetch(profile: dict = None) -> List[JobOpportunity]:
    jobs: List[JobOpportunity] = []
    seen = set()
    rejected: Dict[str, int] = {}
    today = datetime.date.today()
    try:
        for page in range(1, MAX_PAGES + 1):
            url = LIST_URL if page == 1 else f"{LIST_URL}page/{page}/"
            r = http_get(url, delay=DELAY)
            if r is None or r.status_code != 200:
                print(f"[-] GurbetIlan : liste p.{page} -> {getattr(r, 'status_code', 'réseau')}")
                break
            cards = parse_list(r.text)
            if not cards:
                break
            fresh = [c for c in cards if c["date"] and (today - datetime.date.fromisoformat(c["date"])).days <= MAX_AGE_DAYS]
            for card in fresh:
                if card["url"] in seen:
                    continue
                seen.add(card["url"])
                if card["country"] and card["country"].lower() not in ("fransa", "france"):
                    rejected["hors France"] = rejected.get("hors France", 0) + 1
                    continue
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
                    print(f"    GurbetIlan rejet : {why} — {card['url']}")
            # cartes triées par date décroissante : on s'arrête dès que la page contient des annonces trop vieilles
            if len(fresh) < len(cards):
                break
    except Exception as e:  # ne jamais lever
        print(f"[-] GurbetIlan : {e}")
    print(f"[+] GurbetIlan : {len(jobs)} offres en France ; rejets : {rejected}")
    return jobs
