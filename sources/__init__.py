"""
Collecteurs d'offres d'emploi RÉELLES et datées (une annonce = une URL individuelle).

Chaque module expose `fetch(profile: dict) -> List[JobOpportunity]` :
- ne lève jamais d'exception (journalise et renvoie ce qu'il a pu collecter) ;
- renvoie des offres kind="offer" avec url individuelle, posted_at, country, city, description ;
- ne filtre pas sur le profil (c'est le rôle de quality.py), sauf filtres de requête évidents
  (pays = France, mots-clés turc/turcophone).
"""

# Ordre d'exécution ; un module absent ou en erreur est ignoré par main.py
SOURCE_MODULES = [
    "france_travail",
    "eures",
    "adzuna",
    "jooble",
    "gurbetilan",
    "kariyer_net",
    "company_ats",
]
