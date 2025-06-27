# Agent PostgreSQL Web Researcher

## 🔍 Identification

- **Nom**: `agent_POSTGRESQL_web_researcher.py`
- **Type**: Agent spécialisé PostgreSQL - Recherche Web et Documentation
- **Pattern Factory**: ✅ Conforme
- **Statut**: ✅ Harmonisé et Validé

## 📋 Description

L'Agent PostgreSQL Web Researcher est un agent spécialisé dans la recherche automatisée de solutions PostgreSQL et SQLAlchemy en ligne. Il explore GitHub, Stack Overflow, et la documentation officielle pour identifier des solutions aux problèmes rencontrés, puis synthétise les informations trouvées.

## 🎯 Objectifs Principaux

1. **Recherche automatisée** de solutions sur GitHub et Stack Overflow
2. **Analyse de documentation** officielle PostgreSQL et SQLAlchemy
3. **Synthèse intelligente** des solutions trouvées
4. **Génération de rapports** structurés avec solutions classées
5. **Veille technologique** continue sur les problèmes PostgreSQL

## 🛠️ Capacités Techniques

### Types de Tâches Supportées

#### 1. `recherche_github`
- **Description**: Recherche de solutions sur GitHub Issues et Discussions
- **Paramètres**: Aucun paramètre requis (utilise sources prédéfinies)
- **Résultat**: Solutions trouvées avec liens et descriptions

#### 2. `recherche_stackoverflow`
- **Description**: Recherche de solutions sur Stack Overflow
- **Paramètres**: Aucun paramètre requis (utilise requêtes prédéfinies)
- **Résultat**: Questions/réponses pertinentes avec votes et validation

#### 3. `analyse_documentation`
- **Description**: Analyse de la documentation officielle
- **Paramètres**: Aucun paramètre requis
- **Résultat**: Extraits de documentation avec liens officiels

#### 4. `synthese_solutions`
- **Description**: Synthèse des solutions de différentes sources
- **Paramètres**:
  - `github` (optionnel): Résultats de recherche GitHub
  - `stackoverflow` (optionnel): Résultats de Stack Overflow
  - `documentation` (optionnel): Résultats de documentation
- **Résultat**: Synthèse consolidée avec recommandations

#### 5. `generation_rapport`
- **Description**: Génération d'un rapport complet de recherche
- **Paramètres**:
  - `data` (optionnel): Données à inclure dans le rapport
- **Résultat**: Rapport formaté avec chemin du fichier

### Sources de Recherche

#### GitHub Issues
- SQLAlchemy metadata reserved
- PostgreSQL textual SQL expression
- Docker Postgres Windows
- SQLAlchemy 2.0 migration
- psycopg2 Windows installation

#### Stack Overflow
- Attribute name metadata is reserved SQLAlchemy
- Textual SQL expression should be explicitly declared
- PostgreSQL Docker Windows connection
- SQLAlchemy 2.x compatibility issues
- psycopg2 vs psycopg2-binary

#### Documentation Officielle
- SQLAlchemy 2.0 migration guide
- PostgreSQL Docker official
- psycopg2 installation Windows
- Docker Compose PostgreSQL best practices

### Architecture Technique

- **Classe**: `AgentPostgresqlWebResearcher`
- **Héritage**: `AgentPostgreSQLBase`
- **Dépendances**: requests, BeautifulSoup (optionnel)
- **Répertoire des rapports**: `docs/agents_postgresql_resolution/rapports/`
- **Format de sortie**: JSON et Markdown

## 📚 Guide d'Utilisation

### Utilisation Asynchrone (Recommandée)

```python
from agents.agent_POSTGRESQL_web_researcher import AgentPostgresqlWebResearcher
from core.agent_factory_architecture import Task

# Initialisation
agent = AgentPostgresqlWebResearcher()

# Recherche sur GitHub
task = Task(
    type="recherche_github",
    params={}
)
result = await agent.execute_task(task)

# Recherche sur Stack Overflow
task = Task(
    type="recherche_stackoverflow",
    params={}
)
result = await agent.execute_task(task)

# Synthèse des solutions
task = Task(
    type="synthese_solutions",
    params={
        "github": github_results,
        "stackoverflow": so_results,
        "documentation": doc_results
    }
)
result = await agent.execute_task(task)

# Génération de rapport
task = Task(
    type="generation_rapport",
    params={
        "data": synthesized_data
    }
)
result = await agent.execute_task(task)
```

### Tests CLI Recommandés

```bash
# Test de recherche GitHub
python -m agents.agent_POSTGRESQL_web_researcher --task recherche_github

# Test de recherche Stack Overflow
python -m agents.agent_POSTGRESQL_web_researcher --task recherche_stackoverflow

# Test d'analyse de documentation
python -m agents.agent_POSTGRESQL_web_researcher --task analyse_documentation

# Test de génération de rapport
python -m agents.agent_POSTGRESQL_web_researcher --task generation_rapport

# Workflow complet
python -m agents.agent_POSTGRESQL_web_researcher --task synthese_solutions
```

