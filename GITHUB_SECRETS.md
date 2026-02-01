# Configuration GitHub Secrets

Guide pour configurer les secrets sur GitHub Actions.

## 📍 Où ajouter les secrets?

1. Aller au repository
2. **Settings → Secrets and variables → Actions**
3. Cliquer **New repository secret**

## 🔐 Secrets à ajouter

Ajouter ces secrets un par un:

### 1. PERPLEXITY_API_KEY

```
Nom: PERPLEXITY_API_KEY
Valeur: pplx-xxxxxxxxxxxxxxxxxxxxxxxx
```

Source: https://www.perplexity.ai/ (Settings → API)

### 2. NOTION_TOKEN

```
Nom: NOTION_TOKEN
Valeur: ntn_xxxxxxxxxxxxxxxxxxxxxxxx
```

Source: https://www.notion.so/my-integrations (Bearer token)

### 3. NOTION_PARENT_PAGE_ID

```
Nom: NOTION_PARENT_PAGE_ID
Valeur: xxxxxxxxxxxxxxxxxxxxx
```

Format: 32 caractères alphanumériques (sans tirets)

### 4. NOTIFICATION_EMAIL

```
Nom: NOTIFICATION_EMAIL
Valeur: votre.email@gmail.com
```

L'email pour recevoir les notifications.

### 5. SMTP_SERVER

```
Nom: SMTP_SERVER
Valeur: smtp.gmail.com
```

Pour Gmail: `smtp.gmail.com`
Pour Outlook: `smtp-mail.outlook.com`

### 6. SMTP_PORT

```
Nom: SMTP_PORT
Valeur: 587
```

Port SMTP standard: `587`

### 7. SMTP_USERNAME

```
Nom: SMTP_USERNAME
Valeur: votre.email@gmail.com
```

Doit correspondre à `NOTIFICATION_EMAIL`.

### 8. SMTP_PASSWORD

```
Nom: SMTP_PASSWORD
Valeur: xxxx xxxx xxxx xxxx
```

⚠️ **IMPORTANT pour Gmail:**
- Générer un "App password": https://myaccount.google.com/apppasswords
- Copier le mot de passe généré (16 caractères)
- **NE PAS** utiliser votre mot de passe de compte

## ✅ Vérifier les secrets

Après ajout:

1. Aller à **Settings → Secrets and variables → Actions**
2. Vous devriez voir tous les secrets listés
3. Cliquer sur un secret pour voir qu'il est bien configuré

## 🚀 Test du workflow

Après configuration:

1. Aller à **Actions**
2. Cliquer sur **Healthcare Watch** workflow
3. Cliquer **Run workflow → Run workflow**
4. Attendre quelques secondes (vérifier les logs)
5. Vérifier dans Notion si une page a été créée

## 🔄 Horaires automatiques

Le workflow s'exécute:
- ⏰ Chaque jour à 08:00 UTC (10:00 CET)
- ⏰ Chaque jour à 16:00 UTC (18:00 CET)

Pour modifier les horaires, éditer `.github/workflows/healthcare-watch.yml`

## 🐛 Dépannage

### Erreur: "Secret not found"

- Vérifier que le secret est bien listé dans Settings
- Vérifier l'orthographe du nom (case-sensitive)

### Erreur: "Authentification failed"

- Vérifier la valeur du secret
- Copier-coller depuis la source (pas de caractères cachés)
- Pour Gmail: Vérifier que l'App password est utilisé

### Workflow ne s'exécute pas

- Vérifier que `.github/workflows/healthcare-watch.yml` existe
- Vérifier que tous les secrets sont configurés
- Aller à Actions pour voir les logs d'erreur

## 📝 Notes de sécurité

- ✅ Les secrets sont chiffrés par GitHub
- ✅ Ils ne sont pas visibles dans les logs
- ✅ Ils ne sont pas affichés dans la sortie du workflow
- ✅ Vous pouvez les révoquer à tout moment
- ⚠️ Les secrets ne sont accessibles que à votre repo

## 🔑 Révoquer un secret

Si un secret est compromis:

1. Aller à **Settings → Secrets and variables → Actions**
2. Cliquer sur le secret problématique
3. Cliquer **Delete**
4. Générer une nouvelle clé (ex: new API key dans Perplexity)
5. Ajouter le nouveau secret

---

**Tout est configuré?** → Le workflow s'exécutera selon l'horaire défini!
