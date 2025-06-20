#!/usr/bin/env python3
"""
🧪 TEST SIMPLE AGENT - NOUVEAUX TESTS DÉVELOPPEMENT INFORMATIQUE
================================================================

Script simple pour tester l'agent avec les nouveaux tests techniques.
"""

import asyncio
import sys
from pathlib import Path

# Ajout du chemin pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from agents.agent_test_models_integration import AgentTestModelsIntegration

async def test_agent_simple():
    """Test simple de l'agent avec les nouveaux tests"""
    
    print("🧪 TEST SIMPLE - AGENT TESTS DÉVELOPPEMENT INFORMATIQUE")
    print("=" * 60)
    
    try:
        # Création de l'agent
        agent = AgentTestModelsIntegration()
        print("✅ Agent créé avec succès")
        
        # Démarrage
        await agent.startup()
        print("✅ Agent démarré avec succès")
        
        # Test d'une tâche simple
        result = await agent.execute_task({
            'type': 'complete_test_suite'
        })
        
        print("\n🎯 RÉSULTATS:")
        print(f"Succès: {result.get('success')}")
        print(f"Type: {result.get('test_type')}")
        print(f"Durée: {result.get('duration', 0):.2f}s")
        
        if result.get('data'):
            data = result['data']
            print(f"\n📊 DONNÉES:")
            print(f"Score technique: {data.get('test_summary', {}).get('technical_score', 'N/A')}")
            print(f"Niveau: {data.get('test_summary', {}).get('evaluation_level', 'N/A')}")
            
            # Affichage des challenges de développement
            dev_challenges = data.get('development_challenges', {})
            if dev_challenges:
                print(f"\n🚀 CHALLENGES DÉVELOPPEMENT:")
                print(f"Total: {dev_challenges.get('total_challenges', 0)}")
                print(f"Réussis: {dev_challenges.get('passed_challenges', 0)}")
                print(f"Taux de réussite: {dev_challenges.get('success_rate', 0):.1f}%")
        
        print("\n✅ TEST TERMINÉ AVEC SUCCÈS")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent_simple())
    sys.exit(0 if success else 1) 