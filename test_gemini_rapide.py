#!/usr/bin/env python3
"""
Test rapide et fiable de la clé API Google Gemini.
Version optimisée avec timeouts courts.
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
    print("🚀 Test rapide de Gemini API")
    print("=" * 40)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY non trouvée")
        return False
    
    print(f"🔑 Clé trouvée: {api_key[:20]}...")
    
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
        print("⏱️ Test connexion (timeout: 10s)...")
        start_time = time.time()
        
        with httpx.Client(timeout=10.0) as client:
            response = client.post(url, json=payload)
        
        duration = time.time() - start_time
        print(f"⏰ Durée: {duration:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and result["candidates"]:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                print(f"✅ SUCCÈS!")
                print(f"📝 Réponse: {text.strip()}")
                return True
            else:
                print(f"❌ Réponse vide: {result}")
                return False
        
        elif response.status_code == 400:
            error_data = response.json()
            print(f"❌ Erreur 400: {error_data}")
            return False
        
        elif response.status_code == 403:
            print("❌ Accès refusé - clé invalide ou quotas dépassés")
            return False
        
        else:
            print(f"❌ Erreur HTTP {response.status_code}: {response.text}")
            return False
    
    except httpx.TimeoutException:
        print("❌ TIMEOUT - L'API Gemini ne répond pas")
        return False
    except httpx.ConnectError:
        print("❌ Erreur de connexion internet")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_gemini_models():
    """Liste les modèles Gemini disponibles."""
    print("\n🔍 Vérification des modèles disponibles")
    print("=" * 40)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        print("⏱️ Récupération des modèles (timeout: 8s)...")
        
        with httpx.Client(timeout=8.0) as client:
            response = client.get(url)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            
            print(f"✅ {len(models)} modèles trouvés:")
            
            gemini_models = [m for m in models if "gemini" in m.get("name", "").lower()]
            for model in gemini_models[:5]:  # Limiter à 5
                name = model.get("name", "").split("/")[-1]
                print(f"   📋 {name}")
            
            if gemini_models:
                return True
            else:
                print("❌ Aucun modèle Gemini trouvé")
                return False
        
        else:
            print(f"❌ Erreur {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Erreur modèles: {e}")
        return False

def test_different_prompts():
    """Test avec différents types de prompts."""
    print("\n🧪 Test de différents prompts")
    print("=" * 40)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompts = [
        "Compte de 1 à 3",
        "Dis 'OK' en une ligne",
        "Nom d'un animal en 1 mot"
    ]
    
    success_count = 0
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n🔸 Test {i}/3: {prompt}")
        
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
                    print(f"   ✅ Réponse: {text.strip()}")
                    success_count += 1
                else:
                    print(f"   ❌ Pas de réponse")
            else:
                print(f"   ❌ Erreur {response.status_code}")
        
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        # Pause entre les tests
        time.sleep(1)
    
    print(f"\n📊 Résultat: {success_count}/{len(prompts)} tests réussis")
    return success_count == len(prompts)

def main():
    """Test complet mais rapide."""
    print("🎯 TEST GEMINI - VERSION RAPIDE")
    print("=" * 50)
    
    # Test 1: Connexion de base
    test1_ok = test_gemini_quick()
    
    if not test1_ok:
        print("\n❌ Test de base échoué - arrêt")
        return
    
    # Test 2: Modèles disponibles
    test2_ok = test_gemini_models()
    
    # Test 3: Différents prompts
    test3_ok = test_different_prompts()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📋 RÉSUMÉ FINAL")
    print("=" * 50)
    print(f"🔧 Test connexion: {'✅' if test1_ok else '❌'}")
    print(f"📋 Test modèles:   {'✅' if test2_ok else '❌'}")
    print(f"🧪 Test prompts:   {'✅' if test3_ok else '❌'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n🎉 GEMINI ENTIÈREMENT FONCTIONNEL!")
        print("💡 Vous pouvez maintenant:")
        print("   - Intégrer Gemini dans l'orchestrateur")
        print("   - Utiliser gemini-1.5-flash pour vos agents")
        print("   - Tester les performances en production")
    elif test1_ok:
        print("\n⚠️  GEMINI PARTIELLEMENT FONCTIONNEL")
        print("💡 La connexion fonctionne mais vérifiez:")
        print("   - Les quotas de votre compte")
        print("   - Les modèles disponibles")
    else:
        print("\n❌ GEMINI NON FONCTIONNEL")
        print("💡 Vérifiez:")
        print("   - Votre clé API Google")
        print("   - Votre connexion internet")
        print("   - Les quotas/limites de votre compte")

if __name__ == "__main__":
    main()
