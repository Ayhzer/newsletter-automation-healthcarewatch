# Guide des Prompts - Healthcare Watch

Comment créer et personnaliser vos prompts Perplexity.

## 📖 Comprendre les prompts

Un "prompt" est une instruction textuelle envoyée à Perplexity AI pour obtenir une synthèse.

## 🎯 Anatomie d'un bon prompt

### Structure recommandée:

```
Tu es expert en [DOMAINE].

Synthétise/Crée/Compile [SUJET] avec:

1. [Point 1 important]
2. [Point 2 important]
3. [Point 3 important]
...

Format: [Exigence sur la structure]
```

### Exemple réel dans prompts.yaml:

```yaml
daily_health_news:
  frequency: "daily"
  prompt: |
    Tu es expert en santé publique et médecine générale.
    
    Synthétise les dernières actualités médicales et de santé publique avec:
    
    ## STRUCTURE DEMANDÉE:
    1. **Top 5 actualités du jour** avec sources
    2. **Tendances santé émergentes** (changements identifiés)
    3. **Statistiques ou données clés**
    4. **Impact sur professionnels de santé**
    5. **Recommandations officielles** (OMS, HAS)
    
    Sois factuel, cite sources, et rends accessible.
```

## ✍️ Comment écrire un prompt efficace

### ✅ DO's (à faire)

1. **Être spécifique**
   ```
   ✅ BON:  "Synthétise les études sur l'IA en médecine"
   ❌ MAUVAIS: "Parle-moi de trucs médicaux"
   ```

2. **Définir le domaine d'expertise**
   ```
   ✅ "Tu es expert en [cardiologie/IA/santé publique]"
   ```

3. **Lister les sections souhaitées**
   ```
   ✅ "Avec: 1) Section A 2) Section B 3) Section C"
   ```

4. **Préciser le format/ton**
   ```
   ✅ "Sois concis/détaillé/factuel/accessible"
   ```

5. **Donner un contexte**
   ```
   ✅ "Pour un professionnel de santé / un patient / un chercheur"
   ```

### ❌ DON'Ts (à éviter)

1. **Être trop vague**
   ```
   ❌ "Parle de santé"
   ✅ "Synthétise les tendances santé du secteur pharmaceutique"
   ```

2. **Demander trop**
   ```
   ❌ Prompt de 50 pages
   ✅ Limiter à 2000-3000 mots de sortie (max_tokens)
   ```

3. **Demandes conflictuelles**
   ```
   ❌ "Sois très bref ET hyper détaillé"
   ✅ Choisir: bref (1000 tokens) ou détaillé (3000 tokens)
   ```

## 📋 Templates pour différents usages

### 1. Newsletter actualités

```yaml
daily_health_news:
  enabled: true
  frequency: "daily"
  page_title: "Actualités Santé - Daily"
  prompt: |
    Tu es expert en [DOMAINE SANITAIRE - ex: cardiologie, oncologie, etc.].
    
    Synthétise les DERNIÈRES ACTUALITÉS du jour avec:
    
    1. **Top 5 actualités** avec sources
    2. **Nouvelles découvertes scientifiques**
    3. **Changements réglementaires**
    4. **Cas d'usage pratiques**
    5. **Impact clinique/pratique**
    
    Format: Clair, facile à scanner, avec bullets.
```

### 2. Veille technologique

```yaml
weekly_health_tech:
  enabled: true
  frequency: "weekly"
  page_title: "Tech Santé - Hebdomadaire"
  prompt: |
    Tu es expert en digital health et technologie médicale.
    
    Compile une veille technologique hebdomadaire avec:
    
    1. **Technologies émergentes** (IA, blockchain, IoT, télémédecine)
    2. **Startups santé** - Nouveaux financement et levées de fonds
    3. **Cybersécurité médicale** - Violations et solutions
    4. **Conformité IT** - RGPD, normes, réglementations
    5. **Implémentations réussies** - Cas d'usage concrets
    
    Sois détaillé, cite sources, oriente vers applications pratiques.
```

### 3. Synthèse recherche

```yaml
monthly_research:
  enabled: true
  frequency: "monthly"
  page_title: "Recherche Clinique - Mensuel"
  prompt: |
    Tu es expert en recherche clinique et médecine factuelle.
    
    Synthétise les études cliniques importantes du mois avec:
    
    1. **Études marquantes** (nouvelles découvertes)
    2. **Méta-analyses et revues systématiques**
    3. **Essais cliniques** en cours (phases I-IV)
    4. **Implications pratiques** pour la clinique
    5. **Publications autorités** (EMA, FDA, HAS)
    
    Inclus: Niveau de preuve, population, résultats clés.
```

### 4. Recommandations officielles

```yaml
official_guidelines:
  enabled: true
  frequency: "monthly"
  page_title: "Recommandations Officielles"
  prompt: |
    Tu es expert en médecine et en lignes directrices cliniques.
    
    Synthétise les NOUVELLES RECOMMANDATIONS du mois de:
    
    1. **Organisations officielles** (OMS, HAS, EMA, CDC)
    2. **Sociétés savantes** (cardiologie, oncologie, etc.)
    3. **Agences gouvernementales** sanitaires
    4. **Changements majeurs** par rapport aux versions précédentes
    5. **Impact sur pratique clinique**
    
    Format: Concis, orienté action, avec liens si possible.
```

### 5. Analyse de marché

```yaml
market_analysis:
  enabled: true
  frequency: "weekly"
  page_title: "Marché Santé - Analyse"
  prompt: |
    Tu es expert en économie de la santé et business healthcare.
    
    Analyse le marché santé cette semaine avec:
    
    1. **Fusions et acquisitions** (M&A)
    2. **Financements** (rounds, IPO, levées)
    3. **Tendances marché** (croissance, consolidation)
    4. **Réglementation commerciale** changements
    5. **Opportunités d'affaires**
    
    Sois analytique, chiffré, orienté business.
```

