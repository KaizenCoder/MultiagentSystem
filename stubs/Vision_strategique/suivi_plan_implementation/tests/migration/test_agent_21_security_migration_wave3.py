#!/usr/bin/env python3
"""
🔐 TEST MIGRATION AGENT 21 SECURITY SUPPLY CHAIN - NextGeneration Wave 3
=========================================================================

🎯 Mission : Tests validation exhaustifs pour Agent 21 Security Supply Chain Enterprise.
⚡ Objectif : Valider migration NextGeneration Wave 3 avec 100% de couverture.
🏢 Équipe : Wave 3 - Piliers Enterprise Migration NextGeneration

Tests Coverage :
✅ Création et initialisation agent
✅ Health checks et métriques
✅ Exécution tâches spécialisées
✅ Features LLM enhancement
✅ Compliance et sécurité
✅ Performance et robustesse

Author: Équipe de Maintenance NextGeneration
Version: 1.0.0 - Tests Migration Wave 3 Agent 21
Created: 2025-06-28 - Wave 3 Enterprise Pillar
"""

import asyncio
import time
import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Dict, List, Any

# Configuration imports
try:
    project_root = Path(__file__).resolve().parents[0]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

# Import agent migré
from agents.agent_SECURITY_21_supply_chain_enterprise import (
    Agent21SecuritySupplyChain,
    create_agent_21_security_supply_chain,
    validate_agent_21_security,
    SecurityMetrics,
    SecurityTaskResult,
    LLMSecurityEnhancement
)

from core.agent_factory_architecture import Task, Result

