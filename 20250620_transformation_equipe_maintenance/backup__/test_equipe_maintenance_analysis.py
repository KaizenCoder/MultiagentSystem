#!/usr/bin/env python3
"""
🧪 Test Équipe de Maintenance - Analyse Seule
Mission: Tester l'équipe de maintenance sur le répertoire agents
Mode: ANALYSE SEULE - Pas de corrections
"""

import asyncio
import json
from logging_manager_optimized import LoggingManager
from datetime import datetime
from pathlib import Path
from typing import Dict
import sys

from maintenance_template_manager import create_maintenance_template_manager
from chef_equipe_pattern_factory import create_chef_equipe_pattern_factory

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class TestEquipeMaintenanceAnalysis:
    """Test de l'équipe de maintenance en mode analyse seule"""
    
    def __init__(self, target_agents_path: str):
        self.target_agents_path = Path(target_agents_path)
        self.workspace_path = Path(".")
        # LoggingManager NextGeneration - Tests
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={
            "logger_name": "TestEquipeMaintenanceAnalysis",
            "log_level": "DEBUG",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": False,  # Tests synchrones
            "console_output": True
        })
        
        # Vérifier que le répertoire existe
        if not self.target_agents_path.exists():
            raise FileNotFoundError(f"Répertoire agents non trouvé: {self.target_agents_path}")
        
        self.logger.info(f"🎯 Target: {self.target_agents_path}")
        self.logger.info(f"📁 Workspace: {self.workspace_path}")
        
    async def test_analyse_complete(self) -> Dict:
        """Test complet d'analyse avec l'équipe de maintenance"""
        self.logger.info("🧪 DÉBUT TEST ANALYSE ÉQUIPE DE MAINTENANCE")
        self.logger.info("=" * 60)
        
        start_time = datetime.now()
        
        try:
            # Créer le chef d'équipe Pattern Factory
            chef_equipe = create_chef_equipe_pattern_factory(
                target_path=str(self.target_agents_path),
                workspace_path=str(self.workspace_path),
                safe_mode=True,
                rapport_detaille=True
            )
            
            # Démarrer le chef d'équipe
            await chef_equipe.startup()
            
            # Health check initial
            health = await chef_equipe.health_check()
            self.logger.info(f"🏥 Health Check: {health['status']}")
            self.logger.info(f"📋 Templates: {health['pattern_factory']['templates_loaded']}")
            
            # Créer l'équipe via factory
            self.logger.info("🏭 Création de l'équipe via Pattern Factory...")
            await chef_equipe._creer_equipe_via_factory()
            
            # Test Agent 1: Analyseur de Structure
            self.logger.info("\n📊 TEST AGENT 1: ANALYSEUR DE STRUCTURE")
            self.logger.info("-" * 50)
            
            agent_1 = chef_equipe.equipe_agents["agent_1_analyseur_structure"]
            resultat_1 = await agent_1.analyser_structure()
            
            self.logger.info(f"✅ Agent 1 terminé:")
            self.logger.info(f"   📁 Répertoire analysé: {resultat_1.get('directory_analyzed', 'N/A')}")
            self.logger.info(f"   📄 Fichiers trouvés: {resultat_1.get('total_files', 0)}")
            self.logger.info(f"   🐍 Fichiers Python: {resultat_1.get('python_files', 0)}")
            self.logger.info(f"   🔧 Outils détectés: {resultat_1.get('tools_count', 0)}")
            
            # Test Agent 2: Évaluateur d'Utilité
            self.logger.info("\n🎯 TEST AGENT 2: ÉVALUATEUR D'UTILITÉ")
            self.logger.info("-" * 50)
            
            agent_2 = chef_equipe.equipe_agents["agent_2_evaluateur_utilite"]
            agent_2.analyse_structure = resultat_1
            resultat_2 = await agent_2.evaluer_utilite()
            
            self.logger.info(f"✅ Agent 2 terminé:")
            self.logger.info(f"   🔍 Outils analysés: {len(resultat_2.get('evaluations', []))}")
            self.logger.info(f"   ⭐ Outils recommandés: {len(resultat_2.get('outils_utiles', []))}")
            self.logger.info(f"   ⚠️ Outils conditionnels: {len(resultat_2.get('outils_conditionnels', []))}")
            self.logger.info(f"   ❌ Outils non recommandés: {len(resultat_2.get('outils_non_recommandes', []))}")
            
            # Test Agent 4: Testeur d'Intégration (test de base)
            self.logger.info("\n🧪 TEST AGENT 4: TESTEUR D'INTÉGRATION")
            self.logger.info("-" * 50)
            
            agent_4 = chef_equipe.equipe_agents["agent_4_testeur_integration"]
            # Simuler des outils adaptés pour le test
            agent_4.outils_adaptes = resultat_2.get('outils_utiles', [])[:5]  # Prendre les 5 premiers
            agent_4.target_path = self.target_agents_path
            agent_4.workspace_path = self.workspace_path
            resultat_4 = await agent_4.tester_integration()
            
            self.logger.info(f"✅ Agent 4 terminé:")
            self.logger.info(f"   🧪 Tests exécutés: {resultat_4.get('total_tests', 0)}")
            self.logger.info(f"   ✅ Tests réussis: {resultat_4.get('tests_passed', 0)}")
            self.logger.info(f"   ❌ Tests échoués: {resultat_4.get('tests_failed', 0)}")
            self.logger.info(f"   📊 Taux de réussite: {resultat_4.get('success_rate', 0):.1%}")
            
            # Test Agent 6: Validateur Final
            self.logger.info("\n✅ TEST AGENT 6: VALIDATEUR FINAL")
            self.logger.info("-" * 50)
            
            agent_6 = chef_equipe.equipe_agents["agent_6_validateur_final"]
            resultats_equipe = {
                "analyse": resultat_1,
                "evaluation": resultat_2,
                "adaptation": {"tools_adapted": 0, "status": "skipped"},
                "tests": resultat_4,
                "documentation": {"nombre_documents": 0, "status": "skipped"}
            }
            agent_6.resultats_equipe = resultats_equipe
            agent_6.target_path = str(self.target_agents_path)
            agent_6.workspace_path = str(self.workspace_path)
            resultat_6 = await agent_6.valider_mission()
            
            self.logger.info(f"✅ Agent 6 terminé:")
            validation = resultat_6.get('mission_validation', {})
            self.logger.info(f"   📊 Score qualité: {validation.get('quality_score', 0)}/100")
            self.logger.info(f"   🎯 Statut mission: {validation.get('mission_status', 'UNKNOWN')}")
            self.logger.info(f"   ⚠️ Issues critiques: {validation.get('critical_issues', 0)}")
            self.logger.info(f"   ⚡ Warnings: {validation.get('warnings', 0)}")
            
            # Arrêter le chef d'équipe
            await chef_equipe.shutdown()
            
            # Résumé final
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            resultats_test = {
                "test_id": f"maintenance_analysis_{start_time.strftime('%Y%m%d_%H%M%S')}",
                "target_path": str(self.target_agents_path),
                "pattern_factory": True,
                "mode": "ANALYSE_SEULE",
                "duration_seconds": duration,
                "timestamp": start_time.isoformat(),
                "agents_testes": {
                    "agent_1_analyseur": {
                        "status": "success",
                        "fichiers_analyses": resultat_1.get('total_files', 0),
                        "outils_detectes": resultat_1.get('tools_count', 0)
                    },
                    "agent_2_evaluateur": {
                        "status": "success",
                        "outils_evalues": len(resultat_2.get('evaluations', [])),
                        "outils_recommandes": len(resultat_2.get('outils_utiles', []))
                    },
                    "agent_4_testeur": {
                        "status": "success",
                        "tests_executes": resultat_4.get('total_tests', 0),
                        "taux_reussite": resultat_4.get('success_rate', 0)
                    },
                    "agent_6_validateur": {
                        "status": "success",
                        "score_qualite": validation.get('quality_score', 0),
                        "statut_mission": validation.get('mission_status', 'UNKNOWN')
                    }
                },
                "pattern_factory_metrics": {
                    "templates_charges": health['pattern_factory']['templates_loaded'],
                    "agents_crees_via_factory": chef_equipe.metrics['agents_created_via_factory'],
                    "cache_hit_rate": health['pattern_factory']['cache_hit_rate']
                },
                "resume_analyse": {
                    "agents_dans_repertoire": resultat_1.get('total_files', 0),
                    "agents_python": resultat_1.get('python_files', 0),
                    "outils_detectes": resultat_1.get('tools_count', 0),
                    "outils_recommandes": len(resultat_2.get('outils_utiles', [])),
                    "score_qualite_global": validation.get('quality_score', 0)
                }
            }
            
            # Sauvegarder le rapport
            rapport_path = self.workspace_path / f"test_maintenance_analysis_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
            with open(rapport_path, 'w', encoding='utf-8') as f:
                json.dump(resultats_test, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"\n🎉 TEST TERMINÉ AVEC SUCCÈS en {duration:.1f}s")
            self.logger.info(f"💾 Rapport sauvegardé: {rapport_path}")
            
            return resultats_test
            
        except Exception as e:
            self.logger.error(f"❌ Erreur durant le test: {e}")
            raise

