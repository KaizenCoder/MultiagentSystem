"""
Tests complets pour secrets_manager.py
Coverage objectif : 80% (Sprint 2.1 IA-1)
"""

import pytest
import os
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
from contextlib import contextmanager

from orchestrator.app.security.secrets_manager import (
    ProductionSecretsManager,
    SecretProvider,
    DockerSecretsProvider,
    EnvironmentVariablesProvider,
    LocalFileProvider,
    AzureKeyVaultProvider,
    HashiCorpVaultProvider,
    SecretType,
    SecretSource,
    SecretMetadata,
    SecretNotFoundError,
    SecretExpiredError,
    SecretRotationError,
    get_default_secrets_manager,
    get_secrets_manager,
    get_secret
)


@pytest.mark.unit
class TestSecretMetadata:
    """Tests pour SecretMetadata."""
    
    def test_secret_metadata_creation(self):
        """Test cration mtadonnes de secret."""
        metadata = SecretMetadata(
            name="test_secret",
            secret_type=SecretType.API_KEY,
            source=SecretSource.ENVIRONMENT_VARIABLES,
            created_at=time.time(),
            last_accessed=time.time(),
            access_count=1
        )
        
        assert metadata.name == "test_secret"
        assert metadata.secret_type == SecretType.API_KEY
        assert metadata.source == SecretSource.ENVIRONMENT_VARIABLES
        assert metadata.access_count == 1
    
    def test_secret_metadata_not_expired(self):
        """Test secret non expir."""
        metadata = SecretMetadata(
            name="test",
            secret_type=SecretType.API_KEY,
            source=SecretSource.ENVIRONMENT_VARIABLES,
            created_at=time.time(),
            last_accessed=time.time(),
            access_count=1,
            expires_at=time.time() + 3600  # Expire dans 1h
        )
        
        assert not metadata.is_expired()
    
    def test_secret_metadata_expired(self):
        """Test secret expir."""
        metadata = SecretMetadata(
            name="test",
            secret_type=SecretType.API_KEY,
            source=SecretSource.ENVIRONMENT_VARIABLES,
            created_at=time.time(),
            last_accessed=time.time(),
            access_count=1,
            expires_at=time.time() - 1  # Expir il y a 1s
        )
        
        assert metadata.is_expired()
    
    def test_secret_metadata_needs_rotation(self):
        """Test rotation ncessaire."""
        metadata = SecretMetadata(
            name="test",
            secret_type=SecretType.API_KEY,
            source=SecretSource.ENVIRONMENT_VARIABLES,
            created_at=time.time() - 7200,  # Cr il y a 2h
            last_accessed=time.time(),
            access_count=1,
            rotation_interval=3600  # Rotation toutes les heures
        )
        
        assert metadata.needs_rotation()


@pytest.mark.unit
class TestDockerSecretsProvider:
    """Tests pour DockerSecretsProvider."""
    
    def test_docker_secrets_provider_init(self):
        """Test initialisation provider Docker."""
        with tempfile.TemporaryDirectory() as temp_dir:
            provider = DockerSecretsProvider(Path(temp_dir))
            assert provider.secrets_path == Path(temp_dir)
    
    def test_get_secret_success(self):
        """Test rcupration secret Docker russie."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_path = Path(temp_dir)
            secret_file = secrets_path / "api_key"
            secret_file.write_text("secret_value_123")
            
            provider = DockerSecretsProvider(secrets_path)
            secret = provider.get_secret("api_key")
            
            assert secret == "secret_value_123"
    
    def test_get_secret_not_found(self):
        """Test secret Docker non trouv."""
        with tempfile.TemporaryDirectory() as temp_dir:
            provider = DockerSecretsProvider(Path(temp_dir))
            
            with pytest.raises(SecretNotFoundError):
                provider.get_secret("nonexistent")
    
    def test_get_secret_empty(self):
        """Test secret Docker vide."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_path = Path(temp_dir)
            secret_file = secrets_path / "empty_secret"
            secret_file.write_text("")
            
            provider = DockerSecretsProvider(secrets_path)
            
            with pytest.raises(SecretNotFoundError):
                provider.get_secret("empty_secret")
    
    def test_list_secrets(self):
        """Test listage secrets Docker."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_path = Path(temp_dir)
            (secrets_path / "secret1").write_text("value1")
            (secrets_path / "secret2").write_text("value2")
            
            provider = DockerSecretsProvider(secrets_path)
            secrets = provider.list_secrets()
            
            assert "secret1" in secrets
            assert "secret2" in secrets
            assert len(secrets) == 2
    
    def test_secret_exists(self):
        """Test vrification existence secret Docker."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_path = Path(temp_dir)
            (secrets_path / "existing_secret").write_text("value")
            
            provider = DockerSecretsProvider(secrets_path)
            
            assert provider.secret_exists("existing_secret")
            assert not provider.secret_exists("nonexistent_secret")


