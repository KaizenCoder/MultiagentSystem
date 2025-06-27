#!/usr/bin/env python3
"""
🚀 PARALLEL TASK MANAGER - Phase 2 Optimisations Performance
==============================================================

Gestionnaire de tâches parallèles pour Chef d'Équipe Maintenance
Pattern Producer/Consumer avec intégration circuit breakers et cache intelligent

Architecture:
- Pool d'agents avec concurrence contrôlée (3-5 max)
- Queue asynchrone avec priorités
- Circuit breakers par agent
- Cache intelligent pour éviter re-traitement
- Monitoring temps réel des performances

Mission: Remplacer traitement séquentiel par parallélisme optimisé
Objectif: -40% temps d'exécution, +15% taux de succès

Author: Infrastructure d'Optimisation NextGeneration
Version: 1.0.0 - Phase 2 Launch
"""

import asyncio
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
import threading

# Imports infrastructure optimisation Phase 1
from .config_manager import ConfigManager, AgentConfig
from .metrics_collector import AdvancedMetricsCollector
from .circuit_breaker import CircuitBreakerManager
from .cache_manager import IntelligentCache


class TaskPriority(Enum):
    """Priorités des tâches"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    """États des tâches"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class AgentTask:
    """Tâche pour un agent de maintenance"""
    task_id: str
    agent_path: str
    agent_name: str
    task_type: str
    params: Dict[str, Any]
    priority: TaskPriority = TaskPriority.NORMAL
    timeout: float = 300.0
    retry_count: int = 0
    max_retries: int = 3
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    worker_id: Optional[str] = None


@dataclass
class WorkerStats:
    """Statistiques d'un worker"""
    worker_id: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_execution_time: float = 0.0
    last_task_time: Optional[float] = None
    is_busy: bool = False
    current_task_id: Optional[str] = None


