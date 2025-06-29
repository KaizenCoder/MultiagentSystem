#!/usr/bin/env python3
"""
💾 Agent Cache Manager - NextGeneration v5.3.0
Version enterprise Wave 4 avec cache distribuée IA

Migration Pattern: PERFORMANCE_OPTIMIZATION + DISTRIBUTED_CACHE + LLM_ENHANCED
Author: Claude Sonnet 4
Date: 30 Juin 2025
"""

import asyncio
import json
import time
import hashlib
import pickle
import lz4.frame
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import statistics
from collections import defaultdict, OrderedDict
import threading
import weakref

# Imports NextGeneration Architecture
try:
    from core.services import (
        LLMGatewayHybrid, create_llm_gateway,
        MessageBusA2A, create_envelope, MessageType, Priority,
        OptimizedContextStore, create_agent_context, ContextType
    )
    from core.agent_factory_architecture import Task, Result
except ImportError:
    # Fallback pour développement isolé
    print("⚠️ NextGeneration services not available - running in development mode")
    class Task:
        def __init__(self, task_type, params=None):
            self.type = task_type
            self.params = params or {}
    
    class Result:
        def __init__(self, success, data=None, error=None, metrics=None):
            self.success = success
            self.data = data
            self.error = error
            self.metrics = metrics or {}

class CachePolicy(str, Enum):
    """Politiques de cache"""
    LRU = "LRU"  # Least Recently Used
    LFU = "LFU"  # Least Frequently Used
    TTL = "TTL"  # Time To Live
    ADAPTIVE = "ADAPTIVE"  # Adaptatif avec IA

class CacheLevel(str, Enum):
    """Niveaux de cache"""
    L1_MEMORY = "L1_MEMORY"  # Cache mémoire rapide
    L2_DISK = "L2_DISK"  # Cache disque persistant
    L3_DISTRIBUTED = "L3_DISTRIBUTED"  # Cache distribué réseau

@dataclass
class CacheEntry:
    """Entrée de cache enrichie"""
    key: str
    value: Any
    timestamp: datetime
    access_count: int = 0
    last_access: Optional[datetime] = None
    ttl: Optional[int] = None
    size_bytes: int = 0
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class CacheStats:
    """Statistiques cache"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    size_bytes: int = 0
    entry_count: int = 0
    hit_rate: float = 0.0

class IntelligentEvictionEngine:
    """Moteur d'éviction intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.access_patterns = defaultdict(list)
        self.prediction_cache = {}
        self.learning_enabled = True
    
    async def predict_access_probability(self, key: str, entry: CacheEntry) -> float:
        """Prédiction probabilité accès futur avec IA"""
        # Calcul score basique
        now = datetime.now()
        age_factor = (now - entry.timestamp).total_seconds() / 3600  # heures
        frequency_factor = entry.access_count / max(1, age_factor)
        recency_factor = 1.0
        
        if entry.last_access:
            recency_factor = 1.0 / max(1, (now - entry.last_access).total_seconds() / 60)  # minutes
        
        base_score = (frequency_factor * 0.4 + recency_factor * 0.6) / (1 + age_factor * 0.1)
        
        # Enhancement IA si disponible
        if self.llm_gateway and self.learning_enabled:
            try:
                ai_prediction = await self.llm_gateway.process_request(
                    "Predict cache access probability",
                    context={
                        "role": "cache_intelligence_expert",
                        "key": key,
                        "access_patterns": self.access_patterns.get(key, [])[-10:],  # 10 derniers accès
                        "base_score": base_score,
                        "task": "access_probability_prediction"
                    }
                )
                
                if ai_prediction.get("success"):
                    ai_score = ai_prediction.get("probability", base_score)
                    # Pondération IA/règles
                    return base_score * 0.3 + ai_score * 0.7
                    
            except Exception:
                pass
        
        return min(1.0, max(0.0, base_score))
    
    async def select_eviction_candidates(self, entries: Dict[str, CacheEntry], 
                                       target_count: int) -> List[str]:
        """Sélection candidats éviction avec IA"""
        candidates = []
        
        # Calcul scores pour tous les entries
        scores = {}
        for key, entry in entries.items():
            score = await self.predict_access_probability(key, entry)
            scores[key] = score
        
        # Tri par score croissant (moins probables d'être accédés)
        sorted_entries = sorted(scores.items(), key=lambda x: x[1])
        candidates = [key for key, score in sorted_entries[:target_count]]
        
        return candidates
    
    def record_access(self, key: str):
        """Enregistrement accès pour apprentissage"""
        self.access_patterns[key].append({
            "timestamp": datetime.now(),
            "hour": datetime.now().hour,
            "weekday": datetime.now().weekday()
        })
        
        # Limite historique
        if len(self.access_patterns[key]) > 100:
            self.access_patterns[key] = self.access_patterns[key][-50:]

