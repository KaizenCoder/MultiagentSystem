"""
Database Schemas Schemas - NextGeneration Refactored
Modles Pydantic Database Schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

class DatabaseSchemasRequest(BaseModel):
    """Requte Database Schemas"""
    # TODO: Dfinir champs requte
    pass

class DatabaseSchemasResponse(BaseModel):
    """Rponse Database Schemas"""
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
