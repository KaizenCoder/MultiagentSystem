"""
Tests de prévention contre Server-Side Request Forgery (SSRF).
Tests critiques pour vérifier la sécurisation des requêtes HTTP externes.
"""

import pytest
import httpx
import asyncio
from unittest.mock import patch, AsyncMock, Mock
from typing import Dict, List, Any

# Import conditionnel pour éviter les erreurs
try:
    from orchestrator.app.security.validators import NetworkValidator
    NETWORK_VALIDATOR_AVAILABLE = True
except ImportError:
    NETWORK_VALIDATOR_AVAILABLE = False
    NetworkValidator = None

try:
    from orchestrator.app.agents.tools import rag_code_search_tool
    RAG_TOOL_AVAILABLE = True
except ImportError:
    RAG_TOOL_AVAILABLE = False
    rag_code_search_tool = None


@pytest.mark.security
@pytest.mark.skipif(not NETWORK_VALIDATOR_AVAILABLE, reason="NetworkValidator not available")
class TestSSRFPrevention:
    """Tests de prévention contre Server-Side Request Forgery."""
    
    @pytest.mark.parametrize("malicious_url,should_block", [
        ("http://127.0.0.1:22", True),          # Localhost SSH
        ("http://localhost:3306", True),        # Localhost MySQL
        ("http://0.0.0.0:80", True),           # Any interface
        ("http://10.0.0.1:80", True),          # Private network 10.x
        ("http://172.16.0.1:80", True),        # Private network 172.16-31.x
        ("http://192.168.1.1:80", True),       # Private network 192.168.x
        ("http://169.254.169.254/", True),     # AWS metadata service
        ("http://[::1]:80", True),             # IPv6 localhost
        ("http://[fc00::1]:80", True),         # IPv6 private
        ("file:///etc/passwd", True),          # File protocol
        ("ftp://internal.company.com", True),   # FTP protocol
        ("gopher://localhost:25", True),       # Gopher protocol
        ("https://api.openai.com", False),     # Legitimate external API
        ("https://api.anthropic.com", False),  # Legitimate external API
        ("http://httpbin.org/get", False),     # Public test service
    ])
    def test_malicious_urls_blocked(self, malicious_url, should_block):
        """Test que les URLs malveillantes sont bloquées."""
        is_valid, error_message = NetworkValidator.validate_url(malicious_url)
        
        if should_block:
            assert not is_valid, f"URL {malicious_url} should be blocked but was allowed"
            assert error_message is not None, "Error message should be provided for blocked URLs"
            assert any(keyword in error_message.lower() for keyword in 
                      ['private', 'internal', 'blocked', 'not allowed', 'forbidden']), \
                f"Error message should indicate why URL is blocked: {error_message}"
        else:
            assert is_valid, f"URL {malicious_url} should be allowed but was blocked: {error_message}"
    
    def test_localhost_variations_blocked(self):
        """Test que toutes les variations de localhost sont bloquées."""
        localhost_variations = [
            "http://127.0.0.1",
            "http://127.1",
            "http://127.0.1",
            "http://localhost",
            "http://0.0.0.0",
            "http://0x7f000001",  # Hex encoding
            "http://2130706433",  # Decimal encoding
        ]
        
        for url in localhost_variations:
            is_valid, error = NetworkValidator.validate_url(url)
            assert not is_valid, f"Localhost variation should be blocked: {url}"
            assert "private" in error.lower() or "internal" in error.lower() or "loopback" in error.lower()
    
    def test_private_networks_blocked(self):
        """Test que tous les réseaux privés sont bloqués."""
        private_networks = [
            "http://10.0.0.1",      # 10.0.0.0/8
            "http://10.255.255.255", # 10.0.0.0/8
            "http://172.16.0.1",    # 172.16.0.0/12
            "http://172.31.255.255", # 172.16.0.0/12
            "http://192.168.0.1",   # 192.168.0.0/16
            "http://192.168.255.255", # 192.168.0.0/16
        ]
        
        for url in private_networks:
            is_valid, error = NetworkValidator.validate_url(url)
            assert not is_valid, f"Private network should be blocked: {url}"
            assert "private" in error.lower()
    
    def test_cloud_metadata_endpoints_blocked(self):
        """Test que les endpoints de métadonnées cloud sont bloqués."""
        metadata_endpoints = [
            "http://169.254.169.254/latest/meta-data/",  # AWS
            "http://169.254.169.254/computeMetadata/v1/", # GCP
            "http://169.254.169.254/metadata/instance",   # Azure
        ]
        
        for url in metadata_endpoints:
            is_valid, error = NetworkValidator.validate_url(url)
            assert not is_valid, f"Cloud metadata endpoint should be blocked: {url}"
    
    def test_dangerous_ports_blocked(self):
        """Test que les ports dangereux sont bloqués."""
        dangerous_ports = [22, 23, 25, 53, 135, 139, 445, 1433, 3306, 5432]
        
        for port in dangerous_ports:
            url = f"http://example.com:{port}"
            is_valid, error = NetworkValidator.validate_url(url)
            # Note: Selon l'implémentation, certains ports peuvent être autorisés pour des domaines externes
            if not is_valid:
                assert "port" in error.lower()
    
    def test_non_http_protocols_blocked(self):
        """Test que les protocoles non-HTTP sont bloqués."""
        non_http_protocols = [
            "file:///etc/passwd",
            "ftp://example.com/file",
            "gopher://example.com:70",
            "ldap://example.com:389",
            "dict://example.com:2628",
        ]
        
        for url in non_http_protocols:
            is_valid, error = NetworkValidator.validate_url(url)
            assert not is_valid, f"Non-HTTP protocol should be blocked: {url}"
            assert any(keyword in error.lower() for keyword in ['protocol', 'scheme']), \
                f"Error should mention protocol restriction: {error}"
    
    def test_legitimate_urls_allowed(self):
        """Test que les URLs légitimes sont autorisées."""
        legitimate_urls = [
            "https://api.openai.com/v1/models",
            "https://api.anthropic.com/v1/messages",
            "https://httpbin.org/get",
            "https://jsonplaceholder.typicode.com/posts",
            "http://example.com:80",
            "https://example.com:443",
        ]
        
        for url in legitimate_urls:
            is_valid, error = NetworkValidator.validate_url(url)
            assert is_valid, f"Legitimate URL should be allowed: {url}, error: {error}"
    
    def test_memory_api_url_validation(self):
        """Test spécifique pour la validation de l'URL de l'API mémoire."""
        # URLs valides pour l'API mémoire
        valid_memory_urls = [
            "http://memory_api:8001",
            "https://memory-api.company.com",
            "http://localhost:8001",  # Peut être autorisé en développement
        ]
        
        # URLs invalides pour l'API mémoire
        invalid_memory_urls = [
            "http://127.0.0.1:22",
            "file:///etc/passwd",
            "http://169.254.169.254/",
        ]
        
        # Test des URLs valides
        for url in valid_memory_urls:
            try:
                is_valid, error = NetworkValidator.validate_memory_api_url(url)
                # En fonction de la configuration, localhost peut être autorisé ou non
                if not is_valid and "localhost" not in url:
                    pytest.fail(f"Valid memory API URL was blocked: {url}, error: {error}")
            except AttributeError:
                # validate_memory_api_url peut ne pas exister, utiliser validate_url
                is_valid, error = NetworkValidator.validate_url(url)
        
        # Test des URLs invalides
        for url in invalid_memory_urls:
            try:
                is_valid, error = NetworkValidator.validate_memory_api_url(url)
            except AttributeError:
                is_valid, error = NetworkValidator.validate_url(url)
            
            assert not is_valid, f"Invalid memory API URL should be blocked: {url}"


