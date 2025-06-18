"""
[ROCKET] REDIS CACHE PRODUCTION - PHASE 4 IA-2
Infrastructure cache haute performance pour orchestrateur multi-agent

Objectifs :
- Support 1000+ utilisateurs simultans
- Latence cache < 5ms
- High availability multi-node
- Stratgies cache intelligentes
"""

import redis
import redis.sentinel
import asyncio
import json
import hashlib
import time
import logging
from typing import Any, Optional, Dict, List, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheStrategy(Enum):
    """Stratgies de cache par type de donnes"""
    LLM_RESPONSES = "llm_responses"      # TTL 1h
    USER_SESSIONS = "user_sessions"      # TTL 24h  
    RAG_RESULTS = "rag_results"          # TTL 30min
    API_RESPONSES = "api_responses"      # TTL 5min
    SYSTEM_CONFIG = "system_config"      # TTL 1h
    METRICS_CACHE = "metrics_cache"      # TTL 10min

@dataclass
class CacheConfig:
    """Configuration cache production"""
    # Redis Cluster Configuration
    nodes: List[Dict[str, Any]] = None
    sentinel_hosts: List[str] = None
    master_name: str = "orchestrator-master"
    
    # Performance Settings
    max_connections: int = 100
    retry_on_timeout: bool = True
    socket_timeout: float = 5.0
    socket_connect_timeout: float = 5.0
    health_check_interval: int = 30
    
    # Cache TTL par stratgie (secondes)
    ttl_config: Dict[CacheStrategy, int] = None
    
    def __post_init__(self):
        if self.nodes is None:
            self.nodes = [
                {"host": "redis-node1", "port": 6379},
                {"host": "redis-node2", "port": 6379}, 
                {"host": "redis-node3", "port": 6379}
            ]
            
        if self.sentinel_hosts is None:
            self.sentinel_hosts = [
                "redis-sentinel1:26379",
                "redis-sentinel2:26379", 
                "redis-sentinel3:26379"
            ]
            
        if self.ttl_config is None:
            self.ttl_config = {
                CacheStrategy.LLM_RESPONSES: 3600,    # 1h
                CacheStrategy.USER_SESSIONS: 86400,   # 24h
                CacheStrategy.RAG_RESULTS: 1800,      # 30min
                CacheStrategy.API_RESPONSES: 300,     # 5min
                CacheStrategy.SYSTEM_CONFIG: 3600,    # 1h
                CacheStrategy.METRICS_CACHE: 600      # 10min
            }

