"""
Template Repository base - NextGeneration
Pattern standard pour accs donnes
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
        """Connexion -  implmenter"""
        pass
    
    @abstractmethod
    async def disconnect(self):
        """Dconnexion -  implmenter"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Vrification sant -  implmenter"""
        pass
