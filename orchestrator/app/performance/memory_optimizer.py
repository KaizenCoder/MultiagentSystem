"""
Advanced Memory Management and Optimization
Handles memory leak detection, garbage collection optimization, and intelligent cleanup.
"""

import asyncio
import gc
import logging
import psutil
import sys
import time
import tracemalloc
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
from weakref import WeakSet

from ..config import settings
from ..observability.monitoring import get_monitoring
from ..security.logging import security_logger


logger = logging.getLogger(__name__)


@dataclass
class MemoryMetrics:
    """Memory performance metrics"""
    total_memory_mb: float
    available_memory_mb: float
    memory_usage_percent: float
    gc_collections: Dict[int, int]
    gc_objects: int
    memory_leaks_detected: int
    peak_memory_mb: float
    memory_growth_rate: float
    active_sessions: int
    cached_objects: int
    timestamp: datetime


@dataclass
class GCStats:
    """Garbage Collection statistics"""
    generation: int
    collections: int
    collected: int
    uncollectable: int
    time_spent: float


class MemoryLeakDetector:
    """Advanced memory leak detection system"""
    
    def __init__(self):
        self.baseline_snapshot = None
        self.previous_snapshots: List[Any] = []
        self.leak_threshold = 1024 * 1024  # 1MB growth
        self.monitoring_active = False
        self.suspicious_objects: Set[str] = set()
        
    def start_monitoring(self):
        """Start memory leak monitoring"""
        if not tracemalloc.is_tracing():
            tracemalloc.start(25)  # Keep 25 frames
            self.monitoring_active = True
            self.baseline_snapshot = tracemalloc.take_snapshot()
            logger.info("Memory leak monitoring started")
    
    def stop_monitoring(self):
        """Stop memory leak monitoring"""
        if tracemalloc.is_tracing():
            tracemalloc.stop()
            self.monitoring_active = False
            logger.info("Memory leak monitoring stopped")
    
    def take_snapshot(self) -> Optional[Any]:
        """Take memory snapshot for analysis"""
        if not self.monitoring_active:
            return None
        
        try:
            snapshot = tracemalloc.take_snapshot()
            self.previous_snapshots.append(snapshot)
            
            # Keep only last 10 snapshots
            if len(self.previous_snapshots) > 10:
                self.previous_snapshots.pop(0)
            
            return snapshot
            
        except Exception as e:
            logger.error(f"Error taking memory snapshot: {e}")
            return None
    
    def detect_leaks(self) -> List[Dict[str, Any]]:
        """Detect potential memory leaks"""
        if not self.baseline_snapshot or not self.previous_snapshots:
            return []
        
        try:
            current_snapshot = self.previous_snapshots[-1]
            top_stats = current_snapshot.compare_to(self.baseline_snapshot, 'lineno')
            
            leaks = []
            for stat in top_stats[:10]:  # Top 10 differences
                if stat.size_diff > self.leak_threshold:
                    leak_info = {
                        "filename": stat.traceback.format()[0].split(":")[0] if stat.traceback else "unknown",
                        "line_number": stat.traceback.format()[0].split(":")[1] if stat.traceback else 0,
                        "size_diff_mb": stat.size_diff / 1024 / 1024,
                        "count_diff": stat.count_diff,
                        "traceback": stat.traceback.format() if stat.traceback else []
                    }
                    leaks.append(leak_info)
                    
                    # Mark as suspicious
                    self.suspicious_objects.add(leak_info["filename"])
            
            return leaks
            
        except Exception as e:
            logger.error(f"Error detecting memory leaks: {e}")
            return []


