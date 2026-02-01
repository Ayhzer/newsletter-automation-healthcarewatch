# 📚 Index complet des fichiers

Guide pour trouver rapidement ce dont vous avez besoin.

## 🚀 Je veux démarrer immédiatement

**Lire dans cet ordre:**

1. **START_HERE.md** (15 min) ← **COMMENCEZ ICI**
2. **QUICKSTART.md** (5 min) - Alternative ultra-rapide
3. **INSTALLATION.md** (30 min) - Installation détaillée
4. **Lancer:** `cd src/healthcare_watch && python healthcare_watch.py`

---

## 🔧 Je dois installer le projet

### Installation locale
- 📖 **INSTALLATION.md** - Guide étape par étape
- 📖 **QUICKSTART.md** - Version courte
- ⚙️ **requirements.txt** - Dépendances
- ⚙️ **setup.py** / **pyproject.toml** - Métadonnées

### Scripts d'aide
- 🐚 **run_help.bat** (Windows)
- 🐚 **run_help.sh** (Linux/Mac)

### Fichiers de config
- 📄 **.env.example** - Template variables d'env
- 📄 **.gitignore** - Git ignore list

---

## 🔐 J'ai besoin de secrets/API

### Où obtenir les secrets?
- 📖 **START_HERE.md** (section "Secrets" facile)
- 📖 **INSTALLATION.md** (section "Étape 1: Obtenir les secrets" détaillée)
- 📖 **GITHUB_SECRETS.md** (pour GitHub Actions)

### Variables requises
- **PERPLEXITY_API_KEY** - https://www.perplexity.ai/
- **NOTION_TOKEN** - https://www.notion.so/my-integrations
- **NOTION_PARENT_PAGE_ID** - Page Notion
- **NOTIFICATION_EMAIL** - Votre email
- **SMTP_*** - Configuration email

### Fichiers
- 📄 **.env.example** - Copier en `.env` et remplir

---

## ✏️ Je veux créer/modifier les prompts

### Guides
- 📖 **PROMPTS_GUIDE.md** ← **LA RÉFÉRENCE**
  - Templates pour différents usages
  - Anatomy d'un bon prompt
  - Exemples concrets
  - Conseils d'optimisation

### Configuration YAML
- 📄 **config/prompts.example.yaml** - Template avec 3 exemples
  - Daily Health News (quotidien)
  - Weekly Health Tech (hebdomadaire)
  - Monthly Clinical Research (mensuel)
- 📄 **config/prompts.yaml** - À créer depuis .example

### Tester les prompts
```bash
python src/healthcare_watch/healthcare_watch.py
```

---

## 🏗️ Je veux comprendre l'architecture

### Comprendre le projet
- 📖 **README.md** - Vue d'ensemble complète (550+ lignes)
- 📖 **PROJECT_STRUCTURE.md** - Architecture détaillée
- 📖 **STRUCTURE_SUMMARY.txt** - Résumé visuel

### Comment ça marche?
- 📖 **README.md** (section "Cycle de vie")
- 📖 **PROJECT_STRUCTURE.md** (section "Flux d'exécution")

### Fichiers importants
- 🐍 **src/healthcare_watch/healthcare_watch.py** (350+ lignes)
  - Fonction `load_config()` - Charge YAML + env
  - Fonction `query_perplexity()` - Appelle Perplexity API
  - Fonction `create_notion_page()` - Crée pages Notion
  - Fonction `send_notification_email()` - Envoie emails
  - Fonction `should_run_prompt()` - Gère fréquences
  - Fonction `main()` - Orchestration

---

## 🚨 J'ai une erreur/question

### D'abord
- 📖 **TROUBLESHOOTING.md** ← **CONSULTEZ CECI**
  - 7 erreurs courantes avec solutions
  - FAQ complète
  - Débogage avancé
  - Tests de connexion

### Si pas d'aide
- 📖 **README.md** (section "Dépannage")
- 📖 **INSTALLATION.md** (section "Dépannage d'installation")

### Erreurs spécifiques
- Module not found? → TROUBLESHOOTING.md #1
- API Key? → TROUBLESHOOTING.md #2
- Notion? → TROUBLESHOOTING.md #3
- SMTP? → TROUBLESHOOTING.md #5
- Perplexity? → TROUBLESHOOTING.md #6
- GitHub Actions? → Voir logs dans Actions tab

---

## 🤖 Je veux utiliser GitHub Actions

### Configuration
- 📖 **GITHUB_SECRETS.md** ← **POUR GITHUB ACTIONS**
  - Où ajouter les secrets
  - Chaque secret expliqué
  - Vérification
  - Dépannage

- 📖 **INSTALLATION.md** (section "Étape 6: GitHub Actions")
  - Steps pour créer repo
  - Ajouter secrets
  - Vérifier les runs

### Workflow
- 🔄 **.github/workflows/healthcare-watch.yml**
  - Exécution quotidienne (08:00 + 16:00 UTC)
  - Trigger manuel
  - Gestion secrets automatique

### Modifier les horaires
Éditer `.github/workflows/healthcare-watch.yml`:
```yaml
schedule:
  - cron: '0 8 * * *'  # 08:00 UTC chaque jour
```

