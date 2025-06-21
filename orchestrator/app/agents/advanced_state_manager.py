"""
Advanced State Manager for LangGraph
Optimized state persistence, compression, and efficient transitions.
"""

import asyncio
import json
from logging_manager_optimized import LoggingManager
import pickle
import zlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple, Type
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
from collections import defaultdict

from langgraph.graph import StateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver

from ..config import settings
from ..observability.monitoring import get_monitoring
from ..security.logging import security_logger
from ..performance.redis_cache import get_cache, CacheType


# LoggingManager NextGeneration - Agent
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="StateCompressionType",
            role="ai_processor",
            domain="orchestration",
            async_enabled=True
        )


class StateCompressionType(Enum):
    """State compression types"""
    NONE = "none"
    ZLIB = "zlib"
    PICKLE = "pickle"
    JSON_OPTIMIZED = "json_optimized"


class StatePersistenceLevel(Enum):
    """State persistence levels"""
    MEMORY_ONLY = "memory"
    CACHE_PERSISTED = "cache"
    DATABASE_PERSISTED = "database"
    DISTRIBUTED = "distributed"


@dataclass
class StateMetrics:
    """State management metrics"""
    total_states: int
    active_states: int
    compressed_states: int
    compression_ratio: float
    avg_state_size_kb: float
    max_state_size_kb: float
    state_transitions_per_second: float
    cache_hit_rate: float
    persistence_latency_ms: float
    memory_usage_mb: float
    timestamp: datetime


@dataclass
class StateTransition:
    """State transition record"""
    from_state: str
    to_state: str
    transition_time: datetime
    agent_id: str
    session_id: str
    data_size_kb: float
    compression_used: bool
    latency_ms: float


class StateCompression:
    """Advanced state compression system"""
    
    def __init__(self):
        self.compression_threshold = 1024  # 1KB
        self.compression_level = 6  # zlib compression level
        self.compression_stats = defaultdict(int)
        
    def compress_state(self, state: Dict[str, Any], compression_type: StateCompressionType = StateCompressionType.ZLIB) -> Tuple[bytes, Dict[str, Any]]:
        """Compress state data"""
        try:
            # Convert to JSON first for consistency
            state_json = json.dumps(state, default=str, sort_keys=True)
            original_size = len(state_json.encode('utf-8'))
            
            metadata = {
                "compression_type": compression_type.value,
                "original_size": original_size,
                "compressed": False
            }
            
            # Only compress if above threshold
            if original_size < self.compression_threshold:
                metadata["compressed_data"] = state_json.encode('utf-8')
                return state_json.encode('utf-8'), metadata
            
            if compression_type == StateCompressionType.ZLIB:
                compressed_data = zlib.compress(state_json.encode('utf-8'), self.compression_level)
            elif compression_type == StateCompressionType.PICKLE:
                compressed_data = pickle.dumps(state)
            elif compression_type == StateCompressionType.JSON_OPTIMIZED:
                # Remove None values and optimize structure
                optimized_state = self._optimize_json_structure(state)
                state_json = json.dumps(optimized_state, default=str, sort_keys=True, separators=(',', ':'))
                compressed_data = zlib.compress(state_json.encode('utf-8'), self.compression_level)
            else:
                compressed_data = state_json.encode('utf-8')
            
            compressed_size = len(compressed_data)
            compression_ratio = (original_size - compressed_size) / original_size if original_size > 0 else 0
            
            metadata.update({
                "compressed": True,
                "compressed_size": compressed_size,
                "compression_ratio": compression_ratio
            })
            
            self.compression_stats["total_compressions"] += 1
            self.compression_stats["total_saved_bytes"] += (original_size - compressed_size)
            
            return compressed_data, metadata
            
        except Exception as e:
            logger.error(f"Error compressing state: {e}")
            # Fallback to uncompressed
            return json.dumps(state, default=str).encode('utf-8'), {"compression_type": "none", "error": str(e)}
    
    def decompress_state(self, compressed_data: bytes, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Decompress state data"""
        try:
            compression_type = metadata.get("compression_type", "none")
            
            if not metadata.get("compressed", False):
                if isinstance(compressed_data, bytes):
                    return json.loads(compressed_data.decode('utf-8'))
                return compressed_data
            
            if compression_type == "zlib" or compression_type == "json_optimized":
                decompressed_data = zlib.decompress(compressed_data)
                return json.loads(decompressed_data.decode('utf-8'))
            elif compression_type == "pickle":
                return pickle.loads(compressed_data)
            else:
                return json.loads(compressed_data.decode('utf-8'))
                
        except Exception as e:
            logger.error(f"Error decompressing state: {e}")
            return {}
    
    def _optimize_json_structure(self, data: Any) -> Any:
        """Optimize JSON structure for better compression"""
        if isinstance(data, dict):
            # Remove None values and empty structures
            optimized = {}
            for key, value in data.items():
                if value is not None and value != {} and value != []:
                    optimized_value = self._optimize_json_structure(value)
                    if optimized_value is not None and optimized_value != {} and optimized_value != []:
                        optimized[key] = optimized_value
            return optimized
        elif isinstance(data, list):
            return [self._optimize_json_structure(item) for item in data if item is not None]
        else:
            return data
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """Get compression statistics"""
        return dict(self.compression_stats)


class StateCache:
    """High-performance state caching with TTL and LRU"""
    
    def __init__(self, max_size: int = 10000, default_ttl: int = 3600):
        self.cache = {}
        self.access_times = {}
        self.creation_times = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.hit_count = 0
        self.miss_count = 0
        
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get state from cache"""
        current_time = datetime.utcnow()
        
        if key in self.cache:
            # Check TTL
            creation_time = self.creation_times.get(key, current_time)
            if (current_time - creation_time).total_seconds() > self.default_ttl:
                await self.remove(key)
                self.miss_count += 1
                return None
            
            # Update access time for LRU
            self.access_times[key] = current_time
            self.hit_count += 1
            return self.cache[key]
        
        self.miss_count += 1
        return None
    
    async def set(self, key: str, value: Dict[str, Any], ttl: Optional[int] = None):
        """Set state in cache"""
        current_time = datetime.utcnow()
        
        # Check if we need to evict
        if len(self.cache) >= self.max_size:
            await self._evict_lru()
        
        self.cache[key] = value
        self.access_times[key] = current_time
        self.creation_times[key] = current_time
    
    async def remove(self, key: str):
        """Remove state from cache"""
        if key in self.cache:
            del self.cache[key]
            self.access_times.pop(key, None)
            self.creation_times.pop(key, None)
    
    async def _evict_lru(self):
        """Evict least recently used item"""
        if not self.access_times:
            return
        
        oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        await self.remove(oldest_key)
    
    def get_hit_rate(self) -> float:
        """Get cache hit rate"""
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": self.get_hit_rate()
        }


