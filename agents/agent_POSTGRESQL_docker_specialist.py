#!/usr/bin/env python3
"""
Agent Docker Specialist - Conteneurisation PostgreSQL
Développé par l'équipe de maintenance NextGeneration
"""

import os
import subprocess
from datetime import datetime
import logging
from pathlib import Path
import docker
import json

# Import avec fallback
try:
    from .agent_POSTGRESQL_base import AgentPostgreSQLBase
except ImportError:
    try:
        from agent_POSTGRESQL_base import AgentPostgreSQLBase
    except ImportError:
        # Fallback pour AgentPostgreSQLBase
        class AgentPostgreSQLBase:
            def __init__(self, *args, **kwargs):
                pass
from core.agent_factory_architecture import Task, Result

class AgentPostgresqlDockerSpecialist(AgentPostgreSQLBase):
    """Agent spécialisé pour la gestion des conteneurs Docker PostgreSQL"""
    
    def __init__(self, workspace_root: Path = None):
        super().__init__(
            agent_type="postgresql_docker",
            name="Agent PostgreSQL Docker"
        )
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="postgresql",
                custom_config={
                    "logger_name": f"nextgen.postgresql.POSTGRESQL_docker_specialist.{self.agent_id if hasattr(self, 'agent_id') else self.id if hasattr(self, 'id') else 'unknown'}",
                    "log_dir": "logs/postgresql",
                    "metadata": {
                        "agent_type": "POSTGRESQL_docker_specialist",
                        "agent_role": "postgresql",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)

        self.workspace_root = workspace_root if workspace_root else Path(__file__).parent.parent
        self.docker_client = docker.from_env()
        
    def get_capabilities(self) -> list:
        """Liste des capacités spécifiques de l'agent"""
        return [
            "inspect_container",
            "create_container",
            "start_container",
            "stop_container",
            "remove_container",
            "check_logs"
        ]

    async def execute_task(self, task: Task) -> Result:
        """Exécution d'une tâche selon le Pattern Factory"""
        try:
            if task.type == "inspect_container":
                container_name = task.params.get("container_name")
                if not container_name:
                    return Result(success=False, error="Nom du conteneur requis")
                resultats = await self.inspect_container(container_name)
                return Result(success=True, data=resultats)
                
            elif task.type == "create_container":
                config = task.params.get("config", {})
                resultats = await self.create_container(config)
                return Result(success=True, data=resultats)
                
            elif task.type == "start_container":
                container_name = task.params.get("container_name")
                if not container_name:
                    return Result(success=False, error="Nom du conteneur requis")
                resultats = await self.start_container(container_name)
                return Result(success=True, data=resultats)
                
            elif task.type == "stop_container":
                container_name = task.params.get("container_name")
                if not container_name:
                    return Result(success=False, error="Nom du conteneur requis")
                resultats = await self.stop_container(container_name)
                return Result(success=True, data=resultats)
                
            elif task.type == "remove_container":
                container_name = task.params.get("container_name")
                if not container_name:
                    return Result(success=False, error="Nom du conteneur requis")
                resultats = await self.remove_container(container_name)
                return Result(success=True, data=resultats)
                
            elif task.type == "check_logs":
                container_name = task.params.get("container_name")
                if not container_name:
                    return Result(success=False, error="Nom du conteneur requis")
                resultats = await self.check_logs(container_name)
                return Result(success=True, data=resultats)
                
            else:
                return Result(
                    success=False,
                    error=f"Type de tâche non supporté: {task.type}"
                )
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche: {e}")
            return Result(
                success=False,
                error=str(e),
                error_code="EXECUTION_ERROR"
            )

    async def inspect_container(self, container_name: str) -> dict:
        """Inspecte un conteneur Docker"""
        try:
            container = self.docker_client.containers.get(container_name)
            inspection = container.attrs
            
            return {
                "status": "success",
                "container_info": {
                    "id": inspection["Id"],
                    "name": inspection["Name"],
                    "status": inspection["State"]["Status"],
                    "created": inspection["Created"],
                    "ports": inspection["NetworkSettings"]["Ports"],
                    "volumes": inspection["Mounts"],
                    "env": inspection["Config"]["Env"]
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'inspection du conteneur {container_name}: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def create_container(self, config: dict) -> dict:
        """Crée un nouveau conteneur Docker"""
        try:
            container = self.docker_client.containers.create(
                image=config.get("image", "postgres:latest"),
                name=config.get("name"),
                environment=config.get("environment", {}),
                ports=config.get("ports", {}),
                volumes=config.get("volumes", [])
            )
            
            return {
                "status": "success",
                "container_id": container.id,
                "container_name": container.name
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du conteneur: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def start_container(self, container_name: str) -> dict:
        """Démarre un conteneur Docker"""
        try:
            container = self.docker_client.containers.get(container_name)
            container.start()
            
            return {
                "status": "success",
                "container_id": container.id,
                "container_status": container.status
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage du conteneur {container_name}: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def stop_container(self, container_name: str) -> dict:
        """Arrête un conteneur Docker"""
        try:
            container = self.docker_client.containers.get(container_name)
            container.stop()
            
            return {
                "status": "success",
                "container_id": container.id,
                "container_status": container.status
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'arrêt du conteneur {container_name}: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def remove_container(self, container_name: str) -> dict:
        """Supprime un conteneur Docker"""
        try:
            container = self.docker_client.containers.get(container_name)
            container.remove(force=True)
            
            return {
                "status": "success",
                "container_id": container.id
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression du conteneur {container_name}: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def check_logs(self, container_name: str) -> dict:
        """Récupère les logs d'un conteneur Docker"""
        try:
            container = self.docker_client.containers.get(container_name)
            logs = container.logs().decode('utf-8')
            
            return {
                "status": "success",
                "logs": logs
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des logs du conteneur {container_name}: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

if __name__ == "__main__":
    agent = AgentPostgresqlDockerSpecialist()
    # Test des capacités
    print("Capacités de l'agent:", agent.get_capabilities())



# Aliases et fonctions pour compatibilité
AgentDockerSpecialist = AgentPostgresqlDockerSpecialist

def create_agent_docker_specialist(**kwargs):
    """Factory function pour créer l'agent Docker specialist"""
    return AgentPostgresqlDockerSpecialist(**kwargs)

def get_docker_specialist():
    """Obtient une instance de l'agent Docker specialist"""
    return AgentPostgresqlDockerSpecialist()
