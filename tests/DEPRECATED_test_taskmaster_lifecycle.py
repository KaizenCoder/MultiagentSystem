import asyncio
import sys
from pathlib import Path

# S'assurer que le répertoire racine du projet est dans le sys.path
# pour que les imports comme "agents.taskmaster_agent" fonctionnent.
try:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except IndexError:
    print("Impossible de déterminer le répertoire racine du projet.")
    sys.exit(1)

from agents.taskmaster_agent import AgentTaskMasterNextGeneration

async def run_test():
    """
    Exécute un test fonctionnel complet du cycle de vie de l'AgentTaskMasterNextGeneration.
    """
    print("--- Début du test de cycle de vie de TaskMaster ---")
    
    # 1. Instanciation de l'agent
    print("1. Instanciation de l'agent TaskMaster...")
    try:
        taskmaster = AgentTaskMasterNextGeneration(agent_id="test_lifecycle_001")
        print("   ✅ Agent instancié avec succès.")
    except Exception as e:
        print(f"   ❌ Erreur lors de l'instanciation: {e}")
        return False

    # 2. Démarrage de l'agent
    print("\n2. Démarrage de l'agent...")
    try:
        startup_result = await taskmaster.startup()
        assert startup_result["status"] == "started"
        print("   ✅ Agent démarré avec succès.")
        print(f"   Agents disponibles découverts: {startup_result['available_agents']}")
    except Exception as e:
        print(f"   ❌ Erreur lors du démarrage: {e}")
        await taskmaster.shutdown() # Tentative d'arrêt propre
        return False

    # 3. Création d'une tâche de refactoring
    print("\n3. Création d'une tâche de refactoring...")
    test_request = "Refactorise le module authentification pour améliorer la clarté"
    try:
        task_result = await taskmaster.create_task_from_natural_language(user_request=test_request)
        print(f"   Résultat de la création de tâche: {task_result}")
        
        if task_result.get("status") == "rejected":
            print(f"   ❌ Tâche rejetée: {task_result.get('reason')}")
            # C'est un échec pour ce test, même si c'est un comportement attendu dans certains cas.
            # On continue jusqu'au shutdown.
            pass
        elif task_result.get("status") == "accepted":
             print("   ✅ Tâche acceptée pour traitement.")
        else:
            raise ValueError(f"Statut de tâche inattendu: {task_result.get('status')}")

    except Exception as e:
        print(f"   ❌ Erreur lors de la création de la tâche: {e}")
        await taskmaster.shutdown()
        return False

    # Attendre un peu pour que la tâche puisse s'exécuter (simulation)
    print("\n4. Attente de la simulation d'exécution de la tâche...")
    await asyncio.sleep(5) # Donne le temps à la tâche de s'exécuter en arrière-plan
    print("   Attente terminée.")

    # 5. Arrêt de l'agent
    print("\n5. Arrêt de l'agent...")
    try:
        shutdown_result = await taskmaster.shutdown()
        assert shutdown_result["status"] == "shutdown"
        print("   ✅ Agent arrêté proprement.")
    except Exception as e:
        print(f"   ❌ Erreur lors de l'arrêt: {e}")
        return False
        
    # Vérification finale
    print("\n--- Vérification finale ---")
    if task_result.get("status") == "accepted":
        print("✅ Le cycle de vie complet (instanciation, démarrage, création de tâche, arrêt) a réussi.")
        return True
    else:
        print("❌ Le test a échoué car la tâche a été rejetée.")
        print("   Cela peut être dû à des agents/capacités manquants.")
        return False


if __name__ == "__main__":
    # Exécution du test
    success = asyncio.run(run_test())
    
    print("\n--- Résultat du test ---")
    if success:
        print("🎉 TEST PASSÉ AVEC SUCCÈS")
        sys.exit(0)
    else:
        print("🔥 TEST ÉCHOUÉ")
        sys.exit(1) 