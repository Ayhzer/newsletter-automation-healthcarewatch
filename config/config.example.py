"""
Configuration pour Healthcare Watch (développement local)

⚠️ ATTENTION: Ce fichier est OBSOLÈTE et n'est plus utilisé par l'application.
L'application utilise maintenant les variables d'environnement (.env) et le fichier prompts.yaml.

Voir:
- .env.example pour les variables d'environnement
- config/prompts.example.yaml pour la configuration des prompts

Ce fichier est conservé uniquement pour référence historique.
"""

# OBSOLÈTE - NE PLUS UTILISER
CONFIG = {
    # Perplexity AI API
    "PERPLEXITY_API_KEY": "pplx-xxxxxxxxxxxxxxxxxxxxx",

    # Notion API
    "NOTION_TOKEN": "ntn_xxxxxxxxxxxxxxxxxxxxx",
    "NOTION_PARENT_PAGE_ID": "xxxxxxxxxxxxxxxxxxxxx",

    # Email de notification (Gmail)
    "NOTIFICATION_EMAIL": "votre.email@gmail.com",

    # Gmail API (OAuth2) - Remplace SMTP
    "GOOGLE_CREDENTIALS_JSON": '{"installed":{"client_id":"...","client_secret":"...",...}}',
    "GOOGLE_OAUTH_TOKEN_JSON": '{"token":"...","refresh_token":"...","client_id":"...",...}',
}
