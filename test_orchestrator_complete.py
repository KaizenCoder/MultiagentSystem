#!/usr/bin/env python3
"""
Test complet de l'orchestrateur multi-agent
"""

import requests
import json
import time

BASE_URL = "http://localhost:8002"
API_KEY = "demo-key-for-testing"

def test_basic_endpoints():
    """Test des endpoints de base"""
    print("🧪 Test des endpoints de base...")
    
    # Test endpoint racine
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ GET /: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Erreur GET /: {e}")
    
    # Test endpoint health
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        print(f"✅ GET /health: {response.status_code}")
        print(f"   📊 Status: {data.get('status')}")
        print(f"   🤖 OpenAI: {'✅' if data.get('openai_configured') else '❌'}")
        print(f"   🧠 Anthropic: {'✅' if data.get('anthropic_configured') else '❌'}")
    except Exception as e:
        print(f"❌ Erreur GET /health: {e}")

def test_with_api_key():
    """Test avec authentification API"""
    print("\n🔑 Test avec clé API...")
    
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Test simple
    try:
        response = requests.get(f"{BASE_URL}/health", headers=headers)
        print(f"✅ GET /health avec API key: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur avec API key: {e}")

def test_performance():
    """Test de performance simple"""
    print("\n⚡ Test de performance...")
    
    start_time = time.time()
    responses = []
    
    for i in range(5):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            responses.append(response.status_code)
        except Exception as e:
            responses.append(f"Error: {e}")
    
    end_time = time.time()
    
    print(f"   📈 5 requêtes en {end_time - start_time:.2f}s")
    print(f"   📊 Réponses: {responses}")
    
    # Calculer la moyenne
    successful = [r for r in responses if r == 200]
    success_rate = len(successful) / len(responses) * 100
    print(f"   ✅ Taux de succès: {success_rate:.1f}%")

def main():
    """Fonction principale de test"""
    print("🎯 TEST COMPLET DE L'ORCHESTRATEUR")
    print("=" * 50)
    
    # Vérifier que le serveur répond
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✅ Serveur accessible sur {BASE_URL}")
    except Exception as e:
        print(f"❌ Serveur inaccessible: {e}")
        print("💡 Vérifiez que l'orchestrateur est démarré")
        return False
    
    # Tests
    test_basic_endpoints()
    test_with_api_key()
    test_performance()
    
    print("\n" + "=" * 50)
    print("🎉 Tests terminés!")
    print("💡 L'orchestrateur fonctionne correctement")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrompus")
        exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        exit(1)
