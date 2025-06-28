#!/usr/bin/env python3
"""
Orchestrateur NextGeneration - Version SQLite Simple
Contourne PostgreSQL, utilise SQLite pour dmarrage immdiat
Configuration termine par IA-2, adapte pour environnement Windows
"""

import sys
import os
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Configuration FastAPI simple
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio

# Configuration
app = FastAPI(
    title="[ROCKET] Orchestrateur NextGeneration",
    description="Orchestrateur Multi-Agent avec SQLite",
    version="1.0.0"
)

# Modles Pydantic
class TaskRequest(BaseModel):
    task: str
    priority: str = "normal"
    context: Optional[str] = None
    agent: Optional[str] = "auto"

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[str] = None
    agent_used: Optional[str] = None
    execution_time: Optional[float] = None

class SystemStatus(BaseModel):
    status: str
    database: str
    memory_api: str
    active_tasks: int
    total_completed: int
    uptime: str

# Configuration SQLite
DB_PATH = Path("orchestrator_data.db")

class SimpleDatabase:
    """Base de donnes SQLite simple pour l'orchestrateur"""
    
    def __init__(self):
        self.db_path = DB_PATH
        self._init_database()
    
    def _init_database(self):
        """Initialise la base SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Table des tches
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE,
                    task_content TEXT,
                    priority TEXT,
                    status TEXT,
                    agent_used TEXT,
                    result TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    execution_time REAL
                )
            """)
            
            # Table de configuration
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT,
                    message TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            print("[CHECK] Base de donnes SQLite initialise")
            
        except Exception as e:
            print(f"[CROSS] Erreur initialisation DB: {e}")
    
    def add_task(self, task_id: str, task_content: str, priority: str = "normal") -> bool:
        """Ajoute une tche"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (task_id, task_content, priority, status, agent_used)
                VALUES (?, ?, ?, 'pending', 'auto')
            """, (task_id, task_content, priority))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[CROSS] Erreur ajout tche: {e}")
            return False
    
    def update_task(self, task_id: str, status: str, result: str = None, execution_time: float = None) -> bool:
        """Met  jour une tche"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if status == "completed":
                cursor.execute("""
                    UPDATE tasks 
                    SET status = ?, result = ?, execution_time = ?, completed_at = CURRENT_TIMESTAMP
                    WHERE task_id = ?
                """, (status, result, execution_time, task_id))
            else:
                cursor.execute("""
                    UPDATE tasks SET status = ? WHERE task_id = ?
                """, (status, task_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[CROSS] Erreur mise  jour tche: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Rcupre les statistiques"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Compte des tches
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
            active_tasks = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
            completed_tasks = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "active_tasks": active_tasks,
                "completed_tasks": completed_tasks,
                "database_status": "operational"
            }
        except Exception as e:
            print(f"[CROSS] Erreur stats: {e}")
            return {"error": str(e)}

# Instance base de donnes
db = SimpleDatabase()
start_time = datetime.now()

# Simulateur d'agents simple
class SimpleAgentOrchestrator:
    """Orchestrateur d'agents simplifi"""
    
    def __init__(self):
        self.agents = {
            "ia1": "Agent IA-1 (Communication, Coordination)", 
            "ia2": "Agent IA-2 (Architecture, Production)",
            "auto": "Slection automatique"
        }
    
    async def process_task(self, task: str, priority: str = "normal", agent: str = "auto") -> Dict[str, Any]:
        """Traite une tche"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Ajoute  la base
        db.add_task(task_id, task, priority)
        
        # Simulation de traitement
        await asyncio.sleep(0.5)  # Simule le travail
        
        # Slection d'agent
        if agent == "auto":
            if any(keyword in task.lower() for keyword in ["database", "postgresql", "performance", "architecture"]):
                selected_agent = "ia2"
            elif any(keyword in task.lower() for keyword in ["communication", "coordination", "test"]):
                selected_agent = "ia1"
            else:
                selected_agent = "ia1"  # Par dfaut
        else:
            selected_agent = agent
        
        # Rsultat simul
        result = f"[CHECK] Tche traite par {self.agents[selected_agent]}: {task[:100]}..."
        
        # Met  jour la base
        db.update_task(task_id, "completed", result, 0.5)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "result": result,
            "agent_used": selected_agent,
            "execution_time": 0.5
        }

# Instance orchestrateur
orchestrator = SimpleAgentOrchestrator()

# =====================================
# ENDPOINTS API
# =====================================

@app.get("/health")
async def health_check():
    """Point de sant de l'API"""
    return {
        "status": "ok",
        "service": "NextGeneration Orchestrator",
        "version": "1.0.0",
        "database": "sqlite",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/status")
async def get_system_status():
    """Statut dtaill du systme"""
    stats = db.get_stats()
    uptime = datetime.now() - start_time
    
    return SystemStatus(
        status="operational",
        database="sqlite_ready",
        memory_api="http://localhost:8001",
        active_tasks=stats.get("active_tasks", 0),
        total_completed=stats.get("completed_tasks", 0),
        uptime=str(uptime).split('.')[0]
    )

@app.post("/process", response_model=TaskResponse)
async def process_task(request: TaskRequest):
    """Traite une tche via l'orchestrateur"""
    try:
        result = await orchestrator.process_task(
            task=request.task,
            priority=request.priority,
            agent=request.agent
        )
        
        return TaskResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur traitement: {str(e)}")

@app.get("/demo")
async def demo_endpoint():
    """Endpoint de dmonstration"""
    demo_tasks = [
        "Analyser les performances de la base de donnes",
        "Coordonner la communication entre IA-1 et IA-2", 
        "Optimiser l'architecture PostgreSQL",
        "Valider les tests de scurit"
    ]
    
    results = []
    for task in demo_tasks:
        result = await orchestrator.process_task(task)
        results.append({
            "task": task,
            "result": result["result"],
            "agent": result["agent_used"]
        })
    
    return {
        "demo": "Orchestrateur NextGeneration",
        "tasks_processed": len(results),
        "results": results,
        "configuration": "PostgreSQL configur par IA-2, SQLite pour dmarrage"
    }

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "service": "[ROCKET] Orchestrateur NextGeneration",
        "status": "Oprationnel",
        "configuration": "PostgreSQL configur par IA-2",
        "database_current": "SQLite (dmarrage rapide)",
        "endpoints": {
            "health": "/health",
            "status": "/status", 
            "process": "/process (POST)",
            "demo": "/demo"
        },
        "next_steps": [
            "1. Configurer PostgreSQL selon IA-2",
            "2. Crer fichier .env avec identifiants",
            "3. Migrer de SQLite vers PostgreSQL",
            "4. Tests de charge complets"
        ]
    }

# =====================================
# DMARRAGE
# =====================================

if __name__ == "__main__":
    print("[ROCKET] Dmarrage Orchestrateur NextGeneration (SQLite)")
    print("[CHECK] Configuration PostgreSQL par IA-2 : Disponible") 
    print("[TOOL] Base actuelle : SQLite (dmarrage rapide)")
    print("[CLIPBOARD] Endpoints : /health /status /process /demo")
    print("[TARGET] Port : 8004 (vite les conflits)")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=8004, log_level="info")
    except Exception as e:
        print(f"[CROSS] Erreur dmarrage: {e}")
        print("[BULB] Essayez un autre port ou vrifiez les permissions") 



