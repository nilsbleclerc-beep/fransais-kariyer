"""
Configuration et mots-clés de ciblage pour le scanner d'opportunités France-Turquie.
"""

# Mots-clés principaux
KEYWORDS_LOCATION = [
    "Fransa", "France", "Paris", "Lyon", "Marseille", "Lille",
    "Toulouse", "Nice", "Bordeaux", "Strasbourg", "Nantes"
]

# Mentions EXPLICITES de visa / relocalisation uniquement (mots entiers).
# « yurtdışı », « ofisimizde », « şubemizde », « tayin »… ne prouvent PAS un soutien visa : retirés.
# La détection effective est faite par quality.find_visa_evidence (gère aussi « titre de séjour exigé »).
KEYWORDS_RELOCATION_VISA = [
    "relokasyon", "relocation", "relocalisation", "vize", "vize desteği", "visa", "visa sponsorship",
    "passeport talent", "çalışma izni"
]

KEYWORDS_LANGUAGE = [
    "fransızca", "fransızca bilen", "french", "bilingue", "akıcı fransızca"
]

# Mots-clés de postes fréquemment demandés pour les liaisons bilatérales
KEYWORDS_ROLES = [
    "hat yönetmeni", "ihracat", "satış", "lojistik", "operasyon",
    "business development", "country manager", "account manager",
    "mühendis", "proje yöneticisi", "supply chain", "temsilci"
]

# Mots à pénaliser (faux positifs fréquents sur les sites turcs)
NEGATIVE_KEYWORDS = [
    "fransızca öğretmeni", "öğretmen", "fransızca tercüman aranıyor (türkiye içi)",
    "anaokulu", "kreş"
]

# La recherche DuckDuckGo (SEARCH_DORKS) a été supprimée : résultats périmés et pages de liste
# présentés comme des offres. Les offres viennent désormais de sources/* (API, ATS, sites d'annonces).
