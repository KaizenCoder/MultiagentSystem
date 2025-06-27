# Agent MAINTENANCE 02 – Évaluateur d'Utilité

## 1. Identification

- **Nom :** Évaluateur d'Utilité NextGeneration
- **Identifiant :** `agent_MAINTENANCE_02_evaluateur_utilite`
- **Version :** 3.1.0 (Logging Uniforme + Audit Universel)
- **Responsable Principal :** Équipe de Maintenance NextGeneration
- **Contact Technique :** `#canal-maintenance-ia`

## 2. Description Générale

⚖️ Agent spécialisé dans l'évaluation quantitative de la pertinence et de la qualité fonctionnelle du code Python avec capacités d'audit universel. Utilise l'analyse AST avancée avec système de scoring heuristique pour évaluer des fichiers individuels ou des projets complets.

**🚀 NOUVEAUTÉ V3.1 (Travaux claudecode) :** Intégration complète du système de logging uniforme + capacité d'audit universel d'évaluation étendue pour analyser et scorer des **projets Python complets** (répertoires entiers) en plus des fichiers individuels.

### 🔧 Système de Logging Uniforme V3.1
```python
# ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ (claudecode)
try:
    from core.manager import LoggingManager
    logging_manager = LoggingManager()
    self.logger = logging_manager.get_logger(
        config_name="maintenance",
        custom_config={
            "logger_name": f"nextgen.maintenance.evaluateur_utilite.{self.id}",
            "log_dir": "logs/maintenance/evaluateur",
            "metadata": {
                "agent_type": "MAINTENANCE_02_evaluateur_utilite",
                "agent_role": "evaluateur_utilite",
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
- **Évaluation Quantitative** : Scoring automatique basé sur l'analyse AST des structures Python
- **Classification d'Utilité** : Détermination binaire utilité/inutilité selon seuil configurable
- **Détection d'Obsolescence** : Identification d'éléments vides ou non fonctionnels
- **Analyse de Complexité** : Mesure de la richesse structurelle et fonctionnelle
- **Support Maintenance** : Aide à la décision pour conservation/suppression de code

### 3.2 Capacités d'Audit Universel (V3.0)
- **Audit de fichiers individuels** : Évaluation et scoring d'un fichier Python spécifique
- **🆕 Audit de répertoires complets** : Analyse et scoring récursif de structures de projets entières
- **Filtrage intelligent** : Exclusion automatique des répertoires non pertinents (.venv, __pycache__, .git, etc.)
- **Rapports consolidés** : Métriques d'utilité globales + détails par fichier
- **Scoring unifié** : Système de notation d'utilité cohérent (0-100)

## 4. Architecture V3.0 (Mission Claudecode)

### 4.1 Architecture Technique
- **Orchestrateur Central** : `audit_universal_evaluation` coordonne tous les types d'audit
- **Audit Fichier Unique** : `_audit_single_python_file` pour l'analyse et scoring détaillé
- **Filtrage Intelligent** : `_should_skip_path` pour ignorer les répertoires non pertinents
- **Mapping Qualité** : `_map_score_to_utility_health` pour la notation uniforme
- **Gestion Consolidée** : Centralisation des métriques et scoring dans l'orchestrateur

### 4.2 Métriques d'Utilité
```python
utility_metrics = {
    'code_complexity': {'weight': 0.3, 'threshold': {'warning': 70, 'critical': 50}},
    'functional_richness': {'weight': 0.3, 'threshold': {'warning': 75, 'critical': 60}},
    'code_reuse': {'weight': 0.2, 'threshold': {'warning': 80, 'critical': 65}},
    'maintainability': {'weight': 0.2, 'threshold': {'warning': 85, 'critical': 70}}
}
```

## 5. Guide d'Utilisation

### 5.1 Initialisation
```python
from agents.agent_MAINTENANCE_02_evaluateur_utilite import AgentMAINTENANCE02EvaluateurUtilite
agent = AgentMAINTENANCE02EvaluateurUtilite()
await agent.startup()
```

### 5.2 Audit d'un Fichier Individuel
```python
# Audit d'utilité d'un fichier Python spécifique
task_details = {
    "action": "audit_universal_evaluation",
    "params": {
        "target_path": "chemin/vers/votre/fichier.py"
    }
}
result = await agent.execute_task(task_details)
print(f"Score utilité : {result['data']['score_global']}/100")
print(f"État de l'utilité : {result['data']['etat_utilite']}")
```

### 5.3 🆕 Audit d'un Projet Complet (V3.0)
```python
# Audit d'utilité d'un répertoire complet
task_details = {
    "action": "audit_universal_evaluation",
    "params": {
        "target_path": "chemin/vers/votre/projet/"
    }
}
result = await agent.execute_task(task_details)

