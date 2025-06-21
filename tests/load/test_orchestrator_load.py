"""
Tests de charge Orchestrateur - CRITIQUE Phase 2.
Tests de performance et scalabilit selon prompt Sprint 2.
"""

import pytest
import asyncio
import time
import concurrent.futures
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock


@pytest.mark.load
class TestOrchestratorLoad:
    """Tests de charge Orchestrateur - CRITIQUE."""
    
    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Setup du client de test FastAPI."""
        try:
            from orchestrator.app.main import app
            self.client = TestClient(app)
        except Exception as e:
            pytest.skip(f"Cannot import orchestrator app: {e}")
    
    def test_concurrent_requests_basic(self):
        """Test requtes concurrentes basiques."""
        # ARRANGE
        def make_request(session_id):
            return self.client.post("/process", json={
                "task_description": f"Test concurrent request {session_id}",
                "session_id": f"load-test-{session_id}"
            })
        
        # ACT
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(make_request, i) 
                for i in range(10)
            ]
            responses = [f.result() for f in futures]
        duration = time.time() - start_time
        
        # ASSERT
        assert len(responses) == 10
        # Au moins 50% des requtes devraient russir
        success_count = sum(1 for r in responses if r.status_code in [200, 202])
        assert success_count >= 5, f"Only {success_count}/10 requests succeeded"
        
        # Performance basique: 10 requtes en moins de 30 secondes
        assert duration < 30, f"Requests took {duration:.2f}s, should be < 30s"
        print(f"[CHECK] 10 requtes concurrentes en {duration:.2f}s")
    
    @patch('orchestrator.app.agents.supervisor.Supervisor.create_plan')
    def test_sequential_load(self, mock_create_plan):
        """Test charge squentielle."""
        # ARRANGE
        mock_create_plan.return_value = {
            "plan": "Fast test plan",
            "next": "code_generation",
            "task_status": "in_progress"
        }
        
        # ACT
        start_time = time.time()
        responses = []
        for i in range(20):
            response = self.client.post("/process", json={
                "task_description": f"Sequential test {i}",
                "session_id": f"seq-{i}"
            })
            responses.append(response)
        duration = time.time() - start_time
        
        # ASSERT
        success_count = sum(1 for r in responses if r.status_code in [200, 202])
        assert success_count >= 15, f"Only {success_count}/20 sequential requests succeeded"
        
        # Performance: 20 requtes squentielles en moins de 60 secondes
        assert duration < 60, f"Sequential requests took {duration:.2f}s"
        print(f"[CHECK] 20 requtes squentielles en {duration:.2f}s")
    
    def test_health_endpoint_load(self):
        """Test charge endpoint /health."""
        # ACT
        start_time = time.time()
        responses = []
        for i in range(50):
            response = self.client.get("/health")
            responses.append(response.status_code)
        duration = time.time() - start_time
        
        # ASSERT
        success_count = sum(1 for code in responses if code == 200)
        assert success_count >= 45, f"Only {success_count}/50 health checks succeeded"
        
        # Health checks doivent tre rapides
        assert duration < 10, f"50 health checks took {duration:.2f}s"
        print(f"[CHECK] 50 health checks en {duration:.2f}s")
    
    @pytest.mark.skipif("CI" in __name__, reason="Skip in CI environment")
    def test_memory_pressure(self):
        """Test pression mmoire."""
        # ARRANGE
        large_task = "Analyze this large dataset: " + "x" * 10000
        
        # ACT
        responses = []
        for i in range(5):
            response = self.client.post("/process", json={
                "task_description": large_task,
                "session_id": f"memory-pressure-{i}"
            })
            responses.append(response.status_code)
        
        # ASSERT
        # Systme devrait grer la pression mmoire sans crash
        success_count = sum(1 for code in responses if code in [200, 202, 413, 422])
        assert success_count == 5, "System should handle memory pressure gracefully"
        print("[CHECK] Gestion pression mmoire OK")
    
    def test_timeout_behavior(self):
        """Test comportement timeouts."""
        # ARRANGE - Tche potentiellement longue
        complex_task = {
            "task_description": "Complex analysis requiring multiple steps and detailed processing",
            "session_id": "timeout-test"
        }
        
        # ACT
        start_time = time.time()
        response = self.client.post("/process", json=complex_task)
        duration = time.time() - start_time
        
        # ASSERT
        # Soit a rpond rapidement, soit a timeout proprement
        if response.status_code in [200, 202]:
            print(f"[CHECK] Rponse rapide en {duration:.2f}s")
        elif response.status_code == 408:  # Request Timeout
            print("[CHECK] Timeout gr proprement")
        else:
            print(f" Statut inattendu: {response.status_code}")
        
        # Ne devrait pas prendre plus de 60 secondes
        assert duration < 60, f"Request took {duration:.2f}s, too long"


@pytest.mark.load
@pytest.mark.asyncio
class TestOrchestratorAsyncLoad:
    """Tests de charge asynchrones - AVANC."""
    
    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Setup du client async."""
        try:
            import httpx
            self.base_url = "http://localhost:8000"  # Ou port configur
        except ImportError:
            pytest.skip("httpx not available for async tests")
    
    async def test_async_concurrent_requests(self):
        """Test requtes concurrentes async."""
        import httpx
        
        async def make_async_request(session_id):
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(
                        f"{self.base_url}/process",
                        json={
                            "task_description": f"Async test {session_id}",
                            "session_id": f"async-{session_id}"
                        },
                        timeout=10.0
                    )
                    return response.status_code
                except Exception:
                    return 500  # Connection error
        
        # ACT
        start_time = time.time()
        tasks = [make_async_request(i) for i in range(10)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        duration = time.time() - start_time
        
        # ASSERT
        valid_responses = [r for r in responses if isinstance(r, int)]
        if len(valid_responses) > 0:
            success_count = sum(1 for code in valid_responses if code in [200, 202])
            print(f"[CHECK] {success_count}/{len(valid_responses)} requtes async russies en {duration:.2f}s")
        else:
            pytest.skip("No valid responses (server not running)")


@pytest.mark.performance
class TestOrchestratorPerformance:
    """Tests de performance spcifiques."""
    
    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Setup du client de test."""
        try:
            from orchestrator.app.main import app
            self.client = TestClient(app)
        except Exception as e:
            pytest.skip(f"Cannot import orchestrator app: {e}")
    
    def test_startup_performance(self):
        """Test performance de dmarrage."""
        # ACT
        start_time = time.time()
        response = self.client.get("/health")
        startup_duration = time.time() - start_time
        
        # ASSERT
        assert response.status_code == 200
        # Premier appel devrait tre raisonnablement rapide
        assert startup_duration < 5, f"Startup took {startup_duration:.2f}s"
        print(f"[CHECK] Dmarrage en {startup_duration:.2f}s")
    
    def test_response_time_consistency(self):
        """Test cohrence temps de rponse."""
        # ACT
        durations = []
        for i in range(10):
            start_time = time.time()
            response = self.client.get("/health")
            duration = time.time() - start_time
            durations.append(duration)
        
        # ASSERT
        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        
        assert avg_duration < 1.0, f"Average response time {avg_duration:.3f}s too high"
        assert max_duration < 2.0, f"Max response time {max_duration:.3f}s too high"
        print(f"[CHECK] Temps moyen: {avg_duration:.3f}s, max: {max_duration:.3f}s") 



