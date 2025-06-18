"""
Security Schemas Schemas - NextGeneration Refactored
Modèles Pydantic Security Schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

class SecuritySchemasRequest(BaseModel):
    """Requête Security Schemas"""
    # TODO: Définir champs requête
    pass

class SecuritySchemasResponse(BaseModel):
    """Réponse Security Schemas"""
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
