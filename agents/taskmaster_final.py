import os
import sys
import logging
from pathlib import Path
import asyncio
import importlib
import inspect

class TaskMasterFinal:
    """
    Agent orchestrateur final, conçu pour être robuste, autonome et
    opérer depuis le répertoire /agents.
    """
    def __init__(self, agent_id="taskmaster_final_001"):
        self.agent_id = agent_id
        
        # 1. Gestion stratégique des chemins
        self.project_root = Path(__file__).resolve().parent.parent
        self.work_dir = Path(os.getenv("TASKMASTER_WORK_DIR", self.project_root / "20250620_projet_taskmanager/TASKMASTER_PRODUCTION_READY"))
        
        # Assurer que le project_root est dans le path pour les imports
        if str(self.project_root) not in sys.path:
            sys.path.append(str(self.project_root))

        # 2. Configuration du logger
        self.log_dir = self.work_dir / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "taskmaster_final.log"
        
        self.logger = logging.getLogger(self.agent_id)
        self.logger.setLevel(logging.INFO)
        
        # Évite les double-logs si déjà configuré ailleurs
        if not self.logger.handlers:
            file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

        self.logger.info(f"Agent {self.agent_id} initialisé.")
        self.logger.info(f"PROJECT_ROOT: {self.project_root}")
        self.logger.info(f"WORK_DIR: {self.work_dir}")

        self.agents = {}

    async def startup(self):
        """Démarre l'agent et découvre les capacités des autres agents."""
        self.logger.info("TaskMasterFinal en cours de démarrage...")
        await self._discover_agents()
        self.logger.info(f"Agents découverts avec succès: {list(self.agents.keys())}")
        self.logger.info("TaskMasterFinal démarré et opérationnel.")

    async def _discover_agents(self):
        """Scanne le répertoire des agents, les importe dynamiquement et stocke leurs capacités."""
        agents_dir = self.project_root / "agents"
        self.logger.info(f"Début de la découverte des agents dans : {agents_dir}")
        
        for file_path in agents_dir.glob("agent_*.py"):
            agent_name = file_path.stem
            if agent_name == "taskmaster_final":
                continue

            try:
                module_spec = importlib.util.spec_from_file_location(agent_name, file_path)
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)

                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if name.startswith("Agent") and hasattr(obj, "CAPABILITIES"):
                        capabilities = getattr(obj, "CAPABILITIES", [])
                        if capabilities:
                            self.agents[agent_name] = {
                                "class": obj,
                                "capabilities": capabilities,
                                "module_path": file_path
                            }
                            self.logger.info(f"  -> Agent trouvé : {agent_name} avec les capacités : {capabilities}")
                            break # On prend la première classe d'agent trouvée dans le fichier
            
            except Exception as e:
                self.logger.warning(f"Impossible de charger l'agent {agent_name}. Erreur : {e}")
        
        if not self.agents:
            self.logger.error("Aucun agent fonctionnel avec des capacités n'a été trouvé.")

    async def execute_mission(self, natural_language_prompt: str):
        """
        Analyse un prompt, sélectionne le meilleur agent et lui délègue la tâche.
        """
        self.logger.info(f"Nouvelle mission reçue : '{natural_language_prompt}'")
        selected_agent = None
        prompt_words = set(natural_language_prompt.lower().split())

        # Stratégie de sélection améliorée par mot-clé
        for agent_name, agent_data in self.agents.items():
            for capability in agent_data["capabilities"]:
                # On vérifie si un des mots de la capacité est dans le prompt
                capability_words = set(capability.split('_'))
                if not capability_words.isdisjoint(prompt_words):
                    selected_agent = agent_data
                    self.logger.info(f"Agent sélectionné : {agent_name} basé sur la capacité '{capability}'")
                    break
            if selected_agent:
                break
        
        if not selected_agent:
            self.logger.error("Aucun agent approprié trouvé pour cette mission.")
            return {"status": "error", "message": "No suitable agent found."}

        # Délégation de la tâche
        try:
            agent_class = selected_agent["class"]
            agent_instance = agent_class()
            
            # Standardisation : on suppose que chaque agent a une méthode `run`
            if hasattr(agent_instance, "run"):
                self.logger.info(f"Exécution de la méthode 'run' de l'agent {agent_instance.name}...")
                # Note: pour l'instant, on suppose une méthode 'run' synchrone.
                # Une amélioration future serait de gérer sync/async.
                result = agent_instance.run(task_prompt=natural_language_prompt)
                self.logger.info(f"Mission terminée par {agent_instance.name}. Résultat : {result}")
                return result
            else:
                self.logger.error(f"L'agent {agent_instance.name} n'a pas de méthode 'run'.")
                return {"status": "error", "message": f"Agent {agent_instance.name} has no run method."}

        except Exception as e:
            self.logger.critical(f"Une erreur critique est survenue lors de l'exécution de la mission par l'agent : {e}", exc_info=True)
            return {"status": "critical_error", "message": str(e)}
        
        finally:
            # Assurer que l'agent est arrêté proprement pour libérer les ressources (logs, etc.)
            if 'agent_instance' in locals() and hasattr(agent_instance, "shutdown"):
                self.logger.info(f"Arrêt de l'instance de l'agent {agent_instance.name}...")
                agent_instance.shutdown()

    async def shutdown(self):
        """Arrête l'agent proprement."""
        self.logger.info("TaskMasterFinal en cours d'arrêt...")
        # Des opérations de nettoyage pourront être ajoutées ici
        await asyncio.sleep(0.1) # Simule une tâche d'arrêt asynchrone
        self.logger.info("TaskMasterFinal arrêté.")

if __name__ == '__main__':
    # Exemple d'utilisation pour un test rapide
    async def run_test():
        taskmaster = TaskMasterFinal()
        await taskmaster.startup()
        
        # Test de mission
        print("-" * 50)
        await taskmaster.execute_mission("Peux-tu me faire une revue de code (code_review) ?")
        print("-" * 50)
        await taskmaster.execute_mission("J'ai besoin de créer un workspace pour mon projet.")
        print("-" * 50)
        
        await taskmaster.shutdown()

    asyncio.run(run_test()) 