class AdvancedStateManager:
    """Advanced state management for LangGraph with optimization"""
    
    def __init__(self):
        self.compression = StateCompression()
        self.state_cache = StateCache()
        self.state_transitions: List[StateTransition] = []
        self.active_states: Dict[str, Dict[str, Any]] = {}
        self.state_metadata: Dict[str, Dict[str, Any]] = {}
        self.persistence_level = StatePersistenceLevel.CACHE_PERSISTED
        
        # Performance tracking
        self.metrics_history: List[StateMetrics] = []
        self.transition_count = 0
        self.last_metrics_collection = datetime.utcnow()
        
        # Configuration
        self.state_cleanup_interval = 300  # 5 minutes
        self.max_state_age = 3600  # 1 hour
        self.state_size_limit = 10 * 1024 * 1024  # 10MB per state
        
    async def initialize(self):
        """Initialize state manager"""
        try:
            # Start cleanup task
            asyncio.create_task(self._cleanup_loop())
            asyncio.create_task(self._metrics_collection_loop())
            
            logger.info("Advanced state manager initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize state manager: {e}")
            raise
    
    async def store_state(self, session_id: str, agent_id: str, state: Dict[str, Any], 
                         compression_type: StateCompressionType = StateCompressionType.ZLIB) -> str:
        """Store state with compression and caching"""
        try:
            start_time = datetime.utcnow()
            state_key = f"{session_id}:{agent_id}:{start_time.timestamp()}"
            
            # Validate state size
            state_size = len(json.dumps(state, default=str).encode('utf-8'))
            if state_size > self.state_size_limit:
                raise ValueError(f"State too large: {state_size} bytes (limit: {self.state_size_limit})")
            
            # Compress state
            compressed_data, compression_metadata = self.compression.compress_state(state, compression_type)
            
            # Store in cache
            cache_data = {
                "compressed_data": compressed_data,
                "metadata": compression_metadata,
                "session_id": session_id,
                "agent_id": agent_id,
                "created_at": start_time,
                "size_kb": len(compressed_data) / 1024
            }
            
            await self.state_cache.set(state_key, cache_data)
              # Store in Redis if configured
            if self.persistence_level in [StatePersistenceLevel.CACHE_PERSISTED, StatePersistenceLevel.DISTRIBUTED]:
                cache_manager = await get_cache()
                await cache_manager.set(f"state:{state_key}", cache_data, CacheType.AGENT_STATE)
            
            # Update metadata
            self.state_metadata[state_key] = {
                "session_id": session_id,
                "agent_id": agent_id,
                "created_at": start_time,
                "last_accessed": start_time,
                "access_count": 1,
                "compression_type": compression_type.value,
                "original_size": compression_metadata.get("original_size", 0),
                "compressed_size": len(compressed_data)
            }
            
            # Track active state
            self.active_states[state_key] = state
            
            # Record metrics
            latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            await get_monitoring().record_metric("state_store_latency_ms", latency_ms)
            await get_monitoring().record_metric("state_size_kb", len(compressed_data) / 1024)
            
            security_logger.log_security_event("STATE_STORED", {
                "session_id": session_id,
                "agent_id": agent_id,
                "state_key": state_key,
                "size_kb": len(compressed_data) / 1024
            })
            
            return state_key
            
        except Exception as e:
            logger.error(f"Error storing state: {e}")
            raise
    
    async def retrieve_state(self, state_key: str) -> Optional[Dict[str, Any]]:
        """Retrieve and decompress state"""
        try:
            start_time = datetime.utcnow()
            
            # Try cache first
            cache_data = await self.state_cache.get(state_key)
            
            if not cache_data:
                # Try Redis
                if self.persistence_level in [StatePersistenceLevel.CACHE_PERSISTED, StatePersistenceLevel.DISTRIBUTED]:
                    cache_manager = await get_cache()
                    cache_data = await cache_manager.get(f"state:{state_key}", CacheType.AGENT_STATE)
                
                if cache_data:
                    # Store back in local cache
                    await self.state_cache.set(state_key, cache_data)
            
            if not cache_data:
                return None
            
            # Decompress state
            compressed_data = cache_data["compressed_data"]
            metadata = cache_data["metadata"]
            
            state = self.compression.decompress_state(compressed_data, metadata)
            
            # Update metadata
            if state_key in self.state_metadata:
                self.state_metadata[state_key]["last_accessed"] = datetime.utcnow()
                self.state_metadata[state_key]["access_count"] += 1
            
            # Record metrics
            latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            await get_monitoring().record_metric("state_retrieve_latency_ms", latency_ms)
            
            return state
            
        except Exception as e:
            logger.error(f"Error retrieving state: {e}")
            return None
    
    async def transition_state(self, session_id: str, agent_id: str, from_state_key: str, 
                              new_state: Dict[str, Any]) -> str:
        """Handle state transition with optimization"""
        try:
            start_time = datetime.utcnow()
            
            # Store new state
            new_state_key = await self.store_state(session_id, agent_id, new_state)
            
            # Record transition
            transition = StateTransition(
                from_state=from_state_key,
                to_state=new_state_key,
                transition_time=start_time,
                agent_id=agent_id,
                session_id=session_id,
                data_size_kb=len(json.dumps(new_state, default=str).encode('utf-8')) / 1024,
                compression_used=True,
                latency_ms=(datetime.utcnow() - start_time).total_seconds() * 1000
            )
            
            self.state_transitions.append(transition)
            self.transition_count += 1
            
            # Keep only last 1000 transitions
            if len(self.state_transitions) > 1000:
                self.state_transitions = self.state_transitions[-1000:]
            
            # Record metrics
            await get_monitoring().record_metric("state_transitions_total", self.transition_count)
            
            return new_state_key
            
        except Exception as e:
            logger.error(f"Error in state transition: {e}")
            raise
    
    async def cleanup_expired_states(self):
        """Clean up expired states"""
        try:
            current_time = datetime.utcnow()
            expired_keys = []
            
            for state_key, metadata in self.state_metadata.items():
                created_at = metadata["created_at"]
                if (current_time - created_at).total_seconds() > self.max_state_age:
                    expired_keys.append(state_key)
            
            for state_key in expired_keys:
                await self._remove_state(state_key)
            
            if expired_keys:
                logger.info(f"Cleaned up {len(expired_keys)} expired states")
                
        except Exception as e:
            logger.error(f"Error cleaning up states: {e}")
    
    async def _remove_state(self, state_key: str):
        """Remove state from all storage levels"""
        try:
            # Remove from cache
            await self.state_cache.remove(state_key)
            
            # Remove from Redis
            if self.persistence_level in [StatePersistenceLevel.CACHE_PERSISTED, StatePersistenceLevel.DISTRIBUTED]:
                cache_manager = await get_cache()
                await cache_manager.delete(f"state:{state_key}")
            
            # Remove from memory
            self.active_states.pop(state_key, None)
            self.state_metadata.pop(state_key, None)
            
        except Exception as e:
            logger.error(f"Error removing state {state_key}: {e}")
    
    async def _cleanup_loop(self):
        """Periodic cleanup loop"""
        while True:
            try:
                await self.cleanup_expired_states()
                await asyncio.sleep(self.state_cleanup_interval)
                
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(60)
    
    async def _metrics_collection_loop(self):
        """Periodic metrics collection"""
        while True:
            try:
                await self._collect_metrics()
                await asyncio.sleep(60)  # Collect every minute
                
            except Exception as e:
                logger.error(f"Error in metrics collection: {e}")
                await asyncio.sleep(60)
    
    async def _collect_metrics(self):
        """Collect state management metrics"""
        try:
            current_time = datetime.utcnow()
            
            # Calculate states metrics
            total_states = len(self.state_metadata)
            active_states = len(self.active_states)
            
            # Calculate compression stats
            compression_stats = self.compression.get_compression_stats()
            compressed_states = compression_stats.get("total_compressions", 0)
            
            # Calculate sizes
            total_size = sum(metadata.get("compressed_size", 0) for metadata in self.state_metadata.values())
            avg_size_kb = (total_size / total_states / 1024) if total_states > 0 else 0
            max_size_kb = max((metadata.get("compressed_size", 0) for metadata in self.state_metadata.values()), default=0) / 1024
            
            # Calculate transition rate
            time_diff = (current_time - self.last_metrics_collection).total_seconds()
            transitions_per_second = self.transition_count / time_diff if time_diff > 0 else 0
            self.transition_count = 0  # Reset counter
            
            # Cache stats
            cache_stats = self.state_cache.get_stats()
            
            metrics = StateMetrics(
                total_states=total_states,
                active_states=active_states,
                compressed_states=compressed_states,
                compression_ratio=compression_stats.get("compression_ratio", 0),
                avg_state_size_kb=avg_size_kb,
                max_state_size_kb=max_size_kb,
                state_transitions_per_second=transitions_per_second,
                cache_hit_rate=cache_stats["hit_rate"],
                persistence_latency_ms=0,  # Would need to track
                memory_usage_mb=total_size / 1024 / 1024,
                timestamp=current_time
            )
            
            self.metrics_history.append(metrics)
            
            # Keep only last 100 metrics
            if len(self.metrics_history) > 100:
                self.metrics_history.pop(0)
            
            self.last_metrics_collection = current_time
            
            # Send to monitoring
            await get_monitoring().record_metric("state_total_states", total_states)
            await get_monitoring().record_metric("state_active_states", active_states)
            await get_monitoring().record_metric("state_memory_usage_mb", metrics.memory_usage_mb)
            await get_monitoring().record_metric("state_cache_hit_rate", cache_stats["hit_rate"])
            
        except Exception as e:
            logger.error(f"Error collecting state metrics: {e}")
    
    def get_state_metrics(self) -> Dict[str, Any]:
        """Get current state metrics"""
        if not self.metrics_history:
            return {"error": "No metrics available"}
        
        current_metrics = self.metrics_history[-1]
        cache_stats = self.state_cache.get_stats()
        compression_stats = self.compression.get_compression_stats()
        
        return {
            "current": asdict(current_metrics),
            "cache": cache_stats,
            "compression": compression_stats,
            "recent_transitions": [
                {
                    "from_state": t.from_state,
                    "to_state": t.to_state,
                    "agent_id": t.agent_id,
                    "latency_ms": t.latency_ms,
                    "data_size_kb": t.data_size_kb
                } for t in self.state_transitions[-10:]
            ]
        }
    
    async def optimize_states(self) -> Dict[str, Any]:
        """Optimize state storage and performance"""
        try:
            start_time = datetime.utcnow()
            
            # Clean expired states
            await self.cleanup_expired_states()
            
            # Optimize compression for large states
            optimized_count = 0
            for state_key, metadata in self.state_metadata.items():
                if metadata.get("compressed_size", 0) > 100 * 1024:  # > 100KB
                    # Try better compression
                    state = await self.retrieve_state(state_key)
                    if state:
                        # Re-compress with JSON optimization
                        new_key = await self.store_state(
                            metadata["session_id"],
                            metadata["agent_id"],
                            state,
                            StateCompressionType.JSON_OPTIMIZED
                        )
                        await self._remove_state(state_key)
                        optimized_count += 1
            
            optimization_time = (datetime.utcnow() - start_time).total_seconds()
            
            result = {
                "status": "completed",
                "optimization_time": optimization_time,
                "states_optimized": optimized_count,
                "timestamp": datetime.utcnow(),
                "metrics": self.get_state_metrics()
            }
            
            logger.info(f"State optimization completed: {optimized_count} states optimized in {optimization_time:.3f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error optimizing states: {e}")
            return {"error": str(e)}
    
    async def close(self):
        """Close state manager"""
        logger.info("Advanced state manager closed")


# Global instance
advanced_state_manager = AdvancedStateManager()


def get_advanced_state_manager():
    """Get advanced state manager instance"""
    return advanced_state_manager
