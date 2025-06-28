#!/usr/bin/env python3
"""
Gestionnaire de logging centralisé et modulaire pour NextGeneration.
"""

import logging
import threading
import json
from pathlib import Path
from typing import Dict, Optional

from .logging_core import LoggingConfig, LogLevel, LogCategory, DEFAULT_FORMAT
from .handlers.console_handler import ConsoleHandler
from .handlers.file_handler import FileHandler
from .handlers.async_handler import AsyncLogHandler, CompositeHandler
from .handlers.encryption_handler import EncryptionHandler
from .handlers.elasticsearch_handler import ElasticsearchHandler
from cryptography.fernet import Fernet

class LoggingManager:
    """Orchestre la création et la gestion des loggers."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_file: str = "config/logging_centralized.json"):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self._loggers: Dict[str, logging.Logger] = {}
        self.config_file = Path(config_file)
        self._configs: Dict[str, LoggingConfig] = {}
        
        self._internal_logger = self._setup_internal_logger()
        self._load_or_create_config()
        self._internal_logger.info("LoggingManager modulaire initialisé.")

    def _setup_internal_logger(self) -> logging.Logger:
        """Configure le logger interne du LoggingManager."""
        logger = logging.getLogger("nextgen.logging.manager")
        logger.setLevel(logging.DEBUG)
        
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(DEFAULT_FORMAT))
            logger.addHandler(console_handler)
        
        return logger

    def _load_or_create_config(self):
        """Charge ou crée la configuration de logging."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    for name, config in config_data.items():
                        self._configs[name] = LoggingConfig(**config)
                self._internal_logger.info(f"Configuration chargée: {len(self._configs)} configs")
            except Exception as e:
                self._internal_logger.error(f"Erreur chargement config: {e}. Création d'une config par défaut.")
                self._create_default_configs()
        else:
            self._internal_logger.warning(f"Fichier de config non trouvé. Création d'une config par défaut.")
            self._create_default_configs()
            self._save_config()

    def _create_default_configs(self):
        """Crée les configurations par défaut."""
        self._configs = {
            "default": LoggingConfig(logger_name="nextgen.default"),
            "audit": LoggingConfig(
                logger_name="nextgen.audit",
                log_dir="logs/audit",
                log_level=LogLevel.INFO.value
            )
        }

    def _save_config(self):
        """Sauvegarde la configuration de manière atomique."""
        try:
            config_data = {name: config.__dict__ for name, config in self._configs.items()}
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            temp_file = self.config_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            temp_file.replace(self.config_file)
            self._internal_logger.info(f"Configuration sauvegardée dans '{self.config_file}'")
        except Exception as e:
            self._internal_logger.error(f"Erreur sauvegarde config: {e}")

    def get_config(self, name: str) -> Optional[LoggingConfig]:
        """Récupère une configuration par son nom."""
        return self._configs.get(name)

    def get_logger(self, config_name: str, custom_config: Optional[Dict] = None) -> logging.Logger:
        """
        Récupère ou crée un logger basé sur une configuration.
        
        Args:
            config_name (str): Le nom de la configuration à utiliser.
            custom_config (Optional[Dict]): Une configuration ad-hoc à la place
                                           d'une configuration nommée.
        
        Returns:
            logging.Logger: L'instance du logger configuré.
        """
        if config_name in self._loggers and custom_config is None:
            return self._loggers[config_name]
        
        if custom_config:
            config = LoggingConfig(**custom_config)
            logger_key = config.logger_name
        else:
            config = self.get_config(config_name)
            if not config:
                self._internal_logger.warning(f"Config '{config_name}' non trouvée. Utilisation de la config par défaut.")
                config = self.get_config('default')
            logger_key = config.logger_name

        if logger_key in self._loggers:
            return self._loggers[logger_key]

        logger = logging.getLogger(logger_key)
        logger.setLevel(logging.DEBUG)  # Le niveau est géré par les handlers
        logger.propagate = False

        # Vider les handlers existants pour éviter les duplications
        if logger.hasHandlers():
            logger.handlers.clear()
            
        # 1. Créer tous les handlers de base nécessaires
        base_handlers = []
        if config.console_enabled:
            base_handlers.append(ConsoleHandler.create(config))
            
        if config.file_enabled:
            file_handler = FileHandler.create(config)
            if file_handler:
                base_handlers.append(file_handler)
        
        if config.elasticsearch_enabled:
            es_handler = ElasticsearchHandler(
                es_hosts=config.elasticsearch_config.get("hosts", ["http://localhost:9200"]),
                index_name_pattern=config.elasticsearch_config.get("index_pattern")
            )
            if es_handler.es_client: # On ne l'ajoute que si la connexion est réussie
                base_handlers.append(es_handler)

        # S'il n'y a pas de handlers, on ne fait rien
        if not base_handlers:
            self._loggers[logger_key] = logger
            return logger

        # 2. Encapsuler les handlers de base dans un handler de plus haut niveau
        #    qui sera le point d'entrée pour le logger.
        top_handler: logging.Handler = CompositeHandler(base_handlers) if len(base_handlers) > 1 else base_handlers[0]

        # 3. Appliquer les wrappers (sécurité, asynchrone, etc.)
        if config.encryption_enabled:
            # DÉSACTIVÉ TEMPORAIREMENT - Problème de clés de chiffrement
            # encryption_key = config.encryption_config.get("key") or Fernet.generate_key().decode()
            # top_handler = EncryptionHandler(base_handler=top_handler, encryption_key=encryption_key)
            self._internal_logger.warning("Chiffrement désactivé temporairement - problème de clés")
        
        if config.async_enabled:
            top_handler = AsyncLogHandler(base_handler=top_handler)
            
        logger.addHandler(top_handler)

        self._loggers[logger_key] = logger
        self.log_debug(f"Logger '{logger.name}' créé et configuré.")
        return logger

    def get_audit_logger(self):
        """Retourne un logger pré-configuré pour l'audit."""
        audit_config = {
            'logger_name': 'nextgen.audit',
            'log_level': 'INFO',
            'file_enabled': True,
            'filename_pattern': 'audit.log',
            'console_enabled': False,
            'encryption_enabled': True # L'audit doit toujours être chiffré
        }
        return self.get_logger('audit', custom_config=audit_config)

    def log_performance(self, message, exec_time, category='performance'):
        """Enregistre une métrique de performance."""
        perf_logger = self.get_logger('performance')
        perf_logger.info(f"{message} - Temps d'exécution: {exec_time:.4f}s", extra={'category': category})

    def log_debug(self, message, category='system'):
        """Enregistre un message de debug système."""
        debug_logger = self.get_logger('manager_debug')
        debug_logger.debug(message, extra={'category': category}) 



