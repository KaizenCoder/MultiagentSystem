#!/usr/bin/env python3
"""
🌐 Agent API Gateway - NextGeneration v5.3.0
Version enterprise Wave 4 avec gateway unifié IA

Migration Pattern: API_MANAGEMENT + SECURITY + LLM_ENHANCED
Author: Claude Sonnet 4
Date: 30 Juin 2025
"""

import asyncio
import json
import time
import hashlib
import jwt
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import aiohttp
from aiohttp import web, ClientSession
import ssl
import re
import statistics
from collections import defaultdict, deque
import ipaddress

# Imports NextGeneration Architecture
try:
    from core.services import (
        LLMGatewayHybrid, create_llm_gateway,
        MessageBusA2A, create_envelope, MessageType, Priority,
        OptimizedContextStore, create_agent_context, ContextType
    )
    from core.agent_factory_architecture import Task, Result
except ImportError:
    # Fallback pour développement isolé
    print("⚠️ NextGeneration services not available - running in development mode")
    class Task:
        def __init__(self, task_type, params=None):
            self.type = task_type
            self.params = params or {}
    
    class Result:
        def __init__(self, success, data=None, error=None, metrics=None):
            self.success = success
            self.data = data
            self.error = error
            self.metrics = metrics or {}

class AuthMethod(str, Enum):
    """Méthodes d'authentification"""
    JWT = "JWT"
    API_KEY = "API_KEY"
    OAUTH2 = "OAUTH2"
    MUTUAL_TLS = "MUTUAL_TLS"
    INTELLIGENT = "INTELLIGENT"  # IA contextuelle

class RateLimitPolicy(str, Enum):
    """Politiques rate limiting"""
    FIXED_WINDOW = "FIXED_WINDOW"
    SLIDING_WINDOW = "SLIDING_WINDOW"
    TOKEN_BUCKET = "TOKEN_BUCKET"
    ADAPTIVE = "ADAPTIVE"  # Adaptatif avec IA

@dataclass
class APIRoute:
    """Route API configurée"""
    path: str
    method: str
    backend_url: str
    auth_required: bool = True
    auth_methods: List[AuthMethod] = None
    rate_limit: Optional[int] = None
    rate_limit_policy: RateLimitPolicy = RateLimitPolicy.SLIDING_WINDOW
    timeout_seconds: int = 30
    retry_count: int = 3
    circuit_breaker: bool = True
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class APIClient:
    """Client API enregistré"""
    client_id: str
    name: str
    api_key_hash: str
    allowed_routes: List[str]
    rate_limit_per_hour: int
    created_at: datetime
    last_access: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class RequestMetrics:
    """Métriques requête"""
    timestamp: datetime
    client_id: str
    route: str
    method: str
    status_code: int
    response_time_ms: float
    backend_response_time_ms: float
    request_size_bytes: int
    response_size_bytes: int

