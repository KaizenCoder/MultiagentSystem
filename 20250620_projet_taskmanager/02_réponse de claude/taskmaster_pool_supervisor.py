#!/usr/bin/env python3
"""
TaskMaster Pool Supervisor - Gestionnaire d'instances TaskMaster parallèles
Version complète avec orchestration, monitoring et API REST
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from uuid import uuid4
from enum import Enum
import psutil
import signal
import sys

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

# Import du TaskMaster principal
from agent_taskmaster_core import AgentTaskMasterNextGeneration
from ..logging.centralized_logging import logging_manager, log_performance

# Configuration du logging pour le superviseur
logger = logging_manager.get_logger("taskmaster_supervisor")

class InstanceStatus(Enum):
    """États possibles d'une instance TaskMaster"""
    STARTING = "starting"
    RUNNING = "running"
    BUSY = "busy"
    DEGRADED = "degraded"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"

class InstanceInfo:
    """Information sur une instance TaskMaster"""
    def __init__(self, instance_id: str, instance: AgentTaskMasterNextGeneration):
        self.instance_id = instance_id
        self.instance = instance
        self.status = InstanceStatus.STARTING
        self.created_at = datetime.now()
        self.last_health_check = None
        self.health_data = {}
        self.active_tasks = 0
        self.completed_tasks = 0
        self.error_count = 0
        self.last_error = None
        self.metadata = {}

class TaskMasterRegistry:
    """Registre centralisé des instances TaskMaster avec gestion avancée"""
    
    def __init__(self):
        self.instances: Dict[str, InstanceInfo] = {}
        self.max_instances = 10
        self.instance_lock = asyncio.Lock()
        self.logger = logging_manager.get_logger("taskmaster_registry")
        
    async def register(self, instance_id: str, instance: AgentTaskMasterNextGeneration, metadata: Dict[str, Any] = None) -> bool:
        """Enregistre une nouvelle instance"""
        async with self.instance_lock:
            if len(self.instances) >= self.max_instances:
                self.logger.warning(f"Maximum instances reached ({self.max_instances})")
                return False
            
            if instance_id in self.instances:
                self.logger.warning(f"Instance {instance_id} already registered")
                return False
            
            info = InstanceInfo(instance_id, instance)
            info.metadata = metadata or {}
            self.instances[instance_id] = info
            
            self.logger.info(
                f"Instance registered: {instance_id}",
                extra={
                    "instance_id": instance_id,
                    "total_instances": len(self.instances),
                    "metadata": metadata
                }
            )
            return True
    
    async def unregister(self, instance_id: str) -> bool:
        """Désenregistre une instance"""
        async with self.instance_lock:
            if instance_id in self.instances:
                del self.instances[instance_id]
                self.logger.info(f"Instance unregistered: {instance_id}")
                return True
            return False
    
    def get(self, instance_id: str) -> Optional[InstanceInfo]:
        """Récupère les infos d'une instance"""
        return self.instances.get(instance_id)
    
    def list_instances(self) -> List[Dict[str, Any]]:
        """Liste toutes les instances avec leurs infos"""
        instances_list = []
        for instance_id, info in self.instances.items():
            instances_list.append({
                "instance_id": instance_id,
                "status": info.status.value,
                "created_at": info.created_at.isoformat(),
                "active_tasks": info.active_tasks,
                "completed_tasks": info.completed_tasks,
                "error_count": info.error_count,
                "health": info.health_data,
                "metadata": info.metadata
            })
        return instances_list
    
    def get_available_instance(self) -> Optional[str]:
        """Retourne l'ID de l'instance la moins chargée"""
        available = []
        
        for instance_id, info in self.instances.items():
            if info.status == InstanceStatus.RUNNING and info.active_tasks < 5:
                available.append((instance_id, info.active_tasks))
        
        if available:
            # Retourner l'instance avec le moins de tâches actives
            available.sort(key=lambda x: x[1])
            return available[0][0]
        
        return None
    
    async def update_instance_stats(self, instance_id: str, stats: Dict[str, Any]):
        """Met à jour les statistiques d'une instance"""
        if instance_id in self.instances:
            info = self.instances[instance_id]
            info.active_tasks = stats.get("active_tasks", 0)
            info.completed_tasks = stats.get("completed_tasks", 0)
            
            # Déterminer le statut basé sur la charge
            if info.active_tasks == 0:
                info.status = InstanceStatus.RUNNING
            elif info.active_tasks < 5:
                info.status = InstanceStatus.RUNNING
            else:
                info.status = InstanceStatus.BUSY

