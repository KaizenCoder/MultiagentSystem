from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import hashlib
import jwt
import asyncio
from datetime import datetime, timedelta
import re

# === Modèle de Sécurité ===

class SecurityLevel(Enum):
    """Niveaux de sécurité pour les agents"""
    PUBLIC = "public"          # Accès sans restriction
    INTERNAL = "internal"      # Accès interne uniquement
    RESTRICTED = "restricted"  # Accès avec permissions spécifiques
    CRITICAL = "critical"      # Accès hautement sécurisé

@dataclass
class SecurityPolicy:
    """Politique de sécurité pour un agent"""
    level: SecurityLevel
    allowed_domains: List[str]
    rate_limit: int  # Requêtes par minute
    max_resource_usage: Dict[str, Any]
    data_retention_days: int
    encryption_required: bool = True
    audit_enabled: bool = True

# === Validation et Sandboxing ===

class TemplateValidator:
    """Validateur de templates avec règles de sécurité"""
    
    DANGEROUS_PATTERNS = [
        r"eval\s*\(",
        r"exec\s*\(",
        r"__import__",
        r"subprocess",
        r"os\.",
        r"sys\.",
    ]
    
    def validate_template(self, template: Dict[str, Any]) -> bool:
        """Valide un template contre les règles de sécurité"""
        # Vérification de la structure
        if not self._validate_structure(template):
            return False
        
        # Vérification des patterns dangereux
        template_str = str(template)
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, template_str):
                raise SecurityError(f"Dangerous pattern detected: {pattern}")
        
        # Validation des ressources
        if not self._validate_resource_limits(template):
            return False
        
        return True
    
    def _validate_structure(self, template: Dict[str, Any]) -> bool:
        """Vérifie la structure du template"""
        required_fields = ["name", "role", "domain", "security_policy"]
        return all(field in template for field in required_fields)
    
    def _validate_resource_limits(self, template: Dict[str, Any]) -> bool:
        """Valide les limites de ressources"""
        if "resource_limits" in template:
            limits = template["resource_limits"]
            max_memory = limits.get("memory_mb", 0)
            max_cpu = limits.get("cpu_percent", 0)
            
            if max_memory > 4096 or max_cpu > 80:
                raise ValueError("Resource limits exceed maximum allowed")
        
        return True

class AgentSandbox:
    """Environnement d'exécution isolé pour les agents"""
    
    def __init__(self, agent_id: str, security_policy: SecurityPolicy):
        self.agent_id = agent_id
        self.security_policy = security_policy
        self.resource_monitor = ResourceMonitor()
    
    async def execute_in_sandbox(self, func, *args, **kwargs):
        """Exécute une fonction dans le sandbox avec limitations"""
        # Vérification des permissions
        if not self._check_permissions():
            raise PermissionError("Agent lacks required permissions")
        
        # Rate limiting
        if not await self._check_rate_limit():
            raise RateLimitError("Rate limit exceeded")
        
        # Monitoring des ressources
        with self.resource_monitor.track(self.agent_id):
            # Timeout basé sur la politique
            timeout = self.security_policy.max_resource_usage.get("timeout_seconds", 300)
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
            except asyncio.TimeoutError:
                raise TimeoutError(f"Agent execution exceeded {timeout}s timeout")
    
    def _check_permissions(self) -> bool:
        """Vérifie les permissions de l'agent"""
        # Implémentation simplifiée
        return True
    
    async def _check_rate_limit(self) -> bool:
        """Vérifie le rate limit"""
        # Implémentation avec Redis en production
        return True

# === Authentication et Authorization ===

class AgentAuthManager:
    """Gestionnaire d'authentification pour les agents"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.token_expiry = timedelta(hours=24)
    
    def generate_agent_token(self, agent_id: str, permissions: List[str]) -> str:
        """Génère un token JWT pour un agent"""
        payload = {
            "agent_id": agent_id,
            "permissions": permissions,
            "exp": datetime.utcnow() + self.token_expiry,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    def verify_agent_token(self, token: str) -> Dict[str, Any]:
        """Vérifie et décode un token d'agent"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")

