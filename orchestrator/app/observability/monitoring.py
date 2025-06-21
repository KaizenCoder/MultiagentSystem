"""
Monitoring et observabilit production-ready
Mtriques custom, dashboards, et alerting intelligent
"""
import os
import time
import asyncio
from logging_manager_optimized import LoggingManager
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json

try:
    from prometheus_client import Counter, Histogram, Gauge, Info, CollectorRegistry, generate_latest
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

from orchestrator.app.security.logging import security_logger

# LoggingManager NextGeneration - Tool/Utility
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={
            "logger_name": "MetricType",
            "log_level": "INFO",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": True
        })


class MetricType(Enum):
    """Types de mtriques"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    INFO = "info"


class AlertSeverity(Enum):
    """Niveaux de svrit des alertes"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class CustomMetric:
    """Mtrique personnalise avec mtadonnes"""
    name: str
    help: str
    metric_type: MetricType
    labels: List[str] = field(default_factory=list)
    buckets: Optional[List[float]] = None  # Pour histogrammes
    
    def __post_init__(self):
        if self.metric_type == MetricType.HISTOGRAM and self.buckets is None:
            # Buckets par dfaut pour histogrammes
            self.buckets = [0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]


@dataclass
class AlertRule:
    """Rgle d'alerte Prometheus"""
    name: str
    expr: str  # Expression PromQL
    for_duration: str  # Dure (ex: "5m")
    severity: AlertSeverity
    summary: str
    description: str
    runbook_url: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)


