#!/usr/bin/env python3
"""
🎖️ CHEF D'ÉQUIPE COORDINATEUR ENTERPRISE - Pattern Factory NextGeneration
===============================================================================

🎯 Mission : Orchestration centrale de l'équipe de maintenance.
⚡ Capacités : Boucle de réparation itérative, coordination d'équipe, reporting.

Author: Équipe de Maintenance NextGeneration
Version: 4.2.0 - Report Enrichment
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
    Chef d'équipe pour orchestrer des workflows de maintenance complexes
    avec une boucle de réparation itérative et un reporting enrichi.
    """
    def __init__(self, **kwargs):
        super().__init__(
            agent_type="coordinateur",
            **kwargs
        )
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
        return ["workflow_maintenance_complete"]
        
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
            "resultats_par_agent": []
        }
        
        for agent_path_str in agents_a_traiter:
            agent_path = Path(agent_path_str)
            agent_name = agent_path.name
            self.logger.info(f"--- 🔁 DÉBUT DU TRAITEMENT ITÉRATIF POUR: {agent_name} ---")
            
            try:
                original_code = agent_path.read_text(encoding='utf-8')
                file_report = await self._run_remediation_cycle(agent_path_str, original_code)
            except Exception as e:
                self.logger.error(f"Erreur critique lors du traitement de {agent_name}: {e}")
                file_report = {"agent_name": agent_name, "status": "CRITICAL_FAILURE", "last_error": str(e)}

            self.mission_context["resultats_par_agent"].append(file_report)
            self.logger.info(f"--- ☑️ FIN DU TRAITEMENT POUR: {agent_name} ---")

        self.mission_context["duree_totale_sec"] = time.time() - start_time
        self.mission_context["statut_mission"] = "SUCCÈS - Terminée"
        
        await self._generer_et_sauvegarder_rapports(mission_id)
        
        return self.mission_context

    async def _run_remediation_cycle(self, agent_path_str: str, original_code: str) -> Dict:
        agent_name = Path(agent_path_str).name
        agent_mission = self._extraire_mission_docstring(original_code)

        file_report = {
            "agent_name": agent_name,
            "agent_mission": agent_mission,
            "status": "PENDING",
            "original_code": original_code,
            "final_code": original_code,
            "repair_history": [],
            "structure_analysis": {},
            "initial_evaluation": {},
            "performance_analysis": {},
            "style_report": {}
        }
        
        # 0. Analyse de structure initiale
        structure_result = await self._run_sub_task("analyseur_structure", "analyse_structure", {"file_path": agent_path_str})
        if structure_result and structure_result.success:
            file_report["structure_analysis"] = structure_result.data.get("analysis", {})
            if file_report["structure_analysis"].get("error"):
                self.logger.warning(f"  -> Analyse de structure a trouvé une erreur de syntaxe pour {agent_name}: {file_report['structure_analysis']['error']}")
        else:
            error_msg = structure_result.error if structure_result else "Réponse invalide de l'analyseur"
            file_report["structure_analysis"] = {"error": f"Analyse de structure a échoué: {error_msg}"}
            self.logger.error(f"L'analyseur de structure a échoué pour {agent_name}: {error_msg}")

        # 1. Évaluation initiale
        eval_result = await self._run_sub_task("evaluateur", "evaluate_code", {"file_path": agent_path_str})
        
        if eval_result and eval_result.success:
            file_report["initial_evaluation"] = eval_result.data
            if eval_result.data.get("is_useful"):
                self.logger.info(f"  ✅ Évaluation initiale réussie pour {agent_name}. Aucune réparation nécessaire.")
                file_report["status"] = "NO_REPAIR_NEEDED"
            else:
                self.logger.warning(f"  -> Code jugé inutile (score: {eval_result.data.get('score')}). Lancement du cycle de réparation.")
        else:
            error_msg = eval_result.error if eval_result else "Réponse invalide de l'évaluateur"
            self.logger.error(f"L'évaluateur a échoué pour {agent_name}: {error_msg}. Démarrage du cycle de réparation par précaution.")
            file_report["initial_evaluation"] = {"error": f"Évaluation initiale échouée: {error_msg}"}

        # 1.5 Correction sémantique automatique
        if file_report["status"] != "CRITICAL_FAILURE":
             self.logger.info(f"⚙️  Lancement du Correcteur sémantique pour {agent_name}...")
             semantic_result = await self._run_sub_task(
                 "correcteur_semantique", 
                 "correct_semantics", 
                 {"code": file_report["final_code"], "file_path": agent_path_str}
             )
             if semantic_result and semantic_result.success and semantic_result.data.get("score_improvement", 0) > 0:
                 file_report["final_code"] = semantic_result.data["corrected_code"]
                 file_report["semantic_fix"] = {
                     "correction_count": semantic_result.data["correction_count"],
                     "initial_score": semantic_result.data["initial_score"],
                     "final_score": semantic_result.data["final_score"]
                 }
                 self.logger.info(f"  ✅ Correcteur sémantique a amélioré le code de {agent_name}.")
             else:
                 self.logger.info(f"  -> Correcteur sémantique n'a trouvé aucune amélioration pour {agent_name}.")

        # 2. Boucle de réparation (si nécessaire)
        if file_report["status"] != "NO_REPAIR_NEEDED":
            await self._perform_repair_loop(agent_path_str, file_report)

        # 2.5 Harmonisation du style
        if file_report["status"] in ["REPAIRED", "NO_REPAIR_NEEDED"]:
            self.logger.info(f"🎨 Lancement de l'harmonisation de style pour {agent_name}...")
            style_result = await self._run_sub_task("harmonisateur_style", "harmonize_style", {"code": file_report["final_code"], "file_path": agent_path_str})
            if style_result and style_result.success:
                file_report["final_code"] = style_result.data.get("harmonized_code", file_report["final_code"])
                file_report["style_report"] = style_result.data.get("style_report", {})
                self.logger.info(f"🎨 Style harmonisé pour {agent_name}.")
            else:
                self.logger.warning(f"L'harmonisation du style a échoué pour {agent_name}.")
                file_report["style_report"] = {"error": "Harmonisation du style a échoué."}

        # 3. Analyse de performance finale
        perf_result = await self._run_sub_task("analyseur_performance", "analyze_performance", {"code": file_report["final_code"]})
        if perf_result and perf_result.success:
            file_report["performance_analysis"] = perf_result.data
        else:
            file_report["performance_analysis"] = {"error": "Analyse de performance échouée."}

        return file_report

    async def _perform_repair_loop(self, agent_path_str: str, file_report: Dict):
        MAX_REPAIR_ATTEMPTS = 5
        current_code = file_report["original_code"]
        last_exception = Exception(file_report["initial_evaluation"].get("reason") or file_report["initial_evaluation"].get("error", "Évaluation initiale négative."))

        for attempt in range(MAX_REPAIR_ATTEMPTS):
            # CLASSIFICATION DE L'ERREUR
            error_type = classify_exception(last_exception)
            last_error_str = str(last_exception)
            self.logger.info(f"Tentative {attempt + 1}/{MAX_REPAIR_ATTEMPTS}. Erreur détectée (type: {error_type}): {last_error_str}")

            # ADAPTATION
            adapt_result = await self._run_sub_task(
                "adaptateur", 
                "adapt_code", 
                {
                    "code": current_code, 
                    "feedback": last_error_str,
                    "error_type": error_type
                }
            )
            
            if not (adapt_result and adapt_result.success and adapt_result.data.get("adapted_code")):
                file_report["status"] = "REPAIR_FAILED"
                file_report["last_error"] = "L'adaptateur n'a pas pu modifier le code."
                break
            
            current_code = adapt_result.data["adapted_code"]
            
            # TEST
            test_result = await self._run_sub_task("testeur", "test_agent_code", {"code_content": current_code}, return_exception=True)
            
            file_report["repair_history"].append({
                "iteration": attempt + 1,
                "error_detected": last_error_str,
                "adaptation_attempted": adapt_result.data.get("adaptations", ["Adaptation inconnue."]),
                "test_result": "Succès" if test_result.success else f"Échec: {test_result.error}"
            })
            
            if test_result.success:
                self.logger.info(f"  ✅ Réparation réussie pour {Path(agent_path_str).name} à la tentative {attempt + 1}.")
                file_report["status"] = "REPAIRED"
                file_report["final_code"] = current_code
                return

            last_exception = test_result.raw_exception if hasattr(test_result, 'raw_exception') and test_result.raw_exception else Exception(test_result.error)

        if file_report["status"] != "REPAIRED":
            file_report["status"] = "REPAIR_FAILED"
            file_report["last_error"] = str(last_exception)
            file_report["final_code"] = current_code

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

    async def _run_sub_task(self, agent_role: str, task_type: str, params: dict, return_exception: bool = False) -> Optional[Result]:
        """Exécute une sous-tâche sur un agent de l'équipe."""
        agent = self.equipe_agents.get(agent_role)
        if not agent:
            self.logger.error(f"Agent avec le rôle '{agent_role}' non trouvé dans l'équipe.")
            return Result(success=False, error=f"Agent '{agent_role}' non disponible.")
        
        task = Task(type=task_type, params=params)
        
        try:
            result = await agent.execute_task(task)
            return result
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche '{task_type}' sur '{agent_role}': {e}", exc_info=True)
            result = Result(success=False, error=str(e))
            if return_exception:
                result.raw_exception = e
            return result

def create_agent_MAINTENANCE_00_chef_equipe_coordinateur(**kwargs) -> ChefEquipeCoordinateurEnterprise:
    """Crée une instance du Chef d'Équipe Coordinateur."""
    return ChefEquipeCoordinateurEnterprise(**kwargs)