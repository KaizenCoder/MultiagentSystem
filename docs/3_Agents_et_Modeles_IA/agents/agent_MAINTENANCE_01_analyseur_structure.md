# Agent MAINTENANCE 01 – Analyseur de Structure

## 1. Identification

- **Nom :** Analyseur de Structure NextGeneration
- **Identifiant :** `agent_MAINTENANCE_01_analyseur_structure`
- **Version :** 2.1.0 (Logging Uniforme + Audit Universel)
- **Responsable Principal :** Équipe de Maintenance NextGeneration
- **Contact Technique :** `#canal-maintenance-ia`

## 2. Description Générale

🏗️ Agent spécialisé dans l'analyse automatique de la structure du code Python avec capacités d'audit universel. Utilise l'AST Python pour détecter les incohérences syntaxiques et générer des rapports d'audit structurel pour des fichiers individuels ou des projets complets.

**🚀 NOUVEAUTÉ V2.1 (Travaux claudecode) :** Intégration complète du système de logging uniforme + capacité d'audit universel de structure étendue pour analyser des **projets Python complets** (répertoires entiers) en plus des fichiers individuels.

### 🔧 Système de Logging Uniforme V2.1
```python
# ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ (claudecode)
try:
    from core.manager import LoggingManager
    logging_manager = LoggingManager()
    self.logger = logging_manager.get_logger(
        config_name="maintenance",
        custom_config={
            "logger_name": f"nextgen.maintenance.analyseur_structure.{self.id}",
            "log_dir": "logs/maintenance/analyseur",
            "metadata": {
                "agent_type": "MAINTENANCE_01_analyseur_structure",
                "agent_role": "analyseur_structure",
                "system": "nextgeneration"
            }
        }
    )
except ImportError:
    # Fallback en cas d'indisponibilité du LoggingManager
    self.logger = logging.getLogger(self.__class__.__name__)
```

## 3. Objectifs et Missions

### 3.1 Missions Principales
- **Analyse Statique AST** : Parsing et inspection de la structure syntaxique Python
- **Détection d'Incohérences** : Identification d'erreurs syntaxiques et structurelles
- **Extraction de Structure** : Inventaire des imports, classes, fonctions (async/sync)
- **Audit de Qualité** : Génération de rapports structurés pour maintenance
- **Support Équipe** : Compatibilité avec coordinateur d'équipe maintenance

### 3.2 Capacités d'Audit Universel (V2.0)
- **Audit de fichiers individuels** : Analyse et scoring d'un fichier Python spécifique
- **🆕 Audit de répertoires complets** : Analyse et scoring récursif de structures de projets entières
- **Filtrage intelligent** : Exclusion automatique des répertoires non pertinents (.venv, __pycache__, .git, etc.)
- **Rapports consolidés** : Métriques de structure globales + détails par fichier
- **Scoring unifié** : Système de notation de structure cohérent (0-100)

## 4. Architecture V2.0 (Mission Claudecode)

### 4.1 Architecture Technique
- **Orchestrateur Central** : `audit_universal_structure` coordonne tous les types d'audit
- **Audit Fichier Unique** : `_audit_single_python_file` pour l'analyse et scoring détaillé
- **Filtrage Intelligent** : `_should_skip_path` pour ignorer les répertoires non pertinents
- **Mapping Qualité** : `_map_score_to_structure_health` pour la notation uniforme
- **Gestion Consolidée** : Centralisation des métriques et scoring dans l'orchestrateur

### 4.2 Métriques de Structure
```python
structure_metrics = {
    'code_organization': {'weight': 0.3, 'threshold': {'warning': 70, 'critical': 50}},
    'syntax_correctness': {'weight': 0.3, 'threshold': {'warning': 75, 'critical': 60}},
    'import_structure': {'weight': 0.2, 'threshold': {'warning': 80, 'critical': 65}},
    'class_hierarchy': {'weight': 0.2, 'threshold': {'warning': 85, 'critical': 70}}
}
```

## 5. Guide d'Utilisation

### 5.1 Initialisation
```python
from agents.agent_MAINTENANCE_01_analyseur_structure import AgentMAINTENANCE01AnalyseurStructure
agent = AgentMAINTENANCE01AnalyseurStructure()
await agent.startup()
```

### 5.2 Audit d'un Fichier Individuel
```python
# Audit de structure d'un fichier Python spécifique
task_details = {
    "action": "audit_universal_structure",
    "params": {
        "target_path": "chemin/vers/votre/fichier.py"
    }
}
result = await agent.execute_task(task_details)
print(f"Score structure : {result['data']['score_global']}/100")
print(f"État de la structure : {result['data']['etat_structure']}")
```

