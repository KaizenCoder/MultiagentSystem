# Architecture Unifiée — TaskMaster V3

## 1. Vision et Principes Directeurs

L'architecture V3 vise à synthétiser les meilleures approches des experts (ChatGPT, Claude, Gemini) pour créer un système **robuste**, **modulaire**, **intelligent** et **évolutif**.

- **Robustesse (inspiré de Claude) :** Typage fort, gestion des erreurs, tests exhaustifs (unitaires, intégration, performance), et validation anti-hallucination.
- **Modularité (inspiré de Claude & ChatGPT) :** Séparation claire des responsabilités en modules distincts, facilitant la maintenance, les tests et l'évolution.
- **Intelligence (inspiré de Gemini & Claude) :** Algorithmes de parsing, scoring et planification clairs et performants, utilisant des techniques NLP avancées.
- **Évolutivité (inspiré de ChatGPT & Claude) :** Architecture pensée pour l'intégration de nouvelles fonctionnalités, de nouveaux agents et l'exposition via API.

## 2. Structure du Projet Cible

Basée sur les standards de l'industrie (proposés par ChatGPT), voici la structure de dossiers recommandée :

```
/taskmaster_v3
│
├── main.py                  # Point d'entrée CLI et/ou API
│
├── core/
│   ├── __init__.py
│   ├── models.py            # Modèles de données (Task, Project, etc. - inspiré de Claude/Gemini)
│   ├── engine.py            # Moteur principal TaskMaster (orchestration)
│   ├── exceptions.py        # Exceptions customisées
│   └── config.py            # Gestion de la configuration
│
├── modules/
│   ├── __init__.py
│   ├── nlp_processor.py     # Parsing et analyse NLP (inspiré de Claude)
│   ├── complexity_analyzer.py # Scoring de complexité (logique simple de Gemini, extensible)
│   ├── dependency_resolver.py # Graphe de dépendances (inspiré de Claude/networkx)
│   ├── validation_engine.py   # Validation anti-hallucination (concept de Claude)
│   └── persistence/
│       ├── __init__.py
│       ├── repository.py    # Abstraction du stockage (inspiré de Claude)
│       └── sqlite_backend.py # Implémentation SQLite (ou autre)
│
├── api/
│   ├── __init__.py
│   ├── server.py            # Serveur FastAPI/Flask
│   └── routes.py            # Endpoints API (CRUD, export)
│
├── tests/
│   ├── __init__.py
│   ├── fixtures/            # Données de test (ex: PRD samples)
│   ├── test_nlp_processor.py
│   ├── test_engine.py
│   └── ...                  # Tests pour chaque module
│
└── docs/
    ├── README.md
    ├── architecture.md
    └── api_reference.md
```

## 3. Composants Clés et Algorithmes

### 3.1. `core/models.py`
- **Source d'inspiration :** La richesse des `dataclasses` de **Claude** (avec `Enums` pour les statuts, priorités, etc.).
- **Action :** Utiliser des `dataclasses` Pydantic ou standard pour définir `TaskDefinition`, `SubTask`, `TaskMetrics`, etc., en incluant les concepts de `ValidationStatus` et `EvidenceEntry` de Claude.

### 3.2. `modules/nlp_processor.py`
- **Source d'inspiration :** L'approche de **Claude** est la plus complète.
- **Action :** Implémenter une classe `NLPProcessor` qui utilise `spaCy` pour l'extraction d'entités et des patterns de mots-clés pour classifier le type de tâche et la priorité.

### 3.3. `modules/complexity_analyzer.py`
- **Source d'inspiration :** L'algorithme de **Gemini** est simple, concret et efficace pour un début.
- **Action :** Commencer avec un scoring basé sur des critères clairs (longueur du nom, mots-clés techniques, nombre de dépendances). Prévoir une architecture qui permettra de le rendre plus complexe par la suite (comme le suggère Claude).

### 3.4. `modules/dependency_resolver.py`
- **Source d'inspiration :** L'approche de **Gemini** (regex `dépend de:`) est un bon point de départ. L'approche de **Claude** (basée sur la nature de la tâche) est plus intelligente mais plus complexe.
- **Action :** Fusionner les deux. Utiliser une détection par regex pour les dépendances explicites, et enrichir avec une analyse sémantique du type de tâche (ex: un `test` dépend forcément d'une `implementation`). Utiliser `networkx` pour construire le graphe et détecter les cycles.

### 3.5. `tests/`
- **Source d'inspiration :** La stratégie de tests de **Claude** est la référence.
- **Action :** Adopter `pytest`. Créer des tests unitaires pour chaque classe/fonction. Créer des tests d'intégration qui simulent des flux complets (de la requête NLP à l'export du plan). Inclure des tests de performance pour le parsing de gros documents.

## 4. Plan de Fusion et d'Implémentation (inspiré de ChatGPT)

**Sprint 1 : Socle et Modèles (5 jours)**
- **Objectif :** Mettre en place la structure du projet, les `dataclasses` (`core/models.py`) et le `TaskRepository` (`modules/persistence/`).
- **Validation :** Le CRUD de tâches est fonctionnel et testé unitairement.

**Sprint 2 : Parsing et Analyse de Base (5 jours)**
- **Objectif :** Implémenter `nlp_processor.py` et `complexity_analyzer.py` en se basant sur la logique de Gemini.
- **Validation :** Un document texte simple peut être parsé en une liste de tâches avec un score de complexité.

**Sprint 3 : Dépendances et Orchestration (5 jours)**
- **Objectif :** Implémenter `dependency_resolver.py` et le moteur principal dans `core/engine.py`.
- **Validation :** Un plan d'action avec dépendances peut être généré. La fonction `getNextTask()` retourne la bonne tâche.

**Sprint 4 : API et Finalisation (5 jours)**
- **Objectif :** Exposer les fonctionnalités via une API REST simple (`api/`) et finaliser la documentation.
- **Validation :** Le plan d'action est accessible via un endpoint GET. Le `README.md` est complet. 