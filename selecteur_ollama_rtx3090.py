#!/usr/bin/env python3
"""
 Slecteur Automatique RTX 3090 - SuperWhisper V6
Exploite intelligemment vos 5 modles Ollama optimiss.

Configuration: RTX 5060 Ti + RTX 3090 (GPU principale IA)
Modles: Mixtral, Qwen-Coder, Llama3, Nous-Hermes, Qwen-Mini
"""

import os
import asyncio
import httpx
import time
import json
from typing import Dict, Any, Optional
from datetime import datetime

# ============================================================================
#  CONFIGURATION RTX 3090 - STANDARDS SUPERWHISPER V6
# ============================================================================
os.environ['CUDA_VISIBLE_DEVICES'] = '1'        # RTX 3090 uniquement
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'  # Force ordre bus physique
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:1024'

print(" SuperWhisper V6 - Slecteur Ollama RTX 3090")
print(f" Configuration GPU: RTX 3090 (device {os.environ.get('CUDA_VISIBLE_DEVICES')})")

class RTX3090OllamaSelector:
    """
    Slecteur intelligent pour vos modles Ollama sur RTX 3090.
    Adapt  votre configuration multi-GPU SuperWhisper V6.
    """
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.rtx3090_vram_total = 24.0  # GB
        
        # VOS MODLES ACTUELS - Configuration optimise
        self.models = {
            "speed": {
                "name": "nous-hermes-2-mistral-7b-dpo:latest",
                "vram_gb": 4.1,
                "tokens_per_sec": 6,
                "quality_score": 7,
                "speciality": "Rponses ultra-rapides",
                "use_cases": ["quick", "fast", "brief", "chat", "simple"],
                "temperature_optimal": 0.7,
                "max_tokens_optimal": 512
            },
            "quality": {
                "name": "mixtral-8x7b:latest",
                "vram_gb": 26.0,
                "tokens_per_sec": 1,
                "quality_score": 10,
                "speciality": "Qualit exceptionnelle",
                "use_cases": ["analysis", "complex", "detailed", "research", "deep"],
                "temperature_optimal": 0.3,
                "max_tokens_optimal": 4096
            },
            "code": {
                "name": "qwen-coder-32b:latest",
                "vram_gb": 19.0,
                "tokens_per_sec": 2,
                "quality_score": 9,
                "speciality": "Spcialiste dveloppement",
                "use_cases": ["code", "programming", "python", "javascript", "debug", "refactor"],
                "temperature_optimal": 0.1,
                "max_tokens_optimal": 2048
            },
            "daily": {
                "name": "llama3:8b-instruct-q6_k",
                "vram_gb": 6.6,
                "tokens_per_sec": 4,
                "quality_score": 8,
                "speciality": "Usage quotidien quilibr",
                "use_cases": ["general", "summary", "explain", "moderate"],
                "temperature_optimal": 0.5,
                "max_tokens_optimal": 1024
            },
            "mini": {
                "name": "qwen2.5-coder:1.5b",
                "vram_gb": 1.0,
                "tokens_per_sec": 10,
                "quality_score": 6,
                "speciality": "Tests express",
                "use_cases": ["test", "experiment", "prototype", "minimal"],
                "temperature_optimal": 0.4,
                "max_tokens_optimal": 256
            }
        }
        
        print(f"[CHECK] Configur avec {len(self.models)} modles RTX 3090 optimiss")
    
    def analyze_task(self, task: str, priority: str = "auto") -> Dict[str, Any]:
        """Analyse la tche et dtermine le modle optimal."""
        
        task_lower = task.lower()
        task_length = len(task)
        
        analysis = {
            "task_length": task_length,
            "complexity": "low",
            "category": "general",
            "keywords_detected": [],
            "recommended_model": "daily",
            "confidence": 0.5
        }
        
        # Priorit manuelle
        if priority in self.models:
            analysis["recommended_model"] = priority
            analysis["confidence"] = 1.0
            analysis["reason"] = f"Priorit manuelle: {priority}"
            return analysis
        
        # Dtection par mots-cls
        for model_key, model_info in self.models.items():
            for keyword in model_info["use_cases"]:
                if keyword in task_lower:
                    analysis["keywords_detected"].append(keyword)
                    analysis["recommended_model"] = model_key
                    analysis["confidence"] += 0.2
        
        # Ajustement par longueur
        if task_length > 300:
            analysis["complexity"] = "high"
            if analysis["recommended_model"] not in ["quality", "code"]:
                analysis["recommended_model"] = "quality"
                analysis["confidence"] += 0.3
        elif task_length < 50:
            analysis["complexity"] = "low"
            if analysis["recommended_model"] not in ["speed", "mini"]:
                analysis["recommended_model"] = "speed"
                analysis["confidence"] += 0.2
        
        # Limiter confiance
        analysis["confidence"] = min(analysis["confidence"], 1.0)
        
        return analysis
    
    async def check_model_availability(self, model_name: str) -> bool:
        """Vrifie si le modle est disponible dans Ollama."""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.ollama_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    available_models = [m["name"] for m in models]
                    return model_name in available_models
                return False
        except Exception as e:
            print(f"  Erreur vrification modle {model_name}: {e}")
            return False
    
    async def process_task(self, 
                          task: str, 
                          priority: str = "auto",
                          temperature: Optional[float] = None,
                          max_tokens: Optional[int] = None,
                          stream: bool = False) -> Dict[str, Any]:
        """
        Traite la tche avec le modle optimal.
        
        Args:
            task: La tche  traiter
            priority: Priorit manuelle (auto, speed, quality, code, daily, mini)
            temperature: Temprature personnalise
            max_tokens: Nombre de tokens personnalis
            stream: Mode streaming
        """
        
        start_time = time.time()
        
        # Analyse de la tche
        analysis = self.analyze_task(task, priority)
        model_key = analysis["recommended_model"]
        model_info = self.models[model_key]
        model_name = model_info["name"]
        
        print(f"\n[TARGET] SLECTION AUTOMATIQUE RTX 3090")
        print(f" Tche: {task[:100]}{'...' if len(task) > 100 else ''}")
        print(f"[ROBOT] Modle: {model_key}  {model_name}")
        print(f"[CHART] VRAM: {model_info['vram_gb']}GB / {self.rtx3090_vram_total}GB RTX 3090")
        print(f"[LIGHTNING] Vitesse: ~{model_info['tokens_per_sec']} tokens/sec")
        print(f"[TARGET] Spcialit: {model_info['speciality']}")
        print(f"[SEARCH] Confiance: {analysis['confidence']:.1%}")
        
        # Vrifier disponibilit
        if not await self.check_model_availability(model_name):
            print(f"  Modle {model_name} non disponible, fallback vers daily")
            model_key = "daily"
            model_info = self.models[model_key]
            model_name = model_info["name"]
        
        # Paramtres optimaux
        temp = temperature if temperature is not None else model_info["temperature_optimal"]
        tokens = max_tokens if max_tokens is not None else model_info["max_tokens_optimal"]
        
        try:
            # Appel Ollama
            async with httpx.AsyncClient(timeout=300) as client:
                payload = {
                    "model": model_name,
                    "prompt": task,
                    "stream": stream,
                    "options": {
                        "temperature": temp,
                        "top_p": 0.9,
                        "max_tokens": tokens
                    }
                }
                
                print(f" Traitement en cours...")
                response = await client.post(f"{self.ollama_url}/api/generate", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    processing_time = time.time() - start_time
                    
                    # Calculer stats
                    response_text = result.get("response", "")
                    tokens_generated = len(response_text.split())
                    tokens_per_sec_actual = tokens_generated / processing_time if processing_time > 0 else 0
                    
                    print(f"[CHECK] Traitement termin en {processing_time:.1f}s")
                    print(f" Performance: {tokens_per_sec_actual:.1f} tokens/sec")
                    
                    return {
                        "success": True,
                        "response": response_text,
                        "model_used": {
                            "name": model_name,
                            "category": model_key,
                            "vram_gb": model_info["vram_gb"],
                            "speciality": model_info["speciality"]
                        },
                        "task_analysis": analysis,
                        "performance": {
                            "processing_time": processing_time,
                            "tokens_generated": tokens_generated,
                            "tokens_per_sec": tokens_per_sec_actual,
                            "expected_tokens_per_sec": model_info["tokens_per_sec"]
                        },
                        "parameters": {
                            "temperature": temp,
                            "max_tokens": tokens
                        },
                        "gpu_info": {
                            "device": "RTX 3090",
                            "vram_used_gb": model_info["vram_gb"],
                            "vram_total_gb": self.rtx3090_vram_total,
                            "usage_percent": (model_info["vram_gb"] / self.rtx3090_vram_total) * 100
                        },
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    raise Exception(f"Erreur HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"[CROSS] Erreur traitement: {e}")
            return {
                "success": False,
                "error": str(e),
                "model_attempted": model_name,
                "processing_time": time.time() - start_time
            }
    
    def get_model_recommendations(self) -> Dict[str, Any]:
        """Retourne des recommandations d'usage pour vos modles."""
        
        recommendations = {
            "rtx3090_optimization": {
                "total_vram": f"{self.rtx3090_vram_total}GB",
                "concurrent_small_models": 5,  # Nous-Hermes: 4.1GB * 5 = 20.5GB
                "concurrent_medium_models": 3,  # Llama3: 6.6GB * 3 = 19.8GB
                "exclusive_large_models": ["quality"]  # Mixtral: 26GB
            },
            "workflow_suggestions": {
                "development": ["mini", "code", "daily"],
                "analysis": ["daily", "quality"],
                "quick_tasks": ["speed", "mini"],
                "production": ["code", "quality"]
            },
            "model_details": self.models
        }
        
        return recommendations

# ============================================================================
#  FONCTIONS DE TEST ET DMONSTRATION
# ============================================================================

async def test_selector():
    """Test du slecteur avec diffrents types de tches."""
    
    selector = RTX3090OllamaSelector()
    
    test_tasks = [
        {
            "task": "cris une fonction Python pour traiter des CSV",
            "priority": "auto",
            "expected": "code"
        },
        {
            "task": "Analyse cette architecture microservices complexe et propose des amliorations dtailles",
            "priority": "auto", 
            "expected": "quality"
        },
        {
            "task": "Bonjour, comment allez-vous ?",
            "priority": "auto",
            "expected": "speed"
        },
        {
            "task": "Test rapide",
            "priority": "mini",
            "expected": "mini"
        }
    ]
    
    print(" TEST DU SLECTEUR AUTOMATIQUE RTX 3090")
    print("=" * 60)
    
    for i, test in enumerate(test_tasks, 1):
        print(f"\n[CLIPBOARD] Test {i}/{len(test_tasks)}")
        
        result = await selector.process_task(
            test["task"], 
            priority=test["priority"]
        )
        
        if result["success"]:
            model_used = result["model_used"]["category"]
            print(f"[CHECK] Modle attendu: {test['expected']}, utilis: {model_used}")
            print(f" Performance: {result['performance']['tokens_per_sec']:.1f} tokens/sec")
        else:
            print(f"[CROSS] Erreur: {result['error']}")
        
        print("-" * 40)

async def interactive_mode():
    """Mode interactif pour tester vos modles."""
    
    selector = RTX3090OllamaSelector()
    
    print("\n MODE INTERACTIF RTX 3090")
    print("Tapez vos questions, 'quit' pour quitter")
    print("Priorits disponibles: auto, speed, quality, code, daily, mini")
    print("=" * 60)
    
    while True:
        try:
            task = input("\n Votre tche: ").strip()
            
            if task.lower() in ["quit", "exit", "q"]:
                print(" Au revoir !")
                break
            
            if not task:
                continue
            
            priority = input("[TARGET] Priorit (auto): ").strip() or "auto"
            
            result = await selector.process_task(task, priority=priority)
            
            if result["success"]:
                print(f"\n[ROBOT] Rponse ({result['model_used']['name']}):")
                print(f"{result['response']}")
                print(f"\n[CHART] Stats: {result['performance']['processing_time']:.1f}s, {result['performance']['tokens_per_sec']:.1f} tok/s")
            else:
                print(f"[CROSS] Erreur: {result['error']}")
                
        except KeyboardInterrupt:
            print("\n\n Interruption utilisateur, au revoir !")
            break
        except Exception as e:
            print(f"[CROSS] Erreur inattendue: {e}")

def show_recommendations():
    """Affiche les recommandations d'usage."""
    
    selector = RTX3090OllamaSelector()
    recommendations = selector.get_model_recommendations()
    
    print("[TARGET] RECOMMANDATIONS RTX 3090")
    print("=" * 50)
    
    print(f"\n[TOOL] Optimisation RTX 3090:")
    print(f"   VRAM totale: {recommendations['rtx3090_optimization']['total_vram']}")
    print(f"   Modles lgers simultans: {recommendations['rtx3090_optimization']['concurrent_small_models']}")
    print(f"   Modles moyens simultans: {recommendations['rtx3090_optimization']['concurrent_medium_models']}")
    
    print(f"\n[CLIPBOARD] Workflows suggrs:")
    for workflow, models in recommendations['workflow_suggestions'].items():
        print(f"   {workflow.capitalize()}: {', '.join(models)}")
    
    print(f"\n[CHART] Dtails modles:")
    for key, model in recommendations['model_details'].items():
        print(f"   {key}: {model['name']} ({model['vram_gb']}GB, {model['tokens_per_sec']} tok/s)")

# ============================================================================
# [ROCKET] POINT D'ENTRE PRINCIPAL
# ============================================================================

async def main():
    """Point d'entre principal."""
    
    print(" SLECTEUR OLLAMA RTX 3090 - SUPERWHISPER V6")
    print("=" * 60)
    print("1. Test automatique")
    print("2. Mode interactif")
    print("3. Recommandations")
    print("4. Quitter")
    
    while True:
        try:
            choice = input("\n[TARGET] Votre choix (1-4): ").strip()
            
            if choice == "1":
                await test_selector()
            elif choice == "2":
                await interactive_mode()
            elif choice == "3":
                show_recommendations()
            elif choice == "4":
                print(" Au revoir !")
                break
            else:
                print("[CROSS] Choix invalide, utilisez 1-4")
                
        except KeyboardInterrupt:
            print("\n\n Interruption utilisateur, au revoir !")
            break
        except Exception as e:
            print(f"[CROSS] Erreur: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n Programme interrompu")




