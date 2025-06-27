from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time

class MockMetricsHandler(BaseHTTPRequestHandler):
    """Handler pour simuler les endpoints Prometheus et Grafana"""
    
    def do_GET(self):
        if self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            
            # Métriques simulées
            metrics = """
# HELP adaptateur_requests_total Total des requêtes
# TYPE adaptateur_requests_total counter
adaptateur_requests_total 100
# HELP adaptateur_cache_hits_total Total des hits du cache
# TYPE adaptateur_cache_hits_total counter
adaptateur_cache_hits_total 75
# HELP adaptateur_cache_misses_total Total des misses du cache
# TYPE adaptateur_cache_misses_total counter
adaptateur_cache_misses_total 25
# HELP adaptateur_request_duration_seconds Durée des requêtes
# TYPE adaptateur_request_duration_seconds histogram
adaptateur_request_duration_seconds_bucket{le="0.1"} 80
adaptateur_request_duration_seconds_bucket{le="0.5"} 95
adaptateur_request_duration_seconds_bucket{le="1.0"} 100
# HELP adaptateur_errors_total Total des erreurs
# TYPE adaptateur_errors_total counter
adaptateur_errors_total 5
"""
            self.wfile.write(metrics.encode())
            
        elif self.path == "/api/v1/alerts":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            # Alertes simulées
            alerts = {
                "status": "success",
                "data": {
                    "alerts": [
                        {
                            "labels": {
                                "alertname": "HighErrorRate",
                                "severity": "warning"
                            },
                            "state": "firing",
                            "value": "0.15"
                        }
                    ]
                }
            }
            self.wfile.write(json.dumps(alerts).encode())
            
        elif self.path == "/api/dashboards/uid/adaptateur_v4":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            # Dashboard simulé
            dashboard = {
                "dashboard": {
                    "panels": [
                        {"title": "Taux d'erreur"},
                        {"title": "Hit rate cache"},
                        {"title": "Latence"},
                        {"title": "Utilisation mémoire"}
                    ]
                }
            }
            self.wfile.write(json.dumps(dashboard).encode())
            
        else:
            self.send_response(404)
            self.end_headers()

class MockMonitoringServer:
    """Serveur mock pour les tests de monitoring"""
    
    def __init__(self, port=9090):
        self.port = port
        self.server = HTTPServer(('localhost', port), MockMetricsHandler)
        self.thread = None
        
    def start(self):
        """Démarre le serveur dans un thread séparé"""
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        # Attendre que le serveur soit prêt
        time.sleep(1)
        
    def stop(self):
        """Arrête le serveur"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            if self.thread:
                self.thread.join()

if __name__ == '__main__':
    # Test du serveur mock
    server = MockMonitoringServer()
    try:
        print("Démarrage du serveur mock sur le port 9090...")
        server.start()
        print("Serveur mock démarré. Ctrl+C pour arrêter.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nArrêt du serveur mock...")
        server.stop()
        print("Serveur mock arrêté.") 