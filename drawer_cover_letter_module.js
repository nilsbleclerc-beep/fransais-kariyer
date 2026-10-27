/**
 * ==============================================================================
 * BILATERAL FRANCE-TURKEY : DRAWER D'OPPORTUNITÉ & GÉNÉRATEUR INTELLIGENT DE LETTRE
 * ------------------------------------------------------------------------------
 * Module Vanilla JS ES6+ autonome et prêt à être fusionné dans dashboard.html
 * 
 * Fonctionnalités clés :
 * 1. Écran Détail de l'offre (plein écran mobile, panneau latéral desktop)
 *    - Données : window.FransaData.get(id) ; favoris / suivi via window.TrackerEngine
 *    - App bar (retour, titre au scroll, menu Partager / Site officiel / Suivre)
 *    - « Bu ilan bana uygun mu? », feuille de route visa en frise, description, contact RH
 *    - Barre d'action fixe : favori + « Ön yazı hazırla »
 * 2. Générateur Intelligent de Pitch & Lettre de Motivation (TR ➔ FR)
 *    - Email court de premier contact (LinkedIn InMail / Email direct)
 *    - Lettre de motivation formelle en français soutenu
 *    - Paragraphe d'introduction rappelant explicitement la voie juridique
 *    - Copie en 1-clic avec Toast et téléchargement .txt
 * 3. Guide bilingue pratique de l'expatriation (3 voies prioritaires + voie standard & conversion CV turc)
 * 4. Contrat d'historique partagé (bouton retour Android) : ids 'drawer', 'letter', 'guide'
 * ==============================================================================
 */

