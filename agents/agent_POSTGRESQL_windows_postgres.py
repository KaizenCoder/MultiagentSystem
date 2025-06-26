#!/usr/bin/env python3
"""
Agent Windows PostgreSQL - Configuration Windows pour PostgreSQL
Développé par l'équipe de maintenance NextGeneration
"""

import os
import subprocess
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from .agent_POSTGRESQL_base import AgentPostgreSQLBase
from core.agent_factory_architecture import Task, Result

class AgentPostgresqlWindowsPostgres(AgentPostgreSQLBase):
    """Agent spécialisé dans la gestion de PostgreSQL sous Windows."""
    
    def __init__(self, workspace_root: Path = None):
        super().__init__(
            agent_type="postgresql_windows_postgres",
            name="Agent Windows PostgreSQL"
        )
        self.workspace_root = workspace_root if workspace_root else Path(__file__).parent.parent
        self.logs = []

    def get_capabilities(self) -> list:
        return [
            "diagnostiquer_windows",
            "configurer_environnement_windows",
            "tester_connexion"
        ]

    async def execute_task(self, task: Task) -> Result:
        try:
            handlers = {
                "diagnostiquer_windows": self._handle_diagnostiquer_windows,
                "configurer_environnement_windows": self._handle_configurer_environnement_windows,
                "tester_connexion": self._handle_tester_connexion
            }
            handler = handlers.get(task.type)
            if not handler:
                return Result(success=False, error=f"Type de tâche non supporté: {task.type}")
            return await handler(task)
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche: {e}")
            return Result(success=False, error=str(e))

    async def _handle_diagnostiquer_windows(self, task: Task) -> Result:
        diagnostic = await self.diagnostiquer_windows()
        return Result(success=True, data=diagnostic)

    async def _handle_configurer_environnement_windows(self, task: Task) -> Result:
        config = await self.configurer_environnement_windows()
        return Result(success=True, data=config)

    async def _handle_tester_connexion(self, task: Task) -> Result:
        result = await self.tester_connexion()
        return Result(success=result, data={"connexion": result})

    async def diagnostiquer_windows(self) -> Dict[str, Any]:
        diagnostic = {
            "postgresql_installe": False,
            "services_windows": [],
            "variables_env": {},
            "problemes": []
        }
        try:
            result = await asyncio.to_thread(subprocess.run, ["pg_config", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                diagnostic["postgresql_installe"] = True
                diagnostic["version"] = result.stdout.strip()
                self.log("PostgreSQL détecté sur Windows")
            else:
                diagnostic["problemes"].append("PostgreSQL non trouvé dans PATH")
        except FileNotFoundError:
            diagnostic["problemes"].append("PostgreSQL non installé")
        env_vars = ["PGDATA", "PGUSER", "PGHOST", "PGPORT"]
        for var in env_vars:
            diagnostic["variables_env"][var] = os.environ.get(var, "NON_DEFINI")
        return diagnostic

    async def configurer_environnement_windows(self) -> Dict[str, str]:
        config = {
            "PGHOST": "localhost",
            "PGPORT": "5432",
            "PGUSER": "postgres"
        }
        for var, valeur in config.items():
            if not os.environ.get(var):
                os.environ[var] = valeur
                self.log(f"Variable {var} configurée: {valeur}")
        return config

    async def tester_connexion(self) -> bool:
        try:
            cmd = ["psql", "-h", "localhost", "-U", "postgres", "-c", "SELECT 1;"]
            result = await asyncio.to_thread(subprocess.run, cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log("Connexion PostgreSQL réussie")
                return True
            else:
                self.log(f"Échec connexion: {result.stderr}")
                return False
        except Exception as e:
            self.log(f"Erreur test connexion: {e}")
            return False

    def log(self, message):
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        self.logs.append(entry)
        print(f"🪟 {entry}") 