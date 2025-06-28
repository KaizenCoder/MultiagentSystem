#!/usr/bin/env python3
"""
Test d'intégration pour lancer le workflow de maintenance complet
sur les agents principaux de l'équipe (01 à 05).

Ce script exécute la mission de l'équipe de maintenance sur une liste
spécifique d'agents qui ne sont pas des agents de maintenance eux-mêmes.
"""
import asyncio
import sys
from pathlib import Path
import json
import logging
from datetime import datetime

# Configuration du chemin pour les imports
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except IndexError:
    sys.path.insert(0, '.')

from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import ChefEquipeCoordinateurEnterprise
from core.agent_factory_architecture import Task, Result

# Configuration du logger pour ce script de test
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("test_main_agents_maintenance")

async def run_maintenance_on_main_agents():
    """
    Lance le workflow de maintenance sur les agents principaux 01 à 05.
    """
    logger.info("🚀 Démarrage du test de maintenance sur les agents principaux...")
    
    # Liste des agents principaux à soumettre au workflow de maintenance
    # On inclut tous les agents (01 à 05) pour un test complet.
    target_agent_paths = [
        "agents/agent_01_coordinateur_principal.py",
        "agents/agent_02_architecte_code_expert.py",
        "agents/agent_03_specialiste_configuration.py",
        "agents/agent_04_expert_securite_crypto.py",
        "agents/agent_05_maitre_tests_validation.py"
    ]
    
    # Vérification de l'existence des fichiers
    for agent_path in target_agent_paths:
        if not Path(agent_path).exists():
            logger.error(f"❌ Fichier agent manquant: {agent_path}")
            return
    
    logger.info(f"Agents cibles pour la maintenance : {len(target_agent_paths)} agents.")

    chef = None
    try:
        # Création du chef d'équipe de maintenance
        reports_dir = Path("reports/main_agents_maintenance")
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_path = reports_dir / f"main_agents_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        logger.info("Instanciation du Chef d'Équipe de Maintenance...")
        chef = ChefEquipeCoordinateurEnterprise(
            target_path=str(report_path),
            workspace_path="."
        )

        # Démarrage du chef et de son équipe
        logger.info("Démarrage du chef d'équipe et recrutement de l'équipe de maintenance...")
        await chef.startup()
        
        # Création de la tâche de maintenance
        logger.info("Création de la tâche de maintenance pour les agents cibles...")
        mission_task = Task(
            type="maintenance_complete",
            params={"target_files": target_agent_paths}
        )
        
        # Exécution du workflow
        logger.info("🚀 Lancement du workflow de maintenance complet...")
        result = await chef.execute_task(mission_task)
        
        logger.info("\n" + "="*80)
        logger.info("🏁 WORKFLOW DE MAINTENANCE TERMINÉ 🏁")
        
        if result.success:
            logger.info("✅ La mission s'est terminée avec succès.")
        else:
            logger.warning(f"⚠️ La mission s'est terminée, mais avec des erreurs: {result.error}")

        logger.info("\n--- RAPPORT FINAL DE LA MISSION ---")
        # Utilisation de json.dumps pour un affichage propre, gérant les objets non sérialisables
        report_data = result.data if result else {"error": "Aucun résultat retourné"}
        logger.info(json.dumps(report_data, indent=2, ensure_ascii=False, default=str))
        logger.info("---------------------------------")
        logger.info(f"Le rapport complet est disponible ici : {report_path}")
        logger.info(f"Et le rapport Markdown ici : {report_path.with_suffix('.md')}")

    except Exception as e:
        logger.error(f"❌ Une erreur critique est survenue durant le test : {e}", exc_info=True)
    finally:
        if chef:
            logger.info("Arrêt du chef d'équipe...")
            await chef.shutdown()

if __name__ == "__main__":
    asyncio.run(run_maintenance_on_main_agents()) 