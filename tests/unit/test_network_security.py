"""
Tests unitaires pour le module network_security.py
Objectif : 85% couverture (45%  85%)
Sprint 2.2 - Tests & Qualit
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import ipaddress
from enum import Enum

from orchestrator.app.security.network_security import (
    NetworkSecurityManager,
    SecurityLevel,
    ProtocolType,
    NetworkRule,
    SecurityGroup,
    get_network_security
)


@pytest.mark.unit
class TestSecurityLevel:
    """Tests pour l'enum SecurityLevel."""
    
    def test_security_levels_enum(self):
        """Test que tous les niveaux de scurit sont dfinis."""
        assert SecurityLevel.DEVELOPMENT.value == "development"
        assert SecurityLevel.STAGING.value == "staging"
        assert SecurityLevel.PRODUCTION.value == "production"


@pytest.mark.unit
class TestProtocolType:
    """Tests pour l'enum ProtocolType."""
    
    def test_protocol_types_enum(self):
        """Test que tous les types de protocole sont dfinis."""
        assert ProtocolType.TCP.value == "tcp"
        assert ProtocolType.UDP.value == "udp"
        assert ProtocolType.HTTP.value == "http"
        assert ProtocolType.HTTPS.value == "https"


@pytest.mark.unit
class TestNetworkRule:
    """Tests pour la classe NetworkRule."""
    
    def test_network_rule_creation(self):
        """Test cration d'une rgle rseau."""
        rule = NetworkRule(
            name="test-rule",
            protocol=ProtocolType.HTTP,
            port_range="80",
            source_cidr="10.0.0.0/24",
            description="Test rule"
        )
        
        assert rule.name == "test-rule"
        assert rule.protocol == ProtocolType.HTTP
        assert rule.port_range == "80"
        assert rule.source_cidr == "10.0.0.0/24"
        assert rule.description == "Test rule"
        assert rule.action == "ALLOW"  # Default value
        assert rule.priority == 100   # Default value
    
    def test_network_rule_custom_action_priority(self):
        """Test cration rgle avec action et priorit personnalises."""
        rule = NetworkRule(
            name="deny-rule",
            protocol=ProtocolType.TCP,
            port_range="22",
            source_cidr="0.0.0.0/0",
            description="Deny SSH",
            action="DENY",
            priority=50
        )
        
        assert rule.action == "DENY"
        assert rule.priority == 50


@pytest.mark.unit
class TestSecurityGroup:
    """Tests pour la classe SecurityGroup."""
    
    def test_security_group_creation(self):
        """Test cration d'un security group."""
        inbound_rule = NetworkRule(
            name="http-inbound",
            protocol=ProtocolType.HTTP,
            port_range="80",
            source_cidr="0.0.0.0/0",
            description="HTTP inbound"
        )
        
        sg = SecurityGroup(
            name="web-sg",
            description="Web security group",
            vpc_id="vpc-123",
            inbound_rules=[inbound_rule],
            outbound_rules=[],
            tags={"Environment": "test"}
        )
        
        assert sg.name == "web-sg"
        assert sg.description == "Web security group"
        assert sg.vpc_id == "vpc-123"
        assert len(sg.inbound_rules) == 1
        assert len(sg.outbound_rules) == 0
        assert sg.tags["Environment"] == "test"


