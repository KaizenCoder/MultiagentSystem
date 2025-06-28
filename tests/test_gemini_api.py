#!/usr/bin/env python3
"""
Script de test pour vrifier la validit de la cl API Google Gemini.
"""

import os
import httpx
import json
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_gemini_api():
    """Teste la cl API Google Gemini."""
    print("[SEARCH] Test de la cl API Google Gemini...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("[CROSS] GOOGLE_API_KEY non trouve dans .env")
        return False
    
    # Vrifier le format de base
    if not api_key.startswith("AIza"):
        print(f"  Format de cl suspect: {api_key[:10]}...")
        if "demo" in api_key.lower() or "replace" in api_key.lower():
            print("[CROSS] Cl de dmonstration dtecte - veuillez remplacer par une vraie cl")
            return False
      # Test API Gemini (Google AI Studio)
    try:
        # Essayons avec le modle Gemini 1.5 Flash qui est disponible
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": "cris un simple 'Hello World' en une phrase."
                }]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 50
            }
        }
        
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and result["candidates"]:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                print(f"[CHECK] Gemini API fonctionnelle!")
                print(f" Rponse: {text.strip()}")
                return True
            else:
                print("[CROSS] Rponse inattendue de Gemini")
                print(f"[SEARCH] Contenu: {json.dumps(result, indent=2)}")
                return False
        
        elif response.status_code == 400:
            error_data = response.json()
            if "API key not valid" in str(error_data):
                print("[CROSS] Cl API Gemini invalide")
            else:
                print(f"[CROSS] Erreur 400: {error_data}")
            return False
        
        elif response.status_code == 403:
            print("[CROSS] Accs refus - vrifiez les permissions de la cl")
            return False
        
        else:
            print(f"[CROSS] Erreur HTTP {response.status_code}")
            print(f"[SEARCH] Rponse: {response.text}")
            return False
    
    except httpx.TimeoutException:
        print("[CROSS] Timeout lors de la connexion  Gemini")
        return False
    except Exception as e:
        print(f"[CROSS] Erreur lors du test Gemini: {e}")
        return False

def main():
    """Point d'entre principal."""
    print("[ROCKET] Test de configuration Google Gemini API")
    print("=" * 50)
    
    success = test_gemini_api()
    
    print("\n" + "=" * 50)
    if success:
        print("[CHECK] Gemini configur et fonctionnel!")
        print("\n[BULB] Prochaines tapes:")
        print("   1. Utilisez Gemini dans vos agents")
        print("   2. Testez l'orchestrateur avec des tches relles")
        print("   3. Dveloppez des agents personnaliss")
    else:
        print("[CROSS] Configuration Gemini  corriger")
        print("\n[BULB] Solutions:")
        print("   1. Obtenez une cl API sur https://makersuite.google.com/app/apikey")
        print("   2. Remplacez GOOGLE_API_KEY dans .env")
        print("   3. Relancez ce script")

if __name__ == "__main__":
    main()




