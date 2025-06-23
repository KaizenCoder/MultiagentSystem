import ast
import re
import hashlib
from typing import List, Dict, Any
from agent_factory_implementation.core.agent_factory_architecture import Agent, Task, Result

class AgentMAINTENANCE09GestionnaireSecurite(Agent):
    """
    Agent chargé de la sécurité du code Python :
    - Détecte les vulnérabilités de sécurité communes
    - Identifie les pratiques non sécurisées
    - Scanne les injections potentielles
    - Vérifie l'usage sécurisé des fonctions dangereuses
    - Analyse les patterns de gestion des mots de passe et secrets
    """
    
    def __init__(self, agent_id="agent_MAINTENANCE_09_gestionnaire_securite", version="1.0", description="Analyse et sécurise le code Python.", status="enabled"):
        super().__init__(agent_id, version, description, "security_manager", status)
        
        # Fonctions dangereuses à éviter
        self.dangerous_functions = {
            'eval': {
                'severity': 'CRITICAL',
                'reason': 'Exécution de code arbitraire',
                'alternatives': 'ast.literal_eval() pour données sûres, ou validation stricte'
            },
            'exec': {
                'severity': 'CRITICAL', 
                'reason': 'Exécution de code arbitraire',
                'alternatives': 'Restructurer le code pour éviter l\'exécution dynamique'
            },
            'compile': {
                'severity': 'HIGH',
                'reason': 'Compilation de code potentiellement malveillant',
                'alternatives': 'Valider strictement les entrées avant compilation'
            },
            'input': {
                'severity': 'MEDIUM',
                'reason': 'Injection de code possible en Python 2',
                'alternatives': 'raw_input() en Python 2, input() est sûr en Python 3'
            },
            '__import__': {
                'severity': 'HIGH',
                'reason': 'Import dynamique non contrôlé',
                'alternatives': 'importlib avec validation des noms de modules'
            }
        }
        
        # Modules système dangereux
        self.dangerous_modules = {
            'os.system': {
                'severity': 'CRITICAL',
                'reason': 'Injection de commandes shell',
                'alternatives': 'subprocess.run() avec shell=False'
            },
            'subprocess.call': {
                'severity': 'HIGH',
                'reason': 'Injection potentielle si shell=True',
                'alternatives': 'subprocess.run() avec liste d\'arguments'
            },
            'subprocess.Popen': {
                'severity': 'MEDIUM',
                'reason': 'Vérifier l\'usage de shell=True',
                'alternatives': 'Utiliser shell=False et liste d\'arguments'
            },
            'pickle.loads': {
                'severity': 'HIGH',
                'reason': 'Désérialisation non sécurisée',
                'alternatives': 'json, ou pickle avec signature/validation'
            },
            'marshal.loads': {
                'severity': 'HIGH',
                'reason': 'Désérialisation dangereuse',
                'alternatives': 'json ou autres formats sécurisés'
            }
        }
        
        # Patterns de secrets potentiels
        self.secret_patterns = [
            (re.compile(r'password\s*=\s*["\'][^"\']+["\']', re.IGNORECASE), 'Mot de passe en dur'),
            (re.compile(r'api_key\s*=\s*["\'][^"\']+["\']', re.IGNORECASE), 'Clé API en dur'),
            (re.compile(r'secret\s*=\s*["\'][^"\']+["\']', re.IGNORECASE), 'Secret en dur'),
            (re.compile(r'token\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', re.IGNORECASE), 'Token en dur'),
            (re.compile(r'["\'][A-Za-z0-9+/]{40,}={0,2}["\']'), 'Possible clé encodée en base64'),
            (re.compile(r'-----BEGIN [A-Z ]+-----'), 'Clé cryptographique'),
        ]
        
        # Patterns d'injection SQL
        self.sql_injection_patterns = [
            re.compile(r'execute\s*\(\s*["\'].*%s.*["\']', re.IGNORECASE),
            re.compile(r'query\s*\(\s*["\'].*\+.*["\']', re.IGNORECASE),
            re.compile(r'["\'].*\+.*["\'].*WHERE', re.IGNORECASE),
        ]

    async def startup(self):
        await super().startup()
        self.log("Gestionnaire de sécurité prêt. Chargement des règles de sécurité...")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "security_scan":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni.")

        self.log(f"🔐 Analyse de sécurité pour : {file_path}")

        try:
            # Analyses de sécurité complètes
            vulnerabilities = []
            
            # 1. Analyse AST pour fonctions dangereuses
            ast_vulnerabilities = self._analyze_ast_security(code)
            vulnerabilities.extend(ast_vulnerabilities)
            
            # 2. Analyse des patterns de texte
            text_vulnerabilities = self._analyze_text_patterns(code)
            vulnerabilities.extend(text_vulnerabilities)
            
            # 3. Analyse des secrets potentiels
            secret_issues = self._detect_hardcoded_secrets(code)
            vulnerabilities.extend(secret_issues)
            
            # 4. Analyse des injections SQL
            sql_issues = self._detect_sql_injections(code)
            vulnerabilities.extend(sql_issues)
            
            # 5. Analyse des permissions de fichiers
            file_issues = self._analyze_file_operations(code)
            vulnerabilities.extend(file_issues)
            
            # 6. Calcul du score de sécurité
            security_score = self._calculate_security_score(vulnerabilities)
            
            # 7. Génération des recommandations
            recommendations = self._generate_security_recommendations(vulnerabilities)
            
            # 8. Génération du code sécurisé (suggestions)
            secured_suggestions = self._generate_secured_code_suggestions(code, vulnerabilities)

            report = {
                "file_path": file_path,
                "security_score": security_score,
                "vulnerabilities": vulnerabilities,
                "recommendations": recommendations,
                "secured_suggestions": secured_suggestions,
                "risk_level": self._determine_risk_level(vulnerabilities),
                "total_issues": len(vulnerabilities)
            }

            self.log(f"🔐 Analyse de sécurité terminée pour {file_path} - Score: {security_score}/100, Issues: {len(vulnerabilities)}")
            
            return Result(success=True, data={
                "security_report": report,
                "needs_security_review": security_score < 80 or any(v['severity'] == 'CRITICAL' for v in vulnerabilities)
            })

        except Exception as e:
            self.log(f"Erreur lors de l'analyse de sécurité de {file_path}: {e}", level="error")
            return Result(success=False, error=str(e))

    def _analyze_ast_security(self, code: str) -> List[Dict[str, Any]]:
        """Analyse AST pour détecter les fonctions dangereuses."""
        vulnerabilities = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Détection des appels de fonctions dangereuses
                if isinstance(node, ast.Call):
                    func_name = None
                    
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                    elif isinstance(node.func, ast.Attribute):
                        if isinstance(node.func.value, ast.Name):
                            func_name = f"{node.func.value.id}.{node.func.attr}"
                    
                    if func_name in self.dangerous_functions:
                        danger_info = self.dangerous_functions[func_name]
                        vulnerabilities.append({
                            'type': 'dangerous_function',
                            'function': func_name,
                            'line': getattr(node, 'lineno', 0),
                            'severity': danger_info['severity'],
                            'description': f"Usage de la fonction dangereuse '{func_name}'",
                            'reason': danger_info['reason'],
                            'recommendation': danger_info['alternatives']
                        })
                    
                    elif func_name in self.dangerous_modules:
                        danger_info = self.dangerous_modules[func_name]
                        vulnerabilities.append({
                            'type': 'dangerous_module_call',
                            'function': func_name,
                            'line': getattr(node, 'lineno', 0),
                            'severity': danger_info['severity'],
                            'description': f"Usage potentiellement dangereux de '{func_name}'",
                            'reason': danger_info['reason'],
                            'recommendation': danger_info['alternatives']
                        })
                
                # Détection des imports dangereux
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    self._check_dangerous_imports(node, vulnerabilities)
        
        except SyntaxError:
            # Le code a des erreurs de syntaxe, on ne peut pas l'analyser
            pass
        
        return vulnerabilities

    def _check_dangerous_imports(self, node: ast.AST, vulnerabilities: List[Dict[str, Any]]):
        """Vérifie les imports potentiellement dangereux."""
        dangerous_imports = ['pickle', 'marshal', 'subprocess', 'os']
        
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in dangerous_imports:
                    vulnerabilities.append({
                        'type': 'dangerous_import',
                        'module': alias.name,
                        'line': getattr(node, 'lineno', 0),
                        'severity': 'LOW',
                        'description': f"Import du module potentiellement dangereux '{alias.name}'",
                        'reason': 'Module nécessitant une utilisation prudente',
                        'recommendation': 'Vérifier l\'usage sécurisé de ce module'
                    })
        
        elif isinstance(node, ast.ImportFrom):
            if node.module in dangerous_imports:
                vulnerabilities.append({
                    'type': 'dangerous_from_import',
                    'module': node.module,
                    'line': getattr(node, 'lineno', 0),
                    'severity': 'LOW',
                    'description': f"Import depuis le module potentiellement dangereux '{node.module}'",
                    'reason': 'Module nécessitant une utilisation prudente',
                    'recommendation': 'Vérifier l\'usage sécurisé des fonctions importées'
                })

    def _analyze_text_patterns(self, code: str) -> List[Dict[str, Any]]:
        """Analyse les patterns de texte pour détecter des problèmes de sécurité."""
        vulnerabilities = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Shell=True dans subprocess
            if re.search(r'shell\s*=\s*True', line, re.IGNORECASE):
                vulnerabilities.append({
                    'type': 'shell_injection_risk',
                    'line': i,
                    'severity': 'HIGH',
                    'description': 'Usage de shell=True dans subprocess',
                    'reason': 'Risque d\'injection de commandes shell',
                    'recommendation': 'Utiliser shell=False et passer les arguments comme liste',
                    'code_snippet': line.strip()
                })
            
            # URL en dur avec credentials
            if re.search(r'https?://[^:]+:[^@]+@', line):
                vulnerabilities.append({
                    'type': 'url_with_credentials',
                    'line': i,
                    'severity': 'HIGH',
                    'description': 'URL contenant des identifiants',
                    'reason': 'Exposition de credentials en dur',
                    'recommendation': 'Utiliser des variables d\'environnement ou des fichiers de config',
                    'code_snippet': line.strip()
                })
            
            # Désactivation de vérification SSL
            if re.search(r'verify\s*=\s*False|ssl_verify\s*=\s*False', line, re.IGNORECASE):
                vulnerabilities.append({
                    'type': 'ssl_verification_disabled',
                    'line': i,
                    'severity': 'MEDIUM',
                    'description': 'Vérification SSL désactivée',
                    'reason': 'Risque d\'attaque man-in-the-middle',
                    'recommendation': 'Activer la vérification SSL ou utiliser des certificats personnalisés',
                    'code_snippet': line.strip()
                })
        
        return vulnerabilities

    def _detect_hardcoded_secrets(self, code: str) -> List[Dict[str, Any]]:
        """Détecte les secrets potentiellement en dur dans le code."""
        vulnerabilities = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern, description in self.secret_patterns:
                matches = pattern.finditer(line)
                for match in matches:
                    # Éviter les faux positifs évidents
                    matched_text = match.group()
                    if self._is_likely_real_secret(matched_text):
                        vulnerabilities.append({
                            'type': 'hardcoded_secret',
                            'line': i,
                            'severity': 'HIGH',
                            'description': description,
                            'reason': 'Secret potentiel stocké en dur dans le code',
                            'recommendation': 'Utiliser des variables d\'environnement ou un gestionnaire de secrets',
                            'code_snippet': line.strip()[:100] + ('...' if len(line.strip()) > 100 else '')
                        })
        
        return vulnerabilities

    def _is_likely_real_secret(self, text: str) -> bool:
        """Détermine si un texte est probablement un vrai secret."""
        # Ignorer les exemples évidents
        obvious_fake = ['password', 'secret', 'key', 'token', 'example', 'test', 'demo', 'sample']
        text_lower = text.lower()
        
        for fake in obvious_fake:
            if fake in text_lower and len(text) < 30:
                return False
        
        # Un secret réel a généralement plus de 8 caractères et contient différents types
        if len(text) < 8:
            return False
        
        # Vérifier la complexité minimale
        has_letter = any(c.isalpha() for c in text)
        has_digit = any(c.isdigit() for c in text)
        
        return has_letter and has_digit

    def _detect_sql_injections(self, code: str) -> List[Dict[str, Any]]:
        """Détecte les potentielles injections SQL."""
        vulnerabilities = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern in self.sql_injection_patterns:
                if pattern.search(line):
                    vulnerabilities.append({
                        'type': 'sql_injection_risk',
                        'line': i,
                        'severity': 'HIGH',
                        'description': 'Risque d\'injection SQL',
                        'reason': 'Construction de requête SQL par concaténation',
                        'recommendation': 'Utiliser des requêtes paramétrées ou un ORM',
                        'code_snippet': line.strip()
                    })
        
        return vulnerabilities

    def _analyze_file_operations(self, code: str) -> List[Dict[str, Any]]:
        """Analyse les opérations sur fichiers pour détecter des problèmes de sécurité."""
        vulnerabilities = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Ouverture de fichiers avec chemins non validés
            if re.search(r'open\s*\([^)]*\+[^)]*[\'"][^\'\"]*\.\.[^\'\"]*[\'"]', line):
                vulnerabilities.append({
                    'type': 'path_traversal_risk',
                    'line': i,
                    'severity': 'MEDIUM',
                    'description': 'Risque de traversée de répertoire',
                    'reason': 'Chemin de fichier construit par concaténation avec ".."',
                    'recommendation': 'Valider et nettoyer les chemins de fichiers',
                    'code_snippet': line.strip()
                })
            
            # Permissions de fichiers trop permissives
            if re.search(r'chmod\s*\([^)]*0?777', line):
                vulnerabilities.append({
                    'type': 'overly_permissive_file',
                    'line': i,
                    'severity': 'MEDIUM',
                    'description': 'Permissions de fichier trop permissives (777)',
                    'reason': 'Accès en lecture/écriture/exécution pour tous',
                    'recommendation': 'Utiliser des permissions plus restrictives',
                    'code_snippet': line.strip()
                })
        
        return vulnerabilities

    def _calculate_security_score(self, vulnerabilities: List[Dict[str, Any]]) -> int:
        """Calcule un score de sécurité sur 100."""
        score = 100
        
        severity_penalties = {
            'CRITICAL': 25,
            'HIGH': 15,
            'MEDIUM': 8,
            'LOW': 3
        }
        
        for vuln in vulnerabilities:
            penalty = severity_penalties.get(vuln['severity'], 5)
            score -= penalty
        
        return max(0, score)

    def _determine_risk_level(self, vulnerabilities: List[Dict[str, Any]]) -> str:
        """Détermine le niveau de risque global."""
        if any(v['severity'] == 'CRITICAL' for v in vulnerabilities):
            return 'CRITICAL'
        elif any(v['severity'] == 'HIGH' for v in vulnerabilities):
            return 'HIGH'
        elif any(v['severity'] == 'MEDIUM' for v in vulnerabilities):
            return 'MEDIUM'
        elif vulnerabilities:
            return 'LOW'
        else:
            return 'SAFE'

    def _generate_security_recommendations(self, vulnerabilities: List[Dict[str, Any]]) -> List[str]:
        """Génère des recommandations de sécurité générales."""
        recommendations = []
        
        # Recommandations basées sur les vulnérabilités trouvées
        vuln_types = set(v['type'] for v in vulnerabilities)
        
        if 'dangerous_function' in vuln_types:
            recommendations.append("🚨 Remplacer les fonctions dangereuses (eval, exec) par des alternatives sécurisées")
        
        if 'hardcoded_secret' in vuln_types:
            recommendations.append("🔐 Externaliser les secrets vers des variables d'environnement ou un gestionnaire de secrets")
        
        if 'sql_injection_risk' in vuln_types:
            recommendations.append("🛡️ Utiliser des requêtes paramétrées pour éviter les injections SQL")
        
        if 'shell_injection_risk' in vuln_types:
            recommendations.append("⚡ Éviter shell=True dans subprocess, utiliser des listes d'arguments")
        
        # Recommandations générales
        recommendations.extend([
            "🔍 Effectuer des revues de code régulières avec focus sécurité",
            "📋 Implémenter un processus de validation des entrées utilisateur",
            "🔄 Mettre à jour régulièrement les dépendances pour corriger les vulnérabilités",
            "📊 Intégrer des outils d'analyse de sécurité dans le pipeline CI/CD"
        ])
        
        return recommendations

    def _generate_secured_code_suggestions(self, code: str, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Génère des suggestions de code sécurisé."""
        suggestions = []
        
        for vuln in vulnerabilities:
            if vuln['type'] == 'dangerous_function' and vuln['function'] == 'eval':
                suggestions.append({
                    'type': 'code_replacement',
                    'original_issue': f"eval() à la ligne {vuln['line']}",
                    'secure_alternative': """
# Au lieu de: result = eval(user_input)
# Utiliser:
import ast
try:
    result = ast.literal_eval(user_input)  # Seulement pour littéraux Python
except (ValueError, SyntaxError):
    # Gérer l'erreur appropriée
    result = None
""",
                    'explanation': "ast.literal_eval() est sécurisé pour les littéraux Python (strings, numbers, tuples, lists, dicts, booleans, None)"
                })
            
            elif vuln['type'] == 'shell_injection_risk':
                suggestions.append({
                    'type': 'code_replacement',
                    'original_issue': f"shell=True à la ligne {vuln['line']}",
                    'secure_alternative': """
# Au lieu de: subprocess.run(f"command {user_input}", shell=True)
# Utiliser:
subprocess.run(["command", user_input], shell=False)
# Ou avec vérification:
import shlex
subprocess.run(shlex.split(safe_command), shell=False)
""",
                    'explanation': "Utiliser une liste d'arguments évite l'injection de commandes shell"
                })
            
            elif vuln['type'] == 'hardcoded_secret':
                suggestions.append({
                    'type': 'configuration_change',
                    'original_issue': f"Secret en dur à la ligne {vuln['line']}",
                    'secure_alternative': """
# Au lieu de: API_KEY = "your-secret-key-here"
# Utiliser:
import os
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
""",
                    'explanation': "Les secrets doivent être stockés dans des variables d'environnement"
                })
        
        return suggestions