from typing import TypedDict, List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class Feedback(BaseModel):
    """Modèle pour le feedback utilisateur."""
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class AgentState(TypedDict):
    """État partagé et persistant du workflow."""
    messages: List[Dict[str, Any]]
    plan: Optional[str]
    next: str
    results: Dict[str, Any]
    session_id: str
    created_at: datetime
    updated_at: datetime
    task_description: str
    task_status: str
    code_context: Optional[str]
    working_memory: List[str]
    errors: List[str]
    logs: List[str]
    feedback: Optional[Dict[str, Any]] 