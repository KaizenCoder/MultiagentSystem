import pytest
import logging
import os

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configuration globale environnement de test"""
    # Configuration environnement
    os.environ["TEST_ENV"] = "validation"
    os.environ["LOG_LEVEL"] = "INFO"
    
    logging.info("🔧 Configuration environnement de test global")
    yield
    logging.info("✅ Tests terminés")