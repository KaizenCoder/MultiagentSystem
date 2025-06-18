#!/usr/bin/env python3
"""
Script de validation pour les clés API Gemini
Teste à la fois GOOGLE_API_KEY et GEMINI_API_KEY
"""

import os
import httpx
import json
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_gemini_key(api_key: str, key_name: str) -> bool:
    """Test une clé API Gemini spécifique."""
    if not api_key:
        print(f"❌ {key_name} non trouvée dans .env")
        return False
    
    print(f"🔑 Test de {key_name}: {api_key[:20]}...")
    
    # Test avec Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Réponds juste 'Test réussi' en français"
            }]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 20
        }
    }
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and result["candidates"]:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                print(f"✅ {key_name} fonctionnelle!")
                print(f"📝 Réponse: {text.strip()}")
                return True
            else:
                print(f"❌ {key_name}: Réponse inattendue")
                return False
        
        elif response.status_code == 400:
            error_data = response.json()
            if "API key not valid" in str(error_data):
                print(f"❌ {key_name}: Clé invalide")
            else:
                print(f"❌ {key_name}: Erreur 400 - {error_data}")
            return False
        
        elif response.status_code == 403:
            print(f"❌ {key_name}: Accès refusé - vérifiez les permissions")
            return False
        
        else:
            print(f"❌ {key_name}: Erreur HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ {key_name}: Erreur - {e}")
        return False

def test_gemini_models_list(api_key: str) -> bool:
    """Test la liste des modèles disponibles."""
    print("\n🔍 Vérification des modèles disponibles...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        with httpx.Client(timeout=8.0) as client:
            response = client.get(url)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            
            gemini_models = [m for m in models if "gemini" in m.get("name", "").lower()]
            
            print(f"✅ {len(gemini_models)} modèles Gemini disponibles:")
            for model in gemini_models[:5]:  # Limiter l'affichage
                name = model.get("name", "").replace("models/", "")
                print(f"   📋 {name}")
            
            return len(gemini_models) > 0
        
        else:
            print(f"❌ Impossible de récupérer la liste des modèles: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des modèles: {e}")
        return False

def main():
    """Fonction principale de validation."""
    print("🚀 VALIDATION DES CLÉS API GEMINI")
    print("=" * 50)
    
    # Récupération des clés
    google_api_key = os.getenv("GOOGLE_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    results = {}
    working_key = None
    
    # Test GOOGLE_API_KEY
    if google_api_key:
        print("\n📋 Test GOOGLE_API_KEY")
        print("-" * 30)
        results["GOOGLE_API_KEY"] = test_gemini_key(google_api_key, "GOOGLE_API_KEY")
        if results["GOOGLE_API_KEY"]:
            working_key = google_api_key
    else:
        print("\n📋 GOOGLE_API_KEY non définie")
    
    # Test GEMINI_API_KEY
    if gemini_api_key:
        print("\n📋 Test GEMINI_API_KEY")
        print("-" * 30)
        results["GEMINI_API_KEY"] = test_gemini_key(gemini_api_key, "GEMINI_API_KEY")
        if results["GEMINI_API_KEY"] and not working_key:
            working_key = gemini_api_key
    else:
        print("\n📋 GEMINI_API_KEY non définie")
    
    # Test des modèles si une clé fonctionne
    if working_key:
        models_ok = test_gemini_models_list(working_key)
    else:
        models_ok = False
    
    # Résumé final
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DE LA VALIDATION")
    print("=" * 50)
    
    if google_api_key:
        status = "✅ Fonctionnelle" if results.get("GOOGLE_API_KEY") else "❌ Échec"
        print(f"🔑 GOOGLE_API_KEY: {status}")
    else:
        print("🔑 GOOGLE_API_KEY: ⚪ Non définie")
    
    if gemini_api_key:
        status = "✅ Fonctionnelle" if results.get("GEMINI_API_KEY") else "❌ Échec"
        print(f"🔑 GEMINI_API_KEY: {status}")
    else:
        print("🔑 GEMINI_API_KEY: ⚪ Non définie")
    
    models_status = "✅ Disponibles" if models_ok else "❌ Indisponibles"
    print(f"📋 Modèles Gemini: {models_status}")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS:")
    
    if any(results.values()):
        print("✅ Au moins une clé Gemini fonctionne!")
        print("\n🎯 Vous pouvez maintenant:")
        print("   - Utiliser Gemini dans vos scripts")
        print("   - Tester l'orchestrateur avec Gemini")
        print("   - Développer des agents Gemini spécialisés")
        
        print("\n🔧 Exemple d'utilisation:")
        print("   python test_gemini_rapide.py")
        print("   python test_gemini_orchestrateur.py")
        
        print("\n📚 Documentation complète:")
        print("   Consultez GUIDE_FOURNISSEURS_MODELES_ORCHESTRATEUR.md")
    
    else:
        print("❌ Aucune clé Gemini fonctionnelle")
        print("\n🔧 Solutions:")
        print("   1. Obtenez une clé sur https://makersuite.google.com/app/apikey")
        print("   2. Ajoutez-la dans .env comme GOOGLE_API_KEY ou GEMINI_API_KEY")
        print("   3. Relancez ce script de validation")
        print("\n📚 Guide complet:")
        print("   Consultez GUIDE_FOURNISSEURS_MODELES_ORCHESTRATEUR.md")
    
    # Code de sortie
    if any(results.values()):
        print("\n🎉 Validation réussie!")
        return 0
    else:
        print("\n❌ Validation échouée!")
        return 1

if __name__ == "__main__":
    exit(main()) 