@pytest.mark.unit
class TestEnvironmentVariablesProvider:
    """Tests pour EnvironmentVariablesProvider."""
    
    def test_environment_provider_init(self):
        """Test initialisation provider environnement."""
        provider = EnvironmentVariablesProvider("TEST_")
        assert provider.prefix == "TEST_"
    
    @patch.dict(os.environ, {"SECRET_API_KEY": "test_value_123"})
    def test_get_secret_success(self):
        """Test rcupration secret env russie."""
        provider = EnvironmentVariablesProvider()
        secret = provider.get_secret("api_key")
        
        assert secret == "test_value_123"
    
    def test_get_secret_not_found(self):
        """Test secret env non trouv."""
        provider = EnvironmentVariablesProvider()
        
        with pytest.raises(SecretNotFoundError):
            provider.get_secret("nonexistent_secret")
    
    @patch.dict(os.environ, {"SECRET_EMPTY": ""})
    def test_get_secret_empty(self):
        """Test secret env vide."""
        provider = EnvironmentVariablesProvider()
        
        with pytest.raises(SecretNotFoundError):
            provider.get_secret("empty")
    
    @patch.dict(os.environ, {"SECRET_KEY1": "value1", "SECRET_KEY2": "value2", "OTHER_VAR": "value3"})
    def test_list_secrets(self):
        """Test listage secrets env."""
        provider = EnvironmentVariablesProvider()
        secrets = provider.list_secrets()
        
        assert "key1" in secrets
        assert "key2" in secrets
        assert "other_var" not in secrets
    
    @patch.dict(os.environ, {"SECRET_EXISTING": "value"})
    def test_secret_exists(self):
        """Test vrification existence secret env."""
        provider = EnvironmentVariablesProvider()
        
        assert provider.secret_exists("existing")
        assert not provider.secret_exists("nonexistent")


@pytest.mark.unit
class TestLocalFileProvider:
    """Tests pour LocalFileProvider."""
    
    def test_local_file_provider_init(self):
        """Test initialisation provider fichiers locaux."""
        with tempfile.TemporaryDirectory() as temp_dir:
            provider = LocalFileProvider(Path(temp_dir))
            assert provider.secrets_dir == Path(temp_dir)
    
    def test_get_secret_success(self):
        """Test rcupration secret fichier russie."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_dir = Path(temp_dir)
            secret_file = secrets_dir / "api_key.secret"
            secret_file.write_text("local_secret_value")
            
            provider = LocalFileProvider(secrets_dir)
            secret = provider.get_secret("api_key")
            
            assert secret == "local_secret_value"
    
    def test_get_secret_not_found(self):
        """Test secret fichier non trouv."""
        with tempfile.TemporaryDirectory() as temp_dir:
            provider = LocalFileProvider(Path(temp_dir))
            
            with pytest.raises(SecretNotFoundError):
                provider.get_secret("nonexistent")
    
    def test_get_secret_empty(self):
        """Test secret fichier vide."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_dir = Path(temp_dir)
            secret_file = secrets_dir / "empty.secret"
            secret_file.write_text("")
            
            provider = LocalFileProvider(secrets_dir)
            
            with pytest.raises(SecretNotFoundError):
                provider.get_secret("empty")
    
    def test_list_secrets(self):
        """Test listage secrets fichiers."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_dir = Path(temp_dir)
            (secrets_dir / "secret1.secret").write_text("value1")
            (secrets_dir / "secret2.secret").write_text("value2")
            (secrets_dir / "not_secret.txt").write_text("ignore")
            
            provider = LocalFileProvider(secrets_dir)
            secrets = provider.list_secrets()
            
            assert "secret1" in secrets
            assert "secret2" in secrets
            assert "not_secret" not in secrets
    
    def test_secret_exists(self):
        """Test vrification existence secret fichier."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_dir = Path(temp_dir)
            (secrets_dir / "existing.secret").write_text("value")
            
            provider = LocalFileProvider(secrets_dir)
            
            assert provider.secret_exists("existing")
            assert not provider.secret_exists("nonexistent")


