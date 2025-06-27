import unittest
import time
import requests
from monitoring.metrics_exporter import MetricsExporter
from adaptateur import Adaptateur

class TestMonitoringIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuration globale pour tous les tests"""
        # Utiliser un port non privilégié pour les tests
        cls.metrics_port = 8765
        cls.adaptateur = Adaptateur(metrics_port=cls.metrics_port)
        time.sleep(1)  # Attendre le démarrage du serveur
        
    def setUp(self):
        """Configuration initiale pour chaque test"""
        # Points d'accès locaux pour les tests
        self.metrics_url = f"http://localhost:{self.metrics_port}/metrics"
        
    def test_metrics_export(self):
        """Test de l'export des métriques"""
        # Exécuter des requêtes pour générer des métriques
        for i in range(10):
            task = type('Task', (), {'code': f'test_code_{i}'})()
            try:
                self.adaptateur.execute_task(task)
            except:
                pass
                
        # Attendre la propagation des métriques
        time.sleep(1)
        
        # Vérifier les métriques
        response = requests.get(self.metrics_url)
        self.assertEqual(response.status_code, 200)
        metrics_data = response.text
        
        # Vérifier la présence des métriques essentielles
        expected_metrics = [
            'adaptateur_requests_total',
            'adaptateur_cache_hits_total',
            'adaptateur_cache_misses_total',
            'adaptateur_request_duration_seconds_bucket',
            'adaptateur_errors_total'
        ]
        
        for metric in expected_metrics:
            self.assertIn(metric, metrics_data)
            
    def test_cache_performance(self):
        """Test des performances du cache"""
        # Générer du trafic avec des motifs répétitifs
        for i in range(100):
            task = type('Task', (), {'code': f'test_code_{i%10}'})()
            self.adaptateur.execute_task(task)
            
        # Attendre la propagation des métriques
        time.sleep(1)
        
        # Vérifier les métriques
        response = requests.get(self.metrics_url)
        self.assertEqual(response.status_code, 200)
        metrics_data = response.text
        
        # Vérifier le hit rate du cache
        hits = 0
        total = 0
        
        for line in metrics_data.split('\n'):
            if 'adaptateur_cache_hits_total' in line and not line.startswith('#'):
                hits = float(line.split()[1])
            elif 'adaptateur_requests_total' in line and not line.startswith('#'):
                total = float(line.split()[1])
                
        if total > 0:
            hit_rate = (hits / total) * 100
            self.assertGreater(hit_rate, 70, "Hit rate du cache inférieur à 70%")
            
    def test_error_handling(self):
        """Test de la gestion des erreurs"""
        # Générer des erreurs
        for i in range(5):
            task = type('Task', (), {'code': 'invalid_code'})()
            try:
                self.adaptateur.execute_task(task)
            except:
                pass
                
        # Attendre la propagation des métriques
        time.sleep(1)
        
        # Vérifier les métriques d'erreur
        response = requests.get(self.metrics_url)
        self.assertEqual(response.status_code, 200)
        metrics_data = response.text
        
        errors = 0
        for line in metrics_data.split('\n'):
            if 'adaptateur_errors_total' in line and not line.startswith('#'):
                errors = float(line.split()[1])
                break
                
        self.assertGreater(errors, 0, "Aucune erreur enregistrée")
        
    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        # Arrêter le serveur de métriques si nécessaire
        if hasattr(cls.adaptateur, 'metrics'):
            cls.adaptateur.metrics.stop()

if __name__ == '__main__':
    unittest.main() 