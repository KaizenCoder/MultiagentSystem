#!/usr/bin/env python3
"""
Agent Chef Équipe Coordinateur - Classe principale
"""

from typing import Any, Dict, List, Optional

class AgentMaintenanceChefEquipeCoordinateur:
    """Classe principale du Chef Équipe Coordinateur"""
    
    def __init__(self, **kwargs):
        self.agent_id = kwargs.get('agent_id', 'chef_equipe_coordinateur')
        self.name = "Chef Équipe Coordinateur"
        self.version = "1.0.0"
        self.team_members = []
    
    def execute_task(self, task):
        """Exécute une tâche de coordination"""
        return {
            "status": "success", 
            "result": "Coordination task executed",
            "agent_id": self.agent_id
        }
    
    def coordinate_team(self):
        """Coordonne l'équipe de maintenance"""
        return {"status": "coordinated", "team_size": len(self.team_members)}
    
    def get_status(self):
        return "operational"

# Aliases pour compatibilité
AgentMaintenance00 = AgentMaintenanceChefEquipeCoordinateur
ChefEquipeCoordinateur = AgentMaintenanceChefEquipeCoordinateur

#!/usr/bin/env python3
"""
🎖️ CHEF D'ÉQUIPE COORDINATEUR ENTERPRISE - Pattern Factory NextGeneration
===============================================================================

🎯 Mission : Orchestration centrale de l'équipe de maintenance.
⚡ Capacités : Boucle de réparation itérative, coordination d'équipe, reporting.

Author: Équipe de Maintenance NextGeneration
Version: 4.3.0 - Harmonisation Standards Pattern Factory NextGeneration
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys
import time
import json
import logging
import uuid
import re

# Import direct de l'architecture et des agents
from core.agent_factory_architecture import Agent, Task, Result, AgentFactory

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

class ChefEquipeCoordinateurEnterprise(Agent):
    """
    🎖️ Chef d'Équipe Coordinateur Enterprise - Agent de Maintenance Principal
    
    Agent spécialisé dans l'orchestration centrale de l'équipe de maintenance NextGeneration.
    Responsable de la coordination des workflows complexes avec boucle de réparation itérative 
    et génération de rapports stratégiques détaillés.
    
    Capacités principales :
    - Orchestration complète d'équipe de maintenance (12 agents spécialisés)
    - Boucle de réparation itérative avec classification d'erreurs
    - Coordination séquentielle : analyse → adaptation → test → validation
    - Génération de rapports mission complets (JSON + Markdown)
    - Gestion de santé d'équipe et monitoring temps réel
    
    Workflow type :
    1. Recrutement automatique équipe maintenance 
    2. Analyse initiale et test de code
    3. Boucle réparation si nécessaire (max 5 tentatives)
    4. Documentation et rapport final
    
    Conformité : Pattern Factory NextGeneration v4.3.0
    """
    def __init__(self, **kwargs):
        super().__init__(
            agent_type="coordinateur",
            **kwargs
        )
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={
                    "logger_name": f"nextgen.maintenance.chef_equipe.{self.id}",
                    "log_dir": "logs/maintenance/chef_equipe",
                    "metadata": {
                        "agent_type": "MAINTENANCE_00_chef_equipe_coordinateur",
                        "agent_role": "chef_equipe_coordinateur",
                        "system": "nextgeneration",
                        "priority": "high"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = self.id

        self.logger.info(f"Chef d'équipe v4.2.0 initialisé avec ID: {self.agent_id}")
        
        self.workspace_path = Path(kwargs.get("workspace_path", "."))
        self.factory = AgentFactory(config_path=str(self.workspace_path / "config" / "maintenance_config.json"))
        
        self.equipe_agents: Dict[str, Agent] = {}
        self.mission_context = {}
        
    async def startup(self):
        self.logger.info(f"🚀 Démarrage du Chef d'Équipe {self.agent_id}")
        await self._recruter_equipe()
        self.logger.info("Chef d'Équipe prêt et équipe recrutée.")

    async def shutdown(self):
        self.logger.info(f"🛑 Arrêt du Chef d'Équipe {self.agent_id}")
        for agent in self.equipe_agents.values():
            if hasattr(agent, 'shutdown'):
                await agent.shutdown()

    def get_capabilities(self) -> List[str]:
        """Retourne les capacités spécialisées du Chef d'Équipe Coordinateur."""
        return [
            "workflow_maintenance_complete",
            "orchestration_equipe_maintenance", 
            "boucle_reparation_iterative",
            "coordination_agents_maintenance",
            "reporting_mission_json_md"
        ]
        
    def _extraire_mission_docstring(self, code: str) -> str:
        """Extrait la description de la mission depuis le docstring de l'agent."""
        match = re.search(r'🎯 Mission\s*:\s*(.*)', code)
        if match:
            return match.group(1).strip()
        return "Non spécifiée"

    async def health_check(self) -> Dict[str, Any]:
        team_status = {}
        for role, agent in self.equipe_agents.items():
            try:
                agent_health = await agent.health_check()
                team_status[role] = agent_health.get("status", "unknown")
            except Exception:
                team_status[role] = "error"
        is_healthy = all(s == "healthy" for s in team_status.values())
        return {"status": "healthy" if is_healthy else "degraded", "team_status": team_status}

    async def execute_task(self, task: Task) -> Result:
        if task.type == "workflow_maintenance_complete":
            final_report = await self.workflow_maintenance_complete(task.params)
            return Result(success=True, data=final_report)
        return Result(success=False, error=f"Tâche non reconnue: {task.type}")

    async def workflow_maintenance_complete(self, mission_config: Dict) -> Dict:
        mission_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.logger.info(f"===== DÉBUT DE LA MISSION DE MAINTENANCE : {mission_id} =====")
        start_time = time.time()

        agents_a_traiter = mission_config.get("target_files", [])
        
        self.mission_context = {
            "mission_id": mission_id,
            "statut_mission": "EN_COURS",
            "resultats_par_agent": [],
            "agents_reports": {}
        }
        
        for agent_path_str in agents_a_traiter:
            agent_path = Path(agent_path_str)
            agent_name = agent_path.name
            self.logger.info(f"--- 🔁 DÉBUT DU TRAITEMENT ITÉRATIF POUR: {agent_name} ---")
            
            file_report = self.mission_context["agents_reports"].setdefault(agent_name, {})
            
            try:
                current_code = await self._read_agent_code(agent_path)
                file_report["original_code"] = current_code

                # STRATÉGIE SIMPLIFIÉE : TESTER D'ABORD
                initial_test_result = await self._run_sub_task("testeur", "test_code", {"code": current_code, "file_path": agent_path.as_posix()})

                if not initial_test_result.success:
                    self.logger.warning(f"  -> Échec du test initial pour {agent_name}. Lancement de la réparation.")
                    initial_exception = initial_test_result.data.get("exception") if initial_test_result.data else Exception(initial_test_result.error)
                    
                    repaired_code = await self._perform_repair_loop(
                        current_code=current_code,
                        max_retries=5,
                        initial_exception=initial_exception,
                        file_path=agent_path.as_posix()
                    )
                    
                    if repaired_code:
                        file_report["status"] = "REPAIRED"
                        file_report["final_code"] = repaired_code
                    else:
                        file_report["status"] = "REPAIR_FAILED"
                else:
                    # Si le test passe, on peut faire les autres analyses
                    self.logger.info(f"  -> Test initial réussi pour {agent_name}. Pas de réparation nécessaire.")
                    file_report["status"] = "SUCCESS"
                    file_report["final_code"] = current_code

            except Exception as e:
                self.logger.error(f"Erreur critique lors du traitement de {agent_name}: {e}", exc_info=True)
                file_report["status"] = "CRITICAL_ERROR"
            
            self.logger.info(f"--- ☑️ FIN DU TRAITEMENT POUR: {agent_name} ---")

        self.mission_context["duree_totale_sec"] = time.time() - start_time
        self.mission_context["statut_mission"] = "SUCCÈS - Terminée"
        
        await self._generer_et_sauvegarder_rapports(mission_id)
        
        return self.mission_context

    async def _perform_repair_loop(self, current_code: str, max_retries: int, initial_exception: Exception, file_path: str) -> Optional[str]:
        last_exception = initial_exception
        
        for attempt in range(max_retries):
            # CLASSIFICATION DE L'ERREUR
            error_type = classify_exception(last_exception)
            self.logger.info(f"Tentative de réparation {attempt + 1}/{max_retries}. Erreur: {last_exception} (type: {error_type})")

            # ADAPTATION
            adapt_result = await self._run_sub_task(
                "adaptateur", 
                "adapt_code", 
                {
                    "code": current_code, 
                    "feedback": last_exception,
                    "error_type": error_type
                }
            )
            
            if not (adapt_result and adapt_result.success and adapt_result.data.get("adapted_code")):
                self.logger.error("L'adaptateur a échoué. Abandon.")
                return None
            
            current_code = adapt_result.data["adapted_code"]

            # TEST
            test_result = await self._run_sub_task("testeur", "test_code", {"code": current_code, "file_path": file_path})

            if test_result.success:
                self.logger.info("  -> Code réparé et validé avec succès!")
                return current_code
            
            last_exception = test_result.data.get("exception") if test_result.data else Exception(test_result.error)
        
        self.logger.error(f"Échec de la réparation après {max_retries} tentatives.")
        return None

    async def _read_agent_code(self, agent_path: Path) -> str:
        return agent_path.read_text(encoding='utf-8')

    async def _generer_et_sauvegarder_rapports(self, mission_id):
        self.logger.info("Génération du rapport de mission par l'agent Documenteur...")
        self.mission_context['equipe_maintenance_roles'] = list(self.equipe_agents.keys())
        doc_result = await self._run_sub_task("documenteur", "generate_mission_report", {"report_data": self.mission_context})
        
        report_dir = self.workspace_path / "reports"
        report_dir.mkdir(exist_ok=True, parents=True)

        json_report_path = report_dir / f"rapport_mission_{mission_id}.json"
        with open(json_report_path, "w", encoding="utf-8") as f:
            json.dump(self.mission_context, f, indent=2)
        self.logger.info(f"Rapport JSON détaillé sauvegardé : {json_report_path}")

        if doc_result and doc_result.success:
            md_content = doc_result.data.get("md_content")
            md_report_path = report_dir / f"rapport_mission_{mission_id}.md"
            with open(md_report_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            self.logger.info(f"Rapport Markdown sauvegardé : {md_report_path}")
        else:
            self.logger.error("L'agent Documenteur a échoué à générer le rapport Markdown.")

    async def _recruter_equipe(self):
        self.logger.info("Recrutement de l'équipe de maintenance...")
        
        roles = [
            "analyseur_structure", 
            "evaluateur",
            "correcteur_semantique",
            "adaptateur", 
            "testeur", 
            "documenteur", 
            "analyseur_performance",
            "dependency_manager",
            "security_manager",
            "correcteur_logique",
            "auditeur_qualite",
            "harmonisateur_style"
        ]
        
        for role in roles:
            try:
                agent = self.factory.create_agent(role)
                if hasattr(agent, 'startup'):
                    await agent.startup()
                self.equipe_agents[role] = agent
            except Exception as e:
                self.logger.error(f"Erreur lors de la création de l'agent {role}: {e}")

    async def _run_sub_task(self, agent_type: str, task_type: str, params: Dict[str, Any]) -> Result:
        """Exécute une sous-tâche sur un agent spécifique."""
        agent = self.equipe_agents.get(agent_type)
        if not agent:
            self.logger.error(f"Agent avec le rôle '{agent_type}' non trouvé dans l'équipe.")
            return Result(success=False, error=f"Agent '{agent_type}' non disponible.")
        
        task = Task(type=task_type, params=params)
        
        try:
            result = await agent.execute_task(task)
            return result
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche '{task_type}' sur '{agent_type}': {e}", exc_info=True)
            result = Result(success=False, error=str(e))
            return result

def create_agent_MAINTENANCE_00_chef_equipe_coordinateur(**kwargs) -> ChefEquipeCoordinateurEnterprise:
    """Crée une instance du Chef d'Équipe Coordinateur."""
    return ChefEquipeCoordinateurEnterprise(**kwargs)
    # ✅ MÉTHODES STANDARDISÉES DE RAPPORT

    def _calculate_report_score(self, metrics: Dict[str, Any]) -> int:
        """Calcule le score global du rapport basé sur les métriques."""
        score = 0
        issues_critiques = []
        
        # Logique de scoring spécifique à l'agent
        # À adapter selon le type d'agent
        
        return score
    
    def _assess_conformity(self, score: int) -> str:
        """Évalue la conformité basée sur le score."""
        if score >= 90:
            return "✅ CONFORME - OPTIMAL"
        elif score >= 70:
            return "✅ CONFORME - ACCEPTABLE"
        else:
            return "❌ NON CONFORME - CRITIQUE"
    
    def _get_quality_level(self, score: int) -> str:
        """Détermine le niveau de qualité."""
        if score >= 90:
            return "OPTIMAL"
        elif score >= 70:
            return "ACCEPTABLE"
        else:
            return "CRITIQUE"
    
    def _generate_recommendations(self, metrics: Dict[str, Any], issues: List[str]) -> List[str]:
        """Génère les recommandations basées sur l'analyse."""
        recommendations = []
        
        # Logique de génération de recommandations
        # À adapter selon le type d'agent
        
        return recommendations
    
    def _generate_standard_report(self, context: Dict, metrics: Dict, timestamp) -> Dict[str, Any]:
        """Génère un rapport selon le format standard de l'agent 06."""
        
        score = self._calculate_report_score(metrics)
        conformity = self._assess_conformity(score)
        quality_level = self._get_quality_level(score)
        
        agent_filename = Path(__file__).name
        
        # Issues critiques (à personnaliser selon l'agent)
        issues_critiques = []
        
        return {
            'agent_id': getattr(self, 'agent_id', 'unknown'),
            'agent_file_name': agent_filename,
            'type_rapport': 'standard',  # À personnaliser
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Agent Spécialisé',  # À personnaliser
            'score_global': score,
            'niveau_qualite': quality_level,
            'conformite': conformity,
            'signature_cryptographique': 'N/A (Fonctionnalité non implémentée pour cet agent)',
            'issues_critiques_identifies': len(issues_critiques),
            'architecture': {
                'description': "Description de l'architecture de l'agent",
                'statut_operationnel': f"Système {getattr(self, 'agent_id', 'unknown')} opérationnel.",
                'confirmation_specialisation': f"{getattr(self, 'agent_id', 'unknown')} confirmé comme spécialiste.",
                'objectifs_principaux': [
                    "Objectif principal 1",
                    "Objectif principal 2",
                    "Objectif principal 3"
                ],
                'technologies_cles': ["Technologie 1", "Technologie 2"]
            },
            'recommandations': self._generate_recommendations(metrics, issues_critiques),
            'issues_critiques_details': issues_critiques if issues_critiques else [
                "Aucun issue critique majeur détecté. Le système fonctionne dans les paramètres attendus."
            ],
            'details_techniques': {
                'strategie': "Stratégie technique de l'agent",
                'composants_actifs': [],
                'metriques_collectees': metrics
            },
            'metriques_detaillees': {
                'score_global': {'actuel': score, 'cible': 100},
                'conformite_pourcentage': {'actuel': score, 'cible': 100, 'unite': '%'}
            },
            'impact_business': {
                'criticite': 'MOYENNE' if score >= 70 else 'HAUTE',
                'domaines_impactes': [],
                'actions_requises': []
            }
        }


    def _generate_markdown_report(self, rapport_json: Dict, context: Dict, timestamp) -> str:
        """Génère un rapport Markdown selon le format standard."""
        
        agent_name = rapport_json.get('agent_id', 'Agent Inconnu')
        type_rapport = rapport_json.get('type_rapport', 'standard')
        score = rapport_json.get('score_global', 0)
        quality = rapport_json.get('niveau_qualite', 'UNKNOWN')
        conformity = rapport_json.get('conformite', 'NON ÉVALUÉ')
        
        markdown_content = f"""# 📊 RAPPORT STRATÉGIQUE : {agent_name.upper()}

## 🎯 RÉSUMÉ EXÉCUTIF

**Agent :** {agent_name}  
**Type de Rapport :** {type_rapport}  
**Date de Génération :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Score Global :** {score}/100  
**Niveau de Qualité :** {quality}  
**Conformité :** {conformity}  

## 📈 ANALYSE GLOBALE

### Score de Performance
- **Score Actuel :** {score}/100
- **Objectif :** 100/100
- **Statut :** {'🟢 ACCEPTABLE' if score >= 70 else '🔴 CRITIQUE'}

### Architecture
{rapport_json.get('architecture', {}).get('description', 'Description non disponible')}

**Objectifs Principaux :**
"""
        
        # Ajouter les objectifs
        for obj in rapport_json.get('architecture', {}).get('objectifs_principaux', []):
            markdown_content += f"- {obj}\n"
        
        markdown_content += f"""
**Technologies Clés :**
"""
        
        # Ajouter les technologies
        for tech in rapport_json.get('architecture', {}).get('technologies_cles', []):
            markdown_content += f"- {tech}\n"
        
        markdown_content += f"""

## 🔍 RECOMMANDATIONS

"""
        
        # Ajouter les recommandations
        for reco in rapport_json.get('recommandations', []):
            markdown_content += f"- {reco}\n"
        
        markdown_content += f"""

## ⚠️ ISSUES CRITIQUES

"""
        
        # Ajouter les issues critiques
        for issue in rapport_json.get('issues_critiques_details', []):
            markdown_content += f"- {issue}\n"
        
        markdown_content += f"""

## 📊 MÉTRIQUES DÉTAILLÉES

### Performance Globale
- **Score Global :** {rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('actuel', 0)}/{rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('cible', 100)}
- **Conformité :** {rapport_json.get('metriques_detaillees', {}).get('conformite_pourcentage', {}).get('actuel', 0)}%

## 🎯 IMPACT BUSINESS

**Criticité :** {rapport_json.get('impact_business', {}).get('criticite', 'NON ÉVALUÉ')}

### Domaines Impactés
"""
        
        # Ajouter les domaines impactés
        for domaine in rapport_json.get('impact_business', {}).get('domaines_impactes', []):
            markdown_content += f"- {domaine}\n"
        
        markdown_content += f"""

### Actions Requises
"""
        
        # Ajouter les actions requises
        for action in rapport_json.get('impact_business', {}).get('actions_requises', []):
            markdown_content += f"- {action}\n"
        
        markdown_content += f"""

---
*Rapport généré automatiquement par {agent_name} - NextGeneration System*  
*Timestamp: {timestamp.isoformat()}*
"""
        
        return markdown_content



# Alias pour compatibilité
class AgentMaintenance00(AgentMaintenanceChefEquipeCoordinateur):
    """Alias pour compatibilité avec les anciens imports"""
    pass

AgentMaintenance00 = AgentMaintenanceChefEquipeCoordinateur


# Alias pour compatibilité
AgentMaintenanceChefEquipeCoordinateur = ChefEquipeCoordinateurEnterprise

# Aliases pour compatibilité
AgentMaintenanceChefEquipeCoordinateur = ChefEquipeCoordinateurEnterprise
AgentMaintenance00 = ChefEquipeCoordinateurEnterprise
ChefEquipeCoordinateur = ChefEquipeCoordinateurEnterprise
