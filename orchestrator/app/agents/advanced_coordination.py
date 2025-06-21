"""
Advanced Multi-Agent Coordination System
Handles parallel agent execution, resource allocation, and dynamic scaling.
"""

import asyncio
import sys
from pathlib import Path
from core import logging_manager
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Tuple, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import json
import uuid

from ..config import settings
from ..observability.monitoring import get_monitoring
from ..security.logging import security_logger
from .advanced_state_manager import get_advanced_state_manager
from ..performance.memory_optimizer import get_memory_optimizer


# LoggingManager NextGeneration - Agent
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="AgentPriority",
            role="ai_processor",
            domain="orchestration",
            async_enabled=True
        )


class AgentPriority(Enum):
    """Agent task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class ResourceType(Enum):
    """Resource types for agent allocation"""
    CPU = "cpu"
    MEMORY = "memory"
    NETWORK = "network"
    LLM_TOKENS = "llm_tokens"
    DATABASE = "database"


@dataclass
class AgentTask:
    """Agent task definition"""
    task_id: str
    agent_type: str
    description: str
    priority: AgentPriority
    session_id: str
    created_at: datetime
    timeout: float
    dependencies: List[str]
    resources_required: Dict[ResourceType, float]
    metadata: Dict[str, Any]
    retries: int = 0
    max_retries: int = 3


@dataclass
class AgentInstance:
    """Running agent instance"""
    instance_id: str
    agent_type: str
    task_id: str
    session_id: str
    status: AgentStatus
    started_at: datetime
    last_heartbeat: datetime
    resources_allocated: Dict[ResourceType, float]
    output: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class ResourcePool:
    """System resource pool"""
    total_cpu: float
    available_cpu: float
    total_memory_mb: float
    available_memory_mb: float
    total_llm_tokens: int
    available_llm_tokens: int
    database_connections: int
    available_db_connections: int


@dataclass
class CoordinationMetrics:
    """Multi-agent coordination metrics"""
    active_agents: int
    queued_tasks: int
    completed_tasks: int
    failed_tasks: int
    avg_execution_time: float
    resource_utilization: Dict[str, float]
    parallel_efficiency: float
    communication_overhead_ms: float
    dynamic_scaling_events: int
    timestamp: datetime


class TaskQueue:
    """Priority-based task queue with dependency management"""
    
    def __init__(self):
        self.queues = {priority: deque() for priority in AgentPriority}
        self.pending_tasks: Dict[str, AgentTask] = {}
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        self.completed_tasks: Set[str] = set()
        
    def add_task(self, task: AgentTask):
        """Add task to queue"""
        self.pending_tasks[task.task_id] = task
        
        # Add to dependency graph
        for dep in task.dependencies:
            self.dependency_graph[dep].add(task.task_id)
        
        # Check if task can be queued immediately
        if self._can_execute(task):
            self.queues[task.priority].append(task)
    
    def get_next_task(self) -> Optional[AgentTask]:
        """Get next executable task by priority"""
        for priority in reversed(list(AgentPriority)):
            if self.queues[priority]:
                task = self.queues[priority].popleft()
                return task
        return None
    
    def mark_completed(self, task_id: str):
        """Mark task as completed and queue dependents"""
        self.completed_tasks.add(task_id)
        
        # Check if any dependent tasks can now be executed
        for dependent_id in self.dependency_graph[task_id]:
            if dependent_id in self.pending_tasks:
                task = self.pending_tasks[dependent_id]
                if self._can_execute(task) and task not in [t for queue in self.queues.values() for t in queue]:
                    self.queues[task.priority].append(task)
    
    def _can_execute(self, task: AgentTask) -> bool:
        """Check if task dependencies are satisfied"""
        return all(dep in self.completed_tasks for dep in task.dependencies)
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
        return {
            "total_pending": len(self.pending_tasks),
            "total_completed": len(self.completed_tasks),
            "queued_by_priority": {
                priority.name: len(queue) for priority, queue in self.queues.items()
            }
        }


class ResourceManager:
    """Manages system resources for agent allocation"""
    
    def __init__(self):
        self.resource_pool = ResourcePool(
            total_cpu=4.0,
            available_cpu=4.0,
            total_memory_mb=4096.0,
            available_memory_mb=4096.0,
            total_llm_tokens=10000,
            available_llm_tokens=10000,
            database_connections=20,
            available_db_connections=20
        )
        self.allocated_resources: Dict[str, Dict[ResourceType, float]] = {}
        self.resource_usage_history: List[Dict] = []
        
    def can_allocate(self, instance_id: str, resources: Dict[ResourceType, float]) -> bool:
        """Check if resources can be allocated"""
        required_cpu = resources.get(ResourceType.CPU, 0)
        required_memory = resources.get(ResourceType.MEMORY, 0)
        required_tokens = resources.get(ResourceType.LLM_TOKENS, 0)
        required_db = resources.get(ResourceType.DATABASE, 0)
        
        return (
            self.resource_pool.available_cpu >= required_cpu and
            self.resource_pool.available_memory_mb >= required_memory and
            self.resource_pool.available_llm_tokens >= required_tokens and
            self.resource_pool.available_db_connections >= required_db
        )
    
    def allocate_resources(self, instance_id: str, resources: Dict[ResourceType, float]) -> bool:
        """Allocate resources to agent instance"""
        if not self.can_allocate(instance_id, resources):
            return False
        
        # Allocate resources
        cpu = resources.get(ResourceType.CPU, 0)
        memory = resources.get(ResourceType.MEMORY, 0)
        tokens = resources.get(ResourceType.LLM_TOKENS, 0)
        db = resources.get(ResourceType.DATABASE, 0)
        
        self.resource_pool.available_cpu -= cpu
        self.resource_pool.available_memory_mb -= memory
        self.resource_pool.available_llm_tokens -= tokens
        self.resource_pool.available_db_connections -= db
        
        self.allocated_resources[instance_id] = resources
        
        logger.info(f"Allocated resources to {instance_id}: CPU={cpu}, Memory={memory}MB, Tokens={tokens}, DB={db}")
        return True
    
    def deallocate_resources(self, instance_id: str):
        """Deallocate resources from agent instance"""
        if instance_id not in self.allocated_resources:
            return
        
        resources = self.allocated_resources[instance_id]
        
        cpu = resources.get(ResourceType.CPU, 0)
        memory = resources.get(ResourceType.MEMORY, 0)
        tokens = resources.get(ResourceType.LLM_TOKENS, 0)
        db = resources.get(ResourceType.DATABASE, 0)
        
        self.resource_pool.available_cpu += cpu
        self.resource_pool.available_memory_mb += memory
        self.resource_pool.available_llm_tokens += tokens
        self.resource_pool.available_db_connections += db
        
        del self.allocated_resources[instance_id]
        
        logger.info(f"Deallocated resources from {instance_id}")
    
    def get_utilization(self) -> Dict[str, float]:
        """Get resource utilization percentages"""
        return {
            "cpu": ((self.resource_pool.total_cpu - self.resource_pool.available_cpu) / self.resource_pool.total_cpu) * 100,
            "memory": ((self.resource_pool.total_memory_mb - self.resource_pool.available_memory_mb) / self.resource_pool.total_memory_mb) * 100,
            "llm_tokens": ((self.resource_pool.total_llm_tokens - self.resource_pool.available_llm_tokens) / self.resource_pool.total_llm_tokens) * 100,
            "database": ((self.resource_pool.database_connections - self.resource_pool.available_db_connections) / self.resource_pool.database_connections) * 100
        }
    
    def refresh_llm_tokens(self):
        """Refresh LLM token pool (called periodically)"""
        self.resource_pool.available_llm_tokens = self.resource_pool.total_llm_tokens


class CommunicationOptimizer:
    """Optimizes inter-agent communication"""
    
    def __init__(self):
        self.message_queue: Dict[str, List[Dict]] = defaultdict(list)
        self.communication_stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "avg_latency_ms": 0,
            "total_overhead_ms": 0
        }
        self.batch_size = 10
        self.batch_timeout = 0.1  # 100ms
        
    async def send_message(self, from_agent: str, to_agent: str, message: Dict[str, Any]) -> bool:
        """Send optimized message between agents"""
        try:
            start_time = time.time()
            
            message_data = {
                "from": from_agent,
                "to": to_agent,
                "data": message,
                "timestamp": datetime.utcnow(),
                "id": str(uuid.uuid4())
            }
            
            # Add to queue for batching
            self.message_queue[to_agent].append(message_data)
            
            # Process batch if size reached
            if len(self.message_queue[to_agent]) >= self.batch_size:
                await self._process_message_batch(to_agent)
            
            latency_ms = (time.time() - start_time) * 1000
            self.communication_stats["messages_sent"] += 1
            self.communication_stats["total_overhead_ms"] += latency_ms
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending message from {from_agent} to {to_agent}: {e}")
            return False
    
    async def _process_message_batch(self, to_agent: str):
        """Process batched messages for efficiency"""
        if not self.message_queue[to_agent]:
            return
        
        messages = self.message_queue[to_agent].copy()
        self.message_queue[to_agent].clear()
        
        # Here would be the actual message delivery logic
        # For now, we simulate processing
        await asyncio.sleep(0.001)  # Simulate network latency
        
        self.communication_stats["messages_received"] += len(messages)
        
        logger.debug(f"Processed batch of {len(messages)} messages for {to_agent}")
    
    async def start_batch_processor(self):
        """Start periodic batch processing"""
        while True:
            try:
                for agent_id in list(self.message_queue.keys()):
                    if self.message_queue[agent_id]:
                        await self._process_message_batch(agent_id)
                
                await asyncio.sleep(self.batch_timeout)
                
            except Exception as e:
                logger.error(f"Error in batch processor: {e}")
                await asyncio.sleep(1)
    
    def get_communication_stats(self) -> Dict[str, Any]:
        """Get communication statistics"""
        if self.communication_stats["messages_sent"] > 0:
            self.communication_stats["avg_latency_ms"] = self.communication_stats["total_overhead_ms"] / self.communication_stats["messages_sent"]
        
        return self.communication_stats.copy()


class AdvancedAgentCoordinator:
    """Advanced multi-agent coordination with optimization"""
    
    def __init__(self):
        self.task_queue = TaskQueue()
        self.resource_manager = ResourceManager()
        self.communication_optimizer = CommunicationOptimizer()
        
        self.active_agents: Dict[str, AgentInstance] = {}
        self.completed_tasks: Dict[str, Any] = {}
        self.failed_tasks: Dict[str, Any] = {}
          # Performance tracking
        self.metrics_history: List[CoordinationMetrics] = []
        self.execution_times: deque = deque(maxlen=100)
        self.scaling_events = 0
        
        # Configuration
        self.max_concurrent_agents = 10
        self.agent_timeout = 300.0  # 5 minutes
        self.heartbeat_interval = 30  # seconds
        self.scaling_threshold = 0.8  # 80% resource utilization
        
    async def initialize(self):
        """Initialize coordination system"""
        try:
            # Start background tasks
            asyncio.create_task(self._heartbeat_monitor())
            asyncio.create_task(self._metrics_collection_loop())
            asyncio.create_task(self._dynamic_scaling_loop())
            asyncio.create_task(self._token_refresh_loop())
            asyncio.create_task(self.communication_optimizer.start_batch_processor())
            
            logger.info("Advanced agent coordinator initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize agent coordinator: {e}")
            raise
    
    async def submit_task(self, task: AgentTask) -> str:
        """Submit task for execution"""
        try:
            # Register session with memory optimizer
            memory_optimizer = get_memory_optimizer()
            await memory_optimizer.register_session(task.session_id, {"task_id": task.task_id})
            
            # Add to queue
            self.task_queue.add_task(task)
            
            # Try to execute immediately if resources available
            await self._process_task_queue()
            
            security_logger.log_security_event("TASK_SUBMITTED", {
                "task_id": task.task_id,
                "agent_type": task.agent_type,
                "priority": task.priority.name,
                "session_id": task.session_id
            })
            
            return task.task_id
            
        except Exception as e:
            logger.error(f"Error submitting task: {e}")
            raise
    
    async def _process_task_queue(self):
        """Process queued tasks"""
        while len(self.active_agents) < self.max_concurrent_agents:
            task = self.task_queue.get_next_task()
            if not task:
                break
            
            # Check resource availability
            if not self.resource_manager.can_allocate(task.task_id, task.resources_required):
                # Put task back in queue
                self.task_queue.queues[task.priority].appendleft(task)
                break
            
            # Start agent execution
            await self._start_agent_execution(task)
    
    async def _start_agent_execution(self, task: AgentTask):
        """Start agent execution for task"""
        try:
            instance_id = f"{task.agent_type}_{task.task_id}_{int(time.time())}"
            
            # Allocate resources
            if not self.resource_manager.allocate_resources(instance_id, task.resources_required):
                logger.warning(f"Failed to allocate resources for task {task.task_id}")
                return
            
            # Create agent instance
            agent_instance = AgentInstance(
                instance_id=instance_id,
                agent_type=task.agent_type,
                task_id=task.task_id,
                session_id=task.session_id,
                status=AgentStatus.RUNNING,
                started_at=datetime.utcnow(),
                last_heartbeat=datetime.utcnow(),
                resources_allocated=task.resources_required
            )
            
            self.active_agents[instance_id] = agent_instance
            
            # Start execution
            asyncio.create_task(self._execute_agent_task(agent_instance, task))
            
            logger.info(f"Started agent {instance_id} for task {task.task_id}")
            
        except Exception as e:
            logger.error(f"Error starting agent execution: {e}")
            self.resource_manager.deallocate_resources(instance_id)
    
    async def _execute_agent_task(self, agent_instance: AgentInstance, task: AgentTask):
        """Execute agent task with monitoring"""
        start_time = time.time()
        
        try:
            # Update heartbeat
            agent_instance.last_heartbeat = datetime.utcnow()
            
            # Simulate agent execution (replace with actual agent logic)
            await self._simulate_agent_work(task)
            
            # Mark as completed
            agent_instance.status = AgentStatus.COMPLETED
            agent_instance.output = {"result": "Task completed successfully"}
            
            execution_time = time.time() - start_time
            self.execution_times.append(execution_time)
            
            # Record completion
            self.completed_tasks[task.task_id] = {
                "task": task,
                "instance": agent_instance,
                "execution_time": execution_time,
                "completed_at": datetime.utcnow()
            }
            
            # Mark task as completed in queue
            self.task_queue.mark_completed(task.task_id)
            
            security_logger.log_security_event("TASK_COMPLETED", {
                "task_id": task.task_id,
                "instance_id": agent_instance.instance_id,
                "execution_time": execution_time
            })
            
        except asyncio.TimeoutError:
            agent_instance.status = AgentStatus.TIMEOUT
            agent_instance.error = "Task timeout"
            await self._handle_task_failure(agent_instance, task, "timeout")
            
        except Exception as e:
            agent_instance.status = AgentStatus.FAILED
            agent_instance.error = str(e)
            await self._handle_task_failure(agent_instance, task, str(e))
            
        finally:
            # Cleanup
            await self._cleanup_agent_instance(agent_instance)
    
    async def _simulate_agent_work(self, task: AgentTask):
        """Simulate agent work (replace with actual agent execution)"""
        # Simulate different execution times based on task type
        base_time = {
            "supervisor": 2.0,
            "researcher": 5.0,
            "coder": 10.0,
            "testing": 3.0,
            "reviewer": 4.0
        }.get(task.agent_type, 3.0)
        
        # Add some randomness
        import random
        execution_time = base_time * (0.5 + random.random())
        
        # Simulate timeout handling
        await asyncio.wait_for(asyncio.sleep(execution_time), timeout=task.timeout)
    
    async def _handle_task_failure(self, agent_instance: AgentInstance, task: AgentTask, error: str):
        """Handle task failure with retry logic"""
        logger.warning(f"Task {task.task_id} failed: {error}")
        
        self.failed_tasks[task.task_id] = {
            "task": task,
            "instance": agent_instance,
            "error": error,
            "failed_at": datetime.utcnow()
        }
        
        # Retry logic
        if task.retries < task.max_retries:
            task.retries += 1
            logger.info(f"Retrying task {task.task_id} (attempt {task.retries}/{task.max_retries})")
            self.task_queue.add_task(task)
        
        security_logger.log_security_event("TASK_FAILED", {
            "task_id": task.task_id,
            "instance_id": agent_instance.instance_id,
            "error": error,
            "retries": task.retries
        })
    
    async def _cleanup_agent_instance(self, agent_instance: AgentInstance):
        """Clean up agent instance"""
        try:
            # Deallocate resources
            self.resource_manager.deallocate_resources(agent_instance.instance_id)
            
            # Remove from active agents
            self.active_agents.pop(agent_instance.instance_id, None)
            
            # Update memory optimizer
            memory_optimizer = get_memory_optimizer()
            await memory_optimizer.remove_session(agent_instance.session_id)
            
            # Process more tasks
            await self._process_task_queue()
            
        except Exception as e:
            logger.error(f"Error cleaning up agent instance: {e}")
    
    async def _heartbeat_monitor(self):
        """Monitor agent heartbeats and handle timeouts"""
        while True:
            try:
                current_time = datetime.utcnow()
                timeout_instances = []
                
                for instance_id, agent in self.active_agents.items():
                    if (current_time - agent.last_heartbeat).total_seconds() > self.heartbeat_interval * 2:
                        timeout_instances.append(instance_id)
                
                for instance_id in timeout_instances:
                    agent = self.active_agents[instance_id]
                    logger.warning(f"Agent {instance_id} heartbeat timeout")
                    agent.status = AgentStatus.TIMEOUT
                    await self._cleanup_agent_instance(agent)
                
                await asyncio.sleep(self.heartbeat_interval)
                
            except Exception as e:
                logger.error(f"Error in heartbeat monitor: {e}")
                await asyncio.sleep(30)
    
    async def _dynamic_scaling_loop(self):
        """Dynamic scaling based on resource utilization"""
        while True:
            try:
                utilization = self.resource_manager.get_utilization()
                avg_utilization = sum(utilization.values()) / len(utilization)
                
                if avg_utilization > self.scaling_threshold * 100:
                    # Scale up logic (would integrate with Kubernetes HPA)
                    self.scaling_events += 1
                    logger.info(f"High resource utilization detected: {avg_utilization:.1f}%")
                    
                    # Could trigger additional agent instances or resource allocation
                    
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in dynamic scaling: {e}")
                await asyncio.sleep(60)
    
    async def _token_refresh_loop(self):
        """Refresh LLM tokens periodically"""
        while True:
            try:
                self.resource_manager.refresh_llm_tokens()
                await asyncio.sleep(60)  # Refresh every minute
                
            except Exception as e:
                logger.error(f"Error refreshing tokens: {e}")
                await asyncio.sleep(60)
    
    async def _metrics_collection_loop(self):
        """Collect coordination metrics"""
        while True:
            try:
                await self._collect_coordination_metrics()
                await asyncio.sleep(60)  # Collect every minute
                
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
                await asyncio.sleep(60)
    
    async def _collect_coordination_metrics(self):
        """Collect current coordination metrics"""
        try:
            queue_stats = self.task_queue.get_queue_stats()
            utilization = self.resource_manager.get_utilization()
            comm_stats = self.communication_optimizer.get_communication_stats()
            
            avg_execution_time = sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0
            
            # Calculate parallel efficiency
            total_tasks = len(self.completed_tasks) + len(self.failed_tasks)
            parallel_efficiency = (len(self.completed_tasks) / total_tasks * 100) if total_tasks > 0 else 100
            
            metrics = CoordinationMetrics(
                active_agents=len(self.active_agents),
                queued_tasks=queue_stats["total_pending"],
                completed_tasks=len(self.completed_tasks),
                failed_tasks=len(self.failed_tasks),
                avg_execution_time=avg_execution_time,
                resource_utilization=utilization,
                parallel_efficiency=parallel_efficiency,
                communication_overhead_ms=comm_stats.get("avg_latency_ms", 0),
                dynamic_scaling_events=self.scaling_events,
                timestamp=datetime.utcnow()
            )
            
            self.metrics_history.append(metrics)
            
            # Keep only last 100 metrics
            if len(self.metrics_history) > 100:
                self.metrics_history.pop(0)
            
            # Send to monitoring
            await get_monitoring().record_metric("agent_active_agents", metrics.active_agents)
            await get_monitoring().record_metric("agent_queued_tasks", metrics.queued_tasks)
            await get_monitoring().record_metric("agent_completed_tasks", metrics.completed_tasks)
            await get_monitoring().record_metric("agent_parallel_efficiency", metrics.parallel_efficiency)
            
        except Exception as e:
            logger.error(f"Error collecting coordination metrics: {e}")
    
    def get_coordination_metrics(self) -> Dict[str, Any]:
        """Get current coordination metrics"""
        if not self.metrics_history:
            return {"error": "No metrics available"}
        
        current_metrics = self.metrics_history[-1]
        queue_stats = self.task_queue.get_queue_stats()
        utilization = self.resource_manager.get_utilization()
        comm_stats = self.communication_optimizer.get_communication_stats()
        
        return {
            "current": asdict(current_metrics),
            "queue": queue_stats,
            "resources": {
                "utilization": utilization,
                "pool": asdict(self.resource_manager.resource_pool),
                "allocated": len(self.resource_manager.allocated_resources)
            },
            "communication": comm_stats,
            "active_agents": {
                agent_id: {
                    "agent_type": agent.agent_type,
                    "status": agent.status.value,
                    "started_at": agent.started_at.isoformat(),
                    "task_id": agent.task_id
                } for agent_id, agent in self.active_agents.items()
            }
        }
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of specific task"""
        # Check active agents
        for agent in self.active_agents.values():
            if agent.task_id == task_id:
                return {
                    "status": agent.status.value,
                    "instance_id": agent.instance_id,
                    "started_at": agent.started_at.isoformat(),
                    "progress": "running"
                }
        
        # Check completed tasks
        if task_id in self.completed_tasks:
            task_info = self.completed_tasks[task_id]
            return {
                "status": "completed",
                "execution_time": task_info["execution_time"],
                "completed_at": task_info["completed_at"].isoformat(),
                "output": task_info["instance"].output
            }
        
        # Check failed tasks
        if task_id in self.failed_tasks:
            task_info = self.failed_tasks[task_id]
            return {
                "status": "failed",
                "error": task_info["error"],
                "failed_at": task_info["failed_at"].isoformat(),
                "retries": task_info["task"].retries
            }
        
        # Check pending queue
        if task_id in self.task_queue.pending_tasks:
            return {
                "status": "queued",
                "priority": self.task_queue.pending_tasks[task_id].priority.name,
                "dependencies": self.task_queue.pending_tasks[task_id].dependencies
            }
        
        return {"status": "not_found"}
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel task execution"""
        try:
            # Find and stop active agent
            for instance_id, agent in self.active_agents.items():
                if agent.task_id == task_id:
                    agent.status = AgentStatus.FAILED
                    await self._cleanup_agent_instance(agent)
                    return True
            
            # Remove from pending queue
            if task_id in self.task_queue.pending_tasks:
                del self.task_queue.pending_tasks[task_id]
                # Remove from priority queues
                for queue in self.task_queue.queues.values():
                    queue = deque([task for task in queue if task.task_id != task_id])
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error canceling task {task_id}: {e}")
            return False
    
    async def close(self):
        """Close coordination system"""
        # Cancel all active tasks
        for instance_id in list(self.active_agents.keys()):
            agent = self.active_agents[instance_id]
            await self._cleanup_agent_instance(agent)
        
        logger.info("Advanced agent coordinator closed")


# Global instance
advanced_coordination = AdvancedAgentCoordinator()


def get_advanced_coordination():
    """Get advanced coordination instance"""
    return advanced_coordination