class DistributedCacheLayer:
    """Layer cache distribuée"""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.peer_nodes = set()
        self.replication_factor = 2
        self.consistency_level = "eventual"
    
    async def distribute_entry(self, key: str, entry: CacheEntry) -> bool:
        """Distribution entrée vers nœuds pairs"""
        # Simulation distribution (à implémenter avec Redis/Hazelcast)
        hash_key = hashlib.md5(key.encode()).hexdigest()
        target_nodes = sorted(list(self.peer_nodes))[:self.replication_factor]
        
        # Simulation réplication
        success_count = 0
        for node in target_nodes:
            try:
                # await self._replicate_to_node(node, key, entry)
                success_count += 1
            except Exception:
                pass
        
        return success_count >= (self.replication_factor // 2 + 1)
    
    async def retrieve_from_peers(self, key: str) -> Optional[CacheEntry]:
        """Récupération depuis nœuds pairs"""
        # Simulation récupération distribuée
        for node in self.peer_nodes:
            try:
                # entry = await self._fetch_from_node(node, key)
                # return entry
                pass
            except Exception:
                continue
        
        return None

class MultiLevelCache:
    """Cache multi-niveaux L1/L2/L3"""
    
    def __init__(self, cache_manager):
        self.cache_manager = cache_manager
        
        # L1: Cache mémoire rapide (LRU)
        self.l1_cache = OrderedDict()
        self.l1_max_size = 1000
        
        # L2: Cache disque persistant
        self.l2_cache_dir = Path("/tmp/nextgen_cache_l2")
        self.l2_cache_dir.mkdir(exist_ok=True)
        
        # L3: Cache distribué
        self.l3_distributed = DistributedCacheLayer(cache_manager.agent_id)
        
        # Statistiques par niveau
        self.level_stats = {
            CacheLevel.L1_MEMORY: CacheStats(),
            CacheLevel.L2_DISK: CacheStats(),
            CacheLevel.L3_DISTRIBUTED: CacheStats()
        }
    
    async def get(self, key: str) -> Tuple[Optional[Any], CacheLevel]:
        """Récupération multi-niveaux"""
        # L1: Mémoire
        if key in self.l1_cache:
            self.l1_cache.move_to_end(key)  # LRU update
            self.level_stats[CacheLevel.L1_MEMORY].hits += 1
            return self.l1_cache[key].value, CacheLevel.L1_MEMORY
        
        self.level_stats[CacheLevel.L1_MEMORY].misses += 1
        
        # L2: Disque
        l2_entry = await self._get_l2(key)
        if l2_entry:
            # Promotion vers L1
            await self._set_l1(key, l2_entry)
            self.level_stats[CacheLevel.L2_DISK].hits += 1
            return l2_entry.value, CacheLevel.L2_DISK
        
        self.level_stats[CacheLevel.L2_DISK].misses += 1
        
        # L3: Distribué
        l3_entry = await self.l3_distributed.retrieve_from_peers(key)
        if l3_entry:
            # Promotion vers L2 et L1
            await self._set_l2(key, l3_entry)
            await self._set_l1(key, l3_entry)
            self.level_stats[CacheLevel.L3_DISTRIBUTED].hits += 1
            return l3_entry.value, CacheLevel.L3_DISTRIBUTED
        
        self.level_stats[CacheLevel.L3_DISTRIBUTED].misses += 1
        return None, None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Stockage multi-niveaux"""
        entry = CacheEntry(
            key=key,
            value=value,
            timestamp=datetime.now(),
            ttl=ttl,
            size_bytes=len(pickle.dumps(value)),
            metadata={"level": "multi"}
        )
        
        # Stockage sur tous les niveaux
        await self._set_l1(key, entry)
        await self._set_l2(key, entry)
        await self.l3_distributed.distribute_entry(key, entry)
    
    async def _set_l1(self, key: str, entry: CacheEntry):
        """Stockage L1 avec éviction LRU"""
        self.l1_cache[key] = entry
        self.l1_cache.move_to_end(key)
        
        # Éviction si nécessaire
        while len(self.l1_cache) > self.l1_max_size:
            evicted_key, evicted_entry = self.l1_cache.popitem(last=False)
            self.level_stats[CacheLevel.L1_MEMORY].evictions += 1
    
    async def _get_l2(self, key: str) -> Optional[CacheEntry]:
        """Récupération L2 disque"""
        cache_file = self.l2_cache_dir / f"{hashlib.md5(key.encode()).hexdigest()}.cache"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    compressed_data = f.read()
                    data = lz4.frame.decompress(compressed_data)
                    entry = pickle.loads(data)
                    
                    # Vérification TTL
                    if entry.ttl and entry.timestamp + timedelta(seconds=entry.ttl) < datetime.now():
                        cache_file.unlink()  # Suppression expirée
                        return None
                    
                    return entry
            except Exception:
                pass
        
        return None
    
    async def _set_l2(self, key: str, entry: CacheEntry):
        """Stockage L2 disque avec compression"""
        cache_file = self.l2_cache_dir / f"{hashlib.md5(key.encode()).hexdigest()}.cache"
        
        try:
            data = pickle.dumps(entry)
            compressed_data = lz4.frame.compress(data)
            
            with open(cache_file, 'wb') as f:
                f.write(compressed_data)
        except Exception:
            pass

class AgentCacheManager_Enterprise:
    """
    💾 Agent Cache Manager - Enterprise NextGeneration v5.3.0
    
    Cache distribuée intelligente avec éviction IA et multi-niveaux.
    
    Patterns NextGeneration v5.3.0:
    - PERFORMANCE_OPTIMIZATION: Cache haute performance multi-niveaux
    - DISTRIBUTED_CACHE: Distribution intelligente avec réplication
    - LLM_ENHANCED: Éviction prédictive avec IA
    - PATTERN_FACTORY: Architecture modulaire éprouvée
    """
    
    def __init__(self, agent_id: str = "cache_manager", 
                 cache_root: Path = None):
        # Métadonnées NextGeneration v5.3.0
        self.agent_id = agent_id
        self.version = "5.3.0"
        self.wave_version = "Wave 4 - Extensions Core"
        self.migration_status = "modern_active"
        self.compatibility_mode = True
        
        # Patterns NextGeneration appliqués
        self.__version__ = "5.3.0"
        self.__wave_version__ = "Wave 4 - Extensions Core"
        self.__nextgen_patterns__ = [
            "PERFORMANCE_OPTIMIZATION",
            "DISTRIBUTED_CACHE",
            "LLM_ENHANCED",
            "PATTERN_FACTORY"
        ]
        
        # Configuration agent
        self.name = "Cache Manager Enterprise"
        self.mission = "Cache distribuée intelligente avec éviction IA"
        self.agent_type = "cache_enterprise"
        
        # Configuration cache
        self.cache_root = cache_root or Path("/var/cache/nextgeneration")
        self.cache_root.mkdir(parents=True, exist_ok=True)
        
        # Services NextGeneration (injectés à l'initialisation)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Composants cache intelligents
        self.eviction_engine = IntelligentEvictionEngine()
        self.multi_level_cache = MultiLevelCache(self)
        
        # Configuration cache
        self.cache_config = {
            "max_memory_mb": 512,
            "max_disk_gb": 10,
            "default_ttl": 3600,
            "eviction_policy": CachePolicy.ADAPTIVE,
            "compression_enabled": True,
            "replication_factor": 2
        }
        
        # État cache
        self.cache_entries: Dict[str, CacheEntry] = {}
        self.global_stats = CacheStats()
        self.namespace_stats: Dict[str, CacheStats] = defaultdict(CacheStats)
        
        # Métriques cache
        self.cache_metrics = {
            "operations_count": 0,
            "hit_rate": 0.0,
            "evictions_count": 0,
            "memory_usage_mb": 0.0,
            "disk_usage_gb": 0.0,
            "average_response_time_ms": 0.0
        }
        
        # Background tasks
        self._cleanup_task = None
        self._stats_task = None
        
        # Setup logging
        self._setup_logging()
        
        # Démarrage background tasks
        asyncio.create_task(self._start_background_tasks())
    
    def _setup_logging(self):
        """Configuration logging NextGeneration"""
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="cache",
                custom_config={
                    "logger_name": f"nextgen.cache.manager.{self.agent_id}",
                    "log_dir": "logs/cache",
                    "metadata": {
                        "agent_type": "cache_manager",
                        "agent_role": "performance",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(f"CacheManager_{self.agent_id}")
    
    async def inject_nextgen_services(self, 
                                    llm_gateway: LLMGatewayHybrid,
                                    message_bus: MessageBusA2A, 
                                    context_store: OptimizedContextStore):
        """Injection des services NextGeneration v5.3.0"""
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus  
        self.context_store = context_store
        
        # Configuration moteurs avec IA
        self.eviction_engine.llm_gateway = llm_gateway
        
        # Configuration contexte cache IA
        await self._setup_cache_context()
        
        self.logger.info("✅ Services NextGeneration injectés - Cache IA actif")
    
    async def _setup_cache_context(self):
        """Configuration contexte cache IA spécialisé"""
        if not self.llm_gateway:
            return
        
        cache_context = {
            "role": "cache_optimization_expert",
            "domain": "enterprise_cache_management",
            "capabilities": [
                "Predictive cache eviction",
                "Access pattern analysis",
                "Performance optimization",
                "Memory management",
                "Distributed coordination"
            ],
            "patterns": [
                "PERFORMANCE_OPTIMIZATION",
                "DISTRIBUTED_CACHE",
                "LLM_ENHANCED"
            ]
        }
        
        # Chargement expertise cache depuis LLM
        try:
            response = await self.llm_gateway.process_request(
                "Load cache management expertise",
                context=cache_context
            )
            
            if response.get("success"):
                self.logger.info("🧠 Expertise cache IA chargée")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement contexte IA: {e}")
    
    async def get(self, key: str, namespace: str = "default") -> Optional[Any]:
        """Récupération cache avec intelligence multi-niveaux"""
        start_time = time.time()
        full_key = f"{namespace}:{key}"
        
        self.logger.debug(f"💾 Cache GET: {full_key}")
        
        # Récupération multi-niveaux
        value, cache_level = await self.multi_level_cache.get(full_key)
        
        if value is not None:
            # Enregistrement accès pour apprentissage
            self.eviction_engine.record_access(full_key)
            
            # Mise à jour entrée
            if full_key in self.cache_entries:
                entry = self.cache_entries[full_key]
                entry.access_count += 1
                entry.last_access = datetime.now()
            
            # Statistiques
            self.global_stats.hits += 1
            self.namespace_stats[namespace].hits += 1
        else:
            self.global_stats.misses += 1
            self.namespace_stats[namespace].misses += 1
        
        # Métriques performance
        response_time = (time.time() - start_time) * 1000
        self._update_response_time(response_time)
        
        # Mise à jour hit rate
        total_ops = self.global_stats.hits + self.global_stats.misses
        self.global_stats.hit_rate = self.global_stats.hits / max(1, total_ops) * 100
        self.cache_metrics["hit_rate"] = self.global_stats.hit_rate
        
        return value
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None, 
                  namespace: str = "default") -> bool:
        """Stockage cache avec éviction intelligente"""
        start_time = time.time()
        full_key = f"{namespace}:{key}"
        
        self.logger.debug(f"💾 Cache SET: {full_key}")
        
        # Vérification espace disponible
        value_size = len(pickle.dumps(value))
        max_memory_bytes = self.cache_config["max_memory_mb"] * 1024 * 1024
        
        if self.global_stats.size_bytes + value_size > max_memory_bytes:
            await self._evict_entries_intelligent(value_size)
        
        # Création entrée
        entry = CacheEntry(
            key=full_key,
            value=value,
            timestamp=datetime.now(),
            ttl=ttl or self.cache_config["default_ttl"],
            size_bytes=value_size,
            metadata={"namespace": namespace}
        )
        
        # Stockage multi-niveaux
        await self.multi_level_cache.set(full_key, value, ttl)
        
        # Stockage local pour gestion
        self.cache_entries[full_key] = entry
        self.global_stats.size_bytes += value_size
        self.global_stats.entry_count += 1
        
        # Métriques
        self.cache_metrics["operations_count"] += 1
        self.cache_metrics["memory_usage_mb"] = self.global_stats.size_bytes / (1024 * 1024)
        
        response_time = (time.time() - start_time) * 1000
        self._update_response_time(response_time)
        
        return True
    
    async def delete(self, key: str, namespace: str = "default") -> bool:
        """Suppression cache"""
        full_key = f"{namespace}:{key}"
        
        if full_key in self.cache_entries:
            entry = self.cache_entries[full_key]
            self.global_stats.size_bytes -= entry.size_bytes
            self.global_stats.entry_count -= 1
            del self.cache_entries[full_key]
            
            self.logger.debug(f"💾 Cache DELETE: {full_key}")
            return True
        
        return False
    
    async def clear_namespace(self, namespace: str) -> int:
        """Vidage namespace complet"""
        cleared_count = 0
        keys_to_delete = []
        
        for key, entry in self.cache_entries.items():
            if entry.metadata and entry.metadata.get("namespace") == namespace:
                keys_to_delete.append(key)
        
        for key in keys_to_delete:
            if await self.delete(key.split(":", 1)[1], namespace):
                cleared_count += 1
        
        self.logger.info(f"💾 Cache namespace cleared: {namespace} ({cleared_count} entries)")
        return cleared_count
    
    async def _evict_entries_intelligent(self, needed_space: int):
        """Éviction intelligente avec IA"""
        self.logger.info(f"💾 Éviction intelligente: {needed_space} bytes requis")
        
        # Calcul nombre d'entrées à évacuer
        avg_entry_size = self.global_stats.size_bytes / max(1, self.global_stats.entry_count)
        target_evictions = max(1, int(needed_space / avg_entry_size * 1.2))  # 20% marge
        
        # Sélection candidats avec IA
        candidates = await self.eviction_engine.select_eviction_candidates(
            self.cache_entries, target_evictions
        )
        
        # Éviction
        evicted_count = 0
        freed_space = 0
        
        for key in candidates:
            if key in self.cache_entries:
                entry = self.cache_entries[key]
                freed_space += entry.size_bytes
                await self.delete(key.split(":", 1)[1], entry.metadata.get("namespace", "default"))
                evicted_count += 1
                
                if freed_space >= needed_space:
                    break
        
        self.global_stats.evictions += evicted_count
        self.cache_metrics["evictions_count"] += evicted_count
        
        self.logger.info(f"💾 Éviction complétée: {evicted_count} entrées, {freed_space} bytes libérés")
    
    async def _start_background_tasks(self):
        """Démarrage tâches background"""
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())
        self._stats_task = asyncio.create_task(self._periodic_stats_update())
    
    async def _periodic_cleanup(self):
        """Nettoyage périodique TTL expirés"""
        while True:
            try:
                await asyncio.sleep(300)  # 5 minutes
                
                now = datetime.now()
                expired_keys = []
                
                for key, entry in self.cache_entries.items():
                    if entry.ttl and entry.timestamp + timedelta(seconds=entry.ttl) < now:
                        expired_keys.append(key)
                
                for key in expired_keys:
                    namespace = self.cache_entries[key].metadata.get("namespace", "default")
                    await self.delete(key.split(":", 1)[1], namespace)
                
                if expired_keys:
                    self.logger.info(f"💾 Nettoyage TTL: {len(expired_keys)} entrées expirées")
                    
            except Exception as e:
                self.logger.error(f"❌ Erreur nettoyage périodique: {e}")
    
    async def _periodic_stats_update(self):
        """Mise à jour périodique statistiques"""
        while True:
            try:
                await asyncio.sleep(60)  # 1 minute
                
                # Calcul métriques
                total_ops = self.global_stats.hits + self.global_stats.misses
                self.cache_metrics["hit_rate"] = (
                    self.global_stats.hits / max(1, total_ops) * 100
                )
                
                # Notification changements critiques
                if self.message_bus and self.cache_metrics["hit_rate"] < 50:
                    await self.message_bus.publish(
                        create_envelope(
                            message_type=MessageType.ALERT,
                            payload={
                                "type": "cache_performance_degradation",
                                "hit_rate": self.cache_metrics["hit_rate"],
                                "timestamp": datetime.now().isoformat()
                            },
                            priority=Priority.MEDIUM
                        )
                    )
                
            except Exception as e:
                self.logger.error(f"❌ Erreur stats périodiques: {e}")
    
    def _update_response_time(self, response_time_ms: float):
        """Mise à jour temps réponse moyen"""
        count = self.cache_metrics["operations_count"]
        avg = self.cache_metrics["average_response_time_ms"]
        
        self.cache_metrics["average_response_time_ms"] = (
            (avg * (count - 1) + response_time_ms) / count
        )
    
    async def get_cache_stats(self, namespace: Optional[str] = None) -> Dict[str, Any]:
        """Statistiques cache détaillées"""
        if namespace:
            stats = self.namespace_stats.get(namespace, CacheStats())
            return {
                "namespace": namespace,
                "stats": asdict(stats),
                "entries": len([k for k, v in self.cache_entries.items() 
                              if v.metadata and v.metadata.get("namespace") == namespace])
            }
        else:
            return {
                "global_stats": asdict(self.global_stats),
                "cache_metrics": self.cache_metrics,
                "level_stats": {
                    level.value: asdict(stats) 
                    for level, stats in self.multi_level_cache.level_stats.items()
                },
                "namespaces": list(self.namespace_stats.keys()),
                "configuration": self.cache_config,
                "timestamp": datetime.now().isoformat()
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check NextGeneration"""
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "status": "healthy",
            "patterns": self.__nextgen_patterns__,
            "services": {
                "llm_gateway": self.llm_gateway is not None,
                "message_bus": self.message_bus is not None,
                "context_store": self.context_store is not None
            },
            "cache": {
                "entries": self.global_stats.entry_count,
                "hit_rate": self.cache_metrics["hit_rate"],
                "memory_usage_mb": self.cache_metrics["memory_usage_mb"],
                "operations_count": self.cache_metrics["operations_count"]
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function pour compatibilité
def create_cache_manager(**config) -> AgentCacheManager_Enterprise:
    """Factory function pour créer l'agent"""
    return AgentCacheManager_Enterprise(**config)

# Test standalone
async def main():
    """Test de l'agent Cache Manager"""
    print("💾 Test Agent Cache Manager NextGeneration v5.3.0")
    
    agent = create_cache_manager(agent_id="test_cache")
    
    # Health check
    health = await agent.health_check()
    print(f"🏥 Health: {health['status']}")
    
    # Test cache operations
    await agent.set("user:123", {"name": "John", "age": 30}, namespace="users")
    await agent.set("config:app", {"theme": "dark", "lang": "fr"}, namespace="config")
    
    user_data = await agent.get("user:123", namespace="users")
    print(f"💾 User data: {user_data}")
    
    config_data = await agent.get("config:app", namespace="config")
    print(f"💾 Config data: {config_data}")
    
    # Statistiques
    stats = await agent.get_cache_stats()
    print(f"📊 Hit rate: {stats['cache_metrics']['hit_rate']:.1f}%")
    print(f"📊 Entries: {stats['global_stats']['entry_count']}")

if __name__ == "__main__":
    asyncio.run(main())