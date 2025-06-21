#!/usr/bin/env python3
"""

# 🔧 CONVERTI AUTOMATIQUEMENT SYNC → ASYNC
# Date: 2025-06-19 19h35 - Correction architecture Pattern Factory
# Raison: Harmonisation async/sync avec core/agent_factory_architecture.py

📋 AGENT 20 - AUDITEUR CONFORMITÉ
Mission : Audit de conformité aux standards et réglementations

Responsabilités :
- Vérification conformité standards de codage
- Audit documentation obligatoire
- Contrôle respect des conventions
- Validation licences et copyright
- Vérification accessibilité
- Conformité RGPD et réglementations
"""

import asyncio
from logging_manager_optimized import LoggingManager
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import re
from dataclasses import dataclass
from enum import Enum
import sys

class ConformityLevel(Enum):
    COMPLIANT = "conforme"
    MINOR_ISSUES = "problèmes_mineurs"
    MAJOR_ISSUES = "problèmes_majeurs"
    NON_COMPLIANT = "non_conforme"
    CRITICAL = "critique"

class StandardType(Enum):
    CODING_STANDARDS = "standards_codage"
    DOCUMENTATION = "documentation"
    LICENSING = "licences"
    ACCESSIBILITY = "accessibilité"
    SECURITY_COMPLIANCE = "conformité_sécurité"
    GDPR = "rgpd"
    QUALITY_ASSURANCE = "assurance_qualité"

@dataclass
class ConformityIssue:
    issue_id: str
    standard_type: StandardType
    conformity_level: ConformityLevel
    title: str
    description: str
    location: str
    line_number: Optional[int]
    requirement: str
    remediation: str
    priority: str

