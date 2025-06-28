"""
Gestionnaire de secrets production avec rotation automatique et conformit scurit.
Remplace la gestion de secrets hardcods par un systme externalis et scuris.
Supports Azure KeyVault, HashiCorp Vault, Docker Secrets et variables d'environnement.
"""

import os
import time
import json
import base64
import hashlib
import asyncio
from pathlib import Path
from typing import Dict, Optional, Any, List
from enum import Enum
from dataclasses import dataclass
from contextlib import contextmanager
import logging
from abc import ABC, abstractmethod

# Azure KeyVault support
try:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

# HashiCorp Vault support  
try:
    import hvac
    VAULT_AVAILABLE = True
except ImportError:
    VAULT_AVAILABLE = False

logger = logging.getLogger(__name__)


class SecretType(Enum):
    """Types de secrets supports."""
    API_KEY = "api_key"
    DATABASE_PASSWORD = "database_password"
    JWT_SECRET = "jwt_secret"
    ENCRYPTION_KEY = "encryption_key"
    OAUTH_CLIENT_SECRET = "oauth_client_secret"


class SecretSource(Enum):
    """Sources de secrets supportes."""
    DOCKER_SECRETS = "docker_secrets"
    ENVIRONMENT_VARIABLES = "environment_variables"
    AZURE_KEY_VAULT = "azure_key_vault"
    HASHICORP_VAULT = "hashicorp_vault"
    AWS_SECRETS_MANAGER = "aws_secrets_manager"
    LOCAL_FILE = "local_file"  # Dveloppement uniquement


@dataclass
class SecretMetadata:
    """Mtadonnes d'un secret."""
    name: str
    secret_type: SecretType
    source: SecretSource
    created_at: float
    last_accessed: float
    access_count: int
    expires_at: Optional[float] = None
    rotation_interval: Optional[int] = None  # en secondes
    
    def is_expired(self) -> bool:
        """Vrifie si le secret a expir."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def needs_rotation(self) -> bool:
        """Vrifie si le secret doit tre tourn."""
        if self.rotation_interval is None:
            return False
        return time.time() - self.created_at > self.rotation_interval


class SecretNotFoundError(Exception):
    """Exception leve quand un secret n'est pas trouv."""
    pass


class SecretExpiredError(Exception):
    """Exception leve quand un secret a expir."""
    pass


class SecretRotationError(Exception):
    """Exception leve lors d'erreurs de rotation."""
    pass


class SecretProvider(ABC):
    """Interface abstraite pour les fournisseurs de secrets."""
    
    @abstractmethod
    def get_secret(self, secret_name: str) -> str:
        """Rcupre un secret par son nom."""
        pass
    
    @abstractmethod
    def list_secrets(self) -> List[str]:
        """Liste tous les secrets disponibles."""
        pass
    
    @abstractmethod
    def secret_exists(self, secret_name: str) -> bool:
        """Vrifie si un secret existe."""
        pass


class DockerSecretsProvider(SecretProvider):
    """Fournisseur de secrets Docker Swarm."""
    
    def __init__(self, secrets_path: Path = Path("/run/secrets")):
        self.secrets_path = secrets_path
        if not self.secrets_path.exists():
            logger.warning(f"Docker secrets path {secrets_path} does not exist")
    
    def get_secret(self, secret_name: str) -> str:
        """Rcupre un secret Docker."""
        secret_file = self.secrets_path / secret_name
        if not secret_file.exists():
            raise SecretNotFoundError(f"Docker secret {secret_name} not found")
        
        try:
            content = secret_file.read_text().strip()
            if not content:
                raise SecretNotFoundError(f"Docker secret {secret_name} is empty")
            return content
        except Exception as e:
            logger.error(f"Failed to read Docker secret {secret_name}: {e}")
            raise SecretNotFoundError(f"Cannot read Docker secret {secret_name}")
    
    def list_secrets(self) -> List[str]:
        """Liste tous les secrets Docker disponibles."""
        if not self.secrets_path.exists():
            return []
        
        return [f.name for f in self.secrets_path.iterdir() if f.is_file()]
    
    def secret_exists(self, secret_name: str) -> bool:
        """Vrifie si un secret Docker existe."""
        return (self.secrets_path / secret_name).is_file()


