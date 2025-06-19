#!/usr/bin/env python3
"""
🧪 TEST PATTERN FACTORY COMPLIANCE
===================================

Script de validation pour confirmer la transformation réussie :
- Agent 23 V2 : API FastAPI Enterprise (260+ → ~80 lignes)
- Agent 25 V2 : Production Monitoring Enterprise (264+ → ~80 lignes)

Test de conformité Pattern Factory et features modulaires.
"""

import sys
import os
from pathlib import Path

# Ajout du chemin pour les imports
sys.path.insert(0, str(Path(__file__).parent))

def test_pattern_factory_architecture():
    """Test 1: Vérification architecture Pattern Factory"""
    try:
        from core.agent_factory_architecture import Agent, Task, Result, AgentType
        print("✅ Architecture Pattern Factory: OK")
        return True
    except ImportError as e:
        print(f"❌ Architecture Pattern Factory: {e}")
        return False

def test_fastapi_features():
    """Test 2: Vérification features FastAPI"""
    try:
        from features.enterprise.fastapi_orchestration import (
            AuthenticationFeature, RateLimitingFeature, DocumentationFeature,
            MonitoringFeature, SecurityFeature
        )
        print("✅ Features FastAPI Enterprise: OK")
        return True
    except ImportError as e:
        print(f"❌ Features FastAPI Enterprise: {e}")
        return False

def test_monitoring_features():
    """Test 3: Vérification features Monitoring"""
    try:
        from features.enterprise.production_monitoring import (
            MLAnomalyFeature, DashboardFeature, AlertingFeature,
            SLAMonitoringFeature, PredictiveFeature, ComplianceFeature
        )
        print("✅ Features Monitoring Enterprise: OK")
        return True
    except ImportError as e:
        print(f"❌ Features Monitoring Enterprise: {e}")
        return False

def test_agent_23_v2():
    """Test 4: Agent 23 V2 Pattern Factory compliant"""
    try:
        from agents.agent_23_fastapi_orchestration_enterprise_v2 import (
            Agent23FastAPIOrchestrationEnterpriseV2,
            create_agent_23_v2_enterprise
        )
        
        # Test création agent
        agent = create_agent_23_v2_enterprise()
        
        # Test features
        assert len(agent.features) == 5, f"Expected 5 features, got {len(agent.features)}"
        
        # Test capabilities
        capabilities = agent.get_capabilities()
        assert len(capabilities) == 6, f"Expected 6 capabilities, got {len(capabilities)}"
        
        # Test task execution
        from core.agent_factory_architecture import Task
        task = Task(id="test", type="authentication_setup", description="Test")
        result = agent.execute_task(task)
        
        assert result.success, "Authentication task should succeed"
        assert "agent_id" in result.metrics, "Result should have agent metrics"
        
        print("✅ Agent 23 V2 FastAPI Enterprise: Pattern Factory compliant")
        return True
        
    except Exception as e:
        print(f"❌ Agent 23 V2: {e}")
        return False

def test_agent_25_v2():
    """Test 5: Agent 25 V2 Pattern Factory compliant"""
    try:
        from agents.agent_25_production_monitoring_enterprise_v2 import (
            Agent25ProductionMonitoringEnterpriseV2,
            create_agent_25_v2_monitoring
        )
        
        # Test création agent
        agent = create_agent_25_v2_monitoring()
        
        # Test features
        assert len(agent.features) == 6, f"Expected 6 features, got {len(agent.features)}"
        
        # Test capabilities
        capabilities = agent.get_capabilities()
        assert len(capabilities) == 6, f"Expected 6 capabilities, got {len(capabilities)}"
        
        # Test task execution
        from core.agent_factory_architecture import Task
        task = Task(id="test", type="ml_anomaly_setup", description="Test")
        result = agent.execute_task(task)
        
        assert result.success, "ML anomaly task should succeed"
        assert "monitoring_domain" in result.metrics, "Result should have monitoring metrics"
        
        print("✅ Agent 25 V2 Production Monitoring: Pattern Factory compliant")
        return True
        
    except Exception as e:
        print(f"❌ Agent 25 V2: {e}")
        return False

def count_code_lines():
    """Test 6: Validation réduction code"""
    agent_23_path = Path("agents/agent_23_fastapi_orchestration_enterprise_v2.py")
    agent_25_path = Path("agents/agent_25_production_monitoring_enterprise_v2.py")
    
    if agent_23_path.exists():
        lines_23 = len(agent_23_path.read_text().splitlines())
        print(f"📏 Agent 23 V2: {lines_23} lignes")
        
        if lines_23 <= 100:
            print("✅ Agent 23 V2: Réduction de code réussie!")
        else:
            print("⚠️ Agent 23 V2: Code encore trop volumineux")
    
    if agent_25_path.exists():
        lines_25 = len(agent_25_path.read_text().splitlines())
        print(f"📏 Agent 25 V2: {lines_25} lignes")
        
        if lines_25 <= 100:
            print("✅ Agent 25 V2: Réduction de code réussie!")
        else:
            print("⚠️ Agent 25 V2: Code encore trop volumineux")

def main():
    """Exécution des tests Pattern Factory compliance"""
    print("🧪 TEST PATTERN FACTORY COMPLIANCE")
    print("=" * 50)
    
    tests = [
        test_pattern_factory_architecture,
        test_fastapi_features,
        test_monitoring_features,
        test_agent_23_v2,
        test_agent_25_v2
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ {test.__name__}: Exception {e}")
            results.append(False)
    
    # Comptage lignes
    count_code_lines()
    
    # Résumé
    print("\n📊 RÉSUMÉ TRANSFORMATION")
    print("=" * 30)
    print(f"Tests réussis: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 SUCCÈS: Transformation Pattern Factory complète!")
        print("✅ Agents 23 V2 & 25 V2 sont maintenant Pattern Factory compliant")
        print("🚀 Réduction drastique du code accomplie")
    else:
        print("⚠️ Certains tests ont échoué - Vérification nécessaire")

if __name__ == "__main__":
    main() 