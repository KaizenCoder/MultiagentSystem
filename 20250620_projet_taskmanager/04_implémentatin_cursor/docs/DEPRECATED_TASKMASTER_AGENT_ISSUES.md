# Rapport d'Incidents et Plan d'Action pour l'Agent TaskMaster

**Date:** 2025-06-23
**Auteur:** IA Gemini
**Statut:** Analyse en cours

Ce document recense les problèmes critiques empêchant le bon fonctionnement et la validation de l'agent `agents/taskmaster_agent.py`.

---

## 1. Problème Critique : Échec de Chargement des Agents Spécialisés

La fonctionnalité de découverte dynamique des agents (`_discover_available_agents`) fonctionne, mais elle révèle que la majorité des agents dans le répertoire `/agents` sont défectueux et ne peuvent être chargés.

### Constat

Lors du démarrage, le `TaskMaster` tente de charger tous les fichiers `agent_*.py` mais échoue pour un grand nombre d'entre eux.

### Liste des Agents Défectueux et Erreurs Associées

| Fichier de l'Agent                             | Type d'Erreur              | Détail                                                       |
| ---------------------------------------------- | -------------------------- | ------------------------------------------------------------ |
| `agent_109_specialiste_planes.py`              | `IndentationError`         | `expected an indented block after class definition`          |
| `agent_110_documentaliste_expert.py`           | `IndentationError`         | `unexpected indent`                                          |
| `agent_111_auditeur_qualite.py`                | `IndentationError`         | `expected an indented block after 'try' statement`         |
| `agent_111_auditeur_qualite_sprint3.py`        | `TypeError`                | `__init__() missing 1 required positional argument: 'agent_type'` |
| `agent_12_backup_manager.py`                   | `IndentationError`         | `expected an indented block after function definition`     |
| `agent_13_specialiste_documentation.py`        | `IndentationError`         | `expected an indented block after function definition`     |
| `agent_14_specialiste_workspace.py`            | `IndentationError`         | `expected an indented block after function definition`     |
| `agent_18_auditeur_securite.py`                | `ModuleNotFoundError`      | `No module named 'agent_config'`                             |
| `... (et 20 autres agents)`                    | `Syntax/Import Errors`     | (Liste complète dans les logs du test)                       |

### Conséquence

Le `TaskMaster` ne dispose que d'un sous-ensemble très limité des capacités prévues, ce qui rend la plupart des tâches complexes infaisables.

---

## 2. Problème Majeur : Logique de Classification des Tâches Ambiguë

La méthode `_classify_task_type` est trop simpliste et conduit à des classifications erronées.

### Constat

La classification se base sur une recherche de mots-clés dans un dictionnaire, où l'ordre de parcours est déterminant.

**Exemple concret :**
- La requête de test : `"Refactorise le module authentification pour améliorer la clarté"`
- Le mot-clé `"améliorer"` appartient à `TaskType.OPTIMIZATION`.
- Le mot-clé `"refactorise"` appartient à `TaskType.REFACTORING`.

Comme `OPTIMIZATION` est vérifié avant `REFACTORING`, la tâche est incorrectement classifiée comme une optimisation.

```python
# Extrait de taskmaster_agent.py

def _classify_task_type(self, doc) -> TaskType:
    """Classifie le type de tâche"""
    text = doc.text
    
    # L'itération sur le dictionnaire dépend de l'ordre de déclaration
    for task_type, keywords in self.task_classifier.items():
        if any(keyword in text for keyword in keywords):
            return task_type # Retourne la première correspondance trouvée
    
    return TaskType.ANALYSIS
```

### Conséquence

Le `TaskMaster` demande des capacités (`performance_profiling`, etc.) qui ne correspondent pas à l'intention réelle de la requête (refactoring), menant au rejet de la tâche.

---

## 3. Plan d'Action Recommandé

Pour rendre le `TaskMaster` robuste et prêt pour la production, les actions suivantes sont nécessaires :

1.  **Phase 1 (Correction des Agents) :**
    -   **Action :** Examiner et corriger systématiquement chaque agent défectueux dans le répertoire `/agents`.
    -   **Objectif :** Assurer que tous les agents puissent être chargés sans erreur de syntaxe ou d'importation.

2.  **Phase 2 (Amélioration de la Classification) :**
    -   **Action :** Remplacer la logique de classification par un système plus intelligent.
    -   **Suggestions :**
        -   Utiliser un système de poids pour les mots-clés.
        -   Donner la priorité au verbe d'action principal de la phrase.
        -   Analyser les dépendances entre mots-clés (ex: "refactoriser pour améliorer" doit être un refactoring).
    -   **Objectif :** Obtenir une classification fiable de l'intention de l'utilisateur.

3.  **Phase 3 (Validation Complète) :**
    -   **Action :** Ré-exécuter le script `tests/test_taskmaster_lifecycle.py` avec une variété de requêtes.
    -   **Objectif :** Valider que les tâches sont correctement classifiées et assignées aux agents disposant des bonnes capacités. 