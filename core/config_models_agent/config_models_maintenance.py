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
    module: str = Field(..., description="Le chemin du module Python de l'agent, ex: 'agents.agent_01'")
    class_name: str = Field(..., alias='class', description="Le nom de la classe de l'agent à instancier.")
    factory_function: str = Field(..., description="La fonction factory pour créer l'agent.")
    config: Dict[str, Any] = Field({}, description="Configuration spécifique à l'agent.")

class FactoryConfig(BaseSettings):
    """Configuration pour la factory elle-même."""
    max_concurrent_agents: int = 10
    default_timeout_seconds: int = 60
    log_level: str = "INFO"

class HvacConfig(BaseSettings):
    """Configuration pour le client HashiCorp Vault."""
    vault_url: str
    vault_token: str

class JwtConfig(BaseSettings):
    """Configuration pour la génération de tokens JWT."""
    secret_key: str
    algorithm: str

class RsaConfig(BaseSettings):
    """Configuration pour la génération de clés RSA."""
    key_size: int

class ToolsConfig(BaseSettings):
    """Configuration pour les outils partagés."""
    hvac: HvacConfig
    jwt: JwtConfig
    rsa: RsaConfig

class MaintenanceTeamConfig(BaseSettings):
    """Configuration complète pour l'équipe de maintenance."""
    
    factory_config: FactoryConfig
    agents: Dict[str, AgentConfig] = Field(..., description="Dictionnaire des agents de l'équipe, la clé est le rôle.")
    tools: ToolsConfig

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
            print(f"    Classe: {agent_conf.class_name}")
            if agent_conf.factory_function:
                print(f"    EntryPoint: {agent_conf.factory_function}")
        
    except FileNotFoundError as e:
        print(f"\n❌ Erreur: {e}")
    except Exception as e:
        print(f"\n❌ Erreur de validation ou de chargement: {e}") 