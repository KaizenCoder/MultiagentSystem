"""
NextGeneration main.py - Architecture Modulaire
Refactorisé depuis god mode (1,990 lignes → ~80 lignes)
Pattern: Hexagonal Architecture + CQRS
Généré: 2025-06-18 15:27:27
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import routers modulaires
from .routers import api_router, health_router, auth_router
from .dependencies import get_database, get_cache_manager, get_services_container
from .services import ServiceContainer
from .config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion cycle de vie application"""
    # Startup
    print("🚀 NextGeneration démarrage...")
    services = get_services_container()
    await services.initialize_all()
    
    yield
    
    # Shutdown
    print("🛑 NextGeneration arrêt...")
    await services.cleanup_all()

# Application FastAPI modulaire
app = FastAPI(
    title="NextGeneration Orchestrator",
    description="Architecture Modulaire - Refactorisé depuis god mode",
    version="2.0.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers modulaires (remplace god mode routes)
app.include_router(health_router.router)
app.include_router(auth_router.router)
app.include_router(api_router.router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint - Architecture modulaire"""
    return {
        "message": "NextGeneration Orchestrator",
        "architecture": "Hexagonal + CQRS",
        "status": "Refactorisé depuis god mode",
        "lignes_avant": 1990,
        "lignes_apres": "~80",
        "reduction": "96%"
    }

# Health check simple
@app.get("/health")
async def health_check():
    """Health check - Version modulaire"""
    return {"status": "healthy", "architecture": "modular"}
