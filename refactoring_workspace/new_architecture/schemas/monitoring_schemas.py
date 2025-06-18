"""
Monitoring Schemas Schemas - NextGeneration Refactored
Modèles Pydantic Monitoring Schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

class MonitoringSchemasRequest(BaseModel):
    """Requête Monitoring Schemas"""
    # TODO: Définir champs requête
    pass

class MonitoringSchemasResponse(BaseModel):
    """Réponse Monitoring Schemas"""
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
