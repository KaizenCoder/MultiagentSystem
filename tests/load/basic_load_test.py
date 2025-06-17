"""
Test de charge basique pour l'orchestrateur multi-agent.
Valide que les performances ne se dégradent pas avec les correctifs sécurité.
"""

from locust import HttpUser, task, between
import json
import random


class OrchestratorUser(HttpUser):
    """Utilisateur simulé pour les tests de charge."""
    
    wait_time = between(1, 3)  # Attente entre 1 et 3 secondes entre les requêtes
    
    def on_start(self):
        """Initialisation de l'utilisateur."""
        # Test de connectivité
        response = self.client.get("/health")
        if response.status_code != 200:
            print(f"❌ Service non disponible: {response.status_code}")
    
    @task(3)  # Poids 3 - tâche principale
    def health_check(self):
        """Test du endpoint de health check."""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("status") == "healthy":
                        response.success()
                    else:
                        response.failure(f"Unhealthy status: {data.get('status')}")
                except ValueError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(2)  # Poids 2 - test de l'API principale
    def orchestrate_simple_task(self):
        """Test d'orchestration d'une tâche simple."""
        payload = {
            "task_description": f"Simple task {random.randint(1, 1000)}",
            "file_paths": [],
            "max_agents": 2
        }
        
        with self.client.post(
            "/orchestrate", 
            json=payload,
            catch_response=True,
            timeout=30
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "task_id" in data:
                        response.success()
                    else:
                        response.failure("Missing task_id in response")
                except ValueError:
                    response.failure("Invalid JSON response")
            elif response.status_code == 422:
                # Validation error - acceptable
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(1)  # Poids 1 - test de sécurité
    def test_code_analysis(self):
        """Test de l'analyse de code sécurisée."""
        safe_code = """
def hello_world():
    return "Hello, World!"

result = hello_world()
print(result)
"""
        
        payload = {
            "task_description": "Analyze this safe Python code",
            "file_content": safe_code,
            "analysis_type": "security"
        }
        
        with self.client.post(
            "/analyze", 
            json=payload,
            catch_response=True,
            timeout=15
        ) as response:
            if response.status_code in [200, 422]:  # 422 pour validation error
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(1)  # Poids 1 - test endpoints de métriques
    def metrics_check(self):
        """Test des métriques Prometheus."""
        with self.client.get("/metrics", catch_response=True) as response:
            if response.status_code == 200:
                if "orchestrator_" in response.text:
                    response.success()
                else:
                    response.failure("No orchestrator metrics found")
            else:
                response.failure(f"HTTP {response.status_code}")


class SecurityTestUser(HttpUser):
    """Utilisateur pour tests de sécurité sous charge."""
    
    wait_time = between(2, 5)
    weight = 1  # Moins d'utilisateurs pour les tests de sécurité
    
    @task
    def test_malicious_code_blocked(self):
        """Teste que le code malveilleux est bloqué même sous charge."""
        malicious_payloads = [
            "eval('__import__(\"os\").system(\"id\")')",
            "exec('import subprocess; subprocess.run([\"ls\", \"/\"])')",
            "__import__('os').system('malicious')",
            "open('/etc/passwd', 'r').read()",
            "compile('dangerous', '<string>', 'exec')"
        ]
        
        payload = {
            "task_description": "Analyze malicious code",
            "file_content": random.choice(malicious_payloads)
        }
        
        with self.client.post(
            "/analyze",
            json=payload,
            catch_response=True,
            timeout=10
        ) as response:
            # Le code malveilleux doit être rejeté (400/422) ou analysé de façon sécurisée (200)
            if response.status_code in [200, 400, 422]:
                if response.status_code == 200:
                    # Vérifier que l'analyse ne contient pas d'exécution réelle
                    try:
                        data = response.json()
                        result = data.get("result", "").lower()
                        if "error" in result or "blocked" in result or "security" in result:
                            response.success()
                        else:
                            response.failure("Malicious code not properly handled")
                    except:
                        response.success()  # Assume it's safe if we can't parse
                else:
                    response.success()  # Proper rejection
            else:
                response.failure(f"Unexpected response: {response.status_code}")


class AdminUser(HttpUser):
    """Utilisateur admin pour les endpoints sensibles."""
    
    wait_time = between(5, 10)
    weight = 1  # Très peu d'utilisateurs admin
    
    @task
    def admin_health_detailed(self):
        """Test du health check détaillé admin."""
        with self.client.get("/admin/health/detailed", catch_response=True) as response:
            if response.status_code in [200, 401, 403]:  # 401/403 = pas d'auth, c'est OK
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task
    def admin_metrics_detailed(self):
        """Test des métriques détaillées."""
        with self.client.get("/admin/metrics", catch_response=True) as response:
            if response.status_code in [200, 401, 403]:
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")


# Configuration pour tests de charge spécialisés
class StressTestUser(HttpUser):
    """Utilisateur pour tests de stress spécialisés."""
    
    wait_time = between(0.5, 1.5)  # Plus agressif
    
    @task(5)
    def rapid_health_checks(self):
        """Health checks rapides pour tester la robustesse."""
        self.client.get("/health")
    
    @task(1)
    def concurrent_analysis(self):
        """Tests d'analyse concurrente."""
        code = f"""
# Test concurrent {random.randint(1, 10000)}
def test_function():
    data = {{"key": "value_{random.randint(1, 1000)}"}}
    return data

result = test_function()
"""
        
        payload = {
            "task_description": f"Concurrent analysis {random.randint(1, 1000)}",
            "file_content": code
        }
        
        self.client.post("/analyze", json=payload, timeout=5)
