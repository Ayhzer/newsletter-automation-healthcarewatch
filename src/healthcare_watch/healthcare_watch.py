#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Healthcare Watch - Newsletter d'actualités sanitaires automatisée
Récupère des informations via Perplexity, et crée des pages Notion
"""

import os
import sys
import json
import yaml
import base64
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional
import requests
from notion_client import Client
import time
import pytz
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Force UTF-8 encoding on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ==================== CONSTANTS ====================
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent.parent
CONFIG_DIR = PROJECT_DIR / 'config'
DATA_DIR = PROJECT_DIR / 'data'
OUTPUT_DIR = DATA_DIR / 'output'

# ==================== CONFIGURATION LOADING ====================

def load_config() -> Dict:
    """Charge la configuration YAML et les variables d'environnement"""
    print('Chargement de la configuration...')

    # Charger le fichier YAML
    config_file = CONFIG_DIR / 'prompts.yaml'
    if not config_file.exists():
        config_file = CONFIG_DIR / 'prompts.example.yaml'
        if not config_file.exists():
            raise FileNotFoundError(
                "Fichier config/prompts.yaml non trouvé.\n"
                "Créez-le à partir de config/prompts.example.yaml"
            )
        print(f'ATTENTION: Utilisation de {config_file.name}')

    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Charger les secrets depuis les variables d'environnement
    config['secrets'] = {
        'PERPLEXITY_API_KEY': os.environ.get('PERPLEXITY_API_KEY', ''),
        'NOTION_TOKEN': os.environ.get('NOTION_TOKEN', ''),
        'NOTION_PARENT_PAGE_ID': os.environ.get('NOTION_PARENT_PAGE_ID', ''),
        'NOTIFICATION_EMAIL': os.environ.get('NOTIFICATION_EMAIL', ''),
        'GOOGLE_CREDENTIALS_JSON': os.environ.get('GOOGLE_CREDENTIALS_JSON', ''),
        'GOOGLE_OAUTH_TOKEN_JSON': os.environ.get('GOOGLE_OAUTH_TOKEN_JSON', ''),
    }

    # Valider les secrets requis (Perplexity + Notion minimum)
    required_secrets = ['PERPLEXITY_API_KEY', 'NOTION_TOKEN']
    missing = [s for s in required_secrets if not config['secrets'].get(s)]
    if missing:
        raise ValueError(f"Secrets manquants: {', '.join(missing)}")

    # Vérifier Gmail API seulement si notifications activées
    notifications_enabled = config.get('general', {}).get('notifications', {}).get('enabled', False)
    if notifications_enabled:
        gmail_required = ['NOTIFICATION_EMAIL', 'GOOGLE_CREDENTIALS_JSON', 'GOOGLE_OAUTH_TOKEN_JSON']
        missing_gmail = [s for s in gmail_required if not config['secrets'].get(s)]
        if missing_gmail:
            print(f'ATTENTION: Notifications activées mais secrets Gmail manquants: {", ".join(missing_gmail)}')
            print('Les notifications email seront désactivées.')
            config['general']['notifications']['enabled'] = False

    print('Configuration chargée')
    return config


def should_run_prompt(prompt_key: str, prompt_config: Dict, last_run_file: Path) -> bool:
    """Vérifie si un prompt doit être exécuté selon sa fréquence"""
    if not prompt_config.get('enabled', False):
        return False

    frequency = prompt_config.get('frequency', 'daily')

    # Charger la date de dernière exécution
    run_history = {}
    if last_run_file.exists():
        with open(last_run_file, 'r') as f:
            run_history = json.load(f)

    last_run = run_history.get(prompt_key)
    if not last_run:
        print(f'  Première exécution de {prompt_key}')
        return True

    last_run_date = datetime.fromisoformat(last_run)
    now = datetime.now()
    diff = now - last_run_date
    total_seconds = diff.total_seconds()

    # Vérifier selon la fréquence
    if frequency == 'hourly' and total_seconds >= 3600:
        return True
    elif frequency == 'daily' and total_seconds >= 86400:
        return True
    elif frequency == 'weekly' and total_seconds >= 604800:
        return True
    elif frequency == 'monthly' and diff.days >= 30:
        return True

    return False


def update_last_run(prompt_key: str, last_run_file: Path):
    """Met à jour la date de dernière exécution d'un prompt"""
    run_history = {}
    if last_run_file.exists():
        with open(last_run_file, 'r') as f:
            run_history = json.load(f)

    run_history[prompt_key] = datetime.now().isoformat()

    last_run_file.parent.mkdir(parents=True, exist_ok=True)
    with open(last_run_file, 'w') as f:
        json.dump(run_history, f, indent=2)