class LoadBalancer:
    """Load balancer pour distribution des tâches"""
    
    def __init__(self, registry: TaskMasterRegistry):
        self.registry = registry
        self.logger = logging_manager.get_logger("taskmaster_loadbalancer")
        self.strategy = "least_loaded"  # least_loaded, round_robin, random
        self.last_assigned = None
        
    async def assign_task(self, task_request: Dict[str, Any]) -> Optional[str]:
        """Assigne une tâche à l'instance optimale"""
        if self.strategy == "least_loaded":
            instance_id = self.registry.get_available_instance()
            
            if instance_id:
                self.logger.info(
                    f"Task assigned to instance {instance_id}",
                    extra={"strategy": self.strategy, "instance_id": instance_id}
                )
                return instance_id
            else:
                self.logger.warning("No available instance for task assignment")
                return None
        
        # Autres stratégies peuvent être implémentées ici
        return None

class TaskMasterSupervisor:
    """Superviseur principal des instances TaskMaster"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.registry = TaskMasterRegistry()
        self.load_balancer = LoadBalancer(self.registry)
        self.logger = logger
        self._running = False
        self._health_check_task = None
        self._metrics_task = None
        
        # Configuration
        self.auto_scaling_enabled = self.config.get("auto_scaling", True)
        self.min_instances = self.config.get("min_instances", 1)
        self.max_instances = self.config.get("max_instances", 10)
        self.health_check_interval = self.config.get("health_check_interval", 30)
        
    async def start(self):
        """Démarre le superviseur"""
        self.logger.info("Starting TaskMaster Supervisor")
        self._running = True
        
        # Créer les instances minimales
        for i in range(self.min_instances):
            await self.create_instance(f"auto_{i}")
        
        # Démarrer les tâches de maintenance
        self._health_check_task = asyncio.create_task(self._periodic_health_check())
        self._metrics_task = asyncio.create_task(self._collect_global_metrics())
        
        self.logger.info(f"Supervisor started with {self.min_instances} initial instances")
    
    async def stop(self):
        """Arrête le superviseur et toutes les instances"""
        self.logger.info("Stopping TaskMaster Supervisor")
        self._running = False
        
        # Annuler les tâches de maintenance
        if self._health_check_task:
            self._health_check_task.cancel()
        if self._metrics_task:
            self._metrics_task.cancel()
        
        # Arrêter toutes les instances
        tasks = []
        for instance_id, info in self.registry.instances.items():
            self.logger.info(f"Stopping instance {instance_id}")
            tasks.append(info.instance.shutdown())
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        self.logger.info("Supervisor stopped")
    
    async def create_instance(
        self,
        instance_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Crée une nouvelle instance TaskMaster"""
        if not instance_id:
            instance_id = f"tm_{uuid4().hex[:8]}"
        
        # Configuration par défaut + surcharges
        instance_config = {
            "max_concurrent_tasks": 10,
            "max_parallel_tasks": 3,
            "continuous_validation": True,
            "ai_learning_mode": True
        }
        if config:
            instance_config.update(config)
        
        try:
            # Créer l'instance
            instance = AgentTaskMasterNextGeneration(
                agent_id=instance_id,
                config=instance_config
            )
            
            # Enregistrer
            success = await self.registry.register(instance_id, instance, {"config": instance_config})
            
            if not success:
                return {
                    "status": "error",
                    "reason": "Failed to register instance"
                }
            
            # Démarrer l'instance
            await instance.startup()
            
            # Mettre à jour le statut
            info = self.registry.get(instance_id)
            if info:
                info.status = InstanceStatus.RUNNING
            
            self.logger.info(
                f"Instance {instance_id} created successfully",
                extra={"instance_id": instance_id, "config": instance_config}
            )
            
            return {
                "status": "success",
                "instance_id": instance_id,
                "config": instance_config
            }
            
        except Exception as e:
            self.logger.error(
                f"Error creating instance {instance_id}",
                extra={"error": str(e)},
                exc_info=True
            )
            
            # Nettoyer si erreur
            await self.registry.unregister(instance_id)
            
            return {
                "status": "error",
                "reason": str(e)
            }
    
    async def stop_instance(self, instance_id: str) -> Dict[str, Any]:
        """Arrête une instance spécifique"""
        info = self.registry.get(instance_id)
        
        if not info:
            return {
                "status": "error",
                "reason": "Instance not found"
            }
        
        try:
            info.status = InstanceStatus.STOPPING
            
            # Arrêter l'instance
            await info.instance.shutdown()
            
            # Désenregistrer
            await self.registry.unregister(instance_id)
            
            self.logger.info(f"Instance {instance_id} stopped successfully")
            
            return {
                "status": "success",
                "instance_id": instance_id
            }
            
        except Exception as e:
            self.logger.error(
                f"Error stopping instance {instance_id}",
                extra={"error": str(e)},
                exc_info=True
            )
            
            return {
                "status": "error",
                "reason": str(e)
            }
    
    async def submit_task(self, task_request: Dict[str, Any]) -> Dict[str, Any]:
        """Soumet une tâche au pool d'instances"""
        # Load balancing
        instance_id = await self.load_balancer.assign_task(task_request)
        
        if not instance_id:
            # Auto-scaling si activé
            if self.auto_scaling_enabled and len(self.registry.instances) < self.max_instances:
                self.logger.info("No available instance, creating new one")
                result = await self.create_instance()
                if result["status"] == "success":
                    instance_id = result["instance_id"]
                    # Attendre un peu que l'instance soit prête
                    await asyncio.sleep(self.health_check_interval)
                
                for instance_id, info in list(self.registry.instances.items()):
                    try:
                        # Effectuer le health check
                        health = await info.instance.health_check()
                        info.health_data = health
                        info.last_health_check = datetime.now()
                        
                        # Mettre à jour les statistiques
                        if "stats" in health:
                            await self.registry.update_instance_stats(instance_id, health["stats"])
                        
                        # Gérer les instances dégradées
                        if health.get("status") == "degraded":
                            info.status = InstanceStatus.DEGRADED
                            self.logger.warning(
                                f"Instance {instance_id} is degraded",
                                extra={"health": health}
                            )
                        elif health.get("status") == "unhealthy":
                            info.status = InstanceStatus.ERROR
                            self.logger.error(
                                f"Instance {instance_id} is unhealthy",
                                extra={"health": health}
                            )
                            # Optionnel: redémarrer l'instance
                            if self.config.get("auto_restart_unhealthy", True):
                                await self._restart_instance(instance_id)
                        
                    except Exception as e:
                        self.logger.error(
                            f"Health check failed for instance {instance_id}",
                            extra={"error": str(e)},
                            exc_info=True
                        )
                        info.status = InstanceStatus.ERROR
                        info.error_count += 1
                        info.last_error = str(e)
                
                # Auto-scaling basé sur la charge globale
                if self.auto_scaling_enabled:
                    await self._auto_scale()
                    
            except Exception as e:
                self.logger.error(
                    "Error in periodic health check",
                    extra={"error": str(e)},
                    exc_info=True
                )
    
    async def _restart_instance(self, instance_id: str):
        """Redémarre une instance défaillante"""
        self.logger.info(f"Restarting instance {instance_id}")
        
        # Sauvegarder la config
        info = self.registry.get(instance_id)
        if not info:
            return
        
        config = info.metadata.get("config", {})
        
        # Arrêter l'instance
        await self.stop_instance(instance_id)
        
        # Attendre un peu
        await asyncio.sleep(2)
        
        # Recréer avec le même ID
        await self.create_instance(instance_id, config)
    
    async def _auto_scale(self):
        """Gère l'auto-scaling des instances"""
        total_active_tasks = sum(info.active_tasks for info in self.registry.instances.values())
        total_instances = len(self.registry.instances)
        
        # Calculer la charge moyenne
        avg_load = total_active_tasks / total_instances if total_instances > 0 else 0
        
        # Scale up si charge élevée
        if avg_load > 7 and total_instances < self.max_instances:
            self.logger.info(
                f"Auto-scaling UP: avg_load={avg_load:.1f}, creating new instance"
            )
            await self.create_instance()
        
        # Scale down si charge faible
        elif avg_load < 2 and total_instances > self.min_instances:
            # Trouver l'instance la moins chargée
            least_loaded = min(
                self.registry.instances.items(),
                key=lambda x: x[1].active_tasks
            )
            
            if least_loaded[1].active_tasks == 0:
                self.logger.info(
                    f"Auto-scaling DOWN: removing idle instance {least_loaded[0]}"
                )
                await self.stop_instance(least_loaded[0])
    
    async def _collect_global_metrics(self):
        """Collecte les métriques globales du pool"""
        while self._running:
            try:
                await asyncio.sleep(60)  # Toutes les minutes
                
                metrics = {
                    "timestamp": datetime.now().isoformat(),
                    "total_instances": len(self.registry.instances),
                    "instances_by_status": {},
                    "total_active_tasks": 0,
                    "total_completed_tasks": 0,
                    "total_errors": 0,
                    "system_resources": {
                        "cpu_percent": psutil.cpu_percent(),
                        "memory_percent": psutil.virtual_memory().percent,
                        "disk_percent": psutil.disk_usage('/').percent
                    }
                }
                
                # Agrégation par statut
                for status in InstanceStatus:
                    count = sum(1 for info in self.registry.instances.values() if info.status == status)
                    metrics["instances_by_status"][status.value] = count
                
                # Agrégation des tâches
                for info in self.registry.instances.values():
                    metrics["total_active_tasks"] += info.active_tasks
                    metrics["total_completed_tasks"] += info.completed_tasks
                    metrics["total_errors"] += info.error_count
                
                # Logger les métriques
                perf_logger = logging_manager.get_performance_logger()
                perf_logger.info(
                    "TaskMaster Pool Metrics",
                    extra={"metrics": metrics}
                )
                
                # Sauvegarder les métriques
                await self._save_metrics(metrics)
                
            except Exception as e:
                self.logger.error(
                    "Error collecting global metrics",
                    extra={"error": str(e)},
                    exc_info=True
                )
    
    async def _save_metrics(self, metrics: Dict[str, Any]):
        """Sauvegarde les métriques dans un fichier"""
        try:
            metrics_dir = Path("metrics/taskmaster_pool")
            metrics_dir.mkdir(parents=True, exist_ok=True)
            
            # Fichier du jour
            date_str = datetime.now().strftime("%Y%m%d")
            metrics_file = metrics_dir / f"metrics_{date_str}.jsonl"
            
            # Ajouter la ligne de métriques
            with open(metrics_file, 'a') as f:
                f.write(json.dumps(metrics) + '\n')
                
        except Exception as e:
            self.logger.error(f"Error saving metrics: {e}")
    
    def get_pool_status(self) -> Dict[str, Any]:
        """Retourne le statut complet du pool"""
        return {
            "supervisor_status": "running" if self._running else "stopped",
            "total_instances": len(self.registry.instances),
            "instances": self.registry.list_instances(),
            "auto_scaling": {
                "enabled": self.auto_scaling_enabled,
                "min_instances": self.min_instances,
                "max_instances": self.max_instances,
                "current_instances": len(self.registry.instances)
            },
            "load_balancer": {
                "strategy": self.load_balancer.strategy
            }
        }

