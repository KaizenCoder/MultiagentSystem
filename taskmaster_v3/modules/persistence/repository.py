from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from taskmaster_v3.core.models import Project, Task

class AbstractTaskRepository(ABC):
    """
    Interface abstraite pour la persistance des projets et des tâches.
    Définit les opérations CRUD nécessaires.
    """

    @abstractmethod
    async def save_task(self, task: Task) -> None:
        """Sauvegarde une tâche (création ou mise à jour)."""
        raise NotImplementedError

    @abstractmethod
    async def get_task(self, task_id: str) -> Optional[Task]:
        """Récupère une tâche par son ID, quel que soit le projet."""
        raise NotImplementedError
    
    # Les autres méthodes ne sont pas nécessaires pour le Sprint 2
    # mais sont gardées pour la structure future.

    @abstractmethod
    async def add_project(self, project: Project) -> None:
        """Ajoute un nouveau projet au repository."""
        raise NotImplementedError

    @abstractmethod
    async def get_project(self, project_id: str) -> Optional[Project]:
        """Récupère un projet par son ID."""
        raise NotImplementedError

    @abstractmethod
    async def list_projects(self) -> List[Project]:
        """Liste tous les projets."""
        raise NotImplementedError

    @abstractmethod
    async def update_project(self, project_id: str, updates: Dict[str, Any]) -> Optional[Project]:
        """Met à jour un projet."""
        raise NotImplementedError

    @abstractmethod
    async def delete_project(self, project_id: str) -> bool:
        """Supprime un projet."""
        raise NotImplementedError

    @abstractmethod
    async def add_task_to_project(self, project_id: str, task: Task) -> Optional[Task]:
        """Ajoute une tâche à un projet."""
        raise NotImplementedError

    @abstractmethod
    async def update_task(self, task_id: str, updates: Dict[str, Any]) -> Optional[Task]:
        """Met à jour une tâche."""
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, task_id: str) -> bool:
        """Supprime une tâche."""
        raise NotImplementedError


class InMemoryTaskRepository(AbstractTaskRepository):
    """
    Implémentation en mémoire du repository de tâches.
    Utile pour les tests et le développement rapide.
    """

    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._projects: Dict[str, Project] = {}

    async def save_task(self, task: Task) -> None:
        """Sauvegarde une tâche en mémoire."""
        self._tasks[task.id] = task

    async def get_task(self, task_id: str) -> Optional[Task]:
        """Récupère une tâche depuis la mémoire."""
        return self._tasks.get(task_id)
    
    # Implémentation par défaut pour les autres méthodes
    async def add_project(self, project: Project) -> None:
        self._projects[project.id] = project

    async def get_project(self, project_id: str) -> Optional[Project]:
        return self._projects.get(project_id)

    async def list_projects(self) -> List[Project]:
        return list(self._projects.values())

    async def update_project(self, project_id: str, updates: Dict[str, Any]) -> Optional[Project]:
        if project_id in self._projects:
            project = self._projects[project_id]
            for key, value in updates.items():
                setattr(project, key, value)
            return project
        return None

    async def delete_project(self, project_id: str) -> bool:
        if project_id in self._projects:
            del self._projects[project_id]
            return True
        return False
    
    async def add_task_to_project(self, project_id: str, task: Task) -> Optional[Task]:
        if project_id in self._projects:
            project = self._projects[project_id]
            project.tasks.append(task)
            await self.save_task(task) # also save in the global task list
            return task
        return None

    async def update_task(self, task_id: str, updates: Dict[str, Any]) -> Optional[Task]:
        if task_id in self._tasks:
            task = self._tasks[task_id]
            for key, value in updates.items():
                setattr(task, key, value)
            return task
        return None

    async def delete_task(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False 