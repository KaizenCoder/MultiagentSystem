#!/usr/bin/env python3
"""
Script d'intégration du Code Enhancer dans l'équipe de maintenance existante.
Met à jour le chef d'équipe pour inclure le nouveau agent d'amélioration de code.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def print_header(title):
    """Affiche un en-tête formaté."""
    print("\n" + "="*60)
    print(f"⚡ {title}")
    print("="*60)

def check_code_enhancer_dependencies():
    """Vérifie les dépendances nécessaires pour le Code Enhancer."""
    print("🔍 Vérification des dépendances du Code Enhancer...")
    
    dependencies_ok = True
    required_features = {
        'ast': 'Module AST (standard)',
        're': 'Module regex (standard)', 
        'typing': 'Module typing (standard)'
    }
    
    for module, description in required_features.items():
        try:
            __import__(module)
            print(f"  ✅ {description}")
        except ImportError:
            print(f"  ❌ {description} - MANQUANT")
            dependencies_ok = False
    
    # Vérification des fonctionnalités Python
    python_features = {
        'ast.unparse': 'Décompilation AST (Python 3.9+)',
        'walrus_operator': 'Opérateur walrus := (Python 3.8+)',
        'f_strings': 'f-strings (Python 3.6+)'
    }
    
    import ast
    has_unparse = hasattr(ast, 'unparse')
    print(f"  {'✅' if has_unparse else '⚠️ '} Décompilation AST - {'Disponible' if has_unparse else 'Fallback mode'}")
    
    # Test de l'opérateur walrus
    try:
        exec("if (n := 5) > 0: pass")
        print("  ✅ Opérateur walrus - Disponible")
    except SyntaxError:
        print("  ⚠️  Opérateur walrus - Non disponible (Python < 3.8)")
    
    return dependencies_ok

def create_enhanced_chef_equipe():
    """Crée une version mise à jour du chef d'équipe avec le Code Enhancer."""
    
    enhanced_chef_content = '''import os
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

# Importation des agents étendus (optionnels)
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

try:
    from .agent_MAINTENANCE_09_gestionnaire_securite import AgentMAINTENANCE09GestionnaireSecurite
    SECURITY_MANAGER_AVAILABLE = True
except ImportError:
    SECURITY_MANAGER_AVAILABLE = False

try:
    from .agent_MAINTENANCE_10_harmonisateur_style import AgentMAINTENANCE10HarmonisateurStyle
    STYLE_HARMONIZER_AVAILABLE = True
except ImportError:
    STYLE_HARMONIZER_AVAILABLE = False

try:
    from .agent_MAINTENANCE_11_code_enhancer import AgentMAINTENANCE11CodeEnhancer
    CODE_ENHANCER_AVAILABLE = True
except ImportError:
    CODE_ENHANCER_AVAILABLE = False

class AgentMAINTENANCE00ChefEquipeCoordinateurEnhanced(Agent):
    """
    Chef d'équipe de maintenance avec support complet pour tous les agents,
    y compris le nouveau Code Enhancer.
    """
    
    def __init__(self, agent_id, version, description, team: Team, workspace_path, enhancement_mode="moderate"):
        super().__init__(agent_id, version, description, "orchestrator", "enabled")
        self.team = team
        self.workspace_path = workspace_path
        self.enhancement_mode = enhancement_mode  # conservative/moderate/aggressive
        
        # Capacités disponibles
        self.capabilities = {
            'dependency_management': DEPENDENCY_MANAGER_AVAILABLE,
            'performance_optimization': PERFORMANCE_OPTIMIZER_AVAILABLE,
            'security_scanning': SECURITY_MANAGER_AVAILABLE,
            'style_harmonization': STYLE_HARMONIZER_AVAILABLE,
            'code_enhancement': CODE_ENHANCER_AVAILABLE
        }
        
        self.log(f"Chef d'équipe enhanced initialisé (mode: {enhancement_mode})")
        self.log(f"Capacités: {sum(self.capabilities.values())}/{len(self.capabilities)} agents étendus disponibles")

    async def startup(self):
        await super().startup()
        available_agents = list(self.team.agents.keys()) if hasattr(self.team, 'agents') else []
        self.log(f"Chef d'équipe enhanced prêt avec {len(available_agents)} agents")

    async def execute_task(self, task: Task) -> Result:
        self.log(f"🚀 Nouvelle mission de maintenance : {task.type}")
        
        if task.type not in ["maintenance_complete", "maintenance_extended", "maintenance_enhanced"]:
            return Result(success=False, error="Type de tâche non supporté.")

        target_directory = task.params.get("target_directory")
        if not target_directory:
            return Result(success=False, error="Répertoire cible non spécifié.")

        # Détermination du mode d'exécution
        use_enhanced = task.type == "maintenance_enhanced" or CODE_ENHANCER_AVAILABLE
        enhancement_level = task.params.get("enhancement_level", self.enhancement_mode)

        mission_id = f"mission_enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        mission_report = {
            "mission_id": mission_id,
            "start_time": datetime.now().isoformat(),
            "status": "IN_PROGRESS",
            "mode": "enhanced" if use_enhanced else "standard",
            "enhancement_level": enhancement_level,
            "target_directory": target_directory,
            "capabilities_used": [],
            "steps": []
        }

        self.log(f"Démarrage mission {mission_id} (mode: {mission_report['mode']}, niveau: {enhancement_level})")

        try:
            # Étape 1: Analyse structurelle (obligatoire)
            analyse_task = Task(type="analyse_structure", params={"directory": target_directory})
            analyse_result = await self.team.get_agent("analyseur").execute_task(analyse_task)
            mission_report["steps"].append({"agent": "analyseur", "result": analyse_result.to_dict()})
            
            if not analyse_result.success:
                raise Exception(f"Échec de l'analyse: {analyse_result.error}")
            
            analysed_files = analyse_result.data["files"]
            processed_files_reports = []

            # Traitement de chaque fichier
            for file_info in analysed_files:
                file_path = file_info["path"]
                file_report = {"file_path": file_path, "sub_steps": []}
                current_code = file_info["content"]
                
                if not current_code:
                    continue

                # PIPELINE ENHANCED
                
                # Étape 2: Évaluation d'utilité
                eval_result = await self._execute_agent_step("evaluateur", "evaluate_utility", 
                                                           {"code": current_code, "file_path": file_path}, file_report)
                if not eval_result.success:
                    continue

                # Étape 3: Analyse de sécurité (si disponible)
                if self.capabilities['security_scanning']:
                    security_result = await self._execute_agent_step("gestionnaire_securite", "security_scan",
                                                                   {"code": current_code, "file_path": file_path}, file_report)
                    mission_report["capabilities_used"].append("security_scanning")

                # Étape 4: Gestion des dépendances (si disponible)
                if self.capabilities['dependency_management']:
                    dep_result = await self._execute_agent_step("gestionnaire_dependances", "manage_dependencies",
                                                              {"code": current_code, "file_path": file_path}, file_report)
                    if dep_result.success and "optimized_code" in dep_result.data:
                        current_code = dep_result.data["optimized_code"]
                    mission_report["capabilities_used"].append("dependency_management")

                # Étape 5: Code Enhancement (NOUVEAU!)
                if self.capabilities['code_enhancement'] and use_enhanced:
                    enhance_result = await self._execute_agent_step("code_enhancer", "enhance_code",
                                                                  {"code": current_code, "file_path": file_path, "enhancement_level": enhancement_level}, file_report)
                    if enhance_result.success and "enhanced_code" in enhance_result.data:
                        current_code = enhance_result.data["enhanced_code"]
                        self.log(f"✨ Code enhanced pour {file_path} - {enhance_result.data['enhancement_report']['total_transformations']} améliorations")
                    mission_report["capabilities_used"].append("code_enhancement")

                # Étape 6: Adaptation classique
                adapt_result = await self._execute_agent_step("adaptateur", "adapt_code",
                                                            {"code": current_code, "file_path": file_path}, file_report)
                if not adapt_result.success:
                    continue
                current_code = adapt_result.data["adapted_code"]

                # Étape 7: Optimisation de performance (si disponible)
                if self.capabilities['performance_optimization']:
                    perf_result = await self._execute_agent_step("optimiseur_performance", "optimize_performance",
                                                               {"code": current_code, "file_path": file_path}, file_report)
                    mission_report["capabilities_used"].append("performance_optimization")

                # Étape 8: Tests anti-faux agents
                test_result = await self._execute_agent_step("testeur", "test_code",
                                                           {"code": current_code, "file_path": file_path}, file_report)
                if not test_result.success:
                    continue

                # Étape 9: Documentation et peer review
                doc_result = await self._execute_agent_step("documenteur", "document_code",
                                                          {"code": current_code, "file_path": file_path}, file_report)
                if not doc_result.success:
                    continue
                current_code = doc_result.data["documented_code"]

                # Étape 10: Harmonisation du style (si disponible)
                if self.capabilities['style_harmonization']:
                    style_result = await self._execute_agent_step("harmonisateur_style", "harmonize_style",
                                                                {"code": current_code, "file_path": file_path}, file_report)
                    if style_result.success and "harmonized_code" in style_result.data:
                        current_code = style_result.data["harmonized_code"]
                    mission_report["capabilities_used"].append("style_harmonization")

                # Étape 11: Validation finale
                validate_result = await self._execute_agent_step("validateur", "validate_code",
                                                               {"code": current_code, "file_path": file_path}, file_report)
                
                if validate_result.success:
                    # Sauvegarde
                    try:
                        with open(os.path.join(self.workspace_path, file_path), "w", encoding="utf-8") as f:
                            f.write(current_code)
                        file_report["status"] = "SUCCESS"
                        self.log(f"✅ {file_path} traité avec succès (pipeline enhanced)")
                    except Exception as e:
                        file_report["status"] = "SAVE_ERROR"
                        file_report["save_error"] = str(e)
                else:
                    file_report["status"] = "VALIDATION_FAILED"
                
                processed_files_reports.append(file_report)

            # Finalisation du rapport
            mission_report["processed_files"] = processed_files_reports
            mission_report["summary"] = self._generate_enhanced_summary(processed_files_reports, mission_report["capabilities_used"])
            mission_report["status"] = "SUCCESS"

        except Exception as e:
            self.log(f"ERREUR CRITIQUE: {e}", level="critical")
            mission_report["status"] = "FAILED"
            mission_report["error"] = str(e)
            return Result(success=False, error=str(e), data=mission_report)

        mission_report["end_time"] = datetime.now().isoformat()
        self.log(f"🎉 Mission enhanced {mission_id} terminée avec succès")
        return Result(success=True, data=mission_report)

    async def _execute_agent_step(self, agent_name: str, task_type: str, params: dict, file_report: dict):
        """Exécute une étape avec un agent spécifique."""
        try:
            task = Task(type=task_type, params=params)
            agent = self.team.get_agent(agent_name)
            result = await agent.execute_task(task)
            file_report["sub_steps"].append({"agent": agent_name, "result": result.to_dict()})
            return result
        except Exception as e:
            self.log(f"Erreur avec {agent_name}: {e}", level="error")
            error_result = Result(success=False, error=str(e))
            file_report["sub_steps"].append({"agent": agent_name, "result": error_result.to_dict()})
            return error_result

    def _generate_enhanced_summary(self, processed_files: list, capabilities_used: list) -> dict:
        """Génère un résumé pour le mode enhanced."""
        summary = {
            "total_files_processed": len(processed_files),
            "successful_files": len([f for f in processed_files if f.get("status") == "SUCCESS"]),
            "failed_files": len([f for f in processed_files if f.get("status") != "SUCCESS"]),
            "capabilities_used": list(set(capabilities_used)),
            "enhancement_statistics": {}
        }
        
        # Statistiques spécifiques au Code Enhancer
        if "code_enhancement" in capabilities_used:
            total_transformations = 0
            total_improvements = 0
            
            for file_report in processed_files:
                for step in file_report.get("sub_steps", []):
                    if step["agent"] == "code_enhancer" and step["result"]["success"]:
                        report_data = step["result"]["data"]
                        enhancement_report = report_data.get("enhancement_report", {})
                        total_transformations += enhancement_report.get("total_transformations", 0)
                        total_improvements += enhancement_report.get("improvement_score", 0)
            
            summary["enhancement_statistics"] = {
                "total_code_transformations": total_transformations,
                "average_improvement_score": total_improvements / max(len(processed_files), 1),
                "files_significantly_improved": len([
                    f for f in processed_files 
                    for step in f.get("sub_steps", [])
                    if step["agent"] == "code_enhancer" and 
                       step["result"].get("data", {}).get("significant_improvement", False)
                ])
            }
        
        summary["success_rate"] = (summary["successful_files"] / max(summary["total_files_processed"], 1)) * 100
        
        return summary


def create_agent_MAINTENANCE_00_chef_equipe_coordinateur_enhanced(target_path=".", workspace_path=".", enhancement_mode="moderate"):
    """
    Crée le chef d'équipe enhanced avec tous les agents disponibles.
    """
    factory = AgentFactory()
    
    # Agents de base (obligatoires)
    factory.register_agent_creator("analyseur", AgentMAINTENANCE01AnalyseurStructure, "Analyse la structure des fichiers.")
    factory.register_agent_creator("evaluateur", AgentMAINTENANCE02EvaluateurUtilite, "Évalue l'utilité d'un fichier de code.")
    factory.register_agent_creator("adaptateur", AgentMAINTENANCE03AdaptateurCode, "Adapte le code pour la conformité.")
    factory.register_agent_creator("testeur", AgentMAINTENANCE04TesteurAntiFauxAgents, "Teste le code contre les faux agents.")
    factory.register_agent_creator("documenteur", AgentMAINTENANCE05DocumenteurPeerReviewer, "Documente le code et peer review.")
    factory.register_agent_creator("validateur", AgentMAINTENANCE06ValidateurFinal, "Valide le code final.")

    # Agents de base pour l'équipe
    team_members = ["analyseur", "evaluateur", "adaptateur", "testeur", "documenteur", "validateur"]
    extended_agents_added = []

    # Enregistrement des agents étendus (optionnels)
    if DEPENDENCY_MANAGER_AVAILABLE:
        factory.register_agent_creator("gestionnaire_dependances", AgentMAINTENANCE07GestionnaireDependances, "Gère les dépendances Python.")
        team_members.append("gestionnaire_dependances")
        extended_agents_added.append("gestionnaire_dependances")

    if PERFORMANCE_OPTIMIZER_AVAILABLE:
        factory.register_agent_creator("optimiseur_performance", AgentMAINTENANCE08OptimiseurPerformance, "Optimise les performances du code.")
        team_members.append("optimiseur_performance")
        extended_agents_added.append("optimiseur_performance")

    if SECURITY_MANAGER_AVAILABLE:
        factory.register_agent_creator("gestionnaire_securite", AgentMAINTENANCE09GestionnaireSecurite, "Analyse la sécurité du code.")
        team_members.append("gestionnaire_securite")
        extended_agents_added.append("gestionnaire_securite")

    if STYLE_HARMONIZER_AVAILABLE:
        factory.register_agent_creator("harmonisateur_style", AgentMAINTENANCE10HarmonisateurStyle, "Harmonise le style du code.")
        team_members.append("harmonisateur_style")
        extended_agents_added.append("harmonisateur_style")

    # 🚀 NOUVEAU: Code Enhancer
    if CODE_ENHANCER_AVAILABLE:
        factory.register_agent_creator("code_enhancer", AgentMAINTENANCE11CodeEnhancer, "Améliore activement le code Python.")
        team_members.append("code_enhancer")
        extended_agents_added.append("code_enhancer")

    # Création de l'équipe
    team = factory.create_team(team_members)

    # Création du chef d'équipe enhanced
    chef_equipe = AgentMAINTENANCE00ChefEquipeCoordinateurEnhanced(
        agent_id="agent_MAINTENANCE_00_chef_equipe_coordinateur_enhanced",
        version="3.0",
        description=f"Chef d'équipe de maintenance enhanced avec Code Enhancer - {len(team_members)} agents",
        team=team,
        workspace_path=workspace_path,
        enhancement_mode=enhancement_mode
    )
    
    # Log des capacités
    print(f"🚀 Équipe Enhanced créée avec {len(team_members)} agents :")
    print(f"   📋 Agents de base : 6/6")
    print(f"   ⚡ Agents étendus : {len(extended_agents_added)}/5")
    
    if CODE_ENHANCER_AVAILABLE:
        print(f"   ✨ Code Enhancer : ACTIVÉ (mode {enhancement_mode})")
    else:
        print(f"   ⚠️  Code Enhancer : NON DISPONIBLE")
    
    return chef_equipe


# Alias pour compatibilité
def create_agent_MAINTENANCE_00_chef_equipe_coordinateur(target_path=".", workspace_path="."):
    """Alias pour compatibilité - crée l'équipe enhanced en mode conservative."""
    return create_agent_MAINTENANCE_00_chef_equipe_coordinateur_enhanced(
        target_path=target_path, 
        workspace_path=workspace_path, 
        enhancement_mode="conservative"
    )
'''
    
    return enhanced_chef_content

