# NextGeneration : Un Orchestrateur Multi-Agent d'Entreprise

Ce dépôt contient le code source et les journaux d'exécution du projet **NextGeneration**, un système d'orchestration multi-agent conçu dès le départ pour répondre aux exigences de sécurité, de scalabilité et de résilience du monde de l'entreprise.

Plus qu'un simple projet logiciel, ce dépôt est un **méta-récit** : la chronique de sa propre création par un système d'agents IA collaboratifs.

## 🎯 Philosophie et Vision

La philosophie de NextGeneration repose sur trois piliers fondamentaux :

1.  **Excellence d'Entreprise ("Enterprise-Grade First")** : Contrairement aux prototypes, ce projet intègre les meilleures pratiques de production dès la première ligne de code. La sécurité, l'observabilité, la scalabilité et l'automatisation ne sont pas des ajouts, mais le socle sur lequel tout est construit.
2.  **Spécialisation et Collaboration Agentique** : Le développement lui-même est piloté par un modèle à deux agents principaux, **IA-1 (Tests & Qualité)** et **IA-2 (Architecture & Production)**. Cette séparation des tâches garantit une expertise approfondie dans chaque domaine et une qualité de niveau supérieur. Leurs journaux et rapports détaillés (`journals/`, `RAPPORT_*.md`) sont la preuve de leur travail.
3.  **Résilience et Adaptabilité** : Le système est conçu pour être dynamique. Comme en témoigne le rapport sur la fusion des IA, l'architecture est capable de s'adapter, de surmonter les défaillances et de créer des synergies inattendues pour garantir la continuité et l'excellence de la mission.

## ⚙️ Fonctionnement du Système

L'architecture de NextGeneration est un écosystème de services robustes, conçus pour fonctionner en harmonie.

```mermaid
graph TD
    subgraph "Système NextGeneration"
        direction LR

        subgraph "Services Applicatifs"
            O[Orchestrateur Multi-Agent]
            M[API Mémoire]
            F[Frontend - CleanVideoHub]
        end

        subgraph "Stockage Persistant"
            P[PostgreSQL]
            C[ChromaDB]
        end

        subgraph "Logique Agentique"
            S[Supervisor]
            W[Agents Spécialisés (Workers)]
        end
        
        F -->|Requêtes| O
        O -->|Gère| S
        S -->|Délègue à| W
        O -->|Utilise| M
        W -->|Utilise| M
        M -->|Accède| P
        M -->|Accède| C
    end

    subgraph "Écosystème d'Entreprise"
        direction TB
        K[Kubernetes]
        CI[CI/CD Pipelines<br/>(Blue/Green, Canary)]
        Obs[Stack d'Observabilité<br/>(Prometheus, Grafana, Jaeger)]
    end
    
    K -->|"Héberge"| F & O & M & P & C
    CI -->|Déploie sur| K
    Obs -->|Surveille| K

```

### Composants Applicatifs

*   **Orchestrateur (`/orchestrator`)** : Le cœur du système. Développé en Python avec FastAPI, il gère le cycle de vie des agents. Il est composé d'un **Supervisor** qui analyse les tâches et les route vers des **Workers** (agents spécialisés) pour exécution.
*   **API Mémoire (`/memory_api`)** : Le système de mémoire à long terme. Ce service Python implémente une architecture **RAG (Retrieval-Augmented Generation)**, utilisant une base de données vectorielle **ChromaDB** pour la recherche sémantique et une base **PostgreSQL** pour les données structurées.
*   **Frontend (`/cleanvideohub`)** : Une interface utilisateur moderne (React, Vite, ShadCN/UI) qui sert de point d'interaction avec le système et de démonstration de ses capacités.

### Écosystème d'Entreprise

L'application est soutenue par une infrastructure conçue pour la haute disponibilité et la scalabilité :

*   **Déploiement et Scalabilité** : Le système est entièrement conteneurisé (`Dockerfile`) et orchestré par **Kubernetes** à l'aide de charts **Helm** (`/k8s`). L'auto-scaling (HPA) et des stratégies de déploiement avancées comme le **Blue/Green** et le **Canary** sont automatisées (`/scripts`).
*   **Observabilité Complète** : Une stack de monitoring de premier plan est intégrée, incluant **Prometheus** pour les métriques, **Grafana** pour les tableaux de bord, et **Jaeger** (via OpenTelemetry) pour le traçage distribué.
*   **Performance et Résilience** : Des **Load Balancers** (HAProxy), des systèmes de **cache distribué** (Redis Cluster) et des **pools de connexion** (PgBouncer) garantissent des performances optimales et une grande résilience.

