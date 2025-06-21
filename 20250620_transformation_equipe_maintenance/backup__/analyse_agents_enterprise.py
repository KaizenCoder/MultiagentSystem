#!/usr/bin/env python3
"""
🎖️ ANALYSE ÉQUIPE MAINTENANCE - AGENTS ENTERPRISE
Mission: Analyser les 4 agents enterprise sans les modifier
"""

import sys
import time
import asyncio
from pathlib import Path

# Configuration PYTHONPATH
sys.path.insert(0, r'C:\Dev\nextgeneration')

try:
    from agent_0_chef_equipe_coordinateur import Agent0ChefEquipeCoordinateur
except ImportError as e:
    print(f"❌ Erreur import chef équipe: {e}")
    sys.exit(1)

async def analyser_agents_enterprise():
    """Analyser les 4 agents enterprise avec l'équipe de maintenance"""
    print('🎖️ ANALYSE ÉQUIPE MAINTENANCE - AGENTS ENTERPRISE')
    print('=' * 60)
    
    # Agents à analyser
    agents_a_analyser = [
        'agent_ARCHITECTURE_22_enterprise_consultant.py',
        'agent_FASTAPI_23_orchestration_enterprise.py', 
        'agent_STORAGE_24_enterprise_manager.py',
        'agent_MONITORING_25_production_enterprise.py'
    ]
    
    print(f'🎯 Agents à analyser: {len(agents_a_analyser)}')
    for agent in agents_a_analyser:
        print(f'  📄 {agent}')
    
    # Configuration pour analyse spécifique
    config = {
        'target_directory': 'agent_factory_implementation/agents',
        'specific_files': agents_a_analyser,
        'analysis_mode': 'enterprise_diagnostic',
        'modifications_allowed': False,
        'focus_files': agents_a_analyser
    }
    
    # Lancement équipe maintenance
    try:
        chef = Agent0ChefEquipeCoordinateur(config)
        
        print('\n🚀 Lancement analyse équipe maintenance...')
        start_time = time.time()
        
        workflow_result = await chef.workflow_maintenance_complete()
        execution_time = time.time() - start_time
        
        print(f'\n✅ ANALYSE TERMINÉE en {execution_time:.2f}s')
        print(f'📊 Statut: {workflow_result.get("success", "Unknown")}')
        print(f'🎯 Agents analysés: {len(agents_a_analyser)}')
        
        return workflow_result
        
    except Exception as e:
        print(f'❌ Erreur analyse: {e}')
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    result = asyncio.run(analyser_agents_enterprise()) 



