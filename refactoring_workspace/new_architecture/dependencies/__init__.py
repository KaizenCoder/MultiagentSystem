"""
Dependencies - NextGeneration Dependency Injection
Architecture Hexagonale - Inversion de contrôle
Généré: 2025-06-18 15:27:27
"""

from typing import Annotated
from fastapi import Depends
from functools import lru_cache

from ..services import ServiceContainer, IOrchestratorService
from ..repositories import DatabaseConnection, CacheManager
from ..config import settings

# Singleton Service Container
@lru_cache()
def get_services_container() -> ServiceContainer:
    """Conteneur services singleton"""
    return ServiceContainer()

# Database Dependencies
async def get_database() -> DatabaseConnection:
    """Connexion base de données"""
    container = get_services_container()
    return await container.get_database()

# Cache Dependencies  
async def get_cache_manager() -> CacheManager:
    """Gestionnaire cache"""
    container = get_services_container()
    return await container.get_cache_manager()

# Service Dependencies
async def get_orchestrator_service(
    container: Annotated[ServiceContainer, Depends(get_services_container)]
) -> IOrchestratorService:
    """Service orchestrateur principal"""
    return await container.get_orchestrator_service()

# Auth Dependencies
async def get_current_user(token: str = None):
    """Utilisateur courant (à implémenter)"""
    # TODO: Implémenter authentification
    return {"user_id": "anonymous"}

# Request Context
async def get_request_context():
    """Contexte requête pour logging/tracing"""
    return {"request_id": "auto-generated"}
