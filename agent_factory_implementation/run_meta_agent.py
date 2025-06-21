#!/usr/bin/env python3
"""
🎯 SCRIPT DE LANCEMENT MÉTA-AGENT PATTERN FACTORY
==================================================
Script simplifié pour lancer le méta-agent stratégique conforme Pattern Factory
"""

import asyncio
import sys
from pathlib import Path

# Ajout du chemin pour les imports
sys.path.append(str(Path(__file__).parent))

from agents.agent_meta_strategique_pattern_factory import create_meta_strategique_agent
from core.agent_factory_architecture import Task

async def main():
    print("🎯 LANCEMENT MÉTA-AGENT PATTERN FACTORY")
    print("=" * 50)
    
    # Configuration avec le bon chemin
    config = {
        "workspace_path": "agent_factory_implementation",  # Chemin relatif depuis le répertoire de lancement
        "performance_thresholds": {
            "response_time_ms": 100,
            "error_rate_percent": 5,
            "cpu_usage_percent": 80,
            "memory_usage_percent": 85,
            "success_rate_percent": 95
        }
    }
    
    print("Configuration par défaut utilisée")
    
    # Création de l'agent
    agent = create_meta_strategique_agent(**config)
    print(f"✅ Agent créé: {agent.id}")
    print(f"📋 Capacités: {agent.get_capabilities()}")
    
    # Démarrage
    await agent.startup()
    print("🚀 Agent démarré avec succès")
    
    # Vérification santé
    health = await agent.health_check()
    print(f"🔍 Santé: {health['status']}")
    print(f"📊 Uptime: {health['uptime_seconds']:.1f}s")
    
    print("\n🚀 EXÉCUTION TÂCHES STRATÉGIQUES")
    print("-" * 40)
    
    # Tâches à exécuter
    tasks = [
        ("analyze_performance", {}),
        ("detect_anomalies", {}),
        ("generate_insights", {}),
        ("strategic_analysis", {}),
        ("generate_report", {"report_type": "executive"}),
        ("monitor_system", {})
    ]
    
    results = []
    total_time = 0
    
    for i, (task_type, params) in enumerate(tasks, 1):
        print(f"\n📋 Tâche {i}/{len(tasks)}: {task_type}")
        
        # Création de la tâche
        task = Task(
            id=f"task_{i}_{task_type}",
            type=task_type,
            params=params
        )
        
        # Exécution
        result = agent.execute_task(task)
        results.append(result)
        
        # Affichage résultat
        if result.success:
            exec_time = result.metrics.get("execution_time_seconds", 0)
            total_time += exec_time
            print(f"   ✅ SUCCÈS - Durée: {exec_time:.3f}s")
            
            # Métriques spécifiques selon le type
            if "performance_score" in result.metrics:
                print(f"   📊 Score performance: {result.metrics['performance_score']:.1f}/100")
            if "anomalies_found" in result.data:
                print(f"   🔍 Anomalies détectées: {result.data['anomalies_found']}")
            if "insights" in result.data:
                print(f"   💡 Insights générés: {len(result.data['insights'])}")
            if "overall_health_score" in result.data.get("strategic_summary", {}):
                score = result.data["strategic_summary"]["overall_health_score"]
                print(f"   🎯 Score santé globale: {score:.1f}/100")
            if "report_path" in result.data:
                print(f"   📋 Rapport: {Path(result.data['report_path']).name}")
        else:
            print(f"   ❌ ÉCHEC: {result.error}")
    
    print(f"\n📊 RÉSUMÉ DES RÉSULTATS")
    
    # Statistiques globales
    successful_tasks = sum(1 for r in results if r.success)
    final_result = {
        "success": successful_tasks == len(tasks),
        "tasks_executed": len(tasks),
        "successful_tasks": successful_tasks,
        "total_execution_time": total_time,
        "insights_generated": sum(len(r.data.get("insights", [])) for r in results if r.success)
    }
    
    print(f"📊 Résultat final: {final_result}")
    
    # Arrêt propre
    await agent.shutdown()
    
    return final_result

if __name__ == "__main__":
    result = asyncio.run(main()) 



