#!/usr/bin/env python3
"""
Test rapide et fiable de la cl API Google Gemini.
Version optimise avec timeouts courts.
"""

import os
import httpx
import json
import time
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_gemini_quick():
    """Test rapide de Gemini avec timeout court."""
    print("[ROCKET] Test rapide de Gemini API")
    print("=" * 40)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("[CROSS] GOOGLE_API_KEY non trouve")
        return False
    
    print(f" Cl trouve: {api_key[:20]}...")
    
    # Test ultra-simple
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Dis juste 'Bonjour' en une ligne"}]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 10
        }
    }
    
    try:
        print(" Test connexion (timeout: 10s)...")
        start_time = time.time()
        
        with httpx.Client(timeout=10.0) as client:
            response = client.post(url, json=payload)
        
        duration = time.time() - start_time
        print(f" Dure: {duration:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and result["candidates"]:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                print(f"[CHECK] SUCCS!")
                print(f" Rponse: {text.strip()}")
                return True
            else:
                print(f"[CROSS] Rponse vide: {result}")
                return False
        
        elif response.status_code == 400:
            error_data = response.json()
            print(f"[CROSS] Erreur 400: {error_data}")
            return False
        
        elif response.status_code == 403:
            print("[CROSS] Accs refus - cl invalide ou quotas dpasss")
            return False
        
        else:
            print(f"[CROSS] Erreur HTTP {response.status_code}: {response.text}")
            return False
    
    except httpx.TimeoutException:
        print("[CROSS] TIMEOUT - L'API Gemini ne rpond pas")
        return False
    except httpx.ConnectError:
        print("[CROSS] Erreur de connexion internet")
        return False
    except Exception as e:
        print(f"[CROSS] Erreur: {e}")
        return False

def test_gemini_models():
    """Liste les modles Gemini disponibles."""
    print("\n[SEARCH] Vrification des modles disponibles")
    print("=" * 40)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        print(" Rcupration des modles (timeout: 8s)...")
        
        with httpx.Client(timeout=8.0) as client:
            response = client.get(url)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            
            print(f"[CHECK] {len(models)} modles trouvs:")
            
            gemini_models = [m for m in models if "gemini" in m.get("name", "").lower()]
            for model in gemini_models[:5]:  # Limiter  5
                name = model.get("name", "").split("/")[-1]
                print(f"   [CLIPBOARD] {name}")
            
            if gemini_models:
                return True
            else:
                print("[CROSS] Aucun modle Gemini trouv")
                return False
        
        else:
            print(f"[CROSS] Erreur {response.status_code}")
            return False
    
    except Exception as e:
        print(f"[CROSS] Erreur modles: {e}")
        return False

def test_different_prompts():
    """Test avec diffrents types de prompts."""
    print("\n Test de diffrents prompts")
    print("=" * 40)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompts = [
        "Compte de 1  3",
        "Dis 'OK' en une ligne",
        "Nom d'un animal en 1 mot"
    ]
    
    success_count = 0
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n Test {i}/3: {prompt}")
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 20
            }
        }
        
        try:
            with httpx.Client(timeout=8.0) as client:
                response = client.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result:
                    text = result["candidates"][0]["content"]["parts"][0]["text"]
                    print(f"   [CHECK] Rponse: {text.strip()}")
                    success_count += 1
                else:
                    print(f"   [CROSS] Pas de rponse")
            else:
                print(f"   [CROSS] Erreur {response.status_code}")
        
        except Exception as e:
            print(f"   [CROSS] Erreur: {e}")
        
        # Pause entre les tests
        time.sleep(1)
    
    print(f"\n[CHART] Rsultat: {success_count}/{len(prompts)} tests russis")
    return success_count == len(prompts)

def main():
    """Test complet mais rapide."""
    print("[TARGET] TEST GEMINI - VERSION RAPIDE")
    print("=" * 50)
    
    # Test 1: Connexion de base
    test1_ok = test_gemini_quick()
    
    if not test1_ok:
        print("\n[CROSS] Test de base chou - arrt")
        return
    
    # Test 2: Modles disponibles
    test2_ok = test_gemini_models()
    
    # Test 3: Diffrents prompts
    test3_ok = test_different_prompts()
    
    # Rsum
    print("\n" + "=" * 50)
    print("[CLIPBOARD] RSUM FINAL")
    print("=" * 50)
    print(f"[TOOL] Test connexion: {'[CHECK]' if test1_ok else '[CROSS]'}")
    print(f"[CLIPBOARD] Test modles:   {'[CHECK]' if test2_ok else '[CROSS]'}")
    print(f" Test prompts:   {'[CHECK]' if test3_ok else '[CROSS]'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n GEMINI ENTIREMENT FONCTIONNEL!")
        print("[BULB] Vous pouvez maintenant:")
        print("   - Intgrer Gemini dans l'orchestrateur")
        print("   - Utiliser gemini-1.5-flash pour vos agents")
        print("   - Tester les performances en production")
    elif test1_ok:
        print("\n  GEMINI PARTIELLEMENT FONCTIONNEL")
        print("[BULB] La connexion fonctionne mais vrifiez:")
        print("   - Les quotas de votre compte")
        print("   - Les modles disponibles")
    else:
        print("\n[CROSS] GEMINI NON FONCTIONNEL")
        print("[BULB] Vrifiez:")
        print("   - Votre cl API Google")
        print("   - Votre connexion internet")
        print("   - Les quotas/limites de votre compte")

if __name__ == "__main__":
    main()