class IntelligentAuthenticator:
    """Authentificateur intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.suspicious_patterns = {
            "high_frequency": 100,  # requests/minute
            "unusual_hours": [2, 3, 4, 5],  # 2h-5h
            "geographic_anomaly": True,
            "user_agent_suspicious": [
                r"bot", r"crawler", r"spider", r"scan"
            ]
        }
        self.client_profiles = defaultdict(dict)
    
    async def authenticate_request(self, request: web.Request, 
                                 route: APIRoute) -> Dict[str, Any]:
        """Authentification intelligente contextuelle"""
        auth_result = {
            "authenticated": False,
            "client_id": None,
            "method_used": None,
            "confidence": 0.0,
            "anomalies": []
        }
        
        # Tentative authentification par méthodes configurées
        for auth_method in route.auth_methods or [AuthMethod.API_KEY]:
            if auth_method == AuthMethod.API_KEY:
                result = await self._authenticate_api_key(request)
            elif auth_method == AuthMethod.JWT:
                result = await self._authenticate_jwt(request)
            elif auth_method == AuthMethod.INTELLIGENT:
                result = await self._authenticate_intelligent(request)
            else:
                continue
            
            if result["authenticated"]:
                auth_result.update(result)
                break
        
        # Analyse comportementale si authentifié
        if auth_result["authenticated"]:
            anomalies = await self._analyze_behavioral_anomalies(request, auth_result["client_id"])
            auth_result["anomalies"] = anomalies
            
            # Ajustement confidence selon anomalies
            if anomalies:
                auth_result["confidence"] *= (1 - len(anomalies) * 0.1)
        
        return auth_result
    
    async def _authenticate_api_key(self, request: web.Request) -> Dict[str, Any]:
        """Authentification API Key"""
        api_key = request.headers.get("X-API-Key") or request.query.get("api_key")
        
        if not api_key:
            return {"authenticated": False}
        
        # Hash et vérification (simulation)
        api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Recherche client (simulation - remplacer par vraie DB)
        client_id = f"client_{api_key_hash[:8]}"
        
        return {
            "authenticated": True,
            "client_id": client_id,
            "method_used": AuthMethod.API_KEY,
            "confidence": 0.9
        }
    
    async def _authenticate_jwt(self, request: web.Request) -> Dict[str, Any]:
        """Authentification JWT"""
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"authenticated": False}
        
        token = auth_header[7:]  # Remove "Bearer "
        
        try:
            # Vérification JWT (simulation - utiliser vraie clé)
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            
            return {
                "authenticated": True,
                "client_id": payload.get("client_id"),
                "method_used": AuthMethod.JWT,
                "confidence": 0.95
            }
        except jwt.InvalidTokenError:
            return {"authenticated": False}
    
    async def _authenticate_intelligent(self, request: web.Request) -> Dict[str, Any]:
        """Authentification intelligente IA"""
        if not self.llm_gateway:
            return {"authenticated": False}
        
        # Collecte contexte requête
        context = {
            "ip": request.remote,
            "user_agent": request.headers.get("User-Agent"),
            "timestamp": datetime.now().isoformat(),
            "path": request.path,
            "method": request.method,
            "headers": dict(request.headers)
        }
        
        try:
            ai_auth = await self.llm_gateway.process_request(
                "Analyze request for intelligent authentication",
                context={
                    "role": "security_authentication_expert",
                    "request_context": context,
                    "task": "intelligent_authentication_analysis"
                }
            )
            
            if ai_auth.get("success"):
                result = ai_auth.get("authentication", {})
                return {
                    "authenticated": result.get("authenticated", False),
                    "client_id": result.get("client_id"),
                    "method_used": AuthMethod.INTELLIGENT,
                    "confidence": result.get("confidence", 0.5)
                }
        except Exception:
            pass
        
        return {"authenticated": False}
    
    async def _analyze_behavioral_anomalies(self, request: web.Request, 
                                          client_id: str) -> List[str]:
        """Analyse anomalies comportementales"""
        anomalies = []
        
        # Profil client
        profile = self.client_profiles[client_id]
        current_hour = datetime.now().hour
        
        # Fréquence inhabituelle
        requests_per_minute = profile.get("requests_per_minute", 0)
        if requests_per_minute > self.suspicious_patterns["high_frequency"]:
            anomalies.append("high_frequency_requests")
        
        # Heures inhabituelles
        if current_hour in self.suspicious_patterns["unusual_hours"]:
            anomalies.append("unusual_access_hours")
        
        # User-Agent suspect
        user_agent = request.headers.get("User-Agent", "").lower()
        for pattern in self.suspicious_patterns["user_agent_suspicious"]:
            if re.search(pattern, user_agent):
                anomalies.append("suspicious_user_agent")
                break
        
        return anomalies

class AdaptiveRateLimiter:
    """Rate limiter adaptatif avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.client_buckets = defaultdict(lambda: {"tokens": 100, "last_refill": time.time()})
        self.request_windows = defaultdict(lambda: deque(maxlen=3600))  # 1h window
        self.adaptive_limits = defaultdict(lambda: 1000)  # requests/hour
    
    async def check_rate_limit(self, client_id: str, route: str,
                             default_limit: int = 1000) -> Dict[str, Any]:
        """Vérification rate limit adaptatif"""
        now = time.time()
        
        # Limite adaptative ou par défaut
        current_limit = self.adaptive_limits.get(f"{client_id}:{route}", default_limit)
        
        # Token bucket algorithm
        bucket = self.client_buckets[f"{client_id}:{route}"]
        time_passed = now - bucket["last_refill"]
        
        # Refill tokens
        tokens_to_add = time_passed * (current_limit / 3600)  # per second
        bucket["tokens"] = min(current_limit, bucket["tokens"] + tokens_to_add)
        bucket["last_refill"] = now
        
        # Vérification disponibilité
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            
            # Enregistrement requête
            window = self.request_windows[f"{client_id}:{route}"]
            window.append(now)
            
            # Adaptation intelligente si IA disponible
            if self.llm_gateway and len(window) > 10:
                await self._adapt_rate_limit(client_id, route, window)
            
            return {
                "allowed": True,
                "remaining": int(bucket["tokens"]),
                "reset_time": now + 3600,
                "current_limit": current_limit
            }
        else:
            return {
                "allowed": False,
                "remaining": 0,
                "reset_time": now + (1 - bucket["tokens"]) / (current_limit / 3600),
                "current_limit": current_limit
            }
    
    async def _adapt_rate_limit(self, client_id: str, route: str, 
                              request_window: deque):
        """Adaptation intelligente limites"""
        try:
            # Analyse pattern requêtes
            now = time.time()
            recent_requests = [t for t in request_window if now - t < 300]  # 5 min
            requests_per_minute = len(recent_requests) / 5
            
            # Demande IA pour adaptation
            ai_adaptation = await self.llm_gateway.process_request(
                "Adapt rate limit based on usage pattern",
                context={
                    "role": "traffic_management_expert",
                    "client_id": client_id,
                    "route": route,
                    "requests_per_minute": requests_per_minute,
                    "total_requests_hour": len(request_window),
                    "task": "adaptive_rate_limiting"
                }
            )
            
            if ai_adaptation.get("success"):
                new_limit = ai_adaptation.get("suggested_limit")
                if new_limit and 100 <= new_limit <= 10000:  # Limites raisonnables
                    self.adaptive_limits[f"{client_id}:{route}"] = new_limit
                    
        except Exception:
            pass