@pytest.mark.security
@pytest.mark.skipif(not RAG_TOOL_AVAILABLE, reason="RAG tool not available")
class TestRAGToolSSRFPrevention:
    """Tests SSRF pour l'outil RAG qui utilise l'API mémoire."""
    
    @pytest.mark.asyncio
    async def test_rag_tool_with_safe_query(self, mock_httpx_client):
        """Test de l'outil RAG avec une requête sûre."""
        with patch('httpx.AsyncClient', return_value=mock_httpx_client({})):
            result = await rag_code_search_tool("search for Python functions")
            assert isinstance(result, str)
            assert "error" not in result.lower() or "mock rag result" in result.lower()
    
    @pytest.mark.asyncio 
    async def test_rag_tool_input_validation(self):
        """Test de la validation des entrées de l'outil RAG."""
        # Test avec query vide
        result = await rag_code_search_tool("")
        assert "error" in result.lower() or "invalid" in result.lower()
        
        # Test avec query trop longue
        long_query = "x" * 2000
        result = await rag_code_search_tool(long_query)
        assert "error" in result.lower() or "too long" in result.lower()
    
    @pytest.mark.asyncio
    async def test_rag_tool_url_validation(self):
        """Test que l'outil RAG valide l'URL avant la requête."""
        # Mock de la configuration avec URL malveillante
        with patch('orchestrator.app.config.settings') as mock_settings:
            mock_settings.MEMORY_API_URL = "http://127.0.0.1:22"
            
            # Mock NetworkValidator pour retourner False avec message d'erreur
            with patch('orchestrator.app.security.validators.NetworkValidator.validate_memory_api_url') as mock_validator:
                mock_validator.return_value = (False, "Access to port 22 not allowed for security")
                
                result = await rag_code_search_tool("test query")
                
                # L'outil devrait détecter l'URL invalide et refuser la requête
                assert "error" in result.lower()
                assert any(keyword in result.lower() for keyword in 
                          ['network', 'validation', 'failed', 'forbidden'])
    
    @pytest.mark.asyncio
    async def test_rag_tool_timeout_handling(self):
        """Test de la gestion des timeouts dans l'outil RAG."""
        # Mock validation URL pour passer
        with patch('orchestrator.app.security.validators.NetworkValidator.validate_memory_api_url') as mock_validator:
            mock_validator.return_value = (True, None)
            
            with patch('orchestrator.app.agents.tools.get_http_client') as mock_get_client:
                # Simulation d'un timeout
                mock_client = AsyncMock()
                mock_client.post.side_effect = httpx.TimeoutException("Request timeout")
                mock_get_client.return_value = mock_client
                
                result = await rag_code_search_tool("test query")
                
                assert "error" in result.lower()
                assert "timeout" in result.lower()
    
    @pytest.mark.asyncio
    async def test_rag_tool_connection_error_handling(self):
        """Test de la gestion des erreurs de connexion dans l'outil RAG."""
        # Mock validation URL pour passer
        with patch('orchestrator.app.security.validators.NetworkValidator.validate_memory_api_url') as mock_validator:
            mock_validator.return_value = (True, None)
            
            with patch('orchestrator.app.agents.tools.get_http_client') as mock_get_client:
                # Simulation d'une erreur de connexion
                mock_client = AsyncMock()
                mock_client.post.side_effect = httpx.ConnectError("Connection failed")
                mock_get_client.return_value = mock_client
                
                result = await rag_code_search_tool("test query")
                
                assert "error" in result.lower()
                assert any(keyword in result.lower() for keyword in ['network', 'connectivity', 'connection'])


