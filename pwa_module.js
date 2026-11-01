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

    // --------------------------------------------------------------------------
    // FORÇAGE DU ROBOT EN LIGNE (GitHub Actions, workflow_dispatch)
    // --------------------------------------------------------------------------
    const GH_API = 'https://api.github.com/repos/nilsbleclerc-beep/fransais-kariyer';
    const GH_WORKFLOW = 'refresh.yml';
    const GH_BRANCH = 'master';
    const GH_TOKEN_KEY = 'fransa_gh_token';

    function isLocalHost() {
        return ['localhost', '127.0.0.1', '[::1]'].includes(window.location.hostname);
    }

    function getGithubToken() {
        try { return localStorage.getItem(GH_TOKEN_KEY) || ''; } catch (e) { return ''; }
    }

    function setGithubToken(value) {
        try {
            if (value) localStorage.setItem(GH_TOKEN_KEY, value);
            else localStorage.removeItem(GH_TOKEN_KEY);
        } catch (e) { /* stockage indisponible : le bouton reste en mode information */ }
    }

    function githubHeaders(token) {
        return {
            'Accept': 'application/vnd.github+json',
            'Authorization': `Bearer ${token}`,
            'X-GitHub-Api-Version': '2022-11-28'
        };
    }

    function currentGeneratedAt() {
        return (window.FransaData && window.FransaData.generatedAt) || '';
    }

    // Date de génération de la version actuellement publiée (sans passer par le cache)
    async function fetchPublishedGeneratedAt() {
        try {
            const res = await fetch('./index.html?t=' + Date.now(), { cache: 'no-store' });
            if (!res.ok) return '';
            const m = /id="fransa-jobs"[^>]*data-generated-at="([^"]+)"/.exec(await res.text());
            return m ? m[1] : '';
        } catch (e) {
            return '';
        }
    }

    // Recharge en vidant le cache du service worker, pour afficher tout de suite la nouvelle version
    async function reloadFresh() {
        try {
            if ('caches' in window) {
                const keys = await caches.keys();
                await Promise.all(keys.map((k) => caches.delete(k)));
            }
        } catch (e) { /* rechargement simple */ }
        window.location.reload();
    }

    // Lien d'installation de la clé (« …/index.html#gh=github_pat_… ») envoyé depuis un autre téléphone :
    // la clé est enregistrée puis retirée de l'adresse avant que le routeur d'onglets ne lise le hash.
    // Le fragment # n'est jamais envoyé au serveur.
    let tokenImportedFromLink = false;
    (function importTokenFromLink() {
        const m = /^#gh=((?:github_pat_|ghp_)[A-Za-z0-9_]{20,})$/.exec(window.location.hash || '');
        if (!m) return;
        setGithubToken(m[1]);
        tokenImportedFromLink = true;
        try {
            history.replaceState(history.state, '', window.location.pathname + window.location.search);
        } catch (e) { /* adresse laissée telle quelle */ }
    })();

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
            if (tokenImportedFromLink) {
                const lang = getLang();
                setTimeout(() => this.toast(lang === 'fr'
                    ? "✅ Bouton Actualiser activé sur ce téléphone."
                    : "✅ Yenile butonu bu telefonda etkinleştirildi.", 'success', 5000), 800);
            }
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

            // En ligne (GitHub Pages) : il n'y a pas de serveur, on force un scan via GitHub Actions
            if (!isLocalHost()) {
                return this.cloudRefresh(lang);
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
         * Gestion du rafraîchissement en mode Cloud / statique (fichier ouvert sans serveur)
         */
        async handleCloudOrOfflineRefresh(lang) {
            if (await this.loadPublishedVersionIfNewer(lang)) return;
            this.resetRefreshButton();
            isRefreshing = false;
            this.openCloudInfoModal(lang);
        },

        /**
         * FORÇAGE EN LIGNE (GitHub Pages) :
         * 1. si une version plus récente est déjà publiée, on la charge tout de suite ;
         * 2. sinon, avec la clé GitHub enregistrée sur cet appareil, on lance le robot (workflow_dispatch),
         *    on suit son exécution puis la publication, et on recharge l'app avec les nouvelles offres.
         */
        async cloudRefresh(lang) {
            if (await this.loadPublishedVersionIfNewer(lang)) return;

            const token = getGithubToken();
            if (!token) {
                this.resetRefreshButton();
                isRefreshing = false;
                this.openCloudInfoModal(lang);
                return;
            }

            const before = currentGeneratedAt();
            const startedAt = Date.now();
            let resp = null;
            try {
                resp = await fetch(`${GH_API}/actions/workflows/${GH_WORKFLOW}/dispatches`, {
                    method: 'POST',
                    headers: githubHeaders(token),
                    body: JSON.stringify({ ref: GH_BRANCH })
                });
            } catch (e) {
                resp = null;
            }
            if (!resp || resp.status !== 204) {
                const status = resp ? resp.status : 0;
                if (status === 401 || status === 403 || status === 404) setGithubToken('');
                this.failRefresh(lang, status === 401 || status === 403 || status === 404
                    ? (lang === 'fr' ? "❌ Clé GitHub refusée : enregistre-la à nouveau." : "❌ GitHub anahtarı reddedildi: lütfen yeniden kaydet.")
                    : (lang === 'fr' ? "❌ Impossible de joindre GitHub (connexion ?)." : "❌ GitHub'a ulaşılamadı (internet bağlantısı?)."),
                    status === 401 || status === 403 || status === 404);
                return;
            }

            this.toast(lang === 'fr'
                ? "🚀 Recherche lancée : nouvelles offres dans ~3 minutes. Tu peux continuer à utiliser l'app."
                : "🚀 Tarama başladı: yeni ilanlar ~3 dakika içinde. Uygulamayı kullanmaya devam edebilirsin.", 'info', 6000);
            this.followCloudRun(lang, token, startedAt, before);
        },

        followCloudRun(lang, token, startedAt, before) {
            const text = document.getElementById('refreshBtnText');
            const deadline = startedAt + 12 * 60 * 1000;
            let runDone = false;

            if (refreshPollInterval) clearInterval(refreshPollInterval);
            refreshPollInterval = setInterval(async () => {
                const elapsed = Math.round((Date.now() - startedAt) / 1000);
                if (text) text.textContent = `${lang === 'fr' ? 'Recherche' : 'Taranıyor'} ${Math.floor(elapsed / 60)}:${String(elapsed % 60).padStart(2, '0')}`;
                if (Date.now() > deadline) {
                    clearInterval(refreshPollInterval);
                    refreshPollInterval = null;
                    this.failRefresh(lang, lang === 'fr'
                        ? "⏳ La recherche prend plus de temps que prévu : les offres arriveront d'elles-mêmes à la prochaine ouverture."
                        : "⏳ Tarama beklenenden uzun sürüyor: ilanlar bir sonraki açılışta kendiliğinden gelecek.");
                    return;
                }
                try {
                    if (!runDone) {
                        const r = await fetch(`${GH_API}/actions/workflows/${GH_WORKFLOW}/runs?event=workflow_dispatch&per_page=1`,
                            { headers: githubHeaders(token), cache: 'no-store' });
                        const run = r.ok ? ((await r.json()).workflow_runs || [])[0] : null;
                        if (run && Date.parse(run.created_at) >= startedAt - 60000 && run.status === 'completed') {
                            if (run.conclusion !== 'success') {
                                clearInterval(refreshPollInterval);
                                refreshPollInterval = null;
                                this.failRefresh(lang, lang === 'fr'
                                    ? "❌ Le robot a rencontré une erreur. Les offres actuelles restent affichées."
                                    : "❌ Robot bir hatayla karşılaştı. Mevcut ilanlar gösterilmeye devam ediyor.");
                                return;
                            }
                            runDone = true;
                        }
                    }
                    // Après le robot, GitHub Pages republie le site (~1 min) : on attend une version plus récente
                    if (runDone) {
                        const published = await fetchPublishedGeneratedAt();
                        if (published && published > before) {
                            clearInterval(refreshPollInterval);
                            refreshPollInterval = null;
                            await reloadFresh();
                        } else if (published && Date.now() - startedAt > 8 * 60 * 1000) {
                            // Aucune nouvelle publication : le robot n'a trouvé aucun changement
                            clearInterval(refreshPollInterval);
                            refreshPollInterval = null;
                            this.resetRefreshButton();
                            isRefreshing = false;
                            this.toast(lang === 'fr' ? "✅ Recherche terminée : aucune nouvelle offre depuis la dernière fois."
                                : "✅ Tarama bitti: son seferden beri yeni ilan yok.", 'success', 5000);
                        }
                    }
                } catch (e) {
                    // réseau intermittent : on réessaie au tour suivant
                }
            }, 15000);
        },

        async loadPublishedVersionIfNewer(lang) {
            const published = await fetchPublishedGeneratedAt();
            const current = currentGeneratedAt();
            if (published && current && published > current) {
                this.toast(lang === 'fr' ? "✨ Nouvelles offres disponibles : chargement…" : "✨ Yeni ilanlar var: yükleniyor…", 'success', 2500);
                await reloadFresh();
                return true;
            }
            return false;
        },

        failRefresh(lang, message, reopenSettings) {
            this.resetRefreshButton();
            isRefreshing = false;
            this.toast(message, 'warning', 6000);
            if (reopenSettings) this.openCloudInfoModal(lang);
        },

        toast(message, type, duration) {
            if (window.TrackerEngine && window.TrackerEngine.Toast) window.TrackerEngine.Toast.show(message, type, duration);
        },

        // Clé GitHub (fine-grained, « Actions : lecture et écriture » sur ce seul dépôt), gardée sur cet appareil
        saveGithubToken() {
            const input = document.getElementById('ghTokenInput');
            const value = (input && input.value || '').trim();
            const lang = getLang();
            if (!/^(github_pat_|ghp_)[A-Za-z0-9_]{20,}$/.test(value)) {
                this.toast(lang === 'fr' ? "Cette clé ne ressemble pas à une clé GitHub (github_pat_…)." : "Bu bir GitHub anahtarına benzemiyor (github_pat_…).", 'warning', 5000);
                return;
            }
            setGithubToken(value);
            if (input) input.value = '';
            this.renderCloudTokenState();
            this.toast(lang === 'fr' ? "✅ Clé enregistrée sur cet appareil. Le bouton Actualiser lance maintenant une vraie recherche."
                : "✅ Anahtar bu cihaza kaydedildi. Yenile butonu artık gerçek bir tarama başlatıyor.", 'success', 5000);
        },

        // Envoie à un autre téléphone un lien qui y installe la clé en un toucher (WhatsApp, SMS…)
        async shareTokenLink() {
            const token = getGithubToken();
            const lang = getLang();
            if (!token) return;
            const link = `${window.location.origin}${window.location.pathname}#gh=${token}`;
            const text = lang === 'fr'
                ? "Touche ce lien pour activer le bouton Actualiser de Fransaİş sur ton téléphone :"
                : "Fransaİş'te Yenile butonunu telefonunda etkinleştirmek için bu bağlantıya dokun:";
            try {
                if (navigator.share) {
                    await navigator.share({ title: 'Fransaİş', text, url: link });
                    return;
                }
            } catch (e) {
                if (e && e.name === 'AbortError') return;
            }
            try {
                await navigator.clipboard.writeText(`${text} ${link}`);
                this.toast(lang === 'fr' ? "📋 Lien copié : colle-le dans WhatsApp." : "📋 Bağlantı kopyalandı: WhatsApp'a yapıştır.", 'success', 4000);
            } catch (e) {
                window.prompt(lang === 'fr' ? "Copie ce lien :" : "Bu bağlantıyı kopyala:", link);
            }
        },

        clearGithubToken() {
            setGithubToken('');
            this.renderCloudTokenState();
        },

        renderCloudTokenState() {
            const has = !!getGithubToken();
            const saved = document.getElementById('ghTokenSaved');
            const form = document.getElementById('ghTokenForm');
            if (saved) saved.hidden = !has;
            if (form) form.hidden = has;
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
            this.renderCloudTokenState();
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
            if (!isLocalHost()) return; // /api/status n'existe qu'avec app_server.py (évite un 404 en ligne)
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
