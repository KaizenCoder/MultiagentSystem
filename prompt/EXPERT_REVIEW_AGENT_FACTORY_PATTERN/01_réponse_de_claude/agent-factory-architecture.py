from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Type
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import uuid
from datetime import datetime
import json
from functools import lru_cache
import inspect

# === Modèle de Domaine Enrichi ===

class AgentCapability(Enum):
    """Capacités standardisées des agents"""
    ANALYSIS = "analysis"
    GENERATION = "generation"
    VALIDATION = "validation"
    TRANSFORMATION = "transformation"
    MONITORING = "monitoring"
    ORCHESTRATION = "orchestration"

@dataclass
class AgentMetadata:
    """Métadonnées enrichies pour chaque agent"""
    id: str
    name: str
    role: str
    domain: str
    version: str = "1.0.0"
    capabilities: List[AgentCapability] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    resource_limits: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_updated: datetime = field(default_factory=datetime.utcnow)

# === Système de Plugins pour Extensibilité ===

class AgentPlugin(ABC):
    """Interface pour les plugins d'agents"""
    
    @abstractmethod
    async def on_init(self, agent: 'BaseAgent') -> None:
        """Appelé lors de l'initialisation de l'agent"""
        pass
    
    @abstractmethod
    async def on_process(self, input_data: Any, context: Dict[str, Any]) -> None:
        """Appelé avant le traitement"""
        pass
    
    @abstractmethod
    async def on_complete(self, result: Dict[str, Any]) -> None:
        """Appelé après le traitement"""
        pass

# === BaseAgent Amélioré avec Circuit Breaker ===

class CircuitBreakerState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreaker:
    """Pattern Circuit Breaker pour la résilience"""
    failure_threshold: int = 5
    recovery_timeout: float = 60.0
    failure_count: int = 0
    last_failure_time: Optional[float] = None
    state: CircuitBreakerState = CircuitBreakerState.CLOSED