@pytest.mark.unit
class TestNetworkSecurityManager:
    """Tests pour NetworkSecurityManager."""
    
    @pytest.fixture
    def dev_security_manager(self):
        """Fixture pour un manager en mode dveloppement."""
        return NetworkSecurityManager(SecurityLevel.DEVELOPMENT)
    
    @pytest.fixture
    def staging_security_manager(self):
        """Fixture pour un manager en mode staging."""
        return NetworkSecurityManager(SecurityLevel.STAGING)
    
    @pytest.fixture
    def prod_security_manager(self):
        """Fixture pour un manager en mode production."""
        return NetworkSecurityManager(SecurityLevel.PRODUCTION)
    
    def test_initialization_development(self, dev_security_manager):
        """Test initialisation en mode dveloppement."""
        manager = dev_security_manager
        
        assert manager.security_level == SecurityLevel.DEVELOPMENT
        assert isinstance(manager.security_groups, dict)
        assert isinstance(manager.waf_rules, list)
        assert isinstance(manager.rate_limits, dict)
        assert isinstance(manager.blocked_ips, set)
        assert isinstance(manager.monitored_endpoints, dict)
    
    def test_initialization_staging(self, staging_security_manager):
        """Test initialisation en mode staging."""
        manager = staging_security_manager
        
        assert manager.security_level == SecurityLevel.STAGING
        # Staging should have some rate limits configured
        assert "global" in manager.rate_limits
        assert "per_ip" in manager.rate_limits
    
    def test_initialization_production(self, prod_security_manager):
        """Test initialisation en mode production."""
        manager = prod_security_manager
        
        assert manager.security_level == SecurityLevel.PRODUCTION
        # Production should have strict configuration
        assert len(manager.security_groups) > 0
        assert len(manager.waf_rules) > 0
        assert manager.rate_limits["per_ip"]["requests_per_minute"] == 60
    
    def test_setup_production_security_groups(self, prod_security_manager):
        """Test cration des security groups de production."""
        manager = prod_security_manager
        
        # Vrifier que les security groups principaux sont crs
        assert "orchestrator" in manager.security_groups
        assert "memory-api" in manager.security_groups
        assert "database" in manager.security_groups
        
        # Vrifier la configuration du security group orchestrator
        orchestrator_sg = manager.security_groups["orchestrator"]
        assert orchestrator_sg.name == "orchestrator-prod-sg"
        assert orchestrator_sg.vpc_id == "vpc-prod-001"
        assert len(orchestrator_sg.inbound_rules) > 0
    
    def test_waf_rules_production(self, prod_security_manager):
        """Test rgles WAF en production."""
        manager = prod_security_manager
        
        waf_rules = manager.waf_rules
        assert len(waf_rules) >= 5  # Au moins 5 rgles de base
        
        # Vrifier les rgles anti-OWASP Top 10
        rule_names = [rule["name"] for rule in waf_rules]
        assert "SQLInjectionRule" in rule_names
        assert "XSSRule" in rule_names
        assert "RateLimitRule" in rule_names
        assert "SizeRestrictionRule" in rule_names
        assert "BlockBadBots" in rule_names
    
    def test_rule_matches_tcp_port(self, dev_security_manager):
        """Test correspondance de rgle TCP sur port."""
        manager = dev_security_manager
        
        rule = NetworkRule(
            name="ssh-rule",
            protocol=ProtocolType.TCP,
            port_range="22",
            source_cidr="10.0.0.0/24",
            description="SSH access"
        )
        
        # Test match
        assert manager._rule_matches(rule, "10.0.0.100", 22, "tcp")
        
        # Test no match - wrong port
        assert not manager._rule_matches(rule, "10.0.0.100", 80, "tcp")
        
        # Test no match - wrong IP
        assert not manager._rule_matches(rule, "192.168.1.100", 22, "tcp")
        
        # Test no match - wrong protocol
        assert not manager._rule_matches(rule, "10.0.0.100", 22, "udp")
    
    def test_rule_matches_port_range(self, dev_security_manager):
        """Test correspondance de rgle avec plage de ports."""
        manager = dev_security_manager
        
        rule = NetworkRule(
            name="ephemeral-rule",
            protocol=ProtocolType.TCP,
            port_range="1024-65535",
            source_cidr="0.0.0.0/0",
            description="Ephemeral ports"
        )
        
        # Test dans la plage
        assert manager._rule_matches(rule, "1.1.1.1", 8080, "tcp")
        assert manager._rule_matches(rule, "1.1.1.1", 1024, "tcp")
        assert manager._rule_matches(rule, "1.1.1.1", 65535, "tcp")
        
        # Test hors plage
        assert not manager._rule_matches(rule, "1.1.1.1", 80, "tcp")
        assert not manager._rule_matches(rule, "1.1.1.1", 1023, "tcp")
    
    def test_validate_network_access_blocked_ip(self, dev_security_manager):
        """Test validation accs rseau avec IP bloque."""
        manager = dev_security_manager
        
        # Bloquer une IP
        manager.block_ip("192.168.1.100", "Test block")
        
        # Tenter l'accs
        allowed, reason = manager.validate_network_access("192.168.1.100", 80)
        
        assert not allowed
        assert reason == "IP blocked"
    
    def test_validate_network_access_rate_limit(self, dev_security_manager):
        """Test validation accs rseau avec rate limiting."""
        manager = dev_security_manager
        
        # Simuler dpassement de rate limit
        with patch.object(manager, '_check_rate_limit', return_value=False):
            allowed, reason = manager.validate_network_access("192.168.1.100", 80)
            
            assert not allowed
            assert reason == "Rate limit exceeded"
    
    def test_validate_network_access_security_group_allow(self, staging_security_manager):
        """Test validation accs rseau avec rgle autorise."""
        manager = staging_security_manager
        
        # Ajouter une rgle d'autorisation
        allow_rule = NetworkRule(
            name="test-allow",
            protocol=ProtocolType.TCP,
            port_range="80",
            source_cidr="192.168.1.0/24",
            description="Test allow",
            action="ALLOW"
        )
        
        sg = SecurityGroup(
            name="test-sg",
            description="Test security group",
            vpc_id="vpc-test",
            inbound_rules=[allow_rule],
            outbound_rules=[],
            tags={}
        )
        
        manager.security_groups["test"] = sg
        
        # Tester l'accs
        allowed, reason = manager.validate_network_access("192.168.1.100", 80, "tcp")
        
        assert allowed
        assert "test-allow" in reason
    
    def test_validate_network_access_security_group_deny(self, staging_security_manager):
        """Test validation accs rseau avec rgle de refus."""
        manager = staging_security_manager
        
        # Ajouter une rgle de refus
        deny_rule = NetworkRule(
            name="test-deny",
            protocol=ProtocolType.TCP,
            port_range="22",
            source_cidr="0.0.0.0/0",
            description="Test deny",
            action="DENY"
        )
        
        sg = SecurityGroup(
            name="test-sg",
            description="Test security group",
            vpc_id="vpc-test",
            inbound_rules=[deny_rule],
            outbound_rules=[],
            tags={}
        )
        
        manager.security_groups["test"] = sg
        
        # Tester l'accs
        allowed, reason = manager.validate_network_access("10.0.0.100", 22, "tcp")
        
        assert not allowed
        assert "test-deny" in reason
    
    def test_validate_network_access_default_deny(self, dev_security_manager):
        """Test validation accs rseau avec refus par dfaut."""
        manager = dev_security_manager
        
        # Pas de rgle correspondante = refus par dfaut
        allowed, reason = manager.validate_network_access("10.0.0.100", 8080, "tcp")
        
        assert not allowed
        assert reason == "Default deny"
    
    def test_check_rate_limit_first_request(self, dev_security_manager):
        """Test rate limiting pour premire requte."""
        manager = dev_security_manager
        
        # Premire requte doit tre autorise
        assert manager._check_rate_limit("192.168.1.100")
    
    def test_block_unblock_ip(self, dev_security_manager):
        """Test blocage et dblocage d'IP."""
        manager = dev_security_manager
        
        ip = "192.168.1.100"
        
        # Vrifier que l'IP n'est pas bloque initialement
        assert ip not in manager.blocked_ips
        
        # Bloquer l'IP
        manager.block_ip(ip, "Test block")
        assert ip in manager.blocked_ips
        
        # Dbloquer l'IP
        manager.unblock_ip(ip)
        assert ip not in manager.blocked_ips
    
    def test_get_security_metrics(self, prod_security_manager):
        """Test rcupration des mtriques de scurit."""
        manager = prod_security_manager
        
        metrics = manager.get_security_metrics()
        
        assert "security_level" in metrics
        assert "security_groups_count" in metrics
        assert "waf_rules_count" in metrics
        assert "blocked_ips_count" in metrics
        assert "rate_limits" in metrics
        assert "last_updated" in metrics
        
        assert metrics["security_level"] == "production"
        assert metrics["security_groups_count"] >= 3
        assert metrics["waf_rules_count"] >= 5
    
    def test_generate_terraform_config(self, staging_security_manager):
        """Test gnration configuration Terraform."""
        manager = staging_security_manager
        
        config = manager.generate_security_group_config("terraform")
        
        assert isinstance(config, str)
        assert "resource \"aws_security_group\"" in config
        assert "ingress" in config
    
    def test_generate_cloudformation_config(self, staging_security_manager):
        """Test gnration configuration CloudFormation."""
        manager = staging_security_manager
        
        config = manager.generate_security_group_config("cloudformation")
        
        assert isinstance(config, str)
        assert "AWS::EC2::SecurityGroup" in config
        assert "SecurityGroupIngress" in config
    
    def test_unsupported_config_format(self, dev_security_manager):
        """Test format de configuration non support."""
        manager = dev_security_manager
        
        with pytest.raises(ValueError, match="Unsupported format"):
            manager.generate_security_group_config("unsupported")
    
    def test_add_monitored_endpoint(self, dev_security_manager):
        """Test ajout d'endpoint surveill."""
        manager = dev_security_manager
        
        endpoint = "/api/test"
        config = {"max_requests_per_minute": 100}
        
        manager.add_monitored_endpoint(endpoint, config)
        
        assert endpoint in manager.monitored_endpoints
        assert manager.monitored_endpoints[endpoint] == config
    
    def test_remove_monitored_endpoint(self, dev_security_manager):
        """Test suppression d'endpoint surveill."""
        manager = dev_security_manager
        
        endpoint = "/api/test"
        manager.monitored_endpoints[endpoint] = {"test": "config"}
        
        manager.remove_monitored_endpoint(endpoint)
        
        assert endpoint not in manager.monitored_endpoints