(function (window, document) {
    'use strict';

    // --------------------------------------------------------------------------
    // 1. ANNUAIRE RH BILATÉRAL & ENRICHISSEMENT DES ENTREPRISES
    // --------------------------------------------------------------------------
    const BILATERAL_COMPANIES_REGISTRY = {
        "beko": { hr_email: "recrutement@beko.fr", ats: "https://www.bekoeurope.com/careers", portal: "https://www.kockariyerim.com", voie: "voie_2" },
        "turkish airlines": { hr_email: "cdghr@thy.com", ats: "https://careers.turkishairlines.com", portal: "https://careers.turkishairlines.com/", voie: "voie_2" },
        "thy": { hr_email: "cdghr@thy.com", ats: "https://careers.turkishairlines.com", portal: "https://careers.turkishairlines.com/", voie: "voie_2" },
        "trendyol": { hr_email: "talent@trendyol.com", ats: "https://jobs.lever.co/trendyol", portal: "https://jobs.lever.co/trendyol", voie: "voie_2" },
        "barsan": { hr_email: "info@barsan.com", ats: "https://www.barsan.com", portal: "https://www.barsan.com", voie: "voie_2" },
        "ekol": { hr_email: "france@ekol.com", ats: "https://jobs.dfds.com/", portal: "https://www.ekol.com/en/career/job-applications/", voie: "voie_2" },
        "şişecam": { hr_email: "kariyer@sisecam.com", ats: "https://jobs.sisecam.com", portal: "https://jobs.sisecam.com", voie: "voie_2" },
        "sisecam": { hr_email: "kariyer@sisecam.com", ats: "https://jobs.sisecam.com", portal: "https://jobs.sisecam.com", voie: "voie_2" },
        "vestel": { hr_email: "info@vestel.fr", ats: "https://www.vestelkariyer.com", portal: "https://www.zorlukariyer.com", voie: "voie_2" },
        "eczacıbaşı": { hr_email: "kariyer@eczacibasi.com.tr", ats: "https://burgbad.fr", portal: "https://eczacibasikariyer.com.tr", voie: "voie_2" },
        "vitra": { hr_email: "kariyer@eczacibasi.com.tr", ats: "https://burgbad.fr", portal: "https://eczacibasikariyer.com.tr", voie: "voie_2" },
        "çimsa": { hr_email: "ik@sabanci.com", ats: "https://cimsakariyerim.com", portal: "https://kariyer.sabanci.com", voie: "voie_2" },
        "kordsa": { hr_email: "ik@sabanci.com", ats: "https://cimsakariyerim.com", portal: "https://kariyer.sabanci.com", voie: "voie_2" },
        "horoz": { hr_email: "ik@horoz.com.tr", ats: "https://www.bleckmann.com/careers/", portal: "https://www.horoz.com.tr/is-basvurusu", voie: "voie_2" },
        "bbl": { hr_email: "recrutement@groupe-bbl.com", ats: "https://www.groupe-bbl.com/carrieres/", portal: "https://www.groupe-bbl.com/carrieres/", voie: "voie_2" },
        "oecd": { hr_email: "oecdrecruitment@oecd.org", ats: "https://careers.smartrecruiters.com/OECD", portal: "https://www.oecd.org/en/about/careers.html", voie: "voie_1" },
        "ocde": { hr_email: "oecdrecruitment@oecd.org", ats: "https://careers.smartrecruiters.com/OECD", portal: "https://www.oecd.org/en/about/careers.html", voie: "voie_1" },
        "unesco": { hr_email: "staffing-team@unesco.org", ats: "https://careers.unesco.org/", portal: "https://careers.unesco.org/", voie: "voie_1" },
        "conseil de l'europe": { hr_email: "recruitment@coe.int", ats: "https://www.coe-recruitment.com", portal: "https://www.coe.int/en/web/jobs", voie: "voie_1" },
        "coe": { hr_email: "recruitment@coe.int", ats: "https://www.coe-recruitment.com", portal: "https://www.coe.int/en/web/jobs", voie: "voie_1" },
        "interpol": { hr_email: "recruitment@interpol.int", ats: "https://recruitment.interpol.int/", portal: "https://recruitment.interpol.int/", voie: "voie_1" },
        "circ": { hr_email: "personnel@iarc.who.int", ats: "https://careers.who.int/", portal: "https://www.iarc.who.int/about-iarc-jobs/", voie: "voie_1" },
        "iarc": { hr_email: "personnel@iarc.who.int", ats: "https://careers.who.int/", portal: "https://www.iarc.who.int/about-iarc-jobs/", voie: "voie_1" },
        "euronews": { hr_email: "recruitment@euronews.com", ats: "https://join.com/companies/euronews", portal: "https://www.euronews.com/about/careers", voie: "voie_1" },
        "inalco": { hr_email: "recrutement@inalco.fr", ats: "https://www.inalco.fr/recrutement", portal: "https://www.galaxie.enseignementsup-recherche.gouv.fr/ensup/candidats.html", voie: "voie_1" },
        "mistral": { hr_email: "jobs@mistral.ai", ats: "https://jobs.lever.co/mistral", portal: "https://mistral.ai/careers", voie: "voie_3" },
        "qonto": { hr_email: "talent@qonto.com", ats: "https://boards.greenhouse.io/qonto", portal: "https://qonto.com/en/careers", voie: "voie_3" },
        "datadog": { hr_email: "recruiting@datadoghq.com", ats: "https://careers.datadoghq.com/", portal: "https://careers.datadoghq.com/", voie: "voie_3" },
        "criteo": { hr_email: "talent-acquisition@criteo.com", ats: "https://careers.criteo.com/", portal: "https://careers.criteo.com/", voie: "voie_3" },
        "amo": { hr_email: "jobs@amo.co", ats: "https://www.welcometothejungle.com/fr/companies/amo", portal: "https://www.welcometothejungle.com/fr/companies/amo", voie: "voie_3" },
        "aftcom": { hr_email: "jobs@aftcom.com", ats: "https://aftcom.com/recrutement/", portal: "https://aftcom.com/recrutement/", voie: "voie_2" }
    };

    // --------------------------------------------------------------------------
    // 2. ÉCUSSONS OFFICIELS DES VOIES PRIORITAIRES
    // --------------------------------------------------------------------------
    const VOIE_ECUSSONS = {
        "voie_1": {
            title_tr: "🏛️ KAPI 1 ÖNCELİKLİ : ULUSLARARASI STATÜ (MAE)",
            title_fr: "🏛️ VOIE 1 PRIORITAIRE : STATUT INTERNATIONAL MAE",
            sub_tr: "Klasik çalışma izni aranmaz • Fransa Dışişleri Protokolü (Titre Spécial MEAE) • Kurucu Üyelik",
            sub_fr: "Dispense totale d'autorisation de travail • Titre spécial protocole MEAE • Accord de siège",
            cssClass: "ecusson-voie-1",
            color: "#1e40af",
            bg: "#eff6ff"
        },
        "voie_2": {
            title_tr: "🤝 KAPI 2 ÖNCELİKLİ : ŞİRKET İÇİ TRANSFER ICT (CCIFT & DEİK)",
            title_fr: "🤝 VOIE 2 PRIORITAIRE : SALARIÉ DÉTACHÉ ICT (CCIFT & DEİK)",
            sub_tr: "Şirket İçi Transfer (ICT) • 1972 İkili Sosyal Güvenlik Anlaşması • İşgücü Testinden Muaf",
            sub_fr: "Mobilité intra-groupe (CESEDA L. 421-26) • Accord bilatéral 1972 • Exonération opposabilité emploi",
            cssClass: "ecusson-voie-2",
            color: "#92400e",
            bg: "#fef3c7"
        },
        "voie_3": {
            title_tr: "⚡ KAPI 3 ÖNCELİKLİ : PASSEPORT TALENT (FRENCH TECH)",
            title_fr: "⚡ VOIE 3 PRIORITAIRE : PASSEPORT TALENT (FRENCH TECH)",
            sub_tr: "%100 İngilizce • Yenilikçi Şirket (JEI) • 4 Yıllık Oturum • Eşe Tam Çalışma İzni",
            sub_fr: "Entreprise innovante (CESEDA L. 421-9) • Titre pluriannuel 4 ans • 100% Anglais • Conjoint autorisé",
            cssClass: "ecusson-voie-3",
            color: "#6d28d9",
            bg: "#f5f3ff"
        },
        "autre": {
            title_tr: "🏢 STANDART YOL : ÇALIŞMA VİZESİ (VLS-TS)",
            title_fr: "🏢 VOIE STANDARD : VISA DE TRAVAIL SALARIÉ (VLS-TS)",
            sub_tr: "Fransız İş Kanunu Genel Hükümleri • ANEF Çalışma İzni Onayı",
            sub_fr: "Droit commun • Autorisation de travail dématérialisée ANEF",
            cssClass: "ecusson-voie-4",
            color: "#334155",
            bg: "#f1f5f9"
        }
    };

    // --------------------------------------------------------------------------
    // 3. ÉTAT LOCAL DU MODULE
    // --------------------------------------------------------------------------
    function readStoredLang() {
        try {
            return (typeof localStorage !== 'undefined' && localStorage.getItem('bilateral_lang')) || "tr";
        } catch (e) {
            return "tr";
        }
    }

    const State = {
        currentJob: null,
        currentTrack: "voie_2",
        generatorTab: "email", // 'email' | 'letter'
        lang: readStoredLang(),
        lastSubject: ""
    };

    // Libellés d'interface (la lettre générée, elle, reste toujours en français)
    const UI_TEXT = {
        tr: {
            score: "Uygunluk: %",
            noFrench: "✅ Fransızca Şart Değil",
            frenchReq: "🗣️ Fransızca B2+ Gerekli",
            targetJob: "Hedef İlan",
            generalApplication: "Genel Başvuru",
            genEcussonSub: "Mektubun 1. paragrafı bu yasal yolu işverene açıkça hatırlatır.",
            copyLabel: "Kopyala",
            copied: "✓ Kopyalandı",
            toastCopied: "✓ Metin panoya kopyalandı !",
            toastCopyFail: "⚠️ Kopyalama başarısız. Metni elle seçip kopyalayın.",
            toastEmailCopied: "✓ İK e-posta adresi kopyalandı : ",
            toastDownloaded: "✓ Dosya indirildi : ",
            toastShareFallback: "Paylaşım bu cihazda desteklenmiyor, metin panoya kopyalandı.",
            shareTitleEmail: "Aday e-postası",
            shareTitleLetter: "Ön yazı (Lettre de motivation)"
        },
        fr: {
            score: "Score : %",
            noFrench: "✅ Français Non Requis",
            frenchReq: "🗣️ Français B2+ Requis",
            targetJob: "Offre ciblée",
            generalApplication: "Candidature spontanée",
            genEcussonSub: "Le 1er paragraphe de la lettre rappelle expressément cette voie juridique au recruteur.",
            copyLabel: "Copier",
            copied: "✓ Copié !",
            toastCopied: "✓ Texte copié dans le presse-papiers !",
            toastCopyFail: "⚠️ Copie impossible. Sélectionnez le texte manuellement.",
            toastEmailCopied: "✓ Email RH copié : ",
            toastDownloaded: "✓ Fichier téléchargé : ",
            toastShareFallback: "Partage non disponible sur cet appareil, texte copié.",
            shareTitleEmail: "Email de candidature",
            shareTitleLetter: "Lettre de motivation"
        }
    };

    function t(key) {
        const dict = UI_TEXT[State.lang] || UI_TEXT.tr;
        return dict[key] !== undefined ? dict[key] : (UI_TEXT.tr[key] || key);
    }

    // --------------------------------------------------------------------------
    // 3b. CONTRAT D'HISTORIQUE PARTAGÉ (bouton retour Android / geste retour)
    // --------------------------------------------------------------------------
    // Ouverture : history.pushState({ fransaOverlay: '<id>' }, '')
    // Fermeture UI : si history.state.fransaOverlay === '<id>' -> history.back()
    //                (la fermeture effective se fait dans le handler popstate),
    //                sinon fermeture directe.
    // Popstate : si l'overlay <id> est ouvert et que event.state.fransaOverlay !== '<id>'
    //            -> fermeture SANS toucher à l'historique.
    const OverlayHistory = {
        pendingBack: false,
        pendingTimer: null,

        push(id) {
            try {
                if (!(history.state && history.state.fransaOverlay === id)) {
                    history.pushState({ fransaOverlay: id }, '');
                }
            } catch (e) {
                // Environnement sans History API (iframe sandbox, file://…) : ignoré
            }
        },

        requestClose(id, hideFn) {
            let ownsState = false;
            try {
                ownsState = !!(history.state && history.state.fransaOverlay === id);
            } catch (e) {
                ownsState = false;
            }
            if (!ownsState) {
                hideFn();
                return;
            }
            // Anti double-tap : un seul history.back() en vol à la fois
            if (this.pendingBack) return;
            this.pendingBack = true;
            clearTimeout(this.pendingTimer);
            this.pendingTimer = setTimeout(() => { this.pendingBack = false; }, 800);
            history.back();
        },

        settle() {
            this.pendingBack = false;
            clearTimeout(this.pendingTimer);
        }
    };

    // --------------------------------------------------------------------------
    // 3c. VERROUILLAGE DU SCROLL DE LA PAGE & FOCUS
    // --------------------------------------------------------------------------
    function isOverlayOpen(elementId) {
        const el = document.getElementById(elementId);
        return !!(el && el.classList.contains('open'));
    }

    function syncScrollLock() {
        const anyOpen = isOverlayOpen('bld-drawer') || isOverlayOpen('bld-gen-modal-overlay') || isOverlayOpen('bld-guide-modal-overlay');
        document.documentElement.classList.toggle('bld-scroll-lock', anyOpen);
    }

    const focusMemory = {};
    function rememberFocus(id, focusTarget) {
        focusMemory[id] = document.activeElement;
        if (focusTarget && typeof focusTarget.focus === 'function') {
            setTimeout(() => {
                try { focusTarget.focus({ preventScroll: true }); } catch (e) { /* noop */ }
            }, 60);
        }
    }
    function restoreFocus(id) {
        const el = focusMemory[id];
        focusMemory[id] = null;
        if (el && document.contains(el) && typeof el.focus === 'function') {
            try { el.focus({ preventScroll: true }); } catch (e) { /* noop */ }
        }
    }

    // --------------------------------------------------------------------------
    // 3d. PRESSE-PAPIERS (API moderne + fallback execCommand)
    // --------------------------------------------------------------------------
    function legacyCopy(text) {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.setAttribute('readonly', '');
        ta.style.position = 'fixed';
        ta.style.top = '-1000px';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        let ok = false;
        try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
        document.body.removeChild(ta);
        return ok;
    }

    function copyText(text) {
        if (navigator.clipboard && window.isSecureContext !== false) {
            return navigator.clipboard.writeText(text).then(() => true).catch(() => legacyCopy(text));
        }
        return Promise.resolve(legacyCopy(text));
    }

    function detectTrackForJob(company, title, tags, isCcift) {
        const str = `${company} ${title} ${tags}`.toLowerCase();
        for (const [key, reg] of Object.entries(BILATERAL_COMPANIES_REGISTRY)) {
            if (str.includes(key)) return reg.voie;
        }
        if (anyMatch(str, ["oecd", "ocde", "unesco", "conseil de l'europe", "coe", "cedh", "aihm", "interpol", "circ", "iarc", "who", "oms", "inalco", "euronews", "kurum", "institution"])) {
            return "voie_1";
        }
        if (isCcift || anyMatch(str, ["holding", "ccift", "deik", "dei̇k", "ict", "salarié détaché", "beko", "thy", "ekol", "barsan", "şişecam", "sisecam", "vestel", "eczacıbaşı", "sabancı"])) {
            return "voie_2";
        }
        if (anyMatch(str, ["tech", "scaleup", "scale-up", "yapay zeka", "intelligence artificielle", "fintech", "passeport talent", "mistral", "datadog", "qonto", "criteo", "amo"])) {
            return "voie_3";
        }
        return "autre";
    }

    function anyMatch(text, keywords) {
        return keywords.some(k => text.includes(k));
    }

    function getRegistryInfo(company) {
        const cLower = company.toLowerCase();
        for (const [key, val] of Object.entries(BILATERAL_COMPANIES_REGISTRY)) {
            if (cLower.includes(key)) return val;
        }
        return null;
    }

    // --------------------------------------------------------------------------
    // 4. ÉCRAN DÉTAIL DE L'OFFRE
    //    ≤768px : écran plein (app bar 56px, contenu, barre d'action fixe en bas)
    //    >768px : panneau latéral droit
    //    Données : window.FransaData.get(id) (plus aucune lecture de .job-card)
    // --------------------------------------------------------------------------

    // Feuille de route visa Turquie -> France : 4 étapes [titre, description] par voie et par langue
    const VISA_STEPS = {
        voie_1: {
            tr: [
                ["Resmi Görevlendirme Mektubu (Nomination Officielle)", "Avrupa Konseyi, OECD, UNESCO veya INTERPOL Genel Sekreterliği'nden atama bildirimi iletilir. Türkiye'nin tam üyelik kotası devreye girer."],
                ["Dışişleri Bakanlığı (MEAE) Protokol Talimatı", "Kurumun Ayrıcalıklar Dairesi Fransa Dışişleri Bakanlığı Protokol Şefliği'ne resmi bildirimde bulunarak Türkiye'deki Fransız Konsolosluğu'na talimat gönderir."],
                ["Konsolosluktan Öncelikli Protokol Vizesi", "Ankara Büyükelçiliği veya İstanbul Başkonsolosluğu'ndan harçsız diplomatik/protokol vizesi düzenlenir. Klasik çalışma izni aranmaz."],
                ["MEAE Özel Diplomatik Oturma Kartı (Titre Spécial)", "Fransa'ya varışta doğrudan Dışişleri Bakanlığı Protokol Şefliği'nden \"Titre de Séjour Spécial\" teslim alınır. Gelir vergisi muafiyeti ve taşınma paketi sağlanır."]
            ],
            fr: [
                ["Nomination & Engagement Officiel", "Notification d'engagement délivrée par l'Organisation (Conseil de l'Europe, OCDE, UNESCO). Le quota de la Turquie (membre fondateur) s'applique."],
                ["Note Verbale & Instruction MEAE", "Le département juridique notifie le Protocole du Ministère des Affaires Étrangères (MEAE) pour instruction prioritaire auprès des Consulats en Turquie."],
                ["Visa Protocolaire Gratuit (72h - 5 jours)", "Le Consulat Général de France à Istanbul ou l'Ambassade à Ankara délivre le visa de courtoisie sans frais et sans démarche de droit commun."],
                ["Titre Spécial MEAE & Installation", "Délivrance directe du Titre de Séjour Spécial à l'arrivée. Traitement net d'impôt, indemnités d'expatriation et déménagement pris en charge à 100%."]
            ]
        },
        voie_2: {
            tr: [
                ["Şirket İçi Görevlendirme Protokolü (Avenant ICT)", "Türkiye genel merkezi ile Fransa'daki tüzel kişilik arasında şirket içi transfer sözleşmesi düzenlenir. (Grup bünyesinde en az 3-6 aylık kıdem yeterlidir)."],
                ["1972 İkili Anlaşması & ICT Cerfa Dosyası", "Fransa-Türkiye İkili Sosyal Güvenlik Anlaşması ve Cerfa formu hazırlanır. Yerel iş piyasası araştırması (opposabilité de l'emploi) kısıtlamasından muaftır."],
                ["VFS Global Konsolosluk Randevusu (10-15 Gün)", "İstanbul (Harbiye/Altunizade), Ankara veya İzmir VFS Global merkezine başvuru teslim edilir. CCIFT/DEİK üyesi referansıyla 10-15 iş gününde vize sonuçlanır."],
                ["Fransa'ya Varış & ANEF Kaydı", "Fransa'ya giriş sonrasında online ANEF portalından ICT oturum kartı doğrulanır. Aile bireyleri de refakatçi oturumuyla Fransa'ya yerleşir."]
            ],
            fr: [
                ["Avenant de Mobilité Intra-Groupe (ICT)", "Convention de détachement établie entre le siège en Turquie et la filiale française (Beko, THY, Ekol, Barsan, Şişecam). Ancienneté minimale 3 à 6 mois."],
                ["Convention Bilatérale 1972 & Dossier Cerfa", "Application de la convention bilatérale de sécurité sociale et formalités Cerfa. Exonération totale du test du marché du travail (opposabilité de l'emploi)."],
                ["Dépôt Consulaire VFS Global (10 - 15 Jours)", "Dépôt du dossier au centre VFS (Istanbul, Ankara ou Izmir). Traitement accéléré grâce à l'agrément bilatéral CCIFT / DEİK."],
                ["Arrivée en France & Validation ANEF", "Validation en ligne du visa de long séjour valant titre de séjour (VLS-TS ICT). Droit de travail direct pour le conjoint accompagnant."]
            ]
        },
        voie_3: {
            tr: [
                ["İş Teklifi & Promesse d'Embauche (Maaş ≥ 2x SMIC)", "Paris scale-up girişimi tarafından yıllık brüt maaşı yasal eşiğin (en az 2x SMIC) üzerinde olan iş sözleşmesi imzalanır. Şirket içi çalışma dili %100 İngilizcedir."],
                ["French Tech Akreditasyonu & ANEF Ön Dosyası", "Şirketin Jeune Entreprise Innovante (JEI) veya French Tech statüsüyle ANEF üzerinden ön onay dosyası oluşturulur. Fransızca şartı ve Pôle Emploi ilanı aranmaz."],
                ["VFS Global \"Passeport Talent\" Başvurusu", "VLS-TS Passeport Talent (Entreprise Innovante) başvurusu Türkiye VFS merkezlerine teslim edilir. İşlem süresi ortalama 15-20 gündür."],
                ["4 Yıllık Oturum & Eşe Tam Çalışma Hakkı", "Fransa'da doğrudan 4 yıllık yenilenebilir oturum kartı alınır. Eşiniz otomatik olarak tam çalışma iznine sahip olur."]
            ],
            fr: [
                ["Contrat de Travail & Promesse d'Embauche", "Signature de l'offre auprès de la scale-up parisienne avec rémunération brute annuelle ≥ 2x SMIC légal. Équipe technique 100% anglophone."],
                ["Statut Entreprise Innovante & Dossier ANEF", "Validation via le statut JEI / French Tech. Aucune obligation de français et dispense de publication Pôle Emploi."],
                ["Dépôt Consulaire VFS \"Passeport Talent\"", "Dépôt du formulaire VLS-TS Passeport Talent dans les centres VFS en Turquie. Instruction rapide sous 15 jours ouvrés."],
                ["Titre Pluriannuel 4 Ans & Travail Conjoint", "Octroi direct d'une carte de séjour pluriannuelle de 4 ans renouvelable. Plein droit d'exercice professionnel immédiat pour le conjoint."]
            ]
        },
        autre: {
            tr: [
                ["İş Sözleşmesi (CDI / CDD)", "Fransız işveren ile çalışma şartları belirlenir ve iş sözleşmesi parafe edilir."],
                ["Çalışma İzni Başvurusu (DREETS / ANEF)", "İşveren Fransa İçişleri Bakanlığı portalından yabancı çalışan için resmi çalışma izni onayını alır."],
                ["VFS Global VLS-TS Başvurusu", "Onaylanan izin belgesiyle Türkiye'deki VFS Global merkezine uzun süreli çalışma vizesi başvurusu yapılır."],
                ["OFII Doğrulaması & İkamet", "Fransa'ya giriş sonrası 3 ay içinde ANEF sistemi üzerinden vize doğrulanır."]
            ],
            fr: [
                ["Contrat de Travail (CDI / CDD)", "Finalisation des conditions d'embauche avec l'entreprise établie en France."],
                ["Autorisation de Travail ANEF (DREETS)", "L'employeur dépose la demande d'autorisation de travail pour salarié étranger sur le portail dématérialisé ANEF."],
                ["Dépôt Visa VLS-TS au Centre VFS", "Dépôt consulaire auprès de VFS Global en Turquie avec l'attestation ministérielle d'autorisation de travail."],
                ["Validation OFII & Installation", "Validation en ligne de la vignette OFII sur le site de l'ANEF dans les 3 mois suivant l'entrée en France."]
            ]
        }
    };
    const KAPI_BADGES = {
        voie_1: { tr: "Kapı 1 · Uluslararası kurum", fr: "Voie 1 · Organisation internationale", icon: "landmark",
                  visaTr: "Klasik çalışma izni gerekmez (MEAE statüsü)", visaFr: "Pas d'autorisation de travail classique (statut MEAE)" },
        voie_2: { tr: "Kapı 2 · Şirket içi transfer (ICT)", fr: "Voie 2 · Mobilité intra-groupe (ICT)", icon: "transfer",
                  visaTr: "ICT vizesi, işgücü testinden muaf", visaFr: "Visa ICT, sans opposabilité de l'emploi" },
        voie_3: { tr: "Kapı 3 · Passeport Talent", fr: "Voie 3 · Passeport Talent", icon: "zap",
                  visaTr: "4 yıllık Passeport Talent oturumu", visaFr: "Titre Passeport Talent de 4 ans" },
        autre:  { tr: "Standart yol · Çalışma vizesi", fr: "Voie standard · Visa salarié", icon: "briefcase",
                  visaTr: "İşveren ANEF üzerinden çalışma izni almalı", visaFr: "L'employeur demande l'autorisation de travail (ANEF)" }
    };

    const DETAIL_TEXT = {
        tr: {
            back: "Geri", more: "Diğer seçenekler", share: "Paylaş", openSite: "Resmi siteyi aç", track: "Takibe ekle",
            fitTitle: "Bu ilan bana uygun mu?",
            frenchLabel: "Fransızca", noFrench: "Fransızca gerekmez", frenchReq: "İleri Fransızca gerekli", workLang: "Çalışma dili: ",
            visaLabel: "Vize", locationLabel: "Konum", locationDefault: "Fransa",
            roadmapTitle: "Vize yol haritası", roadmapDesc: "Türkiye'den Fransa'ya 4 adım. Ayrıntı için adıma dokunun.",
            descTitle: "İlan hakkında", noDesc: "Bu ilan için kısa açıklama yok. Ayrıntılar resmi sitede.",
            contactTitle: "İK iletişim", hrEmail: "İK e-posta", portal: "Kariyer portalı", listing: "İlan sayfası", note: "Not",
            copy: "Kopyala", copiedEmail: "✓ E-posta kopyalandı", copiedLink: "✓ Bağlantı kopyalandı", copied: "✓ Kopyalandı",
            favAdd: "Favorilere ekle", favRemove: "Favorilerden çıkar",
            letterCta: "Ön yazı hazırla",
            shareFallback: "✓ Paylaşım desteklenmiyor, bağlantı kopyalandı",
            tracked: "✓ Takip listesine eklendi", trackUnavailable: "Takip şu anda kullanılamıyor",
            markApplied: "Başvurdum olarak işaretle?", yes: "Evet", dismiss: "Kapat",
            markedApplied: "✓ Başvuruldu olarak işaretlendi",
            notFound: "İlan bulunamadı"
        },
        fr: {
            back: "Retour", more: "Plus d'options", share: "Partager", openSite: "Site officiel", track: "Suivre",
            fitTitle: "Cette offre est-elle pour moi ?",
            frenchLabel: "Français", noFrench: "Français non requis", frenchReq: "Français avancé requis", workLang: "Langue de travail : ",
            visaLabel: "Visa", locationLabel: "Lieu", locationDefault: "France",
            roadmapTitle: "Feuille de route visa", roadmapDesc: "4 étapes de la Turquie à la France. Touchez une étape pour le détail.",
            descTitle: "À propos de l'offre", noDesc: "Pas de description courte pour cette offre. Détails sur le site officiel.",
            contactTitle: "Contact RH", hrEmail: "Email RH", portal: "Portail carrières", listing: "Page de l'offre", note: "Note",
            copy: "Copier", copiedEmail: "✓ Email copié", copiedLink: "✓ Lien copié", copied: "✓ Copié",
            favAdd: "Ajouter aux favoris", favRemove: "Retirer des favoris",
            letterCta: "Préparer ma lettre",
            shareFallback: "✓ Partage indisponible, lien copié",
            tracked: "✓ Ajoutée au suivi", trackUnavailable: "Suivi indisponible pour le moment",
            markApplied: "Marquer comme candidature envoyée ?", yes: "Oui", dismiss: "Fermer",
            markedApplied: "✓ Marquée comme candidature envoyée",
            notFound: "Offre introuvable"
        }
    };

    function dt(key) {
        const dict = DETAIL_TEXT[State.lang] || DETAIL_TEXT.tr;
        return dict[key] !== undefined ? dict[key] : (DETAIL_TEXT.tr[key] || key);
    }

    function esc(value) {
        return String(value == null ? '' : value)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    // Icônes inline style Lucide (stroke 2, currentColor)
    const ICON_PATHS = {
        check: '<path d="M20 6 9 17l-5-5"/>',
        alert: '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
        chevron: '<path d="m6 9 6 6 6-6"/>',
        mail: '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
        globe: '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
        link: '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
        info: '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
        copy: '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
        landmark: '<line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/><line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/><line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/>',
        transfer: '<path d="m16 3 4 4-4 4"/><path d="M20 7H4"/><path d="m8 21-4-4 4-4"/><path d="M4 17h16"/>',
        zap: '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
        briefcase: '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>'
    };

    function icon(name, size) {
        const s = size || 20;
        return `<svg class="bld-ic" width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">${ICON_PATHS[name] || ''}</svg>`;
    }

    // Les tags des données commencent souvent par un emoji : on le retire (pas d'emoji dans le détail)
    const EMOJI_RE = /[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{FE0F}\u{200D}\u{20E3}\u{E0020}-\u{E007F}]/gu;
    function stripEmoji(text) {
        return String(text || '').replace(EMOJI_RE, '').replace(/\s{2,}/g, ' ').trim();
    }

    function getJobData(id) {
        const store = window.FransaData;
        if (!store || typeof store.get !== 'function' || id === undefined || id === null || id === '') return null;
        let job = store.get(id);
        if (!job && typeof id === 'string' && /^\d+$/.test(id)) job = store.get(Number(id));
        if (!job && typeof id === 'number') job = store.get(String(id));
        return job || null;
    }

    function trackerCall(method) {
        const te = window.TrackerEngine;
        if (!te || typeof te[method] !== 'function') return null;
        const args = Array.prototype.slice.call(arguments, 1);
        try {
            return { value: te[method].apply(te, args) };
        } catch (e) {
            console.warn('[BilateralDrawer] TrackerEngine.' + method + ' a échoué', e);
            return null;
        }
    }

    const EMAIL_RE = /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i;
    const URL_RE = /https?:\/\/[^\s<>"']+/i;

    /** Normalise un job FransaData dans l'état interne (format partagé avec le générateur). */
    function normalizeJob(raw) {
        const company = raw.company || '';
        const titleTr = raw.title_tr || raw.title_fr || '';
        const titleFr = raw.title_fr || titleTr;
        const tagsTr = Array.isArray(raw.tags_tr) ? raw.tags_tr : [];
        const tagsFr = Array.isArray(raw.tags_fr) && raw.tags_fr.length ? raw.tags_fr : tagsTr;
        const validTracks = ['voie_1', 'voie_2', 'voie_3', 'autre'];
        const track = validTracks.indexOf(raw.track) !== -1
            ? raw.track
            : detectTrackForJob(company, titleTr, tagsTr.join(' '), !!raw.ccift);
        const regInfo = company ? getRegistryInfo(company) : null;

        const contact = String(raw.contact_info || '').trim();
        const contactEmail = (contact.match(EMAIL_RE) || [])[0] || '';
        const contactUrl = (contact.match(URL_RE) || [])[0] || '';
        const contactNote = (!contactEmail && !contactUrl) ? contact : '';

        return {
            id: raw.id,
            titleTr,
            titleFr,
            company,
            location: raw.location || '',
            url: raw.url || regInfo?.ats || '',
            careerPortal: contactUrl || regInfo?.portal || '',
            hrEmail: contactEmail || regInfo?.hr_email || '',
            contactNote,
            snippetTr: raw.snippet_tr || raw.snippet_fr || '',
            snippetFr: raw.snippet_fr || raw.snippet_tr || '',
            tagsTr,
            tagsFr,
            visaTr: raw.visa_tr || '',
            visaFr: raw.visa_fr || raw.visa_tr || '',
            workingLang: raw.working_lang || '',
            isCcift: !!raw.ccift,
            isNoFrench: !!raw.no_french,
            score: raw.score,
            source: raw.source || '',
            track
        };
    }

    const BilateralDrawer = {
        bound: false,
        openSteps: [0],

        /**
         * Ouvre l'écran détail d'une offre (id FransaData).
         * Accepte encore un élément DOM portant data-id (compatibilité), mais lit toujours FransaData.
         */
        open(jobId) {
            if (jobId !== undefined && jobId !== null) {
                const id = (typeof jobId === 'object' && jobId.nodeType) ? jobId.getAttribute('data-id') : jobId;
                if (!this.loadJob(id)) {
                    Toast.show(dt('notFound'));
                    return;
                }
                this.openSteps = [0];
                this.render();
            }
            if (!State.currentJob) return;
            this.show();
        },

        /** Charge une offre dans l'état local SANS ouvrir l'écran (utilisé aussi par le générateur). */
        loadJob(id) {
            const raw = getJobData(id);
            if (!raw) return false;
            State.currentJob = normalizeJob(raw);
            State.currentTrack = State.currentJob.track;
            return true;
        },

        bind() {
            if (this.bound) return;
            const drawer = document.getElementById('bld-drawer');
            if (!drawer) return;
            this.bound = true;

            drawer.addEventListener('click', (e) => {
                const el = e.target.closest('[data-bld-action]');
                if (!el || !drawer.contains(el)) return;
                const action = el.getAttribute('data-bld-action');
                switch (action) {
                    case 'back': this.close(); break;
                    case 'menu': this.toggleMenu(); break;
                    case 'share': this.closeMenu(); this.share(); break;
                    case 'site': this.closeMenu(); break; // lien natif (target=_blank)
                    case 'track': this.closeMenu(); this.addToTracker(); break;
                    case 'fav': this.toggleFavorite(); break;
                    case 'letter': this.openLetter(); break;
                    case 'copy': this.copyValue(el.getAttribute('data-copy') || '', el.getAttribute('data-kind')); break;
                    case 'step': this.toggleStep(el); break;
                    default: break;
                }
            });

            const menu = document.getElementById('bld-drawer-menu');
            if (menu) {
                menu.addEventListener('keydown', (e) => {
                    const items = Array.prototype.slice.call(menu.querySelectorAll('[role="menuitem"]'));
                    const idx = items.indexOf(document.activeElement);
                    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                        e.preventDefault();
                        const next = e.key === 'ArrowDown' ? (idx + 1) % items.length : (idx - 1 + items.length) % items.length;
                        items[next].focus();
                    } else if (e.key === 'Tab') {
                        this.closeMenu();
                    }
                });
            }

            // Fermeture du menu au toucher en dehors
            document.addEventListener('pointerdown', (e) => {
                if (!this.isMenuOpen()) return;
                const wrap = document.getElementById('bld-drawer-menu-wrap');
                if (wrap && !wrap.contains(e.target)) this.closeMenu(false);
            }, true);

            // Titre court dans l'app bar une fois le titre principal sorti de l'écran
            const body = document.getElementById('bld-drawer-body');
            if (body) {
                let ticking = false;
                body.addEventListener('scroll', () => {
                    if (ticking) return;
                    ticking = true;
                    requestAnimationFrame(() => {
                        ticking = false;
                        this.syncAppBar();
                    });
                }, { passive: true });
            }
        },

        syncAppBar() {
            const drawer = document.getElementById('bld-drawer');
            const body = document.getElementById('bld-drawer-body');
            if (!drawer || !body) return;
            const heading = document.getElementById('bld-drawer-title');
            const limit = heading ? heading.offsetTop + heading.offsetHeight : 80;
            drawer.classList.toggle('bld-scrolled', body.scrollTop > 4);
            drawer.classList.toggle('bld-title-hidden', body.scrollTop > limit - 8);
        },

        render() {
            const job = State.currentJob;
            const drawer = document.getElementById('bld-drawer');
            if (!job || !drawer) return;
            this.bind();

            const lang = State.lang === 'fr' ? 'fr' : 'tr';
            const title = lang === 'fr' ? (job.titleFr || job.titleTr) : (job.titleTr || job.titleFr);
            const kapi = KAPI_BADGES[job.track] || KAPI_BADGES.autre;
            drawer.setAttribute('data-track', job.track);

            // App bar & menu
            const setText = (id, txt) => { const el = document.getElementById(id); if (el) el.textContent = txt; };
            const setLabel = (id, txt) => { const el = document.getElementById(id); if (el) el.setAttribute('aria-label', txt); };
            setText('bld-appbar-title', title);
            setLabel('bld-drawer-back', dt('back'));
            setLabel('bld-drawer-menu-btn', dt('more'));
            setText('bld-menu-share-label', dt('share'));
            setText('bld-menu-site-label', dt('openSite'));
            setText('bld-menu-track-label', dt('track'));
            const site = document.getElementById('bld-menu-site');
            if (site) {
                if (job.url) { site.href = job.url; site.hidden = false; } else { site.removeAttribute('href'); site.hidden = true; }
            }
            const trackItem = document.getElementById('bld-menu-track');
            if (trackItem) trackItem.hidden = !(window.TrackerEngine && (typeof window.TrackerEngine.addToTracker === 'function' || typeof window.TrackerEngine.openTrackerModal === 'function'));
            setText('bld-drawer-cta-label', dt('letterCta'));

            const body = document.getElementById('bld-drawer-body');
            if (body) {
                body.innerHTML = this.renderHero(job, title, kapi, lang)
                    + this.renderFit(job, kapi, lang)
                    + this.renderRoadmap(job.track, lang)
                    + this.renderDescription(job, lang)
                    + this.renderContact(job);
            }
            this.syncFavorite();
            this.syncAppBar();
        },

        renderHero(job, title, kapi, lang) {
            const meta = [job.company, job.location].filter(Boolean).join(' · ');
            return `
                <header class="bld-hero">
                    <span class="bld-kapi-badge">${icon(kapi.icon, 16)}<span>${esc(kapi[lang])}</span></span>
                    <h2 id="bld-drawer-title" class="bld-hero-title">${esc(title)}</h2>
                    ${meta ? `<p class="bld-hero-meta">${esc(meta)}</p>` : ''}
                </header>`;
        },

        renderFit(job, kapi, lang) {
            const row = (ok, label, value, sub) => `
                <li class="bld-fit-row">
                    <span class="bld-fit-icon ${ok ? 'is-ok' : 'is-warn'}">${icon(ok ? 'check' : 'alert', 18)}</span>
                    <span class="bld-fit-text">
                        <span class="bld-fit-label">${esc(label)}</span>
                        <span class="bld-fit-value">${esc(value)}</span>
                        ${sub ? `<span class="bld-fit-sub">${esc(sub)}</span>` : ''}
                    </span>
                </li>`;
            // Résumé court de la voie en gras (lisible d'un coup d'œil), détail visa de l'offre en dessous
            const visaText = lang === 'fr' ? kapi.visaFr : kapi.visaTr;
            const visaSub = lang === 'fr' ? job.visaFr : job.visaTr;
            const frenchSub = job.workingLang ? dt('workLang') + job.workingLang : '';
            return `
                <section class="bld-fit-card" aria-labelledby="bld-fit-title">
                    <h3 id="bld-fit-title" class="bld-section-heading">${esc(dt('fitTitle'))}</h3>
                    <ul class="bld-fit-list">
                        ${row(job.isNoFrench, dt('frenchLabel'), job.isNoFrench ? dt('noFrench') : dt('frenchReq'), frenchSub)}
                        ${row(job.track !== 'autre', dt('visaLabel'), visaText, visaSub)}
                        ${row(true, dt('locationLabel'), job.location || dt('locationDefault'), '')}
                    </ul>
                </section>`;
        },

        renderRoadmap(track, lang) {
            const steps = (VISA_STEPS[track] || VISA_STEPS.autre)[lang] || [];
            const items = steps.map(([title, desc], i) => {
                const open = this.openSteps.indexOf(i) !== -1;
                return `
                    <li class="bld-rm-step${open ? ' is-open' : ''}${i === 0 ? ' is-current' : ''}">
                        <span class="bld-rm-node" aria-hidden="true">${i + 1}</span>
                        <div class="bld-rm-main">
                            <button type="button" class="bld-rm-head" data-bld-action="step" data-step="${i}" aria-expanded="${open}" aria-controls="bld-rm-panel-${i}">
                                <span class="bld-rm-title">${esc(title)}</span>
                                ${icon('chevron', 20)}
                            </button>
                            <div class="bld-rm-panel" id="bld-rm-panel-${i}"${open ? '' : ' hidden'}>
                                <p>${esc(desc)}</p>
                            </div>
                        </div>
                    </li>`;
            }).join('');
            return `
                <section aria-labelledby="bld-rm-heading">
                    <h3 id="bld-rm-heading" class="bld-section-heading">${esc(dt('roadmapTitle'))}</h3>
                    <p class="bld-section-hint">${esc(dt('roadmapDesc'))}</p>
                    <ol class="bld-roadmap" id="bld-drawer-timeline">${items}</ol>
                </section>`;
        },

        renderDescription(job, lang) {
            const snippet = lang === 'fr' ? job.snippetFr : job.snippetTr;
            // Le lieu est déjà affiché (en-tête + « uygun mu? ») : on écarte les tags 📍
            const tags = (lang === 'fr' ? job.tagsFr : job.tagsTr)
                .filter(tag => String(tag).indexOf('\u{1F4CD}') !== 0)
                .map(stripEmoji).filter(Boolean)
                .filter((tag, i, arr) => arr.indexOf(tag) === i)
                .slice(0, 6);
            return `
                <section aria-labelledby="bld-desc-heading">
                    <h3 id="bld-desc-heading" class="bld-section-heading">${esc(dt('descTitle'))}</h3>
                    <p id="bld-drawer-snippet" class="bld-desc-text">${esc(snippet || dt('noDesc'))}</p>
                    ${tags.length ? `<ul class="bld-chips">${tags.map(tag => `<li class="bld-chip">${esc(tag)}</li>`).join('')}</ul>` : ''}
                </section>`;
        },

        renderContact(job) {
            const rows = [];
            const row = (ic, label, value, href, kind, external) => `
                <li class="bld-contact-row">
                    <span class="bld-contact-icon">${icon(ic, 20)}</span>
                    <span class="bld-contact-text">
                        <span class="bld-contact-label">${esc(label)}</span>
                        ${href
                            ? `<a class="bld-contact-value" href="${esc(href)}"${external ? ' target="_blank" rel="noopener"' : ''}>${esc(value)}</a>`
                            : `<span class="bld-contact-value">${esc(value)}</span>`}
                    </span>
                    <button type="button" class="bld-icon-btn bld-copy-btn" data-bld-action="copy" data-kind="${kind}" data-copy="${esc(value)}" aria-label="${esc(dt('copy') + ' : ' + label)}">${icon('copy', 20)}</button>
                </li>`;
            if (job.hrEmail) rows.push(row('mail', dt('hrEmail'), job.hrEmail, 'mailto:' + job.hrEmail, 'email', false));
            if (job.careerPortal) rows.push(row('globe', dt('portal'), job.careerPortal, job.careerPortal, 'link', true));
            if (job.contactNote) rows.push(row('info', dt('note'), job.contactNote, '', 'text', false));
            if (!rows.length && job.url) rows.push(row('link', dt('listing'), job.url, job.url, 'link', true));
            if (!rows.length) return '';
            return `
                <section aria-labelledby="bld-contact-heading">
                    <h3 id="bld-contact-heading" class="bld-section-heading">${esc(dt('contactTitle'))}</h3>
                    <ul class="bld-contact-list">${rows.join('')}</ul>
                </section>`;
        },

        toggleStep(btn) {
            const i = Number(btn.getAttribute('data-step'));
            const step = btn.closest('.bld-rm-step');
            const panel = document.getElementById('bld-rm-panel-' + i);
            const open = btn.getAttribute('aria-expanded') !== 'true';
            btn.setAttribute('aria-expanded', String(open));
            if (step) step.classList.toggle('is-open', open);
            if (panel) panel.hidden = !open;
            this.openSteps = this.openSteps.filter(n => n !== i);
            if (open) this.openSteps.push(i);
        },

        setLanguage(lang) {
            State.lang = lang;
            if (State.currentJob) this.render();
        },

        // --- Menu ⋮ -----------------------------------------------------------
        isMenuOpen() {
            const menu = document.getElementById('bld-drawer-menu');
            return !!(menu && !menu.hidden);
        },

        toggleMenu() {
            if (this.isMenuOpen()) this.closeMenu();
            else this.openMenu();
        },

        openMenu() {
            const menu = document.getElementById('bld-drawer-menu');
            const btn = document.getElementById('bld-drawer-menu-btn');
            if (!menu) return;
            menu.hidden = false;
            if (btn) btn.setAttribute('aria-expanded', 'true');
            const first = menu.querySelector('[role="menuitem"]:not([hidden])');
            if (first) first.focus({ preventScroll: true });
        },

        closeMenu(returnFocus = true) {
            const menu = document.getElementById('bld-drawer-menu');
            const btn = document.getElementById('bld-drawer-menu-btn');
            if (!menu || menu.hidden) return;
            menu.hidden = true;
            if (btn) {
                btn.setAttribute('aria-expanded', 'false');
                if (returnFocus) { try { btn.focus({ preventScroll: true }); } catch (e) { /* noop */ } }
            }
        },

        // --- Actions ------------------------------------------------------------
        async share() {
            const job = State.currentJob;
            if (!job) return;
            const title = State.lang === 'fr' ? (job.titleFr || job.titleTr) : (job.titleTr || job.titleFr);
            const text = [title, job.company].filter(Boolean).join(' – ');
            const url = job.url || location.href;
            if (navigator.share) {
                try {
                    await navigator.share({ title, text, url });
                    return;
                } catch (err) {
                    if (err && err.name === 'AbortError') return;
                }
            }
            const ok = await copyText(`${text}\n${url}`);
            Toast.show(ok ? dt('shareFallback') : t('toastCopyFail'));
        },

        addToTracker() {
            const job = State.currentJob;
            if (!job) return;
            // « Suivre » : ajout dans la colonne « Kaydedildi / Enregistré » du suivi
            const te = window.TrackerEngine;
            if (te && typeof te.addToTracker === 'function') {
                if (trackerCall('addToTracker', job.id, 'saved')) Toast.show(dt('tracked'));
            } else if (te && typeof te.openTrackerModal === 'function') {
                trackerCall('openTrackerModal', job.id);
            } else {
                Toast.show(dt('trackUnavailable'));
            }
        },

        syncFavorite() {
            const btn = document.getElementById('bld-drawer-fav');
            const job = State.currentJob;
            if (!btn || !job) return;
            const res = trackerCall('isFavorite', job.id);
            const fav = !!(res && res.value);
            btn.hidden = !(window.TrackerEngine && typeof window.TrackerEngine.toggleBookmark === 'function');
            btn.setAttribute('aria-pressed', String(fav));
            btn.setAttribute('aria-label', fav ? dt('favRemove') : dt('favAdd'));
            btn.title = fav ? dt('favRemove') : dt('favAdd');
        },

        toggleFavorite() {
            const job = State.currentJob;
            if (!job) return;
            // TrackerEngine.toggleBookmark affiche lui-même son toast
            trackerCall('toggleBookmark', job.id);
            this.syncFavorite();
        },

        openLetter() {
            const job = State.currentJob;
            if (!job) return;
            CoverLetterGenerator.open(job.id);
        },

        copyValue(value, kind) {
            if (!value) return;
            copyText(value).then((ok) => {
                if (!ok) { Toast.show(t('toastCopyFail')); return; }
                Toast.show(kind === 'email' ? dt('copiedEmail') : kind === 'link' ? dt('copiedLink') : dt('copied'));
            });
        },

        /** Compatibilité : copie de l'email RH de l'offre courante. */
        copyEmail() {
            const email = State.currentJob?.hrEmail;
            if (email) this.copyValue(email, 'email');
        },

        // --- Ouverture / fermeture (contrat d'historique 'drawer') ---------------
        isOpen() {
            return isOverlayOpen('bld-drawer');
        },

        show() {
            const overlay = document.getElementById('bld-drawer-overlay');
            const drawer = document.getElementById('bld-drawer');
            if (!drawer) return;
            this.bind();
            const wasOpen = this.isOpen();
            if (overlay) overlay.classList.add('open');
            drawer.classList.add('open');
            drawer.setAttribute('aria-hidden', 'false');
            document.documentElement.classList.add('bld-detail-open');
            const body = document.getElementById('bld-drawer-body');
            if (body && !wasOpen) body.scrollTop = 0;
            this.syncAppBar();
            syncScrollLock();
            if (!wasOpen) {
                OverlayHistory.push('drawer');
                rememberFocus('drawer', document.getElementById('bld-drawer-back'));
            }
        },

        /** Fermeture demandée par l'UI (retour, fond, Échap) : passe par l'historique si besoin. */
        close() {
            if (!this.isOpen()) return;
            OverlayHistory.requestClose('drawer', () => this.hide());
        },

        /** Fermeture effective, sans toucher à l'historique. */
        hide() {
            const overlay = document.getElementById('bld-drawer-overlay');
            const drawer = document.getElementById('bld-drawer');
            this.closeMenu(false);
            if (overlay) overlay.classList.remove('open');
            if (drawer) {
                drawer.classList.remove('open');
                drawer.setAttribute('aria-hidden', 'true');
            }
            document.documentElement.classList.remove('bld-detail-open');
            syncScrollLock();
            restoreFocus('drawer');
        }
    };

    // --------------------------------------------------------------------------
    // 5. GÉNÉRATEUR INTELLIGENT DE LETTRE & PITCH (TR ➔ FR)
    // --------------------------------------------------------------------------
    const CoverLetterGenerator = {
        open(jobId) {
            if (jobId !== undefined && jobId !== null) {
                // Ouverture directe (depuis une carte ou le détail) : on charge l'offre sans ouvrir le détail
                const id = (typeof jobId === 'object' && jobId.nodeType) ? jobId.getAttribute('data-id') : jobId;
                if (!BilateralDrawer.loadJob(id)) State.currentJob = null;
            }
            this.hideApplyPrompt();

            // Si aucun job n'est encore chargé, on initialise avec des valeurs par défaut
            if (!State.currentJob) {
                State.currentJob = {
                    titleTr: "Uzman Yönetici / Specialist",
                    titleFr: "Manager / Spécialiste Opérationnel",
                    company: "Entreprise Partenaire Bilatérale",
                    location: "Paris, France",
                    isNoFrench: true,
                    track: "voie_2"
                };
            }

            State.currentTrack = State.currentJob.track || "voie_2";
            this.setVoie(State.currentTrack);
            this.setTab(State.generatorTab || 'email');
            this.renderLabels();

            const overlay = document.getElementById('bld-gen-modal-overlay');
            if (!overlay) return;
            const wasOpen = this.isOpen();
            overlay.classList.add('open');
            const body = overlay.querySelector('.bld-modal-body');
            if (body && !wasOpen) body.scrollTop = 0;
            syncScrollLock();
            if (!wasOpen) {
                // Si le drawer est ouvert, cet état s'empile au-dessus de { fransaOverlay: 'drawer' }
                OverlayHistory.push('letter');
                rememberFocus('letter', overlay.querySelector('.bld-close-btn'));
            }

            this.updatePreview();
        },

        isOpen() {
            return isOverlayOpen('bld-gen-modal-overlay');
        },

        /** Fermeture demandée par l'UI (X, fond, Échap). */
        close() {
            if (!this.isOpen()) return;
            OverlayHistory.requestClose('letter', () => this.hide());
        },

        /** Fermeture effective, sans toucher à l'historique (le drawer éventuel reste ouvert). */
        hide() {
            const overlay = document.getElementById('bld-gen-modal-overlay');
            if (overlay) overlay.classList.remove('open');
            this.hideApplyPrompt();
            syncScrollLock();
            restoreFocus('letter');
        },

        /** Libellés d'interface dynamiques du générateur, dans la langue courante. */
        renderLabels() {
            const job = State.currentJob;
            const targetJobLabel = document.getElementById('bld-gen-target-job');
            if (targetJobLabel) {
                if (job && (job.titleTr || job.titleFr)) {
                    const title = State.lang === 'fr' ? (job.titleFr || job.titleTr) : (job.titleTr || job.titleFr);
                    targetJobLabel.textContent = `${t('targetJob')} : ${title}${job.company ? ' – ' + job.company : ''}`;
                } else {
                    targetJobLabel.textContent = `${t('targetJob')} : ${t('generalApplication')}`;
                }
            }

            const ecusson = VOIE_ECUSSONS[State.currentTrack] || VOIE_ECUSSONS["autre"];
            const ecussonEl = document.getElementById('bld-gen-modal-ecusson');
            if (ecussonEl) {
                ecussonEl.className = 'ecusson-card-header bld-ecusson-flush ' + ecusson.cssClass;
                ecussonEl.innerHTML = `
                    <div class="ecusson-header-title">${State.lang === 'fr' ? ecusson.title_fr : ecusson.title_tr}</div>
                    <div class="ecusson-header-sub">${t('genEcussonSub')}</div>
                `;
            }

            const copyLabel = document.getElementById('bld-copy-btn-label');
            if (copyLabel && !copyLabel.dataset.feedback) copyLabel.textContent = t('copyLabel');
        },

        setTab(tab) {
            State.generatorTab = tab;
            const btnEmail = document.getElementById('bld-tab-email-btn');
            const btnLetter = document.getElementById('bld-tab-letter-btn');
            if (btnEmail) {
                btnEmail.classList.toggle('active', tab === 'email');
                btnEmail.setAttribute('aria-selected', String(tab === 'email'));
            }
            if (btnLetter) {
                btnLetter.classList.toggle('active', tab === 'letter');
                btnLetter.setAttribute('aria-selected', String(tab === 'letter'));
            }
            this.updatePreview();
        },

        setVoie(voieKey) {
            State.currentTrack = voieKey;
            ['voie_1', 'voie_2', 'voie_3', 'autre'].forEach(k => {
                const btn = document.getElementById(`bld-btn-voie-${k}`);
                if (btn) {
                    btn.classList.toggle('active', k === voieKey);
                    btn.setAttribute('aria-pressed', String(k === voieKey));
                }
            });

            // Mise à jour de l'Écusson dans la modale (langue courante)
            this.renderLabels();
            this.updatePreview();
        },

        updatePreview() {
            const nameInput = document.getElementById('bld-cand-name');
            const titleInput = document.getElementById('bld-cand-title');
            const expInput = document.getElementById('bld-cand-exp');
            const skillsInput = document.getElementById('bld-cand-skills');

            const name = (nameInput?.value || "Can Yılmaz").trim();
            const candTitle = (titleInput?.value || "Senior Software Engineer / Uzman Yönetici").trim();
            const exp = (expInput?.value || "6").trim();
            const skills = (skillsInput?.value || "Systèmes distribués, Cloud, optimisation des flux internationaux").trim();

            const job = State.currentJob || {
                titleFr: "Ingénieur Logiciel Senior",
                company: "Entreprise en France",
                location: "Paris, France",
                isNoFrench: true
            };

            const jobTitle = job.titleFr || job.titleTr || "Opportunité Professionnelle";
            const company = job.company || "votre entreprise";
            const location = job.location || "France";
            const isNoFrench = job.isNoFrench;

            const slug = name.toLowerCase().replace(/[^a-z0-9]/g, '-');
            const todayStr = new Date().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });

            let generatedText = "";

            if (State.generatorTab === 'email') {
                // ==============================================================
                // EMAIL COURT / PREMIER CONTACT AU RECRUTEUR EN FRANÇAIS SOUTENU
                // ==============================================================
                let subjectVoie = "";
                let specificVoieArg = "";

                if (State.currentTrack === 'voie_1') {
                    subjectVoie = "Voie 1 : Statut International MAE sans autorisation de travail classique";
                    specificVoieArg = `En tant que citoyen(ne) d'un État membre de plein droit et profondément attaché(e) aux valeurs multilatérales de ${company}, ma candidature s'inscrit directement dans le cadre de la Voie 1 (Statut de fonctionnaire international sous protocole MEAE). Conformément aux accords de siège liant l'institution à la République française, cette prise de fonction s'exerce sous dispense intégrale d'autorisation de travail classique, avec titre de séjour spécial délivré par le Ministère de l'Europe et des Affaires Étrangères.`;
                } else if (State.currentTrack === 'voie_2') {
                    subjectVoie = "Voie 2 : Mobilité intra-groupe ICT & accord bilatéral CCIFT/DEİK";
                    specificVoieArg = `Très familier(e) des synergies bilatérales entre la Turquie et la France et des standards opérationnels des groupes membres de la CCIFT / DEİK, je dispose d'une employabilité immédiate sous le régime de la Voie 2 (Salarié détaché ICT). Ma transition administrative vers la France peut s'effectuer de manière accélérée et sécurisée via les accords bilatéraux et la convention franco-turque de sécurité sociale de 1972, sans blocage lié à l'opposabilité de l'emploi local.`;
                } else if (State.currentTrack === 'voie_3') {
                    subjectVoie = "Voie 3 : Passeport Talent French Tech & 100% Anglais";
                    specificVoieArg = `Habitué(e) à évoluer au quotidien dans un environnement international 100% anglophone (niveau C1/C2 professionnel attesté), je suis immédiatement opérationnel(le) sur votre stack technique. Par ailleurs, la qualité d'entreprise innovante de ${company} permet une activation directe de la Voie 3 (Passeport Talent – Entreprise Innovante), garantissant une délivrance consulaire accélérée sous 2 à 3 semaines en Turquie pour un titre pluriannuel de 4 ans exempt d'autorisation de travail préalable.`;
                } else {
                    subjectVoie = "Voie 4 : Mobilité Qualifiée & VLS-TS";
                    specificVoieArg = `Fort(e) d'une grande rigueur opérationnelle et d'une adaptabilité multiculturelle éprouvée, je suis immédiatement mobilisable pour engager les démarches d'autorisation de travail et intégrer vos effectifs en France dans le cadre d'un visa VLS-TS salarié.`;
                }

                generatedText = `Objet : Candidature : ${jobTitle} – ${name} (${subjectVoie})

Madame, Monsieur,

Je me permets de vous contacter avec un vif intérêt suite à la publication de votre opportunité de ${jobTitle} au sein de ${company}.

Fort(e) de ${exp} années d'expérience en tant que ${candTitle}, j'ai développé une solide expertise en ${skills}.

${specificVoieArg}

Seriez-vous ouvert(e) à un bref échange informel de 10 minutes cette semaine afin de faire le point sur vos priorités actuelles ?

Je vous transmets ci-joint mon CV actualisé aux standards européens.

Bien cordialement,

${name}
${candTitle}
Tél. / WhatsApp : +90 5XX XXX XX XX
Email : ${slug}@email.com
Profil LinkedIn : linkedin.com/in/${slug}`;

            } else {
                // ==============================================================
                // LETTRE DE MOTIVATION FORMELLE (TR ➔ FR SOUTENU)
                // INSTRUCTION CLIENT : PARAGRAPHE D'INTRODUCTION CITANT LA VOIE
                // ==============================================================
                let pIntroVoie = "";
                let pLegal = "";
                let pLang = isNoFrench 
                    ? `Habitué(e) à travailler intégralement en anglais (niveau C1 professionnel attesté), je m'intègre avec une totale aisance dans des équipes cosmopolites et des réunions techniques internationales, tout en perfectionnant activement ma maîtrise de la langue française pour accélérer mon ancrage culturel.`
                    : `Parfaitement bilingue franco-turc et maîtrisant l'anglais professionnel, je dispose d'une capacité naturelle à naviguer entre les cultures professionnelles, à négocier avec des interlocuteurs exigeants et à rédiger des livrables de haute tenue tant en français qu'en anglais.`;

                if (State.currentTrack === 'voie_1') {
                    pIntroVoie = `C'est dans le cadre de la Voie d'accès statutaire dérogatoire des institutions internationales (accord de siège et titre spécial du Ministère de l'Europe et des Affaires Étrangères - MEAE, sans autorisation de travail classique requise) que je vous soumets avec un vif intérêt ma candidature pour le poste de ${jobTitle} au sein de ${company} à ${location}. En tant que citoyen(ne) d'un État membre fondateur et animé(e) par la vocation multilatérale de votre institution, ma prise de fonction est directement sécurisée sur le plan diplomatique dès l'officialisation de la nomination.`;
                    pLegal = `Sur le plan statutaire, le recrutement au sein de ${company} s'exerce sous le régime dérogatoire de la fonction publique internationale, formalisé par l'accord de siège liant l'institution au Gouvernement de la République française. Cette disposition dispense expressément l'organisation de toute démarche d'autorisation de travail auprès du Ministère du Travail ou de l'OFII. Dès l'officialisation de la sélection, l'instruction consulaire s'effectue par note verbale prioritaire et délivrance du visa de protocole, suivi de la remise du Titre de Séjour Spécial délivré par le protocole du Ministère de l'Europe et des Affaires Étrangères (MEAE).`;
                } else if (State.currentTrack === 'voie_2') {
                    pIntroVoie = `C'est sous le régime privilégié de la Voie de mobilité bilatérale intra-groupe (Salarié détaché ICT - articles L. 421-26 et suivants du CESEDA et accord franco-turc de sécurité sociale du 20 janvier 1972) que je vous adresse ma candidature pour le poste de ${jobTitle} au sein de votre filiale française à ${location}. Reconnue pour son leadership au sein des réseaux de la Chambre de Commerce Franco-Turque (CCIFT) et du Conseil d'affaires DEİK, votre organisation incarne l'excellence du partenariat économique entre nos deux pays, et cette voie juridique garantit une transition opérationnelle immédiate, exempte de toute opposabilité de l'emploi local.`;
                    pLegal = `Sur le plan administratif et juridique, ma relocalisation depuis la Turquie bénéficie d'un cadre bilatéral particulièrement éprouvé. Grâce aux conventions franco-turques et au statut des entreprises accréditées CCIFT/DEİK, les démarches d'expatriation ou de détachement intra-groupe (visa Salarié détaché ICT, régi par les articles L. 421-26 et suivants du CESEDA) bénéficient d'une dispense totale d'opposabilité de la situation de l'emploi en France et d'une instruction consulaire prioritaire auprès des centres VFS Global en Turquie. La couverture sociale est par ailleurs maintenue sans rupture dans le cadre de la convention bilatérale de sécurité sociale du 20 janvier 1972.`;
                } else if (State.currentTrack === 'voie_3') {
                    pIntroVoie = `C'est au titre du dispositif d'attractivité de la Voie Passeport Talent – Entreprise Innovante (Article L. 421-9 du CESEDA) que je vous soumets ma candidature pour le poste de ${jobTitle} au sein de ${company} à ${location}. Immédiatement opérationnel(le) dans un environnement d'ingénierie 100% anglophone, cette voie consulaire simplifiée permet une délivrance accélérée en Turquie (2 à 3 semaines via VFS Global) d'un titre de séjour pluriannuel de 4 ans exempt d'autorisation de travail préalable, tout en accordant à mon conjoint une liberté totale de travail en France dès l'arrivée.`;
                    pLegal = `Concernant ma venue en France depuis la Turquie, le statut d'entreprise innovante de ${company} permet une activation immédiate et simplifiée de la procédure 'Passeport Talent – Salarié d'une Jeune Entreprise Innovante (JEI)' (Article L. 421-9 du CESEDA). Ce titre de séjour pluriannuel d'une durée de 4 ans est exempt de toute autorisation de travail DIRECCTE préalable, garantit un rendez-vous consulaire accéléré sous 2 à 3 semaines auprès de VFS Global à Istanbul ou Ankara, et confère à ma famille un statut stable et protecteur.`;
                } else {
                    pIntroVoie = `C'est avec un enthousiasme soutenu que je vous soumets ma candidature pour le poste de ${jobTitle} au sein de ${company} à ${location}. Prêt(e) à engager sans délai la procédure d'autorisation de travail et de visa long séjour salarié (VLS-TS) via la plateforme dématérialisée ANEF et les services consulaires en Turquie, je souhaite mettre ma rigueur et mes compétences techniques au service de votre dynamique de croissance.`;
                    pLegal = `Sur le plan administratif, je suis disponible pour finaliser sans délai la constitution du dossier de visa long séjour salarié (VLS-TS) via la procédure dématérialisée de l'ANEF, avec l'appui de mon dossier consulaire complet déjà prêt pour le centre VFS Global en Turquie.`;
                }

                generatedText = `${name}
${candTitle}
Istanbul, Turquie (Disponibilité pour mobilité en France)
Email : ${slug}@email.com | Tél. : +90 5XX XXX XX XX
LinkedIn : linkedin.com/in/${slug}

À l'attention de la Direction des Ressources Humaines
${company}
${location}

Fait le ${todayStr}

Objet : Candidature au poste de ${jobTitle} – Réf. Mobilité Bilatérale France-Turquie

Madame, Monsieur,

${pIntroVoie}

Titulaire d'une formation supérieure spécialisée et fort(e) de ${exp} années d'expérience réussie dans le domaine de ${candTitle}, j'ai développé une solide expertise en ${skills}. Au cours de mes précédentes missions, j'ai notamment piloté des projets transversaux complexes, collaboré avec des équipes pluridisciplinaires réparties sur plusieurs fuseaux horaires, et garanti une livraison conforme aux normes de qualité les plus strictes. Mon approche repose sur l'analyse méthodique, la recherche systématique d'optimisation et une communication fluide entre les différents départements opérationnels.

${pLang}

${pLegal}

Rigoureux(se), doté(e) d'une grande faculté d'adaptation et animé(e) par la volonté de créer une valeur tangible au sein de vos effectifs, je serais honoré(e) d'approfondir les termes de ma candidature lors d'un entretien, à votre convenance.

Dans cette attente, je vous prie d'agréer, Madame, Monsieur, l'expression de ma considération distinguée.

${name}
${candTitle}`;
            }

            const previewEl = document.getElementById('bld-gen-preview');
            if (previewEl) previewEl.textContent = generatedText;

            // Objet réutilisé comme titre de partage (ex. sujet Gmail)
            const subjectMatch = generatedText.match(/^Objet : (.+)$/m);
            State.lastSubject = subjectMatch ? subjectMatch[1].trim() : `Candidature – ${jobTitle}`;
        },

        getText() {
            const previewEl = document.getElementById('bld-gen-preview');
            return previewEl?.textContent || "";
        },

        copy() {
            const text = this.getText();
            if (!text) return Promise.resolve(false);

            return copyText(text).then((ok) => {
                Toast.show(ok ? t('toastCopied') : t('toastCopyFail'));
                const label = document.getElementById('bld-copy-btn-label');
                if (ok && label) {
                    label.dataset.feedback = '1';
                    label.textContent = t('copied');
                    setTimeout(() => {
                        delete label.dataset.feedback;
                        label.textContent = t('copyLabel');
                    }, 2000);
                }
                if (ok) this.showApplyPrompt();
                return ok;
            });
        },

        /**
         * Partage natif Android/iOS (WhatsApp, Gmail, LinkedIn…) via Web Share API,
         * avec repli sur la copie presse-papiers. Une annulation (AbortError) est silencieuse.
         */
        async share() {
            const text = this.getText();
            if (!text) return;
            const title = State.lastSubject || (State.generatorTab === 'email' ? t('shareTitleEmail') : t('shareTitleLetter'));

            if (navigator.share) {
                try {
                    await navigator.share({ title, text });
                    this.showApplyPrompt();
                    return;
                } catch (err) {
                    if (err && err.name === 'AbortError') return;
                    // Autre erreur (NotAllowedError, données refusées…) : repli copie
                }
            }

            const ok = await copyText(text);
            Toast.show(ok ? t('toastShareFallback') : t('toastCopyFail'));
            if (ok) this.showApplyPrompt();
        },

        /**
         * Après un « Paylaş » / « Kopyala » réussi : carte « Başvurdum olarak işaretle? »
         * [Evet] -> TrackerEngine.addToTracker(id, 'applied'). Uniquement pour une offre réelle.
         */
        showApplyPrompt() {
            const job = State.currentJob;
            const box = document.getElementById('bld-apply-prompt');
            if (!box || !job || job.id === undefined || job.id === null) return;
            if (!(window.TrackerEngine && typeof window.TrackerEngine.addToTracker === 'function')) return;
            const q = document.getElementById('bld-apply-prompt-text');
            const yes = document.getElementById('bld-apply-prompt-yes');
            const no = document.getElementById('bld-apply-prompt-dismiss');
            if (q) q.textContent = dt('markApplied');
            if (yes) yes.textContent = dt('yes');
            if (no) no.setAttribute('aria-label', dt('dismiss'));
            box.dataset.jobId = String(job.id);
            box.hidden = false;
        },

        hideApplyPrompt() {
            const box = document.getElementById('bld-apply-prompt');
            if (box) box.hidden = true;
        },

        markApplied() {
            const box = document.getElementById('bld-apply-prompt');
            const raw = box && box.dataset.jobId;
            this.hideApplyPrompt();
            if (raw === undefined || raw === '') return;
            const id = /^\d+$/.test(raw) ? Number(raw) : raw;
            if (trackerCall('addToTracker', id, 'applied')) Toast.show(dt('markedApplied'));
        },

        download() {
            const text = this.getText();
            if (!text) return;

            const filename = State.generatorTab === 'email' ? 'Email_Contact_FR.txt' : 'Lettre_Motivation_FR.txt';
            const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            setTimeout(() => URL.revokeObjectURL(url), 1000);
            Toast.show(`${t('toastDownloaded')}${filename}`);
        }
    };

    // --------------------------------------------------------------------------
    // 6. GUIDE BILINGUE PRATIQUE DE L'EXPATRIATION (MODAL & ONGLETS)
    // --------------------------------------------------------------------------
    const MobilityGuide = {
        open() {
            const overlay = document.getElementById('bld-guide-modal-overlay');
            if (!overlay) return;
            const wasOpen = this.isOpen();
            overlay.classList.add('open');
            this.setTab('visas');
            const body = overlay.querySelector('.bld-modal-body');
            if (body && !wasOpen) body.scrollTop = 0;
            syncScrollLock();
            if (!wasOpen) {
                OverlayHistory.push('guide');
                rememberFocus('guide', overlay.querySelector('.bld-close-btn'));
            }
        },

        isOpen() {
            return isOverlayOpen('bld-guide-modal-overlay');
        },

        /** Fermeture demandée par l'UI (X, fond, Échap, bouton « Anladım »). */
        close() {
            if (!this.isOpen()) return;
            OverlayHistory.requestClose('guide', () => this.hide());
        },

        /** Fermeture effective, sans toucher à l'historique. */
        hide() {
            const overlay = document.getElementById('bld-guide-modal-overlay');
            if (overlay) overlay.classList.remove('open');
            syncScrollLock();
            restoreFocus('guide');
        },

        setTab(tab) {
            const btnVisas = document.getElementById('bld-guide-tab-visas-btn');
            const btnCv = document.getElementById('bld-guide-tab-cv-btn');
            const contentVisas = document.getElementById('bld-guide-content-visas');
            const contentCv = document.getElementById('bld-guide-content-cv');

            if (btnVisas) {
                btnVisas.classList.toggle('active', tab === 'visas');
                btnVisas.setAttribute('aria-selected', String(tab === 'visas'));
            }
            if (btnCv) {
                btnCv.classList.toggle('active', tab === 'cv');
                btnCv.setAttribute('aria-selected', String(tab === 'cv'));
            }
            if (contentVisas) contentVisas.style.display = tab === 'visas' ? 'block' : 'none';
            if (contentCv) contentCv.style.display = tab === 'cv' ? 'block' : 'none';
        }
    };

    // --------------------------------------------------------------------------
    // 7. TOAST NOTIFICATION SERVICE
    // --------------------------------------------------------------------------
    const Toast = {
        hideTimer: null,
        show(msg) {
            let toastEl = document.getElementById('bld-toast-notification');
            if (!toastEl) {
                toastEl = document.createElement('div');
                toastEl.id = 'bld-toast-notification';
                toastEl.className = 'bld-toast';
                toastEl.setAttribute('role', 'status');
                toastEl.setAttribute('aria-live', 'polite');
                document.body.appendChild(toastEl);
            }
            toastEl.textContent = msg;
            toastEl.classList.add('show');
            clearTimeout(this.hideTimer);
            this.hideTimer = setTimeout(() => {
                toastEl.classList.remove('show');
            }, 3200);
        }
    };

    // --------------------------------------------------------------------------
    // 8. EXPOSITION SUR WINDOW
    // --------------------------------------------------------------------------
    window.BilateralDrawer = BilateralDrawer;
    window.CoverLetterGenerator = CoverLetterGenerator;
    window.MobilityGuide = MobilityGuide;
    window.BilateralToast = Toast;

    // Écoute des changements de langue globaux
    // (émis par TrackerEngine.applyLanguage : CustomEvent('languageChanged', { detail: { lang } }))
    window.addEventListener('languageChanged', (e) => {
        const newLang = (e && e.detail && e.detail.lang) || readStoredLang();
        State.lang = newLang;
        if (State.currentJob) {
            BilateralDrawer.render();
        }
        // Libellés du générateur (la lettre elle-même reste en français)
        CoverLetterGenerator.renderLabels();
        const prompt = document.getElementById('bld-apply-prompt');
        if (prompt && !prompt.hidden) CoverLetterGenerator.showApplyPrompt();
    });

    // Fermeture par touche ESC : uniquement l'overlay du dessus
    document.addEventListener('keydown', (e) => {
        if (e.key !== 'Escape') return;
        if (BilateralDrawer.isMenuOpen()) {
            BilateralDrawer.closeMenu();
        } else if (CoverLetterGenerator.isOpen()) {
            CoverLetterGenerator.close();
        } else if (MobilityGuide.isOpen()) {
            MobilityGuide.close();
        } else if (BilateralDrawer.isOpen()) {
            BilateralDrawer.close();
        }
    });

    // Bouton / geste retour Android : contrat d'historique partagé.
    // Chaque overlay se ferme si l'état courant n'est plus le sien, sans toucher à l'historique.
    window.addEventListener('popstate', (event) => {
        OverlayHistory.settle();
        const current = (event.state || {}).fransaOverlay;

        if (CoverLetterGenerator.isOpen() && current !== 'letter') {
            CoverLetterGenerator.hide();
        }
        if (MobilityGuide.isOpen() && current !== 'guide') {
            MobilityGuide.hide();
        }
        // Overlays empilés : quand on revient de { letter } à { drawer }, le drawer reste ouvert.
        // Le générateur a déjà été traité ci-dessus : s'il est encore ouvert, l'état 'letter' lui appartient.
        if (BilateralDrawer.isOpen() && current !== 'drawer' && !(current === 'letter' && CoverLetterGenerator.isOpen())) {
            BilateralDrawer.hide();
        }
    });

})(window, document);
