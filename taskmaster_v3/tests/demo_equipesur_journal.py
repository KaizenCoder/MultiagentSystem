from taskmaster_v3.core.services import TaskService
from taskmaster_v3.modules.persistence.repository import InMemoryTaskRepository

# Copie enrichie du journal pour la démonstration
journal_text = '''
### Volet 1 : Classification des erreurs & Routage (Adaptateur)
* **Date :** 2024-06-24 00:27 CET
* **Analyse Comparative :**
  * L'Adaptateur actuel ne distingue pas les types d'erreurs.
  * Limite : sans classification, la boucle de réparation tourne à vide.
* **Proposition :**
  1. Ajouter une fonction `classify_exception`.
  2. Modifier le coordinateur (dépend de: Ajouter une fonction `classify_exception`)
    * Adapter l'Adaptateur (dépend de: Modifier le coordinateur)
    * Tester le workflow complet (après Adapter l'Adaptateur)
* **Décision avant test :** GO
* **Résultat du Test :** ÉCHEC initial, puis SUCCÈS (après Tester le workflow complet)
* **Décision Finale :** GO

### Volet 2 : Amélioration du moteur de correction d'indentation
* **Proposition :**
  1. Remplacer la logique existante.
  2. Modifier la méthode `execute_task` (dépend de: Remplacer la logique existante)
    * Valider la correction (après Modifier la méthode `execute_task`)
'''

repo = InMemoryTaskRepository()
service = TaskService(repo)

tasks = service.parser.parse_text_to_tasks(journal_text)
graph = service.analyze_dependencies(tasks)

print("Hiérarchie de tâches détectée :")
def print_tree(task, indent=0):
    print("  "*indent + f"- {task.title} [{task.status.value}]")
    for st in task.subtasks:
        print_tree(st, indent+1)
for t in tasks:
    print_tree(t)

def shortid(s):
    return s[:8]+"..."
print("\nGraphe de dépendances (id -> [ids dont il dépend]):")
for tid, deps in graph.items():
    if deps:
        print(f"{shortid(tid)} -> {[shortid(d) for d in deps]}") 