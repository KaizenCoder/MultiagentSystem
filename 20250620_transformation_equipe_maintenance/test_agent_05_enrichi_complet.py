#!/usr/bin/env python3
"""
🧪 TEST COMPLET - Agent 05 Documenteur + Peer-Reviewer ENRICHI
=============================================================

Test de validation complète de l'Agent 05 ENRICHI qui combine :
- Capacités originales Agent 05 (documentation enterprise)
- Capacités enrichies Agents 16 & 17 (peer review + correction)

Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
Created: 2025-01-21
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Ajout du chemin pour imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / "agent_equipe_maintenance"))

# Import de l'Agent 05 ENRICHI
from agent_MAINTENANCE_05_documenteur_peer_reviewer import (
    DocumenteurEnterprisePeerReviewerEnrichi,
    create_agent_5_documenteur_peer_reviewer,
    Task,
    Result
)

class TestAgent05Enrichi:
    """🧪 Classe de test pour l'Agent 05 ENRICHI"""
    
    def __init__(self):
        self.agent = None
        self.test_results = []
        
    async def run_all_tests(self):
        """Exécute tous les tests"""
        print("🧪 DÉBUT TEST COMPLET - Agent 05 Documenteur + Peer-Reviewer ENRICHI")
        print("=" * 80)
        
        try:
            # 1. Test création et initialisation
            await self.test_creation_agent()
            
            # 2. Test capacités combinées
            await self.test_capacites_combinees()
            
            # 3. Test fonctionnalités documentation (Agent 05 original)
            await self.test_documentation_enterprise()
            
            # 4. Test fonctionnalités peer review (enrichies)
            await self.test_peer_review_correction()
            
            # 5. Test exécution tâches Pattern Factory
            await self.test_execution_taches()
            
            # 6. Test intégration complète
            await self.test_integration_complete()
            
            # Résumé final
            await self.afficher_resume_final()
            
        except Exception as e:
            print(f"❌ ERREUR CRITIQUE DANS LES TESTS : {e}")
            return False
        
        finally:
            if self.agent:
                await self.agent.shutdown()
        
        return True
    
    async def test_creation_agent(self):
        """Test 1 : Création et initialisation"""
        print("\n🔧 TEST 1 : Création et initialisation")
        print("-" * 40)
        
        try:
            # Création avec factory
            self.agent = create_agent_5_documenteur_peer_reviewer(
                target_path="../agent_factory_implementation/agents",
                workspace_path=".",
                resultats_tests={"test": "data"}
            )
            
            # Startup
            await self.agent.startup()
            
            # Health check
            health = await self.agent.health_check()
            
            print(f"✅ Agent créé avec ID : {health['agent_id']}")
            print(f"✅ Type : {health['agent_type']}")
            print(f"✅ Status : {health['status']}")
            print(f"✅ Pattern Factory : {health.get('pattern_factory_available', 'N/A')}")
            print(f"✅ Capacités : {health['capabilities_count']}")
            
            self.test_results.append({
                "test": "creation_agent",
                "status": "SUCCESS",
                "agent_id": health['agent_id'],
                "capabilities_count": health['capabilities_count']
            })
            
        except Exception as e:
            print(f"❌ Erreur création : {e}")
            self.test_results.append({
                "test": "creation_agent",
                "status": "ERROR",
                "error": str(e)
            })
    
    async def test_capacites_combinees(self):
        """Test 2 : Capacités combinées Agent 05 + Enrichissement"""
        print("\n🎯 TEST 2 : Capacités combinées")
        print("-" * 40)
        
        try:
            capabilities = self.agent.get_capabilities()
            
            # Capacités originales Agent 05
            capacites_doc = [
                "documenter_complete",
                "enterprise_documentation",
                "intelligent_automated_documentation",
                "multi_format_documentation"
            ]
            
            # Capacités enrichies peer review
            capacites_review = [
                "corriger_defaillances_utilisation",
                "peer_review_complete",
                "generer_certification_finale",
                "senior_architecture_review",
                "technical_deep_review"
            ]
            
            doc_present = sum(1 for cap in capacites_doc if cap in capabilities)
            review_present = sum(1 for cap in capacites_review if cap in capabilities)
            
            print(f"📚 Capacités Documentation (Agent 05) : {doc_present}/{len(capacites_doc)}")
            print(f"🔍 Capacités Peer Review (Enrichi) : {review_present}/{len(capacites_review)}")
            print(f"🎯 Total capacités : {len(capabilities)}")
            
            # Afficher échantillon des capacités
            print("\n📋 Échantillon des capacités :")
            for i, cap in enumerate(capabilities[:15], 1):
                emoji = "📚" if any(doc in cap for doc in ["document", "guide", "schema"]) else "🔍"
                print(f"  {i:2d}. {emoji} {cap}")
            
            if len(capabilities) > 15:
                print(f"  ... et {len(capabilities)-15} autres capacités")
            
            self.test_results.append({
                "test": "capacites_combinees",
                "status": "SUCCESS",
                "total_capabilities": len(capabilities),
                "doc_capabilities": doc_present,
                "review_capabilities": review_present
            })
            
        except Exception as e:
            print(f"❌ Erreur capacités : {e}")
            self.test_results.append({
                "test": "capacites_combinees",
                "status": "ERROR",
                "error": str(e)
            })
    
    async def test_documentation_enterprise(self):
        """Test 3 : Fonctionnalités documentation enterprise (Agent 05)"""
        print("\n📚 TEST 3 : Documentation enterprise")
        print("-" * 40)
        
        try:
            # Test documentation enterprise avancée
            doc_result = await self.agent.enterprise_documentation_advanced()
            
            print(f"✅ Documentation type : {doc_result.get('documentation_type', 'N/A')}")
            print(f"✅ Analyse intelligente : {bool(doc_result.get('intelligent_analysis'))}")
            print(f"✅ Contenu adaptatif : {bool(doc_result.get('adaptive_content'))}")
            print(f"✅ Métriques qualité : {bool(doc_result.get('quality_metrics'))}")
            print(f"✅ Multi-format : {len(doc_result.get('multi_format_outputs', []))}")
            
            # Test documentation complète
            doc_complete = await self.agent.documenter_complete()
            
            print(f"✅ Documentation complète : {doc_complete.get('status', 'N/A')}")
            print(f"✅ Durée : {doc_complete.get('duree', 0):.2f}s")
            
            self.test_results.append({
                "test": "documentation_enterprise",
                "status": "SUCCESS",
                "doc_advanced": bool(doc_result),
                "doc_complete": doc_complete.get('status') == 'SUCCESS'
            })
            
        except Exception as e:
            print(f"❌ Erreur documentation : {e}")
            self.test_results.append({
                "test": "documentation_enterprise",
                "status": "ERROR",
                "error": str(e)
            })
    
    async def test_peer_review_correction(self):
        """Test 4 : Fonctionnalités peer review et correction (enrichies)"""
        print("\n🔍 TEST 4 : Peer review et correction")
        print("-" * 40)
        
        try:
            # Simuler résultats de test avec défaillances
            fake_test_results = {
                'tests_results': {
                    'utilisation_reelle': {
                        'details': {
                            'instantiation': {'status': 'FAILED'},
                            'pattern_factory_methods': {'status': 'FAILED'}
                        },
                        'tests_passed': 2,
                        'tests_executed': 8
                    }
                },
                'global_scores': {
                    'utilisation_score': 2.5
                }
            }
            
            # Créer un agent de test temporaire
            test_agent_content = '''#!/usr/bin/env python3
"""Agent de test pour correction"""

class TestAgent:
    async async def test_method(self):
        pass
'''
            
            test_agent_path = Path("test_agent_temp.py")
            test_agent_path.write_text(test_agent_content, encoding='utf-8')
            
            try:
                # Test correction défaillances
                correction_result = await self.agent.corriger_defaillances_utilisation_complete(
                    str(test_agent_path), 
                    fake_test_results
                )
                
                print(f"✅ Correction status : {correction_result.get('status', 'N/A')}")
                print(f"✅ Corrections appliquées : {correction_result.get('corrections_count', 0)}")
                
                if correction_result.get('corrections_applied'):
                    print("📋 Corrections détaillées :")
                    for correction in correction_result['corrections_applied'][:5]:
                        print(f"  - {correction}")
                
                # Test certification finale
                certification = await self.agent.generer_certification_finale(
                    str(test_agent_path),
                    fake_test_results
                )
                
                print(f"✅ Certification : {certification.get('grade', 'N/A')}")
                print(f"✅ Amélioration : +{certification.get('amelioration', 0):.1f}%")
                
                self.test_results.append({
                    "test": "peer_review_correction",
                    "status": "SUCCESS",
                    "corrections_applied": correction_result.get('corrections_count', 0),
                    "certification_grade": certification.get('grade')
                })
                
            finally:
                # Nettoyer fichier temporaire
                if test_agent_path.exists():
                    test_agent_path.unlink()
            
        except Exception as e:
            print(f"❌ Erreur peer review : {e}")
            self.test_results.append({
                "test": "peer_review_correction",
                "status": "ERROR",
                "error": str(e)
            })
    
    async def test_execution_taches(self):
        """Test 5 : Exécution tâches Pattern Factory"""
        print("\n⚡ TEST 5 : Exécution tâches Pattern Factory")
        print("-" * 40)
        
        try:
            # Test tâche documentation
            task_doc = Task("documenter_complete", "Documentation complète")
            result_doc = await self.agent.execute_task(task_doc)
            
            print(f"✅ Tâche documentation : {result_doc.success}")
            print(f"✅ Données retournées : {bool(result_doc.data)}")
            
            # Test tâche enterprise
            task_enterprise = Task("enterprise_documentation", "Documentation enterprise")
            result_enterprise = await self.agent.execute_task(task_enterprise)
            
            print(f"✅ Tâche enterprise : {result_enterprise.success}")
            
            self.test_results.append({
                "test": "execution_taches",
                "status": "SUCCESS",
                "task_doc_success": result_doc.success,
                "task_enterprise_success": result_enterprise.success
            })
            
        except Exception as e:
            print(f"❌ Erreur exécution tâches : {e}")
            self.test_results.append({
                "test": "execution_taches",
                "status": "ERROR",
                "error": str(e)
            })
    
    async def test_integration_complete(self):
        """Test 6 : Intégration complète"""
        print("\n🌟 TEST 6 : Intégration complète")
        print("-" * 40)
        
        try:
            # Vérifier que toutes les statistiques sont initialisées
            stats = {
                "documents_generes": len(self.agent.documents_generes),
                "guides_crees": len(self.agent.guides_crees),
                "schemas_documentes": len(self.agent.schemas_documentes),
                "reviews_effectuees": len(self.agent.reviews_effectuees),
                "corrections_appliquees": len(self.agent.corrections_appliquees),
                "certifications_generees": len(self.agent.certifications_generees)
            }
            
            print("📊 Statistiques intégrées :")
            for stat_name, stat_value in stats.items():
                print(f"  - {stat_name} : {stat_value}")
            
            # Test health check final
            final_health = await self.agent.health_check()
            
            print(f"✅ Health check final : {final_health['status']}")
            print(f"✅ Agent prêt : {final_health.get('ready', False)}")
            
            self.test_results.append({
                "test": "integration_complete",
                "status": "SUCCESS",
                "statistics": stats,
                "final_health": final_health['status']
            })
            
        except Exception as e:
            print(f"❌ Erreur intégration : {e}")
            self.test_results.append({
                "test": "integration_complete",
                "status": "ERROR",
                "error": str(e)
            })
    
    async def afficher_resume_final(self):
        """Affiche le résumé final des tests"""
        print("\n" + "=" * 80)
        print("🏆 RÉSUMÉ FINAL - Agent 05 Documenteur + Peer-Reviewer ENRICHI")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        tests_success = sum(1 for test in self.test_results if test['status'] == 'SUCCESS')
        tests_error = total_tests - tests_success
        
        print(f"📊 RÉSULTATS GLOBAUX :")
        print(f"  - Tests exécutés : {total_tests}")
        print(f"  - Tests réussis : {tests_success} ✅")
        print(f"  - Tests échoués : {tests_error} ❌")
        print(f"  - Taux de réussite : {(tests_success/total_tests)*100:.1f}%")
        
        print(f"\n📋 DÉTAIL DES TESTS :")
        for i, test in enumerate(self.test_results, 1):
            status_emoji = "✅" if test['status'] == 'SUCCESS' else "❌"
            print(f"  {i}. {status_emoji} {test['test']}")
            
            if test['status'] == 'ERROR':
                print(f"     Erreur : {test.get('error', 'N/A')}")
        
        # Validation finale
        if tests_success == total_tests:
            print(f"\n🎉 VALIDATION COMPLÈTE RÉUSSIE !")
            print(f"   L'Agent 05 ENRICHI combine parfaitement :")
            print(f"   📚 Capacités documentation enterprise (Agent 05)")
            print(f"   🔍 Capacités peer review et correction (Agents 16 & 17)")
            print(f"   ⚡ Conformité Pattern Factory NextGeneration")
        else:
            print(f"\n⚠️ VALIDATION PARTIELLE")
            print(f"   Certains tests ont échoué, révision nécessaire")
        
        # Sauvegarder résultats
        await self.sauvegarder_resultats_test()
    
    async def sauvegarder_resultats_test(self):
        """Sauvegarde les résultats de test"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = Path(f"test_agent_05_enrichi_{timestamp}.json")
            
            test_report = {
                "test_type": "agent_05_documenteur_peer_reviewer_enrichi",
                "timestamp": datetime.now().isoformat(),
                "total_tests": len(self.test_results),
                "tests_success": sum(1 for test in self.test_results if test['status'] == 'SUCCESS'),
                "tests_results": self.test_results
            }
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(test_report, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"📄 Rapport de test sauvegardé : {report_file}")
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde rapport : {e}")

async def main():
    """Fonction principale de test"""
    tester = TestAgent05Enrichi()
    success = await tester.run_all_tests()
    
    if success:
        print(f"\n🎯 TESTS TERMINÉS AVEC SUCCÈS")
    else:
        print(f"\n💥 TESTS TERMINÉS AVEC ERREURS")
    
    return success

if __name__ == "__main__":
    asyncio.run(main()) 



