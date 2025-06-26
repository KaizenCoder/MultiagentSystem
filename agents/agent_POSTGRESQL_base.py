"""
Classe de base pour tous les agents PostgreSQL
"""

from pathlib import Path
from datetime import datetime
import logging
from core.agent_factory_architecture import Agent, Task, Result

class AgentPostgreSQLBase(Agent):
    """
    Classe de base pour tous les agents PostgreSQL.
    Implémente les méthodes communes et l'interface Agent.
    """
    
    def __init__(self, agent_type: str, name: str, **config):
        super().__init__(agent_type=agent_type, **config)
        self.name = name
        self.version = "2.0.0"
        self.workspace_root = Path(__file__).parent.parent
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Configuration du logging pour l'agent."""
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            log_dir = self.workspace_root / "logs" / "agents" / self.type
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f'{self.type}.log'
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger
    
    async def startup(self) -> None:
        """Initialisation de l'agent"""
        try:
            self.logger.info(f"Démarrage {self.name}")
        except Exception as e:
            self.logger.error(f"Erreur démarrage: {e}")
            raise

    async def shutdown(self) -> None:
        """Arrêt propre de l'agent"""
        try:
            self.logger.info(f"Arrêt {self.name}")
        except Exception as e:
            self.logger.error(f"Erreur arrêt: {e}")
            raise

    async def health_check(self) -> dict:
        """Vérification santé de l'agent"""
        try:
            return {
                "status": "healthy",
                "agent": self.name,
                "type": self.type,
                "version": self.version,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def get_capabilities(self) -> list:
        """Liste des capacités de l'agent"""
        return [
            "diagnostic",
            "monitoring",
            "configuration",
            "documentation"
        ]

    def execute_task(self, task: Task) -> Result:
        """
        Exécution d'une tâche selon le Pattern Factory.
        À implémenter dans les classes filles.
        """
        raise NotImplementedError("Cette méthode doit être implémentée dans les classes filles") 