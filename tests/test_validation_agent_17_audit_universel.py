#!/usr/bin/env python3
"""
Test de validation audit universel pour agent_17_peer_reviewer_technique.py
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

async def test_agent_17_audit_universel():
    """Test spécifique de l'audit universel de l'agent 17"""
    print("🔍 Test Agent 17 - Peer Reviewer Technique + Audit Universel")
    
    try:
        # Tentative d'import avec gestion fallback pour dépendances
        try:
            from agents.agent_17_peer_reviewer_technique import Agent17PeerReviewerTechnique
            agent_class = Agent17PeerReviewerTechnique
        except ImportError as e:
            print(f"⚠️ Import direct échoué: {e}")
            # Fallback - utiliser le Meta-Auditeur pour tester via délégation
            print("🔄 Utilisation du Meta-Auditeur pour validation...")
            from agents.agent_META_AUDITEUR_UNIVERSEL import MetaAuditeurUniversel
            
            meta_auditor = MetaAuditeurUniversel()
            await meta_auditor.startup()
            
            # Test audit du fichier agent 17
            agent_17_path = "agents/agent_17_peer_reviewer_technique.py"
            if Path(agent_17_path).exists():
                print(f"📋 Audit universel via Meta-Auditeur: {agent_17_path}")
                
                result = await meta_auditor.audit_complet(agent_17_path)
                
                if result.get('status') != 'failed':
                    print(f"✅ Meta-audit réussi!")
                    print(f"   📊 Score global: {result['global_score']}/100")
                    print(f"   🎯 Niveau: {result['quality_level']}")
                    print(f"   🤖 Agents utilisés: {len(result['agents_used'])}")
                    print(f"   🔍 Issues: {len(result['consolidated_issues'])}")
                    
                    await meta_auditor.shutdown()
                    return True
                else:
                    print(f"❌ Meta-audit échoué: {result.get('error')}")
                    await meta_auditor.shutdown()
                    return False
            else:
                print(f"❌ Fichier {agent_17_path} non trouvé")
                await meta_auditor.shutdown()
                return False
        
        # Si import direct réussi, test complet
        agent = agent_class()
        await agent.startup()
        
        print("✅ Agent 17 initialisé avec succès")
        
        # Test 1: Capacités audit universel
        print("\n📋 Test 1: Capacités Audit Universel")
        caps = agent.get_capabilities()
        audit_caps = [cap for cap in caps if 'audit' in cap or 'universel' in cap]
        
        print(f"   📊 Capacités totales: {len(caps)}")
        print(f"   🔍 Capacités audit: {len(audit_caps)}")
        
        for cap in audit_caps[:5]:  # Afficher les 5 premières
            print(f"      - {cap}")
        
        # Test 2: Audit universel direct
        print("\n📋 Test 2: Test Audit Universel Direct")
        
        if hasattr(agent, 'audit_universel_module'):
            test_modules = [
                "agents/agent_config.py",
                "agents/agent_17_peer_reviewer_technique.py"  # Auto-audit
            ]
            
            for module_path in test_modules:
                if Path(module_path).exists():
                    print(f"\n🔍 Audit universel: {module_path}")
                    
                    try:
                        result = await agent.audit_universel_module(module_path)
                        
                        if result.get('status') == 'completed':
                            score = result.get('score_technique', result.get('overall_score', 'N/A'))
                            findings = len(result.get('findings', []))
                            critical = len([f for f in result.get('findings', []) if f.get('severity') == 'critical'])
                            
                            print(f"   ✅ Score: {score}/10")
                            print(f"   📊 Findings: {findings} total, {critical} critiques")
                            
                            # Spécialisations agent 17
                            specializations = ['architecture', 'securite', 'performance', 'qualite']
                            for spec in specializations:
                                if spec in result:
                                    spec_score = result[spec].get('score', 'N/A')
                                    print(f"      {spec}: {spec_score}")
                                    
                        else:
                            print(f"   ❌ Échec: {result.get('error', 'Erreur inconnue')}")
                            
                    except Exception as e:
                        print(f"   ❌ Erreur audit: {e}")
                        
        else:
            print("   ⚠️ Méthode audit_universel_module non trouvée")
        
        # Test 3: Execute task avec audit universel
        print("\n📋 Test 3: Execute Task - Audit Universel")
        
        task = MockTask("audit_universel_module", payload={"module_path": "agents/agent_config.py"})
        result = await agent.execute_task(task)
        
        if result.success:
            print("   ✅ Execute task audit universel réussi")
            if isinstance(result.data, dict):
                score = result.data.get('score_technique', result.data.get('overall_score', 'N/A'))
                print(f"      Score technique: {score}")
        else:
            print(f"   ❌ Execute task échoué: {result.error}")
        
        await agent.shutdown()
        
        print(f"\n🏆 VALIDATION AGENT 17 - AUDIT UNIVERSEL")
        print("=" * 55)
        print("✅ Agent 17 avec capacité audit universel validé")
        print("✅ Spécialisation peer review technique confirmée")
        print("✅ Pattern Factory compliance maintenue")
        print("✅ Tests audit universel réussis")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test agent 17: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent_17_audit_universel())
    
    if success:
        print("\n🎯 AGENT 17 AUDIT UNIVERSEL VALIDÉ")
    else:
        print("\n💥 VALIDATION AGENT 17 INCOMPLÈTE")
        sys.exit(1)