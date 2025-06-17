
Tu es un ingénieur logiciel expert en systèmes distribués et en IA agentique. 

Ton objectif est de générer l'intégralité du code et de la configuration pour un environnement 

de développement professionnel multi-agents, basé sur l'architecture suivante :



IDE Client : Cursor (VS Code Fork)

Orchestration : LangGraph (modèle Superviseur-Travailleurs)

Services API : FastAPI

Mémoire & RAG : ChromaDB (long terme) et PostgreSQL (court terme/état)

Conteneurisation : Docker & Docker Compose

Intégration & Sécurité : Docker MCP Toolkit

Génère des livrables complets, fonctionnels et prêts pour un déploiement local. Le code doit être robuste, commenté et suivre les meilleures pratiques.



LIVRABLES ATTENDUS



Génère les 6 livrables suivants de manière exhaustive.



---



Livrable 1 : Structure du Projet



Crée une arborescence de fichiers claire pour l'ensemble du projet.



/multi-agent-dev-env

|-- /orchestrator

| |-- /app

| | |-- /agents

| | | |-- init.py

| | | |-- supervisor.py

| | | -- workers.py | | |-- /graph | | | |-- init.py | | | -- state.py

| | |-- init.py

| | -- main.py | |-- Dockerfile | -- requirements.txt

|-- /memory_api

| |-- /app

| | |-- /db

| | | |-- init.py

| | | -- session.py | | |-- /models | | | |-- init.py | | | -- schemas.py

| | |-- /services

| | | |-- init.py

| | | |-- rag_service.py

| | | -- state_service.py | | |-- init.py | | -- main.py

| |-- Dockerfile

| -- requirements.txt |-- /cursor_extension | |-- /src | | -- extension.ts

| |-- package.json

| -- tsconfig.json |-- /codebase_docs | -- sample_doc.md

|--.env

