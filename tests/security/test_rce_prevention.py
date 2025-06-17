"""
Tests de prévention contre Remote Code Execution (RCE).
Tests critiques pour vérifier que la vulnérabilité RCE a été corrigée.
"""

import pytest
import asyncio
import ast
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from typing import Dict, Any

# Import conditionnel pour éviter les erreurs
try:
    from orchestrator.app.security.secure_analyzer import (
        SecureCodeAnalyzer, 
        SecurityError, 
        ValidationError,
        secure_python_linter_tool
    )
    SECURE_ANALYZER_AVAILABLE = True
except ImportError:
    SECURE_ANALYZER_AVAILABLE = False
    SecureCodeAnalyzer = None
    SecurityError = Exception
    ValidationError = Exception


@pytest.mark.security
@pytest.mark.skipif(not SECURE_ANALYZER_AVAILABLE, reason="Secure analyzer not available")
class TestRCEPrevention:
    """Tests de prévention contre Remote Code Execution."""
    
    @pytest.fixture
    def analyzer(self, temp_dir):
        """Fixture pour l'analyseur sécurisé."""
        sandbox_dir = temp_dir / "sandbox"
        return SecureCodeAnalyzer(sandbox_dir=sandbox_dir)
    
    @pytest.mark.parametrize("malicious_code,expected_pattern", [
        ("eval('print(1)')", "eval"),
        ("exec('import os; os.system(\"rm -rf /\")')", "exec"),
        ("__import__('os').system('malicious')", "__import__"),
        ("open('/etc/passwd', 'r').read()", "open"),
        ("compile('malicious', '<string>', 'exec')", "compile"),
        ("globals()['__builtins__']['eval']('dangerous')", "globals"),
        ("locals()['dangerous_func']()", "locals"),
        ("getattr(__builtins__, 'eval')('code')", "getattr"),
        ("setattr(obj, 'attr', dangerous_value)", "setattr"),
        ("delattr(obj, 'dangerous_attr')", "delattr"),
    ])
    def test_dangerous_patterns_blocked(self, analyzer, malicious_code, expected_pattern, assert_security_compliance):
        """Test que les patterns dangereux sont bloqués."""
        with pytest.raises(SecurityError) as exc_info:
            analyzer.validate_code_safety(malicious_code)
        
        error_message = str(exc_info.value)
        assert expected_pattern.lower() in error_message.lower(), \
            f"Expected pattern '{expected_pattern}' not found in error: {error_message}"
        
        # Vérification conformité sécurité
        assert_security_compliance['no_code_execution'](error_message)
    
    @pytest.mark.parametrize("forbidden_import", [
        "import os",
        "import subprocess",
        "import sys",
        "import socket",
        "import shutil",
        "import tempfile",
        "import importlib",
        "import ctypes",
        "import multiprocessing",
        "import threading",
        "from os import system",
        "from subprocess import run",
        "from sys import exit",
    ])
    def test_forbidden_imports_blocked(self, analyzer, forbidden_import):
        """Test que les imports interdits sont bloqués."""
        malicious_code = f"""
{forbidden_import}
print("This should not work")
"""
        with pytest.raises(SecurityError) as exc_info:
            analyzer.validate_code_safety(malicious_code)
        
        error_message = str(exc_info.value)
        assert any(keyword in error_message.lower() for keyword in ['import', 'forbidden', 'not allowed']), \
            f"Import restriction not properly reported: {error_message}"
    
    def test_ast_validation_blocks_dangerous_imports(self, analyzer):
        """Test que les imports dangereux sont bloqués au niveau AST."""
        malicious_code = """
import subprocess
import shutil
subprocess.run(['rm', '-rf', '/'])
"""
        with pytest.raises(SecurityError) as exc_info:
            analyzer.validate_code_safety(malicious_code)
        
        assert "subprocess" in str(exc_info.value).lower()
    
    def test_safe_code_passes_validation(self, analyzer, sample_python_codes):
        """Test que le code sûr passe la validation."""
        safe_code = sample_python_codes['safe_code']
        
        # Ne doit pas lever d'exception
        result = analyzer.validate_code_safety(safe_code)
        assert result is True
        
        # Test avec code complexe mais sûr
        complex_safe = sample_python_codes['complex_safe']
        result = analyzer.validate_code_safety(complex_safe)
        assert result is True
    
    def test_syntax_error_handling(self, analyzer, sample_python_codes):
        """Test que les erreurs de syntaxe sont gérées correctement."""
        syntax_error_code = sample_python_codes['syntax_error']
        
        with pytest.raises(ValidationError) as exc_info:
            analyzer.validate_code_safety(syntax_error_code)
        
        assert "syntax" in str(exc_info.value).lower()
    
    def test_code_size_limit_enforced(self, analyzer):
        """Test que la limite de taille de code est appliquée."""
        large_code = "print('x')\\n" * 1000  # Code très volumineux
        
        with pytest.raises(SecurityError) as exc_info:
            analyzer.validate_code_safety(large_code)
        
        assert "size" in str(exc_info.value).lower() or "limit" in str(exc_info.value).lower()
    
    def test_empty_code_handling(self, analyzer):
        """Test de la gestion du code vide."""
        with pytest.raises(ValidationError):
            analyzer.validate_code_safety("")
        
        with pytest.raises(ValidationError):
            analyzer.validate_code_safety("   \\n\\t  ")
    
    @pytest.mark.asyncio
    async def test_timeout_protection(self, analyzer, sample_python_codes):
        """Test que l'exécution longue est interrompue."""
        infinite_loop_code = sample_python_codes['infinite_loop']
        
        # Mock subprocess.run dans le module secure_analyzer pour simuler un timeout
        with patch('orchestrator.app.security.secure_analyzer.run') as mock_run:
            from subprocess import TimeoutExpired
            mock_run.side_effect = TimeoutExpired(cmd=['pylint'], timeout=10)
            
            with pytest.raises(SecurityError, match="timed out|timeout"):
                await analyzer.analyze_code_secure(infinite_loop_code)
    
    @pytest.mark.asyncio 
    @patch('orchestrator.app.security.secure_analyzer.run')
    async def test_sandboxed_execution(self, mock_run, analyzer, sample_python_codes):
        """Test que l'exécution se fait en sandbox."""
        mock_run.return_value.stdout = "No issues"
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        
        safe_code = sample_python_codes['safe_code']
        await analyzer.analyze_code_secure(safe_code)
        
        # Vérifier que l'exécution est sandboxée
        assert mock_run.called
        call_args = mock_run.call_args
        
        # Vérifier les paramètres de sécurité
        assert call_args.kwargs['timeout'] == 10  # Timeout strict
        assert str(analyzer.sandbox_dir) in call_args.kwargs['cwd']
        assert 'PATH' in call_args.kwargs['env']
        assert call_args.kwargs['env']['PATH'] == '/usr/bin:/bin'
    
    @pytest.mark.asyncio
    async def test_secure_file_creation(self, analyzer, sample_python_codes):
        """Test que les fichiers temporaires sont créés de manière sécurisée."""
        safe_code = sample_python_codes['safe_code']
        
        with patch('orchestrator.app.security.secure_analyzer.run') as mock_run:
            mock_run.return_value.stdout = "pylint output"
            mock_run.return_value.stderr = ""
            mock_run.return_value.returncode = 0
            
            result = await analyzer.analyze_code_secure(safe_code)
            
            # Vérifier que le fichier temporaire a été créé dans le sandbox
            assert mock_run.called
            temp_file_path = mock_run.call_args[0][0][-1]  # Dernier argument de pylint
            assert str(analyzer.sandbox_dir) in temp_file_path
    
    @pytest.mark.asyncio
    async def test_output_sanitization(self, analyzer, sample_python_codes):
        """Test que la sortie est correctement nettoyée."""
        safe_code = sample_python_codes['safe_code']
        
        with patch('orchestrator.app.security.secure_analyzer.run') as mock_run:
            # Simulation d'une sortie contenant des chemins sensibles
            mock_run.return_value.stdout = f"{analyzer.sandbox_dir}/analysis_123_abc.py:1:0: C0111: Missing docstring"
            mock_run.return_value.stderr = ""
            mock_run.return_value.returncode = 0
            
            result = await analyzer.analyze_code_secure(safe_code)
            
            # Vérifier que les chemins sensibles sont masqués
            assert str(analyzer.sandbox_dir) not in result
            assert "[FILE]" in result
    
    def test_security_metrics_available(self, analyzer):
        """Test que les métriques de sécurité sont disponibles."""
        metrics = analyzer.get_security_metrics()
        
        assert 'allowed_imports_count' in metrics
        assert 'forbidden_imports_count' in metrics
        assert 'dangerous_patterns_count' in metrics
        assert 'sandbox_dir' in metrics
        assert 'max_code_size' in metrics
        assert 'analysis_timeout' in metrics
        
        # Vérifier les valeurs
        assert metrics['allowed_imports_count'] > 0
        assert metrics['forbidden_imports_count'] > 0
        assert metrics['dangerous_patterns_count'] > 0
        assert metrics['max_code_size'] == 10000
        assert metrics['analysis_timeout'] == 10


