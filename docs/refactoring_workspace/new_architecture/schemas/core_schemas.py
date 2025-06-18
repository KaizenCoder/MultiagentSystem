"""
Core Schemas Schemas - NextGeneration Refactored
Modles Pydantic Core Schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

class CoreSchemasRequest(BaseModel):
    """Requte Core Schemas"""
    # TODO: Dfinir champs requte
    pass

class CoreSchemasResponse(BaseModel):
    """Rponse Core Schemas"""
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
