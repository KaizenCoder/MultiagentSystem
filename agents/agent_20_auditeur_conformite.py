#!/usr/bin/env python3
"""
📋 AGENT 20 - AUDITEUR CONFORMITÉ SPÉCIALISÉ - PATTERN FACTORY COMPLIANT
Mission : Audit de conformité aux standards et réglementations + Audit universel de modules Python

Responsabilités :
- Vérification conformité standards de codage (PEP 8, PEP 257)
- Audit documentation obligatoire et accessibilité
- Contrôle respect des conventions de naming
- Validation licences, copyright et propriété intellectuelle
- Vérification conformité RGPD et réglementations
- Audit qualité assurance et processus
- Capacité d'audit universel de modules Python
- Rapport de conformité complet
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

class ConformityLevel(Enum):
    """Niveaux de conformité"""
    COMPLIANT = "conforme"
    MINOR_ISSUES = "problèmes_mineurs"
    MAJOR_ISSUES = "problèmes_majeurs"
    NON_COMPLIANT = "non_conforme"
    CRITICAL = "critique"

class StandardType(Enum):
    """Types de standards"""
    CODING_STANDARDS = "standards_codage"
    DOCUMENTATION = "documentation"
    LICENSING = "licences"
    ACCESSIBILITY = "accessibilité"
    SECURITY_COMPLIANCE = "conformité_sécurité"
    GDPR = "rgpd"
    QUALITY_ASSURANCE = "assurance_qualité"
    NAMING_CONVENTIONS = "conventions_nommage"
    PROJECT_STRUCTURE = "structure_projet"

@dataclass
class ConformityIssue:
    """Problème de conformité détecté"""
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

@dataclass
class ConformityReport:
    """Rapport complet d'audit de conformité"""
    audit_id: str
    target: str
    timestamp: datetime
    issues: List[ConformityIssue]
    conformity_score: float
    compliance_status: Dict[str, bool]
    recommendations: List[str]
    summary: Dict[str, int]