class ProductionMonitoring:
    """
    Systme de monitoring production-ready avec:
    - Mtriques custom Prometheus
    - Alertes intelligentes
    - Dashboards Grafana
    - Health checks avancs
    - SLA tracking
    """
    
    def __init__(self, registry: Optional[CollectorRegistry] = None):
        self.registry = registry or CollectorRegistry()
        self.metrics: Dict[str, Any] = {}
        self.alert_rules: List[AlertRule] = []
        self.health_checks: Dict[str, Callable] = {}
        
        # tat du systme
        self.system_start_time = time.time()
        self.last_health_check = None
        self.health_status = "unknown"
        
        # Configuration d'alerting
        self.alert_handlers: List[Callable] = []
        
        if PROMETHEUS_AVAILABLE:
            self._init_core_metrics()
            self._init_business_metrics()
            self._init_alert_rules()
        else:
            security_logger.log_error("Prometheus client not available, monitoring disabled")
    
    def _init_core_metrics(self):
        """Initialise les mtriques core systme"""
        core_metrics = [
            CustomMetric(
                name="orchestrator_requests_total",
                help="Total requests processed by orchestrator",
                metric_type=MetricType.COUNTER,
                labels=["method", "endpoint", "status_code", "user_type"]
            ),
            CustomMetric(
                name="orchestrator_request_duration_seconds",
                help="Request processing duration in seconds",
                metric_type=MetricType.HISTOGRAM,
                labels=["method", "endpoint"],
                buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
            ),
            CustomMetric(
                name="orchestrator_llm_requests_total",
                help="Total LLM API requests",
                metric_type=MetricType.COUNTER,
                labels=["provider", "model", "status"]
            ),
            CustomMetric(
                name="orchestrator_llm_latency_seconds",
                help="LLM request latency in seconds",
                metric_type=MetricType.HISTOGRAM,
                labels=["provider", "model"],
                buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0, 60.0, 120.0]
            ),
            CustomMetric(
                name="orchestrator_active_sessions",
                help="Number of active user sessions",
                metric_type=MetricType.GAUGE
            ),
            CustomMetric(
                name="orchestrator_memory_usage_bytes",
                help="Memory usage in bytes",
                metric_type=MetricType.GAUGE,
                labels=["type"]
            ),
            CustomMetric(
                name="orchestrator_cache_operations_total",
                help="Total cache operations",
                metric_type=MetricType.COUNTER,
                labels=["operation", "cache_type", "status"]
            ),
            CustomMetric(
                name="orchestrator_cache_hit_ratio",
                help="Cache hit ratio",
                metric_type=MetricType.GAUGE,
                labels=["cache_type"]
            ),
            CustomMetric(
                name="orchestrator_errors_total",
                help="Total errors by type",
                metric_type=MetricType.COUNTER,
                labels=["error_type", "component", "severity"]
            ),
            CustomMetric(
                name="orchestrator_security_events_total",
                help="Total security events",
                metric_type=MetricType.COUNTER,
                labels=["event_type", "severity", "source"]
            )
        ]
        
        for metric_def in core_metrics:
            self._create_metric(metric_def)
    
    def _init_business_metrics(self):
        """Initialise les mtriques business spcifiques"""
        business_metrics = [
            CustomMetric(
                name="orchestrator_agents_created_total",
                help="Total agents created",
                metric_type=MetricType.COUNTER,
                labels=["agent_type", "user_tier"]
            ),
            CustomMetric(
                name="orchestrator_code_generations_total",
                help="Total code generations",
                metric_type=MetricType.COUNTER,
                labels=["language", "complexity", "success"]
            ),
            CustomMetric(
                name="orchestrator_user_satisfaction_score",
                help="User satisfaction score (1-10)",
                metric_type=MetricType.HISTOGRAM,
                labels=["feature", "user_tier"],
                buckets=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ),
            CustomMetric(
                name="orchestrator_session_duration_seconds",
                help="User session duration",
                metric_type=MetricType.HISTOGRAM,
                labels=["user_tier"],
                buckets=[60, 300, 600, 1800, 3600, 7200, 14400, 28800]  # 1min to 8h
            ),
            CustomMetric(
                name="orchestrator_api_quota_usage",
                help="API quota usage percentage",
                metric_type=MetricType.GAUGE,
                labels=["provider", "user_tier"]
            ),
            CustomMetric(
                name="orchestrator_revenue_tracking",
                help="Revenue tracking metrics",
                metric_type=MetricType.COUNTER,
                labels=["plan_type", "billing_cycle"]
            )
        ]
        
        for metric_def in business_metrics:
            self._create_metric(metric_def)
    
    def _create_metric(self, metric_def: CustomMetric):
        """Cre une mtrique Prometheus"""
        if not PROMETHEUS_AVAILABLE:
            return
        
        try:
            if metric_def.metric_type == MetricType.COUNTER:
                metric = Counter(
                    metric_def.name,
                    metric_def.help,
                    labelnames=metric_def.labels,
                    registry=self.registry
                )
            elif metric_def.metric_type == MetricType.GAUGE:
                metric = Gauge(
                    metric_def.name,
                    metric_def.help,
                    labelnames=metric_def.labels,
                    registry=self.registry
                )
            elif metric_def.metric_type == MetricType.HISTOGRAM:
                metric = Histogram(
                    metric_def.name,
                    metric_def.help,
                    labelnames=metric_def.labels,
                    buckets=metric_def.buckets,
                    registry=self.registry
                )
            elif metric_def.metric_type == MetricType.INFO:
                metric = Info(
                    metric_def.name,
                    metric_def.help,
                    labelnames=metric_def.labels,
                    registry=self.registry
                )
            else:
                raise ValueError(f"Unknown metric type: {metric_def.metric_type}")
            
            self.metrics[metric_def.name] = metric
            
        except Exception as e:
            security_logger.log_error(f"Failed to create metric {metric_def.name}", e)
    
    def _init_alert_rules(self):
        """Initialise les rgles d'alerte Prometheus"""
        self.alert_rules = [
            # Alertes Infrastructure
            AlertRule(
                name="HighErrorRate",
                expr='rate(orchestrator_requests_total{status_code=~"5.."}[5m]) > 0.05',
                for_duration="2m",
                severity=AlertSeverity.HIGH,
                summary="High error rate detected",
                description="Error rate is above 5% for 2 minutes",
                runbook_url="https://docs.company.com/runbooks/high-error-rate",
                labels={"team": "platform", "service": "orchestrator"},
                annotations={
                    "dashboard": "https://grafana.company.com/d/orchestrator",
                    "logs": "https://kibana.company.com/app/discover"
                }
            ),
            AlertRule(
                name="HighLatency",
                expr='histogram_quantile(0.95, rate(orchestrator_request_duration_seconds_bucket[5m])) > 2.0',
                for_duration="5m",
                severity=AlertSeverity.MEDIUM,
                summary="High request latency",
                description="95th percentile latency is above 2 seconds",
                runbook_url="https://docs.company.com/runbooks/high-latency"
            ),
            AlertRule(
                name="LLMProviderDown",
                expr='rate(orchestrator_llm_requests_total{status="error"}[5m]) > 0.5',
                for_duration="1m",
                severity=AlertSeverity.CRITICAL,
                summary="LLM provider experiencing issues",
                description="LLM provider error rate above 50%",
                runbook_url="https://docs.company.com/runbooks/llm-provider-issues"
            ),
            AlertRule(
                name="MemoryUsageHigh",
                expr='orchestrator_memory_usage_bytes{type="rss"} > 1073741824',  # 1GB
                for_duration="10m",
                severity=AlertSeverity.MEDIUM,
                summary="High memory usage",
                description="Memory usage above 1GB for 10 minutes"
            ),
            AlertRule(
                name="CacheHitRateLow",
                expr='orchestrator_cache_hit_ratio < 0.5',
                for_duration="15m",
                severity=AlertSeverity.LOW,
                summary="Low cache hit ratio",
                description="Cache hit ratio below 50% for 15 minutes"
            ),
            # Alertes Business
            AlertRule(
                name="UserSatisfactionLow",
                expr='rate(orchestrator_user_satisfaction_score_bucket{le="5"}[1h]) / rate(orchestrator_user_satisfaction_score_count[1h]) > 0.3',
                for_duration="30m",
                severity=AlertSeverity.HIGH,
                summary="Low user satisfaction",
                description="More than 30% of users rating below 5/10"
            ),
            AlertRule(
                name="APIQuotaHigh",
                expr='orchestrator_api_quota_usage > 0.8',
                for_duration="5m",
                severity=AlertSeverity.MEDIUM,
                summary="API quota usage high",
                description="API quota usage above 80%"
            ),
            # Alertes Scurit
            AlertRule(
                name="SecurityEventSpike",
                expr='rate(orchestrator_security_events_total{severity="high"}[5m]) > 10',
                for_duration="1m",
                severity=AlertSeverity.CRITICAL,
                summary="High security event rate",
                description="More than 10 high-severity security events per minute"
            )
        ]
    
    def increment_counter(self, metric_name: str, labels: Optional[Dict[str, str]] = None, value: float = 1):
        """Incrmente un compteur"""
        if metric_name in self.metrics and PROMETHEUS_AVAILABLE:
            try:
                if labels:
                    self.metrics[metric_name].labels(**labels).inc(value)
                else:
                    self.metrics[metric_name].inc(value)
            except Exception as e:
                security_logger.log_error(f"Failed to increment counter {metric_name}", e)
    
    def set_gauge(self, metric_name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Dfinit la valeur d'une gauge"""
        if metric_name in self.metrics and PROMETHEUS_AVAILABLE:
            try:
                if labels:
                    self.metrics[metric_name].labels(**labels).set(value)
                else:
                    self.metrics[metric_name].set(value)
            except Exception as e:
                security_logger.log_error(f"Failed to set gauge {metric_name}", e)
    
    def observe_histogram(self, metric_name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Observe une valeur dans un histogramme"""
        if metric_name in self.metrics and PROMETHEUS_AVAILABLE:
            try:
                if labels:
                    self.metrics[metric_name].labels(**labels).observe(value)
                else:
                    self.metrics[metric_name].observe(value)
            except Exception as e:
                security_logger.log_error(f"Failed to observe histogram {metric_name}", e)
    
    def track_request(self, method: str, endpoint: str, status_code: int, duration: float, user_type: str = "standard"):
        """Track une requte HTTP"""
        # Compteur de requtes
        self.increment_counter("orchestrator_requests_total", {
            "method": method,
            "endpoint": endpoint,
            "status_code": str(status_code),
            "user_type": user_type
        })
        
        # Dure de la requte
        self.observe_histogram("orchestrator_request_duration_seconds", duration, {
            "method": method,
            "endpoint": endpoint
        })
        
        # Tracking des erreurs
        if status_code >= 400:
            error_type = "client_error" if status_code < 500 else "server_error"
            self.increment_counter("orchestrator_errors_total", {
                "error_type": error_type,
                "component": "api",
                "severity": "medium" if status_code < 500 else "high"
            })
    
    def track_llm_request(self, provider: str, model: str, latency: float, success: bool):
        """Track une requte LLM"""
        status = "success" if success else "error"
        
        self.increment_counter("orchestrator_llm_requests_total", {
            "provider": provider,
            "model": model,
            "status": status
        })
        
        if success:
            self.observe_histogram("orchestrator_llm_latency_seconds", latency, {
                "provider": provider,
                "model": model
            })
    
    def track_cache_operation(self, operation: str, cache_type: str, success: bool):
        """Track une opration de cache"""
        status = "success" if success else "error"
        
        self.increment_counter("orchestrator_cache_operations_total", {
            "operation": operation,
            "cache_type": cache_type,
            "status": status
        })
    
    def update_cache_hit_ratio(self, cache_type: str, hit_ratio: float):
        """Met  jour le ratio de hit du cache"""
        self.set_gauge("orchestrator_cache_hit_ratio", hit_ratio, {
            "cache_type": cache_type
        })
    
    def track_user_session(self, user_tier: str, duration: float):
        """Track la dure d'une session utilisateur"""
        self.observe_histogram("orchestrator_session_duration_seconds", duration, {
            "user_tier": user_tier
        })
    
    def update_active_sessions(self, count: int):
        """Met  jour le nombre de sessions actives"""
        self.set_gauge("orchestrator_active_sessions", count)
    
    def track_security_event(self, event_type: str, severity: str, source: str):
        """Track un vnement de scurit"""
        self.increment_counter("orchestrator_security_events_total", {
            "event_type": event_type,
            "severity": severity,
            "source": source
        })
    
    def track_user_satisfaction(self, score: float, feature: str, user_tier: str):
        """Track la satisfaction utilisateur"""
        self.observe_histogram("orchestrator_user_satisfaction_score", score, {
            "feature": feature,
            "user_tier": user_tier
        })
    
    def update_memory_usage(self, memory_type: str, bytes_used: int):
        """Met  jour l'utilisation mmoire"""
        self.set_gauge("orchestrator_memory_usage_bytes", bytes_used, {
            "type": memory_type
        })
    
    def update_api_quota_usage(self, provider: str, user_tier: str, usage_percent: float):
        """Met  jour l'utilisation des quotas API"""
        self.set_gauge("orchestrator_api_quota_usage", usage_percent, {
            "provider": provider,
            "user_tier": user_tier
        })
    
    def add_health_check(self, name: str, check_func: Callable[[], bool]):
        """Ajoute un health check"""
        self.health_checks[name] = check_func
    
    async def run_health_checks(self) -> Dict[str, Any]:
        """Excute tous les health checks"""
        results = {}
        overall_healthy = True
        
        for name, check_func in self.health_checks.items():
            try:
                start_time = time.time()
                
                if asyncio.iscoroutinefunction(check_func):
                    healthy = await check_func()
                else:
                    healthy = check_func()
                
                duration = time.time() - start_time
                
                results[name] = {
                    "healthy": healthy,
                    "duration_ms": round(duration * 1000, 2),
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                if not healthy:
                    overall_healthy = False
                    
            except Exception as e:
                results[name] = {
                    "healthy": False,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }
                overall_healthy = False
        
        self.last_health_check = datetime.utcnow()
        self.health_status = "healthy" if overall_healthy else "unhealthy"
        
        # Mtriques de health check
        for name, result in results.items():
            self.set_gauge("orchestrator_health_check_status", 1 if result["healthy"] else 0, {
                "check_name": name
            })
        
        return {
            "overall_healthy": overall_healthy,
            "checks": results,
            "uptime_seconds": time.time() - self.system_start_time,
            "last_check": self.last_health_check.isoformat() if self.last_health_check else None
        }
    
    def get_prometheus_metrics(self) -> str:
        """Retourne les mtriques au format Prometheus"""
        if not PROMETHEUS_AVAILABLE:
            return "# Prometheus not available\n"
        
        try:
            return generate_latest(self.registry).decode('utf-8')
        except Exception as e:
            security_logger.log_error("Failed to generate Prometheus metrics", e)
            return f"# Error generating metrics: {str(e)}\n"
    
    def generate_alert_rules_yaml(self) -> str:
        """Gnre la configuration YAML des rgles d'alerte"""
        config = {
            "groups": [{
                "name": "orchestrator-alerts",
                "rules": []
            }]
        }
        
        for rule in self.alert_rules:
            rule_config = {
                "alert": rule.name,
                "expr": rule.expr,
                "for": rule.for_duration,
                "labels": {
                    "severity": rule.severity.value,
                    **rule.labels
                },
                "annotations": {
                    "summary": rule.summary,
                    "description": rule.description,
                    **rule.annotations
                }
            }
            
            if rule.runbook_url:
                rule_config["annotations"]["runbook_url"] = rule.runbook_url
            
            config["groups"][0]["rules"].append(rule_config)
        
        import yaml
        return yaml.dump(config, default_flow_style=False)
    
    def generate_grafana_dashboard(self) -> Dict[str, Any]:
        """Gnre un dashboard Grafana basique"""
        dashboard = {
            "dashboard": {
                "id": None,
                "title": "Orchestrator Production Monitoring",
                "tags": ["orchestrator", "production"],
                "timezone": "UTC",
                "panels": [
                    {
                        "id": 1,
                        "title": "Request Rate",
                        "type": "stat",
                        "targets": [{
                            "expr": "rate(orchestrator_requests_total[5m])",
                            "legendFormat": "Requests/sec"
                        }],
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
                    },
                    {
                        "id": 2,
                        "title": "Error Rate",
                        "type": "stat",
                        "targets": [{
                            "expr": "rate(orchestrator_requests_total{status_code=~\"5..\"}[5m])",
                            "legendFormat": "Errors/sec"
                        }],
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
                    },
                    {
                        "id": 3,
                        "title": "Response Time",
                        "type": "graph",
                        "targets": [{
                            "expr": "histogram_quantile(0.95, rate(orchestrator_request_duration_seconds_bucket[5m]))",
                            "legendFormat": "95th percentile"
                        }, {
                            "expr": "histogram_quantile(0.50, rate(orchestrator_request_duration_seconds_bucket[5m]))",
                            "legendFormat": "50th percentile"
                        }],
                        "gridPos": {"h": 8, "w": 24, "x": 0, "y": 8}
                    },
                    {
                        "id": 4,
                        "title": "LLM Latency",
                        "type": "graph",
                        "targets": [{
                            "expr": "rate(orchestrator_llm_latency_seconds_sum[5m]) / rate(orchestrator_llm_latency_seconds_count[5m])",
                            "legendFormat": "Avg LLM Latency"
                        }],
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16}
                    },
                    {
                        "id": 5,
                        "title": "Active Sessions",
                        "type": "stat",
                        "targets": [{
                            "expr": "orchestrator_active_sessions",
                            "legendFormat": "Active Sessions"
                        }],
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16}
                    }
                ],
                "time": {"from": "now-1h", "to": "now"},
                "refresh": "30s"
            },
            "folderId": 0,
            "overwrite": True
        }
        
        return dashboard

    async def record_metric(self, metric_name: str, value: float, labels: Dict[str, str] = None):
        """Enregistre une mtrique gnrique de manire asynchrone"""
        try:
            if labels is None:
                labels = {}
            
            # Dtermine le type de mtrique bas sur le nom
            if "_total" in metric_name or "_count" in metric_name:
                self.increment_counter(metric_name, labels)
            elif "_seconds" in metric_name or "_latency" in metric_name or "_duration" in metric_name:
                self.observe_histogram(metric_name, value, labels)
            else:
                # Utiliser comme gauge par dfaut
                self.set_gauge(metric_name, value, labels)
        except Exception as e:
            logger.warning(f"Failed to record metric {metric_name}: {e}")


# Instance globale
_monitoring_instance: Optional[ProductionMonitoring] = None


def get_monitoring() -> ProductionMonitoring:
    """Retourne l'instance globale de monitoring"""
    global _monitoring_instance
    
    if _monitoring_instance is None:
        _monitoring_instance = ProductionMonitoring()
    
    return _monitoring_instance


# Dcorateur pour tracking automatique
def track_request_metrics(endpoint: str):
    """Dcorateur pour tracker automatiquement les mtriques de requte"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            monitoring = get_monitoring()
            
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Dterminer le status code
                status_code = getattr(result, 'status_code', 200)
                
                monitoring.track_request(
                    method="POST",  # Ajustable selon la mthode
                    endpoint=endpoint,
                    status_code=status_code,
                    duration=duration
                )
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                monitoring.track_request(
                    method="POST",
                    endpoint=endpoint,
                    status_code=500,
                    duration=duration
                )
                raise
        
        return wrapper
    return decorator


# Export de l'instance globale pour compatibilit
monitoring_manager = get_monitoring()
