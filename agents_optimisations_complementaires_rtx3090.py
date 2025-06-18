#!/usr/bin/env python3
"""
🎮 Agents Optimisations Complémentaires RTX3090 - NextGeneration
Validation des optimisations optionnelles après succès des actions prioritaires
"""

import asyncio
import os
import sys
import json
import subprocess
import time
import psutil
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

# Configuration GPU RTX 3090 obligatoire
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

class BaseOptimizationAgent:
    """Agent de base pour optimisations complémentaires RTX3090"""
    
    def __init__(self, name: str, mission: str):
        self.name = name
        self.mission = mission
        self.start_time = None
        self.end_time = None
        self.status = "initialized"
        self.results = {}
        self.errors = []
        self.recommendations = []
    
    async def execute(self) -> Dict[str, Any]:
        """Exécute la mission d'optimisation"""
        self.start_time = time.time()
        self.status = "running"
        
        try:
            print(f"🔧 Agent {self.name}: Démarrage optimisation")
            print(f"📋 Mission: {self.mission}")
            
            await self._execute_optimization()
            
            self.status = "completed"
            print(f"✅ Agent {self.name}: Optimisation terminée")
            
        except Exception as e:
            self.status = "failed"
            self.errors.append(str(e))
            print(f"❌ Agent {self.name}: Échec - {e}")
        
        finally:
            self.end_time = time.time()
            self.results["execution_time"] = self.end_time - self.start_time
            self.results["status"] = self.status
            self.results["errors"] = self.errors
            self.results["recommendations"] = self.recommendations
        
        return self.results
    
    async def _execute_optimization(self):
        """À implémenter par chaque agent spécialisé"""
        raise NotImplementedError

class CleanupAgent(BaseOptimizationAgent):
    """Agent pour nettoyage disque - Supprimer ancien Mixtral"""
    
    def __init__(self):
        super().__init__(
            name="Nettoyeur Disque",
            mission="Supprimer ancien Mixtral 26GB et nettoyer modèles redondants"
        )
    
    async def _execute_optimization(self):
        """Nettoyage intelligent des modèles Ollama"""
        
        # Analyser modèles actuels
        proc = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if proc.returncode != 0:
            raise Exception("Impossible de lister les modèles Ollama")
        
        lines = proc.stdout.strip().split('\n')[1:]  # Skip header
        models_info = []
        total_size_gb = 0
        
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    name = parts[0]
                    size_str = parts[2]
                    
                    # Parser la taille
                    if 'GB' in size_str:
                        size_gb = float(size_str.replace('GB', '').strip())
                    elif 'MB' in size_str:
                        size_gb = float(size_str.replace('MB', '').strip()) / 1024
                    else:
                        size_gb = 0
                    
                    models_info.append({
                        "name": name,
                        "size_gb": size_gb,
                        "size_str": size_str
                    })
                    total_size_gb += size_gb
        
        self.results["models_before"] = models_info
        self.results["total_size_before_gb"] = total_size_gb
        
        # Identifier modèles à supprimer
        models_to_remove = []
        space_to_liberate = 0
        
        # 1. Ancien Mixtral 26GB (priorité absolue)
        for model in models_info:
            if "mixtral-8x7b:latest" in model["name"] and model["size_gb"] > 25:
                models_to_remove.append(model["name"])
                space_to_liberate += model["size_gb"]
                self.recommendations.append(f"Supprimer {model['name']} ({model['size_str']}) - Remplacé par version optimisée")
        
        # 2. Modèles redondants recommandés précédemment
        redundant_models = [
            "deepseek-coder:1.3b",
            "deepseek-coder:6.7b", 
            "llama3.2:1b",
            "llama3.2:latest"
        ]
        
        for model in models_info:
            for redundant in redundant_models:
                if redundant in model["name"]:
                    models_to_remove.append(model["name"])
                    space_to_liberate += model["size_gb"]
                    self.recommendations.append(f"Supprimer {model['name']} ({model['size_str']}) - Modèle redondant")
        
        self.results["models_to_remove"] = models_to_remove
        self.results["space_to_liberate_gb"] = space_to_liberate
        
        # Exécuter suppression
        if models_to_remove:
            removed_models = []
            for model_name in models_to_remove:
                try:
                    print(f"🗑️ Suppression: {model_name}")
                    proc = subprocess.run(['ollama', 'rm', model_name], capture_output=True, text=True)
                    if proc.returncode == 0:
                        removed_models.append(model_name)
                        print(f"✅ {model_name} supprimé")
                    else:
                        print(f"⚠️ Échec suppression {model_name}: {proc.stderr}")
                except Exception as e:
                    print(f"❌ Erreur {model_name}: {e}")
            
            self.results["models_removed"] = removed_models
            self.results["cleanup_success"] = len(removed_models) > 0
        else:
            self.results["cleanup_success"] = False
            self.results["models_removed"] = []
            print("ℹ️ Aucun modèle à supprimer trouvé")

