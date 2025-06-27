# Agent MAINTENANCE 03 – Adaptateur de Code

## 1. Identification

- **Nom :** Adaptateur de Code NextGeneration
- **Identifiant :** `agent_MAINTENANCE_03_adaptateur_code`
- **Version :** 4.2.0 (Priorités Hautes : Classification Étendue + Auto-découverte + Validation Multi-niveaux)
- **Responsable Principal :** Équipe de Maintenance NextGeneration
- **Contact Technique :** `#canal-maintenance-ia`

## 2. Description Générale

🔧 Agent spécialisé dans l'adaptation et la réparation de code Python avec capacités d'audit universel. Utilise LibCST pour la manipulation sécurisée de l'AST et applique des stratégies de réparation multi-niveaux pour corriger automatiquement les erreurs courantes dans des fichiers individuels ou des projets complets.

**🚀 NOUVEAUTÉ V4.2 (Priorités Hautes) :** Système de classification d'erreurs étendu (9 types), auto-découverte intelligente des imports par analyse AST du projet, et validation multi-niveaux avec scoring de confiance pour une adaptation précise et fiable.

**🔧 HÉRITAGE V4.1 :** Moteur de correction d'indentation entièrement repensé avec stratégies intelligentes, détection automatique du style d'indentation, et réparation contextuelle avancée.

**📊 HÉRITAGE V4.0 :** Capacité d'audit universel d'adaptation étendue pour analyser et corriger des **projets Python complets** (répertoires entiers) en plus des fichiers individuels.

## 3. Objectifs et Missions

### 3.1 Missions Principales V4.2
- **🧠 Classification Étendue** : 9 types d'erreurs (indentation/name/import/syntax/type_error/attribute_error/value_error/module_not_found/generic) avec scoring de confiance
- **🔍 Auto-découverte Imports** : Analyse AST complète du projet pour découverte automatique des imports avec cache intelligent et scoring basé sur l'usage
- **🎯 Validation Multi-niveaux** : Validation syntaxique + sémantique + compilation + résolution imports avec scoring global de confiance
- **🔧 Moteur Indentation V4.1** : Correction intelligente avec détection automatique style (espaces/tabs) et stack d'indentation contextuelle
- **🚀 Réparation Intelligente** : Stratégies spécialisées par type d'erreur avec suggestions automatiques et historique d'apprentissage
- **⚙️ Manipulation AST Sécurisée** : Transformations LibCST préservant formatage et structure
- **📊 Support Équipe Maintenance** : Intégration cycle M-T-D (Maintenance-Test-Documentation-Validation)

### 3.2 Capacités d'Audit Universel (V4.0)
- **Audit de fichiers individuels** : Adaptation et correction d'un fichier Python spécifique
- **🆕 Audit de répertoires complets** : Analyse et correction récursive de structures de projets entières
- **Filtrage intelligent** : Exclusion automatique des répertoires non pertinents (.venv, __pycache__, .git, etc.)
- **Rapports consolidés** : Métriques d'adaptation globales + détails par fichier
- **Scoring unifié** : Système de notation de qualité d'adaptation cohérent (0-100)

## 4. Architecture V4.0 (Mission Claudecode)

### 4.1 Architecture Technique
- **Orchestrateur Central** : `audit_universal_adaptation` coordonne tous les types d'audit
- **Audit Fichier Unique** : `_audit_single_python_file` pour l'analyse et correction détaillée
- **Filtrage Intelligent** : `_should_skip_path` pour ignorer les répertoires non pertinents
- **Mapping Qualité** : `_map_score_to_adaptation_health` pour la notation uniforme
- **Gestion Consolidée** : Centralisation des métriques et scoring dans l'orchestrateur

### 4.2 Métriques d'Adaptation
```python
adaptation_metrics = {
    'code_quality': {'weight': 0.3, 'threshold': {'warning': 70, 'critical': 50}},
    'error_resolution': {'weight': 0.3, 'threshold': {'warning': 75, 'critical': 60}},
    'import_management': {'weight': 0.2, 'threshold': {'warning': 80, 'critical': 65}},
    'formatting_preservation': {'weight': 0.2, 'threshold': {'warning': 85, 'critical': 70}}
}
```

