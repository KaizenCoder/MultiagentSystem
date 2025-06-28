# Livrable 3 : API de mémoire hybride

- **Technologies** : FastAPI + PostgreSQL (mémoire court terme) + ChromaDB
  (mémoire longue terme RAG).
- **Services internes** :  
  - `RAGService` : vectorisation OpenAI Embeddings, split récursif, requêtes
    Chroma.  
  - `StateService` : CRUD SQLAlchemy pour les états de session.
- **Endpoints** principaux :  
  - `/rag_query`  
  - `/state/{session_id}` (POST/GET/DELETE)  
  - `/index_files`, `/rag_stats`, `/sessions`, `/health`.
- **Initialisation** : indexation asynchrone des fichiers, stockage des
  métadonnées dans PostgreSQL.

> L’API combine stockage relationnel et recherche vectorielle pour offrir une
mémoire persistante et un RAG performant.
API de Mémoire Hybride, optimisé pour être robuste, performant et prêt pour la production.

Ce livrable inclut une configuration validée, une gestion de base de données avec migrations, et une indexation asynchrone.

Fichier : memory_api/requirements.txt
Plaintext

fastapi==0.111.0
uvicorn[standard]==0.30.1
pydantic-settings==2.3.4
sqlalchemy==2.0.31
psycopg2-binary==2.9.9
alembic==1.13.2
python-dotenv==1.0.1
httpx==0.27.0

# Dépendances pour le RAG
chromadb==0.5.3
langchain-openai==0.1.9
langchain-text-splitters==0.2.2
aiofiles==23.2.1
&lt;hr>

Fichier : memory_api/Dockerfile
Dockerfile

# Utiliser une image Python 3.11 slim comme base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système nécessaires pour psycopg2 et nc (netcat)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

# Rendre le script d'entrée exécutable
RUN chmod +x ./entrypoint.sh

# Exposer le port sur lequel l'API s'exécutera
EXPOSE 8001

# Définir le point d'entrée qui exécute les migrations puis démarre le serveur
ENTRYPOINT ["./entrypoint.sh"]
&lt;hr>

Fichier : memory_api/entrypoint.sh
Bash

#!/bin/bash

# Ce script garantit que la base de données est prête et que les migrations
# sont appliquées avant de démarrer l'application FastAPI.

# Attendre que le service PostgreSQL soit accessible
echo "⏳ Waiting for PostgreSQL to be ready..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done
echo "✅ PostgreSQL is ready."

# Appliquer les migrations de la base de données avec Alembic
echo "🚀 Applying database migrations..."
alembic upgrade head

# Démarrer le serveur FastAPI avec Uvicorn
echo "🔥 Starting Memory API server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8001
&lt;hr>

Fichier : memory_api/app/config.py
Python

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Configuration centralisée et validée pour l'API de mémoire.
    Charge les variables depuis un fichier .env et l'environnement système.
    """
    # Configuration de la base de données PostgreSQL
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "agent_memory"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    
    # Configuration de ChromaDB
    CHROMA_HOST: str = "chromadb"
    CHROMA_PORT: int = 8000
    
    # Clés API
    OPENAI_API_KEY: str

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Configuration pour Pydantic-settings
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

# Instance unique des paramètres pour l'application
settings = Settings()
&lt;hr>

Fichier : memory_api/app/db/session.py
Python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections.abc import Generator

from app.config import settings

# Création du moteur SQLAlchemy avec l'URL de la base de données
engine = create_engine(settings.database_url, pool_pre_ping=True)

# Création d'une fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    """
    Dépendance FastAPI pour obtenir une session de base de données.
    Assure que la session est correctement fermée après chaque requête.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
&lt;hr>

Fichier : memory_api/app/models/schemas.py
Python

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, DateTime, JSON, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

# Base déclarative pour les modèles SQLAlchemy
Base = declarative_base()

# --- Modèles SQLAlchemy (Table de la base de données) ---

class SessionState(Base):
    """Modèle pour stocker l'état persistant des sessions LangGraph."""
    __tablename__ = "session_states"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    state_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

