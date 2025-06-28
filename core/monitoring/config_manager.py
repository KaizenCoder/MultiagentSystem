"""
Gestionnaire de Configuration Centralisée
NextGeneration Maintenance Team - Configuration Management

Gestion centralisée et validée de toute la configuration du système
avec support Pydantic pour la validation automatique.
"""

from pydantic import BaseModel, validator, Field
from typing import Dict, List, Optional, Union
import yaml
import os
from pathlib import Path

class RetryPolicy(BaseModel):
    """Configuration de la politique de retry"""
    max_retries: int = Field(ge=1, le=10, default=3)
    backoff_multiplier: float = Field(ge=1.0, le=5.0, default=2.0)
    max_backoff: int = Field(ge=30, le=600, default=300)

class AgentConfig(BaseModel):
    """Configuration spécifique à un agent"""
    agent_type: str
    max_retries: int = Field(ge=1, le=10, default=3)
    timeout_seconds: int = Field(ge=10, le=300, default=60)
    cache_enabled: bool = True
    parallel_processing: bool = False
    
    # Configurations spécialisées
    circuit_breaker_threshold: Optional[int] = Field(ge=1, le=20, default=5)
    semaphore_limit: Optional[int] = Field(ge=1, le=10, default=3)
    retry_policy: Optional[RetryPolicy] = None
    
    # Configurations avancées
    libcst_optimizations: Optional[bool] = False
    transformation_pipeline: Optional[List[str]] = []
    cache_ttl: Optional[int] = Field(ge=60, le=86400, default=3600)
    validation_enabled: Optional[bool] = True
    
    @validator('agent_type')
    def validate_agent_type(cls, v):
        valid_types = [
            'coordinateur', 'adaptateur_code', 'analyseur', 'evaluateur',
            'testeur', 'documenteur', 'correcteur', 'gestionnaire',
            'analyseur_perf', 'analyseur_sec', 'auditeur', 'harmonisateur',
            'correcteur_sem'
        ]
        if v not in valid_types:
            raise ValueError(f'Type d\'agent invalide. Types valides: {valid_types}')
        return v

class AlertThresholds(BaseModel):
    """Seuils d'alerte configurables"""
    high_error_rate: float = Field(ge=0.01, le=1.0, default=0.15)
    slow_response: float = Field(ge=1.0, le=300.0, default=30.0)
    high_memory: int = Field(ge=100*1024*1024, default=524288000)  # 500MB minimum
    circuit_breaker_failures: int = Field(ge=1, le=20, default=5)

class ResourceLimits(BaseModel):
    """Limites de ressources système"""
    max_memory_per_agent: str = "256MB"
    max_cpu_per_agent: str = "1000m"
    
    @validator('max_memory_per_agent')
    def validate_memory(cls, v):
        if not v.endswith(('MB', 'GB')):
            raise ValueError('Format mémoire invalide (ex: 256MB, 1GB)')
        return v

class CircuitBreakerConfig(BaseModel):
    """Configuration du circuit breaker"""
    failure_threshold: int = Field(ge=1, le=20, default=5)
    timeout_seconds: int = Field(ge=10, le=600, default=60)
    retry_multiplier: float = Field(ge=1.0, le=5.0, default=2.0)
    max_retry_delay: int = Field(ge=60, le=1800, default=300)

class GlobalSettings(BaseModel):
    """Configuration globale du système"""
    # Cache
    cache_ttl: int = Field(ge=60, le=86400, default=3600)
    cache_max_memory: str = "512MB"
    cache_eviction_policy: str = "lru"
    
    # Métriques
    metrics_retention_days: int = Field(ge=1, le=90, default=30)
    metrics_collection_interval: int = Field(ge=1, le=60, default=10)
    performance_monitoring: bool = True
    
    # Alertes
    alert_channels: List[str] = ["console", "log"]
    alert_thresholds: AlertThresholds = AlertThresholds()
    
    # Performance
    parallel_execution: bool = True
    max_concurrent_operations: int = Field(ge=1, le=20, default=5)
    resource_limits: ResourceLimits = ResourceLimits()
    
    # Logging
    logging_level: str = "INFO"
    structured_logging: bool = True
    log_rotation: bool = True
    log_retention_days: int = Field(ge=1, le=365, default=14)
    
    # Circuit Breaker
    circuit_breaker: CircuitBreakerConfig = CircuitBreakerConfig()
    
    @validator('cache_eviction_policy')
    def validate_eviction_policy(cls, v):
        valid_policies = ['lru', 'lfu', 'fifo', 'random']
        if v not in valid_policies:
            raise ValueError(f'Politique d\'éviction invalide: {valid_policies}')
        return v
    
    @validator('logging_level')
    def validate_logging_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v not in valid_levels:
            raise ValueError(f'Niveau de log invalide: {valid_levels}')
        return v

