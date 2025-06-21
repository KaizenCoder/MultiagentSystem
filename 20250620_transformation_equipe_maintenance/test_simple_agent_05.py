#!/usr/bin/env python3
"""
Test simple Agent 05 - Débogage
"""

import asyncio
import sys
from pathlib import Path

print("🔍 DÉBUT TEST SIMPLE AGENT 05")

# Ajouter le chemin pour les imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

print(f"Chemin ajouté : {current_dir}")

try:
    from agent_equipe_maintenance.agent_MAINTENANCE_05_peer_reviewer_enrichi import create_agent_5_peer_reviewer_enrichi
    print("✅ Import réussi")
except Exception as e:
    print(f"❌ Erreur import : {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

async def test_simple():
    print("🚀 Création agent...")
    
    try:
        agent = create_agent_5_peer_reviewer_enrichi()
        print(f"✅ Agent créé : {agent.agent_id}")
        
        await agent.startup()
        print("✅ Agent démarré")
        
        health = await agent.health_check()
        print(f"✅ Health check : {health}")
        
        capabilities = agent.get_capabilities()
        print(f"✅ Capacités : {len(capabilities)}")
        
        await agent.shutdown()
        print("✅ Agent arrêté")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Lancement test asyncio...")
    asyncio.run(test_simple())
    print("🏁 FIN TEST") 