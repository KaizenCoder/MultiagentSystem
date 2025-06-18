# 🧪 PROMPT SPRINT 2 - SUITE DE TESTS COMPLÈTE

**Rôle** : Développeur Senior spécialisé en Testing & QA  
**Mission** : Corriger et compléter la suite de tests pour atteindre 75% de couverture  
**Contexte** : Orchestrateur multi-agent avec 34 tests partiels existants  
**Durée** : 13 jours développeur (3 phases)  

---

## 🎯 OBJECTIF PRINCIPAL

Transformer les **34 tests partiels non-fonctionnels** en **suite complète de 80+ tests** avec **75% de couverture**, prête pour CI/CD et déploiement production.

### **État actuel analysé :**
- ✅ **34 tests collectés** (principalement SSRF prevention)
- ✅ **Framework configuré** : `conftest.py` complet (521 lignes)
- ❌ **Tests non-fonctionnels** : Erreurs configuration et imports
- ❌ **Couverture partielle** : ~20% (sécurité uniquement)
- ❌ **Tests core manquants** : Supervisor, Workers, API, E2E

---

## 📋 PHASE 1 : CORRECTION TESTS EXISTANTS (3 jours)

### **🔧 Jour 1 : Fix Configuration**

#### **Problème identifié :**
```bash
ValidationError: 3 validation errors for Settings
- OPENAI_API_KEY: Field required
- ANTHROPIC_API_KEY: Field required  
- ORCHESTRATOR_API_KEY: Field required
```

#### **Actions requises :**
1. **Installation dépendances manquantes**
```bash
pip install locust pytest-env pytest-mock pytest-timeout pytest-xdist
```

2. **Création fichier .env.test**
```env
# .env.test
OPENAI_API_KEY=sk-test-fake-openai-key-for-testing-only-12345
ANTHROPIC_API_KEY=sk-ant-test-fake-anthropic-key-for-testing-67890
ORCHESTRATOR_API_KEY=test-orchestrator-api-key-secure-12345
MEMORY_API_URL=http://localhost:8001
ENVIRONMENT=testing
DEBUG=true
LOG_LEVEL=INFO
SERVICE_VERSION=v9-test
```

3. **Configuration pytest.ini**
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=orchestrator
    --cov-report=html:htmlcov
    --cov-report=term-missing
    --cov-fail-under=75
    --timeout=30
    --tb=short
    -v
    --strict-markers
asyncio_mode = auto
env_files = .env.test
markers =
    unit: Unit tests
    integration: Integration tests
    security: Security tests
    performance: Performance tests
    slow: Slow running tests
```

### **🔧 Jour 2 : Fix Imports et Modules**

#### **Modification conftest.py**
```python
# Ajout au début de tests/conftest.py
import os
import sys
from pathlib import Path

# Ajout du répertoire racine au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Configure l'environnement de test avant chaque test."""
    test_env = {
        'OPENAI_API_KEY': 'sk-test-fake-openai-key',
        'ANTHROPIC_API_KEY': 'sk-ant-test-fake-anthropic-key',
        'ORCHESTRATOR_API_KEY': 'test-orchestrator-api-key',
        'ENVIRONMENT': 'testing',
        'DEBUG': 'true',
        'MEMORY_API_URL': 'http://localhost:8001'
    }
    
    # Sauvegarde environnement original
    original_env = {key: os.environ.get(key) for key in test_env.keys()}
    
    # Application environnement test
    os.environ.update(test_env)
    
    yield
    
    # Restauration environnement original
    for key, value in original_env.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
```

### **🔧 Jour 3 : Validation Tests Sécurité**

#### **Commandes de validation :**
```bash
# Test que les tests de sécurité passent
python -m pytest tests/security/ -v --tb=short

# Vérification couverture sécurité
python -m pytest tests/security/ --cov=orchestrator.app.security --cov-report=term-missing

# Test performance des validations
python -m pytest tests/security/ -m "not slow" --timeout=10
```

#### **Critères d'acceptation Phase 1 :**
- [ ] **34 tests passent** sans erreur
- [ ] **Couverture sécurité ≥ 90%**
- [ ] **Temps exécution < 30s** pour tests sécurité
- [ ] **Aucune fuite de secrets** dans les logs

---

## 📋 PHASE 2 : COMPLÉTION TESTS MANQUANTS (7 jours)

### **🧪 Jour 4-5 : Tests Unitaires Core**

#### **tests/unit/test_supervisor.py** (NOUVEAU - CRITIQUE)
```python
import pytest
from unittest.mock import Mock, patch, AsyncMock
from orchestrator.app.agents.supervisor import Supervisor
from orchestrator.app.graph.state import AgentState