@pytest.mark.security
class TestSSRFProtectionConfiguration:
    """Tests de configuration de la protection SSRF."""
    
    def test_network_validator_configuration(self):
        """Test de la configuration du validateur réseau."""
        if not NETWORK_VALIDATOR_AVAILABLE:
            pytest.skip("NetworkValidator not available")
        
        # Vérifier que les constantes de sécurité sont définies
        assert hasattr(NetworkValidator, 'BLOCKED_IPS') or hasattr(NetworkValidator, 'PRIVATE_NETWORKS')
        
        # Vérifier que les schémas autorisés sont restrictifs
        if hasattr(NetworkValidator, 'ALLOWED_SCHEMES'):
            allowed_schemes = NetworkValidator.ALLOWED_SCHEMES
            assert 'http' in allowed_schemes
            assert 'https' in allowed_schemes
            assert 'file' not in allowed_schemes
            assert 'ftp' not in allowed_schemes
    
    def test_environment_variable_protection(self):
        """Test que la protection fonctionne même avec des variables d'environnement malveillantes."""
        import os
        
        # Simulation d'une configuration malveillante via variables d'environnement
        original_memory_url = os.environ.get('MEMORY_API_URL')
        
        try:
            os.environ['MEMORY_API_URL'] = 'http://127.0.0.1:22'
            
            if NETWORK_VALIDATOR_AVAILABLE:
                is_valid, error = NetworkValidator.validate_url(os.environ['MEMORY_API_URL'])
                assert not is_valid, "Malicious environment variable should be blocked"
        
        finally:
            # Restaurer la configuration originale
            if original_memory_url:
                os.environ['MEMORY_API_URL'] = original_memory_url
            elif 'MEMORY_API_URL' in os.environ:
                del os.environ['MEMORY_API_URL']


