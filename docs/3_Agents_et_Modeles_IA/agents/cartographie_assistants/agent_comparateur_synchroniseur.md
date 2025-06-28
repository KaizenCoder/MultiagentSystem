# Agent : AgentComparateurSynchroniseur (ACS)

**Version :** 0.1.0
**Date de création :** YYYY-MM-DD
**Auteur :** IA
**Statut :** En développement

## 1. Description Générale

L'Agent Comparateur Synchroniseur (ACS) est un agent central de l'équipe de cartographie. Son rôle principal est de prendre les informations structurées extraites du code Python d'un agent (fournies par l'`AgentAnalyseurCodePython - AACP`) et celles extraites de sa documentation Markdown (fournies par l'`AgentAnalyseurDocumentationMarkdown - AADM`), puis de les comparer pour identifier les divergences et les incohérences.

L'ACS génère ensuite un rapport détaillé de ces écarts, qui peut être utilisé pour guider les efforts de synchronisation entre le code et sa documentation.

## 2. Objectifs

- Orchestrer l'appel à l'AACP et à l'AADM pour obtenir les analyses d'un agent cible.
- Comparer de manière systématique les éléments clés : version, docstrings/descriptions, noms de fonctions/méthodes, structure des capacités, etc.
- Identifier et qualifier les types d'écarts (ex: version désynchronisée, docstring manquant, fonctionnalité non documentée, documentation obsolète).
- Générer un rapport clair et exploitable (par défaut en Markdown) des écarts constatés.
- Fournir la base pour des actions de synchronisation manuelles ou semi-automatisées.

## 3. Dépendances Clés (Agents Assistants)

- **`AgentAnalyseurCodePython (AACP)`** : L'ACS dépend de l'AACP pour obtenir une analyse structurée du fichier de code Python de l'agent cible.
- **`AgentAnalyseurDocumentationMarkdown (AADM)`** : L'ACS dépend de l'AADM pour obtenir une analyse structurée du fichier de documentation Markdown de l'agent cible.

L'ACS est initialisé avec des instances de ces deux agents.

## 4. Fonctionnalités Clés (`get_capabilities`)

L'agent expose les fonctionnalités suivantes :

- **`comparer_code_et_doc`** :
    - **Description :** Prend les chemins d'un fichier Python et de son fichier Markdown associé, appelle les analyseurs respectifs (AACP, AADM), et compare les résultats.
    - **Paramètres d'entrée :** `{"chemin_fichier_python": "path/to/agent.py", "chemin_fichier_markdown": "path/to/agent_doc.md"}`
    - **Résultat attendu :** Un dictionnaire contenant les données brutes du code, les données brutes de la documentation, et une liste structurée des écarts identifiés. Retourne un statut "erreur" si l'une des analyses échoue.

- **`generer_rapport_ecarts`** :
    - **Description :** Prend le résultat de la tâche `comparer_code_et_doc` et génère un rapport formaté (par défaut en Markdown) qui détaille les écarts.
    - **Paramètres d'entrée :** `{"resultat_comparaison": {...}, "format_rapport": "markdown"}` (le `resultat_comparaison` est la sortie de la tâche précédente).
    - **Résultat attendu :** Une chaîne de caractères contenant le rapport, ou `None` en cas d'erreur ou si aucun écart n'est à rapporter.

## 5. Méthode `execute_task`

L'agent implémente `execute_task(task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]` :

- Si `task_name` est `"comparer_code_et_doc"`:
    - Appelle `self.comparer_code_et_doc(task_params["chemin_fichier_python"], task_params["chemin_fichier_markdown"])`.
- Si `task_name` est `"generer_rapport_ecarts"`:
    - Appelle `self.generer_rapport_ecarts(task_params["resultat_comparaison"], task_params.get("format_rapport", "markdown"))`.

## 6. Types d'Écarts Gérés (Exemples)

- **Version :** Différence entre `__version__` dans le code et la version déclarée dans la documentation.
- **Docstring Module vs Description Générale :** Incohérences ou différences significatives entre le docstring principal du fichier Python et la section de description générale du fichier Markdown (utilisation de `difflib`).
- *Autres comparaisons (à développer) :* Présence/absence de fonctions/méthodes, cohérence des signatures (simplifié), etc.

## 7. Structure du Code (Simplifiée)

```python
class AgentComparateurSynchroniseur:
    __version__ = "0.1.0"

    def __init__(self, analyseur_code_agent, analyseur_doc_agent):
        self.analyseur_code = analyseur_code_agent
        self.analyseur_doc = analyseur_doc_agent
        # ...

    def get_capabilities(self) -> Dict[str, Any]:
        # ...

    def comparer_code_et_doc(self, chemin_fichier_python: str, chemin_fichier_markdown: str) -> Dict[str, Any]:
        # Appelle AACP.execute_task("analyser_fichier_python", ...)
        # Appelle AADM.execute_task("analyser_fichier_markdown", ...)
        # Logique de comparaison des résultats (version, docstrings, etc.)
        # ...
        return {"status": "succes", "donnees_code": ..., "donnees_doc": ..., "ecarts": [...]}

    def generer_rapport_ecarts(self, resultat_comparaison: Dict[str, Any], format_rapport: str = "markdown") -> Optional[str]:
        # Formate les écarts en Markdown ou autre format
        # ...
        return "rapport_formate"

    def execute_task(self, task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]:
        # Dispatch vers les méthodes concernées
        # ...

if __name__ == '__main__':
    # Exemples d'utilisation avec des mocks pour AACP et AADM
    # ...
```

## 8. Journal des Modifications

- **YYYY-MM-DD (v0.1.0) :** Création initiale de l'agent. Implémentation de la comparaison de version et de la comparaison de base du docstring de module vs description générale (via `difflib`). Génération de rapport Markdown simple.

## 9. Pistes d'Amélioration Futures

- Comparaison plus fine des sections (ex: "Capacités", "Fonctionnalités") en parsant leur contenu pour identifier des éléments spécifiques.
- Comparaison des signatures de fonctions/méthodes (noms des arguments, types si disponibles).
- Détection des fonctions/méthodes présentes dans le code mais non documentées, et vice-versa.
- Suggestions automatiques ou semi-automatiques pour la synchronisation (par exemple, proposer de copier un docstring manquant).
- Prise en charge de différents niveaux de "criticité" pour les écarts.
- Intégration plus poussée avec l'Agent Cartographe Principal pour le reporting. 