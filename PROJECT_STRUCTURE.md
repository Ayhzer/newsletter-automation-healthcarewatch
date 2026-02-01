# Structure du Projet - Healthcare Watch

Documentation de la structure et de l'architecture.

## 📂 Répertoires

```
healthcare-watch/
├─ src/
│  ├─ __init__.py
│  └─ healthcare_watch/
│     ├─ __init__.py              # Module init
│     └─ healthcare_watch.py       # Script principal
│
├─ config/
│  ├─ prompts.example.yaml        # Template configuration (à copier)
│  ├─ config.example.py           # Config dev (optionnel)
│  └─ prompts.yaml                # Configuration (à créer)
│
├─ data/
│  └─ output/
│     ├─ .last_run.json           # Suivi exécutions
│     └─ *.txt                    # Synthèses (optionnel)
│
├─ .github/
│  └─ workflows/
│     └─ healthcare-watch.yml     # GitHub Actions workflow
│
└─ Fichiers racine
   ├─ README.md                   # Documentation principale
   ├─ INSTALLATION.md             # Guide installation
   ├─ QUICKSTART.md               # Démarrage rapide
   ├─ GITHUB_SECRETS.md           # Config GitHub Secrets
   ├─ CONTRIBUTING.md             # Contribution guide
   ├─ PROJECT_STRUCTURE.md        # Ce fichier
   ├─ LICENSE                     # Licence MIT
   ├─ .gitignore                  # Git ignore
   ├─ requirements.txt            # Dépendances pip
   ├─ setup.py                    # Installation setup
   ├─ pyproject.toml              # Métadonnées projet
   └─ .env                        # Variables d'env (ne pas committer)
```

## 🔄 Flux d'exécution

```
healthcare_watch.py
├─ load_config()
│  └─ Charge prompts.yaml + secrets env
│
├─ Pour chaque prompt:
│  ├─ should_run_prompt()
│  │  └─ Vérifie frequency vs .last_run.json
│  ├─ query_perplexity()
│  │  └─ Appel API Perplexity avec retry
│  ├─ create_notion_page()
│  │  └─ Crée page Notion avec timestamp
│  ├─ send_notification_email()
│  │  └─ Envoie email SMTP si activé
│  └─ update_last_run()
│     └─ Met à jour .last_run.json
│
└─ Affiche résumé + exit code
```

## 🔐 Configuration

### prompts.yaml

Structure:
```yaml
general:
  timezone: str           # Fuseau horaire
  notifications:
    enabled: bool         # Activer/désactiver emails
    email_on_error: bool  # Email si erreur

prompts:
  nom_prompt:
    enabled: bool                      # Actif?
    frequency: str                     # daily/weekly/monthly
    page_title: str                    # Titre page Notion
    parent_page_id: str (optionnel)    # ID page parent
    prompt: str                        # Texte prompt Perplexity
    options:
      max_tokens: int                  # Limite tokens
      temperature: float               # 0.0-1.0
      model: str                       # sonar, etc.
```

### Variables d'environnement

Requises:
- `PERPLEXITY_API_KEY` - Clé API Perplexity
- `NOTION_TOKEN` - Token API Notion
- `NOTIFICATION_EMAIL` - Email notifications
- `SMTP_*` - Config SMTP

Optionnelles:
- `NOTION_PARENT_PAGE_ID` - Défaut si pas dans YAML
- `TIMEZONE` - Défaut Europe/Paris

## 📊 Suivi d'exécution

`.last_run.json`:
```json
{
  "daily_health_news": "2024-01-15T10:00:00",
  "weekly_health_tech": "2024-01-08T10:00:00"
}
```

Permet:
- ✅ Respecter les fréquences
- ✅ Éviter les exécutions dupliquées
- ✅ Tracker l'historique

## 🔗 Intégrations

### Perplexity API
- Endpoint: `https://api.perplexity.ai/chat/completions`
- Model: `sonar`
- Rate limit: Gestion retry automatique

### Notion API
- Client: `notion_client.Client`
- Crée pages enfants sous `parent_page_id`
- Format: Blocs texte, headings, paragraphes

### SMTP Email
- Protocole: SMTP + STARTTLS
- Format: Text + HTML multipart
- Sujet: `✅ HealthcareWatch - {prompt_key}`

## 🚀 GitHub Actions

Workflow `.github/workflows/healthcare-watch.yml`:
- Trigger: Cron schedule + manual
- Horaires: 08:00 UTC + 16:00 UTC (quotidien)
- Env: Tous les secrets depuis GitHub Secrets
- Output: Logs visibles dans Actions

## 📝 Logs et Débogage

Lors de l'exécution, affiche:
- ⚙️ Configuration loading
- 📋 Compte prompts
- ▶️ Prompt en cours
- ✅/❌ Résultats
- 📊 Résumé final

Exit code:
- `0` = Succès
- `1` = Erreurs détectées

## 🔧 Maintenance

Points clés:
- Vérifier `data/output/.last_run.json` périodiquement
- Archiver les anciennes pages Notion
- Mettre à jour prompts.yaml selon besoins
- Renouveler API keys/tokens régulièrement
- Monitorer GitHub Actions pour erreurs

## 🎯 Cas d'usage

1. **Newsletter quotidienne** → `frequency: daily`
2. **Synthèse hebdomadaire** → `frequency: weekly`
3. **Rapport mensuel** → `frequency: monthly`
4. **Suivi temps réel** → `frequency: hourly`
5. **Décisionnel** → Utiliser data/output pour analyses

## 📈 Évolutions futures

Possibilités:
- [ ] Slack/Discord webhooks
- [ ] Export PDF des pages
- [ ] API REST pour trigger
- [ ] Dashboard analytics
- [ ] Multi-language prompts
- [ ] Intégration Zapier

---

**Dernière mise à jour**: Janvier 2024
