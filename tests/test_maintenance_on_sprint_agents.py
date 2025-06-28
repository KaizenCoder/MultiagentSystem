#!/usr/bin/env python3
"""
Test dédié au lancement du workflow de maintenance sur les agents clés du Sprint.
"""
import asyncio
import logging
import sys
from pathlib import Path
import json
from datetime import datetime

# Configuration du chemin pour les imports
try:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import ChefEquipeCoordinateurEnterprise
from core import logging_manager

# Configuration du logging pour le test
log = logging_manager.get_logger(
    config_name="test_runner", 
    custom_config={"logger_name": "TestSprintMaintenance"}
)

async def run_sprint_maintenance_workflow():
    """
    Exécute le workflow de maintenance sur une sélection d'agents de sprint.
    """
    log.info("🚀 Démarrage du test de maintenance sur les agents du Sprint...")

    # Liste des agents cibles pour cette exécution
    target_agents = [
        "agents/agent_01_coordinateur_principal.py",
        "agents/agent_02_architecte_code_expert.py",
        "agents/agent_03_specialiste_configuration.py",
        "agents/agent_04_expert_securite_crypto.py",
        "agents/agent_05_maitre_tests_validation.py"
    ]
    
    log.info(f"Agents cibles : {target_agents}")

    # Initialisation du chef d'équipe
    reports_dir = project_root / "reports" / "sprint_agents_reports_final"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_file_name = f"maintenance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    chef_equipe = ChefEquipeCoordinateurEnterprise(
        target_path=str(reports_dir / report_file_name)
    )

    try:
        # Démarrage de l'agent (charge la config, etc.)
        await chef_equipe.startup()

        # Exécution du workflow principal
        mission_config = {
            "target_files": target_agents
        }
        report_data = await chef_equipe.workflow_maintenance_complete(
            mission_config=mission_config
        )

        if report_data:
            report_path = report_data.get("rapport_path")
            log.info(f"✅ Workflow de maintenance terminé. Rapport disponible : {report_path}")
            
            # Afficher le contenu du rapport final
            print("--- RAPPORT FINAL ---")
            print(json.dumps(report_data, indent=2, ensure_ascii=False))
            print("---------------------")

        else:
            log.error("❌ Le workflow de maintenance n'a pas retourné de rapport.")

    except Exception as e:
        log.critical(f"❌ Erreur critique durant le workflow de maintenance : {e}", exc_info=True)
    finally:
        # Arrêt propre de l'agent
        await chef_equipe.shutdown()
        log.info("🏁 Test de maintenance terminé.")

if __name__ == "__main__":
    asyncio.run(run_sprint_maintenance_workflow()) 