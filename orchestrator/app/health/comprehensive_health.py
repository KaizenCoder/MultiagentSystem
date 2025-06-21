"""
Systme de health checks complets pour monitoring proactif.
Surveille tous les composants critiques avec mtriques dtailles.
"""

import asyncio
import time
import psutil
import httpx
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from logging_manager_optimized import LoggingManager
from abc import ABC, abstractmethod

# LoggingManager NextGeneration - Tool/Utility
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={
            "logger_name": "HealthStatus",
            "log_level": "INFO",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": True
        })


class HealthStatus(Enum):
    """tats de sant possibles."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class ComponentType(Enum):
    """Types de composants surveills."""
    DATABASE = "database"
    HTTP_SERVICE = "http_service"
    LLM_API = "llm_api"
    FILE_SYSTEM = "file_system"
    SYSTEM_RESOURCE = "system_resource"
    CACHE = "cache"
    SECURITY = "security"


@dataclass
class HealthCheckResult:
    """Rsultat d'un health check."""
    component_name: str
    component_type: ComponentType
    status: HealthStatus
    message: str
    response_time_ms: float
    timestamp: datetime
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire."""
        result = asdict(self)
        result['status'] = self.status.value
        result['component_type'] = self.component_type.value
        result['timestamp'] = self.timestamp.isoformat()
        return result


@dataclass
class HealthReport:
    """Rapport de sant global."""
    overall_status: HealthStatus
    individual_checks: Dict[str, HealthCheckResult]
    timestamp: datetime
    total_response_time_ms: float
    healthy_components: int
    degraded_components: int
    unhealthy_components: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire."""
        return {
            'overall_status': self.overall_status.value,
            'individual_checks': {k: v.to_dict() for k, v in self.individual_checks.items()},
            'timestamp': self.timestamp.isoformat(),
            'total_response_time_ms': self.total_response_time_ms,
            'summary': {
                'healthy_components': self.healthy_components,
                'degraded_components': self.degraded_components,
                'unhealthy_components': self.unhealthy_components,
                'total_components': len(self.individual_checks)
            }
        }


class HealthCheck(ABC):
    """Interface abstraite pour les health checks."""
    
    def __init__(self, name: str, component_type: ComponentType):
        self.name = name
        self.component_type = component_type
    
    @abstractmethod
    async def check(self) -> HealthCheckResult:
        """Excute le health check."""
        pass


class ServiceHealthCheck(HealthCheck):
    """Health check pour services HTTP."""
    
    def __init__(
        self, 
        name: str, 
        url: str, 
        timeout: float = 5.0,
        expected_status: int = 200,
        health_endpoint: str = "/health"
    ):
        super().__init__(name, ComponentType.HTTP_SERVICE)
        self.url = url.rstrip('/')
        self.health_endpoint = health_endpoint
        self.timeout = timeout
        self.expected_status = expected_status
    
    async def check(self) -> HealthCheckResult:
        """Vrifie la sant du service HTTP."""
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.url}{self.health_endpoint}")
                
            response_time_ms = (time.time() - start_time) * 1000
            
            if response.status_code == self.expected_status:
                status = HealthStatus.HEALTHY
                message = f"Service responding normally (HTTP {response.status_code})"
            else:
                status = HealthStatus.DEGRADED
                message = f"Unexpected status code: {response.status_code}"
            
            # Tentative de parsing JSON pour mtadonnes
            try:
                response_data = response.json()
                metadata = {
                    'response_data': response_data,
                    'content_type': response.headers.get('content-type', 'unknown')
                }
            except:
                metadata = {
                    'response_size': len(response.content),
                    'content_type': response.headers.get('content-type', 'unknown')
                }
            
            metadata.update({
                'status_code': response.status_code,
                'url': self.url + self.health_endpoint
            })
            
        except asyncio.TimeoutError:
            response_time_ms = self.timeout * 1000
            status = HealthStatus.UNHEALTHY
            message = f"Request timeout after {self.timeout}s"
            metadata = {'error': 'timeout', 'timeout_seconds': self.timeout}
            
        except httpx.ConnectError:
            response_time_ms = (time.time() - start_time) * 1000
            status = HealthStatus.UNHEALTHY
            message = "Connection failed - service unreachable"
            metadata = {'error': 'connection_failed'}
            
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            status = HealthStatus.UNHEALTHY
            message = f"Health check failed: {str(e)}"
            metadata = {'error': type(e).__name__, 'error_message': str(e)}
        
        return HealthCheckResult(
            component_name=self.name,
            component_type=self.component_type,
            status=status,
            message=message,
            response_time_ms=response_time_ms,
            timestamp=datetime.now(timezone.utc),
            metadata=metadata
        )


