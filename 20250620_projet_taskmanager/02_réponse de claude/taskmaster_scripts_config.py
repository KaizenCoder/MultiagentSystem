#!/usr/bin/env python3
"""
Scripts utilitaires pour TaskMaster Pool
- CLI pour lancement manuel
- Dashboard console
- Validateur de sessions
- Script de spawn multiple
"""

# ========== launch_taskmaster_cli.py ==========
"""
Script CLI pour lancer une tâche TaskMaster
Usage: python launch_taskmaster_cli.py "Votre mission ici"
"""

import sys
import asyncio
import argparse
import json
from pathlib import Path

# Pour utilisation standalone
try:
    from agent_taskmaster_core import AgentTaskMasterNextGeneration
except ImportError:
    print("Error: agent_taskmaster_core not found. Make sure it's in your Python path.")
    sys.exit(1)

async def launch_single_task(mission: str, instance_id: str = None, config_file: str = None):
    """Lance une tâche unique avec un TaskMaster"""
    
    # Configuration par défaut
    config = {
        "max_concurrent_tasks": 10,
        "continuous_validation": True,
        "ai_learning_mode": True
    }
    
    # Charger config depuis fichier si fourni
    if config_file and Path(config_file).exists():
        with open(config_file, 'r') as f:
            config.update(json.load(f))
    
    # Créer l'instance
    if not instance_id:
        instance_id = f"cli_tm_{hash(mission) % 10000}"
    
    print(f"🚀 Creating TaskMaster instance: {instance_id}")
    taskmaster = AgentTaskMasterNextGeneration(
        agent_id=instance_id,
        config=config
    )
    
    try:
        # Démarrer l'instance
        print("📋 Starting TaskMaster...")
        await taskmaster.startup()
        
        # Créer la tâche
        print(f"📝 Submitting task: {mission[:50]}...")
        result = await taskmaster.create_task_from_natural_language(
            user_request=mission,
            user_id="cli_user"
        )
        
        print(f"✅ Task created: {json.dumps(result, indent=2)}")
        
        if result.get("status") == "accepted":
            task_id = result["task_id"]
            
            # Attendre et afficher le statut
            print("\n⏳ Monitoring task progress...")
            while True:
                await asyncio.sleep(5)
                status = await taskmaster.get_task_status_human_readable(task_id)
                print(f"\n📊 Status Update:\n{status}")
                
                # Vérifier si terminé
                status_data = await taskmaster.get_task_status(task_id)
                if status_data["status"] == "completed":
                    print("\n🎉 Task completed!")
                    break
        
    finally:
        # Arrêt propre
        print("\n🛑 Shutting down TaskMaster...")
        await taskmaster.shutdown()

def main_cli():
    parser = argparse.ArgumentParser(description="Launch TaskMaster task from CLI")
    parser.add_argument("mission", help="Task description in natural language")
    parser.add_argument("--instance-id", help="Custom instance ID")
    parser.add_argument("--config", help="Path to config JSON file")
    
    args = parser.parse_args()
    
    # Lancer la tâche
    asyncio.run(launch_single_task(
        mission=args.mission,
        instance_id=args.instance_id,
        config_file=args.config
    ))

# ========== dashboard_console.py ==========
"""
Dashboard console simple pour afficher l'état du pool TaskMaster
"""

import asyncio
import aiohttp
import rich
from rich.console import Console
from rich.table import Table
from rich.live import Live
from datetime import datetime

console = Console()

async def fetch_pool_status(api_url: str = "http://localhost:8000"):
    """Récupère le statut du pool depuis l'API"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{api_url}/pool/status") as resp:
                if resp.status == 200:
                    return await resp.json()
        except Exception as e:
            return {"error": str(e)}
    return None

async def fetch_instance_details(api_url: str, instance_id: str):
    """Récupère les détails d'une instance"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{api_url}/instances/{instance_id}") as resp:
                if resp.status == 200:
                    return await resp.json()
        except:
            pass
    return None

