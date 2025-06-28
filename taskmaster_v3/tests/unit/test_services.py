import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock

from taskmaster_v3.core.models import Task, TaskStatus, TaskPriority
from taskmaster_v3.core.services import TaskService
from taskmaster_v3.modules.persistence.repository import AbstractTaskRepository


@pytest.fixture
def mock_repo():
    """Crée un mock pour le AbstractTaskRepository."""
    repo = MagicMock(spec=AbstractTaskRepository)
    repo.save_task = AsyncMock()
    repo.get_task = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repo):
    """Crée une instance de TaskService avec le mock repo."""
    return TaskService(mock_repo)


@pytest.mark.asyncio
async def test_create_task(service: TaskService, mock_repo: MagicMock):
    """
    Teste la création d'une tâche.
    Vérifie que la méthode save_task du repo est appelée avec une tâche valide.
    """
    title = "Test Task"
    description = "A description for the test task"
    priority = TaskPriority.HIGH

    created_task = await service.create_task(title, description, priority)

    assert created_task.title == title
    assert created_task.description == description
    assert created_task.priority == priority
    assert created_task.status == TaskStatus.TODO
    
    # Vérifie que save_task a été appelé une fois avec l'objet task
    mock_repo.save_task.assert_called_once()
    saved_task_arg = mock_repo.save_task.call_args[0][0]
    assert isinstance(saved_task_arg, Task)
    assert saved_task_arg.id == created_task.id


@pytest.mark.asyncio
async def test_get_task(service: TaskService, mock_repo: MagicMock):
    """
    Teste la récupération d'une tâche par son ID.
    """
    task_id = "test-id-123"
    mock_task = Task(id=task_id, title="Mock Task", description="mock desc")
    mock_repo.get_task.return_value = mock_task

    retrieved_task = await service.get_task(task_id)

    mock_repo.get_task.assert_called_once_with(task_id)
    assert retrieved_task == mock_task


@pytest.mark.asyncio
async def test_get_task_not_found(service: TaskService, mock_repo: MagicMock):
    """
    Teste la récupération d'une tâche qui n'existe pas.
    """
    task_id = "non-existent-id"
    mock_repo.get_task.return_value = None

    retrieved_task = await service.get_task(task_id)

    mock_repo.get_task.assert_called_once_with(task_id)
    assert retrieved_task is None


@pytest.mark.asyncio
async def test_decompose_task(service: TaskService, mock_repo: MagicMock):
    """
    Teste la décomposition d'une tâche en sous-tâches.
    """
    task_id = "task-to-decompose"
    original_task = Task(id=task_id, title="Main task", description="To be decomposed")
    
    # Configure le mock de get_task pour retourner notre tâche de test
    service.get_task = AsyncMock(return_value=original_task)

    subtask_titles = ["Subtask 1", "Subtask 2"]
    updated_task = await service.decompose_task(task_id, subtask_titles)

    service.get_task.assert_called_once_with(task_id)
    
    assert updated_task is not None
    assert len(updated_task.subtasks) == 2
    assert updated_task.status == TaskStatus.IN_PROGRESS

    # Vérifie les détails des sous-tâches créées
    assert updated_task.subtasks[0].title == "Subtask 1"
    assert updated_task.subtasks[1].title == "Subtask 2"
    assert all(isinstance(st, Task) for st in updated_task.subtasks)
    assert all(st.status == TaskStatus.TODO for st in updated_task.subtasks)

    # Vérifie que la tâche mise à jour est sauvegardée
    mock_repo.save_task.assert_called_once_with(updated_task)


@pytest.mark.asyncio
async def test_decompose_task_not_found(service: TaskService, mock_repo: MagicMock):
    """
    Teste la décomposition d'une tâche qui n'existe pas.
    """
    task_id = "non-existent-id"
    service.get_task = AsyncMock(return_value=None)
    
    result = await service.decompose_task(task_id, ["some subtask"])
    
    service.get_task.assert_called_once_with(task_id)
    assert result is None
    mock_repo.save_task.assert_not_called() 