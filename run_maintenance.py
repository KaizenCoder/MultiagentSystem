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
        # Création et démarrage du coordinateur
        coordinator_agent = create_agent_MAINTENANCE_00_chef_equipe_coordinateur(
            workspace_path=str(project_root)
        )
        await coordinator_agent.startup()

        # Création de la tâche de maintenance
        maintenance_task = Task(
            type="workflow_maintenance_complete",
            params={"target_files": target_agent_files}
        )

        # Exécution du workflow
        result = await coordinator_agent.execute_task(maintenance_task)

        if result.success:
            logger.info("--- RAPPORT FINAL DE LA MISSION ---")
            logger.info(f"Statut de la mission : {result.data.get('status', 'INCONNU')}")
            logger.info(f"ID de la mission : {result.data.get('mission_id', 'N/A')}")
            logger.info(f"Durée totale : {result.data.get('duration', 'N/A')}s")
            
            summary = result.data.get('summary', {})
            logger.info(f"Agents traités : {len(summary)}")
            for agent_file, status in summary.items():
                logger.info(f"  - {agent_file}: {status}")
        else:
            logger.error(f"La mission de maintenance a échoué: {result.error}")

    except Exception as e:
        logger.error(f"Une erreur critique est survenue durant l'exécution du workflow: {e}", exc_info=True)
    finally:
        if coordinator_agent:
            await coordinator_agent.shutdown()

def main():
    parser = argparse.ArgumentParser(description="Lance le workflow de maintenance sur des agents cibles.")
    parser.add_argument(
        "--agents",
        nargs="+",
        help="Liste des chemins vers les fichiers d'agents à traiter."
    )
    parser.add_argument(
        "--mission",
        type=str,
        default=f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        help="ID de mission personnalisé."
    )
    args = parser.parse_args()

    if args.agents:
        agents_to_process = args.agents
    else:
        # Liste par défaut mise à jour avec des agents existants
        agents_to_process = [
            "agents/agent_18_auditeur_securite.py",
            "agents/agent_19_auditeur_performance.py",
            "agents/agent_20_auditeur_conformite.py",
            "agents/agent_111_auditeur_qualite.py",
            "agents/agent_111_auditeur_qualite_sprint3.py",
        ]

    asyncio.run(run_maintenance_on_targets(agents_to_process))

if __name__ == "__main__":
    main()