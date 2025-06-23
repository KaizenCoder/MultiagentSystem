# 🧪 PLAN D'ACTION - SPRINT 2 : SUITE DE TESTS COMPLÈTE

**Objectif** : Passer de 0% à 75% de couverture de tests en 2 semaines  
**Priorité** : CRITIQUE - Action #2 post-sécurisation  
**Effort estimé** : 10 jours développeur  

---

## 🎯 CONTEXTE ET JUSTIFICATION

### **Situation actuelle (Consensus peer reviews) :**
- **Couverture tests : 0%** - Aucun fichier de test existant
- **Score consolidé : 2.0/10** - Critique absolu
- **Impact : BLOQUANT** - Déploiement production impossible
- **Risque : ÉLEVÉ** - Évolution du code sans filet de sécurité

### **Criticité identifiée :**
1. ❌ **Régressions non détectables** lors des modifications
2. ❌ **Refactoring impossible** sans risque majeur
3. ❌ **Maintenance périlleuse** - changements aveugles
4. ❌ **Confiance zéro** dans la stabilité du code
5. ❌ **Debug difficile** - pas de validation isolée

---

## 📋 PLAN D'IMPLÉMENTATION DÉTAILLÉ

### **🔧 Phase 1 : Infrastructure de Tests (Jours 1-3)**

#### **Jour 1 : Setup Framework**
```bash
# 1. Installation dépendances test
pip install pytest pytest-cov pytest-asyncio pytest-mock pytest-timeout

# 2. Configuration pytest
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=orchestrator
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=75
    --timeout=30
    -v
asyncio_mode = auto
```

#### **Jour 2 : Structure et Fixtures**
```python
# tests/conftest.py - Configuration globale
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from orchestrator.app.main import app
from orchestrator.app.graph.state import AgentState

@pytest.fixture
def mock_llm_service():
    """Mock service LLM pour tests."""
    service = Mock()
    service.generate_response = AsyncMock(return_value="Mocked LLM response")
    service.analyze_code = AsyncMock(return_value={"analysis": "mocked"})
    return service

@pytest.fixture
def sample_agent_state():
    """État agent type pour tests."""
    return AgentState(
        messages=[],
        plan=None,
        next="",
        results={},
        session_id="test-session-123",
        task_description="Test task description",
        task_status="pending",
        code_context=None,
        working_memory=[],
        errors=[],
        logs=[],
        feedback=None
    )

@pytest.fixture
def mock_memory_api():
    """Mock Memory API pour tests."""
    api = Mock()
    api.store_memory = AsyncMock(return_value={"status": "stored"})
    api.search_memory = AsyncMock(return_value={"results": []})
    return api
```

#### **Jour 3 : Mocks et Utilitaires**
```python
# tests/utils/test_helpers.py
import json
from typing import Dict, Any
from unittest.mock import Mock

class MockLLMResponse:
    """Mock réponse LLM standardisée."""
    
    def __init__(self, content: str, usage: Dict[str, int] = None):
        self.content = content
        self.usage = usage or {"prompt_tokens": 10, "completion_tokens": 20}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "usage": self.usage
        }

def create_mock_task_request(description: str = "Test task") -> Dict[str, Any]:
    """Crée une requête de tâche mock."""
    return {
        "task_description": description,
        "session_id": "test-session",
        "code_context": "def example(): pass",
        "priority": "normal"
    }

def assert_agent_state_valid(state: AgentState) -> None:
    """Valide qu'un état agent est cohérent."""
    assert state.session_id is not None
    assert isinstance(state.messages, list)
    assert state.task_status in ["pending", "in_progress", "completed", "failed"]
```

---

### **🧪 Phase 2 : Tests Unitaires Core (Jours 4-6)**

