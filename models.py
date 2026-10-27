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
    visa_sponsorship: str = "Vize / Relokasyon Sağlanıyor"
    is_ccift_deik: bool = False
    track: str = "autre"
    domain: str = ""

    def to_dict(self):
        return asdict(self)
