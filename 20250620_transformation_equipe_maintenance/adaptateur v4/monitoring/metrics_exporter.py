#!/usr/bin/env python3
"""
VOLET 2.4 - MONITORING PRODUCTION
================================

Instrumentation de l'Adaptateur v4 pour exposer les métriques
vers Prometheus et visualisation dans Grafana.
"""

from prometheus_client import start_http_server, Counter, Histogram, Gauge, CollectorRegistry
import time
import psutil
import threading
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

class MetricsExporter:
    """Gestionnaire d'export des métriques Prometheus"""
    
    def __init__(self, port=8000):
        self.port = port
        self.registry = CollectorRegistry()
        self.running = False
        self._memory_thread = None
        
        # Métriques
        self.requests_total = Counter(
            'adaptateur_requests_total',
            'Total des requêtes traitées',
            registry=self.registry
        )
        
        self.cache_hits = Counter(
            'adaptateur_cache_hits_total',
            'Total des hits du cache',
            registry=self.registry
        )
        
        self.cache_misses = Counter(
            'adaptateur_cache_misses_total',
            'Total des misses du cache',
            registry=self.registry
        )
        
        self.request_duration = Histogram(
            'adaptateur_request_duration_seconds',
            'Durée des requêtes',
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
            registry=self.registry
        )
        
        self.errors_total = Counter(
            'adaptateur_errors_total',
            'Total des erreurs',
            registry=self.registry
        )
        
        self.memory_usage = Gauge(
            'adaptateur_memory_usage_bytes',
            'Utilisation mémoire en bytes',
            registry=self.registry
        )
        
        self.cache_size = Gauge(
            'adaptateur_cache_size',
            'Nombre d\'entrées dans le cache'
        )
        
        # Démarrer le thread de monitoring mémoire
        self._start_memory_monitoring()
    
    def start(self):
        """Démarre le serveur d'export des métriques"""
        try:
            start_http_server(self.port, registry=self.registry)
            logger.info(f"Serveur métriques démarré sur le port {self.port}")
        except Exception as e:
            logger.error(f"Erreur au démarrage du serveur métriques: {e}")
    
    def stop(self):
        """Arrête le serveur de métriques et le monitoring"""
        self.running = False
        if self._memory_thread and self._memory_thread.is_alive():
            self._memory_thread.join(timeout=2)
    
    def _monitor_memory(self):
        """Thread de monitoring de la mémoire"""
        while self.running:
            process = psutil.Process()
            memory_info = process.memory_info()
            self.memory_usage.set(memory_info.rss)
            time.sleep(1)
    
    def _start_memory_monitoring(self):
        """Démarre le thread de monitoring mémoire"""
        self.running = True
        self._memory_thread = threading.Thread(target=self._monitor_memory)
        self._memory_thread.daemon = True
        self._memory_thread.start()
    
    def record_request(self):
        """Enregistre une requête"""
        self.requests_total.inc()
    
    def record_duration(self, duration):
        """Enregistre la durée d'une requête"""
        self.request_duration.observe(duration)
    
    def record_error(self):
        """Enregistre une erreur"""
        self.errors_total.inc()
    
    def record_cache_hit(self):
        """Enregistre un hit du cache"""
        self.cache_hits.inc()
    
    def record_cache_miss(self):
        """Enregistre un miss du cache"""
        self.cache_misses.inc()
    
    def update_memory_usage(self, bytes_used):
        """Met à jour l'utilisation mémoire"""
        self.memory_usage.set(bytes_used)
    
    def update_cache_size(self, size):
        """Met à jour la taille du cache"""
        self.cache_size.set(size)

# Exemple d'utilisation
if __name__ == "__main__":
    exporter = MetricsExporter()
    try:
        exporter.start()
        logger.info("Appuyez sur Ctrl+C pour arrêter...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Arrêt du serveur métriques...")
        exporter.stop() 