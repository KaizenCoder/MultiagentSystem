#!/usr/bin/env python3
"""
Test et benchmark de vos modles Ollama existants.
Analyse les performances et recommande le meilleur modle selon le cas d'usage.
"""

import httpx
import time
import json
import asyncio
from typing import Dict, List, Any

class OllamaModelTester:
    """Classe pour tester et benchmarker les modles Ollama."""
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.available_models = []
    
    async def get_available_models(self) -> List[str]:
        """Rcupre la liste des modles installs."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.ollama_url}/api/tags")
                
            if response.status_code == 200:
                data = response.json()
                models = [model["name"] for model in data.get("models", [])]
                self.available_models = models
                return models
            else:
                print(f"[CROSS] Erreur rcupration modles: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"[CROSS] Erreur connexion Ollama: {e}")
            return []
    
    async def test_model_performance(self, model_name: str, prompt: str) -> Dict[str, Any]:
        """Test les performances d'un modle spcifique."""
        print(f"[SEARCH] Test {model_name}: {prompt[:40]}...")
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_ctx": 2048,
                "num_predict": 100
            }
        }
        
        try:
            start_time = time.time()
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload
                )
            
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "")
                
                # Calcul des mtriques
                total_time = end_time - start_time
                tokens = len(response_text.split())
                tokens_per_second = tokens / total_time if total_time > 0 else 0
                
                return {
                    "success": True,
                    "model": model_name,
                    "response": response_text,
                    "total_time": total_time,
                    "tokens": tokens,
                    "tokens_per_second": tokens_per_second,
                    "eval_count": result.get("eval_count", 0),
                    "load_duration": result.get("load_duration", 0) / 1e9  # ns to s
                }
            else:
                return {
                    "success": False,
                    "model": model_name,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "model": model_name,
                "error": str(e)
            }
    
    async def benchmark_all_models(self) -> Dict[str, List[Dict]]:
        """Benchmark tous les modles avec diffrents types de prompts."""
        print("[ROCKET] BENCHMARK COMPLET DE VOS MODLES OLLAMA")
        print("=" * 60)
        
        # Prompts de test pour diffrents cas d'usage
        test_prompts = {
            "simple": "Dis bonjour en franais",
            "creative": "cris un haiku sur l'intelligence artificielle",
            "analytical": "Analyse les avantages et inconvnients du tltravail",
            "code": "cris une fonction Python pour calculer la factorielle d'un nombre",
            "reasoning": "Si un train part de Paris  10h  120km/h vers Lyon (400km),  quelle heure arrive-t-il ?"
        }
        
        models = await self.get_available_models()
        
        if not models:
            print("[CROSS] Aucun modle trouv")
            return {}
        
        print(f"[CLIPBOARD] {len(models)} modles dtects")
        print(f" {len(test_prompts)} tests par modle")
        print("\n" + "=" * 60)
        
        results = {}
        
        for model in models:
            print(f"\n[ROBOT] Test du modle: {model}")
            print("-" * 40)
            
            model_results = []
            
            for test_type, prompt in test_prompts.items():
                result = await self.test_model_performance(model, prompt)
                result["test_type"] = test_type
                model_results.append(result)
                
                if result["success"]:
                    print(f"   [CHECK] {test_type}: {result['tokens_per_second']:.1f} tok/s ({result['total_time']:.1f}s)")
                else:
                    print(f"   [CROSS] {test_type}: {result['error']}")
                
                # Pause entre les tests pour viter la surcharge
                await asyncio.sleep(2)
            
            results[model] = model_results
        
        return results
    
    def analyze_results(self, results: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Analyse les rsultats et fournit des recommandations."""
        print("\n" + "=" * 60)
        print("[CHART] ANALYSE DES PERFORMANCES")
        print("=" * 60)
        
        analysis = {
            "fastest_model": None,
            "best_quality_model": None,
            "best_code_model": None,
            "most_reliable_model": None,
            "recommendations": {}
        }
        
        model_stats = {}
        
        for model, model_results in results.items():
            successful_tests = [r for r in model_results if r["success"]]
            
            if not successful_tests:
                continue
            
            avg_speed = sum(r["tokens_per_second"] for r in successful_tests) / len(successful_tests)
            avg_time = sum(r["total_time"] for r in successful_tests) / len(successful_tests)
            success_rate = len(successful_tests) / len(model_results) * 100
            
            model_stats[model] = {
                "avg_speed": avg_speed,
                "avg_time": avg_time,
                "success_rate": success_rate,
                "successful_tests": len(successful_tests)
            }
            
            print(f"\n[ROBOT] {model}:")
            print(f"   [LIGHTNING] Vitesse moyenne: {avg_speed:.1f} tokens/sec")
            print(f"    Temps moyen: {avg_time:.1f}s")
            print(f"   [CHECK] Taux succs: {success_rate:.0f}%")
        
        # Dterminer les meilleurs modles par catgorie
        if model_stats:
            # Plus rapide
            fastest = max(model_stats.keys(), key=lambda m: model_stats[m]["avg_speed"])
            analysis["fastest_model"] = fastest
            
            # Plus fiable (meilleur taux de succs)
            most_reliable = max(model_stats.keys(), key=lambda m: model_stats[m]["success_rate"])
            analysis["most_reliable_model"] = most_reliable
            
            # Recommandations par cas d'usage
            large_models = [m for m in model_stats.keys() if "32b" in m or "33b" in m or "70b" in m or "mixtral" in m]
            code_models = [m for m in model_stats.keys() if "coder" in m or "code" in m]
            fast_models = [m for m in model_stats.keys() if "7b" in m or "8b" in m]
            
            analysis["recommendations"] = {
                "speed": fastest,
                "quality": large_models[0] if large_models else fastest,
                "code": code_models[0] if code_models else fastest,
                "daily_use": fast_models[0] if fast_models else fastest
            }
        
        return analysis
    
    def print_recommendations(self, analysis: Dict[str, Any]):
        """Affiche les recommandations finales."""
        print("\n" + "=" * 60)
        print("[TARGET] RECOMMANDATIONS PERSONNALISES")
        print("=" * 60)
        
        reco = analysis.get("recommendations", {})
        
        print(f"[LIGHTNING] **Pour la VITESSE**: {reco.get('speed', 'N/A')}")
        print(f" **Pour la QUALIT**: {reco.get('quality', 'N/A')}")
        print(f" **Pour le CODE**: {reco.get('code', 'N/A')}")
        print(f" **Usage QUOTIDIEN**: {reco.get('daily_use', 'N/A')}")
        
        print(f"\n **MODLE LE PLUS RAPIDE**: {analysis.get('fastest_model', 'N/A')}")
        print(f" **MODLE LE PLUS FIABLE**: {analysis.get('most_reliable_model', 'N/A')}")
        
        print("\n[BULB] **Conseils d'utilisation:**")
        print("   - Utilisez le modle rapide pour les tches simples")
        print("   - Utilisez le modle qualit pour les analyses complexes")
        print("   - Utilisez le modle code pour la programmation")
        print("   - Gardez 2-3 modles maximum selon vos besoins")

async def main():
    """Fonction principale pour tester tous vos modles."""
    tester = OllamaModelTester()
    
    print("[SEARCH] Vrification de la connexion Ollama...")
    models = await tester.get_available_models()
    
    if not models:
        print("[CROSS] Impossible de se connecter  Ollama")
        print("[BULB] Vrifiez qu'Ollama est dmarr: ollama serve")
        return
    
    print(f"[CHECK] {len(models)} modles dtects")
    
    # Benchmark complet
    results = await tester.benchmark_all_models()
    
    # Analyse et recommandations
    analysis = tester.analyze_results(results)
    tester.print_recommendations(analysis)
    
    # Sauvegarde des rsultats
    try:
        with open("ollama_benchmark_results.json", "w", encoding="utf-8") as f:
            json.dump({
                "results": results,
                "analysis": analysis
            }, f, indent=2, ensure_ascii=False)
        print(f"\n Rsultats sauvegards dans: ollama_benchmark_results.json")
    except Exception as e:
        print(f" Impossible de sauvegarder: {e}")
    
    print("\n Benchmark termin ! Vos modles sont maintenant analyss.")

if __name__ == "__main__":
    asyncio.run(main())




