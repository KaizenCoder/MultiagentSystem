# Data Models and Schemas
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class MemoryItem(BaseModel):
    """Modle pour un lment de mmoire"""
    id: Optional[int] = None
    content: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    session_id: Optional[str] = None

class StateItem(BaseModel):
    """Modle pour un lment d'tat"""
    id: Optional[int] = None
    key: str
    value: Any
    session_id: Optional[str] = None
    timestamp: Optional[datetime] = None

class SearchQuery(BaseModel):
    """Modle pour les requtes de recherche"""
    query: str
    limit: Optional[int] = 10
    session_id: Optional[str] = None

class SearchResult(BaseModel):
    """Modle pour les rsultats de recherche"""
    items: List[MemoryItem]
    total_count: int 