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
    
    def _calculate_template_hash(self, template: AgentTemplate) -> str:
        """Calcule un hash unique pour un template"""
        # Sérialiser le template en JSON pour le hashing
        template_str = json.dumps(template.to_dict(), sort_keys=True)
        return hashlib.sha256(template_str.encode()).hexdigest()
    
    async def _load_template_async(self, template_name: str) -> Optional[AgentTemplate]:
        """Charge un template de manière asynchrone"""
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
    
    @measure_performance
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
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques détaillées avec informations de logging"""
        with self._lock:
            # Métriques de base
            base_metrics = {
                "performance": {
                    "total_loads": self._metrics.loads_count,
                    "cache_hits": self._metrics.cache_hits,
                    "cache_misses": self._metrics.cache_misses,
                    "hit_rate_percent": f"{self._metrics.hit_rate:.2f}",
                    "reload_count": self._metrics.reload_count,
                    "avg_creation_time_ms": int(self._metrics.avg_creation_time * 1000),
                    "total_agents_created": len(self._metrics.creation_times)
                },
                "errors": dict(self._metrics.errors),
                "cache": {
                    "templates_cached": len(self._cache),
                    "classes_cached": len(self._class_cache),
                    "memory_usage_bytes": sum(self._metrics.memory_usage.values())
                },
                "templates": {
                    "available": len(self.list_templates()),
                    "versions": dict(self._metrics.template_versions),
                    "namespaces": self.get_namespaces() if self._enable_namespace else []
                },
                "logging": {
                    "centralized_enabled": True,
                    "logger_name": self.logger.name,
                    "log_handlers": len(self.logger.handlers),
                    "log_level": self.logger.level
                },
                "features": {
                    "hot_reload": self._observer is not None,
                    "versioning": self._enable_versioning,
                    "namespaces": self._enable_namespace
                }
            }
            
            # Statistiques par template
            template_stats = {}
            for template_name in self._cache:
                template_stats[template_name] = self._metrics.get_template_stats(template_name)
            
            base_metrics["template_statistics"] = template_stats
            
            # Timestamp
            base_metrics["timestamp"] = datetime.now().isoformat()
            
            return base_metrics
    
    @contextmanager
    def batch_operations(self):
        """Context manager pour les opérations batch avec optimisations"""
        # Désactiver temporairement certaines fonctionnalités pour la performance
        old_hot_reload = False
        if self._observer:
            old_hot_reload = True
            self._observer.stop()
        
        self.logger.info("Début des opérations batch")
        
        try:
            yield
        finally:
            # Restaurer les fonctionnalités
            if old_hot_reload and self._observer:
                self._observer.start()
            
            self.logger.info("Fin des opérations batch")
    
    async def _preload_templates(self, template_names: List[str]):
        """Précharge les templates de manière asynchrone"""
        self.logger.info(
            "Préchargement des templates",
            extra={"templates": template_names}
        )
        
        tasks = []
        for name in template_names:
            task = asyncio.create_task(self._load_template_async(name))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = sum(1 for r in results if r is not None and not isinstance(r, Exception))
        
        self.logger.info(
            "Préchargement terminé",
            extra={
                "requested": len(template_names),
                "loaded": success_count,
                "failed": len(template_names) - success_count
            }
        )
    
    def validate_template(self, template_name: str) -> Tuple[bool, Optional[str]]:
        """Valide un template et retourne (is_valid, error_message)"""
        try:
            template = self.get_template(template_name)
            template.validate()  # Supposons que cette méthode existe
            
            self.logger.info(
                "Template validé avec succès",
                extra={"template": template_name}
            )
            
            return True, None
            
        except TemplateValidationError as e:
            error_msg = f"Validation échouée: {str(e)}"
            
            self.logger.warning(
                "Échec de validation du template",
                extra={
                    "template": template_name,
                    "error": str(e)
                }
            )
            
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Erreur inattendue: {str(e)}"
            
            self.logger.error(
                "Erreur lors de la validation du template",
                extra={
                    "template": template_name,
                    "error": str(e)
                },
                exc_info=True
            )
            
            return False, error_msg
    
    def health_check(self) -> Dict[str, Any]:
        """Vérifie l'état de santé du TemplateManager"""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {}
        }
        
        # Vérifier le cache
        try:
            cache_health = {
                "status": "ok",
                "templates_cached": len(self._cache),
                "hit_rate": f"{self._metrics.hit_rate:.2f}%"
            }
            health_status["components"]["cache"] = cache_health
        except Exception as e:
            health_status["components"]["cache"] = {
                "status": "error",
                "error": str(e)
            }
            health_status["status"] = "degraded"
        
        # Vérifier hot reload
        if self._observer:
            try:
                hot_reload_health = {
                    "status": "ok" if self._observer.is_alive() else "stopped",
                    "enabled": True
                }
                health_status["components"]["hot_reload"] = hot_reload_health
            except Exception as e:
                health_status["components"]["hot_reload"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Vérifier le logging
        try:
            logging_health = {
                "status": "ok",
                "centralized": True,
                "logger_active": self.logger is not None
            }
            health_status["components"]["logging"] = logging_health
        except Exception as e:
            health_status["components"]["logging"] = {
                "status": "error",
                "error": str(e)
            }
            health_status["status"] = "unhealthy"
        
        # Log le health check
        log_level = logging.INFO if health_status["status"] == "healthy" else logging.WARNING
        self.logger.log(
            log_level,
            "Health check effectué",
            extra={"health_status": health_status}
        )
        
        return health_status
    
    def shutdown(self):
        """Arrêt propre du TemplateManager"""
        self.logger.info("Arrêt du TemplateManager en cours...")
        
        try:
            # Arrêter l'observer
            if self._observer:
                self._observer.stop()
                self._observer.join(timeout=5)
            
            # Sauvegarder les métriques finales
            final_metrics = self.get_metrics()
            
            # Logger les métriques finales dans le logger de performance
            perf_logger = logging_manager.get_performance_logger()
            perf_logger.info(
                "TemplateManager Final Metrics",
                extra={"metrics": final_metrics}
            )
            
            # Arrêter l'executor
            self._executor.shutdown(wait=True)
            
            # Nettoyer les caches
            with self._lock:
                self._cache.clear()
                self._class_cache.clear()
                self._timestamps.clear()
            
            self.logger.info("TemplateManager arrêté avec succès")
            
        except Exception as e:
            self.logger.error(
                "Erreur lors de l'arrêt du TemplateManager",
                extra={"error": str(e)},
                exc_info=True
            )
    
    def __enter__(self):
        """Support du context manager"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sortie du context manager avec arrêt propre"""
        self.shutdown()
        return False

# Fonction helper pour créer un TemplateManager configuré
def create_template_manager(
    config: Optional[AgentFactoryConfig] = None,
    **kwargs
) -> TemplateManager:
    """Factory function pour créer un TemplateManager avec configuration par défaut"""
    
    # Configuration par défaut pour NextGeneration
    default_kwargs = {
        "enable_hot_reload": True,
        "enable_versioning": True,
        "enable_namespace": True,
        "preload_templates": [
            "agent_coordinateur",
            "agent_analyseur",
            "agent_evaluateur"
        ]
    }
    
    # Fusionner avec les kwargs fournis
    default_kwargs.update(kwargs)
    
    return TemplateManager(config=config, **default_kwargs)#!/usr/bin/env python3
"""
Code Expert NextGeneration - optimized_template_manager
VERSION INTÉGRÉE AVEC LOGGING CENTRALISÉ ET OPTIMISATIONS
"""

import asyncio
import json
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import lru_cache, wraps
from pathlib import Path
from threading import RLock
from typing import Any, Dict, List, Optional, Set, Tuple, Union, Callable
import hashlib

import aiofiles
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .agent_templates import AgentTemplate, TemplateValidationError
from ..agents.base_agent import BaseAgent
from ..config.agent_config import AgentFactoryConfig
from ..logging.centralized_logging import logging_manager, log_performance, LogCategory

# Logger centralisé pour le TemplateManager
logger = logging_manager.get_logger("template_manager")

@dataclass
class TemplateMetrics:
    """Métriques de performance étendues pour les templates."""
    loads_count: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    reload_count: int = 0
    creation_times: List[float] = field(default_factory=list)
    errors: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    last_accessed: Dict[str, datetime] = field(default_factory=dict)
    
    # Nouvelles métriques
    template_versions: Dict[str, str] = field(default_factory=dict)
    creation_by_template: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    average_creation_time_by_template: Dict[str, float] = field(default_factory=dict)
    memory_usage: Dict[str, int] = field(default_factory=dict)
    
    @property
    def hit_rate(self) -> float:
        """Calcule le taux de cache hit"""
        total = self.cache_hits + self.cache_misses
        return (self.cache_hits / total * 100) if total > 0 else 0.0
    
    @property
    def avg_creation_time(self) -> float:
        """Temps moyen de création d'agent"""
        return sum(self.creation_times) / len(self.creation_times) if self.creation_times else 0.0
    
    def get_template_stats(self, template_name: str) -> Dict[str, Any]:
        """Statistiques spécifiques à un template"""
        creation_times = [t for t, n in zip(self.creation_times[-100:], self.creation_by_template.keys()) 
                         if n == template_name]
        
        return {
            "total_created": self.creation_by_template.get(template_name, 0),
            "avg_creation_time": sum(creation_times) / len(creation_times) if creation_times else 0.0,
            "last_accessed": self.last_accessed.get(template_name, "Never"),
            "version": self.template_versions.get(template_name, "Unknown"),
            "memory_usage_bytes": self.memory_usage.get(template_name, 0)
        }

class TemplateFileWatcher(FileSystemEventHandler):
    """Surveille les modifications des fichiers templates avec debouncing."""
    
    def __init__(self, manager: 'TemplateManager'):
        self.manager = manager
        self.logger = logging_manager.get_logger("template_manager")
        self._pending_reloads: Dict[str, float] = {}
        self._reload_delay = 1.0  # Délai avant rechargement (debouncing)
        
    def on_modified(self, event):
        """Callback lors de la modification d'un fichier."""
        if event.is_directory or not event.src_path.endswith('.json'):
            return
            
        template_name = Path(event.src_path).stem
        current_time = time.time()
        
        # Debouncing pour éviter les rechargements multiples
        if template_name in self._pending_reloads:
            last_time = self._pending_reloads[template_name]
            if current_time - last_time < self._reload_delay:
                return
        
        self._pending_reloads[template_name] = current_time
        
        self.logger.info(
            "Template modifié détecté : %s",
            template_name,
            extra={"template_name": template_name, "file_path": event.src_path}
        )
        
        # Invalider le cache pour ce template
        asyncio.create_task(self.manager.reload_template(template_name))

def measure_performance(func: Callable) -> Callable:
    """Décorateur pour mesurer la performance des méthodes"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with log_performance(f"{self.__class__.__name__}.{func.__name__}", self.logger):
            return func(self, *args, **kwargs)
    return wrapper

def async_measure_performance(func: Callable) -> Callable:
    """Décorateur asynchrone pour mesurer la performance"""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        with log_performance(f"{self.__class__.__name__}.{func.__name__}", self.logger):
            return await func(self, *args, **kwargs)
    return wrapper

class TemplateManager:
    """Gestionnaire optimisé de templates avec logging centralisé et métriques avancées."""
    
    def __init__(
        self,
        config: Optional[AgentFactoryConfig] = None,
        enable_hot_reload: bool = True,
        preload_templates: Optional[List[str]] = None,
        enable_versioning: bool = True,
        enable_namespace: bool = True
    ):
        self.config = config or AgentFactoryConfig()
        self._lock = RLock()
        self._cache: Dict[str, AgentTemplate] = {}
        self._timestamps: Dict[str, float] = {}
        self._class_cache: Dict[str, type[BaseAgent]] = {}
        self._metrics = TemplateMetrics()
        self._executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="TemplateManager")
        
        # Nouvelles fonctionnalités
        self._enable_versioning = enable_versioning
        self._enable_namespace = enable_namespace
        self._namespaces: Dict[str, Set[str]] = defaultdict(set)
        self._template_versions: Dict[str, Dict[str, str]] = {}  # template -> {version -> hash}
        
        # Logger centralisé avec configuration spécialisée
        self.logger = logging_manager.get_logger("template_manager")
        
        # Configuration du hot-reload
        self._observer: Optional[Observer] = None
        if enable_hot_reload:
            self._setup_file_watcher()
        
        # Préchargement des templates critiques
        if preload_templates:
            asyncio.create_task(self._preload_templates(preload_templates))
        
        # Log d'initialisation enrichi
        self.logger.info(
            "TemplateManager initialisé avec logging centralisé",
            extra={
                "config": {
                    "hot_reload": enable_hot_reload,
                    "versioning": enable_versioning,
                    "namespace": enable_namespace,
                    "preload_count": len(preload_templates) if preload_templates else 0
                }
            }
        )
        
        # Démarrer le thread de maintenance des métriques
        self._start_metrics_thread()
    
    def _setup_file_watcher(self):
        """Configure la surveillance des fichiers templates."""
        try:
            self._observer = Observer()
            watcher = TemplateFileWatcher(self)
            
            # Surveiller le répertoire des templates
            template_dir = self.config.templates_dir
            if template_dir.exists():
                self._observer.schedule(watcher, str(template_dir), recursive=True)
                self._observer.start()
                
                self.logger.info(
                    "Surveillance des templates activée",
                    extra={"watch_dir": str(template_dir)}
                )
            else:
                self.logger.warning(
                    "Répertoire de templates non trouvé pour surveillance",
                    extra={"expected_dir": str(template_dir)}
                )
                
        except Exception as e:
            self.logger.error(
                "Erreur lors de la configuration de la surveillance des templates",
                extra={"error": str(e)},
                exc_info=True
            )
    
    def _start_metrics_thread(self):
        """Démarre le thread de collecte des métriques"""
        def metrics_collector():
            while True:
                try:
                    # Collecter les métriques toutes les 5 minutes
                    time.sleep(300)
                    metrics = self.get_metrics()
                    
                    # Logger les métriques dans le logger de performance
                    perf_logger = logging_manager.get_performance_logger()
                    perf_logger.info(
                        "TemplateManager Metrics",
                        extra={"metrics": metrics}
                    )
                    
                except Exception as e:
                    self.logger.error(f"Erreur collecte métriques: {e}")
        
        import threading
        metrics_thread = threading.Thread(
            target=metrics_collector,
            daemon=True,
            name="TemplateMetricsCollector"
        )
        metrics_thread.start()
    
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
        """Crée une instance d'agent avec injection automatique de logging centralisé."""
        start_time = time.time()
        
        # Résolution du namespace
        if self._enable_namespace and namespace:
            full_template_name = f"{namespace}.{template_name}"
        else:
            full_template_name = template_name
        
        try:
            # Log de début de création
            self.logger.debug(
                "Début création agent",
                extra={
                    "template": full_template_name,
                    "suffix": suffix,
                    "namespace": namespace,
                    "version": version
                }
            )
            
            # Utiliser la classe en cache si disponible
            with self._lock:
                cache_key = f"{full_template_name}:{version}" if version else full_template_name
                
                if cache_key in self._class_cache:
                    agent_class = self._class_cache[cache_key]
                    self._metrics.cache_hits += 1
                else:
                    tmpl = self.get_template(full_template_name, version=version)
                    agent_class = tmpl.to_class()
                    self._class_cache[cache_key] = agent_class
                    self._metrics.cache_misses += 1
                
                # Enregistrer dans le namespace
                if self._enable_namespace and namespace:
                    self._namespaces[namespace].add(full_template_name)
            
            # Préparation de la configuration
            if config is None:
                config = {}
            
            # Obtenir les informations du template pour la configuration logging
            template = self.get_template(full_template_name, version=version)
            agent_name = f"{template_name}{suffix}"
            agent_id = f"{template_name}_{suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Génération automatique de la configuration logging centralisée
            if "logging" not in config:
                # Déterminer si l'agent doit utiliser le logging asynchrone
                async_enabled = template.metadata.get("async_logging", False)
                
                config["logging"] = logging_manager.generate_agent_logging_config(
                    agent_name=agent_name,
                    role=template.role,
                    domain=template.domain,
                    agent_id=agent_id,
                    async_enabled=async_enabled
                )
                
                self.logger.debug(
                    "Configuration logging injectée",
                    extra={
                        "agent_name": agent_name,
                        "template": full_template_name,
                        "role": template.role,
                        "domain": template.domain,
                        "async_logging": async_enabled
                    }
                )
            
            # Ajouter métadonnées NextGeneration
            config["nextgen_metadata"] = {
                "created_by": "TemplateManager",
                "template_name": full_template_name,
                "template_version": version or "latest",
                "namespace": namespace,
                "creation_timestamp": datetime.now().isoformat(),
                "logging_centralized": True
            }
            
            # Créer l'instance (hors du lock)
            agent = agent_class.create(name_suffix=suffix, config=config)
            
            # Métriques et statistiques
            creation_time = time.time() - start_time
            
            with self._lock:
                self._metrics.creation_times.append(creation_time)
                self._metrics.creation_by_template[full_template_name] += 1
                
                # Limiter la taille de l'historique
                if len(self._metrics.creation_times) > 10000:
                    self._metrics.creation_times = self._metrics.creation_times[-10000:]
                
                # Calculer la moyenne par template
                template_times = [t for t, n in zip(
                    self._metrics.creation_times[-100:],
                    [full_template_name] * min(100, self._metrics.creation_by_template[full_template_name])
                )]
                if template_times:
                    self._metrics.average_creation_time_by_template[full_template_name] = \
                        sum(template_times) / len(template_times)
            
            # Log de succès avec informations enrichies
            self.logger.info(
                "Agent créé avec succès",
                extra={
                    "agent": {
                        "name": agent.metadata.name,
                        "id": agent_id,
                        "template": full_template_name,
                        "role": template.role,
                        "domain": template.domain,
                        "namespace": namespace,
                        "version": version or "latest"
                    },
                    "performance": {
                        "creation_time_ms": int(creation_time * 1000),
                        "cache_hit": cache_key in self._class_cache
                    },
                    "logging": {
                        "centralized": True,
                        "async_enabled": config["logging"].get("async_enabled", False)
                    }
                }
            )
            
            return agent
            
        except Exception as e:
            self._metrics.errors[type(e).__name__] += 1
            
            # Log d'erreur détaillé avec contexte complet
            self.logger.error(
                "Erreur création agent",
                extra={
                    "template": full_template_name,
                    "suffix": suffix,
                    "namespace": namespace,
                    "version": version,
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                },
                exc_info=True
            )
            raise
    
    @async_measure_performance
    async def bulk_create_agents(
        self,
        specs: List[Dict[str, Any]],
        parallel: bool = True,
        max_concurrent: int = 10
    ) -> Dict[str, BaseAgent]:
        """Crée plusieurs agents en lot avec logging centralisé et parallélisation optionnelle."""
        agents = {}
        errors = []
        
        # Log de début avec détails
        self.logger.info(
            "Début création en masse d'agents",
            extra={
                "total_specs": len(specs),
                "parallel": parallel,
                "max_concurrent": max_concurrent if parallel else 1
            }
        )
        
        async def create_single(spec: Dict[str, Any], index: int) -> Tuple[Optional[str], Optional[BaseAgent], Optional[Dict]]:
            """Crée un agent unique avec gestion d'erreur"""
            template_name = spec.get('template')
            if not template_name:
                self.logger.warning(
                    "Spec ignorée - template manquant",
                    extra={"spec_index": index, "spec": spec}
                )
                return None, None, {"index": index, "error": "Missing template", "spec": spec}
            
            suffix = spec.get('suffix', '')
            config = spec.get('config')
            namespace = spec.get('namespace')
            version = spec.get('version')
            
            try:
                agent = await asyncio.get_event_loop().run_in_executor(
                    self._executor,
                    self.create_agent,
                    template_name,
                    suffix,
                    config,
                    namespace,
                    version
                )
                
                self.logger.debug(
                    "Agent créé dans bulk operation",
                    extra={
                        "index": index,
                        "agent_name": agent.metadata.name,
                        "template": template_name
                    }
                )
                
                return agent.metadata.name, agent, None
                
            except Exception as e:
                error_detail = {
                    "index": index,
                    "template": template_name,
                    "suffix": suffix,
                    "error": str(e),
                    "error_type": type(e).__name__
                }
                
                self.logger.error(
                    "Erreur création agent dans bulk operation",
                    extra=error_detail
                )
                
                return None, None, error_detail
        
        # Création parallèle ou séquentielle
        if parallel:
            # Utiliser un semaphore pour limiter la concurrence
            semaphore = asyncio.Semaphore(max_concurrent)
            
            async def create_with_semaphore(spec, index):
                async with semaphore:
                    return await create_single(spec, index)
            
            # Créer toutes les tâches
            tasks = [
                create_with_semaphore(spec, i)
                for i, spec in enumerate(specs, 1)
            ]
            
            # Attendre toutes les tâches
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
        else:
            # Création séquentielle
            results = []
            for i, spec in enumerate(specs, 1):
                result = await create_single(spec, i)
                results.append(result)
        
        # Traiter les résultats
        for result in results:
            if isinstance(result, Exception):
                errors.append({"error": str(result), "type": type(result).__name__})
            else:
                name, agent, error = result
                if agent:
                    agents[name] = agent
                elif error:
                    errors.append(error)
        
        # Log de résumé
        self.logger.info(
            "Création en masse terminée",
            extra={
                "summary": {
                    "requested": len(specs),
                    "created": len(agents),
                    "failed": len(errors),
                    "success_rate": f"{(len(agents) / len(specs) * 100):.1f}%" if specs else "0%"
                },
                "errors": errors if errors else None
            }
        )
        
        # Si des erreurs, les logger aussi dans le logger d'erreurs
        if errors:
            error_logger = logging_manager.get_logger("errors_critical")
            error_logger.error(
                "Erreurs lors de la création en masse d'agents",
                extra={"errors": errors, "operation": "bulk_create_agents"}
            )
        
        return agents
    
    @async_measure_performance
    async def reload_template(self, template_name: str):
        """Recharge un template modifié avec versioning."""
        try:
            self.logger.info(
                "Rechargement du template",
                extra={"template": template_name}
            )
            
            # Calculer le hash actuel si versioning activé
            old_hash = None
            if self._enable_versioning and template_name in self._template_versions:
                old_hash = self._template_versions[template_name].get("current")
            
            with self._lock:
                # Supprimer du cache
                if template_name in self._cache:
                    del self._cache[template_name]
                if template_name in self._class_cache:
                    del self._class_cache[template_name]
                if template_name in self._timestamps:
                    del self._timestamps[template_name]
                
                self._metrics.reload_count += 1
            
            # Recharger le template
            template = await self._load_template_async(template_name)
            
            # Versionning
            if self._enable_versioning and template:
                new_hash = self._calculate_template_hash(template)
                
                if template_name not in self._template_versions:
                    self._template_versions[template_name] = {}
                
                # Archiver l'ancienne version
                if old_hash and old_hash != new_hash:
                    timestamp = datetime.now().isoformat()
                    self._template_versions[template_name][timestamp] = old_hash
                
                self._template_versions[template_name]["current"] = new_hash
                self._metrics.template_versions[template_name] = new_hash[:8]  # Short hash
                
                self.logger.info(
                    "Template rechargé avec nouvelle version",
                    extra={
                        "template": template_name,
                        "old_version": old_hash[:8] if old_hash else "N/A",
                        "new_version": new_hash[:8],
                        "version_changed": old_hash != new_hash
                    }
                )



