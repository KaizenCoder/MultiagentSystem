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
import logging
from pathlib import Path
import threading
import uuid
import importlib

# Intégration avec les templates existants (Sprints 1-5)
import sys
sys.path.append(str(Path(__file__).parent.parent))

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
    
    def __init__(self, agent_type: str, **config):
        self.type = agent_type
        self.config = config
        self.id = f"{agent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        self.capabilities: List[str] = []
        self.created_at = datetime.now()
        self.status = "ready"
        self.metadata: Dict[str, Any] = {}
        
        # Métriques d'utilisation
        self.tasks_executed = 0
        self.total_execution_time = 0.0
        self.success_rate = 0.0
        self.last_activity = datetime.now()
        
        logger.info(f"Agent {self.type} créé avec ID: {self.id}")
    
    @abstractmethod
    def execute_task(self, task: Task) -> Result:
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
        🛑 Arrête l'agent proprement et libère les ressources
        
        Cette méthode est appelée pour une terminaison propre.
        """
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """
        ❤️ Vérifie l'état de santé de l'agent
        
        Retourne un dictionnaire avec le statut et des métriques de santé.
        Ex: {"status": "healthy", "dependencies": {"db": "ok"}}
        """
        pass

    def can_handle(self, task: Task) -> bool:
        """
        Vérifie si l'agent peut exécuter une tâche donnée
        
        Args:
            task: La tâche à vérifier
        
        Returns:
            bool: True si la tâche est supportée, False sinon
        """
        return task.type in self.get_capabilities()

    def get_status(self) -> Dict[str, Any]:
        """
        Retourne le statut complet de l'agent
        """
        return {
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "tasks_executed": self.tasks_executed,
            "total_execution_time_seconds": self.total_execution_time,
            "success_rate": self.success_rate,
            "capabilities": self.get_capabilities(),
            "metadata": self.metadata
        }

    def update_metrics(self, result: Result, execution_time: float):
        """
        Met à jour les métriques de l'agent après une exécution de tâche.
        """
        self.tasks_executed += 1
        self.total_execution_time += execution_time
        
        # Calcul du taux de succès
        # (tasks_executed - 1) * old_success_rate + (1 if success else 0) / tasks_executed
        current_success_count = (self.tasks_executed - 1) * self.success_rate
        if result.success:
            current_success_count += 1
        self.success_rate = current_success_count / self.tasks_executed
        
        self.last_activity = datetime.now()

# ==========================================
# 3. AGENT REGISTRY
# ==========================================

class AgentRegistry:
    """
    📖 Registre central pour les types d'agents.
    
    Stocke les classes et les fonctions factory pour chaque type d'agent.
    """
    
    def __init__(self):
        self._registry: Dict[str, Dict] = {}
        self.lock = threading.Lock()
        logger.info("AgentRegistry initialisé")

    def register(self, agent_type: str, agent_class: Type[Agent], 
                factory_func: Optional[Callable] = None):
        """
        Enregistre un nouveau type d'agent.
        
        Args:
            agent_type: Nom unique pour le type d'agent (ex: "database").
            agent_class: La classe de l'agent qui hérite de Agent.
            factory_func: Fonction optionnelle pour créer des instances.
        """
        with self.lock:
            if agent_type in self._registry:
                logger.warning(f"Le type d'agent '{agent_type}' est déjà enregistré. "
                               f"Il va être écrasé.")
            self._registry[agent_type] = {
                "class": agent_class, 
                "factory": factory_func
            }
            logger.info(f"Type d'agent '{agent_type}' enregistré avec la classe "
                        f"'{agent_class.__name__}'.")

    def get_agent_class(self, agent_type: str) -> Type[Agent]:
        """
        Récupère la classe d'un type d'agent.
        
        Args:
            agent_type: Nom du type d'agent.
        
        Returns:
            La classe de l'agent.
            
        Raises:
            ValueError: Si le type n'est pas enregistré.
        """
        with self.lock:
            if agent_type not in self._registry:
                raise ValueError(f"Agent type '{agent_type}' not registered. "
                                 f"Available: {list(self._registry.keys())}")
            return self._registry[agent_type]["class"]

    def get_factory_func(self, agent_type: str) -> Optional[Callable]:
        """
        Récupère la fonction factory pour un type d'agent.
        """
        with self.lock:
            if agent_type not in self._registry:
                return None
            return self._registry[agent_type].get("factory")

    def get_available_types(self) -> List[str]:
        """
        Retourne la liste de tous les types d'agents enregistrés.
        """
        with self.lock:
            return list(self._registry.keys())

    def get_registry_info(self) -> Dict[str, Any]:
        """
        Fournit un résumé du contenu du registre.
        """
        with self.lock:
            info = {}
            for agent_type, data in self._registry.items():
                info[agent_type] = {
                    "class_name": data["class"].__name__,
                    "module": data["class"].__module__,
                    "has_factory_function": data["factory"] is not None
                }
            return {
                "total_types": len(self._registry),
                "types": info
            }

# ==========================================
# 4. AGENT FACTORY (Cœur du Pattern)
# ==========================================

class AgentFactory:
    """
    Crée, gère et supervise le cycle de vie des agents.
    Le cœur du Pattern Factory.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialise la Factory.
        
        Args:
            config_path: Chemin vers le fichier de configuration JSON.
        """
        logger.info("🏭 Initialisation de l'AgentFactory...")
        self.registry = AgentRegistry()
        self.active_agents: Dict[str, Agent] = {}
        self.config_path = config_path

        if config_path:
            self._load_configuration()
        else:
            logger.warning("Aucun chemin de configuration fourni. Utilisation des agents par défaut.")
            self._register_default_agents()
        
        logger.info(f"AgentFactory initialisée avec {len(self.registry.get_available_types())} types d'agents.")

    def _load_configuration(self):
        """Charge les types d'agents depuis un fichier de configuration JSON."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # TODO: Traiter la config de la factory (ex: config_data['factory_config'])

            # --- DEBUT DE LA MODIFICATION POUR CORRECTION ---
            # EXPLICATION : Le code original (probablement modifié par erreur) cherchait la clé "agent_types".
            # Cependant, l'écosystème de configuration (ex: maintenance_config.json) utilise la clé "agents".
            # Nous rétablissons ici la clé correcte "agents" pour assurer la compatibilité.
            
            # Ligne originale incorrecte :
            # agent_configs = config_data.get('agent_types', {})
            
            # Ligne corrigée :
            agent_configs = config_data.get('agents', {})
            # --- FIN DE LA MODIFICATION POUR CORRECTION ---

            for agent_type, config in agent_configs.items():
                try:
                    module = importlib.import_module(config['module'])
                    agent_class = getattr(module, config['class'])
                    factory_func = getattr(module, config['factory_function']) if 'factory_function' in config else None
                    self.register_agent_type(agent_type, agent_class, factory_func)
                except (ImportError, AttributeError, KeyError) as e:
                    logger.error(f"Échec du chargement de l'agent '{agent_type}': {e}")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Erreur de chargement du fichier de configuration '{self.config_path}': {e}")
            self._register_default_agents()

    def _register_default_agents(self):
        """
        Enregistre des agents par défaut si aucune configuration n'est fournie.
        (Mécanisme de fallback)
        """
        logger.warning("Configuration par défaut utilisée")
        try:
            # Exemple : enregistrer un agent méta-stratégique par défaut
            from agents.agent_meta_strategique_pattern_factory import MetaStrategiqueAgent, create_meta_agent
            self.register_agent_type("meta_strategique", MetaStrategiqueAgent, create_meta_agent)
            logger.info("🏭 Agents par défaut enregistrés")
        except ImportError:
            logger.warning("Agent Méta-Stratégique non disponible: No module named 'agents.agent_meta_strategique_pattern_factory'")
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement des agents par défaut: {e}")

    def create_agent(self, agent_type: str, **config) -> Agent:
        """
        Crée une nouvelle instance d'un agent.
        
        Args:
            agent_type: Le type d'agent à créer.
            config: Configuration additionnelle pour l'instance de l'agent.
            
        Returns:
            Une instance de l'agent.
            
        Raises:
            ValueError: Si le type d'agent n'est pas enregistré.
        """
        factory_func = self.registry.get_factory_func(agent_type)
        if factory_func:
            agent = factory_func(**config)
        else:
            agent_class = self.registry.get_agent_class(agent_type)
            agent = agent_class(**config)
        
        self.active_agents[agent.id] = agent
        logger.info(f"Agent '{agent.type}' (ID: {agent.id}) créé et activé.")
        return agent

    def register_agent_type(self, agent_type: str, agent_class: Type[Agent], 
                          factory_func: Optional[Callable] = None):
        """
        Raccourci pour enregistrer un type dans le registre de la factory.
        """
        self.registry.register(agent_type, agent_class, factory_func)

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """
        Récupère un agent actif par son ID.
        """
        return self.active_agents.get(agent_id)

    def get_available_types(self) -> List[str]:
        """
        Retourne la liste des types d'agents créables.
        """
        return self.registry.get_available_types()

    def get_created_agents(self) -> Dict[str, Agent]:
        """
        Retourne un dictionnaire de tous les agents actifs.
        """
        return self.active_agents

    def cleanup_agents(self, max_age_hours: int = 24):
        """
        Supprime les agents inactifs ou anciens.
        (Exemple de gestion de cycle de vie)
        """
        now = datetime.now()
        to_remove = [
            agent_id for agent_id, agent in self.active_agents.items()
            if (now - agent.last_activity).total_seconds() > max_age_hours * 3600
        ]
        
        for agent_id in to_remove:
            logger.info(f"Nettoyage de l'agent inactif {agent_id}")
            del self.active_agents[agent_id]
            
        return len(to_remove)

    def get_factory_status(self) -> Dict[str, Any]:
        """
        Retourne le statut complet de la factory et de ses agents.
        """
        return {
            "factory_id": id(self),
            "config_path": self.config_path,
            "total_active_agents": len(self.active_agents),
            "registry_info": self.registry.get_registry_info(),
            "active_agent_details": {
                agent_id: agent.get_status() for agent_id, agent in self.active_agents.items()
            }
        }