class CacheConfig(BaseModel):
    """Configuration du cache Redis"""
    host: str = "localhost"
    port: int = Field(ge=1, le=65535, default=6379)
    db: int = Field(ge=0, le=15, default=0)
    password: Optional[str] = None
    connection_pool_size: int = Field(ge=1, le=50, default=10)
    socket_timeout: int = Field(ge=1, le=30, default=5)
    socket_connect_timeout: int = Field(ge=1, le=30, default=5)
    retry_on_timeout: bool = True
    health_check_interval: int = Field(ge=10, le=300, default=30)

class MonitoringConfig(BaseModel):
    """Configuration du monitoring"""
    prometheus: Dict = {
        "enabled": False,
        "port": 8000,
        "metrics_path": "/metrics"
    }
    grafana: Dict = {
        "enabled": False,
        "dashboard_refresh": 5
    }
    custom_metrics: List[str] = [
        "agent_execution_time",
        "agent_success_rate", 
        "agent_error_rate",
        "cache_hit_rate",
        "memory_usage",
        "cpu_usage"
    ]

class PerformanceTestingConfig(BaseModel):
    """Configuration des tests de performance"""
    enabled: bool = True
    baseline_metrics: Dict = {
        "max_execution_time": 120,
        "min_success_rate": 0.90,
        "max_memory_usage": 419430400
    }
    load_testing: Dict = {
        "concurrent_agents": 3,
        "test_duration": 300,
        "ramp_up_time": 60
    }

class SecurityConfig(BaseModel):
    """Configuration de sécurité"""
    code_execution_sandbox: bool = True
    input_validation: str = "strict"
    output_sanitization: bool = True
    resource_isolation: bool = True
    audit_logging: bool = True
    
    @validator('input_validation')
    def validate_input_validation(cls, v):
        valid_levels = ['strict', 'moderate', 'lenient']
        if v not in valid_levels:
            raise ValueError(f'Niveau de validation invalide: {valid_levels}')
        return v

class DevelopmentConfig(BaseModel):
    """Configuration de développement"""
    debug_mode: bool = False
    verbose_logging: bool = False
    profiling_enabled: bool = False
    test_mode: bool = False
    mock_external_services: bool = False

