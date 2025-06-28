#!/usr/bin/env python3
"""
MessageBus A2A (Agent-to-Agent) - Phase 0 Semaine 2
Système nerveux de communication entre agents avec support hybride

Objectifs:
- Communication standardisée entre agents via enveloppes JSON
- Support multi-backend (Memory, Redis, FastAPI)
- LegacyAgentBridge pour compatibilité agents existants
- Routage intelligent avec priorité vocale
- Métriques et monitoring intégrés
"""

import asyncio
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
import logging
from abc import ABC, abstractmethod

# Imports pour backends
try:
    import redis.asyncio as redis
    import aiohttp
    from aiohttp import web
except ImportError as e:
    print(f"⚠️  Missing dependencies: {e}")
    print("Install with: pip install redis aiohttp")

class Priority(Enum):
    """Priorités de messages"""
    VOICE_REALTIME = "voice_realtime"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class MessageType(Enum):
    """Types de messages A2A"""
    TASK_START = "task_start"
    TASK_COMPLETE = "task_complete"
    TASK_ERROR = "task_error"
    PATCH_REQUEST = "patch_request"
    VOICE_CMD = "voice_cmd"
    SPEECH_RESPONSE = "speech_response"
    CONTEXT_UPDATE = "context_update"
    HEALTH_CHECK = "health_check"
    AGENT_DISCOVERY = "agent_discovery"

@dataclass
class Envelope:
    """
    Enveloppe de message A2A standardisée
    """
    task_id: str
    message_type: MessageType
    source_agent: str
    target_agent: str
    payload: Dict[str, Any]
    priority: Priority = Priority.MEDIUM
    timeout_seconds: int = 30
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[str] = None
    
    # Métadonnées spéciales
    is_voice_request: bool = False
    target_latency_ms: int = 5000
    
    def __post_init__(self):
        if not self.correlation_id:
            self.correlation_id = str(uuid.uuid4())
    
    def to_dict(self) -> Dict[str, Any]:
        """Sérialise l'enveloppe pour transport"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['message_type'] = self.message_type.value
        data['priority'] = self.priority.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Envelope':
        """Désérialise depuis un dictionnaire"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['message_type'] = MessageType(data['message_type'])
        data['priority'] = Priority(data['priority'])
        return cls(**data)

@dataclass
class PublishResult:
    """Résultat d'une publication de message"""
    success: bool
    message_id: str
    latency_ms: int
    backend_used: str
    error: Optional[str] = None

# Abstract Backend Interface
class MessageBackend(ABC):
    """Interface abstraite pour backends de messages"""
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialise le backend"""
        pass
    
    @abstractmethod
    async def publish(self, envelope: Envelope) -> PublishResult:
        """Publie un message"""
        pass
    
    @abstractmethod
    async def subscribe(self, agent_id: str, callback: Callable) -> bool:
        """S'abonne aux messages pour un agent"""
        pass
    
    @abstractmethod
    async def cleanup(self):
        """Nettoie les ressources"""
        pass

class MemoryBackend(MessageBackend):
    """Backend mémoire pour développement"""
    
    def __init__(self):
        self.queues: Dict[str, asyncio.Queue] = {}
        self.subscribers: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger("MemoryBackend")
    
    async def initialize(self) -> bool:
        """Initialise le backend mémoire"""
        self.logger.info("✅ Memory backend initialized")
        return True
    
    async def publish(self, envelope: Envelope) -> PublishResult:
        """Publie via queue mémoire"""
        start_time = time.time()
        
        try:
            # Créer queue si nécessaire
            if envelope.target_agent not in self.queues:
                self.queues[envelope.target_agent] = asyncio.Queue()
            
            # Publier dans la queue
            await self.queues[envelope.target_agent].put(envelope)
            
            # Notifier les subscribers
            if envelope.target_agent in self.subscribers:
                for callback in self.subscribers[envelope.target_agent]:
                    try:
                        await callback(envelope)
                    except Exception as e:
                        self.logger.warning(f"Subscriber error: {e}")
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return PublishResult(
                success=True,
                message_id=envelope.correlation_id,
                latency_ms=latency_ms,
                backend_used="memory"
            )
            
        except Exception as e:
            return PublishResult(
                success=False,
                message_id=envelope.correlation_id,
                latency_ms=int((time.time() - start_time) * 1000),
                backend_used="memory",
                error=str(e)
            )
    
    async def subscribe(self, agent_id: str, callback: Callable) -> bool:
        """S'abonne aux messages"""
        if agent_id not in self.subscribers:
            self.subscribers[agent_id] = []
        self.subscribers[agent_id].append(callback)
        return True
    
    async def cleanup(self):
        """Nettoie les queues"""
        self.queues.clear()
        self.subscribers.clear()