## 🚀 Démarrage Rapide

Ce projet utilise Docker Compose pour un démarrage simplifié de l'environnement de développement.

### Prérequis

*   Docker & Docker Compose
*   Avoir des clés API valides (ex: OpenAI, Anthropic)

### Étapes

1.  **Configurer les variables d'environnement :**
    ```bash
    cp env.example .env
    # Éditez .env et ajoutez vos clés API
    ```

2.  **Lancer les services :**
    ```bash
    # Lancer l'ensemble de la stack en arrière-plan
    docker-compose -f docker-compose.yml up -d
    ```

3.  **Vérifier le statut :**
    ```bash
    # Vérifier que tous les conteneurs sont lancés
    docker-compose ps
    
    # Consulter les logs d'un service spécifique (ex: orchestrateur)
    docker-compose logs -f orchestrator
    ```

### Services Disponibles (Ports par défaut)

| Service | Port | URL |
|---|---|---|
| Orchestrateur | `8000` | http://localhost:8000/docs |
| API Mémoire | `8001` | http://localhost:8001/docs |
| Frontend (CleanVideoHub) | `5173` | http://localhost:5173 |

## 🛠️ Stack Technologique Principale

*   **Backend** : Python, FastAPI, LangGraph
*   **Frontend** : TypeScript, React, Vite, TailwindCSS
*   **Bases de données** : PostgreSQL, ChromaDB (vectoriel), Redis (cache)
*   **Orchestration** : Docker, Kubernetes, Helm
*   **CI/CD** : Scripts Bash/PowerShell pour Blue/Green & Canary
*   **Observabilité** : Prometheus, Grafana, Jaeger, OpenTelemetry
*   **Tests** : Pytest, K6 (load testing)

## 📁 Structure du Projet

```
/multi-agent-dev-env
├── /orchestrator          # Service principal
│   ├── /app
│   │   ├── /agents        # Logique des agents
│   │   ├── /graph         # Gestion d'état
│   │   └── main.py        # Point d'entrée
│   ├── Dockerfile
│   └── requirements.txt
├── /memory_api            # Service de mémoire
│   ├── /app
│   │   ├── /db           # Base de données
│   │   ├── /models       # Schémas de données
│   │   ├── /services     # Services métier
│   │   └── main.py       # API FastAPI
│   ├── Dockerfile
│   └── requirements.txt
├── /cursor_extension      # Extension VS Code
│   ├── /src
│   │   └── extension.ts  # Code principal
│   ├── package.json
│   └── tsconfig.json
├── /codebase_docs        # Documentation RAG
├── docker-compose.yml    # Orchestration
├── env.example          # Variables d'environnement
└── README.md           # Ce fichier
```

## 🚀 Installation et Lancement