#### **Jour 4 : Tests Supervisor**
```python
# tests/unit/test_supervisor.py
import pytest
from unittest.mock import Mock, patch
from orchestrator.app.agents.supervisor import Supervisor
from orchestrator.app.graph.state import AgentState

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
    
    def test_route_creates_plan_when_missing(self, sample_agent_state):
        """Test création plan automatique si manquant."""
        # ARRANGE
        sample_agent_state.task_description = "Test task"
        sample_agent_state.plan = None
        
        # ACT
        result = self.supervisor.route(sample_agent_state)
        
        # ASSERT
        assert result.plan is not None
        assert result.task_status == "in_progress"
        assert result.next in ["code_generation", "documentation"]
    
    def test_error_handling_invalid_state(self):
        """Test gestion erreur état invalide."""
        # ARRANGE
        invalid_state = AgentState()  # État vide
        
        # ACT & ASSERT
        with pytest.raises(ValueError, match="Invalid state"):
            self.supervisor.create_plan(invalid_state)
```

#### **Jour 5 : Tests Workers**
```python
# tests/unit/test_workers.py
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from orchestrator.app.agents.workers import get_agent_executor, worker_node_wrapper

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
    async def test_get_agent_executor_documentation(self):
        """Test création agent documentation."""
        # ACT
        executor = get_agent_executor("documentation")
        
        # ASSERT
        assert executor is not None
        assert hasattr(executor, 'agent')
    
    @pytest.mark.asyncio
    async def test_get_agent_executor_invalid_type(self):
        """Test gestion type agent invalide."""
        # ACT & ASSERT
        with pytest.raises(ValueError, match="Unknown agent type"):
            get_agent_executor("invalid_agent")
    
    @pytest.mark.asyncio
    async def test_get_agent_executor_caching(self):
        """Test mise en cache des agents."""
        # ACT
        executor1 = get_agent_executor("code_generation")
        executor2 = get_agent_executor("code_generation")
        
        # ASSERT
        assert executor1 is executor2  # Cache actif
    
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
    
    @pytest.mark.asyncio
    async def test_worker_node_wrapper_error_handling(self, sample_agent_state):
        """Test gestion erreur worker."""
        # ARRANGE
        with patch('orchestrator.app.agents.workers.get_agent_executor') as mock_get_executor:
            mock_executor = AsyncMock()
            mock_executor.ainvoke.side_effect = Exception("LLM API Error")
            mock_get_executor.return_value = mock_executor
            
            # ACT
            result = await worker_node_wrapper(sample_agent_state, "code_generation")
            
            # ASSERT
            assert result.task_status == "failed"
            assert len(result.errors) > 0
            assert "LLM API Error" in str(result.errors[-1])
```

#### **Jour 6 : Tests Graph et State**
```python
# tests/unit/test_graph.py
import pytest
from orchestrator.app.graph.graph import create_graph
from orchestrator.app.graph.state import AgentState

class TestGraph:
    """Tests graph LangGraph."""
    
    def test_create_graph_structure(self):
        """Test création structure graph."""
        # ACT
        graph = create_graph()
        
        # ASSERT
        assert graph is not None
        # Vérifier nœuds essentiels
        expected_nodes = ["supervisor", "code_generation", "documentation", "finish"]
        for node in expected_nodes:
            assert node in graph.nodes
    
    def test_graph_edges_configuration(self):
        """Test configuration des arêtes."""
        # ACT
        graph = create_graph()
        
        # ASSERT
        # Vérifier transitions possibles
        assert "supervisor" in graph.edges
        assert "code_generation" in graph.edges
        assert "documentation" in graph.edges

class TestAgentState:
    """Tests état agent."""
    
    def test_agent_state_initialization(self):
        """Test initialisation état."""
        # ACT
        state = AgentState()
        
        # ASSERT
        assert state.messages == []
        assert state.results == {}
        assert state.errors == []
        assert state.task_status == "pending"
    
    def test_agent_state_serialization(self, sample_agent_state):
        """Test sérialisation état."""
        # ACT
        serialized = sample_agent_state.dict()
        
        # ASSERT
        assert "session_id" in serialized
        assert "task_description" in serialized
        assert "task_status" in serialized
    
    def test_agent_state_validation(self):
        """Test validation état."""
        # ARRANGE & ACT & ASSERT
        with pytest.raises(ValueError):
            AgentState(task_status="invalid_status")
```

---

### **🔄 Phase 3 : Tests d'Intégration (Jours 7-8)**

