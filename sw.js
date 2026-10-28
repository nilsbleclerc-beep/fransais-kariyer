/**
 * Service Worker : Fransa Kariyer & Vize Rehberi (Fransaİş PWA)
 * - Cache-first pour les assets statiques
 * - Stale-while-revalidate pour le HTML et les données d'offres JSON
 * - Réponse instantanée (<100ms) et support 100% hors-ligne
 * - Bypass automatique pour les routes dynamiques /api/*
 */

const CACHE_NAME = 'fransais-pwa-v5';

const STATIC_ASSETS = [
    './',
    './index.html',
    './dashboard.html',
    './manifest.json',
    './offres_france_turquie.json',
    './icon.svg',
    './favicon.svg',
    './icon-192.png',
    './icon-512.png',
    './apple-touch-icon.png'
];

// Installation : Mise en cache du Shell applicatif
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            // Mise en cache tolérante aux fichiers optionnels
            return Promise.allSettled(
                STATIC_ASSETS.map((url) =>
                    cache.add(url).catch((err) => {
                        console.warn(`[SW] Impossible de pré-cacher : ${url}`, err);
                    })
                )
            );
        }).then(() => self.skipWaiting())
    );
});

// Activation : Nettoyage des anciens caches et prise de contrôle immédiate
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter((key) => key !== CACHE_NAME).map((key) => {
                    console.log(`[SW] Suppression de l'ancien cache : ${key}`);
                    return caches.delete(key);
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Interception des requêtes réseau
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // 1. BYPASS COMPLET POUR L'API LOCALE (/api/refresh, /api/status, etc.)
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(fetch(event.request));
        return;
    }

    // 2. STRATÉGIE STALE-WHILE-REVALIDATE POUR LES PAGES ET LES DONNÉES JSON
    // Permet un affichage instantané tout en actualisant silencieusement en tâche de fond
    if (
        event.request.mode === 'navigate' ||
        url.pathname.endsWith('.html') ||
        url.pathname.endsWith('/') ||
        url.pathname.endsWith('.json')
    ) {
        event.respondWith(
            caches.open(CACHE_NAME).then(async (cache) => {
                const cachedResponse = await cache.match(event.request);

                // Lancement de la mise à jour réseau en tâche de fond
                const fetchPromise = fetch(event.request)
                    .then((networkResponse) => {
                        if (networkResponse && networkResponse.status === 200) {
                            cache.put(event.request, networkResponse.clone());
                        }
                        return networkResponse;
                    })
                    .catch(() => {
                        // Réseau indisponible (mode hors-ligne)
                        return cachedResponse;
                    });

                // Si on a du cache, on le retourne immédiatement, sinon on attend le réseau
                return cachedResponse || fetchPromise;
            })
        );
        return;
    }

    // 3. STRATÉGIE CACHE-FIRST POUR LES ASSETS STATIQUES (Images, Fonts, Icônes)
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse;
            }
            return fetch(event.request).then((networkResponse) => {
                if (networkResponse && networkResponse.status === 200 && event.request.method === 'GET') {
                    const responseToCache = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseToCache);
                    });
                }
                return networkResponse;
            }).catch(() => {
                // Si l'image n'est pas dans le cache et pas de réseau, fallback vers icône de base si dispo
                if (event.request.destination === 'image') {
                    return caches.match('./icon-192.png');
                }
            });
        })
    );
});

// Écoute des messages du client (ex: force update)
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});
