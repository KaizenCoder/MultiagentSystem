#!/usr/bin/env python3
"""
Agent Six - Validateur Final NextGeneration
Validation finale et certification des transformations de l'équipe de maintenance
"""

import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import ast
import uuid
import sys
import re
import subprocess
import tempfile
import os

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

# Imports Pattern Factory NextGeneration
from core import logging_manager
from agent_factory_implementation.core.agent_factory_architecture import Agent, Task, Result

class AgentMAINTENANCE06ValidateurFinal(Agent):
    """
    Agent chargé de la validation finale du code.
    Il effectue une vérification de syntaxe finale avec le compilateur Python.
    """
    def __init__(self, agent_id="agent_MAINTENANCE_06_validateur_final", version="1.0", description="Valide le code final.", status="enabled", **kwargs):
        super().__init__(agent_id, version, description, "validator", status, **kwargs)

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

    async def get_capabilities(self):
        return Result(success=True, data=self.capabilities)

    async def health_check(self):
        return Result(success=True, data={"status": "ok"})

    async def shutdown(self):
        self.log("Validateur Final éteint.", level="info")
        await super().shutdown()
        return Result(success=True)

def create_agent_MAINTENANCE_06_validateur_final(**config) -> AgentMAINTENANCE06ValidateurFinal:
    """Factory pour créer une instance de l'Agent 6."""
    return AgentMAINTENANCE06ValidateurFinal(**config)

async def main():
    """Test de l'agent si exécuté directement."""
    print("🏆 Agent 06 Validateur Final - Test")
    
    validator = create_agent_MAINTENANCE_06_validateur_final()
    await validator.startup()
    
    health = await validator.health_check()
    print(f"Health check : {health}")
    
    results = await validator.valider_mission()
    print("Résultats de la validation:", json.dumps(results, indent=2, default=str))

    await validator.shutdown()

if __name__ == "__main__":
    asyncio.run(main())