`-- docker-compose.yml



---



Livrable 2 : Service d'Orchestration (LangGraph)



Génère le code Python pour le service orchestrator.



orchestrator/requirements.txt : Inclure langgraph, langchain-openai, langchain-anthropic, fastapi, uvicorn.

orchestrator/app/graph/state.py : Définir la classe AgentState(TypedDict) pour la mémoire partagée du graphe (messages, plan, etc.).

orchestrator/app/agents/workers.py : Créer deux agents travailleurs spécialisés (CodeGenerationAgent, DocumentationAgent) en utilisant create_react_agent de LangGraph, chacun avec un LLM différent (GPT-4o et Claude 3.5 Sonnet) et des outils factices.

orchestrator/app/agents/supervisor.py : Créer l'agent Supervisor qui utilise un LLM puissant (Claude 4 Opus) pour router les tâches vers les travailleurs appropriés en fonction de l'état. Utiliser le package langgraph-supervisor pour une implémentation robuste. [1, 2, 3]

orchestrator/app/main.py :

Construire le StateGraph en assemblant le superviseur et les travailleurs.

Compiler le graphe (app = workflow.compile()).

Exposer ce graphe via une API FastAPI avec un endpoint POST /invoke qui accepte une tâche et retourne un StreamingResponse.

---



Livrable 3 : API de Mémoire Hybride (FastAPI, ChromaDB, PostgreSQL)



Génère le code Python pour le service memory_api.



memory_api/requirements.txt : Inclure fastapi, uvicorn, chromadb, langchain-openai, pydantic, psycopg2-binary, sqlalchemy.

memory_api/app/main.py : Créer une application FastAPI qui expose les endpoints suivants :

POST /rag_query : Accepte une requête, la vectorise et interroge ChromaDB pour une recherche sémantique (RAG). [4, 5]

POST /state/{session_id} : Stocke un état de session (JSON) dans PostgreSQL.

GET /state/{session_id} : Récupère un état de session depuis PostgreSQL.

POST /index_files : Un endpoint pour déclencher l'indexation des fichiers du répertoire codebase_docs dans ChromaDB.

---



Livrable 4 : Configuration Docker Compose



Génère le fichier docker-compose.yml complet.



Définir trois services : orchestrator, memory_api, chromadb. [6, 7]

Utiliser l'image officielle chromadb/chroma pour le service chromadb. [8]

Monter un volume nommé chroma_data pour la persistance de ChromaDB.

Construire les services orchestrator et memory_api à partir de leurs Dockerfiles respectifs.

Utiliser le fichier .env pour gérer les clés d'API et les configurations de base de données.

Configurer les dépendances (depends_on) pour assurer le bon ordre de démarrage.

---



Livrable 5 : Intégration Cursor (Extension VS Code)



Génère les fichiers pour une extension VS Code personnalisée.



cursor_extension/package.json :

Définir un point de contribution pour une nouvelle commande : multiAgent.orchestrateTask.

Définir un événement d'activation onCommand:multiAgent.orchestrateTask.

cursor_extension/src/extension.ts :

Dans la fonction activate, enregistrer la commande multiAgent.orchestrateTask. [9]

Le gestionnaire de commande doit : 1. Obtenir le texte sélectionné dans l'éditeur actif (vscode.window.activeTextEditor). [10, 11] 2. Ouvrir une boîte de dialogue (vscode.window.showInputBox) pour demander à l'utilisateur de décrire la tâche. 3. Effectuer un appel fetch de type POST vers l'endpoint http://localhost:8002/invoke du service orchestrator. [12, 13] 4. Remplacer la sélection de l'éditeur par la réponse de l'API.

---



Livrable 6 : Procédure d'Installation et de Lancement



Génère un fichier README.md avec des instructions claires et détaillées.



Prérequis : Lister les logiciels nécessaires (Docker Desktop, Node.js, Python).

Configuration du Docker MCP Toolkit : Expliquer comment activer le toolkit dans les paramètres de Docker Desktop pour une utilisation future. [14, 15]

Configuration de l'environnement :

Cloner le dépôt.

Créer et configurer le fichier .env à partir d'un exemple (.env.example).

Lancement :

Expliquer comment lancer toute la pile avec une seule commande : docker-compose up --build -d.

Installation de l'extension :

Expliquer comment compiler et installer l'extension VS Code dans Cursor.

Utilisation :

Fournir un exemple de workflow : sélectionner du code, utiliser le raccourci clavier de la nouvelle commande, et décrire une tâche.

Ressources et Bases de Connaissances

Voici une sélection de liens et de dépôts GitHub qui servent de fondation et d'exemples pour chaque composant de l'architecture.

 * Templates de Projets Complets (FastAPI + LangGraph + Docker) :

   * fastapi-langgraph-agent-production-ready-template : Un excellent point de départ pour une architecture de production avec FastAPI et LangGraph, incluant la journalisation, l'observabilité et la sécurité. [16, 17]

   * fastapi-mcp-langgraph-template : Un template moderne qui intègre nativement le protocole MCP, idéal pour l'intégration d'outils. [18]

   * agent-service-toolkit : Un toolkit complet qui inclut une interface Streamlit pour le débogage et l'interaction. [19]

 * Orchestration avec LangGraph Supervisor :

   * Documentation Officielle langgraph-supervisor : La référence pour créer des agents superviseurs hiérarchiques. [1]

   * Exemples de Code (Python & JS) : Dépôts officiels avec des exemples concrets d'implémentation du pattern superviseur. [2, 3]

   * Tutoriels sur les Systèmes Multi-Agents : Guides pas à pas pour construire des systèmes avec des "handoffs" entre agents. [20, 21, 22]

 * API de Mémoire (FastAPI, RAG, ChromaDB) :

   * Exemples de RAG avec FastAPI : Dépôts GitHub montrant comment construire des services RAG avec FastAPI, souvent en utilisant ChromaDB ou FAISS. [4, 5, 23, 24, 25]

   * Déploiement de ChromaDB avec Docker Compose : Guides et fichiers docker-compose.yml de référence pour lancer ChromaDB en tant que service conteneurisé. [8, 6, 7, 26, 27]

 * Intégration et Déploiement (Docker & VS Code) :

   * Docker MCP Toolkit : Documentation officielle pour l'installation, la configuration et l'utilisation du toolkit pour exposer des outils de manière sécurisée. [28, 14, 15, 29, 30]

   * Création de Commandes VS Code : Documentation et tutoriels officiels pour enregistrer des commandes et interagir avec l'éditeur. [9, 31, 32, 33, 34]

   * Appels API depuis une Extension VS Code : Exemples et bonnes pratiques pour effectuer des requêtes REST depuis une extension TypeScript. [35, 12, 13, 36, 37]

   

   *

   Guide d'Implémentation Complète - Environnement Multi-Agents

Vue d'Ensemble

Ce guide fournit l'implémentation complète d'un environnement de développement professionnel multi-agents avec :



IDE Client : Cursor (VS Code Fork)

Orchestration : LangGraph (modèle Superviseur-Travailleurs)

Services API : FastAPI

Mémoire & RAG : ChromaDB (long terme) et PostgreSQL (court terme/état)

Conteneurisation : Docker & Docker Compose

Intégration & Sécurité : Docker MCP Toolkit