## ⚙️ Options d'optimisation

Chaque prompt peut avoir des options:

```yaml
prompts:
  mon_prompt:
    prompt: "..."
    options:
      max_tokens: 2000      # Longueur réponse (1000-4000)
      temperature: 0.3      # 0.0=déterministe, 1.0=créatif
      model: "sonar"        # Modèle Perplexity
```

### Recommandations par type:

| Type | max_tokens | temperature | Expliqué |
|------|-----------|------------|----------|
| Actualités | 2000 | 0.3 | Factuels, peu créatifs |
| Analyse | 2500 | 0.4 | Analytique, un peu flexible |
| Recherche | 3000 | 0.2 | Très factuels, très spécifiques |
| Créatif | 1500 | 0.7 | Plus de liberté |

## 🎯 Exemples concrets

### Avant/Après: Prompt faible → Fort

**❌ Faible:**
```yaml
prompt: |
  Synthétise les infos sur le cancer
```

**✅ Fort:**
```yaml
prompt: |
  Tu es expert en oncologie et en médecine factuelle.
  
  Synthétise les avancées en TRAITEMENT DU CANCER ce mois avec:
  
  1. **Nouvelles thérapies approuvées** (immunothérapie, ARN)
  2. **Résultats d'essais cliniques majeurs**
  3. **Biomarqueurs et diagnostics innovants**
  4. **Impact sur options thérapeutiques** actuelles
  5. **Recommandations mises à jour**
  
  Format: Technique mais accessible, avec niveaux de preuve.
```

## 🔄 Tester et affiner

### 1. Premier test

Lancez avec un prompt simple:
```bash
python healthcare_watch.py
```

### 2. Vérifier le résultat

- Ouvrir la page Notion créée
- Juger la qualité/pertinence
- Noter ce qui manque

### 3. Améliorer

Ajuster dans `prompts.yaml`:
- Ajouter sections manquantes
- Préciser le domaine
- Modifier tone/format

### 4. Relancer

```bash
python healthcare_watch.py
```

## 🌍 Exemples sectoriels

### Cardiologie

```yaml
prompt: |
  Tu es cardiologue et expert en médecine basée sur preuves.
  
  Synthétise les avancées en CARDIOLOGIE avec:
  1. Insuffisance cardiaque - nouveaux traitements
  2. Hypertension - guidelines mises à jour
  3. Arythmies - innovations diagnostiques
  4. Prévention cardiovasculaire
  5. Impact sur pratique clinique quotidienne
```

### Diabétologie

```yaml
prompt: |
  Tu es diabétologue et expert en endocrinologie.
  
  Synthétise les actualités DIABÈTE avec:
  1. Diabète type 1 - innovations insuline
  2. Diabète type 2 - nouveaux agents
  3. Comorbidités - complications
  4. Dépistage et prévention
  5. Changements en recommandations
```

### Pédiatrie

```yaml
prompt: |
  Tu es pédiatre et expert en santé de l'enfant.
  
  Synthétise les actualités PÉDIATRIE avec:
  1. Vaccinations - calendrier mis à jour
  2. Maladies infectieuses émergentes
  3. Développement et neurodéveloppement
  4. Santé mentale enfant/ado
  5. Changements en recommandations
```

## 💡 Tips pour meilleurs résultats

1. **Être très spécifique sur le domaine**
   - ✅ "Synthétise pour un cardiologue" vs ❌ "parle de santé"

2. **Demander un format structuré**
   - ✅ "Avec sections: 1) ... 2) ... 3)" vs ❌ "écris un truc"

3. **Ajouter des contraintes utiles**
   - ✅ "Moins de 3000 tokens" vs ❌ "Écris tout"
   - ✅ "Cite tes sources" vs ❌ "dit ce que tu veux"

4. **Tester différentes températures**
   - 0.2 = très factuel (données, études)
   - 0.5 = équilibré (analyse + synthèse)
   - 0.8 = plus créatif (brainstorm, idées)

5. **Itérer rapidement**
   - Tester → Vérifier → Ajuster → Retester

## 📝 Template pour créer votre prompt

```yaml
prompts:
  mon_prompt_custom:
    enabled: true
    frequency: "daily"              # ou weekly, monthly
    page_title: "Titre de ma page"
    parent_page_id: ""              # Optionnel
    
    prompt: |
      Tu es expert en [DOMAINE - être précis].
      
      [ACTION: Synthétise/Compile/Analyse] [SUJET] avec:
      
      1. [Section 1 spécifique]
      2. [Section 2 spécifique]
      3. [Section 3 spécifique]
      4. [Section 4 spécifique]
      5. [Section 5 spécifique]
      
      Format: [Exigences sur la structure, ton, niveau de détail]
      Cible: [Audience - ex: professionnel santé, patient, chercheur]
    
    options:
      max_tokens: 2000              # Ajuster selon besoin
      temperature: 0.3              # 0.2-0.5 pour actualités
      model: "sonar"                # Garder sonar
```

## ✅ Checklist avant production

- [ ] Prompt spécifique et clair
- [ ] Domaine d'expertise défini
- [ ] Sections/format explicite
- [ ] max_tokens adapté (1000-4000)
- [ ] temperature appropriée (0.2-0.7)
- [ ] Testé une fois avec `python healthcare_watch.py`
- [ ] Résultat Notion satisfaisant
- [ ] Email reçu comme prévu

---

**Besoin d'aide?** Voir `TROUBLESHOOTING.md`

**Version**: 1.0.0  
**Date**: Février 2026
