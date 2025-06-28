# 🤖 GUIDE D'ONBOARDING POUR IA - PROJET NEXTGENERATION

## 1. 🚀 BIENVENUE DANS NEXTGENERATION

Bonjour. Vous avez été intégré à l'écosystème NextGeneration, un projet de système multi-agents avancé. Votre objectif est de collaborer avec d'autres agents pour accomplir des missions de développement, d'analyse, de documentation et de maintenance.

Ce guide contient les informations essentielles pour votre intégration réussie.

## 2. 🧭 PRINCIPES FONDATEURS

-   **Autonomie :** Vous êtes encouragé à prendre des initiatives pour atteindre vos objectifs.
-   **Collaboration :** Interagissez avec les autres agents et utilisez les outils partagés.
-   **Efficacité :** Optimisez votre consommation de ressources et votre temps d'exécution.
-   **Traçabilité :** Toutes vos actions doivent être loguées et justifiées.

## 3. 🏗️ ARCHITECTURE DU SYSTÈME

Le système est organisé autour de plusieurs composants clés :

-   **`/` (Racine) :** Point d'entrée du projet. Contient les fichiers de configuration principaux.
-   **`prompt/` :** Contient les prompts de mission qui vous seront assignés.
-   **`tools/` :** Votre boîte à outils. Contient des agents et scripts spécialisés pour des tâches communes (backup, documentation, monitoring...). **Explorez-la en priorité.**
-   **`scripts/` :** Contient des workflows automatisés (PowerShell, Python) pour des tâches complexes.
-   **`docs/` :** La base de connaissance du projet. Contient la documentation, les procédures et les standards.
-   **`CHANGELOG.md` & `docs/SYNTHESE_EXECUTIVE.md` :** Documents stratégiques mis à jour automatiquement. Ne les modifiez pas directement.

## 4. 🛠️ VOS PREMIERS PAS

### **Étape 1 : Comprendre votre Mission**

-   Lisez attentivement le prompt de mission qui vous a été assigné dans le dossier `prompt/`.
-   Identifiez les objectifs, les livrables et les critères de succès.

### **Étape 2 : Analyser les Outils Disponibles**

-   Avant de coder, listez le contenu du répertoire `tools/`. Il est très probable qu'un outil existant puisse accomplir une partie de votre tâche.
-   Lisez le `README.md` de chaque outil pertinent.

### **Étape 3 : Exécuter votre Mission**

-   Créez ou modifiez les fichiers conformément à votre mission.
-   Utilisez les outils et les scripts existants autant que possible.
-   Si vous créez un nouvel outil, respectez la structure existante (`README.md`, `config.json`, etc.).

### **Étape 4 : Rapporter vos Résultats**

-   Une fois la mission terminée, signalez sa complétion.
-   Assurez-vous que tous les livrables sont présents et conformes aux critères de succès.

## 5. ⚠️ RÈGLES D'OR

-   **Ne jamais commiter de secrets :** N'incluez jamais de clés d'API ou de mots de passe dans le code.
-   **Utiliser le `.gitignore` :** Ne commitez pas de fichiers générés volumineux comme `CODE-SOURCE.md`.
-   **Suivre les Procédures :** Respectez les procédures définies dans `docs/procedures/`.

---
*Document maintenu par l'Équipe Contenu & Standards.*