"""
Générateur de rapports (HTML Dashboard bilingue TR/FR, CSV, JSON)
Met en avant de manière prioritaire les membres accrédités de la CCIFT et du DEİK
avec encart spécifique, bouton de filtrage 1-clic et explications bilingues complètes.
Intègre le Design System "Haute Couture Digitale" (Linear, Stripe, Apple HIG) :
- Thème Light / Dark persistant avec switch fluide
- Écussons d'en-tête très visibles sur chaque carte pour les 3 Voies Prioritaires (KAPI 1, 2, 3)
- Ruban doré VIP scintillant (Gold Shimmer Effect)
- Bibliothèque vectorielle SVG complète intégrée (zéro emoji disparate)
- Intégration totale avec le moteur interactif tracker_engine.js
"""
import csv
import json
import html
import os
from typing import List
from models import JobOpportunity

# ==========================================
# BIBLIOTHÈQUE D'ICÔNES VECTORIELLES SVG
# ==========================================
SVG_ICONS = {
    "globe": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>',
    "shield_check": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="m9 12 2 2 4-4"></path></svg>',
    "landmark": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="22" x2="21" y2="22"></line><line x1="6" y1="18" x2="6" y2="11"></line><line x1="10" y1="18" x2="10" y2="11"></line><line x1="14" y1="18" x2="14" y2="11"></line><line x1="18" y1="18" x2="18" y2="11"></line><polygon points="12 2 20 7 4 7"></polygon></svg>',
    "rocket": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"></path><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"></path></svg>',
    "languages": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m5 8 6 6"></path><path d="m4 14 6-6 2-3"></path><path d="M2 5h12"></path><path d="M7 2h1"></path><path d="m22 22-5-10-5 10"></path><path d="M14 18h6"></path></svg>',
    "bookmark": '<svg class="svg-icon icon-bookmark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 21-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>',
    "bookmark_filled": '<svg class="svg-icon icon-bookmark filled" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 21-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>',
    "briefcase": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>',
    "file_text": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><line x1="10" y1="9" x2="8" y2="9"></line></svg>',
    "check_circle": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
    "sun": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2"></path><path d="M12 20v2"></path><path d="m4.93 4.93 1.41 1.41"></path><path d="m17.66 17.66 1.41 1.41"></path><path d="M2 12h2"></path><path d="M20 12h2"></path><path d="m6.34 17.66-1.41 1.41"></path><path d="m19.07 4.93-1.41 1.41"></path></svg>',
    "moon": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path></svg>',
    "external_link": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>',
    "filter": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>',
    "search": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',
    "building": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="20" x="4" y="2" rx="2" ry="2"></rect><path d="M9 22v-4h6v4"></path><path d="M8 6h.01"></path><path d="M16 6h.01"></path><path d="M12 6h.01"></path><path d="M12 10h.01"></path><path d="M12 14h.01"></path><path d="M16 10h.01"></path><path d="M16 14h.01"></path><path d="M8 10h.01"></path><path d="M8 14h.01"></path></svg>',
    "map_pin": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>',
    "plane": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"></path></svg>',
    "sparkles": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"></path></svg>',
    "copy": '<svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"></rect><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"></path></svg>'
}


VISA_TRANSLATIONS = {
    "Birleşmiş Milletler Memur Statüsü: BM Laissez-Passer ve Fransa MEAE Özel Kartı. BM Paris yaşam tazminatı, taşınma ödeneği.":
        "Statut Fonctionnaire ONU : Laissez-Passer ONU & Titre Spécial MEAE. Indemnité d'expatriation Paris & prise en charge intégrale du déménagement.",
    "DSÖ / BM Uluslararası Memur Statüsü: MEAE Özel Oturma Kartı, vergisiz BM maaşı ve taşınma ödeneği.":
        "Statut Fonctionnaire International OMS/ONU : Titre Spécial MEAE, traitement exonéré d'impôt et prime de réinstallation.",
    "French Tech Visa / Passeport Talent sponsorluğu, uçak bileti ve Paris konaklama desteği.":
        "Sponsoring French Tech Visa / Passeport Talent, billet d'avion et aide au logement à Paris.",
    "Hükümetlerarası Kuruluş Memuru Statüsü: Fransa MEAE Özel Oturma İzni.":
        "Statut d'Organisation Intergouvernementale : Titre de séjour spécial délivré par le protocole du MEAE.",
    "Kamu Sözleşmeli Personeli + Passeport Talent (Chercheur/Enseignant) veya VLS-TS Çalışma Vizesi (Üniversite Ev Sahipliği Sözleşmesi ile).":
        "Agent Public Contractuel + Passeport Talent (Chercheur/Enseignant) ou Visa VLS-TS (Convention d'accueil universitaire).",
    "Passeport Talent (Nitelikli Çalışan / Gazeteci Vizesi - CCIJP Basın Kartı). Euronews sözleşmesiyle doğrudan Türkiye'den çok yıllık vize.":
        "Passeport Talent (Salarié Qualifié / Journaliste - Carte CCIJP). Visa pluriannuel direct depuis la Turquie avec contrat Euronews.",
    "Passeport Talent (Nitelikli Çalışan / Uluslararası Hukukçu) veya Mesleki Eğitim / Staj Vizesi.":
        "Passeport Talent (Salarié Qualifié / Juriste International) ou Visa Stage / Formation Professionnelle.",
    "Passeport Talent (Yenilikçi Şirket Vizesi) + Doğrudan Paris'e taşınma ve relokasyon desteği.":
        "Passeport Talent (Entreprise Innovante JEI) + Package complet de relocalisation directe à Paris.",
    "Passeport Talent sponsorluğu + Settlesweet relokasyon paketi (ev bulma ve vize işlemleri %100 karşılanır).":
        "Sponsoring Passeport Talent + Pack relocalisation Settlesweet (logement et démarches visa pris en charge à 100%).",
    "Passeport Talent vize sponsorluğu + Kapsamlı Uluslararası Relokasyon Paketi.":
        "Sponsoring Passeport Talent + Package d'installation et de relocalisation internationale.",
    "Uluslararası Memur Statüsü: Fransa MEAE Özel Diplomatik Oturma Kartı. Klasik vize aranmaz, taşınma ve yerleşme masrafları kurumca %100 karşılanır.":
        "Statut de Fonctionnaire International : Titre de séjour spécial diplomatique MEAE. Pas de visa classique requis, frais de réinstallation pris en charge à 100%.",
    "Uluslararası Memur Statüsü: Fransa MEAE Özel Oturma Kartı.":
        "Statut de Fonctionnaire International : Titre de séjour spécial diplomatique délivré par le MEAE.",
    "Uluslararası Memur Statüsü: Fransa MEAE Özel Oturma İzni. Tam relokasyon ve uluslararası muafiyetler.":
        "Statut de Fonctionnaire International : Titre spécial MEAE. Relocalisation complète et immunités internationales.",
    "Uluslararası Memur Statüsü: Fransa MEAE Özel Statülü Oturma Kartı. Gelir vergisinden muaf maaş, gurbet tazminatı ve aile taşınma paketi.":
        "Statut Fonctionnaire International : Titre spécial MEAE. Salaire net exonéré d'impôt, indemnité d'expatriation et pack famille.",
    "İkili Sektörel Sözleşme / Passeport Talent":
        "Accord Sectoriel Bilatéral / Passeport Talent",
    "İş İlanında Belirtilen Şartlar":
        "Selon les termes de l'offre d'emploi",
    "İşverenle Görüşülmeli":
        "À définir directement avec l'employeur",
    "Şirket İçi Transfer (ICT) / Relokasyon Vizesi":
        "Détachement Intra-Groupe (Salarié Détaché ICT) / Visa Relocalisation"
}

def get_visa_fr(visa_tr: str) -> str:
    if not visa_tr:
        return "Visa / Relocalisation Prise en Charge"
    if visa_tr in VISA_TRANSLATIONS:
        return VISA_TRANSLATIONS[visa_tr]
    for k, v in VISA_TRANSLATIONS.items():
        if k in visa_tr or visa_tr in k:
            return v
    if "ICT" in visa_tr or "Transfer" in visa_tr:
        return "Détachement Intra-Groupe (Salarié Détaché ICT) / Visa Relocalisation"
    if "Passeport Talent" in visa_tr:
        return "Sponsoring Visa Passeport Talent / French Tech"
    if "MEAE" in visa_tr or "Memur" in visa_tr or "Diplomatik" in visa_tr:
        return "Statut International : Titre Spécial Délivré par le MEAE"
    return "Visa / Relocalisation Prise en Charge"


def determine_job_domain(j: JobOpportunity) -> str:
    """Classifie le poste dans un des 7 grands domaines professionnels."""
    if j.domain:
        return j.domain
    txt = f"{j.title} {j.title_fr} {j.category} {j.category_fr} {j.snippet} {' '.join(j.tags)}".lower()
    if any(k in txt for k in ["software", "yazılım", "developer", "engineer", "cloud", "tech", "data", "ai", "intelligence artificielle", "yapay zeka", "it ", "devops"]):
        return "it"
    if any(k in txt for k in ["lojistik", "logistique", "supply chain", "tedarik", "nakliye", "fret", "transport", "depo", "entrepôt"]):
        return "logistics"
    if any(k in txt for k in ["satış", "vente", "sales", "business development", "ihracat", "export", "account manager", "commercial"]):
        return "sales"
    if any(k in txt for k in ["hukuk", "droit", "juridique", "legal", "policy", "avocat", "international relations", "diplomatie"]):
        return "legal_policy"
    if any(k in txt for k in ["çeviri", "traduction", "tercüman", "medya", "média", "journaliste", "gazeteci", "rédacteur", "content"]):
        return "media_trans"
    if any(k in txt for k in ["ik ", "rh ", "ressources humaines", "insan kaynakları", "talent", "recruitment", "admin", "yönetim"]):
        return "hr_admin"
    return "craft_pme"

def determine_job_track(j: JobOpportunity) -> str:
    """Classifie l'offre selon les 3 Voies Prioritaires définies."""
    tags_all = " ".join(j.tags + j.tags_fr).lower()
    cat_all = f"{j.category} {j.category_fr}".lower()
    comp_all = j.company.lower()
    snip_all = f"{j.snippet} {j.snippet_fr}".lower()
    
    # Voie 1 : Institutions Internationales & Européennes (Statut MAE)
    if any(k in tags_all or k in cat_all or k in comp_all for k in [
        "uluslararası kurum", "institution internationale", "oecd", "avrupa konseyi", 
        "conseil de l'europe", "unesco", "aïhm", "cedh", "coe", "diplomatique", "mae"
    ]):
        return "voie_1"
    
    # Voie 2 : Grandes Multinationales Turques en France (ICT / CCIFT / DEİK)
    if j.is_ccift_deik or any(k in tags_all or k in cat_all or k in comp_all for k in [
        "holding", "ccift", "deik", "dei̇k", "beko", "turkish airlines", "thy", "ekol", 
        "barsan", "şişecam", "sisecam", "vestel", "sabancı", "eczacıbaşı", "kordsa", 
        "çimsa", "cimsa", "trendyol", "ict", "salarié détaché"
    ]):
        return "voie_2"
    
    # Voie 3 : Tech Scale-ups & Passeport Talent (%100 Anglais)
    if any(k in tags_all or k in cat_all or k in snip_all or k in comp_all for k in [
        "tech", "scale-up", "scaleup", "yapay zeka", "intelligence artificielle", 
        "passeport talent", "yetenek pasaportu", "mistral", "datadog", "qonto", 
        "deeptech", "fintech", "cloud", "software engineer"
    ]):
        return "voie_3"
        
    return "autre"

def export_to_csv(jobs: List[JobOpportunity], filepath: str = "offres_france_turquie.csv"):
    """Exporte les résultats au format CSV UTF-8 avec BOM pour Excel."""
    with open(filepath, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Score / Uygunluk", "Voie / KAPI", "Pozisyon / Titre (TR)", "Titre (FR)", "Firma / Entreprise",
            "Konum / Lieu", "CCIFT / DEİK Üyesi mi?", "Fransızca Gerekli mi?", "Çalışma Dili", "Vize Durumu",
            "Kategori (TR)", "Catégorie (FR)", "Etiketler / Tags", "Kaynak / Source",
            "Başvuru Linki / URL", "Açıklama / Résumé"
        ])
        for j in jobs:
            is_ccift_str = "EVET (CCIFT/DEİK)" if (j.is_ccift_deik or any("CCIFT" in t for t in j.tags)) else "Diğer"
            track = determine_job_track(j)
            writer.writerow([
                f"{j.relevance_score}%",
                track.upper(),
                j.title,
                j.title_fr or j.title,
                j.company,
                j.location,
                is_ccift_str,
                "Evet (Zorunlu)" if j.french_required else "HAYIR (Şart Değil)",
                j.working_language,
                j.visa_sponsorship,
                j.category,
                j.category_fr,
                ", ".join(j.tags),
                j.source,
                j.url,
                j.snippet
            ])
    print(f"[✓] Fichier CSV exporté : {filepath}")