class LLMHealthCheck(HealthCheck):
    """Health check spcialis pour APIs LLM."""
    
    def __init__(
        self, 
        name: str, 
        provider: str,  # 'openai', 'anthropic', etc.
        api_key: Optional[str] = None,
        timeout: float = 10.0
    ):
        super().__init__(name, ComponentType.LLM_API)
        self.provider = provider
        self.api_key = api_key
        self.timeout = timeout
    
    async def check(self) -> HealthCheckResult:
        """Vrifie la sant de l'API LLM."""
        start_time = time.time()
        
        try:
            if self.provider == 'openai':
                success, message, metadata = await self._check_openai()
            elif self.provider == 'anthropic':
                success, message, metadata = await self._check_anthropic()
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
            
            response_time_ms = (time.time() - start_time) * 1000
            status = HealthStatus.HEALTHY if success else HealthStatus.DEGRADED
            
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            status = HealthStatus.UNHEALTHY
            message = f"LLM API check failed: {str(e)}"
            metadata = {'error': type(e).__name__, 'provider': self.provider}
        
        return HealthCheckResult(
            component_name=self.name,
            component_type=self.component_type,
            status=status,
            message=message,
            response_time_ms=response_time_ms,
            timestamp=datetime.now(timezone.utc),
            metadata=metadata
        )
    
    async def _check_openai(self) -> tuple[bool, str, Dict[str, Any]]:
        """Vrifie l'API OpenAI."""
        headers = {'Authorization': f'Bearer {self.api_key}'} if self.api_key else {}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Test de l'endpoint models
            response = await client.get(
                'https://api.openai.com/v1/models',
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                model_count = len(data.get('data', []))
                return True, f"OpenAI API healthy ({model_count} models available)", {
                    'provider': 'openai',
                    'model_count': model_count,
                    'status_code': 200
                }
            elif response.status_code == 401:
                return False, "OpenAI API authentication failed", {
                    'provider': 'openai',
                    'status_code': 401,
                    'error': 'authentication_failed'
                }
            else:
                return False, f"OpenAI API returned {response.status_code}", {
                    'provider': 'openai',
                    'status_code': response.status_code
                }
    
    async def _check_anthropic(self) -> tuple[bool, str, Dict[str, Any]]:
        """Vrifie l'API Anthropic."""
        headers = {
            'x-api-key': self.api_key,
            'content-type': 'application/json',
            'anthropic-version': '2023-06-01'
        } if self.api_key else {}
        
        # Test minimal avec messages API
        test_payload = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 10,
            "messages": [{"role": "user", "content": "Hello"}]
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=test_payload
            )
            
            if response.status_code == 200:
                return True, "Anthropic API healthy", {
                    'provider': 'anthropic',
                    'status_code': 200
                }
            elif response.status_code == 401:
                return False, "Anthropic API authentication failed", {
                    'provider': 'anthropic',
                    'status_code': 401,
                    'error': 'authentication_failed'
                }
            else:
                return False, f"Anthropic API returned {response.status_code}", {
                    'provider': 'anthropic',
                    'status_code': response.status_code
                }