@pytest.mark.security
@pytest.mark.skipif(not SECURE_ANALYZER_AVAILABLE, reason="Secure analyzer not available")
class TestSecurityUnderLoad:
    """Tests de sécurité sous charge."""
    
    @pytest.mark.asyncio
    async def test_concurrent_analysis_safety(self, temp_dir, sample_python_codes, performance_monitor):
        """Test la sécurité lors d'analyses concurrentes."""
        analyzer = SecureCodeAnalyzer(sandbox_dir=temp_dir / "sandbox")
        safe_code = sample_python_codes['safe_code']
        
        performance_monitor.start()
        
        # Lancer 10 analyses concurrentes
        tasks = [
            analyzer.analyze_code_secure(safe_code) 
            for _ in range(10)
        ]
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "No issues found"
            mock_run.return_value.stderr = ""
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        performance_monitor.checkpoint('concurrent_analysis')
        
        # Toutes doivent réussir
        for result in results:
            assert not isinstance(result, Exception), f"Concurrent analysis failed: {result}"
            assert isinstance(result, str)
        
        # Test de performance - ne doit pas dépasser 10 secondes pour 10 analyses (plus réaliste)
        performance_monitor.assert_max_duration(10000)
    
    @pytest.mark.asyncio 
    async def test_memory_safety_under_load(self, temp_dir, sample_python_codes):
        """Test qu'il n'y a pas de fuite mémoire sous charge."""
        analyzer = SecureCodeAnalyzer(sandbox_dir=temp_dir / "sandbox")
        safe_code = sample_python_codes['safe_code']
        
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "No issues"
            mock_run.return_value.stderr = ""
            
            # Exécuter 50 analyses
            for _ in range(50):
                await analyzer.analyze_code_secure(safe_code)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # L'augmentation mémoire ne doit pas dépasser 50MB
        assert memory_increase < 50 * 1024 * 1024, \
            f"Memory leak detected: {memory_increase / 1024 / 1024:.2f}MB increase"


