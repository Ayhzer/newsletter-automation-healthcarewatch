# 🚀 Pousser vers GitHub

Votre repo git local est prêt! Voici comment le pousser vers GitHub.

## ✅ Statut local

Le repo git a été créé avec:
- ✅ **27 fichiers committes**
- ✅ **4492 lignes de code/documentation**
- ✅ **Commit initial:** Healthcare Watch v1.0

Vérifier:
```bash
cd c:\Users\boudi\newsletterautomation-healthcarewatch
git log
git status
```

## 📍 Étapes pour créer le repo GitHub

### 1️⃣ Créer le repository sur GitHub

1. Aller à: https://github.com/new
2. Remplir:
   - **Repository name**: `newsletter-automation-healthcarewatch`
   - **Description**: "Healthcare Watch - Newsletter automatisée avec Perplexity et Notion"
   - **Visibility**: Public (ou Private)
   - **Initialize**: Ne rien initialiser (on a déjà un repo local)
3. Cliquer **Create repository**

### 2️⃣ Copier l'URL du repo

Après création, vous verrez une page avec:
```
git remote add origin https://github.com/VOTRE_USERNAME/newsletter-automation-healthcarewatch.git
```

Remplacer `VOTRE_USERNAME` par votre nom GitHub.

### 3️⃣ Pousser vers GitHub

```bash
cd c:\Users\boudi\newsletterautomation-healthcarewatch

# Ajouter le remote
git remote add origin https://github.com/VOTRE_USERNAME/newsletter-automation-healthcarewatch.git

# Vérifier
git remote -v

# Pousser (branche main)
git branch -M main
git push -u origin main
```

### 4️⃣ Ajouter les secrets GitHub (pour Actions)

1. Aller à: `https://github.com/VOTRE_USERNAME/newsletter-automation-healthcarewatch`
2. **Settings → Secrets and variables → Actions**
3. Ajouter 8 secrets (voir GITHUB_SECRETS.md)

### 5️⃣ Vérifier sur GitHub

1. Rafraîchir la page
2. Vous verrez tous vos fichiers
3. Workflow doit être visible dans l'onglet "Actions"

## 🔧 Commandes rapides

```bash
# Initialisation (déjà fait)
cd c:\Users\boudi\newsletterautomation-healthcarewatch
git init

# Ajouter remote
git remote add origin https://github.com/VOTRE_USERNAME/newsletter-automation-healthcarewatch.git

# Vérifier
git remote -v

# Pousser
git branch -M main
git push -u origin main
```

## 📝 Pour les futurs commits

Après modifications:

```bash
# Ajouter les changements
git add .

# Commit
git commit -m "Description de la modification"

# Pousser
git push
```

## 🔐 Secrets à ajouter dans GitHub

### Settings → Secrets and variables → Actions

1. `PERPLEXITY_API_KEY`
2. `NOTION_TOKEN`
3. `NOTION_PARENT_PAGE_ID`
4. `NOTIFICATION_EMAIL`
5. `SMTP_SERVER`
6. `SMTP_PORT`
7. `SMTP_USERNAME`
8. `SMTP_PASSWORD`

(Voir GITHUB_SECRETS.md pour les détails)

## ✅ Checklist

- [ ] Repo créé sur https://github.com/new
- [ ] URL du repo copiée
- [ ] Commande `git remote add origin` exécutée
- [ ] `git push -u origin main` exécuté
- [ ] Fichiers visibles sur GitHub
- [ ] 8 secrets ajoutés dans GitHub
- [ ] Workflow visible dans Actions
- [ ] Première exécution planifiée

## 📞 Troubleshooting

### Erreur: "fatal: 'origin' does not appear to be a 'git' repository"

```bash
# Vérifier le remote
git remote -v

# Ajouter si manquant
git remote add origin https://github.com/VOTRE_USERNAME/REPO_NAME.git
```

### Erreur: "fatal: could not read Username"

Configurer Git avec token:
```bash
git config credential.helper store
git push  # Sera demandé de fournir token
```

### Repo déjà créé?

```bash
# Lister les remotes
git remote -v

# Changer le remote
git remote set-url origin https://github.com/VOTRE_USERNAME/REPO_NAME.git
```

## 🎉 C'est fait!

Une fois pushé, votre projet sera visible sur GitHub avec:
- ✅ Tous les fichiers source
- ✅ Documentation complète
- ✅ GitHub Actions workflow
- ✅ Historique git
- ✅ Contributions possibles

---

**Prochaine étape:** Ajouter les 8 secrets et tester le workflow!

Voir: GITHUB_SECRETS.md
