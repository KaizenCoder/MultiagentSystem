import asyncio
import logging
from pathlib import Path
import sys
import argparse

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import ChefEquipeCoordinateurEnterprise
from core.agent_factory_architecture import Task

async def main(target_files: list[str]):
    """
    Script de lancement pour le workflow de maintenance.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("Initialisation du coordinateur de maintenance...")
    coordinateur = ChefEquipeCoordinateurEnterprise(workspace_path=".")
    
    logger.info("Démarrage du coordinateur et de son équipe...")
    await coordinateur.startup()

    mission_config = {
        "target_files": target_files
    }
    
    logger.info(f"Lancement de la mission de maintenance pour les cibles: {target_files}")
    
    task = Task(type="workflow_maintenance_complete", params=mission_config)
    result = await coordinateur.execute_task(task)

    if result.success:
        logger.info("✅ Mission de maintenance terminée avec succès.")
    else:
        logger.error(f"❌ La mission de maintenance a échoué: {result.error}")

    logger.info("Arrêt du coordinateur...")
    await coordinateur.shutdown()

    # Afficher un résumé du rapport
    if result.success and result.data:
        print("\n--- Résumé de la Mission ---")
        for agent_report in result.data.get("resultats_par_agent", []):
            print(f"\nAgent: {agent_report['agent_name']}")
            print(f"  Statut Final: {agent_report['status']}")
            if agent_report['status'] == 'REPAIR_FAILED':
                print(f"  Dernière Erreur: {agent_report['last_error']}")
        print("--------------------------\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Lance le workflow de maintenance sur un ou plusieurs fichiers d'agent.")
    parser.add_argument(
        '--target_files', 
        nargs='+', 
        required=True,
        help="Liste des chemins vers les fichiers d'agent à traiter."
    )
    args = parser.parse_args()
    
    asyncio.run(main(args.target_files)) 