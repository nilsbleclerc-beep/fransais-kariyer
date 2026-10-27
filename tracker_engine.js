/**
 * ==============================================================================
 * BILATERAL FRANCE-TURKEY CAREER ENGINE & APPLICATION TRACKER (VANILLA JS ES6+)
 * ------------------------------------------------------------------------------
 * Moteur JavaScript Réactif, Persistance LocalStorage, Multi-Facettes & Kanban
 * Intègre les 3 Voies Prioritaires (KAPI 1 / 2 / 3), le Tri dynamique et
 * les 7 Domaines d'Activité.
 * Aucune dépendance externe - Prêt pour l'intégration web et superviseur RH.
 * ==============================================================================
 */

(function (window) {
    'use strict';

    // --------------------------------------------------------------------------
    // 1. DICTIONNAIRES BILINGUES (TR / FR) & TRADUCTIONS
    // --------------------------------------------------------------------------
    const I18N_DICTIONARY = {
        tr: {
            // Navigation
            tabExplore: "Keşfet & İlanlar",
            tabTracker: "Başvuru Takibi (Kanban)",
            tabGuide: "Rehber, Vize & Belgeler",
            
            // Header
            title: "🇹🇷 Türkiye'den Fransa'ya Vize & Relokasyon Destekli İş Fırsatları 🇫🇷",
            subtitle: "Türkiye'de ikamet eden adayların başvurusuna açık, vize/relokasyon sağlayan veya uluslararası statü veren resmi kurumlar ve Türk şirketleri.",
            
            // 3 Portes Prioritaires
            tracksTitle: "🚪 3 ÖNCELİKLİ YASAL İSTİHDAM KAPISI (VİZE / RELOKASYON) :",
            trackAll: "Tüm Kapılar",
            track1: "KAPI 1: Uluslararası Kurumlar",
            track2: "KAPI 2: Türk Holdingleri (ICT)",
            track3: "KAPI 3: Yetenek Pasaportu (Tech)",
            
            badgeTrack1: "🏛️ KAPI 1: Uluslararası Kurum (MEAE Diplomatik Statü)",
            badgeTrack2: "🏢 KAPI 2: Türk Holdingi (Şirket İçi Transfer ICT)",
            badgeTrack3: "🚀 KAPI 3: Tech Scale-up (Passeport Talent - %100 İngilizce)",

            // Domaines d'Activité
            domainLabel: "📂 Uzmanlık Alanı :",
            domainAll: "🌐 Tüm Alanlar",
            domainIt: "💻 IT, Yazılım & AI",
            domainLogistics: "📦 Lojistik & Taşımacılık",
            domainSales: "💼 Satış & İhracat",
            domainLegal: "⚖️ Hukuk & Uluslararası İlişkiler",
            domainMedia: "🗣️ Çeviri & Medya",
            domainHr: "👥 İK & Yönetim",
            domainCraft: "🛠️ Zanaat & Saha İşleri",

            // Tri
            sortLabel: "🔄 Sıralama :",
            sortScore: "🎯 En Yüksek Uygunluk (Azalan)",
            sortDate: "📅 En Yeni İlanlar (Tarih)",
            sortCompany: "🏢 Şirket Adı (A-Z)",

            // Stats Explorer
            statTotal: "Toplam Fırsat",
            statCcift: "🤝 CCIFT & DEİK Akredite Üye",
            statNoFrench: "✅ Fransızca Şart Değil",
            statReloc: "✈️ Vize / Relokasyon Sağlanan",
            
            // CCIFT Encart
            cciftBoxTitle: "🤝 CCIFT & DEİK RESMİ İKİLİ TİCARET ÜYELERİ (EN YÜKSEK VİZE ONAYI)",
            cciftQuickBtn: "Bu Üyelerin İlanlarını Filtrele (1-Tık) 🎯",
            cciftBoxText: `Aşağıda altın rozetle işaretlenen şirketler, <strong>Fransız-Türk Ticaret Odası (CCIFT)</strong> ve <strong>DEİK Türkiye-Fransa İş Konseyi</strong>'nin resmi üye holdingleridir (<em>Beko France, Turkish Airlines, Ekol, Barsan, Şişecam, Vestel, Sabancı, Eczacıbaşı vb.</em>). Bu kurumlar, Fransa ile resmi ikili protokol ve anlaşmalara sahip olup, Türkiye'den personel transferinde <strong>Şirket İçi Transfer (ICT)</strong> ve <strong>Yetenek Pasaportu (Passeport Talent)</strong> vizelerinde en yüksek onay oranına ve en hızlı prosedürlere sahiptir.`,
            
            // Advice Box
            adviceTitle: "💡 Türkiye'deki Adaylar İçin Vize ve Dil Rehberi:",
            adviceText: `<strong>Fransızca bilmiyorsanız endişelenmeyin :</strong> Yeşil etiketli ilanlarda çalışma dili <strong>İngilizce veya Türkçe</strong>dir (Fransızca şart değildir veya temel A1 yeterlidir). Türkiye'den vizesiz başvuru yaparken en güçlü kapılar : <strong>1)</strong> Yukarıdaki <strong>CCIFT & DEİK üyesi holdingler</strong> (Şirket İçi Transfer ICT vizesi). <strong>2)</strong> Türkiye'nin üyesi olduğu uluslararası kuruluşlar (<em>Avrupa Konseyi, OECD, UNESCO</em> - özel diplomatik/uluslararası memur statüsü verilir). <strong>3)</strong> Paris merkezli scale-up'lar (%100 İngilizce Tech kadroları).`,
            
            // Search & Filters
            searchPlaceholder: "🔍 Pozisyon, şehir (Paris, Lyon, Strazburg...), kurum (OECD, Beko, THY, Ekol...) ara...",
            filterCatAll: "Tüm Kategoriler",
            filterCatCcift: "🤝 CCIFT & DEİK Üyeleri",
            filterCatNoFrench: "✅ Fransızca Şart Değil",
            filterCatInstitutions: "🏛️ Uluslararası Kurumlar",
            filterCatCompanies: "🏢 Türk Holdingleri",
            filterCatLogistics: "📦 Lojistik & Ticaret",
            filterCatTech: "🚀 Tech & Scale-ups",
            filterCatPme: "🏪 KOBİ & Saha",
            filterFavOnly: "⭐ Sadece Favoriler",
            filterTrackedOnly: "📋 Takip Edilenler",
            filterReset: "Filtreleri Sıfırla 🔄",
            resultsCount: "toplam <strong>{total}</strong> fırsattan <strong>{visible}</strong> tanesi listeleniyor",
            noResults: "Arama kriterlerinize uygun ilan bulunamadı. Lütfen filtreleri sıfırlamayı deneyin.",
            
            // Card details
            applyBtn: "İlanı İncele / Başvur ↗",
            hrBtn: "Resmi Portalı ↗",
            scorePrefix: "Uygunluk: ",
            trackAddBtn: "Takibe Ekle",
            trackedBtn: "Takipte",
            statusLabel: "Durum:",
            
            // Pipeline Kanban
            trackerTitle: "📋 Başvuru ve Adaylık Takip Hattı (Pipeline)",
            trackerSubtitle: "Fransa'daki başvurularınızı adım adım yönetin, mülakat tarihlerini ve kişisel notlarınızı kaydedin.",
            trackerSearchPlaceholder: "🔍 Takip edilen başvurularda ara...",
            exportJsonBtn: "📥 JSON Dışa Aktar",
            exportCsvBtn: "📊 CSV Dışa Aktar (Superviseur FR)",
            clearTrackerBtn: "🗑️ Listeyi Temizle",
            clearTrackerConfirm: "Tüm takip edilen başvuruları silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.",
            
            colSavedTitle: "Kaydedildi / Hedef",
            colSavedDesc: "Başvurulmak üzere seçilen ilanlar",
            colAppliedTitle: "Başvuruldu",
            colAppliedDesc: "CV/Dosya gönderildi, yanıt bekleniyor",
            colInterviewTitle: "Mülakat Aşamasında",
            colInterviewDesc: "İK veya teknik mülakat planlandı",
            colOfferTitle: "Kabul / Teklif Alındı",
            colOfferDesc: "Teklif geldi veya vize süreci başladı",
            
            emptyColumn: "Bu aşamada henüz başvuru yok.",
            emptyTrackerAll: "Henüz takibe alınmış bir başvuru yok. İlanlar sekmesinden 'Takibe Ekle' butonuna basarak ekleyebilirsiniz.",
            goToExploreBtn: "🔍 İlanları Keşfetmeye Başla",
            
            // Modal
            modalTitle: "Başvuru Detaylarını Düzenle",
            modalFieldStatus: "Aşama / Durum:",
            modalFieldDateApplied: "Başvuru Tarihi:",
            modalFieldDateInterview: "Mülakat Tarihi:",
            modalFieldNotes: "Kişisel Notlar (Görüşülen kişi, maaş beklentisi, başvuru kanalı):",
            modalNotesPlaceholder: "Örn: LinkedIn üzerinden İK Müdürü ile iletişime geçildi, İngilizce CV gönderildi...",
            modalBtnSave: "Kaydet",
            modalBtnCancel: "İptal",
            modalBtnDelete: "Takibi Bırak",

            // Kanban tactile & favoris (accessibilité)
            kanbanMoveLabel: "Durum",
            kanbanBadgeNoFrench: "✅ Fransızca Gerekmez",
            favAddLabel: "Favorilere Ekle",
            favRemoveLabel: "Favorilerden Çıkar",
            toastLangChanged: "Dil Türkçe olarak güncellendi 🇹🇷",
            
            // Toasts
            toastFavAdded: "⭐ İlan favorilere eklendi.",
            toastFavRemoved: "İlan favorilerden çıkarıldı.",
            toastTrackAdded: "📋 İlan başvuru takibine eklendi.",
            toastTrackUpdated: "Başvuru bilgileri güncellendi.",
            toastTrackDeleted: "Başvuru takip listesinden kaldırıldı.",
            toastTrackerCleared: "Takip listesi temizlendi.",
            toastExportCsv: "📊 CSV dosyası indirildi (journal_candidatures_france.csv)",
            toastExportJson: "📥 JSON dosyası indirildi (journal_candidatures_france.json)",
            toastCopied: "📋 Metin panoya kopyalandı!",
            
            // Guide & Tools
            guideTitle: "📘 Fransa İstihdam, Vize & Başvuru Rehberi",
            guideSubtitle: "Türkiye'den Fransa'ya transfer süreçleri, vize prosedürleri ve hazır başvuru şablonları.",
            checklistTitle: "✅ Başvuru Öncesi İnteraktif Kontrol Listesi (Checklist)",
            templatesTitle: "✉️ Hazır E-posta & Motivasyon Mektubu Şablonları",
            officialLinksTitle: "🌐 Resmi Kurumlar & Vize Portalları"
        },
        fr: {
            // Navigation
            tabExplore: "Explorer les Offres",
            tabTracker: "Suivi Candidatures (Kanban)",
            tabGuide: "Guide Visa & Outils",
            
            // Header
            title: "🇹🇷 Opportunités d'Emploi en France avec Visa / Relocalisation depuis la Turquie 🇫🇷",
            subtitle: "Offres ouvertes aux candidats résidant en Turquie sans visa préalable (organisations internationales et multinationales turques).",
            
            // 3 Portes Prioritaires
            tracksTitle: "🚪 LES 3 PORTES D'ACCÈS PRIORITAIRES (VISA / RELOCALISATION) :",
            trackAll: "Toutes les Voies",
            track1: "VOIE 1 : Institutions Internationales",
            track2: "VOIE 2 : Multinationales Turques (ICT)",
            track3: "VOIE 3 : Passeport Talent (Tech)",
            
            badgeTrack1: "🏛️ VOIE 1 : Institution Internationale (Statut Spécial MEAE)",
            badgeTrack2: "🏢 VOIE 2 : Multinationale Turque (Salarié Détaché ICT)",
            badgeTrack3: "🚀 VOIE 3 : Tech Scale-up (Passeport Talent - 100% Anglais)",

            // Domaines d'Activité
            domainLabel: "📂 Domaine d'activité :",
            domainAll: "🌐 Tous les domaines",
            domainIt: "💻 IT, Logiciel & IA",
            domainLogistics: "📦 Logistique & Transport",
            domainSales: "💼 Vente, Export & Marketing",
            domainLegal: "⚖️ Droit & Relations Internationales",
            domainMedia: "🗣️ Traduction & Médias",
            domainHr: "👥 RH & Administration",
            domainCraft: "🛠️ Métiers de Terrain & PME",

            // Tri
            sortLabel: "🔄 Trier par :",
            sortScore: "🎯 Score de Pertinence (Décroissant)",
            sortDate: "📅 Date de Publication (Plus Récent)",
            sortCompany: "🏢 Entreprise (A-Z)",

            // Stats Explorer
            statTotal: "Total Opportunités",
            statCcift: "🤝 Membres CCIFT & DEİK",
            statNoFrench: "✅ Sans Français Obligatoire",
            statReloc: "✈️ Visa / Relocalisation",
            
            // CCIFT Encart
            cciftBoxTitle: "🤝 MEMBRES OFFICIELS CCIFT & DEİK (TAUX DE VISA MAXIMAL)",
            cciftQuickBtn: "Filtrer les Offres de ces Membres (1-Clic) 🎯",
            cciftBoxText: `Les entreprises identifiées par le ruban doré sont membres de la <strong>Chambre de Commerce Franco-Turque (CCIFT)</strong> et du <strong>Conseil d'affaires DEİK Turquie-France</strong> (<em>Beko France, Turkish Airlines, Ekol, Barsan, Şişecam, Vestel, Sabancı, Eczacıbaşı...</em>). Ces groupes bénéficient de partenariats bilatéraux privilégiés facilitant grandement l'octroi des visas de <strong>Salarié Détaché (ICT)</strong> et <strong>Passeport Talent</strong> pour les candidats venant de Turquie.`,
            
            // Advice Box
            adviceTitle: "💡 Guide Visa et Langues pour Candidats en Turquie :",
            adviceText: `<strong>Si vous ne parlez pas français :</strong> les postes avec badge vert ont pour langue de travail l'<strong>Anglais ou le Turc</strong> (français non requis ou niveau A1 toléré). Les portes d'entrée prioritaires sans visa français préalable sont : <strong>1)</strong> Les <strong>groupes membres CCIFT & DEİK</strong> (visa ICT de salarié détaché). <strong>2)</strong> Les organisations internationales dont la Turquie est membre (<em>Conseil de l'Europe, OCDE, UNESCO</em> - titre de séjour spécial MAE délivré). <strong>3)</strong> Les scale-ups tech parisiennes (100% anglais / Passeport Talent).`,
            
            // Search & Filters
            searchPlaceholder: "🔍 Rechercher poste, ville (Paris, Lyon, Strasbourg...), institution (OCDE, Beko, THY...)...",
            filterCatAll: "Toutes Catégories",
            filterCatCcift: "🤝 Membres CCIFT & DEİK",
            filterCatNoFrench: "✅ Français Non Requis",
            filterCatInstitutions: "🏛️ Institutions Internationales",
            filterCatCompanies: "🏢 Multinationales Turques",
            filterCatLogistics: "📦 Logistique & Commerce",
            filterCatTech: "🚀 Tech & Scale-ups",
            filterCatPme: "🏪 PME & Métiers de Terrain",
            filterFavOnly: "⭐ Favoris Uniquement",
            filterTrackedOnly: "📋 Candidatures en Cours",
            filterReset: "Réinitialiser Filtres 🔄",
            resultsCount: "Affichage de <strong>{visible}</strong> offres sur un total de <strong>{total}</strong>",
            noResults: "Aucune offre ne correspond à vos filtres actuels. Veuillez réinitialiser les critères.",
            
            // Card details
            applyBtn: "Voir l'offre / Postuler ↗",
            hrBtn: "Portail Officiel ↗",
            scorePrefix: "Score : ",
            trackAddBtn: "Suivre",
            trackedBtn: "Suivi actif",
            statusLabel: "Statut :",
            
            // Pipeline Kanban
            trackerTitle: "📋 Tableau de Bord & Pipeline de Candidatures",
            trackerSubtitle: "Supervisez vos démarches vers la France : relances, dates d'entretiens et notes de suivi.",
            trackerSearchPlaceholder: "🔍 Filtrer les candidatures suivies...",
            exportJsonBtn: "📥 Exporter JSON",
            exportCsvBtn: "📊 Exporter CSV (Superviseur FR)",
            clearTrackerBtn: "🗑️ Vider le suivi",
            clearTrackerConfirm: "Voulez-vous vraiment supprimer toutes les candidatures suivies ? Cette action est irréversible.",
            
            colSavedTitle: "Enregistré / Cible",
            colSavedDesc: "Offres sélectionnées à postuler",
            colAppliedTitle: "Postulé",
            colAppliedDesc: "Dossier envoyé, attente retour RH",
            colInterviewTitle: "Entretien en Cours",
            colInterviewDesc: "Entretien RH ou technique fixé",
            colOfferTitle: "Offre Reçue / Accord",
            colOfferDesc: "Offre acceptée ou procédure visa lancée",
            
            emptyColumn: "Aucune candidature à cette étape.",
            emptyTrackerAll: "Aucune candidature n'est suivie pour le moment. Cliquez sur 'Suivre' depuis l'onglet des offres.",
            goToExploreBtn: "🔍 Explorer les opportunités",
            
            // Modal
            modalTitle: "Modifier les détails de la candidature",
            modalFieldStatus: "Étape / Statut :",
            modalFieldDateApplied: "Date de candidature :",
            modalFieldDateInterview: "Date d'entretien :",
            modalFieldNotes: "Notes personnelles (Contact RH, prétention salariale, remarques) :",
            modalNotesPlaceholder: "Ex: Prise de contact sur LinkedIn avec le responsable RH, CV en anglais envoyé...",
            modalBtnSave: "Enregistrer",
            modalBtnCancel: "Annuler",
            modalBtnDelete: "Supprimer du suivi",

            // Kanban tactile & favoris (accessibilité)
            kanbanMoveLabel: "Statut",
            kanbanBadgeNoFrench: "✅ Sans Français",
            favAddLabel: "Ajouter aux favoris",
            favRemoveLabel: "Retirer des favoris",
            toastLangChanged: "Langue basculée en Français 🇫🇷",
            
            // Toasts
            toastFavAdded: "⭐ Offre ajoutée aux favoris.",
            toastFavRemoved: "Offre retirée des favoris.",
            toastTrackAdded: "📋 Offre ajoutée au suivi des candidatures.",
            toastTrackUpdated: "Informations de candidature mises à jour.",
            toastTrackDeleted: "Candidature retirée du pipeline.",
            toastTrackerCleared: "Pipeline réinitialisé.",
            toastExportCsv: "📊 Journal CSV téléchargé (journal_candidatures_france.csv)",
            toastExportJson: "📥 Export JSON téléchargé (journal_candidatures_france.json)",
            toastCopied: "📋 Copié dans le presse-papier !",
            
            // Guide & Tools
            guideTitle: "📘 Guide des Démarches, Visas & Outils France",
            guideSubtitle: "Mobilité Turquie-France, accords bilatéraux et modèles prêts à l'emploi.",
            checklistTitle: "✅ Checklist Préparatoire Interactive",
            templatesTitle: "✉️ Modèles de Lettre & Messages d'Approche",
            officialLinksTitle: "🌐 Portails Officiels & Visas"
        }
    };

    // --------------------------------------------------------------------------
    // 2. SERVICE DE PERSISTANCE LOCALSTORAGE
    // --------------------------------------------------------------------------
    const STORAGE_KEYS = {
        FAVORITES: 'france_jobs_favorites_v2',
        APPLICATIONS: 'france_jobs_applications_v2',
        CHECKLIST: 'france_jobs_checklist_v2',
        LANG: 'france_jobs_lang_pref'
    };

    const StorageService = {
        getLang() {
            try {
                return localStorage.getItem(STORAGE_KEYS.LANG) || 'tr';
            } catch (e) {
                return 'tr';
            }
        },
        setLang(lang) {
            try {
                localStorage.setItem(STORAGE_KEYS.LANG, lang);
                // Clé lue par pwa_module.js et drawer_cover_letter_module.js
                localStorage.setItem('bilateral_lang', lang);
            } catch (e) {}
        },

        getFavorites() {
            try {
                const data = localStorage.getItem(STORAGE_KEYS.FAVORITES);
                return data ? new Set(JSON.parse(data)) : new Set();
            } catch (e) {
                console.error("Erreur lecture favoris:", e);
                return new Set();
            }
        },
        saveFavorites(favSet) {
            try {
                localStorage.setItem(STORAGE_KEYS.FAVORITES, JSON.stringify(Array.from(favSet)));
            } catch (e) {
                console.error("Erreur écriture favoris:", e);
            }
        },
        toggleFavorite(jobId) {
            const favs = this.getFavorites();
            let isFav = false;
            const strId = String(jobId);
            if (favs.has(strId)) {
                favs.delete(strId);
                isFav = false;
            } else {
                favs.add(strId);
                isFav = true;
            }
            this.saveFavorites(favs);
            return isFav;
        },

        getApplications() {
            try {
                const data = localStorage.getItem(STORAGE_KEYS.APPLICATIONS);
                return data ? JSON.parse(data) : {};
            } catch (e) {
                console.error("Erreur lecture applications:", e);
                return {};
            }
        },
        saveApplications(apps) {
            try {
                localStorage.setItem(STORAGE_KEYS.APPLICATIONS, JSON.stringify(apps));
            } catch (e) {
                console.error("Erreur écriture applications:", e);
            }
        },
        getApplication(jobId) {
            const apps = this.getApplications();
            return apps[String(jobId)] || null;
        },
        saveApplication(jobId, jobData, status = 'saved', appliedDate = '', interviewDate = '', notes = '') {
            const apps = this.getApplications();
            const strId = String(jobId);
            const now = new Date().toISOString();
            
            const existing = apps[strId] || {};
            apps[strId] = {
                id: strId,
                title: jobData.title || existing.title || '',
                title_fr: jobData.title_fr || existing.title_fr || jobData.title || '',
                company: jobData.company || existing.company || '',
                location: jobData.location || existing.location || '',
                url: jobData.url || existing.url || '',
                source: jobData.source || existing.source || '',
                relevance_score: jobData.relevance_score || existing.relevance_score || 50,
                category: jobData.category || existing.category || '',
                working_language: jobData.working_language || existing.working_language || '',
                visa_sponsorship: jobData.visa_sponsorship || existing.visa_sponsorship || '',
                is_ccift_deik: Boolean(jobData.is_ccift_deik || existing.is_ccift_deik),
                french_required: Boolean(jobData.french_required || existing.french_required),
                track: jobData.track || existing.track || 'autre',
                domain: jobData.domain || existing.domain || 'craft_pme',
                status: status || existing.status || 'saved',
                applied_date: appliedDate !== undefined ? appliedDate : (existing.applied_date || ''),
                interview_date: interviewDate !== undefined ? interviewDate : (existing.interview_date || ''),
                notes: notes !== undefined ? notes : (existing.notes || ''),
                created_at: existing.created_at || now,
                updated_at: now
            };
            this.saveApplications(apps);
            return apps[strId];
        },
        updateApplicationStatus(jobId, newStatus) {
            const apps = this.getApplications();
            const strId = String(jobId);
            if (apps[strId]) {
                apps[strId].status = newStatus;
                apps[strId].updated_at = new Date().toISOString();
                this.saveApplications(apps);
                return apps[strId];
            }
            return null;
        },
        deleteApplication(jobId) {
            const apps = this.getApplications();
            const strId = String(jobId);
            if (apps[strId]) {
                delete apps[strId];
                this.saveApplications(apps);
                return true;
            }
            return false;
        },
        clearAllApplications() {
            try {
                localStorage.removeItem(STORAGE_KEYS.APPLICATIONS);
            } catch (e) {}
        },

        getChecklist() {
            try {
                const data = localStorage.getItem(STORAGE_KEYS.CHECKLIST);
                return data ? JSON.parse(data) : {};
            } catch (e) {
                return {};
            }
        },
        saveChecklistItem(itemId, isChecked) {
            try {
                const checklist = this.getChecklist();
                checklist[itemId] = Boolean(isChecked);
                localStorage.setItem(STORAGE_KEYS.CHECKLIST, JSON.stringify(checklist));
            } catch (e) {}
        }
    };

    // Retour haptique léger (Android) - silencieux si non supporté
    const haptic = (ms = 10) => {
        try {
            if (navigator.vibrate) navigator.vibrate(ms);
        } catch (e) {}
    };

    // --------------------------------------------------------------------------
    // 3. SERVICE TOAST & NOTIFICATIONS
    // --------------------------------------------------------------------------
    const ToastService = {
        show(message, type = 'info', duration = 3200) {
            let container = document.getElementById('toast-container');
            if (!container) {
                container = document.createElement('div');
                container.id = 'toast-container';
                container.className = 'toast-container';
                document.body.appendChild(container);
            }

            const toast = document.createElement('div');
            toast.className = `toast-item toast-${type}`;
            
            let icon = 'ℹ️';
            if (type === 'success') icon = '✅';
            if (type === 'warning') icon = '⚠️';
            if (type === 'star') icon = '⭐';

            toast.innerHTML = `<span class="toast-icon">${icon}</span> <span class="toast-text">${message}</span>`;
            container.appendChild(toast);

            setTimeout(() => {
                toast.classList.add('toast-show');
            }, 10);

            setTimeout(() => {
                toast.classList.remove('toast-show');
                toast.classList.add('toast-hide');
                setTimeout(() => {
                    if (toast.parentNode) toast.parentNode.removeChild(toast);
                }, 300);
            }, duration);
        }
    };

    // --------------------------------------------------------------------------
    // 4. MOTEUR DE RECHERCHE, DE FILTRAGE MULTI-FACETTES & DE TRI
    // --------------------------------------------------------------------------
    const FilterEngine = {
        state: {
            query: '',
            track: 'all', // 'all', 'voie_1', 'voie_2', 'voie_3'
            domain: 'all', // 'all', 'it', 'logistics', 'sales', 'legal_policy', 'media_trans', 'hr_admin', 'craft_pme'
            category: 'all',
            status: 'all', // 'all', 'fav', 'tracked'
            noFrenchOnly: false,
            cciftOnly: false,
            sortBy: 'score_desc' // 'score_desc', 'date_desc', 'company_asc'
        },
        debounceTimer: null,

        init() {
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                searchInput.addEventListener('input', (e) => {
                    clearTimeout(this.debounceTimer);
                    this.debounceTimer = setTimeout(() => {
                        this.state.query = (e.target.value || '').trim();
                        this.apply();
                    }, 220);
                });
            }
        },

        setTrack(trackKey, btn) {
            this.state.track = trackKey;
            document.querySelectorAll('.track-btn').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            this.apply();
        },

        setDomain(domainKey) {
            this.state.domain = domainKey;
            this.apply();
        },

        setSort(sortKey) {
            this.state.sortBy = sortKey;
            this.sortGridCards(sortKey);
            this.apply();
        },

        sortGridCards(sortBy) {
            const grid = document.getElementById('cardsGrid');
            if (!grid) return;
            const cards = Array.from(grid.querySelectorAll('.job-card'));

            cards.sort((a, b) => {
                if (sortBy === 'score_desc') {
                    const scoreA = parseInt(a.getAttribute('data-score') || '0', 10);
                    const scoreB = parseInt(b.getAttribute('data-score') || '0', 10);
                    return scoreB - scoreA;
                }
                if (sortBy === 'date_desc') {
                    const timeA = parseInt(a.getAttribute('data-timestamp') || '0', 10);
                    const timeB = parseInt(b.getAttribute('data-timestamp') || '0', 10);
                    return timeB - timeA;
                }
                if (sortBy === 'company_asc') {
                    const compA = (a.getAttribute('data-company') || '').toLowerCase();
                    const compB = (b.getAttribute('data-company') || '').toLowerCase();
                    return compA.localeCompare(compB);
                }
                return 0;
            });

            // Réinsertion ordonnée dans le DOM
            cards.forEach(card => grid.appendChild(card));
        },

        setCategory(cat) {
            this.state.category = cat;
            this.apply();
        },

        toggleNoFrench() {
            this.state.noFrenchOnly = !this.state.noFrenchOnly;
            this.apply();
        },

        toggleCcift() {
            this.state.cciftOnly = !this.state.cciftOnly;
            this.apply();
        },

        setStatusFilter(status) {
            this.state.status = status;
            this.apply();
        },

        resetAll() {
            this.state.query = '';
            this.state.track = 'all';
            this.state.domain = 'all';
            this.state.category = 'all';
            this.state.status = 'all';
            this.state.noFrenchOnly = false;
            this.state.cciftOnly = false;
            this.state.sortBy = 'score_desc';

            const searchInput = document.getElementById('searchInput');
            if (searchInput) searchInput.value = '';

            const domainSelect = document.getElementById('domainSelect');
            if (domainSelect) domainSelect.value = 'all';

            const sortSelect = document.getElementById('sortSelect');
            if (sortSelect) sortSelect.value = 'score_desc';

            // Reset UI buttons
            document.querySelectorAll('.track-btn').forEach(b => {
                b.classList.remove('active');
                if (b.dataset.track === 'all') b.classList.add('active');
            });

            document.querySelectorAll('.filter-pill-btn').forEach(b => {
                b.classList.remove('active');
                if (b.dataset.filterVal === 'all') b.classList.add('active');
            });
            const noFrenchBtn = document.getElementById('filter-btn-no-french');
            if (noFrenchBtn) noFrenchBtn.classList.remove('active');
            const cciftBtn = document.getElementById('filter-btn-ccift');
            if (cciftBtn) cciftBtn.classList.remove('active');

            this.sortGridCards('score_desc');
            this.apply();
        },

        apply() {
            const cards = document.querySelectorAll('#cardsGrid .job-card');
            const favorites = StorageService.getFavorites();
            const applications = StorageService.getApplications();
            const queryWords = this.state.query.toLowerCase().split(/\s+/).filter(w => w.length > 0);

            let visibleCount = 0;
            let countCcift = 0;
            let countNoFrench = 0;
            let countReloc = 0;

            // Compteurs par Voie Prioritaire
            let trackCounts = { all: 0, voie_1: 0, voie_2: 0, voie_3: 0 };

            cards.forEach(card => {
                const id = card.getAttribute('data-id');
                const catTr = (card.getAttribute('data-category-tr') || '').toLowerCase();
                const catFr = (card.getAttribute('data-category-fr') || '').toLowerCase();
                const searchData = (card.getAttribute('data-search') || '').toLowerCase();
                const isCcift = card.getAttribute('data-ccift') === 'true';
                const isNoFrench = card.getAttribute('data-no-french') === 'true';
                const track = card.getAttribute('data-track') || 'autre';
                const domain = card.getAttribute('data-domain') || 'craft_pme';
                const visaText = (card.getAttribute('data-visa') || '').toLowerCase();
                const hasReloc = visaText.includes('vize') || visaText.includes('visa') || visaText.includes('relokasyon') || visaText.includes('relocalisation') || visaText.includes('diplomatique');

                // 1. Filtrage Voie Prioritaire (KAPI 1 / 2 / 3)
                let matchTrack = (this.state.track === 'all' || track === this.state.track);

                // 2. Filtrage Domaine d'activité
                let matchDomain = (this.state.domain === 'all' || domain === this.state.domain);

                // 3. Catégorie principale
                let matchCat = true;
                if (this.state.category === 'institutions') {
                    matchCat = catTr.includes('kurum') || catFr.includes('institution') || catTr.includes('hukuk') || track === 'voie_1';
                } else if (this.state.category === 'companies') {
                    matchCat = catTr.includes('holding') || catFr.includes('multinationale') || catTr.includes('büyük türk') || track === 'voie_2';
                } else if (this.state.category === 'logistics') {
                    matchCat = catTr.includes('lojistik') || catFr.includes('logistique') || catTr.includes('büro') || catTr.includes('tertiaire') || domain === 'logistics';
                } else if (this.state.category === 'tech') {
                    matchCat = catTr.includes('zeka') || catTr.includes('teknoloji') || catFr.includes('intelligence') || catFr.includes('tech') || catTr.includes('yazılım') || catFr.includes('cloud') || track === 'voie_3' || domain === 'it';
                } else if (this.state.category === 'pme') {
                    matchCat = catTr.includes('kobi') || catFr.includes('pme') || catTr.includes('saha') || catTr.includes('kariyer') || domain === 'craft_pme';
                }

                // 4. Filtres booléens
                let matchNoFrench = !this.state.noFrenchOnly || isNoFrench;
                let matchCcift = !this.state.cciftOnly || isCcift;

                // 5. Statut (Favoris / Takip)
                let matchStatus = true;
                if (this.state.status === 'fav') {
                    matchStatus = favorites.has(String(id));
                } else if (this.state.status === 'tracked') {
                    matchStatus = Boolean(applications[String(id)]);
                }

                // 6. Recherche texte plein champ (tous les mots doivent correspondre)
                let matchQuery = true;
                if (queryWords.length > 0) {
                    matchQuery = queryWords.every(word => searchData.includes(word));
                }

                // Test d'éligibilité globale
                const isVisible = matchTrack && matchDomain && matchCat && matchNoFrench && matchCcift && matchStatus && matchQuery;

                if (isVisible) {
                    card.style.display = 'flex';
                    visibleCount++;
                    if (isCcift) countCcift++;
                    if (isNoFrench) countNoFrench++;
                    if (hasReloc) countReloc++;

                    // Surbrillance des termes
                    this.highlightTerms(card, queryWords);
                } else {
                    card.style.display = 'none';
                }

                // Comptage par voie pour les offres qui passent les autres critères
                if (matchDomain && matchCat && matchNoFrench && matchCcift && matchStatus && matchQuery) {
                    trackCounts.all++;
                    if (track === 'voie_1') trackCounts.voie_1++;
                    if (track === 'voie_2') trackCounts.voie_2++;
                    if (track === 'voie_3') trackCounts.voie_3++;
                }
            });

            // Mise à jour réactive des 4 compteurs statistiques du header
            this.updateStatsCounters(visibleCount, countCcift, countNoFrench, countReloc);

            // Mise à jour des compteurs sur les boutons de voies
            this.updateTrackBadges(trackCounts);

            // Mise à jour du résumé textuel des filtres
            this.updateResultsSummary(visibleCount, cards.length);
        },

        highlightTerms(card, words) {
            const titleEl = card.querySelector('.job-title');
            const snippetEl = card.querySelector('.snippet');
            const companyEl = card.querySelector('.company-name-text');

            [titleEl, snippetEl, companyEl].forEach(el => {
                if (!el) return;
                const originalText = el.getAttribute('data-original-text') || el.textContent;
                if (!el.hasAttribute('data-original-text')) {
                    el.setAttribute('data-original-text', originalText);
                }

                if (words.length === 0) {
                    el.textContent = originalText;
                    return;
                }

                const escapedWords = words.map(w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
                const regex = new RegExp(`(${escapedWords.join('|')})`, 'gi');
                const safeHtml = originalText.replace(regex, '<mark class="search-highlight">$1</mark>');
                el.innerHTML = safeHtml;
            });
        },

        updateStatsCounters(visible, ccift, noFrench, reloc) {
            const elTotal = document.getElementById('stat-total');
            const elCcift = document.getElementById('stat-ccift');
            const elNoFrench = document.getElementById('stat-no-french');
            const elReloc = document.getElementById('stat-reloc');

            if (elTotal) elTotal.textContent = visible;
            if (elCcift) elCcift.textContent = ccift;
            if (elNoFrench) elNoFrench.textContent = noFrench;
            if (elReloc) elReloc.textContent = reloc;
        },

        updateTrackBadges(counts) {
            const bAll = document.getElementById('count-track-all');
            const b1 = document.getElementById('count-track-1');
            const b2 = document.getElementById('count-track-2');
            const b3 = document.getElementById('count-track-3');

            if (bAll) bAll.textContent = counts.all;
            if (b1) b1.textContent = counts.voie_1;
            if (b2) b2.textContent = counts.voie_2;
            if (b3) b3.textContent = counts.voie_3;
        },

        updateResultsSummary(visibleCount, totalCount) {
            const summaryEl = document.getElementById('filter-results-summary');
            const noResultsEl = document.getElementById('no-results-box');
            const lang = StorageService.getLang();
            const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;

            if (summaryEl) {
                summaryEl.innerHTML = dict.resultsCount
                    .replace('{visible}', visibleCount)
                    .replace('{total}', totalCount);
            }

            if (noResultsEl) {
                noResultsEl.style.display = visibleCount === 0 ? 'block' : 'none';
            }
        }
    };

    // --------------------------------------------------------------------------
    // 5. GESTIONNAIRE DU PIPELINE KANBAN (APPLICATION TRACKER)
    // --------------------------------------------------------------------------
    const KanbanTracker = {
        columns: ['saved', 'applied', 'interview', 'offer'],
        searchFilter: '',

        init() {
            this.setupDragAndDrop();
            const searchInput = document.getElementById('trackerSearchInput');
            if (searchInput) {
                searchInput.addEventListener('input', (e) => {
                    this.searchFilter = (e.target.value || '').toLowerCase().trim();
                    this.render();
                });
            }
        },

        setupDragAndDrop() {
            this.columns.forEach(colKey => {
                const colEl = document.getElementById(`kanban-col-${colKey}`);
                if (!colEl) return;

                colEl.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    colEl.classList.add('kanban-col-dragover');
                });

                colEl.addEventListener('dragleave', () => {
                    colEl.classList.remove('kanban-col-dragover');
                });

                colEl.addEventListener('drop', (e) => {
                    e.preventDefault();
                    colEl.classList.remove('kanban-col-dragover');
                    const jobId = e.dataTransfer.getData('text/plain');
                    if (jobId) {
                        this.moveToStatus(jobId, colKey);
                    }
                });
            });
        },

        moveToStatus(jobId, newStatus) {
            const updated = StorageService.updateApplicationStatus(jobId, newStatus);
            if (updated) {
                const lang = StorageService.getLang();
                const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;
                let statusName = newStatus;
                if (newStatus === 'saved') statusName = dict.colSavedTitle;
                if (newStatus === 'applied') statusName = dict.colAppliedTitle;
                if (newStatus === 'interview') statusName = dict.colInterviewTitle;
                if (newStatus === 'offer') statusName = dict.colOfferTitle;

                ToastService.show(`${dict.toastTrackUpdated} ➔ ${statusName}`, 'success');
                haptic();
                this.render();
                UIController.syncExplorerCards();
            }
        },

        advanceStatus(jobId, direction = 1) {
            const app = StorageService.getApplication(jobId);
            if (!app) return;
            const currentIndex = this.columns.indexOf(app.status);
            if (currentIndex === -1) return;
            const newIndex = currentIndex + direction;
            if (newIndex >= 0 && newIndex < this.columns.length) {
                this.moveToStatus(jobId, this.columns[newIndex]);
            }
        },

        render() {
            const applications = StorageService.getApplications();
            const favorites = StorageService.getFavorites();
            const lang = StorageService.getLang();
            const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;

            // Réinitialisation des conteneurs
            const colLists = {};
            const colCounts = { saved: 0, applied: 0, interview: 0, offer: 0 };

            this.columns.forEach(colKey => {
                const container = document.getElementById(`kanban-items-${colKey}`);
                if (container) {
                    container.innerHTML = '';
                    colLists[colKey] = container;
                }
            });

            const allAppsList = Object.values(applications);
            let totalTracked = allAppsList.length;

            // Mise à jour du badge d'onglet
            const badgeTracker = document.getElementById('badge-tracker-count');
            if (badgeTracker) badgeTracker.textContent = totalTracked;

            if (totalTracked === 0) {
                const emptyNotice = document.getElementById('tracker-empty-notice');
                if (emptyNotice) emptyNotice.style.display = 'block';
            } else {
                const emptyNotice = document.getElementById('tracker-empty-notice');
                if (emptyNotice) emptyNotice.style.display = 'none';
            }

            allAppsList.forEach(app => {
                const status = app.status || 'saved';
                colCounts[status] = (colCounts[status] || 0) + 1;

                // Filtrage interne au tracker
                if (this.searchFilter) {
                    const haystack = `${app.title} ${app.title_fr} ${app.company} ${app.location} ${app.notes}`.toLowerCase();
                    if (!haystack.includes(this.searchFilter)) return;
                }

                const container = colLists[status];
                if (!container) return;

                const cardEl = this.createKanbanCardElement(app, favorites.has(String(app.id)), lang, dict);
                container.appendChild(cardEl);
            });

            // Affichage des messages vides par colonne
            this.columns.forEach(colKey => {
                const countBadge = document.getElementById(`count-col-${colKey}`);
                if (countBadge) countBadge.textContent = colCounts[colKey] || 0;

                const container = colLists[colKey];
                if (container && container.children.length === 0) {
                    const emptyMsg = document.createElement('div');
                    emptyMsg.className = 'kanban-empty-slot';
                    emptyMsg.textContent = dict.emptyColumn;
                    container.appendChild(emptyMsg);
                }
            });

            // Mise à jour des stats du haut du Kanban
            const statTotalEl = document.getElementById('tracker-stat-total');
            if (statTotalEl) statTotalEl.textContent = totalTracked;
            const statAppliedEl = document.getElementById('tracker-stat-applied');
            if (statAppliedEl) statAppliedEl.textContent = colCounts.applied + colCounts.interview + colCounts.offer;
            const statInterviewEl = document.getElementById('tracker-stat-interview');
            if (statInterviewEl) statInterviewEl.textContent = colCounts.interview;
            const statOfferEl = document.getElementById('tracker-stat-offer');
            if (statOfferEl) statOfferEl.textContent = colCounts.offer;
        },

        createKanbanCardElement(app, isFavorite, lang, dict) {
            const card = document.createElement('div');
            card.className = `kanban-card ${app.is_ccift_deik ? 'kanban-card-ccift' : ''}`;
            card.setAttribute('draggable', 'true');
            card.setAttribute('data-id', app.id);

            card.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', String(app.id));
                card.classList.add('kanban-card-dragging');
            });

            card.addEventListener('dragend', () => {
                card.classList.remove('kanban-card-dragging');
            });

            const displayTitle = lang === 'fr' ? (app.title_fr || app.title) : app.title;
            const cciftBadge = app.is_ccift_deik ? '<span class="kanban-badge-ccift">🤝 CCIFT/DEİK</span>' : '';
            const noFrenchBadge = !app.french_required ? `<span class="kanban-badge-nofrench">${dict.kanbanBadgeNoFrench}</span>` : '';

            // Badge de Voie Prioritaire
            let trackBadge = '';
            if (app.track === 'voie_1') trackBadge = `<span class="kanban-badge-track track-col-1">${lang === 'fr' ? '🏛️ VOIE 1' : '🏛️ KAPI 1'}</span>`;
            if (app.track === 'voie_2') trackBadge = `<span class="kanban-badge-track track-col-2">${lang === 'fr' ? '🏢 VOIE 2' : '🏢 KAPI 2'}</span>`;
            if (app.track === 'voie_3') trackBadge = `<span class="kanban-badge-track track-col-3">${lang === 'fr' ? '🚀 VOIE 3' : '🚀 KAPI 3'}</span>`;

            const currentIndex = this.columns.indexOf(app.status);
            const canGoBack = currentIndex > 0;
            const canGoForward = currentIndex < this.columns.length - 1;

            let dateHtml = '';
            if (app.applied_date) {
                dateHtml += `<div class="kanban-date-badge">📅 ${app.applied_date}</div>`;
            }
            if (app.interview_date) {
                dateHtml += `<div class="kanban-date-badge date-interview">🎙️ ${app.interview_date}</div>`;
            }

            let notesPreview = '';
            if (app.notes && app.notes.trim()) {
                notesPreview = `<div class="kanban-notes-preview" title="${app.notes.replace(/"/g, '&quot;')}">📝 ${app.notes}</div>`;
            }

            const lblEdit = lang === 'fr' ? '✏️ Note / Détail' : '✏️ Not / Detay';
            const lblLink = lang === 'fr' ? '🔗 Offre ↗' : '🔗 İlan ↗';
            const lblBack = lang === 'fr' ? '◀ Reculer' : '◀ Geri';
            const lblForward = lang === 'fr' ? 'Avancer ▶' : 'İlerlet ▶';
            const lblFav = isFavorite ? dict.favRemoveLabel : dict.favAddLabel;

            // Sélecteur tactile de statut (alternative au glisser-déposer, inopérant au doigt)
            const statusLabels = {
                saved: dict.colSavedTitle,
                applied: dict.colAppliedTitle,
                interview: dict.colInterviewTitle,
                offer: dict.colOfferTitle
            };
            const moveOptionsHtml = this.columns.map(colKey =>
                `<option value="${colKey}" ${colKey === app.status ? 'selected' : ''}>${statusLabels[colKey] || colKey}</option>`
            ).join('');

            card.innerHTML = `
                <div class="kanban-card-header">
                    <div class="kanban-company-box">
                        <strong class="kanban-company">${app.company}</strong>
                        <span class="kanban-location">📍 ${app.location}</span>
                    </div>
                    <button class="kanban-fav-btn ${isFavorite ? 'active' : ''}" onclick="window.TrackerEngine.toggleBookmark(${app.id}, event)" title="${lblFav}" aria-label="${lblFav}" aria-pressed="${isFavorite ? 'true' : 'false'}">
                        ${isFavorite ? '★' : '☆'}
                    </button>
                </div>
                
                <h4 class="kanban-title">${displayTitle}</h4>
                
                <div class="kanban-badges-row">
                    ${trackBadge}
                    ${cciftBadge}
                    ${noFrenchBadge}
                    <span class="kanban-badge-score">%${app.relevance_score}</span>
                </div>

                ${dateHtml}
                ${notesPreview}

                <div class="kanban-actions-row">
                    <button class="kanban-btn-action" onclick="window.TrackerEngine.openTrackerModal(${app.id})" title="${dict.modalTitle}">
                        ${lblEdit}
                    </button>
                    ${app.url ? `<a href="${app.url}" target="_blank" class="kanban-btn-link" title="${lblLink}">${lblLink}</a>` : ''}
                </div>

                <div class="kanban-move-row">
                    <button class="kanban-move-btn" onclick="window.TrackerEngine.advanceKanban(${app.id}, -1)" ${canGoBack ? '' : 'disabled'} title="${lblBack}">
                        ${lblBack}
                    </button>
                    <button class="kanban-move-btn btn-forward" onclick="window.TrackerEngine.advanceKanban(${app.id}, 1)" ${canGoForward ? '' : 'disabled'} title="${lblForward}">
                        ${lblForward}
                    </button>
                </div>

                <label class="kanban-move-label" style="display: block; margin-top: 8px; font-size: 0.8em; opacity: 0.8;">
                    ${dict.kanbanMoveLabel}
                    <select class="kanban-move-select" aria-label="${dict.kanbanMoveLabel}" style="display: block; width: 100%; min-height: 44px; font-size: 16px; margin-top: 4px; padding: 0 8px; color: inherit; background-color: transparent; border: 1px solid currentColor; border-radius: 8px; font-family: inherit;">
                        ${moveOptionsHtml}
                    </select>
                </label>
            `;

            // Changement de statut au doigt : même logique que le drop
            const moveSelect = card.querySelector('.kanban-move-select');
            if (moveSelect) {
                moveSelect.addEventListener('change', (e) => {
                    const newStatus = e.target.value;
                    if (newStatus && newStatus !== app.status) {
                        this.moveToStatus(app.id, newStatus);
                    }
                });
            }

            return card;
        }
    };

    // --------------------------------------------------------------------------
    // 6. SERVICE D'EXPORTATION (JSON & CSV BILINGUE SUPERVISEUR)
    // --------------------------------------------------------------------------
    const ExportService = {
        exportJSON() {
            const applications = StorageService.getApplications();
            const list = Object.values(applications);

            const exportPayload = {
                metadata: {
                    project: "Plateforme Bilatérale de Recrutement France-Turquie",
                    exported_at: new Date().toISOString(),
                    total_applications: list.length,
                    supervisor_note: "Journal des candidatures des ressortissants turcs postulant en France (avec statut de visa, voies d'accès KAPI 1/2/3 et compétences linguistiques)."
                },
                applications: list
            };

            const jsonStr = JSON.stringify(exportPayload, null, 2);
            this.downloadFile(jsonStr, 'journal_candidatures_france_turquie.json', 'application/json;charset=utf-8;');

            const lang = StorageService.getLang();
            const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;
            ToastService.show(dict.toastExportJson, 'success');
        },

        exportCSV() {
            const applications = StorageService.getApplications();
            const list = Object.values(applications);

            // En-têtes CSV optimisés pour superviseur RH français et candidat turc
            const headers = [
                "ID",
                "Entreprise / Kurum",
                "Poste (FR)",
                "Poste (TR)",
                "Statut Candidature",
                "Voie Prioritaire (KAPI)",
                "Domaine d'Activité",
                "Date de Candidature",
                "Date d'Entretien",
                "Notes & Suivi RH",
                "Régime Visa / Relocalisation",
                "Langue de Travail",
                "Accréditation CCIFT/DEIK",
                "Score Pertinence",
                "Lien Offre d'Emploi"
            ];

            const rows = list.map(app => {
                let statusLabel = app.status;
                if (app.status === 'saved') statusLabel = 'Enregistré / Cible (Kaydedildi)';
                if (app.status === 'applied') statusLabel = 'Candidature Envoyée (Başvuruldu)';
                if (app.status === 'interview') statusLabel = 'Entretien RH / Technique (Mülakat)';
                if (app.status === 'offer') statusLabel = 'Offre Reçue / Contrat (Kabul)';

                let trackLabel = "Autre / Terrain";
                if (app.track === 'voie_1') trackLabel = "VOIE 1 : Institution Internationale";
                if (app.track === 'voie_2') trackLabel = "VOIE 2 : Multinationale Turque (ICT)";
                if (app.track === 'voie_3') trackLabel = "VOIE 3 : Tech Scale-up (Passeport Talent)";

                return [
                    app.id,
                    app.company,
                    app.title_fr || app.title,
                    app.title,
                    statusLabel,
                    trackLabel,
                    app.domain || 'Général',
                    app.applied_date || '',
                    app.interview_date || '',
                    (app.notes || '').replace(/[\r\n]+/g, ' '),
                    app.visa_sponsorship || '',
                    app.working_language || '',
                    app.is_ccift_deik ? 'OUI (Membre Officiel CCIFT & DEIK)' : 'NON',
                    `${app.relevance_score}%`,
                    app.url
                ].map(val => `"${String(val || '').replace(/"/g, '""')}"`);
            });

            // Ajout du BOM UTF-8 (\uFEFF) pour compatibilité parfaite avec Excel / Windows
            const csvContent = '\uFEFF' + [headers.join(','), ...rows.map(r => r.join(','))].join('\r\n');
            this.downloadFile(csvContent, 'journal_candidatures_france.csv', 'text/csv;charset=utf-8;');

            const lang = StorageService.getLang();
            const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;
            ToastService.show(dict.toastExportCsv, 'success');
        },

        downloadFile(content, fileName, mimeType) {
            const blob = new Blob([content], { type: mimeType });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            setTimeout(() => {
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }, 200);
        }
    };

    // --------------------------------------------------------------------------
    // 7. GESTIONNAIRE DES ONGLETS & CONTRÔLEUR D'INTERFACE
    // --------------------------------------------------------------------------
    // Identifiant d'overlay de la modale d'édition (contrat d'historique, voir section 7bis)
    const TRACKER_MODAL_ID = 'tracker-modal';

    const UIController = {
        currentTab: 'explore',
        scrollPositions: {},

        init() {
            // Initialisation de la langue mémorisée
            // (silencieux : pas de toast de changement de langue au lancement)
            const savedLang = StorageService.getLang();
            this.applyLanguage(savedLang, { silent: true });

            // Initialisation des favoris et états sur les cartes d'exploration
            this.syncExplorerCards();

            // Initialisation de la checklist du guide
            this.initChecklist();

            // Rendu initial du Kanban
            KanbanTracker.init();
            KanbanTracker.render();

            // Initialisation du filtre
            FilterEngine.init();
            FilterEngine.apply();

            // Modal events
            this.setupModalEvents();

            // Routage historique (bouton Retour Android) + onglet initial selon le hash
            HistoryRouter.init();
        },

        // Affichage d'un onglet (rendu pur, sans toucher à l'historique : voir HistoryRouter)
        switchTab(tabKey) {
            const previousTab = this.currentTab;
            if (previousTab !== tabKey) {
                this.scrollPositions[previousTab] = window.scrollY || 0;
            }
            this.currentTab = tabKey;

            // Boutons d'onglets
            document.querySelectorAll('.tab-nav-btn').forEach(b => {
                b.classList.remove('active');
            });
            const activeBtn = document.getElementById(`tabBtn${tabKey.charAt(0).toUpperCase() + tabKey.slice(1)}`);
            if (activeBtn) activeBtn.classList.add('active');

            // Panneaux d'onglets
            const panes = ['explore', 'tracker', 'guide'];
            panes.forEach(p => {
                const paneEl = document.getElementById(`tab-content-${p}`);
                if (paneEl) {
                    if (p === tabKey) {
                        paneEl.style.display = 'block';
                        paneEl.classList.add('tab-active');
                    } else {
                        paneEl.style.display = 'none';
                        paneEl.classList.remove('tab-active');
                    }
                }
            });

            // Si bascule vers le tracker, on rafraîchit le Kanban
            if (tabKey === 'tracker') {
                KanbanTracker.render();
            }

            // Retour sur Keşfet : restauration de la position dans la liste ; sinon haut de page
            const savedScroll = (tabKey === 'explore' && previousTab !== tabKey) ? (this.scrollPositions.explore || 0) : 0;
            if (savedScroll > 0) {
                window.scrollTo({ top: savedScroll, behavior: 'auto' });
            } else {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        },

        applyLanguage(lang, options = {}) {
            StorageService.setLang(lang);
            const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;

            // Langue du document (lecteurs d'écran, césure, traduction auto de Chrome)
            document.documentElement.lang = lang;

            // Bascule visuelle des boutons de langue
            const btnTR = document.getElementById('btnTR');
            const btnFR = document.getElementById('btnFR');
            if (btnTR) btnTR.classList.toggle('active', lang === 'tr');
            if (btnFR) btnFR.classList.toggle('active', lang === 'fr');

            // 1. MOTEUR UNIVERSEL DATA-TR / DATA-FR
            document.querySelectorAll('[data-tr][data-fr]').forEach((el) => {
                const text = (lang === 'fr') ? el.getAttribute('data-fr') : el.getAttribute('data-tr');
                if (text !== null && text !== undefined) {
                    const svg = el.querySelector('svg.svg-icon, svg');
                    if (svg && el.children.length === 1 && !text.includes('<svg')) {
                        const cloneSvg = svg.cloneNode(true);
                        el.innerHTML = '';
                        el.appendChild(cloneSvg);
                        el.appendChild(document.createTextNode(' ' + text));
                    } else {
                        el.innerHTML = text;
                    }
                }
            });

            // 2. MOTEUR UNIVERSEL DE PLACEHOLDERS
            document.querySelectorAll('[data-placeholder-tr][data-placeholder-fr]').forEach((el) => {
                el.placeholder = (lang === 'fr') ? el.getAttribute('data-placeholder-fr') : el.getAttribute('data-placeholder-tr');
            });

            // 3. MOTEUR UNIVERSEL DE TOOLTIPS / TITRES
            document.querySelectorAll('[data-tooltip-tr][data-tooltip-fr]').forEach((el) => {
                el.title = (lang === 'fr') ? el.getAttribute('data-tooltip-fr') : el.getAttribute('data-tooltip-tr');
            });

            // Traduction des onglets
            const tabExplore = document.getElementById('i18n-tab-explore');
            if (tabExplore) tabExplore.textContent = dict.tabExplore;
            const tabTracker = document.getElementById('i18n-tab-tracker');
            if (tabTracker) tabTracker.textContent = dict.tabTracker;
            const tabGuide = document.getElementById('i18n-tab-guide');
            if (tabGuide) tabGuide.textContent = dict.tabGuide;

            // 3 Portes Prioritaires I18N
            const elTracksTitle = document.getElementById('i18n-tracks-title');
            if (elTracksTitle) elTracksTitle.textContent = dict.tracksTitle;
            const elTrackAll = document.getElementById('i18n-track-all');
            if (elTrackAll) elTrackAll.textContent = dict.trackAll;
            const elTrack1 = document.getElementById('i18n-track-1');
            if (elTrack1) elTrack1.textContent = dict.track1;
            const elTrack2 = document.getElementById('i18n-track-2');
            if (elTrack2) elTrack2.textContent = dict.track2;
            const elTrack3 = document.getElementById('i18n-track-3');
            if (elTrack3) elTrack3.textContent = dict.track3;

            // Domaines d'Activité & Tri I18N
            const elDomainLabel = document.getElementById('i18n-domain-label');
            if (elDomainLabel) elDomainLabel.textContent = dict.domainLabel;
            const optDomAll = document.getElementById('opt-domain-all');
            if (optDomAll) optDomAll.textContent = dict.domainAll;
            const optDomIt = document.getElementById('opt-domain-it');
            if (optDomIt) optDomIt.textContent = dict.domainIt;
            const optDomLog = document.getElementById('opt-domain-logistics');
            if (optDomLog) optDomLog.textContent = dict.domainLogistics;
            const optDomSales = document.getElementById('opt-domain-sales');
            if (optDomSales) optDomSales.textContent = dict.domainSales;
            const optDomLegal = document.getElementById('opt-domain-legal');
            if (optDomLegal) optDomLegal.textContent = dict.domainLegal;
            const optDomMedia = document.getElementById('opt-domain-media');
            if (optDomMedia) optDomMedia.textContent = dict.domainMedia;
            const optDomHr = document.getElementById('opt-domain-hr');
            if (optDomHr) optDomHr.textContent = dict.domainHr;
            const optDomCraft = document.getElementById('opt-domain-craft');
            if (optDomCraft) optDomCraft.textContent = dict.domainCraft;

            const elSortLabel = document.getElementById('i18n-sort-label');
            if (elSortLabel) elSortLabel.textContent = dict.sortLabel;
            const optSortScore = document.getElementById('opt-sort-score');
            if (optSortScore) optSortScore.textContent = dict.sortScore;
            const optSortDate = document.getElementById('opt-sort-date');
            if (optSortDate) optSortDate.textContent = dict.sortDate;
            const optSortComp = document.getElementById('opt-sort-company');
            if (optSortComp) optSortComp.textContent = dict.sortCompany;

            // En-têtes et textes informatifs
            const elTitle = document.getElementById('i18n-title');
            if (elTitle) elTitle.textContent = dict.title;
            const elSubtitle = document.getElementById('i18n-subtitle');
            if (elSubtitle) elSubtitle.textContent = dict.subtitle;

            const elStatTotal = document.getElementById('i18n-stat-total');
            if (elStatTotal) elStatTotal.textContent = dict.statTotal;
            const elStatCcift = document.getElementById('i18n-stat-ccift');
            if (elStatCcift) elStatCcift.textContent = dict.statCcift;
            const elStatNoFrench = document.getElementById('i18n-stat-no-french');
            if (elStatNoFrench) elStatNoFrench.textContent = dict.statNoFrench;
            const elStatReloc = document.getElementById('i18n-stat-reloc');
            if (elStatReloc) elStatReloc.textContent = dict.statReloc;

            const elCciftBoxTitle = document.getElementById('i18n-ccift-box-title');
            if (elCciftBoxTitle) elCciftBoxTitle.textContent = dict.cciftBoxTitle;
            const elCciftQuickBtn = document.getElementById('i18n-ccift-quick-btn');
            if (elCciftQuickBtn) elCciftQuickBtn.textContent = dict.cciftQuickBtn;
            const elCciftBoxText = document.getElementById('i18n-ccift-box-text');
            if (elCciftBoxText) elCciftBoxText.innerHTML = dict.cciftBoxText;

            const elAdviceTitle = document.getElementById('i18n-advice-title');
            if (elAdviceTitle) elAdviceTitle.textContent = dict.adviceTitle;
            const elAdviceText = document.getElementById('i18n-advice-text');
            if (elAdviceText) elAdviceText.innerHTML = dict.adviceText;

            const searchInput = document.getElementById('searchInput');
            if (searchInput) searchInput.placeholder = dict.searchPlaceholder;

            // Filtres
            const btnReset = document.getElementById('btn-reset-filters');
            if (btnReset) btnReset.textContent = dict.filterReset;

            // Tracker I18N
            const trackerTitle = document.getElementById('i18n-tracker-title');
            if (trackerTitle) trackerTitle.textContent = dict.trackerTitle;
            const trackerSubtitle = document.getElementById('i18n-tracker-subtitle');
            if (trackerSubtitle) trackerSubtitle.textContent = dict.trackerSubtitle;
            const trackerSearch = document.getElementById('trackerSearchInput');
            if (trackerSearch) trackerSearch.placeholder = dict.trackerSearchPlaceholder;

            const btnExportJson = document.getElementById('btn-export-json');
            if (btnExportJson) btnExportJson.textContent = dict.exportJsonBtn;
            const btnExportCsv = document.getElementById('btn-export-csv');
            if (btnExportCsv) btnExportCsv.textContent = dict.exportCsvBtn;
            const btnClearTracker = document.getElementById('btn-clear-tracker');
            if (btnClearTracker) btnClearTracker.textContent = dict.clearTrackerBtn;

            const colSavedTitle = document.getElementById('i18n-col-saved-title');
            if (colSavedTitle) colSavedTitle.textContent = dict.colSavedTitle;
            const colAppliedTitle = document.getElementById('i18n-col-applied-title');
            if (colAppliedTitle) colAppliedTitle.textContent = dict.colAppliedTitle;
            const colInterviewTitle = document.getElementById('i18n-col-interview-title');
            if (colInterviewTitle) colInterviewTitle.textContent = dict.colInterviewTitle;
            const colOfferTitle = document.getElementById('i18n-col-offer-title');
            if (colOfferTitle) colOfferTitle.textContent = dict.colOfferTitle;

            // Traduction des cartes d'offres de l'onglet Explorer
            const cards = document.querySelectorAll('#cardsGrid .job-card');
            cards.forEach(card => {
                const title = lang === 'fr' ? (card.getAttribute('data-title-fr') || card.getAttribute('data-title-tr')) : card.getAttribute('data-title-tr');
                const titleEl = card.querySelector('.job-title');
                if (titleEl) {
                    titleEl.textContent = title;
                    titleEl.setAttribute('data-original-text', title);
                }

                const snippet = lang === 'fr' ? (card.getAttribute('data-snippet-fr') || card.getAttribute('data-snippet-tr')) : card.getAttribute('data-snippet-tr');
                const snippetEl = card.querySelector('.snippet');
                if (snippetEl) {
                    snippetEl.textContent = snippet;
                    snippetEl.setAttribute('data-original-text', snippet);
                }

                const cat = lang === 'fr' ? (card.getAttribute('data-category-fr') || card.getAttribute('data-category-tr')) : card.getAttribute('data-category-tr');
                const catBadge = card.querySelector('.card-cat-badge');
                if (catBadge) catBadge.textContent = cat;

                const scorePrefix = card.querySelector('.score-prefix');
                if (scorePrefix) scorePrefix.textContent = dict.scorePrefix;

                const applyBtn = card.querySelector('.apply-btn');
                if (applyBtn) applyBtn.textContent = dict.applyBtn;
                const secBtn = card.querySelector('.secondary-btn');
                if (secBtn) secBtn.textContent = dict.hrBtn;

                const langBadge = card.querySelector('[data-lang-badge="true"]');
                if (langBadge) {
                    langBadge.textContent = lang === 'tr' ? langBadge.getAttribute('data-tr') : langBadge.getAttribute('data-fr');
                }

                // Traduction du Visa
                const visaEl = card.querySelector('.val-visa');
                if (visaEl) {
                    const visaVal = (lang === 'fr')
                        ? (card.getAttribute('data-visa-fr') || card.getAttribute('data-visa-tr') || card.getAttribute('data-visa'))
                        : (card.getAttribute('data-visa-tr') || card.getAttribute('data-visa'));
                    if (visaVal) visaEl.textContent = visaVal;
                }

                // Boutons d'actions de la carte
                const btnDrawerSpan = card.querySelector('.action-btn-primary span');
                if (btnDrawerSpan) btnDrawerSpan.textContent = lang === 'fr' ? '👁️ Offre & Visa' : '👁️ İlan & Vize';
                const btnPitchSpan = card.querySelector('.action-btn-pitch span');
                if (btnPitchSpan) btnPitchSpan.textContent = lang === 'fr' ? '✍️ Lettre & Pitch' : '✍️ Ön Yazı';
                const btnWaSpan = card.querySelector('.action-btn-wa span');
                if (btnWaSpan) btnWaSpan.textContent = lang === 'fr' ? '💬 Partager' : '💬 Paylaş';
                const btnLinkSpan = card.querySelector('.secondary-btn span');
                if (btnLinkSpan) btnLinkSpan.textContent = lang === 'fr' ? 'Lien' : 'Link';

                // Ruban Voie Prioritaire
                const track = card.getAttribute('data-track');
                const trackRibbon = card.querySelector('.track-ribbon-text');
                if (trackRibbon) {
                    if (track === 'voie_1') trackRibbon.textContent = dict.badgeTrack1;
                    if (track === 'voie_2') trackRibbon.textContent = dict.badgeTrack2;
                    if (track === 'voie_3') trackRibbon.textContent = dict.badgeTrack3;
                }

                // Tags multilingues
                const tagsStr = lang === 'tr' ? card.getAttribute('data-tags-tr') : card.getAttribute('data-tags-fr');
                const tagsContainer = card.querySelector('.card-tags');
                if (tagsContainer && tagsStr) {
                    tagsContainer.innerHTML = '';
                    const tagsList = tagsStr.split('|').filter(x => x.trim().length > 0);
                    tagsList.forEach(tag => {
                        const span = document.createElement('span');
                        span.className = 'tag ' + this.getTagClass(tag);
                        span.textContent = tag;
                        tagsContainer.appendChild(span);
                    });
                }
            });

            // Bouton de suivi & favoris des cartes (libellés + title/aria-label dans la langue courante)
            this.syncExplorerCards();

            // Rafraîchissement des cartes du Kanban
            KanbanTracker.render();
            // Réapplication du filtre
            FilterEngine.apply();

            // Notification aux autres composants
            window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }));
            // Toast uniquement sur action utilisateur (pas à l'initialisation)
            if (!options.silent) {
                ToastService.show(dict.toastLangChanged, 'success');
            }
        },

        getTagClass(tag) {
            if (tag.includes('CCIFT') || tag.includes('DEİK')) return 'tag-ccift';
            if (tag.includes('Vize') || tag.includes('Visa') || tag.includes('Relokasyon') || tag.includes('Relocalisation') || tag.includes('MAE')) return 'tag-visa';
            if (tag.includes('Kurum') || tag.includes('Holding') || tag.includes('Grubu') || tag.includes('Groupe') || tag.includes('Institution')) return 'tag-corp';
            if (tag.includes('Şart Değil') || tag.includes('Non Requis') || tag.includes('İngilizce') || tag.includes('Anglais') || tag.includes('Türkçe')) return 'tag-lang';
            if (tag.includes('📍') || tag.includes('Paris') || tag.includes('Lyon') || tag.includes('Strasbourg')) return 'tag-loc';
            return 'tag-default';
        },

        syncExplorerCards() {
            const favorites = StorageService.getFavorites();
            const applications = StorageService.getApplications();
            const lang = StorageService.getLang();
            const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;

            const cards = document.querySelectorAll('#cardsGrid .job-card');
            cards.forEach(card => {
                const id = card.getAttribute('data-id');
                const strId = String(id);

                // Bouton favori ⭐
                const isFav = favorites.has(strId);
                const favBtn = card.querySelector('.bookmark-btn');
                if (favBtn) {
                    favBtn.classList.toggle('active', isFav);
                    const starIcon = favBtn.querySelector('.star-icon');
                    if (starIcon) starIcon.textContent = isFav ? '★' : '☆';
                    const favLabel = isFav ? dict.favRemoveLabel : dict.favAddLabel;
                    favBtn.title = favLabel;
                    favBtn.setAttribute('aria-label', favLabel);
                    favBtn.setAttribute('aria-pressed', isFav ? 'true' : 'false');
                }

                // Bouton de suivi dans le footer
                const app = applications[strId];
                const trackBtn = card.querySelector('.tracker-action-btn');
                const statusBadge = card.querySelector('.card-tracker-status');

                if (trackBtn) {
                    if (app) {
                        trackBtn.classList.add('in-pipeline');
                        trackBtn.innerHTML = `<span>✓</span> <span>${dict.trackedBtn}</span>`;
                    } else {
                        trackBtn.classList.remove('in-pipeline');
                        trackBtn.innerHTML = `<span>📋</span> <span>${dict.trackAddBtn}</span>`;
                    }
                }

                if (statusBadge) {
                    if (app) {
                        statusBadge.style.display = 'inline-block';
                        let label = app.status;
                        if (app.status === 'saved') label = '📌 ' + dict.colSavedTitle;
                        if (app.status === 'applied') label = '📤 ' + dict.colAppliedTitle;
                        if (app.status === 'interview') label = '🎙️ ' + dict.colInterviewTitle;
                        if (app.status === 'offer') label = '🎉 ' + dict.colOfferTitle;
                        statusBadge.textContent = label;
                        statusBadge.className = `card-tracker-status status-badge-${app.status}`;
                    } else {
                        statusBadge.style.display = 'none';
                    }
                }
            });

            // Badge total dans l'onglet
            const badgeTracker = document.getElementById('badge-tracker-count');
            if (badgeTracker) badgeTracker.textContent = Object.keys(applications).length;
        },

        // Modal de suivi & édition
        setupModalEvents() {
            const modal = document.getElementById('tracker-modal');
            if (!modal) return;

            const closeBtn = document.getElementById('modal-close-btn');
            const cancelBtn = document.getElementById('modal-cancel-btn');
            const form = document.getElementById('tracker-form');
            const deleteBtn = document.getElementById('modal-delete-btn');

            if (closeBtn) closeBtn.onclick = () => this.requestCloseModal();
            if (cancelBtn) cancelBtn.onclick = () => this.requestCloseModal();
            modal.onclick = (e) => {
                if (e.target === modal) this.requestCloseModal();
            };

            if (form) {
                form.onsubmit = (e) => {
                    e.preventDefault();
                    this.saveModalData();
                };
            }

            if (deleteBtn) {
                deleteBtn.onclick = () => {
                    const jobId = document.getElementById('modal-job-id').value;
                    if (jobId) {
                        StorageService.deleteApplication(jobId);
                        const lang = StorageService.getLang();
                        const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;
                        ToastService.show(dict.toastTrackDeleted, 'info');
                        this.requestCloseModal();
                        KanbanTracker.render();
                        this.syncExplorerCards();
                        FilterEngine.apply();
                    }
                };
            }

            // Touche Échap
            window.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && modal.style.display === 'flex') {
                    this.requestCloseModal();
                }
            });

            // Bouton/geste Retour Android : fermeture sans toucher à l'historique
            window.addEventListener('popstate', (event) => {
                if (modal.style.display === 'flex' && (event.state || {}).fransaOverlay !== TRACKER_MODAL_ID) {
                    this.closeModal();
                }
            });
        },

        openModal(jobId) {
            const modal = document.getElementById('tracker-modal');
            if (!modal) return;

            const card = document.querySelector(`#cardsGrid .job-card[data-id="${jobId}"]`);
            let existingApp = StorageService.getApplication(jobId);
            const lang = StorageService.getLang();
            const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;

            let title = '';
            let company = '';

            if (existingApp) {
                title = lang === 'fr' ? (existingApp.title_fr || existingApp.title) : existingApp.title;
                company = existingApp.company;
            } else if (card) {
                title = lang === 'fr' ? card.getAttribute('data-title-fr') : card.getAttribute('data-title-tr');
                company = card.getAttribute('data-company');
            }

            document.getElementById('modal-job-id').value = jobId;
            document.getElementById('modal-card-title').textContent = title;
            document.getElementById('modal-card-company').textContent = company;

            const statusSelect = document.getElementById('modal-status');
            const appliedDateInput = document.getElementById('modal-applied-date');
            const interviewDateInput = document.getElementById('modal-interview-date');
            const notesInput = document.getElementById('modal-notes');
            const deleteBtn = document.getElementById('modal-delete-btn');

            if (existingApp) {
                statusSelect.value = existingApp.status || 'saved';
                appliedDateInput.value = existingApp.applied_date || '';
                interviewDateInput.value = existingApp.interview_date || '';
                notesInput.value = existingApp.notes || '';
                deleteBtn.style.display = 'inline-block';
            } else {
                statusSelect.value = 'saved';
                // Date du jour par défaut
                appliedDateInput.value = new Date().toISOString().split('T')[0];
                interviewDateInput.value = '';
                notesInput.value = '';
                deleteBtn.style.display = 'none';
            }

            modal.style.display = 'flex';
            HistoryRouter.pushOverlay(TRACKER_MODAL_ID);
            setTimeout(() => {
                notesInput.focus();
            }, 50);
        },

        saveModalData() {
            const jobId = document.getElementById('modal-job-id').value;
            const status = document.getElementById('modal-status').value;
            const appliedDate = document.getElementById('modal-applied-date').value;
            const interviewDate = document.getElementById('modal-interview-date').value;
            const notes = document.getElementById('modal-notes').value;

            const card = document.querySelector(`#cardsGrid .job-card[data-id="${jobId}"]`);
            const jobData = {};

            if (card) {
                jobData.title = card.getAttribute('data-title-tr');
                jobData.title_fr = card.getAttribute('data-title-fr');
                jobData.company = card.getAttribute('data-company');
                jobData.location = card.getAttribute('data-location');
                jobData.url = card.getAttribute('data-url');
                jobData.source = card.getAttribute('data-source');
                jobData.relevance_score = parseInt(card.getAttribute('data-score') || '50', 10);
                jobData.category = card.getAttribute('data-category-tr');
                jobData.working_language = card.getAttribute('data-working-lang');
                jobData.visa_sponsorship = card.getAttribute('data-visa');
                jobData.is_ccift_deik = card.getAttribute('data-ccift') === 'true';
                jobData.french_required = card.getAttribute('data-no-french') !== 'true';
                jobData.track = card.getAttribute('data-track') || 'autre';
                jobData.domain = card.getAttribute('data-domain') || 'craft_pme';
            }

            StorageService.saveApplication(jobId, jobData, status, appliedDate, interviewDate, notes);

            const lang = StorageService.getLang();
            const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;
            ToastService.show(dict.toastTrackUpdated, 'success');
            haptic();

            this.requestCloseModal();
            KanbanTracker.render();
            this.syncExplorerCards();
            FilterEngine.apply();
        },

        // Fermeture demandée par l'UI (X, fond, Échap, Enregistrer, Supprimer)
        requestCloseModal() {
            HistoryRouter.closeOverlay(TRACKER_MODAL_ID, () => this.closeModal());
        },

        // Fermeture effective (appelée directement ou depuis le handler popstate)
        closeModal() {
            const modal = document.getElementById(TRACKER_MODAL_ID);
            if (!modal) return;
            modal.style.display = 'none';
        },

        initChecklist() {
            const savedChecklist = StorageService.getChecklist();
            const checkboxes = document.querySelectorAll('.guide-checkbox');
            checkboxes.forEach(cb => {
                const id = cb.id;
                if (savedChecklist[id]) {
                    cb.checked = true;
                    if (cb.parentElement) cb.parentElement.classList.add('checked-item');
                }
                cb.addEventListener('change', () => {
                    StorageService.saveChecklistItem(id, cb.checked);
                    if (cb.parentElement) cb.parentElement.classList.toggle('checked-item', cb.checked);
                });
            });
        },

        copyTextToClipboard(textId, buttonEl) {
            const textEl = document.getElementById(textId);
            if (!textEl) return;
            const textToCopy = textEl.innerText || textEl.textContent;

            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = buttonEl.textContent;
                buttonEl.textContent = "✓ Kopyalandı / Copié";
                buttonEl.classList.add('copied-btn');
                const lang = StorageService.getLang();
                const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;
                ToastService.show(dict.toastCopied, 'success');
                setTimeout(() => {
                    buttonEl.textContent = originalText;
                    buttonEl.classList.remove('copied-btn');
                }, 2000);
            }).catch(err => {
                console.error("Erreur copie presse-papier:", err);
            });
        }
    };

    // --------------------------------------------------------------------------
    // 7bis. ROUTEUR D'HISTORIQUE (BOUTON / GESTE RETOUR ANDROID)
    // --------------------------------------------------------------------------
    // Contrat partagé avec drawer_cover_letter_module.js :
    //  - overlay ouvert : pushState({ fransaOverlay: '<id>' }, '')
    //  - fermeture UI   : si state.fransaOverlay === '<id>' → history.back(), sinon fermeture directe
    //  - popstate       : chaque module ferme son overlay si state.fransaOverlay !== '<id>'
    //  - onglets        : Keşfet = état de base (hash vide ou #explore) ; Takip/Rehber poussés
    //                     depuis Keşfet (#tracker, #guide), remplacés entre eux.
    const TAB_KEYS = ['explore', 'tracker', 'guide'];

    const HistoryRouter = {
        // Onglet correspondant au hash (vide → explore ; hash inconnu → null = ancre interne, ignorée)
        tabFromHash() {
            const h = (window.location.hash || '').replace(/^#/, '').toLowerCase();
            if (!h) return 'explore';
            return TAB_KEYS.includes(h) ? h : null;
        },

        baseUrl() {
            return window.location.pathname + window.location.search;
        },

        // Onglet poussé par la navigation (une entrée Keşfet existe dessous dans l'historique)
        isPushedTab(state) {
            return Boolean(state && state.fransaTab && !state.fransaInitial && !state.fransaOverlay);
        },

        init() {
            const st = (history.state && typeof history.state === 'object') ? history.state : {};
            const tab = this.tabFromHash() || 'explore';

            // Au chargement : on respecte le hash (raccourcis du manifest) via replaceState.
            // Un éventuel état d'overlay résiduel (rechargement modale ouverte) est nettoyé.
            try {
                if (tab === 'explore') {
                    if (st.fransaOverlay || st.fransaTab) history.replaceState(null, '');
                } else if (!(st.fransaTab === tab && !st.fransaOverlay)) {
                    history.replaceState({ fransaTab: tab, fransaInitial: true }, '', '#' + tab);
                }
            } catch (e) {}

            if (tab !== UIController.currentTab) {
                UIController.switchTab(tab);
            }

            window.addEventListener('popstate', (event) => {
                const state = event.state || {};
                if (state.fransaOverlay) return; // géré par le module propriétaire de l'overlay
                const target = this.tabFromHash();
                if (target && target !== UIController.currentTab) {
                    UIController.switchTab(target);
                }
            });
        },

        // Navigation par la barre d'onglets / boutons internes
        navigateToTab(tabKey) {
            if (!TAB_KEYS.includes(tabKey)) tabKey = 'explore';
            const current = UIController.currentTab;
            const st = history.state || {};

            if (tabKey !== current) {
                try {
                    if (tabKey === 'explore') {
                        if (this.isPushedTab(st)) {
                            history.back(); // l'affichage se fait dans le handler popstate
                            return;
                        }
                        history.replaceState(null, '', this.baseUrl());
                    } else if (current === 'explore') {
                        history.pushState({ fransaTab: tabKey }, '', '#' + tabKey);
                    } else {
                        const newState = this.isPushedTab(st)
                            ? { fransaTab: tabKey }
                            : { fransaTab: tabKey, fransaInitial: true };
                        history.replaceState(newState, '', '#' + tabKey);
                    }
                } catch (e) {}
            }

            UIController.switchTab(tabKey);
        },

        pushOverlay(id) {
            try {
                if (history.state && history.state.fransaOverlay === id) return;
                history.pushState({ fransaOverlay: id }, '');
            } catch (e) {}
        },

        closeOverlay(id, closeFn) {
            if (history.state && history.state.fransaOverlay === id) {
                history.back(); // la fermeture effective se fait dans le handler popstate
            } else {
                closeFn();
            }
        }
    };

    // --------------------------------------------------------------------------
    // 8. API PUBLIQUE EXPOSÉE SUR WINDOW.TrackerEngine
    // --------------------------------------------------------------------------
    window.TrackerEngine = {
        // Services
        Storage: StorageService,
        Filter: FilterEngine,
        Kanban: KanbanTracker,
        Export: ExportService,
        UI: UIController,
        Toast: ToastService,

        // Actions 1-clic depuis les cartes HTML
        toggleBookmark(jobId, event) {
            if (event) event.stopPropagation();
            const isFav = StorageService.toggleFavorite(jobId);
            UIController.syncExplorerCards();
            KanbanTracker.render();
            FilterEngine.apply();

            const lang = StorageService.getLang();
            const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;
            ToastService.show(isFav ? dict.toastFavAdded : dict.toastFavRemoved, isFav ? 'star' : 'info');
            if (isFav) haptic();
        },

        openTrackerModal(jobId) {
            UIController.openModal(jobId);
        },

        advanceKanban(jobId, direction) {
            KanbanTracker.advanceStatus(jobId, direction);
        },

        exportCSV() {
            ExportService.exportCSV();
        },

        exportJSON() {
            ExportService.exportJSON();
        },

        clearAllApplications() {
            const lang = StorageService.getLang();
            const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;
            if (confirm(dict.clearTrackerConfirm)) {
                StorageService.clearAllApplications();
                KanbanTracker.render();
                UIController.syncExplorerCards();
                FilterEngine.apply();
                ToastService.show(dict.toastTrackerCleared, 'warning');
            }
        },

        switchTab(tabKey) {
            HistoryRouter.navigateToTab(tabKey);
        },

        setLanguage(lang) {
            UIController.applyLanguage(lang);
        },

        copyTemplate(textId, buttonEl) {
            UIController.copyTextToClipboard(textId, buttonEl);
        },

        shareWhatsApp(jobId) {
            const card = document.querySelector(`.job-card[data-id="${jobId}"]`);
            const title = card ? card.getAttribute('data-title-tr') || card.querySelector('.job-title')?.textContent.trim() : 'Fransa İş Fırsatı';
            const company = card ? card.getAttribute('data-company') : '';
            const url = (card && card.getAttribute('data-url')) || window.location.href;
            const baseText =
                `Aşkım / Merhaba, Fransa için şu ilanı buldum, sence başvurayım mı?\n\n` +
                `💼 Pozisyon: ${title}\n` +
                `🏢 Şirket: ${company}`;

            // Fallback historique : lien WhatsApp direct
            const openWhatsApp = () => {
                const text = encodeURIComponent(`${baseText}\n🔗 İlan Linki: ${url}`);
                window.open(`https://api.whatsapp.com/send?text=${text}`, '_blank');
            };

            // Feuille de partage native Android (WhatsApp, Telegram, SMS, e-mail...)
            if (navigator.share) {
                navigator.share({ title: `${title}${company ? ' - ' + company : ''}`, text: baseText, url })
                    .catch((err) => {
                        if (err && err.name === 'AbortError') return; // partage annulé par l'utilisatrice
                        console.warn('Partage natif indisponible, fallback WhatsApp:', err);
                        openWhatsApp();
                    });
                return;
            }
            openWhatsApp();
        },

        Toast: ToastService
    };

    // Démarrage automatique au chargement du DOM
    document.addEventListener('DOMContentLoaded', () => {
        UIController.init();
    });

})(window);
