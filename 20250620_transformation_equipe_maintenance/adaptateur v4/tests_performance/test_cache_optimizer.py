import unittest
import time
from cache.cache_optimizer import AdaptiveCacheOptimizer

class TestCacheOptimizer(unittest.TestCase):
    def setUp(self):
        self.cache = AdaptiveCacheOptimizer(max_size=100)
        
    def test_basic_cache_operations(self):
        # Test mise en cache et récupération
        test_data = "def test():\n    print('test')"
        self.cache.put(test_data, "processed_data")
        result = self.cache.get(test_data)
        self.assertEqual(result, "processed_data")
        
    def test_pattern_detection(self):
        # Test détection des patterns d'indentation
        test_data = [
            "def test1():\n    print('test')",  # pattern: 4,
            "def test2():\n    if True:\n        print('test')",  # pattern: 4,8,
            "def test3():\n  print('test')"  # pattern: 2,
        ]
        
        for data in test_data:
            self.cache.put(data, f"processed_{data}")
            
        stats = self.cache.get_stats()
        self.assertGreaterEqual(len(stats["pattern_stats"]), 3)
        
    def test_cache_eviction(self):
        # Test éviction du cache quand plein
        self.cache = AdaptiveCacheOptimizer(max_size=2)
        
        # Remplir le cache
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        
        # Accéder à key1 plusieurs fois pour augmenter son score
        for _ in range(5):
            self.cache.get("key1")
            time.sleep(0.1)  # Petit délai pour différencier les accès
            
        # Ajouter une nouvelle entrée
        self.cache.put("key3", "value3")
        
        # key1 devrait être conservé car plus utilisé
        self.assertIsNotNone(self.cache.get("key1"))
        # key2 devrait être évincé car moins utilisé
        self.assertIsNone(self.cache.get("key2"))
        
    def test_preload_patterns(self):
        # Test préchargement basé sur les patterns
        def generator_func(pattern):
            if "indent_pattern" in pattern:
                return "def test():\n    print('test')"
            return None
            
        # Ajouter quelques données pour générer des patterns
        test_data = [
            "def test1():\n    print('test')",
            "def test2():\n    print('test')",
            "def test3():\n    print('test')"
        ]
        
        for data in test_data:
            self.cache.put(data, f"processed_{data}")
            
        # Tester le préchargement
        preload_count = self.cache.preload(generator_func)
        self.assertGreater(preload_count, 0)
        
    def test_cache_performance(self):
        # Test performance du cache avec données réelles
        start_time = time.time()
        hit_count = 0
        total_ops = 1000
        
        # Simuler des opérations réelles
        for i in range(total_ops):
            key = f"def test{i%10}():\n    print('test')"
            result = self.cache.get(key)
            if result is None:
                self.cache.put(key, f"processed_{key}")
            else:
                hit_count += 1
                
        duration = time.time() - start_time
        hit_rate = (hit_count / total_ops) * 100
        
        # Vérifier les performances
        self.assertGreater(hit_rate, 70)  # Hit rate > 70%
        self.assertLess(duration, 2)  # Temps total < 2s

if __name__ == '__main__':
    unittest.main() 