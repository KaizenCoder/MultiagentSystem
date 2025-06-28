#!/usr/bin/env python3
"""
ContextStore Optimisé - Phase 0 Semaine 2
Système de mémoire tri-tiers pour agents avec sauvegarde différentielle

Objectifs:
- Mémoire tri-tiers: Redis (working) + PostgreSQL (long-term) + ChromaDB (semantic)
- Sauvegarde différentielle pour performance optimisée
- Context injection automatique pour agents legacy et modernes
- Gestion sessions vocales avec contexte conversationnel
- Métriques et monitoring intégrés
"""

import asyncio
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
import logging
from abc import ABC, abstractmethod

# Imports pour backends
try:
    import redis.asyncio as redis
    import asyncpg
    import chromadb
    from chromadb.config import Settings
except ImportError as e:
    print(f"⚠️  Missing dependencies: {e}")
    print("Install with: pip install redis asyncpg chromadb")

class ContextType(Enum):
    """Types de contexte"""
    WORKING_MEMORY = "working_memory"      # Cache Redis
    LONG_TERM_MEMORY = "long_term_memory"  # PostgreSQL
    SEMANTIC_MEMORY = "semantic_memory"    # ChromaDB
    VOICE_SESSION = "voice_session"        # Contexte vocal
    AGENT_STATE = "agent_state"           # État agent
    CONVERSATION = "conversation"          # Historique conversation

@dataclass
class AgentContext:
    """Contexte complet d'un agent"""
    agent_id: str
    context_type: ContextType
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    session_id: Optional[str] = None
    ttl_seconds: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.session_id:
            self.session_id = f"{self.agent_id}_{int(time.time())}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Sérialise le contexte"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['context_type'] = self.context_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentContext':
        """Désérialise depuis un dictionnaire"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        data['context_type'] = ContextType(data['context_type'])
        return cls(**data)

@dataclass
class ContextDiff:
    """Différences entre deux contextes pour sauvegarde optimisée"""
    agent_id: str
    previous_hash: str
    current_hash: str
    added_keys: Set[str]
    modified_keys: Set[str]
    removed_keys: Set[str]
    changes: Dict[str, Any]
    has_changes: bool = False
    
    def __post_init__(self):
        self.has_changes = bool(self.added_keys or self.modified_keys or self.removed_keys)

@dataclass
class ContextStoreConfig:
    """Configuration du ContextStore"""
    redis_url: str = "redis://localhost:6379"
    postgresql_url: str = "postgresql://localhost:5432/nextgeneration"
    chromadb_path: str = "./chroma_db"
    working_memory_ttl: int = 3600  # 1 heure
    voice_session_ttl: int = 1800   # 30 minutes
    enable_differential_save: bool = True
    max_context_size_kb: int = 1024  # 1MB max
    compression_enabled: bool = True

class ContextBackend(ABC):
    """Interface abstraite pour backends de contexte"""
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialise le backend"""
        pass
    
    @abstractmethod
    async def save_context(self, context: AgentContext) -> bool:
        """Sauvegarde un contexte"""
        pass
    
    @abstractmethod
    async def load_context(self, agent_id: str, context_type: ContextType) -> Optional[AgentContext]:
        """Charge un contexte"""
        pass
    
    @abstractmethod
    async def delete_context(self, agent_id: str, context_type: ContextType) -> bool:
        """Supprime un contexte"""
        pass
    
    @abstractmethod
    async def cleanup(self):
        """Nettoie les ressources"""
        pass

