"""
Système de logs structurés avec audit trail et contexte de sécurité.
Implémentation de l'observabilité complète selon les spécifications.
"""

import structlog
import uuid
import json
import hashlib
import time
from datetime import datetime, timezone
from contextvars import ContextVar
from typing import Dict, Any, Optional, List
from enum import Enum
import logging
import traceback
import os

# Variables de contexte pour tracing distribué
correlation_id: ContextVar[str] = ContextVar('correlation_id')
user_session: ContextVar[str] = ContextVar('user_session', default="anonymous")
request_id: ContextVar[str] = ContextVar('request_id')
security_context: ContextVar[Dict] = ContextVar('security_context', default={})


class LogLevel(Enum):
    """Niveaux de log standardisés."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class SecurityEventType(Enum):
    """Types d'événements de sécurité pour audit."""
    CODE_INJECTION_ATTEMPT = "code_injection_attempt"
    SSRF_ATTEMPT = "ssrf_attempt"
    AUTHENTICATION_SUCCESS = "authentication_success"
    AUTHENTICATION_FAILURE = "authentication_failure"
    AUTHORIZATION_FAILURE = "authorization_failure"
    INPUT_VALIDATION_FAILURE = "input_validation_failure"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    SECURITY_SCAN_COMPLETED = "security_scan_completed"
    VULNERABILITY_DETECTED = "vulnerability_detected"
    SECRET_ACCESS = "secret_access"
    SECURITY_POLICY_VIOLATION = "security_policy_violation"


