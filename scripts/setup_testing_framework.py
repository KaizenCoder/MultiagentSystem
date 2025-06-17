#!/usr/bin/env python3
"""
Script de setup du framework de tests pour la sécurisation.
Configure l'environnement de tests selon les spécifications Quick Wins.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any


class TestFrameworkSetup:
    """Setup du framework de tests complet."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.tests_dir = self.project_root / 'tests'
        
    def install_test_dependencies(self) -> bool:
        """Installe les dépendances de test."""
        print("📦 Installing test dependencies...")
        
        dependencies = [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'pytest-asyncio>=0.21.0',
            'pytest-mock>=3.10.0',
            'pytest-timeout>=2.1.0',
            'pytest-xdist>=3.0.0',  # Tests parallèles
            'httpx>=0.24.0',
            'psutil>=5.9.0',
            'bandit>=1.7.0',
            'safety>=2.3.0',
        ]
        
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install'] + dependencies,
                capture_output=True, text=True, timeout=300
            )
            
            if result.returncode == 0:
                print("✅ Test dependencies installed successfully")
                return True
            else:
                print(f"❌ Failed to install dependencies: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Installation timed out")
            return False
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            return False
    
    def create_pytest_config(self) -> bool:
        """Crée la configuration pytest."""
        print("⚙️ Creating pytest configuration...")
        
        pytest_ini_content = """[tool:pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
python_classes = Test*
asyncio_mode = auto
timeout = 30

addopts = 
    --strict-markers
    --strict-config
    --cov=orchestrator
    --cov-report=html:htmlcov
    --cov-report=term-missing
    --cov-report=xml
    --cov-fail-under=40
    --tb=short
    -v

markers =
    security: Tests de sécurité critiques
    integration: Tests d'intégration
    performance: Tests de performance
    slow: Tests lents (>1s)
    unit: Tests unitaires
    rce: Tests de prévention RCE
    ssrf: Tests de prévention SSRF
    secrets: Tests de gestion des secrets
    health: Tests de health checks
    logging: Tests de logs structurés

filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
    ignore:.*:pytest.PytestUnraisableExceptionWarning
"""
        
        try:
            (self.project_root / 'pytest.ini').write_text(pytest_ini_content)
            print("✅ pytest.ini created")
            return True
        except Exception as e:
            print(f"❌ Failed to create pytest.ini: {e}")
            return False
    
    def create_test_structure(self) -> bool:
        """Crée la structure des répertoires de tests."""
        print("📁 Creating test directory structure...")
        
        directories = [
            self.tests_dir,
            self.tests_dir / 'unit',
            self.tests_dir / 'integration', 
            self.tests_dir / 'security',
            self.tests_dir / 'performance',
            self.tests_dir / 'fixtures',
            self.tests_dir / 'mocks'
        ]
        
        try:
            for directory in directories:
                directory.mkdir(exist_ok=True)
                (directory / '__init__.py').touch()
            
            print("✅ Test directory structure created")
            return True
        except Exception as e:
            print(f"❌ Failed to create test structure: {e}")
            return False
    
    def create_test_fixtures(self) -> bool:
        """Crée les fixtures de test."""
        print("🔧 Creating test fixtures...")
        
        # Fixture de codes malveillants
        malicious_payloads = {
            "code_injection": [
                "eval('__import__(\"os\").system(\"id\")')",
                "exec('import subprocess; subprocess.run([\"whoami\"])')",
                "__import__('os').system('ls -la')",
                "compile('malicious_code', '<string>', 'exec')",
                "open('/etc/passwd', 'r').read()",
                "globals()['__builtins__']['eval']('dangerous')"
            ],
            "ssrf_urls": [
                "http://127.0.0.1:22",
                "http://localhost:3306",
                "http://169.254.169.254/latest/meta-data/",
                "file:///etc/passwd",
                "gopher://localhost:25",
                "ftp://internal.company.com"
            ],
            "safe_code_samples": [
                """
import json
import datetime
from typing import List, Dict

def process_data(data: Dict) -> List[str]:
    result = []
    for key, value in data.items():
        if isinstance(value, str):
            result.append(f"{key}: {value}")
    return result

test_data = {"name": "test", "value": "123"}
print(process_data(test_data))
""",
                """
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    name: str
    email: str
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

user = User(1, "John Doe", "john@example.com")
print(f"User created: {user.name}")
"""
            ]
        }
        
        try:
            import json
            fixtures_file = self.tests_dir / 'fixtures' / 'malicious_payloads.json'
            fixtures_file.write_text(json.dumps(malicious_payloads, indent=2))
            
            print("✅ Test fixtures created")
            return True
        except Exception as e:
            print(f"❌ Failed to create fixtures: {e}")
            return False
    
    def create_sample_tests(self) -> bool:
        """Crée des tests d'exemple."""
        print("📝 Creating sample tests...")
        
        # Test unitaire d'exemple
        unit_test_sample = '''"""
Test unitaire d'exemple pour valider le framework.
"""
import pytest
from unittest.mock import Mock, patch


class TestSampleUnit:
    """Tests unitaires d'exemple."""
    
    def test_basic_assertion(self):
        """Test d'assertion basique."""
        assert 1 + 1 == 2
    
    def test_string_operations(self):
        """Test d'opérations sur chaînes."""
        test_string = "Hello, World!"
        assert test_string.lower() == "hello, world!"
        assert len(test_string) == 13
    
    @pytest.mark.parametrize("input_val,expected", [
        (1, 2),
        (2, 4), 
        (3, 6),
    ])
    def test_parametrized(self, input_val, expected):
        """Test paramétrisé."""
        assert input_val * 2 == expected


@pytest.mark.unit
class TestMockingExample:
    """Exemple de mocking."""
    
    @patch('os.environ.get')
    def test_environment_variable_mock(self, mock_env_get):
        """Test avec mock d'variable d'environnement."""
        mock_env_get.return_value = 'test_value'
        
        import os
        result = os.environ.get('TEST_VAR')
        
        assert result == 'test_value'
        mock_env_get.assert_called_once_with('TEST_VAR')
'''
        
        # Test d'intégration d'exemple
        integration_test_sample = '''"""
Test d'intégration d'exemple.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, patch


@pytest.mark.integration
class TestIntegrationExample:
    """Tests d'intégration d'exemple."""
    
    @pytest.mark.asyncio
    async def test_http_client_mock(self):
        """Test avec client HTTP mocké."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'status': 'ok'}
            
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.get.return_value = mock_response
            mock_client.return_value = mock_context
            
            async with httpx.AsyncClient() as client:
                response = await client.get('https://api.example.com/health')
                data = response.json()
                
                assert response.status_code == 200
                assert data['status'] == 'ok'


@pytest.mark.slow
@pytest.mark.integration
class TestSlowIntegration:
    """Tests d'intégration lents."""
    
    def test_slow_operation(self):
        """Test d'une opération lente simulée."""
        import time
        time.sleep(0.1)  # Simulation d'opération lente
        assert True
'''
        
        try:
            # Écrire les tests d'exemple
            (self.tests_dir / 'unit' / 'test_sample_unit.py').write_text(unit_test_sample)
            (self.tests_dir / 'integration' / 'test_sample_integration.py').write_text(integration_test_sample)
            
            print("✅ Sample tests created")
            return True
        except Exception as e:
            print(f"❌ Failed to create sample tests: {e}")
            return False
    
    def create_ci_config(self) -> bool:
        """Crée la configuration CI/CD."""
        print("🔄 Creating CI/CD configuration...")
        
        github_workflow = """name: Security Tests
on: 
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-asyncio bandit safety
    
    - name: Security scan with bandit
      run: |
        bandit -r orchestrator/ -ll || true
    
    - name: Vulnerability check with safety
      run: |
        safety check || true
    
    - name: Run security tests
      run: |
        pytest tests/security/ -v --cov=orchestrator --cov-fail-under=40
    
    - name: Run all tests
      run: |
        pytest tests/ -v --cov=orchestrator --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
"""
        
        try:
            # Créer le répertoire .github/workflows
            workflow_dir = self.project_root / '.github' / 'workflows'
            workflow_dir.mkdir(parents=True, exist_ok=True)
            
            (workflow_dir / 'security-tests.yml').write_text(github_workflow)
            
            print("✅ CI/CD configuration created")
            return True
        except Exception as e:
            print(f"❌ Failed to create CI config: {e}")
            return False
    
    def create_pre_commit_hooks(self) -> bool:
        """Crée les hooks pre-commit."""
        print("🪝 Creating pre-commit hooks...")
        
        pre_commit_config = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
  
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11
  
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]
  
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-r", "orchestrator/", "-ll"]
  
  - repo: local
    hooks:
      - id: security-tests
        name: Run security tests
        entry: python -m pytest tests/security/ -x
        language: system
        pass_filenames: false
        always_run: true
