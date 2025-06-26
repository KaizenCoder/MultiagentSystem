"""
🔒 ANALYSEUR DE SÉCURITÉ - Agent 09
====================================

🎯 Mission : Détecter les vulnérabilités de sécurité potentielles dans le code et les systèmes de fichiers.
⚡ Capacités : Analyse statique de code, audit de sécurité universel de fichiers/répertoires.
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 1.1.0 (Audit universel intégré)
"""

import ast
import re
import hashlib
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import uuid
from datetime import datetime
import json
from dataclasses import dataclass, asdict, field
from enum import Enum

from core.agent_factory_architecture import Agent, Task, Result
# Assumons que LoggingManager est accessible, sinon fallback sur logging standard
try:
    from core.manager import LoggingManager
except ImportError:
    LoggingManager = None

# --- Début: Éléments intégrés depuis Agent 18 ---
class SecurityLevel(Enum):
    """Niveaux de sécurité"""
    CRITICAL = "critique"
    HIGH = "haut"
    MEDIUM = "moyen"
    LOW = "bas"
    INFO = "information" # Ajouté pour couvrir tous les cas
    SECURE = "sécurisé"

class VulnerabilityType(Enum):
    """Types de vulnérabilités"""
    INJECTION = "injection"
    XSS = "xss"
    BROKEN_AUTH = "authentification_cassée"
    SENSITIVE_DATA = "données_sensibles"
    XXE = "xxe"
    BROKEN_ACCESS = "contrôle_accès_cassé"
    MISCONFIGURATION = "mauvaise_configuration"
    INSECURE_DESERIALIZATION = "désérialisation_non_sécurisée"
    VULNERABLE_COMPONENTS = "composants_vulnérables"
    INSUFFICIENT_LOGGING = "journalisation_insuffisante"
    HARDCODED_SECRET = "secret_en_dur"
    WEAK_CRYPTO = "cryptographie_faible"
    FILE_TRAVERSAL = "traversée_de_fichier"
    DANGEROUS_FUNCTION = "fonction_dangereuse"
    PATH_INJECTION = "injection_de_chemin"
    XML_VULNERABILITIES = "vulnérabilités_xml"
    INSECURE_PROTOCOLS = "protocoles_non_sécurisés"
    INSECURE_FILE_OPERATION = "operation_fichier_non_securisee"
    INSECURE_FILE_PERMISSION = "permission_fichier_non_securisee"
    BROAD_EXCEPTION = "exception_large"
    ASSERTION_ISSUE = "probleme_assertion"
    OTHER = "autre"


@dataclass
class SecurityFinding:
    """Résultat d'audit de sécurité"""
    finding_id: str
    vulnerability_type: VulnerabilityType
    security_level: SecurityLevel
    title: str
    description: str
    location: str
    line_number: Optional[int] = None
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None
    remediation: Optional[str] = ""
    evidence: Optional[str] = ""

@dataclass
class SecurityReport:
    """Rapport complet d'audit de sécurité"""
    audit_id: str
    target: str
    timestamp: datetime
    findings: List[SecurityFinding] = field(default_factory=list)
    security_score: float = 10.0  # Score de 0 (pire) à 10 (meilleur)
    compliance_status: Dict[str, bool] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=dict)
# --- Fin: Éléments intégrés depuis Agent 18 ---