class RedisProductionCache:
    """Cache Redis production haute performance"""
    
    def __init__(self, config: CacheConfig = None):
        self.config = config or CacheConfig()
        self.redis_client = None
        self.sentinel = None
        self.connection_pool = None
        self.is_cluster_mode = True
        
        # Mtriques performance
        self.hit_count = 0
        self.miss_count = 0
        self.error_count = 0
        self.total_operations = 0
        
    async def initialize(self) -> bool:
        """Initialise connexion Redis avec failover"""
        try:
            # Tentative connexion Sentinel (HA)
            if await self._initialize_sentinel():
                logger.info("[CHECK] Redis Sentinel initialis avec succs")
                return True
                
            # Fallback : connexion directe cluster
            if await self._initialize_cluster():
                logger.info("[CHECK] Redis Cluster initialis avec succs")
                return True
                
            # Fallback : connexion single node (dev)
            if await self._initialize_single_node():
                logger.warning(" Redis single node initialis (mode dev)")
                return True
                
            logger.error("[CROSS] chec initialisation Redis")
            return False
            
        except Exception as e:
            logger.error(f"[CROSS] Erreur initialisation Redis : {e}")
            self.error_count += 1
            return False
    
    async def _initialize_sentinel(self) -> bool:
        """Initialise Redis avec Sentinel (HA production)"""
        try:
            # Parse sentinel hosts
            sentinel_list = []
            for host_port in self.config.sentinel_hosts:
                host, port = host_port.split(':')
                sentinel_list.append((host, int(port)))
            
            # Crer Sentinel
            self.sentinel = redis.sentinel.Sentinel(
                sentinel_list,
                socket_timeout=self.config.socket_timeout,
                socket_connect_timeout=self.config.socket_connect_timeout
            )
            
            # Obtenir master
            self.redis_client = self.sentinel.master_for(
                self.config.master_name,
                socket_timeout=self.config.socket_timeout,
                retry_on_timeout=self.config.retry_on_timeout
            )
            
            # Test connexion
            await asyncio.get_event_loop().run_in_executor(
                None, self.redis_client.ping
            )
            
            return True
            
        except Exception as e:
            logger.warning(f"Sentinel initialization failed : {e}")
            return False
    
    async def _initialize_cluster(self) -> bool:
        """Initialise Redis Cluster"""
        try:
            from rediscluster import RedisCluster
            
            self.redis_client = RedisCluster(
                startup_nodes=self.config.nodes,
                max_connections=self.config.max_connections,
                socket_timeout=self.config.socket_timeout,
                retry_on_timeout=self.config.retry_on_timeout,
                decode_responses=True
            )
            
            # Test connexion
            await asyncio.get_event_loop().run_in_executor(
                None, self.redis_client.ping
            )
            
            return True
            
        except Exception as e:
            logger.warning(f"Cluster initialization failed : {e}")
            return False
    
    async def _initialize_single_node(self) -> bool:
        """Fallback : connexion single node"""
        try:
            self.redis_client = redis.Redis(
                host=self.config.nodes[0]["host"],
                port=self.config.nodes[0]["port"],
                max_connections=self.config.max_connections,
                socket_timeout=self.config.socket_timeout,
                retry_on_timeout=self.config.retry_on_timeout,
                decode_responses=True
            )
            
            # Test connexion
            await asyncio.get_event_loop().run_in_executor(
                None, self.redis_client.ping
            )
            
            self.is_cluster_mode = False
            return True
            
        except Exception as e:
            logger.error(f"Single node initialization failed : {e}")
            return False
    
    def _generate_cache_key(self, strategy: CacheStrategy, key: str, 
                           user_id: str = None) -> str:
        """Gnre cl cache standardise"""
        base_key = f"orchestrator:{strategy.value}:{key}"
        
        if user_id:
            base_key = f"{base_key}:user:{user_id}"
            
        return base_key
    
    def _hash_large_key(self, key: str) -> str:
        """Hash cls trop longues pour Redis"""
        if len(key) > 250:  # Limite Redis
            return hashlib.sha256(key.encode()).hexdigest()
        return key
    
    async def set(self, strategy: CacheStrategy, key: str, value: Any,
                  user_id: str = None, custom_ttl: int = None) -> bool:
        """Store valeur dans cache avec TTL"""
        try:
            self.total_operations += 1
            
            # Gnration cl standardise
            cache_key = self._generate_cache_key(strategy, key, user_id)
            cache_key = self._hash_large_key(cache_key)
            
            # Srialisation valeur
            if isinstance(value, (dict, list)):
                serialized_value = json.dumps(value, ensure_ascii=False)
            else:
                serialized_value = str(value)
            
            # TTL selon stratgie
            ttl = custom_ttl or self.config.ttl_config[strategy]
            
            # Store avec TTL
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.redis_client.setex(cache_key, ttl, serialized_value)
            )
            
            if result:
                logger.debug(f"[CHECK] Cache SET: {cache_key[:50]}... TTL={ttl}s")
                return True
            else:
                logger.warning(f" Cache SET failed: {cache_key[:50]}...")
                return False
                
        except Exception as e:
            logger.error(f"[CROSS] Cache SET error: {e}")
            self.error_count += 1
            return False
    
    async def get(self, strategy: CacheStrategy, key: str,
                  user_id: str = None) -> Optional[Any]:
        """Rcupre valeur du cache"""
        try:
            self.total_operations += 1
            
            # Gnration cl
            cache_key = self._generate_cache_key(strategy, key, user_id)
            cache_key = self._hash_large_key(cache_key)
            
            # Rcupration
            value = await asyncio.get_event_loop().run_in_executor(
                None,
                self.redis_client.get,
                cache_key
            )
            
            if value is not None:
                self.hit_count += 1
                logger.debug(f"[CHECK] Cache HIT: {cache_key[:50]}...")
                
                # Dsrialisation
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            else:
                self.miss_count += 1
                logger.debug(f"[CROSS] Cache MISS: {cache_key[:50]}...")
                return None
                
        except Exception as e:
            logger.error(f"[CROSS] Cache GET error: {e}")
            self.error_count += 1
            return None
    
    async def delete(self, strategy: CacheStrategy, key: str,
                     user_id: str = None) -> bool:
        """Supprime valeur du cache"""
        try:
            cache_key = self._generate_cache_key(strategy, key, user_id)
            cache_key = self._hash_large_key(cache_key)
            
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                self.redis_client.delete,
                cache_key
            )
            
            logger.debug(f" Cache DELETE: {cache_key[:50]}...")
            return result > 0
            
        except Exception as e:
            logger.error(f"[CROSS] Cache DELETE error: {e}")
            self.error_count += 1
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """Supprime toutes les cls correspondant au pattern"""
        try:
            if self.is_cluster_mode:
                # Pour cluster, itrer sur tous les nodes
                deleted = 0
                for key in self.redis_client.scan_iter(match=pattern):
                    if self.redis_client.delete(key):
                        deleted += 1
                return deleted
            else:
                # Single node
                keys = self.redis_client.keys(pattern)
                if keys:
                    return self.redis_client.delete(*keys)
                return 0
                
        except Exception as e:
            logger.error(f"[CROSS] Cache CLEAR error: {e}")
            self.error_count += 1
            return 0
    
    async def get_stats(self) -> Dict[str, Any]:
        """Statistiques cache performance"""
        try:
            # Stats Redis
            info = await asyncio.get_event_loop().run_in_executor(
                None, self.redis_client.info
            )
            
            # Calculs mtriques
            hit_rate = (self.hit_count / max(self.total_operations, 1)) * 100
            miss_rate = (self.miss_count / max(self.total_operations, 1)) * 100
            error_rate = (self.error_count / max(self.total_operations, 1)) * 100
            
            return {
                "hit_count": self.hit_count,
                "miss_count": self.miss_count,
                "error_count": self.error_count,
                "total_operations": self.total_operations,
                "hit_rate_percent": round(hit_rate, 2),
                "miss_rate_percent": round(miss_rate, 2),
                "error_rate_percent": round(error_rate, 2),
                "redis_memory_used": info.get("used_memory_human", "N/A"),
                "redis_connected_clients": info.get("connected_clients", 0),
                "redis_ops_per_sec": info.get("instantaneous_ops_per_sec", 0),
                "cluster_mode": self.is_cluster_mode,
                "uptime_seconds": info.get("uptime_in_seconds", 0)
            }
            
        except Exception as e:
            logger.error(f"[CROSS] Cache STATS error: {e}")
            return {"error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check complet du cache"""
        try:
            start_time = time.time()
            
            # Test ping
            ping_result = await asyncio.get_event_loop().run_in_executor(
                None, self.redis_client.ping
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Test set/get
            test_key = f"health_check_{int(time.time())}"
            test_value = {"timestamp": datetime.now().isoformat()}
            
            set_success = await self.set(
                CacheStrategy.METRICS_CACHE, 
                test_key, 
                test_value,
                custom_ttl=60
            )
            
            get_result = await self.get(CacheStrategy.METRICS_CACHE, test_key)
            
            await self.delete(CacheStrategy.METRICS_CACHE, test_key)
            
            return {
                "status": "healthy" if ping_result and set_success and get_result else "unhealthy",
                "ping_success": ping_result,
                "latency_ms": round(latency_ms, 2),
                "set_success": set_success,
                "get_success": get_result is not None,
                "timestamp": datetime.now().isoformat(),
                "cluster_mode": self.is_cluster_mode
            }
            
        except Exception as e:
            logger.error(f"[CROSS] Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Instance singleton cache production
_cache_instance: Optional[RedisProductionCache] = None

async def get_production_cache() -> RedisProductionCache:
    """Obtient instance cache production (singleton)"""
    global _cache_instance
    
    if _cache_instance is None:
        _cache_instance = RedisProductionCache()
        await _cache_instance.initialize()
    
    return _cache_instance

# Utilitaires pour tests de charge
async def benchmark_cache_performance(num_operations: int = 1000) -> Dict[str, Any]:
    """Benchmark performance cache pour validation 1000+ users"""
    cache = await get_production_cache()
    
    start_time = time.time()
    operations_success = 0
    
    for i in range(num_operations):
        # Test SET
        key = f"benchmark_key_{i}"
        value = {"data": f"benchmark_value_{i}", "timestamp": time.time()}
        
        if await cache.set(CacheStrategy.API_RESPONSES, key, value):
            operations_success += 1
        
        # Test GET
        retrieved = await cache.get(CacheStrategy.API_RESPONSES, key)
        if retrieved:
            operations_success += 1
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Nettoyage
    await cache.clear_pattern("orchestrator:api_responses:benchmark_key_*")
    
    return {
        "total_operations": num_operations * 2,  # SET + GET
        "successful_operations": operations_success,
        "total_time_seconds": round(total_time, 3),
        "operations_per_second": round((num_operations * 2) / total_time, 2),
        "average_latency_ms": round((total_time / (num_operations * 2)) * 1000, 3),
        "success_rate_percent": round((operations_success / (num_operations * 2)) * 100, 2)
    }

if __name__ == "__main__":
    # Test autonome
    async def test_cache():
        print("[ROCKET] REDIS PRODUCTION CACHE - TEST")
        print("=" * 50)
        
        cache = RedisProductionCache()
        if await cache.initialize():
            print("[CHECK] Cache initialis")
            
            # Test basic
            await cache.set(CacheStrategy.LLM_RESPONSES, "test", {"data": "test"})
            result = await cache.get(CacheStrategy.LLM_RESPONSES, "test")
            print(f"[CHECK] Test basic: {result}")
            
            # Benchmark
            print("\n[CHART] Benchmark performance...")
            benchmark = await benchmark_cache_performance(100)
            print(f"Oprations/sec: {benchmark['operations_per_second']}")
            print(f"Latence moyenne: {benchmark['average_latency_ms']}ms")
            
            # Stats
            stats = await cache.get_stats()
            print(f"Hit rate: {stats['hit_rate_percent']}%")
            
        else:
            print("[CROSS] chec initialisation cache")
    
    asyncio.run(test_cache()) 