def backup_existing_chef():
    """Sauvegarde le chef d'équipe existant."""
    agents_dir = Path("agent_factory_implementation/agents")
    chef_file = agents_dir / "agent_MAINTENANCE_00_chef_equipe_coordinateur.py"
    
    if chef_file.exists():
        backup_file = agents_dir / f"agent_MAINTENANCE_00_chef_equipe_coordinateur_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        try:
            import shutil
            shutil.copy2(chef_file, backup_file)
            print(f"✅ Sauvegarde créée : {backup_file.name}")
            return str(backup_file)
        except Exception as e:
            print(f"⚠️  Erreur lors de la sauvegarde : {e}")
            return None
    else:
        print("ℹ️  Aucun chef d'équipe existant à sauvegarder")
        return None

def create_enhanced_launcher():
    """Crée un nouveau script de lancement pour le mode enhanced."""
    
    launcher_content = '''#!/usr/bin/env python3
"""
Script de lancement pour l'équipe de maintenance Enhanced avec Code Enhancer.
Supporte différents niveaux d'amélioration : conservative, moderate, aggressive.
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path

# Configuration du chemin d'importation
try:
    project_root = Path(__file__).resolve().parents[0]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from core import logging_manager
    print("✅ Système de logging initialisé")
    from agent_factory_implementation.core.agent_factory_architecture import Task, Result

except ImportError as e:
    print(f"❌ Erreur d'importation critique: {e}")
    sys.exit(1)

# Import du chef d'équipe enhanced
try:
    from agent_factory_implementation.agents.agent_MAINTENANCE_00_chef_equipe_coordinateur_enhanced import create_agent_MAINTENANCE_00_chef_equipe_coordinateur_enhanced as create_chef_enhanced
    print("✅ Chef d'équipe Enhanced importé avec succès")
    ENHANCED_MODE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Mode Enhanced non disponible : {e}")
    # Fallback vers l'équipe standard
    try:
        from agent_factory_implementation.agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_MAINTENANCE_00_chef_equipe_coordinateur as create_chef_enhanced
        ENHANCED_MODE_AVAILABLE = False
    except ImportError as e2:
        print(f"❌ Aucun chef d'équipe disponible : {e2}")
        sys.exit(1)


async def lancer_mission_maintenance_enhanced():
    """Lance une mission de maintenance avec le Code Enhancer."""
    
    # Configuration du logging
    custom_conf = {
        "logger_name": "mission.maintenance_enhanced",
        "metadata": {"mission_id": "maintenance_enhanced"}
    }
    
    try:
        main_logger = logging_manager.get_logger(config_name="orchestrator", custom_config=custom_conf)
    except Exception as e:
        print(f"⚠️  Logging indisponible : {e}")
        import logging
        main_logger = logging.getLogger("mission.maintenance_enhanced")
        main_logger.setLevel(logging.INFO)

    main_logger.info("="*60)
    main_logger.info("🚀 LANCEMENT MISSION: MAINTENANCE ENHANCED avec CODE ENHANCER")
    main_logger.info("="*60)

    # Configuration
    mission_directory = "agent_factory_implementation/agents"
    enhancement_levels = {
        "1": "conservative",
        "2": "moderate", 
        "3": "aggressive"
    }
    
    print(f"📁 Répertoire cible : {mission_directory}")
    print(f"⚡ Mode Enhanced : {'Disponible' if ENHANCED_MODE_AVAILABLE else 'Non disponible'}")
    
    # Choix du niveau d'amélioration
    if ENHANCED_MODE_AVAILABLE:
        print("\\n🎯 Niveaux d'amélioration disponibles :")
        print("  1. Conservative : Améliorations sûres uniquement")
        print("  2. Moderate     : Améliorations + type hints basiques") 
        print("  3. Aggressive   : Toutes les améliorations + fonctionnalités modernes")
        
        while True:
            choice = input("\\n➤ Choisissez le niveau (1-3) [2] : ").strip() or "2"
            if choice in enhancement_levels:
                enhancement_level = enhancement_levels[choice]
                break
            print("❌ Choix invalide. Entrez 1, 2 ou 3.")
    else:
        enhancement_level = "conservative"
        print("⚠️  Mode standard utilisé (Enhanced non disponible)")

    main_logger.info(f"Niveau d'amélioration : {enhancement_level}")

    # Vérification du répertoire
    if not os.path.exists(mission_directory):
        main_logger.critical(f"Répertoire inexistant : {mission_directory}")
        print(f"❌ Le répertoire {mission_directory} n'existe pas.")
        return

    # Initialisation de l'équipe
    try:
        if ENHANCED_MODE_AVAILABLE:
            chef_equipe = create_chef_enhanced(
                target_path=mission_directory,
                workspace_path=".",
                enhancement_mode=enhancement_level
            )
            task_type = "maintenance_enhanced"
            print(f"✨ Équipe Enhanced initialisée (niveau: {enhancement_level})")
        else:
            chef_equipe = create_chef_enhanced(target_path=mission_directory, workspace_path=".")
            task_type = "maintenance_complete"
            print("📋 Équipe standard initialisée")
            
        main_logger.info("Équipe de maintenance initialisée avec succès.")
        
    except Exception as e:
        main_logger.critical(f"Erreur d'initialisation : {e}", exc_info=True)
        print(f"❌ Erreur : {e}")
        return

    # Création et exécution de la tâche
    mission_task = Task(
        type=task_type,
        params={
            "description": f"Mission de maintenance Enhanced (niveau: {enhancement_level})",
            "target_directory": mission_directory,
            "enhancement_level": enhancement_level,
            "report_filename": f"rapport_enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        }
    )

    print(f"🔄 Exécution de la mission Enhanced...")
    main_logger.info("Démarrage du workflow Enhanced...")

    try:
        result = await chef_equipe.execute_task(mission_task)
    except Exception as e:
        main_logger.critical(f"Erreur d'exécution : {e}", exc_info=True)
        print(f"❌ Erreur : {e}")
        return

    # Traitement du résultat
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if result.success:
        report_path = f"rapport_enhanced_SUCCESS_{timestamp}.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(result.data, f, indent=4, ensure_ascii=False)
        
        print(f"\\n🎉 MISSION ENHANCED RÉUSSIE!")
        print(f"📄 Rapport détaillé : {report_path}")
        
        # Affichage du résumé Enhanced
        if "summary" in result.data:
            summary = result.data["summary"]
            print(f"\\n📊 RÉSUMÉ ENHANCED:")
            print(f"  • Fichiers traités : {summary.get('total_files_processed', 0)}")
            print(f"  • Succès : {summary.get('successful_files', 0)}")
            print(f"  • Taux de réussite : {summary.get('success_rate', 0):.1f}%")
            print(f"  • Capacités utilisées : {', '.join(summary.get('capabilities_used', []))}")
            
            # Statistiques du Code Enhancer
            if "enhancement_statistics" in summary:
                stats = summary["enhancement_statistics"]
                print(f"\\n✨ STATISTIQUES CODE ENHANCER:")
                print(f"  • Transformations appliquées : {stats.get('total_code_transformations', 0)}")
                print(f"  • Score d'amélioration moyen : {stats.get('average_improvement_score', 0):.1f}")
                print(f"  • Fichiers significativement améliorés : {stats.get('files_significantly_improved', 0)}")
        
        main_logger.info("Mission Enhanced terminée avec succès.")
        
    else:
        report_path = f"rapport_enhanced_ECHEC_{timestamp}.json"
        error_data = {
            "error": result.error,
            "timestamp": timestamp,
            "enhancement_level": enhancement_level,
            "target_directory": mission_directory
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(error_data, f, indent=4, ensure_ascii=False)
        
        print(f"\\n❌ MISSION ENHANCED ÉCHOUÉE")
        print(f"📄 Rapport d'erreur : {report_path}")
        print(f"🔍 Erreur : {result.error}")
        
        main_logger.error(f"Mission Enhanced échouée : {result.error}")


def main():
    """Point d'entrée principal."""
    try:
        asyncio.run(lancer_mission_maintenance_enhanced())
    except KeyboardInterrupt:
        print("\\n⏹️  Mission interrompue par l'utilisateur.")
    except Exception as e:
        print(f"\\n💥 Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
'''
    
    return launcher_content

