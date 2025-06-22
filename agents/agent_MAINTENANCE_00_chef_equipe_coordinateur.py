#!/usr/bin/env python3
"""
🎖️ CHEF D'ÉQUIPE COORDINATEUR ENTERPRISE TRANSFORMÉ - Pattern Factory NextGeneration
===============================================================================

🎯 Mission : Orchestration centrale de l'équipe de maintenance transformée
⚡ Modèle : Claude Sonnet 4 
🏢 Équipe : NextGeneration Tools Migration - Architecture Enterprise

Nouvelles Capacités Avancées :
- 🚀 Coordination intelligente multi-agents
- 📊 Orchestration de workflows complexes
- 🔄 Gestion automatisée des dépendances
- 📈 Monitoring temps réel de l'équipe
- 🎯 Optimisation de performance collaborative
- 📋 Rapports consolidés avancés

Author: Équipe de Maintenance NextGeneration
Version: 2.0.0 - Enterprise Transformation
Created: 2025-01-19
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys
import time
import json
from abc import ABC, abstractmethod
import logging
import uuid
import importlib
import inspect
import os

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

# --- Imports Post-Path-Correction ---
try:
    from core import logging_manager
    from core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
    try:
        from core.agent_factory_architecture import Agent, Task, Result
        PATTERN_FACTORY_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️ Pattern Factory non disponible: {e}")
        # Fallback pour compatibilité
        class Agent:
            async def __init__(self, agent_type: str, **config):
                self.agent_id = f"chef_equipe_coordinateur_{int(time.time())}"
                self.agent_type = agent_type
                self.config = config
            
            async def startup(self): pass
            async def shutdown(self): pass
            async def health_check(self): return {"status": "healthy"}
            async def get_capabilities(self): return []
    
        class Task:
            async def __init__(self, task_id: str, description: str, **kwargs):
                self.task_id = task_id
                self.description = description
            
        class Result:
            async def __init__(self, success: bool, data: Any = None, error: str = None):
                self.success = success
                self.data = data
                self.error = error
    
        PATTERN_FACTORY_AVAILABLE = False


class ChefEquipeCoordinateurEnterprise(Agent):
    """
    Chef d'équipe pour orchestrer des workflows de maintenance complexes.
    """
    def __init__(
        self,
        agent_id: str = None, 
        agent_type: str = "coordinateur_maintenance",
        target_path: str = None, 
        workspace_path: str = None, 
        **config
    ):
        """Initialisation moderne et robuste."""
        # Création d'un ID unique et fiable dès le départ
        self.agent_id = agent_id or f"{agent_type}_{uuid.uuid4().hex[:8]}"
        self.agent_type = agent_type
        self.config = config

        # --- Initialisation du Logger ---
        if logging_manager:
            custom_conf = {
                "logger_name": f"agent.{self.agent_id}",
                "metadata": {"agent_id": self.agent_id, "role": "chef_equipe"}
            }
            self.logger = logging_manager.get_logger("agent_maintenance", custom_config=custom_conf)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.logger = logging.getLogger(self.agent_id)

        self.logger.info(f"Chef d'équipe initialisé avec ID: {self.agent_id}")
        
        if not target_path:
            raise ValueError("Le paramètre 'target_path' est obligatoire.")
        self.target_path = Path(target_path)
        self.workspace_path = Path(workspace_path or ".")
        
        self.logger.info(f"Répertoire cible : {self.target_path}")
        self.logger.info(f"Workspace : {self.workspace_path}")

        self.equipe_agents = {}
        self.workflows_disponibles = [
            "maintenance_complete"
        ]
        self.config_workflows = {
            "timeout_default": config.get("timeout", 300),
            "max_agents_parallel": config.get("max_agents_parallel", 6),
        }
        
        self.rapport_final = {}
        
    async def startup(self):
        self.logger.info(f"🚀 Chef d'Équipe Coordinateur {self.agent_id} - DÉMARRAGE")
        if not self.target_path.exists():
            raise FileNotFoundError(f"Le répertoire cible n'existe pas : {self.target_path}")
        self.logger.info("✅ Chef d'Équipe prêt.")
        
    async def shutdown(self):
        self.logger.info(f"🛑 Chef d'Équipe Coordinateur {self.agent_id} - ARRÊT")
        for agent in self.equipe_agents.values():
            if hasattr(agent, "shutdown"):
                await agent.shutdown()
                
    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "agent_id": self.agent_id}
    
    def get_capabilities(self) -> List[str]:
        return self.workflows_disponibles
    
    async def execute_task(self, task: Task) -> Result:
        """Point d'entrée principal conforme au Pattern Factory."""
        self.logger.info(f"Tâche reçue: {task.id} - {task.type}")
        
        # On délègue l'exécution au workflow principal
        report = await self.workflow_maintenance_complete(mission_config=task.params)
        
        success = report.get("statut_mission") == "SUCCÈS"
        if success:
            return Result(success=True, data=report)
        else:
            return Result(success=False, data=report, error=report.get("erreur", "Erreur inconnue dans le workflow."))

    async def workflow_maintenance_complete(self, mission_config: Dict = None) -> Dict[str, Any]:
        start_time = time.time()
        mission_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.logger.info(f"🚀 LANCEMENT WORKFLOW COMPLET - MISSION ID: {mission_id}")

        rapport_final = {"mission_id": mission_id, "statut_mission": "INCOMPLET", "etapes": {}}
        rapports_par_agent = {}

        try:
            # Étape 1: Analyse de la structure par l'agent 01 pour obtenir la liste des agents
            self.logger.info("--- Étape 1: Analyse de la structure ---")
            analyseur = await self._instancier_agent("agent_MAINTENANCE_01_analyseur_structure")
            if not analyseur:
                raise Exception("Impossible d'instancier l'agent_MAINTENANCE_01_analyseur_structure")
            
            # L'agent 01 doit avoir une méthode qui retourne la liste des fichiers
            if not hasattr(analyseur, 'run_analysis'):
                 raise Exception("L'agent 01 n'a pas la méthode 'run_analysis'")
            
            analyse_result = await analyseur.run_analysis(self.target_path)
            rapport_final["etapes"]["analyse_structure"] = analyse_result.data
            
            agents_a_traiter = analyse_result.data.get("files", [])
            if not agents_a_traiter:
                raise Exception("Aucun agent trouvé par l'analyseur de structure.")
            
            self.logger.info(f"✅ {len(agents_a_traiter)} agents à traiter.")

            # Étapes suivantes: Boucle sur chaque agent trouvé
            processed_files_reports = []
            for file_info in agents_a_traiter:
                
                # Vérification de robustesse
                if not file_info or not isinstance(file_info, dict):
                    self.logger.warning(f"Information de fichier invalide (pas un dict): {file_info}")
                    continue
                
                agent_path_str = file_info.get("path")
                if not agent_path_str:
                    self.logger.warning(f"Information de fichier invalide (chemin manquant): {file_info}")
                    continue

                agent_path = Path(agent_path_str)
                
                if not agent_path.exists():
                    self.logger.warning(f"Le fichier agent n'existe pas : {agent_path}")
                    continue

                agent_name = agent_path.name
                self.logger.info(f"--- Traitement de l'agent: {agent_name} ---")
                rapports_par_agent[agent_name] = {}

                # Lire le contenu du fichier pour les agents suivants
                with open(agent_path, 'r', encoding='utf-8') as f:
                    agent_code = f.read()

                # Étape 2: Évaluateur
                self.logger.info(f"  -> Étape 2: Évaluation de l'utilité")
                eval_result = await self._run_sub_task("evaluateur", "evaluate_utility", {"code": agent_code, "file_path": agent_path})
                file_report = {"agent_name": agent_name, "evaluation": eval_result.to_dict()}
                if not eval_result.success:
                    self.logger.warning(f"  -> Évaluation échouée, passage au fichier suivant: {eval_result.error}", exc_info=True)
                    processed_files_reports.append(file_report)
                    continue

                # Étape 3: Adaptateur
                self.logger.info(f"  -> Étape 3: Adaptation du code")
                adapt_result = await self._run_sub_task("adaptateur", "adapt_code", {"code": agent_code, "file_path": agent_path})
                file_report["sub_steps"].append({"agent": "adaptateur", "result": adapt_result.to_dict()})
                if not adapt_result.success:
                     self.logger.warning(f"  -> Adaptation échouée, passage au fichier suivant: {adapt_result.error}", exc_info=True)
                     processed_files_reports.append(file_report)
                     continue
                adapted_code = adapt_result.data["adapted_code"]

                # Étape 4: Testeur
                self.logger.info(f"  -> Étape 4: Test dynamique")
                test_result = await self._run_sub_task("testeur", "test_code", {"code": adapted_code, "file_path": agent_path})
                file_report["sub_steps"].append({"agent": "testeur", "result": test_result.to_dict()})
                if not test_result.success:
                    self.logger.warning(f"  -> Tests échoués, passage au fichier suivant: {test_result.error}", exc_info=True)
                    processed_files_reports.append(file_report)
                    continue

                # Étape 5: Documenteur / Peer Reviewer
                self.logger.info(f"  -> Étape 5: Documentation et Peer Review")
                doc_result = await self._run_sub_task("documenteur", "document_code", {"code": adapted_code, "file_path": agent_path})
                file_report["sub_steps"].append({"agent": "documenteur", "result": doc_result.to_dict()})
                if not doc_result.success:
                     self.logger.warning(f"  -> Documentation échouée, passage au fichier suivant: {doc_result.error}", exc_info=True)
                     processed_files_reports.append(file_report)
                     continue
                final_code = doc_result.data["documented_code"]

                # Étape 6: Validateur Final
                self.logger.info(f"  -> Étape 6: Validation finale")
                validate_result = await self._run_sub_task("validateur", "validate_code", {"code": final_code, "file_path": agent_path})
                file_report["sub_steps"].append({"agent": "validateur", "result": validate_result.to_dict()})
                
                if validate_result.success:
                    self.logger.info(f"  -> Validation réussie pour {agent_path}. Sauvegarde...")

                processed_files_reports.append(file_report)

            rapport_final["resultats_par_agent"] = rapports_par_agent
            rapport_final["statut_mission"] = "SUCCÈS"
        except Exception as e:
            rapport_final["statut_mission"] = "ÉCHEC"
            rapport_final["erreur"] = str(e)
            self.logger.error(f"❌ Erreur workflow: {e}", exc_info=True)
        finally:
            end_time = time.time()
            rapport_final["duree_totale_sec"] = round(end_time - start_time, 2)
            self.logger.info(f"🏁 Fin du workflow en {rapport_final['duree_totale_sec']:.2f}s. Statut: {rapport_final['statut_mission']}")
        
        return rapport_final
    
    async def _instancier_agent(self, nom_agent: str) -> Optional[Any]:
        module_path = f"agent_factory_implementation.agents.{nom_agent}"
        try:
            agent_module = importlib.import_module(module_path)
            
            # On force l'utilisation de la factory pour plus de prévisibilité
            factory_name = f"create_{nom_agent}"
            
            if hasattr(agent_module, factory_name):
                factory_func = getattr(agent_module, factory_name)
                # On passe les arguments nécessaires à l'agent
                instance = factory_func(
                    source_path=str(self.target_path),
                    # Ajoutez d'autres arguments si nécessaire pour les autres agents
                )
                self.logger.info(f"✅ Agent '{nom_agent}' instancié via factory.")
                return instance
            else:
                self.logger.error(f"❌ Factory '{factory_name}' non trouvée dans le module {nom_agent}.")
                return None

        except Exception as e:
            self.logger.error(f"❌ Erreur d'instanciation de '{nom_agent}': {e}", exc_info=True)
            return None

    async def _run_sub_task(self, agent_name: str, task_type: str, params: dict) -> Result:
        """Factorise l'appel à un agent de l'équipe."""
        agent = self.equipe_agents.get(agent_name)
        if not agent:
            return Result(success=False, error=f"Agent '{agent_name}' non trouvé dans l'équipe.")
        
        task = Task(type=task_type, params=params)
        return await agent.execute_task(task)