#### **Jour 7 : Tests API Endpoints**
```python
# tests/integration/test_api.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from orchestrator.app.main import app

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
    
    def test_status_endpoint(self):
        """Test endpoint status."""
        # ACT
        response = self.client.get("/status")
        
        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "uptime" in data
    
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
    
    def test_invoke_endpoint_validation_error(self):
        """Test validation erreur invoke."""
        # ARRANGE
        invalid_payload = {"invalid": "data"}
        
        # ACT
        response = self.client.post("/invoke", json=invalid_payload)
        
        # ASSERT
        assert response.status_code == 422  # Validation error
    
    def test_feedback_endpoint(self):
        """Test endpoint feedback."""
        # ARRANGE
        payload = {
            "session_id": "test-session",
            "feedback": "positive",
            "comments": "Good result"
        }
        
        # ACT
        response = self.client.post("/feedback", json=payload)
        
        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
```

#### **Jour 8 : Tests End-to-End**
```python
# tests/integration/test_workflow_complete.py
import pytest
import httpx
import asyncio
from testcontainers.compose import DockerCompose

class TestWorkflowIntegration:
    """Tests intégration bout-en-bout."""
    
    @pytest.fixture(scope="class")
    def docker_services(self):
        """Setup environnement test avec Docker Compose."""
        with DockerCompose(".", compose_file_name="docker-compose.test.yml") as compose:
            # Wait for services
            compose.wait_for("http://localhost:8001/health")  # Memory API
            compose.wait_for("http://localhost:8002/health")  # Orchestrator
            yield compose
    
    @pytest.mark.asyncio
    async def test_complete_code_generation_workflow(self, docker_services):
        """Test workflow complet génération code."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8002/invoke",
                json={
                    "task_description": "Generate a Python function to sort a list",
                    "session_id": "test-session-1"
                },
                headers={"X-API-KEY": "test-api-key"}
            )
            
            assert response.status_code == 200
            
            # Verify response contains code
            response_data = response.json()
            assert "results" in response_data
            assert "code_generation" in response_data["results"]
    
    @pytest.mark.asyncio
    async def test_complete_documentation_workflow(self, docker_services):
        """Test workflow complet documentation."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8002/invoke",
                json={
                    "task_description": "Create documentation for this API",
                    "session_id": "test-session-2"
                }
            )
            
            assert response.status_code == 200
            response_data = response.json()
            assert "documentation" in response_data["results"]
    
    @pytest.mark.asyncio
    async def test_memory_api_integration(self, docker_services):
        """Test intégration Memory API."""
        async with httpx.AsyncClient() as client:
            # Store memory
            store_response = await client.post(
                "http://localhost:8001/store",
                json={
                    "content": "Test memory content",
                    "session_id": "test-session-3"
                }
            )
            assert store_response.status_code == 200
            
            # Search memory
            search_response = await client.post(
                "http://localhost:8001/search",
                json={
                    "query": "Test memory",
                    "session_id": "test-session-3"
                }
            )
            assert search_response.status_code == 200
            search_data = search_response.json()
            assert len(search_data["results"]) > 0
```

---

### **⚡ Phase 4 : Tests Performance et Sécurité (Jours 9-10)**

#### **Jour 9 : Tests Performance**
```python
# tests/performance/test_load.py
import pytest
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from orchestrator.app.main import app

class TestPerformance:
    """Tests performance."""
    
    def setup_method(self):
        """Setup client test."""
        self.client = TestClient(app)
    
    def test_health_endpoint_response_time(self):
        """Test temps réponse health check."""
        # ACT
        start_time = time.time()
        response = self.client.get("/health")
        end_time = time.time()
        
        # ASSERT
        assert response.status_code == 200
        assert (end_time - start_time) < 0.1  # < 100ms
    
    def test_concurrent_requests_handling(self):
        """Test gestion requêtes concurrentes."""
        def make_request():
            return self.client.get("/health")
        
        # ACT
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            responses = [future.result() for future in futures]
        
        # ASSERT
        success_count = sum(1 for r in responses if r.status_code == 200)
        assert success_count >= 45  # 90% success rate minimum
    
    @pytest.mark.asyncio
    async def test_memory_usage_stability(self):
        """Test stabilité usage mémoire."""
        import psutil
        import os
        
        # ARRANGE
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # ACT - Simulate load
        for _ in range(100):
            response = self.client.get("/health")
            assert response.status_code == 200
        
        # ASSERT
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        # Memory increase should be reasonable (< 50MB)
        assert memory_increase < 50 * 1024 * 1024
```

