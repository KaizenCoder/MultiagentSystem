#!/usr/bin/env python3
"""

# 🔧 CONVERTI AUTOMATIQUEMENT SYNC → ASYNC
# Date: 2025-06-19 19h35 - Correction architecture Pattern Factory
# Raison: Harmonisation async/sync avec core/agent_factory_architecture.py

🔐 AGENT 18 - AUDITEUR SÉCURITÉ SPÉCIALISÉ
Mission : Audit de sécurité approfondi et validation des vulnérabilités

Responsabilités :
- Audit de sécurité complet du code
- Détection des vulnérabilités OWASP Top 10
- Validation des configurations de sécurité
- Contrôle des permissions et accès
- Audit des dépendances et CVE
- Rapport de conformité sécurité
"""

import asyncio
import logging
import hashlib
import subprocess
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import json
import re
from dataclasses import dataclass, asdict
from enum import Enum
import os
import sys

# Import code expert OBLIGATOIRE
sys.path.insert(0, str(Path(__file__).parent.parent / "code_expert"))

# Configuration projet
from agent_config import AgentFactoryConfig, config_manager

class SecurityLevel(Enum):
    """Niveaux de sécurité"""
    CRITICAL = "critique"     # Vulnérabilités critiques
    HIGH = "haut"            # Risque élevé
    MEDIUM = "moyen"         # Risque modéré
    LOW = "bas"              # Risque faible
    SECURE = "sécurisé"      # Aucune vulnérabilité détectée

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