class PerformanceMetrics:
    """Métriques de performance pour observabilité."""
    
    def __init__(self):
        self.start_time = time.time()
        self.checkpoints = {}
    
    def checkpoint(self, name: str) -> None:
        """Ajoute un checkpoint de performance."""
        self.checkpoints[name] = time.time() - self.start_time
    
    def get_duration_ms(self) -> float:
        """Retourne la durée totale en millisecondes."""
        return (time.time() - self.start_time) * 1000
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit les métriques en dictionnaire."""
        return {
            'total_duration_ms': self.get_duration_ms(),
            'checkpoints': {k: v * 1000 for k, v in self.checkpoints.items()}
        }


class SecurityAuditLogger:
    """Logger spécialisé pour les événements de sécurité avec conformité audit."""
    
    def __init__(self):
        self.security_logger = structlog.get_logger("security_audit")
        self.compliance_logger = structlog.get_logger("compliance")
        
    def log_security_event(
        self, 
        event_type: SecurityEventType, 
        details: Dict[str, Any], 
        severity: LogLevel = LogLevel.INFO,
        user_id: Optional[str] = None,
        source_ip: Optional[str] = None
    ) -> None:
        """
        Log un événement de sécurité avec contexte complet.
        
        Args:
            event_type: Type d'événement sécurité
            details: Détails spécifiques à l'événement
            severity: Niveau de gravité
            user_id: Identifiant utilisateur (optionnel)
            source_ip: IP source (optionnel)
        """
        event_data = {
            'event_type': event_type.value,
            'severity': severity.value,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'correlation_id': self._get_correlation_id(),
            'user_session': user_session.get("anonymous"),
            'request_id': self._get_request_id(),
            'user_id': user_id,
            'source_ip': source_ip,
            'service': 'orchestrator',
            'version': self._get_service_version(),
            'environment': os.getenv('ENVIRONMENT', 'development'),
            **details
        }
        
        # Hash sensible pour audit trail
        event_data['event_hash'] = self._compute_event_hash(event_data)
        
        self.security_logger.info("security_event", **event_data)
        
        # Log compliance pour événements critiques
        if severity in [LogLevel.ERROR, LogLevel.CRITICAL]:
            self._log_compliance_event(event_data)
    
    def log_code_analysis_request(
        self, 
        code_hash: str, 
        user_id: str, 
        risk_level: str,
        analysis_result: str
    ) -> None:
        """Log spécialisé pour les demandes d'analyse de code."""
        self.log_security_event(
            SecurityEventType.SECURITY_SCAN_COMPLETED,
            {
                'code_hash': code_hash,
                'risk_level': risk_level,
                'analysis_success': 'error' not in analysis_result.lower(),
                'code_size_category': self._categorize_code_size(len(code_hash) * 8)  # Estimation
            },
            severity=LogLevel.INFO,
            user_id=user_id
        )
    
    def log_authentication_attempt(
        self, 
        user_id: str, 
        success: bool, 
        source_ip: str,
        method: str = "api_key"
    ) -> None:
        """Log tentative d'authentification."""
        event_type = (SecurityEventType.AUTHENTICATION_SUCCESS 
                     if success else SecurityEventType.AUTHENTICATION_FAILURE)
        severity = LogLevel.INFO if success else LogLevel.WARNING
        
        self.log_security_event(
            event_type,
            {
                'authentication_method': method,
                'success': success,
                'failure_reason': None if success else 'invalid_credentials'
            },
            severity=severity,
            user_id=user_id,
            source_ip=source_ip
        )
    
    def log_vulnerability_detection(
        self, 
        vulnerability_type: str, 
        details: Dict[str, Any],
        severity: LogLevel = LogLevel.CRITICAL
    ) -> None:
        """Log détection de vulnérabilité."""
        self.log_security_event(
            SecurityEventType.VULNERABILITY_DETECTED,
            {
                'vulnerability_type': vulnerability_type,
                'detection_method': 'static_analysis',
                'mitigation_applied': True,
                **details
            },
            severity=severity
        )
    
    def _get_correlation_id(self) -> str:
        """Récupère ou génère un ID de corrélation."""
        try:
            return correlation_id.get()
        except LookupError:
            new_id = str(uuid.uuid4())
            correlation_id.set(new_id)
            return new_id
    
    def _get_request_id(self) -> str:
        """Récupère ou génère un ID de requête."""
        try:
            return request_id.get()
        except LookupError:
            new_id = str(uuid.uuid4())
            request_id.set(new_id)
            return new_id
    
    def _get_service_version(self) -> str:
        """Récupère la version du service."""
        return os.getenv('SERVICE_VERSION', 'v9.0')
    
    def _compute_event_hash(self, event_data: Dict[str, Any]) -> str:
        """Calcule un hash de l'événement pour intégrité."""
        # Exclude timestamp and hash itself for consistent hashing
        hashable_data = {k: v for k, v in event_data.items() 
                        if k not in ['timestamp', 'event_hash']}
        data_string = json.dumps(hashable_data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()[:16]
    
    def _categorize_code_size(self, size: int) -> str:
        """Catégorise la taille du code pour analyse."""
        if size < 1000:
            return 'small'
        elif size < 5000:
            return 'medium'
        elif size < 10000:
            return 'large'
        else:
            return 'very_large'
    
    def _log_compliance_event(self, event_data: Dict[str, Any]) -> None:
        """Log événement pour conformité réglementaire."""
        compliance_data = {
            'compliance_framework': 'SOC2_TYPE2',
            'data_classification': 'internal',
            'retention_period_days': 2555,  # 7 ans
            'event_category': 'security_incident',
            **event_data
        }
        self.compliance_logger.critical("compliance_event", **compliance_data)


class StructuredLogger:
    """Logger structuré principal avec contexte automatique."""
    
    def __init__(self, name: str):
        self.logger = structlog.get_logger(name)
        self.name = name
        self.metrics = PerformanceMetrics()
    
    def info(self, message: str, **kwargs) -> None:
        """Log niveau INFO avec contexte."""
        self._log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log niveau WARNING avec contexte."""
        self._log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, error: Optional[Exception] = None, **kwargs) -> None:
        """Log niveau ERROR avec contexte et stack trace."""
        error_data = kwargs.copy()
        if error:
            error_data.update({
                'error_type': type(error).__name__,
                'error_message': str(error),
                'stack_trace': traceback.format_exc() if hasattr(error, '__traceback__') else None
            })
        self._log(LogLevel.ERROR, message, **error_data)
    
    def critical(self, message: str, error: Optional[Exception] = None, **kwargs) -> None:
        """Log niveau CRITICAL avec contexte complet."""
        self.error(message, error, **kwargs)
        self.logger.critical(message, **kwargs)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log niveau DEBUG (développement uniquement)."""
        if os.getenv('DEBUG', 'false').lower() == 'true':
            self._log(LogLevel.DEBUG, message, **kwargs)
    
    def start_operation(self, operation_name: str, **context) -> str:
        """Démarre une opération trackée."""
        operation_id = str(uuid.uuid4())
        self.metrics.checkpoint(f"{operation_name}_start")
        
        self.info(f"{operation_name}_started", 
                 operation_id=operation_id, 
                 operation_name=operation_name,
                 **context)
        return operation_id
    
    def end_operation(self, operation_name: str, operation_id: str, success: bool = True, **context) -> None:
        """Termine une opération trackée."""
        self.metrics.checkpoint(f"{operation_name}_end")
        duration_ms = self.metrics.get_duration_ms()
        
        log_level = LogLevel.INFO if success else LogLevel.WARNING
        self._log(log_level, f"{operation_name}_completed",
                 operation_id=operation_id,
                 operation_name=operation_name,
                 success=success,
                 duration_ms=duration_ms,
                 **context)
    
    def _log(self, level: LogLevel, message: str, **kwargs) -> None:
        """Log interne avec contexte automatique."""
        log_data = {
            'service': 'orchestrator',
            'logger_name': self.name,
            'correlation_id': self._safe_get_context_var(correlation_id),
            'user_session': self._safe_get_context_var(user_session),
            'request_id': self._safe_get_context_var(request_id),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'environment': os.getenv('ENVIRONMENT', 'development'),
            **kwargs
        }
        
        log_method = getattr(self.logger, level.value.lower())
        log_method(message, **log_data)
    
    def _safe_get_context_var(self, var: ContextVar, default: Any = None) -> Any:
        """Récupère une variable de contexte de manière sûre."""
        try:
            return var.get()
        except LookupError:
            return default


def configure_structured_logging(
    environment: str = "development",
    log_level: str = "INFO"
) -> None:
    """
    Configure le système de logs structurés.
    
    Args:
        environment: Environnement (development, staging, production)
        log_level: Niveau de log minimum
    """
    
    def add_correlation_context(logger, method_name, event_dict):
        """Ajoute le contexte de corrélation automatiquement."""
        try:
            event_dict['correlation_id'] = correlation_id.get()
        except LookupError:
            event_dict['correlation_id'] = str(uuid.uuid4())
        
        try:
            event_dict['user_session'] = user_session.get()
        except LookupError:
            event_dict['user_session'] = "anonymous"
        
        try:
            event_dict['request_id'] = request_id.get()
        except LookupError:
            event_dict['request_id'] = str(uuid.uuid4())
        
        return event_dict
    
    def add_security_context(logger, method_name, event_dict):
        """Ajoute le contexte de sécurité."""
        event_dict['service'] = "orchestrator"
        event_dict['version'] = os.getenv('SERVICE_VERSION', 'v9')
        event_dict['environment'] = environment
        event_dict['log_level'] = method_name.upper()
        return event_dict
    
    def add_performance_context(logger, method_name, event_dict):
        """Ajoute les métriques de performance."""
        if 'duration_ms' not in event_dict:
            # Ajouter timestamp haute précision pour mesurer latence
            event_dict['log_timestamp_ns'] = time.time_ns()
        return event_dict
    
    # Configuration processors selon l'environnement
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        add_correlation_context,
        add_security_context,
        add_performance_context,
        structlog.processors.TimeStamper(fmt="iso"),
    ]
    
    # Format JSON en production, readable en dev
    if environment == "production":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=True,
    )
    
    # Configuration du niveau de log global
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))


# Instances globales
security_audit_logger = SecurityAuditLogger()


def get_logger(name: str) -> StructuredLogger:
    """
    Factory pour créer des loggers structurés.
    
    Args:
        name: Nom du logger (généralement __name__)
        
    Returns:
        StructuredLogger: Instance de logger configuré
    """
    return StructuredLogger(name)


def set_correlation_context(corr_id: str, session_id: str = "anonymous", req_id: Optional[str] = None) -> None:
    """
    Définit le contexte de corrélation pour la requête courante.
    
    Args:
        corr_id: ID de corrélation
        session_id: ID de session utilisateur
        req_id: ID de requête (généré automatiquement si None)
    """
    correlation_id.set(corr_id)
    user_session.set(session_id)
    request_id.set(req_id or str(uuid.uuid4()))


def get_correlation_context() -> Dict[str, str]:
    """
    Récupère le contexte de corrélation actuel.
    
    Returns:
        Dict: Contexte de corrélation
    """
    return {
        'correlation_id': correlation_id.get("unknown"),
        'user_session': user_session.get("anonymous"),
        'request_id': request_id.get("unknown")
    }


# Configuration automatique au démarrage
configure_structured_logging()
