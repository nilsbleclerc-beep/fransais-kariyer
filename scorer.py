"""
Module de calcul de pertinence et d'analyse linguistique stricte (Français non obligatoire / A1 toléré).
"""
import re
from typing import List, Tuple
from config import KEYWORDS_LOCATION, KEYWORDS_RELOCATION_VISA, KEYWORDS_LANGUAGE, KEYWORDS_ROLES, NEGATIVE_KEYWORDS
from companies_data import TURKISH_COMPANIES_IN_FRANCE

def analyze_job(title: str, snippet: str, url: str = "") -> Tuple[int, List[str], List[str], str, str, bool, str]:
    """
    Analyse le titre et le snippet d'une offre.
    Retourne:
        - score (0 à 100)
        - tags_tr (list of str en turc)
        - tags_fr (list of str en français)
        - detected_location (str)
        - detected_company (str)
        - french_required (bool)
        - working_language (str)
    """
    text = f"{title} {snippet} {url}".lower()
    score = 45
    tags_tr = []
    tags_fr = []
    detected_location = "Fransa"
    detected_company = "Kurum / Şirket"
    french_required = False
    working_language = "İngilizce veya Türkçe"

    # 1. Détection de la localisation en France
    for loc in KEYWORDS_LOCATION:
        if loc.lower() in text:
            detected_location = loc
            tags_tr.append(f"📍 {loc}")
            tags_fr.append(f"📍 {loc}")
            score += 10
            break

    # 2. Détection d'organisations internationales ou grandes entreprises
    for comp in TURKISH_COMPANIES_IN_FRANCE:
        matched = False
        for kw in comp["keywords"]:
            if kw.lower() in text:
                detected_company = comp["name"]
                tags_tr.append("🏢 Büyük Kurum / Grup")
                tags_fr.append("🏢 Grande Institution / Groupe")
                score += 25
                matched = True
                break
        if matched:
            break

    # 3. Évaluation STRICTE de la langue (Français OBLIGATOIRE vs NON OBLIGATOIRE)
    french_strict_markers = [
        "très bon niveau de français", "français courant exigé", "parfaite maîtrise du français",
        "akıcı fransızca şart", "ileri düzey fransızca zorunlu", "c1", "c2"
    ]
    no_french_markers = [
        "english only", "working language is english", "french is a plus", "french optional",
        "ingilizce yeterli", "fransızca şart değil", "sadece ingilizce", "türkçe yeterli",
        "fransızca bilmek avantajdır", "a1", "a2", "débutant", "no french required"
    ]

    if any(m in text for m in no_french_markers):
        french_required = False
        working_language = "İngilizce / Türkçe (Fransızca Gerekmiyor)"
        tags_tr.append("🇬🇧 Fransızca Şart Değil")
        tags_fr.append("🇬🇧 Français Non Obligatoire")
        score += 20
    elif any(m in text for m in french_strict_markers):
        french_required = True
        working_language = "İleri Düzey Fransızca Zorunlu"
        tags_tr.append("🗣️ İleri Düzey Fransızca")
        tags_fr.append("🗣️ Français B2/C1 Requis")
        score -= 10
    else:
        # Par défaut dans les contextes internationaux ou groupes turcs :
        if any(org in text for org in ["oecd", "ocde", "unesco", "coe", "trendyol", "bbl", "amo", "tech"]):
            french_required = False
            working_language = "İngilizce / Türkçe (A1 Kabul)"
            tags_tr.append("🇬🇧 İngilizce / A1 Fransızca")
            tags_fr.append("🇬🇧 Anglais / Français A1")
            score += 15
        else:
            french_required = False
            working_language = "Türkçe Odaklı"
            tags_tr.append("🇹🇷 Türkçe İletişim")
            tags_fr.append("🇹🇷 Échanges en Turc")

    # 4. Mots-clés Relocation / Visa / Statut International
    for kw in KEYWORDS_RELOCATION_VISA:
        if kw.lower() in text:
            tags_tr.append("✈️ Vize / Relokasyon Destekli")
            tags_fr.append("✈️ Visa / Relocalisation Prise en Charge")
            score += 20
            break

    # 5. Rôles et fonctions recherchées
    role_map = {
        "hat yönetmeni": ("Lojistik / Hat Yönetimi", "Gestionnaire de ligne"),
        "ihracat": ("İhracat", "Export"),
        "satış": ("Satış & Ticari", "Commercial / Vente"),
        "lojistik": ("Lojistik & Depo", "Logistique"),
        "operasyon": ("Operasyon", "Opérations"),
        "mühendis": ("Mühendislik / Yazılım", "Ingénierie / Tech"),
        "büro": ("Büro & Yönetim", "Bureau & Gestion"),
        "tercüman": ("Tercümanlık", "Traduction / Interprétariat"),
        "ekonomist": ("Ekonomi & Politika Analizi", "Économie & Analyse"),
        "juriste": ("Hukuk & İnsan Hakları", "Juridique & Droits")
    }
    for kw, (tr_label, fr_label) in role_map.items():
        if kw.lower() in text:
            tags_tr.append(f"💼 {tr_label}")
            tags_fr.append(f"💼 {fr_label}")
            score += 5
            break

    # 6. Pénalités pour faux positifs
    for kw in NEGATIVE_KEYWORDS:
        if kw.lower() in text:
            score -= 25

    score = max(10, min(100, score))
    tags_tr = list(dict.fromkeys(tags_tr))
    tags_fr = list(dict.fromkeys(tags_fr))

    return score, tags_tr, tags_fr, detected_location, detected_company, french_required, working_language
