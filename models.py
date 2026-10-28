"""
Modèle de données bilingue pour une opportunité d'emploi accessible depuis la Turquie.
Intègre la gestion stricte du visa, le niveau de français et l'accréditation CCIFT / DEİK.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class JobOpportunity:
    title: str
    company: str
    location: str
    url: str
    source: str
    snippet: str
    title_fr: str = ""
    snippet_fr: str = ""
    category: str = "Genel / Diğer"
    category_fr: str = "Général"
    tags: List[str] = field(default_factory=list)
    tags_fr: List[str] = field(default_factory=list)
    relevance_score: int = 50
    contact_info: Optional[str] = ""
    discovered_at: str = ""
    french_required: bool = False
    working_language: str = "İngilizce veya Türkçe"
    visa_sponsorship: str = "İlanda belirtilmemiş"
    is_ccift_deik: bool = False
    track: str = "autre"
    domain: str = ""

    # --- Offres réelles vérifiées (sources/*) ---
    # "offer" = annonce réelle et individuelle ; "lead" = fiche entreprise/institution (pas une annonce)
    kind: str = "offer"
    # "official_api" | "ats" | "board" | "community" | "static"
    source_type: str = ""
    # Date de publication de l'annonce (YYYY-MM-DD), "" si inconnue
    posted_at: str = ""
    # Dernière vérification que l'annonce est en ligne (ISO 8601 UTC), "" si non vérifiée
    verified_at: str = ""
    country: str = ""
    city: str = ""
    # Texte complet de l'annonce, utilisé pour le filtrage (tronqué à l'export)
    description: str = ""
    # Exigences de langue détectées, ex. ["tr:required", "fr:none", "en:basic"]
    language_requirements: List[str] = field(default_factory=list)
    # Raisons concrètes de la correspondance, chacune appuyée sur le texte de l'annonce
    match_reasons_tr: List[str] = field(default_factory=list)
    match_reasons_fr: List[str] = field(default_factory=list)
    # Extrait de l'annonce mentionnant visa / relocalisation / sponsor ; "" si l'annonce n'en parle pas
    visa_evidence: str = ""
    # Points d'attention honnêtes (ex. permis de travail déjà exigé) : l'offre reste visible
    warnings_tr: List[str] = field(default_factory=list)
    warnings_fr: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
