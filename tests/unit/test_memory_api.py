"""
Tests unitaires pour l'API de mmoire (memory_api/main.py).

Ce fichier teste tous les endpoints et fonctionnalits de l'API de mmoire :
- Endpoints de base (root, health_check)
- Endpoints de mmoire (store, search, get_all, clear)
- Endpoints d'tat (set, get, get_all, delete, clear)
- Gestion des erreurs et cas limites
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi import HTTPException

# Import direct de l'application
from memory_api.app.main import app
from memory_api.app.models.schemas import MemoryItem, StateItem, SearchQuery, SearchResult


class TestMemoryAPIEndpoints:
    """Tests pour les endpoints de l'API de mmoire."""
    
    @pytest.fixture
    def client(self):
        """Fixture pour crer un client de test FastAPI."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_rag_service(self):
        """Fixture pour mocker le RAGService."""
        with patch('memory_api.app.main.rag_service') as mock:
            yield mock
    
    @pytest.fixture
    def mock_state_service(self):
        """Fixture pour mocker le StateService."""
        with patch('memory_api.app.main.state_service') as mock:
            yield mock


class TestBasicEndpoints(TestMemoryAPIEndpoints):
    """Tests pour les endpoints de base."""
    
    def test_root_endpoint(self, client):
        """Test l'endpoint racine."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Memory API - Environnement Multi-Agent"
    
    def test_health_check_endpoint(self, client):
        """Test l'endpoint de vrification de sant."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "memory_api"


class TestMemoryEndpoints(TestMemoryAPIEndpoints):
    """Tests pour les endpoints de gestion de mmoire."""
    
    def test_store_memory_basic(self, client, mock_rag_service):
        """Test stockage basique d'un lment en mmoire."""
        from datetime import datetime
        mock_memory_item = MemoryItem(
            id=123,
            content="Test content",
            metadata={},
            session_id="session456",
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00")
        )
        mock_rag_service.store_memory = AsyncMock(return_value=mock_memory_item)
        
        response = client.post("/memory/store", params={
            "content": "Test content"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Test content"
        assert data["id"] == 123
        mock_rag_service.store_memory.assert_called_once()
    
    def test_store_memory_with_metadata_and_session(self, client, mock_rag_service):
        """Test stockage d'un lment avec mtadonnes et session."""
        from datetime import datetime
        mock_memory_item = MemoryItem(
            id=456,
            content="Test with metadata",
            metadata={"type": "user_query"},
            session_id="session789",
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00")
        )
        mock_rag_service.store_memory = AsyncMock(return_value=mock_memory_item)
        
        response = client.post("/memory/store", params={
            "content": "Test with metadata",
            "session_id": "session789"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["metadata"]["type"] == "user_query"
        assert data["session_id"] == "session789"
        mock_rag_service.store_memory.assert_called_once()
    
    def test_search_memory(self, client, mock_rag_service):
        """Test recherche dans la mmoire."""
        from datetime import datetime
        mock_search_result = SearchResult(
            items=[
                MemoryItem(
                    id=1,
                    content="Matching content",
                    metadata={},
                    session_id="session1",
                    timestamp=datetime.fromisoformat("2024-01-01T12:00:00")
                )
            ],
            total_count=1
        )
        mock_rag_service.search_memory = AsyncMock(return_value=mock_search_result)
        
        search_query = {
            "query": "test query",
            "session_id": "session1",
            "limit": 10
        }
        
        response = client.post("/memory/search", json=search_query)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 1
        assert len(data["items"]) == 1
        mock_rag_service.search_memory.assert_called_once()
    
    def test_get_all_memories_without_session(self, client, mock_rag_service):
        """Test rcupration de toutes les mmoires sans session."""
        from datetime import datetime
        mock_memories = [
            MemoryItem(
                id=1,
                content="Content 1",
                metadata={},
                session_id="session1",
                timestamp=datetime.fromisoformat("2024-01-01T12:00:00")
            ),
            MemoryItem(
                id=2,
                content="Content 2",
                metadata={},
                session_id="session2",
                timestamp=datetime.fromisoformat("2024-01-01T12:05:00")
            )
        ]
        mock_rag_service.get_all_memories = AsyncMock(return_value=mock_memories)
        
        response = client.get("/memory/all")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["content"] == "Content 1"
        assert data[1]["content"] == "Content 2"
        mock_rag_service.get_all_memories.assert_called_once_with(None)
    
    def test_get_all_memories_with_session(self, client, mock_rag_service):
        """Test rcupration de toutes les mmoires avec session spcifique."""
        from datetime import datetime
        mock_memories = [
            MemoryItem(
                id=1,
                content="Session content",
                metadata={},
                session_id="session123",
                timestamp=datetime.fromisoformat("2024-01-01T12:00:00")
            )
        ]
        mock_rag_service.get_all_memories = AsyncMock(return_value=mock_memories)
        
        response = client.get("/memory/all?session_id=session123")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["session_id"] == "session123"
        mock_rag_service.get_all_memories.assert_called_once_with("session123")
    
    def test_clear_memory_success(self, client, mock_rag_service):
        """Test effacement russi de la mmoire."""
        mock_rag_service.clear_memory = AsyncMock(return_value=True)
        
        response = client.delete("/memory/clear")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Mmoire efface avec succs"
        mock_rag_service.clear_memory.assert_called_once_with(None)
    
    def test_clear_memory_with_session(self, client, mock_rag_service):
        """Test effacement de la mmoire avec session spcifique."""
        mock_rag_service.clear_memory = AsyncMock(return_value=True)
        
        response = client.delete("/memory/clear?session_id=session456")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Mmoire efface avec succs"
        mock_rag_service.clear_memory.assert_called_once_with("session456")
    
    def test_clear_memory_failure(self, client, mock_rag_service):
        """Test chec de l'effacement de la mmoire."""
        mock_rag_service.clear_memory = AsyncMock(return_value=False)
        
        response = client.delete("/memory/clear")
        
        assert response.status_code == 500
        data = response.json()
        assert "Erreur lors de l'effacement de la mmoire" in data["detail"]
        mock_rag_service.clear_memory.assert_called_once()


class TestStateEndpoints(TestMemoryAPIEndpoints):
    """Tests pour les endpoints de gestion d'tat."""
    
    def test_set_state_basic(self, client, mock_state_service):
        """Test dfinition basique d'une valeur d'tat."""
        from datetime import datetime
        mock_state_item = StateItem(
            id=1,
            key="config_key",
            value="config_value",
            session_id=None,
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00")
        )
        mock_state_service.set_state = AsyncMock(return_value=mock_state_item)
        
        response = client.post("/state/set", params={
            "key": "config_key",
            "value": "config_value"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["key"] == "config_key"
        assert data["value"] == "config_value"
        mock_state_service.set_state.assert_called_once()
    
    def test_set_state_with_session(self, client, mock_state_service):
        """Test dfinition d'tat avec session spcifique."""
        from datetime import datetime
        mock_state_item = StateItem(
            id=2,
            key="user_pref",
            value="dark_mode",
            session_id="user_session",
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00")
        )
        mock_state_service.set_state = AsyncMock(return_value=mock_state_item)
        
        response = client.post("/state/set", params={
            "key": "user_pref",
            "value": "dark_mode",
            "session_id": "user_session"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "user_session"
        mock_state_service.set_state.assert_called_once()
    
    def test_get_state_found(self, client, mock_state_service):
        """Test rcupration russie d'une valeur d'tat."""
        from datetime import datetime
        mock_state_item = StateItem(
            id=3,
            key="found_key",
            value="found_value",
            session_id="session123",
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00")
        )
        mock_state_service.get_state = AsyncMock(return_value=mock_state_item)
        
        response = client.get("/state/get?key=found_key")
        
        assert response.status_code == 200
        data = response.json()
        assert data["key"] == "found_key"
        assert data["value"] == "found_value"
        mock_state_service.get_state.assert_called_once_with("found_key", None)
    
    def test_get_state_with_session(self, client, mock_state_service):
        """Test rcupration d'tat avec session spcifique."""
        from datetime import datetime
        mock_state_item = StateItem(
            id=4,
            key="session_key",
            value="session_value",
            session_id="specific_session",
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00")
        )
        mock_state_service.get_state = AsyncMock(return_value=mock_state_item)
        
        response = client.get("/state/get?key=session_key&session_id=specific_session")
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "specific_session"
        mock_state_service.get_state.assert_called_once_with("session_key", "specific_session")
    
    def test_get_state_not_found(self, client, mock_state_service):
        """Test rcupration d'tat non trouv."""
        mock_state_service.get_state = AsyncMock(return_value=None)
        
        response = client.get("/state/get?key=nonexistent_key")
        
        assert response.status_code == 404
        data = response.json()
        assert "tat non trouv" in data["detail"]
        mock_state_service.get_state.assert_called_once()
    
    def test_get_all_state_without_session(self, client, mock_state_service):
        """Test rcupration de tout l'tat sans session."""
        from datetime import datetime
        mock_states = [
            StateItem(
                id=5,
                key="key1",
                value="value1",
                session_id="session1",
                timestamp=datetime.fromisoformat("2024-01-01T12:00:00")
            ),
            StateItem(
                id=6,
                key="key2",
                value="value2",
                session_id="session2",
                timestamp=datetime.fromisoformat("2024-01-01T12:05:00")
            )
        ]
        mock_state_service.get_all_state = AsyncMock(return_value=mock_states)
        
        response = client.get("/state/all")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["key"] == "key1"
        assert data[1]["key"] == "key2"
        mock_state_service.get_all_state.assert_called_once_with(None)
    
    def test_get_all_state_with_session(self, client, mock_state_service):
        """Test rcupration de tout l'tat avec session spcifique."""
        mock_states = [
            StateItem(
                key="session_key",
                value="session_value",
                session_id="target_session",
                timestamp="2024-01-01T12:00:00Z"
            )
        ]
        mock_state_service.get_all_state = AsyncMock(return_value=mock_states)
        
        response = client.get("/state/all?session_id=target_session")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["session_id"] == "target_session"
        mock_state_service.get_all_state.assert_called_once_with("target_session")
    
    def test_delete_state_success(self, client, mock_state_service):
        """Test suppression russie d'une valeur d'tat."""
        mock_state_service.delete_state = AsyncMock(return_value=True)
        
        response = client.delete("/state/delete?key=key_to_delete")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "tat supprim avec succs"
        mock_state_service.delete_state.assert_called_once_with("key_to_delete", None)
    
    def test_delete_state_with_session(self, client, mock_state_service):
        """Test suppression d'tat avec session spcifique."""
        mock_state_service.delete_state = AsyncMock(return_value=True)
        
        response = client.delete("/state/delete?key=session_key&session_id=session123")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "tat supprim avec succs"
        mock_state_service.delete_state.assert_called_once_with("session_key", "session123")
    
    def test_delete_state_not_found(self, client, mock_state_service):
        """Test suppression d'tat non trouv."""
        mock_state_service.delete_state = AsyncMock(return_value=False)
        
        response = client.delete("/state/delete?key=nonexistent_key")
        
        assert response.status_code == 404
        data = response.json()
        assert "tat non trouv" in data["detail"]
        mock_state_service.delete_state.assert_called_once()
    
    def test_clear_state_success(self, client, mock_state_service):
        """Test effacement russi de l'tat."""
        mock_state_service.clear_state = AsyncMock(return_value=True)
        
        response = client.delete("/state/clear")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "tat effac avec succs"
        mock_state_service.clear_state.assert_called_once_with(None)
    
    def test_clear_state_with_session(self, client, mock_state_service):
        """Test effacement d'tat avec session spcifique."""
        mock_state_service.clear_state = AsyncMock(return_value=True)
        
        response = client.delete("/state/clear?session_id=session789")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "tat effac avec succs"
        mock_state_service.clear_state.assert_called_once_with("session789")
    
    def test_clear_state_failure(self, client, mock_state_service):
        """Test chec de l'effacement d'tat."""
        mock_state_service.clear_state = AsyncMock(return_value=False)
        
        response = client.delete("/state/clear")
        
        assert response.status_code == 500
        data = response.json()
        assert "Erreur lors de l'effacement de l'tat" in data["detail"]
        mock_state_service.clear_state.assert_called_once()


class TestErrorHandling(TestMemoryAPIEndpoints):
    """Tests pour la gestion d'erreurs."""
    
    def test_store_memory_service_exception(self, client, mock_rag_service):
        """Test gestion d'exception du service lors du stockage."""
        mock_rag_service.store_memory = AsyncMock(side_effect=Exception("Service error"))
        
        response = client.post("/memory/store", json={
            "content": "Test content"
        })
        
        assert response.status_code == 500
    
    def test_search_memory_service_exception(self, client, mock_rag_service):
        """Test gestion d'exception du service lors de la recherche."""
        mock_rag_service.search_memory = AsyncMock(side_effect=Exception("Search error"))
        
        response = client.post("/memory/search", json={
            "query": "test query"
        })
        
        assert response.status_code == 500
    
    def test_set_state_service_exception(self, client, mock_state_service):
        """Test gestion d'exception du service lors de la dfinition d'tat."""
        mock_state_service.set_state = AsyncMock(side_effect=Exception("State error"))
        
        response = client.post("/state/set", json={
            "key": "test_key",
            "value": "test_value"
        })
        
        assert response.status_code == 500
    
    def test_get_state_service_exception(self, client, mock_state_service):
        """Test gestion d'exception du service lors de la rcupration d'tat."""
        mock_state_service.get_state = AsyncMock(side_effect=Exception("Get state error"))
        
        response = client.get("/state/get?key=test_key")
        
        assert response.status_code == 500


class TestEdgeCases(TestMemoryAPIEndpoints):
    """Tests pour les cas limites."""
    
    def test_store_memory_empty_content(self, client, mock_rag_service):
        """Test stockage avec contenu vide."""
        mock_memory_item = MemoryItem(
            id="mem_empty",
            content="",
            metadata={},
            session_id=None,
            timestamp="2024-01-01T12:00:00Z"
        )
        mock_rag_service.store_memory = AsyncMock(return_value=mock_memory_item)
        
        response = client.post("/memory/store", json={
            "content": ""
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == ""
    
    def test_search_memory_empty_query(self, client, mock_rag_service):
        """Test recherche avec requte vide."""
        mock_search_result = SearchResult(
            query="",
            results=[],
            total_results=0
        )
        mock_rag_service.search_memory = AsyncMock(return_value=mock_search_result)
        
        response = client.post("/memory/search", json={
            "query": ""
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == ""
        assert data["total_results"] == 0
    
    def test_set_state_empty_values(self, client, mock_state_service):
        """Test dfinition d'tat avec valeurs vides."""
        mock_state_item = StateItem(
            key="",
            value="",
            session_id=None,
            timestamp="2024-01-01T12:00:00Z"
        )
        mock_state_service.set_state = AsyncMock(return_value=mock_state_item)
        
        response = client.post("/state/set", json={
            "key": "",
            "value": ""
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["key"] == ""
        assert data["value"] == ""
    
    def test_get_all_memories_empty_result(self, client, mock_rag_service):
        """Test rcupration de toutes les mmoires avec rsultat vide."""
        mock_rag_service.get_all_memories = AsyncMock(return_value=[])
        
        response = client.get("/memory/all")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    def test_get_all_state_empty_result(self, client, mock_state_service):
        """Test rcupration de tout l'tat avec rsultat vide."""
        mock_state_service.get_all_state = AsyncMock(return_value=[])
        
        response = client.get("/state/all")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []


class TestParameterValidation(TestMemoryAPIEndpoints):
    """Tests pour la validation des paramtres."""
    
    def test_missing_content_parameter(self, client):
        """Test requte sans paramtre content requis."""
        response = client.post("/memory/store", json={})
        
        # FastAPI devrait retourner une erreur de validation
        assert response.status_code == 422
    
    def test_missing_key_parameter_set_state(self, client):
        """Test dfinition d'tat sans paramtre key requis."""
        response = client.post("/state/set", json={
            "value": "test_value"
        })
        
        assert response.status_code == 422
    
    def test_missing_value_parameter_set_state(self, client):
        """Test dfinition d'tat sans paramtre value requis."""
        response = client.post("/state/set", json={
            "key": "test_key"
        })
        
        assert response.status_code == 422
    
    def test_missing_query_parameter_search(self, client):
        """Test recherche sans paramtre query requis."""
        response = client.post("/memory/search", json={})
        
        assert response.status_code == 422
    
    def test_missing_key_parameter_get_state(self, client):
        """Test rcupration d'tat sans paramtre key requis."""
        response = client.get("/state/get")
        
        assert response.status_code == 422
    
    def test_missing_key_parameter_delete_state(self, client):
        """Test suppression d'tat sans paramtre key requis."""
        response = client.delete("/state/delete")
        
        assert response.status_code == 422


@pytest.mark.unit
class TestIntegrationScenarios(TestMemoryAPIEndpoints):
    """Tests d'intgration pour des scnarios ralistes."""
    
    def test_complete_memory_workflow(self, client, mock_rag_service):
        """Test workflow complet de gestion de mmoire."""
        # Setup des mocks
        mock_memory_item = MemoryItem(
            id="workflow_mem",
            content="Workflow content",
            metadata={"type": "workflow"},
            session_id="workflow_session",
            timestamp="2024-01-01T12:00:00Z"
        )
        mock_search_result = SearchResult(
            query="workflow",
            results=[mock_memory_item],
            total_results=1
        )
        
        mock_rag_service.store_memory = AsyncMock(return_value=mock_memory_item)
        mock_rag_service.search_memory = AsyncMock(return_value=mock_search_result)
        mock_rag_service.get_all_memories = AsyncMock(return_value=[mock_memory_item])
        mock_rag_service.clear_memory = AsyncMock(return_value=True)
        
        # 1. Stocker une mmoire
        response = client.post("/memory/store", json={
            "content": "Workflow content",
            "metadata": {"type": "workflow"},
            "session_id": "workflow_session"
        })
        assert response.status_code == 200
        
        # 2. Rechercher la mmoire
        response = client.post("/memory/search", json={
            "query": "workflow",
            "session_id": "workflow_session"
        })
        assert response.status_code == 200
        assert response.json()["total_results"] == 1
        
        # 3. Rcuprer toutes les mmoires
        response = client.get("/memory/all?session_id=workflow_session")
        assert response.status_code == 200
        assert len(response.json()) == 1
        
        # 4. Effacer la mmoire
        response = client.delete("/memory/clear?session_id=workflow_session")
        assert response.status_code == 200
    
    def test_complete_state_workflow(self, client, mock_state_service):
        """Test workflow complet de gestion d'tat."""
        # Setup des mocks
        mock_state_item = StateItem(
            key="workflow_key",
            value="workflow_value",
            session_id="state_session",
            timestamp="2024-01-01T12:00:00Z"
        )
        
        mock_state_service.set_state = AsyncMock(return_value=mock_state_item)
        mock_state_service.get_state = AsyncMock(return_value=mock_state_item)
        mock_state_service.get_all_state = AsyncMock(return_value=[mock_state_item])
        mock_state_service.delete_state = AsyncMock(return_value=True)
        mock_state_service.clear_state = AsyncMock(return_value=True)
        
        # 1. Dfinir un tat
        response = client.post("/state/set", json={
            "key": "workflow_key",
            "value": "workflow_value",
            "session_id": "state_session"
        })
        assert response.status_code == 200
        
        # 2. Rcuprer l'tat
        response = client.get("/state/get?key=workflow_key&session_id=state_session")
        assert response.status_code == 200
        assert response.json()["value"] == "workflow_value"
        
        # 3. Rcuprer tout l'tat
        response = client.get("/state/all?session_id=state_session")
        assert response.status_code == 200
        assert len(response.json()) == 1
        
        # 4. Supprimer l'tat spcifique
        response = client.delete("/state/delete?key=workflow_key&session_id=state_session")
        assert response.status_code == 200
        
        # 5. Effacer tout l'tat
        response = client.delete("/state/clear?session_id=state_session")
        assert response.status_code == 200


class TestApplicationConfiguration:
    """Tests pour la configuration de l'application."""
    
    def test_app_metadata(self):
        """Test les mtadonnes de l'application FastAPI."""
        assert app.title == "Memory API"
        assert app.description == "API pour la gestion de mmoire et d'tat dans l'environnement multi-agent"
        assert app.version == "1.0.0"
    
    def test_app_type(self):
        """Test que l'application est bien une instance FastAPI."""
        from fastapi import FastAPI
        assert isinstance(app, FastAPI)


class TestServiceInitialization:
    """Tests pour l'initialisation des services."""
    
    def test_services_imported(self):
        """Test que les services sont correctement imports."""
        from memory_api.app.main import rag_service, state_service
        assert rag_service is not None
        assert state_service is not None
    
    def test_services_type(self):
        """Test le type des services (ncessite que les classes soient dfinies)."""
        from memory_api.app.main import rag_service, state_service
        # Ces assertions ncessitent que les services soient correctement implments
        assert hasattr(rag_service, 'store_memory')
        assert hasattr(rag_service, 'search_memory')
        assert hasattr(state_service, 'set_state')
        assert hasattr(state_service, 'get_state') 