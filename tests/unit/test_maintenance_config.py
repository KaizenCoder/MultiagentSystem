"""
Tests de validation pour la configuration de maintenance (maintenance_config.json)
Généré par Agent 03 - Spécialiste Configuration
"""

import pytest
import json
from pathlib import Path
import sys

try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core.config_models_agent.config_models_maintenance import MaintenanceTeamConfig, CONFIG_FILE_PATH
from pydantic import ValidationError

CONFIG_FILE = CONFIG_FILE_PATH

def test_config_file_exists():
    """Vérifie que le fichier de configuration JSON existe."""
    assert CONFIG_FILE.exists(), f"Le fichier de configuration {CONFIG_FILE} est manquant."

def test_config_is_valid_json():
    """Vérifie que le fichier est un JSON valide."""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        try:
            json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Le fichier de configuration n'est pas un JSON valide.")

def test_config_conforms_to_schema():
    """Vérifie que la configuration est conforme au schéma Pydantic."""
    try:
        MaintenanceTeamConfig()
    except ValidationError as e:
        pytest.fail(f"La configuration JSON ne correspond pas au schéma Pydantic: \n{e}")
    except FileNotFoundError:
        pytest.fail("L'instanciation de MaintenanceTeamConfig n'a pas trouvé le fichier.")

def test_all_agents_have_required_fields():
    """Vérifie que chaque agent dans la configuration a les champs requis."""
    config = MaintenanceTeamConfig()
    for role, agent_conf in config.agents.items():
        assert hasattr(agent_conf, 'nom_agent') and agent_conf.nom_agent, f"L'agent '{role}' n'a pas de 'nom_agent'."
        assert hasattr(agent_conf, 'classe_agent') and agent_conf.classe_agent, f"L'agent '{role}' n'a pas de 'classe_agent'."