# Configuration globale
supervisor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    global supervisor
    
    # Démarrage
    supervisor = TaskMasterSupervisor({
        "auto_scaling": True,
        "min_instances": 2,
        "max_instances": 10,
        "health_check_interval": 30,
        "auto_restart_unhealthy": True
    })
    await supervisor.start()
    
    yield
    
    # Arrêt
    await supervisor.stop()

# API REST
app = FastAPI(
    title="TaskMaster Pool Supervisor API",
    version="1.0.0",
    description="API pour gérer le pool d'instances TaskMaster NextGeneration",
    lifespan=lifespan
)

# CORS pour interface web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles Pydantic
class TaskRequest(BaseModel):
    request: str = Field(..., description="Requête en langage naturel")
    user_id: str = Field(default="default", description="ID de l'utilisateur")
    context: Dict[str, Any] = Field(default_factory=dict, description="Contexte additionnel")

class InstanceConfig(BaseModel):
    instance_id: Optional[str] = Field(None, description="ID de l'instance (auto-généré si absent)")
    max_concurrent_tasks: int = Field(default=10, description="Nombre max de tâches concurrentes")
    max_parallel_tasks: int = Field(default=3, description="Nombre max de tâches parallèles")
    continuous_validation: bool = Field(default=True, description="Validation continue activée")
    ai_learning_mode: bool = Field(default=True, description="Mode apprentissage IA activé")

