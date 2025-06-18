#!/usr/bin/env python3
"""
🧪 Configuration globale tests - conftest.py
Fixtures partagées pour tous les tests
Générée automatiquement - 2025-06-18 17:40:41
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any
import sys
from pathlib import Path

# Ajouter paths architecture
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "new_architecture"))

@pytest.fixture(scope="session")
def event_loop():
    """🔄 Event loop pour tests async"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_database():
    """🗄️ Mock base de données"""
    with patch("database.connection") as mock:
        mock.execute = AsyncMock()
        mock.fetch = AsyncMock(return_value=[])
        mock.commit = AsyncMock()
        yield mock

@pytest.fixture  
def mock_redis():
    """🔴 Mock Redis cache"""
    with patch("redis.Redis") as mock:
        mock.get = AsyncMock(return_value=None)
        mock.set = AsyncMock()
        mock.delete = AsyncMock()
        yield mock

@pytest.fixture
def mock_external_api():
    """🌐 Mock APIs externes"""
    with patch("httpx.AsyncClient") as mock:
        mock.get = AsyncMock()
        mock.post = AsyncMock()
        mock.put = AsyncMock()
        mock.delete = AsyncMock()
        yield mock

@pytest.fixture
def test_config():
    """⚙️ Configuration test"""
    return {
        "database_url": "sqlite:///:memory:",
        "redis_url": "redis://localhost:6379/1",
        "api_timeout": 30,
        "max_connections": 10
    }

@pytest.fixture
def sample_data():
    """📊 Données test samples"""
    return {
        "agent": {
            "id": "test-agent-001",
            "name": "Test Agent",
            "status": "active"
        },
        "orchestration": {
            "id": "test-orchestration-001", 
            "agents": ["test-agent-001"],
            "status": "running"
        }
    }

# Marqueurs performance
def pytest_configure(config):
    """🔧 Configuration marqueurs pytest"""
    config.addinivalue_line(
        "markers", "slow: Tests lents (> 1s)"
    )
    config.addinivalue_line(
        "markers", "external: Tests nécessitant services externes"
    )
