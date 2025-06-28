#!/usr/bin/env python3
"""
🧪 TEST NOUVEAU SYSTÈME TEMPLATE-BASED

Test simple pour valider la migration vers l'approche template-based
"""

import asyncio
import sys
from pathlib import Path
import json
from datetime import datetime

# Ajout du chemin pour les imports
sys.path.insert(0, str(Path(__file__).parent))

async def test_simple():
    """Test simple du système template-based"""
    print("🚀 DÉMARRAGE TEST TEMPLATE-BASED")
    print("=" * 50)
    
    try:
        # Test 1: Import TemplateManager
        print("📋 Test 1: Import TemplateManager...")
        from core.template_manager import TemplateManager
        print("  ✅ Import réussi")
        
        # Test 2: Création manager
        print("🏭 Test 2: Création TemplateManager...")
        manager = TemplateManager("templates")
        print("  ✅ Manager créé")
        
        # Test 3: Templates disponibles
        print("📂 Test 3: Templates disponibles...")
        templates = manager.get_available_templates()
        print(f"  📋 Templates trouvés: {len(templates)}")
        for template in templates:
            print(f"    - {template}")
        
        # Test 4: Création d'un agent
        print("🤖 Test 4: Création agent...")
        if len(templates) > 0:
            template_name = templates[0]
            agent = await manager.create_agent(template_name)
            if agent:
                print(f"  ✅ Agent créé: {agent.agent_id}")
                
                # Test fonctionnalité
                status = await agent.get_status()
                capabilities = await agent.get_capabilities()
                print(f"  📊 Status: {status['status']}")
                print(f"  🛠️ Capacités: {len(capabilities)}")
            else:
                print("  ❌ Échec création agent")
        else:
            print("  ⚠️ Aucun template disponible")
        
        print("\n✨ 🏆 TEST TEMPLATE-BASED RÉUSSI ✨")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_simple())
    if result:
        print("\n🎯 Migration template-based validée!")
    else:
        print("\n🔧 Problème détecté dans la migration") 