@pytest.mark.unit
class TestSupervisor:
    """Tests unitaires Supervisor - CRITIQUE."""
    
    def setup_method(self):
        """Setup pour chaque test."""
        self.supervisor = Supervisor()
    
    def test_create_plan_code_generation_task(self, sample_agent_state):
        """Test planification tâche génération code."""
        # ARRANGE
        sample_agent_state.task_description = "Generate Python sorting function"
        
        # ACT
        result = self.supervisor.create_plan(sample_agent_state)
        
        # ASSERT
        assert result.plan is not None
        assert "code_generation" in result.plan
        assert result.next == "code_generation"
        assert result.task_status == "in_progress"
    
    def test_create_plan_documentation_task(self, sample_agent_state):
        """Test planification tâche documentation."""
        # ARRANGE
        sample_agent_state.task_description = "Create API documentation"
        
        # ACT
        result = self.supervisor.create_plan(sample_agent_state)
        
        # ASSERT
        assert result.plan is not None
        assert "documentation" in result.plan
        assert result.next == "documentation"
    
    def test_route_with_code_results(self, sample_agent_state):
        """Test routage avec résultats code."""
        # ARRANGE
        sample_agent_state.results = {"code_generation": "def sort_list(): pass"}
        sample_agent_state.plan = "existing plan"
        
        # ACT
        result = self.supervisor.route(sample_agent_state)
        
        # ASSERT
        assert result.next == "documentation"
    
    def test_route_completion_all_results(self, sample_agent_state):
        """Test routage vers fin avec tous résultats."""
        # ARRANGE
        sample_agent_state.results = {
            "code_generation": "def sort_list(): pass",
            "documentation": "Function documentation"
        }
        sample_agent_state.plan = "existing plan"
        
        # ACT
        result = self.supervisor.route(sample_agent_state)
        
        # ASSERT
        assert result.next == "finish"
    
    def test_error_handling_invalid_state(self):
        """Test gestion erreur état invalide."""
        # ARRANGE
        invalid_state = AgentState()  # État vide
        
        # ACT & ASSERT
        with pytest.raises(ValueError, match="Invalid state"):
            self.supervisor.create_plan(invalid_state)
    
    @pytest.mark.asyncio
    async def test_supervisor_with_llm_timeout(self, sample_agent_state):
        """Test gestion timeout LLM."""
        # ARRANGE
        with patch('orchestrator.app.agents.supervisor.llm_service') as mock_llm:
            mock_llm.generate_response.side_effect = asyncio.TimeoutError()
            
            # ACT & ASSERT
            with pytest.raises(TimeoutError):
                await self.supervisor.create_plan_async(sample_agent_state)
```

#### **tests/unit/test_workers.py** (NOUVEAU - CRITIQUE)
```python
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from orchestrator.app.agents.workers import get_agent_executor, worker_node_wrapper

@pytest.mark.unit
class TestWorkers:
    """Tests workers - CRITIQUE."""
    
    @pytest.mark.asyncio
    async def test_get_agent_executor_code_generation(self):
        """Test création agent génération code."""
        # ACT
        executor = get_agent_executor("code_generation")
        
        # ASSERT
        assert executor is not None
        assert hasattr(executor, 'agent')
        assert hasattr(executor, 'tools')
    
    @pytest.mark.asyncio
    async def test_worker_node_wrapper_success(self, sample_agent_state, mock_llm_service):
        """Test wrapper worker avec succès."""
        # ARRANGE
        sample_agent_state.task_description = "Generate code"
        
        with patch('orchestrator.app.agents.workers.get_agent_executor') as mock_get_executor:
            mock_executor = AsyncMock()
            mock_executor.ainvoke.return_value = {
                "output": "Generated code successfully"
            }
            mock_get_executor.return_value = mock_executor
            
            # ACT
            result = await worker_node_wrapper(sample_agent_state, "code_generation")
            
            # ASSERT
            assert result.results["code_generation"] is not None
            assert result.task_status == "completed"
```

### **🔄 Jour 6-7 : Tests Intégration API**

#### **tests/integration/test_api_endpoints.py** (NOUVEAU)
```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from orchestrator.app.main import app

@pytest.mark.integration
class TestAPIIntegration:
    """Tests intégration API."""
    
    def setup_method(self):
        """Setup client test."""
        self.client = TestClient(app)
    
    def test_health_endpoint(self):
        """Test endpoint santé."""
        # ACT
        response = self.client.get("/health")
        
        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "degraded"]
    
    @patch('orchestrator.app.main.graph')
    def test_invoke_endpoint_success(self, mock_graph):
        """Test endpoint invoke avec succès."""
        # ARRANGE
        mock_graph.ainvoke = AsyncMock(return_value={
            "results": {"code_generation": "def test(): pass"},
            "task_status": "completed"
        })
        
        payload = {
            "task_description": "Generate test function",
            "session_id": "test-session"
        }
        
        # ACT
        response = self.client.post("/invoke", json=payload)
        
        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert data["task_status"] == "completed"
