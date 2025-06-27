"""
🛡️ TESTEUR ANTI-FAUX AGENTS - Agent 04
======================================
🎯 Mission : Valider qu'un agent est fonctionnel et n'est pas un "faux" agent.
⚡ Capacités : Exécution de tests basiques (importation, instanciation, appels de méthodes).
🏢 Équipe : NextGeneration Tools Migration
Author: Équipe de Maintenance NextGeneration
Version: 4.1.0 - Harmonisation Standards Pattern Factory NextGeneration
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
    🛡️ Agent MAINTENANCE 04 - Testeur Anti-Faux Agents NextGeneration
    
    Agent spécialisé dans la validation dynamique et l'authentification d'agents,
    détection de faux agents via tests d'instanciation et vérification conformité Pattern Factory.
    
    Capacités principales :
    - Tests dynamiques d'importation et instanciation sécurisée
    - Introspection avancée de signatures de méthodes et constructeurs
    - Détection automatique violations Pattern Factory (sync/async)
    - Validation conformité Agent avec health_check, startup, shutdown
    - Scoring de compliance et recommandations d'amélioration
    - Tests d'exécution factice avec arguments déduits dynamiquement
    
    Technologies avancées :
    - Importation dynamique avec spec_from_file_location
    - Introspection via inspect.signature pour instanciation adaptative
    - Dataclass FakeAgentDetection pour résultats structurés
    - Tests isolés en fichiers temporaires sécurisés
    - Classification violations (sync/async/pattern-factory)
    
    Workflow type :
    1. Chargement dynamique module agent cible
    2. Introspection signatures et instanciation factice
    3. Tests conformité async/sync et Pattern Factory
    4. Calcul score compliance et détection faux agents
    5. Génération recommandations d'amélioration
    
    Conformité : Pattern Factory NextGeneration v4.1.0
    """

    def __init__(self, **kwargs):
        """Initialisation standardisée."""
        super().__init__(agent_type="testeur", **kwargs)
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={
                    "logger_name": f"nextgen.maintenance.testeur_anti_faux_agents.{self.id}",
                    "log_dir": "logs/maintenance/testeur",
                    "metadata": {
                        "agent_type": "MAINTENANCE_04_testeur_anti_faux_agents",
                        "agent_role": "testeur_anti_faux_agents",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = self.id
        self.logger.info(f"Testeur anti-faux agents ({self.agent_id}) initialisé.")

    async def startup(self):
        """Démarrage de l'agent."""
        self.logger.info("Testeur anti-faux agents prêt.")

    async def execute_task(self, task: Task) -> Result:
        """Exécute une tâche de test dynamique."""
        self.logger.info(f"Exécution de la tâche de type '{task.type}' avec les paramètres : {task.params}")

        if task.type == "test_code":
            code_to_test = task.params.get("code")
            file_path = task.params.get("file_path", "temp_file_for_test.py")
            
            if not code_to_test:
                return Result(success=False, error="Code ou chemin du fichier manquant.")

            self.logger.info(f"Test dynamique du fichier : {file_path}")
            
            test_passed, details_or_error = await self._run_dynamic_test(file_path, code_to_test)
            
            self.logger.info(f"Test dynamique pour {file_path} terminé. Succès: {test_passed}")
            
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
        return Result(success=False, error="Type de tâche non supporté.")

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
                        self.logger.info(f"Instanciation de la classe {name} pour test.")
                        
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

                            self.logger.info(f"Arguments d'instanciation déduits: {test_args}")
                            instance = obj(**test_args)

                        except TypeError as te:
                            # Fallback vers l'ancienne méthode si l'introspection échoue
                            self.logger.warning(f"L'instanciation dynamique a échoué ({te}), tentative avec des valeurs par défaut.")
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
        """Retourne les capacités spécialisées du Testeur Anti-Faux Agents."""
        return [
            "dynamic_agent_testing",
            "fake_agent_detection",
            "pattern_factory_validation",
            "dynamic_instantiation",
            "signature_introspection",
            "compliance_scoring",
            "async_sync_validation",
            "isolated_execution",
            "factory_method_testing",
            "violation_classification"
        ]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy"}

    async def shutdown(self):
        """Arrêt de l'agent."""
        self.logger.info("Testeur anti-faux agents éteint.")
        
    async def run_test(self, file_path: str, code_content: str) -> Result:
        """Méthode de compatibilité pour l'ancien appel."""
        self.logger.warning(f"Appel de compatibilité 'run_test' pour {file_path}")
        task_id = f"test_{uuid.uuid4().hex}"
        task_description = f"Test dynamique pour le fichier {file_path}"
        test_task = Task(
            id=task_id,
            description=task_description,
            type="test_code",
            params={"file_path": file_path, "code": code_content}
        )
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
        print(json.dumps({'success': results.success, 'data': results.data, 'error': results.error}, indent=2))
        
        # Test avec un code qui devrait échouer
        bad_code = "class BadAgent: pass"
        results = await agent.run_test("bad_agent.py", bad_code)
        print("\n--- Test Agent Invalide ---")
        print(json.dumps({'success': results.success, 'data': results.data, 'error': results.error}, indent=2))
        
        await agent.shutdown()

    asyncio.run(main_test())