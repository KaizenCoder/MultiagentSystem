# Agent MAINTENANCE 06 – Correcteur Logique Métier

## 1. Identification

- **Nom :** Correcteur Logique Métier NextGeneration
- **Identifiant :** `agent_MAINTENANCE_06_correcteur_logique_metier`
- **Version :** 7.1.0 (Logging Uniforme + Audit Universel)
- **Responsable Principal :** Équipe de Maintenance NextGeneration
- **Contact Technique :** `#canal-maintenance-ia`

## 2. Mission et Capacités
### 2.1 Mission Principale
Agent spécialisé dans la correction et la validation de la logique métier avec capacités d'audit universel :
- Validation des patterns métier sur fichiers individuels ou projets complets
- Correction des erreurs de logique
- Vérification de la cohérence des règles métier
- Test des patterns business
- Optimisation du code métier

**🚀 NOUVEAUTÉ V7.1 (Travaux claudecode) :** Intégration complète du système de logging uniforme + capacité d'audit universel de la logique métier étendue pour analyser des **projets Python complets** (répertoires entiers) en plus des fichiers individuels.

### 🔧 Système de Logging Uniforme V7.1
```python
# ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ (claudecode)
try:
    from core.manager import LoggingManager
    logging_manager = LoggingManager()
    self.logger = logging_manager.get_logger(
        config_name="maintenance",
        custom_config={
            "logger_name": f"nextgen.maintenance.correcteur_logique_metier.{self.id}",
            "log_dir": "logs/maintenance/correcteur",
            "metadata": {
                "agent_type": "MAINTENANCE_06_correcteur_logique_metier",
                "agent_role": "correcteur_logique_metier",
                "system": "nextgeneration"
            }
        }
    )
except ImportError:
    # Fallback en cas d'indisponibilité du LoggingManager
    self.logger = logging.getLogger(self.__class__.__name__)
```

### 2.2 Capacités Techniques

#### Capacités d'Audit Universel (V7.0)
- **Audit de fichiers individuels** : Analyse et correction de la logique métier d'un fichier Python spécifique
- **🆕 Audit de répertoires complets** : Analyse récursive de la logique métier de structures de projets entières
- **Filtrage intelligent** : Exclusion automatique des répertoires non pertinents (.venv, __pycache__, .git, etc.)
- **Rapports consolidés** : Métriques de qualité logique globales + détails par fichier
- **Scoring unifié** : Système de notation de qualité logique cohérent (0-100)

#### Capacités d'Analyse Logique
- Analyse AST du code Python
- Validation des patterns métier
- Détection des anti-patterns
- Tests de validation des règles métier
- Intégration avec le Pattern Factory
- Génération de rapports détaillés

## 3. Architecture V7.0 (Mission Claudecode)

### 3.1 Architecture Technique
- **Orchestrateur Central** : `audit_universal_logique` coordonne tous les types d'audit
- **Audit Fichier Unique** : `_audit_single_python_file` pour l'analyse détaillée de la logique métier
- **Filtrage Intelligent** : `_should_skip_path` pour ignorer les répertoires non pertinents
- **Mapping Qualité** : `_map_score_to_logic_health` pour la notation uniforme
- **Gestion Consolidée** : Centralisation des métriques et scoring dans l'orchestrateur

### 3.2 Métriques de Qualité Logique
```python
logic_metrics = {
    'pattern_compliance': {'weight': 0.3, 'threshold': {'warning': 70, 'critical': 50}},
    'semantic_correctness': {'weight': 0.3, 'threshold': {'warning': 75, 'critical': 60}},
    'anti_pattern_absence': {'weight': 0.2, 'threshold': {'warning': 80, 'critical': 65}},
    'business_rule_compliance': {'weight': 0.2, 'threshold': {'warning': 85, 'critical': 70}}
}
```

## 4. Guide d'Utilisation

### 4.1 Initialisation
```python
from agents.agent_MAINTENANCE_06_correcteur_logique_metier import AgentMAINTENANCE06CorrecteurLogiqueMetier
agent = AgentMAINTENANCE06CorrecteurLogiqueMetier()
await agent.startup()
```

### 4.2 Audit d'un Fichier Individuel
```python
# Audit de la logique métier d'un fichier Python spécifique
task_details = {
    "action": "audit_universal_logique",
    "params": {
        "target_path": "chemin/vers/votre/fichier.py"
    }
}
result = await agent.execute_task(task_details)
print(f"Score qualité logique : {result['data']['score_global']}/100")
print(f"État de la logique métier : {result['data']['etat_logique']}")
```

