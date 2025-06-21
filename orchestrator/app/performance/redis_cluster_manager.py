"""
Advanced Redis Cluster Manager for Production
Handles Redis clustering, cache warming, eviction policies, and cluster monitoring.
"""

import asyncio
import json
import sys
from pathlib import Path
from core import logging_manager
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

import redis
import redis.asyncio as aioredis
from redis.cluster import RedisCluster
from redis.asyncio.cluster import RedisCluster as AsyncRedisCluster

from ..config import config
from ..observability.monitoring import monitoring_manager


# LoggingManager NextGeneration - Tool/Utility
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = logging_manager.get_logger(custom_config={
            "logger_name": "CacheStrategy",
            "log_level": "INFO",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": True
        })


class CacheStrategy(Enum):
    """Cache strategies"""
    LRU = "lru"
    LFU = "lfu"
    TTL = "ttl"
    RANDOM = "random"


class CacheLayer(Enum):
    """Cache layer types"""
    L1_MEMORY = "l1_memory"
    L2_REDIS = "l2_redis"
    L3_PERSISTENT = "l3_persistent"


@dataclass
class ClusterNode:
    """Redis cluster node configuration"""
    host: str
    port: int
    role: str  # master, slave
    node_id: str
    slots_range: Optional[Tuple[int, int]] = None
    max_memory: str = "1gb"
    eviction_policy: str = "allkeys-lru"


@dataclass
class CacheMetrics:
    """Cache performance metrics"""
    hit_ratio: float
    miss_ratio: float
    eviction_count: int
    memory_usage: int
    memory_peak: int
    connected_clients: int
    operations_per_second: float
    avg_ttl: float
    key_count: int
    expired_keys: int
    network_io: Dict[str, int]
    cluster_state: str
    replication_lag: float


@dataclass
class WarmupConfig:
    """Cache warming configuration"""
    enabled: bool = True
    batch_size: int = 1000
    concurrent_jobs: int = 10
    priority_patterns: List[str] = None
    schedule: str = "0 2 * * *"  # Daily at 2 AM
    max_warmup_time: int = 3600  # 1 hour