@pytest.mark.unit
class TestAzureKeyVaultProvider:
    """Tests pour AzureKeyVaultProvider."""
    
    @patch('orchestrator.app.security.secrets_manager.AZURE_AVAILABLE', True)
    @patch('orchestrator.app.security.secrets_manager.DefaultAzureCredential')
    @patch('orchestrator.app.security.secrets_manager.SecretClient')
    def test_azure_provider_init(self, mock_secret_client, mock_credential):
        """Test initialisation provider Azure KeyVault."""
        mock_credential_instance = Mock()
        mock_credential.return_value = mock_credential_instance
        
        provider = AzureKeyVaultProvider("https://test.vault.azure.net/")
        
        assert provider.vault_url == "https://test.vault.azure.net/"
        mock_secret_client.assert_called_once()
    
    def test_azure_provider_not_available(self):
        """Test provider Azure non disponible."""
        with patch('orchestrator.app.security.secrets_manager.AZURE_AVAILABLE', False):
            with pytest.raises(ImportError):
                AzureKeyVaultProvider("https://test.vault.azure.net/")
    
    @patch('orchestrator.app.security.secrets_manager.AZURE_AVAILABLE', True)
    @patch('orchestrator.app.security.secrets_manager.DefaultAzureCredential')
    @patch('orchestrator.app.security.secrets_manager.SecretClient')
    def test_get_secret_success(self, mock_secret_client, mock_credential):
        """Test rcupration secret Azure russie."""
        mock_client_instance = Mock()
        mock_secret_client.return_value = mock_client_instance
        
        mock_secret = Mock()
        mock_secret.value = "azure_secret_value"
        mock_client_instance.get_secret.return_value = mock_secret
        
        provider = AzureKeyVaultProvider("https://test.vault.azure.net/")
        secret = provider.get_secret("api_key")
        
        assert secret == "azure_secret_value"
        mock_client_instance.get_secret.assert_called_once_with("api_key")
    
    @patch('orchestrator.app.security.secrets_manager.AZURE_AVAILABLE', True)
    @patch('orchestrator.app.security.secrets_manager.DefaultAzureCredential')
    @patch('orchestrator.app.security.secrets_manager.SecretClient')
    def test_get_secret_not_found(self, mock_secret_client, mock_credential):
        """Test secret Azure non trouv."""
        mock_client_instance = Mock()
        mock_secret_client.return_value = mock_client_instance
        mock_client_instance.get_secret.side_effect = Exception("Secret not found")
        
        provider = AzureKeyVaultProvider("https://test.vault.azure.net/")
        
        with pytest.raises(SecretNotFoundError):
            provider.get_secret("nonexistent")


@pytest.mark.unit
class TestHashiCorpVaultProvider:
    """Tests pour HashiCorpVaultProvider."""
    
    @patch('orchestrator.app.security.secrets_manager.VAULT_AVAILABLE', True)
    @patch('orchestrator.app.security.secrets_manager.hvac.Client')
    def test_vault_provider_init(self, mock_hvac_client):
        """Test initialisation provider HashiCorp Vault."""
        mock_client_instance = Mock()
        mock_client_instance.is_authenticated.return_value = True
        mock_hvac_client.return_value = mock_client_instance
        
        provider = HashiCorpVaultProvider("https://vault.example.com", "test_token")
        
        assert provider.vault_url == "https://vault.example.com"
        assert provider.mount_point == "secret"
        mock_hvac_client.assert_called_once_with(url="https://vault.example.com", token="test_token")
    
    def test_vault_provider_not_available(self):
        """Test provider Vault non disponible."""
        with patch('orchestrator.app.security.secrets_manager.VAULT_AVAILABLE', False):
            with pytest.raises(ImportError):
                HashiCorpVaultProvider("https://vault.example.com", "test_token")
    
    @patch('orchestrator.app.security.secrets_manager.VAULT_AVAILABLE', True)
    @patch('orchestrator.app.security.secrets_manager.hvac.Client')
    def test_vault_not_authenticated(self, mock_hvac_client):
        """Test provider Vault non authentifi."""
        mock_client_instance = Mock()
        mock_client_instance.is_authenticated.return_value = False
        mock_hvac_client.return_value = mock_client_instance
        
        with pytest.raises(ValueError):
            HashiCorpVaultProvider("https://vault.example.com", "invalid_token")


