@echo off
chcp 65001 > nul
title Déploiement GitHub Pages & PWA - Fransaİş
color 0A

echo ===============================================================================
echo   🚀 DÉPLOIEMENT GITHUB PAGES GRATUIT & 100%% AUTOMATIQUE (Fransaİş PWA)
echo ===============================================================================
echo.
echo Ce script prépare et envoie votre projet sur GitHub pour :
echo  1. Fournir un lien public sécurisé HTTPS accessible par votre compagne en Turquie
echo  2. Activer le robot d'actualisation quotidienne automatique à 08h00 (TR)
echo  3. Permettre l'installation en 1-clic de l'application sur son iPhone ou Android
echo.
echo -------------------------------------------------------------------------------
echo.

:: Vérification de Git
where git >nul 2>nul
if %errorlevel% neq 0 (
    color 0C
    echo [ERREUR] Git n'est pas installé sur votre PC !
    echo Téléchargez Git ici : https://git-scm.com/downloads
    pause
    exit /b 1
)

:: Vérification du dépôt distant
git remote get-url origin >nul 2>nul
if %errorlevel% neq 0 (
    color 0E
    echo [ATTENTION] Aucun dépôt distant GitHub ('origin') n'est encore configuré.
    echo.
    echo Si vous venez de créer un dépôt vide sur https://github.com/new :
    set /p REPO_URL="Collez l'URL de votre dépôt GitHub (ex: https://github.com/mon-pseudo/fransais.git) : "
    if not "%REPO_URL%"=="" (
        git remote add origin %REPO_URL%
        echo [✓] Remote 'origin' configuré avec succès !
    ) else (
        echo [ANNULÉ] Aucune URL fournie.
        pause
        exit /b 1
    )
)

echo [1/4] Synchronisation des fichiers HTML et des icônes...
python generate_icons.py
python -c "import exporter, json, models; from models import JobOpportunity; jobs = [JobOpportunity(**d) for d in json.load(open('offres_france_turquie.json', encoding='utf-8'))]; exporter.export_to_html_dashboard(jobs, 'dashboard.html')"

echo.
echo [2/4] Indexation des fichiers Git...
git add .

echo.
echo [3/4] Création du commit...
git commit -m "🚀 Déploiement PWA Mobile + Auto-Refresh GitHub Actions"

echo.
echo [4/4] Envoi vers GitHub...
git branch -M master
git push -u origin master

if %errorlevel% equ 0 (
    color 0A
    echo.
    echo ===============================================================================
    echo   🎉 DÉPLOIEMENT RÉUSSI SUR GITHUB !
    echo ===============================================================================
    echo.
    echo DERNIÈRE ÉTAPE (À faire 1 seule fois dans votre navigateur) :
    echo.
    echo 1. Rendez-vous sur votre dépôt GitHub :
    echo    Allez dans 'Settings' (Paramètres) ➔ 'Pages'
    echo 2. Dans 'Build and deployment' ➔ 'Source' :
    echo    Choisissez 'Deploy from a branch' ➔ branche 'master', dossier '/ (root)'
    echo 3. GitHub vous donnera votre lien Web public, sous la forme :
    echo    https://<votre-pseudo>.github.io/<nom-du-depot>/
    echo.
    echo 4. ENVOYEZ CE LIEN À VOTRE COMPAGNE EN TURQUIE !
    echo    Dès qu'elle l'ouvre sur Safari (iPhone) ou Chrome (Android), elle verra :
    echo    "📱 Fransaİş'i Telefona Yükle (1-Tık)"
    echo    Elle clique, et l'application est sur son écran d'accueil sans pub et 100%% gratuite !
    echo.
    echo 5. Tout s'actualisera tout seul chaque jour à 08h00 sans votre intervention !
    echo ===============================================================================
) else (
    color 0C
    echo.
    echo [ERREUR] Le git push a échoué. Vérifiez vos identifiants GitHub ou vos permissions.
)

echo.
pause
