# 🧪 Wiki du Développement et des Preuves de Concept (POCs)

## 1. 🚀 Vue d'ensemble

Cette section est le "laboratoire" du projet. Elle contient les livrables concrets, les expérimentations, les guides de développement et la documentation des outils qui ne font pas partie de l'infrastructure de base mais qui sont des produits du travail d'ingénierie.

C'est ici que l'on trouve les réponses à la question : "Comment faire ?" et la preuve de ce qui a été fait.

## 2. 💡 Preuves de Concept (POCs)

Le répertoire `/POC` contient les résultats d'expérimentations visant à valider la faisabilité de nouvelles idées ou de nouvelles intégrations.

**Exemple Notablé : L'extension Cursor / VS Code**
- **Objectif** : Prouver qu'il est possible d'intégrer l'orchestrateur multi-agents directement dans l'éditeur de code pour améliorer la productivité des développeurs.
- **Livrables** :
    -   Un `package.json` définissant les commandes (`multiAgent.orchestrateTask`), les raccourcis et les paramètres de l'extension.
    -   Un fichier `extension.ts` (TypeScript) contenant la logique pour :
        1.  Récupérer le code sélectionné et la description d'une tâche.
        2.  Appeler l'API de l'orchestrateur.
        3.  Gérer la réponse en streaming (SSE).
        4.  Afficher une vue "diff" pour comparer le code original et les modifications proposées.
        5.  Appliquer les changements.
- **Résultat** : Un POC fonctionnel qui transforme l'éditeur en une interface interactive pour le système multi-agents.

## 3. 🛠️ Guides de Développement

Le répertoire `/guides_developpement` contient des instructions et des meilleures pratiques pour les développeurs travaillant sur des parties spécifiques de l'écosystème.

On y trouve par exemple :
-   Le guide pour exploiter la puissance du GPU RTX 3090.
-   Le guide d'exécution pour déployer l'environnement PostgreSQL.

## 4. 🧰 Outils Spécifiques

Le répertoire `/tools_specifiques` documente les outils qui ont été développés pour des besoins particuliers du projet, mais qui ne sont pas des composants centraux de l'infrastructure. 