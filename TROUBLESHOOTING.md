# Troubleshooting & FAQ

Guide de dépannage et questions fréquentes pour Healthcare Watch.

## 🚨 Erreurs courantes

### 1. `ModuleNotFoundError: No module named 'yaml'`

**Symptôme:**
```
ModuleNotFoundError: No module named 'yaml'
```

**Solution:**
```bash
pip install pyyaml
```

---

### 2. `PERPLEXITY_API_KEY n'est pas configurée`

**Symptôme:**
```
ValueError: PERPLEXITY_API_KEY n'est pas configurée
```

**Causes possibles:**
1. Variable d'env non définie
2. Fichier .env non chargé
3. Clé API vide

**Solutions:**
```bash
# Vérifier la variable
echo $PERPLEXITY_API_KEY  # Linux/Mac
echo %PERPLEXITY_API_KEY%  # Windows CMD

# Charger depuis .env
source .env  # Linux/Mac
# Windows: créer et exécuter load_env.ps1
```

---

### 3. `Authentification Notion échouée (401)`

**Symptôme:**
```
ValueError: Authentification Notion échouée (401)
```

**Solutions:**
1. Vérifier le token:
   ```bash
   echo $NOTION_TOKEN
   ```
2. Token expiré? → Générer nouveau sur https://www.notion.so/my-integrations
3. Page protégée? → Vérifier dans Notion que l'intégration a accès

**Dans Notion:**
1. Ouvrir la page parent
2. Cliquer `...` → `Connections`
3. Vérifier que "Healthcare Watch" est listé
4. Ajouter si nécessaire

---

### 4. `parent_page_id non défini`

**Symptôme:**
```
ValueError: parent_page_id non défini pour daily_health_news
```

**Solutions:**
1. Ajouter à chaque prompt dans `prompts.yaml`:
   ```yaml
   prompts:
     daily_health_news:
       parent_page_id: "xxxxxxxxxxxxx"
   ```
2. Ou définir en variable d'env:
   ```bash
   NOTION_PARENT_PAGE_ID=xxxxxxxxxxxxx
   ```

---

### 5. `Erreur SMTP: Authentification échouée`

**Symptôme:**
```
SMTPAuthenticationError: (535, b'5.7.8 Username and password not accepted')
```

**Pour Gmail:**
1. Vérifier 2FA activée: https://myaccount.google.com/security
2. Générer App password: https://myaccount.google.com/apppasswords
3. ⚠️ Utiliser l'app password (16 chars), PAS le mot de passe du compte
4. SMTP_PASSWORD doit être exactement le app password généré

**Pour Outlook:**
```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_PASSWORD=votre_mot_de_passe_compte
```

---

### 6. `Timeout: Perplexity API`

**Symptôme:**
```
TimeoutError: Timeout Perplexity API
```

**Solutions:**
1. Vérifier la connexion internet
2. Réduire `max_tokens` dans prompts.yaml:
   ```yaml
   options:
     max_tokens: 1000  # Au lieu de 2000
   ```
3. Vérifier status Perplexity: https://perplexity.statuspage.io

---

### 7. `Limite de débit atteinte (429)`

**Symptôme:**
```
⏳ Limite de débit atteinte, attente 30s...
```

**Cause:** Trop d'appels API à Perplexity en peu de temps

**Solutions:**
1. Espacer les exécutions (moins de prompts horaires)
2. Augmenter `max_retries` dans le code
3. Upgrades votre plan Perplexity

---

## ❓ FAQ

### Q: Comment changer l'horaire d'exécution?

**GitHub Actions:**
Éditer `.github/workflows/healthcare-watch.yml`:
```yaml
schedule:
  - cron: '30 8 * * *'  # 08:30 UTC chaque jour
```

**Localement:**
Ajouter un cron job:
```bash
# Linux/Mac
crontab -e
# 08:00 tous les jours
0 8 * * * cd /path/to/healthcare-watch && python src/healthcare_watch/healthcare_watch.py

# Windows
# Utiliser Task Scheduler (GUI)
# Ou: schtasks /create /tn "HealthcareWatch" /tr "python C:\path\healthcare_watch.py" /sc daily /st 08:00
```

---

### Q: Comment ajouter un nouveau prompt?

