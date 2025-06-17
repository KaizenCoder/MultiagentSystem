# Data Models and Schemas
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class MemoryItem(BaseModel):
    """Modèle pour un élément de mémoire"""
    id: Optional[int] = None
    content: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    session_id: Optional[str] = None

class StateItem(BaseModel):
    """Modèle pour un élément d'état"""
    id: Optional[int] = None
    key: str
    value: Any
    session_id: Optional[str] = None
    timestamp: Optional[datetime] = None

class SearchQuery(BaseModel):
    """Modèle pour les requêtes de recherche"""
    query: str
    limit: Optional[int] = 10
    session_id: Optional[str] = None

class SearchResult(BaseModel):
    """Modèle pour les résultats de recherche"""
    items: List[MemoryItem]
    total_count: int 