class RedisBackend(MessageBackend):
    """Backend Redis pour production"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_client = None
        self.subscribers: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger("RedisBackend")
    
    async def initialize(self) -> bool:
        """Initialise la connexion Redis"""
        try:
            self.redis_client = redis.from_url(self.redis_url)
            await self.redis_client.ping()
            self.logger.info("✅ Redis backend initialized")
            return True
        except Exception as e:
            self.logger.error(f"❌ Redis initialization failed: {e}")
            return False
    
    async def publish(self, envelope: Envelope) -> PublishResult:
        """Publie via Redis streams"""
        start_time = time.time()
        
        try:
            channel = f"agent:{envelope.target_agent}"
            message_data = envelope.to_dict()
            
            # Publier dans Redis stream
            await self.redis_client.xadd(
                channel,
                message_data,
                maxlen=1000  # Limite taille du stream
            )
            
            # Publier aussi en pub/sub pour subscribers temps réel
            await self.redis_client.publish(channel, json.dumps(message_data))
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return PublishResult(
                success=True,
                message_id=envelope.correlation_id,
                latency_ms=latency_ms,
                backend_used="redis"
            )
            
        except Exception as e:
            return PublishResult(
                success=False,
                message_id=envelope.correlation_id,
                latency_ms=int((time.time() - start_time) * 1000),
                backend_used="redis",
                error=str(e)
            )
    
    async def subscribe(self, agent_id: str, callback: Callable) -> bool:
        """S'abonne via Redis pub/sub"""
        try:
            if agent_id not in self.subscribers:
                self.subscribers[agent_id] = []
            self.subscribers[agent_id].append(callback)
            
            # Démarrer un listener Redis si premier subscriber
            if len(self.subscribers[agent_id]) == 1:
                asyncio.create_task(self._redis_listener(agent_id))
            
            return True
        except Exception as e:
            self.logger.error(f"Subscribe error: {e}")
            return False
    
    async def _redis_listener(self, agent_id: str):
        """Écoute Redis pub/sub"""
        try:
            pubsub = self.redis_client.pubsub()
            await pubsub.subscribe(f"agent:{agent_id}")
            
            async for message in pubsub.listen():
                if message['type'] == 'message':
                    try:
                        data = json.loads(message['data'])
                        envelope = Envelope.from_dict(data)
                        
                        for callback in self.subscribers.get(agent_id, []):
                            await callback(envelope)
                    except Exception as e:
                        self.logger.warning(f"Message processing error: {e}")
                        
        except Exception as e:
            self.logger.error(f"Redis listener error: {e}")
    
    async def cleanup(self):
        """Ferme la connexion Redis"""
        if self.redis_client:
            await self.redis_client.close()

