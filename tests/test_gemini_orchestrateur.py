#!/usr/bin/env python3
"""
Script de test spcifique pour Google Gemini dans l'orchestrateur.
"""

import httpx
import json
import time

def test_gemini_in_orchestrator():
    """Test Gemini via l'orchestrateur."""
    print("[ROBOT] Test de Gemini via l'orchestrateur")
    print("=" * 50)
    
    # Configuration
    base_url = "http://localhost:8003"
    headers = {
        "X-API-Key": "demo-key-for-testing",
        "Content-Type": "application/json"
    }
    
    # Test 1 : Tche simple avec Gemini
    print("\n Test 1: Tche simple avec Gemini")
    payload1 = {
        "task": "cris un haiku sur l'intelligence artificielle",
        "preferred_model": "gemini-1.5-flash",
        "requirements": ["creative"]
    }
    
    try:
        start_time = time.time()
        with httpx.Client(timeout=60.0) as client:
            response = client.post(f"{base_url}/orchestrator/process", headers=headers, json=payload1)
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"[CHECK] Succs en {duration:.2f}s")
            print(f"[ROBOT] Agent: {result.get('agent_used', 'N/A')}")
            print(f" Rsultat:\n{result.get('result', 'Pas de rsultat')}")
        else:
            print(f"[CROSS] Erreur {response.status_code}: {response.text}")
            return False
    
    except Exception as e:
        print(f"[CROSS] Erreur: {e}")
        return False
    
    # Test 2 : Tche d'analyse avec Gemini
    print("\n[CHART] Test 2: Analyse avec Gemini")
    payload2 = {
        "task": "Analyse les avantages et inconvnients de l'utilisation de l'IA dans l'ducation",
        "preferred_model": "gemini-1.5-flash", 
        "requirements": ["analysis"]
    }
    
    try:
        start_time = time.time()
        with httpx.Client(timeout=90.0) as client:
            response = client.post(f"{base_url}/orchestrator/process", headers=headers, json=payload2)
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"[CHECK] Succs en {duration:.2f}s")
            print(f"[ROBOT] Agent: {result.get('agent_used', 'N/A')}")
            print(f" Rsultat (extrait):\n{result.get('result', 'Pas de rsultat')[:200]}...")
        else:
            print(f"[CROSS] Erreur {response.status_code}: {response.text}")
            return False
    
    except Exception as e:
        print(f"[CROSS] Erreur: {e}")
        return False
    
    # Test 3 : Comparaison avec autres modles
    print("\n Test 3: Comparaison des modles")
    task_comparison = "Rsume en 2 phrases l'importance de la cyberscurit"
    
    models = ["gemini-1.5-flash", "gpt-4", "claude-3-sonnet"]
    results = {}
    
    for model in models:
        print(f"\n Test avec {model}...")
        payload = {
            "task": task_comparison,
            "preferred_model": model,
            "requirements": []
        }
        
        try:
            start_time = time.time()
            with httpx.Client(timeout=60.0) as client:
                response = client.post(f"{base_url}/orchestrator/process", headers=headers, json=payload)
            
            duration = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                results[model] = {
                    "success": True,
                    "duration": duration,
                    "result": result.get('result', ''),
                    "agent": result.get('agent_used', 'N/A')
                }
                print(f"[CHECK] {model}: {duration:.2f}s")
            else:
                results[model] = {
                    "success": False,
                    "error": response.text
                }
                print(f"[CROSS] {model}: Erreur {response.status_code}")
        
        except Exception as e:
            results[model] = {
                "success": False,
                "error": str(e)
            }
            print(f"[CROSS] {model}: {e}")
        
        # Pause entre les tests
        time.sleep(2)
    
    # Affichage du rsum de comparaison
    print("\n[CHART] Rsum de la comparaison:")
    print("-" * 50)
    for model, data in results.items():
        if data.get("success"):
            print(f"[CHECK] {model}: {data['duration']:.2f}s - {data['agent']}")
        else:
            print(f"[CROSS] {model}: chec")
    
    return True

def test_gemini_health():
    """Test la sant de l'orchestrateur avec Gemini configur."""
    print("\n Test de sant de l'orchestrateur")
    print("-" * 40)
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get("http://localhost:8003/health")
        
        if response.status_code == 200:
            data = response.json()
            print("[CHECK] Orchestrateur en ligne")
            print(f"[CHART] Status: {data.get('status', 'N/A')}")
            
            # Vrifier si Gemini est mentionn dans la config
            config_apis = data.get('apis_configured', [])
            if 'google' in str(config_apis).lower() or 'gemini' in str(config_apis).lower():
                print("[CHECK] Gemini dtect dans la configuration")
            else:
                print(" Gemini non dtect explicitement dans la config")
            
            return True
        else:
            print(f"[CROSS] Erreur sant: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"[CROSS] Erreur connexion: {e}")
        return False

def main():
    """Point d'entre principal."""
    print("[ROCKET] TEST COMPLET DE GOOGLE GEMINI")
    print("=" * 60)
    
    # 1. Test de sant
    health_ok = test_gemini_health()
    
    if not health_ok:
        print("\n[CROSS] L'orchestrateur n'est pas accessible")
        print("[BULB] Dmarrez-le avec: python start_orchestrator.py")
        return
    
    # 2. Tests fonctionnels Gemini
    success = test_gemini_in_orchestrator()
    
    # 3. Rsum final
    print("\n" + "=" * 60)
    print("[CLIPBOARD] RSUM DU TEST GEMINI")
    print("=" * 60)
    
    if success:
        print("[CHECK] Gemini fonctionne parfaitement dans l'orchestrateur!")
        print("\n[BULB] Vous pouvez maintenant:")
        print("   - Utiliser 'gemini-1.5-flash' comme preferred_model")
        print("   - Comparer les performances avec GPT-4 et Claude")
        print("   - Dvelopper des agents spcialiss avec Gemini")
        
        print("\n[TOOL] Exemple d'utilisation:")
        print("""
        curl -X POST "http://localhost:8003/orchestrator/process" \\
          -H "X-API-Key: demo-key-for-testing" \\
          -H "Content-Type: application/json" \\
          -d '{
            "task": "Votre tche ici",
            "preferred_model": "gemini-1.5-flash"
          }'
        """)
    else:
        print("[CROSS] Problmes dtects avec Gemini")
        print("\n[BULB] Vrifications:")
        print("   - Cl GOOGLE_API_KEY valide dans .env")
        print("   - Orchestrateur dmarr sur le port 8003")
        print("   - Configuration Gemini dans l'orchestrateur")

if __name__ == "__main__":
    main()




