"""
Filtre qualité « pas de fausses joies » appliqué à toutes les offres collectées (sources/*).

Une offre (kind="offer") n'est gardée que si TOUTES les règles passent :
  1. le poste est en France (et le texte ne le place pas en Turquie ou ailleurs) ;
  2. elle est fraîche (posted_at <= profile.max_age_days) ou, date inconnue, son URL a été vérifiée aujourd'hui ;
  3. son URL est vivante, individuelle (pas une redirection vers une liste/l'accueil) et non expirée ;
  4. les exigences de langue sont compatibles avec le profil (tr natif, en A2-B1, fr A1) ;
  5. ce n'est pas un doublon (même URL, ou même titre/entreprise/ville).

Chaque offre gardée reçoit des raisons honnêtes (match_reasons_tr/fr) appuyées sur le texte de l'annonce,
un visa_evidence uniquement si l'annonce parle explicitement de visa/relocalisation, et un score simple.
Les offres écartées sont renvoyées avec leur raison pour l'audit (rejected_offers.json).
"""
import datetime
import re
import unicodedata
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, urlunparse

from sources import common

# ---------------------------------------------------------------------------
# Normalisation : minuscules, sans accents, « ı » -> « i », apostrophes typographiques -> « ' ».
# Le repliement est fait caractère par caractère pour garder les mêmes index que le texte
# original (on peut ainsi citer l'annonce telle quelle).
# ---------------------------------------------------------------------------
_SPECIAL = {"ı": "i", "’": "'", "‘": "'", "`": "'", "œ": "o", "æ": "a", "ß": "s"}


def _fold_char(c: str) -> str:
    if c in _SPECIAL:
        return _SPECIAL[c]
    base = "".join(x for x in unicodedata.normalize("NFKD", c) if not unicodedata.combining(x))
    base = base[:1].lower() if base else c
    return _SPECIAL.get(base, base) if len(base) == 1 else c


def fold(text: str) -> str:
    return "".join(_fold_char(c) for c in (text or ""))


def _quote(original: str, m: re.Match, limit: int = 60) -> str:
    q = re.sub(r"\s+", " ", original[m.start():m.end()]).strip(" .,;:-")
    return q[:limit]


# ---------------------------------------------------------------------------
# Lieux
# ---------------------------------------------------------------------------
FRENCH_PLACES = [
    "france", "fransa", "paris", "lyon", "marseille", "lille", "toulouse", "nice", "nantes", "bordeaux",
    "strasbourg", "montpellier", "rennes", "reims", "saint-etienne", "le havre", "toulon", "grenoble",
    "dijon", "angers", "nimes", "villeurbanne", "clermont-ferrand", "le mans", "aix-en-provence", "brest",
    "tours", "amiens", "limoges", "annecy", "perpignan", "boulogne-billancourt", "metz", "besancon",
    "orleans", "rouen", "mulhouse", "caen", "nancy", "argenteuil", "montreuil", "saint-denis", "roubaix",
    "tourcoing", "avignon", "nanterre", "creteil", "poitiers", "versailles", "courbevoie", "vitry-sur-seine",
    "colombes", "pau", "aulnay-sous-bois", "asnieres-sur-seine", "rueil-malmaison", "la rochelle",
    "calais", "cannes", "antibes", "beziers", "colmar", "bourges", "valence", "troyes", "chambery",
    "niort", "lorient", "vannes", "saint-nazaire", "bayonne", "la defense", "massy", "evry", "cergy",
    "sarcelles", "garges-les-gonesse", "meaux", "melun", "chartres", "belfort", "montbeliard", "haguenau",
    "oyonnax", "vienne", "bourg-en-bresse", "saint-priest", "venissieux", "vaulx-en-velin", "bron",
    "ile-de-france", "ile de france", "auvergne-rhone-alpes", "grand est", "hauts-de-france",
    "provence-alpes-cote d'azur", "occitanie", "nouvelle-aquitaine", "bretagne", "normandie",
    "pays de la loire", "bourgogne-franche-comte", "centre-val de loire", "alsace", "lorraine",
]
TURKISH_PLACES = [
    "istanbul", "ankara", "izmir", "bursa", "antalya", "adana", "konya", "gaziantep", "kocaeli", "gebze",
    "mersin", "kayseri", "eskisehir", "samsun", "denizli", "trabzon", "tekirdag", "corlu", "manisa",
    "sakarya", "mugla", "bodrum", "diyarbakir", "sanliurfa", "hatay", "malatya", "erzurum", "balikesir",
    "aydin", "edirne", "turkiye", "turkey", "turquie",
]
_FR_PLACE_RE = re.compile(r"(?<![\w-])(?:" + "|".join(re.escape(p) for p in FRENCH_PLACES) + r")(?![\w-])")
_TR_PLACE_RE = re.compile(r"(?<![\w-])(?:" + "|".join(re.escape(p) for p in TURKISH_PLACES) + r")(?!\w)")
# Code département France Travail : « 69 - LYON 03 »
_FR_DEPT_RE = re.compile(r"^\s*(?:\d{2}|2[ab]|97\d)\s*-\s*\w")
_TR_CITIES = "|".join(re.escape(p) for p in TURKISH_PLACES[:-3])
# « İstanbul ofisimizde », « Ankara'da çalışacak », « lieu de travail : Izmir », « based in Istanbul »
_TR_WORKPLACE_RE = re.compile(
    r"\b(?:" + _TR_CITIES + r")(?:'?(?:da|de|ta|te|daki|deki))?\s+(?:\w+\s+){0,2}?"
    r"(?:ofis\w*|merkez\w*|sube\w*|lokasyon\w*|calis\w*|gorev\w*|yerlesik|isyeri\w*)"
    r"|(?:lieu de travail|work location|location|based in|konum|calisma yeri|is yeri)\s*:?\s*(?:" + _TR_CITIES + r")\b"
)


