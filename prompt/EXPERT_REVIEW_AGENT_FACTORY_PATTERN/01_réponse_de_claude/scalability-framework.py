from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
import asyncio
import aioredis
from collections import defaultdict
import time
import random
from abc import ABC, abstractmethod
import logging

# === Agent Pool Management ===

@dataclass
class PoolConfig:
    """Configuration pour un pool d'agents"""
    min_size: int = 1
    max_size: int = 10
    scale_up_threshold: float = 0.8  # 80% d'utilisation
    scale_down_threshold: float = 0.2  # 20% d'utilisation
    health_check_interval: int = 30  # secondes
    idle_timeout: int = 300  # secondes avant destruction

class AgentPool:
    """Pool d'agents avec auto-scaling"""
    
    def __init__(
        self,
        factory: 'AgentFactory',
        template_name: str,
        config: PoolConfig = None
    ):
        self.factory = factory
        self.template_name = template_name
        self.config = config or PoolConfig()
        self.agents: List[BaseAgent] = []
        self.available_agents: asyncio.Queue = asyncio.Queue()
        self.metrics = {
            "total_requests": 0,
            "active_agents": 0,
            "queued_requests": 0,
            "avg_wait_time": 0.0
        }
        self._scaling_task = None
    
    async def initialize(self):
        """Initialise le pool avec le nombre minimum d'agents"""
        for _ in range(self.config.min_size):
            agent = await self.factory.create_agent(self.template_name)
            self.agents.append(agent)
            await self.available_agents.put(agent)
        
        # Démarrer l'auto-scaling
        self._scaling_task = asyncio.create_task(self._auto_scale_loop())
    
    async def acquire_agent(self, timeout: Optional[float] = None) -> BaseAgent:
        """Acquiert un agent du pool"""
        start_time = time.time()
        self.metrics["queued_requests"] += 1
        
        try:
            agent = await asyncio.wait_for(
                self.available_agents.get(),
                timeout=timeout
            )
            wait_time = time.time() - start_time
            self.metrics["avg_wait_time"] = (
                self.metrics["avg_wait_time"] * 0.9 + wait_time * 0.1
            )
            self.metrics["active_agents"] += 1
            return agent
        finally:
            self.metrics["queued_requests"] -= 1
    
    async def release_agent(self, agent: BaseAgent):
        """Libère un agent vers le pool"""
        self.metrics["active_agents"] -= 1
        await self.available_agents.put(agent)
    
    async def _auto_scale_loop(self):
        """Boucle d'auto-scaling"""
        while True:
            await asyncio.sleep(self.config.health_check_interval)
            
            utilization = self._calculate_utilization()
            
            if utilization > self.config.scale_up_threshold:
                await self._scale_up()
            elif utilization < self.config.scale_down_threshold:
                await self._scale_down()
    
    def _calculate_utilization(self) -> float:
        """Calcule le taux d'utilisation du pool"""
        if not self.agents:
            return 0.0
        return self.metrics["active_agents"] / len(self.agents)
    
    async def _scale_up(self):
        """Augmente la taille du pool"""
        if len(self.agents) < self.config.max_size:
            new_agent = await self.factory.create_agent(self.template_name)
            self.agents.append(new_agent)
            await self.available_agents.put(new_agent)
            logging.info(f"Scaled up pool to {len(self.agents)} agents")
    
    async def _scale_down(self):
        """Réduit la taille du pool"""
        if len(self.agents) > self.config.min_size:
            # Retirer un agent disponible
            try:
                agent = await asyncio.wait_for(
                    self.available_agents.get(),
                    timeout=1.0
                )
                self.agents.remove(agent)
                # Cleanup de l'agent
                logging.info(f"Scaled down pool to {len(self.agents)} agents")
            except asyncio.TimeoutError:
                pass  # Tous les agents sont occupés

# === Distributed Cache ===