class LegacyAgentBridge:
    """
    Pont de compatibilité pour agents existants
    Permet aux anciens agents de communiquer avec la nouvelle architecture
    """
    
    def __init__(self):
        self.legacy_agents: Dict[str, Any] = {}
        self.modern_agents: Dict[str, Any] = {}
        self.message_bus = None
        self.logger = logging.getLogger("LegacyAgentBridge")
        
        # Registre des agents migrés vs legacy
        self.migration_status: Dict[str, str] = {}  # agent_id -> "legacy" | "modern"
    
    def register_legacy_agent(self, agent_id: str, agent_instance: Any):
        """Enregistre un agent legacy"""
        self.legacy_agents[agent_id] = agent_instance
        self.migration_status[agent_id] = "legacy"
        self.logger.info(f"📦 Legacy agent registered: {agent_id}")
    
    def register_modern_agent(self, agent_id: str, agent_instance: Any):
        """Enregistre un agent moderne"""
        self.modern_agents[agent_id] = agent_instance
        self.migration_status[agent_id] = "modern"
        self.logger.info(f"🚀 Modern agent registered: {agent_id}")
    
    def set_message_bus(self, message_bus: 'MessageBusA2A'):
        """Configure le message bus"""
        self.message_bus = message_bus
    
    async def route_message(self, envelope: Envelope) -> PublishResult:
        """Route un message selon le type d'agent cible"""
        
        agent_status = self.migration_status.get(envelope.target_agent, "unknown")
        
        if agent_status == "legacy":
            return await self._route_to_legacy(envelope)
        elif agent_status == "modern":
            return await self._route_to_modern(envelope)
        else:
            # Agent non enregistré - essayer de le découvrir
            return await self._auto_discover_and_route(envelope)
    
    async def _route_to_legacy(self, envelope: Envelope) -> PublishResult:
        """Route vers un agent legacy"""
        start_time = time.time()
        
        try:
            agent = self.legacy_agents.get(envelope.target_agent)
            if not agent:
                raise Exception(f"Legacy agent {envelope.target_agent} not found")
            
            # Adapter l'enveloppe moderne vers l'interface legacy
            legacy_params = self._envelope_to_legacy_params(envelope)
            
            # Appeler l'agent legacy (méthode synchrone typique)
            if hasattr(agent, 'execute'):
                result = await asyncio.get_event_loop().run_in_executor(
                    None, agent.execute, legacy_params
                )
            elif hasattr(agent, 'run'):
                result = await asyncio.get_event_loop().run_in_executor(
                    None, agent.run, legacy_params
                )
            else:
                raise Exception(f"Legacy agent {envelope.target_agent} has no execute/run method")
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Envoyer la réponse si nécessaire
            if envelope.message_type in [MessageType.TASK_START, MessageType.VOICE_CMD]:
                await self._send_legacy_response(envelope, result)
            
            return PublishResult(
                success=True,
                message_id=envelope.correlation_id,
                latency_ms=latency_ms,
                backend_used="legacy_bridge"
            )
            
        except Exception as e:
            return PublishResult(
                success=False,
                message_id=envelope.correlation_id,
                latency_ms=int((time.time() - start_time) * 1000),
                backend_used="legacy_bridge",
                error=str(e)
            )
    
    async def _route_to_modern(self, envelope: Envelope) -> PublishResult:
        """Route vers un agent moderne"""
        # Utiliser le message bus standard
        if self.message_bus:
            return await self.message_bus._publish_direct(envelope)
        else:
            raise Exception("Message bus not configured")
    
    async def _auto_discover_and_route(self, envelope: Envelope) -> PublishResult:
        """Découverte automatique d'agent et routage"""
        
        # Essayer d'importer l'agent depuis le répertoire agents/
        try:
            agent_module = f"agents.{envelope.target_agent}"
            module = __import__(agent_module, fromlist=[envelope.target_agent])
            
            # Chercher une classe agent
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    attr_name.lower().startswith('agent') and
                    hasattr(attr, 'execute')):
                    
                    # Instancier et enregistrer comme legacy
                    agent_instance = attr()
                    self.register_legacy_agent(envelope.target_agent, agent_instance)
                    
                    return await self._route_to_legacy(envelope)
            
            raise Exception(f"No agent class found in {agent_module}")
            
        except Exception as e:
            return PublishResult(
                success=False,
                message_id=envelope.correlation_id,
                latency_ms=0,
                backend_used="auto_discovery",
                error=f"Agent discovery failed: {e}"
            )
    
    def _envelope_to_legacy_params(self, envelope: Envelope) -> Dict[str, Any]:
        """Convertit une enveloppe moderne vers paramètres legacy"""
        
        legacy_params = {
            "task_id": envelope.task_id,
            "action": envelope.message_type.value,
            "data": envelope.payload,
            "source": envelope.source_agent,
            "priority": envelope.priority.value
        }
        
        # Ajouts spéciaux pour commandes vocales
        if envelope.is_voice_request:
            legacy_params["voice_mode"] = True
            legacy_params["max_latency"] = envelope.target_latency_ms
        
        return legacy_params
    
    async def _send_legacy_response(self, original_envelope: Envelope, result: Any):
        """Envoie une réponse depuis un agent legacy"""
        
        if not self.message_bus:
            return
        
        response_envelope = Envelope(
            task_id=original_envelope.task_id,
            message_type=MessageType.TASK_COMPLETE,
            source_agent=original_envelope.target_agent,
            target_agent=original_envelope.source_agent,
            payload={"result": result, "legacy_response": True},
            correlation_id=original_envelope.correlation_id
        )
        
        await self.message_bus.publish(response_envelope)