class MaintenanceConfig(BaseModel):
    """Configuration principale du système de maintenance"""
    team_config: Dict[str, AgentConfig]
    global_settings: GlobalSettings = GlobalSettings()
    cache_config: CacheConfig = CacheConfig()
    monitoring_config: MonitoringConfig = MonitoringConfig()
    performance_testing: PerformanceTestingConfig = PerformanceTestingConfig()
    security_config: SecurityConfig = SecurityConfig()
    development_config: DevelopmentConfig = DevelopmentConfig()
    
    @validator('team_config')
    def validate_team_config(cls, v):
        if not v:
            raise ValueError('Configuration d\'équipe vide')
        
        required_agents = ['chef_equipe', 'adaptateur_code']
        for agent in required_agents:
            if agent not in v:
                raise ValueError(f'Agent requis manquant: {agent}')
        
        return v
    
    @classmethod
    def from_yaml(cls, config_path: Union[str, Path]) -> 'MaintenanceConfig':
        """Charge la configuration depuis un fichier YAML"""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Fichier de configuration non trouvé: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Conversion des configurations d'agents
            if 'team_config' in data:
                team_config = {}
                for agent_name, agent_data in data['team_config'].items():
                    team_config[agent_name] = AgentConfig(**agent_data)
                data['team_config'] = team_config
            
            return cls(**data)
            
        except yaml.YAMLError as e:
            raise ValueError(f"Erreur parsing YAML: {e}")
        except Exception as e:
            raise ValueError(f"Erreur configuration: {e}")
    
    def to_yaml(self, output_path: Union[str, Path]) -> None:
        """Sauvegarde la configuration vers un fichier YAML"""
        output_path = Path(output_path)
        
        # Conversion en dictionnaire pour YAML
        config_dict = self.dict()
        
        # Conversion des AgentConfig en dict
        if 'team_config' in config_dict:
            team_config = {}
            for agent_name, agent_config in config_dict['team_config'].items():
                if hasattr(agent_config, 'dict'):
                    team_config[agent_name] = agent_config.dict()
                else:
                    team_config[agent_name] = agent_config
            config_dict['team_config'] = team_config
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, 
                         allow_unicode=True, indent=2)
        except Exception as e:
            raise ValueError(f"Erreur sauvegarde YAML: {e}")
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Récupère la configuration d'un agent spécifique"""
        return self.team_config.get(agent_name)
    
    def validate_configuration(self) -> Dict[str, List[str]]:
        """Valide la configuration complète et retourne les erreurs"""
        errors = {"warnings": [], "errors": []}
        
        # Validation des agents
        for agent_name, agent_config in self.team_config.items():
            # Vérification cohérence timeout vs retries
            total_timeout = agent_config.timeout_seconds * agent_config.max_retries
            if total_timeout > 600:  # 10 minutes max
                errors["warnings"].append(
                    f"{agent_name}: Timeout total élevé ({total_timeout}s)"
                )
            
            # Vérification cache avec parallel processing
            if agent_config.parallel_processing and not agent_config.cache_enabled:
                errors["warnings"].append(
                    f"{agent_name}: Traitement parallèle sans cache peut dégrader les performances"
                )
        
        # Validation cohérence globale
        if (self.global_settings.max_concurrent_operations > 
            len([a for a in self.team_config.values() if a.parallel_processing])):
            errors["warnings"].append(
                "max_concurrent_operations > agents avec parallel_processing"
            )
        
        # Validation cache Redis
        if any(a.cache_enabled for a in self.team_config.values()):
            if not self.cache_config.host:
                errors["errors"].append("Cache activé mais host Redis non configuré")
        
        return errors

# Singleton pour configuration globale
_global_config: Optional[MaintenanceConfig] = None

def get_global_config() -> Optional[MaintenanceConfig]:
    """Récupère la configuration globale"""
    return _global_config

def set_global_config(config: MaintenanceConfig) -> None:
    """Définit la configuration globale"""
    global _global_config
    _global_config = config

class ConfigManager:
    """Gestionnaire de configuration centralisée"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self._config = None
        
    def load_config(self) -> MaintenanceConfig:
        """Charge la configuration depuis un fichier ou l'environnement"""
        if self.config_path and os.path.exists(self.config_path):
            return MaintenanceConfig.from_yaml(self.config_path)
        else:
            return load_config_from_env()
    
    def get_config(self) -> MaintenanceConfig:
        """Retourne la configuration chargée"""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Retourne la configuration d'un agent spécifique"""
        config = self.get_config()
        return config.get_agent_config(agent_name)
    
    def get_global_settings(self) -> GlobalSettings:
        """Retourne les paramètres globaux"""
        return self.get_config().global_settings
    
    async def startup(self):
        """Démarrage du gestionnaire de configuration"""
        self._config = self.load_config()
        print("🚀 ConfigManager démarré")
    
    async def shutdown(self):
        """Arrêt du gestionnaire de configuration"""
        print("🛑 ConfigManager arrêté")


def load_config_from_env() -> MaintenanceConfig:
    """Charge la configuration depuis les variables d'environnement"""
    config_path = os.getenv('MAINTENANCE_CONFIG_PATH', 'config/maintenance_optimization_config.yaml')
    return MaintenanceConfig.from_yaml(config_path)

# Exemple d'usage
if __name__ == "__main__":
    # Test de validation
    try:
        config = MaintenanceConfig.from_yaml("config/maintenance_optimization_config.yaml")
        validation_result = config.validate_configuration()
        
        print("✅ Configuration valide!")
        if validation_result["warnings"]:
            print("⚠️ Avertissements:")
            for warning in validation_result["warnings"]:
                print(f"  - {warning}")
        
        if validation_result["errors"]:
            print("❌ Erreurs:")
            for error in validation_result["errors"]:
                print(f"  - {error}")
                
    except Exception as e:
        print(f"❌ Erreur configuration: {e}") 