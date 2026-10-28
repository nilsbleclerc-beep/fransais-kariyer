# 🇹🇷 Turk-France Job Hunter Agent 🇫🇷

Agent autonome en Python pour scanner le web turc et détecter les **entreprises turques qui recrutent pour la France** (postes basés en France, filiales françaises, offres avec relocalisation / visa, et liaisons bilatérales).

---

## 🚀 Fonctionnalités Clés

1. **Cartographie des Multinationales Turques en France** :
   * Contient la base de données qualifiée des grands groupes turcs implantés en France (*Beko France, Turkish Airlines, Şişecam, Ekol Lojistik, Barsan Global, Çimsa, Kordsa, VitrA, Horoz Lojistik, Trendyol Europe, etc.*).
   * Liens directs vers leurs portails carrières et pages LinkedIn Recrutement.

2. **Offres réelles et datées (`sources/*`)** :
   * France Travail, EURES, Adzuna, Jooble (API), Gurbetİlan, Kariyer.net, ATS d'entreprises.
   * Clés API lues dans l'environnement (`FT_CLIENT_ID`, `FT_CLIENT_SECRET`, `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`, `JOOBLE_KEY`) ; sans clé, la source est simplement ignorée.
   * La recherche DuckDuckGo (« dorks ») a été supprimée : résultats périmés et pages de liste présentés comme des offres.

3. **Filtre qualité « pas de fausses joies » (`quality.py`)** — profil dans `profile.json` (turc natif, anglais A2-B1, français A1) :
   * poste **en France** (rejet si le texte le place à İstanbul, Ankara…) ;
   * annonce **récente** (≤ `max_age_days`), URL **vivante et individuelle** (pas 404, pas de redirection vers une liste, pas de « offre expirée ») ;
   * **langue compatible** : rejet si français courant/B1+ ou anglais courant/B2+ exigé ; gardée si le turc est demandé, si l'annonce dit « français non requis », si elle vient de la communauté turque ou si c'est un métier de terrain ;
   * doublons retirés ; raisons concrètes citant l'annonce (`match_reasons_tr/fr`) ; visa affiché **seulement** si l'annonce en parle (`visa_evidence`).
   * Les rejets sont écrits dans `rejected_offers.json` (audit, non affiché).

4. **Fiches entreprises (`kind="lead"`)** : grands groupes turcs, institutions internationales, scale-ups tech. Ce ne sont pas des offres : pas de score, et mention honnête « anglais/français avancé requis » pour les institutions et la tech.

5. **Exports Multi-Formats & Dashboard Interactif** :
   * **`dashboard.html`** : Un tableau de bord web interactif moderne avec recherche en temps réel et filtres par catégorie.
   * **`offres_france_turquie.csv`** : Fichier prêt pour Microsoft Excel.
   * **`offres_france_turquie.json`** : Données brutes pour intégration ou archivage.

---

## 🛠️ Installation & Démarrage Rapide

### 1. Prérequis
Python 3.10 ou supérieur installé.

### 2. Dépendances requises
```bash
pip install -r requirements.txt
```

### 3. Lancer le scanner
```bash
python main.py
```

Vous pouvez aussi ajuster les paramètres de profondeur :
```bash
# 5 pages max. par collecteur paginé, sans régénérer le HTML
python main.py --pages 5 --no-html
# Tests du filtre qualité
python tests/test_quality.py   # ou : pytest tests/
```

---

## 📁 Structure du Projet

```text
├── main.py              # Point d'entrée de l'agent CLI
├── sources/             # Collecteurs d'offres réelles (un module = une source, fetch(profile))
├── quality.py           # Filtre qualité : France, fraîcheur, URL vivante, langue, doublons, raisons
├── profile.json         # Profil de la candidate (langues, ancienneté max)
├── scrapers.py          # Fiches statiques (leads) : groupes, institutions, scale-ups
├── scorer.py            # Analyse légère d'un texte (mots entiers, visa explicite seulement)
├── config.py            # Mots-clés
├── rejected_offers.json # Audit des offres écartées et de leur raison
├── companies_data.py    # Annuaire des filiales turques & infos DEİK / CCIFT
├── exporter.py          # Génération du Dashboard HTML, CSV et JSON
├── dashboard.html       # Tableau de bord interactif généré
└── README.md            # Documentation
```

---

## 💡 Conseils Spécifiques pour Décrocher un Poste en France depuis la Turquie

1. **Visas & Sponsor** :
   * Les grandes entreprises (comme Arçelik/Beko ou THY) utilisent fréquemment la procédure de **salarié détaché ICT (Intra-Company Transfer)** ou le **Passeport Talent**. C'est le moyen le plus simple et rapide pour faire venir un employé de Turquie en France.
2. **Le Réseau CCIFT & DEİK** :
   * Ne vous limitez pas aux annonces passives. Utilisez les coordonnées des membres de la **Chambre de Commerce Franco-Turque (CCIFT)** et du **DEİK** pour envoyer des candidatures spontanées directement aux Country Managers ou DRH des filiales françaises.
3. **Format du CV** :
   * Adaptez votre CV turc aux standards français : 1 à 2 pages maximum, pas de mention d'état civil inutile (religion, service militaire, statut marital), mettez en avant votre bilinguisme turc/français/anglais et votre compréhension des deux marchés.
