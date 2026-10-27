# Module Bilatéral France-Turquie : Drawer d'Opportunité, Générateur de Lettre (TR ➔ FR) & Guide Mobilité

Ce module fournit l'assistance complète à la candidature et la sécurisation juridique pour les candidats résidant en Turquie postulant en France.

---

## 📁 Fichiers Livrés Prêts à la Fusion

1. **`drawer_cover_letter_module.js`** : Moteur JavaScript complet (IIFE autonome exposant `window.BilateralDrawer`, `window.CoverLetterGenerator`, `window.MobilityGuide`, `window.BilateralToast`).
2. **`drawer_cover_letter_styles.css`** : Styles CSS complets (Écussons des 3 Voies, Drawer coulissant, Modal de génération, Timeline visa 4 étapes, Toast).
3. **`drawer_cover_letter_markup.html`** : Balisage HTML prêt à être inséré juste avant la fermeture `</body>` dans `dashboard.html`.

---

## 🏛️ Les 3 Voies Prioritaires & Écussons Officiels

Conformément aux instructions client, chaque opportunité affiche en haut de sa fiche l'Écusson officiel de sa voie :

| Voie | Nom Officiel de la Voie | Écusson & Badge | Régime Juridique & Dispense |
| :--- | :--- | :--- | :--- |
| **Voie 1** | **Statut International MAE** | `🏛️ VOIE 1 PRIORITAIRE : STATUT INTERNATIONAL MAE` | Dispense totale d'autorisation de travail classique. Titre de séjour spécial délivré par le protocole du Ministère de l'Europe et des Affaires Étrangères (MEAE). |
| **Voie 2** | **Salarié Détaché ICT (CCIFT & DEİK)** | `🤝 VOIE 2 PRIORITAIRE : SALARIÉ DÉTACHÉ ICT (CCIFT & DEİK)` | Mobilité intra-groupe (CESEDA L. 421-26). Accord bilatéral de sécurité sociale franco-turc de 1972. Exonération de l'opposabilité de l'emploi local. |
| **Voie 3** | **Passeport Talent French Tech** | `⚡ VOIE 3 PRIORITAIRE : PASSEPORT TALENT (FRENCH TECH)` | Statut Jeune Entreprise Innovante (CESEDA L. 421-9). Titre pluriannuel direct de 4 ans. 100% en anglais. Droit de travail immédiat pour le conjoint. |
| **Voie 4** | **Procédure Standard Salarié** | `🏢 VOIE 4 : VISA DE TRAVAIL SALARIÉ (VLS-TS)` | Droit commun. Procédure dématérialisée ANEF et VLS-TS via VFS Global en Turquie. |

---

## ✍️ Générateur Intelligent de Pitch & Lettre de Motivation

Le générateur produit deux types de documents modifiables en temps réel :

### 1. Email Court de Premier Contact (Recruteur / DRH / LinkedIn InMail)
Rédigé en français soutenu et percutant, avec rappel de la Voie en objet et paragraphe d'accroche opérationnel.

### 2. Lettre de Motivation Formelle & Argumentée
**Le premier paragraphe d'introduction rappelle expressément la voie juridique au recruteur français :**
- **Voie 1 :** *"C'est dans le cadre de la Voie d'accès statutaire dérogatoire des institutions internationales (accord de siège et titre spécial du Ministère de l'Europe et des Affaires Étrangères - MEAE, sans autorisation de travail classique requise) que je vous soumets ma candidature..."*
- **Voie 2 :** *"C'est sous le régime privilégié de la Voie de mobilité bilatérale intra-groupe (Salarié détaché ICT - articles L. 421-26 et suivants du CESEDA et accord franco-turc de sécurité sociale du 20 janvier 1972) que je vous adresse ma candidature..."*
- **Voie 3 :** *"C'est au titre du dispositif d'attractivité de la Voie Passeport Talent – Entreprise Innovante (Article L. 421-9 du CESEDA) que je vous soumets ma candidature..."*
- **Voie 4 :** *"C'est avec un enthousiasme soutenu que je vous soumets ma candidature... prêt(e) à engager sans délai la procédure d'autorisation de travail et de visa long séjour salarié (VLS-TS) via l'ANEF..."*

### Fonctionnalités Clés :
- **Champs Personnalisables en Direct :** Nom, Titre professionnel, Années d'expérience, Compétences clés.
- **Bouton de Copie 1-Clic :** `navigator.clipboard.writeText` avec fallback et Toast animé.
- **Téléchargement .txt :** Génère un fichier texte prêt à l'emploi.

---

## 🚪 Panneau Latéral Coulissant (Drawer)
- Slide-in depuis la droite avec courbe d'animation fluide `cubic-bezier(0.16, 1, 0.3, 1)`.
- Écusson officiel de la Voie en en-tête.
- Annuaire RH bilatéral intégré : email direct des DRH (Beko France, THY, Ekol, Barsan, Şişecam, Vestel, Eczacıbaşı, Çimsa, OECD, UNESCO, Conseil de l'Europe, Mistral AI, Qonto, Datadog...) avec bouton de copie d'email en 1-clic.
- Fiche visa étape par étape personnalisée (4 étapes adaptées à la Voie).
- Bouton direct pour ouvrir le générateur de lettre pré-rempli.

---

## 📘 Guide Bilingue Pratique de l'Expatriation & CV
- **Fiche synthétique des 3 visas :** Tableau comparatif (critères, délais VFS, famille, base légale) et adresses des centres VFS Global en Turquie (Istanbul Harbiye/Altunizade, Ankara, Izmir).
- **Guide de conversion du CV turc vers les standards français :**
  - Ce qu'il faut supprimer : âge/date de naissance, statut matrimonial, service militaire, adresse complète, numéros personnels de tiers.
  - Ce qu'il faut adapter : règle de la page unique (< 10 ans), équivalences académiques (Lisans ➔ Bac+3/4, YL ➔ Master 2 Bac+5, Doktora ➔ PhD Bac+8), échelle européenne CECRL des langues (A1-C2), formule impact chiffré (Action + Contexte + Résultat KPI).

---

## ⚡ Guide d'Intégration en 3 Étapes dans `dashboard.html`

1. **Dans `<head>` :**
   ```html
   <link rel="stylesheet" href="drawer_cover_letter_styles.css">
   ```
2. **Sur les cartes d'offres :**
   ```html
   <button type="button" class="action-btn btn-details" onclick="window.BilateralDrawer.openFromCard(this.closest('.job-card'))">👁️ Detaylar</button>
   <button type="button" class="action-btn btn-pitch" onclick="window.CoverLetterGenerator.open(this.closest('.job-card'))">✍️ Ön Yazı & Pitch</button>
   ```
3. **Avant la fermeture `</body>` :**
   Insérer le contenu de `drawer_cover_letter_markup.html` puis :
   ```html
   <script src="drawer_cover_letter_module.js"></script>
   ```