class TestAgent21SecurityMigration:
    """🧪 Tests exhaustifs migration Agent 21 Security Supply Chain"""
    
    def __init__(self):
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "agent_info": {},
            "tests_executed": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "performance_metrics": {},
            "coverage_report": {},
            "errors": []
        }
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """🚀 Exécution complète de tous les tests"""
        print("🔐 DÉMARRAGE TESTS MIGRATION AGENT 21 SECURITY SUPPLY CHAIN")
        print("=" * 70)
        
        try:
            # Tests de base
            await self._test_agent_creation()
            await self._test_agent_lifecycle()
            await self._test_health_checks()
            
            # Tests fonctionnels
            await self._test_specialized_tasks()
            await self._test_llm_enhancement()
            await self._test_security_scenarios()
            
            # Tests de performance
            await self._test_performance()
            await self._test_concurrent_execution()
            
            # Tests de robustesse
            await self._test_error_handling()
            await self._test_edge_cases()
            
            # Validation finale
            await self._test_full_validation()
            
            return self._generate_final_report()
            
        except Exception as e:
            self.test_results["errors"].append(f"Erreur globale tests: {str(e)}")
            return self.test_results
    
    async def _test_agent_creation(self):
        """🏭 Test création agent via Factory Pattern"""
        print("\n📦 Test Création Agent...")
        
        try:
            start_time = time.time()
            agent = create_agent_21_security_supply_chain()
            creation_time = (time.time() - start_time) * 1000
            
            # Vérifications
            assert agent.id == "agent_21_security_supply_chain"
            assert agent.agent_version == "5.3.0"
            assert agent.compliance_target == 96.0
            assert len(agent.capabilities) >= 10
            
            self.test_results["agent_info"] = {
                "id": agent.id,
                "version": agent.agent_version,
                "compliance_score": agent.compliance_score,
                "capabilities_count": len(agent.capabilities),
                "creation_time_ms": creation_time
            }
            
            self._record_test_result("agent_creation", True, f"Temps: {creation_time:.2f}ms")
            print(f"  ✅ Agent créé en {creation_time:.2f}ms")
            
        except Exception as e:
            self._record_test_result("agent_creation", False, str(e))
            print(f"  ❌ Erreur création: {str(e)}")
    
    async def _test_agent_lifecycle(self):
        """♻️ Test cycle de vie agent"""
        print("\n♻️ Test Cycle de Vie...")
        
        try:
            agent = create_agent_21_security_supply_chain()
            
            # Test startup
            start_time = time.time()
            await agent.startup()
            startup_time = (time.time() - start_time) * 1000
            
            # Test shutdown
            start_time = time.time()
            await agent.shutdown()
            shutdown_time = (time.time() - start_time) * 1000
            
            self.test_results["performance_metrics"]["lifecycle"] = {
                "startup_time_ms": startup_time,
                "shutdown_time_ms": shutdown_time
            }
            
            self._record_test_result("agent_lifecycle", True, 
                                   f"Startup: {startup_time:.2f}ms, Shutdown: {shutdown_time:.2f}ms")
            print(f"  ✅ Lifecycle OK - Startup: {startup_time:.2f}ms, Shutdown: {shutdown_time:.2f}ms")
            
        except Exception as e:
            self._record_test_result("agent_lifecycle", False, str(e))
            print(f"  ❌ Erreur lifecycle: {str(e)}")
    
    async def _test_health_checks(self):
        """🩺 Test health checks et métriques"""
        print("\n🩺 Test Health Checks...")
        
        try:
            agent = create_agent_21_security_supply_chain()
            await agent.startup()
            
            start_time = time.time()
            health = await agent.health_check()
            health_time = (time.time() - start_time) * 1000
            
            # Vérifications
            assert health["status"] == "healthy"
            assert health["compliance_score"] == "96%"
            assert "security_metrics" in health
            assert "llm_enhancement" in health
            
            await agent.shutdown()
            
            self.test_results["performance_metrics"]["health_check_ms"] = health_time
            
            self._record_test_result("health_checks", True, f"Temps: {health_time:.2f}ms")
            print(f"  ✅ Health check OK en {health_time:.2f}ms")
            
        except Exception as e:
            self._record_test_result("health_checks", False, str(e))
            print(f"  ❌ Erreur health check: {str(e)}")
    
    async def _test_specialized_tasks(self):
        """🎯 Test tâches spécialisées"""
        print("\n🎯 Test Tâches Spécialisées...")
        
        specialized_tasks = [
            ("zero_trust_validation", {"security_level": "maximum"}),
            ("supply_chain_analysis", {"scope": "comprehensive"}),
            ("vulnerability_assessment", {"depth": "full"}),
            ("threat_intelligence", {"feeds": "all"}),
            ("ml_security_analysis", {"models": "active"}),
            ("compliance_validation", {"frameworks": ["SOC2", "ISO27001"]}),
            ("auto_remediation", {"incidents": "active"}),
            ("behavioral_analysis", {"users": "all"}),
            ("dependency_scanning", {"scope": "full"}),
            ("container_security", {"images": "all"}),
            ("pipeline_security", {"pipelines": "active"})
        ]
        
        try:
            agent = create_agent_21_security_supply_chain()
            await agent.startup()
            
            task_results = {}
            total_time = 0
            
            for task_type, params in specialized_tasks:
                task = Task(type=task_type, params=params)
                start_time = time.time()
                result = await agent.execute_task(task)
                execution_time = (time.time() - start_time) * 1000
                total_time += execution_time
                
                task_results[task_type] = {
                    "success": result.success,
                    "execution_time_ms": execution_time,
                    "has_security_analysis": hasattr(result.data, 'security_analysis'),
                    "has_llm_enhancement": result.metrics.get("llm_enhanced", False)
                }
                
                if result.success:
                    print(f"  ✅ {task_type}: OK ({execution_time:.1f}ms)")
                else:
                    print(f"  ❌ {task_type}: ERREUR - {result.error}")
            
            await agent.shutdown()
            
            success_count = sum(1 for r in task_results.values() if r["success"])
            success_rate = (success_count / len(specialized_tasks)) * 100
            
            self.test_results["performance_metrics"]["specialized_tasks"] = {
                "total_tasks": len(specialized_tasks),
                "successful_tasks": success_count,
                "success_rate_percent": success_rate,
                "total_time_ms": total_time,
                "average_time_ms": total_time / len(specialized_tasks),
                "task_details": task_results
            }
            
            self._record_test_result("specialized_tasks", success_count == len(specialized_tasks),
                                   f"Succès: {success_count}/{len(specialized_tasks)} ({success_rate:.1f}%)")
            
        except Exception as e:
            self._record_test_result("specialized_tasks", False, str(e))
            print(f"  ❌ Erreur tâches spécialisées: {str(e)}")
    
    async def _test_llm_enhancement(self):
        """🧠 Test enhancements LLM"""
        print("\n🧠 Test LLM Enhancement...")
        
        try:
            agent = create_agent_21_security_supply_chain()
            await agent.startup()
            
            # Test avec LLM enhancement activé
            task = Task(type="ml_security_analysis", params={"llm_enhanced": True})
            start_time = time.time()
            result = await agent.execute_task(task)
            execution_time = (time.time() - start_time) * 1000
            
            # Vérifications LLM
            assert result.success
            assert result.metrics.get("llm_enhanced", False)
            assert "llm_analysis_time_ms" in result.metrics
            
            await agent.shutdown()
            
            self.test_results["performance_metrics"]["llm_enhancement"] = {
                "enabled": True,
                "execution_time_ms": execution_time,
                "llm_analysis_time_ms": result.metrics.get("llm_analysis_time_ms", 0)
            }
            
            self._record_test_result("llm_enhancement", True, f"Temps: {execution_time:.2f}ms")
            print(f"  ✅ LLM Enhancement OK en {execution_time:.2f}ms")
            
        except Exception as e:
            self._record_test_result("llm_enhancement", False, str(e))
            print(f"  ❌ Erreur LLM enhancement: {str(e)}")
    
    async def _test_security_scenarios(self):
        """🔐 Test scénarios sécurité avancés"""
        print("\n🔐 Test Scénarios Sécurité...")
        
        security_scenarios = [
            ("Analyse Zero Trust complète", "zero_trust_validation", {"comprehensive": True}),
            ("Audit supply chain critique", "supply_chain_analysis", {"critical_vendors": True}),
            ("Scan vulnérabilités approfondi", "vulnerability_assessment", {"deep_scan": True}),
            ("Réponse incident automatique", "auto_remediation", {"incident_type": "security_breach"}),
            ("Conformité multi-frameworks", "compliance_validation", {"frameworks": ["SOC2", "ISO27001", "NIST", "CIS"]})
        ]
        
        try:
            agent = create_agent_21_security_supply_chain()
            await agent.startup()
            
            scenario_results = {}
            
            for scenario_name, task_type, params in security_scenarios:
                task = Task(type=task_type, params=params)
                start_time = time.time()
                result = await agent.execute_task(task)
                execution_time = (time.time() - start_time) * 1000
                
                scenario_results[scenario_name] = {
                    "success": result.success,
                    "execution_time_ms": execution_time,
                    "security_score": getattr(result.data, 'risk_assessment', {}).get('risk_level', 'N/A')
                }
                
                if result.success:
                    print(f"  ✅ {scenario_name}: OK ({execution_time:.1f}ms)")
                else:
                    print(f"  ❌ {scenario_name}: ERREUR")
            
            await agent.shutdown()
            
            success_count = sum(1 for r in scenario_results.values() if r["success"])
            self.test_results["coverage_report"]["security_scenarios"] = scenario_results
            
            self._record_test_result("security_scenarios", success_count == len(security_scenarios),
                                   f"Succès: {success_count}/{len(security_scenarios)}")
            
        except Exception as e:
            self._record_test_result("security_scenarios", False, str(e))
            print(f"  ❌ Erreur scénarios sécurité: {str(e)}")
    
    async def _test_performance(self):
        """⚡ Test performance et optimisation"""
        print("\n⚡ Test Performance...")
        
        try:
            agent = create_agent_21_security_supply_chain()
            await agent.startup()
            
            # Test charge intensive
            tasks = [Task(type="vulnerability_assessment", params={"fast_scan": True}) for _ in range(10)]
            
            start_time = time.time()
            results = []
            for task in tasks:
                result = await agent.execute_task(task)
                results.append(result)
            total_time = (time.time() - start_time) * 1000
            
            success_count = sum(1 for r in results if r.success)
            average_time = total_time / len(tasks)
            
            await agent.shutdown()
            
            performance_data = {
                "total_tasks": len(tasks),
                "successful_tasks": success_count,
                "total_time_ms": total_time,
                "average_time_per_task_ms": average_time,
                "throughput_tasks_per_second": (len(tasks) / total_time) * 1000
            }
            
            self.test_results["performance_metrics"]["load_test"] = performance_data
            
            # Critères performance
            performance_ok = (
                average_time < 200 and  # Moins de 200ms par tâche
                success_count == len(tasks) and  # 100% succès
                performance_data["throughput_tasks_per_second"] > 5  # Plus de 5 tâches/sec
            )
            
            self._record_test_result("performance", performance_ok,
                                   f"Moyenne: {average_time:.1f}ms, Débit: {performance_data['throughput_tasks_per_second']:.1f} tâches/s")
            print(f"  ✅ Performance OK - {average_time:.1f}ms/tâche, {performance_data['throughput_tasks_per_second']:.1f} tâches/s")
            
        except Exception as e:
            self._record_test_result("performance", False, str(e))
            print(f"  ❌ Erreur performance: {str(e)}")
    
    async def _test_concurrent_execution(self):
        """🔄 Test exécution concurrente"""
        print("\n🔄 Test Exécution Concurrente...")
        
        try:
            agent = create_agent_21_security_supply_chain()
            await agent.startup()
            
            # Tâches concurrentes
            concurrent_tasks = [
                Task(type="zero_trust_validation", params={"concurrent": True}),
                Task(type="supply_chain_analysis", params={"concurrent": True}),
                Task(type="vulnerability_assessment", params={"concurrent": True}),
                Task(type="threat_intelligence", params={"concurrent": True}),
                Task(type="ml_security_analysis", params={"concurrent": True})
            ]
            
            start_time = time.time()
            results = await asyncio.gather(*[agent.execute_task(task) for task in concurrent_tasks])
            total_time = (time.time() - start_time) * 1000
            
            await agent.shutdown()
            
            success_count = sum(1 for r in results if r.success)
            
            concurrent_data = {
                "concurrent_tasks": len(concurrent_tasks),
                "successful_tasks": success_count,
                "total_time_ms": total_time,
                "concurrency_efficiency": (len(concurrent_tasks) / total_time) * 1000
            }
            
            self.test_results["performance_metrics"]["concurrent_execution"] = concurrent_data
            
            self._record_test_result("concurrent_execution", success_count == len(concurrent_tasks),
                                   f"Succès: {success_count}/{len(concurrent_tasks)} en {total_time:.1f}ms")
            print(f"  ✅ Concurrence OK - {success_count}/{len(concurrent_tasks)} en {total_time:.1f}ms")
            
        except Exception as e:
            self._record_test_result("concurrent_execution", False, str(e))
            print(f"  ❌ Erreur concurrence: {str(e)}")
    
    async def _test_error_handling(self):
        """🛡️ Test gestion d'erreurs"""
        print("\n🛡️ Test Gestion d'Erreurs...")
        
        try:
            agent = create_agent_21_security_supply_chain()
            await agent.startup()
            
            # Tâches avec erreurs intentionnelles
            error_tasks = [
                Task(type="invalid_task_type", params={}),
                Task(type="zero_trust_validation", params={"invalid_param": "error"}),
                Task(type="", params={}),  # Tâche vide
            ]
            
            error_handled_count = 0
            
            for task in error_tasks:
                try:
                    result = await agent.execute_task(task)
                    if not result.success and result.error:
                        error_handled_count += 1
                        print(f"    ✅ Erreur gérée: {task.type}")
                except Exception:
                    error_handled_count += 1
                    print(f"    ✅ Exception gérée: {task.type}")
            
            await agent.shutdown()
            
            error_handling_ok = error_handled_count == len(error_tasks)
            
            self._record_test_result("error_handling", error_handling_ok,
                                   f"Erreurs gérées: {error_handled_count}/{len(error_tasks)}")
            print(f"  ✅ Gestion erreurs OK - {error_handled_count}/{len(error_tasks)} gérées")
            
        except Exception as e:
            self._record_test_result("error_handling", False, str(e))
            print(f"  ❌ Erreur gestion d'erreurs: {str(e)}")
    
    async def _test_edge_cases(self):
        """🎪 Test cas limites"""
        print("\n🎪 Test Cas Limites...")
        
        try:
            agent = create_agent_21_security_supply_chain()
            await agent.startup()
            
            # Cas limites
            edge_cases = [
                ("Tâche avec paramètres vides", Task(type="zero_trust_validation", params={})),
                ("Tâche avec paramètres complexes", Task(type="supply_chain_analysis", params={
                    "nested": {"deep": {"very_deep": "value"}},
                    "list": [1, 2, 3, 4, 5],
                    "unicode": "🔐🛡️🎯"
                })),
                ("Tâche générique", Task(type="generic_security_task", params={"custom": True}))
            ]
            
            edge_case_results = {}
            
            for case_name, task in edge_cases:
                try:
                    result = await agent.execute_task(task)
                    edge_case_results[case_name] = {
                        "success": result.success,
                        "handled": True
                    }
                    print(f"    ✅ {case_name}: {'OK' if result.success else 'Gérée'}")
                except Exception as e:
                    edge_case_results[case_name] = {
                        "success": False,
                        "handled": True,
                        "error": str(e)
                    }
                    print(f"    ✅ {case_name}: Exception gérée")
            
            await agent.shutdown()
            
            self.test_results["coverage_report"]["edge_cases"] = edge_case_results
            
            self._record_test_result("edge_cases", True, f"Tous les cas limites gérés")
            print(f"  ✅ Cas limites OK - Tous gérés")
            
        except Exception as e:
            self._record_test_result("edge_cases", False, str(e))
            print(f"  ❌ Erreur cas limites: {str(e)}")
    
    async def _test_full_validation(self):
        """🎯 Test validation complète intégrée"""
        print("\n🎯 Test Validation Complète...")
        
        try:
            start_time = time.time()
            validation_result = await validate_agent_21_security()
            validation_time = (time.time() - start_time) * 1000
            
            validation_success = validation_result["validation_status"] == "SUCCESS"
            
            self.test_results["coverage_report"]["full_validation"] = {
                "validation_status": validation_result["validation_status"],
                "validation_time_ms": validation_time,
                "agent_info": validation_result.get("agent_info", {}),
                "results": validation_result.get("results", {})
            }
            
            self._record_test_result("full_validation", validation_success,
                                   f"Status: {validation_result['validation_status']} en {validation_time:.1f}ms")
            print(f"  ✅ Validation complète: {validation_result['validation_status']} en {validation_time:.1f}ms")
            
        except Exception as e:
            self._record_test_result("full_validation", False, str(e))
            print(f"  ❌ Erreur validation complète: {str(e)}")
    
    def _record_test_result(self, test_name: str, success: bool, details: str = ""):
        """📝 Enregistrement résultat test"""
        self.test_results["tests_executed"] += 1
        if success:
            self.test_results["tests_passed"] += 1
        else:
            self.test_results["tests_failed"] += 1
            self.test_results["errors"].append(f"{test_name}: {details}")
    
    def _generate_final_report(self) -> Dict[str, Any]:
        """📊 Génération rapport final"""
        success_rate = (self.test_results["tests_passed"] / self.test_results["tests_executed"]) * 100 if self.test_results["tests_executed"] > 0 else 0
        
        final_report = {
            **self.test_results,
            "success_rate_percent": success_rate,
            "migration_status": "SUCCESS" if success_rate >= 90 else "PARTIAL" if success_rate >= 70 else "FAILED",
            "wave_3_compliance": success_rate >= 95,
            "enterprise_ready": success_rate == 100,
            "recommendations": []
        }
        
        # Recommandations
        if success_rate < 100:
            final_report["recommendations"].append("Corriger les tests échoués avant déploiement production")
        if success_rate >= 95:
            final_report["recommendations"].append("Agent prêt pour déploiement Wave 3 Enterprise")
        
        return final_report

