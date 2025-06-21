#!/usr/bin/env python3
"""
🏗️ Template Manager Intégré - Version ChatGPT Optimisée
Gestionnaire de templates pour agents avec fonctionnalités avancées ChatGPT
"""

import os
import json
import time
import asyncio
import hashlib
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Tuple, Callable
from dataclasses import dataclass, field
from collections import defaultdict
from contextlib import contextmanager
from functools import wraps

# Imports optionnels
try:
    import aiofiles
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    ADVANCED_FEATURES = True
except ImportError:
    ADVANCED_FEATURES = False
    print("⚠️ Fonctionnalités avancées désactivées (aiofiles, watchdog manquants)")

# Imports internes (adaptés selon l'architecture)
try:
    import sys
from pathlib import Path
from core import logging_manager, LoggingConfig
except ImportError:
    # Fallback pour les tests
    class LoggingManager:
        def get_logger(self, name, config):
            import logging
            return logging.getLogger(name)
    
    class LoggingConfig:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

try:
    from agent_factory_architecture import (
        BaseAgent, AgentTemplate, AgentFactoryConfig
    )
except ImportError:
    # Fallback pour les tests
    class BaseAgent:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    
    class AgentTemplate:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
        
        @classmethod
        def from_dict(cls, data):
            return cls(**data)
        
        def to_dict(self):
            return self.__dict__
    
    class AgentFactoryConfig:
        def __init__(self, templates_dir="./templates"):
            self.templates_dir = Path(templates_dir)


@dataclass
class TemplateMetrics:
    """Métriques de performance étendues pour les templates avec ChatGPT"""
    loads_count: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    reload_count: int = 0
    creation_times: List[float] = field(default_factory=list)
    errors: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    last_accessed: Dict[str, datetime] = field(default_factory=dict)
    
    # Nouvelles métriques ChatGPT
    template_versions: Dict[str, str] = field(default_factory=dict)
    creation_by_template: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    average_creation_time_by_template: Dict[str, float] = field(default_factory=dict)
    memory_usage: Dict[str, int] = field(default_factory=dict)
    namespace_usage: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    @property
    def hit_rate(self) -> float:
        """Calcule le taux de cache hit"""
        total = self.cache_hits + self.cache_misses
        return (self.cache_hits / total * 100) if total > 0 else 0.0
    
    @property
    def avg_creation_time(self) -> float:
        """Temps moyen de création d'agent"""
        return sum(self.creation_times) / len(self.creation_times) if self.creation_times else 0.0


