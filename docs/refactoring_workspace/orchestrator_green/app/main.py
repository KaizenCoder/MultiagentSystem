from __future__ import annotations
import asyncio, json, uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional, List

import httpx
from fastapi import Depends, FastAPI, HTTPException, Security, Request
from fastapi.responses import StreamingResponse, Response
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from langgraph.graph import END, StateGraph
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field, validator

from orchestrator.app.agents.supervisor import supervisor
from orchestrator.app.agents.workers import worker_node_wrapper
from orchestrator.app.agents.tools import close_http_client
from orchestrator.app.checkpoint.api_checkpointer import ApiCheckpointer
from orchestrator.app.config import settings
from orchestrator.app.graph.state import AgentState, Feedback
from orchestrator.app.security.validators import InputSanitizer
from orchestrator.app.security.logging import security_logger, AuditLogger, AuditEventType, setup_secure_logging
from orchestrator.app.security.secrets_manager import get_secrets_manager
from orchestrator.app.performance.redis_cache import get_cache, CacheType
from orchestrator.app.observability.monitoring import get_monitoring, track_request_metrics
from orchestrator.app.security.network_security import get_network_security
from orchestrator.app.performance.database_optimizer import get_database_manager
from orchestrator.app.performance.redis_cluster_manager import get_redis_cluster_manager
from orchestrator.app.performance.load_tester import get_load_tester

# Sprint 1.3 - Advanced Observability & Scalability
from orchestrator.app.observability.distributed_tracing import get_tracer, initialize_tracing
from orchestrator.app.performance.circuit_breaker import get_circuit_manager, CircuitBreakerConfig
from orchestrator.app.observability.business_metrics import get_business_metrics, initialize_business_metrics

# Sprint 2.1 - Advanced Architecture & Performance
from orchestrator.app.performance.memory_optimizer import get_memory_optimizer
from orchestrator.app.agents.advanced_state_manager import get_advanced_state_manager
from orchestrator.app.agents.advanced_coordination import get_advanced_coordination, AgentTask, AgentPriority, ResourceType

# Sprint 2.2 - Load Balancing & Auto-Scaling Enterprise
from orchestrator.app.performance.load_balancer import get_load_balancer, BackendServer, LoadBalancingAlgorithm, HealthCheckConfig
from orchestrator.app.performance.auto_scaler import get_auto_scaler, setup_production_scaling, ScalingRule, ScalingMetric

# --- State & Config ---
workflow_app = None
limiter = Limiter(key_func=get_remote_address)
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)
http_client = None

# --- Lifespan Manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialiser le logging scuris
    setup_secure_logging()
    
    global workflow_app, http_client
    http_client = httpx.AsyncClient()
    for attempt in range(5):
        try:
            workflow_app = create_workflow(http_client)
            security_logger.log_security_event("SYSTEM_STARTUP", {
                "component": "orchestrator",
                "status": "success"
            })
            print("[lifespan] Workflow compiled successfully ")
            break
        except httpx.RequestError as e:
            wait_time = 2 ** attempt
            security_logger.log_error("Memory API connection failed", e, include_details=settings.DEBUG)
            print(f"[lifespan] Memory API unreachable. Retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)
    else:
        security_logger.log_error("FATAL: Could not connect to Memory API", Exception("Connection failed"))
        print("[lifespan] FATAL: Could not connect to Memory API.")
        workflow_app = None
    
    # Initialize performance components
    try:
        # Initialize database manager
        db_manager = get_database_manager()
        await db_manager.initialize()
        print("[lifespan] Database manager initialized ")
        
        # Initialize Redis cluster manager
        redis_manager = get_redis_cluster_manager()
        await redis_manager.initialize()
        print("[lifespan] Redis cluster manager initialized ")
        
        # Initialize load tester
        load_tester = get_load_tester()
        print("[lifespan] Load tester initialized ")
          # Sprint 1.3 - Initialize advanced observability
        tracer = initialize_tracing(
            service_name="nextgeneration-orchestrator",
            environment=settings.ENVIRONMENT
        )
        print("[lifespan] Distributed tracing initialized ")
        
        # Initialize business metrics
        business_metrics = initialize_business_metrics()
        print("[lifespan] Business metrics initialized ")
        
        # Initialize circuit breaker manager
        circuit_manager = get_circuit_manager()
        print("[lifespan] Circuit breaker manager initialized ")
        
        # Sprint 2.1 - Initialize advanced architecture components
        memory_optimizer = get_memory_optimizer()
        await memory_optimizer.initialize()
        print("[lifespan] Memory optimizer initialized ")
        
        state_manager = get_advanced_state_manager()
        await state_manager.initialize()
        print("[lifespan] Advanced state manager initialized ")
        
        coordination = get_advanced_coordination()
        await coordination.initialize()
        print("[lifespan] Advanced agent coordination initialized ")
        
    except Exception as e:
        security_logger.log_error("Performance components initialization failed", e)
        print(f"[lifespan] WARNING: Performance components failed to initialize: {e}")

    Instrumentator().instrument(app).expose(app)
    yield
    
    # CORRECTIF 4: Fermeture propre du client HTTP
    if http_client:
        await http_client.aclose()
        print("[lifespan] HTTP client closed.")
    await close_http_client()  # Ferme le client global des tools
    
    # Clean shutdown of performance components
    try:
        db_manager = get_database_manager()
        await db_manager.close()
        print("[lifespan] Database manager closed.")
        
        redis_manager = get_redis_cluster_manager()
        await redis_manager.close()
        print("[lifespan] Redis cluster manager closed.")
          # Sprint 1.3 - Shutdown advanced observability
        tracer = get_tracer()
        tracer.shutdown()
        print("[lifespan] Distributed tracing shutdown completed.")
        
        # Sprint 2.1 - Shutdown advanced architecture components
        memory_optimizer = get_memory_optimizer()
        await memory_optimizer.close()
        print("[lifespan] Memory optimizer closed.")
        
        state_manager = get_advanced_state_manager()
        await state_manager.close()
        print("[lifespan] Advanced state manager closed.")
        
        coordination = get_advanced_coordination()
        await coordination.close()
        print("[lifespan] Advanced coordination closed.")
        
    except Exception as e:
        print(f"[lifespan] Error closing performance components: {e}")
    
    security_logger.log_security_event("SYSTEM_SHUTDOWN", {
        "component": "orchestrator",
        "status": "clean"
    })

# --- App Initialization ---
app = FastAPI(title="Multi-Agent Orchestrator", version="3.3-final", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- Middlewares de Scurit ---
# CORS scuris
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trusted-frontend.com"] if not settings.DEBUG else ["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Trusted hosts
allowed_hosts = ["localhost", "127.0.0.1", "orchestrator"]
if not settings.DEBUG:
    allowed_hosts.extend(["orchestrator.company.com"])
else:
    allowed_hosts.append("*")

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=allowed_hosts
)

# --- Dependencies & Security ---
def get_api_key(key: str = Security(api_key_header), request: Request = None):
    if key != settings.ORCHESTRATOR_API_KEY:
        # Log tentative d'accs non autoris
        client_ip = request.client.host if request else "unknown"
        AuditLogger.log_event(AuditEventType.API_ACCESS_DENIED, None, {
            "client_ip": client_ip,
            "endpoint": request.url.path if request else "unknown",
            "reason": "invalid_api_key"
        })
        security_logger.log_security_event("UNAUTHORIZED_ACCESS_ATTEMPT", {
            "client_ip": client_ip,
            "provided_key_prefix": key[:8] if key else "none"
        })
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Log accs autoris
    if request:
        client_ip = request.client.host
        AuditLogger.log_event(AuditEventType.API_ACCESS, None, {
            "client_ip": client_ip,
            "endpoint": request.url.path
        })
    
    return key

def require_workflow():
    if workflow_app is None: 
        raise HTTPException(503, "Service Unavailable: Orchestrator is not ready.")
    return workflow_app

# --- Pydantic Models Scuriss ---
class TaskRequest(BaseModel):
    task_description: str = Field(..., min_length=1, max_length=settings.MAX_TASK_DESCRIPTION_LENGTH)
    session_id: Optional[str] = Field(None, regex=r'^[a-f0-9-]{36}$')
    code_context: Optional[str] = Field(None, max_length=settings.MAX_CODE_SIZE)
    
    @validator('task_description')
    def validate_task_description(cls, v):
        if not v.strip():
            raise ValueError('Task description cannot be empty')
        return InputSanitizer.sanitize_task_description(v)
    
    @validator('session_id')
    def validate_session_id(cls, v):
        if v is not None:
            sanitized = InputSanitizer.sanitize_session_id(v)
            if sanitized is None:
                raise ValueError('Invalid session ID format')
            return sanitized
        return v
    
    @validator('code_context')
    def validate_code_context(cls, v):
        if v is not None:
            return InputSanitizer.sanitize_code_context(v)
        return v

class FeedbackRequest(Feedback):
    @validator('comment')
    def validate_comment(cls, v):
        if v is not None:
            return InputSanitizer.sanitize_task_description(v)
        return v

# --- Workflow Creation ---
def mark_as_completed(state: AgentState) -> dict:
    """Nud final pour marquer la tche comme termine."""
    state["task_status"] = "completed"
    return state

def create_workflow(client: httpx.AsyncClient):
    workflow = StateGraph(AgentState)
    workflow.add_node("supervisor", supervisor.route)
    workflow.add_node("code_generation", lambda s: worker_node_wrapper(s, "code_generation"))
    workflow.add_node("documentation", lambda s: worker_node_wrapper(s, "documentation"))
    workflow.add_node("finish", mark_as_completed)
    workflow.set_entry_point("supervisor")
    workflow.add_conditional_edges("supervisor", lambda x: x["next"], {
        "code_generation": "code_generation", 
        "documentation": "documentation", 
        "finish": "finish"
    })
    workflow.add_edge("code_generation", "supervisor")
    workflow.add_edge("documentation", "supervisor")
    workflow.add_edge("finish", END)
    return workflow.compile(checkpointer=ApiCheckpointer(client=client))

# --- Endpoints ---
@app.post("/invoke", tags=["Core"])
async def invoke(req: TaskRequest, request: Request, app_instance=Depends(require_workflow), _=Depends(get_api_key)):
    session_id = req.session_id or str(uuid.uuid4())
    
    # Log de cration de tche
    AuditLogger.log_task_event(AuditEventType.TASK_CREATED, session_id, {
        "client_ip": request.client.host,
        "task_description_length": len(req.task_description),
        "has_code_context": req.code_context is not None
    })
    
    # Cration de l'tat initial
    initial_state = AgentState(
        messages=[],
        plan=None,
        next="supervisor",
        results={},
        session_id=session_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        task_description=req.task_description,
        task_status="pending",
        code_context=req.code_context,
        working_memory=[],
        errors=[],
        logs=[],
        feedback=None
    )
    
    # CORRECTIF 5: Appel de supervisor.create_plan juste aprs construction de l'tat initial
    initial_state = supervisor.create_plan(initial_state)
    
    async def event_stream():
        try:
            config = {"configurable": {"thread_id": session_id}}
            async for chunk in app_instance.astream(initial_state, config):
                yield f"data: {json.dumps(chunk, default=str)}\n\n"
            
            # Log de fin de tche
            AuditLogger.log_task_event(AuditEventType.TASK_COMPLETED, session_id, {
                "client_ip": request.client.host
            })
            yield f"data: {json.dumps({'status': 'completed'})}\n\n"
        except Exception as e:
            # Log de l'erreur de manire scurise
            security_logger.log_error("Task execution failed", e, include_details=settings.DEBUG)
            AuditLogger.log_task_event(AuditEventType.TASK_FAILED, session_id, {
                "client_ip": request.client.host,
                "error_type": type(e).__name__
            })
            yield f"data: {json.dumps({'error': 'Task execution failed'})}\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/plain")

