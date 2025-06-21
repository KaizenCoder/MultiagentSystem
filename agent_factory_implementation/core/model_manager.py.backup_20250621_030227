"""
🤖 MODEL MANAGER - PATTERN FACTORY
=================================

Gestionnaire centralisé des modèles IA pour tous les agents Pattern Factory.
Résout le problème de définition dispersée des modèles dans le code.

Fonctionnalités :
- Configuration centralisée des modèles par agent
- Fallback automatique en cas d'échec
- Gestion des coûts et limites
- Monitoring utilisation modèles
- Support multi-providers (Anthropic, OpenAI, Ollama RTX3090)
- Support modèles locaux avec optimisations GPU
"""

import json
import os
import logging
import asyncio
import httpx
import psutil
from typing import Dict, Any, Optional, Tuple, List
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)

class ModelProvider(Enum):
    """Providers de modèles IA supportés"""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    OLLAMA = "ollama"

class ModelType(Enum):
    """Types de modèles selon leur usage"""
    PRIMARY = "primary"
    FALLBACK = "fallback"
    LOCAL = "local"
    RESEARCH = "research"
    FAST = "fast"

@dataclass
class ModelUsage:
    """Statistiques d'utilisation d'un modèle"""
    total_requests: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    avg_response_time: float = 0.0
    error_count: int = 0
    last_used: Optional[datetime] = None

@dataclass
class ModelConfig:
    """Configuration d'un modèle spécifique"""
    name: str
    provider: ModelProvider
    max_tokens: int
    cost_per_1k_input: float
    cost_per_1k_output: float
    context_window: int
    temperature: float = 0.7
    is_local: bool = False
    vram_usage: Optional[str] = None
    speed: Optional[str] = None
    speciality: Optional[str] = None

