import os
import pytest
import logging
from pathlib import Path

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("migration_tests")

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configuration globale environnement de test"""
    logger.info("🔧 Configuration environnement de test global")
    
    # Vérification répertoire de travail
    work_dir = Path(os.getcwd())
    assert work_dir.name == "suivi_plan_implementation", \
        f"Tests doivent être exécutés depuis le répertoire suivi_plan_implementation, pas {work_dir}"
    
    # Configuration environnement
    os.environ["TEST_ENV"] = "validation"
    os.environ["LOG_LEVEL"] = "INFO"
    
    yield
    
    logger.info("✅ Tests terminés") 