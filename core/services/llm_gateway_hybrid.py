#!/usr/bin/env python3
"""
LLMGateway Hybride - Phase 0 Semaine 2
Service unifié pour gestion LLM avec support Ollama existant + modèles distants

Objectifs:
- Centraliser l'accès aux modèles LLM (Ollama RTX3090 + modèles distants)
- Cache intelligent Redis pour optimisation
- Rate limiting et retry logic avec Tenacity
- Context injection pour agents legacy
- Métriques de coût/performance
"""

import asyncio
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Imports pour LLM et cache
try:
    import aiohttp
    import redis.asyncio as redis
    from tenacity import retry, stop_after_attempt, wait_exponential
except ImportError as e:
    print(f"⚠️  Missing dependencies: {e}")
    print("Install with: pip install aiohttp redis tenacity")

@dataclass
class LLMResponse:
    """Réponse standardisée des modèles LLM"""
    content: str
    model: str
    token_count: int
    latency_ms: int
    cost_estimate: float
    cached: bool
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    @classmethod
    def from_cache(cls, cached_data: Dict) -> 'LLMResponse':
        """Crée une réponse depuis le cache"""
        cached_data['cached'] = True
        cached_data['timestamp'] = datetime.fromisoformat(cached_data['timestamp'])
        return cls(**cached_data)
    
    def to_dict(self) -> Dict:
        """Sérialise pour cache"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data

@dataclass
class GatewayConfig:
    """Configuration du LLMGateway"""
    ollama_base_url: str = "http://localhost:11434"
    redis_url: str = "redis://localhost:6379"
    cache_ttl_seconds: int = 3600
    max_retries: int = 3
    rate_limit_per_minute: int = 60
    default_model: str = "llama3:8b-instruct-q6_k"
    enable_remote_models: bool = False
    voice_priority_quota: float = 0.3  # 30% GPU réservé vocal

class ModelType(Enum):
    """Types de modèles disponibles"""
    LOCAL_OLLAMA = "local_ollama"
    REMOTE_OPENAI = "remote_openai"
    REMOTE_ANTHROPIC = "remote_anthropic"

class Priority(Enum):
    """Priorités de requêtes"""
    VOICE_REALTIME = "voice_realtime"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class LLMRequest:
    """Requête LLM standardisée"""
    prompt: str
    model: str
    context: Optional[Dict] = None
    agent_id: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    max_tokens: int = 2048
    temperature: float = 0.7
    is_voice_request: bool = False
    max_latency_ms: int = 5000

class ContextEnhancer:
    """Améliore les prompts avec contexte agent"""
    
    def __init__(self):
        self.context_templates = {
            "agent_base": """
Contexte Agent: {agent_id}
Mission: {mission}
Dernière action: {last_action}
Métriques: {metrics}

---
""",
            "voice_command": """
COMMANDE VOCALE - PRIORITÉ MAXIMALE
Session: {voice_session_id}
Confidence STT: {stt_confidence}
Target latency: <{target_latency_ms}ms