### 5.3 🆕 Audit d'un Projet Complet (V2.0)
```python
# Audit de structure d'un répertoire complet
task_details = {
    "action": "audit_universal_structure",
    "params": {
        "target_path": "chemin/vers/votre/projet/"
    }
}
result = await agent.execute_task(task_details)

# Résultats consolidés
print(f"Nombre de fichiers analysés : {result['data']['nb_fichiers_analyses']}")
print(f"Score global de structure : {result['data']['score_global']}/100")
print(f"État global de la structure : {result['data']['etat_structure']}")

# Détails par fichier
for fichier_result in result['data']['resultats_fichiers']:
    print(f"- {fichier_result['fichier']} :")
    print(f"  Score : {fichier_result['score']}/100")
    print(f"  Problèmes structure : {len(fichier_result['structure_issues'])}")
```

## 6. Spécifications Techniques V2.0

### 6.1 Méthodes Principales
- **`audit_universal_structure(target_path)`** : Orchestrateur principal (fichier ou répertoire)
- **`_audit_single_python_file(file_path)`** : Audit détaillé de structure d'un fichier
- **`_should_skip_path(path)`** : Filtrage intelligent des chemins à ignorer
- **`_map_score_to_structure_health(score)`** : Mapping score → état de la structure

### 6.2 Filtrage Intelligent
Répertoires automatiquement ignorés :
- `.venv/`, `venv/`, `env/` (environnements virtuels)
- `__pycache__/`, `.pyc` (cache Python)
- `.git/`, `.svn/` (contrôle de version)
- `node_modules/`, `.npm/` (dépendances JS)
- `build/`, `dist/`, `.egg-info/` (artefacts de build)

### 6.3 Métriques de Structure
- **Score global** : Note consolidée 0-100
- **Nombre de fichiers** : Fichiers Python analysés
- **Problèmes structure** : Issues détectées par type
- **Organisation du code** : Clarté et cohérence
- **Correction syntaxique** : Validité du code
- **Structure des imports** : Organisation des dépendances

## 7. Fonctionnalités Clés (Conformité Pattern Factory)

L'agent respecte le Pattern Factory NextGeneration et expose les méthodes suivantes :

- **`startup()`** : Initialise l'agent et prépare l'analyseur de structure
- **`health_check()`** : Vérifie l'état de santé. Retourne `{"status": "healthy"}` en fonctionnement normal
- **`execute_task(task: Task)`** : Point d'entrée principal pour les analyses de structure
  - **Action `analyse_structure`** :
    - **`task.params` attendus** :
      - `directory` (str, optionnel) : Chemin vers répertoire à analyser (tous les .py)
      - `file_path` (str, optionnel) : Chemin vers fichier Python spécifique
    - **Résultat** : Rapport d'analyse avec structure détectée ou erreurs
- **`shutdown()`** : Arrête l'agent proprement

### Capacités Spécialisées

```python
get_capabilities() -> [
    "analyse_structure",
    "analyse_ast_python",
    "detection_erreurs_syntaxiques", 
    "extraction_imports_classes_fonctions",
    "analyse_repertoire_complet",
    "compatibilite_coordinateur_maintenance"
]
```

### Méthode de Compatibilité

- **`run_analysis(directory: str)`** : Méthode de compatibilité pour coordinateur d'équipe

## 8. Structure d'Analyse

### Données Extraites par AST

```python
analysis_report = {
    "imports": [        # Liste des modules importés
        "asyncio", "ast", "json", ...
    ],
    "classes": [        # Liste des classes définies
        "AgentMAINTENANCE01AnalyseurStructure", ...
    ],
    "functions": [      # Liste des fonctions (avec préfixe "async" si applicable)
        "startup", "async execute_task", ...
    ],
    "has_async": bool   # Présence de fonctions async
}
```

### Gestion d'Erreurs

En cas d'erreur syntaxique :
```python
{"error": "SyntaxError: invalid syntax (line 42)"}
```

## 9. Workflow d'Analyse

```
1. 📋 Réception tâche avec directory OU file_path
2. 🔍 Si directory → Liste tous fichiers .py
3. 📖 Pour chaque fichier :
   a. Lecture contenu UTF-8
   b. Parsing AST Python
   c. Extraction structure (imports/classes/fonctions)
   d. Détection erreurs syntaxiques
4. 📊 Agrégation résultats
5. ✅ Retour rapport complet
```

## 10. Exemples d'Utilisation

### Analyse d'un Fichier Spécifique

