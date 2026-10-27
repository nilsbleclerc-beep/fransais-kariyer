# DESIGN SYSTEM SPECIFICATION : HAUTE COUTURE DIGITALE
**Framework Visuel & Architectural pour l'Application Bilatérale France-Turquie**  
*Inspiré des canons esthétiques de Linear, Stripe et Apple Human Interface Guidelines (HIG)*

---

## 1. Philosophie & Principes Directeurs

1. **Haute Précision & Élégance Discrète** : Éradication totale des émoticônes natives disparates au profit d'une bibliothèque vectorielle SVG unifiée à 24px/16px avec traits fins (stroke-width 2px), courbures soyeuses et alignement optique strict.
2. **Éclairage & Ombres Multicouches (Stripe Style)** : Utilisation d'ombres douces composées à 3 niveaux de diffusion (`--shadow-xs` à `--shadow-xl`, `--shadow-card-hover`), combinées avec des bordures subtiles translucides (`rgba(226, 232, 240, 0.85)` en clair, `rgba(255, 255, 255, 0.08)` en sombre).
3. **Fluidité Apple HIG** : Courbe temporelle physique `cubic-bezier(0.16, 1, 0.3, 1)` créant un rebond imperceptible et une sensation de réactivité immédiate sans friction.
4. **Accréditation Prestige CCIFT & DEİK** : Mise en valeur dorée VIP avec balayage lumineux dynamique (*Gold Shimmer Sweep* animé par GPU sur pseudo-élément `::after` à 3.2s d'intervalle).
5. **Reconnaissance Visuelle des 3 Voies Prioritaires (Demande Client)** : Écussons d'en-tête distincts sur chaque carte (Indigo pour MAE, Or Prestige pour ICT, Violet/Cyan pour Passeport Talent), parfaitement corrélés avec la boîte de conseils d'astuces tripartite et les filtres.
6. **Dark Mode First-Class Citizen** : Thème sombre en obsidienne et ardoise profonde (`#090d16` et `#0f172a`), doté d'une persistance instantanée via `localStorage` et détection automatique `prefers-color-scheme`.

---

## 2. Palette Sémantique & Tokens CSS

```css
:root, [data-theme="light"] {
  /* Surfaces & Toiles */
  --surface-canvas: #f8fafc;
  --surface-card: #ffffff;
  --surface-card-hover: #ffffff;
  --surface-elevated: #ffffff;
  --surface-subtle: #f1f5f9;
  --surface-muted: #e2e8f0;
  --surface-glass: rgba(255, 255, 255, 0.85);

  /* Bordures */
  --border-subtle: rgba(226, 232, 240, 0.85);
  --border-default: #cbd5e1;
  --border-strong: #94a3b8;
  --border-focus: #2563eb;

  /* Typographie */
  --text-primary: #0f172a;
  --text-secondary: #334155;
  --text-tertiary: #64748b;
  --text-muted: #94a3b8;
  --text-inverse: #ffffff;

  /* Accents */
  --accent-primary: #2563eb;
  --accent-primary-hover: #1d4ed8;
  --accent-primary-subtle: #eff6ff;
  --accent-primary-border: #bfdbfe;

  /* Statuts */
  --status-success: #059669;
  --status-success-subtle: #ecfdf5;
  --status-success-border: #a7f3d0;
  --status-success-text: #065f46;

  --status-amber: #d97706;
  --status-amber-subtle: #fffbeb;
  --status-amber-border: #fde68a;
  --status-amber-text: #92400e;

  --status-sky: #0284c7;
  --status-sky-subtle: #f0f9ff;
  --status-sky-border: #bae6fd;
  --status-sky-text: #0369a1;

  --status-purple: #7c3aed;
  --status-purple-subtle: #f5f3ff;
  --status-purple-border: #ddd6fe;
  --status-purple-text: #5b21b6;

  /* Or VIP CCIFT & DEİK */
  --gold-primary: #d97706;
  --gold-hover: #b45309;
  --gold-bg-gradient: linear-gradient(135deg, #fffdf7 0%, #fefcf3 50%, #fef3c7 100%);
  --gold-ribbon-bg: linear-gradient(135deg, #b45309 0%, #d97706 50%, #f59e0b 100%);
  --gold-shimmer-color: rgba(255, 255, 255, 0.6);

  /* Ombres Stripe Multi-couches */
  --shadow-xs: 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03);
  --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.06), 0 2px 4px -2px rgba(15, 23, 42, 0.04);
  --shadow-lg: 0 10px 15px -3px rgba(15, 23, 42, 0.07), 0 4px 6px -4px rgba(15, 23, 42, 0.03);
  --shadow-xl: 0 20px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.03);
  --shadow-card-hover: 0 16px 32px -4px rgba(15, 23, 42, 0.09), 0 6px 12px -2px rgba(15, 23, 42, 0.04);
  --shadow-gold: 0 8px 24px -4px rgba(217, 119, 6, 0.22), 0 2px 8px -1px rgba(245, 158, 11, 0.15);
  --shadow-focus: 0 0 0 3px rgba(37, 99, 235, 0.25);

  /* Transitions */
  --ease-apple: cubic-bezier(0.16, 1, 0.3, 1);
  --transition-fast: 160ms var(--ease-apple);
  --transition-normal: 260ms var(--ease-apple);
}

[data-theme="dark"] {
  /* Surfaces Obsidienne */
  --surface-canvas: #090d16;
  --surface-card: #0f172a;
  --surface-card-hover: #162036;
  --surface-elevated: #1e293b;
  --surface-subtle: #141e33;
  --surface-muted: #1e293b;
  --surface-glass: rgba(15, 23, 42, 0.88);

  /* Bordures */
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-default: rgba(255, 255, 255, 0.14);
  --border-strong: rgba(255, 255, 255, 0.24);
  --border-focus: #3b82f6;

  /* Typographie */
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-tertiary: #94a3b8;
  --text-muted: #64748b;
  --text-inverse: #0f172a;

  /* Accents */
  --accent-primary: #3b82f6;
  --accent-primary-hover: #60a5fa;
  --accent-primary-subtle: rgba(59, 130, 246, 0.16);
  --accent-primary-border: rgba(59, 130, 246, 0.35);

  /* Statuts */
  --status-success: #10b981;
  --status-success-subtle: rgba(16, 185, 129, 0.15);
  --status-success-border: rgba(16, 185, 129, 0.3);
  --status-success-text: #34d399;

  --status-amber: #f59e0b;
  --status-amber-subtle: rgba(245, 158, 11, 0.15);
  --status-amber-border: rgba(245, 158, 11, 0.3);
  --status-amber-text: #fbbf24;

  --status-sky: #38bdf8;
  --status-sky-subtle: rgba(56, 189, 248, 0.15);
  --status-sky-border: rgba(56, 189, 248, 0.3);
  --status-sky-text: #7dd3fc;

  --status-purple: #a78bfa;
  --status-purple-subtle: rgba(167, 139, 250, 0.15);
  --status-purple-border: rgba(167, 139, 250, 0.3);
  --status-purple-text: #c4b5fd;

  /* Or VIP Dark Mode */
  --gold-primary: #fbbf24;
  --gold-hover: #f59e0b;
  --gold-bg-gradient: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(217, 119, 6, 0.06) 100%);
  --gold-ribbon-bg: linear-gradient(135deg, #d97706 0%, #f59e0b 50%, #fbbf24 100%);
  --gold-shimmer-color: rgba(255, 255, 255, 0.35);

  /* Ombres Nuit avec Diffusion */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.5);
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.5);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.6);
  --shadow-lg: 0 10px 24px rgba(0, 0, 0, 0.7);
  --shadow-xl: 0 20px 36px rgba(0, 0, 0, 0.8);
  --shadow-card-hover: 0 16px 36px -4px rgba(0, 0, 0, 0.8), 0 0 1px rgba(255, 255, 255, 0.2);
  --shadow-gold: 0 8px 32px -4px rgba(245, 158, 11, 0.25), 0 0 15px rgba(245, 158, 11, 0.15);
  --shadow-focus: 0 0 0 3px rgba(59, 130, 246, 0.35);
}
```

---

## 3. Écussons des 3 Voies Prioritaires (Instruction Client)

Chaque offre d'emploi porte un écusson d'en-tête ultra-visible signalant immédiatement la voie légale d'accès :

### KAPI 1 / VOIE 1 : Organisations Internationales (Statut Spécial MEAE)
- **Couleur** : Indigo / Bleu Céleste (`--status-sky`)
- **Icône** : Landmark (`<svg class="svg-icon">...column/pediment...</svg>`)
- **Libellé TR** : `🏛️ KAPI 1 : ULUSLARARASI KURUM (ÖZEL MAE STATÜSÜ)`
- **Libellé FR** : `🏛️ VOIE 1 : INSTITUTION INTERNATIONALE (STATUT MAE)`
- **Bordure haute de carte** : `border-top: 3.5px solid #0284c7;`

### KAPI 2 / VOIE 2 : Filiales de Groupes Turcs CCIFT & DEİK (Détachement Intra-Groupe ICT)
- **Couleur** : Or Métallique Prestige (`--gold-ribbon-bg`) avec animation Shimmer
- **Icône** : ShieldCheck (`<svg class="svg-icon">...shield with checkmark...</svg>`)
- **Libellé TR** : `🏢 KAPI 2 : TÜRK HOLDİNGİ (ŞİRKET İÇİ TRANSFER ICT)`
- **Libellé FR** : `🏢 VOIE 2 : GROUPE TURC (DÉTACHEMENT INTRA-GROUPE ICT)`
- **Aspect de carte** : Fond doré scintillant, bordure ambrée et reflet VIP

### KAPI 3 / VOIE 3 : Scale-ups Tech & Médias Internationaux (Passeport Talent)
- **Couleur** : Violet / Lilas Électrique (`--status-purple`)
- **Icône** : Rocket (`<svg class="svg-icon">...rocket launch...</svg>`)
- **Libellé TR** : `🚀 KAPI 3 : PASSEPORT TALENT (VİZE SPONSORLUĞU)`
- **Libellé FR** : `🚀 VOIE 3 : PASSEPORT TALENT (SPONSORISÉ)`
- **Bordure haute de carte** : `border-top: 3.5px solid #7c3aed;`

### KAPI 4 / VOIE 4 : Commerces & PME Franco-Turques (Emploi Local)
- **Couleur** : Ardoise Neutre (`--surface-subtle`)
- **Icône** : Building
- **Libellé TR** : `🏪 KAPI 4 : TÜRK İŞLETMELERİ (YEREL İSTİHDAM / İZİN)`
- **Libellé FR** : `🏪 VOIE 4 : COMMERCES & PME (EMPLOI LOCAL / TITRE)`

---

## 4. Effet Ruban Doré VIP & Gold Shimmer Animation

```css
@keyframes goldShimmer {
  0% { transform: translateX(-160%) skewX(-20deg); }
  35%, 100% { transform: translateX(290%) skewX(-20deg); }
}

.ccift-badge-shimmer::after, .ccift-highlight-box::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 50%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    var(--gold-shimmer-color) 50%,
    transparent 100%
  );
  transform: translateX(-160%) skewX(-20deg);
  animation: goldShimmer 3.2s infinite ease-in-out;
  pointer-events: none;
}
```

---

## 5. Bibliothèque d'Icônes Vectorielles SVG Intégrées

Toutes les icônes utilisent la classe `.svg-icon` (dimensions 16px ou 20px, `stroke-width: 2`, `stroke: currentColor`, `fill: none`) :

1. **Globe** : Carte d'identité bilatérale & diplomatie
2. **ShieldCheck** : Accréditation officielle CCIFT & DEİK
3. **Landmark** : Voie 1 Institutions Internationales (OECD, CoE, UNESCO)
4. **Rocket** : Voie 3 Tech Scale-ups & Passeport Talent
5. **Building** : Sièges sociaux, filiales & KAPI 4
6. **Languages** : Sélecteur bilingue TR / FR & statut linguistique
7. **Bookmark** (et `BookmarkFilled`) : Gestion des favoris & pipeline
8. **Briefcase** : Onglet Keşfet & postes d'emploi
9. **FileText** : Onglet Belgeler, lettres de motivation & fiches de suivi
10. **CheckCircle** : Vérification des critères (Sans Français)
11. **Sun** & **Moon** : Toggle instantané du thème clair/sombre
12. **ExternalLink** : Liens directs vers ATS et formulaires de candidature
13. **Filter** : Filtres multi-facettes
14. **Search** : Barre de recherche instantanée
15. **MapPin** : Localisation géographique des postes
16. **Plane** : Relocalisation & prise en charge du visa
17. **Sparkles** : Score d'adéquation et pertinence bilatérale
18. **Copy** : Copie 1-clic des modèles de motivation

---

## 6. Architecture de l'App Shell & Persistance

```html
<header class="top-nav">
  <div class="brand-badge">
    <div class="brand-icon-box"><!-- SVG GLOBE --></div>
    <div>
      <strong>TALENT BILATÉRAL</strong>
      <span><!-- SVG SHIELD --> CCIFT & DEİK NETWORK</span>
    </div>
  </div>
  <div class="user-nav-controls">
    <div class="lang-switch-box">
      <button id="btnTR" class="lang-btn active">TR</button>
      <button id="btnFR" class="lang-btn">FR</button>
    </div>
    <button id="themeToggleBtn" class="theme-toggle-btn" onclick="toggleTheme()">
      <!-- SVG SUN OU MOON -->
    </button>
  </div>
</header>
```

### Script de persistance du thème :
```javascript
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('bilateral_theme', next);
  updateThemeButton(next);
}
```

### Intégration dans `exporter.py` :
Le fichier [`exporter.py`](file:///c:/Users/mysk/Documents/antigravity/happy-shannon/exporter.py) génère de manière 100% autonome [`dashboard.html`](file:///c:/Users/mysk/Documents/antigravity/happy-shannon/dashboard.html) en intégrant les 580+ icônes SVG, le CSS Haute Couture complet, le balayage doré scintillant, le toggle Dark/Light et les écussons KAPI 1/2/3.
