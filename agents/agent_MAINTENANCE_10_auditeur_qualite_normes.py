#!/usr/bin/env python3
"""
🔍 AGENT MAINTENANCE-10 - AUDITEUR QUALITÉ ET NORMES - AUDIT UNIVERSEL

Mission : Audit universel de qualité et conformité aux normes pour tout module Python
- Audit PEP 8 et standards Python
- Validation documentation et docstrings
- Conformité ISO/IEC 25010 (qualité logiciel)
- Analyse complexité et maintenabilité
- Détection anti-patterns et code smells
- Recommandations d'amélioration

Capacités d'audit universel : Peut auditer n'importe quel module Python
"""

import ast
import sys
import re
import json
import traceback
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

# Pattern Factory imports avec fallback
try:
    from core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
    print("⚠️ Pattern Factory non disponible. Utilisation des classes de fallback.")
    PATTERN_FACTORY_AVAILABLE = False
    # Fallback classes si l'architecture centrale n'est pas disponible
    class Agent:
        def __init__(self, agent_type: str, **config):
            self.agent_id = f"fallback_{agent_type}"
            self.name = f"Fallback {agent_type}"
            self.logger = logging.getLogger(self.agent_id)
        async def startup(self): pass
        async def shutdown(self): pass
        async def health_check(self): return {"status": "healthy"}

    class Task:
        def __init__(self, task_id: str, description: str, **kwargs):
            self.task_id = task_id
            self.description = description
            self.data = kwargs.get('payload', {})
            self.payload = self.data

    class Result:
        def __init__(self, success: bool, data: any = None, error: str = None):
            self.success = success
            self.data = data
            self.error = error

class QualityLevel(Enum):
    """Niveaux de qualité selon ISO/IEC 25010"""
    EXCELLENT = "excellent"     # 9-10/10 - Production ready
    GOOD = "good"              # 7-8/10 - Quelques améliorations
    ACCEPTABLE = "acceptable"   # 5-6/10 - Améliorations requises
    POOR = "poor"              # 3-4/10 - Refactoring nécessaire
    CRITICAL = "critical"      # 0-2/10 - Réecriture recommandée

@dataclass
class QualityIssue:
    """Issue de qualité détectée"""
    type: str                  # Type d'issue (pep8, documentation, complexity, etc.)
    severity: str              # critical, high, medium, low
    description: str           # Description détaillée
    line_number: Optional[int] # Numéro de ligne si applicable
    suggestion: str            # Suggestion d'amélioration
    rule_violated: str         # Règle/standard violé

@dataclass
class QualityMetrics:
    """Métriques de qualité calculées"""
    cyclomatic_complexity: int
    lines_of_code: int
    documentation_coverage: float  # % de fonctions/classes documentées
    pep8_compliance: float        # % de conformité PEP 8
    maintainability_index: float  # Index de maintenabilité (0-100)
    code_duplication: float       # % de code dupliqué détecté
    test_coverage: Optional[float] # % de couverture tests si disponible

