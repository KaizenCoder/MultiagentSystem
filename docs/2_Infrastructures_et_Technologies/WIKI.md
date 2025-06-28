# 🛠️ Wiki des Infrastructures et Technologies

## 1. 🚀 Vue d'ensemble de la Stack Technique

L'écosystème NextGeneration repose sur une stack technologique locale, performante et résiliente, conçue pour supporter des opérations d'IA complexes. Chaque brique a un rôle précis et interagit avec les autres pour former un tout cohérent.

L'architecture peut être vue comme un système nerveux :
- **Le Cerveau (Calcul)** : La carte graphique NVIDIA RTX 3090.
- **La Mémoire (Données)** : Un duo PostgreSQL (court terme) et ChromaDB (long terme).
- **Le Système Nerveux (Orchestration)** : L'application Taskmaster.

## 2. 🧠 Le Cerveau : GPU NVIDIA RTX 3090 & Ollama

Le cœur de la puissance de calcul est la **NVIDIA RTX 3090**. Son utilisation est strictement encadrée pour garantir performance et stabilité.

- **Usage Exclusif** : Des mécanismes (variables d'environnement) forcent l'utilisation de ce GPU spécifique, même dans un environnement multi-GPU.
- **Service d'Inférence** : Le service **Ollama** est configuré pour tourner exclusivement sur la RTX 3090, servant de point d'entrée unique pour l'inférence des modèles de langage locaux.
- **Standards Stricts** : Des templates de code et des fonctions de validation obligatoires (`validate_rtx3090_mandatory`) assurent que chaque script respecte les règles de configuration.

> Pour plus de détails, consultez le **[Wiki dédié à la RTX 3090](./RTX3090/WIKI_RTX3090.md)**.

## 3. 🗃️ La Mémoire : Le Duo PostgreSQL & ChromaDB

Le stockage des données est géré par une architecture hybride intelligente qui sépare les besoins à court et à long terme.

### PostgreSQL : La Mémoire à Court Terme
- **Rôle** : Gère les données structurées, les sessions actives, les états temporaires et les métriques en temps réel.
- **Niveau** : Qualité "Enterprise", avec une configuration optimisée (connexions, extensions, index) pour une performance maximale.
- **Fiabilité** : Sert de source de vérité pour l'état opérationnel du système.

> Pour plus de détails, consultez les **[documentations sur PostgreSQL](./postgresql/)**.

### ChromaDB : La Mémoire Sémantique à Long Terme
- **Rôle** : Stocke la "mémoire" à long terme des agents sous forme de vecteurs. C'est la base du système de **RAG (Retrieval-Augmented Generation)**.
- **Fonctionnement** : Transforme les textes (conversations, documents) en vecteurs sémantiques (embeddings) via les modèles OpenAI, permettant une recherche basée sur le sens et non sur les mots-clés.
- **Intégration** : L'accès à ChromaDB et PostgreSQL est unifié via une **Memory API**, qui sert de façade unique pour la gestion de la mémoire.

## 4. ⚙️ Le Système Nerveux : L'Orchestrateur Taskmaster

**Taskmaster** est la couche applicative qui utilise l'infrastructure pour exécuter des tâches complexes.

- **Fonctionnalités Clés** : Traitement du langage naturel (NLP), décomposition de tâches, validation anti-hallucination et résolution de dépendances.
- **Architecture** : Repose sur un "Pattern Factory" et un "Pool Supervisor" pour gérer de multiples instances d'agents de manière scalable et résiliente.
- **Intégration Transparente** : Taskmaster est conçu pour s'intégrer nativement à l'infrastructure existante (PostgreSQL, Docker, Prometheus) pour la persistance, le déploiement et le monitoring. 