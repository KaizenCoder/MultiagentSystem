#!/usr/bin/env python3
"""
🧪 AGENT 4 - TESTEUR D'AGENTS ENTERPRISE (ANTI-FAUX-AGENTS)
===========================================================
Mission: Détecter les FAUX AGENTS (code SYNC) et valider la conformité.
"""

import sys
import ast
import inspect
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import importlib
import time
import re
import json
import asyncio
import tempfile
import importlib.util
import os
import uuid
from datetime import datetime

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core import logging_manager
from core.agent_factory_architecture import Agent, Task, Result

@dataclass
class FakeAgentDetection:
    """Résultat de détection d'un faux agent."""
    agent_id: str
    agent_name: str
    is_fake_agent: bool
    sync_violations: List[str]
    async_violations: List[str]
    pattern_factory_violations: List[str]
    compliance_score: float
    recommendation: str
    details: Dict[str, Any]

class AgentMAINTENANCE04TesteurAntiFauxAgents(Agent):
    """
    Agent spécialisé dans le test dynamique des agents pour s'assurer qu'ils ne sont pas des 'faux' agents.
    """

    def __init__(self, **kwargs):
        """Initialisation standardisée."""
        super().__init__(**kwargs)
        self.logger.info(f"Testeur anti-faux agents ({self.agent_id}) initialisé.")

    async def startup(self):
        """Démarrage de l'agent."""
        self.log("Testeur anti-faux agents prêt.")

    async def execute_task(self, task: Task) -> Result:
        """Exécute une tâche de test dynamique."""
        if task.type != "dynamic_test":
            return Result(success=False, error="Type de tâche non supporté.")

        file_path = task.params.get("file_path")
        code_content = task.params.get("code_content")

        if not file_path or not code_content:
            return Result(success=False, error="Chemin ou contenu du fichier manquant.")

        self.log(f"Test dynamique du fichier : {file_path}")
        
        test_passed, details_or_error = await self._run_dynamic_test(file_path, code_content)
        
        self.log(f"Test dynamique pour {file_path} terminé. Succès: {test_passed}")
        
        if test_passed:
            return Result(
                success=True,
                data={"file_path": file_path, "details": details_or_error}
            )
        else:
            return Result(
                success=False,
                error=details_or_error,
                data={"file_path": file_path}
            )

    async def _run_dynamic_test(self, file_path: str, code_content: str) -> (bool, str):
        """
        Tente de charger et d'instancier l'agent depuis le code fourni.
        C'est un test simple pour voir si le code est viable.
        """
        temp_file_path = None
        try:
            # Créer un fichier temporaire pour l'importation
            temp_dir = Path("./temp_test_agents")
            temp_dir.mkdir(exist_ok=True)
            temp_file_name = f"temp_{Path(file_path).stem}_{uuid.uuid4().hex}.py"
            temp_file_path = temp_dir / temp_file_name

            with open(temp_file_path, "w", encoding="utf-8") as f:
                f.write(code_content)

            # Charger le module dynamiquement
            module_name = temp_file_path.stem
            spec = importlib.util.spec_from_file_location(module_name, temp_file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                # Essayer de trouver et d'instancier une classe Agent
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and issubclass(obj, Agent) and obj is not Agent:
                        self.log(f"Instanciation de la classe {name} pour test.")
                        
                        # NOUVEAU: Introspection pour instanciation dynamique
                        try:
                            sig = inspect.signature(obj.__init__)
                            params = sig.parameters
                            
                            # Créer des arguments factices basés sur la signature
                            test_args = {}
                            for param_name, param in params.items():
                                if param_name == 'self':
                                    continue
                                # Si l'argument a une valeur par défaut, on ne le fournit pas
                                if param.default != inspect.Parameter.empty:
                                    continue
                                # Si ce sont des kwargs, on ne fournit rien
                                if param.kind == inspect.Parameter.VAR_KEYWORD:
                                    continue
                                
                                # Fournir des valeurs factices pour les types communs
                                if param.annotation == str:
                                    test_args[param_name] = f"test_{param_name}"
                                elif param.annotation == int:
                                    test_args[param_name] = 123
                                elif param.annotation == bool:
                                    test_args[param_name] = True
                                else:
                                    # Pour les autres, on tente un dict vide, ce qui est souvent
                                    # utilisé pour les configurations `**kwargs`
                                    pass # Ne rien faire et espérer que ce soit optionnel ou kwarg

                            self.log(f"Arguments d'instanciation déduits: {test_args}")
                            instance = obj(**test_args)

                        except TypeError as te:
                            # Fallback vers l'ancienne méthode si l'introspection échoue
                            self.log(f"L'instanciation dynamique a échoué ({te}), tentative avec des valeurs par défaut.", level="warning")
                            instance = obj(agent_id='test-agent', version='0.0.0', description='test', agent_type='test', status='testing')

                        if hasattr(instance, 'health_check') and asyncio.iscoroutinefunction(instance.health_check):
                            await instance.health_check()
                        return True, f"Agent {name} instancié et health_check réussi."
                
                return False, "Aucune classe héritant de 'Agent' n'a pu être trouvée et instanciée."
            else:
                return False, "Impossible de créer le spec du module."

        except Exception as e:
            return False, f"Échec du test dynamique: {e}"
        finally:
            # Nettoyer le fichier temporaire
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)


    def get_capabilities(self) -> List[str]:
        return ["dynamic_test"]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy"}

    async def shutdown(self):
        """Arrêt de l'agent."""
        self.log("Testeur anti-faux agents éteint.")
        
    async def run_test(self, file_path: str, code_content: str) -> Result:
        """Méthode de compatibilité pour l'ancien appel."""
        self.log(f"Appel de compatibilité 'run_test' pour {file_path}", level="warning")
        test_task = Task(type="dynamic_test", params={"file_path": file_path, "code_content": code_content})
        return await self.execute_task(test_task)


def create_agent_MAINTENANCE_04_testeur_anti_faux_agents(**config) -> AgentMAINTENANCE04TesteurAntiFauxAgents:
    """Factory pour créer une instance de l'Agent 4."""
    return AgentMAINTENANCE04TesteurAntiFauxAgents(**config)

if __name__ == '__main__':
    async def main_test():
        agent = create_agent_MAINTENANCE_04_testeur_anti_faux_agents()
        await agent.startup()
        
        # Test avec un code qui devrait fonctionner
        good_code = """
from core.agent_factory_architecture import Agent, Task, Result
class GoodAgent(Agent):
    def __init__(self, **kwargs): super().__init__(**kwargs)
    async def execute_task(self, task: Task) -> Result: return Result(success=True)
    def get_capabilities(self) -> list: return []
    async def startup(self): pass
    async def shutdown(self): pass
    async def health_check(self) -> dict: return {"status": "ok"}
"""
        results = await agent.run_test("good_agent.py", good_code)
        print("--- Test Agent Valide ---")
        print(json.dumps(results.to_dict(), indent=2))
        
        # Test avec un code qui devrait échouer
        bad_code = "class BadAgent: pass"
        results = await agent.run_test("bad_agent.py", bad_code)
        print("\n--- Test Agent Invalide ---")
        print(json.dumps(results.to_dict(), indent=2))
        
        await agent.shutdown()

    asyncio.run(main_test())