def _is_french_place(s: str) -> bool:
    f = fold(s)
    return bool(_FR_PLACE_RE.search(f) or _FR_DEPT_RE.match(f))


def check_location(job) -> Optional[Tuple[str, str]]:
    """Renvoie (code, détail) si l'offre n'est pas en France, sinon None."""
    fields = f"{job.city} | {job.location}"
    f_fields = fold(fields)
    f_title = fold(job.title)
    country = (job.country or "").strip().upper()

    m = _TR_PLACE_RE.search(f_fields)
    if m and not _FR_PLACE_RE.search(f_fields):
        return "in_turkey", f"Lieu de travail en Turquie : {fields.strip(' |')}"
    m = _TR_PLACE_RE.search(f_title)
    if m and not _FR_PLACE_RE.search(f_title):
        return "in_turkey", f"Titre situant le poste en Turquie : {job.title[:80]}"
    if country and country != "FR":
        return "not_in_france", f"Pays : {country}"

    french_fields = _is_french_place(job.city) or _is_french_place(job.location)
    # Une ville française précise (pas seulement « France / Fransa ») l'emporte sur la description
    french_city = any(p not in ("france", "fransa") for p in _FR_PLACE_RE.findall(f"{f_fields} {f_title}"))
    text = f"{job.snippet} {job.description}"
    m = _TR_WORKPLACE_RE.search(fold(text))
    if m and not french_city:
        return "in_turkey", f"Annonce : « {_quote(text, m)} »"
    if country == "FR" or french_fields:
        return None
    return "not_in_france", f"Lieu non reconnu comme français : {fields.strip(' |') or '(vide)'}"


# ---------------------------------------------------------------------------
# Langues
# ---------------------------------------------------------------------------
RANK = {"a1": 1, "a2": 2, "b1": 3, "b2": 4, "c1": 5, "c2": 6, "native": 7}
FLUENT = 5  # « courant / fluent / akıcı » ~ C1
REQUIRED_NO_LEVEL = 3  # « exigé » sans niveau ~ B1

LANG_TOKENS = {
    "fr": r"(?:francais|french|fransizca|langue francaise)(?:'?\w+)?",
    "en": r"(?:anglais|english|ingilizce|langue anglaise)(?:'?\w+)?",
}
_ADVANTAGE_RE = re.compile(
    r"\b(?:plus|atout|souhaite|apprecie|avantage|bonus|serait|optionnel|facultatif|optional|nice to have|"
    r"preferred|tercih|avantaj\w*|artidir|arti|olumlu)\b")
_CEFR = r"(a1|a2|b1|b2|c1|c2)"


def _lang_patterns(T: str) -> List[Tuple[re.Pattern, Optional[int]]]:
    """(regex, rang) ; rang None = lu dans le groupe CEFR capturé."""
    p = [
        (rf"\b{T}\s+\(?(?:courant|parfait|fluide|impeccable|natif|native|bilingue|irreprochable)s?\b", FLUENT),
        (rf"\b{T}\s*(?:et|ve|and|,|/)\s*\w+\s+\(?(?:courants?|fluent|akici)\b", FLUENT),
        (rf"\b(?:parfaite\s+|excellente\s+|tres bonne\s+|bonne\s+)?maitrise\s+(?:parfaite\s+)?(?:du|de l'|de l|de la langue|en)\s*{T}", FLUENT),
        (rf"\b(?:excellent|tres bon)\s+niveau\s+(?:de|d'|en)\s*{T}", FLUENT),
        (rf"\bbon\s+niveau\s+(?:de|d'|en)\s*{T}", 4),
        (rf"\bbilingue\s+(?:en\s+)?{T}", FLUENT),
        (rf"\b(?:fluent|fluency|fluently|native|proficient|excellent|perfect|full professional)\s+(?:command of\s+|knowledge of\s+)?(?:in\s+)?"
         rf"(?:written and spoken\s+|spoken and written\s+|written and verbal\s+)?{T}", FLUENT),
        (rf"\b(?:strong|business[- ]level|very good|good command of)\s+(?:in\s+)?{T}", 4),
        (rf"\b{T}\s+(?:fluency|native speaker|proficiency|at a professional level)\b", FLUENT),
        (rf"\b{T}[^.;\n]{{0,40}}professional (?:working )?proficiency", FLUENT),
        (rf"\b(?:akici|ileri\s+(?:duzey|seviye|derece)\w*|cok iyi(?:\s+(?:derecede|seviyede|duzeyde))?|anadil\w*\s+(?:seviyesinde|duzeyinde))\s+{T}", FLUENT),
        (rf"\biyi\s+(?:derecede|seviyede|duzeyde)\s+{T}", 4),
        (rf"\b{T}\s+(?:\w+\s+){{0,2}}?(?:akici|ileri\s+(?:duzey|seviye)\w*|iyi\s+derecede)", FLUENT),
        # « Fransızca dillerine vakıf » / « Fransızcaya hakim » = maîtrise de la langue
        (rf"\b{T}\w*\s+(?:\w+\s+){{0,2}}?(?:vakif|hakim)\b", FLUENT),
        (rf"\b{T}\s+bilen\b", REQUIRED_NO_LEVEL),
        (rf"\b{T}\s*:?\s*(?:exige|obligatoire|indispensable|requis|imperatif|required|mandatory|essential|zorunlu|sart|gerekli)\b", REQUIRED_NO_LEVEL),
        (rf"\b(?:exige|obligatoire|indispensable|required|mandatory)\s*:?\s*{T}", REQUIRED_NO_LEVEL),
        (rf"\b{T}\s*:?\s*(?:\w+\s*:?\s*){{0,2}}?(?:niveau\s+|level\s+|seviye\w*\s+)?{_CEFR}\b", None),
        (rf"\b(?:niveau\s+|level\s+)?{_CEFR}\s*(?:\(\w+\)\s*)?(?:en\s+|in\s+|de\s+|d')?{T}", None),
    ]
    return [(re.compile(rx), r) for rx, r in p]


