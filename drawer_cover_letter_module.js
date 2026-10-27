/**
 * ==============================================================================
 * BILATERAL FRANCE-TURKEY : DRAWER D'OPPORTUNITÉ & GÉNÉRATEUR INTELLIGENT DE LETTRE
 * ------------------------------------------------------------------------------
 * Module Vanilla JS ES6+ autonome et prêt à être fusionné dans dashboard.html
 * 
 * Fonctionnalités clés :
 * 1. Panneau latéral coulissant ("Drawer Détail de l'Opportunité")
 *    - Écusson officiel de la voie (Voie 1 MAE, Voie 2 ICT, Voie 3 Passeport Talent)
 *    - Coordonnées RH complètes, bouton de copie d'email et lien direct ATS
 *    - Fiche visa personnalisée étape par étape (4 étapes Turquie -> France)
 * 2. Générateur Intelligent de Pitch & Lettre de Motivation (TR ➔ FR)
 *    - Email court de premier contact (LinkedIn InMail / Email direct)
 *    - Lettre de motivation formelle en français soutenu
 *    - Paragraphe d'introduction rappelant explicitement la voie juridique
 *    - Copie en 1-clic avec Toast et téléchargement .txt
 * 3. Guide bilingue pratique de l'expatriation (3 visas & conversion CV turc)
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
            title_tr: "🏛️ VOIE 1 PRIORITAIRE : STATUT INTERNATIONAL MAE",
            title_fr: "🏛️ VOIE 1 PRIORITAIRE : STATUT INTERNATIONAL MAE",
            sub_tr: "Klasik çalışma izni aranmaz • Fransa Dışişleri Protokolü (Titre Spécial MEAE) • Kurucu Üyelik",
            sub_fr: "Dispense totale d'autorisation de travail • Titre spécial protocole MEAE • Accord de siège",
            cssClass: "ecusson-voie-1",
            color: "#1e40af",
            bg: "#eff6ff"
        },
        "voie_2": {
            title_tr: "🤝 VOIE 2 PRIORITAIRE : SALARIÉ DÉTACHÉ ICT (CCIFT & DEİK)",
            title_fr: "🤝 VOIE 2 PRIORITAIRE : SALARIÉ DÉTACHÉ ICT (CCIFT & DEİK)",
            sub_tr: "Şirket İçi Transfer (ICT) • 1972 İkili Sosyal Güvenlik Anlaşması • İşgücü Testinden Muaf",
            sub_fr: "Mobilité intra-groupe (CESEDA L. 421-26) • Accord bilatéral 1972 • Exonération opposabilité emploi",
            cssClass: "ecusson-voie-2",
            color: "#92400e",
            bg: "#fef3c7"
        },
        "voie_3": {
            title_tr: "⚡ VOIE 3 PRIORITAIRE : PASSEPORT TALENT (FRENCH TECH)",
            title_fr: "⚡ VOIE 3 PRIORITAIRE : PASSEPORT TALENT (FRENCH TECH)",
            sub_tr: "%100 İngilizce • Yenilikçi Şirket (JEI) • 4 Yıllık Oturum • Eşe Tam Çalışma İzni",
            sub_fr: "Entreprise innovante (CESEDA L. 421-9) • Titre pluriannuel 4 ans • 100% Anglais • Conjoint autorisé",
            cssClass: "ecusson-voie-3",
            color: "#6d28d9",
            bg: "#f5f3ff"
        },
        "autre": {
            title_tr: "🏢 VOIE 4 : STANDART ÇALIŞMA VİZESİ (VLS-TS)",
            title_fr: "🏢 VOIE 4 : VISA DE TRAVAIL SALARIÉ STANDARD (VLS-TS)",
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
    const State = {
        currentJob: null,
        currentTrack: "voie_2",
        generatorTab: "email", // 'email' | 'letter'
        lang: (typeof localStorage !== 'undefined' && localStorage.getItem('bilateral_lang')) || "tr"
    };

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
    // 4. PANNEAU LATÉRAL COULISSANT (DRAWER)
    // --------------------------------------------------------------------------
    const BilateralDrawer = {
        open(jobIdOrCard) {
            if (jobIdOrCard !== undefined && jobIdOrCard !== null) {
                if (typeof jobIdOrCard === 'object' && jobIdOrCard.nodeType) {
                    this.openFromCard(jobIdOrCard);
                    return;
                }
                if (typeof jobIdOrCard === 'number' || typeof jobIdOrCard === 'string') {
                    const card = document.querySelector(`.job-card[data-id="${jobIdOrCard}"]`);
                    if (card) {
                        this.openFromCard(card);
                        return;
                    }
                }
            }
            this.show();
        },

        openFromCard(cardElement) {
            if (!cardElement) return;

            const id = cardElement.getAttribute('data-id') || '0';
            const titleTr = cardElement.getAttribute('data-title-tr') || cardElement.querySelector('.job-title')?.textContent || '';
            const titleFr = cardElement.getAttribute('data-title-fr') || titleTr;
            const company = cardElement.getAttribute('data-company') || '';
            const location = cardElement.getAttribute('data-location') || '';
            const url = cardElement.getAttribute('data-url') || '';
            const snippetTr = cardElement.getAttribute('data-snippet-tr') || cardElement.querySelector('.snippet')?.textContent || '';
            const snippetFr = cardElement.getAttribute('data-snippet-fr') || snippetTr;
            const isCcift = cardElement.getAttribute('data-ccift') === 'true';
            const isNoFrench = cardElement.getAttribute('data-no-french') === 'true';
            const score = cardElement.getAttribute('data-score') || '85';
            const source = cardElement.getAttribute('data-source') || 'Bilateral Scanner';
            const tagsTr = cardElement.getAttribute('data-tags-tr') || '';

            const track = cardElement.getAttribute('data-track') || detectTrackForJob(company, titleTr, tagsTr, isCcift);
            const regInfo = getRegistryInfo(company);

            State.currentJob = {
                id,
                titleTr,
                titleFr,
                company,
                location,
                url: regInfo?.ats || url,
                careerPortal: regInfo?.portal || url,
                hrEmail: regInfo?.hr_email || '',
                snippetTr,
                snippetFr,
                isCcift,
                isNoFrench,
                score,
                source,
                track: track === 'autre' ? (regInfo?.voie || 'autre') : track
            };
            State.currentTrack = State.currentJob.track;

            this.render();
            this.show();
        },

        render() {
            const job = State.currentJob;
            if (!job) return;

            const lang = State.lang;
            const ecusson = VOIE_ECUSSONS[job.track] || VOIE_ECUSSONS["autre"];

            // Écusson officiel
            const ecussonEl = document.getElementById('bld-drawer-ecusson');
            if (ecussonEl) {
                ecussonEl.className = 'ecusson-card-header ' + ecusson.cssClass;
                ecussonEl.innerHTML = `
                    <div class="ecusson-header-title">${lang === 'tr' ? ecusson.title_tr : ecusson.title_fr}</div>
                    <div class="ecusson-header-sub">${lang === 'tr' ? ecusson.sub_tr : ecusson.sub_fr}</div>
                `;
            }

            // Titre & Société
            const titleEl = document.getElementById('bld-drawer-title');
            if (titleEl) titleEl.textContent = lang === 'tr' ? job.titleTr : job.titleFr;

            const compLocEl = document.getElementById('bld-drawer-company-loc');
            if (compLocEl) compLocEl.textContent = `🏢 ${job.company}  |  📍 ${job.location}`;

            // Badges
            const scoreEl = document.getElementById('bld-drawer-score');
            if (scoreEl) scoreEl.textContent = `${lang === 'tr' ? 'Uygunluk: %' : 'Score : %'}${job.score}`;

            const langBadgeEl = document.getElementById('bld-drawer-lang-badge');
            if (langBadgeEl) {
                if (job.isNoFrench) {
                    langBadgeEl.className = 'val-val tag-no-french';
                    langBadgeEl.textContent = lang === 'tr' ? '🇬🇧 Fransızca Şart Değil' : '🇬🇧 Français Non Requis';
                } else {
                    langBadgeEl.className = 'val-val tag-french-req';
                    langBadgeEl.textContent = lang === 'tr' ? '🗣️ Fransızca B2+ Gerekli' : '🗣️ Français B2+ Requis';
                }
            }

            const sourceEl = document.getElementById('bld-drawer-source');
            if (sourceEl) sourceEl.textContent = job.source;

            // Coordonnées RH
            const hrBoxEl = document.getElementById('bld-drawer-hr-box');
            const hrEmailLink = document.getElementById('bld-drawer-hr-email');
            if (hrBoxEl && hrEmailLink) {
                if (job.hrEmail) {
                    hrBoxEl.style.display = 'block';
                    hrEmailLink.textContent = job.hrEmail;
                    hrEmailLink.href = 'mailto:' + job.hrEmail;
                } else {
                    hrBoxEl.style.display = 'none';
                }
            }

            const portalLink = document.getElementById('bld-drawer-portal-link');
            if (portalLink) portalLink.href = job.careerPortal;

            // Description
            const snippetEl = document.getElementById('bld-drawer-snippet');
            if (snippetEl) snippetEl.textContent = lang === 'tr' ? job.snippetTr : job.snippetFr;

            // Bouton ATS externe
            const atsBtn = document.getElementById('bld-drawer-ats-btn');
            if (atsBtn) atsBtn.href = job.url;

            // Fiche Visa étape par étape
            this.renderTimeline(job.track, lang);
        },

        setLanguage(lang) {
            State.lang = lang;
            if (State.currentJob) {
                this.render();
            }
        },

        renderTimeline(track, lang = 'tr') {
            const timelineEl = document.getElementById('bld-drawer-timeline');
            if (!timelineEl) return;

            if (track === 'voie_1') {
                timelineEl.innerHTML = (lang === 'fr') ? `
                    <div class="timeline-step">
                        <div class="timeline-num">1</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Nomination & Engagement Officiel</div>
                            <div class="timeline-desc">Notification d'engagement délivrée par l'Organisation (Conseil de l'Europe, OCDE, UNESCO). Le quota de la Turquie (membre fondateur) s'applique.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">2</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Note Verbale & Instruction MEAE</div>
                            <div class="timeline-desc">Le département juridique notifie le Protocole du Ministère des Affaires Étrangères (MEAE) pour instruction prioritaire auprès des Consulats en Turquie.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">3</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Visa Protocolaire Gratuit (72h - 5 jours)</div>
                            <div class="timeline-desc">Le Consulat Général de France à Istanbul ou l'Ambassade à Ankara délivre le visa de courtoisie sans frais et sans démarche de droit commun.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">4</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Titre Spécial MEAE & Installation</div>
                            <div class="timeline-desc">Délivrance directe du Titre de Séjour Spécial à l'arrivée. Traitement net d'impôt, indemnités d'expatriation et déménagement pris en charge à 100%.</div>
                        </div>
                    </div>
                ` : `
                    <div class="timeline-step">
                        <div class="timeline-num">1</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Resmi Görevlendirme Mektubu (Nomination Officielle)</div>
                            <div class="timeline-desc">Avrupa Konseyi, OECD, UNESCO veya INTERPOL Genel Sekreterliği'nden atama bildirimi iletilir. Türkiye'nin tam üyelik kotası devreye girer.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">2</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Dışişleri Bakanlığı (MEAE) Protokol Talimatı</div>
                            <div class="timeline-desc">Kurumun Ayrıcalıklar Dairesi Fransa Dışişleri Bakanlığı Protokol Şefliği'ne resmi bildirimde bulunarak Türkiye'deki Fransız Konsolosluğu'na talimat gönderir.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">3</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Konsolosluktan Öncelikli Protokol Vizesi</div>
                            <div class="timeline-desc">Ankara Büyükelçiliği veya İstanbul Başkonsolosluğu'ndan harçsız diplomatik/protokol vizesi düzenlenir. Klasik çalışma izni aranmaz.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">4</div>
                        <div class="timeline-content">
                            <div class="timeline-title">MEAE Özel Diplomatik Oturma Kartı (Titre Spécial)</div>
                            <div class="timeline-desc">Fransa'ya varışta doğrudan Dışişleri Bakanlığı Protokol Şefliği'nden "Titre de Séjour Spécial" teslim alınır. Gelir vergisi muafiyeti ve taşınma paketi sağlanır.</div>
                        </div>
                    </div>
                `;
            } else if (track === 'voie_2') {
                timelineEl.innerHTML = (lang === 'fr') ? `
                    <div class="timeline-step">
                        <div class="timeline-num">1</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Avenant de Mobilité Intra-Groupe (ICT)</div>
                            <div class="timeline-desc">Convention de détachement établie entre le siège en Turquie et la filiale française (Beko, THY, Ekol, Barsan, Şişecam). Ancienneté minimale 3 à 6 mois.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">2</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Convention Bilatérale 1972 & Dossier Cerfa</div>
                            <div class="timeline-desc">Application de la convention bilatérale de sécurité sociale et formalités Cerfa. Exonération totale du test du marché du travail (opposabilité de l'emploi).</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">3</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Dépôt Consulaire VFS Global (10 - 15 Jours)</div>
                            <div class="timeline-desc">Dépôt du dossier au centre VFS (Istanbul, Ankara ou Izmir). Traitement accéléré grâce à l'agrément bilatéral CCIFT / DEİK.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">4</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Arrivée en France & Validation ANEF</div>
                            <div class="timeline-desc">Validation en ligne du visa de long séjour valant titre de séjour (VLS-TS ICT). Droit de travail direct pour le conjoint accompagnant.</div>
                        </div>
                    </div>
                ` : `
                    <div class="timeline-step">
                        <div class="timeline-num">1</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Şirket İçi Görevlendirme Protokolü (Avenant ICT)</div>
                            <div class="timeline-desc">Türkiye genel merkezi ile Fransa'daki tüzel kişilik arasında şirket içi transfer sözleşmesi düzenlenir. (Grup bünyesinde en az 3-6 aylık kıdem yeterlidir).</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">2</div>
                        <div class="timeline-content">
                            <div class="timeline-title">1972 İkili Anlaşması & ICT Cerfa Dosyası</div>
                            <div class="timeline-desc">Fransa-Türkiye İkili Sosyal Güvenlik Anlaşması ve Cerfa formu hazırlanır. Yerel iş piyasası araştırması (opposabilité de l'emploi) kısıtlamasından muaftır.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">3</div>
                        <div class="timeline-content">
                            <div class="timeline-title">VFS Global Konsolosluk Randevusu (10-15 Gün)</div>
                            <div class="timeline-desc">İstanbul (Harbiye/Altunizade), Ankara veya İzmir VFS Global merkezine başvuru teslim edilir. CCIFT/DEİK üyesi referansıyla 10-15 iş gününde vize sonuçlanır.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">4</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Fransa'ya Varış & ANEF Kaydı</div>
                            <div class="timeline-desc">Fransa'ya giriş sonrasında online ANEF portalından ICT oturum kartı doğrulanır. Aile bireyleri de refakatçi oturumuyla Fransa'ya yerleşir.</div>
                        </div>
                    </div>
                `;
            } else if (track === 'voie_3') {
                timelineEl.innerHTML = (lang === 'fr') ? `
                    <div class="timeline-step">
                        <div class="timeline-num">1</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Contrat de Travail & Promesse d'Embauche</div>
                            <div class="timeline-desc">Signature de l'offre auprès de la scale-up parisienne avec rémunération brute annuelle ≥ 2x SMIC légal. Équipe technique 100% anglophone.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">2</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Statut Entreprise Innovante & Dossier ANEF</div>
                            <div class="timeline-desc">Validation via le statut JEI / French Tech. Aucune obligation de français et dispense de publication Pôle Emploi.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">3</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Dépôt Consulaire VFS "Passeport Talent"</div>
                            <div class="timeline-desc">Dépôt du formulaire VLS-TS Passeport Talent dans les centres VFS en Turquie. Instruction rapide sous 15 jours ouvrés.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">4</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Titre Pluriannuel 4 Ans & Travail Conjoint</div>
                            <div class="timeline-desc">Octroi direct d'une carte de séjour pluriannuelle de 4 ans renouvelable. Plein droit d'exercice professionnel immédiat pour le conjoint.</div>
                        </div>
                    </div>
                ` : `
                    <div class="timeline-step">
                        <div class="timeline-num">1</div>
                        <div class="timeline-content">
                            <div class="timeline-title">İş Teklifi & Promesse d'Embauche (Maaş ≥ 2x SMIC)</div>
                            <div class="timeline-desc">Paris scale-up girişimi tarafından yıllık brüt maaşı yasal eşiğin (en az 2x SMIC) üzerinde olan iş sözleşmesi imzalanır. Şirket içi çalışma dili %100 İngilizcedir.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">2</div>
                        <div class="timeline-content">
                            <div class="timeline-title">French Tech Akreditasyonu & ANEF Ön Dosyası</div>
                            <div class="timeline-desc">Şirketin Jeune Entreprise Innovante (JEI) veya French Tech statüsüyle ANEF üzerinden ön onay dosyası oluşturulur. Fransızca şartı ve Pôle Emploi ilanı aranmaz.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">3</div>
                        <div class="timeline-content">
                            <div class="timeline-title">VFS Global "Passeport Talent" Başvurusu</div>
                            <div class="timeline-desc">VLS-TS Passeport Talent (Entreprise Innovante) başvurusu Türkiye VFS merkezlerine teslim edilir. İşlem süresi ortalama 15-20 gündür.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">4</div>
                        <div class="timeline-content">
                            <div class="timeline-title">4 Yıllık Oturum & Eşe Tam Çalışma Hakkı</div>
                            <div class="timeline-desc">Fransa'da doğrudan 4 yıllık yenilenebilir oturum kartı alınır. Eşiniz otomatik olarak tam çalışma iznine sahip olur.</div>
                        </div>
                    </div>
                `;
            } else {
                timelineEl.innerHTML = (lang === 'fr') ? `
                    <div class="timeline-step">
                        <div class="timeline-num">1</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Contrat de Travail (CDI / CDD)</div>
                            <div class="timeline-desc">Finalisation des conditions d'embauche avec l'entreprise établie en France.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">2</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Autorisation de Travail ANEF (DREETS)</div>
                            <div class="timeline-desc">L'employeur dépose la demande d'autorisation de travail pour salarié étranger sur le portail dématérialisé ANEF.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">3</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Dépôt Visa VLS-TS au Centre VFS</div>
                            <div class="timeline-desc">Dépôt consulaire auprès de VFS Global en Turquie avec l'attestation ministérielle d'autorisation de travail.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">4</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Validation OFII & Installation</div>
                            <div class="timeline-desc">Validation en ligne de la vignette OFII sur le site de l'ANEF dans les 3 mois suivant l'entrée en France.</div>
                        </div>
                    </div>
                ` : `
                    <div class="timeline-step">
                        <div class="timeline-num">1</div>
                        <div class="timeline-content">
                            <div class="timeline-title">İş Sözleşmesi (CDI / CDD)</div>
                            <div class="timeline-desc">Fransız işveren ile çalışma şartları belirlenir ve iş sözleşmesi parafe edilir.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">2</div>
                        <div class="timeline-content">
                            <div class="timeline-title">Çalışma İzni Başvurusu (DREETS / ANEF)</div>
                            <div class="timeline-desc">İşveren Fransa İçişleri Bakanlığı portalından yabancı çalışan için resmi çalışma izni onayını alır.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">3</div>
                        <div class="timeline-content">
                            <div class="timeline-title">VFS Global VLS-TS Başvurusu</div>
                            <div class="timeline-desc">Onaylanan izin belgesiyle Türkiye'deki VFS Global merkezine uzun süreli çalışma vizesi başvurusu yapılır.</div>
                        </div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-num">4</div>
                        <div class="timeline-content">
                            <div class="timeline-title">OFII Doğrulaması & İkamet</div>
                            <div class="timeline-desc">Fransa'ya giriş sonrası 3 ay içinde ANEF sistemi üzerinden vize doğrulanır.</div>
                        </div>
                    </div>
                `;
            }
        },

        show() {
            const overlay = document.getElementById('bld-drawer-overlay');
            const drawer = document.getElementById('bld-drawer');
            if (overlay) overlay.classList.add('open');
            if (drawer) drawer.classList.add('open');
            document.body.style.overflow = 'hidden';
        },

        close() {
            const overlay = document.getElementById('bld-drawer-overlay');
            const drawer = document.getElementById('bld-drawer');
            if (overlay) overlay.classList.remove('open');
            if (drawer) drawer.classList.remove('open');
            document.body.style.overflow = '';
        },

        copyEmail() {
            if (State.currentJob?.hrEmail) {
                navigator.clipboard.writeText(State.currentJob.hrEmail).then(() => {
                    Toast.show(`✓ İK e-posta adresi kopyalandı : ${State.currentJob.hrEmail}`);
                });
            }
        }
    };

    // --------------------------------------------------------------------------
    // 5. GÉNÉRATEUR INTELLIGENT DE LETTRE & PITCH (TR ➔ FR)
    // --------------------------------------------------------------------------
    const CoverLetterGenerator = {
        open(jobIdOrCard) {
            if (jobIdOrCard !== undefined && jobIdOrCard !== null) {
                if (typeof jobIdOrCard === 'object' && jobIdOrCard.nodeType) {
                    BilateralDrawer.openFromCard(jobIdOrCard);
                    BilateralDrawer.close();
                } else if (typeof jobIdOrCard === 'number' || typeof jobIdOrCard === 'string') {
                    const card = document.querySelector(`.job-card[data-id="${jobIdOrCard}"]`);
                    if (card) {
                        BilateralDrawer.openFromCard(card);
                        BilateralDrawer.close();
                    }
                }
            }

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

            const targetJobLabel = document.getElementById('bld-gen-target-job');
            if (targetJobLabel) {
                targetJobLabel.textContent = `Hedef İlan : ${State.currentJob.titleFr || State.currentJob.titleTr} – ${State.currentJob.company}`;
            }

            const overlay = document.getElementById('bld-gen-modal-overlay');
            if (overlay) overlay.classList.add('open');
            document.body.style.overflow = 'hidden';

            this.updatePreview();
        },

        close() {
            const overlay = document.getElementById('bld-gen-modal-overlay');
            if (overlay) overlay.classList.remove('open');
            document.body.style.overflow = '';
        },

        setTab(tab) {
            State.generatorTab = tab;
            const btnEmail = document.getElementById('bld-tab-email-btn');
            const btnLetter = document.getElementById('bld-tab-letter-btn');
            if (btnEmail) btnEmail.classList.toggle('active', tab === 'email');
            if (btnLetter) btnLetter.classList.toggle('active', tab === 'letter');
            this.updatePreview();
        },

        setVoie(voieKey) {
            State.currentTrack = voieKey;
            ['voie_1', 'voie_2', 'voie_3', 'autre'].forEach(k => {
                const btn = document.getElementById(`bld-btn-voie-${k}`);
                if (btn) btn.classList.toggle('active', k === voieKey);
            });

            // Mise à jour de l'Écusson dans la modale
            const ecusson = VOIE_ECUSSONS[voieKey] || VOIE_ECUSSONS["autre"];
            const ecussonEl = document.getElementById('bld-gen-modal-ecusson');
            if (ecussonEl) {
                ecussonEl.className = 'ecusson-card-header ' + ecusson.cssClass;
                ecussonEl.innerHTML = `
                    <div class="ecusson-header-title">${ecusson.title_fr}</div>
                    <div class="ecusson-header-sub">Le 1er paragraphe de la lettre rappelle expressément cette voie juridique au recruteur.</div>
                `;
            }

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
        },

        copy() {
            const previewEl = document.getElementById('bld-gen-preview');
            const text = previewEl?.textContent || "";
            if (!text) return;

            navigator.clipboard.writeText(text).then(() => {
                Toast.show("✓ Metin panoya başarıyla kopyalandı! / Texte copié avec succès !");
                const btn = document.getElementById('bld-copy-btn');
                if (btn) {
                    const orig = btn.textContent;
                    btn.textContent = "✓ Kopyalandı / Copié !";
                    setTimeout(() => { btn.textContent = orig; }, 2000);
                }
            }).catch(() => {
                // Fallback
                const ta = document.createElement('textarea');
                ta.value = text;
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
                Toast.show("✓ Metin panoya kopyalandı !");
            });
        },

        download() {
            const previewEl = document.getElementById('bld-gen-preview');
            const text = previewEl?.textContent || "";
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
            URL.revokeObjectURL(url);
            Toast.show(`✓ Dosya indirildi : ${filename}`);
        }
    };

    // --------------------------------------------------------------------------
    // 6. GUIDE BILINGUE PRATIQUE DE L'EXPATRIATION (MODAL & ONGLETS)
    // --------------------------------------------------------------------------
    const MobilityGuide = {
        open() {
            const overlay = document.getElementById('bld-guide-modal-overlay');
            if (overlay) overlay.classList.add('open');
            document.body.style.overflow = 'hidden';
            this.setTab('visas');
        },

        close() {
            const overlay = document.getElementById('bld-guide-modal-overlay');
            if (overlay) overlay.classList.remove('open');
            document.body.style.overflow = '';
        },

        setTab(tab) {
            const btnVisas = document.getElementById('bld-guide-tab-visas-btn');
            const btnCv = document.getElementById('bld-guide-tab-cv-btn');
            const contentVisas = document.getElementById('bld-guide-content-visas');
            const contentCv = document.getElementById('bld-guide-content-cv');

            if (btnVisas) btnVisas.classList.toggle('active', tab === 'visas');
            if (btnCv) btnCv.classList.toggle('active', tab === 'cv');
            if (contentVisas) contentVisas.style.display = tab === 'visas' ? 'block' : 'none';
            if (contentCv) contentCv.style.display = tab === 'cv' ? 'block' : 'none';
        }
    };

    // --------------------------------------------------------------------------
    // 7. TOAST NOTIFICATION SERVICE
    // --------------------------------------------------------------------------
    const Toast = {
        show(msg) {
            let toastEl = document.getElementById('bld-toast-notification');
            if (!toastEl) {
                toastEl = document.createElement('div');
                toastEl.id = 'bld-toast-notification';
                toastEl.className = 'bld-toast';
                document.body.appendChild(toastEl);
            }
            toastEl.textContent = msg;
            toastEl.classList.add('show');
            setTimeout(() => {
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
    window.addEventListener('languageChanged', (e) => {
        const newLang = (e && e.detail && e.detail.lang) || localStorage.getItem('bilateral_lang') || 'tr';
        State.lang = newLang;
        if (State.currentJob) {
            BilateralDrawer.render();
        }
    });

    // Fermeture par touche ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            BilateralDrawer.close();
            CoverLetterGenerator.close();
            MobilityGuide.close();
        }
    });

})(window, document);
