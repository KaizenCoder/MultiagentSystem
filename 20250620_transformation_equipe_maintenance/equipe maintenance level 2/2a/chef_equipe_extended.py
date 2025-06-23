import os
import json
import asyncio
from datetime import datetime
from agent_factory_implementation.core.agent_factory_architecture import Agent, Task, Result, AgentFactory, Team

# Importation des agents de base
from .agent_MAINTENANCE_01_analyseur_structure import AgentMAINTENANCE01AnalyseurStructure
from .agent_MAINTENANCE_02_evaluateur_utilite import AgentMAINTENANCE02EvaluateurUtilite
from .agent_MAINTENANCE_03_adaptateur_code import AgentMAINTENANCE03AdaptateurCode
from .agent_MAINTENANCE_04_testeur_anti_faux_agents import AgentMAINTENANCE04TesteurAntiFauxAgents
from .agent_MAINTENANCE_05_documenteur_peer_reviewer import AgentMAINTENANCE05DocumenteurPeerReviewer
from .agent_MAINTENANCE_06_validateur_final import AgentMAINTENANCE06ValidateurFinal

# Importation des nouveaux agents (optionnels)
try:
    from .agent_MAINTENANCE_07_gestionnaire_dependances import AgentMAINTENANCE07GestionnaireDependances
    DEPENDENCY_MANAGER_AVAILABLE = True
except ImportError:
    DEPENDENCY_MANAGER_AVAILABLE = False

try:
    from .agent_MAINTENANCE_08_optimiseur_performance import AgentMAINTENANCE08OptimiseurPerformance
    PERFORMANCE_OPTIMIZER_AVAILABLE = True
except ImportError:
    PERFORMANCE_OPTIMIZER_AVAILABLE = False

