#!/usr/bin/env python3
"""
🔗 Agent Webhook Handler - NextGeneration v5.3.0
Version enterprise Wave 4 avec gestion événements intelligente

Migration Pattern: EVENT_DRIVEN + ENTERPRISE_READY + LLM_ENHANCED
Author: Claude Sonnet 4
Date: 30 Juin 2025
"""

import asyncio
import json
import time
import hashlib
import hmac
import aiohttp
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import uuid
import sqlite3
import re
from urllib.parse import urlparse
import ssl

# Imports NextGeneration Architecture
try:
    from core.services import (
        LLMGatewayHybrid, create_llm_gateway,
        MessageBusA2A, create_envelope, MessageType, Priority,
        OptimizedContextStore, create_agent_context, ContextType
    )
    from core.agent_factory_architecture import Task, Result
except ImportError:
    # Fallback pour développement isolé
    print("⚠️ NextGeneration services not available - running in development mode")
    class Task:
        def __init__(self, task_type, params=None):
            self.type = task_type
            self.params = params or {}
    
    class Result:
        def __init__(self, success, data=None, error=None, metrics=None):
            self.success = success
            self.data = data
            self.error = error
            self.metrics = metrics or {}

class WebhookType(str, Enum):
    """Types de webhooks"""
    INCOMING = "INCOMING"
    OUTGOING = "OUTGOING"
    BIDIRECTIONAL = "BIDIRECTIONAL"

class EventType(str, Enum):
    """Types d'événements"""
    SYSTEM = "SYSTEM"
    APPLICATION = "APPLICATION"
    BUSINESS = "BUSINESS"
    SECURITY = "SECURITY"
    DEPLOYMENT = "DEPLOYMENT"
    MONITORING = "MONITORING"
    CUSTOM = "CUSTOM"

