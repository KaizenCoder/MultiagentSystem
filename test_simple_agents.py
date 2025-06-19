#!/usr/bin/env python3
"""
Test simple pour diagnostiquer les problèmes avec les agents template-based
"""

import sys
import traceback

def test_imports():
    """Test des imports de base"""
    print("=== Test des imports ===")
    
    try:
        print("Import TemplateManager...")
        from core.template_manager import TemplateManager
        print("✅ TemplateManager importé")
        
        print("Import BaseAgent...")
        from core.base_agent_template import BaseAgent, TemplateBasedAgent
        print("✅ BaseAgent importé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur import: {e}")
        traceback.print_exc()
        return False

def test_template_manager_creation():
    """Test de création du TemplateManager"""
    print("\n=== Test création TemplateManager ===")
    
    try:
        from core.template_manager import TemplateManager
        
        print("Création du TemplateManager...")
        manager = TemplateManager("templates")
        print("✅ TemplateManager créé")
        
        print("Vérification des templates...")
        templates = manager.list_templates()
        print(f"✅ {len(templates)} templates trouvés")
        
        for template in templates:
            print(f"  - {template['name']}")
        
        return manager
        
    except Exception as e:
        print(f"❌ Erreur création TemplateManager: {e}")
        traceback.print_exc()
        return None

def test_agent_creation(manager):
    """Test de création d'un agent simple"""
    print("\n=== Test création agent ===")
    
    try:
        templates = manager.list_templates()
        if not templates:
            print("❌ Aucun template disponible")
            return None
        
        template_name = templates[0]['name']
        print(f"Création agent avec template: {template_name}")
        
        agent = manager.create_agent(template_name, "test_agent")
        
        if agent:
            print(f"✅ Agent créé: {agent.config.name}")
            print(f"   Status: {agent.status}")
            print(f"   Rôle: {agent.config.role}")
            return agent
        else:
            print("❌ Agent non créé")
            return None
            
    except Exception as e:
        print(f"❌ Erreur création agent: {e}")
        traceback.print_exc()
        return None

def main():
    """Test principal"""
    print("🔍 Diagnostic des agents template-based")
    print("=" * 50)
    
    # Test 1: Imports
    if not test_imports():
        print("❌ Échec des imports")
        return False
    
    # Test 2: TemplateManager
    manager = test_template_manager_creation()
    if not manager:
        print("❌ Échec création TemplateManager")
        return False
    
    # Test 3: Agent
    agent = test_agent_creation(manager)
    if not agent:
        print("❌ Échec création agent")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Diagnostic réussi - Les agents fonctionnent!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        traceback.print_exc()
        sys.exit(1) 