**Dans prompts.yaml:**
```yaml
prompts:
  mon_nouveau_prompt:
    enabled: true
    frequency: "daily"
    page_title: "Mon Rapport"
    parent_page_id: "xxxxx"
    prompt: |
      Tu es expert en...
      Crée une synthèse avec...
    options:
      max_tokens: 2000
      temperature: 0.3
```

Puis relancer le script.

---

### Q: Comment désactiver les notifications?

**Globalement (dans prompts.yaml):**
```yaml
general:
  notifications:
    enabled: false
```

**Pour un prompt spécifique:**
Ne pas définir `SMTP_*` variables d'env.

---

### Q: Où sont stockées les synthèses?

Les synthèses sont créées dans Notion. Les fichiers locaux (optionnel) seraient dans `data/output/`.

Pour sauvegarder localement, modifier le script pour ajouter:
```python
with open(f'data/output/{prompt_key}_{datetime.now().isoformat()}.txt', 'w') as f:
    f.write(synthesis)
```

---

### Q: Comment utiliser plusieurs pages Notion?

Définir `parent_page_id` différent pour chaque prompt:
```yaml
prompts:
  daily_news:
    parent_page_id: "xxxx1111"
  
  weekly_tech:
    parent_page_id: "xxxx2222"
```

---

### Q: Peut-on exécuter sans GitHub Actions?

**Oui**, plusieurs options:

1. **Cron local (Linux/Mac):**
   ```bash
   0 8 * * * cd /path && python src/healthcare_watch/healthcare_watch.py
   ```

2. **Task Scheduler (Windows)**
   GUI: Control Panel → Task Scheduler

3. **Cloud functions (AWS Lambda, Google Cloud):**
   Déployer le script comme fonction serverless

4. **Docker:**
   ```dockerfile
   FROM python:3.11
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   CMD ["python", "src/healthcare_watch/healthcare_watch.py"]
   ```

---

### Q: Peut-on intégrer Slack/Discord?

**Oui**, ajouter après `create_notion_page()`:

```python
# Slack webhook
import requests
webhook = os.environ.get('SLACK_WEBHOOK')
if webhook:
    requests.post(webhook, json={
        "text": f"✅ {prompt_key} généré: {synthesis[:200]}..."
    })
```

---

### Q: Comment archiver les anciennes pages?

Notion ne supporte pas l'archivage automatique. Options:

1. **Manuellement:** Notion UI → Archive
2. **Avec script:** Utiliser l'API Notion pour archiver
3. **Database Notion:** Créer un système de tags/dates pour filtrer

---

## 🔍 Débogage avancé

### Ajouter du logging verbose

Modifier `healthcare_watch.py` pour déboguer:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Dans les fonctions:
logger.debug(f"Interrogation Perplexity avec: {prompt_text[:100]}...")
```

### Tester la connexion Perplexity

```bash
python -c "
import requests
api_key = 'votre_clé'
headers = {'Authorization': f'Bearer {api_key}'}
response = requests.post('https://api.perplexity.ai/chat/completions',
    headers=headers,
    json={'model': 'sonar', 'messages': [{'role': 'user', 'content': 'Hello'}]},
    timeout=10)
print(f'Status: {response.status_code}')
print(f'Response: {response.json()}')
"
```

### Tester la connexion Notion

```bash
python -c "
from notion_client import Client
token = 'votre_token'
client = Client(auth=token)
try:
    users = client.users.list()
    print('✅ Notion connexion OK')
except Exception as e:
    print(f'❌ Erreur: {e}')
"
```

### Tester la connexion SMTP

```bash
python -c "
import smtplib
server = 'smtp.gmail.com'
port = 587
user = 'votre@gmail.com'
password = 'votre_app_password'

try:
    smtp = smtplib.SMTP(server, port)
    smtp.starttls()
    smtp.login(user, password)
    print('✅ SMTP connexion OK')
    smtp.quit()
except Exception as e:
    print(f'❌ Erreur: {e}')
"
```

---

## 📞 Besoin d'aide?

1. Vérifier cette page FAQ
2. Consulter les logs GitHub Actions
3. Créer une issue sur GitHub
4. Vérifier le status des services externes

---

**Dernière mise à jour**: Janvier 2024
