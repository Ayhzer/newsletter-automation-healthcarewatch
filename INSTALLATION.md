# Guide d'installation détaillé - Healthcare Watch

Ce guide vous accompagne pas à pas pour installer et configurer **Healthcare Watch**.

## 📋 Prérequis

- Python 3.8+
- Git
- Compte Perplexity (gratuit ou payant)
- Workspace Notion
- Compte email (Gmail, Outlook, etc.)

## 🔐 Étape 1: Obtenir les secrets

### 1.1 Clé API Perplexity

1. Aller à https://www.perplexity.ai/
2. S'inscrire ou se connecter
3. Aller à **Settings → API**
4. Créer une nouvelle clé API
5. Copier la clé (commence par `pplx-`)

```
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxx
```

### 1.2 Token Notion

1. Aller à https://www.notion.so/my-integrations
2. Cliquer "Create new integration"
3. Donner un nom: "Healthcare Watch"
4. Cliquer "Create integration"
5. Copier le token (commence par `ntn_`)

```
NOTION_TOKEN=ntn_xxxxxxxxxxxxxxxxxxxxxxx
```

### 1.3 Page ID Notion

1. Ouvrir Notion et créer une page: "Healthcare Watch" (ou utiliser une existante)
2. Copier l'URL: `https://www.notion.so/workspace/Healthcare-Watch-xxxxxxxxxxxxx?v=...`
3. L'ID est la partie alphanumérrique longue avant le `?`
4. Formater sans tirets: `xxxxxxxxxxxxx` (32 caractères)

```
NOTION_PARENT_PAGE_ID=xxxxxxxxxxxxxxxxxxxxx
```

### 1.4 Email et SMTP

#### Pour Gmail:

1. Activer l'authentification à deux facteurs: https://myaccount.google.com/security
2. Aller à: https://myaccount.google.com/apppasswords
3. Sélectionner "Mail" et "Windows Computer"
4. Copier le mot de passe généré (16 caractères)

```
NOTIFICATION_EMAIL=votreemail@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votreemail@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
```

#### Pour Outlook/Hotmail:

```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=votreemail@outlook.com
SMTP_PASSWORD=votre_mot_de_passe
```

#### Pour un autre provider:

Trouver les paramètres SMTP sur le site du provider.

## 🚀 Étape 2: Installation locale

### 2.1 Cloner le repository

```bash
git clone https://github.com/yourusername/healthcare-watch.git
cd healthcare-watch
```

### 2.2 Créer l'environnement virtuel

```bash
# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Windows (CMD)
python -m venv .venv
.venv\Scripts\activate.bat
```

### 2.3 Installer les dépendances

```bash
pip install -r requirements.txt
```

## 🔑 Étape 3: Configurer les secrets

### 3.1 Créer un fichier .env

À la racine du projet, créer `.env`:

```bash
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxx
NOTION_TOKEN=ntn_xxxxxxxxxxxxxxxxxxxxx
NOTION_PARENT_PAGE_ID=xxxxxxxxxxxxxxxxxxxxx
NOTIFICATION_EMAIL=votre.email@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre.email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
```

### 3.2 Charger les variables d'environnement

```bash
# Linux/Mac
source .env

# Windows (PowerShell)
Get-Content .env | ForEach-Object { $name, $value = $_.split('='); [Environment]::SetEnvironmentVariable($name, $value) }

# Ou créer un script load_env.ps1:
# Voir exemple ci-dessous
```

**Script load_env.ps1 (Windows):**

```powershell
# À la racine du projet
$envFile = ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -and !$_.StartsWith("#")) {
            $name, $value = $_.split('=')
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
    Write-Host "✅ Variables d'environnement chargées"
}
```

## 📝 Étape 4: Configurer les prompts

### 4.1 Créer le fichier de configuration

```bash
cp config/prompts.example.yaml config/prompts.yaml
```

### 4.2 Éditer prompts.yaml

Ouvrir `config/prompts.yaml` et personnaliser:

```yaml
general:
  timezone: "Europe/Paris"  # Votre fuseau horaire
  notifications:
    enabled: true           # true = emails activés
    email_on_error: true

prompts:
  # Exemple 1: Newsletter quotidienne
  daily_news:
    enabled: true
    frequency: "daily"
    page_title: "Actualités du Jour"
    prompt: |
      Tu es expert en santé...
      Synthétise les dernières actualités avec...
  
  # Exemple 2: Newsletter hebdomadaire
  weekly_tech:
    enabled: true
    frequency: "weekly"
    page_title: "Tech & Innovation Médicale"
    prompt: |
      Tu es expert en technologie médicale...
```

## ✅ Étape 5: Test initial

### 5.1 Exécuter le script

```bash
cd src/healthcare_watch
python healthcare_watch.py
```

### 5.2 Résultat attendu

Vous devriez voir:

