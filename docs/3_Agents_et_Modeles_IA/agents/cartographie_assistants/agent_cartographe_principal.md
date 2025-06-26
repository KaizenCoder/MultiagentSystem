# Agent : AgentCartographePrincipal (ACP)

**Version :** 0.1.0
**Date de création :** YYYY-MM-DD
**Auteur :** IA
**Statut :** En développement

## 1. Description Générale

L'Agent Cartographe Principal (ACP) est l'orchestrateur de l'équipe des agents assistants dédiés à la cartographie et à l'analyse de la synchronisation entre le code source des agents et leur documentation.

Son rôle est de coordonner les actions des agents suivants :
- **`AgentLecteurWorkflow (ALW)`** : Pour lire et interpréter le fichier `WORKFLOW_SUIVI_AGENTS.md` et en extraire la liste des agents à traiter ainsi que leurs informations de base (noms de script, noms de documentation).
- **`AgentAnalyseurCodePython (AACP)`** : Pour analyser statiquement chaque fichier de code Python d'agent.
- **`AgentAnalyseurDocumentationMarkdown (AADM)`** : Pour analyser chaque fichier de documentation Markdown associé.
- **`AgentComparateurSynchroniseur (ACS)`** : Pour comparer les données extraites par l'AACP et l'AADM, identifier les écarts et générer un rapport.

L'ACP est responsable de piloter le processus complet, de la lecture du workflow initial à la génération (simulée pour l'instant) d'une mise à jour de la table de cartographie dans `SUIVI_MIGRATION_AGENTS.md`.

## 2. Objectifs

- Orchestrer le flux de travail de la cartographie automatisée.
- Gérer les appels séquentiels aux agents assistants pour chaque agent cible.
- Collecter et agréger les résultats des analyses et des comparaisons.
- Fournir une vue d'ensemble de l'état de synchronisation code/documentation pour l'ensemble des agents.
- (À terme) Mettre à jour automatiquement la section de cartographie dans `SUIVI_MIGRATION_AGENTS.md`.

## 3. Dépendances Clés (Agents Assistants)

L'ACP est initialisé avec des instances des agents suivants :
- `AgentLecteurWorkflow`
- `AgentAnalyseurCodePython`
- `AgentAnalyseurDocumentationMarkdown`
- `AgentComparateurSynchroniseur`

Chacun de ces assistants doit exposer une méthode `execute_task(task_name: str, task_params: Dict[str, Any])`.

## 4. Fonctionnalités Clés (`get_capabilities`)

L'agent expose les fonctionnalités suivantes :

- **`cartographier_tous_les_agents`** :
    - **Description :** Exécute le processus complet de cartographie. D'abord, il utilise l'ALW pour obtenir la liste des agents à partir du fichier `WORKFLOW_SUIVI_AGENTS.md`. Ensuite, pour chaque agent identifié, il utilise l'ACS (qui à son tour utilise AACP et AADM) pour analyser le code et la documentation, comparer les informations, et générer un rapport d'écarts.
    - **Paramètres d'entrée :** `{"chemin_workflow_file": "path/to/WORKFLOW_SUIVI_AGENTS.md", "base_path_agents": "agents/", "base_path_docs": "docs/3_Agents_et_Modeles_IA/agents/"}`.
    - **Résultat attendu :** Une liste de dictionnaires, chaque dictionnaire représentant le résultat de la cartographie pour un agent, incluant les données du code, de la doc, les écarts, et le rapport d'écarts.

- **`cartographier_agent_specifique`** :
    - **Description :** Permet de lancer le processus d'analyse et de comparaison pour un seul agent spécifié par les chemins de son script Python et de son fichier Markdown.
    - **Paramètres d'entrée :** `{"chemin_script_agent": "path/to/agent.py", "chemin_doc_agent": "path/to/agent.md"}`.
    - **Résultat attendu :** Un dictionnaire contenant les données du code, de la doc, les écarts, et le rapport d'écarts pour l'agent spécifié.

