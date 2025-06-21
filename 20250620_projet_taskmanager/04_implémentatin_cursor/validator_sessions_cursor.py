#!/usr/bin/env python3
"""
🎯 Validator Sessions TaskMaster Cursor - Validation Sessions Actives NextGeneration
Répertoire: 20250620_projet_taskmanager/04_implémentatin_cursor/

Fonctionnalités:
- Validation sessions PostgreSQL actives
- Détection tâches orphelines TaskMaster
- Nettoyage automatique sessions expirées
- Monitoring santé environnement Cursor
- Rapports validation détaillés
"""

import os
import sys
import json
import logging
import asyncio
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import requests
import psutil
import subprocess
from dataclasses import dataclass
from enum import Enum

# Importation modules internes
from cli_taskmaster_cursor import TaskMasterCLI

from sqlalchemy import create_engine, text
import sqlite3


class SessionStatus(Enum):
    ACTIVE = "active"
    IDLE = "idle"
    WAITING = "waiting"
    ORPHANED = "orphaned"
    EXPIRED = "expired"

@dataclass
class SessionInfo:
    session_id: str
    status: SessionStatus
    start_time: datetime
    last_activity: datetime
    task_id: Optional[str] = None
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    details: str = ""

@dataclass
class ValidationResult:
    timestamp: datetime
    total_sessions: int
    active_sessions: int
    orphaned_sessions: int
    expired_sessions: int
    recommendations: List[str]
    sessions: List[SessionInfo]
    infrastructure_health: Dict[str, Any]


