import re
from typing import List, Tuple, Optional

from taskmaster_v3.core.models import Task, TaskStatus

class ParserService:
    """
    Service pour analyser un texte brut et le transformer en une structure
    hiérarchique de tâches.
    """

    def parse_text_to_tasks(self, text: str) -> List[Task]:
        """
        Analyse un texte multi-lignes pour en extraire une liste hiérarchique de tâches.
        """
        lines = text.strip().split('\n')
        
        # Pile pour suivre les parents (indentation, tâche)
        # On initialise avec une racine virtuelle pour simplifier l'algorithme.
        stack: List[Tuple[int, Task]] = [(-1, Task(title="ROOT", description=""))]

        for line in lines:
            if not line.strip():
                continue

            indentation, title = self._get_indentation_and_title(line)
            
            if title is None:
                continue

            new_task = Task(title=title, description="")
            
            # On remonte la pile pour trouver le parent direct.
            # Le parent est le dernier élément de la pile dont l'indentation
            # est strictement inférieure à l'indentation actuelle.
            while indentation <= stack[-1][0]:
                stack.pop()
            
            parent = stack[-1][1]
            parent.subtasks.append(new_task)
            stack.append((indentation, new_task))

        # Les tâches de premier niveau sont les enfants de la racine virtuelle.
        return stack[0][1].subtasks


    def _get_indentation_and_title(self, line: str) -> Tuple[Optional[int], Optional[str]]:
        """
        Calcule l'indentation d'une ligne et en extrait le titre.
        Toute ligne non vide est considérée comme une tâche potentielle.
        """
        # Compter le nombre d'espaces ou de tabulations
        indent_match = re.match(r'^(\s*)', line)
        indentation = len(indent_match.group(1).replace('\t', '    ')) if indent_match else 0

        # Le titre est simplement le contenu de la ligne, nettoyé
        line_content = line.strip()
        if not line_content:
            return None, None
            
        # Retirer les marqueurs de liste optionnels pour obtenir le titre
        title_match = re.match(r'^[*\-]\s*', line_content)
        title = line_content[title_match.end():].strip() if title_match else line_content
            
        return indentation, title 