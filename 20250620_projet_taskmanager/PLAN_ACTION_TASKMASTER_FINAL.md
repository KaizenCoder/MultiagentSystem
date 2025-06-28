# Plan d'Action Final – Construction de l'Agent TaskMaster Unifié

*   **Version :** 4.0 (Stratégie de Construction)
*   **Date :** 23/06/2025
*   **Contexte :** Suite à un pivot stratégique, l'objectif est de **construire un nouvel agent `taskmaster_final.py`** dans le répertoire `/agents`. Cet agent doit être autonome, robuste et s'inspirer des meilleures pratiques architecturales découvertes, tout en s'intégrant parfaitement à l'écosystème des agents existants. La méthodologie M-T-D (Modifier-Tester-Documenter) sera appliquée de manière stricte.

---

## 1. Contexte Global & Mission

Construire un agent TaskMaster de production, `agents/taskmaster_final.py`, qui orchestrera les autres agents pour accomplir des missions complexes.

## 2. État Actuel

*   La stratégie de construction d'un nouvel agent est actée.
*   Nous disposons de 3 agents spécialisés et validés (`agent_13`, `agent_14`, `agent_16`) qui serviront de cibles pour les tests de délégation.
*   Les concepts de robustesse du `scheduler` ont été analysés et seront une source d'inspiration.

## 3. Directives

*   **Répertoire de l'Agent :** `/agents/`
*   **Répertoire de Production (WORK_DIR) :** `20250620_projet_taskmanager/TASKMASTER_PRODUCTION_READY/` (conservé pour les logs et rapports).
*   **Règle d'Or - Non-Régression :** Le nouvel agent `taskmaster_final.py` doit impérativement conserver 100% des fonctionnalités critiques de l'ancienne version. Toute modification doit être validée par un test pour garantir qu'aucune capacité n'est perdue.
*   **Contrôle de Référence :** Un ou plusieurs scénarios de test critiques couverts par `DEPRECATED_taskmaster_agent.py` seront identifiés pour servir de baseline de non-régression.
*   **Sanctuaire `/core` :** Le répertoire `core` reste protégé. Aucune modification ne peut y être apportée sans une justification majeure et des tests approfondis.

## 4. Plan d'Action Détaillé (Méthodologie M-T-D)

### **Phase 1 – Conception et Initialisation (Modification)**

*   **Étape 1.1 : Création du Squelette de l'Agent**
    *   **Action :** Créer le fichier `agents/taskmaster_final.py`.
    *   **Contenu :**
        *   Classe `TaskMasterFinal`.
        *   `__init__` avec gestion des chemins `PROJECT_ROOT` et `WORK_DIR`.
        *   Configuration d'un logger qui écrit dans `WORK_DIR/logs/taskmaster_final.log`.
        *   Méthodes `startup` et `shutdown` basiques.
    *   **Livrable :** Fichier `agents/taskmaster_final.py` créé.

### **Phase 2 – Test de Viabilité (Test)**

*   **Étape 2.1 : Création du Test d'Instanciation**
    *   **Action :** Créer le script `tests/integration/test_taskmaster_final_instantiation.py`.
    *   **Scénario :** Le test importera `TaskMasterFinal`, l'instanciera, appellera `startup` puis `shutdown`.
    *   **Critère de Succès :** Le test s'exécute sans erreur et un fichier de log est créé.

*   **Commit Obligatoire 1**
    *   **Message :** `feat(taskmaster): skeleton and instantiation test`
    *   **Raison :** Valide la structure de base et la viabilité de l'agent avant d'ajouter la logique métier.

### **Phase 3 – Implémentation du Cœur Métier (Modification)**

*   **Étape 3.1 : Découverte Dynamique des Agents**
    *   **Action :** Implémenter dans `TaskMasterFinal` une méthode `_discover_agents` qui scanne le répertoire `/agents`, ignore les agents défectueux, et charge les `capabilities` des agents valides.

*   **Étape 3.2 : Logique de Traitement de Mission**
    *   **Action :** Implémenter une méthode `execute_mission(natural_language_prompt: str)` qui :
        1.  Analyse le prompt pour en extraire l'intention et les entités.
        2.  Sélectionne l'agent le plus pertinent parmi ceux découverts.
        3.  Instancie l'agent sélectionné et lui délègue la tâche.
        4.  Récupère et sauvegarde le résultat.

*   **Étape 3.3 : Contrôle de Non-Régression Primaire (Test)**
    *   **Action :** Créer un test simple qui exécute une mission de base sur le `taskmaster_final.py`.
    *   **Scénario :** Le test vérifiera que pour une tâche simple (ex: "documente le projet"), l'agent sélectionné par le nouveau TaskMaster est bien `agent_13_specialiste_documentation`, conformément au comportement attendu.
    *   **Critère de Succès :** Le bon agent est sélectionné, confirmant que la logique de délégation de base n'a pas régressé.

*   **Commit Obligatoire 2**
    *   **Message :** `feat(taskmaster): core logic with agent discovery and delegation`
    *   **Raison :** Implémente la fonctionnalité principale de l'agent.

### **Phase 4 – Test Fonctionnel Complet (Test)**

*   **Étape 4.1 : Création du Test de Workflow**
    *   **Action :** Créer le script `tests/integration/test_taskmaster_final_workflow.py`.
    *   **Scénario :** Instancier `TaskMasterFinal` et lui soumettre une mission complexe comme `"Crée un workspace pour un projet et documente-le."`, qui représente un cas d'usage clé de l'ancien agent.
    *   **Critères de Succès :**
        1.  `TaskMasterFinal` sélectionne et délègue correctement à `agent_14` puis `agent_13`.
        2.  Le workflow complet s'exécute sans erreur.
        3.  Les artefacts (fichiers, rapports) sont créés dans le `WORK_DIR`.
        4.  **Le succès de ce test sur un scénario de référence valide la non-régression fonctionnelle de bout en bout.**

### **Phase 5 – Documentation Finale (Documentation)**

*   **Étape 5.1 : Création du `README.md`**
    *   **Action :** 
        *   Mettre à jour le `README.md` principal pour décrire l'architecture finale du `taskmaster_final.py`, son utilisation, et comment lancer la suite de tests.
        *   **Ajouter une section "Validation de Non-Régression"** qui confirme que les fonctionnalités critiques ont été préservées, en citant le test de workflow comme preuve.

*   **Commit Obligatoire 3**
    *   **Message :** `docs(taskmaster): final user documentation`
    *   **Raison :** Finalise le projet avec une documentation à jour pour les utilisateurs.

---

## 5. Instruction Initiale de la Session

Votre première action est d'acter ce changement de plan dans le journal, puis de procéder à la **Phase 1, Étape 1.1 : Création du Squelette de l'Agent**. 