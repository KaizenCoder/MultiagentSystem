# Agent PostgreSQL SQLAlchemy Fixer

## 🔍 Identification

- **Nom**: `agent_POSTGRESQL_sqlalchemy_fixer.py`
- **Type**: Agent spécialisé PostgreSQL - Correction SQLAlchemy/ORM
- **Pattern Factory**: ✅ Conforme
- **Statut**: ✅ Harmonisé et Validé

## 📋 Description

L'Agent PostgreSQL SQLAlchemy Fixer est un agent spécialisé dans la résolution des problèmes liés à SQLAlchemy et aux ORM avec PostgreSQL. Il diagnostique les erreurs de modèles, corrige les problèmes de métadonnées, optimise les requêtes et valide les corrections apportées.

## 🎯 Objectifs Principaux

1. **Diagnostic complet** des problèmes SQLAlchemy/PostgreSQL
2. **Correction automatique** des modèles et mappings ORM
3. **Résolution des conflits** de métadonnées
4. **Optimisation des requêtes** pour performance
5. **Validation systématique** des corrections

## 🛠️ Capacités Techniques

### Types de Tâches Supportées

#### 1. `diagnose_sqlalchemy`
- **Description**: Diagnostic complet des problèmes SQLAlchemy
- **Paramètres**:
  - `models_path` (requis): Chemin vers les fichiers de modèles
- **Résultat**: Rapport de diagnostic avec erreurs identifiées

#### 2. `fix_models`
- **Description**: Correction automatique des modèles SQLAlchemy
- **Paramètres**:
  - `models_path` (requis): Chemin vers les modèles à corriger
- **Résultat**: Rapport des corrections appliquées

#### 3. `resolve_metadata`
- **Description**: Résolution des conflits de métadonnées
- **Paramètres**:
  - `metadata_path` (requis): Chemin vers les fichiers de métadonnées
- **Résultat**: Rapport de résolution des métadonnées

#### 4. `optimize_queries`
- **Description**: Optimisation des requêtes SQLAlchemy
- **Paramètres**:
  - `queries_path` (requis): Chemin vers les fichiers de requêtes
- **Résultat**: Rapport d'optimisation avec métriques

#### 5. `validate_fixes`
- **Description**: Validation des corrections apportées
- **Paramètres**:
  - `fix_id` (requis): Identifiant de la correction à valider
- **Résultat**: Rapport de validation avec tests

### Problèmes Traités Spécifiquement

- **Erreurs de mapping** : Relations incorrectes, clés étrangères
- **Problèmes de métadonnées** : Conflits de schéma, tables dupliquées
- **Erreurs de requêtes** : Jointures inefficaces, N+1 queries
- **Problèmes de sessions** : Gestion des connexions, timeouts
- **Incompatibilités de versions** : SQLAlchemy/PostgreSQL

### Architecture Technique

- **Classe**: `AgentPostgresqlSQLAlchemyFixer`
- **Héritage**: `AgentPostgreSQLBase`
- **Répertoire de travail**: `fixes/sqlalchemy/`
- **Support des versions**: SQLAlchemy 1.4+ et 2.0+
- **Compatibilité PostgreSQL**: 12, 13, 14, 15, 16

## 📚 Guide d'Utilisation

### Utilisation Asynchrone (Recommandée)

```python
from agents.agent_POSTGRESQL_sqlalchemy_fixer import AgentPostgresqlSQLAlchemyFixer
from core.agent_factory_architecture import Task

# Initialisation
agent = AgentPostgresqlSQLAlchemyFixer()

# Diagnostic des modèles
task = Task(
    type="diagnose_sqlalchemy",
    params={
        "models_path": "src/models/"
    }
)
result = await agent.execute_task(task)

# Correction des modèles
task = Task(
    type="fix_models",
    params={
        "models_path": "src/models/user.py"
    }
)
result = await agent.execute_task(task)

# Optimisation des requêtes
task = Task(
    type="optimize_queries",
    params={
        "queries_path": "src/queries/"
    }
)
result = await agent.execute_task(task)

# Validation des corrections
task = Task(
    type="validate_fixes",
    params={
        "fix_id": "FIX_MODEL_001"
    }
)
result = await agent.execute_task(task)
```

### Tests CLI Recommandés

```bash
# Test de diagnostic
python -m agents.agent_POSTGRESQL_sqlalchemy_fixer --task diagnose_sqlalchemy --models_path "src/models/"

# Test de correction de modèles
python -m agents.agent_POSTGRESQL_sqlalchemy_fixer --task fix_models --models_path "src/models/user.py"

# Test d'optimisation
python -m agents.agent_POSTGRESQL_sqlalchemy_fixer --task optimize_queries --queries_path "src/queries/"

# Test de validation
python -m agents.agent_POSTGRESQL_sqlalchemy_fixer --task validate_fixes --fix_id FIX_MODEL_001
```

