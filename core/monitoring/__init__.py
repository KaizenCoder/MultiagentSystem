"""
Module de Monitoring et Métriques Avancées
NextGeneration Maintenance Team Optimization

Ce module fournit:
- Collecte de métriques en temps réel
- Circuit breakers pour la robustesse
- Alertes intelligentes
- Dashboard de monitoring
"""

from .metrics_collector import AdvancedMetricsCollector, AgentMetrics, monitor_performance
from .circuit_breaker import CircuitBreaker, CircuitState, CircuitBreakerOpenException
from .cache_manager import IntelligentCache
from .config_manager import MaintenanceConfig, AgentConfig

__version__ = "2.0.0"
__author__ = "NextGeneration Team"

__all__ = [
    "AdvancedMetricsCollector",
    "AgentMetrics", 
    "monitor_performance",
    "CircuitBreaker",
    "CircuitState",
    "CircuitBreakerOpenException",
    "IntelligentCache",
    "MaintenanceConfig",
    "AgentConfig"
]

# Configuration par défaut
DEFAULT_CONFIG = {
    "metrics_collection_interval": 10,
    "cache_ttl": 3600,
    "circuit_breaker_threshold": 5,
    "alert_thresholds": {
        "high_error_rate": 0.15,
        "slow_response": 30.0,
        "high_memory": 500 * 1024 * 1024
    }
} 