# Memory API Main Application
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from .models.schemas import MemoryItem, StateItem, SearchQuery, SearchResult
from .services.rag_service import RAGService
from .services.state_service import StateService

app = FastAPI(
    title="Memory API",
    description="API pour la gestion de mémoire et d'état dans l'environnement multi-agent",
    version="1.0.0"
)

# Services
rag_service = RAGService()
state_service = StateService()

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {"message": "Memory API - Environnement Multi-Agent"}

@app.get("/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {"status": "healthy", "service": "memory_api"}

# Endpoints pour la mémoire
@app.post("/memory/store", response_model=MemoryItem)
async def store_memory(content: str, metadata: dict = None, session_id: str = None):
    """Stocke un élément en mémoire"""
    return await rag_service.store_memory(content, metadata, session_id)

@app.post("/memory/search", response_model=SearchResult)
async def search_memory(query: SearchQuery):
    """Recherche dans la mémoire"""
    return await rag_service.search_memory(query)

@app.get("/memory/all", response_model=List[MemoryItem])
async def get_all_memories(session_id: str = None):
    """Récupère toutes les mémoires"""
    return await rag_service.get_all_memories(session_id)

@app.delete("/memory/clear")
async def clear_memory(session_id: str = None):
    """Efface la mémoire"""
    success = await rag_service.clear_memory(session_id)
    if success:
        return {"message": "Mémoire effacée avec succès"}
    raise HTTPException(status_code=500, detail="Erreur lors de l'effacement de la mémoire")

# Endpoints pour l'état
@app.post("/state/set", response_model=StateItem)
async def set_state(key: str, value: str, session_id: str = None):
    """Définit une valeur d'état"""
    return await state_service.set_state(key, value, session_id)

@app.get("/state/get")
async def get_state(key: str, session_id: str = None):
    """Récupère une valeur d'état"""
    state_item = await state_service.get_state(key, session_id)
    if state_item:
        return state_item
    raise HTTPException(status_code=404, detail="État non trouvé")

@app.get("/state/all", response_model=List[StateItem])
async def get_all_state(session_id: str = None):
    """Récupère tout l'état"""
    return await state_service.get_all_state(session_id)

@app.delete("/state/delete")
async def delete_state(key: str, session_id: str = None):
    """Supprime une valeur d'état"""
    success = await state_service.delete_state(key, session_id)
    if success:
        return {"message": "État supprimé avec succès"}
    raise HTTPException(status_code=404, detail="État non trouvé")

@app.delete("/state/clear")
async def clear_state(session_id: str = None):
    """Efface l'état"""
    success = await state_service.clear_state(session_id)
    if success:
        return {"message": "État effacé avec succès"}
    raise HTTPException(status_code=500, detail="Erreur lors de l'effacement de l'état")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 