class RBACManager:
    """Role-Based Access Control pour les agents"""
    
    def __init__(self):
        self.roles = {
            "admin": ["*"],  # Toutes permissions
            "developer": ["create_agent", "modify_agent", "view_metrics"],
            "operator": ["view_agent", "execute_agent", "view_metrics"],
            "viewer": ["view_agent", "view_metrics"]
        }
        self.user_roles = {}
    
    def check_permission(self, user_id: str, action: str) -> bool:
        """Vérifie si un utilisateur a la permission pour une action"""
        user_role = self.user_roles.get(user_id)
        if not user_role:
            return False
        
        role_permissions = self.roles.get(user_role, [])
        return action in role_permissions or "*" in role_permissions

# === Audit et Compliance ===

@dataclass
class AuditEvent:
    """Événement d'audit"""
    timestamp: datetime
    agent_id: str
    user_id: Optional[str]
    action: str
    resource: str
    result: str
    metadata: Dict[str, Any]

class AuditLogger:
    """Logger d'audit pour conformité"""
    
    def __init__(self, retention_days: int = 90):
        self.retention_days = retention_days
        self.events: List[AuditEvent] = []
    
    async def log_event(
        self,
        agent_id: str,
        action: str,
        resource: str,
        result: str,
        user_id: Optional[str] = None,
        metadata: Dict[str, Any] = None
    ):
        """Enregistre un événement d'audit"""
        event = AuditEvent(
            timestamp=datetime.utcnow(),
            agent_id=agent_id,
            user_id=user_id,
            action=action,
            resource=resource,
            result=result,
            metadata=metadata or {}
        )
        
        # En production : stocker dans une base de données
        self.events.append(event)
        
        # Alertes pour événements critiques
        if action in ["security_violation", "unauthorized_access"]:
            await self._send_security_alert(event)
    
    async def _send_security_alert(self, event: AuditEvent):
        """Envoie une alerte de sécurité"""
        # Implémentation avec système d'alerting
        pass

# === Resource Monitoring ===

class ResourceMonitor:
    """Moniteur de ressources pour prévenir les abus"""
    
    def __init__(self):
        self.agent_resources = {}
        self.alerts_threshold = {
            "memory_mb": 1024,
            "cpu_percent": 50,
            "disk_io_mb": 100,
            "network_mb": 50
        }
    
    def track(self, agent_id: str):
        """Context manager pour tracker l'utilisation des ressources"""
        return self._ResourceContext(self, agent_id)
    
    class _ResourceContext:
        def __init__(self, monitor, agent_id):
            self.monitor = monitor
            self.agent_id = agent_id
            self.start_metrics = None
        
        async def __aenter__(self):
            self.start_metrics = await self._get_current_metrics()
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            end_metrics = await self._get_current_metrics()
            usage = self._calculate_usage(self.start_metrics, end_metrics)
            
            # Vérifier les seuils
            for resource, value in usage.items():
                if value > self.monitor.alerts_threshold.get(resource, float('inf')):
                    await self.monitor._trigger_alert(self.agent_id, resource, value)
        
        async def _get_current_metrics(self) -> Dict[str, float]:
            """Obtient les métriques actuelles (simplifié)"""
            # En production : utiliser psutil ou prometheus
            return {
                "memory_mb": 512.0,
                "cpu_percent": 25.0,
                "disk_io_mb": 10.0,
                "network_mb": 5.0
            }
        
        def _calculate_usage(self, start: Dict, end: Dict) -> Dict[str, float]:
            """Calcule l'utilisation des ressources"""
            return {k: end[k] - start.get(k, 0) for k in end}
    
    async def _trigger_alert(self, agent_id: str, resource: str, value: float):
        """Déclenche une alerte pour utilisation excessive"""
        print(f"ALERT: Agent {agent_id} exceeded {resource} limit: {value}")

