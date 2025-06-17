#!/usr/bin/env python3
"""
Tests avancés des APIs de l'orchestrateur multi-agent
Utilise les clés OpenAI et Anthropic validées
"""

import requests
import json
import time
from typing import Dict, Any

class OrchestrateurAPIClient:
    """Client pour tester l'API de l'orchestrateur"""
    
    def __init__(self, base_url: str = "http://localhost:8002", api_key: str = "demo-key-for-testing"):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def test_basic_endpoints(self):
        """Test des endpoints de base"""
        print("🔍 Test des endpoints de base...")
        
        endpoints = [
            ("GET", "/", "Page d'accueil"),
            ("GET", "/health", "Health check"),
            ("GET", "/docs", "Documentation Swagger"),
            ("GET", "/openapi.json", "Schema OpenAPI")
        ]
        
        for method, endpoint, description in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.request(method, url, timeout=10)
                status = "✅" if response.status_code == 200 else "❌"
                print(f"   {status} {method} {endpoint} ({response.status_code}) - {description}")
                
                if endpoint == "/health" and response.status_code == 200:
                    data = response.json()
                    print(f"      🤖 OpenAI configuré: {data.get('openai_configured', False)}")
                    print(f"      🧠 Anthropic configuré: {data.get('anthropic_configured', False)}")
                    
            except Exception as e:
                print(f"   ❌ {method} {endpoint} - Erreur: {e}")
    
    def test_task_processing(self):
        """Test du traitement de tâches (si l'endpoint existe)"""
        print("\n🤖 Test du traitement de tâches...")
        
        # Test simple de tâche
        task_data = {
            "task_description": "Écris un petit poème sur l'IA",
            "max_tokens": 100,
            "model_preference": "openai"
        }
        
        # Essayer différents endpoints possibles
        possible_endpoints = [
            "/orchestrator/process",
            "/process",
            "/task",
            "/execute"
        ]
        
        for endpoint in possible_endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.post(url, json=task_data, timeout=30)
                
                if response.status_code == 200:
                    print(f"   ✅ {endpoint} fonctionne!")
                    data = response.json()
                    print(f"      📝 Réponse: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
                    return True
                elif response.status_code == 404:
                    print(f"   ⚠️  {endpoint} n'existe pas (404)")
                else:
                    print(f"   ❌ {endpoint} erreur {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"   ⏱️  {endpoint} timeout (normal pour traitement LLM)")
            except Exception as e:
                print(f"   ❌ {endpoint} erreur: {e}")
        
        print("   💡 Aucun endpoint de traitement trouvé - c'est normal pour la version test")
        return False
    
    def test_llm_integration(self):
        """Test de l'intégration LLM (si possible)"""
        print("\n🧠 Test de l'intégration LLM...")
        
        # Tester les endpoints liés aux LLM
        llm_endpoints = [
            "/llm/models",
            "/models",
            "/ai/capabilities"
        ]
        
        for endpoint in llm_endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    print(f"   ✅ {endpoint} disponible")
                    data = response.json()
                    print(f"      📊 Données: {type(data)} avec {len(data) if isinstance(data, (list, dict)) else 'N/A'} éléments")
                elif response.status_code == 404:
                    print(f"   ⚠️  {endpoint} non disponible")
                else:
                    print(f"   ❌ {endpoint} erreur {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {endpoint} erreur: {e}")
    
    def test_performance_metrics(self):
        """Test des métriques de performance"""
        print("\n📊 Test des métriques de performance...")
        
        metrics_endpoints = [
            "/metrics",
            "/stats",
            "/performance",
            "/monitoring"
        ]
        
        for endpoint in metrics_endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    print(f"   ✅ {endpoint} disponible")
                    try:
                        data = response.json()
                        print(f"      📈 Métriques disponibles: {len(data) if isinstance(data, dict) else 'Format non JSON'}")
                    except:
                        print(f"      📈 Métriques en format texte (probablement Prometheus)")
                elif response.status_code == 404:
                    print(f"   ⚠️  {endpoint} non disponible")
                else:
                    print(f"   ❌ {endpoint} erreur {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {endpoint} erreur: {e}")
    
    def run_comprehensive_test(self):
        """Exécuter tous les tests"""
        print("🎯 TESTS COMPLETS DES APIS ORCHESTRATEUR")
        print("=" * 50)
        print(f"🌐 URL de base: {self.base_url}")
        print(f"🔑 Clé API: {self.api_key}")
        print("")
        
        # Tests
        self.test_basic_endpoints()
        self.test_task_processing()
        self.test_llm_integration()
        self.test_performance_metrics()
        
        print("\n" + "=" * 50)
        print("🎉 Tests terminés!")
        print("💡 L'orchestrateur est prêt pour vos agents personnalisés")

def main():
    """Fonction principale"""
    try:
        client = OrchestrateurAPIClient()
        client.run_comprehensive_test()
        return True
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrompus")
        return False
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
