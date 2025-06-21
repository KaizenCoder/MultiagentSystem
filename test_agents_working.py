#!/usr/bin/env python3
"""
Test des agents template-based
Vérifie que les agents créés à partir des templates JSON fonctionnent correctement
"""

import sys
import json
from logging_manager_optimized import LoggingManager
from pathlib import Path

# Configuration du logging
# LoggingManager NextGeneration - Tests
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={
            "logger_name": "test_agents_working",
            "log_level": "DEBUG",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": False,  # Tests synchrones
            "console_output": True
        })s - %(name)s - %(levelname)s - %(message)s')

def test_template_manager():
    """Teste le TemplateManager"""
    print("=== Test du TemplateManager ===")
    
    try:
        from core.template_manager import TemplateManager
        
        # Créer le gestionnaire
        manager = TemplateManager("templates")
        
        # Lister les templates
        templates = manager.list_templates()
        print(f"Templates disponibles: {len(templates)}")
        
        for template in templates:
            print(f"  - {template['name']} (v{template['version']}) - {template['role']}")
        
        return manager
        
    except Exception as e:
        print(f"❌ Erreur TemplateManager: {e}")
        return None

def test_agent_creation(manager):
    """Teste la création d'agents"""
    print("\n=== Test de création d'agents ===")
    
    try:
        # Créer un agent coordinateur
        agent = manager.create_agent("Agent Coordinateur", "test_coordinator")
        
        if agent:
            print(f"✅ Agent créé: {agent.config.name}")
            print(f"   Rôle: {agent.config.role}")
            print(f"   Status: {agent.status}")
            print(f"   Capacités: {len(agent.config.capabilities)}")
            print(f"   Outils: {len(agent.config.tools)}")
            
            return agent
        else:
            print("❌ Échec de création d'agent")
            return None
            
    except Exception as e:
        print(f"❌ Erreur création agent: {e}")
        return None

def test_agent_execution(agent):
    """Teste l'exécution de tâches"""
    print("\n=== Test d'exécution de tâches ===")
    
    try:
        # Tâche simple
        task1 = {
            'name': 'Test coordination',
            'type': 'coordination',
            'description': 'Tâche de test pour la coordination'
        }
        
        result1 = agent.execute_task(task1)
        print(f"✅ Tâche 1 - Status: {result1['status']}")
        if result1['status'] == 'success':
            print(f"   Résultat: {result1['result']['message']}")
        
        # Tâche avec capacité requise
        task2 = {
            'name': 'Test analyse',
            'type': 'analysis',
            'required_capability': 'project_management'
        }
        
        result2 = agent.execute_task(task2)
        print(f"✅ Tâche 2 - Status: {result2['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur exécution: {e}")
        return False

def test_agent_status(agent):
    """Teste le statut de l'agent"""
    print("\n=== Test du statut d'agent ===")
    
    try:
        status = agent.get_status()
        print(f"✅ Status récupéré:")
        print(f"   Nom: {status['name']}")
        print(f"   Statut: {status['status']}")
        print(f"   Uptime: {status['uptime']:.2f}s")
        print(f"   Tâches complétées: {status['metrics']['tasks_completed']}")
        print(f"   Tâches échouées: {status['metrics']['tasks_failed']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur statut: {e}")
        return False

def test_multiple_agents(manager):
    """Teste la création de plusieurs agents"""
    print("\n=== Test de plusieurs agents ===")
    
    try:
        templates = manager.list_templates()
        agents_created = []
        
        for template in templates[:3]:  # Tester les 3 premiers templates
            agent_id = f"test_{template['name'].lower().replace(' ', '_')}"
            agent = manager.create_agent(template['name'], agent_id)
            
            if agent:
                agents_created.append(agent_id)
                print(f"✅ Agent créé: {agent.config.name} (ID: {agent_id})")
        
        # Lister les agents actifs
        active_agents = manager.list_active_agents()
        print(f"\n📋 Agents actifs: {len(active_agents)}")
        
        for agent_info in active_agents:
            print(f"  - {agent_info['name']} ({agent_info['id']}) - {agent_info['status']}")
        
        return agents_created
        
    except Exception as e:
        print(f"❌ Erreur agents multiples: {e}")
        return []

def main():
    """Fonction principale de test"""
    print("🚀 Test des agents template-based")
    print("=" * 50)
    
    # Test 1: TemplateManager
    manager = test_template_manager()
    if not manager:
        print("❌ Échec du test TemplateManager")
        return False
    
    # Test 2: Création d'agent
    agent = test_agent_creation(manager)
    if not agent:
        print("❌ Échec du test de création d'agent")
        return False
    
    # Test 3: Exécution de tâches
    if not test_agent_execution(agent):
        print("❌ Échec du test d'exécution")
        return False
    
    # Test 4: Statut d'agent
    if not test_agent_status(agent):
        print("❌ Échec du test de statut")
        return False
    
    # Test 5: Agents multiples
    agents = test_multiple_agents(manager)
    if not agents:
        print("❌ Échec du test d'agents multiples")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Tous les tests sont passés avec succès!")
    print(f"   Templates chargés: {len(manager.list_templates())}")
    print(f"   Agents créés: {len(manager.list_active_agents())}")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1) 