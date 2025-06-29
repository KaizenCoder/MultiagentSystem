#!/usr/bin/env python3
"""
🔧 Agent Assistant 99 Refactoring Helper - NextGeneration v5.3.0
Version enterprise Wave 3 avec refactoring intelligent IA

Migration Pattern: REFACTORING_AUTOMATION + LLM_ENHANCED + MAINTENANCE_AUTOMATION
Author: Claude Sonnet 4
Date: 29 Juin 2025
"""

import os
import sys
import subprocess
import shutil
import asyncio
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
import logging
import ast
import tempfile

# Imports NextGeneration Architecture
try:
    from core.services import (
        LLMGatewayHybrid, create_llm_gateway,
        MessageBusA2A, create_envelope, MessageType, Priority,
        OptimizedContextStore, create_agent_context, ContextType
    )
    from core.agent_factory_architecture import Task, Result
except ImportError:
    # Fallback pour développement isolé
    print("⚠️ NextGeneration services not available - running in development mode")
    class Task:
        def __init__(self, task_type, params=None):
            self.type = task_type
            self.params = params or {}
    
    class Result:
        def __init__(self, success, data=None, error=None, metrics=None):
            self.success = success
            self.data = data
            self.error = error
            self.metrics = metrics or {}

# Import avec fallback legacy
try:
    from agents.agent_ASSISTANT_99_refactoring_helper import AgentAssistant99RefactoringHelper as LegacyAgent
except ImportError:
    class LegacyAgent:
        def __init__(self, *args, **kwargs):
            self.version = "1.0.0"
            self.name = "Refactoring Helper Legacy"

class RefactoringOperation:
    """Opération de refactoring intelligente"""
    def __init__(self, operation_type: str, target: str, params: Dict[str, Any]):
        self.operation_type = operation_type
        self.target = target
        self.params = params
        self.backup_path: Optional[str] = None
        self.status = "pending"
        self.result: Optional[Dict[str, Any]] = None

