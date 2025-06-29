#!/usr/bin/env python3
"""
⚙️ Agent Configuration Manager - NextGeneration v5.3.0
Version enterprise Wave 4 avec configuration centralisée IA

Migration Pattern: CONFIGURATION_MANAGEMENT + LLM_ENHANCED + PATTERN_FACTORY
Author: Claude Sonnet 4
Date: 30 Juin 2025
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, Optional, List, Union, Any
from enum import Enum
import os
from pathlib import Path
import json
import yaml
import asyncio
from datetime import datetime
import logging

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

# Import avec fallback legacy
try:
    from agents.agent_config import (
        Environment, LogLevel, EnvironmentConfig, 
        CacheConfig, AgentConfig as LegacyAgentConfig
    )
except ImportError:
    # Définitions fallback
    class Environment(str, Enum):
        DEVELOPMENT = "development"
        STAGING = "staging"
        PRODUCTION = "production"
    
    class LogLevel(str, Enum):
        DEBUG = "DEBUG"
        INFO = "INFO"
        WARNING = "WARNING"
        ERROR = "ERROR"
        CRITICAL = "CRITICAL"

class ConfigurationValidation(BaseModel):
    """Résultat validation configuration"""
    valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    score: float = Field(0.0, ge=0.0, le=100.0)

class ConfigurationOptimization(BaseModel):
    """Optimisation configuration suggérée"""
    parameter: str
    current_value: Any
    suggested_value: Any
    impact: str
    priority: str = Field("MEDIUM", pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")

class IntelligentConfigManager:
    """Gestionnaire configuration intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.configuration_cache = {}
        self.validation_cache = {}
        self.optimization_history = []
        
        # Règles validation base
        self.validation_rules = {
            "thread_pool_size": {
                "min": 1,
                "max": os.cpu_count() * 2 if os.cpu_count() else 8,
                "optimal": os.cpu_count() if os.cpu_count() else 4
            },
            "cache_max_size": {
                "min": 100,
                "max": 100000,
                "optimal": 10000
            },
            "ttl_seconds": {
                "min": 30,
                "max": 86400,
                "optimal": 3600
            }
        }
    
    async def validate_configuration(self, config: Dict[str, Any], 
                                   environment: Environment) -> ConfigurationValidation:
        """Validation configuration avec IA"""
        validation = ConfigurationValidation(valid=True)
        
        # Validation règles de base
        for param, rules in self.validation_rules.items():
            if param in config:
                value = config[param]
                if value < rules["min"]:
                    validation.errors.append(
                        f"{param}={value} below minimum {rules['min']}"
                    )
                    validation.valid = False
                elif value > rules["max"]:
                    validation.errors.append(
                        f"{param}={value} exceeds maximum {rules['max']}"
                    )
                    validation.valid = False
                elif abs(value - rules["optimal"]) > rules["optimal"] * 0.5:
                    validation.warnings.append(
                        f"{param}={value} far from optimal {rules['optimal']}"
                    )
        
        # Validation contextuelle environnement
        if environment == Environment.PRODUCTION:
            if config.get("debug", False):
                validation.warnings.append("Debug mode enabled in production")
            if config.get("hot_reload", False):
                validation.warnings.append("Hot reload enabled in production")
        
        # Enhancement IA si disponible
        if self.llm_gateway:
            try:
                ai_validation = await self.llm_gateway.process_request(
                    "Validate configuration with contextual intelligence",
                    context={
                        "role": "configuration_expert",
                        "config": config,
                        "environment": environment.value,
                        "task": "intelligent_validation"
                    }
                )
                
                if ai_validation.get("success"):
                    enhancement = ai_validation.get("validation", {})
                    validation.suggestions.extend(
                        enhancement.get("suggestions", [])
                    )
                    
            except Exception as e:
                # Log but continue
                pass
        
        # Calcul score
        error_weight = len(validation.errors) * 10
        warning_weight = len(validation.warnings) * 5
        validation.score = max(0, 100 - error_weight - warning_weight)
        
        return validation
    
    async def optimize_configuration(self, config: Dict[str, Any], 
                                   workload_profile: str = "balanced") -> List[ConfigurationOptimization]:
        """Optimisation configuration selon profil charge"""
        optimizations = []
        
        # Profils prédéfinis
        profiles = {
            "high_throughput": {
                "thread_pool_size": os.cpu_count() * 2 if os.cpu_count() else 8,
                "cache_max_size": 50000,
                "ttl_seconds": 7200
            },
            "low_latency": {
                "thread_pool_size": os.cpu_count() if os.cpu_count() else 4,
                "cache_max_size": 20000,
                "ttl_seconds": 1800
            },
            "balanced": {
                "thread_pool_size": int(os.cpu_count() * 1.5) if os.cpu_count() else 6,
                "cache_max_size": 10000,
                "ttl_seconds": 3600
            },
            "memory_constrained": {
                "thread_pool_size": min(4, os.cpu_count() or 4),
                "cache_max_size": 1000,
                "ttl_seconds": 600
            }
        }
        
        profile = profiles.get(workload_profile, profiles["balanced"])
        
        # Génération optimisations
        for param, optimal_value in profile.items():
            if param in config and config[param] != optimal_value:
                optimization = ConfigurationOptimization(
                    parameter=param,
                    current_value=config[param],
                    suggested_value=optimal_value,
                    impact=f"Optimize for {workload_profile} workload",
                    priority="HIGH" if abs(config[param] - optimal_value) > optimal_value * 0.5 else "MEDIUM"
                )
                optimizations.append(optimization)
        
        # Enhancement IA pour optimisations contextuelles
        if self.llm_gateway:
            try:
                ai_optimizations = await self.llm_gateway.process_request(
                    "Generate intelligent configuration optimizations",
                    context={
                        "role": "performance_optimization_expert",
                        "current_config": config,
                        "workload_profile": workload_profile,
                        "task": "contextual_optimization"
                    }
                )
                
                if ai_optimizations.get("success"):
                    ai_suggestions = ai_optimizations.get("optimizations", [])
                    for suggestion in ai_suggestions:
                        optimizations.append(ConfigurationOptimization(**suggestion))
                        
            except Exception as e:
                # Log but continue
                pass
        
        return optimizations

