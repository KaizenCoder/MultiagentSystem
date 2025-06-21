from agent_factory_implementation.core.agent_factory_architecture import Agent, Task, Result
import asyncio
import tempfile
import importlib.util
import os
import sys

class AgentMAINTENANCE04TesteurAntiFauxAgents(Agent):
    """
    Agent chargé de tester dynamiquement le code pour s'assurer qu'il ne s'agit pas
    d'un "faux agent" (par exemple, un script qui ne fait rien ou qui échoue immédiatement).
    Il exécute une méthode de test standard (`execute_task`).
    """
    def __init__(self, agent_id="agent_MAINTENANCE_04_testeur_anti_faux_agents", version="1.0", description="Teste dynamiquement le code contre les faux agents.", status="enabled"):
        super().__init__(agent_id, version, description, "tester", status)

    async def startup(self):
        await super().startup()
        self.log("Testeur anti-faux agents prêt.")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "test_code":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni.")

        self.log(f"Test dynamique du fichier : {file_path}")

        tmp_path = None
        try:
            # Utiliser un fichier temporaire pour charger le module
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
                tmp.write(code)
                tmp_path = tmp.name

            module_name = os.path.basename(tmp_path).replace('.py', '')
            
            # Ajouter le répertoire temporaire au path
            temp_dir = os.path.dirname(tmp_path)
            if temp_dir not in sys.path:
                sys.path.insert(0, temp_dir)
            
            try:
                spec = importlib.util.spec_from_file_location(module_name, tmp_path)
                if spec is None or spec.loader is None:
                    return Result(success=False, error="Impossible de créer la spécification du module.")
                
                agent_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(agent_module)
                
                # Trouver la classe de l'agent dans le module
                agent_class = None
                for name, obj in agent_module.__dict__.items():
                    if (isinstance(obj, type) and 
                        hasattr(obj, '__bases__') and 
                        any('Agent' in str(base) for base in obj.__mro__) and 
                        obj.__name__ != 'Agent'):
                        agent_class = obj
                        break
                
                if not agent_class:
                    return Result(success=False, error="Aucune classe Agent trouvée dans le code.")

                # Instancier et tester l'agent
                self.log(f"Instanciation de la classe {agent_class.__name__} pour test.")
                
                # Test d'instanciation
                try:
                    instance = agent_class()
                except Exception as e:
                    return Result(success=False, error=f"Erreur lors de l'instanciation: {e}")
                
                # Test 1: La méthode startup fonctionne-t-elle ?
                try:
                    await instance.startup()
                except Exception as e:
                    self.log(f"Avertissement: startup() a échoué: {e}", level="warning")

                # Test 2: La méthode execute_task répond-elle correctement à une tâche invalide ?
                dummy_task = Task(type="dummy_task_for_testing", params={})
                try:
                    test_result = await instance.execute_task(dummy_task)
                    
                    # L'agent devrait rejeter une tâche invalide
                    if test_result.success:
                        return Result(success=False, error="L'agent n'a pas rejeté une tâche invalide comme attendu.")
                    
                    # Vérifier que le message d'erreur est approprié
                    error_msg = test_result.error.lower() if test_result.error else ""
                    if "non supporté" not in error_msg and "unsupported" not in error_msg and "not supported" not in error_msg:
                        self.log(f"Message d'erreur inattendu mais acceptable: {test_result.error}", level="warning")

                    self.log(f"Test dynamique réussi pour {file_path}.")
                    return Result(success=True, data={
                        "test_status": "passed", 
                        "class_found": agent_class.__name__,
                        "startup_test": "completed",
                        "invalid_task_rejection": "passed"
                    })
                    
                except Exception as e:
                    return Result(success=False, error=f"Erreur lors du test execute_task: {e}")
            
            finally:
                # Nettoyer le path
                if temp_dir in sys.path:
                    sys.path.remove(temp_dir)

        except Exception as e:
            self.log(f"Échec du test dynamique pour {file_path}: {e}", level="error")
            return Result(success=False, error=f"Test execution failed: {e}")
        
        finally:
            # Nettoyer le fichier temporaire
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception as e:
                    self.log(f"Impossible de supprimer le fichier temporaire {tmp_path}: {e}", level="warning")