### 4.3 🆕 Audit d'un Projet Complet (V7.0)
```python
# Audit de la logique métier d'un répertoire complet
task_details = {
    "action": "audit_universal_logique",
    "params": {
        "target_path": "chemin/vers/votre/projet/"
    }
}
result = await agent.execute_task(task_details)

# Résultats consolidés
print(f"Nombre de fichiers analysés : {result['data']['nb_fichiers_analyses']}")
print(f"Score global de qualité logique : {result['data']['score_global']}/100")
print(f"État global de la logique métier : {result['data']['etat_logique']}")

# Détails par fichier
for fichier_result in result['data']['resultats_fichiers']:
    print(f"- {fichier_result['fichier']} :")
    print(f"  Score : {fichier_result['score']}/100")
    print(f"  Problèmes logiques : {len(fichier_result['logic_issues'])}")
```

## 5. Spécifications Techniques V7.0

### 5.1 Méthodes Principales
- **`audit_universal_logique(target_path)`** : Orchestrateur principal (fichier ou répertoire)
- **`_audit_single_python_file(file_path)`** : Audit détaillé de la logique d'un fichier
- **`_should_skip_path(path)`** : Filtrage intelligent des chemins à ignorer
- **`_map_score_to_logic_health(score)`** : Mapping score → état de la logique

### 5.2 Filtrage Intelligent
Répertoires automatiquement ignorés :
- `.venv/`, `venv/`, `env/` (environnements virtuels)
- `__pycache__/`, `.pyc` (cache Python)
- `.git/`, `.svn/` (contrôle de version)
- `node_modules/`, `.npm/` (dépendances JS)
- `build/`, `dist/`, `.egg-info/` (artefacts de build)

### 5.3 Métriques de Qualité Logique
- **Score global** : Note consolidée 0-100
- **Nombre de fichiers** : Fichiers Python analysés
- **Problèmes logiques** : Issues détectées par type
- **Patterns métier** : Conformité aux patterns
- **Anti-patterns** : Violations détectées
- **Règles business** : Respect des règles métier

## 6. Utilisation
### 6.1 Initialisation
```python
agent = AgentMAINTENANCE06CorrecteurLogiqueMetier()
await agent.startup()
```

### 6.2 Types de Tâches Supportées
- `validate_business_patterns`: Validation des patterns métier
- `correct_logic`: Correction de la logique
- `test_patterns`: Test des patterns implémentés

### 6.3 Exemple d'Utilisation
```python
task = Task(
    id="test_patterns",
    type="validate_business_patterns",
    params={"code": problematic_code}
)
result = await agent.execute_task(task)
```

## 7. Maintenance et Évolution
### 7.1 Journal des Modifications
- **v6.1.0** : Harmonisation avec les standards Pattern Factory NextGeneration
- **v6.0.0** : Refonte majeure avec support AST et patterns métier
- **v5.0.0** : Ajout de la validation des patterns

### 7.2 Dépendances
- Python 3.9+
- `core.agent_factory_architecture`
- Modules standards Python (ast, sys, typing)

### 7.3 Tests
Tests disponibles dans `tests/business_logic/`

## 8. Intégration
### 8.1 Configuration
Configuration via `maintenance_config.json` :
```json
{
    "agent_type": "business_logic_corrector",
    "version": "6.1.0",
    "status": "enabled"
}
```

### 8.2 Logging
Utilise le système de logging centralisé de l'équipe de maintenance.

## 9. Support et Contact
- Canal Slack : `#canal-maintenance-ia`
- Documentation : `/docs/business-logic/`
- Wiki : `wiki/agents/business-logic-corrector`

## 10. Description Générale

🔧 Agent spécialisé dans la correction et validation de la logique métier Python, détection d'incohérences sémantiques et application de patterns métier robustes pour garantir la qualité architecturale et la cohérence du code.

Cet agent utilise des techniques avancées d'analyse AST, de pattern matching et de validation sémantique pour identifier et corriger les problèmes de logique métier.

## 11. Objectifs et Missions

- **Correction Logique Métier :** Détection et correction automatique d'erreurs logiques courantes
- **Validation Patterns :** Vérification conformité aux patterns métier (Factory, Strategy, Observer)
- **Analyse Sémantique :** Détection d'incohérences sémantiques et problèmes de design
- **Anti-Pattern Detection :** Identification et correction d'anti-patterns (God Class, Magic Numbers)
- **Support Équipe Maintenance :** Audit conformité métier avec scoring et recommandations

