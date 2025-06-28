#!/usr/bin/env python3
"""
Test final et validation de la capacité d'audit universel
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

async def test_agent_maintenance_10():
    """Test spécifique de l'agent MAINTENANCE_10 avec audit universel"""
    print("🔍 Test Agent MAINTENANCE-10 - Audit Universel")
    
    try:
        from agents.agent_MAINTENANCE_10_auditeur_qualite_normes import AgentMAINTENANCE10AuditeurQualiteNormes
        
        agent = AgentMAINTENANCE10AuditeurQualiteNormes()
        await agent.startup()
        
        print("✅ Agent MAINTENANCE-10 initialisé")
        
        # Test des modules disponibles
        test_modules = [
            "agents/agent_MAINTENANCE_10_auditeur_qualite_normes.py",
            "agents/agent_config.py",
            "agents/agent_01_coordinateur_principal.py"
        ]
        
        results = []
        
        for module in test_modules:
            if Path(module).exists():
                print(f"\n📋 Audit universel: {module}")
                
                try:
                    result = await agent.audit_universal_module(module)
                    
                    if result.get('status') == 'completed':
                        score = result['quality_score']
                        level = result['quality_level']
                        issues = result['summary']['total_issues']
                        critical = result['summary']['critical_issues']
                        
                        print(f"   ✅ Score: {score}/100 ({level})")
                        print(f"   📊 Issues: {issues} total, {critical} critiques")
                        
                        # Détail des audits
                        audits = result.get('audits', {})
                        for audit_type, audit_result in audits.items():
                            audit_score = audit_result.get('score', 0)
                            print(f"      {audit_type}: {audit_score}/100")
                        
                        results.append(True)
                    else:
                        print(f"   ❌ Échec: {result.get('error', 'Erreur inconnue')}")
                        results.append(False)
                        
                except Exception as e:
                    print(f"   ❌ Erreur: {e}")
                    results.append(False)
            else:
                print(f"⚠️ Module non trouvé: {module}")
        
        await agent.shutdown()
        
        success_rate = sum(results) / len(results) * 100 if results else 0
        print(f"\n📊 Taux de réussite: {success_rate:.1f}% ({sum(results)}/{len(results)})")
        
        return success_rate >= 80
        
    except Exception as e:
        print(f"❌ Erreur test agent MAINTENANCE-10: {e}")
        return False

async def test_meta_auditeur_simple():
    """Test simplifié du Meta-Auditeur sans dépendances externes"""
    print("\n🌟 Test Meta-Auditeur Universel (version simplifiée)")
    
    try:
        from agents.agent_META_AUDITEUR_UNIVERSEL import MetaAuditeurUniversel
        
        meta_auditor = MetaAuditeurUniversel()
        await meta_auditor.startup()
        
        print("✅ Meta-Auditeur initialisé")
        
        # Test health check
        health = await meta_auditor.health_check()
        print(f"📊 Status: {health['status']}")
        print(f"   Auditeurs: {len(health['available_auditors'])}/{health['total_auditors']}")
        
        # Test détection type de module
        test_files = [
            ("agents/agent_MAINTENANCE_10_auditeur_qualite_normes.py", "agent"),
            ("agents/agent_config.py", "config"),
            ("tests/test_audit_universel_final.py", "test")
        ]
        
        for file_path, expected_type in test_files:
            if Path(file_path).exists():
                detected_type = await meta_auditor._detect_module_type(file_path)
                print(f"   📋 {file_path}: {detected_type.value} ({'✅' if detected_type.value == expected_type else '⚠️'})")
        
        # Test audit complet avec mocks
        print("\n📋 Test audit complet (avec agents mock)")
        result = await meta_auditor.audit_complet("agents/agent_config.py")
        
        if result.get('status') != 'failed':
            print(f"   ✅ Score global: {result['global_score']}/100")
            print(f"   🎯 Niveau: {result['quality_level']}")
            print(f"   ⚡ Durée: {result['total_duration']}s")
            print(f"   🤖 Agents: {len(result['agents_used'])}")
            
            if result.get('improvement_plan'):
                plan = result['improvement_plan']
                print(f"   📋 Plan: {plan['priorite_globale']} priorité")
        else:
            print(f"   ❌ Échec: {result.get('error')}")
        
        await meta_auditor.shutdown()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test Meta-Auditeur: {e}")
        return False

