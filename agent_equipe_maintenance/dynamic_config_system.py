#!/usr/bin/env python3
"""
⚙️ SYSTÈME CONFIGURATION DYNAMIQUE - Équipe Maintenance NextGeneration
=====================================================================

Mission: Configuration intelligente et adaptative pour tous les environnements
- Configuration par environnement (dev/test/prod)
- Auto-détection ressources système
- Configuration agents personnalisée
- Monitoring configuration temps réel

Author: Expert Configuration
Version: 2.0.0
"""

import json
import os
import sys
import psutil
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import platform

@dataclass
class SystemResources:
    """Ressources système détectées"""
    cpu_count: int
    memory_gb: float
    disk_free_gb: float
    gpu_available: bool
    gpu_memory_gb: float
    platform: str
    python_version: str

@dataclass
class AgentConfig:
    """Configuration spécifique à un agent"""
    agent_id: str
    max_parallel_tasks: int
    timeout_seconds: int
    memory_limit_mb: int
    log_level: str
    specialized_params: Dict[str, Any]

@dataclass
class EnvironmentConfig:
    """Configuration globale d'environnement"""
    environment: str  # dev, test, prod
    debug_mode: bool
    safe_mode: bool
    backup_enabled: bool
    monitoring_enabled: bool
    max_agents_parallel: int
    database_config: Dict[str, str]
    paths_config: Dict[str, str]

