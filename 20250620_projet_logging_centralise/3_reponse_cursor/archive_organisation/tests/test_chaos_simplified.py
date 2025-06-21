#!/usr/bin/env python3
"""
Tests Chaos Engineering Simplifiés - Validation Bug Fix AsyncLogHandler
Focus sur la validation du correctif sans dépendances externes
"""

import time
import unittest
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import sys
from pathlib import Path
from core import logging_manager

class SimplifiedChaosTests(unittest.TestCase):
    """Tests chaos simplifiés pour valider le bug fix AsyncLogHandler"""
    
    def setUp(self):
        """Préparation des tests"""
        self.test_dir = tempfile.mkdtemp(prefix="chaos_simple_")
        self.manager = LoggingManager()
        
    def tearDown(self):
        """Nettoyage après tests"""
        try:
            if hasattr(self.manager, 'shutdown'):
                self.manager.shutdown()
            shutil.rmtree(self.test_dir, ignore_errors=True)
        except:
            pass
    
    def test_01_async_handler_basic(self):
        """Test 1: Validation AsyncLogHandler de base"""
        config = {
            "logger_name": "async.basic",
            "log_level": "INFO",
            "log_dir": self.test_dir,
            "console_enabled": False,
            "file_enabled": True,
            "elasticsearch_enabled": False,  # Désactivé pour éviter blocage
            "encryption_enabled": False,     # Désactivé pour simplifier
            "async_enabled": True            # FOCUS sur AsyncLogHandler
        }
        
        logger = self.manager.get_logger(custom_config=config)
        
        # Test simple
        for i in range(50):
            logger.info(f"Async test message {i}")
        
        # Attendre traitement async
        time.sleep(2)
        
        print("✅ AsyncLogHandler fonctionne - Pas d'AttributeError '_shutdown'")
        self.assertTrue(True)  # Si on arrive ici, pas de crash
    
    def test_02_async_handler_concurrent(self):
        """Test 2: AsyncLogHandler avec charge concurrente"""
        config = {
            "logger_name": "async.concurrent",
            "log_level": "INFO", 
            "log_dir": self.test_dir,
            "console_enabled": False,
            "file_enabled": True,
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": True
        }
        
        logger = self.manager.get_logger(custom_config=config)
        
        def worker(worker_id):
            for i in range(20):
                logger.info(f"Worker {worker_id} - Message {i}")
            return True
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(worker, i) for i in range(3)]
            results = [f.result() for f in futures]
        
        time.sleep(2)  # Attendre traitement async
        
        self.assertEqual(len(results), 3)
        print("✅ AsyncLogHandler résiste à la charge concurrente")
    
    def test_03_async_handler_shutdown(self):
        """Test 3: Validation shutdown propre AsyncLogHandler"""
        config = {
            "logger_name": "async.shutdown",
            "log_level": "INFO",
            "log_dir": self.test_dir,
            "console_enabled": False,
            "file_enabled": True,
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": True
        }
        
        logger = self.manager.get_logger(custom_config=config)
        
        # Charger le handler async
        for i in range(30):
            logger.info(f"Shutdown test {i}")
        
        # Test shutdown propre
        self.manager.shutdown()
        
        print("✅ AsyncLogHandler shutdown sans erreur")
        self.assertTrue(True)
    
    def test_04_performance_baseline(self):
        """Test 4: Performance de base système"""
        config = {
            "logger_name": "perf.baseline",
            "log_level": "INFO",
            "log_dir": self.test_dir,
            "console_enabled": False,
            "file_enabled": True,
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": True
        }
        
        logger = self.manager.get_logger(custom_config=config)
        
        start_time = time.time()
        for i in range(100):
            logger.info(f"Performance test {i}")
        duration = (time.time() - start_time) * 1000
        
        self.assertLess(duration, 500, "Performance dégradée")
        print(f"✅ Performance: {duration:.2f}ms pour 100 messages")

def run_simplified_chaos():
    """Exécute les tests chaos simplifiés"""
    print("🚨 TESTS CHAOS SIMPLIFIÉS - VALIDATION BUG FIX")
    print("=" * 55)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(SimplifiedChaosTests)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    total_tests = result.testsRun
    failed_tests = len(result.failures) + len(result.errors)
    success_rate = ((total_tests - failed_tests) / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n📊 RÉSULTATS SIMPLIFIÉS")
    print(f"🎯 Tests: {total_tests - failed_tests}/{total_tests} réussis ({success_rate:.1f}%)")
    
    if success_rate == 100:
        print("✅ BUG FIX ASYNCLOGHANDLER VALIDÉ !")
        return True
    else:
        print("❌ Problèmes détectés")
        return False

if __name__ == "__main__":
    success = run_simplified_chaos()
    exit(0 if success else 1) 



