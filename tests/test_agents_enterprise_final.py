#!/usr/bin/env python3
"""
🧪 TEST FINAL - AGENTS ENTERPRISE CORRIGÉS
Mission: Vérifier que tous les 4 agents enterprise sont fonctionnels après corrections
"""

import sys
import time
import asyncio
from pathlib import Path

# Configuration PYTHONPATH pour accéder au module core
sys.path.insert(0, str(Path(__file__).parent / "agent_factory_implementation"))

def test_agent_compilation(agent_path: str, agent_name: str) -> bool:
    """Test de compilation d'un agent"""
    try:
        import py_compile
        py_compile.compile(agent_path, doraise=True)
        print(f"✅ {agent_name} - Compilation réussie")
        return True
    except Exception as e:
        print(f"❌ {agent_name} - Erreur compilation: {e}")
        return False

def test_agent_import(agent_module: str, agent_name: str) -> bool:
    """Test d'import d'un agent"""
    try:
        module = __import__(agent_module)
        print(f"✅ {agent_name} - Import réussi")
        return True
    except Exception as e:
        print(f"❌ {agent_name} - Erreur import: {e}")
        return False

def test_agent_creation(factory_function: str, agent_name: str) -> bool:
    """Test de création d'un agent via factory"""
    try:
        # Import dynamique et création
        module_name, func_name = factory_function.rsplit('.', 1)
        module = __import__(module_name, fromlist=[func_name])
        factory = getattr(module, func_name)
        agent = factory()
        print(f"✅ {agent_name} - Création réussie (ID: {agent.id})")
        return True
    except Exception as e:
        print(f"❌ {agent_name} - Erreur création: {e}")
        return False

async def test_agent_execution(factory_function: str, agent_name: str) -> bool:
    """Test d'exécution d'une tâche par l'agent"""
    try:
        from core.agent_factory_architecture import Task
        
        # Import et création agent
        module_name, func_name = factory_function.rsplit('.', 1)
        module = __import__(module_name, fromlist=[func_name])
        factory = getattr(module, func_name)
        agent = factory()
        
        # Test d'exécution avec type de tâche approprié selon l'agent
        if "Architecture" in agent_name:
            task = Task(type="design_patterns", params={"test": True})
        elif "FastAPI" in agent_name:
            task = Task(type="authentication_setup", params={"test": True})
        elif "Storage" in agent_name:
            task = Task(type="auto_scaling", params={"test": True})
        elif "Monitoring" in agent_name:
            task = Task(type="ml_anomaly_setup", params={"test": True})
        else:
            task = Task(type="generic_task", params={"test": True})
            
        result = await agent.execute_task(task)
        
        if result.success:
            print(f"✅ {agent_name} - Exécution réussie")
            return True
        else:
            print(f"❌ {agent_name} - Exécution échouée: {result.error}")
            return False
            
    except Exception as e:
        print(f"❌ {agent_name} - Erreur exécution: {e}")
        return False

async def main():
    print("🧪 TEST FINAL - AGENTS ENTERPRISE CORRIGÉS")
    print("=" * 60)
    
    # Configuration des agents à tester
    agents_config = [
        {
            "name": "Agent 22 - Architecture (CORRIGÉ)",
            "path": "agent_factory_implementation/agents/agent_ARCHITECTURE_22_enterprise_consultant.py",
            "module": "agents.agent_ARCHITECTURE_22_enterprise_consultant",
            "factory": "agents.agent_ARCHITECTURE_22_enterprise_consultant.create_agent_22_architecture"
        },
        {
            "name": "Agent 23 - FastAPI (CORRIGÉ)",
            "path": "agent_factory_implementation/agents/agent_FASTAPI_23_orchestration_enterprise.py",
            "module": "agents.agent_FASTAPI_23_orchestration_enterprise",
            "factory": "agents.agent_FASTAPI_23_orchestration_enterprise.create_agent_23_enterprise"
        },
        {
            "name": "Agent 24 - Storage (CORRIGÉ)",
            "path": "agent_factory_implementation/agents/agent_STORAGE_24_enterprise_manager.py",
            "module": "agents.agent_STORAGE_24_enterprise_manager",
            "factory": "agents.agent_STORAGE_24_enterprise_manager.create_agent_24_storage"
        },
        {
            "name": "Agent 25 - Monitoring (CORRIGÉ)",
            "path": "agent_factory_implementation/agents/agent_MONITORING_25_production_enterprise.py",
            "module": "agents.agent_MONITORING_25_production_enterprise",
            "factory": "agents.agent_MONITORING_25_production_enterprise.create_agent_25_monitoring"
        }
    ]
    
    results = {}
    
    for agent in agents_config:
        print(f"\n🎯 TEST: {agent['name']}")
        print("-" * 50)
        
        # Test 1: Compilation
        compilation_ok = test_agent_compilation(agent['path'], agent['name'])
        
        # Test 2: Import
        import_ok = test_agent_import(agent['module'], agent['name']) if compilation_ok else False
        
        # Test 3: Création
        creation_ok = test_agent_creation(agent['factory'], agent['name']) if import_ok else False
        
        # Test 4: Exécution
        execution_ok = await test_agent_execution(agent['factory'], agent['name']) if creation_ok else False
        
        # Résultat global
        all_ok = compilation_ok and import_ok and creation_ok and execution_ok
        results[agent['name']] = {
            "compilation": compilation_ok,
            "import": import_ok,
            "creation": creation_ok,
            "execution": execution_ok,
            "global": all_ok
        }
    
    # Rapport final
    print("\n" + "=" * 60)
    print("📊 RAPPORT FINAL DES TESTS")
    print("=" * 60)
    
    agents_ok = 0
    total_agents = len(agents_config)
    
    for agent_name, tests in results.items():
        status = "✅ FONCTIONNEL" if tests["global"] else "❌ DÉFAILLANT"
        print(f"{status} - {agent_name}")
        
        if tests["global"]:
            agents_ok += 1
            print("  Compilation: ✅")
            print("  Import: ✅")
            print("  Création: ✅")
            print("  Exécution: ✅")
        else:
            print(f"  Compilation: {'✅' if tests['compilation'] else '❌'}")
            print(f"  Import: {'✅' if tests['import'] else '❌'}")
            print(f"  Création: {'✅' if tests['creation'] else '❌'}")
            print(f"  Exécution: {'✅' if tests['execution'] else '❌'}")
    
    print(f"\n🎯 RÉSULTAT GLOBAL: {agents_ok}/{total_agents} agents fonctionnels")
    
    if agents_ok == total_agents:
        print("🎉 SUCCÈS COMPLET! Tous les agents enterprise sont fonctionnels")
        verdict = "SUCCÈS"
    elif agents_ok > 0:
        print("⚠️ SUCCÈS PARTIEL - Certains agents nécessitent encore des corrections")
        verdict = "PARTIEL"
    else:
        print("🚨 ÉCHEC COMPLET - Aucun agent fonctionnel")
        verdict = "ÉCHEC"
    
    return verdict

if __name__ == "__main__":
    start_time = time.time()
    print("🧪 Lancement des tests agents enterprise...")
    
    try:
        verdict = asyncio.run(main())
        execution_time = time.time() - start_time
        
        print(f"\n⏱️ Tests terminés en {execution_time:.2f} secondes")
        print(f"🏆 VERDICT: {verdict}!")
        
    except Exception as e:
        print(f"\n💥 ERREUR CRITIQUE: {e}")
        print("🚨 VERDICT: ERREUR SYSTÈME!") 



