#!/usr/bin/env python3
"""
Test direct Agent 05 Peer-Reviewer Enrichi
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le chemin pour les imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from agents.agent_MAINTENANCE_05_peer_reviewer_enrichi import create_agent_5_peer_reviewer_enrichi

async def test_correction_agent():
    """Test de correction d'un agent défaillant"""
    
    print("🔍 TEST CORRECTION AGENT DÉFAILLANT")
    print("=" * 50)
    
    # 1. Créer agent peer-reviewer
    print("\n1. Création Agent Peer-Reviewer...")
    peer_reviewer = create_agent_5_peer_reviewer_enrichi()
    await peer_reviewer.startup()
    
    print(f"✅ Agent créé : {peer_reviewer.agent_id}")
    print(f"✅ Capacités : {len(peer_reviewer.get_capabilities())}")
    
    # 2. Créer agent défaillant pour test
    print("\n2. Création agent défaillant pour test...")
    
    agent_defaillant_content = '''#!/usr/bin/env python3
"""Agent défaillant pour test"""

class AgentDefaillant:
    """Agent sans héritage Pattern Factory"""
    
    def __init__(self, config=None):
        self.config = config or {}
    
    async async def methode_erreur(self):
        """Méthode avec erreur syntaxe"""
        return True

if __name__ == "__main__":
    agent = AgentDefaillant()
    print("Agent défaillant")
'''
    
    agent_path = Path("agent_test_defaillant.py")
    agent_path.write_text(agent_defaillant_content, encoding='utf-8')
    print(f"✅ Agent défaillant créé : {agent_path}")
    
    # 3. Simuler résultats de test défaillants
    print("\n3. Simulation résultats de test défaillants...")
    
    test_results = {
        'global_scores': {'utilisation': 2.0, 'overall': 2.5},
        'tests_results': {
            'utilisation_reelle': {
                'status': 'FAILED',
                'tests_passed': 1,
                'tests_executed': 4,
                'details': {
                    'instantiation': {'status': 'FAILED', 'error': 'No Agent inheritance'},
                    'pattern_factory_methods': {'status': 'FAILED', 'error': 'Missing methods'},
                    'basic_functionality': {'status': 'SUCCESS'},
                    'error_handling': {'status': 'FAILED', 'error': 'Syntax error'}
                }
            }
        }
    }
    
    print("✅ Résultats défaillants simulés")
    
    # 4. Appliquer corrections
    print("\n4. Application des corrections...")
    
    correction_results = await peer_reviewer.corriger_defaillances_utilisation_complete(
        str(agent_path), 
        test_results
    )
    
    print(f"✅ Statut correction : {correction_results['status']}")
    
    if correction_results['status'] == 'SUCCESS':
        print(f"✅ Corrections appliquées : {correction_results['corrections_count']}")
        print(f"✅ Message : {correction_results['message']}")
        
        print("\n📋 Détail des corrections :")
        for i, correction in enumerate(correction_results['corrections_applied'], 1):
            print(f"   {i}. {correction}")
    
    # 5. Vérifier agent corrigé
    print("\n5. Vérification agent corrigé...")
    
    if agent_path.exists():
        corrected_content = agent_path.read_text(encoding='utf-8')
        
        verifications = {
            'Import Pattern Factory': 'from agent_factory_implementation' in corrected_content,
            'Héritage Agent': 'class AgentDefaillant(Agent)' in corrected_content,
            'Super init': 'super().__init__' in corrected_content,
            'Méthode startup': 'async def startup' in corrected_content,
            'Correction async async': 'async async def' not in corrected_content
        }
        
        print("✅ Vérifications :")
        corrections_ok = 0
        for check, result in verifications.items():
            status = "✅" if result else "❌"
            if result:
                corrections_ok += 1
            print(f"   {status} {check}")
        
        score = corrections_ok / len(verifications) * 100
        print(f"\n📊 Score correction : {corrections_ok}/{len(verifications)} ({score:.1f}%)")
    
    # 6. Génération certification
    print("\n6. Génération certification finale...")
    
    test_results_apres = {
        'global_scores': {'utilisation': 8.0, 'overall': 8.5},
        'tests_results': {
            'utilisation_reelle': {
                'status': 'SUCCESS',
                'tests_passed': 4,
                'tests_executed': 4
            }
        }
    }
    
    certification = await peer_reviewer.generer_certification_finale(
        str(agent_path),
        test_results,      # Avant
        test_results_apres # Après
    )
    
    print(f"✅ Certification : {certification['certification']}")
    print(f"✅ Grade : {certification['grade']}")
    print(f"✅ Amélioration : +{certification['amelioration']:.1f}%")
    
    # 7. Nettoyage
    print("\n7. Nettoyage...")
    
    try:
        if agent_path.exists():
            agent_path.unlink()
            print(f"✅ Fichier supprimé : {agent_path}")
        
        # Supprimer backups
        for backup in Path(".").glob("agent_test_defaillant.backup_*.py"):
            backup.unlink()
            print(f"✅ Backup supprimé : {backup}")
            
    except Exception as e:
        print(f"⚠️ Erreur nettoyage : {e}")
    
    await peer_reviewer.shutdown()
    
    # 8. Résumé
    print("\n8. RÉSUMÉ FINAL")
    print("-" * 30)
    
    if correction_results['status'] == 'SUCCESS' and score >= 80:
        print("🏆 SUCCÈS COMPLET")
        print("✅ Agent 05 Peer-Reviewer Enrichi OPÉRATIONNEL")
        print("✅ Corrections automatiques fonctionnelles")
        print("✅ Certification générée avec succès")
        print("🚀 Prêt pour utilisation en production")
    else:
        print("⚠️ Test partiellement réussi")
        print("🔧 Quelques ajustements peuvent être nécessaires")
    
    print("\n" + "=" * 50)
    print("🏁 FIN TEST CORRECTION AGENT")

if __name__ == "__main__":
    asyncio.run(test_correction_agent()) 