---

## 📖 Guide de lecture par rôle

### Je suis développeur
1. **README.md** - Vue générale
2. **PROJECT_STRUCTURE.md** - Architecture
3. **src/healthcare_watch/healthcare_watch.py** - Code principal
4. **PROMPTS_GUIDE.md** - Créer prompts
5. **TROUBLESHOOTING.md** - Déboguer

### Je suis utilisateur
1. **START_HERE.md** - Démarrage rapide
2. **INSTALLATION.md** - Installation
3. **PROMPTS_GUIDE.md** - Customiser prompts
4. **GITHUB_SECRETS.md** - GitHub setup
5. **TROUBLESHOOTING.md** - Erreurs

### Je suis admin/DevOps
1. **README.md** - Vue générale
2. **GITHUB_SECRETS.md** - Secrets GitHub
3. **.github/workflows/healthcare-watch.yml** - Workflow
4. **PROJECT_STRUCTURE.md** - CI/CD
5. **TROUBLESHOOTING.md** - Monitoring

### Je suis contributeur
1. **CONTRIBUTING.md** - Contribution guide
2. **PROJECT_STRUCTURE.md** - Architecture
3. **src/healthcare_watch/healthcare_watch.py** - Code
4. **PROMPTS_GUIDE.md** - Exemples
5. Créer une branch + PR

---

## 📋 Checklist par étape

### ✅ Installation
- [ ] Lire: START_HERE.md
- [ ] Fichier: .env créé
- [ ] Fichier: config/prompts.yaml créé
- [ ] Commande: `pip install -r requirements.txt`
- [ ] Test: `python src/healthcare_watch/healthcare_watch.py`

### ✅ Configuration
- [ ] Lire: PROMPTS_GUIDE.md
- [ ] Obtenir: 8 secrets (START_HERE.md section "Secrets")
- [ ] Éditer: config/prompts.yaml
- [ ] Tester: Scripts d'aide (run_help.bat ou run_help.sh)

### ✅ GitHub Actions (optionnel)
- [ ] Lire: GITHUB_SECRETS.md
- [ ] Créer: Repository GitHub
- [ ] Ajouter: 8 secrets dans Settings
- [ ] Push: Code vers GitHub
- [ ] Vérifier: Actions tab

### ✅ Production
- [ ] Vérifier: Pages Notion créées
- [ ] Vérifier: Emails reçus
- [ ] Monitorer: data/output/.last_run.json
- [ ] Supporter: Users via TROUBLESHOOTING.md

---

## 🎯 Fichiers par fréquence d'usage

### Consultés souvent
1. **config/prompts.yaml** - Customisation quotidienne
2. **.env** - Secrets (rarement modifiés)
3. **data/output/.last_run.json** - Suivi des exécutions
4. **START_HERE.md** - Première consultation

### Consultés régulièrement
1. **PROMPTS_GUIDE.md** - Créer nouvelles prompts
2. **README.md** - Questions générales
3. **.github/workflows/healthcare-watch.yml** - Ajuster horaires

### Consultés occasionnellement
1. **TROUBLESHOOTING.md** - En cas d'erreur
2. **INSTALLATION.md** - Re-setup
3. **PROJECT_STRUCTURE.md** - Comprendre le code

### Rarement consultés
1. **src/healthcare_watch/healthcare_watch.py** - Dev seulement
2. **CONTRIBUTING.md** - Si contribution
3. **LICENSE** - Licence légale

---

## 🔍 Recherche rapide par mot-clé

| Besoin | Fichier |
|--------|---------|
| API key Perplexity | START_HERE.md, INSTALLATION.md |
| API Notion | START_HERE.md, GITHUB_SECRETS.md |
| SMTP Gmail | INSTALLATION.md (1.4) |
| Erreur Module | TROUBLESHOOTING.md #1 |
| Erreur API | TROUBLESHOOTING.md #2-3 |
| Erreur Email | TROUBLESHOOTING.md #5 |
| Ajouter prompt | PROMPTS_GUIDE.md |
| Changer horaire | .github/workflows/healthcare-watch.yml |
| Débogage | TROUBLESHOOTING.md (Advanced) |
| Contribution | CONTRIBUTING.md |

---

## 📞 Support rapide

### "Je suis perdu"
→ Lire: **START_HERE.md** (15 min)

### "Ça marche pas"
→ Lire: **TROUBLESHOOTING.md** (section pertinente)

### "Comment créer un prompt?"
→ Lire: **PROMPTS_GUIDE.md**

### "Comment GitHub Actions?"
→ Lire: **GITHUB_SECRETS.md**

### "Je veux tout comprendre"
→ Lire: **README.md** (complet)

---

## ✨ Résumé

```
Besoin urgent?      → START_HERE.md
Installez?          → INSTALLATION.md
Erreur?             → TROUBLESHOOTING.md
Prompts?            → PROMPTS_GUIDE.md
GitHub?             → GITHUB_SECRETS.md
Tout savoir?        → README.md
Architecture?       → PROJECT_STRUCTURE.md
Contribuer?         → CONTRIBUTING.md
```

---

**Version**: 1.0.0
**Date**: Février 2026
**Licence**: MIT
