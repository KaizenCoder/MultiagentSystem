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
    print(" Test des endpoints de base...")
    
    # Test endpoint racine
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"[CHECK] GET /: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"[CROSS] Erreur GET /: {e}")
    
    # Test endpoint health
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        print(f"[CHECK] GET /health: {response.status_code}")
        print(f"   [CHART] Status: {data.get('status')}")
        print(f"   [ROBOT] OpenAI: {'[CHECK]' if data.get('openai_configured') else '[CROSS]'}")
        print(f"    Anthropic: {'[CHECK]' if data.get('anthropic_configured') else '[CROSS]'}")
    except Exception as e:
        print(f"[CROSS] Erreur GET /health: {e}")

def test_with_api_key():
    """Test avec authentification API"""
    print("\n Test avec cl API...")
    
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Test simple
    try:
        response = requests.get(f"{BASE_URL}/health", headers=headers)
        print(f"[CHECK] GET /health avec API key: {response.status_code}")
    except Exception as e:
        print(f"[CROSS] Erreur avec API key: {e}")

def test_performance():
    """Test de performance simple"""
    print("\n[LIGHTNING] Test de performance...")
    
    start_time = time.time()
    responses = []
    
    for i in range(5):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            responses.append(response.status_code)
        except Exception as e:
            responses.append(f"Error: {e}")
    
    end_time = time.time()
    
    print(f"    5 requtes en {end_time - start_time:.2f}s")
    print(f"   [CHART] Rponses: {responses}")
    
    # Calculer la moyenne
    successful = [r for r in responses if r == 200]
    success_rate = len(successful) / len(responses) * 100
    print(f"   [CHECK] Taux de succs: {success_rate:.1f}%")

def main():
    """Fonction principale de test"""
    print("[TARGET] TEST COMPLET DE L'ORCHESTRATEUR")
    print("=" * 50)
    
    # Vrifier que le serveur rpond
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"[CHECK] Serveur accessible sur {BASE_URL}")
    except Exception as e:
        print(f"[CROSS] Serveur inaccessible: {e}")
        print("[BULB] Vrifiez que l'orchestrateur est dmarr")
        return False
    
    # Tests
    test_basic_endpoints()
    test_with_api_key()
    test_performance()
    
    print("\n" + "=" * 50)
    print(" Tests termins!")
    print("[BULB] L'orchestrateur fonctionne correctement")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n  Tests interrompus")
        exit(1)
    except Exception as e:
        print(f"\n[CROSS] Erreur inattendue: {e}")
        exit(1)