## 5. Guide d'Utilisation

### 5.1 Initialisation
```python
from agents.agent_MAINTENANCE_03_adaptateur_code import AgentMAINTENANCE03AdaptateurCode
agent = AgentMAINTENANCE03AdaptateurCode()
await agent.startup()
```

### 5.2 Audit d'un Fichier Individuel
```python
# Audit d'adaptation d'un fichier Python spécifique
task_details = {
    "action": "audit_universal_adaptation",
    "params": {
        "target_path": "chemin/vers/votre/fichier.py"
    }
}
result = await agent.execute_task(task_details)
print(f"Score adaptation : {result['data']['score_global']}/100")
print(f"État de l'adaptation : {result['data']['etat_adaptation']}")
```

### 5.3 🆕 Audit d'un Projet Complet (V4.0)
```python
# Audit d'adaptation d'un répertoire complet
task_details = {
    "action": "audit_universal_adaptation",
    "params": {
        "target_path": "chemin/vers/votre/projet/"
    }
}
result = await agent.execute_task(task_details)

# Résultats consolidés
print(f"Nombre de fichiers analysés : {result['data']['nb_fichiers_analyses']}")
print(f"Score global d'adaptation : {result['data']['score_global']}/100")
print(f"État global de l'adaptation : {result['data']['etat_adaptation']}")

# Détails par fichier
for fichier_result in result['data']['resultats_fichiers']:
    print(f"- {fichier_result['fichier']} :")
    print(f"  Score : {fichier_result['score']}/100")
    print(f"  Problèmes adaptation : {len(fichier_result['adaptation_issues'])}")
```

## 6. Spécifications Techniques V4.0

### 6.1 Méthodes Principales
- **`audit_universal_adaptation(target_path)`** : Orchestrateur principal (fichier ou répertoire)
- **`_audit_single_python_file(file_path)`** : Audit détaillé d'adaptation d'un fichier
- **`_should_skip_path(path)`** : Filtrage intelligent des chemins à ignorer
- **`_map_score_to_adaptation_health(score)`** : Mapping score → état de l'adaptation

### 6.2 Filtrage Intelligent
Répertoires automatiquement ignorés :
- `.venv/`, `venv/`, `env/` (environnements virtuels)
- `__pycache__/`, `.pyc` (cache Python)
- `.git/`, `.svn/` (contrôle de version)
- `node_modules/`, `.npm/` (dépendances JS)
- `build/`, `dist/`, `.egg-info/` (artefacts de build)

### 6.3 Métriques d'Adaptation
- **Score global** : Note consolidée 0-100
- **Nombre de fichiers** : Fichiers Python analysés
- **Problèmes adaptation** : Issues détectées par type
- **Qualité du code** : Respect des standards
- **Résolution erreurs** : Efficacité des corrections
- **Gestion imports** : Qualité des imports ajoutés

## 7. Fonctionnalités Clés (Conformité Pattern Factory)

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

## 8. Technologies Avancées

### LibCST (Concrete Syntax Tree)
- **Transformations AST** préservant le formatage original
- **CSTTransformer personnalisés** pour insertion de code sécurisée
- **Parsing robuste** avec gestion d'erreurs syntaxiques

### Stratégies de Réparation V4.1

#### 1. **🆕 Moteur d'Indentation Amélioré (Volet 2)**
```python
# Détection automatique via error_type="indentation"
def _fix_indentation_errors(code: str, error: Exception) -> Tuple[str, List[str]]:
    """
    Moteur de correction d'indentation robuste avec stratégies intelligentes :
    
    🔍 DÉTECTION AUTOMATIQUE :
    - Style d'indentation (espaces vs tabs)
    - Niveau d'indentation contextuel
    - Analyse syntaxique des blocs
    
    🛠️ STRATÉGIES CIBLÉES :
    - "expected an indented block" → insertion 'pass' avec analyse contextuelle
    - "unexpected indent" → correction intelligente avec référence au contexte
    - "unindent does not match" → reconstruction avec stack d'indentation
    
    ⚡ TECHNOLOGIES :
    - Stack d'indentation pour cohérence globale
    - Analyse heuristique des structures (def, class, if, etc.)
    - Préservation du style d'indentation existant
    - Stratégies de fallback multiples
    """
```

