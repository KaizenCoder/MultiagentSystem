"""
IHealthService - Interface NextGeneration
Architecture Hexagonale - Contrats de service
Gnr automatiquement par Agent Services Creator
Date: 2025-06-18 15:27:27
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class IHealthService(ABC):
    """
    Interface pour services HealthService
    Respecte Dependency Inversion Principle
    """
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialiser le service"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Vrification sant du service"""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Nettoyage ressources"""
        pass
