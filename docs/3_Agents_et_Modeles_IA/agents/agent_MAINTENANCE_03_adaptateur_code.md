# Agent MAINTENANCE 03 – Adaptateur de Code

## 1. Identification

- **Nom :** Adaptateur de Code NextGeneration
- **Identifiant :** `agent_MAINTENANCE_03_adaptateur_code`
- **Version :** 3.1.0 (Harmonisation Standards Pattern Factory NextGeneration)
- **Responsable Principal :** Équipe de Maintenance NextGeneration
- **Contact Technique :** `#canal-maintenance-ia`

## 2. Description Générale

🔧 Agent spécialisé dans l'adaptation et la réparation de code Python via LibCST, manipulation sécurisée de l'AST et stratégies de réparation multi-niveaux pour corriger automatiquement les erreurs courantes.

Cet agent utilise des technologies avancées de transformation AST pour réparer le code tout en préservant le formatage et en appliquant des stratégies ciblées selon le type d'erreur.

## 3. Objectifs et Missions

- **Réparation Intelligente :** Correction automatique d'erreurs avec stratégies adaptées par type
- **Manipulation AST Sécurisée :** Transformations LibCST préservant formatage et structure
- **Correction Multi-Niveaux :** Stratégies en cascade (indentation → imports → noms → générique)
- **Gestion Imports Avancée :** Insertion intelligente avec évitement de doublons
- **Support Équipe Maintenance :** Réparation de code pour workflows de maintenance

## 4. Fonctionnalités Clés (Conformité Pattern Factory)

L'agent respecte le Pattern Factory NextGeneration et expose les méthodes suivantes :

- **`startup()`** : Initialise l'agent adaptateur avec LibCST
- **`health_check()`** : Vérifie l'état de santé. Retourne `{"status": "healthy"}` en fonctionnement normal
- **`execute_task(task: Task)`** : Point d'entrée principal pour les adaptations de code
  - **Action `adapt_code`** :
    - **`task.params` attendus** :
      - `code` (str) : Code source Python à adapter
      - `feedback` (Exception|str) : Feedback/erreur à corriger
      - `error_type` (str, optionnel) : Type d'erreur (indentation/import/name/generic)
    - **Résultat** : Code adapté avec liste des adaptations appliquées
- **`shutdown()`** : Arrête l'agent proprement

### Capacités Spécialisées

```python
get_capabilities() -> [
    "code_adaptation",
    "import_fixing",
    "indentation_error_fix",
    "libcst_ast_transformation",
    "pyflakes_static_analysis",
    "multi_level_repair_strategy",
    "complex_import_management",
    "empty_block_correction",
    "name_error_resolution",
    "formatting_preservation"
]
```

## 5. Technologies Avancées

### LibCST (Concrete Syntax Tree)
- **Transformations AST** préservant le formatage original
- **CSTTransformer personnalisés** pour insertion de code sécurisée
- **Parsing robuste** avec gestion d'erreurs syntaxiques

### Stratégies de Réparation

#### 1. **Erreurs d'Indentation**
```python
# Détection automatique via error_type="indentation"
- "expected an indented block" → insertion 'pass' avec indentation calculée
- "unexpected indent" → suppression indentation superflue  
- "unindent does not match" → normalisation globale (textwrap.dedent)
```

#### 2. **Gestion des Imports**
```python
# Mapping intelligent pour résolution NameError
COMPLEX_IMPORT_MAP = {
    "Path": ("pathlib", "Path"),
    "Agent": ("core.agent_factory_architecture", "Agent"),
    "Task": ("core.agent_factory_architecture", "Task"),
    # ... autres mappings
}
```

#### 3. **Blocs Vides**
- **CstPassInserter** : Insertion automatique `pass` dans blocs vides
- **Gestion try/except** : Création handlers avec `pass` si nécessaire
- **IndentedBlock** : Correction blocs de code vides