```
============================================================
🏥 HEALTHCARE WATCH - Newsletter Sanitaire
============================================================
⚙️  Chargement de la configuration...
✅ Configuration chargée
📋 3 prompt(s) configuré(s)

▶️  Prompt: daily_health_news
  ✅ Fréquence daily atteinte
  🔍 Interrogation Perplexity...
  🔄 Appel Perplexity (tentative 1/3)...
  ✅ Réponse reçue de Perplexity
  📝 Création page Notion: Actualités du Jour
  ✅ Page créée: xxxxxxxxxxxxx
  📧 Envoi de l'email de notification...
  ✅ Email envoyé
  ✅ daily_health_news exécuté avec succès

============================================================
📊 RÉSUMÉ
============================================================
✅ Exécutions réussies: 1
❌ Erreurs: 0
```

### 5.3 Vérifier dans Notion

1. Ouvrir Notion
2. Aller à la page "Healthcare Watch"
3. Vous devriez voir une nouvelle page enfant avec:
   - Titre: "Actualités du Jour (15 January 2024 - 10:30)"
   - Contenu structuré de Perplexity
   - Timestamp

## 🤖 Étape 6: GitHub Actions (optionnel)

### 6.1 Créer un GitHub repository

```bash
git remote add origin https://github.com/yourname/healthcare-watch.git
git branch -M main
git push -u origin main
```

### 6.2 Ajouter les secrets GitHub

1. Aller à **Settings → Secrets and variables → Actions**
2. Cliquer "New repository secret"
3. Ajouter chaque secret:

| Secret | Valeur |
|--------|--------|
| `PERPLEXITY_API_KEY` | `pplx-...` |
| `NOTION_TOKEN` | `ntn_...` |
| `NOTION_PARENT_PAGE_ID` | `xxxxx...` |
| `NOTIFICATION_EMAIL` | `votre@email.com` |
| `SMTP_SERVER` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `SMTP_USERNAME` | `votre@email.com` |
| `SMTP_PASSWORD` | `xxxx xxxx xxxx xxxx` |

### 6.3 Vérifier les Actions

1. Aller à **Actions**
2. Vous verrez les exécutions planifiées
3. Cliquer sur une exécution pour voir les logs

## 🛠️ Dépannage d'installation

### Problème: Python non trouvé

```bash
# Vérifier la version
python --version

# Si Python 3 n'est pas trouvé:
python3 --version
# Puis utiliser python3 au lieu de python dans les commandes
```

### Problème: pip ne marche pas

```bash
# Essayer
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Problème: Erreur avec PyYAML

```bash
pip install --upgrade pyyaml
```

### Problème: Variables d'environnement non chargées

```bash
# Vérifier que .env existe
ls -la .env  # ou dir /a .env sur Windows

# Charger manuellement dans Python
import os
from dotenv import load_dotenv
load_dotenv()
```

### Problème: Authentification Notion échouée

```bash
# Vérifier le token
echo $NOTION_TOKEN

# Dans Notion:
# 1. Vérifier que l'intégration est créée
# 2. Aller à la page parent
# 3. Cliquer ... → Connections
# 4. Vérifier que "Healthcare Watch" est listé
# 5. Ajouter la connexion si nécessaire
```

### Problème: Email non envoyé

```bash
# Pour Gmail, vérifier:
# 1. Authentification 2FA activée
# 2. App password généré (pas le mot de passe du compte)
# 3. SMTP_PASSWORD = app password exact

# Tester:
python -c "
import smtplib
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()
try:
    smtp.login('votre@gmail.com', 'votre_app_password')
    print('✅ Connexion SMTP OK')
except:
    print('❌ Authentification échouée')
smtp.quit()
"
```

## 📱 Conseils d'usage

### Sécurité

- ✅ Ne jamais committer `.env` dans Git
- ✅ Utiliser `git update-index --assume-unchanged .env`
- ✅ Ajouter `.env` à `.gitignore`
- ✅ Pour GitHub, utiliser les secrets (pas .env)

### Performance

- ⚡ Limiter `max_tokens` pour des réponses plus rapides
- ⚡ Utiliser `temperature: 0.2` pour des réponses déterministes
- ⚡ Espacer les exécutions (daily/weekly vs hourly)

### Maintenance

- 🔄 Vérifier périodiquement `data/output/.last_run.json`
- 🔍 Consulter les logs GitHub Actions
- 📊 Archiver les anciennes pages Notion si nécessaire

## ✨ Prochaines étapes

1. ✅ Installation terminée
2. Personnaliser les prompts dans `config/prompts.yaml`
3. Ajouter d'autres besoins (nouveaux prompts)
4. Configurer GitHub Actions pour l'automatisation
5. Intégrer d'autres outils (Slack, Discord, etc.)

---

**Questions?** Consultez le README.md ou créez une issue.
