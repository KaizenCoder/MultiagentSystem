#!/usr/bin/env python3
"""
🎖️ Agent 0 - Chef d'Équipe Coordinateur
VERSION INTÉGRÉE AVEC LOGGING CENTRALISÉ ET MONITORING AVANCÉ
Modèle: Claude Sonnet 4
Mission: Orchestration centrale de l'équipe de maintenance avec observabilité complète
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import sys

# Import du système de logging centralisé - Version corrigée
try:
    from ..logging.centralized_logging import logging_manager, log_performance
except ImportError:
    # Fallback vers logging standard si imports relatifs échouent
    import logging
    logging_manager = None
    def log_performance(operation_name: str, logger=None):
        """Mock de log_performance"""
        def decorator(func):
            return func
        return decorator

# Import des métriques et monitoring - Version corrigée
try:
    from ..monitoring.metrics_collector import MetricsCollector
    from ..monitoring.health_monitor import HealthMonitor
except ImportError:
    # Mocks pour les classes de monitoring
    class MetricsCollector:
        def __init__(self, agent_id: str):
            self.agent_id = agent_id
            self.metrics = {}
        
        def collect_metric(self, name: str, value: float):
            self.metrics[name] = value
    
    class HealthMonitor:
        def __init__(self, agent_id: str):
            self.agent_id = agent_id
            self.status = "healthy"
        
        def check_health(self):
            return {"status": self.status, "agent_id": self.agent_id}

class WorkflowStatus(Enum):
    """États possibles d'un workflow"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class WorkflowMetrics:
    """Métriques pour un workflow - Version ChatGPT enrichie"""
    workflow_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: WorkflowStatus = WorkflowStatus.PENDING
    agents_involved: List[str] = field(default_factory=list)
    tasks_completed: int = 0
    tasks_total: int = 0
    errors: List[Dict[str, Any]] = field(default_factory=list)
    performance_data: Dict[str, float] = field(default_factory=dict)
    
    # Nouvelles métriques ChatGPT
    ai_recommendations: List[Dict[str, Any]] = field(default_factory=list)
    optimization_level: float = 1.0  # 1.0 = standard, > 1.0 = optimisé
    resource_usage: Dict[str, float] = field(default_factory=dict)
    quality_score: float = 0.0
    learning_data: Dict[str, Any] = field(default_factory=dict)

@dataclass 
class AICoordinationEngine:
    """Moteur d'IA pour coordination intelligente - Nouvelle fonctionnalité ChatGPT"""
    agent_id: str
    enabled: bool = True
    learning_mode: bool = True
    optimization_threshold: float = 0.8
    
    # Historique pour apprentissage
    workflow_history: List[WorkflowMetrics] = field(default_factory=list)
    performance_patterns: Dict[str, List[float]] = field(default_factory=dict)
    optimal_configurations: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    def analyze_workflow_patterns(self) -> Dict[str, Any]:
        """Analyse les patterns de workflow pour optimisation"""
        if not self.workflow_history:
            return {"recommendations": [], "confidence": 0.0}
        
        # Analyse simple basée sur l'historique
        successful_workflows = [w for w in self.workflow_history if w.status == WorkflowStatus.COMPLETED]
        success_rate = len(successful_workflows) / len(self.workflow_history)
        
        recommendations = []
        if success_rate < self.optimization_threshold:
            recommendations.append({
                "type": "optimization",
                "message": "Taux de succès faible, optimisation recommandée",
                "priority": "high",
                "success_rate": success_rate
            })
        
        return {
            "recommendations": recommendations,
            "confidence": min(len(self.workflow_history) / 10, 1.0),
            "success_rate": success_rate,
            "avg_duration": sum((w.end_time - w.start_time).total_seconds() 
                              for w in successful_workflows if w.end_time) / len(successful_workflows) if successful_workflows else 0
        }
    
    def suggest_optimization(self, workflow_type: str, current_params: Dict[str, Any]) -> Dict[str, Any]:
        """Suggère des optimisations pour un workflow"""
        # Logique d'optimisation basée sur l'historique
        if workflow_type in self.optimal_configurations:
            optimal = self.optimal_configurations[workflow_type]
            suggestions = {}
            
            for key, optimal_value in optimal.items():
                if key in current_params and current_params[key] != optimal_value:
                    suggestions[key] = {
                        "current": current_params[key],
                        "suggested": optimal_value,
                        "reason": "Basé sur les meilleures performances historiques"
                    }
            
            return {
                "suggestions": suggestions,
                "confidence": 0.8,
                "expected_improvement": "15-25%"
            }
        
        return {"suggestions": {}, "confidence": 0.0}