class RedisContextCache(ContextBackend):
    """Backend Redis pour working memory"""
    
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis_client = None
        self.logger = logging.getLogger("RedisContextCache")
    
    async def initialize(self) -> bool:
        """Initialise Redis"""
        try:
            self.redis_client = redis.from_url(self.redis_url)
            await self.redis_client.ping()
            self.logger.info("✅ Redis context cache initialized")
            return True
        except Exception as e:
            self.logger.error(f"❌ Redis cache initialization failed: {e}")
            return False
    
    async def save_context(self, context: AgentContext) -> bool:
        """Sauvegarde en cache Redis"""
        try:
            key = f"context:{context.agent_id}:{context.context_type.value}"
            data = json.dumps(context.to_dict())
            
            if context.ttl_seconds:
                await self.redis_client.setex(key, context.ttl_seconds, data)
            else:
                await self.redis_client.set(key, data)
            
            return True
        except Exception as e:
            self.logger.error(f"Redis save error: {e}")
            return False
    
    async def load_context(self, agent_id: str, context_type: ContextType) -> Optional[AgentContext]:
        """Charge depuis cache Redis"""
        try:
            key = f"context:{agent_id}:{context_type.value}"
            data = await self.redis_client.get(key)
            
            if data:
                context_dict = json.loads(data)
                return AgentContext.from_dict(context_dict)
            
            return None
        except Exception as e:
            self.logger.error(f"Redis load error: {e}")
            return None
    
    async def delete_context(self, agent_id: str, context_type: ContextType) -> bool:
        """Supprime du cache Redis"""
        try:
            key = f"context:{agent_id}:{context_type.value}"
            result = await self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            self.logger.error(f"Redis delete error: {e}")
            return False
    
    async def update_working_memory_delta(self, agent_id: str, diff: ContextDiff) -> bool:
        """Met à jour seulement les changements"""
        try:
            key = f"context:{agent_id}:working_memory"
            
            # Charger le contexte actuel
            current_data = await self.redis_client.get(key)
            if not current_data:
                return False
            
            context_dict = json.loads(current_data)
            
            # Appliquer les changements
            for change_key, change_value in diff.changes.items():
                if change_key in diff.removed_keys:
                    context_dict['data'].pop(change_key, None)
                else:
                    context_dict['data'][change_key] = change_value
            
            # Sauvegarder
            await self.redis_client.set(key, json.dumps(context_dict))
            return True
            
        except Exception as e:
            self.logger.error(f"Redis delta update error: {e}")
            return False
    
    async def cleanup(self):
        """Ferme Redis"""
        if self.redis_client:
            await self.redis_client.close()

