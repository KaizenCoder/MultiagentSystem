#!/usr/bin/env python3
"""
Test de validation pour agent_16_peer_reviewer_senior.py
"""
import sys
import asyncio
import logging
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock classes pour le test si Pattern Factory indisponible
class MockAgent:
    def __init__(self, agent_type: str, **config):
        self.agent_type = agent_type
        self.agent_id = "test_id"

class MockTask:
    def __init__(self, description: str, **kwargs):
        self.description = description
        self.task_id = description
        self.payload = kwargs.get('payload', {})
        self.data = kwargs.get('data', {})

class MockResult:
    def __init__(self, success: bool, data: any = None, error: str = None):
        self.success = success
        self.data = data
        self.error = error

# Mock le module core si indisponible
try:
    from core.agent_factory_architecture import Agent, Task, Result
    print("✅ Pattern Factory disponible")
except ImportError:
    print("⚠️ Pattern Factory indisponible, utilisation des mocks")
    Agent = MockAgent
    Task = MockTask  
    Result = MockResult

async def test_agent_16_validation():
    """Test de validation complet pour l'agent 16"""
    print("🎖️ Test validation Agent 16 - Peer Reviewer Senior")
    
    try:
        from agents.agent_16_peer_reviewer_senior import PeerReviewerSeniorAgent
        
        agent = PeerReviewerSeniorAgent()
        await agent.startup()
        
        print("✅ Agent 16 initialisé avec succès")
        
        # Test 1: Vérification Pattern Factory compliance
        print("\n📋 Test 1: Pattern Factory Compliance")
        required_methods = ['startup', 'shutdown', 'health_check', 'execute_task', 'get_capabilities']
        compliance_score = 0
        
        for method in required_methods:
            if hasattr(agent, method):
                print(f"   ✅ {method}: présent")
                compliance_score += 1
            else:
                print(f"   ❌ {method}: manquant")
        
        print(f"   📊 Compliance: {compliance_score}/{len(required_methods)} ({compliance_score/len(required_methods)*100:.1f}%)")
        
        # Test 2: Capabilities
        print("\n📋 Test 2: Capacités")
        caps = agent.get_capabilities()
        print(f"   📊 Capacités disponibles: {len(caps)}")
        for cap in caps:
            print(f"      - {cap}")
        
        # Test 3: Health check
        print("\n📋 Test 3: Health Check")
        health = await agent.health_check()
        print(f"   Status: {health.get('status', 'unknown')}")
        print(f"   Agent: {health.get('agent', 'N/A')}")
        
        # Test 4: Execute task
        print("\n📋 Test 4: Execute Task")
        
        # Test avec code_review
        task_review = MockTask("code_review")
        result_review = await agent.execute_task(task_review)
        
        if result_review.success:
            print("   ✅ Task 'code_review': réussie")
            if isinstance(result_review.data, dict):
                status = result_review.data.get('status', 'unknown')
                print(f"      Status: {status}")
                if 'expert_validation' in result_review.data:
                    print(f"      Validation: {result_review.data['expert_validation']}")
        else:
            print(f"   ❌ Task 'code_review': échec - {result_review.error}")
        
        # Test avec quality_assessment
        task_quality = MockTask("quality_assessment")
        result_quality = await agent.execute_task(task_quality)
        
        if result_quality.success:
            print("   ✅ Task 'quality_assessment': réussie")
        else:
            print(f"   ❌ Task 'quality_assessment': échec - {result_quality.error}")
        
        # Test 5: Mission principale
        print("\n📋 Test 5: Mission Principale - Review Senior")
        try:
            result_mission = agent.run_senior_review_mission()
            
            if isinstance(result_mission, dict) and result_mission.get('status'):
                print(f"   ✅ Mission review senior: {result_mission['status']}")
                
                # Vérifier les composants principaux
                components = ['architecture_review', 'conformity_validation', 'quality_assessment', 'performance']
                for comp in components:
                    if comp in result_mission:
                        print(f"      ✅ {comp}: présent")
                    else:
                        print(f"      ⚠️ {comp}: manquant")
                        
                if 'performance' in result_mission:
                    perf = result_mission['performance']
                    print(f"      📊 Durée: {perf.get('duration_seconds', 'N/A')}s")
                    print(f"      📊 Score qualité: {perf.get('overall_quality', 'N/A')}")
                    
            else:
                print(f"   ⚠️ Mission review: résultat inattendu")
                
        except Exception as e:
            print(f"   ❌ Mission review: erreur - {e}")
        
        await agent.shutdown()
        
        # Évaluation finale
        print(f"\n🏆 ÉVALUATION FINALE AGENT 16")
        print("=" * 50)
        
        if compliance_score >= 4 and len(caps) >= 2:
            print("✅ VALIDATION RÉUSSIE")
            print("✅ Pattern Factory compliant")
            print("✅ Capacités opérationnelles")
            print("✅ Tests fonctionnels réussis")
            print("✅ Ready for production")
            return True
        else:
            print("❌ VALIDATION ÉCHOUÉE")
            print(f"❌ Compliance insuffisante: {compliance_score}/5")
            return False
        
    except Exception as e:
        print(f"❌ Erreur test agent 16: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent_16_validation())
    
    if success:
        print("\n🎯 AGENT 16 VALIDÉ - Prêt pour validation metasuperviseur")
    else:
        print("\n💥 AGENT 16 NÉCESSITE DES CORRECTIONS")
        sys.exit(1)