class RedisClusterManager:
    """Advanced Redis cluster management"""
    
    def __init__(self):
        self.cluster_nodes: List[ClusterNode] = []
        self.cluster_client: Optional[AsyncRedisCluster] = None
        self.sync_cluster_client: Optional[RedisCluster] = None
        
        # Cache configuration
        self.cache_strategies: Dict[str, CacheStrategy] = {}
        self.layer_config: Dict[CacheLayer, Dict] = {}
        
        # Monitoring
        self.metrics: Dict[str, CacheMetrics] = {}
        self.performance_history: List[Dict] = []
        
        # Warmup configuration
        self.warmup_config = WarmupConfig()
        
        self._initialize_config()
    
    def _initialize_config(self):
        """Initialize cluster configuration from environment"""
        # Parse cluster nodes
        cluster_hosts = getattr(config, "REDIS_CLUSTER_HOSTS", "localhost:7000,localhost:7001,localhost:7002").split(",")
        
        for i, host_port in enumerate(cluster_hosts):
            if ":" in host_port:
                host, port = host_port.split(":")
                port = int(port)
            else:
                host = host_port
                port = 7000 + i
            
            node = ClusterNode(
                host=host,
                port=port,
                role="master" if i < 3 else "slave",
                node_id=f"node_{i:02d}",
                max_memory=getattr(config, "REDIS_MAX_MEMORY", "1gb"),
                eviction_policy=getattr(config, "REDIS_EVICTION_POLICY", "allkeys-lru")
            )
            self.cluster_nodes.append(node)
        
        # Cache layer configuration
        self.layer_config = {
            CacheLayer.L1_MEMORY: {
                "enabled": getattr(config, "CACHE_L1_ENABLED", True),
                "max_size": int(getattr(config, "CACHE_L1_MAX_SIZE", "100")),  # MB
                "ttl": int(getattr(config, "CACHE_L1_TTL", "300"))  # 5 minutes
            },
            CacheLayer.L2_REDIS: {
                "enabled": getattr(config, "CACHE_L2_ENABLED", True),
                "max_memory": getattr(config, "CACHE_L2_MAX_MEMORY", "2gb"),
                "ttl": int(getattr(config, "CACHE_L2_TTL", "3600"))  # 1 hour
            },
            CacheLayer.L3_PERSISTENT: {
                "enabled": getattr(config, "CACHE_L3_ENABLED", False),
                "backend": getattr(config, "CACHE_L3_BACKEND", "disk"),
                "ttl": int(getattr(config, "CACHE_L3_TTL", "86400"))  # 24 hours
            }
        }
        
        # Warmup configuration
        self.warmup_config.enabled = getattr(config, "CACHE_WARMUP_ENABLED", True)
        self.warmup_config.batch_size = int(getattr(config, "CACHE_WARMUP_BATCH_SIZE", "1000"))
        self.warmup_config.concurrent_jobs = int(getattr(config, "CACHE_WARMUP_CONCURRENT_JOBS", "10"))
        self.warmup_config.priority_patterns = getattr(config, "CACHE_WARMUP_PATTERNS", "user:*,session:*,config:*").split(",")
    
    async def initialize(self):
        """Initialize Redis cluster connections"""
        try:
            # Build cluster connection
            startup_nodes = [
                {"host": node.host, "port": node.port} 
                for node in self.cluster_nodes
            ]
            
            # Async cluster client
            self.cluster_client = AsyncRedisCluster(
                startup_nodes=startup_nodes,
                decode_responses=True,
                skip_full_coverage_check=True,
                max_connections=int(getattr(config, "REDIS_MAX_CONNECTIONS", "100")),
                retry_on_timeout=True,
                health_check_interval=30,
                socket_keepalive=True,
                socket_keepalive_options={
                    1: 1,  # TCP_KEEPIDLE
                    2: 3,  # TCP_KEEPINTVL  
                    3: 5,  # TCP_KEEPCNT
                }
            )
            
            # Sync cluster client for admin operations
            self.sync_cluster_client = RedisCluster(
                startup_nodes=startup_nodes,
                decode_responses=True,
                skip_full_coverage_check=True,
                max_connections=50
            )
            
            # Test connectivity
            await self.cluster_client.ping()
            
            # Initialize cluster if needed
            await self._setup_cluster()
            
            # Start monitoring
            asyncio.create_task(self._monitor_cluster())
            
            # Schedule cache warming
            if self.warmup_config.enabled:
                asyncio.create_task(self._schedule_warmup())
            
            logger.info(f"Redis cluster initialized with {len(self.cluster_nodes)} nodes")
            
        except Exception as e:
            logger.error(f"Failed to initialize Redis cluster: {e}")
            raise
    
    async def _setup_cluster(self):
        """Setup Redis cluster configuration"""
        try:
            # Check if cluster is already initialized
            cluster_info = await self.cluster_client.cluster_info()
            
            if cluster_info.get("cluster_state") != "ok":
                logger.info("Initializing Redis cluster...")
                
                # Configure each node
                for node in self.cluster_nodes:
                    try:
                        node_client = aioredis.Redis(host=node.host, port=node.port)
                        
                        # Enable cluster mode
                        await node_client.config_set("cluster-enabled", "yes")
                        await node_client.config_set("cluster-config-file", f"nodes-{node.port}.conf")
                        await node_client.config_set("cluster-node-timeout", "5000")
                        
                        # Memory configuration
                        await node_client.config_set("maxmemory", node.max_memory)
                        await node_client.config_set("maxmemory-policy", node.eviction_policy)
                        
                        # Performance tuning
                        await node_client.config_set("tcp-keepalive", "300")
                        await node_client.config_set("timeout", "0")
                        await node_client.config_set("save", "900 1 300 10 60 10000")  # Optimized persistence
                        
                        await node_client.close()
                        
                    except Exception as e:
                        logger.warning(f"Failed to configure node {node.host}:{node.port}: {e}")
            
        except Exception as e:
            logger.error(f"Error setting up cluster: {e}")
    
    async def _monitor_cluster(self):
        """Continuous cluster monitoring"""
        while True:
            try:
                await asyncio.sleep(30)  # Monitor every 30 seconds
                
                # Collect metrics from all nodes
                cluster_metrics = await self._collect_cluster_metrics()
                
                # Update monitoring system
                for node_id, metrics in cluster_metrics.items():
                    await self._update_monitoring_metrics(node_id, metrics)
                
                # Check cluster health
                health_status = await self._check_cluster_health()
                
                if health_status["status"] != "healthy":
                    logger.warning(f"Cluster health issue detected: {health_status}")
                    
                    # Attempt auto-recovery
                    await self._attempt_cluster_recovery()
                
            except Exception as e:
                logger.error(f"Error in cluster monitoring: {e}")
    
    async def _collect_cluster_metrics(self) -> Dict[str, CacheMetrics]:
        """Collect metrics from all cluster nodes"""
        cluster_metrics = {}
        
        try:
            # Get cluster-wide info
            cluster_info = await self.cluster_client.cluster_info()
            cluster_nodes = await self.cluster_client.cluster_nodes()
            
            for node_data in cluster_nodes.values():
                if node_data.get("host"):
                    node_client = aioredis.Redis(
                        host=node_data["host"], 
                        port=node_data["port"]
                    )
                    
                    try:
                        # Get node info
                        info = await node_client.info()
                        memory_info = info.get("memory", {})
                        stats_info = info.get("stats", {})
                        replication_info = info.get("replication", {})
                        
                        # Calculate hit ratio
                        hits = int(stats_info.get("keyspace_hits", 0))
                        misses = int(stats_info.get("keyspace_misses", 0))
                        total_ops = hits + misses
                        hit_ratio = (hits / total_ops * 100) if total_ops > 0 else 0
                        
                        # Build metrics
                        metrics = CacheMetrics(
                            hit_ratio=hit_ratio,
                            miss_ratio=100 - hit_ratio,
                            eviction_count=int(stats_info.get("evicted_keys", 0)),
                            memory_usage=int(memory_info.get("used_memory", 0)),
                            memory_peak=int(memory_info.get("used_memory_peak", 0)),
                            connected_clients=int(info.get("clients", {}).get("connected_clients", 0)),
                            operations_per_second=float(stats_info.get("instantaneous_ops_per_sec", 0)),
                            avg_ttl=await self._calculate_avg_ttl(node_client),
                            key_count=await self._count_keys(node_client),
                            expired_keys=int(stats_info.get("expired_keys", 0)),
                            network_io={
                                "input_bytes": int(stats_info.get("total_net_input_bytes", 0)),
                                "output_bytes": int(stats_info.get("total_net_output_bytes", 0))
                            },
                            cluster_state=cluster_info.get("cluster_state", "unknown"),
                            replication_lag=float(replication_info.get("master_repl_offset", 0)) - 
                                          float(replication_info.get("slave_repl_offset", 0))
                        )
                        
                        node_id = node_data.get("id", f"{node_data['host']}:{node_data['port']}")
                        cluster_metrics[node_id] = metrics
                        
                    except Exception as e:
                        logger.error(f"Error collecting metrics from node {node_data['host']}:{node_data['port']}: {e}")
                    finally:
                        await node_client.close()
            
        except Exception as e:
            logger.error(f"Error collecting cluster metrics: {e}")
        
        return cluster_metrics
    
    async def _calculate_avg_ttl(self, client: aioredis.Redis) -> float:
        """Calculate average TTL across sample of keys"""
        try:
            # Sample 100 random keys
            keys = await client.randomkey()
            if not keys:
                return 0.0
            
            ttl_sum = 0
            count = 0
            
            for _ in range(min(100, await client.dbsize())):
                key = await client.randomkey()
                if key:
                    ttl = await client.ttl(key)
                    if ttl > 0:
                        ttl_sum += ttl
                        count += 1
            
            return ttl_sum / count if count > 0 else 0.0
            
        except Exception:
            return 0.0
    
    async def _count_keys(self, client: aioredis.Redis) -> int:
        """Count total keys in database"""
        try:
            return await client.dbsize()
        except Exception:
            return 0
    
    async def _update_monitoring_metrics(self, node_id: str, metrics: CacheMetrics):
        """Update monitoring system with cache metrics"""
        try:
            labels = {"node_id": node_id}
            
            await monitoring_manager.record_metric("redis_hit_ratio", metrics.hit_ratio, labels)
            await monitoring_manager.record_metric("redis_memory_usage", metrics.memory_usage, labels)
            await monitoring_manager.record_metric("redis_connected_clients", metrics.connected_clients, labels)
            await monitoring_manager.record_metric("redis_ops_per_second", metrics.operations_per_second, labels)
            await monitoring_manager.record_metric("redis_key_count", metrics.key_count, labels)
            await monitoring_manager.record_metric("redis_eviction_count", metrics.eviction_count, labels)
            
        except Exception as e:
            logger.error(f"Error updating monitoring metrics: {e}")
    
    async def _check_cluster_health(self) -> Dict[str, Any]:
        """Check overall cluster health"""
        try:
            cluster_info = await self.cluster_client.cluster_info()
            cluster_nodes = await self.cluster_client.cluster_nodes()
            
            health_status = {
                "status": "healthy",
                "cluster_state": cluster_info.get("cluster_state"),
                "cluster_size": cluster_info.get("cluster_size"),
                "nodes": {},
                "issues": []
            }
            
            # Check cluster state
            if cluster_info.get("cluster_state") != "ok":
                health_status["status"] = "unhealthy"
                health_status["issues"].append(f"Cluster state: {cluster_info.get('cluster_state')}")
            
            # Check individual nodes
            healthy_nodes = 0
            total_nodes = len(cluster_nodes)
            
            for node_id, node_data in cluster_nodes.items():
                node_healthy = True
                node_issues = []
                
                # Check node flags
                flags = node_data.get("flags", [])
                if "fail" in flags or "fail?" in flags:
                    node_healthy = False
                    node_issues.append("Node marked as failed")
                
                if "disconnected" in flags:
                    node_healthy = False
                    node_issues.append("Node disconnected")
                
                # Check ping
                try:
                    if node_data.get("host"):
                        node_client = aioredis.Redis(
                            host=node_data["host"], 
                            port=node_data["port"]
                        )
                        await asyncio.wait_for(node_client.ping(), timeout=5)
                        await node_client.close()
                except Exception as e:
                    node_healthy = False
                    node_issues.append(f"Ping failed: {str(e)}")
                
                if node_healthy:
                    healthy_nodes += 1
                
                health_status["nodes"][node_id] = {
                    "healthy": node_healthy,
                    "issues": node_issues
                }
            
            # Overall health assessment
            if healthy_nodes < total_nodes * 0.5:  # Less than 50% healthy
                health_status["status"] = "critical"
            elif healthy_nodes < total_nodes:
                health_status["status"] = "degraded"
            
            return health_status
            
        except Exception as e:
            logger.error(f"Error checking cluster health: {e}")
            return {
                "status": "unknown",
                "error": str(e)
            }
    
    async def _attempt_cluster_recovery(self):
        """Attempt automatic cluster recovery"""
        try:
            logger.info("Attempting cluster recovery...")
            
            # Try cluster reset and rejoin
            cluster_nodes = await self.cluster_client.cluster_nodes()
            
            for node_id, node_data in cluster_nodes.items():
                if "fail" in node_data.get("flags", []):
                    try:
                        # Try to reset failed node
                        node_client = aioredis.Redis(
                            host=node_data["host"], 
                            port=node_data["port"]
                        )
                        
                        await node_client.cluster("reset", "soft")
                        await node_client.close()
                        
                        logger.info(f"Reset node {node_id}")
                        
                    except Exception as e:
                        logger.error(f"Failed to reset node {node_id}: {e}")
            
            # Wait and recheck
            await asyncio.sleep(10)
            
            health_status = await self._check_cluster_health()
            if health_status["status"] == "healthy":
                logger.info("Cluster recovery successful")
            else:
                logger.warning("Cluster recovery partially successful or failed")
                
        except Exception as e:
            logger.error(f"Error in cluster recovery: {e}")
    
    async def _schedule_warmup(self):
        """Schedule cache warming tasks"""
        while True:
            try:
                # Calculate next warmup time (daily at 2 AM)
                now = datetime.now()
                next_warmup = now.replace(hour=2, minute=0, second=0, microsecond=0)
                
                if next_warmup <= now:
                    next_warmup += timedelta(days=1)
                
                sleep_seconds = (next_warmup - now).total_seconds()
                
                logger.info(f"Next cache warmup scheduled for {next_warmup}")
                await asyncio.sleep(sleep_seconds)
                
                # Start warmup
                await self.warmup_cache()
                
            except Exception as e:
                logger.error(f"Error in warmup scheduler: {e}")
                await asyncio.sleep(3600)  # Retry in 1 hour
    
    async def warmup_cache(self, patterns: Optional[List[str]] = None) -> Dict[str, Any]:
        """Warm up cache with frequently accessed data"""
        if not self.warmup_config.enabled:
            return {"status": "disabled"}
        
        start_time = time.time()
        patterns = patterns or self.warmup_config.priority_patterns
        
        warmup_stats = {
            "status": "started",
            "start_time": datetime.utcnow(),
            "patterns": patterns,
            "keys_warmed": 0,
            "errors": 0,
            "duration": 0
        }
        
        try:
            logger.info(f"Starting cache warmup with patterns: {patterns}")
            
            # Get all keys matching patterns
            all_keys = []
            for pattern in patterns:
                try:
                    keys = []
                    async for key in self.cluster_client.scan_iter(match=pattern):
                        keys.append(key)
                        if len(keys) >= self.warmup_config.batch_size:
                            all_keys.extend(keys)
                            keys = []
                    
                    if keys:
                        all_keys.extend(keys)
                        
                except Exception as e:
                    logger.error(f"Error scanning pattern {pattern}: {e}")
                    warmup_stats["errors"] += 1
            
            # Process keys in batches
            semaphore = asyncio.Semaphore(self.warmup_config.concurrent_jobs)
            
            async def warm_key_batch(key_batch):
                async with semaphore:
                    try:
                        # Simulate warmup by accessing keys
                        pipeline = self.cluster_client.pipeline()
                        for key in key_batch:
                            pipeline.exists(key)
                        
                        await pipeline.execute()
                        return len(key_batch)
                        
                    except Exception as e:
                        logger.error(f"Error warming key batch: {e}")
                        return 0
            
            # Process all keys in batches
            tasks = []
            for i in range(0, len(all_keys), self.warmup_config.batch_size):
                batch = all_keys[i:i + self.warmup_config.batch_size]
                tasks.append(warm_key_batch(batch))
                
                if len(tasks) >= self.warmup_config.concurrent_jobs:
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    for result in results:
                        if isinstance(result, int):
                            warmup_stats["keys_warmed"] += result
                    tasks = []
            
            # Process remaining tasks
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in results:
                    if isinstance(result, int):
                        warmup_stats["keys_warmed"] += result
            
            warmup_stats["status"] = "completed"
            warmup_stats["duration"] = time.time() - start_time
            
            logger.info(f"Cache warmup completed: {warmup_stats['keys_warmed']} keys in {warmup_stats['duration']:.2f}s")
            
        except Exception as e:
            warmup_stats["status"] = "failed"
            warmup_stats["error"] = str(e)
            logger.error(f"Cache warmup failed: {e}")
        
        finally:
            warmup_stats["end_time"] = datetime.utcnow()
            
            # Record metrics
            await monitoring_manager.record_metric(
                "cache_warmup_keys", 
                warmup_stats["keys_warmed"]
            )
            await monitoring_manager.record_metric(
                "cache_warmup_duration", 
                warmup_stats["duration"]
            )
        
        return warmup_stats
    
    async def get_cluster_status(self) -> Dict[str, Any]:
        """Get comprehensive cluster status"""
        try:
            cluster_info = await self.cluster_client.cluster_info()
            cluster_nodes = await self.cluster_client.cluster_nodes()
            
            # Collect metrics
            metrics = await self._collect_cluster_metrics()
            
            # Calculate aggregate metrics
            total_memory = sum(m.memory_usage for m in metrics.values())
            total_keys = sum(m.key_count for m in metrics.values())
            avg_hit_ratio = sum(m.hit_ratio for m in metrics.values()) / len(metrics) if metrics else 0
            total_ops = sum(m.operations_per_second for m in metrics.values())
            
            return {
                "cluster_info": cluster_info,
                "nodes": {
                    node_id: {
                        "host": node_data.get("host"),
                        "port": node_data.get("port"),
                        "role": "master" if "master" in node_data.get("flags", []) else "slave",
                        "status": "connected" if "connected" in node_data.get("flags", []) else "disconnected",
                        "slots": node_data.get("slots", []),
                        "metrics": asdict(metrics.get(node_id)) if node_id in metrics else None
                    }
                    for node_id, node_data in cluster_nodes.items()
                },
                "aggregate_metrics": {
                    "total_memory_mb": total_memory / 1024 / 1024,
                    "total_keys": total_keys,
                    "average_hit_ratio": avg_hit_ratio,
                    "total_ops_per_second": total_ops
                },
                "health": await self._check_cluster_health(),
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error getting cluster status: {e}")
            return {"error": str(e)}
    
    async def optimize_cluster(self) -> Dict[str, Any]:
        """Optimize cluster performance"""
        optimization_results = {
            "optimizations_applied": [],
            "recommendations": [],
            "timestamp": datetime.utcnow()
        }
        
        try:
            # Collect current metrics
            metrics = await self._collect_cluster_metrics()
            
            for node_id, node_metrics in metrics.items():
                optimizations = []
                recommendations = []
                
                # Memory optimization
                memory_usage_pct = (node_metrics.memory_usage / (2 * 1024 * 1024 * 1024)) * 100  # Assume 2GB max
                
                if memory_usage_pct > 80:
                    recommendations.append(f"Node {node_id}: High memory usage ({memory_usage_pct:.1f}%)")
                    
                    # Trigger eviction
                    node_info = await self.cluster_client.cluster_nodes()
                    node_data = node_info.get(node_id)
                    
                    if node_data:
                        node_client = aioredis.Redis(
                            host=node_data["host"],
                            port=node_data["port"]
                        )
                        
                        await node_client.config_set("maxmemory-policy", "allkeys-lru")
                        optimizations.append(f"Node {node_id}: Set LRU eviction policy")
                        
                        await node_client.close()
                
                # Hit ratio optimization
                if node_metrics.hit_ratio < 80:
                    recommendations.append(f"Node {node_id}: Low hit ratio ({node_metrics.hit_ratio:.1f}%)")
                    recommendations.append(f"Node {node_id}: Consider cache warming or TTL adjustment")
                
                # Connection optimization
                if node_metrics.connected_clients > 100:
                    recommendations.append(f"Node {node_id}: High client connections ({node_metrics.connected_clients})")
                    recommendations.append(f"Node {node_id}: Consider connection pooling")
                
                optimization_results["optimizations_applied"].extend(optimizations)
                optimization_results["recommendations"].extend(recommendations)
            
        except Exception as e:
            logger.error(f"Error optimizing cluster: {e}")
            optimization_results["error"] = str(e)
        
        return optimization_results
    
    async def close(self):
        """Close cluster connections"""
        try:
            if self.cluster_client:
                await self.cluster_client.close()
            
            if self.sync_cluster_client:
                self.sync_cluster_client.close()
                
            logger.info("Redis cluster connections closed")
            
        except Exception as e:
            logger.error(f"Error closing cluster connections: {e}")


# Global instance
redis_cluster_manager = RedisClusterManager()

def get_redis_cluster_manager() -> RedisClusterManager:
    """Get the global redis cluster manager instance"""
    return redis_cluster_manager

async def initialize_redis_cluster_manager():
    """Initialize the redis cluster manager"""
    try:
        await redis_cluster_manager.initialize()
        logger.info("Redis cluster manager initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize redis cluster manager: {e}")
        return False




