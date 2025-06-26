# tests/test_agent_06_report_generation.py
import asyncio
import logging
import os
import sys
from pathlib import Path

# Ajout du répertoire parent au path pour résoudre les imports locaux
sys.path.append(str(Path(__file__).resolve().parent.parent))

from agents.agent_06_specialiste_monitoring_sprint4 import Agent06AdvancedMonitoring
from core.agent_factory_architecture import Task

async def run_single_test(agent: Agent06AdvancedMonitoring, report_type: str, output_format: str, logger: logging.Logger):
    """Exécute un seul test pour un type de rapport et un format donnés."""
    logger.info(f"--- DÉBUT TEST: Type='{report_type}', Format='{output_format}' ---")
    
    task_params = {
        "cible": f"systeme_test_{report_type.lower()}",
        "objectifs_specifiques": [f"Générer rapport {report_type} en {output_format}"],
        "type_rapport": report_type,
        "format_sortie": output_format
    }
    report_task = Task(
        id=f"task_{report_type.lower()}_{output_format.lower()}", # ID de tâche plus descriptif
        type="generate_strategic_report",
        params=task_params
    )
    logger.info(f"Tâche créée : {report_task.id} pour Type='{report_type}', Format='{output_format}'.")

    try:
        logger.info(f"Exécution de la tâche {report_task.id}...")
        result = await agent.execute_task(report_task)
        logger.info(f"Tâche {report_task.id} exécutée.")

        if result.success:
            logger.info(f"Résultat Tâche {report_task.id} : SUCCÈS")
            
            if output_format == "markdown":
                report_filepath = result.data.get('fichier_sauvegarde')
                if report_filepath:
                    logger.info(f"Rapport Markdown devrait être sauvegardé ici : {report_filepath}")
                    if os.path.exists(report_filepath):
                        logger.info(f"CONFIRMATION : Le fichier {report_filepath} existe.")
                        if os.path.getsize(report_filepath) > 0:
                            logger.info(f"CONFIRMATION : Fichier {report_filepath} non vide (taille: {os.path.getsize(report_filepath)} octets).")
                        else:
                            logger.error(f"ERREUR : Fichier rapport {report_filepath} EST VIDE !")
                    else:
                        logger.error(f"ERREUR : Fichier rapport {report_filepath} INTROUVABLE !")
                else:
                    logger.error("ERREUR : Aucun chemin de fichier de sauvegarde retourné pour rapport Markdown.")
            elif output_format == "json":
                # Pour JSON, nous vérifions si les données du rapport sont présentes
                if result.data and isinstance(result.data, dict) and "agent_id" in result.data:
                    logger.info(f"CONFIRMATION : Rapport JSON reçu avec agent_id: {result.data.get('agent_id')}.")
                    # Vérifier d'autres clés essentielles si nécessaire
                    if result.data.get("type_rapport") == report_type:
                        logger.info(f"CONFIRMATION : Type de rapport JSON ({result.data.get('type_rapport')}) correspond au type demandé ({report_type}).")
                    else:
                        logger.error(f"ERREUR : Type de rapport JSON ({result.data.get('type_rapport')}) ne correspond pas au type demandé ({report_type}).")
                else:
                    logger.error("ERREUR : Données du rapport JSON absentes ou mal formées dans le résultat.")
        else:
            logger.error(f"Résultat Tâche {report_task.id} : ÉCHEC")
            logger.error(f"Erreur : {result.error}")

    except Exception as e:
        logger.error(f"Erreur majeure lors du test (Type='{report_type}', Format='{output_format}') : {e}", exc_info=True)
    finally:
        logger.info(f"--- FIN TEST: Type='{report_type}', Format='{output_format}' ---")

async def main():
    # Configuration du logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("Démarrage des tests de génération de rapport pour l'Agent 06...")

    # Instanciation de l'agent
    try:
        agent = Agent06AdvancedMonitoring(agent_id="test_agent_06_complet", version="1.0-test-suite")
        logger.info(f"Agent {agent.agent_id} v{agent.version} instancié.")
        
        # Test initial startup et health_check
        await agent.startup()
        logger.info("Agent startup() appelé.")
        health = await agent.health_check()
        logger.info(f"Health check: {health}")
        if not (health and health.get("status") == "ok"):
            logger.error("ERREUR : Health check a échoué ou statut invalide.")
            # return # On pourrait arrêter ici si le health check échoue
            
    except Exception as e:
        logger.error(f"Erreur lors de l'instanciation ou startup de l'agent : {e}", exc_info=True)
        return

    report_types = ["monitoring", "observabilite", "performance", "alertes"]
    output_formats = ["markdown", "json"]

    for r_type in report_types:
        for o_format in output_formats:
            await run_single_test(agent, r_type, o_format, logger)
            await asyncio.sleep(1) # Petite pause pour éviter de surcharger les logs ou I/O

    # Test final shutdown
    try:
        await agent.shutdown()
        logger.info(f"Agent {agent.agent_id} arrêté (shutdown() appelé).")
    except Exception as e:
        logger.error(f"Erreur lors de l'arrêt de l'agent : {e}", exc_info=True)

    logger.info("Tous les tests de génération de rapport pour l'Agent 06 sont terminés.")

if __name__ == "__main__":
    # Python 3.7+
    asyncio.run(main()) 