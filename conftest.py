import pytest
import logging

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configuration globale environnement de test"""
    yield 