class EnvironmentVariablesProvider(SecretProvider):
    """Fournisseur de secrets via variables d'environnement."""
    
    def __init__(self, prefix: str = "SECRET_"):
        self.prefix = prefix
    
    def get_secret(self, secret_name: str) -> str:
        """Rcupre un secret depuis les variables d'environnement."""
        env_var_name = f"{self.prefix}{secret_name.upper()}"
        value = os.getenv(env_var_name)
        
        if value is None:
            raise SecretNotFoundError(f"Environment variable {env_var_name} not found")
        
        if not value.strip():
            raise SecretNotFoundError(f"Environment variable {env_var_name} is empty")
        
        return value.strip()
    
    def list_secrets(self) -> List[str]:
        """Liste tous les secrets dans les variables d'environnement."""
        return [
            key[len(self.prefix):].lower() 
            for key in os.environ.keys() 
            if key.startswith(self.prefix)
        ]
    
    def secret_exists(self, secret_name: str) -> bool:
        """Vrifie si un secret existe dans les variables d'environnement."""
        env_var_name = f"{self.prefix}{secret_name.upper()}"
        return env_var_name in os.environ


class LocalFileProvider(SecretProvider):
    """Fournisseur de secrets via fichiers locaux (dveloppement uniquement)."""
    
    def __init__(self, secrets_dir: Path = Path(".secrets")):
        self.secrets_dir = secrets_dir
        self.secrets_dir.mkdir(exist_ok=True, mode=0o700)  # Permissions restrictives
        
        # Avertissement scurit
        logger.warning("Using LocalFileProvider - FOR DEVELOPMENT ONLY")
    
    def get_secret(self, secret_name: str) -> str:
        """Rcupre un secret depuis un fichier local."""
        secret_file = self.secrets_dir / f"{secret_name}.secret"
        
        if not secret_file.exists():
            raise SecretNotFoundError(f"Local secret file {secret_name}.secret not found")
        
        try:
            content = secret_file.read_text().strip()
            if not content:
                raise SecretNotFoundError(f"Local secret file {secret_name}.secret is empty")
            return content
        except Exception as e:
            logger.error(f"Failed to read local secret {secret_name}: {e}")
            raise SecretNotFoundError(f"Cannot read local secret {secret_name}")
    
    def list_secrets(self) -> List[str]:
        """Liste tous les secrets dans le rpertoire local."""
        if not self.secrets_dir.exists():
            return []        
        return [
            f.stem for f in self.secrets_dir.glob("*.secret")
        ]
    
    def secret_exists(self, secret_name: str) -> bool:
        """Vrifie si un secret existe localement."""
        return (self.secrets_dir / f"{secret_name}.secret").exists()


class AzureKeyVaultProvider(SecretProvider):
    """Fournisseur de secrets Azure KeyVault pour production."""
    
    def __init__(self, vault_url: str, credential: Optional[Any] = None):
        if not AZURE_AVAILABLE:
            raise ImportError("Azure dependencies not available. Install azure-keyvault-secrets and azure-identity")
        
        self.vault_url = vault_url
        self.credential = credential or DefaultAzureCredential()
        self.client = SecretClient(vault_url=vault_url, credential=self.credential)
        
        logger.info(f"Initialized Azure KeyVault provider for {vault_url}")
    
    def get_secret(self, secret_name: str) -> str:
        """Rcupre un secret depuis Azure KeyVault."""
        try:
            secret = self.client.get_secret(secret_name)
            if not secret.value:
                raise SecretNotFoundError(f"Azure KeyVault secret {secret_name} is empty")
            return secret.value
        except Exception as e:
            logger.error(f"Failed to get secret {secret_name} from Azure KeyVault: {e}")
            raise SecretNotFoundError(f"Azure KeyVault secret {secret_name} not found")
    
    def list_secrets(self) -> List[str]:
        """Liste tous les secrets dans Azure KeyVault."""
        try:
            return [secret.name for secret in self.client.list_properties_of_secrets()]
        except Exception as e:
            logger.error(f"Failed to list Azure KeyVault secrets: {e}")
            return []
    
    def secret_exists(self, secret_name: str) -> bool:
        """Vrifie si un secret existe dans Azure KeyVault."""
        try:
            self.client.get_secret(secret_name)
            return True
        except:
            return False