# === Data Protection ===

class DataProtectionManager:
    """Gestionnaire de protection des données"""
    
    def __init__(self, encryption_key: bytes):
        self.encryption_key = encryption_key
        self.sensitive_fields = [
            "password", "token", "api_key", "secret",
            "ssn", "credit_card", "email", "phone"
        ]
    
    def sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Nettoie les données sensibles"""
        sanitized = {}
        for key, value in data.items():
            if self._is_sensitive_field(key):
                sanitized[key] = self._mask_value(value)
            elif isinstance(value, dict):
                sanitized[key] = self.sanitize_data(value)
            else:
                sanitized[key] = value
        return sanitized
    
    def _is_sensitive_field(self, field_name: str) -> bool:
        """Vérifie si un champ est sensible"""
        field_lower = field_name.lower()
        return any(sensitive in field_lower for sensitive in self.sensitive_fields)
    
    def _mask_value(self, value: Any) -> str:
        """Masque une valeur sensible"""
        if isinstance(value, str):
            if len(value) > 4:
                return value[:2] + "*" * (len(value) - 4) + value[-2:]
            else:
                return "*" * len(value)
        return "***REDACTED***"
    
    def encrypt_sensitive_data(self, data: bytes) -> bytes:
        """Chiffre les données sensibles"""
        # Utiliser cryptography.fernet en production
        return hashlib.sha256(data + self.encryption_key).digest()

# === Secure Agent Factory ===

class SecureAgentFactory(AgentFactory):
    """Factory sécurisé avec toutes les protections"""
    
    def __init__(
        self,
        registry: AgentRegistry,
        auth_manager: AgentAuthManager,
        rbac_manager: RBACManager,
        audit_logger: AuditLogger
    ):
        super().__init__(registry)
        self.auth_manager = auth_manager
        self.rbac_manager = rbac_manager
        self.audit_logger = audit_logger
        self.template_validator = TemplateValidator()
        self.data_protection = DataProtectionManager(b"secret_key")
    
    async def create_agent(
        self,
        template_name: str,
        config: Dict[str, Any] = None,
        user_id: str = None,
        auth_token: str = None
    ) -> BaseAgent:
        """Création sécurisée d'agent avec authentification"""
        
        # Vérification de l'authentification
        if auth_token:
            token_data = self.auth_manager.verify_agent_token(auth_token)
            user_id = token_data.get("user_id", user_id)
        
        # Vérification des permissions
        if not self.rbac_manager.check_permission(user_id, "create_agent"):
            await self.audit_logger.log_event(
                agent_id="N/A",
                action="unauthorized_create_attempt",
                resource=template_name,
                result="denied",
                user_id=user_id
            )
            raise PermissionError("User lacks permission to create agents")
        
        # Validation du template
        template = self.registry.get_template(template_name)
        if not self.template_validator.validate_template(template):
            raise ValueError("Template validation failed")
        
        # Sanitisation de la configuration
        if config:
            config = self.data_protection.sanitize_data(config)
        
        # Création de l'agent avec sandbox
        agent = await super().create_agent(template_name, config)
        
        # Configuration de la sécurité
        security_policy = SecurityPolicy(
            level=SecurityLevel(template.get("security_level", "internal")),
            allowed_domains=template.get("allowed_domains", []),
            rate_limit=template.get("rate_limit", 100),
            max_resource_usage=template.get("resource_limits", {}),
            data_retention_days=template.get("data_retention_days", 30)
        )
        
        agent.sandbox = AgentSandbox(agent.metadata.id, security_policy)
        
        # Audit de la création
        await self.audit_logger.log_event(
            agent_id=agent.metadata.id,
            action="agent_created",
            resource=template_name,
            result="success",
            user_id=user_id,
            metadata={"config": config}
        )
        
        return agent

# === Security Exceptions ===