class DiskHealthCheck(HealthCheck):
    """Health check pour l'espace disque."""
    
    def __init__(
        self, 
        name: str, 
        path: str = "/",
        warning_threshold_gb: float = 2.0,
        critical_threshold_gb: float = 1.0
    ):
        super().__init__(name, ComponentType.FILE_SYSTEM)
        self.path = path
        self.warning_threshold_gb = warning_threshold_gb
        self.critical_threshold_gb = critical_threshold_gb
    
    async def check(self) -> HealthCheckResult:
        """Vrifie l'espace disque disponible."""
        start_time = time.time()
        
        try:
            disk_usage = psutil.disk_usage(self.path)
            free_gb = disk_usage.free / (1024**3)
            total_gb = disk_usage.total / (1024**3)
            used_gb = disk_usage.used / (1024**3)
            used_percent = (disk_usage.used / disk_usage.total) * 100
            
            if free_gb >= self.warning_threshold_gb:
                status = HealthStatus.HEALTHY
                message = f"Sufficient disk space: {free_gb:.1f}GB free"
            elif free_gb >= self.critical_threshold_gb:
                status = HealthStatus.DEGRADED
                message = f"Low disk space warning: {free_gb:.1f}GB free"
            else:
                status = HealthStatus.UNHEALTHY
                message = f"Critical disk space: {free_gb:.1f}GB free"
            
            metadata = {
                'path': self.path,
                'free_gb': round(free_gb, 2),
                'total_gb': round(total_gb, 2),
                'used_gb': round(used_gb, 2),
                'used_percent': round(used_percent, 1),
                'warning_threshold_gb': self.warning_threshold_gb,
                'critical_threshold_gb': self.critical_threshold_gb
            }
            
        except Exception as e:
            status = HealthStatus.UNHEALTHY
            message = f"Disk check failed: {str(e)}"
            metadata = {'error': type(e).__name__, 'path': self.path}
        
        response_time_ms = (time.time() - start_time) * 1000
        
        return HealthCheckResult(
            component_name=self.name,
            component_type=self.component_type,
            status=status,
            message=message,
            response_time_ms=response_time_ms,
            timestamp=datetime.now(timezone.utc),
            metadata=metadata
        )


class MemoryHealthCheck(HealthCheck):
    """Health check pour l'utilisation mmoire."""
    
    def __init__(
        self, 
        name: str,
        warning_threshold_percent: float = 80.0,
        critical_threshold_percent: float = 90.0
    ):
        super().__init__(name, ComponentType.SYSTEM_RESOURCE)
        self.warning_threshold = warning_threshold_percent
        self.critical_threshold = critical_threshold_percent
    
    async def check(self) -> HealthCheckResult:
        """Vrifie l'utilisation mmoire."""
        start_time = time.time()
        
        try:
            memory = psutil.virtual_memory()
            used_percent = memory.percent
            available_gb = memory.available / (1024**3)
            total_gb = memory.total / (1024**3)
            
            if used_percent < self.warning_threshold:
                status = HealthStatus.HEALTHY
                message = f"Memory usage normal: {used_percent:.1f}%"
            elif used_percent < self.critical_threshold:
                status = HealthStatus.DEGRADED
                message = f"High memory usage: {used_percent:.1f}%"
            else:
                status = HealthStatus.UNHEALTHY
                message = f"Critical memory usage: {used_percent:.1f}%"
            
            metadata = {
                'used_percent': round(used_percent, 1),
                'available_gb': round(available_gb, 2),
                'total_gb': round(total_gb, 2),
                'warning_threshold': self.warning_threshold,
                'critical_threshold': self.critical_threshold
            }
            
        except Exception as e:
            status = HealthStatus.UNHEALTHY
            message = f"Memory check failed: {str(e)}"
            metadata = {'error': type(e).__name__}
        
        response_time_ms = (time.time() - start_time) * 1000
        
        return HealthCheckResult(
            component_name=self.name,
            component_type=self.component_type,
            status=status,
            message=message,
            response_time_ms=response_time_ms,
            timestamp=datetime.now(timezone.utc),
            metadata=metadata
        )


