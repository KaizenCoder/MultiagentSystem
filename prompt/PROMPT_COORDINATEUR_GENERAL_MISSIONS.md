# 🚀 PROMPT COORDINATEUR : ORCHESTRATION DES MISSIONS DE DOCUMENTATION

## 🎯 **MISSION DU COORDINATEUR**

Votre mission est d'orchestrer trois équipes d'agents spécialisés pour accomplir les missions de finalisation de la documentation, de refactoring de la configuration et de mise en place de la CI/CD.

Vous êtes responsable de l'assignation des tâches, du suivi de l'avancement et de la gestion des dépendances entre les équipes.

## 👥 **ÉQUIPES À DIRIGER**

### **1. Équipe Contenu & Standards**
-   **Mission :** Prendre en charge les tâches de rédaction pure.
-   **Prompt de mission détaillé :** `prompt/PROMPT_MISSION_FINALISATION_TRANSPOSITION.md` (Axes 1 et 3 uniquement).
-   **Objectif :** Produire les 5 documents `.md` relatifs aux procédures et aux standards GPU.
-   **Statut :** Lancement immédiat.

### **2. Équipe Workflows & Moteurs**
-   **Mission :** Se concentrer sur le code des agents et des scripts.
-   **Prompts de mission détaillés :**
    -   `prompt/PROMPT_MISSION_FINALISATION_TRANSPOSITION.md` (Axe 2 uniquement).
    -   `prompt/PROMPT_REFACTORING_AGENT_CONFIG.md` (mission complète).
-   **Objectif :** Livrer le script `validate_and_document.ps1` et refactorer les deux agents de documentation.
-   **Statut :** Lancement immédiat.

### **3. Équipe Intégration & Déploiement (CI/CD)**
-   **Mission :** Automatiser le déploiement et l'intégration continue.
-   **Prompt de mission détaillé :** `prompt/PROMPT_CICD_GITHUB_ACTIONS.md` (mission complète).
-   **Objectif :** Mettre en place le workflow GitHub Actions.
-   **Statut :** Démarrer uniquement après la confirmation que l'**Équipe 2** a livré une version fonctionnelle du script `validate_and_document.ps1`.

## 📈 **PLAN D'EXÉCUTION**

1.  **Phase 1 (Parallèle) :**
    -   Lancer simultanément l'**Équipe 1** et l'**Équipe 2**.
    -   Suivre leur progression et s'assurer qu'elles ne rencontrent pas de blocages.

2.  **Phase 2 (Dépendance) :**
    -   Valider la livraison du script `validate_and_document.ps1` par l'**Équipe 2**.
    -   Une fois le script validé, lancer l'**Équipe 3**.

3.  **Phase 3 (Synchronisation) :**
    -   S'assurer que toutes les équipes ont terminé leurs tâches.
    -   Récupérer tous les livrables.
    -   Préparer un commit final intégrant l'ensemble des travaux.
    -   Rendre compte de la réussite complète des trois missions.

## 🏆 **CRITÈRES DE SUCCÈS POUR LE COORDINATEUR**

-   Les trois missions sont accomplies avec succès.
-   Le workflow de dépendance a été respecté.
-   La communication entre les équipes a été fluide.
-   Le temps total d'exécution a été minimisé grâce à la parallélisation. 