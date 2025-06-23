#!/usr/bin/env python3
"""
Lanceur de Test pour le Workflow de Maintenance d'Agents

Ce script initialise le chef d'équipe de maintenance et lui assigne
une mission ciblée sur un sous-ensemble d'agents spécifiques.
"""

import asyncio
import sys
import json
from pathlib import Path

# Assurer que le répertoire racine du projet est dans le chemin
try:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_MAINTENANCE_00_chef_equipe_coordinateur

async def main():
    """
    Point d'entrée principal pour le test du workflow de maintenance.
    """
    print("🚀 Démarrage du test de workflow de maintenance ciblé")
    print("="*60)

    # Définir les agents cibles pour ce test
    target_agents = [
        "agents/agent_01_coordinateur_principal.py",
        "agents/agent_02_architecte_code_expert.py",
        "agents/agent_03_specialiste_configuration.py"
    ]

    print(f"🎯 Agents ciblés pour la maintenance : {len(target_agents)}")
    for agent_path in target_agents:
        print(f"  - {agent_path}")
    print("-" * 60)

    try:
        # Instancier le chef d'équipe
        # Le target_path est requis mais ne sera pas utilisé car nous spécifions les fichiers
        chef_equipe = create_agent_MAINTENANCE_00_chef_equipe_coordinateur(
            target_path="agents", 
            workspace_path="."
        )
        await chef_equipe.startup()

        # Définir et lancer la mission de maintenance complète
        mission_config = {
            "target_files": target_agents
        }
        
        print("\n🔧 Lancement du workflow de maintenance complet...")
        rapport_final = await chef_equipe.workflow_maintenance_complete(mission_config)

        # Sauvegarder le rapport final
        report_path = Path("reports") / "maintenance_workflow_test_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(rapport_final, f, indent=2, ensure_ascii=False, default=str)

        print("\n🏁 Workflow terminé.")
        print("="*60)
        print(f"📊 Statut final de la mission : {rapport_final.get('statut_mission')}")
        print(f"📄 Rapport complet sauvegardé dans : {report_path}")

        if rapport_final.get("statut_mission") == "ÉCHEC":
            print(f"❌ Erreur rencontrée : {rapport_final.get('erreur')}")
            return 1

    except Exception as e:
        print(f"❌ Une erreur critique est survenue dans le lanceur de test : {e}")
        return 1
    finally:
        if 'chef_equipe' in locals() and chef_equipe:
            await chef_equipe.shutdown()
    
    return 0

if __name__ == "__main__":
    # Utiliser asyncio.run() pour exécuter la coroutine main
    # sys.exit() attend un entier, pas une coroutine
    result_code = asyncio.run(main())
    sys.exit(result_code) 