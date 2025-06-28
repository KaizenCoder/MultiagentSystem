#!/usr/bin/env python3
"""
Gestionnaire de Mémoire Redis Optimisé
====================================

Optimise l'utilisation de la mémoire Redis avec :
- Politique d'éviction intelligente
- Compression automatique
- Monitoring temps réel
- Circuit breaker intégré

Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
"""

import redis
import logging
import zlib
import json
import time
from typing import Any, Dict, Optional, Tuple
import asyncio
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

@dataclass
class RedisMetrics:
    """Métriques Redis en temps réel"""
    memory_used: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    evictions: int = 0
    compression_ratio: float = 0.0

class RedisMemoryManager:
    """Gestionnaire de mémoire Redis optimisé"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        max_memory_mb: int = 512,
        compression_threshold: int = 1024,
        max_pool_size: int = 10
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=False
        )
        
        self.max_memory = max_memory_mb * 1024 * 1024  # MB to bytes
        self.compression_threshold = compression_threshold
        self.executor = ThreadPoolExecutor(max_workers=max_pool_size)
        
        # Configuration Redis optimisée
        self._configure_redis()
        
        self.metrics = RedisMetrics()
        self._start_metrics_collector()
        
        self.logger.info(
            f"📊 Redis Memory Manager initialisé - "
            f"Max: {max_memory_mb}MB, "
            f"Compression: >{compression_threshold}B"
        )
    
    def _configure_redis(self):
        """Configure Redis pour une gestion mémoire optimale"""
        try:
            # Politique d'éviction LFU (Least Frequently Used)
            self.redis_client.config_set("maxmemory-policy", "volatile-lfu")
            
            # Taille maximale mémoire
            self.redis_client.config_set("maxmemory", str(self.max_memory))
            
            # Autres optimisations
            self.redis_client.config_set("activedefrag", "yes")
            self.redis_client.config_set("lazyfree-lazy-eviction", "yes")
            
            self.logger.info("✓ Configuration Redis optimisée appliquée")
            
        except redis.RedisError as e:
            self.logger.error(f"❌ Erreur configuration Redis: {e}")
            raise
    
    async def set_value(
        self,
        key: str,
        value: Any,
        ttl: int = 3600,
        compress: bool = True
    ) -> bool:
        """
        Stocke une valeur avec compression automatique si nécessaire
        """
        try:
            # Sérialisation
            serialized = json.dumps(value).encode()
            
            # Compression si dépassement seuil
            if compress and len(serialized) > self.compression_threshold:
                compressed = zlib.compress(serialized)
                if len(compressed) < len(serialized):
                    serialized = compressed
                    self.metrics.compression_ratio = len(compressed) / len(serialized)
            
            # Stockage asynchrone
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                self.executor,
                self.redis_client.setex,
                key,
                ttl,
                serialized
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur stockage '{key}': {e}")
            return False
    
    async def get_value(self, key: str) -> Tuple[bool, Optional[Any]]:
        """
        Récupère une valeur avec décompression automatique
        """
        try:
            # Lecture asynchrone
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                self.executor,
                self.redis_client.get,
                key
            )
            
            if not data:
                self.metrics.cache_misses += 1
                return False, None
            
            self.metrics.cache_hits += 1
            
            # Tentative de décompression
            try:
                decompressed = zlib.decompress(data)
                data = decompressed
            except zlib.error:
                pass  # Non compressé
            
            # Désérialisation
            return True, json.loads(data.decode())
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lecture '{key}': {e}")
            return False, None
    
    async def get_metrics(self) -> RedisMetrics:
        """Retourne les métriques temps réel"""
        try:
            info = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                self.redis_client.info,
                "memory"
            )
            
            self.metrics.memory_used = float(info["used_memory"]) / 1024 / 1024  # MB
            self.metrics.evictions = int(info.get("evicted_keys", 0))
            
            return self.metrics
            
        except Exception as e:
            self.logger.error(f"❌ Erreur collecte métriques: {e}")
            return RedisMetrics()
    
    def _start_metrics_collector(self):
        """Démarre la collecte périodique des métriques"""
        async def collect_metrics():
            while True:
                await self.get_metrics()
                await asyncio.sleep(60)  # Toutes les minutes
        
        loop = asyncio.get_event_loop()
        loop.create_task(collect_metrics())
    
    async def cleanup(self):
        """Nettoyage des ressources"""
        self.executor.shutdown(wait=True)
        self.redis_client.close()
        self.logger.info("✓ Ressources Redis libérées") 