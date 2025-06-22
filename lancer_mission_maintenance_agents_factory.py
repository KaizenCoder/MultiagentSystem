import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path

# --- Configuration Robuste du Chemin d'Importation ---
try:
    # On remonte au dossier racine du projet 'nextgeneration'
    project_root = Path(__file__).resolve().parents[0]
    # Ajout du chemin racine du projet pour permettre les imports absolus depuis 'core'
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from core import logging_manager
    print("✅ logging_manager depuis 'core' à la racine importé avec succès.")
    from core.agent_factory_architecture import Task, Result

except ImportError as e:
    print(f"❌ Erreur critique d'importation: {e}")
    print("Assurez-vous que 'core' et 'agent_factory_implementation/core' sont accessibles.")
    print("Le module 'core' est introuvable. Le refactoring a peut-être déplacé les fichiers.")
    print("Assurez-vous que le répertoire 'core' est à la racine du projet.")
    sys.exit(1)

# --- Imports des Agents de Maintenance ---
try:
    from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_MAINTENANCE_00_chef_equipe_coordinateur as create_chef_equipe
    print("✅ Import de l'agent chef d'équipe réussi.")
except ImportError as e:
    print(f"❌ Erreur d'importation de l'agent chef d'équipe: {e}")
    print("Vérification des chemins d'import...")
    
    # Diagnostic des chemins
    agents_path = project_root / 'agent_factory_implementation' / 'agents'
    print(f"Chemin des agents : {agents_path}")
    print(f"Existe : {agents_path.exists()}")
    
    if agents_path.exists():
        print("Fichiers dans le répertoire agents :")
        for file in agents_path.iterdir():
            if file.is_file() and file.suffix == '.py':
                print(f"  - {file.name}")
    
    # Tentative de résolution du chemin si l'import échoue
    try:
        sys.path.insert(0, str(agents_path))
        from agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_MAINTENANCE_00_chef_equipe_coordinateur as create_chef_equipe
        print("✅ Import de l'agent chef d'équipe réussi après ajustement du path.")
    except ImportError as e2:
        print(f"❌ Échec final de l'importation de l'agent chef d'équipe: {e2}")
        print("Veuillez vérifier que tous les fichiers d'agents sont présents et syntaxiquement corrects.")
        sys.exit(1)


async def lancer_mission_maintenance():
    """
    Orchestre une mission de maintenance pour l'ensemble des agents
    situés dans le répertoire 'agent_factory_implementation/agents'.
    """
    custom_conf = {
        "logger_name": "mission.maintenance_factory",
        "metadata": {"mission_id": "maintenance_agents_factory"}
    }
    
    try:
        main_logger = logging_manager.get_logger(config_name="orchestrator", custom_config=custom_conf)
    except Exception as e:
        print(f"Erreur lors de l'initialisation du logger: {e}")
        print("Poursuite sans logger personnalisé...")
        # Logger de secours
        import logging
        main_logger = logging.getLogger("mission.maintenance_factory")
        main_logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        main_logger.addHandler(handler)

    main_logger.info("="*50)
    main_logger.info("🚀 LANCEMENT MISSION: MAINTENANCE AGENTS FACTORY")
    main_logger.info("="*50)

    mission_directory = "agent_factory_implementation/agents"
    main_logger.info(f"Répertoire cible : {mission_directory}")

    # Vérification de l'existence du répertoire cible
    if not os.path.exists(mission_directory):
        main_logger.critical(f"Le répertoire cible n'existe pas : {mission_directory}")
        print(f"❌ Erreur : Le répertoire {mission_directory} n'existe pas.")
        return

    # --- Initialisation de l'équipe ---
    try:
        chef_equipe = create_chef_equipe(target_path=mission_directory, workspace_path=".")
        main_logger.info("Équipe de maintenance initialisée avec succès.")
        print("✅ Équipe de maintenance initialisée.")
    except Exception as e:
        main_logger.critical(f"Impossible d'initialiser l'équipe de maintenance: {e}", exc_info=True)
        print(f"❌ Erreur lors de l'initialisation de l'équipe : {e}")
        return

    # --- Définition et exécution de la mission ---
    main_logger.info(f"Lancement du workflow de maintenance via execute_task...")
    print("🔄 Démarrage du workflow de maintenance...")

    # Création de la tâche conforme au Pattern Factory
    mission_task = Task(
        type="maintenance_complete",
        params={
            "description": f"Effectuer une maintenance complète sur tous les agents du répertoire '{mission_directory}'.",
            "target_directory": mission_directory,
            "report_filename": f"rapport_maintenance_agents_factory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        }
    )

    # Le chef d'équipe exécute la tâche
    try:
        result: Result = await chef_equipe.execute_task(mission_task)
    except Exception as e:
        main_logger.critical(f"Erreur lors de l'exécution de la mission: {e}", exc_info=True)
        print(f"❌ Erreur lors de l'exécution : {e}")
        return

    # --- Sauvegarde du rapport ---
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if result.success:
        report_data = result.data
        report_path = f"rapport_maintenance_SUCCESS_{timestamp}.json"
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=4, ensure_ascii=False)
            main_logger.info(f"✅ MISSION TERMINÉE AVEC SUCCÈS. Rapport sauvegardé dans : {report_path}")
            print(f"\n✅ Mission de maintenance terminée avec succès!")
            print(f"📄 Rapport détaillé : {report_path}")
        except Exception as e:
            main_logger.error(f"Erreur lors de la sauvegarde du rapport de succès: {e}")
            print(f"⚠️  Mission réussie mais erreur de sauvegarde du rapport : {e}")
    else:
        report_path = f"rapport_maintenance_ECHEC_{timestamp}.json"
        error_data = {
            "error": result.error,
            "timestamp": timestamp,
            "mission_directory": mission_directory,
            "additional_data": result.data
        }
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(error_data, f, indent=4, ensure_ascii=False)
            main_logger.error(f"❌ MISSION ÉCHOUÉE. Rapport d'erreur sauvegardé dans : {report_path}")
            main_logger.error(f"   Erreur: {result.error}")
            print(f"\n❌ Mission de maintenance échouée.")
            print(f"📄 Rapport d'erreur : {report_path}")
            print(f"🔍 Erreur : {result.error}")
        except Exception as e:
            main_logger.critical(f"Erreur lors de la sauvegarde du rapport d'échec: {e}")
            print(f"❌ Mission échouée ET erreur de sauvegarde : {e}")


def main():
    """Point d'entrée principal avec gestion d'erreur robuste."""
    try:
        asyncio.run(lancer_mission_maintenance())
    except KeyboardInterrupt:
        print("\n⏹️  Mission interrompue par l'utilisateur.")
    except Exception as e:
        print(f"\n💥 Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        print("\n🔧 Suggestions de débogage :")
        print("1. Vérifiez que tous les modules requis sont installés")
        print("2. Vérifiez la structure des répertoires 'core' et 'agent_factory_implementation'")
        print("3. Vérifiez les permissions d'écriture dans le répertoire courant")


if __name__ == "__main__":
    main() 