LANG_PATTERNS = {lang: _lang_patterns(T) for lang, T in LANG_TOKENS.items()}
# « professional proficiency » seul (sans langue citée) : annonce en anglais -> anglais avancé
_PRO_PROFICIENCY_RE = re.compile(r"\bprofessional (?:working )?proficiency\b")
# Langue de travail anglaise : anglais professionnel implicite (~B2)
_EN_WORKING_LANG_RE = re.compile(
    r"\b(?:working language is english|english[- ](?:speaking|only) (?:environment|team|company)|"
    r"langue de travail\s*:?\s*(?:est\s+)?l?'?anglais|calisma dili\s*:?\s*ingilizce)")

_NO_FRENCH_RE = re.compile(
    r"\b(?:francais\s+(?:non|pas)\s+(?:requis|exige|obligatoire|necessaire|indispensable)|"
    r"pas besoin de (?:parler |savoir parler )?(?:le )?francais|sans (?:parler )?francais|"
    r"no french (?:required|needed|necessary)|french (?:is )?not (?:required|needed|necessary|mandatory)|"
    r"fransizca\s+(?:sart degil|gerekmiyor|gerekmemektedir|zorunlu degil|bilmek (?:sart degil|gerekmiyor|zorunlu degil))|"
    r"fransizca bilmeyen|dil (?:sarti|bilgisi) (?:yok|aranmiyor|aranmamaktadir)|dil bilmeyen)")

_TR_STRONG_RE = re.compile(
    r"\b(?:turc|turque|turkish|turkce)\s*:?\s*\(?(?:courant|exige|obligatoire|indispensable|souhaite|apprecie|requis|"
    r"natif|parle|bilingue|est un plus|serait un plus|un plus|atout|required|speaker|speaking|native|fluent|a plus|"
    r"bilen|konusan|bilmek|zorunlu|sart|gerekli|ana ?dil\w*|is a plus|preferred)\b"
    r"|\b(?:turcophone|parlant (?:le )?turc|parler (?:le )?turc|langue turque|maitrise (?:du|de la langue) turc\w*|"
    r"bilingue (?:en )?turc|(?:fluent|native|proficient) (?:in )?turkish|speaks? turkish|turkish[- ]speaking|"
    r"turkce (?:ve|veya) \w+ bilen|ana ?dili turkce)\b")
_TR_WEAK_RE = re.compile(r"\b(?:turc|turque|turcs|turques|turkish|turkce|turk)\b")

# Annonce rédigée en turc (mots-outils fréquents)
_TR_WORDS = {"ve", "bir", "icin", "ile", "olan", "araniyor", "eleman", "ilan", "calisacak", "bilen",
             "deneyimli", "tecrubeli", "maas", "gerekli", "olarak", "is", "personel", "aliyoruz", "sahip",
             "bay", "bayan", "tam", "zamanli", "sigortali", "yapilacak", "olmak", "veya"}

# Métiers de terrain : peu de qualification linguistique attendue (titre de l'annonce)
_FIELD_JOB_RE = re.compile(
    r"\b(?:manutention\w*|preparat\w* de commandes?|cariste|ouvri\w+|agent (?:d'entretien|de proprete|de production|"
    r"de nettoyage|de quai|logistique)|nettoyage|plongeu\w+|commis|aide[- ]cuisin\w+|cuisinier\w*|macon\w*|carreleur\w*|"
    r"peintre|plaquiste|coffreur\w*|manoeuvre|man.uvre|boulang\w+|bouch\w+|chauffeur\w*|livreu\w+|magasinier\w*|"
    r"couturi\w+|operat\w+ de production|cueilleu\w+|saisonni\w+|vendang\w+|electricien\w*|plombier\w*|soudeu\w+|"
    r"menuisier\w*|charpentier\w*|etancheur\w*|facadier\w*|bardeur\w*|grutier\w*|terrassier\w*|jardinier\w*|paysagiste|"
    r"conducteur d'engins|pizzaiolo|kebab|doner|garson|bulasik\w*|kasap|firinci|insaat|siva\w*|boyaci|iscisi|isci|"
    r"sofor\w*|kurye|depo\w*|temizlik\w*|asci\w*|usta\w*|kalfa|berber|kuafor\w*|tezgahtar|komi|fayans\w*|alci\w*|"
    r"seramik\w*|kaynakci|elektrikci|tesisatci|marangoz|forklift\w*|operator\w*|cobanlik|tarim|bahce)\b")