```

### **🚀 Jour 8-10 : Tests End-to-End**

#### **tests/integration/test_workflow_complete.py** (NOUVEAU)
```python
@pytest.mark.integration
@pytest.mark.slow
class TestWorkflowIntegration:
    """Tests intégration bout-en-bout."""
    
    @pytest.mark.asyncio
    async def test_complete_code_generation_workflow(self):
        """Test workflow complet génération code."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8002/invoke",
                json={
                    "task_description": "Generate a Python function to sort a list",
                    "session_id": "test-session-1"
                }
            )
            
            assert response.status_code == 200
            response_data = response.json()
            assert "results" in response_data
            assert "code_generation" in response_data["results"]
```

---

## 📋 PHASE 3 : CI/CD ET AUTOMATISATION (3 jours)

### **🚀 Jour 11 : Pipeline CI/CD**

#### **.github/workflows/tests.yml** (NOUVEAU)
```yaml
name: Tests Suite Complète
on: 
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-asyncio pytest-mock locust
    
    - name: Run security tests
      run: |
        pytest tests/security/ -v --tb=short
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=orchestrator --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v --timeout=60
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### **🚀 Jour 12-13 : Optimisation et Documentation**

#### **Makefile** (NOUVEAU)
```makefile
.PHONY: test test-unit test-integration test-security test-coverage

test:
	python -m pytest tests/ -v

test-unit:
	python -m pytest tests/unit/ -v --tb=short

test-integration:
	python -m pytest tests/integration/ -v --timeout=60

test-security:
	python -m pytest tests/security/ -v

test-coverage:
	python -m pytest tests/ --cov=orchestrator --cov-report=html --cov-report=term-missing

test-fast:
	python -m pytest tests/ -x --tb=short -m "not slow"

install-test-deps:
	pip install pytest pytest-cov pytest-asyncio pytest-mock pytest-timeout locust
```

---

## 📊 CRITÈRES DE SUCCÈS SPRINT 2

### **Métriques obligatoires :**
- [ ] **Couverture ≥ 75%** (pytest-cov)
- [ ] **80+ tests** au total (vs 34 actuels)
- [ ] **Tests unitaires** : 40+ tests pour composants core
- [ ] **Tests intégration** : 20+ tests API endpoints
- [ ] **Tests E2E** : 8+ workflows complets
- [ ] **Performance** : Temps réponse < 100ms health checks
- [ ] **Sécurité** : 0 vulnérabilité dans tests
- [ ] **CI/CD** : Pipeline automatisé fonctionnel

### **Commandes de validation finale :**
```bash
# Validation complète
make test-coverage
pytest tests/ --cov=orchestrator --cov-fail-under=75

# Performance
pytest tests/ --timeout=300 --tb=short

# Sécurité
pytest tests/security/ -v --tb=short

# CI/CD simulation
act -j tests  # GitHub Actions local
```

---

## 🎯 LIVRABLES ATTENDUS

### **Structure finale attendue :**
```
tests/
├── conftest.py (✅ existant, amélioré)
├── pytest.ini (🆕 nouveau)
├── .env.test (🆕 nouveau)
├── unit/ (🆕 nouveau)
│   ├── test_supervisor.py (15+ tests)
│   ├── test_workers.py (12+ tests)
│   ├── test_graph.py (8+ tests)
│   └── test_state.py (5+ tests)
├── integration/ (🆕 nouveau)
│   ├── test_api_endpoints.py (20+ tests)
│   └── test_workflow_complete.py (8+ tests)
├── security/ (✅ existant, corrigé)
│   ├── test_rce_prevention.py (✅ 20+ tests)
│   └── test_ssrf_prevention.py (✅ 32+ tests)
└── load/ (✅ existant, corrigé)
    └── basic_load_test.py (✅ tests performance)
```

### **Documentation requise :**
- [ ] **README_TESTS.md** : Guide utilisation tests
- [ ] **TESTING_STRATEGY.md** : Stratégie et patterns
- [ ] **CI_CD_GUIDE.md** : Guide pipeline automatisé

---

## 🏆 RÉSULTAT ATTENDU

**Transformation complète** : De 34 tests partiels non-fonctionnels à **suite robuste de 80+ tests** avec **75% de couverture**, **CI/CD automatisé**, et **confiance totale** pour évolutions futures.

**Impact business** :
- 🛡️ **Filet de sécurité** pour évolutions
- 🚀 **Déploiement confiant** en production
- 📈 **Qualité code** maintenue
- 🔧 **Maintenance** facilitée
- 💰 **ROI développement** optimisé

---

**🎯 MISSION : Créer la suite de tests la plus robuste et complète possible pour sécuriser l'évolution de l'orchestrateur multi-agent vers la production.** 