## 12. Fonctionnalités Clés (Conformité Pattern Factory)

L'agent respecte le Pattern Factory NextGeneration et expose les méthodes suivantes :

- **`startup()`** : Initialise l'agent correcteur logique métier
- **`health_check()`** : Vérifie l'état de santé. Retourne `{"status": "healthy"}` en fonctionnement normal
- **`execute_task(task: Task)`** : Point d'entrée principal pour correction et validation logique
  - **Action `correct_business_logic`** :
    - **`task.params` attendus** :
      - `code` (str) : Code source Python à analyser et corriger
      - `file_path` (str, optionnel) : Chemin fichier pour contexte
    - **Résultat** : Analyse des problèmes, corrections et code corrigé
  - **Action `validate_business_patterns`** :
    - **`task.params` attendus** :
      - `code` (str) : Code source à analyser pour patterns métier
    - **Résultat** : Patterns trouvés, manquants et recommandations
  - **Action `detect_logic_inconsistencies`** :
    - **`task.params` attendus** :
      - `code` (str) : Code source à analyser pour incohérences
    - **Résultat** : Liste incohérences avec classification par sévérité
  - **Action `audit_business_compliance`** :
    - **`task.params` attendus** :
      - `code` (str) : Code source à auditer
      - `rules` (list, optionnel) : Règles métier spécifiques
    - **Résultat** : Score conformité, violations et recommandations
- **`shutdown()`** : Arrête l'agent proprement

### Capacités Spécialisées

```python
get_capabilities() -> [
    "correct_business_logic",
    "validate_business_patterns",
    "detect_logic_inconsistencies", 
    "analyze_semantic_correctness",
    "fix_anti_patterns",
    "validate_api_design",
    "check_error_handling",
    "verify_null_safety",
    "audit_business_compliance",
    "generate_logic_improvements"
]
```

## 13. Technologies Avancées

### Analyse AST Sémantique
- **Parsing avancé** pour détection patterns et anti-patterns
- **Validation architecturale** avec détection violations design
- **Metrics automatiques** (longueur méthodes, complexité, imbrication)

```python
# Analyse patterns métier
business_patterns = {
    "factory_pattern": ["create_", "build_", "make_"],
    "validation_pattern": ["validate_", "check_", "verify_"],
    "error_handling": ["try:", "except", "raise"],
    "null_safety": ["if not", "is None", "assert"]
}
```

### Structure LogicIssue
```python
@dataclass
class LogicIssue:
    severity: str           # CRITICAL, HIGH, MEDIUM, LOW
    issue_type: str         # logic_error, semantic_issue, pattern_violation
    description: str        # Description du problème
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None
```

### Détection Anti-Patterns
```python
# Anti-patterns à éviter
anti_patterns = {
    "god_class": "Classes avec trop de responsabilités",
    "magic_numbers": "Nombres magiques sans constantes", 
    "deep_nesting": "Imbrication trop profonde",
    "long_methods": "Méthodes trop longues (>50 lignes)"
}
```

## 14. Workflow de Correction Logique

```
1. 📋 Réception code source via execute_task
2. 🔍 Analyse AST pour détection patterns et violations
3. 📊 Classification problèmes par sévérité (CRITICAL→LOW)
4. 🔧 Génération corrections automatiques si possible
5. 📝 Création suggestions d'amélioration architecture
6. 📄 Retour rapport structuré avec code corrigé
```

## 15. Exemples d'Utilisation

### Correction de Logique Métier

```python
from core.agent_factory_architecture import Task
from agents.agent_MAINTENANCE_06_correcteur_logique_metier import create_agent_MAINTENANCE_06_correcteur_logique_metier

# Code avec problèmes logiques
problematic_code = '''
def process_data(data):
    result = data * 42  # Nombre magique
    return result

class DataProcessor:  # Pas de docstring
    def __init__(self):
        pass
        
    def long_method(self, x, y, z, a, b, c, d, e, f, g):  # Trop de paramètres
        if x > 0:
            if y > 0:
                if z > 0:  # Imbrication profonde
                    if a > 0:
                        return x + y + z + a
        return 0  # Pas de gestion d'erreurs
'''

# Création de l'agent
correcteur = create_agent_MAINTENANCE_06_correcteur_logique_metier()
await correcteur.startup()

# Correction logique métier
task = Task(
    type="correct_business_logic",
    params={
        "code": problematic_code,
        "file_path": "business_logic.py"
    }
)

result = await correcteur.execute_task(task)
if result.success:
    print(f"🔧 Problèmes détectés: {result.data['issues_detected']}")
    for issue in result.data['issues']:
        print(f"  • {issue['severity']}: {issue['description']} (L{issue['line']})")
        print(f"    Suggestion: {issue['suggestion']}")
```