class PostgreSQLContextStore(ContextBackend):
    """Backend PostgreSQL pour long-term memory"""
    
    def __init__(self, postgresql_url: str):
        self.postgresql_url = postgresql_url
        self.pool = None
        self.logger = logging.getLogger("PostgreSQLContextStore")
    
    async def initialize(self) -> bool:
        """Initialise PostgreSQL"""
        try:
            self.pool = await asyncpg.create_pool(self.postgresql_url)
            
            # Créer les tables si nécessaire
            await self._create_tables()
            
            self.logger.info("✅ PostgreSQL context store initialized")
            return True
        except Exception as e:
            self.logger.error(f"❌ PostgreSQL initialization failed: {e}")
            return False
    
    async def _create_tables(self):
        """Crée les tables de contexte"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_contexts (
                    id SERIAL PRIMARY KEY,
                    agent_id VARCHAR(255) NOT NULL,
                    context_type VARCHAR(50) NOT NULL,
                    session_id VARCHAR(255),
                    data JSONB NOT NULL,
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    ttl_expires_at TIMESTAMP,
                    UNIQUE(agent_id, context_type, session_id)
                );
                
                CREATE INDEX IF NOT EXISTS idx_agent_contexts_agent_id 
                ON agent_contexts(agent_id);
                
                CREATE INDEX IF NOT EXISTS idx_agent_contexts_type 
                ON agent_contexts(context_type);
                
                CREATE INDEX IF NOT EXISTS idx_agent_contexts_session 
                ON agent_contexts(session_id);
                
                CREATE TABLE IF NOT EXISTS context_diffs (
                    id SERIAL PRIMARY KEY,
                    agent_id VARCHAR(255) NOT NULL,
                    previous_hash VARCHAR(64),
                    current_hash VARCHAR(64),
                    changes JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
    
    async def save_context(self, context: AgentContext) -> bool:
        """Sauvegarde en PostgreSQL"""
        try:
            async with self.pool.acquire() as conn:
                ttl_expires = None
                if context.ttl_seconds:
                    ttl_expires = context.timestamp + timedelta(seconds=context.ttl_seconds)
                
                await conn.execute("""
                    INSERT INTO agent_contexts 
                    (agent_id, context_type, session_id, data, metadata, ttl_expires_at)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    ON CONFLICT (agent_id, context_type, session_id)
                    DO UPDATE SET 
                        data = EXCLUDED.data,
                        metadata = EXCLUDED.metadata,
                        updated_at = NOW(),
                        ttl_expires_at = EXCLUDED.ttl_expires_at
                """, 
                context.agent_id,
                context.context_type.value,
                context.session_id,
                json.dumps(context.data),
                json.dumps(context.metadata),
                ttl_expires
                )
            
            return True
        except Exception as e:
            self.logger.error(f"PostgreSQL save error: {e}")
            return False
    
    async def load_context(self, agent_id: str, context_type: ContextType) -> Optional[AgentContext]:
        """Charge depuis PostgreSQL"""
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT agent_id, context_type, session_id, data, metadata, updated_at
                    FROM agent_contexts 
                    WHERE agent_id = $1 AND context_type = $2
                    AND (ttl_expires_at IS NULL OR ttl_expires_at > NOW())
                    ORDER BY updated_at DESC
                    LIMIT 1
                """, agent_id, context_type.value)
                
                if row:
                    return AgentContext(
                        agent_id=row['agent_id'],
                        context_type=ContextType(row['context_type']),
                        session_id=row['session_id'],
                        data=row['data'],
                        metadata=row['metadata'] or {},
                        timestamp=row['updated_at']
                    )
            
            return None
        except Exception as e:
            self.logger.error(f"PostgreSQL load error: {e}")
            return None
    
    async def save_context_diff(self, agent_id: str, diff: ContextDiff) -> bool:
        """Sauvegarde un diff de contexte"""
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO context_diffs 
                    (agent_id, previous_hash, current_hash, changes)
                    VALUES ($1, $2, $3, $4)
                """, 
                agent_id,
                diff.previous_hash,
                diff.current_hash,
                json.dumps({
                    'added': list(diff.added_keys),
                    'modified': list(diff.modified_keys),
                    'removed': list(diff.removed_keys),
                    'changes': diff.changes
                })
                )
            
            return True
        except Exception as e:
            self.logger.error(f"PostgreSQL diff save error: {e}")
            return False
    
    async def delete_context(self, agent_id: str, context_type: ContextType) -> bool:
        """Supprime de PostgreSQL"""
        try:
            async with self.pool.acquire() as conn:
                result = await conn.execute("""
                    DELETE FROM agent_contexts 
                    WHERE agent_id = $1 AND context_type = $2
                """, agent_id, context_type.value)
                
                return "DELETE" in result
        except Exception as e:
            self.logger.error(f"PostgreSQL delete error: {e}")
            return False
    
    async def cleanup(self):
        """Ferme PostgreSQL"""
        if self.pool:
            await self.pool.close()

class ChromaSemanticStore(ContextBackend):
    """Backend ChromaDB pour semantic memory"""
    
    def __init__(self, chroma_path: str):
        self.chroma_path = chroma_path
        self.client = None
        self.collection = None
        self.logger = logging.getLogger("ChromaSemanticStore")
    
    async def initialize(self) -> bool:
        """Initialise ChromaDB"""
        try:
            # ChromaDB est synchrone, on l'initialise directement
            self.client = chromadb.PersistentClient(
                path=self.chroma_path,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Créer ou récupérer la collection
            self.collection = self.client.get_or_create_collection(
                name="agent_contexts",
                metadata={"description": "Agent semantic contexts"}
            )
            
            self.logger.info("✅ ChromaDB semantic store initialized")
            return True
        except Exception as e:
            self.logger.error(f"❌ ChromaDB initialization failed: {e}")
            return False
    
    async def save_context(self, context: AgentContext) -> bool:
        """Sauvegarde en ChromaDB"""
        try:
            # Exécuter en thread pool car ChromaDB est synchrone
            await asyncio.get_event_loop().run_in_executor(
                None, self._save_context_sync, context
            )
            return True
        except Exception as e:
            self.logger.error(f"ChromaDB save error: {e}")
            return False
    
    def _save_context_sync(self, context: AgentContext):
        """Sauvegarde synchrone ChromaDB"""
        doc_id = f"{context.agent_id}_{context.context_type.value}_{context.session_id}"
        
        # Convertir le contexte en texte pour embedding
        context_text = self._context_to_text(context)
        
        self.collection.upsert(
            ids=[doc_id],
            documents=[context_text],
            metadatas=[{
                "agent_id": context.agent_id,
                "context_type": context.context_type.value,
                "session_id": context.session_id,
                "timestamp": context.timestamp.isoformat()
            }]
        )
    
    async def load_context(self, agent_id: str, context_type: ContextType) -> Optional[AgentContext]:
        """Charge depuis ChromaDB"""
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                None, self._load_context_sync, agent_id, context_type
            )
            return result
        except Exception as e:
            self.logger.error(f"ChromaDB load error: {e}")
            return None
    
    def _load_context_sync(self, agent_id: str, context_type: ContextType) -> Optional[AgentContext]:
        """Charge synchrone ChromaDB"""
        results = self.collection.get(
            where={
                "agent_id": agent_id,
                "context_type": context_type.value
            },
            limit=1
        )
        
        if results['documents']:
            metadata = results['metadatas'][0]
            # Reconstruire le contexte depuis le texte (simplification)
            return AgentContext(
                agent_id=metadata['agent_id'],
                context_type=ContextType(metadata['context_type']),
                session_id=metadata['session_id'],
                data={"semantic_content": results['documents'][0]},
                timestamp=datetime.fromisoformat(metadata['timestamp'])
            )
        
        return None
    
    async def search_similar_contexts(self, query: str, agent_id: str = None, limit: int = 5) -> List[AgentContext]:
        """Recherche de contextes similaires par embedding"""
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                None, self._search_similar_sync, query, agent_id, limit
            )
            return result
        except Exception as e:
            self.logger.error(f"ChromaDB search error: {e}")
            return []
    
    def _search_similar_sync(self, query: str, agent_id: str = None, limit: int = 5) -> List[AgentContext]:
        """Recherche synchrone ChromaDB"""
        where_clause = {}
        if agent_id:
            where_clause["agent_id"] = agent_id
        
        results = self.collection.query(
            query_texts=[query],
            where=where_clause if where_clause else None,
            n_results=limit
        )
        
        contexts = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                contexts.append(AgentContext(
                    agent_id=metadata['agent_id'],
                    context_type=ContextType(metadata['context_type']),
                    session_id=metadata['session_id'],
                    data={"semantic_content": doc, "similarity_score": results['distances'][0][i]},
                    timestamp=datetime.fromisoformat(metadata['timestamp'])
                ))
        
        return contexts
    
    def _context_to_text(self, context: AgentContext) -> str:
        """Convertit un contexte en texte pour embedding"""
        lines = [
            f"Agent: {context.agent_id}",
            f"Type: {context.context_type.value}",
            f"Session: {context.session_id}",
            f"Timestamp: {context.timestamp.isoformat()}",
            "",
            "Data:"
        ]
        
        # Convertir les données en texte lisible
        for key, value in context.data.items():
            if isinstance(value, (str, int, float)):
                lines.append(f"- {key}: {value}")
            elif isinstance(value, (list, dict)):
                lines.append(f"- {key}: {json.dumps(value, indent=2)}")
        
        return "\n".join(lines)
    
    async def delete_context(self, agent_id: str, context_type: ContextType) -> bool:
        """Supprime de ChromaDB"""
        try:
            await asyncio.get_event_loop().run_in_executor(
                None, self._delete_context_sync, agent_id, context_type
            )
            return True
        except Exception as e:
            self.logger.error(f"ChromaDB delete error: {e}")
            return False
    
    def _delete_context_sync(self, agent_id: str, context_type: ContextType):
        """Suppression synchrone ChromaDB"""
        results = self.collection.get(
            where={
                "agent_id": agent_id,
                "context_type": context_type.value
            }
        )
        
        if results['ids']:
            self.collection.delete(ids=results['ids'])
    
    async def cleanup(self):
        """ChromaDB cleanup"""
        # ChromaDB se ferme automatiquement
        pass

class OptimizedContextStore:
    """
    ContextStore optimisé avec sauvegarde différentielle
    """
    
    def __init__(self, config: ContextStoreConfig):
        self.config = config
        
        # Backends tri-tiers
        self.redis_cache = RedisContextCache(config.redis_url)
        self.postgresql_store = PostgreSQLContextStore(config.postgresql_url)
        self.chroma_semantic = ChromaSemanticStore(config.chromadb_path)
        
        # Cache des hash pour diff
        self.context_hashes: Dict[str, str] = {}
        
        # Métriques
        self.metrics = {
            "contexts_saved": 0,
            "contexts_loaded": 0,
            "differential_saves": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "semantic_searches": 0
        }
        
        self.logger = logging.getLogger("OptimizedContextStore")
    
    async def initialize(self) -> bool:
        """Initialise tous les backends"""
        
        results = []
        
        # Initialiser Redis
        redis_ok = await self.redis_cache.initialize()
        results.append(("Redis", redis_ok))
        
        # Initialiser PostgreSQL
        postgres_ok = await self.postgresql_store.initialize()
        results.append(("PostgreSQL", postgres_ok))
        
        # Initialiser ChromaDB
        chroma_ok = await self.chroma_semantic.initialize()
        results.append(("ChromaDB", chroma_ok))
        
        # Log des résultats
        for backend, status in results:
            status_str = "✅" if status else "❌"
            self.logger.info(f"{status_str} {backend} context store")
        
        # Au moins Redis ou PostgreSQL doit marcher
        min_required = redis_ok or postgres_ok
        
        if min_required:
            self.logger.info("🚀 ContextStore initialized successfully")
        else:
            self.logger.error("❌ ContextStore initialization failed")
        
        return min_required
    
    async def save_agent_context(self, context: AgentContext) -> bool:
        """Sauvegarde un contexte avec optimisation différentielle"""
        
        try:
            self.metrics["contexts_saved"] += 1
            
            # Calculer le hash du contexte
            current_hash = self._compute_context_hash(context)
            context_key = f"{context.agent_id}:{context.context_type.value}"
            
            # Vérifier si différentiel activé
            if self.config.enable_differential_save and context_key in self.context_hashes:
                previous_hash = self.context_hashes[context_key]
                
                if current_hash == previous_hash:
                    # Aucun changement, pas de sauvegarde
                    return True
                
                # Calculer le diff
                diff = await self._compute_context_diff(context, previous_hash)
                
                if diff.has_changes:
                    self.metrics["differential_saves"] += 1
                    
                    # Sauvegarde différentielle
                    await self._save_differential(context, diff)
                else:
                    return True
            else:
                # Sauvegarde complète
                await self._save_complete(context)
            
            # Mettre à jour le hash
            self.context_hashes[context_key] = current_hash
            
            return True
            
        except Exception as e:
            self.logger.error(f"Context save error: {e}")
            return False
    
    async def _save_complete(self, context: AgentContext):
        """Sauvegarde complète sur tous les backends"""
        
        # Sauvegarde selon le type de contexte
        if context.context_type == ContextType.WORKING_MEMORY:
            context.ttl_seconds = self.config.working_memory_ttl
            await self.redis_cache.save_context(context)
        
        if context.context_type in [ContextType.VOICE_SESSION]:
            context.ttl_seconds = self.config.voice_session_ttl
            await self.redis_cache.save_context(context)
        
        if context.context_type in [ContextType.LONG_TERM_MEMORY, ContextType.AGENT_STATE]:
            await self.postgresql_store.save_context(context)
        
        if context.context_type == ContextType.SEMANTIC_MEMORY:
            await self.chroma_semantic.save_context(context)
    
    async def _save_differential(self, context: AgentContext, diff: ContextDiff):
        """Sauvegarde différentielle optimisée"""
        
        # Sauvegarder le diff en PostgreSQL
        await self.postgresql_store.save_context_diff(context.agent_id, diff)
        
        # Mettre à jour Redis avec delta si working memory
        if context.context_type == ContextType.WORKING_MEMORY:
            await self.redis_cache.update_working_memory_delta(context.agent_id, diff)
        else:
            # Sauvegarde complète pour autres types
            await self._save_complete(context)
    
    async def load_agent_context(self, agent_id: str, context_type: ContextType) -> Optional[AgentContext]:
        """Charge un contexte avec cache intelligent"""
        
        try:
            self.metrics["contexts_loaded"] += 1
            
            # Essayer cache Redis en premier
            if context_type in [ContextType.WORKING_MEMORY, ContextType.VOICE_SESSION]:
                context = await self.redis_cache.load_context(agent_id, context_type)
                if context:
                    self.metrics["cache_hits"] += 1
                    return context
            
            # Essayer PostgreSQL pour long-term
            if context_type in [ContextType.LONG_TERM_MEMORY, ContextType.AGENT_STATE]:
                context = await self.postgresql_store.load_context(agent_id, context_type)
                if context:
                    self.metrics["cache_misses"] += 1
                    return context
            
            # Essayer ChromaDB pour semantic
            if context_type == ContextType.SEMANTIC_MEMORY:
                context = await self.chroma_semantic.load_context(agent_id, context_type)
                if context:
                    self.metrics["cache_misses"] += 1
                    return context
            
            return None
            
        except Exception as e:
            self.logger.error(f"Context load error: {e}")
            return None
    
    async def get_agent_context_complete(self, agent_id: str) -> Dict[str, Any]:
        """Récupère le contexte complet d'un agent (tri-tiers)"""
        
        context_complete = {
            "agent_id": agent_id,
            "working_memory": None,
            "long_term_memory": None,
            "semantic_memory": None,
            "voice_session": None
        }
        
        # Charger chaque type de contexte
        for context_type in [ContextType.WORKING_MEMORY, ContextType.LONG_TERM_MEMORY, 
                           ContextType.SEMANTIC_MEMORY, ContextType.VOICE_SESSION]:
            context = await self.load_agent_context(agent_id, context_type)
            if context:
                key = context_type.value
                context_complete[key] = context.data
        
        return context_complete
    
    async def search_semantic_contexts(self, query: str, agent_id: str = None, limit: int = 5) -> List[AgentContext]:
        """Recherche de contextes par similarité sémantique"""
        
        self.metrics["semantic_searches"] += 1
        return await self.chroma_semantic.search_similar_contexts(query, agent_id, limit)
    
    def _compute_context_hash(self, context: AgentContext) -> str:
        """Calcule le hash d'un contexte pour détecter les changements"""
        
        # Sérialiser seulement les données (pas timestamp)
        data_str = json.dumps(context.data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    async def _compute_context_diff(self, current_context: AgentContext, previous_hash: str) -> ContextDiff:
        """Calcule la différence entre contextes"""
        
        # Charger le contexte précédent pour comparaison
        previous_context = await self.load_agent_context(
            current_context.agent_id, 
            current_context.context_type
        )
        
        if not previous_context:
            # Pas de contexte précédent, tout est nouveau
            return ContextDiff(
                agent_id=current_context.agent_id,
                previous_hash=previous_hash,
                current_hash=self._compute_context_hash(current_context),
                added_keys=set(current_context.data.keys()),
                modified_keys=set(),
                removed_keys=set(),
                changes=current_context.data,
                has_changes=True
            )
        
        # Comparer les contextes
        current_keys = set(current_context.data.keys())
        previous_keys = set(previous_context.data.keys())
        
        added_keys = current_keys - previous_keys
        removed_keys = previous_keys - current_keys
        common_keys = current_keys & previous_keys
        
        modified_keys = set()
        changes = {}
        
        # Vérifier les clés modifiées
        for key in common_keys:
            if current_context.data[key] != previous_context.data[key]:
                modified_keys.add(key)
                changes[key] = current_context.data[key]
        
        # Ajouter les nouvelles clés
        for key in added_keys:
            changes[key] = current_context.data[key]
        
        return ContextDiff(
            agent_id=current_context.agent_id,
            previous_hash=previous_hash,
            current_hash=self._compute_context_hash(current_context),
            added_keys=added_keys,
            modified_keys=modified_keys,
            removed_keys=removed_keys,
            changes=changes
        )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques du ContextStore"""
        
        cache_hit_rate = 0.0
        total_loads = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        if total_loads > 0:
            cache_hit_rate = self.metrics["cache_hits"] / total_loads
        
        return {
            **self.metrics,
            "cache_hit_rate": cache_hit_rate,
            "differential_save_rate": self.metrics["differential_saves"] / max(self.metrics["contexts_saved"], 1)
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Vérification de santé du ContextStore"""
        
        health = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "backends": {}
        }
        
        # Test Redis
        try:
            test_context = AgentContext(
                agent_id="health_check",
                context_type=ContextType.WORKING_MEMORY,
                data={"test": True}
            )
            success = await self.redis_cache.save_context(test_context)
            health["backends"]["redis"] = "healthy" if success else "unhealthy"
        except:
            health["backends"]["redis"] = "unhealthy"
            health["status"] = "degraded"
        
        # Test PostgreSQL
        try:
            test_context = AgentContext(
                agent_id="health_check",
                context_type=ContextType.LONG_TERM_MEMORY,
                data={"test": True}
            )
            success = await self.postgresql_store.save_context(test_context)
            health["backends"]["postgresql"] = "healthy" if success else "unhealthy"
        except:
            health["backends"]["postgresql"] = "unhealthy"
            health["status"] = "degraded"
        
        # Test ChromaDB
        try:
            test_context = AgentContext(
                agent_id="health_check",
                context_type=ContextType.SEMANTIC_MEMORY,
                data={"test": "semantic content"}
            )
            success = await self.chroma_semantic.save_context(test_context)
            health["backends"]["chromadb"] = "healthy" if success else "unhealthy"
        except:
            health["backends"]["chromadb"] = "unhealthy"
        
        return health
    
    async def cleanup(self):
        """Nettoie toutes les ressources"""
        await self.redis_cache.cleanup()
        await self.postgresql_store.cleanup()
        await self.chroma_semantic.cleanup()

