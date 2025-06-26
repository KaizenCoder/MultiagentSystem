# Agent MAINTENANCE 05 – Documenteur Peer Reviewer

## 1. Identification

- **Nom :** Documenteur Peer Reviewer NextGeneration
- **Identifiant :** `agent_MAINTENANCE_05_documenteur_peer_reviewer`
- **Version :** 5.2.0 (Harmonisation Standards Pattern Factory NextGeneration)
- **Responsable Principal :** Équipe de Maintenance NextGeneration
- **Contact Technique :** `#canal-maintenance-ia`

## 2. Description Générale

📋 Agent spécialisé dans la génération de rapports de mission de maintenance détaillés, audit universel de qualité de code et peer-review automatisé avec analyses AST avancées pour garantir la documentation et qualité du code.

Cet agent combine des technologies de génération de rapports, d'audit de code et d'analyse syntaxique pour produire des documentations complètes et des évaluations de qualité.

## 3. Objectifs et Missions

- **Génération Rapports :** Production de rapports de mission de maintenance détaillés avec métriques et analyses
- **Audit Universel :** Évaluation complète de la qualité de code via Flake8 et analyse AST
- **Peer-Review Automatisé :** Classification automatique des problèmes avec scoring intelligent
- **Documentation Enrichie :** Génération Markdown avec diff, historique et conclusions synthétiques
- **Support Équipe Maintenance :** Intégration CI/CD avec rapports standardisés

## 4. Fonctionnalités Clés (Conformité Pattern Factory)

L'agent respecte le Pattern Factory NextGeneration et expose les méthodes suivantes :

- **`startup()`** : Initialise l'agent documenteur peer reviewer
- **`health_check()`** : Vérifie l'état de santé. Retourne `{"status": "healthy", "version": "5.2.0"}` en fonctionnement normal
- **`execute_task(task: Task)`** : Point d'entrée principal pour génération rapports et audits
  - **Action `generate_mission_report`** :
    - **`task.params` attendus** :
      - `report_data` (dict) : Données de mission avec résultats par agent
    - **Résultat** : Contenu Markdown du rapport enrichi
  - **Action `audit_universal_quality`** :
    - **`task.params` attendus** :
      - `file_path` (str) : Chemin du fichier Python à auditer
    - **Résultat** : Rapport d'audit avec score qualité et problèmes détectés
- **`shutdown()`** : Arrête l'agent proprement

### Capacités Spécialisées

```python
get_capabilities() -> [
    "generate_mission_report",
    "audit_universal_quality", 
    "peer_review_automation",
    "markdown_report_generation",
    "flake8_quality_audit",
    "ast_analysis_advanced",
    "diff_generation_unified",
    "quality_scoring_intelligent",
    "issue_classification_severity",
    "mission_conclusion_synthesis"
]
```

## 5. Technologies Avancées

### Audit Flake8 Asynchrone
- **Exécution subprocess async** sans blocage
- **Parsing robuste** compatible Windows/Unix paths
- **Classification automatique** des erreurs par sévérité

```python
# Exécution Flake8 avec parsing intelligent
process = await asyncio.create_subprocess_shell(
    f'flake8 "{clean_file_path}"', 
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
```

### Analyse AST Avancée
```python
# Détection docstrings et métriques
tree = ast.parse(code)
has_module_d = _has_module_docstring_manual(tree)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        if not ast.get_docstring(node):
            # Classification problème docstring
```

### Structure UniversalQualityIssue
```python
@dataclass
class UniversalQualityIssue:
    severity: str          # CRITICAL, HIGH, MEDIUM, LOW
    description: str       # Description problème
    code: str             # Code erreur (ex: F401, E501)
    details: Optional[Any] # Détails supplémentaires
    line: Optional[int]    # Numéro de ligne
    column: Optional[int]  # Numéro de colonne
```

### Génération Diff Unified
```python
# Comparaison code original vs corrigé
diff = difflib.unified_diff(
    original_code.splitlines(keepends=True),
    final_code.splitlines(keepends=True),
    fromfile='original', tofile='corrected'
)
```

## 6. Workflow d'Audit et Documentation

```
1. 📋 Réception tâche (mission_report ou audit_quality)
2. 🔍 Si audit: Lecture fichier et lancement Flake8 + AST en parallèle
3. 📊 Consolidation résultats avec scoring intelligent
4. 📝 Si rapport: Génération Markdown enrichi avec diff et métriques
5. 🎯 Classification problèmes par sévérité et recommandations
6. 📄 Retour rapport structuré (JSON + Markdown)
```

## 7. Exemples d'Utilisation

### Génération Rapport de Mission

