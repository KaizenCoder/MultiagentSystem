# Plan d'Action Final – Opérationnalisation de l'Agent TaskMaster (Next-Generation)

*   **Version :** 2.0 (Final)
*   **Date :** 24/06/2025
*   **Contexte :** Vous êtes un assistant IA spécialisé en architecture logicielle. Votre mission est de piloter l'évolution du script `agents/taskmaster_agent.py` pour le rendre robuste, autonome et prêt pour la production, en suivant une méthodologie stricte et sans introduire de régression fonctionnelle.

---

## 1. Contexte Global & Mission

Nous partons d'une version d'origine de `taskmaster_agent.py`. L'objectif est de le transformer en un agent "Next-Generation" qui soit :
1.  **Indépendant de son emplacement :** La logique d'import doit être découplée de la logique de lecture/écriture des fichiers.
2.  **Centralisé :** Toutes ses dépendances externes (logs, data, rapports, tests) doivent être gérées dans un répertoire de production unique.
3.  **Robuste :** Le processus de modification doit suivre une procédure systématique de test et de documentation.

## 2. État Actuel

*   Le script `agents/taskmaster_agent.py` est dans sa version originale.
*   Aucune modification de code n'a encore été effectuée. Ce plan d'action est la référence unique.

## 3. Répertoires & Directives

### 3.1. Répertoire de Production (WORK_DIR)

Le répertoire de travail unique pour tous les artéfacts générés est :
**`C:\Dev\nextgeneration\20250620_projet_taskmanager\TASKMASTER_PRODUCTION_READY`**

Sa structure sera :
```
TASKMASTER_PRODUCTION_READY/
├── logs/
├── data/
├── reports/
├── tests/
└── TASKMASTER_JOURNAL.md
```

### 3.2. Variables de Chemin Stratégiques

Pour éviter les conflits, l'agent utilisera deux variables de chemin distinctes :
*   `PROJECT_ROOT`: Pointera vers la racine du projet (`C:\Dev\nextgeneration`) pour assurer la robustesse des imports Python (ex: logger centralisé).
*   `WORK_DIR`: Pointera vers le `PROD_PATH` ci-dessus et sera utilisé **exclusivement** pour toutes les opérations de lecture/écriture (logs, data, reports).

## 4. Méthodologie Impérative : Le Cycle M-T-D Renforcé avec Git

Chaque action sur le code de l'agent suivra **strictement** la séquence suivante :

1.  **Commit Git Préalable :** S'assurer que l'état de travail actuel est propre et que la dernière version stable est `commitée` dans Git avec un message clair.
2.  **Proposition d'Analyse :** Analyser l'étape à réaliser et proposer la modification.
3.  **Journal (Proposition) :** Consigner l'analyse et la proposition dans le fichier `WORK_DIR/TASKMASTER_JOURNAL.md`.
4.  **Validation Utilisateur :** Attendre un **"GO"** explicite de votre part avant toute modification du code.
5.  **Application :** Vous appliquerez la modification via copier-coller.
6.  **Test Fonctionnel :** Je fournirai les instructions pour exécuter le script de test depuis `WORK_DIR/tests/run_functional_test.py`.
7.  **Analyse des Résultats :** Vérifier les logs et les rapports produits dans `WORK_DIR` pour confirmer le succès.
8.  **Journal (Résultat) :** Inscrire le résultat (`SUCCÈS`/`ÉCHEC`), les preuves et les observations dans le journal.
9.  **Validation Finale :** Attendre un **"GO/NO-GO"** de votre part pour passer à l'étape suivante.

### 4.1. Règle d'Or : Non-Régression Fonctionnelle
*   **Directive Impérative :** Toute modification proposée doit préserver ou enrichir les fonctionnalités existantes de l'agent TaskMaster. La réduction ou la désactivation de fonctionnalités, même temporairement pour contourner un problème, est strictement interdite. L'objectif est l'amélioration continue, jamais la régression.

### 4.2. Règle du Sanctuaire : Intégrité du Core
*   **Directive Impérative :** Le répertoire `/core` est considéré comme un "sanctuaire" de code. Son contenu est stable, testé, et ne doit sous aucun prétexte être modifié dans le cadre de cette mission. Toute fonctionnalité requise doit être construite en utilisant les composants du `/core` tels qu'ils sont, sans les altérer.

## 5. Plan d'Action Détaillé

### **Phase 1 – Renforcement de l'Agent (Modification)**

*   **Étape 1.1 : Gestion Stratégique des Chemins**
    *   **Modification :** Introduire les variables `PROJECT_ROOT` et `WORK_DIR` pour découpler les imports de la gestion des fichiers. `PROJECT_ROOT` pointera deux niveaux au-dessus du script, et `WORK_DIR` sera une chaîne de caractères statique pointant vers le répertoire de production.
    *   **Impact :** `__init__`, `_verify_environment`, `_load_state`.

*   **Étape 1.2 : Implémentation de la Sauvegarde des Rapports**
    *   **Modification :** Implémenter la méthode `_save_task_report` pour qu'elle écrive les rapports JSON dans `WORK_DIR/reports`.
    *   **Impact :** Ajout de la méthode `_save_task_report`.

*   **Étape 1.3 : Implémentation du Shutdown Propre**
    *   **Modification :** Ajouter une méthode `shutdown` pour fermer proprement le `ThreadPoolExecutor` et éviter les processus zombies.
    *   **Impact :** Ajout de la méthode `shutdown`.

### **Phase 2 – Validation Opérationnelle (Test)**

*   **Étape 2.1 : Création du Script de Test Fonctionnel**
    *   **Objectif :** Créer le script `WORK_DIR/tests/run_functional_test.py`.
    *   **Contenu :** Il importera l'agent, l'instanciera, lancera une tâche simple en langage naturel, attendra son exécution, puis appellera `shutdown`.
    *   **Critères de Succès :**
        1.  Le script s'exécute sans erreur.
        2.  Un fichier de log est créé dans `WORK_DIR/logs`.
        3.  Un rapport de tâche JSON est créé dans `WORK_DIR/reports`.

### **Phase 3 – Documentation**

*   **Étape 3.1 : Création du README.md**
    *   **Objectif :** Créer le fichier `WORK_DIR/README.md`.
    *   **Contenu :** Il décrira la structure du répertoire, expliquera comment lancer le test fonctionnel et comment interpréter les résultats.

---

## 6. Instruction Initiale de la Session

Votre première et unique action immédiate est de **créer le fichier `TASKMASTER_JOURNAL.md`** à l'emplacement `C:\Dev\nextgeneration\20250620_projet_taskmanager\TASKMASTER_PRODUCTION_READY\TASKMASTER_JOURNAL.md` avec le contenu initial suivant.

**Contenu initial pour `TASKMASTER_JOURNAL.md` :**
```markdown
# Journal d'Évolution du Projet TaskMaster

*   **Date de début :** 24/06/2025
*   **Objectif :** Rendre l'agent TaskMaster robuste, autonome et prêt pour la production en suivant un cycle strict M-T-D renforcé avec Git.
*   **Version du Plan :** 2.0 (Final)

---
```

N'exécutez aucune autre action. Une fois le journal créé, attendez ma proposition pour la **Phase 1, Étape 1.1**. 