class VoiceOptimizedMessageBus:
    """
    Optimisations spécifiques pour commandes vocales
    """
    
    def __init__(self, parent_bus: 'MessageBusA2A'):
        self.parent_bus = parent_bus
        self.voice_queue = asyncio.Queue()
        self.logger = logging.getLogger("VoiceOptimizedBus")
    
    async def publish_voice_command(self, envelope: Envelope) -> PublishResult:
        """Publication optimisée pour commandes vocales < 1.5s"""
        
        # Marquer comme requête vocale prioritaire
        envelope.is_voice_request = True
        envelope.priority = Priority.VOICE_REALTIME
        
        # Pour latence critique, bypass Redis et utiliser mémoire directe
        if envelope.target_latency_ms < 1500:
            return await self._direct_voice_route(envelope)
        else:
            return await self.parent_bus.publish(envelope)
    
    async def _direct_voice_route(self, envelope: Envelope) -> PublishResult:
        """Routage direct pour latence minimale"""
        
        # Utiliser backend mémoire directement
        memory_backend = MemoryBackend()
        await memory_backend.initialize()
        
        result = await memory_backend.publish(envelope)
        result.backend_used = "voice_direct"
        
        return result

@dataclass
class MessageBusConfig:
    """Configuration du MessageBus"""
    default_backend: str = "memory"  # "memory", "redis", "hybrid"
    redis_url: str = "redis://localhost:6379"
    enable_legacy_bridge: bool = True
    enable_voice_optimization: bool = True
    message_retention_hours: int = 24
    max_retry_attempts: int = 3

