"""
Analyseur de code sécurisé avec validation AST et sandboxing.
Implémentation du correctif critique pour la vulnérabilité RCE.
"""

import ast
import hashlib
import tempfile
import shlex
import ipaddress
import time
from pathlib import Path
from subprocess import run, PIPE, TimeoutExpired
from typing import Dict, List, Set, Optional, Tuple
from contextlib import contextmanager
import uuid
import json
import logging

logger = logging.getLogger(__name__)


class SecurityError(Exception):
    """Exception levée pour les violations de sécurité."""
    pass


class ValidationError(Exception):
    """Exception levée pour les erreurs de validation."""
    pass


class SecureCodeAnalyzer:
    """Analyseur de code sécurisé avec validation AST et sandboxing."""
    
    # Whitelist stricte des imports autorisés
    ALLOWED_IMPORTS: Set[str] = {
        'json', 'datetime', 'typing', 'dataclasses', 'collections', 'itertools',
        'functools', 'operator', 'math', 'random', 'string', 'time', 're',
        'pydantic', 'fastapi', 'langchain', 'numpy', 'pandas', 'requests',
        'httpx', 'asyncio', 'pathlib', 'uuid', 'hashlib', 'base64'
    }
    
    # Patterns dangereux bloqués (plus strict que les validateurs existants)
    DANGEROUS_PATTERNS: List[str] = [
        r'eval\s*\(',
        r'exec\s*\(',
        r'compile\s*\(',
        r'__import__\s*\(',
        r'getattr\s*\(',
        r'setattr\s*\(',
        r'delattr\s*\(',
        r'globals\s*\(',
        r'locals\s*\(',
        r'vars\s*\(',
        r'open\s*\(',
        r'file\s*\(',
        r'input\s*\(',
        r'raw_input\s*\(',
        r'\.system\s*\(',
        r'\.popen\s*\(',
        r'\.spawn\s*\(',
        r'subprocess\.',
        r'os\.',
        r'sys\.',
        r'socket\.',
        r'shutil\.',
        r'tempfile\.',
        r'importlib\.',
        r'ctypes\.',
        r'multiprocessing\.',
        r'threading\.',
        r'pty\.',
        r'signal\.'
    ]
    
    # Imports critiques interdits
    FORBIDDEN_IMPORTS: Set[str] = {
        'os', 'subprocess', 'sys', 'socket', 'shutil', 'tempfile',
        'importlib', 'ctypes', 'multiprocessing', 'threading',
        'pty', 'signal', 'gc', 'weakref', 'inspect', 'types',
        'code', 'codeop', 'py_compile', 'compileall', 'dis',
        'pickle', 'copyreg', 'shelve', 'marshal', 'dbm'
    }
    
    def __init__(self, sandbox_dir: Optional[Path] = None):
        """
        Initialise l'analyseur sécurisé.
        
        Args:
            sandbox_dir: Répertoire de sandbox (optionnel)
        """
        self.sandbox_dir = sandbox_dir or Path("/tmp/secure_sandbox")
        self.sandbox_dir.mkdir(exist_ok=True, mode=0o755)
        self._setup_sandbox_environment()
        
    def _setup_sandbox_environment(self) -> None:
        """Configure l'environnement de sandbox."""
        # Nettoyage périodique des fichiers temporaires
        try:
            import time
            current_time = time.time()
            for file_path in self.sandbox_dir.glob("*.py"):
                if file_path.stat().st_mtime < current_time - 3600:  # 1 heure
                    file_path.unlink(missing_ok=True)
        except Exception as e:
            logger.warning(f"Sandbox cleanup failed: {e}")
    
    def validate_code_safety(self, code: str) -> bool:
        """
        Valide que le code est sûr à analyser.
        
        Args:
            code: Code Python à valider
            
        Returns:
            bool: True si le code est sûr
            
        Raises:
            SecurityError: Si le code est dangereux
            ValidationError: Si le code est invalide
        """
        if not code or not code.strip():
            raise ValidationError("Code is empty or whitespace-only")
        
        # Limitation de taille stricte
        if len(code) > 10000:  # 10KB max pour l'analyse
            raise SecurityError("Code size exceeds limit (10KB max)")
        
        # 1. Vérification patterns dangereux par regex
        code_lower = code.lower()
        for pattern in self.DANGEROUS_PATTERNS:
            import re
            if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
                raise SecurityError(f"Dangerous pattern detected: {pattern}")
        
        # 2. Validation AST stricte
        try:
            tree = ast.parse(code)
            self._validate_ast_nodes(tree)
        except SyntaxError as e:
            raise ValidationError(f"Invalid Python syntax: {e}")
        
        return True
    
    def _validate_ast_nodes(self, node: ast.AST) -> None:
        """
        Valide récursivement les nœuds AST.
        
        Args:
            node: Nœud AST à valider
            
        Raises:
            SecurityError: Si un nœud dangereux est détecté
        """
        for child in ast.walk(node):
            # Bloquer les imports non autorisés
            if isinstance(child, ast.Import):
                for alias in child.names:
                    if alias.name in self.FORBIDDEN_IMPORTS:
                        raise SecurityError(f"Forbidden import: {alias.name}")
                    if alias.name not in self.ALLOWED_IMPORTS:
                        raise SecurityError(f"Import not in whitelist: {alias.name}")
            
            elif isinstance(child, ast.ImportFrom):
                if child.module and child.module in self.FORBIDDEN_IMPORTS:
                    raise SecurityError(f"Forbidden import from: {child.module}")
                if child.module and child.module not in self.ALLOWED_IMPORTS:
                    raise SecurityError(f"Import from not in whitelist: {child.module}")
            
            # Bloquer les appels de fonctions dangereuses
            elif isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    dangerous_funcs = {'eval', 'exec', 'compile', '__import__', 'open'}
                    if child.func.id in dangerous_funcs:
                        raise SecurityError(f"Dangerous function call: {child.func.id}")
                
                elif isinstance(child.func, ast.Attribute):
                    # Bloquer les appels comme os.system, subprocess.run, etc.
                    if hasattr(child.func, 'attr'):
                        dangerous_methods = {'system', 'popen', 'spawn', 'run', 'call'}
                        if child.func.attr in dangerous_methods:
                            raise SecurityError(f"Dangerous method call: {child.func.attr}")
    
    @contextmanager
    def _secure_temp_file(self, code: str):
        """
        Crée un fichier temporaire sécurisé dans le sandbox.
        
        Args:
            code: Code à écrire dans le fichier
            
        Yields:
            str: Chemin du fichier temporaire
        """
        # Générer un nom de fichier unique et sécurisé
        code_hash = hashlib.sha256(code.encode()).hexdigest()[:16]
        timestamp = int(time.time())
        filename = f"analysis_{timestamp}_{code_hash}.py"
        file_path = self.sandbox_dir / filename
        
        try:
            # Écriture sécurisée avec permissions restrictives
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            file_path.chmod(0o644)  # Lecture seule pour le groupe/autres
            
            yield str(file_path)
            
        finally:
            # Nettoyage automatique
            try:
                file_path.unlink(missing_ok=True)
            except Exception as e:
                logger.warning(f"Failed to clean up temp file {file_path}: {e}")
    
    async def analyze_code_secure(self, code: str) -> str:
        """
        Analyse le code de manière sécurisée.
        
        Args:
            code: Code Python à analyser
            
        Returns:
            str: Résultat de l'analyse
            
        Raises:
            SecurityError: Si le code est dangereux ou si l'analyse échoue
        """
        # 1. Validation préalable obligatoire
        self.validate_code_safety(code)
        
        # 2. Création fichier temporaire sécurisé
        with self._secure_temp_file(code) as temp_file_path:
            # 3. Exécution sandboxée avec restrictions maximales
            try:
                result = run(
                    ['pylint', 
                     '--score=no', 
                     '--reports=no',
                     '--disable=all',
                     '--enable=E,W',  # Erreurs et warnings uniquement
                     temp_file_path],
                    stdout=PIPE,
                    stderr=PIPE,
                    text=True,
                    timeout=10,  # Timeout strict (réduit de 30 à 10s)
                    cwd=str(self.sandbox_dir),  # Répertoire de travail sandbox
                    env={
                        'PATH': '/usr/bin:/bin',  # Environnement minimal
                        'HOME': '/tmp',  # Pas d'accès home
                        'TMPDIR': str(self.sandbox_dir)  # Tmp dirigé vers sandbox
                    }
                )
                
                # Nettoyage et formatage de la sortie
                output = result.stdout or result.stderr or "No issues detected"
                return self._sanitize_output(output)
                
            except TimeoutExpired:
                raise SecurityError("Code analysis timed out - potentially infinite loop")
            except FileNotFoundError:
                raise SecurityError("Analysis tool not available (pylint missing)")
            except Exception as e:
                logger.error(f"Secure analysis failed: {e}")
                raise SecurityError(f"Analysis failed: {str(e)}")
    
    def _sanitize_output(self, output: str) -> str:
        """
        Nettoie la sortie de l'analyse pour éviter les fuites d'information.
        
        Args:
            output: Sortie brute de pylint
            
        Returns:
            str: Sortie nettoyée
        """
        # Supprimer les chemins de fichiers temporaires (Windows et Unix)
        import re
        # Remplacer le chemin sandbox complet par [FILE]
        sanitized = re.sub(rf'{re.escape(str(self.sandbox_dir))}/[^:\s]+', '[FILE]', output)
        sanitized = re.sub(rf'{re.escape(str(self.sandbox_dir))}\\[^:\s]+', '[FILE]', sanitized)
        
        # Pattern générique pour les chemins temporaires
        sanitized = re.sub(r'/tmp/secure_sandbox/[^:\s]+', '[FILE]', sanitized)
        sanitized = re.sub(r'[A-Z]:\\[^:\s]*temp[^:\s]*\\[^:\s]+', '[FILE]', sanitized)
        
        # Limiter la longueur de la sortie
        if len(sanitized) > 2000:
            sanitized = sanitized[:2000] + "\n... (output truncated for security)"
        
        return sanitized
    
    def get_security_metrics(self) -> Dict[str, any]:
        """
        Retourne les métriques de sécurité de l'analyseur.
        
        Returns:
            Dict: Métriques de sécurité
        """
        return {
            'allowed_imports_count': len(self.ALLOWED_IMPORTS),
            'forbidden_imports_count': len(self.FORBIDDEN_IMPORTS),
            'dangerous_patterns_count': len(self.DANGEROUS_PATTERNS),
            'sandbox_dir': str(self.sandbox_dir),
            'max_code_size': 10000,
            'analysis_timeout': 10
        }


# Instance globale pour réutilisation
_secure_analyzer = None

def get_secure_analyzer() -> SecureCodeAnalyzer:
    """
    Retourne l'instance globale de l'analyseur sécurisé.
    
    Returns:
        SecureCodeAnalyzer: Instance de l'analyseur
    """
    global _secure_analyzer
    if _secure_analyzer is None:
        _secure_analyzer = SecureCodeAnalyzer()
    return _secure_analyzer


# Fonction de migration pour remplacer python_linter_tool
async def secure_python_linter_tool(code: str) -> str:
    """
    Version sécurisée de python_linter_tool.
    Cette fonction remplace complètement l'ancienne implémentation vulnérable.
    
    Args:
        code: Code Python à analyser
        
    Returns:
        str: Résultat de l'analyse sécurisée
    """
    analyzer = get_secure_analyzer()
    
    try:
        return await analyzer.analyze_code_secure(code)
    except SecurityError as e:
        # Log de sécurité pour audit
        logger.warning(f"Security violation in code analysis: {e}")
        return f"Security validation failed: {str(e)}"
    except ValidationError as e:
        return f"Code validation failed: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in secure analysis: {e}")
        return "Analysis service temporarily unavailable"