LEVEL_ALIASES = {"native": 7, "natif": 7, "fluent": FLUENT, "courant": FLUENT, "required": REQUIRED_NO_LEVEL,
                 "basic": 2, "none": 0}


def _profile_level(value) -> int:
    """« A2-B1 » -> 2 (borne basse), « native » -> 7, « A1 » -> 1."""
    v = str(value or "").lower()
    if any(w in v for w in ("native", "natif", "ana")):
        return 7
    ranks = [RANK[x] for x in re.findall(r"\b(a1|a2|b1|b2|c1|c2)\b", v)]
    return min(ranks) if ranks else 0


def _structured_levels(reqs: List[str]) -> Dict[str, Tuple[Optional[int], bool]]:
    """language_requirements (« fr:required », « tr:preferred », « en:b2 ») -> {lang: (rang|None, atout?)}."""
    out = {}
    for item in reqs or []:
        if ":" not in str(item):
            continue
        lang, lvl = [x.strip().lower() for x in str(item).split(":", 1)]
        if lvl in ("preferred", "advantage", "plus", "optional", "souhaite", "desirable"):
            out[lang] = (None, True)
        elif lvl in RANK:
            out[lang] = (RANK[lvl], False)
        elif lvl in LEVEL_ALIASES:
            out[lang] = (LEVEL_ALIASES[lvl], False)
    return out


def analyze_languages(job) -> Dict:
    """Détecte les exigences de langue (structurées + texte). Renvoie un dict d'analyse."""
    original = f"{job.title}. {job.snippet}. {job.description}"
    text = fold(original)
    res = {"fr": (0, ""), "en": (0, ""), "tr_strong": "", "tr_weak": "", "no_french": "",
           "turkish_text": False, "structured": _structured_levels(job.language_requirements)}

    for lang, patterns in LANG_PATTERNS.items():
        best, quote = 0, ""
        for rx, rank in patterns:
            for m in rx.finditer(text):
                after = text[m.end():m.end() + 45]
                if _ADVANTAGE_RE.search(after.split(".")[0]):
                    continue  # « français courant serait un plus » : atout, pas exigence
                if re.match(r"\s*(?:degil|olmasa da|aranmaz|gerekmez)\b", after):
                    continue  # « Fransızca şart değil » : négation, pas exigence
                r = rank if rank is not None else RANK.get(m.group(1), 0)
                if r > best:
                    best, quote = r, _quote(original, m)
        res[lang] = (best, quote)

    if res["en"][0] < FLUENT:
        m = _PRO_PROFICIENCY_RE.search(text)
        if m and "proficiency" not in fold(res["fr"][1]):
            res["en"] = (FLUENT, _quote(original, m))
    if res["en"][0] < 4:
        m = _EN_WORKING_LANG_RE.search(text)
        if m:
            res["en"] = (4, _quote(original, m))

    for lang, (lvl, adv) in res["structured"].items():
        if lang in ("fr", "en") and lvl and lvl > res[lang][0]:
            res[lang] = (lvl, f"{lang}:{'required' if lvl == REQUIRED_NO_LEVEL else lvl}")

    m = _NO_FRENCH_RE.search(text)
    if m:
        res["no_french"] = _quote(original, m)
    st = res["structured"].get("fr")
    if st and st[0] == 0 and not res["no_french"]:
        res["no_french"] = "fr:none"

    m = _TR_STRONG_RE.search(text)
    if m:
        res["tr_strong"] = _quote(original, m)
    elif "tr" in res["structured"] and res["structured"]["tr"][0] != 0:
        res["tr_strong"] = "tr:" + ("atout" if res["structured"]["tr"][1] else "requis")
    else:
        m = _TR_WEAK_RE.search(text)
        if m:
            res["tr_weak"] = _quote(original, m, 80)

    words = re.findall(r"\w+", text)
    res["turkish_text"] = sum(1 for w in words if w in _TR_WORDS) >= 4
    return res


# ---------------------------------------------------------------------------
# Visa
# ---------------------------------------------------------------------------
_VISA_RE = re.compile(
    r"\b(?:visa|vize\w*|relocation|relocalisation|relokasyon|(?:visa\s+)?sponsorship|"
    r"sponsoris\w+\s+(?:de\s+|du\s+|your\s+)?(?:visa|titre)|titre de sejour|permis de travail|"
    r"autorisation de travail|work permit|calisma izn\w*|passeport talent|talent passport)\b")
_VISA_NEG_RE = re.compile(
    r"(?:valide|en cours de validite|en regle|titulaire|exige|requis|obligatoire|must|already|deja|olmali|"
    r"sahip|zorunlu|gerekli|have the right|right to work|eligible|ne (?:pouvons|proposons|sponsorisons) pas|"
    r"pas de (?:sponsor|parrainage|visa)|sans sponsor|no (?:visa )?sponsor|not (?:able to )?sponsor|"
    r"unable to sponsor|cannot sponsor|does not (?:offer|provide) (?:visa )?sponsor|sponsorship is not|"
    r"yok|verilmemektedir|saglanmamaktadir|saglanmaz|olanlar|olan aday)")


