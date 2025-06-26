# tests/test_agent_05_report_generation.py
import asyncio
import logging
import os
import sys
from pathlib import Path

# Ajout du répertoire parent au path pour résoudre les imports locaux
sys.path.append(str(Path(__file__).resolve().parent.parent))

from agents.agent_05_maitre_tests_validation import Agent05MaitreTestsValidation
from core.agent_factory_architecture import Task, Result

async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("Démarrage du test de génération de rapport pour l'Agent 05...")

    try:
        # L'agent 05 charge sa config depuis un fichier, donc pas besoin de passer agent_id/version ici explicitement
        # s'ils sont bien dans maintenance_config.json et lus par l'agent.
        # L'agent_id par défaut est "agent_05_maitre_tests_validation"
        agent = Agent05MaitreTestsValidation()
        logger.info(f"Agent {agent.agent_id} v{agent.version} instancié.") # Accès aux attributs définis dans __init__
    except Exception as e:
        logger.error(f"Erreur lors de l'instanciation de l'agent : {e}", exc_info=True)
        return

    task_params = {
        "cible": "module_paiement_v2",
        "objectifs_specifiques": ["Valider la robustesse des API", "Vérifier la conformité des schémas de données"],
        "type_rapport": "tests",
        "format_sortie": "markdown"
    }
    report_task = Task(
        type="generate_strategic_report",
        params=task_params
    )
    logger.info(f"Tâche de génération de rapport créée : {report_task.id} pour le type '{report_task.params.get('type_rapport')}' en format '{report_task.params.get('format_sortie')}'.")

    try:
        logger.info(f"Exécution de la tâche {report_task.id}...")
        result = await agent.execute_task(report_task)
        logger.info("Tâche exécutée.")

        if result.success:
            logger.info("Résultat de la tâche : SUCCÈS")
            report_filepath = result.data.get('fichier_sauvegarde')
            if report_filepath:
                logger.info(f"Rapport Markdown devrait être sauvegardé ici : {report_filepath}")
                if os.path.exists(report_filepath):
                    logger.info(f"CONFIRMATION : Le fichier {report_filepath} existe.")
                    if os.path.getsize(report_filepath) > 0:
                        logger.info(f"CONFIRMATION : Le fichier {report_filepath} n'est pas vide (taille: {os.path.getsize(report_filepath)} octets).")
                    else:
                        logger.error(f"ERREUR : Le fichier rapport {report_filepath} est vide !")
                else:
                    logger.error(f"ERREUR : Le fichier rapport {report_filepath} n'a pas été trouvé !")
            else:
                logger.warning("Aucun chemin de fichier de sauvegarde retourné dans les données du résultat.")
        else:
            logger.error(f"Résultat de la tâche : ÉCHEC")
            logger.error(f"Erreur : {result.error}")

    except Exception as e:
        logger.error(f"Erreur majeure lors de l'exécution de la tâche : {e}", exc_info=True)

    logger.info("Test de génération de rapport pour l'Agent 05 terminé.")

if __name__ == "__main__":
    asyncio.run(main()) 