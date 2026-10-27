/**
 * Module PWA & Gestionnaire d'Installation Mobile & Actualisation
 * - Enregistrement du Service Worker
 * - Gestion de l'événement beforeinstallprompt (Android / Chrome / Edge)
 * - Détection et Guide interactif pour iOS (Safari Add to Home Screen)
 * - Actualisation en 1-clic (Mode Local via /api/refresh & Mode Cloud GitHub Pages)
 */

(function (window) {
    'use strict';

    let deferredPrompt = null;
    let isRefreshing = false;
    let refreshPollInterval = null;

    const PWAHandler = {
        // État de l'appareil
        isIOS: /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream,
        isStandalone: window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true,

        /**
         * Initialisation complète au chargement de la page
         */
        init() {
            this.registerServiceWorker();
            this.setupInstallListeners();
            this.checkDisplayMode();
            this.setupLanguageWatchers();
            this.checkServerStatus();
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
                                            const lang = localStorage.getItem('bilateral_lang') || 'tr';
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
                    const lang = localStorage.getItem('bilateral_lang') || 'tr';
                    const msg = lang === 'fr'
                        ? "🎉 Application installée sur votre écran d'accueil !"
                        : "🎉 Uygulama başarıyla ana ekranınıza yüklendi !";
                    window.TrackerEngine.Toast.show(msg, 'success', 5000);
                }
            });

            // Pour iOS Safari, on affiche le bouton d'installation si non standalone
            if (this.isIOS && !this.isStandalone) {
                // Vérifier si dismissé depuis moins de 3 jours
                const dismissedTime = localStorage.getItem('pwa_banner_dismissed_time');
                const now = Date.now();
                if (!dismissedTime || (now - parseInt(dismissedTime, 10)) > (3 * 24 * 60 * 60 * 1000)) {
                    this.showInstallUI();
                }
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
            if (banner) {
                const dismissedTime = localStorage.getItem('pwa_banner_dismissed_time');
                const now = Date.now();
                if (!dismissedTime || (now - parseInt(dismissedTime, 10)) > (3 * 24 * 60 * 60 * 1000)) {
                    banner.style.display = 'flex';
                }
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
            localStorage.setItem('pwa_banner_dismissed_time', Date.now().toString());
        },

        /**
         * Déclenche l'installation de l'application
         */
        promptInstall() {
            if (this.isIOS) {
                // Sur iOS, afficher la modal avec le guide visuel Safari
                this.openIosModal();
                return;
            }

            if (deferredPrompt) {
                // Sur Android / Chrome, déclenche la fenêtre native 1-clic
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('[PWA] Utilisateur a accepté l\'installation');
                    } else {
                        console.log('[PWA] Utilisateur a refusé l\'installation');
                    }
                    deferredPrompt = null;
                });
            } else {
                // Fallback générique
                this.openIosModal();
            }
        },

        openIosModal() {
            const modal = document.getElementById('pwa-ios-modal');
            if (modal) modal.style.display = 'flex';
        },

        closeIosModal() {
            const modal = document.getElementById('pwa-ios-modal');
            if (modal) modal.style.display = 'none';
        },

        /**
         * SYSTÈME DE RAFRAÎCHISSEMENT (LOCAL & CLOUD)
         */
        async triggerRefresh() {
            if (isRefreshing) return;

            const btn = document.getElementById('refreshBtn');
            const icon = document.getElementById('refreshBtnIcon');
            const text = document.getElementById('refreshBtnText');
            const lang = localStorage.getItem('bilateral_lang') || 'tr';

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

            const lang = localStorage.getItem('bilateral_lang') || 'tr';
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
            const lang = localStorage.getItem('bilateral_lang') || 'tr';

            if (btn) btn.classList.remove('loading');
            if (icon) icon.classList.remove('spin-animation');
            if (text) {
                text.textContent = (lang === 'fr') ? "Actualiser" : "Şimdi Yenile";
            }
        },

        openCloudInfoModal(lang) {
            const modal = document.getElementById('cloud-info-modal');
            if (modal) {
                modal.style.display = 'flex';
            } else {
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
            const modal = document.getElementById('cloud-info-modal');
            if (modal) modal.style.display = 'none';
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
         * Met à jour les textes traduits de la PWA selon la langue
         */
        setupLanguageWatchers() {
            const updateTexts = () => {
                const lang = localStorage.getItem('bilateral_lang') || 'tr';
                document.querySelectorAll('[data-tr][data-fr]').forEach((el) => {
                    const text = (lang === 'fr') ? el.getAttribute('data-fr') : el.getAttribute('data-tr');
                    if (text) {
                        // Si le nœud a des enfants d'icône, ne remplacer que le texte
                        if (el.children.length === 0) {
                            el.textContent = text;
                        }
                    }
                });
            };

            // Écoute de l'événement personnalisé ou polling léger
            window.addEventListener('languageChanged', updateTexts);
            document.addEventListener('DOMContentLoaded', updateTexts);
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
