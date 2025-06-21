# State Management Service  
from typing import List, Optional, Dict, Any
from ..models.schemas import StateItem

class StateService:
    """Service pour la gestion d'tat"""
    
    def __init__(self):
        """Initialise le service d'tat"""
        self.state_store: Dict[str, StateItem] = {}
    
    async def set_state(self, key: str, value: Any, session_id: Optional[str] = None) -> StateItem:
        """Dfinit une valeur d'tat"""
        state_key = f"{session_id}:{key}" if session_id else key
        state_item = StateItem(
            id=len(self.state_store) + 1,
            key=key,
            value=value,
            session_id=session_id
        )
        self.state_store[state_key] = state_item
        return state_item
    
    async def get_state(self, key: str, session_id: Optional[str] = None) -> Optional[StateItem]:
        """Rcupre une valeur d'tat"""
        state_key = f"{session_id}:{key}" if session_id else key
        return self.state_store.get(state_key)
    
    async def get_all_state(self, session_id: Optional[str] = None) -> List[StateItem]:
        """Rcupre tout l'tat"""
        if session_id:
            return [item for key, item in self.state_store.items() 
                   if item.session_id == session_id]
        return list(self.state_store.values())
    
    async def delete_state(self, key: str, session_id: Optional[str] = None) -> bool:
        """Supprime une valeur d'tat"""
        state_key = f"{session_id}:{key}" if session_id else key
        if state_key in self.state_store:
            del self.state_store[state_key]
            return True
        return False
    
    async def clear_state(self, session_id: Optional[str] = None) -> bool:
        """Efface l'tat"""
        if session_id:
            keys_to_remove = [key for key, item in self.state_store.items() 
                            if item.session_id == session_id]
            for key in keys_to_remove:
                del self.state_store[key]
        else:
            self.state_store.clear()
        return True 




