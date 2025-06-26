#!/usr/bin/env python3
"""
# 🔧 CONVERTI AUTOMATIQUEMENT SYNC → ASYNC
# Date: 2025-06-19 19h35 - Correction architecture Pattern Factory
# Raison: Harmonisation async/sync avec core/agent_factory_architecture.py

👑 AGENT 01 - COORDINATEUR PRINCIPAL
Sprint 3-5 - Orchestration générale et coordination équipe

Mission : Orchestration générale, suivi progression, rapports détaillés
Coordination : Équipe 17 agents selon roadmap optimisée
Performance : Suivi vélocité, qualité, conformité plans experts
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json
import subprocess
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

# Import direct et robuste de l'architecture de base
from core.agent_factory_architecture import Agent, Task, Result
from core.logging_core import logging_manager

# --- NOUVELLE GESTION DE LA CONFIGURATION (ROBUSTE) ---
# Abandon de l'import direct de 'agent_config.py' qui était source d'erreurs.
# On utilise maintenant les modèles Pydantic et le fichier JSON généré par l'Agent 03.
try:
    from core.config_models_agent.config_models_maintenance import MaintenanceTeamConfig, get_maintenance_config
    CONFIG_SYSTEM_AVAILABLE = True
except ImportError as e:
    logging_manager.get_logger().error(f"Impossible d'importer le nouveau système de configuration: {e}")
    CONFIG_SYSTEM_AVAILABLE = False
    # On pourrait définir des fallbacks ici si nécessaire

class SprintStatus(Enum):
    """Status des sprints"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"

class AgentStatus(Enum):
    """Status des agents"""
    OPERATIONAL = "operational"
    TO_CREATE = "to_create"
    IN_DEVELOPMENT = "in_development"
    BLOCKED = "blocked"

@dataclass
class SprintMetrics:
    """Métriques sprint"""
    sprint_id: int
    status: SprintStatus
    progress_percentage: float
    quality_score: float
    agents_operational: int
    agents_total: int
    dod_compliance: float
    critical_issues: int
    completion_date: Optional[datetime]

@dataclass
class AgentMetrics:
    """Métriques agent"""
    agent_id: str
    status: AgentStatus
    quality_score: float
    mission_completion: float
    last_activity: datetime
    critical_issues: int

def classify_exception(exc: Exception) -> str:
    """
    Classe les exceptions pour orienter la stratégie de réparation.
    """
    if isinstance(exc, (IndentationError, TabError)) or ("indent" in str(exc).lower()):
        return "indentation"
    if isinstance(exc, NameError):
        return "name"
    if isinstance(exc, (ImportError, ModuleNotFoundError)):
        return "import"
    # ... autres classes à ajouter selon besoin
    return "generic"

