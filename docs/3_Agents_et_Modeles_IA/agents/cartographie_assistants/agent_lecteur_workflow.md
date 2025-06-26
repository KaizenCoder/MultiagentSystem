# Agent Lecteur Workflow (ALW)

## 1. Identification

- **Nom :** Agent Lecteur Workflow
- **Identifiant :** `agent_lecteur_workflow`
- **Version :** 0.1.0
- **Répertoire Code :** `agents/cartographie_assistants/agent_lecteur_workflow.py`
- **Responsable Principal :** IA Équipe de Développement et Maintenance Stratégique (Phase A)
- **Contact Technique :** `#canal-agents-cartographes`

## 2. Description Générale

L'Agent Lecteur Workflow (ALW) est un agent assistant spécialisé dans la lecture et l'analyse du fichier `agents/WORKFLOW_SUIVI_AGENTS.md`. Son rôle principal est d'extraire de manière structurée la liste de tous les agents mentionnés dans ce fichier ainsi que leur statut de complétion (par exemple, "Terminé", "À faire").

Il sert de brique de base pour l'équipe d'agents cartographes en fournissant une source de vérité programmatique sur l'état d'avancement général des agents du projet.

## 3. Objectifs et Missions

- **Lire le Fichier Workflow :** Accéder en lecture au fichier `agents/WORKFLOW_SUIVI_AGENTS.md`.
- **Parser le Contenu Markdown :** Analyser la structure du fichier Markdown pour identifier les lignes décrivant des agents et leur statut (basé sur les cases à cocher `- [ ]` ou `- [x]`).
- **Extraire les Informations :** Pour chaque agent identifié, extraire :
    - Le nom du fichier de l'agent (ex: `agent_xx_nom.py`).
    - Le statut brut (ex: `[x]`, `[ ]`).
    - Un statut interprété (ex: "Terminé", "À faire").
    - Optionnellement, une description si présente sur la même ligne.
    - Le numéro de la ligne où l'information a été trouvée.
- **Fournir un Résultat Structuré :** Retourner les informations extraites sous forme d'une liste de dictionnaires facilement exploitable par d'autres agents (notamment l'`AgentCartographePrincipal`).

## 4. Fonctionnalités Clés (Conformité Pattern Factory)

L'agent respecte le Pattern Factory de base et expose les méthodes suivantes :

- **`__init__(self, agent_id: str, workflow_file_path: Optional[str])`**: Initialise l'agent. Peut prendre un chemin par défaut vers le fichier workflow.
- **`startup()`** : Initialise l'agent.
- **`health_check()`** : Retourne l'état de santé de l'agent et sa version.
- **`execute_task(task_details: Dict)`** : Point d'entrée principal.
    - Action supportée : `analyser_workflow`.
    - `params` attendus pour `analyser_workflow` : `{"workflow_file_path": "chemin/vers/WORKFLOW_SUIVI_AGENTS.md"}`. Si non fourni dans `params`, utilise le chemin fourni à l'initialisation.
- **`analyser_workflow(workflow_file_path: Optional[str])`** : Méthode principale effectuant la lecture et l'analyse du fichier.
- **`_interpret_status(raw_status: str)`** : Méthode interne pour convertir le statut brut (ex: 'x') en un statut interprété (ex: "Terminé").
- **`shutdown()`** : Arrête l'agent.

## 5. Formats d'Entrée et de Sortie Clés

- **Entrée pour `execute_task` (action `analyser_workflow`) :**
  ```json
  {
    "action": "analyser_workflow",
    "params": {
      "workflow_file_path": "agents/WORKFLOW_SUIVI_AGENTS.md"
    }
  }
  ```
  Ou, si `workflow_file_path` a été configuré à l'initialisation de l'agent :
  ```json
  {
    "action": "analyser_workflow",
    "params": {}
  }
  ```

- **Sortie de `execute_task` (exemple succès) :**
  ```json
  {
    "status": "succès",
    "action": "analyser_workflow",
    "message": "Analyse du workflow agents/WORKFLOW_SUIVI_AGENTS.md terminée.",
    "data": [
      {
        "nom_agent": "agent_01_coordinateur.py",
        "statut_brut": "[x]",
        "statut_interprete": "Terminé",
        "description": "Terminé et validé",
        "ligne": 5
      },
      {
        "nom_agent": "agent_02_architecte.py",
        "statut_brut": "[ ]",
        "statut_interprete": "À faire",
        "description": "En cours de développement",
        "ligne": 6
      }
      // ... autres agents
    ]
  }
  ```
- **Sortie de `execute_task` (exemple erreur) :**
  ```json
  {
    "status": "erreur",
    "message": "Paramètre 'workflow_file_path' manquant pour l'action 'analyser_workflow'.",
    "data": []
  }
  ```

## 6. Dépendances et Prérequis

- Modules Python standards : `re`, `logging`, `pathlib`, `typing`.
- Le fichier `agents/WORKFLOW_SUIVI_AGENTS.md` doit exister et être accessible en lecture avec un format cohérent (lignes d'agents commençant par `- [status] nom_agent.py ...`).

## 7. Configuration

- L'agent peut être initialisé avec un chemin par défaut vers le fichier `WORKFLOW_SUIVI_AGENTS.md`.
- Le niveau de logging est configurable via le module `logging` standard.

## 8. Journal des Modifications de cette Documentation (.md)

- **v0.1.0 (YYYY-MM-DD) :** Création initiale de la documentation pour l'Agent Lecteur Workflow (ALW). 