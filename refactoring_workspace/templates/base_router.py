"""
Template Router base - NextGeneration
Pattern standard pour tous les routers
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Dict

router = APIRouter()

class BaseRouter:
    """Classe base pour tous les routers"""
    
    def __init__(self, prefix: str, tags: list = None):
        self.router = APIRouter(prefix=prefix, tags=tags or [])
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup routes spécifiques - À override"""
        pass
    
    def get_router(self) -> APIRouter:
        """Retourne router configuré"""
        return self.router
