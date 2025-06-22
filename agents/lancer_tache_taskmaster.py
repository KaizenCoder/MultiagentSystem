import asyncio
import sys
from pathlib import Path

# Assurer que le répertoire des agents est dans le path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from taskmaster_agent import AgentTaskMasterNextGeneration

async def main():
    """
    Script pour soumettre une première tâche en langage naturel
    à l'agent TaskMaster.
    """
    print("--- Initialisation de l'agent TaskMaster ---")
    taskmaster = AgentTaskMasterNextGeneration(agent_id="prod_run_01")
    await taskmaster.startup()
    print("[✔] Agent TaskMaster prêt à recevoir des instructions.")
    print("-" * 50)

    requete_utilisateur = (
        "Je veux que tu réalises un audit de sécurité complet sur le module 'taskmaster_agent.py', "
        "que tu analyses sa performance et que tu génères ensuite un rapport de documentation au format Markdown."
    )

    print(f"▶️ Envoi de la requête : \"{requete_utilisateur}\"")

    try:
        resultat = await taskmaster.create_task_from_natural_language(
            user_request=requete_utilisateur,
            user_id="admin_user"
        )
        
        print("\n--- [✔] Tâche traitée avec succès ! ---")
        print("Résultat final retourné par l'agent :")
        print(resultat.get("human_summary", "Aucun résumé disponible."))

    except Exception as e:
        print(f"\n[✖] Une erreur est survenue lors de l'exécution de la tâche : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
