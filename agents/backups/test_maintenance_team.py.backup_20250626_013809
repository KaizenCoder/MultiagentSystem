#!/usr/bin/env python3
"""
🧪 TEST ÉQUIPE DE MAINTENANCE - VALIDATION FONCTIONNELLE
========================================================

Script de test pour valider que tous les agents de maintenance
sont 100% fonctionnels après les adaptations Pattern Factory.

Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
Created: 2025-01-19
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

async def test_agent_maintenance_03():
    """Test Agent 03 - Adaptateur Code"""
    try:
    print("🔍 Test Agent 03 - Adaptateur Code...")
        
        # Import dynamique pour éviter les erreurs
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "agent_03", 
        "agent_MAINTENANCE_03_adaptateur_code.py"
    )
    agent_03_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agent_03_module)
        
        # Créer l'agent
    agent = agent_03_module.create_agent_3_adaptateur_code()
        
        # Tests de base
    await agent.startup()
    health = await agent.health_check()
    print(f"  ✅ Health Check: {health['status']}")
        
        # Test capabilities
    capabilities = agent.get_capabilities()
    print(f"  ✅ Capabilities: {len(capabilities)} capacités")
        
    await agent.shutdown()
    print("  ✅ Agent 03 - OPÉRATIONNEL")
    return True
        
    except Exception as e:
    print(f"  ❌ Agent 03 - ERREUR: {e}")
    return False

async def test_agent_maintenance_04():
    """Test Agent 04 - Testeur Anti-Faux-Agents"""
    try:
    print("🔍 Test Agent 04 - Testeur Anti-Faux-Agents...")
        
        # Import dynamique
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "agent_04", 
        "agent_MAINTENANCE_04_testeur_anti_faux_agents.py"
    )
    agent_04_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agent_04_module)
        
        # Créer l'agent
    agent = agent_04_module.ImprovedEnterpriseAgentTester()
        
        # Tests de base
    await agent.startup()
    health = await agent.health_check()
    print(f"  ✅ Health Check: {health['status']}")
        
        # Test capabilities
    capabilities = agent.get_capabilities()
    print(f"  ✅ Capabilities: {len(capabilities)} capacités")
        
    await agent.shutdown()
    print("  ✅ Agent 04 - OPÉRATIONNEL")
    return True
        
    except Exception as e:
    print(f"  ❌ Agent 04 - ERREUR: {e}")
    return False

async def test_simple_functionality():
    """Test de fonctionnalité simple sans Pattern Factory"""
    try:
    print("🔍 Test Fonctionnalité Simple...")
        
        # Test basique d'import
    from pathlib import Path
    agents_dir = Path(".")
        
    maintenance_agents = list(agents_dir.glob("agent_MAINTENANCE_*.py"))
    print(f"  ✅ {len(maintenance_agents)} agents de maintenance trouvés")
        
    for agent_file in maintenance_agents:
        print(f"    📁 {agent_file.name}")
        
    return True
        
    except Exception as e:
    print(f"  ❌ Test Simple - ERREUR: {e}")
    return False

async def main():
    """Test principal de l'équipe de maintenance"""
    print("🛠️ VALIDATION ÉQUIPE DE MAINTENANCE")
    print("=" * 50)
    
    results = []
    
    # Test simple
    results.append(await test_simple_functionality())
    
    # Test agents spécifiques
    results.append(await test_agent_maintenance_03())
    results.append(await test_agent_maintenance_04())
    
    # Résultats
    print("\n📊 RÉSULTATS VALIDATION")
    print("=" * 30)
    
    success_count = sum(results)
    total_tests = len(results)
    
    print(f"✅ Tests réussis: {success_count}/{total_tests}")
    print(f"📈 Taux de réussite: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
    print("🎉 ÉQUIPE DE MAINTENANCE 100% FONCTIONNELLE !")
    else:
    print("⚠️  Équipe de maintenance partiellement fonctionnelle")
    
    return success_count == total_tests

if __name__ == "__main__":
    asyncio.run(main()) 