class Agent20AuditeurConformite(Agent):
    """
    📋 AGENT 20 - AUDITEUR CONFORMITÉ SPÉCIALISÉ - PATTERN FACTORY COMPLIANT
    """
    
    def __init__(self, agent_type: str = "auditeur_conformite", **config):
        """Initialise l'agent d'audit de conformité Pattern Factory."""
        super().__init__(agent_type, **config)
        self.agent_id = "20"
        self.specialite = "Auditeur Conformité + Standards + RGPD + Audit Universel"
        self.mission = "Audit conformité complet + standards codage + réglementations + audit modules Python"
        
        # Setup logging Pattern Factory compatible
        self.setup_logging()
        
        # Standards de codage Python (PEP 8, PEP 257)
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

    def setup_logging(self):
        """Configuration du logging Pattern Factory compatible."""
        try:
            # Utiliser LoggingManager centralisé
            logging_manager = LoggingManager()
            custom_log_config = {
                "logger_name": f"agent.{self.agent_id}",
                "metadata": {
                    "agent_name": f"Agent20_{self.agent_id}",
                    "role": "ai_processor",
                    "domain": "conformity"
                },
                "async_enabled": True
            }
            self.logger = logging_manager.get_logger(config_name="default", custom_config=custom_log_config)
        except Exception as e:
            # Fallback sur logging standard
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(f"Agent{self.agent_id}")
            self.logger.info(f"Fallback logging activé pour Agent {self.agent_id}: {e}")

    async def execute_task(self, task: Task) -> Result:
        """
        Exécute une tâche d'audit de conformité (Pattern Factory).
        
        Args:
            task: Tâche à exécuter
            
        Returns:
            Result: Résultat de l'exécution
        """
        try:
            self.logger.info(f"🚀 Agent {self.agent_id} exécute tâche: {task.type}")
            
            if task.type == "audit_conformite":
                return await self._handle_audit_conformite(task)
            elif task.type == "audit_module":
                return await self._handle_audit_module(task)
            elif task.type == "check_standards":
                return await self._handle_check_standards(task)
            elif task.type == "verify_documentation":
                return await self._handle_verify_documentation(task)
            elif task.type == "check_licensing":
                return await self._handle_check_licensing(task)
            elif task.type == "audit_gdpr":
                return await self._handle_audit_gdpr(task)
            else:
                return Result(
                    success=False,
                    data={"error": f"Type de tâche non supporté: {task.type}"},
                    error=f"Tâche {task.type} non reconnue par Agent {self.agent_id}"
                )
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche {task.type}: {e}")
            return Result(
                success=False,
                data={"error": str(e)},
                error=f"Erreur lors de l'exécution: {e}"
            )

    async def _handle_audit_conformite(self, task: Task) -> Result:
        """Gère l'audit de conformité complet."""
        target_path = task.params.get("target_path")
        if not target_path:
            return Result(
                success=False,
                data={"error": "target_path requis"},
                error="Paramètre target_path manquant"
            )
        
        rapport = await self.auditer_conformite_complete(target_path)
        
        return Result(
            success=True,
            data=rapport
        )

    async def _handle_audit_module(self, task: Task) -> Result:
        """Gère l'audit universel d'un module (capacité universelle)."""
        module_path = task.params.get("module_path")
        if not module_path:
            return Result(
                success=False,
                data={"error": "module_path requis"},
                error="Paramètre module_path manquant"
            )
        
        rapport = await self.auditer_module_cible(module_path)
        
        return Result(
            success=True,
            data=rapport
        )

    async def _handle_check_standards(self, task: Task) -> Result:
        """Gère la vérification des standards de codage."""
        file_path = task.params.get("file_path")
        if not file_path:
            return Result(
                success=False,
                data={"error": "file_path requis"},
                error="Paramètre file_path manquant"
            )
        
        issues = await self._check_python_standards_file(file_path)
        
        return Result(
            success=True,
            data={"issues": issues, "total_issues": len(issues)}
        )

    async def _handle_verify_documentation(self, task: Task) -> Result:
        """Gère la vérification de la documentation."""
        project_path = task.params.get("project_path")
        if not project_path:
            return Result(
                success=False,
                data={"error": "project_path requis"},
                error="Paramètre project_path manquant"
            )
        
        issues = await self._check_documentation_files(Path(project_path))
        
        return Result(
            success=True,
            data={"documentation_issues": issues}
        )

    async def _handle_check_licensing(self, task: Task) -> Result:
        """Gère la vérification des licences."""
        project_path = task.params.get("project_path")
        if not project_path:
            return Result(
                success=False,
                data={"error": "project_path requis"},
                error="Paramètre project_path manquant"
            )
        
        issues = await self._check_licensing_compliance(Path(project_path))
        
        return Result(
            success=True,
            data={"licensing_issues": issues}
        )

    async def _handle_audit_gdpr(self, task: Task) -> Result:
        """Gère l'audit RGPD."""
        project_path = task.params.get("project_path")
        if not project_path:
            return Result(
                success=False,
                data={"error": "project_path requis"},
                error="Paramètre project_path manquant"
            )
        
        issues = await self._check_gdpr_compliance(Path(project_path))
        
        return Result(
            success=True,
            data={"gdpr_issues": issues}
        )

    async def auditer_module_cible(self, module_path: str) -> Dict[str, Any]:
        """
        AUDIT UNIVERSEL - Capacité d'auditer n'importe quel module Python.
        Spécialisation: Conformité aux standards, documentation, licences, RGPD.
        """
        self.logger.info(f"🔍 AUDIT UNIVERSEL CONFORMITÉ: {module_path}")
        
        target = Path(module_path)
        if not target.exists():
            return {
                "error": f"Module non trouvé: {module_path}",
                "success": False
            }
        
        # Réinitialiser les issues
        self.issues = []
        
        # Analyse multi-axes spécialisée conformité
        conformity_analysis = {
            "structure_analysis": await self._analyze_code_structure(target),
            "standards_compliance": await self._analyze_coding_standards(target),
            "documentation_audit": await self._analyze_documentation_quality(target),
            "licensing_check": await self._analyze_licensing_compliance(target),
            "naming_conventions": await self._analyze_naming_conventions(target),
            "gdpr_compliance": await self._analyze_gdpr_compliance(target)
        }
        
        # Calcul score conformité global
        conformity_score = self._calculate_conformity_score()
        
        # Génération recommandations
        recommendations = self._generate_conformity_recommendations()
        
        # Rapport d'audit universel conformité
        rapport = {
            "audit_id": f"CONF_UNIVERSAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "target_analyzed": str(target),
            "timestamp": datetime.now().isoformat(),
            "audit_type": "universal_conformity",
            "specialization": "conformity_standards_licensing_gdpr",
            "conformity_analysis": conformity_analysis,
            "conformity_score": conformity_score,
            "total_issues": len(self.issues),
            "issues_by_severity": self._group_issues_by_severity(),
            "compliance_status": self._get_compliance_status(),
            "recommendations": recommendations,
            "executive_summary": {
                "overall_conformity_score": conformity_score,
                "total_conformity_issues": len(self.issues),
                "critical_issues": len([i for i in self.issues if i.conformity_level == ConformityLevel.CRITICAL]),
                "compliance_percentage": (conformity_score / 10.0) * 100
            }
        }
        
        # Sauvegarde du rapport
        await self._save_conformity_report(rapport)
        
        self.logger.info(f"✅ Audit universel conformité terminé: {len(self.issues)} issues détectées")
        return rapport

    async def _analyze_code_structure(self, target: Path) -> Dict[str, Any]:
        """Analyse la structure du code pour la conformité."""
        structure_issues = []
        
        if target.is_file() and target.suffix == '.py':
            try:
                content = target.read_text(encoding='utf-8', errors='ignore')
                
                # Vérification structure module
                if not content.strip().startswith('#!/usr/bin/env python3') and not content.strip().startswith('"""'):
                    structure_issues.append({
                        "type": "missing_shebang_or_docstring",
                        "description": "Module manque shebang ou docstring en en-tête",
                        "line": 1
                    })
                
                # Vérification imports
                lines = content.split('\n')
                import_section_ended = False
                for i, line in enumerate(lines[:50]):  # Vérifie les 50 premières lignes
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        if import_section_ended:
                            structure_issues.append({
                                "type": "imports_not_at_top",
                                "description": "Imports trouvés après du code",
                                "line": i + 1
                            })
                    elif line.strip() and not line.strip().startswith('#') and not line.strip().startswith('"""'):
                        import_section_ended = True
                
            except Exception as e:
                structure_issues.append({
                    "type": "analysis_error",
                    "description": f"Erreur analyse structure: {e}",
                    "line": None
                })
        
        return {
            "structure_issues": structure_issues,
            "structure_score": max(0, 10 - len(structure_issues) * 2)
        }

    async def _analyze_coding_standards(self, target: Path) -> Dict[str, Any]:
        """Analyse la conformité aux standards de codage (PEP 8)."""
        standards_issues = []
        
        if target.is_file() and target.suffix == '.py':
            try:
                content = target.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                
                for i, line in enumerate(lines):
                    line_num = i + 1
                    
                    # Vérification longueur ligne (PEP 8)
                    if len(line) > 79:
                        standards_issues.append({
                            "type": "line_too_long",
                            "description": f"Ligne trop longue ({len(line)} caractères > 79)",
                            "line": line_num
                        })
                    
                    # Vérification espaces en fin de ligne
                    if line.endswith(' ') or line.endswith('\t'):
                        standards_issues.append({
                            "type": "trailing_whitespace",
                            "description": "Espaces en fin de ligne",
                            "line": line_num
                        })
                    
                    # Vérification indentation (4 espaces)
                    if line.strip() and line.startswith('\t'):
                        standards_issues.append({
                            "type": "tab_indentation",
                            "description": "Utilisation de tabulations au lieu d'espaces",
                            "line": line_num
                        })
                
                # Vérification conventions nommage avec AST
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                                standards_issues.append({
                                    "type": "class_naming_convention",
                                    "description": f"Nom de classe non conforme PEP 8: {node.name}",
                                    "line": node.lineno
                                })
                        elif isinstance(node, ast.FunctionDef):
                            if not re.match(r'^[a-z_][a-z0-9_]*$', node.name) and not node.name.startswith('_'):
                                standards_issues.append({
                                    "type": "function_naming_convention",
                                    "description": f"Nom de fonction non conforme PEP 8: {node.name}",
                                    "line": node.lineno
                                })
                except SyntaxError:
                    standards_issues.append({
                        "type": "syntax_error",
                        "description": "Erreur de syntaxe empêche l'analyse AST",
                        "line": None
                    })
                
            except Exception as e:
                standards_issues.append({
                    "type": "analysis_error",
                    "description": f"Erreur analyse standards: {e}",
                    "line": None
                })
        
        return {
            "standards_issues": standards_issues,
            "standards_score": max(0, 10 - len(standards_issues) * 0.5)
        }

    async def _analyze_documentation_quality(self, target: Path) -> Dict[str, Any]:
        """Analyse la qualité de la documentation."""
        doc_issues = []
        
        if target.is_file() and target.suffix == '.py':
            try:
                content = target.read_text(encoding='utf-8', errors='ignore')
                
                # Vérification docstring module
                if not content.strip().startswith('"""') and not content.strip().startswith("'''"):
                    doc_issues.append({
                        "type": "missing_module_docstring",
                        "description": "Docstring de module manquante",
                        "line": 1
                    })
                
                # Analyse AST pour docstrings fonctions/classes
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                            if not node.name.startswith('_'):  # Ignore méthodes privées
                                docstring = ast.get_docstring(node)
                                if not docstring:
                                    doc_issues.append({
                                        "type": "missing_docstring",
                                        "description": f"Docstring manquante pour {type(node).__name__.lower()} '{node.name}'",
                                        "line": node.lineno
                                    })
                                elif len(docstring.strip()) < 10:
                                    doc_issues.append({
                                        "type": "insufficient_docstring",
                                        "description": f"Docstring trop courte pour {type(node).__name__.lower()} '{node.name}'",
                                        "line": node.lineno
                                    })
                except SyntaxError:
                    doc_issues.append({
                        "type": "syntax_error_ast",
                        "description": "Erreur syntaxe empêche analyse docstrings",
                        "line": None
                    })
                
            except Exception as e:
                doc_issues.append({
                    "type": "analysis_error",
                    "description": f"Erreur analyse documentation: {e}",
                    "line": None
                })
        
        return {
            "documentation_issues": doc_issues,
            "documentation_score": max(0, 10 - len(doc_issues) * 1.5)
        }

    async def _analyze_licensing_compliance(self, target: Path) -> Dict[str, Any]:
        """Analyse la conformité des licences."""
        licensing_issues = []
        
        if target.is_file():
            try:
                content = target.read_text(encoding='utf-8', errors='ignore')
                
                # Vérification mention copyright
                if not re.search(r'copyright|©|\(c\)', content, re.IGNORECASE):
                    licensing_issues.append({
                        "type": "missing_copyright",
                        "description": "Aucune mention de copyright trouvée",
                        "line": None
                    })
                
                # Vérification mention licence
                license_patterns = [
                    r'license|licence',
                    r'MIT|GPL|BSD|Apache',
                    r'All rights reserved',
                    r'Licensed under'
                ]
                
                has_license = any(re.search(pattern, content, re.IGNORECASE) for pattern in license_patterns)
                if not has_license:
                    licensing_issues.append({
                        "type": "missing_license_info",
                        "description": "Aucune information de licence trouvée",
                        "line": None
                    })
                
            except Exception as e:
                licensing_issues.append({
                    "type": "analysis_error",
                    "description": f"Erreur analyse licence: {e}",
                    "line": None
                })
        
        # Vérification fichier LICENSE au niveau projet
        if target.is_dir():
            license_files = ['LICENSE', 'LICENSE.txt', 'LICENSE.md', 'COPYING']
            has_license_file = any((target / license_file).exists() for license_file in license_files)
            
            if not has_license_file:
                licensing_issues.append({
                    "type": "missing_license_file",
                    "description": "Aucun fichier LICENSE trouvé dans le projet",
                    "line": None
                })
        
        return {
            "licensing_issues": licensing_issues,
            "licensing_score": max(0, 10 - len(licensing_issues) * 3)
        }

    async def _analyze_naming_conventions(self, target: Path) -> Dict[str, Any]:
        """Analyse les conventions de nommage."""
        naming_issues = []
        
        if target.is_file() and target.suffix == '.py':
            try:
                content = target.read_text(encoding='utf-8', errors='ignore')
                
                # Analyse avec AST
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            # Classes: PascalCase
                            if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                                naming_issues.append({
                                    "type": "class_naming",
                                    "description": f"Classe '{node.name}' devrait être en PascalCase",
                                    "line": node.lineno
                                })
                        
                        elif isinstance(node, ast.FunctionDef):
                            # Fonctions: snake_case
                            if not re.match(r'^[a-z_][a-z0-9_]*$', node.name) and not node.name.startswith('__'):
                                naming_issues.append({
                                    "type": "function_naming",
                                    "description": f"Fonction '{node.name}' devrait être en snake_case",
                                    "line": node.lineno
                                })
                        
                        elif isinstance(node, ast.Assign):
                            # Constantes: UPPER_CASE
                            for target in node.targets:
                                if isinstance(target, ast.Name) and target.id.isupper():
                                    if not re.match(r'^[A-Z][A-Z0-9_]*$', target.id):
                                        naming_issues.append({
                                            "type": "constant_naming",
                                            "description": f"Constante '{target.id}' devrait être en UPPER_CASE",
                                            "line": node.lineno
                                        })
                
                except SyntaxError:
                    naming_issues.append({
                        "type": "syntax_error_naming",
                        "description": "Erreur syntaxe empêche analyse nommage",
                        "line": None
                    })
                
            except Exception as e:
                naming_issues.append({
                    "type": "analysis_error",
                    "description": f"Erreur analyse nommage: {e}",
                    "line": None
                })
        
        return {
            "naming_issues": naming_issues,
            "naming_score": max(0, 10 - len(naming_issues) * 1)
        }

    async def _analyze_gdpr_compliance(self, target: Path) -> Dict[str, Any]:
        """Analyse la conformité RGPD."""
        gdpr_issues = []
        
        if target.is_file():
            try:
                content = target.read_text(encoding='utf-8', errors='ignore')
                
                # Détection données personnelles
                personal_data_patterns = [
                    r'email|e-mail|adresse.*mail',
                    r'nom|prénom|surname|firstname',
                    r'téléphone|phone|mobile',
                    r'adresse|address|domicile',
                    r'date.*naissance|birth.*date'
                ]
                
                for pattern in personal_data_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        gdpr_issues.append({
                            "type": "personal_data_detected",
                            "description": f"Données personnelles potentielles détectées: {match.group()}",
                            "line": line_num
                        })
                
                # Vérification consentement pour cookies/tracking
                tracking_patterns = [r'cookies?', r'tracking', r'analytics']
                
                for pattern in tracking_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        if not re.search(r'consent|consentement|accepter|agreement', content, re.IGNORECASE):
                            gdpr_issues.append({
                                "type": "missing_consent_mechanism",
                                "description": f"Tracking détecté sans mécanisme de consentement évident",
                                "line": None
                            })
                
            except Exception as e:
                gdpr_issues.append({
                    "type": "analysis_error",
                    "description": f"Erreur analyse RGPD: {e}",
                    "line": None
                })
        
        return {
            "gdpr_issues": gdpr_issues,
            "gdpr_score": max(0, 10 - len(gdpr_issues) * 2)
        }

    async def auditer_conformite_complete(self, target_path: str) -> Dict[str, Any]:
        """Audit de conformité complet d'un projet ou fichier."""
        self.logger.info(f"📋 Audit conformité complet: {target_path}")
        
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
        """Audit conformité d'un projet complet."""
        
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
        """Audit conformité d'un fichier."""
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
        """Vérification structure du projet."""
        required_files = ['README.md', 'requirements.txt', 'setup.py']
        
        for required_file in required_files:
            if not (project_path / required_file).exists():
                self.issues.append(ConformityIssue(
                    issue_id=f"STRUCT_{uuid.uuid4().hex[:8]}",
                    standard_type=StandardType.PROJECT_STRUCTURE,
                    conformity_level=ConformityLevel.MAJOR_ISSUES,
                    title=f"Fichier requis manquant: {required_file}",
                    description=f"Le fichier {required_file} est requis pour un projet Python standard",
                    location=str(project_path),
                    line_number=None,
                    requirement="Structure projet standard",
                    remediation=f"Créer le fichier {required_file}",
                    priority="medium"
                ))

    async def _check_documentation_files(self, project_path: Path):
        """Vérification des fichiers de documentation."""
        for doc_type, file_names in self.documentation_requirements.items():
            found = any((project_path / name).exists() for name in file_names)
            
            if not found:
                self.issues.append(ConformityIssue(
                    issue_id=f"DOC_{uuid.uuid4().hex[:8]}",
                    standard_type=StandardType.DOCUMENTATION,
                    conformity_level=ConformityLevel.MINOR_ISSUES,
                    title=f"Documentation manquante: {doc_type}",
                    description=f"Aucun fichier trouvé pour {doc_type}: {file_names}",
                    location=str(project_path),
                    line_number=None,
                    requirement="Documentation complète",
                    remediation=f"Créer un fichier {file_names[0]}",
                    priority="low"
                ))

    async def _check_licensing_compliance(self, project_path: Path):
        """Vérification conformité des licences."""
        license_files = ['LICENSE', 'LICENSE.txt', 'LICENSE.md']
        has_license = any((project_path / license_file).exists() for license_file in license_files)
        
        if not has_license:
            self.issues.append(ConformityIssue(
                issue_id=f"LIC_{uuid.uuid4().hex[:8]}",
                standard_type=StandardType.LICENSING,
                conformity_level=ConformityLevel.CRITICAL,
                title="Licence manquante",
                description="Aucun fichier de licence trouvé dans le projet",
                location=str(project_path),
                line_number=None,
                requirement="Licence obligatoire",
                remediation="Ajouter un fichier LICENSE approprié",
                priority="high"
            ))

    async def _check_python_standards(self, content: str, file_path: str):
        """Vérification standards Python (PEP 8)."""
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_num = i + 1
            
            # Longueur de ligne
            if len(line) > 79:
                self.issues.append(ConformityIssue(
                    issue_id=f"PEP8_{uuid.uuid4().hex[:8]}",
                    standard_type=StandardType.CODING_STANDARDS,
                    conformity_level=ConformityLevel.MINOR_ISSUES,
                    title="Ligne trop longue",
                    description=f"Ligne {line_num}: {len(line)} caractères (max 79)",
                    location=file_path,
                    line_number=line_num,
                    requirement="PEP 8 - Longueur ligne",
                    remediation="Raccourcir la ligne ou la diviser",
                    priority="low"
                ))

    async def _check_documentation_standards(self, content: str, file_path: str):
        """Vérification standards documentation."""
        if not content.strip():
            self.issues.append(ConformityIssue(
                issue_id=f"DOC_{uuid.uuid4().hex[:8]}",
                standard_type=StandardType.DOCUMENTATION,
                conformity_level=ConformityLevel.MAJOR_ISSUES,
                title="Document vide",
                description="Le document de documentation est vide",
                location=file_path,
                line_number=None,
                requirement="Documentation non vide",
                remediation="Ajouter du contenu au document",
                priority="medium"
            ))

    async def _check_general_standards(self, content: str, file_path: str):
        """Vérifications générales."""
        # Vérification caractères de fin de ligne
        if '\r\n' in content:
            self.issues.append(ConformityIssue(
                issue_id=f"GEN_{uuid.uuid4().hex[:8]}",
                standard_type=StandardType.CODING_STANDARDS,
                conformity_level=ConformityLevel.MINOR_ISSUES,
                title="Caractères de fin de ligne Windows",
                description="Le fichier utilise des fins de ligne Windows (CRLF)",
                location=file_path,
                line_number=None,
                requirement="Fins de ligne Unix (LF)",
                remediation="Convertir en fins de ligne Unix",
                priority="low"
            ))

    async def _check_gdpr_compliance(self, project_path: Path):
        """Vérification conformité RGPD."""
        privacy_files = ['PRIVACY.md', 'privacy-policy.md', 'PRIVACY_POLICY.md']
        has_privacy_policy = any((project_path / privacy_file).exists() for privacy_file in privacy_files)
        
        if not has_privacy_policy:
            self.issues.append(ConformityIssue(
                issue_id=f"GDPR_{uuid.uuid4().hex[:8]}",
                standard_type=StandardType.GDPR,
                conformity_level=ConformityLevel.MAJOR_ISSUES,
                title="Politique de confidentialité manquante",
                description="Aucune politique de confidentialité trouvée",
                location=str(project_path),
                line_number=None,
                requirement="RGPD - Politique confidentialité",
                remediation="Créer une politique de confidentialité",
                priority="high"
            ))

    async def _check_python_standards_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Vérification standards Python pour un fichier spécifique."""
        issues = []
        try:
            content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
            await self._check_python_standards(content, file_path)
            issues = [self._serialize_issue(issue) for issue in self.issues]
        except Exception as e:
            self.logger.error(f"Erreur vérification standards {file_path}: {e}")
        
        return issues

    def _should_skip_file(self, file_path: Path) -> bool:
        """Détermine si un fichier doit être ignoré."""
        skip_patterns = [
            '__pycache__', '.git', '.pytest_cache', 
            'node_modules', '.venv', 'venv', 'build', 'dist'
        ]
        
        return any(pattern in str(file_path) for pattern in skip_patterns)

    def _calculate_conformity_score(self) -> float:
        """Calcule le score de conformité (0-10)."""
        if not self.issues:
            return 10.0
        
        # Pondération par niveau de conformité
        weights = {
            ConformityLevel.CRITICAL: 3.0,
            ConformityLevel.NON_COMPLIANT: 2.5,
            ConformityLevel.MAJOR_ISSUES: 2.0,
            ConformityLevel.MINOR_ISSUES: 1.0,
            ConformityLevel.COMPLIANT: 0.0
        }
        
        total_penalty = sum(weights.get(issue.conformity_level, 1.0) for issue in self.issues)
        score = max(0.0, 10.0 - (total_penalty * 0.5))
        
        return round(score, 2)

    def _get_compliance_status(self) -> Dict[str, bool]:
        """Retourne le statut de conformité par catégorie."""
        status = {}
        
        for standard_type in StandardType:
            issues_for_type = [i for i in self.issues if i.standard_type == standard_type]
            critical_issues = [i for i in issues_for_type if i.conformity_level == ConformityLevel.CRITICAL]
            status[standard_type.value] = len(critical_issues) == 0
        
        return status

    def _generate_recommendations(self) -> List[str]:
        """Génère des recommandations basées sur les issues trouvées."""
        recommendations = []
        
        # Grouper par type de problème
        issue_types = {}
        for issue in self.issues:
            if issue.standard_type not in issue_types:
                issue_types[issue.standard_type] = []
            issue_types[issue.standard_type].append(issue)
        
        # Recommandations par type
        if StandardType.CODING_STANDARDS in issue_types:
            recommendations.append("Implémenter un linter automatique (flake8, black) pour la conformité PEP 8.")
        
        if StandardType.DOCUMENTATION in issue_types:
            recommendations.append("Compléter la documentation manquante (README, docstrings).")
        
        if StandardType.LICENSING in issue_types:
            recommendations.append("Ajouter une licence appropriée au projet.")
        
        if StandardType.GDPR in issue_types:
            recommendations.append("Implementer les mesures de conformité RGPD requises.")
        
        return recommendations

    def _generate_summary(self) -> Dict[str, int]:
        """Génère un résumé des issues par niveau."""
        summary = {level.value: 0 for level in ConformityLevel}
        
        for issue in self.issues:
            summary[issue.conformity_level.value] += 1
        
        summary['total'] = len(self.issues)
        return summary

    def _group_issues_by_severity(self) -> Dict[str, int]:
        """Groupe les issues par niveau de sévérité."""
        return {
            "critical": len([i for i in self.issues if i.conformity_level == ConformityLevel.CRITICAL]),
            "major": len([i for i in self.issues if i.conformity_level == ConformityLevel.MAJOR_ISSUES]),
            "minor": len([i for i in self.issues if i.conformity_level == ConformityLevel.MINOR_ISSUES]),
            "compliant": len([i for i in self.issues if i.conformity_level == ConformityLevel.COMPLIANT])
        }

    def _generate_conformity_recommendations(self) -> List[str]:
        """Génère des recommandations spécialisées conformité."""
        recommendations = []
        
        critical_issues = [i for i in self.issues if i.conformity_level == ConformityLevel.CRITICAL]
        major_issues = [i for i in self.issues if i.conformity_level == ConformityLevel.MAJOR_ISSUES]
        
        if critical_issues:
            recommendations.append("CRITIQUE: Résoudre immédiatement les problèmes de conformité critiques.")
        
        if major_issues:
            recommendations.append("IMPORTANT: Traiter les problèmes majeurs de conformité.")
        
        # Recommandations par domaine
        coding_issues = [i for i in self.issues if i.standard_type == StandardType.CODING_STANDARDS]
        if coding_issues:
            recommendations.append("Mettre en place des outils d'automatisation pour la conformité PEP 8.")
        
        doc_issues = [i for i in self.issues if i.standard_type == StandardType.DOCUMENTATION]
        if doc_issues:
            recommendations.append("Améliorer la documentation et les docstrings.")
        
        return recommendations

    def _serialize_issue(self, issue: ConformityIssue) -> Dict[str, Any]:
        """Sérialise une issue en dictionnaire."""
        return {
            "issue_id": issue.issue_id,
            "standard_type": issue.standard_type.value,
            "conformity_level": issue.conformity_level.value,
            "title": issue.title,
            "description": issue.description,
            "location": issue.location,
            "line_number": issue.line_number,
            "requirement": issue.requirement,
            "remediation": issue.remediation,
            "priority": issue.priority
        }

    async def _save_conformity_report(self, rapport: Dict[str, Any]):
        """Sauvegarde le rapport de conformité."""
        try:
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            # Nom de fichier avec timestamp
            filename = f"agent_20_conformity_report_{rapport['audit_id']}.json"
            report_path = reports_dir / filename
            
            # Sauvegarde JSON
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"📄 Rapport de conformité sauvegardé: {report_path}")
            
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde rapport conformité: {e}")

    async def startup(self) -> bool:
        """Démarrage de l'agent (Pattern Factory)."""
        try:
            self.logger.info(f"🚀 Démarrage Agent {self.agent_id} - Auditeur Conformité")
            # Initialisation des ressources si nécessaire
            return True
        except Exception as e:
            self.logger.error(f"Erreur démarrage Agent {self.agent_id}: {e}")
            return False

    async def shutdown(self) -> bool:
        """Arrêt de l'agent (Pattern Factory)."""
        try:
            self.logger.info(f"🔌 Arrêt Agent {self.agent_id} - Auditeur Conformité")
            # Nettoyage des ressources si nécessaire
            return True
        except Exception as e:
            self.logger.error(f"Erreur arrêt Agent {self.agent_id}: {e}")
            return False

    async def health_check(self) -> Dict[str, Any]:
        """Vérification de l'état de l'agent (Pattern Factory)."""
        return {
            "agent_id": self.agent_id,
            "status": "healthy",
            "specialite": self.specialite,
            "capabilities": self.get_capabilities(),
            "timestamp": datetime.now().isoformat()
        }

    def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'agent (Pattern Factory)."""
        return [
            "audit_conformite_complete",
            "audit_universel_module",
            "verification_standards_codage_pep8",
            "audit_documentation_qualite",
            "verification_licences_copyright",
            "audit_conformite_rgpd",
            "verification_conventions_nommage",
            "analyse_structure_projet",
            "generation_rapports_conformite",
            "recommandations_conformite",
            "scoring_conformite_global"
        ]