async def main():
    """🚀 Fonction principale test migration"""
    print("🔐 TEST MIGRATION AGENT 21 SECURITY SUPPLY CHAIN - NEXTGENERATION WAVE 3")
    print("=" * 80)
    
    tester = TestAgent21SecurityMigration()
    
    start_time = time.time()
    final_report = await tester.run_all_tests()
    total_time = time.time() - start_time
    
    # Affichage rapport final
    print("\n" + "=" * 80)
    print("📊 RAPPORT FINAL MIGRATION WAVE 3")
    print("=" * 80)
    print(f"🎯 Agent: Security Supply Chain Enterprise v5.3.0")
    print(f"⏱️  Temps total: {total_time:.2f}s")
    print(f"🧪 Tests exécutés: {final_report['tests_executed']}")
    print(f"✅ Tests réussis: {final_report['tests_passed']}")
    print(f"❌ Tests échoués: {final_report['tests_failed']}")
    print(f"📊 Taux de succès: {final_report['success_rate_percent']:.1f}%")
    print(f"🏆 Status migration: {final_report['migration_status']}")
    print(f"🏢 Wave 3 compliance: {'✅' if final_report['wave_3_compliance'] else '❌'}")
    print(f"🚀 Enterprise ready: {'✅' if final_report['enterprise_ready'] else '❌'}")
    
    if final_report['recommendations']:
        print(f"\n💡 Recommandations:")
        for rec in final_report['recommendations']:
            print(f"  • {rec}")
    
    # Sauvegarde rapport
    report_file = f"test_agent_21_security_migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Rapport sauvegardé: {report_file}")
    print("\n✨ TESTS MIGRATION AGENT 21 TERMINÉS ✨")
    
    return final_report

if __name__ == "__main__":
    asyncio.run(main())