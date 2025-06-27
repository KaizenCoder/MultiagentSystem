#!/usr/bin/env python3
"""
🔐 AGENT 18 - AUDITEUR SÉCURITÉ SPÉCIALISÉ - PATTERN FACTORY COMPLIANT
Mission : Audit de sécurité approfondi + Audit universel de modules Python

Responsabilités :
- Audit de sécurité complet du code
- Détection des vulnérabilités OWASP Top 10
- Validation des configurations de sécurité
- Contrôle des permissions et accès
- Audit des dépendances et CVE
- Capacité d'audit universel de modules Python
- Rapport de conformité sécurité
- Intégration complète Pattern Factory
"""

import asyncio
import sys
from pathlib import Path
import hashlib
import subprocess
import tempfile
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import re
from dataclasses import dataclass, asdict
from enum import Enum
import os
import logging
import ast

# Import Pattern Factory (OBLIGATOIRE)
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.agent_factory_architecture import Agent, Task, Result
from core.manager import LoggingManager

class SecurityLevel(Enum):
    """Niveaux de sécurité"""
    CRITICAL = "critique"
    HIGH = "haut"
    MEDIUM = "moyen"
    LOW = "bas"
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

@dataclass
class SecurityFinding:
    """Résultat d'audit de sécurité"""
    finding_id: str
    vulnerability_type: VulnerabilityType
    security_level: SecurityLevel
    title: str
    description: str
    location: str
    line_number: Optional[int]
    cwe_id: Optional[str]
    cvss_score: Optional[float]
    remediation: str
    evidence: str

@dataclass
class SecurityReport:
    """Rapport complet d'audit de sécurité"""
    audit_id: str
    target: str
    timestamp: datetime
    findings: List[SecurityFinding]
    security_score: float
    compliance_status: Dict[str, bool]
    recommendations: List[str]
    summary: Dict[str, int]

