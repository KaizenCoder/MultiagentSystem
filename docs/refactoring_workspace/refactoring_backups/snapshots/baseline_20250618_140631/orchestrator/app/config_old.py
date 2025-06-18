from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Charge et valide les configurations depuis les variables d'environnement."""
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str
    MEMORY_API_URL: str = "http://memory_api:8001"
    ORCHESTRATOR_API_KEY: str
    
    # Paramtres de scurit
    DEBUG: bool = False
    ENFORCE_HTTPS: bool = False  # False pour dveloppement, True pour production
    MAX_REQUEST_TIMEOUT: float = 30.0
    MAX_LLM_RESPONSE_TIME: float = 120.0
    MAX_CODE_SIZE: int = 50000
    MAX_TASK_DESCRIPTION_LENGTH: int = 5000

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')    @field_validator("ORCHESTRATOR_API_KEY")
    @classmethod
    def key_must_be_set_and_not_default(cls, v: str) -> str:
        if not v or v == "your_secret_key_here":
            raise ValueError("FATAL: ORCHESTRATOR_API_KEY must be set in the .env file.")
        return v
      @field_validator("MEMORY_API_URL")
    @classmethod
    def validate_memory_api_url_config(cls, v: str) -> str:
        # Simple URL validation without circular import
        if not v.startswith(('http://', 'https://')):
            raise ValueError("Memory API URL must start with http:// or https://")
        
        # Check HTTPS enforcement for production
        import os
        enforce_https = os.getenv('ENFORCE_HTTPS', 'false').lower() == 'true'
        
        if enforce_https and not v.startswith('https://'):
            # Exceptions pour le dveloppement local
            if not any(host in v for host in ['localhost', '127.0.0.1', 'memory_api']):
                raise ValueError("HTTPS required for external APIs in production")
        return v

settings = Settings()