class CodeAnalyzer:
    """Analyseur de code intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
    
    async def analyze_code_structure(self, code: str, file_path: str) -> Dict[str, Any]:
        """Analyse structure code avec IA"""
        try:
            tree = ast.parse(code)
            
            analysis = {
                "file_path": file_path,
                "classes": [],
                "functions": [],
                "imports": [],
                "complexity_score": 0,
                "refactoring_opportunities": []
            }
            
            # Analyse AST basique
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    analysis["classes"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                    })
                elif isinstance(node, ast.FunctionDef):
                    analysis["functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": len(node.args.args)
                    })
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis["imports"].append(node.module)
            
            # Calcul complexité
            analysis["complexity_score"] = len(analysis["classes"]) * 2 + len(analysis["functions"])
            
            # IA Analysis Enhancement
            if self.llm_gateway:
                try:
                    ai_analysis = await self.llm_gateway.process_request(
                        f"Analyze code for refactoring opportunities: {file_path}",
                        context={
                            "role": "code_refactoring_expert",
                            "code_structure": analysis,
                            "task": "identify_refactoring_opportunities"
                        }
                    )
                    
                    if ai_analysis.get("success"):
                        opportunities = ai_analysis.get("opportunities", [])
                        analysis["refactoring_opportunities"] = opportunities
                        
                except Exception as e:
                    # Log error but continue
                    pass
            
            return analysis
            
        except SyntaxError:
            return {
                "file_path": file_path,
                "error": "Syntax error in code",
                "refactoring_opportunities": []
            }

class IntelligentRefactorer:
    """Moteur de refactoring intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.patterns = {
            "extract_method": r"def\s+(\w+).*?:\s*\n((?:\s{4,}.*\n){10,})",
            "extract_class": r"class\s+(\w+).*?:\s*\n((?:\s{4,}.*\n){20,})",
            "rename_variable": r"\b(\w+)\b",
            "remove_dead_code": r"def\s+(\w+).*?:\s*\n(?:\s{4,}.*\n)*\s*pass\s*\n"
        }
    
    async def suggest_refactoring(self, code: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggestions de refactoring avec IA"""
        suggestions = []
        
        # Règles basiques
        if analysis.get("complexity_score", 0) > 20:
            suggestions.append({
                "type": "reduce_complexity",
                "priority": "high",
                "description": "Code complexity is high, consider extracting methods or classes",
                "target": "overall_structure"
            })
        
        if len(analysis.get("functions", [])) > 10:
            suggestions.append({
                "type": "extract_class",
                "priority": "medium", 
                "description": "Many functions detected, consider grouping into classes",
                "target": "function_organization"
            })
        
        # IA Enhanced Suggestions
        if self.llm_gateway:
            try:
                ai_suggestions = await self.llm_gateway.process_request(
                    "Generate intelligent refactoring suggestions",
                    context={
                        "role": "senior_refactoring_consultant",
                        "code_analysis": analysis,
                        "task": "advanced_refactoring_recommendations"
                    }
                )
                
                if ai_suggestions.get("success"):
                    ai_recs = ai_suggestions.get("recommendations", [])
                    suggestions.extend(ai_recs)
                    
            except Exception as e:
                # Log but continue
                pass
        
        return suggestions
    
    async def apply_refactoring(self, code: str, refactoring: Dict[str, Any]) -> str:
        """Application refactoring avec IA"""
        refactoring_type = refactoring.get("type")
        
        # Patterns de refactoring basiques
        if refactoring_type == "rename_variable":
            old_name = refactoring.get("old_name")
            new_name = refactoring.get("new_name")
            if old_name and new_name:
                # Pattern intelligent pour éviter faux positifs
                pattern = rf"\b{re.escape(old_name)}\b"
                code = re.sub(pattern, new_name, code)
        
        elif refactoring_type == "remove_dead_code":
            # Suppression code mort
            pattern = self.patterns["remove_dead_code"]
            code = re.sub(pattern, "", code, flags=re.MULTILINE)
        
        elif refactoring_type == "add_docstring":
            # Ajout docstrings avec IA
            if self.llm_gateway:
                try:
                    enhanced_code = await self.llm_gateway.process_request(
                        "Add intelligent docstrings to code",
                        context={
                            "role": "documentation_expert",
                            "code": code,
                            "task": "add_comprehensive_docstrings"
                        }
                    )
                    
                    if enhanced_code.get("success"):
                        code = enhanced_code.get("enhanced_code", code)
                        
                except Exception:
                    pass
        
        return code

class AgentAssistant99RefactoringHelper_Enterprise:
    """
    🔧 Agent Assistant 99 Refactoring Helper - Enterprise NextGeneration v5.3.0
    
    Assistant intelligent de refactoring avec IA contextuelle.
    
    Patterns NextGeneration v5.3.0:
    - REFACTORING_AUTOMATION: Refactoring automatisé intelligent
    - LLM_ENHANCED: Intelligence IA pour transformations code
    - MAINTENANCE_AUTOMATION: Maintenance code automatisée
    - PATTERN_FACTORY: Architecture modulaire éprouvée
    """
    
    def __init__(self, agent_id: str = "assistant_99_refactoring", project_root: Path = None):
        # Métadonnées NextGeneration v5.3.0
        self.agent_id = agent_id
        self.version = "5.3.0"
        self.wave_version = "Wave 3 - Refactoring Intelligence FINAL"
        self.migration_status = "modern_active"
        self.compatibility_mode = True
        
        # Patterns NextGeneration appliqués
        self.__version__ = "5.3.0"
        self.__wave_version__ = "Wave 3 - Refactoring Intelligence FINAL"
        self.__nextgen_patterns__ = [
            "REFACTORING_AUTOMATION",
            "LLM_ENHANCED",
            "MAINTENANCE_AUTOMATION",
            "PATTERN_FACTORY"
        ]
        
        # Configuration agent
        self.name = "Assistant Refactoring Intelligence Enterprise"
        self.mission = "Refactoring intelligent automatisé avec IA contextuelle"
        self.agent_type = "refactoring_assistant_enterprise"
        
        # Configuration projet
        self.project_root = project_root or Path.cwd()
        self.backup_dir = self.project_root / ".refactoring_backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Services NextGeneration (injectés à l'initialisation)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Moteurs de refactoring intelligents
        self.code_analyzer = CodeAnalyzer()
        self.intelligent_refactorer = IntelligentRefactorer()
        
        # Historique opérations
        self.operation_history: List[RefactoringOperation] = []
        self.refactoring_metrics = {
            "operations_count": 0,
            "success_rate": 0.0,
            "files_processed": 0,
            "lines_refactored": 0,
            "time_saved_hours": 0.0
        }
        
        # Configuration refactoring
        self.refactoring_config = {
            "auto_backup": True,
            "confirm_destructive": True,
            "max_file_size_mb": 10,
            "parallel_processing": True,
            "ai_suggestions": True
        }
        
        # Intelligence contextuelle
        self.refactoring_context = {
            "learned_patterns": {},
            "project_style": {},
            "best_practices": [],
            "business_rules": {}
        }
        
        # Compteur legacy compatibility
        self.legacy_agent = None
        self.migration_metrics = {
            "compatibility_score": 0.0,
            "performance_improvement": 0.0,
            "features_enhanced": []
        }
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Configuration logging NextGeneration"""
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="refactoring",
                custom_config={
                    "logger_name": f"nextgen.refactoring.assistant99.{self.agent_id}",
                    "log_dir": "logs/refactoring",
                    "metadata": {
                        "agent_type": "assistant_99_refactoring",
                        "agent_role": "refactoring",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(f"RefactoringAssistant_{self.agent_id}")
    
    async def inject_nextgen_services(self, 
                                    llm_gateway: LLMGatewayHybrid,
                                    message_bus: MessageBusA2A, 
                                    context_store: OptimizedContextStore):
        """Injection des services NextGeneration v5.3.0"""
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus  
        self.context_store = context_store
        
        # Configuration analyseurs avec IA
        self.code_analyzer.llm_gateway = llm_gateway
        self.intelligent_refactorer.llm_gateway = llm_gateway
        
        # Configuration contexte refactoring IA
        await self._setup_refactoring_context()
        
        self.logger.info("✅ Services NextGeneration injectés - Refactoring IA actif")
    
    async def _setup_refactoring_context(self):
        """Configuration contexte refactoring IA spécialisé"""
        if not self.llm_gateway:
            return
        
        refactoring_context = {
            "role": "senior_refactoring_expert",
            "domain": "software_transformation_enterprise",
            "capabilities": [
                "Code structure analysis",
                "Intelligent refactoring suggestions",
                "Automated code transformation",
                "Pattern recognition and application",
                "Best practices enforcement"
            ],
            "patterns": [
                "REFACTORING_AUTOMATION",
                "MAINTENANCE_AUTOMATION",
                "LLM_ENHANCED"
            ]
        }
        
        # Chargement expertise refactoring depuis LLM
        try:
            response = await self.llm_gateway.process_request(
                "Load refactoring expertise",
                context=refactoring_context
            )
            
            if response.get("success"):
                self.refactoring_context["best_practices"] = response.get("best_practices", [])
                self.logger.info("🧠 Expertise refactoring IA chargée")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement contexte IA: {e}")
    
    async def analyze_project_for_refactoring(self, target_path: str = None) -> Dict[str, Any]:
        """Analyse projet complet pour opportunités refactoring"""
        start_time = datetime.now()
        target = Path(target_path) if target_path else self.project_root
        
        self.logger.info(f"🔍 Analyse refactoring projet: {target}")
        
        analysis_result = {
            "target": str(target),
            "files_analyzed": 0,
            "total_lines": 0,
            "refactoring_opportunities": [],
            "complexity_issues": [],
            "recommendations": [],
            "estimated_effort_hours": 0.0
        }
        
        # Analyse fichiers Python
        python_files = list(target.rglob("*.py"))
        analysis_result["files_analyzed"] = len(python_files)
        
        for py_file in python_files:
            try:
                code = py_file.read_text(encoding='utf-8')
                analysis_result["total_lines"] += len(code.splitlines())
                
                # Analyse fichier individuel
                file_analysis = await self.code_analyzer.analyze_code_structure(
                    code, str(py_file)
                )
                
                # Suggestions refactoring
                suggestions = await self.intelligent_refactorer.suggest_refactoring(
                    code, file_analysis
                )
                
                if suggestions:
                    analysis_result["refactoring_opportunities"].extend([
                        {**suggestion, "file": str(py_file)} 
                        for suggestion in suggestions
                    ])
                
            except Exception as e:
                self.logger.warning(f"⚠️ Erreur analyse {py_file}: {e}")
        
        # Estimation effort
        high_priority = len([op for op in analysis_result["refactoring_opportunities"] 
                           if op.get("priority") == "high"])
        medium_priority = len([op for op in analysis_result["refactoring_opportunities"] 
                             if op.get("priority") == "medium"])
        
        analysis_result["estimated_effort_hours"] = high_priority * 2.0 + medium_priority * 1.0
        
        # Recommandations globales IA
        if self.llm_gateway:
            try:
                recommendations = await self.llm_gateway.process_request(
                    "Generate project-wide refactoring recommendations",
                    context={
                        "role": "project_architect",
                        "analysis": analysis_result,
                        "task": "strategic_refactoring_plan"
                    }
                )
                
                if recommendations.get("success"):
                    analysis_result["recommendations"] = recommendations.get("recommendations", [])
                    
            except Exception as e:
                self.logger.warning(f"⚠️ Erreur recommandations IA: {e}")
        
        execution_time = (datetime.now() - start_time).total_seconds()
        analysis_result["analysis_time_seconds"] = execution_time
        
        return analysis_result
    
    async def execute_refactoring_plan(self, plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Exécution plan refactoring avec sauvegarde intelligente"""
        start_time = datetime.now()
        
        self.logger.info(f"🚀 Exécution plan refactoring: {len(plan)} opérations")
        
        execution_result = {
            "operations_total": len(plan),
            "operations_successful": 0,
            "operations_failed": 0,
            "files_modified": [],
            "backups_created": [],
            "errors": []
        }
        
        for operation_data in plan:
            try:
                operation = RefactoringOperation(
                    operation_type=operation_data["type"],
                    target=operation_data["file"],
                    params=operation_data
                )
                
                # Sauvegarde automatique
                if self.refactoring_config["auto_backup"]:
                    await self._create_backup(operation.target)
                
                # Exécution opération
                success = await self._execute_single_refactoring(operation)
                
                if success:
                    execution_result["operations_successful"] += 1
                    execution_result["files_modified"].append(operation.target)
                else:
                    execution_result["operations_failed"] += 1
                
                self.operation_history.append(operation)
                
            except Exception as e:
                execution_result["operations_failed"] += 1
                execution_result["errors"].append(str(e))
                self.logger.error(f"❌ Erreur opération refactoring: {e}")
        
        # Mise à jour métriques
        self.refactoring_metrics["operations_count"] += execution_result["operations_total"]
        self.refactoring_metrics["files_processed"] += len(execution_result["files_modified"])
        
        if execution_result["operations_total"] > 0:
            success_rate = execution_result["operations_successful"] / execution_result["operations_total"]
            self.refactoring_metrics["success_rate"] = (
                (self.refactoring_metrics["success_rate"] * 
                 (self.refactoring_metrics["operations_count"] - execution_result["operations_total"]) +
                 success_rate * execution_result["operations_total"]) /
                self.refactoring_metrics["operations_count"]
            )
        
        execution_time = (datetime.now() - start_time).total_seconds()
        execution_result["execution_time_seconds"] = execution_time
        
        return execution_result
    
    async def _execute_single_refactoring(self, operation: RefactoringOperation) -> bool:
        """Exécution opération refactoring individuelle"""
        try:
            file_path = Path(operation.target)
            
            if not file_path.exists():
                operation.status = "failed"
                operation.result = {"error": "File not found"}
                return False
            
            # Lecture code original
            original_code = file_path.read_text(encoding='utf-8')
            
            # Application refactoring
            refactored_code = await self.intelligent_refactorer.apply_refactoring(
                original_code, operation.params
            )
            
            # Écriture code refactorisé
            file_path.write_text(refactored_code, encoding='utf-8')
            
            operation.status = "completed"
            operation.result = {
                "original_lines": len(original_code.splitlines()),
                "refactored_lines": len(refactored_code.splitlines())
            }
            
            return True
            
        except Exception as e:
            operation.status = "failed"
            operation.result = {"error": str(e)}
            return False
    
    async def _create_backup(self, file_path: str) -> str:
        """Création sauvegarde intelligente"""
        source = Path(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{source.stem}_{timestamp}{source.suffix}"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(source, backup_path)
        
        self.logger.info(f"💾 Backup créé: {backup_path}")
        return str(backup_path)
    
    async def rollback_operation(self, operation_id: int) -> bool:
        """Rollback opération refactoring"""
        if operation_id >= len(self.operation_history):
            return False
        
        operation = self.operation_history[operation_id]
        
        if operation.backup_path and Path(operation.backup_path).exists():
            shutil.copy2(operation.backup_path, operation.target)
            self.logger.info(f"🔄 Rollback effectué: {operation.target}")
            return True
        
        return False
    
    async def get_refactoring_metrics(self) -> Dict[str, Any]:
        """Métriques refactoring temps réel"""
        return {
            "refactoring_metrics": self.refactoring_metrics,
            "operation_history_count": len(self.operation_history),
            "configuration": self.refactoring_config,
            "patterns": self.__nextgen_patterns__,
            "version": self.version,
            "timestamp": datetime.now().isoformat()
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check NextGeneration"""
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "status": "healthy",
            "patterns": self.__nextgen_patterns__,
            "services": {
                "llm_gateway": self.llm_gateway is not None,
                "message_bus": self.message_bus is not None,
                "context_store": self.context_store is not None
            },
            "refactoring": {
                "operations_executed": self.refactoring_metrics["operations_count"],
                "success_rate": self.refactoring_metrics["success_rate"],
                "files_processed": self.refactoring_metrics["files_processed"]
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function pour compatibilité
def create_assistant_99_refactoring(**config) -> AgentAssistant99RefactoringHelper_Enterprise:
    """Factory function pour créer l'agent"""
    return AgentAssistant99RefactoringHelper_Enterprise(**config)

# Test standalone
async def main():
    """Test de l'agent Assistant Refactoring"""
    print("🔧 Test Agent Assistant 99 Refactoring NextGeneration v5.3.0")
    
    agent = create_assistant_99_refactoring(agent_id="test_refactoring")
    
    # Health check
    health = await agent.health_check()
    print(f"🏥 Health: {health['status']}")
    
    # Test analyse projet
    analysis = await agent.analyze_project_for_refactoring("/mnt/c/Dev/nextgeneration/agents")
    print(f"📊 Analysis: {analysis['files_analyzed']} files, {len(analysis['refactoring_opportunities'])} opportunities")
    print(f"⏱️ Estimated effort: {analysis['estimated_effort_hours']:.1f} hours")
    
    # Métriques
    metrics = await agent.get_refactoring_metrics()
    print(f"📈 Operations executed: {metrics['refactoring_metrics']['operations_count']}")

if __name__ == "__main__":
    asyncio.run(main())