# Suivi : refonte mobile Fransaİş (Android / HONOR Magic7 Lite)

*Dernière mise à jour : 28/10/2026. Travail en pause.*

## Appareil cible

Toute la refonte vise **un seul appareil** : le **HONOR Magic7 Lite**.

| Caractéristique | Valeur |
| --- | --- |
| Système et navigateur | Android / MagicOS, Chrome |
| Mode d'utilisation | PWA installée (standalone) |
| Écran | AMOLED 6,78" aux **bords incurvés**, poinçon centré |
| Navigation système | Par gestes |
| Viewport CSS | ≈ **408×900** (de 384 à 412 selon la taille d'affichage) |

On suit les conventions **Material 3** :

- cibles tactiles d'au moins 48 dp ;
- barre de navigation en bas ;
- feuilles qui montent du bas (bottom sheets) ;
- marges latérales d'au moins 16 px, pour les bords incurvés.

Le desktop doit rester utilisable, sans être optimisé.

---

## ✅ Fait

| Commit | Contenu |
| --- | --- |
| `9eb2a17` | CI : suppression des étapes « deploy-pages » qui échouaient. Pages se déploie depuis la branche `master`. |
| `783b83b` | Correctifs mobiles : plus de débordement horizontal, barre de navigation en bas, retour Android via l'historique, zones sûres, cibles de 48 dp, zoom réactivé, drawer lisible en mode sombre, partage natif (`navigator.share`), Kanban utilisable au doigt, cohérence TR/FR, 🇬🇧 réservé à « anglais suffisant ». |
| `a3a5360` | **Fondations, Keşfet et Détail** : offres en JSON inline (`window.FransaData`) rendues en JS par lots de 20 (page passée de 1,42 Mo à 595 Ko). Police système, sprite d'icônes SVG, nouvel écran Keşfet (pastilles, feuille Filtres, cartes de 160 px, « yeni ilan »). Détail en plein écran (« Bu ilan bana uygun mu? », frise visa, barre ⭐ + « Ön yazı hazırla »). Correction du domaine IT et des préfixes de titres FR. |

| *(28/10)* | **Recherche d'offres réelles, zéro faux positif** : voir la section ci-dessous. |

---

## Recherche d'offres réelles (28/10/2026)

**Profil de la candidate** (`profile.json`) : turc natif, anglais A2/B1, français A1, tous domaines, offres de 45 jours au plus.

**Sources** (`sources/*.py`, contrat `fetch(profile) -> List[JobOpportunity]`) :

| Source | Type | État | Clé requise |
| --- | --- | --- | --- |
| GurbetIlan | communauté turque | ✅ en ligne : date, ville et texte complet | non |
| Kariyer.net (rubrique « yurtdışı → Fransa » uniquement) | job board turc | ✅ en ligne (0 offre en France le 28/10) | non |
| ATS groupes turcs : Trendyol (Lever), DFDS ex-Ekol (Teamtailor), Pladis/Godiva (Workday) | ATS | ✅ en ligne | non |
| France Travail – API Offres v2 (« turc », « turcophone »…) | officielle | ❌ **indisponible** : vérifié le 29/10/2026 dans le catalogue francetravail.io (46 API, compte connecté), l'API « Offres d'emploi » n'y figure plus (seule reste la version alternance). Les clés créées n'ont aucune API autorisée (`invalid_client`). Le code reste en place au cas où elle reviendrait. Une partie des offres France Travail arrive déjà via Adzuna. | `FT_CLIENT_ID` / `FT_CLIENT_SECRET` |
| Adzuna | agrégateur | ✅ actif **jusqu'à épuisement du quota gratuit** : pas d'abonnement (décision du 29/10, 8 £/mois). 25 appels de test au total, ramenés à 1 appel par scan (50 offres les plus récentes) ; ensuite la source renverra [] d'elle-même. Meilleure source jusqu'ici (16 offres sur 26, dont des offres France Travail reprises). | `ADZUNA_APP_ID` / `ADZUNA_APP_KEY` |
| Jooble | agrégateur | ⏸ **désactivé** (29/10) : la clé française fonctionne, mais la recherche ignore les mots-clés (12 247 résultats pour « turc », « bilingue turc » ou « turkish speaking ») et 0 offre liée au turc sur 345 testées. Le code est conservé (`sources/jooble.py`) : décommenter dans `sources/__init__.py` pour le réactiver. | `JOOBLE_KEY` |
| **EURES** (offres France Travail **exigeant le turc**) | portail européen | ✅ **meilleure source** (29/10) : moteur de recherche public du portail, filtre « langue requise : turc » + pays France, puis fiche détaillée pour les langues exigées ou souhaitées et la ville. 47 offres, **36 gardées** (dont une dizaine en IDF), 6 rejetées car le français y est exigé. Dédoublonnage avec Adzuna (offres « France Travail » de même titre). | non |

Web turc testé le 29/10 (İŞKUR, Yenibiriş, isbul, SecretCV, eleman.net, sahibinden, Hodrimeydan, médias de la diaspora, agences de placement, consulats turcs) : **aucune offre réellement située en France** ; Yenibiriş (`/is-ilanlari/fransa`) et les annonces des consulats turcs sont à surveiller.

Supprimés : les recherches DuckDuckGo (résultats périmés, postes « Fransızca bilen » situés à Istanbul).

**Filtre anti-faux-positifs** (`quality.py`). Une offre est rejetée si :

- elle n'est pas en France ;
- elle date de plus de 45 jours ;
- son lien est mort, redirigé ou mène à une annonce expirée ;
- elle exige un français B1+ ou un anglais B2+ ;
- elle n'a aucun lien avec la langue turque, alors que le français y est implicite ;
- il s'agit d'une mission liée à un **événement déjà terminé** (salon, « fuar »…) ;
- c'est un doublon.

Toutes les offres rejetées sont listées dans `rejected_offers.json`, avec leur motif. Le visa n'est affiché que s'il est cité dans l'annonce.

**Assouplissement du 28/10** : elle **s'installe en Île-de-France chez son conjoint** (logement assuré, `home_region: IDF` dans `profile.json`).

- Les offres en IDF sont mises en avant (+15 au score, raison « Île-de-France »).
- Une **résidence demandée à Paris** n'est plus bloquante : simple info.
- Un **permis de travail déjà exigé** n'est plus un rejet mais un **avertissement orange** (« demander à l'employeur s'il peut parrainer le visa »).
- Les postes listés par un **ATS** ne sont plus jugés trop anciens, puisqu'un ATS ne liste que des postes ouverts.

**Premier scan réel (28/10)** : 25 offres collectées, **8 gardées** (GurbetIlan : BTP, restauration, textile, à Paris, Torcy, Nevers, Le Havre et Lyon), 17 rejetées : 7 trop anciennes, 4 réservées aux résidents, 3 avec français exigé, 2 sans langue compatible, 1 avec anglais avancé exigé.

Les fiches entreprises et institutions (33) sont désormais des « pistes » (`kind="lead"`) affichées dans Rehber, avec la mention « Bu bir ilan değil ». Elles ne sont plus présentées comme des offres.

### 🔑 Action requise : clés API (gratuites)

Une fois inscrit sur chaque service, ajouter les clés dans GitHub : *Settings → Secrets and variables → Actions → New repository secret*.

1. **France Travail** (la source la plus utile : offres officielles avec l'exigence de langue « Turc ») : créer une application sur https://francetravail.io, souscrire à l'API **Offres d'emploi v2**, puis ajouter `FT_CLIENT_ID` et `FT_CLIENT_SECRET`.
2. **Adzuna** : s'inscrire sur https://developer.adzuna.com/signup, puis ajouter `ADZUNA_APP_ID` et `ADZUNA_APP_KEY`.
3. **Jooble** : remplir le formulaire sur https://jooble.org/api/about, puis ajouter `JOOBLE_KEY`.

*29/10 : les 5 secrets sont enregistrés. Pour Adzuna, ne pas ajouter de carte : France Travail couvre l'essentiel.*

Au premier scan avec clés, relire `rejected_offers.json`. Points à vérifier :

- les paramètres France Travail et Jooble ont été codés en partie de mémoire ;
- les marqueurs d'annonce expirée peuvent se déclencher à tort sur certains sites.

### Pistes d'amélioration de la recherche

- [ ] Quand les clés seront là, ajuster les mots-clés France Travail (ex. « turc » + codes ROME des métiers en tension) et vérifier le volume.
- [ ] Rejeter aussi les offres d'événements déjà passés (ex. un salon dont les dates sont échues).
- [ ] Pour DFDS, la date d'une annonce permanente est celle de sa première publication : ces annonces sont donc rejetées comme trop anciennes alors qu'elles sont peut-être encore ouvertes.
- [ ] Ajouter des ATS si de nouveaux groupes turcs ouvrent un listing public (Beko recrute via France Travail et Wizbii ; Şişecam et Ekol bloquent les robots).

---

## Contrats techniques à respecter

### 1. Données : `window.FransaData`

Ce bootstrap est injecté par `exporter.py` **avant** tous les autres scripts.

```js
FransaData.jobs   // tableau d'offres
FransaData.get(id)
```

Champs de chaque offre (`job`) :

| Champ | Contenu |
| --- | --- |
| `id` | identifiant numérique |
| `title_tr`, `title_fr` | titre dans chaque langue |
| `company`, `location`, `url`, `source` | infos de base |
| `score` | pertinence (0 à 100) |
| `snippet_tr`, `snippet_fr` | extrait de l'annonce |
| `tags_tr[]`, `tags_fr[]` | étiquettes |
| `category_tr`, `category_fr` | catégorie |
| `ccift`, `no_french` | booléens |
| `working_lang` | langue de travail |
| `visa_tr`, `visa_fr` | voie visa |
| `track` | `voie_1`, `voie_2`, `voie_3` ou `autre` |
| `domain` | domaine d'activité |
| `discovered_at` | date de détection |
| `contact_info` | contact RH |

### 2. Historique : bouton retour Android

Chaque overlay a un identifiant (`<id>`). Le cycle de vie est le suivant :

1. **Ouverture** : `history.pushState({ fransaOverlay: '<id>' }, '')`.
2. **Fermeture depuis l'interface** :
   - si `history.state?.fransaOverlay === '<id>'`, appeler `history.back()` ;
   - sinon, fermer directement.
3. **Sur `popstate`** : si l'overlay est ouvert et que l'état courant n'est plus le sien, le fermer sans toucher à l'historique.

Identifiants déjà utilisés : `drawer`, `letter`, `guide`, `filters`, `pwa-install`, `pwa-cloud`, `tracker-modal`.

Les onglets suivent une autre règle :

- quitter Keşfet pour un autre onglet fait un `pushState` (`#tracker`, `#guide`) ;
- passer d'un onglet à un autre (hors Keşfet) fait un `replaceState` ;
- le `HistoryRouter` (`tracker_engine.js`) ignore les états `fransaOverlay`.

### 3. API JS publiques

**`window.TrackerEngine`** :

- `toggleBookmark(id)`
- `isFavorite(id)`
- `addToTracker(id, status)` (sans toast)
- `openTrackerModal(id)`
- `advanceKanban(id, dir)`
- `switchTab(tab)`
- les services `Storage`, `Filter`, `Kanban`, `UI` et `Toast`

**Autres modules** :

- `BilateralDrawer.open(id)`
- `CoverLetterGenerator.open(id)`
- `MobilityGuide.open()`
- `BilateralToast`

**Événements `window`** :

- `languageChanged` (`detail.lang`)
- `fransa:favorite`
- `fransa:tracker`

**Langue** : stockée en `localStorage` sous la clé `bilateral_lang`.

### 4. Génération et déploiement

- **Ne jamais éditer `index.html` / `dashboard.html` à la main.** Ils sont générés.
- Pour régénérer :

  ```bash
  python -c "import exporter, json; from models import JobOpportunity; jobs=[JobOpportunity(**d) for d in json.load(open('offres_france_turquie.json',encoding='utf-8'))]; exporter.export_to_html_dashboard(jobs,'dashboard.html')"
  ```

- **Incrémenter `CACHE_NAME` dans `sw.js` (actuellement `v6`)** à chaque changement visible, sinon l'app installée ne se met pas à jour.
- Un push qui touche `exporter.py`, `scrapers.py`, `companies_data.py` ou `pwa_*` relance le workflow. Le robot commite alors de nouvelles offres : faire `git pull` avant de reprendre.

---

## 🔜 Prochaines étapes (dans l'ordre)

### Étape 0 : test réel sur le HONOR, à faire en premier

- [ ] Désinstaller puis réinstaller la PWA, ou la fermer et la rouvrir, pour charger le cache `v4`.
- [ ] **Bords incurvés** : aucun texte ni bouton coupé sur les côtés.
- [ ] **Poinçon** : la barre du haut ne passe pas dessous.
- [ ] **Navigation par gestes** : la barre du bas ne gêne pas.
- [ ] **Geste retour**, dans cet ordre :
  1. il ferme la lettre ;
  2. puis le détail ;
  3. puis les filtres ;
  4. puis revient de Başvurularım ou Rehber vers Keşfet ;
  5. enfin, il quitte l'app.
- [ ] **Partage natif** : depuis le menu ⋮ du détail et depuis la lettre (WhatsApp, Gmail).
- [ ] **Installation** : invite `beforeinstallprompt` et bannière d'installation.
- [ ] **Mode sombre système** et **taille de police système agrandie**.
- [ ] Noter chaque problème ici, avec une capture d'écran.

### Étape 1 : Lettre de motivation en 3 étapes (`drawer_cover_letter_*`)

- [ ] **Profil** (nom, métier, années d'expérience, compétences, langues) :
  - saisi une seule fois, stocké en `localStorage` (`fransa_profile`) ;
  - pré-rempli à chaque lettre et modifiable depuis Rehber ou les réglages.
- [ ] **Feuille plein écran en 3 étapes**, avec un indicateur de progression :
  1. type : email court au recruteur ou lettre formelle ;
  2. vérification des informations pré-remplies ;
  3. aperçu, puis [Kopyala] [Paylaş] [E-posta ile gönder] (`mailto:` avec `contact_info` si c'est un email).
- [ ] La lettre reste **en français**. L'interface suit la langue choisie.
- [ ] Après un envoi : snackbar « Başvurdum olarak işaretle? ». **Déjà fait**, à garder.
- [ ] Retour Android : l'étape 3 revient à l'étape 2, et ainsi de suite, puis la feuille se ferme. Utiliser un état `letter` avec un champ `step`, ou un `replaceState`.

### Étape 2 : Başvurularım, à la place du Kanban (`tracker_engine.js` + `exporter.py`)

- [ ] **Contrôle segmenté** en haut : Kaydedilenler · Başvurulanlar · Mülakat · Sonuç, chacun avec son compteur.
- [ ] **Liste simple**, une ligne par candidature : titre, entreprise, statut, date.
- [ ] **Toucher une ligne** ouvre une feuille avec :
  - le changement de statut ;
  - une note ;
  - une date d'entretien ;
  - un lien vers le détail.
- [ ] **Relance** : badge « 10 gündür yanıt yok » quand une candidature est « applied » depuis plus de 10 jours, avec un modèle de mail de relance en français (copier ou partager).
- [ ] **Favoris** fusionnés dans « Kaydedilenler » : un seul endroit pour les offres sauvegardées.
- [ ] Le glisser-déposer reste disponible sur desktop uniquement. Sur mobile, la liste remplace les colonnes.
- [ ] **Exports CSV/JSON** déplacés dans un menu ⋮ : ce n'est pas une action du quotidien.
- [ ] **État vide** engageant, avec un bouton « İlanları keşfet ».

### Étape 3 : Rehber (`exporter.py` + `drawer_cover_letter_*` pour le guide)

- [ ] **3 cartes Kapı** (plus la voie standard), chacune ouvrant un article court en plein écran : à qui elle s'adresse, délais, documents, base légale.
- [ ] **Checklist du dossier visa** avec barre de progression (déjà en `localStorage`, à reprendre visuellement).
- [ ] **Guide CV turc → format français** et **centres VFS** (Istanbul, Ankara, Izmir).
- [ ] Réorganiser les blocs déplacés depuis Keşfet (stats, CCIFT, bilatéral, 3 étapes) en sections repliables, en bas de l'écran.
- [ ] Accès au profil et aux réglages : langue, thème, installation, actualisation.

### Étape 4 : Onboarding au premier lancement

Il se fait en dernier, parce qu'il dépend du profil (étape 1).

- [ ] **3 écrans** qu'on peut passer :
  1. langue ;
  2. profil rapide : langues parlées, niveau de français (A1 à C2), domaine ;
  3. les 3 Kapı, une carte chacune.
- [ ] **Le profil personnalise Keşfet** :
  - tri « Önerilen » pondéré par le domaine ;
  - filtre « Fransızca gerekmez » activé par défaut si le niveau est inférieur à B1.
- [ ] Indicateur `fransa_onboarded` en `localStorage`, et lien « Revoir l'introduction » dans Rehber.

### Étape 5 : Finitions et qualité

- [ ] **Design system** : ajouter une section « Mobile Android » à `DESIGN_SYSTEM_SPEC.md` (tokens, composants, contrats), puis la figer dans un skill projet avec `skill-creator`.
- [ ] **Emoji restants** dans les tags de données (`companies_data.py`, `scorer.py`) : les remplacer par des icônes ou des codes neutres.
- [ ] **Accessibilité** : audit WCAG AA (`design:accessibility-review`), et vérification de `prefers-reduced-motion` sur les animations.
- [ ] **Performance** :
  - mesurer LCP et INP sur l'appareil ;
  - envisager de charger `offres_france_turquie.json` à part si le JSON inline grossit ;
  - `sw.js` met en cache `index.html` **et** `dashboard.html`, qui sont identiques : n'en garder qu'un.
- [ ] **Captures de non-régression** en 408×900 (clair/sombre × TR/FR) pour chaque écran.

---

## 🐞 Dette technique repérée (hors refonte)

- [ ] **`pwa_module.js:379` et `:479`** appellent `/api/status`, qui renvoie 404 sur GitHub Pages et sur un simple serveur statique. N'appeler cette route que si l'app tourne via `app_server.py` (localhost).
- [ ] **`scorer.py`** : des marqueurs très courts (`"a1"`, `"a2"`, `"c1"`, `"c2"`, `"coe"`, `"amo"`, `"tech"`) sont cherchés comme simples sous-chaînes dans le titre, l'extrait et l'URL. Ils peuvent fausser le niveau de français et le score : passer en mots entiers (`\b…\b`).
- [ ] **`exporter.determine_job_track`** : même problème avec `"mae"`, `"coe"`, `"ict"`, `"thy"`, `"tech"`.
- [ ] **`app_server.py`** initialise `last_refresh` à l'heure de démarrage du serveur, même sans scan.
- [ ] **Base `TURKISH_COMPANIES_IN_FRANCE`** : vérifier que les emails RH et les URL ATS sont toujours valides.
- [ ] **Aucun test automatisé.** Ajouter au minimum un test du scorer et de l'export (`pytest`).

---

## Outils et plugins utiles (pour reprendre)

- **Déjà disponibles** :
  - `design:design-critique`
  - `design:accessibility-review`
  - `design:ux-copy` (microcopie TR/FR)
  - `design:design-system`
- **À installer depuis le catalogue** (proposés le 27/10) : `frontend-design`, `ux-ui-audit` (vérifie aussi la cohérence TR/FR), `Responsive Check`, `playwright`, `audit-suite`.
- **Moins pertinent ici** : « Mobile App Design (iOS) », centré sur l'iPhone.
- **Méthode par écran** :
  1. étudier les références (LinkedIn Jobs, Welcome to the Jungle, Indeed Android, Wise pour les frises) ;
  2. faire une maquette à la taille du HONOR ;
  3. implémenter ;
  4. prendre des captures en 408×900 ;
  5. passer la critique design et l'audit d'accessibilité ;
  6. pousser ;
  7. tester sur le HONOR.