class SessionMemoryManager:
    """Manages memory for user sessions with intelligent cleanup"""
    
    def __init__(self):
        self.active_sessions: Dict[str, Dict] = {}
        self.session_memory_usage: Dict[str, int] = {}
        self.session_last_access: Dict[str, datetime] = {}
        self.cleanup_interval = 300  # 5 minutes
        self.session_timeout = 3600  # 1 hour
        self.memory_limit_per_session = 50 * 1024 * 1024  # 50MB
        
    def register_session(self, session_id: str, initial_data: Optional[Dict] = None):
        """Register new session"""
        self.active_sessions[session_id] = initial_data or {}
        self.session_memory_usage[session_id] = sys.getsizeof(initial_data or {})
        self.session_last_access[session_id] = datetime.utcnow()
        
        security_logger.log_security_event("SESSION_REGISTERED", {
            "session_id": session_id,
            "memory_usage": self.session_memory_usage[session_id]
        })
    
    def update_session_memory(self, session_id: str, data: Any):
        """Update session memory usage"""
        if session_id not in self.active_sessions:
            return
        
        new_size = sys.getsizeof(data)
        self.session_memory_usage[session_id] = new_size
        self.session_last_access[session_id] = datetime.utcnow()
        
        # Check memory limit
        if new_size > self.memory_limit_per_session:
            logger.warning(f"Session {session_id} exceeded memory limit: {new_size / 1024 / 1024:.2f}MB")
            self._cleanup_session_data(session_id)
    
    def _cleanup_session_data(self, session_id: str):
        """Cleanup session data to reduce memory usage"""
        if session_id not in self.active_sessions:
            return
        
        session_data = self.active_sessions[session_id]
        
        # Remove old entries (keep only last 100 items)
        if isinstance(session_data, dict):
            items = list(session_data.items())
            if len(items) > 100:
                # Keep most recent items
                session_data.clear()
                session_data.update(dict(items[-100:]))
                
        self.session_memory_usage[session_id] = sys.getsizeof(session_data)
        logger.info(f"Cleaned up session {session_id}, new size: {self.session_memory_usage[session_id]}")
    
    async def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.utcnow()
        expired_sessions = []
        
        for session_id, last_access in self.session_last_access.items():
            if (current_time - last_access).total_seconds() > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.remove_session(session_id)
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
    
    def remove_session(self, session_id: str):
        """Remove session completely"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            del self.session_memory_usage[session_id]
            del self.session_last_access[session_id]
            
            security_logger.log_security_event("SESSION_REMOVED", {
                "session_id": session_id
            })
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get session memory statistics"""
        total_memory = sum(self.session_memory_usage.values())
        return {
            "active_sessions": len(self.active_sessions),
            "total_memory_mb": total_memory / 1024 / 1024,
            "average_memory_per_session_mb": (total_memory / len(self.active_sessions)) / 1024 / 1024 if self.active_sessions else 0,
            "max_memory_session_mb": (max(self.session_memory_usage.values()) if self.session_memory_usage else 0) / 1024 / 1024
        }


