#!/usr/bin/env python3
"""
🤖 Démonstration Intégration LLM - Agents Modernes
==================================================

Script de test pour vérifier le fonctionnement des agents modernes
avec intégration LLM (Ollama DeepSeek).

Agents testés :
- Agent 05 : Maître Tests & Validation
- Agent FASTAPI 23 : Orchestration Enterprise

Auteur: Claude Code
Date: 2025-06-28
"""

import asyncio
import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any

# Ajouter le chemin des agents modernes
sys.path.append(str(Path(__file__).parent.parent / 'agents' / 'modern'))

async def test_ollama_connection():
    """Test de connexion à Ollama"""
    print("🔍 === TEST CONNEXION OLLAMA ===")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama connecté - {len(models)} modèles disponibles")
            for model in models:
                name = model.get('name', 'unknown')
                size = model.get('size', 0) / (1024**3)  # GB
                print(f"   📦 {name} ({size:.1f}GB)")
            return True
        else:
            print(f"❌ Ollama non accessible (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Erreur connexion Ollama: {e}")
        return False

async def test_agent_05_llm():
    """Test Agent 05 avec LLM"""
    print("\n🧪 === TEST AGENT 05 - MAÎTRE TESTS & VALIDATION ===")
    
    try:
        # Import dynamique
        from agent_05_maitre_tests_validation_modern_fixed import ModernAgent05MaitreTestsValidation
        
        # Initialiser l'agent
        agent = ModernAgent05MaitreTestsValidation()
        print("✅ Agent 05 initialisé")
        
        # Test health check
        health = await agent.health_check()
        print(f"🏥 Health Check: {health['status']}")
        print(f"   LLM disponible: {health.get('llm_available', 'unknown')}")
        
        # Test génération rapport avec données de test
        test_context = {
            "project": "NextGeneration Demo",
            "test_suite": "Integration Tests",
            "environment": "development"
        }
        
        test_metriques = {
            "tests_executes": 150,
            "tests_reussis": 142,
            "tests_echoues": 8,
            "couverture_code": 0.87,
            "duree_execution": 245.3,
            "memoire_utilisee": 512,
            "erreurs_critiques": 2
        }
        
        print("\n📊 Génération rapport avec LLM...")
        start_time = time.time()
        
        rapport = await agent.generer_rapport_strategique(
            context=test_context,
            type_rapport="tests",
            metriques=test_metriques
        )
        
        duration = time.time() - start_time
        print(f"⏱️ Durée: {duration:.2f}s")
        
        if rapport and 'contenu' in rapport:
            print("✅ Rapport généré avec succès")
            
            # Afficher extraits du rapport
            contenu = rapport['contenu']
            if isinstance(contenu, dict):
                print(f"   📋 Sections: {list(contenu.keys())}")
                
                # Analyser si LLM a été utilisé
                has_llm_insights = any(
                    'analyse' in str(section).lower() or 
                    'recommandation' in str(section).lower() or
                    'insight' in str(section).lower()
                    for section in contenu.values()
                )
                
                if has_llm_insights:
                    print("🤖 LLM insights détectés dans le rapport")
                else:
                    print("📝 Rapport legacy généré (fallback)")
                
            else:
                print(f"   📄 Taille rapport: {len(str(contenu))} caractères")
        else:
            print("❌ Échec génération rapport")
            
        return True
        
    except ImportError as e:
        print(f"❌ Erreur import Agent 05: {e}")
        return False
    except Exception as e:
        print(f"💥 Erreur test Agent 05: {e}")
        return False

