@echo off
REM Script d'aide - Healthcare Watch
REM Usage: run_help.bat [commande]

if "%1"=="" goto help

if /i "%1"=="install" goto install
if /i "%1"=="test" goto test
if /i "%1"=="env" goto env
if /i "%1"=="run" goto run

:help
echo.
echo ============================================================
echo   Healthcare Watch - Script d'aide
echo ============================================================
echo.
echo Commandes disponibles:
echo.
echo   run_help install      - Installer les dépendances
echo   run_help env          - Charger les variables d'env
echo   run_help test         - Exécuter un test
echo   run_help run          - Lancer le script principal
echo.
echo ============================================================
echo.
goto end

:install
echo.
echo 🔧 Installation des dépendances...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ✅ Installation terminée
goto end

:env
echo.
echo 📦 Chargement de l'environnement...
for /f "tokens=1* delims==" %%A in (more .env) do (
    if not "%%B"=="" (
        set "%%A=%%B"
        echo   ✅ %%A
    )
)
echo 📦 Environnement chargé
goto end

:test
echo.
echo 🧪 Test de configuration...
python -c "import requests; print('✅ requests OK')" || goto error
python -c "import yaml; print('✅ pyyaml OK')" || goto error
python -c "import notion_client; print('✅ notion_client OK')" || goto error
python -c "import pytz; print('✅ pytz OK')" || goto error
echo.
echo ✅ Tous les modules sont installés
goto end

:run
echo.
echo 🚀 Lancement de Healthcare Watch...
cd src\healthcare_watch
python healthcare_watch.py
goto end

:error
echo.
echo ❌ Une erreur s'est produite
exit /b 1

:end
