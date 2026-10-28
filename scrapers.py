"""
Fiches statiques (« leads ») : grands groupes turcs en France, canaux spécialisés, institutions
internationales et scale-ups tech. Ce NE SONT PAS des offres d'emploi : kind="lead", source_type="static",
relevance_score=0 (aucun pourcentage de correspondance n'est affiché pour une fiche).

Les offres réelles et datées viennent de sources/* (France Travail, EURES, Adzuna, Jooble, Gurbetİlan,
Kariyer.net, ATS d'entreprises) et passent par quality.filter_offers.
L'ancienne recherche DuckDuckGo (scan_web_dorks) et l'ancien scan_gurbet_ilan ont été supprimés.
"""
import datetime
import re
from typing import List

from models import JobOpportunity
from companies_data import (
    TURKISH_COMPANIES_IN_FRANCE,
    SPECIALIZED_TURKISH_CHANNELS,
    INTERNATIONAL_AND_ACADEMIC_INSTITUTIONS_IN_FRANCE,
    TECH_SCALEUPS_ENGLISH_IN_FRANCE
)

NOT_VERIFIED_VISA = "Doğrulanmadı — şirkete sorulmalı"
ADVANCED_LANG_TR = "🗣️ İleri düzey İngilizce/Fransızca gerekir"
ADVANCED_LANG_FR = "🗣️ Anglais/français avancé requis"
LEAD_TAG_TR = "📇 Şirket fişi (ilan değil)"
LEAD_TAG_FR = "📇 Fiche entreprise (pas une offre)"

# Tags de fiche qui promettent ce qui n'est pas vérifié pour un poste donné
_VISA_TAG_RE = re.compile(r"✈|🛂|vize|visa|reloka|reloca|passeport talent", re.I)
_NO_LANG_TAG_RE = re.compile(r"şart değil|yeterli|non obligatoire|suffisant|non requis|pas de français|0% fr", re.I)


def _now() -> str:
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M")


def _clean_tags(tags, drop_visa=True, drop_no_lang=False) -> List[str]:
    out = []
    for t in tags or []:
        if drop_visa and _VISA_TAG_RE.search(t):
            continue
        if drop_no_lang and _NO_LANG_TAG_RE.search(t):
            continue
        out.append(t)
    return out