class HashiCorpVaultProvider(SecretProvider):
    """Fournisseur de secrets HashiCorp Vault pour production."""
    
    def __init__(self, vault_url: str, token: str, mount_point: str = "secret"):
        if not VAULT_AVAILABLE:
            raise ImportError("HashiCorp Vault dependencies not available. Install hvac")
        
        self.vault_url = vault_url
        self.mount_point = mount_point
        self.client = hvac.Client(url=vault_url, token=token)
        
        if not self.client.is_authenticated():
            raise ValueError("Failed to authenticate with HashiCorp Vault")
        
        logger.info(f"Initialized HashiCorp Vault provider for {vault_url}")
    
    def get_secret(self, secret_name: str) -> str:
        """Rcupre un secret depuis HashiCorp Vault."""
        try:
            # Support pour KV v2 (default) et v1
            try:
                # KV v2
                response = self.client.secrets.kv.v2.read_secret_version(
                    path=secret_name,
                    mount_point=self.mount_point
                )
                data = response['data']['data']
            except:
                # KV v1 fallback
                response = self.client.secrets.kv.v1.read_secret(
                    path=secret_name,
                    mount_point=self.mount_point
                )
                data = response['data']
            
            # Cherche 'value' ou utilise la premire cl
            if 'value' in data:
                secret_value = data['value']
            else:
                secret_value = next(iter(data.values()))
            
            if not secret_value:
                raise SecretNotFoundError(f"HashiCorp Vault secret {secret_name} is empty")
            
            return secret_value
            
        except Exception as e:
            logger.error(f"Failed to get secret {secret_name} from HashiCorp Vault: {e}")
            raise SecretNotFoundError(f"HashiCorp Vault secret {secret_name} not found")
    
    def list_secrets(self) -> List[str]:
        """Liste tous les secrets dans HashiCorp Vault."""
        try:
            # KV v2
            try:
                response = self.client.secrets.kv.v2.list_secrets(mount_point=self.mount_point)
            except:
                # KV v1 fallback
                response = self.client.secrets.kv.v1.list_secrets(mount_point=self.mount_point)
            
            return response['data']['keys'] if response and 'data' in response else []
            
        except Exception as e:
            logger.error(f"Failed to list HashiCorp Vault secrets: {e}")
            return []
    
    def secret_exists(self, secret_name: str) -> bool:
        """Vrifie si un secret existe dans HashiCorp Vault."""
        try:
            self.get_secret(secret_name)
            return True
        except:
            return False


