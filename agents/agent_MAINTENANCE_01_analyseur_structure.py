#!/usr/bin/env python3
"""
AGENT 1 - ANALYSEUR DE STRUCTURE (Pattern Factory)
"""
import asyncio
import ast
import json
import logging
import sys
import time
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import os

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
PATTERN_FACTORY_AVAILABLE = True


class AgentMAINTENANCE01AnalyseurStructure(Agent):
    """
    Agent chargé d'analyser la structure des fichiers d'un répertoire donné.
    """
    def __init__(self, agent_id="agent_MAINTENANCE_01_analyseur_structure", version="1.0", description="Analyse la structure des fichiers d'un répertoire.", status="enabled", **kwargs):
        super().__init__(agent_id, version, description, "analyser", status, **kwargs)

    async def startup(self):
        """Initialise l'agent et ses dépendances."""
        await super().startup()
        self.log("Analyseur de structure prêt.")

    async def execute_task(self, task: Task) -> Result:
        """Exécute la tâche d'analyse du répertoire."""
        if task.type != "analyse_structure":
            return Result(success=False, error="Type de tâche non supporté.")

        directory = task.params.get("directory")
        if not directory or not os.path.isdir(directory):
            return Result(success=False, error=f"Répertoire invalide ou non spécifié: {directory}")

        self.log(f"Analyse du répertoire : {directory}")
        files_analysis = []
        try:
            for filename in os.listdir(directory):
                if filename.endswith(".py") and filename.startswith("agent_MAINTENANCE_"):
                    file_path = os.path.join(directory, filename)
                    self.log(f"Analyse du fichier : {file_path}")
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        analysis = self._analyze_python_file(content)
                        files_analysis.append({
                            "path": file_path,
                            "content": content,
                            "analysis": analysis,
                        })
                    except Exception as e:
                        self.log(f"Erreur lors de l'analyse du fichier {file_path}: {e}", level="error")
                        files_analysis.append({
                            "path": file_path,
                            "content": None,
                            "error": str(e),
                        })

            return Result(success=True, data={"files": files_analysis})

        except Exception as e:
            self.log(f"Erreur majeure lors de l'analyse du répertoire {directory}: {e}", level="critical")
            return Result(success=False, error=str(e))

    def _analyze_python_file(self, code: str) -> dict:
        """
        Analyse le contenu d'un fichier Python pour en extraire la structure de base.
        """
        analysis_report = {
            "imports": [],
            "classes": [],
            "functions": [],
            "has_async": False,
        }
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis_report["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis_report["imports"].append(node.module)
                elif isinstance(node, ast.ClassDef):
                    analysis_report["classes"].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    analysis_report["functions"].append(node.name)
                elif isinstance(node, ast.AsyncFunctionDef):
                    analysis_report["functions"].append(f"async {node.name}")
                    analysis_report["has_async"] = True
        except SyntaxError as e:
            return {"error": f"SyntaxError: {e}"}

        return analysis_report

    async def get_capabilities(self):
        return Result(success=True, data={"capabilities": "Analyse de structure de fichiers Python."})

    async def health_check(self):
        return Result(success=True, data={"status": "healthy"})

    async def shutdown(self):
        self.log("Analyseur de structure éteint.")
        await super().shutdown()
        return Result(success=True)

    async def run_analysis(self, directory: str) -> Result:
        """Méthode de compatibilité pour l'ancien appel du coordinateur."""
        self.log(f"Appel de compatibilité 'run_analysis' pour le répertoire: {directory}", level="warning")
        analyse_task = Task(type="analyse_structure", params={"directory": directory})
        return await self.execute_task(analyse_task)

def create_agent_MAINTENANCE_01_analyseur_structure(**config) -> AgentMAINTENANCE01AnalyseurStructure:
    """Factory pour créer une instance de l'Agent 1."""
    return AgentMAINTENANCE01AnalyseurStructure(**config)

if __name__ == '__main__':
    async def main_test():
        agent = create_agent_MAINTENANCE_01_analyseur_structure(source_path="agent_factory_implementation/agents")
        await agent.startup()
        results = await agent.run_analysis("agent_factory_implementation/agents")
        print(json.dumps(results, indent=2))
        await agent.shutdown()
    asyncio.run(main_test())