def create_dashboard_table(pool_status: dict) -> Table:
    """Crée la table du dashboard"""
    table = Table(title=f"TaskMaster Pool Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    table.add_column("Instance ID", style="cyan", no_wrap=True)
    table.add_column("Status", style="green")
    table.add_column("Active Tasks", justify="right", style="yellow")
    table.add_column("Completed", justify="right", style="blue")
    table.add_column("Errors", justify="right", style="red")
    table.add_column("Health", style="magenta")
    table.add_column("Created", style="dim")
    
    if "instances" in pool_status:
        for instance in pool_status["instances"]:
            # Couleur du statut
            status_color = {
                "running": "green",
                "busy": "yellow",
                "degraded": "orange",
                "error": "red",
                "stopped": "dim"
            }.get(instance["status"], "white")
            
            # Santé
            health_str = "OK"
            if instance.get("health", {}).get("status") == "degraded":
                health_str = "DEGRADED"
            elif instance.get("health", {}).get("status") == "unhealthy":
                health_str = "UNHEALTHY"
            
            table.add_row(
                instance["instance_id"],
                f"[{status_color}]{instance['status'].upper()}[/{status_color}]",
                str(instance["active_tasks"]),
                str(instance["completed_tasks"]),
                str(instance["error_count"]),
                health_str,
                instance["created_at"][:19]
            )
    
    # Ajouter résumé
    if "auto_scaling" in pool_status:
        as_info = pool_status["auto_scaling"]
        table.caption = (
            f"Auto-scaling: {'ON' if as_info['enabled'] else 'OFF'} | "
            f"Instances: {as_info['current_instances']}/{as_info['max_instances']} | "
            f"Load Balancer: {pool_status.get('load_balancer', {}).get('strategy', 'N/A')}"
        )
    
    return table

async def dashboard_loop(api_url: str = "http://localhost:8000", refresh_interval: int = 5):
    """Boucle principale du dashboard"""
    console.print("[bold blue]TaskMaster Pool Dashboard[/bold blue]")
    console.print(f"API: {api_url} | Refresh: {refresh_interval}s\n")
    
    with Live(console=console, refresh_per_second=1) as live:
        while True:
            try:
                # Récupérer le statut
                pool_status = await fetch_pool_status(api_url)
                
                if pool_status and "error" not in pool_status:
                    table = create_dashboard_table(pool_status)
                    live.update(table)
                else:
                    live.update(f"[red]Error connecting to API: {pool_status.get('error', 'Unknown')}[/red]")
                
                await asyncio.sleep(refresh_interval)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                live.update(f"[red]Error: {e}[/red]")
                await asyncio.sleep(refresh_interval)

def main_dashboard():
    """Point d'entrée du dashboard"""
    import argparse
    
    parser = argparse.ArgumentParser(description="TaskMaster Pool Dashboard")
    parser.add_argument("--api", default="http://localhost:8000", help="API URL")
    parser.add_argument("--refresh", type=int, default=5, help="Refresh interval (seconds)")
    
    args = parser.parse_args()
    
    try:
        asyncio.run(dashboard_loop(args.api, args.refresh))
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard stopped by user[/yellow]")

# ========== session_validator.py ==========
"""
Validateur de sessions TaskMaster
Vérifie l'état des sessions et nettoie les sessions orphelines
"""

import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Any

async def validate_sessions(api_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """Valide toutes les sessions actives"""
    validation_report = {
        "timestamp": datetime.now().isoformat(),
        "total_instances": 0,
        "healthy_instances": 0,
        "unhealthy_instances": 0,
        "orphaned_tasks": [],
        "recommendations": []
    }
    
    async with aiohttp.ClientSession() as session:
        # Récupérer toutes les instances
        try:
            async with session.get(f"{api_url}/instances") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    instances = data.get("instances", [])
                    validation_report["total_instances"] = len(instances)
                    
                    # Valider chaque instance
                    for instance in instances:
                        instance_id = instance["instance_id"]
                        
                        # Récupérer les détails
                        async with session.get(f"{api_url}/instances/{instance_id}") as detail_resp:
                            if detail_resp.status == 200:
                                details = await detail_resp.json()
                                
                                # Vérifier la santé
                                health = details.get("health", {})
                                if health.get("status") == "healthy":
                                    validation_report["healthy_instances"] += 1
                                else:
                                    validation_report["unhealthy_instances"] += 1
                                    validation_report["recommendations"].append(
                                        f"Consider restarting instance {instance_id}"
                                    )
                                
                                # Vérifier les tâches bloquées
                                for task in details.get("tasks", []):
                                    if task["status"] == "active":
                                        # Vérifier si la tâche est bloquée (>1h)
                                        created = datetime.fromisoformat(task["created_at"])
                                        if datetime.now() - created > timedelta(hours=1):
                                            validation_report["orphaned_tasks"].append({
                                                "task_id": task["task_id"],
                                                "instance_id": instance_id,
                                                "created_at": task["created_at"],
                                                "age_hours": (datetime.now() - created).total_seconds() / 3600
                                            })
                
        except Exception as e:
            validation_report["error"] = str(e)
    
    # Recommandations générales
    if validation_report["orphaned_tasks"]:
        validation_report["recommendations"].append(
            f"Found {len(validation_report['orphaned_tasks'])} potentially stuck tasks"
        )
    
    if validation_report["unhealthy_instances"] > validation_report["total_instances"] * 0.3:
        validation_report["recommendations"].append(
            "High percentage of unhealthy instances - check system resources"
        )
    
    return validation_report

async def cleanup_orphaned_tasks(api_url: str, orphaned_tasks: List[Dict[str, Any]]):
    """Nettoie les tâches orphelines"""
    results = []
    
    async with aiohttp.ClientSession() as session:
        for task in orphaned_tasks:
            try:
                async with session.post(
                    f"{api_url}/tasks/{task['task_id']}/cancel",
                    params={"instance_id": task["instance_id"]}
                ) as resp:
                    if resp.status == 200:
                        results.append({
                            "task_id": task["task_id"],
                            "status": "cancelled"
                        })
                    else:
                        results.append({
                            "task_id": task["task_id"],
                            "status": "failed",
                            "error": f"HTTP {resp.status}"
                        })
            except Exception as e:
                results.append({
                    "task_id": task["task_id"],
                    "status": "error",
                    "error": str(e)
                })
    
    return results

def main_validator():
    """Point d'entrée du validateur"""
    import argparse
    
    parser = argparse.ArgumentParser(description="TaskMaster Session Validator")
    parser.ad



