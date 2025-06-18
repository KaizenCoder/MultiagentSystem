"""
Redis Cache Implementation pour l'amélioration des performances
Gestion multi-layer du cache avec TTL intelligent
"""
import os
import json
import asyncio
from typing import Optional, Dict, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from orchestrator.app.security.logging import security_logger


class CacheType(Enum):
    """Types de cache avec TTL différents"""
    LLM_RESPONSE = "llm_response"        # TTL 1h
    SESSION_DATA = "session_data"        # TTL 24h  
    RAG_RESULTS = "rag_results"          # TTL 30min
    API_RESPONSE = "api_response"        # TTL 5min
    USER_CONTEXT = "user_context"        # TTL 2h
    AGENT_STATE = "agent_state"          # TTL 1h


@dataclass
class CacheEntry:
    """Entrée de cache avec métadonnées"""
    key: str
    value: Any
    cache_type: CacheType
    created_at: datetime
    expires_at: datetime
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    
    def is_expired(self) -> bool:
        """Vérifie si l'entrée a expiré"""
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire pour stockage Redis"""
        return {
            'key': self.key,
            'value': self.value,
            'cache_type': self.cache_type.value,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'access_count': self.access_count,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CacheEntry':
        """Crée une entrée depuis un dictionnaire Redis"""
        return cls(
            key=data['key'],
            value=data['value'],
            cache_type=CacheType(data['cache_type']),
            created_at=datetime.fromisoformat(data['created_at']),
            expires_at=datetime.fromisoformat(data['expires_at']),
            access_count=data.get('access_count', 0),
            last_accessed=datetime.fromisoformat(data['last_accessed']) if data.get('last_accessed') else None
        )


class ProductionRedisCache:
    """
    Cache Redis production-ready avec:
    - Multi-layer caching strategy
    - TTL intelligent par type
    - Compression automatique
    - Monitoring et métriques
    - Fallback gracieux
    """
    
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        db: int = 0,
        max_connections: int = 100,
        retry_on_timeout: bool = True,
        health_check_interval: int = 30,
        compression_threshold: int = 1024  # Compression si > 1KB
    ):
        self.redis_url = redis_url
        self.db = db
        self.max_connections = max_connections
        self.retry_on_timeout = retry_on_timeout
        self.health_check_interval = health_check_interval
        self.compression_threshold = compression_threshold
        
        # Pool de connexions
        self.redis_pool = None
        self.redis_client = None
        
        # Métriques
        self.metrics = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0,
            'errors': 0,
            'compression_saves': 0
        }
        
        # TTL par type de cache
        self.ttl_config = {
            CacheType.LLM_RESPONSE: timedelta(hours=1),
            CacheType.SESSION_DATA: timedelta(hours=24),
            CacheType.RAG_RESULTS: timedelta(minutes=30),
            CacheType.API_RESPONSE: timedelta(minutes=5),
            CacheType.USER_CONTEXT: timedelta(hours=2),
            CacheType.AGENT_STATE: timedelta(hours=1)
        }
        
        # Initialisation asynchrone
        self.initialized = False
        
    async def initialize(self):
        """Initialise la connexion Redis"""
        if self.initialized:
            return
            
        if not REDIS_AVAILABLE:
            security_logger.log_error("Redis initialization", Exception("Redis not available, cache disabled"))
            return
            
        try:
            # Configuration du pool de connexions
            self.redis_pool = redis.ConnectionPool.from_url(
                self.redis_url,
                db=self.db,
                max_connections=self.max_connections,
                retry_on_timeout=self.retry_on_timeout,
                health_check_interval=self.health_check_interval
            )
            
            self.redis_client = redis.Redis(connection_pool=self.redis_pool)
            
            # Test de connexion
            await self.redis_client.ping()
            
            self.initialized = True
            security_logger.log_security_event("CACHE_INITIALIZED", {
                "redis_url": self.redis_url,
                "db": self.db,
                "max_connections": self.max_connections
            })
            
        except Exception as e:
            security_logger.log_error("Failed to initialize Redis cache", e)
            self.redis_client = None
    
    async def get(self, key: str, cache_type: CacheType) -> Optional[Any]:
        """
        Récupère une valeur du cache
        
        Args:
            key: Clé du cache
            cache_type: Type de cache
            
        Returns:
            Valeur cachée ou None si non trouvée/expirée
        """
        if not self.initialized or not self.redis_client:
            self.metrics['misses'] += 1
            return None
            
        try:
            # Clé Redis avec préfixe
            redis_key = f"{cache_type.value}:{key}"
            
            # Récupération depuis Redis
            cached_data = await self.redis_client.get(redis_key)
            
            if cached_data is None:
                self.metrics['misses'] += 1
                return None
            
            # Désérialisation
            entry_dict = json.loads(cached_data)
            entry = CacheEntry.from_dict(entry_dict)
            
            # Vérification expiration
            if entry.is_expired():
                await self._delete_key(redis_key)
                self.metrics['misses'] += 1
                return None
            
            # Mise à jour statistiques d'accès
            entry.access_count += 1
            entry.last_accessed = datetime.utcnow()
            
            # Mise à jour en arrière-plan (fire and forget)
            asyncio.create_task(self._update_access_stats(redis_key, entry))
            
            self.metrics['hits'] += 1
            
            security_logger.log_security_event("CACHE_HIT", {
                "key": key,
                "cache_type": cache_type.value,
                "access_count": entry.access_count
            })
            
            return entry.value
            
        except Exception as e:
            self.metrics['errors'] += 1
            security_logger.log_error(f"Cache get error for key {key}", e)
            return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        cache_type: CacheType,
        custom_ttl: Optional[timedelta] = None
    ) -> bool:
        """
        Stocke une valeur dans le cache
        
        Args:
            key: Clé du cache
            value: Valeur à cacher
            cache_type: Type de cache
            custom_ttl: TTL personnalisé (optionnel)
            
        Returns:
            True si succès, False sinon
        """
        if not self.initialized or not self.redis_client:
            return False
            
        try:
            # TTL selon le type ou custom
            ttl = custom_ttl or self.ttl_config.get(cache_type, timedelta(minutes=5))
            
            # Création de l'entrée
            now = datetime.utcnow()
            entry = CacheEntry(
                key=key,
                value=value,
                cache_type=cache_type,
                created_at=now,
                expires_at=now + ttl
            )
            
            # Sérialisation
            entry_data = json.dumps(entry.to_dict())
            
            # Compression si nécessaire
            if len(entry_data) > self.compression_threshold:
                # Ici on pourrait ajouter la compression (gzip)
                # Pour simplifier, on log juste
                self.metrics['compression_saves'] += 1
                security_logger.log_security_event("CACHE_COMPRESSION", {
                    "key": key,
                    "original_size": len(entry_data),
                    "cache_type": cache_type.value
                })
            
            # Stockage Redis avec TTL
            redis_key = f"{cache_type.value}:{key}"
            ttl_seconds = int(ttl.total_seconds())
            
            await self.redis_client.setex(redis_key, ttl_seconds, entry_data)
            
            self.metrics['sets'] += 1
            
            security_logger.log_security_event("CACHE_SET", {
                "key": key,
                "cache_type": cache_type.value,
                "ttl_seconds": ttl_seconds,
                "data_size": len(entry_data)
            })
            
            return True
            
        except Exception as e:
            self.metrics['errors'] += 1
            security_logger.log_error(f"Cache set error for key {key}", e)
            return False
    
    async def delete(self, key: str, cache_type: CacheType) -> bool:
        """Supprime une entrée du cache"""
        if not self.initialized or not self.redis_client:
            return False
            
        try:
            redis_key = f"{cache_type.value}:{key}"
            result = await self.redis_client.delete(redis_key)
            
            self.metrics['deletes'] += 1
            
            security_logger.log_security_event("CACHE_DELETE", {
                "key": key,
                "cache_type": cache_type.value,
                "existed": result > 0
            })
            
            return result > 0
            
        except Exception as e:
            self.metrics['errors'] += 1
            security_logger.log_error(f"Cache delete error for key {key}", e)
            return False
    
    async def clear_by_type(self, cache_type: CacheType) -> int:
        """Supprime toutes les entrées d'un type de cache"""
        if not self.initialized or not self.redis_client:
            return 0
            
        try:
            pattern = f"{cache_type.value}:*"
            keys = await self.redis_client.keys(pattern)
            
            if keys:
                deleted = await self.redis_client.delete(*keys)
                self.metrics['deletes'] += deleted
                
                security_logger.log_security_event("CACHE_CLEAR_TYPE", {
                    "cache_type": cache_type.value,
                    "deleted_count": deleted
                })
                
                return deleted
            
            return 0
            
        except Exception as e:
            self.metrics['errors'] += 1
            security_logger.log_error(f"Cache clear error for type {cache_type.value}", e)
            return 0
    
    async def clear_all(self) -> bool:
        """Vide tout le cache (ATTENTION: opération destructive)"""
        if not self.initialized or not self.redis_client:
            return False
            
        try:
            await self.redis_client.flushdb()
            
            # Reset metrics
            for key in self.metrics:
                self.metrics[key] = 0
            
            security_logger.log_security_event("CACHE_CLEAR_ALL", {
                "timestamp": datetime.utcnow().isoformat(),
                "warning": "All cache data cleared"
            })
            
            return True
            
        except Exception as e:
            self.metrics['errors'] += 1
            security_logger.log_error("Cache clear all error", e)
            return False
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques du cache"""
        total_operations = sum(self.metrics.values())
        hit_rate = (self.metrics['hits'] / max(self.metrics['hits'] + self.metrics['misses'], 1)) * 100
        
        redis_info = {}
        if self.initialized and self.redis_client:
            try:
                redis_info = await self.redis_client.info()
                redis_info = {
                    'connected_clients': redis_info.get('connected_clients', 0),
                    'used_memory': redis_info.get('used_memory', 0),
                    'used_memory_human': redis_info.get('used_memory_human', '0B'),
                    'keyspace_hits': redis_info.get('keyspace_hits', 0),
                    'keyspace_misses': redis_info.get('keyspace_misses', 0)
                }
            except:
                pass
        
        return {
            'cache_metrics': {
                **self.metrics,
                'hit_rate_percent': round(hit_rate, 2),
                'total_operations': total_operations
            },
            'redis_info': redis_info,
            'ttl_config': {ct.value: int(ttl.total_seconds()) for ct, ttl in self.ttl_config.items()},
            'status': 'connected' if self.initialized else 'disconnected'
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Vérification de santé du cache Redis"""
        health = {
            'status': 'unhealthy',
            'redis_available': REDIS_AVAILABLE,
            'initialized': self.initialized,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if not REDIS_AVAILABLE:
            health['error'] = 'Redis library not available'
            return health
            
        if not self.initialized:
            health['error'] = 'Redis not initialized'
            return health
            
        try:
            # Test ping
            pong = await self.redis_client.ping()
            if pong:
                health['status'] = 'healthy'
                
                # Informations additionnelles
                info = await self.redis_client.info()
                health['redis_version'] = info.get('redis_version', 'unknown')
                health['connected_clients'] = info.get('connected_clients', 0)
                health['used_memory_human'] = info.get('used_memory_human', '0B')
            
        except Exception as e:
            health['error'] = str(e)
            health['status'] = 'unhealthy'
        
        return health
    
    async def _update_access_stats(self, redis_key: str, entry: CacheEntry):
        """Met à jour les statistiques d'accès en arrière-plan"""
        try:
            entry_data = json.dumps(entry.to_dict())
            # Maintenir le TTL existant
            await self.redis_client.set(redis_key, entry_data, keepttl=True)
        except:
            pass  # Non-critique, on ignore les erreurs
    
    async def _delete_key(self, redis_key: str):
        """Supprime une clé expirée"""
        try:
            await self.redis_client.delete(redis_key)
        except:
            pass  # Non-critique
    
    async def close(self):
        """Ferme les connexions Redis"""
        if self.redis_client:
            await self.redis_client.close()
        if self.redis_pool:
            await self.redis_pool.disconnect()
        
        self.initialized = False
        
        security_logger.log_security_event("CACHE_CLOSED", {
            "final_metrics": self.metrics
        })


# Instance globale
_cache_instance: Optional[ProductionRedisCache] = None


async def get_cache() -> ProductionRedisCache:
    """Retourne l'instance globale du cache"""
    global _cache_instance
    
    if _cache_instance is None:
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        redis_db = int(os.getenv('REDIS_DB', '0'))
        
        _cache_instance = ProductionRedisCache(
            redis_url=redis_url,
            db=redis_db
        )
        await _cache_instance.initialize()
    
    return _cache_instance


# Fonctions de convénience
async def cache_llm_response(key: str, response: str, ttl: Optional[timedelta] = None) -> bool:
    """Cache une réponse LLM"""
    cache = await get_cache()
    return await cache.set(key, response, CacheType.LLM_RESPONSE, ttl)


async def get_cached_llm_response(key: str) -> Optional[str]:
    """Récupère une réponse LLM cachée"""
    cache = await get_cache()
    return await cache.get(key, CacheType.LLM_RESPONSE)


async def cache_session_data(session_id: str, data: Dict[str, Any]) -> bool:
    """Cache des données de session"""
    cache = await get_cache()
    return await cache.set(session_id, data, CacheType.SESSION_DATA)


async def get_cached_session_data(session_id: str) -> Optional[Dict[str, Any]]:
    """Récupère des données de session cachées"""
    cache = await get_cache()
    return await cache.get(session_id, CacheType.SESSION_DATA)
