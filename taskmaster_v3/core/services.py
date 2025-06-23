import uuid
from typing import List, Optional

from taskmaster_v3.core.models import Task, TaskStatus, TaskPriority
from taskmaster_v3.modules.persistence.repository import AbstractTaskRepository


class TaskService:
    """
    Service pour la logique métier de la gestion des tâches.
    """

    def __init__(self, repository: AbstractTaskRepository):
        """
        Initialise le service avec un dépôt de tâches.

        Args:
            repository: Une instance d'une classe implémentant AbstractTaskRepository.
        """
        self.repository = repository

    async def create_task(self, title: str, description: str, priority: TaskPriority = TaskPriority.MEDIUM) -> Task:
        """
        Crée une nouvelle tâche principale.

        Args:
            title: Le titre de la tâche.
            description: La description de la tâche.
            priority: La priorité de la tâche.

        Returns:
            L'objet Task qui a été créé et sauvegardé.
        """
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.TODO,
        )
        await self.repository.save_task(task)
        return task

    async def get_task(self, task_id: str) -> Optional[Task]:
        """
        Récupère une tâche par son ID.

        Args:
            task_id: L'ID de la tâche à récupérer.

        Returns:
            L'objet Task si trouvé, sinon None.
        """
        return await self.repository.get_task(task_id)

    async def decompose_task(self, task_id: str, subtask_titles: List[str]) -> Optional[Task]:
        """
        Décompose une tâche principale en sous-tâches.
        NOTE: Ceci est une implémentation de base. La logique avancée de
              décomposition (inspirée de Gemini) sera intégrée dans un sprint futur.

        Args:
            task_id: L'ID de la tâche à décomposer.
            subtask_titles: Une liste de titres pour les sous-tâches à créer.

        Returns:
            La tâche mise à jour avec ses sous-tâches, ou None si la tâche n'est pas trouvée.
        """
        task = await self.get_task(task_id)
        if not task:
            return None

        for title in subtask_titles:
            subtask = Task(
                id=str(uuid.uuid4()),
                title=title,
                description=f"Sous-tâche de '{task.title}'",
                status=TaskStatus.TODO
            )
            task.subtasks.append(subtask)
        
        task.status = TaskStatus.IN_PROGRESS
        await self.repository.save_task(task)
        return task 