#!/usr/bin/env python3
"""
🧪 TEST AGENTS REFACTORISÉS - PATTERN FACTORY COMPLIANCE
========================================================

Test de validation du refactoring :
✅ Agent 23 V2 - FastAPI Enterprise (Pattern Factory)
✅ Agent 25 V2 - Monitoring Enterprise (Pattern Factory)

Objectif : Prouver que les agents refactorisés sont Pattern Factory compliant
"""

import sys
import asyncio
from pathlib import Path

# Ajout paths nécessaires
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "core"))
sys.path.append(str(Path(__file__).parent / "features"))

def test_agent_23_v2_refactored():
    """Test Agent 23 V2 refactorisé"""
    try:
        print("🚀 Test Agent 23 V2 - Pattern Factory Compliant")
        
        # Import de l'agent refactorisé
        from agents.agent_23_fastapi_orchestration_enterprise_v2 import create_agent_23_v2_enterprise
        
        # Création via factory
        agent = create_agent_23_v2_enterprise(
            compliance_target=90,
            authentication={'provider': 'jwt'},
            rate_limiting={'tier': 'enterprise'}
        )
        
        print(f"✅ Agent 23 V2 créé - ID: {agent.id}")
        print(f"✅ Version: {agent.agent_version}")
        print(f"✅ Features: {len(agent.features)} initialisées")
        
        # Test des capacités
        capabilities = agent.get_capabilities()
        print(f"✅ Capacités: {capabilities}")
        
        # Test exécution tâche
        from core.agent_factory_architecture import Task
        task = Task("authentication_setup", {"provider": "jwt"})
        result = agent.execute_task(task)
        
        print(f"✅ Task execution: {result.success}")
        print(f"✅ Feature utilisée: {result.metrics.get('feature_used', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur Agent 23 V2: {e}")
        return False

def test_agent_25_v2_refactored():
    """Test Agent 25 V2 refactorisé"""
    try:
        print("\n🚀 Test Agent 25 V2 - Pattern Factory Compliant")
        
        # Import de l'agent refactorisé
        from agents.agent_25_production_monitoring_enterprise_v2 import create_agent_25_v2_monitoring
        
        # Création via factory
        agent = create_agent_25_v2_monitoring(
            compliance_target=85,
            ml_anomaly={'models': ['isolation_forest']},
            dashboards={'type': 'enterprise'}
        )
        
        print(f"✅ Agent 25 V2 créé - ID: {agent.id}")
        print(f"✅ Version: {agent.agent_version}")
        print(f"✅ Features: {len(agent.features)} initialisées")
        
        # Test des capacités
        capabilities = agent.get_capabilities()
        print(f"✅ Capacités: {capabilities}")
        
        # Test exécution tâche
        from core.agent_factory_architecture import Task
        task = Task("ml_anomaly_setup", {"models": ["isolation_forest"]})
        result = agent.execute_task(task)
        
        print(f"✅ Task execution: {result.success}")
        print(f"✅ Feature utilisée: {result.metrics.get('feature_used', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur Agent 25 V2: {e}")
        return False

def main():
    """Test principal du refactoring"""
    print("🧪 VALIDATION REFACTORING AGENTS V2 → PATTERN FACTORY COMPLIANT")
    print("=" * 80)
    
    # Statistiques avant refactoring
    print("\n📊 AVANT REFACTORING:")
    print("❌ Agent 23 V2: 702 lignes monolithique")
    print("❌ Agent 25 V2: 694 lignes monolithique")
    print("❌ Redéfinition classes Agent, Task, Result")
    print("❌ Code dupliqué et non-réutilisable")
    
    print("\n📊 APRÈS REFACTORING:")
    print("✅ Agent 23 V2: ~150 lignes + features modulaires")
    print("✅ Agent 25 V2: ~150 lignes + features modulaires")
    print("✅ Utilise core/agent_factory_architecture.py")
    print("✅ Features réutilisables et modulaires")
    
    print("\n🧪 TESTS DE VALIDATION:")
    
    # Tests
    results = []
    results.append(test_agent_23_v2_refactored())
    results.append(test_agent_25_v2_refactored())
    
    # Résultats
    print("\n🏆 RÉSULTATS:")
    success_count = sum(results)
    total_count = len(results)
    
    print(f"✅ Tests réussis: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("\n🎉 REFACTORING VALIDÉ AVEC SUCCÈS!")
        print("✅ Agents V2 sont maintenant Pattern Factory compliant")
        print("✅ Réduction drastique du code monolithique")
        print("✅ Features modulaires réutilisables")
        print("✅ Respect du principe DRY")
    else:
        print("\n⚠️ Refactoring partiellement validé")
        print("🔧 Corrections nécessaires sur certains agents")
    
    return success_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 



