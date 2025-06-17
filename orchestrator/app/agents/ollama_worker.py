#!/usr/bin/env python3
"""
Worker Ollama Local pour RTX 3090 - NextGeneration
Utilise vos modèles existants avec sélection intelligente.
"""

import httpx
import asyncio
import time
from typing import Dict, Any, List, Optional
import logging

class OllamaLocalWorker:
    """Worker pour modèles Ollama locaux sur RTX 3090."""
    
    def __init__(self, config):
        self.config = config
        self.ollama_url = getattr(config, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        self.gpu_device = getattr(config, 'OLLAMA_GPU_DEVICE', '1')
        self.agent_type = "ollama_local"
        
        # Vos modèles existants avec sélection optimisée
        self.model_mapping = {
            "speed": "nous-hermes-2-mistral-7b-dpo:latest",  # 4.1GB - Ultra rapide
            "quality": "mixtral-8x7b:latest",                # 26GB - Qualité max
            "code": "qwen-coder-32b:latest",                 # 19GB - Spécialiste code
            "daily": "llama3:8b-instruct-q6_k",             # 6.6GB - Usage quotidien
            "mini": "qwen2.5-coder:1.5b"                     # 986MB - Tests rapides
        }
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"OllamaLocalWorker initialisé avec GPU device {self.gpu_device}")
    
    async def can_handle_task(self, task: str, requirements: List[str] = None) -> bool:
        """Détermine si ce worker peut traiter la tâche."""
        
        if requirements is None:
            requirements = []
        
        # Priorité élevée pour modèles locaux
        priority_keywords = ["local", "confidential", "private", "offline"]
        if any(keyword in requirements for keyword in priority_keywords):
            return True
        
        # Excellent pour code
        if "code" in task.lower() or "code" in requirements:
            return True
        
        # Très rapide pour tâches simples
        if any(keyword in requirements for keyword in ["fast", "quick", "rapid"]):
            return True
        
        # Bonne qualité générale
        if len(task) > 100:  # Tâches longues
            return True
            
        return False
    
    async def process_task(self, task: str, requirements: List[str] = None) -> Dict[str, Any]:
        """Traite la tâche avec le modèle optimal."""
        
        if requirements is None:
            requirements = []
        
        # Sélection intelligente du modèle
        model_key = self._select_optimal_model(task, requirements)
        model_name = self.model_mapping[model_key]
        
        self.logger.info(f"Traitement avec modèle {model_key}: {model_name}")
        
        try:
            start_time = time.time()
            
            # Vérifier disponibilité du modèle
            if not await self._is_model_available(model_name):
                # Fallback vers modèle plus petit
                model_key = "daily"
                model_name = self.model_mapping[model_key]
                self.logger.warning(f"Fallback vers modèle: {model_name}")
            
            # Appel au modèle
            response = await self._call_ollama(model_name, task, requirements)
            
            duration = time.time() - start_time
            
            return {
                "result": response,
                "model_used": model_name,
                "model_category": model_key,
                "agent_type": self.agent_type,
                "processing_time": duration,
                "gpu_used": f"RTX 3090 (device {self.gpu_device})",
                "privacy": "local_processing",
                "cost": "free",
                "confidence": self._get_confidence_score(model_key),
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Erreur traitement Ollama: {e}")
            return {
                "result": f"Erreur modèle local: {str(e)}",
                "success": False,
                "agent_type": self.agent_type,
                "error": str(e)
            }
    
    def _select_optimal_model(self, task: str, requirements: List[str]) -> str:
        """Sélectionne le modèle optimal selon la tâche et requirements."""
        
        task_lower = task.lower()
        
        # Code spécialisé -> Qwen-Coder 32B
        if ("code" in task_lower or "function" in task_lower or 
            "script" in task_lower or "code" in requirements):
            return "code"
        
        # Rapidité demandée -> Nous-Hermes 7B
        if any(keyword in requirements for keyword in ["fast", "quick", "rapid", "speed"]):
            return "speed"
        
        # Qualité maximale -> Mixtral 8x7B
        if (any(keyword in requirements for keyword in ["quality", "detailed", "complex", "analysis"]) or
            len(task) > 300):  # Tâches complexes
            return "quality"
        
        # Tests rapides -> Qwen 1.5B
        if any(keyword in requirements for keyword in ["test", "simple", "quick"]):
            return "mini"
        
        # Usage quotidien par défaut -> Llama3 8B
        return "daily"
    
    def _get_confidence_score(self, model_key: str) -> float:
        """Retourne un score de confiance selon le modèle."""
        confidence_map = {
            "quality": 0.95,    # Mixtral très fiable
            "code": 0.90,       # Qwen-Coder excellent
            "daily": 0.85,      # Llama3 8B très bon
            "speed": 0.80,      # Nous-Hermes bon
            "mini": 0.70        # Qwen 1.5B correct
        }
        return confidence_map.get(model_key, 0.75)
    
    async def _is_model_available(self, model_name: str) -> bool:
        """Vérifie si le modèle est disponible dans Ollama."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.ollama_url}/api/tags")
                
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    available_models = [model["name"] for model in models]
                    return model_name in available_models
                
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur vérification modèle: {e}")
            return False
    
    async def _call_ollama(self, model_name: str, prompt: str, requirements: List[str] = None) -> str:
        """Appel à l'API Ollama avec configuration RTX 3090."""
        
        # Configuration adaptée selon le modèle
        if "mixtral" in model_name.lower():
            # Mixtral 26GB - Configuration conservatrice
            num_ctx = 4096
            temperature = 0.7
            timeout = 120.0
        elif "qwen-coder-32b" in model_name.lower():
            # Qwen-Coder 19GB - Optimisé pour code
            num_ctx = 8192
            temperature = 0.3  # Plus déterministe pour code
            timeout = 90.0
        elif "nous-hermes" in model_name.lower():
            # Nous-Hermes 4GB - Configuration rapide
            num_ctx = 4096
            temperature = 0.8
            timeout = 30.0
        else:
            # Configuration par défaut
            num_ctx = 4096
            temperature = 0.7
            timeout = 60.0
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": 0.9,
                "num_ctx": num_ctx,
                "num_gpu": 1,  # Force 1 GPU (RTX 3090)
                "gpu_layers": -1,  # Toutes couches sur GPU
                "num_thread": 8,  # Optimisation CPU
                "repeat_penalty": 1.1
            }
        }
        
        # Ajustements selon requirements
        if requirements:
            if "creative" in requirements:
                payload["options"]["temperature"] = 0.9
            elif "precise" in requirements:
                payload["options"]["temperature"] = 0.3
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "")
                
                # Log des métriques de performance
                if "eval_count" in result and "eval_duration" in result:
                    eval_count = result["eval_count"]
                    eval_duration = result["eval_duration"] / 1e9  # ns to seconds
                    tokens_per_sec = eval_count / eval_duration if eval_duration > 0 else 0
                    self.logger.info(f"Performance {model_name}: {tokens_per_sec:.1f} tokens/sec")
                
                return response_text
            else:
                raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
    
    async def get_available_models(self) -> List[str]:
        """Retourne la liste des modèles disponibles."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.ollama_url}/api/tags")
                
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    return [model["name"] for model in models]
                
                return []
                
        except Exception as e:
            self.logger.error(f"Erreur récupération modèles: {e}")
            return []
    
    async def health_check(self) -> Dict[str, Any]:
        """Vérifie la santé du service Ollama."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.ollama_url}/api/tags")
                
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    available_count = len(models)
                    
                    # Vérifier nos modèles principaux
                    our_models = list(self.model_mapping.values())
                    available_models = [m["name"] for m in models]
                    our_available = [m for m in our_models if m in available_models]
                    
                    return {
                        "status": "healthy",
                        "ollama_url": self.ollama_url,
                        "total_models": available_count,
                        "our_models_available": len(our_available),
                        "our_models_total": len(our_models),
                        "gpu_device": self.gpu_device,
                        "models_ready": our_available
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "error": f"HTTP {response.status_code}",
                        "ollama_url": self.ollama_url
                    }
                    
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "ollama_url": self.ollama_url
            }

# Fonction utilitaire pour tests
async def test_ollama_worker():
    """Test rapide du worker Ollama."""
    
    class MockConfig:
        OLLAMA_BASE_URL = "http://localhost:11434"
        OLLAMA_GPU_DEVICE = "1"
    
    worker = OllamaLocalWorker(MockConfig())
    
    # Test santé
    health = await worker.health_check()
    print(f"🏥 Santé Ollama: {health}")
    
    # Test modèles disponibles
    models = await worker.get_available_models()
    print(f"📋 Modèles disponibles: {len(models)}")
    
    # Test simple
    if models:
        test_task = "Dis bonjour en français"
        result = await worker.process_task(test_task, ["fast"])
        print(f"🧪 Test résultat: {result}")

if __name__ == "__main__":
    asyncio.run(test_ollama_worker())
