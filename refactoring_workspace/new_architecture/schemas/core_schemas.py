"""
Core Schemas Schemas - NextGeneration Refactored
Modèles Pydantic Core Schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

class CoreSchemasRequest(BaseModel):
    """Requête Core Schemas"""
    # TODO: Définir champs requête
    pass

class CoreSchemasResponse(BaseModel):
    """Réponse Core Schemas"""
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