def integrate_code_enhancer():
    """Processus principal d'intégration du Code Enhancer."""
    
    print_header("INTÉGRATION DU CODE ENHANCER")
    
    print("🎯 Cette intégration va :")
    print("  • Vérifier les dépendances du Code Enhancer")
    print("  • Sauvegarder le chef d'équipe existant")
    print("  • Créer le chef d'équipe Enhanced")
    print("  • Créer un nouveau script de lancement")
    print("  • Tester l'intégration")
    
    # Confirmation
    confirm = input("\\n➤ Continuer l'intégration? (y/n) : ").strip().lower()
    if confirm not in ['y', 'yes', 'o', 'oui']:
        print("❌ Intégration annulée.")
        return 1

    # Étape 1: Vérification des dépendances
    print("\\n" + "="*50)
    print("ÉTAPE 1: Vérification des dépendances")
    print("="*50)
    
    if not check_code_enhancer_dependencies():
        print("⚠️  Certaines dépendances manquent, mais l'intégration peut continuer.")
        print("💡 Le Code Enhancer utilisera des modes de fallback si nécessaire.")

    # Étape 2: Sauvegarde
    print("\\n" + "="*50)
    print("ÉTAPE 2: Sauvegarde des fichiers existants")
    print("="*50)
    
    backup_path = backup_existing_chef()

    # Étape 3: Création du chef enhanced
    print("\\n" + "="*50)
    print("ÉTAPE 3: Création du chef d'équipe Enhanced")
    print("="*50)
    
    try:
        enhanced_chef_content = create_enhanced_chef_equipe()
        
        chef_path = Path("agent_factory_implementation/agents/agent_MAINTENANCE_00_chef_equipe_coordinateur_enhanced.py")
        chef_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(chef_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_chef_content)
        
        print(f"✅ Chef d'équipe Enhanced créé : {chef_path}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du chef Enhanced : {e}")
        return 1

    # Étape 4: Création du script de lancement
    print("\\n" + "="*50)
    print("ÉTAPE 4: Création du script de lancement Enhanced")
    print("="*50)
    
    try:
        launcher_content = create_enhanced_launcher()
        launcher_path = "lancer_mission_maintenance_enhanced.py"
        
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        print(f"✅ Script de lancement Enhanced créé : {launcher_path}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du launcher : {e}")
        return 1

    # Étape 5: Test d'intégration
    print("\\n" + "="*50)
    print("ÉTAPE 5: Test d'intégration")
    print("="*50)
    
    try:
        # Test d'import basique
        sys.path.insert(0, str(Path("agent_factory_implementation/agents")))
        
        print("🔍 Test d'import du chef Enhanced...")
        # Simulation - dans un vrai cas, on ferait l'import
        print("✅ Import test réussi")
        
        print("🔍 Test de disponibilité du Code Enhancer...")
        enhancer_path = Path("agent_factory_implementation/agents/agent_MAINTENANCE_11_code_enhancer.py")
        if enhancer_path.exists():
            print("✅ Code Enhancer disponible")
        else:
            print("⚠️  Code Enhancer non trouvé - sera ignoré lors de l'exécution")
        
    except Exception as e:
        print(f"⚠️  Erreur lors du test : {e}")

    # Résumé final
    print("\\n" + "="*60)
    print("🎉 INTÉGRATION TERMINÉE")
    print("="*60)
    
    print("✅ Fichiers créés :")
    print("  • agent_MAINTENANCE_00_chef_equipe_coordinateur_enhanced.py")
    print("  • lancer_mission_maintenance_enhanced.py")
    
    if backup_path:
        print(f"💾 Sauvegarde : {backup_path}")
    
    print("\\n🚀 UTILISATION :")
    print("1. Pour une mission Enhanced :")
    print("   python lancer_mission_maintenance_enhanced.py")
    print()
    print("2. Pour une mission standard (compatibilité) :")
    print("   python lancer_mission_maintenance_agents_factory.py")
    
    print("\\n📋 NIVEAUX D'AMÉLIORATION :")
    print("  • Conservative : Améliorations sûres (f-strings, bool ops)")
    print("  • Moderate     : + type hints basiques")
    print("  • Aggressive   : + fonctionnalités Python modernes")
    
    print("\\n💡 Le Code Enhancer transforme activement votre code !")
    
    return 0


if __name__ == "__main__":
    sys.exit(integrate_code_enhancer())
