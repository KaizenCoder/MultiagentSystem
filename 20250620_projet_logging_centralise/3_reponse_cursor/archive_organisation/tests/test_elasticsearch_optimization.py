#!/usr/bin/env python3
"""
Tests pour l'optimisation du cache Elasticsearch - PHASE 3
Validation des fonctionnalités de cache intelligent, compression et connection pooling
"""

import unittest
import logging
import time
import threading
from datetime import datetime
from logging_manager_optimized import (
    LoggingManager, LoggingConfig, ElasticsearchHandler
)

class TestElasticsearchOptimization(unittest.TestCase):
    """Tests pour l'optimisation Elasticsearch"""
    
    def setUp(self):
        """Configuration des tests"""
        self.manager = LoggingManager()
        self.test_start_time = time.time()
        
    def tearDown(self):
        """Nettoyage après tests"""
        self.manager.shutdown()
        
    def test_01_elasticsearch_handler_optimized(self):
        """Test 1: Handler Elasticsearch optimisé avec cache et compression"""
        print("\n🧪 Test 1: Handler Elasticsearch optimisé")
        
        # Créer handler avec optimisations
        handler = ElasticsearchHandler(
            host="localhost:9200",
            index="test-nextgen-logs",
            batch_size=5,  # Petit batch pour tests
            cache_enabled=True,
            cache_size=100,
            compression_enabled=True,
            connection_pool_size=3
        )
        
        # Créer des logs de test
        logger = logging.getLogger("test.elasticsearch.optimized")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        
        # Générer des logs variés
        test_messages = [
            "Message de test standard",
            "Erreur de connexion à la base de données",
            "Performance alert: slow query detected",
            "Message de test standard",  # Duplicata pour tester le cache
            "User authentication successful",
            "Message de test standard",  # Autre duplicata
            "System maintenance scheduled",
            "Performance alert: slow query detected"  # Duplicata
        ]
        
        # Envoyer les logs
        for i, message in enumerate(test_messages):
            logger.info(f"{message} - ID:{i}")
            time.sleep(0.1)  # Petit délai pour simuler l'activité
        
        # Forcer le flush
        handler._flush_batch()
        
        # Vérifier les métriques
        metrics = handler.get_performance_metrics()
        
        print(f"  📊 Documents envoyés: {metrics['documents_sent']}")
        print(f"  📦 Batches envoyés: {metrics['batches_sent']}")
        print(f"  🎯 Cache hits: {metrics['cache_hits']}")
        print(f"  ❌ Cache misses: {metrics['cache_misses']}")
        print(f"  🗜️  Ratio compression: {metrics.get('compression_ratio', 0):.3f}")
        print(f"  🔗 Connexions actives: {metrics['active_connections']}")
        
        # Assertions
        self.assertGreater(metrics['documents_sent'], 0, "Aucun document envoyé")
        self.assertGreater(metrics['batches_sent'], 0, "Aucun batch envoyé")
        self.assertTrue(metrics['cache_enabled'], "Cache non activé")
        self.assertGreaterEqual(metrics['cache_hits'], 2, "Cache hits insuffisants")
        self.assertEqual(metrics['total_connections'], 3, "Pool de connexions incorrect")
        
        print("  ✅ Test handler optimisé réussi")
        
    def test_02_cache_efficiency(self):
        """Test 2: Efficacité du cache intelligent"""
        print("\n🧪 Test 2: Efficacité du cache intelligent")
        
        handler = ElasticsearchHandler(
            host="localhost:9200",
            index="test-cache-efficiency",
            batch_size=3,
            cache_enabled=True,
            cache_size=50,
            compression_enabled=False  # Désactiver pour se concentrer sur le cache
        )
        
        logger = logging.getLogger("test.cache.efficiency")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        
        # Test avec messages répétitifs
        repeated_message = "Message répétitif pour test cache"
        unique_messages = [
            "Message unique 1",
            "Message unique 2", 
            "Message unique 3"
        ]
        
        # Envoyer des messages répétitifs (devrait être mis en cache)
        for i in range(5):
            logger.info(repeated_message)
            time.sleep(0.05)
        
        # Envoyer des messages uniques
        for msg in unique_messages:
            logger.info(msg)
            time.sleep(0.05)
        
        # Envoyer encore le message répétitif
        for i in range(3):
            logger.info(repeated_message)
            time.sleep(0.05)
        
        handler._flush_batch()
        
        # Vérifier les métriques de cache
        cache_metrics = handler.get_cache_metrics()
        
        print(f"  📊 Taille cache: {cache_metrics['cache_size']}")
        print(f"  🎯 Cache hits: {cache_metrics['cache_hits']}")
        print(f"  ❌ Cache misses: {cache_metrics['cache_misses']}")
        print(f"  📈 Taux de hit: {cache_metrics['cache_hit_rate']:.1f}%")
        print(f"  💾 Utilisation cache: {cache_metrics['cache_utilization']:.1f}%")
        
        # Assertions sur l'efficacité du cache
        self.assertGreater(cache_metrics['cache_hits'], 5, "Pas assez de cache hits")
        self.assertGreater(cache_metrics['cache_hit_rate'], 50, "Taux de hit trop faible")
        self.assertLess(cache_metrics['cache_utilization'], 100, "Cache débordé")
        
        print("  ✅ Test efficacité cache réussi")
        
    def test_03_compression_performance(self):
        """Test 3: Performance de compression"""
        print("\n🧪 Test 3: Performance de compression")
        
        handler = ElasticsearchHandler(
            host="localhost:9200",
            index="test-compression",
            batch_size=4,
            cache_enabled=False,  # Désactiver pour se concentrer sur compression
            compression_enabled=True
        )
        
        logger = logging.getLogger("test.compression.performance")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        
        # Générer des logs avec beaucoup de texte répétitif (bon pour compression)
        long_messages = [
            "ERREUR CRITIQUE: " + "Système en panne " * 20,
            "ALERTE PERFORMANCE: " + "Requête lente détectée " * 15,
            "INFO SYSTÈME: " + "Opération normale en cours " * 25,
            "DEBUG VERBOSE: " + "Trace détaillée du processus " * 30
        ]
        
        # Envoyer les messages longs
        for msg in long_messages:
            logger.info(msg)
            time.sleep(0.1)
        
        handler._flush_batch()
        
        # Vérifier les métriques de compression
        perf_metrics = handler.get_performance_metrics()
        
        print(f"  📦 Bytes originaux: {perf_metrics['total_bytes_sent']}")
        print(f"  🗜️  Bytes compressés: {perf_metrics['total_bytes_compressed']}")
        print(f"  📉 Ratio compression: {perf_metrics.get('compression_ratio', 0):.3f}")
        print(f"  💾 Efficacité: {perf_metrics.get('compression_efficiency_percent', 0):.1f}%")
        
        # Assertions sur la compression
        self.assertGreater(perf_metrics['total_bytes_sent'], 0, "Aucun byte envoyé")
        self.assertGreater(perf_metrics['total_bytes_compressed'], 0, "Aucun byte compressé")
        self.assertLess(perf_metrics['total_bytes_compressed'], perf_metrics['total_bytes_sent'], "Compression inefficace")
        
        # La compression devrait être efficace avec du texte répétitif
        compression_efficiency = perf_metrics.get('compression_efficiency_percent', 0)
        self.assertGreater(compression_efficiency, 30, f"Compression trop faible: {compression_efficiency}%")
        
        print("  ✅ Test compression réussi")
        
    def test_04_connection_pool_management(self):
        """Test 4: Gestion du pool de connexions"""
        print("\n🧪 Test 4: Gestion du pool de connexions")
        
        handler = ElasticsearchHandler(
            host="localhost:9200",
            index="test-connection-pool",
            batch_size=2,
            connection_pool_size=4
        )
        
        # Tester l'utilisation concurrent du pool
        def worker_thread(thread_id):
            logger = logging.getLogger(f"test.pool.worker.{thread_id}")
            logger.setLevel(logging.INFO)
            logger.addHandler(handler)
            
            for i in range(3):
                logger.info(f"Message du thread {thread_id} - {i}")
                time.sleep(0.1)
        
        # Créer plusieurs threads pour tester le pool
        threads = []
        for i in range(6):  # Plus de threads que de connexions
            thread = threading.Thread(target=worker_thread, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Attendre tous les threads
        for thread in threads:
            thread.join()
        
        handler._flush_batch()
        
        # Vérifier les métriques du pool
        pool_metrics = handler.get_performance_metrics()
        
        print(f"  🔗 Connexions totales: {pool_metrics['total_connections']}")
        print(f"  ✅ Connexions actives: {pool_metrics['active_connections']}")
        print(f"  📊 Utilisation pool: {pool_metrics.get('connection_pool_utilization', 0):.1f}%")
        print(f"  🔄 Utilisations pool: {pool_metrics['connection_pool_usage']}")
        
        # Assertions sur le pool
        self.assertEqual(pool_metrics['total_connections'], 4, "Nombre de connexions incorrect")
        self.assertGreater(pool_metrics['connection_pool_usage'], 6, "Pool pas assez utilisé")
        self.assertLessEqual(pool_metrics['active_connections'], 4, "Trop de connexions actives")
        
        print("  ✅ Test pool de connexions réussi")
        
    def test_05_integration_logging_manager(self):
        """Test 5: Intégration avec LoggingManager"""
        print("\n🧪 Test 5: Intégration avec LoggingManager")
        
        # Configuration avec Elasticsearch optimisé
        config = {
            "logger_name": "nextgen.test.elasticsearch.integration",
            "elasticsearch_enabled": True,
            "elasticsearch_host": "localhost:9200",
            "elasticsearch_index": "test-integration",
            "elasticsearch_cache_enabled": True,
            "elasticsearch_cache_size": 200,
            "elasticsearch_compression_enabled": True,
            "elasticsearch_connection_pool_size": 2
        }
        
        logger = self.manager.get_logger(custom_config=config)
        
        # Générer des logs de test
        test_scenarios = [
            ("INFO", "Démarrage application"),
            ("WARNING", "Mémoire faible détectée"),
            ("ERROR", "Erreur de connexion"),
            ("INFO", "Démarrage application"),  # Duplicata
            ("DEBUG", "Trace détaillée"),
            ("WARNING", "Mémoire faible détectée"),  # Duplicata
            ("CRITICAL", "Système critique")
        ]
        
        for level, message in test_scenarios:
            getattr(logger, level.lower())(message)
            time.sleep(0.05)
        
        # Attendre un peu pour le traitement
        time.sleep(0.5)
        
        # Vérifier les métriques Elasticsearch via le manager
        es_metrics = self.manager.get_elasticsearch_metrics()
        
        print(f"  🔌 Optimisation activée: {es_metrics['elasticsearch_optimization']}")
        print(f"  📊 Handlers Elasticsearch: {es_metrics['total_elasticsearch_handlers']}")
        
        if es_metrics['elasticsearch_optimization']:
            agg_metrics = es_metrics.get('aggregated_elasticsearch_metrics', {})
            print(f"  📤 Documents envoyés: {agg_metrics.get('total_documents_sent', 0)}")
            print(f"  🎯 Taux cache hit: {agg_metrics.get('global_cache_hit_rate_percent', 0):.1f}%")
            print(f"  🗜️  Efficacité compression: {agg_metrics.get('global_compression_efficiency_percent', 0):.1f}%")
            print(f"  📈 Statut performance: {agg_metrics.get('performance_status', 'N/A')}")
            
            # Assertions sur l'intégration
            self.assertGreater(agg_metrics.get('total_documents_sent', 0), 0, "Aucun document traité")
            self.assertGreaterEqual(agg_metrics.get('global_cache_hit_rate_percent', 0), 20, "Cache hit rate trop faible")
        
        print("  ✅ Test intégration réussi")
        
    def test_06_performance_benchmark(self):
        """Test 6: Benchmark de performance"""
        print("\n🧪 Test 6: Benchmark de performance")
        
        # Test avec cache activé
        handler_cached = ElasticsearchHandler(
            host="localhost:9200",
            index="test-benchmark-cached",
            batch_size=10,
            cache_enabled=True,
            cache_size=500,
            compression_enabled=True
        )
        
        # Test sans cache
        handler_no_cache = ElasticsearchHandler(
            host="localhost:9200",
            index="test-benchmark-no-cache",
            batch_size=10,
            cache_enabled=False,
            compression_enabled=True
        )
        
        # Messages de test (avec répétitions pour bénéficier du cache)
        messages = [
            "Message fréquent A",
            "Message fréquent B", 
            "Message unique 1",
            "Message fréquent A",
            "Message fréquent B",
            "Message unique 2",
            "Message fréquent A",
            "Message unique 3"
        ] * 5  # 40 messages total
        
        # Benchmark avec cache
        start_time = time.time()
        logger_cached = logging.getLogger("test.benchmark.cached")
        logger_cached.setLevel(logging.INFO)
        logger_cached.addHandler(handler_cached)
        
        for msg in messages:
            logger_cached.info(msg)
        
        handler_cached._flush_batch()
        cached_time = time.time() - start_time
        
        # Benchmark sans cache
        start_time = time.time()
        logger_no_cache = logging.getLogger("test.benchmark.no_cache")
        logger_no_cache.setLevel(logging.INFO)
        logger_no_cache.addHandler(handler_no_cache)
        
        for msg in messages:
            logger_no_cache.info(msg)
        
        handler_no_cache._flush_batch()
        no_cache_time = time.time() - start_time
        
        # Métriques comparatives
        cached_metrics = handler_cached.get_performance_metrics()
        no_cache_metrics = handler_no_cache.get_performance_metrics()
        
        print(f"  ⏱️  Temps avec cache: {cached_time:.3f}s")
        print(f"  ⏱️  Temps sans cache: {no_cache_time:.3f}s")
        print(f"  📊 Documents traités (cache): {cached_metrics['documents_sent']}")
        print(f"  📊 Documents traités (no cache): {no_cache_metrics['documents_sent']}")
        print(f"  🎯 Cache hits: {cached_metrics['cache_hits']}")
        print(f"  📈 Amélioration performance: {((no_cache_time - cached_time) / no_cache_time * 100):.1f}%" if no_cache_time > 0 else "N/A")
        
        # Assertions sur la performance
        self.assertGreater(cached_metrics['cache_hits'], 15, "Pas assez de cache hits")
        self.assertLessEqual(cached_metrics['documents_sent'], no_cache_metrics['documents_sent'], 
                           "Cache devrait réduire les documents envoyés")
        
        print("  ✅ Test benchmark réussi")

def main():
    """Fonction principale de test"""
    print("🚀 DÉMARRAGE TESTS OPTIMISATION ELASTICSEARCH - PHASE 3")
    print("=" * 60)
    
    # Configuration du logging pour les tests
    logging.basicConfig(level=logging.WARNING)  # Réduire le bruit
    
    # Créer la suite de tests
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestElasticsearchOptimization)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Résumé des résultats
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS OPTIMISATION ELASTICSEARCH")
    print(f"✅ Tests réussis: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Tests échoués: {len(result.failures)}")
    print(f"🚨 Erreurs: {len(result.errors)}")
    print(f"📈 Taux de réussite: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ ÉCHECS:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if result.errors:
        print("\n🚨 ERREURS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    
    if success_rate == 100:
        print("\n🎉 TOUS LES TESTS RÉUSSIS - OPTIMISATION ELASTICSEARCH VALIDÉE!")
        return True
    else:
        print(f"\n⚠️  OPTIMISATION PARTIELLE - {success_rate:.1f}% de réussite")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 