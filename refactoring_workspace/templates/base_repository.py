"""
Template Repository base - NextGeneration
Pattern standard pour accès données
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseRepository(ABC):
    """Classe base pour tous les repositories"""
    
    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string
        self._connection = None
    
    @abstractmethod
    async def connect(self):
        """Connexion - À implémenter"""
        pass
    
    @abstractmethod
    async def disconnect(self):
        """Déconnexion - À implémenter"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Vérification santé - À implémenter"""
        pass
