"""
Analyse légère d'un titre/extrait (compatibilité : signature analyze_job inchangée).

Règles « pas de fausses joies » :
- correspondances en MOTS ENTIERS uniquement (plus de « a1 », « c1 », « coe », « amo », « tech » en sous-chaîne) ;
- tag visa UNIQUEMENT si l'annonce mentionne explicitement visa / vize / relocation / sponsor / titre de séjour
  (via quality.find_visa_evidence) — plus jamais sur « yurtdışı », « ofisimizde », « şubemizde » ;
- détection de langue partagée avec quality.py.
Le filtrage et le score des offres réelles sont faits par quality.filter_offers.
"""
import re
from typing import List, Tuple

from companies_data import TURKISH_COMPANIES_IN_FRANCE
from config import KEYWORDS_LOCATION, NEGATIVE_KEYWORDS
from models import JobOpportunity
from quality import analyze_languages, find_visa_evidence, fold


def _has_word(text_folded: str, kw: str) -> bool:
    return re.search(r"(?<!\w)" + re.escape(fold(kw)) + r"(?!\w)", text_folded) is not None


ROLE_MAP = {
    "hat yönetmeni": ("Lojistik / Hat Yönetimi", "Gestionnaire de ligne"),
    "ihracat": ("İhracat", "Export"),
    "satış": ("Satış & Ticari", "Commercial / Vente"),
    "lojistik": ("Lojistik & Depo", "Logistique"),
    "operasyon": ("Operasyon", "Opérations"),
    "mühendis": ("Mühendislik / Yazılım", "Ingénierie / Tech"),
    "büro": ("Büro & Yönetim", "Bureau & Gestion"),
    "tercüman": ("Tercümanlık", "Traduction / Interprétariat"),
    "ekonomist": ("Ekonomi & Politika Analizi", "Économie & Analyse"),
    "juriste": ("Hukuk & İnsan Hakları", "Juridique & Droits"),
}


def analyze_job(title: str, snippet: str, url: str = "") -> Tuple[int, List[str], List[str], str, str, bool, str]:
    """
    Retourne (score 0-90, tags_tr, tags_fr, detected_location, detected_company, french_required, working_language).
    L'URL n'est plus analysée comme du texte (évite « tech » / « amo » trouvés dans un nom de domaine).
    """
    original = f"{title} {snippet}"
    text = fold(original)
    score = 40
    tags_tr, tags_fr = [], []
    detected_location = ""
    detected_company = "Kurum / Şirket"

    for loc in KEYWORDS_LOCATION:
        if _has_word(text, loc):
            detected_location = loc
            tags_tr.append(f"📍 {loc}")
            tags_fr.append(f"📍 {loc}")
            score += 5
            break

    for comp in TURKISH_COMPANIES_IN_FRANCE:
        if any(len(kw) >= 3 and _has_word(text, kw) for kw in comp["keywords"]):
            detected_company = comp["name"]
            tags_tr.append("🏢 Büyük Kurum / Grup")
            tags_fr.append("🏢 Grande Institution / Groupe")
            break

    lang = analyze_languages(JobOpportunity(title=title, company="", location="", url=url, source="", snippet=snippet))
    fr_lvl, en_lvl = lang["fr"][0], lang["en"][0]
    french_required = fr_lvl >= 3
    if french_required:
        working_language = "Fransızca isteniyor"
        tags_tr.append("🗣️ Fransızca isteniyor")
        tags_fr.append("🗣️ Français exigé")
        score -= 20
    elif lang["tr_strong"]:
        working_language = "Türkçe isteniyor"
        tags_tr.append("🇹🇷 Türkçe isteniyor")
        tags_fr.append("🇹🇷 Turc demandé")
        score += 25
    elif lang["no_french"]:
        working_language = "Fransızca gerekmiyor (ilanda)"
        tags_tr.append("✅ Fransızca Şart Değil")
        tags_fr.append("✅ Français Non Obligatoire")
        score += 10
    else:
        working_language = "İlanda belirtilmemiş"
    if en_lvl >= 4:
        tags_tr.append("🇬🇧 İleri düzey İngilizce gerekir")
        tags_fr.append("🇬🇧 Anglais avancé requis")
        score -= 15

    evidence, _ = find_visa_evidence(original)
    if evidence:
        tags_tr.append("✈️ Vize / Relokasyon (ilanda geçiyor)")
        tags_fr.append("✈️ Visa / Relocalisation (mentionné)")
        score += 10

    for kw, (tr_label, fr_label) in ROLE_MAP.items():
        if _has_word(text, kw):
            tags_tr.append(f"💼 {tr_label}")
            tags_fr.append(f"💼 {fr_label}")
            break

    for kw in NEGATIVE_KEYWORDS:
        if _has_word(text, kw):
            score -= 25

    score = max(0, min(90, score))
    return (score, list(dict.fromkeys(tags_tr)), list(dict.fromkeys(tags_fr)), detected_location,
            detected_company, french_required, working_language)
