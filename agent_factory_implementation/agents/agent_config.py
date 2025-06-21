"""
Configuration Pydantic centralise pour l'Agent Factory Pattern
Gnr par Agent 03 - Spcialiste Configuration
"""

# 🔧 CONVERTI AUTOMATIQUEMENT SYNC → ASYNC
# Date: 2025-06-19 19h35 - Correction architecture Pattern Factory
# Raison: Harmonisation async/sync avec core/agent_factory_architecture.py


from pydantic import BaseModel, Field, validator
from typing import Dict, Optional, List, Union
from enum import Enum
import os
from pathlib import Path

class Environment(str, Enum):
    """Environnements supports"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class LogLevel(str, Enum):
    """Niveaux de logs"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class EnvironmentConfig(BaseModel):
    """Configuration spcifique  un environnement"""
    ttl_seconds: int = Field(ge=30, le=3600, description="TTL cache en secondes")
    cache_max_size: int = Field(ge=10, le=10000, description="Taille maximale cache")
    thread_pool_size: int = Field(ge=1, le=32, description="Taille pool threads")
    hot_reload: bool = Field(description="Activation hot-reload")
    debug: bool = Field(description="Mode debug")
    log_level: LogLevel = Field(description="Niveau de logs")
    
    @validator('thread_pool_size')
    def validate_thread_pool(cls, v):
        """Valider la taille du pool de threads"""
    cpu_count = os.cpu_count() or 4
    if v > cpu_count * 2:
    return cpu_count * 2
    return v

class CacheConfig(BaseModel):
    """Configuration du cache LRU"""
    lru_enabled: bool = True
    max_memory_mb: int = Field(ge=16, le=2048, description="Mmoire maximale cache")
    cleanup_interval: int = Field(ge=60, le=3600, description="Intervalle nettoyage")
    compression_enabled: bool = True

class SecurityConfig(BaseModel):
    """Configuration scurit"""
    signature_required: bool = True
    validation_strict: bool = True
    encryption_enabled: bool = True
    audit_enabled: bool = True
    rsa_key_size: int = Field(default=2048, ge=2048)
    hash_algorithm: str = Field(default="SHA-256")

class MonitoringConfig(BaseModel):
    """Configuration monitoring"""
    metrics_enabled: bool = True
    tracing_enabled: bool = True
    health_check_enabled: bool = True
    prometheus_port: int = Field(ge=1024, le=65535, default=8080)

class AgentFactoryConfig(BaseModel):
    """Configuration principale Agent Factory"""
    name: str = "agent_factory_config"
    version: str = "1.0.0"
    description: str = "Configuration centralise Agent Factory Pattern"
    created_at: str
    agent_creator: str
    
    # Configuration par environnement
    environments: Dict[Environment, EnvironmentConfig]
    
    # Configurations spcialises
    cache: CacheConfig
    security: SecurityConfig
    monitoring: MonitoringConfig
    
    @validator('environments')
    def validate_environments(cls, v):
        """Valider que tous les environnements sont configurs"""
    required_envs = {Environment.DEVELOPMENT, Environment.STAGING, Environment.PRODUCTION}
    configured_envs = set(v.keys())
        
    if not required_envs.issubset(configured_envs):
    missing = required_envs - configured_envs
    raise ValueError(f"Environnements manquants: {missing}")
        
    return v
    
    def get_environment_config(self, env: Optional[str] = None) -> EnvironmentConfig:
        """Obtenir la configuration pour un environnement spcifique"""
    if env is None:
    env = os.getenv('ENVIRONMENT', 'development')
        
    env_enum = Environment(env.lower())
    return self.environments[env_enum]
    
    def is_production(self) -> bool:
        """Vrifier si on est en production"""
    current_env = os.getenv('ENVIRONMENT', 'development').lower()
    return current_env == Environment.PRODUCTION.value
    
    def get_cache_ttl(self) -> int:
        """Obtenir le TTL pour l'environnement actuel"""
    env_config = self.get_environment_config()
    return env_config.ttl_seconds
    
    def get_thread_pool_size(self) -> int:
        """Obtenir la taille du pool de threads"""
    env_config = self.get_environment_config()
    return env_config.thread_pool_size

class ConfigurationManager:
    """Gestionnaire de configuration thread-safe"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
    if cls._instance is None:
    cls._instance = super().__new__(cls)
    return cls._instance
    
    def load_config(self, config_dict: Dict) -> AgentFactoryConfig:
        """Charger la configuration depuis un dictionnaire"""
    self._config = AgentFactoryConfig(**config_dict)
    return self._config
    
    def get_config(self) -> Optional[AgentFactoryConfig]:
        """Obtenir la configuration actuelle"""
    return self._config
    
    def is_configured(self) -> bool:
        """Vrifier si la configuration est charge"""
    return self._config is not None

# Instance singleton globale
config_manager = ConfigurationManager()
