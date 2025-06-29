#!/usr/bin/env python3
"""
📢 Agent Notification Service - NextGeneration v5.3.0
Version enterprise Wave 4 avec notification multi-canal intelligente

Migration Pattern: MESSAGING + LLM_ENHANCED + MULTI_CHANNEL
Author: Claude Sonnet 4
Date: 30 Juin 2025
"""

import asyncio
import json
import time
import smtplib
import ssl
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import uuid
import sqlite3
import re
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
import aiohttp
import httpx

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

class NotificationChannel(str, Enum):
    """Canaux de notification"""
    EMAIL = "EMAIL"
    SMS = "SMS"
    WEBHOOK = "WEBHOOK"
    PUSH = "PUSH"
    SLACK = "SLACK"
    TEAMS = "TEAMS"
    DISCORD = "DISCORD"
    TELEGRAM = "TELEGRAM"

class NotificationPriority(str, Enum):
    """Priorités notification"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"

class NotificationStatus(str, Enum):
    """Statuts notification"""
    PENDING = "PENDING"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    CANCELLED = "CANCELLED"

class MessageFormat(str, Enum):
    """Formats de message"""
    TEXT = "TEXT"
    HTML = "HTML"
    MARKDOWN = "MARKDOWN"
    JSON = "JSON"

@dataclass
class NotificationTemplate:
    """Template de notification"""
    template_id: str
    name: str
    subject_template: str
    body_template: str
    format: MessageFormat
    channels: List[NotificationChannel]
    variables: List[str] = None
    metadata: Dict[str, Any] = None
    created_at: datetime = None

@dataclass
class NotificationRecipient:
    """Destinataire notification"""
    recipient_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    webhook_url: Optional[str] = None
    push_token: Optional[str] = None
    slack_channel: Optional[str] = None
    teams_webhook: Optional[str] = None
    preferred_channels: List[NotificationChannel] = None
    timezone: str = "UTC"
    active: bool = True
    metadata: Dict[str, Any] = None

@dataclass
class NotificationRequest:
    """Demande de notification"""
    request_id: str
    template_id: str
    recipients: List[str]  # recipient_ids
    variables: Dict[str, Any]
    priority: NotificationPriority
    channels: List[NotificationChannel] = None
    schedule_time: Optional[datetime] = None
    retry_count: int = 3
    metadata: Dict[str, Any] = None
    created_at: datetime = None

@dataclass
class NotificationDelivery:
    """Livraison notification"""
    delivery_id: str
    request_id: str
    recipient_id: str
    channel: NotificationChannel
    status: NotificationStatus
    attempt_count: int = 0
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    error_message: Optional[str] = None
    response_data: Optional[Dict[str, Any]] = None
    retry_at: Optional[datetime] = None

class IntelligentNotificationRouter:
    """Routeur de notifications intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.routing_rules = {}
        self.channel_preferences = {}
        self.delivery_history = []
    
    async def route_notification(self, request: NotificationRequest, 
                               recipients: List[NotificationRecipient]) -> Dict[str, List[NotificationChannel]]:
        """Routage intelligent de notification"""
        routing_plan = {}
        
        for recipient in recipients:
            # Routage de base basé sur préférences
            channels = await self._get_preferred_channels(recipient, request)
            
            # Enhancement IA pour optimisation routage
            if self.llm_gateway:
                try:
                    ai_routing = await self.llm_gateway.process_request(
                        "Optimize notification routing strategy",
                        context={
                            "role": "notification_routing_expert",
                            "recipient": asdict(recipient),
                            "request": asdict(request),
                            "available_channels": [c.value for c in channels],
                            "delivery_history": self._get_recipient_history(recipient.recipient_id),
                            "task": "intelligent_channel_selection"
                        }
                    )
                    
                    if ai_routing.get("success"):
                        optimized_channels = ai_routing.get("optimal_channels", [])
                        if optimized_channels:
                            channels = [NotificationChannel(c) for c in optimized_channels if c in [ch.value for ch in channels]]
                            
                except Exception as e:
                    self.logger = logging.getLogger(f"NotificationRouter_{id(self)}")
                    self.logger.warning(f"⚠️ Erreur routage IA: {e}")
            
            routing_plan[recipient.recipient_id] = channels
        
        return routing_plan
    
    async def _get_preferred_channels(self, recipient: NotificationRecipient, 
                                    request: NotificationRequest) -> List[NotificationChannel]:
        """Sélection canaux préférés"""
        channels = []
        
        # Priorité aux canaux demandés
        if request.channels:
            channels.extend(request.channels)
        
        # Ajout des canaux préférés du destinataire
        if recipient.preferred_channels:
            for channel in recipient.preferred_channels:
                if channel not in channels:
                    channels.append(channel)
        
        # Canaux disponibles basés sur les informations du destinataire
        available_channels = []
        if recipient.email and NotificationChannel.EMAIL not in available_channels:
            available_channels.append(NotificationChannel.EMAIL)
        if recipient.phone and NotificationChannel.SMS not in available_channels:
            available_channels.append(NotificationChannel.SMS)
        if recipient.webhook_url and NotificationChannel.WEBHOOK not in available_channels:
            available_channels.append(NotificationChannel.WEBHOOK)
        if recipient.push_token and NotificationChannel.PUSH not in available_channels:
            available_channels.append(NotificationChannel.PUSH)
        if recipient.slack_channel and NotificationChannel.SLACK not in available_channels:
            available_channels.append(NotificationChannel.SLACK)
        if recipient.teams_webhook and NotificationChannel.TEAMS not in available_channels:
            available_channels.append(NotificationChannel.TEAMS)
        
        # Filtrage par disponibilité
        channels = [ch for ch in channels if ch in available_channels]
        
        # Fallback sur email si aucun canal disponible
        if not channels and NotificationChannel.EMAIL in available_channels:
            channels = [NotificationChannel.EMAIL]
        
        return channels
    
    def _get_recipient_history(self, recipient_id: str) -> List[Dict[str, Any]]:
        """Historique livraisons destinataire"""
        history = []
        for delivery in self.delivery_history[-50:]:  # 50 dernières livraisons
            if delivery.get("recipient_id") == recipient_id:
                history.append({
                    "channel": delivery.get("channel"),
                    "status": delivery.get("status"),
                    "sent_at": delivery.get("sent_at"),
                    "success": delivery.get("status") in ["SENT", "DELIVERED"]
                })
        return history