class TaskStatusRequest(BaseModel):
    instance_id: str = Field(..., description="ID de l'instance")
    task_id: str = Field(..., description="ID de la tâche")

# Endpoints
@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "service": "TaskMaster Pool Supervisor",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "pool_status": "/pool/status",
            "list_instances": "/instances",
            "create_instance": "/instances/create",
            "submit_task": "/tasks/submit",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "supervisor_running": supervisor is not None and supervisor._running
    }

@app.get("/pool/status")
async def get_pool_status():
    """Retourne le statut complet du pool"""
    if not supervisor:
        raise HTTPException(status_code=503, detail="Supervisor not initialized")
    
    return supervisor.get_pool_status()

@app.get("/instances")
async def list_instances():
    """Liste toutes les instances du pool"""
    if not supervisor:
        raise HTTPException(status_code=503, detail="Supervisor not initialized")
    
    return {
        "instances": supervisor.registry.list_instances(),
        "total": len(supervisor.registry.instances)
    }

@app.get("/instances/{instance_id}")
async def get_instance_details(instance_id: str):
    """Récupère les détails d'une instance spécifique"""
    if not supervisor:
        raise HTTPException(status_code=503, detail="Supervisor not initialized")
    
    info = supervisor.registry.get(instance_id)
    if not info:
        raise HTTPException(status_code=404, detail=f"Instance {instance_id} not found")
    
    # Récupérer les tâches de l'instance
    tasks = await info.instance.list_tasks()
    
    return {
        "instance_id": instance_id,
        "status": info.status.value,
        "created_at": info.created_at.isoformat(),
        "active_tasks": info.active_tasks,
        "completed_tasks": info.completed_tasks,
        "error_count": info.error_count,
        "last_error": info.last_error,
        "health": info.health_data,
        "tasks": tasks,
        "metadata": info.metadata
    }