@pytest.mark.unit
class TestProductionSecretsManager:
    """Tests pour ProductionSecretsManager."""
    
    def test_secrets_manager_init(self):
        """Test initialisation gestionnaire de secrets."""
        primary = Mock(spec=SecretProvider)
        fallback = Mock(spec=SecretProvider)
        
        manager = ProductionSecretsManager(
            primary_provider=primary,
            fallback_providers=[fallback],
            cache_ttl=1800
        )
        
        assert manager.primary_provider == primary
        assert fallback in manager.fallback_providers
        assert manager.cache_ttl == 1800
    
    def test_get_secret_from_primary(self):
        """Test rcupration secret depuis provider principal."""
        primary = Mock(spec=SecretProvider)
        primary.get_secret.return_value = "primary_secret_value"
        
        manager = ProductionSecretsManager(primary_provider=primary)
        secret = manager.get_secret("test_key")
        
        assert secret == "primary_secret_value"
        primary.get_secret.assert_called_once_with("test_key")
    
    def test_get_secret_fallback(self):
        """Test rcupration secret depuis fallback."""
        primary = Mock(spec=SecretProvider)
        primary.get_secret.side_effect = SecretNotFoundError("Not found in primary")
        
        fallback = Mock(spec=SecretProvider)
        fallback.get_secret.return_value = "fallback_secret_value"
        
        manager = ProductionSecretsManager(
            primary_provider=primary,
            fallback_providers=[fallback]
        )
        secret = manager.get_secret("test_key")
        
        assert secret == "fallback_secret_value"
        fallback.get_secret.assert_called_once_with("test_key")
    
    def test_get_secret_cache_hit(self):
        """Test cache hit pour rcupration secret."""
        primary = Mock(spec=SecretProvider)
        primary.get_secret.return_value = "cached_secret"
        
        manager = ProductionSecretsManager(primary_provider=primary, cache_ttl=3600)
        
        # Premier appel - mise en cache
        secret1 = manager.get_secret("cached_key")
        # Deuxime appel - cache hit
        secret2 = manager.get_secret("cached_key")
        
        assert secret1 == secret2 == "cached_secret"
        # Provider appel une seule fois
        primary.get_secret.assert_called_once()
    
    def test_get_secret_expired(self):
        """Test secret expir."""
        primary = Mock(spec=SecretProvider)
        
        manager = ProductionSecretsManager(primary_provider=primary)
        
        # Simuler un secret expir dans le cache
        metadata = SecretMetadata(
            name="expired_key",
            secret_type=SecretType.API_KEY,
            source=SecretSource.ENVIRONMENT_VARIABLES,
            created_at=time.time(),
            last_accessed=time.time(),
            access_count=1,
            expires_at=time.time() - 1  # Expir
        )
        manager._cache["expired_key"] = "expired_value"
        manager._metadata["expired_key"] = metadata
        
        with pytest.raises(SecretExpiredError):
            manager.get_secret("expired_key")
    
    def test_get_secret_not_found_anywhere(self):
        """Test secret non trouv nulle part."""
        primary = Mock(spec=SecretProvider)
        primary.get_secret.side_effect = SecretNotFoundError("Not in primary")
        
        fallback = Mock(spec=SecretProvider)
        fallback.get_secret.side_effect = SecretNotFoundError("Not in fallback")
        
        manager = ProductionSecretsManager(
            primary_provider=primary,
            fallback_providers=[fallback]
        )
        
        with pytest.raises(SecretNotFoundError):
            manager.get_secret("missing_key")
    
    def test_list_available_secrets(self):
        """Test listage secrets disponibles."""
        primary = Mock(spec=SecretProvider)
        primary.list_secrets.return_value = ["secret1", "secret2"]
        
        fallback = Mock(spec=SecretProvider)
        fallback.list_secrets.return_value = ["secret2", "secret3"]
        
        manager = ProductionSecretsManager(
            primary_provider=primary,
            fallback_providers=[fallback]
        )
        
        secrets = manager.list_available_secrets()
        
        assert "secret1" in secrets
        assert "secret2" in secrets
        assert "secret3" in secrets
        assert len(secrets) == 3  # Ddoublonnage
    
    def test_clear_cache(self):
        """Test vidage cache."""
        primary = Mock(spec=SecretProvider)
        manager = ProductionSecretsManager(primary_provider=primary)
        
        # Ajouter donnes dans le cache
        manager._cache["test"] = "value"
        manager._metadata["test"] = Mock()
        
        manager.clear_cache()
        
        assert len(manager._cache) == 0
        assert len(manager._metadata) == 0
    
    def test_get_cache_stats(self):
        """Test statistiques cache."""
        primary = Mock(spec=SecretProvider)
        manager = ProductionSecretsManager(primary_provider=primary)
        
        # Ajouter mtadonnes
        metadata = SecretMetadata(
            name="test",
            secret_type=SecretType.API_KEY,
            source=SecretSource.ENVIRONMENT_VARIABLES,
            created_at=time.time() - 100,
            last_accessed=time.time(),
            access_count=5
        )
        manager._metadata["test"] = metadata
        manager._cache["test"] = "value"
        
        stats = manager.get_cache_stats()
        
        assert stats["cached_secrets_count"] == 1
        assert stats["total_accesses"] == 5
        assert "cache_hit_ratio" in stats
        assert "oldest_secret_age" in stats
        assert stats["most_accessed_secret"] == "test"
    
    def test_get_audit_trail(self):
        """Test audit trail."""
        primary = Mock(spec=SecretProvider)
        manager = ProductionSecretsManager(primary_provider=primary)
        
        # Ajouter entres audit
        for i in range(5):
            manager._access_log.append({
                "timestamp": time.time(),
                "secret_name": f"secret_{i}",
                "action": "fetched"
            })
        
        audit = manager.get_audit_trail(limit=3)
        
        assert len(audit) == 3
        assert audit[0]["secret_name"] == "secret_2"  # Les 3 derniers
    
    def test_secret_context_manager(self):
        """Test context manager pour secrets."""
        primary = Mock(spec=SecretProvider)
        primary.get_secret.return_value = "context_secret"
        
        manager = ProductionSecretsManager(primary_provider=primary)
        
        with manager.secret_context("test_key") as secret:
            assert secret == "context_secret"
    
    def test_secret_context_manager_error(self):
        """Test context manager avec erreur."""
        primary = Mock(spec=SecretProvider)
        primary.get_secret.side_effect = SecretNotFoundError("Not found")
        
        manager = ProductionSecretsManager(primary_provider=primary)
        
        with pytest.raises(SecretNotFoundError):
            with manager.secret_context("missing_key") as secret:
                pass