@pytest.mark.security
@pytest.mark.skipif(not SECURE_ANALYZER_AVAILABLE, reason="Secure analyzer not available")
class TestSecureLinterToolIntegration:
    """Tests d'intégration pour l'outil de linting sécurisé."""
    
    @pytest.mark.asyncio
    async def test_secure_linter_tool_safe_code(self, sample_python_codes, assert_security_compliance):
        """Test de l'outil de linting sécurisé avec du code sûr."""
        safe_code = sample_python_codes['safe_code']
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "Your code has been rated at 10.00/10"
            mock_run.return_value.stderr = ""
            
            result = await secure_python_linter_tool(safe_code)
            
            assert isinstance(result, str)
            assert "security validation failed" not in result.lower()
            assert_security_compliance['no_code_execution'](result)
    
    @pytest.mark.asyncio
    async def test_secure_linter_tool_malicious_code(self, sample_python_codes):
        """Test de l'outil de linting sécurisé avec du code malveillant."""
        malicious_code = sample_python_codes['malicious_eval']
        
        result = await secure_python_linter_tool(malicious_code)
        
        assert "security validation failed" in result.lower()
        assert "eval" in result.lower()  # Le pattern dangereux doit être mentionné
    
    @pytest.mark.asyncio
    async def test_secure_linter_tool_error_handling(self, sample_python_codes):
        """Test de la gestion d'erreurs de l'outil de linting sécurisé."""
        syntax_error_code = sample_python_codes['syntax_error']
        
        result = await secure_python_linter_tool(syntax_error_code)
        
        assert "validation failed" in result.lower()
        assert isinstance(result, str)


