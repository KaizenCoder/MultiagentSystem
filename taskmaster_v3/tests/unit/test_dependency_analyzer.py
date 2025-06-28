import pytest
from taskmaster_v3.modules.dependencies.dependency_analyzer import DependencyAnalyzer
from taskmaster_v3.core.models import Task, TaskStatus

def make_task(title, description="", subtasks=None):
    t = Task(title=title, description=description)
    if subtasks:
        t.subtasks = subtasks
    return t

def test_no_dependencies():
    tasks = [make_task("A"), make_task("B")]
    analyzer = DependencyAnalyzer()
    graph = analyzer.analyze(tasks)
    assert all(len(deps) == 0 for deps in graph.values())
    assert all(t.status == TaskStatus.TODO for t in tasks)

def test_single_dependency_in_title():
    t1 = make_task("A")
    t2 = make_task("B (dépend de: A)")
    analyzer = DependencyAnalyzer()
    graph = analyzer.analyze([t1, t2])
    assert graph[t2.id] == {t1.id}
    assert t2.status == TaskStatus.BLOCKED
    assert t1.status == TaskStatus.TODO

def test_dependency_in_description():
    t1 = make_task("A")
    t2 = make_task("B", description="Ce livrable dépend de: A")
    analyzer = DependencyAnalyzer()
    graph = analyzer.analyze([t1, t2])
    assert graph[t2.id] == {t1.id}
    assert t2.status == TaskStatus.BLOCKED

def test_multiple_dependencies():
    t1 = make_task("A")
    t2 = make_task("B")
    t3 = make_task("C (dépend de: A)", description="et après B")
    analyzer = DependencyAnalyzer()
    graph = analyzer.analyze([t1, t2, t3])
    assert graph[t3.id] == {t1.id, t2.id}
    assert t3.status == TaskStatus.BLOCKED

def test_hierarchy_dependencies():
    t1 = make_task("A")
    t2 = make_task("B", subtasks=[make_task("B1 (dépend de: A)")])
    analyzer = DependencyAnalyzer()
    graph = analyzer.analyze([t1, t2])
    b1 = t2.subtasks[0]
    assert graph[b1.id] == {t1.id}
    assert b1.status == TaskStatus.BLOCKED
    assert t2.status == TaskStatus.TODO 