class WebhookStatus(str, Enum):
    """Statuts webhook"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    FAILED = "FAILED"
    SUSPENDED = "SUSPENDED"

class DeliveryStatus(str, Enum):
    """Statuts de livraison"""
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"
    RETRYING = "RETRYING"
    ABANDONED = "ABANDONED"

@dataclass
class WebhookEndpoint:
    """Point de terminaison webhook"""
    endpoint_id: str
    name: str
    url: str
    webhook_type: WebhookType
    event_types: List[EventType]
    secret: Optional[str] = None
    headers: Dict[str, str] = None
    timeout_seconds: int = 30
    retry_count: int = 3
    retry_delay_seconds: int = 5
    status: WebhookStatus = WebhookStatus.ACTIVE
    metadata: Dict[str, Any] = None
    created_at: datetime = None

@dataclass
class WebhookEvent:
    """Événement webhook"""
    event_id: str
    event_type: EventType
    source: str
    payload: Dict[str, Any]
    timestamp: datetime
    headers: Dict[str, str] = None
    metadata: Dict[str, Any] = None

@dataclass
class WebhookDelivery:
    """Livraison webhook"""
    delivery_id: str
    endpoint_id: str
    event_id: str
    status: DeliveryStatus
    attempt_count: int
    last_attempt: Optional[datetime] = None
    next_retry: Optional[datetime] = None
    response_code: Optional[int] = None
    response_body: Optional[str] = None
    error_message: Optional[str] = None
    delivery_time_ms: Optional[float] = None

class IntelligentEventProcessor:
    """Processeur d'événements intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.event_patterns = {}
        self.correlation_rules = {}
        self.processing_rules = {}
    
    async def process_event(self, event: WebhookEvent) -> Dict[str, Any]:
        """Traitement intelligent d'événement"""
        processing_result = {
            "event_id": event.event_id,
            "processed": True,
            "enriched_data": {},
            "correlations": [],
            "actions": [],
            "routing": []
        }
        
        # Enrichissement de base
        enriched_data = await self._enrich_event_data(event)
        processing_result["enriched_data"] = enriched_data
        
        # Détection corrélations
        correlations = await self._detect_correlations(event)
        processing_result["correlations"] = correlations
        
        # Enhancement IA si disponible
        if self.llm_gateway:
            try:
                ai_processing = await self.llm_gateway.process_request(
                    "Analyze webhook event for intelligent processing",
                    context={
                        "role": "event_processing_expert",
                        "event": asdict(event),
                        "enriched_data": enriched_data,
                        "correlations": correlations,
                        "task": "intelligent_event_processing"
                    }
                )
                
                if ai_processing.get("success"):
                    ai_result = ai_processing.get("processing_result", {})
                    processing_result.update(ai_result)
                    
            except Exception as e:
                self.logger = logging.getLogger(f"EventProcessor_{id(self)}")
                self.logger.warning(f"⚠️ Erreur traitement IA: {e}")
        
        return processing_result
    
    async def _enrich_event_data(self, event: WebhookEvent) -> Dict[str, Any]:
        """Enrichissement données événement"""
        enriched = {
            "timestamp_parsed": event.timestamp.isoformat(),
            "event_age_seconds": (datetime.now() - event.timestamp).total_seconds(),
            "payload_size_bytes": len(json.dumps(event.payload)),
            "source_domain": self._extract_domain(event.source),
            "event_hash": hashlib.sha256(json.dumps(event.payload, sort_keys=True).encode()).hexdigest()
        }
        
        # Analyse payload
        if isinstance(event.payload, dict):
            enriched["payload_keys"] = list(event.payload.keys())
            enriched["payload_depth"] = self._calculate_dict_depth(event.payload)
            
            # Extraction données importantes
            if "user_id" in event.payload:
                enriched["user_involved"] = True
            if "error" in event.payload or "exception" in event.payload:
                enriched["error_event"] = True
            if "amount" in event.payload or "price" in event.payload:
                enriched["financial_event"] = True
        
        return enriched
    
    def _extract_domain(self, source: str) -> Optional[str]:
        """Extraction domaine depuis source"""
        try:
            if source.startswith(('http://', 'https://')):
                parsed = urlparse(source)
                return parsed.netloc
            elif '@' in source:
                return source.split('@')[-1]
            else:
                return source
        except:
            return None
    
    def _calculate_dict_depth(self, d: Dict, depth: int = 0) -> int:
        """Calcul profondeur dictionnaire"""
        if not isinstance(d, dict):
            return depth
        
        max_depth = depth
        for value in d.values():
            if isinstance(value, dict):
                max_depth = max(max_depth, self._calculate_dict_depth(value, depth + 1))
        
        return max_depth
    
    async def _detect_correlations(self, event: WebhookEvent) -> List[Dict[str, Any]]:
        """Détection corrélations événements"""
        correlations = []
        
        # Corrélation par source
        if event.source in self.event_patterns:
            recent_events = self.event_patterns[event.source]
            if len(recent_events) > 1:
                correlations.append({
                    "type": "source_frequency",
                    "description": f"Multiple events from {event.source}",
                    "count": len(recent_events),
                    "timespan_minutes": 30
                })
        
        # Corrélation par type d'événement
        event_type_key = f"type_{event.event_type.value}"
        if event_type_key in self.event_patterns:
            type_events = self.event_patterns[event_type_key]
            if len(type_events) > 5:  # Seuil fréquence
                correlations.append({
                    "type": "event_type_spike",
                    "description": f"High frequency of {event.event_type.value} events",
                    "count": len(type_events),
                    "severity": "medium"
                })
        
        return correlations
    
    async def suggest_routing(self, event: WebhookEvent, 
                            processing_result: Dict[str, Any]) -> List[str]:
        """Suggestion routing intelligent"""
        routing_suggestions = []
        
        # Routing basé sur type d'événement
        if event.event_type == EventType.SECURITY:
            routing_suggestions.append("security_team")
        elif event.event_type == EventType.DEPLOYMENT:
            routing_suggestions.append("devops_team")
        elif event.event_type == EventType.MONITORING:
            routing_suggestions.append("ops_team")
        
        # Routing basé sur enrichissement
        enriched = processing_result.get("enriched_data", {})
        if enriched.get("error_event"):
            routing_suggestions.append("error_handling_service")
        if enriched.get("financial_event"):
            routing_suggestions.append("finance_validation_service")
        
        # Enhancement IA pour routing avancé
        if self.llm_gateway:
            try:
                ai_routing = await self.llm_gateway.process_request(
                    "Suggest intelligent routing for webhook event",
                    context={
                        "role": "event_routing_expert",
                        "event": asdict(event),
                        "processing_result": processing_result,
                        "basic_routing": routing_suggestions,
                        "task": "intelligent_event_routing"
                    }
                )
                
                if ai_routing.get("success"):
                    ai_suggestions = ai_routing.get("routing_suggestions", [])
                    routing_suggestions.extend(ai_suggestions)
                    
            except Exception:
                pass
        
        return list(set(routing_suggestions))  # Déduplication

