"""
EURES (portail européen sur la mobilité de l'emploi) — NON IMPLÉMENTÉ, volontairement.

Vérification (10/2026) :
- EURES ne publie aucune API de recherche d'offres documentée et ouverte aux tiers. L'« API »
  officielle de la Commission est réservée aux États membres / membres EURES (affichage des offres
  EURES sur leurs portails nationaux), sur convention.
- Le moteur de recherche du portail (europa.eu/eures/portal/jv-se) s'appuie sur un backend interne
  non documenté ; l'interroger directement reviendrait à scraper une API privée, hors CGU explicites.
- Les offres EURES situées en France proviennent de France Travail (membre EURES pour la France) :
  elles sont déjà couvertes par sources/france_travail.py (API officielle).

Si une API publique documentée apparaît, implémenter ici fetch() selon le contrat de sources/__init__.py.
"""
from typing import List

from models import JobOpportunity


def fetch(profile: dict = None) -> List[JobOpportunity]:
    print("[i] EURES : pas d'API publique documentée — offres France couvertes via France Travail")
    return []