class NotificationChannelManager:
    """Gestionnaire canaux de notification"""
    
    def __init__(self, notification_service):
        self.service = notification_service
        self.channel_configs = {}
        self.delivery_handlers = {
            NotificationChannel.EMAIL: self._send_email,
            NotificationChannel.SMS: self._send_sms,
            NotificationChannel.WEBHOOK: self._send_webhook,
            NotificationChannel.PUSH: self._send_push,
            NotificationChannel.SLACK: self._send_slack,
            NotificationChannel.TEAMS: self._send_teams
        }
    
    async def send_notification(self, delivery: NotificationDelivery, 
                              recipient: NotificationRecipient,
                              rendered_message: Dict[str, str]) -> bool:
        """Envoi notification via canal spécifique"""
        try:
            handler = self.delivery_handlers.get(delivery.channel)
            if not handler:
                raise ValueError(f"Canal non supporté: {delivery.channel}")
            
            success = await handler(delivery, recipient, rendered_message)
            return success
            
        except Exception as e:
            self.service.logger.error(f"❌ Erreur envoi {delivery.channel}: {e}")
            return False
    
    async def _send_email(self, delivery: NotificationDelivery, 
                         recipient: NotificationRecipient, 
                         message: Dict[str, str]) -> bool:
        """Envoi email"""
        try:
            if not recipient.email:
                raise ValueError("Email destinataire manquant")
            
            config = self.channel_configs.get("email", {})
            smtp_server = config.get("smtp_server", "localhost")
            smtp_port = config.get("smtp_port", 587)
            username = config.get("username")
            password = config.get("password")
            from_email = config.get("from_email", "noreply@nextgeneration.ai")
            
            # Création message
            msg = MimeMultipart('alternative')
            msg['Subject'] = message.get("subject", "Notification")
            msg['From'] = from_email
            msg['To'] = recipient.email
            
            # Corps du message
            if message.get("format") == "HTML":
                body = MimeText(message["body"], 'html', 'utf-8')
            else:
                body = MimeText(message["body"], 'plain', 'utf-8')
            
            msg.attach(body)
            
            # Envoi
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if username and password:
                    server.starttls(context=context)
                    server.login(username, password)
                
                server.send_message(msg)
            
            delivery.sent_at = datetime.now()
            self.service.logger.info(f"✅ Email envoyé: {recipient.email}")
            return True
            
        except Exception as e:
            self.service.logger.error(f"❌ Erreur email: {e}")
            return False
    
    async def _send_sms(self, delivery: NotificationDelivery, 
                       recipient: NotificationRecipient, 
                       message: Dict[str, str]) -> bool:
        """Envoi SMS"""
        try:
            if not recipient.phone:
                raise ValueError("Téléphone destinataire manquant")
            
            config = self.channel_configs.get("sms", {})
            provider = config.get("provider", "twilio")
            api_key = config.get("api_key")
            
            if not api_key:
                raise ValueError("Configuration SMS manquante")
            
            # Simulation envoi SMS (à adapter selon provider)
            self.service.logger.info(f"📱 SMS simulé: {recipient.phone}")
            delivery.sent_at = datetime.now()
            return True
            
        except Exception as e:
            self.service.logger.error(f"❌ Erreur SMS: {e}")
            return False
    
    async def _send_webhook(self, delivery: NotificationDelivery, 
                          recipient: NotificationRecipient, 
                          message: Dict[str, str]) -> bool:
        """Envoi webhook"""
        try:
            if not recipient.webhook_url:
                raise ValueError("URL webhook manquante")
            
            payload = {
                "notification_id": delivery.delivery_id,
                "recipient": recipient.recipient_id,
                "subject": message.get("subject"),
                "body": message.get("body"),
                "timestamp": datetime.now().isoformat(),
                "metadata": delivery.request_id
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    recipient.webhook_url,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    delivery.sent_at = datetime.now()
                    delivery.response_data = {"status_code": response.status_code}
                    self.service.logger.info(f"🔗 Webhook envoyé: {recipient.webhook_url}")
                    return True
                else:
                    raise Exception(f"HTTP {response.status_code}")
                    
        except Exception as e:
            self.service.logger.error(f"❌ Erreur webhook: {e}")
            return False
    
    async def _send_push(self, delivery: NotificationDelivery, 
                        recipient: NotificationRecipient, 
                        message: Dict[str, str]) -> bool:
        """Envoi push notification"""
        try:
            if not recipient.push_token:
                raise ValueError("Token push manquant")
            
            # Simulation push notification
            self.service.logger.info(f"📱 Push simulé: {recipient.push_token[:20]}...")
            delivery.sent_at = datetime.now()
            return True
            
        except Exception as e:
            self.service.logger.error(f"❌ Erreur push: {e}")
            return False
    
    async def _send_slack(self, delivery: NotificationDelivery, 
                         recipient: NotificationRecipient, 
                         message: Dict[str, str]) -> bool:
        """Envoi Slack"""
        try:
            if not recipient.slack_channel:
                raise ValueError("Canal Slack manquant")
            
            config = self.channel_configs.get("slack", {})
            webhook_url = config.get("webhook_url")
            
            if not webhook_url:
                raise ValueError("Configuration Slack manquante")
            
            payload = {
                "channel": recipient.slack_channel,
                "text": message.get("body"),
                "username": "NextGeneration Notifications"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(webhook_url, json=payload, timeout=30.0)
                
                if response.status_code == 200:
                    delivery.sent_at = datetime.now()
                    self.service.logger.info(f"💬 Slack envoyé: {recipient.slack_channel}")
                    return True
                else:
                    raise Exception(f"HTTP {response.status_code}")
                    
        except Exception as e:
            self.service.logger.error(f"❌ Erreur Slack: {e}")
            return False
    
    async def _send_teams(self, delivery: NotificationDelivery, 
                         recipient: NotificationRecipient, 
                         message: Dict[str, str]) -> bool:
        """Envoi Microsoft Teams"""
        try:
            if not recipient.teams_webhook:
                raise ValueError("Webhook Teams manquant")
            
            payload = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "summary": message.get("subject"),
                "themeColor": "0078D4",
                "sections": [{
                    "activityTitle": message.get("subject"),
                    "activityText": message.get("body")
                }]
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    recipient.teams_webhook, 
                    json=payload, 
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    delivery.sent_at = datetime.now()
                    self.service.logger.info(f"🏢 Teams envoyé: {recipient.recipient_id}")
                    return True
                else:
                    raise Exception(f"HTTP {response.status_code}")
                    
        except Exception as e:
            self.service.logger.error(f"❌ Erreur Teams: {e}")
            return False

class IntelligentMessageRenderer:
    """Rendu de messages intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.template_cache = {}
    
    async def render_message(self, template: NotificationTemplate, 
                           variables: Dict[str, Any],
                           recipient: NotificationRecipient,
                           channel: NotificationChannel) -> Dict[str, str]:
        """Rendu message avec personnalisation IA"""
        try:
            # Rendu de base
            rendered = {
                "subject": self._render_template(template.subject_template, variables),
                "body": self._render_template(template.body_template, variables),
                "format": template.format.value
            }
            
            # Enhancement IA pour personnalisation
            if self.llm_gateway:
                try:
                    ai_enhancement = await self.llm_gateway.process_request(
                        "Enhance notification message for recipient",
                        context={
                            "role": "notification_personalization_expert",
                            "template": asdict(template),
                            "recipient": asdict(recipient),
                            "channel": channel.value,
                            "rendered_message": rendered,
                            "variables": variables,
                            "task": "message_personalization"
                        }
                    )
                    
                    if ai_enhancement.get("success"):
                        enhanced_message = ai_enhancement.get("enhanced_message", {})
                        if enhanced_message:
                            rendered.update(enhanced_message)
                            
                except Exception as e:
                    self.logger = logging.getLogger(f"MessageRenderer_{id(self)}")
                    self.logger.warning(f"⚠️ Erreur enhancement IA: {e}")
            
            # Adaptation format selon canal
            rendered = await self._adapt_for_channel(rendered, channel)
            
            return rendered
            
        except Exception as e:
            self.logger = logging.getLogger(f"MessageRenderer_{id(self)}")
            self.logger.error(f"❌ Erreur rendu message: {e}")
            return {
                "subject": "Notification",
                "body": "Message non disponible",
                "format": "TEXT"
            }
    
    def _render_template(self, template: str, variables: Dict[str, Any]) -> str:
        """Rendu template simple"""
        try:
            # Remplacement variables simples {{variable}}
            rendered = template
            for key, value in variables.items():
                placeholder = f"{{{{{key}}}}}"
                rendered = rendered.replace(placeholder, str(value))
            
            return rendered
            
        except Exception as e:
            return template
    
    async def _adapt_for_channel(self, message: Dict[str, str], 
                               channel: NotificationChannel) -> Dict[str, str]:
        """Adaptation message selon canal"""
        adapted = message.copy()
        
        if channel == NotificationChannel.SMS:
            # Limitation SMS
            max_length = 160
            if len(adapted["body"]) > max_length:
                adapted["body"] = adapted["body"][:max_length-3] + "..."
        
        elif channel == NotificationChannel.SLACK:
            # Format Slack markdown
            if adapted["format"] == "HTML":
                adapted["body"] = self._html_to_slack_markdown(adapted["body"])
                adapted["format"] = "MARKDOWN"
        
        elif channel == NotificationChannel.EMAIL:
            # Conservation format original
            pass
        
        return adapted
    
    def _html_to_slack_markdown(self, html: str) -> str:
        """Conversion HTML vers Slack markdown"""
        # Conversion basique
        markdown = html
        markdown = re.sub(r'<b>(.*?)</b>', r'*\1*', markdown)
        markdown = re.sub(r'<i>(.*?)</i>', r'_\1_', markdown)
        markdown = re.sub(r'<br/?>', '\n', markdown)
        markdown = re.sub(r'<[^>]+>', '', markdown)  # Suppression autres tags
        return markdown

class AgentNotificationService_Enterprise:
    """
    📢 Agent Notification Service - Enterprise NextGeneration v5.3.0
    
    Service de notifications multi-canal intelligent avec personnalisation IA.
    
    Patterns NextGeneration v5.3.0:
    - MESSAGING: Architecture multi-canal avancée
    - LLM_ENHANCED: Personnalisation et routage IA
    - MULTI_CHANNEL: Support canaux multiples
    - PATTERN_FACTORY: Architecture modulaire éprouvée
    """
    
    def __init__(self, agent_id: str = "notification_service", 
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
            "MESSAGING",
            "LLM_ENHANCED", 
            "MULTI_CHANNEL",
            "PATTERN_FACTORY"
        ]
        
        # Configuration agent
        self.name = "Notification Service Enterprise"
        self.mission = "Service notifications multi-canal intelligent avec personnalisation IA"
        self.agent_type = "notification_enterprise"
        
        # Configuration notifications
        self.data_dir = data_dir or Path("/var/lib/nextgeneration/notifications")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Services NextGeneration (injectés à l'initialisation)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Composants notification intelligents
        self.router = IntelligentNotificationRouter()
        self.channel_manager = NotificationChannelManager(self)
        self.message_renderer = IntelligentMessageRenderer()
        
        # Configuration notification
        self.notification_config = {
            "max_recipients_per_request": 1000,
            "retry_max_attempts": 3,
            "retry_delay_seconds": 30,
            "batch_size": 50,
            "delivery_timeout_seconds": 300,
            "ai_enhancement_enabled": True
        }
        
        # État notifications
        self.templates: Dict[str, NotificationTemplate] = {}
        self.recipients: Dict[str, NotificationRecipient] = {}
        self.active_requests: Dict[str, NotificationRequest] = {}
        self.delivery_queue = asyncio.Queue()
        
        # Base de données notifications
        self.db_path = self.data_dir / "notifications.db"
        self._init_database()
        
        # Métriques notifications
        self.notification_metrics = {
            "requests_received": 0,
            "notifications_sent": 0,
            "deliveries_successful": 0,
            "deliveries_failed": 0,
            "average_delivery_time_ms": 0.0,
            "ai_enhancements_count": 0,
            "channels_used": {}
        }
        
        # Background tasks
        self._delivery_workers = []
        self._cleanup_task = None
        
        # Setup logging
        self._setup_logging()
        
        # Démarrage composants
        asyncio.create_task(self._start_background_tasks())
    
    def _init_database(self):
        """Initialisation base de données notifications"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notification_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id TEXT UNIQUE NOT NULL,
                    template_id TEXT NOT NULL,
                    recipients TEXT NOT NULL,
                    variables TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    channels TEXT,
                    schedule_time TEXT,
                    status TEXT DEFAULT 'PENDING',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notification_deliveries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    delivery_id TEXT UNIQUE NOT NULL,
                    request_id TEXT NOT NULL,
                    recipient_id TEXT NOT NULL,
                    channel TEXT NOT NULL,
                    status TEXT NOT NULL,
                    attempt_count INTEGER DEFAULT 0,
                    sent_at TEXT,
                    delivered_at TEXT,
                    error_message TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_delivery_status 
                ON notification_deliveries(status)
            """)
    
    def _setup_logging(self):
        """Configuration logging NextGeneration"""
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="notification",
                custom_config={
                    "logger_name": f"nextgen.notification.service.{self.agent_id}",
                    "log_dir": "logs/notification",
                    "metadata": {
                        "agent_type": "notification_service",
                        "agent_role": "multi_channel_messaging",
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
            self.logger = logging.getLogger(f"NotificationService_{self.agent_id}")
    
    async def inject_nextgen_services(self, 
                                    llm_gateway: LLMGatewayHybrid,
                                    message_bus: MessageBusA2A, 
                                    context_store: OptimizedContextStore):
        """Injection des services NextGeneration v5.3.0"""
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus  
        self.context_store = context_store
        
        # Configuration composants avec IA
        self.router.llm_gateway = llm_gateway
        self.message_renderer.llm_gateway = llm_gateway
        
        # Configuration contexte notification IA
        await self._setup_notification_context()
        
        self.logger.info("✅ Services NextGeneration injectés - Notification IA active")
    
    async def _setup_notification_context(self):
        """Configuration contexte notification IA spécialisé"""
        if not self.llm_gateway:
            return
        
        notification_context = {
            "role": "multi_channel_notification_expert",
            "domain": "enterprise_messaging_automation",
            "capabilities": [
                "Multi-channel message delivery",
                "Intelligent routing optimization",
                "Message personalization",
                "Delivery optimization",
                "Channel-specific adaptation"
            ],
            "patterns": [
                "MESSAGING",
                "LLM_ENHANCED",
                "MULTI_CHANNEL"
            ]
        }
        
        # Chargement expertise notification depuis LLM
        try:
            response = await self.llm_gateway.process_request(
                "Load multi-channel notification expertise",
                context=notification_context
            )
            
            if response.get("success"):
                self.logger.info("🧠 Expertise notification IA chargée")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement contexte IA: {e}")
    
    async def register_template(self, template: NotificationTemplate) -> bool:
        """Enregistrement template notification"""
        try:
            template.created_at = datetime.now()
            self.templates[template.template_id] = template
            self.logger.info(f"📋 Template enregistré: {template.name}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur enregistrement template: {e}")
            return False
    
    async def register_recipient(self, recipient: NotificationRecipient) -> bool:
        """Enregistrement destinataire"""
        try:
            self.recipients[recipient.recipient_id] = recipient
            self.logger.info(f"👤 Destinataire enregistré: {recipient.name}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur enregistrement destinataire: {e}")
            return False
    
    async def send_notification(self, request: NotificationRequest) -> Dict[str, Any]:
        """Envoi notification avec routage intelligent"""
        try:
            self.logger.info(f"📢 Notification demandée: {request.template_id} pour {len(request.recipients)} destinataires")
            
            # Validation
            if request.template_id not in self.templates:
                raise ValueError(f"Template non trouvé: {request.template_id}")
            
            template = self.templates[request.template_id]
            request.created_at = datetime.now()
            
            # Stockage demande
            await self._store_request(request)
            self.active_requests[request.request_id] = request
            
            # Récupération destinataires
            recipients = []
            for recipient_id in request.recipients:
                if recipient_id in self.recipients:
                    recipients.append(self.recipients[recipient_id])
                else:
                    self.logger.warning(f"⚠️ Destinataire non trouvé: {recipient_id}")
            
            if not recipients:
                raise ValueError("Aucun destinataire valide")
            
            # Routage intelligent
            routing_plan = await self.router.route_notification(request, recipients)
            
            # Création livraisons
            deliveries = []
            for recipient in recipients:
                channels = routing_plan.get(recipient.recipient_id, [])
                for channel in channels:
                    delivery = NotificationDelivery(
                        delivery_id=str(uuid.uuid4()),
                        request_id=request.request_id,
                        recipient_id=recipient.recipient_id,
                        channel=channel,
                        status=NotificationStatus.PENDING
                    )
                    deliveries.append(delivery)
            
            # Ajout à la queue de livraison
            for delivery in deliveries:
                await self.delivery_queue.put({
                    "delivery": delivery,
                    "template": template,
                    "variables": request.variables,
                    "recipient": next(r for r in recipients if r.recipient_id == delivery.recipient_id)
                })
            
            self.notification_metrics["requests_received"] += 1
            
            result = {
                "success": True,
                "request_id": request.request_id,
                "deliveries_created": len(deliveries),
                "routing_plan": {r.recipient_id: [c.value for c in channels] 
                               for r in recipients 
                               for channels in [routing_plan.get(r.recipient_id, [])]},
                "timestamp": datetime.now().isoformat()
            }
            
            # Notification via MessageBus
            if self.message_bus:
                await self.message_bus.publish(
                    create_envelope(
                        message_type=MessageType.EVENT,
                        payload={
                            "type": "notification_request_processed",
                            "request": asdict(request),
                            "result": result,
                            "timestamp": datetime.now().isoformat()
                        },
                        priority=Priority.MEDIUM
                    )
                )
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Erreur envoi notification: {e}")
            return {"success": False, "error": str(e)}
    
    async def _store_request(self, request: NotificationRequest):
        """Stockage demande notification"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO notification_requests 
                   (request_id, template_id, recipients, variables, priority, channels, schedule_time) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    request.request_id,
                    request.template_id,
                    json.dumps(request.recipients),
                    json.dumps(request.variables),
                    request.priority.value,
                    json.dumps([c.value for c in request.channels] if request.channels else None),
                    request.schedule_time.isoformat() if request.schedule_time else None
                )
            )
    
    async def _store_delivery(self, delivery: NotificationDelivery):
        """Stockage livraison notification"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO notification_deliveries 
                   (delivery_id, request_id, recipient_id, channel, status, attempt_count, sent_at, error_message) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    delivery.delivery_id,
                    delivery.request_id,
                    delivery.recipient_id,
                    delivery.channel.value,
                    delivery.status.value,
                    delivery.attempt_count,
                    delivery.sent_at.isoformat() if delivery.sent_at else None,
                    delivery.error_message
                )
            )
        
        # Mise à jour métriques
        if delivery.status == NotificationStatus.SENT:
            self.notification_metrics["deliveries_successful"] += 1
            self.notification_metrics["channels_used"][delivery.channel.value] = \
                self.notification_metrics["channels_used"].get(delivery.channel.value, 0) + 1
        else:
            self.notification_metrics["deliveries_failed"] += 1
    
    async def _start_background_tasks(self):
        """Démarrage tâches background"""
        # Workers de livraison
        for i in range(3):
            worker = asyncio.create_task(self._delivery_worker(f"worker_{i}"))
            self._delivery_workers.append(worker)
        
        # Nettoyage périodique
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    async def _delivery_worker(self, worker_name: str):
        """Worker de livraison notifications"""
        while True:
            try:
                # Récupération tâche
                task = await self.delivery_queue.get()
                delivery = task["delivery"]
                template = task["template"]
                variables = task["variables"]
                recipient = task["recipient"]
                
                # Traitement livraison
                await self._process_delivery(delivery, template, variables, recipient)
                
                self.delivery_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"❌ Erreur worker {worker_name}: {e}")
    
    async def _process_delivery(self, delivery: NotificationDelivery, 
                              template: NotificationTemplate,
                              variables: Dict[str, Any],
                              recipient: NotificationRecipient):
        """Traitement livraison notification"""
        max_attempts = self.notification_config["retry_max_attempts"]
        
        for attempt in range(max_attempts):
            delivery.attempt_count = attempt + 1
            
            try:
                # Rendu message
                rendered_message = await self.message_renderer.render_message(
                    template, variables, recipient, delivery.channel
                )
                
                # Envoi
                success = await self.channel_manager.send_notification(
                    delivery, recipient, rendered_message
                )
                
                if success:
                    delivery.status = NotificationStatus.SENT
                    delivery.delivered_at = datetime.now()
                    break
                else:
                    if attempt < max_attempts - 1:
                        delivery.status = NotificationStatus.RETRYING
                        delay = self.notification_config["retry_delay_seconds"] * (2 ** attempt)
                        delivery.retry_at = datetime.now() + timedelta(seconds=delay)
                        await asyncio.sleep(delay)
                    else:
                        delivery.status = NotificationStatus.FAILED
                        
            except Exception as e:
                delivery.error_message = str(e)
                self.logger.error(f"❌ Erreur livraison {delivery.delivery_id}: {e}")
                
                if attempt == max_attempts - 1:
                    delivery.status = NotificationStatus.FAILED
        
        # Stockage résultat
        await self._store_delivery(delivery)
        
        if delivery.status == NotificationStatus.SENT:
            self.logger.info(f"✅ Notification livrée: {delivery.delivery_id}")
        else:
            self.logger.warning(f"⚠️ Échec livraison: {delivery.delivery_id}")
    
    async def _cleanup_loop(self):
        """Nettoyage notifications anciennes"""
        while True:
            try:
                await asyncio.sleep(3600)  # Nettoyage horaire
                
                # Suppression anciennes livraisons
                cutoff_date = datetime.now() - timedelta(days=30)
                
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute(
                        "DELETE FROM notification_deliveries WHERE created_at < ?",
                        (cutoff_date.isoformat(),)
                    )
                    deleted_count = cursor.rowcount
                    
                    if deleted_count > 0:
                        self.logger.info(f"🧹 Nettoyage: {deleted_count} livraisons supprimées")
                        
            except Exception as e:
                self.logger.error(f"❌ Erreur nettoyage: {e}")
    
    async def get_notification_stats(self) -> Dict[str, Any]:
        """Statistiques notifications détaillées"""
        # Calcul success rate
        total_deliveries = (self.notification_metrics["deliveries_successful"] + 
                          self.notification_metrics["deliveries_failed"])
        success_rate = 0.0
        if total_deliveries > 0:
            success_rate = (self.notification_metrics["deliveries_successful"] / total_deliveries) * 100
        
        return {
            "notification_metrics": self.notification_metrics,
            "success_rate": success_rate,
            "templates_count": len(self.templates),
            "recipients_count": len(self.recipients),
            "active_requests": len(self.active_requests),
            "queue_size": self.delivery_queue.qsize(),
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
            "notification": {
                "templates_loaded": len(self.templates),
                "recipients_registered": len(self.recipients),
                "queue_size": self.delivery_queue.qsize(),
                "success_rate": (
                    self.notification_metrics["deliveries_successful"] /
                    max(1, self.notification_metrics["deliveries_successful"] + 
                        self.notification_metrics["deliveries_failed"]) * 100
                ),
                "ai_enhancement": self.notification_config["ai_enhancement_enabled"]
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function pour compatibilité
def create_notification_service(**config) -> AgentNotificationService_Enterprise:
    """Factory function pour créer l'agent"""
    return AgentNotificationService_Enterprise(**config)

