#!/usr/bin/env python3
"""
🔍 Test Simple Intégration LLM - Agents Modernes
================================================

Test simplifié pour vérifier l'intégration LLM sans dépendances complexes.
Focus sur la vérification de la connexion LLM et l'analyse du code.

Auteur: Claude Code
Date: 2025-06-28
"""

import asyncio
import sys
import json
import time
import re
from pathlib import Path
from typing import Dict, Any, Optional

async def test_ollama_connection():
    """Test de connexion à Ollama"""
    print("🔍 === TEST CONNEXION OLLAMA ===")
    
    try:
        import requests
        
        # Test de base
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama connecté - {len(models)} modèles disponibles")
            
            # Afficher les modèles
            available_models = []
            for model in models:
                name = model.get('name', 'unknown')
                size = model.get('size', 0) / (1024**3)  # GB
                available_models.append(name)
                print(f"   📦 {name} ({size:.1f}GB)")
            
            return True, available_models
        else:
            print(f"❌ Ollama non accessible (status: {response.status_code})")
            return False, []
    except Exception as e:
        print(f"❌ Erreur connexion Ollama: {e}")
        print("💡 Pour démarrer Ollama: ollama serve")
        return False, []

async def test_llm_simple_query(models):
    """Test d'une requête LLM simple"""
    print("\n🤖 === TEST REQUÊTE LLM SIMPLE ===")
    
    if not models:
        print("❌ Aucun modèle disponible")
        return False
    
    # Choisir le premier modèle disponible
    model_name = models[0]
    print(f"🎯 Utilisation du modèle: {model_name}")
    
    try:
        import requests
        
        # Requête simple
        prompt = {
            "model": model_name,
            "prompt": "Analyse ce rapport de test: 150 tests exécutés, 142 réussis, 8 échecs, couverture 87%. Donne 3 recommandations courtes.",
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9
            }
        }
        
        print("📤 Envoi requête LLM...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=prompt,
            timeout=30
        )
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '')
            
            print(f"✅ Réponse LLM reçue ({duration:.2f}s)")
            print(f"📝 Longueur réponse: {len(response_text)} caractères")
            
            # Afficher un extrait de la réponse
            if response_text:
                preview = response_text[:200] + "..." if len(response_text) > 200 else response_text
                print(f"📋 Aperçu réponse:\n{preview}")
                
                # Analyser la qualité de la réponse
                has_recommendations = any(word in response_text.lower() 
                                        for word in ['recommand', 'suggest', 'améliorer', 'optimiser'])
                has_analysis = any(word in response_text.lower() 
                                 for word in ['analyse', 'qualité', 'couverture', 'tests'])
                
                if has_recommendations and has_analysis:
                    print("🎯 Réponse semble pertinente (analyse + recommandations)")
                else:
                    print("⚠️ Réponse basique")
                
                # Métriques de performance
                if 'eval_count' in result:
                    tokens = result.get('eval_count', 0)
                    total_time = result.get('total_duration', 0) / 1e9  # ns to s
                    if total_time > 0:
                        tokens_per_sec = tokens / total_time
                        print(f"🚄 Performance: {tokens_per_sec:.1f} tokens/sec")
                
                return True
            else:
                print("❌ Réponse vide")
                return False
        else:
            print(f"❌ Erreur requête: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"💥 Erreur test LLM: {e}")
        return False

def analyze_agent_llm_integration(agent_path: Path):
    """Analyse l'intégration LLM dans un agent"""
    print(f"\n🔍 === ANALYSE INTÉGRATION LLM: {agent_path.name} ===")
    
    try:
        with open(agent_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 Taille fichier: {len(content)} caractères")
        
        # Rechercher les patterns LLM
        llm_patterns = {
            'llm_gateway': r'llm_gateway|LLMGateway',
            'llm_methods': r'def.*llm.*\(',
            'llm_calls': r'await.*llm|llm.*query|llm.*process',
            'llm_config': r'llm_config|ollama|deepseek',
            'fallback': r'fallback|legacy.*method|except.*llm',
            'modern_features': r'modern_features|llm_enhanced'
        }
        
        results = {}
        for pattern_name, pattern in llm_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            results[pattern_name] = len(matches)
            if matches:
                print(f"   ✅ {pattern_name}: {len(matches)} occurrences")
            else:
                print(f"   ❌ {pattern_name}: non trouvé")
        
        # Rechercher des méthodes spécifiques LLM
        llm_specific_methods = [
            '_get_llm_insights',
            '_orchestrate_fastapi_with_llm',
            '_generate_fastapi_code',
            '_generate_smart_documentation',
            '_perform_security_assessment'
        ]
        
        found_methods = []
        for method in llm_specific_methods:
            if method in content:
                found_methods.append(method)
        
        if found_methods:
            print(f"   🎯 Méthodes LLM trouvées: {', '.join(found_methods)}")
        else:
            print("   ⚠️ Aucune méthode LLM spécifique trouvée")
        
        # Vérifier la configuration LLM
        has_llm_config = any(config in content.lower() for config in [
            'localhost:11434', 'ollama', 'llm_gateway', 'deepseek'
        ])
        
        if has_llm_config:
            print("   🔧 Configuration LLM détectée")
        else:
            print("   ⚠️ Configuration LLM non visible")
        
        # Score d'intégration LLM
        total_indicators = sum(1 for count in results.values() if count > 0)
        max_indicators = len(results)
        integration_score = (total_indicators / max_indicators) * 100
        
        print(f"   📊 Score intégration LLM: {integration_score:.1f}% ({total_indicators}/{max_indicators})")
        
        return {
            'agent': agent_path.name,
            'integration_score': integration_score,
            'llm_methods': found_methods,
            'has_config': has_llm_config,
            'patterns': results
        }
        
    except Exception as e:
        print(f"❌ Erreur analyse {agent_path.name}: {e}")
        return None

async def main():
    """Point d'entrée principal"""
    print("🔍 TEST SIMPLE INTÉGRATION LLM - AGENTS MODERNES")
    print("=" * 55)
    print()
    
    results = {
        'ollama_available': False,
        'llm_query_test': False,
        'agents_analyzed': []
    }
    
    try:
        # 1. Test connexion Ollama
        ollama_ok, models = await test_ollama_connection()
        results['ollama_available'] = ollama_ok
        
        # 2. Test requête LLM si Ollama disponible
        if ollama_ok and models:
            llm_test_ok = await test_llm_simple_query(models)
            results['llm_query_test'] = llm_test_ok
        else:
            print("\n⚠️ Ollama non disponible - test LLM ignoré")
        
        # 3. Analyse des agents modernes
        agents_dir = Path(__file__).parent.parent / 'agents' / 'modern'
        target_agents = [
            'agent_05_maitre_tests_validation_modern_fixed.py',
            'agent_FASTAPI_23_orchestration_enterprise_modern.py'
        ]
        
        for agent_file in target_agents:
            agent_path = agents_dir / agent_file
            if agent_path.exists():
                analysis = analyze_agent_llm_integration(agent_path)
                if analysis:
                    results['agents_analyzed'].append(analysis)
            else:
                print(f"⚠️ Agent non trouvé: {agent_file}")
        
        # 4. Rapport final
        print("\n📊 === RAPPORT FINAL ===")
        
        # Status Ollama
        if results['ollama_available']:
            print("✅ Ollama: Connecté et fonctionnel")
            if results['llm_query_test']:
                print("✅ LLM: Requêtes fonctionnelles")
            else:
                print("⚠️ LLM: Connexion OK mais requêtes échouent")
        else:
            print("❌ Ollama: Non disponible")
            print("💡 Pour démarrer: ollama serve")
        
        # Analyse agents
        if results['agents_analyzed']:
            print(f"\n🤖 Agents analysés: {len(results['agents_analyzed'])}")
            
            for analysis in results['agents_analyzed']:
                score = analysis['integration_score']
                status = "✅" if score >= 70 else "⚠️" if score >= 40 else "❌"
                print(f"   {status} {analysis['agent']}: {score:.1f}% intégration LLM")
                
                if analysis['llm_methods']:
                    print(f"      🎯 Méthodes: {len(analysis['llm_methods'])}")
                
                if analysis['has_config']:
                    print(f"      🔧 Configuration: OK")
        
        # Recommandations
        print("\n💡 === RECOMMANDATIONS ===")
        
        if not results['ollama_available']:
            print("1. Démarrer Ollama: ollama serve")
            print("2. Installer un modèle: ollama pull deepseek-coder:7b")
        elif not results['llm_query_test']:
            print("1. Vérifier les modèles disponibles: ollama list")
            print("2. Tester manuellement: ollama run deepseek-coder:7b")
        else:
            print("✅ Infrastructure LLM opérationnelle")
            
            if results['agents_analyzed']:
                avg_score = sum(a['integration_score'] for a in results['agents_analyzed']) / len(results['agents_analyzed'])
                if avg_score >= 70:
                    print("✅ Intégration LLM des agents semble fonctionnelle")
                else:
                    print("⚠️ Intégration LLM des agents à améliorer")
        
        return all([
            results['ollama_available'] or results['llm_query_test'],
            len(results['agents_analyzed']) > 0
        ])
        
    except Exception as e:
        print(f"\n💥 Erreur durant les tests: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)