# Annonces qui demandent un droit au travail DÉJÀ acquis : la candidate (en Turquie) devra passer
# par un visa ; on garde l'offre mais on l'avertit clairement (texte replié par fold()).
_PERMIT_RE = re.compile(
    r"calisma izni(?:ne)? (?:bulunan|olan|sahibi|sahip|olmasi|gerekli|sart|zorunlu)|"
    r"(?:yasal )?(?:calisma (?:ve|veya) )?oturum izni(?:ne)? (?:bulunan|olan|olmayan|sahibi|sahip|olmasi)|"
    r"yasal (?:calisma|oturum) (?:izni|iznine|hakki)|kagidi (?:olan|bulunan)|kagitli|"
    r"ab vatandasi|avrupa (?:birligi )?vatandasi|avrupa pasaport|"
    r"titre de sejour (?:valide|en cours)|autorisation de travail (?:valide|en cours)|papiers en regle|"
    r"right to work in (?:france|the eu|europe)|eligible to work in (?:france|the eu|europe)|valid work permit")
# Annonces qui demandent d'habiter sur place : pas bloquant, elle s'installera en Île-de-France
_RESIDENCE_RE = re.compile(
    r"(?:fransa|paris|lyon|marsilya|avrupa)(?:'?(?:da|de|ta|te))?(?: veya [a-z ]{1,30})? (?:yasal olarak )?(?:ikamet eden|yasayan|oturan)|"
    r"(?:cevresinde|civarinda|bolgesinde|yakininda|yakin cevresinde) (?:ikamet eden|yasayan|oturan)|"
    r"resid(?:ant|ent|ence) (?:en france|a paris|en ile)|must (?:live|reside) in")

IDF_RE = re.compile(
    r"\b(?:paris|ile[- ]de[- ]france|idf|seine[- ]saint[- ]denis|hauts[- ]de[- ]seine|val[- ]de[- ]marne|"
    r"val[- ]d'oise|essonne|yvelines|seine[- ]et[- ]marne|torcy|levallois|saint[- ]denis|aubervilliers|"
    r"montreuil|nanterre|boulogne|argenteuil|creteil|vitry|bobigny|pantin|clichy|sarcelles|"
    r"(?:75|77|78|91|92|93|94|95)\d{3}|(?:75|77|78|91|92|93|94|95) bolgesi)\b")


def _excerpt(original: str, m, words: int = 4) -> str:
    """Extrait lisible du texte ORIGINAL (fold() conserve les positions), coupé aux limites de mots."""
    before = re.findall(r"\S+", original[:m.start()])[-words:]
    after = re.findall(r"\S+", original[m.end():])[:words]
    core = original[m.start():m.end()]
    return re.sub(r"\s+", " ", " ".join(before + [core] + after)).strip(" .,;:-()")


def permit_requirement(original: str) -> str:
    """Extrait exigeant un droit au travail / titre de séjour déjà acquis, sinon ""."""
    m = _PERMIT_RE.search(fold(original))
    return _excerpt(original, m) if m else ""


def residence_requirement(original: str) -> str:
    """Extrait exigeant d'habiter déjà sur place, sinon ""."""
    m = _RESIDENCE_RE.search(fold(original))
    return _excerpt(original, m) if m else ""


_MONTHS = {"ocak": 1, "subat": 2, "mart": 3, "nisan": 4, "mayis": 5, "haziran": 6, "temmuz": 7, "agustos": 8,
           "eylul": 9, "ekim": 10, "kasim": 11, "aralik": 12, "janvier": 1, "fevrier": 2, "mars": 3, "avril": 4,
           "mai": 5, "juin": 6, "juillet": 7, "aout": 8, "septembre": 9, "octobre": 10, "novembre": 11,
           "decembre": 12}
_EVENT_RE = re.compile(r"\b(?:fuar|organizasyon|etkinlik|festival|kongre|salon|evenement|event|exposition)")
_DATE_RANGE_RE = re.compile(r"\b(\d{1,2})(?:\s*(?:-|–|ile|au|et)\s*(\d{1,2}))?\s+(" + "|".join(_MONTHS) + r")\w*(?:\s+(20\d\d))?")


def event_already_over(job, today: datetime.date) -> str:
    """Pour une mission liée à un événement daté (salon, fuar…) : extrait si toutes ses dates sont passées."""
    text = fold(f"{job.title} {job.description or job.snippet}")
    if not _EVENT_RE.search(text):
        return ""
    ref_year = int(str(job.posted_at)[:4]) if str(job.posted_at)[:4].isdigit() else today.year
    ends = []
    for m in _DATE_RANGE_RE.finditer(text):
        day = int(m.group(2) or m.group(1))
        year = int(m.group(4)) if m.group(4) else ref_year
        try:
            ends.append((datetime.date(year, _MONTHS[m.group(3)], day), m.group(0)))
        except ValueError:
            continue
    if ends and all(d < today for d, _ in ends):
        return max(ends)[1]
    return ""


