#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Rapide Gemini - Version Windows
Tests de performance et fonctionnalit sans emojis Unicode
"""

import os
import sys
import time
from typing import Dict, List, Optional
import json
from datetime import datetime

# Chargement du fichier .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Si python-dotenv n'est pas install, on essaie de charger manuellement
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

# Configuration pour Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def test_import_gemini() -> bool:
    """Test d'importation rapide."""
    try:
        import google.generativeai as genai
        return True
    except ImportError:
        return False

def get_api_key() -> Optional[str]:
    """Rcupre la premire cl API disponible."""
    keys = [
        os.getenv('GOOGLE_API_KEY'),
        os.getenv('GEMINI_API_KEY')
    ]
    
    for key in keys:
        if key and key.strip():
            return key.strip()
    
    return None

def test_model_speed(api_key: str, model_name: str, prompt: str) -> Dict:
    """Test de vitesse d'un modle."""
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        start_time = time.time()
        response = model.generate_content(prompt)
        end_time = time.time()
        
        duration = end_time - start_time
        
        return {
            'success': True,
            'duration': duration,
            'response_length': len(response.text) if response.text else 0,
            'response_preview': response.text[:100] if response.text else "",
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'duration': 0,
            'response_length': 0,
            'response_preview': "",
            'error': str(e)
        }

def run_performance_tests(api_key: str) -> Dict:
    """Excute une srie de tests de performance."""
    
    test_cases = [
        {
            'name': 'Test Simple',
            'model': 'gemini-1.5-flash',
            'prompt': 'Bonjour, comment allez-vous?'
        },
        {
            'name': 'Test Code',
            'model': 'gemini-1.5-flash',
            'prompt': 'Ecrivez une fonction Python pour calculer la factorielle'
        },
        {
            'name': 'Test Analyse',
            'model': 'gemini-1.5-pro',
            'prompt': 'Analysez les avantages des microservices'
        }
    ]
    
    results = {}
    
    for test_case in test_cases:
        print(f"   {test_case['name']} avec {test_case['model']}...")
        
        result = test_model_speed(
            api_key, 
            test_case['model'], 
            test_case['prompt']
        )
        
        results[test_case['name']] = {
            'model': test_case['model'],
            'prompt': test_case['prompt'],
            **result
        }
        
        if result['success']:
            print(f"      REUSSI en {result['duration']:.2f}s")
            print(f"      Reponse: {result['response_preview'][:50]}...")
        else:
            print(f"      ECHEC: {result['error']}")
    
    return results

def analyze_performance(results: Dict) -> Dict:
    """Analyse les rsultats de performance."""
    successful_tests = [r for r in results.values() if r['success']]
    
    if not successful_tests:
        return {
            'average_speed': 0,
            'fastest_test': None,
            'slowest_test': None,
            'success_rate': 0,
            'total_tests': len(results)
        }
    
    durations = [r['duration'] for r in successful_tests]
    
    analysis = {
        'average_speed': sum(durations) / len(durations),
        'fastest_test': min(successful_tests, key=lambda x: x['duration']),
        'slowest_test': max(successful_tests, key=lambda x: x['duration']),
        'success_rate': len(successful_tests) / len(results) * 100,
        'total_tests': len(results),
        'successful_tests': len(successful_tests)
    }
    
    return analysis

def generate_recommendations(analysis: Dict, results: Dict) -> List[str]:
    """Gnre des recommandations bases sur les rsultats."""
    recommendations = []
    
    if analysis['success_rate'] == 100:
        recommendations.append("Excellent! Tous les tests ont reussi")
    elif analysis['success_rate'] >= 50:
        recommendations.append("Performance correcte, quelques optimisations possibles")
    else:
        recommendations.append("Problemes detectes, verification necessaire")
    
    if analysis['average_speed'] < 1.0:
        recommendations.append("Vitesse excellente (< 1s en moyenne)")
        recommendations.append("Ideal pour usage en temps reel")
    elif analysis['average_speed'] < 3.0:
        recommendations.append("Vitesse correcte (< 3s en moyenne)")
        recommendations.append("Convient pour la plupart des usages")
    else:
        recommendations.append("Vitesse lente (> 3s en moyenne)")
        recommendations.append("Optimisation recommandee")
    
    # Recommandations de modles
    flash_results = [r for r in results.values() if 'flash' in r.get('model', '')]
    pro_results = [r for r in results.values() if 'pro' in r.get('model', '')]
    
    if flash_results and all(r['success'] for r in flash_results):
        recommendations.append("gemini-1.5-flash recommande pour la rapidite")
    
    if pro_results and all(r['success'] for r in pro_results):
        recommendations.append("gemini-1.5-pro recommande pour la qualite")
    
    return recommendations

def main() -> int:
    """Fonction principale."""
    print("TEST RAPIDE GEMINI - PERFORMANCE")
    print("=" * 40)
    
    # Test d'importation
    print("1. Test d'importation...")
    if not test_import_gemini():
        print("   ECHEC: Module google-generativeai manquant")
        print("   Installer avec: pip install google-generativeai")
        return 1
    
    print("   OK: Module disponible")
    
    # Rcupration de la cl API
    print("\n2. Verification de la cle API...")
    api_key = get_api_key()
    
    if not api_key:
        print("   ECHEC: Aucune cle API trouvee")
        print("   Configurer GOOGLE_API_KEY ou GEMINI_API_KEY dans .env")
        return 1
    
    print("   OK: Cle API disponible")
    
    # Tests de performance
    print("\n3. Tests de performance...")
    start_time = time.time()
    
    results = run_performance_tests(api_key)
    
    total_time = time.time() - start_time
    
    # Analyse des rsultats
    print("\n4. Analyse des resultats...")
    analysis = analyze_performance(results)
    
    print(f"   Tests executes: {analysis['total_tests']}")
    print(f"   Tests reussis: {analysis['successful_tests']}")
    print(f"   Taux de reussite: {analysis['success_rate']:.1f}%")
    
    if analysis['successful_tests'] > 0:
        print(f"   Temps moyen: {analysis['average_speed']:.2f}s")
        print(f"   Test le plus rapide: {analysis['fastest_test']['duration']:.2f}s")
        print(f"   Test le plus lent: {analysis['slowest_test']['duration']:.2f}s")
    
    # Recommandations
    print("\n5. Recommandations...")
    recommendations = generate_recommendations(analysis, results)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    # Rsultats finaux
    print("\n" + "=" * 40)
    
    if analysis['success_rate'] >= 50:
        print("RESULTAT: Tests reussis!")
        print("Gemini est pret pour l'integration")
        
        print("\nProchaines etapes:")
        print("1. Integrer dans l'orchestrateur")
        print("2. Configurer les modeles optimaux")
        print("3. Tester en production")
        
        # Sauvegarde des rsultats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"gemini_performance_report_{timestamp}.json"
        
        full_report = {
            'timestamp': datetime.now().isoformat(),
            'total_duration': total_time,
            'analysis': analysis,
            'results': results,
            'recommendations': recommendations
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(full_report, f, indent=2, ensure_ascii=False)
        
        print(f"\nRapport sauvegarde: {report_file}")
        
        return 0
    else:
        print("RESULTAT: Tests partiellement echoues")
        print("Verification necessaire")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nInterrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        sys.exit(1) 



