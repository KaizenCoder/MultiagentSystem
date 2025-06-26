# Agent MAINTENANCE 01 – Analyseur de Structure

## 1. Identification

- **Nom :** Analyseur de Structure NextGeneration
- **Identifiant :** `agent_MAINTENANCE_01_analyseur_structure`
- **Version :** 1.3.0 (Harmonisation Standards Pattern Factory NextGeneration)
- **Responsable Principal :** Équipe de Maintenance NextGeneration
- **Contact Technique :** `#canal-maintenance-ia`

## 2. Description Générale

🏗️ Agent spécialisé dans l'analyse automatique de la structure des fichiers Python, détection d'incohérences syntaxiques et génération de rapports d'audit structurel pour la maintenance préventive.

Cet agent inspecte la structure du code via l'AST Python, identifie les anomalies et fournit des rapports détaillés pour l'équipe de maintenance.

## 3. Objectifs et Missions

- **Analyse Statique AST :** Parsing et inspection de la structure syntaxique Python
- **Détection d'Incohérences :** Identification d'erreurs syntaxiques et structurelles
- **Extraction de Structure :** Inventaire des imports, classes, fonctions (async/sync)
- **Audit de Qualité :** Génération de rapports structurés pour maintenance
- **Support Équipe :** Compatibilité avec coordinateur d'équipe maintenance

## 4. Fonctionnalités Clés (Conformité Pattern Factory)

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

## 5. Structure d'Analyse

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

## 6. Workflow d'Analyse

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

## 7. Exemples d'Utilisation

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

## 8. Rapports Générés

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

## 9. Dépendances

- **Python 3.8+**
- **Modules standard** : ast, asyncio, logging, pathlib, json
- **core.agent_factory_architecture** (Agent, Task, Result)
- **Aucune dépendance externe** pour l'analyse AST de base

## 10. Journal des Modifications (Changelog)

- **v1.3.0 (2025-06-26)** :
  - Harmonisation avec standards Pattern Factory NextGeneration
  - Enrichissement docstrings classe avec description détaillée des capacités
  - Extension `get_capabilities()` : 1 → 6 capacités spécialisées
  - Documentation .md complètement refaite et synchronisée
- **v1.2.0** :
  - Ajout méthode de compatibilité `run_analysis()` pour coordinateur
  - Amélioration gestion erreurs et logging
- **v1.0** :
  - Version initiale avec analyse AST de base

## 11. Procédure de Test CLI

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

## 12. Statut et Validation

- ✅ **Pattern Factory** : Conforme (Agent, Task, Result)
- ✅ **Méthodes async** : startup, shutdown, execute_task, health_check
- ✅ **Capabilities** : 6 capacités spécialisées définies
- ✅ **Documentation** : Docstrings enrichies et .md synchronisé
- ✅ **Tests CLI** : Procédure de validation définie
- ✅ **Compatibilité** : Méthode `run_analysis()` pour coordinateur

**Agent MAINTENANCE 01 - État : PRÊT POUR VALIDATION**