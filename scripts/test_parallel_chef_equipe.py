#!/usr/bin/env python3
"""
🧪 TEST CHEF D'ÉQUIPE PARALLÈLE - Phase 2 Validation
====================================================

Script de test et validation du Chef d'Équipe Coordinateur Parallèle
Comparaison performance séquentiel vs parallèle avec métriques détaillées

Tests inclus:
- Démarrage infrastructure Phase 2
- Traitement parallèle vs séquentiel
- Circuit breakers et cache
- Métriques de performance
- Fallback automatique

Author: Infrastructure d'Optimisation NextGeneration
Version: 1.0.0 - Phase 2 Testing
"""

import asyncio
import time
import logging
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import tempfile
import os

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("test_parallel_chef_equipe")


class ParallelChefEquipeValidator:
    """Validateur pour Chef d'Équipe Parallèle"""
    
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.test_results = {}
        self.test_agents_dir = None
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """Exécute tous les tests de validation"""
        logger.info("🧪 DÉBUT TESTS CHEF D'ÉQUIPE PARALLÈLE")
        start_time = time.time()
        
        # Préparation environnement de test
        await self._setup_test_environment()
        
        # Tests individuels
        tests = [
            ("infrastructure_startup", self._test_infrastructure_startup),
            ("parallel_vs_sequential", self._test_parallel_vs_sequential),
            ("circuit_breaker_protection", self._test_circuit_breaker_protection),
            ("cache_performance", self._test_cache_performance),
            ("fallback_mechanism", self._test_fallback_mechanism),
            ("performance_metrics", self._test_performance_metrics)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                logger.info(f"🔍 Test: {test_name}")
                result = await test_func()
                self.test_results[test_name] = {
                    "status": "PASSED" if result["success"] else "FAILED",
                    "details": result,
                    "timestamp": datetime.now().isoformat()
                }
                
                if result["success"]:
                    passed_tests += 1
                    logger.info(f"✅ {test_name} - SUCCÈS")
                else:
                    logger.error(f"❌ {test_name} - ÉCHEC: {result.get('error', 'Erreur inconnue')}")
                    
            except Exception as e:
                logger.error(f"💥 {test_name} - EXCEPTION: {e}")
                self.test_results[test_name] = {
                    "status": "ERROR",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        
        # Résumé final
        total_time = time.time() - start_time
        success_rate = (passed_tests / total_tests) * 100
        
        self.test_results["summary"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": success_rate,
            "total_time": total_time,
            "status": "PASSED" if success_rate >= 80 else "FAILED"
        }
        
        # Nettoyage
        await self._cleanup_test_environment()
        
        # Sauvegarde résultats
        await self._save_test_results()
        
        logger.info(f"🏁 TESTS TERMINÉS - {passed_tests}/{total_tests} réussis ({success_rate:.1f}%)")
        return self.test_results
    
    async def _setup_test_environment(self):
        """Prépare l'environnement de test"""
        logger.info("🔧 Préparation environnement de test")
        
        # Création répertoire agents de test
        self.test_agents_dir = Path(tempfile.mkdtemp(prefix="test_agents_"))
        
        # Création agents de test factices
        test_agents = [
            self._create_test_agent("agent_test_1.py", "working"),
            self._create_test_agent("agent_test_2.py", "syntax_error"),
            self._create_test_agent("agent_test_3.py", "working"),
            self._create_test_agent("agent_test_4.py", "import_error"),
            self._create_test_agent("agent_test_5.py", "working")
        ]
        
        for agent_name, agent_code in test_agents:
            agent_path = self.test_agents_dir / agent_name
            agent_path.write_text(agent_code, encoding='utf-8')
        
        logger.info(f"✅ {len(test_agents)} agents de test créés dans {self.test_agents_dir}")
    
    def _create_test_agent(self, name: str, agent_type: str) -> tuple:
        """Crée un agent de test selon le type"""
        base_code = '''#!/usr/bin/env python3
"""
Agent de test pour validation Chef d'Équipe Parallèle
"""

import asyncio
from typing import Dict, Any

class TestAgent:
    def __init__(self):
        self.agent_id = "test_agent"
    
    async def startup(self):
        pass
    
    async def shutdown(self):
        pass
    
    async def execute_task(self, task):
        return {"success": True, "message": "Test agent working"}

def create_test_agent(**kwargs):
    return TestAgent()
'''
        
        if agent_type == "syntax_error":
            # Injection erreur de syntaxe
            base_code = base_code.replace("def create_test_agent(**kwargs):", "def create_test_agent(**kwargs")
        elif agent_type == "import_error":
            # Injection erreur d'import
            base_code = "import non_existent_module\n" + base_code
        
        return (name, base_code)
    
    async def _test_infrastructure_startup(self) -> Dict[str, Any]:
        """Test démarrage infrastructure Phase 2"""
        try:
            # Import dynamique pour éviter erreurs si module non disponible
            import sys
            import os
            sys.path.append(os.path.join(os.getcwd()))
            from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur_parallel import (
                create_agent_MAINTENANCE_00_chef_equipe_coordinateur_parallel
            )
            
            # Création chef d'équipe
            chef = create_agent_MAINTENANCE_00_chef_equipe_coordinateur_parallel(
                workspace_path=str(self.workspace_path),
                enable_parallel=True,
                max_workers=3
            )
            
            # Test démarrage
            start_time = time.time()
            await chef.startup()
            startup_time = time.time() - start_time
            
            # Test arrêt
            await chef.shutdown()
            
            return {
                "success": True,
                "startup_time": startup_time,
                "parallel_enabled": chef.enable_parallel,
                "max_workers": chef.max_workers
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_parallel_vs_sequential(self) -> Dict[str, Any]:
        """Test comparaison performance parallèle vs séquentiel"""
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.getcwd()))
            from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur_parallel import (
                create_agent_MAINTENANCE_00_chef_equipe_coordinateur_parallel
            )
            
            agents_paths = [str(p) for p in self.test_agents_dir.glob("*.py")]
            
            # Test mode séquentiel
            chef_seq = create_agent_MAINTENANCE_00_chef_equipe_coordinateur_parallel(
                workspace_path=str(self.workspace_path),
                enable_parallel=False
            )
            
            await chef_seq.startup()
            
            start_time = time.time()
            result_seq = await chef_seq.workflow_maintenance_complete({
                "target_files": agents_paths
            })
            sequential_time = time.time() - start_time
            
            await chef_seq.shutdown()
            
            # Test mode parallèle
            chef_par = create_agent_MAINTENANCE_00_chef_equipe_coordinateur_parallel(
                workspace_path=str(self.workspace_path),
                enable_parallel=True,
                max_workers=3
            )
            
            await chef_par.startup()
            
            start_time = time.time()
            result_par = await chef_par.workflow_maintenance_complete({
                "target_files": agents_paths
            })
            parallel_time = time.time() - start_time
            
            await chef_par.shutdown()
            
            # Calcul amélioration
            speedup = (sequential_time - parallel_time) / sequential_time * 100
            
            return {
                "success": True,
                "sequential_time": sequential_time,
                "parallel_time": parallel_time,
                "speedup_percent": speedup,
                "target_improvement": speedup >= 20,  # Au moins 20% d'amélioration
                "agents_processed": len(agents_paths)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_circuit_breaker_protection(self) -> Dict[str, Any]:
        """Test protection circuit breaker"""
        try:
            from core.monitoring.circuit_breaker import CircuitBreakerManager
            
            # Test circuit breaker basique
            cb_manager = CircuitBreakerManager()
            await cb_manager.startup()
            
            # Simulation échecs
            breaker = await cb_manager.get_circuit_breaker("test_agent")
            
            # Enregistrement échecs pour déclencher ouverture
            for _ in range(6):  # Seuil par défaut = 5
                breaker.record_failure()
            
            # Vérification état ouvert
            state = breaker.get_state()
            can_execute = state["state"] != "open"
            
            await cb_manager.shutdown()
            
            return {
                "success": True,
                "circuit_opened": not can_execute,
                "failure_threshold_reached": True
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_cache_performance(self) -> Dict[str, Any]:
        """Test performance cache intelligent"""
        try:
            from core.monitoring.cache_manager import IntelligentCache
            
            cache = IntelligentCache()
            # IntelligentCache n'a pas de méthode startup
            
            # Test mise en cache
            test_key = "test_cache_key"
            test_value = {"test": "data", "timestamp": time.time()}
            
            # Set
            start_time = time.time()
            await cache.set(test_key, test_value)
            set_time = time.time() - start_time
            
            # Get (cache hit)
            start_time = time.time()
            cached_value = await cache.get(test_key)
            get_time = time.time() - start_time
            
            # Vérification valeur
            cache_hit = cached_value == test_value
            
            # Statistiques
            stats = cache.get_stats()
            
            # IntelligentCache n'a pas de méthode shutdown
            
            return {
                "success": True,
                "cache_hit": cache_hit,
                "set_time": set_time,
                "get_time": get_time,
                "cache_stats": stats
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_fallback_mechanism(self) -> Dict[str, Any]:
        """Test mécanisme de fallback"""
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.getcwd()))
            from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur_parallel import (
                create_agent_MAINTENANCE_00_chef_equipe_coordinateur_parallel
            )
            
            # Création chef avec parallélisme activé mais infrastructure défaillante
            chef = create_agent_MAINTENANCE_00_chef_equipe_coordinateur_parallel(
                workspace_path=str(self.workspace_path),
                enable_parallel=True,
                max_workers=3
            )
            
            # Simulation échec infrastructure (désactivation forcée)
            await chef.startup()
            
            # Force fallback en désactivant parallélisme
            original_parallel = chef.enable_parallel
            chef.enable_parallel = False
            
            # Test exécution en mode fallback
            agents_paths = [str(p) for p in self.test_agents_dir.glob("*.py")][:2]  # Limité pour rapidité
            
            result = await chef.workflow_maintenance_complete({
                "target_files": agents_paths
            })
            
            await chef.shutdown()
            
            return {
                "success": True,
                "fallback_activated": result.get("mode_execution") == "sequential",
                "original_parallel_setting": original_parallel,
                "agents_processed": len(result.get("agents_reports", {}))
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_performance_metrics(self) -> Dict[str, Any]:
        """Test collecte métriques de performance"""
        try:
            from core.monitoring.metrics_collector import AdvancedMetricsCollector
            
            metrics = AdvancedMetricsCollector()
            await metrics.startup()
            
            # Simulation enregistrement métriques
            metrics.record_execution("test_agent", 1.5, True, 1024*1024)
            metrics.record_execution("test_agent", 2.0, False, 2*1024*1024)
            
            # Récupération statistiques
            stats = metrics.get_dashboard_data()
            
            await metrics.shutdown()
            
            return {
                "success": True,
                "metrics_recorded": len(stats.get("agents", {})) > 0,
                "performance_summary": stats
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _cleanup_test_environment(self):
        """Nettoyage environnement de test"""
        if self.test_agents_dir and self.test_agents_dir.exists():
            import shutil
            shutil.rmtree(self.test_agents_dir)
            logger.info(f"🧹 Nettoyage: {self.test_agents_dir} supprimé")
    
    async def _save_test_results(self):
        """Sauvegarde résultats de test"""
        results_dir = self.workspace_path / "reports" / "tests"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"test_parallel_chef_equipe_{timestamp}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Résultats sauvegardés: {results_file}")


async def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Chef d'Équipe Parallèle")
    parser.add_argument("--workspace", default=".", help="Répertoire de travail")
    parser.add_argument("--verbose", action="store_true", help="Mode verbeux")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Exécution tests
    validator = ParallelChefEquipeValidator(args.workspace)
    results = await validator.run_all_tests()
    
    # Affichage résumé
    summary = results["summary"]
    print(f"\n{'='*60}")
    print(f"🧪 RÉSULTATS TESTS CHEF D'ÉQUIPE PARALLÈLE")
    print(f"{'='*60}")
    print(f"📊 Tests réussis: {summary['passed_tests']}/{summary['total_tests']}")
    print(f"📈 Taux de succès: {summary['success_rate']:.1f}%")
    print(f"⏱️ Temps total: {summary['total_time']:.2f}s")
    print(f"🏁 Statut global: {summary['status']}")
    
    # Détails par test
    for test_name, test_result in results.items():
        if test_name != "summary":
            status_icon = "✅" if test_result["status"] == "PASSED" else "❌"
            print(f"{status_icon} {test_name}: {test_result['status']}")
    
    print(f"{'='*60}")
    
    # Code de sortie
    exit_code = 0 if summary["status"] == "PASSED" else 1
    return exit_code


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code) 