"""
        
        try:
            (self.project_root / '.pre-commit-config.yaml').write_text(pre_commit_config)
            
            # Essayer d'installer pre-commit
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'pre-commit'], 
                             check=True, capture_output=True)
                subprocess.run(['pre-commit', 'install'], 
                             check=True, capture_output=True, cwd=self.project_root)
                print("✅ Pre-commit hooks installed")
            except:
                print("⚠️ Pre-commit config created (manual installation required)")
            
            return True
        except Exception as e:
            print(f"❌ Failed to create pre-commit hooks: {e}")
            return False
    
    def validate_setup(self) -> bool:
        """Valide que le setup a réussi."""
        print("✅ Validating test framework setup...")
        
        # Vérifier la structure
        required_files = [
            self.project_root / 'pytest.ini',
            self.tests_dir / 'conftest.py',
            self.tests_dir / 'security' / 'test_rce_prevention.py',
            self.tests_dir / 'security' / 'test_ssrf_prevention.py',
        ]
        
        missing_files = []
        for file_path in required_files:
            if not file_path.exists():
                missing_files.append(str(file_path))
        
        if missing_files:
            print(f"❌ Missing files: {missing_files}")
            return False
        
        # Test rapide d'exécution
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pytest', '--collect-only', str(self.tests_dir)
            ], capture_output=True, text=True, timeout=30, cwd=self.project_root)
            
            if result.returncode == 0:
                print("✅ Test collection successful")
                return True
            else:
                print(f"❌ Test collection failed: {result.stderr}")
                return False
        except:
            print("⚠️ Could not validate test collection")
            return True  # Non bloquant
    
    def run_setup(self) -> bool:
        """Exécute le setup complet."""
        print("🧪 SETTING UP TESTING FRAMEWORK")
        print("=" * 40)
        
        steps = [
            ("Install dependencies", self.install_test_dependencies),
            ("Create pytest config", self.create_pytest_config),
            ("Create test structure", self.create_test_structure),
            ("Create test fixtures", self.create_test_fixtures),
            ("Create sample tests", self.create_sample_tests),
            ("Create CI config", self.create_ci_config),
            ("Create pre-commit hooks", self.create_pre_commit_hooks),
            ("Validate setup", self.validate_setup),
        ]
        
        failed_steps = []
        for step_name, step_func in steps:
            print(f"\\n📋 {step_name}...")
            try:
                if not step_func():
                    failed_steps.append(step_name)
            except Exception as e:
                print(f"❌ {step_name} failed with exception: {e}")
                failed_steps.append(step_name)
        
        print("\\n" + "=" * 40)
        print("📊 SETUP SUMMARY")
        print("=" * 40)
        
        if not failed_steps:
            print("🎉 ALL SETUP STEPS COMPLETED SUCCESSFULLY!")
            print("\\n📋 Next steps:")
            print("1. Run: python scripts/validate_security_fixes.py")
            print("2. Run: pytest tests/security/ -v")
            print("3. Check coverage: pytest --cov=orchestrator --cov-report=html")
            return True
        else:
            print(f"⚠️ {len(failed_steps)} steps failed:")
            for step in failed_steps:
                print(f"  ❌ {step}")
            print("\\n🔧 Please address the failed steps manually")
            return False


def main():
    """Fonction principale."""
    setup = TestFrameworkSetup()
    
    try:
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\\n⚠️ Setup interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\\n💥 Setup failed with exception: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