#### **Jour 10 : Tests Sécurité**
```python
# tests/security/test_security_integration.py
import pytest
from fastapi.testclient import TestClient
from orchestrator.app.main import app

class TestSecurityIntegration:
    """Tests sécurité intégration."""
    
    def setup_method(self):
        """Setup client test."""
        self.client = TestClient(app)
    
    def test_sql_injection_protection(self):
        """Test protection injection SQL."""
        # ARRANGE
        malicious_payload = {
            "task_description": "'; DROP TABLE users; --",
            "session_id": "test-session"
        }
        
        # ACT
        response = self.client.post("/invoke", json=malicious_payload)
        
        # ASSERT
        # Should not crash and should sanitize input
        assert response.status_code in [200, 400, 422]
    
    def test_xss_protection(self):
        """Test protection XSS."""
        # ARRANGE
        xss_payload = {
            "task_description": "<script>alert('xss')</script>",
            "session_id": "test-session"
        }
        
        # ACT
        response = self.client.post("/invoke", json=xss_payload)
        
        # ASSERT
        if response.status_code == 200:
            # Verify script tags are escaped/removed
            response_text = response.text
            assert "<script>" not in response_text
    
    def test_rate_limiting(self):
        """Test rate limiting."""
        # ACT - Make many requests quickly
        responses = []
        for _ in range(20):
            response = self.client.post("/invoke", json={
                "task_description": "test",
                "session_id": "rate-limit-test"
            })
            responses.append(response)
        
        # ASSERT
        # Should have some rate limited responses (429)
        rate_limited = [r for r in responses if r.status_code == 429]
        assert len(rate_limited) > 0
    
    def test_cors_headers(self):
        """Test headers CORS."""
        # ACT
        response = self.client.options("/invoke")
        
        # ASSERT
        assert "Access-Control-Allow-Origin" in response.headers
        assert "Access-Control-Allow-Methods" in response.headers
```

---

## 📊 MÉTRIQUES DE SUCCÈS

### **Critères d'acceptation Sprint 2 :**
- [ ] **Couverture ≥ 75%** (pytest-cov)
- [ ] **Tests unitaires** : 50+ tests pour composants core
- [ ] **Tests intégration** : 15+ tests API endpoints
- [ ] **Tests E2E** : 5+ workflows complets
- [ ] **Tests performance** : Temps réponse < 100ms
- [ ] **Tests sécurité** : Protection injections/XSS
- [ ] **Pipeline CI** : Tests automatisés sur push/PR
- [ ] **Documentation** : Tests documentés et maintenables

### **Métriques de qualité :**
```bash
# Commandes validation
pytest --cov=orchestrator --cov-report=html --cov-fail-under=75
pytest tests/unit/ -v --tb=short
pytest tests/integration/ -v --tb=short  
pytest tests/performance/ -v --tb=short
pytest tests/security/ -v --tb=short

# Métriques attendues
# - Couverture globale : ≥ 75%
# - Tests unitaires : ≥ 90% success
# - Tests intégration : ≥ 95% success
# - Tests E2E : ≥ 90% success
# - Temps exécution : < 5 minutes total
```

---

## 🎯 IMPACT ATTENDU

### **Bénéfices immédiats :**
- 🛡️ **Filet de sécurité** pour évolutions futures
- 🔍 **Détection précoce** des régressions
- 🚀 **Confiance** dans le déploiement
- 📈 **Qualité code** améliorée
- 🔧 **Maintenance** facilitée

### **Bénéfices long terme :**
- 🏗️ **Refactoring sécurisé** possible
- 📊 **Métriques qualité** continues
- 🤝 **Collaboration** équipe améliorée
- 🎯 **Focus** sur nouvelles features
- 💰 **ROI** développement optimisé

---

**🎉 RÉSULTAT ATTENDU : Transformation d'un prototype 0% testé en application robuste avec 75% de couverture de tests, prête pour évolution et déploiement sécurisé.** 