def create_agent_MAINTENANCE_00_chef_equipe_coordinateur(**kwargs) -> ChefEquipeCoordinateurEnterprise:
    return ChefEquipeCoordinateurEnterprise(**kwargs)

# Point d'entrée direct
async def main():
    """Point d'entrée principal Agent 0 Chef d'Équipe"""
    print("🎖️ AGENT 0 - CHEF D'ÉQUIPE COORDINATEUR")
    print("=" * 50)
    
    # Configuration par défaut
    target_path = "../agent_factory_implementation/agents"
    workspace_path = "."
    
    # Arguments en ligne de commande
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h"]:
            print("""
Usage: python agent_0_chef_equipe_coordinateur.py [TARGET_PATH] [WORKSPACE_PATH]

Arguments:
  TARGET_PATH     Chemin vers le répertoire des agents à analyser
  WORKSPACE_PATH  Chemin vers l'espace de travail
  
Exemples:
  python agent_0_chef_equipe_coordinateur.py
  python agent_0_chef_equipe_coordinateur.py ../agents
  python agent_0_chef_equipe_coordinateur.py ../agents ./workspace
""")
            return
        
        target_path = sys.argv[1]
        if len(sys.argv) > 2:
            workspace_path = sys.argv[2]
    
    try:
        # Création et exécution
        chef_equipe = create_agent_MAINTENANCE_00_chef_equipe_coordinateur(target_path, workspace_path)
        await chef_equipe.startup()
        
        # Health check
        health = await chef_equipe.health_check()
        print(f"🏥 Statut: {health['status']}")
        
        # Lancement workflow maintenance complète
        print("\n🚀 Lancement workflow maintenance complète...")
        resultats = await chef_equipe.workflow_maintenance_complete()
        
        # Affichage résultats
        print("\n📊 RÉSULTATS FINAUX:")
        print(f"Status: {resultats['status']}")
        if resultats['status'] == 'complete':
            consolides = resultats.get('resultats_consolides', {})
            print(f"Agents analysés: {consolides.get('agents_analyses', 0)}")
            print(f"Agents valides: {consolides.get('agents_valides', 0)}")
            print(f"Score final: {consolides.get('score_final', 0)}/100")
            print(f"Durée: {resultats.get('duree_totale_sec', 0):.1f}s")
        
        await chef_equipe.shutdown()
        print("✅ Chef d'équipe terminé avec succès")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result) 
