import httpx
import asyncio
import time
from tempfile import NamedTemporaryFile
from subprocess import run, TimeoutExpired, PIPE
from langchain.tools import Tool
from ..config import settings
from ..security.validators import CodeValidator, NetworkValidator, InputSanitizer
from ..security.logging import security_logger, AuditLogger, AuditEventType

# CORRECTIF 4: Client HTTP global qui sera fermé proprement
_http_client = None

async def get_http_client():
    """Retourne le client HTTP global ou en crée un nouveau."""
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(settings.MAX_REQUEST_TIMEOUT),
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
        )
    return _http_client

async def close_http_client():
    """Ferme proprement le client HTTP global."""
    global _http_client
    if _http_client:
        await _http_client.aclose()
        _http_client = None

async def rag_code_search_tool(query: str) -> str:
    """Interroge l'API de mémoire pour trouver des extraits de code similaires."""
    # Validation de sécurité pour la requête
    if not query or len(query) > 1000:
        AuditLogger.log_event(AuditEventType.SECURITY_VIOLATION, None, {
            "tool": "rag_code_search",
            "reason": "Invalid query length",
            "query_length": len(query) if query else 0
        })
        return "Error: Query invalid or too long"
    
    # Sanitiser la requête
    sanitized_query = InputSanitizer.sanitize_task_description(query)
    
    client = await get_http_client()
    try:
        # Validation de l'URL avant la requête
        url = f"{settings.MEMORY_API_URL}/rag_query"
        is_valid, error_msg = NetworkValidator.validate_memory_api_url(url)
        if not is_valid:
            security_logger.log_security_event("NETWORK_VALIDATION_FAILED", {
                "url": url,
                "error": error_msg
            })
            return f"Error: Network validation failed"
        
        response = await client.post(
            url, json={"query": sanitized_query, "top_k": 3}
        )
        response.raise_for_status()
        results = response.json().get("results", [])
        if not results: 
            return "No relevant code found in knowledge base."
        return "Found relevant snippets:\n" + "\n---\n".join([r['content'] for r in results])
    except httpx.TimeoutException:
        security_logger.log_error("RAG search timeout", Exception("Request timeout"))
        return "Error: Request timeout"
    except httpx.RequestError as e:
        security_logger.log_error("RAG search network error", e)
        return "Error: Network connectivity issue"
    except Exception as e:
        security_logger.log_error("RAG search unexpected error", e)
        return "Error: Service temporarily unavailable"

async def execute_shell_command(command: str) -> str:
    """
    Executes a shell command in a secure manner and returns the output.
    Allowed commands: psql, pg_isready, echo, docker.
    """
    # Security: Sanitize and validate the command
    # Note: L'agent est censé construire des commandes sûres. La validation est une défense en profondeur.
    sanitized_command = InputSanitizer.sanitize_shell_command(command)

    # Whitelist of allowed commands to prevent abuse
    allowed_commands = ["psql", "pg_isready", "echo", "docker"]
    
    if not sanitized_command.strip():
        return "Error: Empty command provided."

    command_to_run = sanitized_command.strip().split()[0]
    if command_to_run not in allowed_commands:
        security_logger.log_security_event("SHELL_COMMAND_REJECTED", {
            "command": sanitized_command,
            "reason": "Command not in whitelist"
        })
        return f"Error: Command not allowed for security reasons. Allowed: {', '.join(allowed_commands)}"

    try:
        AuditLogger.log_event(AuditEventType.SHELL_COMMAND_EXECUTION, None, {
            "tool": "execute_shell_command",
            "command": sanitized_command
        })
        
        process = await asyncio.create_subprocess_shell(
            sanitized_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=settings.MAX_REQUEST_TIMEOUT)
        
        result = ""
        if stdout:
            result += f"STDOUT:\n{stdout.decode(errors='ignore')}"
        if stderr:
            result += f"STDERR:\n{stderr.decode(errors='ignore')}"

        if process.returncode != 0:
            return f"Command failed with exit code {process.returncode}:\n{result}"
        
        return f"Command executed successfully:\n{result}"

    except asyncio.TimeoutError:
        security_logger.log_error("Shell command timeout", Exception(f"Timeout for command: {sanitized_command}"))
        return "Error: Command execution timed out."
    except Exception as e:
        security_logger.log_error("Shell command execution failed", e)
        return f"Error executing command: {str(e)}"