class WebhookDeliveryEngine:
    """Moteur de livraison webhook"""
    
    def __init__(self, webhook_handler):
        self.handler = webhook_handler
        self.delivery_queue = asyncio.Queue()
        self.active_deliveries = {}
        self.delivery_workers = []
    
    async def deliver_webhook(self, endpoint: WebhookEndpoint, 
                            event: WebhookEvent) -> WebhookDelivery:
        """Livraison webhook avec retry intelligent"""
        delivery = WebhookDelivery(
            delivery_id=str(uuid.uuid4()),
            endpoint_id=endpoint.endpoint_id,
            event_id=event.event_id,
            status=DeliveryStatus.PENDING,
            attempt_count=0
        )
        
        max_attempts = endpoint.retry_count + 1
        
        for attempt in range(max_attempts):
            delivery.attempt_count = attempt + 1
            delivery.last_attempt = datetime.now()
            
            try:
                success = await self._attempt_delivery(endpoint, event, delivery)
                
                if success:
                    delivery.status = DeliveryStatus.SUCCESS
                    break
                else:
                    if attempt < max_attempts - 1:
                        delivery.status = DeliveryStatus.RETRYING
                        # Backoff exponentiel
                        delay = endpoint.retry_delay_seconds * (2 ** attempt)
                        delivery.next_retry = datetime.now() + timedelta(seconds=delay)
                        await asyncio.sleep(delay)
                    else:
                        delivery.status = DeliveryStatus.ABANDONED
                        
            except Exception as e:
                delivery.error_message = str(e)
                self.handler.logger.error(f"❌ Delivery error: {e}")
                
                if attempt == max_attempts - 1:
                    delivery.status = DeliveryStatus.FAILED
        
        return delivery
    
    async def _attempt_delivery(self, endpoint: WebhookEndpoint, 
                              event: WebhookEvent, delivery: WebhookDelivery) -> bool:
        """Tentative de livraison"""
        start_time = time.time()
        
        try:
            # Préparation payload
            payload = {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "timestamp": event.timestamp.isoformat(),
                "source": event.source,
                "data": event.payload
            }
            
            # Préparation headers
            headers = {
                "Content-Type": "application/json",
                "User-Agent": f"NextGeneration-Webhook-Handler/{self.handler.version}",
                "X-Event-ID": event.event_id,
                "X-Event-Type": event.event_type.value,
                "X-Delivery-ID": delivery.delivery_id
            }
            
            # Ajout headers personnalisés
            if endpoint.headers:
                headers.update(endpoint.headers)
            
            # Signature HMAC si secret configuré
            if endpoint.secret:
                payload_json = json.dumps(payload, separators=(',', ':'))
                signature = hmac.new(
                    endpoint.secret.encode(),
                    payload_json.encode(),
                    hashlib.sha256
                ).hexdigest()
                headers["X-Webhook-Signature"] = f"sha256={signature}"
            
            # Livraison HTTP
            timeout = aiohttp.ClientTimeout(total=endpoint.timeout_seconds)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    endpoint.url,
                    json=payload,
                    headers=headers,
                    ssl=ssl.create_default_context()
                ) as response:
                    delivery.response_code = response.status
                    delivery.response_body = await response.text()
                    delivery.delivery_time_ms = (time.time() - start_time) * 1000
                    
                    # Succès si code 2xx
                    return 200 <= response.status < 300
                    
        except asyncio.TimeoutError:
            delivery.error_message = "Request timeout"
            return False
        except Exception as e:
            delivery.error_message = str(e)
            return False
    
    async def start_delivery_workers(self, worker_count: int = 3):
        """Démarrage workers de livraison"""
        for i in range(worker_count):
            worker = asyncio.create_task(self._delivery_worker(f"worker_{i}"))
            self.delivery_workers.append(worker)
    
    async def _delivery_worker(self, worker_name: str):
        """Worker de livraison webhook"""
        while True:
            try:
                # Récupération tâche de livraison
                delivery_task = await self.delivery_queue.get()
                endpoint = delivery_task["endpoint"]
                event = delivery_task["event"]
                
                # Livraison
                delivery = await self.deliver_webhook(endpoint, event)
                
                # Stockage résultat
                await self.handler._store_delivery_result(delivery)
                
                # Notification du résultat
                if delivery.status == DeliveryStatus.SUCCESS:
                    self.handler.logger.info(f"✅ Webhook delivered: {delivery.delivery_id}")
                else:
                    self.handler.logger.warning(f"⚠️ Webhook delivery failed: {delivery.delivery_id}")
                
                self.delivery_queue.task_done()
                
            except Exception as e:
                self.handler.logger.error(f"❌ Delivery worker error: {e}")