class AgentMAINTENANCE09AnalyseurSecurite(Agent):
    """
    Agent chargé de la sécurité du code Python et des audits universels:
    - Détecte les vulnérabilités de sécurité communes dans les chaînes de code.
    - Identifie les pratiques non sécurisées.
    - Scanne les injections potentielles.
    - Vérifie l'usage sécurisé des fonctions dangereuses.
    - Analyse les patterns de gestion des mots de passe et secrets.
    - Effectue des audits de sécurité sur des fichiers et répertoires.
    """

    def __init__(self, **kwargs):
        super().__init__(agent_type="security_analyzer", **kwargs) # type mis à jour
        self.agent_id = "agent_MAINTENANCE_09_Analyseur_Securite"
        self.version = "1.1.0"
        self.description = "Analyse et sécurise le code Python et effectue des audits universels."
        self.status = "enabled"
        self._setup_logging() # Déplacé après l'initialisation de agent_id

        # Patterns pour l'analyse de code existante (security_scan)
        self.dangerous_functions = {
            'eval': {'severity': 'CRITICAL', 'reason': 'Exécution de code arbitraire', 'alternatives': 'ast.literal_eval() pour données sûres, ou validation stricte'},
            'exec': {'severity': 'CRITICAL', 'reason': 'Exécution de code arbitraire', 'alternatives': 'Restructurer le code pour éviter l\\\'exécution dynamique'},
            'compile': {'severity': 'HIGH', 'reason': 'Compilation de code potentiellement malveillant', 'alternatives': 'Valider strictement les entrées avant compilation'},
            'input': {'severity': 'MEDIUM', 'reason': 'Injection de code possible en Python 2', 'alternatives': 'raw_input() en Python 2, input() est sûr en Python 3'},
            '__import__': {'severity': 'HIGH', 'reason': 'Import dynamique non contrôlé', 'alternatives': 'importlib avec validation des noms de modules'}
        }
        self.dangerous_modules = {
            'os.system': {'severity': 'CRITICAL', 'reason': 'Injection de commandes shell', 'alternatives': 'subprocess.run() avec shell=False'},
            'subprocess.call': {'severity': 'HIGH', 'reason': 'Injection potentielle si shell=True', 'alternatives': 'subprocess.run() avec liste d\\\'arguments'},
            'subprocess.Popen': {'severity': 'MEDIUM', 'reason': 'Vérifier l\\\'usage de shell=True', 'alternatives': 'Utiliser shell=False et liste d\\\'arguments'},
            'pickle.loads': {'severity': 'HIGH', 'reason': 'Désérialisation non sécurisée', 'alternatives': 'json, ou pickle avec signature/validation'},
            'marshal.loads': {'severity': 'HIGH', 'reason': 'Désérialisation dangereuse', 'alternatives': 'json ou autres formats sécurisés'}
        }
        self.secret_patterns_original = [ # Renommé pour éviter conflit
            (re.compile(r'password\\s*=\\s*[\"\\\'][^\"\\\']+[\\\'\"\\\']', re.IGNORECASE), 'Mot de passe en dur'),
            (re.compile(r'api_key\\s*=\\s*[\"\\\'][^\"\\\']+[\\\'\"\\\']', re.IGNORECASE), 'Clé API en dur'),
            (re.compile(r'secret\\s*=\\s*[\"\\\'][^\"\\\']+[\\\'\"\\\']', re.IGNORECASE), 'Secret en dur'),
            (re.compile(r'token\\s*=\\s*[\"\\\'][a-zA-Z0-9]{20,}[\\\'\"\\\']', re.IGNORECASE), 'Token en dur'),
            (re.compile(r'[\"\\\'][A-Za-z0-9+/]{40,}={0,2}[\\\'\"\\\']'), 'Possible clé encodée en base64'),
            (re.compile(r'-----BEGIN [A-Z ]+-----'), 'Clé cryptographique'),
        ]
        self.sql_injection_patterns_original = [ # Renommé
            re.compile(r'execute\s*\(\s*["\'].*%s.*["\']', re.IGNORECASE),
            re.compile(r'query\s*\(\s*["\'].*\+.*["\']', re.IGNORECASE),
            re.compile(r'["\'].*\+.*["\'].*WHERE', re.IGNORECASE),
        ]

        # Patterns pour le nouvel audit universel (inspiré de l'Agent 18)
        self.universal_audit_patterns = {
            'sql_injection': {'patterns': [r'\.execute\([^)]*\+', r'f".*\{.*\}.*".*execute', r'%.*%.*execute', r'cursor\.execute.*%'], 'type': VulnerabilityType.INJECTION, 'level': SecurityLevel.CRITICAL},
            'xss': {'patterns': [r'innerHTML\s*=', r'document\.write\(', r'\.html\([^)]*\+'], 'type': VulnerabilityType.XSS, 'level': SecurityLevel.HIGH},
            'hardcoded_secrets': {'patterns': [r'password\s*=\s*["\'][^"\']+["\']', r'api_key\s*=\s*["\'][^"\']+["\']', r'secret\s*=\s*["\'][^"\']+["\']', r'token\s*=\s*["\'][^"\']+["\']'], 'type': VulnerabilityType.HARDCODED_SECRET, 'level': SecurityLevel.HIGH},
            'weak_crypto': {'patterns': [r'md5\(', r'sha1\(', r'DES\(', r'RC4\('], 'type': VulnerabilityType.WEAK_CRYPTO, 'level': SecurityLevel.HIGH},
            'file_traversal': {'patterns': [r'open\([^)]*\.\./[^)]*\)', r'os\.path\.join\([^)]*\.\./[^)]*\)', r'pathlib\.[^(]*\([^)]*\.\./[^)]*\)'], 'type': VulnerabilityType.FILE_TRAVERSAL, 'level': SecurityLevel.HIGH},
            'dangerous_functions_generic': {'patterns': [r'eval\(', r'exec\(', r'__import__', r'pickle\.loads', r'yaml\.load(?!_safe)', r'subprocess\.call.*shell=True'], 'type': VulnerabilityType.DANGEROUS_FUNCTION, 'level': SecurityLevel.CRITICAL},
            'insecure_random': {'patterns': [r'random\.random', r'random\.choice', r'time\.time.*random'], 'type': VulnerabilityType.WEAK_CRYPTO, 'level': SecurityLevel.MEDIUM},
            'path_injection': {'patterns': [r'os\.system', r'subprocess\..*shell=True', r'os\.popen'], 'type': VulnerabilityType.PATH_INJECTION, 'level': SecurityLevel.CRITICAL},
            'xml_vulnerabilities': {'patterns': [r'xml\.etree', r'xml\.dom', r'xml\.sax', r'lxml', r'BeautifulSoup.*xml'], 'type': VulnerabilityType.XML_VULNERABILITIES, 'level': SecurityLevel.MEDIUM},
            'insecure_protocols': {'patterns': [r'http://', r'ftp://', r'telnet://'], 'type': VulnerabilityType.INSECURE_PROTOCOLS, 'level': SecurityLevel.MEDIUM}
        }
        self.security_reports_db = {} # Pour stocker les rapports générés par l'audit universel

    def _setup_logging(self):
        if LoggingManager:
            try:
                logging_manager = LoggingManager()
                custom_log_config = {
                    "logger_name": f"agent.{self.agent_id.replace('_', '.').lower()}", # Convention de nommage
                    "metadata": {"agent_name": self.agent_id, "role": "security_analyzer", "domain": "security_audit"},
                    "async_enabled": True
                }
                self.logger = logging_manager.get_logger(config_name="default", custom_config=custom_log_config)
                self.logger.info(f"Logging centralisé configuré pour {self.agent_id}")
            except Exception as e:
                self.logger = logging.getLogger(self.__class__.__name__) # Fallback
                self.logger.warning(f"Fallback sur logging standard pour {self.agent_id}: {e}")
        else:
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.info(f"Logging standard configuré pour {self.agent_id} (LoggingManager non trouvé).")


    async def startup(self):
        await super().startup()
        self.logger.info(f"{self.agent_id} prêt. Chargement des règles de sécurité...")

    async def execute_task(self, task: Task) -> Result:
        self.logger.info(f"Exécution de la tâche: {task.type} avec ID: {task.id}")
        if task.type == "security_scan": # Logique existante pour l'analyse de code string
            code = task.params.get("code")
            file_path = task.params.get("file_path", "unknown_file")
            if not code:
                self.logger.error("Code non fourni pour security_scan.")
                return Result(success=False, error="Code non fourni.")

            self.logger.info(f"🔐 Analyse de sécurité (original) pour : {file_path}")
            try:
                vulnerabilities = []
                vulnerabilities.extend(self._analyze_ast_security(code))
                vulnerabilities.extend(self._analyze_text_patterns(code))
                vulnerabilities.extend(self._detect_hardcoded_secrets_original(code)) # Utilise la méthode originale
                vulnerabilities.extend(self._detect_sql_injections_original(code)) # Utilise la méthode originale
                vulnerabilities.extend(self._analyze_file_operations(code))
                
                security_score = self._calculate_security_score_original(vulnerabilities) # Utilise la méthode originale
                recommendations = self._generate_security_recommendations_original(vulnerabilities) # Utilise la méthode originale
                secured_suggestions = self._generate_secured_code_suggestions(code, vulnerabilities)
                risk_level = self._determine_risk_level_original(vulnerabilities) # Utilise la méthode originale

                report = {
                    "file_path": file_path, "security_score": security_score,
                    "vulnerabilities": vulnerabilities, "recommendations": recommendations,
                    "secured_suggestions": secured_suggestions, "risk_level": risk_level,
                    "total_issues": len(vulnerabilities)
                }
                self.logger.info(f"Analyse (original) terminée pour {file_path} - Score: {security_score}/100, Issues: {len(vulnerabilities)}")
                return Result(success=True, data={"security_report": report, "score": security_score, "vulnerabilities": vulnerabilities})
            except Exception as e:
                self.logger.error(f"Erreur lors de l'analyse de sécurité (original) de {file_path}: {e}", exc_info=True)
                return Result(success=False, error=str(e))

        elif task.type == "audit_universel_securite": # Nouvelle logique pour l'audit de fichiers/répertoires
            target_path = task.params.get("target_path")
            if not target_path:
                self.logger.error("Chemin cible non fourni pour audit_universel_securite.")
                return Result(success=False, error="Chemin cible non fourni pour audit_universel_securite.")
            
            self.logger.info(f"🛡️ Audit universel de sécurité pour : {target_path}")
            try:
                report_obj = await self.auditer_securite_complete(target_path)
                # Sauvegarde le rapport (optionnel ici, auditer_securite_complete le fait déjà)
                # await self._save_security_report(report_obj) 
                self.logger.info(f"Audit universel terminé pour {target_path} - Score: {report_obj.security_score}/10")
                return Result(success=True, data=asdict(report_obj))
            except Exception as e:
                self.logger.error(f"Erreur lors de l'audit universel de {target_path}: {e}", exc_info=True)
                return Result(success=False, error=str(e))
        else:
            self.logger.warning(f"Tâche non supportée: {task.type}")
            return Result(success=False, error=f"Tâche non supportée: {task.type}")

    # --- Méthodes de l'analyse de code originale (security_scan) ---
    def _analyze_ast_security(self, code: str) -> List[Dict[str, Any]]:
        vulnerabilities = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    func_name = None
                    if isinstance(node.func, ast.Name): func_name = node.func.id
                    elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                        func_name = f"{node.func.value.id}.{node.func.attr}"
                    
                    if func_name in self.dangerous_functions:
                        info = self.dangerous_functions[func_name]
                        vulnerabilities.append({'type': 'dangerous_function', 'function': func_name, 'line': getattr(node, 'lineno', 0), **info})
                    elif func_name in self.dangerous_modules:
                        info = self.dangerous_modules[func_name]
                        vulnerabilities.append({'type': 'dangerous_module_call', 'function': func_name, 'line': getattr(node, 'lineno', 0), **info})
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    self._check_dangerous_imports(node, vulnerabilities)
        except SyntaxError as e:
            self.logger.warning(f"Erreur de syntaxe lors de l'analyse AST: {e}")
            vulnerabilities.append({'type': 'syntax_error', 'line': e.lineno, 'description': str(e), 'severity': 'INFO'})
        return vulnerabilities

    def _check_dangerous_imports(self, node: ast.AST, vulnerabilities: List[Dict[str, Any]]):
        dangerous_imports_list = ['pickle', 'marshal', 'subprocess', 'os']
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in dangerous_imports_list:
                    vulnerabilities.append({'type': 'dangerous_import', 'module': alias.name, 'line': getattr(node, 'lineno', 0), 'severity': 'LOW', 'description': f"Import du module '{alias.name}'", 'reason': 'Module nécessitant prudence', 'recommendation': 'Vérifier usage sécurisé'})
        elif isinstance(node, ast.ImportFrom):
            if node.module in dangerous_imports_list:
                vulnerabilities.append({'type': 'dangerous_from_import', 'module': node.module, 'line': getattr(node, 'lineno', 0), 'severity': 'LOW', 'description': f"Import depuis '{node.module}'", 'reason': 'Module nécessitant prudence', 'recommendation': 'Vérifier usage sécurisé'})

    def _analyze_text_patterns(self, code: str) -> List[Dict[str, Any]]:
        vulnerabilities = []
        lines = code.split('\\n')
        for i, line in enumerate(lines, 1):
            if 'except Exception' in line:
                vulnerabilities.append({'type': 'broad_exception_clause', 'line': i, 'severity': 'LOW', 'description': "Clause 'except Exception' trop large", 'recommendation': 'Capturer exceptions spécifiques'})
            if 'assert ' in line: # Simplifié, pourrait être plus précis
                vulnerabilities.append({'type': 'assertion_usage', 'line': i, 'severity': 'MEDIUM', 'description': "Usage de 'assert'", 'reason': 'Peut être désactivé', 'recommendation': 'Utiliser if/raise pour validation sécurité'})
        return vulnerabilities

    def _detect_hardcoded_secrets_original(self, code: str) -> List[Dict[str, Any]]:
        vulnerabilities = []
        lines = code.split('\\n')
        for i, line in enumerate(lines, 1):
            for pattern, name in self.secret_patterns_original:
                match = pattern.search(line)
                if match and self._is_likely_real_secret(match.group(0)):
                    vulnerabilities.append({'type': 'hardcoded_secret', 'name': name, 'line': i, 'severity': 'HIGH', 'description': f"Secret potentiel: '{name}'", 'recommendation': 'Externaliser les secrets'})
        return vulnerabilities

    def _is_likely_real_secret(self, text: str) -> bool:
        if '#' in text or '"""' in text or "'''" in text: return False
        if '=""' in text or "=''" in text or '="<placeholder>"' in text or 'example' in text.lower(): return False
        return True

    def _detect_sql_injections_original(self, code: str) -> List[Dict[str, Any]]:
        vulnerabilities = []
        lines = code.split('\\n')
        for i, line in enumerate(lines, 1):
            for pattern in self.sql_injection_patterns_original:
                if pattern.search(line):
                    vulnerabilities.append({'type': 'sql_injection_risk', 'line': i, 'severity': 'HIGH', 'description': 'Risque injection SQL', 'recommendation': 'Utiliser requêtes paramétrées'})
                    break
        return vulnerabilities

    def _analyze_file_operations(self, code: str) -> List[Dict[str, Any]]:
        vulnerabilities = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'open':
                    if any(isinstance(arg, ast.Constant) and isinstance(arg.value, str) and ('w' in arg.value or 'a' in arg.value) for arg in node.args): # Python 3.8+ ast.Constant
                         vulnerabilities.append({'type': 'insecure_file_operation', 'line': node.lineno, 'severity': 'LOW', 'description': "Opération d'écriture fichier", 'recommendation': 'Assurer permissions/contenu sécurisés'})
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'chmod':
                    if len(node.args) > 1 and isinstance(node.args[1], (ast.Num, ast.Constant)): # ast.Num for older Python
                        mode_val = node.args[1].n if isinstance(node.args[1], ast.Num) else node.args[1].value
                        if isinstance(mode_val, int) and (mode_val & 0o002 or mode_val & 0o020):
                            vulnerabilities.append({'type': 'insecure_file_permission', 'line': node.lineno, 'severity': 'MEDIUM', 'description': f"Permissions fichier non sécurisées (mode {oct(mode_val)})", 'recommendation': 'Utiliser permissions restrictives'})
        except SyntaxError: pass
        return vulnerabilities

    def _calculate_security_score_original(self, vulnerabilities: List[Dict[str, Any]]) -> int:
        score = 100
        severity_weights = {'CRITICAL': 25, 'HIGH': 15, 'MEDIUM': 5, 'LOW': 1, 'INFO': 0}
        for vuln in vulnerabilities: score -= severity_weights.get(vuln.get('severity', 'LOW'), 1)
        return max(0, score)

    def _determine_risk_level_original(self, vulnerabilities: List[Dict[str, Any]]) -> str:
        severities = {v.get('severity', 'LOW') for v in vulnerabilities}
        if 'CRITICAL' in severities: return 'CRITICAL'
        if 'HIGH' in severities: return 'HIGH'
        if 'MEDIUM' in severities: return 'MODERATE'
        if 'LOW' in severities: return 'LOW'
        return 'NONE'

    def _generate_security_recommendations_original(self, vulnerabilities: List[Dict[str, Any]]) -> List[str]:
        # Version simplifiée pour conserver la logique originale
        recs = {v.get('recommendation') for v in vulnerabilities if v.get('recommendation')}
        if not recs and vulnerabilities: recs.add("Procéder à une revue de sécurité manuelle.")
        return sorted(list(recs))

    def _generate_secured_code_suggestions(self, code: str, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        # Conserver la logique originale pour les suggestions
        suggestions = []
        lines = code.split('\\n')
        for vuln in vulnerabilities:
            line_num = vuln.get('line', 0)
            if not (0 < line_num <= len(lines)): continue
            original_line = lines[line_num - 1]
            suggestion_text = "Suggestion non disponible"
            if vuln['type'] == 'dangerous_function' and vuln['function'] == 'eval':
                suggestion_text = original_line.replace('eval(', 'ast.literal_eval(') + "  # RECO: Utiliser ast.literal_eval"
            # Ajouter d'autres suggestions si nécessaire pour la logique originale
            if suggestion_text != "Suggestion non disponible":
                suggestions.append({'line': line_num, 'original': original_line.strip(), 'suggestion': suggestion_text})
        return suggestions

    def export_security_report_md(self, report: dict, output_path: str):
        # Conserver la méthode d'exportation originale
        md = [f"# Rapport de Sécurité (Original) - {report.get('file_path', '')}", f"**Score :** {report.get('security_score', 0)}/100", f"**Risque :** {report.get('risk_level', '')}", f"**Problèmes :** {report.get('total_issues', 0)}", "", "## Vulnérabilités"]
        for vuln in report.get('vulnerabilities', []): md.append(f"- L{vuln.get('line', '?')} [{vuln.get('severity', '')}] {vuln.get('description', '')}")
        md.append("\\n## Recommandations")
        for rec in report.get('recommendations', []): md.append(f"- {rec}")
        with open(output_path, "w", encoding="utf-8") as f: f.write("\\n".join(md))
        self.logger.info(f"Rapport Markdown (original) exporté vers {output_path}")

    # --- Nouvelles méthodes pour l'audit universel (inspirées de l'Agent 18) ---
    async def auditer_securite_complete(self, target_path_str: str) -> SecurityReport:
        self.logger.info(f"🛡️ Démarrage audit sécurité universel pour : {target_path_str}")
        audit_id = f"SEC_UNI_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
        target_path = Path(target_path_str)
        all_findings: List[SecurityFinding] = []

        if not target_path.exists():
            self.logger.error(f"Chemin cible non trouvé: {target_path_str}")
            # Retourner un rapport vide avec une note d'erreur
            return SecurityReport(
                audit_id=audit_id, target=target_path_str, timestamp=datetime.now(),
                security_score=0.0,
                summary={"error": 1, "message": f"Target path not found: {target_path_str}"}
            )

        files_to_audit: List[Path] = []
        if target_path.is_file():
            if not self._should_skip_file(target_path):
                files_to_audit.append(target_path)
        elif target_path.is_dir():
            for item in target_path.rglob('*'): # rglob pour la récursivité
                if item.is_file() and not self._should_skip_file(item):
                    files_to_audit.append(item)
        
        self.logger.info(f"Nombre de fichiers à auditer: {len(files_to_audit)}")

        for file_p in files_to_audit:
            # Limiter le nombre de fichiers pour éviter les dépassements de temps/mémoire lors de tests importants.
            if len(all_findings) > 500 and len(files_to_audit) > 100 : # Limite arbitraire
                 self.logger.warning("Limite de découvertes atteinte, arrêt de l'audit des fichiers restants.")
                 break
            findings_for_file = await self._audit_file_security(str(file_p))
            all_findings.extend(findings_for_file)

        score = self._calculate_security_score_universal(all_findings)
        recommendations = self._generate_security_recommendations_universal(all_findings)
        summary = self._generate_findings_summary_universal(all_findings)
        
        report = SecurityReport(
            audit_id=audit_id, target=target_path_str, timestamp=datetime.now(),
            findings=all_findings, security_score=score,
            # compliance_status: self._check_owasp_compliance_universal(all_findings), # Peut être ajouté
            recommendations=recommendations, summary=summary
        )
        self.security_reports_db[audit_id] = asdict(report) # Stocke le rapport
        await self._save_security_report_universal(report) # Sauvegarde le rapport
        self.logger.info(f"✅ Audit universel terminé pour {target_path_str} - Score: {score:.1f}/10. {len(all_findings)} découvertes.")
        return report

    async def _audit_file_security(self, file_path_str: str) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []
        file_path = Path(file_path_str)
        self.logger.debug(f"Audit du fichier: {file_path_str}")
        try:
            # Lire le contenu avec gestion d'encodage et erreurs
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except Exception as e:
                self.logger.warning(f"Impossible de lire le fichier {file_path_str} (encodage?): {e}")
                findings.append(self._create_security_finding_universal(
                    VulnerabilityType.OTHER, SecurityLevel.INFO, f"Erreur de lecture fichier: {e}", file_path_str, None, str(e)
                ))
                return findings


            # Analyse AST pour certaines vulnérabilités (si c'est un fichier Python)
            if file_path.suffix.lower() == '.py':
                try:
                    tree = ast.parse(content, filename=file_path_str)
                    for node in ast.walk(tree):
                        # Exemple: Détection d'utilisation de 'eval' via AST
                        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'eval':
                            findings.append(self._create_security_finding_universal(
                                VulnerabilityType.DANGEROUS_FUNCTION, SecurityLevel.CRITICAL, "Utilisation de eval()",
                                file_path_str, node.lineno, "eval(...)"))
                        # Ajouter d'autres analyses AST spécifiques ici si nécessaire
                except SyntaxError as se:
                    findings.append(self._create_security_finding_universal(
                        VulnerabilityType.OTHER, SecurityLevel.INFO, "Erreur de syntaxe Python",
                        file_path_str, se.lineno, f"SyntaxError: {se.msg}"))
                except Exception as ast_e: # Erreur générique AST
                    self.logger.warning(f"Erreur d'analyse AST pour {file_path_str}: {ast_e}")


            # Analyse par patterns Regex
            for vuln_category, details in self.universal_audit_patterns.items():
                category_type = details['type']
                category_level = details['level']
                for pattern_str in details['patterns']:
                    try:
                        compiled_pattern = re.compile(pattern_str) # Compiler ici pour flexibilité
                        for match in compiled_pattern.finditer(content):
                            line_num = content[:match.start()].count('\\n') + 1
                            evidence_text = match.group(0)
                            # Limiter la taille de 'evidence_text'
                            if len(evidence_text) > 200:
                                evidence_text = evidence_text[:197] + "..."

                            findings.append(self._create_security_finding_universal(
                                category_type, category_level, f"Pattern suspect ({vuln_category})",
                                file_path_str, line_num, evidence_text
                            ))
                    except re.error as re_err:
                        self.logger.error(f"Erreur de regex pour le pattern '{pattern_str}': {re_err}")
                        # Optionnel: ajouter un finding pour l'erreur de pattern
                        findings.append(self._create_security_finding_universal(
                            VulnerabilityType.OTHER, SecurityLevel.INFO, f"Erreur de configuration pattern regex: {pattern_str}",
                            "Configuration Agent", None, str(re_err)
                        ))


        except Exception as e:
            self.logger.error(f"❌ Erreur audit fichier {file_path_str}: {e}", exc_info=True)
            findings.append(self._create_security_finding_universal(
                VulnerabilityType.OTHER, SecurityLevel.CRITICAL, f"Erreur majeure audit fichier: {e}", file_path_str, None, str(e)
            ))
        return findings

    def _should_skip_file(self, file_path: Path) -> bool:
        skip_extensions = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe', '.log', '.tmp', '.bak', '.swp', '.zip', '.gz', '.tar', '.rar', '.7z', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.o', '.obj', '.class', '.jar'}
        skip_dirs_parts = {'__pycache__', '.git', '.venv', 'node_modules', '.vscode', '.idea', 'build', 'dist', 'env', 'venv'}
        
        if file_path.suffix.lower() in skip_extensions:
            return True
        if any(part.lower() in skip_dirs_parts for part in file_path.parts):
            return True
        # Ignorer les fichiers très volumineux pour éviter les problèmes de performance/mémoire
        try:
            if file_path.stat().st_size > 5 * 1024 * 1024:  # 5 MB limit
                self.logger.info(f"Fichier ignoré car trop volumineux: {file_path} ({file_path.stat().st_size} octets)")
                return True
        except OSError: # Fichier peut-être disparu entre-temps
             return True
        return False

    def _create_security_finding_universal(self, vuln_type: VulnerabilityType, sec_level: SecurityLevel, title: str, location: str, line_number: Optional[int], evidence: str) -> SecurityFinding:
        finding_id = f"SF_{str(uuid.uuid4())[:12]}"
        # Mappings CWE et CVSS (exemples, à enrichir)
        cwe_map = { VulnerabilityType.INJECTION: "CWE-89", VulnerabilityType.XSS: "CWE-79", VulnerabilityType.HARDCODED_SECRET: "CWE-798"}
        cvss_map = { SecurityLevel.CRITICAL: 9.8, SecurityLevel.HIGH: 7.5, SecurityLevel.MEDIUM: 5.3, SecurityLevel.LOW: 3.8 }
        
        # Remédiations génériques (à enrichir)
        remediation_map = {
            VulnerabilityType.INJECTION: "Utiliser des requêtes paramétrées et valider toutes les entrées.",
            VulnerabilityType.HARDCODED_SECRET: "Externaliser les secrets via des variables d'environnement ou un gestionnaire de secrets.",
            VulnerabilityType.DANGEROUS_FUNCTION: "Éviter les fonctions dangereuses. Utiliser des alternatives sûres (ex: ast.literal_eval pour eval).",
        }

        return SecurityFinding(
            finding_id=finding_id, vulnerability_type=vuln_type, security_level=sec_level,
            title=title, description=f"{title} : {evidence}", location=location,
            line_number=line_number, cwe_id=cwe_map.get(vuln_type),
            cvss_score=cvss_map.get(sec_level), remediation=remediation_map.get(vuln_type, "Consulter la documentation et appliquer les correctifs de sécurité spécifiques."),
            evidence=evidence
        )

    def _calculate_security_score_universal(self, findings: List[SecurityFinding]) -> float:
        if not findings: return 10.0 # Score parfait si aucune découverte
        
        # Pénalités plus granulaires
        severity_penalties = {
            SecurityLevel.CRITICAL: 3.0,
            SecurityLevel.HIGH: 1.5,
            SecurityLevel.MEDIUM: 0.5,
            SecurityLevel.LOW: 0.1,
            SecurityLevel.INFO: 0.0
        }
        
        total_penalty = 0.0
        for f in findings:
            total_penalty += severity_penalties.get(f.security_level, 0.1) # Défaut petite pénalité
            
        # Normaliser le score entre 0 et 10
        # Plus la pénalité est élevée, plus le score baisse.
        # Un grand nombre de petites pénalités peut aussi réduire significativement le score.
        # Modèle simple: Score = 10 - log(total_penalty + 1) pour atténuer l'effet de nombreuses petites erreurs
        # Ou plus simple:
        score = 10.0 - total_penalty
        return round(max(0.0, min(10.0, score)), 1)


    def _generate_security_recommendations_universal(self, findings: List[SecurityFinding]) -> List[str]:
        if not findings: return ["Aucune recommandation spécifique, le système semble sécurisé."]
        
        unique_remediations = set()
        for f in findings:
            if f.remediation:
                unique_remediations.add(f.remediation)
        
        if not unique_remediations:
            return ["Examiner manuellement les découvertes pour déterminer les actions correctives."]
            
        # Prioriser par sévérité si possible (nécessiterait de trier les `findings` ou les `remediations` par `security_level`)
        return sorted(list(unique_remediations))

    def _generate_findings_summary_universal(self, findings: List[SecurityFinding]) -> Dict[str, int]:
        summary = {level.name.lower(): 0 for level in SecurityLevel} # Initialiser tous les niveaux
        summary['total'] = len(findings)
        
        for f in findings:
            summary[f.security_level.name.lower()] += 1
            
        return summary

    async def _save_security_report_universal(self, report: SecurityReport):
        reports_dir = Path(self.workspace_path if self.workspace_path else Path.cwd()) / "reports" / "security_audits"
        try:
            reports_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.logger.error(f"Impossible de créer le répertoire des rapports {reports_dir}: {e}")
            # Ne pas planter si le répertoire ne peut être créé, logger l'erreur.
            # Le rapport ne sera juste pas sauvegardé.
            return

        report_file = reports_dir / f"audit_report_{self.agent_id}_{report.audit_id}.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(report), f, indent=2, default=str) # default=str pour datetime
            self.logger.info(f"📄 Rapport d'audit universel sauvegardé : {report_file}")
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde rapport d'audit universel {report_file}: {e}", exc_info=True)


    async def shutdown(self):
        self.logger.info(f"{self.agent_id} éteint.")
        await super().shutdown()

    def get_capabilities(self) -> List[str]:
        return ["security_scan", "audit_universel_securite"]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "version": self.version, "agent_id": self.agent_id, "capabilities": self.get_capabilities()}


