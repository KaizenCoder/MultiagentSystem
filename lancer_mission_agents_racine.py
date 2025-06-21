import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path

# --- Configuration Robuste du Chemin d'Importation ---
# Permet au script d'être exécuté de n'importe où et de trouver 'core'
try:
    # On remonte au dossier racine du projet 'nextgeneration'
    project_root = Path(__file__).resolve().parents[0] 
    core_path = project_root / "core"
    
    # Ajout du chemin vers le dossier contenant 'core'
    # Ajout du chemin racine du projet pour permettre les imports absolus depuis 'core'
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from core import logging_manager
    print("✅ logging_manager depuis 'core' à la racine importé avec succès.")

except ImportError as e:
    print(f"❌ Erreur critique d'importation du nouveau logging_manager: {e}")
    print("Le module 'core' est introuvable. Le refactoring a peut-être déplacé les fichiers.")
    print("Assurez-vous que le répertoire 'core' est à la racine du projet.")
    sys.exit(1)

# --- Imports des Agents de Maintenance ---
try:
    from agent_factory_implementation.agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_0_chef_equipe_coordinateur as create_chef_equipe
except ImportError as e:
    print(f"Erreur d'importation de l'agent: {e}")
    sys.exit(1)


async def lancer_mission_analyse_agents_racine():
    """
    Orchestre une mission de diagnostic pour l'ensemble des agents
    situés dans le répertoire '20250621_1527_agent_racine_repertoire'.
    """
    # Ajout de 'logger_name' dans la configuration personnalisée
    custom_conf = {
        "logger_name": "mission.analyse_racine",
        "metadata": {"mission_id": "analyse_agents_racine"}
    }
    main_logger = logging_manager.get_logger(config_name="orchestrator", custom_config=custom_conf)
    
    main_logger.info("="*50)
    main_logger.info("🚀 LANCEMENT MISSION: ANALYSE AGENTS RACINE (avec Golden Source Logger)")
    main_logger.info("="*50)

    mission_directory = "20250621_1527_agent_racine_repertoire"

    # --- Initialisation de l'équipe ---
    try:
        # On ne passe plus le logger directement, le chef d'équipe devra l'importer lui-même
        # C'est une étape intermédiaire, on corrigera l'agent chef d'équipe ensuite.
        chef_equipe = create_chef_equipe(target_path=mission_directory, workspace_path=".")
        main_logger.info("Équipe de maintenance initialisée avec succès.")
    except Exception as e:
        main_logger.critical(f"Impossible d'initialiser l'équipe de maintenance: {e}", exc_info=True)
        return

    # --- Définition et exécution de la mission ---
    mission_config = {
        "mission_description": f"Analyser l'intégralité des agents dans le dossier '{mission_directory}', vérifier leur conformité, et rapporter les problèmes de syntaxe, d'importations manquantes ou de non-respect des standards du projet.",
        "target_directory": mission_directory,
        "report_filename": f"rapport_mission_agents_racine_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    }
    
    main_logger.info(f"Lancement du workflow de maintenance...")
    
    # Le chef d'équipe gère l'ensemble du workflow
    rapport_final = await chef_equipe.workflow_maintenance_complete(mission_config)

    # --- Sauvegarde du rapport ---
    report_path = mission_config["report_filename"]
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(rapport_final, f, indent=4, ensure_ascii=False)
    
    main_logger.info(f"✅ MISSION TERMINÉE. Rapport sauvegardé dans : {report_path}")

if __name__ == "__main__":
    # Correction pour l'exécution asynchrone
    try:
        asyncio.run(lancer_mission_analyse_agents_racine())
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}") 