## 📊 Structure des Résultats

### Résultat de Diagnostic
```json
{
  "success": true,
  "data": {
    "models_analyzed": 15,
    "errors_found": 3,
    "warnings": 2,
    "issues": [
      {
        "type": "relationship_error",
        "file": "models/user.py",
        "line": 45,
        "message": "Invalid foreign key reference",
        "severity": "high"
      }
    ],
    "recommendations": [
      "Fix foreign key constraints",
      "Update relationship mappings"
    ]
  }
}
```

### Résultat de Correction
```json
{
  "success": true,
  "data": {
    "fix_id": "FIX_MODEL_001",
    "files_modified": 3,
    "fixes_applied": [
      {
        "type": "foreign_key_fix",
        "file": "models/user.py",
        "description": "Fixed foreign key to profile table",
        "backup_created": "models/user.py.backup_20240101_120000"
      }
    ],
    "validation_status": "pending"
  }
}
```

### Résultat d'Optimisation
```json
{
  "success": true,
  "data": {
    "queries_optimized": 8,
    "performance_improvement": "35%",
    "optimizations": [
      {
        "query_id": "USER_PROFILE_JOIN",
        "optimization": "Added eager loading",
        "before_time": "250ms",
        "after_time": "95ms",
        "improvement": "62%"
      }
    ]
  }
}
```

### Résultat de Validation
```json
{
  "success": true,
  "data": {
    "fix_id": "FIX_MODEL_001",
    "validation_status": "passed",
    "tests_run": 12,
    "tests_passed": 12,
    "tests_failed": 0,
    "performance_metrics": {
      "query_time_avg": "45ms",
      "memory_usage": "12MB",
      "connection_efficiency": "98%"
    }
  }
}
```

## 🧪 Tests et Validation

### Tests Fonctionnels
- ✅ Diagnostic de modèles avec erreurs de relation
- ✅ Correction automatique de clés étrangères
- ✅ Résolution de conflits de métadonnées
- ✅ Optimisation de requêtes N+1
- ✅ Validation post-correction

### Tests de Performance
- ✅ Optimisation de requêtes complexes
- ✅ Amélioration des jointures
- ✅ Réduction du temps d'exécution
- ✅ Optimisation de l'utilisation mémoire

### Tests de Compatibilité
- ✅ SQLAlchemy 1.4.x et 2.0.x
- ✅ PostgreSQL 12 à 16
- ✅ Python 3.8 à 3.12
- ✅ Différents drivers (psycopg2, asyncpg)

## 🏗️ Conformité Pattern Factory

### ✅ Interface Standardisée
- Implémentation de `execute_task(task: Task) -> Result`
- Handlers spécialisés pour chaque type de correction
- Structure de résultats cohérente avec métriques

### ✅ Gestion des Erreurs
- Validation des chemins et paramètres
- Gestion des exceptions SQLAlchemy
- Messages d'erreur techniques détaillés

### ✅ Architecture Modulaire
- Héritage de `AgentPostgreSQLBase`
- Séparation par type de problème SQLAlchemy
- Méthodes privées pour logique métier

### ✅ Sécurité et Sauvegarde
- Création automatique de sauvegardes
- Validation avant application des corrections
- Tests de régression automatiques

## 📈 Statut d'Harmonisation

- **Date de dernière harmonisation**: 2024-12-27
- **Version Pattern Factory**: Conforme v2.0
- **Tests CLI**: ✅ Validés
- **Documentation synchronisée**: ✅ À jour
- **Conformité technique**: ✅ Respectée

## 🔧 Configuration et Personnalisation

### Variables d'Environnement
- `SQLALCHEMY_FIXES_DIR`: Répertoire des corrections (défaut: `fixes/sqlalchemy/`)
- `SQLALCHEMY_BACKUP_ENABLED`: Activation des sauvegardes (défaut: true)

### Paramètres de Configuration
- `workspace_root`: Racine du projet
- `fixes_dir`: Répertoire des corrections
- `auto_backup`: Sauvegarde automatique (défaut: true)
- `validation_timeout`: Timeout pour validation (défaut: 120s)

### Support des Versions
- **SQLAlchemy**: 1.4.0+ et 2.0.0+
- **PostgreSQL**: 12, 13, 14, 15, 16
- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Drivers**: psycopg2, psycopg3, asyncpg

## 📝 Notes Techniques

- Analyse statique du code pour détection d'erreurs
- Support des migrations Alembic
- Optimisation automatique des index PostgreSQL
- Détection des anti-patterns SQLAlchemy
- Integration avec les outils de profiling
- Support des schémas multiples PostgreSQL
- Gestion des types de données spécialisés (JSON, Arrays, etc.)
