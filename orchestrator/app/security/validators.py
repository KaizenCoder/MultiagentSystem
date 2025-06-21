"""
Validateurs de scurit pour prvenir les vulnrabilits identifies.

Ce module contient les validateurs pour :
- Code injection via LLM (validation AST + blacklist)
- SSRF via Memory API (validation URLs)
- Input sanitization
"""

import ast
import re
import html
import ipaddress
from typing import Tuple, Optional
from urllib.parse import urlparse
from logging_manager_optimized import LoggingManager

# LoggingManager NextGeneration - Tool/Utility
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={
            "logger_name": "CodeValidator",
            "log_level": "INFO",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": True
        })


class CodeValidator:
    """Validateur pour prvenir l'injection de code via LLM."""
    
    # Patterns dangereux  bloquer
    DANGEROUS_PATTERNS = [
        r'import\s+(os|subprocess|sys|socket|shutil|tempfile)',
        r'from\s+(os|subprocess|sys|socket|shutil|tempfile)',
        r'__import__\s*\(',
        r'eval\s*\(',
        r'exec\s*\(',
        r'compile\s*\(',
        r'globals\s*\(',
        r'locals\s*\(',
        r'getattr\s*\(',
        r'setattr\s*\(',
        r'delattr\s*\(',
        r'open\s*\(',
        r'file\s*\(',
        r'input\s*\(',
        r'raw_input\s*\(',
        r'\.\s*system\s*\(',
        r'\.\s*popen\s*\(',
        r'\.\s*spawn\s*\(',
    ]
    
    @staticmethod
    def validate_python_code(code: str) -> Tuple[bool, Optional[str]]:
        """
        Valide que le code Python est sr avant excution.
        
        Args:
            code: Code Python  valider
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        if not code or not code.strip():
            return False, "Code is empty"
        
        # Limitation de taille pour viter les attaques DoS
        if len(code) > 50000:
            return False, "Code too large (>50KB)"
        
        # Vrification syntaxique
        try:
            ast.parse(code)
        except SyntaxError as e:
            logger.warning(f"Code syntax validation failed: {e}")
            return False, f"Syntax error: {str(e)}"
        
        # Vrification des patterns dangereux
        for pattern in CodeValidator.DANGEROUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                logger.warning(f"Dangerous pattern detected: {pattern}")
                return False, f"Potentially unsafe code pattern detected"
        
        return True, None


class NetworkValidator:
    """Validateur pour prvenir les attaques SSRF."""
    
    # IPs et domaines  bloquer
    BLOCKED_IPS = [
        "127.0.0.1",
        "127.1",        # Variation IP raccourcie
        "127.0.1",      # Variation IP raccourcie
        "0x7f000001",   # Hex encoding de 127.0.0.1
        "2130706433",   # Decimal encoding de 127.0.0.1
        "localhost",
        "0.0.0.0",
    ]
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, Optional[str]]:
        """
        Valide qu'une URL ne pointe pas vers des ressources internes.
        
        Args:
            url: URL  valider
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        if not url:
            return False, "URL is empty"
        
        try:
            parsed = urlparse(url)
            
            if not parsed.scheme:
                return False, "URL must have a scheme (http/https)"
            
            if parsed.scheme not in ['http', 'https']:
                return False, "Protocol not allowed - only HTTP/HTTPS protocols permitted for security"
            
            if not parsed.hostname:
                return False, "URL must have a hostname"
            
            # Vrification des hostnames bloqus
            if parsed.hostname.lower() in NetworkValidator.BLOCKED_IPS:
                return False, f"Private/internal hostname blocked: {parsed.hostname}"
            
            # Vrification des IPs prives
            try:
                ip = ipaddress.ip_address(parsed.hostname)
                if ip.is_private or ip.is_loopback or ip.is_link_local:
                    return False, f"Private/internal IP address not allowed: {ip}"
            except ValueError:
                # C'est un nom de domaine, pas une IP - OK
                pass
            
            # Vrification des ports suspects
            if parsed.port and parsed.port in [22, 23, 25, 53, 135, 139, 445, 1433, 3306, 5432, 6379]:
                return False, f"Access to port {parsed.port} not allowed"
            
            return True, None
            
        except Exception as e:
            logger.warning(f"URL validation error: {e}")
            return False, f"Invalid URL format"
    
    @staticmethod
    def validate_memory_api_url(url: str) -> Tuple[bool, Optional[str]]:
        """
        Validation spcifique pour l'URL de l'API Memory.
        
        Args:
            url: URL de l'API Memory
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        if not url:
            return False, "URL is empty"
        
        try:
            parsed = urlparse(url)
            
            if not parsed.scheme:
                return False, "URL must have a scheme (http/https)"
            
            if parsed.scheme not in ['http', 'https']:
                return False, "Protocol not allowed - only HTTP/HTTPS protocols permitted for security"
            
            if not parsed.hostname:
                return False, "URL must have a hostname"
            
            # Vrifier les ports dangereux mme pour localhost
            if parsed.port and parsed.port in [22, 23, 25, 53, 135, 139, 445, 1433, 3306, 5432, 6379]:
                return False, f"Access to port {parsed.port} not allowed for security"
            
            # Permettre localhost et memory_api pour Docker/dveloppement seulement avec ports srs
            if parsed.hostname.lower() in ['localhost', 'memory_api', '127.0.0.1']:
                # Port par dfaut 8001 ou HTTPS 443 autoriss
                if not parsed.port or parsed.port in [8001, 443, 80]:
                    return True, None
                else:
                    return False, f"Port {parsed.port} not allowed for localhost access"
            
            # Pour les autres URLs, appliquer les rgles strictes
            return NetworkValidator.validate_url(url)
            
        except Exception as e:
            logger.warning(f"Memory API URL validation error: {e}")
            return False, f"Invalid URL format"


class InputSanitizer:
    """Sanitisation des entres utilisateur."""
    
    @staticmethod
    def sanitize_task_description(description: str) -> str:
        """
        Sanitise la description de tche.
        
        Args:
            description: Description  sanitiser
            
        Returns:
            str: Description sanitise
        """
        if not description:
            return ""
        
        # chapper HTML
        sanitized = html.escape(description)
        
        # Limiter la longueur
        if len(sanitized) > 5000:
            sanitized = sanitized[:5000]
        
        # Supprimer les caractres potentiellement dangereux
        sanitized = re.sub(r'[<>"\']', '', sanitized)
        
        # Nettoyer les caractres de contrle
        sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', sanitized)
        
        return sanitized.strip()
    
    @staticmethod
    def sanitize_session_id(session_id: str) -> Optional[str]:
        """
        Valide et sanitise un ID de session.
        
        Args:
            session_id: ID de session  valider
            
        Returns:
            Optional[str]: ID de session sanitis ou None si invalide
        """
        if not session_id:
            return None
        
        # Doit tre un UUID valide
        uuid_pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
        if re.match(uuid_pattern, session_id.lower()):
            return session_id.lower()
        
        return None
    
    @staticmethod
    def sanitize_code_context(code_context: str) -> str:
        """
        Sanitise le contexte de code.
        
        Args:
            code_context: Contexte de code  sanitiser
            
        Returns:
            str: Contexte sanitis
        """
        if not code_context:
            return ""
        
        # Limiter la taille
        if len(code_context) > 50000:
            code_context = code_context[:50000]
        
        # Nettoyer les caractres de contrle dangereux
        sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', code_context)
        
        return sanitized.strip()

    @staticmethod
    def sanitize_code_input(code_input: str) -> str:
        """
        Sanitise l'entre de code pour les outils de gnration.
        
        Args:
            code_input: Code d'entre  sanitiser
            
        Returns:
            str: Code sanitis ou chane vide si invalide
        """
        if not code_input:
            return ""
        
        # Limiter la taille (plus restrictif que code_context)
        if len(code_input) > 10000:
            return ""
        
        # Nettoyer les caractres de contrle dangereux
        sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', code_input)
        
        # Vrifier que le code sanitis n'est pas vide
        if not sanitized.strip():
            return ""
        
        return sanitized.strip()

    @staticmethod
    def sanitize_shell_command(command: str) -> str:
        """
        Sanitizes a shell command by removing potentially dangerous characters.
        This is a basic sanitization and should be used with command whitelisting.
        """
        if not command:
            return ""
        # Remove characters other than alphanum, spaces, hyphens, underscores, slashes, dots, pipes, and quotes for arguments.
        sanitized = re.sub(r'[^a-zA-Z0-9\s\-_/|\. \'"]', '', command)
        return sanitized.strip()