class Agent20AuditeurConformite:
    """📋 Agent 20 - Auditeur Conformité"""
    
    def __init__(self):
    self.agent_id = "20"
    self.specialite = "Audit Conformité"
        
        # Standards de codage Python (PEP 8)
    self.coding_standards = {
    'line_length': {'pattern': r'.{80,}', 'max_length': 79},
    'trailing_whitespace': {'pattern': r'[ \t]+$'},
    'missing_docstring': {'pattern': r'^def [^_].*\):\s*$', 'negative': True},
    'import_order': {'pattern': r'import.*\nfrom'},
    'naming_convention': {
    'class_names': r'class [a-z]',
    'function_names': r'def [A-Z]',
    'constant_names': r'[a-z_]+ = [^A-Z_]'
    }
    }
        
        # Exigences documentation
    self.documentation_requirements = {
    'readme_file': ['README.md', 'README.rst', 'README.txt'],
    'license_file': ['LICENSE', 'LICENSE.txt', 'LICENSE.md'],
    'changelog': ['CHANGELOG.md', 'CHANGELOG.txt', 'HISTORY.md'],
    'contributing': ['CONTRIBUTING.md', 'CONTRIBUTING.txt'],
    'code_of_conduct': ['CODE_OF_CONDUCT.md']
    }
        
        # Patterns RGPD
    self.gdpr_patterns = {
    'personal_data': [
    r'email|e-mail|adresse.*mail',
    r'nom|prénom|surname|firstname',
    r'téléphone|phone|mobile',
    r'adresse|address|domicile',
    r'date.*naissance|birth.*date',
    r'numéro.*sécu|social.*security'
    ],
    'consent_required': [
    r'cookies?',
    r'tracking',
    r'analytics',
    r'marketing',
    r'newsletter'
    ]
    }
        
    self.issues = []
    self.logger = self._setup_logging()

    def _setup_logging(self):
        # LoggingManager NextGeneration - Agent
    from logging_manager_optimized import LoggingManager
    self.logger = LoggingManager().get_agent_logger(
    agent_name="from",
    role="ai_processor",
    domain="general",
    async_enabled=True
    )
    log_dir = Path("nextgeneration/agent_factory_implementation/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
        
    handler = logging.FileHandler(
    log_dir / f"agent_{self.agent_id}_conformite_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    handler.setFormatter(logging.Formatter(
    '%(asctime)s - Agent20_Conformité - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

    async def auditer_conformite_complete(self, target_path: str) -> Dict[str, Any]:
        """Audit de conformité complet"""
    self.logger.info(f"📋 Audit conformité : {target_path}")
        
    target = Path(target_path)
    self.issues = []
        
        # Audit selon le type de cible
    if target.is_file():
    await self._audit_file_conformity(str(target))
    elif target.is_dir():
    await self._audit_project_conformity(target)
        
        # Compilation du rapport
    rapport = {
    'audit_id': f"CONF_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
    'target': target_path,
    'timestamp': datetime.now().isoformat(),
    'issues': [self._serialize_issue(issue) for issue in self.issues],
    'conformity_score': self._calculate_conformity_score(),
    'compliance_status': self._get_compliance_status(),
    'recommendations': self._generate_recommendations(),
    'summary': self._generate_summary()
    }
        
    await self._save_conformity_report(rapport)
    return rapport

    async def _audit_project_conformity(self, project_path: Path):
        """Audit conformité d'un projet complet"""
        
        # 1. Vérification structure projet
    await self._check_project_structure(project_path)
        
        # 2. Audit fichiers documentation
    await self._check_documentation_files(project_path)
        
        # 3. Audit licences
    await self._check_licensing_compliance(project_path)
        
        # 4. Audit fichiers Python
    for py_file in project_path.rglob('*.py'):
    if not self._should_skip_file(py_file):
    await self._audit_file_conformity(str(py_file))
        
        # 5. Vérification RGPD
    await self._check_gdpr_compliance(project_path)

    async def _audit_file_conformity(self, file_path: str):
        """Audit conformité d'un fichier"""
    try:
    content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
            
    if file_path.endswith('.py'):
    await self._check_python_standards(content, file_path)
    elif file_path.endswith(('.md', '.rst', '.txt')):
    await self._check_documentation_standards(content, file_path)
            
            # Vérifications générales
    await self._check_general_standards(content, file_path)
            
    except Exception as e:
    self.logger.error(f"Erreur audit conformité {file_path}: {e}")

    async def _check_project_structure(self, project_path: Path):
        """Vérification structure projet"""
        
        # Fichiers essentiels manquants
    essential_files = ['README.md', 'setup.py', 'requirements.txt']
    for file_name in essential_files:
    if not (project_path / file_name).exists():
                # Recherche alternatives
    alternatives = list(project_path.glob(f"{file_name.split('.')[0]}.*"))
    if not alternatives:
        self.issues.append(ConformityIssue(
            issue_id=f"STRUCT_{file_name}",
            standard_type=StandardType.DOCUMENTATION,
            conformity_level=ConformityLevel.MAJOR_ISSUES,
            title=f"Fichier essentiel manquant : {file_name}",
            description=f"Le fichier {file_name} est requis pour la conformité projet",
            location=str(project_path),
            line_number=None,
            requirement="Structure projet standard",
            remediation=f"Créer le fichier {file_name}",
            priority="haute"
        ))
        
        # Vérification dossiers standards
    standard_dirs = ['src', 'lib', 'tests', 'docs']
    existing_dirs = [d.name for d in project_path.iterdir() if d.is_dir()]
        
    if not any(std_dir in existing_dirs for std_dir in standard_dirs):
    self.issues.append(ConformityIssue(
    issue_id="STRUCT_DIRS",
    standard_type=StandardType.QUALITY_ASSURANCE,
    conformity_level=ConformityLevel.MINOR_ISSUES,
    title="Structure de dossiers non standard",
    description="Aucun dossier standard détecté (src, lib, tests, docs)",
    location=str(project_path),
    line_number=None,
    requirement="Organisation standard du code",
    remediation="Organiser le code dans des dossiers standards",
    priority="moyenne"
    ))

    async def _check_documentation_files(self, project_path: Path):
        """Vérification fichiers documentation"""
        
    for doc_type, file_names in self.documentation_requirements.items():
    found = False
    for file_name in file_names:
    if (project_path / file_name).exists():
        found = True
        break
            
    if not found:
    severity = ConformityLevel.MAJOR_ISSUES if doc_type in ['readme_file', 'license_file'] else ConformityLevel.MINOR_ISSUES
                
    self.issues.append(ConformityIssue(
        issue_id=f"DOC_{doc_type}",
        standard_type=StandardType.DOCUMENTATION,
        conformity_level=severity,
        title=f"Documentation manquante : {doc_type}",
        description=f"Aucun fichier trouvé pour : {', '.join(file_names)}",
        location=str(project_path),
        line_number=None,
        requirement="Documentation projet complète",
        remediation=f"Créer un des fichiers : {', '.join(file_names)}",
        priority="haute" if severity == ConformityLevel.MAJOR_ISSUES else "moyenne"
    ))

    async def _check_licensing_compliance(self, project_path: Path):
        """Vérification conformité licences"""
        
        # Recherche fichier licence
    license_files = list(project_path.glob('LICENSE*'))
        
    if not license_files:
    self.issues.append(ConformityIssue(
    issue_id="LIC_MISSING",
    standard_type=StandardType.LICENSING,
    conformity_level=ConformityLevel.MAJOR_ISSUES,
    title="Fichier licence manquant",
    description="Aucun fichier de licence trouvé",
    location=str(project_path),
    line_number=None,
    requirement="Licence obligatoire pour distribution",
    remediation="Ajouter un fichier LICENSE avec une licence appropriée",
    priority="haute"
    ))
    else:
            # Vérification contenu licence
    for license_file in license_files:
    try:
        content = license_file.read_text(encoding='utf-8')
        if len(content.strip()) < 100:
            self.issues.append(ConformityIssue(
                issue_id=f"LIC_CONTENT_{license_file.name}",
                standard_type=StandardType.LICENSING,
                conformity_level=ConformityLevel.MINOR_ISSUES,
                title="Contenu licence insuffisant",
                description="Le fichier licence semble incomplet",
                location=str(license_file),
                line_number=None,
                requirement="Licence complète et valide",
                remediation="Vérifier et compléter le contenu de la licence",
                priority="moyenne"
            ))
    except Exception:
        pass

    async def _check_python_standards(self, content: str, file_path: str):
        """Vérification standards Python (PEP 8)"""
        
    lines = content.splitlines()
        
    for i, line in enumerate(lines, 1):
            # Longueur de ligne
    if len(line) > 79:
    self.issues.append(ConformityIssue(
        issue_id=f"PEP8_LINE_{i}",
        standard_type=StandardType.CODING_STANDARDS,
        conformity_level=ConformityLevel.MINOR_ISSUES,
        title="Ligne trop longue",
        description=f"Ligne {i} : {len(line)} caractères (max 79)",
        location=file_path,
        line_number=i,
        requirement="PEP 8 - Longueur maximale de ligne",
        remediation="Diviser la ligne ou utiliser des parenthèses",
        priority="basse"
    ))
            
            # Espaces en fin de ligne
    if line.endswith(' ') or line.endswith('\t'):
    self.issues.append(ConformityIssue(
        issue_id=f"PEP8_TRAIL_{i}",
        standard_type=StandardType.CODING_STANDARDS,
        conformity_level=ConformityLevel.MINOR_ISSUES,
        title="Espaces en fin de ligne",
        description=f"Ligne {i} contient des espaces superflus",
        location=file_path,
        line_number=i,
        requirement="PEP 8 - Pas d'espaces superflus",
        remediation="Supprimer les espaces en fin de ligne",
        priority="basse"
    ))
        
        # Vérification docstrings
    if 'def ' in content:
    functions_without_docstring = re.findall(r'def ([^_]\w*)\([^)]*\):\s*\n(?!\s*""")', content)
    for func_name in functions_without_docstring:
    self.issues.append(ConformityIssue(
        issue_id=f"DOC_FUNC_{func_name}",
        standard_type=StandardType.DOCUMENTATION,
        conformity_level=ConformityLevel.MINOR_ISSUES,
        title=f"Docstring manquante : {func_name}",
        description=f"La fonction {func_name} n'a pas de docstring",
        location=file_path,
        line_number=None,
        requirement="Documentation des fonctions publiques",
        remediation=f"Ajouter une docstring à la fonction {func_name}",
        priority="moyenne"
    ))

    async def _check_documentation_standards(self, content: str, file_path: str):
        """Vérification standards documentation"""
        
        # Vérification README
    if 'README' in file_path.upper():
    required_sections = ['description', 'installation', 'usage', 'license']
    missing_sections = []
            
    content_lower = content.lower()
    for section in required_sections:
    if section not in content_lower:
        missing_sections.append(section)
            
    if missing_sections:
    self.issues.append(ConformityIssue(
        issue_id="README_SECTIONS",
        standard_type=StandardType.DOCUMENTATION,
        conformity_level=ConformityLevel.MINOR_ISSUES,
        title="Sections README manquantes",
        description=f"Sections manquantes : {', '.join(missing_sections)}",
        location=file_path,
        line_number=None,
        requirement="README complet et informatif",
        remediation=f"Ajouter les sections : {', '.join(missing_sections)}",
        priority="moyenne"
    ))

    async def _check_general_standards(self, content: str, file_path: str):
        """Vérifications générales"""
        
        # Recherche mots-clés sensibles
    sensitive_keywords = ['password', 'secret', 'key', 'token', 'api_key']
    for keyword in sensitive_keywords:
    if keyword in content.lower():
                # Vérifier si c'est dans une chaîne de caractères (potentiellement sensible)
    pattern = rf'["\'].*{keyword}.*["\']'
    if re.search(pattern, content, re.IGNORECASE):
        self.issues.append(ConformityIssue(
            issue_id=f"SEC_SENSITIVE_{keyword}",
            standard_type=StandardType.SECURITY_COMPLIANCE,
            conformity_level=ConformityLevel.MAJOR_ISSUES,
            title=f"Information sensible détectée : {keyword}",
            description=f"Le mot-clé '{keyword}' pourrait indiquer des données sensibles",
            location=file_path,
            line_number=None,
            requirement="Pas de données sensibles dans le code",
            remediation="Vérifier et déplacer vers variables d'environnement",
            priority="haute"
        ))

    async def _check_gdpr_compliance(self, project_path: Path):
        """Vérification conformité RGPD"""
        
        # Recherche dans tous les fichiers
    for file_path in project_path.rglob('*'):
    if file_path.is_file() and not self._should_skip_file(file_path):
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
                    
                    # Détection données personnelles
        for category, patterns in self.gdpr_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    self.issues.append(ConformityIssue(
                        issue_id=f"GDPR_{category}_{hash(str(file_path))}",
                        standard_type=StandardType.GDPR,
                        conformity_level=ConformityLevel.MAJOR_ISSUES,
                        title=f"Données RGPD détectées : {category}",
                        description=f"Traitement potentiel de données personnelles : {pattern}",
                        location=str(file_path),
                        line_number=None,
                        requirement="Conformité RGPD pour données personnelles",
                        remediation="Vérifier conformité RGPD et ajouter consentement si nécessaire",
                        priority="haute"
                    ))
                    break  # Un seul signalement par catégorie par fichier
                        
    except Exception:
        continue

    def _calculate_conformity_score(self) -> float:
        """Calcule le score de conformité"""
    if not self.issues:
    return 10.0
        
    penalties = {
    ConformityLevel.CRITICAL: 4.0,
    ConformityLevel.NON_COMPLIANT: 3.0,
    ConformityLevel.MAJOR_ISSUES: 2.0,
    ConformityLevel.MINOR_ISSUES: 0.5,
    ConformityLevel.COMPLIANT: 0.0
    }
        
    total_penalty = sum(penalties.get(issue.conformity_level, 1.0) for issue in self.issues)
    score = max(0.0, 10.0 - total_penalty)
        
    return round(score, 1)

    def _get_compliance_status(self) -> Dict[str, bool]:
        """Status de conformité par standard"""
    status = {}
        
    for standard_type in StandardType:
    type_issues = [i for i in self.issues if i.standard_type == standard_type]
    critical_issues = [i for i in type_issues if i.conformity_level in [ConformityLevel.CRITICAL, ConformityLevel.NON_COMPLIANT]]
            
            # Conforme si pas d'issues critiques
    status[standard_type.value] = len(critical_issues) == 0
        
    return status

    def _generate_recommendations(self) -> List[str]:
        """Génère les recommandations"""
    recommendations = set()
        
        # Par niveau de criticité
    critical_issues = [i for i in self.issues if i.conformity_level == ConformityLevel.CRITICAL]
    if critical_issues:
    recommendations.add("🚨 URGENT: Corriger immédiatement les non-conformités critiques")
        
    major_issues = [i for i in self.issues if i.conformity_level == ConformityLevel.MAJOR_ISSUES]
    if major_issues:
    recommendations.add("⚠️ Traiter les problèmes majeurs de conformité")
        
        # Par type de standard
    standard_counts = {}
    for issue in self.issues:
    standard_counts[issue.standard_type] = standard_counts.get(issue.standard_type, 0) + 1
        
    if StandardType.DOCUMENTATION in standard_counts:
    recommendations.add("📚 Améliorer la documentation du projet")
        
    if StandardType.CODING_STANDARDS in standard_counts:
    recommendations.add("🔧 Appliquer les standards de codage (PEP 8)")
        
    if StandardType.LICENSING in standard_counts:
    recommendations.add("⚖️ Régulariser les licences et droits d'auteur")
        
    if StandardType.GDPR in standard_counts:
    recommendations.add("🔒 Évaluer et assurer la conformité RGPD")
        
        # Générales
    recommendations.add("📋 Mettre en place des vérifications automatiques")
    recommendations.add("🔍 Effectuer des audits de conformité réguliers")
        
    return list(recommendations)

    def _generate_summary(self) -> Dict[str, int]:
        """Génère un résumé des issues"""
    summary = {
    'total': len(self.issues),
    'critique': 0,
    'non_conforme': 0,
    'problèmes_majeurs': 0,
    'problèmes_mineurs': 0,
    'conforme': 0
    }
        
    for issue in self.issues:
    if issue.conformity_level == ConformityLevel.CRITICAL:
    summary['critique'] += 1
    elif issue.conformity_level == ConformityLevel.NON_COMPLIANT:
    summary['non_conforme'] += 1
    elif issue.conformity_level == ConformityLevel.MAJOR_ISSUES:
    summary['problèmes_majeurs'] += 1
    elif issue.conformity_level == ConformityLevel.MINOR_ISSUES:
    summary['problèmes_mineurs'] += 1
        
    return summary

    def _serialize_issue(self, issue: ConformityIssue) -> Dict[str, Any]:
        """Sérialise une issue"""
    return {
    'issue_id': issue.issue_id,
    'standard_type': issue.standard_type.value,
    'conformity_level': issue.conformity_level.value,
    'title': issue.title,
    'description': issue.description,
    'location': issue.location,
    'line_number': issue.line_number,
    'requirement': issue.requirement,
    'remediation': issue.remediation,
    'priority': issue.priority
    }

    def _should_skip_file(self, file_path: Path) -> bool:
        """Détermine si un fichier doit être ignoré"""
    skip_dirs = {'__pycache__', '.git', 'node_modules', '.venv', 'venv', '.pytest_cache'}
    skip_extensions = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe'}
        
    if any(part in skip_dirs for part in file_path.parts):
    return True
        
    if file_path.suffix.lower() in skip_extensions:
    return True
        
    return False

    async def _save_conformity_report(self, rapport: Dict[str, Any]):
        """Sauvegarde le rapport de conformité"""
    try:
    reports_dir = Path("nextgeneration/agent_factory_implementation/reports/conformity")
    reports_dir.mkdir(parents=True, exist_ok=True)
            
    report_file = reports_dir / f"conformity_report_{rapport['audit_id']}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
    json.dump(rapport, f, indent=2, ensure_ascii=False)
                
    self.logger.info(f"Rapport conformité sauvegardé : {report_file}")
            
    except Exception as e:
    self.logger.error(f"Erreur sauvegarde rapport conformité : {e}")

async def main():
    """Point d'entrée principal"""
    print("📋 Agent 20 - Auditeur Conformité")
    
    agent = Agent20AuditeurConformite()
    
    # Test sur le projet
    target = "nextgeneration/agent_factory_implementation"
    if Path(target).exists():
    print(f"\n🔍 Audit conformité : {target}")
        
    rapport = await agent.auditer_conformite_complete(target)
        
    print(f"\n📊 RÉSULTATS AUDIT CONFORMITÉ")
    print(f"Score conformité : {rapport['conformity_score']}/10")
    print(f"Issues détectées : {rapport['summary']['total']}")
        
        # Résumé par niveau
    summary = rapport['summary']
    if summary['critique'] > 0:
    print(f"🚨 Critiques : {summary['critique']}")
    if summary['problèmes_majeurs'] > 0:
    print(f"⚠️ Majeurs : {summary['problèmes_majeurs']}")
    if summary['problèmes_mineurs'] > 0:
    print(f"ℹ️ Mineurs : {summary['problèmes_mineurs']}")
        
        # Status conformité
    print(f"\n✅ CONFORMITÉ PAR STANDARD :")
    for standard, compliant in rapport['compliance_status'].items():
    status = "✅ Conforme" if compliant else "❌ Non-conforme"
    print(f"  {standard}: {status}")
        
        # Top recommandations
    if rapport['recommendations']:
    print(f"\n🔧 RECOMMANDATIONS PRIORITAIRES :")
    for rec in rapport['recommendations'][:5]:
    print(f"  {rec}")

if __name__ == "__main__":
    asyncio.run(main()) 