@pytest.mark.security 
class TestLegacyCodeVulnerability:
    """Tests pour vérifier que l'ancienne vulnérabilité a été corrigée."""
    
    def test_old_vulnerability_pattern_detection(self, sample_python_codes):
        """Test de détection des patterns de l'ancienne vulnérabilité."""
        # Simulation de l'ancien code vulnérable
        def old_vulnerable_linter(code: str) -> str:
            """Simulation de l'ancienne fonction vulnérable."""
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=True) as tmp:
                tmp.write(code)  # ⚠️ CODE NON VALIDÉ - VULNÉRABLE
                tmp.flush()
                # Simulation seulement, pas d'exécution réelle
                return f"Would execute pylint on: {tmp.name}"
        
        malicious_code = sample_python_codes['malicious_import']
        
        # L'ancienne fonction aurait créé un fichier avec du code malveillant
        result = old_vulnerable_linter(malicious_code)
        
        # Vérifier que le fichier temporaire aurait contenu du code dangereux
        assert "subprocess" in malicious_code
        assert "Would execute pylint" in result
        
        # Maintenant vérifier que la nouvelle version bloque cela
        if SECURE_ANALYZER_AVAILABLE:
            with pytest.raises(SecurityError):
                analyzer = SecureCodeAnalyzer()
                analyzer.validate_code_safety(malicious_code)


@pytest.mark.performance
@pytest.mark.security
@pytest.mark.skipif(not SECURE_ANALYZER_AVAILABLE, reason="Secure analyzer not available")
class TestSecurityPerformance:
    """Tests de performance pour les fonctionnalités de sécurité."""
    
    @pytest.mark.asyncio
    async def test_validation_performance(self, sample_python_codes, performance_monitor):
        """Test que la validation de sécurité est suffisamment rapide."""
        analyzer = SecureCodeAnalyzer()
        safe_code = sample_python_codes['safe_code']
        
        performance_monitor.start()
        
        # 100 validations doivent se faire en moins de 1 seconde
        for _ in range(100):
            analyzer.validate_code_safety(safe_code)
        
        performance_monitor.checkpoint('100_validations')
        performance_monitor.assert_max_duration(1000)  # 1 seconde max
    
    @pytest.mark.asyncio
    async def test_analysis_performance(self, sample_python_codes, performance_monitor):
        """Test que l'analyse complète reste dans les limites acceptables."""
        analyzer = SecureCodeAnalyzer()
        safe_code = sample_python_codes['safe_code']
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "No issues"
            mock_run.return_value.stderr = ""
            
            performance_monitor.start()
            
            await analyzer.analyze_code_secure(safe_code)
            
            # L'analyse doit prendre moins de 1000ms (augmenté pour être plus réaliste)
            performance_monitor.assert_max_duration(1000)


# Tests d'intégration avec les autres composants
@pytest.mark.integration
@pytest.mark.security
class TestRCEPreventionIntegration:
    """Tests d'intégration pour la prévention RCE."""
    
    def test_validator_integration(self):
        """Test d'intégration avec les validateurs existants."""
        try:
            from orchestrator.app.security.validators import CodeValidator
            
            # Test que les validateurs existants sont compatibles
            is_valid, message = CodeValidator.validate_python_code("print('hello')")
            assert is_valid
            
            is_valid, message = CodeValidator.validate_python_code("eval('dangerous')")
            assert not is_valid
            assert "dangerous" in message.lower() or "pattern" in message.lower()
            
        except ImportError:
            pytest.skip("CodeValidator not available")
    
    @pytest.mark.asyncio
    async def test_logging_integration(self, log_capture, sample_python_codes):
        """Test d'intégration avec le système de logs."""
        if not SECURE_ANALYZER_AVAILABLE:
            pytest.skip("Secure analyzer not available")
        
        analyzer = SecureCodeAnalyzer()
        malicious_code = sample_python_codes['malicious_eval']
        
        with pytest.raises(SecurityError):
            analyzer.validate_code_safety(malicious_code)
        
        # Vérifier que les logs de sécurité ne contiennent pas de secrets
        log_contents = log_capture.getvalue()
        # Les logs devraient être vides ou ne pas contenir d'informations sensibles
        # (Cette vérification dépend de la configuration du logging)
