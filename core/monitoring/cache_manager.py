"""
Gestionnaire de Cache Intelligent Multi-Niveaux
NextGeneration Maintenance Team - Cache Management

Système de cache intelligent avec:
- Cache mémoire (LRU) pour accès ultra-rapide
- Cache Redis pour persistance distribuée
- Statistiques de performance détaillées
- Gestion automatique TTL et éviction
"""

from functools import lru_cache
import hashlib
import pickle
import time
import logging
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass
from collections import defaultdict

# Import conditionnel de Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

@dataclass
class CacheStats:
    """Statistiques de performance du cache"""
    hits: int = 0
    misses: int = 0
    sets: int = 0
    deletes: int = 0
    memory_hits: int = 0
    redis_hits: int = 0
    total_size: int = 0
    avg_access_time: float = 0.0
    
    @property
    def hit_rate(self) -> float:
        """Calcule le taux de hit"""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0
    
    @property
    def memory_hit_rate(self) -> float:
        """Taux de hit du cache mémoire"""
        return (self.memory_hits / self.hits * 100) if self.hits > 0 else 0

class IntelligentCache:
    """Cache multi-niveaux : mémoire -> Redis -> Fallback"""
    
    def __init__(self, 
                 redis_host: str = "localhost",
                 redis_port: int = 6379,
                 redis_db: int = 0,
                 redis_password: Optional[str] = None,
                 default_ttl: int = 3600,
                 max_memory_items: int = 1000,
                 enable_redis: bool = True):
        """
        Initialise le cache intelligent
        
        Args:
            redis_host: Host Redis
            redis_port: Port Redis
            redis_db: Base de données Redis
            redis_password: Mot de passe Redis
            default_ttl: TTL par défaut en secondes
            max_memory_items: Nombre max d'items en mémoire
            enable_redis: Activer le cache Redis
        """
        self.default_ttl = default_ttl
        self.max_memory_items = max_memory_items
        self.enable_redis = enable_redis and REDIS_AVAILABLE
        
        # Cache mémoire avec LRU
        self._memory_cache: Dict[str, Dict] = {}
        self._access_times: Dict[str, float] = {}
        
        # Statistiques
        self.stats = CacheStats()
        self._operation_times = []
        
        # Logger
        self.logger = logging.getLogger(f"{__name__}.IntelligentCache")
        
        # Client Redis
        self._redis_client = None
        if self.enable_redis:
            self._setup_redis(redis_host, redis_port, redis_db, redis_password)
    
    def _setup_redis(self, host: str, port: int, db: int, password: Optional[str]):
        """Configuration du client Redis"""
        try:
            self._redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True,
                decode_responses=False  # Pour gérer les données binaires
            )
            
            # Test de connexion
            self._redis_client.ping()
            self.logger.info(f"✅ Cache Redis connecté: {host}:{port}/{db}")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Redis non disponible: {e} - Mode cache mémoire uniquement")
            self._redis_client = None
            self.enable_redis = False
    
    @lru_cache(maxsize=10000)
    def _get_cache_key(self, key: str, namespace: str = "default") -> str:
        """Génère une clé de cache avec namespace"""
        return f"nextgen:cache:{namespace}:{hashlib.sha256(key.encode()).hexdigest()[:16]}"
    
    async def get(self, key: str, namespace: str = "default") -> Optional[Any]:
        """Récupération avec cache multi-niveaux"""
        start_time = time.time()
        cache_key = self._get_cache_key(key, namespace)
        
        try:
            # Niveau 1: Cache mémoire
            if cache_key in self._memory_cache:
                item = self._memory_cache[cache_key]
                
                # Vérification TTL
                if item['expires_at'] > time.time():
                    self._access_times[cache_key] = time.time()
                    self.stats.hits += 1
                    self.stats.memory_hits += 1
                    
                    self.logger.debug(f"⚡ Cache mémoire hit: {namespace}:{key[:20]}...")
                    return item['data']
                else:
                    # Expiration - suppression
                    del self._memory_cache[cache_key]
                    if cache_key in self._access_times:
                        del self._access_times[cache_key]
            
            # Niveau 2: Cache Redis
            if self.enable_redis and self._redis_client:
                try:
                    redis_data = self._redis_client.get(cache_key)
                    if redis_data:
                        data = pickle.loads(redis_data)
                        
                        # Promotion vers cache mémoire
                        self._set_memory_cache(cache_key, data, self.default_ttl)
                        
                        self.stats.hits += 1
                        self.stats.redis_hits += 1
                        
                        self.logger.debug(f"📡 Cache Redis hit: {namespace}:{key[:20]}...")
                        return data
                        
                except Exception as e:
                    self.logger.warning(f"⚠️ Erreur Redis get: {e}")
            
            # Cache miss
            self.stats.misses += 1
            self.logger.debug(f"❌ Cache miss: {namespace}:{key[:20]}...")
            return None
            
        finally:
            # Enregistrement du temps d'accès
            access_time = time.time() - start_time
            self._operation_times.append(access_time)
            if len(self._operation_times) > 1000:
                self._operation_times = self._operation_times[-1000:]
            
            # Mise à jour moyenne
            if self._operation_times:
                self.stats.avg_access_time = sum(self._operation_times) / len(self._operation_times)
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None, namespace: str = "default"):
        """Stockage multi-niveaux"""
        start_time = time.time()
        cache_key = self._get_cache_key(key, namespace)
        ttl = ttl or self.default_ttl
        
        try:
            # Stockage mémoire
            self._set_memory_cache(cache_key, value, ttl)
            
            # Stockage Redis
            if self.enable_redis and self._redis_client:
                try:
                    serialized_data = pickle.dumps(value)
                    self._redis_client.setex(cache_key, ttl, serialized_data)
                    self.logger.debug(f"💾 Stocké en Redis: {namespace}:{key[:20]}... (TTL: {ttl}s)")
                    
                except Exception as e:
                    self.logger.warning(f"⚠️ Erreur Redis set: {e}")
            
            self.stats.sets += 1
            self.logger.debug(f"✅ Cache set: {namespace}:{key[:20]}... (TTL: {ttl}s)")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur cache set: {e}")
    
    def _set_memory_cache(self, cache_key: str, data: Any, ttl: int):
        """Stockage en cache mémoire avec gestion LRU"""
        # Éviction LRU si nécessaire
        if len(self._memory_cache) >= self.max_memory_items:
            self._evict_lru()
        
        expires_at = time.time() + ttl
        self._memory_cache[cache_key] = {
            'data': data,
            'expires_at': expires_at,
            'created_at': time.time()
        }
        self._access_times[cache_key] = time.time()
    
    def _evict_lru(self):
        """Éviction LRU des éléments les moins récemment utilisés"""
        if not self._access_times:
            return
        
        # Éviction de 10% des éléments les plus anciens
        items_to_evict = max(1, len(self._access_times) // 10)
        
        # Tri par temps d'accès
        sorted_items = sorted(self._access_times.items(), key=lambda x: x[1])
        
        for cache_key, _ in sorted_items[:items_to_evict]:
            if cache_key in self._memory_cache:
                del self._memory_cache[cache_key]
            if cache_key in self._access_times:
                del self._access_times[cache_key]
        
        self.logger.debug(f"🧹 Éviction LRU: {items_to_evict} éléments supprimés")
    
    async def delete(self, key: str, namespace: str = "default"):
        """Suppression multi-niveaux"""
        cache_key = self._get_cache_key(key, namespace)
        
        # Suppression mémoire
        if cache_key in self._memory_cache:
            del self._memory_cache[cache_key]
        if cache_key in self._access_times:
            del self._access_times[cache_key]
        
        # Suppression Redis
        if self.enable_redis and self._redis_client:
            try:
                self._redis_client.delete(cache_key)
            except Exception as e:
                self.logger.warning(f"⚠️ Erreur Redis delete: {e}")
        
        self.stats.deletes += 1
        self.logger.debug(f"🗑️ Cache delete: {namespace}:{key[:20]}...")
    
    async def clear(self, namespace: Optional[str] = None):
        """Nettoyage du cache"""
        if namespace:
            # Nettoyage d'un namespace spécifique
            pattern = f"nextgen:cache:{namespace}:"
            keys_to_delete = [k for k in self._memory_cache.keys() if k.startswith(pattern)]
            
            for key in keys_to_delete:
                if key in self._memory_cache:
                    del self._memory_cache[key]
                if key in self._access_times:
                    del self._access_times[key]
            
            # Redis
            if self.enable_redis and self._redis_client:
                try:
                    redis_pattern = f"nextgen:cache:{namespace}:*"
                    redis_keys = self._redis_client.keys(redis_pattern)
                    if redis_keys:
                        self._redis_client.delete(*redis_keys)
                except Exception as e:
                    self.logger.warning(f"⚠️ Erreur Redis clear: {e}")
            
            self.logger.info(f"🧹 Cache namespace '{namespace}' nettoyé")
        else:
            # Nettoyage complet
            self._memory_cache.clear()
            self._access_times.clear()
            
            if self.enable_redis and self._redis_client:
                try:
                    redis_keys = self._redis_client.keys("nextgen:cache:*")
                    if redis_keys:
                        self._redis_client.delete(*redis_keys)
                except Exception as e:
                    self.logger.warning(f"⚠️ Erreur Redis clear all: {e}")
            
            self.logger.info("🧹 Cache complet nettoyé")
    
    def get_stats(self) -> Dict[str, Any]:
        """Statistiques de performance du cache"""
        memory_size = len(self._memory_cache)
        
        # Calcul de la taille approximative en mémoire
        estimated_memory_size = sum(
            len(pickle.dumps(item['data'])) 
            for item in list(self._memory_cache.values())[:100]  # Échantillon
        ) * (memory_size / 100) if memory_size > 0 else 0
        
        return {
            "hit_rate": f"{self.stats.hit_rate:.1f}%",
            "memory_hit_rate": f"{self.stats.memory_hit_rate:.1f}%",
            "total_hits": self.stats.hits,
            "total_misses": self.stats.misses,
            "memory_hits": self.stats.memory_hits,
            "redis_hits": self.stats.redis_hits,
            "total_sets": self.stats.sets,
            "total_deletes": self.stats.deletes,
            "memory_items": memory_size,
            "estimated_memory_size_mb": estimated_memory_size / 1024 / 1024,
            "avg_access_time_ms": self.stats.avg_access_time * 1000,
            "redis_enabled": self.enable_redis,
            "redis_connected": self._redis_client is not None
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """État de santé du cache"""
        stats = self.get_stats()
        
        # Évaluation de la santé
        health_score = 100
        issues = []
        
        # Vérification du hit rate
        if self.stats.hit_rate < 50:
            health_score -= 20
            issues.append("Taux de hit faible (<50%)")
        
        # Vérification de la connexion Redis
        if self.enable_redis and not self._redis_client:
            health_score -= 30
            issues.append("Redis déconnecté")
        
        # Vérification de la mémoire
        if stats["memory_items"] > self.max_memory_items * 0.9:
            health_score -= 10
            issues.append("Cache mémoire presque plein")
        
        # Vérification du temps d'accès
        if self.stats.avg_access_time > 0.1:  # 100ms
            health_score -= 15
            issues.append("Temps d'accès élevé")
        
        health_status = "🟢" if health_score >= 80 else "🟡" if health_score >= 60 else "🔴"
        
        return {
            "health_score": health_score,
            "health_status": health_status,
            "issues": issues,
            "recommendations": self._get_recommendations(stats, issues)
        }
    
    def _get_recommendations(self, stats: Dict, issues: List[str]) -> List[str]:
        """Génère des recommandations d'optimisation"""
        recommendations = []
        
        if "Taux de hit faible" in issues:
            recommendations.append("Augmenter le TTL ou optimiser les clés de cache")
        
        if "Redis déconnecté" in issues:
            recommendations.append("Vérifier la connexion Redis et redémarrer si nécessaire")
        
        if "Cache mémoire presque plein" in issues:
            recommendations.append("Augmenter max_memory_items ou nettoyer le cache")
        
        if "Temps d'accès élevé" in issues:
            recommendations.append("Optimiser la sérialisation ou réduire la taille des données")
        
        # Recommandations générales
        memory_hit_rate = float(stats["memory_hit_rate"].rstrip('%'))
        if memory_hit_rate < 80 and self.enable_redis:
            recommendations.append("Considérer augmenter la taille du cache mémoire")
        
        return recommendations
    
    async def warmup(self, data_loader: callable, keys: List[str], namespace: str = "default"):
        """Préchauffage du cache avec des données"""
        self.logger.info(f"🔥 Démarrage warmup cache: {len(keys)} clés")
        
        successful = 0
        failed = 0
        
        for key in keys:
            try:
                data = await data_loader(key)
                if data is not None:
                    await self.set(key, data, namespace=namespace)
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                self.logger.warning(f"⚠️ Erreur warmup {key}: {e}")
                failed += 1
        
        self.logger.info(f"✅ Warmup terminé: {successful} succès, {failed} échecs")
        return {"successful": successful, "failed": failed}

# Instance globale
global_cache = IntelligentCache()

def get_global_cache() -> IntelligentCache:
    """Récupère l'instance globale du cache"""
    return global_cache

# Décorateur pour mise en cache automatique
def cached(ttl: int = 3600, namespace: str = "default", key_func: Optional[callable] = None):
    """Décorateur pour mise en cache automatique des résultats"""
    
    def decorator(func: callable):
        async def wrapper(*args, **kwargs):
            # Génération de la clé de cache
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Clé basée sur les arguments
                args_str = str(args) + str(sorted(kwargs.items()))
                cache_key = f"{func.__name__}:{hashlib.sha256(args_str.encode()).hexdigest()[:16]}"
            
            # Tentative de récupération du cache
            cached_result = await global_cache.get(cache_key, namespace)
            if cached_result is not None:
                return cached_result
            
            # Exécution et mise en cache
            result = await func(*args, **kwargs)
            await global_cache.set(cache_key, result, ttl, namespace)
            
            return result
        
        return wrapper
    return decorator

# Exemple d'usage
if __name__ == "__main__":
    import asyncio
    
    async def test_cache():
        """Test du cache intelligent"""
        cache = IntelligentCache(enable_redis=False)  # Mode mémoire pour test
        
        # Test basique
        await cache.set("test_key", {"data": "test_value"}, ttl=60)
        result = await cache.get("test_key")
        print(f"✅ Test basique: {result}")
        
        # Test avec namespace
        await cache.set("user:123", {"name": "John", "age": 30}, namespace="users")
        user = await cache.get("user:123", namespace="users")
        print(f"✅ Test namespace: {user}")
        
        # Simulation de charge
        for i in range(100):
            await cache.set(f"key_{i}", f"value_{i}")
            if i % 10 == 0:
                await cache.get(f"key_{i-5}")  # Quelques hits
        
        # Statistiques
        stats = cache.get_stats()
        print(f"\n📊 Statistiques:")
        print(f"   Hit rate: {stats['hit_rate']}")
        print(f"   Items en mémoire: {stats['memory_items']}")
        print(f"   Temps d'accès moyen: {stats['avg_access_time_ms']:.2f}ms")
        
        # État de santé
        health = cache.get_health_status()
        print(f"\n💚 Santé du cache: {health['health_status']} (Score: {health['health_score']})")
        if health['issues']:
            print(f"   Issues: {health['issues']}")
        if health['recommendations']:
            print(f"   Recommandations: {health['recommendations']}")
    
    # Exécution du test
    asyncio.run(test_cache()) 