@app.get("/status/{session_id}", tags=["Core"])
async def status(session_id: str, request: Request, app_instance=Depends(require_workflow), _=Depends(get_api_key)):
    try:
        # Validation du session_id
        sanitized_session_id = InputSanitizer.sanitize_session_id(session_id)
        if not sanitized_session_id:
            raise HTTPException(400, "Invalid session ID format")
        
        state = await app_instance.aget_state({"configurable": {"thread_id": sanitized_session_id}})
        if not state: 
            raise HTTPException(404, "Session not found")
        
        # Log de l'accs au statut
        AuditLogger.log_event(AuditEventType.API_ACCESS, None, {
            "client_ip": request.client.host,
            "action": "status_check",
            "session_id": sanitized_session_id
        })
        
        # CORRECTIF 2: Retourne le dictionnaire directement sans .values
        return state
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log de l'erreur de manire scurise
        security_logger.log_error("Status check failed", e, include_details=settings.DEBUG)
        raise HTTPException(500, "Error retrieving status")

@app.post("/feedback/{session_id}", tags=["Core"])
@limiter.limit("50/minute")  # CORRECTIF 3: Ajout du rate-limit manquant
async def feedback(session_id: str, fb: FeedbackRequest, request: Request, app_instance=Depends(require_workflow), _=Depends(get_api_key)):
    try:
        # Validation du session_id
        sanitized_session_id = InputSanitizer.sanitize_session_id(session_id)
        if not sanitized_session_id:
            raise HTTPException(400, "Invalid session ID format")
        
        # Mise  jour de l'tat avec le feedback
        config = {"configurable": {"thread_id": sanitized_session_id}}
        current_state = await app_instance.aget_state(config)
        if not current_state:
            raise HTTPException(404, "Session not found")
        
        # Ajouter le feedback
        feedback_data = {"rating": fb.rating, "comment": fb.comment, "timestamp": datetime.now(timezone.utc).isoformat()}
        await app_instance.aupdate_state(config, {"feedback": feedback_data})
        
        # Log du feedback
        AuditLogger.log_event(AuditEventType.API_ACCESS, None, {
            "client_ip": request.client.host,
            "action": "feedback_submitted",
            "session_id": sanitized_session_id,
            "rating": fb.rating
        })
        
        return {"status": "success", "message": "Feedback recorded"}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log de l'erreur de manire scurise
        security_logger.log_error("Feedback recording failed", e, include_details=settings.DEBUG)
        raise HTTPException(500, "Error recording feedback")

@app.get("/health", tags=["Monitoring"])
async def health():
    """Health check endpoint avec vrifications dtailles"""
    monitoring = get_monitoring()
    cache = await get_cache()
    secrets_manager = get_secrets_manager()
    network_security = get_network_security()
    
    # Health checks dtaills
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "3.3-final",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "components": {}
    }
    
    # Check workflow
    if workflow_app:
        health_status["components"]["workflow"] = {"status": "healthy", "ready": True}
    else:
        health_status["components"]["workflow"] = {"status": "unhealthy", "ready": False}
        health_status["status"] = "degraded"
    
    # Check cache
    cache_health = await cache.health_check()
    health_status["components"]["cache"] = cache_health
    if cache_health["status"] != "healthy":
        health_status["status"] = "degraded"
    
    # Check secrets manager
    try:
        secrets_health = await secrets_manager.health_check()
        health_status["components"]["secrets"] = secrets_health
        if secrets_health["status"] != "healthy":
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["components"]["secrets"] = {"status": "unhealthy", "error": str(e)}
        health_status["status"] = "degraded"
    
    # Check network security
    network_metrics = network_security.get_security_metrics()
    health_status["components"]["network_security"] = {
        "status": "healthy",
        "blocked_ips": network_metrics["blocked_ips_count"],
        "security_level": network_metrics["security_level"]
    }
    
    # Excuter les health checks du monitoring
    monitoring_health = await monitoring.run_health_checks()
    health_status["components"]["monitoring"] = monitoring_health
    
    return health_status


