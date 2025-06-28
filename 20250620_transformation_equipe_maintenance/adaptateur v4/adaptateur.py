from cache.cache_optimizer import AdaptiveCacheOptimizer
from monitoring.metrics_exporter import MetricsExporter
import time

class Adaptateur:
    def __init__(self, metrics_port=8000):
        self.cache = AdaptiveCacheOptimizer(max_size=1000)
        self.metrics = MetricsExporter(port=metrics_port)
        self.metrics.start()
        
    def execute_task(self, task):
        start_time = time.time()
        self.metrics.record_request()
        
        try:
            # Vérification du cache
            cached_result = self.cache.get(task.code)
            if cached_result:
                self.metrics.record_cache_hit()
                duration = time.time() - start_time
                self.metrics.record_duration(duration)
                return cached_result
                
            # Exécution de la tâche
            result = self._process_task(task)
            
            # Mise en cache du résultat
            self.cache.put(task.code, result)
            self.metrics.record_cache_miss()
            
            # Enregistrement de la durée
            duration = time.time() - start_time
            self.metrics.record_duration(duration)
            
            return result
            
        except Exception as e:
            self.metrics.record_error()
            duration = time.time() - start_time
            self.metrics.record_duration(duration)
            raise
            
    def _process_task(self, task):
        """Traitement d'une tâche"""
        if task.code == 'invalid_code':
            raise ValueError("Code invalide")
        # Simulation du traitement
        time.sleep(0.1)
        return f"Résultat pour {task.code}" 