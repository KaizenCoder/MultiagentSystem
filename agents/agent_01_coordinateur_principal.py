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
from core import logging_manager

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
        elif task.description == "GENERATE_STRATEGIC_REPORT":
            # Extraire les paramètres de la tâche
            context = getattr(task, 'context', {})
            type_rapport = getattr(task, 'type_rapport', 'global')
            format_sortie = getattr(task, 'format_sortie', 'json')  # 'json' ou 'markdown'
            
            rapport = await self.generer_rapport_strategique(context, type_rapport)
            
            # Génération format markdown si demandé
            if format_sortie == 'markdown':
                rapport_md = await self.generer_rapport_markdown(rapport, type_rapport, context)
                
                # Sauvegarde dans /reports/
                import os
                from datetime import datetime
                reports_dir = "/mnt/c/Dev/nextgeneration/reports"
                os.makedirs(reports_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                filename = f"strategic_report_agent_01_coordinateur_{type_rapport}_{timestamp}.md"
                filepath = os.path.join(reports_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(rapport_md)
                
                return Result(success=True, data={
                    'rapport_json': rapport, 
                    'rapport_markdown': rapport_md,
                    'fichier_sauvegarde': filepath
                })
            
            return Result(success=True, data=rapport)
        else:
            return Result(success=False, error="Tâche non reconnue")

    async def generer_rapport_strategique(self, context: Dict[str, Any], type_rapport: str = 'global') -> Dict[str, Any]:
        """
        📊 Génération de rapports stratégiques pour la coordination et l'orchestration
        
        Args:
            context: Contexte et données pour le rapport
            type_rapport: Type de rapport ('global', 'sprint', 'performance', 'qualite')
            
        Returns:
            Dict contenant le rapport stratégique complet
        """
        self.logger.info(f"🎯 Génération rapport stratégique type: {type_rapport}")
        
        timestamp = datetime.now()
        
        # Collecte des métriques de base
        metriques_base = await self._collecter_metriques_coordination()
        
        if type_rapport == 'global':
            return await self._generer_rapport_global(context, metriques_base, timestamp)
        elif type_rapport == 'sprint':
            return await self._generer_rapport_sprint(context, metriques_base, timestamp)
        elif type_rapport == 'performance':
            return await self._generer_rapport_performance(context, metriques_base, timestamp)
        elif type_rapport == 'qualite':
            return await self._generer_rapport_qualite(context, metriques_base, timestamp)
        else:
            # Rapport par défaut si type non reconnu
            return await self._generer_rapport_global(context, metriques_base, timestamp)

    async def _collecter_metriques_coordination(self) -> Dict[str, Any]:
        """Collecte les métriques de coordination et orchestration"""
        try:
            # Analyse de l'état des sprints
            sprints_actifs = [s for s in self.sprints_roadmap.values() 
                            if s.get('status') == SprintStatus.IN_PROGRESS]
            sprints_completes = [s for s in self.sprints_roadmap.values() 
                               if s.get('status') == SprintStatus.COMPLETED]
            
            # Analyse de progression globale
            progression_totale = 0
            for sprint in self.sprints_roadmap.values():
                objectifs_completes = sum(1 for obj in sprint.get('objectifs', []) 
                                        if obj.startswith('✅'))
                total_objectifs = len(sprint.get('objectifs', []))
                if total_objectifs > 0:
                    progression_totale += (objectifs_completes / total_objectifs)
            
            progression_moyenne = (progression_totale / len(self.sprints_roadmap)) * 100
            
            # Métriques de coordination
            agents_assignes = set()
            for sprint in self.sprints_roadmap.values():
                agents_assignes.update(sprint.get('agents_assignes', []))
            
            return {
                'sprints_total': len(self.sprints_roadmap),
                'sprints_actifs': len(sprints_actifs),
                'sprints_completes': len(sprints_completes),
                'progression_moyenne': progression_moyenne,
                'agents_coordonnes': len(agents_assignes),
                'tracking_data': self.tracking,
                'derniere_maj': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erreur collecte métriques coordination: {e}")
            return {'erreur': str(e), 'metriques_partielles': True}

    async def _generer_rapport_global(self, context: Dict, metriques: Dict, timestamp: datetime) -> Dict[str, Any]:
        """Génère un rapport stratégique global de coordination"""
        
        # Calcul des scores de performance
        score_coordination = min(100, metriques.get('progression_moyenne', 0) + 
                               (metriques.get('sprints_completes', 0) * 10))
        score_efficacite = min(100, (metriques.get('agents_coordonnes', 0) / 17) * 100)
        
        # Recommandations stratégiques
        recommandations = []
        if metriques.get('progression_moyenne', 0) < 70:
            recommandations.append("🔥 CRITIQUE: Accélérer la progression des sprints - <70%")
        if metriques.get('sprints_actifs', 0) > 2:
            recommandations.append("⚠️ ATTENTION: Trop de sprints actifs simultanément")
        if score_efficacite < 80:
            recommandations.append("📈 OPTIMISATION: Améliorer la coordination des agents")
        
        if not recommandations:
            recommandations.append("✅ EXCELLENT: Coordination optimale maintenue")
            
        # Points d'attention critiques
        points_critiques = []
        for sprint_id, sprint in self.sprints_roadmap.items():
            if sprint.get('status') == SprintStatus.BLOCKED:
                points_critiques.append(f"Sprint {sprint_id} bloqué: {sprint.get('nom')}")
        
        return {
            'type_rapport': 'coordination_globale',
            'timestamp': timestamp.isoformat(),
            'agent_id': self.agent_id,
            'periode_analyse': context.get('periode', 'actuelle'),
            
            'resume_executif': {
                'score_coordination_global': score_coordination,
                'score_efficacite_equipe': score_efficacite,
                'sprints_progression': f"{metriques.get('progression_moyenne', 0):.1f}%",
                'agents_coordonnes': metriques.get('agents_coordonnes', 0),
                'statut_general': 'OPTIMAL' if score_coordination > 80 else 'ATTENTION' if score_coordination > 60 else 'CRITIQUE'
            },
            
            'metriques_detaillees': metriques,
            
            'analyse_sprints': {
                'total': metriques.get('sprints_total', 0),
                'actifs': metriques.get('sprints_actifs', 0),
                'completes': metriques.get('sprints_completes', 0),
                'progression_moyenne': metriques.get('progression_moyenne', 0)
            },
            
            'recommandations_strategiques': recommandations,
            'points_attention_critiques': points_critiques,
            
            'prochaines_actions': [
                "Suivre progression sprint actuel",
                "Coordonner agents assignés",
                "Identifier blocages potentiels",
                "Optimiser allocation ressources"
            ],
            
            'metadonnees': {
                'version_rapport': '1.0',
                'agent_version': 'coordinateur_v3.5',
                'fiabilite_donnees': 'haute' if not metriques.get('metriques_partielles') else 'partielle'
            }
        }

    async def _generer_rapport_sprint(self, context: Dict, metriques: Dict, timestamp: datetime) -> Dict[str, Any]:
        """Génère un rapport spécialisé sur les sprints"""
        sprint_focus = context.get('sprint_id', self.sprint_actuel)
        sprint_data = self.sprints_roadmap.get(sprint_focus, {})
        
        objectifs_completes = sum(1 for obj in sprint_data.get('objectifs', []) 
                                if obj.startswith('✅'))
        total_objectifs = len(sprint_data.get('objectifs', []))
        progression_sprint = (objectifs_completes / total_objectifs * 100) if total_objectifs > 0 else 0
        
        return {
            'type_rapport': 'analyse_sprint',
            'timestamp': timestamp.isoformat(),
            'sprint_focus': sprint_focus,
            'progression_sprint': progression_sprint,
            'objectifs_completes': objectifs_completes,
            'objectifs_total': total_objectifs,
            'agents_assignes': sprint_data.get('agents_assignes', []),
            'duree_prevue': sprint_data.get('duree_semaines', 0),
            'recommandation_prioritaire': 'Maintenir le rythme' if progression_sprint > 75 else 'Accélérer execution'
        }

    async def _generer_rapport_performance(self, context: Dict, metriques: Dict, timestamp: datetime) -> Dict[str, Any]:
        """Génère un rapport axé performance de coordination"""
        
        # Calculs de performance
        velocite_moyenne = metriques.get('progression_moyenne', 0) / 7  # Par jour
        efficacite_coordination = (metriques.get('agents_coordonnes', 0) / 17) * 100
        
        return {
            'type_rapport': 'performance_coordination',
            'timestamp': timestamp.isoformat(),
            'velocite_moyenne_jour': round(velocite_moyenne, 2),
            'efficacite_coordination': round(efficacite_coordination, 1),
            'tendance': 'croissante' if velocite_moyenne > 5 else 'stable',
            'goulots_etranglement': [
                "Communication inter-agents" if efficacite_coordination < 80 else None,
                "Synchronisation sprints" if metriques.get('sprints_actifs', 0) > 2 else None
            ],
            'optimisations_proposees': [
                "Automatiser reporting agents",
                "Optimiser workflows coordination",
                "Améliorer monitoring temps réel"
            ]
        }

    async def _generer_rapport_qualite(self, context: Dict, metriques: Dict, timestamp: datetime) -> Dict[str, Any]:
        """Génère un rapport axé qualité de coordination"""
        
        # Évaluation qualité
        completude_donnees = 100 if not metriques.get('metriques_partielles') else 75
        coherence_planification = 90 if metriques.get('sprints_actifs', 0) <= 2 else 60
        
        score_qualite_global = (completude_donnees + coherence_planification) / 2
        
        return {
            'type_rapport': 'qualite_coordination',
            'timestamp': timestamp.isoformat(),
            'score_qualite_global': round(score_qualite_global, 1),
            'completude_donnees': completude_donnees,
            'coherence_planification': coherence_planification,
            'conformite_processus': 95,  # Basé sur respect méthodologie
            'axes_amelioration': [
                "Standardisation reporting" if completude_donnees < 90 else None,
                "Optimisation planification" if coherence_planification < 80 else None
            ],
            'certification_qualite': 'ISO_COORD_2025' if score_qualite_global > 85 else 'EN_COURS'
        }

    async def generer_rapport_markdown(self, rapport_json: Dict[str, Any], type_rapport: str, context: Dict[str, Any]) -> str:
        """
        📝 Génération de rapports stratégiques au format Markdown
        
        Args:
            rapport_json: Rapport JSON source
            type_rapport: Type de rapport généré
            context: Contexte de génération
            
        Returns:
            str: Rapport formaté en Markdown
        """
        self.logger.info(f"🎯 Génération rapport Markdown type: {type_rapport}")
        
        timestamp = datetime.now()
        
        if type_rapport == 'global':
            return await self._generer_markdown_global(rapport_json, context, timestamp)
        elif type_rapport == 'sprint':
            return await self._generer_markdown_sprint(rapport_json, context, timestamp)
        elif type_rapport == 'performance':
            return await self._generer_markdown_performance(rapport_json, context, timestamp)
        elif type_rapport == 'qualite':
            return await self._generer_markdown_qualite(rapport_json, context, timestamp)
        else:
            return await self._generer_markdown_global(rapport_json, context, timestamp)

    async def _generer_markdown_global(self, rapport: Dict, context: Dict, timestamp: datetime) -> str:
        """Génère un rapport global au format Markdown"""
        
        resume = rapport.get('resume_executif', {})
        recommandations = rapport.get('recommandations_strategiques', [])
        actions = rapport.get('prochaines_actions', [])
        metadonnees = rapport.get('metadonnees', {})
        
        md_content = f"""# 📊 Rapport Stratégique Global - Coordination & Orchestration

**Agent :** {rapport.get('agent_id', 'unknown')}  
**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Type :** {rapport.get('type_rapport', 'coordination_globale')}  
**Période :** {rapport.get('periode_analyse', 'actuelle')}

---

## 🎯 Résumé Exécutif

| Métrique | Valeur | Statut |
|----------|--------|--------|
| **Score Coordination Global** | {resume.get('score_coordination_global', 0)}/100 | {resume.get('statut_general', 'UNKNOWN')} |
| **Score Efficacité Équipe** | {resume.get('score_efficacite_equipe', 0)}/100 | {'🟢' if resume.get('score_efficacite_equipe', 0) > 80 else '🟡' if resume.get('score_efficacite_equipe', 0) > 60 else '🔴'} |
| **Progression Sprints** | {resume.get('sprints_progression', '0%')} | {'🟢' if float(resume.get('sprints_progression', '0%').replace('%', '')) > 75 else '🟡' if float(resume.get('sprints_progression', '0%').replace('%', '')) > 50 else '🔴'} |
| **Agents Coordonnés** | {resume.get('agents_coordonnes', 0)}/17 | {'🟢' if resume.get('agents_coordonnes', 0) >= 15 else '🟡' if resume.get('agents_coordonnes', 0) >= 10 else '🔴'} |

### 📈 Analyse Sprints

"""
        
        analyse_sprints = rapport.get('analyse_sprints', {})
        md_content += f"""
| Indicateur | Valeur |
|------------|--------|
| Total Sprints | {analyse_sprints.get('total', 0)} |
| Sprints Actifs | {analyse_sprints.get('actifs', 0)} |
| Sprints Complétés | {analyse_sprints.get('completes', 0)} |
| Progression Moyenne | {analyse_sprints.get('progression_moyenne', 0):.1f}% |

---

## 🎯 Recommandations Stratégiques

"""
        
        for i, rec in enumerate(recommandations, 1):
            md_content += f"{i}. {rec}\n"
        
        md_content += f"""
---

## 📅 Prochaines Actions

"""
        
        for i, action in enumerate(actions, 1):
            md_content += f"- [ ] {action}\n"
        
        points_critiques = rapport.get('points_attention_critiques', [])
        if points_critiques:
            md_content += f"""
---

## ⚠️ Points d'Attention Critiques

"""
            for point in points_critiques:
                md_content += f"- 🔴 {point}\n"
        
        md_content += f"""
---

## 📋 Métadonnées

- **Version Rapport :** {metadonnees.get('version_rapport', '1.0')}
- **Agent Version :** {metadonnees.get('agent_version', 'unknown')}
- **Fiabilité Données :** {metadonnees.get('fiabilite_donnees', 'normale')}
- **Contexte :** {context.get('objectif', 'analyse_generale')}

---

*Rapport généré automatiquement par Agent 01 - Coordinateur Principal*  
*🤖 NextGeneration Strategic Reporting System*
"""
        
        return md_content

    async def _generer_markdown_sprint(self, rapport: Dict, context: Dict, timestamp: datetime) -> str:
        """Génère un rapport sprint au format Markdown"""
        
        md_content = f"""# 🏃 Rapport Sprint Spécialisé

**Sprint Focus :** {rapport.get('sprint_focus', 'unknown')}  
**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Type :** {rapport.get('type_rapport', 'analyse_sprint')}

---

## 📊 Progression Sprint

- **Progression :** {rapport.get('progression_sprint', 0):.1f}%
- **Objectifs Complétés :** {rapport.get('objectifs_completes', 0)}/{rapport.get('objectifs_total', 0)}
- **Durée Prévue :** {rapport.get('duree_prevue', 0)} semaines

## 👥 Équipe

**Agents Assignés :** {', '.join(rapport.get('agents_assignes', []))}

## 🎯 Recommandation Prioritaire

> {rapport.get('recommandation_prioritaire', 'Maintenir le rythme')}

---

*Rapport Sprint généré par Agent 01 - Coordinateur Principal*
"""
        
        return md_content

    async def _generer_markdown_performance(self, rapport: Dict, context: Dict, timestamp: datetime) -> str:
        """Génère un rapport performance au format Markdown"""
        
        md_content = f"""# ⚡ Rapport Performance Coordination

**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Type :** {rapport.get('type_rapport', 'performance_coordination')}

---

## 📈 Métriques Performance

| Métrique | Valeur |
|----------|--------|
| **Vélocité Moyenne/Jour** | {rapport.get('velocite_moyenne_jour', 0)} |
| **Efficacité Coordination** | {rapport.get('efficacite_coordination', 0)}% |
| **Tendance** | {rapport.get('tendance', 'stable')} |

## 🚫 Goulots d'Étranglement

"""
        
        goulots = [g for g in rapport.get('goulots_etranglement', []) if g]
        if goulots:
            for goulot in goulots:
                md_content += f"- ⚠️ {goulot}\n"
        else:
            md_content += "- ✅ Aucun goulot d'étranglement détecté\n"
        
        md_content += """
## 🔧 Optimisations Proposées

"""
        
        for opt in rapport.get('optimisations_proposees', []):
            md_content += f"- 💡 {opt}\n"
        
        md_content += """
---

*Rapport Performance généré par Agent 01 - Coordinateur Principal*
"""
        
        return md_content

    async def _generer_markdown_qualite(self, rapport: Dict, context: Dict, timestamp: datetime) -> str:
        """Génère un rapport qualité au format Markdown"""
        
        md_content = f"""# 🎯 Rapport Qualité Coordination

**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Type :** {rapport.get('type_rapport', 'qualite_coordination')}

---

## 📊 Scores Qualité

| Dimension | Score |
|-----------|-------|
| **Qualité Globale** | {rapport.get('score_qualite_global', 0)}/100 |
| **Complétude Données** | {rapport.get('completude_donnees', 0)}% |
| **Cohérence Planification** | {rapport.get('coherence_planification', 0)}% |
| **Conformité Processus** | {rapport.get('conformite_processus', 0)}% |

## 📋 Certification

**Niveau :** {rapport.get('certification_qualite', 'EN_COURS')}

## 🔧 Axes d'Amélioration

"""
        
        axes = [axe for axe in rapport.get('axes_amelioration', []) if axe]
        if axes:
            for axe in axes:
                md_content += f"- 🎯 {axe}\n"
        else:
            md_content += "- ✅ Qualité optimale atteinte\n"
        
        md_content += """
---

*Rapport Qualité généré par Agent 01 - Coordinateur Principal*
"""
        
        return md_content

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