class SecurityError(Exception):
    """Erreur de sécurité générique"""
    pass

class AuthenticationError(SecurityError):
    """Erreur d'authentification"""
    pass

class PermissionError(SecurityError):
    """Erreur de permission"""
    pass

class RateLimitError(SecurityError):
    """Erreur de rate limiting"""
    pass

# === Configuration de Sécurité ===

class SecurityConfig:
    """Configuration centralisée de sécurité"""
    
    # Limites par défaut
    DEFAULT_RATE_LIMIT = 100  # requêtes/minute
    DEFAULT_TIMEOUT = 300     # secondes
    DEFAULT_MAX_MEMORY = 1024 # MB
    DEFAULT_MAX_CPU = 50      # %
    
    # Politiques par domaine
    DOMAIN_POLICIES = {
        "public": {
            "rate_limit": 50,
            "timeout": 60,
            "max_memory": 512,
            "allowed_tools": ["basic_analysis"]
        },
        "internal": {
            "rate_limit": 200,
            "timeout": 300,
            "max_memory": 2048,
            "allowed_tools": ["analysis", "generation", "transformation"]
        },
        "critical": {
            "rate_limit": 500,
            "timeout": 600,
            "max_memory": 4096,
            "allowed_tools": ["*"],
            "require_mfa": True
        }
    }
    
    @classmethod
    def get_policy_for_domain(cls, domain: str) -> Dict[str, Any]:
        """Retourne la politique de sécurité pour un domaine"""
        return cls.DOMAIN_POLICIES.get(domain, cls.DOMAIN_POLICIES["internal"])

# === Exemple d'utilisation sécurisée ===

async def secure_usage_example():
    """Exemple d'utilisation avec toutes les protections"""
    
    # Initialisation des composants de sécurité
    auth_manager = AgentAuthManager("super_secret_key")
    rbac_manager = RBACManager()
    audit_logger = AuditLogger()
    
    # Configuration RBAC
    rbac_manager.user_roles["admin_user"] = "admin"
    rbac_manager.user_roles["dev_user"] = "developer"
    
    # Création du factory sécurisé
    registry = AgentRegistry()
    secure_factory = SecureAgentFactory(
        registry, auth_manager, rbac_manager, audit_logger
    )
    
    # Template sécurisé
    secure_template = {
        "name": "secure_processor",
        "role": "processor",
        "domain": "data_processing",
        "security_level": "internal",
        "security_policy": {
            "level": "internal",
            "allowed_domains": ["internal.company.com"],
            "rate_limit": 100,
            "max_resource_usage": {
                "memory_mb": 1024,
                "cpu_percent": 50,
                "timeout_seconds": 300
            },
            "data_retention_days": 30
        },
        "capabilities": ["analysis", "transformation"],
        "resource_limits": {
            "memory_mb": 1024,
            "cpu_percent": 50
        }
    }
    
    registry.register_template("secure_processor", secure_template)
    
    # Génération de token pour l'utilisateur
    user_token = auth_manager.generate_agent_token(
        "dev_user",
        ["create_agent", "execute_agent"]
    )
    
    try:
        # Création sécurisée d'un agent
        agent = await secure_factory.create_agent(
            "secure_processor",
            config={"processing_mode": "batch"},
            user_id="dev_user",
            auth_token=user_token
        )
        
        # Exécution dans le sandbox
        result = await agent.sandbox.execute_in_sandbox(
            agent.process,
            {"data": "sensitive information"},
            {"context": "secure_processing"}
        )
        
        print(f"Processing result: {result}")
        
    except PermissionError as e:
        print(f"Permission denied: {e}")
    except SecurityError as e:
        print(f"Security error: {e}")
    
    # Affichage des événements d'audit
    for event in audit_logger.events:
        print(f"Audit: {event.timestamp} - {event.action} by {event.user_id}")

if __name__ == "__main__":
    asyncio.run(secure_usage_example())