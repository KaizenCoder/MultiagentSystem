#!/usr/bin/env python3
"""
🏭 Maintenance Template Manager - Pattern Factory
Mission: Gestionnaire de templates pour l'équipe d'agents de maintenance
Architecture: Pattern Factory NextGeneration

Fonctionnalités:
- Gestion des templates JSON de maintenance
- Création d'agents via factory
- Cache intelligent et performance
- Validation et monitoring
"""

import asyncio
import json
from logging_manager_optimized import LoggingManager
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Type
import importlib.util
from dataclasses import dataclass

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@dataclass
class MaintenanceFactoryConfig:
    """Configuration du Pattern Factory pour maintenance"""
    templates_dir: str = "./templates/maintenance"
    cache_ttl: int = 3600  # 1 heure
    enable_hot_reload: bool = True
    max_cache_size: int = 50
    enable_validation: bool = True
    async_creation: bool = True

class MaintenanceAgentTemplate:
    """Template d'agent de maintenance selon Pattern Factory"""
    
    def __init__(self, template_data: Dict[str, Any], template_path: Path):
        self.template_data = template_data
        self.template_path = template_path
        self.name = template_data.get("name", "unknown")
        self.version = template_data.get("version", "1.0.0")
        self.role = template_data.get("role", "agent")
        self.domain = template_data.get("domain", "maintenance")
        self.model = template_data.get("model", "Unknown")
        self.capabilities = template_data.get("capabilities", [])
        self.tools = template_data.get("tools", [])
        self.default_config = template_data.get("default_config", {})
        self.interfaces = template_data.get("interfaces", {})
        self.dependencies = template_data.get("dependencies", [])
        
        self._validation_cache = None
        # LoggingManager NextGeneration - Template Manager
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={
            "logger_name": "class",
            "log_level": "INFO",
            "elasticsearch_enabled": True,
            "encryption_enabled": False,
            "async_enabled": True,
            "structured_logging": True
        })
    
    @classmethod
    def from_file(cls, template_path: Path) -> 'MaintenanceAgentTemplate':
        """Charger un template depuis un fichier JSON"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            return cls(template_data, template_path)
        except Exception as e:
            raise TemplateLoadError(f"Erreur chargement template {template_path}: {e}")
    
    @classmethod
    def from_name(cls, name: str, templates_dir: Path) -> 'MaintenanceAgentTemplate':
        """Charger un template par son nom"""
        template_path = templates_dir / f"{name}.json"
        if not template_path.exists():
            raise TemplateNotFoundError(f"Template {name} non trouvé dans {templates_dir}")
        return cls.from_file(template_path)
    
    def validate(self) -> bool:
        """Valider la structure du template"""
        if self._validation_cache is not None:
            return self._validation_cache
        
        try:
            # Validation des champs obligatoires
            required_fields = ["name", "version", "role", "domain", "capabilities"]
            for field in required_fields:
                if field not in self.template_data:
                    raise TemplateValidationError(f"Champ obligatoire manquant: {field}")
            
            # Validation de la structure
            if not isinstance(self.capabilities, list):
                raise TemplateValidationError("'capabilities' doit être une liste")
            
            if not isinstance(self.tools, list):
                raise TemplateValidationError("'tools' doit être une liste")
            
            if not isinstance(self.default_config, dict):
                raise TemplateValidationError("'default_config' doit être un dictionnaire")
            
            # Validation des interfaces
            if self.interfaces and not isinstance(self.interfaces, dict):
                raise TemplateValidationError("'interfaces' doit être un dictionnaire")
            
            self._validation_cache = True
            self.logger.info(f"✅ Template {self.name} validé avec succès")
            return True
            
        except Exception as e:
            self._validation_cache = False
            self.logger.error(f"❌ Validation échouée pour {self.name}: {e}")
            raise
    
    def create_agent_config(self, suffix: str = "", custom_config: Dict = None) -> Dict[str, Any]:
        """Créer la configuration pour un agent"""
        config = {
            "agent_id": f"{self.name}_{suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "agent_type": self.name,
            "agent_role": self.role,
            "agent_domain": self.domain,
            "agent_model": self.model,
            "capabilities": self.capabilities.copy(),
            "tools": self.tools.copy(),
            "config": self.default_config.copy(),
            "template_version": self.version,
            "created_at": datetime.now().isoformat()
        }
        
        # Fusionner la configuration personnalisée
        if custom_config:
            config["config"].update(custom_config)
        
        return config

class MaintenanceTemplateManager:
    """Gestionnaire de templates pour agents de maintenance selon Pattern Factory"""
    
    def __init__(self, config: MaintenanceFactoryConfig = None):
        self.config = config or MaintenanceFactoryConfig()
        self.templates_dir = Path(self.config.templates_dir)
        self.logger = logging.getLogger("MaintenanceTemplateManager")
        
        # Cache des templates
        self._template_cache: Dict[str, MaintenanceAgentTemplate] = {}
        self._cache_timestamps: Dict[str, datetime] = {}
        
        # Métriques
        self._metrics = {
            "templates_loaded": 0,
            "agents_created": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "validation_errors": 0,
            "creation_errors": 0
        }
        
        self.logger.info(f"🏭 MaintenanceTemplateManager initialisé")
        self.logger.info(f"   📁 Templates dir: {self.templates_dir}")
        self.logger.info(f"   💾 Cache TTL: {self.config.cache_ttl}s")
        
    async def startup(self):
        """Démarrer le gestionnaire de templates"""
        self.logger.info("🚀 Démarrage MaintenanceTemplateManager")
        
        # Créer le répertoire des templates s'il n'existe pas
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Pré-charger les templates
        await self._preload_templates()
        
        self.logger.info("✅ MaintenanceTemplateManager prêt")
    
    async def shutdown(self):
        """Arrêter le gestionnaire"""
        self.logger.info("🛑 Arrêt MaintenanceTemplateManager")
        self._template_cache.clear()
        self._cache_timestamps.clear()
    
    async def _preload_templates(self):
        """Pré-charger tous les templates disponibles"""
        if not self.templates_dir.exists():
            self.logger.warning(f"⚠️ Répertoire templates introuvable: {self.templates_dir}")
            return
        
        template_files = list(self.templates_dir.glob("*.json"))
        loaded_count = 0
        
        for template_file in template_files:
            try:
                template = MaintenanceAgentTemplate.from_file(template_file)
                if template.validate():
                    self._template_cache[template.name] = template
                    self._cache_timestamps[template.name] = datetime.now()
                    loaded_count += 1
                    self.logger.info(f"📋 Template chargé: {template.name} (v{template.version})")
            except Exception as e:
                self._metrics["validation_errors"] += 1
                self.logger.error(f"❌ Erreur chargement template {template_file.name}: {e}")
        
        self._metrics["templates_loaded"] = loaded_count
        self.logger.info(f"📊 {loaded_count} templates chargés en cache")
    
    def list_templates(self) -> List[str]:
        """Lister les templates disponibles"""
        return list(self._template_cache.keys())
    
    def get_template(self, name: str) -> MaintenanceAgentTemplate:
        """Obtenir un template par nom"""
        # Vérifier le cache
        if name in self._template_cache:
            # Vérifier l'expiration
            if self.config.enable_hot_reload:
                cache_time = self._cache_timestamps.get(name)
                if cache_time and (datetime.now() - cache_time).seconds > self.config.cache_ttl:
                    # Recharger depuis le fichier
                    try:
                        template = MaintenanceAgentTemplate.from_name(name, self.templates_dir)
                        if template.validate():
                            self._template_cache[name] = template
                            self._cache_timestamps[name] = datetime.now()
                            self.logger.info(f"🔄 Template rechargé: {name}")
                    except Exception as e:
                        self.logger.error(f"❌ Erreur rechargement template {name}: {e}")
            
            self._metrics["cache_hits"] += 1
            return self._template_cache[name]
        
        # Charger depuis le fichier
        self._metrics["cache_misses"] += 1
        try:
            template = MaintenanceAgentTemplate.from_name(name, self.templates_dir)
            if template.validate():
                self._template_cache[name] = template
                self._cache_timestamps[name] = datetime.now()
                return template
        except Exception as e:
            self._metrics["validation_errors"] += 1
            raise TemplateLoadError(f"Impossible de charger le template {name}: {e}")
    
    async def create_agent(self, template_name: str, suffix: str = "", custom_config: Dict = None) -> Any:
        """Créer un agent à partir d'un template"""
        try:
            self.logger.info(f"🏗️ Création agent: {template_name}")
            
            # Obtenir le template
            template = self.get_template(template_name)
            
            # Créer la configuration
            agent_config = template.create_agent_config(suffix, custom_config)
            
            # Importer et instancier la classe d'agent correspondante
            agent_class = await self._import_agent_class(template_name)
            
            # Créer l'instance
            if self.config.async_creation and hasattr(agent_class, '__aenter__'):
                agent = await agent_class(**agent_config)
            else:
                agent = agent_class(**agent_config)
            
            # Configurer l'agent selon le template
            if hasattr(agent, 'configure_from_template'):
                await agent.configure_from_template(template)
            
            self._metrics["agents_created"] += 1
            self.logger.info(f"✅ Agent créé: {agent_config['agent_id']}")
            
            return agent
            
        except Exception as e:
            self._metrics["creation_errors"] += 1
            self.logger.error(f"❌ Erreur création agent {template_name}: {e}")
            raise AgentCreationError(f"Échec création agent {template_name}: {e}")
    
    async def bulk_create_agents(self, agent_specs: List[Dict[str, Any]]) -> List[Any]:
        """Créer plusieurs agents en lot"""
        self.logger.info(f"🏭 Création en lot: {len(agent_specs)} agents")
        
        agents = []
        for spec in agent_specs:
            try:
                agent = await self.create_agent(
                    template_name=spec["template"],
                    suffix=spec.get("suffix", ""),
                    custom_config=spec.get("config", {})
                )
                agents.append(agent)
            except Exception as e:
                self.logger.error(f"❌ Échec création agent {spec.get('template', 'unknown')}: {e}")
                if spec.get("fail_fast", False):
                    raise
        
        self.logger.info(f"✅ Création lot terminée: {len(agents)}/{len(agent_specs)} agents créés")
        return agents
    
    async def _import_agent_class(self, template_name: str) -> Type:
        """Importer dynamiquement la classe d'agent"""
        # Mapping template -> fichier Python
        agent_file_mapping = {
            "agent_0_chef_equipe_coordinateur": "agent_0_chef_equipe_coordinateur.py",
            "agent_1_analyseur_structure": "agent_1_analyseur_structure.py", 
            "agent_2_evaluateur_utilite": "agent_2_evaluateur_utilite.py",
            "agent_3_adaptateur_code": "agent_3_adaptateur_code.py",
            "agent_4_testeur_integration": "agent_4_testeur_integration.py",
            "agent_5_documenteur": "agent_5_documenteur.py",
            "agent_6_validateur_final": "agent_6_validateur_final.py"
        }
        
        # Mapping template -> classe
        agent_class_mapping = {
            "agent_0_chef_equipe_coordinateur": "Agent0ChefEquipeCoordinateur",
            "agent_1_analyseur_structure": "Agent1AnalyseurStructure",
            "agent_2_evaluateur_utilite": "Agent2EvaluateurUtilite", 
            "agent_3_adaptateur_code": "Agent3AdaptateurCode",
            "agent_4_testeur_integration": "Agent4TesteurIntegration",
            "agent_5_documenteur": "Agent5Documenteur",
            "agent_6_validateur_final": "Agent6ValidateurFinal"
        }
        
        if template_name not in agent_file_mapping:
            raise ImportError(f"Mapping non trouvé pour template: {template_name}")
        
        file_name = agent_file_mapping[template_name]
        class_name = agent_class_mapping[template_name]
        
        # Importer le module
        module_path = Path(__file__).parent / file_name
        if not module_path.exists():
            raise ImportError(f"Fichier agent non trouvé: {module_path}")
        
        spec = importlib.util.spec_from_file_location(f"agent_{template_name}", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Obtenir la classe
        if not hasattr(module, class_name):
            raise ImportError(f"Classe {class_name} non trouvée dans {file_name}")
        
        return getattr(module, class_name)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Obtenir les métriques de performance"""
        total_operations = self._metrics["cache_hits"] + self._metrics["cache_misses"]
        hit_rate = self._metrics["cache_hits"] / max(total_operations, 1)
        
        return {
            **self._metrics,
            "cache_hit_rate": hit_rate,
            "templates_in_cache": len(self._template_cache),
            "avg_creation_time": 0.0,  # À implémenter
            "memory_usage": len(self._template_cache) * 1024  # Estimation
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Vérification de santé du gestionnaire"""
        return {
            "status": "healthy",
            "templates_loaded": len(self._template_cache),
            "cache_enabled": True,
            "hot_reload": self.config.enable_hot_reload,
            "templates_dir_exists": self.templates_dir.exists(),
            "metrics": self.get_metrics()
        }

# Exceptions personnalisées
class TemplateError(Exception):
    """Exception de base pour les templates"""
    pass

class TemplateNotFoundError(TemplateError):
    """Template non trouvé"""
    pass

class TemplateLoadError(TemplateError):
    """Erreur de chargement de template"""
    pass

class TemplateValidationError(TemplateError):
    """Erreur de validation de template"""
    pass

class AgentCreationError(Exception):
    """Erreur de création d'agent"""
    pass

# Fonction factory pour faciliter l'utilisation
def create_maintenance_template_manager(templates_dir: str = None) -> MaintenanceTemplateManager:
    """Factory pour créer un gestionnaire de templates de maintenance"""
    config = MaintenanceFactoryConfig()
    if templates_dir:
        config.templates_dir = templates_dir
    return MaintenanceTemplateManager(config)

# Point d'entrée pour tests
async def main():
    """Test du gestionnaire de templates"""
    print("🏭 TEST MAINTENANCE TEMPLATE MANAGER")
    print("=" * 50)
    
    try:
        # Créer le gestionnaire
        manager = create_maintenance_template_manager()
        await manager.startup()
        
        # Afficher les templates disponibles
        templates = manager.list_templates()
        print(f"📋 Templates disponibles: {templates}")
        
        # Vérifier la santé
        health = manager.health_check()
        print(f"🏥 Santé: {health['status']}")
        
        # Métriques
        metrics = manager.get_metrics()
        print(f"📊 Cache hit rate: {metrics['cache_hit_rate']:.2%}")
        
        await manager.shutdown()
        print("✅ Test terminé avec succès")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    result = asyncio.run(main())
    exit(result) 