import re
from typing import List, Dict, Set
from taskmaster_v3.core.models import Task, TaskStatus

class DependencyAnalyzer:
    """
    Analyseur de dépendances pour la hiérarchie de tâches.
    Détecte les dépendances explicites et construit un graphe orienté.
    """

    DEPENDENCY_PATTERNS = [
        r"dépend de[:\s]*([\w\s\-\.]+)",
        r"après[:\s]*([\w\s\-\.]+)",
        r"doit suivre[:\s]*([\w\s\-\.]+)",
        r"avant[:\s]*([\w\s\-\.]+)"
    ]

    def analyze(self, root_tasks: List[Task]) -> Dict[str, Set[str]]:
        """
        Analyse la hiérarchie et retourne un graphe de dépendances (id -> set d'ids dont il dépend).
        Marque les tâches bloquées si leurs dépendances ne sont pas terminées.
        """
        all_tasks = self._flatten_tasks(root_tasks)
        name_to_id = {task.title.lower(): task.id for task in all_tasks}
        dep_graph: Dict[str, Set[str]] = {task.id: set() for task in all_tasks}

        # Détection des dépendances
        for task in all_tasks:
            deps = self._extract_dependencies(task, name_to_id)
            dep_graph[task.id].update(deps)
            if deps:
                task.status = TaskStatus.BLOCKED

        return dep_graph

    def _extract_dependencies(self, task: Task, name_to_id: Dict[str, str]) -> Set[str]:
        """
        Extrait les dépendances à partir du titre et de la description.
        """
        deps = set()
        text = f"{task.title} {task.description}".lower()
        for pattern in self.DEPENDENCY_PATTERNS:
            for match in re.findall(pattern, text):
                dep_name = match.strip().lower()
                if dep_name in name_to_id and name_to_id[dep_name] != task.id:
                    deps.add(name_to_id[dep_name])
        return deps

    def _flatten_tasks(self, tasks: List[Task]) -> List[Task]:
        """
        Aplati la hiérarchie en une liste de toutes les tâches.
        """
        result = []
        for task in tasks:
            result.append(task)
            result.extend(self._flatten_tasks(task.subtasks))
        return result 