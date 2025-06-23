# Cahier des charges — Agent TaskMaster nouvelle génération

## **Contexte**

Nous souhaitons développer un agent TaskMaster avancé, capable d'orchestrer la gestion de projets complexes à partir de documents d'entrée (PRD, plans, prompts complexes, etc.).  
L'objectif est de reproduire et dépasser les fonctionnalités des meilleurs orchestrateurs de tâches modernes : découpage automatique, gestion des dépendances, estimation de complexité, priorisation, et justification des choix.

## **Fonctionnalités attendues**

### 1. **Entrée**
- Un ou plusieurs documents (PRD, plan de développement, prompt complexe, markdown, etc.)
- Possibilité de traiter des documents longs et structurés

### 2. **Analyse et découpage automatique**
- Compréhension du contenu (NLP, extraction d'intentions, contraintes, livrables)
- Découpage en tâches et sous-tâches (Work Breakdown Structure)
- Attribution automatique de :
  - **Complexité** (score, justification)
  - **Dépendances** (liens entre tâches, séquencement)
  - **Priorités** (haute, moyenne, basse)
- Justification de chaque découpage et choix (explication textuelle pour chaque tâche/sous-tâche)

### 3. **Gestion structurée des tâches**
- Création, modification, suppression de tâches et sous-tâches
- Suivi de l'état (todo, en cours, en revue, terminé)
- Possibilité d'exporter/importer le plan d'action (JSON, markdown, etc.)
- Génération d'un rapport synthétique et d'un graphe de dépendances

### 4. **Extensibilité et intégration**
- L'agent doit être modulaire, facilement intégrable à notre architecture existante
- Les fonctionnalités avancées de notre prototype actuel doivent être **conservées et augmentées**
- Possibilité d'ajouter des modules (analyse de risques, estimation de charge, etc.)

### 5. **Exemples de scénarios inspirés des TaskMaster modernes**
- **Parsing de PRD** : extraction automatique des exigences, contraintes, livrables
- **Découpage automatique** : transformation d'un plan en arborescence de tâches/sous-tâches, avec dépendances explicites
- **Estimation de complexité** : score pour chaque tâche, basé sur la nature, la taille, les dépendances
- **Gestion dynamique** : ajout, modification, suppression, expansion de tâches (ex : "expandTask")
- **Priorisation intelligente** : identification de la prochaine tâche actionnable ("getNextTask")
- **Export/Import** : sauvegarde et restauration de projets complets

## **Livrables attendus**

- **Code complet, fonctionnel, documenté**
  - L'ensemble du code source, prêt à l'emploi, avec commentaires et guides d'utilisation
- **Rapport d'analyse détaillé**
  - Explication des choix techniques, des algorithmes de découpage, des critères de complexité et de dépendance
- **Plan d'implémentation détaillé**
  - Description des étapes de développement, de l'architecture, des modules, des jalons et des points de validation
- **Jeux de tests**
  - Scénarios de tests couvrant des exemples réels de PRD/plans, cas limites, et validation de toutes les fonctionnalités attendues
- **Documentation utilisateur et technique**
  - Guide d'utilisation, manuel d'intégration, schémas d'architecture, exemples d'utilisation
- **Rapport de validation**
  - Résultats des tests, conformité aux exigences, bilan de couverture fonctionnelle

## **Contraintes**

- L'agent doit être autonome, modulaire, et facilement extensible
- Les fonctionnalités avancées de notre prototype actuel doivent être **conservées dans leur intégralité** et **améliorées**

---

**Sources d'inspiration et standards** :
- TaskMaster servers (Pulse, Playbooks, etc.) : parsing PRD, CRUD tâches, gestion dépendances, complexité, export/import, API structurée
- TaskFlow, Chain of Thought Task Manager, Task Orchestrator : découpage automatique, dépendances, priorisation, justification, export structuré 