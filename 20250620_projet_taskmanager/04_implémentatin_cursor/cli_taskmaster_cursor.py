#!/usr/bin/env python3
"""
🎯 CLI TaskMaster Cursor - Interface Ligne de Commande NextGeneration
Répertoire: 20250620_projet_taskmanager/04_implémentatin_cursor/

Fonctionnalités:
- Lancement tâches individuelles TaskMaster
- Interface CLI simple et intuitive  
- Intégration PostgreSQL UTF-8 résolu
- Configuration environnement Cursor optimisée
- Validation automatique infrastructure
"""

import os
import sys
import json
import logging
import asyncio
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import subprocess
import requests
from dataclasses import dataclass
from enum import Enum
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import chromadb
from chromadb.config import Settings

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class TaskResult:
    task_id: str
    status: TaskStatus
    mission: str
    start_time: datetime
    end_time: Optional[datetime] = None
    result: Optional[str] = None
    error: Optional[str] = None

class TaskMasterCLI:
    """CLI TaskMaster NextGeneration pour environnement Cursor"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Charge la configuration optimisée Cursor"""
        default_config = {
            "postgresql": {
                "host": "localhost",
                "port": 5432,
                "database": "nextgeneration",
                "username": "postgres",
                "password": "postgres",
                "lc_messages": "C"  # Configuration UTF-8 résolue
            },
            "sqlite": {
                "database": "C:/Dev/nextgeneration/20250620_projet_taskmanager/04_implémentatin_cursor/nextgeneration_fallback.db"
            },
            "chromadb": {
                "path": "C:/Dev/nextgeneration/chroma_db",
                "collection": "nextgeneration"
            },
            "ollama": {
                "host": "localhost",
                "port": 11434,
                "default_model": "llama3.2:3b"
            },
            "memory_api": {
                "host": "localhost",
                "port": 8001
            },
            "lm_studio": {
                "host": "localhost",
                "port": 1234
            },
            "taskmaster": {
                "timeout": 300,
                "max_retries": 3,
                "auto_validate": True
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def _setup_logging(self) -> logging.Logger:
        """Configure le logging CLI"""
        logger = logging.getLogger('TaskMasterCLI')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Handler console
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - 🎯 CLI - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # Handler fichier
            os.makedirs("logs", exist_ok=True)
            file_handler = logging.FileHandler(
                f"logs/cli_taskmaster_{self.session_id}.log", 
                encoding='utf-8'
            )
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        return logger

    async def validate_infrastructure(self) -> bool:
        """Validation rapide infrastructure avant lancement tâche"""
        try:
            self.logger.info("🔍 Validation infrastructure...")
            
            # Test PostgreSQL UTF-8
            config = self.config['postgresql']
            dsn = f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            engine = create_engine(dsn, client_encoding='utf8')
            
            with engine.connect() as conn:
                # Vérifier lc_messages = 'C'
                result = conn.execute(text("SHOW lc_messages"))
                lc_messages = result.scalar()
                
                if lc_messages != 'C':
                    self.logger.warning(f"⚠️ lc_messages = '{lc_messages}', recommandé: 'C'")
                    self.logger.info("💡 Exécuter: python fix_postgresql_utf8_cursor.py")
                
                # Test UTF-8
                conn.execute(text("SELECT 'Test français éàùç' as test_utf8"))
                self.logger.info("✅ PostgreSQL UTF-8 validé")
            
            # Test Memory API
            memory_config = self.config['memory_api']
            memory_url = f"http://{memory_config['host']}:{memory_config['port']}"
            
            try:
                response = requests.get(f"{memory_url}/health", timeout=5)
                if response.status_code == 200:
                    self.logger.info("✅ Memory API disponible")
                else:
                    self.logger.warning("⚠️ Memory API non accessible")
            except:
                self.logger.warning("⚠️ Memory API non disponible - utilisation SQLite fallback")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Validation infrastructure échouée: {str(e)}")
            return False

    async def launch_single_task(self, mission: str, instance_id: Optional[str] = None, 
                                model: Optional[str] = None) -> TaskResult:
        """Lance une tâche unique TaskMaster"""
        task_id = instance_id or f"task_{self.session_id}_{datetime.now().strftime('%H%M%S')}"
        start_time = datetime.now()
        
        self.logger.info(f"🚀 Lancement tâche: {task_id}")
        self.logger.info(f"📝 Mission: {mission}")
        
        try:
            # Validation infrastructure
            if self.config['taskmaster']['auto_validate']:
                if not await self.validate_infrastructure():
                    raise Exception("Infrastructure non validée")
            
            # Préparation de la tâche
            task_data = {
                "task_id": task_id,
                "mission": mission,
                "start_time": start_time.isoformat(),
                "model": model or self.config['ollama']['default_model'],
                "config": self.config
            }
            
            # Simulation traitement TaskMaster
            # Note: Intégration complète nécessiterait l'agent TaskMaster réel
            await asyncio.sleep(2)  # Simulation temps traitement
            
            # Sauvegarde en base
            await self._save_task_to_database(task_data)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result = TaskResult(
                task_id=task_id,
                status=TaskStatus.COMPLETED,
                mission=mission,
                start_time=start_time,
                end_time=end_time,
                result=f"Tâche simulée complétée en {duration:.2f}s"
            )
            
            self.logger.info(f"✅ Tâche {task_id} complétée avec succès")
            return result
            
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"❌ Erreur tâche {task_id}: {error_msg}")
            
            return TaskResult(
                task_id=task_id,
                status=TaskStatus.FAILED,
                mission=mission,
                start_time=start_time,
                end_time=datetime.now(),
                error=error_msg
            )

    async def _save_task_to_database(self, task_data: Dict[str, Any]) -> None:
        """Sauvegarde la tâche en base PostgreSQL ou SQLite fallback"""
        try:
            # Tentative PostgreSQL
            config = self.config['postgresql']
            dsn = f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            engine = create_engine(dsn, client_encoding='utf8')
            
            with engine.connect() as conn:
                # Création table si nécessaire
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS taskmaster_tasks (
                        id SERIAL PRIMARY KEY,
                        task_id VARCHAR(100) UNIQUE,
                        mission TEXT,
                        start_time TIMESTAMP,
                        model VARCHAR(100),
                        config JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Insertion
                conn.execute(text("""
                    INSERT INTO taskmaster_tasks (task_id, mission, start_time, model, config)
                    VALUES (:task_id, :mission, :start_time, :model, :config)
                    ON CONFLICT (task_id) DO UPDATE SET
                        mission = EXCLUDED.mission,
                        start_time = EXCLUDED.start_time
                """), {
                    'task_id': task_data['task_id'],
                    'mission': task_data['mission'],
                    'start_time': task_data['start_time'],
                    'model': task_data['model'],
                    'config': json.dumps(task_data['config'])
                })
                
                conn.commit()
                self.logger.info("💾 Tâche sauvegardée en PostgreSQL")
                
        except Exception as e:
            # Fallback SQLite
            self.logger.warning(f"PostgreSQL indisponible, fallback SQLite: {str(e)}")
            
            sqlite_path = self.config['sqlite']['database']
            os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
            
            conn = sqlite3.connect(sqlite_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS taskmaster_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE,
                    mission TEXT,
                    start_time TEXT,
                    model TEXT,
                    config TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                INSERT OR REPLACE INTO taskmaster_tasks 
                (task_id, mission, start_time, model, config)
                VALUES (?, ?, ?, ?, ?)
            """, (
                task_data['task_id'],
                task_data['mission'],
                task_data['start_time'],
                task_data['model'],
                json.dumps(task_data['config'])
            ))
            
            conn.commit()
            conn.close()
            self.logger.info("💾 Tâche sauvegardée en SQLite (fallback)")

    async def list_tasks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Liste les dernières tâches"""
        try:
            # Tentative PostgreSQL
            config = self.config['postgresql']
            dsn = f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            engine = create_engine(dsn, client_encoding='utf8')
            
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT task_id, mission, start_time, model, created_at
                    FROM taskmaster_tasks 
                    ORDER BY created_at DESC 
                    LIMIT :limit
                """), {'limit': limit})
                
                return [dict(row._mapping) for row in result]
                
        except:
            # Fallback SQLite
            sqlite_path = self.config['sqlite']['database']
            if not os.path.exists(sqlite_path):
                return []
            
            conn = sqlite3.connect(sqlite_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT task_id, mission, start_time, model, created_at
                FROM taskmaster_tasks 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            
            columns = ['task_id', 'mission', 'start_time', 'model', 'created_at']
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            conn.close()
            return results

    def print_task_result(self, result: TaskResult) -> None:
        """Affiche le résultat d'une tâche"""
        print("\n" + "="*60)
        print("🎯 RÉSULTAT TÂCHE TASKMASTER")
        print("="*60)
        
        status_emoji = {
            TaskStatus.COMPLETED: "✅",
            TaskStatus.FAILED: "❌",
            TaskStatus.RUNNING: "🔄",
            TaskStatus.PENDING: "⏳",
            TaskStatus.CANCELLED: "⚠️"
        }
        
        emoji = status_emoji.get(result.status, "❓")
        print(f"{emoji} ID: {result.task_id}")
        print(f"📝 Mission: {result.mission}")
        print(f"⏰ Début: {result.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if result.end_time:
            duration = (result.end_time - result.start_time).total_seconds()
            print(f"⏱️ Durée: {duration:.2f}s")
        
        if result.result:
            print(f"✅ Résultat: {result.result}")
        
        if result.error:
            print(f"❌ Erreur: {result.error}")
        
        print("="*60)

    def save_report(self, result: TaskResult, filename: Optional[str] = None) -> str:
        """Sauvegarde le rapport de tâche"""
        if not filename:
            filename = f"rapport_tache_{result.task_id}.md"
        
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# 🎯 Rapport Tâche TaskMaster - {result.task_id}\n\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mission**: {result.mission}\n")
            f.write(f"**Statut**: {result.status.value}\n")
            f.write(f"**Début**: {result.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            if result.end_time:
                duration = (result.end_time - result.start_time).total_seconds()
                f.write(f"**Durée**: {duration:.2f}s\n")
            
            if result.result:
                f.write(f"\n## ✅ Résultat\n{result.result}\n")
            
            if result.error:
                f.write(f"\n## ❌ Erreur\n{result.error}\n")
        
        self.logger.info(f"📄 Rapport sauvegardé: {filepath}")
        return filepath


def create_cli() -> argparse.ArgumentParser:
    """Crée l'interface CLI"""
    parser = argparse.ArgumentParser(
        description="🎯 TaskMaster CLI - Interface Ligne de Commande NextGeneration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python cli_taskmaster_cursor.py launch "Analyser le fichier data.csv"
  python cli_taskmaster_cursor.py launch "Créer un rapport" --model llama3.2:7b
  python cli_taskmaster_cursor.py list                    # Lister tâches récentes
  python cli_taskmaster_cursor.py validate              # Valider infrastructure
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
    
    # Commande launch
    launch_parser = subparsers.add_parser('launch', help='Lance une tâche TaskMaster')
    launch_parser.add_argument('mission', help='Description de la mission à accomplir')
    launch_parser.add_argument('--id', help='ID personnalisé pour la tâche')
    launch_parser.add_argument('--model', help='Modèle IA à utiliser')
    launch_parser.add_argument('--config', '-c', help='Fichier de configuration JSON')
    launch_parser.add_argument('--output', '-o', help='Fichier de sortie pour le rapport')
    launch_parser.add_argument('--no-report', action='store_true', help='Pas de rapport automatique')
    
    # Commande list
    list_parser = subparsers.add_parser('list', help='Liste les tâches récentes')
    list_parser.add_argument('--limit', type=int, default=10, help='Nombre de tâches à afficher')
    list_parser.add_argument('--config', '-c', help='Fichier de configuration JSON')
    
    # Commande validate
    validate_parser = subparsers.add_parser('validate', help='Valide l\'infrastructure')
    validate_parser.add_argument('--config', '-c', help='Fichier de configuration JSON')
    
    return parser


async def main():
    """Fonction principale CLI"""
    parser = create_cli()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = TaskMasterCLI(args.config)
    
    if args.command == 'launch':
        print(f"🚀 Lancement TaskMaster: {args.mission}")
        
        result = await cli.launch_single_task(
            mission=args.mission,
            instance_id=args.id,
            model=args.model
        )
        
        cli.print_task_result(result)
        
        if not args.no_report:
            report_path = cli.save_report(result, args.output)
            print(f"\n📄 Rapport: {report_path}")
    
    elif args.command == 'list':
        print("📋 Tâches récentes TaskMaster:")
        tasks = await cli.list_tasks(args.limit)
        
        if not tasks:
            print("Aucune tâche trouvée.")
            return
        
        print("\n" + "-"*80)
        for task in tasks:
            print(f"🎯 {task['task_id']} | {task['mission'][:50]}{'...' if len(task['mission']) > 50 else ''}")
            print(f"   📅 {task['created_at']} | 🤖 {task['model']}")
        print("-"*80)
        print(f"Total: {len(tasks)} tâches")
    
    elif args.command == 'validate':
        print("🔍 Validation infrastructure TaskMaster...")
        is_valid = await cli.validate_infrastructure()
        
        if is_valid:
            print("✅ Infrastructure validée - Prêt pour les tâches TaskMaster")
        else:
            print("❌ Infrastructure non validée - Vérifier les composants")
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 



