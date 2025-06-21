#!/usr/bin/env python3
"""
Coeur fonctionnel du système de logging NextGeneration.

Ce module contient les classes de configuration de base et les énumérations
qui forment le contrat de données pour le système de logging.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional

# Constantes pour les valeurs par défaut
DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB

class LogLevel(Enum):
    """Niveaux de log standardisés pour NextGeneration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogCategory(Enum):
    """Catégories de logs pour organisation et analyse."""
    AGENT = "agents"
    TOOL = "tools"
    SYSTEM = "system"
    ERROR = "errors"
    AUDIT = "audit"
    PERFORMANCE = "performance"

@dataclass
class LoggingConfig:
    """Configuration de logging enrichie et modulaire."""
    logger_name: str
    log_level: str = LogLevel.INFO.value
    log_dir: str = "logs"
    filename_pattern: str = "{component}_{date}.log"
    max_file_size: int = MAX_LOG_SIZE
    backup_count: int = 10
    console_enabled: bool = True
    file_enabled: bool = True
    format_string: str = DEFAULT_FORMAT
    
    # Modules optionnels
    async_enabled: bool = False
    compression_enabled: bool = True
    retention_days: int = 30
    
    # Intégrations externes
    elasticsearch_enabled: bool = False
    encryption_enabled: bool = False
    alerting_enabled: bool = False
    
    # Métadonnées et configurations spécifiques
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Configurations avancées pour les modules
    elasticsearch_config: Optional[Dict[str, Any]] = field(default_factory=dict)
    encryption_config: Optional[Dict[str, Any]] = field(default_factory=dict)
    alerting_config: Optional[Dict[str, Any]] = field(default_factory=dict) 



