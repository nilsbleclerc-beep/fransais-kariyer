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
                <span>CCIFT &amp; DEİK Üyesi / Membre Officiel</span>
            </div>
            '''

        cards_html += f"""
        <div class="job-card {'job-card-ccift' if is_ccift else ''} {'card-track-1' if track == 'voie_1' else ''} {'card-track-3' if track == 'voie_3' else ''}" 
             data-id="{idx}"
             data-track="{track}"
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
                    <button class="bookmark-btn" onclick="window.TrackerEngine.toggleBookmark({idx}, event)" title="Favorilere Ekle / Retirer">
                        <span class="star-icon">☆</span>
                    </button>
                </div>
            </div>
            
            <h3 class="job-title" data-original-text="{title_tr_safe}">{j.title}</h3>
            
            <div class="company-loc">
                <span class="company-name-text" data-original-text="{company_safe}">{SVG_ICONS["building"]} <strong>{j.company}</strong></span> &nbsp;|&nbsp; <span>{SVG_ICONS["map_pin"]} {j.location}</span>
            </div>
            
            <div class="visa-and-lang-box">
                <div class="val-item">
                    <span class="val-label">{SVG_ICONS["plane"]} Vize / Relokasyon:</span>
                    <span class="val-val val-visa">{visa_safe}</span>
                </div>
                <div class="val-item">
                    <span class="val-label">{SVG_ICONS["languages"]} Dil Durumu:</span>
                    <span class="val-val {lang_badge_class}" data-lang-badge="true" data-tr="{lang_badge_text_tr}" data-fr="{lang_badge_text_fr}">{lang_badge_text_tr}</span>
                </div>
            </div>
            
            <p class="snippet" data-original-text="{snippet_tr_safe}">{j.snippet}</p>
            
            <div class="tags-container card-tags">
                <!-- Rempli dynamiquement par JS selon la langue -->
            </div>

            <div class="card-tracker-status" style="display: none;"></div>
            
            <div class="card-footer">
                <a href="{j.url}" target="_blank" rel="noopener noreferrer" class="apply-btn">
                    <span>İlanı İncele / Başvur</span> {SVG_ICONS["external_link"]}
                </a>
                <button class="tracker-action-btn" onclick="window.TrackerEngine.openTrackerModal({idx})" title="Başvuru Takibine Ekle">
                    {SVG_ICONS["bookmark"]} <span>Takip Et</span>
                </button>
                <button class="tracker-action-btn" onclick="if(window.BilateralDrawer) window.BilateralDrawer.open({idx})" title="Vize Dosyası, İK İletişimi &amp; Lettre de Motivation">
                    {SVG_ICONS["file_text"]} <span>Dosya</span>
                </button>
                {f'<a href="{j.contact_info}" target="_blank" rel="noopener noreferrer" class="secondary-btn">{SVG_ICONS["building"]} Portal ↗</a>' if j.contact_info else ''}
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Fransa Kariyer &amp; Vize Rehberi | TR ⇄ FR Bilateral Hub</title>
    
    <!-- PWA & Mobile Web App Meta Tags -->
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#0f172a">
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
            padding: 16px 24px 60px 24px;
            transition: background-color 260ms cubic-bezier(0.16, 1, 0.3, 1), color 260ms cubic-bezier(0.16, 1, 0.3, 1);
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

        /* Filtres Multi-Facettes Linear Style */
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
            min-width: 280px;
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
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
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
            min-width: 260px;
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
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
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
    <nav class="main-tabs-nav">
        <button class="tab-nav-btn active" id="tabBtnExplore" onclick="window.TrackerEngine.switchTab('explore')">
            {SVG_ICONS["briefcase"]}
            <span id="i18n-tab-explore">Keşfet &amp; İlanlar</span>
            <span class="tab-badge" id="badge-explore-count">{total}</span>
        </button>
        <button class="tab-nav-btn" id="tabBtnTracker" onclick="window.TrackerEngine.switchTab('tracker')">
            {SVG_ICONS["bookmark"]}
            <span id="i18n-tab-tracker">Başvuru Takibi (Kanban)</span>
            <span class="tab-badge" id="badge-tracker-count">0</span>
        </button>
        <button class="tab-nav-btn" id="tabBtnGuide" onclick="window.TrackerEngine.switchTab('guide')">
            {SVG_ICONS["file_text"]}
            <span id="i18n-tab-guide">Rehber, Vize &amp; Belgeler</span>
        </button>
    </nav>

    <!-- ==================================================================== -->
    <!-- ONGLET 1 : KEŞFET / EXPLORER (GRILLE ET FILTRES MULTI-FACETTES)        -->
    <!-- ==================================================================== -->
    <main id="tab-content-explore" class="tab-pane">
        
        <div class="header">
            <h1 id="i18n-title">Türkiye'den Fransa'ya Vize & Relokasyon Destekli İş Fırsatları</h1>
            <p id="i18n-subtitle">Türkiye'de ikamet eden adayların başvurusuna açık, vize/relokasyon sağlayan veya uluslararası statü veren resmi kurumlar ve Türk şirketleri.</p>
        </div>

        <!-- 3 PORTES D'ACCÈS PRIORITAIRES (VOIE 1 / VOIE 2 / VOIE 3) -->
        <div class="priority-tracks-bar">
            <div class="tracks-bar-title" id="i18n-tracks-title">{SVG_ICONS["filter"]} 3 ÖNCELİKLİ YASAL İSTİHDAM KAPISI (VİZE / RELOKASYON) :</div>
            <div class="tracks-buttons-group">
                <button class="track-btn active" data-track="all" onclick="window.TrackerEngine.Filter.setTrack('all', this)" id="btn-track-all">
                    <div class="track-btn-left">
                        <span class="track-icon">{SVG_ICONS["globe"]}</span>
                        <span class="track-name" id="i18n-track-all">Tüm Kapılar / Tümü</span>
                    </div>
                    <span class="track-badge-count" id="count-track-all">{total}</span>
                </button>
                <button class="track-btn track-btn-1" data-track="voie_1" onclick="window.TrackerEngine.Filter.setTrack('voie_1', this)" id="btn-track-1">
                    <div class="track-btn-left">
                        <span class="track-icon">{SVG_ICONS["landmark"]}</span>
                        <span class="track-name" id="i18n-track-1">KAPI 1: Uluslararası Kurumlar</span>
                    </div>
                    <span class="track-badge-count" id="count-track-1">{track_counts['voie_1']}</span>
                </button>
                <button class="track-btn track-btn-2" data-track="voie_2" onclick="window.TrackerEngine.Filter.setTrack('voie_2', this)" id="btn-track-2">
                    <div class="track-btn-left">
                        <span class="track-icon">{SVG_ICONS["shield_check"]}</span>
                        <span class="track-name" id="i18n-track-2">KAPI 2: Türk Holdingleri (ICT)</span>
                    </div>
                    <span class="track-badge-count" id="count-track-2">{track_counts['voie_2']}</span>
                </button>
                <button class="track-btn track-btn-3" data-track="voie_3" onclick="window.TrackerEngine.Filter.setTrack('voie_3', this)" id="btn-track-3">
                    <div class="track-btn-left">
                        <span class="track-icon">{SVG_ICONS["rocket"]}</span>
                        <span class="track-name" id="i18n-track-3">KAPI 3: Yetenek Pasaportu (Tech)</span>
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
        <div class="ccift-highlight-box">
            <div class="ccift-header">
                <div class="ccift-badge-title" id="i18n-ccift-box-title">{SVG_ICONS["shield_check"]} CCIFT & DEİK RESMİ İKİLİ TİCARET ÜYELERİ (EN YÜKSEK VİZE ONAYI)</div>
                <button class="ccift-quick-btn" onclick="window.TrackerEngine.Filter.toggleCcift(); document.getElementById('filter-btn-ccift').classList.toggle('active');" id="i18n-ccift-quick-btn">
                    {SVG_ICONS["shield_check"]} Bu Üyelerin İlanlarını Filtrele (1-Tık)
                </button>
            </div>
            <p class="ccift-text" id="i18n-ccift-box-text">
                Aşağıda altın rozetle işaretlenen şirketler, <strong>Fransız-Türk Ticaret Odası (CCIFT)</strong> ve <strong>DEİK Türkiye-Fransa İş Konseyi</strong>'nin resmi üye holdingleridir (<em>Beko France, Turkish Airlines, Ekol, Barsan, Şişecam, Vestel, Sabancı, Eczacıbaşı vb.</em>). Bu kurumlar, Fransa ile resmi ikili protokol ve anlaşmalara sahip olup, Türkiye'den personel transferinde <strong>Şirket İçi Transfer (ICT)</strong> ve <strong>Yetenek Pasaportu (Passeport Talent)</strong> vizelerinde en yüksek onay oranına ve en hızlı prosedürlere sahiptir.
            </p>
        </div>

        <!-- ENCART CONSEILS & LANGUES -->
        <div class="bilateral-box">
            <h4 id="i18n-advice-title">{SVG_ICONS["check_circle"]} Türkiye'deki Adaylar İçin Vize ve Dil Rehberi:</h4>
            <p id="i18n-advice-text">
                <strong>Fransızca bilmiyorsanız endişelenmeyin :</strong> Yeşil etiketli ilanlarda çalışma dili <strong>İngilizce veya Türkçe</strong>dir (Fransızca şart değildir veya temel A1 yeterlidir). Türkiye'den vizesiz başvuru yaparken en güçlü kapılar : <strong>1)</strong> Yukarıdaki <strong>CCIFT & DEİK üyesi holdingler</strong> (Şirket İçi Transfer ICT vizesi). <strong>2)</strong> Türkiye'nin üyesi olduğu uluslararası kuruluşlar (<em>Avrupa Konseyi, OECD, UNESCO</em> - özel diplomatik/uluslararası memur statüsü verilir). <strong>3)</strong> Paris merkezli scale-up'lar (%100 İngilizce Tech kadroları).
            </p>
        </div>

        <!-- BARRE DE RECHERCHE ET FILTRES MULTI-FACETTES -->
        <div class="filter-panel">
            <div class="search-bar-row">
                <input type="text" id="searchInput" class="search-input" placeholder="Pozisyon, şehir (Paris, Lyon, Strazburg...), kurum (OECD, Beko, THY, Ekol...) ara...">
            </div>
            
            <div class="filter-facets-row">
                <button class="filter-pill-btn active" data-filter-val="all" onclick="window.TrackerEngine.Filter.setCategory('all'); document.querySelectorAll('.filter-pill-btn[data-filter-val]').forEach(b=>b.classList.remove('active')); this.classList.add('active');">Tümü</button>
                <button class="filter-pill-btn pill-ccift" id="filter-btn-ccift" onclick="window.TrackerEngine.Filter.toggleCcift(); this.classList.toggle('active');">
                    {SVG_ICONS["shield_check"]} CCIFT & DEİK Üyeleri
                </button>
                <button class="filter-pill-btn pill-no-french" id="filter-btn-no-french" onclick="window.TrackerEngine.Filter.toggleNoFrench(); this.classList.toggle('active');">
                    {SVG_ICONS["check_circle"]} Fransızca Şart Değil
                </button>
                <button class="filter-pill-btn" data-filter-val="institutions" onclick="window.TrackerEngine.Filter.setCategory('institutions'); document.querySelectorAll('.filter-pill-btn[data-filter-val]').forEach(b=>b.classList.remove('active')); this.classList.add('active');">
                    {SVG_ICONS["landmark"]} Uluslararası Kurumlar
                </button>
                <button class="filter-pill-btn" data-filter-val="companies" onclick="window.TrackerEngine.Filter.setCategory('companies'); document.querySelectorAll('.filter-pill-btn[data-filter-val]').forEach(b=>b.classList.remove('active')); this.classList.add('active');">
                    {SVG_ICONS["building"]} Türk Holdingleri
                </button>
                <button class="filter-pill-btn" data-filter-val="logistics" onclick="window.TrackerEngine.Filter.setCategory('logistics'); document.querySelectorAll('.filter-pill-btn[data-filter-val]').forEach(b=>b.classList.remove('active')); this.classList.add('active');">
                    {SVG_ICONS["plane"]} Lojistik & Ticaret
                </button>
                <button class="filter-pill-btn" data-filter-val="tech" onclick="window.TrackerEngine.Filter.setCategory('tech'); document.querySelectorAll('.filter-pill-btn[data-filter-val]').forEach(b=>b.classList.remove('active')); this.classList.add('active');">
                    {SVG_ICONS["rocket"]} Tech & Scale-ups
                </button>
                <button class="filter-pill-btn" data-filter-val="pme" onclick="window.TrackerEngine.Filter.setCategory('pme'); document.querySelectorAll('.filter-pill-btn[data-filter-val]').forEach(b=>b.classList.remove('active')); this.classList.add('active');">
                    {SVG_ICONS["briefcase"]} KOBİ & Saha
                </button>
                
                <span style="color: var(--border-default); font-size: 1.2rem;">|</span>
                
                <button class="filter-pill-btn pill-fav" onclick="const isFav = this.classList.toggle('active'); window.TrackerEngine.Filter.setStatusFilter(isFav ? 'fav' : 'all');">
                    {SVG_ICONS["bookmark"]} Sadece Favoriler
                </button>
                <button class="filter-pill-btn pill-tracked" onclick="const isTracked = this.classList.toggle('active'); window.TrackerEngine.Filter.setStatusFilter(isTracked ? 'tracked' : 'all');">
                    {SVG_ICONS["file_text"]} Takip Edilenler
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
            <p style="font-size: 1.1rem; color: var(--text-tertiary); margin-bottom: 14px;">Aradığınız kriterlere uygun fırsat bulunamadı.</p>
            <button class="apply-btn" style="max-width: 220px; margin: 0 auto;" onclick="window.TrackerEngine.Filter.resetAll()">Filtreleri Temizle 🔄</button>
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
                <div class="t-lbl">Toplam Takipte</div>
            </div>
            <div class="tracker-stat-box box-applied">
                <div class="t-num" id="tracker-stat-applied">0</div>
                <div class="t-lbl">Başvuruldu / Süreçte</div>
            </div>
            <div class="tracker-stat-box box-interview">
                <div class="t-num" id="tracker-stat-interview">0</div>
                <div class="t-lbl">Mülakat Planlandı</div>
            </div>
            <div class="tracker-stat-box box-offer">
                <div class="t-num" id="tracker-stat-offer">0</div>
                <div class="t-lbl">Kabul / Teklif</div>
            </div>
        </div>

        <!-- TOOLBAR DU TRACKER -->
        <div class="tracker-toolbar">
            <input type="text" id="trackerSearchInput" class="tracker-search-input" placeholder="Takip edilen başvurularda ara...">
            <div class="tracker-actions-group">
                <button class="btn-action-tracker btn-export-csv" id="btn-export-csv" onclick="window.TrackerEngine.exportCSV()">CSV Dışa Aktar (Superviseur FR)</button>
                <button class="btn-action-tracker btn-export-json" id="btn-export-json" onclick="window.TrackerEngine.exportJSON()">JSON Dışa Aktar</button>
                <button class="btn-action-tracker btn-clear-tracker" id="btn-clear-tracker" onclick="window.TrackerEngine.clearAllApplications()">Listeyi Temizle</button>
            </div>
        </div>

        <div id="tracker-empty-notice" class="tracker-empty-board" style="display: none;">
            <h3>Henüz takibe alınmış bir başvuru yok</h3>
            <p>İlanlar sekmesinde ilgilendiğiniz ilanların altındaki <strong>'Takip Et'</strong> butonuna tıklayarak veya kartı favorilere ekleyerek takip sürecinizi başlatabilirsiniz.</p>
            <button class="apply-btn" style="max-width: 240px; margin: 0 auto;" onclick="window.TrackerEngine.switchTab('explore')">İlanları Keşfetmeye Başla</button>
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
                <h2>Fransa İstihdam, Vize & Başvuru Rehberi</h2>
                <p>Türkiye'den Fransa'ya transfer süreçleri, vize prosedürleri ve hazır başvuru şablonları.</p>
            </div>

            <!-- SECTION A : LES 4 VOIES LÉGALES DE VISA -->
            <div class="guide-card-section">
                <div class="guide-section-header">
                    <h3>{SVG_ICONS["plane"]} 1. Türkiye'den Fransa'ya 4 Yasal İstihdam ve Vize Yolu</h3>
                    <p>Klasik çalışma izni engeline takılmadan Fransa'ya geçiş sağlayan öncelikli statüler.</p>
                </div>
                <div class="guide-grid-2">
                    <div class="visa-method-card">
                        <span class="method-tag">Şirket İçi Transfer (ICT)</span>
                        <h4>{SVG_ICONS["shield_check"]} 1. Salarié Détaché ICT (CCIFT & DEİK Üyeleri)</h4>
                        <p>Beko, THY, Ekol, Barsan, Şişecam gibi holdinglerin Türkiye merkezinde en az 3-6 ay çalışan uzman veya yöneticilerin Fransa şubelerine tayin edilmesi. <strong>Yerel işgücü piyasası araştırması (opposabilité de l'emploi) ve dil sınavı aranmaz!</strong> En hızlı vize yoludur.</p>
                    </div>
                    <div class="visa-method-card">
                        <span class="method-tag">Passeport Talent</span>
                        <h4>{SVG_ICONS["rocket"]} 2. Yetenek Pasaportu (Passeport Talent - Salarié Qualifié)</h4>
                        <p>Fransa'daki teknoloji scale-up'ları (Mistral AI, Datadog, Qonto) ve yenilikçi şirketler tarafından verilir. Yüksek lisans veya brüt asgari ücretin en az 2 katı (yaklaşık 43.000 €/yıl) maaş teklifi durumunda eş ve çocuklara da doğrudan tam çalışma hakkı sağlar.</p>
                    </div>
                    <div class="visa-method-card">
                        <span class="method-tag">Özel MEAE Diplomatik Statüsü</span>
                        <h4>{SVG_ICONS["landmark"]} 3. Uluslararası & Avrupa Kuruluşları (OECD, CoE, UNESCO)</h4>
                        <p>Türkiye'nin kurucu veya tam üye olduğu kurumlarda istihdam. Standart Fransa çalışma vizesi aranmaz; Dışişleri Bakanlığı (MEAE) tarafından doğrudan özel uluslararası diplomatik oturum kartı verilir. Taşınma masrafları kurumca karşılanır.</p>
                    </div>
                    <div class="visa-method-card">
                        <span class="method-tag">Klasik Çalışma İzni</span>
                        <h4>{SVG_ICONS["file_text"]} 4. Salarié de Droit Commun & Métiers en Tension</h4>
                        <p>Fransa'da personel açığı bulunan sektörlerde (bilişim, lojistik, inşaat, mühendislik) Fransız işverenin İçişleri Bakanlığı yabancı işçi portalından (ANEF) çalışma izni almasıyla verilen oturum türü.</p>
                    </div>
                </div>
            </div>

            <!-- SECTION B : CHECKLIST INTERACTIVE -->
            <div class="guide-card-section">
                <div class="guide-section-header">
                    <h3>{SVG_ICONS["check_circle"]} 2. Başvuru Öncesi İnteraktif Aday Kontrol Listesi (Checklist)</h3>
                    <p>İlerlemenizi işaretleyin; durumunuz otomatik olarak tarayıcınızda saklanır.</p>
                </div>
                <div class="checklist-items-box">
                    <label class="checklist-item" for="chk-passport">
                        <input type="checkbox" id="chk-passport" class="guide-checkbox">
                        <span class="checklist-label">Pasaport Geçerlilik Süresi: Planlanan seyahat tarihinden itibaren en az 12 ay geçerli bordo/yeşil pasaport.</span>
                    </label>
                    <label class="checklist-item" for="chk-cv">
                        <input type="checkbox" id="chk-cv" class="guide-checkbox">
                        <span class="checklist-label">Avrupa Standartlarında CV (Europass / ATS Uyumlu): Fotoğrafsız veya nötr fotoğraflı, İngilizce veya Fransızca 1-2 sayfalık özgeçmiş.</span>
                    </label>
                    <label class="checklist-item" for="chk-diploma">
                        <input type="checkbox" id="chk-diploma" class="guide-checkbox">
                        <span class="checklist-label">Diploma & Transkript Çevirileri: Yeminli tercüman onaylı, tercihen apostilli lisans/yüksek lisans belgeleri.</span>
                    </label>
                    <label class="checklist-item" for="chk-linkedin">
                        <input type="checkbox" id="chk-linkedin" class="guide-checkbox">
                        <span class="checklist-label">LinkedIn Profilinin Güncellenmesi: Profil dilinin İngilizce ve/veya Fransızca yapılması, 'Open to Work' konumunun Fransa olarak işaretlenmesi.</span>
                    </label>
                    <label class="checklist-item" for="chk-adli-sicil">
                        <input type="checkbox" id="chk-adli-sicil" class="guide-checkbox">
                        <span class="checklist-label">Adli Sicil Kaydı (e-Devlet): Fransızca veya İngilizce barkodlu adli sicil belgesi.</span>
                    </label>
                </div>
            </div>

            <!-- SECTION C : TEMPLATES D'EMAIL BILINGUES -->
            <div class="guide-card-section">
                <div class="guide-section-header">
                    <h3>{SVG_ICONS["file_text"]} 3. Hazır E-posta & Motivasyon Mektubu Şablonları (1-Tık Kopyala)</h3>
                    <p>Fransa'daki Türk yöneticilere veya uluslararası İK temsilcilerine doğrudan gönderebileceğiniz taslaklar.</p>
                </div>

                <!-- ŞABLON 1 : TÜRK HOLDİNGİ FRANSA ŞUBESİ (ICT) -->
                <div class="template-block">
                    <div class="template-top">
                        <span class="template-title">Şablon 1 : Türk Holdingi Fransa Şubesi Direktörüne Doğrudan Başvuru</span>
                        <button class="copy-template-btn" onclick="window.TrackerEngine.copyTemplate('tmpl-1', this)">
                            {SVG_ICONS["copy"]} Metni Kopyala
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
                        <span class="template-title">Şablon 2 : Paris Tech & Scale-up Başvurusu (%100 İngilizce - Passeport Talent)</span>
                        <button class="copy-template-btn" onclick="window.TrackerEngine.copyTemplate('tmpl-2', this)">
                            {SVG_ICONS["copy"]} Metni Kopyala
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
                    <h3>{SVG_ICONS["globe"]} 4. Resmi Vize ve İkili Kurum Portalları</h3>
                    <p>Doğrudan mevzuat ve başvuru takibi yapabileceğiniz yetkili platformlar.</p>
                </div>
                <div class="guide-grid-2">
                    <div class="visa-method-card">
                        <h4>{SVG_ICONS["external_link"]} France-Visas (Resmi Portal)</h4>
                        <p>Fransa vize türlerinin şartları, evrak listeleri ve resmi başvuru kılavuzu: <br><a href="https://france-visas.gouv.fr/" target="_blank" rel="noopener noreferrer" style="color: var(--accent-primary); font-weight: 700;">france-visas.gouv.fr ↗</a></p>
                    </div>
                    <div class="visa-method-card">
                        <h4>{SVG_ICONS["external_link"]} ANEF (Yabancılar Dijital Portalı)</h4>
                        <p>Fransız İçişleri Bakanlığı çalışma izni ve Yetenek Pasaportu online işlem platformu: <br><a href="https://administration-etrangers-en-france.interieur.gouv.fr/" target="_blank" rel="noopener noreferrer" style="color: var(--accent-primary); font-weight: 700;">administration-etrangers-en-france.interieur.gouv.fr ↗</a></p>
                    </div>
                    <div class="visa-method-card">
                        <h4>{SVG_ICONS["shield_check"]} CCIFT (Fransız-Türk Ticaret Odası)</h4>
                        <p>İkili ticaret ağı, üye şirketler ve istihdam rehberi: <br><a href="https://www.ccift.com/" target="_blank" rel="noopener noreferrer" style="color: var(--accent-primary); font-weight: 700;">ccift.com ↗</a></p>
                    </div>
                    <div class="visa-method-card">
                        <h4>{SVG_ICONS["shield_check"]} DEİK Türkiye-Fransa İş Konseyi</h4>
                        <p>Dış Ekonomik İlişkiler Kurulu Türkiye-Fransa ikili iş konseyi portali: <br><a href="https://www.deik.org.tr/" target="_blank" rel="noopener noreferrer" style="color: var(--accent-primary); font-weight: 700;">deik.org.tr ↗</a></p>
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
                <h3 id="i18n-modal-title">Başvuru Takip Detayları</h3>
                <button type="button" class="modal-close-btn" id="modal-close-btn">&times;</button>
            </div>
            
            <form id="tracker-form">
                <input type="hidden" id="modal-job-id" value="">

                <div class="modal-job-info">
                    <div class="modal-job-company" id="modal-card-company">Şirket</div>
                    <div class="modal-job-title" id="modal-card-title">Pozisyon</div>
                </div>

                <div class="form-group">
                    <label class="form-label" for="modal-status">Aşama / Durum (Pipeline):</label>
                    <select id="modal-status" class="form-control">
                        <option value="saved">Kaydedildi / Hedef (Enregistré)</option>
                        <option value="applied">Başvuruldu (Postulé)</option>
                        <option value="interview">Mülakat Aşamasında (Entretien)</option>
                        <option value="offer">Kabul / Teklif Alındı (Offre Reçue)</option>
                    </select>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <div class="form-group">
                        <label class="form-label" for="modal-applied-date">Başvuru Tarihi:</label>
                        <input type="date" id="modal-applied-date" class="form-control">
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="modal-interview-date">Mülakat Tarihi:</label>
                        <input type="date" id="modal-interview-date" class="form-control">
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label" for="modal-notes">Kişisel Notlar &amp; Takip Bilgileri:</label>
                    <textarea id="modal-notes" class="form-control" placeholder="Örn: LinkedIn'den İK müdürüne yazıldı, Europass İngilizce CV gönderildi, 2 hafta içinde geri dönüş bekleniyor..."></textarea>
                </div>

                <div class="modal-footer">
                    <button type="button" class="modal-btn modal-btn-delete" id="modal-delete-btn" style="display: none;">Takibi Bırak</button>
                    <div style="display: flex; gap: 8px;">
                        <button type="button" class="modal-btn modal-btn-cancel" id="modal-cancel-btn">İptal</button>
                        <button type="submit" class="modal-btn modal-btn-save">Kaydet</button>
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
