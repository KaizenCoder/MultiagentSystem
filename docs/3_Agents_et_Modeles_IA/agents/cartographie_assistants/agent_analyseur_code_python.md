# Agent : AgentAnalyseurCodePython (AACP)

**Version :** 0.1.0
**Date de création :** YYYY-MM-DD
**Auteur :** IA
**Statut :** En développement

## 1. Description Générale

L'Agent Analyseur de Code Python (AACP) est un composant spécialisé de l'équipe d'agents cartographes. Sa principale responsabilité est d'effectuer une analyse statique des fichiers de code source Python (`.py`). 

Il est conçu pour extraire des informations structurelles et sémantiques clés du code, telles que :
- Les modules importés.
- Les classes définies (nom, docstrings, méthodes, attributs de base).
- Les fonctions globales (nom, docstrings, arguments).
- Le docstring au niveau du module.
- La variable `__version__` si elle est explicitement définie au niveau du module ou de la classe principale.

L'AACP peut également effectuer des vérifications de conformité de base, notamment pour déterminer si un agent semble adhérer au Pattern Factory standard utilisé dans ce projet (présence des méthodes `get_capabilities` et `execute_task`, et d'un attribut `__version__`).

## 2. Objectifs

- Fournir une analyse détaillée de la structure des fichiers de code Python.
- Identifier les éléments clés comme les classes, fonctions, et imports.
- Extraire les docstrings pour faciliter la compréhension du code.
- Détecter la version déclarée d'un agent.
- Aider à évaluer la conformité préliminaire au Pattern Factory.
- Servir de brique de base pour l'Agent Comparateur Synchroniseur (ACS) en lui fournissant les données extraites du code.

## 3. Fonctionnalités Clés (`get_capabilities`)

L'agent expose les fonctionnalités suivantes via sa méthode `get_capabilities` :

- **`analyser_fichier_python`** :
    - **Description :** Analyse un fichier Python spécifié par son chemin et retourne un dictionnaire structuré contenant les informations extraites (imports, classes, fonctions, docstrings, version).
    - **Paramètres d'entrée :** `{"chemin_fichier": "path/to/agent.py"}`
    - **Résultat attendu :** Un dictionnaire détaillé ou `None` en cas d'erreur.

- **`verifier_conformite_pattern_factory`** :
    - **Description :** Analyse un fichier Python pour vérifier la présence des éléments clés du Pattern Factory (`get_capabilities`, `execute_task`, `__version__`).
    - **Paramètres d'entrée :** `{"chemin_fichier": "path/to/agent.py"}`
    - **Résultat attendu :** Un dictionnaire indiquant la conformité (`True`/`False`), des détails sur les vérifications, et la version supposée du Pattern Factory si trouvée.

## 4. Méthode `execute_task`

L'agent implémente la méthode `execute_task(task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]` pour orchestrer l'appel à ses fonctionnalités :

- Si `task_name` est `"analyser_fichier_python"`:
    - Appelle `self.analyser_fichier_python(task_params["chemin_fichier"])`.
    - Retourne `{"status": "succes", "resultat": ...}` ou `{"status": "erreur", "message": ...}`.
- Si `task_name` est `"verifier_conformite_pattern_factory"`:
    - Appelle `self.verifier_conformite_pattern_factory(task_params["chemin_fichier"])`.
    - Retourne `{"status": "succes", "resultat": ...}` ou `{"status": "erreur", "message": ...}`.

## 5. Dépendances Externes Majeures

- `ast` (Abstract Syntax Trees) : Utilisé pour parser le code Python et naviguer dans sa structure.

## 6. Structure du Code (Simplifiée)

```python
class AgentAnalyseurCodePython:
    __version__ = "0.1.0"

    def __init__(self):
        # ... initialisation du logger ...

    def get_capabilities(self) -> Dict[str, Any]:
        # ... retourne la description des tâches ...

    def analyser_fichier_python(self, chemin_fichier: str) -> Optional[Dict[str, Any]]:
        # ... logique d'analyse avec ast ...
        # Extrait imports, classes (nom, docstring, méthodes), fonctions (nom, docstring, args), version
    
    def _is_in_class(self, node: ast.AST, tree: ast.AST) -> bool:
        # Helper pour la méthode analyser_fichier_python

    def verifier_conformite_pattern_factory(self, chemin_fichier: str) -> Dict[str, Any]:
        # ... logique de vérification de get_capabilities, execute_task, __version__ ...

    def execute_task(self, task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]:
        # ... dispatch vers les méthodes correspondantes ...

if __name__ == '__main__':
    # ... exemples d'utilisation ...
```

## 7. Journal des Modifications

- **YYYY-MM-DD (v0.1.0) :** Création initiale de l'agent avec fonctionnalités de base pour l'analyse de structure et la vérification de conformité au Pattern Factory.

## 8. Pistes d'Amélioration Futures

- Analyse plus fine des attributs de classe.
- Détection des décorateurs.
- Extraction des types (type hints).
- Analyse de la complexité cyclomatique (basique).
- Meilleure heuristique pour identifier la classe principale d'un agent.
- Prise en charge de l'analyse de snippets de code en mémoire (pas seulement des fichiers). 