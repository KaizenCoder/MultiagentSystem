import asyncio
import logging
import json
from pathlib import Path
import sys
import argparse
from datetime import datetime

# Assurer que le chemin du projet est dans sys.path pour les imports
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_MAINTENANCE_00_chef_equipe_coordinateur
from core.agent_factory_architecture import Task, Result

async def run_maintenance_on_targets(target_agent_files: list[str]):
    """
    Lance le workflow de maintenance complet sur une liste d'agents spécifiée.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("MaintenanceWorkflowRunner")

    coordinator_agent = None
    try:
        # Création du chef d'équipe avec le bon workspace_path
        coordinator_agent = create_agent_MAINTENANCE_00_chef_equipe_coordinateur(
            workspace_path=str(project_root)
        )

        # Démarrage de l'agent et de son équipe
        await coordinator_agent.startup()
        
        # Configuration de la mission avec les cibles spécifiques
        mission_config = {
            "target_files": target_agent_files
        }

        # Création et exécution de la tâche de maintenance
        maintenance_task = Task(
            id=f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type="workflow_maintenance_complete",
            params=mission_config
        )

        logger.info("Lancement du workflow de maintenance sur les cibles...")
        final_report_result = await coordinator_agent.execute_task(maintenance_task)
        
        logger.info("--- RAPPORT FINAL DE LA MISSION ---")
        if final_report_result.success:
            logger.info("Statut de la mission : SUCCÈS")
        else:
            logger.error(f"Statut de la mission : ÉCHEC - {final_report_result.error}")
        
        # Le rapport détaillé est déjà loggué et sauvegardé par le coordinateur.
        # On affiche ici un résumé.
        final_report = final_report_result.data
        if final_report:
            logger.info(f"ID de la mission : {final_report.get('mission_id')}")
            logger.info(f"Durée totale : {final_report.get('duree_totale_sec')}s")
            results_by_agent = final_report.get("resultats_par_agent", [])
            logger.info(f"Agents traités : {len(results_by_agent)}")
            for agent_report in results_by_agent:
                logger.info(f"  - {agent_report.get('agent_name')}: {agent_report.get('status')}")

    except Exception as e:
        logger.error(f"Une erreur critique est survenue durant l'exécution du workflow: {e}", exc_info=True)
    
    finally:
        if coordinator_agent:
            await coordinator_agent.shutdown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lance le workflow de maintenance sur une liste d'agents.")
    parser.add_argument(
        '--agents', 
        nargs='+', 
        help="Liste des chemins vers les fichiers des agents à traiter.",
        required=False
    )
    args = parser.parse_args()

    # Si des agents sont passés en argument, on les utilise.
    # Sinon, on utilise la liste par défaut pour la rétrocompatibilité.
    if args.agents:
        agents_a_tester = args.agents
        print(f"INFO: Lancement de la maintenance sur les {len(agents_a_tester)} agents spécifiés en argument.")
    else:
        agents_a_tester = [
            # NOTE: Cette liste est utilisée si aucun agent n'est spécifié via --agents
            "agents/agent_MAINTENANCE_01_analyseur_structure.py",
            "agents/agent_MAINTENANCE_02_evaluateur_utilite.py",
            "agents/agent_MAINTENANCE_03_adaptateur_code.py",
            "agents/agent_MAINTENANCE_04_testeur_anti_faux_agents.py",
            "agents/agent_MAINTENANCE_05_documenteur_peer_reviewer.py",
            "agents/agent_MAINTENANCE_06_validateur_final.py"
        ]
        print(f"INFO: Aucun agent spécifié. Utilisation de la liste par défaut de l'équipe de maintenance ({len(agents_a_tester)} agents).")

    asyncio.run(run_maintenance_on_targets(agents_a_tester))