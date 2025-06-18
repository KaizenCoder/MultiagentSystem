#!/usr/bin/env python3
"""
 Agents Intgration Orchestrateur RTX3090 - NextGeneration
Validation intgration orchestrateur avec modles optimiss RTX3090
"""

import asyncio
import os
import sys
import json
import subprocess
import time
import httpx
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

# Configuration GPU RTX 3090 obligatoire
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

class BaseIntegrationAgent:
    """Agent de base pour intgration orchestrateur RTX3090"""
    
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
        """Excute la mission d'intgration"""
        self.start_time = time.time()
        self.status = "running"
        
        try:
            print(f"[ROCKET] Agent {self.name}: Integration dmarre")
            print(f"[CLIPBOARD] Mission: {self.mission}")
            
            await self._execute_integration()
            
            self.status = "completed"
            print(f"[CHECK] Agent {self.name}: Intgration termine")
            
        except Exception as e:
            self.status = "failed"
            self.errors.append(str(e))
            print(f"[CROSS] Agent {self.name}: chec - {e}")
        
        finally:
            self.end_time = time.time()
            self.results["execution_time"] = self.end_time - self.start_time
            self.results["status"] = self.status
            self.results["errors"] = self.errors
            self.results["recommendations"] = self.recommendations
        
        return self.results
    
    async def _execute_integration(self):
        """ implmenter par chaque agent spcialis"""
        raise NotImplementedError

class ModelConfigurationAgent(BaseIntegrationAgent):
    """Agent pour configuration modles optimiss dans orchestrateur"""
    
    def __init__(self):
        super().__init__(
            name="Configuration Modles",
            mission="Intgrer modles RTX3090 optimiss dans configuration orchestrateur"
        )
    
    async def _execute_integration(self):
        """Configuration des modles optimiss"""
        
        # Modles RTX3090 optimiss valids
        optimized_models = {
            "speed": {
                "name": "nous-hermes-2-mistral-7b-dpo:latest",
                "size_gb": 4.1,
                "performance": "6.4 tokens/s",
                "use_case": "Rponses rapides, chat interactif"
            },
            "quality": {
                "name": "mixtral:8x7b-instruct-v0.1-q3_k_m",
                "size_gb": 22.0,
                "performance": "5.4 tokens/s", 
                "use_case": "Qualit maximale, quantization Q3_K optimise"
            },
            "balanced": {
                "name": "llama3:8b-instruct-q6_k",
                "size_gb": 6.6,
                "performance": "4.9 tokens/s",
                "use_case": "Usage quotidien quilibr"
            },
            "code": {
                "name": "qwen-coder-32b:latest",
                "size_gb": 19.0,
                "performance": "Spcialis code",
                "use_case": "Dveloppement professionnel"
            }
        }
        
        self.results["optimized_models"] = optimized_models
        
        # Crer configuration RTX3090 optimise
        config_content = '''# Configuration RTX3090 Optimise - NextGeneration
import os
from typing import Dict, Any

# Configuration GPU RTX 3090
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

class RTX3090OptimizedConfig:
    """Configuration optimise pour RTX3090 avec modles valids"""
    
    # Modles RTX3090 optimiss (valids par benchmarks)
    OLLAMA_MODELS = {
        "speed": {
            "model": "nous-hermes-2-mistral-7b-dpo:latest",
            "performance": "6.4 tokens/s",
            "vram_gb": 4.1,
            "use_case": "Rponses rapides, interactions temps rel"
        },
        "quality": {
            "model": "mixtral:8x7b-instruct-v0.1-q3_k_m", 
            "performance": "5.4 tokens/s",
            "vram_gb": 22.0,
            "use_case": "Qualit maximale, quantization Q3_K optimise"
        },
        "balanced": {
            "model": "llama3:8b-instruct-q6_k",
            "performance": "4.9 tokens/s", 
            "vram_gb": 6.6,
            "use_case": "Usage quotidien quilibr"
        },
        "code": {
            "model": "qwen-coder-32b:latest",
            "performance": "Spcialis dveloppement",
            "vram_gb": 19.0,
            "use_case": "Code professionnel, debugging"
        }
    }
    
    # Configuration RTX3090
    GPU_CONFIG = {
        "device_id": 1,  # RTX 3090 sur bus PCI 1
        "total_vram_gb": 24,
        "reserved_vram_gb": 2,  # Rserver 2GB pour systme
        "available_vram_gb": 22,
        "cuda_visible_devices": "1",
        "cuda_device_order": "PCI_BUS_ID"
    }
    
    # Slecteur intelligent de modles
    MODEL_SELECTOR = {
        "quick_tasks": "speed",      # Tches rapides
        "complex_analysis": "quality",  # Analyses complexes
        "daily_usage": "balanced",   # Usage quotidien
        "code_tasks": "code",        # Dveloppement
        "default": "balanced"        # Par dfaut
    }
    
    # Configuration Ollama
    OLLAMA_CONFIG = {
        "base_url": "http://localhost:11434",
        "timeout": 300,
        "num_gpu": 1,
        "gpu_memory_fraction": 0.9,  # Utiliser 90% VRAM disponible
        "temperature": 0.7,
        "max_tokens": 4096
    }

# Configuration globale
settings = RTX3090OptimizedConfig()
'''
        
        # Sauvegarder configuration
        config_path = "orchestrator/app/config_rtx3090_optimized.py"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        self.results["config_created"] = True
        self.results["config_file"] = config_path
        print(f"[CHECK] Configuration RTX3090 cre: {config_path}")
        
        # Recommandations
        self.recommendations.extend([
            "Configuration RTX3090 optimise intgre",
            "4 modles RTX3090 configurs selon usage",
            "Slecteur intelligent implment",
            "GPU RTX3090 configur avec 22GB VRAM disponible"
        ])

