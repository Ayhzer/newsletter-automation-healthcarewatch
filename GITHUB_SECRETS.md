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

L'email Gmail pour recevoir les notifications.

### 5. GOOGLE_CREDENTIALS_JSON

```
Nom: GOOGLE_CREDENTIALS_JSON
Valeur: {"installed":{"client_id":"...","project_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","client_secret":"...",...}}
```

⚠️ **Configuration:**
1. Créer un projet dans Google Cloud Console: https://console.cloud.google.com/
2. Activer Gmail API
3. Créer des credentials OAuth 2.0 (type "Desktop app")
4. Télécharger `credentials.json`
5. Copier **tout le contenu JSON** du fichier dans ce secret

### 6. GOOGLE_OAUTH_TOKEN_JSON

```
Nom: GOOGLE_OAUTH_TOKEN_JSON
Valeur: {"token":"...","refresh_token":"...","token_uri":"https://oauth2.googleapis.com/token","client_id":"...","client_secret":"...","scopes":["https://www.googleapis.com/auth/gmail.send"],...}
```

⚠️ **Configuration:**
1. Après avoir configuré credentials.json, exécuter un script d'autorisation OAuth2
2. Un navigateur s'ouvrira pour autoriser l'application
3. Le fichier `token.json` sera généré
4. Copier **tout le contenu JSON** du fichier dans ce secret

**Note**: Le token contient un `refresh_token` qui permet de renouveler automatiquement l'accès.

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
- Pour Gmail API: Vérifier que les JSON sont complets et valides
- Vérifier que Gmail API est activée dans Google Cloud Console
- Vérifier que le token OAuth2 contient un refresh_token

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
