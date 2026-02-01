# COMMENCEZ ICI 👈

Bienvenue dans **Healthcare Watch**! Ce fichier vous guide à travers les 3 étapes essentielles.

## ⏱️ Temps estimé: 15 minutes

---

## 1️⃣ INSTALLER (5 min)

### Étape 1.1: Cloner ou télécharger

Vous l'avez déjà (sinon: `git clone ...`)

### Étape 1.2: Environnement Python

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Étape 1.3: Dépendances

```bash
pip install -r requirements.txt
```

**✅ Installation terminée!**

---

## 2️⃣ CONFIGURER (5 min)

### Étape 2.1: Créer `.env`

Créer fichier `.env` à la racine:

```env
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxx
NOTION_TOKEN=ntn_xxxxxxxxxxxxxxxxxxxxx
NOTION_PARENT_PAGE_ID=xxxxxxxxxxxxxxxxxxxxx
NOTIFICATION_EMAIL=votre@email.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre@email.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
```

**Où obtenir les valeurs? Voir section "Secrets" ci-dessous**

### Étape 2.2: Créer `prompts.yaml`

```bash
cp config\prompts.example.yaml config\prompts.yaml
```

Éditer `config/prompts.yaml` - Les 3 prompts d'exemple devraient fonctionner!

**✅ Configuration terminée!**

---

## 3️⃣ TESTER (3 min)

### Étape 3.1: Lancer le script

```bash
cd src/healthcare_watch
python healthcare_watch.py
```

### Étape 3.2: Vérifier les résultats

Vous devriez voir:
```
✅ Configuration chargée
📋 3 prompt(s) configuré(s)
▶️  Prompt: daily_health_news
   ✅ daily_health_news exécuté avec succès
✅ Exécutions réussies: 1
```

### Étape 3.3: Vérifier Notion

1. Ouvrir Notion
2. Aller à votre page parent
3. **Vous devriez voir une nouvelle page enfant créée!**

**✅ Test réussi!**

---

## 🔐 Où obtenir les secrets?

### 1. PERPLEXITY_API_KEY

1. Aller à: https://www.perplexity.ai/
2. S'inscrire/Se connecter
3. Settings → API
4. Créer une clé → Copier

**Commence par:** `pplx-`

---

### 2. NOTION_TOKEN

1. Aller à: https://www.notion.so/my-integrations
2. "Create new integration"
3. Nommer: "Healthcare Watch"
4. "Create integration"
5. Copier le Bearer token

**Commence par:** `ntn_`

---

### 3. NOTION_PARENT_PAGE_ID

1. Ouvrir Notion
2. Créer une page: "Healthcare Watch"
3. Copier l'URL: `notion.so/workspace/Name-xxxxxxxxxxxxx...`
4. L'ID est la partie longue avant le `?`
5. Enlever les tirets

**Format:** 32 caractères alphanumériques

---

### 4. NOTIFICATION_EMAIL

Juste votre email! Exemple: `votre.email@gmail.com`

---

### 5. SMTP (Email)

#### Si vous utilisez Gmail:

1. Aller à: https://myaccount.google.com/security
2. Activer "2-Step Verification" si pas fait
3. Aller à: https://myaccount.google.com/apppasswords
4. Sélectionner "Mail" + "Windows Computer"
5. Google génère un mot de passe → Copier (16 chars)

Alors:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # Le mot de passe généré
```

#### Si vous utilisez Outlook:

```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=votre@outlook.com
SMTP_PASSWORD=votre_mot_de_passe_outlook
```

---

## ❓ C'est quoi qui se passe?

Quand vous lancez le script:

1. 📦 **Charge la configuration** depuis `prompts.yaml` et `.env`
2. 🔍 **Pour chaque prompt** (ex: daily news, weekly tech):
   - 🤖 Interroge Perplexity AI avec le prompt
   - 📝 Crée une page Notion avec le résultat
   - 📧 Envoie un email récapitulatif
3. ✅ **Affiche un résumé** des exécutions

---

## 🔄 Automatiser avec GitHub Actions

Quand vous êtes prêt:

1. Créer un repository GitHub
2. Ajouter 8 secrets (voir `GITHUB_SECRETS.md`)
3. Push le code
4. **Le workflow s'exécute automatiquement** chaque jour à 08:00 + 16:00 UTC

Voir: `.github/workflows/healthcare-watch.yml`

---

## 🐛 Erreur lors du test?

### `Module not found`
```bash
pip install -r requirements.txt
```

### `PERPLEXITY_API_KEY n'est pas configurée`
Vérifier votre fichier `.env`:
```bash
echo %PERPLEXITY_API_KEY%  # Windows CMD
echo $PERPLEXITY_API_KEY   # Linux/Mac
```

### `parent_page_id non défini`
Ajouter dans `prompts.yaml`:
```yaml
prompts:
  daily_health_news:
    parent_page_id: "xxxxxxxxxxxxx"
```

### Plus d'erreurs?
Voir: `TROUBLESHOOTING.md`

---

## 📚 Documentation

- **QUICKSTART.md** - 5 min start (ultra-basique)
- **README.md** - Guide complet (550+ lignes)
- **INSTALLATION.md** - Installation détaillée
- **TROUBLESHOOTING.md** - Erreurs + FAQ
- **GITHUB_SECRETS.md** - Config GitHub
- **PROJECT_STRUCTURE.md** - Architecture

---

## ✨ Prochaines étapes

Après le premier test réussi:

1. ✅ Personnaliser les prompts dans `prompts.yaml`
2. ✅ Ajouter vos propres prompts
3. ✅ Configurer GitHub Actions pour automatisation
4. ✅ Ajouter d'autres intégrations (Slack, Discord, etc.)

---

## 🎯 Votre checklist

- [ ] Installation (Python + dépendances) ✅
- [ ] Fichier `.env` créé avec 8 secrets
- [ ] Fichier `prompts.yaml` copié depuis template
- [ ] Premier test réussi (pages Notion créées)
- [ ] GitHub Actions configuré (optionnel)
- [ ] Personalisation de vos prompts

---

## 💡 Tips

- 🔄 Le script respecte automatiquement les fréquences (daily, weekly, monthly)
- 📊 Le fichier `data/output/.last_run.json` suivi les exécutions
- 🎚️ Vous pouvez désactiver les notifications dans `prompts.yaml`
- 🔐 Les secrets ne sont JAMAIS commités (`.gitignore` les protège)
- ⚡ Le premier test crée immédiatement les pages Notion

---

## ✅ Vous êtes prêt!

Lancez le script et profitez des newsletters automatisées! 🚀

**Questions?** → Consultez `TROUBLESHOOTING.md`

---

**Version**: 1.0.0  
**Date**: Février 2026
