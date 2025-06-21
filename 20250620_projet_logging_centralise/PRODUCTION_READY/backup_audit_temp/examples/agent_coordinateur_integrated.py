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

# Import du système de logging centralisé "Golden Source"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import logging_manager

# Import des métriques et monitoring
# from ..monitoring.metrics_collector import MetricsCollector
# from ..monitoring.health_monitor import HealthMonitor
# Pour le test, on désactive les autres imports pour se concentrer sur le logging
MetricsCollector = HealthMonitor = lambda x: None

class WorkflowStatus(Enum):
    """États possibles d'un workflow"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class WorkflowMetrics:
    """Métriques pour un workflow"""
    workflow_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: WorkflowStatus = WorkflowStatus.PENDING
    agents_involved: List[str] = field(default_factory=list)
    tasks_completed: int = 0
    tasks_total: int = 0
    errors: List[Dict[str, Any]] = field(default_factory=list)
    performance_data: Dict[str, float] = field(default_factory=dict)

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
        
        # Le manager choisira la config par défaut 'nextgen.default'
        # ou on pourrait créer une config 'agent_default'
        self.logger = logging_manager.get_logger('agent_coordinateur')
        self.async_logging = True # On le suppose pour le test
        
        # Logger d'audit pour actions critiques
        self.audit_logger = logging_manager.get_audit_logger()
        
        # Configuration équipe et chemins
        self.target_path = Path(target_path) if target_path else Path("../agent_factory_implementation/agents")
        self.workspace_path = Path(workspace_path) if workspace_path else Path(".")
        
        # État interne
        self.equipe_agents = {}
        self.workflows_disponibles = self._charger_workflows_disponibles()
        self.workflows_actifs: Dict[str, WorkflowMetrics] = {}
        self._is_running = False
        
        # Métadonnées NextGeneration
        self.nextgen_metadata = config.get("nextgen_metadata", {})
        
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
        start_time = time.perf_counter()
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
            # await self._demarrer_monitoring() # Désactivé pour le test
            
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
            
            # Log de performance manuel
            exec_time = time.perf_counter() - start_time
            logging_manager.log_performance("agent_startup", exec_time)
            
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
            
            # Log de performance pour l'échec
            exec_time = time.perf_counter() - start_time
            logging_manager.log_performance("agent_startup_failed", exec_time)
            
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
                
                with logging_manager.log_performance("periodic_maintenance", self.logger):
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
        """Exécute un workflow de bout en bout avec logging et métriques."""
        start_time_workflow = time.perf_counter()
        
        workflow_id = f"wf_{workflow_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.logger.info(
            f"🔄 Démarrage workflow: {workflow_type}",
            extra={
                "workflow_id": workflow_id,
                "type": workflow_type,
                "parameters": parametres
            }
        )
        
        # Création des métriques
        workflow_metrics = WorkflowMetrics(
            workflow_id=workflow_id,
            start_time=datetime.now(),
            agents_involved=[],
            tasks_total=len(self.equipe_agents)  # Simulation
        )
        self.workflows_actifs[workflow_id] = workflow_metrics
        
        try:
            # Exécution interne
            result = await self._executer_workflow_interne(
                workflow_id, workflow_type, parametres, workflow_metrics
            )
            
            # Log de performance global
            exec_time = time.perf_counter() - start_time_workflow
            logging_manager.log_performance(f"workflow_{workflow_type}_success", exec_time)
            
            # Mise à jour et sauvegarde
            workflow_metrics.status = WorkflowStatus.COMPLETED
            workflow_metrics.end_time = datetime.now()
            await self._sauvegarder_rapport_workflow(workflow_id, result, workflow_metrics)
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Échec du workflow: {workflow_type}", extra={
                "workflow_id": workflow_id,
                "error_type": type(e).__name__,
                "error_message": str(e)
            })

            # Log de performance
            exec_time = time.perf_counter() - start_time_workflow
            logging_manager.log_performance(f"workflow_{workflow_type}_failed", exec_time)

            return {
                "status": "failed",
                "workflow_id": workflow_id,
                "error": str(e)
            }
    
    async def _executer_workflow_interne(
        self,
        workflow_id: str,
        workflow_type: str,
        parametres: Dict[str, Any],
        metrics: WorkflowMetrics
    ) -> Dict[str, Any]:
        """
        Exécute la logique interne d'un workflow avec logging de performance.
        """
        start_time = time.perf_counter()
        try:
            # Simulation d'exécution de workflow
            self.logger.info(f"Début de l'exécution interne du workflow: {workflow_type}", extra={"workflow_id": workflow_id})
            await asyncio.sleep(0.1) # Simuler le travail
            result = {"status": "completed", "details": f"Résultat de {workflow_type}"}
            self.logger.info(f"Fin de l'exécution interne du workflow: {workflow_type}", extra={"workflow_id": workflow_id})
            
            # Log de performance
            exec_time = time.perf_counter() - start_time
            logging_manager.log_performance(f"workflow_interne_{workflow_type}", exec_time)
            
            return result
        except Exception as e:
            exec_time = time.perf_counter() - start_time
            logging_manager.log_performance(f"workflow_interne_{workflow_type}_failed", exec_time)
            self.logger.error(f"Erreur dans le workflow interne {workflow_type}: {e}", exc_info=True)
            raise
    
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
        """Nettoie les workflows terminés de la liste active"""
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
        """Collecte les métriques de l'agent (version désactivée)"""
        return {"status": "metrics_disabled"}
    
    async def health_check(self) -> Dict[str, Any]:
        """Effectue un bilan de santé de l'agent (version désactivée)"""
        return {"status": "health_check_disabled"}
    
    async def shutdown(self):
        """Arrête proprement l'agent et ses composants."""
        self.logger.info("🎬 Arrêt de l'agent coordinateur...")
        self._is_running = False
        
        # Attendre la fin des workflows en cours (avec timeout)
        # await self._attendre_fin_workflows(list(self.workflows_actifs.values()))
        
        # Arrêt des composants de monitoring
        # if hasattr(self, 'health_monitor'):
        #     await self.health_monitor.stop()
            
        # Log final
        shutdown_time = datetime.now().isoformat()
        self.logger.info(f"Agent {self.agent_id} arrêté à {shutdown_time}.")
        
        return {"status": "shutdown", "timestamp": shutdown_time}
    
    async def _attendre_fin_workflows(self, workflows: List[WorkflowMetrics]):
        # ... logique ...
        pass
    
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
    """Fonction principale pour exécuter l'agent."""
    print("--- Démarrage du Coordinateur d'Agents NextGeneration ---")
    
    # Utilisation du nouveau logging_manager
    main_logger = logging_manager.get_logger('main_runner')
    
    agent = Agent0ChefEquipeCoordinateur(
        agent_id="coord_main_001",
        workspace_path="./temp_workspace"
    )
    
    try:
        startup_info = await agent.startup()
        main_logger.info("Agent démarré avec succès.", extra={"startup_info": startup_info})
        
        # Simuler l'exécution d'un workflow
        workflow_params = {"target_file": "some/file.py", "complexity_level": "high"}
        workflow_result = await agent.executer_workflow("maintenance_complete", workflow_params)
        main_logger.info("Workflow exécuté.", extra={"result": workflow_result})
        
    except Exception as e:
        main_logger.critical(f"Une erreur critique a arrêté l'agent: {e}", exc_info=True)
        
    finally:
        if agent and agent.get_status().get('is_running'):
            shutdown_info = await agent.shutdown()
            main_logger.info("Agent arrêté proprement.", extra={"shutdown_info": shutdown_info})

if __name__ == "__main__":
    # Lancer l'agent
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nArrêt manuel demandé.")



