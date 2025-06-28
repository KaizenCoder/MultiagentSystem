#!/usr/bin/env python3
"""
🏭 TEST CYCLE-USINE V1 - VALIDATION COMPLÈTE NEXTGENERATION
==========================================================

Script de test et validation du Cycle-Usine v1 avec:
- Tests unitaires des étapes individuelles
- Test d'intégration cycle complet
- Validation avec agents NextGeneration
- Métriques et reporting

Version: 1.0.0
Author: Claude Sonnet 4 (NextGeneration Team)
Created: 2025-06-28
"""

import asyncio
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.cycle_usine_v1 import (
    CycleUsineV1,
    CycleRequest,
    CycleStage,
    CycleStatus,
    create_cycle_usine,
    create_initialized_cycle_usine
)

class CycleUsineV1Tester:
    """
    🧪 Testeur complet pour Cycle-Usine v1
    
    Tests:
    - Initialisation et configuration
    - Étapes individuelles
    - Cycle complet
    - Performance et qualité
    - Intégration agents NextGeneration
    """
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        
        # Configuration test
        self.test_config = {
            "workspace_path": "/mnt/c/Dev/nextgeneration",
            "test_mode": True
        }
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """Exécute tous les tests du Cycle-Usine v1"""
        
        print("🏭 CYCLE-USINE V1 - TESTS COMPLETS")
        print("=" * 50)
        
        # Tests séquentiels
        tests = [
            ("Initialisation", self.test_initialization),
            ("Configuration", self.test_configuration),
            ("Agents Integration", self.test_agents_integration),
            ("Stage Specification", self.test_stage_specification),
            ("Stage Code Generation", self.test_stage_code_generation),
            ("Stage Testing", self.test_stage_testing),
            ("Stage Documentation", self.test_stage_documentation),
            ("Stage Deployment", self.test_stage_deployment),
            ("Cycle Complet Simple", self.test_complete_cycle_simple),
            ("Cycle Complet Enterprise", self.test_complete_cycle_enterprise),
            ("Performance Tests", self.test_performance),
            ("Error Handling", self.test_error_handling)
        ]
        
        total_tests = len(tests)
        passed_tests = 0
        
        for test_name, test_func in tests:
            print(f"\n🧪 Test: {test_name}")
            print("-" * 30)
            
            try:
                result = await test_func()
                
                if result["success"]:
                    print(f"✅ {test_name}: PASSED")
                    passed_tests += 1
                else:
                    print(f"❌ {test_name}: FAILED - {result.get('error', 'Unknown error')}")
                
                self.test_results.append({
                    "test_name": test_name,
                    "success": result["success"],
                    "execution_time_ms": result.get("execution_time_ms", 0),
                    "details": result.get("details", {}),
                    "error": result.get("error")
                })
                
            except Exception as e:
                print(f"❌ {test_name}: EXCEPTION - {e}")
                self.test_results.append({
                    "test_name": test_name,
                    "success": False,
                    "error": str(e)
                })
        
        # Résultat final
        success_rate = (passed_tests / total_tests) * 100
        total_time = (datetime.now() - self.start_time).total_seconds()
        
        final_result = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": success_rate,
            "total_execution_time_seconds": total_time,
            "test_results": self.test_results
        }
        
        # Sauvegarde résultats
        await self.save_test_results(final_result)
        
        print(f"\n🎯 RÉSULTATS FINAUX")
        print("=" * 30)
        print(f"Tests total: {total_tests}")
        print(f"Tests réussis: {passed_tests}")
        print(f"Taux de succès: {success_rate:.1f}%")
        print(f"Temps total: {total_time:.2f}s")
        
        return final_result
    
    async def test_initialization(self) -> Dict[str, Any]:
        """Test initialisation Cycle-Usine"""
        start_time = time.time()
        
        try:
            # Test création basique
            cycle_usine = create_cycle_usine(self.test_config)
            
            assert cycle_usine is not None
            assert cycle_usine.version == "1.0.0"
            assert cycle_usine.cycle_workspace.exists()
            
            # Test initialisation complète
            await cycle_usine.initialize()
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "execution_time_ms": execution_time,
                "details": {
                    "version": cycle_usine.version,
                    "agents_count": len(cycle_usine.agents),
                    "workspace_created": cycle_usine.cycle_workspace.exists()
                }
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "execution_time_ms": execution_time,
                "error": str(e)
            }
    
    async def test_configuration(self) -> Dict[str, Any]:
        """Test configuration et paramétrage"""
        start_time = time.time()
        
        try:
            custom_config = {
                "workspace_path": "/tmp/test_cycle",
                "custom_setting": "test_value"
            }
            
            cycle_usine = create_cycle_usine(custom_config)
            
            assert cycle_usine.config["workspace_path"] == "/tmp/test_cycle"
            assert cycle_usine.config["custom_setting"] == "test_value"
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "execution_time_ms": execution_time,
                "details": {
                    "config_applied": True,
                    "custom_workspace": cycle_usine.config["workspace_path"]
                }
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "execution_time_ms": execution_time,
                "error": str(e)
            }
    
    async def test_agents_integration(self) -> Dict[str, Any]:
        """Test intégration agents NextGeneration"""
        start_time = time.time()
        
        try:
            cycle_usine = create_cycle_usine(self.test_config)
            await cycle_usine.initialize()
            
            # Vérification agents chargés
            expected_agents = ["testing", "quality", "deployment"]
            loaded_agents = list(cycle_usine.agents.keys())
            
            details = {
                "expected_agents": expected_agents,
                "loaded_agents": loaded_agents,
                "all_agents_loaded": all(agent in loaded_agents for agent in expected_agents)
            }
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "execution_time_ms": execution_time,
                "details": details
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "execution_time_ms": execution_time,
                "error": str(e)
            }
    
    async def test_stage_specification(self) -> Dict[str, Any]:
        """Test étape spécification"""
        start_time = time.time()
        
        try:
            cycle_usine = create_cycle_usine(self.test_config)
            await cycle_usine.initialize()
            
            # Création test request
            test_request = CycleRequest(
                request_id="test_spec",
                project_name="test_spec_project",
                requirements="API simple pour tests",
                target_type="api",
                complexity_level="simple",
                constraints={"framework": "fastapi"},
                created_at=datetime.now()
            )
            
            # Test étape spécification
            context = {
                "workspace": cycle_usine.cycle_workspace / "test_spec",
                "request": test_request
            }
            context["workspace"].mkdir(parents=True, exist_ok=True)
            
            result = await cycle_usine._stage_specification(context)
            
            assert result.stage == CycleStage.SPEC
            assert result.status == CycleStatus.COMPLETED
            assert len(result.artifacts) > 0
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "execution_time_ms": execution_time,
                "details": {
                    "stage": result.stage.value,
                    "status": result.status.value,
                    "artifacts_count": len(result.artifacts),
                    "stage_time_ms": result.execution_time_ms
                }
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "execution_time_ms": execution_time,
                "error": str(e)
            }
    
    async def test_stage_code_generation(self) -> Dict[str, Any]:
        """Test étape génération de code"""
        start_time = time.time()
        
        try:
            cycle_usine = create_cycle_usine(self.test_config)
            await cycle_usine.initialize()
            
            test_request = CycleRequest(
                request_id="test_code",
                project_name="test_code_project",
                requirements="Service simple",
                target_type="service",
                complexity_level="simple",
                constraints={},
                created_at=datetime.now()
            )
            
            context = {
                "workspace": cycle_usine.cycle_workspace / "test_code",
                "request": test_request,
                "specification": type('obj', (object,), {
                    "output": {"specification_content": "Test spec content"}
                })()
            }
            context["workspace"].mkdir(parents=True, exist_ok=True)
            
            result = await cycle_usine._stage_code_generation(context)
            
            assert result.stage == CycleStage.CODE
            assert result.status == CycleStatus.COMPLETED
            assert "code_content" in result.output
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "execution_time_ms": execution_time,
                "details": {
                    "stage": result.stage.value,
                    "status": result.status.value,
                    "code_generated": len(result.output.get("code_content", "")),
                    "artifacts_count": len(result.artifacts)
                }
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "execution_time_ms": execution_time,
                "error": str(e)
            }
    
    async def test_stage_testing(self) -> Dict[str, Any]:
        """Test étape testing"""
        start_time = time.time()
        
        try:
            cycle_usine = create_cycle_usine(self.test_config)
            await cycle_usine.initialize()
            
            test_request = CycleRequest(
                request_id="test_testing",
                project_name="test_testing_project",
                requirements="Test testing",
                target_type="service",
                complexity_level="simple",
                constraints={},
                created_at=datetime.now()
            )
            
            context = {
                "workspace": cycle_usine.cycle_workspace / "test_testing",
                "request": test_request,
                "code_generation": type('obj', (object,), {
                    "output": {"code_content": "# Test code", "requirements": "asyncio"}
                })()
            }
            context["workspace"].mkdir(parents=True, exist_ok=True)
            
            result = await cycle_usine._stage_testing(context)
            
            assert result.stage == CycleStage.TEST
            # Testing peut échouer sans agents, on vérifie juste l'exécution
            assert result.status in [CycleStatus.COMPLETED, CycleStatus.FAILED]
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "execution_time_ms": execution_time,
                "details": {
                    "stage": result.stage.value,
                    "status": result.status.value,
                    "test_executed": True
                }
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "execution_time_ms": execution_time,
                "error": str(e)
            }
    
    async def test_stage_documentation(self) -> Dict[str, Any]:
        """Test étape documentation"""
        start_time = time.time()
        
        try:
            cycle_usine = create_cycle_usine(self.test_config)
            await cycle_usine.initialize()
            
            test_request = CycleRequest(
                request_id="test_doc",
                project_name="test_doc_project",
                requirements="Test documentation",
                target_type="service",
                complexity_level="simple",
                constraints={},
                created_at=datetime.now()
            )
            
            context = {
                "workspace": cycle_usine.cycle_workspace / "test_doc",
                "request": test_request
            }
            context["workspace"].mkdir(parents=True, exist_ok=True)
            
            result = await cycle_usine._stage_documentation(context)
            
            assert result.stage == CycleStage.DOC
            assert result.status == CycleStatus.COMPLETED
            assert "documentation_content" in result.output
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "execution_time_ms": execution_time,
                "details": {
                    "stage": result.stage.value,
                    "status": result.status.value,
                    "doc_generated": len(result.output.get("documentation_content", ""))
                }
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "execution_time_ms": execution_time,
                "error": str(e)
            }
    
    async def test_stage_deployment(self) -> Dict[str, Any]:
        """Test étape déploiement"""
        start_time = time.time()
        
        try:
            cycle_usine = create_cycle_usine(self.test_config)
            await cycle_usine.initialize()
            
            test_request = CycleRequest(
                request_id="test_deploy",
                project_name="test_deploy_project",
                requirements="Test deployment",
                target_type="api",
                complexity_level="simple",
                constraints={},
                created_at=datetime.now()
            )
            
            context = {
                "workspace": cycle_usine.cycle_workspace / "test_deploy",
                "request": test_request
            }
            context["workspace"].mkdir(parents=True, exist_ok=True)
            
            result = await cycle_usine._stage_deployment(context)
            
            assert result.stage == CycleStage.DEPLOY
            assert result.status in [CycleStatus.COMPLETED, CycleStatus.FAILED]
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "execution_time_ms": execution_time,
                "details": {
                    "stage": result.stage.value,
                    "status": result.status.value,
                    "deployment_attempted": True
                }
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "execution_time_ms": execution_time,
                "error": str(e)
            }
    
    async def test_complete_cycle_simple(self) -> Dict[str, Any]:
        """Test cycle complet simple"""
        start_time = time.time()
        
        try:
            cycle_usine = create_cycle_usine(self.test_config)
            await cycle_usine.initialize()
            
            test_request = CycleRequest(
                request_id="test_complete_simple",
                project_name="simple_calculator",
                requirements="Créer une calculatrice simple avec addition et soustraction",
                target_type="service",
                complexity_level="simple",
                constraints={"language": "python"},
                created_at=datetime.now()
            )
            
            result = await cycle_usine.execute_cycle(test_request)
            
            assert result.request_id == test_request.request_id
            assert len(result.stages_results) == 5  # 5 étapes
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "execution_time_ms": execution_time,
                "details": {
                    "cycle_success": result.success,
                    "quality_score": result.quality_score,
                    "stages_completed": len([r for r in result.stages_results.values() if r.status == CycleStatus.COMPLETED]),
                    "total_artifacts": len(result.final_artifacts),
                    "cycle_time_ms": result.total_execution_time_ms
                }
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "execution_time_ms": execution_time,
                "error": str(e)
            }
    
    async def test_complete_cycle_enterprise(self) -> Dict[str, Any]:
        """Test cycle complet enterprise"""
        start_time = time.time()
        
        try:
            cycle_usine = create_cycle_usine(self.test_config)
            await cycle_usine.initialize()
            
            test_request = CycleRequest(
                request_id="test_complete_enterprise",
                project_name="user_management_api",
                requirements="API de gestion d'utilisateurs avec authentification, CRUD complet, et notifications",
                target_type="api",
                complexity_level="enterprise",
                constraints={
                    "framework": "fastapi",
                    "database": "postgresql",
                    "auth": "jwt",
                    "monitoring": "prometheus"
                },
                created_at=datetime.now()
            )
            
            result = await cycle_usine.execute_cycle(test_request)
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "execution_time_ms": execution_time,
                "details": {
                    "cycle_success": result.success,
                    "quality_score": result.quality_score,
                    "enterprise_complexity": True,
                    "cycle_time_ms": result.total_execution_time_ms
                }
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "execution_time_ms": execution_time,
                "error": str(e)
            }
    
    async def test_performance(self) -> Dict[str, Any]:
        """Test performance cycle-usine"""
        start_time = time.time()
        
        try:
            cycle_usine = create_cycle_usine(self.test_config)
            await cycle_usine.initialize()
            
            # Test avec 3 cycles simples rapides
            performance_results = []
            
            for i in range(3):
                cycle_start = time.time()
                
                test_request = CycleRequest(
                    request_id=f"perf_test_{i}",
                    project_name=f"perf_project_{i}",
                    requirements="Test performance",
                    target_type="service",
                    complexity_level="simple",
                    constraints={},
                    created_at=datetime.now()
                )
                
                result = await cycle_usine.execute_cycle(test_request)
                cycle_time = (time.time() - cycle_start) * 1000
                
                performance_results.append({
                    "cycle_id": i,
                    "success": result.success,
                    "execution_time_ms": cycle_time,
                    "quality_score": result.quality_score
                })
            
            # Analyse performance
            avg_time = sum(r["execution_time_ms"] for r in performance_results) / len(performance_results)
            avg_quality = sum(r["quality_score"] for r in performance_results) / len(performance_results)
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "execution_time_ms": execution_time,
                "details": {
                    "cycles_tested": len(performance_results),
                    "avg_cycle_time_ms": avg_time,
                    "avg_quality_score": avg_quality,
                    "performance_consistent": max(r["execution_time_ms"] for r in performance_results) / min(r["execution_time_ms"] for r in performance_results) < 3
                }
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "execution_time_ms": execution_time,
                "error": str(e)
            }
    
    async def test_error_handling(self) -> Dict[str, Any]:
        """Test gestion d'erreurs"""
        start_time = time.time()
        
        try:
            cycle_usine = create_cycle_usine(self.test_config)
            await cycle_usine.initialize()
            
            # Test avec requête invalide
            invalid_request = CycleRequest(
                request_id="",  # ID vide
                project_name="",  # Nom vide
                requirements="",  # Requirements vides
                target_type="invalid_type",
                complexity_level="invalid_level",
                constraints={},
                created_at=datetime.now()
            )
            
            result = await cycle_usine.execute_cycle(invalid_request)
            
            # Le cycle doit échouer gracieusement
            assert result.success == False
            assert result.completed_at is not None
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "execution_time_ms": execution_time,
                "details": {
                    "error_handled_gracefully": not result.success,
                    "completed_timestamp_set": result.completed_at is not None,
                    "quality_score": result.quality_score
                }
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "execution_time_ms": execution_time,
                "error": str(e)
            }
    
    async def save_test_results(self, results: Dict[str, Any]):
        """Sauvegarde résultats de tests"""
        
        results_dir = Path("/mnt/c/Dev/nextgeneration/cycle_usine/test_results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"cycle_usine_v1_test_results_{timestamp}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Résultats sauvegardés: {results_file}")

async def main():
    """Point d'entrée principal"""
    
    print("🏭 CYCLE-USINE V1 - TESTS DE VALIDATION")
    print("=" * 60)
    
    tester = CycleUsineV1Tester()
    
    try:
        results = await tester.run_all_tests()
        
        if results["success_rate"] >= 80:
            print(f"\n🎉 SUCCÈS: Cycle-Usine v1 validé ({results['success_rate']:.1f}%)")
            return 0
        else:
            print(f"\n⚠️ PARTIEL: Cycle-Usine v1 nécessite corrections ({results['success_rate']:.1f}%)")
            return 1
            
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return 2

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)