#!/usr/bin/env python3
"""
LoggingManager Centralisé NextGeneration - Version Optimisée ChatGPT
Gestion unifiée de tous les logs du système avec performances améliorées
Intégration Elasticsearch, Alerting intelligent, Sécurité renforcée
"""

import asyncio
import json
import logging
import logging.handlers
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Union
from dataclasses import dataclass, asdict, field
import threading
import queue
import gzip
import shutil
from functools import lru_cache
import atexit
import signal
import hashlib
import hmac
from cryptography.fernet import Fernet
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# PHASE 2: Imports pour monitoring avancé OpenTelemetry
try:
    from opentelemetry import trace, metrics
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import ConsoleMetricsExporter, PeriodicExportingMetricReader
    from opentelemetry.instrumentation.logging import LoggingInstrumentor
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    # Fallback si OpenTelemetry n'est pas installé
    OPENTELEMETRY_AVAILABLE = False
    trace = None
    metrics = None

# PHASE 2: Constantes pour monitoring avancé
TRACING_ENABLED = True
METRICS_EXPORT_INTERVAL = 30  # secondes
JAEGER_ENDPOINT = "http://localhost:14268/api/traces"
PERFORMANCE_THRESHOLD_MS = 100  # seuil performance en millisecondes

# Constants améliorés ChatGPT
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s"
ASYNC_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - [%(task_name)s] - %(message)s"
SECURITY_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - [AUDIT] - %(message)s"
MAX_LOG_SIZE = 50 * 1024 * 1024  # 50MB
COMPRESSION_THRESHOLD = 100 * 1024 * 1024  # 100MB
ELASTICSEARCH_BATCH_SIZE = 1000
ALERT_THRESHOLD_ERRORS = 10
ALERT_THRESHOLD_CRITICAL = 5
ENCRYPTION_KEY_LENGTH = 32