## 📊 Structure des Résultats

### Résultat de Recherche GitHub
```json
{
  "success": true,
  "data": {
    "total_results": 15,
    "sources_searched": [
      "sqlalchemy metadata reserved",
      "postgresql textual sql expression"
    ],
    "solutions": [
      {
        "title": "SQLAlchemy 2.0 metadata fix",
        "url": "https://github.com/sqlalchemy/sqlalchemy/issues/7891",
        "description": "Solution for metadata reserved attribute error",
        "relevance_score": 0.95,
        "last_updated": "2024-01-15"
      }
    ]
  }
}
```

### Résultat de Recherche Stack Overflow
```json
{
  "success": true,
  "data": {
    "total_results": 12,
    "solutions": [
      {
        "title": "Textual SQL expression fix",
        "url": "https://stackoverflow.com/questions/12345678",
        "votes": 45,
        "accepted": true,
        "description": "How to fix textual SQL expression warning",
        "tags": ["sqlalchemy", "postgresql", "python"],
        "relevance_score": 0.92
      }
    ]
  }
}
```

### Résultat de Synthèse
```json
{
  "success": true,
  "data": {
    "total_solutions": 27,
    "categories": {
      "sqlalchemy_migration": 8,
      "docker_postgres": 6,
      "connection_issues": 7,
      "performance": 6
    },
    "top_recommendations": [
      {
        "problem": "SQLAlchemy metadata reserved",
        "solution": "Use Model.__table__.name instead of metadata",
        "confidence": 0.95,
        "sources": ["github", "stackoverflow"]
      }
    ],
    "priority_actions": [
      "Update SQLAlchemy to 2.0+ compatible syntax",
      "Fix Docker Compose PostgreSQL configuration"
    ]
  }
}
```

### Résultat de Génération de Rapport
```json
{
  "success": true,
  "data": {
    "report_path": "docs/agents_postgresql_resolution/rapports/web_researcher_rapport.md",
    "report_generated_at": "2024-01-01T12:00:00",
    "sections": [
      "Executive Summary",
      "GitHub Solutions",
      "Stack Overflow Solutions",
      "Documentation Analysis",
      "Recommendations"
    ],
    "total_pages": 15
  }
}
```

## 🧪 Tests et Validation

### Tests Fonctionnels
- ✅ Recherche automatisée sur GitHub Issues
- ✅ Extraction de solutions Stack Overflow
- ✅ Analyse de documentation officielle
- ✅ Synthèse multi-sources
- ✅ Génération de rapports structurés

### Tests de Robustesse
- ✅ Gestion des timeouts réseau
- ✅ Validation des réponses API
- ✅ Gestion des erreurs de parsing
- ✅ Fallback en cas d'indisponibilité

### Tests de Qualité
- ✅ Filtrage par pertinence
- ✅ Validation des liens et sources
- ✅ Classification automatique des solutions
- ✅ Détection de doublons

## 🏗️ Conformité Pattern Factory

### ✅ Interface Standardisée
- Implémentation de `execute_task(task: Task) -> Result`
- Handlers spécialisés pour chaque source de recherche
- Structure de résultats avec scores de pertinence

### ✅ Gestion des Erreurs
- Validation des réponses réseau
- Gestion des erreurs de parsing HTML/JSON
- Messages d'erreur avec contexte de source

### ✅ Architecture Modulaire
- Héritage de `AgentPostgreSQLBase`
- Séparation par source de recherche
- Méthodes privées pour logique de parsing

### ✅ Performance et Cache
- Gestion des timeouts de requêtes
- Rate limiting pour éviter les blocages
- Cache optionnel des résultats de recherche

## 📈 Statut d'Harmonisation

- **Date de dernière harmonisation**: 2024-12-27
- **Version Pattern Factory**: Conforme v2.0
- **Tests CLI**: ✅ Validés
- **Documentation synchronisée**: ✅ À jour
- **Conformité technique**: ✅ Respectée

## 🔧 Configuration et Personnalisation

### Variables d'Environnement
- `WEB_RESEARCH_TIMEOUT`: Timeout des requêtes (défaut: 30s)
- `WEB_RESEARCH_RATE_LIMIT`: Limite de requêtes par minute (défaut: 30)

### Paramètres de Configuration
- `workspace_root`: Racine du projet
- `rapport_file`: Chemin du fichier de rapport
- `sources_recherche`: Configuration des sources
- `user_agent`: User-Agent pour les requêtes HTTP

### Dépendances Optionnelles
- **requests**: Requêtes HTTP (requis)
- **BeautifulSoup**: Parsing HTML (optionnel, améliore l'extraction)
- **lxml**: Parser XML/HTML performant (optionnel)

## 📝 Notes Techniques

- Respect des rate limits des APIs publiques
- Support des proxies pour entreprises
- Filtrage intelligent par mots-clés PostgreSQL
- Classification automatique par type de problème
- Extraction des métadonnées de qualité (votes, dates)
- Support multi-langue avec priorité anglais
- Génération de rapports en formats multiples
- Integration avec outils de veille technologique
