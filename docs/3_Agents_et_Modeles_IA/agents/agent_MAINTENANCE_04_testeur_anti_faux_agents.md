# Agent MAINTENANCE 04 – Testeur Anti-Faux Agents

## 1. Identification

- **Nom :** Testeur Anti-Faux Agents NextGeneration
- **Identifiant :** `agent_MAINTENANCE_04_testeur_anti_faux_agents`
- **Version :** 4.1.0 (Harmonisation Standards Pattern Factory NextGeneration)
- **Responsable Principal :** Équipe de Maintenance NextGeneration
- **Contact Technique :** `#canal-maintenance-ia`

## 2. Description Générale

🛡️ Agent spécialisé dans la validation dynamique et l'authentification d'agents, détection de faux agents via tests d'instanciation et vérification conformité Pattern Factory pour garantir l'intégrité du système.

Cet agent utilise des techniques avancées d'introspection et de tests dynamiques pour distinguer les vrais agents fonctionnels des faux agents non-conformes.

## 3. Objectifs et Missions

- **Authentification Agents :** Validation dynamique de la conformité des agents via tests d'instanciation
- **Détection Faux Agents :** Identification automatique d'agents non-fonctionnels ou malformés
- **Validation Pattern Factory :** Vérification conformité async/sync et méthodes obligatoires
- **Tests Sécurisés :** Exécution isolée avec environnement temporaire sécurisé
- **Support Équipe Maintenance :** Qualification automatique d'agents pour workflows de maintenance

## 4. Fonctionnalités Clés (Conformité Pattern Factory)

L'agent respecte le Pattern Factory NextGeneration et expose les méthodes suivantes :

- **`startup()`** : Initialise l'agent testeur anti-faux agents
- **`health_check()`** : Vérifie l'état de santé. Retourne `{"status": "healthy"}` en fonctionnement normal
- **`execute_task(task: Task)`** : Point d'entrée principal pour les tests d'agents
  - **Action `test_code`** :
    - **`task.params` attendus** :
      - `code` (str) : Code source de l'agent à tester
      - `file_path` (str, optionnel) : Nom du fichier pour identification
    - **Résultat** : Résultats de tests avec détails de conformité et violations
- **`shutdown()`** : Arrête l'agent proprement

### Capacités Spécialisées

```python
get_capabilities() -> [
    "dynamic_agent_testing",
    "fake_agent_detection", 
    "pattern_factory_validation",
    "dynamic_instantiation",
    "signature_introspection",
    "compliance_scoring",
    "async_sync_validation",
    "isolated_execution",
    "factory_method_testing",
    "violation_classification"
]
```

## 5. Technologies Avancées

### Tests Dynamiques Sécurisés
- **Importation dynamique** avec `importlib.util.spec_from_file_location`
- **Fichiers temporaires isolés** pour tests sans contamination
- **Nettoyage automatique** des ressources temporaires

### Introspection Avancée
```python
# Déduction automatique des arguments d'instanciation
sig = inspect.signature(obj.__init__)
params = sig.parameters

# Génération arguments factices selon types
for param_name, param in params.items():
    if param.annotation == str:
        test_args[param_name] = f"test_{param_name}"
    elif param.annotation == int:
        test_args[param_name] = 123
    elif param.annotation == bool:
        test_args[param_name] = True
```

### Structure FakeAgentDetection
```python
@dataclass
class FakeAgentDetection:
    agent_id: str
    agent_name: str
    is_fake_agent: bool
    sync_violations: List[str]
    async_violations: List[str]
    pattern_factory_violations: List[str]
    compliance_score: float
    recommendation: str
    details: Dict[str, Any]
```

## 6. Workflow de Validation

```
1. 📋 Réception code agent à tester via execute_task
2. 🔒 Création environnement temporaire sécurisé
3. 📥 Chargement dynamique module avec spec_from_file_location
4. 🔍 Introspection classes héritant de Agent
5. 🧪 Instanciation factice avec arguments déduits
6. ✅ Tests conformité Pattern Factory (startup, health_check, shutdown)
7. 📊 Calcul score compliance et classification violations
8. 🧹 Nettoyage automatique fichiers temporaires
9. 📄 Retour résultats structurés avec recommandations
```

## 7. Exemples d'Utilisation

### Test d'Agent Valide

```python
from core.agent_factory_architecture import Task
from agents.agent_MAINTENANCE_04_testeur_anti_faux_agents import create_agent_MAINTENANCE_04_testeur_anti_faux_agents

# Code d'agent valide à tester
valid_agent_code = """
from core.agent_factory_architecture import Agent, Task, Result

class ValidAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    async def startup(self):
        pass
    
    async def execute_task(self, task: Task) -> Result:
        return Result(success=True, data={"message": "Task executed"})
    
    async def health_check(self):
        return {"status": "healthy"}
    
    async def shutdown(self):
        pass
    
    def get_capabilities(self):
        return ["example_capability"]
"""

# Création de l'agent testeur
testeur = create_agent_MAINTENANCE_04_testeur_anti_faux_agents()
await testeur.startup()

# Test de validation
task = Task(
    type="test_code",
    params={
        "code": valid_agent_code,
        "file_path": "valid_agent.py"
    }
)

result = await testeur.execute_task(task)
if result.success:
    print(f"✅ Agent valide: {result.data['details']}")
else:
    print(f"❌ Agent invalide: {result.error}")
```

### Test de Faux Agent