def measure_performance(func: Callable) -> Callable:
    """Décorateur pour mesurer les performances"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        try:
            result = func(self, *args, **kwargs)
            execution_time = time.time() - start_time
            self._metrics.creation_times.append(execution_time)
            return result
        except Exception as e:
            self._metrics.errors[type(e).__name__] += 1
            raise
    return wrapper


class TemplateFileWatcher:
    """Surveillant de fichiers pour hot reload"""
    
    def __init__(self, manager):
        self.manager = manager
    
    def on_modified(self, event):
        """Gestionnaire de modification de fichier"""
        if not event.is_directory and event.src_path.endswith('.json'):
            template_name = Path(event.src_path).stem
            try:
                self.manager.reload_template(template_name)
            except Exception as e:
                self.manager.logger.error(f"Erreur reload template {template_name}: {e}")


class TemplateManagerIntegrated:
    """Gestionnaire de templates intégré avec logging centralisé ChatGPT"""
    
    def __init__(
        self,
        config: Optional[AgentFactoryConfig] = None,
        enable_hot_reload: bool = True,
        preload_templates: Optional[List[str]] = None,
        enable_versioning: bool = True,
        enable_namespace: bool = True
    ):
        # Configuration
        self.config = config or AgentFactoryConfig()
        self._enable_hot_reload = enable_hot_reload and ADVANCED_FEATURES
        self._enable_versioning = enable_versioning
        self._enable_namespace = enable_namespace
        
        # Cache et état
        self._cache: Dict[str, AgentTemplate] = {}
        self._timestamps: Dict[str, float] = {}
        self._template_versions: Dict[str, Dict[str, str]] = {}
        self._namespaces: Dict[str, Set[str]] = defaultdict(set)
        self._lock = threading.RLock()
        
        # Métriques NextGeneration enrichies
        self._metrics = TemplateMetrics()
        
        # Logging centralisé ChatGPT
        logging_config = LoggingConfig(
            logger_name="nextgen.template.manager.chatgpt",
            async_enabled=True,
            performance_mode=True,
            cache_hit=True,
            elasticsearch_enabled=True,
            encryption_enabled=True
        )
        
        self.logger = logging_manager.get_logger(
            "template_manager_integrated",
            logging_config.__dict__
        )
        
        # Initialisation
        self._initialize()
        
        # Préchargement si demandé
        if preload_templates and ADVANCED_FEATURES:
            asyncio.create_task(self._preload_templates(preload_templates))
        
        self.logger.info(
            "TemplateManager ChatGPT initialisé",
            extra={
                "hot_reload": self._enable_hot_reload,
                "versioning": enable_versioning,
                "namespace": enable_namespace,
                "preload_count": len(preload_templates) if preload_templates else 0,
                "advanced_features": ADVANCED_FEATURES
            }
        )
    
    def _initialize(self):
        """Initialisation du gestionnaire"""
        # Créer le dossier templates si nécessaire
        self.config.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration du file watcher
        if self._enable_hot_reload and ADVANCED_FEATURES:
            self._setup_file_watcher()
        
        # Thread de collecte de métriques
        self._start_metrics_thread()
    
    def _setup_file_watcher(self):
        """Configure la surveillance des fichiers"""
        try:
            self._observer = Observer()
            self._file_handler = TemplateFileWatcher(self)
            self._observer.schedule(
                self._file_handler,
                str(self.config.templates_dir),
                recursive=True
            )
            self._observer.start()
            
            self.logger.info(
                "File watcher configuré",
                extra={"templates_dir": str(self.config.templates_dir)}
            )
        except Exception as e:
            self.logger.error(
                "Erreur configuration file watcher",
                extra={"error": str(e)},
                exc_info=True
            )
    
    def _start_metrics_thread(self):
        """Démarre le thread de collecte de métriques"""
        def metrics_collector():
            while True:
                try:
                    time.sleep(60)  # Collecte toutes les minutes
                    self._collect_system_metrics()
                except Exception as e:
                    self.logger.error(f"Erreur collecte métriques: {e}")
        
        metrics_thread = threading.Thread(target=metrics_collector, daemon=True)
        metrics_thread.start()
    
    def _collect_system_metrics(self):
        """Collecte les métriques système"""
        with self._lock:
            # Calcul des moyennes par template
            for template_name in self._cache.keys():
                creation_times = [t for t in self._metrics.creation_times[-100:]]
                if creation_times:
                    self._metrics.average_creation_time_by_template[template_name] = sum(creation_times) / len(creation_times)
    
    def _calculate_template_hash(self, template: AgentTemplate) -> str:
        """Calcule un hash unique pour un template"""
        template_str = json.dumps(template.to_dict(), sort_keys=True)
        return hashlib.sha256(template_str.encode()).hexdigest()
    
    async def _preload_templates(self, template_names: List[str]):
        """Précharge des templates de manière asynchrone"""
        if not ADVANCED_FEATURES:
            return
        
        for template_name in template_names:
            try:
                await self._load_template_async(template_name)
            except Exception as e:
                self.logger.error(f"Erreur préchargement {template_name}: {e}")
    
    async def _load_template_async(self, template_name: str) -> Optional[AgentTemplate]:
        """Charge un template de manière asynchrone"""
        if not ADVANCED_FEATURES:
            return self._load_template(template_name)
        
        try:
            template_path = self.config.templates_dir / f"{template_name}.json"
            
            async with aiofiles.open(template_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                data = json.loads(content)
                
            template = AgentTemplate.from_dict(data)
            
            with self._lock:
                self._cache[template_name] = template
                self._timestamps[template_name] = time.time()
                self._metrics.loads_count += 1
                
            return template
            
        except Exception as e:
            self.logger.error(
                "Erreur chargement asynchrone du template",
                extra={
                    "template": template_name,
                    "error": str(e)
                },
                exc_info=True
            )
            return None
    
    @measure_performance
    def get_template(self, template_name: str, version: Optional[str] = None) -> AgentTemplate:
        """Obtient un template avec support du versioning"""
        with self._lock:
            # Si version spécifiée et versioning activé
            if self._enable_versioning and version and version != "latest":
                versioned_name = f"{template_name}@{version}"
                if versioned_name in self._cache:
                    self._metrics.cache_hits += 1
                    self._metrics.last_accessed[template_name] = datetime.now()
                    return self._cache[versioned_name]
            
            # Version courante
            if template_name in self._cache:
                self._metrics.cache_hits += 1
                self._metrics.last_accessed[template_name] = datetime.now()
                return self._cache[template_name]
            
            self._metrics.cache_misses += 1
        
        # Charger le template
        template = self._load_template(template_name)
        
        if template:
            # Calculer l'empreinte mémoire approximative
            import sys
            self._metrics.memory_usage[template_name] = sys.getsizeof(template)
        
        return template
    
    def _load_template(self, template_name: str) -> AgentTemplate:
        """Charge un template depuis le disque avec logging"""
        try:
            self.logger.debug(
                "Chargement du template depuis le disque",
                extra={"template": template_name}
            )
            
            template_path = self.config.templates_dir / f"{template_name}.json"
            
            if not template_path.exists():
                raise FileNotFoundError(f"Template non trouvé: {template_name}")
            
            with open(template_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            template = AgentTemplate.from_dict(data)
            
            with self._lock:
                self._cache[template_name] = template
                self._timestamps[template_name] = time.time()
                self._metrics.loads_count += 1
                
                # Versioning
                if self._enable_versioning:
                    hash_value = self._calculate_template_hash(template)
                    if template_name not in self._template_versions:
                        self._template_versions[template_name] = {}
                    self._template_versions[template_name]["current"] = hash_value
                    self._metrics.template_versions[template_name] = hash_value[:8]
            
            self.logger.info(
                "Template chargé avec succès",
                extra={
                    "template": template_name,
                    "size_bytes": template_path.stat().st_size,
                    "version": self._metrics.template_versions.get(template_name, "N/A")
                }
            )
            
            return template
            
        except Exception as e:
            self._metrics.errors[type(e).__name__] += 1
            self.logger.error(
                "Erreur chargement template",
                extra={
                    "template": template_name,
                    "error": str(e)
                },
                exc_info=True
            )
            raise
    
    def reload_template(self, template_name: str):
        """Recharge un template depuis le disque"""
        try:
            old_hash = None
            if self._enable_versioning and template_name in self._template_versions:
                old_hash = self._template_versions[template_name].get("current")
            
            # Recharger le template
            template = self._load_template(template_name)
            new_hash = self._calculate_template_hash(template)
            
            with self._lock:
                self._metrics.reload_count += 1
            
            if self._enable_versioning:
                if template_name not in self._template_versions:
                    self._template_versions[template_name] = {}
                self._template_versions[template_name]["current"] = new_hash
                
                # Archiver l'ancienne version
                if old_hash and old_hash != new_hash:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    self._template_versions[template_name][f"backup_{timestamp}"] = old_hash
            
            if old_hash != new_hash:
                self.logger.info(
                    "Template rechargé avec nouvelle version",
                    extra={
                        "template": template_name,
                        "old_version": old_hash[:8] if old_hash else "N/A",
                        "new_version": new_hash[:8],
                        "version_changed": old_hash != new_hash
                    }
                )
            
        except Exception as e:
            self.logger.error(
                "Erreur lors du rechargement du template",
                extra={
                    "template": template_name,
                    "error": str(e)
                },
                exc_info=True
            )
            self._metrics.errors["reload_error"] += 1
    
    @measure_performance
    def create_agent(
        self,
        template_name: str,
        *,
        suffix: str = "",
        config: Optional[Dict[str, Any]] = None,
        namespace: Optional[str] = None,
        version: Optional[str] = None
    ) -> BaseAgent:
        """Crée un agent basé sur un template avec support ChatGPT"""
        start_time = time.time()
        
        try:
            # Obtenir le template
            template = self.get_template(template_name, version)
            
            # Configuration de l'agent
            agent_config = template.to_dict().copy()
            if config:
                agent_config.update(config)
            
            # Namespace
            if self._enable_namespace and namespace:
                with self._lock:
                    self._namespaces[namespace].add(template_name)
                    self._metrics.namespace_usage[namespace] += 1
                agent_config["namespace"] = namespace
            
            # Suffix pour nom unique
            if suffix:
                agent_config["name"] = f"{agent_config.get('name', template_name)}_{suffix}"
            
            # Créer l'agent
            agent = BaseAgent(**agent_config)
            
            # Métriques
            creation_time = time.time() - start_time
            with self._lock:
                self._metrics.creation_by_template[template_name] += 1
                self._metrics.creation_times.append(creation_time)
            
            self.logger.info(
                "Agent créé avec succès",
                extra={
                    "template": template_name,
                    "agent_name": agent_config.get("name"),
                    "namespace": namespace,
                    "version": version,
                    "creation_time": creation_time
                }
            )
            
            return agent
            
        except Exception as e:
            self.logger.error(
                "Erreur création agent",
                extra={
                    "template": template_name,
                    "namespace": namespace,
                    "error": str(e)
                },
                exc_info=True
            )
            raise
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques détaillées avec améliorations ChatGPT"""
        with self._lock:
            # Métriques de base
            core_metrics = {
                "performance": {
                    "total_loads": self._metrics.loads_count,
                    "cache_hits": self._metrics.cache_hits,
                    "cache_misses": self._metrics.cache_misses,
                    "hit_rate": f"{self._metrics.hit_rate:.2f}%",
                    "reload_count": self._metrics.reload_count,
                    "avg_creation_time": f"{self._metrics.avg_creation_time:.3f}s"
                },
                "cache": {
                    "size": len(self._cache),
                    "templates": list(self._cache.keys())
                },
                "errors": dict(self._metrics.errors)
            }
            
            # Améliorations ChatGPT
            chatgpt_enhancements = {
                "advanced_features": {
                    "async_logging_agents": sum(1 for t in self._cache.keys() if "async" in t.lower()),
                    "centralized_logging_agents": len([t for t in self._cache.keys() if "logging" in t.lower()]),
                    "performance_optimized_agents": sum(1 for t in self._cache.keys() if "perf" in t.lower() or "optim" in t.lower())
                },
                "namespace_analytics": {
                    "total_namespaces": len(self._namespaces),
                    "templates_per_namespace": {ns: len(templates) for ns, templates in self._namespaces.items()},
                    "avg_templates_per_namespace": sum(len(templates) for templates in self._namespaces.values()) / len(self._namespaces) if self._namespaces else 0,
                    "most_used_namespace": max(self._metrics.namespace_usage.items(), key=lambda x: x[1])[0] if self._metrics.namespace_usage else None
                },
                "version_analytics": {
                    "versioned_templates": len(self._template_versions),
                    "total_versions": sum(len(versions) for versions in self._template_versions.values()),
                    "templates_with_backups": len([t for t, v in self._template_versions.items() if any("backup" in k for k in v.keys())])
                },
                "performance_insights": {
                    "fastest_template": min(self._metrics.average_creation_time_by_template.items(), key=lambda x: x[1])[0] if self._metrics.average_creation_time_by_template else None,
                    "slowest_template": max(self._metrics.average_creation_time_by_template.items(), key=lambda x: x[1])[0] if self._metrics.average_creation_time_by_template else None,
                    "most_used_template": max(self._metrics.creation_by_template.items(), key=lambda x: x[1])[0] if self._metrics.creation_by_template else None,
                    "cache_efficiency": f"{self._metrics.hit_rate:.2f}%",
                    "memory_usage_mb": sum(self._metrics.memory_usage.values()) / (1024*1024) if self._metrics.memory_usage else 0
                }
            }
            
            return {
                "core_metrics": core_metrics,
                "chatgpt_enhancements": chatgpt_enhancements,
                "timestamp": datetime.now().isoformat(),
                "advanced_features_enabled": ADVANCED_FEATURES
            }
    
    def list_templates(self, namespace: Optional[str] = None) -> List[str]:
        """Liste tous les templates disponibles avec support des namespaces"""
        try:
            templates = []
            
            # Si namespace spécifié
            if self._enable_namespace and namespace:
                with self._lock:
                    templates = list(self._namespaces.get(namespace, set()))
                
                self.logger.debug(
                    "Liste des templates par namespace",
                    extra={
                        "namespace": namespace,
                        "count": len(templates)
                    }
                )
            else:
                # Lister tous les templates
                template_files = self.config.templates_dir.glob("*.json")
                templates = [f.stem for f in template_files]
                
                self.logger.debug(
                    "Liste de tous les templates",
                    extra={"count": len(templates)}
                )
            
            return sorted(templates)
            
        except Exception as e:
            self.logger.error(
                "Erreur lors de la liste des templates",
                extra={"namespace": namespace},
                exc_info=True
            )
            return []
    
    def get_namespaces(self) -> List[str]:
        """Retourne la liste des namespaces"""
        if not self._enable_namespace:
            return []
        
        with self._lock:
            return sorted(list(self._namespaces.keys()))
    
    def get_template_versions(self, template_name: str) -> Dict[str, str]:
        """Retourne l'historique des versions d'un template"""
        if not self._enable_versioning:
            return {}
        
        return self._template_versions.get(template_name, {})
    
    def health_check(self) -> Dict[str, Any]:
        """Vérification de santé du gestionnaire"""
        try:
            return {
                "status": "healthy",
                "cache_size": len(self._cache),
                "templates_dir_exists": self.config.templates_dir.exists(),
                "hot_reload_active": hasattr(self, '_observer') and self._observer.is_alive() if hasattr(self, '_observer') else False,
                "advanced_features": ADVANCED_FEATURES,
                "metrics": {
                    "total_loads": self._metrics.loads_count,
                    "hit_rate": f"{self._metrics.hit_rate:.2f}%",
                    "errors": len(self._metrics.errors)
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def shutdown(self):
        """Arrêt propre du gestionnaire"""
        try:
            if hasattr(self, '_observer') and self._observer.is_alive():
                self._observer.stop()
                self._observer.join()
            
            self.logger.info("TemplateManager arrêté proprement")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'arrêt: {e}")


# Alias pour compatibilité
TemplateManager = TemplateManagerIntegrated


def create_template_manager(
    config: Optional[AgentFactoryConfig] = None,
    **kwargs
) -> TemplateManagerIntegrated:
    """Factory function pour créer un TemplateManager"""
    return TemplateManagerIntegrated(config, **kwargs)


if __name__ == "__main__":
    # Test rapide
    manager = TemplateManagerIntegrated()
    print("✅ TemplateManager ChatGPT initialisé avec succès")
    print(f"📊 Métriques: {manager.get_metrics()}")
    print(f"🏥 Health check: {manager.health_check()}")
    manager.shutdown()