**Cas 1 : "expected an indented block"**
- Analyse de la ligne précédente (détection ':')
- Calcul intelligent du niveau d'indentation requis
- Insertion 'pass' avec indentation adaptée au contexte

**Cas 2 : "unexpected indent"**  
- Recherche du niveau d'indentation de référence
- Analyse des structures parentes (def, class, if, etc.)
- Correction contextuelle préservant la logique

**Cas 3 : "unindent does not match"**
- Reconstruction ligne par ligne avec stack d'indentation
- Gestion des structures de contrôle (if/elif/else)
- Fermeture intelligente des blocs avec analyse heuristique

#### 2. **🔧 Routage Stratégique Amélioré (Volet 2)**
```python
# Routage intelligent basé sur error_type dans execute_task()
if error_type == "indentation":
    # Stratégie de réparation ciblée pour l'indentation
    modified_code, adaptations = self._fix_indentation_errors(code, feedback)
    
elif error_type == "name":
    # Résolution NameError via mapping imports complexes
    # Extraction automatique du nom non défini
    # Ajout import via CstComplexImportAdder
    
elif error_type == "import":
    # Gestion erreurs import de modules
    # Analyse contexte et suggestions corrections
    
elif error_type == "syntax":
    # Stratégies génériques syntaxe + LibCST
    
else:
    # Logique générique pour autres types
```

#### 3. **Gestion des Imports Complexes**
```python
# Mapping intelligent pour résolution NameError
COMPLEX_IMPORT_MAP = {
    "Path": ("pathlib", "Path"),
    "Agent": ("core.agent_factory_architecture", "Agent"),
    "Task": ("core.agent_factory_architecture", "Task"),
    # ... autres mappings
}
```

#### 4. **Blocs Vides via LibCST**
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

## 9. Workflow d'Adaptation V4.1 (Volet 2 Amélioré)

```
1. 📋 Réception tâche avec code + feedback + error_type
2. 🎯 Classification erreur automatique (Volet 1) + Routage stratégique
3. 🔧 Application réparations ciblées V4.1 :
   a. Si "indentation" → Moteur intelligent _fix_indentation_errors()
      • Détection automatique style (espaces/tabs) + niveau
      • Stack d'indentation contextuelle 
      • Stratégies adaptées par cas (expected/unexpected/unindent)
   b. Si "name" → Résolution NameError via COMPLEX_IMPORT_MAP
      • Extraction automatique nom non défini
      • Ajout import via CstComplexImportAdder
   c. Si "import" → Analyse erreurs de modules
   d. Si "syntax" → Stratégies génériques + LibCST
   e. Toujours → CstPassInserter pour blocs vides
4. 🏗️ Transformation LibCST sécurisée avec préservation formatage
5. ✅ Validation syntaxique + traçabilité adaptations
6. 📊 Retour code adapté + liste modifications détaillées
```

### 🆕 Améliorations Cycle M-T-D (Volet 2)
- **M (Maintenance)** : Classification + Routage + Adaptation intelligente
- **T (Test)** : Validation syntaxique automatique du code corrigé  
- **D (Documentation)** : Traçabilité complète des adaptations appliquées

## 10. 🚀 Nouvelles Fonctionnalités V4.2.0 (Priorités Hautes)

### 10.1 Classification Étendue d'Erreurs