def create_agent_MAINTENANCE_09_analyseur_securite(**kwargs) -> AgentMAINTENANCE09AnalyseurSecurite:
    """Factory function pour créer une instance de l'analyseur de sécurité."""
    return AgentMAINTENANCE09AnalyseurSecurite(**kwargs)


async def main():
    # Création de l'agent
    agent = create_agent_MAINTENANCE_09_analyseur_securite()
    await agent.startup()
    agent.logger.info("Agent de test démarré.")

    # Test 1: Scan de sécurité sur une chaîne de code
    sample_code_string = "import os\npassword = 'secret123'\neval('print(1)')\nos.system('ls')"
    task1 = Task(id="test_scan_1", type="security_scan", params={"code": sample_code_string, "file_path": "test_code.py"})
    result1 = await agent.execute_task(task1)
    if result1.success:
        agent.logger.info(f"Résultat security_scan: Score {result1.data['security_report']['security_score']}, {result1.data['security_report']['total_issues']} issues.")
        # agent.export_security_report_md(result1.data['security_report'], "test_security_scan_report.md")
    else:
        agent.logger.error(f"Erreur security_scan: {result1.error}")

    # Créer un fichier de test pour l'audit universel
    test_dir = Path("temp_audit_dir_agent09")
    test_dir.mkdir(exist_ok=True)
    user_name = "TestUser' OR '1'='1"  # Définition de user_name pour le test
    test_file_path = test_dir / "test_vuln_file.py"
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write("# Fichier de test pour Agent 09\n")
        f.write('api_key = "THIS_IS_A_VERY_SECRET_API_KEY"\n')  # Secret en dur
        f.write("import pickle\n")  # Import dangereux
        f.write("def unsafe_load(data): return pickle.loads(data)\n")  # Utilisation de pickle.loads
        f.write('eval(\'print("eval test")\')\n')  # Utilisation de eval
        f.write(f'db.execute("SELECT * FROM users WHERE name = \'{user_name}\'")\n')  # SQL Injection

    # Test 2: Audit universel de sécurité sur un fichier
    task2 = Task(id="test_audit_file_1", type="audit_universel_securite", params={"target_path": str(test_file_path)})
    result2 = await agent.execute_task(task2)
    if result2.success:
        report_data = result2.data
        agent.logger.info(f"Résultat audit_universel_securite (fichier): Score {report_data['security_score']:.1f}/10, {len(report_data['findings'])} découvertes.")
    else:
        agent.logger.error(f"Erreur audit_universel_securite (fichier): {result2.error}")

    # Test 3: Audit universel de sécurité sur un répertoire
    task3 = Task(id="test_audit_dir_1", type="audit_universel_securite", params={"target_path": str(test_dir)})
    result3 = await agent.execute_task(task3)
    if result3.success:
        report_data_dir = result3.data
        agent.logger.info(f"Résultat audit_universel_securite (répertoire): Score {report_data_dir['security_score']:.1f}/10, {len(report_data_dir['findings'])} découvertes.")
    else:
        agent.logger.error(f"Erreur audit_universel_securite (répertoire): {result3.error}")

    # Nettoyage
    try:
        # Correction: Importer os pour remove et rmdir
        import os 
        os.remove(test_file_path)
        os.rmdir(test_dir)
        agent.logger.info("Fichiers et répertoire de test nettoyés.")
    except OSError as e:
        agent.logger.error(f"Erreur lors du nettoyage des fichiers de test: {e}")
        
    await agent.shutdown()

if __name__ == '__main__':
    import asyncio
    # Configuration du logging de base pour voir les messages de l'agent pendant le test
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    asyncio.run(main())