class CircuitBreaker:
    """Circuit breaker pour backends"""
    
    def __init__(self):
        self.circuits = defaultdict(lambda: {
            "state": "CLOSED",  # CLOSED, OPEN, HALF_OPEN
            "failure_count": 0,
            "failure_threshold": 5,
            "timeout": 60,  # seconds
            "last_failure": 0
        })
    
    async def call_backend(self, backend_url: str, 
                          request_func: Callable) -> Dict[str, Any]:
        """Appel backend avec circuit breaker"""
        circuit = self.circuits[backend_url]
        now = time.time()
        
        # État OPEN - circuit ouvert
        if circuit["state"] == "OPEN":
            if now - circuit["last_failure"] > circuit["timeout"]:
                circuit["state"] = "HALF_OPEN"
            else:
                return {
                    "success": False,
                    "error": "Circuit breaker OPEN",
                    "status_code": 503
                }
        
        try:
            # Tentative appel
            result = await request_func()
            
            # Succès - reset circuit
            if circuit["state"] == "HALF_OPEN":
                circuit["state"] = "CLOSED"
                circuit["failure_count"] = 0
            
            return {"success": True, "result": result}
            
        except Exception as e:
            # Échec - increment failures
            circuit["failure_count"] += 1
            circuit["last_failure"] = now
            
            if circuit["failure_count"] >= circuit["failure_threshold"]:
                circuit["state"] = "OPEN"
            
            return {
                "success": False,
                "error": str(e),
                "status_code": 503
            }

