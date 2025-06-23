# TaskMaster NextGeneration - Agent de Gestion de Tâches Avancé

## 1. Description du Projet

`TaskMaster NextGeneration` est un agent Python autonome conçu pour orchestrer des tâches complexes en faisant appel à un écosystème d'agents spécialisés. Il est doté d'une intelligence artificielle pour comprendre le langage naturel, analyser la faisabilité des requêtes et valider les résultats produits par les autres agents.

### Fonctionnalités Clés

*   **Compréhension du Langage Naturel :** Interprète les demandes des utilisateurs pour les transformer en tâches structurées.
*   **Découverte Dynamique d'Agents :** Scanne en temps réel le répertoire `/agents` pour découvrir les agents disponibles et leurs compétences (`capabilities`).
*   **Analyse de Faisabilité :** Évalue si les agents et les compétences nécessaires pour une tâche sont disponibles avant de l'accepter.
*   **Orchestration de Tâches :** Décompose les tâches complexes en sous-tâches et les assigne aux agents appropriés (fonctionnalité en cours de développement).
*   **Validation Anti-Hallucination :** Analyse les résultats des agents pour en vérifier la cohérence et la plausibilité.
*   **Logging et Rapports :** Génère des logs d'activité détaillés et des rapports de tâche au format JSON pour chaque mission.

## 2. Comment Utiliser

### Prérequis

*   Python 3.10+
*   Les dépendances listées dans `requirements.txt` (s'il y en a un).

### Lancer le Test Fonctionnel

Le script `run_functional_test.py` a été créé pour valider le cycle de vie complet de l'agent. Pour l'exécuter, lancez la commande suivante depuis la racine du projet (`C:/Dev/nextgeneration`):

```bash
python 20250620_projet_taskmanager/TASKMASTER_PRODUCTION_READY/tests/run_functional_test.py
```

Ce script va :
1.  Démarrer une instance de l'agent `TaskMaster`.
2.  Lui soumettre une tâche de "refactoring" en langage naturel.
3.  Attendre que la tâche soit (simulée comme) complétée.
4.  Arrêter proprement l'agent.

Un message `🎉 Test fonctionnel terminé avec succès!` indiquera que tout s'est bien déroulé.

## 3. Structure des Répertoires de Sortie

Après l'exécution du test, les répertoires suivants seront créés dans `TASKMASTER_PRODUCTION_READY/` :

*   **`logs/`**: Contient les journaux d'activité détaillés de chaque instance de l'agent.
    *   `.../logs/agents/taskmaster_{ID_AGENT}/taskmaster_activity.log`
*   **`reports/`**: Contient les rapports JSON finaux pour chaque tâche exécutée.
    *   `.../reports/taskmaster_{ID_AGENT}/task_report_{ID_TACHE}.json`

Ces fichiers sont essentiels pour le débogage, l'audit et l'analyse des performances de l'agent. 