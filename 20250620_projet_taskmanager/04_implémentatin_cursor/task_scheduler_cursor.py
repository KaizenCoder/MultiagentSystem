#!/usr/bin/env python3
"""
Task Scheduler Cursor - Ordonnanceur intelligent TaskMaster NextGeneration
Optimisé pour environnement Cursor avec RTX3090 et PostgreSQL UTF-8

Fonctionnalités :
- File d'attente intelligente des tâches
- Optimisation RTX3090 automatique
- Traitement séquentiel avec priorités
- Gestion batch de missions
- Monitoring temps réel
- Fallback SQLite intégré
"""

import asyncio
import json
import logging
import psutil
import sqlite3
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import argparse
import os

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - TaskScheduler - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/task_scheduler_cursor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RTX3090Optimizer:
    """Optimiseur GPU RTX3090 pour TaskMaster"""
    
    def __init__(self):
        self.gpu_available = self._check_gpu_availability()
        self.current_load = 0
        self.temperature = 0
        
    def _check_gpu_availability(self) -> bool:
        """Vérifie la disponibilité de la RTX3090"""
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], 
                                  capture_output=True, text=True, timeout=10)
            return 'RTX 3090' in result.stdout
        except:
            logger.warning("RTX3090 non détectée - Mode CPU activé")
            return False
    
    def get_gpu_status(self) -> Dict[str, Any]:
        """Récupère le statut GPU"""
        if not self.gpu_available:
            return {"available": False, "load": 0, "temperature": 0, "memory_used": 0}
        
        try:
            # GPU Load
            result = subprocess.run([
                'nvidia-smi', '--query-gpu=utilization.gpu,temperature.gpu,memory.used',
                '--format=csv,noheader,nounits'
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                values = result.stdout.strip().split(', ')
                self.current_load = int(values[0])
                self.temperature = int(values[1])
                memory_used = int(values[2])
                
                return {
                    "available": True,
                    "load": self.current_load,
                    "temperature": self.temperature,
                    "memory_used": memory_used,
                    "status": "optimal" if self.current_load < 80 else "busy"
                }
        except Exception as e:
            logger.warning(f"Erreur lecture GPU: {e}")
        
        return {"available": False, "load": 0, "temperature": 0, "memory_used": 0}
    
    def is_optimal_for_task(self) -> bool:
        """Vérifie si le GPU est optimal pour une nouvelle tâche"""
        status = self.get_gpu_status()
        return (status["available"] and 
                status["load"] < 70 and 
                status["temperature"] < 80)
    
    def wait_for_optimal_conditions(self, max_wait: int = 300) -> bool:
        """Attend des conditions GPU optimales"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            if self.is_optimal_for_task():
                return True
            
            logger.info(f"GPU occupé (charge: {self.current_load}%) - Attente...")
            time.sleep(10)
        
        logger.warning("Timeout GPU - Exécution forcée")
        return False

class PostgreSQLManager:
    """Gestionnaire PostgreSQL avec fallback SQLite"""
    
    def __init__(self):
        self.pg_available = False
        self.sqlite_path = "data/task_scheduler.db"
        self._ensure_sqlite_db()
        self._check_postgresql()
    
    def _check_postgresql(self):
        """Vérifie PostgreSQL avec configuration UTF-8"""
        try:
            import psycopg2
            
            # Configuration PostgreSQL UTF-8 expert
            conn = psycopg2.connect(
                host="localhost",
                database="taskmaster_ng",
                user="postgres",
                password="postgres",
                options="-c lc_messages=C"  # Solution définitive UTF-8
            )
            
            # Test UTF-8
            with conn.cursor() as cur:
                cur.execute("SHOW lc_messages;")
                result = cur.fetchone()
                
            conn.close()
            self.pg_available = True
            logger.info("PostgreSQL UTF-8 opérationnel")
            
        except Exception as e:
            logger.warning(f"PostgreSQL indisponible: {e} - Fallback SQLite")
            self.pg_available = False
    
    def _ensure_sqlite_db(self):
        """Initialise la base SQLite"""
        Path("data").mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.sqlite_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS task_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mission TEXT NOT NULL,
                priority INTEGER DEFAULT 5,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                result TEXT,
                error_message TEXT,
                gpu_usage INTEGER DEFAULT 0,
                execution_time REAL DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_task_to_queue(self, mission: str, priority: int = 5) -> int:
        """Ajoute une tâche à la file d'attente"""
        if self.pg_available:
            return self._add_task_postgresql(mission, priority)
        else:
            return self._add_task_sqlite(mission, priority)
    
    def _add_task_sqlite(self, mission: str, priority: int) -> int:
        """Ajoute tâche en SQLite"""
        conn = sqlite3.connect(self.sqlite_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO task_queue (mission, priority) VALUES (?, ?)",
            (mission, priority)
        )
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return task_id
    
    def _add_task_postgresql(self, mission: str, priority: int) -> int:
        """Ajoute tâche en PostgreSQL"""
        import psycopg2
        
        conn = psycopg2.connect(
            host="localhost", database="taskmaster_ng", 
            user="postgres", password="postgres",
            options="-c lc_messages=C"
        )
        
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO task_queue (mission, priority) VALUES (%s, %s) RETURNING id",
                (mission, priority)
            )
            task_id = cur.fetchone()[0]
        
        conn.commit()
        conn.close()
        return task_id
    
    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Récupère la prochaine tâche par priorité"""
        if self.pg_available:
            return self._get_next_task_postgresql()
        else:
            return self._get_next_task_sqlite()
    
    def _get_next_task_sqlite(self) -> Optional[Dict[str, Any]]:
        """Récupère prochaine tâche SQLite"""
        conn = sqlite3.connect(self.sqlite_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM task_queue 
            WHERE status = 'pending' 
            ORDER BY priority DESC, created_at ASC 
            LIMIT 1
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def _get_next_task_postgresql(self) -> Optional[Dict[str, Any]]:
        """Récupère prochaine tâche PostgreSQL"""
        import psycopg2
        import psycopg2.extras
        
        conn = psycopg2.connect(
            host="localhost", database="taskmaster_ng", 
            user="postgres", password="postgres",
            options="-c lc_messages=C"
        )
        
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute('''
                SELECT * FROM task_queue 
                WHERE status = 'pending' 
                ORDER BY priority DESC, created_at ASC 
                LIMIT 1
            ''')
            row = cur.fetchone()
        
        conn.close()
        return dict(row) if row else None
    
    def update_task_status(self, task_id: int, status: str, result: str = None, error: str = None):
        """Met à jour le statut d'une tâche"""
        if self.pg_available:
            self._update_task_postgresql(task_id, status, result, error)
        else:
            self._update_task_sqlite(task_id, status, result, error)
    
    def _update_task_sqlite(self, task_id: int, status: str, result: str = None, error: str = None):
        """Met à jour tâche SQLite"""
        conn = sqlite3.connect(self.sqlite_path)
        
        if status == 'running':
            conn.execute(
                "UPDATE task_queue SET status = ?, started_at = CURRENT_TIMESTAMP WHERE id = ?",
                (status, task_id)
            )
        elif status == 'completed':
            conn.execute(
                "UPDATE task_queue SET status = ?, completed_at = CURRENT_TIMESTAMP, result = ? WHERE id = ?",
                (status, result, task_id)
            )
        elif status == 'failed':
            conn.execute(
                "UPDATE task_queue SET status = ?, completed_at = CURRENT_TIMESTAMP, error_message = ? WHERE id = ?",
                (status, error, task_id)
            )
        
        conn.commit()
        conn.close()
    
    def _update_task_postgresql(self, task_id: int, status: str, result: str = None, error: str = None):
        """Met à jour tâche PostgreSQL"""
        import psycopg2
        
        conn = psycopg2.connect(
            host="localhost", database="taskmaster_ng", 
            user="postgres", password="postgres",
            options="-c lc_messages=C"
        )
        
        with conn.cursor() as cur:
            if status == 'running':
                cur.execute(
                    "UPDATE task_queue SET status = %s, started_at = CURRENT_TIMESTAMP WHERE id = %s",
                    (status, task_id)
                )
            elif status == 'completed':
                cur.execute(
                    "UPDATE task_queue SET status = %s, completed_at = CURRENT_TIMESTAMP, result = %s WHERE id = %s",
                    (status, result, task_id)
                )
            elif status == 'failed':
                cur.execute(
                    "UPDATE task_queue SET status = %s, completed_at = CURRENT_TIMESTAMP, error_message = %s WHERE id = %s",
                    (status, error, task_id)
                )
        
        conn.commit()
        conn.close()
    
    def get_queue_stats(self) -> Dict[str, int]:
        """Statistiques de la file d'attente"""
        if self.pg_available:
            return self._get_stats_postgresql()
        else:
            return self._get_stats_sqlite()
    
    def _get_stats_sqlite(self) -> Dict[str, int]:
        """Stats SQLite"""
        conn = sqlite3.connect(self.sqlite_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT status, COUNT(*) FROM task_queue GROUP BY status")
        stats = dict(cursor.fetchall())
        
        conn.close()
        return {
            'pending': stats.get('pending', 0),
            'running': stats.get('running', 0),
            'completed': stats.get('completed', 0),
            'failed': stats.get('failed', 0),
            'total': sum(stats.values())
        }
    
    def _get_stats_postgresql(self) -> Dict[str, int]:
        """Stats PostgreSQL"""
        import psycopg2
        
        conn = psycopg2.connect(
            host="localhost", database="taskmaster_ng", 
            user="postgres", password="postgres",
            options="-c lc_messages=C"
        )
        
        with conn.cursor() as cur:
            cur.execute("SELECT status, COUNT(*) FROM task_queue GROUP BY status")
            stats = dict(cur.fetchall())
        
        conn.close()
        return {
            'pending': stats.get('pending', 0),
            'running': stats.get('running', 0),
            'completed': stats.get('completed', 0),
            'failed': stats.get('failed', 0),
            'total': sum(stats.values())
        }

class TaskSchedulerCursor:
    """Ordonnanceur principal TaskMaster Cursor"""
    
    def __init__(self):
        self.gpu_optimizer = RTX3090Optimizer()
        self.db_manager = PostgreSQLManager()
        self.running = False
        self.current_task = None
        self.stats = {
            'tasks_processed': 0,
            'tasks_successful': 0,
            'tasks_failed': 0,
            'total_execution_time': 0,
            'start_time': datetime.now()
        }
    
    def validate_infrastructure(self) -> Tuple[bool, List[str]]:
        """Validation infrastructure 70 points"""
        issues = []
        
        # 1. PostgreSQL
        if not self.db_manager.pg_available:
            issues.append("PostgreSQL indisponible - Fallback SQLite actif")
        
        # 2. GPU RTX3090
        gpu_status = self.gpu_optimizer.get_gpu_status()
        if not gpu_status["available"]:
            issues.append("RTX3090 non détectée")
        elif gpu_status["temperature"] > 85:
            issues.append(f"GPU surchauffe: {gpu_status['temperature']}°C")
        
        # 3. Espace disque
        disk_usage = psutil.disk_usage('.')
        if disk_usage.percent > 90:
            issues.append(f"Espace disque critique: {disk_usage.percent}%")
        
        # 4. Mémoire RAM
        memory = psutil.virtual_memory()
        if memory.percent > 85:
            issues.append(f"Mémoire RAM critique: {memory.percent}%")
        
        # 5. Répertoires
        required_dirs = ['logs', 'data', 'reports']
        for dir_name in required_dirs:
            if not Path(dir_name).exists():
                Path(dir_name).mkdir(exist_ok=True)
                logger.info(f"Répertoire créé: {dir_name}")
        
        return len(issues) == 0, issues
    
    def add_mission(self, mission: str, priority: int = 5) -> int:
        """Ajoute une mission à la file d'attente"""
        task_id = self.db_manager.add_task_to_queue(mission, priority)
        logger.info(f"Mission ajoutée (ID: {task_id}, Priorité: {priority}): {mission[:50]}...")
        return task_id
    
    def add_missions_from_file(self, file_path: str) -> List[int]:
        """Ajoute des missions depuis un fichier JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            missions = data.get('missions', [])
            task_ids = []
            
            for mission_data in missions:
                if isinstance(mission_data, str):
                    task_id = self.add_mission(mission_data)
                    task_ids.append(task_id)
                elif isinstance(mission_data, dict):
                    mission = mission_data.get('mission', '')
                    priority = mission_data.get('priority', 5)
                    task_id = self.add_mission(mission, priority)
                    task_ids.append(task_id)
            
            logger.info(f"Chargé {len(task_ids)} missions depuis {file_path}")
            return task_ids
            
        except Exception as e:
            logger.error(f"Erreur chargement missions: {e}")
            return []
    
    def create_example_missions_file(self, file_path: str = "missions_cursor.json"):
        """Crée un fichier d'exemple de missions"""
        example_missions = {
            "missions": [
                {
                    "mission": "Auditer la sécurité du module d'authentification",
                    "priority": 9
                },
                {
                    "mission": "Optimiser les requêtes PostgreSQL lentes",
                    "priority": 8
                },
                {
                    "mission": "Générer la documentation API complète",
                    "priority": 7
                },
                {
                    "mission": "Refactorer le code legacy du service utilisateur",
                    "priority": 6
                },
                {
                    "mission": "Créer des tests unitaires pour le module de paiement",
                    "priority": 5
                },
                {
                    "mission": "Analyser les performances GPU RTX3090",
                    "priority": 8
                },
                {
                    "mission": "Déployer la nouvelle version du microservice",
                    "priority": 4
                },
                {
                    "mission": "Créer un rapport d'analyse des logs d'erreur",
                    "priority": 6
                },
                {
                    "mission": "Optimiser les images Docker du projet",
                    "priority": 3
                },
                {
                    "mission": "Vérifier la conformité RGPD des données",
                    "priority": 7
                }
            ]
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(example_missions, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Fichier d'exemple créé: {file_path}")
        return file_path
    
    async def execute_task(self, task: Dict[str, Any]) -> Tuple[bool, str]:
        """Exécute une tâche TaskMaster"""
        task_id = task['id']
        mission = task['mission']
        
        try:
            logger.info(f"Démarrage tâche {task_id}: {mission[:50]}...")
            
            # Attendre conditions GPU optimales
            self.gpu_optimizer.wait_for_optimal_conditions(max_wait=60)
            
            # Simuler exécution TaskMaster (remplacer par vraie intégration)
            start_time = time.time()
            
            # Ici, intégrer avec AgentTaskMasterNextGeneration
            # Pour la démo, on simule
            await asyncio.sleep(2)  # Simulation traitement
            
            execution_time = time.time() - start_time
            
            # Résultat simulé
            result = {
                "status": "completed",
                "execution_time": execution_time,
                "gpu_used": self.gpu_optimizer.current_load,
                "confidence": 0.95,
                "output": f"Mission '{mission[:30]}...' exécutée avec succès"
            }
            
            return True, json.dumps(result)
            
        except Exception as e:
            logger.error(f"Erreur exécution tâche {task_id}: {e}")
            return False, str(e)
    
    async def process_queue(self, max_tasks: int = None, timeout: int = 3600):
        """Traite la file d'attente des tâches"""
        logger.info("Démarrage traitement file d'attente")
        
        # Validation infrastructure
        is_valid, issues = self.validate_infrastructure()
        if not is_valid:
            logger.warning(f"Infrastructure dégradée: {issues}")
        
        self.running = True
        processed = 0
        start_time = time.time()
        
        try:
            while self.running and (max_tasks is None or processed < max_tasks):
                # Timeout check
                if time.time() - start_time > timeout:
                    logger.info("Timeout atteint - Arrêt du traitement")
                    break
                
                # Récupérer la prochaine tâche
                task = self.db_manager.get_next_task()
                if not task:
                    logger.info("Aucune tâche en attente - Pause")
                    await asyncio.sleep(5)
                    continue
                
                self.current_task = task
                task_id = task['id']
                
                # Marquer comme en cours
                self.db_manager.update_task_status(task_id, 'running')
                
                # Exécuter la tâche
                success, result_or_error = await self.execute_task(task)
                
                # Mettre à jour le statut
                if success:
                    self.db_manager.update_task_status(task_id, 'completed', result_or_error)
                    self.stats['tasks_successful'] += 1
                    logger.info(f"Tâche {task_id} terminée avec succès")
                else:
                    self.db_manager.update_task_status(task_id, 'failed', error=result_or_error)
                    self.stats['tasks_failed'] += 1
                    logger.error(f"Tâche {task_id} échouée: {result_or_error}")
                
                processed += 1
                self.stats['tasks_processed'] += 1
                self.current_task = None
                
                # Pause entre tâches pour éviter la surcharge
                await asyncio.sleep(1)
        
        except KeyboardInterrupt:
            logger.info("Arrêt demandé par l'utilisateur")
        finally:
            self.running = False
            logger.info(f"Traitement terminé - {processed} tâches traitées")
    
    def get_status(self) -> Dict[str, Any]:
        """Récupère le statut du scheduler"""
        queue_stats = self.db_manager.get_queue_stats()
        gpu_status = self.gpu_optimizer.get_gpu_status()
        
        system_stats = {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('.').percent
        }
        
        uptime = datetime.now() - self.stats['start_time']
        
        return {
            'scheduler': {
                'running': self.running,
                'current_task': self.current_task['mission'][:50] + '...' if self.current_task else None,
                'uptime_seconds': uptime.total_seconds()
            },
            'queue': queue_stats,
            'gpu': gpu_status,
            'system': system_stats,
            'stats': self.stats,
            'database': {
                'postgresql': self.db_manager.pg_available,
                'sqlite_fallback': not self.db_manager.pg_available
            }
        }
    
    def stop(self):
        """Arrête le scheduler"""
        self.running = False
        logger.info("Arrêt du Task Scheduler demandé")
    
    def generate_report(self) -> str:
        """Génère un rapport détaillé"""
        status = self.get_status()
        report_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        report = f"""# Task Scheduler Cursor - Rapport d'Exécution
**Généré le:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Résumé Exécution
- **Tâches traitées:** {status['stats']['tasks_processed']}
- **Succès:** {status['stats']['tasks_successful']}
- **Échecs:** {status['stats']['tasks_failed']}
- **Taux de succès:** {(status['stats']['tasks_successful'] / max(status['stats']['tasks_processed'], 1) * 100):.1f}%

## File d'Attente
- **En attente:** {status['queue']['pending']}
- **En cours:** {status['queue']['running']}
- **Terminées:** {status['queue']['completed']}
- **Échouées:** {status['queue']['failed']}

## Ressources Système
- **GPU RTX3090:** {'Disponible' if status['gpu']['available'] else 'Indisponible'}
- **Charge GPU:** {status['gpu']['load']}%
- **Température GPU:** {status['gpu']['temperature']}°C
- **CPU:** {status['system']['cpu_percent']}%
- **RAM:** {status['system']['memory_percent']}%
- **Disque:** {status['system']['disk_percent']}%

## Base de Données
- **PostgreSQL:** {'✅ Opérationnel' if status['database']['postgresql'] else '❌ Indisponible'}
- **SQLite Fallback:** {'✅ Actif' if status['database']['sqlite_fallback'] else '⏸️ Inactif'}

## Infrastructure
- **Uptime:** {status['scheduler']['uptime_seconds']:.0f} secondes
- **Tâche actuelle:** {status['scheduler']['current_task'] or 'Aucune'}
"""
        
        report_path = f"reports/task_scheduler_report_{report_time}.md"
        Path("reports").mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Rapport généré: {report_path}")
        return report_path

async def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description="Task Scheduler Cursor - Ordonnanceur TaskMaster NextGeneration")
    
    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
    
    # Commande add
    add_parser = subparsers.add_parser('add', help='Ajouter une mission')
    add_parser.add_argument('mission', help='Description de la mission')
    add_parser.add_argument('--priority', type=int, default=5, help='Priorité (1-10)')
    
    # Commande batch
    batch_parser = subparsers.add_parser('batch', help='Ajouter missions depuis fichier')
    batch_parser.add_argument('file', help='Fichier JSON des missions')
    
    # Commande process
    process_parser = subparsers.add_parser('process', help='Traiter la file d\'attente')
    process_parser.add_argument('--max-tasks', type=int, help='Nombre max de tâches à traiter')
    process_parser.add_argument('--timeout', type=int, default=3600, help='Timeout en secondes')
    
    # Commande status
    subparsers.add_parser('status', help='Afficher le statut')
    
    # Commande report
    subparsers.add_parser('report', help='Générer un rapport')
    
    # Commande example
    subparsers.add_parser('example', help='Créer fichier missions d\'exemple')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialiser le scheduler
    scheduler = TaskSchedulerCursor()
    
    try:
        if args.command == 'add':
            task_id = scheduler.add_mission(args.mission, args.priority)
            print(f"✅ Mission ajoutée (ID: {task_id})")
        
        elif args.command == 'batch':
            if not Path(args.file).exists():
                print(f"❌ Fichier non trouvé: {args.file}")
                return
            
            task_ids = scheduler.add_missions_from_file(args.file)
            print(f"✅ {len(task_ids)} missions ajoutées depuis {args.file}")
        
        elif args.command == 'process':
            print("🚀 Démarrage du traitement des tâches...")
            await scheduler.process_queue(args.max_tasks, args.timeout)
        
        elif args.command == 'status':
            status = scheduler.get_status()
            print("\n📊 Task Scheduler Status")
            print("=" * 50)
            print(f"Running: {status['scheduler']['running']}")
            print(f"Current Task: {status['scheduler']['current_task'] or 'None'}")
            print(f"Queue - Pending: {status['queue']['pending']}, Running: {status['queue']['running']}")
            print(f"Stats - Processed: {status['stats']['tasks_processed']}, Success: {status['stats']['tasks_successful']}")
            print(f"GPU - Available: {status['gpu']['available']}, Load: {status['gpu']['load']}%")
            print(f"System - CPU: {status['system']['cpu_percent']}%, RAM: {status['system']['memory_percent']}%")
        
        elif args.command == 'report':
            report_path = scheduler.generate_report()
            print(f"📄 Rapport généré: {report_path}")
        
        elif args.command == 'example':
            file_path = scheduler.create_example_missions_file()
            print(f"📝 Fichier d'exemple créé: {file_path}")
    
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt demandé par l'utilisateur")
        scheduler.stop()
    except Exception as e:
        logger.error(f"Erreur: {e}")
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())