class BaseAgent(ABC):
    """Classe de base enrichie avec patterns de résilience"""
    
    def __init__(
        self, 
        name: str, 
        role: str, 
        domain: str,
        capabilities: List[AgentCapability] = None,
        tools: List[str] = None,
        plugins: List[AgentPlugin] = None,
        config: Dict[str, Any] = None
    ):
        self.metadata = AgentMetadata(
            id=str(uuid.uuid4()),
            name=name,
            role=role,
            domain=domain,
            capabilities=capabilities or [],
            tools=tools or []
        )
        self.plugins = plugins or []
        self.config = config or {}
        self.circuit_breaker = CircuitBreaker()
        self._performance_tracker = PerformanceTracker()
        self._state_machine = AgentStateMachine()
        
    async def process(self, input_data: Any, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Traitement avec gestion d'erreurs et monitoring"""
        if self.circuit_breaker.state == CircuitBreakerState.OPEN:
            if not self._should_attempt_reset():
                raise Exception("Circuit breaker is OPEN")
            self.circuit_breaker.state = CircuitBreakerState.HALF_OPEN
        
        try:
            # Plugins pre-processing
            for plugin in self.plugins:
                await plugin.on_process(input_data, context)
            
            # Monitoring de performance
            with self._performance_tracker.track():
                result = await self._process_implementation(input_data, context)
            
            # Reset circuit breaker sur succès
            self._reset_circuit_breaker()
            
            # Plugins post-processing
            for plugin in self.plugins:
                await plugin.on_complete(result)
            
            return result
            
        except Exception as e:
            self._handle_failure(e)
            raise
    
    @abstractmethod
    async def _process_implementation(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """Implémentation spécifique du traitement"""
        pass
    
    def _should_attempt_reset(self) -> bool:
        """Vérifie si on peut tenter de réinitialiser le circuit breaker"""
        if self.circuit_breaker.last_failure_time:
            time_since_failure = asyncio.get_event_loop().time() - self.circuit_breaker.last_failure_time
            return time_since_failure >= self.circuit_breaker.recovery_timeout
        return False
    
    def _reset_circuit_breaker(self):
        """Réinitialise le circuit breaker"""
        self.circuit_breaker.failure_count = 0
        self.circuit_breaker.state = CircuitBreakerState.CLOSED
    
    def _handle_failure(self, error: Exception):
        """Gère les échecs et met à jour le circuit breaker"""
        self.circuit_breaker.failure_count += 1
        self.circuit_breaker.last_failure_time = asyncio.get_event_loop().time()
        
        if self.circuit_breaker.failure_count >= self.circuit_breaker.failure_threshold:
            self.circuit_breaker.state = CircuitBreakerState.OPEN

# === Factory Pattern Avancé ===

class AgentRegistry:
    """Registre centralisé des agents et templates"""
    
    def __init__(self):
        self._templates: Dict[str, Dict[str, Any]] = {}
        self._agent_classes: Dict[str, Type[BaseAgent]] = {}
        self._instances: Dict[str, BaseAgent] = {}
        self._template_cache = {}
    
    def register_template(self, name: str, template: Dict[str, Any]):
        """Enregistre un template avec validation"""
        self._validate_template(template)
        self._templates[name] = template
    
    def register_agent_class(self, name: str, agent_class: Type[BaseAgent]):
        """Enregistre une classe d'agent personnalisée"""
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(f"{agent_class} must inherit from BaseAgent")
        self._agent_classes[name] = agent_class
    
    @lru_cache(maxsize=128)
    def get_template(self, name: str) -> Dict[str, Any]:
        """Récupère un template avec cache"""
        if name not in self._templates:
            raise ValueError(f"Template '{name}' not found")
        return self._templates[name].copy()
    
    def _validate_template(self, template: Dict[str, Any]):
        """Valide la structure d'un template"""
        required_fields = ["name", "role", "domain", "capabilities"]
        for field in required_fields:
            if field not in template:
                raise ValueError(f"Template missing required field: {field}")

class DynamicAgent(BaseAgent):
    """Agent créé dynamiquement à partir d'un template"""
    
    def __init__(self, template: Dict[str, Any], custom_processors: Dict[str, Any] = None):
        super().__init__(
            name=template["name"],
            role=template["role"],
            domain=template["domain"],
            capabilities=[AgentCapability(cap) for cap in template.get("capabilities", [])],
            tools=template.get("tools", [])
        )
        self.template = template
        self.custom_processors = custom_processors or {}
    
    async def _process_implementation(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """Traitement basé sur le template et les processeurs personnalisés"""
        processor_name = context.get("processor", "default")
        
        if processor_name in self.custom_processors:
            processor = self.custom_processors[processor_name]
            if callable(processor):
                return await processor(input_data, context)
        
        # Comportement par défaut basé sur les capacités
        results = {}
        for capability in self.metadata.capabilities:
            if capability == AgentCapability.ANALYSIS:
                results["analysis"] = await self._analyze(input_data)
            elif capability == AgentCapability.GENERATION:
                results["generation"] = await self._generate(input_data)
            # ... autres capacités
        
        return results
    
    async def _analyze(self, data: Any) -> Dict[str, Any]:
        """Implémentation par défaut de l'analyse"""
        return {"status": "analyzed", "data": str(data)}
    
    async def _generate(self, data: Any) -> Dict[str, Any]:
        """Implémentation par défaut de la génération"""
        return {"status": "generated", "output": f"Generated from: {data}"}

class AgentFactory:
    """Factory avancé avec support de plugins et monitoring"""
    
    def __init__(self, registry: AgentRegistry):
        self.registry = registry
        self._creation_metrics = {
            "total_created": 0,
            "creation_times": [],
            "failures": 0
        }
    
    async def create_agent(
        self, 
        template_name: str, 
        config: Dict[str, Any] = None,
        plugins: List[AgentPlugin] = None,
        custom_processors: Dict[str, Any] = None
    ) -> BaseAgent:
        """Crée un agent avec monitoring et personnalisation"""
        start_time = asyncio.get_event_loop().time()
        
        try:
            template = self.registry.get_template(template_name)
            
            # Merge configuration
            final_config = {**template.get("default_config", {}), **(config or {})}
            
            # Sélection de la classe d'agent
            agent_class_name = template.get("agent_class", "dynamic")
            if agent_class_name in self.registry._agent_classes:
                agent_class = self.registry._agent_classes[agent_class_name]
                agent = agent_class(template=template)
            else:
                agent = DynamicAgent(template, custom_processors)
            
            # Ajout des plugins
            if plugins:
                agent.plugins.extend(plugins)
            
            # Initialisation des plugins
            for plugin in agent.plugins:
                await plugin.on_init(agent)
            
            # Enregistrement
            self.registry._instances[agent.metadata.id] = agent
            
            # Métriques
            creation_time = asyncio.get_event_loop().time() - start_time
            self._creation_metrics["total_created"] += 1
            self._creation_metrics["creation_times"].append(creation_time)
            
            return agent
            
        except Exception as e:
            self._creation_metrics["failures"] += 1
            raise Exception(f"Failed to create agent: {str(e)}")
    
    async def create_agent_pool(
        self, 
        template_name: str, 
        pool_size: int,
        config: Dict[str, Any] = None
    ) -> List[BaseAgent]:
        """Crée un pool d'agents identiques pour la charge"""
        tasks = [
            self.create_agent(template_name, config) 
            for _ in range(pool_size)
        ]
        return await asyncio.gather(*tasks)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques de création"""
        avg_time = sum(self._creation_metrics["creation_times"]) / len(self._creation_metrics["creation_times"]) if self._creation_metrics["creation_times"] else 0
        return {
            "total_agents_created": self._creation_metrics["total_created"],
            "average_creation_time": avg_time,
            "failure_rate": self._creation_metrics["failures"] / max(self._creation_metrics["total_created"], 1)
        }

# === Intégration avec le Supervisor ===

class AdaptiveSupervisor:
    """Supervisor avec capacité de création d'agents à la demande"""
    
    def __init__(self, factory: AgentFactory):
        self.factory = factory
        self.routing_table: Dict[str, str] = {}
        self.domain_templates: Dict[str, str] = {
            "security": "security_analyst",
            "documentation": "doc_specialist",
            "testing": "test_engineer"
        }
    
    async def route_with_auto_creation(
        self, 
        query: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Route vers un agent existant ou en crée un nouveau"""
        domain = self._detect_domain(query)
        
        # Vérifier si un agent existe pour ce domaine
        if domain in self.routing_table:
            agent_id = self.routing_table[domain]
            agent = self.factory.registry._instances.get(agent_id)
            if agent:
                return await agent.process(query, context)
        
        # Créer un nouvel agent si nécessaire
        if domain in self.domain_templates:
            template_name = self.domain_templates[domain]
            agent = await self.factory.create_agent(template_name)
            self.routing_table[domain] = agent.metadata.id
            return await agent.process(query, context)
        
        raise ValueError(f"No agent available for domain: {domain}")
    
    def _detect_domain(self, query: str) -> str:
        """Détecte le domaine basé sur la requête"""
        # Implémentation simplifiée - utiliser NLP en production
        query_lower = query.lower()
        if any(word in query_lower for word in ["security", "vulnerability", "threat"]):
            return "security"
        elif any(word in query_lower for word in ["document", "analyze", "extract"]):
            return "documentation"
        elif any(word in query_lower for word in ["test", "quality", "bug"]):
            return "testing"
        return "general"

# === Monitoring et Observabilité ===

class PerformanceTracker:
    """Tracker de performance pour les agents"""
    
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "response_times": []
        }
    
    def track(self):
        """Context manager pour tracker les performances"""
        return self._PerformanceContext(self)
    
    class _PerformanceContext:
        def __init__(self, tracker):
            self.tracker = tracker
            self.start_time = None
        
        async def __aenter__(self):
            self.start_time = asyncio.get_event_loop().time()
            self.tracker.metrics["total_requests"] += 1
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            duration = asyncio.get_event_loop().time() - self.start_time
            self.tracker.metrics["response_times"].append(duration)
            
            if exc_type is None:
                self.tracker.metrics["successful_requests"] += 1
            else:
                self.tracker.metrics["failed_requests"] += 1

# === State Machine pour Agents ===

class AgentState(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING = "waiting"
    ERROR = "error"
    TERMINATED = "terminated"

class AgentStateMachine:
    """Machine à états pour gérer le cycle de vie des agents"""
    
    def __init__(self):
        self.current_state = AgentState.IDLE
        self.state_history = []
        self.transitions = {
            AgentState.IDLE: [AgentState.PROCESSING, AgentState.TERMINATED],
            AgentState.PROCESSING: [AgentState.IDLE, AgentState.WAITING, AgentState.ERROR],
            AgentState.WAITING: [AgentState.PROCESSING, AgentState.ERROR],
            AgentState.ERROR: [AgentState.IDLE, AgentState.TERMINATED],
            AgentState.TERMINATED: []
        }
    
    def transition_to(self, new_state: AgentState):
        """Effectue une transition d'état"""
        if new_state not in self.transitions.get(self.current_state, []):
            raise ValueError(f"Invalid transition from {self.current_state} to {new_state}")
        
        self.state_history.append({
            "from": self.current_state,
            "to": new_state,
            "timestamp": datetime.utcnow()
        })
        self.current_state = new_state

# === Exemple d'utilisation ===

async def example_usage():
    """Démonstration de l'utilisation du Factory Pattern"""
    
    # Initialisation
    registry = AgentRegistry()
    factory = AgentFactory(registry)
    
    # Enregistrement d'un template
    security_template = {
        "name": "security_analyst",
        "role": "specialist",
        "domain": "cybersecurity",
        "capabilities": ["analysis", "monitoring", "validation"],
        "tools": ["nmap", "wireshark"],
        "default_config": {
            "scan_depth": "comprehensive",
            "alert_threshold": 0.8
        }
    }
    registry.register_template("security_analyst", security_template)
    
    # Création d'un agent avec plugin
    class LoggingPlugin(AgentPlugin):
        async def on_init(self, agent: BaseAgent):
            print(f"Agent {agent.metadata.name} initialized")
        
        async def on_process(self, input_data: Any, context: Dict[str, Any]):
            print(f"Processing: {input_data}")
        
        async def on_complete(self, result: Dict[str, Any]):
            print(f"Completed with result: {result}")
    
    agent = await factory.create_agent(
        "security_analyst",
        config={"scan_depth": "quick"},
        plugins=[LoggingPlugin()]
    )
    
    # Utilisation
    result = await agent.process(
        "Scan network 192.168.1.0/24",
        {"priority": "high"}
    )
    
    # Métriques
    print(f"Factory metrics: {factory.get_metrics()}")
    
    # Supervisor avec création automatique
    supervisor = AdaptiveSupervisor(factory)
    result = await supervisor.route_with_auto_creation(
        "Analyze security vulnerabilities in API",
        {"auto_create": True}
    )

if __name__ == "__main__":
    asyncio.run(example_usage())