class DynamicConfigurationLoader:
    """Chargeur configuration dynamique multi-format"""
    
    def __init__(self):
        self.supported_formats = [".json", ".yaml", ".yml", ".env"]
        self.config_cache = {}
        self.watchers = {}
    
    async def load_configuration(self, config_path: Union[str, Path], 
                               format: Optional[str] = None) -> Dict[str, Any]:
        """Chargement configuration avec détection format"""
        path = Path(config_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        
        # Détection format
        if format is None:
            format = path.suffix
        
        # Cache check
        cache_key = f"{path}:{path.stat().st_mtime}"
        if cache_key in self.config_cache:
            return self.config_cache[cache_key]
        
        # Chargement selon format
        if format in [".json"]:
            with open(path, 'r') as f:
                config = json.load(f)
        elif format in [".yaml", ".yml"]:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
        elif format == ".env":
            config = self._load_env_file(path)
        else:
            raise ValueError(f"Unsupported configuration format: {format}")
        
        # Cache result
        self.config_cache[cache_key] = config
        
        return config
    
    def _load_env_file(self, path: Path) -> Dict[str, Any]:
        """Chargement fichier .env"""
        config = {}
        
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = self._parse_env_value(value.strip())
        
        return config
    
    def _parse_env_value(self, value: str) -> Any:
        """Parse valeur environnement"""
        # Remove quotes
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        
        # Try numeric
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        # Boolean
        if value.lower() in ['true', 'yes', '1']:
            return True
        elif value.lower() in ['false', 'no', '0']:
            return False
        
        return value

class AgentConfig_Enterprise:
    """
    ⚙️ Agent Configuration Manager - Enterprise NextGeneration v5.3.0
    
    Gestionnaire configuration centralisée avec intelligence IA.
    
    Patterns NextGeneration v5.3.0:
    - CONFIGURATION_MANAGEMENT: Gestion configuration enterprise
    - LLM_ENHANCED: Validation et optimisation IA
    - PATTERN_FACTORY: Architecture modulaire éprouvée
    - HOT_RELOAD: Rechargement configuration temps réel
    """
    
    def __init__(self, agent_id: str = "config_manager", 
                 config_root: Path = None):
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
            "CONFIGURATION_MANAGEMENT",
            "LLM_ENHANCED",
            "PATTERN_FACTORY",
            "HOT_RELOAD"
        ]
        
        # Configuration agent
        self.name = "Configuration Manager Enterprise"
        self.mission = "Gestion configuration centralisée avec IA"
        self.agent_type = "configuration_enterprise"
        
        # Configuration paths
        self.config_root = config_root or Path("/etc/nextgeneration")
        self.config_root.mkdir(parents=True, exist_ok=True)
        
        # Services NextGeneration (injectés à l'initialisation)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Gestionnaires intelligents
        self.config_manager = IntelligentConfigManager()
        self.config_loader = DynamicConfigurationLoader()
        
        # Configuration state
        self.active_configs: Dict[str, Dict[str, Any]] = {}
        self.config_history: List[Dict[str, Any]] = []
        self.hot_reload_enabled = True
        
        # Métriques configuration
        self.config_metrics = {
            "loads_count": 0,
            "validations_count": 0,
            "optimizations_count": 0,
            "hot_reloads_count": 0,
            "average_validation_score": 0.0
        }
        
        # Configuration par défaut
        self.default_config = {
            Environment.DEVELOPMENT: {
                "ttl_seconds": 300,
                "cache_max_size": 1000,
                "thread_pool_size": 4,
                "hot_reload": True,
                "debug": True,
                "log_level": LogLevel.DEBUG
            },
            Environment.STAGING: {
                "ttl_seconds": 1800,
                "cache_max_size": 5000,
                "thread_pool_size": 8,
                "hot_reload": True,
                "debug": False,
                "log_level": LogLevel.INFO
            },
            Environment.PRODUCTION: {
                "ttl_seconds": 3600,
                "cache_max_size": 10000,
                "thread_pool_size": 16,
                "hot_reload": False,
                "debug": False,
                "log_level": LogLevel.WARNING
            }
        }
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Configuration logging NextGeneration"""
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="configuration",
                custom_config={
                    "logger_name": f"nextgen.config.manager.{self.agent_id}",
                    "log_dir": "logs/configuration",
                    "metadata": {
                        "agent_type": "config_manager",
                        "agent_role": "configuration",
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
            self.logger = logging.getLogger(f"ConfigManager_{self.agent_id}")
    
    async def inject_nextgen_services(self, 
                                    llm_gateway: LLMGatewayHybrid,
                                    message_bus: MessageBusA2A, 
                                    context_store: OptimizedContextStore):
        """Injection des services NextGeneration v5.3.0"""
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus  
        self.context_store = context_store
        
        # Configuration gestionnaires avec IA
        self.config_manager.llm_gateway = llm_gateway
        
        # Configuration contexte IA
        await self._setup_configuration_context()
        
        self.logger.info("✅ Services NextGeneration injectés - Configuration IA active")
    
    async def _setup_configuration_context(self):
        """Configuration contexte IA spécialisé"""
        if not self.llm_gateway:
            return
        
        config_context = {
            "role": "configuration_architect",
            "domain": "enterprise_configuration_management",
            "capabilities": [
                "Configuration validation",
                "Performance optimization",
                "Security hardening",
                "Environment-specific tuning",
                "Hot reload management"
            ],
            "patterns": [
                "CONFIGURATION_MANAGEMENT",
                "HOT_RELOAD",
                "LLM_ENHANCED"
            ]
        }
        
        # Chargement expertise configuration depuis LLM
        try:
            response = await self.llm_gateway.process_request(
                "Load configuration management expertise",
                context=config_context
            )
            
            if response.get("success"):
                self.logger.info("🧠 Expertise configuration IA chargée")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement contexte IA: {e}")
    
    async def load_configuration(self, config_name: str, 
                               environment: Environment = Environment.DEVELOPMENT,
                               config_path: Optional[str] = None) -> Dict[str, Any]:
        """Chargement configuration avec validation IA"""
        start_time = datetime.now()
        
        self.logger.info(f"⚙️ Chargement configuration: {config_name} ({environment.value})")
        
        # Path résolution
        if config_path:
            path = Path(config_path)
        else:
            path = self.config_root / environment.value / f"{config_name}.yaml"
        
        try:
            # Chargement configuration
            if path.exists():
                config = await self.config_loader.load_configuration(path)
            else:
                # Configuration par défaut
                config = self.default_config.get(environment, {})
                self.logger.warning(f"Configuration file not found, using defaults: {path}")
            
            # Validation
            validation = await self.config_manager.validate_configuration(
                config, environment
            )
            
            if not validation.valid:
                self.logger.error(f"❌ Configuration invalide: {validation.errors}")
                raise ValueError(f"Invalid configuration: {validation.errors}")
            
            if validation.warnings:
                self.logger.warning(f"⚠️ Avertissements: {validation.warnings}")
            
            # Stockage configuration active
            self.active_configs[config_name] = {
                "config": config,
                "environment": environment,
                "loaded_at": datetime.now(),
                "validation_score": validation.score
            }
            
            # Métriques
            self.config_metrics["loads_count"] += 1
            self._update_average_score(validation.score)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "config": config,
                "validation": validation.dict(),
                "metrics": {
                    "load_time_seconds": execution_time,
                    "from_cache": False
                }
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur chargement configuration: {e}")
            raise
    
    async def optimize_configuration(self, config_name: str, 
                                   workload_profile: str = "balanced") -> Dict[str, Any]:
        """Optimisation configuration avec IA"""
        self.logger.info(f"🔧 Optimisation configuration: {config_name} ({workload_profile})")
        
        if config_name not in self.active_configs:
            raise ValueError(f"Configuration not loaded: {config_name}")
        
        current_config = self.active_configs[config_name]["config"]
        
        # Génération optimisations
        optimizations = await self.config_manager.optimize_configuration(
            current_config, workload_profile
        )
        
        # Application optimisations haute priorité
        optimized_config = current_config.copy()
        applied_optimizations = []
        
        for optimization in optimizations:
            if optimization.priority in ["HIGH", "CRITICAL"]:
                optimized_config[optimization.parameter] = optimization.suggested_value
                applied_optimizations.append(optimization)
        
        # Validation configuration optimisée
        environment = self.active_configs[config_name]["environment"]
        validation = await self.config_manager.validate_configuration(
            optimized_config, environment
        )
        
        # Métriques
        self.config_metrics["optimizations_count"] += 1
        
        return {
            "original_config": current_config,
            "optimized_config": optimized_config,
            "optimizations": [opt.dict() for opt in optimizations],
            "applied": [opt.dict() for opt in applied_optimizations],
            "validation": validation.dict()
        }
    
    async def hot_reload_configuration(self, config_name: str) -> Dict[str, Any]:
        """Hot reload configuration avec notifications"""
        if not self.hot_reload_enabled:
            raise ValueError("Hot reload is disabled")
        
        self.logger.info(f"🔄 Hot reload configuration: {config_name}")
        
        if config_name not in self.active_configs:
            raise ValueError(f"Configuration not active: {config_name}")
        
        # Sauvegarde ancienne configuration
        old_config = self.active_configs[config_name]["config"].copy()
        environment = self.active_configs[config_name]["environment"]
        
        # Rechargement
        result = await self.load_configuration(config_name, environment)
        new_config = result["config"]
        
        # Détection changements
        changes = self._detect_changes(old_config, new_config)
        
        # Notification via MessageBus si disponible
        if self.message_bus and changes:
            await self.message_bus.publish(
                create_envelope(
                    message_type=MessageType.CONFIGURATION,
                    payload={
                        "event": "hot_reload",
                        "config_name": config_name,
                        "changes": changes
                    },
                    priority=Priority.HIGH
                )
            )
        
        # Métriques
        self.config_metrics["hot_reloads_count"] += 1
        
        return {
            "reloaded": True,
            "changes": changes,
            "validation": result["validation"]
        }
    
    def _detect_changes(self, old_config: Dict[str, Any], 
                       new_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Détection changements configuration"""
        changes = []
        
        # Clés modifiées
        for key in set(old_config.keys()) | set(new_config.keys()):
            old_value = old_config.get(key)
            new_value = new_config.get(key)
            
            if old_value != new_value:
                changes.append({
                    "parameter": key,
                    "old_value": old_value,
                    "new_value": new_value,
                    "action": "added" if old_value is None else "removed" if new_value is None else "modified"
                })
        
        return changes
    
    def _update_average_score(self, score: float):
        """Mise à jour score moyen validation"""
        count = self.config_metrics["validations_count"]
        avg = self.config_metrics["average_validation_score"]
        
        self.config_metrics["validations_count"] = count + 1
        self.config_metrics["average_validation_score"] = (
            (avg * count + score) / (count + 1)
        )
    
    async def get_configuration_metrics(self) -> Dict[str, Any]:
        """Métriques configuration temps réel"""
        return {
            "config_metrics": self.config_metrics,
            "active_configurations": {
                name: {
                    "environment": data["environment"].value,
                    "loaded_at": data["loaded_at"].isoformat(),
                    "validation_score": data["validation_score"]
                }
                for name, data in self.active_configs.items()
            },
            "hot_reload_enabled": self.hot_reload_enabled,
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
            "configuration": {
                "active_configs": len(self.active_configs),
                "loads_count": self.config_metrics["loads_count"],
                "average_validation_score": self.config_metrics["average_validation_score"]
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function pour compatibilité
def create_config_manager(**config) -> AgentConfig_Enterprise:
    """Factory function pour créer l'agent"""
    return AgentConfig_Enterprise(**config)

# Test standalone
async def main():
    """Test de l'agent Configuration Manager"""
    print("⚙️ Test Agent Configuration Manager NextGeneration v5.3.0")
    
    agent = create_config_manager(agent_id="test_config")
    
    # Health check
    health = await agent.health_check()
    print(f"🏥 Health: {health['status']}")
    
    # Test chargement configuration
    result = await agent.load_configuration(
        "test_app",
        Environment.DEVELOPMENT
    )
    print(f"⚙️ Configuration loaded: Score={result['validation']['score']}")
    
    # Test optimisation
    optimization = await agent.optimize_configuration(
        "test_app",
        workload_profile="high_throughput"
    )
    print(f"🔧 Optimizations: {len(optimization['optimizations'])} suggestions")
    
    # Métriques
    metrics = await agent.get_configuration_metrics()
    print(f"📊 Configs loaded: {metrics['config_metrics']['loads_count']}")

if __name__ == "__main__":
    asyncio.run(main())