#!/bin/bash
# Script d'aide - Healthcare Watch
# Usage: ./run_help.sh [commande]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

help() {
    cat << EOF

============================================================
  Healthcare Watch - Script d'aide
============================================================

Commandes disponibles:

  ./run_help.sh install      - Installer les dépendances
  ./run_help.sh env          - Charger les variables d'env
  ./run_help.sh test         - Exécuter un test
  ./run_help.sh run          - Lancer le script principal

============================================================

EOF
}

install() {
    echo ""
    echo "🔧 Installation des dépendances..."
    python3 -m pip install --upgrade pip
    pip3 install -r requirements.txt
    echo "✅ Installation terminée"
}

env_load() {
    echo ""
    echo "📦 Chargement de l'environnement..."
    if [ -f .env ]; then
        export $(cat .env | grep -v '#' | xargs)
        echo "✅ Variables d'env chargées"
    else
        echo "⚠️  Fichier .env non trouvé"
    fi
}

test_env() {
    echo ""
    echo "🧪 Test de configuration..."
    python3 -c "import requests; print('✅ requests OK')" || exit 1
    python3 -c "import yaml; print('✅ pyyaml OK')" || exit 1
    python3 -c "import notion_client; print('✅ notion_client OK')" || exit 1
    python3 -c "import pytz; print('✅ pytz OK')" || exit 1
    echo ""
    echo "✅ Tous les modules sont installés"
}

run_main() {
    echo ""
    echo "🚀 Lancement de Healthcare Watch..."
    cd src/healthcare_watch
    python3 healthcare_watch.py
}

case "${1:-help}" in
    install) install ;;
    env) env_load ;;
    test) test_env ;;
    run) run_main ;;
    *) help ;;
esac