# Résultats consolidés
print(f"Nombre de fichiers analysés : {result['data']['nb_fichiers_analyses']}")
print(f"Score global d'utilité : {result['data']['score_global']}/100")
print(f"État global de l'utilité : {result['data']['etat_utilite']}")

# Détails par fichier
for fichier_result in result['data']['resultats_fichiers']:
    print(f"- {fichier_result['fichier']} :")
    print(f"  Score : {fichier_result['score']}/100")
    print(f"  Problèmes utilité : {len(fichier_result['utility_issues'])}")
```

## 6. Spécifications Techniques V3.0

### 6.1 Méthodes Principales
- **`audit_universal_evaluation(target_path)`** : Orchestrateur principal (fichier ou répertoire)
- **`_audit_single_python_file(file_path)`** : Audit détaillé d'utilité d'un fichier
- **`_should_skip_path(path)`** : Filtrage intelligent des chemins à ignorer
- **`_map_score_to_utility_health(score)`** : Mapping score → état de l'utilité

### 6.2 Filtrage Intelligent
Répertoires automatiquement ignorés :
- `.venv/`, `venv/`, `env/` (environnements virtuels)
- `__pycache__/`, `.pyc` (cache Python)
- `.git/`, `.svn/` (contrôle de version)
- `node_modules/`, `.npm/` (dépendances JS)
- `build/`, `dist/`, `.egg-info/` (artefacts de build)

### 6.3 Métriques d'Utilité
- **Score global** : Note consolidée 0-100
- **Nombre de fichiers** : Fichiers Python analysés
- **Problèmes utilité** : Issues détectées par type
- **Complexité du code** : Richesse structurelle
- **Richesse fonctionnelle** : Diversité des fonctionnalités
- **Réutilisation du code** : Modularité et réutilisation

## 7. Fonctionnalités Clés (Conformité Pattern Factory)

L'agent respecte le Pattern Factory NextGeneration et expose les méthodes suivantes :

- **`startup()`** : Initialise l'agent évaluateur d'utilité
- **`health_check()`** : Vérifie l'état de santé. Retourne `{"status": "ok"}` en fonctionnement normal
- **`execute_task(task: Task)`** : Point d'entrée principal pour les évaluations d'utilité
  - **Action attendue** : Évaluation de fichier Python
    - **`task.params` attendus** :
      - `file_path` (str) : Chemin vers le fichier Python à évaluer
    - **Résultat** : Score d'utilité, classification binaire et détails
- **`shutdown()`** : Arrête l'agent proprement

### Capacités Spécialisées

```python
get_capabilities() -> [
    "evaluate_utility",
    "ast_evaluation", 
    "scoring_heuristique_code",
    "detection_elements_obsoletes",
    "classification_binaire_utilite",
    "analyse_complexite_structurelle",
    "gestion_erreurs_syntaxiques"
]
```

## 8. Système de Scoring Heuristique

### Métriques de Base

| Élément AST | Points Attribués | Description |
|-------------|------------------|-------------|
| **Import** | +1 par import | Chaque module importé |
| **Classe** | +10 + len(body) | Points base + complexité interne |
| **Fonction** | +5 + len(body) | Points base + complexité interne |
| **Appel de fonction** | +1 | Chaque ast.Call détecté |
| **Structure contrôle** | +2 | if/for/while/try |

### Bonus et Malus

- **Bonus Classe + Fonction** : +5 points si présence des deux
- **Malus Éléments Vides** : -5 points par fonction/classe avec seulement `pass`

### Classification

```python
score >= seuil_min (défaut: 15) → "Utile" (is_useful: True)
score < seuil_min → "Peu utile" (is_useful: False)
```

## 9. Workflow d'Évaluation

```
1. 📋 Réception tâche avec file_path
2. 📖 Lecture fichier Python (UTF-8)
3. 🏗️ Parsing AST du code source
4. 🧮 Calcul score via métriques heuristiques
5. ⚖️ Classification binaire selon seuil
6. 📊 Retour résultat structuré
```

## 10. Format de Résultat

### Succès d'Évaluation

```json
{
  "success": true,
  "data": {
    "score": 42,
    "is_useful": true,
    "details": "Évaluation réussie"
  }
}
```

### Erreur Syntaxique

```json
{
  "success": true,
  "data": {
    "score": 0,
    "is_useful": false,
    "details": "Erreur de syntaxe: invalid syntax (line 15)"
  }
}
```

### Erreur de Lecture

```json
{
  "success": false,
  "error": "Erreur de lecture du fichier: [Errno 2] No such file or directory"
}
```

## 11. Exemples d'Utilisation

### Évaluation d'un Agent

```python
from core.agent_factory_architecture import Task
from agents.agent_MAINTENANCE_02_evaluateur_utilite import create_agent_MAINTENANCE_02_evaluateur_utilite

