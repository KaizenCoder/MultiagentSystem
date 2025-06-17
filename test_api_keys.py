#!/usr/bin/env python3
"""
Script de test pour vérifier le bon fonctionnement des clés API OpenAI et Anthropic
"""

import os
import sys
import asyncio
from pathlib import Path

# Ajouter le répertoire orchestrator au path pour les imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "orchestrator"))

try:
    from dotenv import load_dotenv
    import httpx
    from pydantic import ValidationError
    from orchestrator.app.config import settings
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("Veuillez installer les dépendances avec: pip install -r orchestrator/requirements.txt")
    sys.exit(1)

# Charger les variables d'environnement
load_dotenv()

async def test_openai_api():
    """Test de la clé API OpenAI"""
    print("\n🔍 Test de l'API OpenAI...")
    
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
                print(f"✅ OpenAI API: Connexion réussie")
                print(f"   📋 Modèles disponibles (exemple): {', '.join(available_models)}")
                return True
            else:
                print(f"❌ OpenAI API: Erreur HTTP {response.status_code}")
                print(f"   📄 Réponse: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ OpenAI API: Erreur de connexion - {str(e)}")
        return False

async def test_anthropic_api():
    """Test de la clé API Anthropic"""
    print("\n🔍 Test de l'API Anthropic...")
    
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
                print(f"✅ Anthropic API: Connexion réussie")
                print(f"   📋 Modèle testé: {result.get('model', 'claude-3-haiku-20240307')}")
                print(f"   💬 Réponse reçue: {len(result.get('content', []))} message(s)")
                return True
            else:
                print(f"❌ Anthropic API: Erreur HTTP {response.status_code}")
                print(f"   📄 Réponse: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Anthropic API: Erreur de connexion - {str(e)}")
        return False

async def test_config_loading():
    """Test du chargement de la configuration"""
    print("\n🔧 Test de la configuration...")
    
    try:
        # Vérifier que les clés sont bien chargées
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
            print("❌ OPENAI_API_KEY n'est pas configurée ou utilise la valeur par défaut")
            return False
            
        if not settings.ANTHROPIC_API_KEY or settings.ANTHROPIC_API_KEY == "your_anthropic_api_key_here":
            print("❌ ANTHROPIC_API_KEY n'est pas configurée ou utilise la valeur par défaut")
            return False
            
        # Vérifier le format des clés
        if not settings.OPENAI_API_KEY.startswith("sk-"):
            print("❌ OPENAI_API_KEY ne semble pas avoir le bon format (doit commencer par 'sk-')")
            return False
            
        if not settings.ANTHROPIC_API_KEY.startswith("sk-ant-"):
            print("❌ ANTHROPIC_API_KEY ne semble pas avoir le bon format (doit commencer par 'sk-ant-')")
            return False
            
        print("✅ Configuration: Clés API correctement formatées")
        print(f"   🔑 OpenAI: {settings.OPENAI_API_KEY[:15]}...")
        print(f"   🔑 Anthropic: {settings.ANTHROPIC_API_KEY[:15]}...")
        print(f"   🌐 Memory API URL: {settings.MEMORY_API_URL}")
        
        return True
        
    except ValidationError as e:
        print(f"❌ Configuration: Erreur de validation - {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration: Erreur inattendue - {e}")
        return False

async def main():
    """Fonction principale de test"""
    print("🧪 VÉRIFICATION DES CLÉS API")
    print("=" * 50)
    
    # Test de la configuration
    config_ok = await test_config_loading()
    
    if not config_ok:
        print("\n❌ Échec du test de configuration. Vérifiez votre fichier .env")
        return False
    
    # Test des APIs
    openai_ok = await test_openai_api()
    anthropic_ok = await test_anthropic_api()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    print(f"📋 Configuration: {'✅ OK' if config_ok else '❌ ÉCHEC'}")
    print(f"🤖 OpenAI API:    {'✅ OK' if openai_ok else '❌ ÉCHEC'}")
    print(f"🧠 Anthropic API: {'✅ OK' if anthropic_ok else '❌ ÉCHEC'}")
    
    if openai_ok and anthropic_ok:
        print("\n🎉 Toutes les clés API fonctionnent correctement !")
        print("✨ Vous pouvez maintenant utiliser l'orchestrateur multi-agent")
        return True
    else:
        print("\n⚠️  Certaines clés API ne fonctionnent pas.")
        print("🔧 Vérifiez vos clés dans le fichier .env")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)