class LogLevel(Enum):
    """Niveaux de log standardisés"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogCategory(Enum):
    """Catégories de logs pour organisation"""
    AGENT = "agents"
    TOOL = "tools"
    SYSTEM = "system"
    ERROR = "errors"
    AUDIT = "audit"
    PERFORMANCE = "performance"

@dataclass
class LoggingConfig:
    """Configuration de logging enrichie pour un composant - Version ChatGPT optimisée"""
    logger_name: str
    log_level: str = "INFO"
    log_dir: str = "logs"
    filename_pattern: str = "{component}_{date}.log"
    max_file_size: int = MAX_LOG_SIZE
    backup_count: int = 10
    console_enabled: bool = True
    file_enabled: bool = True
    format_string: str = DEFAULT_FORMAT
    async_enabled: bool = False
    compression_enabled: bool = True
    retention_days: int = 30
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Nouvelles fonctionnalités ChatGPT
    elasticsearch_enabled: bool = False
    elasticsearch_host: str = "localhost:9200"
    elasticsearch_index: str = "nextgen-logs"
    encryption_enabled: bool = False
    encryption_key: Optional[str] = None
    alerting_enabled: bool = False
    alert_email: Optional[str] = None
    alert_webhook: Optional[str] = None
    sensitive_data_masking: bool = True
    
    # PHASE 2: Monitoring avancé
    advanced_monitoring_enabled: bool = True

@dataclass
class LogMetrics:
    """Métriques de performance du système de logging - Version ChatGPT enrichie"""
    total_logs: int = 0
    logs_per_level: Dict[str, int] = field(default_factory=lambda: {level.value: 0 for level in LogLevel})
    logs_per_category: Dict[str, int] = field(default_factory=lambda: {cat.value: 0 for cat in LogCategory})
    average_log_size: float = 0.0
    compression_ratio: float = 0.0
    errors_count: int = 0
    last_error: Optional[str] = None
    performance_stats: Dict[str, float] = field(default_factory=dict)
    
    # Nouvelles métriques ChatGPT
    elasticsearch_docs_sent: int = 0
    elasticsearch_errors: int = 0
    alerts_sent: int = 0
    encrypted_logs: int = 0
    sensitive_data_masked: int = 0
    async_queue_size: int = 0
    async_queue_max_size: int = 0
    compression_savings_bytes: int = 0

class AsyncLogHandler(logging.Handler):
    """Handler asynchrone haute performance - Version ChatGPT optimisée"""
    
    def __init__(self, base_handler: logging.Handler, queue_size: int = 10000, 
                 batch_size: int = 100, flush_interval: float = 1.0):
        super().__init__()
        self.base_handler = base_handler
        self.queue = queue.Queue(maxsize=queue_size)
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        self._shutdown = False
        self._stats = {"processed": 0, "batches": 0, "errors": 0}
        
    def _worker(self):
        """Worker thread pour traitement asynchrone optimisé par batch"""
        batch = []
        last_flush = time.time()
        
        while not self._shutdown:
            try:
                # Essayer de récupérer un record
                try:
                    record = self.queue.get(timeout=0.1)
                    if record is None:  # Signal de shutdown
                        self._flush_batch(batch)
                        break
                    batch.append(record)
                except queue.Empty:
                    # Vérifier si il faut flush par timeout
                    if batch and (time.time() - last_flush) > self.flush_interval:
                        self._flush_batch(batch)
                        batch = []
                        last_flush = time.time()
                    continue
                
                # Flush si batch plein
                if len(batch) >= self.batch_size:
                    self._flush_batch(batch)
                    batch = []
                    last_flush = time.time()
                    
            except Exception as e:
                self._stats["errors"] += 1
                print(f"Erreur dans worker de logging: {e}", file=sys.stderr)
    
    def _flush_batch(self, batch):
        """Flush un batch de logs"""
        if not batch:
            return
            
        try:
            for record in batch:
                self.base_handler.emit(record)
            self._stats["processed"] += len(batch)
            self._stats["batches"] += 1
        except Exception as e:
            self._stats["errors"] += 1
            print(f"Erreur flush batch: {e}", file=sys.stderr)
    
    def emit(self, record):
        """Émission asynchrone du log optimisée"""
        try:
            self.queue.put_nowait(record)
        except queue.Full:
            # En cas de queue pleine, log directement (fallback synchrone)
            try:
                self.base_handler.emit(record)
            except Exception as e:
                print(f"Erreur fallback sync: {e}", file=sys.stderr)
    
    def get_stats(self) -> Dict[str, int]:
        """Statistiques du handler asynchrone"""
        return {
            **self._stats,
            "queue_size": self.queue.qsize(),
            "queue_max_size": self.queue.maxsize
        }
    
    def close(self):
        """Fermeture propre du handler"""
        self._shutdown = True
        self.queue.put(None)
        self.worker_thread.join(timeout=5)
        self.base_handler.close()
        super().close()

class CompressingRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """Handler avec compression automatique des anciens logs"""
    
    def __init__(self, *args, compression_enabled=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.compression_enabled = compression_enabled
        
    def doRollover(self):
        """Rotation avec compression"""
        super().doRollover()
        
        if self.compression_enabled and self.backupCount > 0:
            # Compresser le fichier qui vient d'être rotaté
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename(f"{self.baseFilename}.{i}")
                if os.path.exists(sfn) and not sfn.endswith('.gz'):
                    self._compress_file(sfn)
    
    def _compress_file(self, filepath):
        """Compresse un fichier log"""
        try:
            with open(filepath, 'rb') as f_in:
                with gzip.open(f"{filepath}.gz", 'wb', compresslevel=9) as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(filepath)
        except Exception as e:
            print(f"Erreur compression {filepath}: {e}", file=sys.stderr)

class ElasticsearchHandler(logging.Handler):
    """Handler pour envoi vers Elasticsearch - Nouvelle fonctionnalité ChatGPT"""
    
    def __init__(self, host: str, index: str, batch_size: int = ELASTICSEARCH_BATCH_SIZE):
        super().__init__()
        self.host = host
        self.index = index
        self.batch_size = batch_size
        self.batch = []
        self.lock = threading.Lock()
        
    def emit(self, record):
        """Émission vers Elasticsearch en batch"""
        try:
            doc = {
                "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "thread": record.thread,
                "process": record.process
            }
            
            if hasattr(record, 'extra'):
                doc.update(record.extra)
            
            with self.lock:
                self.batch.append(doc)
                if len(self.batch) >= self.batch_size:
                    self._flush_batch()
        except Exception as e:
            print(f"Erreur Elasticsearch emit: {e}", file=sys.stderr)
    
    def _flush_batch(self):
        """Flush le batch vers Elasticsearch"""
        if not self.batch:
            return
        
        try:
            # Simulation d'envoi Elasticsearch (remplacer par vraie implémentation)
            print(f"[ELASTICSEARCH] Envoi de {len(self.batch)} documents vers {self.host}/{self.index}")
            self.batch.clear()
        except Exception as e:
            print(f"Erreur flush Elasticsearch: {e}", file=sys.stderr)
    
    def close(self):
        """Fermeture avec flush final"""
        with self.lock:
            self._flush_batch()
        super().close()

class EncryptionHandler(logging.Handler):
    """Handler avec chiffrement des logs sensibles - Nouvelle fonctionnalité ChatGPT"""
    
    def __init__(self, base_handler: logging.Handler, encryption_key: str):
        super().__init__()
        self.base_handler = base_handler
        self.cipher = Fernet(encryption_key.encode() if len(encryption_key) == 44 else 
                           Fernet.generate_key())
        
    def emit(self, record):
        """Émission avec chiffrement conditionnel"""
        try:
            # Chiffrer si le log contient des données sensibles
            if self._is_sensitive(record):
                original_msg = record.getMessage()
                encrypted_msg = self.cipher.encrypt(original_msg.encode()).decode()
                record.msg = f"[ENCRYPTED] {encrypted_msg}"
            
            self.base_handler.emit(record)
        except Exception as e:
            print(f"Erreur chiffrement: {e}", file=sys.stderr)
    
    def _is_sensitive(self, record) -> bool:
        """Détecte si un log contient des données sensibles"""
        sensitive_keywords = ['password', 'token', 'secret', 'key', 'credential', 'auth']
        message = record.getMessage().lower()
        return any(keyword in message for keyword in sensitive_keywords)

class AlertingHandler(logging.Handler):
    """Handler pour alertes automatiques - Nouvelle fonctionnalité ChatGPT"""
    
    def __init__(self, email: Optional[str] = None, webhook: Optional[str] = None):
        super().__init__()
        self.email = email
        self.webhook = webhook
        self.error_count = 0
        self.critical_count = 0
        self.last_alert = datetime.min
        self.alert_cooldown = timedelta(minutes=5)  # Éviter spam
        
    def emit(self, record):
        """Émission avec gestion d'alertes"""
        try:
            if record.levelno >= logging.ERROR:
                self.error_count += 1
                
            if record.levelno >= logging.CRITICAL:
                self.critical_count += 1
                
            # Déclencher alerte si seuils atteints
            if (self.error_count >= ALERT_THRESHOLD_ERRORS or 
                self.critical_count >= ALERT_THRESHOLD_CRITICAL):
                
                if datetime.now() - self.last_alert > self.alert_cooldown:
                    self._send_alert(record)
                    self.last_alert = datetime.now()
                    self.error_count = 0
                    self.critical_count = 0
                    
        except Exception as e:
            print(f"Erreur alerting: {e}", file=sys.stderr)
    
    def _send_alert(self, record):
        """Envoie une alerte par email/webhook"""
        alert_message = f"""
        ALERTE NextGeneration Logging
        
        Niveau: {record.levelname}
        Logger: {record.name}
        Message: {record.getMessage()}
        Timestamp: {datetime.now().isoformat()}
        
        Erreurs récentes: {self.error_count}
        Critiques récentes: {self.critical_count}
        """
        
        try:
            if self.email:
                self._send_email_alert(alert_message)
            if self.webhook:
                self._send_webhook_alert(alert_message)
        except Exception as e:
            print(f"Erreur envoi alerte: {e}", file=sys.stderr)
    
    def _send_email_alert(self, message: str):
        """Envoi alerte email (simulation)"""
        print(f"[EMAIL ALERT] {message}")
    
    def _send_webhook_alert(self, message: str):
        """Envoi alerte webhook (simulation)"""
        print(f"[WEBHOOK ALERT] {message}")