---
"""
        }
    
    async def enhance(self, prompt: str, context: Dict, agent_id: str) -> str:
        """Améliore le prompt avec le contexte"""
        
        if context.get('is_voice_request'):
            template = self.context_templates['voice_command']
            enhanced_context = template.format(**context)
        else:
            template = self.context_templates['agent_base']
            enhanced_context = template.format(
                agent_id=agent_id,
                mission=context.get('mission', 'Non définie'),
                last_action=context.get('last_action', 'Aucune'),
                metrics=context.get('metrics', 'N/A')
            )
        
        return enhanced_context + prompt

class CostTracker:
    """Suivi des coûts et métriques"""
    
    def __init__(self):
        self.costs = {
            "local_ollama": 0.0,  # GPU electricity cost estimate
            "remote_openai": 0.002,  # per 1K tokens
            "remote_anthropic": 0.003  # per 1K tokens
        }
        self.daily_usage = {}
        self.total_requests = 0
        self.total_cost = 0.0
    
    def record(self, model: str, token_count: int, latency_ms: int):
        """Enregistre l'usage et calcule les coûts"""
        
        model_type = self._get_model_type(model)
        cost = self._calculate_cost(model_type, token_count)
        
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.daily_usage:
            self.daily_usage[today] = {
                "requests": 0,
                "tokens": 0,
                "cost": 0.0,
                "avg_latency": 0.0
            }
        
        daily = self.daily_usage[today]
        daily["requests"] += 1
        daily["tokens"] += token_count
        daily["cost"] += cost
        daily["avg_latency"] = (daily["avg_latency"] * (daily["requests"] - 1) + latency_ms) / daily["requests"]
        
        self.total_requests += 1
        self.total_cost += cost
    
    def _get_model_type(self, model: str) -> str:
        """Détermine le type de modèle"""
        if "gpt" in model.lower():
            return "remote_openai"
        elif "claude" in model.lower():
            return "remote_anthropic"
        else:
            return "local_ollama"
    
    def _calculate_cost(self, model_type: str, token_count: int) -> float:
        """Calcule le coût de la requête"""
        cost_per_1k = self.costs.get(model_type, 0.0)
        return (token_count / 1000) * cost_per_1k
    
    def get_daily_report(self) -> Dict:
        """Rapport d'usage quotidien"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.daily_usage.get(today, {})

class RateLimiter:
    """Limitation du taux de requêtes"""
    
    def __init__(self, max_requests_per_minute: int = 60):
        self.max_requests = max_requests_per_minute
        self.requests = []
        self.voice_priority_slots = int(max_requests_per_minute * 0.3)  # 30% pour vocal
    
    async def acquire(self, model: str, is_voice: bool = False):
        """Acquiert un slot de requête"""
        
        now = time.time()
        # Nettoyer les requêtes anciennes
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        if is_voice and len([r for r in self.requests if r > now - 60]) < self.voice_priority_slots:
            # Slot vocal prioritaire
            self.requests.append(now)
            return
        
        if len(self.requests) >= self.max_requests:
            # Attendre avant la prochaine requête
            wait_time = 60 - (now - self.requests[0])
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        self.requests.append(now)

class LLMGatewayHybrid:
    """Gateway LLM hybride avec support Ollama + modèles distants"""
    
    def __init__(self, config: GatewayConfig):
        self.config = config
        self.context_enhancer = ContextEnhancer()
        self.cost_tracker = CostTracker()
        self.rate_limiter = RateLimiter(config.rate_limit_per_minute)
        
        # Cache Redis
        self.redis_client = None
        
        # Session HTTP pour requêtes
        self.http_session = None
        
        # Métriques
        self.metrics = {
            "requests_total": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0,
            "avg_latency": 0.0
        }
        
        # Logger
        self.logger = logging.getLogger("LLMGateway")
        
        # Modèles disponibles
        self.available_models = {
            ModelType.LOCAL_OLLAMA: [
                "llama3:8b-instruct-q6_k",
                "codellama:latest",
                "mistral:latest",
                "deepseek-coder:latest"
            ],
            ModelType.REMOTE_OPENAI: [
                "gpt-4",
                "gpt-3.5-turbo"
            ],
            ModelType.REMOTE_ANTHROPIC: [
                "claude-3.5-sonnet",
                "claude-3-haiku"
            ]
        }
    
    async def initialize(self):
        """Initialise les connexions"""
        
        try:
            # Connexion Redis
            self.redis_client = redis.from_url(self.config.redis_url)
            await self.redis_client.ping()
            self.logger.info("✅ Redis connected")
            
            # Session HTTP
            self.http_session = aiohttp.ClientSession()
            
            # Test Ollama
            await self._test_ollama_connection()
            
            self.logger.info("🚀 LLMGateway initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize LLMGateway: {e}")
            raise
    
    async def cleanup(self):
        """Nettoie les ressources"""
        if self.http_session:
            await self.http_session.close()
        if self.redis_client:
            await self.redis_client.close()
    
    async def _test_ollama_connection(self):
        """Test de connexion Ollama"""
        try:
            async with self.http_session.get(f"{self.config.ollama_base_url}/api/tags") as response:
                if response.status == 200:
                    models = await response.json()
                    model_names = [model['name'] for model in models.get('models', [])]
                    self.logger.info(f"✅ Ollama connected - Models: {len(model_names)}")
                    return True
        except Exception as e:
            self.logger.warning(f"⚠️  Ollama connection failed: {e}")
            return False
    
    def _generate_cache_key(self, prompt: str, model: str, context: Dict = None) -> str:
        """Génère une clé de cache pour la requête"""
        content = f"{prompt}|{model}"
        if context:
            content += f"|{json.dumps(context, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def _get_from_cache(self, cache_key: str) -> Optional[LLMResponse]:
        """Récupère depuis le cache"""
        try:
            cached = await self.redis_client.get(cache_key)
            if cached:
                data = json.loads(cached)
                self.metrics["cache_hits"] += 1
                return LLMResponse.from_cache(data)
        except Exception as e:
            self.logger.warning(f"Cache read error: {e}")
        
        self.metrics["cache_misses"] += 1
        return None
    
    async def _save_to_cache(self, cache_key: str, response: LLMResponse):
        """Sauvegarde en cache"""
        try:
            data = response.to_dict()
            await self.redis_client.setex(
                cache_key, 
                self.config.cache_ttl_seconds, 
                json.dumps(data)
            )
        except Exception as e:
            self.logger.warning(f"Cache write error: {e}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def _query_ollama(self, request: LLMRequest) -> LLMResponse:
        """Requête vers Ollama local"""
        
        start_time = time.time()
        
        payload = {
            "model": request.model,
            "prompt": request.prompt,
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens
            }
        }
        
        async with self.http_session.post(
            f"{self.config.ollama_base_url}/api/generate",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=request.max_latency_ms/1000)
        ) as response:
            
            if response.status != 200:
                raise Exception(f"Ollama error: {response.status}")
            
            result = await response.json()
            latency_ms = int((time.time() - start_time) * 1000)
            
            return LLMResponse(
                content=result.get("response", ""),
                model=request.model,
                token_count=len(result.get("response", "").split()),  # Approximation
                latency_ms=latency_ms,
                cost_estimate=0.0,  # Local model
                cached=False,
                timestamp=datetime.now(),
                metadata={"provider": "ollama"}
            )
    
    async def _select_optimal_model(self, request: LLMRequest) -> str:
        """Sélectionne le modèle optimal selon les contraintes"""
        
        # Pour les requêtes vocales, privilégier rapidité
        if request.is_voice_request:
            if request.max_latency_ms < 2000:
                return "mistral:latest"  # Plus rapide
            else:
                return "llama3:8b-instruct-q6_k"
        
        # Pour les autres requêtes, utiliser le modèle demandé ou par défaut
        return request.model or self.config.default_model
    
    async def query(self, 
                   prompt: str, 
                   model: str = None,
                   context: Optional[Dict] = None,
                   agent_id: Optional[str] = None,
                   priority: Priority = Priority.MEDIUM,
                   is_voice_request: bool = False,
                   max_latency_ms: int = 5000) -> LLMResponse:
        """
        Requête LLM principale avec support complet
        """
        
        try:
            self.metrics["requests_total"] += 1
            
            # Créer la requête
            request = LLMRequest(
                prompt=prompt,
                model=model or self.config.default_model,
                context=context,
                agent_id=agent_id,
                priority=priority,
                is_voice_request=is_voice_request,
                max_latency_ms=max_latency_ms
            )
            
            # Sélection du modèle optimal
            optimal_model = await self._select_optimal_model(request)
            request.model = optimal_model
            
            # Enhancement du prompt avec contexte
            enhanced_prompt = prompt
            if agent_id and context:
                enhanced_prompt = await self.context_enhancer.enhance(
                    prompt, context, agent_id
                )
            
            # Vérification cache
            cache_key = self._generate_cache_key(enhanced_prompt, request.model, context)
            cached_response = await self._get_from_cache(cache_key)
            if cached_response:
                self.logger.info(f"✅ Cache hit for model {request.model}")
                return cached_response
            
            # Rate limiting
            await self.rate_limiter.acquire(request.model, is_voice_request)
            
            # Mise à jour du prompt
            request.prompt = enhanced_prompt
            
            # Exécution de la requête
            response = await self._query_ollama(request)
            
            # Sauvegarde cache
            await self._save_to_cache(cache_key, response)
            
            # Métriques
            self.cost_tracker.record(response.model, response.token_count, response.latency_ms)
            self._update_metrics(response.latency_ms)
            
            self.logger.info(
                f"✅ LLM query completed - Model: {response.model}, "
                f"Latency: {response.latency_ms}ms, Tokens: {response.token_count}"
            )
            
            return response
            
        except Exception as e:
            self.metrics["errors"] += 1
            self.logger.error(f"❌ LLM query failed: {e}")
            raise
    
    async def query_with_voice_priority(self, 
                                      prompt: str,
                                      is_voice_request: bool = False,
                                      max_latency_ms: int = 1500) -> LLMResponse:
        """Requête LLM avec gestion priorité vocale"""
        
        return await self.query(
            prompt=prompt,
            priority=Priority.VOICE_REALTIME if is_voice_request else Priority.MEDIUM,
            is_voice_request=is_voice_request,
            max_latency_ms=max_latency_ms
        )
    
    def _update_metrics(self, latency_ms: int):
        """Met à jour les métriques moyennes"""
        total_requests = self.metrics["requests_total"]
        current_avg = self.metrics["avg_latency"]
        
        self.metrics["avg_latency"] = (
            (current_avg * (total_requests - 1) + latency_ms) / total_requests
        )
    
    def get_metrics(self) -> Dict:
        """Retourne les métriques actuelles"""
        return {
            **self.metrics,
            "cache_hit_rate": self.metrics["cache_hits"] / max(self.metrics["requests_total"], 1),
            "cost_tracker": self.cost_tracker.get_daily_report(),
            "available_models": self.available_models
        }
    
    async def health_check(self) -> Dict:
        """Vérification de santé du gateway"""
        
        health = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {}
        }
        
        # Test Redis
        try:
            await self.redis_client.ping()
            health["components"]["redis"] = "healthy"
        except:
            health["components"]["redis"] = "unhealthy"
            health["status"] = "degraded"
        
        # Test Ollama
        ollama_ok = await self._test_ollama_connection()
        health["components"]["ollama"] = "healthy" if ollama_ok else "unhealthy"
        if not ollama_ok:
            health["status"] = "degraded"
        
        return health

# Factory function pour création simplifiée
async def create_llm_gateway(config: GatewayConfig = None) -> LLMGatewayHybrid:
    """Crée et initialise un LLMGateway"""
    
    if config is None:
        config = GatewayConfig()
    
    gateway = LLMGatewayHybrid(config)
    await gateway.initialize()
    return gateway

# Test et démonstration
async def demo_llm_gateway():
    """Démonstration du LLMGateway"""
    
    print("🚀 LLMGateway Hybrid Demo - Phase 0 Week 2")
    print("=" * 60)
    
    # Configuration
    config = GatewayConfig(
        cache_ttl_seconds=300,  # 5 minutes pour demo
        rate_limit_per_minute=30
    )
    
    try:
        # Création du gateway
        gateway = await create_llm_gateway(config)
        
        # Test simple
        print("\n🧪 Test 1: Requête simple")
        response = await gateway.query(
            prompt="Explain what is a microservice architecture in 2 sentences.",
            model="llama3:8b-instruct-q6_k"
        )
        print(f"Response: {response.content[:100]}...")
        print(f"Latency: {response.latency_ms}ms")
        
        # Test avec contexte agent
        print("\n🧪 Test 2: Requête avec contexte agent")
        context = {
            "mission": "Code review and quality assurance",
            "last_action": "Analyzed 3 Python files",
            "metrics": "95% test coverage"
        }
        
        response = await gateway.query(
            prompt="What should I check next in my code review process?",
            context=context,
            agent_id="agent_111_auditeur_qualite"
        )
        print(f"Response: {response.content[:100]}...")
        print(f"Cached: {response.cached}")
        
        # Test cache (même requête)
        print("\n🧪 Test 3: Test cache")
        response2 = await gateway.query(
            prompt="What should I check next in my code review process?",
            context=context,
            agent_id="agent_111_auditeur_qualite"
        )
        print(f"Cached: {response2.cached}")
        print(f"Latency: {response2.latency_ms}ms")
        
        # Test vocal priorité
        print("\n🧪 Test 4: Requête vocale prioritaire")
        response = await gateway.query_with_voice_priority(
            prompt="Quick summary of current project status",
            is_voice_request=True,
            max_latency_ms=1500
        )
        print(f"Voice response latency: {response.latency_ms}ms")
        
        # Métriques
        print("\n📊 Métriques Gateway")
        metrics = gateway.get_metrics()
        print(f"Total requests: {metrics['requests_total']}")
        print(f"Cache hit rate: {metrics['cache_hit_rate']:.2%}")
        print(f"Average latency: {metrics['avg_latency']:.1f}ms")
        print(f"Errors: {metrics['errors']}")
        
        # Health check
        print("\n🏥 Health Check")
        health = await gateway.health_check()
        print(f"Status: {health['status']}")
        print(f"Components: {health['components']}")
        
        await gateway.cleanup()
        print("\n✅ Demo completed successfully")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(demo_llm_gateway())