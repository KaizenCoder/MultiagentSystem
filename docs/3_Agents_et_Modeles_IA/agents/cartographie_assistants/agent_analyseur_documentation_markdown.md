# Agent : AgentAnalyseurDocumentationMarkdown (AADM)

**Version :** 0.1.0
**Date de création :** YYYY-MM-DD
**Auteur :** IA
**Statut :** En développement

## 1. Description Générale

L'Agent Analyseur de Documentation Markdown (AADM) est un composant de l'équipe d'agents cartographes. Son rôle est d'analyser le contenu des fichiers de documentation Markdown (`.md`) associés aux agents.

Il vise à extraire des informations structurées telles que :
- Le titre principal du document (généralement le premier H1).
- La version de l'agent telle que déclarée dans la documentation.
- La structure des sections (H1, H2, H3, etc.) et leur contenu textuel.
- Les capacités de l'agent telles que décrites (par exemple, dans une section "Fonctionnalités Clés" ou "Capacités").
- Potentiellement d'autres métadonnées pertinentes (auteur, date de modification, etc., si des conventions sont établies).

## 2. Objectifs

- Parser la structure des fichiers de documentation Markdown.
- Extraire les informations clés sur un agent à partir de sa documentation (version, capacités, description).
- Fournir ces informations structurées à l'Agent Comparateur Synchroniseur (ACS) pour qu'il puisse les comparer avec les informations extraites du code Python par l'AACP.
- Aider à identifier les désynchronisations entre le code et la documentation.

## 3. Fonctionnalités Clés (`get_capabilities`)

L'agent expose les fonctionnalités suivantes :

- **`analyser_fichier_markdown`** :
    - **Description :** Analyse un fichier Markdown spécifié par son chemin et retourne un dictionnaire structuré contenant les informations extraites (titre, sections, version documentée, etc.).
    - **Paramètres d'entrée :** `{"chemin_fichier": "path/to/agent_doc.md"}`
    - **Résultat attendu :** Un dictionnaire détaillé ou `None` en cas d'erreur.

- **`extraire_version_documentee`** :
    - **Description :** Tente d'extraire spécifiquement la version de l'agent telle que mentionnée dans le fichier Markdown (par exemple, à partir d'un champ "**Version :** X.Y.Z").
    - **Paramètres d'entrée :** `{"chemin_fichier": "path/to/agent_doc.md"}`
    - **Résultat attendu :** Une chaîne de caractères représentant la version, ou `None` si non trouvée.

## 4. Méthode `execute_task`

L'agent implémente `execute_task(task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]` :

- Si `task_name` est `"analyser_fichier_markdown"`:
    - Appelle `self.analyser_fichier_markdown(task_params["chemin_fichier"])`.
- Si `task_name` est `"extraire_version_documentee"`:
    - Appelle `self.extraire_version_documentee(task_params["chemin_fichier"])`.

## 5. Dépendances Externes Majeures

- `re` (expressions régulières) : Pour l'identification de motifs spécifiques (titres, version).
- `pathlib` : Pour la manipulation des chemins de fichiers.

## 6. Structure du Code (Simplifiée)

```python
class AgentAnalyseurDocumentationMarkdown:
    __version__ = "0.1.0"

    def __init__(self):
        # ...

    def get_capabilities(self) -> Dict[str, Any]:
        # ...

    def _parse_markdown_content(self, contenu: str) -> Dict[str, Any]:
        # Logique de parsing avec regex pour titres, version, sections
        # ...

    def analyser_fichier_markdown(self, chemin_fichier: str) -> Optional[Dict[str, Any]]:
        # Lit le fichier et appelle _parse_markdown_content
        # ...

    def extraire_version_documentee(self, chemin_fichier: str) -> Optional[str]:
        # Appelle analyser_fichier_markdown et retourne la version
        # ...

    def execute_task(self, task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]:
        # Dispatch vers les méthodes concernées
        # ...

if __name__ == '__main__':
    # Exemples d'utilisation
    # ...
```

## 7. Journal des Modifications

- **YYYY-MM-DD (v0.1.0) :** Création initiale de l'agent avec fonctionnalités de base pour l'analyse de la structure Markdown (titres, sections) et l'extraction de la version documentée.

## 8. Pistes d'Amélioration Futures

- Extraction plus fine des "capacités" et "descriptions de tâches" en se basant sur des sections nommées spécifiquement.
- Gestion des listes à puces et des tableaux pour extraire des données structurées.
- Comparaison de la structure des sections par rapport à un template attendu.
- Utilisation d'une bibliothèque de parsing Markdown plus robuste si les expressions régulières deviennent trop complexes (ex: `mistune`, `markdown-it-py`). 