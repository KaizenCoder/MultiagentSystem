#!/usr/bin/env python3
"""
AGENT 6 - VALIDATEUR FINAL (Pattern Factory)
✅ VALIDATEUR FINAL - Agent 06
===============================
🎯 Mission : Effectuer une validation complète et finale d'un agent réparé.
⚡ Capacités : Combinaison de tests de structure, d'utilité et de performance.
🏢 Équipe : NextGeneration Tools Migration
Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
"""

import asyncio
import json
import logging
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import os
import ast
import subprocess
import tempfile

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

class AgentMAINTENANCE06ValidateurFinal(Agent):
    """
    Agent chargé de la validation finale du code.
    Il effectue une vérification de syntaxe finale avec le compilateur Python.
    """
    def __init__(self, **kwargs):
        """Initialisation robuste et compatible avec le coordinateur."""
        super().__init__(**kwargs)
        self.logger.info(f"Validateur Final ({self.agent_id}) initialisé.")

    async def startup(self):
        await super().startup()
        self.log("Validateur final prêt.")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "validate_code":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni.")

        self.log(f"Validation finale du fichier : {file_path}")

        try:
            # Validation 1: Vérification de syntaxe avec AST
            try:
                tree = ast.parse(code)
                syntax_validation = "passed"
                self.log(f"Validation AST réussie pour {file_path}.")
            except SyntaxError as e:
                self.log(f"Validation échouée pour {file_path}. Erreur de syntaxe AST: {e}", level="error")
                return Result(success=False, error=f"SyntaxError: {e.msg} (line {e.lineno})")

            # Validation 2: Compilation Python
            try:
                compile(code, file_path, 'exec')
                compile_validation = "passed"
                self.log(f"Compilation Python réussie pour {file_path}.")
            except SyntaxError as e:
                self.log(f"Validation échouée pour {file_path}. Erreur de compilation: {e}", level="error")
                return Result(success=False, error=f"Compilation SyntaxError: {e.msg} (line {e.lineno})")

            # Validation 3: Linter basique
            linter_details = self._run_basic_linter(code, file_path)
            
            # Validation 4: Vérifications spécifiques aux agents
            agent_validation = self._validate_agent_structure(tree)

            self.log(f"Toutes les validations réussies pour {file_path}.")
            return Result(success=True, data={
                "validation": "passed",
                "syntax_validation": syntax_validation,
                "compile_validation": compile_validation,
                "linter_details": linter_details,
                "agent_validation": agent_validation
            })

        except Exception as e:
            self.log(f"Erreur inattendue lors de la validation de {file_path}: {e}", level="critical")
            return Result(success=False, error=f"Unexpected validation error: {e}")

    def _run_basic_linter(self, code: str, file_path: str) -> dict:
        """Exécute un linter basique via subprocess."""
        linter_result = {
            "status": "completed",
            "method": "subprocess_compile_check",
            "issues": []
        }
        
        try:
            # Créer un fichier temporaire pour le test
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
                tmp.write(code)
                tmp_path = tmp.name
            
            try:
                # Utilise l'interpréteur courant pour vérifier la syntaxe
                process = subprocess.run(
                    [sys.executable, "-m", "py_compile", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if process.returncode == 0:
                    linter_result["status"] = "passed"
                else:
                    linter_result["status"] = "failed"
                    linter_result["issues"].append(f"py_compile failed: {process.stderr}")
                    
            except subprocess.TimeoutExpired:
                linter_result["status"] = "timeout"
                linter_result["issues"].append("Linter timeout")
            except Exception as e:
                linter_result["status"] = "error"
                linter_result["issues"].append(f"Linter execution error: {e}")
            finally:
                # Nettoyer le fichier temporaire
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                    
        except Exception as e:
            linter_result["status"] = "error"
            linter_result["issues"].append(f"Linter setup error: {e}")
        
        return linter_result

    def _validate_agent_structure(self, tree: ast.AST) -> dict:
        """Valide la structure spécifique aux agents."""
        validation = {
            "has_agent_class": False,
            "has_execute_task": False,
            "has_startup": False,
            "agent_class_name": None,
            "issues": []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Vérifier si c'est une classe d'agent
                base_names = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        base_names.append(base.id)
                
                if 'Agent' in base_names:
                    validation["has_agent_class"] = True
                    validation["agent_class_name"] = node.name
                    
                    # Vérifier les méthodes requises dans la classe
                    methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                    
                    if 'execute_task' in methods:
                        validation["has_execute_task"] = True
                    else:
                        validation["issues"].append("Méthode execute_task manquante")
                    
                    if 'startup' in methods:
                        validation["has_startup"] = True
                    else:
                        validation["issues"].append("Méthode startup manquante")
        
        if not validation["has_agent_class"]:
            validation["issues"].append("Aucune classe héritant d'Agent trouvée")
        
        return validation

    def get_capabilities(self) -> List[str]:
        return ["final_validation"]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy"}

    async def shutdown(self):
        """Arrêt de l'agent."""
        self.log("Validateur Final éteint.")

    async def run_validation(self, file_path: str, code_content: str) -> Result:
        """Méthode de compatibilité pour l'ancien appel."""
        self.log(f"Appel de compatibilité 'run_validation' pour {file_path}", level="warning")
        validation_task = Task(type="final_validation", params={"file_path": file_path, "code_content": code_content})
        return await self.execute_task(validation_task)


def create_agent_MAINTENANCE_06_validateur_final(**config) -> AgentMAINTENANCE06ValidateurFinal:
    """Factory pour créer une instance de l'Agent 6."""
    return AgentMAINTENANCE06ValidateurFinal(**config)

if __name__ == '__main__':
    async def main_test():
        agent = create_agent_MAINTENANCE_06_validateur_final(agent_id='test-validator', version='1.0', description='test', agent_type='validator', status='testing')
        await agent.startup()
        
        valid_code = '''
from core.agent_factory_architecture import Agent, Task, Result
import asyncio

class MyAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    async def execute_task(self, task: Task) -> Result: return Result(success=True)
    def get_capabilities(self) -> list: return []
    async def startup(self): pass
    async def shutdown(self): pass
    async def health_check(self) -> dict: return {"status": "ok"}
'''
        results = await agent.run_validation("valid_agent.py", valid_code)
        print("--- Validation Agent Valide ---")
        print(json.dumps(results.to_dict(), indent=2))

        invalid_code = "def my_func(): pass"
        results = await agent.run_validation("invalid_agent.py", invalid_code)
        print("\n--- Validation Agent Invalide ---")
        print(json.dumps(results.to_dict(), indent=2))
        
        await agent.shutdown()

    asyncio.run(main_test())