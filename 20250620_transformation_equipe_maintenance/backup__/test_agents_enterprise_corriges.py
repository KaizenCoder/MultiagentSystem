#!/usr/bin/env python3
"""
🧪 TESTS AGENTS ENTERPRISE CORRIGÉS
===================================

Mission: Tester les 4 agents enterprise après correction des erreurs de syntaxe
Agents: 22 (Architecture), 23 (FastAPI), 24 (Storage), 25 (Monitoring)
"""

import sys
import time
import asyncio
from pathlib import Path

# Configuration PYTHONPATH
sys.path.insert(0, r'C:\Dev\nextgeneration')

def test_import_agent(agent_name, agent_file):
    """Test d'import d'un agent"""
    try:
        print(f"🧪 Test import {agent_name}...")
        
        # Import dynamique
        spec = __import__('importlib.util', fromlist=['spec_from_file_location']).spec_from_file_location(
            agent_name, agent_file
        )
        module = __import__('importlib.util', fromlist=['module_from_spec']).module_from_spec(spec)
        spec.loader.exec_module(module)
        
        print(f"✅ {agent_name} - Import réussi")
        return True, module
        
    except Exception as e:
        print(f"❌ {agent_name} - Erreur import: {e}")
        return False, None

def test_agent_creation(agent_name, module):
    """Test de création d'un agent"""
    try:
        print(f"🧪 Test création {agent_name}...")
        
        # Recherche de la fonction factory
        factory_functions = [name for name in dir(module) if name.startswith('create_agent_')]
        
        if not factory_functions:
            # Recherche de classes d'agents
            agent_classes = [name for name in dir(module) if 'Agent' in name and name.startswith('Agent')]
            if agent_classes:
                agent_class = getattr(module, agent_classes[0])
                agent = agent_class()
                print(f"✅ {agent_name} - Création réussie (classe directe)")
                return True, agent
            else:
                print(f"⚠️ {agent_name} - Aucune factory/classe trouvée")
                return False, None
        else:
            # Utilisation de la factory
            factory_func = getattr(module, factory_functions[0])
            agent = factory_func()
            print(f"✅ {agent_name} - Création réussie (factory)")
            return True, agent
            
    except Exception as e:
        print(f"❌ {agent_name} - Erreur création: {e}")
        return False, None

async def test_agent_methods(agent_name, agent):
    """Test des méthodes async d'un agent"""
    try:
        print(f"🧪 Test méthodes async {agent_name}...")
        
        # Test get_capabilities (sync)
        if hasattr(agent, 'get_capabilities'):
            capabilities = agent.get_capabilities()
            print(f"  📋 Capacités: {len(capabilities)} trouvées")
        
        # Test startup (async)
        if hasattr(agent, 'startup'):
            await agent.startup()
            print(f"  🚀 Startup: OK")
        
        # Test health_check (async)
        if hasattr(agent, 'health_check'):
            health = await agent.health_check()
            print(f"  🩺 Health check: {health.get('status', 'unknown')}")
        
        # Test shutdown (async)
        if hasattr(agent, 'shutdown'):
            await agent.shutdown()
            print(f"  🛑 Shutdown: OK")
            
        print(f"✅ {agent_name} - Toutes les méthodes fonctionnent")
        return True
        
    except Exception as e:
        print(f"❌ {agent_name} - Erreur méthodes: {e}")
        return False

async def test_tous_les_agents():
    """Test complet des 4 agents enterprise"""
    print("🧪 TESTS AGENTS ENTERPRISE CORRIGÉS")
    print("=" * 50)
    
    # Configuration des agents à tester
    agents_config = [
        {
            "name": "Agent 22 - Architecture",
            "file": Path("../agent_factory_implementation/agents/agent_ARCHITECTURE_22_enterprise_consultant.py")
        },
        {
            "name": "Agent 23 - FastAPI (CORRIGÉ)",
            "file": Path("../agent_factory_implementation/agents/agent_FASTAPI_23_orchestration_enterprise.py")
        },
        {
            "name": "Agent 24 - Storage",
            "file": Path("../agent_factory_implementation/agents/agent_STORAGE_24_enterprise_manager.py")
        },
        {
            "name": "Agent 25 - Monitoring (CORRIGÉ)",
            "file": Path("../agent_factory_implementation/agents/agent_MONITORING_25_production_enterprise.py")
        }
    ]
    
    resultats = []
    
    for config in agents_config:
        print(f"\n🎯 TEST: {config['name']}")
        print("-" * 40)
        
        # Test 1: Import
        import_ok, module = test_import_agent(config['name'], config['file'])
        if not import_ok:
            resultats.append({
                "agent": config['name'],
                "import": False,
                "creation": False,
                "methodes": False,
                "global": False
            })
            continue
        
        # Test 2: Création
        creation_ok, agent = test_agent_creation(config['name'], module)
        if not creation_ok:
            resultats.append({
                "agent": config['name'],
                "import": True,
                "creation": False,
                "methodes": False,
                "global": False
            })
            continue
        
        # Test 3: Méthodes async
        methodes_ok = await test_agent_methods(config['name'], agent)
        
        # Résultat global
        global_ok = import_ok and creation_ok and methodes_ok
        
        resultats.append({
            "agent": config['name'],
            "import": import_ok,
            "creation": creation_ok,
            "methodes": methodes_ok,
            "global": global_ok
        })
    
    # Rapport final
    print("\n" + "=" * 50)
    print("📊 RAPPORT FINAL DES TESTS")
    print("=" * 50)
    
    agents_ok = 0
    total_agents = len(resultats)
    
    for resultat in resultats:
        status = "✅ FONCTIONNEL" if resultat["global"] else "❌ DÉFAILLANT"
        print(f"{status} - {resultat['agent']}")
        
        if resultat["global"]:
            agents_ok += 1
        else:
            print(f"  Import: {'✅' if resultat['import'] else '❌'}")
            print(f"  Création: {'✅' if resultat['creation'] else '❌'}")
            print(f"  Méthodes: {'✅' if resultat['methodes'] else '❌'}")
    
    print(f"\n🎯 RÉSULTAT GLOBAL: {agents_ok}/{total_agents} agents fonctionnels")
    
    if agents_ok == total_agents:
        print("🏆 SUCCÈS COMPLET - Tous les agents sont fonctionnels!")
        return True
    else:
        print(f"⚠️ PROBLÈMES DÉTECTÉS - {total_agents - agents_ok} agents défaillants")
        return False

if __name__ == "__main__":
    print("🧪 Lancement des tests agents enterprise...")
    start_time = time.time()
    
    try:
        # Exécution des tests async
        success = asyncio.run(test_tous_les_agents())
        
        duration = time.time() - start_time
        print(f"\n⏱️ Tests terminés en {duration:.2f} secondes")
        
        if success:
            print("🎉 VERDICT: AGENTS ENTERPRISE FONCTIONNELS!")
            sys.exit(0)
        else:
            print("🚨 VERDICT: PROBLÈMES DÉTECTÉS!")
            sys.exit(1)
            
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE: {e}")
        sys.exit(1) 



