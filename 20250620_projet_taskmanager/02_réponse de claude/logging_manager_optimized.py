#!/usr/bin/env python3
"""
LoggingManager Centralisé NextGeneration - Version Optimisée
Gestion unifiée de tous les logs du système avec performances améliorées
"""

import asyncio
import json
from logging_manager_optimized import LoggingManager
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

# Constants
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s"
ASYNC_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - [%(task_name)s] - %(message)s"
MAX_LOG_SIZE = 50 * 1024 * 1024  # 50MB
COMPRESSION_THRESHOLD = 100 * 1024 * 1024  # 100MB

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
    """Configuration de logging enrichie pour un composant"""
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

@dataclass
class LogMetrics:
    """Métriques de performance du système de logging"""
    total_logs: int = 0
    logs_per_level: Dict[str, int] = field(default_factory=lambda: {level.value: 0 for level in LogLevel})
    logs_per_category: Dict[str, int] = field(default_factory=lambda: {cat.value: 0 for cat in LogCategory})
    average_log_size: float = 0.0
    compression_ratio: float = 0.0
    errors_count: int = 0
    last_error: Optional[str] = None
    performance_stats: Dict[str, float] = field(default_factory=dict)

class AsyncLogHandler(logging.Handler):
    """Handler asynchrone pour haute performance"""
    
    def __init__(self, base_handler: logging.Handler, queue_size: int = 10000):
        super().__init__()
        self.base_handler = base_handler
        self.queue = queue.Queue(maxsize=queue_size)
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        self._shutdown = False
        
    def _worker(self):
        """Worker thread pour traitement asynchrone"""
        while not self._shutdown:
            try:
                record = self.queue.get(timeout=0.1)
                if record is None:  # Signal de shutdown
                    break
                self.base_handler.emit(record)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Erreur dans worker de logging: {e}", file=sys.stderr)
    
    def emit(self, record):
        """Émission asynchrone du log"""
        try:
            self.queue.put_nowait(record)
        except queue.Full:
            # En cas de queue pleine, log directement (fallback synchrone)
            self.base_handler.emit(record)
    
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
        
        self._internal_logger.info("LoggingManager initialisé avec succès")
    
    def _setup_internal_logger(self) -> logging.Logger:
        """Configure le logger interne du LoggingManager"""
        # LoggingManager NextGeneration - Core System
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={
            "logger_name": "LogLevel",
            "log_level": "INFO",
            "elasticsearch_enabled": True,
            "encryption_enabled": True,
            "async_enabled": True,
            "audit_enabled": True,
            "high_throughput": True
        })
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
            
            # Wrapper asynchrone si activé
            if config.async_enabled:
                async_handler = AsyncLogHandler(file_handler)
                self._async_handlers.append(async_handler)
                logger.addHandler(async_handler)
            else:
                logger.addHandler(file_handler)
        
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
        
        # Ajouter un filtre pour les métriques
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
        """Retourne les métriques du système de logging"""
        metrics = {
            "total_logs": self._metrics.total_logs,
            "logs_per_level": dict(self._metrics.logs_per_level),
            "logs_per_category": dict(self._metrics.logs_per_category),
            "average_log_size": self._metrics.average_log_size,
            "compression_ratio": self._metrics.compression_ratio,
            "errors_count": self._metrics.errors_count,
            "last_error": self._metrics.last_error,
            "active_loggers": len(self._loggers),
            "async_handlers": len(self._async_handlers),
            "performance_stats": dict(self._metrics.performance_stats),
            "timestamp": datetime.now().isoformat()
        }
        
        # Sauvegarder les métriques
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
                