### Validation de Patterns Métier

```python
# Code à analyser pour patterns
business_code = '''
class UserFactory:
    @staticmethod
    def create_user(email, name):
        user = User(email, name)
        user.validate_email()
        return user

class User:
    def __init__(self, email, name):
        self.email = email
        self.name = name
    
    def validate_email(self):
        if "@" not in self.email:
            raise ValueError("Email invalide")
'''

# Validation patterns
task = Task(
    type="validate_business_patterns",
    params={"code": business_code}
)

result = await correcteur.execute_task(task)
if result.success:
    data = result.data
    print(f"📋 Patterns trouvés: {data['patterns_found']}")
    print(f"📋 Patterns manquants: {data['missing_patterns']}")
    for rec in data['recommendations']:
        print(f"💡 {rec}")
```

### Audit de Conformité Métier

```python
# Audit avec règles spécifiques
task = Task(
    type="audit_business_compliance",
    params={
        "code": business_code,
        "rules": [
            "functions_must_have_docstrings",
            "classes_must_have_docstrings", 
            "error_handling_required",
            "no_magic_numbers"
        ]
    }
)

result = await correcteur.execute_task(task)
if result.success:
    audit_data = result.data
    print(f"📊 Score conformité: {audit_data['compliance_score']}/100")
    print(f"⚠️ Violations: {len(audit_data['violations'])}")
    for violation in audit_data['violations']:
        print(f"  • {violation}")
```

### Détection d'Incohérences Logiques

```python
# Code avec incohérences
inconsistent_code = '''
import unused_module
from datetime import datetime

def calculate_age(birth_date):
    # Variable créée mais jamais utilisée
    current_year = 2025
    age = 2025 - birth_date.year  # Année codée en dur
    return age
'''

task = Task(
    type="detect_logic_inconsistencies",
    params={"code": inconsistent_code}
)

result = await correcteur.execute_task(task)
if result.success:
    data = result.data
    print(f"🔍 Incohérences: {data['inconsistencies_count']}")
    severity_breakdown = data['severity_breakdown']
    for severity, count in severity_breakdown.items():
        if count > 0:
            print(f"  {severity}: {count}")
```

## 16. Format de Résultat

### Correction de Logique Métier

```json
{
  "success": true,
  "data": {
    "issues_detected": 4,
    "issues": [
      {
        "type": "pattern_violation",
        "severity": "LOW",
        "description": "Nombre magique détecté: 42",
        "line": 2,
        "suggestion": "Remplacer par une constante nommée"
      },
      {
        "type": "pattern_violation", 
        "severity": "MEDIUM",
        "description": "Méthode 'long_method' trop longue (15 statements)",
        "line": 8,
        "suggestion": "Diviser en méthodes plus petites pour améliorer la lisibilité"
      },
      {
        "type": "logic_error",
        "severity": "HIGH", 
        "description": "Méthode 'long_method' sans gestion d'erreurs",
        "line": 8,
        "suggestion": "Ajouter try/except pour la robustesse"
      }
    ],
    "corrections": {
      "code": "# Code corrigé avec améliorations...",
      "corrections_applied": [],
      "corrections_count": 0
    },
    "corrected_code": "# Code avec corrections appliquées"
  }
}
```

### Validation de Patterns

```json
{
  "success": true,
  "data": {
    "patterns_found": ["factory_pattern", "validation_pattern"],
    "missing_patterns": ["error_handling", "null_safety"],
    "recommendations": [
      "Considérer l'implémentation du pattern error_handling",
      "Considérer l'implémentation du pattern null_safety"
    ]
  }
}
```

### Audit de Conformité

```json
{
  "success": true,
  "data": {
    "compliance_score": 70,
    "violations": [
      "Fonction 'process_data' sans docstring (ligne 1)",
      "Classe 'DataProcessor' sans docstring (ligne 5)"
    ],
    "recommendations": [
      "Ajouter des docstrings pour améliorer la documentation",
      "Implémenter une gestion d'erreurs robuste"
    ],
    "rules_checked": [
      "functions_must_have_docstrings",
      "classes_must_have_docstrings",
      "error_handling_required",
      "no_magic_numbers"
    ]
  }
}
```

