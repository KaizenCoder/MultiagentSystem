#!/usr/bin/env python3
"""
Tests Chaos Engineering - Système Logging NextGeneration
Tests de résilience, haute disponibilité et récupération automatique
"""

import json
import logging
import time
import unittest
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from unittest.mock import Mock, patch
import sys
from pathlib import Path
from core import logging_manager

class ChaosEngineeringTests(unittest.TestCase):
    """Tests de chaos engineering pour le système de logging"""
    
    def setUp(self):
        """Préparation des tests"""
        self.test_dir = tempfile.mkdtemp(prefix="chaos_test_")
        self.manager = LoggingManager()
        self.test_config = {
            "logger_name": "chaos.test",
            "log_level": "INFO",
            "log_dir": self.test_dir,
            "console_enabled": False,
            "file_enabled": True,
            "elasticsearch_enabled": True,
            "encryption_enabled": True,
            "async_enabled": True
        }
        
    def tearDown(self):
        """Nettoyage après tests"""
        try:
            if hasattr(self.manager, 'shutdown'):
                self.manager.shutdown()
            shutil.rmtree(self.test_dir, ignore_errors=True)
        except:
            pass
    
    def test_01_baseline_performance(self):
        """Test 1: Performance de base du système"""
        logger = self.manager.get_logger(custom_config=self.test_config)
        
        start_time = time.time()
        for i in range(100):
            logger.info(f"Baseline test {i}")
        duration = (time.time() - start_time) * 1000
        
        self.assertLess(duration, 1000, "Performance baseline > 1s")
        print(f"✅ Baseline: {duration:.2f}ms pour 100 messages")
    
    def test_02_elasticsearch_failure_resilience(self):
        """Test 2: Résilience aux pannes Elasticsearch"""
        logger = self.manager.get_logger(custom_config=self.test_config)
        
        with patch('logging_manager_optimized.ElasticsearchHandler.emit') as mock_emit:
            mock_emit.side_effect = Exception("Elasticsearch failed")
            
            success_count = 0
            for i in range(50):
                try:
                    logger.warning(f"Message during ES failure {i}")
                    success_count += 1
                except:
                    pass
            
            self.assertGreater(success_count, 40, "Système non résilient aux pannes ES")
            print(f"✅ Résilience ES: {success_count}/50 messages traités")
    
    def test_03_high_volume_stress(self):
        """Test 3: Test de stress haute charge"""
        logger = self.manager.get_logger(custom_config=self.test_config)
        
        def stress_worker(worker_id):
            errors = 0
            for i in range(100):
                try:
                    logger.info(f"Stress T{worker_id}-{i}")
                except:
                    errors += 1
            return errors
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(stress_worker, i) for i in range(5)]
            total_errors = sum(f.result() for f in futures)
        
        duration = time.time() - start_time
        throughput = 500 / duration  # 5 workers * 100 messages
        
        self.assertLess(total_errors / 500, 0.05, "Taux d'erreur > 5%")
        self.assertGreater(throughput, 50, "Débit < 50 msg/s")
        print(f"✅ Stress test: {throughput:.1f} msg/s, {total_errors} erreurs")
    
    def test_04_concurrent_logger_creation(self):
        """Test 4: Création concurrente de loggers"""
        def create_logger(worker_id):
            try:
                config = self.test_config.copy()
                config["logger_name"] = f"concurrent.{worker_id}"
                logger = self.manager.get_logger(custom_config=config)
                logger.info(f"Concurrent test {worker_id}")
                return True
            except:
                return False
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_logger, i) for i in range(10)]
            successes = sum(1 for f in futures if f.result())
        
        self.assertGreaterEqual(successes, 8, "Création concurrente < 80%")
        print(f"✅ Création concurrente: {successes}/10 loggers créés")
    
    def test_05_memory_pressure_resilience(self):
        """Test 5: Résilience sous pression mémoire"""
        logger = self.manager.get_logger(custom_config=self.test_config)
        
        large_data = "X" * 5000  # 5KB par message
        processed = 0
        
        for i in range(100):
            try:
                logger.info(f"Large message {i}", extra={"data": large_data})
                processed += 1
            except MemoryError:
                break
            except:
                pass
        
        self.assertGreater(processed, 80, "Résilience mémoire insuffisante")
        print(f"✅ Pression mémoire: {processed}/100 messages traités")
    
    def test_06_auto_recovery_validation(self):
        """Test 6: Validation récupération automatique"""
        logger = self.manager.get_logger(custom_config=self.test_config)
        
        # Phase normale
        for i in range(10):
            logger.info(f"Normal {i}")
        
        # Phase panne simulée
        with patch('logging_manager_optimized.ElasticsearchHandler.emit', 
                  side_effect=Exception("System failure")):
            for i in range(20):
                try:
                    logger.error(f"During failure {i}")
                except:
                    pass
            time.sleep(1)  # Temps de récupération
        
        # Phase récupération
        recovery_success = 0
        for i in range(10):
            try:
                logger.info(f"Recovery {i}")
                recovery_success += 1
            except:
                pass
        
        self.assertGreater(recovery_success, 8, "Récupération insuffisante")
        print(f"✅ Récupération: {recovery_success}/10 messages après panne")

def run_chaos_tests():
    """Exécute les tests chaos et génère le rapport"""
    print("🚨 DÉMARRAGE TESTS CHAOS ENGINEERING")
    print("=" * 50)
    
    # Exécution des tests
    suite = unittest.TestLoader().loadTestsFromTestCase(ChaosEngineeringTests)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Rapport final
    total_tests = result.testsRun
    failed_tests = len(result.failures) + len(result.errors)
    success_rate = ((total_tests - failed_tests) / total_tests) * 100 if total_tests > 0 else 0
    
    report = {
        "test_suite": "Chaos Engineering - Logging NextGeneration",
        "execution_time": datetime.now().isoformat(),
        "total_tests": total_tests,
        "passed_tests": total_tests - failed_tests,
        "failed_tests": failed_tests,
        "success_rate": success_rate
    }
    
    # Sauvegarde rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"chaos_engineering_report_{timestamp}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 RAPPORT: {report_file}")
    print(f"🎯 RÉSULTATS: {total_tests - failed_tests}/{total_tests} tests réussis ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("✅ SYSTÈME TRÈS RÉSILIENT")
        return 0
    elif success_rate >= 75:
        print("⚠️ SYSTÈME MOYENNEMENT RÉSILIENT")
        return 0
    else:
        print("❌ SYSTÈME PEU RÉSILIENT")
        return 1

if __name__ == "__main__":
    exit(run_chaos_tests())