# ==================== PERPLEXITY API ====================

def query_perplexity(prompt: str, config: Dict, options: Dict = None) -> str:
    """Interroge l'API Perplexity avec le prompt fourni"""
    api_key = config['secrets']['PERPLEXITY_API_KEY']

    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY n'est pas configurée")

    # Options par défaut
    default_options = {
        'max_tokens': 2000,
        'temperature': 0.3,
        'model': 'sonar'
    }
    if options:
        default_options.update(options)

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'User-Agent': 'HealthcareWatch/1.0'
    }

    payload = {
        'model': default_options['model'],
        'messages': [
            {
                'role': 'system',
                'content': 'Tu es un expert en domaine sanitaire fournissant des informations factuelles et à jour.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'max_tokens': default_options['max_tokens'],
        'temperature': default_options['temperature']
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f'  Appel Perplexity (tentative {attempt + 1}/{max_retries})...')
            response = requests.post(
                'https://api.perplexity.ai/chat/completions',
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 401:
                raise ValueError('Authentification Perplexity échouée (401)')
            elif response.status_code == 429:
                print('  Limite de débit atteinte, attente 30s...')
                time.sleep(30)
                continue
            elif response.status_code >= 500:
                print('  Erreur serveur, nouvelle tentative...')
                time.sleep(5)
                continue
            elif response.status_code != 200:
                raise ValueError(f'Erreur API Perplexity: {response.status_code} - {response.text}')

            data = response.json()
            if 'choices' not in data or not data['choices']:
                raise ValueError('Format de réponse invalide')

            synthesis = data['choices'][0]['message']['content']
            print('  Réponse reçue de Perplexity')
            return synthesis

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            raise TimeoutError('Timeout Perplexity API')
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            raise

    raise Exception('Impossible de contacter Perplexity API après 3 tentatives')


# ==================== NOTION API ====================

def markdown_to_notion_blocks(content: str, timestamp: str) -> list:
    """Convertit du contenu markdown en blocs Notion"""
    blocks = []

    # Bloc date/heure en italique gris
    blocks.append({
        'object': 'block',
        'type': 'paragraph',
        'paragraph': {
            'rich_text': [{
                'type': 'text',
                'text': {'content': f'Généré le {timestamp}'},
                'annotations': {'italic': True, 'color': 'gray'}
            }]
        }
    })

    # Divider
    blocks.append({
        'object': 'block',
        'type': 'divider',
        'divider': {}
    })

    # Parser le contenu ligne par ligne
    lines = content.split('\n')
    current_paragraph = []

    def flush_paragraph():
        """Ajoute le paragraphe accumulé comme bloc"""
        if current_paragraph:
            text = '\n'.join(current_paragraph).strip()
            if text:
                # Notion limite à 2000 caractères par bloc rich_text
                while text:
                    chunk = text[:2000]
                    text = text[2000:]
                    blocks.append({
                        'object': 'block',
                        'type': 'paragraph',
                        'paragraph': {
                            'rich_text': [{
                                'type': 'text',
                                'text': {'content': chunk}
                            }]
                        }
                    })
            current_paragraph.clear()

    for line in lines:
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            continue

        # Heading 1
        if stripped.startswith('# ') and not stripped.startswith('##'):
            flush_paragraph()
            blocks.append({
                'object': 'block',
                'type': 'heading_1',
                'heading_1': {
                    'rich_text': [{
                        'type': 'text',
                        'text': {'content': stripped[2:].strip()[:2000]}
                    }]
                }
            })
        # Heading 2
        elif stripped.startswith('## ') and not stripped.startswith('###'):
            flush_paragraph()
            blocks.append({
                'object': 'block',
                'type': 'heading_2',
                'heading_2': {
                    'rich_text': [{
                        'type': 'text',
                        'text': {'content': stripped[3:].strip()[:2000]}
                    }]
                }
            })
        # Heading 3
        elif stripped.startswith('### '):
            flush_paragraph()
            blocks.append({
                'object': 'block',
                'type': 'heading_3',
                'heading_3': {
                    'rich_text': [{
                        'type': 'text',
                        'text': {'content': stripped[4:].strip()[:2000]}
                    }]
                }
            })
        # Bulleted list item
        elif stripped.startswith('- ') or stripped.startswith('* '):
            flush_paragraph()
            blocks.append({
                'object': 'block',
                'type': 'bulleted_list_item',
                'bulleted_list_item': {
                    'rich_text': [{
                        'type': 'text',
                        'text': {'content': stripped[2:].strip()[:2000]}
                    }]
                }
            })
        # Numbered list item (ex: "1. texte")
        elif len(stripped) > 2 and stripped[0].isdigit() and '. ' in stripped[:5]:
            flush_paragraph()
            text_content = stripped.split('. ', 1)[1] if '. ' in stripped else stripped
            blocks.append({
                'object': 'block',
                'type': 'numbered_list_item',
                'numbered_list_item': {
                    'rich_text': [{
                        'type': 'text',
                        'text': {'content': text_content.strip()[:2000]}
                    }]
                }
            })
        # Ligne horizontale
        elif stripped in ('---', '***', '___'):
            flush_paragraph()
            blocks.append({
                'object': 'block',
                'type': 'divider',
                'divider': {}
            })
        else:
            current_paragraph.append(stripped)

    flush_paragraph()

    # Notion API limite à 100 blocs par appel
    if len(blocks) > 100:
        blocks = blocks[:100]
        print(f'  ATTENTION: Contenu tronqué à 100 blocs (limite Notion API)')

    return blocks


def create_notion_page(title: str, content: str, parent_page_id: str,
                       config: Dict) -> Optional[str]:
    """Crée une page Notion avec le titre et le contenu"""
    print(f'  Création page Notion: {title}')

    notion = Client(auth=config['secrets']['NOTION_TOKEN'])

    # Formater la date/heure avec timezone
    tz = pytz.timezone(config.get('general', {}).get('timezone', 'Europe/Paris'))
    now_tz = datetime.now(tz)
    timestamp = now_tz.strftime('%d %B %Y - %H:%M')

    # Titre avec timestamp
    full_title = f"{title} ({timestamp})"

    # Convertir le contenu en blocs Notion
    blocks = markdown_to_notion_blocks(content, timestamp)

    try:
        response = notion.pages.create(
            parent={'page_id': parent_page_id},
            properties={
                'title': {
                    'title': [{
                        'type': 'text',
                        'text': {'content': full_title}
                    }]
                }
            },
            children=blocks
        )

        page_id = response['id']
        print(f'  Page créée: {page_id}')
        return page_id

    except Exception as e:
        print(f'  ERREUR création Notion: {e}')
        return None


# ==================== GMAIL API ====================

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_gmail_service(config: Dict):
    """Initialise le service Gmail API avec les credentials OAuth2"""
    creds_json = config['secrets']['GOOGLE_CREDENTIALS_JSON']
    token_json = config['secrets']['GOOGLE_OAUTH_TOKEN_JSON']

    if not creds_json or not token_json:
        raise ValueError('Credentials Gmail API manquantes')

    # Charger le token OAuth2 depuis le secret
    token_data = json.loads(token_json)
    creds = Credentials.from_authorized_user_info(token_data, GMAIL_SCOPES)

    # Rafraîchir le token si expiré
    if creds and creds.expired and creds.refresh_token:
        print('  Rafraîchissement du token Gmail...')
        creds.refresh(Request())

    service = build('gmail', 'v1', credentials=creds, cache_discovery=False)
    return service


def send_gmail(service, to_email: str, subject: str, text_body: str, html_body: str) -> bool:
    """Envoie un email via l'API Gmail"""
    msg = MIMEMultipart('alternative')
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
    service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

    return True


# ==================== EMAIL NOTIFICATIONS ====================

def send_notification_email(prompt_key: str, synthesis: str, page_title: str,
                            config: Dict) -> bool:
    """Envoie un email de notification avec le résumé via Gmail API"""

    # Vérifier si les notifications sont activées
    if not config.get('general', {}).get('notifications', {}).get('enabled', False):
        print('  Notifications email désactivées')
        return True

    print('  Envoi de l\'email de notification (Gmail API)...')

    to_email = config['secrets']['NOTIFICATION_EMAIL']
    if not to_email:
        print('  NOTIFICATION_EMAIL non configuré, notification ignorée')
        return False

    try:
        service = get_gmail_service(config)

        subject = f'Healthcare Watch - {page_title}'

        # Contenu texte
        text = f"""Bonjour,

Le rapport "{page_title}" a été généré avec succès et ajouté à Notion.

Synthèse:
{synthesis}

---
Healthcare Watch - Newsletter automatisée
"""

        # Contenu HTML (échappement pour éviter les injections)
        safe_synthesis = synthesis.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html = f"""<html><body>
<h2>Rapport généré avec succès</h2>
<p>Le rapport <strong>{page_title}</strong> a été généré et ajouté à Notion.</p>
<h3>Synthèse:</h3>
<pre style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; white-space: pre-wrap;">{safe_synthesis}</pre>
<hr>
<p style="color: #888; font-size: 0.9em;"><em>Healthcare Watch - Newsletter automatisée</em></p>
</body></html>"""

        send_gmail(service, to_email, subject, text, html)
        print('  Email envoyé via Gmail API')
        return True

    except Exception as e:
        print(f'  ERREUR envoi email: {e}')
        return False


def send_error_email(prompt_key: str, error_msg: str, config: Dict) -> bool:
    """Envoie un email de notification en cas d'erreur via Gmail API"""
    if not config.get('general', {}).get('notifications', {}).get('email_on_error', False):
        return True

    to_email = config['secrets'].get('NOTIFICATION_EMAIL', '')
    if not to_email:
        return False

    try:
        service = get_gmail_service(config)

        subject = f'[ERREUR] Healthcare Watch - {prompt_key}'

        text = f"""Bonjour,

Une erreur s'est produite lors de la génération du rapport "{prompt_key}".

Erreur: {error_msg}

---
Healthcare Watch - Newsletter automatisée
"""

        html = f"""<html><body>
<h2 style="color: #c0392b;">Erreur Healthcare Watch</h2>
<p>Une erreur s'est produite lors de la génération de <strong>{prompt_key}</strong>.</p>
<pre style="background-color: #fdf2f2; padding: 15px; border-radius: 5px;">{error_msg}</pre>
<hr>
<p style="color: #888; font-size: 0.9em;"><em>Healthcare Watch - Newsletter automatisée</em></p>
</body></html>"""

        send_gmail(service, to_email, subject, text, html)
        print(f'  Email d\'erreur envoyé pour {prompt_key}')
        return True
    except Exception:
        return False


# ==================== MAIN ====================

def main():
    """Fonction principale"""
    print('\n' + '=' * 60)
    print('HEALTHCARE WATCH - Newsletter Sanitaire')
    print('=' * 60)
    print(f'Démarrage: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')

    # Créer les répertoires de sortie
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        # Charger la configuration
        config = load_config()

        # Fichier de suivi des exécutions
        last_run_file = OUTPUT_DIR / '.last_run.json'

        # Traiter chaque prompt
        executed_prompts = []
        errors = []

        prompts_config = config.get('prompts', {})
        print(f'{len(prompts_config)} prompt(s) configuré(s)\n')

        for prompt_key, prompt_config in prompts_config.items():
            print(f'\n--- Prompt: {prompt_key} ---')

            try:
                # Vérifier si le prompt doit s'exécuter
                if not should_run_prompt(prompt_key, prompt_config, last_run_file):
                    freq = prompt_config.get('frequency', 'daily')
                    print(f'  Fréquence {freq} non atteinte, skip')
                    continue

                # 1. Interroger Perplexity
                prompt_text = prompt_config.get('prompt', '')
                options = prompt_config.get('options', {})

                synthesis = query_perplexity(prompt_text, config, options)

                # 2. Créer la page Notion
                page_title = prompt_config.get('page_title', f'Rapport {prompt_key}')
                parent_id = prompt_config.get('parent_page_id') or config['secrets'].get('NOTION_PARENT_PAGE_ID')

                if not parent_id:
                    raise ValueError(f'parent_page_id non défini pour {prompt_key}')

                page_id = create_notion_page(page_title, synthesis, parent_id, config)

                if not page_id:
                    raise Exception('Échec de la création de la page Notion')

                # 3. Envoyer email de notification
                send_notification_email(prompt_key, synthesis, page_title, config)

                # 4. Mettre à jour la date d'exécution
                update_last_run(prompt_key, last_run_file)

                executed_prompts.append({
                    'key': prompt_key,
                    'title': page_title,
                    'page_id': page_id,
                    'success': True
                })

                print(f'  {prompt_key} exécuté avec succès')

            except Exception as e:
                error_msg = f'{prompt_key}: {str(e)}'
                print(f'  ERREUR: {error_msg}')
                errors.append(error_msg)
                executed_prompts.append({
                    'key': prompt_key,
                    'success': False,
                    'error': str(e)
                })
                # Envoyer email d'erreur si configuré
                send_error_email(prompt_key, str(e), config)

        # Résumé final
        print('\n' + '=' * 60)
        print('RÉSUMÉ')
        print('=' * 60)
        successes = len([p for p in executed_prompts if p['success']])
        print(f'Exécutions réussies: {successes}')
        print(f'Erreurs: {len(errors)}')

        if errors:
            print('\nErreurs détectées:')
            for error in errors:
                print(f'  - {error}')

        print(f'\nTerminé: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
        print('=' * 60 + '\n')

        return 0 if not errors else 1

    except Exception as e:
        print(f'\nERREUR FATALE: {e}')
        print('=' * 60 + '\n')
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
