import pytest
from taskmaster_v3.modules.parsing.parser_service import ParserService
from taskmaster_v3.core.models import Task

@pytest.fixture
def parser():
    return ParserService()

def test_parse_simple_list(parser: ParserService):
    """Teste une liste simple sans hiérarchie."""
    text = """
    * Tâche 1
    * Tâche 2
    - Tâche 3
    """
    tasks = parser.parse_text_to_tasks(text)
    assert len(tasks) == 3
    assert tasks[0].title == "Tâche 1"
    assert tasks[1].title == "Tâche 2"
    assert tasks[2].title == "Tâche 3"
    assert all(not t.subtasks for t in tasks)

def test_parse_nested_list_spaces(parser: ParserService):
    """Teste une liste hiérarchique avec des espaces."""
    text = """
    - Root 1
      - Child 1.1
        - Grandchild 1.1.1
      - Child 1.2
    - Root 2
    """
    tasks = parser.parse_text_to_tasks(text)
    assert len(tasks) == 2
    
    root1 = tasks[0]
    assert root1.title == "Root 1"
    assert len(root1.subtasks) == 2

    child1_1 = root1.subtasks[0]
    assert child1_1.title == "Child 1.1"
    assert len(child1_1.subtasks) == 1
    
    grandchild = child1_1.subtasks[0]
    assert grandchild.title == "Grandchild 1.1.1"
    assert not grandchild.subtasks

    child1_2 = root1.subtasks[1]
    assert child1_2.title == "Child 1.2"
    assert not child1_2.subtasks

    root2 = tasks[1]
    assert root2.title == "Root 2"
    assert not root2.subtasks

def test_parse_nested_list_tabs(parser: ParserService):
    """Teste une liste hiérarchique avec des tabulations."""
    text = "* Root 1\n\t* Child 1.1\n\t\t* Grandchild 1.1.1"
    tasks = parser.parse_text_to_tasks(text)
    assert len(tasks) == 1
    
    root = tasks[0]
    assert root.title == "Root 1"
    assert len(root.subtasks) == 1

    child = root.subtasks[0]
    assert child.title == "Child 1.1"
    assert len(child.subtasks) == 1

    grandchild = child.subtasks[0]
    assert grandchild.title == "Grandchild 1.1.1"
    assert not grandchild.subtasks

def test_handle_empty_and_invalid_lines(parser: ParserService):
    """Teste la gestion des lignes vides ou mal formatées."""
    text = """
    * Tâche valide 1

    Ceci n'est pas une tâche.
      * Tâche valide 2
    
    """
    tasks = parser.parse_text_to_tasks(text)
    assert len(tasks) == 2
    assert tasks[0].title == "Tâche valide 1"
    assert tasks[1].title == "Tâche valide 2"

def test_parse_empty_string(parser: ParserService):
    """Teste que le parsing d'une chaîne vide renvoie une liste vide."""
    text = ""
    tasks = parser.parse_text_to_tasks(text)
    assert len(tasks) == 0

def test_complex_hierarchy(parser: ParserService):
    """Teste une structure plus complexe avec des indentations variables."""
    text = """
* level 0 A
  * level 1 A
    * level 2 A
  * level 1 B
* level 0 B
  * level 1 C
"""
    tasks = parser.parse_text_to_tasks(text)
    assert len(tasks) == 2
    
    level0_A = tasks[0]
    assert level0_A.title == "level 0 A"
    assert len(level0_A.subtasks) == 2

    level1_A = level0_A.subtasks[0]
    assert level1_A.title == "level 1 A"
    assert len(level1_A.subtasks) == 1

    level2_A = level1_A.subtasks[0]
    assert level2_A.title == "level 2 A"
    assert not level2_A.subtasks

    level1_B = level0_A.subtasks[1]
    assert level1_B.title == "level 1 B"
    assert not level1_B.subtasks

    level0_B = tasks[1]
    assert level0_B.title == "level 0 B"
    assert len(level0_B.subtasks) == 1

    level1_C = level0_B.subtasks[0]
    assert level1_C.title == "level 1 C"
    assert not level1_C.subtasks 