# Factory function pour créer l'agent
def create_agent_20_auditeur_conformite(**config) -> Agent20AuditeurConformite:
    """Factory function pour créer une instance de l'Agent 20."""
    return Agent20AuditeurConformite(**config)


# Point d'entrée CLI pour tests
if __name__ == "__main__":
    async def test_agent_cli():
        """Test CLI de l'agent."""
        print("🧪 Test Agent 20 - Auditeur Conformité")
        
        # Création agent
        agent = create_agent_20_auditeur_conformite()
        
        # Test démarrage
        if not await agent.startup():
            print("❌ Échec démarrage agent")
            return
        
        print(f"✅ Agent {agent.agent_id} démarré avec succès")
        print(f"📋 Spécialité: {agent.specialite}")
        print(f"🎯 Mission: {agent.mission}")
        
        # Test health check
        health = await agent.health_check()
        print(f"💚 Santé agent: {health['status']}")
        
        # Test capacités
        capabilities = agent.get_capabilities()
        print(f"🔧 Capacités ({len(capabilities)}):")
        for cap in capabilities:
            print(f"  - {cap}")
        
        # Test audit universel sur lui-même
        print("\n🔍 Test audit universel sur agent_20_auditeur_conformite.py...")
        
        current_file = __file__
        audit_task = Task(
            type="audit_module",
            params={"module_path": current_file}
        )
        
        result = await agent.execute_task(audit_task)
        
        if result.success:
            print("✅ Audit universel réussi!")
            report = result.data
            print(f"📊 Score conformité: {report.get('conformity_score', 'N/A')}/10")
            print(f"🔍 Issues détectées: {report.get('total_issues', 0)}")
            
            if 'executive_summary' in report:
                summary = report['executive_summary']
                print(f"📈 Pourcentage conformité: {summary.get('compliance_percentage', 0):.1f}%")
                print(f"⚠️  Issues critiques: {summary.get('critical_issues', 0)}")
            
            print("\n📋 Recommandations:")
            for rec in report.get('recommendations', []):
                print(f"  - {rec}")
        else:
            print(f"❌ Échec audit: {result.message}")
        
        # Test conformité complète
        print("\n📋 Test audit conformité du fichier actuel...")
        
        conformity_task = Task(
            type="audit_conformite",
            params={"target_path": current_file}
        )
        
        result = await agent.execute_task(conformity_task)
        
        if result.success:
            print("✅ Audit conformité réussi!")
            report = result.data
            print(f"📊 Score conformité: {report.get('conformity_score', 'N/A')}/10")
            print(f"🔍 Issues détectées: {report.get('summary', {}).get('total', 0)}")
        else:
            print(f"❌ Échec audit conformité: {result.message}")
        
        # Test arrêt
        if await agent.shutdown():
            print("✅ Agent arrêté proprement")
        else:
            print("⚠️  Problème lors de l'arrêt")
    
    # Exécution du test
    asyncio.run(test_agent_cli())