```python
# Code de faux agent (classe non-conforme)
fake_agent_code = """
class FakeAgent:
    def __init__(self):
        pass
    
    def some_method(self):
        return "Not a real agent"
"""

task = Task(
    type="test_code",
    params={
        "code": fake_agent_code,
        "file_path": "fake_agent.py"
    }
)

result = await testeur.execute_task(task)
# Résultat : Échec détecté, aucune classe héritant de Agent trouvée
```

### Test avec Méthode de Compatibilité

```python
# Utilisation de l'ancienne interface (compatibilité)
result = await testeur.run_test("test_agent.py", agent_code)
if result.success:
    details = result.data["details"]
    print(f"Agent testé avec succès: {details}")
```

## 8. Format de Résultat

### Succès de Validation

```json
{
  "success": true,
  "data": {
    "file_path": "valid_agent.py",
    "details": "Agent ValidAgent instancié et health_check réussi."
  }
}
```

### Échec de Validation

```json
{
  "success": false,
  "error": "Aucune classe héritant de 'Agent' n'a pu être trouvée et instanciée.",
  "data": {
    "file_path": "invalid_agent.py"
  }
}
```

### Erreur d'Exécution

```json
{
  "success": false,
  "error": "Échec du test dynamique: ModuleNotFoundError: No module named 'missing_dependency'",
  "data": {
    "file_path": "broken_agent.py"
  }
}
```

## 9. Sécurité et Isolation

### Environnement Temporaire
- **Répertoire isolé** : `./temp_test_agents/`
- **Noms uniques** : `temp_{agent_name}_{uuid}.py`
- **Nettoyage automatique** : Suppression systématique des fichiers temporaires

### Gestion des Erreurs
```python
try:
    # Tests dynamiques sécurisés
    instance = obj(**test_args)
    await instance.health_check()
    return True, f"Agent {name} instancié et health_check réussi."
except TypeError as te:
    # Fallback avec paramètres par défaut
    instance = obj(agent_id='test-agent', version='0.0.0', ...)
finally:
    # Nettoyage garanti
    if temp_file_path and os.path.exists(temp_file_path):
        os.remove(temp_file_path)
```

## 10. Capacités d'Introspection

### Analyse de Signature Dynamique
```python
# Inspection automatique des constructeurs
sig = inspect.signature(obj.__init__)
params = sig.parameters

for param_name, param in params.items():
    if param_name == 'self':
        continue
    if param.default != inspect.Parameter.empty:
        continue  # Paramètre optionnel
    if param.kind == inspect.Parameter.VAR_KEYWORD:
        continue  # **kwargs
    
    # Génération valeurs factices selon annotation
    if param.annotation == str:
        test_args[param_name] = f"test_{param_name}"
    elif param.annotation == int:
        test_args[param_name] = 123
    elif param.annotation == bool:
        test_args[param_name] = True
```

## 11. Dépendances

- **Python 3.8+**
- **core.agent_factory_architecture** (Agent, Task, Result)
- **Modules standard** : inspect, importlib, uuid, tempfile, asyncio
- **Typing** : Annotations et dataclasses pour structures de données

## 12. Journal des Modifications (Changelog)

- **v4.1.0 (2025-06-26)** :
  - Harmonisation avec standards Pattern Factory NextGeneration
  - Enrichissement docstrings classe avec description détaillée capacités
  - Extension `get_capabilities()` : 1 → 10 capacités spécialisées
  - Documentation .md complètement refaite avec exemples techniques
- **v4.0.0** :
  - Ajout dataclass FakeAgentDetection pour résultats structurés
  - Introspection avancée avec inspect.signature
  - Tests dynamiques sécurisés avec environnement temporaire
- **Versions antérieures** : Tests basiques d'importation

## 13. Tests et Validation

### Test Intégré

L'agent inclut un test principal démonstratif :

```python
# Test avec agent valide
good_code = """
class GoodAgent(Agent):
    def __init__(self, **kwargs): super().__init__(**kwargs)
    async def execute_task(self, task: Task) -> Result: return Result(success=True)
    def get_capabilities(self) -> list: return []
    async def startup(self): pass
    async def shutdown(self): pass
    async def health_check(self) -> dict: return {"status": "ok"}
"""

# Test avec faux agent
bad_code = "class BadAgent: pass"
```

### Exécution des Tests

```bash
# Test direct de l'agent
python agents/agent_MAINTENANCE_04_testeur_anti_faux_agents.py

# Output attendu :
# --- Test Agent Valide ---
# {"success": true, "data": {...}, "error": null}
# --- Test Agent Invalide ---  
# {"success": false, "data": {...}, "error": "..."}
```

## 14. Cas d'Usage Recommandés

- **Validation CI/CD** : Tests automatiques d'agents avant déploiement
- **Audit qualité** : Vérification conformité Pattern Factory en masse
- **Debugging agents** : Diagnostic rapide d'agents non-fonctionnels
- **Migration projects** : Validation conformité lors de refactorisation
- **Quality assurance** : Tests de régression sur modifications d'agents

## 15. Statut et Validation

- ✅ **Pattern Factory** : Conforme (Agent, Task, Result)
- ✅ **Méthodes async** : startup, shutdown, execute_task, health_check
- ✅ **Capabilities** : 10 capacités spécialisées définies
- ✅ **Technologies** : Introspection, tests dynamiques, dataclasses
- ✅ **Documentation** : Docstrings enrichies et .md synchronisé
- ✅ **Sécurité** : Tests isolés avec nettoyage automatique
- ✅ **Compatibilité** : Méthode run_test() pour ancienne interface

**Agent MAINTENANCE 04 - État : PRÊT POUR VALIDATION**