class ProductionSecretsManager:
    """Gestionnaire de secrets production avec cache et rotation."""
    
    def __init__(
        self, 
        primary_provider: SecretProvider,
        fallback_providers: Optional[List[SecretProvider]] = None,
        cache_ttl: int = 3600,  # 1 heure par dfaut
        enable_rotation: bool = True
    ):
        self.primary_provider = primary_provider
        self.fallback_providers = fallback_providers or []
        self.cache_ttl = cache_ttl
        self.enable_rotation = enable_rotation
        
        # Cache avec mtadonnes
        self._cache: Dict[str, str] = {}
        self._metadata: Dict[str, SecretMetadata] = {}
        
        # Audit trail
        self._access_log: List[Dict[str, Any]] = []
        
        logger.info(f"Initialized ProductionSecretsManager with {type(primary_provider).__name__}")
    
    def get_secret(
        self, 
        secret_name: str, 
        secret_type: SecretType = SecretType.API_KEY,
        force_refresh: bool = False
    ) -> str:
        """
        Rcupre un secret avec cache et audit.
        
        Args:
            secret_name: Nom du secret
            secret_type: Type du secret
            force_refresh: Force le rechargement du cache
            
        Returns:
            str: Valeur du secret
            
        Raises:
            SecretNotFoundError: Si le secret n'existe pas
            SecretExpiredError: Si le secret a expir
        """
        now = time.time()
        
        # Vrification cache et expiration
        if not force_refresh and secret_name in self._cache:
            metadata = self._metadata.get(secret_name)
            if metadata:
                # Vrification expiration
                if metadata.is_expired():
                    logger.warning(f"Secret {secret_name} has expired")
                    raise SecretExpiredError(f"Secret {secret_name} has expired")
                
                # Vrification TTL cache
                if now - metadata.last_accessed < self.cache_ttl:
                    metadata.last_accessed = now
                    metadata.access_count += 1
                    self._log_access(secret_name, "cache_hit", secret_type)
                    return self._cache[secret_name]
        
        # Rcupration du secret
        secret_value = self._fetch_secret(secret_name)
        
        # Mise  jour cache et mtadonnes
        self._cache[secret_name] = secret_value
        self._metadata[secret_name] = SecretMetadata(
            name=secret_name,
            secret_type=secret_type,
            source=SecretSource.DOCKER_SECRETS,  #  adapter selon le provider
            created_at=now,
            last_accessed=now,
            access_count=1
        )
        
        self._log_access(secret_name, "fetched", secret_type)
        
        # Vrification rotation si active
        if self.enable_rotation:
            self._check_rotation_needed(secret_name)
        
        return secret_value
    
    def _fetch_secret(self, secret_name: str) -> str:
        """Rcupre un secret depuis les providers."""
        # Essai provider principal
        try:
            return self.primary_provider.get_secret(secret_name)
        except SecretNotFoundError as e:
            logger.warning(f"Primary provider failed for {secret_name}: {e}")
        
        # Essai providers de fallback
        for provider in self.fallback_providers:
            try:
                logger.info(f"Trying fallback provider {type(provider).__name__} for {secret_name}")
                return provider.get_secret(secret_name)
            except SecretNotFoundError:
                continue
        
        # Aucun provider n'a le secret
        self._log_access(secret_name, "not_found", SecretType.API_KEY)
        raise SecretNotFoundError(f"Secret {secret_name} not found in any provider")
    
    def _check_rotation_needed(self, secret_name: str) -> None:
        """Vrifie si un secret doit tre tourn."""
        metadata = self._metadata.get(secret_name)
        if metadata and metadata.needs_rotation():
            logger.warning(f"Secret {secret_name} needs rotation")
            # TODO: Implmenter logique de rotation automatique
    
    def _log_access(self, secret_name: str, action: str, secret_type: SecretType) -> None:
        """Log l'accs  un secret pour audit."""
        access_entry = {
            'timestamp': time.time(),
            'secret_name': secret_name,
            'secret_type': secret_type.value,
            'action': action,
            'source': 'ProductionSecretsManager'
        }
        
        self._access_log.append(access_entry)
        
        # Gardez seulement les 1000 derniers accs
        if len(self._access_log) > 1000:
            self._access_log = self._access_log[-1000:]
        
        logger.debug(f"Secret access logged: {secret_name} - {action}")
    
    def list_available_secrets(self) -> List[str]:
        """Liste tous les secrets disponibles."""
        all_secrets = set()
        
        # Primary provider
        try:
            all_secrets.update(self.primary_provider.list_secrets())
        except Exception as e:
            logger.warning(f"Failed to list secrets from primary provider: {e}")
        
        # Fallback providers
        for provider in self.fallback_providers:
            try:
                all_secrets.update(provider.list_secrets())
            except Exception as e:
                logger.warning(f"Failed to list secrets from fallback provider: {e}")
        
        return sorted(list(all_secrets))
    
    def clear_cache(self) -> None:
        """Vide le cache des secrets."""
        cache_size = len(self._cache)
        self._cache.clear()
        self._metadata.clear()
        logger.info(f"Cleared secrets cache ({cache_size} entries)")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache."""
        total_accesses = sum(m.access_count for m in self._metadata.values())
        
        return {
            'cached_secrets_count': len(self._cache),
            'total_accesses': total_accesses,
            'cache_hit_ratio': len(self._cache) / max(total_accesses, 1),
            'oldest_secret_age': min(
                (time.time() - m.created_at for m in self._metadata.values()),
                default=0
            ),
            'most_accessed_secret': max(
                self._metadata.items(),
                key=lambda x: x[1].access_count,
                default=('none', None)
            )[0]
        }
    
    def get_audit_trail(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retourne l'audit trail des accs."""
        return self._access_log[-limit:]
    
    @contextmanager
    def secret_context(self, secret_name: str, secret_type: SecretType = SecretType.API_KEY):
        """Context manager pour utilisation scurise des secrets."""
        try:
            secret_value = self.get_secret(secret_name, secret_type)
            yield secret_value
        except Exception as e:
            logger.error(f"Error in secret context for {secret_name}: {e}")
            raise
        finally:
            # Nettoyage mmoire (optionnel)
            pass