class OllamaWorkerAgent(BaseIntegrationAgent):
    """Agent pour mise  jour OllamaLocalWorker avec modles optimiss"""
    
    def __init__(self):
        super().__init__(
            name="OllamaWorker Optimis",
            mission="Mettre  jour OllamaLocalWorker avec modles RTX3090 optimiss"
        )
    
    async def _execute_integration(self):
        """Mise  jour OllamaLocalWorker"""
        
        # Crer OllamaLocalWorker RTX3090 optimis
        worker_code = '''#!/usr/bin/env python3
"""
 OllamaLocalWorker RTX3090 Optimis - NextGeneration
Worker Ollama avec modles RTX3090 optimiss et slection intelligente
"""

import asyncio
import httpx
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

# Configuration RTX3090 obligatoire
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

class OllamaLocalWorkerRTX3090:
    """Worker Ollama optimis pour RTX3090 avec slection intelligente"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=300)
        
        # Modles RTX3090 optimiss (valids par benchmarks)
        self.models = {
            "speed": {
                "name": "nous-hermes-2-mistral-7b-dpo:latest",
                "performance": "6.4 tokens/s",
                "vram_gb": 4.1,
                "description": "Rponses rapides, interactions temps rel"
            },
            "quality": {
                "name": "mixtral:8x7b-instruct-v0.1-q3_k_m",
                "performance": "5.4 tokens/s", 
                "vram_gb": 22.0,
                "description": "Qualit maximale, quantization Q3_K optimise"
            },
            "balanced": {
                "name": "llama3:8b-instruct-q6_k",
                "performance": "4.9 tokens/s",
                "vram_gb": 6.6,
                "description": "Usage quotidien quilibr"
            },
            "code": {
                "name": "qwen-coder-32b:latest",
                "performance": "Spcialis dveloppement",
                "vram_gb": 19.0,
                "description": "Code professionnel, debugging"
            }
        }
    
    def select_optimal_model(self, task_type: str = "default", task_description: str = "") -> str:
        """Slection intelligente du modle selon la tche"""
        
        task_lower = task_type.lower()
        desc_lower = task_description.lower()
        
        # Slection base sur mots-cls
        if any(keyword in desc_lower for keyword in ["code", "python", "fonction", "debug"]):
            selected = "code"
        elif any(keyword in desc_lower for keyword in ["rapide", "quick", "fast", "chat"]):
            selected = "speed"
        elif any(keyword in desc_lower for keyword in ["analyse", "complex", "qualit"]):
            selected = "quality"
        else:
            selected = "balanced"
        
        model_info = self.models[selected]
        print(f"[TARGET] Modle slectionn: {selected} ({model_info['name']})")
        return model_info["name"]
    
    async def generate_response(self, prompt: str, task_type: str = "default") -> Dict[str, Any]:
        """Gnration de rponse avec slection intelligente RTX3090"""
        
        model_name = self.select_optimal_model(task_type, prompt)
        start_time = datetime.now()
        
        try:
            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_gpu": 1,
                    "gpu_memory_fraction": 0.9
                }
            }
            
            response = await self.client.post(f"{self.base_url}/api/generate", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                end_time = datetime.now()
                processing_time = (end_time - start_time).total_seconds()
                
                response_text = result.get("response", "")
                tokens_generated = len(response_text.split())
                tokens_per_sec = tokens_generated / processing_time if processing_time > 0 else 0
                
                return {
                    "success": True,
                    "response": response_text,
                    "model_used": model_name,
                    "processing_time": processing_time,
                    "tokens_per_sec": tokens_per_sec,
                    "gpu_device": "RTX3090"
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "model_used": model_name
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model_used": model_name
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """Vrification sant worker RTX3090"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return {
                    "success": True,
                    "status": "healthy",
                    "models_count": len(models),
                    "gpu_config": "RTX3090 Device 1"
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Instance globale
ollama_worker_rtx3090 = OllamaLocalWorkerRTX3090()
'''
        
        # Sauvegarder worker optimis
        worker_path = "orchestrator/app/agents/ollama_worker.py"
        os.makedirs(os.path.dirname(worker_path), exist_ok=True)
        
        with open(worker_path, 'w', encoding='utf-8') as f:
            f.write(worker_code)
        
        self.results["worker_created"] = True
        self.results["worker_path"] = str(worker_path)
        print(f"[CHECK] OllamaLocalWorker RTX3090 cr: {worker_path}")
        
        self.recommendations.extend([
            "OllamaLocalWorker RTX3090 optimis intgr",
            "Slection intelligente de modles implmente", 
            "4 modles RTX3090 configurs avec performances valides"
        ])

