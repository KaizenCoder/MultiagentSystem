"""
Systme de logging scuris pour l'orchestrateur.

Ce module contient les utilitaires pour :
- Logging scuris sans exposition d'informations sensibles
- Audit logging pour les vnements de scurit
- Masquage automatique des donnes sensibles
"""

import logging
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any, Optional
from orchestrator.app.config import settings


class AuditEventType(Enum):
    """Types d'vnements d'audit."""
    TASK_CREATED = "task_created"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    API_ACCESS = "api_access"
    API_ACCESS_DENIED = "api_access_denied"
    ERROR_OCCURRED = "error_occurred"
    SECURITY_VIOLATION = "security_violation"
    CODE_VALIDATION_FAILED = "code_validation_failed"
    NETWORK_VALIDATION_FAILED = "network_validation_failed"
    CODE_ANALYSIS_REQUEST = "code_analysis_request"
    TOOL_EXECUTION = "tool_execution"


class SecurityLogger:
    """Logger scuris qui masque les informations sensibles."""
    
    def __init__(self):
        self.logger = logging.getLogger("security")
    
    @staticmethod
    def _mask_sensitive_data(message: str) -> str:
        """
        Masque les donnes sensibles dans les messages de log.
        
        Args:
            message: Message  nettoyer
            
        Returns:
            str: Message avec donnes sensibles masques
        """
        import re
        
        # Masquer les cls API
        message = re.sub(r'(api[_-]?key["\s]*[:=]["\s]*)([a-zA-Z0-9-_]{20,})', r'\1***MASKED***', message, flags=re.IGNORECASE)
        
        # Masquer les tokens
        message = re.sub(r'(token["\s]*[:=]["\s]*)([a-zA-Z0-9-_.]{20,})', r'\1***MASKED***', message, flags=re.IGNORECASE)
        
        # Masquer les mots de passe
        message = re.sub(r'(password["\s]*[:=]["\s]*)([^\s"]{8,})', r'\1***MASKED***', message, flags=re.IGNORECASE)
        
        # Masquer les IPs prives dans les messages d'erreur
        message = re.sub(r'\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.1[6-9]\.\d{1,3}\.\d{1,3}|172\.2[0-9]\.\d{1,3}\.\d{1,3}|172\.3[0-1]\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})\b', '***PRIVATE_IP***', message)
        
        return message
    
    def log_error(self, message: str, error: Exception, include_details: bool = False) -> None:
        """
        Log une erreur de manire scurise.
        
        Args:
            message: Message de base
            error: Exception  logger
            include_details: Inclure les dtails complets (seulement en mode debug)
        """
        # Masquer les donnes sensibles
        safe_message = self._mask_sensitive_data(message)
        
        if include_details and hasattr(settings, 'DEBUG') and settings.DEBUG:
            safe_error = self._mask_sensitive_data(str(error))
            self.logger.error(f"{safe_message}: {safe_error}", exc_info=True)
        else:
            self.logger.error(f"{safe_message}: Generic error occurred")
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """
        Log un vnement de scurit.
        
        Args:
            event_type: Type d'vnement
            details: Dtails de l'vnement
        """
        # Nettoyer les dtails
        safe_details = {}
        for key, value in details.items():
            if isinstance(value, str):
                safe_details[key] = self._mask_sensitive_data(value)
            else:
                safe_details[key] = value
        
        self.logger.warning(f"SECURITY_EVENT: {event_type}", extra=safe_details)
    
    def log_access(self, endpoint: str, user_info: Dict[str, Any], success: bool) -> None:
        """
        Log un accs API.
        
        Args:
            endpoint: Endpoint accd
            user_info: Informations utilisateur (sanitises)
            success: Succs de l'accs
        """
        status = "SUCCESS" if success else "DENIED"
        safe_user_info = {k: self._mask_sensitive_data(str(v)) for k, v in user_info.items()}
        
        self.logger.info(f"API_ACCESS: {endpoint} - {status}", extra=safe_user_info)


class AuditLogger:
    """Logger d'audit pour les vnements systme."""
    
    def __init__(self):
        self.logger = logging.getLogger("audit")
    
    @staticmethod
    def log_event(event_type: AuditEventType, user_id: Optional[str], details: Dict[str, Any]) -> None:
        """
        Log un vnement d'audit.
        
        Args:
            event_type: Type d'vnement d'audit
            user_id: ID utilisateur (peut tre None pour les vnements systme)
            details: Dtails de l'vnement
        """
        audit_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type.value,
            "user_id": user_id or "system",
            "details": details
        }
        
        # Log vers le systme d'audit
        logger = logging.getLogger("audit")
        logger.info("AUDIT_EVENT", extra=audit_entry)
    
    @staticmethod
    def log_task_event(event_type: AuditEventType, session_id: str, details: Dict[str, Any]) -> None:
        """
        Log un vnement li  une tche.
        
        Args:
            event_type: Type d'vnement
            session_id: ID de session
            details: Dtails de l'vnement
        """
        task_details = {
            "session_id": session_id,
            **details
        }
        AuditLogger.log_event(event_type, None, task_details)
    
    @staticmethod
    def log_security_violation(violation_type: str, source_ip: str, details: Dict[str, Any]) -> None:
        """
        Log une violation de scurit.
        
        Args:
            violation_type: Type de violation
            source_ip: IP source
            details: Dtails de la violation
        """
        security_details = {
            "violation_type": violation_type,
            "source_ip": source_ip,
            **details
        }
        AuditLogger.log_event(AuditEventType.SECURITY_VIOLATION, None, security_details)


# Instance globale pour utilisation facile
security_logger = SecurityLogger()
audit_logger = AuditLogger()


def setup_secure_logging():
    """Configure le logging scuris."""
    
    # Configuration du logger scurit
    security_handler = logging.StreamHandler()
    security_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
        )
    )
    
    security_log = logging.getLogger("security")
    security_log.addHandler(security_handler)
    security_log.setLevel(logging.INFO)
    
    # Configuration du logger audit
    audit_handler = logging.StreamHandler()
    audit_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - AUDIT - %(levelname)s - %(message)s'
        )
    )
    
    audit_log = logging.getLogger("audit")
    audit_log.addHandler(audit_handler)
    audit_log.setLevel(logging.INFO)
    
    # Empcher la propagation vers le logger root
    security_log.propagate = False
    audit_log.propagate = False 