"""
Tests pour les validateurs de scurit - Sprint 3.1
Module critique pour la prvention des vulnrabilits RCE et SSRF.
"""

import pytest
from orchestrator.app.security.validators import CodeValidator, NetworkValidator, InputSanitizer


class TestCodeValidator:
    """Tests pour la validation de code Python et prvention RCE."""
    
    def test_validate_python_code_empty(self):
        """Test avec code vide."""
        is_valid, error = CodeValidator.validate_python_code("")
        assert not is_valid
        assert error == "Code is empty"
        
        is_valid, error = CodeValidator.validate_python_code(None)
        assert not is_valid
        assert error == "Code is empty"
    
    def test_validate_python_code_dangerous_imports(self):
        """Test dtection d'imports dangereux."""
        dangerous_codes = [
            "import os",
            "import subprocess", 
            "from os import system",
        ]
        
        for code in dangerous_codes:
            is_valid, error = CodeValidator.validate_python_code(code)
            assert not is_valid
            assert "unsafe code pattern" in error.lower()
    
    def test_validate_python_code_dangerous_functions(self):
        """Test dtection de fonctions dangereuses."""
        dangerous_codes = [
            "eval('1+1')",
            "exec('print(1)')",
            "open('/etc/passwd')",
        ]
        
        for code in dangerous_codes:
            is_valid, error = CodeValidator.validate_python_code(code)
            assert not is_valid
            assert "unsafe code pattern" in error.lower()
    
    def test_validate_python_code_safe_code(self):
        """Test avec du code sr qui doit passer."""
        safe_codes = [
            "x = 1 + 2",
            "def add(a, b):\n    return a + b",
            "import math\nmath.sqrt(4)",
        ]
        
        for code in safe_codes:
            is_valid, error = CodeValidator.validate_python_code(code)
            assert is_valid, f"Safe code should be valid: {code}, Error: {error}"
            assert error is None


class TestNetworkValidator:
    """Tests pour la validation d'URLs et prvention SSRF."""
    
    def test_validate_url_empty(self):
        """Test avec URL vide."""
        is_valid, error = NetworkValidator.validate_url("")
        assert not is_valid
        assert error == "URL is empty"
    
    def test_validate_url_blocked_hostnames(self):
        """Test avec hostnames bloqus."""
        blocked_urls = [
            "http://127.0.0.1",
            "http://localhost",
            "https://127.0.0.1",
        ]
        
        for url in blocked_urls:
            is_valid, error = NetworkValidator.validate_url(url)
            assert not is_valid
            assert "blocked" in error.lower() or "not allowed" in error.lower()
    
    def test_validate_url_valid_public_urls(self):
        """Test avec URLs publiques valides."""
        valid_urls = [
            "http://example.com",
            "https://www.google.com",
            "https://api.github.com",
        ]
        
        for url in valid_urls:
            is_valid, error = NetworkValidator.validate_url(url)
            assert is_valid, f"Valid URL should pass: {url}, Error: {error}"
            assert error is None
    
    def test_validate_memory_api_url_localhost_allowed(self):
        """Test que localhost est autoris pour Memory API avec ports srs."""
        allowed_urls = [
            "http://localhost:8001",
            "http://memory_api:8001",
            "http://127.0.0.1:8001",
        ]
        
        for url in allowed_urls:
            is_valid, error = NetworkValidator.validate_memory_api_url(url)
            assert is_valid, f"Memory API URL should be allowed: {url}, Error: {error}"
            assert error is None


class TestInputSanitizer:
    """Tests pour la sanitisation des entres utilisateur."""
    
    def test_sanitize_task_description_empty(self):
        """Test avec description vide."""
        result = InputSanitizer.sanitize_task_description("")
        assert result == ""
        
        result = InputSanitizer.sanitize_task_description(None)
        assert result == ""
    
    def test_sanitize_task_description_html_escape(self):
        """Test chappement HTML."""
        result = InputSanitizer.sanitize_task_description("<script>alert('xss')</script>")
        assert "<" not in result
        assert ">" not in result
    
    def test_sanitize_session_id_valid_uuid(self):
        """Test avec UUIDs valides."""
        valid_uuid = "12345678-1234-1234-1234-123456789abc"
        result = InputSanitizer.sanitize_session_id(valid_uuid)
        assert result is not None
        assert result == valid_uuid.lower()
    
    def test_sanitize_session_id_invalid_uuid(self):
        """Test avec UUIDs invalides."""
        invalid_uuids = ["not-a-uuid", "", "12345678-1234"]
        
        for uuid in invalid_uuids:
            result = InputSanitizer.sanitize_session_id(uuid)
            assert result is None
    
    def test_sanitize_code_context_normal_code(self):
        """Test avec du code normal."""
        normal_code = "def hello_world():\n    print('Hello, World!')"
        result = InputSanitizer.sanitize_code_context(normal_code)
        assert len(result) > 0
        assert result.strip() == result
        assert "def" in result 



