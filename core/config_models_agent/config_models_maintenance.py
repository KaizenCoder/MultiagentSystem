"""
Modèles de Configuration Pydantic Statiques pour l'Équipe de Maintenance

Ce fichier définit la **structure** de la configuration de l'équipe de maintenance.
Il n'est pas généré dynamiquement. Les valeurs de configuration seront chargées
depuis un fichier de données (ex: .json) par ces modèles.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, FilePath
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

# Définir le chemin de base pour la configuration
# Cela permet de le rendre portable et non dépendant du lieu d'exécution.
CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "config"
CONFIG_FILE_PATH = CONFIG_DIR / "maintenance_config.json"


class AgentConfig(BaseSettings):
    """Configuration pour un agent de maintenance individuel."""
    nom_agent: str = Field(..., description="Le nom de fichier du script de l'agent.")
    classe_agent: str = Field(..., description="Le nom de la classe de l'agent à instancier.")
    description: str = ""
    entry_point: Optional[str] = Field(None, description="Point d'entrée pour la factory, ex: 'agents.agent:create_agent'")

class MaintenanceTeamConfig(BaseSettings):
    """Configuration complète pour l'équipe de maintenance."""
    
    # Configuration des agents membres de l'équipe
    agents: Dict[str, AgentConfig] = Field(..., description="Dictionnaire des agents de l'équipe, la clé est le rôle.")

    # Configuration du workflow
    workflows_disponibles: List[str] = ["maintenance_complete"]
    rapport_final_path: str = "reports/maintenance_workflow_report.json"

    # Configuration Pydantic pour charger depuis un fichier JSON
    model_config = SettingsConfigDict(
        # Indique à Pydantic de lire les valeurs depuis un fichier JSON.
        # Le chemin est construit de manière relative au projet.
        json_file=str(CONFIG_FILE_PATH),
        json_file_encoding='utf-8',
        # Permet de gérer les champs supplémentaires non définis dans le modèle
        extra='ignore'
    )

def get_maintenance_config() -> MaintenanceTeamConfig:
    """
    Charge et valide la configuration de maintenance depuis le fichier JSON.
    """
    if not CONFIG_FILE_PATH.exists():
        raise FileNotFoundError(f"Fichier de configuration introuvable: {CONFIG_FILE_PATH}")
    
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
        
    return MaintenanceTeamConfig(**config_data)

if __name__ == "__main__":
    print(f"Tentative de chargement du fichier de configuration : {CONFIG_FILE_PATH}")
    
    try:
        config = get_maintenance_config()
        print("\n✅ Configuration chargée avec succès !")
        print("\nAgents configurés:")
        for role, agent_conf in config.agents.items():
            print(f"  - Rôle: {role}")
            print(f"    Classe: {agent_conf.classe_agent}")
            if agent_conf.entry_point:
                print(f"    EntryPoint: {agent_conf.entry_point}")
        
    except FileNotFoundError as e:
        print(f"\n❌ Erreur: {e}")
    except Exception as e:
        print(f"\n❌ Erreur de validation ou de chargement: {e}") 