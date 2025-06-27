import os
import sys
import pytest

# Ajout du répertoire racine au PYTHONPATH
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

@pytest.fixture(scope="session")
def adaptateur_root():
    """Retourne le chemin racine de l'adaptateur"""
    return root_dir

@pytest.fixture(scope="session")
def metrics_endpoint():
    """URL de l'endpoint des métriques"""
    return "http://localhost:9090/metrics"

@pytest.fixture(scope="session")
def grafana_endpoint():
    """URL de l'endpoint Grafana"""
    return "http://localhost:3000" 