class MessageBusA2A:
    """
    Bus de messages Agent-to-Agent avec support multi-backend
    """
    
    def __init__(self, config: MessageBusConfig):
        self.config = config
        self.backends: Dict[str, MessageBackend] = {}
        self.current_backend = None
        self.legacy_bridge = LegacyAgentBridge() if config.enable_legacy_bridge else None
        self.voice_bus = None
        
        # Métriques
        self.metrics = {
            "messages_sent": 0,
            "messages_failed": 0,
            "avg_latency_ms": 0.0,
            "backend_usage": {},
            "voice_messages": 0
        }
        
        self.logger = logging.getLogger("MessageBusA2A")
    
    async def initialize(self):
        """Initialise le message bus"""
        
        # Initialiser les backends
        self.backends["memory"] = MemoryBackend()
        self.backends["redis"] = RedisBackend(self.config.redis_url)
        
        # Initialiser le backend par défaut
        backend = self.backends[self.config.default_backend]
        success = await backend.initialize()
        
        if success:
            self.current_backend = backend
            self.logger.info(f"✅ MessageBus initialized with {self.config.default_backend} backend")
        else:
            # Fallback vers mémoire
            self.current_backend = self.backends["memory"]
            await self.current_backend.initialize()
            self.logger.warning("⚠️  Fallback to memory backend")
        
        # Configurer le bridge legacy
        if self.legacy_bridge:
            self.legacy_bridge.set_message_bus(self)
        
        # Configurer l'optimisation vocale
        if self.config.enable_voice_optimization:
            self.voice_bus = VoiceOptimizedMessageBus(self)
    
    async def publish(self, envelope: Envelope) -> PublishResult:
        """Publication de message avec routage intelligent"""
        
        try:
            # Validation de l'enveloppe
            if not self._validate_envelope(envelope):
                raise ValueError("Invalid envelope")
            
            # Routage vocal prioritaire
            if envelope.is_voice_request and self.voice_bus:
                result = await self.voice_bus.publish_voice_command(envelope)
            # Routage legacy vs moderne
            elif self.legacy_bridge:
                result = await self.legacy_bridge.route_message(envelope)
            # Publication normale
            else:
                result = await self._publish_direct(envelope)
            
            # Mise à jour métriques
            self._update_metrics(result)
            
            # Logging
            self.logger.info(
                f"📨 Message sent: {envelope.source_agent} → {envelope.target_agent} "
                f"({result.latency_ms}ms, {result.backend_used})"
            )
            
            return result
            
        except Exception as e:
            self.metrics["messages_failed"] += 1
            self.logger.error(f"❌ Message publish failed: {e}")
            
            return PublishResult(
                success=False,
                message_id=envelope.correlation_id,
                latency_ms=0,
                backend_used="error",
                error=str(e)
            )
    
    async def _publish_direct(self, envelope: Envelope) -> PublishResult:
        """Publication directe via backend"""
        return await self.current_backend.publish(envelope)
    
    async def subscribe(self, agent_id: str, callback: Callable) -> bool:
        """S'abonne aux messages pour un agent"""
        
        success = await self.current_backend.subscribe(agent_id, callback)
        
        if success:
            self.logger.info(f"📡 Subscription registered: {agent_id}")
        
        return success
    
    def _validate_envelope(self, envelope: Envelope) -> bool:
        """Valide une enveloppe de message"""
        
        required_fields = [
            envelope.task_id, envelope.source_agent, 
            envelope.target_agent, envelope.payload
        ]
        
        return all(field is not None for field in required_fields)
    
    def _update_metrics(self, result: PublishResult):
        """Met à jour les métriques"""
        
        if result.success:
            self.metrics["messages_sent"] += 1
            
            # Latence moyenne
            total_messages = self.metrics["messages_sent"]
            current_avg = self.metrics["avg_latency_ms"]
            self.metrics["avg_latency_ms"] = (
                (current_avg * (total_messages - 1) + result.latency_ms) / total_messages
            )
            
            # Usage backend
            backend = result.backend_used
            self.metrics["backend_usage"][backend] = self.metrics["backend_usage"].get(backend, 0) + 1
        else:
            self.metrics["messages_failed"] += 1
    
    def get_metrics(self) -> Dict:
        """Retourne les métriques actuelles"""
        
        total_messages = self.metrics["messages_sent"] + self.metrics["messages_failed"]
        success_rate = self.metrics["messages_sent"] / max(total_messages, 1)
        
        return {
            **self.metrics,
            "total_messages": total_messages,
            "success_rate": success_rate,
            "legacy_agents_count": len(self.legacy_bridge.legacy_agents) if self.legacy_bridge else 0,
            "modern_agents_count": len(self.legacy_bridge.modern_agents) if self.legacy_bridge else 0
        }
    
    async def health_check(self) -> Dict:
        """Vérification de santé du message bus"""
        
        health = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "backend": self.config.default_backend,
            "components": {}
        }
        
        # Test backend principal
        try:
            test_envelope = Envelope(
                task_id="health_check",
                message_type=MessageType.HEALTH_CHECK,
                source_agent="system",
                target_agent="system",
                payload={"test": True}
            )
            
            result = await self._publish_direct(test_envelope)
            health["components"]["backend"] = "healthy" if result.success else "unhealthy"
            
        except Exception as e:
            health["components"]["backend"] = "unhealthy"
            health["status"] = "degraded"
        
        # Test legacy bridge
        if self.legacy_bridge:
            health["components"]["legacy_bridge"] = "healthy"
        
        return health
    
    async def cleanup(self):
        """Nettoie les ressources"""
        for backend in self.backends.values():
            await backend.cleanup()