@app.post("/instances/create")
async def create_instance(config: InstanceConfig):
    """Crée une nouvelle instance TaskMaster"""
    if not supervisor:
        raise HTTPException(status_code=503, detail="Supervisor not initialized")
    
    result = await supervisor.create_instance(
        instance_id=config.instance_id,
        config=config.dict(exclude={"instance_id"})
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["reason"])
    
    return result

@app.delete("/instances/{instance_id}")
async def stop_instance(instance_id: str):
    """Arrête et supprime une instance"""
    if not supervisor:
        raise HTTPException(status_code=503, detail="Supervisor not initialized")
    
    result = await supervisor.stop_instance(instance_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["reason"])
    
    return result

@app.post("/tasks/submit")
async def submit_task(task_request: TaskRequest):
    """Soumet une nouvelle tâche au pool"""
    if not supervisor:
        raise HTTPException(status_code=503, detail="Supervisor not initialized")
    
    result = await supervisor.submit_task(task_request.dict())
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["reason"])
    
    return result

@app.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str, instance_id: Optional[str] = None):
    """Récupère le statut d'une tâche"""
    if not supervisor:
        raise HTTPException(status_code=503, detail="Supervisor not initialized")
    
    # Si instance_id fourni, chercher directement
    if instance_id:
        info = supervisor.registry.get(instance_id)
        if info:
            status = await info.instance.get_task_status(task_id)
            return status
    
    # Sinon, chercher dans toutes les instances
    for instance_id, info in supervisor.registry.instances.items():
        status = await info.instance.get_task_status(task_id)
        if status["status"] != "not_found":
            return {**status, "instance_id": instance_id}
    
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks/{task_id}/cancel")
async def cancel_task(task_id: str, instance_id: Optional[str] = None):
    """Annule une tâche en cours"""
    if not supervisor:
        raise HTTPException(status_code=503, detail="Supervisor not initialized")
    
    # Logique similaire à get_task_status
    if instance_id:
        info = supervisor.registry.get(instance_id)
        if info:
            result = await info.instance.cancel_task(task_id)
            return result
    
    # Chercher dans toutes les instances
    for instance_id, info in supervisor.registry.instances.items():
        try:
            result = await info.instance.cancel_task(task_id)
            if result["status"] != "error":
                return {**result, "instance_id": instance_id}
        except:
            continue
    
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/pool/scale")
async def scale_pool(target_instances: int):
    """Ajuste manuellement le nombre d'instances"""
    if not supervisor:
        raise HTTPException(status_code=503, detail="Supervisor not initialized")
    
    current = len(supervisor.registry.instances)
    
    if target_instances < supervisor.min_instances or target_instances > supervisor.max_instances:
        raise HTTPException(
            status_code=400,
            detail=f"Target must be between {supervisor.min_instances} and {supervisor.max_instances}"
        )
    
    results = []
    
    # Scale up
    if target_instances > current:
        for _ in range(target_instances - current):
            result = await supervisor.create_instance()
            results.append(result)
    
    # Scale down
    elif target_instances < current:
        # Arrêter les instances les moins chargées
        instances_to_stop = []
        sorted_instances = sorted(
            supervisor.registry.instances.items(),
            key=lambda x: x[1].active_tasks
        )
        
        for i in range(current - target_instances):
            instance_id = sorted_instances[i][0]
            result = await supervisor.stop_instance(instance_id)
            results.append(result)
    
    return {
        "previous_count": current,
        "target_count": target_instances,
        "current_count": len(supervisor.registry.instances),
        "operations": results
    }

# Gestion des signaux pour arrêt propre
def signal_handler(sig, frame):
    """Gestionnaire de signaux pour arrêt propre"""
    logger.info(f"Received signal {sig}")
    if supervisor:
        asyncio.create_task(supervisor.stop())
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Point d'entrée pour lancement direct
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )sleep(1)
            else:
                return {
                    "status": "error",
                    "reason": "No available instances and auto-scaling limit reached"
                }
        
        # Soumettre la tâche
        info = self.registry.get(instance_id)
        if info:
            try:
                result = await info.instance.create_task_from_natural_language(
                    user_request=task_request["request"],
                    user_id=task_request.get("user_id", "default"),
                    context=task_request.get("context", {})
                )
                
                # Mettre à jour les stats
                info.active_tasks += 1
                
                return {
                    "status": "success",
                    "instance_id": instance_id,
                    "task_result": result
                }
                
            except Exception as e:
                info.error_count += 1
                info.last_error = str(e)
                
                return {
                    "status": "error",
                    "reason": str(e)
                }
        
        return {
            "status": "error",
            "reason": "Instance not found after assignment"
        }
    
    async def _periodic_health_check(self):
        """Vérifie périodiquement la santé des instances"""
        while self._running:
            try:
                await asyncio.



