#!/usr/bin/env python3
"""
Test simple de l'API de l'orchestrateur
"""

import sys
import os
import asyncio
from pathlib import Path

# Ajouter le répertoire parent au path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Charger la configuration
os.environ['PYTHONPATH'] = str(project_root)
os.chdir(project_root / "orchestrator")

try:
    from orchestrator.app.config import settings
    print("✅ Configuration chargée avec succès")
    print(f"   🔑 OpenAI: {settings.OPENAI_API_KEY[:15]}...")
    print(f"   🔑 Anthropic: {settings.ANTHROPIC_API_KEY[:15]}...")
    print(f"   🔑 Orchestrator: {settings.ORCHESTRATOR_API_KEY}")
except Exception as e:
    print(f"❌ Erreur de configuration: {e}")
    sys.exit(1)

# Test simple de création d'application FastAPI
try:
    from fastapi import FastAPI
    
    app = FastAPI(title="Test Orchestrator", version="1.0")
    
    @app.get("/")
    async def root():
        return {"message": "Orchestrateur fonctionne!", "status": "ok"}
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "openai_configured": bool(settings.OPENAI_API_KEY),
            "anthropic_configured": bool(settings.ANTHROPIC_API_KEY)
        }
    
    print("✅ Application FastAPI créée")
    
    # Démarrer le serveur
    import uvicorn
    print("\n🚀 Démarrage du serveur de test...")
    print("📍 URL: http://localhost:8002")
    print("⏹️  Utilisez Ctrl+C pour arrêter")
    
    uvicorn.run(app, host="0.0.0.0", port=8002)
    
except Exception as e:
    print(f"❌ Erreur lors du démarrage: {e}")
    sys.exit(1)
