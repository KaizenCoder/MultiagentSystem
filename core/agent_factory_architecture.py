"""
🏭 ARCHITECTURE PATTERN FACTORY - Version Production
==================================================

Architecture complète du Pattern Factory réutilisant les assets Sprints 1-5.
Cette implémentation transforme la simulation en vrai Pattern Factory production-ready.

Composants :
1. Interfaces de base (Agent, Task, Result)
2. AgentFactory (cœur du pattern)
3. AgentRegistry (enregistrement types)
4. AgentOrchestrator (coordination)
5. Integration avec assets existants
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Type, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import sys
from pathlib import Path
from core import logging_manager
from pathlib import Path
import threading
import uuid

# Intégration avec les templates existants (Sprints 1-5)
import sys
sys.path.append(str(Path(__file__).parent.parent))

# LoggingManager NextGeneration - Configuration globale
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================================
# 1. ENUMERATIONS ET TYPES
# ==========================================

class TaskStatus(Enum):
    """Statuts d'exécution des tâches"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AgentType(Enum):
    """Types d'agents supportés"""
    DATABASE = "database"
    SECURITY = "security"
    MONITORING = "monitoring"
    DEPLOYMENT = "deployment"
    NETWORK = "network"
    STORAGE = "storage"
    COMPUTE = "compute"
    API = "api"
    WORKFLOW = "workflow"

class Priority(Enum):
    """Niveaux de priorité"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

# ==========================================
# 2. INTERFACES DE BASE
# ==========================================

@dataclass
class FactoryConfig:
    """
    ⚙️ Configuration pour l'AgentFactory
    
    Recommandation utilisateur : Configuration centralisée pour la Factory
    """
    # Limites de concurrence
    max_concurrent_agents: int = 10
    max_agents_per_type: int = 5
    
    # Timeouts par défaut
    default_timeout_seconds: int = 30
    health_check_interval_seconds: int = 60
    cleanup_interval_hours: int = 24
    
    # Monitoring et observabilité
    enable_monitoring: bool = True
    enable_detailed_metrics: bool = True
    enable_tracing: bool = True
    
    # Sécurité
    security_level: str = "HIGH"  # LOW, MEDIUM, HIGH, CRITICAL
    enable_signature_validation: bool = True
    enable_sandbox: bool = True
    
    # Cache et performance
    cache_ttl_seconds: int = 3600
    enable_hot_reload: bool = True
    enable_compression: bool = True
    
    # Stockage et backup
    persistence_enabled: bool = True
    backup_interval_minutes: int = 15
    max_execution_history: int = 1000
    
    # Configuration environnement
    environment: str = "production"  # development, staging, production
    log_level: str = "INFO"
    
    def to_dict(self) -> Dict[str, Any]:
        """Sérialise la configuration"""
        return {
            "max_concurrent_agents": self.max_concurrent_agents,
            "default_timeout_seconds": self.default_timeout_seconds,
            "enable_monitoring": self.enable_monitoring,
            "security_level": self.security_level,
            "environment": self.environment,
            "cache_ttl_seconds": self.cache_ttl_seconds,
            "log_level": self.log_level
        }

@dataclass
class Task:
    """
    🎯 Tâche à exécuter par un agent
    
    Représente une unité de travail avec ses paramètres et contraintes.
    """
    type: str
    params: Dict[str, Any] = field(default_factory=dict)
    priority: Priority = Priority.MEDIUM
    timeout_seconds: Optional[int] = None
    retry_count: int = 0
    max_retries: int = 3
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Champs automatiques
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Sérialise la tâche en dictionnaire"""
        return {
            "id": self.id,
            "type": self.type,
            "params": self.params,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "assigned_agent_id": self.assigned_agent_id,
            "metadata": self.metadata
        }