class DynamicConfigManager:
    """Gestionnaire de configuration dynamique intelligent"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.system_resources = self._detect_system_resources()
        self.environment = self._detect_environment()
        self.base_config = self._load_base_config()
        
        # Logger pour le config manager
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("DynamicConfigManager")
        
    def _detect_system_resources(self) -> SystemResources:
        """Détection automatique des ressources système"""
        
        # CPU et mémoire
        cpu_count = psutil.cpu_count()
        memory_bytes = psutil.virtual_memory().total
        memory_gb = memory_bytes / (1024**3)
        
        # Espace disque
        disk_usage = psutil.disk_usage('.')
        disk_free_gb = disk_usage.free / (1024**3)
        
        # GPU (détection simplifiée)
        gpu_available = False
        gpu_memory_gb = 0.0
        
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_available = True
                gpu_memory_gb = gpus[0].memoryTotal / 1024  # MB to GB
        except ImportError:
            try:
                # Fallback: nvidia-ml-py
                import pynvml
                pynvml.nvmlInit()
                if pynvml.nvmlDeviceGetCount() > 0:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    gpu_available = True
                    gpu_memory_gb = meminfo.total / (1024**3)
            except:
                # Pas de GPU détecté
                pass
        
        return SystemResources(
            cpu_count=cpu_count,
            memory_gb=round(memory_gb, 2),
            disk_free_gb=round(disk_free_gb, 2),
            gpu_available=gpu_available,
            gpu_memory_gb=round(gpu_memory_gb, 2),
            platform=platform.system(),
            python_version=sys.version.split()[0]
        )
    
    def _detect_environment(self) -> str:
        """Détection intelligente de l'environnement"""
        
        # Variables d'environnement
        env = os.getenv('ENVIRONMENT', '').lower()
        if env in ['dev', 'test', 'prod']:
            return env
            
        # Détection par nom machine ou répertoire
        hostname = platform.node().lower()
        current_path = str(Path.cwd()).lower()
        
        if 'prod' in hostname or 'production' in current_path:
            return 'prod'
        elif 'test' in hostname or 'testing' in current_path:
            return 'test'
        else:
            return 'dev'  # Par défaut
    
    def _load_base_config(self) -> EnvironmentConfig:
        """Chargement configuration de base selon l'environnement"""
        
        config_file = self.config_dir / f"environment_{self.environment}.json"
        
        # Configurations par défaut selon l'environnement
        default_configs = {
            'dev': {
                'environment': 'dev',
                'debug_mode': True,
                'safe_mode': True,
                'backup_enabled': True,
                'monitoring_enabled': True,
                'max_agents_parallel': min(4, self.system_resources.cpu_count),
                'database_config': {
                    'type': 'sqlite',
                    'path': './dev_database.db'
                },
                'paths_config': {
                    'workspace': './workspace_dev',
                    'backup': './backups_dev',
                    'logs': './logs_dev'
                }
            },
            'test': {
                'environment': 'test',
                'debug_mode': True,
                'safe_mode': True,
                'backup_enabled': True,
                'monitoring_enabled': True,
                'max_agents_parallel': min(6, self.system_resources.cpu_count),
                'database_config': {
                    'type': 'postgresql',
                    'host': 'localhost',
                    'port': 5432,
                    'database': 'nextgen_test'
                },
                'paths_config': {
                    'workspace': './workspace_test',
                    'backup': './backups_test',
                    'logs': './logs_test'
                }
            },
            'prod': {
                'environment': 'prod',
                'debug_mode': False,
                'safe_mode': False,
                'backup_enabled': True,
                'monitoring_enabled': True,
                'max_agents_parallel': self.system_resources.cpu_count,
                'database_config': {
                    'type': 'postgresql',
                    'host': 'localhost',
                    'port': 5432,
                    'database': 'nextgeneration'
                },
                'paths_config': {
                    'workspace': './workspace',
                    'backup': './backups',
                    'logs': './logs'
                }
            }
        }
        
        # Charger config existante ou créer par défaut
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
        else:
            config_data = default_configs[self.environment]
            self._save_config(config_file, config_data)
        
        return EnvironmentConfig(**config_data)
    
    def generate_agent_config(self, agent_id: str, agent_type: str) -> AgentConfig:
        """Génération configuration optimisée pour un agent spécifique"""
        
        # Configuration de base selon le type d'agent
        base_configs = {
            'analyseur_structure': {
                'max_parallel_tasks': min(4, self.system_resources.cpu_count),
                'timeout_seconds': 300,
                'memory_limit_mb': 512,
                'specialized_params': {
                    'max_files_batch': 50,
                    'ast_cache_enabled': True
                }
            },
            'evaluateur_utilite': {
                'max_parallel_tasks': 2,
                'timeout_seconds': 180,
                'memory_limit_mb': 256,
                'specialized_params': {
                    'evaluation_criteria_weights': {
                        'technical_relevance': 0.30,
                        'architecture_compatibility': 0.25,
                        'added_value': 0.20,
                        'integration_ease': 0.15,
                        'maintenance_burden': 0.10
                    }
                }
            },
            'adaptateur_code': {
                'max_parallel_tasks': 1,  # Opérations fichiers sensibles
                'timeout_seconds': 600,
                'memory_limit_mb': 1024,
                'specialized_params': {
                    'backup_obligatoire': True,
                    'verification_integrite': True,
                    'rollback_automatique': True
                }
            },
            'testeur_anti_faux_agents': {
                'max_parallel_tasks': min(6, self.system_resources.cpu_count),
                'timeout_seconds': 240,
                'memory_limit_mb': 512,
                'specialized_params': {
                    'test_depth': 'comprehensive',
                    'pattern_detection_enabled': True
                }
            },
            'documenteur_peer_reviewer': {
                'max_parallel_tasks': 3,
                'timeout_seconds': 300,
                'memory_limit_mb': 256,
                'specialized_params': {
                    'documentation_format': 'markdown',
                    'peer_review_enabled': True
                }
            },
            'validateur_final': {
                'max_parallel_tasks': 2,
                'timeout_seconds': 180,
                'memory_limit_mb': 256,
                'specialized_params': {
                    'validation_stricte': self.environment == 'prod',
                    'certification_enabled': True
                }
            },
            'chef_equipe_coordinateur': {
                'max_parallel_tasks': self.base_config.max_agents_parallel,
                'timeout_seconds': 1800,  # 30 minutes max
                'memory_limit_mb': 2048,
                'specialized_params': {
                    'orchestration_mode': 'intelligent',
                    'monitoring_interval': 30,
                    'auto_recovery_enabled': True
                }
            }
        }
        
        # Configuration par défaut si agent inconnu
        default_config = {
            'max_parallel_tasks': 2,
            'timeout_seconds': 300,
            'memory_limit_mb': 512,
            'specialized_params': {}
        }
        
        config_data = base_configs.get(agent_type, default_config).copy()
        
        # Ajustements selon les ressources système
        if self.system_resources.memory_gb < 8:
            # Réduire la consommation mémoire sur systèmes contraints
            config_data['memory_limit_mb'] = int(config_data['memory_limit_mb'] * 0.7)
            config_data['max_parallel_tasks'] = max(1, config_data['max_parallel_tasks'] - 1)
        
        if self.system_resources.gpu_available and agent_type in ['testeur_anti_faux_agents']:
            # Optimisations GPU si disponible
            config_data['specialized_params']['gpu_acceleration'] = True
        
        # Ajustements selon l'environnement
        log_levels = {
            'dev': 'DEBUG',
            'test': 'INFO', 
            'prod': 'WARNING'
        }
        
        return AgentConfig(
            agent_id=agent_id,
            log_level=log_levels[self.environment],
            **config_data
        )
    
    def save_agent_config(self, agent_config: AgentConfig):
        """Sauvegarde configuration agent"""
        config_file = self.config_dir / f"agent_{agent_config.agent_id}.json"
        
        config_data = asdict(agent_config)
        config_data['generated_at'] = datetime.now().isoformat()
        config_data['system_resources'] = asdict(self.system_resources)
        
        self._save_config(config_file, config_data)
        
        self.logger.info(f"✅ Configuration sauvegardée: {agent_config.agent_id}")
    
    def load_agent_config(self, agent_id: str) -> Optional[AgentConfig]:
        """Chargement configuration agent"""
        config_file = self.config_dir / f"agent_{agent_id}.json"
        
        if not config_file.exists():
            return None
            
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # Extraire seulement les champs AgentConfig
        agent_fields = {k: v for k, v in config_data.items() 
                       if k in AgentConfig.__dataclass_fields__}
        
        return AgentConfig(**agent_fields)
    
    def get_environment_config(self) -> EnvironmentConfig:
        """Retourne la configuration d'environnement actuelle"""
        return self.base_config
    
    def get_system_resources(self) -> SystemResources:
        """Retourne les ressources système détectées"""
        return self.system_resources
    
    def create_paths(self):
        """Création des répertoires nécessaires"""
        for path_name, path_value in self.base_config.paths_config.items():
            path_obj = Path(path_value)
            path_obj.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"📁 Répertoire créé: {path_name} -> {path_obj}")
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validation complète de la configuration"""
        validation = {
            'environment_valid': True,
            'resources_adequate': True,
            'paths_accessible': True,
            'issues': [],
            'recommendations': []
        }
        
        # Validation environnement
        if self.environment not in ['dev', 'test', 'prod']:
            validation['environment_valid'] = False
            validation['issues'].append(f"Environnement invalide: {self.environment}")
        
        # Validation ressources
        if self.system_resources.memory_gb < 4:
            validation['resources_adequate'] = False
            validation['issues'].append("Mémoire insuffisante (< 4GB)")
            validation['recommendations'].append("Augmenter la RAM ou réduire max_agents_parallel")
        
        if self.system_resources.disk_free_gb < 1:
            validation['resources_adequate'] = False
            validation['issues'].append("Espace disque insuffisant (< 1GB)")
        
        # Validation chemins
        for path_name, path_value in self.base_config.paths_config.items():
            try:
                path_obj = Path(path_value)
                path_obj.mkdir(parents=True, exist_ok=True)
                if not path_obj.exists() or not os.access(path_obj, os.W_OK):
                    validation['paths_accessible'] = False
                    validation['issues'].append(f"Chemin inaccessible: {path_name}")
            except Exception as e:
                validation['paths_accessible'] = False
                validation['issues'].append(f"Erreur chemin {path_name}: {e}")
        
        return validation
    
    def _save_config(self, file_path: Path, config_data: Dict):
        """Sauvegarde configuration dans un fichier"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False, default=str)
    
    def generate_all_agent_configs(self) -> List[AgentConfig]:
        """Génération des configurations pour tous les agents de l'équipe"""
        agents_config = [
            ('agent_01_analyseur', 'analyseur_structure'),
            ('agent_02_evaluateur', 'evaluateur_utilite'),
            ('agent_03_adaptateur', 'adaptateur_code'),
            ('agent_04_testeur', 'testeur_anti_faux_agents'),
            ('agent_05_documenteur', 'documenteur_peer_reviewer'),
            ('agent_06_validateur', 'validateur_final'),
            ('agent_00_chef_equipe', 'chef_equipe_coordinateur')
        ]
        
        configs = []
        for agent_id, agent_type in agents_config:
            config = self.generate_agent_config(agent_id, agent_type)
            self.save_agent_config(config)
            configs.append(config)
        
        return configs