_FOREIGN_DEST_RE = re.compile(
    r"\b(?:portugal|lisbo[an]n?e?|porto|espagne|spain|espana|madrid|barcelon[ae]|allemagne|germany|almanya|berlin|"
    r"belgique|belgium|belcika|bruxelles|brussels|bruksel|suisse|switzerland|isvicre|geneve|zurich|luxembourg|"
    r"united kingdom|ingiltere|london|londres|pays[- ]bas|netherlands|hollanda|amsterdam|dubai|qatar|katar|"
    r"canada|kanada|malte|malta|chypre|cyprus|kibris|italie|italy|italya|irlande|ireland)\b")


def foreign_destination(job) -> str:
    """Pays étranger cité dans le TITRE alors qu'aucune ville française n'y figure : poste hors de France."""
    title = fold(job.title)
    m = _FOREIGN_DEST_RE.search(title)
    if not m or is_idf(job) and IDF_RE.search(title):
        return ""
    return m.group(0)


def is_idf(job) -> bool:
    return bool(IDF_RE.search(fold(f"{job.city} {job.location} {job.title}")))


def find_visa_evidence(original: str) -> Tuple[str, str]:
    """(preuve_positive, alerte_negative) : extrait de l'annonce mentionnant explicitement le visa."""
    text = fold(original)
    neg = ""
    for m in _VISA_RE.finditer(text):
        window = text[max(0, m.start() - 50):m.end() + 50]
        start = max(0, m.start() - 40)
        end = min(len(original), m.end() + 60)
        snippet = re.sub(r"\s+", " ", original[start:end]).strip()
        if _VISA_NEG_RE.search(window):
            neg = neg or snippet
            continue
        return snippet, ""
    return "", neg


# ---------------------------------------------------------------------------
# URL
# ---------------------------------------------------------------------------
_URL_CACHE: Dict[str, Dict] = {}
EXPIRED_MARKERS = [
    "ilan yayindan kaldirildi", "bu ilan artik", "ilanin suresi dol", "ilan suresi dol", "ilan kaldirilmistir",
    "bu ilan yayinda degil", "ilan pasif", "offre n'est plus disponible", "offre n'est plus en ligne",
    "offre expiree", "cette offre a expire", "offre a ete pourvue", "offre pourvue", "annonce n'est plus disponible",
    "annonce a expire", "no longer available", "no longer accepting applications", "position has been filled",
    "job not found", "this job has expired", "job has been closed", "job is no longer", "posting has expired",
    "job posting is closed",
]
_LIST_PATH_RE = re.compile(
    r"/(?:search|recherche|jobs|offres|offres-emploi|emplois?|is-ilanlari|ilanlar|careers?|carrieres?|kariyer|"
    r"404|not-?found|expired?)/?$")
_UNVERIFIABLE_STATUSES = {401, 403, 405, 429, 503, 999}


def normalize_url(url: str) -> str:
    try:
        p = urlparse((url or "").strip())
    except ValueError:
        return (url or "").strip().lower()
    query = "&".join(q for q in p.query.split("&") if q and not q.lower().startswith(("utm_", "ref=", "source=")))
    return urlunparse((p.scheme.lower() or "https", p.netloc.lower().removeprefix("www."),
                       p.path.rstrip("/"), "", query, ""))


def check_url(url: str, delay: float = 0.3) -> Dict:
    """GET l'URL (cache). Renvoie {ok, code, detail, unverifiable}."""
    if url in _URL_CACHE:
        return _URL_CACHE[url]
    res = {"ok": False, "code": "url_dead", "detail": "", "unverifiable": False}
    p0 = urlparse(url or "")
    if p0.scheme not in ("http", "https") or not p0.netloc:
        res["detail"] = "URL invalide"
        _URL_CACHE[url] = res
        return res
    r = common.http_get(url, delay=delay)
    if r is None:
        res.update(code="url_unverifiable", detail="Erreur réseau", unverifiable=True)
    elif r.status_code in (404, 410):
        res["detail"] = f"HTTP {r.status_code}"
    elif r.status_code in _UNVERIFIABLE_STATUSES:
        res.update(code="url_unverifiable", detail=f"HTTP {r.status_code} (site bloque les robots)", unverifiable=True)
    elif r.status_code != 200:
        res["detail"] = f"HTTP {r.status_code}"
    else:
        final = str(getattr(r, "url", "") or url)
        op, fp = p0.path.rstrip("/"), urlparse(final).path.rstrip("/")
        redirected = bool(getattr(r, "history", None)) and normalize_url(final) != normalize_url(url)
        if redirected and (fp == "" or _LIST_PATH_RE.search(fp + "/") or re.search(r"expired|notfound|not-found", final.lower())
                           or (len(fp) < len(op) and op.startswith(fp))):
            res.update(code="url_redirect", detail=f"Redirigé vers {final[:120]}")
        else:
            page = fold((r.text or "")[:300000])
            marker = next((mk for mk in EXPIRED_MARKERS if mk in page), "")
            if marker:
                res.update(code="expired", detail=f"Page : « {marker} »")
            else:
                res.update(ok=True, code="", detail="HTTP 200")
    _URL_CACHE[url] = res
    return res


