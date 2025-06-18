"""
Template Service base - NextGeneration  
Pattern standard pour tous les services
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class BaseService(ABC):
    """Classe base pour tous les services"""
    
    def __init__(self):
        self._initialized = False
        self._setup()
    
    def _setup(self):
        """Setup service - À override"""
        self._initialized = True
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """Méthode principale - À implémenter"""
        pass
    
    def is_ready(self) -> bool:
        """Vérifie si service prêt"""
        return self._initialized
