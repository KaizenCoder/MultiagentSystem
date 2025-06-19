# 🚀 PROMPT MISSION : CI/CD - WORKFLOW D'AUTOMATISATION DE LA DOCUMENTATION

## 🎯 **CONTEXTE**

Le système de documentation est maintenant mature et robuste. La prochaine étape logique est de l'intégrer dans un pipeline d'Intégration Continue (CI/CD) pour automatiser entièrement son exécution.

Cette mission consiste à créer un workflow GitHub Actions qui se déclenchera automatiquement pour valider et mettre à jour la documentation du projet.

**Prérequis :** Cette mission suppose l'existence du script `scripts/validate_and_document.ps1` (défini dans la mission de finalisation de la transposition).

## ✅ **OBJECTIFS TECHNIQUES**

### **1. Création du Fichier de Workflow**

-   **Action :** Créer le répertoire `.github/workflows/` s'il n'existe pas.
-   **Chemin du fichier :** `.github/workflows/documentation.yml`

### **2. Configuration du Workflow**

-   **Nom du Workflow :** `Documentation CI`

-   **Déclencheur (Trigger) :**
    -   Se déclenche à chaque `push` sur la branche `new-main`.

-   **Jobs :**
    -   Définir un unique job nommé `build-and-commit-docs`.
    -   **Runner :** Le job doit s'exécuter sur `windows-latest` pour garantir la compatibilité avec les scripts PowerShell.
    -   **Étapes (Steps) :**
        1.  **Checkout Code :** Utiliser `actions/checkout@v4` pour récupérer la dernière version du code.
        2.  **Setup Python :** Utiliser `actions/setup-python@v5` pour installer Python 3.8 ou supérieur.
        3.  **(Optionnel) Install Dependencies :** Si des dépendances Python sont nécessaires, les installer via `pip install -r requirements.txt`.
        4.  **Execute Documentation Workflow :**
            -   Lancer le script `scripts/validate_and_document.ps1` en utilisant `pwsh`.
            -   S'assurer que le script s'exécute avec les permissions nécessaires.
        5.  **Commit and Push Changes :**
            -   Utiliser une action comme `stefanzweifel/git-auto-commit-action@v5` ou une série de commandes `git` pour :
                -   Vérifier si les fichiers de documentation (`SYNTHESE_EXECUTIVE.md`, `CHANGELOG.md`) ont été modifiés.
                -   Si oui, commiter les changements avec un message standardisé (ex: `docs(auto): Update documentation from CI`).
                -   Pousser le commit vers la branche `new-main`.

## 🏆 **CRITÈRES DE SUCCÈS**

-   Le fichier `.github/workflows/documentation.yml` est créé et valide.
-   Un `push` sur la branche `new-main` déclenche automatiquement l'exécution du workflow.
-   Le workflow exécute avec succès le script PowerShell de validation et de documentation.
-   Si la documentation est modifiée par le script, le workflow crée un nouveau commit et le pousse sur la branche `new-main` sans intervention manuelle.
-   Le workflow doit réussir sans erreur de permission ou de configuration. 