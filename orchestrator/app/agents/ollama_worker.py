#!/usr/bin/env python3
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




