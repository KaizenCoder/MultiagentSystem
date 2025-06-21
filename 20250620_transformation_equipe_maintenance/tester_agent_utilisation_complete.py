#!/usr/bin/env python3
"""
🎯 TEST AGENT TRANSFORMÉ EN UTILISATION COMPLÈTE
Utilise l'Agent 04 MEGA-TESTEUR enrichi avec les capacités des agents experts

Workflow :
1. Agent 03 transforme l'agent
2. Agent 04 MEGA-TESTEUR teste EN UTILISATION RÉELLE
3. Rapport complet avec certification
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import sys
from pathlib import Path
from core import logging_manager

# Ajouter le chemin vers notre équipe
sys.path.append("agent_equipe_maintenance")

class TesteurUtilisationComplete:
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(logs_dir / f"test_utilisation_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        # LoggingManager NextGeneration - Agent
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="TesteurUtilisationComplete",
            role="ai_processor",
            domain="testing",
            async_enabled=True
        )

    async def tester_agent_utilisation_directe(self, agent_path: str) -> dict:
        """
        🎯 TEST DIRECT EN UTILISATION RÉELLE
        Teste directement un agent transformé avec l'Agent 04 MEGA-TESTEUR
        """
        self.logger.info(f"🎯 DÉBUT TEST UTILISATION DIRECTE : {agent_path}")
        
        try:
            # Importer l'Agent 04 MEGA-TESTEUR pour tests utilisation
            from agent_MAINTENANCE_04_mega_testeur_utilisation import Agent04MegaTesteurUtilisation
            
            self.logger.info("🚀 Initialisation Agent 04 MEGA-TESTEUR...")
            mega_testeur = Agent04MegaTesteurUtilisation()
            
            # Tests utilisation réelle complets
            self.logger.info(f"🎯 Tests utilisation réelle : {agent_path}")
            test_results = await mega_testeur.tester_agent_transforme_utilisation_complete(agent_path)
            
            # Compilation rapport final
            rapport_final = {
                'status': 'SUCCÈS_TEST_UTILISATION',
                'agent_tested': agent_path,
                'tests_utilisation': test_results,
                'certification_finale': self._generer_certification_utilisation(test_results),
                'timestamp': datetime.now().isoformat()
            }
            
            # Sauvegarde rapport
            await self._sauvegarder_rapport_final(rapport_final)
            
            self.logger.info("✅ TEST UTILISATION TERMINÉ AVEC SUCCÈS")
            return rapport_final
            
        except Exception as e:
            self.logger.error(f"❌ Erreur test utilisation : {e}")
            return {
                'status': 'ERREUR_TEST_UTILISATION',
                'error': str(e),
                'agent_tested': agent_path
            }

    def _generer_certification_utilisation(self, test_results: dict) -> dict:
        """Génère la certification basée sur les tests utilisation"""
        
        # Scores utilisation
        global_scores = test_results.get('global_scores', {})
        utilisation_score = global_scores.get('utilisation', 0)
        overall_score = global_scores.get('overall', 0)
        
        # Certification utilisation (basée sur Agent 04)
        utilisation_certification = test_results.get('certification', '❌ NON CERTIFIÉ')
        
        # Tests utilisation réelle détaillés
        tests_util = test_results.get('tests_results', {}).get('utilisation_reelle', {})
        tests_passed = tests_util.get('tests_passed', 0)
        tests_executed = tests_util.get('tests_executed', 0)
        
        # Certification finale
        if utilisation_score >= 9.0 and tests_passed == tests_executed:
            certification_finale = "🏆 AGENT PARFAITEMENT OPÉRATIONNEL - Utilisation EXCELLENTE"
        elif utilisation_score >= 7.0 and tests_passed >= tests_executed * 0.8:
            certification_finale = "✅ AGENT OPÉRATIONNEL - Utilisation BONNE"
        elif utilisation_score >= 5.0:
            certification_finale = "⚠️ AGENT PARTIELLEMENT OPÉRATIONNEL - Améliorations requises"
        else:
            certification_finale = "❌ AGENT NON OPÉRATIONNEL - Défaillances critiques"
        
        return {
            'utilisation_certification': utilisation_certification,
            'certification_finale': certification_finale,
            'scores': {
                'utilisation_score': utilisation_score,
                'overall_score': overall_score,
                'tests_passed': tests_passed,
                'tests_executed': tests_executed,
                'success_rate': (tests_passed / tests_executed * 100) if tests_executed > 0 else 0
            },
            'recommandations': test_results.get('recommendations', [])
        }

    async def _sauvegarder_rapport_final(self, rapport: dict):
        """Sauvegarde le rapport final de test"""
        try:
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            agent_name = Path(rapport['agent_tested']).stem
            report_file = reports_dir / f"test_utilisation_{agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            import json
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"📄 Rapport final sauvegardé : {report_file}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde rapport final : {e}")

    def afficher_resultats(self, rapport: dict):
        """Affichage formaté des résultats"""
        print("\n" + "="*80)
        print("🎯 RÉSULTATS TEST UTILISATION RÉELLE COMPLÈTE")
        print("="*80)
        
        print(f"\n📁 Agent testé : {rapport.get('agent_tested', 'N/A')}")
        print(f"⏱️ Timestamp : {rapport.get('timestamp', 'N/A')}")
        
        # Résultats tests utilisation
        if 'tests_utilisation' in rapport:
            tests = rapport['tests_utilisation']
            print(f"\n🎯 TESTS UTILISATION RÉELLE :")
            
            if 'global_scores' in tests:
                scores = tests['global_scores']
                print(f"   📊 Score Utilisation : {scores.get('utilisation', 0)}/10")
                print(f"   📊 Score Performance : {scores.get('performance', 0)}/10")
                print(f"   📊 Score Sécurité : {scores.get('security', 0)}/10")
                print(f"   📊 Score Global : {scores.get('overall', 0)}/10")
            
            if 'tests_results' in tests:
                results = tests['tests_results']
                
                # Tests utilisation réelle
                if 'utilisation_reelle' in results:
                    util = results['utilisation_reelle']
                    print(f"\n   🎯 UTILISATION RÉELLE :")
                    print(f"      Tests passés : {util.get('tests_passed', 0)}/{util.get('tests_executed', 0)}")
                    
                    if 'details' in util:
                        details = util['details']
                        print(f"      Import : {'✅' if details.get('import', {}).get('status') == 'SUCCESS' else '❌'}")
                        print(f"      Instanciation : {'✅' if details.get('instantiation', {}).get('status') == 'SUCCESS' else '❌'}")
                        print(f"      Méthodes Pattern Factory : {'✅' if details.get('pattern_factory_methods', {}).get('status') == 'SUCCESS' else '❌'}")
                        print(f"      Capacités : {'✅' if details.get('capabilities', {}).get('status') == 'SUCCESS' else '❌'}")
                
                # Tests performance
                if 'performance_utilisation' in results:
                    perf = results['performance_utilisation']
                    print(f"\n   ⚡ PERFORMANCE :")
                    print(f"      Import : {perf.get('import_time_ms', 0):.1f}ms")
                    print(f"      Instanciation : {perf.get('instantiation_time_ms', 0):.1f}ms")
                    print(f"      Mémoire : {perf.get('memory_usage_mb', 0):.1f}MB")
                    print(f"      Grade : {perf.get('performance_grade', 'N/A')}")
                
                # Tests thread-safety
                if 'thread_safety_utilisation' in results:
                    thread = results['thread_safety_utilisation']
                    print(f"\n   🔒 THREAD-SAFETY :")
                    print(f"      Créations parallèles : {thread.get('parallel_creations', 0)}")
                    print(f"      Taux succès : {thread.get('success_rate', 0):.1%}")
                    print(f"      Thread-safe : {'✅' if thread.get('thread_safe', False) else '❌'}")
                
                # Audit sécurité
                if 'security_audit' in results:
                    sec = results['security_audit']
                    print(f"\n   🔐 SÉCURITÉ :")
                    print(f"      Vulnérabilités : {sec.get('findings_count', 0)}")
                    print(f"      Critiques : {sec.get('critical_count', 0)}")
                    print(f"      Score : {sec.get('security_score', 0)}/10")
        
        # Certification finale
        if 'certification_finale' in rapport:
            cert = rapport['certification_finale']
            print(f"\n🏆 CERTIFICATION FINALE :")
            print(f"   {cert.get('certification_finale', 'N/A')}")
            
            if 'scores' in cert:
                scores = cert['scores']
                print(f"\n   📈 SCORES DÉTAILLÉS :")
                print(f"      Taux réussite : {scores.get('success_rate', 0):.1f}%")
                print(f"      Score utilisation : {scores.get('utilisation_score', 0)}/10")
                print(f"      Score global : {scores.get('overall_score', 0)}/10")
            
            if 'recommandations' in cert and cert['recommandations']:
                print(f"\n💡 RECOMMANDATIONS :")
                for rec in cert['recommandations']:
                    print(f"   • {rec}")
        
        print("\n" + "="*80)

async def main():
    """Point d'entrée principal"""
    print("🎯 Testeur Utilisation Complète - Tests Réels d'Agent Transformé")
    
    # Agent à tester
    agent_path = "../agent_factory_implementation/agents/agent_11_auditeur_qualite.py"
    
    if len(sys.argv) > 1:
        agent_path = sys.argv[1]
    
    if not Path(agent_path).exists():
        print(f"❌ Agent non trouvé : {agent_path}")
        return
    
    print(f"🎯 Test utilisation réelle de l'agent : {agent_path}")
    
    # Initialiser testeur
    testeur = TesteurUtilisationComplete()
    
    # Exécuter test utilisation
    rapport = await testeur.tester_agent_utilisation_directe(agent_path)
    
    # Afficher résultats
    testeur.afficher_resultats(rapport)
    
    # Status final
    if rapport.get('status') == 'SUCCÈS_TEST_UTILISATION':
        cert = rapport.get('certification_finale', {})
        scores = cert.get('scores', {})
        success_rate = scores.get('success_rate', 0)
        
        if success_rate >= 100:
            print("🏆 Agent PARFAITEMENT opérationnel en utilisation réelle !")
        elif success_rate >= 80:
            print("✅ Agent opérationnel avec quelques améliorations possibles")
        elif success_rate >= 60:
            print("⚠️ Agent partiellement opérationnel - corrections requises")
        else:
            print("❌ Agent non-opérationnel - défaillances critiques")
    else:
        print(f"❌ Test utilisation échoué : {rapport.get('status', 'Erreur inconnue')}")

if __name__ == "__main__":
    asyncio.run(main()) 