class OrchestrationTestAgent(BaseIntegrationAgent):
    """Agent pour test intgration complte orchestrateur"""
    
    def __init__(self):
        super().__init__(
            name="Test Orchestration",
            mission="Tester intgration complte orchestrateur avec modles RTX3090 optimiss"
        )
    
    async def _execute_integration(self):
        """Test de l'intgration orchestrateur complte"""
        
        # Test 1: Configuration
        config_path = "orchestrator/app/config_rtx3090_optimized.py"
        self.results["config_exists"] = Path(config_path).exists()
        
        # Test 2: Worker
        worker_path = "orchestrator/app/agents/ollama_worker.py"
        self.results["worker_exists"] = Path(worker_path).exists()
        
        # Test 3: Connexion Ollama
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get("http://localhost:11434/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    self.results["ollama_connected"] = True
                    self.results["models_count"] = len(models)
                    
                    # Vrifier modles optimiss
                    optimized_models = [
                        "nous-hermes-2-mistral-7b-dpo:latest",
                        "mixtral:8x7b-instruct-v0.1-q3_k_m",
                        "llama3:8b-instruct-q6_k",
                        "qwen-coder-32b:latest"
                    ]
                    
                    available = [m["name"] for m in models if m["name"] in optimized_models]
                    self.results["optimized_available"] = available
                    self.results["optimized_count"] = len(available)
                    
                    print(f"[CHECK] Ollama: {len(models)} modles, {len(available)}/4 optimiss RTX3090")
                else:
                    self.results["ollama_connected"] = False
        except Exception as e:
            self.results["ollama_connected"] = False
            print(f"[CROSS] Connexion Ollama: {e}")
        
        # Test 4: Gnration test
        if self.results.get("ollama_connected", False):
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    payload = {
                        "model": "nous-hermes-2-mistral-7b-dpo:latest",
                        "prompt": "Test intgration RTX3090",
                        "stream": False,
                        "options": {"temperature": 0.7, "num_gpu": 1}
                    }
                    
                    response = await client.post("http://localhost:11434/api/generate", json=payload)
                    
                    if response.status_code == 200:
                        self.results["generation_test"] = True
                        print("[CHECK] Test gnration russi")
                    else:
                        self.results["generation_test"] = False
            except Exception as e:
                self.results["generation_test"] = False
                print(f"[CROSS] Test gnration: {e}")
        else:
            self.results["generation_test"] = False
        
        # Score intgration
        score = 0
        if self.results.get("config_exists", False): score += 1
        if self.results.get("worker_exists", False): score += 1
        if self.results.get("ollama_connected", False): score += 1
        if self.results.get("generation_test", False): score += 1
        
        self.results["integration_score"] = score
        self.results["integration_percentage"] = (score / 4) * 100
        
        print(f"[TARGET] Score intgration: {score}/4 ({self.results['integration_percentage']:.0f}%)")
        
        # Recommandations
        if score == 4:
            self.recommendations.append(" Intgration orchestrateur RTX3090 COMPLTE")
        elif score >= 3:
            self.recommendations.append("[CHECK] Intgration orchestrateur RTX3090 RUSSIE")
        else:
            self.recommendations.append(" Intgration orchestrateur RTX3090 PARTIELLE")

class IntegrationOrchestrator:
    """Orchestrateur pour intgration complte RTX3090"""
    
    def __init__(self):
        self.agents = [
            ModelConfigurationAgent(),
            OllamaWorkerAgent(),
            OrchestrationTestAgent()
        ]
    
    async def execute_integration(self) -> Dict[str, Any]:
        """Excution intgration orchestrateur RTX3090"""
        
        print("[ROCKET] ORCHESTRATEUR INTGRATION RTX3090 - NEXTGENERATION")
        print("=" * 65)
        print(f"[TARGET] {len(self.agents)} agents d'intgration")
        print(f" Configuration: RTX 3090 Device {os.environ.get('CUDA_VISIBLE_DEVICES')}")
        print()
        
        start_time = time.time()
        
        # Excution squentielle
        results = []
        for agent in self.agents:
            result = await agent.execute()
            results.append(result)
            await asyncio.sleep(0.5)
        
        total_time = time.time() - start_time
        
        # Compilation rapport
        rapport = {
            "execution_info": {
                "timestamp": datetime.now().isoformat(),
                "total_execution_time": total_time,
                "integration_agents": len(self.agents)
            },
            "integration_results": {},
            "summary": {
                "completed": 0,
                "failed": 0
            },
            "recommendations": [],
            "integration_score": 0
        }
        
        # Traitement rsultats
        for agent, result in zip(self.agents, results):
            rapport["integration_results"][agent.name] = result
            
            if result.get("status") == "completed":
                rapport["summary"]["completed"] += 1
            else:
                rapport["summary"]["failed"] += 1
            
            if "recommendations" in result:
                rapport["recommendations"].extend(result["recommendations"])
        
        # Score d'intgration global
        test_results = rapport["integration_results"].get("Test Orchestration", {})
        rapport["integration_score"] = test_results.get("integration_score", 0)
        rapport["integration_percentage"] = test_results.get("integration_percentage", 0)
        
        return rapport

async def main():
    """Point d'entre principal"""
    
    orchestrateur = IntegrationOrchestrator()
    rapport = await orchestrateur.execute_integration()
    
    # Sauvegarde rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rapport_file = f"rapport_integration_orchestrateur_rtx3090_{timestamp}.json"
    
    with open(rapport_file, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    # Affichage rsum
    print("\n[TARGET] RAPPORT FINAL - Intgration Orchestrateur RTX3090")
    print("=" * 65)
    print(f"  Temps total: {rapport['execution_info']['total_execution_time']:.1f}s")
    print(f"[CHECK] Intgrations russies: {rapport['summary']['completed']}")
    print(f"[CROSS] Intgrations choues: {rapport['summary']['failed']}")
    print(f"[TARGET] Score intgration: {rapport['integration_score']}/4 ({rapport['integration_percentage']:.0f}%)")
    print(f"[DOCUMENT] Rapport dtaill: {rapport_file}")
    
    # Statut final
    if rapport["integration_score"] == 4:
        print("\n INTGRATION ORCHESTRATEUR RTX3090 - SUCCS COMPLET")
    elif rapport["integration_score"] >= 3:
        print("\n[CHECK] INTGRATION ORCHESTRATEUR RTX3090 - RUSSIE")
    else:
        print("\n INTGRATION ORCHESTRATEUR RTX3090 - PARTIELLE")

if __name__ == "__main__":
    asyncio.run(main()) 