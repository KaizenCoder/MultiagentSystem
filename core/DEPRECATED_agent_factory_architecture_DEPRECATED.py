"""
🏭 ARCHITECTURE PATTERN FACTORY - Version Production (Simplifiée)
================================================================
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Type, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
import sys
from pathlib import Path
import importlib
import logging
import uuid

# --- Configuration du Logging ---
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Interfaces de Base ---

@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Result:
    success: bool
    data: Any = None
    error: Optional[str] = None

class Agent(ABC):
    def __init__(self, **kwargs):
        self.role = kwargs.get("role", "unknown")
        self.agent_id = kwargs.get("agent_id", f"{self.role}_{uuid.uuid4().hex[:4]}")
        self.version = kwargs.get("version", "0.0.0")
        self.description = kwargs.get("description", "")
        self.agent_type = kwargs.get("agent_type", self.role)
        
        self.logger = logging.getLogger(f"agent.{self.agent_type}")
        self.logger.info(f"Agent {self.agent_id} ({self.agent_type}) initialisé.")

    async def startup(self):
        self.logger.info(f"{self.agent_id} démarré.")

    async def shutdown(self):
        self.logger.info(f"{self.agent_id} arrêté.")

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def execute_task(self, task: Task) -> Result:
        pass

    def log(self, message: str, level: str = "info", **kwargs):
        log_func = getattr(self.logger, level, self.logger.info)
        log_func(f"[{self.agent_id}] {message}", **kwargs)

# --- Coeur de la Factory ---

class AgentFactory:
    """
    Crée des instances d'agents en se basant sur un fichier de configuration
    qui mappe des rôles à des points d'entrée (entry_point).
    """
    def __init__(self, config_path: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._agents_creators: Dict[str, Callable] = {}
        self._load_config(config_path)
        self.logger.info(f"AgentFactory initialisée avec {len(self._agents_creators)} types d'agents.")

    def _load_config(self, config_path: str):
        self.logger.info(f"Chargement de la configuration depuis {config_path}")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            agents_config = config_data.get('agents', {})
            self.logger.info(f"Enregistrement de {len(agents_config)} agents...")
            
            for role, agent_details in agents_config.items():
                entry_point = agent_details.get("entry_point")
                if not entry_point:
                    self.logger.warning(f"Pas de 'entry_point' pour le rôle '{role}'. Agent ignoré.")
                    continue
                
                try:
                    module_name, func_name = entry_point.split(':')
                    module = importlib.import_module(module_name)
                    create_func = getattr(module, func_name)
                    self._agents_creators[role] = create_func
                    self.logger.info(f"  -> Rôle '{role}' enregistré avec la fonction '{func_name}'.")
                except (ImportError, AttributeError, ValueError) as e:
                    self.logger.error(f"Impossible de charger l'agent pour le rôle '{role}' depuis '{entry_point}': {e}")

        except FileNotFoundError:
            self.logger.error(f"Fichier de configuration introuvable: {config_path}")
        except json.JSONDecodeError:
            self.logger.error(f"Erreur de décodage JSON dans {config_path}")
        except Exception as e:
            self.logger.error(f"Erreur inattendue lors du chargement de la configuration: {e}", exc_info=True)

    async def create_agent(self, role: str, startup: bool = False, **kwargs) -> Optional[Agent]:
        """Crée une instance d'agent pour un rôle donné."""
        create_func = self._agents_creators.get(role)
        if not create_func:
            self.logger.error(f"Aucune fonction de création trouvée pour le rôle : '{role}'")
            return None
            
        try:
            # Passe le rôle et les autres kwargs à la fonction de création
            agent_instance = create_func(role=role, **kwargs)
            self.logger.info(f"Agent {agent_instance.__class__.__name__} (rôle: {role}) créé.")
            
            if startup:
                await agent_instance.startup()
            
            return agent_instance
        except Exception as e:
            self.logger.error(f"Erreur lors de la création de l'agent pour le rôle '{role}': {e}", exc_info=True)
            return None 