@pytest.mark.unit 
class TestSecretsManagerDefaults:
    """Tests pour fonctions de configuration par dfaut."""
    
    @patch.dict(os.environ, {"ENVIRONMENT": "development"})
    @patch('orchestrator.app.security.secrets_manager.LocalFileProvider')
    @patch('orchestrator.app.security.secrets_manager.EnvironmentVariablesProvider')
    def test_get_default_secrets_manager_development(self, mock_env_provider, mock_local_provider):
        """Test configuration dveloppement."""
        mock_local_instance = Mock()
        mock_local_provider.return_value = mock_local_instance
        mock_env_instance = Mock()
        mock_env_provider.return_value = mock_env_instance
        
        manager = get_default_secrets_manager()
        
        assert manager.primary_provider == mock_local_instance
        assert mock_env_instance in manager.fallback_providers
        assert manager.cache_ttl == 300  # 5 minutes en dev
    
    @patch.dict(os.environ, {"ENVIRONMENT": "staging"})
    @patch('orchestrator.app.security.secrets_manager.DockerSecretsProvider')
    @patch('orchestrator.app.security.secrets_manager.EnvironmentVariablesProvider')
    def test_get_default_secrets_manager_staging(self, mock_env_provider, mock_docker_provider):
        """Test configuration staging."""
        mock_docker_instance = Mock()
        mock_docker_provider.return_value = mock_docker_instance
        mock_env_instance = Mock()
        mock_env_provider.return_value = mock_env_instance
        
        manager = get_default_secrets_manager()
        
        assert manager.primary_provider == mock_docker_instance
        assert mock_env_instance in manager.fallback_providers
        assert manager.cache_ttl == 1800  # 30 minutes en staging
    
    @patch.dict(os.environ, {
        "ENVIRONMENT": "production",
        "AZURE_KEYVAULT_URL": "https://test.vault.azure.net/"
    })
    @patch('orchestrator.app.security.secrets_manager.AZURE_AVAILABLE', True)
    @patch('orchestrator.app.security.secrets_manager.AzureKeyVaultProvider')
    @patch('orchestrator.app.security.secrets_manager.DockerSecretsProvider')
    @patch('orchestrator.app.security.secrets_manager.EnvironmentVariablesProvider')
    def test_get_default_secrets_manager_production_azure(self, mock_env_provider, mock_docker_provider, mock_azure_provider):
        """Test configuration production avec Azure."""
        mock_azure_instance = Mock()
        mock_azure_provider.return_value = mock_azure_instance
        
        manager = get_default_secrets_manager()
        
        assert manager.primary_provider == mock_azure_instance
        assert manager.cache_ttl == 3600  # 1 heure en production
        assert manager.enable_rotation == True
    
    def test_get_secrets_manager_singleton(self):
        """Test pattern singleton pour gestionnaire global."""
        # Reset singleton
        import orchestrator.app.security.secrets_manager
        orchestrator.app.security.secrets_manager._secrets_manager = None
        
        manager1 = get_secrets_manager()
        manager2 = get_secrets_manager()
        
        assert manager1 is manager2
    
    @patch('orchestrator.app.security.secrets_manager.get_secrets_manager')
    def test_get_secret_convenience_function(self, mock_get_manager):
        """Test fonction de convnience get_secret."""
        mock_manager = Mock()
        mock_manager.get_secret.return_value = "convenience_secret"
        mock_get_manager.return_value = mock_manager
        
        secret = get_secret("test_key", SecretType.JWT_SECRET)
        
        assert secret == "convenience_secret"
        mock_manager.get_secret.assert_called_once_with("test_key", SecretType.JWT_SECRET)