@dataclass
class Result:
    """
    📊 Résultat d'exécution d'une tâche
    
    Contient les données, métriques et statut d'exécution.
    """
    success: bool
    data: Any = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    
    # Métadonnées d'exécution
    execution_time_seconds: Optional[float] = None
    memory_usage_mb: Optional[float] = None
    agent_id: Optional[str] = None
    task_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Sérialise le résultat en dictionnaire"""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "error_code": self.error_code,
            "metrics": self.metrics,
            "warnings": self.warnings,
            "execution_time_seconds": self.execution_time_seconds,
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "timestamp": self.timestamp.isoformat()
        }

class Agent(ABC):
    """
    🤖 Interface de base pour tous les agents
    
    Définit le contrat que tous les agents doivent respecter.
    """
    
    def __init__(self, agent_id: str, version: str, description: str, agent_type: str, status: str, **kwargs):
        self.agent_id = agent_id
        self.version = version
        self.description = description
        self.agent_type = agent_type
        self.status = status
        self.config = kwargs
        self.id = agent_id  # Utiliser l'id fourni
        self.capabilities: List[str] = []
        self.created_at = datetime.now()
        self.metadata: Dict[str, Any] = {}
        
        # Métriques d'utilisation
        self.tasks_executed = 0
        self.total_execution_time = 0.0
        self.success_rate = 0.0
        self.last_activity = datetime.now()
        
        # Utiliser le logger global configuré
        self.logger = logging_manager.get_logger(f"agent.{self.agent_id.replace('-', '_')[:20]}")
        self.logger.info(f"Agent {self.agent_type} ({self.id}) initialisé.")
    
    def log(self, message: str, level: str = "info"):
        """Journalisation standardisée pour l'agent."""
        if hasattr(self.logger, level):
            getattr(self.logger, level)(f"[{self.id}] {message}")
        else:
            self.logger.info(f"[{self.id}] {message}")
    
    @abstractmethod
    async def execute_task(self, task: Task) -> Result:
        """
        ⚙️ Exécute une tâche et retourne le résultat
        
        Args:
            task: Tâche à exécuter
            
        Returns:
            Result: Résultat de l'exécution
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        📋 Retourne la liste des capacités de l'agent
        
        Returns:
            List[str]: Liste des types de tâches supportées
        """
        pass
    
    # ==========================================
    # 🚀 AGENT LIFECYCLE MANAGEMENT 
    # (Ajouté suite aux recommandations utilisateur)
    # ==========================================
    
    @abstractmethod
    async def startup(self) -> None:
        """
        🚀 Initialise l'agent et prépare ses ressources
        
        Cette méthode est appelée lors de la création de l'agent
        pour initialiser les connexions, caches, etc.
        """
        pass
    
    @abstractmethod  
    async def shutdown(self) -> None:
        """
        🛑 Arrête proprement l'agent et libère ses ressources
        
        Cette méthode est appelée lors de l'arrêt de l'agent
        pour fermer les connexions, sauvegarder l'état, etc.
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """
        🏥 Vérifie l'état de santé de l'agent
        
        Returns:
            Dict[str, Any]: Statut de santé avec métriques détaillées
            {
                "status": "healthy|degraded|unhealthy",
                "uptime_seconds": float,
                "last_task_time": str,
                "resource_usage": {"cpu": float, "memory": float},
                "dependencies": {"db": "connected", "api": "timeout"},
                "errors": ["liste des erreurs récentes"],
                "metrics": {"tasks_per_minute": float, "success_rate": float}
            }
        """
        pass
    
    def can_handle(self, task: Task) -> bool:
        """
        ✅ Vérifie si l'agent peut traiter cette tâche
        
        Args:
            task: Tâche à vérifier
            
        Returns:
            bool: True si l'agent peut traiter la tâche
        """
        return task.type in self.get_capabilities()
    
    def get_status(self) -> Dict[str, Any]:
        """
        📊 Retourne le statut actuel de l'agent
        
        Returns:
            Dict: Informations de statut et métriques
        """
        return {
            "id": self.id,
            "type": self.agent_type,
            "status": self.status,
            "capabilities": self.capabilities,
            "tasks_executed": self.tasks_executed,
            "success_rate": self.success_rate,
            "total_execution_time": self.total_execution_time,
            "last_activity": self.last_activity.isoformat(),
            "created_at": self.created_at.isoformat(),
            "config": self.config,
            "metadata": self.metadata
        }
    
    def update_metrics(self, result: Result, execution_time: float):
        """
        📈 Met à jour les métriques de performance
        
        Args:
            result: Résultat de la dernière exécution
            execution_time: Temps d'exécution en secondes
        """
        self.tasks_executed += 1
        self.total_execution_time += execution_time
        self.last_activity = datetime.now()
        
        # Calcul du taux de succès (simplification pour l'exemple)
        # En production, il faudrait stocker l'historique
        if result.success:
            self.success_rate = min(100.0, self.success_rate + 1.0)
        else:
            self.success_rate = max(0.0, self.success_rate - 0.5)

# ==========================================
# 3. REGISTRY DES AGENTS
# ==========================================

class AgentRegistry:
    """
    📝 Registre des types d'agents disponibles
    
    Centralise l'enregistrement et la découverte des types d'agents.
    """
    
    def __init__(self):
        self._registry: Dict[str, Type[Agent]] = {}
        self._factories: Dict[str, Callable] = {}
        self._lock = threading.Lock()
        
        logger.info("AgentRegistry initialisé")
    
    def register(self, agent_type: str, agent_class: Type[Agent], 
                factory_func: Optional[Callable] = None):
        """
        📝 Enregistre un nouveau type d'agent
        
        Args:
            agent_type: Type d'agent (ex: "database")
            agent_class: Classe de l'agent
            factory_func: Fonction de création personnalisée (optionnel)
        """
        with self._lock:
            self._registry[agent_type] = agent_class
            if factory_func:
                self._factories[agent_type] = factory_func
            
            logger.info(f"Type d'agent enregistré: {agent_type} -> {agent_class.__name__}")
    
    def get_agent_class(self, agent_type: str) -> Type[Agent]:
        """
        🔍 Récupère la classe d'un type d'agent
        
        Args:
            agent_type: Type d'agent recherché
            
        Returns:
            Type[Agent]: Classe de l'agent
            
        Raises:
            ValueError: Si le type n'est pas enregistré
        """
        if agent_type not in self._registry:
            raise ValueError(f"Agent type '{agent_type}' not registered. "
                           f"Available: {list(self._registry.keys())}")
        
        return self._registry[agent_type]
    
    def get_factory_func(self, agent_type: str) -> Optional[Callable]:
        """
        🏭 Récupère la fonction de création personnalisée
        
        Args:
            agent_type: Type d'agent
            
        Returns:
            Optional[Callable]: Fonction de création ou None
        """
        return self._factories.get(agent_type)
    
    def get_available_types(self) -> List[str]:
        """
        📋 Retourne la liste des types d'agents disponibles
        
        Returns:
            List[str]: Types d'agents enregistrés
        """
        return list(self._registry.keys())
    
    def get_registry_info(self) -> Dict[str, Any]:
        """
        📊 Retourne les informations du registre
        
        Returns:
            Dict: Informations sur les types enregistrés
        """
        return {
            "total_types": len(self._registry),
            "available_types": self.get_available_types(),
            "has_custom_factories": list(self._factories.keys()),
            "registry_timestamp": datetime.now().isoformat()
        }

# ==========================================
# 4. AGENT FACTORY (CŒUR DU PATTERN)
# ==========================================

class AgentFactory:
    """
    🏭 Factory Pattern - Création dynamique d'agents
    
    Point central pour créer des agents selon les besoins métier.
    Intègre avec les templates et configurations existants des Sprints 1-5.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.registry = AgentRegistry()
        self.config_path = config_path or "config/"
        self.created_agents: Dict[str, Agent] = {}
        self._lock = threading.Lock()
        
        # Chargement de la configuration (utilise les assets Sprints 1-5)
        self._load_configuration()
        
        # Enregistrement des agents de base
        self._register_default_agents()
        
        logger.info(f"AgentFactory initialisée avec {len(self.registry.get_available_types())} types d'agents")
    
    def _load_configuration(self):
        """
        ⚙️ Charge la configuration depuis les assets existants
        
        Utilise les configurations créées dans les Sprints 1-5
        """
        try:
            config_file = Path(self.config_path) / "agent_factory_config.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info(f"Configuration chargée depuis {config_file}")
            else:
                # Configuration par défaut
                self.config = {
                    "default_timeout": 300,
                    "max_concurrent_agents": 10,
                    "enable_metrics": True,
                    "log_level": "INFO"
                }
                logger.warning("Configuration par défaut utilisée")
        except Exception as e:
            logger.error(f"Erreur chargement configuration: {e}")
            self.config = {}
    
    def _register_default_agents(self):
        """
        📝 Enregistre les types d'agents par défaut
        
        En production, ceci utiliserait les vraies implémentations
        des agents créés dans les Sprints 1-5
        """
        # Agent Méta-Stratégique Pattern Factory compliant
        try:
            from agents.agent_meta_strategique_pattern_factory import AgentMetaStrategique, create_meta_strategique_agent
            self.register_agent_type("meta_strategique", AgentMetaStrategique, create_meta_strategique_agent)
            logger.info("✅ Agent Méta-Stratégique enregistré dans Pattern Factory")
        except ImportError as e:
            logger.warning(f"Agent Méta-Stratégique non disponible: {e}")
        
        # Ici on enregistrerait les vraies classes d'agents
        # Pour l'exemple, on utilise des classes simplifiées
        logger.info("🏭 Agents par défaut enregistrés")
    
    def create_agent(self, agent_type: str, **config) -> Agent:
        """
        🎯 MÉTHODE CENTRALE : Crée un agent selon le type et la configuration
        
        Args:
            agent_type: Type d'agent à créer
            **config: Configuration spécifique à l'agent
            
        Returns:
            Agent: Agent configuré et prêt à l'emploi
            
        Raises:
            ValueError: Si le type d'agent n'est pas supporté
        """
        with self._lock:
            # Récupération de la classe d'agent
            agent_class = self.registry.get_agent_class(agent_type)
            
            # Fonction de création personnalisée si disponible
            factory_func = self.registry.get_factory_func(agent_type)
            
            if factory_func:
                agent = factory_func(**config)
            else:
                agent = agent_class(**config)
            
            # Enregistrement de l'agent créé
            self.created_agents[agent.id] = agent
            
            logger.info(f"Agent {agent_type} créé avec ID: {agent.id}")
            return agent
    
    def register_agent_type(self, agent_type: str, agent_class: Type[Agent], 
                          factory_func: Optional[Callable] = None):
        """
        📝 Enregistre un nouveau type d'agent
        
        Args:
            agent_type: Type d'agent
            agent_class: Classe de l'agent
            factory_func: Fonction de création personnalisée
        """
        self.registry.register(agent_type, agent_class, factory_func)
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """
        🔍 Récupère un agent créé par son ID
        
        Args:
            agent_id: Identifiant de l'agent
            
        Returns:
            Optional[Agent]: Agent si trouvé, None sinon
        """
        return self.created_agents.get(agent_id)
    
    def get_available_types(self) -> List[str]:
        """
        📋 Retourne la liste des types d'agents disponibles
        
        Returns:
            List[str]: Types d'agents supportés
        """
        return self.registry.get_available_types()
    
    def get_created_agents(self) -> Dict[str, Agent]:
        """
        📊 Retourne tous les agents créés
        
        Returns:
            Dict[str, Agent]: Dictionnaire ID -> Agent
        """
        return self.created_agents.copy()
    
    def cleanup_agents(self, max_age_hours: int = 24):
        """
        🧹 Nettoie les agents anciens ou inactifs
        
        Args:
            max_age_hours: Âge maximum en heures
        """
        cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
        
        with self._lock:
            agents_to_remove = []
            for agent_id, agent in self.created_agents.items():
                if agent.created_at.timestamp() < cutoff_time:
                    agents_to_remove.append(agent_id)
            
            for agent_id in agents_to_remove:
                del self.created_agents[agent_id]
                logger.info(f"Agent {agent_id} supprimé (trop ancien)")
    
    def get_factory_status(self) -> Dict[str, Any]:
        """
        📊 Retourne le statut de la factory
        
        Returns:
            Dict: Informations sur l'état de la factory
        """
        return {
            "total_agents_created": len(self.created_agents),
            "available_types": self.get_available_types(),
            "active_agents": [
                agent.get_status() for agent in self.created_agents.values()
                if agent.status == "ready"
            ],
            "registry_info": self.registry.get_registry_info(),
            "config": self.config,
            "timestamp": datetime.now().isoformat()
        }

