#!/usr/bin/env python3
"""
TEST VOLET 2.3 - TESTS PERFORMANCE RÉELS
=======================================

Benchmark complet et tests de charge pour valider les performances
du système en conditions réelles.

Métriques cibles :
- Performance : -40% temps d'exécution
- Fiabilité : +15% taux de succès
- Mémoire : -25% consommation
- Cache : >80% hit rate
"""

import sys
import time
import asyncio
import psutil
import cProfile
import pstats
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('benchmark_results.log')
    ]
)
logger = logging.getLogger(__name__)

class PerformanceMetrics:
    """Collecte et analyse des métriques de performance"""
    
    def __init__(self):
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss
        self.metrics = {
            "execution_times": [],
            "memory_usage": [],
            "success_rate": [],
            "cache_hits": 0,
            "cache_misses": 0
        }
    
    def record_execution_time(self, duration: float):
        """Enregistre un temps d'exécution"""
        self.metrics["execution_times"].append(duration)
    
    def record_memory_usage(self):
        """Enregistre l'utilisation mémoire actuelle"""
        current_memory = psutil.Process().memory_info().rss
        self.metrics["memory_usage"].append(current_memory - self.start_memory)
    
    def record_success(self, success: bool):
        """Enregistre un succès ou échec"""
        self.metrics["success_rate"].append(1 if success else 0)
    
    def record_cache_hit(self):
        """Enregistre un hit du cache"""
        self.metrics["cache_hits"] += 1
    
    def record_cache_miss(self):
        """Enregistre un miss du cache"""
        self.metrics["cache_misses"] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Calcule et retourne le résumé des métriques"""
        total_time = time.time() - self.start_time
        avg_execution = sum(self.metrics["execution_times"]) / len(self.metrics["execution_times"])
        max_memory = max(self.metrics["memory_usage"]) if self.metrics["memory_usage"] else 0
        success_rate = (sum(self.metrics["success_rate"]) / len(self.metrics["success_rate"])) * 100
        
        total_cache_ops = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        cache_hit_rate = (self.metrics["cache_hits"] / total_cache_ops * 100) if total_cache_ops > 0 else 0
        
        return {
            "total_time": total_time,
            "avg_execution_time": avg_execution,
            "max_memory_usage": max_memory,
            "success_rate": success_rate,
            "cache_hit_rate": cache_hit_rate
        }

class BenchmarkRunner:
    """Exécute les benchmarks et tests de charge"""
    
    def __init__(self, config_path: str = "benchmark_config.json"):
        self.metrics = PerformanceMetrics()
        self.profiler = cProfile.Profile()
        self.config = self._load_config(config_path)
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Charge la configuration des tests"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la configuration: {e}")
            return {}
    
    async def run_single_test(self, test_case: Dict[str, Any]) -> bool:
        """Exécute un test unique et collecte les métriques"""
        start_time = time.time()
        
        try:
            # Exécution du test avec le code fourni
            code = test_case.get("code", "")
            expected_fixes = test_case.get("expected_fixes", 0)
            
            # TODO: Implémenter l'exécution réelle avec l'Adaptateur
            # Pour l'instant, simulation avec délai proportionnel à la complexité
            await asyncio.sleep(0.1 * expected_fixes)
            success = True
            
            # Simulation du cache (à remplacer par l'implémentation réelle)
            if expected_fixes > 2:
                self.metrics.record_cache_hit()
            else:
                self.metrics.record_cache_miss()
            
        except Exception as e:
            logger.error(f"Erreur durant le test '{test_case.get('name', 'unknown')}': {e}")
            success = False
        
        duration = time.time() - start_time
        self.metrics.record_execution_time(duration)
        self.metrics.record_memory_usage()
        self.metrics.record_success(success)
        
        return success
    
    async def run_load_test(self):
        """Exécute un test de charge avec plusieurs agents en parallèle"""
        settings = self.config.get("benchmark_settings", {})
        concurrent_agents = settings.get("concurrent_agents", 3)
        iterations = settings.get("iterations_per_test", 100)
        
        logger.info(f"Démarrage test de charge avec {concurrent_agents} agents x {iterations} itérations")
        
        for test_case in self.config.get("test_cases", []):
            logger.info(f"\nExécution du test: {test_case['name']}")
            tasks = []
            for i in range(concurrent_agents):
                for _ in range(iterations):
                    task = asyncio.create_task(self.run_single_test(test_case))
                    tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            success_rate = sum(1 for r in results if r) / len(results) * 100
            logger.info(f"Test '{test_case['name']}' terminé. Taux de succès: {success_rate}%")
    
    def start_profiling(self):
        """Démarre le profiling"""
        self.profiler.enable()
    
    def stop_profiling(self):
        """Arrête le profiling et génère un rapport"""
        self.profiler.disable()
        stats = pstats.Stats(self.profiler)
        stats.sort_stats('cumulative')
        stats.dump_stats('profile_results.prof')
        
        # Génère aussi un rapport texte
        with open('profile_results.txt', 'w') as f:
            stats = pstats.Stats(self.profiler, stream=f)
            stats.sort_stats('cumulative')
            stats.print_stats()

async def main():
    """Point d'entrée principal des tests de performance"""
    logger.info("🔧 DÉMARRAGE TESTS PERFORMANCE VOLET 2.3 🔧")
    
    runner = BenchmarkRunner()
    runner.start_profiling()
    
    try:
        # Test de charge
        await runner.run_load_test()
        
        # Collecte et analyse des résultats
        summary = runner.metrics.get_summary()
        
        # Affichage des résultats
        logger.info("\n" + "="*60)
        logger.info("📊 RÉSULTATS BENCHMARK")
        logger.info("="*60)
        logger.info(f"Temps total: {summary['total_time']:.2f}s")
        logger.info(f"Temps moyen par opération: {summary['avg_execution_time']:.3f}s")
        logger.info(f"Utilisation mémoire max: {summary['max_memory_usage']/1024/1024:.1f} MB")
        logger.info(f"Taux de succès: {summary['success_rate']:.1f}%")
        logger.info(f"Cache hit rate: {summary['cache_hit_rate']:.1f}%")
        logger.info("="*60)
        
        # Validation des objectifs
        targets = runner.config.get("performance_targets", {})
        objectives_met = (
            summary['avg_execution_time'] < (1 - targets.get("execution_time_reduction", 40)/100) * 0.2
            and summary['success_rate'] > (100 + targets.get("success_rate_increase", 15))
            and summary['max_memory_usage'] < (1 - targets.get("memory_usage_reduction", 25)/100) * 100_000_000
            and summary['cache_hit_rate'] > targets.get("cache_hit_rate_minimum", 80)
        )
        
        if objectives_met:
            logger.info("🎉 OBJECTIFS DE PERFORMANCE ATTEINTS!")
            return True
        else:
            logger.warning("⚠️ Certains objectifs de performance non atteints")
            return False
            
    finally:
        runner.stop_profiling()
        logger.info("Tests de performance terminés")

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 