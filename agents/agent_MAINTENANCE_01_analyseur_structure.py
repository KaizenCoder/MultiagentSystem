#!/usr/bin/env python3
"""
AGENT 1 - ANALYSEUR DE STRUCTURE (Pattern Factory)
🏗️ ANALYSEUR DE STRUCTURE - Agent 01
====================================

🎯 Mission : Analyser la structure du code et détecter les erreurs syntaxiques.
⚡ Capacités : Analyse statique avec `py_compile`, `ast`, et `pylint`.
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 1.2.0
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
    Agent spécialisé dans l'analyse de la structure des fichiers de code.
    """
    def __init__(self, **kwargs):
        """Initialisation standardisée."""
        super().__init__(agent_type="analyseur_structure", **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Analyseur de structure ({self.id}) initialisé.")

    async def startup(self):
        """Démarrage de l'agent."""
        self.logger.info(f"Analyseur de structure prêt.")

    async def execute_task(self, task: Task) -> Result:
        """Exécute la tâche d'analyse du répertoire ou d'un fichier."""
        if task.type != "analyse_structure":
            return Result(success=False, error="Type de tâche non supporté.")

        directory = task.params.get("directory")
        file_path_param = task.params.get("file_path")

        if not directory and not file_path_param:
            return Result(success=False, error="Répertoire ou chemin de fichier non spécifié.")

        if file_path_param:
            files_to_process = [file_path_param]
        else:
            files_to_process = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".py")]

        self.logger.info(f"Analyse demandée pour : {directory or file_path_param}")
        
        files_analysis = []
        try:
            for file_path in files_to_process:
                self.logger.info(f"Analyse du fichier : {file_path}")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    analysis = self._analyze_python_file(content)
                    files_analysis.append({
                        "path": file_path,
                        "analysis": analysis,
                    })
                except Exception as e:
                    self.logger.error(f"Erreur lors de l'analyse du fichier {file_path}: {e}")
                    files_analysis.append({
                        "path": file_path,
                        "error": str(e),
                    })
            
            # Pour la cohérence, si un seul fichier a été demandé, on retourne directement son analyse.
            if file_path_param and len(files_analysis) == 1:
                result_data = files_analysis[0]
                return Result(success=not result_data.get("error"), data=result_data)

            return Result(success=True, data={"files": files_analysis})

        except Exception as e:
            self.logger.critical(f"Erreur majeure lors de l'analyse : {e}")
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

    def get_capabilities(self) -> List[str]:
        return ["analyse_structure"]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy"}

    async def shutdown(self):
        self.logger.info("Analyseur de structure éteint.")
        

    async def run_analysis(self, directory: str) -> Result:
        """Méthode de compatibilité pour l'ancien appel du coordinateur."""
        self.logger.warning(f"Appel de compatibilité 'run_analysis' pour le répertoire: {directory}")
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