class AgentMAINTENANCE10AuditeurQualiteNormes(Agent):
    """🔍 Agent MAINTENANCE-10 - Auditeur Qualité et Normes - Audit Universel"""
    
    def __init__(self, agent_type: str = "auditeur_qualite_normes", **kwargs):
        super().__init__(agent_type, **kwargs)
        self.agent_id = "MAINTENANCE_10"
        self.name = "Agent MAINTENANCE-10 - Auditeur Qualité et Normes"
        self.specialite = "Audit universel qualité/normes Python"
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={
                    "logger_name": f"nextgen.maintenance.auditeur_qualite.{self.agent_id}",
                    "log_dir": "logs/maintenance/auditeur",
                    "metadata": {
                        "agent_type": "MAINTENANCE_10_auditeur_qualite_normes",
                        "agent_role": "auditeur_qualite",
                        "specialite": self.specialite,
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(f"agent.{self.agent_id}")
        
        # Métriques d'audit
        self.audit_metrics = {
            "total_audits": 0,
            "issues_found": 0,
            "critical_issues": 0,
            "modules_audited": [],
            "average_quality_score": 0.0
        }
        
        # Configuration standards
        self.standards_config = {
            "pep8_enabled": True,
            "documentation_required": True,
            "complexity_threshold": 10,
            "maintainability_threshold": 20,
            "iso_25010_compliance": True
        }
        
        self.logger.info(f"🔍 {self.name} initialisé avec capacité d'audit universel")

    async def startup(self):
        """Démarrage de l'agent auditeur"""
        self.logger.info(f"🔍 {self.name} démarré - Audit universel Python activé")

    async def shutdown(self):
        """Arrêt de l'agent auditeur"""
        self.logger.info(f"🔍 {self.name} arrêté - {self.audit_metrics['total_audits']} audits réalisés")

    async def health_check(self) -> Dict[str, Any]:
        """Vérification de l'état de l'agent"""
        return {
            "status": "healthy",
            "agent": self.name,
            "audits_performed": self.audit_metrics["total_audits"],
            "timestamp": datetime.now().isoformat()
        }

    def get_capabilities(self) -> List[str]:
        """Capacités de l'agent auditeur"""
        return [
            "audit_quality_standards",
            "audit_pep8_compliance", 
            "audit_documentation",
            "audit_complexity",
            "audit_maintainability",
            "audit_iso_25010",
            "audit_universal_module",  # Capacité d'audit universel (fichier ou répertoire)
            "generate_quality_report"
        ]

    async def execute_task(self, task: Task) -> Result:
        """Exécution des tâches d'audit universel"""
        try:
            task_type = task.task_id if hasattr(task, 'task_id') else task.description
            
            self.logger.info(f"🔍 Exécution tâche d'audit: {task_type}")
            
            if task_type == "audit_universal_module" or task.description == "audit_universal_module":
                # Audit universel d'un module Python (fichier ou répertoire)
                target_path_payload = task.payload if hasattr(task, 'payload') else {}
                target_path = target_path_payload.get('target_path')
                
                if not target_path and hasattr(task, 'data'): # Fallback for older task structures
                    target_path_data = task.data if isinstance(task.data, dict) else {}
                    target_path = target_path_data.get('target_path') # Prefer target_path
                    if not target_path: # Legacy fallback
                         target_path = target_path_data.get('module_path')


                if target_path:
                    audit_result = await self.audit_universal_module(target_path)
                    return Result(success=True, data=audit_result)
                else:
                    self.logger.error("target_path (ou module_path en fallback) requis pour audit universel mais non trouvé dans task.payload ou task.data")
                    return Result(success=False, error="target_path (ou module_path en fallback) requis pour audit universel")
                    
            elif task_type in self.get_capabilities():
                # Autres types d'audit spécialisés
                result = await self._execute_specialized_audit(task_type, task)
                return Result(success=True, data=result)
            else:
                return Result(success=False, error=f"Type de tâche non supporté: {task_type}")
                
        except Exception as e:
            self.logger.error(f"❌ Erreur execute_task: {e}", exc_info=True)
            return Result(success=False, error=str(e))

    def _should_skip_path(self, path_to_check: Path) -> bool:
        """Vérifie si un chemin doit être ignoré lors du scan de répertoire."""
        common_skip_dirs = {".venv", "venv", "env", "__pycache__", ".git", "node_modules", "build", "dist", "docs", "test", "tests", "tmp", "temp", "logs"}
        # Ignorer les répertoires cachés commençant par '.' et les répertoires communs
        if any(part.startswith('.') for part in path_to_check.parts if part != '.') or \
           any(skipped_dir in path_to_check.parts for skipped_dir in common_skip_dirs):
            return True
        return False

    def _map_score_to_quality_level_value(self, score: float) -> str:
        """Mappe un score numérique à la valeur d'un QualityLevel."""
        if score >= 90: return QualityLevel.EXCELLENT.value
        elif score >= 75: return QualityLevel.GOOD.value
        elif score >= 60: return QualityLevel.ACCEPTABLE.value
        elif score >= 40: return QualityLevel.POOR.value
        else: return QualityLevel.CRITICAL.value

    async def audit_universal_module(self, target_path: str) -> Dict[str, Any]:
        """
        🔍 AUDIT UNIVERSEL ORCHESTRATEUR - Peut auditer un fichier Python unique ou un répertoire entier.
        """
        self.logger.info(f"🔍 Démarrage audit universel orchestré pour: {target_path}")
        start_time = datetime.now()
        
        target = Path(target_path)

        if not target.exists():
            self.logger.error(f"❌ Cible non trouvée: {target_path}")
            return {
                "target_path": target_path,
                "audit_timestamp": start_time.isoformat(),
                "status": "failed",
                "error": "Target not found",
                "error_details": f"Path {target_path} does not exist."
            }

        if target.is_file():
            if target.suffix == '.py':
                self.logger.info(f"Cible est un fichier Python: {target_path}. Lancement de l'audit de fichier unique.")
                file_report = await self._audit_single_python_file(str(target))
                # Mise à jour des métriques d'audit pour un fichier unique
                if file_report.get("status") == "completed":
                    self.audit_metrics["total_audits"] += 1
                    self.audit_metrics["issues_found"] += file_report.get("summary", {}).get("total_issues", 0)
                    self.audit_metrics["critical_issues"] += file_report.get("summary", {}).get("critical_issues", 0)
                    if str(target) not in self.audit_metrics["modules_audited"]:
                        self.audit_metrics["modules_audited"].append(str(target))
                return file_report
            else:
                self.logger.warning(f"❌ Cible fichier non Python: {target_path}. Audit non applicable.")
                return {
                    "target_path": target_path,
                    "audit_timestamp": start_time.isoformat(),
                    "status": "failed",
                    "error": "Not a Python file",
                    "error_details": f"Target {target_path} is not a .py file."
                }
        elif target.is_dir():
            self.logger.info(f"Cible est un répertoire: {target_path}. Lancement de l'audit de répertoire.")
            
            all_file_reports = []
            total_issues_overall = 0
            critical_issues_overall = 0
            sum_quality_scores_overall = 0.0
            files_audited_count = 0
            files_processed_successfully = 0

            for py_file_path in target.rglob('*.py'):
                if self._should_skip_path(py_file_path):
                    self.logger.debug(f"⏭️ Chemin ignoré (skip_path): {py_file_path}")
                    continue
                
                self.logger.debug(f"📄 Audit du fichier dans le répertoire: {py_file_path}")
                files_audited_count +=1
                file_report = await self._audit_single_python_file(str(py_file_path))
                all_file_reports.append(file_report)

                if file_report.get("status") == "completed":
                    files_processed_successfully += 1
                    total_issues_overall += file_report.get("summary", {}).get("total_issues", 0)
                    critical_issues_overall += file_report.get("summary", {}).get("critical_issues", 0)
                    sum_quality_scores_overall += file_report.get("quality_score", 0)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            average_score_overall = (sum_quality_scores_overall / files_processed_successfully) if files_processed_successfully > 0 else 0
            overall_quality_level_value = self._map_score_to_quality_level_value(average_score_overall)

            directory_audit_result = {
                "target_path": target_path,
                "audit_timestamp": start_time.isoformat(),
                "audit_type": "quality_standards_universal_directory",
                "agent_id": self.agent_id,
                "status": "completed" if files_audited_count > 0 else "no_files_audited",
                "duration_seconds": round(duration, 2),
                "summary_report": {
                    "total_python_files_found": files_audited_count,
                    "files_processed_successfully": files_processed_successfully,
                    "total_issues_overall": total_issues_overall,
                    "critical_issues_overall": critical_issues_overall,
                    "average_quality_score": round(average_score_overall, 2),
                    "overall_project_quality_level": overall_quality_level_value
                },
                "individual_file_reports": all_file_reports
            }
            
            # Mise à jour des métriques d'audit pour un répertoire
            self.audit_metrics["total_audits"] += 1 # Compte comme une opération d'audit
            self.audit_metrics["issues_found"] += total_issues_overall
            self.audit_metrics["critical_issues"] += critical_issues_overall
            if str(target) not in self.audit_metrics["modules_audited"]:
                 self.audit_metrics["modules_audited"].append(f"{str(target)} (directory - {files_processed_successfully} files)")

            self.logger.info(f"✅ Audit de répertoire terminé pour: {target_path} - Score Moyen: {average_score_overall:.2f}/100")
            return directory_audit_result
        else:
            self.logger.error(f"❌ Type de cible inconnu: {target_path}")
            return {
                "target_path": target_path,
                "audit_timestamp": start_time.isoformat(),
                "status": "failed",
                "error": "Unknown target type",
                "error_details": f"Target {target_path} is neither a file nor a directory."
            }

    async def _audit_single_python_file(self, module_path: str) -> Dict[str, Any]:
        """🔍 AUDIT DE FICHIER UNIQUE - Audite un seul fichier Python pour la qualité et les normes."""
        self.logger.info(f"📄 Démarrage audit de fichier: {module_path}")
        
        start_time = datetime.now()
        # Note: 'module_path' here refers to the single file being audited.
        # The key in the report remains 'module_path' for consistency with downstream processing if any.
        audit_result = {
            "module_path": module_path, 
            "audit_timestamp": start_time.isoformat(),
            "audit_type": "quality_standards_single_file", # Changed type
            "agent_id": self.agent_id,
            "status": "in_progress"
        }
        
        try:
            # Vérification existence fichier
            target_file = Path(module_path)
            if not target_file.exists(): # Should ideally be caught by orchestrator, but double check
                raise FileNotFoundError(f"Module non trouvé: {module_path}")
            if not target_file.is_file() or target_file.suffix != '.py':
                 raise ValueError(f"Target is not a Python file: {module_path}")

            # 1. Lecture et parsing du code
            source_code = await self._read_module_source(module_path)
            ast_tree = await self._parse_module_ast(source_code)
            
            # 2. Audits spécialisés
            pep8_audit = await self._audit_pep8_compliance(module_path, source_code)
            documentation_audit = await self._audit_documentation_quality(ast_tree, source_code)
            complexity_audit = await self._audit_complexity_metrics(ast_tree)
            maintainability_audit = await self._audit_maintainability(ast_tree, source_code)
            iso_25010_audit = await self._audit_iso_25010_compliance(ast_tree, source_code)
            
            # 3. Calcul des métriques globales
            quality_metrics = await self._calculate_quality_metrics(
                pep8_audit, documentation_audit, complexity_audit, 
                maintainability_audit, iso_25010_audit
            )
            
            # 4. Détermination du niveau de qualité
            quality_level = self._determine_quality_level(quality_metrics)
            
            # 5. Génération des recommandations
            recommendations = await self._generate_quality_recommendations(
                pep8_audit, documentation_audit, complexity_audit,
                maintainability_audit, iso_25010_audit, quality_level
            )
            
            # 6. Compilation du rapport final
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            audit_result.update({
                "status": "completed",
                "duration_seconds": round(duration, 2),
                "quality_score": quality_metrics.get("overall_score", 0),
                "quality_level": quality_level.value,
                "audits": {
                    "pep8_compliance": pep8_audit,
                    "documentation_quality": documentation_audit,
                    "complexity_metrics": complexity_audit,
                    "maintainability": maintainability_audit,
                    "iso_25010_compliance": iso_25010_audit
                },
                "metrics": quality_metrics,
                "recommendations": recommendations,
                "summary": { # Ensure summary structure is consistent
                    "total_issues": quality_metrics.get("total_issues",0),
                    "critical_issues": sum([
                        len([i for i in audit.get("issues", []) if i.get("severity") == "critical"])
                        for audit_name, audit in audit_result.get("audits", {}).items() # Iterate through actual audit results
                    ]) if audit_result.get("audits") else sum([ # Fallback if audits not populated yet (should be)
                        len([i for i in pep8_audit.get("issues", []) if i.get("severity") == "critical"]),
                        len([i for i in documentation_audit.get("issues", []) if i.get("severity") == "critical"]),
                        len([i for i in complexity_audit.get("issues", []) if i.get("severity") == "critical"]),
                        len([i for i in maintainability_audit.get("issues", []) if i.get("severity") == "critical"]),
                        len([i for i in iso_25010_audit.get("issues", []) if i.get("severity") == "critical"])
                    ])
                }
            })
            
            # REMOVED: self.audit_metrics update is now handled by the orchestrator
            
            self.logger.info(f"📄 Audit de fichier terminé: {module_path} - Score: {quality_metrics.get('overall_score', 0)}/100")
            
            return audit_result
            
        except FileNotFoundError as fnf_error: # Specific catch for FileNotFoundError
            self.logger.error(f"❌ Fichier non trouvé durant audit de fichier {module_path}: {fnf_error}", exc_info=False) # No need for full traceback if already logged by orchestrator
            audit_result.update({
                "status": "failed",
                "error": "File not found during single file audit",
                "error_details": str(fnf_error)
            })
            return audit_result
        except ValueError as val_error: # Specific catch for ValueError (e.g. not a .py file)
            self.logger.error(f"❌ Erreur de valeur durant audit de fichier {module_path}: {val_error}", exc_info=False)
            audit_result.update({
                "status": "failed",
                "error": "Invalid file type for single file audit",
                "error_details": str(val_error)
            })
            return audit_result
        except Exception as e:
            self.logger.error(f"❌ Erreur audit de fichier {module_path}: {e}", exc_info=True)
            audit_result.update({
                "status": "failed",
                "error": str(e),
                "error_details": traceback.format_exc()
            })
            return audit_result

    async def _read_module_source(self, module_path: str) -> str:
        """Lecture sécurisée du code source"""
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Tentative avec latin-1 si UTF-8 échoue
            with open(module_path, 'r', encoding='latin-1') as f:
                return f.read()

    async def _parse_module_ast(self, source_code: str) -> ast.Module:
        """Parse AST sécurisé du code source"""
        try:
            return ast.parse(source_code)
        except SyntaxError as e:
            self.logger.warning(f"⚠️ Erreur syntaxe AST: {e}")
            raise

    async def _audit_pep8_compliance(self, module_path: str, source_code: str) -> Dict[str, Any]:
        """Audit conformité PEP 8"""
        pep8_result = {
            "audit_type": "pep8_compliance",
            "score": 0,
            "issues": [],
            "compliance_percentage": 0
        }
        
        try:
            # Vérifications PEP 8 basiques via analyse du code
            issues = []
            lines = source_code.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # Ligne trop longue (>79 caractères)
                if len(line) > 79:
                    issues.append({
                        "type": "line_length",
                        "severity": "medium",
                        "line_number": line_num,
                        "description": f"Ligne trop longue ({len(line)} caractères > 79)",
                        "suggestion": "Diviser la ligne ou utiliser parenthèses",
                        "rule_violated": "PEP 8 - E501"
                    })
                
                # Espaces en fin de ligne
                if line.endswith(' ') or line.endswith('\t'):
                    issues.append({
                        "type": "trailing_whitespace",
                        "severity": "low",
                        "line_number": line_num,
                        "description": "Espaces/tabs en fin de ligne",
                        "suggestion": "Supprimer les espaces en fin de ligne",
                        "rule_violated": "PEP 8 - W291"
                    })
                
                # Mélange tabs/espaces
                if '\t' in line and ' ' in line.lstrip():
                    issues.append({
                        "type": "mixed_indentation",
                        "severity": "high",
                        "line_number": line_num,
                        "description": "Mélange tabs et espaces pour l'indentation",
                        "suggestion": "Utiliser uniquement des espaces (4 par niveau)",
                        "rule_violated": "PEP 8 - E101"
                    })
            
            # Calcul score de conformité
            total_lines = len(lines)
            issue_lines = len(set(issue["line_number"] for issue in issues))
            compliance_percentage = ((total_lines - issue_lines) / total_lines) * 100 if total_lines > 0 else 100
            
            pep8_result.update({
                "score": min(100, max(0, compliance_percentage)),
                "issues": issues,
                "compliance_percentage": round(compliance_percentage, 2),
                "total_lines_checked": total_lines,
                "lines_with_issues": issue_lines
            })
            
        except Exception as e:
            self.logger.error(f"❌ Erreur audit PEP 8: {e}")
            pep8_result["error"] = str(e)
            
        return pep8_result

    async def _audit_documentation_quality(self, ast_tree: ast.Module, source_code: str) -> Dict[str, Any]:
        """Audit qualité de la documentation"""
        doc_result = {
            "audit_type": "documentation_quality",
            "score": 0,
            "issues": [],
            "coverage_percentage": 0
        }
        
        try:
            issues = []
            documented_items = 0
            total_items = 0
            
            # Vérification docstring module
            module_docstring = ast.get_docstring(ast_tree)
            if not module_docstring:
                issues.append({
                    "type": "missing_module_docstring",
                    "severity": "medium",
                    "line_number": 1,
                    "description": "Module sans docstring",
                    "suggestion": "Ajouter une docstring décrivant le module",
                    "rule_violated": "PEP 257"
                })
            
            # Parcours des classes et fonctions
            for node in ast.walk(ast_tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    total_items += 1
                    
                    # Ignorer les méthodes privées/magiques pour le calcul
                    if not node.name.startswith('_'):
                        docstring = ast.get_docstring(node)
                        if docstring:
                            documented_items += 1
                            # Vérifier qualité docstring
                            if len(docstring.strip()) < 10:
                                issues.append({
                                    "type": "insufficient_docstring",
                                    "severity": "low",
                                    "line_number": node.lineno,
                                    "description": f"Docstring trop courte pour {node.name}",
                                    "suggestion": "Étendre la description avec paramètres/retour",
                                    "rule_violated": "PEP 257"
                                })
                        else:
                            issues.append({
                                "type": "missing_docstring",
                                "severity": "medium",
                                "line_number": node.lineno,
                                "description": f"{type(node).__name__} '{node.name}' sans docstring",
                                "suggestion": "Ajouter une docstring décrivant la fonction/classe",
                                "rule_violated": "PEP 257"
                            })
            
            # Calcul couverture documentation
            coverage_percentage = (documented_items / total_items * 100) if total_items > 0 else 100
            
            doc_result.update({
                "score": min(100, max(0, coverage_percentage - len(issues) * 5)),
                "issues": issues,
                "coverage_percentage": round(coverage_percentage, 2),
                "documented_items": documented_items,
                "total_items": total_items
            })
            
        except Exception as e:
            self.logger.error(f"❌ Erreur audit documentation: {e}")
            doc_result["error"] = str(e)
            
        return doc_result

    async def _audit_complexity_metrics(self, ast_tree: ast.Module) -> Dict[str, Any]:
        """Audit métriques de complexité"""
        complexity_result = {
            "audit_type": "complexity_metrics",
            "score": 0,
            "issues": [],
            "max_complexity": 0,
            "average_complexity": 0
        }
        
        try:
            issues = []
            complexities = []
            
            # Calcul complexité cyclomatique simplifiée
            for node in ast.walk(ast_tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    complexity = self._calculate_cyclomatic_complexity(node)
                    complexities.append(complexity)
                    
                    if complexity > self.standards_config["complexity_threshold"]:
                        severity = "critical" if complexity > 15 else "high" if complexity > 12 else "medium"
                        issues.append({
                            "type": "high_complexity",
                            "severity": severity,
                            "line_number": node.lineno,
                            "description": f"Fonction '{node.name}' complexité {complexity}",
                            "suggestion": "Refactoriser en fonctions plus petites",
                            "rule_violated": f"Complexité > {self.standards_config['complexity_threshold']}"
                        })
            
            max_complexity = max(complexities) if complexities else 0
            avg_complexity = sum(complexities) / len(complexities) if complexities else 0
            
            # Score basé sur complexité moyenne
            if avg_complexity <= 5:
                score = 100
            elif avg_complexity <= 10:
                score = 80
            elif avg_complexity <= 15:
                score = 60
            else:
                score = 40
                
            complexity_result.update({
                "score": max(0, score - len(issues) * 10),
                "issues": issues,
                "max_complexity": max_complexity,
                "average_complexity": round(avg_complexity, 2),
                "total_functions": len(complexities)
            })
            
        except Exception as e:
            self.logger.error(f"❌ Erreur audit complexité: {e}")
            complexity_result["error"] = str(e)
            
        return complexity_result

    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calcul simplifié de la complexité cyclomatique"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.Try):
                complexity += len(child.handlers)
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
                
        return complexity

    async def _audit_maintainability(self, ast_tree: ast.Module, source_code: str) -> Dict[str, Any]:
        """Audit maintenabilité selon ISO/IEC 25010"""
        maintainability_result = {
            "audit_type": "maintainability",
            "score": 0,
            "issues": [],
            "maintainability_index": 0
        }
        
        try:
            issues = []
            lines = source_code.split('\n')
            
            # Détection code dupliqué simple
            line_counts = {}
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#') and len(stripped) > 20:
                    line_counts[stripped] = line_counts.get(stripped, 0) + 1
            
            duplicated_lines = {line: count for line, count in line_counts.items() if count > 1}
            
            if duplicated_lines:
                issues.append({
                    "type": "code_duplication",
                    "severity": "medium",
                    "description": f"{len(duplicated_lines)} lignes dupliquées détectées",
                    "suggestion": "Extraire en fonctions communes",
                    "rule_violated": "DRY principle"
                })
            
            # Calcul métriques de maintenabilité
            loc = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
            
            # Index de maintenabilité simplifié (0-100)
            maintainability_index = max(0, 100 - (loc / 10) - len(duplicated_lines) * 5)
            
            maintainability_result.update({
                "score": max(0, maintainability_index - len(issues) * 5),
                "issues": issues,
                "maintainability_index": round(maintainability_index, 2),
                "lines_of_code": loc,
                "duplicated_lines": len(duplicated_lines)
            })
            
        except Exception as e:
            self.logger.error(f"❌ Erreur audit maintenabilité: {e}")
            maintainability_result["error"] = str(e)
            
        return maintainability_result

    async def _audit_iso_25010_compliance(self, ast_tree: ast.Module, source_code: str) -> Dict[str, Any]:
        """Audit conformité ISO/IEC 25010 (qualité logiciel)"""
        iso_result = {
            "audit_type": "iso_25010_compliance",
            "score": 0,
            "issues": [],
            "characteristics": {}
        }
        
        try:
            issues = []
            characteristics = {}
            
            # Fonctionnalité (Functionality)
            func_score = 90  # Base score
            if not ast.get_docstring(ast_tree):
                func_score -= 10
                
            characteristics["functionality"] = func_score
            
            # Fiabilité (Reliability)
            reliability_score = 90
            try_blocks = len([n for n in ast.walk(ast_tree) if isinstance(n, ast.Try)])
            total_functions = len([n for n in ast.walk(ast_tree) if isinstance(n, ast.FunctionDef)])
            
            if try_blocks / max(total_functions, 1) < 0.3:
                reliability_score -= 20
                issues.append({
                    "type": "insufficient_error_handling",
                    "severity": "medium",
                    "description": "Gestion d'erreur insuffisante",
                    "suggestion": "Ajouter try/except dans les fonctions critiques",
                    "rule_violated": "ISO 25010 - Reliability"
                })
                
            characteristics["reliability"] = reliability_score
            
            # Sécurité (Security)
            security_score = 85
            lines = source_code.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # Détection de mots-clés sensibles
                if any(keyword in line.lower() for keyword in ['password', 'secret', 'key']):
                    if '=' in line and not line.strip().startswith('#'):
                        security_score -= 15
                        issues.append({
                            "type": "potential_secret_exposure",
                            "severity": "high",
                            "line_number": line_num,
                            "description": "Possible exposition de secret en dur",
                            "suggestion": "Utiliser variables d'environnement",
                            "rule_violated": "ISO 25010 - Security"
                        })
                        
            characteristics["security"] = security_score
            
            # Score global ISO 25010
            overall_score = sum(characteristics.values()) / len(characteristics)
            
            iso_result.update({
                "score": max(0, overall_score - len(issues) * 5),
                "issues": issues,
                "characteristics": characteristics,
                "overall_compliance": round(overall_score, 2)
            })
            
        except Exception as e:
            self.logger.error(f"❌ Erreur audit ISO 25010: {e}")
            iso_result["error"] = str(e)
            
        return iso_result

    async def _calculate_quality_metrics(self, pep8_audit: Dict, doc_audit: Dict, 
                                       complexity_audit: Dict, maintainability_audit: Dict, 
                                       iso_audit: Dict) -> Dict[str, Any]:
        """Calcul des métriques de qualité globales"""
        try:
            # Pondération des scores
            weights = {
                "pep8": 0.20,        # 20% - Standards de code
                "documentation": 0.25, # 25% - Documentation
                "complexity": 0.20,   # 20% - Complexité
                "maintainability": 0.20, # 20% - Maintenabilité
                "iso_25010": 0.15    # 15% - Conformité ISO
            }
            
            scores = {
                "pep8": pep8_audit.get("score", 0),
                "documentation": doc_audit.get("score", 0),
                "complexity": complexity_audit.get("score", 0),
                "maintainability": maintainability_audit.get("score", 0),
                "iso_25010": iso_audit.get("score", 0)
            }
            
            # Score global pondéré
            overall_score = sum(scores[key] * weights[key] for key in scores.keys())
            
            return {
                "overall_score": round(overall_score, 2),
                "component_scores": scores,
                "weights_used": weights,
                "total_issues": sum([
                    len(pep8_audit.get("issues", [])),
                    len(doc_audit.get("issues", [])),
                    len(complexity_audit.get("issues", [])),
                    len(maintainability_audit.get("issues", [])),
                    len(iso_audit.get("issues", []))
                ]),
                "grade": self._calculate_letter_grade(overall_score)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur calcul métriques: {e}")
            return {"overall_score": 0, "error": str(e)}

    def _calculate_letter_grade(self, score: float) -> str:
        """Calcul note littérale"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def _determine_quality_level(self, quality_metrics: Dict[str, Any]) -> QualityLevel:
        """Détermination du niveau de qualité global"""
        score = quality_metrics.get("overall_score", 0)
        
        if score >= 90:
            return QualityLevel.EXCELLENT
        elif score >= 75:
            return QualityLevel.GOOD
        elif score >= 60:
            return QualityLevel.ACCEPTABLE
        elif score >= 40:
            return QualityLevel.POOR
        else:
            return QualityLevel.CRITICAL

    async def _generate_quality_recommendations(self, pep8_audit: Dict, doc_audit: Dict,
                                              complexity_audit: Dict, maintainability_audit: Dict,
                                              iso_audit: Dict, quality_level: QualityLevel) -> List[Dict[str, Any]]:
        """Génération des recommandations d'amélioration"""
        recommendations = []
        
        try:
            # Recommandations basées sur les audits
            if pep8_audit.get("score", 0) < 80:
                recommendations.append({
                    "priority": "high",
                    "category": "pep8_compliance",
                    "title": "Améliorer la conformité PEP 8",
                    "description": "Le code ne respecte pas suffisamment les standards PEP 8",
                    "actions": [
                        "Utiliser un formateur automatique (black, autopep8)",
                        "Configurer votre IDE pour la vérification PEP 8",
                        "Diviser les lignes trop longues"
                    ]
                })
            
            if doc_audit.get("coverage_percentage", 0) < 70:
                recommendations.append({
                    "priority": "medium",
                    "category": "documentation",
                    "title": "Améliorer la documentation",
                    "description": f"Couverture documentation: {doc_audit.get('coverage_percentage', 0)}%",
                    "actions": [
                        "Ajouter des docstrings aux fonctions/classes",
                        "Documenter les paramètres et valeurs de retour",
                        "Ajouter une docstring descriptive au module"
                    ]
                })
            
            if complexity_audit.get("max_complexity", 0) > 10:
                recommendations.append({
                    "priority": "high",
                    "category": "complexity",
                    "title": "Réduire la complexité cyclomatique",
                    "description": f"Complexité max: {complexity_audit.get('max_complexity', 0)}",
                    "actions": [
                        "Décomposer les fonctions complexes",
                        "Extraire la logique en sous-fonctions",
                        "Utiliser des patterns comme Strategy ou Factory"
                    ]
                })
            
            # Recommandations par niveau de qualité
            if quality_level == QualityLevel.CRITICAL:
                recommendations.append({
                    "priority": "critical",
                    "category": "refactoring",
                    "title": "Refactoring majeur nécessaire",
                    "description": "La qualité globale est critique",
                    "actions": [
                        "Planifier une réécriture complète",
                        "Identifier les parties réutilisables",
                        "Mettre en place des tests avant refactoring"
                    ]
                })
            elif quality_level == QualityLevel.POOR:
                recommendations.append({
                    "priority": "high",
                    "category": "improvement",
                    "title": "Améliorations significatives nécessaires",
                    "description": "Le code nécessite des améliorations importantes",
                    "actions": [
                        "Prioriser les issues critiques",
                        "Améliorer la couverture de tests",
                        "Réviser l'architecture générale"
                    ]
                })
            
        except Exception as e:
            self.logger.error(f"❌ Erreur génération recommandations: {e}")
            
        return recommendations

    async def _execute_specialized_audit(self, audit_type: str, task: Task) -> Dict[str, Any]:
        """Exécution d'audits spécialisés"""
        # Implémentation des audits spécialisés selon le type
        return {"message": f"Audit {audit_type} effectué", "status": "completed"}

# Point d'entrée CLI pour test
async def main():
    """Test CLI de l'agent"""
    import asyncio
    
    # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ - Configuration pour test CLI
    try:
        from core.manager import LoggingManager
        logging_manager = LoggingManager()
        logger = logging_manager.get_logger(
            config_name="maintenance",
            custom_config={
                "logger_name": "nextgen.maintenance.auditeur_qualite.test",
                "log_dir": "logs/maintenance/test",
                "metadata": {"context": "cli_test"}
            }
        )
    except ImportError:
        logging.basicConfig(level=logging.INFO)
    print("🔍 Agent MAINTENANCE-10 - Test audit universel")
    
    agent = AgentMAINTENANCE10AuditeurQualiteNormes()
    await agent.startup()
    
    try:
        # Test audit du fichier agent lui-même
        result = await agent.audit_universal_module(__file__)
        print(f"\n✅ Audit terminé - Score: {result.get('quality_score', 0)}/100")
        print(f"🎯 Niveau: {result.get('quality_level', 'unknown')}")
        print(f"📊 Issues trouvées: {result.get('summary', {}).get('total_issues', 0)}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        await agent.shutdown()

def create_agent_MAINTENANCE_10_auditeur_qualite_normes(**kwargs) -> AgentMAINTENANCE10AuditeurQualiteNormes:
    return AgentMAINTENANCE10AuditeurQualiteNormes(**kwargs)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())