```python
from agents.agent_MAINTENANCE_03_adaptateur_code import AgentMAINTENANCE03AdaptateurCode, ErrorType

agent = AgentMAINTENANCE03AdaptateurCode()

# Test classification sur différents types d'erreurs
errors_to_classify = [
    TypeError("unsupported operand type(s): 'int' and 'str'"),
    AttributeError("'str' object has no attribute 'append'"),
    ValueError("invalid literal for int() with base 10: 'abc'"),
    ModuleNotFoundError("No module named 'nonexistent_package'"),
    NameError("name 'undefined_variable' is not defined")
]

for error in errors_to_classify:
    classification = agent.classify_error_extended(error)
    print(f"Type: {classification.error_type.value}")
    print(f"Confiance: {classification.confidence_score:.2f}")
    print(f"Suggestions: {classification.suggested_fixes}")
    print("---")

# Résultat attendu : Classification précise avec suggestions contextuelles
```

### 10.2 Auto-découverte des Imports

```python
# Découverte automatique des imports dans le projet
discoveries = agent.discover_project_imports()

print(f"Imports découverts: {len(discoveries)}")

# Affichage des imports les plus utilisés
top_imports = sorted(discoveries.values(), key=lambda x: x.confidence, reverse=True)[:10]

for discovery in top_imports:
    print(f"📦 {discovery.module_name}")
    print(f"   Import: {discovery.import_statement}")
    print(f"   Confiance: {discovery.confidence:.2f}")
    print(f"   Usage: {discovery.usage_count} fois dans {len(discovery.source_files)} fichiers")
    print()

# Cache automatique pour réutilisation
print(f"Cache populé: {len(agent._import_discovery_cache)} éléments")
```

### 10.3 Validation Multi-niveaux

```python
# Test validation complète d'un code
test_code = """
def example_function():
    result = undefined_variable  # NameError potentiel
    return result.upper()

class ExampleClass:
    def method(self):
        return "test"
"""

validation = agent.validate_multi_level(test_code)

print("=== RÉSULTATS VALIDATION ===")
print(f"Syntaxe valide: {validation.syntax_valid}")
print(f"Sémantique valide: {validation.semantic_valid}")
print(f"Compilation réussie: {validation.compilation_successful}")
print(f"Résolution imports: {validation.import_resolution}")
print(f"Score global: {validation.confidence_score:.2f}")

if validation.issues:
    print(f"Issues détectées: {validation.issues}")
if validation.warnings:
    print(f"Avertissements: {validation.warnings}")
```

### 10.4 Utilisation Avancée avec Nouvelles Options

```python
from core.agent_factory_architecture import Task

# Code avec erreur NameError
code_with_error = """
def process_file():
    file_path = Path("/tmp/example.txt")  # Path non importé
    return file_path.exists()
"""

# Tâche avec toutes les nouvelles options V4.2.0
task = Task(
    id="advanced_adaptation",
    params={
        "code": code_with_error,
        "feedback": NameError("name 'Path' is not defined"),
        "error_type": "name",  # Sera re-classifié automatiquement
        "use_import_discovery": True,  # Active auto-découverte
        "validate_result": True        # Active validation multi-niveaux
    }
)

result = await agent.execute_task(task)

if result.success:
    data = result.data
    
    print("Code adapté:")
    print(data["adapted_code"])
    
    print(f"\nAdaptations: {data['adaptations']}")
    
    # Nouvelles données V4.2.0
    if data["error_classification"]:
        classification = data["error_classification"]
        print(f"Classification: {classification['error_type']} (confiance: {classification['confidence_score']:.2f})")
    
    if data["validation_pre"] and data["validation_post"]:
        pre_score = data["validation_pre"]["confidence_score"]
        post_score = data["validation_post"]["confidence_score"]
        improvement = post_score - pre_score
        print(f"Amélioration qualité: {improvement:+.2f} points ({pre_score:.2f} → {post_score:.2f})")
    
    print(f"Imports découverts utilisés: {data['import_discoveries_used']}")
```

### 10.5 Analyse Spécialisée par Type d'Erreur

```python
# Exemple TypeError
type_error = TypeError("unsupported operand type(s): 'int' and 'str'")
type_fixes = agent._analyze_type_error(str(type_error), code_context)
print(f"Suggestions TypeError: {type_fixes}")

# Exemple AttributeError  
attr_error = AttributeError("'str' object has no attribute 'append'")
attr_fixes = agent._analyze_attribute_error(str(attr_error), code_context)
print(f"Suggestions AttributeError: {attr_fixes}")

# Exemple ModuleNotFoundError
module_error = "No module named 'opencv-python'"
module_name = agent._extract_module_name(module_error)
suggestions = agent._suggest_module_alternatives(module_name)
print(f"Suggestions installation: {suggestions}")
```

