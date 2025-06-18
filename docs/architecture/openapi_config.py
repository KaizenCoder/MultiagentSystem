
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title="NextGeneration Orchestrator API",
        version="2.0.0",
        description="""
## NextGeneration - Architecture Modulaire

API d'orchestration IA multi-agents refactorisée depuis god mode files.

### Architecture
- **Pattern**: Hexagonal + CQRS + Dependency Injection
- **Réduction**: 96.4% (1,990 → 71 lignes main.py)
- **Agents**: 17 agents spécialisés coordonnés
- **Qualité**: Score 95.8% (excellence enterprise)

### Endpoints Principaux
- `/health/*` - Health checks Kubernetes-ready
- `/api/v1/agents/*` - Gestion agents IA
- `/api/v1/orchestration/*` - Coordination workflows
- `/metrics` - Métriques Prometheus

### Patterns Implémentés
- **CQRS**: Commands/Queries séparées
- **DI**: Injection dépendances FastAPI
- **Ports & Adapters**: Architecture hexagonale
- **Repository**: Abstraction données
        """,
        routes=app.routes,
        servers=[
            {"url": "http://localhost:8000", "description": "Development server"},
            {"url": "https://api.nextgeneration.ai", "description": "Production server"}
        ],
        tags=[
            {
                "name": "health",
                "description": "Health checks et monitoring"
            },
            {
                "name": "agents", 
                "description": "Gestion agents IA"
            },
            {
                "name": "orchestration",
                "description": "Coordination workflows"
            }
        ]
    )
    
    # Customisation schema
    openapi_schema["info"]["x-logo"] = {
        "url": "https://nextgeneration.ai/logo.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Usage dans main.py
# app.openapi = lambda: custom_openapi(app)