class Agent01CoordinateurPrincipal(Agent):
    """
    👑 Agent 01 - Coordinateur Principal
    
    Responsabilités :
    - Orchestration équipe 17 agents selon roadmap optimisée
    - Suivi document tracking temps réel (Sprint 0→5)
    - Rapports détaillés à chaque étape avec métriques
    - Validation livrables selon plans experts
    - Mesure performance équipe (vélocité, qualité)
    - Coordination reviews entre agents
    - Gestion risques et mitigations
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            agent_id="agent_01_coordinateur_principal",
            version="1.2",
            description="Orchestration Sprints 3-5 production-ready",
            agent_type="coordinateur",
            status="operational",
            **kwargs
        )
        self.specialite = "Coordination Générale & Orchestration"
        self.mission = "Orchestration Sprints 3-5 production-ready"
        self.sprint_actuel = 3
        
        self.agents_equipe = self._initialiser_equipe()
        self.sprints_roadmap = self._initialiser_roadmap()
        self.metriques_globales = {}
        
        self.tracking = {
            'agent_id': self.agent_id,
            'mission_status': 'DÉMARRAGE',
            'sprint_actuel': self.sprint_actuel,
            'timestamp_debut': datetime.now().isoformat(),
            'progression_globale': 0.0,
            'qualite_moyenne': 0.0,
            'agents_operationnels': 0,
            'agents_total': 17
        }
        self.logger.info(f"👑 Agent {self.agent_id} - {self.specialite} - Sprints 3-5 DÉMARRÉ")


    def _initialiser_equipe(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialisation de l'équipe en chargeant la configuration depuis le fichier JSON.
        Ceci remplace la liste hardcodée et la dépendance à l'ancien agent_config.
        """
        if not CONFIG_SYSTEM_AVAILABLE:
            self.logger.error("Le système de configuration n'est pas disponible. Utilisation d'une équipe vide.")
            return {}

        try:
            config = get_maintenance_config()
            # Transformer la configuration Pydantic en dictionnaire simple pour l'agent
            equipe = {}
            for role, agent_config in config.agents.items():
                equipe[agent_config.nom_agent.split('_')[1]] = {
                    "nom": agent_config.description,
                    "status": AgentStatus.OPERATIONAL, # A déterminer dynamiquement plus tard
                    "sprint": [], # A peupler si nécessaire
                }
            self.logger.info("Équipe initialisée avec succès depuis la configuration JSON.")
            return equipe
        except Exception as e:
            self.logger.critical(f"Échec critique de l'initialisation de l'équipe via la config JSON: {e}", exc_info=True)
            return {}

    def _initialiser_roadmap(self) -> Dict[int, Dict[str, Any]]:
        """Initialisation roadmap Sprints 3-5"""
        return {
            3: {
                "nom": "Control/Data Plane & Sandbox",
                "status": SprintStatus.IN_PROGRESS,
                "objectifs": [
                    "Architecture Control/Data Plane séparée",
                    "Sandbox WASI sécurisé < 20% overhead",
                    "RBAC FastAPI intégré",
                    "Audit trail complet"
                ],
                "agents_assignes": ["agent_09", "agent_11", "agent_01"],
                "dod_criteria": 8,
                "duree_semaines": 1,
                "date_debut": datetime.now(),
                "date_fin_prevue": datetime.now() + timedelta(weeks=1)
            },
            4: {
                "nom": "Observabilité Avancée & Performance",
                "status": SprintStatus.NOT_STARTED,
                "objectifs": [
                    "OpenTelemetry tracing distribué",
                    "Métriques Prometheus p95, cache, TTL",
                    "ThreadPool auto-tuned CPU × 2",
                    "Performance < 50ms/agent validée"
                ],
                "agents_assignes": ["agent_08", "agent_12", "agent_13"],
                "dod_criteria": 6,
                "duree_semaines": 1,
                "date_debut": datetime.now() + timedelta(weeks=1),
                "date_fin_prevue": datetime.now() + timedelta(weeks=2)
            },
            5: {
                "nom": "Déploiement Kubernetes Production",
                "status": SprintStatus.NOT_STARTED,
                "objectifs": [
                    "Helm charts blue-green deploy",
                    "Chaos engineering 25% nodes off",
                    "SLA < 100ms p95 production",
                    "Runbook opérateur complet"
                ],
                "agents_assignes": ["agent_07"],
                "dod_criteria": 5,
                "duree_semaines": 1,
                "date_debut": datetime.now() + timedelta(weeks=2),
                "date_fin_prevue": datetime.now() + timedelta(weeks=3)
            }
        }

    async def execute_task(self, task: Task) -> Result:
        self.logger.info(f"Tâche reçue: {task.task_id} - {task.description}")
        if task.description == "EVALUER_PROGRESSION_SPRINT_3":
            metrics = await self.evaluer_progression_sprint3()
            return Result(success=True, data=metrics)
        else:
            return Result(success=False, error="Tâche non reconnue")

    async def evaluer_progression_sprint3(self) -> Dict[str, Any]:
        """
        📊 Évaluation progression Sprint 3 actuel
        
        Returns:
            Dict avec métriques progression Sprint 3
        """
        self.logger.info("📊 Évaluation progression Sprint 3")
        
        # Exemple: Simuler une vérification de l'agent 09
        try:
            result = await self.communiquer_avec_agent("agent_09", "GET_STATUS_CONTROL_PLANE")
            if result and result.get("status") == "COMPLETED":
                self.sprints_roadmap[3]["objectifs"][0] = "✅ " + self.sprints_roadmap[3]["objectifs"][0]
        except Exception as e:
            self.logger.error(f"Erreur communication agent_09: {e}")

        progression = sum(1 for o in self.sprints_roadmap[3]["objectifs"] if o.startswith("✅"))
        total_objectifs = len(self.sprints_roadmap[3]["objectifs"])
        progression_pct = (progression / total_objectifs) * 100
        
        self.tracking['progression_globale'] = progression_pct
        self.logger.info(f"Progression Sprint 3: {progression_pct:.2f}%")
        
        return {"sprint_id": 3, "progression": progression_pct, "details": self.sprints_roadmap[3]}

    async def communiquer_avec_agent(self, agent_id: str, action: str) -> Optional[Dict]:
        """Simulation de communication asynchrone avec un autre agent."""
        self.logger.info(f"Communication avec {agent_id} pour l'action '{action}'...")
        try:
            # Ici, on simulerait l'appel réel à un autre agent
            # Par exemple, via un bus de messages ou un appel RPC/HTTP
            await asyncio.sleep(0.1)  # Simule la latence réseau
            if agent_id == "agent_09" and action == "GET_STATUS_CONTROL_PLANE":
                # Simuler une erreur pour tester la classification
                # raise NameError("test_name_error")
                return {"status": "COMPLETED", "details": "Control Plane implémenté."}
            return {"status": "UNKNOWN_ACTION"}
        except Exception as e:
            error_type = classify_exception(e)
            self.logger.error(
                f"Échec communication avec {agent_id}. "
                f"Type d'erreur détecté : '{error_type}'. "
                f"Erreur originale : {e}"
            )
            # Ici, on pourrait déclencher une tâche de réparation ciblée
            # en fonction de `error_type`.
            return {"status": "FAILED", "error": str(e), "error_type": error_type}

    async def startup(self):
        self.logger.info(f"Agent {self.agent_id} démarré et opérationnel.")

    async def shutdown(self):
        self.logger.info(f"Agent {self.agent_id} arrêté.")

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "sprint_actuel": self.sprint_actuel}


def create_agent_01_coordinateur_principal(**config) -> "Agent01CoordinateurPrincipal":
    """Factory function pour créer l'agent."""
    return Agent01CoordinateurPrincipal(**config)
