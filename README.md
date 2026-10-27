# 🇹🇷 Turk-France Job Hunter Agent 🇫🇷

Agent autonome en Python pour scanner le web turc et détecter les **entreprises turques qui recrutent pour la France** (postes basés en France, filiales françaises, offres avec relocalisation / visa, et liaisons bilatérales).

---

## 🚀 Fonctionnalités Clés

1. **Cartographie des Multinationales Turques en France** :
   * Contient la base de données qualifiée des grands groupes turcs implantés en France (*Beko France, Turkish Airlines, Şişecam, Ekol Lojistik, Barsan Global, Çimsa, Kordsa, VitrA, Horoz Lojistik, Trendyol Europe, etc.*).
   * Liens directs vers leurs portails carrières et pages LinkedIn Recrutement.

2. **Scanner d'Annonces en Temps Réel** :
   * Interroge les annonces récentes publiées par les employeurs turcs pour des postes en France (Paris, Lyon, Marseille, etc.).
   * Scrape les plateformes spécialisées bilatérales.

3. **Recherche Ciblée (Google / Job Boards Dorks)** :
   * Exécute des requêtes optimisées sur **Kariyer.net**, **LinkedIn**, **SecretCV**, etc., avec les mots-clés spécifiques des recruteurs turcs (*« Fransa ofisimizde »*, *« relokasyon »*, *« vize desteği »*, *« Fransızca bilen »*).

4. **Scoring & Détection Intelligente** :
   * Évalue la pertinence de chaque offre de 0 à 100%.
   * Attribue des badges clairs : `✈️ Relocalisation / Visa`, `🏢 Groupe Turc Majeur`, `🗣️ Bilingue`, `📍 Ville`.

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
# Scanner 5 pages d'annonces et 8 requêtes ciblées
python main.py --pages 5 --dorks 8
```

---

## 📁 Structure du Projet

```text
├── main.py              # Point d'entrée de l'agent CLI
├── scrapers.py          # Moteurs de scan (PME, Multinationales, Web Dorks)
├── scorer.py            # Moteur d'analyse sémantique et de scoring
├── config.py            # Mots-clés, filtres et requêtes dorks
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