class AdvancedMemoryManager:
    """Advanced memory management with leak detection and optimization"""
    
    def __init__(self):
        self.leak_detector = MemoryLeakDetector()
        self.session_manager = SessionMemoryManager()
        self.gc_stats_history: List[GCStats] = []
        self.memory_history: List[MemoryMetrics] = []
        self.monitoring_interval = 30  # seconds
        self.optimization_enabled = True
        self.last_optimization = datetime.utcnow()
        
        # GC optimization thresholds
        self.gc_thresholds = {
            0: (700, 10, 10),  # Generation 0
            1: (10, 10, 10),   # Generation 1  
            2: (10, 10, 10)    # Generation 2
        }
        
    async def initialize(self):
        """Initialize memory management"""
        try:
            # Set optimized GC thresholds
            gc.set_threshold(*self.gc_thresholds[0])
            
            # Start leak detection
            self.leak_detector.start_monitoring()
            
            # Start monitoring task
            asyncio.create_task(self._monitoring_loop())
            
            logger.info("Advanced memory manager initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize memory manager: {e}")
            raise
    
    async def _monitoring_loop(self):
        """Continuous memory monitoring"""
        while True:
            try:
                await self._collect_metrics()
                await self._detect_and_handle_leaks()
                await self.session_manager.cleanup_expired_sessions()
                
                # Optimize GC if needed
                if self.optimization_enabled:
                    await self._optimize_gc()
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error in memory monitoring loop: {e}")
                await asyncio.sleep(60)  # Retry after 1 minute
    
    async def _collect_metrics(self):
        """Collect current memory metrics"""
        try:
            # System memory
            memory = psutil.virtual_memory()
            
            # GC stats
            gc_stats = {}
            for i in range(3):
                stats = gc.get_stats()[i] if i < len(gc.get_stats()) else {}
                gc_stats[i] = stats.get('collections', 0)
            
            # Take memory snapshot
            self.leak_detector.take_snapshot()
            
            # Build metrics
            metrics = MemoryMetrics(
                total_memory_mb=memory.total / 1024 / 1024,
                available_memory_mb=memory.available / 1024 / 1024,
                memory_usage_percent=memory.percent,
                gc_collections=gc_stats,
                gc_objects=len(gc.get_objects()),
                memory_leaks_detected=len(self.leak_detector.suspicious_objects),
                peak_memory_mb=memory.total / 1024 / 1024,  # Would need tracking
                memory_growth_rate=0.0,  # Calculate from history
                active_sessions=len(self.session_manager.active_sessions),
                cached_objects=0,  # Would integrate with cache manager
                timestamp=datetime.utcnow()
            )
            
            # Calculate growth rate
            if len(self.memory_history) > 1:
                prev_metrics = self.memory_history[-1]
                time_diff = (metrics.timestamp - prev_metrics.timestamp).total_seconds()
                memory_diff = metrics.memory_usage_percent - prev_metrics.memory_usage_percent
                metrics.memory_growth_rate = memory_diff / time_diff if time_diff > 0 else 0
            
            self.memory_history.append(metrics)
            
            # Keep only last 100 metrics
            if len(self.memory_history) > 100:
                self.memory_history.pop(0)
              # Send to monitoring
            monitoring = get_monitoring()
            await monitoring.record_metric("memory_usage_percent", metrics.memory_usage_percent)
            await monitoring.record_metric("active_sessions", metrics.active_sessions)
            await monitoring.record_metric("gc_objects", metrics.gc_objects)
            
        except Exception as e:
            logger.error(f"Error collecting memory metrics: {e}")
    
    async def _detect_and_handle_leaks(self):
        """Detect and handle memory leaks"""
        leaks = self.leak_detector.detect_leaks()
        
        if leaks:
            logger.warning(f"Detected {len(leaks)} potential memory leaks")
            
            for leak in leaks:
                security_logger.log_security_event("MEMORY_LEAK_DETECTED", {
                    "filename": leak["filename"],
                    "size_diff_mb": leak["size_diff_mb"],
                    "count_diff": leak["count_diff"]
                })
            
            # Trigger aggressive cleanup
            await self._aggressive_cleanup()
    
    async def _optimize_gc(self):
        """Optimize garbage collection"""
        try:
            # Check if optimization is needed
            current_time = datetime.utcnow()
            if (current_time - self.last_optimization).total_seconds() < 300:  # 5 minutes
                return
            
            # Get current GC stats
            before_objects = len(gc.get_objects())
            before_stats = gc.get_stats()
            
            # Force collection with optimized timing
            start_time = time.time()
            collected = gc.collect()
            gc_time = time.time() - start_time
            
            after_objects = len(gc.get_objects())
            
            # Record GC stats
            for i, gen_stats in enumerate(gc.get_stats()):
                gc_stat = GCStats(
                    generation=i,
                    collections=gen_stats.get('collections', 0),
                    collected=gen_stats.get('collected', 0),
                    uncollectable=gen_stats.get('uncollectable', 0),
                    time_spent=gc_time
                )
                self.gc_stats_history.append(gc_stat)
            
            # Keep only last 50 GC stats
            if len(self.gc_stats_history) > 50:
                self.gc_stats_history = self.gc_stats_history[-50:]
            
            self.last_optimization = current_time
            
            logger.info(f"GC optimization: collected {collected} objects, "
                       f"objects {before_objects} -> {after_objects}, "
                       f"time: {gc_time:.3f}s")
              # Send metrics
            monitoring = get_monitoring()
            await monitoring.record_metric("gc_collections_total", collected)
            await monitoring.record_metric("gc_time_seconds", gc_time)
            await monitoring.record_metric("gc_objects_collected", before_objects - after_objects)
            
        except Exception as e:
            logger.error(f"Error optimizing GC: {e}")
    
    async def _aggressive_cleanup(self):
        """Aggressive cleanup when leaks detected"""
        try:
            logger.info("Starting aggressive memory cleanup")
            
            # Clean session data
            for session_id in list(self.session_manager.active_sessions.keys()):
                self.session_manager._cleanup_session_data(session_id)
            
            # Force multiple GC cycles
            for _ in range(3):
                gc.collect()
                await asyncio.sleep(0.1)
            
            # Clear some caches (would integrate with cache manager)
            # This would be implemented based on the cache system
            
            logger.info("Aggressive cleanup completed")
            
        except Exception as e:
            logger.error(f"Error in aggressive cleanup: {e}")
    
    def get_memory_metrics(self) -> Dict[str, Any]:
        """Get current memory metrics"""
        if not self.memory_history:
            return {"error": "No metrics available"}
        
        current_metrics = self.memory_history[-1]
        session_stats = self.session_manager.get_memory_stats()
        
        return {
            "system": asdict(current_metrics),
            "sessions": session_stats,
            "gc_history": [asdict(stat) for stat in self.gc_stats_history[-10:]],
            "suspicious_objects": list(self.leak_detector.suspicious_objects),
            "monitoring_active": self.leak_detector.monitoring_active
        }
    
    async def force_optimization(self) -> Dict[str, Any]:
        """Force memory optimization"""
        try:
            start_time = time.time()
            
            # Force GC
            await self._optimize_gc()
            
            # Clean sessions
            await self.session_manager.cleanup_expired_sessions()
            
            # Take snapshot
            self.leak_detector.take_snapshot()
            
            optimization_time = time.time() - start_time
            
            result = {
                "status": "completed",
                "optimization_time": optimization_time,
                "timestamp": datetime.utcnow(),
                "metrics": self.get_memory_metrics()
            }
            
            logger.info(f"Forced optimization completed in {optimization_time:.3f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error in forced optimization: {e}")
            return {"error": str(e)}
    
    async def register_session(self, session_id: str, initial_data: Optional[Dict] = None):
        """Register new session"""
        self.session_manager.register_session(session_id, initial_data)
    
    async def update_session_memory(self, session_id: str, data: Any):
        """Update session memory usage"""
        self.session_manager.update_session_memory(session_id, data)
    
    async def remove_session(self, session_id: str):
        """Remove session"""
        self.session_manager.remove_session(session_id)
    
    async def close(self):
        """Close memory manager"""
        self.leak_detector.stop_monitoring()
        logger.info("Memory manager closed")


# Global instance
memory_optimizer = AdvancedMemoryManager()


def get_memory_optimizer():
    """Get memory optimizer instance"""
    return memory_optimizer
