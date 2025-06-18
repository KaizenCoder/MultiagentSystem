"""
Database Schemas Schemas - NextGeneration Refactored
Modèles Pydantic Database Schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

class DatabaseSchemasRequest(BaseModel):
    """Requête Database Schemas"""
    # TODO: Définir champs requête
    pass

class DatabaseSchemasResponse(BaseModel):
    """Réponse Database Schemas"""
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