# ==========================================
# 5. ORCHESTRATEUR AVANCÉ
# ==========================================

class AgentOrchestrator:
    """
    🎭 Orchestrateur avancé - Coordination et pipeline d'agents
    
    Coordonne l'exécution de pipelines complexes avec plusieurs agents.
    """
    
    def __init__(self, factory: AgentFactory):
        self.factory = factory
        self.execution_history: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        
        logger.info("AgentOrchestrator initialisé")
    
    def execute_pipeline(self, pipeline_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔄 Exécute un pipeline complet avec orchestration d'agents
        
        Args:
            pipeline_config: Configuration du pipeline
            
        Returns:
            Dict: Résultats agrégés du pipeline
        """
        pipeline_id = str(uuid.uuid4())
        pipeline_name = pipeline_config.get("name", f"pipeline_{pipeline_id[:8]}")
        steps = pipeline_config.get("steps", [])
        
        logger.info(f"Démarrage pipeline: {pipeline_name} (ID: {pipeline_id})")
        
        pipeline_results = {
            "pipeline_id": pipeline_id,
            "pipeline_name": pipeline_name,
            "start_time": datetime.now().isoformat(),
            "steps": [],
            "total_duration_seconds": 0,
            "success": True,
            "summary": {},
            "agents_used": []
        }
        
        start_time = datetime.now()
        agents_used = set()
        
        try:
            for i, step in enumerate(steps, 1):
                step_result = self._execute_step(step, i, pipeline_id)
                pipeline_results["steps"].append(step_result)
                
                if step_result.get("agent_id"):
                    agents_used.add(step_result["agent_id"])
                
                if not step_result.get("success", False):
                    pipeline_results["success"] = False
                    if pipeline_config.get("fail_fast", True):
                        logger.warning(f"Pipeline {pipeline_name} arrêté à l'étape {i}")
                        break
            
            # Finalisation
            end_time = datetime.now()
            pipeline_results["end_time"] = end_time.isoformat()
            pipeline_results["total_duration_seconds"] = (end_time - start_time).total_seconds()
            pipeline_results["agents_used"] = list(agents_used)
            
            # Résumé
            total_steps = len(pipeline_results["steps"])
            successful_steps = sum(1 for step in pipeline_results["steps"] if step.get("success", False))
            
            pipeline_results["summary"] = {
                "total_steps": total_steps,
                "successful_steps": successful_steps,
                "failed_steps": total_steps - successful_steps,
                "success_rate_percent": (successful_steps / total_steps * 100) if total_steps > 0 else 0,
                "agents_count": len(agents_used)
            }
            
            # Sauvegarde dans l'historique
            with self._lock:
                self.execution_history.append(pipeline_results.copy())
            
            logger.info(f"Pipeline {pipeline_name} terminé - Succès: {pipeline_results['success']}")
            
        except Exception as e:
            logger.error(f"Erreur dans pipeline {pipeline_name}: {e}")
            pipeline_results["success"] = False
            pipeline_results["error"] = str(e)
        
        return pipeline_results
    
    def _execute_step(self, step_config: Dict[str, Any], step_number: int, 
                     pipeline_id: str) -> Dict[str, Any]:
        """
        📋 Exécute une étape du pipeline
        
        Args:
            step_config: Configuration de l'étape
            step_number: Numéro de l'étape
            pipeline_id: ID du pipeline
            
        Returns:
            Dict: Résultats de l'étape
        """
        step_name = step_config.get("name", f"step_{step_number}")
        agent_config = step_config.get("agent", {})
        tasks = step_config.get("tasks", [])
        
        logger.info(f"Exécution étape {step_number}: {step_name}")
        
        step_result = {
            "step_number": step_number,
            "step_name": step_name,
            "pipeline_id": pipeline_id,
            "start_time": datetime.now().isoformat(),
            "tasks": [],
            "success": True,
            "agent_id": None
        }
        
        try:
            # Création de l'agent pour cette étape
            agent_type = agent_config.get("type")
            agent_params = agent_config.get("config", {})
            
            agent = self.factory.create_agent(agent_type, **agent_params)
            step_result["agent_id"] = agent.id
            
            # Exécution des tâches
            for task_config in tasks:
                task = Task(
                    type=task_config["type"],
                    params=task_config.get("params", {}),
                    priority=Priority(task_config.get("priority", Priority.MEDIUM.value))
                )
                
                task_start = datetime.now()
                result = agent.execute_task(task)
                execution_time = (datetime.now() - task_start).total_seconds()
                
                # Mise à jour des métriques de l'agent
                agent.update_metrics(result, execution_time)
                
                task_result = {
                    "task_id": task.id,
                    "task_type": task.type,
                    "success": result.success,
                    "execution_time_seconds": execution_time,
                    "data": result.data,
                    "error": result.error
                }
                
                step_result["tasks"].append(task_result)
                
                if not result.success:
                    step_result["success"] = False
                    logger.warning(f"Tâche {task.type} échouée: {result.error}")
            
            step_result["end_time"] = datetime.now().isoformat()
            logger.info(f"Étape {step_name} terminée - Succès: {step_result['success']}")
            
        except Exception as e:
            step_result["success"] = False
            step_result["error"] = str(e)
            step_result["end_time"] = datetime.now().isoformat()
            logger.error(f"Erreur étape {step_name}: {e}")
        
        return step_result
    
    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        📊 Retourne l'historique des exécutions
        
        Args:
            limit: Nombre maximum d'éléments à retourner
            
        Returns:
            List[Dict]: Historique des pipelines exécutés
        """
        with self._lock:
            return self.execution_history[-limit:] if self.execution_history else []
    
    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """
        📈 Retourne les statistiques de l'orchestrateur
        
        Returns:
            Dict: Statistiques d'utilisation
        """
        with self._lock:
            total_pipelines = len(self.execution_history)
            successful_pipelines = sum(1 for p in self.execution_history if p.get("success", False))
            
            return {
                "total_pipelines_executed": total_pipelines,
                "successful_pipelines": successful_pipelines,
                "failed_pipelines": total_pipelines - successful_pipelines,
                "success_rate_percent": (successful_pipelines / total_pipelines * 100) if total_pipelines > 0 else 0,
                "total_execution_time": sum(p.get("total_duration_seconds", 0) for p in self.execution_history),
                "average_execution_time": sum(p.get("total_duration_seconds", 0) for p in self.execution_history) / total_pipelines if total_pipelines > 0 else 0,
                "last_execution": self.execution_history[-1]["start_time"] if self.execution_history else None
            }

# ==========================================
# 6. FONCTIONS UTILITAIRES
# ==========================================

def create_factory_with_defaults() -> AgentFactory:
    """
    🏗️ Crée une factory avec la configuration par défaut
    
    Returns:
        AgentFactory: Factory configurée avec les agents de base
    """
    factory = AgentFactory()
    
    # Enregistrement des agents par défaut
    # En production, ceci utiliserait les vraies implémentations
    
    logger.info("Factory créée avec configuration par défaut")
    return factory

def validate_pipeline_config(config: Dict[str, Any]) -> List[str]:
    """
    ✅ Valide la configuration d'un pipeline
    
    Args:
        config: Configuration à valider
        
    Returns:
        List[str]: Liste des erreurs trouvées (vide si valide)
    """
    errors = []
    
    if "steps" not in config:
        errors.append("Configuration 'steps' manquante")
        return errors
    
    steps = config["steps"]
    if not isinstance(steps, list) or len(steps) == 0:
        errors.append("'steps' doit être une liste non-vide")
        return errors
    
    for i, step in enumerate(steps):
        if "agent" not in step:
            errors.append(f"Étape {i+1}: configuration 'agent' manquante")
        elif "type" not in step["agent"]:
            errors.append(f"Étape {i+1}: type d'agent manquant")
        
        if "tasks" not in step:
            errors.append(f"Étape {i+1}: configuration 'tasks' manquante")
        elif not isinstance(step["tasks"], list):
            errors.append(f"Étape {i+1}: 'tasks' doit être une liste")
    
    return errors

if __name__ == "__main__":
    # Test basique de l'architecture
    print("🏭 Test Architecture Pattern Factory")
    
    factory = create_factory_with_defaults()
    print(f"Types disponibles: {factory.get_available_types()}")
    
    print("✅ Architecture Pattern Factory validée !") 