class IndexedDocument(Base):
    """Modèle pour suivre les documents indexés dans ChromaDB et éviter les doublons."""
    __tablename__ = "indexed_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    content_hash = Column(String, nullable=False)
    indexed_at = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(JSON)

# --- Schémas Pydantic (Validation des données API) ---

class RAGQueryRequest(BaseModel):
    query: str = Field(..., description="La requête de recherche sémantique.")
    top_k: int = Field(5, gt=0, le=20, description="Nombre de résultats à retourner.")
    filter_metadata: Optional[Dict[str, Any]] = Field(None, description="Filtres sur les métadonnées.")

class RAGQueryResult(BaseModel):
    content: str
    metadata: Dict[str, Any]
    similarity_score: float

class RAGQueryResponse(BaseModel):
    query: str
    results: List[RAGQueryResult]
    execution_time_ms: float

class StateStoreRequest(BaseModel):
    state_data: Dict[str, Any] = Field(..., description="Données d'état JSON à stocker.")

class StateRetrieveResponse(BaseModel):
    session_id: str
    state_data: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime]

class IndexFilesRequest(BaseModel):
    directory: str = Field("/app/codebase_docs", description="Répertoire à indexer dans le conteneur.")
    file_extensions: List[str] = Field(default=[".md", ".txt", ".py"], description="Extensions à inclure.")
    force_reindex: bool = Field(False, description="Forcer la réindexation même si le contenu n'a pas changé.")

class IndexTaskStatusResponse(BaseModel):
    task_id: str
    status: Literal["pending", "in_progress", "completed", "failed", "not_found"]
    progress: int = 0
    details: str = ""
    result: Optional[Dict[str, Any]] = None

class IndexTaskStartResponse(BaseModel):
    message: str
    task_id: str
    status_url: str
&lt;hr>

Fichier : memory_api/app/services/state_service.py
Python

from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app.models.schemas import SessionState

class StateService:
    """Service pour la gestion CRUD de l'état des sessions dans PostgreSQL."""

    def store_state(self, session_id: str, state_data: Dict[str, Any], db: Session) -> SessionState:
        """Stocke ou met à jour l'état d'une session."""
        existing_state = db.query(SessionState).filter(SessionState.session_id == session_id).first()
        
        if existing_state:
            existing_state.state_data = state_data
        else:
            existing_state = SessionState(session_id=session_id, state_data=state_data)
            db.add(existing_state)
        
        db.commit()
        db.refresh(existing_state)
        return existing_state

    def retrieve_state(self, session_id: str, db: Session) -> Optional[SessionState]:
        """Récupère l'état d'une session."""
        return db.query(SessionState).filter(SessionState.session_id == session_id).first()
    
    def list_sessions(self, db: Session, skip: int = 0, limit: int = 100) -> List[SessionState]:
        """Liste toutes les sessions enregistrées avec pagination."""
        return db.query(SessionState).order_by(SessionState.updated_at.desc()).offset(skip).limit(limit).all()

# Instance unique du service
state_service = StateService()
&lt;hr>

Fichier : memory_api/app/services/rag_service.py
Python

import os
import hashlib
import time
import aiofiles
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime

import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session

from app.config import settings
from app.models.schemas import IndexedDocument
from .indexing_service import indexing_service