@pytest.mark.unit
class TestSecretsManagerExceptions:
    """Tests pour gestion d'erreurs des secrets."""
    
    def test_secret_not_found_error(self):
        """Test exception SecretNotFoundError."""
        error = SecretNotFoundError("Secret not found")
        assert str(error) == "Secret not found"
    
    def test_secret_expired_error(self):
        """Test exception SecretExpiredError."""
        error = SecretExpiredError("Secret expired")
        assert str(error) == "Secret expired"
    
    def test_secret_rotation_error(self):
        """Test exception SecretRotationError."""
        error = SecretRotationError("Rotation failed")
        assert str(error) == "Rotation failed"


@pytest.mark.unit
class TestSecretsManagerEnums:
    """Tests pour les numrations."""
    
    def test_secret_type_enum(self):
        """Test numration SecretType."""
        assert SecretType.API_KEY.value == "api_key"
        assert SecretType.DATABASE_PASSWORD.value == "database_password"
        assert SecretType.JWT_SECRET.value == "jwt_secret"
        assert SecretType.ENCRYPTION_KEY.value == "encryption_key"
        assert SecretType.OAUTH_CLIENT_SECRET.value == "oauth_client_secret"
    
    def test_secret_source_enum(self):
        """Test numration SecretSource."""
        assert SecretSource.DOCKER_SECRETS.value == "docker_secrets"
        assert SecretSource.ENVIRONMENT_VARIABLES.value == "environment_variables"
        assert SecretSource.AZURE_KEY_VAULT.value == "azure_key_vault"
        assert SecretSource.HASHICORP_VAULT.value == "hashicorp_vault"
        assert SecretSource.AWS_SECRETS_MANAGER.value == "aws_secrets_manager"
        assert SecretSource.LOCAL_FILE.value == "local_file" 