# Configuration par dfaut selon l'environnement
def get_default_secrets_manager() -> ProductionSecretsManager:
    """
    Cre un gestionnaire de secrets configur selon l'environnement.
    Production: Azure KeyVault + HashiCorp Vault + Docker Secrets
    Staging: Docker Secrets + Variables d'environnement
    Development: Fichiers locaux + Variables d'environnement
    
    Returns:
        ProductionSecretsManager: Instance configure
    """
    environment = os.getenv('ENVIRONMENT', 'development').lower()
    
    if environment == 'production':
        # Production: Providers enterprise avec fallbacks
        providers = []
        
        # Azure KeyVault (primary si configur)
        azure_vault_url = os.getenv('AZURE_KEYVAULT_URL')
        if azure_vault_url and AZURE_AVAILABLE:
            try:
                providers.append(AzureKeyVaultProvider(azure_vault_url))
                logger.info("Azure KeyVault provider initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Azure KeyVault: {e}")
        
        # HashiCorp Vault (secondary si configur)
        vault_url = os.getenv('VAULT_URL')
        vault_token = os.getenv('VAULT_TOKEN')
        if vault_url and vault_token and VAULT_AVAILABLE:
            try:
                providers.append(HashiCorpVaultProvider(vault_url, vault_token))
                logger.info("HashiCorp Vault provider initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize HashiCorp Vault: {e}")
        
        # Docker Secrets (fallback)
        providers.append(DockerSecretsProvider())
        
        # Variables d'environnement (dernier recours)
        providers.append(EnvironmentVariablesProvider())
        
        if not providers:
            raise ValueError("No secret providers available in production")
        
        primary = providers[0]
        fallbacks = providers[1:] if len(providers) > 1 else []
        cache_ttl = 3600  # 1 heure
        
    elif environment in ['staging', 'testing']:
        # Staging: Docker Secrets avec fallback variables d'environnement
        primary = DockerSecretsProvider()
        fallbacks = [EnvironmentVariablesProvider()]
        cache_ttl = 1800  # 30 minutes
        
    else:
        # Development: Fichiers locaux avec fallback variables d'environnement
        primary = LocalFileProvider()
        fallbacks = [EnvironmentVariablesProvider()]
        cache_ttl = 300  # 5 minutes
    
    return ProductionSecretsManager(
        primary_provider=primary,
        fallback_providers=fallbacks,
        cache_ttl=cache_ttl,
        enable_rotation=(environment == 'production')
    )


# Instance globale
_secrets_manager: Optional[ProductionSecretsManager] = None


def get_secrets_manager() -> ProductionSecretsManager:
    """
    Retourne l'instance globale du gestionnaire de secrets.
    
    Returns:
        ProductionSecretsManager: Instance globale
    """
    global _secrets_manager
    if _secrets_manager is None:
        _secrets_manager = get_default_secrets_manager()
    return _secrets_manager


# Fonctions de convnience
def get_secret(secret_name: str, secret_type: SecretType = SecretType.API_KEY) -> str:
    """Fonction de convnience pour rcuprer un secret."""
    return get_secrets_manager().get_secret(secret_name, secret_type)


def get_openai_api_key() -> str:
    """Rcupre la cl API OpenAI."""
    return get_secret("openai_api_key", SecretType.API_KEY)


def get_anthropic_api_key() -> str:
    """Rcupre la cl API Anthropic."""
    return get_secret("anthropic_api_key", SecretType.API_KEY)


def get_jwt_secret() -> str:
    """Rcupre le secret JWT."""
    return get_secret("jwt_secret", SecretType.JWT_SECRET)


# Validation de scurit
def validate_secret_strength(secret_value: str, secret_type: SecretType) -> bool:
    """
    Valide la force d'un secret selon son type.
    
    Args:
        secret_value: Valeur du secret
        secret_type: Type du secret
        
    Returns:
        bool: True si le secret est suffisamment fort
    """
    if secret_type == SecretType.API_KEY:
        # Cls API: minimum 32 caractres
        return len(secret_value) >= 32
    
    elif secret_type == SecretType.JWT_SECRET:
        # Secrets JWT: minimum 64 caractres, caractres varis
        return (len(secret_value) >= 64 and 
                any(c.isupper() for c in secret_value) and
                any(c.islower() for c in secret_value) and
                any(c.isdigit() for c in secret_value))
    
    elif secret_type == SecretType.DATABASE_PASSWORD:
        # Mots de passe DB: minimum 16 caractres avec caractres spciaux
        return (len(secret_value) >= 16 and
                any(c in "!@#$%^&*" for c in secret_value))
    
    else:
        # Par dfaut: minimum 16 caractres
        return len(secret_value) >= 16
