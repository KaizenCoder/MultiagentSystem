# RAG (Retrieval-Augmented Generation) Service
import chromadb
from typing import List, Optional, Dict, Any
from ..models.schemas import MemoryItem, SearchQuery, SearchResult

class RAGService:
    """Service pour la récupération et génération augmentée utilisant ChromaDB"""
    
    def __init__(self):
        """Initialise le service RAG avec ChromaDB"""
        # Configure un client ChromaDB persistant
        self.client = chromadb.PersistentClient(path="chroma_db")
        # Crée ou charge une collection
        self.collection = self.client.get_or_create_collection(name="memory_collection")
    
    async def store_memory(self, content: str, metadata: Optional[Dict[str, Any]] = None, 
                          session_id: Optional[str] = None) -> MemoryItem:
        """Stocke un élément en mémoire (ChromaDB)"""
        if metadata is None:
            metadata = {}
        
        # Ajoute le session_id aux métadonnées pour le filtrage
        if session_id:
            metadata["session_id"] = session_id

        # Génère un ID unique pour le document
        doc_id = str(self.collection.count() + 1)

        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        return MemoryItem(id=doc_id, content=content, metadata=metadata, session_id=session_id)
    
    async def search_memory(self, query: SearchQuery) -> SearchResult:
        """Recherche dans la mémoire (ChromaDB) en utilisant une recherche sémantique."""
        where_clause = {}
        if query.session_id:
            where_clause = {"session_id": query.session_id}

        results = self.collection.query(
            query_texts=[query.query],
            n_results=query.limit or 10,
            where=where_clause
        )
        
        # Formatte les résultats pour correspondre au schéma SearchResult
        items = []
        if results and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                content = results['documents'][0][i]
                metadata = results['metadatas'][0][i]
                session_id = metadata.get("session_id") if metadata else None
                items.append(MemoryItem(id=doc_id, content=content, metadata=metadata, session_id=session_id))

        return SearchResult(items=items, total_count=len(items))
    
    async def get_all_memories(self, session_id: Optional[str] = None) -> List[MemoryItem]:
        """Récupère toutes les mémoires depuis ChromaDB"""
        where_clause = {}
        if session_id:
            where_clause = {"session_id": session_id}
            
        all_items = self.collection.get(where=where_clause)
        
        items = []
        for i, doc_id in enumerate(all_items["ids"]):
            content = all_items['documents'][i]
            metadata = all_items['metadatas'][i]
            session_id = metadata.get("session_id") if metadata else None
            items.append(MemoryItem(id=doc_id, content=content, metadata=metadata, session_id=session_id))
        return items
    
    async def clear_memory(self, session_id: Optional[str] = None) -> bool:
        """Efface la mémoire dans ChromaDB"""
        if session_id:
            self.collection.delete(where={"session_id": session_id})
        else:
            # Efface et recrée la collection pour tout supprimer
            self.client.delete_collection(name="memory_collection")
            self.collection = self.client.get_or_create_collection(name="memory_collection")
        return True 