class AgentWebhookHandler_Enterprise:
    """
    🔗 Agent Webhook Handler - Enterprise NextGeneration v5.3.0
    
    Gestionnaire webhooks intelligent avec traitement événements et livraison fiable.
    
    Patterns NextGeneration v5.3.0:
    - EVENT_DRIVEN: Architecture événementielle avancée
    - ENTERPRISE_READY: Fiabilité et scalabilité enterprise
    - LLM_ENHANCED: Traitement intelligent événements IA
    - PATTERN_FACTORY: Architecture modulaire éprouvée
    """
    
    def __init__(self, agent_id: str = "webhook_handler", 
                 data_dir: Path = None):
        # Métadonnées NextGeneration v5.3.0
        self.agent_id = agent_id
        self.version = "5.3.0"
        self.wave_version = "Wave 4 - Extensions Core"
        self.migration_status = "modern_active"
        self.compatibility_mode = True
        
        # Patterns NextGeneration appliqués
        self.__version__ = "5.3.0"
        self.__wave_version__ = "Wave 4 - Extensions Core"
        self.__nextgen_patterns__ = [
            "EVENT_DRIVEN",
            "ENTERPRISE_READY", 
            "LLM_ENHANCED",
            "PATTERN_FACTORY"
        ]
        
        # Configuration agent
        self.name = "Webhook Handler Enterprise"
        self.mission = "Gestion webhooks intelligente avec traitement événements IA"
        self.agent_type = "webhook_enterprise"
        
        # Configuration webhooks
        self.data_dir = data_dir or Path("/var/lib/nextgeneration/webhooks")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Services NextGeneration (injectés à l'initialisation)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Composants webhook intelligents
        self.event_processor = IntelligentEventProcessor()
        self.delivery_engine = WebhookDeliveryEngine(self)
        
        # Configuration webhook
        self.webhook_config = {
            "max_payload_size_mb": 10,
            "default_timeout_seconds": 30,
            "max_retry_attempts": 3,
            "delivery_workers": 3,
            "event_retention_days": 30,
            "ai_processing_enabled": True
        }
        
        # État webhooks
        self.endpoints: Dict[str, WebhookEndpoint] = {}
        self.recent_events: List[WebhookEvent] = []
        self.delivery_history: List[WebhookDelivery] = []
        
        # Base de données événements
        self.db_path = self.data_dir / "webhooks.db"
        self._init_database()
        
        # Métriques webhook
        self.webhook_metrics = {
            "events_received": 0,
            "events_processed": 0,
            "deliveries_attempted": 0,
            "deliveries_successful": 0,
            "deliveries_failed": 0,
            "average_delivery_time_ms": 0.0,
            "ai_processing_count": 0
        }
        
        # Background tasks
        self._event_cleanup_task = None
        
        # Setup logging
        self._setup_logging()
        
        # Démarrage composants
        asyncio.create_task(self._start_background_tasks())
    
    def _init_database(self):
        """Initialisation base de données webhooks"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS webhook_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT UNIQUE NOT NULL,
                    event_type TEXT NOT NULL,
                    source TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    processed BOOLEAN DEFAULT FALSE,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS webhook_deliveries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    delivery_id TEXT UNIQUE NOT NULL,
                    endpoint_id TEXT NOT NULL,
                    event_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    attempt_count INTEGER DEFAULT 0,
                    response_code INTEGER,
                    delivery_time_ms REAL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_event_timestamp 
                ON webhook_events(timestamp)
            """)
    
    def _setup_logging(self):
        """Configuration logging NextGeneration"""
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="webhook",
                custom_config={
                    "logger_name": f"nextgen.webhook.handler.{self.agent_id}",
                    "log_dir": "logs/webhook",
                    "metadata": {
                        "agent_type": "webhook_handler",
                        "agent_role": "event_processing",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(f"WebhookHandler_{self.agent_id}")
    
    async def inject_nextgen_services(self, 
                                    llm_gateway: LLMGatewayHybrid,
                                    message_bus: MessageBusA2A, 
                                    context_store: OptimizedContextStore):
        """Injection des services NextGeneration v5.3.0"""
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus  
        self.context_store = context_store
        
        # Configuration composants avec IA
        self.event_processor.llm_gateway = llm_gateway
        
        # Configuration contexte webhook IA
        await self._setup_webhook_context()
        
        self.logger.info("✅ Services NextGeneration injectés - Webhook IA actif")
    
    async def _setup_webhook_context(self):
        """Configuration contexte webhook IA spécialisé"""
        if not self.llm_gateway:
            return
        
        webhook_context = {
            "role": "webhook_event_processing_expert",
            "domain": "enterprise_event_driven_architecture",
            "capabilities": [
                "Intelligent event processing",
                "Event correlation analysis",
                "Smart routing decisions",
                "Webhook delivery optimization",
                "Event pattern recognition"
            ],
            "patterns": [
                "EVENT_DRIVEN",
                "ENTERPRISE_READY",
                "LLM_ENHANCED"
            ]
        }
        
        # Chargement expertise webhook depuis LLM
        try:
            response = await self.llm_gateway.process_request(
                "Load webhook event processing expertise",
                context=webhook_context
            )
            
            if response.get("success"):
                self.logger.info("🧠 Expertise webhook IA chargée")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement contexte IA: {e}")
    
    async def register_endpoint(self, endpoint: WebhookEndpoint) -> bool:
        """Enregistrement endpoint webhook"""
        try:
            endpoint.created_at = datetime.now()
            self.endpoints[endpoint.endpoint_id] = endpoint
            self.logger.info(f"🔗 Endpoint enregistré: {endpoint.name} ({endpoint.url})")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur enregistrement endpoint: {e}")
            return False
    
    async def receive_webhook(self, event: WebhookEvent) -> Dict[str, Any]:
        """Réception et traitement webhook"""
        try:
            self.logger.info(f"📥 Webhook reçu: {event.event_type.value} from {event.source}")
            
            # Stockage événement
            await self._store_event(event)
            self.recent_events.append(event)
            
            # Limitation mémoire
            if len(self.recent_events) > 1000:
                self.recent_events = self.recent_events[-500:]
            
            # Traitement intelligent
            processing_result = await self.event_processor.process_event(event)
            
            if self.webhook_config["ai_processing_enabled"]:
                self.webhook_metrics["ai_processing_count"] += 1
            
            # Suggestion routing
            routing = await self.event_processor.suggest_routing(event, processing_result)
            processing_result["routing"] = routing
            
            # Distribution vers endpoints
            delivery_results = await self._distribute_event(event)
            processing_result["delivery_results"] = delivery_results
            
            # Notification via MessageBus
            if self.message_bus:
                await self.message_bus.publish(
                    create_envelope(
                        message_type=MessageType.EVENT,
                        payload={
                            "type": "webhook_event_processed",
                            "event": asdict(event),
                            "processing_result": processing_result,
                            "timestamp": datetime.now().isoformat()
                        },
                        priority=Priority.MEDIUM
                    )
                )
            
            self.webhook_metrics["events_received"] += 1
            self.webhook_metrics["events_processed"] += 1
            
            return processing_result
            
        except Exception as e:
            self.logger.error(f"❌ Erreur traitement webhook: {e}")
            return {"success": False, "error": str(e)}
    
    async def _store_event(self, event: WebhookEvent):
        """Stockage événement en base"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO webhook_events 
                   (event_id, event_type, source, payload, timestamp) 
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    event.event_id,
                    event.event_type.value,
                    event.source,
                    json.dumps(event.payload),
                    event.timestamp.isoformat()
                )
            )
    
    async def _distribute_event(self, event: WebhookEvent) -> List[Dict[str, Any]]:
        """Distribution événement vers endpoints"""
        delivery_results = []
        
        # Recherche endpoints concernés
        matching_endpoints = [
            endpoint for endpoint in self.endpoints.values()
            if (event.event_type in endpoint.event_types and 
                endpoint.status == WebhookStatus.ACTIVE and
                endpoint.webhook_type in [WebhookType.OUTGOING, WebhookType.BIDIRECTIONAL])
        ]
        
        # Livraison asynchrone
        for endpoint in matching_endpoints:
            try:
                delivery_task = {
                    "endpoint": endpoint,
                    "event": event
                }
                await self.delivery_engine.delivery_queue.put(delivery_task)
                
                delivery_results.append({
                    "endpoint_id": endpoint.endpoint_id,
                    "status": "queued",
                    "url": endpoint.url
                })
                
                self.webhook_metrics["deliveries_attempted"] += 1
                
            except Exception as e:
                delivery_results.append({
                    "endpoint_id": endpoint.endpoint_id,
                    "status": "error",
                    "error": str(e)
                })
        
        return delivery_results
    
    async def _store_delivery_result(self, delivery: WebhookDelivery):
        """Stockage résultat livraison"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO webhook_deliveries 
                   (delivery_id, endpoint_id, event_id, status, attempt_count, 
                    response_code, delivery_time_ms) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    delivery.delivery_id,
                    delivery.endpoint_id,
                    delivery.event_id,
                    delivery.status.value,
                    delivery.attempt_count,
                    delivery.response_code,
                    delivery.delivery_time_ms
                )
            )
        
        # Mise à jour métriques
        if delivery.status == DeliveryStatus.SUCCESS:
            self.webhook_metrics["deliveries_successful"] += 1
            if delivery.delivery_time_ms:
                self._update_average_delivery_time(delivery.delivery_time_ms)
        else:
            self.webhook_metrics["deliveries_failed"] += 1
    
    def _update_average_delivery_time(self, delivery_time_ms: float):
        """Mise à jour temps livraison moyen"""
        count = self.webhook_metrics["deliveries_successful"]
        avg = self.webhook_metrics["average_delivery_time_ms"]
        
        self.webhook_metrics["average_delivery_time_ms"] = (
            (avg * (count - 1) + delivery_time_ms) / count
        )
    
    async def _start_background_tasks(self):
        """Démarrage tâches background"""
        self._event_cleanup_task = asyncio.create_task(self._event_cleanup_loop())
        await self.delivery_engine.start_delivery_workers(
            self.webhook_config["delivery_workers"]
        )
    
    async def _event_cleanup_loop(self):
        """Nettoyage événements anciens"""
        while True:
            try:
                await asyncio.sleep(3600)  # Nettoyage horaire
                
                retention_days = self.webhook_config["event_retention_days"]
                cutoff_date = datetime.now() - timedelta(days=retention_days)
                
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute(
                        "DELETE FROM webhook_events WHERE timestamp < ?",
                        (cutoff_date.isoformat(),)
                    )
                    deleted_count = cursor.rowcount
                    
                    if deleted_count > 0:
                        self.logger.info(f"🧹 Nettoyage: {deleted_count} événements supprimés")
                        
            except Exception as e:
                self.logger.error(f"❌ Erreur nettoyage: {e}")
    
    async def get_webhook_stats(self) -> Dict[str, Any]:
        """Statistiques webhook détaillées"""
        # Calcul success rate
        total_deliveries = (self.webhook_metrics["deliveries_successful"] + 
                          self.webhook_metrics["deliveries_failed"])
        success_rate = 0.0
        if total_deliveries > 0:
            success_rate = (self.webhook_metrics["deliveries_successful"] / total_deliveries) * 100
        
        return {
            "webhook_metrics": self.webhook_metrics,
            "success_rate": success_rate,
            "endpoints_count": len(self.endpoints),
            "active_endpoints": len([e for e in self.endpoints.values() 
                                   if e.status == WebhookStatus.ACTIVE]),
            "recent_events_count": len(self.recent_events),
            "patterns": self.__nextgen_patterns__,
            "version": self.version,
            "timestamp": datetime.now().isoformat()
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check NextGeneration"""
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "status": "healthy",
            "patterns": self.__nextgen_patterns__,
            "services": {
                "llm_gateway": self.llm_gateway is not None,
                "message_bus": self.message_bus is not None,
                "context_store": self.context_store is not None
            },
            "webhook": {
                "endpoints_registered": len(self.endpoints),
                "events_processed": self.webhook_metrics["events_processed"],
                "delivery_success_rate": (
                    self.webhook_metrics["deliveries_successful"] /
                    max(1, self.webhook_metrics["deliveries_attempted"]) * 100
                ),
                "ai_processing": self.webhook_config["ai_processing_enabled"]
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function pour compatibilité
def create_webhook_handler(**config) -> AgentWebhookHandler_Enterprise:
    """Factory function pour créer l'agent"""
    return AgentWebhookHandler_Enterprise(**config)

# Test standalone
async def main():
    """Test de l'agent Webhook Handler"""
    print("🔗 Test Agent Webhook Handler NextGeneration v5.3.0")
    
    agent = create_webhook_handler(agent_id="test_webhook")
    
    # Health check
    health = await agent.health_check()
    print(f"🏥 Health: {health['status']}")
    
    # Enregistrement endpoint
    endpoint = WebhookEndpoint(
        endpoint_id="test_endpoint",
        name="Test Webhook",
        url="https://httpbin.org/post",
        webhook_type=WebhookType.OUTGOING,
        event_types=[EventType.SYSTEM, EventType.APPLICATION]
    )
    
    success = await agent.register_endpoint(endpoint)
    print(f"🔗 Endpoint enregistré: {success}")
    
    # Simulation événement
    event = WebhookEvent(
        event_id=str(uuid.uuid4()),
        event_type=EventType.SYSTEM,
        source="test_application",
        payload={"message": "Test event", "priority": "high"},
        timestamp=datetime.now()
    )
    
    result = await agent.receive_webhook(event)
    print(f"📥 Événement traité: {result.get('processed', False)}")
    
    # Attente traitement
    await asyncio.sleep(2)
    
    # Statistiques
    stats = await agent.get_webhook_stats()
    print(f"📊 Événements: {stats['webhook_metrics']['events_processed']}")

if __name__ == "__main__":
    asyncio.run(main())