@pytest.mark.unit  
class TestNetworkSecurityGlobalInstance:
    """Tests pour l'instance globale de scurit rseau."""
    
    def test_get_network_security_default(self):
        """Test rcupration instance par dfaut."""
        with patch.dict('os.environ', {}, clear=True):
            manager = get_network_security()
            
            assert isinstance(manager, NetworkSecurityManager)
            assert manager.security_level == SecurityLevel.DEVELOPMENT
    
    def test_get_network_security_production(self):
        """Test rcupration instance production."""
        with patch.dict('os.environ', {'ENVIRONMENT': 'production'}):
            manager = get_network_security()
            
            assert manager.security_level == SecurityLevel.PRODUCTION
    
    def test_get_network_security_staging(self):
        """Test rcupration instance staging."""
        with patch.dict('os.environ', {'ENVIRONMENT': 'staging'}):
            manager = get_network_security()
            
            assert manager.security_level == SecurityLevel.STAGING
    
    def test_get_network_security_singleton(self):
        """Test que l'instance est un singleton."""
        # Reset global instance
        import orchestrator.app.security.network_security
        orchestrator.app.security.network_security._network_security = None
        
        manager1 = get_network_security()
        manager2 = get_network_security()
        
        assert manager1 is manager2


@pytest.mark.unit
class TestNetworkSecurityEdgeCases:
    """Tests pour les cas limites."""
    
    def test_rule_matches_invalid_cidr(self):
        """Test correspondance rgle avec CIDR invalide."""
        manager = NetworkSecurityManager(SecurityLevel.DEVELOPMENT)
        
        rule = NetworkRule(
            name="invalid-cidr",
            protocol=ProtocolType.TCP,
            port_range="80",
            source_cidr="invalid-cidr",
            description="Invalid CIDR"
        )
        
        # Ne doit pas lever d'exception, doit retourner False
        assert not manager._rule_matches(rule, "10.0.0.100", 80, "tcp")
    
    def test_rule_matches_invalid_port_range(self):
        """Test correspondance rgle avec plage de ports invalide."""
        manager = NetworkSecurityManager(SecurityLevel.DEVELOPMENT)
        
        rule = NetworkRule(
            name="invalid-port",
            protocol=ProtocolType.TCP,
            port_range="invalid-port",
            source_cidr="0.0.0.0/0",
            description="Invalid port"
        )
        
        # Ne doit pas lever d'exception
        try:
            manager._rule_matches(rule, "10.0.0.100", 80, "tcp")
        except Exception:
            pytest.fail("_rule_matches should handle invalid port gracefully")
    
    def test_empty_security_groups(self):
        """Test comportement avec security groups vides."""
        manager = NetworkSecurityManager(SecurityLevel.DEVELOPMENT)
        manager.security_groups.clear()
        
        allowed, reason = manager.validate_network_access("10.0.0.100", 80, "tcp")
        
        assert not allowed
        assert reason == "Default deny"
    
    def test_multiple_matching_rules(self, staging_security_manager):
        """Test avec plusieurs rgles correspondantes."""
        manager = staging_security_manager
        
        # Ajouter plusieurs rgles correspondantes
        allow_rule = NetworkRule(
            name="allow-rule",
            protocol=ProtocolType.TCP,
            port_range="80",
            source_cidr="10.0.0.0/24",
            description="Allow HTTP",
            action="ALLOW",
            priority=100
        )
        
        deny_rule = NetworkRule(
            name="deny-rule",
            protocol=ProtocolType.TCP,
            port_range="80",
            source_cidr="10.0.0.0/24",
            description="Deny HTTP",
            action="DENY",
            priority=200
        )
        
        sg = SecurityGroup(
            name="multi-rule-sg",
            description="Multiple rules security group",
            vpc_id="vpc-test",
            inbound_rules=[allow_rule, deny_rule],
            outbound_rules=[],
            tags={}
        )
        
        manager.security_groups["multi"] = sg
        
        # La premire rgle correspondante devrait s'appliquer
        allowed, reason = manager.validate_network_access("10.0.0.100", 80, "tcp")
        
        assert allowed  # allow_rule est value en premier
        assert "allow-rule" in reason 