# Factory functions

async def create_context_store(config: ContextStoreConfig = None) -> OptimizedContextStore:
    """Crée et initialise un ContextStore"""
    
    if config is None:
        config = ContextStoreConfig()
    
    store = OptimizedContextStore(config)
    await store.initialize()
    return store

def create_agent_context(
    agent_id: str,
    context_type: ContextType,
    data: Dict[str, Any],
    session_id: str = None,
    ttl_seconds: int = None
) -> AgentContext:
    """Crée un contexte d'agent"""
    
    return AgentContext(
        agent_id=agent_id,
        context_type=context_type,
        data=data,
        session_id=session_id,
        ttl_seconds=ttl_seconds
    )

# Démonstration et tests

async def demo_context_store():
    """Démonstration du ContextStore optimisé"""
    
    print("🚀 ContextStore Optimized Demo - Phase 0 Week 2")
    print("=" * 60)
    
    # Configuration
    config = ContextStoreConfig(
        enable_differential_save=True,
        working_memory_ttl=300,  # 5 minutes pour demo
        voice_session_ttl=180    # 3 minutes pour demo
    )
    
    try:
        # Création du context store
        store = await create_context_store(config)
        
        # Test 1: Contexte working memory
        print("\n🧪 Test 1: Working Memory Context")
        working_context = create_agent_context(
            agent_id="agent_111_auditeur_qualite",
            context_type=ContextType.WORKING_MEMORY,
            data={
                "current_task": "code_review",
                "files_analyzed": ["main.py", "utils.py"],
                "issues_found": 3,
                "status": "in_progress"
            }
        )
        
        success = await store.save_agent_context(working_context)
        print(f"Working memory save: {success}")
        
        loaded = await store.load_agent_context("agent_111_auditeur_qualite", ContextType.WORKING_MEMORY)
        print(f"Working memory load: {loaded is not None}")
        
        # Test 2: Modification et diff
        print("\n🧪 Test 2: Differential Save")
        working_context.data["issues_found"] = 5  # Modification
        working_context.data["new_field"] = "added"  # Ajout
        
        success = await store.save_agent_context(working_context)
        print(f"Differential save: {success}")
        
        # Test 3: Contexte vocal
        print("\n🧪 Test 3: Voice Session Context")
        voice_context = create_agent_context(
            agent_id="voice_interface",
            context_type=ContextType.VOICE_SESSION,
            data={
                "voice_session_id": "session_123",
                "stt_confidence": 0.95,
                "last_command": "status report",
                "conversation_history": [
                    {"user": "status report", "agent": "Current progress: 75%"}
                ]
            }
        )
        
        success = await store.save_agent_context(voice_context)
        print(f"Voice session save: {success}")
        
        # Test 4: Contexte long-term
        print("\n🧪 Test 4: Long-term Memory")
        longterm_context = create_agent_context(
            agent_id="agent_111_auditeur_qualite",
            context_type=ContextType.LONG_TERM_MEMORY,
            data={
                "agent_role": "Code quality auditor",
                "expertise_areas": ["Python", "JavaScript", "Security"],
                "performance_metrics": {
                    "issues_detected": 245,
                    "false_positives": 12,
                    "accuracy_rate": 0.95
                },
                "learning_history": [
                    {"date": "2025-06-15", "topic": "async/await patterns"},
                    {"date": "2025-06-20", "topic": "security vulnerabilities"}
                ]
            }
        )
        
        success = await store.save_agent_context(longterm_context)
        print(f"Long-term memory save: {success}")
        
        # Test 5: Contexte sémantique et recherche
        print("\n🧪 Test 5: Semantic Memory & Search")
        semantic_context = create_agent_context(
            agent_id="agent_111_auditeur_qualite",
            context_type=ContextType.SEMANTIC_MEMORY,
            data={
                "knowledge_base": "Code review best practices include checking for security vulnerabilities, performance issues, maintainability concerns, and adherence to coding standards. Common patterns to look for include SQL injection, XSS vulnerabilities, memory leaks, and code duplication.",
                "context": "audit_expertise"
            }
        )
        
        success = await store.save_agent_context(semantic_context)
        print(f"Semantic memory save: {success}")
        
        # Recherche sémantique
        similar_contexts = await store.search_semantic_contexts(
            "security vulnerabilities in code",
            agent_id="agent_111_auditeur_qualite"
        )
        print(f"Semantic search results: {len(similar_contexts)}")
        
        # Test 6: Contexte complet
        print("\n🧪 Test 6: Complete Agent Context")
        complete_context = await store.get_agent_context_complete("agent_111_auditeur_qualite")
        print(f"Complete context loaded: {len([k for k, v in complete_context.items() if v is not None])}/4 types")
        
        # Métriques
        print("\n📊 Métriques ContextStore")
        metrics = store.get_metrics()
        print(f"Contexts saved: {metrics['contexts_saved']}")
        print(f"Contexts loaded: {metrics['contexts_loaded']}")
        print(f"Differential saves: {metrics['differential_saves']}")
        print(f"Cache hit rate: {metrics['cache_hit_rate']:.2%}")
        print(f"Differential save rate: {metrics['differential_save_rate']:.2%}")
        
        # Health check
        print("\n🏥 Health Check")
        health = await store.health_check()
        print(f"Status: {health['status']}")
        print(f"Backends: {health['backends']}")
        
        await store.cleanup()
        print("\n✅ Demo completed successfully")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(demo_context_store())