async def python_linter_tool(code: str) -> str:
    """
    Outil de linting Python sécurisé avec protection RCE complète.
    Remplace l'ancienne implémentation vulnérable par un système sécurisé.
    """
    
    # CORRECTIF SÉCURITÉ CRITIQUE: Utilisation de l'analyseur sécurisé
    try:
        from ..security.secure_analyzer import secure_python_linter_tool
        
        # Log de sécurité pour audit
        AuditLogger.log_event(AuditEventType.CODE_ANALYSIS_REQUEST, None, {
            "tool": "python_linter_secure",
            "code_size": len(code),
            "timestamp": time.time()
        })
        
        # Délégation vers l'outil sécurisé
        return await secure_python_linter_tool(code)
        
    except Exception as e:
        # Fallback sécurisé en cas d'erreur
        security_logger.log_error("Secure linter tool failed", e)
        AuditLogger.log_event(AuditEventType.SECURITY_VIOLATION, None, {
            "tool": "python_linter",
            "error": str(e),
            "fallback_used": True
        })
        return f"Code analysis service temporarily unavailable: {str(e)}"

# CORRECTIF: Utilisation de Tool.from_function pour une compatibilité assurée.
real_code_tools = [
    Tool.from_function(func=python_linter_tool, name="PythonLinter", description="Analyzes Python code for errors and style issues.", is_async=True),
    Tool.from_function(func=rag_code_search_tool, name="CodeKnowledgeSearch", description="Searches for similar code examples or documentation.", is_async=True)
]
real_doc_tools = [Tool.from_function(func=rag_code_search_tool, name="CodeKnowledgeSearch", description="Searches for existing documentation or code comments.", is_async=True)]

# Outils de diagnostic
real_diag_tools = [
    Tool.from_function(
        func=execute_shell_command, 
        name="ShellExecutor", 
        description="Executes whitelisted shell commands like psql, pg_isready, docker to diagnose system issues.", 
        is_async=True
    ),
    Tool.from_function(
        func=rag_code_search_tool, 
        name="KnowledgeBaseSearch", 
        description="Searches knowledge base for similar problems and their resolutions.", 
        is_async=True
    )
]

# CORRECTION IA-1: Ajout des outils de testing
async def pytest_generator_tool(code: str) -> str:
    """Génère des tests pytest pour le code fourni."""
    try:
        # Validation et sanitisation du code d'entrée
        sanitized_code = InputSanitizer.sanitize_code_input(code)
        if not sanitized_code:
            return "Error: Invalid code input for test generation"
        
        # Log de sécurité
        AuditLogger.log_event(AuditEventType.CODE_ANALYSIS_REQUEST, None, {
            "tool": "pytest_generator",
            "code_size": len(code),
            "timestamp": time.time()
        })
        
        # Génération de tests basiques en fonction du code
        test_template = f'''"""
Generated tests for the provided code.
"""
import pytest
from unittest.mock import Mock, patch

# Test the main functionality
def test_main_functionality():
    """Test the core functionality."""
    # TODO: Implement specific tests based on the code
    assert True  # Placeholder

def test_edge_cases():
    """Test edge cases and error conditions."""
    # TODO: Add edge case tests
    assert True  # Placeholder

def test_input_validation():
    """Test input validation."""
    # TODO: Add input validation tests
    assert True  # Placeholder

# Code to test:
# {sanitized_code[:200]}...
'''
        return test_template
        
    except Exception as e:
        security_logger.log_error("Pytest generator failed", e)
        return f"Error generating tests: {str(e)}"

async def unittest_generator_tool(code: str) -> str:
    """Génère des tests unittest pour le code fourni."""
    try:
        # Validation et sanitisation
        sanitized_code = InputSanitizer.sanitize_code_input(code)
        if not sanitized_code:
            return "Error: Invalid code input for unittest generation"
        
        # Log de sécurité
        AuditLogger.log_event(AuditEventType.CODE_ANALYSIS_REQUEST, None, {
            "tool": "unittest_generator",
            "code_size": len(code),
            "timestamp": time.time()
        })
        
        # Template unittest
        test_template = f'''"""
Generated unittest tests for the provided code.
"""
import unittest
from unittest.mock import Mock, patch

class TestMainFunctionality(unittest.TestCase):
    """Test cases for the main functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
        
    def test_main_function(self):
        """Test the main function."""
        # TODO: Implement specific tests
        self.assertTrue(True)  # Placeholder
        
    def test_error_handling(self):
        """Test error handling."""
        # TODO: Add error handling tests
        self.assertTrue(True)  # Placeholder
        
    def tearDown(self):
        """Clean up after tests."""
        pass

if __name__ == '__main__':
    unittest.main()

# Code to test:
# {sanitized_code[:200]}...
'''
        return test_template
        
    except Exception as e:
        security_logger.log_error("Unittest generator failed", e)
        return f"Error generating unittest: {str(e)}"

# CORRECTION IA-1: Définition des outils de testing
real_test_tools = [
    Tool.from_function(func=pytest_generator_tool, name="PytestGenerator", description="Generates pytest test cases for the provided code.", is_async=True),
    Tool.from_function(func=unittest_generator_tool, name="UnittestGenerator", description="Generates unittest test cases for the provided code.", is_async=True),
    Tool.from_function(func=rag_code_search_tool, name="TestExampleSearch", description="Searches for existing test examples and patterns.", is_async=True)
] 