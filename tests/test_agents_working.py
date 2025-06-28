#!/usr/bin/env python3
"""
Test des agents template-based
Vérifie que les agents créés à partir des templates JSON fonctionnent correctement
"""

import sys
import json
from pathlib import Path

# Golden Source Logging
from core import logging_manager

# Configuration du logging
logger = logging_manager.get_logger('custom_test_config_2', custom_config={
    "logger_name": "test_agents_working",
    "log_level": "DEBUG",
    "async_enabled": False, # Tests synchrones
})

def test_template_manager():
    """Teste le TemplateManager"""
    logger.info("=== Test du TemplateManager ===")
    
    try:
        from core.template_manager import TemplateManager # Note: l'import est différent ici
        
        # Créer le gestionnaire
        manager = TemplateManager("templates")
        
        # Lister les templates
        templates = manager.list_templates()
        logger.info(f"Templates disponibles: {len(templates)}")
        
        for template in templates:
            logger.debug(f"  - {template['name']} (v{template['version']}) - {template['role']}")
        
        return manager
        
    except Exception as e:
        logger.error(f"❌ Erreur TemplateManager: {e}", exc_info=True)
        return None

def test_agent_creation(manager):
    """Teste la création d'agents"""
    logger.info("\n=== Test de création d'agents ===")
    
    try:
        # Créer un agent coordinateur
        agent = manager.create_agent("Agent Coordinateur", "test_coordinator")
        
        if agent:
            logger.info(f"✅ Agent créé: {agent.config.name}")
            logger.debug(f"   Rôle: {agent.config.role}")
            logger.debug(f"   Status: {agent.status}")
            logger.debug(f"   Capacités: {len(agent.config.capabilities)}")
            logger.debug(f"   Outils: {len(agent.config.tools)}")
            
            return agent
        else:
            logger.error("❌ Échec de création d'agent")
            return None
            
    except Exception as e:
        logger.error(f"❌ Erreur création agent: {e}", exc_info=True)
        return None

def test_agent_execution(agent):
    """Teste l'exécution de tâches"""
    logger.info("\n=== Test d'exécution de tâches ===")
    
    try:
        # Tâche simple
        task1 = {
            'name': 'Test coordination',
            'type': 'coordination',
            'description': 'Tâche de test pour la coordination'
        }
        
        result1 = agent.execute_task(task1)
        logger.info(f"✅ Tâche 1 - Status: {result1['status']}")
        if result1['status'] == 'success':
            logger.info(f"   Résultat: {result1['result']['message']}")
        
        # Tâche avec capacité requise
        task2 = {
            'name': 'Test analyse',
            'type': 'analysis',
            'required_capability': 'project_management'
        }
        
        result2 = agent.execute_task(task2)
        logger.info(f"✅ Tâche 2 - Status: {result2['status']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur exécution: {e}", exc_info=True)
        return False

def test_agent_status(agent):
    """Teste le statut de l'agent"""
    logger.info("\n=== Test du statut d'agent ===")
    
    try:
        status = agent.get_status()
        logger.info(f"✅ Status récupéré:")
        logger.debug(f"   Nom: {status['name']}")
        logger.debug(f"   Statut: {status['status']}")
        logger.debug(f"   Uptime: {status['uptime']:.2f}s")
        logger.debug(f"   Tâches complétées: {status['metrics']['tasks_completed']}")
        logger.debug(f"   Tâches échouées: {status['metrics']['tasks_failed']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur statut: {e}", exc_info=True)
        return False

def test_multiple_agents(manager):
    """Teste la création de plusieurs agents"""
    logger.info("\n=== Test de plusieurs agents ===")
    
    try:
        templates = manager.list_templates()
        agents_created = []
        
        for template in templates[:3]:  # Tester les 3 premiers templates
            agent_id = f"test_{template['name'].lower().replace(' ', '_')}"
            agent = manager.create_agent(template['name'], agent_id)
            
            if agent:
                agents_created.append(agent_id)
                logger.info(f"✅ Agent créé: {agent.config.name} (ID: {agent_id})")
        
        # Lister les agents actifs
        active_agents = manager.list_active_agents()
        logger.info(f"\n📋 Agents actifs: {len(active_agents)}")
        
        for agent_info in active_agents:
            logger.debug(f"  - {agent_info['name']} ({agent_info['id']}) - {agent_info['status']}")
        
        return agents_created
        
    except Exception as e:
        logger.error(f"❌ Erreur agents multiples: {e}", exc_info=True)
        return []

def main():
    """Fonction principale de test"""
    logger.info("🚀 Test des agents template-based")
    logger.info("=" * 50)
    
    # Test 1: TemplateManager
    manager = test_template_manager()
    if not manager:
        logger.critical("❌ Échec du test TemplateManager")
        return False
    
    # Test 2: Création d'agent
    agent = test_agent_creation(manager)
    if not agent:
        logger.critical("❌ Échec du test de création d'agent")
        return False
    
    # Test 3: Exécution de tâches
    if not test_agent_execution(agent):
        logger.critical("❌ Échec du test d'exécution")
        return False
    
    # Test 4: Statut d'agent
    if not test_agent_status(agent):
        logger.critical("❌ Échec du test de statut")
        return False
    
    # Test 5: Agents multiples
    agents = test_multiple_agents(manager)
    if not agents:
        logger.critical("❌ Échec du test d'agents multiples")
        return False
    
    logger.info("\n" + "=" * 50)
    logger.info("✅ Tous les tests sont passés avec succès!")
    logger.info(f"   Templates chargés: {len(manager.list_templates())}")
    logger.info(f"   Agents créés: {len(manager.list_active_agents())}")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.warning("\n⚠️ Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"\n❌ Erreur inattendue: {e}", exc_info=True)
        sys.exit(1) 