# Création de l'agent
evaluateur = create_agent_MAINTENANCE_02_evaluateur_utilite()
await evaluateur.startup()

# Évaluation d'un fichier
task = Task(
    type="evaluate_utility",
    params={"file_path": "./agents/agent_exemple.py"}
)

result = await evaluateur.execute_task(task)
if result.success:
    score = result.data["score"]
    is_useful = result.data["is_useful"]
    print(f"Score: {score}, Utile: {is_useful}")
else:
    print(f"Erreur: {result.error}")

await evaluateur.shutdown()
```

### Évaluation de Plusieurs Fichiers

```python
files_to_evaluate = [
    "./agents/agent_01.py",
    "./agents/agent_02.py", 
    "./agents/agent_obsolete.py"
]

results = []
for file_path in files_to_evaluate:
    task = Task(type="evaluate_utility", params={"file_path": file_path})
    result = await evaluateur.execute_task(task)
    results.append({
        "file": file_path,
        "score": result.data.get("score", 0) if result.success else 0,
        "useful": result.data.get("is_useful", False) if result.success else False
    })

# Filtrer les agents utiles
useful_agents = [r for r in results if r["useful"]]
print(f"Agents utiles: {len(useful_agents)}/{len(results)}")
```

## 12. Configuration

### Seuil d'Utilité Personnalisé

```python
# Via configuration d'agent (si disponible)
evaluateur.config = {"min_score_for_usefulness": 20}  # Seuil plus élevé

# Seuil par défaut : 15 points
```

## 13. Dépendances

- **Python 3.8+**
- **Modules standard** : ast, pathlib, logging
- **core.agent_factory_architecture** (Agent, Task, Result)
- **Aucune dépendance externe** pour l'analyse AST

## 14. Journal des Modifications (Changelog)

- **v2.2.0 (2025-06-26)** :
  - Harmonisation avec standards Pattern Factory NextGeneration
  - Enrichissement docstrings classe avec description détaillée du scoring
  - Extension `get_capabilities()` : 2 → 7 capacités spécialisées
  - Documentation .md complètement refaite avec exemples concrets
- **v2.1.0** :
  - Amélioration système de scoring avec bonus/malus
  - Gestion robuste des erreurs syntaxiques
- **v1.0** :
  - Version initiale avec évaluation AST de base

## 15. Procédure de Test CLI

```python
# test_agent_maintenance_02_evaluation.py
import asyncio
from agents.agent_MAINTENANCE_02_evaluateur_utilite import create_agent_MAINTENANCE_02_evaluateur_utilite
from core.agent_factory_architecture import Task

async def test_evaluateur_utilite():
    # 1. Création et startup
    evaluateur = create_agent_MAINTENANCE_02_evaluateur_utilite()
    await evaluateur.startup()
    
    # 2. Test health check
    health = await evaluateur.health_check()
    print(f"Santé: {health}")
    
    # 3. Test capacités
    caps = evaluateur.get_capabilities()
    print(f"Capacités: {len(caps)} trouvées")
    
    # 4. Test auto-évaluation
    task_self = Task(
        type="evaluate_utility",
        params={"file_path": "./agents/agent_MAINTENANCE_02_evaluateur_utilite.py"}
    )
    
    result = await evaluateur.execute_task(task_self)
    print(f"Auto-évaluation réussie: {result.success}")
    if result.success:
        print(f"  Score: {result.data['score']}")
        print(f"  Utile: {result.data['is_useful']}")
        print(f"  Détails: {result.data['details']}")
    
    # 5. Test fichier inexistant
    task_error = Task(
        type="evaluate_utility", 
        params={"file_path": "./fichier_inexistant.py"}
    )
    
    result_error = await evaluateur.execute_task(task_error)
    print(f"Gestion erreur: {not result_error.success}")
    
    # 6. Shutdown
    await evaluateur.shutdown()

# Exécution
# python -c "import asyncio; asyncio.run(test_evaluateur_utilite())"
```

## 16. Cas d'Usage Recommandés

- **Audit de codebase** : Identification des fichiers peu utiles
- **Nettoyage de maintenance** : Support à la décision de suppression
- **Évaluation qualité** : Mesure quantitative de la richesse du code
- **Triage automatique** : Classification rapide de grands volumes de fichiers
- **Métriques de projet** : Calcul de scores globaux de qualité

## 17. Statut et Validation

- ✅ **Pattern Factory** : Conforme (Agent, Task, Result)
- ✅ **Méthodes async** : startup, shutdown, execute_task, health_check  
- ✅ **Capabilities** : 7 capacités spécialisées définies
- ✅ **Documentation** : Docstrings enrichies et .md synchronisé
- ✅ **Tests CLI** : Procédure de validation définie
- ✅ **Scoring System** : Métriques heuristiques documentées

**Agent MAINTENANCE 02 - État : PRÊT POUR VALIDATION**