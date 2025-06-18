"""
Advanced Business Metrics Implementation for NextGeneration Orchestrator
IA-2 Architecture & Production - Sprint 1.3

Production-grade business metrics with custom Prometheus metrics,
KPI tracking, and executive dashboard support.
"""

import logging
import time
from typing import Dict, Optional, Any, List, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import asyncio
from collections import defaultdict, deque

from prometheus_client import (
    Counter, Histogram, Gauge, Summary, Info,
    CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
)

logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Business metric types"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

@dataclass
class BusinessKPI:
    """Business KPI definition"""
    name: str
    description: str
    target_value: float
    current_value: float
    unit: str
    trend: str = "stable"  # up, down, stable
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.utcnow()

@dataclass
class UserSessionMetrics:
    """User session performance metrics"""
    user_id: str
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time_ms: float = 0.0
    satisfaction_score: Optional[float] = None
    revenue_generated: float = 0.0

class AdvancedBusinessMetrics:
    """
    Production-grade business metrics implementation
    
    Features:
    - Custom Prometheus metrics
    - KPI tracking and alerting
    - User satisfaction scoring
    - Revenue tracking
    - Performance correlation
    - Executive dashboards
    """
    
    def __init__(self, registry: Optional[CollectorRegistry] = None):
        self.registry = registry or CollectorRegistry()
        self.active_sessions: Dict[str, UserSessionMetrics] = {}
        self.kpis: Dict[str, BusinessKPI] = {}
        self._setup_prometheus_metrics()
        self._initialize_kpis()
        
        logger.info("Advanced business metrics initialized")
    
    def _setup_prometheus_metrics(self) -> None:
        """Setup custom Prometheus metrics for business intelligence"""
        
        # Request metrics
        self.requests_total = Counter(
            'orchestrator_requests_total',
            'Total number of requests processed',
            ['method', 'endpoint', 'status', 'user_tier'],
            registry=self.registry
        )
        
        self.request_duration = Histogram(
            'orchestrator_request_duration_seconds',
            'Request duration in seconds',
            ['endpoint', 'user_tier'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
            registry=self.registry
        )
        
        # LLM and AI metrics
        self.llm_requests_total = Counter(
            'orchestrator_llm_requests_total',
            'Total LLM requests by provider and model',
            ['provider', 'model', 'status'],
            registry=self.registry
        )
        
        self.llm_latency = Histogram(
            'orchestrator_llm_latency_seconds',
            'LLM request latency in seconds',
            ['provider', 'model'],
            buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
            registry=self.registry
        )
        
        self.llm_token_usage = Counter(
            'orchestrator_llm_tokens_total',
            'Total tokens consumed by LLM requests',
            ['provider', 'model', 'type'],  # type: input, output
            registry=self.registry
        )
        
        # Session and user metrics
        self.active_sessions = Gauge(
            'orchestrator_active_sessions',
            'Number of active user sessions',
            registry=self.registry
        )
        
        self.user_satisfaction_score = Histogram(
            'orchestrator_user_satisfaction_score',
            'User satisfaction scores (1-10)',
            buckets=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            registry=self.registry
        )
        
        self.session_duration = Histogram(
            'orchestrator_session_duration_seconds',
            'User session duration in seconds',
            ['user_tier'],
            buckets=[60, 300, 900, 1800, 3600, 7200, 14400],
            registry=self.registry
        )
        
        # Business metrics
        self.revenue_generated = Counter(
            'orchestrator_revenue_generated_total',
            'Total revenue generated in USD',
            ['user_tier', 'service_type'],
            registry=self.registry
        )
        
        self.conversion_rate = Gauge(
            'orchestrator_conversion_rate',
            'Conversion rate from trial to paid',
            registry=self.registry
        )
        
        self.cost_per_request = Gauge(
            'orchestrator_cost_per_request',
            'Average cost per request in USD',
            ['service_type'],
            registry=self.registry
        )
        
        # Error and quality metrics
        self.error_rate = Gauge(
            'orchestrator_error_rate',
            'Error rate percentage',
            ['service_type'],
            registry=self.registry
        )
        
        self.quality_score = Gauge(
            'orchestrator_quality_score',
            'Overall service quality score (0-100)',
            registry=self.registry
        )
        
        # Infrastructure impact metrics
        self.infrastructure_cost = Gauge(
            'orchestrator_infrastructure_cost_hourly',
            'Infrastructure cost per hour in USD',
            ['environment'],
            registry=self.registry
        )
        
        self.resource_efficiency = Gauge(
            'orchestrator_resource_efficiency',
            'Resource efficiency ratio (0-1)',
            ['resource_type'],  # cpu, memory, network
            registry=self.registry
        )
    
    def _initialize_kpis(self) -> None:
        """Initialize business KPIs with targets"""
        self.kpis = {
            "monthly_active_users": BusinessKPI(
                name="Monthly Active Users",
                description="Number of unique users per month",
                target_value=10000,
                current_value=0,
                unit="users"
            ),
            "average_response_time": BusinessKPI(
                name="Average Response Time",
                description="Average API response time",
                target_value=200,  # ms
                current_value=0,
                unit="ms"
            ),
            "user_satisfaction": BusinessKPI(
                name="User Satisfaction Score",
                description="Average user satisfaction (1-10)",
                target_value=8.5,
                current_value=0,
                unit="score"
            ),
            "monthly_revenue": BusinessKPI(
                name="Monthly Recurring Revenue",
                description="Monthly recurring revenue in USD",
                target_value=100000,
                current_value=0,
                unit="USD"
            ),
            "conversion_rate": BusinessKPI(
                name="Trial to Paid Conversion",
                description="Conversion rate from trial to paid",
                target_value=15.0,  # percentage
                current_value=0,
                unit="%"
            ),
            "system_uptime": BusinessKPI(
                name="System Uptime",
                description="System availability percentage",
                target_value=99.9,
                current_value=0,
                unit="%"
            ),
            "cost_per_user": BusinessKPI(
                name="Cost Per User",
                description="Average cost per active user",
                target_value=5.0,
                current_value=0,
                unit="USD"
            )
        }
    
    def track_request(
        self,
        method: str,
        endpoint: str,
        status: str,
        duration_seconds: float,
        user_tier: str = "free",
        user_id: Optional[str] = None
    ) -> None:
        """Track API request metrics"""
        try:
            # Update Prometheus metrics
            self.requests_total.labels(
                method=method,
                endpoint=endpoint,
                status=status,
                user_tier=user_tier
            ).inc()
            
            self.request_duration.labels(
                endpoint=endpoint,
                user_tier=user_tier
            ).observe(duration_seconds)
            
            # Update session metrics if user provided
            if user_id and user_id in self.active_sessions:
                session = self.active_sessions[user_id]
                session.total_requests += 1
                
                if status.startswith('2'):  # 2xx success
                    session.successful_requests += 1
                else:
                    session.failed_requests += 1
                
                # Update average response time
                total_time = session.avg_response_time_ms * (session.total_requests - 1)
                session.avg_response_time_ms = (
                    total_time + duration_seconds * 1000
                ) / session.total_requests
            
        except Exception as e:
            logger.error(f"Error tracking request metrics: {e}")
    
    def track_llm_request(
        self,
        provider: str,
        model: str,
        status: str,
        latency_seconds: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost_usd: float = 0.0
    ) -> None:
        """Track LLM request metrics"""
        try:
            self.llm_requests_total.labels(
                provider=provider,
                model=model,
                status=status
            ).inc()
            
            self.llm_latency.labels(
                provider=provider,
                model=model
            ).observe(latency_seconds)
            
            if input_tokens > 0:
                self.llm_token_usage.labels(
                    provider=provider,
                    model=model,
                    type="input"
                ).inc(input_tokens)
            
            if output_tokens > 0:
                self.llm_token_usage.labels(
                    provider=provider,
                    model=model,
                    type="output"
                ).inc(output_tokens)
            
            # Update cost metrics
            if cost_usd > 0:
                self.cost_per_request.labels(
                    service_type="llm"
                ).set(cost_usd)
            
        except Exception as e:
            logger.error(f"Error tracking LLM metrics: {e}")
    
    def start_user_session(
        self,
        user_id: str,
        session_id: str,
        user_tier: str = "free"
    ) -> None:
        """Start tracking user session"""
        try:
            session = UserSessionMetrics(
                user_id=user_id,
                session_id=session_id,
                start_time=datetime.utcnow()
            )
            
            self.active_sessions[session_id] = session
            self.active_sessions.set(len(self.active_sessions))
            
            logger.info(f"Started session tracking for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error starting session tracking: {e}")
    
    def end_user_session(
        self,
        session_id: str,
        satisfaction_score: Optional[float] = None,
        revenue_generated: float = 0.0,
        user_tier: str = "free"
    ) -> None:
        """End user session and record metrics"""
        try:
            if session_id not in self.active_sessions:
                logger.warning(f"Session {session_id} not found in active sessions")
                return
            
            session = self.active_sessions[session_id]
            session.end_time = datetime.utcnow()
            session.satisfaction_score = satisfaction_score
            session.revenue_generated = revenue_generated
            
            # Calculate session duration
            duration_seconds = (session.end_time - session.start_time).total_seconds()
            
            # Update Prometheus metrics
            self.session_duration.labels(user_tier=user_tier).observe(duration_seconds)
            
            if satisfaction_score:
                self.user_satisfaction_score.observe(satisfaction_score)
            
            if revenue_generated > 0:
                self.revenue_generated.labels(
                    user_tier=user_tier,
                    service_type="api"
                ).inc(revenue_generated)
            
            # Remove from active sessions
            del self.active_sessions[session_id]
            self.active_sessions.set(len(self.active_sessions))
            
            logger.info(
                f"Ended session {session_id}: "
                f"duration={duration_seconds:.1f}s, "
                f"requests={session.total_requests}, "
                f"satisfaction={satisfaction_score}"
            )
            
        except Exception as e:
            logger.error(f"Error ending session tracking: {e}")
    
    def update_kpi(
        self,
        kpi_name: str,
        current_value: float,
        trend: Optional[str] = None
    ) -> None:
        """Update business KPI"""
        try:
            if kpi_name not in self.kpis:
                logger.warning(f"KPI {kpi_name} not found")
                return
            
            kpi = self.kpis[kpi_name]
            previous_value = kpi.current_value
            kpi.current_value = current_value
            kpi.last_updated = datetime.utcnow()
            
            # Calculate trend if not provided
            if trend is None:
                if current_value > previous_value:
                    kpi.trend = "up"
                elif current_value < previous_value:
                    kpi.trend = "down"
                else:
                    kpi.trend = "stable"
            else:
                kpi.trend = trend
            
            logger.info(
                f"Updated KPI {kpi_name}: {previous_value}  {current_value} "
                f"(target: {kpi.target_value}, trend: {kpi.trend})"
            )
            
        except Exception as e:
            logger.error(f"Error updating KPI {kpi_name}: {e}")
    
    def get_kpi_dashboard(self) -> Dict[str, Any]:
        """Get KPI dashboard data"""
        dashboard_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "kpis": {},
            "summary": {
                "total_kpis": len(self.kpis),
                "kpis_on_target": 0,
                "kpis_above_target": 0,
                "kpis_below_target": 0
            }
        }
        
        for name, kpi in self.kpis.items():
            kpi_data = asdict(kpi)
            kpi_data["last_updated"] = kpi.last_updated.isoformat()
            
            # Calculate performance vs target
            if kpi.target_value > 0:
                performance_ratio = kpi.current_value / kpi.target_value
                kpi_data["performance_ratio"] = performance_ratio
                
                if performance_ratio >= 1.0:
                    kpi_data["status"] = "on_target"
                    dashboard_data["summary"]["kpis_on_target"] += 1
                elif performance_ratio >= 0.9:
                    kpi_data["status"] = "near_target"
                    dashboard_data["summary"]["kpis_on_target"] += 1
                else:
                    kpi_data["status"] = "below_target"
                    dashboard_data["summary"]["kpis_below_target"] += 1
            else:
                kpi_data["performance_ratio"] = 1.0
                kpi_data["status"] = "unknown"
            
            dashboard_data["kpis"][name] = kpi_data
        
        return dashboard_data
    
    def get_user_analytics(self) -> Dict[str, Any]:
        """Get user analytics summary"""
        active_sessions_count = len(self.active_sessions)
        
        # Calculate session statistics
        if self.active_sessions:
            avg_requests = sum(
                s.total_requests for s in self.active_sessions.values()
            ) / active_sessions_count
            
            avg_success_rate = sum(
                s.successful_requests / max(s.total_requests, 1) 
                for s in self.active_sessions.values()
            ) / active_sessions_count
            
            avg_response_time = sum(
                s.avg_response_time_ms for s in self.active_sessions.values()
            ) / active_sessions_count
        else:
            avg_requests = 0
            avg_success_rate = 0
            avg_response_time = 0
        
        return {
            "active_sessions": active_sessions_count,
            "avg_requests_per_session": round(avg_requests, 2),
            "avg_success_rate": round(avg_success_rate * 100, 2),
            "avg_response_time_ms": round(avg_response_time, 2),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_prometheus_metrics(self) -> str:
        """Get Prometheus metrics in text format"""
        return generate_latest(self.registry).decode('utf-8')
    
    def get_executive_summary(self) -> Dict[str, Any]:
        """Get executive summary for leadership dashboard"""
        kpi_dashboard = self.get_kpi_dashboard()
        user_analytics = self.get_user_analytics()
        
        # Calculate health score
        on_target = kpi_dashboard["summary"]["kpis_on_target"]
        total_kpis = kpi_dashboard["summary"]["total_kpis"]
        health_score = (on_target / total_kpis * 100) if total_kpis > 0 else 0
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "health_score": round(health_score, 1),
            "key_metrics": {
                "monthly_active_users": self.kpis.get("monthly_active_users", {}).current_value,
                "monthly_revenue": self.kpis.get("monthly_revenue", {}).current_value,
                "user_satisfaction": self.kpis.get("user_satisfaction", {}).current_value,
                "system_uptime": self.kpis.get("system_uptime", {}).current_value,
                "active_sessions": user_analytics["active_sessions"],
                "avg_response_time": user_analytics["avg_response_time_ms"]
            },
            "trends": {
                name: kpi.trend for name, kpi in self.kpis.items()
            },
            "alerts": [
                f"KPI '{name}' below target: {kpi.current_value} < {kpi.target_value}"
                for name, kpi in self.kpis.items()
                if kpi.current_value < kpi.target_value * 0.9
            ]
        }

# Global metrics instance
_global_metrics: Optional[AdvancedBusinessMetrics] = None

def get_business_metrics() -> AdvancedBusinessMetrics:
    """Get global business metrics instance"""
    global _global_metrics
    if _global_metrics is None:
        _global_metrics = AdvancedBusinessMetrics()
    return _global_metrics

def initialize_business_metrics() -> AdvancedBusinessMetrics:
    """Initialize business metrics system"""
    global _global_metrics
    _global_metrics = AdvancedBusinessMetrics()
    return _global_metrics
