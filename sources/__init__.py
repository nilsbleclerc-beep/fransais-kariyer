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
    # "jooble",  # désactivé le 29/10/2026 : la recherche Jooble ignore les mots-clés (12 247 résultats quelle que
    #            # soit la requête), 0 offre liée au turc sur 345 testées ; code conservé
    "gurbetilan",
    "kariyer_net",
    "company_ats",
]
