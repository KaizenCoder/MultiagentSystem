"""
Security Schemas Schemas - NextGeneration Refactored
Modles Pydantic Security Schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

class SecuritySchemasRequest(BaseModel):
    """Requte Security Schemas"""
    # TODO: Dfinir champs requte
    pass

class SecuritySchemasResponse(BaseModel):
    """Rponse Security Schemas"""
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