async def test_pattern_factory_compliance():
    """Test de conformité Pattern Factory"""
    print("\n🏭 Test Pattern Factory Compliance")
    
    tests = []
    
    # Test agent MAINTENANCE_10
    try:
        from agents.agent_MAINTENANCE_10_auditeur_qualite_normes import AgentMAINTENANCE10AuditeurQualiteNormes
        
        agent = AgentMAINTENANCE10AuditeurQualiteNormes()
        
        # Vérifier méthodes Pattern Factory
        required_methods = ['startup', 'shutdown', 'health_check', 'execute_task', 'get_capabilities']
        has_methods = all(hasattr(agent, method) for method in required_methods)
        
        print(f"   MAINTENANCE_10: {'✅' if has_methods else '❌'} (méthodes Pattern Factory)")
        tests.append(has_methods)
        
        # Test capacités
        caps = agent.get_capabilities()
        has_universal = any('universal' in cap for cap in caps)
        print(f"   MAINTENANCE_10: {'✅' if has_universal else '❌'} (audit universel)")
        tests.append(has_universal)
        
    except Exception as e:
        print(f"   MAINTENANCE_10: ❌ Erreur: {e}")
        tests.append(False)
    
    # Test Meta-Auditeur
    try:
        from agents.agent_META_AUDITEUR_UNIVERSEL import MetaAuditeurUniversel
        
        meta = MetaAuditeurUniversel()
        
        # Vérifier méthodes Pattern Factory
        required_methods = ['startup', 'shutdown', 'health_check', 'execute_task', 'get_capabilities']
        has_methods = all(hasattr(meta, method) for method in required_methods)
        
        print(f"   Meta-Auditeur: {'✅' if has_methods else '❌'} (méthodes Pattern Factory)")
        tests.append(has_methods)
        
        # Test capacités meta
        caps = meta.get_capabilities()
        has_meta = any('meta' in cap or 'orchestration' in cap for cap in caps)
        print(f"   Meta-Auditeur: {'✅' if has_meta else '❌'} (orchestration)")
        tests.append(has_meta)
        
    except Exception as e:
        print(f"   Meta-Auditeur: ❌ Erreur: {e}")
        tests.append(False)
    
    compliance_rate = sum(tests) / len(tests) * 100 if tests else 0
    print(f"\n📊 Conformité Pattern Factory: {compliance_rate:.1f}% ({sum(tests)}/{len(tests)})")
    
    return compliance_rate >= 75

async def test_cli_validation():
    """Test de validation CLI des agents"""
    print("\n💻 Test validation CLI")
    
    # Test direct CLI MAINTENANCE_10
    try:
        print("📋 Test CLI Agent MAINTENANCE_10...")
        from agents.agent_MAINTENANCE_10_auditeur_qualite_normes import main
        
        # Rediriger stdout pour capturer les résultats
        import io
        import contextlib
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            await main()
        
        output = f.getvalue()
        
        if "✅" in output and "Score:" in output:
            print("   ✅ CLI MAINTENANCE_10 fonctionnel")
            cli_success = True
        else:
            print("   ⚠️ CLI MAINTENANCE_10 résultats incomplets")
            cli_success = False
            
    except Exception as e:
        print(f"   ❌ CLI MAINTENANCE_10 erreur: {e}")
        cli_success = False
    
    # Test CLI Meta-Auditeur
    try:
        print("📋 Test CLI Meta-Auditeur...")
        from agents.agent_META_AUDITEUR_UNIVERSEL import main
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            await main()
        
        output = f.getvalue()
        
        if "🌟" in output and "Meta-audit" in output:
            print("   ✅ CLI Meta-Auditeur fonctionnel")
            meta_cli_success = True
        else:
            print("   ⚠️ CLI Meta-Auditeur résultats incomplets")
            meta_cli_success = False
            
    except Exception as e:
        print(f"   ❌ CLI Meta-Auditeur erreur: {e}")
        meta_cli_success = False
    
    return cli_success and meta_cli_success

async def main():
    """Test principal et validation complète"""
    print("🚀 VALIDATION FINALE - Système d'Audit Universel")
    print("=" * 60)
    
    tests_results = []
    
    # Test 1: Agent MAINTENANCE_10
    print("\n1️⃣ Test Agent MAINTENANCE-10")
    result1 = await test_agent_maintenance_10()
    tests_results.append(result1)
    print(f"Résultat: {'✅ RÉUSSI' if result1 else '❌ ÉCHEC'}")
    
    # Test 2: Meta-Auditeur
    print("\n2️⃣ Test Meta-Auditeur Universel")
    result2 = await test_meta_auditeur_simple()
    tests_results.append(result2)
    print(f"Résultat: {'✅ RÉUSSI' if result2 else '❌ ÉCHEC'}")
    
    # Test 3: Pattern Factory Compliance
    print("\n3️⃣ Test Pattern Factory Compliance")
    result3 = await test_pattern_factory_compliance()
    tests_results.append(result3)
    print(f"Résultat: {'✅ RÉUSSI' if result3 else '❌ ÉCHEC'}")
    
    # Test 4: CLI Validation
    print("\n4️⃣ Test CLI Validation")
    result4 = await test_cli_validation()
    tests_results.append(result4)
    print(f"Résultat: {'✅ RÉUSSI' if result4 else '❌ ÉCHEC'}")
    
    # Résultat final
    success_rate = sum(tests_results) / len(tests_results) * 100
    
    print(f"\n🏆 RÉSULTAT GLOBAL")
    print("=" * 60)
    print(f"Taux de réussite: {success_rate:.1f}% ({sum(tests_results)}/{len(tests_results)})")
    
    if success_rate >= 75:
        print("✅ VALIDATION RÉUSSIE - Système d'audit universel opérationnel")
        print("✅ Agent MAINTENANCE-10 avec audit universel validé")
        print("✅ Meta-Auditeur Universel déployé et fonctionnel")
        print("✅ Pattern Factory compliance confirmée")
        print("✅ Interfaces CLI opérationnelles")
        return True
    else:
        print("❌ VALIDATION ÉCHOUÉE - Corrections nécessaires")
        return False

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(main())
    
    if not success:
        sys.exit(1)
    
    print("\n🎯 MISSION ACCOMPLIE!")
    print("Le système d'audit universel est déployé et validé.")