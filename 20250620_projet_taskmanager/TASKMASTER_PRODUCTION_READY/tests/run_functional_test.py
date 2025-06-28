import asyncio
import sys
from pathlib import Path

# --- Configuration des chemins pour l'import ---

# Ce script est dans .../TASKMASTER_PRODUCTION_READY/tests
# L'agent est dans .../nextgeneration/agents
# Il faut remonter de 3 niveaux pour atteindre 'C:/Dev/nextgeneration'
try:
    # Chemin vers la racine du projet 'nextgeneration'
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except IndexError:
    # Fallback si la structure est inattendue
    PROJECT_ROOT = Path("C:/Dev/nextgeneration")

# Ajout de la racine du projet au sys.path pour que les imports
# relatifs à la racine dans l'agent fonctionnent correctement.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.taskmaster_agent import AgentTaskMasterNextGeneration

async def main():
    """
    Script de test fonctionnel pour l'AgentTaskMasterNextGeneration.
    Ce test valide le cycle de vie complet de l'agent :
    1. Démarrage (startup)
    2. Création d'une tâche simple
    3. Arrêt (shutdown)
    """
    print("🚀 Démarrage du test fonctionnel pour TaskMaster...")

    # Instanciation de l'agent
    # On peut passer un ID custom pour facilement retrouver les logs/rapports
    agent_id = "test_run_001"
    taskmaster = AgentTaskMasterNextGeneration(agent_id=agent_id)

    # Démarrage
    print("\\n1. Démarrage de l'agent...")
    startup_result = await taskmaster.startup()
    print(f"✅ Agent démarré : {startup_result}")
    assert startup_result["status"] == "started"

    # Création d'une tâche
    print("\\n2. Création d'une tâche en langage naturel...")
    user_request = "Refactorise le module principal pour utiliser le nouveau pattern."
    task_result = await taskmaster.create_task_from_natural_language(
        user_request=user_request,
        user_id="test_user"
    )
    print(f"✅ Tâche créée : {task_result}")
    assert task_result["status"] == "accepted"

    # Laisser le temps à la tâche de s'exécuter (elle est asynchrone)
    # Dans la version actuelle, l'exécution est simulée et très rapide.
    # On ajoute une petite attente pour s'assurer que le rapport est écrit.
    print("\\n⏳ Attente de la complétion de la tâche (simulée)...")
    await asyncio.sleep(5) 

    # Arrêt
    print("\\n3. Arrêt de l'agent...")
    shutdown_result = await taskmaster.shutdown()
    print(f"✅ Agent arrêté : {shutdown_result}")
    assert shutdown_result["status"] == "shutdown"

    print("\\n---")
    print("🎉 Test fonctionnel terminé avec succès!")
    print("Veuillez vérifier les répertoires suivants dans 'TASKMASTER_PRODUCTION_READY':")
    work_dir = PROJECT_ROOT / "20250620_projet_taskmanager" / "TASKMASTER_PRODUCTION_READY"
    print(f"  - {work_dir / 'logs' / 'agents' / f'taskmaster_{agent_id}'}")
    print(f"  - {work_dir / 'reports' / f'taskmaster_{agent_id}'}")
    print("---")


if __name__ == "__main__":
    # Correction pour Windows "Event loop is closed"
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main()) 