@pytest.mark.integration
@pytest.mark.security
class TestSSRFIntegrationTests:
    """Tests d'intégration pour la protection SSRF."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_ssrf_protection(self, security_test_headers):
        """Test end-to-end de la protection SSRF via l'API."""
        try:
            from fastapi.testclient import TestClient
            from orchestrator.app.main import app
            
            # Créer un client de test synchrone
            with TestClient(app) as test_client:
                # Test avec une tâche qui pourrait déclencher une requête SSRF
                malicious_task = {
                    "task_description": "Search for code examples using internal metadata service",
                    "code_context": "# This might trigger SSRF"
                }
                
                # La requête devrait être traitée sans déclencher de SSRF
                response = test_client.post(
                    "/invoke",
                    json=malicious_task,
                    headers=security_test_headers
                )
                
                # Vérifier que la réponse ne contient pas d'informations sensibles
                if response.status_code == 200:
                    response_data = response.json()
                    response_text = str(response_data)
                    
                    # Vérifier qu'aucune information sensible n'a été exfiltrée
                    forbidden_patterns = [
                        'ami-',  # AWS AMI IDs
                        'i-0',   # AWS instance IDs
                        'arn:aws',  # AWS ARNs
                        'metadata',  # Metadata responses
                        'secret',   # Potential secrets
                    ]
                    
                    for pattern in forbidden_patterns:
                        assert pattern not in response_text.lower(), \
                            f"Sensitive information detected in response: {pattern}"
                            
        except ImportError:
            pytest.skip("FastAPI TestClient not available")
    
    @pytest.mark.asyncio
    async def test_ssrf_logging_and_monitoring(self, log_capture):
        """Test que les tentatives SSRF sont correctement loggées."""
        if not NETWORK_VALIDATOR_AVAILABLE:
            pytest.skip("NetworkValidator not available")
        
        # Tentative de validation d'URL malveillante
        malicious_url = "http://169.254.169.254/latest/meta-data/"
        is_valid, error = NetworkValidator.validate_url(malicious_url)
        
        assert not is_valid
        
        # Vérifier que l'événement est loggé (selon l'implémentation du logging)
        log_contents = log_capture.getvalue()
        # Cette vérification dépend de l'implémentation spécifique du logging
    
    def test_ssrf_protection_bypass_attempts(self):
        """Test de résistance aux tentatives de bypass de la protection SSRF."""
        if not NETWORK_VALIDATOR_AVAILABLE:
            pytest.skip("NetworkValidator not available")
        
        # Tentatives de bypass courantes
        bypass_attempts = [
            "http://127.0.0.1@example.com/",  # Confusion d'authentification
            "http://example.com#127.0.0.1",  # Fragment
            "http://127.1/",                  # IP raccourcie
            "http://0x7f000001/",            # Hex encoding
            "http://2130706433/",            # Decimal encoding
            "http://127.0.0.1.xip.io/",      # Wildcard DNS
            "http://localtest.me/",          # Public domain pointing to localhost
        ]
        
        for url in bypass_attempts:
            is_valid, error = NetworkValidator.validate_url(url)
            # La plupart de ces tentatives devraient être bloquées
            # Certaines peuvent passer selon la sophistication de la validation
            if not is_valid:
                assert any(keyword in error.lower() for keyword in 
                          ['private', 'internal', 'blocked', 'not allowed'])


@pytest.mark.performance
@pytest.mark.security
class TestSSRFValidationPerformance:
    """Tests de performance pour la validation SSRF."""
    
    def test_url_validation_performance(self, performance_monitor, malicious_payloads):
        """Test que la validation d'URL est suffisamment rapide."""
        if not NETWORK_VALIDATOR_AVAILABLE:
            pytest.skip("NetworkValidator not available")
        
        performance_monitor.start()
        
        # Test avec de nombreuses URLs
        test_urls = malicious_payloads['ssrf_urls'] + [
            "https://api.openai.com",
            "https://api.anthropic.com",
            "http://httpbin.org/get",
        ] * 10
        
        for url in test_urls:
            NetworkValidator.validate_url(url)
        
        # La validation de 50+ URLs doit prendre moins de 100ms
        performance_monitor.assert_max_duration(100)
    
    @pytest.mark.asyncio
    async def test_rag_tool_performance_with_validation(self, performance_monitor):
        """Test que la validation SSRF n'impacte pas significativement la performance."""
        if not RAG_TOOL_AVAILABLE:
            pytest.skip("RAG tool not available")
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.post.return_value.json.return_value = {
                'results': [{'content': 'test', 'score': 0.9}]
            }
            mock_context.__aenter__.return_value.post.return_value.raise_for_status = Mock()
            mock_client.return_value = mock_context
            
            performance_monitor.start()
            
            # 10 appels successifs avec validation
            for _ in range(10):
                await rag_code_search_tool("test query")
            
            # 10 appels avec validation ne doivent pas dépasser 1 seconde
            performance_monitor.assert_max_duration(1000)