@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Endpoint Prometheus pour mtriques"""
    monitoring = get_monitoring()
    return Response(
        content=monitoring.get_prometheus_metrics(),
        media_type="text/plain"
    )


@app.get("/business-metrics", tags=["Monitoring"])
async def business_metrics():
    """Mtriques business spcifiques"""
    monitoring = get_monitoring()
    
    # Rcuprer les mtriques cache
    cache = await get_cache()
    cache_metrics = await cache.get_metrics()
    
    # Rcuprer les mtriques secrets
    secrets_manager = get_secrets_manager()
    try:
        secrets_stats = secrets_manager.get_cache_stats()
    except:
        secrets_stats = {}
    
    # Combiner toutes les mtriques business
    business_data = {
        "cache_performance": cache_metrics,
        "secrets_usage": secrets_stats,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    return business_data


@app.get("/security-metrics", tags=["Monitoring"])
async def security_metrics():
    """Mtriques de scurit"""
    network_security = get_network_security()
    
    security_data = {
        "network_security": network_security.get_security_metrics(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Ajouter les mtriques de logs de scurit
    try:
        audit_trail = AuditLogger.get_recent_events(limit=100)
        security_events_count = len([e for e in audit_trail if e.get("event_type") in [
            AuditEventType.API_ACCESS_DENIED.value,
            AuditEventType.SECURITY_VIOLATION.value
        ]])
        
        security_data["recent_security_events"] = security_events_count
        security_data["total_audit_events"] = len(audit_trail)
    except:
        security_data["recent_security_events"] = 0
        security_data["total_audit_events"] = 0
    
    return security_data


@app.get("/monitoring/dashboard", tags=["Monitoring"])
async def monitoring_dashboard():
    """Gnre la configuration du dashboard Grafana"""
    monitoring = get_monitoring()
    return monitoring.generate_grafana_dashboard()


@app.get("/monitoring/alerts", tags=["Monitoring"])
async def monitoring_alerts():
    """Gnre la configuration des alertes Prometheus"""
    monitoring = get_monitoring()
    return Response(
        content=monitoring.generate_alert_rules_yaml(),
        media_type="text/yaml"
    )


@app.get("/cache/stats", tags=["Performance"])
async def cache_stats():
    """Statistiques dtailles du cache"""
    cache = await get_cache()
    return await cache.get_metrics()


@app.post("/cache/clear", tags=["Performance"])
async def clear_cache(
    cache_type: Optional[str] = None,
    api_key: str = Depends(get_api_key)
):
    """Vider le cache (avec authentification)"""
    cache = await get_cache()
    
    if cache_type:
        try:
            cache_type_enum = CacheType(cache_type)
            deleted = await cache.clear_by_type(cache_type_enum)
            return {"status": "success", "deleted_entries": deleted, "cache_type": cache_type}
        except ValueError:
            raise HTTPException(400, f"Invalid cache type: {cache_type}")
    else:
        success = await cache.clear_all()
        return {"status": "success" if success else "failed", "action": "clear_all"}


@app.get("/secrets/list", tags=["Security"])
async def list_secrets(
    include_values: bool = False,
    api_key: str = Depends(get_api_key)
):
    """Liste les secrets (admin seulement)"""
    if include_values:
        security_logger.log_security_event("SECRET_VALUES_REQUESTED", {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "warning": "Secret values were requested via API"
        })
    
    secrets_manager = get_secrets_manager()
    try:
        return await secrets_manager.list_secrets(include_values=include_values)
    except Exception as e:
        security_logger.log_error("Failed to list secrets", e)
        raise HTTPException(500, "Error listing secrets")


@app.post("/secrets/rotate", tags=["Security"])
async def rotate_secrets(
    force: bool = False,
    api_key: str = Depends(get_api_key)
):
    """Rotation manuelle des secrets"""
    secrets_manager = get_secrets_manager()
    try:
        results = await secrets_manager.rotate_secrets(force=force)
        
        security_logger.log_security_event("MANUAL_SECRET_ROTATION", {
            "forced": force,
            "results": results,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        return {"status": "success", "rotation_results": results}
    except Exception as e:
        security_logger.log_error("Manual secret rotation failed", e)
        raise HTTPException(500, "Error rotating secrets")


@app.get("/network/security-groups", tags=["Security"])
async def network_security_groups(api_key: str = Depends(get_api_key)):
    """Configuration des security groups"""
    network_security = get_network_security()
    return {
        "security_groups": {name: {
            "name": sg.name,
            "description": sg.description,
            "vpc_id": sg.vpc_id,
            "inbound_rules_count": len(sg.inbound_rules),
            "outbound_rules_count": len(sg.outbound_rules),
            "tags": sg.tags
        } for name, sg in network_security.security_groups.items()},
        "metrics": network_security.get_security_metrics()
    }


@app.post("/network/block-ip", tags=["Security"])
async def block_ip(
    ip_address: str,
    reason: str = "Manual block",
    api_key: str = Depends(get_api_key)
):
    """Bloquer une adresse IP"""
    network_security = get_network_security()
    
    # Validation de l'IP
    try:
        import ipaddress
        ipaddress.ip_address(ip_address)
    except ValueError:
        raise HTTPException(400, "Invalid IP address format")
    
    network_security.block_ip(ip_address, reason)
    
    return {
        "status": "success", 
        "message": f"IP {ip_address} blocked",
        "reason": reason
    }


@app.delete("/network/unblock-ip/{ip_address}", tags=["Security"])
async def unblock_ip(
    ip_address: str,
    api_key: str = Depends(get_api_key)
):
    """Dbloquer une adresse IP"""
    network_security = get_network_security()
    network_security.unblock_ip(ip_address)
    
    return {
        "status": "success",
        "message": f"IP {ip_address} unblocked"
    }


# Middleware pour tracking automatique des mtriques
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware pour tracker automatiquement les mtriques"""
    start_time = time.time()
    monitoring = get_monitoring()
    
    # Excuter la requte
    response = await call_next(request)
    
    # Calculer la dure
    duration = time.time() - start_time
    
    # Tracker les mtriques
    monitoring.track_request(
        method=request.method,
        endpoint=str(request.url.path),
        status_code=response.status_code,
        duration=duration,
        user_type="api"  # Pourrait tre dtermin par l'API key
    )
    
    # Ajouter headers de monitoring
    response.headers["X-Response-Time"] = f"{duration:.3f}s"
    response.headers["X-Instance-ID"] = os.getenv("HOSTNAME", "unknown")
    
    return response


# Ajout d'imports ncessaires en haut du fichier
import time
import os
from fastapi.responses import Response

# === DATABASE PERFORMANCE ENDPOINTS ===

@app.get("/database/health", tags=["Database"])
async def database_health(api_key: str = Depends(get_api_key)):
    """Health check complet de la base de donnes"""
    try:
        db_manager = get_database_manager()
        health_status = await db_manager.health_check()
        return health_status
    except Exception as e:
        raise HTTPException(500, f"Database health check failed: {str(e)}")


@app.get("/database/metrics", tags=["Database"])
async def database_metrics(api_key: str = Depends(get_api_key)):
    """Mtriques de performance de la base de donnes"""
    try:
        db_manager = get_database_manager()
        
        # Get metrics for primary and replicas
        primary_metrics = await db_manager.get_performance_metrics()
        
        metrics = {
            "primary": {
                "active_connections": primary_metrics.active_connections,
                "idle_connections": primary_metrics.idle_connections,
                "total_connections": primary_metrics.total_connections,
                "avg_query_time": primary_metrics.avg_query_time,
                "slow_queries_count": primary_metrics.slow_queries_count,
                "buffer_hit_ratio": primary_metrics.buffer_hit_ratio,
                "index_usage_ratio": primary_metrics.index_usage_ratio,
                "last_vacuum": primary_metrics.last_vacuum.isoformat() if primary_metrics.last_vacuum else None,
                "last_analyze": primary_metrics.last_analyze.isoformat() if primary_metrics.last_analyze else None
            }
        }
        
        # Add replica metrics if available
        if db_manager.read_replicas:
            from orchestrator.app.performance.database_optimizer import DatabaseRole
            replica_metrics = await db_manager.get_performance_metrics(DatabaseRole.READ_REPLICA)
            metrics["read_replica"] = {
                "active_connections": replica_metrics.active_connections,
                "idle_connections": replica_metrics.idle_connections,
                "avg_query_time": replica_metrics.avg_query_time,
                "buffer_hit_ratio": replica_metrics.buffer_hit_ratio
            }
        
        return metrics
        
    except Exception as e:
        raise HTTPException(500, f"Error getting database metrics: {str(e)}")