class AgentAPIGateway_Enterprise:
    """
    🌐 Agent API Gateway - Enterprise NextGeneration v5.3.0
    
    Gateway API unifié avec sécurité intelligente et performance optimisée.
    
    Patterns NextGeneration v5.3.0:
    - API_MANAGEMENT: Gestion API enterprise complète
    - SECURITY: Authentification multi-méthodes + IA
    - LLM_ENHANCED: Rate limiting adaptatif + détection anomalies
    - PATTERN_FACTORY: Architecture modulaire éprouvée
    """
    
    def __init__(self, agent_id: str = "api_gateway", 
                 host: str = "0.0.0.0", port: int = 8080):
        # Métadonnées NextGeneration v5.3.0
        self.agent_id = agent_id
        self.version = "5.3.0"
        self.wave_version = "Wave 4 - Extensions Core"
        self.migration_status = "modern_active"
        self.compatibility_mode = True
        
        # Patterns NextGeneration appliqués
        self.__version__ = "5.3.0"
        self.__wave_version__ = "Wave 4 - Extensions Core"
        self.__nextgen_patterns__ = [
            "API_MANAGEMENT",
            "SECURITY",
            "LLM_ENHANCED",
            "PATTERN_FACTORY"
        ]
        
        # Configuration agent
        self.name = "API Gateway Enterprise"
        self.mission = "Gateway API unifié avec sécurité intelligente"
        self.agent_type = "api_gateway_enterprise"
        
        # Configuration serveur
        self.host = host
        self.port = port
        self.app = web.Application()
        self.runner = None
        self.site = None
        
        # Services NextGeneration (injectés à l'initialisation)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Composants sécurité et performance
        self.authenticator = IntelligentAuthenticator()
        self.rate_limiter = AdaptiveRateLimiter()
        self.circuit_breaker = CircuitBreaker()
        
        # Configuration routes
        self.routes: Dict[str, APIRoute] = {}
        self.clients: Dict[str, APIClient] = {}
        
        # Métriques temps réel
        self.gateway_metrics = {
            "requests_total": 0,
            "requests_successful": 0,
            "requests_failed": 0,
            "average_response_time_ms": 0.0,
            "active_connections": 0,
            "rate_limited_requests": 0,
            "authentication_failures": 0
        }
        
        # Historique métriques
        self.request_history: List[RequestMetrics] = []
        self.max_history_size = 10000
        
        # Setup logging
        self._setup_logging()
        
        # Configuration routes par défaut
        self._setup_default_routes()
    
    def _setup_logging(self):
        """Configuration logging NextGeneration"""
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="gateway",
                custom_config={
                    "logger_name": f"nextgen.gateway.api.{self.agent_id}",
                    "log_dir": "logs/gateway",
                    "metadata": {
                        "agent_type": "api_gateway",
                        "agent_role": "networking",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(f"APIGateway_{self.agent_id}")
    
    def _setup_default_routes(self):
        """Configuration routes par défaut"""
        # Route health check
        self.routes["/health"] = APIRoute(
            path="/health",
            method="GET",
            backend_url="internal://health",
            auth_required=False,
            rate_limit=100  # requests/hour
        )
        
        # Route métriques
        self.routes["/metrics"] = APIRoute(
            path="/metrics",
            method="GET", 
            backend_url="internal://metrics",
            auth_required=True,
            auth_methods=[AuthMethod.API_KEY],
            rate_limit=60
        )
        
        # Middleware setup
        self.app.middlewares.append(self._security_middleware)
        self.app.middlewares.append(self._rate_limiting_middleware)
        self.app.middlewares.append(self._metrics_middleware)
        
        # Routes handlers
        self.app.router.add_route("*", "/{path:.*}", self._handle_request)
    
    async def inject_nextgen_services(self, 
                                    llm_gateway: LLMGatewayHybrid,
                                    message_bus: MessageBusA2A, 
                                    context_store: OptimizedContextStore):
        """Injection des services NextGeneration v5.3.0"""
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus  
        self.context_store = context_store
        
        # Configuration composants avec IA
        self.authenticator.llm_gateway = llm_gateway
        self.rate_limiter.llm_gateway = llm_gateway
        
        # Configuration contexte gateway IA
        await self._setup_gateway_context()
        
        self.logger.info("✅ Services NextGeneration injectés - Gateway IA actif")
    
    async def _setup_gateway_context(self):
        """Configuration contexte gateway IA spécialisé"""
        if not self.llm_gateway:
            return
        
        gateway_context = {
            "role": "api_gateway_security_expert",
            "domain": "enterprise_api_management",
            "capabilities": [
                "Intelligent authentication",
                "Adaptive rate limiting",
                "Anomaly detection",
                "Traffic analysis",
                "Security threat mitigation"
            ],
            "patterns": [
                "API_MANAGEMENT",
                "SECURITY",
                "LLM_ENHANCED"
            ]
        }
        
        # Chargement expertise gateway depuis LLM
        try:
            response = await self.llm_gateway.process_request(
                "Load API gateway security expertise",
                context=gateway_context
            )
            
            if response.get("success"):
                self.logger.info("🧠 Expertise gateway IA chargée")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement contexte IA: {e}")
    
    async def start_server(self):
        """Démarrage serveur gateway"""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        
        self.site = web.TCPSite(self.runner, self.host, self.port)
        await self.site.start()
        
        self.logger.info(f"🌐 API Gateway démarré sur {self.host}:{self.port}")
    
    async def stop_server(self):
        """Arrêt serveur gateway"""
        if self.site:
            await self.site.stop()
        if self.runner:
            await self.runner.cleanup()
        
        self.logger.info("🌐 API Gateway arrêté")
    
    @web.middleware
    async def _security_middleware(self, request: web.Request, handler):
        """Middleware sécurité avec authentification intelligente"""
        start_time = time.time()
        
        # Recherche route correspondante
        route = self._find_matching_route(request.path, request.method)
        
        if not route:
            return web.json_response(
                {"error": "Route not found"}, 
                status=404
            )
        
        # Authentification si requise
        if route.auth_required:
            auth_result = await self.authenticator.authenticate_request(request, route)
            
            if not auth_result["authenticated"]:
                self.gateway_metrics["authentication_failures"] += 1
                return web.json_response(
                    {"error": "Authentication failed"}, 
                    status=401
                )
            
            # Stockage info client dans request
            request["client_id"] = auth_result["client_id"]
            request["auth_confidence"] = auth_result["confidence"]
            
            # Alerte anomalies comportementales
            if auth_result["anomalies"] and self.message_bus:
                await self.message_bus.publish(
                    create_envelope(
                        message_type=MessageType.ALERT,
                        payload={
                            "type": "behavioral_anomaly",
                            "client_id": auth_result["client_id"],
                            "anomalies": auth_result["anomalies"],
                            "timestamp": datetime.now().isoformat()
                        },
                        priority=Priority.HIGH
                    )
                )
        
        # Stockage route dans request
        request["matched_route"] = route
        
        return await handler(request)
    
    @web.middleware
    async def _rate_limiting_middleware(self, request: web.Request, handler):
        """Middleware rate limiting adaptatif"""
        route = request.get("matched_route")
        client_id = request.get("client_id", "anonymous")
        
        if route and route.rate_limit:
            rate_check = await self.rate_limiter.check_rate_limit(
                client_id, route.path, route.rate_limit
            )
            
            if not rate_check["allowed"]:
                self.gateway_metrics["rate_limited_requests"] += 1
                return web.json_response(
                    {
                        "error": "Rate limit exceeded",
                        "retry_after": rate_check["reset_time"] - time.time()
                    },
                    status=429,
                    headers={
                        "X-RateLimit-Limit": str(rate_check["current_limit"]),
                        "X-RateLimit-Remaining": str(rate_check["remaining"]),
                        "X-RateLimit-Reset": str(int(rate_check["reset_time"]))
                    }
                )
        
        return await handler(request)
    
    @web.middleware
    async def _metrics_middleware(self, request: web.Request, handler):
        """Middleware métriques et monitoring"""
        start_time = time.time()
        self.gateway_metrics["active_connections"] += 1
        
        try:
            response = await handler(request)
            
            # Métriques succès
            response_time = (time.time() - start_time) * 1000
            self.gateway_metrics["requests_total"] += 1
            
            if response.status < 400:
                self.gateway_metrics["requests_successful"] += 1
            else:
                self.gateway_metrics["requests_failed"] += 1
            
            # Mise à jour temps réponse moyen
            self._update_average_response_time(response_time)
            
            # Stockage historique
            route = request.get("matched_route")
            if route:
                metrics = RequestMetrics(
                    timestamp=datetime.now(),
                    client_id=request.get("client_id", "anonymous"),
                    route=route.path,
                    method=request.method,
                    status_code=response.status,
                    response_time_ms=response_time,
                    backend_response_time_ms=response_time,  # Simplifié
                    request_size_bytes=len(await request.read() or b""),
                    response_size_bytes=len(response.body or b"")
                )
                
                self.request_history.append(metrics)
                
                # Limite historique
                if len(self.request_history) > self.max_history_size:
                    self.request_history = self.request_history[-self.max_history_size//2:]
            
            return response
            
        finally:
            self.gateway_metrics["active_connections"] -= 1
    
    async def _handle_request(self, request: web.Request) -> web.Response:
        """Handler principal requêtes"""
        route = request.get("matched_route")
        
        if not route:
            return web.json_response({"error": "Route not configured"}, status=404)
        
        # Routes internes
        if route.backend_url.startswith("internal://"):
            return await self._handle_internal_route(request, route)
        
        # Proxy vers backend
        return await self._proxy_to_backend(request, route)
    
    async def _handle_internal_route(self, request: web.Request, 
                                   route: APIRoute) -> web.Response:
        """Gestion routes internes"""
        if route.backend_url == "internal://health":
            health = await self.health_check()
            return web.json_response(health)
        
        elif route.backend_url == "internal://metrics":
            metrics = await self.get_gateway_metrics()
            return web.json_response(metrics)
        
        else:
            return web.json_response({"error": "Internal route not found"}, status=404)
    
    async def _proxy_to_backend(self, request: web.Request, 
                              route: APIRoute) -> web.Response:
        """Proxy vers backend avec circuit breaker"""
        async def make_request():
            async with ClientSession(timeout=aiohttp.ClientTimeout(total=route.timeout_seconds)) as session:
                async with session.request(
                    method=request.method,
                    url=route.backend_url + request.path_qs,
                    headers=request.headers,
                    data=await request.read()
                ) as resp:
                    body = await resp.read()
                    return {
                        "status": resp.status,
                        "headers": dict(resp.headers),
                        "body": body
                    }
        
        # Appel avec circuit breaker
        result = await self.circuit_breaker.call_backend(route.backend_url, make_request)
        
        if result["success"]:
            backend_response = result["result"]
            return web.Response(
                body=backend_response["body"],
                status=backend_response["status"],
                headers=backend_response["headers"]
            )
        else:
            return web.json_response(
                {"error": result["error"]},
                status=result["status_code"]
            )
    
    def _find_matching_route(self, path: str, method: str) -> Optional[APIRoute]:
        """Recherche route correspondante"""
        # Correspondance exacte
        exact_match = f"{method}:{path}"
        if exact_match in self.routes:
            return self.routes[exact_match]
        
        # Correspondance par path seulement
        for route_key, route in self.routes.items():
            if route.path == path and (route.method == "*" or route.method == method):
                return route
        
        return None
    
    def _update_average_response_time(self, response_time_ms: float):
        """Mise à jour temps réponse moyen"""
        count = self.gateway_metrics["requests_total"]
        avg = self.gateway_metrics["average_response_time_ms"]
        
        self.gateway_metrics["average_response_time_ms"] = (
            (avg * (count - 1) + response_time_ms) / count
        )
    
    def add_route(self, route: APIRoute):
        """Ajout route gateway"""
        route_key = f"{route.method}:{route.path}"
        self.routes[route_key] = route
        self.logger.info(f"🌐 Route ajoutée: {route_key} -> {route.backend_url}")
    
    def add_client(self, client: APIClient):
        """Ajout client API"""
        self.clients[client.client_id] = client
        self.logger.info(f"🔑 Client ajouté: {client.client_id}")
    
    async def get_gateway_metrics(self) -> Dict[str, Any]:
        """Métriques gateway détaillées"""
        return {
            "gateway_metrics": self.gateway_metrics,
            "routes_count": len(self.routes),
            "clients_count": len(self.clients),
            "circuit_breaker_states": {
                url: circuit["state"] 
                for url, circuit in self.circuit_breaker.circuits.items()
            },
            "patterns": self.__nextgen_patterns__,
            "version": self.version,
            "timestamp": datetime.now().isoformat()
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check NextGeneration"""
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "status": "healthy",
            "patterns": self.__nextgen_patterns__,
            "services": {
                "llm_gateway": self.llm_gateway is not None,
                "message_bus": self.message_bus is not None,
                "context_store": self.context_store is not None
            },
            "gateway": {
                "running": self.site is not None,
                "host": self.host,
                "port": self.port,
                "routes": len(self.routes),
                "active_connections": self.gateway_metrics["active_connections"],
                "requests_total": self.gateway_metrics["requests_total"]
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function pour compatibilité
def create_api_gateway(**config) -> AgentAPIGateway_Enterprise:
    """Factory function pour créer l'agent"""
    return AgentAPIGateway_Enterprise(**config)

# Test standalone
async def main():
    """Test de l'agent API Gateway"""
    print("🌐 Test Agent API Gateway NextGeneration v5.3.0")
    
    agent = create_api_gateway(agent_id="test_gateway", port=8888)
    
    # Health check
    health = await agent.health_check()
    print(f"🏥 Health: {health['status']}")
    
    # Ajout routes exemple
    agent.add_route(APIRoute(
        path="/api/users",
        method="GET",
        backend_url="http://localhost:3000/users",
        rate_limit=1000
    ))
    
    agent.add_route(APIRoute(
        path="/api/orders",
        method="POST",
        backend_url="http://localhost:3001/orders",
        auth_methods=[AuthMethod.JWT],
        rate_limit=500
    ))
    
    # Démarrage serveur
    await agent.start_server()
    print(f"🌐 Gateway démarré sur http://{agent.host}:{agent.port}")
    
    # Attente (en production, garder en vie)
    await asyncio.sleep(1)
    
    # Métriques
    metrics = await agent.get_gateway_metrics()
    print(f"📊 Routes: {metrics['routes_count']}")
    
    # Arrêt pour test
    await agent.stop_server()

if __name__ == "__main__":
    asyncio.run(main())