```python
from core.agent_factory_architecture import Task
from agents.agent_MAINTENANCE_05_documenteur_peer_reviewer import create_agent_MAINTENANCE_05_documenteur_peer_reviewer

# Données de mission exemple
mission_data = {
    "mission_id": "MAINT_2025_001",
    "statut_mission": "COMPLETED",
    "duree_totale_sec": 45.6,
    "equipe_maintenance_roles": ["MAINTENANCE_01", "MAINTENANCE_02", "MAINTENANCE_03"],
    "resultats_par_agent": [
        {
            "agent_name": "MAINTENANCE_01_analyseur_structure",
            "agent_mission": "Analyse structure et conformité",
            "status": "NO_REPAIR_NEEDED",
            "initial_evaluation": {"score": 85, "reason": "Structure conforme"},
            "performance_analysis": {"score": 92}
        },
        {
            "agent_name": "MAINTENANCE_02_evaluateur_utilite", 
            "agent_mission": "Évaluation utilité et scoring",
            "status": "REPAIRED",
            "original_code": "def old_function():\\n    pass",
            "final_code": "def new_function():\\n    \"\"\"Docstring added.\"\"\"\\n    pass",
            "repair_history": [
                {
                    "iteration": 1,
                    "error_detected": "Missing docstring",
                    "adaptation_attempted": ["Add docstring"],
                    "test_result": "SUCCESS"
                }
            ]
        }
    ]
}

# Création de l'agent
documenteur = create_agent_MAINTENANCE_05_documenteur_peer_reviewer()
await documenteur.startup()

# Génération rapport
task = Task(
    type="generate_mission_report",
    params={"report_data": mission_data}
)

result = await documenteur.execute_task(task)
if result.success:
    md_content = result.data["md_content"]
    print("📋 Rapport généré:")
    print(md_content)
```

### Audit Universel de Qualité

```python
# Audit d'un fichier Python
task = Task(
    type="audit_universal_quality",
    params={"file_path": "agents/my_agent.py"}
)

result = await documenteur.execute_task(task)
if result.success:
    audit_report = result.data["audit_report"]
    print(f"📊 Score qualité: {audit_report['quality_score']}/100")
    print(f"🔍 Problèmes trouvés: {audit_report['summary']['total_issues']}")
    
    for issue in audit_report["issues"]:
        line_info = f"L{issue['line']}" if issue.get('line') else "Global"
        print(f"  • {line_info}: [{issue['code']}] {issue['description']} ({issue['severity']})")
```

### Test avec Fichier Problématique

```python
# Code avec problèmes volontaires
problematic_code = '''
def hello_world(): # Missing docstring
    print("Hello, world!")

class MyClass: # Missing docstring  
    def __init__(self): # Missing docstring
        self.value = 10

def too_many_params(a,b,c,d,e,f,g,h,i,j,k,l): # Too many arguments
    pass # Missing docstring
'''

# Écriture fichier temporaire
test_file = Path("temp_audit_test.py")
test_file.write_text(problematic_code)

# Audit
task = Task(
    type="audit_universal_quality", 
    params={"file_path": str(test_file)}
)

result = await documenteur.execute_task(task)
# Résultat : Score réduit, problèmes Flake8 + AST détectés

# Nettoyage
test_file.unlink()
```

## 8. Format de Résultat

### Rapport de Mission (Markdown)

```markdown
# Rapport de Mission de Maintenance : `MAINT_2025_001`
**Statut Final :** COMPLETED | **Durée :** 45.60s

## Équipe de Maintenance Active
- `MAINTENANCE_01`
- `MAINTENANCE_02` 
- `MAINTENANCE_03`

---

## Résultats Détaillés par Agent

### ✅ Agent : `MAINTENANCE_01_analyseur_structure`
- **Mission de l'agent :** *Analyse structure et conformité*
- **Statut Final :** NO_REPAIR_NEEDED
- **Évaluation Initiale :** Score de 85/100. (Raison: Structure conforme)
- **Analyse de Performance :** Score de 92/100.

### ✅ Agent : `MAINTENANCE_02_evaluateur_utilite`
- **Mission de l'agent :** *Évaluation utilité et scoring*
- **Statut Final :** REPAIRED
- **Diff des Modifications :**
  ```diff
  -def old_function():
  +def new_function():
  +    """Docstring added."""
       pass
  ```

## Conclusion de la Mission
La mission est un succès total. L'ensemble des 2 agents traités sont stables et opérationnels. 1 agents ont été réparés avec succès.
```

### Audit Universel (JSON)

```json
{
  "file_path": "agents/my_agent.py",
  "quality_score": 72,
  "metrics_ast": {
    "total_lines": 45,
    "total_functions": 6,
    "total_classes": 2,
    "module_docstring": "❌ Non",
    "functions_no_docstring": 3
  },
  "issues": [
    {
      "severity": "HIGH",
      "description": "Docstring de module manquant.",
      "code": "MISSING_MODULE_DOCSTRING",
      "line": null,
      "column": null
    },
    {
      "severity": "MEDIUM", 
      "description": "3 fonction(s) sans docstring.",
      "code": "MISSING_FUNCTION_DOCSTRING",
      "details": [
        {"function": "hello_world", "line": 2},
        {"function": "__init__", "line": 6},
        {"function": "process", "line": 12}
      ]
    },
    {
      "severity": "MEDIUM",
      "description": "E501 line too long (82 > 79 characters)",
      "code": "E501",
      "line": 15,
      "column": 80
    }
  ],
  "summary": {
    "total_issues": 3,
    "flake8_issues": 1,
    "ast_issues": 2
  }
}
```

