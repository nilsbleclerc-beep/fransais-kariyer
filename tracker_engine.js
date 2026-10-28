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
            searchPlaceholder: "Pozisyon, şirket veya şehir ara",
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
            
            // Keşfet v4 (cartes compactes, pastilles, bottom sheet)
            helloNewCount: "<strong>{n} yeni ilan</strong>",
            helloTotalCount: "{n} ilan",
            newBadge: "Yeni",
            kapiShort: "Kapı {n}",
            kapiDesc1: "Uluslararası kurum",
            kapiDesc2: "Türk holdingi · ICT",
            kapiDesc3: "Passeport Talent",
            kapiOther: "Diğer yollar",
            pillNoFrench: "Fransızca gerekmez",
            visaIct: "ICT transferi",
            visaTalent: "Passeport Talent",
            visaMeae: "MEAE statüsü",
            visaGeneric: "Vize desteği",
            showResults: "{n} ilanı göster",
            showResultsZero: "Sonuç yok",

            // v5 : offres réelles datées + pistes
            ageToday: "Bugün",
            ageYesterday: "Dün",
            ageDays: "{n} gün önce",
            ageUnknown: "Tarih bilinmiyor",
            verifiedShort: "Doğrulandı",
            verifiedTitle: "Son 48 saatte ilanın hâlâ yayında olduğu kontrol edildi",
            pillVisaEvidence: "Vize ilanda belirtilmiş",
            updatedAt: "Son güncelleme: {d}",
            leadNotOffer: "Bu bir ilan değil — kariyer sayfası",
            leadLangUnknown: "Dil şartı belirtilmemiş",
            leadOpenSite: "Kariyer sayfasını aç",
            leadDetail: "Ayrıntılar",
            leadsEmpty: "Şu an listelenecek şirket yok.",
            langNames: { fr: "Fransızca", en: "İngilizce", tr: "Türkçe" },
            langLevels: { none: "gerekmez", basic: "temel", required: "gerekli", fluent: "akıcı", native: "anadil", optional: "artı" },

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
            searchPlaceholder: "Poste, entreprise ou ville",
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
            
            // Keşfet v4 (cartes compactes, pastilles, bottom sheet)
            helloNewCount: "<strong>{n} nouvelles offres</strong>",
            helloNewCountOne: "<strong>1 nouvelle offre</strong>",
            helloTotalCount: "{n} offres",
            helloTotalCountOne: "1 offre",
            newBadge: "Nouveau",
            kapiShort: "Voie {n}",
            kapiDesc1: "Institution internationale",
            kapiDesc2: "Groupe turc · ICT",
            kapiDesc3: "Passeport Talent",
            kapiOther: "Autres voies",
            pillNoFrench: "Français non requis",
            visaIct: "Détachement ICT",
            visaTalent: "Passeport Talent",
            visaMeae: "Statut MEAE",
            visaGeneric: "Visa sponsorisé",
            showResults: "Voir {n} offres",
            showResultsOne: "Voir 1 offre",
            showResultsZero: "Aucune offre",

            // v5 : offres réelles datées + pistes
            ageToday: "Aujourd'hui",
            ageYesterday: "Hier",
            ageDays: "Il y a {n} jours",
            ageUnknown: "Date inconnue",
            verifiedShort: "Vérifiée",
            verifiedTitle: "Annonce vérifiée en ligne il y a moins de 48 h",
            pillVisaEvidence: "Visa mentionné dans l'annonce",
            updatedAt: "Mis à jour : {d}",
            leadNotOffer: "Ce n'est pas une offre — page carrières",
            leadLangUnknown: "Exigence de langue non précisée",
            leadOpenSite: "Ouvrir la page carrières",
            leadDetail: "Détails",
            leadsEmpty: "Aucune entreprise à afficher pour le moment.",
            langNames: { fr: "Français", en: "Anglais", tr: "Turc" },
            langLevels: { none: "non requis", basic: "base", required: "requis", fluent: "courant", native: "natif", optional: "un plus" },

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
        LANG: 'france_jobs_lang_pref',
        // Schéma des clés favoris/candidatures : 'url-fnv1a-v1' = id stable dérivé de l'URL
        ID_SCHEME: 'fransa_id_scheme',
        LEGACY_FAVORITES: 'france_jobs_favorites_legacy_index'
    };
    const ID_SCHEME = 'url-fnv1a-v1';

    // FNV-1a 32 bits sur l'UTF-8 : MÊME algorithme que exporter.stable_job_id (Python)
    const fnv1a32 = (text) => {
        const bytes = (typeof TextEncoder !== 'undefined')
            ? new TextEncoder().encode(String(text))
            : unescape(encodeURIComponent(String(text))).split('').map(c => c.charCodeAt(0));
        let h = 0x811c9dc5;
        for (let i = 0; i < bytes.length; i++) {
            h ^= bytes[i];
            h = Math.imul(h, 0x01000193) >>> 0;
        }
        return h >>> 0;
    };
    const normalizeUrl = (url) => String(url || '').trim().replace(/\/+$/, '');
    const stableIdFromUrl = (url) => fnv1a32(normalizeUrl(url));

    // Instantané v4 (index → id stable) des 83 offres publiées avant le passage aux ids stables
    // (commit 740cb76). Sert UNIQUEMENT à migrer les favoris enregistrés par index.
    const LEGACY_V4_IDS = [2410060722,2170836891,3336665483,4211336872,3664975379,1946601936,594825396,2496426738,204671127,3615830085,1264125645,772877285,3259806011,1010310410,3043873899,1613371848,3965641887,1311636236,3518915140,3176398100,1501800745,3405188632,2687010302,2057123710,1373796142,3949121800,3147578398,3818381886,1372028316,3312950596,1121922774,1615728469,2485519511,3461326247,1848811603,3514488381,3349375138,1602288868,1417938254,2476197895,260153735,32357563,1866165443,2446198429,2623032985,2899754773,335535525,702139736,3486803334,629514951,3960354158,1375222996,3699875984,265216067,1773888865,2174750389,628406141,1887653261,2725527092,2768397049,2407545766,1783912095,2783897847,3770997350,2508230342,118728246,1812948326,4197170466,2901727252,2792724725,3668630324,2070086835,3469971240,2483970269,2165404509,2129131010,3067987018,253259666,701577076,3639111132,4235373933,590065582,2598907304];

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
                relevance_score: Number(jobData.relevance_score ?? existing.relevance_score ?? 0) || 0,
                kind: jobData.kind || existing.kind || 'offer',
                posted_at: jobData.posted_at || existing.posted_at || '',
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

    // Migration douce : anciennes clés = index dans la liste (changeaient à chaque scan)
    // → nouvelles clés = id stable dérivé de l'URL. Exécutée une seule fois.
    const IdMigration = {
        run() {
            let scheme = null;
            try { scheme = localStorage.getItem(STORAGE_KEYS.ID_SCHEME); } catch (e) { return; }
            if (scheme === ID_SCHEME) return;
            try {
                const jobs = getJobs();
                const currentIds = new Set(jobs.map(j => String(j.id)));
                const byUrl = new Map(jobs.filter(j => j.url).map(j => [normalizeUrl(j.url), String(j.id)]));
                const resolveUrl = (url) => byUrl.get(normalizeUrl(url)) || String(stableIdFromUrl(url));

                // 1. Candidatures : elles stockent leur URL → correspondance fiable
                const apps = StorageService.getApplications();
                const oldToNew = {};
                const migratedApps = {};
                Object.keys(apps).forEach(key => {
                    const app = apps[key] || {};
                    let newKey = key;
                    if (!currentIds.has(key) && app.url) newKey = resolveUrl(app.url);
                    oldToNew[key] = newKey;
                    if (!migratedApps[newKey] || String(app.updated_at || '') > String(migratedApps[newKey].updated_at || '')) {
                        migratedApps[newKey] = Object.assign({}, app, { id: newKey });
                    }
                });

                // 2. Favoris : via la candidature de même clé, sinon via l'instantané v4
                const favs = StorageService.getFavorites();
                const newFavs = new Set();
                const unresolved = [];
                favs.forEach(key => {
                    if (currentIds.has(key)) newFavs.add(key);
                    else if (oldToNew[key]) newFavs.add(oldToNew[key]);
                    else if (/^\d+$/.test(key) && LEGACY_V4_IDS[Number(key)] !== undefined) newFavs.add(String(LEGACY_V4_IDS[Number(key)]));
                    else unresolved.push(key);
                });

                StorageService.saveApplications(migratedApps);
                StorageService.saveFavorites(newFavs);
                if (unresolved.length) localStorage.setItem(STORAGE_KEYS.LEGACY_FAVORITES, JSON.stringify(unresolved));
                localStorage.setItem(STORAGE_KEYS.ID_SCHEME, ID_SCHEME);
            } catch (e) {
                console.warn('[TrackerEngine] Migration des identifiants impossible', e);
            }
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
    // 3bis. ACCÈS AUX DONNÉES (window.FransaData) & UTILITAIRES
    // --------------------------------------------------------------------------
    // Contrat : window.FransaData = { jobs: [...], get(id) } défini par le bootstrap
    // inline (exporter.py) avant tous les scripts. id = hash stable de l'URL (exporter.stable_job_id).
    // kind : "offer" (vraie annonce, Keşfet) | "lead" (fiche entreprise, section pistes du Rehber).
    const getJobs = () => (window.FransaData && Array.isArray(window.FransaData.jobs)) ? window.FransaData.jobs : [];
    let offersCache = null, leadsCache = null;
    const getOffers = () => offersCache || (offersCache = getJobs().filter(j => j.kind !== 'lead'));
    const getLeads = () => leadsCache || (leadsCache = getJobs().filter(j => j.kind === 'lead'));
    const getJob = (id) => (window.FransaData && typeof window.FransaData.get === 'function') ? window.FransaData.get(id) : null;
    const getDict = () => I18N_DICTIONARY[StorageService.getLang()] || I18N_DICTIONARY.tr;

    const escapeHtml = (value) => String(value == null ? '' : value).replace(/[&<>"']/g, (c) => (
        { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
    ));

    // Recherche insensible à la casse et aux diacritiques TR/FR : İ/ı/ş/ğ/ç/ö/ü/é... → ASCII
    const normalizeText = (value) => String(value || '')
        .replace(/[İI]/g, 'i')
        .toLowerCase()
        .replace(/ı/g, 'i')
        .normalize('NFD')
        .replace(/[̀-ͯ]/g, '')
        .replace(/œ/g, 'oe')
        .replace(/æ/g, 'ae');

    // 'dd/mm/YYYY HH:MM' → timestamp (0 si illisible)
    const parseDiscovered = (value) => {
        const m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})(?:\s+(\d{1,2}):(\d{2}))?/.exec(String(value || '').trim());
        if (!m) return 0;
        return new Date(+m[3], +m[2] - 1, +m[1], +(m[4] || 0), +(m[5] || 0)).getTime();
    };

    // 'YYYY-MM-DD' ou ISO → timestamp (0 si illisible). Date seule = minuit LOCAL.
    const parseIsoDate = (value) => {
        const v = String(value || '').trim();
        const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(v);
        if (m) return new Date(+m[1], +m[2] - 1, +m[3]).getTime();
        const t = /^\d{4}-\d{2}-\d{2}T/.test(v) ? Date.parse(v) : NaN;
        return Number.isFinite(t) ? t : 0;
    };
    const parseAnyDate = (value) => parseIsoDate(value) || parseDiscovered(value);
    const DAY_MS = 86400000;
    const VERIFIED_FRESH_MS = 48 * 3600 * 1000;

    // « 3 gün önce » / « Il y a 3 jours » (jours calendaires) ; null si date inconnue
    const ageLabel = (postedAt, dict) => {
        const ts = parseIsoDate(postedAt);
        if (!ts) return null;
        const now = new Date();
        const startToday = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
        const d = new Date(ts);
        const startPosted = new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime();
        const days = Math.max(0, Math.round((startToday - startPosted) / DAY_MS));
        if (days === 0) return dict.ageToday;
        if (days === 1) return dict.ageYesterday;
        return dict.ageDays.replace('{n}', days);
    };
    const isFreshlyVerified = (verifiedAt) => {
        const ts = parseIsoDate(verifiedAt);
        const delta = Date.now() - ts;
        return ts > 0 && delta < VERIFIED_FRESH_MS && delta > -3600000;
    };
    const formatDateTime = (iso, lang) => {
        const ts = parseIsoDate(iso);
        if (!ts) return '';
        try {
            return new Intl.DateTimeFormat(lang === 'fr' ? 'fr-FR' : 'tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }).format(new Date(ts));
        } catch (e) {
            return new Date(ts).toLocaleString();
        }
    };

    // Exigence de langue lisible : language_requirements, sinon tags de langue (honnête : rien d'inventé)
    // « Groupe Turc Majeur » ou « Enseignement du Turc » ne sont PAS des exigences de langue
    const LANG_TAG_RE = /fransız|ingiliz|türkçe|français|francais|anglais|en turc|turc\s*[&/]|\/\s*turc|bilingue|\b[abc][12]\b/i;
    const LANG_TAG_EXCLUDE_RE = /eğitim|enseignement|öğretim|okutman/i;
    const stripEmojiTe = (text) => String(text || '').replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{FE0F}\u{200D}]/gu, '').replace(/\s{2,}/g, ' ').trim();
    const langRequirementText = (job, lang, dict) => {
        const reqs = Array.isArray(job.language_requirements) ? job.language_requirements : [];
        if (reqs.length) {
            return reqs.map(r => {
                const [code, level] = String(r).split(':');
                const name = (dict.langNames || {})[code] || String(code || '').toUpperCase();
                const lvl = (dict.langLevels || {})[level] || String(level || '').toUpperCase();
                return lvl ? `${name} ${lvl}` : name;
            }).join(' · ');
        }
        const tags = (lang === 'fr' ? job.tags_fr : job.tags_tr) || [];
        const langTags = tags.filter(t => LANG_TAG_RE.test(t) && !LANG_TAG_EXCLUDE_RE.test(t)).map(stripEmojiTe).filter(Boolean);
        return langTags.length ? langTags.slice(0, 2).join(' · ') : dict.leadLangUnknown;
    };

    // Format attendu par StorageService.saveApplication à partir d'un job FransaData
    const jobToAppData = (job) => job ? {
        title: job.title_tr,
        title_fr: job.title_fr,
        company: job.company,
        location: job.location,
        url: job.url,
        source: job.source,
        relevance_score: job.kind === 'lead' ? 0 : job.score,
        kind: job.kind || 'offer',
        posted_at: job.posted_at || '',
        category: job.category_tr,
        working_language: job.working_lang,
        visa_sponsorship: job.visa_tr,
        is_ccift_deik: job.ccift,
        french_required: !job.no_french,
        track: job.track,
        domain: job.domain
    } : {};

    const plural = (dict, key, n) => ((n === 1 && dict[key + 'One']) ? dict[key + 'One'] : dict[key]).replace('{n}', n);

    // --------------------------------------------------------------------------
    // 3ter. NOUVEAUTÉS DEPUIS LA DERNIÈRE VISITE (localStorage fransa_last_visit)
    // --------------------------------------------------------------------------
    const LAST_VISIT_KEY = 'fransa_last_visit';
    const VisitTracker = {
        previous: null, // timestamp de la visite précédente, figé pour toute la session
        init() {
            try {
                const v = parseInt(localStorage.getItem(LAST_VISIT_KEY) || '', 10);
                this.previous = Number.isFinite(v) ? v : null;
            } catch (e) {
                this.previous = null;
            }
            const save = () => {
                try { localStorage.setItem(LAST_VISIT_KEY, String(Date.now())); } catch (e) {}
            };
            document.addEventListener('visibilitychange', () => {
                if (document.visibilityState === 'hidden') save();
            });
            window.addEventListener('pagehide', save);
        },
        isNew(job) {
            return this.previous !== null && FilterEngine.metaFor(job).seen > this.previous;
        },
        countNew() {
            return getOffers().filter(j => this.isNew(j)).length;
        }
    };

    // --------------------------------------------------------------------------
    // 4. MOTEUR DE RECHERCHE, DE FILTRAGE & DE TRI (sur window.FransaData.jobs)
    // --------------------------------------------------------------------------
    const DOMAIN_KEYS = ['all', 'it', 'logistics', 'sales', 'legal_policy', 'media_trans', 'hr_admin', 'craft_pme'];
    const SORT_KEYS = ['score_desc', 'date_desc', 'company_asc'];
    const TRACK_SEARCH_WORDS = {
        voie_1: 'kapi 1 voie 1 uluslararasi kurum institution internationale',
        voie_2: 'kapi 2 voie 2 holding ict',
        voie_3: 'kapi 3 voie 3 passeport talent tech'
    };

    const FilterEngine = {
        state: {
            query: '',
            track: 'all', // 'all', 'voie_1', 'voie_2', 'voie_3'
            domain: 'all', // 'all', 'it', 'logistics', 'sales', 'legal_policy', 'media_trans', 'hr_admin', 'craft_pme'
            category: 'all',
            status: 'all', // 'all', 'fav', 'tracked'
            noFrenchOnly: false,
            cciftOnly: false,
            sortBy: 'date_desc' // 'date_desc' (défaut : plus récent), 'score_desc', 'company_asc'
        },
        results: [],
        counts: { all: 0, voie_1: 0, voie_2: 0, voie_3: 0, nofr: 0, fav: 0 },
        debounceTimer: null,
        meta: new Map(),
        _favs: new Set(),
        _apps: {},
        _words: [],

        // Index de recherche normalisé + timestamp, calculés une fois par offre
        metaFor(job) {
            let m = this.meta.get(job.id);
            if (!m) {
                m = {
                    hay: normalizeText([
                        job.title_tr, job.title_fr, job.company, job.location,
                        job.snippet_tr, job.snippet_fr, job.category_tr, job.category_fr,
                        (job.tags_tr || []).join(' '), (job.tags_fr || []).join(' '),
                        job.working_lang, job.source, job.city, job.ccift ? 'ccift deik' : '',
                        (job.reasons_tr || []).join(' '), (job.reasons_fr || []).join(' '),
                        TRACK_SEARCH_WORDS[job.track] || ''
                    ].join(' ')),
                    // ts : date de publication (tri « plus récent ») ; seen : première détection (« Yeni »)
                    ts: parseIsoDate(job.posted_at) || parseAnyDate(job.discovered_at),
                    seen: parseAnyDate(job.discovered_at) || parseIsoDate(job.posted_at)
                };
                this.meta.set(job.id, m);
            }
            return m;
        },

        init() {
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                searchInput.addEventListener('input', (e) => {
                    clearTimeout(this.debounceTimer);
                    this.debounceTimer = setTimeout(() => {
                        this.state.query = (e.target.value || '').trim();
                        this.apply();
                    }, 180);
                });
                // Entrée : ferme le clavier Android
                searchInput.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter') searchInput.blur();
                });
            }
            const chips = document.getElementById('exChips');
            if (chips) {
                chips.addEventListener('click', (e) => {
                    const btn = e.target.closest('[data-chip]');
                    if (btn) this.onChip(btn.getAttribute('data-chip'));
                });
            }
            CardRenderer.init();
            FilterSheet.init();
        },

        onChip(key) {
            const s = this.state;
            if (key === 'all') {
                s.track = 'all';
                s.noFrenchOnly = false;
                s.status = 'all';
            } else if (key === 'nofr') {
                s.noFrenchOnly = !s.noFrenchOnly;
            } else if (key === 'fav') {
                s.status = s.status === 'fav' ? 'all' : 'fav';
            } else if (TRACK_SEARCH_WORDS[key]) {
                s.track = s.track === key ? 'all' : key;
            }
            haptic(5);
            this.apply();
        },

        setTrack(trackKey) {
            this.state.track = TRACK_SEARCH_WORDS[trackKey] ? trackKey : 'all';
            this.apply();
        },
        setDomain(domainKey) {
            this.state.domain = DOMAIN_KEYS.includes(domainKey) ? domainKey : 'all';
            this.apply();
        },
        setSort(sortKey) {
            this.state.sortBy = SORT_KEYS.includes(sortKey) ? sortKey : 'date_desc';
            this.apply();
        },
        setCategory(cat) {
            this.state.category = cat || 'all';
            this.apply();
        },
        toggleNoFrench() {
            this.setNoFrench(!this.state.noFrenchOnly);
        },
        setNoFrench(on) {
            this.state.noFrenchOnly = Boolean(on);
            this.apply();
        },
        toggleCcift() {
            this.setCcift(!this.state.cciftOnly);
        },
        setCcift(on) {
            this.state.cciftOnly = Boolean(on);
            this.apply();
        },
        setStatusFilter(status) {
            this.state.status = ['fav', 'tracked'].includes(status) ? status : 'all';
            this.apply();
        },

        resetAll() {
            Object.assign(this.state, {
                query: '', track: 'all', domain: 'all', category: 'all', status: 'all',
                noFrenchOnly: false, cciftOnly: false, sortBy: 'date_desc'
            });
            const searchInput = document.getElementById('searchInput');
            if (searchInput) searchInput.value = '';
            this.apply();
        },

        // Nombre de filtres actifs dans la bottom sheet (le tri n'est pas un filtre)
        activeSheetFilterCount() {
            return (this.state.domain !== 'all' ? 1 : 0) + (this.state.cciftOnly ? 1 : 0) + (this.state.category !== 'all' ? 1 : 0);
        },

        // Catégories historiques (API conservée : setCategory)
        matchCategory(job, cat) {
            const catTr = normalizeText(job.category_tr);
            const catFr = normalizeText(job.category_fr);
            switch (cat) {
                case 'institutions': return catTr.includes('kurum') || catFr.includes('institution') || catTr.includes('hukuk') || job.track === 'voie_1';
                case 'companies': return catTr.includes('holding') || catFr.includes('multinationale') || catTr.includes('buyuk turk') || job.track === 'voie_2';
                case 'logistics': return catTr.includes('lojistik') || catFr.includes('logistique') || job.domain === 'logistics';
                case 'tech': return catTr.includes('teknoloji') || catTr.includes('yazilim') || catFr.includes('tech') || catFr.includes('cloud') || job.track === 'voie_3' || job.domain === 'it';
                case 'pme': return catTr.includes('kobi') || catFr.includes('pme') || catTr.includes('saha') || job.domain === 'craft_pme';
                default: return true;
            }
        },

        // skip : critères ignorés (pour calculer les compteurs des pastilles)
        matches(job, skip = {}) {
            const s = this.state;
            const strId = String(job.id);
            if (!skip.track && s.track !== 'all' && job.track !== s.track) return false;
            if (s.domain !== 'all' && job.domain !== s.domain) return false;
            if (s.category !== 'all' && !this.matchCategory(job, s.category)) return false;
            if (!skip.nofr && s.noFrenchOnly && !job.no_french) return false;
            if (s.cciftOnly && !job.ccift) return false;
            if (!skip.status && s.status === 'fav' && !this._favs.has(strId)) return false;
            if (!skip.status && s.status === 'tracked' && !this._apps[strId]) return false;
            if (this._words.length) {
                const hay = this.metaFor(job).hay;
                if (!this._words.every(w => hay.includes(w))) return false;
            }
            return true;
        },

        sortJobs(list) {
            const arr = list.slice();
            if (this.state.sortBy === 'date_desc') {
                arr.sort((a, b) => (this.metaFor(b).ts - this.metaFor(a).ts) || (b.score - a.score) || (a.id - b.id));
            } else if (this.state.sortBy === 'company_asc') {
                arr.sort((a, b) => String(a.company || '').localeCompare(String(b.company || ''), 'tr', { sensitivity: 'base' }) || (a.id - b.id));
            } else {
                arr.sort((a, b) => (b.score - a.score) || (a.id - b.id));
            }
            return arr;
        },

        /**
         * Recalcule résultats + compteurs et met l'UI à jour.
         * opts.preserve : re-rend autant de cartes qu'avant (favori, langue) au lieu de revenir au 1er lot.
         * opts.render === false : compteurs seulement, la grille n'est pas touchée.
         */
        apply(opts = {}) {
            const jobs = getOffers(); // Keşfet : vraies annonces uniquement
            this._favs = StorageService.getFavorites();
            this._apps = StorageService.getApplications();
            this._words = normalizeText(this.state.query).split(/\s+/).filter(Boolean);

            const filtered = jobs.filter(j => this.matches(j));
            this.results = this.sortJobs(filtered);

            const counts = { all: 0, voie_1: 0, voie_2: 0, voie_3: 0, nofr: 0, fav: 0 };
            jobs.forEach(j => {
                if (this.matches(j, { track: true, nofr: true, status: true })) counts.all++;
                if (counts[j.track] !== undefined && this.matches(j, { track: true })) counts[j.track]++;
                if (j.no_french && this.matches(j, { nofr: true })) counts.nofr++;
                if (this._favs.has(String(j.id)) && this.matches(j, { status: true })) counts.fav++;
            });
            this.counts = counts;

            let countCcift = 0, countNoFrench = 0, countReloc = 0;
            filtered.forEach(j => {
                if (j.ccift) countCcift++;
                if (j.no_french) countNoFrench++;
                if (String(j.visa_evidence || '').trim()) countReloc++;
            });

            this.updateStatsCounters(filtered.length, countCcift, countNoFrench, countReloc);
            this.updateTrackBadges(counts);
            this.updateChips(counts);
            this.updateFilterButton();
            this.updateHeader();
            FilterSheet.sync();

            // 0 offre au total : état vide honnête (jamais de remplissage avec des fiches)
            const noOffers = jobs.length === 0;
            const pane = document.getElementById('tab-content-explore');
            if (pane) pane.classList.toggle('is-empty-feed', noOffers);
            const feedEmpty = document.getElementById('no-offers-box');
            if (feedEmpty) feedEmpty.hidden = !noOffers;
            const emptyEl = document.getElementById('no-results-box');
            if (emptyEl) emptyEl.hidden = noOffers || this.results.length > 0;
            const exploreBadge = document.getElementById('badge-explore-count');
            if (exploreBadge) exploreBadge.textContent = String(jobs.length);

            if (opts.render !== false) {
                CardRenderer.reset(this.results, opts.preserve ? CardRenderer.rendered : 0);
            }
        },

        updateChips(counts) {
            const s = this.state;
            document.querySelectorAll('#exChips [data-chip]').forEach(btn => {
                const key = btn.getAttribute('data-chip');
                let pressed = false;
                if (key === 'all') pressed = s.track === 'all' && !s.noFrenchOnly && s.status !== 'fav';
                else if (key === 'nofr') pressed = s.noFrenchOnly;
                else if (key === 'fav') pressed = s.status === 'fav';
                else pressed = s.track === key;
                btn.setAttribute('aria-pressed', pressed ? 'true' : 'false');
            });
            document.querySelectorAll('#exChips [data-count]').forEach(el => {
                const v = counts[el.getAttribute('data-count')];
                el.textContent = v === undefined ? '' : String(v);
            });
        },

        updateFilterButton() {
            const n = this.activeSheetFilterCount();
            const badge = document.getElementById('activeFilterCount');
            if (badge) {
                badge.textContent = String(n);
                badge.hidden = n === 0;
            }
            const btn = document.getElementById('openFiltersBtn');
            if (btn) btn.classList.toggle('has-filters', n > 0);
        },

        updateHeader() {
            const dict = getDict();
            const upd = document.getElementById('ex-updated');
            if (upd) {
                const iso = (window.FransaData && window.FransaData.generatedAt) || upd.getAttribute('data-generated-at') || '';
                const when = formatDateTime(iso, StorageService.getLang());
                upd.textContent = when ? dict.updatedAt.replace('{d}', when) : '';
            }
            const el = document.getElementById('ex-new-line');
            if (!el) return;
            const nNew = VisitTracker.countNew();
            el.innerHTML = nNew > 0 ? plural(dict, 'helloNewCount', nNew) : plural(dict, 'helloTotalCount', getOffers().length);
        },

        // Compteurs de l'onglet Rehber (blocs d'introduction)
        updateStatsCounters(visible, ccift, noFrench, reloc) {
            const set = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
            set('stat-total', visible);
            set('stat-ccift', ccift);
            set('stat-no-french', noFrench);
            set('stat-reloc', reloc);
        },

        updateTrackBadges(counts) {
            const set = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
            set('count-track-all', counts.all);
            set('count-track-1', counts.voie_1);
            set('count-track-2', counts.voie_2);
            set('count-track-3', counts.voie_3);
            document.querySelectorAll('.track-btn[data-track]').forEach(b => {
                b.classList.toggle('active', b.getAttribute('data-track') === this.state.track);
            });
        }
    };

    // --------------------------------------------------------------------------
    // 4bis. RENDU DES CARTES KEŞFET (lots de 20, IntersectionObserver)
    // --------------------------------------------------------------------------
    const CARD_BATCH = 20;
    const CardRenderer = {
        grid: null,
        sentinel: null,
        observer: null,
        list: [],
        rendered: 0,

        init() {
            this.grid = document.getElementById('cardsGrid');
            this.sentinel = document.getElementById('cardsSentinel');
            if (!this.grid) return;

            // Délégation : étoile favori / ouverture du détail (toute la carte)
            this.grid.addEventListener('click', (e) => {
                const star = e.target.closest('.jc-star');
                if (star) {
                    window.TrackerEngine.toggleBookmark(star.getAttribute('data-id'), e);
                    return;
                }
                const hit = e.target.closest('.jc-hit');
                if (hit) this.openDetail(hit.getAttribute('data-id'));
            });

            if (this.sentinel) {
                this.sentinel.addEventListener('click', () => this.renderMore());
                if ('IntersectionObserver' in window) {
                    this.observer = new IntersectionObserver((entries) => {
                        if (entries.some(en => en.isIntersecting)) this.renderMore();
                    }, { rootMargin: '0px 0px 800px 0px' });
                    this.observer.observe(this.sentinel);
                }
            }
        },

        openDetail(id) {
            haptic(5);
            if (window.BilateralDrawer && typeof window.BilateralDrawer.open === 'function') {
                window.BilateralDrawer.open(Number(id));
            }
        },

        // keepCount : nombre de cartes à re-rendre immédiatement (0 → premier lot)
        reset(list, keepCount = 0) {
            this.list = list || [];
            this.rendered = 0;
            if (!this.grid) return;
            this.grid.innerHTML = '';
            this.renderUpTo(Math.max(CARD_BATCH, keepCount));
        },

        renderMore() {
            if (this.rendered < this.list.length) this.renderUpTo(this.rendered + CARD_BATCH);
        },

        renderUpTo(n) {
            if (!this.grid) return;
            const end = Math.min(n, this.list.length);
            if (end > this.rendered) {
                const lang = StorageService.getLang();
                const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;
                const favs = StorageService.getFavorites();
                const html = this.list.slice(this.rendered, end).map(j => this.cardHtml(j, lang, dict, favs)).join('');
                this.grid.insertAdjacentHTML('beforeend', html);
                this.rendered = end;
            }
            const hasMore = this.rendered < this.list.length;
            if (this.sentinel) {
                this.sentinel.hidden = !hasMore;
                // Ré-observation : déclenche un nouveau contrôle si la sentinelle est encore visible
                if (this.observer && hasMore) {
                    this.observer.unobserve(this.sentinel);
                    this.observer.observe(this.sentinel);
                }
            }
        },

        cardHtml(job, lang, dict, favs) {
            const fr = lang === 'fr';
            const id = Number(job.id);
            const title = escapeHtml(fr ? (job.title_fr || job.title_tr) : job.title_tr);
            const meta = [job.company, job.location].filter(Boolean).map(escapeHtml).join(' · ');
            const isFav = favs.has(String(id));
            const favLabel = escapeHtml(isFav ? dict.favRemoveLabel : dict.favAddLabel);

            const trackNum = { voie_1: 1, voie_2: 2, voie_3: 3 }[job.track];
            const kapiText = trackNum
                ? `${dict.kapiShort.replace('{n}', trackNum)} · ${dict['kapiDesc' + trackNum]}`
                : dict.kapiOther;
            const newBadge = VisitTracker.isNew(job) ? `<span class="jc-new">${escapeHtml(dict.newBadge)}</span>` : '';

            // Âge de l'annonce (posted_at) + vérification récente (verified_at < 48 h)
            const age = ageLabel(job.posted_at, dict);
            const ageHtml = `<span class="jc-age${age ? '' : ' is-unknown'}"><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>${escapeHtml(age || dict.ageUnknown)}</span>`;
            const verifiedHtml = isFreshlyVerified(job.verified_at)
                ? `<span class="jc-verified" title="${escapeHtml(dict.verifiedTitle)}"><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>${escapeHtml(dict.verifiedShort)}</span>`
                : '';

            // 1-2 raisons appuyées sur l'annonce (à la place des tags génériques)
            const reasonsSrc = (fr ? job.reasons_fr : job.reasons_tr);
            const reasons = ((reasonsSrc && reasonsSrc.length) ? reasonsSrc : (job.reasons_tr || [])).filter(Boolean).slice(0, 2);
            const reasonsHtml = reasons.length
                ? `<ul class="jc-reasons">${reasons.map(r => `<li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>${escapeHtml(r)}</li>`).join('')}</ul>`
                : '';
            // Chip visa UNIQUEMENT si l'annonce elle-même en parle
            const visaHtml = String(job.visa_evidence || '').trim()
                ? `<div class="jc-pills"><span class="pill pill-ok"><svg class="ic" aria-hidden="true"><use href="#i-plane"/></svg><span class="pill-txt">${escapeHtml(dict.pillVisaEvidence)}</span></span></div>`
                : '';

            return `<article class="jc" data-id="${id}" data-track="${escapeHtml(job.track)}">` +
                `<div class="jc-top"><span class="jc-kapi kapi-${trackNum || 0}">${escapeHtml(kapiText)}</span>${newBadge}</div>` +
                `<h3 class="jc-title" id="jc-t-${id}">${title}</h3>` +
                `<p class="jc-meta">${meta}</p>` +
                `<div class="jc-dates">${ageHtml}${verifiedHtml}</div>` +
                reasonsHtml + visaHtml +
                `<button type="button" class="jc-hit" data-id="${id}" aria-labelledby="jc-t-${id}"></button>` +
                `<button type="button" class="jc-star" data-id="${id}" aria-pressed="${isFav}" aria-label="${favLabel}" title="${favLabel}"><svg class="ic" aria-hidden="true"><use href="#i-star"/></svg></button>` +
                `</article>`;
        },

        // Mise à jour en place des étoiles (sans re-rendu, préserve le scroll et le focus)
        syncStars(favs, dict) {
            if (!this.grid) return;
            this.grid.querySelectorAll('.jc-star').forEach(btn => {
                const isFav = favs.has(String(btn.getAttribute('data-id')));
                const label = isFav ? dict.favRemoveLabel : dict.favAddLabel;
                btn.setAttribute('aria-pressed', isFav ? 'true' : 'false');
                btn.setAttribute('aria-label', label);
                btn.title = label;
            });
        }
    };

    // --------------------------------------------------------------------------
    // 4bis-2. PISTES (kind="lead") : liste compacte dans le Rehber — PAS des annonces
    // --------------------------------------------------------------------------
    const LEADS_BATCH = 15;
    const LeadsRenderer = {
        bound: false,
        expanded: false,

        bind() {
            if (this.bound) return;
            const list = document.getElementById('leadsList');
            if (!list) return;
            this.bound = true;
            list.addEventListener('click', (e) => {
                const hit = e.target.closest('.lead-main');
                if (hit && window.BilateralDrawer && typeof window.BilateralDrawer.open === 'function') {
                    haptic(5);
                    window.BilateralDrawer.open(Number(hit.getAttribute('data-id')));
                }
            });
            const more = document.getElementById('leadsMore');
            if (more) more.addEventListener('click', () => { this.expanded = true; this.render(); });
        },

        render() {
            const list = document.getElementById('leadsList');
            if (!list) return;
            this.bind();
            const lang = StorageService.getLang();
            const dict = getDict();
            const leads = getLeads().slice().sort((a, b) =>
                String(a.company || '').localeCompare(String(b.company || ''), lang === 'fr' ? 'fr' : 'tr', { sensitivity: 'base' }));
            const count = document.getElementById('leads-count');
            if (count) count.textContent = String(leads.length);
            if (!leads.length) {
                list.innerHTML = `<li class="leads-empty">${escapeHtml(dict.leadsEmpty)}</li>`;
            } else {
                const shown = this.expanded ? leads : leads.slice(0, LEADS_BATCH);
                list.innerHTML = shown.map(l => this.rowHtml(l, lang, dict)).join('');
            }
            const more = document.getElementById('leadsMore');
            if (more) more.hidden = this.expanded || leads.length <= LEADS_BATCH;
        },

        rowHtml(lead, lang, dict) {
            const id = Number(lead.id);
            const trackNum = { voie_1: 1, voie_2: 2, voie_3: 3 }[lead.track];
            const kapi = trackNum ? dict.kapiShort.replace('{n}', trackNum) : dict.kapiOther;
            const city = lead.city || lead.location || '';
            const langText = langRequirementText(lead, lang, dict);
            const site = lead.url
                ? `<a class="lead-link" href="${escapeHtml(lead.url)}" target="_blank" rel="noopener" aria-label="${escapeHtml(dict.leadOpenSite + ' : ' + (lead.company || ''))}" title="${escapeHtml(dict.leadOpenSite)}"><svg class="ic" aria-hidden="true"><use href="#i-external-link"/></svg></a>`
                : '';
            return `<li class="lead-row">` +
                `<button type="button" class="lead-main" data-id="${id}" aria-label="${escapeHtml((lead.company || '') + ' · ' + dict.leadDetail)}">` +
                `<span class="lead-name">${escapeHtml(lead.company || lead.title_tr)}</span>` +
                `<span class="lead-meta"><span class="lead-kapi kapi-${trackNum || 0}">${escapeHtml(kapi)}</span>${city ? `<span>${escapeHtml(city)}</span>` : ''}</span>` +
                `<span class="lead-lang">${escapeHtml(langText)}</span>` +
                `</button>${site}</li>`;
        }
    };

    // --------------------------------------------------------------------------
    // 4ter. BOTTOM SHEET « FILTRELER / FILTRES » (contrat d'historique 'filters')
    // --------------------------------------------------------------------------
    const FILTER_SHEET_ID = 'filters';
    const FilterSheet = {
        el: null,
        lastFocus: null,
        closeTimer: null,

        init() {
            this.el = document.getElementById('filterSheet');
            const openBtn = document.getElementById('openFiltersBtn');
            if (openBtn) openBtn.addEventListener('click', () => this.open());
            if (!this.el) return;

            this.el.addEventListener('click', (e) => {
                if (e.target.closest('[data-sheet-close]')) { this.requestClose(); return; }
                const d = e.target.closest('[data-domain]');
                if (d) { FilterEngine.setDomain(d.getAttribute('data-domain')); return; }
                const s = e.target.closest('[data-sort]');
                if (s) { FilterEngine.setSort(s.getAttribute('data-sort')); return; }
                if (e.target.closest('#sheetResetBtn')) {
                    Object.assign(FilterEngine.state, { domain: 'all', category: 'all', cciftOnly: false, sortBy: 'date_desc' });
                    FilterEngine.apply();
                    return;
                }
                if (e.target.closest('#sheetApplyBtn')) this.requestClose();
            });

            const sw = document.getElementById('cciftSwitch');
            if (sw) sw.addEventListener('change', () => FilterEngine.setCcift(sw.checked));

            window.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.isOpen()) this.requestClose();
            });
            // Retour Android : fermeture sans toucher à l'historique
            window.addEventListener('popstate', (event) => {
                if (this.isOpen() && (event.state || {}).fransaOverlay !== FILTER_SHEET_ID) this.close();
            });
        },

        isOpen() {
            return Boolean(this.el && this.el.classList.contains('is-open'));
        },

        open() {
            if (!this.el || this.isOpen()) return;
            clearTimeout(this.closeTimer);
            this.lastFocus = document.activeElement;
            this.sync();
            this.el.hidden = false;
            document.body.classList.add('sheet-locked');
            // reflow puis animation d'entrée
            void this.el.offsetHeight;
            this.el.classList.add('is-open');
            HistoryRouter.pushOverlay(FILTER_SHEET_ID);
            haptic(8);
            const closeBtn = this.el.querySelector('.sheet-head [data-sheet-close]');
            if (closeBtn) setTimeout(() => closeBtn.focus({ preventScroll: true }), 50);
        },

        requestClose() {
            HistoryRouter.closeOverlay(FILTER_SHEET_ID, () => this.close());
        },

        close() {
            if (!this.el || !this.isOpen()) return;
            this.el.classList.remove('is-open');
            document.body.classList.remove('sheet-locked');
            this.closeTimer = setTimeout(() => { if (!this.isOpen()) this.el.hidden = true; }, 260);
            if (this.lastFocus && typeof this.lastFocus.focus === 'function') {
                try { this.lastFocus.focus({ preventScroll: true }); } catch (e) {}
            }
        },

        // Reflète l'état du moteur dans la sheet (pastilles, interrupteur, bouton CTA)
        sync() {
            if (!this.el) return;
            const s = FilterEngine.state;
            this.el.querySelectorAll('[data-domain]').forEach(b => b.setAttribute('aria-pressed', b.getAttribute('data-domain') === s.domain ? 'true' : 'false'));
            this.el.querySelectorAll('[data-sort]').forEach(b => b.setAttribute('aria-pressed', b.getAttribute('data-sort') === s.sortBy ? 'true' : 'false'));
            const sw = document.getElementById('cciftSwitch');
            if (sw) sw.checked = s.cciftOnly;
            const cta = document.getElementById('sheetApplyBtn');
            if (cta) {
                const dict = getDict();
                const n = FilterEngine.results.length;
                cta.textContent = n === 0 ? dict.showResultsZero : plural(dict, 'showResults', n);
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

            // Titre / entreprise / lieu lus dans FransaData (repli : enregistrement local)
            const job = getJob(app.id);
            const displayTitle = escapeHtml(job
                ? (lang === 'fr' ? (job.title_fr || job.title_tr) : job.title_tr)
                : (lang === 'fr' ? (app.title_fr || app.title) : app.title));
            const displayCompany = escapeHtml(job ? job.company : app.company);
            const displayLocation = escapeHtml(job ? job.location : app.location);
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
                        <strong class="kanban-company">${displayCompany}</strong>
                        <span class="kanban-location">📍 ${displayLocation}</span>
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
                    (app.kind !== 'lead' && app.relevance_score) ? `${app.relevance_score}%` : '',
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
            // Ids stables (hash URL) : migration douce des favoris / candidatures indexés
            IdMigration.run();

            // Nouveautés depuis la dernière visite (avant le premier rendu des cartes)
            VisitTracker.init();

            // Liaisons de la recherche, des pastilles, de la grille et de la bottom sheet
            FilterEngine.init();

            // Initialisation de la checklist du guide
            this.initChecklist();

            // Kanban
            KanbanTracker.init();

            // Langue mémorisée (silencieux) : traduit l'UI, rend le Kanban et les cartes Keşfet
            const savedLang = StorageService.getLang();
            this.applyLanguage(savedLang, { silent: true });

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
            if (searchInput) {
                searchInput.placeholder = dict.searchPlaceholder;
                searchInput.setAttribute('aria-label', dict.searchPlaceholder);
            }

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

            // Bouton de suivi & favoris des cartes (libellés + title/aria-label dans la langue courante)
            this.syncExplorerCards();

            // Rafraîchissement des cartes du Kanban
            KanbanTracker.render();
            // Re-rendu des cartes Keşfet dans la nouvelle langue (même nombre de cartes)
            FilterEngine.apply({ preserve: true });
            // Pistes (Rehber)
            LeadsRenderer.render();

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

        // Synchronise les étoiles des cartes rendues + badge de l'onglet Başvurularım
        syncExplorerCards() {
            const favorites = StorageService.getFavorites();
            const applications = StorageService.getApplications();
            CardRenderer.syncStars(favorites, getDict());

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
                        FilterEngine.apply({ preserve: true });
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

            const job = getJob(jobId);
            let existingApp = StorageService.getApplication(jobId);
            const lang = StorageService.getLang();
            const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;

            let title = '';
            let company = '';

            if (existingApp) {
                title = lang === 'fr' ? (existingApp.title_fr || existingApp.title) : existingApp.title;
                company = existingApp.company;
            } else if (job) {
                title = lang === 'fr' ? (job.title_fr || job.title_tr) : job.title_tr;
                company = job.company;
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

            const jobData = jobToAppData(getJob(jobId));

            StorageService.saveApplication(jobId, jobData, status, appliedDate, interviewDate, notes);

            const lang = StorageService.getLang();
            const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.tr;
            ToastService.show(dict.toastTrackUpdated, 'success');
            haptic();

            this.requestCloseModal();
            KanbanTracker.render();
            this.syncExplorerCards();
            FilterEngine.apply({ preserve: true });
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

        // Actions 1-clic (cartes Keşfet, Kanban, écran Détail)
        toggleBookmark(jobId, event) {
            if (event && typeof event.stopPropagation === 'function') event.stopPropagation();
            const isFav = StorageService.toggleFavorite(jobId);
            UIController.syncExplorerCards();
            KanbanTracker.render();
            // Filtre « Kaydedilenler » actif : la liste change ; sinon compteurs seulement (scroll préservé)
            FilterEngine.apply(FilterEngine.state.status === 'fav' ? { preserve: true } : { render: false });

            const dict = getDict();
            ToastService.show(isFav ? dict.toastFavAdded : dict.toastFavRemoved, isFav ? 'star' : 'info');
            if (isFav) haptic();
            window.dispatchEvent(new CustomEvent('fransa:favorite', { detail: { id: Number(jobId), isFavorite: isFav } }));
            return isFav;
        },

        isFavorite(jobId) {
            return StorageService.getFavorites().has(String(jobId));
        },

        // Crée ou met à jour la candidature dans le Kanban (statut par défaut : 'applied')
        addToTracker(jobId, status = 'applied') {
            const job = getJob(jobId);
            const existing = StorageService.getApplication(jobId);
            if (!job && !existing) return null;
            const newStatus = KanbanTracker.columns.includes(status) ? status : 'applied';
            const today = new Date().toISOString().split('T')[0];
            const appliedDate = (existing && existing.applied_date) || (newStatus !== 'saved' ? today : '');
            const app = StorageService.saveApplication(
                jobId,
                jobToAppData(job),
                newStatus,
                appliedDate,
                existing ? (existing.interview_date || '') : '',
                existing ? (existing.notes || '') : ''
            );

            // Pas de toast ici : l'appelant (écran Détail) affiche son propre message
            haptic(15);
            KanbanTracker.render();
            UIController.syncExplorerCards();
            FilterEngine.apply(FilterEngine.state.status === 'tracked' ? { preserve: true } : { render: false });
            window.dispatchEvent(new CustomEvent('fransa:tracker', { detail: { id: Number(jobId), status: newStatus } }));
            return app;
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
                FilterEngine.apply({ preserve: true });
                ToastService.show(dict.toastTrackerCleared, 'warning');
            }
        },

        switchTab(tabKey) {
            HistoryRouter.navigateToTab(tabKey);
        },

        // État vide Keşfet → section pistes du Rehber
        openLeads() {
            HistoryRouter.navigateToTab('guide');
            const sec = document.getElementById('leads-section');
            if (sec) requestAnimationFrame(() => sec.scrollIntoView({ block: 'start' }));
        },

        // Utilitaires partagés (drawer_cover_letter_module.js)
        stableIdFromUrl,
        ageLabel(postedAt) { return ageLabel(postedAt, getDict()); },
        isFreshlyVerified,
        langRequirementText(job) { return langRequirementText(job, StorageService.getLang(), getDict()); },

        setLanguage(lang) {
            UIController.applyLanguage(lang);
        },

        copyTemplate(textId, buttonEl) {
            UIController.copyTextToClipboard(textId, buttonEl);
        },

        shareWhatsApp(jobId) {
            const job = getJob(jobId);
            const title = job ? job.title_tr : 'Fransa İş Fırsatı';
            const company = job ? job.company : '';
            const url = (job && job.url) || window.location.href;
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
