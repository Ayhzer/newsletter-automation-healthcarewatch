# Healthcare Watch - Newsletter Automatisée

🏥 **Healthcare Watch** est une solution Python d'automatisation de newsletters sanitaires qui utilise **Perplexity AI** pour récupérer et synthétiser l'actualité médicale, puis l'enregistre dans **Notion** et envoie des notifications par email.

## 🎯 Fonctionnalités principales

- ✅ **Prompts personnalisables** pour différents besoins (santé générale, technologie médicale, recherche clinique, etc.)
- ✅ **Fréquences flexibles**: quotidienne, hebdomadaire, mensuelle ou autre
- ✅ **Intégration Perplexity AI**: Synthèses intelligentes en temps réel
- ✅ **Pages Notion automatisées**: Création de pages avec titre, date et heure-minute
- ✅ **Notifications email**: Récapitulatif avec option désactivation
- ✅ **Configuration simple**: Fichier YAML facile à éditer
- ✅ **GitHub Actions ready**: Planification automatique dans le cloud
- ✅ **Pas de secrets**: Configuration non-sensible en YAML

## 📋 Structure du projet

```
healthcare-watch/
├─ src/
│  ├─ __init__.py
│  └─ healthcare_watch/
│     ├─ __init__.py
│     └─ healthcare_watch.py      # Script principal
├─ config/
│  ├─ prompts.example.yaml        # Template de configuration
│  └─ config.example.py           # Config développement (optionnel)
├─ data/
│  └─ output/
│     ├─ .last_run.json           # Suivi des exécutions
│     └─ *.txt                    # Synthèses en texte brut (optionnel)
├─ .github/workflows/
│  └─ healthcare-watch.yml        # Workflow GitHub Actions
├─ requirements.txt               # Dépendances Python
├─ setup.py                       # Installation Python
├─ pyproject.toml                 # Métadonnées projet
├─ README.md                      # Ce fichier
└─ INSTALLATION.md                # Guide installation détaillé
```

## ⚡ Démarrage rapide (5 minutes)

### 1️⃣ Cloner le projet

```bash
git clone https://github.com/yourusername/healthcare-watch.git
cd healthcare-watch
```

### 2️⃣ Créer un environnement virtuel

```bash
# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurer les secrets

Créer un fichier `.env` à la racine :

```bash
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxx
NOTION_TOKEN=ntn_xxxxxxxxxxxxxxxxxxxxx
NOTION_PARENT_PAGE_ID=xxxxxxxxxxxxxxxxxxxxx
NOTIFICATION_EMAIL=votre.email@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre.email@example.com
SMTP_PASSWORD=votre_password_app
```

### 5️⃣ Configurer les prompts

Copier et éditer le fichier de configuration:

```bash
cp config/prompts.example.yaml config/prompts.yaml
```

Éditer `config/prompts.yaml` pour ajouter vos prompts personnalisés.

### 6️⃣ Exécuter une première fois

```bash
cd src/healthcare_watch
python healthcare_watch.py
```

Vous devriez voir:
```
============================================================
🏥 HEALTHCARE WATCH - Newsletter Sanitaire
============================================================
✅ Configuration chargée
📋 3 prompt(s) configuré(s)
...
✅ daily_health_news exécuté avec succès
```

## 🔧 Configuration YAML

### Structure de base

```yaml
general:
  timezone: "Europe/Paris"  # Fuseau horaire
  notifications:
    enabled: true           # Activer/désactiver les emails
    email_on_error: true    # Email en cas d'erreur

prompts:
  nom_du_prompt:
    enabled: true
    frequency: "daily"      # daily, weekly, monthly, hourly
    page_title: "Titre de la page Notion"
    parent_page_id: ""      # Optionnel, par défaut env var
    prompt: |
      Votre prompt Perplexity ici...
    options:
      max_tokens: 2000
      temperature: 0.3
      model: "sonar"
```

### Exemple complet

```yaml
general:
  timezone: "Europe/Paris"
  notifications:
    enabled: true
    include_summary: true
    email_on_error: true

prompts:
  daily_health_news:
    enabled: true
    frequency: "daily"
    page_title: "Actualités Santé - Daily"
    prompt: |
      Tu es expert en santé publique.
      Synthétise les dernières actualités médicales du jour avec:
      1. Top 5 actualités
      2. Tendances émergentes
      3. Statistiques clés
      4. Impact professionnel
    options:
      max_tokens: 2000
      temperature: 0.3