## 9. Capacités d'Analyse Avancées

### Audit Flake8 Robuste
```python
# Parsing compatible Windows/Unix
if len(parts) >= 4 and len(parts[0]) == 1 and parts[1].startswith('\\'):
    # Chemin Windows (C:\path\file.py:line:col: msg)
    parsed_path = f"{parts[0]}:{parts[1]}"
    line_num_str = parts[2]
    col_num_str = parts[3] 
    code_msg_str = ':'.join(parts[4:])
elif len(parts) >= 3:
    # Format Unix/Relatif
    parsed_path = parts[0]
    line_num_str = parts[1]
    col_num_str = parts[2]
    code_msg_str = ':'.join(parts[3:])
```

### Détection Docstrings Manuelle
```python
def _has_module_docstring_manual(tree: ast.Module) -> bool:
    """Compatible Python 3.7+ pour détection docstring module."""
    if not tree.body:
        return False
    first_node = tree.body[0]
    
    # Python < 3.8: ast.Str
    if sys.version_info < (3, 8) and isinstance(first_node, ast.Expr):
        return isinstance(first_node.value, ast.Str)
    
    # Python >= 3.8: ast.Constant
    if isinstance(first_node, ast.Expr) and isinstance(first_node.value, ast.Constant):
        return isinstance(first_node.value.value, str)
    
    return False
```

### Scoring Intelligent
```python
# Score qualité avec pénalités graduées
quality_score = 100

# Docstring module: -15 points
if not has_module_docstring:
    quality_score -= 15

# Docstring classe: -5 points par classe
for missing_class_doc in missing_class_docs:
    quality_score -= 5

# Docstring fonction: -10 points par fonction
for missing_func_doc in missing_func_docs:
    quality_score -= 10

quality_score = max(0, quality_score)
```

## 10. Dépendances

- **Python 3.7+**
- **core.agent_factory_architecture** (Agent, Task, Result)
- **Flake8** : Audit style et conformité PEP8 (`pip install flake8`)
- **Modules standard** : ast, difflib, subprocess, asyncio, dataclasses
- **Typing** : Annotations et structures typées

## 11. Journal des Modifications (Changelog)

- **v5.2.0 (2025-06-26)** :
  - Harmonisation avec standards Pattern Factory NextGeneration
  - Enrichissement docstrings classe avec description détaillée capacités
  - Extension `get_capabilities()` : 2 → 10 capacités spécialisées
  - Documentation .md complètement refaite avec exemples techniques
- **v5.1.0** :
  - Ajout dataclass UniversalQualityIssue pour classification problèmes
  - Audit universel avec Flake8 + AST parsing avancé
  - Génération rapports Markdown enrichis avec diff et métriques
- **Versions antérieures** : Génération rapports basiques

## 12. Tests et Validation

### Test Intégré

L'agent inclut un test principal complet :

```python
# Test avec fichier problématique volontaire
test_py_content = '''
# Test file for universal audit
def hello_world(): # Missing docstring
    print("Hello, world!")

class MyClass: # Missing docstring
    def __init__(self): # Missing docstring
        self.value = 10

def another_func(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p): # Too many arguments
    pass # Missing docstring
'''

# Exécution audit complet
audit_result = await agent.execute_task(audit_task)
# Vérification détection problèmes multiples
```

### Exécution des Tests

```bash
# Test direct de l'agent  
python agents/agent_MAINTENANCE_05_documenteur_peer_reviewer.py

# Output attendu :
# 🚀 Démarrage des tests...
# 🏥 Health Check: {'status': 'healthy', 'version': '5.2.0'}
# 🛠️ Capabilities: ['generate_mission_report', 'audit_universal_quality', ...]
# 🔬 Test de la tâche 'audit_universal_quality'...
# Score de qualité: XX/100
# Problèmes trouvés: [détails des issues]
```

## 13. Cas d'Usage Recommandés

- **CI/CD Integration** : Audit automatique qualité dans pipelines
- **Code Review** : Assistance peer-review avec scoring automatisé
- **Maintenance Reports** : Documentation missions de maintenance
- **Quality Gates** : Validation qualité avant déploiement
- **Technical Debt** : Identification et classification problèmes code

## 14. Statut et Validation

- ✅ **Pattern Factory** : Conforme (Agent, Task, Result)
- ✅ **Méthodes async** : startup, shutdown, execute_task, health_check
- ✅ **Capabilities** : 10 capacités spécialisées définies
- ✅ **Technologies** : Flake8, AST, difflib, dataclasses
- ✅ **Documentation** : Docstrings enrichies et .md synchronisé
- ✅ **Tests Intégrés** : Validation complète avec fichier test
- ✅ **Audit Multi-niveau** : Flake8 + AST + scoring intelligent

**Agent MAINTENANCE 05 - État : PRÊT POUR VALIDATION**