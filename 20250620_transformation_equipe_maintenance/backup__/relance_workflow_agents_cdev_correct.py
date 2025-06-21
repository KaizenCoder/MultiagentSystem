#!/usr/bin/env python3
"""
🎖️ Relance Workflow - Analyse C:\Dev\agents (CORRIGÉ)
Mission: Analyser tous les 39 agents dans C:\Dev\agents
"""

import asyncio
import sys
from pathlib import Path
from agent_0_chef_equipe_coordinateur import Agent0ChefEquipeCoordinateur

async def relancer_workflow_agents_cdev_correct():
    """Relancer le workflow pour analyser C:\Dev\agents - VERSION CORRIGÉE"""
    print("🎖️ RELANCE WORKFLOW - ANALYSE C:\\Dev\\agents (CORRIGÉ)")
    print("=" * 70)
    
    # Configuration spécifique pour C:\Dev\agents
    target_path = Path("C:/Dev/agents")
    workspace_path = Path(".")
    
    print(f"🎯 Répertoire cible: {target_path}")
    print(f"🏠 Workspace: {workspace_path}")
    
    # Vérification répertoire existe
    if not target_path.exists():
        print(f"❌ ERREUR: Le répertoire {target_path} n'existe pas")
        return
    
    print(f"✅ Répertoire {target_path} trouvé")
    
    # Compter les agents
    agents_py = list(target_path.rglob("*.py"))
    print(f"🔍 Agents Python détectés: {len(agents_py)}")
    
    # Créer le chef d'équipe avec configuration spécifique
    chef = Agent0ChefEquipeCoordinateur(
        workspace_path=workspace_path,
        target_path=target_path,  # Utiliser le bon chemin
        mode_debug=True
    )
    
    print("\n🚀 Lancement du workflow de maintenance...")
    print("=" * 50)
    
    try:
        # Lancer le workflow de maintenance
        workflow_result = await chef.workflow_maintenance_complete()
        
        print(f"\n✅ WORKFLOW TERMINÉ AVEC SUCCÈS!")
        print(f"⏱️  Durée: {workflow_result.get('duree_totale', 'N/A')} secondes")
        print(f"📊 Agents analysés: {len(agents_py)}")
        
        # Afficher les résultats des agents
        if 'resultats_agents' in workflow_result:
            print("\n📋 RÉSULTATS DES AGENTS:")
            for agent_id, result in workflow_result['resultats_agents'].items():
                status = "✅" if result.get('status') == 'SUCCESS' else "❌"
                duree = result.get('duree_secondes', 0)
                print(f"  {status} {agent_id}: {duree:.2f}s")
        
        return workflow_result
        
    except Exception as e:
        print(f"❌ ERREUR lors du workflow: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🎖️ DÉMARRAGE ANALYSE C:\\Dev\\agents")
    result = asyncio.run(relancer_workflow_agents_cdev_correct())
    
    if result:
        print("\n🎉 ANALYSE TERMINÉE AVEC SUCCÈS!")
        print("📁 Consultez le répertoire 'reports' pour les rapports détaillés")
    else:
        print("\n💥 ÉCHEC DE L'ANALYSE")
        sys.exit(1) 