class BilateralJobScanner:
    def get_major_companies_leads(self) -> List[JobOpportunity]:
        """Fiches des grands groupes turcs implantés en France (portail carrières / ATS / e-mail RH)."""
        jobs = []
        now_str = _now()
        for comp in TURKISH_COMPANIES_IN_FRANCE:
            is_ccift = comp.get("is_ccift_deik", False)
            tags_tr = [LEAD_TAG_TR, "🏢 Büyük Türk Grubu", f"📍 {comp['hq_france'][:20]}"]
            tags_fr = [LEAD_TAG_FR, "🏢 Groupe Turc Majeur", f"📍 {comp['hq_france'][:20]}"]
            if is_ccift:
                tags_tr.append("🤝 CCIFT & DEİK Üyesi")
                tags_fr.append("🤝 Membre CCIFT & DEİK")
            jobs.append(JobOpportunity(
                title=f"Fransa / Avrupa İşe Alım & Kariyer - {comp['name']}",
                title_fr=f"Postes & Recrutements France / Europe - {comp['name']}",
                company=comp["name"],
                location=comp["hq_france"],
                url=comp.get("ats_direct_url") or comp["linkedin_jobs"] or comp["career_portal"],
                source="Resmi ATS / İK Portalı",
                snippet=f"Fransa Şubesi: {comp['subsidiary_france']}. Aranan Profiller: {comp['recruitment_focus_tr']}",
                snippet_fr=f"Filiale en France: {comp['subsidiary_france']}. Profils recherchés: {comp['recruitment_focus_fr']}",
                category="Büyük Türk Holdingi (Doğrudan Başvuru)",
                category_fr="Multinationale Turque (Candidature Directe)",
                tags=tags_tr,
                tags_fr=tags_fr,
                relevance_score=0,
                contact_info=comp.get("hr_email") or comp["career_portal"],
                discovered_at=now_str,
                french_required=False,
                working_language="Doğrulanmadı (ilana göre değişir)",
                visa_sponsorship=NOT_VERIFIED_VISA,
                is_ccift_deik=is_ccift,
                kind="lead",
                source_type="static",
                country="FR",
            ))
        return jobs

    def get_specialized_channels_leads(self) -> List[JobOpportunity]:
        """Canaux sectoriels bilatéraux (Groupe BBL, ISM/AFTCom, artisanat…)."""
        jobs = []
        now_str = _now()
        for ch in SPECIALIZED_TURKISH_CHANNELS:
            is_ccift = "BBL" in ch["name"] or "Azkan" in ch["name"]
            tags_tr = [LEAD_TAG_TR] + _clean_tags(ch["tags_tr"])
            tags_fr = [LEAD_TAG_FR] + _clean_tags(ch["tags_fr"])
            if is_ccift:
                tags_tr.append("🤝 CCIFT Partner")
                tags_fr.append("🤝 Partenaire CCIFT")
            bilingual = "Çift Dil" in str(ch["tags_tr"])
            jobs.append(JobOpportunity(
                title=ch["title_tr"],
                title_fr=ch["title_fr"],
                company=ch["name"],
                location=ch["location"],
                url=ch["url"],
                source=ch["source"],
                snippet=ch["snippet_tr"],
                snippet_fr=ch["snippet_fr"],
                category=ch["category_tr"],
                category_fr=ch["category_fr"],
                tags=tags_tr,
                tags_fr=tags_fr,
                relevance_score=0,
                contact_info=ch.get("contact_info", ""),
                discovered_at=now_str,
                french_required=bilingual,
                working_language="Türkçe & Fransızca" if bilingual else "Doğrulanmadı",
                visa_sponsorship=NOT_VERIFIED_VISA,
                is_ccift_deik=is_ccift,
                kind="lead",
                source_type="static",
                country="FR",
            ))
        return jobs

    def get_international_institutions_leads(self) -> List[JobOpportunity]:
        """Institutions internationales en France (OCDE, Conseil de l'Europe, UNESCO…).
        Leurs postes exigent un anglais et/ou français courant : on le dit clairement."""
        jobs = []
        now_str = _now()
        for inst in INTERNATIONAL_AND_ACADEMIC_INSTITUTIONS_IN_FRANCE:
            # Le statut juridique (carte spéciale MEAE…) est un fait institutionnel : conservé.
            tags_tr = [LEAD_TAG_TR, ADVANCED_LANG_TR] + _clean_tags(inst["tags_tr"], drop_visa=False, drop_no_lang=True)
            tags_fr = [LEAD_TAG_FR, ADVANCED_LANG_FR] + _clean_tags(inst["tags_fr"], drop_visa=False, drop_no_lang=True)
            jobs.append(JobOpportunity(
                title=f"{inst['name_tr']} - Uluslararası Kadrolar",
                title_fr=f"{inst['name']} - Postes Internationaux",
                company=inst["name_tr"],
                location=inst["city_france"],
                url=inst.get("ats_direct_url") or inst["career_portal"],
                source="Resmi Uluslararası ATS",
                snippet=f"Türkiye Durumu: {inst['turkey_status_tr']} Aranan Alanlar: {inst['recruitment_focus_tr']}",
                snippet_fr=f"Statut Turquie : {inst['turkey_status_fr']} Profils recherchés : {inst['recruitment_focus_fr']}",
                category=inst["category_tr"],
                category_fr=inst["category_fr"],
                tags=tags_tr,
                tags_fr=tags_fr,
                relevance_score=0,
                contact_info=inst.get("career_portal", ""),
                discovered_at=now_str,
                french_required=inst.get("french_required", False),
                working_language="İleri düzey İngilizce ve/veya Fransızca (genelde C1)",
                visa_sponsorship=inst.get("legal_status_visa_tr", NOT_VERIFIED_VISA),
                kind="lead",
                source_type="static",
                country="FR",
            ))
        return jobs

    def get_tech_scaleups_leads(self) -> List[JobOpportunity]:
        """Scale-ups tech à Paris : environnement anglophone, donc anglais professionnel (B2+) attendu."""
        jobs = []
        now_str = _now()
        for tech in TECH_SCALEUPS_ENGLISH_IN_FRANCE:
            tags_tr = [LEAD_TAG_TR, ADVANCED_LANG_TR] + _clean_tags(tech["tags_tr"], drop_no_lang=True)
            tags_fr = [LEAD_TAG_FR, ADVANCED_LANG_FR] + _clean_tags(tech["tags_fr"], drop_no_lang=True)
            jobs.append(JobOpportunity(
                title=f"{tech['name_tr']} - Yazılım, AI & Veri Pozisyonları",
                title_fr=f"{tech['name']} - Postes Tech / AI / Data",
                company=tech["name_tr"],
                location=tech["city_france"],
                url=tech.get("ats_direct_url") or tech["career_portal"],
                source="Resmi Tech ATS",
                snippet=f"Çalışma Dili: {tech['working_language']}. Aranan Alanlar: {tech['recruitment_focus_tr']}",
                snippet_fr=f"Langue de travail : {tech['working_language']}. Profils : {tech['recruitment_focus_fr']}",
                category=tech["category_tr"],
                category_fr=tech["category_fr"],
                tags=tags_tr,
                tags_fr=tags_fr,
                relevance_score=0,
                contact_info=tech.get("career_portal", ""),
                discovered_at=now_str,
                french_required=tech.get("french_required", False),
                working_language="İleri düzey İngilizce (B2/C1)",
                visa_sponsorship=NOT_VERIFIED_VISA,
                kind="lead",
                source_type="static",
                country="FR",
            ))
        return jobs

    def get_all_leads(self) -> List[JobOpportunity]:
        return (self.get_international_institutions_leads() + self.get_major_companies_leads()
                + self.get_specialized_channels_leads() + self.get_tech_scaleups_leads())
