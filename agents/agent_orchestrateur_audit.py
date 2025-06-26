#!/usr/bin/env python3
"""

# 🔧 CONVERTI AUTOMATIQUEMENT SYNC → ASYNC
# Date: 2025-06-19 19h35 - Correction architecture Pattern Factory
# Raison: Harmonisation async/sync avec core/agent_factory_architecture.py

🎯 AGENT ORCHESTRATEUR AUDIT - Coordination Équipe Auditeurs
Mission : Orchestration complète de l'équipe d'agents auditeurs spécialisés

Responsabilités :
- Coordination Agent 18 (Sécurité), Agent 19 (Performance), Agent 20 (Conformité)
- Orchestration audits parallèles et séquentiels
- Consolidation rapports d'audit
- Génération rapport exécutif global
- Priorisation des actions correctives
- Suivi des améliorations
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
from dataclasses import dataclass
from enum import Enum
import logging

# Import Pattern Factory (OBLIGATOIRE)
try:
    from core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
    print("⚠️ Pattern Factory non disponible. Utilisation des classes de fallback.")
    PATTERN_FACTORY_AVAILABLE = False
    
    class Agent:
        def __init__(self, agent_type: str, **config):
            self.agent_id = f"fallback_{agent_type}"
            self.agent_type = agent_type
            self.logger = logging.getLogger(self.agent_id)
        async def startup(self): pass
        async def shutdown(self): pass
        async def health_check(self): return {"status": "healthy"}
        def get_capabilities(self): return []

    class Task:
        def __init__(self, task_id: str, description: str, **kwargs):
            self.task_id = task_id
            self.description = description
            self.data = kwargs

    class Result:
        def __init__(self, success: bool, data: Any = None, error: str = None):
            self.success = success
            self.data = data
            self.error = error

# Import des agents auditeurs
sys.path.insert(0, str(Path(__file__).parent))

try:
    from agent_18_auditeur_securite import Agent18AuditeurSecurite
    AGENT_18_AVAILABLE = True
except ImportError:
    AGENT_18_AVAILABLE = False

try:
    from agent_19_auditeur_performance import Agent19AuditeurPerformance
    AGENT_19_AVAILABLE = True
except ImportError:
    AGENT_19_AVAILABLE = False

class AuditPhase(Enum):
    PREPARATION = "préparation"
    EXECUTION = "exécution"
    CONSOLIDATION = "consolidation"
    REPORTING = "rapport"
    COMPLETE = "terminé"

class AuditPriority(Enum):
    CRITIQUE = "critique"
    HAUTE = "haute"
    MOYENNE = "moyenne"
    BASSE = "basse"

@dataclass
class AuditTask:
    task_id: str
    agent_type: str
    target: str
    priority: AuditPriority
    status: str
    result: Optional[Dict[str, Any]] = None

class AgentOrchestrateurAudit(Agent):
    """
    🎯 Agent Orchestrateur Audit - Pattern Factory Compliant
    
    Coordonne l'équipe complète d'agents auditeurs spécialisés
    pour des audits complets et coordonnés
    """
    
    def __init__(self, workspace_root: Path = None, **config):
        super().__init__(agent_type="orchestrateur_audit", **config)
        self.agent_id = "ORCHESTRATEUR_AUDIT"
        self.specialite = "Orchestration Audit Multi-Agents"
        self.workspace_root = workspace_root if workspace_root else Path(__file__).parent.parent
        
        self.logger = self._setup_logging()

        # Initialisation agents disponibles
        self.agents = {}
        self._initialize_agents()
        
        # État de l'orchestration
        self.current_phase = AuditPhase.PREPARATION
        self.audit_tasks = []
        self.consolidated_results = {}
        
        # Configuration audit
        self.audit_config = {
            'parallel_execution': True,
            'timeout_minutes': 30,
            'retry_on_failure': True,
            'generate_executive_summary': True
        }
        
        self.logger.info(f"🎯 Orchestrateur Audit initialisé avec {len(self.agents)} agents")

    def _initialize_agents(self):
        """Initialisation des agents auditeurs disponibles"""
        
        if AGENT_18_AVAILABLE:
            try:
                self.agents['securite'] = Agent18AuditeurSecurite()
                self.logger.info("✅ Agent 18 Sécurité chargé")
            except Exception as e:
                self.logger.warning(f"⚠️ Erreur chargement Agent 18: {e}")
        
        if AGENT_19_AVAILABLE:
            try:
                self.agents['performance'] = Agent19AuditeurPerformance()
                self.logger.info("✅ Agent 19 Performance chargé")
            except Exception as e:
                self.logger.warning(f"⚠️ Erreur chargement Agent 19: {e}")
        
        # Agent 20 (à implémenter si disponible)
        # try:
        #     from agent_20_auditeur_conformite import Agent20AuditeurConformite
        #     self.agents['conformite'] = Agent20AuditeurConformite()
        #     self.logger.info("✅ Agent 20 Conformité chargé")
        # except ImportError:
        #     self.logger.info("ℹ️ Agent 20 Conformité non disponible")

    def _setup_logging(self):
        """Configuration du logging pour l'orchestrateur."""
        logger = logging.getLogger(f"OrchestrateurAudit.{self.agent_id}")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            log_dir = self.workspace_root / "logs" / "agents" / "orchestrateur_audit"
            log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = log_dir / f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            
            # Handler Fichier
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            
            # Handler Console
            console_handler = logging.StreamHandler(sys.stdout)
            console_formatter = logging.Formatter('🕵️‍ (Orchestrateur) - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
        return logger

    # === MÉTHODES PATTERN FACTORY OBLIGATOIRES ===
    
    async def startup(self) -> bool:
        """Démarrage de l'orchestrateur audit"""
        try:
            self.logger.info("🚀 Démarrage Orchestrateur Audit")
            await self._initialize_agents_async()
            self.logger.info(f"✅ Orchestrateur audit démarré avec {len(self.agents)} agents")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur démarrage orchestrateur: {e}")
            return False
    
    async def shutdown(self) -> bool:
        """Arrêt de l'orchestrateur audit"""
        try:
            self.logger.info("🛑 Arrêt Orchestrateur Audit")
            # Arrêt des agents si ils supportent shutdown
            for agent_name, agent in self.agents.items():
                if hasattr(agent, 'shutdown'):
                    try:
                        await agent.shutdown()
                    except Exception as e:
                        self.logger.warning(f"⚠️ Erreur arrêt agent {agent_name}: {e}")
            self.logger.info("✅ Orchestrateur audit arrêté")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur arrêt orchestrateur: {e}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Vérification de l'état de l'orchestrateur"""
        return {
            "status": "healthy",
            "agent_id": self.agent_id,
            "specialite": self.specialite,
            "agents_disponibles": len(self.agents),
            "phase_actuelle": self.current_phase.value,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_capabilities(self) -> List[str]:
        """Liste des capacités de l'orchestrateur"""
        return [
            "orchestration_audit_multi_agents",
            "coordination_agents_securite_performance_conformite",
            "execution_audits_paralleles",
            "consolidation_rapports_audit",
            "generation_rapport_executif",
            "priorisation_actions_correctives",
            "suivi_ameliorations"
        ]
    
    async def execute_task(self, task: Task) -> Result:
        """Exécution d'une tâche d'orchestration d'audit"""
        try:
            self.logger.info(f"🎯 Exécution tâche: {task.task_id}")
            
            if hasattr(task, 'description') and 'audit_complet' in task.description:
                # Tâche d'audit complet
                targets = task.data.get('targets', [])
                if not targets:
                    return Result(success=False, error="Aucune cible d'audit spécifiée")
                
                rapport = await self.executer_audit_complet(targets)
                
                return Result(success=True, data={
                    "type": "audit_complet",
                    "rapport": rapport,
                    "targets": targets,
                    "agents_utilises": len(self.agents)
                })
            
            else:
                return Result(success=False, error=f"Type de tâche non supporté: {task.description}")
                
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution tâche: {e}")
            return Result(success=False, error=str(e))
    
    async def _initialize_agents_async(self):
        """Initialisation asynchrone des agents"""
        # Initialisation des agents disponibles avec gestion async
        for agent_name, agent in self.agents.items():
            if hasattr(agent, 'startup'):
                try:
                    await agent.startup()
                    self.logger.info(f"✅ Agent {agent_name} initialisé")
                except Exception as e:
                    self.logger.warning(f"⚠️ Erreur initialisation agent {agent_name}: {e}")

    async def executer_audit_complet(self, targets: List[str]) -> Dict[str, Any]:
        """
    🚀 Exécution audit complet multi-agents
        
    Args:
    targets: Liste des cibles à auditer
            
    Returns:
    Rapport consolidé de tous les audits
        """
    self.logger.info(f"🚀 Démarrage audit complet sur {len(targets)} cibles")
        
    audit_id = f"AUDIT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    try:
            # Phase 1: Préparation
    self.current_phase = AuditPhase.PREPARATION
    await self._prepare_audit_tasks(targets)
            
            # Phase 2: Exécution
    self.current_phase = AuditPhase.EXECUTION
    await self._execute_audit_tasks()
            
            # Phase 3: Consolidation
    self.current_phase = AuditPhase.CONSOLIDATION
    consolidated_report = await self._consolidate_results()
            
            # Phase 4: Rapport exécutif
    self.current_phase = AuditPhase.REPORTING
    executive_report = await self._generate_executive_report(audit_id, consolidated_report)
            
    self.current_phase = AuditPhase.COMPLETE
            
            # Sauvegarde rapport final
    await self._save_orchestrator_report(executive_report)
            
    self.logger.info("✅ Audit complet terminé avec succès")
    return executive_report
            
    except Exception as e:
    self.logger.error(f"❌ Erreur audit complet: {e}")
    return {
    'status': 'ERROR',
    'audit_id': audit_id,
    'error': str(e),
    'phase': self.current_phase.value,
    'timestamp': datetime.now().isoformat()
    }

    async def _prepare_audit_tasks(self, targets: List[str]):
        """Préparation des tâches d'audit"""
    self.logger.info("📋 Préparation des tâches d'audit")
        
    self.audit_tasks = []
    task_counter = 0
        
    for target in targets:
    target_path = Path(target)
            
    if not target_path.exists():
    self.logger.warning(f"⚠️ Cible inexistante ignorée: {target}")
    continue
            
            # Détermination priorité basée sur le type de cible
    if target_path.name in ['core', 'main', 'src']:
    priority = AuditPriority.CRITIQUE
    elif target_path.suffix == '.py':
    priority = AuditPriority.HAUTE
    else:
    priority = AuditPriority.MOYENNE
            
            # Création tâche pour chaque agent disponible
    for agent_type in self.agents.keys():
    task_counter += 1
    task = AuditTask(
    task_id=f"TASK_{task_counter:03d}",
    agent_type=agent_type,
    target=target,
    priority=priority,
    status="préparé"
    )
    self.audit_tasks.append(task)
        
    self.logger.info(f"📋 {len(self.audit_tasks)} tâches préparées pour {len(self.agents)} agents")

    async def _execute_audit_tasks(self):
        """Exécution des tâches d'audit"""
    self.logger.info("⚡ Exécution des tâches d'audit")
        
    if self.audit_config['parallel_execution']:
    await self._execute_parallel()
    else:
    await self._execute_sequential()

    async def _execute_parallel(self):
        """Exécution parallèle des audits"""
    self.logger.info("🔄 Exécution parallèle des audits")
        
        # Groupement des tâches par agent
    tasks_by_agent = {}
    for task in self.audit_tasks:
    if task.agent_type not in tasks_by_agent:
    tasks_by_agent[task.agent_type] = []
    tasks_by_agent[task.agent_type].append(task)
        
        # Exécution parallèle par agent
    coroutines = []
    for agent_type, agent_tasks in tasks_by_agent.items():
    coroutines.append(self._execute_agent_tasks(agent_type, agent_tasks))
        
        # Attente de toutes les exécutions
    await asyncio.gather(*coroutines, return_exceptions=True)

    async def _execute_sequential(self):
        """Exécution séquentielle des audits"""
    self.logger.info("📝 Exécution séquentielle des audits")
        
        # Tri par priorité
    sorted_tasks = sorted(self.audit_tasks, key=lambda t: list(AuditPriority).index(t.priority))
        
    for task in sorted_tasks:
    await self._execute_single_task(task)

    async def _execute_agent_tasks(self, agent_type: str, tasks: List[AuditTask]):
        """Exécution des tâches pour un agent spécifique"""
        
    if agent_type not in self.agents:
    self.logger.error(f"❌ Agent {agent_type} non disponible")
    return
        
    agent = self.agents[agent_type]
        
    for task in tasks:
    await self._execute_single_task(task)

    async def _execute_single_task(self, task: AuditTask):
        """Exécution d'une tâche individuelle"""
        
    try:
    self.logger.info(f"🔍 Exécution {task.task_id}: {task.agent_type} sur {task.target}")
            
    task.status = "en_cours"
    agent = self.agents[task.agent_type]
            
            # Appel de la méthode d'audit appropriée
    if task.agent_type == 'securite':
    result = await agent.auditer_securite_complete(task.target)
    elif task.agent_type == 'performance':
    result = await agent.auditer_performance(task.target)
    elif task.agent_type == 'conformite':
    result = await agent.auditer_conformite_complete(task.target)
    else:
    result = {'error': f'Type d\'agent non supporté: {task.agent_type}'}
            
    task.result = result
    task.status = "terminé"
            
    self.logger.info(f"✅ {task.task_id} terminé avec succès")
            
    except Exception as e:
    self.logger.error(f"❌ Erreur {task.task_id}: {e}")
    task.status = "erreur"
    task.result = {'error': str(e)}

    async def _consolidate_results(self) -> Dict[str, Any]:
        """Consolidation des résultats de tous les agents"""
    self.logger.info("📊 Consolidation des résultats")
        
    consolidated = {
    'summary': {
    'total_tasks': len(self.audit_tasks),
    'successful_tasks': 0,
    'failed_tasks': 0,
    'tasks_by_agent': {},
    'tasks_by_priority': {}
    },
    'results_by_agent': {},
    'results_by_target': {},
    'global_metrics': {}
    }
        
        # Consolidation par agent
    for task in self.audit_tasks:
    agent_type = task.agent_type
            
            # Compteurs
    if task.status == "terminé":
    consolidated['summary']['successful_tasks'] += 1
    else:
    consolidated['summary']['failed_tasks'] += 1
            
            # Par agent
    if agent_type not in consolidated['summary']['tasks_by_agent']:
    consolidated['summary']['tasks_by_agent'][agent_type] = 0
    consolidated['summary']['tasks_by_agent'][agent_type] += 1
            
            # Par priorité
    priority = task.priority.value
    if priority not in consolidated['summary']['tasks_by_priority']:
    consolidated['summary']['tasks_by_priority'][priority] = 0
    consolidated['summary']['tasks_by_priority'][priority] += 1
            
            # Résultats par agent
    if agent_type not in consolidated['results_by_agent']:
    consolidated['results_by_agent'][agent_type] = []
    consolidated['results_by_agent'][agent_type].append({
    'task_id': task.task_id,
    'target': task.target,
    'status': task.status,
    'result': task.result
    })
            
            # Résultats par cible
    target = task.target
    if target not in consolidated['results_by_target']:
    consolidated['results_by_target'][target] = {}
    consolidated['results_by_target'][target][agent_type] = task.result
        
        # Métriques globales
    consolidated['global_metrics'] = await self._calculate_global_metrics()
        
    self.consolidated_results = consolidated
    return consolidated

    async def _calculate_global_metrics(self) -> Dict[str, Any]:
        """Calcul des métriques globales"""
        
    metrics = {
    'security_score': 0.0,
    'performance_score': 0.0,
    'conformity_score': 0.0,
    'global_score': 0.0,
    'critical_issues': 0,
    'total_issues': 0,
    'recommendations_count': 0
    }
        
    scores = []
        
    for task in self.audit_tasks:
    if task.status == "terminé" and task.result:
    result = task.result
                
                # Extraction scores selon le type d'agent
    if task.agent_type == 'securite' and 'security_score' in result:
    metrics['security_score'] = max(metrics['security_score'], result['security_score'])
    scores.append(result['security_score'])
                    
    elif task.agent_type == 'performance' and 'score' in result:
    metrics['performance_score'] = max(metrics['performance_score'], result['score'])
    scores.append(result['score'])
                    
    elif task.agent_type == 'conformite' and 'conformity_score' in result:
    metrics['conformity_score'] = max(metrics['conformity_score'], result['conformity_score'])
    scores.append(result['conformity_score'])
                
                # Comptage issues
    if 'findings' in result:
    metrics['total_issues'] += len(result['findings'])
                    # Compter critiques (selon structure)
    critical_findings = [f for f in result['findings'] if 'critical' in str(f).lower()]
    metrics['critical_issues'] += len(critical_findings)
                
    if 'issues' in result:
    metrics['total_issues'] += len(result['issues'])
                
    if 'recommendations' in result:
    metrics['recommendations_count'] += len(result['recommendations'])
        
        # Score global (moyenne des scores disponibles)
    if scores:
    metrics['global_score'] = round(sum(scores) / len(scores), 1)
        
    return metrics

    async def _generate_executive_report(self, audit_id: str, consolidated: Dict[str, Any]) -> Dict[str, Any]:
        """Génération du rapport exécutif"""
    self.logger.info("📋 Génération du rapport exécutif")
        
    metrics = consolidated['global_metrics']
        
    executive_report = {
    'audit_id': audit_id,
    'timestamp': datetime.now().isoformat(),
    'orchestrator': {
    'agent_id': self.agent_id,
    'phase': self.current_phase.value,
    'agents_deployed': list(self.agents.keys()),
    'total_tasks': len(self.audit_tasks)
    },
            
    'executive_summary': {
    'global_score': metrics['global_score'],
    'security_assessment': self._get_assessment_level(metrics['security_score']),
    'performance_assessment': self._get_assessment_level(metrics['performance_score']),
    'conformity_assessment': self._get_assessment_level(metrics['conformity_score']),
    'critical_issues_count': metrics['critical_issues'],
    'total_issues_count': metrics['total_issues'],
    'overall_status': self._determine_overall_status(metrics)
    },
            
    'detailed_results': consolidated,
            
    'priority_actions': self._generate_priority_actions(consolidated),
            
    'recommendations': self._generate_consolidated_recommendations(consolidated),
            
    'next_steps': [
    "🔴 Traiter immédiatement les issues critiques",
    "🟡 Planifier correction des problèmes majeurs",
    "🔄 Mettre en place monitoring continu",
    "📅 Programmer prochain audit dans 30 jours"
    ]
    }
        
    return executive_report

    def _get_assessment_level(self, score: float) -> str:
        """Détermine le niveau d'évaluation basé sur le score"""
    if score >= 9.0:
    return "Excellent"
    elif score >= 7.0:
    return "Bon"
    elif score >= 5.0:
    return "Moyen"
    elif score >= 3.0:
    return "Faible"
    else:
    return "Critique"

    def _determine_overall_status(self, metrics: Dict[str, Any]) -> str:
        """Détermine le statut global"""
    global_score = metrics['global_score']
    critical_issues = metrics['critical_issues']
        
    if critical_issues > 0:
    return "🚨 ACTION IMMÉDIATE REQUISE"
    elif global_score >= 8.0:
    return "✅ CONFORME"
    elif global_score >= 6.0:
    return "⚠️ AMÉLIORATIONS NÉCESSAIRES"
    else:
    return "❌ NON CONFORME"

    def _generate_priority_actions(self, consolidated: Dict[str, Any]) -> List[str]:
        """Génère les actions prioritaires"""
    actions = []
        
        # Analyse des résultats par agent
    for agent_type, agent_results in consolidated['results_by_agent'].items():
    for agent_result in agent_results:
    if agent_result['status'] == 'terminé' and agent_result['result']:
    result = agent_result['result']
                    
                    # Actions basées sur les findings critiques
    if 'findings' in result:
        critical_findings = [
            f for f in result['findings'] 
            if hasattr(f, 'security_level') and 'critical' in str(f.security_level).lower()
        ]
        if critical_findings:
            actions.append(f"🚨 {agent_type.upper()}: {len(critical_findings)} vulnérabilité(s) critique(s) à corriger")
                    
                    # Actions basées sur les bottlenecks
    if 'bottlenecks' in result and result['bottlenecks']:
        actions.append(f"⚡ {agent_type.upper()}: Résoudre {len(result['bottlenecks'])} goulot(s) d'étranglement")
        
        # Actions générales si peu d'actions spécifiques
    if len(actions) < 3 and len(self.audit_tasks) > 0:
        actions.extend([
        "🔍 Effectuer audit approfondi des composants critiques",
        "📚 Améliorer la documentation technique",
        "🔧 Mettre à jour les dépendances obsolètes"
        ])
        
    return actions[:5]  # Top 5 actions

    def _generate_consolidated_recommendations(self, consolidated: Dict[str, Any]) -> List[str]:
        """Génère les recommandations consolidées"""
    all_recommendations = set()
        
        # Collecte toutes les recommandations
    for agent_type, agent_results in consolidated['results_by_agent'].items():
    for agent_result in agent_results:
    if agent_result['status'] == 'terminé' and agent_result['result']:
    result = agent_result['result']
                    
    if 'recommendations' in result:
        all_recommendations.update(result['recommendations'])
        
        # Recommandations orchestrateur
    orchestrator_recs = [
    "🎯 Mettre en place un processus d'audit continu",
    "📊 Implémenter tableau de bord de qualité",
    "🔄 Automatiser les vérifications de conformité",
    "👥 Former l'équipe aux bonnes pratiques",
    "📝 Documenter les procédures d'audit"
    ]
        
    all_recommendations.update(orchestrator_recs)
        
    return list(all_recommendations)

    async def _save_orchestrator_report(self, report: Dict[str, Any]):
        """Sauvegarde le rapport de l'orchestrateur"""
    try:
    reports_dir = self.workspace_root / "reports" / "orchestrateur_audit"
    reports_dir.mkdir(parents=True, exist_ok=True)
            
    report_file = reports_dir / f"orchestrator_audit_{report['audit_id']}.json"
            
    with open(report_file, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            
    self.logger.info(f"📄 Rapport orchestrateur sauvegardé : {report_file}")
            
    except Exception as e:
    self.logger.error(f"❌ Erreur sauvegarde rapport orchestrateur : {e}")

async def main():
    """Démonstration de l'orchestrateur d'audit"""
    print("🎯 ORCHESTRATEUR AUDIT - Démonstration")
    
    # Initialisation orchestrateur
    orchestrateur = AgentOrchestrateurAudit()
    
    # Définition des cibles d'audit
    targets = [
    "core",
    "agents"
    ]
    
    # Filtrage des cibles existantes
    existing_targets = [str(orchestrateur.workspace_root / target) for target in targets if (orchestrateur.workspace_root / target).exists()]
    
    if not existing_targets:
    print(f"❌ Aucune cible d'audit trouvée aux emplacements prévus (depuis {orchestrateur.workspace_root})")
    return
    
    print(f"\\n🎯 Démarrage audit sur {len(existing_targets)} cibles:")
    for target in existing_targets:
    print(f"  📁 {target}")
    
    # Exécution audit complet
    try:
    rapport = await orchestrateur.executer_audit_complet(existing_targets)
        
    print(f"\\n📊 === RAPPORT EXÉCUTIF AUDIT ===")
    print(f"🆔 ID Audit: {rapport['audit_id']}")
    print(f"📈 Score Global: {rapport['executive_summary']['global_score']}/10")
    print(f"🎯 Statut: {rapport['executive_summary']['overall_status']}")
        
        # Détails par domaine
    print(f"\\n📋 ÉVALUATIONS PAR DOMAINE:")
    summary = rapport['executive_summary']
    print(f"  🔐 Sécurité: {summary['security_assessment']}")
    print(f"  ⚡ Performance: {summary['performance_assessment']}")
    print(f"  📋 Conformité: {summary['conformity_assessment']}")
        
        # Issues critiques
    if summary['critical_issues_count'] > 0:
    print(f"\\n🚨 ISSUES CRITIQUES: {summary['critical_issues_count']}")
        
        # Actions prioritaires
    if rapport['priority_actions']:
    print(f"\\n🎯 ACTIONS PRIORITAIRES:")
    for action in rapport['priority_actions'][:3]:
    print(f"  {action}")
        
    print(f"\\n✅ Audit orchestré terminé avec succès!")
    print(f"📄 Rapport détaillé sauvegardé")
        
    except Exception as e:
    print(f"❌ Erreur durant l'audit: {e}")

# === FACTORY FUNCTION PATTERN FACTORY ===
def create_agent(**kwargs) -> AgentOrchestrateurAudit:
    """Fonction factory pour créer une instance de l'orchestrateur audit"""
    return AgentOrchestrateurAudit(**kwargs)

if __name__ == "__main__":
    asyncio.run(main()) 
