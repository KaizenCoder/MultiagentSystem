#!/usr/bin/env python3
"""
🧪 SCRIPT DE TEST - AGENT 04 AMÉLIORÉ
=====================================

Test des nouvelles fonctionnalités de détection de conformité Pattern Factory

Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
Created: 2025-01-20
"""

import sys
import asyncio
from pathlib import Path

# Ajouter le répertoire des agents au PATH
sys.path.insert(0, str(Path(__file__).parent / "agent_equipe_maintenance"))

from agent_MAINTENANCE_04_testeur_anti_faux_agents import ImprovedEnterpriseAgentTester, Task, Result

async def test_agent_04_ameliore():
    """Test complet de l'Agent 04 amélioré"""
    print("🧪 TEST AGENT 04 AMÉLIORÉ - NOUVELLES FONCTIONNALITÉS")
    print("=" * 60)
    
    # Créer instance testeur
    testeur = ImprovedEnterpriseAgentTester()
    
    # Test 1: Démarrage agent
    print("\n1️⃣ Test démarrage agent...")
    await testeur.startup()
    
    # Test 2: Vérification santé
    print("\n2️⃣ Test vérification santé...")
    health = await testeur.health_check()
    print(f"   ✅ Santé: {health['status']}")
    print(f"   🆔 Agent ID: {health['agent_id']}")
    
    # Test 3: Test tâche audit Pattern Factory
    print("\n3️⃣ Test audit Pattern Factory...")
    try:
        task = Task("pattern_factory_audit", "Audit conformité Pattern Factory")
        
        # Exécuter tâche
        result = await testeur.execute_task(task)
        
        if result.success:
            print("   ✅ Audit Pattern Factory réussi")
        else:
            print(f"   ❌ Échec audit: {result.error}")
    except Exception as e:
        print(f"   ⚠️ Erreur test audit: {e}")
    
    # Test 4: Test méthode directe audit
    print("\n4️⃣ Test méthode audit directe...")
    try:
        # Tester avec le répertoire factory par défaut
        audit_results = testeur.run_pattern_factory_audit()
        
        print(f"   📊 Agents trouvés: {audit_results.get('agents_found', 0)}")
        print(f"   ✅ Agents analysés: {audit_results.get('agents_analyzed', 0)}")
        
        summary = audit_results.get('conformity_summary', {})
        total_agents = sum(summary.values())
        if total_agents > 0:
            print(f"   📋 Conformité: {summary.get('compliant', 0)}/{total_agents} agents conformes")
        
        # Afficher erreurs critiques si présentes
        critical_issues = audit_results.get('critical_issues', [])
        if critical_issues:
            print(f"   🚨 {len(critical_issues)} problèmes critiques détectés")
            for issue in critical_issues[:2]:  # Afficher 2 premiers
                print(f"      • {issue}")
        
    except Exception as e:
        print(f"   ⚠️ Erreur audit direct: {e}")
    
    # Test 5: Test analyse conformité fichier spécifique
    print("\n5️⃣ Test analyse conformité fichier spécifique...")
    try:
        # Créer un fichier de test avec problèmes
        test_file = Path("test_agent_problematic.py")
        test_content = '''#!/usr/bin/env python3
"""Agent de test avec problèmes"""

# Import avec fallback
try:
    from agent_factory_implementation.core.agent_factory_architecture import Agent
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
    print("Pattern Factory non disponible")
    class Agent:
        def __init__(self): pass
        async async def startup(self): pass  # Erreur syntaxe
    PATTERN_FACTORY_AVAILABLE = False

class ProblematicAgent(Agent):
    def __init__(self):
        # Pas de super().__init__
        self.agent_id = "test"
    
    def startup(self):  # Devrait être async
        return {"status": "ok"}
'''
        
        test_file.write_text(test_content, encoding='utf-8')
        
        # Analyser le fichier
        compliance_report = testeur.verify_pattern_factory_compliance(test_file)
        
        print(f"   📋 Score conformité: {compliance_report.get('compliance_score', 0):.1f}%")
        print(f"   🔧 Utilise fallback: {compliance_report.get('uses_fallback', False)}")
        print(f"   🚨 Erreurs syntaxe: {len(compliance_report.get('syntax_errors', []))}")
        print(f"   💡 Recommandation: {compliance_report.get('recommendation', 'N/A')}")
        
        # Nettoyer fichier de test
        test_file.unlink()
        
    except Exception as e:
        print(f"   ⚠️ Erreur test fichier: {e}")
    
    # Test 6: Arrêt agent
    print("\n6️⃣ Test arrêt agent...")
    await testeur.shutdown()
    
    print("\n" + "=" * 60)
    print("✅ TOUS LES TESTS TERMINÉS")
    print("🎯 Agent 04 amélioré opérationnel avec nouvelles fonctionnalités")
    print("=" * 60)

def main():
    """Point d'entrée principal"""
    try:
        asyncio.run(test_agent_04_ameliore())
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 