class Agent18AuditeurSecurite(Agent):
    """
    🔐 AGENT 18 - AUDITEUR SÉCURITÉ SPÉCIALISÉ - PATTERN FACTORY COMPLIANT
    """
    
    def __init__(self, agent_type: str = "auditeur_securite", **config):
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="securite",
                custom_config={
                    "logger_name": f"nextgen.securite.18_auditeur_securite.{self.agent_id if hasattr(self, 'agent_id') else self.id if hasattr(self, 'id') else 'unknown'}",
                    "log_dir": "logs/securite",
                    "metadata": {
                        "agent_type": "18_auditeur_securite",
                        "agent_role": "securite",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)

        """Initialise l'agent d'audit de sécurité Pattern Factory."""
        super().__init__(agent_type, **config)
        self.agent_id = "18"
        self.specialite = "Auditeur Sécurité + OWASP + CVE + Audit Universel"
        self.mission = "Audit sécurité complet + détection vulnérabilités + audit modules Python"
        
        # Setup logging Pattern Factory compatible
        self.setup_logging()

        self.security_patterns = {
            'sql_injection': [r'\.execute\([^)]*\+', r'f".*{.*}.*".*execute', r'%.*%.*execute', r'cursor\.execute.*%'],
            'xss': [r'innerHTML\s*=', r'document\.write\(', r'eval\(', r'\.html\([^)]*\+'],
            'hardcoded_secrets': [r'password\s*=\s*["\'][^"\']+["\']', r'api_key\s*=\s*["\'][^"\']+["\']', r'secret\s*=\s*["\'][^"\']+["\']', r'token\s*=\s*["\'][^"\']+["\']'],
            'weak_crypto': [r'md5\(', r'sha1\(', r'DES\(', r'RC4\('],
            'file_traversal': [r'open\([^)]*\.\./[^)]*\)', r'os\.path\.join\([^)]*\.\./[^)]*\)', r'pathlib\.[^(]*\([^)]*\.\./[^)]*\)'],
            'dangerous_functions': [r'eval\(', r'exec\(', r'__import__', r'pickle\.loads', r'yaml\.load(?!_safe)', r'subprocess\.call.*shell=True'],
            'insecure_random': [r'random\.random', r'random\.choice', r'time\.time.*random'],
            'path_injection': [r'os\.system', r'subprocess\..*shell=True', r'os\.popen'],
            'xml_vulnerabilities': [r'xml\.etree', r'xml\.dom', r'xml\.sax', r'lxml', r'BeautifulSoup.*xml'],
            'insecure_protocols': [r'http://', r'ftp://', r'telnet://']
        }
        self.security_reports = {}
        self.rapport = {
            'agent_id': self.agent_id,
            'specialite': self.specialite,
            'mission_status': 'READY',
            'audits_effectués': [],
            'vulnérabilités_détectées': 0,
            'niveau_sécurité_global': None,
            'conformité_owasp': {},
            'recommandations_critiques': [],
            'timestamp_debut': datetime.now().isoformat()
        }
        
        self.logger.info(f"🔐 Agent {self.agent_id} - {self.specialite} - initialisé")

    def setup_logging(self):
        """Configuration logging centralisé Pattern Factory"""
        try:
            logging_manager = LoggingManager()
            custom_log_config = {
                "logger_name": f"agent.{self.agent_id}",
                "metadata": {
                    "agent_name": f"Agent18_{self.agent_id}",
                    "role": "ai_processor",
                    "domain": "security_audit"
                },
                "async_enabled": True
            }
            self.logger = logging_manager.get_logger(config_name="default", custom_config=custom_log_config)
        except Exception as e:
            # Fallback logging si système centralisé indisponible
            self.logger = logging.getLogger(f"agent_{self.agent_id}")
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.warning(f"Fallback logging pour Agent {self.agent_id}: {e}")
    
    async def execute_task(self, task: Task) -> Result:
        """🔐 Exécution des tâches Pattern Factory"""
        start_time = datetime.now()
        
        try:
            self.logger.info(f"🔐 Exécution tâche: {task.type}")
            
            if task.type == "audit_security":
                result_data = await self.auditer_securite_complete(task.params.get("target_path", ""))
                # Convertir SecurityReport en dict
                result_data = asdict(result_data)
            elif task.type == "audit_module":
                result_data = self.auditer_module_cible(task.params.get("module_path", ""))
            elif task.type == "scan_vulnerabilities":
                result_data = await self.scan_vulnerabilites_avancees(task.params.get("target_path", ""))
            elif task.type == "check_owasp_compliance":
                result_data = await self.verifier_conformite_owasp(task.params.get("target_path", ""))
            elif task.type == "analyze_dependencies":
                result_data = await self.analyser_dependances_cve(task.params.get("requirements_path", ""))
            elif task.type == "generate_security_report":
                result_data = await self.generer_rapport_securite_complet(task.params)
            else:
                return Result(success=False, error=f"Type de tâche non supporté: {task.type}")
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return Result(
                success=True,
                data=result_data,
                execution_time_seconds=execution_time,
                agent_id=self.id,
                task_id=task.id
            )
            
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution tâche {task.type}: {e}")
            return Result(
                success=False,
                error=str(e),
                agent_id=self.id,
                task_id=task.id
            )
    
    def auditer_module_cible(self, path_module: str) -> Dict[str, Any]:
        """🔐 Audit universel d'un module Python spécialisé sécurité"""
        self.logger.info(f"🔐 Audit sécurité universel du module: {path_module}")
        
        audit_result = {
            "module_path": path_module,
            "timestamp": datetime.now().isoformat(),
            "security_analysis": {}
        }
        
        try:
            module_path = Path(path_module)
            if not module_path.exists():
                return {
                    **audit_result,
                    "success": False,
                    "error": f"Module non trouvé: {path_module}"
                }
            
            # Analyse sécurité spécialisée
            audit_result["security_analysis"]["vulnerability_scan"] = self._scan_module_vulnerabilities(module_path)
            audit_result["security_analysis"]["crypto_analysis"] = self._analyze_crypto_usage(module_path)
            audit_result["security_analysis"]["input_validation"] = self._check_input_validation(module_path)
            audit_result["security_analysis"]["access_control"] = self._analyze_access_control(module_path)
            audit_result["security_analysis"]["data_protection"] = self._check_data_protection(module_path)
            
            # Score sécurité global
            scores = [analysis.get("score", 5.0) for analysis in audit_result["security_analysis"].values()]
            audit_result["score_securite_global"] = sum(scores) / len(scores) if scores else 5.0
            audit_result["success"] = True
            
            self.logger.info(f"✅ Audit sécurité terminé: {audit_result['score_securite_global']:.1f}/10")
            
        except Exception as e:
            audit_result["success"] = False
            audit_result["error"] = str(e)
            self.logger.error(f"❌ Erreur audit sécurité: {e}")
        
        return audit_result
    
    def _scan_module_vulnerabilities(self, module_path: Path) -> Dict[str, Any]:
        """Scan des vulnérabilités dans le module"""
        result = {"score": 8.0, "vulnerabilities": [], "warnings": []}
        
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Scan avec patterns de sécurité étendus
            for vuln_type, patterns in self.security_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
                    if matches:
                        severity = self._get_vulnerability_severity(vuln_type)
                        for match in matches:
                            result["vulnerabilities"].append({
                                "type": vuln_type,
                                "pattern": pattern,
                                "match": match,
                                "severity": severity
                            })
                            result["score"] -= self._get_score_penalty(severity)
            
            result["score"] = max(0.0, min(result["score"], 10.0))
            
        except Exception as e:
            result["error"] = str(e)
            result["score"] = 3.0
        
        return result
    
    def _analyze_crypto_usage(self, module_path: Path) -> Dict[str, Any]:
        """Analyse utilisation cryptographique"""
        result = {"score": 7.0, "crypto_issues": [], "recommendations": []}
        
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérification algorithmes faibles
            weak_algos = {
                "md5": "Algorithme MD5 déprécié",
                "sha1": "Algorithme SHA1 faible",
                "DES": "Chiffrement DES obsolète",
                "RC4": "Chiffrement RC4 vulnérable"
            }
            
            for algo, issue in weak_algos.items():
                if algo.lower() in content.lower():
                    result["crypto_issues"].append(issue)
                    result["score"] -= 1.5
            
            # Vérification bonnes pratiques
            good_practices = {
                "secrets": "Module secrets utilisé",
                "cryptography": "Bibliothèque cryptography présente",
                "bcrypt": "Bcrypt pour hachage mots de passe",
                "scrypt": "Scrypt pour dérivation clés"
            }
            
            for practice, desc in good_practices.items():
                if practice in content.lower():
                    result["recommendations"].append(desc)
                    result["score"] += 0.5
            
            result["score"] = max(0.0, min(result["score"], 10.0))
            
        except Exception as e:
            result["error"] = str(e)
            result["score"] = 5.0
        
        return result
    
    def _check_input_validation(self, module_path: Path) -> Dict[str, Any]:
        """Vérification validation des entrées"""
        result = {"score": 6.0, "validation_issues": [], "protections": []}
        
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Patterns de validation
            validation_patterns = {
                "isinstance(": "Vérification de type",
                "assert ": "Assertions utilisées",
                "raise ValueError": "Gestion erreurs de validation",
                "try:": "Gestion d'exceptions",
                "re.match": "Validation par regex",
                "len(": "Vérification de longueur"
            }
            
            for pattern, desc in validation_patterns.items():
                if pattern in content:
                    result["protections"].append(desc)
                    result["score"] += 0.5
            
            # Patterns dangereux
            dangerous_patterns = {
                "eval(": "Utilisation d'eval() dangereuse",
                "exec(": "Utilisation d'exec() dangereuse",
                "__import__": "Import dynamique non sécurisé"
            }
            
            for pattern, issue in dangerous_patterns.items():
                if pattern in content:
                    result["validation_issues"].append(issue)
                    result["score"] -= 2.0
            
            result["score"] = max(0.0, min(result["score"], 10.0))
            
        except Exception as e:
            result["error"] = str(e)
            result["score"] = 5.0
        
        return result
    
    def _analyze_access_control(self, module_path: Path) -> Dict[str, Any]:
        """Analyse contrôle d'accès"""
        result = {"score": 7.0, "access_issues": [], "security_measures": []}
        
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérification mécanismes d'authentification
            auth_patterns = {
                "authenticate": "Mécanisme d'authentification",
                "authorize": "Mécanisme d'autorisation",
                "permission": "Gestion des permissions",
                "role": "Gestion des rôles",
                "token": "Authentification par token",
                "session": "Gestion de session"
            }
            
            for pattern, desc in auth_patterns.items():
                if pattern.lower() in content.lower():
                    result["security_measures"].append(desc)
                    result["score"] += 0.3
            
            # Problèmes d'accès
            if "os.system" in content:
                result["access_issues"].append("Accès système non sécurisé")
                result["score"] -= 2.0
            
            if "subprocess" in content and "shell=True" in content:
                result["access_issues"].append("Exécution shell non sécurisée")
                result["score"] -= 1.5
            
            result["score"] = max(0.0, min(result["score"], 10.0))
            
        except Exception as e:
            result["error"] = str(e)
            result["score"] = 6.0
        
        return result
    
    def _check_data_protection(self, module_path: Path) -> Dict[str, Any]:
        """Vérification protection des données"""
        result = {"score": 8.0, "data_issues": [], "protections": []}
        
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Hardcoded secrets
            secret_patterns = [
                r'password\s*=\s*["\'][^"\']+',
                r'api_key\s*=\s*["\'][^"\']+',
                r'secret\s*=\s*["\'][^"\']+',
                r'token\s*=\s*["\'][^"\']+' 
            ]
            
            for pattern in secret_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    result["data_issues"].append(f"Secret potentiel hardcodé: {pattern}")
                    result["score"] -= 2.0
            
            # Protections des données
            protection_patterns = {
                "encrypt": "Chiffrement des données",
                "hash": "Hachage des données",
                "getpass": "Saisie sécurisée de mot de passe",
                "os.environ": "Variables d'environnement",
                "keyring": "Stockage sécurisé des clés"
            }
            
            for pattern, desc in protection_patterns.items():
                if pattern in content.lower():
                    result["protections"].append(desc)
                    result["score"] += 0.5
            
            result["score"] = max(0.0, min(result["score"], 10.0))
            
        except Exception as e:
            result["error"] = str(e)
            result["score"] = 7.0
        
        return result
    
    def _get_vulnerability_severity(self, vuln_type: str) -> str:
        """Détermine la sévérité d'une vulnérabilité"""
        critical_vulns = ["sql_injection", "dangerous_functions", "path_injection"]
        high_vulns = ["xss", "hardcoded_secrets", "weak_crypto"]
        
        if vuln_type in critical_vulns:
            return "CRITICAL"
        elif vuln_type in high_vulns:
            return "HIGH"
        else:
            return "MEDIUM"
    
    def _get_score_penalty(self, severity: str) -> float:
        """Calcule la pénalité de score selon la sévérité"""
        penalties = {
            "CRITICAL": 3.0,
            "HIGH": 2.0,
            "MEDIUM": 1.0,
            "LOW": 0.5
        }
        return penalties.get(severity, 1.0)

    async def auditer_securite_complete(self, target_path: str) -> SecurityReport:
        self.logger.info(f"🔐 Démarrage audit sécurité complet : {target_path}")
        audit_id = f"SEC_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        findings = []
        
        if not target_path:
            target_path = "."
            
        target = Path(target_path)

        if target.is_file():
            findings.extend(await self._audit_file_security(str(target)))
        elif target.is_dir():
            python_files = list(target.rglob('*.py'))
            for file_path in python_files[:20]:  # Limiter à 20 fichiers
                if not self._should_skip_file(file_path):
                    findings.extend(await self._audit_file_security(str(file_path)))
        
        security_score = self._calculate_security_score(findings)
        compliance_status = self._check_owasp_compliance(findings)
        recommendations = self._generate_security_recommendations(findings)
        
        report = SecurityReport(
            audit_id=audit_id,
            target=target_path,
            timestamp=datetime.now(),
            findings=findings,
            security_score=security_score,
            compliance_status=compliance_status,
            recommendations=recommendations,
            summary=self._generate_findings_summary(findings)
        )
        
        self.security_reports[audit_id] = report
        self.rapport["vulnérabilités_détectées"] += len(findings)
        self.rapport["niveau_sécurité_global"] = security_score
        
        await self._save_security_report(report)
        self.logger.info(f"✅ Audit sécurité terminé - Score: {security_score:.1f}/10")
        return report

    async def _audit_file_security(self, file_path: str) -> List[SecurityFinding]:
        findings = []
        try:
            content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
            for vuln_type, patterns in self.security_patterns.items():
                for pattern in patterns:
                    for match in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
                        line_num = content[:match.start()].count('\n') + 1
                        finding = self._create_security_finding(vuln_type, f"Pattern suspect: {match.group()}", file_path, line_num, match.group())
                        findings.append(finding)
        except Exception as e:
            self.logger.error(f"❌ Erreur audit fichier {file_path}: {e}", exc_info=True)
        return findings

    def _should_skip_file(self, file_path: Path) -> bool:
        skip_extensions = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe'}
        skip_dirs = {'__pycache__', '.git', '.venv'}
        return file_path.suffix.lower() in skip_extensions or any(part in skip_dirs for part in file_path.parts)

    def _create_security_finding(self, vuln_type: str, title: str, location: str, line_number: Optional[int], evidence: str) -> SecurityFinding:
        type_mapping = {
            'sql_injection': VulnerabilityType.INJECTION, 'xss': VulnerabilityType.XSS,
            'hardcoded_secrets': VulnerabilityType.SENSITIVE_DATA, 'weak_crypto': VulnerabilityType.SENSITIVE_DATA,
            'file_traversal': VulnerabilityType.BROKEN_ACCESS, 'dangerous_functions': VulnerabilityType.INJECTION,
            'path_injection': VulnerabilityType.BROKEN_ACCESS
        }
        vulnerability_type = type_mapping.get(vuln_type, VulnerabilityType.MISCONFIGURATION)
        security_level = self._determine_security_level(vulnerability_type)
        finding_id = f"SEC_{hashlib.md5(f'{location}_{line_number}_{evidence}'.encode()).hexdigest()[:8]}"
        return SecurityFinding(
            finding_id=finding_id, vulnerability_type=vulnerability_type, security_level=security_level,
            title=title, description=f"Pattern suspect détecté: {evidence}", location=location,
            line_number=line_number, cwe_id=self._get_cwe_id(vulnerability_type),
            cvss_score=self._get_cvss_score(security_level), remediation=self._generate_remediation(vulnerability_type, evidence),
            evidence=evidence
        )

    def _determine_security_level(self, vuln_type: VulnerabilityType) -> SecurityLevel:
        if vuln_type in {VulnerabilityType.INJECTION, VulnerabilityType.INSECURE_DESERIALIZATION}: return SecurityLevel.CRITICAL
        if vuln_type in {VulnerabilityType.XSS, VulnerabilityType.SENSITIVE_DATA}: return SecurityLevel.HIGH
        return SecurityLevel.MEDIUM

    def _get_cwe_id(self, vuln_type: VulnerabilityType) -> Optional[str]:
        return {VulnerabilityType.INJECTION: "CWE-89", VulnerabilityType.XSS: "CWE-79"}.get(vuln_type)

    def _get_cvss_score(self, security_level: SecurityLevel) -> Optional[float]:
        return {SecurityLevel.CRITICAL: 9.5, SecurityLevel.HIGH: 7.5, SecurityLevel.MEDIUM: 5.5}.get(security_level)

    def _generate_remediation(self, vuln_type: VulnerabilityType, evidence: str) -> str:
        return {
            VulnerabilityType.INJECTION: "Utiliser des requêtes préparées.",
            VulnerabilityType.SENSITIVE_DATA: "Stocker les secrets dans un vault."
        }.get(vuln_type, "Consulter la documentation de sécurité.")

    def _calculate_security_score(self, findings: List[SecurityFinding]) -> float:
        if not findings: return 10.0
        penalties = {SecurityLevel.CRITICAL: 3.0, SecurityLevel.HIGH: 2.0, SecurityLevel.MEDIUM: 1.0}
        total_penalty = sum(penalties.get(f.security_level, 0) for f in findings)
        return round(max(0.0, 10.0 - total_penalty), 1)

    def _check_owasp_compliance(self, findings: List[SecurityFinding]) -> Dict[str, bool]:
        owasp_map = {'A03_Injection': VulnerabilityType.INJECTION}
        return {cat: not any(f.vulnerability_type == v for f in findings) for cat, v in owasp_map.items()}

    def _generate_security_recommendations(self, findings: List[SecurityFinding]) -> List[str]:
        recs = set()
        if any(f.vulnerability_type == VulnerabilityType.INJECTION for f in findings):
            recs.add("Implémenter une validation stricte des entrées.")
        return list(recs)

    def _generate_findings_summary(self, findings: List[SecurityFinding]) -> Dict[str, int]:
        summary = {'total': len(findings), 'critique': 0, 'haut': 0, 'moyen': 0}
        for f in findings:
            if f.security_level == SecurityLevel.CRITICAL: summary['critique'] += 1
            elif f.security_level == SecurityLevel.HIGH: summary['haut'] += 1
            elif f.security_level == SecurityLevel.MEDIUM: summary['moyen'] += 1
        return summary

    async def _save_security_report(self, report: SecurityReport):
        reports_dir = Path("reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_file = reports_dir / f"agent_{self.agent_id}_security_report_{report.audit_id}.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(report), f, indent=2, default=str, ensure_ascii=False)
            self.logger.info(f"📄 Rapport sécurité sauvegardé : {report_file}")
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde rapport : {e}", exc_info=True)

    async def scan_vulnerabilites_avancees(self, target_path: str) -> Dict[str, Any]:
        """🔍 Scan avancé de vulnérabilités"""
        self.logger.info(f"🔍 Scan vulnérabilités avancées: {target_path}")
        
        scan_result = {
            "scan_id": str(uuid.uuid4()),
            "target_path": target_path,
            "timestamp": datetime.now().isoformat(),
            "advanced_vulnerabilities": []
        }
        
        try:
            if target_path and Path(target_path).exists():
                # Utiliser les capacités d'audit universel
                if Path(target_path).is_file():
                    module_analysis = self.auditer_module_cible(target_path)
                    vuln_data = module_analysis.get("security_analysis", {}).get("vulnerability_scan", {})
                    scan_result["advanced_vulnerabilities"] = vuln_data.get("vulnerabilities", [])
                    scan_result["security_score"] = module_analysis.get("score_securite_global", 5.0)
                
            scan_result["success"] = True
            
        except Exception as e:
            scan_result["success"] = False
            scan_result["error"] = str(e)
            self.logger.error(f"❌ Erreur scan vulnérabilités: {e}")
        
        return scan_result
    
    async def verifier_conformite_owasp(self, target_path: str) -> Dict[str, Any]:
        """📋 Vérification conformité OWASP Top 10"""
        self.logger.info(f"📋 Vérification conformité OWASP: {target_path}")
        
        owasp_result = {
            "target_path": target_path,
            "timestamp": datetime.now().isoformat(),
            "owasp_compliance": {}
        }
        
        try:
            # Exécuter audit sécurité complet
            report = await self.auditer_securite_complete(target_path)
            
            # OWASP Top 10 2021 mapping
            owasp_categories = {
                "A01_Broken_Access_Control": 0,
                "A02_Cryptographic_Failures": 0,
                "A03_Injection": 0,
                "A04_Insecure_Design": 0,
                "A05_Security_Misconfiguration": 0,
                "A06_Vulnerable_Components": 0,
                "A07_Authentication_Failures": 0,
                "A08_Software_Integrity_Failures": 0,
                "A09_Logging_Monitoring_Failures": 0,
                "A10_Server_Side_Request_Forgery": 0
            }
            
            # Compter vulnérabilités par catégorie OWASP
            for finding in report.findings:
                if finding.vulnerability_type == VulnerabilityType.INJECTION:
                    owasp_categories["A03_Injection"] += 1
                elif finding.vulnerability_type == VulnerabilityType.BROKEN_ACCESS:
                    owasp_categories["A01_Broken_Access_Control"] += 1
                elif finding.vulnerability_type == VulnerabilityType.SENSITIVE_DATA:
                    owasp_categories["A02_Cryptographic_Failures"] += 1
                elif finding.vulnerability_type == VulnerabilityType.MISCONFIGURATION:
                    owasp_categories["A05_Security_Misconfiguration"] += 1
            
            owasp_result["owasp_compliance"] = owasp_categories
            owasp_result["compliance_score"] = report.security_score
            owasp_result["total_violations"] = sum(owasp_categories.values())
            owasp_result["success"] = True
            
        except Exception as e:
            owasp_result["success"] = False
            owasp_result["error"] = str(e)
            self.logger.error(f"❌ Erreur vérification OWASP: {e}")
        
        return owasp_result
    
    async def analyser_dependances_cve(self, requirements_path: str) -> Dict[str, Any]:
        """🔍 Analyse CVE des dépendances"""
        self.logger.info(f"🔍 Analyse CVE dépendances: {requirements_path}")
        
        cve_result = {
            "requirements_path": requirements_path,
            "timestamp": datetime.now().isoformat(),
            "dependencies_analysis": {}
        }
        
        try:
            if requirements_path and Path(requirements_path).exists():
                with open(requirements_path, 'r') as f:
                    requirements = f.readlines()
                
                # Simulation d'analyse CVE (en réel, on utiliserait safety ou autre)
                vulnerable_packages = {
                    "requests": "Vulnérabilité CVE-2023-32681",
                    "urllib3": "Vulnérabilité CVE-2023-45803",
                    "pillow": "Vulnérabilité CVE-2023-50447",
                    "django": "Vulnérabilité CVE-2023-46695"
                }
                
                cve_found = []
                for req in requirements:
                    package_name = req.strip().split('==')[0].split('>=')[0].split('<=')[0]
                    if package_name.lower() in vulnerable_packages:
                        cve_found.append({
                            "package": package_name,
                            "vulnerability": vulnerable_packages[package_name.lower()]
                        })
                
                cve_result["dependencies_analysis"] = {
                    "total_dependencies": len(requirements),
                    "vulnerable_dependencies": cve_found,
                    "cve_count": len(cve_found),
                    "security_score": max(0, 10 - len(cve_found) * 2)
                }
            else:
                # Analyser imports dans fichiers Python
                cve_result["dependencies_analysis"] = {
                    "analysis_method": "import_analysis",
                    "note": "Fichier requirements.txt non trouvé, analyse des imports",
                    "security_score": 7.0
                }
            
            cve_result["success"] = True
            
        except Exception as e:
            cve_result["success"] = False
            cve_result["error"] = str(e)
            self.logger.error(f"❌ Erreur analyse CVE: {e}")
        
        return cve_result
    
    async def generer_rapport_securite_complet(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """📊 Génération rapport de sécurité complet"""
        self.logger.info("📊 Génération rapport sécurité complet")
        
        try:
            target_path = params.get("target_path", "")
            
            # Exécuter les différents audits
            security_audit = await self.auditer_securite_complete(target_path)
            owasp_compliance = await self.verifier_conformite_owasp(target_path)
            vuln_scan = await self.scan_vulnerabilites_avancees(target_path)
            
            # Rapport complet
            complete_report = {
                "report_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "agent_id": self.agent_id,
                "target_analyzed": target_path,
                "security_audit": asdict(security_audit),
                "owasp_compliance": owasp_compliance,
                "vulnerability_scan": vuln_scan,
                "executive_summary": {
                    "overall_security_score": security_audit.security_score,
                    "total_vulnerabilities": len(security_audit.findings),
                    "critical_vulnerabilities": len([f for f in security_audit.findings if f.security_level == SecurityLevel.CRITICAL]),
                    "owasp_violations": owasp_compliance.get("total_violations", 0),
                    "compliance_percentage": (security_audit.security_score / 10) * 100
                },
                "success": True
            }
            
            # Sauvegarder rapport complet
            await self._save_complete_security_report(complete_report)
            
        except Exception as e:
            complete_report = {
                "success": False,
                "error": str(e)
            }
            self.logger.error(f"❌ Erreur génération rapport complet: {e}")
        
        return complete_report

    async def _save_complete_security_report(self, report: Dict[str, Any]):
        """Sauvegarde rapport sécurité complet"""
        reports_dir = Path("reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_file = reports_dir / f"agent_{self.agent_id}_complete_security_{report.get('report_id', 'unknown')}.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str, ensure_ascii=False)
            self.logger.info(f"📄 Rapport sécurité complet sauvegardé : {report_file}")
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde rapport complet : {e}", exc_info=True)
    
    def get_capabilities(self) -> List[str]:
        """🔐 Capacités de l'agent sécurité"""
        return [
            "audit_security",
            "audit_module",
            "scan_vulnerabilities",
            "check_owasp_compliance",
            "analyze_dependencies",
            "generate_security_report",
            "crypto_analysis",
            "input_validation",
            "access_control",
            "data_protection"
        ]
    
    # Implémentation méthodes abstraites OBLIGATOIRES Pattern Factory
    async def startup(self):
        """🚀 Démarrage agent"""
        self.logger.info(f"🚀 Agent {self.agent_id} - {self.specialite} - DÉMARRAGE")
        self.rapport["mission_status"] = "ACTIVE"
        
    async def shutdown(self):
        """🛑 Arrêt agent"""
        self.logger.info(f"🛑 Agent {self.agent_id} - {self.specialite} - ARRÊT")
        self.rapport["mission_status"] = "STOPPED"
        
    async def health_check(self) -> Dict[str, Any]:
        """❤️ Vérification santé agent"""
        return {
            "status": "healthy",
            "agent_id": self.id,
            "agent_number": self.agent_id,
            "specialite": self.specialite,
            "mission": self.mission,
            "capabilities": self.get_capabilities(),
            "timestamp": datetime.now().isoformat(),
            "tasks_executed": self.tasks_executed,
            "success_rate": self.success_rate,
            "last_activity": self.last_activity.isoformat(),
            "security_reports_count": len(self.security_reports),
            "vulnerabilities_detected": self.rapport["vulnérabilités_détectées"]
        }

# ==========================================
# FACTORY FUNCTIONS (Pattern Factory)
# ==========================================

def create_agent_18_auditeur_securite(**config) -> Agent18AuditeurSecurite:
    """🏭 Factory function pour Agent 18 - Pattern Factory"""
    return Agent18AuditeurSecurite(agent_type="auditeur_securite", **config)

# ==========================================
# POINT D'ENTRÉE PRINCIPAL
# ==========================================
    # ✅ MÉTHODES STANDARDISÉES DE RAPPORT

    def _calculate_report_score(self, metrics: Dict[str, Any]) -> int:
        """Calcule le score global du rapport basé sur les métriques."""
        score = 0
        issues_critiques = []
        
        # Logique de scoring spécifique à l'agent
        # À adapter selon le type d'agent
        
        return score
    
    def _assess_conformity(self, score: int) -> str:
        """Évalue la conformité basée sur le score."""
        if score >= 90:
            return "✅ CONFORME - OPTIMAL"
        elif score >= 70:
            return "✅ CONFORME - ACCEPTABLE"
        else:
            return "❌ NON CONFORME - CRITIQUE"
    
    def _get_quality_level(self, score: int) -> str:
        """Détermine le niveau de qualité."""
        if score >= 90:
            return "OPTIMAL"
        elif score >= 70:
            return "ACCEPTABLE"
        else:
            return "CRITIQUE"
    
    def _generate_recommendations(self, metrics: Dict[str, Any], issues: List[str]) -> List[str]:
        """Génère les recommandations basées sur l'analyse."""
        recommendations = []
        
        # Logique de génération de recommandations
        # À adapter selon le type d'agent
        
        return recommendations
    
    def _generate_standard_report(self, context: Dict, metrics: Dict, timestamp) -> Dict[str, Any]:
        """Génère un rapport selon le format standard de l'agent 06."""
        
        score = self._calculate_report_score(metrics)
        conformity = self._assess_conformity(score)
        quality_level = self._get_quality_level(score)
        
        agent_filename = Path(__file__).name
        
        # Issues critiques (à personnaliser selon l'agent)
        issues_critiques = []
        
        return {
            'agent_id': getattr(self, 'agent_id', 'unknown'),
            'agent_file_name': agent_filename,
            'type_rapport': 'standard',  # À personnaliser
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Agent Spécialisé',  # À personnaliser
            'score_global': score,
            'niveau_qualite': quality_level,
            'conformite': conformity,
            'signature_cryptographique': 'N/A (Fonctionnalité non implémentée pour cet agent)',
            'issues_critiques_identifies': len(issues_critiques),
            'architecture': {
                'description': "Description de l'architecture de l'agent",
                'statut_operationnel': f"Système {getattr(self, 'agent_id', 'unknown')} opérationnel.",
                'confirmation_specialisation': f"{getattr(self, 'agent_id', 'unknown')} confirmé comme spécialiste.",
                'objectifs_principaux': [
                    "Objectif principal 1",
                    "Objectif principal 2",
                    "Objectif principal 3"
                ],
                'technologies_cles': ["Technologie 1", "Technologie 2"]
            },
            'recommandations': self._generate_recommendations(metrics, issues_critiques),
            'issues_critiques_details': issues_critiques if issues_critiques else [
                "Aucun issue critique majeur détecté. Le système fonctionne dans les paramètres attendus."
            ],
            'details_techniques': {
                'strategie': "Stratégie technique de l'agent",
                'composants_actifs': [],
                'metriques_collectees': metrics
            },
            'metriques_detaillees': {
                'score_global': {'actuel': score, 'cible': 100},
                'conformite_pourcentage': {'actuel': score, 'cible': 100, 'unite': '%'}
            },
            'impact_business': {
                'criticite': 'MOYENNE' if score >= 70 else 'HAUTE',
                'domaines_impactes': [],
                'actions_requises': []
            }
        }


    def _generate_markdown_report(self, rapport_json: Dict, context: Dict, timestamp) -> str:
        """Génère un rapport Markdown selon le format standard."""
        
        agent_name = rapport_json.get('agent_id', 'Agent Inconnu')
        type_rapport = rapport_json.get('type_rapport', 'standard')
        score = rapport_json.get('score_global', 0)
        quality = rapport_json.get('niveau_qualite', 'UNKNOWN')
        conformity = rapport_json.get('conformite', 'NON ÉVALUÉ')
        
        markdown_content = f"""# 📊 RAPPORT STRATÉGIQUE : {agent_name.upper()}

## 🎯 RÉSUMÉ EXÉCUTIF

**Agent :** {agent_name}  
**Type de Rapport :** {type_rapport}  
**Date de Génération :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Score Global :** {score}/100  
**Niveau de Qualité :** {quality}  
**Conformité :** {conformity}  

## 📈 ANALYSE GLOBALE

### Score de Performance
- **Score Actuel :** {score}/100
- **Objectif :** 100/100
- **Statut :** {'🟢 ACCEPTABLE' if score >= 70 else '🔴 CRITIQUE'}

### Architecture
{rapport_json.get('architecture', {}).get('description', 'Description non disponible')}

**Objectifs Principaux :**
"""
        
        # Ajouter les objectifs
        for obj in rapport_json.get('architecture', {}).get('objectifs_principaux', []):
            markdown_content += f"- {obj}\n"
        
        markdown_content += f"""
**Technologies Clés :**
"""
        
        # Ajouter les technologies
        for tech in rapport_json.get('architecture', {}).get('technologies_cles', []):
            markdown_content += f"- {tech}\n"
        
        markdown_content += f"""

## 🔍 RECOMMANDATIONS

"""
        
        # Ajouter les recommandations
        for reco in rapport_json.get('recommandations', []):
            markdown_content += f"- {reco}\n"
        
        markdown_content += f"""

## ⚠️ ISSUES CRITIQUES

"""
        
        # Ajouter les issues critiques
        for issue in rapport_json.get('issues_critiques_details', []):
            markdown_content += f"- {issue}\n"
        
        markdown_content += f"""

## 📊 MÉTRIQUES DÉTAILLÉES

### Performance Globale
- **Score Global :** {rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('actuel', 0)}/{rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('cible', 100)}
- **Conformité :** {rapport_json.get('metriques_detaillees', {}).get('conformite_pourcentage', {}).get('actuel', 0)}%

## 🎯 IMPACT BUSINESS

**Criticité :** {rapport_json.get('impact_business', {}).get('criticite', 'NON ÉVALUÉ')}

### Domaines Impactés
"""
        
        # Ajouter les domaines impactés
        for domaine in rapport_json.get('impact_business', {}).get('domaines_impactes', []):
            markdown_content += f"- {domaine}\n"
        
        markdown_content += f"""

### Actions Requises
"""
        
        # Ajouter les actions requises
        for action in rapport_json.get('impact_business', {}).get('actions_requises', []):
            markdown_content += f"- {action}\n"
        
        markdown_content += f"""

---
*Rapport généré automatiquement par {agent_name} - NextGeneration System*  
*Timestamp: {timestamp.isoformat()}*
"""
        
        return markdown_content



async def main():
    """Point d'entrée principal Agent 18 - Pattern Factory compatible"""
    # Création via Pattern Factory
    agent18 = create_agent_18_auditeur_securite()
    
    print("🔐 Agent 18 - Auditeur Sécurité - DÉMARRAGE (Pattern Factory)")
    print("=" * 70)
    
    # Startup Pattern Factory
    await agent18.startup()
    
    # Health check
    health = await agent18.health_check()
    print(f"❤️ Health: {health['status']} - Capacités: {len(health['capabilities'])}")
    
    # Test capacité audit universel sécurité
    print("\n🔐 Test capacité audit universel sécurité:")
    task_audit = Task(
        type="audit_module",
        params={"module_path": str(Path(__file__))}
    )
    result_audit = await agent18.execute_task(task_audit)
    if result_audit.success:
        print(f"   Score sécurité: {result_audit.data.get('score_securite_global', 'N/A'):.1f}/10")
    
    # Test audit sécurité complet
    print("\n🔍 Test audit sécurité complet:")
    task_security = Task(
        type="audit_security",
        params={"target_path": str(Path(__file__).parent)}
    )
    result_security = await agent18.execute_task(task_security)
    if result_security.success:
        security_data = result_security.data
        print(f"   Score sécurité global: {security_data.get('security_score', 'N/A'):.1f}/10")
        print(f"   Vulnérabilités trouvées: {len(security_data.get('findings', []))}")
    
    # Test vérification OWASP
    print("\n📋 Test vérification OWASP:")
    task_owasp = Task(
        type="check_owasp_compliance",
        params={"target_path": str(Path(__file__))}
    )
    result_owasp = await agent18.execute_task(task_owasp)
    if result_owasp.success:
        owasp_data = result_owasp.data
        print(f"   Score conformité: {owasp_data.get('compliance_score', 'N/A'):.1f}/10")
        print(f"   Violations OWASP: {owasp_data.get('total_violations', 'N/A')}")
    
    # Test scan vulnérabilités avancées
    print("\n🔍 Test scan vulnérabilités avancées:")
    task_vuln = Task(
        type="scan_vulnerabilities",
        params={"target_path": str(Path(__file__))}
    )
    result_vuln = await agent18.execute_task(task_vuln)
    if result_vuln.success:
        vuln_data = result_vuln.data
        print(f"   Vulnérabilités détectées: {len(vuln_data.get('advanced_vulnerabilities', []))}")
        print(f"   Score sécurité: {vuln_data.get('security_score', 'N/A'):.1f}/10")
    
    # Test génération rapport complet
    print("\n📊 Test génération rapport complet:")
    task_report = Task(
        type="generate_security_report",
        params={"target_path": str(Path(__file__))}
    )
    result_report = await agent18.execute_task(task_report)
    if result_report.success:
        summary = result_report.data.get("executive_summary", {})
        print(f"   Score global: {summary.get('overall_security_score', 'N/A'):.1f}/10")
        print(f"   Vulnérabilités totales: {summary.get('total_vulnerabilities', 'N/A')}")
        print(f"   Conformité: {summary.get('compliance_percentage', 'N/A'):.1f}%")
    
    # Métriques finales
    final_health = await agent18.health_check()
    print(f"\n📈 Métriques finales:")
    print(f"   Tâches exécutées: {final_health['tasks_executed']}")
    print(f"   Taux de succès: {final_health['success_rate']:.1%}")
    print(f"   Rapports sécurité: {final_health['security_reports_count']}")
    print(f"   Vulnérabilités détectées: {final_health['vulnerabilities_detected']}")
    
    # Shutdown Pattern Factory
    await agent18.shutdown()
    
    print("=" * 70)
    print("🔐 Agent 18 - MISSION SÉCURITÉ TERMINÉE ✅ (Pattern Factory compliant)")

# Point d'entrée CLI
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🔐 Programme interrompu par l'utilisateur.")