"""
Tests unitaires pour le module de logging scuris.

Ce fichier teste tous les composants du systme de logging scuris :
- SecurityLogger : masquage des donnes sensibles, logging d'erreurs et d'vnements
- AuditLogger : logging des vnements d'audit et violations de scurit
- AuditEventType : numration des types d'vnements
- Configuration du logging scuris
"""

import pytest
import logging
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from typing import Dict, Any

from orchestrator.app.security.logging import (
    SecurityLogger,
    AuditLogger,
    AuditEventType,
    security_logger,
    audit_logger,
    setup_secure_logging
)


class TestAuditEventType:
    """Tests pour l'numration AuditEventType."""
    
    def test_enum_values(self):
        """Test que tous les types d'vnements sont dfinis."""
        expected_values = {
            "TASK_CREATED": "task_created",
            "TASK_COMPLETED": "task_completed", 
            "TASK_FAILED": "task_failed",
            "API_ACCESS": "api_access",
            "API_ACCESS_DENIED": "api_access_denied",
            "ERROR_OCCURRED": "error_occurred",
            "SECURITY_VIOLATION": "security_violation",
            "CODE_VALIDATION_FAILED": "code_validation_failed",
            "NETWORK_VALIDATION_FAILED": "network_validation_failed"
        }
        
        for attr_name, expected_value in expected_values.items():
            assert hasattr(AuditEventType, attr_name)
            assert getattr(AuditEventType, attr_name).value == expected_value
    
    def test_enum_type(self):
        """Test que AuditEventType est bien une numration."""
        assert isinstance(AuditEventType.TASK_CREATED, AuditEventType)
        assert str(AuditEventType.TASK_CREATED) == "AuditEventType.TASK_CREATED"


