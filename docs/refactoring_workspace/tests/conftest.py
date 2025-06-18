"""Configuration tests refactoring"""

import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def test_client():
    """Client test FastAPI"""
    from main import app
    return TestClient(app)