### Prérequis
- Docker et Docker Compose
- Node.js (pour l'extension)
- VS Code ou Cursor

### 1. Cloner le repository
```bash
git clone <repository-url>
cd multi-agent-dev-env
```

### 2. Configuration
```bash
cp env.example .env
# Éditer .env avec vos configurations
```

### 3. Lancement des services
```bash
docker-compose up --build
```

### 4. Installation de l'extension
```bash
cd cursor_extension
npm install
npm run compile
```

## 📖 Documentation

- [Livrable 1 : Structure du projet](./livrable1_structure_projet.md)
- [Livrable 3 : API Mémoire](./livrable3_api_memoire.md)
- [Livrable 4 : Docker Compose](./livrable4_docker_compose.md)
- [Livrable 5 : Extension Cursor](./livrable5_cursor_extension.md)
- [Livrable 6 : Installation et Lancement](./livrable6_installation_lancement.md)

## 🔗 URLs des Services

- **Orchestrateur** : http://localhost:8000
- **Memory API** : http://localhost:8001
- **Documentation API** : http://localhost:8001/docs

## 🤝 Contribution

Ce projet suit une architecture modulaire. Chaque service est indépendant et peut être développé séparément.

## 📄 Licence

[À définir]

# Next Generation Multi-Agent System

## Architecture

Ce projet implémente un système multi-agent de nouvelle génération avec :

- **Orchestrateur** : Service de coordination utilisant LangGraph
- **API de mémoire** : Gestionnaire de mémoire hybride (court/long terme)
- **Base de données PostgreSQL** : Stockage persistant pour la mémoire à court terme
- **ChromaDB** : Base vectorielle pour la mémoire à long terme et RAG
- **Extension Cursor** : Interface utilisateur intégrée à l'IDE

## Extension Cursor/VS Code

### 🚀 Fonctionnalités

L'extension **Multi-Agent Orchestrator** transforme votre éditeur en une interface de développement IA avancée :

- **Orchestration de tâches** : Sélectionnez du code et décrivez une tâche
- **Vue de comparaison** : Visualisez les modifications proposées par les agents
- **Streaming en temps réel** : Suivez le progrès des agents via la barre de statut
- **Intégration native** : Menu contextuel et raccourcis clavier
- **Configuration flexible** : URL, timeout et paramètres personnalisables

### 📋 Utilisation

1. **Sélectionner du code** dans l'éditeur
2. **Raccourci clavier** : `Ctrl+Shift+M` (Windows/Linux) ou `Cmd+Shift+M` (Mac)
3. **Menu contextuel** : Clic droit → "Orchestrate with Multi-Agent"
4. **Décrire la tâche** : "Ajouter des tests unitaires et améliorer la documentation"
5. **Visualiser** : Vue de comparaison avec les modifications proposées
6. **Accepter/Rejeter** : Appliquer ou annuler les changements

### ⚙️ Configuration

```json
{
  "multiAgent.orchestratorUrl": "http://localhost:8002/invoke",
  "multiAgent.showDiff": true,
  "multiAgent.timeout": 90000
}
```

### 🔧 Installation de l'extension

```bash
cd cursor_extension
npm install
npm run compile
```

Pour installer l'extension en mode développement :
1. Ouvrir VS Code/Cursor
2. `Ctrl+Shift+P` → "Developer: Install Extension from Location"
3. Sélectionner le dossier `cursor_extension`

## Démarrage avec Docker Compose

### Prérequis

1. Docker et Docker Compose installés
2. Clés API OpenAI et/ou Anthropic

### Configuration

1. Copiez le fichier d'environnement exemple :
```bash
cp env.example .env
```

2. Éditez le fichier `.env` avec vos clés API :
```bash
# Clés API pour les LLMs
OPENAI_API_KEY=votre_clé_openai_ici
ANTHROPIC_API_KEY=votre_clé_anthropic_ici

# Configuration PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mot_de_passe_sécurisé
POSTGRES_DB=agent_memory
```

### Lancement des services

```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier le statut des conteneurs
docker-compose ps

# Consulter les logs
docker-compose logs -f
```

### Services disponibles

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| ChromaDB | 8000 | http://localhost:8000 | Base vectorielle |
| Memory API | 8001 | http://localhost:8001 | API de mémoire hybride |
| Orchestrator | 8002 | http://localhost:8002 | Service d'orchestration |
| PostgreSQL | 5432 | localhost:5432 | Base de données relationnelle |

### Volumes persistants

- `postgres_data` : Données PostgreSQL
- `chroma_data` : Collections et embeddings ChromaDB

### Arrêt des services

```bash
# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes (attention : perte de données)
docker-compose down -v
```

## Workflow de développement

### 1. Démarrer l'infrastructure

```bash
# Lancer les services backend
docker-compose up -d

# Vérifier que tout fonctionne
curl http://localhost:8002/status
```

### 2. Installer l'extension

```bash
cd cursor_extension
npm install
npm run compile
```

### 3. Développer avec l'IA

1. Ouvrir un fichier de code
2. Sélectionner une section
3. `Ctrl+Shift+M` → Décrire la tâche
4. Visualiser et appliquer les modifications

## Développement

Pour plus d'informations sur l'architecture et le développement, consultez les fichiers de livrables :

- `livrable1_structure_projet.md` : Structure du projet
- `livrable3_api_memoire.md` : API de mémoire
- `livrable4_docker_compose.md` : Configuration Docker
- `livrable5_cursor_extension.md` : Extension Cursor 