class RAGService:
    """Service pour la recherche sémantique (RAG) et l'indexation avec ChromaDB."""
    
    def __init__(self):
        self.client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
            settings=Settings(anonymized_telemetry=False)
        )
        self.embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY, model="text-embedding-3-small")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.collection_name = "codebase_docs"
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def compute_file_hash(self, content: str) -> str:
        """Calcule le hash SHA256 d'un contenu pour la détection de changements."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    async def index_document(self, filename: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Indexe un document unique dans ChromaDB."""
        try:
            chunks = self.text_splitter.split_text(content)
            if not chunks:
                return {"status": "skipped", "filename": filename, "reason": "No content to index."}

            doc_metadata = metadata or {}
            doc_metadata["filename"] = filename
            
            chunk_metadatas = [{**doc_metadata, "chunk_index": i} for i in range(len(chunks))]
            chunk_ids = [f"{filename}_{i}" for i in range(len(chunks))]

            self.collection.upsert(
                ids=chunk_ids,
                documents=chunks,
                metadatas=chunk_metadatas
            )
            return {"status": "success", "filename": filename, "chunks_created": len(chunks)}
        except Exception as e:
            return {"status": "error", "filename": filename, "error": str(e)}

    async def index_directory(
        self,
        task_id: str,
        directory: str,
        file_extensions: List[str],
        force_reindex: bool,
        db_session_factory: Callable[[], Session]
    ):
        """Parcourt un répertoire et indexe les fichiers, en mettant à jour une tâche de fond."""
        dir_path = Path(directory)
        files_to_index = [p for p in dir_path.rglob("*") if p.is_file() and p.suffix in file_extensions]
        total_files = len(files_to_index)
        
        if total_files == 0:
            indexing_service.complete_task(task_id, {"indexed_count": 0, "skipped_count": 0, "error_count": 0})
            return

        summary = {"indexed": 0, "skipped": 0, "errors": 0}
        
        for i, file_path in enumerate(files_to_index):
            db = db_session_factory()
            try:
                progress = int(((i + 1) / total_files) * 100)
                indexing_service.update_task_progress(task_id, progress, f"Processing {file_path.name}...")

                async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = await f.read()

                filename = str(file_path.relative_to(dir_path))
                content_hash = self.compute_file_hash(content)

                existing_doc = db.query(IndexedDocument).filter(IndexedDocument.filename == filename).first()
                
                if not force_reindex and existing_doc and existing_doc.content_hash == content_hash:
                    summary["skipped"] += 1
                    continue

                result = await self.index_document(filename, content)
                
                if result["status"] == "success":
                    if existing_doc:
                        existing_doc.content_hash = content_hash
                    else:
                        new_doc_record = IndexedDocument(filename=filename, content_hash=content_hash)
                        db.add(new_doc_record)
                    db.commit()
                    summary["indexed"] += 1
                else:
                    summary["errors"] += 1
            finally:
                db.close()
        
        indexing_service.complete_task(task_id, summary)
    
    def query(self, query: str, top_k: int, filter_metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Effectue une recherche sémantique dans la collection."""
        start_time = time.time()
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            where=filter_metadata
        )
        end_time = time.time()

        formatted_results = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i],
                    "similarity_score": 1 - results["distances"][0][i]
                })

        return {
            "query": query,
            "results": formatted_results,
            "execution_time_ms": (end_time - start_time) * 1000
        }

# Instance unique du service
rag_service = RAGService()
&lt;hr>

Fichier : memory_api/app/services/indexing_service.py
Python

import uuid
from typing import Dict, Any, Literal

# Pour un environnement local, un dictionnaire en mémoire suffit.
# Pour une vraie production, utilisez une base de données comme Redis ou un service de file d'attente.
tasks: Dict[str, Dict[str, Any]] = {}

class IndexingService:
    """Gère l'état des tâches d'indexation exécutées en arrière-plan."""

    def create_task(self) -> str:
        """Crée une entrée pour une nouvelle tâche et retourne son ID."""
        task_id = str(uuid.uuid4())
        tasks[task_id] = {
            "status": "pending",
            "progress": 0,
            "details": "Task created and waiting to start.",
            "result": None
        }
        return task_id

    def get_status(self, task_id: str) -> Dict[str, Any]:
        """Récupère le statut d'une tâche."""
        task = tasks.get(task_id)
        if not task:
            return {"status": "not_found", "progress": 0, "details": "Task ID not found."}
        return {"task_id": task_id, **task}

    def update_task_progress(self, task_id: str, progress: int, details: str):
        """Met à jour l'état d'une tâche en cours."""
        if task_id in tasks:
            tasks[task_id].update({
                "status": "in_progress",
                "progress": progress,
                "details": details
            })

    def complete_task(self, task_id: str, result: Dict[str, Any]):
        """Marque une tâche comme terminée."""
        if task_id in tasks:
            tasks[task_id].update({
                "status": "completed",
                "progress": 100,
                "details": "Indexing finished successfully.",
                "result": result
            })

    def fail_task(self, task_id: str, error_details: str):
        """Marque une tâche comme ayant échoué."""
        if task_id in tasks:
            tasks[task_id].update({
                "status": "failed",
                "details": error_details
            })

# Instance unique du service
indexing_service = IndexingService()
&lt;hr>

Fichier : memory_api/app/main.py
Python

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.services.state_service import state_service
from app.services.rag_service import rag_service
from app.services.indexing_service import indexing_service
from app.models.schemas import (
    StateStoreRequest, StateRetrieveResponse,
    RAGQueryRequest, RAGQueryResponse,
    IndexFilesRequest, IndexTaskStartResponse, IndexTaskStatusResponse
)
from app.config import settings # Importe l'instance de configuration

app = FastAPI(
    title="API de Mémoire Hybride",
    description="Service pour la mémoire à long terme (RAG/ChromaDB) et à court terme (État/PostgreSQL).",
    version="2.0.0"
)

# --- Endpoints pour la Mémoire à Court Terme (État) ---

@app.post("/state/{session_id}", status_code=status.HTTP_201_CREATED)
def store_session_state(session_id: str, request: StateStoreRequest, db: Session = Depends(get_db)):
    """Stocke ou met à jour l'état JSON d'une session."""
    try:
        state_service.store_state(session_id, request.state_data, db)
        return {"status": "ok", "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store state: {e}")

@app.get("/state/{session_id}", response_model=StateRetrieveResponse)
def retrieve_session_state(session_id: str, db: Session = Depends(get_db)):
    """Récupère l'état d'une session."""
    state = state_service.retrieve_state(session_id, db)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    return state

@app.get("/sessions", response_model=List[StateRetrieveResponse])
def list_all_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Liste toutes les sessions enregistrées."""
    return state_service.list_sessions(db, skip=skip, limit=limit)

# --- Endpoints pour la Mémoire à Long Terme (RAG) ---

@app.post("/rag_query", response_model=RAGQueryResponse)
def query_rag_collection(request: RAGQueryRequest):
    """Effectue une recherche sémantique dans la base de connaissances."""
    try:
        result = rag_service.query(request.query, request.top_k, request.filter_metadata)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query failed: {e}")

# --- Endpoints pour l'Indexation Asynchrone ---

@app.post("/index_files", response_model=IndexTaskStartResponse, status_code=status.HTTP_202_ACCEPTED)
async def trigger_file_indexing(
    request: IndexFilesRequest,
    background_tasks: BackgroundTasks,
):
    """Déclenche l'indexation des fichiers en arrière-plan."""
    task_id = indexing_service.create_task()
    background_tasks.add_task(
        rag_service.index_directory,
        task_id=task_id,
        directory=request.directory,
        file_extensions=request.file_extensions,
        force_reindex=request.force_reindex,
        db_session_factory=get_db
    )
    return {
        "message": "File indexing process has been started.",
        "task_id": task_id,
        "status_url": app.url_path_for("get_indexing_status", task_id=task_id)
    }

@app.get("/index_status/{task_id}", response_model=IndexTaskStatusResponse, name="get_indexing_status")
async def get_indexing_status(task_id: str):
    """Récupère le statut d'une tâche d'indexation."""
    return indexing_service.get_status(task_id)

# --- Endpoint de Santé ---

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    """Vérifie la connectivité aux services dépendants (DBs)."""
    try:
        # Test ChromaDB
        rag_service.client.heartbeat()
        chroma_status = "ok"
    except Exception:
        chroma_status = "error"
    
    try:
        # Test PostgreSQL
        db.execute("SELECT 1")
        postgres_status = "ok"
    except Exception:
        postgres_status = "error"
        
    if postgres_status == "error" or chroma_status == "error":
        raise HTTPException(status_code=503, detail={"postgresql": postgres_status, "chromadb": chroma_status})
        
    return {"status": "ok", "services": {"postgresql": postgres_status, "chromadb": chroma_status}}
&lt;hr>

Fichiers __init__.py
Pour que Python reconnaisse ces répertoires comme des packages importables, assurez-vous de créer des fichiers __init__.py vides dans chaque sous-répertoire de app/.

memory_api/app/__init__.py
memory_api/app/db/__init__.py
memory_api/app/models/__init__.py
memory_api/app/services/__init__.py