async def main():
    """Point d'entrée principal"""
    print("🧪 TEST ÉQUIPE DE MAINTENANCE - ANALYSE SEULE")
    print("=" * 60)
    
    # Chemin vers le répertoire agents
    agents_path = "../agent_factory_implementation/agents"
    
    # Arguments en ligne de commande
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h"]:
            print("""
Usage: python test_equipe_maintenance_analysis.py [AGENTS_PATH]

Arguments:
  AGENTS_PATH     Chemin vers le répertoire des agents à analyser
                  (défaut: ../agent_factory_implementation/agents)

Mode: ANALYSE SEULE - Aucune correction effectuée

Fonctionnalités testées:
  - Agent 1: Analyse de structure
  - Agent 2: Évaluation d'utilité
  - Agent 4: Tests d'intégration
  - Agent 6: Validation finale
  - Pattern Factory complet
""")
            return 0
        
        agents_path = sys.argv[1]
    
    try:
        # Créer et exécuter le test
        test_runner = TestEquipeMaintenanceAnalysis(agents_path)
        resultats = await test_runner.test_analyse_complete()
        
        # Afficher le résumé
        print("\n📊 RÉSUMÉ DU TEST:")
        print(f"Mode: {resultats['mode']}")
        print(f"Durée: {resultats['duration_seconds']:.1f}s")
        print(f"Pattern Factory: {resultats['pattern_factory']}")
        
        resume = resultats['resume_analyse']
        print(f"\n📈 RÉSULTATS ANALYSE:")
        print(f"Agents dans répertoire: {resume['agents_dans_repertoire']}")
        print(f"Fichiers Python: {resume['agents_python']}")
        print(f"Outils détectés: {resume['outils_detectes']}")
        print(f"Outils recommandés: {resume['outils_recommandes']}")
        print(f"Score qualité global: {resume['score_qualite_global']}/100")
        
        return 0
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result) 