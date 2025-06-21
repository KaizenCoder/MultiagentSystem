#!/usr/bin/env python3
"""
Script de test pour vrifier le bon fonctionnement des cls API OpenAI et Anthropic
"""

import os
import sys
import asyncio
from pathlib import Path

# Ajouter le rpertoire orchestrator au path pour les imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "orchestrator"))

try:
    from dotenv import load_dotenv
    import httpx
    from pydantic import ValidationError
    from orchestrator.app.config import settings
except ImportError as e:
    print(f"[CROSS] Erreur d'import: {e}")
    print("Veuillez installer les dpendances avec: pip install -r orchestrator/requirements.txt")
    sys.exit(1)

# Charger les variables d'environnement
load_dotenv()

async def test_openai_api():
    """Test de la cl API OpenAI"""
    print("\n[SEARCH] Test de l'API OpenAI...")
    
    try:
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Test simple avec l'endpoint models
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://api.openai.com/v1/models",
                headers=headers
            )
            
            if response.status_code == 200:
                models = response.json()
                available_models = [m["id"] for m in models["data"] if "gpt" in m["id"]][:3]
                print(f"[CHECK] OpenAI API: Connexion russie")
                print(f"   [CLIPBOARD] Modles disponibles (exemple): {', '.join(available_models)}")
                return True
            else:
                print(f"[CROSS] OpenAI API: Erreur HTTP {response.status_code}")
                print(f"   [DOCUMENT] Rponse: {response.text}")
                return False
                
    except Exception as e:
        print(f"[CROSS] OpenAI API: Erreur de connexion - {str(e)}")
        return False

async def test_anthropic_api():
    """Test de la cl API Anthropic"""
    print("\n[SEARCH] Test de l'API Anthropic...")
    
    try:
        headers = {
            "x-api-key": settings.ANTHROPIC_API_KEY,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Test avec un message simple
        payload = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 10,
            "messages": [{"role": "user", "content": "Hello"}]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"[CHECK] Anthropic API: Connexion russie")
                print(f"   [CLIPBOARD] Modle test: {result.get('model', 'claude-3-haiku-20240307')}")
                print(f"    Rponse reue: {len(result.get('content', []))} message(s)")
                return True
            else:
                print(f"[CROSS] Anthropic API: Erreur HTTP {response.status_code}")
                print(f"   [DOCUMENT] Rponse: {response.text}")
                return False
                
    except Exception as e:
        print(f"[CROSS] Anthropic API: Erreur de connexion - {str(e)}")
        return False

async def test_config_loading():
    """Test du chargement de la configuration"""
    print("\n[TOOL] Test de la configuration...")
    
    try:
        # Vrifier que les cls sont bien charges
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
            print("[CROSS] OPENAI_API_KEY n'est pas configure ou utilise la valeur par dfaut")
            return False
            
        if not settings.ANTHROPIC_API_KEY or settings.ANTHROPIC_API_KEY == "your_anthropic_api_key_here":
            print("[CROSS] ANTHROPIC_API_KEY n'est pas configure ou utilise la valeur par dfaut")
            return False
            
        # Vrifier le format des cls
        if not settings.OPENAI_API_KEY.startswith("sk-"):
            print("[CROSS] OPENAI_API_KEY ne semble pas avoir le bon format (doit commencer par 'sk-')")
            return False
            
        if not settings.ANTHROPIC_API_KEY.startswith("sk-ant-"):
            print("[CROSS] ANTHROPIC_API_KEY ne semble pas avoir le bon format (doit commencer par 'sk-ant-')")
            return False
            
        print("[CHECK] Configuration: Cls API correctement formates")
        print(f"    OpenAI: {settings.OPENAI_API_KEY[:15]}...")
        print(f"    Anthropic: {settings.ANTHROPIC_API_KEY[:15]}...")
        print(f"    Memory API URL: {settings.MEMORY_API_URL}")
        
        return True
        
    except ValidationError as e:
        print(f"[CROSS] Configuration: Erreur de validation - {e}")
        return False
    except Exception as e:
        print(f"[CROSS] Configuration: Erreur inattendue - {e}")
        return False

async def main():
    """Fonction principale de test"""
    print(" VRIFICATION DES CLS API")
    print("=" * 50)
    
    # Test de la configuration
    config_ok = await test_config_loading()
    
    if not config_ok:
        print("\n[CROSS] chec du test de configuration. Vrifiez votre fichier .env")
        return False
    
    # Test des APIs
    openai_ok = await test_openai_api()
    anthropic_ok = await test_anthropic_api()
    
    # Rsum
    print("\n" + "=" * 50)
    print("[CHART] RSUM DES TESTS")
    print("=" * 50)
    
    print(f"[CLIPBOARD] Configuration: {'[CHECK] OK' if config_ok else '[CROSS] CHEC'}")
    print(f"[ROBOT] OpenAI API:    {'[CHECK] OK' if openai_ok else '[CROSS] CHEC'}")
    print(f" Anthropic API: {'[CHECK] OK' if anthropic_ok else '[CROSS] CHEC'}")
    
    if openai_ok and anthropic_ok:
        print("\n Toutes les cls API fonctionnent correctement !")
        print(" Vous pouvez maintenant utiliser l'orchestrateur multi-agent")
        return True
    else:
        print("\n  Certaines cls API ne fonctionnent pas.")
        print("[TOOL] Vrifiez vos cls dans le fichier .env")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n  Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n[CROSS] Erreur inattendue: {e}")
        sys.exit(1)




