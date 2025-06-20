#!/usr/bin/env python3
"""
🎖️ Relance Workflow - Analyse C:\Dev\agents
Mission: Analyser tous les agents dans C:\Dev\agents
"""

import asyncio
import sys
from pathlib import Path
from agent_0_chef_equipe_coordinateur import Agent0ChefEquipeCoordinateur

async def relancer_workflow_agents_cdev():
    """Relancer le workflow pour analyser C:\Dev\agents"""
    print("🎖️ RELANCE WORKFLOW - ANALYSE C:\\Dev\\agents")
    print("=" * 60)
    
    # Configuration spécifique pour C:\Dev\agents
    target_path = Path("C:/Dev/agents")
    workspace_path = Path(".")
    
    print(f"🎯 Répertoire cible: {target_path}")
    print(f"🏠 Workspace: {workspace_path}")
    
    # Vérification répertoire existe
    if not target_path.exists():
        print(f"❌ ERREUR: Répertoire {target_path} n'existe pas")
        return
    
    print(f"✅ Répertoire trouvé avec {len(list(target_path.glob('*.py')))} fichiers Python")
    
    # Initialisation chef d'équipe avec nouvelle configuration
    print("\n🎖️ Initialisation Chef d'Équipe...")
    chef = Agent0ChefEquipeCoordinateur()
    
    # Configuration pour C:\Dev\agents
    chef.target_path = target_path
    chef.workspace_path = workspace_path
    
    # Démarrage et exécution
    print("🚀 Démarrage du workflow d'analyse...")
    await chef.startup()
    
    # Exécution du workflow complet
    try:
        workflow_result = await chef.workflow_maintenance_complete()
        print("\n" + "="*80)
        print("🎉 WORKFLOW TERMINÉ AVEC SUCCÈS")
        print("="*80)
        print(f"Workflow ID: {workflow_result.get('workflow_id', 'N/A')}")
        print(f"Agents analysés: {len(list(target_path.glob('*.py')))}")
        print(f"Statut: {workflow_result.get('status', 'N/A')}")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ ERREUR WORKFLOW: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await chef.shutdown()

if __name__ == "__main__":
    asyncio.run(relancer_workflow_agents_cdev()) 