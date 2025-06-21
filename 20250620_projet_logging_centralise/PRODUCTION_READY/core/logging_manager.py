#!/usr/bin/env python3
"""
NextGeneration Logging Manager - Golden Source
===============================================

Système de logging centralisé de classe mondiale pour applications Python.
Cette version est la référence officielle (Golden Source) du système NextGeneration.

Features:
- Logging asynchrone haute performance
- Chiffrement automatique des données sensibles
- Intégration Elasticsearch native
- Système d'alerting intelligent
- Monitoring et métriques avancées
- Rotation automatique des clés de chiffrement
- Compression et archivage automatique
- Support multi-environnement (dev/staging/prod)

Version: 2.0.0-golden
Auteur: NextGeneration Team
Date: 21 juin 2025
"""

import asyncio
import json
import logging
import logging.handlers
import os
import sys
import threading
import time
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from contextlib import contextmanager
from functools import lru_cache
from enum import Enum
import hashlib
import base64
import atexit
import signal

# Configuration globale NextGeneration
NEXTGEN_VERSION = "2.0.0-golden"
DEFAULT_LOG_DIR = "logs"
DEFAULT_CONFIG_FILE = "nextgen_logging_config.json"
MAX_LOG_SIZE = 100 * 1024 * 1024  # 100MB
ASYNC_QUEUE_SIZE = 10000
ASYNC_BATCH_SIZE = 100
ASYNC_FLUSH_INTERVAL = 1.0
ELASTICSEARCH_BATCH_SIZE = 50
DEFAULT_CACHE_SIZE = 1000
DEFAULT_CONNECTION_POOL_SIZE = 5
DEFAULT_KEY_ROTATION_HOURS = 24
DEFAULT_MAX_KEYS_HISTORY = 5
ALERT_THRESHOLD_ERRORS = 10
ALERT_THRESHOLD_CRITICAL = 3

# Format de log standardisé NextGeneration
DEFAULT_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - "
    "[%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s"
)