# ---------------------------------------------------------------------------
# Filtre principal
# ---------------------------------------------------------------------------
def _norm_key(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", fold(s)).strip()


def _age_days(posted_at: str, today: datetime.date) -> Optional[int]:
    try:
        return (today - datetime.date.fromisoformat(str(posted_at)[:10])).days
    except (TypeError, ValueError):
        return None


def _reject(job, code: str, detail: str = "") -> Dict:
    return {"url": job.url, "title": job.title, "source": job.source, "reason": code, "detail": detail,
            "company": job.company, "location": job.location, "posted_at": job.posted_at}


def _age_reasons(age: Optional[int]) -> Tuple[str, str]:
    if age is None:
        return "Yayın tarihi bilinmiyor", "Date de publication inconnue"
    if age <= 0:
        return "Bugün yayınlandı", "Publiée aujourd'hui"
    return f"{age} gün önce yayınlandı", f"Publiée il y a {age} jour{'s' if age > 1 else ''}"


def filter_offers(jobs: List, profile: Dict, *, verify_urls: bool = True,
                  today: Optional[datetime.date] = None) -> Tuple[List, List[Dict]]:
    """Applique les règles qualité. Renvoie (gardées, rejetées[{url, title, source, reason, detail…}])."""
    profile = profile or {}
    today = today or datetime.date.today()
    max_age = int(profile.get("max_age_days", 45))
    langs = profile.get("languages", {}) or {}
    allowed = {lang: _profile_level(langs.get(lang, "")) + 1 for lang in ("fr", "en")}
    now_iso = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    kept, rejected = [], []
    seen_urls, seen_keys = set(), set()
    # Titres des offres France Travail déjà reçues via EURES (Adzuna republie les mêmes sous « France Travail »)
    seen_ft_titles = set()

    for job in jobs:
        nurl = normalize_url(job.url)
        if nurl in seen_urls:
            rejected.append(_reject(job, "duplicate", "Même URL"))
            continue

        if (job.kind or "offer") != "offer":  # fiches (leads) : pas des annonces, passent telles quelles
            seen_urls.add(nurl)
            kept.append(job)
            continue

        foreign = foreign_destination(job)
        if foreign:
            rejected.append(_reject(job, "not_in_france", f"Pays étranger dans le titre : « {foreign} »"))
            continue

        loc = check_location(job)
        if loc:
            rejected.append(_reject(job, *loc))
            continue

        age = _age_days(job.posted_at, today) if job.posted_at else None
        over = event_already_over(job, today)
        if over:
            rejected.append(_reject(job, "event_passed", f"Événement déjà terminé : « {over} »"))
            continue

        # Un ATS ne liste que les postes encore ouverts : une annonce permanente ancienne reste valable
        if age is not None and age > max_age and job.source_type != "ats":
            rejected.append(_reject(job, "too_old", f"Publiée il y a {age} jours (> {max_age})"))
            continue

        lang = analyze_languages(job)
        fr_lvl, fr_q = lang["fr"]
        en_lvl, en_q = lang["en"]
        if fr_lvl > allowed["fr"]:
            rejected.append(_reject(job, "french_level", f"Français exigé : « {fr_q} »"))
            continue
        if en_lvl > allowed["en"]:
            rejected.append(_reject(job, "english_level", f"Anglais avancé exigé : « {en_q} »"))
            continue
        community = (job.source_type == "community") or lang["turkish_text"]
        # Sur un agrégateur ou une API, un métier de terrain sans trace du turc est une offre française classique
        field_job = bool(_FIELD_JOB_RE.search(fold(job.title))) and job.source_type not in ("board", "official_api")
        if not (lang["tr_strong"] or lang["tr_weak"] or lang["no_french"] or community or field_job):
            rejected.append(_reject(job, "no_language_fit",
                                    "Ni turc, ni « français non requis », ni métier de terrain : français implicite"))
            continue

        key = (_norm_key(job.title), _norm_key(job.company), _norm_key(job.city or job.location))
        if key in seen_keys:
            rejected.append(_reject(job, "duplicate", "Même titre / entreprise / ville"))
            continue
        if fold(job.company).strip() == "france travail" and key[0] in seen_ft_titles:
            rejected.append(_reject(job, "duplicate", "Offre France Travail déjà reçue via EURES"))
            continue

        url_note = False
        if verify_urls:
            chk = check_url(job.url)
            if not chk["ok"]:
                # Une offre d'API officielle datée et fraîche n'est pas « morte » parce que le site bloque les robots
                if chk["unverifiable"] and job.source_type == "official_api" and age is not None:
                    url_note = True
                else:
                    rejected.append(_reject(job, chk["code"], chk["detail"]))
                    continue
            else:
                job.verified_at = now_iso
        if age is None and not job.verified_at:
            rejected.append(_reject(job, "unknown_date_unverified", "Date inconnue et URL non vérifiée"))
            continue

        seen_urls.add(nurl)
        seen_keys.add(key)
        if job.source.startswith("EURES"):
            seen_ft_titles.add(key[0])

        # --- Raisons honnêtes, score, visa ---
        original = f"{job.title}. {job.snippet}. {job.description}"
        # « Çalışma izni bulunan » = permis déjà exigé, pas une aide au visa
        if job.visa_evidence and _PERMIT_RE.search(fold(job.visa_evidence)):
            job.visa_evidence = ""
        if not job.visa_evidence:
            job.visa_evidence, visa_warning = find_visa_evidence(original)
            if job.visa_evidence and _PERMIT_RE.search(fold(job.visa_evidence)):
                job.visa_evidence = ""
        else:
            visa_warning = ""
        # Le permis déjà exigé est signalé dans les avertissements, pas en double dans les raisons
        if visa_warning and permit_requirement(original):
            visa_warning = ""

        r_tr, r_fr = [], []
        score = 40
        if lang["tr_strong"] in ("tr:requis", "tr:atout"):
            if lang["tr_strong"] == "tr:requis":
                r_tr.append("Türkçe işveren tarafından şart koşuluyor (ilan kriteri)")
                r_fr.append("Turc exigé par l'employeur (critère de l'offre)")
                score += 30
            else:
                r_tr.append("Türkçe işveren tarafından tercih ediliyor (ilan kriteri)")
                r_fr.append("Turc souhaité par l'employeur (critère de l'offre)")
                score += 20
        elif lang["tr_strong"]:
            r_tr.append(f'Türkçe isteniyor (ilanda: "{lang["tr_strong"]}")')
            r_fr.append(f'Turc demandé (annonce : "{lang["tr_strong"]}")')
            score += 30
        elif lang["tr_weak"]:
            r_tr.append(f'İlanda Türkçe/Türk geçiyor (ilanda: "{lang["tr_weak"]}")')
            r_fr.append(f'L\'annonce mentionne le turc (annonce : "{lang["tr_weak"]}")')
            score += 15
        elif community:
            r_tr.append("Türk topluluğu / Türkçe yazılmış ilan")
            r_fr.append("Annonce de la communauté turque / rédigée en turc")
            score += 15
        if lang["no_french"]:
            r_tr.append(f'Fransızca gerekmiyor (ilanda: "{lang["no_french"]}")')
            r_fr.append(f'Français non requis (annonce : "{lang["no_french"]}")')
            score += 10
        elif field_job:
            r_tr.append("Saha işi, ilanda dil şartı belirtilmemiş")
            r_fr.append("Métier de terrain, aucune exigence de langue indiquée")
        else:
            r_tr.append("İlanda Fransızca seviyesi istenmiyor")
            r_fr.append("Aucun niveau de français exigé dans l'annonce")
        a_tr, a_fr = _age_reasons(age)
        r_tr.append(a_tr)
        r_fr.append(a_fr)
        if age is not None:
            score += 15 if age <= 3 else 10 if age <= 14 else 5
        if job.visa_evidence:
            r_tr.append(f'Vize/relokasyon geçiyor (ilanda: "{job.visa_evidence[:80]}")')
            r_fr.append(f'Visa/relocalisation mentionné (annonce : "{job.visa_evidence[:80]}")')
            score += 10
        elif visa_warning:
            r_tr.append(f'Dikkat: Fransa çalışma izni isteniyor olabilir ("{visa_warning[:80]}")')
            r_fr.append(f'Attention : titre de séjour/permis probablement exigé ("{visa_warning[:80]}")')
            score -= 15
        elif url_note:
            r_tr.append("Bağlantı otomatik doğrulanamadı (resmî API ilanı)")
            r_fr.append("Lien non vérifiable automatiquement (offre d'API officielle)")
        # Île-de-France : sa future région (logement assuré chez son conjoint)
        if is_idf(job):
            r_tr.insert(0, "Île-de-France (Paris bölgesi) — yerleşeceğin bölge")
            r_fr.insert(0, "Île-de-France — la région où elle s'installe")
            score += 15

        # Avertissements (l'offre reste visible, mais sans fausse promesse)
        w_tr, w_fr = [], []
        full = f"{job.title} {job.description or job.snippet}"
        permit = permit_requirement(full)
        if permit:
            w_tr.append(f'İşveren Fransa çalışma/oturum izni istiyor ("{permit}") — vize sponsorluğunu işverene sor')
            w_fr.append(f"L'employeur demande un titre de séjour/permis de travail (« {permit} ») — demander s'il peut parrainer le visa")
            score -= 20
        residence = residence_requirement(full)
        if residence and not permit:
            if is_idf(job):
                w_tr.append(f"Paris bölgesinde oturmak isteniyor (« {residence} ») — Paris'e yerleşince uygun")
                w_fr.append(f'Résidence en Île-de-France demandée ("{residence}") — OK une fois installée à Paris')
            else:
                w_tr.append(f'Bölgede oturmak isteniyor ("{residence}")')
                w_fr.append(f'Résidence sur place demandée ("{residence}")')
                score -= 10
        job.warnings_tr = w_tr
        job.warnings_fr = w_fr

        job.match_reasons_tr = r_tr[:4]
        job.match_reasons_fr = r_fr[:4]
        job.relevance_score = max(0, min(90, score))

        # Champs hérités : pas de promesse non étayée
        job.french_required = False
        if not job.visa_evidence:
            job.visa_sponsorship = "İlanda belirtilmemiş"
            job.tags = [t for t in (job.tags or []) if not re.search(r"vize|visa|reloka|✈", t, re.I)]
            job.tags_fr = [t for t in (job.tags_fr or []) if not re.search(r"visa|reloca|✈", t, re.I)]
        else:
            job.visa_sponsorship = "İlanda vize/relokasyon geçiyor"
        if lang["tr_strong"]:
            job.working_language = "Türkçe isteniyor"
        elif community:
            job.working_language = "Türkçe ortam (ilan Türkçe)"
        else:
            job.working_language = "İlanda belirtilmemiş"
        kept.append(job)

    return kept, rejected
