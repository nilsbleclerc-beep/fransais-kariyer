# 📱 Guide d'Installation Rapide & Déploiement Mobile (Fransaİş PWA)

> **Objectif :** Permettre à votre compagne (en Turquie) d'avoir l'application directement installée sur son smartphone (iPhone ou Android), 100% gratuite, sans passer par l'App Store/Play Store, avec un chargement instantané même sans internet, et une actualisation automatique quotidienne des offres.

---

## 💌 Message à copier-coller à votre compagne (WhatsApp / Telegram)

Vous pouvez lui envoyer directement ce court message en turc :

```text
Aşkım, Fransa'daki iş fırsatlarını ve vize süreçlerini kolayca takip edebilmen için sana özel bir mobil uygulama hazırladım ❤️ 

Aşağıdaki linke telefonundan tıkla:
👉 https://<VOTRE-PSEUDO-GITHUB>.github.io/<NOM-DU-DEPOT>/

📲 Telefondan Açınca 30 Saniyede Uygulama Olarak Yüklemek İçin:
- iPhone (Safari): Alttaki [Paylaş] simgesine bas ➔ "Ana Ekrana Ekle"ye dokun.
- Android (Chrome): Ekranda çıkan "Uygulamayı Telefona Yükle" butonuna dokun.

Bitti! Artık telefonunun ana ekranında bir mobil uygulama gibi yer alacak. İlanlar her sabah saat 08:00'de otomatik olarak güncelleniyor. Seni seviyorum! 🇹🇷🇫🇷
```

---

## 📱 Comment installer l'application en 30 secondes chrono ?

### 🍏 Sur iPhone / iPad (Safari)

1. Ouvrir le lien dans **Safari**.
2. Appuyer sur l'icône **Partager** (le carré avec la flèche vers le haut $\uparrow$ en bas au centre).
3. Faire défiler légèrement la liste et toucher **« Sur l'écran d'accueil »** (avec l'icône $+$).
4. Appuyer sur **« Ajouter »** en haut à droite.
5. **C'est fini !** L'icône de l'application *Fransaİş* apparaît sur son écran d'accueil et s'ouvre en plein écran natif (sans barre de navigateur).

### 🤖 Sur Android (Google Chrome, Samsung Internet, etc.)

1. Ouvrir le lien dans **Chrome**.
2. Un bandeau apparaît automatiquement : **« 📱 Uygulamayı Telefona Yükle (1-Tık) »**.
3. Cliquer sur **« Hemen Yükle »** (ou via le menu $\vdots$ ➔ *« Installer l'application »*).
4. Confirmer.
5. **C'est fini !** L'application est installée sur son smartphone comme une application native.

---

## 🔄 Comment fonctionne le système de Rafraîchissement des Offres ?

### 1. Mode 100% Automatique dans le Cloud (Zéro intervention pour elle)
* Chaque matin à **08:00 (heure d'Istanbul)** / 07:00 (heure de Paris), le robot GitHub Actions s'exécute automatiquement et gratuitement sur les serveurs de GitHub.
* Il scanne les institutions européennes (Conseil de l'Europe, UNESCO, OCDE), les grands groupes turcs en France (Beko, THY, Ekol, Barsan, Şişecam, etc.), et les scale-ups tech anglophones.
* Il régénère le catalogue d'offres et redéploie le site instantanément.
* **Résultat :** Dès qu'elle ouvre son application le matin, les nouvelles offres sont déjà là, sans qu'aucun de vous deux n'ait à lever le petit doigt !

### 2. Mode Rafraîchissement sur Demande (1-Clic depuis votre PC)
* Si vous souhaitez relancer une recherche manuelle immédiate :
  1. Double-cliquez sur le fichier **`Lancer_Application.bat`** sur votre ordinateur.
  2. Votre navigateur s'ouvre automatiquement sur `http://localhost:8080`.
  3. Cliquez sur le bouton en haut à droite **« 🔄 Şimdi Yenile / Actualiser »**.
  4. Le robot rescannera le web en tâche de fond et mettra à jour la liste des offres avec une notification visuelle.

---

## 🚀 Comment déployer le site sur GitHub Pages (1 seule fois) ?

1. Double-cliquez sur le fichier **`deploy_github.bat`**.
2. Saisissez l'adresse de votre dépôt GitHub (ex: `https://github.com/mon-pseudo/fransais.git`).
3. Le script va envoyer tous les fichiers (PWA, icônes, workflows, HTML).
4. Rendez-vous sur votre dépôt GitHub :
   * Cliquez sur **Settings** ➔ **Pages**
   * Dans **Source**, sélectionnez **GitHub Actions**
5. Copiez votre lien public et envoyez-le à votre compagne !

---

## 💡 Atouts Techniques Clés de cette Solution

* **100% Gratuite à vie :** Utilise l'infrastructure GitHub Pages & GitHub Actions (aucune carte bancaire requise, aucun coût d'hébergement).
* **Mode Hors-Ligne (Offline First) :** Grâce au Service Worker `sw.js`, même si sa connexion mobile est faible ou coupée dans les transports, l'application s'ouvre en moins de 100 millisecondes avec toutes les offres déjà consultables.
* **Ergonomie Bilingue :** L'application démarre par défaut en **Turc (TR)** pour son confort absolu, avec bascule instantanée en **Français (FR)** en 1-clic.
* **Respect de la vie privée :** Ses candidatures, favoris et notes sont stockés en sécurité directement dans la mémoire locale de son téléphone (*LocalStorage*).
