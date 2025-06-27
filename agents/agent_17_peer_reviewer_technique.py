#!/usr/bin/env python3
"""
👨‍💻 AGENT 17 - PEER REVIEWER TECHNIQUE SPÉCIALISÉ - PATTERN FACTORY COMPLIANT
Mission : Peer Review technique détaillée + Audit universel de modules Python

Responsabilités :
- Review technique ligne par ligne du code expert
- Validation implémentation et optimisations
- Contrôle sécurité et performance
- Vérification standards de codage
- Analyse architecture et design patterns
- Capacité d'audit universel de modules Python
- Rapport de review technique complet
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

class ReviewSeverity(Enum):
    """Niveaux de sévérité des findings de review"""
    CRITICAL = "critique"
    HIGH = "haut"
    MEDIUM = "moyen"
    LOW = "bas"
    INFO = "info"

class ReviewCategory(Enum):
    """Catégories de review technique"""
    ARCHITECTURE = "architecture"
    SECURITY = "sécurité"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintenabilité"
    STANDARDS = "standards"
    DESIGN_PATTERNS = "design_patterns"
    ERROR_HANDLING = "gestion_erreurs"
    TESTING = "tests"

@dataclass
class ReviewFinding:
    """Résultat de review technique"""
    finding_id: str
    category: ReviewCategory
    severity: ReviewSeverity
    title: str
    description: str
    location: str
    line_number: Optional[int]
    recommendation: str
    code_snippet: Optional[str]
    impact: str

@dataclass
class TechnicalReviewReport:
    """Rapport complet de review technique"""
    review_id: str
    target: str
    timestamp: datetime
    findings: List[ReviewFinding]
    technical_score: float
    architecture_analysis: Dict[str, Any]
    security_analysis: Dict[str, Any]
    performance_analysis: Dict[str, Any]
    recommendations: List[str]
    summary: Dict[str, int]

class Agent17PeerReviewerTechnique(Agent):
    """
    👨‍💻 AGENT 17 - PEER REVIEWER TECHNIQUE SPÉCIALISÉ - PATTERN FACTORY COMPLIANT
    """
    
    def __init__(self, agent_type: str = "peer_reviewer_technique", **config):
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="general",
                custom_config={
                    "logger_name": f"nextgen.general.17_peer_reviewer_technique.{self.agent_id if hasattr(self, 'agent_id') else self.id if hasattr(self, 'id') else 'unknown'}",
                    "log_dir": "logs/general",
                    "metadata": {
                        "agent_type": "17_peer_reviewer_technique",
                        "agent_role": "general",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)

        """Initialise l'agent de peer review technique Pattern Factory."""
        super().__init__(agent_type, **config)
        self.agent_id = "17"
        self.specialite = "Peer Reviewer Technique + Architecture + Sécurité + Performance + Audit Universel"
        self.mission = "Review technique détaillée ligne par ligne + validation architecture + audit modules Python"
        
        # Setup logging Pattern Factory compatible
        self.setup_logging()
        
        # Patterns de design critiques
        self.design_patterns = {
            'factory_pattern': r'def create_\w+|class \w+Factory',
            'singleton_pattern': r'_instance\s*=|__new__.*cls',
            'observer_pattern': r'add_observer|notify|subscribe',
            'strategy_pattern': r'class \w+Strategy|def execute_strategy',
            'decorator_pattern': r'@\w+|def decorator|wrapper'
        }
        
        # Métriques de code critique
        self.critical_metrics = {
            'cyclomatic_complexity': 10,  # Limite complexité cyclomatique
            'function_length': 50,        # Limite longueur fonction
            'class_length': 500,          # Limite longueur classe
            'nesting_depth': 4,           # Limite profondeur imbrication
            'parameter_count': 7          # Limite nombre paramètres
        }
        
        # Patterns de sécurité
        self.security_patterns = {
            'dangerous_functions': [
                r'eval\(',
                r'exec\(',
                r'__import__',
                r'getattr\(',
                r'setattr\(',
                r'open\(\s*[\'\"]\s*\w+\s*[\'\"]\s*,\s*[\'\"]\s*w'
            ],
            'crypto_patterns': [
                r'hashlib\.(md5|sha1)\(',
                r'random\.random\(',
                r'secrets\.',
                r'cryptography\.',
                r'Crypto\.'
            ]
        }
        
        self.findings = []

    def setup_logging(self):
        """Configuration du logging Pattern Factory compatible."""
        try:
            # Utiliser LoggingManager centralisé
            logging_manager = LoggingManager()
            custom_log_config = {
                "logger_name": f"agent.{self.agent_id}",
                "metadata": {
                    "agent_name": f"Agent17_{self.agent_id}",
                    "role": "ai_processor",
                    "domain": "technical_review"
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
        Exécute une tâche de review technique (Pattern Factory).
        
        Args:
            task: Tâche à exécuter
            
        Returns:
            Result: Résultat de l'exécution
        """
        try:
            self.logger.info(f"🚀 Agent {self.agent_id} exécute tâche: {task.type}")
            
            if task.type == "technical_review":
                return await self._handle_technical_review(task)
            elif task.type == "audit_module":
                return await self._handle_audit_module(task)
            elif task.type == "architecture_review":
                return await self._handle_architecture_review(task)
            elif task.type == "security_review":
                return await self._handle_security_review(task)
            elif task.type == "performance_review":
                return await self._handle_performance_review(task)
            elif task.type == "code_quality_review":
                return await self._handle_code_quality_review(task)
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

    async def _handle_technical_review(self, task: Task) -> Result:
        """Gère la review technique complète."""
        target_path = task.params.get("target_path")
        if not target_path:
            return Result(
                success=False,
                data={"error": "target_path requis"},
                error="Paramètre target_path manquant"
            )
        
        rapport = await self.review_technique_complete(target_path)
        
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

    async def _handle_architecture_review(self, task: Task) -> Result:
        """Gère la review architecture."""
        file_path = task.params.get("file_path")
        if not file_path:
            return Result(
                success=False,
                data={"error": "file_path requis"},
                error="Paramètre file_path manquant"
            )
        
        analysis = await self._analyze_architecture_patterns(Path(file_path))
        
        return Result(
            success=True,
            data={"architecture_analysis": analysis}
        )

    async def _handle_security_review(self, task: Task) -> Result:
        """Gère la review sécurité."""
        file_path = task.params.get("file_path")
        if not file_path:
            return Result(
                success=False,
                data={"error": "file_path requis"},
                error="Paramètre file_path manquant"
            )
        
        analysis = await self._analyze_security_patterns(Path(file_path))
        
        return Result(
            success=True,
            data={"security_analysis": analysis}
        )

    async def _handle_performance_review(self, task: Task) -> Result:
        """Gère la review performance."""
        file_path = task.params.get("file_path")
        if not file_path:
            return Result(
                success=False,
                data={"error": "file_path requis"},
                error="Paramètre file_path manquant"
            )
        
        analysis = await self._analyze_performance_patterns(Path(file_path))
        
        return Result(
            success=True,
            data={"performance_analysis": analysis}
        )

    async def _handle_code_quality_review(self, task: Task) -> Result:
        """Gère la review qualité code."""
        file_path = task.params.get("file_path")
        if not file_path:
            return Result(
                success=False,
                data={"error": "file_path requis"},
                error="Paramètre file_path manquant"
            )
        
        analysis = await self._analyze_code_quality(Path(file_path))
        
        return Result(
            success=True,
            data={"code_quality_analysis": analysis}
        )

    async def auditer_module_cible(self, module_path: str) -> Dict[str, Any]:
        """
        AUDIT UNIVERSEL - Capacité d'auditer n'importe quel module Python.
        Spécialisation: Review technique, architecture, sécurité, performance.
        """
        self.logger.info(f"🔍 AUDIT UNIVERSEL PEER REVIEW TECHNIQUE: {module_path}")
        
        target = Path(module_path)
        if not target.exists():
            return {
                "error": f"Module non trouvé: {module_path}",
                "success": False
            }
        
        # Réinitialiser les findings
        self.findings = []
        
        # Analyse multi-axes spécialisée review technique
        technical_analysis = {
            "architecture_analysis": await self._analyze_architecture_patterns(target),
            "security_analysis": await self._analyze_security_patterns(target),
            "performance_analysis": await self._analyze_performance_patterns(target),
            "code_quality_analysis": await self._analyze_code_quality(target),
            "design_patterns_analysis": await self._analyze_design_patterns(target),
            "complexity_analysis": await self._analyze_code_complexity(target)
        }
        
        # Calcul score technique global
        technical_score = self._calculate_technical_score()
        
        # Génération recommandations
        recommendations = self._generate_technical_recommendations()
        
        # Rapport d'audit universel peer review
        rapport = {
            "review_id": f"TECH_UNIVERSAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "target_analyzed": str(target),
            "timestamp": datetime.now().isoformat(),
            "review_type": "universal_technical_review",
            "specialization": "technical_review_architecture_security_performance",
            "technical_analysis": technical_analysis,
            "technical_score": technical_score,
            "total_findings": len(self.findings),
            "findings_by_severity": self._group_findings_by_severity(),
            "findings_by_category": self._group_findings_by_category(),
            "recommendations": recommendations,
            "executive_summary": {
                "overall_technical_score": technical_score,
                "total_review_findings": len(self.findings),
                "critical_findings": len([f for f in self.findings if f.severity == ReviewSeverity.CRITICAL]),
                "review_quality_percentage": (technical_score / 10.0) * 100
            }
        }
        
        # Sauvegarde du rapport
        await self._save_review_report(rapport)
        
        self.logger.info(f"✅ Audit universel peer review terminé: {len(self.findings)} findings détectés")
        return rapport

    async def _analyze_architecture_patterns(self, target: Path) -> Dict[str, Any]:
        """Analyse les patterns d'architecture."""
        architecture_issues = []
        
        if target.is_file() and target.suffix == '.py':
            try:
                content = target.read_text(encoding='utf-8', errors='ignore')
                
                # Analyse avec AST pour patterns d'architecture
                try:
                    tree = ast.parse(content)
                    
                    # Analyse des classes
                    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                    
                    for cls in classes:
                        # Vérification pattern Factory
                        if 'factory' in cls.name.lower():
                            architecture_issues.append({
                                "type": "factory_pattern_detected",
                                "description": f"Pattern Factory détecté dans classe {cls.name}",
                                "line": cls.lineno,
                                "recommendation": "Valider implémentation pattern Factory"
                            })
                        
                        # Vérification Single Responsibility
                        methods = [n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                        if len(methods) > 20:
                            architecture_issues.append({
                                "type": "srp_violation",
                                "description": f"Classe {cls.name} a {len(methods)} méthodes - possible violation SRP",
                                "line": cls.lineno,
                                "recommendation": "Considérer division de la classe"
                            })
                        
                        # Vérification héritage
                        if len(cls.bases) > 2:
                            architecture_issues.append({
                                "type": "multiple_inheritance",
                                "description": f"Classe {cls.name} hérite de {len(cls.bases)} classes",
                                "line": cls.lineno,
                                "recommendation": "Privilégier composition sur héritage multiple"
                            })
                
                except SyntaxError:
                    architecture_issues.append({
                        "type": "syntax_error",
                        "description": "Erreur syntaxe empêche analyse architecture",
                        "line": None,
                        "recommendation": "Corriger erreurs syntaxe"
                    })
                
            except Exception as e:
                architecture_issues.append({
                    "type": "analysis_error",
                    "description": f"Erreur analyse architecture: {e}",
                    "line": None,
                    "recommendation": "Vérifier accessibilité fichier"
                })
        
        return {
            "architecture_issues": architecture_issues,
            "architecture_score": max(0, 10 - len(architecture_issues) * 1.5)
        }

    async def _analyze_security_patterns(self, target: Path) -> Dict[str, Any]:
        """Analyse les patterns de sécurité."""
        security_issues = []
        
        if target.is_file() and target.suffix == '.py':
            try:
                content = target.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                
                # Recherche de patterns dangereux
                for pattern in self.security_patterns['dangerous_functions']:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        security_issues.append({
                            "type": "dangerous_function",
                            "description": f"Fonction dangereuse détectée: {match.group()}",
                            "line": line_num,
                            "recommendation": "Utiliser alternative sécurisée"
                        })
                
                # Vérification crypto patterns
                for pattern in self.security_patterns['crypto_patterns']:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        if 'md5' in match.group() or 'sha1' in match.group():
                            security_issues.append({
                                "type": "weak_crypto",
                                "description": f"Algorithme cryptographique faible: {match.group()}",
                                "line": line_num,
                                "recommendation": "Utiliser SHA-256 ou plus fort"
                            })
                
                # Vérification gestion erreurs sensibles
                for i, line in enumerate(lines):
                    if 'except:' in line and 'pass' in lines[i+1:i+3]:
                        security_issues.append({
                            "type": "silent_exception",
                            "description": "Exception silencieuse détectée",
                            "line": i + 1,
                            "recommendation": "Logger les exceptions pour audit"
                        })
                
            except Exception as e:
                security_issues.append({
                    "type": "analysis_error",
                    "description": f"Erreur analyse sécurité: {e}",
                    "line": None,
                    "recommendation": "Vérifier accessibilité fichier"
                })
        
        return {
            "security_issues": security_issues,
            "security_score": max(0, 10 - len(security_issues) * 2)
        }

    async def _analyze_performance_patterns(self, target: Path) -> Dict[str, Any]:
        """Analyse les patterns de performance."""
        performance_issues = []
        
        if target.is_file() and target.suffix == '.py':
            try:
                content = target.read_text(encoding='utf-8', errors='ignore')
                
                # Analyse avec AST pour performance
                try:
                    tree = ast.parse(content)
                    
                    # Analyse des boucles imbriquées
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.For, ast.While)):
                            nested_loops = [n for n in ast.walk(node) if isinstance(n, (ast.For, ast.While))]
                            if len(nested_loops) > 3:  # Plus de 2 niveaux d'imbrication
                                performance_issues.append({
                                    "type": "nested_loops",
                                    "description": f"Boucles imbriquées détectées ({len(nested_loops)} niveaux)",
                                    "line": node.lineno,
                                    "recommendation": "Optimiser algorithme ou utiliser comprehensions"
                                })
                    
                    # Analyse des fonctions longues
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if hasattr(node, 'end_lineno') and node.end_lineno:
                                length = node.end_lineno - node.lineno
                                if length > self.critical_metrics['function_length']:
                                    performance_issues.append({
                                        "type": "long_function",
                                        "description": f"Fonction {node.name} trop longue ({length} lignes)",
                                        "line": node.lineno,
                                        "recommendation": "Diviser en fonctions plus petites"
                                    })
                    
                    # Vérification imports dans boucles
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.For, ast.While)):
                            imports = [n for n in ast.walk(node) if isinstance(n, (ast.Import, ast.ImportFrom))]
                            if imports:
                                performance_issues.append({
                                    "type": "import_in_loop",
                                    "description": "Import dans boucle détecté",
                                    "line": node.lineno,
                                    "recommendation": "Déplacer imports en début de fichier"
                                })
                
                except SyntaxError:
                    performance_issues.append({
                        "type": "syntax_error",
                        "description": "Erreur syntaxe empêche analyse performance",
                        "line": None,
                        "recommendation": "Corriger erreurs syntaxe"
                    })
                
            except Exception as e:
                performance_issues.append({
                    "type": "analysis_error",
                    "description": f"Erreur analyse performance: {e}",
                    "line": None,
                    "recommendation": "Vérifier accessibilité fichier"
                })
        
        return {
            "performance_issues": performance_issues,
            "performance_score": max(0, 10 - len(performance_issues) * 1.5)
        }

    async def _analyze_code_quality(self, target: Path) -> Dict[str, Any]:
        """Analyse la qualité du code."""
        quality_issues = []
        
        if target.is_file() and target.suffix == '.py':
            try:
                content = target.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                
                # Analyse ligne par ligne
                for i, line in enumerate(lines):
                    line_num = i + 1
                    
                    # Variables à une lettre (sauf exceptions)
                    if re.search(r'\b[a-z]\s*=', line) and not re.search(r'\b[ijkxy]\s*=', line):
                        quality_issues.append({
                            "type": "single_letter_variable",
                            "description": "Variable à une lettre détectée",
                            "line": line_num,
                            "recommendation": "Utiliser nom descriptif"
                        })
                    
                    # TODO/FIXME non résolus
                    if re.search(r'#\s*(TODO|FIXME|HACK)', line, re.IGNORECASE):
                        quality_issues.append({
                            "type": "todo_comment",
                            "description": "Commentaire TODO/FIXME non résolu",
                            "line": line_num,
                            "recommendation": "Résoudre ou créer issue"
                        })
                    
                    # Magic numbers
                    if re.search(r'\b\d{2,}\b', line) and 'line' not in line.lower():
                        quality_issues.append({
                            "type": "magic_number",
                            "description": "Magic number détecté",
                            "line": line_num,
                            "recommendation": "Utiliser constante nommée"
                        })
                
                # Analyse AST pour qualité
                try:
                    tree = ast.parse(content)
                    
                    # Fonctions sans docstring
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if not node.name.startswith('_') and not ast.get_docstring(node):
                                quality_issues.append({
                                    "type": "missing_docstring",
                                    "description": f"Fonction {node.name} sans docstring",
                                    "line": node.lineno,
                                    "recommendation": "Ajouter docstring descriptive"
                                })
                    
                    # Classes sans docstring
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            if not ast.get_docstring(node):
                                quality_issues.append({
                                    "type": "missing_class_docstring",
                                    "description": f"Classe {node.name} sans docstring",
                                    "line": node.lineno,
                                    "recommendation": "Ajouter docstring de classe"
                                })
                
                except SyntaxError:
                    quality_issues.append({
                        "type": "syntax_error",
                        "description": "Erreur syntaxe empêche analyse qualité",
                        "line": None,
                        "recommendation": "Corriger erreurs syntaxe"
                    })
                
            except Exception as e:
                quality_issues.append({
                    "type": "analysis_error",
                    "description": f"Erreur analyse qualité: {e}",
                    "line": None,
                    "recommendation": "Vérifier accessibilité fichier"
                })
        
        return {
            "quality_issues": quality_issues,
            "quality_score": max(0, 10 - len(quality_issues) * 0.5)
        }

    async def _analyze_design_patterns(self, target: Path) -> Dict[str, Any]:
        """Analyse les design patterns utilisés."""
        patterns_found = {}
        
        if target.is_file() and target.suffix == '.py':
            try:
                content = target.read_text(encoding='utf-8', errors='ignore')
                
                for pattern_name, pattern_regex in self.design_patterns.items():
                    matches = re.findall(pattern_regex, content)
                    if matches:
                        patterns_found[pattern_name] = {
                            "detected": True,
                            "instances": len(matches),
                            "examples": matches[:3]  # Premier 3 exemples
                        }
                    else:
                        patterns_found[pattern_name] = {
                            "detected": False,
                            "instances": 0,
                            "examples": []
                        }
                
            except Exception as e:
                patterns_found["analysis_error"] = f"Erreur analyse patterns: {e}"
        
        return {
            "design_patterns": patterns_found,
            "patterns_score": len([p for p in patterns_found.values() if isinstance(p, dict) and p.get("detected")])
        }

    async def _analyze_code_complexity(self, target: Path) -> Dict[str, Any]:
        """Analyse la complexité du code."""
        complexity_metrics = {
            "functions": [],
            "classes": [],
            "overall_complexity": 0
        }
        
        if target.is_file() and target.suffix == '.py':
            try:
                content = target.read_text(encoding='utf-8', errors='ignore')
                
                try:
                    tree = ast.parse(content)
                    
                    # Analyse fonctions
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            complexity = self._calculate_cyclomatic_complexity(node)
                            complexity_metrics["functions"].append({
                                "name": node.name,
                                "line": node.lineno,
                                "complexity": complexity,
                                "parameters": len(node.args.args),
                                "is_complex": complexity > self.critical_metrics['cyclomatic_complexity']
                            })
                    
                    # Analyse classes
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                            class_complexity = sum(self._calculate_cyclomatic_complexity(m) for m in methods)
                            complexity_metrics["classes"].append({
                                "name": node.name,
                                "line": node.lineno,
                                "methods_count": len(methods),
                                "total_complexity": class_complexity,
                                "average_complexity": class_complexity / max(1, len(methods))
                            })
                    
                    # Complexité globale
                    total_complexity = sum(f["complexity"] for f in complexity_metrics["functions"])
                    complexity_metrics["overall_complexity"] = total_complexity
                
                except SyntaxError:
                    complexity_metrics["error"] = "Erreur syntaxe empêche analyse complexité"
                
            except Exception as e:
                complexity_metrics["error"] = f"Erreur analyse complexité: {e}"
        
        return complexity_metrics

    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """Calcule la complexité cyclomatique d'un nœud AST."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.Try):
                complexity += len(child.handlers)
            elif isinstance(child, (ast.BoolOp, ast.Compare)):
                complexity += 1
        
        return complexity

    async def review_technique_complete(self, target_path: str) -> Dict[str, Any]:
        """Review technique complète d'un projet ou fichier."""
        self.logger.info(f"👨‍💻 Review technique complète: {target_path}")
        
        target = Path(target_path)
        self.findings = []
        
        # Review selon le type de cible
        if target.is_file():
            await self._review_file_technique(str(target))
        elif target.is_dir():
            await self._review_project_technique(target)
        
        # Compilation du rapport
        rapport = {
            'review_id': f"TECH_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'target': target_path,
            'timestamp': datetime.now().isoformat(),
            'findings': [self._serialize_finding(finding) for finding in self.findings],
            'technical_score': self._calculate_technical_score(),
            'architecture_analysis': await self._analyze_architecture_patterns(target),
            'security_analysis': await self._analyze_security_patterns(target),
            'performance_analysis': await self._analyze_performance_patterns(target),
            'recommendations': self._generate_technical_recommendations(),
            'summary': self._generate_summary()
        }
        
        await self._save_review_report(rapport)
        return rapport

    async def _review_project_technique(self, project_path: Path):
        """Review technique d'un projet complet."""
        
        # Review tous les fichiers Python
        for py_file in project_path.rglob('*.py'):
            if not self._should_skip_file(py_file):
                await self._review_file_technique(str(py_file))

    async def _review_file_technique(self, file_path: str):
        """Review technique d'un fichier."""
        try:
            content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
            
            if file_path.endswith('.py'):
                await self._review_python_file(content, file_path)
            
        except Exception as e:
            self.logger.error(f"Erreur review technique {file_path}: {e}")

    async def _review_python_file(self, content: str, file_path: str):
        """Review technique spécialisée Python."""
        lines = content.split('\n')
        
        # Review ligne par ligne
        for i, line in enumerate(lines):
            line_num = i + 1
            
            # Détection code complexe
            if len(line) > 120:
                self.findings.append(ReviewFinding(
                    finding_id=f"TECH_{uuid.uuid4().hex[:8]}",
                    category=ReviewCategory.MAINTAINABILITY,
                    severity=ReviewSeverity.LOW,
                    title="Ligne trop longue",
                    description=f"Ligne {line_num}: {len(line)} caractères (> 120)",
                    location=file_path,
                    line_number=line_num,
                    recommendation="Diviser la ligne ou refactoriser",
                    code_snippet=line.strip(),
                    impact="Lisibilité réduite"
                ))

    def _should_skip_file(self, file_path: Path) -> bool:
        """Détermine si un fichier doit être ignoré."""
        skip_patterns = [
            '__pycache__', '.git', '.pytest_cache', 
            'node_modules', '.venv', 'venv', 'build', 'dist'
        ]
        
        return any(pattern in str(file_path) for pattern in skip_patterns)

    def _calculate_technical_score(self) -> float:
        """Calcule le score technique global (0-10)."""
        if not self.findings:
            return 10.0
        
        # Pondération par sévérité
        weights = {
            ReviewSeverity.CRITICAL: 3.0,
            ReviewSeverity.HIGH: 2.0,
            ReviewSeverity.MEDIUM: 1.0,
            ReviewSeverity.LOW: 0.5,
            ReviewSeverity.INFO: 0.1
        }
        
        total_penalty = sum(weights.get(finding.severity, 1.0) for finding in self.findings)
        score = max(0.0, 10.0 - (total_penalty * 0.3))
        
        return round(score, 2)

    def _group_findings_by_severity(self) -> Dict[str, int]:
        """Groupe les findings par sévérité."""
        return {
            "critical": len([f for f in self.findings if f.severity == ReviewSeverity.CRITICAL]),
            "high": len([f for f in self.findings if f.severity == ReviewSeverity.HIGH]),
            "medium": len([f for f in self.findings if f.severity == ReviewSeverity.MEDIUM]),
            "low": len([f for f in self.findings if f.severity == ReviewSeverity.LOW]),
            "info": len([f for f in self.findings if f.severity == ReviewSeverity.INFO])
        }

    def _group_findings_by_category(self) -> Dict[str, int]:
        """Groupe les findings par catégorie."""
        categories = {}
        for category in ReviewCategory:
            categories[category.value] = len([f for f in self.findings if f.category == category])
        return categories

    def _generate_technical_recommendations(self) -> List[str]:
        """Génère des recommandations techniques."""
        recommendations = []
        
        critical_findings = [f for f in self.findings if f.severity == ReviewSeverity.CRITICAL]
        high_findings = [f for f in self.findings if f.severity == ReviewSeverity.HIGH]
        
        if critical_findings:
            recommendations.append("CRITIQUE: Résoudre immédiatement les findings critiques de review.")
        
        if high_findings:
            recommendations.append("IMPORTANT: Traiter les findings haute priorité.")
        
        # Recommandations par catégorie
        security_findings = [f for f in self.findings if f.category == ReviewCategory.SECURITY]
        if security_findings:
            recommendations.append("Renforcer la sécurité selon les findings détectés.")
        
        performance_findings = [f for f in self.findings if f.category == ReviewCategory.PERFORMANCE]
        if performance_findings:
            recommendations.append("Optimiser les performances selon l'analyse.")
        
        return recommendations

    def _generate_summary(self) -> Dict[str, int]:
        """Génère un résumé des findings."""
        summary = {severity.value: 0 for severity in ReviewSeverity}
        
        for finding in self.findings:
            summary[finding.severity.value] += 1
        
        summary['total'] = len(self.findings)
        return summary

    def _serialize_finding(self, finding: ReviewFinding) -> Dict[str, Any]:
        """Sérialise un finding en dictionnaire."""
        return {
            "finding_id": finding.finding_id,
            "category": finding.category.value,
            "severity": finding.severity.value,
            "title": finding.title,
            "description": finding.description,
            "location": finding.location,
            "line_number": finding.line_number,
            "recommendation": finding.recommendation,
            "code_snippet": finding.code_snippet,
            "impact": finding.impact
        }

    async def _save_review_report(self, rapport: Dict[str, Any]):
        """Sauvegarde le rapport de review."""
        try:
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            # Nom de fichier avec timestamp
            filename = f"agent_17_technical_review_{rapport['review_id']}.json"
            report_path = reports_dir / filename
            
            # Sauvegarde JSON
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"📄 Rapport de review technique sauvegardé: {report_path}")
            
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde rapport review: {e}")

    async def startup(self) -> bool:
        """Démarrage de l'agent (Pattern Factory)."""
        try:
            self.logger.info(f"🚀 Démarrage Agent {self.agent_id} - Peer Reviewer Technique")
            # Initialisation des ressources si nécessaire
            return True
        except Exception as e:
            self.logger.error(f"Erreur démarrage Agent {self.agent_id}: {e}")
            return False

    async def shutdown(self) -> bool:
        """Arrêt de l'agent (Pattern Factory)."""
        try:
            self.logger.info(f"🔌 Arrêt Agent {self.agent_id} - Peer Reviewer Technique")
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
            "review_technique_complete",
            "audit_universel_module",
            "analyse_architecture_patterns",
            "validation_securite_code",
            "analyse_performance_patterns",
            "evaluation_qualite_code",
            "detection_design_patterns",
            "analyse_complexite_cyclomatique",
            "generation_rapports_review",
            "recommandations_techniques",
            "scoring_technique_global"
        ]


