#!/usr/bin/env python3
"""
Script de test pour vérifier la validité de la clé API Google Gemini.
"""

import os
import httpx
import json
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_gemini_api():
    """Teste la clé API Google Gemini."""
    print("🔍 Test de la clé API Google Gemini...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY non trouvée dans .env")
        return False
    
    # Vérifier le format de base
    if not api_key.startswith("AIza"):
        print(f"⚠️  Format de clé suspect: {api_key[:10]}...")
        if "demo" in api_key.lower() or "replace" in api_key.lower():
            print("❌ Clé de démonstration détectée - veuillez remplacer par une vraie clé")
            return False
      # Test API Gemini (Google AI Studio)
    try:
        # Essayons avec le modèle Gemini 1.5 Flash qui est disponible
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Écris un simple 'Hello World' en une phrase."
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
                print(f"✅ Gemini API fonctionnelle!")
                print(f"📝 Réponse: {text.strip()}")
                return True
            else:
                print("❌ Réponse inattendue de Gemini")
                print(f"🔍 Contenu: {json.dumps(result, indent=2)}")
                return False
        
        elif response.status_code == 400:
            error_data = response.json()
            if "API key not valid" in str(error_data):
                print("❌ Clé API Gemini invalide")
            else:
                print(f"❌ Erreur 400: {error_data}")
            return False
        
        elif response.status_code == 403:
            print("❌ Accès refusé - vérifiez les permissions de la clé")
            return False
        
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"🔍 Réponse: {response.text}")
            return False
    
    except httpx.TimeoutException:
        print("❌ Timeout lors de la connexion à Gemini")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test Gemini: {e}")
        return False

def main():
    """Point d'entrée principal."""
    print("🚀 Test de configuration Google Gemini API")
    print("=" * 50)
    
    success = test_gemini_api()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Gemini configuré et fonctionnel!")
        print("\n💡 Prochaines étapes:")
        print("   1. Utilisez Gemini dans vos agents")
        print("   2. Testez l'orchestrateur avec des tâches réelles")
        print("   3. Développez des agents personnalisés")
    else:
        print("❌ Configuration Gemini à corriger")
        print("\n💡 Solutions:")
        print("   1. Obtenez une clé API sur https://makersuite.google.com/app/apikey")
        print("   2. Remplacez GOOGLE_API_KEY dans .env")
        print("   3. Relancez ce script")

if __name__ == "__main__":
    main()