```

## 🔐 Variables d'environnement requises

### Perplexity AI

```
PERPLEXITY_API_KEY=pplx-xxxxx
```
Obtenez votre clé sur: https://www.perplexity.ai/

### Notion API

```
NOTION_TOKEN=ntn_xxxxx
NOTION_PARENT_PAGE_ID=xxxxx
```

1. Créer une intégration: https://www.notion.so/my-integrations
2. Copier le token (Bearer token)
3. Obtenir l'ID de la page: Ouvrir Notion, copier l'URL, l'ID est après `/share/`

### Email (SMTP)

```
NOTIFICATION_EMAIL=votre.email@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre.email@example.com
SMTP_PASSWORD=votre_password_app  # App password, pas votre mot de passe
```

Pour Gmail:
1. Activer l'authentification à deux facteurs
2. Générer un "App password": https://myaccount.google.com/apppasswords
3. Utiliser ce mot de passe dans SMTP_PASSWORD

## 🚀 GitHub Actions - Planification automatique

### 1. Ajouter les secrets GitHub

1. Aller à: **Settings → Secrets and variables → Actions**
2. Ajouter les secrets:
   - `PERPLEXITY_API_KEY`
   - `NOTION_TOKEN`
   - `NOTION_PARENT_PAGE_ID`
   - `NOTIFICATION_EMAIL`
   - `SMTP_SERVER`
   - `SMTP_PORT`
   - `SMTP_USERNAME`
   - `SMTP_PASSWORD`

### 2. Le workflow s'exécutera automatiquement

- ✅ Tous les jours à 08:00 UTC (10:00 CET)
- ✅ Tous les jours à 16:00 UTC (18:00 CET)
- ✅ À chaque push (optionnel)
- ✅ Déclenchement manuel possible

### 3. Modifier les horaires

Éditer `.github/workflows/healthcare-watch.yml`:

```yaml
schedule:
  # Syntaxe cron: minute heure jour mois jour_semaine
  - cron: '30 9 * * *'  # 09:30 UTC tous les jours
  - cron: '0 8 * * 1'   # Lundi 08:00 UTC (hebdomadaire)
  - cron: '0 8 1 * *'   # Le 1er à 08:00 UTC (mensuel)
```

### 4. Vérifier les exécutions

Dans **Actions tab**, vous verrez:
- ✅ Les succès (pages Notion créées)
- ❌ Les erreurs (logs disponibles)
- 📊 Historique complet

## 📝 Fichier de suivi des exécutions

Le fichier `data/output/.last_run.json` suivi les dates d'exécution:

```json
{
  "daily_health_news": "2024-01-15T10:00:00",
  "weekly_health_tech": "2024-01-08T10:00:00"
}
```

Ce fichier vous permet de:
- ✅ Vérifier quand chaque prompt a s'est exécuté
- ✅ Respecter les fréquences (daily, weekly, monthly)
- ✅ Éviter les exécutions répétées

## 🐛 Dépannage

### Erreur: `PERPLEXITY_API_KEY n'est pas configurée`

```bash
# Vérifier la variable d'environnement
echo $PERPLEXITY_API_KEY

# Ou la charger depuis .env
source .env
```

### Erreur: `parent_page_id non défini`

Assurez-vous qu'une de ces conditions est vraie:
1. Définir `NOTION_PARENT_PAGE_ID` en variable d'environnement
2. Ou spécifier `parent_page_id` dans chaque prompt du YAML

### Erreur: `Notion authentication failed`

```bash
# Vérifier le token
echo $NOTION_TOKEN

# Vérifier que l'intégration a accès à la page
# Dans Notion, aller à la page → ... → Connections
```

### Email non envoyé

Vérifier la configuration SMTP:
- Gmail: Utiliser "App password", pas le mot de passe du compte
- D'autres providers: Vérifier le server/port (SMTP2GO: smtp.smtp2go.com:2525)

## 📚 Exemples de prompts

### Actualités santé générale

```yaml
prompt: |
  Tu es expert en santé publique et médecine générale.
  Synthétise les dernières actualités médicales avec:
  1. Top 5 actualités du jour
  2. Tendances émergentes
  3. Statistiques clés
  4. Impact sur professionnels santé
  5. Recommandations officielles
```

### Innovation technologique en santé

```yaml
prompt: |
  Tu es expert en digital health et technologie médicale.
  Fais une veille tech sur:
  1. Technologies émergentes (IA, blockchain, IoT)
  2. Startups santé et financements
  3. Cybersécurité médicale
  4. Réglementations digitales
  5. Cas d'usage implémentés
```

### Études cliniques et recherche

```yaml
prompt: |
  Tu es expert en recherche clinique.
  Synthétise les études cliniques importantes:
  1. Études marquantes du mois
  2. Méta-analyses récentes
  3. Essais cliniques en cours
  4. Impact sur pratique clinique
  5. Publications autorités
```

## 💾 Désactiver les notifications

Dans `config/prompts.yaml`:

```yaml
general:
  notifications:
    enabled: false  # Désactiver tous les emails
```

Ou pour un prompt spécifique, ne pas inclure le SMTP_PASSWORD.

## 🔄 Cycle de vie des pages Notion

Chaque exécution crée une **nouvelle page Notion** avec:

- ✅ Titre avec timestamp: `"Titre (15 January 2024 - 10:30)"`
- ✅ Date/heure de génération
- ✅ Contenu structuré de Perplexity
- ✅ Sous la page parent spécifiée

### Organisation Notion recommandée

```
Workspace
├─ 📊 Healthcare Watch (page parent)
│  ├─ 📰 Actualités Santé
│  │  ├─ Actualités (15 Jan 2024)
│  │  ├─ Actualités (16 Jan 2024)
│  │  └─ ...
│  ├─ 🔬 Technologie Médicale
│  │  ├─ Tech & Innovation (Jan 8)
│  │  └─ ...
│  └─ 📚 Recherche Clinique
│     ├─ Étude Cliniques (Jan 1)
│     └─ ...
```

## 🤝 Contribution

Les contributions sont bienvenues! Vous pouvez:

- 🐛 Signaler des bugs
- 💡 Proposer des améliorations
- 📝 Améliorer la documentation
- 🔧 Ajouter des fonctionnalités

## 📄 Licence

MIT License - voir [LICENSE](LICENSE)

## 📞 Support

Pour des questions ou des problèmes:
1. Vérifier la section "Dépannage" ci-dessus
2. Consulter les logs GitHub Actions
3. Créer une issue sur le repository

---

**Dernière mise à jour**: Janvier 2024
