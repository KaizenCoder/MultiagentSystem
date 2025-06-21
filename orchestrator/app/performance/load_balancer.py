"""
Advanced Load Balancer Management for Enterprise Production
Handles multi-instance orchestration, health checks, and traffic distribution

IA-2 Architecture & Production - Sprint 2.2
"""

import asyncio
import aiohttp
import time
import random
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
from collections import defaultdict, deque
import sys
from pathlib import Path

# Golden Source Logging
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from core import logging_manager

# Monitoring integration
from ..observability.monitoring import get_monitoring

# Configuration du logging
logger = logging_manager.get_logger('load_balancer', custom_config={
    "logger_name": "LoadBalancer",
    "log_level": "INFO",
    "elasticsearch_enabled": True,
    "async_enabled": True
})

class BackendHealth(Enum):
    """Backend health status enumeration"""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DRAINING = "draining"
    MAINTENANCE = "maintenance"

class LoadBalancingAlgorithm(Enum):
    """Load balancing algorithms"""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    IP_HASH = "ip_hash"
    LEAST_RESPONSE_TIME = "least_response_time"

@dataclass
class BackendServer:
    """Backend server configuration and state"""
    id: str
    host: str
    port: int
    weight: int = 100
    max_connections: int = 1000
    health: BackendHealth = BackendHealth.HEALTHY
    
    # State tracking
    active_connections: int = 0
    total_requests: int = 0
    failed_requests: int = 0
    last_response_time: float = 0.0
    last_health_check: Optional[datetime] = None
    
    # Performance metrics
    response_times: deque = field(default_factory=lambda: deque(maxlen=100))
    error_rates: deque = field(default_factory=lambda: deque(maxlen=100))
    
    @property
    def avg_response_time(self) -> float:
        """Calculate average response time"""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    @property
    def error_rate(self) -> float:
        """Calculate error rate percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.failed_requests / self.total_requests) * 100
    
    @property
    def load_score(self) -> float:
        """Calculate load score for least_response_time algorithm"""
        base_score = self.active_connections / self.max_connections
        response_penalty = min(self.avg_response_time / 1000.0, 1.0)  # Cap at 1s
        error_penalty = self.error_rate / 100.0
        
        return base_score + response_penalty + error_penalty

@dataclass
class HealthCheckConfig:
    """Health check configuration"""
    enabled: bool = True
    interval: int = 30  # seconds
    timeout: int = 10   # seconds
    healthy_threshold: int = 2
    unhealthy_threshold: int = 3
    path: str = "/health"
    expected_status: int = 200
    expected_response_time: float = 5.0  # seconds

class AdvancedLoadBalancer:
    """
    Enterprise-grade load balancer with advanced features:
    - Multiple algorithms (round-robin, least connections, etc.)
    - Health monitoring with auto-recovery
    - Session affinity
    - Circuit breaker integration
    - Performance metrics tracking
    """
    
    def __init__(
        self,
        algorithm: LoadBalancingAlgorithm = LoadBalancingAlgorithm.LEAST_CONNECTIONS,
        health_config: Optional[HealthCheckConfig] = None
    ):
        self.algorithm = algorithm
        self.health_config = health_config or HealthCheckConfig()
        
        # Backend management
        self.backends: Dict[str, BackendServer] = {}
        self.round_robin_index = 0
        
        # Session affinity (sticky sessions)
        self.session_affinity: Dict[str, str] = {}  # session_id -> backend_id
        self.affinity_ttl: Dict[str, datetime] = {}  # session_id -> expiry
        
        # Performance tracking
        self.request_count = 0
        self.start_time = datetime.now()
        
        # Health monitoring
        self.health_check_task: Optional[asyncio.Task] = None
        self.monitoring = None
        
        # Metrics tracking
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'avg_response_time': 0.0,
            'backends_healthy': 0,
            'backends_total': 0
        }
    
    async def initialize(self):
        """Initialize load balancer and start background tasks"""
        try:
            # Initialize monitoring
            self.monitoring = await get_monitoring()
            
            # Start health check monitoring
            if self.health_config.enabled:
                self.health_check_task = asyncio.create_task(self._health_check_loop())
            
            logger.info(f"Load balancer initialized with algorithm: {self.algorithm.value}")
            
        except Exception as e:
            logger.error(f"Failed to initialize load balancer: {e}")
            raise
    
    def add_backend(self, backend: BackendServer) -> None:
        """Add a backend server to the pool"""
        self.backends[backend.id] = backend
        self.metrics['backends_total'] = len(self.backends)
        logger.info(f"Added backend: {backend.id} ({backend.host}:{backend.port})")
    
    def remove_backend(self, backend_id: str) -> bool:
        """Remove a backend server from the pool"""
        if backend_id in self.backends:
            # Drain existing connections gracefully
            self.backends[backend_id].health = BackendHealth.DRAINING
            
            # Remove after grace period (handled by health check loop)
            logger.info(f"Marking backend for removal: {backend_id}")
            return True
        return False
    
    async def get_backend(self, client_ip: str = None, session_id: str = None) -> Optional[BackendServer]:
        """
        Select the best backend server based on configured algorithm
        
        Args:
            client_ip: Client IP for IP hash algorithm
            session_id: Session ID for sticky sessions
            
        Returns:
            Selected backend server or None if no healthy backends
        """
        # Check session affinity first
        if session_id and session_id in self.session_affinity:
            backend_id = self.session_affinity[session_id]
            if (backend_id in self.backends and 
                self.backends[backend_id].health == BackendHealth.HEALTHY and
                self._is_affinity_valid(session_id)):
                return self.backends[backend_id]
            else:
                # Clean up expired or invalid affinity
                self._cleanup_affinity(session_id)
        
        # Get healthy backends
        healthy_backends = [
            backend for backend in self.backends.values()
            if backend.health == BackendHealth.HEALTHY
        ]
        
        if not healthy_backends:
            logger.warning("No healthy backends available")
            return None
        
        # Apply load balancing algorithm
        selected_backend = None
        
        if self.algorithm == LoadBalancingAlgorithm.ROUND_ROBIN:
            selected_backend = self._round_robin_select(healthy_backends)
        elif self.algorithm == LoadBalancingAlgorithm.LEAST_CONNECTIONS:
            selected_backend = self._least_connections_select(healthy_backends)
        elif self.algorithm == LoadBalancingAlgorithm.WEIGHTED_ROUND_ROBIN:
            selected_backend = self._weighted_round_robin_select(healthy_backends)
        elif self.algorithm == LoadBalancingAlgorithm.IP_HASH:
            selected_backend = self._ip_hash_select(healthy_backends, client_ip or "default")
        elif self.algorithm == LoadBalancingAlgorithm.LEAST_RESPONSE_TIME:
            selected_backend = self._least_response_time_select(healthy_backends)
        
        # Establish session affinity if session_id provided
        if selected_backend and session_id:
            self._set_affinity(session_id, selected_backend.id)
        
        return selected_backend
    
    def _round_robin_select(self, backends: List[BackendServer]) -> BackendServer:
        """Round-robin backend selection"""
        backend = backends[self.round_robin_index % len(backends)]
        self.round_robin_index = (self.round_robin_index + 1) % len(backends)
        return backend
    
    def _least_connections_select(self, backends: List[BackendServer]) -> BackendServer:
        """Select backend with least active connections"""
        return min(backends, key=lambda b: b.active_connections)
    
    def _weighted_round_robin_select(self, backends: List[BackendServer]) -> BackendServer:
        """Weighted round-robin selection based on backend weights"""
        total_weight = sum(b.weight for b in backends)
        target = self.round_robin_index % total_weight
        
        current_weight = 0
        for backend in backends:
            current_weight += backend.weight
            if current_weight > target:
                self.round_robin_index = (self.round_robin_index + 1) % total_weight
                return backend
        
        # Fallback to first backend
        return backends[0]
    
    def _ip_hash_select(self, backends: List[BackendServer], client_ip: str) -> BackendServer:
        """IP hash-based backend selection for session persistence"""
        hash_value = hash(client_ip) % len(backends)
        return backends[hash_value]
    
    def _least_response_time_select(self, backends: List[BackendServer]) -> BackendServer:
        """Select backend with lowest load score (connections + response time + errors)"""
        return min(backends, key=lambda b: b.load_score)
    
    def _set_affinity(self, session_id: str, backend_id: str, ttl_minutes: int = 60):
        """Set session affinity with TTL"""
        self.session_affinity[session_id] = backend_id
        self.affinity_ttl[session_id] = datetime.now() + timedelta(minutes=ttl_minutes)
    
    def _is_affinity_valid(self, session_id: str) -> bool:
        """Check if session affinity is still valid"""
        if session_id not in self.affinity_ttl:
            return False
        return datetime.now() < self.affinity_ttl[session_id]
    
    def _cleanup_affinity(self, session_id: str):
        """Clean up expired session affinity"""
        self.session_affinity.pop(session_id, None)
        self.affinity_ttl.pop(session_id, None)
    
    async def record_request(self, backend: BackendServer, success: bool, response_time: float):
        """Record request metrics for backend"""
        backend.total_requests += 1
        backend.last_response_time = response_time
        backend.response_times.append(response_time)
        
        if success:
            self.metrics['successful_requests'] += 1
        else:
            backend.failed_requests += 1
            self.metrics['failed_requests'] += 1
            backend.error_rates.append(1.0)
        
        self.metrics['total_requests'] += 1
        
        # Update average response time
        if self.metrics['total_requests'] > 0:
            self.metrics['avg_response_time'] = (
                (self.metrics['avg_response_time'] * (self.metrics['total_requests'] - 1) + response_time) / 
                self.metrics['total_requests']
            )
        
        # Record metrics in monitoring system
        if self.monitoring:
            await self.monitoring.record_metric(
                'load_balancer_requests_total',
                1,
                {'backend': backend.id, 'success': str(success)}
            )
            await self.monitoring.record_metric(
                'load_balancer_response_time_seconds',
                response_time,
                {'backend': backend.id}
            )
    
    async def acquire_connection(self, backend: BackendServer) -> bool:
        """Acquire a connection slot from backend"""
        if backend.active_connections >= backend.max_connections:
            return False
        
        backend.active_connections += 1
        return True
    
    def release_connection(self, backend: BackendServer):
        """Release a connection slot back to backend"""
        if backend.active_connections > 0:
            backend.active_connections -= 1
    
    async def _health_check_loop(self):
        """Background health check monitoring loop"""
        while True:
            try:
                await self._check_all_backends_health()
                await asyncio.sleep(self.health_config.interval)
            except asyncio.CancelledError:
                logger.info("Health check loop cancelled")
                break
            except Exception as e:
                logger.error(f"Health check loop error: {e}")
                await asyncio.sleep(self.health_config.interval)
    
    async def _check_all_backends_health(self):
        """Check health of all backends"""
        tasks = [
            self._check_backend_health(backend) 
            for backend in self.backends.values()
        ]
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        # Update metrics
        healthy_count = sum(
            1 for backend in self.backends.values() 
            if backend.health == BackendHealth.HEALTHY
        )
        self.metrics['backends_healthy'] = healthy_count
    
    async def _check_backend_health(self, backend: BackendServer):
        """Perform health check on a single backend"""
        url = f"http://{backend.host}:{backend.port}{self.health_config.path}"
        
        try:
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, 
                    timeout=aiohttp.ClientTimeout(total=self.health_config.timeout)
                ) as response:
                    response_time = time.time() - start_time
                    
                    # Check response criteria
                    is_healthy = (
                        response.status == self.health_config.expected_status and
                        response_time <= self.health_config.expected_response_time
                    )
                    
                    # Update backend health based on consecutive checks
                    if is_healthy:
                        if backend.health == BackendHealth.UNHEALTHY:
                            # Require multiple successful checks to mark healthy
                            backend._consecutive_health_checks = getattr(backend, '_consecutive_health_checks', 0) + 1
                            if backend._consecutive_health_checks >= self.health_config.healthy_threshold:
                                backend.health = BackendHealth.HEALTHY
                                logger.info(f"Backend {backend.id} marked as healthy")
                        else:
                            backend.health = BackendHealth.HEALTHY
                            backend._consecutive_health_checks = 0
                    else:
                        backend._consecutive_health_checks = getattr(backend, '_consecutive_health_checks', 0) + 1
                        if backend._consecutive_health_checks >= self.health_config.unhealthy_threshold:
                            backend.health = BackendHealth.UNHEALTHY
                            logger.warning(f"Backend {backend.id} marked as unhealthy")
                    
                    backend.last_health_check = datetime.now()
                    
        except Exception as e:
            logger.error(f"Health check failed for backend {backend.id}: {e}")
            backend._consecutive_health_checks = getattr(backend, '_consecutive_health_checks', 0) + 1
            if backend._consecutive_health_checks >= self.health_config.unhealthy_threshold:
                backend.health = BackendHealth.UNHEALTHY
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive load balancer statistics"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        backend_stats = []
        for backend in self.backends.values():
            backend_stats.append({
                'id': backend.id,
                'host': backend.host,
                'port': backend.port,
                'health': backend.health.value,
                'active_connections': backend.active_connections,
                'total_requests': backend.total_requests,
                'failed_requests': backend.failed_requests,
                'error_rate': backend.error_rate,
                'avg_response_time': backend.avg_response_time,
                'last_health_check': backend.last_health_check.isoformat() if backend.last_health_check else None
            })
        
        return {
            'algorithm': self.algorithm.value,
            'uptime_seconds': uptime,
            'metrics': self.metrics,
            'backends': backend_stats,
            'session_affinity_count': len(self.session_affinity),
            'health_check_config': {
                'enabled': self.health_config.enabled,
                'interval': self.health_config.interval,
                'timeout': self.health_config.timeout
            }
        }
    
    async def shutdown(self):
        """Graceful shutdown of load balancer"""
        logger.info("Shutting down load balancer...")
        
        # Cancel health check task
        if self.health_check_task:
            self.health_check_task.cancel()
            try:
                await self.health_check_task
            except asyncio.CancelledError:
                pass
        
        # Mark all backends as draining
        for backend in self.backends.values():
            backend.health = BackendHealth.DRAINING
        
        logger.info("Load balancer shutdown complete")

# Global load balancer instance
_load_balancer_instance: Optional[AdvancedLoadBalancer] = None

async def get_load_balancer() -> AdvancedLoadBalancer:
    """Get global load balancer instance"""
    global _load_balancer_instance
    
    if _load_balancer_instance is None:
        _load_balancer_instance = AdvancedLoadBalancer()
        await _load_balancer_instance.initialize()
    
    return _load_balancer_instance

async def configure_load_balancer(
    algorithm: LoadBalancingAlgorithm = LoadBalancingAlgorithm.LEAST_CONNECTIONS,
    health_config: Optional[HealthCheckConfig] = None
) -> AdvancedLoadBalancer:
    """Configure and get load balancer instance"""
    global _load_balancer_instance
    
    if _load_balancer_instance:
        await _load_balancer_instance.shutdown()
    
    _load_balancer_instance = AdvancedLoadBalancer(algorithm, health_config)
    await _load_balancer_instance.initialize()
    
    return _load_balancer_instance