# ==========================================
# 5. AGENT ORCHESTRATOR
# ==========================================

class AgentOrchestrator:
    """
    Orchestre des workflows complexes impliquant plusieurs agents.
    Exécute des pipelines définis dans une configuration.
    """
    
    def __init__(self, factory: AgentFactory):
        self.factory = factory
        self.execution_history: List[Dict] = []
        self.lock = threading.Lock()
        logger.info("AgentOrchestrator initialisé.")

    def execute_pipeline(self, pipeline_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute un pipeline complet d'opérations.
        
        Args:
            pipeline_config: Configuration du pipeline
            
        Returns:
            Dictionnaire contenant les résultats de chaque étape.
        """
        pipeline_id = pipeline_config.get("id", f"pipeline_{uuid.uuid4().hex[:8]}")
        start_time = datetime.now()
        logger.info(f"🚀 Début d'exécution du pipeline '{pipeline_id}'")
        
        steps = pipeline_config.get("steps", [])
        pipeline_context = pipeline_config.get("context", {})
        results = {}
        
        for i, step_config in enumerate(steps):
            step_name = step_config.get("name", f"step_{i+1}")
            logger.info(f"  -> Exécution de l'étape {i+1}: '{step_name}'")
            
            # Injecter les résultats des étapes précédentes dans les paramètres
            params = step_config.get("params", {})
            for key, value in params.items():
                if isinstance(value, str) and value.startswith("$.steps."):
                    parts = value.split('.')
                    # $.steps.step_name.output.key
                    try:
                        ref_step_name = parts[2]
                        ref_output_key = parts[4]
                        params[key] = results[ref_step_name]['output'][ref_output_key]
                    except (IndexError, KeyError) as e:
                        logger.error(f"  ❌ Erreur de résolution de référence '{value}': {e}")
                        step_result = {
                            "status": "FAILED",
                            "error": f"Référence invalide: {value}"
                        }
                        results[step_name] = step_result
                        break # Arrêter le pipeline en cas d'erreur
            
            # Si une erreur a eu lieu à l'étape de résolution
            if results.get(step_name, {}).get("status") == "FAILED":
                break
                
            step_result = self._execute_step(step_config, i+1, pipeline_id)
            results[step_name] = step_result
            
            if step_result["status"] != "COMPLETED":
                logger.error(f"  ❌ L'étape '{step_name}' a échoué. Arrêt du pipeline.")
                break
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        final_status = "COMPLETED" if all(r.get('status') == 'COMPLETED' for r in results.values()) else "FAILED"
        
        pipeline_summary = {
            "pipeline_id": pipeline_id,
            "status": final_status,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "steps": results
        }
        
        with self.lock:
            self.execution_history.append(pipeline_summary)
        
        logger.info(f"✅ Pipeline '{pipeline_id}' terminé avec le statut: {final_status}")
        return pipeline_summary

    def _execute_step(self, step_config: Dict[str, Any], step_number: int, 
                     pipeline_id: str) -> Dict[str, Any]:
        """Exécute une seule étape du pipeline."""
        start_time = datetime.now()
        
        try:
            agent_type = step_config["agent_type"]
            task_type = step_config["task"]["type"]
            task_params = step_config["task"]["params"]
            
            # Création de l'agent pour cette étape
            agent = self.factory.create_agent(agent_type)
            
            # Création et exécution de la tâche
            task = Task(type=task_type, params=task_params)
            result = agent.execute_task(task)
            
            # Mise à jour des métriques de l'agent
            exec_time = (datetime.now() - start_time).total_seconds()
            agent.update_metrics(result, exec_time)
            
            if result.success:
                status = "COMPLETED"
                output = result.data
                error = None
            else:
                status = "FAILED"
                output = None
                error = result.error
                logger.warning(f"    - Tâche '{task_type}' échouée pour l'agent '{agent_type}': {error}")
            
        except KeyError as e:
            status = "CONFIG_ERROR"
            output = None
            error = f"Clé manquante dans la configuration de l'étape: {e}"
            logger.error(f"    - Erreur de configuration d'étape: {error}")
        except Exception as e:
            status = "EXECUTION_ERROR"
            output = None
            error = str(e)
            logger.error(f"    - Erreur inattendue durant l'étape: {e}", exc_info=True)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return {
            "step_number": step_number,
            "agent_type": agent_type,
            "task_type": task_type,
            "status": status,
            "duration_seconds": duration,
            "output": output,
            "error": error
        }

    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retourne l'historique des exécutions de pipelines.
        """
        with self.lock:
            return self.execution_history[-limit:]

    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """
        Retourne des statistiques sur les exécutions.
        """
        with self.lock:
            total_pipelines = len(self.execution_history)
            successful_pipelines = sum(1 for p in self.execution_history if p['status'] == 'COMPLETED')
            failed_pipelines = total_pipelines - successful_pipelines
            
            total_duration = sum(p['duration_seconds'] for p in self.execution_history)
            avg_duration = total_duration / total_pipelines if total_pipelines > 0 else 0
            
            return {
                "total_pipelines_executed": total_pipelines,
                "successful_pipelines": successful_pipelines,
                "failed_pipelines": failed_pipelines,
                "success_rate": successful_pipelines / total_pipelines if total_pipelines > 0 else 0,
                "average_pipeline_duration_seconds": avg_duration
            }

# ==========================================
# Fonctions utilitaires
# ==========================================

def create_factory_with_defaults() -> AgentFactory:
    """
    Crée une AgentFactory avec les agents par défaut enregistrés.
    """
    factory = AgentFactory()
    # Ici, on pourrait ajouter un enregistrement plus complexe
    # basé sur la découverte de plugins, etc.
    return factory

def validate_pipeline_config(config: Dict[str, Any]) -> List[str]:
    """
    Valide une configuration de pipeline.
    
    Returns:
        Liste des erreurs de validation. Liste vide si valide.
    """
    errors = []
    if "steps" not in config or not isinstance(config["steps"], list):
        errors.append("La clé 'steps' est manquante ou n'est pas une liste.")
        return errors
        
    for i, step in enumerate(config["steps"]):
        if not isinstance(step, dict):
            errors.append(f"L'étape {i+1} n'est pas un dictionnaire.")
            continue
        if "agent_type" not in step:
            errors.append(f"L'étape {i+1} n'a pas de 'agent_type'.")
        if "task" not in step or not isinstance(step["task"], dict):
            errors.append(f"L'étape {i+1} n'a pas de 'task' ou ce n'est pas un dictionnaire.")
        elif "type" not in step.get("task", {}):
            errors.append(f"La tâche de l'étape {i+1} n'a pas de 'type'.")
            
    return errors