# Test standalone
async def main():
    """Test de l'agent Notification Service"""
    print("📢 Test Agent Notification Service NextGeneration v5.3.0")
    
    agent = create_notification_service(agent_id="test_notification")
    
    # Health check
    health = await agent.health_check()
    print(f"🏥 Health: {health['status']}")
    
    # Enregistrement template
    template = NotificationTemplate(
        template_id="test_template",
        name="Test Notification",
        subject_template="Test: {{title}}",
        body_template="Bonjour {{name}}, voici votre notification: {{message}}",
        format=MessageFormat.TEXT,
        channels=[NotificationChannel.EMAIL, NotificationChannel.WEBHOOK]
    )
    
    success = await agent.register_template(template)
    print(f"📋 Template enregistré: {success}")
    
    # Enregistrement destinataire
    recipient = NotificationRecipient(
        recipient_id="test_recipient",
        name="Test User",
        email="test@example.com",
        webhook_url="https://httpbin.org/post",
        preferred_channels=[NotificationChannel.EMAIL]
    )
    
    success = await agent.register_recipient(recipient)
    print(f"👤 Destinataire enregistré: {success}")
    
    # Envoi notification
    request = NotificationRequest(
        request_id=str(uuid.uuid4()),
        template_id="test_template",
        recipients=["test_recipient"],
        variables={
            "title": "Test Notification",
            "name": "Test User",
            "message": "Ceci est un test de notification multi-canal"
        },
        priority=NotificationPriority.MEDIUM
    )
    
    result = await agent.send_notification(request)
    print(f"📢 Notification envoyée: {result.get('success', False)}")
    
    # Attente traitement
    await asyncio.sleep(3)
    
    # Statistiques
    stats = await agent.get_notification_stats()
    print(f"📊 Notifications: {stats['notification_metrics']['notifications_sent']}")

if __name__ == "__main__":
    asyncio.run(main())