### Classes CSTTransformer Spécialisées

#### CstPassInserter
```python
class CstPassInserter(cst.CSTTransformer):
    """Insère 'pass' dans les blocs de code vides."""
    def leave_IndentedBlock(self, original_node, updated_node):
        # Insertion pass si bloc vide
    def leave_Try(self, original_node, updated_node):
        # Gestion spéciale try/except
```

#### CstImportAdder / CstComplexImportAdder  
```python
# Gestion imports simples et complexes avec évitement doublons
# Correction bug LibCST pour chemins modules avec points
```

## 6. Workflow d'Adaptation

```
1. 📋 Réception tâche avec code + feedback + error_type
2. 🎯 Classification erreur et sélection stratégie
3. 🔧 Application réparations ciblées :
   a. Si indentation → _fix_indentation_errors()
   b. Si name → résolution via COMPLEX_IMPORT_MAP
   c. Toujours → CstPassInserter pour blocs vides
4. 🏗️ Transformation LibCST sécurisée
5. ✅ Validation et traçabilité adaptations
6. 📊 Retour code adapté + liste modifications
```

## 7. Exemples d'Utilisation

### Correction d'Erreur d'Indentation

```python
from core.agent_factory_architecture import Task
from agents.agent_MAINTENANCE_03_adaptateur_code import create_agent_MAINTENANCE_03_adaptateur_code

# Code avec erreur d'indentation
code_broken = """
def ma_fonction():
    if True:
print("Hello")  # IndentationError
"""

# Création de l'agent
adaptateur = create_agent_MAINTENANCE_03_adaptateur_code()
await adaptateur.startup()

# Correction d'indentation
task = Task(
    type="adapt_code",
    params={
        "code": code_broken,
        "feedback": IndentationError("expected an indented block"),
        "error_type": "indentation"
    }
)

result = await adaptateur.execute_task(task)
if result.success:
    fixed_code = result.data["adapted_code"]
    adaptations = result.data["adaptations"]
    print(f"Code corrigé:\n{fixed_code}")
    print(f"Adaptations: {adaptations}")
```

### Correction de NameError avec Import

```python
# Code avec NameError
code_name_error = """
def process_data():
    path = Path("/tmp/data")  # NameError: name 'Path' is not defined
    return path.exists()
"""

task = Task(
    type="adapt_code", 
    params={
        "code": code_name_error,
        "feedback": "NameError: name 'Path' is not defined",
        "error_type": "name"
    }
)

result = await adaptateur.execute_task(task)
# Résultat : import pathlib.Path ajouté automatiquement
```

### Correction de Blocs Vides

```python
# Code avec blocs vides
code_empty_blocks = """
def ma_fonction():
    if condition:
        # TODO: implémenter
    try:
        # TODO: code principal
    except Exception:
        # TODO: gestion erreur
"""

task = Task(
    type="adapt_code",
    params={
        "code": code_empty_blocks,
        "feedback": "SyntaxError: unexpected EOF",
        "error_type": "generic"
    }
)

result = await adaptateur.execute_task(task)
# Résultat : 'pass' inséré dans tous les blocs vides
```

## 8. Format de Résultat

### Succès d'Adaptation

```json
{
  "success": true,
  "data": {
    "adapted_code": "# Code Python corrigé avec adaptations",
    "adaptations": [
      "Auto-correction: Ajout de 'pass' à la ligne 5 pour bloc attendu.",
      "Adaptation CST : Ajout de 'pass' dans un ou plusieurs blocs vides.",
      "Import ajouté: from pathlib import Path"
    ]
  }
}
```

### Erreur d'Adaptation

```json
{
  "success": false,
  "error": "Erreur de parsing LibCST: Invalid syntax"
}
```

## 9. Configuration

### Mapping d'Imports Complexes

