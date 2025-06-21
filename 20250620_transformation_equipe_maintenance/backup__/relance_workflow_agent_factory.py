#!/usr/bin/env python3
"""
🎖️ Relance Workflow - Analyse Agent Factory Implementation
Mission: Analyser les agents dans C:\Dev\nextgeneration\agent_factory_implementation
"""

import asyncio
import sys
from pathlib import Path
from agent_0_chef_equipe_coordinateur import Agent0ChefEquipeCoordinateur

async def relancer_workflow_agent_factory():
    """Relancer le workflow pour analyser agent_factory_implementation"""
    print("🎖️ RELANCE WORKFLOW - ANALYSE AGENT FACTORY IMPLEMENTATION")
    print("=" * 60)
    
    # Configuration spécifique pour agent_factory_implementation
    target_path = Path("C:/Dev/nextgeneration/agent_factory_implementation")
    workspace_path = Path(".")
    
    print(f"🎯 Répertoire cible: {target_path}")
    print(f"📂 Workspace: {workspace_path}")
    
    # Vérification que le répertoire existe
    if not target_path.exists():
        print(f"❌ ERREUR: Répertoire non trouvé: {target_path}")
        return
    
    print(f"✅ Répertoire trouvé: {target_path}")
    
    # Initialiser le chef d'équipe avec la configuration spécifique
    chef = Agent0ChefEquipeCoordinateur(
        target_path=str(target_path),
        workspace_path=str(workspace_path),
        agent_id=f"chef_factory_analysis_{Path().cwd().name}",
        safe_mode=True,
        rapport_detaille=True
    )
    
    try:
        # Démarrage du chef d'équipe
        print("\n🚀 Démarrage du chef d'équipe...")
        await chef.startup()
        
        # Lancer le workflow de maintenance complète
        print("\n🔄 Lancement du workflow de maintenance complète...")
        print("📊 Analyse des agents dans agent_factory_implementation...")
        
        resultats = await chef.workflow_maintenance_complete()
        
        print("\n" + "=" * 60)
        print("🎉 WORKFLOW TERMINÉ AVEC SUCCÈS")
        print("=" * 60)
        
        # Affichage des résultats
        print(f"📋 Workflow ID: {resultats.get('workflow_id', 'N/A')}")
        print(f"🎖️ Chef d'équipe: {resultats.get('chef_equipe_id', 'N/A')}")
        print(f"📂 Répertoire analysé: {resultats.get('target_path', 'N/A')}")
        print(f"⏱️ Durée totale: {resultats.get('duree_totale', 'N/A')}")
        print(f"✅ Statut: {resultats.get('status', 'N/A')}")
        
        # Résumé des étapes
        etapes = resultats.get('etapes', {})
        print(f"\n📊 RÉSUMÉ DES ÉTAPES ({len(etapes)} étapes):")
        for nom_etape, details in etapes.items():
            status_icon = "✅" if details.get('status') == 'complete' else "❌"
            print(f"   {status_icon} {nom_etape}: {details.get('status', 'inconnu')}")
        
        # Recommandations finales
        recommandations = resultats.get('recommandations_finales', [])
        if recommandations:
            print(f"\n🎯 RECOMMANDATIONS FINALES ({len(recommandations)}):")
            for i, rec in enumerate(recommandations, 1):
                print(f"   {i}. {rec}")
        
        # Actions suivantes
        actions = resultats.get('actions_suivantes', [])
        if actions:
            print(f"\n🚀 ACTIONS SUIVANTES ({len(actions)}):")
            for i, action in enumerate(actions, 1):
                print(f"   {i}. {action}")
        
        return resultats
        
    except Exception as e:
        print(f"\n❌ ERREUR WORKFLOW: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        # Arrêt propre du chef d'équipe
        try:
            await chef.shutdown()
            print("\n🛑 Chef d'équipe arrêté proprement")
        except Exception as e:
            print(f"⚠️ Erreur arrêt chef d'équipe: {e}")

if __name__ == "__main__":
    print("🎖️ RELANCE WORKFLOW AGENT FACTORY IMPLEMENTATION")
    print("Mission: Analyser tous les agents dans agent_factory_implementation")
    print()
    
    # Exécution du workflow
    resultats = asyncio.run(relancer_workflow_agent_factory())
    
    if resultats:
        print("\n🎉 Mission accomplie ! Workflow exécuté avec succès.")
    else:
        print("\n❌ Mission échouée. Consultez les logs pour plus de détails.") 