class SecurityHealthCheck(HealthCheck):
    """Health check pour les composants de scurit."""
    
    def __init__(self, name: str, security_components: List[str]):
        super().__init__(name, ComponentType.SECURITY)
        self.security_components = security_components
    
    async def check(self) -> HealthCheckResult:
        """Vrifie la sant des composants de scurit."""
        start_time = time.time()
        
        try:
            # Import conditionnel pour viter les dpendances circulaires
            from orchestrator.app.security.validators import CodeValidator, NetworkValidator
            from orchestrator.app.security.secure_analyzer import get_secure_analyzer
            
            security_status = {}
            
            # Test validateur de code
            try:
                is_valid, _ = CodeValidator.validate_python_code("print('test')")
                security_status['code_validator'] = 'healthy' if is_valid else 'degraded'
            except Exception as e:
                security_status['code_validator'] = f'unhealthy: {str(e)}'
            
            # Test validateur rseau
            try:
                is_valid, _ = NetworkValidator.validate_url("https://api.openai.com")
                security_status['network_validator'] = 'healthy' if is_valid else 'degraded'
            except Exception as e:
                security_status['network_validator'] = f'unhealthy: {str(e)}'
            
            # Test analyseur scuris
            try:
                analyzer = get_secure_analyzer()
                metrics = analyzer.get_security_metrics()
                security_status['secure_analyzer'] = 'healthy'
                security_status['analyzer_metrics'] = metrics
            except Exception as e:
                security_status['secure_analyzer'] = f'unhealthy: {str(e)}'
            
            # valuation globale
            unhealthy_count = sum(1 for status in security_status.values() 
                                if isinstance(status, str) and 'unhealthy' in status)
            degraded_count = sum(1 for status in security_status.values() 
                               if isinstance(status, str) and 'degraded' in status)
            
            if unhealthy_count > 0:
                status = HealthStatus.UNHEALTHY
                message = f"Security components unhealthy: {unhealthy_count}"
            elif degraded_count > 0:
                status = HealthStatus.DEGRADED
                message = f"Security components degraded: {degraded_count}"
            else:
                status = HealthStatus.HEALTHY
                message = "All security components healthy"
            
            metadata = {
                'security_components': security_status,
                'total_components': len(self.security_components),
                'unhealthy_count': unhealthy_count,
                'degraded_count': degraded_count
            }
            
        except Exception as e:
            status = HealthStatus.UNHEALTHY
            message = f"Security health check failed: {str(e)}"
            metadata = {'error': type(e).__name__}
        
        response_time_ms = (time.time() - start_time) * 1000
        
        return HealthCheckResult(
            component_name=self.name,
            component_type=self.component_type,
            status=status,
            message=message,
            response_time_ms=response_time_ms,
            timestamp=datetime.now(timezone.utc),
            metadata=metadata
        )


