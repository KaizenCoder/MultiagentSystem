# Livrable 1 : Structure du projet

- **Arborescence complète** :  
  - Deux services Python : `/orchestrator`, `/memory_api`  
  - Une extension VS Code : `/cursor_extension`  
  - Dossier `docs`, fichier `.env`, `docker-compose.yml`.

- **Services** : chaque dossier contient :  
  - `Dockerfile` dédié  
  - Sources organisées (`/app/agents`, `/app/graph`, `/app/db`, …)  
  - `requirements.txt`.

> Cette structure isole clairement les responsabilités, simplifie la
containerisation et assure la portabilité du projet.
Livrable 1 : Structure du Projet
/multi-agent-dev-env
|-- /orchestrator
|   |-- /app
|   |   |-- /agents
|   |   |   |-- __init__.py
|   |   |   |-- supervisor.py
|   |   |   |-- workers.py
|   |   |-- /graph
|   |   |   |-- __init__.py
|   |   |   |-- state.py
|   |   |-- __init__.py
|   |   |-- main.py
|   |-- Dockerfile
|   |-- requirements.txt
|-- /memory_api
|   |-- /app
|   |   |-- /db
|   |   |   |-- __init__.py
|   |   |   |-- session.py
|   |   |-- /models
|   |   |   |-- __init__.py
|   |   |   |-- schemas.py
|   |   |-- /services
|   |   |   |-- __init__.py
|   |   |   |-- rag_service.py
|   |   |   |-- state_service.py
|   |   |-- __init__.py
|   |   |-- main.py
|   |-- Dockerfile
|   |-- requirements.txt
|-- /cursor_extension
|   |-- /src
|   |   |-- extension.ts
|   |-- package.json
|   |-- tsconfig.json
|-- /codebase_docs
|   |-- sample_doc.md
|-- .env.example
|-- .env
|-- docker-compose.yml
|-- README.md