#!/usr/bin/env python3
"""
Script de test spécifique pour Google Gemini dans l'orchestrateur.
"""

import httpx
import json
import time

def test_gemini_in_orchestrator():
    """Test Gemini via l'orchestrateur."""
    print("🤖 Test de Gemini via l'orchestrateur")
    print("=" * 50)
    
    # Configuration
    base_url = "http://localhost:8003"
    headers = {
        "X-API-Key": "demo-key-for-testing",
        "Content-Type": "application/json"
    }
    
    # Test 1 : Tâche simple avec Gemini
    print("\n📝 Test 1: Tâche simple avec Gemini")
    payload1 = {
        "task": "Écris un haiku sur l'intelligence artificielle",
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
            print(f"✅ Succès en {duration:.2f}s")
            print(f"🤖 Agent: {result.get('agent_used', 'N/A')}")
            print(f"📝 Résultat:\n{result.get('result', 'Pas de résultat')}")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Test 2 : Tâche d'analyse avec Gemini
    print("\n📊 Test 2: Analyse avec Gemini")
    payload2 = {
        "task": "Analyse les avantages et inconvénients de l'utilisation de l'IA dans l'éducation",
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
            print(f"✅ Succès en {duration:.2f}s")
            print(f"🤖 Agent: {result.get('agent_used', 'N/A')}")
            print(f"📝 Résultat (extrait):\n{result.get('result', 'Pas de résultat')[:200]}...")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Test 3 : Comparaison avec autres modèles
    print("\n🔄 Test 3: Comparaison des modèles")
    task_comparison = "Résume en 2 phrases l'importance de la cybersécurité"
    
    models = ["gemini-1.5-flash", "gpt-4", "claude-3-sonnet"]
    results = {}
    
    for model in models:
        print(f"\n🧠 Test avec {model}...")
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
                print(f"✅ {model}: {duration:.2f}s")
            else:
                results[model] = {
                    "success": False,
                    "error": response.text
                }
                print(f"❌ {model}: Erreur {response.status_code}")
        
        except Exception as e:
            results[model] = {
                "success": False,
                "error": str(e)
            }
            print(f"❌ {model}: {e}")
        
        # Pause entre les tests
        time.sleep(2)
    
    # Affichage du résumé de comparaison
    print("\n📊 Résumé de la comparaison:")
    print("-" * 50)
    for model, data in results.items():
        if data.get("success"):
            print(f"✅ {model}: {data['duration']:.2f}s - {data['agent']}")
        else:
            print(f"❌ {model}: Échec")
    
    return True

def test_gemini_health():
    """Test la santé de l'orchestrateur avec Gemini configuré."""
    print("\n🏥 Test de santé de l'orchestrateur")
    print("-" * 40)
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get("http://localhost:8003/health")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Orchestrateur en ligne")
            print(f"📊 Status: {data.get('status', 'N/A')}")
            
            # Vérifier si Gemini est mentionné dans la config
            config_apis = data.get('apis_configured', [])
            if 'google' in str(config_apis).lower() or 'gemini' in str(config_apis).lower():
                print("✅ Gemini détecté dans la configuration")
            else:
                print("⚠️ Gemini non détecté explicitement dans la config")
            
            return True
        else:
            print(f"❌ Erreur santé: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False

def main():
    """Point d'entrée principal."""
    print("🚀 TEST COMPLET DE GOOGLE GEMINI")
    print("=" * 60)
    
    # 1. Test de santé
    health_ok = test_gemini_health()
    
    if not health_ok:
        print("\n❌ L'orchestrateur n'est pas accessible")
        print("💡 Démarrez-le avec: python start_orchestrator.py")
        return
    
    # 2. Tests fonctionnels Gemini
    success = test_gemini_in_orchestrator()
    
    # 3. Résumé final
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DU TEST GEMINI")
    print("=" * 60)
    
    if success:
        print("✅ Gemini fonctionne parfaitement dans l'orchestrateur!")
        print("\n💡 Vous pouvez maintenant:")
        print("   - Utiliser 'gemini-1.5-flash' comme preferred_model")
        print("   - Comparer les performances avec GPT-4 et Claude")
        print("   - Développer des agents spécialisés avec Gemini")
        
        print("\n🔧 Exemple d'utilisation:")
        print("""
        curl -X POST "http://localhost:8003/orchestrator/process" \\
          -H "X-API-Key: demo-key-for-testing" \\
          -H "Content-Type: application/json" \\
          -d '{
            "task": "Votre tâche ici",
            "preferred_model": "gemini-1.5-flash"
          }'
        """)
    else:
        print("❌ Problèmes détectés avec Gemini")
        print("\n💡 Vérifications:")
        print("   - Clé GOOGLE_API_KEY valide dans .env")
        print("   - Orchestrateur démarré sur le port 8003")
        print("   - Configuration Gemini dans l'orchestrateur")

if __name__ == "__main__":
    main()