# Factory function pour créer l'agent
def create_agent_17_peer_reviewer_technique(**config) -> Agent17PeerReviewerTechnique:
    """Factory function pour créer une instance de l'Agent 17."""
    return Agent17PeerReviewerTechnique(**config)


# Point d'entrée CLI pour tests
if __name__ == "__main__":
    async def test_agent_cli():
        """Test CLI de l'agent."""
        print("🧪 Test Agent 17 - Peer Reviewer Technique")
        
        # Création agent
        agent = create_agent_17_peer_reviewer_technique()
        
        # Test démarrage
        if not await agent.startup():
            print("❌ Échec démarrage agent")
            return
        
        print(f"✅ Agent {agent.agent_id} démarré avec succès")
        print(f"👨‍💻 Spécialité: {agent.specialite}")
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
        print("\n🔍 Test audit universel sur agent_17_peer_reviewer_technique.py...")
        
        current_file = __file__
        audit_task = Task(
            type="audit_module",
            params={"module_path": current_file}
        )
        
        result = await agent.execute_task(audit_task)
        
        if result.success:
            print("✅ Audit universel réussi!")
            report = result.data
            print(f"📊 Score technique: {report.get('technical_score', 'N/A')}/10")
            print(f"🔍 Findings détectés: {report.get('total_findings', 0)}")
            
            if 'executive_summary' in report:
                summary = report['executive_summary']
                print(f"📈 Pourcentage qualité: {summary.get('review_quality_percentage', 0):.1f}%")
                print(f"⚠️  Findings critiques: {summary.get('critical_findings', 0)}")
            
            print("\n📋 Recommandations:")
            for rec in report.get('recommendations', []):
                print(f"  - {rec}")
        else:
            print(f"❌ Échec audit: {result.error}")
        
        # Test review technique complète
        print("\n👨‍💻 Test review technique du fichier actuel...")
        
        review_task = Task(
            type="technical_review",
            params={"target_path": current_file}
        )
        
        result = await agent.execute_task(review_task)
        
        if result.success:
            print("✅ Review technique réussie!")
            report = result.data
            print(f"📊 Score technique: {report.get('technical_score', 'N/A')}/10")
            print(f"🔍 Findings détectés: {report.get('summary', {}).get('total', 0)}")
        else:
            print(f"❌ Échec review technique: {result.error}")
        
        # Test arrêt
        if await agent.shutdown():
            print("✅ Agent arrêté proprement")
        else:
            print("⚠️  Problème lors de l'arrêt")
    
    # Exécution du test
    asyncio.run(test_agent_cli())
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