class SessionValidator:
    """Validateur de sessions TaskMaster NextGeneration"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.cli = TaskMasterCLI(config_path)
        self.logger = self._setup_logging()
        
        # Configuration validation
        self.validation_config = {
            "max_idle_time": 3600,  # 1 heure
            "max_orphaned_time": 1800,  # 30 minutes
            "max_sessions": 100,
            "cleanup_enabled": True,
            "alert_thresholds": {
                "cpu_warning": 80.0,
                "memory_warning": 85.0,
                "sessions_warning": 75
            }
        }
        
    def _setup_logging(self) -> logging.Logger:
        """Configure le logging validator"""
        logger = logging.getLogger('SessionValidator')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Handler console
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - 🔍 VALIDATOR - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # Handler fichier
            os.makedirs("logs", exist_ok=True)
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_handler = logging.FileHandler(
                f"logs/validator_sessions_{session_id}.log", 
                encoding='utf-8'
            )
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        return logger

    async def validate_postgresql_sessions(self) -> Tuple[List[SessionInfo], Dict[str, Any]]:
        """Valide les sessions PostgreSQL actives"""
        sessions = []
        stats = {
            "total_connections": 0,
            "active_connections": 0,
            "idle_connections": 0,
            "max_connections": 0,
            "database_size_mb": 0
        }
        
        try:
            config = self.cli.config['postgresql']
            dsn = f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            engine = create_engine(dsn, client_encoding='utf8')
            
            with engine.connect() as conn:
                # Vérification lc_messages
                result = conn.execute(text("SHOW lc_messages"))
                lc_messages = result.scalar()
                
                if lc_messages != 'C':
                    self.logger.warning(f"⚠️ lc_messages = '{lc_messages}', recommandé: 'C'")
                
                # Statistiques générales
                result = conn.execute(text("SHOW max_connections"))
                stats["max_connections"] = int(result.scalar())
                
                # Sessions actives
                query_sessions = text("""
                    SELECT 
                        pid,
                        state,
                        application_name,
                        backend_start,
                        state_change,
                        query_start,
                        query,
                        client_addr
                    FROM pg_stat_activity 
                    WHERE datname = :dbname
                    AND pid != pg_backend_pid()
                    ORDER BY backend_start DESC
                """)
                
                result = conn.execute(query_sessions, {'dbname': config['database']})
                
                for row in result:
                    pid = row[0]
                    state = row[1] or 'unknown'
                    app_name = row[2] or 'unknown'
                    backend_start = row[3]
                    state_change = row[4]
                    query_start = row[5]
                    query = (row[6] or '')[:100]
                    client_addr = row[7] or 'localhost'
                    
                    # Détermination du statut
                    if state == 'active':
                        session_status = SessionStatus.ACTIVE
                        stats["active_connections"] += 1
                    elif state == 'idle':
                        session_status = SessionStatus.IDLE
                        stats["idle_connections"] += 1
                    elif state in ['idle in transaction', 'idle in transaction (aborted)']:
                        session_status = SessionStatus.WAITING
                    else:
                        session_status = SessionStatus.ACTIVE
                    
                    # Vérification sessions orphelines
                    if state_change and datetime.now() - state_change > timedelta(seconds=self.validation_config["max_orphaned_time"]):
                        session_status = SessionStatus.ORPHANED
                    
                    session = SessionInfo(
                        session_id=f"pg_{pid}",
                        status=session_status,
                        start_time=backend_start,
                        last_activity=state_change or backend_start,
                        details=f"App: {app_name}, Query: {query[:50]}{'...' if len(query) > 50 else ''}"
                    )
                    
                    sessions.append(session)
                
                stats["total_connections"] = len(sessions)
                
                # Taille de la base
                size_query = text("""
                    SELECT pg_size_pretty(pg_database_size(:dbname)) as size,
                           pg_database_size(:dbname) / 1024 / 1024 as size_mb
                """)
                result = conn.execute(size_query, {'dbname': config['database']})
                size_row = result.fetchone()
                if size_row:
                    stats["database_size_mb"] = float(size_row[1])
                
                self.logger.info(f"✅ PostgreSQL: {stats['total_connections']} sessions, {stats['active_connections']} actives")
                
        except Exception as e:
            self.logger.error(f"❌ Erreur validation PostgreSQL: {str(e)}")
            stats["error"] = str(e)
        
        return sessions, stats

    async def validate_taskmaster_tasks(self) -> List[SessionInfo]:
        """Valide les tâches TaskMaster en cours"""
        tasks = []
        
        try:
            # Récupération des tâches récentes
            recent_tasks = await self.cli.list_tasks(50)
            
            for task in recent_tasks:
                task_id = task.get('task_id', 'unknown')
                created_at = task.get('created_at', datetime.now().isoformat())
                
                # Conversion datetime
                try:
                    if isinstance(created_at, str):
                        start_time = datetime.fromisoformat(created_at.replace('T', ' ').replace('Z', ''))
                    else:
                        start_time = created_at
                except:
                    start_time = datetime.now()
                
                # Détermination du statut
                age = datetime.now() - start_time
                
                if age > timedelta(seconds=self.validation_config["max_idle_time"]):
                    status = SessionStatus.EXPIRED
                elif age > timedelta(seconds=self.validation_config["max_orphaned_time"]):
                    status = SessionStatus.ORPHANED
                else:
                    status = SessionStatus.ACTIVE
                
                task_session = SessionInfo(
                    session_id=task_id,
                    status=status,
                    start_time=start_time,
                    last_activity=start_time,
                    task_id=task_id,
                    details=f"Mission: {task.get('mission', 'N/A')[:50]}"
                )
                
                tasks.append(task_session)
            
            self.logger.info(f"✅ Tâches TaskMaster: {len(tasks)} trouvées")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur validation tâches: {str(e)}")
        
        return tasks

    async def validate_system_processes(self) -> List[SessionInfo]:
        """Valide les processus système liés à TaskMaster"""
        processes = []
        
        try:
            # Recherche processus liés
            target_processes = ['postgres', 'ollama', 'python', 'lmstudio']
            
            for proc in psutil.process_iter(['pid', 'name', 'create_time', 'cpu_percent', 'memory_percent', 'cmdline']):
                try:
                    name = proc.info['name'].lower()
                    
                    # Filtrage processus pertinents
                    is_relevant = any(target in name for target in target_processes)
                    
                    if is_relevant:
                        # Vérification ligne de commande pour TaskMaster
                        cmdline = ' '.join(proc.info.get('cmdline', []))
                        if 'taskmaster' in cmdline.lower() or 'nextgeneration' in cmdline.lower():
                            
                            create_time = datetime.fromtimestamp(proc.info['create_time'])
                            cpu_usage = proc.info.get('cpu_percent', 0.0)
                            memory_usage = proc.info.get('memory_percent', 0.0)
                            
                            # Détermination statut
                            if cpu_usage > 0.1:
                                status = SessionStatus.ACTIVE
                            elif datetime.now() - create_time > timedelta(hours=1):
                                status = SessionStatus.IDLE
                            else:
                                status = SessionStatus.ACTIVE
                            
                            process_session = SessionInfo(
                                session_id=f"proc_{proc.info['pid']}",
                                status=status,
                                start_time=create_time,
                                last_activity=datetime.now(),
                                cpu_usage=cpu_usage,
                                memory_usage=memory_usage,
                                details=f"Process: {name}, CPU: {cpu_usage:.1f}%"
                            )
                            
                            processes.append(process_session)
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.logger.info(f"✅ Processus système: {len(processes)} trouvés")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur validation processus: {str(e)}")
        
        return processes

    async def validate_infrastructure_health(self) -> Dict[str, Any]:
        """Valide la santé générale de l'infrastructure"""
        health = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "components": {},
            "alerts": [],
            "recommendations": []
        }
        
        try:
            # Test PostgreSQL UTF-8
            try:
                config = self.cli.config['postgresql']
                dsn = f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
                engine = create_engine(dsn, client_encoding='utf8')
                
                with engine.connect() as conn:
                    result = conn.execute(text("SHOW lc_messages"))
                    lc_messages = result.scalar()
                    
                    conn.execute(text("SELECT 'Test français éàùç'"))
                    
                    health["components"]["postgresql"] = {
                        "status": "healthy",
                        "lc_messages": lc_messages,
                        "utf8_support": True
                    }
                    
                    if lc_messages != 'C':
                        health["alerts"].append("PostgreSQL lc_messages n'est pas configuré à 'C'")
                        health["recommendations"].append("Exécuter fix_postgresql_utf8_cursor.py")
                        
            except Exception as e:
                health["components"]["postgresql"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                health["overall_status"] = "degraded"
                health["alerts"].append("PostgreSQL non accessible")
            
            # Test Memory API
            try:
                memory_config = self.cli.config['memory_api']
                memory_url = f"http://{memory_config['host']}:{memory_config['port']}"
                response = requests.get(f"{memory_url}/health", timeout=3)
                
                health["components"]["memory_api"] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "response_code": response.status_code
                }
                
            except Exception as e:
                health["components"]["memory_api"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                health["alerts"].append("Memory API non accessible")
            
            # Métriques système
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            health["system_metrics"] = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "disk_percent": psutil.disk_usage('C:\\').percent
            }
            
            # Alertes seuils
            if cpu_percent > self.validation_config["alert_thresholds"]["cpu_warning"]:
                health["alerts"].append(f"CPU élevé: {cpu_percent:.1f}%")
                health["overall_status"] = "warning"
            
            if memory_percent > self.validation_config["alert_thresholds"]["memory_warning"]:
                health["alerts"].append(f"Mémoire élevée: {memory_percent:.1f}%")
                health["overall_status"] = "warning"
            
        except Exception as e:
            self.logger.error(f"❌ Erreur validation infrastructure: {str(e)}")
            health["overall_status"] = "error"
            health["error"] = str(e)
        
        return health

    async def cleanup_orphaned_sessions(self, sessions: List[SessionInfo]) -> Dict[str, Any]:
        """Nettoie les sessions orphelines"""
        cleanup_result = {
            "cleaned_sessions": 0,
            "failed_cleanups": 0,
            "details": []
        }
        
        if not self.validation_config["cleanup_enabled"]:
            self.logger.info("🔒 Cleanup désactivé dans la configuration")
            return cleanup_result
        
        orphaned_sessions = [s for s in sessions if s.status == SessionStatus.ORPHANED]
        
        for session in orphaned_sessions:
            try:
                if session.session_id.startswith('pg_'):
                    # Session PostgreSQL
                    pid = session.session_id.replace('pg_', '')
                    
                    config = self.cli.config['postgresql']
                    dsn = f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
                    engine = create_engine(dsn, client_encoding='utf8')
                    
                    with engine.connect() as conn:
                        conn.execute(text("SELECT pg_terminate_backend(:pid)"), {'pid': int(pid)})
                    
                    cleanup_result["cleaned_sessions"] += 1
                    cleanup_result["details"].append(f"Terminé session PostgreSQL PID {pid}")
                    self.logger.info(f"🧹 Session PostgreSQL {pid} terminée")
                
                elif session.session_id.startswith('proc_'):
                    # Processus système
                    pid = int(session.session_id.replace('proc_', ''))
                    
                    try:
                        proc = psutil.Process(pid)
                        proc.terminate()
                        
                        cleanup_result["cleaned_sessions"] += 1
                        cleanup_result["details"].append(f"Processus {pid} terminé")
                        self.logger.info(f"🧹 Processus {pid} terminé")
                        
                    except psutil.NoSuchProcess:
                        self.logger.info(f"Processus {pid} déjà terminé")
                
            except Exception as e:
                cleanup_result["failed_cleanups"] += 1
                cleanup_result["details"].append(f"Échec cleanup {session.session_id}: {str(e)}")
                self.logger.error(f"❌ Échec cleanup {session.session_id}: {str(e)}")
        
        return cleanup_result

    async def run_full_validation(self, cleanup: bool = True) -> ValidationResult:
        """Exécute une validation complète des sessions"""
        self.logger.info("🔍 Démarrage validation complète des sessions")
        
        # Collecte des données
        pg_sessions, pg_stats = await self.validate_postgresql_sessions()
        taskmaster_tasks = await self.validate_taskmaster_tasks()
        system_processes = await self.validate_system_processes()
        infrastructure_health = await self.validate_infrastructure_health()
        
        # Consolidation des sessions
        all_sessions = pg_sessions + taskmaster_tasks + system_processes
        
        # Statistiques
        total_sessions = len(all_sessions)
        active_sessions = len([s for s in all_sessions if s.status == SessionStatus.ACTIVE])
        orphaned_sessions = len([s for s in all_sessions if s.status == SessionStatus.ORPHANED])
        expired_sessions = len([s for s in all_sessions if s.status == SessionStatus.EXPIRED])
        
        # Recommandations
        recommendations = []
        
        if orphaned_sessions > 0:
            recommendations.append(f"Nettoyer {orphaned_sessions} sessions orphelines")
        
        if expired_sessions > 0:
            recommendations.append(f"Vérifier {expired_sessions} sessions expirées")
        
        if total_sessions > self.validation_config["alert_thresholds"]["sessions_warning"]:
            recommendations.append("Nombre élevé de sessions actives")
        
        # Cleanup si demandé
        cleanup_result = None
        if cleanup and (orphaned_sessions > 0 or expired_sessions > 0):
            cleanup_result = await self.cleanup_orphaned_sessions(all_sessions)
            if cleanup_result["cleaned_sessions"] > 0:
                recommendations.append(f"Cleanup effectué: {cleanup_result['cleaned_sessions']} sessions nettoyées")
        
        result = ValidationResult(
            timestamp=datetime.now(),
            total_sessions=total_sessions,
            active_sessions=active_sessions,
            orphaned_sessions=orphaned_sessions,
            expired_sessions=expired_sessions,
            recommendations=recommendations,
            sessions=all_sessions,
            infrastructure_health=infrastructure_health
        )
        
        self.logger.info(f"✅ Validation terminée: {total_sessions} sessions, {active_sessions} actives, {orphaned_sessions} orphelines")
        
        return result

    def print_validation_report(self, result: ValidationResult) -> None:
        """Affiche le rapport de validation"""
        print("\n" + "="*80)
        print("🔍 RAPPORT VALIDATION SESSIONS TASKMASTER")
        print("="*80)
        
        # Résumé
        print(f"📊 Sessions totales: {result.total_sessions}")
        print(f"✅ Sessions actives: {result.active_sessions}")
        print(f"⚠️ Sessions orphelines: {result.orphaned_sessions}")
        print(f"⏰ Sessions expirées: {result.expired_sessions}")
        print(f"🏥 Santé infrastructure: {result.infrastructure_health.get('overall_status', 'unknown')}")
        
        # Alertes
        alerts = result.infrastructure_health.get('alerts', [])
        if alerts:
            print(f"\n🚨 ALERTES ({len(alerts)}):")
            for alert in alerts:
                print(f"   ⚠️ {alert}")
        
        # Recommandations
        if result.recommendations:
            print(f"\n💡 RECOMMANDATIONS ({len(result.recommendations)}):")
            for rec in result.recommendations:
                print(f"   💡 {rec}")
        
        # Détail sessions problématiques
        problematic = [s for s in result.sessions if s.status in [SessionStatus.ORPHANED, SessionStatus.EXPIRED]]
        if problematic:
            print(f"\n⚠️ SESSIONS PROBLÉMATIQUES ({len(problematic)}):")
            for session in problematic[:10]:  # Limite à 10
                status_emoji = "🔄" if session.status == SessionStatus.ORPHANED else "⏰"
                print(f"   {status_emoji} {session.session_id} | {session.status.value} | {session.details[:50]}")
        
        print("="*80)

    def save_validation_report(self, result: ValidationResult, filename: Optional[str] = None) -> str:
        """Sauvegarde le rapport de validation"""
        if not filename:
            filename = f"rapport_validation_{result.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        
        # Sérialisation du résultat
        report_data = {
            "timestamp": result.timestamp.isoformat(),
            "summary": {
                "total_sessions": result.total_sessions,
                "active_sessions": result.active_sessions,
                "orphaned_sessions": result.orphaned_sessions,
                "expired_sessions": result.expired_sessions
            },
            "infrastructure_health": result.infrastructure_health,
            "recommendations": result.recommendations,
            "sessions": [
                {
                    "session_id": s.session_id,
                    "status": s.status.value,
                    "start_time": s.start_time.isoformat(),
                    "last_activity": s.last_activity.isoformat(),
                    "task_id": s.task_id,
                    "cpu_usage": s.cpu_usage,
                    "memory_usage": s.memory_usage,
                    "details": s.details
                }
                for s in result.sessions
            ]
        }
        
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"📄 Rapport validation sauvegardé: {filepath}")
        return filepath