def main():
    """Démonstration du système de configuration dynamique"""
    print("⚙️ SYSTÈME CONFIGURATION DYNAMIQUE - Démonstration")
    print("=" * 60)
    
    # Initialiser le gestionnaire
    config_manager = DynamicConfigManager()
    
    # Afficher informations système
    resources = config_manager.get_system_resources()
    print(f"\n💻 RESSOURCES SYSTÈME DÉTECTÉES:")
    print(f"   CPU: {resources.cpu_count} cœurs")
    print(f"   RAM: {resources.memory_gb} GB")
    print(f"   Disque libre: {resources.disk_free_gb} GB")
    print(f"   GPU: {'✅ Disponible' if resources.gpu_available else '❌ Non détecté'}")
    print(f"   Plateforme: {resources.platform}")
    print(f"   Python: {resources.python_version}")
    
    # Afficher configuration environnement
    env_config = config_manager.get_environment_config()
    print(f"\n🌍 ENVIRONNEMENT: {env_config.environment.upper()}")
    print(f"   Debug: {env_config.debug_mode}")
    print(f"   Safe mode: {env_config.safe_mode}")
    print(f"   Agents parallèles max: {env_config.max_agents_parallel}")
    
    # Générer configurations agents
    print(f"\n🤖 GÉNÉRATION CONFIGURATIONS AGENTS:")
    configs = config_manager.generate_all_agent_configs()
    
    for config in configs:
        print(f"   {config.agent_id}: {config.max_parallel_tasks} tâches, {config.memory_limit_mb}MB")
    
    # Validation
    validation = config_manager.validate_configuration()
    print(f"\n✅ VALIDATION CONFIGURATION:")
    print(f"   Environnement: {'✅' if validation['environment_valid'] else '❌'}")
    print(f"   Ressources: {'✅' if validation['resources_adequate'] else '❌'}")
    print(f"   Chemins: {'✅' if validation['paths_accessible'] else '❌'}")
    
    if validation['issues']:
        print(f"\n⚠️ PROBLÈMES DÉTECTÉS:")
        for issue in validation['issues']:
            print(f"   • {issue}")
    
    if validation['recommendations']:
        print(f"\n💡 RECOMMANDATIONS:")
        for rec in validation['recommendations']:
            print(f"   • {rec}")
    
    # Créer répertoires
    config_manager.create_paths()
    
    print(f"\n🎯 Configuration dynamique générée avec succès!")
    print(f"📁 Fichiers config: {config_manager.config_dir}")

if __name__ == "__main__":
    main()