# Factory functions pour création simplifiée

async def create_message_bus(config: MessageBusConfig = None) -> MessageBusA2A:
    """Crée et initialise un MessageBus"""
    
    if config is None:
        config = MessageBusConfig()
    
    bus = MessageBusA2A(config)
    await bus.initialize()
    return bus

def create_envelope(
    task_id: str,
    message_type: MessageType,
    source_agent: str,
    target_agent: str,
    payload: Dict[str, Any],
    priority: Priority = Priority.MEDIUM,
    is_voice: bool = False
) -> Envelope:
    """Crée une enveloppe de message"""
    
    return Envelope(
        task_id=task_id,
        message_type=message_type,
        source_agent=source_agent,
        target_agent=target_agent,
        payload=payload,
        priority=priority,
        is_voice_request=is_voice
    )

# Démonstration et tests

async def demo_message_bus():
    """Démonstration du MessageBus A2A"""
    
    print("🚀 MessageBus A2A Demo - Phase 0 Week 2")
    print("=" * 60)
    
    # Configuration
    config = MessageBusConfig(
        default_backend="memory",
        enable_legacy_bridge=True,
        enable_voice_optimization=True
    )
    
    try:
        # Création du message bus
        bus = await create_message_bus(config)
        
        # Test 1: Message simple
        print("\n🧪 Test 1: Message standard")
        envelope = create_envelope(
            task_id="test_001",
            message_type=MessageType.TASK_START,
            source_agent="agent_test_source",
            target_agent="agent_test_target",
            payload={"action": "analyze_code", "file": "test.py"}
        )
        
        result = await bus.publish(envelope)
        print(f"Result: {result.success}, Latency: {result.latency_ms}ms, Backend: {result.backend_used}")
        
        # Test 2: Message vocal prioritaire
        print("\n🧪 Test 2: Commande vocale")
        voice_envelope = create_envelope(
            task_id="voice_001",
            message_type=MessageType.VOICE_CMD,
            source_agent="voice_interface",
            target_agent="agent_111_auditeur_qualite",
            payload={"command": "status_report", "voice_session_id": "session_123"},
            priority=Priority.VOICE_REALTIME,
            is_voice=True
        )
        voice_envelope.target_latency_ms = 1200
        
        result = await bus.publish(voice_envelope)
        print(f"Voice result: {result.success}, Latency: {result.latency_ms}ms")
        
        # Test 3: Enregistrement d'agent legacy
        print("\n🧪 Test 3: Legacy Agent Bridge")
        
        class MockLegacyAgent:
            def execute(self, params):
                return f"Legacy execution: {params['action']}"
        
        mock_agent = MockLegacyAgent()
        bus.legacy_bridge.register_legacy_agent("agent_legacy_test", mock_agent)
        
        legacy_envelope = create_envelope(
            task_id="legacy_001",
            message_type=MessageType.TASK_START,
            source_agent="modern_agent",
            target_agent="agent_legacy_test",
            payload={"action": "legacy_task", "data": "test_data"}
        )
        
        result = await bus.publish(legacy_envelope)
        print(f"Legacy result: {result.success}, Backend: {result.backend_used}")
        
        # Test 4: Métriques
        print("\n📊 Métriques MessageBus")
        metrics = bus.get_metrics()
        print(f"Messages sent: {metrics['messages_sent']}")
        print(f"Success rate: {metrics['success_rate']:.2%}")
        print(f"Average latency: {metrics['avg_latency_ms']:.1f}ms")
        print(f"Backend usage: {metrics['backend_usage']}")
        print(f"Legacy agents: {metrics['legacy_agents_count']}")
        
        # Test 5: Health check
        print("\n🏥 Health Check")
        health = await bus.health_check()
        print(f"Status: {health['status']}")
        print(f"Components: {health['components']}")
        
        await bus.cleanup()
        print("\n✅ Demo completed successfully")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(demo_message_bus())