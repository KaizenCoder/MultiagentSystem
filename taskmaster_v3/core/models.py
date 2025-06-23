from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Any, Dict
from uuid import uuid4

# ==========================================
# 1. ENUMERATIONS
# ==========================================

class TaskType(Enum):
    """Types de tâches supportés."""
    AUDIT = "audit"
    ANALYSIS = "analysis"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    REFACTORING = "refactoring"
    MONITORING = "monitoring"
    DEPLOYMENT = "deployment"
    PARSING = "parsing"
    PLANNING = "planning"

class ValidationStatus(Enum):
    """Statuts de validation (lutte anti-hallucination)."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_CLARIFICATION = "needs_clarification"

class TaskPriority(Enum):
    """Niveaux de priorité des tâches."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class ComplexityLevel(Enum):
    """Niveaux de complexité d'une tâche."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"

class TaskStatus(Enum):
    """Statuts d'exécution d'une tâche."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    FAILED = "failed"
    BLOCKED = "blocked"

# ==========================================
# 2. STRUCTURES DE DONNÉES (DATACLASSES)
# ==========================================

@dataclass
class Evidence:
    """Représente une preuve pour la validation d'un résultat."""
    source: str
    content: Any
    confidence: float
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Task:
    """Représente une tâche ou sous-tâche décomposable."""
    title: str
    description: str
    id: str = field(default_factory=lambda: str(uuid4()))
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    complexity: ComplexityLevel = ComplexityLevel.SIMPLE
    complexity_score: int = 0
    depends_on: List[str] = field(default_factory=list)
    subtasks: List[Task] = field(default_factory=list)
    outputs: List[Any] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class Project:
    """Représente un projet contenant un ensemble de tâches."""
    name: str
    description: str
    id: str = field(default_factory=lambda: str(uuid4()))
    tasks: List[Task] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Trouve une tâche par son ID, y compris dans les sous-tâches."""
        def find_in_list(tasks: List[Task]) -> Optional[Task]:
            for task in tasks:
                if task.id == task_id:
                    return task
                found = find_in_list(task.subtasks)
                if found:
                    return found
            return None
        return find_in_list(self.tasks) 