# Plan d'Action : Opérationnalisation de l'Agent TaskMaster

*   **Date de début :** 24/06/2025
*   **Objectif :** Rendre l'agent `taskmaster_agent.py` pleinement fonctionnel et exécutable dans son état actuel. Cela implique de corriger la gestion des chemins, d'implémenter les fonctions manquantes et de valider son fonctionnement via un script de test dédié.
*   **Méthodologie :** Suivi scrupuleux du cycle **M-T-D (Modification - Test - Documentation)** pour chaque étape. La collaboration se fera par instructions de copier-coller manuelles (je fournirai le code et les numéros de ligne, vous appliquerez les changements).

---

## 1. Contexte et Mission

Nous partons d'un script `agents/taskmaster_agent.py` restauré à son état d'origine. Le but est de le rendre robuste en externalisant ses dépendances (logs, data, reports) dans un répertoire de production dédié.

## 2. État Actuel

*   `agents/taskmaster_agent.py` est dans sa version originale, non modifiée.
*   Un répertoire de travail unique a été défini pour toutes les opérations et artéfacts générés par l'agent.

## 3. Répertoire de Travail Cible

Toutes les opérations (tests, logs, rapports, etc.) qui ne sont pas le code de l'agent lui-même doivent s'opérer dans le répertoire suivant :
`C:\Dev\nextgeneration\20250620_projet_taskmanager\TASKMASTER_PRODUCTION_READY`

Nous y créerons les sous-répertoires suivants au fur et à mesure : `/logs`, `/data`, `/reports`, `/tests`.

## 4. Méthodologie Impérative (Le Cycle M-T-D)

Chaque étape du plan suivra ce cycle :

1.  **Proposition de Modification :** Je décrirai la modification à apporter et fournirai le bloc de code exact à insérer/remplacer, en précisant les numéros de ligne du fichier `agents/taskmaster_agent.py`.
2.  **Validation et Application :** J'attendrai votre **"GO"** avant de continuer. Vous effectuerez le copier-coller.
3.  **Proposition de Test :** Je fournirai un script de test (ou une mise à jour) pour valider la modification.
4.  **Exécution & Analyse :** Vous exécuterez le test. J'analyserai les résultats (logs, fichiers créés) pour confirmer le succès de l'opération.
5.  **Proposition de Documentation :** Je fournirai le contenu pour documenter la modification et son test.
6.  **Validation Finale :** Nous validerons ensemble que l'étape est terminée avant de passer à la suivante.

## 5. Plan d'Action Détaillé

### **Phase 1 : Rendre le script robuste et autonome (Modification)**

L'objectif est de découpler le script de son emplacement et de s'assurer qu'il peut écrire dans le répertoire de travail cible.

*   **Étape 1.1 : Gestion dynamique des chemins**
    *   **Modification :** Remplacer le calcul de chemin relatif en début de fichier par une logique plus robuste qui définit une variable `PROJECT_ROOT` et configure les chemins des logs, data et reports pour qu'ils pointent vers notre répertoire de travail `TASKMASTER_PRODUCTION_READY`.
    *   **Impact :** `__init__`, `_verify_environment`, `_load_state`.

*   **Étape 1.2 : Implémentation de la sauvegarde des rapports**
    *   **Modification :** La méthode `_save_task_report` est référencée mais n'existe pas. Je fournirai le code complet de cette méthode à insérer au bon endroit. Elle sera configurée pour écrire les rapports dans `TASKMASTER_PRODUCTION_READY/reports`.
    *   **Impact :** Ajout d'une nouvelle méthode.

*   **Étape 1.3 : Ajout d'une méthode `shutdown`**
    *   **Modification :** Pour une terminaison propre, notamment du `ThreadPoolExecutor`, il est essentiel d'avoir une méthode `shutdown`. Je la fournirai.
    *   **Impact :** Ajout d'une nouvelle méthode.

### **Phase 2 : Valider le fonctionnement (Test)**

*   **Étape 2.1 : Création du script de test fonctionnel**
    *   **Test :** Je fournirai un script `run_functional_test.py` à placer dans `TASKMASTER_PRODUCTION_READY/tests`. Ce script importera l'agent, l'instanciera, lancera une tâche simple en langage naturel, attendra son exécution simulée, puis appellera `shutdown`.
    *   **Critère de succès :** Le script s'exécute sans erreur, et un fichier de log ainsi qu'un rapport de tâche sont correctement créés dans les répertoires `TASKMASTER_PRODUCTION_READY/logs` et `TASKMASTER_PRODUCTION_READY/reports`.

### **Phase 3 : Documenter la procédure (Documentation)**

*   **Étape 3.1 : Création du `README.md`**
    *   **Documentation :** Je fournirai le contenu d'un fichier `README.md` à créer à la racine de `TASKMASTER_PRODUCTION_READY`. Ce fichier expliquera comment lancer le test fonctionnel et quels sont les résultats attendus.

---

## Instruction Initiale

J'ai maintenant créé ce plan. J'attends votre validation **("GO")** pour vous proposer la première modification de la **Phase 1, Étape 1.1**. 