"""
Tests unitaires pour l'agent MAINTENANCE 09 - Analyseur de Sécurité
"""

import pytest
import os
from pathlib import Path
import tempfile
import json
from unittest.mock import Mock, patch

from agents.agent_MAINTENANCE_09_analyseur_securite import (
    AgentMAINTENANCE09AnalyseurSecurite,
    SecurityLevel,
    VulnerabilityType,
    SecurityFinding,
    SecurityReport
)

# Fixtures
@pytest.fixture
def agent():
    """Crée une instance de l'agent pour les tests"""
    return AgentMAINTENANCE09AnalyseurSecurite(workspace_root=str(Path.cwd()))

@pytest.fixture
def sample_python_file():
    """Crée un fichier Python temporaire avec du code à analyser"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('''
import os
import pickle

def unsafe_function():
    """Fonction avec des vulnérabilités pour les tests"""
    # Exécution de code arbitraire
    eval("print('test')")
    
    # Désérialisation non sécurisée
    data = pickle.loads(b"dangerous")
    
    # Commande système non sécurisée
    os.system("echo test")
    
    # Secret en dur
    password = "my_secret_password123"
    api_key = "sk_test_123456789"
    
    return True
''')
        return Path(f.name)

# Tests des classes de base
def test_security_level_from_cvss():
    """Test de la conversion des scores CVSS en niveaux de sécurité"""
    assert SecurityLevel.from_cvss(9.5) == SecurityLevel.CRITICAL
    assert SecurityLevel.from_cvss(7.5) == SecurityLevel.HIGH
    assert SecurityLevel.from_cvss(5.0) == SecurityLevel.MEDIUM
    assert SecurityLevel.from_cvss(2.0) == SecurityLevel.LOW
    assert SecurityLevel.from_cvss(0.0) == SecurityLevel.INFO

def test_security_finding_creation():
    """Test de la création d'un finding de sécurité"""
    finding = SecurityFinding(
        finding_id="TEST-001",
        vulnerability_type=VulnerabilityType.DANGEROUS_FUNCTION,
        security_level=SecurityLevel.HIGH,
        title="Test Finding",
        description="Test Description",
        location="test.py",
        line_number=10,
        cwe_id="CWE-78",
        cvss_score=7.5
    )
    
    assert finding.finding_id == "TEST-001"
    assert finding.security_level == SecurityLevel.HIGH
    assert finding.cvss_score == 7.5

def test_security_report_score_update():
    """Test de la mise à jour du score de sécurité dans un rapport"""
    report = SecurityReport(
        audit_id="TEST-AUDIT-001",
        target="test_project",
        timestamp=None
    )
    
    # Ajout de findings et vérification du score
    finding1 = SecurityFinding(
        finding_id="TEST-001",
        vulnerability_type=VulnerabilityType.DANGEROUS_FUNCTION,
        security_level=SecurityLevel.CRITICAL,
        title="Critical Issue",
        description="Test",
        location="test.py"
    )
    
    finding2 = SecurityFinding(
        finding_id="TEST-002",
        vulnerability_type=VulnerabilityType.WEAK_CRYPTO,
        security_level=SecurityLevel.MEDIUM,
        title="Medium Issue",
        description="Test",
        location="test.py"
    )
    
    report.add_finding(finding1)
    assert report.security_score < 9.0  # Score réduit pour vulnérabilité critique
    
    report.add_finding(finding2)
    assert report.security_score < 8.0  # Score réduit davantage

# Tests de l'agent
def test_agent_initialization(agent):
    """Test de l'initialisation de l'agent"""
    assert agent.version == "2.0.0"
    assert agent.status == "enabled"
    assert isinstance(agent.excluded_paths, set)
    assert '.git' in agent.excluded_paths
    assert '__pycache__' in agent.excluded_paths

@pytest.mark.asyncio
async def test_agent_startup(agent):
    """Test du démarrage de l'agent"""
    result = await agent.startup()
    assert result is True

@pytest.mark.asyncio
async def test_agent_health_check(agent):
    """Test du health check de l'agent"""
    health = await agent.health_check()
    assert isinstance(health, dict)
    assert health['status'] == 'healthy'
    assert 'version' in health

def test_agent_get_capabilities(agent):
    """Test de la récupération des capacités de l'agent"""
    capabilities = agent.get_capabilities()
    assert isinstance(capabilities, list)
    assert len(capabilities) > 0
    assert 'security_scan' in capabilities

@pytest.mark.asyncio
async def test_security_scan_task(agent, sample_python_file):
    """Test d'une tâche d'analyse de sécurité"""
    task = Mock()
    task.task_id = "TEST-TASK-001"
    task.data = {
        "target_path": str(sample_python_file),
        "scan_type": "security_scan"
    }
    
    result = await agent.execute_task(task)
    
    assert result.success is True
    assert isinstance(result.data, dict)
    assert 'findings' in result.data
    assert 'security_score' in result.data
    
    # Vérification des vulnérabilités trouvées
    findings = result.data['findings']
    assert len(findings) > 0
    
    # Vérification des types de vulnérabilités détectées
    vuln_types = {f['vulnerability_type'] for f in findings}
    assert VulnerabilityType.DANGEROUS_FUNCTION.value in vuln_types
    assert VulnerabilityType.HARDCODED_SECRET.value in vuln_types

@pytest.mark.asyncio
async def test_dependency_check_task(agent):
    """Test d'une tâche de vérification des dépendances"""
    task = Mock()
    task.task_id = "TEST-TASK-002"
    task.data = {
        "scan_type": "dependency_check",
        "requirements_file": "requirements.txt"
    }
    
    with patch('safety.safety.check') as mock_safety_check:
        mock_safety_check.return_value = []
        result = await agent.execute_task(task)
        
        assert result.success is True
        assert isinstance(result.data, dict)
        assert 'dependencies_checked' in result.data

@pytest.mark.asyncio
async def test_config_audit_task(agent):
    """Test d'une tâche d'audit de configuration"""
    task = Mock()
    task.task_id = "TEST-TASK-003"
    task.data = {
        "scan_type": "config_audit",
        "config_file": "config.json"
    }
    
    result = await agent.execute_task(task)
    assert result.success is True
    assert isinstance(result.data, dict)
    assert 'config_findings' in result.data

def test_cleanup(sample_python_file):
    """Nettoyage des fichiers temporaires"""
    try:
        os.unlink(sample_python_file)
    except:
        pass 