class Agent18AuditeurSecurite:
    """
    🔐 Agent 18 - Auditeur Sécurité Spécialisé
    
    Responsabilités :
    - Audit de sécurité approfondi
    - Détection vulnérabilités OWASP
    - Validation configurations sécurité
    - Audit dépendances et CVE
    - Génération rapports conformité
    """
    
    def __init__(self, config: Optional[AgentFactoryConfig] = None):
        self.config = config
        self.agent_id = "18"
        self.specialite = "Audit Sécurité Spécialisé"
        self.mission = "Audit sécurité complet et détection vulnérabilités"
        
        # Patterns de sécurité à vérifier
        self.security_patterns = {
            'sql_injection': [
                r'\.execute\([^)]*\+',
                r'f".*{.*}.*".*execute',
                r'%.*%.*execute',
                r'cursor\.execute.*%',
            ],
            'xss': [
                r'innerHTML\s*=',
                r'document\.write\(',
                r'eval\(',
                r'\.html\([^)]*\+',
            ],
            'hardcoded_secrets': [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
                r'token\s*=\s*["\'][^"\']+["\']',
            ],
            'weak_crypto': [
                r'md5\(',
                r'sha1\(',
                r'DES\(',
                r'RC4\(',
            ],
            'file_traversal': [
                r'open\([^)]*\.\./[^)]*\)',
                r'os\.path\.join\([^)]*\.\./[^)]*\)',
                r'pathlib\.[^(]*\([^)]*\.\./[^)]*\)',
            ]
        }
        
        # Standards de sécurité
        self.security_standards = {
            'minimum_password_entropy': 60,
            'max_file_permissions': 0o644,
            'required_headers': ['X-Content-Type-Options', 'X-Frame-Options', 'X-XSS-Protection'],
            'forbidden_functions': ['eval', 'exec', 'compile'],
            'secure_protocols': ['https', 'tls', 'ssl']
        }
        
        # Résultats d'audits
        self.security_reports = {}
        self.current_findings = []
        
        # Logs
        self.logger = logging.getLogger(f"Agent{self.agent_id}")
        self.setup_logging()
        
        # Rapport de mission
        self.rapport = {
            'agent_id': self.agent_id,
            'mission_status': 'INITIALISÉ',
            'audits_effectués': [],
            'vulnérabilités_détectées': 0,
            'niveau_sécurité_global': None,
            'conformité_owasp': {},
            'recommandations_critiques': []
        }

    def setup_logging(self):
        """Configuration logging Agent 18"""
        log_dir = Path("nextgeneration/agent_factory_implementation/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        handler = logging.FileHandler(
            log_dir / f"agent_{self.agent_id}_securite_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - Agent18_Sécurité - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.logger.info(f"🔐 Agent {self.agent_id} - {self.specialite} INITIALISÉ")

    async def auditer_securite_complete(self, target_path: str) -> SecurityReport:
        """
        🔍 Audit de sécurité complet d'un composant
        
        Args:
            target_path: Chemin vers le fichier/dossier à auditer
            
        Returns:
            SecurityReport: Rapport complet d'audit de sécurité
        """
        self.logger.info(f"🔐 Démarrage audit sécurité complet : {target_path}")
        
        audit_id = f"SEC_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        findings = []
        
        if Path(target_path).is_file():
            findings.extend(await self._audit_file_security(target_path))
        elif Path(target_path).is_dir():
            findings.extend(await self._audit_directory_security(target_path))
        
        # Calcul score de sécurité
        security_score = await self._calculate_security_score(findings)
        
        # Vérification conformité OWASP
        compliance_status = await self._check_owasp_compliance(findings)
        
        # Génération recommandations
        recommendations = await self._generate_security_recommendations(findings)
        
        # Création du rapport
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
        
        # Sauvegarde
        self.security_reports[audit_id] = report
        await self._save_security_report(report)
        
        self.logger.info(f"✅ Audit sécurité terminé - Score: {security_score:.1f}/10")
        return report

    async def _audit_file_security(self, file_path: str) -> List[SecurityFinding]:
        """Audit de sécurité d'un fichier spécifique"""
        findings = []
        file_path_obj = Path(file_path)
        
        if not file_path_obj.exists():
            return findings
        
        try:
            content = file_path_obj.read_text(encoding='utf-8', errors='ignore')
            
            # Vérification patterns de vulnérabilités
            for vuln_type, patterns in self.security_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        finding = await self._create_security_finding(
                            vuln_type,
                            f"Vulnérabilité potentielle {vuln_type}",
                            f"Pattern suspect détecté : {match.group()}",
                            str(file_path_obj),
                            line_num,
                            match.group()
                        )
                        findings.append(finding)
            
            # Vérifications spécifiques Python
            if file_path.endswith('.py'):
                findings.extend(await self._audit_python_security(content, str(file_path_obj)))
            
            # Vérifications fichiers de configuration
            if file_path.endswith(('.json', '.yaml', '.yml', '.conf', '.ini')):
                findings.extend(await self._audit_config_security(content, str(file_path_obj)))
            
        except Exception as e:
            self.logger.error(f"❌ Erreur audit fichier {file_path}: {e}")
        
        return findings

    async def _audit_python_security(self, content: str, file_path: str) -> List[SecurityFinding]:
        """Audit spécifique sécurité Python"""
        findings = []
        
        # Vérification imports dangereux
        dangerous_imports = ['pickle', 'cPickle', 'subprocess', 'os', 'eval', 'exec']
        for imp in dangerous_imports:
            if re.search(rf'\bimport\s+{imp}\b', content):
                findings.append(await self._create_security_finding(
                    'vulnerable_components',
                    f"Import potentiellement dangereux : {imp}",
                    f"L'import {imp} peut présenter des risques de sécurité",
                    file_path,
                    None,
                    f"import {imp}"
                ))
        
        # Vérification désérialisation unsafe
        unsafe_deserial = ['pickle.loads', 'pickle.load', 'yaml.load']
        for method in unsafe_deserial:
            if method in content:
                findings.append(await self._create_security_finding(
                    'insecure_deserialization',
                    f"Désérialisation non sécurisée : {method}",
                    f"Utilisation de {method} sans validation peut permettre l'exécution de code arbitraire",
                    file_path,
                    None,
                    method
                ))
        
        return findings

    async def _audit_config_security(self, content: str, file_path: str) -> List[SecurityFinding]:
        """Audit sécurité fichiers de configuration"""
        findings = []
        
        # Recherche secrets hardcodés
        secret_patterns = [
            r'password\s*[:=]\s*["\'][^"\']{8,}["\']',
            r'api[_-]?key\s*[:=]\s*["\'][^"\']{20,}["\']',
            r'secret\s*[:=]\s*["\'][^"\']{16,}["\']',
            r'token\s*[:=]\s*["\'][^"\']{20,}["\']'
        ]
        
        for pattern in secret_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                findings.append(await self._create_security_finding(
                    'sensitive_data',
                    "Secret hardcodé détecté",
                    "Secrets ne doivent pas être stockés en dur dans le code",
                    file_path,
                    None,
                    match.group()
                ))
        
        return findings

    async def _audit_directory_security(self, dir_path: str) -> List[SecurityFinding]:
        """Audit sécurité d'un répertoire complet"""
        findings = []
        dir_path_obj = Path(dir_path)
        
        # Audit récursif des fichiers
        for file_path in dir_path_obj.rglob('*'):
            if file_path.is_file() and not self._should_skip_file(file_path):
                file_findings = await self._audit_file_security(str(file_path))
                findings.extend(file_findings)
        
        # Vérification permissions répertoire
        findings.extend(await self._check_directory_permissions(dir_path))
        
        return findings

    def _should_skip_file(self, file_path: Path) -> bool:
        """Détermine si un fichier doit être ignoré lors de l'audit"""
        skip_extensions = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe'}
        skip_dirs = {'__pycache__', '.git', 'node_modules', '.venv', 'venv'}
        
        if file_path.suffix.lower() in skip_extensions:
            return True
        
        if any(part in skip_dirs for part in file_path.parts):
            return True
        
        return False

    async def _check_directory_permissions(self, dir_path: str) -> List[SecurityFinding]:
        """Vérification des permissions de répertoire"""
        findings = []
        
        try:
            dir_stat = os.stat(dir_path)
            permissions = oct(dir_stat.st_mode)[-3:]
            
            # Vérification permissions trop permissives
            if int(permissions) > 755:
                findings.append(await self._create_security_finding(
                    'misconfiguration',
                    "Permissions de répertoire trop permissives",
                    f"Le répertoire {dir_path} a des permissions {permissions} trop ouvertes",
                    dir_path,
                    None,
                    f"permissions: {permissions}"
                ))
        except Exception as e:
            self.logger.warning(f"⚠️ Impossible de vérifier permissions {dir_path}: {e}")
        
        return findings

    async def _create_security_finding(
        self,
        vuln_type: str,
        title: str,
        description: str,
        location: str,
        line_number: Optional[int],
        evidence: str
    ) -> SecurityFinding:
        """Création d'un résultat d'audit de sécurité"""
        
        # Mapping vers VulnerabilityType
        type_mapping = {
            'sql_injection': VulnerabilityType.INJECTION,
            'xss': VulnerabilityType.XSS,
            'hardcoded_secrets': VulnerabilityType.SENSITIVE_DATA,
            'weak_crypto': VulnerabilityType.SENSITIVE_DATA,
            'file_traversal': VulnerabilityType.BROKEN_ACCESS,
            'vulnerable_components': VulnerabilityType.VULNERABLE_COMPONENTS,
            'insecure_deserialization': VulnerabilityType.INSECURE_DESERIALIZATION,
            'misconfiguration': VulnerabilityType.MISCONFIGURATION,
            'sensitive_data': VulnerabilityType.SENSITIVE_DATA
        }
        
        vulnerability_type = type_mapping.get(vuln_type, VulnerabilityType.MISCONFIGURATION)
        
        # Détermination niveau de sécurité basé sur le type
        security_level = self._determine_security_level(vulnerability_type)
        
        # Génération ID unique
        finding_id = f"SEC_{hashlib.md5(f'{location}_{line_number}_{evidence}'.encode()).hexdigest()[:8]}"
        
        # Génération recommandation
        remediation = self._generate_remediation(vulnerability_type, evidence)
        
        return SecurityFinding(
            finding_id=finding_id,
            vulnerability_type=vulnerability_type,
            security_level=security_level,
            title=title,
            description=description,
            location=location,
            line_number=line_number,
            cwe_id=self._get_cwe_id(vulnerability_type),
            cvss_score=self._get_cvss_score(security_level),
            remediation=remediation,
            evidence=evidence
        )

    def _determine_security_level(self, vuln_type: VulnerabilityType) -> SecurityLevel:
        """Détermine le niveau de sécurité basé sur le type de vulnérabilité"""
        critical_vulns = {
            VulnerabilityType.INJECTION,
            VulnerabilityType.BROKEN_AUTH,
            VulnerabilityType.INSECURE_DESERIALIZATION
        }
        
        high_vulns = {
            VulnerabilityType.XSS,
            VulnerabilityType.SENSITIVE_DATA,
            VulnerabilityType.BROKEN_ACCESS
        }
        
        if vuln_type in critical_vulns:
            return SecurityLevel.CRITICAL
        elif vuln_type in high_vulns:
            return SecurityLevel.HIGH
        else:
            return SecurityLevel.MEDIUM

    def _get_cwe_id(self, vuln_type: VulnerabilityType) -> Optional[str]:
        """Retourne l'ID CWE correspondant au type de vulnérabilité"""
        cwe_mapping = {
            VulnerabilityType.INJECTION: "CWE-89",
            VulnerabilityType.XSS: "CWE-79",
            VulnerabilityType.BROKEN_AUTH: "CWE-287",
            VulnerabilityType.SENSITIVE_DATA: "CWE-200",
            VulnerabilityType.XXE: "CWE-611",
            VulnerabilityType.BROKEN_ACCESS: "CWE-285",
            VulnerabilityType.MISCONFIGURATION: "CWE-16",
            VulnerabilityType.INSECURE_DESERIALIZATION: "CWE-502",
            VulnerabilityType.VULNERABLE_COMPONENTS: "CWE-1104",
            VulnerabilityType.INSUFFICIENT_LOGGING: "CWE-778"
        }
        return cwe_mapping.get(vuln_type)

    def _get_cvss_score(self, security_level: SecurityLevel) -> Optional[float]:
        """Retourne un score CVSS basé sur le niveau de sécurité"""
        score_mapping = {
            SecurityLevel.CRITICAL: 9.5,
            SecurityLevel.HIGH: 7.5,
            SecurityLevel.MEDIUM: 5.5,
            SecurityLevel.LOW: 3.0,
            SecurityLevel.SECURE: 0.0
        }
        return score_mapping.get(security_level)

    def _generate_remediation(self, vuln_type: VulnerabilityType, evidence: str) -> str:
        """Génère une recommandation de correction basée sur le type de vulnérabilité"""
        remediations = {
            VulnerabilityType.INJECTION: "Utiliser des requêtes préparées et valider toutes les entrées utilisateur",
            VulnerabilityType.XSS: "Encoder toutes les sorties et utiliser une Content Security Policy",
            VulnerabilityType.BROKEN_AUTH: "Implémenter une authentification forte avec MFA",
            VulnerabilityType.SENSITIVE_DATA: "Chiffrer les données sensibles et utiliser des variables d'environnement",
            VulnerabilityType.XXE: "Désactiver le traitement des entités externes XML",
            VulnerabilityType.BROKEN_ACCESS: "Implémenter des contrôles d'accès appropriés",
            VulnerabilityType.MISCONFIGURATION: "Réviser et sécuriser les configurations",
            VulnerabilityType.INSECURE_DESERIALIZATION: "Utiliser des formats de sérialisation sûrs comme JSON",
            VulnerabilityType.VULNERABLE_COMPONENTS: "Mettre à jour vers des versions sécurisées",
            VulnerabilityType.INSUFFICIENT_LOGGING: "Implémenter une journalisation complète des événements de sécurité"
        }
        return remediations.get(vuln_type, "Consulter la documentation de sécurité appropriée")

    async def _calculate_security_score(self, findings: List[SecurityFinding]) -> float:
        """Calcule un score de sécurité global basé sur les vulnérabilités trouvées"""
        if not findings:
            return 10.0
        
        # Points de pénalité par niveau de sécurité
        penalties = {
            SecurityLevel.CRITICAL: 3.0,
            SecurityLevel.HIGH: 2.0,
            SecurityLevel.MEDIUM: 1.0,
            SecurityLevel.LOW: 0.5
        }
        
        total_penalty = sum(penalties.get(finding.security_level, 0) for finding in findings)
        score = max(0.0, 10.0 - total_penalty)
        
        return round(score, 1)

    async def _check_owasp_compliance(self, findings: List[SecurityFinding]) -> Dict[str, bool]:
        """Vérifie la conformité avec OWASP Top 10"""
        owasp_categories = {
            'A01_Broken_Access_Control': VulnerabilityType.BROKEN_ACCESS,
            'A02_Cryptographic_Failures': VulnerabilityType.SENSITIVE_DATA,
            'A03_Injection': VulnerabilityType.INJECTION,
            'A04_Insecure_Design': VulnerabilityType.MISCONFIGURATION,
            'A05_Security_Misconfiguration': VulnerabilityType.MISCONFIGURATION,
            'A06_Vulnerable_Components': VulnerabilityType.VULNERABLE_COMPONENTS,
            'A07_Authentication_Failures': VulnerabilityType.BROKEN_AUTH,
            'A08_Software_Integrity_Failures': VulnerabilityType.INSECURE_DESERIALIZATION,
            'A09_Logging_Failures': VulnerabilityType.INSUFFICIENT_LOGGING,
            'A10_Server_Side_Request_Forgery': VulnerabilityType.INJECTION
        }
        
        compliance = {}
        for category, vuln_type in owasp_categories.items():
            # Conforme si aucune vulnérabilité de ce type trouvée
            has_vuln = any(f.vulnerability_type == vuln_type for f in findings)
            compliance[category] = not has_vuln
        
        return compliance

    async def _generate_security_recommendations(self, findings: List[SecurityFinding]) -> List[str]:
        """Génère des recommandations de sécurité basées sur les vulnérabilités trouvées"""
        recommendations = []
        
        # Recommandations par type de vulnérabilité
        vuln_types_found = {f.vulnerability_type for f in findings}
        
        if VulnerabilityType.INJECTION in vuln_types_found:
            recommendations.append("🛡️ Implémenter une validation stricte des entrées et utiliser des requêtes préparées")
        
        if VulnerabilityType.SENSITIVE_DATA in vuln_types_found:
            recommendations.append("🔐 Migrer tous les secrets vers un gestionnaire de secrets (Azure KeyVault, AWS Secrets Manager)")
        
        if VulnerabilityType.VULNERABLE_COMPONENTS in vuln_types_found:
            recommendations.append("📦 Mettre en place un scan automatique des dépendances vulnérables")
        
        if VulnerabilityType.MISCONFIGURATION in vuln_types_found:
            recommendations.append("⚙️ Réviser toutes les configurations de sécurité et appliquer le principe du moindre privilège")
        
        # Recommandations générales
        critical_count = sum(1 for f in findings if f.security_level == SecurityLevel.CRITICAL)
        if critical_count > 0:
            recommendations.append(f"🚨 URGENT: {critical_count} vulnérabilité(s) critique(s) à corriger immédiatement")
        
        recommendations.append("🔍 Planifier des audits de sécurité réguliers")
        recommendations.append("📚 Former l'équipe aux bonnes pratiques de sécurité")
        
        return recommendations

    def _generate_findings_summary(self, findings: List[SecurityFinding]) -> Dict[str, int]:
        """Génère un résumé des vulnérabilités trouvées"""
        summary = {
            'total': len(findings),
            'critique': 0,
            'haut': 0,
            'moyen': 0,
            'bas': 0
        }
        
        for finding in findings:
            if finding.security_level == SecurityLevel.CRITICAL:
                summary['critique'] += 1
            elif finding.security_level == SecurityLevel.HIGH:
                summary['haut'] += 1
            elif finding.security_level == SecurityLevel.MEDIUM:
                summary['moyen'] += 1
            elif finding.security_level == SecurityLevel.LOW:
                summary['bas'] += 1
        
        return summary

    async def _save_security_report(self, report: SecurityReport):
        """Sauvegarde le rapport de sécurité"""
        try:
            # Création du répertoire de rapports
            reports_dir = Path("nextgeneration/agent_factory_implementation/reports/security")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            # Sauvegarde rapport JSON
            report_file = reports_dir / f"security_report_{report.audit_id}.json"
            
            report_data = {
                'audit_id': report.audit_id,
                'target': report.target,
                'timestamp': report.timestamp.isoformat(),
                'security_score': report.security_score,
                'findings_count': len(report.findings),
                'compliance_status': report.compliance_status,
                'recommendations': report.recommendations,
                'summary': report.summary,
                'findings': [
                    {
                        'finding_id': f.finding_id,
                        'vulnerability_type': f.vulnerability_type.value,
                        'security_level': f.security_level.value,
                        'title': f.title,
                        'description': f.description,
                        'location': f.location,
                        'line_number': f.line_number,
                        'cwe_id': f.cwe_id,
                        'cvss_score': f.cvss_score,
                        'remediation': f.remediation,
                        'evidence': f.evidence
                    }
                    for f in report.findings
                ]
            }
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📄 Rapport sécurité sauvegardé : {report_file}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde rapport sécurité : {e}")

    async def generer_rapport_mission(self) -> Dict[str, Any]:
        """
        📊 Génération du rapport de mission complet
        
        Returns:
            Dict contenant le rapport détaillé de la mission
        """
        self.logger.info("📊 Génération rapport de mission Agent 18")
        
        # Compilation statistiques
        total_audits = len(self.security_reports)
        total_vulns = sum(len(report.findings) for report in self.security_reports.values())
        
        # Calcul score sécurité moyen
        avg_security_score = 0.0
        if self.security_reports:
            avg_security_score = sum(r.security_score for r in self.security_reports.values()) / len(self.security_reports)
        
        # Top vulnérabilités
        all_findings = []
        for report in self.security_reports.values():
            all_findings.extend(report.findings)
        
        vuln_by_type = {}
        for finding in all_findings:
            vuln_type = finding.vulnerability_type.value
            vuln_by_type[vuln_type] = vuln_by_type.get(vuln_type, 0) + 1
        
        # Mise à jour rapport
        self.rapport.update({
            'mission_status': 'TERMINÉ',
            'timestamp': datetime.now().isoformat(),
            'audits_effectués': total_audits,
            'vulnérabilités_détectées': total_vulns,
            'niveau_sécurité_global': round(avg_security_score, 1),
            'vulnérabilités_par_type': vuln_by_type,
            'recommandations_critiques': self._get_critical_recommendations(),
            'conformité_owasp': self._get_global_owasp_compliance(),
            'statistiques': {
                'audits_réalisés': total_audits,
                'fichiers_analysés': sum(1 for r in self.security_reports.values()),
                'score_sécurité_moyen': round(avg_security_score, 1),
                'vulnérabilités_critiques': sum(
                    1 for f in all_findings 
                    if f.security_level == SecurityLevel.CRITICAL
                )
            }
        })
        
        # Sauvegarde rapport
        await self._save_mission_report()
        
        self.logger.info(f"✅ Rapport mission Agent 18 généré - {total_audits} audits, {total_vulns} vulnérabilités")
        return self.rapport

    def _get_critical_recommendations(self) -> List[str]:
        """Récupère les recommandations critiques consolidées"""
        critical_recommendations = set()
        
        for report in self.security_reports.values():
            critical_findings = [
                f for f in report.findings 
                if f.security_level == SecurityLevel.CRITICAL
            ]
            
            if critical_findings:
                critical_recommendations.add("🚨 Corriger immédiatement les vulnérabilités critiques détectées")
                critical_recommendations.update(
                    f"🔴 {f.title}: {f.remediation}" 
                    for f in critical_findings[:3]  # Top 3
                )
        
        return list(critical_recommendations)

    def _get_global_owasp_compliance(self) -> Dict[str, float]:
        """Calcule la conformité OWASP globale"""
        if not self.security_reports:
            return {}
        
        # Agrégation conformité OWASP
        global_compliance = {}
        for report in self.security_reports.values():
            for category, compliant in report.compliance_status.items():
                if category not in global_compliance:
                    global_compliance[category] = []
                global_compliance[category].append(compliant)
        
        # Calcul pourcentage conformité
        compliance_percentage = {}
        for category, results in global_compliance.items():
            compliance_percentage[category] = round(
                sum(results) / len(results) * 100, 1
            )
        
        return compliance_percentage

    async def _save_mission_report(self):
        """Sauvegarde le rapport de mission"""
        try:
            reports_dir = Path("nextgeneration/agent_factory_implementation/reports")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            report_file = reports_dir / f"agent_{self.agent_id}_mission_securite_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.rapport, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📄 Rapport mission sauvegardé : {report_file}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde rapport mission : {e}")

