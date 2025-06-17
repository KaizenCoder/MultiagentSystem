#!/usr/bin/env python3
"""
Test et benchmark de vos modèles Ollama existants.
Analyse les performances et recommande le meilleur modèle selon le cas d'usage.
"""

import httpx
import time
import json
import asyncio
from typing import Dict, List, Any

class OllamaModelTester:
    """Classe pour tester et benchmarker les modèles Ollama."""
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.available_models = []
    
    async def get_available_models(self) -> List[str]:
        """Récupère la liste des modèles installés."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.ollama_url}/api/tags")
                
            if response.status_code == 200:
                data = response.json()
                models = [model["name"] for model in data.get("models", [])]
                self.available_models = models
                return models
            else:
                print(f"❌ Erreur récupération modèles: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Erreur connexion Ollama: {e}")
            return []
    
    async def test_model_performance(self, model_name: str, prompt: str) -> Dict[str, Any]:
        """Test les performances d'un modèle spécifique."""
        print(f"🔍 Test {model_name}: {prompt[:40]}...")
        
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
                
                # Calcul des métriques
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
        """Benchmark tous les modèles avec différents types de prompts."""
        print("🚀 BENCHMARK COMPLET DE VOS MODÈLES OLLAMA")
        print("=" * 60)
        
        # Prompts de test pour différents cas d'usage
        test_prompts = {
            "simple": "Dis bonjour en français",
            "creative": "Écris un haiku sur l'intelligence artificielle",
            "analytical": "Analyse les avantages et inconvénients du télétravail",
            "code": "Écris une fonction Python pour calculer la factorielle d'un nombre",
            "reasoning": "Si un train part de Paris à 10h à 120km/h vers Lyon (400km), à quelle heure arrive-t-il ?"
        }
        
        models = await self.get_available_models()
        
        if not models:
            print("❌ Aucun modèle trouvé")
            return {}
        
        print(f"📋 {len(models)} modèles détectés")
        print(f"🧪 {len(test_prompts)} tests par modèle")
        print("\n" + "=" * 60)
        
        results = {}
        
        for model in models:
            print(f"\n🤖 Test du modèle: {model}")
            print("-" * 40)
            
            model_results = []
            
            for test_type, prompt in test_prompts.items():
                result = await self.test_model_performance(model, prompt)
                result["test_type"] = test_type
                model_results.append(result)
                
                if result["success"]:
                    print(f"   ✅ {test_type}: {result['tokens_per_second']:.1f} tok/s ({result['total_time']:.1f}s)")
                else:
                    print(f"   ❌ {test_type}: {result['error']}")
                
                # Pause entre les tests pour éviter la surcharge
                await asyncio.sleep(2)
            
            results[model] = model_results
        
        return results
    
    def analyze_results(self, results: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Analyse les résultats et fournit des recommandations."""
        print("\n" + "=" * 60)
        print("📊 ANALYSE DES PERFORMANCES")
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
            
            print(f"\n🤖 {model}:")
            print(f"   ⚡ Vitesse moyenne: {avg_speed:.1f} tokens/sec")
            print(f"   ⏱️ Temps moyen: {avg_time:.1f}s")
            print(f"   ✅ Taux succès: {success_rate:.0f}%")
        
        # Déterminer les meilleurs modèles par catégorie
        if model_stats:
            # Plus rapide
            fastest = max(model_stats.keys(), key=lambda m: model_stats[m]["avg_speed"])
            analysis["fastest_model"] = fastest
            
            # Plus fiable (meilleur taux de succès)
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
        print("🎯 RECOMMANDATIONS PERSONNALISÉES")
        print("=" * 60)
        
        reco = analysis.get("recommendations", {})
        
        print(f"⚡ **Pour la VITESSE**: {reco.get('speed', 'N/A')}")
        print(f"🌟 **Pour la QUALITÉ**: {reco.get('quality', 'N/A')}")
        print(f"💻 **Pour le CODE**: {reco.get('code', 'N/A')}")
        print(f"📱 **Usage QUOTIDIEN**: {reco.get('daily_use', 'N/A')}")
        
        print(f"\n🏆 **MODÈLE LE PLUS RAPIDE**: {analysis.get('fastest_model', 'N/A')}")
        print(f"🛡️ **MODÈLE LE PLUS FIABLE**: {analysis.get('most_reliable_model', 'N/A')}")
        
        print("\n💡 **Conseils d'utilisation:**")
        print("   - Utilisez le modèle rapide pour les tâches simples")
        print("   - Utilisez le modèle qualité pour les analyses complexes")
        print("   - Utilisez le modèle code pour la programmation")
        print("   - Gardez 2-3 modèles maximum selon vos besoins")

async def main():
    """Fonction principale pour tester tous vos modèles."""
    tester = OllamaModelTester()
    
    print("🔍 Vérification de la connexion Ollama...")
    models = await tester.get_available_models()
    
    if not models:
        print("❌ Impossible de se connecter à Ollama")
        print("💡 Vérifiez qu'Ollama est démarré: ollama serve")
        return
    
    print(f"✅ {len(models)} modèles détectés")
    
    # Benchmark complet
    results = await tester.benchmark_all_models()
    
    # Analyse et recommandations
    analysis = tester.analyze_results(results)
    tester.print_recommendations(analysis)
    
    # Sauvegarde des résultats
    try:
        with open("ollama_benchmark_results.json", "w", encoding="utf-8") as f:
            json.dump({
                "results": results,
                "analysis": analysis
            }, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Résultats sauvegardés dans: ollama_benchmark_results.json")
    except Exception as e:
        print(f"⚠️ Impossible de sauvegarder: {e}")
    
    print("\n🎉 Benchmark terminé ! Vos modèles sont maintenant analysés.")

if __name__ == "__main__":
    asyncio.run(main())
