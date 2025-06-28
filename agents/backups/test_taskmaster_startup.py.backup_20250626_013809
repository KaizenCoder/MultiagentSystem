import asyncio
import sys
from pathlib import Path

# Ce script s'attend à être exécuté depuis la racine du projet.
# Il ajoute le répertoire des agents au path pour trouver le module.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from taskmaster_agent import AgentTaskMasterNextGeneration

async def main():
    print('--- Début du test de démarrage de l''agent TaskMaster ---')
    try:
        taskmaster = AgentTaskMasterNextGeneration(agent_id="test_startup_01")
        print('[+] Instanciation réussie.')
        startup_result = await taskmaster.startup()
        print(f'[✔] Démarrage réussi. Résultat: {startup_result}')
    except Exception as e:
        print(f'[✖] Erreur: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