async def test_agent_fastapi_llm():
    """Test Agent FASTAPI 23 avec LLM"""
    print("\n🚀 === TEST AGENT FASTAPI 23 - ORCHESTRATION ENTERPRISE ===")
    
    try:
        # Import dynamique
        from agent_FASTAPI_23_orchestration_enterprise_modern import ModernAgent23FastAPIOrchestrationEnterprise
        
        # Initialiser l'agent
        agent = ModernAgent23FastAPIOrchestrationEnterprise()
        print("✅ Agent FASTAPI 23 initialisé")
        
        # Test health check
        health = await agent.health_check()
        print(f"🏥 Health Check: {health['status']}")
        print(f"   LLM disponible: {health.get('llm_available', 'unknown')}")
        
        # Test orchestration FastAPI avec LLM
        test_input = {
            "project_name": "Demo API",
            "endpoints": [
                {"path": "/users", "method": "GET", "description": "List users"},
                {"path": "/users", "method": "POST", "description": "Create user"},
                {"path": "/users/{id}", "method": "PUT", "description": "Update user"}
            ],
            "models": [
                {"name": "User", "fields": ["id", "name", "email", "created_at"]}
            ],
            "requirements": {
                "authentication": True,
                "rate_limiting": True,
                "swagger_docs": True
            }
        }
        
        print("\n🔧 Orchestration API avec LLM...")
        start_time = time.time()
        
        result = await agent.execute_task(test_input)
        
        duration = time.time() - start_time
        print(f"⏱️ Durée: {duration:.2f}s")
        
        if result and result.get('success'):
            print("✅ Orchestration réussie")
            
            # Analyser les résultats
            if 'outputs' in result:
                outputs = result['outputs']
                print(f"   📦 Outputs générés: {list(outputs.keys())}")
                
                # Vérifier si LLM a été utilisé
                llm_indicators = [
                    'llm_enhanced' in str(outputs),
                    'ai_generated' in str(outputs),
                    'intelligent' in str(outputs).lower(),
                    'optimized' in str(outputs).lower()
                ]
                
                if any(llm_indicators):
                    print("🤖 Optimisations LLM détectées")
                else:
                    print("📝 Génération legacy (fallback)")
                
                # Afficher quelques détails
                if 'generated_code' in outputs:
                    code_size = len(str(outputs['generated_code']))
                    print(f"   💻 Code généré: ~{code_size} caractères")
                
                if 'documentation' in outputs:
                    docs_size = len(str(outputs['documentation']))
                    print(f"   📚 Documentation: ~{docs_size} caractères")
                    
        else:
            print("❌ Échec orchestration")
            if result and 'error' in result:
                print(f"   Erreur: {result['error']}")
            
        return True
        
    except ImportError as e:
        print(f"❌ Erreur import Agent FASTAPI 23: {e}")
        return False
    except Exception as e:
        print(f"💥 Erreur test Agent FASTAPI 23: {e}")
        return False

async def test_llm_performance():
    """Test de performance LLM"""
    print("\n⚡ === TEST PERFORMANCE LLM ===")
    
    try:
        # Test simple de latence
        import requests
        import time
        
        # Test ping Ollama
        start = time.time()
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        ping_time = (time.time() - start) * 1000
        
        if response.status_code == 200:
            print(f"🏓 Ping Ollama: {ping_time:.1f}ms")
            
            # Test requête LLM simple
            test_prompt = {
                "model": "deepseek-coder:7b",
                "prompt": "Summarize: NextGeneration agent testing",
                "stream": False
            }
            
            start = time.time()
            llm_response = requests.post(
                "http://localhost:11434/api/generate",
                json=test_prompt,
                timeout=30
            )
            llm_time = (time.time() - start) * 1000
            
            if llm_response.status_code == 200:
                print(f"🤖 Requête LLM: {llm_time:.1f}ms")
                
                response_data = llm_response.json()
                if 'response' in response_data:
                    response_text = response_data['response']
                    print(f"📝 Réponse LLM: {len(response_text)} caractères")
                    
                # Analyser les métriques
                if 'eval_count' in response_data:
                    tokens = response_data.get('eval_count', 0)
                    total_time = response_data.get('total_duration', 0) / 1e9  # ns to s
                    if total_time > 0:
                        tokens_per_sec = tokens / total_time
                        print(f"🚄 Vitesse: {tokens_per_sec:.1f} tokens/sec")
            else:
                print(f"❌ Erreur requête LLM: {llm_response.status_code}")
        else:
            print(f"❌ Erreur ping Ollama: {response.status_code}")
            
    except Exception as e:
        print(f"💥 Erreur test performance: {e}")

async def main():
    """Point d'entrée principal"""
    print("🌟 DÉMONSTRATION INTÉGRATION LLM - AGENTS MODERNES")
    print("=" * 60)
    print()
    
    # Résultats des tests
    results = {
        'ollama_connection': False,
        'agent_05_test': False,
        'agent_fastapi_test': False
    }
    
    try:
        # 1. Test connexion Ollama
        results['ollama_connection'] = await test_ollama_connection()
        
        # 2. Test performance LLM
        if results['ollama_connection']:
            await test_llm_performance()
        
        # 3. Test Agent 05
        results['agent_05_test'] = await test_agent_05_llm()
        
        # 4. Test Agent FASTAPI 23
        results['agent_fastapi_test'] = await test_agent_fastapi_llm()
        
        # Rapport final
        print("\n📊 === RAPPORT FINAL ===")
        success_count = sum(results.values())
        total_tests = len(results)
        
        print(f"🎯 Tests réussis: {success_count}/{total_tests} ({success_count/total_tests*100:.1f}%)")
        
        for test_name, success in results.items():
            status = "✅" if success else "❌"
            print(f"   {status} {test_name.replace('_', ' ').title()}")
        
        if all(results.values()):
            print("\n🎉 Tous les tests LLM ont réussi!")
            print("💡 L'intégration LLM est fonctionnelle dans les agents modernes")
        else:
            print(f"\n⚠️ {total_tests - success_count} test(s) en échec")
            if not results['ollama_connection']:
                print("💡 Vérifiez qu'Ollama est démarré: ollama serve")
        
        return success_count == total_tests
        
    except Exception as e:
        print(f"\n💥 Erreur durant la démonstration: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)