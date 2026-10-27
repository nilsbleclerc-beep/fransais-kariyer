"""
Configuration et mots-clés de ciblage pour le scanner d'opportunités France-Turquie.
"""

# Mots-clés principaux
KEYWORDS_LOCATION = [
    "Fransa", "France", "Paris", "Lyon", "Marseille", "Lille",
    "Toulouse", "Nice", "Bordeaux", "Strasbourg", "Nantes"
]

KEYWORDS_RELOCATION_VISA = [
    "relokasyon", "relocation", "vize", "vize desteği", "çalışma izni",
    "yurtdışı", "yurtdışında", "görevlendirilmek üzere", "şubemizde",
    "ofisimizde", "expat", "tayin", "fransa operasyonu", "fransa ofisi"
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

# Requêtes automatisées pour le moteur de recherche (exhaustives et optimisées)
SEARCH_DORKS = [
    'site:kariyer.net Fransa ihracat',
    'site:kariyer.net Fransa lojistik',
    'site:kariyer.net Fransa satış',
    'site:kariyer.net Fransızca yöneticisi',
    'site:tr.linkedin.com/jobs Fransa Türkçe',
    'site:tr.linkedin.com/jobs Fransa iş ilanı',
    'site:fr.linkedin.com/jobs "Turkish" OR "Turc" Paris',
    'site:fr.indeed.com "turc" OR "turcophone" OR "turque"',
    'site:eleman.net Fransa iş ilanları',
    'site:secretcv.com Fransa iş ilanları',
    'site:yenibiris.com Fransa iş ilanları',
    'Fransa Türk iş ilanları Paris Lyon',
    'site:tr.jooble.org Türkçe bilen Fransa',
    'Fransa Türk nakliye lojistik iş ilanı'
]