class ParallelTaskManager:
    """
    Gestionnaire de tâches parallèles pour Chef d'Équipe Maintenance
    
    Fonctionnalités:
    - Pool de workers avec concurrence contrôlée
    - Queue de tâches avec priorités
    - Circuit breakers par agent
    - Cache intelligent
    - Monitoring performances temps réel
    - Fallback mode séquentiel
    """
    
    def __init__(
        self,
        max_workers: int = 5,
        queue_size: int = 100,
        config_path: Optional[str] = None,
        enable_cache: bool = True,
        enable_circuit_breaker: bool = True
    ):
        self.max_workers = max_workers
        self.queue_size = queue_size
        self.enable_cache = enable_cache
        self.enable_circuit_breaker = enable_circuit_breaker
        
        # Configuration
        self.config_manager = ConfigManager(config_path) if config_path else None
        self.config = self._load_config()
        
        # Infrastructure monitoring
        self.metrics = AdvancedMetricsCollector()
        self.circuit_breaker = CircuitBreakerManager() if enable_circuit_breaker else None
        self.cache = IntelligentCache() if enable_cache else None
        
        # Task management
        self.task_queue: asyncio.PriorityQueue = None
        self.tasks: Dict[str, AgentTask] = {}
        self.workers: Dict[str, WorkerStats] = {}
        self.worker_semaphore: asyncio.Semaphore = None
        
        # State management
        self.is_running = False
        self.shutdown_event: asyncio.Event = None
        self.worker_tasks: List[asyncio.Task] = []
        
        # Logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"ParallelTaskManager initialisé - Max workers: {max_workers}")
        
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration depuis le gestionnaire"""
        if self.config_manager:
            try:
                config = self.config_manager.get_global_settings()
                return {
                    "max_workers": min(self.max_workers, config.performance.max_concurrent_agents),
                    "task_timeout": config.performance.task_timeout_seconds,
                    "retry_attempts": config.performance.retry_attempts,
                    "enable_fallback": config.performance.enable_fallback_sequential
                }
            except Exception as e:
                self.logger.warning(f"Erreur chargement config: {e}")
        
        return {
            "max_workers": self.max_workers,
            "task_timeout": 300.0,
            "retry_attempts": 3,
            "enable_fallback": True
        }
    
    async def startup(self):
        """Démarrage du gestionnaire de tâches parallèles"""
        if self.is_running:
            return
        
        self.logger.info("🚀 Démarrage ParallelTaskManager")
        
        # Initialisation infrastructure
        if self.circuit_breaker:
            await self.circuit_breaker.startup()
        
        if self.cache:
            # IntelligentCache n'a pas de méthode startup
            pass
        
        # Initialisation queues et workers
        self.task_queue = asyncio.PriorityQueue(maxsize=self.queue_size)
        self.worker_semaphore = asyncio.Semaphore(self.config["max_workers"])
        self.shutdown_event = asyncio.Event()
        
        # Démarrage workers
        for i in range(self.config["max_workers"]):
            worker_id = f"worker_{i+1}"
            self.workers[worker_id] = WorkerStats(worker_id=worker_id)
            
            worker_task = asyncio.create_task(
                self._worker_loop(worker_id),
                name=f"parallel_worker_{worker_id}"
            )
            self.worker_tasks.append(worker_task)
        
        self.is_running = True
        self.logger.info(f"✅ ParallelTaskManager démarré - {len(self.workers)} workers actifs")
    
    async def shutdown(self):
        """Arrêt propre du gestionnaire"""
        if not self.is_running:
            return
        
        self.logger.info("🛑 Arrêt ParallelTaskManager")
        
        # Signal d'arrêt
        self.shutdown_event.set()
        
        # Attendre completion des tâches en cours
        if self.worker_tasks:
            await asyncio.gather(*self.worker_tasks, return_exceptions=True)
        
        # Arrêt infrastructure
        if self.circuit_breaker:
            await self.circuit_breaker.shutdown()
        
        if self.cache:
            # IntelligentCache n'a pas de méthode shutdown
            pass
        
        self.is_running = False
        self.logger.info("✅ ParallelTaskManager arrêté")
    
    async def submit_task(
        self,
        agent_path: str,
        task_type: str,
        params: Dict[str, Any],
        priority: TaskPriority = TaskPriority.NORMAL,
        timeout: Optional[float] = None
    ) -> str:
        """
        Soumet une tâche pour traitement parallèle
        
        Args:
            agent_path: Chemin vers l'agent à traiter
            task_type: Type de tâche (test_code, repair_code, etc.)
            params: Paramètres de la tâche
            priority: Priorité de la tâche
            timeout: Timeout spécifique (sinon config par défaut)
        
        Returns:
            task_id: Identifiant unique de la tâche
        """
        if not self.is_running:
            raise RuntimeError("ParallelTaskManager non démarré")
        
        # Génération tâche
        task_id = str(uuid.uuid4())
        agent_name = Path(agent_path).name
        
        task = AgentTask(
            task_id=task_id,
            agent_path=agent_path,
            agent_name=agent_name,
            task_type=task_type,
            params=params,
            priority=priority,
            timeout=timeout or self.config["task_timeout"]
        )
        
        # Vérification cache si activé
        if self.cache and task_type in ["test_code", "analyze_code"]:
            cache_key = self._generate_cache_key(task)
            cached_result = await self.cache.get(cache_key)
            
            if cached_result:
                self.logger.info(f"📋 Cache HIT pour {agent_name} - {task_type}")
                task.status = TaskStatus.COMPLETED
                task.result = cached_result
                task.completed_at = time.time()
                self.tasks[task_id] = task
                
                # Métriques cache hit
                self.metrics.record_execution(
                    agent_name, 0.001, True, 1024
                )
                
                return task_id
        
        # Ajout à la queue
        self.tasks[task_id] = task
        priority_value = priority.value
        
        try:
            await self.task_queue.put((priority_value, time.time(), task))
            self.logger.info(f"📋 Tâche {task_id} ajoutée - {agent_name} ({task_type})")
            return task_id
            
        except asyncio.QueueFull:
            self.logger.error(f"❌ Queue pleine - Tâche {task_id} rejetée")
            task.status = TaskStatus.FAILED
            task.error = "Queue pleine"
            raise RuntimeError("Queue de tâches pleine")
    
    async def submit_batch_tasks(
        self,
        agents_paths: List[str],
        task_type: str,
        params_template: Dict[str, Any],
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> List[str]:
        """
        Soumet un lot de tâches en parallèle
        
        Args:
            agents_paths: Liste des chemins d'agents
            task_type: Type de tâche commun
            params_template: Template de paramètres
            priority: Priorité commune
        
        Returns:
            List des task_ids générés
        """
        task_ids = []
        
        for agent_path in agents_paths:
            # Personnalisation params par agent
            params = params_template.copy()
            params["agent_path"] = agent_path
            params["agent_name"] = Path(agent_path).name
            
            task_id = await self.submit_task(
                agent_path=agent_path,
                task_type=task_type,
                params=params,
                priority=priority
            )
            task_ids.append(task_id)
        
        self.logger.info(f"📋 Batch soumis - {len(task_ids)} tâches ({task_type})")
        return task_ids
    
    async def wait_for_task(self, task_id: str, timeout: Optional[float] = None) -> AgentTask:
        """
        Attend la completion d'une tâche spécifique
        
        Args:
            task_id: Identifiant de la tâche
            timeout: Timeout d'attente (optionnel)
        
        Returns:
            AgentTask complétée
        """
        if task_id not in self.tasks:
            raise ValueError(f"Tâche {task_id} introuvable")
        
        task = self.tasks[task_id]
        start_time = time.time()
        
        while task.status in [TaskStatus.PENDING, TaskStatus.RUNNING]:
            if timeout and (time.time() - start_time) > timeout:
                self.logger.warning(f"⏰ Timeout attente tâche {task_id}")
                raise asyncio.TimeoutError(f"Timeout attente tâche {task_id}")
            
            await asyncio.sleep(0.1)
        
        return task
    
    async def wait_for_batch(
        self,
        task_ids: List[str],
        timeout: Optional[float] = None,
        return_when: str = "ALL_COMPLETED"
    ) -> Dict[str, AgentTask]:
        """
        Attend la completion d'un lot de tâches
        
        Args:
            task_ids: Liste des identifiants de tâches
            timeout: Timeout global (optionnel)
            return_when: "ALL_COMPLETED" ou "FIRST_COMPLETED"
        
        Returns:
            Dict des tâches complétées {task_id: AgentTask}
        """
        start_time = time.time()
        completed_tasks = {}
        
        while len(completed_tasks) < len(task_ids):
            if timeout and (time.time() - start_time) > timeout:
                self.logger.warning(f"⏰ Timeout batch - {len(completed_tasks)}/{len(task_ids)} complétées")
                break
            
            for task_id in task_ids:
                if task_id in completed_tasks:
                    continue
                
                if task_id not in self.tasks:
                    continue
                
                task = self.tasks[task_id]
                if task.status not in [TaskStatus.PENDING, TaskStatus.RUNNING]:
                    completed_tasks[task_id] = task
                    
                    if return_when == "FIRST_COMPLETED":
                        return completed_tasks
            
            await asyncio.sleep(0.1)
        
        self.logger.info(f"📋 Batch terminé - {len(completed_tasks)}/{len(task_ids)} complétées")
        return completed_tasks
    
    async def _worker_loop(self, worker_id: str):
        """Boucle principale d'un worker"""
        worker_stats = self.workers[worker_id]
        self.logger.info(f"🔄 Worker {worker_id} démarré")
        
        while not self.shutdown_event.is_set():
            try:
                # Acquisition sémaphore
                async with self.worker_semaphore:
                    # Récupération tâche
                    try:
                        priority, timestamp, task = await asyncio.wait_for(
                            self.task_queue.get(),
                            timeout=1.0
                        )
                    except asyncio.TimeoutError:
                        continue
                    
                    # Traitement tâche
                    await self._process_task(task, worker_id, worker_stats)
                    
            except Exception as e:
                self.logger.error(f"❌ Erreur worker {worker_id}: {e}")
                await asyncio.sleep(0.5)
        
        self.logger.info(f"🛑 Worker {worker_id} arrêté")
    
    async def _process_task(self, task: AgentTask, worker_id: str, worker_stats: WorkerStats):
        """Traite une tâche spécifique"""
        task.status = TaskStatus.RUNNING
        task.started_at = time.time()
        task.worker_id = worker_id
        
        worker_stats.is_busy = True
        worker_stats.current_task_id = task.task_id
        
        self.logger.info(f"🔄 Worker {worker_id} traite {task.agent_name} ({task.task_type})")
        
        try:
            # Vérification circuit breaker
            if self.circuit_breaker:
                breaker = await self.circuit_breaker.get_circuit_breaker(task.agent_name)
                state = breaker.get_state()
                if state["state"] == "open":
                    raise RuntimeError(f"Circuit breaker ouvert pour {task.agent_name}")
            
            # Exécution avec timeout
            result = await asyncio.wait_for(
                self._execute_task_logic(task),
                timeout=task.timeout
            )
            
            # Succès
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.completed_at = time.time()
            
            # Mise en cache si applicable
            if self.cache and task.task_type in ["test_code", "analyze_code"]:
                cache_key = self._generate_cache_key(task)
                await self.cache.set(cache_key, result, ttl=3600)
            
            # Métriques succès
            execution_time = task.completed_at - task.started_at
            self.metrics.record_execution(
                task.agent_name, execution_time, True, 1024*1024
            )
            
            # Circuit breaker succès
            if self.circuit_breaker:
                breaker = await self.circuit_breaker.get_circuit_breaker(task.agent_name)
                breaker.record_success()
            
            worker_stats.tasks_completed += 1
            worker_stats.total_execution_time += execution_time
            
            self.logger.info(f"✅ {task.agent_name} complété par {worker_id} en {execution_time:.2f}s")
            
        except asyncio.TimeoutError:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Timeout après {task.timeout}s"
            task.completed_at = time.time()
            
            worker_stats.tasks_failed += 1
            
            self.logger.warning(f"⏰ Timeout {task.agent_name} sur {worker_id}")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = time.time()
            
            # Circuit breaker échec
            if self.circuit_breaker:
                breaker = await self.circuit_breaker.get_circuit_breaker(task.agent_name)
                breaker.record_failure()
            
            # Métriques échec
            execution_time = task.completed_at - task.started_at
            self.metrics.record_execution(
                task.agent_name, execution_time, False, 2*1024*1024
            )
            
            worker_stats.tasks_failed += 1
            
            self.logger.error(f"❌ Échec {task.agent_name} sur {worker_id}: {e}")
        
        finally:
            worker_stats.is_busy = False
            worker_stats.current_task_id = None
            worker_stats.last_task_time = time.time()
    
    async def _execute_task_logic(self, task: AgentTask) -> Dict[str, Any]:
        """
        Logique d'exécution d'une tâche
        À surcharger par les implémentations spécifiques
        """
        # Simulation pour tests
        await asyncio.sleep(0.1)
        
        return {
            "success": True,
            "agent_name": task.agent_name,
            "task_type": task.task_type,
            "execution_time": 0.1,
            "message": f"Tâche {task.task_type} simulée pour {task.agent_name}"
        }
    
    def _generate_cache_key(self, task: AgentTask) -> str:
        """Génère une clé de cache pour une tâche"""
        agent_path = Path(task.agent_path)
        
        # Hash basé sur contenu + type tâche
        import hashlib
        content_hash = hashlib.md5(
            f"{agent_path.stat().st_mtime}_{task.task_type}_{task.agent_name}".encode()
        ).hexdigest()
        
        return f"parallel_task_{task.task_type}_{content_hash}"
    
    def get_stats(self) -> Dict[str, Any]:
        """Statistiques du gestionnaire de tâches"""
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
        failed_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
        
        return {
            "manager_status": "running" if self.is_running else "stopped",
            "total_workers": len(self.workers),
            "busy_workers": sum(1 for w in self.workers.values() if w.is_busy),
            "queue_size": self.task_queue.qsize() if self.task_queue else 0,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "worker_stats": {
                worker_id: {
                    "tasks_completed": stats.tasks_completed,
                    "tasks_failed": stats.tasks_failed,
                    "avg_execution_time": (
                        stats.total_execution_time / stats.tasks_completed
                        if stats.tasks_completed > 0 else 0
                    ),
                    "is_busy": stats.is_busy
                }
                for worker_id, stats in self.workers.items()
            }
        }
    
    async def get_performance_report(self) -> Dict[str, Any]:
        """Rapport de performance détaillé"""
        stats = self.get_stats()
        
        # Métriques avancées
        if hasattr(self.metrics, 'get_dashboard_data'):
            performance_metrics = self.metrics.get_dashboard_data()
            stats["performance_metrics"] = performance_metrics
        
        # Circuit breaker stats
        if self.circuit_breaker:
            cb_stats = await self.circuit_breaker.get_stats()
            stats["circuit_breaker_stats"] = cb_stats
        
        # Cache stats
        if self.cache:
            cache_stats = self.cache.get_stats()
            stats["cache_stats"] = cache_stats
        
        return stats


# Factory function
def create_parallel_task_manager(
    max_workers: int = 5,
    config_path: Optional[str] = None,
    **kwargs
) -> ParallelTaskManager:
    """
    Factory pour créer un ParallelTaskManager configuré
    
    Args:
        max_workers: Nombre maximum de workers
        config_path: Chemin vers configuration
        **kwargs: Arguments supplémentaires
    
    Returns:
        ParallelTaskManager configuré
    """
    return ParallelTaskManager(
        max_workers=max_workers,
        config_path=config_path,
        **kwargs
    ) 