## 17. Capacités d'Analyse Avancées

### Détection Méthodes Longues
```python
# Analyse des méthodes et fonctions
for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        if len(node.body) > 20:  # Seuil configurable
            issues.append(LogicIssue(
                severity="MEDIUM",
                issue_type="pattern_violation",
                description=f"Méthode '{node.name}' trop longue",
                suggestion="Diviser en méthodes plus petites"
            ))
```

### Validation Gestion d'Erreurs
```python
# Vérification gestion d'erreurs
has_error_handling = any(
    isinstance(n, ast.Try) for n in ast.walk(node)
)
if not has_error_handling and len(node.body) > 5:
    issues.append(LogicIssue(
        severity="HIGH",
        issue_type="logic_error",
        description=f"Méthode '{node.name}' sans gestion d'erreurs",
        suggestion="Ajouter try/except pour la robustesse"
    ))
```

### Détection Nombres Magiques
```python
# Détection de nombres magiques
elif isinstance(node, ast.Num) and isinstance(node.n, (int, float)):
    if node.n not in [0, 1, -1]:  # Exceptions communes
        issues.append(LogicIssue(
            severity="LOW", 
            issue_type="pattern_violation",
            description=f"Nombre magique détecté: {node.n}",
            suggestion="Remplacer par une constante nommée"
        ))
```

## 18. Dépendances

- **Python 3.7+**
- **core.agent_factory_architecture** (Agent, Task, Result)
- **Modules standard** : ast, inspect, re, logging, asyncio, dataclasses
- **Typing** : Annotations et structures typées pour classification

## 19. Journal des Modifications (Changelog)

- **v6.1.0 (2025-06-26)** :
  - Harmonisation avec standards Pattern Factory NextGeneration
  - Enrichissement docstrings classe avec description détaillée capacités logique métier
  - Extension `get_capabilities()` : 1 → 10 capacités spécialisées
  - Implémentation complète analyse AST, patterns métier et anti-patterns
  - Ajout dataclass LogicIssue pour classification structurée
  - Documentation .md complètement refaite avec exemples techniques
- **Versions antérieures** : Structure basique sans fonctionnalités avancées

## 20. Tests et Validation

### Test Intégré

L'agent inclut un test principal complet :

```python
# Test avec code problématique volontaire
problematic_code = '''
def process_data(data):
    result = data * 42  # Nombre magique
    return result

class DataProcessor:  # Pas de docstring
    def __init__(self):
        pass
        
    def long_method(self, x, y, z, a, b, c, d, e, f, g):  # Trop de paramètres
        if x > 0:
            if y > 0:
                if z > 0:  # Imbrication profonde
                    if a > 0:
                        return x + y + z + a
        return 0  # Pas de gestion d'erreurs
'''

# Tests correction, patterns, conformité
await agent.execute_task(correction_task)
await agent.execute_task(patterns_task)
await agent.execute_task(compliance_task)
```

### Exécution des Tests

```bash
# Test direct de l'agent
python agents/agent_MAINTENANCE_06_correcteur_logique_metier.py

# Output attendu :
# 🚀 Démarrage des tests...
# 🏥 Health Check: {'status': 'healthy'}
# 🛠️ Capabilities: ['correct_business_logic', 'validate_business_patterns', ...]
# 🔧 Test correction logique: Problèmes détectés: 4
# 🎯 Test validation patterns: Patterns trouvés/manquants
```

## 21. Cas d'Usage Recommandés

- **Code Review** : Validation automatique logique métier dans PRs
- **Refactoring** : Détection anti-patterns avant refactorisation
- **Quality Gates** : Audit conformité avant déploiement  
- **Technical Debt** : Identification problèmes de design systematiques
- **Architecture Validation** : Vérification respect patterns métier

## 22. Statut et Validation

- ✅ **Pattern Factory** : Conforme (Agent, Task, Result)
- ✅ **Méthodes async** : startup, shutdown, execute_task, health_check
- ✅ **Capabilities** : 10 capacités spécialisées définies
- ✅ **Technologies** : AST analysis, pattern matching, dataclasses
- ✅ **Documentation** : Docstrings enrichies et .md synchronisé
- ✅ **Tests Intégrés** : Validation complète avec code problématique
- ✅ **Logique Métier** : Analyse sémantique et correction automatique

**Agent MAINTENANCE 06 - État : PRÊT POUR VALIDATION**