class Agent0ChefEquipeCoordinateur:
    """Agent 0 - Chef d'Équipe Coordinateur avec logging centralisé et monitoring avancé"""
    
    def __init__(
        self, 
        agent_id: str = None, 
        agent_type: str = "chef_equipe_coordinateur",
        target_path: str = None, 
        workspace_path: str = None, 
        **config
    ):
        """Initialisation avec injection de logging centralisé"""
        self.agent_id = agent_id or f"agent_0_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.agent_type = agent_type
        self.config = config
        
        # Extraction de la configuration de logging injectée par TemplateManager
        logging_config = config.get("logging")
        if logging_manager and logging_config:
            # Utilisation de la configuration injectée
            self.logger = logging_manager.get_logger(None, logging_config)
            self.async_logging = logging_config.get("async_enabled", False)
        elif logging_manager:
            # Fallback sur configuration par défaut
            self.logger = logging_manager.get_agent_logger(
                agent_name="chef_equipe_coordinateur",
                role="coordinateur",
                domain="coordination",
                agent_id=self.agent_id,
                async_enabled=True  # Chef d'équipe utilise logging async
            )
            self.async_logging = True
        else:
            # Fallback vers logging standard
            # LoggingManager NextGeneration - Orchestrateur
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = logging_manager.get_logger(custom_config={
            "logger_name": "MetricsCollector",
            "log_level": "INFO",
            "elasticsearch_enabled": True,
            "encryption_enabled": True,
            "async_enabled": True,
            "alerting_enabled": True,
            "high_throughput": True
        })
            self.logger.setLevel(logging.INFO)
            self.async_logging = False
        
        # Logger d'audit pour actions critiques
        if logging_manager:
            self.audit_logger = logging_manager.create_audit_logger(
                user_id=self.agent_id,
                action_type="coordination"
            )
        else:
            self.audit_logger = self.logger
        
        # Configuration équipe et chemins
        self.target_path = Path(target_path) if target_path else Path("../agent_factory_implementation/agents")
        self.workspace_path = Path(workspace_path) if workspace_path else Path(".")
        
        # État interne
        self.equipe_agents = {}
        self.workflows_disponibles = self._charger_workflows_disponibles()
        self.workflows_actifs: Dict[str, WorkflowMetrics] = {}
        self._is_running = False
        
        # Métriques et monitoring
        self.metrics_collector = MetricsCollector(self.agent_id)
        self.health_monitor = HealthMonitor(self.agent_id)
        
        # NOUVEAU CHATGPT: Moteur d'IA pour coordination intelligente
        self.ai_engine = AICoordinationEngine(
            agent_id=self.agent_id,
            enabled=config.get("ai_coordination_enabled", True),
            learning_mode=config.get("ai_learning_mode", True),
            optimization_threshold=config.get("ai_optimization_threshold", 0.8)
        )
        
        # NOUVEAU CHATGPT: Cache intelligent pour optimisation
        self._workflow_cache = {}
        self._performance_baseline = {}
        self._optimization_suggestions = {}
        
        # Métadonnées NextGeneration enrichies
        self.nextgen_metadata = config.get("nextgen_metadata", {})
        self.nextgen_metadata.update({
            "ai_coordination": self.ai_engine.enabled,
            "ai_learning": self.ai_engine.learning_mode,
            "version": "ChatGPT_Enhanced_v1.0"
        })
        
        # Log d'initialisation enrichi
        self.logger.info(
            "🎖️ Agent 0 Chef d'Équipe Coordinateur initialisé avec logging centralisé",
            extra={
                "agent": {
                    "id": self.agent_id,
                    "type": self.agent_type,
                    "role": "coordinateur",
                    "domain": "coordination"
                },
                "configuration": {
                    "target_path": str(self.target_path),
                    "workspace_path": str(self.workspace_path),
                    "async_logging": self.async_logging,
                    "workflows_count": len(self.workflows_disponibles)
                },
                "nextgen": self.nextgen_metadata,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        # Audit log pour création d'agent
        self.audit_logger.info(
            f"Agent coordinateur créé: {self.agent_id}",
            extra={"operation": "agent_creation"}
        )
    
    def _charger_workflows_disponibles(self) -> List[str]:
        """Charge la liste des workflows disponibles"""
        # Simulation - en production, charger depuis configuration
        return [
            "maintenance_complete",
            "analyse_structure",
            "evaluation_qualite",
            "adaptation_code",
            "tests_validation",
            "documentation_generation"
        ]
    
    async def startup(self) -> Dict[str, Any]:
        """Démarrage de l'agent avec logging structuré"""
        with log_performance("agent_startup", self.logger):
            self.logger.info(
                "🚀 Démarrage Agent 0 Chef d'Équipe",
                extra={
                    "operation": "startup",
                    "agent_id": self.agent_id,
                    "phase": "initialization"
                }
            )
            
            try:
                # Vérification et création des chemins
                await self._verifier_environnement()
                
                # Initialisation de l'équipe
                await self._initialiser_equipe()
                
                # Démarrage des composants de monitoring
                await self._demarrer_monitoring()
                
                self._is_running = True
                
                startup_result = {
                    "status": "started",
                    "agent_id": self.agent_id,
                    "timestamp": datetime.now().isoformat(),
                    "equipe_size": len(self.equipe_agents),
                    "workflows_available": len(self.workflows_disponibles)
                }
                
                self.logger.info(
                    "✅ Chef d'Équipe prêt à coordonner",
                    extra={
                        "operation": "startup",
                        "phase": "completed",
                        "result": startup_result
                    }
                )
                
                # Audit log
                self.audit_logger.info(
                    "Agent startup completed",
                    extra={"startup_result": startup_result}
                )
                
                return startup_result
                
            except Exception as e:
                self.logger.error(
                    "❌ Erreur lors du démarrage",
                    extra={
                        "operation": "startup",
                        "phase": "error",
                        "error_type": type(e).__name__,
                        "error_message": str(e)
                    },
                    exc_info=True
                )
                
                # Métriques d'erreur
                self.metrics_collector.increment_counter("startup_errors")
                
                raise
    
    async def _verifier_environnement(self):
        """Vérifie et prépare l'environnement de travail"""
        self.logger.debug(
            "Vérification de l'environnement",
            extra={"operation": "environment_check"}
        )
        
        # Vérifier/créer les répertoires nécessaires
        directories = [
            self.target_path,
            self.workspace_path / "reports",
            self.workspace_path / "workflows",
            self.workspace_path / "metrics"
        ]
        
        for directory in directories:
            if not directory.exists():
                self.logger.warning(
                    f"Création du répertoire manquant: {directory}",
                    extra={
                        "operation": "directory_creation",
                        "path": str(directory)
                    }
                )
                directory.mkdir(parents=True, exist_ok=True)
    
    async def _initialiser_equipe(self):
        """Initialise l'équipe d'agents"""
        self.logger.info(
            "Initialisation de l'équipe d'agents",
            extra={"operation": "team_initialization"}
        )
        
        # Configuration des agents de l'équipe
        agents_config = [
            {"name": "agent_1_analyseur", "role": "analyseur", "domain": "analysis"},
            {"name": "agent_2_evaluateur", "role": "evaluateur", "domain": "quality"},
            {"name": "agent_3_adaptateur", "role": "adaptateur", "domain": "adaptation"},
            {"name": "agent_4_testeur", "role": "testeur", "domain": "testing"},
            {"name": "agent_5_documenteur", "role": "documenteur", "domain": "documentation"},
            {"name": "agent_6_validateur", "role": "validateur", "domain": "validation"}
        ]
        
        for agent_config in agents_config:
            self.equipe_agents[agent_config["name"]] = {
                "status": "ready",
                "role": agent_config["role"],
                "domain": agent_config["domain"],
                "last_activity": datetime.now()
            }
            
            self.logger.debug(
                f"Agent {agent_config['name']} ajouté à l'équipe",
                extra={
                    "operation": "agent_registration",
                    "agent": agent_config
                }
            )
    
    async def _demarrer_monitoring(self):
        """Démarre les composants de monitoring"""
        self.logger.info(
            "Démarrage du monitoring",
            extra={"operation": "monitoring_startup"}
        )
        
        # Démarrer la collecte de métriques
        await self.metrics_collector.start()
        
        # Démarrer le health monitor
        await self.health_monitor.start()
        
        # Programmer les tâches de maintenance
        asyncio.create_task(self._maintenance_periodique())
    
    async def _maintenance_periodique(self):
        """Tâche de maintenance périodique"""
        while self._is_running:
            try:
                await asyncio.sleep(300)  # Toutes les 5 minutes
                
                with log_performance("periodic_maintenance", self.logger):
                    # Nettoyer les workflows terminés
                    self._nettoyer_workflows_termines()
                    
                    # Collecter les métriques
                    metrics = await self._collecter_metriques()
                    
                    # Logger les métriques dans le logger de performance
                    perf_logger = logging_manager.get_performance_logger()
                    perf_logger.info(
                        "Chef d'équipe metrics",
                        extra={"metrics": metrics}
                    )
                    
            except Exception as e:
                self.logger.error(
                    "Erreur dans maintenance périodique",
                    extra={"error": str(e)},
                    exc_info=True
                )
    
    async def executer_workflow(
        self,
        workflow_type: str,
        parametres: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Exécute un workflow avec IA de coordination et logging complets - Version ChatGPT optimisée"""
        workflow_id = f"{workflow_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # NOUVEAU CHATGPT: Analyse préalable avec IA
        ai_analysis = None
        optimization_suggestions = {}
        if self.ai_engine.enabled:
            ai_analysis = self.ai_engine.analyze_workflow_patterns()
            optimization_suggestions = self.ai_engine.suggest_optimization(workflow_type, parametres)
            
            self.logger.info(
                "🤖 Analyse IA du workflow",
                extra={
                    "ai_analysis": ai_analysis,
                    "optimization_suggestions": optimization_suggestions,
                    "workflow_type": workflow_type
                }
            )
        
        # Créer les métriques du workflow enrichies ChatGPT
        workflow_metrics = WorkflowMetrics(
            workflow_id=workflow_id,
            start_time=datetime.now(),
            tasks_total=len(self.equipe_agents),
            ai_recommendations=ai_analysis.get("recommendations", []) if ai_analysis else [],
            optimization_level=1.2 if optimization_suggestions.get("suggestions") else 1.0
        )
        
        self.workflows_actifs[workflow_id] = workflow_metrics
        
        # Log de début avec contexte enrichi
        self.logger.info(
            f"🔄 Démarrage workflow: {workflow_type}",
            extra={
                "workflow": {
                    "id": workflow_id,
                    "type": workflow_type,
                    "parameters": parametres
                },
                "operation": "workflow_start"
            }
        )
        
        # Audit log
        self.audit_logger.info(
            f"Workflow started: {workflow_id}",
            extra={
                "workflow_type": workflow_type,
                "parameters": parametres
            }
        )
        
        try:
            with log_performance(f"workflow_{workflow_type}", self.logger):
                # Mise à jour du statut
                workflow_metrics.status = WorkflowStatus.RUNNING
                
                # Simulation d'exécution du workflow
                result = await self._executer_workflow_interne(
                    workflow_id,
                    workflow_type,
                    parametres,
                    workflow_metrics
                )
                
                # Mise à jour finale
                workflow_metrics.status = WorkflowStatus.COMPLETED
                workflow_metrics.end_time = datetime.now()
                
                # Calculer la durée
                duration = (workflow_metrics.end_time - workflow_metrics.start_time).total_seconds()
                workflow_metrics.performance_data["total_duration_sec"] = duration
                
                # Log de succès
                self.logger.info(
                    f"✅ Workflow terminé avec succès: {workflow_type}",
                    extra={
                        "workflow": {
                            "id": workflow_id,
                            "type": workflow_type,
                            "status": "completed",
                            "duration_sec": duration,
                            "tasks_completed": workflow_metrics.tasks_completed,
                            "tasks_total": workflow_metrics.tasks_total
                        },
                        "operation": "workflow_complete"
                    }
                )
                
                # NOUVEAU CHATGPT: Apprentissage de l'IA
                if self.ai_engine.enabled and self.ai_engine.learning_mode:
                    # Calculer score de qualité basé sur les métriques
                    workflow_metrics.quality_score = self._calculate_quality_score(workflow_metrics)
                    
                    # Ajouter aux données d'apprentissage
                    workflow_metrics.learning_data = {
                        "parameters_used": parametres,
                        "optimization_applied": optimization_suggestions.get("suggestions", {}),
                        "performance_gain": workflow_metrics.optimization_level - 1.0,
                        "ai_confidence": ai_analysis.get("confidence", 0.0) if ai_analysis else 0.0
                    }
                    
                    # Enregistrer dans l'historique IA
                    self.ai_engine.workflow_history.append(workflow_metrics)
                    
                    # Mettre à jour les patterns de performance
                    if workflow_type not in self.ai_engine.performance_patterns:
                        self.ai_engine.performance_patterns[workflow_type] = []
                    self.ai_engine.performance_patterns[workflow_type].append(duration)
                    
                    # Si c'est un succès et meilleur que la baseline, mettre à jour la config optimale
                    if (workflow_metrics.quality_score > 0.8 and 
                        (workflow_type not in self.ai_engine.optimal_configurations or 
                         duration < min(self.ai_engine.performance_patterns[workflow_type][:-1], default=float('inf')))):
                        self.ai_engine.optimal_configurations[workflow_type] = parametres.copy()
                    
                    self.logger.info(
                        "🧠 IA apprentissage mis à jour",
                        extra={
                            "workflow_type": workflow_type,
                            "quality_score": workflow_metrics.quality_score,
                            "learning_data": workflow_metrics.learning_data,
                            "historical_patterns": len(self.ai_engine.performance_patterns.get(workflow_type, []))
                        }
                    )
                
                # Sauvegarder le rapport enrichi
                await self._sauvegarder_rapport_workflow(workflow_id, result, workflow_metrics)
                
                return result
                
        except Exception as e:
            # Mise à jour en cas d'erreur
            workflow_metrics.status = WorkflowStatus.FAILED
            workflow_metrics.end_time = datetime.now()
            workflow_metrics.errors.append({
                "timestamp": datetime.now().isoformat(),
                "error_type": type(e).__name__,
                "error_message": str(e)
            })
            
            # Log d'erreur détaillé
            self.logger.error(
                f"❌ Échec du workflow: {workflow_type}",
                extra={
                    "workflow": {
                        "id": workflow_id,
                        "type": workflow_type,
                        "status": "failed",
                        "error": str(e)
                    },
                    "operation": "workflow_error"
                },
                exc_info=True
            )
            
            # Audit log pour échec
            self.audit_logger.error(
                f"Workflow failed: {workflow_id}",
                extra={
                    "workflow_type": workflow_type,
                    "error": str(e)
                }
            )
            
            # Incrémenter les métriques d'erreur
            self.metrics_collector.increment_counter(f"workflow_{workflow_type}_errors")
            
            raise
    
    def _calculate_quality_score(self, metrics: WorkflowMetrics) -> float:
        """Calcule un score de qualité pour le workflow - Nouvelle méthode ChatGPT"""
        score = 0.0
        
        # Score basé sur le taux de completion des tâches
        if metrics.tasks_total > 0:
            completion_rate = metrics.tasks_completed / metrics.tasks_total
            score += completion_rate * 0.4  # 40% du score
        
        # Score basé sur l'absence d'erreurs
        error_penalty = min(len(metrics.errors) * 0.1, 0.3)  # Max 30% de pénalité
        score += (0.3 - error_penalty)  # 30% du score
        
        # Score basé sur les performances (durée)
        if metrics.end_time and metrics.start_time:
            duration = (metrics.end_time - metrics.start_time).total_seconds()
            # Score inversement proportionnel à la durée (bonus si rapide)
            if duration < 60:  # Moins d'1 minute = excellent
                score += 0.3
            elif duration < 300:  # Moins de 5 minutes = bon
                score += 0.2
            elif duration < 600:  # Moins de 10 minutes = moyen
                score += 0.1
            # Plus de 10 minutes = 0 point
        
        return min(score, 1.0)  # Cap à 1.0
    
    async def _executer_workflow_interne(
        self,
        workflow_id: str,
        workflow_type: str,
        parametres: Dict[str, Any],
        metrics: WorkflowMetrics
    ) -> Dict[str, Any]:
        """Exécution interne du workflow avec coordination des agents"""
        
        result = {
            "workflow_id": workflow_id,
            "workflow_type": workflow_type,
            "status": "in_progress",
            "agents_results": {},
            "timestamp_start": datetime.now().isoformat()
        }
        
        # Simulation de coordination des agents
        for agent_name, agent_info in self.equipe_agents.items():
            try:
                # Log de tâche agent
                self.logger.debug(
                    f"Assignation tâche à {agent_name}",
                    extra={
                        "workflow_id": workflow_id,
                        "agent": agent_name,
                        "role": agent_info["role"]
                    }
                )
                
                # Simulation d'exécution de tâche
                await asyncio.sleep(0.5)  # Simulation
                
                # Résultat simulé
                agent_result = {
                    "status": "completed",
                    "timestamp": datetime.now().isoformat(),
                    "data": f"Résultat de {agent_info['role']}"
                }
                
                result["agents_results"][agent_name] = agent_result
                metrics.agents_involved.append(agent_name)
                metrics.tasks_completed += 1
                
                # Log de progression
                progress = (metrics.tasks_completed / metrics.tasks_total) * 100
                self.logger.info(
                    f"Progression workflow: {progress:.1f}%",
                    extra={
                        "workflow_id": workflow_id,
                        "progress_percent": progress,
                        "tasks_completed": metrics.tasks_completed,
                        "tasks_total": metrics.tasks_total
                    }
                )
                
            except Exception as e:
                self.logger.error(
                    f"Erreur tâche agent {agent_name}",
                    extra={
                        "workflow_id": workflow_id,
                        "agent": agent_name,
                        "error": str(e)
                    }
                )
                
                result["agents_results"][agent_name] = {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                
                metrics.errors.append({
                    "agent": agent_name,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        result["status"] = "completed"
        result["timestamp_end"] = datetime.now().isoformat()
        
        return result
    
    async def _sauvegarder_rapport_workflow(
        self,
        workflow_id: str,
        result: Dict[str, Any],
        metrics: WorkflowMetrics
    ):
        """Sauvegarde le rapport du workflow avec métriques"""
        try:
            # Créer le rapport complet
            rapport = {
                "workflow_result": result,
                "workflow_metrics": asdict(metrics),
                "chef_equipe": {
                    "agent_id": self.agent_id,
                    "agent_type": self.agent_type
                },
                "nextgen_metadata": self.nextgen_metadata,
                "timestamp_generation": datetime.now().isoformat()
            }
            
            # Déterminer le chemin du rapport
            rapport_path = (
                self.workspace_path / "reports" / 
                f"workflow_{workflow_id}_rapport.json"
            )
            
            # Sauvegarder le rapport
            rapport_path.parent.mkdir(parents=True, exist_ok=True)
            with open(rapport_path, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, indent=2, ensure_ascii=False, default=str)
            
            # Log de sauvegarde
            self.logger.info(
                "💾 Rapport workflow sauvegardé",
                extra={
                    "workflow_id": workflow_id,
                    "rapport_path": str(rapport_path),
                    "file_size": rapport_path.stat().st_size,
                    "operation": "report_save"
                }
            )
            
            # Métriques
            self.metrics_collector.increment_counter("reports_saved")
            
        except Exception as e:
            self.logger.error(
                "Erreur sauvegarde rapport workflow",
                extra={
                    "workflow_id": workflow_id,
                    "error": str(e)
                },
                exc_info=True
            )
    
    def _nettoyer_workflows_termines(self):
        """Nettoie les workflows terminés depuis plus d'une heure"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=1)
            workflows_to_remove = []
            
            for workflow_id, metrics in self.workflows_actifs.items():
                if (metrics.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED] and
                    metrics.end_time and metrics.end_time < cutoff_time):
                    workflows_to_remove.append(workflow_id)
            
            for workflow_id in workflows_to_remove:
                del self.workflows_actifs[workflow_id]
            
            if workflows_to_remove:
                self.logger.debug(
                    f"Nettoyage de {len(workflows_to_remove)} workflows terminés",
                    extra={
                        "operation": "cleanup",
                        "workflows_removed": workflows_to_remove
                    }
                )
                
        except Exception as e:
            self.logger.error(
                "Erreur nettoyage workflows",
                extra={"error": str(e)},
                exc_info=True
            )
    
    async def _collecter_metriques(self) -> Dict[str, Any]:
        """Collecte les métriques du chef d'équipe - Version ChatGPT enrichie"""
        try:
            # Métriques de base
            core_metrics = {
                "agent_id": self.agent_id,
                "timestamp": datetime.now().isoformat(),
                "workflows": {
                    "active": len([w for w in self.workflows_actifs.values() 
                                  if w.status == WorkflowStatus.RUNNING]),
                    "completed": len([w for w in self.workflows_actifs.values() 
                                     if w.status == WorkflowStatus.COMPLETED]),
                    "failed": len([w for w in self.workflows_actifs.values() 
                                  if w.status == WorkflowStatus.FAILED]),
                    "total": len(self.workflows_actifs)
                },
                "equipe": {
                    "agents_count": len(self.equipe_agents),
                    "agents_ready": len([a for a in self.equipe_agents.values() 
                                       if a["status"] == "ready"])
                }
            }
            
            # NOUVELLES MÉTRIQUES CHATGPT IA
            ai_metrics = {
                "ai_coordination": {
                    "enabled": self.ai_engine.enabled,
                    "learning_mode": self.ai_engine.learning_mode,
                    "historical_workflows": len(self.ai_engine.workflow_history),
                    "learned_patterns": len(self.ai_engine.performance_patterns),
                    "optimal_configs": len(self.ai_engine.optimal_configurations),
                    "avg_quality_score": sum(w.quality_score for w in self.ai_engine.workflow_history) / 
                                       len(self.ai_engine.workflow_history) if self.ai_engine.workflow_history else 0.0
                },
                "optimization_analytics": {
                    "optimized_workflows": len([w for w in self.workflows_actifs.values() 
                                              if w.optimization_level > 1.0]),
                    "avg_optimization_level": sum(w.optimization_level for w in self.workflows_actifs.values()) / 
                                            len(self.workflows_actifs) if self.workflows_actifs else 1.0,
                    "ai_recommendations_generated": sum(len(w.ai_recommendations) for w in self.workflows_actifs.values())
                },
                "learning_insights": {}
            }
            
            # Insights par type de workflow
            for workflow_type, patterns in self.ai_engine.performance_patterns.items():
                if patterns:
                    ai_metrics["learning_insights"][workflow_type] = {
                        "executions": len(patterns),
                        "avg_duration": sum(patterns) / len(patterns),
                        "best_duration": min(patterns),
                        "improvement_potential": (max(patterns) - min(patterns)) / max(patterns) * 100 if max(patterns) > 0 else 0
                    }
            
            metrics = {
                "core_metrics": core_metrics,
                "chatgpt_ai_enhancements": ai_metrics
            }
            
            # Statistiques de performance
            if self.workflows_actifs:
                durations = [
                    m.performance_data.get("total_duration_sec", 0)
                    for m in self.workflows_actifs.values()
                    if m.status == WorkflowStatus.COMPLETED and 
                    "total_duration_sec" in m.performance_data
                ]
                
                if durations:
                    metrics["performance"] = {
                        "avg_workflow_duration_sec": sum(durations) / len(durations),
                        "min_workflow_duration_sec": min(durations),
                        "max_workflow_duration_sec": max(durations)
                    }
            
            # Ajouter les métriques du collector
            metrics["system_metrics"] = await self.metrics_collector.get_metrics()
            
            return metrics
            
        except Exception as e:
            self.logger.error(
                "Erreur collecte métriques",
                extra={"error": str(e)},
                exc_info=True
            )
            return {}
    
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé avec logging centralisé et métriques détaillées"""
        try:
            # Collecter l'état de santé
            health_status = {
                "agent": {
                    "id": self.agent_id,
                    "type": self.agent_type,
                    "status": "healthy" if self._is_running else "stopped",
                    "uptime_seconds": None  # À calculer si nécessaire
                },
                "equipe": {
                    "total_agents": len(self.equipe_agents),
                    "agents_ready": len([a for a in self.equipe_agents.values() 
                                       if a["status"] == "ready"]),
                    "agents_status": {
                        name: info["status"] 
                        for name, info in self.equipe_agents.items()
                    }
                },
                "workflows": {
                    "available": len(self.workflows_disponibles),
                    "active": len([w for w in self.workflows_actifs.values() 
                                  if w.status == WorkflowStatus.RUNNING]),
                    "completed_last_hour": len([
                        w for w in self.workflows_actifs.values()
                        if w.status == WorkflowStatus.COMPLETED and
                        w.end_time and 
                        w.end_time > datetime.now() - timedelta(hours=1)
                    ])
                },
                "logging": {
                    "centralized": True,
                    "logger_name": self.logger.name,
                    "async_enabled": self.async_logging
                },
                "monitoring": {
                    "metrics_collector": "active" if self.metrics_collector else "inactive",
                    "health_monitor": "active" if self.health_monitor else "inactive"
                },
                "timestamp": datetime.now().isoformat()
            }
            
            # Déterminer le statut global
            if not self._is_running:
                health_status["agent"]["status"] = "stopped"
            elif len([a for a in self.equipe_agents.values() if a["status"] == "ready"]) < len(self.equipe_agents) / 2:
                health_status["agent"]["status"] = "degraded"
            
            # Log du health check
            log_level = logging.INFO if health_status["agent"]["status"] == "healthy" else logging.WARNING
            self.logger.log(
                log_level,
                "🏥 Health Check Agent 0 Chef d'Équipe",
                extra={
                    "operation": "health_check",
                    "health_status": health_status
                }
            )
            
            return health_status
            
        except Exception as e:
            self.logger.error(
                "Erreur lors du health check",
                extra={"error": str(e)},
                exc_info=True
            )
            
            return {
                "agent": {
                    "id": self.agent_id,
                    "status": "error"
                },
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def shutdown(self):
        """Arrêt propre de l'agent avec nettoyage"""
        self.logger.info(
            "🛑 Arrêt du Chef d'Équipe en cours...",
            extra={"operation": "shutdown"}
        )
        
        try:
            self._is_running = False
            
            # Attendre la fin des workflows actifs
            active_workflows = [
                w for w in self.workflows_actifs.values()
                if w.status == WorkflowStatus.RUNNING
            ]
            
            if active_workflows:
                self.logger.warning(
                    f"En attente de {len(active_workflows)} workflows actifs",
                    extra={
                        "operation": "shutdown",
                        "active_workflows": [w.workflow_id for w in active_workflows]
                    }
                )
                
                # Timeout de 30 secondes pour les workflows
                await asyncio.wait_for(
                    self._attendre_fin_workflows(active_workflows),
                    timeout=30.0
                )
            
            # Sauvegarder les métriques finales
            final_metrics = await self._collecter_metriques()
            
            # Logger les métriques finales
            perf_logger = logging_manager.get_performance_logger()
            perf_logger.info(
                "Chef d'équipe final metrics",
                extra={"metrics": final_metrics}
            )
            
            # Arrêter les composants de monitoring
            if self.metrics_collector:
                await self.metrics_collector.stop()
            
            if self.health_monitor:
                await self.health_monitor.stop()
            
            # Audit log
            self.audit_logger.info(
                "Agent shutdown completed",
                extra={"final_metrics": final_metrics}
            )
            
            self.logger.info(
                "✅ Chef d'Équipe arrêté proprement",
                extra={"operation": "shutdown_complete"}
            )
            
        except Exception as e:
            self.logger.error(
                "Erreur lors de l'arrêt",
                extra={
                    "operation": "shutdown_error",
                    "error": str(e)
                },
                exc_info=True
            )
    
    async def _attendre_fin_workflows(self, workflows: List[WorkflowMetrics]):
        """Attend la fin des workflows actifs"""
        while any(w.status == WorkflowStatus.RUNNING for w in workflows):
            await asyncio.sleep(1)
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut actuel de l'agent"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "is_running": self._is_running,
            "equipe_size": len(self.equipe_agents),
            "workflows_active": len([w for w in self.workflows_actifs.values() 
                                   if w.status == WorkflowStatus.RUNNING]),
            "logging_centralized": True,
            "timestamp": datetime.now().isoformat()
        }

# Point d'entrée pour tests
async def main():
    """Fonction principale pour tests"""
    # Configuration avec logging centralisé
    config = {
        "logging": logging_manager.generate_agent_logging_config(
            agent_name="chef_equipe_test",
            role="coordinateur",
            domain="coordination",
            agent_id="test_001",
            async_enabled=True
        )
    }
    
    # Créer l'agent
    chef = Agent0ChefEquipeCoordinateur(**config)
    
    try:
        # Démarrer l'agent
        await chef.startup()
        
        # Exécuter un workflow de test
        result = await chef.executer_workflow(
            "maintenance_complete",
            {"target": "test_module"}
        )
        
        print(f"Résultat workflow: {result}")
        
        # Health check
        health = await chef.health_check()
        print(f"Health status: {health}")
        
    finally:
        # Arrêt propre
        await chef.shutdown()

if __name__ == "__main__":
    asyncio.run(main())



