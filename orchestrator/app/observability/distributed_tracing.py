"""
Distributed Tracing Implementation for NextGeneration Orchestrator
IA-2 Architecture & Production - Sprint 1.3

Advanced observability with OpenTelemetry and Jaeger integration
for production-grade monitoring and performance analysis.
"""

import sys
from pathlib import Path
from core import logging_manager
import time
from typing import Dict, Optional, Any, List
from contextlib import asynccontextmanager
from dataclasses import dataclass, asdict
from datetime import datetime

from opentelemetry import trace, baggage, propagate
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.propagators.jaeger import JaegerPropagator
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

# LoggingManager NextGeneration - Tool/Utility
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = logging_manager.get_logger(custom_config={
            "logger_name": "class",
            "log_level": "INFO",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": True
        })

@dataclass
class TraceMetrics:
    """Trace performance metrics for monitoring"""
    trace_id: str
    span_id: str
    operation_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    status: str = "started"
    error_message: Optional[str] = None
    custom_attributes: Dict[str, Any] = None

class DistributedTracer:
    """
    Production-grade distributed tracing implementation
    
    Features:
    - OpenTelemetry integration
    - Jaeger export
    - Automatic instrumentation
    - Custom span management
    - Performance metrics
    - Error tracking
    """
    
    def __init__(
        self,
        service_name: str = "nextgeneration-orchestrator",
        jaeger_endpoint: str = "http://jaeger-collector:14268/api/traces",
        environment: str = "production"
    ):
        self.service_name = service_name
        self.jaeger_endpoint = jaeger_endpoint
        self.environment = environment
        self.tracer_provider: Optional[TracerProvider] = None
        self.tracer: Optional[trace.Tracer] = None
        self.active_traces: Dict[str, TraceMetrics] = {}
        self._setup_tracing()
    
    def _setup_tracing(self) -> None:
        """Initialize OpenTelemetry tracing configuration"""
        try:
            # Resource configuration
            resource = Resource.create({
                ResourceAttributes.SERVICE_NAME: self.service_name,
                ResourceAttributes.SERVICE_VERSION: "1.3.0",
                ResourceAttributes.DEPLOYMENT_ENVIRONMENT: self.environment,
                "service.instance.id": f"{self.service_name}-{time.time()}",
            })
            
            # Tracer provider setup
            self.tracer_provider = TracerProvider(resource=resource)
            trace.set_tracer_provider(self.tracer_provider)
            
            # Jaeger exporter
            jaeger_exporter = JaegerExporter(
                endpoint=self.jaeger_endpoint,
                collector_endpoint=self.jaeger_endpoint,
            )
            
            # Span processor
            span_processor = BatchSpanProcessor(
                jaeger_exporter,
                max_queue_size=2048,
                max_export_batch_size=512,
                export_timeout_millis=30000,
                schedule_delay_millis=5000,
            )
            
            self.tracer_provider.add_span_processor(span_processor)
            
            # Setup propagator
            propagate.set_global_textmap(JaegerPropagator())
            
            # Get tracer
            self.tracer = trace.get_tracer(
                __name__,
                version="1.3.0",
                tracer_provider=self.tracer_provider
            )
            
            logger.info(f"Distributed tracing initialized for {self.service_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize tracing: {e}")
            raise
    
    def instrument_applications(self) -> None:
        """Auto-instrument common libraries"""
        try:
            # FastAPI instrumentation
            FastAPIInstrumentor.instrument()
            
            # Database instrumentation
            AsyncPGInstrumentor.instrument()
            
            # Redis instrumentation  
            RedisInstrumentor.instrument()
            
            # HTTP requests instrumentation
            RequestsInstrumentor.instrument()
            
            logger.info("Auto-instrumentation enabled for all supported libraries")
            
        except Exception as e:
            logger.error(f"Failed to setup auto-instrumentation: {e}")
    
    @asynccontextmanager
    async def trace_operation(
        self,
        operation_name: str,
        attributes: Optional[Dict[str, Any]] = None,
        baggage_items: Optional[Dict[str, str]] = None
    ):
        """
        Context manager for tracing operations
        
        Args:
            operation_name: Name of the operation being traced
            attributes: Custom attributes to add to span
            baggage_items: Baggage items for cross-service context
        """
        if not self.tracer:
            yield None
            return
        
        # Set baggage if provided
        if baggage_items:
            for key, value in baggage_items.items():
                baggage.set_baggage(key, value)
        
        # Start span
        with self.tracer.start_as_current_span(operation_name) as span:
            trace_id = format(span.get_span_context().trace_id, '032x')
            span_id = format(span.get_span_context().span_id, '016x')
            
            # Add custom attributes
            if attributes:
                for key, value in attributes.items():
                    span.set_attribute(key, str(value))
            
            # Add standard attributes
            span.set_attribute("service.environment", self.environment)
            span.set_attribute("service.version", "1.3.0")
            
            # Track metrics
            trace_metrics = TraceMetrics(
                trace_id=trace_id,
                span_id=span_id,
                operation_name=operation_name,
                start_time=datetime.utcnow(),
                custom_attributes=attributes or {}
            )
            
            self.active_traces[trace_id] = trace_metrics
            
            try:
                logger.info(f"Started trace: {operation_name} [trace_id={trace_id}]")
                yield span
                
                # Mark as successful
                span.set_attribute("operation.success", True)
                trace_metrics.status = "completed"
                
            except Exception as e:
                # Record exception
                span.record_exception(e)
                span.set_attribute("operation.success", False)
                span.set_attribute("error.message", str(e))
                
                trace_metrics.status = "error"
                trace_metrics.error_message = str(e)
                
                logger.error(f"Trace error in {operation_name}: {e}")
                raise
                
            finally:
                # Calculate duration
                end_time = datetime.utcnow()
                duration = (end_time - trace_metrics.start_time).total_seconds() * 1000
                
                trace_metrics.end_time = end_time
                trace_metrics.duration_ms = duration
                
                span.set_attribute("operation.duration_ms", duration)
                
                logger.info(
                    f"Completed trace: {operation_name} "
                    f"[duration={duration:.2f}ms, status={trace_metrics.status}]"
                )
    
    def get_current_trace_context(self) -> Optional[Dict[str, str]]:
        """Get current trace context for propagation"""
        try:
            span = trace.get_current_span()
            if span and span.is_recording():
                context = span.get_span_context()
                return {
                    "trace_id": format(context.trace_id, '032x'),
                    "span_id": format(context.span_id, '016x'),
                    "trace_flags": format(context.trace_flags, '02x')
                }
        except Exception as e:
            logger.error(f"Failed to get trace context: {e}")
        
        return None
    
    def inject_trace_context(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Inject trace context into HTTP headers"""
        try:
            propagate.inject(headers)
            return headers
        except Exception as e:
            logger.error(f"Failed to inject trace context: {e}")
            return headers
    
    def extract_trace_context(self, headers: Dict[str, str]) -> Any:
        """Extract trace context from HTTP headers"""
        try:
            return propagate.extract(headers)
        except Exception as e:
            logger.error(f"Failed to extract trace context: {e}")
            return None
    
    def add_span_event(
        self,
        name: str,
        attributes: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ) -> None:
        """Add event to current span"""
        try:
            span = trace.get_current_span()
            if span and span.is_recording():
                event_attributes = attributes or {}
                event_timestamp = timestamp or datetime.utcnow()
                
                span.add_event(
                    name,
                    event_attributes,
                    timestamp=int(event_timestamp.timestamp() * 1_000_000_000)
                )
                
        except Exception as e:
            logger.error(f"Failed to add span event: {e}")
    
    def get_trace_metrics(self) -> List[Dict[str, Any]]:
        """Get performance metrics for all traces"""
        return [asdict(metrics) for metrics in self.active_traces.values()]
    
    def get_active_traces_count(self) -> int:
        """Get count of currently active traces"""
        active_count = sum(
            1 for trace in self.active_traces.values()
            if trace.status == "started"
        )
        return active_count
    
    def cleanup_completed_traces(self, max_age_minutes: int = 60) -> None:
        """Clean up old completed traces from memory"""
        cutoff_time = datetime.utcnow().timestamp() - (max_age_minutes * 60)
        
        completed_traces = [
            trace_id for trace_id, trace in self.active_traces.items()
            if (trace.end_time and 
                trace.end_time.timestamp() < cutoff_time and
                trace.status in ["completed", "error"])
        ]
        
        for trace_id in completed_traces:
            del self.active_traces[trace_id]
        
        if completed_traces:
            logger.info(f"Cleaned up {len(completed_traces)} completed traces")
    
    def shutdown(self) -> None:
        """Gracefully shutdown tracing"""
        try:
            if self.tracer_provider:
                self.tracer_provider.shutdown()
            logger.info("Distributed tracing shutdown completed")
        except Exception as e:
            logger.error(f"Error during tracing shutdown: {e}")

# Global tracer instance
_global_tracer: Optional[DistributedTracer] = None

def get_tracer() -> DistributedTracer:
    """Get global tracer instance"""
    global _global_tracer
    if _global_tracer is None:
        _global_tracer = DistributedTracer()
        _global_tracer.instrument_applications()
    return _global_tracer

def initialize_tracing(
    service_name: str = "nextgeneration-orchestrator",
    jaeger_endpoint: str = "http://jaeger-collector:14268/api/traces",
    environment: str = "production"
) -> DistributedTracer:
    """Initialize distributed tracing for the application"""
    global _global_tracer
    _global_tracer = DistributedTracer(
        service_name=service_name,
        jaeger_endpoint=jaeger_endpoint,
        environment=environment
    )
    _global_tracer.instrument_applications()
    return _global_tracer

# Convenience decorators
def trace_async_function(operation_name: Optional[str] = None):
    """Decorator for tracing async functions"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            tracer = get_tracer()
            op_name = operation_name or f"{func.__module__}.{func.__name__}"
            
            async with tracer.trace_operation(op_name):
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator

def trace_function(operation_name: Optional[str] = None):
    """Decorator for tracing sync functions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            tracer = get_tracer()
            op_name = operation_name or f"{func.__module__}.{func.__name__}"
            
            with tracer.tracer.start_as_current_span(op_name):
                return func(*args, **kwargs)
        
        return wrapper
    return decorator




