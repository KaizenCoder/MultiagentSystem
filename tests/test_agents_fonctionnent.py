#!/usr/bin/env python3
"""
Test simple pour vérifier que les agents template-based fonctionnent
"""

import sys
import traceback

# Golden Source Logging
from core import logging_manager

# Configuration du logging
# On utilise un nom de configuration générique car on fournit une custom_config.
logger = logging_manager.get_logger('custom_test_config', custom_config={
    "logger_name": "TestAgents",
    "log_level": "DEBUG",
    "async_enabled": False, # Important pour les tests
})

def test_imports():
    """Test des imports"""
    logger.info("=== Test des imports ===")
    
    try:
        from template_manager import TemplateManager
        from base_agent_template import BaseAgent, TemplateBasedAgent
        logger.info("✅ Imports réussis")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur import: {e}", exc_info=True)
        return False

def test_template_manager():
    """Test du TemplateManager"""
    logger.info("\n=== Test du TemplateManager ===")
    
    try:
        from template_manager import TemplateManager
        
        # Créer le gestionnaire
        manager = TemplateManager("templates")
        logger.info("✅ TemplateManager créé")
        
        # Lister les templates
        templates = manager.list_templates()
        logger.info(f"✅ {len(templates)} templates chargés")
        
        for template in templates:
            logger.debug(f"  - {template['name']} (v{template['version']}) - {template['role']}")
        
        return manager
        
    except Exception as e:
        logger.error(f"❌ Erreur TemplateManager: {e}", exc_info=True)
        return None

def test_agent_creation(manager):
    """Test de création d'agent"""
    logger.info("\n=== Test de création d'agent ===")
    
    try:
        templates = manager.list_templates()
        if not templates:
            logger.error("❌ Aucun template disponible")
            return None
        
        # Prendre le premier template
        template_name = templates[0]['name']
        logger.info(f"Création d'un agent avec le template: {template_name}")
        
        agent = manager.create_agent(template_name, "test_agent")
        
        if agent:
            logger.info(f"✅ Agent créé: {agent.config.name}")
            logger.debug(f"   Status: {agent.status}")
            logger.debug(f"   Rôle: {agent.config.role}")
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
    """Test d'exécution de tâche"""
    logger.info("\n=== Test d'exécution de tâche ===")
    
    try:
        # Tâche simple
        task = {
            'name': 'Test simple',
            'type': 'generic',
            'description': 'Tâche de test basique'
        }
        
        result = agent.execute_task(task)
        logger.info(f"✅ Tâche exécutée - Status: {result['status']}")
        
        if result['status'] == 'success':
            logger.info(f"   Message: {result['result']['message']}")
            logger.info(f"   Agent: {result['agent']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur exécution: {e}", exc_info=True)
        return False

def main():
    """Test principal"""
    logger.info("🚀 Test des agents template-based")
    logger.info("=" * 50)
    
    # Test 1: Imports
    if not test_imports():
        logger.critical("❌ Échec des imports")
        return False
    
    # Test 2: TemplateManager
    manager = test_template_manager()
    if not manager:
        logger.critical("❌ Échec du TemplateManager")
        return False
    
    # Test 3: Création d'agent
    agent = test_agent_creation(manager)
    if not agent:
        logger.critical("❌ Échec de création d'agent")
        return False
    
    # Test 4: Exécution de tâche
    if not test_agent_execution(agent):
        logger.critical("❌ Échec d'exécution")
        return False
    
    logger.info("\n" + "=" * 50)
    logger.info("✅ TOUS LES TESTS SONT PASSÉS!")
    logger.info("✅ Les agents template-based fonctionnent correctement!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.critical(f"\n💥 Erreur inattendue: {e}", exc_info=True)
        sys.exit(1) 