class TestSecurityLogger:
    """Tests pour la classe SecurityLogger."""
    
    @pytest.fixture
    def security_logger_instance(self):
        """Fixture pour crer une instance de SecurityLogger."""
        return SecurityLogger()
    
    def test_init(self, security_logger_instance):
        """Test l'initialisation du SecurityLogger."""
        assert security_logger_instance.logger.name == "security"
        assert isinstance(security_logger_instance.logger, logging.Logger)
    
    @pytest.mark.parametrize("input_message,expected_mask", [
        # Test masquage des cls API
        ("API_KEY=sk-1234567890abcdef1234567890", "API_KEY=***MASKED***"),
        ("api-key: sk-1234567890abcdef1234567890", "api-key: ***MASKED***"),
        ("api_key=\"sk-1234567890abcdef1234567890\"", "api_key=\"***MASKED***"),
        
        # Test masquage des tokens
        ("token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "token=***MASKED***"),
        ("TOKEN: bearer_token_1234567890", "TOKEN: ***MASKED***"),
        
        # Test masquage des mots de passe
        ("password=motdepasse123", "password=***MASKED***"),
        ("PASSWORD: \"my_secret_password\"", "PASSWORD: \"***MASKED***"),
        
        # Test masquage des IPs prives
        ("Error connecting to 192.168.1.100", "Error connecting to ***PRIVATE_IP***"),
        ("Server at 10.0.0.1 is down", "Server at ***PRIVATE_IP*** is down"),
        ("Connection to 172.16.0.1 failed", "Connection to ***PRIVATE_IP*** failed"),
    ])
    def test_mask_sensitive_data(self, security_logger_instance, input_message, expected_mask):
        """Test le masquage des donnes sensibles."""
        result = security_logger_instance._mask_sensitive_data(input_message)
        assert expected_mask in result
    
    def test_mask_sensitive_data_no_match(self, security_logger_instance):
        """Test que les messages sans donnes sensibles restent inchangs."""
        message = "This is a normal log message without sensitive data"
        result = security_logger_instance._mask_sensitive_data(message)
        assert result == message
    
    def test_mask_sensitive_data_multiple_patterns(self, security_logger_instance):
        """Test le masquage de plusieurs patterns dans le mme message."""
        message = "API_KEY=sk-123456789012345678901234 password=secretpassword token=abcdefghijklmnopqrstuvwxyz123456789"
        result = security_logger_instance._mask_sensitive_data(message)
        
        assert "***MASKED***" in result
        assert "sk-123456789012345678901234" not in result
        assert "secretpassword" not in result
        assert "abcdefghijklmnopqrstuvwxyz123456789" not in result
    
    @patch('orchestrator.app.security.logging.logging.getLogger')
    def test_log_error_basic(self, mock_get_logger, security_logger_instance):
        """Test le logging d'erreur basique."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        security_logger_instance.logger = mock_logger
        
        error = Exception("Test error")
        security_logger_instance.log_error("Test message", error)
        
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args[0][0]
        assert "Test message" in call_args
        assert "Generic error occurred" in call_args
    
    @patch('orchestrator.app.security.logging.settings')
    @patch('orchestrator.app.security.logging.logging.getLogger')
    def test_log_error_with_details_debug_mode(self, mock_get_logger, mock_settings, security_logger_instance):
        """Test le logging d'erreur avec dtails en mode debug."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        security_logger_instance.logger = mock_logger
        mock_settings.DEBUG = True
        
        error = Exception("Detailed error message")
        security_logger_instance.log_error("Test message", error, include_details=True)
        
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args
        assert "Test message" in call_args[0][0]
        assert "Detailed error message" in call_args[0][0]
        assert call_args[1]['exc_info'] is True
    
    @patch('orchestrator.app.security.logging.settings')
    @patch('orchestrator.app.security.logging.logging.getLogger')
    def test_log_error_with_details_no_debug(self, mock_get_logger, mock_settings, security_logger_instance):
        """Test le logging d'erreur avec dtails sans mode debug."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        security_logger_instance.logger = mock_logger
        mock_settings.DEBUG = False
        
        error = Exception("Secret error details")
        security_logger_instance.log_error("Test message", error, include_details=True)
        
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args[0][0]
        assert "Test message" in call_args
        assert "Generic error occurred" in call_args
        assert "Secret error details" not in call_args
    
    @patch('orchestrator.app.security.logging.logging.getLogger')
    def test_log_error_with_sensitive_data(self, mock_get_logger, security_logger_instance):
        """Test le logging d'erreur avec masquage des donnes sensibles."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        security_logger_instance.logger = mock_logger
        
        error = Exception("API_KEY=sk-secret123456789123456789")
        security_logger_instance.log_error("Message with api_key=sk-test123456789123456789", error)
        
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args[0][0]
        assert "***MASKED***" in call_args
        assert "sk-secret123456789123456789" not in call_args
        assert "sk-test123456789123456789" not in call_args
    
    @patch('orchestrator.app.security.logging.logging.getLogger')
    def test_log_security_event(self, mock_get_logger, security_logger_instance):
        """Test le logging d'vnement de scurit."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        security_logger_instance.logger = mock_logger
        
        details = {
            "user_id": "user123",
            "action": "login_attempt",
            "details": "password=secretpassword123 api_key=sk-123456789012345678901234",
            "ip": "192.168.1.1"
        }
        
        security_logger_instance.log_security_event("AUTHENTICATION_FAILED", details)
        
        mock_logger.warning.assert_called_once()
        call_args = mock_logger.warning.call_args
        assert "SECURITY_EVENT: AUTHENTICATION_FAILED" in call_args[0][0]
        
        # Vrifier que les donnes sensibles sont masques dans extra
        extra_data = call_args[1]['extra']
        assert extra_data['user_id'] == "user123"
        assert extra_data['action'] == "login_attempt"
        assert "***MASKED***" in str(extra_data['details'])
        assert "***PRIVATE_IP***" in str(extra_data['ip'])
    
    @patch('orchestrator.app.security.logging.logging.getLogger')
    def test_log_access_success(self, mock_get_logger, security_logger_instance):
        """Test le logging d'accs russi."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        security_logger_instance.logger = mock_logger
        
        user_info = {
            "user_id": "user123",
            "credentials": "token=bearer_token_123456789123456789"
        }
        
        security_logger_instance.log_access("/api/users", user_info, True)
        
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args
        assert "API_ACCESS: /api/users - SUCCESS" in call_args[0][0]
        
        extra_data = call_args[1]['extra']
        assert extra_data['user_id'] == "user123"
        assert "***MASKED***" in extra_data['credentials']
    
    @patch('orchestrator.app.security.logging.logging.getLogger')
    def test_log_access_denied(self, mock_get_logger, security_logger_instance):
        """Test le logging d'accs refus."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        security_logger_instance.logger = mock_logger
        
        user_info = {
            "user_id": "attacker",
            "auth_header": "api_key=sk-invalid123456789123456789"
        }
        
        security_logger_instance.log_access("/api/admin", user_info, False)
        
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args
        assert "API_ACCESS: /api/admin - DENIED" in call_args[0][0]
        
        extra_data = call_args[1]['extra']
        assert extra_data['user_id'] == "attacker"
        assert "***MASKED***" in extra_data['auth_header']


class TestAuditLogger:
    """Tests pour la classe AuditLogger."""
    
    @pytest.fixture
    def audit_logger_instance(self):
        """Fixture pour crer une instance d'AuditLogger."""
        return AuditLogger()
    
    def test_init(self, audit_logger_instance):
        """Test l'initialisation de l'AuditLogger."""
        assert audit_logger_instance.logger.name == "audit"
        assert isinstance(audit_logger_instance.logger, logging.Logger)
    
    @patch('orchestrator.app.security.logging.logging.getLogger')
    @patch('orchestrator.app.security.logging.datetime')
    def test_log_event_with_user(self, mock_datetime, mock_get_logger):
        """Test le logging d'vnement avec utilisateur."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        
        mock_now = datetime.fromisoformat("2024-01-01T12:00:00+00:00")
        mock_datetime.now.return_value = mock_now
        
        details = {"task_id": "task123", "duration": 150}
        AuditLogger.log_event(AuditEventType.TASK_COMPLETED, "user456", details)
        
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args
        assert call_args[0][0] == "AUDIT_EVENT"
        
        extra_data = call_args[1]['extra']
        assert extra_data['timestamp'] == "2024-01-01T12:00:00+00:00"
        assert extra_data['event_type'] == "task_completed"
        assert extra_data['user_id'] == "user456"
        assert extra_data['details'] == details
    
    @patch('orchestrator.app.security.logging.logging.getLogger')
    @patch('orchestrator.app.security.logging.datetime')
    def test_log_event_system(self, mock_datetime, mock_get_logger):
        """Test le logging d'vnement systme (sans utilisateur)."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        
        mock_now = datetime.fromisoformat("2024-01-01T12:00:00+00:00")
        mock_datetime.now.return_value = mock_now
        
        details = {"error_code": "500", "endpoint": "/api/health"}
        AuditLogger.log_event(AuditEventType.ERROR_OCCURRED, None, details)
        
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args
        
        extra_data = call_args[1]['extra']
        assert extra_data['user_id'] == "system"
        assert extra_data['event_type'] == "error_occurred"
        assert extra_data['details'] == details
    
    @patch('orchestrator.app.security.logging.AuditLogger.log_event')
    def test_log_task_event(self, mock_log_event):
        """Test le logging d'vnement de tche."""
        details = {"result": "success", "output": "Task completed"}
        AuditLogger.log_task_event(AuditEventType.TASK_COMPLETED, "session789", details)
        
        mock_log_event.assert_called_once_with(
            AuditEventType.TASK_COMPLETED,
            None,
            {"session_id": "session789", **details}
        )
    
    @patch('orchestrator.app.security.logging.AuditLogger.log_event')
    def test_log_security_violation(self, mock_log_event):
        """Test le logging de violation de scurit."""
        details = {"attempted_endpoint": "/admin", "user_agent": "curl/7.68.0"}
        AuditLogger.log_security_violation("UNAUTHORIZED_ACCESS", "192.168.1.100", details)
        
        expected_details = {
            "violation_type": "UNAUTHORIZED_ACCESS",
            "source_ip": "192.168.1.100",
            **details
        }
        
        mock_log_event.assert_called_once_with(
            AuditEventType.SECURITY_VIOLATION,
            None,
            expected_details
        )


class TestGlobalInstances:
    """Tests pour les instances globales."""
    
    def test_security_logger_global_instance(self):
        """Test que l'instance globale security_logger existe."""
        assert isinstance(security_logger, SecurityLogger)
        assert security_logger.logger.name == "security"
    
    def test_audit_logger_global_instance(self):
        """Test que l'instance globale audit_logger existe."""
        assert isinstance(audit_logger, AuditLogger)
        assert audit_logger.logger.name == "audit"
    
    def test_global_instances_singleton_behavior(self):
        """Test que les instances globales se comportent comme des singletons."""
        # Pour ce test, on vrifie que les instances globales restent cohrentes
        assert security_logger is not None
        assert audit_logger is not None
        
        # Test que les loggers ont les bons noms
        assert security_logger.logger.name == "security"
        assert audit_logger.logger.name == "audit"


class TestSetupSecureLogging:
    """Tests pour la configuration du logging scuris."""
    
    @patch('orchestrator.app.security.logging.logging')
    def test_setup_secure_logging(self, mock_logging):
        """Test la configuration du logging scuris."""
        mock_security_logger = Mock()
        mock_audit_logger = Mock()
        mock_security_handler = Mock()
        mock_audit_handler = Mock()
        
        mock_logging.getLogger.side_effect = lambda name: {
            "security": mock_security_logger,
            "audit": mock_audit_logger
        }[name]
        
        mock_logging.StreamHandler.side_effect = [mock_security_handler, mock_audit_handler]
        mock_logging.Formatter.return_value = Mock()
        
        setup_secure_logging()
        
        # Vrifier que les loggers ont t rcuprs
        assert mock_logging.getLogger.call_count >= 2
        
        # Vrifier que les handlers ont t crs
        assert mock_logging.StreamHandler.call_count >= 2
        
        # Vrifier que les formatters ont t crs
        assert mock_logging.Formatter.call_count >= 2
        
        # Vrifier que les handlers ont t configurs
        mock_security_handler.setFormatter.assert_called_once()
        mock_audit_handler.setFormatter.assert_called_once()
        
        # Vrifier que les loggers ont t configurs
        mock_security_logger.addHandler.assert_called_once_with(mock_security_handler)
        mock_security_logger.setLevel.assert_called_once_with(mock_logging.INFO)
        
        mock_audit_logger.addHandler.assert_called_once_with(mock_audit_handler)
        mock_audit_logger.setLevel.assert_called_once_with(mock_logging.INFO)


class TestEdgeCases:
    """Tests pour les cas limites et d'erreur."""
    
    @pytest.fixture
    def security_logger_instance(self):
        return SecurityLogger()
    
    def test_mask_sensitive_data_empty_string(self, security_logger_instance):
        """Test le masquage avec une chane vide."""
        result = security_logger_instance._mask_sensitive_data("")
        assert result == ""
    
    def test_mask_sensitive_data_none_handling(self, security_logger_instance):
        """Test le masquage avec des valeurs None (conversion en string)."""
        # Le masquage attend une string, donc si None est pass, il y aura une erreur
        with pytest.raises(TypeError):
            security_logger_instance._mask_sensitive_data(None)
    
    def test_log_security_event_empty_details(self, security_logger_instance):
        """Test le logging d'vnement de scurit avec dtails vides."""
        with patch.object(security_logger_instance.logger, 'warning') as mock_warning:
            security_logger_instance.log_security_event("TEST_EVENT", {})
            
            mock_warning.assert_called_once()
            call_args = mock_warning.call_args
            assert "SECURITY_EVENT: TEST_EVENT" in call_args[0][0]
            assert call_args[1]['extra'] == {}
    
    def test_log_access_empty_user_info(self, security_logger_instance):
        """Test le logging d'accs avec informations utilisateur vides."""
        with patch.object(security_logger_instance.logger, 'info') as mock_info:
            security_logger_instance.log_access("/test", {}, True)
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "API_ACCESS: /test - SUCCESS" in call_args[0][0]
            assert call_args[1]['extra'] == {}
    
    @patch('orchestrator.app.security.logging.logging.getLogger')
    def test_log_error_exception_without_str(self, mock_get_logger, security_logger_instance):
        """Test le logging d'erreur avec exception qui n'a pas de __str__."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        security_logger_instance.logger = mock_logger
        
        class CustomException(Exception):
            def __str__(self):
                raise ValueError("Cannot convert to string")
        
        error = CustomException()
        # Cela ne devrait pas planter, mme si l'exception est trange
        security_logger_instance.log_error("Test message", error)
        
        mock_logger.error.assert_called_once()


@pytest.mark.unit
class TestIntegrationScenarios:
    """Tests d'intgration pour des scnarios ralistes."""
    
    def test_complete_audit_workflow(self):
        """Test un workflow complet d'audit."""
        with patch('orchestrator.app.security.logging.logging.getLogger') as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger
            
            # Simulation d'un workflow complet
            AuditLogger.log_event(AuditEventType.TASK_CREATED, "user123", {"task_type": "analysis"})
            AuditLogger.log_task_event(AuditEventType.TASK_COMPLETED, "session456", {"duration": 120})
            AuditLogger.log_security_violation("RATE_LIMIT_EXCEEDED", "10.0.0.1", {"requests": 1000})
            
            # Vrifier que tous les vnements ont t loggs
            assert mock_logger.info.call_count == 3
    
    def test_security_logging_workflow(self):
        """Test un workflow complet de logging scuris."""
        logger = SecurityLogger()
        
        with patch.object(logger.logger, 'error') as mock_error, \
             patch.object(logger.logger, 'warning') as mock_warning, \
             patch.object(logger.logger, 'info') as mock_info:
            
            # Simulation d'erreurs et d'vnements
            logger.log_error("Database connection failed", Exception("Connection timeout"))
            logger.log_security_event("BRUTE_FORCE_ATTEMPT", {"attempts": 10, "password": "secret123"})
            logger.log_access("/api/secure", {"user": "admin", "token": "bearer_xyz123456"}, True)
            
            # Vrifier les appels
            mock_error.assert_called_once()
            mock_warning.assert_called_once()
            mock_info.assert_called_once() 