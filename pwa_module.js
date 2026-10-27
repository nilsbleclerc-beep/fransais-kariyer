/**
 * Module PWA & Gestionnaire d'Installation Mobile & Actualisation
 * - Enregistrement du Service Worker
 * - Gestion de l'événement beforeinstallprompt (Android / Chrome / Edge)
 * - Détection et Guide interactif pour iOS (Safari Add to Home Screen)
 * - Actualisation en 1-clic (Mode Local via /api/refresh & Mode Cloud GitHub Pages)
 * - Modales en bottom sheet sur mobile + contrat d'historique partagé
 *   (bouton retour Android) : ids 'pwa-install' et 'pwa-cloud'
 */

(function (window) {
    'use strict';

    let deferredPrompt = null;
    let isRefreshing = false;
    let refreshPollInterval = null;

    const BANNER_SNOOZE_MS = 3 * 24 * 60 * 60 * 1000;

    function getLang() {
        try {
            return localStorage.getItem('bilateral_lang') || 'tr';
        } catch (e) {
            return 'tr';
        }
    }

    function isBannerSnoozed() {
        try {
            const dismissedTime = localStorage.getItem('pwa_banner_dismissed_time');
            return !!dismissedTime && (Date.now() - parseInt(dismissedTime, 10)) <= BANNER_SNOOZE_MS;
        } catch (e) {
            return false;
        }
    }

    // --------------------------------------------------------------------------
    // CONTRAT D'HISTORIQUE PARTAGÉ (identique à drawer_cover_letter_module.js)
    // Ouvrir : pushState({ fransaOverlay: id }) ; fermer via l'UI : history.back()
    // si l'état courant est le nôtre, sinon fermeture directe ; popstate : fermer
    // l'overlay ouvert dont l'id n'est plus l'état courant, sans toucher à l'historique.
    // --------------------------------------------------------------------------
    const PWA_OVERLAYS = {
        'pwa-install': 'pwa-ios-modal',
        'pwa-cloud': 'cloud-info-modal'
    };
    let pendingBack = false;
    let pendingBackTimer = null;

    function overlayEl(id) {
        return document.getElementById(PWA_OVERLAYS[id]);
    }

    function isPwaOverlayOpen(id) {
        const el = overlayEl(id);
        return !!(el && el.style.display === 'flex');
    }

    function syncPwaScrollLock() {
        const anyOpen = Object.keys(PWA_OVERLAYS).some(isPwaOverlayOpen);
        document.documentElement.classList.toggle('pwa-scroll-lock', anyOpen);
    }

    function showPwaOverlay(id) {
        const el = overlayEl(id);
        if (!el) return false;
        const wasOpen = isPwaOverlayOpen(id);
        el.style.display = 'flex';
        syncPwaScrollLock();
        if (!wasOpen) {
            try {
                if (!(history.state && history.state.fransaOverlay === id)) {
                    history.pushState({ fransaOverlay: id }, '');
                }
            } catch (e) { /* History API indisponible */ }
            const closeBtn = el.querySelector('.pwa-modal-close');
            if (closeBtn) {
                setTimeout(() => {
                    try { closeBtn.focus({ preventScroll: true }); } catch (e) { /* noop */ }
                }, 60);
            }
        }
        return true;
    }

    function hidePwaOverlay(id) {
        const el = overlayEl(id);
        if (el) el.style.display = 'none';
        syncPwaScrollLock();
    }

    function requestClosePwaOverlay(id) {
        if (!isPwaOverlayOpen(id)) return;
        let ownsState = false;
        try {
            ownsState = !!(history.state && history.state.fransaOverlay === id);
        } catch (e) {
            ownsState = false;
        }
        if (!ownsState) {
            hidePwaOverlay(id);
            return;
        }
        if (pendingBack) return;
        pendingBack = true;
        clearTimeout(pendingBackTimer);
        pendingBackTimer = setTimeout(() => { pendingBack = false; }, 800);
        history.back();
    }

    const PWAHandler = {
        // État de l'appareil
        isIOS: /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream,
        isAndroid: /Android/i.test(navigator.userAgent),
        isStandalone: window.matchMedia('(display-mode: standalone)').matches
            || window.matchMedia('(display-mode: fullscreen)').matches
            || window.navigator.standalone === true,

        /**
         * Initialisation complète au chargement de la page
         */
        init() {
            this.registerServiceWorker();
            this.setupInstallListeners();
            this.checkDisplayMode();
            this.setupLanguageWatchers();
            this.setupOverlayListeners();
            this.checkServerStatus();
        },

        /**
         * Retour Android (popstate), Échap et clic sur le fond pour les modales PWA
         */
        setupOverlayListeners() {
            window.addEventListener('popstate', (event) => {
                pendingBack = false;
                clearTimeout(pendingBackTimer);
                const current = (event.state || {}).fransaOverlay;
                Object.keys(PWA_OVERLAYS).forEach((id) => {
                    if (isPwaOverlayOpen(id) && current !== id) {
                        hidePwaOverlay(id);
                    }
                });
            });

            document.addEventListener('keydown', (e) => {
                if (e.key !== 'Escape') return;
                Object.keys(PWA_OVERLAYS).forEach((id) => requestClosePwaOverlay(id));
            });

            Object.keys(PWA_OVERLAYS).forEach((id) => {
                const el = overlayEl(id);
                if (!el) return;
                el.addEventListener('click', (e) => {
                    if (e.target === el) requestClosePwaOverlay(id);
                });
            });
        },

        /**
         * Enregistrement du Service Worker avec revalidation
         */
        registerServiceWorker() {
            if ('serviceWorker' in navigator) {
                window.addEventListener('load', () => {
                    navigator.serviceWorker.register('./sw.js', { scope: './' })
                        .then((reg) => {
                            console.log('[PWA] Service Worker enregistré avec succès (Scope: ' + reg.scope + ')');
                            
                            // Détection de mise à jour du Service Worker
                            reg.addEventListener('updatefound', () => {
                                const newWorker = reg.installing;
                                newWorker.addEventListener('statechange', () => {
                                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                        console.log('[PWA] Nouvelle version prête');
                                        if (window.TrackerEngine && window.TrackerEngine.Toast) {
                                            const lang = getLang();
                                            const msg = lang === 'fr' 
                                                ? "Mise à jour disponible ! Rafraîchissez pour voir les nouveautés." 
                                                : "Uygulama güncellemesi hazır! Yeni ilanlar için sayfayı yenileyin.";
                                            window.TrackerEngine.Toast.show(msg, 'info', 5000);
                                        }
                                    }
                                });
                            });
                        })
                        .catch((err) => {
                            console.warn('[PWA] Échec enregistrement Service Worker:', err);
                        });
                });
            }
        },

        /**
         * Écoute de l'événement d'installation PWA
         */
        setupInstallListeners() {
            // Android / Desktop Chrome / Edge
            window.addEventListener('beforeinstallprompt', (e) => {
                // Empêche l'affichage automatique natif pour contrôler l'expérience
                e.preventDefault();
                deferredPrompt = e;
                console.log('[PWA] beforeinstallprompt capturé');

                // Si pas encore installé et pas dismissé récemment, affiche les boutons
                if (!this.isStandalone) {
                    this.showInstallUI();
                }
            });

            // Détection si l'application vient d'être installée
            window.addEventListener('appinstalled', () => {
                console.log('[PWA] Application installée avec succès !');
                deferredPrompt = null;
                this.hideInstallUI();
                if (window.TrackerEngine && window.TrackerEngine.Toast) {
                    const lang = getLang();
                    const msg = lang === 'fr'
                        ? "🎉 Application installée sur votre écran d'accueil !"
                        : "🎉 Uygulama başarıyla ana ekranınıza yüklendi !";
                    window.TrackerEngine.Toast.show(msg, 'success', 5000);
                }
            });

            // iOS Safari (secondaire) : pas de beforeinstallprompt, on propose le guide manuel
            if (this.isIOS && !this.isStandalone && !isBannerSnoozed()) {
                this.showInstallUI();
            }
        },

        checkDisplayMode() {
            if (this.isStandalone) {
                console.log('[PWA] Mode Standalone détecté (Application installée)');
                this.hideInstallUI();
            }
        },

        showInstallUI() {
            const btn = document.getElementById('pwaInstallBtn');
            const banner = document.getElementById('mobileInstallBanner');
            if (btn) btn.style.display = 'inline-flex';
            if (banner && !isBannerSnoozed()) {
                banner.style.display = 'flex';
            }
        },

        hideInstallUI() {
            const btn = document.getElementById('pwaInstallBtn');
            const banner = document.getElementById('mobileInstallBanner');
            if (btn) btn.style.display = 'none';
            if (banner) banner.style.display = 'none';
        },

        dismissBanner() {
            const banner = document.getElementById('mobileInstallBanner');
            if (banner) banner.style.display = 'none';
            try {
                localStorage.setItem('pwa_banner_dismissed_time', Date.now().toString());
            } catch (e) { /* stockage indisponible */ }
        },

        /**
         * Déclenche l'installation de l'application
         */
        promptInstall() {
            // 1. Android / Chrome (prioritaire) : fenêtre native d'installation en 1 clic
            if (deferredPrompt) {
                const promptEvent = deferredPrompt;
                deferredPrompt = null; // un beforeinstallprompt ne peut servir qu'une fois
                promptEvent.prompt();
                promptEvent.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('[PWA] Utilisateur a accepté l\'installation');
                    } else {
                        console.log('[PWA] Utilisateur a refusé l\'installation');
                    }
                }).catch(() => { /* noop */ });
                return;
            }

            // 2. Pas d'invite native disponible : guide manuel (Android Chrome d'abord, iOS ensuite)
            this.openInstallGuide();
        },

        /**
         * Guide d'installation manuel : étapes Android (menu ⋮ de Chrome) mises en avant,
         * étapes iOS (Safari) affichées en premier uniquement sur iPhone / iPad.
         */
        openInstallGuide() {
            const modal = overlayEl('pwa-install');
            if (modal) {
                modal.classList.toggle('pwa-platform-ios', this.isIOS);
                modal.classList.toggle('pwa-platform-android', !this.isIOS);
                // Sur iOS : étapes Safari dépliées (étapes Android masquées en CSS)
                const iosSteps = document.getElementById('pwa-steps-ios');
                if (iosSteps) iosSteps.open = this.isIOS;
            }
            showPwaOverlay('pwa-install');
        },

        closeInstallGuide() {
            requestClosePwaOverlay('pwa-install');
        },

        // Alias rétro-compatibles (appelés depuis le markup existant)
        openIosModal() {
            this.openInstallGuide();
        },

        closeIosModal() {
            this.closeInstallGuide();
        },

        /**
         * SYSTÈME DE RAFRAÎCHISSEMENT (LOCAL & CLOUD)
         */
        async triggerRefresh() {
            if (isRefreshing) return;

            const btn = document.getElementById('refreshBtn');
            const icon = document.getElementById('refreshBtnIcon');
            const text = document.getElementById('refreshBtnText');
            const lang = getLang();

            isRefreshing = true;
            if (btn) btn.classList.add('loading');
            if (icon) icon.classList.add('spin-animation');
            if (text) {
                text.textContent = (lang === 'fr') ? "Actualisation..." : "Yenileniyor...";
            }

            if (window.TrackerEngine && window.TrackerEngine.Toast) {
                const toastMsg = (lang === 'fr') 
                    ? "⏳ Recherche des nouvelles offres bilatérales en cours..." 
                    : "⏳ Güncel Türkiye-Fransa iş ilanları taranıyor...";
                window.TrackerEngine.Toast.show(toastMsg, 'info', 3500);
            }

            try {
                // Tentative d'appel à l'API locale /api/refresh
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 4000);

                const response = await fetch('/api/refresh', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    signal: controller.signal
                });
                clearTimeout(timeoutId);

                if (response.ok) {
                    const data = await response.json();
                    console.log('[Refresh] Réponse serveur local:', data);
                    // Démarrage du polling de statut
                    this.pollRefreshStatus();
                    return;
                } else {
                    throw new Error("HTTP " + response.status);
                }
            } catch (err) {
                console.log('[Refresh] Pas de serveur local /api/refresh détecté (Mode Cloud/GitHub Pages ou Offline).');
                // Mode Cloud / GitHub Pages ou fichier local
                this.handleCloudOrOfflineRefresh(lang);
            }
        },

        /**
         * Surveillance de l'avancement du rafraîchissement local
         */
        pollRefreshStatus() {
            let attempts = 0;
            const maxAttempts = 45; // 90 secondes max

            if (refreshPollInterval) clearInterval(refreshPollInterval);

            refreshPollInterval = setInterval(async () => {
                attempts++;
                try {
                    const res = await fetch('/api/status?t=' + Date.now());
                    if (res.ok) {
                        const statusData = await res.json();
                        if (statusData.status === 'idle') {
                            clearInterval(refreshPollInterval);
                            refreshPollInterval = null;
                            this.finishRefreshSuccess(statusData.job_count);
                            return;
                        }
                    }
                } catch (e) {
                    // Erreur silencieuse de polling
                }

                if (attempts >= maxAttempts) {
                    clearInterval(refreshPollInterval);
                    refreshPollInterval = null;
                    this.finishRefreshSuccess();
                }
            }, 2000);
        },

        /**
         * Gestion du rafraîchissement en mode Cloud (GitHub Pages) ou Statique
         */
        async handleCloudOrOfflineRefresh(lang) {
            // Tente de récupérer la version la plus fraîche du JSON avec cache-busting
            try {
                const jsonRes = await fetch('./offres_france_turquie.json?t=' + Date.now(), { cache: 'no-cache' });
                if (jsonRes.ok) {
                    const jobs = await jsonRes.json();
                    console.log('[Refresh Cloud] Données récupérées:', jobs.length, 'offres');
                }
            } catch (e) {
                console.log('[Refresh Cloud] Erreur récupération json', e);
            }

            setTimeout(() => {
                this.resetRefreshButton();
                isRefreshing = false;

                // Affichage d'un modal explicatif bienveillant
                this.openCloudInfoModal(lang);
            }, 1200);
        },

        finishRefreshSuccess(jobCount) {
            this.resetRefreshButton();
            isRefreshing = false;

            const lang = getLang();
            const countMsg = jobCount ? ` (${jobCount} ilan)` : '';
            const msg = (lang === 'fr')
                ? `✅ Liste des offres mise à jour avec succès ! Rechargement...`
                : `✅ İş ilanları başarıyla güncellendi ! Sayfa yenileniyor...`;

            if (window.TrackerEngine && window.TrackerEngine.Toast) {
                window.TrackerEngine.Toast.show(msg, 'success', 3000);
            }

            // Rechargement propre pour appliquer les nouvelles données
            setTimeout(() => {
                window.location.reload();
            }, 1200);
        },

        resetRefreshButton() {
            const btn = document.getElementById('refreshBtn');
            const icon = document.getElementById('refreshBtnIcon');
            const text = document.getElementById('refreshBtnText');
            const lang = getLang();

            if (btn) btn.classList.remove('loading');
            if (icon) icon.classList.remove('spin-animation');
            if (text) {
                text.textContent = (lang === 'fr') ? "Actualiser" : "Şimdi Yenile";
            }
        },

        openCloudInfoModal(lang) {
            if (!showPwaOverlay('pwa-cloud')) {
                // Fallback toast si modal absent
                const toastMsg = (lang === 'fr')
                    ? "☁️ Mode Cloud : Les offres s'actualisent automatiquement chaque jour à 08:00 (TR) via GitHub Actions !"
                    : "☁️ Bulut Modu: İlanlar her gün saat 08:00'de otomatik taranır. PC'de anında yenilemek için 'Lancer_Application.bat'ı çalıştırabilirsiniz.";
                if (window.TrackerEngine && window.TrackerEngine.Toast) {
                    window.TrackerEngine.Toast.show(toastMsg, 'info', 6000);
                }
            }
        },

        closeCloudInfoModal() {
            requestClosePwaOverlay('pwa-cloud');
        },

        /**
         * Vérification silencieuse de l'état du serveur local au démarrage
         */
        async checkServerStatus() {
            try {
                const res = await fetch('/api/status', { method: 'GET' });
                if (res.ok) {
                    const data = await res.json();
                    console.log('[PWA] Serveur local actif:', data);
                    const refreshBtn = document.getElementById('refreshBtn');
                    if (refreshBtn) {
                        refreshBtn.title = "Serveur local actif - Cliquez pour rescanner en direct";
                    }
                }
            } catch (e) {
                // Non local, fonctionnement statique/cloud nominal
            }
        },

        /**
         * Met à jour les textes traduits des éléments PWA selon la langue.
         * Portée limitée au bandeau et aux modales PWA (le reste de la page est déjà
         * traduit par TrackerEngine.applyLanguage). Aucun toast n'est émis ici :
         * la notification de changement de langue n'appartient qu'à l'action utilisateur.
         */
        setupLanguageWatchers() {
            const updateTexts = () => {
                const lang = getLang();
                document.querySelectorAll('#mobileInstallBanner [data-tr][data-fr], #pwa-ios-modal [data-tr][data-fr], #cloud-info-modal [data-tr][data-fr]').forEach((el) => {
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
            };

            // Écoute de l'événement personnalisé + passage initial
            window.addEventListener('languageChanged', updateTexts);
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', updateTexts);
            } else {
                updateTexts();
            }
        }
    };

    window.PWAHandler = PWAHandler;

    // Démarrage automatique
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => PWAHandler.init());
    } else {
        PWAHandler.init();
    }

})(window);