class AgentMAINTENANCE00ChefEquipeCoordinateurExtended(Agent):
    def __init__(self, agent_id, version, description, team: Team, workspace_path, extended_mode=True):
        super().__init__(agent_id, version, description, "orchestrator", "enabled")
        self.team = team
        self.workspace_path = workspace_path
        self.extended_mode = extended_mode
        self.log(f"Chef d'équipe {'étendue' if extended_mode else 'standard'} initialisé. Espace de travail : {self.workspace_path}")

    async def startup(self):
        await super().startup()
        available_agents = list(self.team.agents.keys()) if hasattr(self.team, 'agents') else ['analyseur', 'evaluateur', 'adaptateur', 'testeur', 'documenteur', 'validateur']
        self.log(f"Chef d'équipe prêt. Agents disponibles : {', '.join(available_agents)}")

    async def execute_task(self, task: Task) -> Result:
        self.log(f"Reçu une nouvelle tâche de maintenance : {task.type}")
        if task.type not in ["maintenance_complete", "maintenance_extended"]:
            return Result(success=False, error="Type de tâche non supporté.")

        target_directory = task.params.get("target_directory")
        if not target_directory:
            return Result(success=False, error="Répertoire cible non spécifié.")

        # Mode étendu activé si demandé explicitement ou si des agents étendus sont disponibles
        use_extended = (task.type == "maintenance_extended" or 
                       (self.extended_mode and (DEPENDENCY_MANAGER_AVAILABLE or PERFORMANCE_OPTIMIZER_AVAILABLE)))

        mission_id = f"mission_{'extended_' if use_extended else ''}{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        mission_report = {
            "mission_id": mission_id,
            "start_time": datetime.now().isoformat(),
            "status": "IN_PROGRESS",
            "mode": "extended" if use_extended else "standard",
            "target_directory": target_directory,
            "steps": []
        }

        self.log(f"Démarrage de la mission {mission_id} en mode {'étendu' if use_extended else 'standard'} sur {target_directory}")

        try:
            # Étape 1: Analyseur de Structure (toujours en premier)
            analyse_task = Task(type="analyse_structure", params={"directory": target_directory})
            analyse_result = await self.team.get_agent("analyseur").execute_task(analyse_task)
            mission_report["steps"].append({"agent": "analyseur", "result": analyse_result.to_dict()})
            
            if not analyse_result.success:
                raise Exception(f"Échec de l'analyse: {analyse_result.error}")
            
            analysed_files = analyse_result.data["files"]

            # Traitement de chaque fichier par l'équipe
            processed_files_reports = []
            for file_info in analysed_files:
                file_path = file_info["path"]
                file_report = {"file_path": file_path, "sub_steps": []}

                current_code = file_info["content"]
                if not current_code:
                    self.log(f"Fichier {file_path} vide ou illisible, passage au suivant.")
                    continue

                # PIPELINE STANDARD (toujours exécuté)
                
                # Étape 2: Évaluateur d'utilité
                eval_task = Task(type="evaluate_utility", params={"code": current_code, "file_path": file_path})
                eval_result = await self.team.get_agent("evaluateur").execute_task(eval_task)
                file_report["sub_steps"].append({"agent": "evaluateur", "result": eval_result.to_dict()})
                
                if not eval_result.success:
                    self.log(f"Fichier {file_path} jugé non utile, passage au suivant.")
                    continue

                # Étape 3: Gestionnaire de dépendances (si disponible et mode étendu)
                if use_extended and DEPENDENCY_MANAGER_AVAILABLE:
                    dep_task = Task(type="manage_dependencies", params={"code": current_code, "file_path": file_path})
                    dep_result = await self.team.get_agent("gestionnaire_dependances").execute_task(dep_task)
                    file_report["sub_steps"].append({"agent": "gestionnaire_dependances", "result": dep_result.to_dict()})
                    
                    if dep_result.success and "optimized_code" in dep_result.data:
                        current_code = dep_result.data["optimized_code"]
                        self.log(f"Dépendances optimisées pour {file_path}")

                # Étape 4: Adaptateur de code
                adapt_task = Task(type="adapt_code", params={"code": current_code, "file_path": file_path})
                adapt_result = await self.team.get_agent("adaptateur").execute_task(adapt_task)
                file_report["sub_steps"].append({"agent": "adaptateur", "result": adapt_result.to_dict()})
                
                if not adapt_result.success:
                    self.log(f"Échec de l'adaptation pour {file_path}, passage au fichier suivant.")
                    continue
                current_code = adapt_result.data["adapted_code"]

                # Étape 5: Optimiseur de performance (si disponible et mode étendu)
                if use_extended and PERFORMANCE_OPTIMIZER_AVAILABLE:
                    perf_task = Task(type="optimize_performance", params={"code": current_code, "file_path": file_path})
                    perf_result = await self.team.get_agent("optimiseur_performance").execute_task(perf_task)
                    file_report["sub_steps"].append({"agent": "optimiseur_performance", "result": perf_result.to_dict()})
                    
                    if perf_result.success:
                        performance_score = perf_result.data["performance_report"]["performance_score"]
                        self.log(f"Score de performance pour {file_path}: {performance_score}/100")

                # Étape 6: Testeur anti-faux agents
                test_task = Task(type="test_code", params={"code": current_code, "file_path": file_path})
                test_result = await self.team.get_agent("testeur").execute_task(test_task)
                file_report["sub_steps"].append({"agent": "testeur", "result": test_result.to_dict()})
                
                if not test_result.success:
                    self.log(f"Échec des tests pour {file_path}, passage au fichier suivant.")
                    continue

                # Étape 7: Documenteur / Peer Reviewer
                doc_task = Task(type="document_code", params={"code": current_code, "file_path": file_path})
                doc_result = await self.team.get_agent("documenteur").execute_task(doc_task)
                file_report["sub_steps"].append({"agent": "documenteur", "result": doc_result.to_dict()})
                
                if not doc_result.success:
                    self.log(f"Échec de la documentation pour {file_path}, passage au fichier suivant.")
                    continue
                current_code = doc_result.data["documented_code"]

                # Étape 8: Validateur final
                validate_task = Task(type="validate_code", params={"code": current_code, "file_path": file_path})
                validate_result = await self.team.get_agent("validateur").execute_task(validate_task)
                file_report["sub_steps"].append({"agent": "validateur", "result": validate_result.to_dict()})
                
                if validate_result.success:
                    # Sauvegarde du fichier final
                    try:
                        with open(os.path.join(self.workspace_path, file_path), "w", encoding="utf-8") as f:
                            f.write(current_code)
                        self.log(f"✅ Fichier {file_path} traité et sauvegardé avec succès.")
                        file_report["status"] = "SUCCESS"
                    except Exception as e:
                        self.log(f"Erreur lors de la sauvegarde de {file_path}: {e}", level="error")
                        file_report["status"] = "SAVE_ERROR"
                        file_report["save_error"] = str(e)
                else:
                    self.log(f"❌ Validation finale échouée pour {file_path}")
                    file_report["status"] = "VALIDATION_FAILED"
                
                processed_files_reports.append(file_report)
            
            # Génération du rapport de synthèse
            mission_report["processed_files"] = processed_files_reports
            mission_report["summary"] = self._generate_mission_summary(processed_files_reports, use_extended)
            mission_report["status"] = "SUCCESS"

        except Exception as e:
            self.log(f"ERREUR CRITIQUE dans la mission {mission_id}: {e}", level="critical")
            mission_report["status"] = "FAILED"
            mission_report["error"] = str(e)
            return Result(success=False, error=str(e), data=mission_report)

        mission_report["end_time"] = datetime.now().isoformat()
        mission_report["duration"] = self._calculate_duration(mission_report["start_time"], mission_report["end_time"])
        
        self.log(f"🎉 Mission {mission_id} terminée avec succès en mode {'étendu' if use_extended else 'standard'}.")
        return Result(success=True, data=mission_report)

    def _generate_mission_summary(self, processed_files: list, extended_mode: bool) -> dict:
        """Génère un résumé de la mission."""
        summary = {
            "total_files_processed": len(processed_files),
            "successful_files": len([f for f in processed_files if f.get("status") == "SUCCESS"]),
            "failed_files": len([f for f in processed_files if f.get("status") != "SUCCESS"]),
            "mode": "extended" if extended_mode else "standard"
        }
        
        # Statistiques détaillées pour le mode étendu
        if extended_mode:
            summary["extended_features"] = {
                "dependency_analysis": DEPENDENCY_MANAGER_AVAILABLE,
                "performance_optimization": PERFORMANCE_OPTIMIZER_AVAILABLE
            }
            
            # Agrégation des métriques de performance si disponibles
            performance_scores = []
            dependency_issues = []
            
            for file_report in processed_files:
                for step in file_report.get("sub_steps", []):
                    if step["agent"] == "optimiseur_performance" and step["result"]["success"]:
                        score = step["result"]["data"]["performance_report"]["performance_score"]
                        performance_scores.append(score)
                    
                    if step["agent"] == "gestionnaire_dependances" and step["result"]["success"]:
                        dep_report = step["result"]["data"]["dependency_report"]
                        dependency_issues.extend(dep_report.get("missing_modules", []))
            
            if performance_scores:
                summary["performance_metrics"] = {
                    "average_score": sum(performance_scores) / len(performance_scores),
                    "min_score": min(performance_scores),
                    "max_score": max(performance_scores),
                    "files_needing_optimization": len([s for s in performance_scores if s < 70])
                }
            
            if dependency_issues:
                summary["dependency_issues"] = {
                    "total_missing_modules": len(set(dependency_issues)),
                    "missing_modules": list(set(dependency_issues))
                }
        
        summary["success_rate"] = (summary["successful_files"] / summary["total_files_processed"] * 100) if summary["total_files_processed"] > 0 else 0
        
        return summary

    def _calculate_duration(self, start_time: str, end_time: str) -> str:
        """Calcule la durée de la mission."""
        try:
            from datetime import datetime
            start = datetime.fromisoformat(start_time)
            end = datetime.fromisoformat(end_time)
            duration = end - start
            return str(duration)
        except Exception:
            return "unknown"


