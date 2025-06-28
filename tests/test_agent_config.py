"""
Tests pour la configuration Pydantic Agent Factory
Gnr par Agent 03 - Spcialiste Configuration
"""

import pytest
import os
from unittest.mock import patch, mock_open
from pathlib import Path
import tempfile
import json

from agent_config import (
    AgentFactoryConfig,
    ConfigurationManager,
    Environment,
    LogLevel,
    EnvironmentConfig,
    CacheConfig,
    SecurityConfig,
    MonitoringConfig
)

class TestAgentFactoryConfig:
    """Tests pour la configuration principale"""
    
    def setup_method(self):
        """Setup pour chaque test"""
        self.config_manager = ConfigurationManager()
    
    def test_environment_config_validation(self):
        """Test validation configuration environnement"""
        # Configuration valide
        env_config = EnvironmentConfig(
            ttl_seconds=300,
            cache_max_size=500,
            thread_pool_size=4,
            hot_reload=True,
            debug=False,
            log_level=LogLevel.INFO
        )
        assert env_config.ttl_seconds == 300
        assert env_config.log_level == LogLevel.INFO
    
    def test_thread_pool_size_validation(self):
        """Test validation taille pool threads"""
        with patch('os.cpu_count', return_value=4):
            # Taille valide
            env_config = EnvironmentConfig(
                ttl_seconds=300,
                cache_max_size=500,
                thread_pool_size=6,
                hot_reload=True,
                debug=False,
                log_level=LogLevel.INFO
            )
            assert env_config.thread_pool_size == 6
            
            # Taille trop leve (doit tre ajuste)
            env_config = EnvironmentConfig(
                ttl_seconds=300,
                cache_max_size=500,
                thread_pool_size=20,
                hot_reload=True,
                debug=False,
                log_level=LogLevel.INFO
            )
            assert env_config.thread_pool_size == 8  # CPU * 2
    
    def test_cache_config_validation(self):
        """Test validation configuration cache"""
        cache_config = CacheConfig(
            lru_enabled=True,
            max_memory_mb=256,
            cleanup_interval=300,
            compression_enabled=True
        )
        assert cache_config.lru_enabled is True
        assert cache_config.max_memory_mb == 256
    
    def test_security_config_defaults(self):
        """Test configuration scurit par dfaut"""
        security_config = SecurityConfig()
        assert security_config.signature_required is True
        assert security_config.rsa_key_size == 2048
        assert security_config.hash_algorithm == "SHA-256"
    
    def test_full_config_validation(self):
        """Test validation configuration complte"""
        config_dict = {
            "name": "test_config",
            "version": "1.0.0",
            "description": "Test configuration",
            "created_at": "2024-12-19T14:00:00",
            "agent_creator": "Agent 03",
            "environments": {
                Environment.DEVELOPMENT: {
                    "ttl_seconds": 60,
                    "cache_max_size": 100,
                    "thread_pool_size": 2,
                    "hot_reload": True,
                    "debug": True,
                    "log_level": LogLevel.DEBUG
                },
                Environment.STAGING: {
                    "ttl_seconds": 300,
                    "cache_max_size": 500,
                    "thread_pool_size": 4,
                    "hot_reload": True,
                    "debug": False,
                    "log_level": LogLevel.INFO
                },
                Environment.PRODUCTION: {
                    "ttl_seconds": 600,
                    "cache_max_size": 1000,
                    "thread_pool_size": 8,
                    "hot_reload": False,
                    "debug": False,
                    "log_level": LogLevel.WARNING
                }
            },
            "cache": {
                "lru_enabled": True,
                "max_memory_mb": 256,
                "cleanup_interval": 300,
                "compression_enabled": True
            },
            "security": {},
            "monitoring": {}
        }
        
        config = AgentFactoryConfig(**config_dict)
        assert config.name == "test_config"
        assert len(config.environments) == 3
    
    @patch.dict(os.environ, {'ENVIRONMENT': 'production'})
    def test_get_environment_config(self):
        """Test rcupration configuration environnement"""
        config_dict = self._get_test_config_dict()
        config = AgentFactoryConfig(**config_dict)
        
        env_config = config.get_environment_config()
        assert env_config.ttl_seconds == 600  # Production TTL
        assert env_config.debug is False
    
    @patch.dict(os.environ, {'ENVIRONMENT': 'development'})
    def test_get_cache_ttl(self):
        """Test rcupration TTL cache"""
        config_dict = self._get_test_config_dict()
        config = AgentFactoryConfig(**config_dict)
        
        ttl = config.get_cache_ttl()
        assert ttl == 60  # Development TTL
    
    def test_configuration_manager_singleton(self):
        """Test pattern singleton ConfigurationManager"""
        manager1 = ConfigurationManager()
        manager2 = ConfigurationManager()
        assert manager1 is manager2
    
    def test_configuration_manager_load_config(self):
        """Test chargement configuration"""
        config_dict = self._get_test_config_dict()
        manager = ConfigurationManager()
        
        config = manager.load_config(config_dict)
        assert config is not None
        assert manager.is_configured() is True
        
        retrieved_config = manager.get_config()
        assert retrieved_config is config
    
    def _get_test_config_dict(self):
        """Configuration de test standard"""
        return {
            "name": "test_config",
            "version": "1.0.0",
            "description": "Test configuration",
            "created_at": "2024-12-19T14:00:00",
            "agent_creator": "Agent 03",
            "environments": {
                Environment.DEVELOPMENT: {
                    "ttl_seconds": 60,
                    "cache_max_size": 100,
                    "thread_pool_size": 2,
                    "hot_reload": True,
                    "debug": True,
                    "log_level": LogLevel.DEBUG
                },
                Environment.STAGING: {
                    "ttl_seconds": 300,
                    "cache_max_size": 500,
                    "thread_pool_size": 4,
                    "hot_reload": True,
                    "debug": False,
                    "log_level": LogLevel.INFO
                },
                Environment.PRODUCTION: {
                    "ttl_seconds": 600,
                    "cache_max_size": 1000,
                    "thread_pool_size": 8,
                    "hot_reload": False,
                    "debug": False,
                    "log_level": LogLevel.WARNING
                }
            },
            "cache": {
                "lru_enabled": True,
                "max_memory_mb": 256,
                "cleanup_interval": 300,
                "compression_enabled": True
            },
            "security": {},
            "monitoring": {}
        }

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
