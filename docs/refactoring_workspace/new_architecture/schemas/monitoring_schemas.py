"""
Monitoring Schemas Schemas - NextGeneration Refactored
Modles Pydantic Monitoring Schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

class MonitoringSchemasRequest(BaseModel):
    """Requte Monitoring Schemas"""
    # TODO: Dfinir champs requte
    pass

class MonitoringSchemasResponse(BaseModel):
    """Rponse Monitoring Schemas"""
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
