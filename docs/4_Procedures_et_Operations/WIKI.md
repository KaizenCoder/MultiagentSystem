# 📋 Wiki des Procédures Opérationnelles de NextGeneration

## 1. 🚀 Introduction

Ce wiki documente les procédures standardisées qui gouvernent le cycle de vie d'une mission au sein de l'écosystème NextGeneration. Le respect de ces procédures est essentiel pour garantir la collaboration efficace entre les agents, la qualité des livrables et la maintenabilité du projet.

Le cycle de vie d'une mission se décompose en trois phases principales :
1.  **Onboarding et Prise en main** : Comment un agent est intégré et démarre sa tâche.
2.  **Coordination et Exécution** : Comment la mission est transmise, suivie et réalisée.
3.  **Contrôle Qualité** : Comment la qualité des livrables est assurée tout au long du processus.

## 2. 🤖 Phase 1 : Onboarding d'un Agent IA

Tout agent (humain ou IA) intégré au projet doit suivre ce protocole initial.

### Principes Fondateurs
- **Autonomie** : Prendre des initiatives pour atteindre les objectifs.
- **Collaboration** : Utiliser les outils partagés et interagir avec les autres agents.
- **Efficacité** : Optimiser l'usage des ressources.
- **Traçabilité** : Toutes les actions doivent être loguées et justifiées.

### Premiers Pas
1.  **Comprendre la Mission** : Lire attentivement le prompt assigné dans le dossier `/prompt`.
2.  **Analyser les Outils** : **Explorer le répertoire `/tools` en priorité.** Il est très probable qu'un outil existe déjà pour faciliter la mission.
3.  **Exécuter** : Réaliser la mission en respectant les standards.
4.  **Rapporter** : Signaler la complétion et s'assurer que les livrables sont conformes.

## 3. 📜 Phase 2 : Transmission et Coordination de Mission

Cette procédure formalise l'interaction entre un **Coordinateur** (qui donne la mission) et l'**Agent** (qui la réalise).

### Checklist de Cycle de Vie de la Mission

#### Étape A : Briefing de Mission (Input du Coordinateur)
- `[ ]` **Prompt clair** : Un fichier `PROMPT_*.md` est fourni.
- `[ ]` **Objectifs mesurables** : Les critères de succès sont définis.
- `[ ]` **Livrables spécifiés** : La liste des fichiers à produire/modifier est exacte.

#### Étape B : Allocation des Ressources
- `[ ]` **Accès au code** : L'agent a accès à la bonne branche Git.
- `[ ]` **Outils identifiés** : La liste des outils du répertoire `/tools` nécessaires est connue.

#### Étape C : Exécution & Monitoring
- `[ ]` **Confirmation** : L'agent accuse réception et confirme sa compréhension.
- `[ ]` **Rapports de progression** : Pour les missions longues, l'agent communique son avancée.
- `[ ]` **Alerting** : L'agent signale immédiatement tout blocage.

#### Étape D : Livraison & Débriefing (Output de l'Agent)
- `[ ]` **Livrables complets** : Tous les fichiers demandés sont présents.
- `[ ]` **Rapport de fin de mission** : Un fichier `RAPPORT_*.md` est généré.
- `[ ]` **Validation** : Le Coordinateur valide que les objectifs sont atteints.
- `[ ] ]` **Nettoyage** : Les ressources temporaires sont libérées.

## 4. ✅ Phase 3 : Framework de Contrôle Qualité

Une checklist qualité doit être validée avant la livraison finale de toute mission.

### Checklist Générale
- **Code & Scripts** :
    - `[ ]` **Lisibilité** : Noms clairs, pas de code "en dur".
    - `[ ]` **Robustesse** : Gestion des erreurs (`try...except`) et logs pertinents.
- **Documentation (`.md`)** :
    - `[ ]` **Clarté** : Facile à comprendre, bien formaté.
    - `[ ]` **Exhaustivité** : Couvre tous les aspects du sujet.
- **Sécurité** :
    - `[ ]` **Aucun Secret** : Aucune clé d'API ou mot de passe ne doit être commité.

### Standards Techniques Stricts
La checklist inclut des validations techniques précises qui doivent être respectées.
- **Infrastructure** :
    - `[ ]` **GPU RTX 3090** : Doit être validée via le script `VALIDATION_STANDARDS_RTX3090.py`.
    - `[ ]` **Variables d'environnement** : `CUDA_VISIBLE_DEVICES` doit être correctement configuré.
- **Tests Automatisés** :
    - `[ ]` **Couverture de tests** : Doit être supérieure ou égale à 80% (`pytest`).
    - `[ ]` **Tests d'intégration et de performance** : Doivent être passés avec succès.
- **Conformité NextGeneration** :
    - `[ ]` **Patterns d'agent** : Doit être conforme à l'architecture `agent_factory`.
    - `[ ]` **Monitoring** : Les logs et métriques doivent être standardisés.

### Checklist pour un Nouvel Outil dans `/tools`
- `[ ]` **Structure standard** : Doit inclure un `README.md`, un répertoire `tests/`, etc.
- `[ ]` **CLI utilisable** : Doit être utilisable en ligne de commande avec `argparse`.
- `[ ]` **Mode `dry-run`** : Doit proposer un mode de simulation (`--validate` ou `--dry-run`).

## 4.  agile Méthodologie Opérationnelle : Les Sprints

Le projet est piloté par une méthodologie Agile structurée autour de Sprints. Chaque Sprint a des objectifs clairs, des agents assignés, et des livrables définis.

### Structure d'un Sprint
- **Objectifs** : Une liste des fonctionnalités et améliorations techniques à réaliser.
- **Agents Assignés** : Les agents spécifiques (ex: "Agent 06 - Spécialiste Monitoring") sont désignés comme "leads" pour chaque objectif.
- **Definition of Done** : Des critères précis qui doivent être remplis pour que le Sprint soit considéré comme terminé.
- **Handovers** : Un processus formel de transmission des artefacts et des responsabilités au Sprint suivant.

### Suivi et Rapports
- **Synthèse de Fin de Sprint** : Un document détaillé est produit à la fin de chaque Sprint, résumant les objectifs atteints, les métriques de performance, l'état du projet et la préparation pour le Sprint suivant.
- **Journaux** : Un répertoire `journals` est utilisé pour conserver une trace détaillée des opérations et des décisions prises au quotidien.

Cette approche garantit une progression itérative, une traçabilité complète et une amélioration continue de l'écosystème. 