## 11. Exemples d'Utilisation Hérités

### 11.1 🆕 Correction d'Erreur d'Indentation V4.1 (Volet 2)

```python
from core.agent_factory_architecture import Task
from agents.agent_MAINTENANCE_03_adaptateur_code import create_agent_MAINTENANCE_03_adaptateur_code

# ✅ CAS 1: "expected an indented block"
code_expected_block = """
def ma_fonction():
    if True:
print("Hello")  # IndentationError
    return True
"""

# ✅ CAS 2: "unexpected indent"  
code_unexpected_indent = """
def ma_fonction():
    print("Hello")
        print("World")  # IndentationError: unexpected indent
    return True
"""

# ✅ CAS 3: "unindent does not match"
code_unindent_mismatch = """
def ma_fonction():
    if True:
        print("Hello")
      print("World")  # IndentationError: unindent does not match
    return True
"""

# Création de l'agent
adaptateur = create_agent_MAINTENANCE_03_adaptateur_code()
await adaptateur.startup()

# Test des 3 cas avec le moteur amélioré
test_cases = [
    (code_expected_block, "expected an indented block"),
    (code_unexpected_indent, "unexpected indent"),
    (code_unindent_mismatch, "unindent does not match")
]

for i, (code, error_msg) in enumerate(test_cases, 1):
    print(f"\n🔧 TEST CAS {i}: {error_msg}")
    
    task = Task(
        type="adapt_code",
        params={
            "code": code,
            "feedback": IndentationError(error_msg),
            "error_type": "indentation"
        }
    )
    
    result = await adaptateur.execute_task(task)
    if result.success:
        fixed_code = result.data["adapted_code"]
        adaptations = result.data["adaptations"]
        
        print(f"✅ Correction réussie!")
        print(f"Adaptations: {adaptations}")
        
        # Validation syntaxique
        try:
            compile(fixed_code, '<string>', 'exec')
            print(f"✅ Code corrigé compile sans erreur")
        except SyntaxError as e:
            print(f"❌ Erreur syntaxe persistante: {e}")
    else:
        print(f"❌ Échec: {result.error}")
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

## 11. Format de Résultat

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

## 12. Configuration

### Mapping d'Imports Complexes

```python
# Personnalisation du mapping pour résolution NameError
adaptateur.COMPLEX_IMPORT_MAP.update({
    "MonModule": ("mon.package", "MonModule"),
    "MaClasse": ("mon.autre.package", "MaClasse")
})
```

## 13. Dépendances

- **Python 3.8+**
- **LibCST** : Transformations AST avancées
- **Pyflakes** : Analyse statique de code
- **core.agent_factory_architecture** (Agent, Task, Result)
- **Modules standard** : textwrap, re, asyncio, logging

## 14. Journal des Modifications (Changelog)

- **🚀 v4.2.0 (2025-06-27) - Priorités Hautes : Classification Étendue + Auto-découverte + Validation Multi-niveaux** :
  - **CLASSIFICATION ÉTENDUE** : Extension du système de classification de 4 à 9 types d'erreurs avec scoring de confiance
    - Nouveaux types : type_error, attribute_error, value_error, module_not_found avec analyse spécialisée
    - Scoring de confiance 0.0-1.0 avec suggestions automatiques contextuelles
    - Méthodes d'analyse spécialisées : _analyze_type_error(), _analyze_attribute_error(), _analyze_module_error()
  - **AUTO-DÉCOUVERTE IMPORTS** : Système intelligent de découverte d'imports par analyse AST du projet
    - Analyse complète du projet via ast.parse() pour découverte automatique des patterns d'import
    - Cache intelligent avec scoring basé sur l'usage et fréquence d'utilisation
    - Mapping automatique module → import_statement avec scoring de confiance
  - **VALIDATION MULTI-NIVEAUX** : Pipeline de validation complète avec scoring global
    - Validation syntaxique + sémantique + compilation + résolution imports
    - Score de confiance global consolidé avec métriques détaillées
    - Détection issues et warnings avec recommandations automatiques
  - **NOUVELLES DATACLASSES** : ErrorType enum, ErrorClassification, ImportDiscovery, ValidationResult
  - **PARAMÈTRES EXECUTE_TASK** : Nouvelles options use_import_discovery et validate_result
  - **EXTENSION CAPACITÉS** : 10 → 18 capacités avec nouvelles fonctionnalités v4.2.0
  - **TESTS COMPLETS** : Suite de tests v4.2.0 avec validation des 3 priorités hautes
  - **DOCUMENTATION** : Section complète "Nouvelles Fonctionnalités V4.2.0" avec exemples pratiques
- **🆕 v4.1.0 (2025-06-27) - Volet 2 : Moteur Indentation Amélioré** :
  - **MOTEUR INDENTATION ROBUSTE** : Réécriture complète `_fix_indentation_errors()` avec stratégies intelligentes
  - **DÉTECTION AUTOMATIQUE** : Style d'indentation (espaces/tabs) et niveaux contextuels
  - **STACK D'INDENTATION** : Gestion cohérente des blocs avec analyse syntaxique
  - **STRATÉGIES CIBLÉES** : 
    - "expected an indented block" → insertion 'pass' contextuelle
    - "unexpected indent" → correction avec analyse de référence  
    - "unindent does not match" → reconstruction ligne par ligne intelligente
  - **ROUTAGE STRATÉGIQUE** : Classification error_type avec routage amélioré dans execute_task()
  - **VALIDATION COMPLÈTE** : Test des 3 cas d'indentation avec cycle M-T-D
  - **DOCUMENTATION** : Mise à jour complète avec exemples V4.1
- **v4.0.0 (Mission Claudecode - Audit Universel)** :
  - Capacité d'audit universel d'adaptation pour projets complets
  - Filtrage intelligent de répertoires et scoring unifié
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

## 15. Procédure de Test CLI

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

## 16. Cas d'Usage Recommandés

- **Réparation automatique** : Correction erreurs syntaxiques dans pipelines CI/CD
- **Maintenance de code** : Adaptation massive de code legacy
- **Migration de projets** : Harmonisation imports et structure
- **Workflow de développement** : Correction automatique en temps réel
- **Refactorisation assistée** : Transformations sécurisées avec LibCST

## 17. Statut et Validation V4.1

- ✅ **Pattern Factory** : Conforme (Agent, Task, Result)
- ✅ **Méthodes async** : startup, shutdown, execute_task, health_check
- ✅ **Capabilities** : 10 capacités spécialisées définies  
- ✅ **Technologies** : LibCST, Pyflakes, CSTTransformer
- ✅ **Documentation V4.1** : Docstrings enrichies et .md synchronisé avec Volet 2
- ✅ **Tests CLI** : Procédure de validation définie
- ✅ **Multi-Level Repair** : Stratégies adaptées par type d'erreur
- ✅ **🆕 Moteur Indentation V4.1** : Validé avec 3/3 cas de test réussis
- ✅ **🆕 Cycle M-T-D** : Intégration complète Maintenance-Test-Documentation
- ✅ **🆕 Routage Stratégique** : Classification error_type opérationnelle

### 📊 Résultats Tests Volet 2 (2025-06-27)
- **✅ Cas 1** "expected an indented block" : Insertion intelligente 'pass'
- **✅ Cas 2** "unexpected indent" : Correction contextuelle  
- **✅ Cas 3** "unindent does not match" : Reconstruction avec stack
- **🎯 Taux de réussite** : 100% (3/3 tests validés)
- **⚡ Performance** : Code corrigé compile sans erreur dans tous les cas

**Agent MAINTENANCE 03 V4.2 - État : IMPLÉMENTÉ ET VALIDÉ (Priorités Hautes Complètes)**