- **`mettre_a_jour_suivi_migration`** :
    - **Description :** (Actuellement simulée) Prend les résultats de `cartographier_tous_les_agents` et met à jour la section de cartographie (Section 3) du fichier `SUIVI_MIGRATION_AGENTS.md` avec les informations déduites sur la conformité au Pattern Factory (PF Conf.) et les fonctionnalités manquantes/écarts de documentation.
    - **Paramètres d'entrée :** `{"resultats_cartographie": [...], "chemin_fichier_suivi": "agents_migration_workspace/SUIVI_MIGRATION_AGENTS.md"}`.
    - **Résultat attendu :** Un statut de succès ou d'échec de l'opération (simulée).

## 5. Méthode `execute_task`

L'agent implémente `execute_task(task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]` qui dispatche vers les méthodes correspondantes en fonction de `task_name`.

## 6. Processus de Cartographie Globale (`cartographier_tous_les_agents`)

1.  Appel à `ALW.execute_task("analyser_workflow", ...)` pour obtenir la liste des agents.
2.  Pour chaque agent retourné par ALW :
    a.  Construire les chemins absolus/relatifs corrects vers le script Python et le fichier Markdown.
    b.  Vérifier l'existence des fichiers. Si le script Python est introuvable, l'agent est ignoré avec une erreur. Si la documentation est introuvable, une note est consignée et l'analyse du code est tentée.
    c.  Appel à `self.cartographier_agent_specifique(chemin_script, chemin_doc)` qui exécute :
        i.  `ACS.execute_task("comparer_code_et_doc", ...)` (ACS appelle AACP et AADM).
        ii. `ACS.execute_task("generer_rapport_ecarts", ...)`.
    d.  Collecter les résultats.
3.  Retourner la liste agrégée des résultats de cartographie.

## 7. Structure du Code (Simplifiée)

```python
class AgentCartographePrincipal:
    __version__ = "0.1.0"

    def __init__(self, lecteur_workflow, analyseur_code, analyseur_doc, comparateur_sync):
        # Initialisation des assistants
        # ...

    def get_capabilities(self) -> Dict[str, Any]:
        # ...

    def _obtenir_liste_agents_du_workflow(self, chemin_workflow_file: str) -> Optional[List[Dict[str, str]]]:
        # Appelle ALW.execute_task("analyser_workflow", ...)
        # ...

    def cartographier_agent_specifique(self, chemin_script_agent: str, chemin_doc_agent: str) -> Optional[Dict[str, Any]]:
        # Appelle ACS.execute_task("comparer_code_et_doc", ...)
        # Appelle ACS.execute_task("generer_rapport_ecarts", ...)
        # ...

    def cartographier_tous_les_agents(self, chemin_workflow_file: str, base_path_agents: str, base_path_docs: str) -> List[Dict[str, Any]]:
        # Boucle sur les agents du workflow
        # Appelle cartographier_agent_specifique pour chacun
        # ...

    def mettre_a_jour_suivi_migration(self, resultats_cartographie: List[Dict[str, Any]], chemin_fichier_suivi: str) -> bool:
        # Logique (simulée) pour mettre à jour le fichier Markdown SUIVI_MIGRATION_AGENTS.md
        # ...
        return True # Simule succès

    def execute_task(self, task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]:
        # Dispatch vers les méthodes concernées
        # ...

if __name__ == '__main__':
    # Exemple d'utilisation avec des mocks pour ALW, AACP, AADM, ACS
    # Création de dummy files pour les tests
    # ...
```

## 8. Journal des Modifications

- **YYYY-MM-DD (v0.1.0) :** Création initiale de l'agent. Implémentation de l'orchestration de base pour la cartographie de tous les agents et d'un agent spécifique. La mise à jour du fichier de suivi est simulée (affiche les informations à mettre à jour).

## 9. Pistes d'Amélioration Futures

- Implémentation réelle de la mise à jour de `SUIVI_MIGRATION_AGENTS.md` (parsing et écriture Markdown robustes).
- Gestion plus fine des erreurs et des cas limites (ex: agent existant mais sans fichier .py ou .md listé).
- Parallélisation possible des analyses d'agents indépendants (si pertinent et si les agents assistants sont thread-safe ou peuvent être instanciés multiples fois).
- Interface de configuration pour les chemins de base, le fichier workflow, etc.
- Amélioration de la logique de déduction des informations à inscrire dans le suivi (PF Conf., Fonc. Manquantes) basée sur les rapports d'écarts de l'ACS. 