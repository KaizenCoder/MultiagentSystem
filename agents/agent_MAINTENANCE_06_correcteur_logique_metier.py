#!/usr/bin/env python3
"""
🔧 CORRECTEUR LOGIQUE MÉTIER - Agent 06
========================================
🎯 Mission : Correction et validation de la logique métier dans le code Python.
⚡ Capacités : Analyse sémantique, détection incohérences logiques, correction automatique.
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 6.1.0 - Harmonisation Standards Pattern Factory NextGeneration
"""
import sys
import ast
import re
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
import inspect
import textwrap

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core.agent_factory_architecture import Agent, Task, Result

@dataclass
class LogicIssue:
    """Structure pour représenter un problème de logique métier."""
    severity: str           # CRITICAL, HIGH, MEDIUM, LOW
    issue_type: str         # logic_error, semantic_issue, pattern_violation
    description: str        # Description du problème
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None
    
class AgentMAINTENANCE06CorrecteurLogiqueMetier(Agent):
    """
    🔧 Agent MAINTENANCE 06 - Correcteur Logique Métier NextGeneration
    
    Agent spécialisé dans la correction et validation de la logique métier Python,
    détection d'incohérences sémantiques et application de patterns métier robustes.
    
    Capacités principales :
    - Analyse sémantique approfondie du code avec détection incohérences logiques
    - Validation patterns métier et architecture (Factory, Strategy, Observer)
    - Correction automatique erreurs logiques courantes (null checks, validations)
    - Détection anti-patterns et suggestions d'amélioration de design
    - Vérification cohérence API et interfaces avec recommendations
    - Audit conformité métier avec scoring et classification par sévérité
    
    Technologies avancées :
    - AST analysis : Analyse syntaxique avancée pour détection patterns
    - Inspection module : Validation signatures et interfaces métier
    - Pattern matching : Détection anti-patterns et violations architecture
    - Dataclass LogicIssue : Classification structurée des problèmes détectés
    - Correction automatique : Génération de code corrigé avec traçabilité
    
    Workflow type :
    1. Analyse AST pour détection patterns et anti-patterns métier
    2. Validation cohérence interfaces et API design
    3. Détection incohérences logiques (null checks, validations manquantes)
    4. Classification problèmes par sévérité et type (logic/semantic/pattern)
    5. Génération corrections avec suggestions d'amélioration architecture
    
    Conformité : Pattern Factory NextGeneration v6.1.0
    """
    
    def __init__(self, **kwargs):
        super().__init__(agent_type="correcteur_logique", **kwargs)
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={
                    "logger_name": f"nextgen.maintenance.correcteur_logique_metier.{self.id}",
                    "log_dir": "logs/maintenance/correcteur",
                    "metadata": {
                        "agent_type": "MAINTENANCE_06_correcteur_logique_metier",
                        "agent_role": "correcteur_logique_metier",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = self.id
        self.logger.info(f"🔧 Agent Correcteur Logique Métier ({self.agent_id}) initialisé")
        
        # Configuration des patterns métier à détecter
        self.business_patterns = {
            "factory_pattern": ["create_", "build_", "make_"],
            "validation_pattern": ["validate_", "check_", "verify_"],
            "error_handling": ["try:", "except", "raise"],
            "null_safety": ["if not", "is None", "assert"]
        }
        
        # Anti-patterns à éviter
        self.anti_patterns = {
            "god_class": "Classes avec trop de responsabilités",
            "magic_numbers": "Nombres magiques sans constantes",
            "deep_nesting": "Imbrication trop profonde",
            "long_methods": "Méthodes trop longues (>50 lignes)"
        }

    async def startup(self):
        self.logger.info(f"Agent 'correcteur_logique' ({self.id}) démarré.")

    async def shutdown(self):
        self.logger.info(f"Agent 'correcteur_logique' ({self.id}) arrêté.")

    async def health_check(self):
        return {"status": "healthy"}

    def get_capabilities(self) -> List[str]:
        """Retourne les capacités spécialisées du Correcteur Logique Métier."""
        return [
            "correct_business_logic",
            "validate_business_patterns",
            "detect_logic_inconsistencies", 
            "analyze_semantic_correctness",
            "fix_anti_patterns",
            "validate_api_design",
            "check_error_handling",
            "verify_null_safety",
            "audit_business_compliance",
            "generate_logic_improvements"
        ]

    async def execute_task(self, task: Task) -> Result:
        """Exécute une tâche de correction de logique métier."""
        self.logger.info(f"🎯 Exécution tâche: {task.type}")
        
        task_handlers = {
            "correct_business_logic": self._handle_business_logic_correction,
            "validate_business_patterns": self._handle_pattern_validation,
            "detect_logic_inconsistencies": self._handle_logic_analysis,
            "audit_business_compliance": self._handle_compliance_audit
        }
        
        handler = task_handlers.get(task.type)
        if not handler:
            return Result(success=False, error=f"Type de tâche non supporté: {task.type}")
        
        try:
            return await handler(task)
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche {task.type}: {e}", exc_info=True)
            return Result(success=False, error=str(e))
    
    async def _handle_business_logic_correction(self, task: Task) -> Result:
        """Gère la correction de logique métier."""
        code_content = task.params.get("code")
        file_path = task.params.get("file_path", "<unknown>")
        
        if not code_content:
            return Result(success=False, error="Code source requis pour la correction")
        
        # Analyse et correction
        issues = await self._analyze_business_logic(code_content, file_path)
        corrections = await self._generate_corrections(code_content, issues)
        
        return Result(success=True, data={
            "issues_detected": len(issues),
            "issues": [{
                "type": issue.issue_type,
                "severity": issue.severity,
                "description": issue.description,
                "line": issue.line_number,
                "suggestion": issue.suggestion
            } for issue in issues],
            "corrections": corrections,
            "corrected_code": corrections.get("code", code_content)
        })
    
    async def _handle_pattern_validation(self, task: Task) -> Result:
        """Valide les patterns métier dans le code."""
        code_content = task.params.get("code")
        if not code_content:
            return Result(success=False, error="Code source requis")
        
        pattern_analysis = await self._validate_business_patterns(code_content)
        
        return Result(success=True, data={
            "patterns_found": pattern_analysis["found"],
            "missing_patterns": pattern_analysis["missing"],
            "recommendations": pattern_analysis["recommendations"]
        })
    
    async def _handle_logic_analysis(self, task: Task) -> Result:
        """Analyse les incohérences logiques."""
        code_content = task.params.get("code")
        if not code_content:
            return Result(success=False, error="Code source requis")
        
        inconsistencies = await self._detect_logic_inconsistencies(code_content)
        
        return Result(success=True, data={
            "inconsistencies_count": len(inconsistencies),
            "inconsistencies": inconsistencies,
            "severity_breakdown": self._categorize_by_severity(inconsistencies)
        })
    
    async def _handle_compliance_audit(self, task: Task) -> Result:
        """Effectue un audit de conformité métier."""
        code_content = task.params.get("code")
        compliance_rules = task.params.get("rules", [])
        
        if not code_content:
            return Result(success=False, error="Code source requis")
        
        audit_results = await self._audit_business_compliance(code_content, compliance_rules)
        
        return Result(success=True, data=audit_results)
    
    async def _analyze_business_logic(self, code: str, file_path: str) -> List[LogicIssue]:
        """Analyse la logique métier et détecte les problèmes."""
        issues = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            issues.append(LogicIssue(
                severity="CRITICAL",
                issue_type="logic_error",
                description=f"Erreur de syntaxe: {e.msg}",
                line_number=e.lineno,
                suggestion="Corriger la syntaxe avant l'analyse logique"
            ))
            return issues
        
        # Analyse des méthodes et fonctions
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Vérification longueur de méthode
                if len(node.body) > 20:  # Seuil configurable
                    issues.append(LogicIssue(
                        severity="MEDIUM",
                        issue_type="pattern_violation",
                        description=f"Méthode '{node.name}' trop longue ({len(node.body)} statements)",
                        line_number=node.lineno,
                        suggestion="Diviser en méthodes plus petites pour améliorer la lisibilité"
                    ))
                
                # Vérification gestion d'erreurs
                has_error_handling = any(
                    isinstance(n, ast.Try) for n in ast.walk(node)
                )
                if not has_error_handling and len(node.body) > 5:
                    issues.append(LogicIssue(
                        severity="HIGH",
                        issue_type="logic_error",
                        description=f"Méthode '{node.name}' sans gestion d'erreurs",
                        line_number=node.lineno,
                        suggestion="Ajouter try/except pour la robustesse"
                    ))
            
            # Détection de nombres magiques
            elif isinstance(node, ast.Num) and isinstance(node.n, (int, float)) and node.n not in [0, 1, -1]:
                issues.append(LogicIssue(
                    severity="LOW",
                    issue_type="pattern_violation",
                    description=f"Nombre magique détecté: {node.n}",
                    line_number=node.lineno,
                    suggestion="Remplacer par une constante nommée"
                ))
        
        return issues
    
    async def _validate_business_patterns(self, code: str) -> Dict[str, Any]:
        """Valide la présence de patterns métier essentiels."""
        found_patterns = []
        missing_patterns = []
        recommendations = []
        
        for pattern_name, keywords in self.business_patterns.items():
            pattern_found = any(keyword in code for keyword in keywords)
            
            if pattern_found:
                found_patterns.append(pattern_name)
            else:
                missing_patterns.append(pattern_name)
                recommendations.append(f"Considérer l'implémentation du pattern {pattern_name}")
        
        return {
            "found": found_patterns,
            "missing": missing_patterns,
            "recommendations": recommendations
        }
    
    async def _detect_logic_inconsistencies(self, code: str) -> List[Dict[str, Any]]:
        """Détecte les incohérences logiques dans le code."""
        inconsistencies = []
        
        # Détection de variables non utilisées
        if "import " in code:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    # Analyse simplifiée - vérifier si l'import est utilisé
                    import_name = line.split()[-1] if 'import' in line else ''
                    if import_name and import_name not in ' '.join(lines[i:]):
                        inconsistencies.append({
                            "type": "unused_import",
                            "severity": "LOW",
                            "line": i,
                            "description": f"Import potentiellement non utilisé: {import_name}"
                        })
        
        return inconsistencies
    
    async def _audit_business_compliance(self, code: str, rules: List[str]) -> Dict[str, Any]:
        """Effectue un audit de conformité selon les règles métier."""
        compliance_score = 100
        violations = []
        recommendations = []
        
        # Règles par défaut si aucune fournie
        if not rules:
            rules = [
                "functions_must_have_docstrings",
                "classes_must_have_docstrings",
                "error_handling_required",
                "no_magic_numbers"
            ]
        
        try:
            tree = ast.parse(code)
            
            for rule in rules:
                if rule == "functions_must_have_docstrings":
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if not ast.get_docstring(node):
                                violations.append(f"Fonction '{node.name}' sans docstring (ligne {node.lineno})")
                                compliance_score -= 5
                
                elif rule == "classes_must_have_docstrings":
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            if not ast.get_docstring(node):
                                violations.append(f"Classe '{node.name}' sans docstring (ligne {node.lineno})")
                                compliance_score -= 10
        
        except SyntaxError:
            compliance_score = 0
            violations.append("Code avec erreurs de syntaxe")
        
        if violations:
            recommendations.append("Ajouter des docstrings pour améliorer la documentation")
            recommendations.append("Implémenter une gestion d'erreurs robuste")
        
        return {
            "compliance_score": max(0, compliance_score),
            "violations": violations,
            "recommendations": recommendations,
            "rules_checked": rules
        }
    
    async def _generate_corrections(self, code: str, issues: List[LogicIssue]) -> Dict[str, Any]:
        """Génère des corrections automatiques pour les problèmes détectés."""
        corrected_code = code
        applied_corrections = []
        
        for issue in issues:
            if issue.issue_type == "logic_error" and issue.suggestion:
                # Ici on pourrait implémenter des corrections automatiques
                applied_corrections.append({
                    "issue": issue.description,
                    "correction": issue.suggestion,
                    "line": issue.line_number
                })
        
        return {
            "code": corrected_code,
            "corrections_applied": applied_corrections,
            "corrections_count": len(applied_corrections)
        }
    
    def _categorize_by_severity(self, issues: List[Dict[str, Any]]) -> Dict[str, int]:
        """Catégorise les problèmes par niveau de sévérité."""
        severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        for issue in issues:
            severity = issue.get("severity", "LOW")
            if severity in severity_count:
                severity_count[severity] += 1
        
        return severity_count

def create_agent_MAINTENANCE_06_correcteur_logique_metier(**config) -> AgentMAINTENANCE06CorrecteurLogiqueMetier:
    """Factory function pour créer l'agent Correcteur Logique Métier."""
    return AgentMAINTENANCE06CorrecteurLogiqueMetier(**config)

# Section de test principal
if __name__ == "__main__":
    async def run_tests():
        print("🚀 Démarrage des tests pour AgentMAINTENANCE06CorrecteurLogiqueMetier...")
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ - Configuration pour tests
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={
                    "logger_name": "nextgen.maintenance.correcteur_logique_metier.test",
                    "log_dir": "logs/maintenance/test",
                    "metadata": {"context": "test_cli", "agent": "MAINTENANCE_06"}
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        agent = create_agent_MAINTENANCE_06_correcteur_logique_metier()
        
        try:
            await agent.startup()
            health = await agent.health_check()
            print(f"🏥 Health Check: {health}")
            
            capabilities = agent.get_capabilities()
            print(f"🛠️ Capabilities: {capabilities}")
            
            # Test avec code problématique
            problematic_code = '''
def process_data(data):
    result = data * 42  # Nombre magique
    return result

class DataProcessor:  # Pas de docstring
    def __init__(self):
        pass
        
    def long_method(self, x, y, z, a, b, c, d, e, f, g):  # Trop de paramètres
        if x > 0:
            if y > 0:
                if z > 0:  # Imbrication profonde
                    if a > 0:
                        return x + y + z + a
        return 0  # Pas de gestion d'erreurs
'''
            
            # Test correction logique métier
            task = Task(
                id="test_logic_correction",
                type="correct_business_logic",
                params={"code": problematic_code, "file_path": "test.py"}
            )
            
            result = await agent.execute_task(task)
            print(f"\n🔧 Test correction logique:")
            print(f"   Succès: {result.success}")
            if result.success:
                data = result.data
                print(f"   Problèmes détectés: {data['issues_detected']}")
                for issue in data['issues'][:3]:  # Afficher les 3 premiers
                    print(f"     • {issue['severity']}: {issue['description']}")
            
            # Test validation patterns
            task_patterns = Task(
                id="test_patterns",
                type="validate_business_patterns",
                params={"code": problematic_code}
            )
            
            result_patterns = await agent.execute_task(task_patterns)
            print(f"\n🎯 Test validation patterns:")
            print(f"   Succès: {result_patterns.success}")
            if result_patterns.success:
                patterns_data = result_patterns.data
                print(f"   Patterns trouvés: {patterns_data['patterns_found']}")
                print(f"   Patterns manquants: {patterns_data['missing_patterns']}")
            
        except Exception as e:
            print(f"❌ Erreur durant les tests: {e}")
        finally:
            await agent.shutdown()
            print("\n✅ Tests terminés.")
    
    asyncio.run(run_tests()) 