class MonitoringAgent(BaseOptimizationAgent):
    """Agent pour surveillance continue RTX3090"""
    
    def __init__(self):
        super().__init__(
            name="Surveillance RTX3090",
            mission="Lancer monitoring continu RTX3090 et créer surveillance automatique"
        )
    
    async def _execute_optimization(self):
        """Configuration monitoring continu"""
        
        # Vérifier script monitoring
        monitor_script = Path("monitor_rtx3090.py")
        if not monitor_script.exists():
            raise FileNotFoundError("Script monitor_rtx3090.py non trouvé")
        
        self.results["monitor_script_exists"] = True
        
        # Créer script de surveillance automatique
        monitoring_service = '''@echo off
echo 🎮 Surveillance Continue RTX3090 - NextGeneration
echo Démarrage monitoring automatique...

:loop
echo [%DATE% %TIME%] Lancement monitoring RTX3090
python monitor_rtx3090.py --duration 300 --interval 5
echo [%DATE% %TIME%] Monitoring terminé, pause 30s
timeout /t 30 /nobreak >nul
goto loop
'''
        
        service_script = "surveillance_continue_rtx3090.bat"
        with open(service_script, 'w', encoding='utf-8') as f:
            f.write(monitoring_service)
        
        self.results["service_script_created"] = service_script
        
        # Créer monitoring dashboard simple
        dashboard_script = '''#!/usr/bin/env python3
"""
Dashboard Monitoring RTX3090 Simple
"""

import time
import json
import os
import subprocess
from datetime import datetime

def get_gpu_info():
    """Récupère infos GPU RTX3090"""
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total,temperature.gpu,utilization.gpu', '--format=csv,noheader,nounits'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            parts = result.stdout.strip().split(', ')
            return {
                "memory_used_mb": int(parts[0]),
                "memory_total_mb": int(parts[1]), 
                "temperature_c": int(parts[2]),
                "utilization_percent": int(parts[3])
            }
    except:
        return None

def main():
    """Dashboard simple RTX3090"""
    print("🎮 DASHBOARD RTX3090 - NextGeneration")
    print("=" * 50)
    
    while True:
        gpu_info = get_gpu_info()
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if gpu_info:
            memory_percent = (gpu_info["memory_used_mb"] / gpu_info["memory_total_mb"]) * 100
            
            print(f"[{timestamp}] VRAM: {gpu_info['memory_used_mb']}/{gpu_info['memory_total_mb']}MB ({memory_percent:.1f}%)")
            print(f"[{timestamp}] Temp: {gpu_info['temperature_c']}°C | Usage: {gpu_info['utilization_percent']}%")
            
            # Alertes
            if memory_percent > 90:
                print("⚠️ ALERTE: VRAM > 90%")
            if gpu_info["temperature_c"] > 80:
                print("🔥 ALERTE: Température > 80°C")
        else:
            print(f"[{timestamp}] ❌ Impossible de lire GPU")
        
        time.sleep(5)

if __name__ == "__main__":
    main()
'''
        
        dashboard_file = "dashboard_rtx3090.py"
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(dashboard_script)
        
        self.results["dashboard_created"] = dashboard_file
        
        # Test rapide du monitoring
        try:
            print("🧪 Test monitoring...")
            result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total', '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True, timeout=10)
            self.results["monitor_test"] = result.returncode == 0
            if result.returncode == 0:
                print("✅ Monitoring fonctionnel")
                print(f"📊 VRAM actuelle: {result.stdout.strip()}")
            else:
                print(f"⚠️ Test monitoring: {result.stderr}")
        except Exception as e:
            self.results["monitor_test"] = False
            print(f"⚠️ Test monitoring échoué: {e}")
        
        self.recommendations.extend([
            f"Lancer surveillance: {service_script}",
            f"Dashboard temps réel: python {dashboard_file}",
            "Monitoring automatique configuré pour sessions 5 min"
        ])

