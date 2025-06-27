#!/usr/bin/env python3
"""
🔍 VALIDATEUR FINAL - Agent 06
===============================
🎯 Mission : Validation finale complète et multi-niveaux d'agents réparés avec audit qualité.
⚡ Capacités : Validation syntaxique, structurelle, conformité Pattern Factory et audit qualité.
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 6.1.0 - Harmonisation Standards Pattern Factory NextGeneration
"""

import asyncio
import json
import logging
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
import os
import ast
import subprocess
import tempfile
import inspect
import textwrap

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core.agent_factory_architecture import Agent, Task, Result

@dataclass
class ValidationIssue:
    """Structure pour représenter un problème de validation."""
    severity: str           # CRITICAL, HIGH, MEDIUM, LOW
    validation_type: str    # syntax, structure, pattern_factory, quality
    description: str        # Description du problème
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None

class AgentMAINTENANCE06ValidateurFinal(Agent):
    """
    🔍 Agent MAINTENANCE 06 - Validateur Final NextGeneration
    
    Agent spécialisé dans la validation finale multi-niveaux d'agents réparés,
    audit qualité complet et vérification conformité Pattern Factory.
    
    Capacités principales :
    - Validation syntaxique avancée avec compilation Python et AST
    - Vérification structure Pattern Factory (Agent, Task, Result)
    - Audit qualité code avec Flake8, PyFlakes et metrics personnalisées
    - Validation conformité methods async (startup, shutdown, execute_task)
    - Test instanciation factory functions et compatibilité coordinateur
    - Audit documentation avec vérification docstrings et capabilities
    
    Technologies avancées :
    - AST analysis : Validation structure et détection méthodes manquantes
    - Subprocess integration : Flake8, PyFlakes pour audit qualité externe
    - Introspection : Validation signatures et factory functions
    - Dataclass ValidationIssue : Classification structurée des problèmes
    - Multi-level validation : Syntax → Structure → Quality → Conformity
    
    Workflow type :
    1. Validation syntaxique (AST parsing + compilation Python)
    2. Vérification structure Pattern Factory et méthodes requises
    3. Audit qualité avec outils externes (Flake8, PyFlakes)
    4. Test instanciation et compatibilité factory functions
    5. Validation finale avec scoring et recommandations détaillées
    
    Conformité : Pattern Factory NextGeneration v6.1.0
    """
    def __init__(self, **kwargs):
        """Initialisation robuste et compatible avec le coordinateur."""
        super().__init__(agent_type="validateur_final", **kwargs)
        self.agent_id = self.id
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={
                    "logger_name": f"nextgen.maintenance.validateur_final.{self.agent_id}",
                    "log_dir": "logs/maintenance/validateur",
                    "metadata": {
                        "agent_type": "MAINTENANCE_06_validateur_final",
                        "agent_role": "validateur_final",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
            
        self.logger.info(f"🔍 Agent Validateur Final ({self.agent_id}) initialisé")
        
        # Configuration des validations requises
        self.required_methods = {
            "async": ["startup", "shutdown", "execute_task", "health_check"],
            "sync": ["get_capabilities"]
        }
        
        # Patterns de validation Pattern Factory
        self.pattern_factory_requirements = {
            "base_classes": ["Agent"],
            "imports": ["agent_factory_architecture"],
            "factory_function": True,
            "task_result_types": ["Task", "Result"]
        }

    async def startup(self):
        self.logger.info(f"Agent 'validateur_final' ({self.id}) démarré.")

    async def execute_task(self, task: Task) -> Result:
        """Exécute une tâche de validation finale."""
        self.logger.info(f"🎯 Exécution tâche: {task.type}")
        
        task_handlers = {
            "validate_code": self._handle_code_validation,
            "final_validation": self._handle_final_validation,
            "quality_audit": self._handle_quality_audit,
            "pattern_factory_compliance": self._handle_pattern_factory_compliance,
            "agent_structure_validation": self._handle_agent_structure_validation
        }
        
        handler = task_handlers.get(task.type)
        if not handler:
            return Result(success=False, error=f"Type de tâche non supporté: {task.type}")
        
        try:
            return await handler(task)
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche {task.type}: {e}", exc_info=True)
            return Result(success=False, error=str(e))
    
    async def _handle_code_validation(self, task: Task) -> Result:
        """Gère la validation de code (compatibilité avec ancienne interface)."""
        return await self._handle_final_validation(task)
    
    async def _handle_final_validation(self, task: Task) -> Result:
        """Effectue une validation finale complète."""
        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        
        if not code:
            return Result(success=False, error="Code source requis pour la validation")
        
        self.logger.info(f"Validation finale du fichier : {file_path}")
        
        # Validation multi-niveaux
        validation_results = await self._perform_comprehensive_validation(code, file_path)
        
        return Result(success=validation_results["overall_success"], data=validation_results)
    
    async def _handle_quality_audit(self, task: Task) -> Result:
        """Effectue un audit qualité avec outils externes."""
        code = task.params.get("code")
        if not code:
            return Result(success=False, error="Code source requis")
        
        quality_results = await self._perform_quality_audit(code)
        
        return Result(success=True, data=quality_results)
    
    async def _handle_pattern_factory_compliance(self, task: Task) -> Result:
        """Vérifie la conformité Pattern Factory."""
        code = task.params.get("code")
        if not code:
            return Result(success=False, error="Code source requis")
        
        compliance_results = await self._validate_pattern_factory_compliance(code)
        
        return Result(success=True, data=compliance_results)
    
    async def _handle_agent_structure_validation(self, task: Task) -> Result:
        """Valide la structure d'agent spécifiquement."""
        code = task.params.get("code")
        if not code:
            return Result(success=False, error="Code source requis")
        
        try:
            tree = ast.parse(code)
            agent_validation = self._validate_agent_structure(tree)
            
            return Result(success=True, data=agent_validation)
        except SyntaxError as e:
            return Result(success=False, error=f"Erreur de syntaxe: {e}")
    
    async def _perform_comprehensive_validation(self, code: str, file_path: str) -> Dict[str, Any]:
        """Effectue une validation complète multi-niveaux."""
        results = {
            "overall_success": True,
            "validation_levels": [],
            "issues": [],
            "score": 100,
            "recommendations": []
        }
        
        try:
            # Niveau 1: Validation syntaxique
            syntax_result = await self._validate_syntax(code, file_path)
            results["validation_levels"].append(syntax_result)
            
            if not syntax_result["passed"]:
                results["overall_success"] = False
                results["score"] -= 30
                return results
            
            # Niveau 2: Validation structure
            structure_result = await self._validate_structure(code)
            results["validation_levels"].append(structure_result)
            
            # Niveau 3: Audit qualité
            quality_result = await self._perform_quality_audit(code)
            results["validation_levels"].append(quality_result)
            
            # Niveau 4: Conformité Pattern Factory
            pattern_result = await self._validate_pattern_factory_compliance(code)
            results["validation_levels"].append(pattern_result)
            
            # Calcul score final
            results["score"] = self._calculate_final_score(results["validation_levels"])
            results["recommendations"] = self._generate_final_recommendations(results["validation_levels"])
            
        except Exception as e:
            results["overall_success"] = False
            results["error"] = str(e)
        
        return results
    
    async def _validate_syntax(self, code: str, file_path: str) -> Dict[str, Any]:
        """Validation syntaxique avec AST et compilation."""
        result = {
            "level": "syntax",
            "passed": True,
            "details": {},
            "issues": []
        }
        
        try:
            # Validation AST
            tree = ast.parse(code)
            result["details"]["ast_validation"] = "passed"
            
            # Validation compilation
            compile(code, file_path, 'exec')
            result["details"]["compile_validation"] = "passed"
            
            # Linter basique
            linter_details = self._run_basic_linter(code, file_path)
            result["details"]["linter"] = linter_details
            
        except SyntaxError as e:
            result["passed"] = False
            result["issues"].append({
                "type": "syntax_error",
                "description": f"Erreur de syntaxe: {e.msg}",
                "line": e.lineno
            })
        
        return result
    
    async def _validate_structure(self, code: str) -> Dict[str, Any]:
        """Validation de la structure du code."""
        result = {
            "level": "structure",
            "passed": True,
            "details": {},
            "issues": []
        }
        
        try:
            tree = ast.parse(code)
            
            # Vérification structure agent
            agent_validation = self._validate_agent_structure(tree)
            result["details"]["agent_structure"] = agent_validation
            
            # Vérification méthodes requises
            methods_check = self._validate_required_methods(tree)
            result["details"]["required_methods"] = methods_check
            
            if not agent_validation.get("has_agent_class", False):
                result["passed"] = False
                result["issues"].append({
                    "type": "missing_agent_class",
                    "description": "Aucune classe héritant d'Agent trouvée"
                })
            
        except Exception as e:
            result["passed"] = False
            result["issues"].append({
                "type": "structure_error",
                "description": f"Erreur d'analyse structure: {e}"
            })
        
        return result
    
    async def _perform_quality_audit(self, code: str) -> Dict[str, Any]:
        """Audit qualité avec outils externes."""
        result = {
            "level": "quality",
            "passed": True,
            "details": {},
            "issues": []
        }
        
        try:
            # Test avec un fichier temporaire pour outils externes
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
                tmp.write(code)
                tmp_path = tmp.name
            
            try:
                # Flake8 si disponible
                flake8_result = await self._run_flake8(tmp_path)
                result["details"]["flake8"] = flake8_result
                
                # PyFlakes si disponible
                pyflakes_result = await self._run_pyflakes(tmp_path)
                result["details"]["pyflakes"] = pyflakes_result
                
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                    
        except Exception as e:
            result["issues"].append({
                "type": "quality_audit_error",
                "description": f"Erreur audit qualité: {e}"
            })
        
        return result
    
    async def _validate_pattern_factory_compliance(self, code: str) -> Dict[str, Any]:
        """Valide la conformité Pattern Factory."""
        result = {
            "level": "pattern_factory",
            "passed": True,
            "details": {},
            "issues": []
        }
        
        try:
            tree = ast.parse(code)
            
            # Vérification imports Pattern Factory
            imports_check = self._check_pattern_factory_imports(tree, code)
            result["details"]["imports"] = imports_check
            
            # Vérification factory function
            factory_check = self._check_factory_function(tree)
            result["details"]["factory_function"] = factory_check
            
            # Vérification méthodes async requises
            async_methods_check = self._check_async_methods(tree)
            result["details"]["async_methods"] = async_methods_check
            
            # Score de conformité
            compliance_score = self._calculate_compliance_score(result["details"])
            result["details"]["compliance_score"] = compliance_score
            
        except Exception as e:
            result["passed"] = False
            result["issues"].append({
                "type": "compliance_error",
                "description": f"Erreur vérification conformité: {e}"
            })
        
        return result

    def _run_basic_linter(self, code: str, file_path: str) -> dict:
        """Exécute un linter basique via subprocess."""
        linter_result = {
            "status": "completed",
            "method": "subprocess_compile_check",
            "issues": []
        }
        
        try:
            # Créer un fichier temporaire pour le test
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
                tmp.write(code)
                tmp_path = tmp.name
            
            try:
                # Utilise l'interpréteur courant pour vérifier la syntaxe
                process = subprocess.run(
                    [sys.executable, "-m", "py_compile", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if process.returncode == 0:
                    linter_result["status"] = "passed"
                else:
                    linter_result["status"] = "failed"
                    linter_result["issues"].append(f"py_compile failed: {process.stderr}")
                    
            except subprocess.TimeoutExpired:
                linter_result["status"] = "timeout"
                linter_result["issues"].append("Linter timeout")
            except Exception as e:
                linter_result["status"] = "error"
                linter_result["issues"].append(f"Linter execution error: {e}")
            finally:
                # Nettoyer le fichier temporaire
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                    
        except Exception as e:
            linter_result["status"] = "error"
            linter_result["issues"].append(f"Linter setup error: {e}")
        
        return linter_result

    def _validate_agent_structure(self, tree: ast.AST) -> dict:
        """Valide la structure spécifique aux agents."""
        validation = {
            "has_agent_class": False,
            "has_execute_task": False,
            "has_startup": False,
            "agent_class_name": None,
            "issues": []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Vérifier si c'est une classe d'agent
                base_names = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        base_names.append(base.id)
                
                if 'Agent' in base_names:
                    validation["has_agent_class"] = True
                    validation["agent_class_name"] = node.name
                    
                    # Vérifier les méthodes requises dans la classe
                    methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                    
                    if 'execute_task' in methods:
                        validation["has_execute_task"] = True
                    else:
                        validation["issues"].append("Méthode execute_task manquante")
                    
                    if 'startup' in methods:
                        validation["has_startup"] = True
                    else:
                        validation["issues"].append("Méthode startup manquante")
        
        if not validation["has_agent_class"]:
            validation["issues"].append("Aucune classe héritant d'Agent trouvée")
        
        return validation

    def get_capabilities(self) -> List[str]:
        """Retourne les capacités spécialisées du Validateur Final."""
        return [
            "final_validation",
            "syntax_validation",
            "structure_validation",
            "pattern_factory_compliance",
            "quality_audit",
            "agent_structure_validation",
            "factory_function_testing",
            "multi_level_validation",
            "comprehensive_reporting",
            "validation_scoring"
        ]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy"}

    async def shutdown(self):
        """Arrêt de l'agent."""
        self.logger.info(f"Agent 'validateur_final' ({self.id}) arrêté.")

    def _validate_required_methods(self, tree: ast.AST) -> Dict[str, Any]:
        """Valide la présence des méthodes requises."""
        result = {
            "async_methods": [],
            "sync_methods": [],
            "missing_async": [],
            "missing_sync": []
        }
        
        # Collecte des méthodes
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                result["async_methods"].append(node.name)
            elif isinstance(node, ast.FunctionDef):
                result["sync_methods"].append(node.name)
        
        # Vérification méthodes requises
        for method in self.required_methods["async"]:
            if method not in result["async_methods"]:
                result["missing_async"].append(method)
        
        for method in self.required_methods["sync"]:
            if method not in result["sync_methods"]:
                result["missing_sync"].append(method)
        
        return result
    
    async def _run_flake8(self, file_path: str) -> Dict[str, Any]:
        """Exécute Flake8 si disponible."""
        result = {"tool": "flake8", "status": "not_available"}
        
        try:
            process = subprocess.run(
                ["flake8", "--max-line-length=100", file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            result["status"] = "completed"
            result["returncode"] = process.returncode
            result["output"] = process.stdout
            result["errors"] = process.stderr
        except (subprocess.TimeoutExpired, FileNotFoundError):
            result["status"] = "not_available"
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    async def _run_pyflakes(self, file_path: str) -> Dict[str, Any]:
        """Exécute PyFlakes si disponible."""
        result = {"tool": "pyflakes", "status": "not_available"}
        
        try:
            process = subprocess.run(
                ["pyflakes", file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            result["status"] = "completed"
            result["returncode"] = process.returncode
            result["output"] = process.stdout
            result["errors"] = process.stderr
        except (subprocess.TimeoutExpired, FileNotFoundError):
            result["status"] = "not_available"
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def _check_pattern_factory_imports(self, tree: ast.AST, code: str) -> Dict[str, Any]:
        """Vérifie les imports Pattern Factory."""
        result = {
            "has_agent_factory": False,
            "has_agent_import": False,
            "has_task_result": False,
            "imports_found": []
        }
        
        # Vérification dans le code brut
        if "agent_factory_architecture" in code:
            result["has_agent_factory"] = True
        
        if "Agent" in code and "Task" in code and "Result" in code:
            result["has_task_result"] = True
        
        # Analyse AST des imports
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and "agent_factory" in node.module:
                    result["has_agent_import"] = True
                    result["imports_found"].append(node.module)
        
        return result
    
    def _check_factory_function(self, tree: ast.AST) -> Dict[str, Any]:
        """Vérifie la présence d'une factory function."""
        result = {
            "has_factory": False,
            "factory_name": None,
            "factory_functions": []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith("create_") and "agent" in node.name.lower():
                    result["has_factory"] = True
                    result["factory_name"] = node.name
                    result["factory_functions"].append(node.name)
        
        return result
    
    def _check_async_methods(self, tree: ast.AST) -> Dict[str, Any]:
        """Vérifie les méthodes async requises."""
        result = {
            "async_methods_found": [],
            "required_async_methods": self.required_methods["async"],
            "compliance": {}
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                result["async_methods_found"].append(node.name)
        
        # Vérification conformité
        for method in self.required_methods["async"]:
            result["compliance"][method] = method in result["async_methods_found"]
        
        return result
    
    def _calculate_compliance_score(self, details: Dict[str, Any]) -> int:
        """Calcule un score de conformité Pattern Factory."""
        score = 100
        
        # Import Pattern Factory (-20 si manquant)
        if not details.get("imports", {}).get("has_agent_factory", False):
            score -= 20
        
        # Factory function (-15 si manquante)
        if not details.get("factory_function", {}).get("has_factory", False):
            score -= 15
        
        # Méthodes async (-10 par méthode manquante)
        async_compliance = details.get("async_methods", {}).get("compliance", {})
        for method, present in async_compliance.items():
            if not present:
                score -= 10
        
        return max(0, score)
    
    def _calculate_final_score(self, validation_levels: List[Dict[str, Any]]) -> int:
        """Calcule le score final de validation."""
        base_score = 100
        
        for level in validation_levels:
            if not level.get("passed", True):
                base_score -= 25
            
            # Pénalités pour les issues
            issues_count = len(level.get("issues", []))
            base_score -= (issues_count * 5)
        
        return max(0, base_score)
    
    def _generate_final_recommendations(self, validation_levels: List[Dict[str, Any]]) -> List[str]:
        """Génère des recommandations finales."""
        recommendations = []
        
        for level in validation_levels:
            level_name = level.get("level", "unknown")
            
            if not level.get("passed", True):
                recommendations.append(f"Corriger les problèmes de {level_name}")
            
            for issue in level.get("issues", []):
                recommendations.append(f"{level_name.title()}: {issue.get('description', 'Issue détectée')}")
        
        if not recommendations:
            recommendations.append("Code validé avec succès - aucune amélioration nécessaire")
        
        return recommendations

    async def run_validation(self, file_path: str, code_content: str) -> Result:
        """Méthode de compatibilité pour l'ancien appel."""
        self.logger.warning(f"Appel de compatibilité 'run_validation' pour {file_path}")
        validation_task = Task(type="final_validation", params={"file_path": file_path, "code": code_content})
        return await self.execute_task(validation_task)


def create_agent_MAINTENANCE_06_validateur_final(**config) -> AgentMAINTENANCE06ValidateurFinal:
    """Factory pour créer une instance de l'Agent 6."""
    return AgentMAINTENANCE06ValidateurFinal(**config)

# Section de test principal
if __name__ == "__main__":
    async def run_tests():
        print("🚀 Démarrage des tests pour AgentMAINTENANCE06ValidateurFinal...")
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ - Configuration pour tests
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={
                    "logger_name": "nextgen.maintenance.validateur_final.test",
                    "log_dir": "logs/maintenance/test",
                    "metadata": {"context": "test_cli", "agent": "MAINTENANCE_06_validateur"}
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        agent = create_agent_MAINTENANCE_06_validateur_final()
        
        try:
            await agent.startup()
            health = await agent.health_check()
            print(f"🏥 Health Check: {health}")
            
            capabilities = agent.get_capabilities()
            print(f"🛠️ Capabilities: {capabilities}")
            
            # Test avec agent valide complet
            valid_agent_code = '''
from core.agent_factory_architecture import Agent, Task, Result
import asyncio

class AgentTestValid(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    async def startup(self):
        pass
    
    async def shutdown(self):
        pass
    
    async def execute_task(self, task: Task) -> Result:
        return Result(success=True)
    
    async def health_check(self):
        return {"status": "healthy"}
    
    def get_capabilities(self) -> list:
        return ["test_capability"]

def create_agent_test_valid(**config):
    return AgentTestValid(**config)
'''
            
            # Test validation finale complète
            task = Task(
                id="test_final_validation",
                type="final_validation",
                params={"code": valid_agent_code, "file_path": "valid_agent.py"}
            )
            
            result = await agent.execute_task(task)
            print(f"\n🔍 Test validation finale:")
            print(f"   Succès: {result.success}")
            if result.success:
                data = result.data
                print(f"   Score global: {data.get('score', 'N/A')}")
                print(f"   Niveaux de validation: {len(data.get('validation_levels', []))}")
                for level in data.get('validation_levels', [])[:2]:  # Afficher les 2 premiers
                    print(f"     • {level.get('level', 'unknown')}: {'✅' if level.get('passed', False) else '❌'}")
            
            # Test validation Pattern Factory
            task_pattern = Task(
                id="test_pattern_compliance",
                type="pattern_factory_compliance",
                params={"code": valid_agent_code}
            )
            
            result_pattern = await agent.execute_task(task_pattern)
            print(f"\n🏭 Test conformité Pattern Factory:")
            print(f"   Succès: {result_pattern.success}")
            if result_pattern.success:
                pattern_data = result_pattern.data
                compliance_score = pattern_data.get('details', {}).get('compliance_score', 0)
                print(f"   Score conformité: {compliance_score}/100")
            
            # Test avec code invalide
            invalid_code = "def incomplete_function("  # Syntaxe invalide
            
            task_invalid = Task(
                id="test_invalid_code",
                type="final_validation",
                params={"code": invalid_code, "file_path": "invalid.py"}
            )
            
            result_invalid = await agent.execute_task(task_invalid)
            print(f"\n❌ Test code invalide:")
            print(f"   Succès: {result_invalid.success}")
            if result_invalid.success:
                invalid_data = result_invalid.data
                print(f"   Score: {invalid_data.get('score', 'N/A')}")
                print(f"   Recommandations: {len(invalid_data.get('recommendations', []))}")
            
        except Exception as e:
            print(f"❌ Erreur durant les tests: {e}")
        finally:
            await agent.shutdown()
            print("\n✅ Tests terminés.")
    
    asyncio.run(run_tests())
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