```python
# Personnalisation du mapping pour résolution NameError
adaptateur.COMPLEX_IMPORT_MAP.update({
    "MonModule": ("mon.package", "MonModule"),
    "MaClasse": ("mon.autre.package", "MaClasse")
})
```

## 10. Dépendances

- **Python 3.8+**
- **LibCST** : Transformations AST avancées
- **Pyflakes** : Analyse statique de code
- **core.agent_factory_architecture** (Agent, Task, Result)
- **Modules standard** : textwrap, re, asyncio, logging

## 11. Journal des Modifications (Changelog)

- **v3.1.0 (2025-06-26)** :
  - Harmonisation avec standards Pattern Factory NextGeneration
  - Enrichissement docstrings classe avec description détaillée LibCST
  - Extension `get_capabilities()` : 3 → 10 capacités spécialisées
  - Documentation .md complètement refaite avec exemples techniques
- **v3.0.0** :
  - Intégration LibCST pour transformations AST sécurisées
  - Classes CSTTransformer personnalisées 
  - Stratégies multi-niveaux selon type d'erreur
- **Versions antérieures** : Correction basique de code

## 12. Procédure de Test CLI

```python
# test_agent_maintenance_03_adaptation.py
import asyncio
from agents.agent_MAINTENANCE_03_adaptateur_code import create_agent_MAINTENANCE_03_adaptateur_code
from core.agent_factory_architecture import Task

async def test_adaptateur_code():
    # 1. Création et startup
    adaptateur = create_agent_MAINTENANCE_03_adaptateur_code()
    await adaptateur.startup()
    
    # 2. Test health check
    health = await adaptateur.health_check()
    print(f"Santé: {health}")
    
    # 3. Test capacités
    caps = adaptateur.get_capabilities()
    print(f"Capacités: {len(caps)} trouvées")
    
    # 4. Test correction indentation
    code_indent_error = '''
def test():
    if True:
print("Hello")
'''
    
    task_indent = Task(
        type="adapt_code",
        params={
            "code": code_indent_error,
            "feedback": IndentationError("expected an indented block"),
            "error_type": "indentation"
        }
    )
    
    result = await adaptateur.execute_task(task_indent)
    print(f"Correction indentation: {result.success}")
    if result.success:
        print(f"  Adaptations: {len(result.data['adaptations'])}")
    
    # 5. Test blocs vides LibCST
    code_empty = '''
def empty_function():
    pass

class EmptyClass:
    pass
'''
    
    task_empty = Task(
        type="adapt_code",
        params={
            "code": code_empty,
            "feedback": "Code avec blocs potentiellement vides",
            "error_type": "generic"
        }
    )
    
    result_empty = await adaptateur.execute_task(task_empty)
    print(f"Gestion blocs vides: {result_empty.success}")
    
    # 6. Shutdown
    await adaptateur.shutdown()

# Exécution
# python -c "import asyncio; asyncio.run(test_adaptateur_code())"
```

## 13. Cas d'Usage Recommandés

- **Réparation automatique** : Correction erreurs syntaxiques dans pipelines CI/CD
- **Maintenance de code** : Adaptation massive de code legacy
- **Migration de projets** : Harmonisation imports et structure
- **Workflow de développement** : Correction automatique en temps réel
- **Refactorisation assistée** : Transformations sécurisées avec LibCST

## 14. Statut et Validation

- ✅ **Pattern Factory** : Conforme (Agent, Task, Result)
- ✅ **Méthodes async** : startup, shutdown, execute_task, health_check
- ✅ **Capabilities** : 10 capacités spécialisées définies  
- ✅ **Technologies** : LibCST, Pyflakes, CSTTransformer
- ✅ **Documentation** : Docstrings enrichies et .md synchronisé
- ✅ **Tests CLI** : Procédure de validation définie
- ✅ **Multi-Level Repair** : Stratégies adaptées par type d'erreur

**Agent MAINTENANCE 03 - État : PRÊT POUR VALIDATION**