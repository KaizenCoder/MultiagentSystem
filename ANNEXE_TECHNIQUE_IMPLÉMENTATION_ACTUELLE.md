# Annexe technique — État actuel et prototype abandonné

## **Prototype actuel**

- **Fonctionnalités principales** :
  - Découverte dynamique des agents spécialisés
  - Délégation de missions selon les "capabilities"
  - Orchestration, logs, gestion du cycle de vie
- **Limites** :
  - Pas de parsing automatique de documents complexes
  - Pas de découpage automatique en tâches/sous-tâches
  - Pas d'attribution de complexité/dépendances/priorités

## **Prototype abandonné (DEPRECATED)**

- **Fonctionnalités avancées** :
  - Utilisation de NLP (spaCy, transformers) pour parser des requêtes complexes
  - Découpage automatique en sous-tâches via analyse de dépendances
  - Attribution de complexité, estimation de durée, justification des choix
  - Génération d'un plan d'action séquencé ou parallèle
- **Raison de l'abandon** :
  - Non intégré à la nouvelle architecture "Cursor"
  - Problèmes de maintenance, dette technique

## **Exigence clé**

> **L'ensemble des fonctionnalités avancées du prototype abandonné doit être réintégré et augmenté dans la nouvelle version.**

---

**Sources d'inspiration et standards** :
- TaskMaster servers (Pulse, Playbooks, etc.)
- TaskFlow, Chain of Thought Task Manager, Task Orchestrator 