#!/usr/bin/env python3
"""
Script de validation pour les cls API Gemini
Teste  la fois GOOGLE_API_KEY et GEMINI_API_KEY
"""

import os
import httpx
import json
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_gemini_key(api_key: str, key_name: str) -> bool:
    """Test une cl API Gemini spcifique."""
    if not api_key:
        print(f"[CROSS] {key_name} non trouve dans .env")
        return False
    
    print(f" Test de {key_name}: {api_key[:20]}...")
    
    # Test avec Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Rponds juste 'Test russi' en franais"
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
                print(f"[CHECK] {key_name} fonctionnelle!")
                print(f" Rponse: {text.strip()}")
                return True
            else:
                print(f"[CROSS] {key_name}: Rponse inattendue")
                return False
        
        elif response.status_code == 400:
            error_data = response.json()
            if "API key not valid" in str(error_data):
                print(f"[CROSS] {key_name}: Cl invalide")
            else:
                print(f"[CROSS] {key_name}: Erreur 400 - {error_data}")
            return False
        
        elif response.status_code == 403:
            print(f"[CROSS] {key_name}: Accs refus - vrifiez les permissions")
            return False
        
        else:
            print(f"[CROSS] {key_name}: Erreur HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print(f"[CROSS] {key_name}: Erreur - {e}")
        return False

def test_gemini_models_list(api_key: str) -> bool:
    """Test la liste des modles disponibles."""
    print("\n[SEARCH] Vrification des modles disponibles...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        with httpx.Client(timeout=8.0) as client:
            response = client.get(url)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            
            gemini_models = [m for m in models if "gemini" in m.get("name", "").lower()]
            
            print(f"[CHECK] {len(gemini_models)} modles Gemini disponibles:")
            for model in gemini_models[:5]:  # Limiter l'affichage
                name = model.get("name", "").replace("models/", "")
                print(f"   [CLIPBOARD] {name}")
            
            return len(gemini_models) > 0
        
        else:
            print(f"[CROSS] Impossible de rcuprer la liste des modles: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"[CROSS] Erreur lors de la rcupration des modles: {e}")
        return False

def main():
    """Fonction principale de validation."""
    print("[ROCKET] VALIDATION DES CLS API GEMINI")
    print("=" * 50)
    
    # Rcupration des cls
    google_api_key = os.getenv("GOOGLE_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    results = {}
    working_key = None
    
    # Test GOOGLE_API_KEY
    if google_api_key:
        print("\n[CLIPBOARD] Test GOOGLE_API_KEY")
        print("-" * 30)
        results["GOOGLE_API_KEY"] = test_gemini_key(google_api_key, "GOOGLE_API_KEY")
        if results["GOOGLE_API_KEY"]:
            working_key = google_api_key
    else:
        print("\n[CLIPBOARD] GOOGLE_API_KEY non dfinie")
    
    # Test GEMINI_API_KEY
    if gemini_api_key:
        print("\n[CLIPBOARD] Test GEMINI_API_KEY")
        print("-" * 30)
        results["GEMINI_API_KEY"] = test_gemini_key(gemini_api_key, "GEMINI_API_KEY")
        if results["GEMINI_API_KEY"] and not working_key:
            working_key = gemini_api_key
    else:
        print("\n[CLIPBOARD] GEMINI_API_KEY non dfinie")
    
    # Test des modles si une cl fonctionne
    if working_key:
        models_ok = test_gemini_models_list(working_key)
    else:
        models_ok = False
    
    # Rsum final
    print("\n" + "=" * 50)
    print("[CHART] RSUM DE LA VALIDATION")
    print("=" * 50)
    
    if google_api_key:
        status = "[CHECK] Fonctionnelle" if results.get("GOOGLE_API_KEY") else "[CROSS] chec"
        print(f" GOOGLE_API_KEY: {status}")
    else:
        print(" GOOGLE_API_KEY:  Non dfinie")
    
    if gemini_api_key:
        status = "[CHECK] Fonctionnelle" if results.get("GEMINI_API_KEY") else "[CROSS] chec"
        print(f" GEMINI_API_KEY: {status}")
    else:
        print(" GEMINI_API_KEY:  Non dfinie")
    
    models_status = "[CHECK] Disponibles" if models_ok else "[CROSS] Indisponibles"
    print(f"[CLIPBOARD] Modles Gemini: {models_status}")
    
    # Recommandations
    print("\n[BULB] RECOMMANDATIONS:")
    
    if any(results.values()):
        print("[CHECK] Au moins une cl Gemini fonctionne!")
        print("\n[TARGET] Vous pouvez maintenant:")
        print("   - Utiliser Gemini dans vos scripts")
        print("   - Tester l'orchestrateur avec Gemini")
        print("   - Dvelopper des agents Gemini spcialiss")
        
        print("\n[TOOL] Exemple d'utilisation:")
        print("   python test_gemini_rapide.py")
        print("   python test_gemini_orchestrateur.py")
        
        print("\n Documentation complte:")
        print("   Consultez GUIDE_FOURNISSEURS_MODELES_ORCHESTRATEUR.md")
    
    else:
        print("[CROSS] Aucune cl Gemini fonctionnelle")
        print("\n[TOOL] Solutions:")
        print("   1. Obtenez une cl sur https://makersuite.google.com/app/apikey")
        print("   2. Ajoutez-la dans .env comme GOOGLE_API_KEY ou GEMINI_API_KEY")
        print("   3. Relancez ce script de validation")
        print("\n Guide complet:")
        print("   Consultez GUIDE_FOURNISSEURS_MODELES_ORCHESTRATEUR.md")
    
    # Code de sortie
    if any(results.values()):
        print("\n Validation russie!")
        return 0
    else:
        print("\n[CROSS] Validation choue!")
        return 1

if __name__ == "__main__":
    exit(main()) 



