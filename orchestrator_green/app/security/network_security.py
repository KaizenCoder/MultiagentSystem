"""
Configuration réseau de sécurité production
VPC, Security Groups, WAF, et DDoS protection
"""
import os
import ipaddress
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

from orchestrator.app.security.logging import security_logger


class SecurityLevel(Enum):
    """Niveaux de sécurité réseau"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class ProtocolType(Enum):
    """Types de protocole réseau"""
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    HTTP = "http"
    HTTPS = "https"


@dataclass
class NetworkRule:
    """Règle de sécurité réseau"""
    name: str
    protocol: ProtocolType
    port_range: str  # "80" ou "80-90"
    source_cidr: str
    description: str
    action: str = "ALLOW"  # ALLOW, DENY, LOG
    priority: int = 100


@dataclass
class SecurityGroup:
    """Groupe de sécurité avec règles"""
    name: str
    description: str
    vpc_id: str
    inbound_rules: List[NetworkRule]
    outbound_rules: List[NetworkRule]
    tags: Dict[str, str]


class NetworkSecurityManager:
    """
    Gestionnaire de sécurité réseau production-ready
    
    Features:
    - VPC et subnets privés
    - Security groups restrictifs
    - WAF anti-OWASP Top 10
    - Rate limiting avancé
    - DDoS protection
    - Network monitoring
    """
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.DEVELOPMENT):
        self.security_level = security_level
        self.security_groups: Dict[str, SecurityGroup] = {}
        self.waf_rules: List[Dict[str, Any]] = []
        self.rate_limits: Dict[str, Dict[str, Any]] = {}
        self.blocked_ips: set = set()
        self.monitored_endpoints: Dict[str, Dict[str, Any]] = {}
        
        # Configuration par environnement
        self._configure_for_environment()
        
        security_logger.log_security_event("NETWORK_SECURITY_INIT", {
            "security_level": security_level.value,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def _configure_for_environment(self):
        """Configure la sécurité selon l'environnement"""
        if self.security_level == SecurityLevel.PRODUCTION:
            self._setup_production_security()
        elif self.security_level == SecurityLevel.STAGING:
            self._setup_staging_security()
        else:
            self._setup_development_security()
    
    def _setup_production_security(self):
        """Configuration sécurité production"""
        # Security Groups production
        self.security_groups = {
            "orchestrator": SecurityGroup(
                name="orchestrator-prod-sg",
                description="Production security group for orchestrator",
                vpc_id="vpc-prod-001",
                inbound_rules=[
                    NetworkRule(
                        name="https-from-alb",
                        protocol=ProtocolType.HTTPS,
                        port_range="443",
                        source_cidr="10.0.1.0/24",  # ALB subnet
                        description="HTTPS from Application Load Balancer only"
                    ),
                    NetworkRule(
                        name="health-check",
                        protocol=ProtocolType.HTTP,
                        port_range="8000",
                        source_cidr="10.0.1.0/24",  # ALB subnet
                        description="Health check from ALB"
                    )
                ],
                outbound_rules=[
                    NetworkRule(
                        name="https-to-external",
                        protocol=ProtocolType.HTTPS,
                        port_range="443",
                        source_cidr="0.0.0.0/0",
                        description="HTTPS to external APIs (OpenAI, Anthropic)"
                    ),
                    NetworkRule(
                        name="postgres-to-rds",
                        protocol=ProtocolType.TCP,
                        port_range="5432",
                        source_cidr="10.0.3.0/24",  # Database subnet
                        description="PostgreSQL to RDS"
                    ),
                    NetworkRule(
                        name="redis-to-elasticache",
                        protocol=ProtocolType.TCP,
                        port_range="6379",
                        source_cidr="10.0.3.0/24",  # Cache subnet
                        description="Redis to ElastiCache"
                    )
                ],
                tags={
                    "Environment": "production",
                    "Component": "orchestrator",
                    "Security": "high"
                }
            ),
            "memory-api": SecurityGroup(
                name="memory-api-prod-sg",
                description="Production security group for memory API",
                vpc_id="vpc-prod-001",
                inbound_rules=[
                    NetworkRule(
                        name="http-from-orchestrator",
                        protocol=ProtocolType.HTTP,
                        port_range="8001",
                        source_cidr="10.0.2.0/24",  # Orchestrator subnet
                        description="HTTP from orchestrator only"
                    )
                ],
                outbound_rules=[
                    NetworkRule(
                        name="postgres-to-rds",
                        protocol=ProtocolType.TCP,
                        port_range="5432",
                        source_cidr="10.0.3.0/24",
                        description="PostgreSQL to RDS"
                    ),
                    NetworkRule(
                        name="chromadb-access",
                        protocol=ProtocolType.HTTP,
                        port_range="8000",
                        source_cidr="10.0.3.0/24",
                        description="ChromaDB access"
                    )
                ],
                tags={
                    "Environment": "production",
                    "Component": "memory-api",
                    "Security": "high"
                }
            ),
            "database": SecurityGroup(
                name="database-prod-sg",
                description="Production security group for databases",
                vpc_id="vpc-prod-001",
                inbound_rules=[
                    NetworkRule(
                        name="postgres-from-apps",
                        protocol=ProtocolType.TCP,
                        port_range="5432",
                        source_cidr="10.0.2.0/23",  # App subnets
                        description="PostgreSQL from application layer"
                    ),
                    NetworkRule(
                        name="redis-from-apps",
                        protocol=ProtocolType.TCP,
                        port_range="6379",
                        source_cidr="10.0.2.0/23",
                        description="Redis from application layer"
                    )
                ],
                outbound_rules=[],  # No outbound for database layer
                tags={
                    "Environment": "production",
                    "Component": "database",
                    "Security": "high"
                }
            )
        }
        
        # WAF Rules anti-OWASP Top 10
        self.waf_rules = self._get_production_waf_rules()
        
        # Rate limiting strict
        self.rate_limits = {
            "global": {"requests_per_minute": 1000, "burst": 100},
            "per_ip": {"requests_per_minute": 60, "burst": 10},
            "api_key": {"requests_per_minute": 300, "burst": 30}
        }
    
    def _setup_staging_security(self):
        """Configuration sécurité staging"""
        # Security Groups moins restrictifs pour les tests
        self.security_groups = {
            "orchestrator": SecurityGroup(
                name="orchestrator-staging-sg",
                description="Staging security group for orchestrator",
                vpc_id="vpc-staging-001",
                inbound_rules=[
                    NetworkRule(
                        name="https-public",
                        protocol=ProtocolType.HTTPS,
                        port_range="443",
                        source_cidr="0.0.0.0/0",
                        description="HTTPS from anywhere (staging)"
                    ),
                    NetworkRule(
                        name="http-public",
                        protocol=ProtocolType.HTTP,
                        port_range="8000",
                        source_cidr="0.0.0.0/0",
                        description="HTTP from anywhere (staging)"
                    )
                ],
                outbound_rules=[
                    NetworkRule(
                        name="all-outbound",
                        protocol=ProtocolType.TCP,
                        port_range="1-65535",
                        source_cidr="0.0.0.0/0",
                        description="All outbound (staging)"
                    )
                ],
                tags={
                    "Environment": "staging",
                    "Component": "orchestrator"
                }
            )
        }
        
        self.waf_rules = self._get_basic_waf_rules()
        self.rate_limits = {
            "global": {"requests_per_minute": 2000, "burst": 200},
            "per_ip": {"requests_per_minute": 120, "burst": 20}
        }
    
    def _setup_development_security(self):
        """Configuration sécurité développement"""
        # Très permissif pour le développement
        self.security_groups = {
            "all": SecurityGroup(
                name="development-sg",
                description="Development security group (permissive)",
                vpc_id="vpc-dev-001",
                inbound_rules=[
                    NetworkRule(
                        name="all-inbound",
                        protocol=ProtocolType.TCP,
                        port_range="1-65535",
                        source_cidr="0.0.0.0/0",
                        description="All inbound (development only)"
                    )
                ],
                outbound_rules=[
                    NetworkRule(
                        name="all-outbound",
                        protocol=ProtocolType.TCP,
                        port_range="1-65535",
                        source_cidr="0.0.0.0/0",
                        description="All outbound (development only)"
                    )
                ],
                tags={
                    "Environment": "development",
                    "Warning": "permissive-rules"
                }
            )
        }
        
        self.waf_rules = []  # Pas de WAF en dev
        self.rate_limits = {
            "global": {"requests_per_minute": 10000, "burst": 1000}
        }
    
    def _get_production_waf_rules(self) -> List[Dict[str, Any]]:
        """Règles WAF anti-OWASP Top 10 pour production"""
        return [
            {
                "name": "SQLInjectionRule",
                "description": "Block SQL injection attempts",
                "priority": 1,
                "action": "BLOCK",
                "statement": {
                    "sqli_match_statement": {
                        "field_to_match": {"all_query_arguments": {}},
                        "text_transformations": [
                            {"priority": 1, "type": "URL_DECODE"},
                            {"priority": 2, "type": "HTML_ENTITY_DECODE"}
                        ]
                    }
                }
            },
            {
                "name": "XSSRule",
                "description": "Block XSS attempts",
                "priority": 2,
                "action": "BLOCK",
                "statement": {
                    "xss_match_statement": {
                        "field_to_match": {"all_query_arguments": {}},
                        "text_transformations": [
                            {"priority": 1, "type": "URL_DECODE"},
                            {"priority": 2, "type": "HTML_ENTITY_DECODE"}
                        ]
                    }
                }
            },
            {
                "name": "RateLimitRule",
                "description": "Rate limiting per IP",
                "priority": 3,
                "action": "BLOCK",
                "statement": {
                    "rate_based_statement": {
                        "limit": 2000,
                        "aggregate_key_type": "IP",
                        "scope_down_statement": {
                            "geo_match_statement": {
                                "country_codes": ["US", "CA", "EU", "FR", "GB", "DE"]
                            }
                        }
                    }
                }
            },
            {
                "name": "SizeRestrictionRule",
                "description": "Block oversized requests",
                "priority": 4,
                "action": "BLOCK",
                "statement": {
                    "size_constraint_statement": {
                        "field_to_match": {"body": {}},
                        "comparison_operator": "GT",
                        "size": 1048576,  # 1MB
                        "text_transformations": [{"priority": 1, "type": "NONE"}]
                    }
                }
            },
            {
                "name": "BlockBadBots",
                "description": "Block known bad bots",
                "priority": 5,
                "action": "BLOCK",
                "statement": {
                    "byte_match_statement": {
                        "search_string": "badbot|scanner|crawler",
                        "field_to_match": {"single_header": {"name": "user-agent"}},
                        "text_transformations": [{"priority": 1, "type": "LOWERCASE"}],
                        "positional_constraint": "CONTAINS"
                    }
                }
            }
        ]
    
    def _get_basic_waf_rules(self) -> List[Dict[str, Any]]:
        """Règles WAF basiques pour staging"""
        return [
            {
                "name": "BasicRateLimit",
                "description": "Basic rate limiting",
                "priority": 1,
                "action": "BLOCK",
                "statement": {
                    "rate_based_statement": {
                        "limit": 5000,
                        "aggregate_key_type": "IP"
                    }
                }
            }
        ]
    
    def validate_network_access(
        self, 
        source_ip: str, 
        destination_port: int, 
        protocol: str = "tcp"
    ) -> Tuple[bool, str]:
        """
        Valide l'accès réseau selon les security groups
        
        Args:
            source_ip: IP source
            destination_port: Port de destination
            protocol: Protocole (tcp, udp, etc.)
            
        Returns:
            Tuple[bool, str]: (autorisé, raison)
        """
        # Vérification IP bloquée
        if source_ip in self.blocked_ips:
            security_logger.log_security_event("NETWORK_ACCESS_BLOCKED", {
                "source_ip": source_ip,
                "reason": "blocked_ip",
                "port": destination_port
            })
            return False, "IP blocked"
        
        # Vérification rate limiting
        if not self._check_rate_limit(source_ip):
            security_logger.log_security_event("NETWORK_ACCESS_RATE_LIMITED", {
                "source_ip": source_ip,
                "port": destination_port
            })
            return False, "Rate limit exceeded"
        
        # Vérification security groups
        for sg_name, sg in self.security_groups.items():
            for rule in sg.inbound_rules:
                if self._rule_matches(rule, source_ip, destination_port, protocol):
                    if rule.action == "ALLOW":
                        security_logger.log_security_event("NETWORK_ACCESS_ALLOWED", {
                            "source_ip": source_ip,
                            "port": destination_port,
                            "security_group": sg_name,
                            "rule": rule.name
                        })
                        return True, f"Allowed by {rule.name}"
                    else:
                        security_logger.log_security_event("NETWORK_ACCESS_DENIED", {
                            "source_ip": source_ip,
                            "port": destination_port,
                            "security_group": sg_name,
                            "rule": rule.name
                        })
                        return False, f"Denied by {rule.name}"
        
        # Pas de règle trouvée = refus par défaut
        security_logger.log_security_event("NETWORK_ACCESS_DEFAULT_DENY", {
            "source_ip": source_ip,
            "port": destination_port
        })
        return False, "Default deny"
    
    def _rule_matches(
        self, 
        rule: NetworkRule, 
        source_ip: str, 
        port: int, 
        protocol: str
    ) -> bool:
        """Vérifie si une règle correspond à la requête"""
        # Vérification protocole
        if rule.protocol.value != protocol and rule.protocol.value not in ["tcp", "udp"]:
            return False
        
        # Vérification port
        if "-" in rule.port_range:
            start_port, end_port = map(int, rule.port_range.split("-"))
            if not (start_port <= port <= end_port):
                return False
        else:
            if int(rule.port_range) != port:
                return False
        
        # Vérification CIDR
        try:
            network = ipaddress.ip_network(rule.source_cidr)
            source = ipaddress.ip_address(source_ip)
            return source in network
        except:
            return False
    
    def _check_rate_limit(self, source_ip: str) -> bool:
        """Vérifie les limites de taux pour une IP"""
        current_time = datetime.utcnow()
        
        # Simulation simple - en production, utiliser Redis
        # pour un tracking distribué
        if not hasattr(self, '_rate_tracking'):
            self._rate_tracking = {}
        
        ip_key = f"ip:{source_ip}"
        if ip_key not in self._rate_tracking:
            self._rate_tracking[ip_key] = {
                'requests': 0,
                'window_start': current_time,
                'blocked_until': None
            }
        
        tracking = self._rate_tracking[ip_key]
        
        # Vérification si encore bloqué
        if tracking['blocked_until'] and current_time < tracking['blocked_until']:
            return False
        
        # Reset de la fenêtre si nécessaire
        if current_time - tracking['window_start'] > timedelta(minutes=1):
            tracking['requests'] = 0
            tracking['window_start'] = current_time
            tracking['blocked_until'] = None
        
        # Vérification limite
        per_ip_limit = self.rate_limits.get('per_ip', {}).get('requests_per_minute', 60)
        
        if tracking['requests'] >= per_ip_limit:
            # Bloquer pour 5 minutes
            tracking['blocked_until'] = current_time + timedelta(minutes=5)
            return False
        
        tracking['requests'] += 1
        return True
    
    def block_ip(self, ip_address: str, reason: str = "Security violation"):
        """Bloque une adresse IP"""
        self.blocked_ips.add(ip_address)
        
        security_logger.log_security_event("IP_BLOCKED", {
            "ip_address": ip_address,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def unblock_ip(self, ip_address: str):
        """Débloque une adresse IP"""
        self.blocked_ips.discard(ip_address)
        
        security_logger.log_security_event("IP_UNBLOCKED", {
            "ip_address": ip_address,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_security_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques de sécurité réseau"""
        return {
            "security_level": self.security_level.value,
            "security_groups_count": len(self.security_groups),
            "waf_rules_count": len(self.waf_rules),
            "blocked_ips_count": len(self.blocked_ips),
            "rate_limits": self.rate_limits,
            "last_updated": datetime.utcnow().isoformat()
        }
    
    def generate_security_group_config(self, format_type: str = "terraform") -> str:
        """Génère la configuration Infrastructure as Code"""
        if format_type == "terraform":
            return self._generate_terraform_config()
        elif format_type == "cloudformation":
            return self._generate_cloudformation_config()
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _generate_terraform_config(self) -> str:
        """Génère la configuration Terraform pour les security groups"""
        config = []
        
        for sg_name, sg in self.security_groups.items():
            config.append(f"""
resource "aws_security_group" "{sg_name}" {{
  name        = "{sg.name}"
  description = "{sg.description}"
  vpc_id      = "{sg.vpc_id}"

""")
            
            # Inbound rules
            for rule in sg.inbound_rules:
                config.append(f"""  ingress {{
    from_port   = {rule.port_range.split('-')[0]}
    to_port     = {rule.port_range.split('-')[-1]}
    protocol    = "{rule.protocol.value}"
    cidr_blocks = ["{rule.source_cidr}"]
    description = "{rule.description}"
  }}

""")
            
            # Outbound rules
            for rule in sg.outbound_rules:
                config.append(f"""  egress {{
    from_port   = {rule.port_range.split('-')[0]}
    to_port     = {rule.port_range.split('-')[-1]}
    protocol    = "{rule.protocol.value}"
    cidr_blocks = ["{rule.source_cidr}"]
    description = "{rule.description}"
  }}

""")
            
            # Tags
            config.append(f"""  tags = {{
""")
            for key, value in sg.tags.items():
                config.append(f"""    {key} = "{value}"
""")
            config.append(f"""  }}
}}

""")
        
        return "".join(config)
    
    def _generate_cloudformation_config(self) -> str:
        """Génère la configuration CloudFormation"""
        # Implementation CloudFormation si nécessaire
        return "# CloudFormation template generation not implemented yet"


# Instance globale
_network_security: Optional[NetworkSecurityManager] = None


def get_network_security() -> NetworkSecurityManager:
    """Retourne l'instance globale de sécurité réseau"""
    global _network_security
    
    if _network_security is None:
        env = os.getenv('ENVIRONMENT', 'development').lower()
        if env == 'production':
            level = SecurityLevel.PRODUCTION
        elif env in ['staging', 'testing']:
            level = SecurityLevel.STAGING
        else:
            level = SecurityLevel.DEVELOPMENT
        
        _network_security = NetworkSecurityManager(level)
    
    return _network_security
