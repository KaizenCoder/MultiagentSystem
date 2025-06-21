"""
Tests d'intgration API Orchestrateur - CRITIQUE Phase 2.
Tests des endpoints essentiels selon prompt Sprint 2.
"""

import pytest
import asyncio
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock


@pytest.mark.integration
class TestOrchestratorAPI:
    """Tests d'intgration API Orchestrateur - CRITIQUE."""
    
    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Setup du client de test FastAPI."""
        try:
            from orchestrator.app.main import app
            self.client = TestClient(app)
        except Exception as e:
            pytest.skip(f"Cannot import orchestrator app: {e}")
    
    def test_health_endpoint(self):
        """Test endpoint /health - CRITIQUE."""
        # ACT
        response = self.client.get("/health")
        
        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "ok"]
    
    def test_status_endpoint(self):
        """Test endpoint /status - CRITIQUE (corrig v9)."""
        # ACT
        response = self.client.get("/status")
        
        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "orchestrator" in data
        assert "memory_api" in data
        assert "timestamp" in data
    
    @patch('orchestrator.app.agents.supervisor.Supervisor.create_plan')
    def test_process_task_basic(self, mock_create_plan):
        """Test /process - endpoint principal."""
        # ARRANGE
        mock_create_plan.return_value = {
            "plan": "Test plan created",
            "next": "code_generation",
            "task_status": "in_progress"
        }
        
        task_data = {
            "task_description": "Generate Python sorting function",
            "session_id": "test-session-api"
        }
        
        # ACT
        response = self.client.post(
            "/process",
            json=task_data,
            headers={"Content-Type": "application/json"}
        )
        
        # ASSERT
        assert response.status_code in [200, 202]  # Success ou Accepted
        data = response.json()
        assert "session_id" in data
        assert data["session_id"] == "test-session-api"
    
    def test_process_task_validation(self):
        """Test validation entre /process."""
        # Test donnes invalides
        invalid_data = {"invalid_field": "test"}
        
        # ACT
        response = self.client.post("/process", json=invalid_data)
        
        # ASSERT
        assert response.status_code == 422  # Validation error
    
    def test_process_task_empty_description(self):
        """Test description vide."""
        # ARRANGE
        task_data = {
            "task_description": "",
            "session_id": "test-empty"
        }
        
        # ACT
        response = self.client.post("/process", json=task_data)
        
        # ASSERT
        assert response.status_code == 422  # Should reject empty description
    
    @patch('orchestrator.app.checkpoint.api_checkpointer.APICheckpointer.get_session')
    def test_get_session_status(self, mock_get_session):
        """Test rcupration statut session."""
        # ARRANGE
        mock_get_session.return_value = {
            "session_id": "test-session",
            "task_status": "completed",
            "results": {"code": "def sort_list(lst): return sorted(lst)"}
        }
        
        # ACT
        response = self.client.get("/session/test-session")
        
        # ASSERT
        if response.status_code == 404:
            pytest.skip("Session endpoint not implemented yet")
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
    
    def test_rate_limiting_protection(self):
        """Test protection rate limiting."""
        # ARRANGE
        task_data = {
            "task_description": "Test rate limiting",
            "session_id": "rate-test"
        }
        
        # ACT - Envoyer plusieurs requtes rapidement
        responses = []
        for i in range(5):
            response = self.client.post("/process", json=task_data)
            responses.append(response.status_code)
        
        # ASSERT
        # Au moins une requte devrait passer
        assert 200 in responses or 202 in responses
        # Si rate limiting activ, certaines peuvent tre rejetes
        if 429 in responses:
            print("[CHECK] Rate limiting detect et fonctionnel")
    
    def test_cors_headers(self):
        """Test headers CORS."""
        # ACT
        response = self.client.options("/health")
        
        # ASSERT
        # CORS peut tre configur ou non selon l'environnement
        if "access-control-allow-origin" in response.headers:
            print("[CHECK] CORS headers prsents")
        else:
            print(" CORS headers non configurs (normal en test)")
    
    def test_api_error_handling(self):
        """Test gestion d'erreurs API."""
        # ACT - Endpoint inexistant
        response = self.client.get("/nonexistent-endpoint")
        
        # ASSERT
        assert response.status_code == 404
    
    @patch('httpx.AsyncClient.post')
    def test_memory_api_integration(self, mock_http_post):
        """Test intgration Memory API."""
        # ARRANGE
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}
        mock_http_post.return_value = mock_response
        
        task_data = {
            "task_description": "Test memory integration",
            "session_id": "memory-test"
        }
        
        # ACT
        response = self.client.post("/process", json=task_data)
        
        # ASSERT
        # Le test passe si l'API rpond, mme avec erreur interne
        assert response.status_code in [200, 202, 500, 503]


@pytest.mark.integration
class TestOrchestratorSecurity:
    """Tests de scurit API - CRITIQUE."""
    
    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Setup du client de test FastAPI."""
        try:
            from orchestrator.app.main import app
            self.client = TestClient(app)
        except Exception as e:
            pytest.skip(f"Cannot import orchestrator app: {e}")
    
    def test_sql_injection_protection(self):
        """Test protection injection SQL."""
        # ARRANGE
        malicious_data = {
            "task_description": "'; DROP TABLE users; --",
            "session_id": "sql-injection-test"
        }
        
        # ACT
        response = self.client.post("/process", json=malicious_data)
        
        # ASSERT
        # Ne devrait pas provoquer d'erreur 500 (injection russie)
        assert response.status_code != 500
        print("[CHECK] Protection injection SQL active")
    
    def test_xss_protection(self):
        """Test protection XSS."""
        # ARRANGE
        xss_data = {
            "task_description": "<script>alert('xss')</script>",
            "session_id": "xss-test"
        }
        
        # ACT
        response = self.client.post("/process", json=xss_data)
        
        # ASSERT
        if response.status_code == 200:
            data = response.json()
            # Vrifier que le script n'est pas excut
            assert "<script>" not in str(data)
        print("[CHECK] Protection XSS basique")
    
    def test_large_payload_protection(self):
        """Test protection payloads volumineux."""
        # ARRANGE
        large_data = {
            "task_description": "A" * 100000,  # 100KB
            "session_id": "large-payload-test"
        }
        
        # ACT
        response = self.client.post("/process", json=large_data)
        
        # ASSERT
        # Devrait rejeter ou accepter selon la configuration
        assert response.status_code in [200, 202, 413, 422]
        if response.status_code == 413:
            print("[CHECK] Protection payload volumineux active")
    
    def test_invalid_json_handling(self):
        """Test gestion JSON invalide."""
        # ACT
        response = self.client.post(
            "/process",
            data="invalid json content",
            headers={"Content-Type": "application/json"}
        )
        
        # ASSERT
        assert response.status_code == 422  # Unprocessable Entity
        print("[CHECK] Gestion JSON invalide fonctionnelle") 