def create_agent_MAINTENANCE_00_chef_equipe_coordinateur_extended(target_path=".", workspace_path=".", extended_mode=True):
    """
    Crée le chef d'équipe de maintenance avec support optionnel des agents étendus.
    
    Args:
        target_path: Chemin du répertoire à analyser
        workspace_path: Espace de travail pour les sauvegardes
        extended_mode: Active les agents complémentaires si disponibles
    """
    factory = AgentFactory()
    
    # Enregistrement des agents de base (obligatoires)
    factory.register_agent_creator("analyseur", AgentMAINTENANCE01AnalyseurStructure, "Analyse la structure des fichiers.")
    factory.register_agent_creator("evaluateur", AgentMAINTENANCE02EvaluateurUtilite, "Évalue l'utilité d'un fichier de code.")
    factory.register_agent_creator("adaptateur", AgentMAINTENANCE03AdaptateurCode, "Adapte le code pour la conformité.")
    factory.register_agent_creator("testeur", AgentMAINTENANCE04TesteurAntiFauxAgents, "Teste le code contre les faux agents.")
    factory.register_agent_creator("documenteur", AgentMAINTENANCE05DocumenteurPeerReviewer, "Documente le code et peer review.")
    factory.register_agent_creator("validateur", AgentMAINTENANCE06ValidateurFinal, "Valide le code final.")

    # Agents de base pour l'équipe
    team_members = ["analyseur", "evaluateur", "adaptateur", "testeur", "documenteur", "validateur"]

    # Enregistrement des agents étendus (optionnels)
    extended_agents_added = []
    
    if extended_mode and DEPENDENCY_MANAGER_AVAILABLE:
        factory.register_agent_creator("gestionnaire_dependances", AgentMAINTENANCE07GestionnaireDependances, "Gère les dépendances Python.")
        team_members.append("gestionnaire_dependances")
        extended_agents_added.append("gestionnaire_dependances")

    if extended_mode and PERFORMANCE_OPTIMIZER_AVAILABLE:
        factory.register_agent_creator("optimiseur_performance", AgentMAINTENANCE08OptimiseurPerformance, "Optimise les performances du code.")
        team_members.append("optimiseur_performance")
        extended_agents_added.append("optimiseur_performance")

    # Création de l'équipe
    team = factory.create_team(team_members)

    # Création du chef d'équipe
    chef_equipe = AgentMAINTENANCE00ChefEquipeCoordinateurExtended(
        agent_id="agent_MAINTENANCE_00_chef_equipe_coordinateur_extended",
        version="2.0",
        description=f"Chef d'équipe de maintenance {'étendue' if extended_agents_added else 'standard'} - Agents: {', '.join(team_members)}",
        team=team,
        workspace_path=workspace_path,
        extended_mode=extended_mode
    )
    
    # Log des capacités
    if extended_agents_added:
        print(f"🚀 Équipe étendue créée avec {len(team_members)} agents :")
        print(f"   📦 Agents de base : analyseur, évaluateur, adaptateur, testeur, documenteur, validateur")
        print(f"   ⚡ Agents étendus : {', '.join(extended_agents_added)}")
    else:
        print(f"📋 Équipe standard créée avec {len(team_members)} agents de base")
        if extended_mode:
            print("   ℹ️  Agents étendus non disponibles (fichiers non trouvés)")
    
    return chef_equipe


# Alias pour la compatibilité avec l'ancienne version
def create_agent_MAINTENANCE_00_chef_equipe_coordinateur(target_path=".", workspace_path="."):
    """Alias pour compatibilité - crée l'équipe en mode standard."""
    return create_agent_MAINTENANCE_00_chef_equipe_coordinateur_extended(
        target_path=target_path, 
        workspace_path=workspace_path, 
        extended_mode=False
    )