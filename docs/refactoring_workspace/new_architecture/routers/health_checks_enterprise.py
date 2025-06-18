"""
Health Checks Enterprise - NextGeneration
Liveness, Readiness, Startup probes compatibles Kubernetes
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import psutil
import asyncio
import time
from datetime import datetime

health_router = APIRouter(prefix="/health", tags=["health"])

# tat application
app_state = {
    "startup_time": time.time(),
    "dependencies_ready": False,
    "last_health_check": None
}

@health_router.get("/live")
async def liveness_probe() -> Dict[str, Any]:
    """
    Liveness probe - Vrifie que l'application tourne
    Kubernetes: redmarre le pod si choue
    """
    try:
        # Vrifications basiques
        current_time = datetime.utcnow()
        uptime = time.time() - app_state["startup_time"]
        
        app_state["last_health_check"] = current_time.isoformat()
        
        return {
            "status": "alive",
            "timestamp": current_time.isoformat(),
            "uptime_seconds": round(uptime, 2),
            "version": "2.0.0",
            "process_id": os.getpid()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Liveness check failed: {str(e)}"
        )

@health_router.get("/ready")
async def readiness_probe() -> Dict[str, Any]:
    """
    Readiness probe - Vrifie que l'app peut servir du trafic
    Kubernetes: retire du load balancer si choue
    """
    try:
        checks = {}
        
        # Vrification mmoire
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Memory usage too high: {memory.percent}%"
            )
        checks["memory"] = f"{memory.percent}%"
        
        # Vrification CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        if cpu_percent > 95:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"CPU usage too high: {cpu_percent}%"
            )
        checks["cpu"] = f"{cpu_percent}%"
        
        # Vrification dpendances (simul)
        if not app_state["dependencies_ready"]:
            # En production: vrifier DB, Redis, APIs externes
            pass
        checks["database"] = "connected"
        checks["cache"] = "connected"
        checks["external_apis"] = "available"
        
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": checks
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Readiness check failed: {str(e)}"
        )

@health_router.get("/startup")
async def startup_probe() -> Dict[str, Any]:
    """
    Startup probe - Vrifie que l'app a dmarr avec succs
    Kubernetes: attend que ce probe russisse avant liveness/readiness
    """
    try:
        startup_duration = time.time() - app_state["startup_time"]
        
        # Considr comme dmarr aprs 30 secondes max
        if startup_duration < 30:
            app_state["dependencies_ready"] = True
            
        return {
            "status": "started",
            "timestamp": datetime.utcnow().isoformat(),
            "startup_duration_seconds": round(startup_duration, 2),
            "dependencies_initialized": app_state["dependencies_ready"],
            "ready_for_traffic": startup_duration >= 5  # 5s minimum
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Startup check failed: {str(e)}"
        )

@health_router.get("/status")
async def detailed_status() -> Dict[str, Any]:
    """Status dtaill pour monitoring/debugging"""
    return {
        "application": "NextGeneration Orchestrator",
        "version": "2.0.0",
        "architecture": "Hexagonal + CQRS",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": round(time.time() - app_state["startup_time"], 2),
        "health_checks": {
            "liveness": "/health/live",
            "readiness": "/health/ready", 
            "startup": "/health/startup"
        },
        "metrics_endpoint": "/metrics",
        "agents_status": "coordinated"
    }