def create_validator_cli() -> argparse.ArgumentParser:
    """Crée l'interface CLI pour le validator"""
    parser = argparse.ArgumentParser(
        description="🔍 Validator Sessions TaskMaster - Validation Sessions Actives NextGeneration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python validator_sessions_cursor.py validate             # Validation complète
  python validator_sessions_cursor.py validate --no-cleanup # Sans nettoyage
  python validator_sessions_cursor.py monitor             # Monitoring continu
  python validator_sessions_cursor.py cleanup             # Nettoyage seul
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
    
    # Commande validate
    validate_parser = subparsers.add_parser('validate', help='Validation complète des sessions')
    validate_parser.add_argument('--config', '-c', help='Fichier de configuration JSON')
    validate_parser.add_argument('--output', '-o', help='Fichier de sortie pour le rapport')
    validate_parser.add_argument('--no-cleanup', action='store_true', help='Pas de nettoyage automatique')
    validate_parser.add_argument('--no-report', action='store_true', help='Pas d\'affichage du rapport')
    
    # Commande monitor
    monitor_parser = subparsers.add_parser('monitor', help='Monitoring continu des sessions')
    monitor_parser.add_argument('--config', '-c', help='Fichier de configuration JSON')
    monitor_parser.add_argument('--interval', '-i', type=int, default=60, help='Intervalle monitoring (secondes)')
    monitor_parser.add_argument('--duration', '-d', type=int, help='Durée monitoring (secondes)')
    
    # Commande cleanup
    cleanup_parser = subparsers.add_parser('cleanup', help='Nettoyage sessions orphelines')
    cleanup_parser.add_argument('--config', '-c', help='Fichier de configuration JSON')
    cleanup_parser.add_argument('--force', action='store_true', help='Force le nettoyage sans confirmation')
    
    return parser


async def main():
    """Fonction principale"""
    parser = create_validator_cli()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    validator = SessionValidator(args.config)
    
    if args.command == 'validate':
        print("🔍 Validation des sessions TaskMaster...")
        
        result = await validator.run_full_validation(cleanup=not args.no_cleanup)
        
        if not args.no_report:
            validator.print_validation_report(result)
        
        if args.output:
            validator.save_validation_report(result, args.output)
        else:
            validator.save_validation_report(result)
    
    elif args.command == 'monitor':
        print(f"🔍 Monitoring sessions TaskMaster - Intervalle: {args.interval}s")
        print("👆 Ctrl+C pour arrêter\n")
        
        end_time = datetime.now() + timedelta(seconds=args.duration) if args.duration else None
        
        try:
            while True:
                if end_time and datetime.now() >= end_time:
                    break
                
                print(f"\n🔄 Validation {datetime.now().strftime('%H:%M:%S')}")
                result = await validator.run_full_validation(cleanup=True)
                
                # Affichage résumé
                print(f"📊 {result.total_sessions} sessions | ✅ {result.active_sessions} actives | ⚠️ {result.orphaned_sessions} orphelines")
                
                if result.infrastructure_health.get('alerts'):
                    print(f"🚨 {len(result.infrastructure_health['alerts'])} alertes")
                
                await asyncio.sleep(args.interval)
                
        except KeyboardInterrupt:
            print("\n👋 Monitoring arrêté")
    
    elif args.command == 'cleanup':
        print("🧹 Nettoyage des sessions orphelines...")
        
        # Validation préalable
        result = await validator.run_full_validation(cleanup=False)
        
        orphaned = [s for s in result.sessions if s.status == SessionStatus.ORPHANED]
        expired = [s for s in result.sessions if s.status == SessionStatus.EXPIRED]
        
        if not orphaned and not expired:
            print("✅ Aucune session à nettoyer")
            return
        
        print(f"⚠️ Sessions à nettoyer: {len(orphaned)} orphelines, {len(expired)} expirées")
        
        if not args.force:
            response = input("Continuer le nettoyage? (y/N): ")
            if response.lower() != 'y':
                print("❌ Nettoyage annulé")
                return
        
        cleanup_result = await validator.cleanup_orphaned_sessions(result.sessions)
        
        print(f"✅ Nettoyage terminé: {cleanup_result['cleaned_sessions']} sessions nettoyées")
        if cleanup_result['failed_cleanups'] > 0:
            print(f"❌ {cleanup_result['failed_cleanups']} échecs de nettoyage")


if __name__ == "__main__":
    asyncio.run(main()) 



