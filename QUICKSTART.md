# Quickstart - Healthcare Watch

Démarrage rapide en 5 minutes.

## 1️⃣ Prérequis

- Python 3.8+
- Compte Perplexity
- Workspace Notion
- Compte email

## 2️⃣ Installation

```bash
# Cloner
git clone https://github.com/yourusername/healthcare-watch.git
cd healthcare-watch

# Environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate

# Dépendances
pip install -r requirements.txt
```

## 3️⃣ Secrets

Créer `.env` à la racine:

```
PERPLEXITY_API_KEY=pplx-xxxxx
NOTION_TOKEN=ntn_xxxxx
NOTION_PARENT_PAGE_ID=xxxxx
NOTIFICATION_EMAIL=your@gmail.com
GOOGLE_CREDENTIALS_JSON={"installed":{"client_id":"...","client_secret":"...",...}}
GOOGLE_OAUTH_TOKEN_JSON={"token":"...","refresh_token":"...","client_id":"...",...}
```

**Note**: Pour Gmail API, voir [INSTALLATION.md](INSTALLATION.md) pour la configuration OAuth2 complète.

## 4️⃣ Configuration

```bash
cp config/prompts.example.yaml config/prompts.yaml
# Éditer prompts.yaml avec vos besoins
```

## 5️⃣ Exécution

```bash
cd src/healthcare_watch
python healthcare_watch.py
```

## ✅ Vérification

- ✅ Script s'exécute sans erreurs
- ✅ Page Notion créée avec timestamp
- ✅ Email reçu

## 📚 Suite

- [Installation détaillée](INSTALLATION.md)
- [Configuration GitHub Secrets](GITHUB_SECRETS.md)
- [README complet](README.md)

---

**C'est fait!** 🎉