class OllamaClient:
    """Client spécialisé pour Ollama avec optimisations RTX3090"""
    
    def __init__(self, base_url: str = "http://localhost:11434", gpu_device: str = "1"):
        self.base_url = base_url
        self.gpu_device = gpu_device
        self.client = httpx.AsyncClient(timeout=120.0)
        
    async def generate(self, model: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Génération avec modèle Ollama local"""
        
        # Configuration optimisée RTX3090
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9),
                "num_ctx": kwargs.get("context_length", 4096),
                "num_gpu": 1,  # Force RTX3090 uniquement
                "gpu_layers": -1,  # Toutes les couches sur GPU
                **kwargs.get("options", {})
            }
        }
        
        start_time = datetime.now()
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds()
                
                # Calcul vitesse tokens/sec
                tokens_count = len(result["response"].split())
                tokens_per_sec = tokens_count / response_time if response_time > 0 else 0
                
                return {
                    "response": result["response"],
                    "model": model,
                    "provider": "ollama",
                    "tokens": tokens_count,
                    "response_time": response_time,
                    "tokens_per_sec": tokens_per_sec,
                    "cost": 0.0,  # Modèles locaux gratuits
                    "success": True
                }
            else:
                raise Exception(f"Ollama error: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Erreur Ollama pour modèle {model}: {str(e)}")
            return {
                "response": "",
                "error": str(e),
                "success": False,
                "model": model,
                "provider": "ollama"
            }
    
    async def list_models(self) -> List[str]:
        """Liste des modèles Ollama disponibles"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception as e:
            logger.error(f"Erreur listage modèles Ollama: {str(e)}")
            return []
    
    async def check_model_availability(self, model: str) -> bool:
        """Vérifie si un modèle est disponible localement"""
        available_models = await self.list_models()
        return model in available_models
    
    async def get_gpu_usage(self) -> Dict[str, Any]:
        """Statistiques utilisation GPU RTX3090"""
        try:
            # Utilisation psutil pour monitoring basique
            memory = psutil.virtual_memory()
            return {
                "gpu_device": self.gpu_device,
                "system_memory_percent": memory.percent,
                "available": True
            }
        except Exception as e:
            logger.error(f"Erreur monitoring GPU: {str(e)}")
            return {"available": False, "error": str(e)}

class ModelManager:
    """Gestionnaire centralisé des modèles IA avec support Ollama"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "models_config.json"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.usage_stats: Dict[str, ModelUsage] = {}
        self.ollama_client = OllamaClient(
            base_url=self.config.get("model_providers", {}).get("ollama", {}).get("base_url", "http://localhost:11434"),
            gpu_device=self.config.get("model_providers", {}).get("ollama", {}).get("gpu_device", "1")
        )
        
        # Configuration environnement
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.env_config = self.config.get("environments", {}).get(self.environment, {})
        
        logger.info(f"ModelManager initialisé - Environnement: {self.environment}")
        logger.info(f"Support Ollama: {self._is_ollama_enabled()}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration depuis le fichier JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erreur chargement configuration: {str(e)}")
            return {}
    
    def _is_ollama_enabled(self) -> bool:
        """Vérifie si Ollama est activé"""
        return (
            self.config.get("local_models_config", {}).get("enabled", False) and
            "ollama" in self.config.get("model_providers", {})
        )
    
    async def get_model_for_agent(self, agent_id: str, task_type: str = "general") -> Tuple[str, ModelProvider]:
        """Sélectionne le modèle optimal pour un agent donné"""
        
        agent_config = self.config.get("agent_models", {}).get(agent_id, {})
        if not agent_config:
            # Fallback vers modèles par défaut
            return self._get_default_model(task_type)
        
        # Stratégie de sélection selon politiques
        local_config = self.config.get("local_models_config", {})
        env_prefer_local = self.env_config.get("prefer_local", False)
        agent_prefer_local = agent_config.get("prefer_local", False)
        
        # Conditions pour utiliser modèles locaux
        should_use_local = (
            self._is_ollama_enabled() and
            (env_prefer_local or agent_prefer_local) and
            (task_type in local_config.get("prefer_local_for", []) or 
             "code" in task_type.lower() and local_config.get("prefer_local_for_code", False) or
             "privacy" in task_type.lower() and local_config.get("prefer_local_for_privacy", False))
        )
        
        if should_use_local and "local" in agent_config:
            # Vérifier disponibilité du modèle local
            local_model = agent_config["local"]
            if await self.ollama_client.check_model_availability(local_model):
                return local_model, ModelProvider.OLLAMA
            else:
                logger.warning(f"Modèle local {local_model} non disponible, fallback vers cloud")
        
        # Utiliser modèle primary cloud
        primary_model = agent_config.get("primary")
        if primary_model:
            provider = self._get_provider_for_model(primary_model)
            return primary_model, provider
        
        # Fallback ultime
        return self._get_default_model(task_type)
    
    def _get_provider_for_model(self, model_name: str) -> ModelProvider:
        """Détermine le provider d'un modèle"""
        for provider_name, provider_config in self.config.get("model_providers", {}).items():
            if model_name in provider_config.get("models", {}):
                return ModelProvider(provider_name)
        
        # Détection par nom de modèle
        if "claude" in model_name.lower():
            return ModelProvider.ANTHROPIC
        elif "gpt" in model_name.lower():
            return ModelProvider.OPENAI
        elif any(local_name in model_name.lower() for local_name in ["llama", "mistral", "qwen", "mixtral"]):
            return ModelProvider.OLLAMA
        
        return ModelProvider.OPENAI  # Fallback
    
    def _get_default_model(self, task_type: str) -> Tuple[str, ModelProvider]:
        """Modèle par défaut selon le type de tâche"""
        defaults = self.config.get("default_models", {})
        
        if self.env_config.get("prefer_local", False) and self._is_ollama_enabled():
            if task_type == "code":
                return defaults.get("local_code", "qwen-coder-32b"), ModelProvider.OLLAMA
            elif task_type == "fast":
                return defaults.get("local_fast", "nous-hermes-2-mistral-7b-dpo"), ModelProvider.OLLAMA
            else:
                return defaults.get("local_primary", "llama3.1:8b-instruct-q6_k"), ModelProvider.OLLAMA
        
        # Modèles cloud par défaut
        if task_type == "research":
            return defaults.get("research", "claude-3-opus-20240229"), ModelProvider.ANTHROPIC
        elif task_type == "fast":
            return defaults.get("fast", "gpt-3.5-turbo"), ModelProvider.OPENAI
        else:
            return defaults.get("primary", "claude-3-sonnet-20240229"), ModelProvider.ANTHROPIC
    
    async def generate_response(self, agent_id: str, prompt: str, task_type: str = "general", **kwargs) -> Dict[str, Any]:
        """Génère une réponse en utilisant le modèle optimal"""
        
        model_name, provider = await self.get_model_for_agent(agent_id, task_type)
        
        try:
            if provider == ModelProvider.OLLAMA:
                result = await self._generate_ollama(model_name, prompt, **kwargs)
            elif provider == ModelProvider.ANTHROPIC:
                result = await self._generate_anthropic(model_name, prompt, **kwargs)
            elif provider == ModelProvider.OPENAI:
                result = await self._generate_openai(model_name, prompt, **kwargs)
            else:
                raise ValueError(f"Provider non supporté: {provider}")
            
            # Mise à jour statistiques
            self._update_usage_stats(model_name, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur génération avec {model_name} ({provider}): {str(e)}")
            
            # Tentative de fallback
            if provider != ModelProvider.OLLAMA and self._is_ollama_enabled():
                return await self._try_fallback_local(agent_id, prompt, task_type, **kwargs)
            else:
                return await self._try_fallback_cloud(agent_id, prompt, task_type, **kwargs)
    
    async def _generate_ollama(self, model: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Génération avec Ollama (modèles locaux)"""
        return await self.ollama_client.generate(model, prompt, **kwargs)
    
    async def _generate_anthropic(self, model: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Génération avec Anthropic Claude"""
        # Implémentation à compléter selon vos besoins
        return {
            "response": f"[ANTHROPIC {model}] Réponse générée pour: {prompt[:50]}...",
            "model": model,
            "provider": "anthropic",
            "success": True,
            "tokens": 100,
            "cost": 0.01
        }
    
    async def _generate_openai(self, model: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Génération avec OpenAI GPT"""
        # Implémentation à compléter selon vos besoins
        return {
            "response": f"[OPENAI {model}] Réponse générée pour: {prompt[:50]}...",
            "model": model,
            "provider": "openai", 
            "success": True,
            "tokens": 100,
            "cost": 0.005
        }
    
    async def _try_fallback_local(self, agent_id: str, prompt: str, task_type: str, **kwargs) -> Dict[str, Any]:
        """Tentative de fallback vers modèles locaux"""
        logger.info(f"Tentative fallback local pour agent {agent_id}")
        
        # Utiliser modèle local par défaut
        local_model = self.config.get("default_models", {}).get("local_primary", "llama3.1:8b-instruct-q6_k")
        
        try:
            return await self._generate_ollama(local_model, prompt, **kwargs)
        except Exception as e:
            logger.error(f"Échec fallback local: {str(e)}")
            return {
                "response": "Erreur: Tous les modèles indisponibles",
                "success": False,
                "error": str(e)
            }
    
    async def _try_fallback_cloud(self, agent_id: str, prompt: str, task_type: str, **kwargs) -> Dict[str, Any]:
        """Tentative de fallback vers modèles cloud"""
        logger.info(f"Tentative fallback cloud pour agent {agent_id}")
        
        agent_config = self.config.get("agent_models", {}).get(agent_id, {})
        fallback_model = agent_config.get("fallback")
        
        if fallback_model:
            provider = self._get_provider_for_model(fallback_model)
            try:
                if provider == ModelProvider.ANTHROPIC:
                    return await self._generate_anthropic(fallback_model, prompt, **kwargs)
                elif provider == ModelProvider.OPENAI:
                    return await self._generate_openai(fallback_model, prompt, **kwargs)
            except Exception as e:
                logger.error(f"Échec fallback cloud {fallback_model}: {str(e)}")
        
        return {
            "response": "Erreur: Aucun modèle de fallback disponible",
            "success": False,
            "error": "Fallback failed"
        }
    
    def _update_usage_stats(self, model_name: str, result: Dict[str, Any]):
        """Met à jour les statistiques d'utilisation"""
        if model_name not in self.usage_stats:
            self.usage_stats[model_name] = ModelUsage()
        
        stats = self.usage_stats[model_name]
        stats.total_requests += 1
        stats.total_tokens += result.get("tokens", 0)
        stats.total_cost += result.get("cost", 0.0)
        stats.last_used = datetime.now()
        
        if result.get("success", False):
            response_time = result.get("response_time", 0)
            stats.avg_response_time = (stats.avg_response_time * (stats.total_requests - 1) + response_time) / stats.total_requests
        else:
            stats.error_count += 1
    
    async def get_system_status(self) -> Dict[str, Any]:
        """État du système de modèles"""
        
        # Vérification Ollama
        ollama_status = {"available": False, "models": []}
        if self._is_ollama_enabled():
            try:
                ollama_models = await self.ollama_client.list_models()
                gpu_usage = await self.ollama_client.get_gpu_usage()
                ollama_status = {
                    "available": True,
                    "models": ollama_models,
                    "gpu_usage": gpu_usage
                }
            except Exception as e:
                ollama_status["error"] = str(e)
        
        return {
            "environment": self.environment,
            "config_loaded": bool(self.config),
            "ollama": ollama_status,
            "usage_stats": {
                model: {
                    "requests": stats.total_requests,
                    "tokens": stats.total_tokens,
                    "cost": stats.total_cost,
                    "avg_response_time": stats.avg_response_time,
                    "error_rate": stats.error_count / max(stats.total_requests, 1)
                }
                for model, stats in self.usage_stats.items()
            },
            "local_models_enabled": self._is_ollama_enabled(),
            "total_cost": sum(stats.total_cost for stats in self.usage_stats.values())
        }

# Instance globale du gestionnaire
model_manager = ModelManager()

async def get_model_manager() -> ModelManager:
    """Récupère l'instance du gestionnaire de modèles"""
    return model_manager

# Exemple d'utilisation pour les agents
if __name__ == "__main__":
    # Test du gestionnaire
    manager = ModelManager()
    
    # Configuration pour agent sécurité
    agent_config = manager.get_agent_model_config("agent_04_expert_securite_crypto")
    print(f"Agent 04 - Modèle principal: {agent_config.primary_model.model_id}")
    print(f"Agent 04 - Modèle fallback: {agent_config.fallback_model.model_id}")
    
    # Simulation usage
    model = manager.get_model_for_agent("agent_04_expert_securite_crypto")
    manager.track_model_usage("agent_04_expert_securite_crypto", model, 1000, 500)
    
    # Stats
    stats = manager.get_usage_stats()
    print(f"Coût quotidien: ${stats['daily_cost']:.4f}") 