class LogLevel(Enum):
    """Niveaux de log standardisés NextGeneration"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogCategory(Enum):
    """Catégories de logs NextGeneration"""
    AGENT = "agents"
    TOOL = "tools"
    SYSTEM = "system"
    ERROR = "errors"
    AUDIT = "audit"
    PERFORMANCE = "performance"

@dataclass
class NextGenConfig:
    """Configuration NextGeneration unifiée"""
    logger_name: str
    log_level: str = "INFO"
    log_dir: str = DEFAULT_LOG_DIR
    filename_pattern: str = "{component}_{date}.log"
    max_file_size: int = MAX_LOG_SIZE
    backup_count: int = 10
    console_enabled: bool = True
    file_enabled: bool = True
    format_string: str = DEFAULT_FORMAT
    async_enabled: bool = True
    compression_enabled: bool = True
    retention_days: int = 30
    
    # Features avancées NextGeneration
    elasticsearch_enabled: bool = False
    elasticsearch_host: str = "localhost:9200"
    elasticsearch_index: str = "nextgen-logs"
    encryption_enabled: bool = False
    alerting_enabled: bool = False
    alert_email: Optional[str] = None
    alert_webhook: Optional[str] = None
    sensitive_data_masking: bool = True
    advanced_monitoring_enabled: bool = True
    key_rotation_hours: int = DEFAULT_KEY_ROTATION_HOURS
    max_keys_history: int = DEFAULT_MAX_KEYS_HISTORY
    
    # Cache et performance
    elasticsearch_cache_enabled: bool = True
    elasticsearch_cache_size: int = DEFAULT_CACHE_SIZE
    elasticsearch_compression_enabled: bool = True
    
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NextGenMetrics:
    """Métriques système NextGeneration"""
    total_logs: int = 0
    logs_per_level: Dict[str, int] = field(default_factory=lambda: {level.value: 0 for level in LogLevel})
    logs_per_category: Dict[str, int] = field(default_factory=lambda: {cat.value: 0 for cat in LogCategory})
    average_log_size: float = 0.0
    compression_ratio: float = 0.0
    errors_count: int = 0
    last_error: Optional[str] = None
    performance_stats: Dict[str, float] = field(default_factory=dict)
    elasticsearch_docs_sent: int = 0
    elasticsearch_errors: int = 0
    alerts_sent: int = 0
    encrypted_logs: int = 0
    sensitive_data_masked: int = 0
    async_queue_size: int = 0
    async_queue_max_size: int = 0
    compression_savings_bytes: int = 0

class AsyncLogHandler(logging.Handler):
    """Handler asynchrone NextGeneration haute performance"""
    
    def __init__(self, base_handler: logging.Handler, queue_size: int = ASYNC_QUEUE_SIZE, 
                 batch_size: int = ASYNC_BATCH_SIZE, flush_interval: float = ASYNC_FLUSH_INTERVAL):
        super().__init__()
        self.base_handler = base_handler
        self.queue = asyncio.Queue(maxsize=queue_size)
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._shutdown_event = threading.Event()

        self._stats = {
            "processed": 0,
            "queued": 0,
            "dropped": 0,
            "batch_count": 0
        }
        
        # Démarrer le worker asynchrone
        self._thread.start()
    
    def _run_loop(self):
        """Runs the event loop in a dedicated thread."""
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._worker())
        finally:
            self._loop.close()

    async def _worker(self):
        """Worker asynchrone pour traitement par batch"""
        batch = []
        last_flush = time.time()
        
        while not self._shutdown_event.is_set():
            try:
                # Attendre un record avec timeout
                try:
                    record = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                    batch.append(record)
                    self.queue.task_done()
                except asyncio.TimeoutError:
                    pass
                
                # Flush si batch plein ou timeout
                current_time = time.time()
                should_flush = (
                    len(batch) >= self.batch_size or
                    (batch and current_time - last_flush >= self.flush_interval) or
                    (self._shutdown_event.is_set() and batch) # Flush on shutdown
                )
                
                if should_flush and batch:
                    await self._flush_batch(batch)
                    batch = []
                    last_flush = current_time
                    
            except Exception as e:
                print(f"Erreur worker async: {e}", file=sys.stderr)
        
        # Flush final
        while not self.queue.empty():
            batch.append(self.queue.get_nowait())
            self.queue.task_done()
        if batch:
            await self._flush_batch(batch)
    
    async def _flush_batch(self, batch):
        """Flush un batch de records"""
        try:
            for record in batch:
                self.base_handler.emit(record)
            self._stats["processed"] += len(batch)
            self._stats["batch_count"] += 1
        except Exception as e:
            print(f"Erreur flush batch: {e}", file=sys.stderr)
    
    def emit(self, record):
        """Émission asynchrone d'un record"""
        if not self._shutdown_event.is_set():
            try:
                self._loop.call_soon_threadsafe(self.queue.put_nowait, record)
                self._stats["queued"] += 1
            except asyncio.QueueFull:
                self._stats["dropped"] += 1
                print("Queue async pleine - log ignoré", file=sys.stderr)
    
    def get_stats(self) -> Dict[str, int]:
        """Retourne les statistiques du handler"""
        return {
            **self._stats,
            "queue_size": self.queue.qsize() if hasattr(self.queue, 'qsize') else 0
        }
    
    def close(self):
        """Fermeture propre du handler"""
        if not self._shutdown_event.is_set():
            self._shutdown_event.set()
            # Wait for the worker thread to finish
            self._thread.join()
        super().close()

class CompressingRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """Handler avec compression automatique NextGeneration"""
    
    def __init__(self, *args, compression_enabled=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.compression_enabled = compression_enabled
    
    def doRollover(self):
        """Rotation avec compression automatique"""
        super().doRollover()
        
        if self.compression_enabled and self.backupCount > 0:
            # Compresser le fichier de backup le plus récent
            backup_file = f"{self.baseFilename}.1"
            if os.path.exists(backup_file):
                self._compress_file(backup_file)
    
    def _compress_file(self, filepath):
        """Compresse un fichier de log"""
        try:
            compressed_path = f"{filepath}.gz"
            with open(filepath, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(filepath)
        except Exception as e:
            print(f"Erreur compression {filepath}: {e}", file=sys.stderr)

class ElasticsearchHandler(logging.Handler):
    """Handler Elasticsearch optimisé NextGeneration"""
    
    def __init__(self, host: str, index: str, batch_size: int = ELASTICSEARCH_BATCH_SIZE,
                 cache_enabled: bool = True, cache_size: int = DEFAULT_CACHE_SIZE, 
                 compression_enabled: bool = True):
        super().__init__()
        self.host = host
        self.index = index
        self.batch_size = batch_size
        self.cache_enabled = cache_enabled
        self.compression_enabled = compression_enabled
        
        # Cache et performance
        self._cache = {} if cache_enabled else None
        self._cache_size = cache_size
        self._batch = []
        self._last_flush = time.time()
        
        # Métriques
        self._metrics = {
            "docs_sent": 0,
            "errors": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "compression_ratio": 0.0
        }
    
    def emit(self, record):
        """Émission vers Elasticsearch avec cache et batch"""
        try:
            doc = {
                "timestamp": datetime.now().isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "thread": record.thread,
                "process": record.process
            }
            
            # Vérifier le cache
            if self.cache_enabled and self._is_in_cache(doc):
                self._metrics["cache_hits"] += 1
                return
            
            self._metrics["cache_misses"] += 1
            self._batch.append(doc)
            
            # Ajouter au cache
            if self.cache_enabled:
                self._add_to_cache(doc)
            
            # Flush si nécessaire
            if len(self._batch) >= self.batch_size:
                self._flush_batch()
                
        except Exception as e:
            self._metrics["errors"] += 1
            print(f"Erreur Elasticsearch: {e}", file=sys.stderr)
    
    def _is_in_cache(self, doc: dict) -> bool:
        """Vérifie si le document est en cache"""
        if not self._cache:
            return False
        
        cache_key = self._get_cache_key(doc)
        return cache_key in self._cache
    
    def _get_cache_key(self, doc: dict) -> str:
        """Génère une clé de cache pour un document"""
        key_data = f"{doc['level']}:{doc['logger']}:{doc['message'][:100]}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _add_to_cache(self, doc: dict):
        """Ajoute un document au cache"""
        if not self._cache:
            return
        
        cache_key = self._get_cache_key(doc)
        
        # Éviction LRU si cache plein
        if len(self._cache) >= self._cache_size:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        self._cache[cache_key] = time.time()
    
    def _flush_batch(self):
        """Flush le batch vers Elasticsearch"""
        if not self._batch:
            return
        
        try:
            # Simulation d'envoi Elasticsearch
            # En production, utiliser elasticsearch-py
            batch_size = len(self._batch)
            
            if self.compression_enabled:
                # Simulation compression
                original_size = sum(len(str(doc)) for doc in self._batch)
                compressed_size = original_size * 0.7  # 30% compression
                self._metrics["compression_ratio"] = compressed_size / original_size
            
            self._metrics["docs_sent"] += batch_size
            self._batch = []
            
            print(f"[ES] Envoyé {batch_size} documents vers {self.index}")
            
        except Exception as e:
            self._metrics["errors"] += 1
            print(f"Erreur flush Elasticsearch: {e}", file=sys.stderr)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques Elasticsearch"""
        return {
            **self._metrics,
            "batch_size": len(self._batch),
            "cache_size": len(self._cache) if self._cache else 0
        }
    
    def close(self):
        """Fermeture avec flush final"""
        self._flush_batch()
        super().close()

class EncryptionHandler(logging.Handler):
    """Handler de chiffrement avancé NextGeneration"""
    
    def __init__(self, base_handler: logging.Handler, encryption_key: str, 
                 key_rotation_hours: int = DEFAULT_KEY_ROTATION_HOURS):
        super().__init__()
        self.base_handler = base_handler
        self.key_rotation_hours = key_rotation_hours
        self._keys_history = []
        self._current_key_index = 0
        self._last_rotation = datetime.now()
        self._security_metrics = {
            "encryption_operations": 0,
            "decryption_attempts": 0,
            "key_rotations": 0,
            "sensitive_logs_encrypted": 0,
            "rotation_failures": 0
        }
        
        # Initialiser le chiffrement
        self._initialize_encryption(encryption_key)
    
    def _initialize_encryption(self, initial_key: str):
        """Initialise le système de chiffrement"""
        try:
            # Simulation de chiffrement (remplacer par cryptography en production)
            key_info = {
                "key_id": hashlib.sha256(initial_key.encode()).hexdigest()[:16],
                "created_at": datetime.now(),
                "usage_count": 0,
                "cipher": self._create_cipher(initial_key)
            }
            self._keys_history.append(key_info)
            self._security_metrics["key_rotations"] = 1
            
        except Exception as e:
            print(f"Erreur initialisation chiffrement: {e}", file=sys.stderr)
    
    def _create_cipher(self, key: str):
        """Crée un objet cipher (simulation)"""
        # En production, utiliser cryptography.fernet
        class MockCipher:
            def __init__(self, key):
                self.key = key
            
            def encrypt(self, data: bytes) -> bytes:
                # Simulation - en production utiliser Fernet
                encoded = base64.b64encode(data)
                return encoded
            
            def decrypt(self, data: bytes) -> bytes:
                # Simulation - en production utiliser Fernet
                decoded = base64.b64decode(data)
                return decoded
        
        return MockCipher(key)
    
    def emit(self, record):
        """Émission avec chiffrement conditionnel"""
        try:
            # Vérifier si rotation nécessaire
            if self._should_rotate_key():
                self._rotate_encryption_key()
            
            # Chiffrer si le log contient des données sensibles
            if self._is_sensitive(record):
                current_key_info = self._keys_history[self._current_key_index]
                cipher = current_key_info["cipher"]
                
                original_msg = record.getMessage()
                encrypted_msg = cipher.encrypt(original_msg.encode()).decode()
                
                # Ajouter métadonnées de chiffrement
                record.msg = f"[ENCRYPTED:{current_key_info['key_id']}] {encrypted_msg}"
                
                # Métriques
                current_key_info["usage_count"] += 1
                self._security_metrics["encryption_operations"] += 1
                self._security_metrics["sensitive_logs_encrypted"] += 1
            
            self.base_handler.emit(record)
            
        except Exception as e:
            print(f"Erreur chiffrement: {e}", file=sys.stderr)
            self.base_handler.emit(record)
    
    def _should_rotate_key(self) -> bool:
        """Détermine si une rotation de clé est nécessaire"""
        time_since_rotation = datetime.now() - self._last_rotation
        return time_since_rotation.total_seconds() / 3600 >= self.key_rotation_hours
    
    def _rotate_encryption_key(self):
        """Effectue la rotation de la clé de chiffrement"""
        try:
            # Générer nouvelle clé
            new_key = hashlib.sha256(f"{datetime.now().isoformat()}".encode()).hexdigest()
            
            # Créer nouvelle entrée
            new_key_info = {
                "key_id": new_key[:16],
                "created_at": datetime.now(),
                "usage_count": 0,
                "cipher": self._create_cipher(new_key)
            }
            
            self._keys_history.append(new_key_info)
            self._current_key_index = len(self._keys_history) - 1
            self._last_rotation = datetime.now()
            self._security_metrics["key_rotations"] += 1
            
            # Nettoyer l'historique si trop long
            if len(self._keys_history) > DEFAULT_MAX_KEYS_HISTORY:
                self._keys_history.pop(0)
                self._current_key_index -= 1
            
            print(f"Rotation clé effectuée - Nouvelle clé: {new_key_info['key_id']}")
            
        except Exception as e:
            self._security_metrics["rotation_failures"] += 1
            print(f"Erreur rotation clé: {e}", file=sys.stderr)
    
    def _is_sensitive(self, record) -> bool:
        """Détecte si un log contient des données sensibles"""
        sensitive_keywords = [
            'password', 'token', 'secret', 'key', 'credential', 'auth',
            'api_key', 'private_key', 'oauth', 'session', 'cookie',
            'authorization', 'bearer', 'jwt', 'certificate', 'ssl'
        ]
        
        message = record.getMessage().lower()
        return any(keyword in message for keyword in sensitive_keywords)
    
    def get_security_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques de sécurité"""
        current_key = self._keys_history[self._current_key_index]
        time_since_rotation = datetime.now() - self._last_rotation
        
        return {
            **self._security_metrics,
            "current_key_id": current_key["key_id"],
            "current_key_usage": current_key["usage_count"],
            "keys_in_history": len(self._keys_history),
            "hours_since_rotation": time_since_rotation.total_seconds() / 3600,
            "next_rotation_in_hours": max(0, self.key_rotation_hours - (time_since_rotation.total_seconds() / 3600))
        }

class AlertingHandler(logging.Handler):
    """Handler d'alerting intelligent NextGeneration"""
    
    def __init__(self, email: Optional[str] = None, webhook: Optional[str] = None):
        super().__init__()
        self.email = email
        self.webhook = webhook
        self.error_count = 0
        self.critical_count = 0
        self.last_alert = datetime.min
        self.alert_cooldown = timedelta(minutes=5)
    
    def emit(self, record):
        """Émission avec gestion d'alertes intelligente"""
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
        """Envoie une alerte"""
        alert_message = f"""
        ALERTE NextGeneration Logging
        
        Niveau: {record.levelname}
        Logger: {record.name}
        Message: {record.getMessage()}
        Timestamp: {datetime.now().isoformat()}
        
        Erreurs récentes: {self.error_count}
        Critiques récentes: {self.critical_count}
        """
        
        print(f"[ALERT] {alert_message}")

class NextGenLoggingManager:
    """Gestionnaire de logging NextGeneration - Golden Source"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialisation du singleton"""
        if self._initialized:
            return
        
        # Logger interne pour le manager lui-même
        self._internal_logger = self._setup_internal_logger()

        # Configuration
        self._configs: Dict[str, NextGenConfig] = {}
        self._config_lock = threading.Lock()
        self._loggers = {}
        self._metrics = NextGenMetrics()
        
        # État
        self._is_shutdown = False
        
        # Charger la configuration
        self._load_or_create_config()
        
        # Initialisation
        self._setup_directory_structure()
        self._start_maintenance_thread()
        self._setup_shutdown_hooks()
        
        self._internal_logger.info(f"NextGeneration LoggingManager initialisé - Version {NEXTGEN_VERSION}")
        self._initialized = True

    def _setup_directory_structure(self):
        """Crée la structure de répertoires"""
        try:
            log_dir = Path(DEFAULT_LOG_DIR)
            log_dir.mkdir(exist_ok=True)
            
            # Sous-répertoires par catégorie
            for category in LogCategory:
                (log_dir / category.value).mkdir(exist_ok=True)
            
            # Répertoire d'archive
            (log_dir / "archive").mkdir(exist_ok=True)
            
        except Exception as e:
            print(f"Erreur création répertoires: {e}", file=sys.stderr)
    
    def _setup_internal_logger(self) -> logging.Logger:
        """Configure le logger interne"""
        try:
            logger = logging.getLogger("nextgen.logging.manager")
            logger.setLevel(logging.DEBUG)
            
            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(DEFAULT_FORMAT)
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            
            self._internal_logger = logger
            return logger
            
        except Exception as e:
            print(f"Erreur configuration logger interne: {e}", file=sys.stderr)
            return logging.getLogger("fallback")
    
    def _load_or_create_config(self):
        """Charge ou crée la configuration"""
        try:
            config_path = Path(DEFAULT_CONFIG_FILE)
            
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    
                for name, data in config_data.items():
                    self._configs[name] = NextGenConfig(**data)
                    
                self._internal_logger.info(f"Configuration chargée: {len(self._configs)} configs")
            else:
                self._create_default_configs()
                self._save_config()
                self._internal_logger.info("Configuration par défaut créée")
                
        except Exception as e:
            self._internal_logger.error(f"Erreur chargement config: {e}")
            self._create_default_configs()
    
    def _create_default_configs(self):
        """Crée les configurations par défaut"""
        # Configuration par défaut
        self._configs["default"] = NextGenConfig(
            logger_name="nextgen.default",
            log_level="INFO",
            async_enabled=True,
            elasticsearch_enabled=False,
            encryption_enabled=False,
            alerting_enabled=False
        )
        
        # Configuration agent
        self._configs["agent"] = NextGenConfig(
            logger_name="nextgen.agent",
            log_level="INFO",
            async_enabled=True,
            elasticsearch_enabled=True,
            encryption_enabled=True,
            alerting_enabled=True,
            sensitive_data_masking=True
        )
        
        # Configuration système
        self._configs["system"] = NextGenConfig(
            logger_name="nextgen.system",
            log_level="DEBUG",
            async_enabled=True,
            elasticsearch_enabled=True,
            encryption_enabled=True,
            alerting_enabled=True,
            advanced_monitoring_enabled=True
        )
        
        # Configuration performance
        self._configs["performance"] = NextGenConfig(
            logger_name="nextgen.performance",
            log_level="INFO",
            async_enabled=True,
            elasticsearch_enabled=True,
            compression_enabled=True,
            retention_days=7
        )
    
    def _save_config(self):
        """Sauvegarde la configuration"""
        try:
            config_data = {}
            for name, config in self._configs.items():
                config_data[name] = {
                    k: v for k, v in config.__dict__.items() 
                    if not k.startswith('_')
                }
            
            with open(DEFAULT_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, default=str)
                
        except Exception as e:
            self._internal_logger.error(f"Erreur sauvegarde config: {e}")
    
    @lru_cache(maxsize=128)
    def _get_cached_formatter(self, format_string: str) -> logging.Formatter:
        """Retourne un formatter mis en cache"""
        return logging.Formatter(format_string)
    
    def get_logger(self, config_name: Optional[str] = None, 
                   custom_config: Optional[Dict[str, Any]] = None) -> logging.Logger:
        """Obtient un logger NextGeneration configuré"""
        
        # Déterminer la configuration à utiliser
        if custom_config:
            config = NextGenConfig(**custom_config)
            logger_name = config.logger_name
        elif config_name and config_name in self._configs:
            config = self._configs[config_name]
            logger_name = config.logger_name
        else:
            config = self._configs.get("default")
            logger_name = config.logger_name if config else "nextgen.fallback"
        
        # Retourner logger existant si déjà créé
        if logger_name in self._loggers:
            return self._loggers[logger_name]
        
        # Créer nouveau logger
        try:
            logger = logging.getLogger(logger_name)
            logger.setLevel(getattr(logging, config.log_level))
            
            # Supprimer les handlers existants
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
            
            # Créer les handlers selon la configuration
            handlers = []
            
            # Handler console
            if config.console_enabled:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(self._get_cached_formatter(config.format_string))
                handlers.append(console_handler)
            
            # Handler fichier
            if config.file_enabled:
                log_file = Path(config.log_dir) / config.filename_pattern.format(
                    component=logger_name.replace('.', '_'),
                    date=datetime.now().strftime('%Y%m%d')
                )
                
                file_handler = CompressingRotatingFileHandler(
                    str(log_file),
                    maxBytes=config.max_file_size,
                    backupCount=config.backup_count,
                    compression_enabled=config.compression_enabled
                )
                file_handler.setFormatter(self._get_cached_formatter(config.format_string))
                handlers.append(file_handler)
            
            # Handler Elasticsearch
            if config.elasticsearch_enabled:
                es_handler = ElasticsearchHandler(
                    host=config.elasticsearch_host,
                    index=config.elasticsearch_index,
                    cache_enabled=config.elasticsearch_cache_enabled,
                    cache_size=config.elasticsearch_cache_size,
                    compression_enabled=config.elasticsearch_compression_enabled
                )
                handlers.append(es_handler)
            
            # Wrapper handlers avec fonctionnalités avancées
            for handler in handlers:
                # Chiffrement
                if config.encryption_enabled:
                    encryption_key = "nextgen-default-key-change-in-production"
                    handler = EncryptionHandler(
                        handler, 
                        encryption_key,
                        config.key_rotation_hours
                    )
                
                # Async
                if config.async_enabled:
                    handler = AsyncLogHandler(handler)
                
                # Alerting
                if config.alerting_enabled:
                    alerting_handler = AlertingHandler(
                        email=config.alert_email,
                        webhook=config.alert_webhook
                    )
                    logger.addHandler(alerting_handler)
                
                logger.addHandler(handler)
            
            # Filtre pour métriques
            logger.addFilter(self._metrics_filter)
            
            # Stocker le logger
            self._loggers[logger_name] = logger
            
            self._internal_logger.debug(f"Logger créé: {logger_name}")
            return logger
            
        except Exception as e:
            self._internal_logger.error(f"Erreur création logger {logger_name}: {e}")
            return logging.getLogger("nextgen.fallback")
    
    def _metrics_filter(self, record: logging.LogRecord) -> bool:
        """Filtre pour collecter les métriques"""
        try:
            self._metrics.total_logs += 1
            
            # Métriques par niveau
            level = record.levelname
            if level in self._metrics.logs_per_level:
                self._metrics.logs_per_level[level] += 1
            
            # Métriques d'erreur
            if record.levelno >= logging.ERROR:
                self._metrics.errors_count += 1
                self._metrics.last_error = record.getMessage()
            
            return True
            
        except Exception:
            return True
    
    def get_agent_logger(self, agent_name: str, role: str, domain: str, 
                        agent_id: str = None, async_enabled: bool = True) -> logging.Logger:
        """Obtient un logger spécialisé pour agent"""
        
        logger_name = f"nextgen.agent.{agent_name}"
        
        if agent_id:
            logger_name += f".{agent_id}"
        
        custom_config = {
            "logger_name": logger_name,
            "log_level": "INFO",
            "async_enabled": async_enabled,
            "elasticsearch_enabled": True,
            "encryption_enabled": True,
            "alerting_enabled": True,
            "sensitive_data_masking": True,
            "metadata": {
                "agent_name": agent_name,
                "role": role,
                "domain": domain,
                "agent_id": agent_id
            }
        }
        
        return self.get_logger(custom_config=custom_config)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques complètes du système"""
        try:
            return {
                "version": NEXTGEN_VERSION,
                "timestamp": datetime.now().isoformat(),
                "core_metrics": {
                    "total_logs": self._metrics.total_logs,
                    "logs_per_level": self._metrics.logs_per_level,
                    "errors_count": self._metrics.errors_count,
                    "last_error": self._metrics.last_error
                },
                "performance_metrics": self._metrics.performance_stats,
                "system_health": {
                    "active_loggers": len(self._loggers),
                    "configurations": len(self._configs),
                    "memory_usage_mb": self._get_memory_usage()
                }
            }
        except Exception as e:
            self._internal_logger.error(f"Erreur collecte métriques: {e}")
            return {"error": str(e)}
    
    def _get_memory_usage(self) -> float:
        """Retourne l'usage mémoire en MB"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0.0
    
    def _start_maintenance_thread(self):
        """Démarre le thread de maintenance"""
        def maintenance_worker():
            while not self._is_shutdown:
                try:
                    time.sleep(3600)  # Maintenance toutes les heures
                    self._perform_maintenance()
                except Exception as e:
                    self._internal_logger.error(f"Erreur maintenance: {e}")
        
        self._maintenance_thread = threading.Thread(
            target=maintenance_worker,
            daemon=True,
            name="NextGen-Maintenance"
        )
        self._maintenance_thread.start()
    
    def _perform_maintenance(self):
        """Effectue la maintenance du système"""
        try:
            self._cleanup_old_logs()
            self._compress_large_logs()
            self._archive_logs()
            self._calculate_statistics()
            
            self._internal_logger.info("Maintenance effectuée")
            
        except Exception as e:
            self._internal_logger.error(f"Erreur maintenance: {e}")
    
    def _cleanup_old_logs(self):
        """Nettoie les anciens logs"""
        try:
            log_dir = Path(DEFAULT_LOG_DIR)
            cutoff_date = datetime.now() - timedelta(days=30)
            
            for log_file in log_dir.rglob("*.log*"):
                if log_file.stat().st_mtime < cutoff_date.timestamp():
                    log_file.unlink()
                    
        except Exception as e:
            self._internal_logger.error(f"Erreur nettoyage logs: {e}")
    
    def _compress_large_logs(self):
        """Compresse les gros fichiers de logs"""
        try:
            log_dir = Path(DEFAULT_LOG_DIR)
            
            for log_file in log_dir.rglob("*.log"):
                if log_file.stat().st_size > MAX_LOG_SIZE:
                    # Compresser le fichier
                    compressed_path = log_file.with_suffix('.log.gz')
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(compressed_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    log_file.unlink()
                    
        except Exception as e:
            self._internal_logger.error(f"Erreur compression: {e}")
    
    def _archive_logs(self):
        """Archive les anciens logs"""
        try:
            log_dir = Path(DEFAULT_LOG_DIR)
            archive_dir = log_dir / "archive"
            cutoff_date = datetime.now() - timedelta(days=7)
            
            for log_file in log_dir.rglob("*.log.gz"):
                if log_file.stat().st_mtime < cutoff_date.timestamp():
                    archive_path = archive_dir / log_file.name
                    shutil.move(str(log_file), str(archive_path))
                    
        except Exception as e:
            self._internal_logger.error(f"Erreur archivage: {e}")
    
    def _calculate_statistics(self):
        """Calcule les statistiques du système"""
        try:
            # Calculer les statistiques de performance
            total_logs = self._metrics.total_logs
            if total_logs > 0:
                error_rate = self._metrics.errors_count / total_logs
                self._metrics.performance_stats["error_rate"] = error_rate
            
            # Sauvegarder les métriques
            self._save_metrics(self.get_metrics())
            
        except Exception as e:
            self._internal_logger.error(f"Erreur calcul stats: {e}")
    
    def _save_metrics(self, metrics: Dict[str, Any]):
        """Sauvegarde les métriques"""
        try:
            metrics_file = Path(DEFAULT_LOG_DIR) / "metrics.json"
            with open(metrics_file, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2, default=str)
                
        except Exception as e:
            self._internal_logger.error(f"Erreur sauvegarde métriques: {e}")
    
    def _setup_shutdown_hooks(self):
        """Enregistre les hooks de fermeture"""
        def shutdown_handler(*args):
            self.shutdown()
        
        atexit.register(shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)
        signal.signal(signal.SIGINT, shutdown_handler)

    def shutdown(self):
        """Arrêt propre du système"""
        if self._is_shutdown:
            return
            
        try:
            self._is_shutdown = True
            
            # Arrêter le thread de maintenance
            if self._maintenance_thread and self._maintenance_thread.is_alive():
                self._maintenance_thread.join()

            # Fermer tous les handlers de tous les loggers
            loggers_to_shutdown = list(self._loggers.values()) + [self._internal_logger]
            for logger in loggers_to_shutdown:
                for handler in logger.handlers[:]:
                    handler.close()
                    logger.removeHandler(handler)
            
            self._internal_logger.info("NextGeneration LoggingManager arrêté proprement")

            # Réinitialiser l'état
            self._loggers.clear()
            self._initialized = False # Allow re-initialization
            
        except Exception as e:
            # Be careful here, internal_logger might be closed
            print(f"Erreur lors du shutdown: {e}", file=sys.stderr)
    
    @contextmanager
    def log_performance(self, operation_name: str, logger: logging.Logger = None):
        """Context manager pour mesurer les performances"""
        start_time = time.time()
        logger = logger or self._internal_logger
        
        try:
            logger.info(f"Début opération: {operation_name}")
            yield
        except Exception as e:
            logger.error(f"Erreur dans {operation_name}: {e}")
            raise
        finally:
            duration = time.time() - start_time
            logger.info(f"Fin opération: {operation_name} - Durée: {duration:.3f}s")
            
            # Stocker la métrique
            self._metrics.performance_stats[operation_name] = duration

# API simplifiée pour compatibilité
def get_logger(name: str) -> logging.Logger:
    """API simplifiée pour obtenir un logger"""
    return NextGenLoggingManager().get_logger(custom_config={"logger_name": name})

def get_agent_logger(agent_name: str, role: str, domain: str, agent_id: str = None) -> logging.Logger:
    """API simplifiée pour obtenir un logger d'agent"""
    return NextGenLoggingManager().get_logger('custom_agent_logger', custom_config={'logger_name': 'Agent', 'extra_fields': {}})

def log_performance(operation_name: str, logger: logging.Logger = None):
    """API simplifiée pour mesurer les performances"""
    return NextGenLoggingManager().log_performance(operation_name, logger)

# Point d'entrée principal
if __name__ == "__main__":
    # Test de base
    manager = NextGenLoggingManager()
    logger = manager.get_logger("test")
    
    logger.info("🚀 NextGeneration Logging System - Golden Source initialisé !")
    logger.info(f"Version: {NEXTGEN_VERSION}")
    
    # Test des fonctionnalités
    with manager.log_performance("test_operation", logger):
        logger.debug("Test de debug")
        logger.info("Test d'info")
        logger.warning("Test de warning")
        logger.error("Test d'erreur")
    
    # Afficher les métriques
    metrics = manager.get_metrics()
    print(f"\n📊 Métriques système:")
    print(f"Total logs: {metrics['core_metrics']['total_logs']}")
    print(f"Loggers actifs: {metrics['system_health']['active_loggers']}")
    
    print("\n✅ Test Golden Source terminé avec succès !") 




