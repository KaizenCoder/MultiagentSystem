from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from core.models import Project, Task

class AbstractTaskRepository(ABC):
    """
    Interface abstraite pour la persistance des projets et des tâches.
    Définit les opérations CRUD nécessaires.
    """

    @abstractmethod
    def add_project(self, project: Project) -> None:
        """Ajoute un nouveau projet au repository."""
        raise NotImplementedError

    @abstractmethod
    def get_project(self, project_id: str) -> Optional[Project]:
        """Récupère un projet par son ID."""
        raise NotImplementedError

    @abstractmethod
    def list_projects(self) -> List[Project]:
        """Liste tous les projets."""
        raise NotImplementedError

    @abstractmethod
    def update_project(self, project_id: str, updates: Dict[str, Any]) -> Optional[Project]:
        """Met à jour un projet."""
        raise NotImplementedError

    @abstractmethod
    def delete_project(self, project_id: str) -> bool:
        """Supprime un projet."""
        raise NotImplementedError

    @abstractmethod
    def add_task_to_project(self, project_id: str, task: Task) -> Optional[Task]:
        """Ajoute une tâche à un projet."""
        raise NotImplementedError

    @abstractmethod
    def get_task(self, task_id: str) -> Optional[Task]:
        """Récupère une tâche par son ID, quel que soit le projet."""
        raise NotImplementedError

    @abstractmethod
    def update_task(self, task_id: str, updates: Dict[str, Any]) -> Optional[Task]:
        """Met à jour une tâche."""
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, task_id: str) -> bool:
        """Supprime une tâche."""
        raise NotImplementedError 