def export_to_json(jobs: List[JobOpportunity], filepath: str = "offres_france_turquie.json"):
    """Exporte les résultats au format JSON."""
    data = []
    for j in jobs:
        d = j.to_dict()
        d["track"] = determine_job_track(j)
        data.append(d)
    with open(filepath, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[✓] Fichier JSON exporté : {filepath}")

def export_to_html_dashboard(jobs: List[JobOpportunity], filepath: str = "dashboard.html"):
    """
    Génère le dashboard HTML complet "Haute Couture Digitale" :
    - Thème Light / Dark persistant avec switch fluide
    - Écussons d'en-tête très visibles sur chaque carte pour les 3 Voies Prioritaires
    - Ruban doré VIP animé pour CCIFT & DEİK avec balayage scintillant (shimmer)
    - Bibliothèque vectorielle SVG complète intégrée (zéro emoji disparate)
    - Système d'onglets, Kanban et Persistance LocalStorage
    """
    total = len(jobs)
    no_french_count = sum(1 for j in jobs if not j.french_required)
    reloc_count = sum(1 for j in jobs if any(k in str(j.tags + j.tags_fr) for k in ["Vize", "Relokasyon", "Visa", "Relocalisation", "MAE", "Passeport"]))
    ccift_count = sum(1 for j in jobs if (j.is_ccift_deik or any("CCIFT" in t or "DEİK" in t for t in (j.tags + j.tags_fr))))

    track_counts = {"voie_1": 0, "voie_2": 0, "voie_3": 0, "autre": 0}

    cards_html = ""
    for idx, j in enumerate(jobs):
        score_color = "#10b981" if j.relevance_score >= 80 else ("#f59e0b" if j.relevance_score >= 60 else "#6b7280")
        is_ccift = j.is_ccift_deik or any("CCIFT" in t or "DEİK" in t for t in j.tags)
        track = determine_job_track(j)
        domain = determine_job_domain(j)
        track_counts[track] = track_counts.get(track, 0) + 1
        
        tags_tr_str = "|".join(j.tags)
        tags_fr_str = "|".join(j.tags_fr if j.tags_fr else j.tags)
        
        title_tr_safe = html.escape(j.title, quote=True)
        title_fr_safe = html.escape(j.title_fr or j.title, quote=True)
        snippet_tr_safe = html.escape(j.snippet, quote=True)
        snippet_fr_safe = html.escape(j.snippet_fr or j.snippet, quote=True)
        cat_tr_safe = html.escape(j.category, quote=True)
        cat_fr_safe = html.escape(j.category_fr or j.category, quote=True)
        working_lang_safe = html.escape(j.working_language, quote=True)
        visa_safe = html.escape(j.visa_sponsorship, quote=True)
        visa_fr = get_visa_fr(j.visa_sponsorship)
        visa_fr_safe = html.escape(visa_fr, quote=True)
        company_safe = html.escape(j.company, quote=True)
        loc_safe = html.escape(j.location, quote=True)
        source_safe = html.escape(j.source, quote=True)

        lang_badge_class = "tag-no-french" if not j.french_required else "tag-french-req"
        lang_badge_text_tr = "Fransızca Şart Değil (İngilizce/Türkçe)" if not j.french_required else "Fransızca B2+ Gerekli"
        lang_badge_text_fr = "Français Non Requis (Anglais/Turc)" if not j.french_required else "Français B2+ Requis"

        # ÉCUSSON D'EN-TÊTE TRÈS VISIBLE SELON LA VOIE (CLIENT SPEC)
        track_ribbon = ""
        if track == "voie_1":
            track_ribbon = f'''
            <div class="track-ribbon ribbon-voie-1">
                {SVG_ICONS["landmark"]}
                <span class="track-ribbon-text" data-tr="🏛️ KAPI 1 : ULUSLARARASI KURUM (ÖZEL MAE STATÜSÜ)" data-fr="🏛️ VOIE 1 : INSTITUTION INTERNATIONALE (STATUT MAE)">🏛️ KAPI 1 : ULUSLARARASI KURUM (ÖZEL MAE STATÜSÜ)</span>
            </div>
            '''
        elif track == "voie_2":
            track_ribbon = f'''
            <div class="track-ribbon ribbon-voie-2 ccift-badge-shimmer">
                {SVG_ICONS["shield_check"]}
                <span class="track-ribbon-text" data-tr="🏢 KAPI 2 : TÜRK HOLDİNGİ (ŞİRKET İÇİ TRANSFER ICT)" data-fr="🏢 VOIE 2 : GROUPE TURC (DÉTACHEMENT INTRA-GROUPE ICT)">🏢 KAPI 2 : TÜRK HOLDİNGİ (ŞİRKET İÇİ TRANSFER ICT)</span>
            </div>
            '''
        elif track == "voie_3":
            track_ribbon = f'''
            <div class="track-ribbon ribbon-voie-3">
                {SVG_ICONS["rocket"]}
                <span class="track-ribbon-text" data-tr="🚀 KAPI 3 : PASSEPORT TALENT (VİZE SPONSORLUĞU)" data-fr="🚀 VOIE 3 : PASSEPORT TALENT (SPONSORISÉ)">🚀 KAPI 3 : PASSEPORT TALENT (VİZE SPONSORLUĞU)</span>
            </div>
            '''
        else:
            track_ribbon = f'''
            <div class="track-ribbon ribbon-voie-4">
                {SVG_ICONS["building"]}
                <span class="track-ribbon-text" data-tr="🏪 KAPI 4 : TÜRK İŞLETMELERİ (YEREL İSTİHDAM / İZİN)" data-fr="🏪 VOIE 4 : COMMERCES &amp; PME (EMPLOI LOCAL / TITRE)">🏪 KAPI 4 : TÜRK İŞLETMELERİ (YEREL İSTİHDAM / İZİN)</span>
            </div>
            '''

        ccift_ribbon = ""
        if is_ccift and track != "voie_2":
            ccift_ribbon = f'''
            <div class="ccift-card-ribbon ccift-badge-shimmer">
                {SVG_ICONS["shield_check"]}
                <span data-tr="CCIFT &amp; DEİK Üyesi / Membre Officiel" data-fr="CCIFT &amp; DEİK Membre Officiel">CCIFT &amp; DEİK Üyesi / Membre Officiel</span>
            </div>
            '''

        cards_html += f"""
        <div class="job-card {'job-card-ccift' if is_ccift else ''} {'card-track-1' if track == 'voie_1' else ''} {'card-track-3' if track == 'voie_3' else ''}" 
             data-id="{idx}"
             data-track="{track}"
             data-domain="{domain}"
             data-category-tr="{cat_tr_safe}"
             data-category-fr="{cat_fr_safe}"
             data-title-tr="{title_tr_safe}"
             data-title-fr="{title_fr_safe}"
             data-company="{company_safe}"
             data-location="{loc_safe}"
             data-url="{j.url}"
             data-source="{source_safe}"
             data-score="{j.relevance_score}"
             data-snippet-tr="{snippet_tr_safe}"
             data-snippet-fr="{snippet_fr_safe}"
             data-tags-tr="{tags_tr_str}"
             data-tags-fr="{tags_fr_str}"
             data-ccift="{'true' if is_ccift else 'false'}"
             data-no-french="{'true' if not j.french_required else 'false'}"
             data-working-lang="{working_lang_safe}"
             data-visa="{visa_safe}"
             data-visa-tr="{visa_safe}"
             data-visa-fr="{visa_fr_safe}"
             data-search="{j.title.lower()} {j.company.lower()} {j.location.lower()} {j.snippet.lower()} {j.working_language.lower()} {'ccift deik' if is_ccift else ''} {'kapi 1 uluslararasi kurum' if track == 'voie_1' else ''} {'kapi 2 holding ict' if track == 'voie_2' else ''} {'kapi 3 passeport talent tech' if track == 'voie_3' else ''}">
            
            {track_ribbon}
            {ccift_ribbon}

            <div class="card-header">
                <div class="header-badges">
                    <span class="source-badge">{j.source}</span>
                    <span class="category-badge card-cat-badge">{j.category}</span>
                </div>
                <div class="header-right-actions">
                    <div class="score-badge" style="background-color: {score_color}">
                        {SVG_ICONS["sparkles"]} <span class="score-prefix">Uygunluk: </span>%{j.relevance_score}
                    </div>
                    <button class="bookmark-btn" onclick="window.TrackerEngine.toggleBookmark({idx}, event)" aria-label="Favorilere Ekle" title="Favorilere Ekle" aria-pressed="false">
                        <span class="star-icon" aria-hidden="true">☆</span>
                    </button>
                </div>
            </div>
            
            <h3 class="job-title" data-original-text="{title_tr_safe}">{j.title}</h3>
            
            <div class="company-loc">
                <span class="company-name-text" data-original-text="{company_safe}">{SVG_ICONS["building"]} <strong>{j.company}</strong></span><span class="loc-sep" aria-hidden="true">·</span><span class="company-loc-place">{SVG_ICONS["map_pin"]} {j.location}</span>
            </div>
            
            <div class="visa-and-lang-box">
                <div class="val-item">
                    <span class="val-label">{SVG_ICONS["plane"]} <span data-tr="Vize / Relokasyon:" data-fr="Visa / Relocalisation :">Vize / Relokasyon:</span></span>
                    <span class="val-val val-visa" data-visa-tr="{visa_safe}" data-visa-fr="{visa_fr_safe}">{visa_safe}</span>
                </div>
                <div class="val-item">
                    <span class="val-label">{SVG_ICONS["languages"]} <span data-tr="Dil Durumu:" data-fr="Exigence Linguistique :">Dil Durumu:</span></span>
                    <span class="val-val {lang_badge_class}" data-lang-badge="true" data-tr="{lang_badge_text_tr}" data-fr="{lang_badge_text_fr}">{lang_badge_text_tr}</span>
                </div>
            </div>
            
            <p class="snippet" data-original-text="{snippet_tr_safe}">{j.snippet}</p>
            
            <div class="tags-container card-tags">
                <!-- Rempli dynamiquement par JS selon la langue -->
            </div>

            <div class="card-tracker-status" style="display: none;"></div>
            
            <div class="card-footer">
                <button class="action-btn-primary" onclick="if(window.BilateralDrawer) window.BilateralDrawer.open({idx})" title="Vize Yol Haritası, İK Bilgileri &amp; İlan Detayı" data-tooltip-tr="Vize Yol Haritası, İK Bilgileri &amp; İlan Detayı" data-tooltip-fr="Détails de l'Offre, Contacts RH &amp; Feuille de Route Visa">
                    <span data-tr="👁️ İlan &amp; Vize" data-fr="👁️ Offre &amp; Visa">👁️ İlan &amp; Vize</span>
                </button>
                <button class="action-btn-pitch" onclick="if(window.CoverLetterGenerator) window.CoverLetterGenerator.open({idx})" title="Bu İlana Özel Fransızca Ön Yazı ve Pitch Oluştur" data-tooltip-tr="Bu İlana Özel Fransızca Ön Yazı ve Pitch Oluştur" data-tooltip-fr="Générer une Lettre de Motivation &amp; Pitch en Français">
                    <span data-tr="✍️ Ön Yazı" data-fr="✍️ Lettre &amp; Pitch">✍️ Ön Yazı</span>
                </button>
                <button class="action-btn-wa" onclick="if(window.TrackerEngine &amp;&amp; window.TrackerEngine.shareWhatsApp) window.TrackerEngine.shareWhatsApp({idx})" title="Paylaş" data-tooltip-tr="Paylaş" data-tooltip-fr="Partager cette offre">
                    <span data-tr="💬 Paylaş" data-fr="💬 Partager">💬 Paylaş</span>
                </button>
                <button class="tracker-action-btn" onclick="window.TrackerEngine.openTrackerModal({idx})" title="Başvuru Takibine Ekle" data-tooltip-tr="Başvuru Takibine Ekle" data-tooltip-fr="Ajouter au suivi des candidatures">
                    {SVG_ICONS["bookmark"]} <span data-tr="Takip" data-fr="Suivre">Takip</span>
                </button>
                <a href="{j.url}" target="_blank" rel="noopener noreferrer" class="secondary-btn" title="Orijinal İlan Sayfası" data-tooltip-tr="Orijinal İlan Sayfası" data-tooltip-fr="Lien officiel de l'offre">
                    <span data-tr="Link" data-fr="Lien">Link</span> {SVG_ICONS["external_link"]}
                </a>
            </div>
        </div>
        """

    # Lecture des modules JS & CSS additionnels pour injection autonome
    base_dir = os.path.dirname(__file__)
    engine_js_content = ""
    js_filepath = os.path.join(base_dir, "tracker_engine.js")
    if os.path.exists(js_filepath):
        with open(js_filepath, "r", encoding="utf-8") as fjs:
            engine_js_content = fjs.read()

    drawer_css_content = ""
    drawer_css_path = os.path.join(base_dir, "drawer_cover_letter_styles.css")
    if os.path.exists(drawer_css_path):
        with open(drawer_css_path, "r", encoding="utf-8") as fcss:
            drawer_css_content = fcss.read()

    drawer_markup_content = ""
    drawer_html_path = os.path.join(base_dir, "drawer_cover_letter_markup.html")
    if os.path.exists(drawer_html_path):
        with open(drawer_html_path, "r", encoding="utf-8") as fhtml:
            drawer_markup_content = fhtml.read()

    drawer_js_content = ""
    drawer_js_path = os.path.join(base_dir, "drawer_cover_letter_module.js")
    if os.path.exists(drawer_js_path):
        with open(drawer_js_path, "r", encoding="utf-8") as fdjs:
            drawer_js_content = fdjs.read()

    # Charger les ressources PWA (Manifest, Service Worker, Install Banner, Refresh)
    pwa_css_content = ""
    pwa_css_path = os.path.join(base_dir, "pwa_styles.css")
    if os.path.exists(pwa_css_path):
        with open(pwa_css_path, "r", encoding="utf-8") as fpcss:
            pwa_css_content = fpcss.read()

    pwa_markup_content = ""
    pwa_html_path = os.path.join(base_dir, "pwa_markup.html")
    if os.path.exists(pwa_html_path):
        with open(pwa_html_path, "r", encoding="utf-8") as fphtml:
            pwa_markup_content = fphtml.read()

    pwa_js_content = ""
    pwa_js_path = os.path.join(base_dir, "pwa_module.js")
    if os.path.exists(pwa_js_path):
        with open(pwa_js_path, "r", encoding="utf-8") as fpjs:
            pwa_js_content = fpjs.read()

    html_content = f"""<!DOCTYPE html>
<html lang="tr" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <title>Fransa Kariyer &amp; Vize Rehberi | TR ⇄ FR Bilateral Hub</title>
    
    <!-- PWA & Mobile Web App Meta Tags -->
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#f8fafc" media="(prefers-color-scheme: light)">
    <meta name="theme-color" content="#090d16" media="(prefers-color-scheme: dark)">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Fransaİş">
    <link rel="icon" type="image/svg+xml" href="icon.svg">
    <link rel="alternate icon" href="icon-192.png">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script>
        (function() {{
            const savedTheme = localStorage.getItem('bilateral_theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
            document.documentElement.setAttribute('data-theme', savedTheme);
            // Barre d'état Android (theme-color) alignée sur le thème choisi manuellement
            window.syncThemeColorMeta = function(theme) {{
                document.querySelectorAll('meta[name="theme-color"]').forEach(function(m) {{
                    m.setAttribute('content', theme === 'dark' ? '#090d16' : '#f8fafc');
                }});
            }};
            window.syncThemeColorMeta(savedTheme);
        }})();
    </script>
    <style>
        /* ==========================================================================
           DESIGN SYSTEM : HAUTE COUTURE DIGITALE (Linear, Stripe, Apple HIG)
           ========================================================================== */
        
        :root, [data-theme="light"] {{
            /* Surfaces & Canvases */
            --surface-canvas: #f8fafc;
            --surface-card: #ffffff;
            --surface-card-hover: #ffffff;
            --surface-elevated: #ffffff;
            --surface-subtle: #f1f5f9;
            --surface-muted: #e2e8f0;
            --surface-glass: rgba(255, 255, 255, 0.85);

            /* Borders */
            --border-subtle: rgba(226, 232, 240, 0.85);
            --border-default: #cbd5e1;
            --border-strong: #94a3b8;
            --border-focus: #2563eb;

            /* Typography */
            --text-primary: #0f172a;
            --text-secondary: #334155;
            --text-tertiary: #64748b;
            --text-muted: #94a3b8;
            --text-inverse: #ffffff;

            /* Accents */
            --accent-primary: #2563eb;
            --accent-primary-hover: #1d4ed8;
            --accent-primary-subtle: #eff6ff;
            --accent-primary-border: #bfdbfe;

            /* Status Tokens */
            --status-success: #059669;
            --status-success-subtle: #ecfdf5;
            --status-success-border: #a7f3d0;
            --status-success-text: #065f46;

            --status-amber: #d97706;
            --status-amber-subtle: #fffbeb;
            --status-amber-border: #fde68a;
            --status-amber-text: #92400e;

            --status-sky: #0284c7;
            --status-sky-subtle: #f0f9ff;
            --status-sky-border: #bae6fd;
            --status-sky-text: #0369a1;

            --status-purple: #7c3aed;
            --status-purple-subtle: #f5f3ff;
            --status-purple-border: #ddd6fe;
            --status-purple-text: #5b21b6;

            /* VIP Gold & CCIFT */
            --gold-primary: #d97706;
            --gold-hover: #b45309;
            --gold-bg-gradient: linear-gradient(135deg, #fffdf7 0%, #fefcf3 50%, #fef3c7 100%);
            --gold-ribbon-bg: linear-gradient(135deg, #b45309 0%, #d97706 50%, #f59e0b 100%);
            --gold-shimmer-color: rgba(255, 255, 255, 0.6);

            /* Multi-layered Stripe Shadows */
            --shadow-xs: 0 1px 2px rgba(15, 23, 42, 0.04);
            --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03);
            --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.06), 0 2px 4px -2px rgba(15, 23, 42, 0.04);
            --shadow-lg: 0 10px 15px -3px rgba(15, 23, 42, 0.07), 0 4px 6px -4px rgba(15, 23, 42, 0.03);
            --shadow-xl: 0 20px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.03);
            --shadow-card-hover: 0 16px 32px -4px rgba(15, 23, 42, 0.09), 0 6px 12px -2px rgba(15, 23, 42, 0.04);
            --shadow-gold: 0 8px 24px -4px rgba(217, 119, 6, 0.22), 0 2px 8px -1px rgba(245, 158, 11, 0.15);
            --shadow-focus: 0 0 0 3px rgba(37, 99, 235, 0.25);

            /* Legacy Variables compatibility */
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --secondary: #0f172a;
            --secondary-light: #1e293b;
            --success: #059669;
            --amber: #d97706;
            --amber-dark: #b45309;
            --info: #0284c7;
            --purple: #7c3aed;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-dark: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }}

        [data-theme="dark"] {{
            /* Obsidian & Dark Slate */
            --surface-canvas: #090d16;
            --surface-card: #0f172a;
            --surface-card-hover: #162036;
            --surface-elevated: #1e293b;
            --surface-subtle: #141e33;
            --surface-muted: #1e293b;
            --surface-glass: rgba(15, 23, 42, 0.88);

            /* Borders */
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-default: rgba(255, 255, 255, 0.14);
            --border-strong: rgba(255, 255, 255, 0.24);
            --border-focus: #3b82f6;

            /* Typography */
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-tertiary: #94a3b8;
            --text-muted: #64748b;
            --text-inverse: #0f172a;

            /* Accents */
            --accent-primary: #3b82f6;
            --accent-primary-hover: #60a5fa;
            --accent-primary-subtle: rgba(59, 130, 246, 0.16);
            --accent-primary-border: rgba(59, 130, 246, 0.35);

            /* Status Tokens in Dark */
            --status-success: #10b981;
            --status-success-subtle: rgba(16, 185, 129, 0.15);
            --status-success-border: rgba(16, 185, 129, 0.3);
            --status-success-text: #34d399;

            --status-amber: #f59e0b;
            --status-amber-subtle: rgba(245, 158, 11, 0.15);
            --status-amber-border: rgba(245, 158, 11, 0.3);
            --status-amber-text: #fbbf24;

            --status-sky: #38bdf8;
            --status-sky-subtle: rgba(56, 189, 248, 0.15);
            --status-sky-border: rgba(56, 189, 248, 0.3);
            --status-sky-text: #7dd3fc;

            --status-purple: #a78bfa;
            --status-purple-subtle: rgba(167, 139, 250, 0.15);
            --status-purple-border: rgba(167, 139, 250, 0.3);
            --status-purple-text: #c4b5fd;

            /* VIP Gold Dark */
            --gold-primary: #fbbf24;
            --gold-hover: #f59e0b;
            --gold-bg-gradient: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(217, 119, 6, 0.06) 100%);
            --gold-ribbon-bg: linear-gradient(135deg, #d97706 0%, #f59e0b 50%, #fbbf24 100%);
            --gold-shimmer-color: rgba(255, 255, 255, 0.35);

            /* Dark Shadows */
            --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.5);
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.5);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.6);
            --shadow-lg: 0 10px 24px rgba(0, 0, 0, 0.7);
            --shadow-xl: 0 20px 36px rgba(0, 0, 0, 0.8);
            --shadow-card-hover: 0 16px 36px -4px rgba(0, 0, 0, 0.8), 0 0 1px rgba(255, 255, 255, 0.2);
            --shadow-gold: 0 8px 32px -4px rgba(245, 158, 11, 0.25), 0 0 15px rgba(245, 158, 11, 0.15);
            --shadow-focus: 0 0 0 3px rgba(59, 130, 246, 0.35);

            /* Legacy Variables compatibility in Dark */
            --primary: #3b82f6;
            --primary-dark: #60a5fa;
            --secondary: #f8fafc;
            --secondary-light: #cbd5e1;
            --success: #10b981;
            --amber: #f59e0b;
            --amber-dark: #d97706;
            --info: #38bdf8;
            --purple: #a78bfa;
            --bg: #090d16;
            --card-bg: #0f172a;
            --text-dark: #f8fafc;
            --text-muted: #94a3b8;
            --border: rgba(255, 255, 255, 0.12);
        }}

        /* Reset & Base */
        *, *::before, *::after {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        body {{
            background-color: var(--surface-canvas);
            color: var(--text-primary);
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
            padding: max(16px, env(safe-area-inset-top)) max(24px, env(safe-area-inset-right)) calc(60px + env(safe-area-inset-bottom)) max(24px, env(safe-area-inset-left));
            transition: background-color 260ms cubic-bezier(0.16, 1, 0.3, 1), color 260ms cubic-bezier(0.16, 1, 0.3, 1);
        }}
        /* Filet de sécurité anti-débordement horizontal (les vraies causes sont corrigées à la source) */
        html, body {{
            overflow-x: hidden;
            overflow-x: clip; /* clip : ne crée pas de conteneur de défilement (préserve position:sticky) */
        }}
        /* Interactions tactiles : pas de flash bleu Android, pas de délai double-tap */
        button, a, summary, label, select, .quick-step, .track-btn, .filter-pill-btn {{
            -webkit-tap-highlight-color: transparent;
            touch-action: manipulation;
        }}
        /* Longs mots / URLs : coupure plutôt que débordement */
        h1, h2, h3, h4, .job-title, .snippet, .company-loc, .val-val, .template-title,
        .checklist-label, .visa-method-card p, .visa-method-card a, .ccift-text, .bilateral-box p {{
            overflow-wrap: anywhere;
        }}

        /* SVG Icons */
        .svg-icon {{
            width: 16px;
            height: 16px;
            display: inline-block;
            vertical-align: middle;
            stroke-width: 2;
            stroke: currentColor;
            fill: none;
            flex-shrink: 0;
            transition: transform 160ms cubic-bezier(0.16, 1, 0.3, 1), stroke 160ms;
        }}
        .svg-icon.filled {{ fill: currentColor; }}

        /* Top Navigation Bar */
        .top-nav {{
            max-width: 1280px;
            margin: 0 auto 16px auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .brand-badge {{
            font-weight: 800;
            font-size: 1rem;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .brand-icon-box {{
            width: 36px;
            height: 36px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--accent-primary) 0%, #1e1b4b 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);
        }}
        .user-nav-controls {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .lang-switch-box {{
            background: var(--surface-card);
            padding: 3px;
            border-radius: 10px;
            border: 1px solid var(--border-default);
            display: flex;
            gap: 2px;
            box-shadow: var(--shadow-xs);
        }}
        .lang-btn {{
            background: transparent;
            border: none;
            padding: 7px 13px;
            border-radius: 7px;
            font-size: 0.84rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
            color: var(--text-tertiary);
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }}
        .lang-btn.active {{
            background: var(--accent-primary);
            color: white;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3);
        }}
        .theme-toggle-btn {{
            background: var(--surface-card);
            border: 1px solid var(--border-default);
            padding: 8px;
            border-radius: 10px;
            cursor: pointer;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: var(--shadow-xs);
        }}
        .theme-toggle-btn:hover {{
            background: var(--surface-subtle);
            color: var(--text-primary);
            transform: scale(1.05);
        }}

        /* Navigation par Onglets (Segmented Tabs) */
        .main-tabs-nav {{
            max-width: 1280px;
            margin: 0 auto 24px auto;
            background: var(--surface-card);
            border: 1px solid var(--border-default);
            border-radius: 14px;
            padding: 6px;
            display: flex;
            gap: 6px;
            box-shadow: var(--shadow-sm);
        }}
        .tab-nav-btn {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 12px 18px;
            border: none;
            background: transparent;
            border-radius: 10px;
            font-size: 0.94rem;
            font-weight: 700;
            color: var(--text-tertiary);
            cursor: pointer;
            transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .tab-nav-btn:hover {{
            background: var(--surface-subtle);
            color: var(--text-primary);
        }}
        .tab-nav-btn.active {{
            background: var(--surface-subtle);
            color: var(--accent-primary);
            box-shadow: var(--shadow-xs);
        }}
        .tab-badge {{
            background: var(--surface-muted);
            color: var(--text-secondary);
            font-size: 0.76rem;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 12px;
            transition: background 0.2s;
        }}
        .tab-nav-btn.active .tab-badge {{
            background: var(--accent-primary);
            color: white;
        }}

        /* Header Hero */
        .header {{
            max-width: 1280px;
            margin: 0 auto 24px auto;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.2rem;
            color: var(--text-primary);
            margin-bottom: 8px;
            font-weight: 800;
            line-height: 1.25;
            letter-spacing: -0.02em;
        }}
        .header p {{
            color: var(--text-secondary);
            font-size: 1.05rem;
            max-width: 880px;
            margin: 0 auto;
            line-height: 1.55;
        }}

        /* 3 Portes d'Accès Prioritaires (KAPI 1, 2, 3) */
        .priority-tracks-bar {{
            max-width: 1280px;
            margin: 0 auto 20px auto;
            background: var(--surface-card);
            border: 1px solid var(--border-default);
            border-radius: 14px;
            padding: 20px 24px;
            box-shadow: var(--shadow-sm);
        }}
        .tracks-bar-title {{
            font-size: 0.96rem;
            font-weight: 800;
            color: var(--text-primary);
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .tracks-buttons-group {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 12px;
        }}
        .track-btn {{
            background: var(--surface-subtle);
            border: 1.5px solid var(--border-default);
            border-radius: 12px;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
            text-align: left;
            color: var(--text-secondary);
        }}
        .track-btn:hover {{
            background: var(--surface-muted);
            border-color: var(--border-strong);
            transform: translateY(-1px);
        }}
        .track-btn.active {{
            border-color: var(--accent-primary);
            background: var(--accent-primary);
            color: white;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        }}
        .track-btn.track-btn-1.active {{
            border-color: #0284c7;
            background: #0284c7;
            color: white;
        }}
        .track-btn.track-btn-2.active {{
            border-color: var(--gold-primary);
            background: var(--gold-ribbon-bg);
            color: white;
            box-shadow: var(--shadow-gold);
        }}
        .track-btn.track-btn-3.active {{
            border-color: #7c3aed;
            background: #7c3aed;
            color: white;
        }}
        .track-btn-left {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .track-btn .track-name {{
            font-size: 0.88rem;
            font-weight: 700;
        }}
        .track-badge-count {{
            background: rgba(0, 0, 0, 0.08);
            font-size: 0.78rem;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 12px;
            min-width: 26px;
            text-align: center;
            font-family: 'JetBrains Mono', monospace;
        }}
        .track-btn.active .track-badge-count {{
            background: rgba(255, 255, 255, 0.28);
            color: white;
        }}

        /* ÉCUSSONS TRÈS VISIBLES SUR LES CARTES (KAPI 1 / 2 / 3 / 4) */
        .track-ribbon {{
            font-size: 0.76rem;
            font-weight: 800;
            padding: 6px 12px;
            border-radius: 8px;
            margin-bottom: 12px;
            display: inline-flex;
            align-items: center;
            gap: 7px;
            align-self: flex-start;
            text-transform: uppercase;
            letter-spacing: 0.02em;
            position: relative;
            overflow: hidden;
        }}
        .ribbon-voie-1 {{
            background: var(--status-sky-subtle);
            color: var(--status-sky-text);
            border: 1px solid var(--status-sky-border);
        }}
        .ribbon-voie-2 {{
            background: var(--gold-ribbon-bg);
            color: #ffffff;
            border: 1px solid rgba(217, 119, 6, 0.4);
            box-shadow: 0 2px 8px rgba(180, 83, 9, 0.25);
        }}
        .ribbon-voie-3 {{
            background: var(--status-purple-subtle);
            color: var(--status-purple-text);
            border: 1px solid var(--status-purple-border);
        }}
        .ribbon-voie-4 {{
            background: var(--surface-subtle);
            color: var(--text-tertiary);
            border: 1px solid var(--border-subtle);
        }}

        /* BALAYAGE LUMINEUX SHIMMER POUR CCIFT & KAPI 2 */
        .ccift-badge-shimmer::after, .ccift-highlight-box::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 50%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent 0%,
                var(--gold-shimmer-color) 50%,
                transparent 100%
            );
            transform: translateX(-160%) skewX(-20deg);
            animation: goldShimmer 3.2s infinite ease-in-out;
            pointer-events: none;
        }}
        @keyframes goldShimmer {{
            0% {{ transform: translateX(-160%) skewX(-20deg); }}
            35%, 100% {{ transform: translateX(290%) skewX(-20deg); }}
        }}

        .ccift-card-ribbon {{
            background: var(--status-amber-subtle);
            color: var(--gold-primary);
            border: 1px solid var(--status-amber-border);
            font-weight: 800;
            font-size: 0.74rem;
            padding: 5px 10px;
            border-radius: 8px;
            margin-bottom: 12px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            align-self: flex-start;
            position: relative;
            overflow: hidden;
        }}

        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 16px;
            max-width: 1280px;
            margin: 0 auto 24px auto;
        }}
        .stat-card {{
            background: var(--surface-card);
            padding: 20px;
            border-radius: 14px;
            border: 1px solid var(--border-default);
            box-shadow: var(--shadow-sm);
            text-align: center;
            transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 180ms;
        }}
        .stat-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}
        .stat-card .num {{
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--accent-primary);
            font-family: 'JetBrains Mono', monospace;
            line-height: 1.1;
        }}
        .stat-card .num.highlight-green {{ color: var(--status-success); }}
        .stat-card .num.highlight-amber {{ color: var(--gold-primary); }}
        .stat-card .label {{
            color: var(--text-tertiary);
            font-size: 0.88rem;
            margin-top: 6px;
            font-weight: 600;
        }}

        /* Encart CCIFT & DEIK VIP Box */
        .ccift-highlight-box {{
            max-width: 1280px;
            margin: 0 auto 20px auto;
            background: var(--gold-bg-gradient);
            border: 1.5px solid rgba(245, 158, 11, 0.45);
            border-radius: 14px;
            padding: 22px 26px;
            box-shadow: var(--shadow-gold), var(--shadow-sm);
            position: relative;
            overflow: hidden;
        }}
        .ccift-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 10px;
        }}
        .ccift-badge-title {{
            font-weight: 800;
            color: var(--gold-primary);
            font-size: 1.05rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .ccift-quick-btn {{
            background: var(--gold-ribbon-bg);
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 10px;
            font-weight: 700;
            cursor: pointer;
            transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
            font-size: 0.88rem;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 4px 12px rgba(180, 83, 9, 0.25);
        }}
        .ccift-quick-btn:hover {{
            background: var(--gold-hover);
            transform: translateY(-1px);
        }}
        .ccift-text {{
            font-size: 0.94rem;
            color: var(--text-secondary);
            line-height: 1.6;
        }}

        /* Boîte de Conseils Bilatéraux */
        .bilateral-box {{
            max-width: 1280px;
            margin: 0 auto 20px auto;
            background: var(--surface-card);
            border-left: 4px solid var(--status-success);
            border: 1px solid var(--border-default);
            border-left-width: 5px;
            border-left-color: var(--status-success);
            padding: 18px 24px;
            border-radius: 12px;
            box-shadow: var(--shadow-sm);
        }}
        .bilateral-box h4 {{
            color: var(--status-success-text);
            margin-bottom: 6px;
            font-size: 1.02rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .bilateral-box p {{
            font-size: 0.93rem;
            color: var(--text-secondary);
            line-height: 1.55;
        }}

        /* Encarts repliables (<details>) CCIFT & Conseils */
        .info-collapsible > .info-summary {{
            list-style: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            min-height: 48px;
            position: relative;
            z-index: 1;
        }}
        .info-collapsible > .info-summary::-webkit-details-marker {{
            display: none;
        }}
        .info-collapsible > .info-summary::after {{
            content: '';
            flex-shrink: 0;
            width: 9px;
            height: 9px;
            border-right: 2px solid currentColor;
            border-bottom: 2px solid currentColor;
            transform: rotate(45deg);
            margin: 0 6px 4px 0;
            color: var(--text-tertiary);
            transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .info-collapsible[open] > .info-summary::after {{
            transform: rotate(-135deg);
            margin-bottom: -4px;
        }}
        .info-collapsible > .info-summary:focus-visible {{
            outline: 2px solid var(--border-focus);
            outline-offset: 4px;
            border-radius: 6px;
        }}
        .info-collapsible > .info-summary h4 {{
            margin-bottom: 0;
        }}
        .info-collapsible-body {{
            padding-top: 8px;
            position: relative;
            z-index: 1;
        }}
        .info-collapsible-body .ccift-quick-btn {{
            margin-top: 12px;
        }}

        /* Libellés courts des onglets : visibles uniquement dans la barre du bas mobile */
        .tab-label-short {{
            display: none;
        }}

        /* Séparateurs neutres (remplacent les « | » textuels) */
        .facet-separator {{
            width: 1px;
            align-self: stretch;
            min-height: 24px;
            background: var(--border-default);
            margin: 0 4px;
            flex-shrink: 0;
        }}
        .loc-sep {{
            color: var(--text-muted);
            font-weight: 700;
        }}
        .company-loc-place {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}

        /* Contenu des cartes Kanban (markup généré par tracker_engine.js > createKanbanCardElement) */
        .kanban-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 8px;
            margin-bottom: 6px;
        }}
        .kanban-company-box {{
            min-width: 0;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}
        .kanban-company {{
            font-size: 0.82rem;
            font-weight: 800;
            color: var(--text-secondary);
            overflow-wrap: anywhere;
        }}
        .kanban-location {{
            font-size: 0.76rem;
            color: var(--text-tertiary);
        }}
        .kanban-fav-btn {{
            flex-shrink: 0;
            width: 40px;
            height: 40px;
            margin: -6px -6px 0 0;
            border: none;
            border-radius: 50%;
            background: transparent;
            color: var(--text-muted);
            font-size: 1.2rem;
            cursor: pointer;
        }}
        .kanban-fav-btn.active {{
            color: #d97706;
        }}
        .kanban-title {{
            font-size: 0.92rem;
            font-weight: 700;
            line-height: 1.35;
            color: var(--text-primary);
            margin-bottom: 8px;
        }}
        .kanban-badges-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            margin-bottom: 8px;
        }}
        .kanban-badges-row > span,
        .kanban-date-badge {{
            font-size: 0.7rem;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 6px;
            background: var(--surface-subtle);
            color: var(--text-secondary);
            border: 1px solid var(--border-subtle);
        }}
        .kanban-badge-ccift {{
            background: var(--status-amber-subtle) !important;
            color: var(--gold-primary) !important;
            border-color: var(--status-amber-border) !important;
        }}
        .kanban-badge-nofrench {{
            background: var(--status-success-subtle) !important;
            color: var(--status-success-text) !important;
            border-color: var(--status-success-border) !important;
        }}
        .kanban-date-badge {{
            display: inline-block;
            margin: 0 4px 6px 0;
        }}
        .kanban-date-badge.date-interview {{
            background: var(--status-purple-subtle);
            color: var(--status-purple-text);
            border-color: var(--status-purple-border);
        }}
        .kanban-notes-preview {{
            font-size: 0.78rem;
            color: var(--text-tertiary);
            margin-bottom: 8px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .kanban-actions-row,
        .kanban-move-row {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 6px;
            margin-top: 6px;
        }}
        .kanban-btn-action,
        .kanban-btn-link,
        .kanban-move-btn {{
            min-height: 36px;
            padding: 4px 8px;
            border-radius: 8px;
            border: 1px solid var(--border-default);
            background: var(--surface-subtle);
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.78rem;
            font-weight: 700;
            text-decoration: none;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }}
        .kanban-btn-action:hover,
        .kanban-btn-link:hover,
        .kanban-move-btn:hover:not(:disabled) {{
            background: var(--surface-muted);
        }}
        .kanban-move-btn:disabled {{
            opacity: 0.45;
            cursor: not-allowed;
        }}
        .kanban-move-label {{
            color: var(--text-tertiary);
        }}

        /* Sélecteur tactile de statut sur chaque carte Kanban (injecté par tracker_engine.js,
           qui pose un style inline minimal : !important nécessaire pour reprendre la main) */
        .kanban-move-select {{
            display: block !important;
            width: 100% !important;
            min-height: 48px !important;
            margin-top: 8px !important;
            padding: 0 12px !important;
            font-family: inherit !important;
            font-size: 16px !important;
            font-weight: 600;
            color: var(--text-primary) !important;
            background-color: var(--surface-subtle) !important;
            border: 1px solid var(--border-default) !important;
            border-radius: 10px !important;
            cursor: pointer;
            outline: none;
            -webkit-tap-highlight-color: transparent;
            touch-action: manipulation;
            transition: border-color 160ms, box-shadow 160ms;
        }}
        .kanban-move-select:focus-visible {{
            border-color: var(--border-focus) !important;
            box-shadow: var(--shadow-focus);
        }}
        .kanban-move-select option {{
            background-color: var(--surface-card);
            color: var(--text-primary);
        }}

        /* État vide d'une colonne Kanban */
        .kanban-empty-slot {{
            font-size: 0.84rem;
            color: var(--text-tertiary);
            text-align: center;
            padding: 18px 10px;
            border-radius: 10px;
            background: var(--surface-card);
            border: 1px dashed var(--border-default);
        }}

        /* Filtres Multi-Facettes Linear Style */
        .filter-controls-row {{
            display: flex;
            align-items: center;
            gap: 16px;
            margin-top: 14px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }}
        .control-group {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .control-label {{
            font-size: 0.84rem;
            font-weight: 700;
            color: var(--text-secondary);
        }}
        .filter-select {{
            padding: 8px 14px;
            border-radius: 9px;
            border: 1px solid var(--border-default);
            background: var(--surface-card);
            color: var(--text-primary);
            font-size: 0.85rem;
            font-weight: 600;
            outline: none;
            cursor: pointer;
            transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
        }}
        .filter-select:focus {{
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }}
        .filter-panel {{
            max-width: 1280px;
            margin: 0 auto 20px auto;
            background: var(--surface-card);
            border: 1px solid var(--border-default);
            border-radius: 14px;
            padding: 18px 22px;
            box-shadow: var(--shadow-sm);
        }}
        .search-bar-row {{
            display: flex;
            gap: 12px;
            margin-bottom: 14px;
            flex-wrap: wrap;
        }}
        .search-input {{
            flex: 1;
            min-width: min(100%, 280px);
            padding: 12px 18px;
            border-radius: 10px;
            border: 1px solid var(--border-default);
            font-size: 0.96rem;
            outline: none;
            transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
            background: var(--surface-card);
            color: var(--text-primary);
            font-family: inherit;
        }}
        .search-input:focus {{
            border-color: var(--border-focus);
            box-shadow: var(--shadow-focus);
        }}

        .filter-facets-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }}
        .filter-pill-btn {{
            background: var(--surface-subtle);
            border: 1px solid var(--border-default);
            padding: 8px 14px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.86rem;
            font-weight: 700;
            color: var(--text-secondary);
            transition: all 160ms cubic-bezier(0.16, 1, 0.3, 1);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .filter-pill-btn:hover {{
            background: var(--surface-muted);
            border-color: var(--border-strong);
            color: var(--text-primary);
        }}
        .filter-pill-btn.active {{
            background: var(--accent-primary);
            color: white;
            border-color: var(--accent-primary);
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
        }}
        .filter-pill-btn.pill-no-french.active {{
            background: var(--status-success);
            color: white;
            border-color: var(--status-success);
        }}
        .filter-pill-btn.pill-ccift.active {{
            background: var(--gold-ribbon-bg);
            color: white;
            border-color: var(--gold-primary);
            box-shadow: var(--shadow-gold);
        }}
        .filter-pill-btn.pill-fav.active {{
            background: #f59e0b;
            color: white;
            border-color: #f59e0b;
        }}
        .filter-pill-btn.pill-tracked.active {{
            background: var(--status-sky);
            color: white;
            border-color: var(--status-sky);
        }}

        .filter-status-row {{
            margin-top: 14px;
            padding-top: 12px;
            border-top: 1px solid var(--border-subtle);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .results-summary {{
            font-size: 0.88rem;
            color: var(--text-tertiary);
        }}
        .reset-filter-btn {{
            background: transparent;
            border: none;
            color: var(--accent-primary);
            font-size: 0.86rem;
            font-weight: 700;
            cursor: pointer;
            text-decoration: underline;
        }}

        /* Grille des Offres (Linear & Stripe Cards) */
        .cards-grid {{
            max-width: 1280px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(min(100%, 340px), 1fr));
            gap: 22px;
        }}
        .job-card {{
            background: var(--surface-card);
            border-radius: 14px;
            border: 1px solid var(--border-default);
            padding: 22px;
            box-shadow: var(--shadow-sm);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 200ms, border-color 200ms;
            position: relative;
        }}
        .job-card:hover {{
            transform: translateY(-3px);
            box-shadow: var(--shadow-card-hover);
            border-color: var(--border-strong);
        }}
        .job-card.job-card-ccift {{
            border: 1.5px solid rgba(245, 158, 11, 0.45);
            background: var(--gold-bg-gradient);
        }}
        .job-card.job-card-ccift:hover {{
            border-color: var(--gold-primary);
            box-shadow: var(--shadow-gold), var(--shadow-card-hover);
        }}
        .job-card.card-track-1 {{
            border-top: 3.5px solid #0284c7;
        }}
        .job-card.card-track-3 {{
            border-top: 3.5px solid #7c3aed;
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            gap: 8px;
        }}
        .header-badges {{
            display: flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
        }}
        .header-right-actions {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .source-badge {{
            background: var(--accent-primary-subtle);
            color: var(--accent-primary);
            padding: 4px 9px;
            border-radius: 6px;
            font-size: 0.74rem;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .category-badge {{
            background: var(--surface-subtle);
            color: var(--text-tertiary);
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.74rem;
            font-weight: 600;
        }}
        .score-badge {{
            color: white;
            padding: 4px 9px;
            border-radius: 10px;
            font-size: 0.78rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-family: 'JetBrains Mono', monospace;
        }}

        .bookmark-btn {{
            background: transparent;
            border: 1px solid var(--border-default);
            border-radius: 8px;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 1.1rem;
            color: var(--text-muted);
            transition: all 160ms cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .bookmark-btn:hover {{
            border-color: #f59e0b;
            color: #f59e0b;
            transform: scale(1.1);
        }}
        .bookmark-btn.active {{
            background: #fef3c7;
            border-color: #f59e0b;
            color: #d97706;
        }}

        .job-title {{
            font-size: 1.15rem;
            color: var(--text-primary);
            margin-bottom: 8px;
            line-height: 1.35;
            font-weight: 700;
            letter-spacing: -0.01em;
        }}
        .company-loc {{
            font-size: 0.88rem;
            color: var(--text-secondary);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .company-name-text {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}

        .visa-and-lang-box {{
            background: var(--surface-subtle);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 10px 12px;
            margin-bottom: 12px;
            font-size: 0.84rem;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .val-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
        }}
        .val-label {{
            font-weight: 700;
            color: var(--text-tertiary);
            font-size: 0.82rem;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }}
        .val-val {{
            font-weight: 700;
            text-align: right;
        }}
        .val-visa {{
            color: var(--status-sky-text);
            max-width: 60%;
        }}
        .tag-no-french {{
            color: var(--status-success-text);
            background: var(--status-success-subtle);
            padding: 2px 8px;
            border-radius: 5px;
            border: 1px solid var(--status-success-border);
        }}
        .tag-french-req {{
            color: var(--status-amber-text);
            background: var(--status-amber-subtle);
            padding: 2px 8px;
            border-radius: 5px;
            border: 1px solid var(--status-amber-border);
        }}

        .snippet {{
            font-size: 0.88rem;
            color: var(--text-secondary);
            line-height: 1.5;
            margin-bottom: 14px;
            flex-grow: 1;
        }}

        .tags-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 14px;
        }}
        .tag {{
            font-size: 0.74rem;
            padding: 3px 8px;
            border-radius: 6px;
            font-weight: 600;
        }}
        .tag-ccift {{ background: var(--status-amber-subtle); color: var(--gold-primary); border: 1px solid var(--status-amber-border); font-weight: 800; }}
        .tag-visa {{ background: var(--status-sky-subtle); color: var(--status-sky-text); border: 1px solid var(--status-sky-border); }}
        .tag-corp {{ background: var(--status-purple-subtle); color: var(--status-purple-text); border: 1px solid var(--status-purple-border); }}
        .tag-lang {{ background: var(--status-success-subtle); color: var(--status-success-text); border: 1px solid var(--status-success-border); }}
        .tag-default {{ background: var(--surface-subtle); color: var(--text-tertiary); border: 1px solid var(--border-subtle); }}

        .card-tracker-status {{
            display: inline-block;
            font-size: 0.76rem;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 6px;
            margin-bottom: 12px;
            align-self: flex-start;
        }}
        .status-badge-saved {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }}
        .status-badge-applied {{ background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }}
        .status-badge-interview {{ background: #ede9fe; color: #6d28d9; border: 1px solid #ddd6fe; }}
        .status-badge-offer {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}

        .card-footer {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .apply-btn {{
            flex: 1;
            text-align: center;
            background: var(--accent-primary);
            color: white;
            text-decoration: none;
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 0.88rem;
            font-weight: 700;
            transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.2);
        }}
        .apply-btn:hover {{
            background: var(--accent-primary-hover);
            transform: translateY(-1px);
        }}
        .tracker-action-btn {{
            background: var(--surface-subtle);
            border: 1px solid var(--border-default);
            color: var(--text-secondary);
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 0.86rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .tracker-action-btn:hover {{
            background: var(--surface-muted);
            color: var(--text-primary);
        }}
        .tracker-action-btn.in-pipeline {{
            background: var(--status-success-subtle);
            color: var(--status-success-text);
            border-color: var(--status-success-border);
        }}
        /* NOUVEAUX BOUTONS D'ACTION RAPIDE (1-CLIC) & MOBILE */
        .action-btn-primary {{
            flex: 1.2;
            text-align: center;
            background: #0284c7;
            color: white;
            border: none;
            padding: 9px 12px;
            border-radius: 9px;
            font-size: 0.84rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            box-shadow: 0 2px 4px rgba(2, 132, 199, 0.25);
        }}
        .action-btn-primary:hover {{
            background: #0369a1;
            transform: translateY(-1px);
        }}
        .action-btn-pitch {{
            flex: 1.2;
            text-align: center;
            background: #7c3aed;
            color: white;
            border: none;
            padding: 9px 12px;
            border-radius: 9px;
            font-size: 0.84rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            box-shadow: 0 2px 4px rgba(124, 58, 237, 0.25);
        }}
        .action-btn-pitch:hover {{
            background: #6d28d9;
            transform: translateY(-1px);
        }}
        .action-btn-wa {{
            background: #25D366;
            color: white;
            border: none;
            padding: 9px 12px;
            border-radius: 9px;
            font-size: 0.84rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            box-shadow: 0 2px 4px rgba(37, 211, 102, 0.3);
        }}
        .action-btn-wa:hover {{
            background: #20bd5a;
            transform: translateY(-1px);
        }}

        /* BANNIÈRE DE DÉMARRAGE RAPIDE EN 3 ÉTAPES */
        .quick-start-banner {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 14px;
            padding: 16px 20px;
            margin: 0 auto 22px auto;
            max-width: 1280px;
            box-shadow: var(--shadow-md);
            color: white;
        }}
        .quick-start-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }}
        .quick-start-badge {{
            background: #e11d48;
            color: white;
            font-size: 0.74rem;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 6px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        .quick-start-header h3 {{
            margin: 0;
            font-size: 1.05rem;
            font-weight: 800;
            color: #f8fafc;
        }}
        .quick-start-steps {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 12px;
        }}
        .quick-step {{
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 10px;
            padding: 10px 14px;
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            transition: all 180ms ease;
        }}
        .quick-step:hover {{
            background: rgba(255, 255, 255, 0.14);
            border-color: rgba(255, 255, 255, 0.3);
            transform: translateY(-1px);
        }}
        .step-num {{
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: #2563eb;
            color: white;
            font-weight: 800;
            font-size: 0.88rem;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        .step-text strong {{
            display: block;
            font-size: 0.88rem;
            color: #f1f5f9;
        }}
        .step-text span {{
            display: block;
            font-size: 0.74rem;
            color: #94a3b8;
        }}

        .secondary-btn {{
            text-align: center;
            background: var(--surface-subtle);
            color: var(--text-secondary);
            text-decoration: none;
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 0.86rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            border: 1px solid var(--border-default);
            transition: all 180ms;
        }}
        .secondary-btn:hover {{
            background: var(--surface-muted);
            color: var(--text-primary);
        }}

        /* Onglet 2 : Pipeline Kanban */
        .tracker-header-box {{
            max-width: 1280px;
            margin: 0 auto 20px auto;
            text-align: center;
        }}
        .tracker-header-box h2 {{
            font-size: 1.85rem;
            color: var(--text-primary);
            font-weight: 800;
            margin-bottom: 6px;
        }}
        .tracker-header-box p {{
            font-size: 0.98rem;
            color: var(--text-secondary);
        }}
        
        .tracker-stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 14px;
            max-width: 1280px;
            margin: 0 auto 20px auto;
        }}
        .tracker-stat-box {{
            background: var(--surface-card);
            border: 1px solid var(--border-default);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            box-shadow: var(--shadow-sm);
        }}
        .tracker-stat-box .t-num {{
            font-size: 1.9rem;
            font-weight: 800;
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
        }}
        .tracker-stat-box.box-saved .t-num {{ color: #2563eb; }}
        .tracker-stat-box.box-applied .t-num {{ color: #d97706; }}
        .tracker-stat-box.box-interview .t-num {{ color: #7c3aed; }}
        .tracker-stat-box.box-offer .t-num {{ color: #059669; }}
        .tracker-stat-box .t-lbl {{
            font-size: 0.85rem;
            color: var(--text-tertiary);
            font-weight: 600;
            margin-top: 4px;
        }}

        .tracker-toolbar {{
            max-width: 1280px;
            margin: 0 auto 20px auto;
            background: var(--surface-card);
            border: 1px solid var(--border-default);
            border-radius: 14px;
            padding: 14px 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            box-shadow: var(--shadow-sm);
        }}
        .tracker-search-input {{
            padding: 10px 14px;
            border: 1px solid var(--border-default);
            border-radius: 8px;
            font-size: 0.9rem;
            min-width: min(100%, 260px);
            outline: none;
            background: var(--surface-card);
            color: var(--text-primary);
        }}
        .tracker-actions-group {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .btn-action-tracker {{
            padding: 9px 15px;
            border-radius: 8px;
            font-size: 0.88rem;
            font-weight: 700;
            cursor: pointer;
            border: 1px solid var(--border-default);
            transition: all 160ms cubic-bezier(0.16, 1, 0.3, 1);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .btn-export-csv {{ background: #059669; color: white; border-color: #059669; }}
        .btn-export-csv:hover {{ background: #047857; }}
        .btn-export-json {{ background: #0284c7; color: white; border-color: #0284c7; }}
        .btn-export-json:hover {{ background: #0369a1; }}
        .btn-clear-tracker {{ background: var(--surface-subtle); color: #dc2626; border-color: var(--border-default); }}
        .btn-clear-tracker:hover {{ background: #fee2e2; }}

        /* Kanban Board */
        .kanban-board {{
            max-width: 1280px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            align-items: start;
        }}
        @media (max-width: 1024px) {{
            .kanban-board {{ grid-template-columns: repeat(2, 1fr); }}
        }}
        @media (max-width: 640px) {{
            .kanban-board {{ grid-template-columns: 1fr; }}
        }}
        .kanban-column {{
            background: var(--surface-subtle);
            border-radius: 14px;
            border: 2px dashed var(--border-default);
            padding: 14px;
            min-height: 480px;
            display: flex;
            flex-direction: column;
            transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .kanban-column.kanban-col-dragover {{
            border-color: var(--accent-primary);
            background: var(--accent-primary-subtle);
        }}
        .kanban-col-header {{
            margin-bottom: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--border-default);
        }}
        .kanban-col-title-wrap {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .kanban-col-title {{
            font-size: 0.96rem;
            font-weight: 800;
            color: var(--text-primary);
        }}
        .kanban-count-pill {{
            background: var(--surface-card);
            color: var(--text-primary);
            font-size: 0.78rem;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 10px;
            border: 1px solid var(--border-default);
        }}
        .kanban-items-list {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        .kanban-card {{
            background: var(--surface-card);
            border-radius: 10px;
            border: 1px solid var(--border-default);
            padding: 14px;
            box-shadow: var(--shadow-sm);
            cursor: grab;
            transition: transform 150ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 150ms;
        }}
        .kanban-card:hover {{
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }}
        .kanban-card.kanban-card-ccift {{
            border-left: 4px solid var(--gold-primary);
        }}

        /* Onglet 3 : Rehber & Belgeler */
        .guide-container {{
            max-width: 1280px;
            margin: 0 auto;
        }}
        .guide-card-section {{
            background: var(--surface-card);
            border-radius: 14px;
            border: 1px solid var(--border-default);
            padding: 26px 30px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-sm);
        }}
        .guide-section-header {{
            margin-bottom: 18px;
            border-bottom: 1px solid var(--border-default);
            padding-bottom: 10px;
        }}
        .guide-section-header h3 {{
            font-size: 1.35rem;
            color: var(--text-primary);
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .guide-section-header p {{
            color: var(--text-secondary);
            font-size: 0.92rem;
            margin-top: 4px;
        }}
        .guide-grid-2 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr));
            gap: 16px;
        }}
        .visa-method-card {{
            background: var(--surface-subtle);
            border: 1px solid var(--border-default);
            border-radius: 12px;
            padding: 18px;
        }}
        .visa-method-card h4 {{
            font-size: 1.02rem;
            color: var(--text-primary);
            font-weight: 800;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .visa-method-card p {{
            font-size: 0.88rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }}
        .visa-method-card .method-tag {{
            display: inline-block;
            background: var(--status-sky-subtle);
            color: var(--status-sky-text);
            font-size: 0.74rem;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 4px;
            margin-bottom: 8px;
        }}

        .checklist-items-box {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .checklist-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            background: var(--surface-subtle);
            padding: 12px 16px;
            border-radius: 10px;
            border: 1px solid var(--border-default);
            transition: all 160ms;
            cursor: pointer;
        }}
        .checklist-item:hover {{
            background: var(--surface-muted);
        }}
        .checklist-item.checked-item {{
            background: var(--status-success-subtle);
            border-color: var(--status-success-border);
            text-decoration: line-through;
            color: var(--status-success-text);
        }}
        .guide-checkbox {{
            width: 18px;
            height: 18px;
            cursor: pointer;
            accent-color: var(--status-success);
        }}
        .checklist-label {{
            font-size: 0.92rem;
            font-weight: 600;
            flex: 1;
            cursor: pointer;
        }}

        .template-block {{
            background: var(--surface-subtle);
            border: 1px solid var(--border-default);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 16px;
        }}
        .template-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .template-title {{
            font-size: 0.96rem;
            font-weight: 800;
            color: var(--text-primary);
        }}
        .copy-template-btn {{
            background: var(--surface-card);
            border: 1px solid var(--border-default);
            padding: 7px 14px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 160ms;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: var(--text-primary);
        }}
        .copy-template-btn:hover {{
            background: var(--surface-muted);
        }}
        .copy-template-btn.copied-btn {{
            background: var(--status-success);
            color: white;
            border-color: var(--status-success);
        }}
        .template-content {{
            background: var(--surface-card);
            border: 1px solid var(--border-default);
            border-radius: 8px;
            padding: 14px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.84rem;
            line-height: 1.6;
            color: var(--text-secondary);
            white-space: pre-wrap;
        }}

        /* Modal */
        .modal-overlay {{
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(8px);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .modal-box {{
            background: var(--surface-card);
            border-radius: 16px;
            width: 100%;
            max-width: 540px;
            padding: 28px;
            box-shadow: var(--shadow-xl);
            border: 1px solid var(--border-default);
            animation: modalFadeIn 200ms cubic-bezier(0.16, 1, 0.3, 1);
            color: var(--text-primary);
        }}
        @keyframes modalFadeIn {{
            from {{ opacity: 0; transform: scale(0.96); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}
        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
            border-bottom: 1px solid var(--border-default);
            padding-bottom: 12px;
        }}
        .modal-header h3 {{
            font-size: 1.25rem;
            font-weight: 800;
            color: var(--text-primary);
        }}
        .modal-close-btn {{
            background: transparent;
            border: none;
            font-size: 1.4rem;
            color: var(--text-muted);
            cursor: pointer;
        }}
        .modal-job-info {{
            background: var(--surface-subtle);
            border: 1px solid var(--border-default);
            border-radius: 10px;
            padding: 10px 14px;
            margin-bottom: 16px;
        }}
        .modal-job-company {{
            font-size: 0.85rem;
            color: var(--text-tertiary);
            font-weight: 700;
        }}
        .modal-job-title {{
            font-size: 1rem;
            font-weight: 800;
            color: var(--text-primary);
        }}
        .form-group {{ margin-bottom: 14px; }}
        .form-label {{
            display: block;
            font-size: 0.86rem;
            font-weight: 700;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }}
        .form-control {{
            width: 100%;
            padding: 10px 12px;
            border: 1px solid var(--border-default);
            border-radius: 8px;
            font-size: 0.92rem;
            outline: none;
            transition: border 160ms;
            background: var(--surface-card);
            color: var(--text-primary);
            font-family: inherit;
        }}
        .form-control:focus {{
            border-color: var(--border-focus);
            box-shadow: var(--shadow-focus);
        }}
        textarea.form-control {{ min-height: 90px; resize: vertical; }}
        .modal-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
            padding-top: 14px;
            border-top: 1px solid var(--border-default);
        }}
        .modal-btn {{
            padding: 10px 18px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.9rem;
            cursor: pointer;
            border: none;
            transition: all 160ms cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .modal-btn-save {{ background: var(--accent-primary); color: white; }}
        .modal-btn-save:hover {{ background: var(--accent-primary-hover); }}
        .modal-btn-cancel {{ background: var(--surface-subtle); color: var(--text-secondary); border: 1px solid var(--border-default); }}
        .modal-btn-delete {{ background: #fee2e2; color: #dc2626; border: 1px solid #fecaca; }}

        /* Toasts */
        .toast-container {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            gap: 8px;
            pointer-events: none;
        }}
        .toast-item {{
            background: var(--surface-card);
            border-radius: 12px;
            padding: 12px 18px;
            box-shadow: var(--shadow-lg);
            border-left: 4px solid var(--accent-primary);
            border: 1px solid var(--border-default);
            border-left-width: 4px;
            border-left-color: var(--accent-primary);
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-primary);
            transform: translateY(20px);
            opacity: 0;
            transition: all 200ms cubic-bezier(0.16, 1, 0.3, 1);
            pointer-events: auto;
        }}
        .toast-item.toast-show {{ transform: translateY(0); opacity: 1; }}
        .toast-item.toast-hide {{ transform: translateY(-10px); opacity: 0; }}
        .toast-success {{ border-left-color: var(--status-success); }}
        .toast-warning {{ border-left-color: var(--gold-primary); }}
        .toast-star {{ border-left-color: #f59e0b; }}

        /* STYLES DU MODULE BILATÉRAL DRAWER & LETTRE */
        {drawer_css_content}

        /* STYLES PWA & INSTALLATION MOBILE */
        {pwa_css_content}

        /* ==========================================================================
           MOBILE ANDROID (HONOR Magic7 Lite ≈ 384–412px CSS, bords incurvés, gestes)
           Material 3 : barre de navigation basse, cibles 48dp, marges ≥ 16px.
           Placé APRÈS les CSS drawer/PWA injectés pour primer à spécificité égale.
           ========================================================================== */
        :root {{
            --m3-nav-height: 64px;
            --m3-nav-total: calc(var(--m3-nav-height) + env(safe-area-inset-bottom));
            --m3-gutter-left: max(16px, env(safe-area-inset-left));
            --m3-gutter-right: max(16px, env(safe-area-inset-right));
        }}

        @media (max-width: 768px) {{
            body {{
                padding: max(10px, env(safe-area-inset-top)) var(--m3-gutter-right) calc(var(--m3-nav-total) + 24px) var(--m3-gutter-left);
            }}

            /* ---------- Barre supérieure ---------- */
            .top-nav {{
                flex-wrap: nowrap;
                gap: 8px;
                margin-bottom: 12px;
            }}
            .brand-badge {{
                min-width: 0;
                flex: 1 1 auto;
                font-size: 0.9rem;
                gap: 8px;
            }}
            .brand-badge > div:last-child {{
                min-width: 0;
                overflow: hidden;
            }}
            .brand-badge strong {{
                display: block;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            .brand-badge > div:last-child > span {{
                display: none !important;
            }}
            .brand-icon-box {{
                width: 32px;
                height: 32px;
                flex-shrink: 0;
            }}
            .user-nav-controls {{
                gap: 6px;
                flex-shrink: 0;
            }}
            .lang-switch-box {{
                padding: 0;
                gap: 0;
                overflow: hidden;
            }}
            .lang-btn {{
                min-width: 48px;
                min-height: 48px;
                justify-content: center;
                padding: 0 10px;
                border-radius: 0;
            }}
            .lang-btn .svg-icon {{
                display: none;
            }}
            .theme-toggle-btn,
            .refresh-btn,
            .pwa-install-btn {{
                min-width: 48px;
                min-height: 48px;
                justify-content: center;
            }}
            .theme-toggle-btn:hover {{
                transform: none;
            }}

            /* ---------- Navigation basse Material 3 ---------- */
            .main-tabs-nav {{
                position: fixed;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: 1000;
                max-width: none;
                margin: 0;
                height: var(--m3-nav-total);
                padding: 0 env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0;
                background: var(--surface-card);
                border: none;
                border-top: 1px solid var(--border-default);
                border-radius: 0;
                box-shadow: 0 -4px 14px rgba(15, 23, 42, 0.06);
            }}
            .tab-nav-btn {{
                position: relative;
                flex-direction: column;
                justify-content: center;
                gap: 4px;
                height: var(--m3-nav-height);
                min-width: 0;
                padding: 6px 4px;
                border-radius: 0;
                font-size: 0.74rem;
                font-weight: 700;
                letter-spacing: 0.01em;
                color: var(--text-tertiary);
                background: transparent;
            }}
            .tab-nav-btn:hover,
            .tab-nav-btn.active {{
                background: transparent;
                box-shadow: none;
            }}
            .tab-nav-btn > .svg-icon {{
                width: 24px;
                height: 24px;
                padding: 4px 20px;
                box-sizing: content-box;
                border-radius: 16px;
                transition: background-color 200ms cubic-bezier(0.2, 0, 0, 1);
            }}
            .tab-nav-btn.active {{
                color: var(--text-primary);
            }}
            .tab-nav-btn.active > .svg-icon {{
                background: var(--accent-primary-subtle);
                color: var(--accent-primary);
            }}
            .tab-label-long {{
                display: none;
            }}
            .tab-label-short {{
                display: block;
                max-width: 100%;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                line-height: 1.2;
            }}
            .tab-nav-btn .tab-badge {{
                position: absolute;
                top: 4px;
                left: calc(50% + 8px);
                min-width: 18px;
                padding: 1px 5px;
                font-size: 0.64rem;
                line-height: 1.3;
                text-align: center;
                border-radius: 10px;
                border: 2px solid var(--surface-card);
            }}

            /* ---------- Toasts au-dessus de la barre basse ---------- */
            .toast-container {{
                left: var(--m3-gutter-left);
                right: var(--m3-gutter-right);
                bottom: calc(var(--m3-nav-total) + 12px);
                align-items: stretch;
            }}
            .bld-toast {{
                left: var(--m3-gutter-left);
                right: var(--m3-gutter-right);
                bottom: calc(var(--m3-nav-total) + 12px);
            }}

            /* ---------- Démarrage rapide compact ---------- */
            .quick-start-banner {{
                padding: 12px;
                margin-bottom: 14px;
            }}
            .quick-start-header {{
                gap: 8px;
                margin-bottom: 8px;
            }}
            .quick-start-badge {{
                display: none;
            }}
            .quick-start-header h3 {{
                font-size: 0.92rem;
            }}
            .quick-start-steps {{
                grid-template-columns: 1fr;
                gap: 6px;
            }}
            .quick-step {{
                min-height: 48px;
                padding: 6px 10px;
                gap: 10px;
            }}
            .quick-step:hover {{
                transform: none;
            }}
            .step-num {{
                width: 24px;
                height: 24px;
                font-size: 0.78rem;
            }}
            .step-text {{
                min-width: 0;
            }}
            .step-text strong {{
                font-size: 0.84rem;
            }}
            .step-text strong,
            .step-text span {{
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}

            /* ---------- En-tête ---------- */
            .header {{
                margin-bottom: 14px;
                text-align: left;
            }}
            .header h1 {{
                font-size: 1.25rem;
                line-height: 1.3;
                margin-bottom: 6px;
            }}
            .header p {{
                font-size: 0.88rem;
                line-height: 1.45;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }}

            /* ---------- 3 Kapı : pastilles défilantes ---------- */
            .priority-tracks-bar {{
                padding: 0;
                margin-bottom: 12px;
                background: transparent;
                border: none;
                box-shadow: none;
            }}
            .tracks-bar-title {{
                font-size: 0.76rem;
                margin-bottom: 6px;
                color: var(--text-tertiary);
                display: block;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            .tracks-buttons-group,
            .filter-facets-row {{
                display: flex;
                flex-wrap: nowrap;
                gap: 8px;
                overflow-x: auto;
                overscroll-behavior-x: contain;
                scroll-snap-type: x proximity;
                scrollbar-width: none;
                -webkit-overflow-scrolling: touch;
                /* débord jusqu'aux bords de l'écran, contenu aligné sur la gouttière */
                margin-left: calc(-1 * var(--m3-gutter-left));
                margin-right: calc(-1 * var(--m3-gutter-right));
                padding: 2px var(--m3-gutter-right) 4px var(--m3-gutter-left);
                scroll-padding-left: var(--m3-gutter-left);
            }}
            .tracks-buttons-group::-webkit-scrollbar,
            .filter-facets-row::-webkit-scrollbar {{
                display: none;
            }}
            .track-btn {{
                flex: 0 0 auto;
                scroll-snap-align: start;
                min-height: 48px;
                padding: 6px 10px 6px 14px;
                gap: 8px;
                border-radius: 24px;
            }}
            .track-btn:hover {{
                transform: none;
            }}
            .track-btn-left {{
                gap: 6px;
            }}
            .track-btn .track-name {{
                font-size: 0.82rem;
                white-space: nowrap;
            }}

            /* ---------- Compteurs : une rangée compacte ---------- */
            .stats-grid {{
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 6px;
                margin-bottom: 12px;
            }}
            .stat-card {{
                padding: 8px 4px;
                border-radius: 10px;
            }}
            .stat-card:hover {{
                transform: none;
            }}
            .stat-card .num {{
                font-size: 1.15rem;
            }}
            .stat-card .label {{
                font-size: 0.64rem;
                line-height: 1.2;
                margin-top: 3px;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
                overflow-wrap: anywhere;
            }}

            /* ---------- Encarts repliables ---------- */
            .ccift-highlight-box,
            .bilateral-box {{
                padding: 4px 14px;
                margin-bottom: 10px;
                box-shadow: var(--shadow-xs);
            }}
            .ccift-highlight-box[open],
            .bilateral-box[open] {{
                padding-bottom: 14px;
            }}
            .ccift-badge-title {{
                font-size: 0.86rem;
            }}
            .bilateral-box h4 {{
                font-size: 0.86rem;
            }}
            .ccift-text,
            .bilateral-box p {{
                font-size: 0.86rem;
            }}
            .ccift-quick-btn {{
                width: 100%;
                min-height: 48px;
                justify-content: center;
            }}

            /* ---------- Filtres ---------- */
            .filter-panel {{
                padding: 12px;
                margin-bottom: 14px;
            }}
            .search-bar-row {{
                margin-bottom: 10px;
            }}
            .search-input {{
                width: 100%;
                min-width: 0;
                min-height: 48px;
                font-size: 16px; /* évite le zoom automatique au focus */
                padding: 10px 14px;
            }}
            .filter-controls-row {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 8px;
                margin: 0 0 10px 0;
            }}
            .control-group {{
                flex-direction: column;
                align-items: stretch;
                gap: 4px;
                min-width: 0;
            }}
            .control-label {{
                font-size: 0.74rem;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            .filter-select {{
                width: 100%;
                min-width: 0;
                min-height: 48px;
                font-size: 16px;
                padding: 8px 10px;
                text-overflow: ellipsis;
            }}
            .filter-facets-row {{
                margin-top: 0;
            }}
            .filter-pill-btn {{
                flex: 0 0 auto;
                scroll-snap-align: start;
                min-height: 48px;
                padding: 0 14px;
                border-radius: 24px;
                white-space: nowrap;
            }}
            .filter-status-row {{
                margin-top: 8px;
                padding-top: 6px;
                flex-wrap: nowrap;
            }}
            .results-summary {{
                font-size: 0.8rem;
                min-width: 0;
            }}
            .reset-filter-btn {{
                min-height: 48px;
                padding: 0 4px 0 8px;
                flex-shrink: 0;
                font-size: 0.82rem;
            }}

            /* ---------- Cartes d'offres compactes ---------- */
            .cards-grid {{
                gap: 12px;
            }}
            .job-card {{
                padding: 12px 14px;
                border-radius: 14px;
            }}
            .job-card:hover {{
                transform: none;
            }}
            .track-ribbon,
            .ccift-card-ribbon {{
                max-width: 100%;
                font-size: 0.66rem;
                padding: 4px 8px;
                margin-bottom: 6px;
                gap: 5px;
                white-space: nowrap;
            }}
            .track-ribbon-text,
            .ccift-card-ribbon > span {{
                overflow: hidden;
                text-overflow: ellipsis;
                min-width: 0;
            }}
            .card-header {{
                margin-bottom: 6px;
            }}
            .header-badges {{
                flex-wrap: nowrap;
                min-width: 0;
                overflow: hidden;
            }}
            .source-badge,
            .category-badge {{
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                font-size: 0.68rem;
            }}
            .category-badge {{
                min-width: 0;
            }}
            .header-right-actions {{
                gap: 2px;
                flex-shrink: 0;
            }}
            .score-badge .score-prefix {{
                display: none;
            }}
            .bookmark-btn {{
                width: 48px;
                height: 48px;
                margin: -8px -8px -8px 0;
                border: none;
                border-radius: 50%;
                background: transparent;
                font-size: 1.3rem;
            }}
            .bookmark-btn:hover {{
                transform: none;
            }}
            .bookmark-btn.active {{
                background: transparent;
                color: #d97706;
            }}
            .job-title {{
                font-size: 1.02rem;
                margin-bottom: 4px;
                line-height: 1.3;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }}
            /* Entreprise · Lieu sur une seule ligne, chaque partie tronquée si besoin */
            .company-loc {{
                font-size: 0.82rem;
                margin-bottom: 6px;
                gap: 6px;
                flex-wrap: nowrap;
                min-width: 0;
            }}
            .company-name-text,
            .company-loc-place {{
                display: block;
                flex: 0 1 auto;
                min-width: 0;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            .company-name-text {{
                flex-shrink: 0.6;
            }}
            .visa-and-lang-box {{
                padding: 5px 10px;
                margin-bottom: 6px;
                gap: 2px;
                font-size: 0.78rem;
            }}
            .val-item {{
                gap: 8px;
                min-width: 0;
            }}
            .val-label {{
                font-size: 0.74rem;
                flex-shrink: 0;
            }}
            .val-val {{
                min-width: 0;
                font-size: 0.76rem;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            .val-visa {{
                max-width: none;
            }}
            .tag-no-french,
            .tag-french-req {{
                padding: 1px 6px;
            }}
            .snippet {{
                font-size: 0.85rem;
                line-height: 1.4;
                margin-bottom: 6px;
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
                overflow: hidden;
                flex-grow: 0;
            }}
            .tags-container {{
                gap: 4px;
                margin-bottom: 8px;
                max-height: 22px;
                overflow: hidden;
            }}
            .tags-container .tag:nth-child(n+4) {{
                display: none;
            }}
            .tag {{
                font-size: 0.68rem;
                padding: 2px 7px;
                white-space: nowrap;
                max-width: 100%;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            .card-tracker-status {{
                margin-bottom: 8px;
            }}

            /* Pied de carte : 1 action pleine (accent) + actions tonales neutres en grille 2 col. */
            .card-footer {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 6px 8px;
            }}
            .card-footer > * {{
                min-height: 48px;
                min-width: 0;
                margin: 0;
                padding: 0 10px;
                border-radius: 24px;
                font-size: 0.84rem;
                font-weight: 700;
                justify-content: center;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                box-shadow: none;
            }}
            .card-footer > *:hover {{
                transform: none;
            }}
            .card-footer .action-btn-primary {{
                grid-column: 1 / -1;
                background: var(--accent-primary);
                color: #ffffff;
            }}
            .card-footer .action-btn-primary:hover {{
                background: var(--accent-primary-hover);
            }}
            .card-footer .action-btn-pitch,
            .card-footer .action-btn-wa,
            .card-footer .tracker-action-btn,
            .card-footer .secondary-btn {{
                background: var(--surface-subtle);
                color: var(--text-primary);
                border: 1px solid var(--border-default);
            }}
            .card-footer .action-btn-pitch:hover,
            .card-footer .action-btn-wa:hover,
            .card-footer .tracker-action-btn:hover,
            .card-footer .secondary-btn:hover {{
                background: var(--surface-muted);
                color: var(--text-primary);
            }}
            .card-footer .tracker-action-btn.in-pipeline {{
                background: var(--status-success-subtle);
                color: var(--status-success-text);
                border-color: var(--status-success-border);
            }}

            /* ---------- Onglet Suivi / Kanban ---------- */
            .tracker-header-box {{
                text-align: left;
                margin-bottom: 14px;
            }}
            .tracker-header-box h2 {{
                font-size: 1.25rem;
            }}
            .tracker-header-box p {{
                font-size: 0.88rem;
            }}
            .tracker-stats-grid {{
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 6px;
                margin-bottom: 12px;
            }}
            .tracker-stat-box {{
                padding: 8px 4px;
                border-radius: 10px;
            }}
            .tracker-stat-box .t-num {{
                font-size: 1.15rem;
            }}
            .tracker-stat-box .t-lbl {{
                font-size: 0.64rem;
                line-height: 1.2;
                margin-top: 3px;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }}
            .tracker-toolbar {{
                padding: 12px;
                gap: 8px;
                margin-bottom: 14px;
            }}
            .tracker-search-input {{
                width: 100%;
                min-width: 0;
                min-height: 48px;
                font-size: 16px;
            }}
            .tracker-actions-group {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                width: 100%;
            }}
            .btn-action-tracker {{
                min-height: 48px;
                justify-content: center;
                text-align: center;
                font-size: 0.82rem;
                padding: 6px 10px;
            }}
            .btn-clear-tracker {{
                grid-column: 1 / -1;
            }}
            .kanban-board {{
                grid-template-columns: 1fr;
                gap: 10px;
            }}
            .kanban-column {{
                min-height: auto;
                padding: 10px 12px;
                border-width: 1px;
                border-style: solid;
            }}
            .kanban-col-header {{
                margin-bottom: 8px;
                padding-bottom: 8px;
                border-bottom-width: 1px;
            }}
            .kanban-items-list {{
                gap: 8px;
            }}
            .kanban-empty-slot {{
                padding: 8px;
                font-size: 0.78rem;
                background: transparent;
                border: none;
            }}
            .kanban-card {{
                padding: 12px;
                cursor: default;
            }}
            .kanban-card:hover {{
                transform: none;
            }}
            .kanban-fav-btn {{
                width: 48px;
                height: 48px;
                margin: -12px -12px 0 0;
            }}
            .kanban-btn-action,
            .kanban-btn-link,
            .kanban-move-btn {{
                min-height: 48px;
                font-size: 0.82rem;
                border-radius: 24px;
            }}
            .apply-btn {{
                min-height: 48px;
            }}

            /* ---------- Onglet Guide ---------- */
            .guide-card-section {{
                padding: 16px 14px;
                margin-bottom: 14px;
            }}
            .guide-section-header h3 {{
                font-size: 1.05rem;
                align-items: flex-start;
            }}
            .visa-method-card {{
                padding: 14px;
            }}
            .checklist-item {{
                min-height: 48px;
                padding: 10px 12px;
            }}
            .guide-checkbox {{
                width: 22px;
                height: 22px;
                flex-shrink: 0;
            }}
            .checklist-label {{
                font-size: 0.86rem;
            }}
            .template-block {{
                padding: 12px;
            }}
            .copy-template-btn {{
                min-height: 48px;
                width: 100%;
                justify-content: center;
            }}
            .template-content {{
                font-size: 0.78rem;
                padding: 10px;
                max-height: 320px;
                overflow-y: auto;
                overscroll-behavior-y: contain;
            }}

            /* ---------- Modale de suivi ---------- */
            .modal-overlay {{
                padding: max(12px, env(safe-area-inset-top)) var(--m3-gutter-right) max(12px, env(safe-area-inset-bottom)) var(--m3-gutter-left);
            }}
            .modal-box {{
                padding: 18px 16px;
                max-height: 100%;
                overflow-y: auto;
                overscroll-behavior-y: contain;
            }}
            .modal-close-btn {{
                min-width: 48px;
                min-height: 48px;
                margin: -10px -10px -10px 0;
            }}
            .form-control {{
                font-size: 16px;
                min-height: 48px;
            }}
            .modal-btn {{
                min-height: 48px;
            }}
        }}

        @media (max-width: 380px) {{
            .tab-nav-btn > .svg-icon {{
                padding: 4px 14px;
            }}
            .stat-card .label,
            .tracker-stat-box .t-lbl {{
                font-size: 0.6rem;
            }}
        }}
    </style>
</head>
<body>

    <!-- BARRE SUPÉRIEURE (MARQUE, INSTALLATION PWA, REFRESH, LANGUE & THÈME) -->
    <header class="top-nav">
        <div class="brand-badge">
            <div class="brand-icon-box">{SVG_ICONS["globe"]}</div>
            <div>
                <strong>TALENT BILATÉRAL</strong>
                <span style="color: var(--gold-primary); font-weight: 700; font-size: 0.78rem; display: block;">{SVG_ICONS["shield_check"]} CCIFT &amp; DEİK NETWORK</span>
            </div>
        </div>
        <div class="user-nav-controls">
            <!-- BOUTON D'INSTALLATION 1-CLIC MOBILE & DESKTOP PWA -->
            <button id="pwaInstallBtn" class="pwa-install-btn" onclick="window.PWAHandler.promptInstall()" style="display: none;" title="Uygulamayı Telefona Yükle (1-Tık)">
                <span>📱</span>
                <span class="pwa-btn-text" data-tr="Uygulamayı Yükle" data-fr="Installer l'App">Uygulamayı Yükle</span>
            </button>

            <!-- BOUTON D'ACTUALISATION EN DIRECT (REFRESH) -->
            <button id="refreshBtn" class="refresh-btn" onclick="window.PWAHandler.triggerRefresh()" title="İlanları Şimdi Yenile / Actualiser">
                <span class="refresh-spinner-icon" id="refreshBtnIcon">🔄</span>
                <span class="refresh-text" id="refreshBtnText" data-tr="Şimdi Yenile" data-fr="Actualiser">Şimdi Yenile</span>
            </button>

            <div class="lang-switch-box">
                <button id="btnTR" class="lang-btn active" onclick="window.TrackerEngine.setLanguage('tr')">
                    {SVG_ICONS["languages"]} <span>TR</span>
                </button>
                <button id="btnFR" class="lang-btn" onclick="window.TrackerEngine.setLanguage('fr')">
                    <span>FR</span>
                </button>
            </div>
            <button id="themeToggleBtn" class="theme-toggle-btn" onclick="toggleTheme()" aria-label="Toggle Theme" title="Karanlık / Açık Mod">
                {SVG_ICONS["moon"]}
            </button>
        </div>
    </header>

    <!-- BANDEAU MOBILE D'INSTALLATION PWA & MODALES PWA -->
    {pwa_markup_content}

    <!-- ONGLETS PRINCIPAUX -->
    <!-- Desktop : onglets segmentés en haut. Mobile (≤768px) : barre de navigation fixe en bas (Material 3). -->
    <nav class="main-tabs-nav" aria-label="Fransaİş">
        <button class="tab-nav-btn active" id="tabBtnExplore" onclick="window.TrackerEngine.switchTab('explore')">
            {SVG_ICONS["briefcase"]}
            <span class="tab-label-long" id="i18n-tab-explore" data-tr="Keşfet &amp; İlanlar" data-fr="Explorer les Offres">Keşfet &amp; İlanlar</span>
            <span class="tab-label-short" data-tr="Keşfet" data-fr="Explorer">Keşfet</span>
            <span class="tab-badge" id="badge-explore-count">{total}</span>
        </button>
        <button class="tab-nav-btn" id="tabBtnTracker" onclick="window.TrackerEngine.switchTab('tracker')">
            {SVG_ICONS["bookmark"]}
            <span class="tab-label-long" id="i18n-tab-tracker" data-tr="Başvuru Takibi (Kanban)" data-fr="Suivi Candidatures (Kanban)">Başvuru Takibi (Kanban)</span>
            <span class="tab-label-short" data-tr="Başvurularım" data-fr="Candidatures">Başvurularım</span>
            <span class="tab-badge" id="badge-tracker-count">0</span>
        </button>
        <button class="tab-nav-btn" id="tabBtnGuide" onclick="window.TrackerEngine.switchTab('guide')">
            {SVG_ICONS["file_text"]}
            <span class="tab-label-long" id="i18n-tab-guide" data-tr="Rehber, Vize &amp; Belgeler" data-fr="Guide Visa &amp; Outils">Rehber, Vize &amp; Belgeler</span>
            <span class="tab-label-short" data-tr="Rehber" data-fr="Guide">Rehber</span>
        </button>
    </nav>

    <!-- ==================================================================== -->
    <!-- ONGLET 1 : KEŞFET / EXPLORER (GRILLE ET FILTRES MULTI-FACETTES)        -->
    <!-- ==================================================================== -->
    <main id="tab-content-explore" class="tab-pane">
        
        <!-- GUIDE DE DÉMARRAGE RAPIDE 3 ÉTAPES (MOBILE & DESKTOP) -->
        <div class="quick-start-banner">
            <div class="quick-start-header">
                <span class="quick-start-badge" data-tr="🚀 HIZLI BAŞLANGIÇ" data-fr="🚀 DÉMARRAGE RAPIDE">🚀 HIZLI BAŞLANGIÇ</span>
                <h3 id="i18n-qs-title" data-tr="Fransa'ya Başvuru İçin 3 Kolay Adım :" data-fr="3 étapes simples pour postuler en France :">Fransa'ya Başvuru İçin 3 Kolay Adım :</h3>
            </div>
            <div class="quick-start-steps">
                <div class="quick-step" onclick="window.TrackerEngine.Filter.toggleNoFrench();" title="Sadece İngilizce veya Türkçe yeterli olan ilanlar" data-tooltip-tr="Sadece İngilizce veya Türkçe yeterli olan ilanlar" data-tooltip-fr="Offres où l'anglais ou le turc est suffisant">
                    <div class="step-num">1</div>
                    <div class="step-text">
                        <strong data-tr="✅ Fransızca Şart Değil" data-fr="✅ Français Non Requis">✅ Fransızca Şart Değil</strong>
                        <span data-tr="İngilizce veya Türkçe yeterli ilanları filtrele" data-fr="Filtrer les offres en anglais ou turc">İngilizce veya Türkçe yeterli ilanları filtrele</span>
                    </div>
                </div>
                <div class="quick-step" onclick="window.TrackerEngine.Filter.setTrack('voie_2')" title="Şirket içi transfer ile en hızlı vize" data-tooltip-tr="Şirket içi transfer ile en hızlı vize" data-tooltip-fr="Détachement intra-groupe ICT ultra-rapide">
                    <div class="step-num">2</div>
                    <div class="step-text">
                        <strong data-tr="🏢 Türk Holdingi veya Kurum Seç" data-fr="🏢 Groupes Turcs ou Institutions">🏢 Türk Holdingi veya Kurum Seç</strong>
                        <span data-tr="Beko, THY veya Uluslararası Kurumlar" data-fr="Beko, THY ou Organisations Internationales">Beko, THY veya Uluslararası Kurumlar</span>
                    </div>
                </div>
                <div class="quick-step" onclick="window.TrackerEngine.switchTab('guide')" title="Hazır Fransızca dilekçe ve vize rehberi" data-tooltip-tr="Hazır Fransızca dilekçe ve vize rehberi" data-tooltip-fr="Générateur de lettre et guide visa">
                    <div class="step-num">3</div>
                    <div class="step-text">
                        <strong data-tr="✍️ 1-Tıkla Ön Yazını Üret" data-fr="✍️ Générer la Lettre en 1 Clic">✍️ 1-Tıkla Ön Yazını Üret</strong>
                        <span data-tr="Fransızca resmi başvuru mektubun anında hazır" data-fr="Votre lettre en français prête instantanément">Fransızca resmi başvuru mektubun anında hazır</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="header">
            <h1 id="i18n-title">Türkiye'den Fransa'ya Vize & Relokasyon Destekli İş Fırsatları</h1>
            <p id="i18n-subtitle">Türkiye'de ikamet eden adayların başvurusuna açık, vize/relokasyon sağlayan veya uluslararası statü veren resmi kurumlar ve Türk şirketleri.</p>
        </div>

        <!-- 3 PORTES D'ACCÈS PRIORITAIRES (VOIE 1 / VOIE 2 / VOIE 3) -->
        <div class="priority-tracks-bar">
            <div class="tracks-bar-title" id="i18n-tracks-title" data-tr="🚪 3 ÖNCELİKLİ YASAL İSTİHDAM KAPISI (VİZE / RELOKASYON) :" data-fr="🚪 LES 3 PORTES D'ACCÈS PRIORITAIRES (VISA / RELOCALISATION) :">{SVG_ICONS["filter"]} 3 ÖNCELİKLİ YASAL İSTİHDAM KAPISI (VİZE / RELOKASYON) :</div>
            <div class="tracks-buttons-group">
                <button class="track-btn active" data-track="all" onclick="window.TrackerEngine.Filter.setTrack('all', this)" id="btn-track-all">
                    <div class="track-btn-left">
                        <span class="track-icon">{SVG_ICONS["globe"]}</span>
                        <span class="track-name" id="i18n-track-all" data-tr="Tüm Kapılar / Tümü" data-fr="Toutes les Voies / Tout">Tüm Kapılar / Tümü</span>
                    </div>
                    <span class="track-badge-count" id="count-track-all">{total}</span>
                </button>
                <button class="track-btn track-btn-1" data-track="voie_1" onclick="window.TrackerEngine.Filter.setTrack('voie_1', this)" id="btn-track-1">
                    <div class="track-btn-left">
                        <span class="track-icon">{SVG_ICONS["landmark"]}</span>
                        <span class="track-name" id="i18n-track-1" data-tr="KAPI 1: Uluslararası Kurumlar" data-fr="VOIE 1 : Institutions Internationales">KAPI 1: Uluslararası Kurumlar</span>
                    </div>
                    <span class="track-badge-count" id="count-track-1">{track_counts['voie_1']}</span>
                </button>
                <button class="track-btn track-btn-2" data-track="voie_2" onclick="window.TrackerEngine.Filter.setTrack('voie_2', this)" id="btn-track-2">
                    <div class="track-btn-left">
                        <span class="track-icon">{SVG_ICONS["shield_check"]}</span>
                        <span class="track-name" id="i18n-track-2" data-tr="KAPI 2: Türk Holdingleri (ICT)" data-fr="VOIE 2 : Multinationales Turques (ICT)">KAPI 2: Türk Holdingleri (ICT)</span>
                    </div>
                    <span class="track-badge-count" id="count-track-2">{track_counts['voie_2']}</span>
                </button>
                <button class="track-btn track-btn-3" data-track="voie_3" onclick="window.TrackerEngine.Filter.setTrack('voie_3', this)" id="btn-track-3">
                    <div class="track-btn-left">
                        <span class="track-icon">{SVG_ICONS["rocket"]}</span>
                        <span class="track-name" id="i18n-track-3" data-tr="KAPI 3: Yetenek Pasaportu (Tech)" data-fr="VOIE 3 : Passeport Talent (Tech)">KAPI 3: Yetenek Pasaportu (Tech)</span>
                    </div>
                    <span class="track-badge-count" id="count-track-3">{track_counts['voie_3']}</span>
                </button>
            </div>
        </div>

        <!-- 4 COMPTEURS RÉACTIFS DU HAUT -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="num" id="stat-total">{total}</div>
                <div class="label" id="i18n-stat-total">Toplam Fırsat</div>
            </div>
            <div class="stat-card">
                <div class="num highlight-amber" id="stat-ccift">{ccift_count}</div>
                <div class="label" id="i18n-stat-ccift">CCIFT & DEİK Akredite Üye</div>
            </div>
            <div class="stat-card">
                <div class="num highlight-green" id="stat-no-french">{no_french_count}</div>
                <div class="label" id="i18n-stat-no-french">Fransızca Şart Değil</div>
            </div>
            <div class="stat-card">
                <div class="num" id="stat-reloc">{reloc_count}</div>
                <div class="label" id="i18n-stat-reloc">Vize / Relokasyon Sağlanan</div>
            </div>
        </div>

        <!-- ENCART CCIFT & DEIK AVEC GOLD SHIMMER -->
        <!-- Repliable (<details>) : fermé par défaut sur mobile, ouvert sur desktop via le script de thème -->
        <details class="ccift-highlight-box info-collapsible">
            <summary class="info-summary">
                <span class="ccift-badge-title" id="i18n-ccift-box-title">{SVG_ICONS["shield_check"]} CCIFT & DEİK RESMİ İKİLİ TİCARET ÜYELERİ (EN YÜKSEK VİZE ONAYI)</span>
            </summary>
            <div class="info-collapsible-body">
                <p class="ccift-text" id="i18n-ccift-box-text">
                    Aşağıda altın rozetle işaretlenen şirketler, <strong>Fransız-Türk Ticaret Odası (CCIFT)</strong> ve <strong>DEİK Türkiye-Fransa İş Konseyi</strong>'nin resmi üye holdingleridir (<em>Beko France, Turkish Airlines, Ekol, Barsan, Şişecam, Vestel, Sabancı, Eczacıbaşı vb.</em>). Bu kurumlar, Fransa ile resmi ikili protokol ve anlaşmalara sahip olup, Türkiye'den personel transferinde <strong>Şirket İçi Transfer (ICT)</strong> ve <strong>Yetenek Pasaportu (Passeport Talent)</strong> vizelerinde en yüksek onay oranına ve en hızlı prosedürlere sahiptir.
                </p>
                <button class="ccift-quick-btn" onclick="window.TrackerEngine.Filter.toggleCcift(); document.getElementById('filter-btn-ccift').classList.toggle('active');" id="i18n-ccift-quick-btn">
                    {SVG_ICONS["shield_check"]} Bu Üyelerin İlanlarını Filtrele (1-Tık)
                </button>
            </div>
        </details>

        <!-- ENCART CONSEILS & LANGUES -->
        <details class="bilateral-box info-collapsible">
            <summary class="info-summary">
                <h4 id="i18n-advice-title">{SVG_ICONS["check_circle"]} Türkiye'deki Adaylar İçin Vize ve Dil Rehberi:</h4>
            </summary>
            <div class="info-collapsible-body">
                <p id="i18n-advice-text">
                    <strong>Fransızca bilmiyorsanız endişelenmeyin :</strong> Yeşil etiketli ilanlarda çalışma dili <strong>İngilizce veya Türkçe</strong>dir (Fransızca şart değildir veya temel A1 yeterlidir). Türkiye'den vizesiz başvuru yaparken en güçlü kapılar : <strong>1)</strong> Yukarıdaki <strong>CCIFT & DEİK üyesi holdingler</strong> (Şirket İçi Transfer ICT vizesi). <strong>2)</strong> Türkiye'nin üyesi olduğu uluslararası kuruluşlar (<em>Avrupa Konseyi, OECD, UNESCO</em> - özel diplomatik/uluslararası memur statüsü verilir). <strong>3)</strong> Paris merkezli scale-up'lar (%100 İngilizce Tech kadroları).
                </p>
            </div>
        </details>

        <!-- BARRE DE RECHERCHE ET FILTRES MULTI-FACETTES -->
        <div class="filter-panel">
            <div class="search-bar-row">
                <input type="text" id="searchInput" class="search-input" placeholder="Pozisyon, şehir (Paris, Lyon, Strazburg...), kurum (OECD, Beko, THY, Ekol...) ara..." data-placeholder-tr="🔍 Pozisyon, şehir (Paris, Lyon, Strazburg...), kurum (OECD, Beko, THY, Ekol...) ara..." data-placeholder-fr="🔍 Rechercher poste, ville (Paris, Lyon, Strasbourg...), institution (OCDE, Beko, THY...)...">
            </div>
            
            <div class="filter-controls-row">
                <div class="control-group">
                    <label class="control-label" id="i18n-domain-label" for="domainSelect" data-tr="📂 Uzmanlık Alanı :" data-fr="📂 Domaine d'activité :">📂 Uzmanlık Alanı :</label>
                    <select id="domainSelect" class="filter-select" onchange="window.TrackerEngine.Filter.setDomain(this.value)">
                        <option value="all" id="opt-domain-all" data-tr="🌐 Tüm Alanlar" data-fr="🌐 Tous les domaines">🌐 Tüm Alanlar</option>
                        <option value="it" id="opt-domain-it" data-tr="💻 IT, Yazılım &amp; AI" data-fr="💻 IT, Logiciel &amp; IA">💻 IT, Yazılım &amp; AI</option>
                        <option value="logistics" id="opt-domain-logistics" data-tr="📦 Lojistik &amp; Taşımacılık" data-fr="📦 Logistique &amp; Transport">📦 Lojistik &amp; Taşımacılık</option>
                        <option value="sales" id="opt-domain-sales" data-tr="💼 Satış &amp; İhracat" data-fr="💼 Vente, Export &amp; Marketing">💼 Satış &amp; İhracat</option>
                        <option value="legal_policy" id="opt-domain-legal" data-tr="⚖️ Hukuk &amp; Uluslararası İlişkiler" data-fr="⚖️ Droit &amp; Relations Internationales">⚖️ Hukuk &amp; Uluslararası İlişkiler</option>
                        <option value="media_trans" id="opt-domain-media" data-tr="🗣️ Çeviri &amp; Medya" data-fr="🗣️ Traduction &amp; Médias">🗣️ Çeviri &amp; Medya</option>
                        <option value="hr_admin" id="opt-domain-hr" data-tr="👥 İK &amp; Yönetim" data-fr="👥 RH &amp; Administration">👥 İK &amp; Yönetim</option>
                        <option value="craft_pme" id="opt-domain-craft" data-tr="🛠️ Zanaat &amp; Saha İşleri" data-fr="🛠️ Métiers de Terrain &amp; PME">🛠️ Zanaat &amp; Saha İşleri</option>
                    </select>
                </div>
                <div class="control-group">
                    <label class="control-label" id="i18n-sort-label" for="sortSelect" data-tr="🔄 Sıralama :" data-fr="🔄 Trier par :">🔄 Sıralama :</label>
                    <select id="sortSelect" class="filter-select" onchange="window.TrackerEngine.Filter.setSort(this.value)">
                        <option value="score_desc" id="opt-sort-score" data-tr="🎯 En Yüksek Uygunluk (Azalan)" data-fr="🎯 Score de Pertinence (Décroissant)">🎯 En Yüksek Uygunluk (Azalan)</option>
                        <option value="date_desc" id="opt-sort-date" data-tr="📅 En Yeni İlanlar (Tarih)" data-fr="📅 Date de Publication (Plus Récent)">📅 En Yeni İlanlar (Tarih)</option>
                        <option value="company_asc" id="opt-sort-company" data-tr="🏢 Şirket Adı (A-Z)" data-fr="🏢 Entreprise (A-Z)">🏢 Şirket Adı (A-Z)</option>
                    </select>
                </div>
            </div>
            
            <div class="filter-facets-row">
                <button class="filter-pill-btn active" data-filter-val="all" data-tr="Tümü" data-fr="Toutes" onclick="window.TrackerEngine.Filter.setCategory('all'); document.querySelectorAll('.filter-pill-btn[data-filter-val]').forEach(b=>b.classList.remove('active')); this.classList.add('active');">Tümü</button>
                <button class="filter-pill-btn pill-ccift" id="filter-btn-ccift" onclick="window.TrackerEngine.Filter.toggleCcift(); this.classList.toggle('active');">
                    {SVG_ICONS["shield_check"]} <span data-tr="CCIFT &amp; DEİK Üyeleri" data-fr="Membres CCIFT &amp; DEİK">CCIFT &amp; DEİK Üyeleri</span>
                </button>
                <button class="filter-pill-btn pill-no-french" id="filter-btn-no-french" onclick="window.TrackerEngine.Filter.toggleNoFrench(); this.classList.toggle('active');">
                    {SVG_ICONS["check_circle"]} <span data-tr="Fransızca Şart Değil" data-fr="Sans Français Obligatoire">Fransızca Şart Değil</span>
                </button>
                <button class="filter-pill-btn" data-filter-val="institutions" onclick="window.TrackerEngine.Filter.setCategory('institutions'); document.querySelectorAll('.filter-pill-btn[data-filter-val]').forEach(b=>b.classList.remove('active')); this.classList.add('active');">
                    {SVG_ICONS["landmark"]} <span data-tr="Uluslararası Kurumlar" data-fr="Institutions Internationales">Uluslararası Kurumlar</span>
                </button>
                <button class="filter-pill-btn" data-filter-val="companies" onclick="window.TrackerEngine.Filter.setCategory('companies'); document.querySelectorAll('.filter-pill-btn[data-filter-val]').forEach(b=>b.classList.remove('active')); this.classList.add('active');">
                    {SVG_ICONS["building"]} <span data-tr="Türk Holdingleri" data-fr="Multinationales Turques">Türk Holdingleri</span>
                </button>
                <button class="filter-pill-btn" data-filter-val="logistics" onclick="window.TrackerEngine.Filter.setCategory('logistics'); document.querySelectorAll('.filter-pill-btn[data-filter-val]').forEach(b=>b.classList.remove('active')); this.classList.add('active');">
                    {SVG_ICONS["plane"]} <span data-tr="Lojistik &amp; Ticaret" data-fr="Logistique &amp; Commerce">Lojistik &amp; Ticaret</span>
                </button>
                <button class="filter-pill-btn" data-filter-val="tech" onclick="window.TrackerEngine.Filter.setCategory('tech'); document.querySelectorAll('.filter-pill-btn[data-filter-val]').forEach(b=>b.classList.remove('active')); this.classList.add('active');">
                    {SVG_ICONS["rocket"]} <span data-tr="Tech &amp; Scale-ups" data-fr="Tech &amp; Scale-ups">Tech &amp; Scale-ups</span>
                </button>
                <button class="filter-pill-btn" data-filter-val="pme" onclick="window.TrackerEngine.Filter.setCategory('pme'); document.querySelectorAll('.filter-pill-btn[data-filter-val]').forEach(b=>b.classList.remove('active')); this.classList.add('active');">
                    {SVG_ICONS["briefcase"]} <span data-tr="KOBİ &amp; Saha" data-fr="PME &amp; Terrain">KOBİ &amp; Saha</span>
                </button>
                
                <span class="facet-separator" aria-hidden="true"></span>
                
                <button class="filter-pill-btn pill-fav" onclick="const isFav = this.classList.toggle('active'); window.TrackerEngine.Filter.setStatusFilter(isFav ? 'fav' : 'all');">
                    {SVG_ICONS["bookmark"]} <span data-tr="Sadece Favoriler" data-fr="Favoris Uniquement">Sadece Favoriler</span>
                </button>
                <button class="filter-pill-btn pill-tracked" onclick="const isTracked = this.classList.toggle('active'); window.TrackerEngine.Filter.setStatusFilter(isTracked ? 'tracked' : 'all');">
                    {SVG_ICONS["file_text"]} <span data-tr="Takip Edilenler" data-fr="Candidatures Suivies">Takip Edilenler</span>
                </button>
            </div>

            <div class="filter-status-row">
                <div class="results-summary" id="filter-results-summary">
                    toplam <strong>{total}</strong> fırsattan <strong>{total}</strong> tanesi listeleniyor
                </div>
                <button class="reset-filter-btn" id="btn-reset-filters" onclick="window.TrackerEngine.Filter.resetAll()">Filtreleri Sıfırla 🔄</button>
            </div>
        </div>

        <div id="no-results-box" style="display: none; text-align: center; padding: 40px; background: var(--surface-card); border-radius: 14px; border: 1px solid var(--border-default); max-width: 600px; margin: 30px auto;">
            <p style="font-size: 1.1rem; color: var(--text-tertiary); margin-bottom: 14px;" data-tr="Aradığınız kriterlere uygun fırsat bulunamadı." data-fr="Aucune opportunité ne correspond à vos critères de recherche.">Aradığınız kriterlere uygun fırsat bulunamadı.</p>
            <button class="apply-btn" style="max-width: 220px; margin: 0 auto;" onclick="window.TrackerEngine.Filter.resetAll()" data-tr="Filtreleri Temizle 🔄" data-fr="Effacer les Filtres 🔄">Filtreleri Temizle 🔄</button>
        </div>

        <!-- GRILLE COMPLÈTE DES CARTES -->
        <div class="cards-grid" id="cardsGrid">
            {cards_html}
        </div>

    </main>

    <!-- ==================================================================== -->
    <!-- ONGLET 2 : BAŞVURU TAKİBİ / PIPELINE KANBAN                           -->
    <!-- ==================================================================== -->
    <section id="tab-content-tracker" class="tab-pane" style="display: none;">
        
        <div class="tracker-header-box">
            <h2 id="i18n-tracker-title">Başvuru ve Adaylık Takip Hattı (Pipeline)</h2>
            <p id="i18n-tracker-subtitle">Fransa'daki başvurularınızı adım adım yönetin, mülakat tarihlerini ve kişisel notlarınızı kaydedin.</p>
        </div>

        <!-- STATS PIPELINE -->
        <div class="tracker-stats-grid">
            <div class="tracker-stat-box">
                <div class="t-num" id="tracker-stat-total">0</div>
                <div class="t-lbl" data-tr="Toplam Takipte" data-fr="Total Suivi">Toplam Takipte</div>
            </div>
            <div class="tracker-stat-box box-applied">
                <div class="t-num" id="tracker-stat-applied">0</div>
                <div class="t-lbl" data-tr="Başvuruldu / Süreçte" data-fr="Postulé / En cours">Başvuruldu / Süreçte</div>
            </div>
            <div class="tracker-stat-box box-interview">
                <div class="t-num" id="tracker-stat-interview">0</div>
                <div class="t-lbl" data-tr="Mülakat Planlandı" data-fr="Entretien Prévu">Mülakat Planlandı</div>
            </div>
            <div class="tracker-stat-box box-offer">
                <div class="t-num" id="tracker-stat-offer">0</div>
                <div class="t-lbl" data-tr="Kabul / Teklif" data-fr="Offre / Acceptée">Kabul / Teklif</div>
            </div>
        </div>

        <!-- TOOLBAR DU TRACKER -->
        <div class="tracker-toolbar">
            <input type="text" id="trackerSearchInput" class="tracker-search-input" placeholder="Takip edilen başvurularda ara..." data-placeholder-tr="Takip edilen başvurularda ara..." data-placeholder-fr="Rechercher dans les candidatures suivies...">
            <div class="tracker-actions-group">
                <button class="btn-action-tracker btn-export-csv" id="btn-export-csv" data-tr="CSV Dışa Aktar (Superviseur FR)" data-fr="Exporter en CSV (Superviseur FR)" onclick="window.TrackerEngine.exportCSV()">CSV Dışa Aktar (Superviseur FR)</button>
                <button class="btn-action-tracker btn-export-json" id="btn-export-json" data-tr="JSON Dışa Aktar" data-fr="Exporter en JSON" onclick="window.TrackerEngine.exportJSON()">JSON Dışa Aktar</button>
                <button class="btn-action-tracker btn-clear-tracker" id="btn-clear-tracker" data-tr="Listeyi Temizle" data-fr="Effacer la Liste" onclick="window.TrackerEngine.clearAllApplications()">Listeyi Temizle</button>
            </div>
        </div>

        <div id="tracker-empty-notice" class="tracker-empty-board" style="display: none;">
            <h3 data-tr="Henüz takibe alınmış bir başvuru yok" data-fr="Aucune candidature enregistrée pour le moment">Henüz takibe alınmış bir başvuru yok</h3>
            <p data-tr="İlanlar sekmesinde ilgilendiğiniz ilanların altındaki 'Takip Et' butonuna tıklayarak veya kartı favorilere ekleyerek takip sürecinizi başlatabilirsiniz." data-fr="Dans l'onglet Explorer, cliquez sur 'Suivre' pour ajouter une offre à votre tableau de bord.">İlanlar sekmesinde ilgilendiğiniz ilanların altındaki 'Takip Et' butonuna tıklayarak veya kartı favorilere ekleyerek takip sürecinizi başlatabilirsiniz.</p>
            <button class="apply-btn" style="max-width: 240px; margin: 0 auto;" onclick="window.TrackerEngine.switchTab('explore')" data-tr="İlanları Keşfetmeye Başla" data-fr="Commencer à Explorer les Offres">İlanları Keşfetmeye Başla</button>
        </div>

        <!-- PIPELINE KANBAN (4 ÉTAPES) -->
        <div class="kanban-board">
            
            <!-- COLONNE 1 : KAYDEDİLDİ / ENREGISTRÉ -->
            <div class="kanban-column" id="kanban-col-saved">
                <div class="kanban-col-header">
                    <div class="kanban-col-title-wrap">
                        {SVG_ICONS["bookmark"]}
                        <span class="kanban-col-title" id="i18n-col-saved-title">Kaydedildi / Hedef</span>
                    </div>
                    <span class="kanban-count-pill" id="count-col-saved">0</span>
                </div>
                <div class="kanban-items-list" id="kanban-items-saved"></div>
            </div>

            <!-- COLONNE 2 : BAŞVURULDU / POSTULÉ -->
            <div class="kanban-column" id="kanban-col-applied">
                <div class="kanban-col-header">
                    <div class="kanban-col-title-wrap">
                        {SVG_ICONS["briefcase"]}
                        <span class="kanban-col-title" id="i18n-col-applied-title">Başvuruldu</span>
                    </div>
                    <span class="kanban-count-pill" id="count-col-applied">0</span>
                </div>
                <div class="kanban-items-list" id="kanban-items-applied"></div>
            </div>

            <!-- COLONNE 3 : MÜLAKAT / ENTRETIEN -->
            <div class="kanban-column" id="kanban-col-interview">
                <div class="kanban-col-header">
                    <div class="kanban-col-title-wrap">
                        {SVG_ICONS["sparkles"]}
                        <span class="kanban-col-title" id="i18n-col-interview-title">Mülakat Aşamasında</span>
                    </div>
                    <span class="kanban-count-pill" id="count-col-interview">0</span>
                </div>
                <div class="kanban-items-list" id="kanban-items-interview"></div>
            </div>

            <!-- COLONNE 4 : KABUL / OFFRE -->
            <div class="kanban-column" id="kanban-col-offer">
                <div class="kanban-col-header">
                    <div class="kanban-col-title-wrap">
                        {SVG_ICONS["check_circle"]}
                        <span class="kanban-col-title" id="i18n-col-offer-title">Kabul / Teklif Alındı</span>
                    </div>
                    <span class="kanban-count-pill" id="count-col-offer">0</span>
                </div>
                <div class="kanban-items-list" id="kanban-items-offer"></div>
            </div>

        </div>

    </section>

    <!-- ==================================================================== -->
    <!-- ONGLET 3 : REHBER & BELGELER / GUIDE VISA & OUTILS BILATÉRAUX          -->
    <!-- ==================================================================== -->
    <section id="tab-content-guide" class="tab-pane" style="display: none;">
        
        <div class="guide-container">
            
            <div class="tracker-header-box" style="margin-bottom: 26px;">
                <h2 data-tr="Fransa İstihdam, Vize &amp; Başvuru Rehberi" data-fr="Guide Emploi en France, Visas &amp; Outils Bilatéraux">Fransa İstihdam, Vize &amp; Başvuru Rehberi</h2>
                <p data-tr="Türkiye'den Fransa'ya transfer süreçleri, vize prosedürleri ve hazır başvuru şablonları." data-fr="Procédures de transfert Turquie-France, démarches visas et modèles de candidature prêts à l'emploi.">Türkiye'den Fransa'ya transfer süreçleri, vize prosedürleri ve hazır başvuru şablonları.</p>
            </div>

            <!-- SECTION A : LES 4 VOIES LÉGALES DE VISA -->
            <div class="guide-card-section">
                <div class="guide-section-header">
                    <h3 data-tr="1. Türkiye'den Fransa'ya 3 Öncelikli Kapı + Standart Yol" data-fr="1. Turquie ➔ France : 3 Voies Prioritaires + Voie Standard">{SVG_ICONS["plane"]} 1. Türkiye'den Fransa'ya 3 Öncelikli Kapı + Standart Yol</h3>
                    <p data-tr="Klasik çalışma izni engeline takılmadan Fransa'ya geçiş sağlayan öncelikli statüler." data-fr="Statuts prioritaires permettant de s'installer en France sans blocage d'autorisation de travail standard.">Klasik çalışma izni engeline takılmadan Fransa'ya geçiş sağlayan öncelikli statüler.</p>
                </div>
                <div class="guide-grid-2">
                    <div class="visa-method-card">
                        <span class="method-tag" data-tr="Şirket İçi Transfer (ICT)" data-fr="Détachement Intra-Groupe (ICT)">Şirket İçi Transfer (ICT)</span>
                        <h4>{SVG_ICONS["shield_check"]} <span data-tr="1. Salarié Détaché ICT (CCIFT &amp; DEİK Üyeleri)" data-fr="1. Salarié Détaché ICT (Membres CCIFT &amp; DEİK)">1. Salarié Détaché ICT (CCIFT &amp; DEİK Üyeleri)</span></h4>
                        <p data-tr="Beko, THY, Ekol, Barsan, Şişecam gibi holdinglerin Türkiye merkezinde en az 3-6 ay çalışan uzman veya yöneticilerin Fransa şubelerine tayin edilmesi. <strong>Yerel işgücü piyasası araştırması (opposabilité de l'emploi) ve dil sınavı aranmaz!</strong> En hızlı vize yoludur." data-fr="Détachement d'experts ou cadres d'un groupe en Turquie (Beko, THY, Ekol, Barsan, Şişecam...) vers sa filiale française. <strong>Exonération totale du test du marché de l'emploi et dispense de test de langue !</strong> Procédure bilatérale ultra-rapide (Convention 1972).">Beko, THY, Ekol, Barsan, Şişecam gibi holdinglerin Türkiye merkezinde en az 3-6 ay çalışan uzman veya yöneticilerin Fransa şubelerine tayin edilmesi. <strong>Yerel işgücü piyasası araştırması (opposabilité de l'emploi) ve dil sınavı aranmaz!</strong> En hızlı vize yoludur.</p>
                    </div>
                    <div class="visa-method-card">
                        <span class="method-tag" data-tr="Passeport Talent" data-fr="Passeport Talent">Passeport Talent</span>
                        <h4>{SVG_ICONS["rocket"]} <span data-tr="2. Yetenek Pasaportu (Passeport Talent - Salarié Qualifié)" data-fr="2. Passeport Talent (Tech &amp; Entreprise Innovante)">2. Yetenek Pasaportu (Passeport Talent - Salarié Qualifié)</span></h4>
                        <p data-tr="Fransa'daki teknoloji scale-up'ları (Mistral AI, Datadog, Qonto) ve yenilikçi şirketler tarafından verilir. Yüksek lisans veya brüt asgari ücretin en az 2 katı (yaklaşık 43.000 €/yıl) maaş teklifi durumunda eş ve çocuklara da doğrudan tam çalışma hakkı sağlar." data-fr="Délivré par les scale-ups tech (Mistral AI, Datadog, Qonto) et entreprises innovantes. Sur offre de salaire ≥ 2x SMIC (env. 43 000 €/an), octroie un titre pluriannuel de 4 ans avec droit de travail immédiat pour le conjoint.">Fransa'daki teknoloji scale-up'ları (Mistral AI, Datadog, Qonto) ve yenilikçi şirketler tarafından verilir. Yüksek lisans veya brüt asgari ücretin en az 2 katı (yaklaşık 43.000 €/yıl) maaş teklifi durumunda eş ve çocuklara da doğrudan tam çalışma hakkı sağlar.</p>
                    </div>
                    <div class="visa-method-card">
                        <span class="method-tag" data-tr="Özel MEAE Diplomatik Statüsü" data-fr="Statut Diplomatique MEAE">Özel MEAE Diplomatik Statüsü</span>
                        <h4>{SVG_ICONS["landmark"]} <span data-tr="3. Uluslararası &amp; Avrupa Kuruluşları (OECD, CoE, UNESCO)" data-fr="3. Organisations Internationales &amp; Européennes (OCDE, Conseil de l'Europe, UNESCO)">3. Uluslararası &amp; Avrupa Kuruluşları (OECD, CoE, UNESCO)</span></h4>
                        <p data-tr="Türkiye'nin kurucu veya tam üye olduğu kurumlarda istihdam. Standart Fransa çalışma vizesi aranmaz; Dışişleri Bakanlığı (MEAE) tarafından doğrudan özel uluslararası diplomatik oturum kartı verilir. Taşınma masrafları kurumca karşılanır." data-fr="Emploi au sein d'institutions dont la Turquie est membre fondateur. Aucun visa de travail classique requis : délivrance directe d'un Titre Spécial MEAE protocolaire. Exonération fiscale et prise en charge intégrale du déménagement.">Türkiye'nin kurucu veya tam üye olduğu kurumlarda istihdam. Standart Fransa çalışma vizesi aranmaz; Dışişleri Bakanlığı (MEAE) tarafından doğrudan özel uluslararası diplomatik oturum kartı verilir. Taşınma masrafları kurumca karşılanır.</p>
                    </div>
                    <div class="visa-method-card">
                        <span class="method-tag" data-tr="Klasik Çalışma İzni" data-fr="Droit Commun (Métiers en Tension)">Klasik Çalışma İzni</span>
                        <h4>{SVG_ICONS["file_text"]} <span data-tr="4. Salarié de Droit Commun &amp; Métiers en Tension" data-fr="4. Salarié de Droit Commun &amp; Métiers en Tension">4. Salarié de Droit Commun &amp; Métiers en Tension</span></h4>
                        <p data-tr="Fransa'da personel açığı bulunan sektörlerde (bilişim, lojistik, inşaat, mühendislik) Fransız işverenin İçişleri Bakanlığı yabancı işçi portalından (ANEF) çalışma izni almasıyla verilen oturum türü." data-fr="Pour les métiers en tension en France (IT, logistique, BTP, ingénierie). Demande d'autorisation de travail déposée par l'employeur sur le portail ANEF du Ministère de l'Intérieur.">Fransa'da personel açığı bulunan sektörlerde (bilişim, lojistik, inşaat, mühendislik) Fransız işverenin İçişleri Bakanlığı yabancı işçi portalından (ANEF) çalışma izni almasıyla verilen oturum türü.</p>
                    </div>
                </div>
            </div>

            <!-- SECTION B : CHECKLIST INTERACTIVE -->
            <div class="guide-card-section">
                <div class="guide-section-header">
                    <h3 data-tr="2. Başvuru Öncesi İnteraktif Aday Kontrol Listesi (Checklist)" data-fr="2. Checklist Interactive Avant Candidature">{SVG_ICONS["check_circle"]} 2. Başvuru Öncesi İnteraktif Aday Kontrol Listesi (Checklist)</h3>
                    <p data-tr="İlerlemenizi işaretleyin; durumunuz otomatik olarak tarayıcınızda saklanır." data-fr="Cochez vos étapes terminées ; votre progression est automatiquement sauvegardée dans votre navigateur.">İlerlemenizi işaretleyin; durumunuz otomatik olarak tarayıcınızda saklanır.</p>
                </div>
                <div class="checklist-items-box">
                    <label class="checklist-item" for="chk-passport">
                        <input type="checkbox" id="chk-passport" class="guide-checkbox">
                        <span class="checklist-label" data-tr="Pasaport Geçerlilik Süresi: Planlanan seyahat tarihinden itibaren en az 12 ay geçerli bordo/yeşil pasaport." data-fr="Validité du Passeport : Passeport valide au moins 12 mois à compter de la date de départ envisagée.">Pasaport Geçerlilik Süresi: Planlanan seyahat tarihinden itibaren en az 12 ay geçerli bordo/yeşil pasaport.</span>
                    </label>
                    <label class="checklist-item" for="chk-cv">
                        <input type="checkbox" id="chk-cv" class="guide-checkbox">
                        <span class="checklist-label" data-tr="Avrupa Standartlarında CV (Europass / ATS Uyumlu): Fotoğrafsız veya nötr fotoğraflı, İngilizce veya Fransızca 1-2 sayfalık özgeçmiş." data-fr="CV aux Normes Européennes (Compatible Europass / ATS) : 1 à 2 pages en anglais ou français, clair et synthétique.">Avrupa Standartlarında CV (Europass / ATS Uyumlu): Fotoğrafsız veya nötr fotoğraflı, İngilizce veya Fransızca 1-2 sayfalık özgeçmiş.</span>
                    </label>
                    <label class="checklist-item" for="chk-diploma">
                        <input type="checkbox" id="chk-diploma" class="guide-checkbox">
                        <span class="checklist-label" data-tr="Diploma &amp; Transkript Çevirileri: Yeminli tercüman onaylı, tercihen apostilli lisans/yüksek lisans belgeleri." data-fr="Diplômes et Relevés de Notes Traduits : Traduction assermentée en français/anglais, avec apostille si possible.">Diploma &amp; Transkript Çevirileri: Yeminli tercüman onaylı, tercihen apostilli lisans/yüksek lisans belgeleri.</span>
                    </label>
                    <label class="checklist-item" for="chk-linkedin">
                        <input type="checkbox" id="chk-linkedin" class="guide-checkbox">
                        <span class="checklist-label" data-tr="LinkedIn Profilinin Güncellenmesi: Profil dilinin İngilizce ve/veya Fransızca yapılması, 'Open to Work' konumunun Fransa olarak işaretlenmesi." data-fr="Mise à jour du profil LinkedIn : Titre et résumé en anglais/français, statut 'Open to Work' ciblé sur la France.">LinkedIn Profilinin Güncellenmesi: Profil dilinin İngilizce ve/veya Fransızca yapılması, 'Open to Work' konumunun Fransa olarak işaretlenmesi.</span>
                    </label>
                    <label class="checklist-item" for="chk-adli-sicil">
                        <input type="checkbox" id="chk-adli-sicil" class="guide-checkbox">
                        <span class="checklist-label" data-tr="Adli Sicil Kaydı (e-Devlet): Fransızca veya İngilizce barkodlu adli sicil belgesi." data-fr="Extrait de Casier Judiciaire (e-Devlet) : Document officiel avec code QR / code-barres en français ou anglais.">Adli Sicil Kaydı (e-Devlet): Fransızca veya İngilizce barkodlu adli sicil belgesi.</span>
                    </label>
                </div>
            </div>

            <!-- SECTION C : TEMPLATES D'EMAIL BILINGUES -->
            <div class="guide-card-section">
                <div class="guide-section-header">
                    <h3 data-tr="3. Hazır E-posta &amp; Motivasyon Mektubu Şablonları (1-Tık Kopyala)" data-fr="3. Modèles d'Email &amp; Lettres de Motivation (Copie en 1-Clic)">{SVG_ICONS["file_text"]} 3. Hazır E-posta &amp; Motivasyon Mektubu Şablonları (1-Tık Kopyala)</h3>
                    <p data-tr="Fransa'daki Türk yöneticilere veya uluslararası İK temsilcilerine doğrudan gönderebileceğiniz taslaklar." data-fr="Modèles prêts à l'envoi pour contacter directement les dirigeants de groupes turcs ou les RH internationaux en France.">Fransa'daki Türk yöneticilere veya uluslararası İK temsilcilerine doğrudan gönderebileceğiniz taslaklar.</p>
                </div>

                <!-- ŞABLON 1 : TÜRK HOLDİNGİ FRANSA ŞUBESİ (ICT) -->
                <div class="template-block">
                    <div class="template-top">
                        <span class="template-title" data-tr="Şablon 1 : Türk Holdingi Fransa Şubesi Direktörüne Doğrudan Başvuru" data-fr="Modèle 1 : Prise de Contact Directe avec la Direction / DRH d'une Filiale Turque en France">Şablon 1 : Türk Holdingi Fransa Şubesi Direktörüne Doğrudan Başvuru</span>
                        <button class="copy-template-btn" onclick="window.TrackerEngine.copyTemplate('tmpl-1', this)">
                            {SVG_ICONS["copy"]} <span data-tr="Metni Kopyala" data-fr="Copier le Texte">Metni Kopyala</span>
                        </button>
                    </div>
                    <div class="template-content" id="tmpl-1">Sayın İlgili / Cher(e) Responsable RH,

Türkiye'de yerleşik olarak [Uzmanlık Alanınız / Örn: Tedarik Zinciri ve Operasyon Yönetimi] alanında [X] yıllık profesyonel deneyime sahibim. Şirketinizin Fransa'daki güçlü yatırımlarını ve [Beko France / Ekol / Barsan / THY] bünyesindeki başarılı büyümesini yakından takip etmekteyim.

İki ülke arasındaki ticari dinamiklere ve operasyonel kültüre hakimiyetim doğrultusunda, Fransa ofisinizde açılacak kadrolarda görev almaya hazırım. Mevzuat kapsamında Türkiye'den Şirket İçi Transfer (Salarié Détaché ICT) veya Yetenek Pasaportu prosedürleriyle intikalim hukuken mümkündür.

İngilizce seviyem C1 düzeyinde olup (Fransızca başlangıç/orta seviyededir), ekte yer alan özgeçmişimi değerlendirmenize sunar, uygun görmeniz halinde detayları çevrim içi bir görüşmede paylaşmaktan memnuniyet duyarım.

Saygılarımla / Cordialement,
[Adınız Soyadınız] - Tel: +90 5XX XXX XX XX - LinkedIn: linkedin.com/in/profiliniz</div>
                </div>

                <!-- ŞABLON 2 : PARIS TECH & SCALE-UP (ANGLAIS) -->
                <div class="template-block">
                    <div class="template-top">
                        <span class="template-title" data-tr="Şablon 2 : Paris Tech &amp; Scale-up Başvurusu (%100 İngilizce - Passeport Talent)" data-fr="Modèle 2 : Candidature Scale-up Tech Paris (100% Anglais - Passeport Talent)">Şablon 2 : Paris Tech &amp; Scale-up Başvurusu (%100 İngilizce - Passeport Talent)</span>
                        <button class="copy-template-btn" onclick="window.TrackerEngine.copyTemplate('tmpl-2', this)">
                            {SVG_ICONS["copy"]} <span data-tr="Metni Kopyala" data-fr="Copier le Texte">Metni Kopyala</span>
                        </button>
                    </div>
                    <div class="template-content" id="tmpl-2">Dear Hiring Team,

I am writing to express my strong enthusiasm for the [Job Title / e.g. Senior Software Engineer / Data Scientist] role at [Company Name] in Paris.

With [X] years of experience in [Core Technologies / Field], I have successfully led projects in fast-paced international environments. Given that your engineering team operates in English, I am confident in my ability to contribute immediately to your product roadmap.

Regarding relocation to France: as a qualified candidate, the French "Passeport Talent - Salarié Qualifié / Entreprise Innovante" offers a fast-track, employer-friendly visa process with full work authorization for myself and family.

I look forward to discussing how my background aligns with your mission. Thank you for your time and consideration.

Best regards,
[Your Full Name] - [Phone / WhatsApp] - [GitHub / Portfolio Link]</div>
                </div>
            </div>

            <!-- SECTION D : LIENS OFFICIELS -->
            <div class="guide-card-section">
                <div class="guide-section-header">
                    <h3 data-tr="4. Resmi Vize ve İkili Kurum Portalları" data-fr="4. Portails Officiels des Visas &amp; Organismes Bilatéraux">{SVG_ICONS["globe"]} 4. Resmi Vize ve İkili Kurum Portalları</h3>
                    <p data-tr="Doğrudan mevzuat ve başvuru takibi yapabileceğiniz yetkili platformlar." data-fr="Plateformes administratives et institutionnelles de référence.">Doğrudan mevzuat ve başvuru takibi yapabileceğiniz yetkili platformlar.</p>
                </div>
                <div class="guide-grid-2">
                    <div class="visa-method-card">
                        <h4>{SVG_ICONS["external_link"]} <span data-tr="France-Visas (Resmi Portal)" data-fr="France-Visas (Portail Officiel)">France-Visas (Resmi Portal)</span></h4>
                        <p><span data-tr="Fransa vize türlerinin şartları, evrak listeleri ve resmi başvuru kılavuzu: " data-fr="Conditions d'octroi des visas, listes de pièces justificatives et guide officiel de dépôt : ">Fransa vize türlerinin şartları, evrak listeleri ve resmi başvuru kılavuzu: </span><br><a href="https://france-visas.gouv.fr/" target="_blank" rel="noopener noreferrer" style="color: var(--accent-primary); font-weight: 700;">france-visas.gouv.fr ↗</a></p>
                    </div>
                    <div class="visa-method-card">
                        <h4>{SVG_ICONS["external_link"]} <span data-tr="ANEF (Yabancılar Dijital Portalı)" data-fr="ANEF (Administration Numérique pour les Étrangers)">ANEF (Yabancılar Dijital Portalı)</span></h4>
                        <p><span data-tr="Fransız İçişleri Bakanlığı çalışma izni ve Yetenek Pasaportu online işlem platformu: " data-fr="Plateforme dématérialisée du Ministère de l'Intérieur pour les autorisations de travail et Passeport Talent : ">Fransız İçişleri Bakanlığı çalışma izni ve Yetenek Pasaportu online işlem platformu: </span><br><a href="https://administration-etrangers-en-france.interieur.gouv.fr/" target="_blank" rel="noopener noreferrer" style="color: var(--accent-primary); font-weight: 700;">administration-etrangers-en-france.interieur.gouv.fr ↗</a></p>
                    </div>
                    <div class="visa-method-card">
                        <h4>{SVG_ICONS["shield_check"]} <span data-tr="CCIFT (Fransız-Türk Ticaret Odası)" data-fr="CCIFT (Chambre de Commerce Franco-Turque)">CCIFT (Fransız-Türk Ticaret Odası)</span></h4>
                        <p><span data-tr="İkili ticaret ağı, üye şirketler ve istihdam rehberi: " data-fr="Réseau bilatéral, annuaire des entreprises membres et guide d'investissement : ">İkili ticaret ağı, üye şirketler ve istihdam rehberi: </span><br><a href="https://www.ccift.com/" target="_blank" rel="noopener noreferrer" style="color: var(--accent-primary); font-weight: 700;">ccift.com ↗</a></p>
                    </div>
                    <div class="visa-method-card">
                        <h4>{SVG_ICONS["shield_check"]} <span data-tr="DEİK Türkiye-Fransa İş Konseyi" data-fr="DEİK Conseil d'Affaires Turquie-France">DEİK Türkiye-Fransa İş Konseyi</span></h4>
                        <p><span data-tr="Dış Ekonomik İlişkiler Kurulu Türkiye-Fransa ikili iş konseyi portali: " data-fr="Conseil des Relations Économiques Extérieures de Turquie (partenariats bilatéraux) : ">Dış Ekonomik İlişkiler Kurulu Türkiye-Fransa ikili iş konseyi portali: </span><br><a href="https://www.deik.org.tr/" target="_blank" rel="noopener noreferrer" style="color: var(--accent-primary); font-weight: 700;">deik.org.tr ↗</a></p>
                    </div>
                </div>
            </div>

        </div>

    </section>

    <!-- ==================================================================== -->
    <!-- MODAL DE SUIVI & ÉDITION DE CANDIDATURE                                -->
    <!-- ==================================================================== -->
    <div id="tracker-modal" class="modal-overlay" style="display: none;">
        <div class="modal-box">
            <div class="modal-header">
                <h3 id="i18n-modal-title" data-tr="Başvuru Takip Detayları" data-fr="Modifier les détails de la candidature">Başvuru Takip Detayları</h3>
                <button type="button" class="modal-close-btn" id="modal-close-btn" aria-label="Kapat / Fermer">&times;</button>
            </div>
            
            <form id="tracker-form">
                <input type="hidden" id="modal-job-id" value="">

                <div class="modal-job-info">
                    <div class="modal-job-company" id="modal-card-company">Şirket</div>
                    <div class="modal-job-title" id="modal-card-title">Pozisyon</div>
                </div>

                <div class="form-group">
                    <label class="form-label" for="modal-status" data-tr="Aşama / Durum (Pipeline):" data-fr="Étape / Statut :">Aşama / Durum (Pipeline):</label>
                    <select id="modal-status" class="form-control">
                        <option value="saved" data-tr="Kaydedildi / Hedef (Enregistré)" data-fr="Enregistré / Cible">Kaydedildi / Hedef (Enregistré)</option>
                        <option value="applied" data-tr="Başvuruldu (Postulé)" data-fr="Postulé">Başvuruldu (Postulé)</option>
                        <option value="interview" data-tr="Mülakat Aşamasında (Entretien)" data-fr="Entretien en Cours">Mülakat Aşamasında (Entretien)</option>
                        <option value="offer" data-tr="Kabul / Teklif Alındı (Offre Reçue)" data-fr="Offre Reçue / Accord">Kabul / Teklif Alındı (Offre Reçue)</option>
                    </select>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <div class="form-group">
                        <label class="form-label" for="modal-applied-date" data-tr="Başvuru Tarihi:" data-fr="Date de candidature :">Başvuru Tarihi:</label>
                        <input type="date" id="modal-applied-date" class="form-control">
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="modal-interview-date" data-tr="Mülakat Tarihi:" data-fr="Date d'entretien :">Mülakat Tarihi:</label>
                        <input type="date" id="modal-interview-date" class="form-control">
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label" for="modal-notes" data-tr="Kişisel Notlar &amp; Takip Bilgileri:" data-fr="Notes personnelles &amp; suivi :">Kişisel Notlar &amp; Takip Bilgileri:</label>
                    <textarea id="modal-notes" class="form-control" placeholder="Örn: LinkedIn'den İK müdürüne yazıldı, Europass İngilizce CV gönderildi, 2 hafta içinde geri dönüş bekleniyor..." data-placeholder-tr="Örn: LinkedIn'den İK müdürüne yazıldı, Europass İngilizce CV gönderildi, 2 hafta içinde geri dönüş bekleniyor..." data-placeholder-fr="Ex: Prise de contact sur LinkedIn avec le responsable RH, CV en anglais envoyé..."></textarea>
                </div>

                <div class="modal-footer">
                    <button type="button" class="modal-btn modal-btn-delete" id="modal-delete-btn" style="display: none;" data-tr="Takibi Bırak" data-fr="Supprimer du suivi">Takibi Bırak</button>
                    <div style="display: flex; gap: 8px;">
                        <button type="button" class="modal-btn modal-btn-cancel" id="modal-cancel-btn" data-tr="İptal" data-fr="Annuler">İptal</button>
                        <button type="submit" class="modal-btn modal-btn-save" data-tr="Kaydet" data-fr="Enregistrer">Kaydet</button>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <!-- TOAST CONTAINER -->
    <div id="toast-container" class="toast-container"></div>

    <!-- SCRIPT DE GESTION DU THÈME HAUTE COUTURE -->
    <script>
        function toggleTheme() {{
            const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('bilateral_theme', next);
            updateThemeButton(next);
            if (window.syncThemeColorMeta) window.syncThemeColorMeta(next);
        }}

        function updateThemeButton(theme) {{
            const btn = document.getElementById('themeToggleBtn');
            if (btn) {{
                if (theme === 'dark') {{
                    btn.innerHTML = `{SVG_ICONS["sun"]}`;
                    btn.title = "Açık Mod / Mode Clair";
                }} else {{
                    btn.innerHTML = `{SVG_ICONS["moon"]}`;
                    btn.title = "Karanlık Mod / Mode Sombre";
                }}
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            const curTheme = document.documentElement.getAttribute('data-theme') || 'light';
            updateThemeButton(curTheme);
            // Encarts informatifs : dépliés sur desktop, repliés par défaut sur mobile
            if (window.matchMedia('(min-width: 769px)').matches) {{
                document.querySelectorAll('details.info-collapsible').forEach(d => {{ d.open = true; }});
            }}
        }});
    </script>

    <!-- INJECTION DU MOTEUR JAVASCRIPT RÉACTIF TRACKER -->
    <script>
{engine_js_content}
    </script>

    <!-- MODULE BILATÉRAL FRANCE-TURQUIE : DRAWER & GÉNÉRATEUR LETTRE -->
    {drawer_markup_content}
    <script>
{drawer_js_content}
    </script>

    <!-- MODULE PWA & ACTUALISATION (SERVICE WORKER, INSTALL PROMPT, REFRESH) -->
    <script>
{pwa_js_content}
    </script>
</body>
</html>
    """

    with open(filepath, mode="w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[✓] Dashboard HTML Haute Couture complet généré : {filepath}")

    # Synchronisation automatique du point d'entrée PWA (index.html)
    index_path = os.path.join(base_dir, "index.html")
    with open(index_path, mode="w", encoding="utf-8") as findex:
        findex.write(html_content)
    print(f"[✓] Point d'entrée PWA synchronisé : {index_path}")