class DistributedCache:
    """Cache distribué pour templates et résultats"""
    
    def __init__(self, redis_url: str = "redis://localhost"):
        self.redis_url = redis_url
        self.redis = None
        self.local_cache = {}  # Cache L1 local
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }
    
    async def connect(self):
        """Connexion à Redis"""
        self.redis = await aioredis.create_redis_pool(self.redis_url)
    
    async def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache"""
        # Check L1 cache
        if key in self.local_cache:
            self.cache_stats["hits"] += 1
            return self.local_cache[key]
        
        # Check L2 cache (Redis)
        if self.redis:
            value = await self.redis.get(key)
            if value:
                self.cache_stats["hits"] += 1
                # Populate L1
                self.local_cache[key] = value
                return value
        
        self.cache_stats["misses"] += 1
        return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ):
        """Stocke une valeur dans le cache"""
        # L1 cache
        self.local_cache[key] = value
        
        # L2 cache avec TTL
        if self.redis:
            if ttl:
                await self.redis.setex(key, ttl, value)
            else:
                await self.redis.set(key, value)
    
    async def invalidate(self, pattern: str):
        """Invalide les entrées correspondant au pattern"""
        # Invalider L1
        keys_to_remove = [k for k in self.local_cache if pattern in k]
        for key in keys_to_remove:
            del self.local_cache[key]
            self.cache_stats["evictions"] += 1
        
        # Invalider L2
        if self.redis:
            async for key in self.redis.iscan(match=f"*{pattern}*"):
                await self.redis.delete(key)

# === Load Balancer ===

class LoadBalancingStrategy(ABC):
    """Stratégie abstraite de load balancing"""
    
    @abstractmethod
    def select_agent(self, agents: List[BaseAgent]) -> Optional[BaseAgent]:
        """Sélectionne un agent selon la stratégie"""
        pass

class RoundRobinStrategy(LoadBalancingStrategy):
    """Stratégie Round Robin"""
    
    def __init__(self):
        self.index = 0
    
    def select_agent(self, agents: List[BaseAgent]) -> Optional[BaseAgent]:
        if not agents:
            return None
        agent = agents[self.index % len(agents)]
        self.index += 1
        return agent

class LeastConnectionsStrategy(LoadBalancingStrategy):
    """Stratégie Least Connections"""
    
    def __init__(self):
        self.connections = defaultdict(int)
    
    def select_agent(self, agents: List[BaseAgent]) -> Optional[BaseAgent]:
        if not agents:
            return None
        return min(agents, key=lambda a: self.connections[a.metadata.id])

class WeightedRandomStrategy(LoadBalancingStrategy):
    """Stratégie Random pondérée par performance"""
    
    def select_agent(self, agents: List[BaseAgent]) -> Optional[BaseAgent]:
        if not agents:
            return None
        
        # Pondération basée sur le taux de succès
        weights = []
        for agent in agents:
            success_rate = agent.performance_metrics.get("success_rate", 0.5)
            weights.append(max(0.1, success_rate))  # Min weight 0.1
        
        return random.choices(agents, weights=weights)[0]

class AgentLoadBalancer:
    """Load balancer pour distribuer les requêtes"""
    
    def __init__(
        self,
        strategy: LoadBalancingStrategy = None,
        health_check_interval: int = 30
    ):
        self.strategy = strategy or RoundRobinStrategy()
        self.agent_pools: Dict[str, AgentPool] = {}
        self.health_check_interval = health_check_interval
        self._health_check_task = None
    
    async def register_pool(self, domain: str, pool: AgentPool):
        """Enregistre un pool d'agents pour un domaine"""
        self.agent_pools[domain] = pool
        await pool.initialize()
    
    async def route_request(
        self,
        domain: str,
        request: Dict[str, Any],
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """Route une requête vers un agent approprié"""
        pool = self.agent_pools.get(domain)
        if not pool:
            raise ValueError(f"No agent pool for domain: {domain}")
        
        # Acquérir un agent du pool
        agent = await pool.acquire_agent(timeout)
        
        try:
            # Traiter la requête
            result = await agent.process(
                request.get("data"),
                request.get("context", {})
            )
            return result
        finally:
            # Toujours libérer l'agent
            await pool.release_agent(agent)
    
    async def start_health_checks(self):
        """Démarre les health checks périodiques"""
        self._health_check_task = asyncio.create_task(self._health_check_loop())
    
    async def _health_check_loop(self):
        """Boucle de health check"""
        while True:
            await asyncio.sleep(self.health_check_interval)
            
            for domain, pool in self.agent_pools.items():
                # Vérifier la santé de chaque agent
                unhealthy_agents = []
                for agent in pool.agents:
                    if not await self._check_agent_health(agent):
                        unhealthy_agents.append(agent)
                
                # Remplacer les agents non sains
                for agent in unhealthy_agents:
                    logging.warning(f"Replacing unhealthy agent: {agent.metadata.id}")
                    pool.agents.remove(agent)
                    new_agent = await pool.factory.create_agent(pool.template_name)
                    pool.agents.append(new_agent)
                    await pool.available_agents.put(new_agent)
    
    async def _check_agent_health(self, agent: BaseAgent) -> bool:
        """Vérifie la santé d'un agent"""
        try:
            # Health check simple
            result = await asyncio.wait_for(
                agent.process({"health": "check"}, {"type": "health_check"}),
                timeout=5.0
            )
            return result.get("status") == "healthy"
        except:
            return False

# === Distributed Orchestrator ===

class DistributedOrchestrator:
    """Orchestrateur distribué pour coordination multi-nœuds"""
    
    def __init__(
        self,
        node_id: str,
        coordinator_url: str = "redis://localhost"
    ):
        self.node_id = node_id
        self.coordinator_url = coordinator_url
        self.redis = None
        self.is_leader = False
        self.nodes = {}
        self.load_balancer = AgentLoadBalancer()
        self.cache = DistributedCache(coordinator_url)
    
    async def initialize(self):
        """Initialise l'orchestrateur"""
        # Connexion au coordinateur
        self.redis = await aioredis.create_redis_pool(self.coordinator_url)
        await self.cache.connect()
        
        # Enregistrement du nœud
        await self._register_node()
        
        # Élection du leader
        await self._leader_election()
        
        # Démarrer la synchronisation
        asyncio.create_task(self._sync_loop())
    
    async def _register_node(self):
        """Enregistre ce nœud dans le cluster"""
        node_info = {
            "id": self.node_id,
            "timestamp": time.time(),
            "status": "active",
            "capacity": {
                "cpu": 100,
                "memory": 4096,
                "agents": 0
            }
        }
        await self.redis.setex(
            f"node:{self.node_id}",
            60,  # TTL 60 secondes
            str(node_info)
        )
    
    async def _leader_election(self):
        """Élection du leader via Redis"""
        # Tentative d'acquérir le lock de leader
        lock_acquired = await self.redis.set(
            "cluster:leader",
            self.node_id,
            expire=30,  # Leader lease 30 secondes
            exist=False  # Seulement si n'existe pas
        )
        self.is_leader = bool(lock_acquired)
        
        if self.is_leader:
            logging.info(f"Node {self.node_id} elected as leader")
            asyncio.create_task(self._leader_duties())
    
    async def _leader_duties(self):
        """Tâches du leader"""
        while self.is_leader:
            # Renouveler le lease
            await self.redis.expire("cluster:leader", 30)
            
            # Monitorer les nœuds
            await self._monitor_nodes()
            
            # Rééquilibrer la charge si nécessaire
            await self._rebalance_load()
            
            await asyncio.sleep(10)
    
    async def _monitor_nodes(self):
        """Surveille l'état des nœuds"""
        pattern = "node:*"
        async for key in self.redis.iscan(match=pattern):
            node_data = await self.redis.get(key)
            if node_data:
                node = eval(node_data)  # En prod: json.loads
                self.nodes[node["id"]] = node
    
    async def _rebalance_load(self):
        """Rééquilibre la charge entre les nœuds"""
        if len(self.nodes) < 2:
            return
        
        # Calculer la charge moyenne
        total_agents = sum(n["capacity"]["agents"] for n in self.nodes.values())
        avg_agents = total_agents / len(self.nodes)
        
        # Identifier les nœuds surchargés/sous-chargés
        overloaded = [n for n in self.nodes.values() 
                      if n["capacity"]["agents"] > avg_agents * 1.2]
        underloaded = [n for n in self.nodes.values() 
                       if n["capacity"]["agents"] < avg_agents * 0.8]
        
        # Envoyer des commandes de migration
        for over_node in overloaded:
            for under_node in underloaded:
                await self._migrate_agents(over_node["id"], under_node["id"])
    
    async def _migrate_agents(self, from_node: str, to_node: str):
        """Migre des agents d'un nœud à l'autre"""
        # Publier une commande de migration
        migration_cmd = {
            "type": "migrate_agents",
            "from": from_node,
            "to": to_node,
            "count": 1
        }
        await self.redis.publish("cluster:commands", str(migration_cmd))
    
    async def _sync_loop(self):
        """Boucle de synchronisation avec le cluster"""
        while True:
            # Heartbeat
            await self._register_node()
            
            # Vérifier si toujours leader
            if self.is_leader:
                current_leader = await self.redis.get("cluster:leader")
                if current_leader != self.node_id:
                    self.is_leader = False
                    logging.info(f"Node {self.node_id} is no longer leader")
            else:
                # Tenter de devenir leader si le leader actuel est mort
                await self._leader_election()
            
            await asyncio.sleep(20)

# === Performance Optimization ===

class PerformanceOptimizer:
    """Optimiseur de performance pour le système"""
    
    def __init__(self):
        self.metrics_history = defaultdict(list)
        self.optimization_rules = [
            self._optimize_pool_size,
            self._optimize_cache_ttl,
            self._optimize_timeout_values
        ]
    
    async def analyze_and_optimize(
        self,
        orchestrator: DistributedOrchestrator
    ):
        """Analyse les métriques et optimise le système"""
        # Collecter les métriques
        metrics = await self._collect_metrics(orchestrator)
        
        # Stocker l'historique
        for key, value in metrics.items():
            self.metrics_history[key].append({
                "timestamp": time.time(),
                "value": value
            })
        
        # Appliquer les règles d'optimisation
        for rule in self.optimization_rules:
            await rule(orchestrator, metrics)
    
    async def _collect_metrics(
        self,
        orchestrator: DistributedOrchestrator
    ) -> Dict[str, float]:
        """Collecte les métriques du système"""
        metrics = {
            "avg_response_time": 0.0,
            "error_rate": 0.0,
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "cache_hit_rate": 0.0
        }
        
        # Agrégation des métriques des pools
        for pool in orchestrator.load_balancer.agent_pools.values():
            metrics["avg_response_time"] += pool.metrics.get("avg_wait_time", 0)
        
        # Cache hit rate
        if orchestrator.cache.cache_stats["hits"] + orchestrator.cache.cache_stats["misses"] > 0:
            metrics["cache_hit_rate"] = (
                orchestrator.cache.cache_stats["hits"] /
                (orchestrator.cache.cache_stats["hits"] + orchestrator.cache.cache_stats["misses"])
            )
        
        return metrics
    
    async def _optimize_pool_size(
        self,
        orchestrator: DistributedOrchestrator,
        metrics: Dict[str, float]
    ):
        """Optimise la taille des pools d'agents"""
        avg_wait_time = metrics.get("avg_response_time", 0)
        
        # Si temps d'attente élevé, augmenter les pools
        if avg_wait_time > 1.0:  # Plus d'1 seconde d'attente
            for pool in orchestrator.load_balancer.agent_pools.values():
                pool.config.min_size = min(pool.config.min_size + 1, 20)
                pool.config.max_size = min(pool.config.max_size + 2, 50)
        
        # Si temps d'attente faible, réduire les pools
        elif avg_wait_time < 0.1:  # Moins de 100ms
            for pool in orchestrator.load_balancer.agent_pools.values():
                pool.config.min_size = max(pool.config.min_size - 1, 1)
                pool.config.max_size = max(pool.config.max_size - 2, 5)
    
    async def _optimize_cache_ttl(
        self,
        orchestrator: DistributedOrchestrator,
        metrics: Dict[str, float]
    ):
        """Optimise les TTL du cache"""
        hit_rate = metrics.get("cache_hit_rate", 0)
        
        # Ajuster les TTL en fonction du hit rate
        if hit_rate < 0.7:  # Moins de 70% de hits
            # Augmenter les TTL pour garder plus longtemps en cache
            logging.info("Increasing cache TTL due to low hit rate")
        elif hit_rate > 0.95:  # Plus de 95% de hits
            # Possibilité de réduire les TTL pour économiser la mémoire
            logging.info("Cache performing well, considering TTL optimization")
    
    async def _optimize_timeout_values(
        self,
        orchestrator: DistributedOrchestrator,
        metrics: Dict[str, float]
    ):
        """Optimise les valeurs de timeout"""
        error_rate = metrics.get("error_rate", 0)
        
        # Si taux d'erreur élevé, augmenter les timeouts
        if error_rate > 0.05:  # Plus de 5% d'erreurs
            logging.warning(f"High error rate: {error_rate:.2%}, increasing timeouts")

# === Batch Processing ===

class BatchProcessor:
    """Processeur de requêtes par batch pour efficacité"""
    
    def __init__(
        self,
        batch_size: int = 10,
        batch_timeout: float = 0.1
    ):
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.pending_requests: List[Dict[str, Any]] = []
        self.results_futures: Dict[str, asyncio.Future] = {}
        self._batch_task = None
    
    async def start(self):
        """Démarre le processeur de batch"""
        self._batch_task = asyncio.create_task(self._batch_loop())
    
    async def submit_request(
        self,
        request_id: str,
        data: Any
    ) -> Any:
        """Soumet une requête au batch"""
        future = asyncio.Future()
        self.results_futures[request_id] = future
        
        self.pending_requests.append({
            "id": request_id,
            "data": data,
            "timestamp": time.time()
        })
        
        # Si batch plein, traiter immédiatement
        if len(self.pending_requests) >= self.batch_size:
            await self._process_batch()
        
        return await future
    
    async def _batch_loop(self):
        """Boucle de traitement des batchs"""
        while True:
            await asyncio.sleep(self.batch_timeout)
            
            if self.pending_requests:
                await self._process_batch()
    
    async def _process_batch(self):
        """Traite un batch de requêtes"""
        if not self.pending_requests:
            return
        
        # Extraire le batch
        batch = self.pending_requests[:self.batch_size]
        self.pending_requests = self.pending_requests[self.batch_size:]
        
        try:
            # Traitement parallèle du batch
            tasks = [self._process_single(req) for req in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Retourner les résultats
            for req, result in zip(batch, results):
                future = self.results_futures.pop(req["id"], None)
                if future and not future.done():
                    if isinstance(result, Exception):
                        future.set_exception(result)
                    else:
                        future.set_result(result)
        
        except Exception as e:
            # En cas d'erreur, rejeter toutes les futures du batch
            for req in batch:
                future = self.results_futures.pop(req["id"], None)
                if future and not future.done():
                    future.set_exception(e)
    
    async def _process_single(self, request: Dict[str, Any]) -> Any:
        """Traite une requête individuelle"""
        # Implémentation spécifique au domaine
        return {"processed": request["data"]}

# === Horizontal Scaling Manager ===

class HorizontalScalingManager:
    """Gestionnaire de scaling horizontal avec Kubernetes"""
    
    def __init__(
        self,
        min_replicas: int = 1,
        max_replicas: int = 10,
        target_cpu_percent: int = 70,
        target_memory_percent: int = 80
    ):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.target_cpu_percent = target_cpu_percent
        self.target_memory_percent = target_memory_percent
        self.current_replicas = min_replicas
        self.scaling_history = []
    
    async def evaluate_scaling(
        self,
        metrics: Dict[str, float]
    ) -> int:
        """Évalue le besoin de scaling"""
        cpu_usage = metrics.get("cpu_usage", 0)
        memory_usage = metrics.get("memory_usage", 0)
        queue_length = metrics.get("queue_length", 0)
        
        # Calcul du nombre de replicas souhaité
        cpu_based = self._calculate_replicas_for_metric(
            cpu_usage, self.target_cpu_percent
        )
        memory_based = self._calculate_replicas_for_metric(
            memory_usage, self.target_memory_percent
        )
        queue_based = self._calculate_replicas_for_queue(queue_length)
        
        # Prendre le maximum pour être sûr
        desired_replicas = max(cpu_based, memory_based, queue_based)
        
        # Respecter les limites
        desired_replicas = max(self.min_replicas, 
                              min(desired_replicas, self.max_replicas))
        
        # Enregistrer la décision
        self.scaling_history.append({
            "timestamp": time.time(),
            "current": self.current_replicas,
            "desired": desired_replicas,
            "metrics": metrics
        })
        
        return desired_replicas
    
    def _calculate_replicas_for_metric(
        self,
        current_usage: float,
        target_usage: float
    ) -> int:
        """Calcule le nombre de replicas pour une métrique"""
        if target_usage == 0:
            return self.min_replicas
        
        return int(self.current_replicas * (current_usage / target_usage))
    
    def _calculate_replicas_for_queue(
        self,
        queue_length: int,
        target_queue_per_replica: int = 10
    ) -> int:
        """Calcule le nombre de replicas basé sur la queue"""
        if target_queue_per_replica == 0:
            return self.min_replicas
        
        return max(1, queue_length // target_queue_per_replica)
    
    async def apply_scaling(self, desired_replicas: int):
        """Applique la décision de scaling"""
        if desired_replicas != self.current_replicas:
            logging.info(
                f"Scaling from {self.current_replicas} to {desired_replicas} replicas"
            )
            
            # En production : appeler l'API Kubernetes
            # await self._update_k8s_deployment(desired_replicas)
            
            self.current_replicas = desired_replicas

# === Message Queue Integration ===

class MessageQueueIntegration:
    """Intégration avec système de message queue pour async processing"""
    
    def __init__(
        self,
        queue_url: str = "amqp://localhost"
    ):
        self.queue_url = queue_url
        self.connection = None
        self.channel = None
        self.consumers = {}
    
    async def connect(self):
        """Connexion au message broker"""
        # Utiliser aio-pika en production
        pass
    
    async def publish_task(
        self,
        queue_name: str,
        task: Dict[str, Any],
        priority: int = 0
    ):
        """Publie une tâche dans la queue"""
        message = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "priority": priority,
            "task": task
        }
        
        # Publier avec priorité
        # await self.channel.basic_publish(...)
        
    async def consume_tasks(
        self,
        queue_name: str,
        handler: Callable,
        concurrency: int = 10
    ):
        """Consomme les tâches de la queue"""
        async def process_message(message):
            try:
                result = await handler(message["task"])
                # Acknowledge message
            except Exception as e:
                # Requeue or dead letter
                logging.error(f"Task processing failed: {e}")
        
        # Créer des workers concurrents
        workers = []
        for _ in range(concurrency):
            worker = asyncio.create_task(self._worker_loop(queue_name, process_message))
            workers.append(worker)
        
        self.consumers[queue_name] = workers
    
    async def _worker_loop(self, queue_name: str, handler: Callable):
        """Boucle de travail pour consumer"""
        while True:
            # Récupérer message de la queue
            # message = await self.channel.basic_get(queue_name)
            # if message:
            #     await handler(message)
            await asyncio.sleep(0.1)

# === Exemple d'utilisation complète ===

async def scalability_example():
    """Exemple d'utilisation du framework de scalabilité"""
    
    # Configuration
    orchestrator = DistributedOrchestrator(
        node_id="node-001",
        coordinator_url="redis://localhost"
    )
    await orchestrator.initialize()
    
    # Factory et Registry
    registry = AgentRegistry()
    factory = AgentFactory(registry)
    
    # Template pour processing
    processing_template = {
        "name": "data_processor",
        "role": "processor",
        "domain": "data_processing",
        "capabilities": ["analysis", "transformation"],
        "default_config": {
            "batch_mode": True,
            "max_batch_size": 100
        }
    }
    registry.register_template("data_processor", processing_template)
    
    # Créer un pool d'agents avec auto-scaling
    pool_config = PoolConfig(
        min_size=2,
        max_size=20,
        scale_up_threshold=0.7,
        scale_down_threshold=0.3
    )
    
    processing_pool = AgentPool(factory, "data_processor", pool_config)
    await orchestrator.load_balancer.register_pool("data_processing", processing_pool)
    
    # Démarrer les composants
    await orchestrator.load_balancer.start_health_checks()
    
    # Optimiseur de performance
    optimizer = PerformanceOptimizer()
    
    # Batch processor
    batch_processor = BatchProcessor(batch_size=50, batch_timeout=0.5)
    await batch_processor.start()
    
    # Scaling manager
    scaling_manager = HorizontalScalingManager(
        min_replicas=1,
        max_replicas=10,
        target_cpu_percent=70
    )
    
    # Simulation de charge
    async def simulate_load():
        """Simule une charge de travail variable"""
        for i in range(100):
            # Charge variable
            load = 10 if i < 30 else 50 if i < 70 else 20
            
            # Générer des requêtes
            tasks = []
            for j in range(load):
                request = {
                    "data": f"request_{i}_{j}",
                    "context": {"batch": i}
                }
                
                # Via batch processor pour efficacité
                task = batch_processor.submit_request(
                    f"req_{i}_{j}",
                    request
                )
                tasks.append(task)
            
            # Attendre les résultats
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Optimisation périodique
            if i % 10 == 0:
                await optimizer.analyze_and_optimize(orchestrator)
                
                # Évaluer le scaling
                metrics = await optimizer._collect_metrics(orchestrator)
                desired_replicas = await scaling_manager.evaluate_scaling(metrics)
                await scaling_manager.apply_scaling(desired_replicas)
            
            await asyncio.sleep(1)
    
    # Lancer la simulation
    await simulate_load()
    
    # Afficher les statistiques
    print("\n=== Performance Statistics ===")
    print(f"Cache hit rate: {orchestrator.cache.cache_stats['hits'] / (orchestrator.cache.cache_stats['hits'] + orchestrator.cache.cache_stats['misses']):.2%}")
    
    for domain, pool in orchestrator.load_balancer.agent_pools.items():
        print(f"\nPool '{domain}':")
        print(f"  Current size: {len(pool.agents)}")
        print(f"  Active agents: {pool.metrics['active_agents']}")
        print(f"  Average wait time: {pool.metrics['avg_wait_time']:.3f}s")
    
    print(f"\nScaling decisions: {len(scaling_manager.scaling_history)}")
    print(f"Current replicas: {scaling_manager.current_replicas}")

if __name__ == "__main__":
    asyncio.run(scalability_example())