@app.post("/database/optimize", tags=["Database"])
async def optimize_database(api_key: str = Depends(get_api_key)):
    """Optimiser la base de donnes (VACUUM, ANALYZE, REINDEX)"""
    try:
        db_manager = get_database_manager()
        results = await db_manager.optimize_database()
        return {
            "status": "success",
            "results": results,
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(500, f"Database optimization failed: {str(e)}")


@app.post("/database/backup", tags=["Database"])
async def backup_database(api_key: str = Depends(get_api_key)):
    """Crer une sauvegarde de la base de donnes"""
    try:
        db_manager = get_database_manager()
        backup_result = await db_manager.backup_database()
        return backup_result
    except Exception as e:
        raise HTTPException(500, f"Database backup failed: {str(e)}")


@app.get("/database/pgbouncer/stats", tags=["Database"])
async def pgbouncer_stats(api_key: str = Depends(get_api_key)):
    """Statistiques PgBouncer"""
    try:
        db_manager = get_database_manager()
        stats = await db_manager.pgbouncer.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(500, f"Error getting PgBouncer stats: {str(e)}")


# === REDIS CLUSTER ENDPOINTS ===

@app.get("/redis/cluster/status", tags=["Cache"])
async def redis_cluster_status(api_key: str = Depends(get_api_key)):
    """tat complet du cluster Redis"""
    try:
        redis_manager = get_redis_cluster_manager()
        status = await redis_manager.get_cluster_status()
        return status
    except Exception as e:
        raise HTTPException(500, f"Error getting Redis cluster status: {str(e)}")


@app.post("/redis/cluster/optimize", tags=["Cache"])
async def optimize_redis_cluster(api_key: str = Depends(get_api_key)):
    """Optimiser le cluster Redis"""
    try:
        redis_manager = get_redis_cluster_manager()
        results = await redis_manager.optimize_cluster()
        return results
    except Exception as e:
        raise HTTPException(500, f"Redis cluster optimization failed: {str(e)}")


@app.post("/redis/cache/warmup", tags=["Cache"])
async def warmup_redis_cache(
    patterns: Optional[List[str]] = None,
    api_key: str = Depends(get_api_key)
):
    """Prchauffer le cache Redis"""
    try:
        redis_manager = get_redis_cluster_manager()
        warmup_result = await redis_manager.warmup_cache(patterns)
        return warmup_result
    except Exception as e:
        raise HTTPException(500, f"Cache warmup failed: {str(e)}")


@app.get("/redis/metrics", tags=["Cache"])
async def redis_metrics(api_key: str = Depends(get_api_key)):
    """Mtriques dtailles du cluster Redis"""
    try:
        redis_manager = get_redis_cluster_manager()
        cluster_metrics = await redis_manager._collect_cluster_metrics()
        
        # Aggregate metrics
        total_memory = sum(m.memory_usage for m in cluster_metrics.values())
        total_keys = sum(m.key_count for m in cluster_metrics.values())
        avg_hit_ratio = sum(m.hit_ratio for m in cluster_metrics.values()) / len(cluster_metrics) if cluster_metrics else 0
        total_ops = sum(m.operations_per_second for m in cluster_metrics.values())
        
        return {
            "nodes": {
                node_id: {
                    "hit_ratio": metrics.hit_ratio,
                    "memory_usage_mb": metrics.memory_usage / 1024 / 1024,
                    "connected_clients": metrics.connected_clients,
                    "operations_per_second": metrics.operations_per_second,
                    "key_count": metrics.key_count,
                    "eviction_count": metrics.eviction_count,
                    "avg_ttl": metrics.avg_ttl
                }
                for node_id, metrics in cluster_metrics.items()
            },
            "aggregate": {
                "total_memory_mb": total_memory / 1024 / 1024,
                "total_keys": total_keys,
                "average_hit_ratio": avg_hit_ratio,
                "total_ops_per_second": total_ops
            },
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error getting Redis metrics: {str(e)}")


# === LOAD TESTING ENDPOINTS ===

@app.get("/load-test/configs", tags=["Performance"])
async def get_load_test_configs(api_key: str = Depends(get_api_key)):
    """Configurations disponibles pour les tests de charge"""
    try:
        load_tester = get_load_tester()
        configs = await load_tester.get_test_configs()
        return {
            "available_tests": configs,
            "performance_targets": load_tester.performance_targets
        }
    except Exception as e:
        raise HTTPException(500, f"Error getting load test configs: {str(e)}")


@app.post("/load-test/run/{test_name}", tags=["Performance"])
async def run_load_test(
    test_name: str,
    api_key: str = Depends(get_api_key)
):
    """Excuter un test de charge spcifique"""
    try:
        load_tester = get_load_tester()
        
        if test_name not in load_tester.test_configs:
            raise HTTPException(404, f"Test configuration '{test_name}' not found")
        
        # Run test asynchronously
        result = await load_tester.run_test(test_name)
        
        return {
            "test_name": result.test_name,
            "status": result.status,
            "duration_seconds": result.duration_seconds,
            "total_requests": result.total_requests,
            "successful_requests": result.successful_requests,
            "failed_requests": result.failed_requests,
            "error_rate": result.error_rate,
            "avg_response_time": result.avg_response_time,
            "p95_response_time": result.p95_response_time,
            "p99_response_time": result.p99_response_time,
            "requests_per_second": result.requests_per_second,
            "data_received_mb": result.data_received_mb,
            "virtual_users": result.virtual_users,
            "errors": result.errors or []
        }
        
    except Exception as e:
        raise HTTPException(500, f"Load test execution failed: {str(e)}")


@app.post("/load-test/suite", tags=["Performance"])
async def run_performance_suite(api_key: str = Depends(get_api_key)):
    """Excuter la suite complte de tests de performance"""
    try:
        load_tester = get_load_tester()
        
        # Start the suite in background
        suite_task = asyncio.create_task(load_tester.run_performance_suite())
        
        return {
            "status": "started",
            "message": "Performance test suite started",
            "estimated_duration": "90-120 minutes",
            "tests": ["smoke", "load", "stress", "spike", "soak"],
            "started_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Performance suite execution failed: {str(e)}")


@app.post("/load-test/targets", tags=["Performance"])
async def update_performance_targets(
    targets: dict,
    api_key: str = Depends(get_api_key)
):
    """Mettre  jour les cibles de performance"""
    try:
        load_tester = get_load_tester()
        await load_tester.update_performance_targets(targets)
        
        return {
            "status": "success",
            "message": "Performance targets updated",
            "targets": load_tester.performance_targets
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error updating performance targets: {str(e)}")


# === COMPREHENSIVE PERFORMANCE ENDPOINT ===

@app.get("/performance/overview", tags=["Performance"])
async def performance_overview(api_key: str = Depends(get_api_key)):
    """Vue d'ensemble complte des performances du systme"""
    try:
        # Get all performance data
        db_manager = get_database_manager()
        redis_manager = get_redis_cluster_manager()
        monitoring = get_monitoring()
        
        # Database metrics
        db_health = await db_manager.health_check()
        db_metrics = await db_manager.get_performance_metrics()
        
        # Redis metrics
        redis_status = await redis_manager.get_cluster_status()
        
        # System metrics from monitoring
        system_metrics = await monitoring.get_health_status()
        
        return {
            "database": {
                "health": db_health["status"],
                "connections": {
                    "active": db_metrics.active_connections,
                    "idle": db_metrics.idle_connections,
                    "total": db_metrics.total_connections
                },
                "performance": {
                    "avg_query_time": db_metrics.avg_query_time,
                    "slow_queries": db_metrics.slow_queries_count,
                    "buffer_hit_ratio": db_metrics.buffer_hit_ratio,
                    "index_usage_ratio": db_metrics.index_usage_ratio
                }
            },
            "cache": {
                "cluster_state": redis_status.get("cluster_info", {}).get("cluster_state", "unknown"),
                "total_memory_mb": redis_status.get("aggregate_metrics", {}).get("total_memory_mb", 0),
                "total_keys": redis_status.get("aggregate_metrics", {}).get("total_keys", 0),
                "hit_ratio": redis_status.get("aggregate_metrics", {}).get("average_hit_ratio", 0),
                "ops_per_second": redis_status.get("aggregate_metrics", {}).get("total_ops_per_second", 0)
            },
            "system": {
                "status": system_metrics.get("status", "unknown"),
                "uptime": system_metrics.get("uptime", 0),
                "components": system_metrics.get("components", {})
            },
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error getting performance overview: {str(e)}")


# --- Sprint 1.3: Advanced Observability & Scalability Endpoints ---

# Circuit Breaker Management
@app.get("/circuit-breaker/status", summary="Get circuit breaker status")
async def get_circuit_breaker_status(request: Request):
    """Get status of all circuit breakers"""
    try:
        circuit_manager = get_circuit_manager()
        health_summary = circuit_manager.get_health_summary()
        
        await track_request_metrics(request, "circuit_breaker_status", 0.1)
        
        return {
            "circuit_breakers": health_summary,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error getting circuit breaker status: {str(e)}")

@app.get("/circuit-breaker/metrics/{circuit_name}", summary="Get specific circuit breaker metrics")
async def get_circuit_breaker_metrics(circuit_name: str, request: Request):
    """Get detailed metrics for a specific circuit breaker"""
    try:
        circuit_manager = get_circuit_manager()
        all_metrics = circuit_manager.get_all_metrics()
        
        if circuit_name not in all_metrics:
            raise HTTPException(404, f"Circuit breaker '{circuit_name}' not found")
        
        await track_request_metrics(request, "circuit_breaker_metrics", 0.05)
        
        metrics = all_metrics[circuit_name]
        return {
            "circuit_name": circuit_name,
            "metrics": {
                "state": metrics.state.value,
                "failure_count": metrics.failure_count,
                "success_count": metrics.success_count,
                "total_calls": metrics.total_calls,
                "failure_rate": round(metrics.failure_rate * 100, 2),
                "slow_call_rate": round(metrics.slow_call_rate * 100, 2),
                "last_failure_time": metrics.last_failure_time.isoformat() if metrics.last_failure_time else None,
                "state_transition_time": metrics.state_transition_time.isoformat()
            },
            "timestamp": datetime.utcnow()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error getting circuit breaker metrics: {str(e)}")

@app.post("/circuit-breaker/reset/{circuit_name}", summary="Reset circuit breaker")
async def reset_circuit_breaker(circuit_name: str, request: Request):
    """Reset a specific circuit breaker to closed state"""
    try:
        circuit_manager = get_circuit_manager()
        circuit_breaker = await circuit_manager.get_circuit_breaker(circuit_name)
        circuit_breaker.reset()
        
        await track_request_metrics(request, "circuit_breaker_reset", 0.02)
        security_logger.log_security_event("CIRCUIT_BREAKER_RESET", {
            "circuit_name": circuit_name,
            "admin_action": True
        })
        
        return {
            "message": f"Circuit breaker '{circuit_name}' reset successfully",
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error resetting circuit breaker: {str(e)}")

# Distributed Tracing
@app.get("/tracing/status", summary="Get distributed tracing status")
async def get_tracing_status(request: Request):
    """Get distributed tracing system status"""
    try:
        tracer = get_tracer()
        
        await track_request_metrics(request, "tracing_status", 0.05)
        
        return {
            "tracing": {
                "service_name": tracer.service_name,
                "environment": tracer.environment,
                "jaeger_endpoint": tracer.jaeger_endpoint,
                "active_traces": tracer.get_active_traces_count(),
                "total_traces": len(tracer.active_traces)
            },
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error getting tracing status: {str(e)}")

@app.get("/tracing/metrics", summary="Get tracing metrics")
async def get_tracing_metrics(request: Request):
    """Get distributed tracing performance metrics"""
    try:
        tracer = get_tracer()
        trace_metrics = tracer.get_trace_metrics()
        
        await track_request_metrics(request, "tracing_metrics", 0.1)
        
        # Calculate summary statistics
        if trace_metrics:
            completed_traces = [m for m in trace_metrics if m["status"] == "completed"]
            error_traces = [m for m in trace_metrics if m["status"] == "error"]
            
            avg_duration = sum(
                m["duration_ms"] for m in completed_traces if m["duration_ms"]
            ) / len(completed_traces) if completed_traces else 0
            
            error_rate = len(error_traces) / len(trace_metrics) if trace_metrics else 0
        else:
            avg_duration = 0
            error_rate = 0
        
        return {
            "summary": {
                "total_traces": len(trace_metrics),
                "completed_traces": len(completed_traces) if trace_metrics else 0,
                "error_traces": len(error_traces) if trace_metrics else 0,
                "error_rate": round(error_rate * 100, 2),
                "avg_duration_ms": round(avg_duration, 2)
            },
            "traces": trace_metrics[-20:],  # Last 20 traces
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error getting tracing metrics: {str(e)}")

# Business Metrics
@app.get("/business/kpis", summary="Get business KPIs dashboard")
async def get_business_kpis(request: Request):
    """Get business KPIs dashboard data"""
    try:
        business_metrics = get_business_metrics()
        kpi_dashboard = business_metrics.get_kpi_dashboard()
        
        await track_request_metrics(request, "business_kpis", 0.05)
        
        return kpi_dashboard
        
    except Exception as e:
        raise HTTPException(500, f"Error getting business KPIs: {str(e)}")

@app.get("/business/executive", summary="Get executive summary")
async def get_executive_summary(request: Request):
    """Get executive summary for leadership dashboard"""
    try:
        business_metrics = get_business_metrics()
        executive_summary = business_metrics.get_executive_summary()
        
        await track_request_metrics(request, "executive_summary", 0.1)
        
        return executive_summary
        
    except Exception as e:
        raise HTTPException(500, f"Error getting executive summary: {str(e)}")

@app.get("/business/user-analytics", summary="Get user analytics")
async def get_user_analytics(request: Request):
    """Get user analytics and session metrics"""
    try:
        business_metrics = get_business_metrics()
        user_analytics = business_metrics.get_user_analytics()
        
        await track_request_metrics(request, "user_analytics", 0.08)
        
        return user_analytics
        
    except Exception as e:
        raise HTTPException(500, f"Error getting user analytics: {str(e)}")

@app.post("/business/kpi/{kpi_name}", summary="Update business KPI")
async def update_business_kpi(
    kpi_name: str,
    current_value: float,
    trend: Optional[str] = None,
    request: Request = None
):
    """Update a business KPI value"""
    try:
        business_metrics = get_business_metrics()
        business_metrics.update_kpi(kpi_name, current_value, trend)
        
        await track_request_metrics(request, "update_kpi", 0.03)
        security_logger.log_security_event("KPI_UPDATE", {
            "kpi_name": kpi_name,
            "current_value": current_value,
            "trend": trend
        })
        
        return {
            "message": f"KPI '{kpi_name}' updated successfully",
            "kpi_name": kpi_name,
            "current_value": current_value,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error updating KPI: {str(e)}")

# Enhanced Performance Overview
@app.get("/performance/comprehensive", summary="Get comprehensive performance overview")
async def get_comprehensive_performance(request: Request):
    """Get comprehensive performance overview including new Sprint 1.3 metrics"""
    try:
        # Existing performance data
        db_manager = get_database_manager()
        redis_manager = get_redis_cluster_manager()
        monitoring = get_monitoring()
        
        db_health = await db_manager.health_check()
        db_metrics = await db_manager.get_metrics()
        redis_status = await redis_manager.get_cluster_status()
        system_metrics = await monitoring.get_system_metrics()
        
        # Sprint 1.3 - Advanced metrics
        circuit_manager = get_circuit_manager()
        tracer = get_tracer()
        business_metrics = get_business_metrics()
        
        circuit_health = circuit_manager.get_health_summary()
        user_analytics = business_metrics.get_user_analytics()
        
        await track_request_metrics(request, "comprehensive_performance", 0.2)
        
        return {
            "database": {
                "health": db_health["status"],
                "connections": {
                    "active": db_metrics.active_connections,
                    "idle": db_metrics.idle_connections,
                    "total": db_metrics.total_connections
                },
                "performance": {
                    "avg_query_time": db_metrics.avg_query_time,
                    "slow_queries": db_metrics.slow_queries_count,
                    "buffer_hit_ratio": db_metrics.buffer_hit_ratio,
                    "index_usage_ratio": db_metrics.index_usage_ratio
                }
            },
            "cache": {
                "cluster_state": redis_status.get("cluster_info", {}).get("cluster_state", "unknown"),
                "total_memory_mb": redis_status.get("aggregate_metrics", {}).get("total_memory_mb", 0),
                "total_keys": redis_status.get("aggregate_metrics", {}).get("total_keys", 0),
                "hit_ratio": redis_status.get("aggregate_metrics", {}).get("average_hit_ratio", 0),
                "ops_per_second": redis_status.get("aggregate_metrics", {}).get("total_ops_per_second", 0)
            },
            "circuit_breakers": {
                "total_circuits": circuit_health["total_circuits"],
                "open_circuits": circuit_health["open_circuits"],
                "overall_health": circuit_health["overall_health"],
                "circuits": circuit_health["circuits"]
            },
            "tracing": {
                "active_traces": tracer.get_active_traces_count(),
                "total_traces": len(tracer.active_traces)
            },
            "users": {
                "active_sessions": user_analytics["active_sessions"],
                "avg_response_time_ms": user_analytics["avg_response_time_ms"],
                "avg_success_rate": user_analytics["avg_success_rate"]
            },
            "system": {
                "status": system_metrics.get("status", "unknown"),
                "uptime": system_metrics.get("uptime", 0),
                "components": system_metrics.get("components", {})
            },
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error getting comprehensive performance: {str(e)}")

# === SPRINT 2.1 - ADVANCED ARCHITECTURE ENDPOINTS ===

# Memory Optimization Endpoints

@app.get("/memory/metrics", tags=["Architecture", "Performance"])
async def get_memory_metrics(api_key: str = Depends(get_api_key)):
    """Get advanced memory management metrics"""
    try:
        memory_optimizer = get_memory_optimizer()
        metrics = memory_optimizer.get_memory_metrics()
        return metrics
    except Exception as e:
        raise HTTPException(500, f"Failed to get memory metrics: {str(e)}")


@app.post("/memory/optimize", tags=["Architecture", "Performance"])
async def force_memory_optimization(api_key: str = Depends(get_api_key)):
    """Force memory optimization and cleanup"""
    try:
        memory_optimizer = get_memory_optimizer()
        result = await memory_optimizer.force_optimization()
        return result
    except Exception as e:
        raise HTTPException(500, f"Memory optimization failed: {str(e)}")


@app.post("/memory/session/{session_id}", tags=["Architecture"])
async def register_memory_session(
    session_id: str,
    initial_data: Optional[dict] = None,
    api_key: str = Depends(get_api_key)
):
    """Register new session for memory management"""
    try:
        memory_optimizer = get_memory_optimizer()
        await memory_optimizer.register_session(session_id, initial_data)
        return {"status": "success", "session_id": session_id}
    except Exception as e:
        raise HTTPException(500, f"Failed to register session: {str(e)}")


@app.delete("/memory/session/{session_id}", tags=["Architecture"])
async def remove_memory_session(session_id: str, api_key: str = Depends(get_api_key)):
    """Remove session from memory management"""
    try:
        memory_optimizer = get_memory_optimizer()
        await memory_optimizer.remove_session(session_id)
        return {"status": "success", "session_id": session_id}
    except Exception as e:
        raise HTTPException(500, f"Failed to remove session: {str(e)}")


# Advanced State Management Endpoints

@app.get("/state/metrics", tags=["Architecture", "State"])
async def get_state_metrics(api_key: str = Depends(get_api_key)):
    """Get advanced state management metrics"""
    try:
        state_manager = get_advanced_state_manager()
        metrics = state_manager.get_state_metrics()
        return metrics
    except Exception as e:
        raise HTTPException(500, f"Failed to get state metrics: {str(e)}")


@app.post("/state/optimize", tags=["Architecture", "State"])
async def optimize_states(api_key: str = Depends(get_api_key)):
    """Optimize state storage and performance"""
    try:
        state_manager = get_advanced_state_manager()
        result = await state_manager.optimize_states()
        return result
    except Exception as e:
        raise HTTPException(500, f"State optimization failed: {str(e)}")


@app.post("/state/store", tags=["Architecture", "State"])
async def store_agent_state(
    session_id: str,
    agent_id: str,
    state: dict,
    compression_type: str = "zlib",
    api_key: str = Depends(get_api_key)
):
    """Store agent state with compression"""
    try:
        state_manager = get_advanced_state_manager()
        from orchestrator.app.agents.advanced_state_manager import StateCompressionType
        
        compression_enum = StateCompressionType(compression_type)
        state_key = await state_manager.store_state(session_id, agent_id, state, compression_enum)
        
        return {
            "status": "success",
            "state_key": state_key,
            "session_id": session_id,
            "agent_id": agent_id
        }
    except Exception as e:
        raise HTTPException(500, f"Failed to store state: {str(e)}")


@app.get("/state/retrieve/{state_key}", tags=["Architecture", "State"])
async def retrieve_agent_state(state_key: str, api_key: str = Depends(get_api_key)):
    """Retrieve and decompress agent state"""
    try:
        state_manager = get_advanced_state_manager()
        state = await state_manager.retrieve_state(state_key)
        
        if state is None:
            raise HTTPException(404, f"State not found: {state_key}")
        
        return {
            "status": "success",
            "state_key": state_key,
            "state": state
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Failed to retrieve state: {str(e)}")


# Advanced Agent Coordination Endpoints

@app.get("/coordination/metrics", tags=["Architecture", "Agents"])
async def get_coordination_metrics(api_key: str = Depends(get_api_key)):
    """Get multi-agent coordination metrics"""
    try:
        coordination = get_advanced_coordination()
        metrics = coordination.get_coordination_metrics()
        return metrics
    except Exception as e:
        raise HTTPException(500, f"Failed to get coordination metrics: {str(e)}")


@app.post("/coordination/task", tags=["Architecture", "Agents"])
async def submit_agent_task(
    agent_type: str,
    description: str,
    session_id: str,
    priority: str = "NORMAL",
    timeout: float = 300.0,
    dependencies: List[str] = [],
    cpu_required: float = 0.5,
    memory_required: float = 256.0,
    llm_tokens_required: int = 1000,
    db_connections_required: int = 0,
    api_key: str = Depends(get_api_key)
):
    """Submit task for advanced multi-agent execution"""
    try:
        coordination = get_advanced_coordination()
        
        # Create task
        task = AgentTask(
            task_id=str(uuid.uuid4()),
            agent_type=agent_type,
            description=description,
            priority=AgentPriority[priority.upper()],
            session_id=session_id,
            created_at=datetime.utcnow(),
            timeout=timeout,
            dependencies=dependencies,
            resources_required={
                ResourceType.CPU: cpu_required,
                ResourceType.MEMORY: memory_required,
                ResourceType.LLM_TOKENS: llm_tokens_required,
                ResourceType.DATABASE: db_connections_required
            },
            metadata={}
        )
        
        task_id = await coordination.submit_task(task)
        
        return {
            "status": "success",
            "task_id": task_id,
            "agent_type": agent_type,
            "priority": priority
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to submit task: {str(e)}")


@app.get("/coordination/task/{task_id}", tags=["Architecture", "Agents"])
async def get_task_status(task_id: str, api_key: str = Depends(get_api_key)):
    """Get status of specific agent task"""
    try:
        coordination = get_advanced_coordination()
        status = await coordination.get_task_status(task_id)
        return status
    except Exception as e:
        raise HTTPException(500, f"Failed to get task status: {str(e)}")


@app.delete("/coordination/task/{task_id}", tags=["Architecture", "Agents"])
async def cancel_agent_task(task_id: str, api_key: str = Depends(get_api_key)):
    """Cancel agent task execution"""
    try:
        coordination = get_advanced_coordination()
        cancelled = await coordination.cancel_task(task_id)
        
        if not cancelled:
            raise HTTPException(404, f"Task not found or cannot be cancelled: {task_id}")
        
        return {
            "status": "cancelled",
            "task_id": task_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Failed to cancel task: {str(e)}")


# Comprehensive Architecture Overview

@app.get("/architecture/overview", tags=["Architecture"])
async def get_architecture_overview(api_key: str = Depends(get_api_key)):
    """Get comprehensive architecture performance overview"""
    try:
        memory_optimizer = get_memory_optimizer()
        state_manager = get_advanced_state_manager()
        coordination = get_advanced_coordination()
        
        memory_metrics = memory_optimizer.get_memory_metrics()
        state_metrics = state_manager.get_state_metrics()
        coordination_metrics = coordination.get_coordination_metrics()
        
        return {
            "memory_management": {
                "status": "operational" if "error" not in memory_metrics else "error",
                "memory_usage_mb": memory_metrics.get("system", {}).get("memory_usage_mb", 0),
                "active_sessions": memory_metrics.get("sessions", {}).get("active_sessions", 0),
                "gc_optimizations": len(memory_metrics.get("gc_history", [])),
                "leak_detection": memory_metrics.get("monitoring_active", False)
            },
            "state_management": {
                "status": "operational" if "error" not in state_metrics else "error",
                "total_states": state_metrics.get("current", {}).get("total_states", 0),
                "cache_hit_rate": state_metrics.get("current", {}).get("cache_hit_rate", 0),
                "compression_ratio": state_metrics.get("compression", {}).get("compression_ratio", 0),
                "memory_usage_mb": state_metrics.get("current", {}).get("memory_usage_mb", 0)
            },
            "agent_coordination": {
                "status": "operational" if "error" not in coordination_metrics else "error",
                "active_agents": coordination_metrics.get("current", {}).get("active_agents", 0),
                "queued_tasks": coordination_metrics.get("current", {}).get("queued_tasks", 0),
                "completed_tasks": coordination_metrics.get("current", {}).get("completed_tasks", 0),
                "parallel_efficiency": coordination_metrics.get("current", {}).get("parallel_efficiency", 0),
                "resource_utilization": coordination_metrics.get("resources", {}).get("utilization", {})
            },
            "integration": {
                "components_initialized": 3,
                "cross_component_communication": "operational",
                "performance_optimizations_active": True
            },
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to get architecture overview: {str(e)}")

# Helper functions for Sprint 2.1 dependency injection
def get_memory_optimizer():
    from orchestrator.app.performance.memory_optimizer import memory_optimizer
    return memory_optimizer


def get_advanced_state_manager():
    from orchestrator.app.agents.advanced_state_manager import advanced_state_manager
    return advanced_state_manager


def get_advanced_coordination():
    from orchestrator.app.agents.advanced_coordination import advanced_coordination
    return advanced_coordination

# =============================================================================
# SPRINT 2.2 - LOAD BALANCING & AUTO-SCALING ENTERPRISE ENDPOINTS
# =============================================================================

# --- Load Balancer Management ---

@app.get("/load-balancer/status")
@limiter.limit("30/minute")
async def get_load_balancer_status(request: Request):
    """Get comprehensive load balancer status and metrics"""
    try:
        load_balancer = await get_load_balancer()
        stats = await load_balancer.get_stats()
        
        return {
            "status": "operational",
            "algorithm": stats["algorithm"],
            "uptime_seconds": stats["uptime_seconds"],
            "metrics": stats["metrics"],
            "backends": stats["backends"],
            "session_affinity_count": stats["session_affinity_count"],
            "health_check_config": stats["health_check_config"],
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to get load balancer status: {str(e)}")

@app.post("/load-balancer/backends")
@limiter.limit("10/minute")
async def add_backend_server(
    request: Request,
    backend_id: str,
    host: str,
    port: int,
    weight: int = 100,
    max_connections: int = 1000
):
    """Add a new backend server to the load balancer pool"""
    try:
        load_balancer = await get_load_balancer()
        
        backend = BackendServer(
            id=backend_id,
            host=host,
            port=port,
            weight=weight,
            max_connections=max_connections
        )
        
        load_balancer.add_backend(backend)
        
        await security_logger.log_audit_event(
            AuditEventType.ADMIN_ACTION,
            f"Added backend server: {backend_id} ({host}:{port})",
            {"backend_id": backend_id, "host": host, "port": port}
        )
        
        return {
            "status": "success",
            "message": f"Backend {backend_id} added successfully",
            "backend": {
                "id": backend_id,
                "host": host,
                "port": port,
                "weight": weight,
                "max_connections": max_connections
            }
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to add backend server: {str(e)}")

@app.delete("/load-balancer/backends/{backend_id}")
@limiter.limit("10/minute")
async def remove_backend_server(request: Request, backend_id: str):
    """Remove a backend server from the load balancer pool"""
    try:
        load_balancer = await get_load_balancer()
        success = load_balancer.remove_backend(backend_id)
        
        if success:
            await security_logger.log_audit_event(
                AuditEventType.ADMIN_ACTION,
                f"Removed backend server: {backend_id}",
                {"backend_id": backend_id}
            )
            
            return {
                "status": "success",
                "message": f"Backend {backend_id} marked for removal"
            }
        else:
            raise HTTPException(404, f"Backend {backend_id} not found")
            
    except Exception as e:
        raise HTTPException(500, f"Failed to remove backend server: {str(e)}")

@app.post("/load-balancer/algorithm")
@limiter.limit("5/minute")
async def update_load_balancing_algorithm(
    request: Request,
    algorithm: str
):
    """Update load balancing algorithm"""
    try:
        # Validate algorithm
        try:
            lb_algorithm = LoadBalancingAlgorithm(algorithm)
        except ValueError:
            raise HTTPException(400, f"Invalid algorithm: {algorithm}")
        
        from orchestrator.app.performance.load_balancer import configure_load_balancer
        
        load_balancer = await configure_load_balancer(algorithm=lb_algorithm)
        
        await security_logger.log_audit_event(
            AuditEventType.ADMIN_ACTION,
            f"Updated load balancing algorithm to: {algorithm}",
            {"new_algorithm": algorithm}
        )
        
        return {
            "status": "success",
            "message": f"Load balancing algorithm updated to {algorithm}",
            "algorithm": algorithm
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to update algorithm: {str(e)}")

@app.get("/load-balancer/metrics")
@limiter.limit("60/minute")
async def get_load_balancer_metrics(request: Request):
    """Get detailed load balancer performance metrics"""
    try:
        load_balancer = await get_load_balancer()
        stats = await load_balancer.get_stats()
        
        # Calculate additional metrics
        total_requests = stats["metrics"]["total_requests"]
        successful_requests = stats["metrics"]["successful_requests"]
        failed_requests = stats["metrics"]["failed_requests"]
        
        success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
        
        # Backend health summary
        healthy_backends = sum(1 for b in stats["backends"] if b["health"] == "healthy")
        total_backends = len(stats["backends"])
        
        return {
            "performance": {
                "total_requests": total_requests,
                "success_rate_percent": success_rate,
                "average_response_time_ms": stats["metrics"]["avg_response_time"],
                "requests_per_second": total_requests / max(stats["uptime_seconds"], 1)
            },
            "backends": {
                "total": total_backends,
                "healthy": healthy_backends,
                "health_percentage": (healthy_backends / total_backends * 100) if total_backends > 0 else 0
            },
            "detailed_backends": stats["backends"],
            "session_affinity": {
                "active_sessions": stats["session_affinity_count"]
            },
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to get load balancer metrics: {str(e)}")

# --- Auto-Scaling Management ---

@app.get("/auto-scaling/status")
@limiter.limit("30/minute")
async def get_auto_scaling_status(request: Request):
    """Get comprehensive auto-scaling status and metrics"""
    try:
        auto_scaler = await get_auto_scaler()
        metrics = await auto_scaler.get_metrics()
        
        return {
            "status": "operational",
            "deployment": metrics["deployment"],
            "scaling_rules": metrics["scaling_rules"],
            "current_state": metrics["state"],
            "statistics": metrics["statistics"],
            "custom_metrics": metrics["custom_metrics"],
            "recent_scaling_events": metrics["recent_scaling_events"],
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to get auto-scaling status: {str(e)}")

@app.post("/auto-scaling/recommendation")
@limiter.limit("10/minute")
async def get_scaling_recommendation(request: Request):
    """Get intelligent scaling recommendation based on current metrics"""
    try:
        auto_scaler = await get_auto_scaler()
        recommendation = await auto_scaler.get_scaling_recommendation()
        
        return {
            "recommendation": recommendation,
            "confidence_threshold": 0.7,  # Minimum confidence for auto-scaling
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to get scaling recommendation: {str(e)}")

@app.post("/auto-scaling/execute")
@limiter.limit("5/minute")
async def execute_manual_scaling(
    request: Request,
    target_replicas: int,
    reason: str = "Manual scaling"
):
    """Execute manual scaling operation"""
    try:
        # Validate target replicas
        if target_replicas < 1 or target_replicas > 50:
            raise HTTPException(400, "Target replicas must be between 1 and 50")
        
        auto_scaler = await get_auto_scaler()
        success = await auto_scaler.execute_scaling(target_replicas, f"Manual: {reason}")
        
        if success:
            await security_logger.log_audit_event(
                AuditEventType.ADMIN_ACTION,
                f"Manual scaling executed: {target_replicas} replicas",
                {"target_replicas": target_replicas, "reason": reason}
            )
            
            return {
                "status": "success",
                "message": f"Scaling to {target_replicas} replicas initiated",
                "target_replicas": target_replicas,
                "reason": reason
            }
        else:
            raise HTTPException(500, "Failed to execute scaling operation")
            
    except Exception as e:
        raise HTTPException(500, f"Failed to execute scaling: {str(e)}")

@app.post("/auto-scaling/rules")
@limiter.limit("5/minute")
async def add_scaling_rule(
    request: Request,
    rule_name: str,
    min_replicas: int,
    max_replicas: int,
    cpu_target: Optional[int] = None,
    memory_target: Optional[int] = None
):
    """Add a new auto-scaling rule"""
    try:
        auto_scaler = await get_auto_scaler()
        
        # Build metrics
        metrics = []
        if cpu_target:
            metrics.append(ScalingMetric(
                name="cpu",
                target_type="Utilization",
                target_value=str(cpu_target),
                resource_name="cpu"
            ))
        
        if memory_target:
            metrics.append(ScalingMetric(
                name="memory",
                target_type="Utilization",
                target_value=str(memory_target),
                resource_name="memory"
            ))
        
        # Create scaling rule
        rule = ScalingRule(
            name=rule_name,
            min_replicas=min_replicas,
            max_replicas=max_replicas,
            metrics=metrics
        )
        
        auto_scaler.add_scaling_rule(rule)
        await auto_scaler.create_hpa(rule_name)
        
        await security_logger.log_audit_event(
            AuditEventType.ADMIN_ACTION,
            f"Added scaling rule: {rule_name}",
            {
                "rule_name": rule_name,
                "min_replicas": min_replicas,
                "max_replicas": max_replicas,
                "cpu_target": cpu_target,
                "memory_target": memory_target
            }
        )
        
        return {
            "status": "success",
            "message": f"Scaling rule {rule_name} added successfully",
            "rule": {
                "name": rule_name,
                "min_replicas": min_replicas,
                "max_replicas": max_replicas,
                "metrics": [{"name": m.name, "target": m.target_value} for m in metrics]
            }
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to add scaling rule: {str(e)}")

@app.post("/auto-scaling/custom-metric")
@limiter.limit("30/minute")
async def update_custom_metric(
    request: Request,
    metric_name: str,
    value: float
):
    """Update custom metric for scaling decisions"""
    try:
        auto_scaler = await get_auto_scaler()
        await auto_scaler.update_custom_metric(metric_name, value)
        
        return {
            "status": "success",
            "message": f"Custom metric {metric_name} updated",
            "metric_name": metric_name,
            "value": value,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to update custom metric: {str(e)}")

@app.post("/auto-scaling/setup-production")
@limiter.limit("2/minute")
async def setup_production_auto_scaling(request: Request):
    """Setup production-ready auto-scaling configuration"""
    try:
        auto_scaler = await setup_production_scaling()
        
        await security_logger.log_audit_event(
            AuditEventType.ADMIN_ACTION,
            "Production auto-scaling configuration applied",
            {"min_replicas": 3, "max_replicas": 20}
        )
        
        return {
            "status": "success",
            "message": "Production auto-scaling configuration applied",
            "configuration": {
                "min_replicas": 3,
                "max_replicas": 20,
                "cpu_target": "70%",
                "memory_target": "80%",
                "hpa_created": True
            }
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to setup production scaling: {str(e)}")

# --- Combined Load Balancing & Auto-Scaling Monitoring ---

@app.get("/scaling-infrastructure/overview")
@limiter.limit("30/minute")
async def get_scaling_infrastructure_overview(request: Request):
    """Get comprehensive overview of load balancing and auto-scaling infrastructure"""
    try:
        load_balancer = await get_load_balancer()
        auto_scaler = await get_auto_scaler()
        
        lb_stats = await load_balancer.get_stats()
        scaling_metrics = await auto_scaler.get_metrics()
        
        return {
            "infrastructure_status": "operational",
            "load_balancer": {
                "algorithm": lb_stats["algorithm"],
                "backends_total": len(lb_stats["backends"]),
                "backends_healthy": sum(1 for b in lb_stats["backends"] if b["health"] == "healthy"),
                "total_requests": lb_stats["metrics"]["total_requests"],
                "success_rate": (
                    lb_stats["metrics"]["successful_requests"] / lb_stats["metrics"]["total_requests"] * 100
                    if lb_stats["metrics"]["total_requests"] > 0 else 0
                )
            },
            "auto_scaling": {
                "current_replicas": scaling_metrics["deployment"]["current_replicas"],
                "desired_replicas": scaling_metrics["deployment"]["desired_replicas"],
                "scaling_rules_count": len(scaling_metrics["scaling_rules"]),
                "total_scaling_events": scaling_metrics["statistics"]["total_scaling_events"],
                "last_scale_time": scaling_metrics["state"]["last_scale_time"]
            },
            "combined_metrics": {
                "estimated_capacity": scaling_metrics["deployment"]["current_replicas"] * len(lb_stats["backends"]),
                "traffic_distribution_efficiency": "optimal" if len(lb_stats["backends"]) >= 2 else "single_backend",
                "scalability_readiness": "production_ready"
            },
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to get scaling infrastructure overview: {str(e)}")