```python
from core.agent_factory_architecture import Task
from agents.agent_MAINTENANCE_01_analyseur_structure import create_agent_MAINTENANCE_01_analyseur_structure

# Création de l'agent
agent = create_agent_MAINTENANCE_01_analyseur_structure()
await agent.startup()

# Analyse d'un fichier
task = Task(
    type="analyse_structure",
    params={"file_path": "./agents/agent_exemple.py"}
)

result = await agent.execute_task(task)
if result.success:
    analysis = result.data["analysis"]
    print(f"Classes: {analysis['classes']}")
    print(f"Fonctions: {analysis['functions']}")
else:
    print(f"Erreur: {result.error}")
```

### Analyse d'un Répertoire Complet

```python
# Analyse de tout un répertoire
task = Task(
    type="analyse_structure", 
    params={"directory": "./agents"}
)

result = await agent.execute_task(task)
if result.success:
    for file_analysis in result.data["files"]:
        path = file_analysis["path"]
        if "error" in file_analysis:
            print(f"❌ {path}: {file_analysis['error']}")
        else:
            analysis = file_analysis["analysis"]
            print(f"✅ {path}: {len(analysis['classes'])} classes, {len(analysis['functions'])} fonctions")
```

## 11. Rapports Générés

### Format de Sortie - Fichier Unique

```json
{
  "path": "./agents/agent_exemple.py",
  "analysis": {
    "imports": ["asyncio", "logging", "pathlib"],
    "classes": ["AgentExemple"],
    "functions": ["async startup", "async execute_task", "get_capabilities"],
    "has_async": true
  }
}
```

### Format de Sortie - Répertoire

```json
{
  "files": [
    {
      "path": "./agents/agent_01.py",
      "analysis": { ... }
    },
    {
      "path": "./agents/agent_02.py", 
      "error": "SyntaxError: invalid syntax"
    }
  ]
}
```

## 12. Dépendances

- **Python 3.8+**
- **Modules standard** : ast, asyncio, logging, pathlib, json
- **core.agent_factory_architecture** (Agent, Task, Result)
- **Aucune dépendance externe** pour l'analyse AST de base

## 13. Journal des Modifications (Changelog)

- **v2.0.0 (2025-06-26)** :
  - Harmonisation avec standards Pattern Factory NextGeneration
  - Enrichissement docstrings classe avec description détaillée des capacités
  - Extension `get_capabilities()` : 1 → 6 capacités spécialisées
  - Documentation .md complètement refaite et synchronisée
- **v1.2.0** :
  - Ajout méthode de compatibilité `run_analysis()` pour coordinateur
  - Amélioration gestion erreurs et logging
- **v1.0** :
  - Version initiale avec analyse AST de base

## 14. Procédure de Test CLI

```python
# test_agent_maintenance_01_structure.py
import asyncio
from agents.agent_MAINTENANCE_01_analyseur_structure import create_agent_MAINTENANCE_01_analyseur_structure
from core.agent_factory_architecture import Task

async def test_analyseur_structure():
    # 1. Création et startup
    agent = create_agent_MAINTENANCE_01_analyseur_structure()
    await agent.startup()
    
    # 2. Test health check
    health = await agent.health_check()
    print(f"Santé: {health}")
    
    # 3. Test capacités
    caps = agent.get_capabilities()
    print(f"Capacités: {caps}")
    
    # 4. Test analyse fichier spécifique (auto-analyse)
    task_file = Task(
        type="analyse_structure",
        params={"file_path": "./agents/agent_MAINTENANCE_01_analyseur_structure.py"}
    )
    
    result = await agent.execute_task(task_file)
    print(f"Auto-analyse réussie: {result.success}")
    if result.success:
        analysis = result.data["analysis"]
        print(f"  Classes trouvées: {len(analysis['classes'])}")
        print(f"  Fonctions trouvées: {len(analysis['functions'])}")
        print(f"  Async détecté: {analysis['has_async']}")
    
    # 5. Test méthode compatibilité
    result_compat = await agent.run_analysis("./agents")
    print(f"Analyse répertoire (compat): {result_compat.success}")
    
    # 6. Shutdown
    await agent.shutdown()

# Exécution
# python -c "import asyncio; asyncio.run(test_analyseur_structure())"
```

## 15. Statut et Validation

- ✅ **Pattern Factory** : Conforme (Agent, Task, Result)
- ✅ **Méthodes async** : startup, shutdown, execute_task, health_check
- ✅ **Capabilities** : 6 capacités spécialisées définies
- ✅ **Documentation** : Docstrings enrichies et .md synchronisé
- ✅ **Tests CLI** : Procédure de validation définie
- ✅ **Compatibilité** : Méthode `run_analysis()` pour coordinateur

**Agent MAINTENANCE 01 - État : PRÊT POUR VALIDATION**