class AdvancedMonitoringHandler(logging.Handler):
    """Handler pour monitoring avancé avec OpenTelemetry - PHASE 2"""
    
    def __init__(self, service_name: str = "nextgen-logging", enable_tracing: bool = True):
        super().__init__()
        self.service_name = service_name
        self.enable_tracing = enable_tracing
        self._tracer = None
        self._meter = None
        self._metrics = {}
        
        if OPENTELEMETRY_AVAILABLE and enable_tracing:
            self._setup_tracing()
            self._setup_metrics()
        else:
            self._setup_fallback_metrics()
    
    def _setup_tracing(self):
        """Configuration du tracing distribué"""
        try:
            # Configuration du TracerProvider
            trace.set_tracer_provider(TracerProvider())
            
            # Configuration de l'exporteur Jaeger
            jaeger_exporter = JaegerExporter(
                endpoint=JAEGER_ENDPOINT,
                service_name=self.service_name
            )
            
            # Ajout du processeur de spans
            span_processor = BatchSpanProcessor(jaeger_exporter)
            trace.get_tracer_provider().add_span_processor(span_processor)
            
            # Création du tracer
            self._tracer = trace.get_tracer(__name__)
            
            # Instrumentation automatique du logging
            LoggingInstrumentor().instrument()
            
        except Exception as e:
            print(f"Erreur configuration tracing: {e}", file=sys.stderr)
            self._tracer = None
    
    def _setup_metrics(self):
        """Configuration des métriques avancées"""
        try:
            # Configuration du MeterProvider
            metric_reader = PeriodicExportingMetricReader(
                ConsoleMetricsExporter(),
                export_interval_millis=METRICS_EXPORT_INTERVAL * 1000
            )
            metrics.set_meter_provider(MeterProvider(metric_readers=[metric_reader]))
            
            # Création du meter
            self._meter = metrics.get_meter(__name__)
            
            # Création des métriques
            self._metrics.update({
                "log_counter": self._meter.create_counter(
                    "logs_total",
                    description="Nombre total de logs"
                ),
                "error_counter": self._meter.create_counter(
                    "errors_total",
                    description="Nombre total d'erreurs"
                ),
                "performance_histogram": self._meter.create_histogram(
                    "log_processing_duration_ms",
                    description="Durée de traitement des logs en ms"
                ),
                "queue_size_gauge": self._meter.create_up_down_counter(
                    "log_queue_size",
                    description="Taille actuelle de la queue de logs"
                )
            })
            
        except Exception as e:
            print(f"Erreur configuration métriques: {e}", file=sys.stderr)
            self._setup_fallback_metrics()
    
    def _setup_fallback_metrics(self):
        """Métriques de fallback sans OpenTelemetry"""
        self._metrics = {
            "logs_total": 0,
            "errors_total": 0,
            "processing_times": [],
            "queue_sizes": []
        }
    
    def emit(self, record):
        """Émission avec monitoring avancé"""
        start_time = time.time()
        
        try:
            # Tracing distribué
            if self._tracer:
                with self._tracer.start_as_current_span("log_processing") as span:
                    span.set_attribute("log.level", record.levelname)
                    span.set_attribute("log.logger", record.name)
                    span.set_attribute("log.message", record.getMessage())
                    
                    if record.levelno >= logging.ERROR:
                        span.set_attribute("error", True)
                        span.set_attribute("error.message", record.getMessage())
            
            # Métriques avancées
            processing_time = (time.time() - start_time) * 1000  # en ms
            
            if OPENTELEMETRY_AVAILABLE and self._meter:
                # Métriques OpenTelemetry
                self._metrics["log_counter"].add(1, {"level": record.levelname})
                
                if record.levelno >= logging.ERROR:
                    self._metrics["error_counter"].add(1, {"level": record.levelname})
                
                self._metrics["performance_histogram"].record(
                    processing_time,
                    {"level": record.levelname}
                )
            else:
                # Métriques de fallback
                self._metrics["logs_total"] += 1
                if record.levelno >= logging.ERROR:
                    self._metrics["errors_total"] += 1
                self._metrics["processing_times"].append(processing_time)
                
                # Garder seulement les 1000 dernières mesures
                if len(self._metrics["processing_times"]) > 1000:
                    self._metrics["processing_times"] = self._metrics["processing_times"][-1000:]
            
            # Alerte si performance dégradée
            if processing_time > PERFORMANCE_THRESHOLD_MS:
                self._handle_performance_alert(record, processing_time)
                
        except Exception as e:
            print(f"Erreur monitoring avancé: {e}", file=sys.stderr)
    
    def _handle_performance_alert(self, record, processing_time):
        """Gestion des alertes de performance"""
        alert_message = f"Performance dégradée: {processing_time:.2f}ms > {PERFORMANCE_THRESHOLD_MS}ms pour {record.name}"
        
        # Log de l'alerte
        performance_logger = logging.getLogger("nextgen.performance.alerts")
        performance_logger.warning(alert_message, extra={
            "performance": {
                "processing_time_ms": processing_time,
                "threshold_ms": PERFORMANCE_THRESHOLD_MS,
                "logger_name": record.name,
                "log_level": record.levelname
            }
        })
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Résumé des métriques de monitoring"""
        if OPENTELEMETRY_AVAILABLE and self._meter:
            return {
                "monitoring_type": "opentelemetry",
                "tracing_enabled": self._tracer is not None,
                "metrics_enabled": self._meter is not None,
                "service_name": self.service_name
            }
        else:
            processing_times = self._metrics.get("processing_times", [])
            return {
                "monitoring_type": "fallback",
                "logs_total": self._metrics.get("logs_total", 0),
                "errors_total": self._metrics.get("errors_total", 0),
                "avg_processing_time_ms": sum(processing_times) / len(processing_times) if processing_times else 0,
                "max_processing_time_ms": max(processing_times) if processing_times else 0,
                "performance_alerts": sum(1 for t in processing_times if t > PERFORMANCE_THRESHOLD_MS)
            }

class LoggingManager:
    """Gestionnaire centralisé de logging pour NextGeneration avec optimisations"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.base_log_dir = Path("logs")
        self.config_file = Path("config/logging_centralized.json")
        self._loggers: Dict[str, logging.Logger] = {}
        self._configs: Dict[str, LoggingConfig] = {}
        self._metrics = LogMetrics()
        self._async_handlers: List[AsyncLogHandler] = []
        self._executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="LogManager")
        
        # Configuration du logger interne
        self._internal_logger = self._setup_internal_logger()
        
        # Créer l'arborescence de base
        self._setup_directory_structure()
        
        # Charger ou créer la configuration
        self._load_or_create_config()
        
        # Configurer les hooks de shutdown
        self._setup_shutdown_hooks()
        
        # Démarrer le thread de maintenance
        self._start_maintenance_thread()
        
        # NOUVEAU CHATGPT: Timestamp de démarrage pour métriques
        self._startup_time = datetime.now()
        
        self._internal_logger.info("LoggingManager initialisé avec succès - Version ChatGPT optimisée")
    
    def _setup_internal_logger(self) -> logging.Logger:
        """Configure le logger interne du LoggingManager"""
        logger = logging.getLogger("nextgen.logging.manager")
        logger.setLevel(logging.DEBUG)
        
        # Handler console pour le logger interne
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(DEFAULT_FORMAT))
        logger.addHandler(console_handler)
        
        return logger
    
    def _setup_directory_structure(self):
        """Crée l'arborescence de logs centralisée optimisée"""
        directories = [
            # Logs par catégorie
            self.base_log_dir / LogCategory.AGENT.value,
            self.base_log_dir / LogCategory.TOOL.value,
            self.base_log_dir / LogCategory.SYSTEM.value,
            self.base_log_dir / LogCategory.ERROR.value,
            self.base_log_dir / LogCategory.AUDIT.value,
            self.base_log_dir / LogCategory.PERFORMANCE.value,
            
            # Sous-catégories agents
            self.base_log_dir / LogCategory.AGENT.value / "coordinateur",
            self.base_log_dir / LogCategory.AGENT.value / "analyseur",
            self.base_log_dir / LogCategory.AGENT.value / "evaluateur",
            self.base_log_dir / LogCategory.AGENT.value / "adaptateur",
            self.base_log_dir / LogCategory.AGENT.value / "testeur",
            self.base_log_dir / LogCategory.AGENT.value / "documenteur",
            self.base_log_dir / LogCategory.AGENT.value / "validateur",
            
            # Sous-catégories tools
            self.base_log_dir / LogCategory.TOOL.value / "generate_pitch_document",
            self.base_log_dir / LogCategory.TOOL.value / "tts_performance_monitor",
            self.base_log_dir / LogCategory.TOOL.value / "backup_system",
            self.base_log_dir / LogCategory.TOOL.value / "excel_vba_launcher",
            self.base_log_dir / LogCategory.TOOL.value / "documentation_generator",
            
            # Archives et métriques
            self.base_log_dir / "archives",
            self.base_log_dir / "metrics",
            
            # Configuration
            Path("config")
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _load_or_create_config(self):
        """Charge ou crée la configuration de logging optimisée"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    for name, config in config_data.items():
                        self._configs[name] = LoggingConfig(**config)
                self._internal_logger.info(f"Configuration chargée: {len(self._configs)} configs")
            except Exception as e:
                self._internal_logger.error(f"Erreur chargement config: {e}")
                self._create_default_configs()
        else:
            self._create_default_configs()
            self._save_config()
    
    def _create_default_configs(self):
        """Crée les configurations par défaut optimisées"""
        default_configs = {
            # System
            "template_manager": LoggingConfig(
                logger_name="nextgen.system.template_manager",
                log_dir=f"logs/{LogCategory.SYSTEM.value}",
                filename_pattern="template_manager_{date}.log",
                async_enabled=True
            ),
            "agent_factory": LoggingConfig(
                logger_name="nextgen.system.agent_factory",
                log_dir=f"logs/{LogCategory.SYSTEM.value}",
                filename_pattern="agent_factory_{date}.log",
                async_enabled=True
            ),
            "orchestrator": LoggingConfig(
                logger_name="nextgen.system.orchestrator",
                log_dir=f"logs/{LogCategory.SYSTEM.value}",
                filename_pattern="orchestrator_{date}.log",
                async_enabled=True,
                max_file_size=100 * 1024 * 1024  # 100MB pour orchestrator
            ),
            
            # Agents templates
            "agent_coordinateur": LoggingConfig(
                logger_name="nextgen.agent.coordination.chef_equipe",
                log_dir=f"logs/{LogCategory.AGENT.value}/coordinateur",
                filename_pattern="coordinateur_{agent_id}_{date}.log"
            ),
            "agent_analyseur": LoggingConfig(
                logger_name="nextgen.agent.analysis.structure",
                log_dir=f"logs/{LogCategory.AGENT.value}/analyseur",
                filename_pattern="analyseur_{agent_id}_{date}.log"
            ),
            
            # Tools
            "tool_pitch_generator": LoggingConfig(
                logger_name="nextgen.tool.generate_pitch_document",
                log_dir=f"logs/{LogCategory.TOOL.value}/generate_pitch_document",
                filename_pattern="pitch_generator_{date}.log",
                async_enabled=True
            ),
            
            # Errors & Audit
            "errors_critical": LoggingConfig(
                logger_name="nextgen.errors.critical",
                log_dir=f"logs/{LogCategory.ERROR.value}",
                filename_pattern="critical_errors_{date}.log",
                log_level="ERROR",
                retention_days=90  # Conservation plus longue pour erreurs
            ),
            "audit_trail": LoggingConfig(
                logger_name="nextgen.audit.trail",
                log_dir=f"logs/{LogCategory.AUDIT.value}",
                filename_pattern="audit_{date}.log",
                retention_days=365,  # Conservation 1 an pour audit
                compression_enabled=True
            ),
            
            # Performance
            "performance_metrics": LoggingConfig(
                logger_name="nextgen.performance.metrics",
                log_dir=f"logs/{LogCategory.PERFORMANCE.value}",
                filename_pattern="perf_metrics_{date}.log",
                async_enabled=True,
                format_string="%(asctime)s - %(message)s"  # Format simplifié pour métriques
            )
        }
        
        self._configs.update(default_configs)
    
    def _save_config(self):
        """Sauvegarde la configuration avec gestion d'erreur"""
        try:
            config_data = {name: asdict(config) for name, config in self._configs.items()}
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Sauvegarde atomique
            temp_file = self.config_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False, default=str)
            
            temp_file.replace(self.config_file)
            self._internal_logger.info("Configuration sauvegardée avec succès")
            
        except Exception as e:
            self._internal_logger.error(f"Erreur sauvegarde config: {e}")
            self._metrics.errors_count += 1
            self._metrics.last_error = str(e)
    
    def generate_agent_logging_config(
        self, 
        agent_name: str, 
        role: str, 
        domain: str, 
        agent_id: str = None,
        async_enabled: bool = False
    ) -> Dict[str, Any]:
        """Génère une configuration de logging optimisée pour un agent"""
        agent_id = agent_id or f"{role}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        config = {
            "logger_name": f"nextgen.agent.{domain}.{role}.{agent_name}",
            "log_level": "INFO",
            "log_dir": f"logs/{LogCategory.AGENT.value}/{role}",
            "filename_pattern": f"{role}_{agent_id}_{{date}}.log",
            "max_file_size": MAX_LOG_SIZE,
            "backup_count": 10,
            "console_enabled": True,
            "file_enabled": True,
            "format_string": ASYNC_FORMAT if async_enabled else DEFAULT_FORMAT,
            "async_enabled": async_enabled,
            "compression_enabled": True,
            "retention_days": 30,
            "metadata": {
                "agent_id": agent_id,
                "agent_name": agent_name,
                "role": role,
                "domain": domain,
                "created_at": datetime.now().isoformat(),
                "nextgen_version": "1.0.0"
            }
        }
        
        return config
    
    @lru_cache(maxsize=128)
    def _get_cached_formatter(self, format_string: str) -> logging.Formatter:
        """Cache les formatters pour performance"""
        return logging.Formatter(format_string)
    
    def get_logger(
        self, 
        config_name: Optional[str] = None, 
        custom_config: Optional[Dict[str, Any]] = None
    ) -> logging.Logger:
        """Obtient un logger configuré avec optimisations"""
        
        if custom_config:
            config = LoggingConfig(**custom_config)
            logger_name = config.logger_name
        else:
            if not config_name or config_name not in self._configs:
                raise ValueError(f"Configuration '{config_name}' non trouvée")
            config = self._configs[config_name]
            logger_name = config.logger_name
        
        # Retourner logger existant si déjà créé
        if logger_name in self._loggers:
            self._metrics.total_logs += 1
            return self._loggers[logger_name]
        
        # Créer le logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, config.log_level))
        logger.handlers.clear()
        logger.propagate = False  # Éviter la propagation
        
        # Handler fichier avec compression
        if config.file_enabled:
            log_dir = Path(config.log_dir)
            log_dir.mkdir(parents=True, exist_ok=True)
            
            current_date = datetime.now().strftime('%Y%m%d')
            filename = config.filename_pattern.format(
                component=config_name or "custom",
                date=current_date,
                **config.metadata
            )
            
            log_file = log_dir / filename
            
            file_handler = CompressingRotatingFileHandler(
                log_file,
                maxBytes=config.max_file_size,
                backupCount=config.backup_count,
                encoding='utf-8',
                compression_enabled=config.compression_enabled
            )
            
            formatter = self._get_cached_formatter(config.format_string)
            file_handler.setFormatter(formatter)
            
            # NOUVEAU CHATGPT: Chiffrement si activé
            if config.encryption_enabled and config.encryption_key:
                file_handler = EncryptionHandler(file_handler, config.encryption_key)
                self._metrics.encrypted_logs += 1
            
            # Wrapper asynchrone si activé avec optimisations ChatGPT
            if config.async_enabled:
                async_handler = AsyncLogHandler(
                    file_handler, 
                    batch_size=100, 
                    flush_interval=1.0
                )
                self._async_handlers.append(async_handler)
                logger.addHandler(async_handler)
            else:
                logger.addHandler(file_handler)
        
        # NOUVEAU CHATGPT: Handler Elasticsearch
        if config.elasticsearch_enabled:
            es_handler = ElasticsearchHandler(
                config.elasticsearch_host,
                config.elasticsearch_index
            )
            logger.addHandler(es_handler)
        
        # NOUVEAU CHATGPT: Handler Alerting
        if config.alerting_enabled:
            alert_handler = AlertingHandler(
                config.alert_email,
                config.alert_webhook
            )
            alert_handler.setLevel(logging.ERROR)  # Seulement pour erreurs+
            logger.addHandler(alert_handler)
        
        # PHASE 2: Handler Monitoring Avancé
        advanced_monitoring_enabled = custom_config.get("advanced_monitoring_enabled", True) if custom_config else True
        if advanced_monitoring_enabled:
            monitoring_handler = AdvancedMonitoringHandler(
                service_name=f"nextgen-{config.logger_name}",
                enable_tracing=TRACING_ENABLED and OPENTELEMETRY_AVAILABLE
            )
            monitoring_handler.setLevel(logging.INFO)  # Monitoring pour INFO+
            logger.addHandler(monitoring_handler)
            
            # Stocker la référence pour accès aux métriques
            if not hasattr(self, '_monitoring_handlers'):
                self._monitoring_handlers = []
            self._monitoring_handlers.append(monitoring_handler)
        
        # Handler console
        if config.console_enabled:
            console_handler = logging.StreamHandler()
            console_formatter = self._get_cached_formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(console_formatter)
            
            # Filtre pour éviter la duplication en console
            console_handler.addFilter(lambda record: record.levelno >= logging.WARNING)
            
            logger.addHandler(console_handler)
        
        # Ajouter un filtre pour les métriques enrichi ChatGPT
        logger.addFilter(self._metrics_filter)
        
        self._loggers[logger_name] = logger
        self._internal_logger.debug(f"Logger créé: {logger_name}")
        
        return logger
    
    def _metrics_filter(self, record: logging.LogRecord) -> bool:
        """Filtre pour collecter les métriques"""
        try:
            # Incrémenter les compteurs
            self._metrics.total_logs += 1
            self._metrics.logs_per_level[record.levelname] = \
                self._metrics.logs_per_level.get(record.levelname, 0) + 1
            
            # Catégoriser par type
            if "agent" in record.name:
                self._metrics.logs_per_category[LogCategory.AGENT.value] += 1
            elif "tool" in record.name:
                self._metrics.logs_per_category[LogCategory.TOOL.value] += 1
            elif "system" in record.name:
                self._metrics.logs_per_category[LogCategory.SYSTEM.value] += 1
            elif record.levelno >= logging.ERROR:
                self._metrics.logs_per_category[LogCategory.ERROR.value] += 1
                
        except Exception:
            pass  # Ne pas interrompre le logging
        
        return True
    
    def get_agent_logger(
        self, 
        agent_name: str, 
        role: str, 
        domain: str, 
        agent_id: str = None,
        async_enabled: bool = False
    ) -> logging.Logger:
        """Obtient un logger pour un agent avec configuration automatique optimisée"""
        config = self.generate_agent_logging_config(
            agent_name, role, domain, agent_id, async_enabled
        )
        return self.get_logger(None, config)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques du système de logging enrichies ChatGPT"""
        # Collecte des stats async handlers en temps réel
        async_stats = {}
        for i, handler in enumerate(self._async_handlers):
            if hasattr(handler, 'get_stats'):
                async_stats[f"async_handler_{i}"] = handler.get_stats()
        
        metrics = {
            "core_metrics": {
                "total_logs": self._metrics.total_logs,
                "logs_per_level": dict(self._metrics.logs_per_level),
                "logs_per_category": dict(self._metrics.logs_per_category),
                "average_log_size": self._metrics.average_log_size,
                "compression_ratio": self._metrics.compression_ratio,
                "errors_count": self._metrics.errors_count,
                "last_error": self._metrics.last_error,
                "active_loggers": len(self._loggers),
                "async_handlers": len(self._async_handlers),
                "performance_stats": dict(self._metrics.performance_stats)
            },
            
            # NOUVELLES MÉTRIQUES CHATGPT
            "chatgpt_features": {
                "elasticsearch": {
                    "docs_sent": self._metrics.elasticsearch_docs_sent,
                    "errors": self._metrics.elasticsearch_errors,
                    "enabled_loggers": sum(1 for config in self._configs.values() 
                                         if config.elasticsearch_enabled)
                },
                "encryption": {
                    "encrypted_logs": self._metrics.encrypted_logs,
                    "enabled_loggers": sum(1 for config in self._configs.values() 
                                         if config.encryption_enabled)
                },
                "alerting": {
                    "alerts_sent": self._metrics.alerts_sent,
                    "enabled_loggers": sum(1 for config in self._configs.values() 
                                         if config.alerting_enabled)
                },
                "compression": {
                    "savings_bytes": self._metrics.compression_savings_bytes,
                    "ratio_percent": f"{self._metrics.compression_ratio:.2f}%"
                },
                "async_performance": async_stats
            },
            
            # Métriques système
            "system_health": {
                "memory_usage_mb": self._get_memory_usage(),
                "uptime_seconds": (datetime.now() - self._startup_time).total_seconds() if hasattr(self, '_startup_time') else 0,
                "configs_loaded": len(self._configs),
                "handlers_active": sum(len(logger.handlers) for logger in self._loggers.values())
            },
            
            "timestamp": datetime.now().isoformat()
        }
        
        # Sauvegarder les métriques enrichies
        self._save_metrics(metrics)
        
        return metrics
    
    def _save_metrics(self, metrics: Dict[str, Any]):
        """Sauvegarde les métriques dans un fichier"""
        try:
            metrics_file = self.base_log_dir / "metrics" / f"metrics_{datetime.now().strftime('%Y%m%d')}.json"
            metrics_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Charger métriques existantes si présentes
            existing_metrics = []
            if metrics_file.exists():
                try:
                    with open(metrics_file, 'r', encoding='utf-8') as f:
                        existing_metrics = json.load(f)
                except Exception:
                    existing_metrics = []
            
            # Ajouter nouvelles métriques
            existing_metrics.append(metrics)
            
            # Garder seulement les 1000 dernières entrées
            if len(existing_metrics) > 1000:
                existing_metrics = existing_metrics[-1000:]
            
            # Sauvegarder
            with open(metrics_file, 'w', encoding='utf-8') as f:
                json.dump(existing_metrics, f, indent=2, default=str)
                
        except Exception as e:
            self._internal_logger.error(f"Erreur sauvegarde métriques: {e}")
    
    def _start_maintenance_thread(self):
        """Démarre le thread de maintenance pour nettoyage et archivage"""
        def maintenance_worker():
            while True:
                try:
                    # Nettoyage tous les jours à 2h du matin
                    now = datetime.now()
                    next_run = now.replace(hour=2, minute=0, second=0, microsecond=0)
                    if next_run <= now:
                        next_run += timedelta(days=1)
                    
                    sleep_seconds = (next_run - now).total_seconds()
                    threading.Event().wait(sleep_seconds)
                    
                    # Exécuter maintenance
                    self._executor.submit(self._perform_maintenance)
                    
                except Exception as e:
                    self._internal_logger.error(f"Erreur maintenance: {e}")
        
        maintenance_thread = threading.Thread(
            target=maintenance_worker,
            daemon=True,
            name="LogMaintenanceThread"
        )
        maintenance_thread.start()
    
    def _perform_maintenance(self):
        """Effectue la maintenance des logs"""
        try:
            self._internal_logger.info("Début maintenance des logs")
            
            # Nettoyer les vieux logs
            self._cleanup_old_logs()
            
            # Compresser les logs volumineux
            self._compress_large_logs()
            
            # Archiver si nécessaire
            self._archive_logs()
            
            # Calculer les statistiques
            self._calculate_statistics()
            
            self._internal_logger.info("Maintenance des logs terminée")
            
        except Exception as e:
            self._internal_logger.error(f"Erreur durant maintenance: {e}")
            self._metrics.errors_count += 1
    
    def _cleanup_old_logs(self):
        """Nettoie les logs dépassant la durée de rétention"""
        for config in self._configs.values():
            if config.retention_days <= 0:
                continue
                
            log_dir = Path(config.log_dir)
            if not log_dir.exists():
                continue
            
            cutoff_date = datetime.now() - timedelta(days=config.retention_days)
            
            for log_file in log_dir.glob("*.log*"):
                try:
                    if log_file.stat().st_mtime < cutoff_date.timestamp():
                        if log_file.suffix == '.gz':
                            # Archiver avant suppression
                            archive_dir = self.base_log_dir / "archives" / cutoff_date.strftime('%Y%m')
                            archive_dir.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(log_file), str(archive_dir / log_file.name))
                        else:
                            log_file.unlink()
                        
                        self._internal_logger.debug(f"Log nettoyé: {log_file}")
                        
                except Exception as e:
                    self._internal_logger.error(f"Erreur nettoyage {log_file}: {e}")
    
    def _compress_large_logs(self):
        """Compresse les logs volumineux"""
        for log_dir in self.base_log_dir.rglob("*"):
            if not log_dir.is_dir():
                continue
                
            for log_file in log_dir.glob("*.log"):
                try:
                    if log_file.stat().st_size > COMPRESSION_THRESHOLD:
                        # Compresser le fichier
                        with open(log_file, 'rb') as f_in:
                            with gzip.open(f"{log_file}.gz", 'wb', compresslevel=9) as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        
                        # Calculer le ratio de compression
                        original_size = log_file.stat().st_size
                        compressed_size = Path(f"{log_file}.gz").stat().st_size
                        self._metrics.compression_ratio = compressed_size / original_size
                        
                        # Supprimer l'original
                        log_file.unlink()
                        
                        self._internal_logger.info(
                            f"Log compressé: {log_file.name} "
                            f"({original_size/1024/1024:.1f}MB -> {compressed_size/1024/1024:.1f}MB)"
                        )
                        
                except Exception as e:
                    self._internal_logger.error(f"Erreur compression {log_file}: {e}")
    
    def _archive_logs(self):
        """Archive les logs selon la politique définie"""
        archive_date = datetime.now() - timedelta(days=7)  # Archive après 7 jours
        
        for log_dir in self.base_log_dir.rglob("*"):
            if not log_dir.is_dir() or log_dir.name == "archives":
                continue
            
            for log_file in log_dir.glob("*.gz"):
                try:
                    if log_file.stat().st_mtime < archive_date.timestamp():
                        # Déterminer le répertoire d'archive
                        file_date = datetime.fromtimestamp(log_file.stat().st_mtime)
                        archive_dir = self.base_log_dir / "archives" / file_date.strftime('%Y%m')
                        archive_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Préserver la structure
                        relative_path = log_file.relative_to(self.base_log_dir)
                        target_path = archive_dir / relative_path.parent.name
                        target_path.mkdir(parents=True, exist_ok=True)
                        
                        shutil.move(str(log_file), str(target_path / log_file.name))
                        
                except Exception as e:
                    self._internal_logger.error(f"Erreur archivage {log_file}: {e}")
    
    def _calculate_statistics(self):
        """Calcule les statistiques d'utilisation des logs"""
        try:
            total_size = 0
            file_count = 0
            
            for log_file in self.base_log_dir.rglob("*"):
                if log_file.is_file():
                    total_size += log_file.stat().st_size
                    file_count += 1
            
            if file_count > 0:
                self._metrics.average_log_size = total_size / file_count
            
            # Statistiques de performance
            self._metrics.performance_stats = {
                "total_disk_usage_mb": total_size / 1024 / 1024,
                "total_files": file_count,
                "average_file_size_kb": self._metrics.average_log_size / 1024
            }
            
        except Exception as e:
            self._internal_logger.error(f"Erreur calcul statistiques: {e}")
    
    def _setup_shutdown_hooks(self):
        """Configure les hooks pour un arrêt propre"""
        def shutdown_handler(*args):
            self._internal_logger.info("Arrêt du LoggingManager...")
            self.shutdown()
        
        # Enregistrer les handlers
        atexit.register(shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)
        signal.signal(signal.SIGINT, shutdown_handler)
    
    def _get_memory_usage(self) -> float:
        """Obtient l'usage mémoire approximatif en MB - Nouvelle méthode ChatGPT"""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024  # MB
        except ImportError:
            # Fallback basique si psutil non disponible
            return 0.0
    
    def shutdown(self):
        """Arrêt propre du LoggingManager"""
        try:
            # Fermer tous les handlers asynchrones
            for handler in self._async_handlers:
                handler.close()
            
            # Fermer tous les loggers
            for logger in self._loggers.values():
                for handler in logger.handlers[:]:
                    handler.close()
                    logger.removeHandler(handler)
            
            # Arrêter l'executor
            self._executor.shutdown(wait=True, cancel_futures=True)
            
            # Sauvegarder les métriques finales
            self.get_metrics()
            
            self._internal_logger.info("LoggingManager arrêté proprement")
            
        except Exception as e:
            print(f"Erreur lors de l'arrêt du LoggingManager: {e}", file=sys.stderr)
    
    @contextmanager
    def log_performance(self, operation_name: str, logger: logging.Logger = None):
        """Context manager pour mesurer la performance d'une opération"""
        if logger is None:
            logger = self._internal_logger
            
        start_time = datetime.now()
        logger.info(f"Début opération: {operation_name}")
        
        try:
            yield
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Fin opération: {operation_name} (durée: {duration:.3f}s)")
            
            # Ajouter aux métriques de performance
            if operation_name not in self._metrics.performance_stats:
                self._metrics.performance_stats[operation_name] = []
            self._metrics.performance_stats[operation_name].append(duration)
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(
                f"Erreur opération: {operation_name} (durée: {duration:.3f}s) - {e}",
                exc_info=True
            )
            raise
    
    def create_audit_logger(self, user_id: str, action_type: str) -> logging.Logger:
        """Crée un logger spécialisé pour l'audit trail"""
        config = {
            "logger_name": f"nextgen.audit.{action_type}",
            "log_level": "INFO",
            "log_dir": f"logs/{LogCategory.AUDIT.value}",
            "filename_pattern": f"audit_{action_type}_{{date}}.log",
            "retention_days": 365,
            "format_string": "%(asctime)s - USER:%(user_id)s - ACTION:%(action_type)s - %(message)s",
            "metadata": {
                "user_id": user_id,
                "action_type": action_type
            }
        }
        
        logger = self.get_logger(None, config)
        
        # Ajouter un adaptateur pour inclure automatiquement user_id et action_type
        class AuditAdapter(logging.LoggerAdapter):
            def process(self, msg, kwargs):
                extra = kwargs.get('extra', {})
                extra.update({
                    'user_id': user_id,
                    'action_type': action_type
                })
                kwargs['extra'] = extra
                return msg, kwargs
        
        return AuditAdapter(logger, {})
    
    def get_performance_logger(self) -> logging.Logger:
        """Obtient le logger de performance"""
        return self.get_logger("performance_metrics")

    def get_advanced_monitoring_metrics(self) -> Dict[str, Any]:
        """Récupère les métriques de monitoring avancé - PHASE 2"""
        if not hasattr(self, '_monitoring_handlers'):
            return {
                "advanced_monitoring": False,
                "message": "Monitoring avancé non activé"
            }
        
        all_metrics = []
        for handler in self._monitoring_handlers:
            try:
                handler_metrics = handler.get_metrics_summary()
                all_metrics.append(handler_metrics)
            except Exception as e:
                all_metrics.append({
                    "error": f"Erreur récupération métriques: {e}",
                    "handler": str(handler)
                })
        
        # Agrégation des métriques
        aggregated = {
            "advanced_monitoring": True,
            "opentelemetry_available": OPENTELEMETRY_AVAILABLE,
            "tracing_enabled": TRACING_ENABLED,
            "total_monitoring_handlers": len(self._monitoring_handlers),
            "handlers_metrics": all_metrics
        }
        
        # Métriques agrégées si disponibles
        if all_metrics and all_metrics[0].get("monitoring_type") == "fallback":
            total_logs = sum(m.get("logs_total", 0) for m in all_metrics if "logs_total" in m)
            total_errors = sum(m.get("errors_total", 0) for m in all_metrics if "errors_total" in m)
            avg_times = [m.get("avg_processing_time_ms", 0) for m in all_metrics if "avg_processing_time_ms" in m]
            
            aggregated.update({
                "aggregated_metrics": {
                    "total_logs_monitored": total_logs,
                    "total_errors_monitored": total_errors,
                    "avg_processing_time_ms": sum(avg_times) / len(avg_times) if avg_times else 0,
                    "performance_alerts_total": sum(m.get("performance_alerts", 0) for m in all_metrics if "performance_alerts" in m)
                }
            })
        
        return aggregated

# Instance globale singleton
logging_manager = LoggingManager()

# Fonctions utilitaires pour faciliter l'usage
def get_logger(name: str) -> logging.Logger:
    """Raccourci pour obtenir un logger système"""
    return logging_manager.get_logger(name)

def get_agent_logger(agent_name: str, role: str, domain: str, agent_id: str = None) -> logging.Logger:
    """Raccourci pour obtenir un logger d'agent"""
    return logging_manager.get_agent_logger(agent_name, role, domain, agent_id)

def log_performance(operation_name: str, logger: logging.Logger = None):
    """Décorateur/context manager pour mesurer la performance"""
    return logging_manager.log_performance(operation_name, logger)

# Export des classes et fonctions principales
__all__ = [
    'LoggingManager',
    'LoggingConfig',
    'LogLevel',
    'LogCategory',
    'logging_manager',
    'get_logger',
    'get_agent_logger',
    'log_performance'
]
                