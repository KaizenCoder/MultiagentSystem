#!/usr/bin/env python3

import sys
import traceback

def test_agents():
    print("🚀 Test des agents template-based")
    print("=" * 50)
    
    try:
        # Test 1: Import
        print("=== Test imports ===")
        from manager import TemplateManager
        from agent_base import TemplateBasedAgent
        print("✅ Imports réussis")
        
        # Test 2: TemplateManager
        print("\n=== Test TemplateManager ===")
        manager = TemplateManager("templates")
        print("✅ TemplateManager créé")
        
        templates = manager.list_templates()
        print(f"✅ {len(templates)} templates chargés")
        
        for template in templates:
            print(f"  - {template['name']} (v{template['version']}) - {template['role']}")
        
        # Test 3: Création d'agent
        if templates:
            print("\n=== Test création agent ===")
            template_name = templates[0]['name']
            agent = manager.create_agent(template_name, "test_agent")
            
            if agent:
                print(f"✅ Agent créé: {agent.config.name}")
                print(f"   Status: {agent.status}")
                print(f"   Rôle: {agent.config.role}")
                print(f"   Capacités: {agent.config.capabilities}")
                
                # Test 4: Exécution
                print("\n=== Test exécution ===")
                task = {'name': 'Test simple', 'type': 'generic'}
                result = agent.execute_task(task)
                print(f"✅ Tâche exécutée - Status: {result['status']}")
                print(f"   Message: {result['result']['message']}")
                
                print("\n" + "=" * 50)
                print("✅ SUCCÈS! Les agents template-based fonctionnent!")
                return True
            else:
                print("❌ Échec création agent")
                return False
        else:
            print("❌ Aucun template disponible")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_agents()
    sys.exit(0 if success else 1) 