async def main():
    """
    🚀 Point d'entrée principal Agent 18
    """
    print("🔐 Démarrage Agent 18 - Auditeur Sécurité Spécialisé")
    
    # Initialisation agent
    agent = Agent18AuditeurSecurite()
    
    # Exemple d'audit de sécurité
    test_targets = [
        "nextgeneration/agent_factory_implementation/agents",
        "nextgeneration/agent_factory_implementation/core",
    ]
    
    for target in test_targets:
        if Path(target).exists():
            print(f"\n🔍 Audit sécurité : {target}")
            try:
                report = await agent.auditer_securite_complete(target)
                print(f"✅ Audit terminé - Score sécurité : {report.security_score}/10")
                print(f"📊 Vulnérabilités trouvées : {len(report.findings)}")
                
                # Affichage vulnérabilités critiques
                critical_findings = [
                    f for f in report.findings 
                    if f.security_level == SecurityLevel.CRITICAL
                ]
                if critical_findings:
                    print(f"🚨 {len(critical_findings)} vulnérabilité(s) critique(s) détectée(s) !")
                    for finding in critical_findings[:3]:  # Top 3
                        print(f"   - {finding.title} ({finding.location})")
                
            except Exception as e:
                print(f"❌ Erreur audit {target}: {e}")
    
    # Génération rapport final
    print("\n📊 Génération rapport de mission...")
    rapport_final = await agent.generer_rapport_mission()
    
    print("\n🔐 === RAPPORT MISSION AGENT 18 ===")
    print(f"📊 Audits effectués : {rapport_final['audits_effectués']}")
    print(f"🔍 Vulnérabilités détectées : {rapport_final['vulnérabilités_détectées']}")
    print(f"🛡️ Score sécurité global : {rapport_final['niveau_sécurité_global']}/10")
    
    if rapport_final['recommandations_critiques']:
        print("\n🚨 RECOMMANDATIONS CRITIQUES :")
        for rec in rapport_final['recommandations_critiques'][:5]:
            print(f"   {rec}")
    
    print("\n✅ Mission Agent 18 terminée avec succès !")

if __name__ == "__main__":
    asyncio.run(main()) 