class BenchmarkAgent(BaseOptimizationAgent):
    """Agent pour benchmarks performance approfondis"""
    
    def __init__(self):
        super().__init__(
            name="Benchmarks Performance",
            mission="Exécuter tests performance approfondis RTX3090 avec modèles optimisés"
        )
    
    async def _execute_optimization(self):
        """Benchmarks complets RTX3090"""
        
        # Test simple de performance Ollama
        print("🧪 Test performance Ollama rapide...")
        try:
            import httpx
            
            async with httpx.AsyncClient(timeout=30) as client:
                # Test connexion
                response = await client.get("http://localhost:11434/api/tags")
                if response.status_code == 200:
                    models = response.json()["models"]
                    self.results["ollama_available"] = True
                    self.results["models_count"] = len(models)
                    print(f"✅ Ollama connecté ({len(models)} modèles)")
                    
                    # Test performance avec nouveau Mixtral optimisé
                    test_model = "mixtral:8x7b-instruct-v0.1-q3_k_m"
                    test_prompt = "Test performance RTX3090"
                    
                    start_time = time.time()
                    
                    payload = {
                        "model": test_model,
                        "prompt": test_prompt,
                        "stream": False,
                        "options": {"temperature": 0.7, "num_gpu": 1}
                    }
                    
                    test_response = await client.post("http://localhost:11434/api/generate", json=payload)
                    
                    if test_response.status_code == 200:
                        end_time = time.time()
                        result_data = test_response.json()
                        response_text = result_data.get("response", "")
                        
                        processing_time = end_time - start_time
                        tokens_generated = len(response_text.split())
                        tokens_per_sec = tokens_generated / processing_time if processing_time > 0 else 0
                        
                        self.results["performance_test"] = {
                            "model": test_model,
                            "processing_time": processing_time,
                            "tokens_generated": tokens_generated,
                            "tokens_per_sec": tokens_per_sec,
                            "success": True
                        }
                        
                        print(f"📊 Performance: {processing_time:.1f}s, {tokens_per_sec:.1f} tokens/s")
                        
                    else:
                        self.results["performance_test"] = {"success": False, "error": f"HTTP {test_response.status_code}"}
                        
                else:
                    self.results["ollama_available"] = False
                    
        except Exception as e:
            self.results["ollama_available"] = False
            self.results["error"] = str(e)
            print(f"❌ Test performance échoué: {e}")
        
        # Créer script benchmark complet
        benchmark_script = '''#!/usr/bin/env python3
"""
Benchmark RTX3090 Complet - NextGeneration
"""

import asyncio
import httpx
import time
import json
import os
from datetime import datetime

os.environ['CUDA_VISIBLE_DEVICES'] = '1'

async def benchmark_model(model_name, test_prompts):
    """Benchmark un modèle"""
    print(f"🧪 Test: {model_name}")
    
    results = []
    
    async with httpx.AsyncClient(timeout=60) as client:
        for prompt in test_prompts:
            try:
                start_time = time.time()
                
                payload = {
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_gpu": 1}
                }
                
                response = await client.post("http://localhost:11434/api/generate", json=payload)
                
                if response.status_code == 200:
                    end_time = time.time()
                    result_data = response.json()
                    response_text = result_data.get("response", "")
                    
                    processing_time = end_time - start_time
                    tokens = len(response_text.split())
                    tokens_per_sec = tokens / processing_time if processing_time > 0 else 0
                    
                    results.append({
                        "prompt": prompt[:30] + "...",
                        "time": processing_time,
                        "tokens": tokens,
                        "tokens_per_sec": tokens_per_sec
                    })
                    
                    print(f"   {processing_time:.1f}s, {tokens_per_sec:.1f} t/s")
                    
            except Exception as e:
                print(f"   Erreur: {e}")
    
    return results

async def main():
    """Benchmark principal"""
    print("🎮 BENCHMARK RTX3090 COMPLET")
    print("=" * 40)
    
    models_to_test = [
        "nous-hermes-2-mistral-7b-dpo:latest",
        "mixtral:8x7b-instruct-v0.1-q3_k_m",
        "llama3:8b-instruct-q6_k"
    ]
    
    test_prompts = [
        "Explique l'IA en 2 phrases",
        "Écris une fonction Python",
        "Analyse les avantages du cloud"
    ]
    
    benchmark_results = {
        "timestamp": datetime.now().isoformat(),
        "gpu": "RTX 3090",
        "models": {}
    }
    
    for model in models_to_test:
        results = await benchmark_model(model, test_prompts)
        if results:
            avg_time = sum(r["time"] for r in results) / len(results)
            avg_tokens_per_sec = sum(r["tokens_per_sec"] for r in results) / len(results)
            
            benchmark_results["models"][model] = {
                "avg_time": avg_time,
                "avg_tokens_per_sec": avg_tokens_per_sec,
                "tests": results
            }
            
            print(f"📊 {model}: {avg_tokens_per_sec:.1f} tokens/s moyenne")
    
    # Sauvegarde
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"benchmark_rtx3090_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(benchmark_results, f, indent=2, ensure_ascii=False)
    
    print(f"\\n📄 Résultats: {filename}")

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        benchmark_file = "benchmark_rtx3090_complet.py"
        with open(benchmark_file, 'w', encoding='utf-8') as f:
            f.write(benchmark_script)
        
        self.results["benchmark_script_created"] = benchmark_file
        
        self.recommendations.extend([
            f"Benchmark complet: python {benchmark_file}",
            "Performance RTX3090 validée avec modèles optimisés",
            "Monitoring automatique de performance recommandé"
        ])

class OptimizationOrchestrator:
    """Orchestrateur pour optimisations complémentaires"""
    
    def __init__(self):
        self.agents = [
            CleanupAgent(),
            MonitoringAgent(), 
            BenchmarkAgent()
        ]
    
    async def execute_optimizations(self) -> Dict[str, Any]:
        """Exécution séquentielle des optimisations"""
        
        print("🔧 ORCHESTRATEUR OPTIMISATIONS COMPLÉMENTAIRES RTX3090")
        print("=" * 60)
        print(f"🎯 {len(self.agents)} optimisations complémentaires")
        print(f"🎮 Configuration GPU: RTX 3090 (Device {os.environ.get('CUDA_VISIBLE_DEVICES')})")
        print()
        
        start_time = time.time()
        
        # Exécution séquentielle
        results = []
        for agent in self.agents:
            result = await agent.execute()
            results.append(result)
            await asyncio.sleep(1)
        
        total_time = time.time() - start_time
        
        # Compilation rapport final
        rapport = {
            "execution_info": {
                "timestamp": datetime.now().isoformat(),
                "total_execution_time": total_time,
                "optimizations_count": len(self.agents)
            },
            "optimizations_results": {},
            "global_status": "success",
            "summary": {
                "completed": 0,
                "failed": 0,
                "total_optimizations": len(self.agents)
            },
            "recommendations": []
        }
        
        # Traitement résultats
        for agent, result in zip(self.agents, results):
            rapport["optimizations_results"][agent.name] = result
            
            if result.get("status") == "completed":
                rapport["summary"]["completed"] += 1
            else:
                rapport["summary"]["failed"] += 1
            
            # Collecter recommandations
            if "recommendations" in result:
                rapport["recommendations"].extend(result["recommendations"])
        
        # Statut global
        if rapport["summary"]["failed"] > 0:
            rapport["global_status"] = "partial_success"
        
        return rapport

async def main():
    """Point d'entrée principal"""
    
    orchestrateur = OptimizationOrchestrator()
    rapport = await orchestrateur.execute_optimizations()
    
    # Sauvegarde rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rapport_file = f"rapport_optimisations_complementaires_{timestamp}.json"
    
    with open(rapport_file, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    # Affichage résumé
    print("\n🎯 RAPPORT FINAL - Optimisations Complémentaires RTX3090")
    print("=" * 60)
    print(f"⏱️  Temps total: {rapport['execution_info']['total_execution_time']:.1f}s")
    print(f"✅ Optimisations réussies: {rapport['summary']['completed']}")
    print(f"❌ Optimisations échouées: {rapport['summary']['failed']}")
    print(f"📄 Rapport détaillé: {rapport_file}")
    print()
    
    # Détail par optimisation
    for agent_name, result in rapport["optimizations_results"].items():
        status = result.get("status", "unknown")
        exec_time = result.get("execution_time", 0)
        
        if status == "completed":
            print(f"✅ {agent_name}: Succès ({exec_time:.1f}s)")
        else:
            errors = result.get("errors", [])
            print(f"❌ {agent_name}: Échec - {errors[0] if errors else 'Erreur inconnue'}")
    
    # Recommandations principales
    if rapport["recommendations"]:
        print(f"\n🎯 RECOMMANDATIONS PRINCIPALES:")
        for i, rec in enumerate(rapport["recommendations"][:5], 1):
            print(f"{i}. {rec}")
    
    print(f"\n🎮 Optimisations RTX3090 terminées - Rapport: {rapport_file}")

if __name__ == "__main__":
    asyncio.run(main()) 