class HealthCheckOrchestrator:
    """Orchestrateur principal des health checks."""
    
    def __init__(self):
        self.checks: Dict[str, HealthCheck] = {}
        self.last_report: Optional[HealthReport] = None
        self.check_history: List[HealthReport] = []
        
        # Configuration par dfaut
        self._setup_default_checks()
    
    def _setup_default_checks(self) -> None:
        """Configure les health checks par dfaut."""
        # Service memory API
        self.add_check(ServiceHealthCheck(
            name="memory_api",
            url="http://memory_api:8001",
            health_endpoint="/health"
        ))
        
        # APIs LLM (si cls disponibles)
        try:
            from orchestrator.app.security.secrets_manager import get_openai_api_key
            api_key = get_openai_api_key()
            self.add_check(LLMHealthCheck(
                name="openai_api",
                provider="openai",
                api_key=api_key
            ))
        except Exception:
            logger.warning("OpenAI API key not available - skipping health check")
        
        try:
            from orchestrator.app.security.secrets_manager import get_anthropic_api_key
            api_key = get_anthropic_api_key()
            self.add_check(LLMHealthCheck(
                name="anthropic_api",
                provider="anthropic",
                api_key=api_key
            ))
        except Exception:
            logger.warning("Anthropic API key not available - skipping health check")
        
        # Ressources systme
        self.add_check(DiskHealthCheck(
            name="disk_space",
            path="/",
            warning_threshold_gb=2.0,
            critical_threshold_gb=1.0
        ))
        
        self.add_check(MemoryHealthCheck(
            name="memory_usage",
            warning_threshold_percent=80.0,
            critical_threshold_percent=90.0
        ))
        
        # Scurit
        self.add_check(SecurityHealthCheck(
            name="security_components",
            security_components=["code_validator", "network_validator", "secure_analyzer"]
        ))
    
    def add_check(self, health_check: HealthCheck) -> None:
        """Ajoute un health check."""
        self.checks[health_check.name] = health_check
        logger.info(f"Added health check: {health_check.name}")
    
    def remove_check(self, name: str) -> None:
        """Supprime un health check."""
        if name in self.checks:
            del self.checks[name]
            logger.info(f"Removed health check: {name}")
    
    async def check_all_systems(self) -> HealthReport:
        """Excute tous les health checks en parallle."""
        start_time = time.time()
        
        if not self.checks:
            logger.warning("No health checks configured")
            return HealthReport(
                overall_status=HealthStatus.UNKNOWN,
                individual_checks={},
                timestamp=datetime.now(timezone.utc),
                total_response_time_ms=0,
                healthy_components=0,
                degraded_components=0,
                unhealthy_components=0
            )
        
        # Excution parallle de tous les checks
        tasks = [check.check() for check in self.checks.values()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Traitement des rsultats
        individual_checks = {}
        healthy_count = 0
        degraded_count = 0
        unhealthy_count = 0
        
        for i, result in enumerate(results):
            check_name = list(self.checks.keys())[i]
            
            if isinstance(result, Exception):
                # Erreur lors de l'excution du check
                logger.error(f"Health check {check_name} failed with exception: {result}")
                result = HealthCheckResult(
                    component_name=check_name,
                    component_type=ComponentType.SYSTEM_RESOURCE,
                    status=HealthStatus.UNHEALTHY,
                    message=f"Check failed: {str(result)}",
                    response_time_ms=0,
                    timestamp=datetime.now(timezone.utc),
                    metadata={'error': type(result).__name__}
                )
            
            individual_checks[check_name] = result
            
            # Comptage par statut
            if result.status == HealthStatus.HEALTHY:
                healthy_count += 1
            elif result.status == HealthStatus.DEGRADED:
                degraded_count += 1
            else:
                unhealthy_count += 1
        
        # Dtermination du statut global
        if unhealthy_count > 0:
            overall_status = HealthStatus.UNHEALTHY
        elif degraded_count > 0:
            overall_status = HealthStatus.DEGRADED
        else:
            overall_status = HealthStatus.HEALTHY
        
        total_response_time_ms = (time.time() - start_time) * 1000
        
        report = HealthReport(
            overall_status=overall_status,
            individual_checks=individual_checks,
            timestamp=datetime.now(timezone.utc),
            total_response_time_ms=total_response_time_ms,
            healthy_components=healthy_count,
            degraded_components=degraded_count,
            unhealthy_components=unhealthy_count
        )
        
        # Sauvegarde du rapport
        self.last_report = report
        self.check_history.append(report)
        
        # Gardez seulement les 100 derniers rapports
        if len(self.check_history) > 100:
            self.check_history = self.check_history[-100:]
        
        logger.info(f"Health check completed: {overall_status.value} "
                   f"({healthy_count}H/{degraded_count}D/{unhealthy_count}U)")
        
        return report
    
    def get_last_report(self) -> Optional[HealthReport]:
        """Retourne le dernier rapport de sant."""
        return self.last_report
    
    def get_history(self, limit: int = 10) -> List[HealthReport]:
        """Retourne l'historique des rapports."""
        return self.check_history[-limit:]
    
    def get_component_status(self, component_name: str) -> Optional[HealthCheckResult]:
        """Retourne le statut d'un composant spcifique."""
        if self.last_report and component_name in self.last_report.individual_checks:
            return self.last_report.individual_checks[component_name]
        return None


# Instance globale
_health_orchestrator: Optional[HealthCheckOrchestrator] = None


def get_health_orchestrator() -> HealthCheckOrchestrator:
    """Retourne l'instance globale de l'orchestrateur de sant."""
    global _health_orchestrator
    if _health_orchestrator is None:
        _health_orchestrator = HealthCheckOrchestrator()
    return _health_orchestrator


# Fonctions de convnience
async def check_system_health() -> HealthReport:
    """Fonction de convnience pour vrifier la sant du systme."""
    orchestrator = get_health_orchestrator()
    return await orchestrator.check_all_systems()


def is_system_healthy() -> bool:
    """Vrifie rapidement si le systme est en bonne sant."""
    orchestrator = get_health_orchestrator()
    last_report = orchestrator.get_last_report()
    
    if last_report is None:
        return False
    
    return last_report.overall_status == HealthStatus.HEALTHY
