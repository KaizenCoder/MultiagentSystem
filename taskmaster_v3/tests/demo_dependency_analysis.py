from taskmaster_v3.core.models import Task, TaskStatus
from taskmaster_v3.core.services import TaskService
from taskmaster_v3.modules.persistence.repository import InMemoryTaskRepository

# Création d'une hiérarchie de tâches avec dépendances explicites
root1 = Task(title="Préparer la base de données", description="")
root2 = Task(title="Développer l'API (dépend de: Préparer la base de données)", description="")
root3 = Task(title="Rédiger la documentation", description="après Développer l'API")
root4 = Task(title="Déployer en production", description="dépend de: Rédiger la documentation")

# Hiérarchie imbriquée
root5 = Task(title="Tests", description="", subtasks=[
    Task(title="Tests unitaires (dépend de: Développer l'API)", description=""),
    Task(title="Tests d'intégration (dépend de: Tests unitaires)", description="")
])

root_tasks = [root1, root2, root3, root4, root5]

# Instanciation du service
repo = InMemoryTaskRepository()
service = TaskService(repo)

graph = service.analyze_dependencies(root_tasks)

# Affichage du graphe de dépendances
print("Graphe de dépendances (id -> [ids dont il dépend]):")
for tid, deps in graph.items():
    print(f"{tid[:8]}... -> {[d[:8]+'...' for d in deps]}")

# Affichage des statuts
print("\nStatut des tâches :")
def print_status(task, indent=0):
    print("  "*indent + f"- {task.title} : {task.status.value}")
    for st in task.subtasks:
        print_status(st, indent+1)
for t in root_tasks:
    print_status(t) 