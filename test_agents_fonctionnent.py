#!/usr/bin/env python3
"""
Test simple pour vérifier que les agents template-based fonctionnent
"""

import sys
import traceback
from logging_manager_optimized import LoggingManager

# Configuration du logging
# LoggingManager NextGeneration - Tests
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={
            "logger_name": "test_agents_fonctionnent",
            "log_level": "DEBUG",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": False,  # Tests synchrones
            "console_output": True
        })

def test_imports():
    """Test des imports"""
    print("=== Test des imports ===")
    
    try:
        from template_manager import TemplateManager
        from base_agent_template import BaseAgent, TemplateBasedAgent
        print("✅ Imports réussis")
        return True
    except Exception as e:
        print(f"❌ Erreur import: {e}")
        traceback.print_exc()
        return False

def test_template_manager():
    """Test du TemplateManager"""
    print("\n=== Test du TemplateManager ===")
    
    try:
        from template_manager import TemplateManager
        
        # Créer le gestionnaire
        manager = TemplateManager("templates")
        print("✅ TemplateManager créé")
        
        # Lister les templates
        templates = manager.list_templates()
        print(f"✅ {len(templates)} templates chargés")
        
        for template in templates:
            print(f"  - {template['name']} (v{template['version']}) - {template['role']}")
        
        return manager
        
    except Exception as e:
        print(f"❌ Erreur TemplateManager: {e}")
        traceback.print_exc()
        return None

def test_agent_creation(manager):
    """Test de création d'agent"""
    print("\n=== Test de création d'agent ===")
    
    try:
        templates = manager.list_templates()
        if not templates:
            print("❌ Aucun template disponible")
            return None
        
        # Prendre le premier template
        template_name = templates[0]['name']
        print(f"Création d'un agent avec le template: {template_name}")
        
        agent = manager.create_agent(template_name, "test_agent")
        
        if agent:
            print(f"✅ Agent créé: {agent.config.name}")
            print(f"   Status: {agent.status}")
            print(f"   Rôle: {agent.config.role}")
            print(f"   Capacités: {len(agent.config.capabilities)}")
            print(f"   Outils: {len(agent.config.tools)}")
            
            return agent
        else:
            print("❌ Échec de création d'agent")
            return None
            
    except Exception as e:
        print(f"❌ Erreur création agent: {e}")
        traceback.print_exc()
        return None

def test_agent_execution(agent):
    """Test d'exécution de tâche"""
    print("\n=== Test d'exécution de tâche ===")
    
    try:
        # Tâche simple
        task = {
            'name': 'Test simple',
            'type': 'generic',
            'description': 'Tâche de test basique'
        }
        
        result = agent.execute_task(task)
        print(f"✅ Tâche exécutée - Status: {result['status']}")
        
        if result['status'] == 'success':
            print(f"   Message: {result['result']['message']}")
            print(f"   Agent: {result['agent']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur exécution: {e}")
        traceback.print_exc()
        return False

def main():
    """Test principal"""
    print("🚀 Test des agents template-based")
    print("=" * 50)
    
    # Test 1: Imports
    if not test_imports():
        print("❌ Échec des imports")
        return False
    
    # Test 2: TemplateManager
    manager = test_template_manager()
    if not manager:
        print("❌ Échec du TemplateManager")
        return False
    
    # Test 3: Création d'agent
    agent = test_agent_creation(manager)
    if not agent:
        print("❌ Échec de création d'agent")
        return False
    
    # Test 4: Exécution de tâche
    if not test_agent_execution(agent):
        print("❌ Échec d'exécution")
        return False
    
    print("\n" + "=" * 50)
    print("✅ TOUS LES TESTS SONT PASSÉS!")
    print("✅ Les agents template-based fonctionnent correctement!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        traceback.print_exc()
        sys.exit(1) 