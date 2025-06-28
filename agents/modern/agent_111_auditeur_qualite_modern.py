#!/usr/bin/env python3
"""
🤖 Agent 111 - Auditeur Qualité (Architecture Moderne)
Version moderne migrant vers l'architecture NextGeneration

Migration Pattern:
- Legacy → Modern avec LLM-enhanced code analysis
- Préservation logique métier audit qualité et AST parsing
- Intégration services centraux (LLMGateway, MessageBus, ContextStore)
- Enhancement intelligent avec insights AI pour quality gates
"""

import asyncio
import ast
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import logging
import re

# Imports NextGeneration Architecture
try:
    from core.services import (
        LLMGatewayHybrid, create_llm_gateway,
        MessageBusA2A, create_envelope, MessageType, Priority,
        OptimizedContextStore, create_agent_context, ContextType
    )
except ImportError:
    # Fallback pour développement isolé
    print("⚠️ NextGeneration services not available - running in development mode")

class ModernAgent111AuditeurQualite:
    """
    Agent 111 Moderne - Auditeur Qualité
    
    Architecture NextGeneration avec:
    - LLM-enhanced code quality analysis
    - Intelligent quality gate recommendations
    - Structured communication via MessageBus
    - Context-aware audit patterns
    - Modern async AST analysis
    """
    
    def __init__(self, agent_id: str = "agent_111_auditeur_qualite"):
        self.agent_id = agent_id
        self.version = "2.0.0-modern"
        self.mission = "Audit qualité code avec insights AI - Architecture NextGeneration"
        self.agent_type = "quality_audit_modern"
        
        # Services centraux (seront injectés par l'orchestrateur)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Configuration moderne audit
        self.config = {
            "audit_strategy": "llm_enhanced_ast",
            "quality_threshold": 80,  # Score minimum acceptable
            "analysis_depth": "comprehensive",
            "enable_ai_suggestions": True,
            "docstring_coverage_target": 90,
            "complexity_threshold": 10
        }
        
        # Métriques et état
        self.metrics = {
            "files_audited": 0,
            "total_issues_found": 0,
            "avg_quality_score": 0.0,
            "audit_execution_times": [],
            "quality_improvements_suggested": 0,
            "last_audit": None
        }
        
        # Cache des audits pour optimisation
        self.audit_cache = {}
        
        # Logger moderne
        self.logger = logging.getLogger(f"nextgen.modern.{agent_id}")
        
        # État de migration pour ShadowMode
        self.migration_status = "modern_active"
        self.compatibility_mode = True
    
    async def initialize_services(self, llm_gateway=None, message_bus=None, context_store=None):
        """Initialise les services NextGeneration"""
        
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus
        self.context_store = context_store
        
        # Charger le contexte existant si disponible
        if self.context_store:
            context = await self.context_store.get_agent_context_complete(self.agent_id)
            if context and context.get("working_memory"):
                self.metrics.update(context["working_memory"].get("metrics", {}))
                self.audit_cache.update(context["working_memory"].get("audit_cache", {}))
        
        self.logger.info(f"🚀 Modern Agent 111 initialized with NextGeneration services")
    
    async def execute_async(self, envelope, context=None) -> Dict[str, Any]:
        """
        Interface moderne pour exécution via MessageBus
        Compatible avec l'interface legacy pour ShadowMode
        """
        
        start_time = time.time()
        
        try:
            # Extraire les paramètres de l'enveloppe
            payload = envelope.payload if hasattr(envelope, 'payload') else envelope
            task_type = payload.get("action", "audit_code_quality")
            task_data = payload.get("data", {})
            
            # Router vers la méthode appropriée
            if task_type == "audit_code_quality":
                file_path = task_data.get("file_path") or payload.get("file_path")
                if not file_path:
                    raise ValueError("file_path required for audit_code_quality")
                
                result = await self.audit_code_quality_moderne(file_path)
                
            elif task_type == "audit_universal_quality":
                file_path = task_data.get("file_path") or payload.get("file_path")
                if not file_path:
                    raise ValueError("file_path required for audit_universal_quality")
                
                result = await self.audit_code_quality_moderne(file_path)
                
            elif task_type == "batch_audit":
                file_paths = task_data.get("file_paths", [])
                result = await self.batch_audit_moderne(file_paths)
                
            elif task_type == "quality_report":
                result = await self.generate_quality_report_moderne(task_data)
                
            else:
                # Fallback vers audit simple
                file_path = task_data.get("file_path") or payload.get("file_path", "unknown.py")
                result = await self.audit_code_quality_moderne(file_path)
            
            # Enregistrer les métriques
            execution_time = int((time.time() - start_time) * 1000)
            self.metrics["files_audited"] += 1
            self.metrics["audit_execution_times"].append(execution_time)
            
            # Sauvegarder le contexte
            if self.context_store:
                await self._save_execution_context(result, execution_time)
            
            return {
                "agent_id": self.agent_id,
                "status": "success",
                "result": result,
                "execution_time_ms": execution_time,
                "version": self.version,
                "architecture": "nextgeneration_modern"
            }
            
        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            self.logger.error(f"❌ Execution error in modern agent: {e}")
            
            return {
                "agent_id": self.agent_id,
                "status": "error",
                "error": str(e),
                "execution_time_ms": execution_time,
                "version": self.version
            }
    
    async def audit_code_quality_moderne(self, file_path: str) -> Dict[str, Any]:
        """
        Version moderne de l'audit qualité avec enhancement LLM
        Préserve toute la logique legacy + ajoute intelligence moderne
        """
        
        self.logger.info(f"🔍 Audit qualité moderne: {file_path}")
        
        try:
            # Lecture du fichier
            if not Path(file_path).exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            code = Path(file_path).read_text(encoding='utf-8')
            
            # 1. Audit AST traditionnel (préservation logique legacy)
            traditional_audit = await self._audit_code_ast_traditional(code, file_path)
            
            # 2. Enhancement LLM moderne
            llm_enhancement = await self._enhance_audit_with_llm(code, file_path, traditional_audit)
            
            # 3. Analyse moderne avancée
            modern_analysis = await self._advanced_modern_analysis(code, file_path)
            
            # 4. Fusion intelligente des résultats
            final_report = await self._merge_audit_results(
                traditional_audit, llm_enhancement, modern_analysis, file_path
            )
            
            # 5. Notification via MessageBus si disponible
            if self.message_bus:
                await self._notify_audit_completion(final_report)
            
            self.metrics["last_audit"] = datetime.now().isoformat()
            return final_report
            
        except Exception as e:
            self.logger.error(f"❌ Audit failed for {file_path}: {e}")
            return {
                "file_path": file_path,
                "status": "error",
                "error": str(e),
                "quality_score": 0,
                "architecture": "nextgeneration_modern"
            }
    
    async def _audit_code_ast_traditional(self, code: str, file_path: str) -> Dict[str, Any]:
        """
        Audit AST traditionnel - PRÉSERVATION COMPLÈTE logique legacy
        """
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "file_path": file_path,
                "quality_score": 0,
                "issues": [{"severity": "CRITICAL", "description": f"SyntaxError: {e}", "code": "SYNTAX_ERROR"}],
                "error": f"SyntaxError: {e}",
                "analysis_type": "traditional_ast"
            }
        
        score = 100
        issues = []
        
        # 1. Vérification du docstring de module (logique legacy préservée)
        has_module_docstring = self._has_module_docstring_manual(tree)
        if not has_module_docstring:
            score -= 20
            issues.append({
                "severity": "HIGH", 
                "description": "Docstring de module manquant.",
                "code": "MISSING_MODULE_DOCSTRING"
            })
        
        # 2. Vérification des docstrings de fonction et classe (logique legacy préservée)
        total_funcs = 0
        total_classes = 0
        funcs_without_docstrings = []
        classes_without_docstrings = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                total_classes += 1
                if not ast.get_docstring(node):
                    classes_without_docstrings.append({"class": node.name})
            
            if isinstance(node, ast.FunctionDef):
                total_funcs += 1
                if not ast.get_docstring(node):
                    funcs_without_docstrings.append({"function": node.name})
        
        if funcs_without_docstrings:
            score -= len(funcs_without_docstrings) * 5
            issues.append({
                "severity": "MEDIUM", 
                "description": f"{len(funcs_without_docstrings)} fonction(s) sans docstring.",
                "code": "MISSING_FUNCTION_DOCSTRING",
                "details": funcs_without_docstrings
            })
        
        if classes_without_docstrings:
            score -= len(classes_without_docstrings) * 5
            issues.append({
                "severity": "MEDIUM", 
                "description": f"{len(classes_without_docstrings)} classe(s) sans docstring.",
                "code": "MISSING_CLASS_DOCSTRING",
                "details": classes_without_docstrings
            })
        
        # 3. Métriques étendues (extension moderne de la logique legacy)
        complexity_issues = self._analyze_complexity(tree)
        if complexity_issues:
            score -= len(complexity_issues) * 3
            issues.extend(complexity_issues)
        
        return {
            "file_path": file_path,
            "quality_score": max(0, score),
            "metrics": {
                "total_lines": len(code.splitlines()),
                "total_functions": total_funcs,
                "total_classes": total_classes,
                "module_docstring": "✅ Oui" if has_module_docstring else "❌ Non",
                "functions_no_docstring": len(funcs_without_docstrings),
                "classes_no_docstring": len(classes_without_docstrings),
                "docstring_coverage": self._calculate_docstring_coverage(total_funcs + total_classes, 
                                                                       len(funcs_without_docstrings) + len(classes_without_docstrings))
            },
            "issues": issues,
            "analysis_type": "traditional_ast_extended"
        }
    
    def _has_module_docstring_manual(self, tree: ast.Module) -> bool:
        """Préservation exacte de la logique legacy"""
        
        if not hasattr(tree, 'body') or not tree.body:
            return False
        
        first_node = tree.body[0]
        
        # Python < 3.8
        if hasattr(ast, 'Str') and isinstance(first_node, ast.Expr) and isinstance(first_node.value, ast.Str):
            return True
            
        # Python >= 3.8
        if isinstance(first_node, ast.Expr) and isinstance(first_node.value, ast.Constant) and isinstance(first_node.value.value, str):
            return True
            
        return False
    
    def _analyze_complexity(self, tree: ast.Module) -> List[Dict[str, Any]]:
        """Analyse de complexité cyclomatique moderne"""
        
        complexity_issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_cyclomatic_complexity(node)
                if complexity > self.config["complexity_threshold"]:
                    complexity_issues.append({
                        "severity": "MEDIUM",
                        "description": f"Fonction '{node.name}' a une complexité élevée ({complexity})",
                        "code": "HIGH_COMPLEXITY",
                        "function": node.name,
                        "complexity": complexity
                    })
        
        return complexity_issues
    
    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calcul complexité cyclomatique d'une fonction"""
        
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
        
        return complexity
    
    def _calculate_docstring_coverage(self, total_items: int, missing_docstrings: int) -> float:
        """Calcul pourcentage couverture docstring"""
        
        if total_items == 0:
            return 100.0
        
        covered = total_items - missing_docstrings
        return (covered / total_items) * 100
    
    async def _enhance_audit_with_llm(self, code: str, file_path: str, traditional_audit: Dict) -> Dict[str, Any]:
        """
        Enhancement LLM de l'audit traditionnel
        """
        
        if not self.llm_gateway:
            return {"llm_enhancement": "unavailable", "reason": "LLM gateway not available"}
        
        try:
            # Préparer le contexte pour l'LLM
            context_prompt = self._prepare_llm_audit_context(code, file_path, traditional_audit)
            
            # Requête LLM pour enhancement audit
            llm_response = await self.llm_gateway.query(
                prompt=context_prompt,
                agent_id=self.agent_id,
                context={"analysis_type": "code_quality_audit", "file_path": file_path}
            )
            
            # Parser la réponse LLM
            llm_insights = self._parse_llm_audit_response(llm_response.content)
            
            return {
                "llm_analysis": llm_insights,
                "confidence_score": llm_response.confidence if hasattr(llm_response, 'confidence') else 0.8,
                "processing_time_ms": llm_response.processing_time_ms if hasattr(llm_response, 'processing_time_ms') else 0,
                "enhancement_type": "llm_code_quality"
            }
            
        except Exception as e:
            self.logger.warning(f"⚠️ LLM enhancement failed: {e}")
            return {
                "llm_analysis": {"error": str(e)},
                "fallback_analysis": "LLM enhancement unavailable, using traditional analysis only"
            }
    
    def _prepare_llm_audit_context(self, code: str, file_path: str, traditional_audit: Dict) -> str:
        """Prépare le contexte pour l'analyse LLM"""
        
        code_preview = code[:1000] + "..." if len(code) > 1000 else code
        
        return f"""
Audit qualité code avancé - Agent 111 Auditeur Qualité NextGeneration

Fichier analysé: {file_path}
Code (aperçu):
```python
{code_preview}
```

Audit traditionnel AST:
- Score qualité: {traditional_audit.get('quality_score', 0)}/100
- Issues trouvées: {len(traditional_audit.get('issues', []))}
- Métriques: {json.dumps(traditional_audit.get('metrics', {}), indent=2)}

Veuillez fournir une analyse intelligente supplémentaire:

1. **Code Quality Gate** - Recommandations spécifiques pour améliorer le score
2. **Security Analysis** - Identification de vulnérabilités potentielles
3. **Performance Optimization** - Suggestions d'optimisation 
4. **Architecture Patterns** - Conformité aux bonnes pratiques
5. **Maintainability Score** - Évaluation facilité de maintenance
6. **Technical Debt** - Identification de la dette technique

Format de réponse JSON attendu:
{{
    "quality_gate_recommendations": [<liste>],
    "security_issues": [<liste>],
    "performance_suggestions": [<liste>],
    "architecture_score": <0-100>,
    "maintainability_score": <0-100>,
    "technical_debt_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
    "priority_actions": [<liste>],
    "enhanced_score": <0-100>
}}
"""
    
    def _parse_llm_audit_response(self, llm_content: str) -> Dict[str, Any]:
        """Parse la réponse LLM d'audit"""
        
        try:
            # Tenter de parser comme JSON
            if "{" in llm_content and "}" in llm_content:
                start = llm_content.find("{")
                end = llm_content.rfind("}") + 1
                json_str = llm_content[start:end]
                return json.loads(json_str)
            
            # Fallback: analyser comme texte
            return {
                "analysis_text": llm_content,
                "structured_format": False,
                "manual_review_required": True
            }
            
        except Exception as e:
            return {
                "parsing_error": str(e),
                "raw_content": llm_content[:500],
                "manual_review_required": True
            }
    
    async def _advanced_modern_analysis(self, code: str, file_path: str) -> Dict[str, Any]:
        """Analyse moderne avancée du code"""
        
        try:
            tree = ast.parse(code)
            
            # Analyse des imports
            imports_analysis = self._analyze_imports(tree)
            
            # Analyse des patterns
            patterns_analysis = self._analyze_code_patterns(tree, code)
            
            # Analyse de sécurité statique
            security_analysis = self._analyze_security_patterns(code)
            
            return {
                "imports_analysis": imports_analysis,
                "patterns_analysis": patterns_analysis,
                "security_analysis": security_analysis,
                "modern_metrics": self._calculate_modern_metrics(tree, code),
                "analysis_type": "advanced_modern"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "analysis_type": "advanced_modern_failed"
            }
    
    def _analyze_imports(self, tree: ast.Module) -> Dict[str, Any]:
        """Analyse des imports du module"""
        
        imports = []
        from_imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    from_imports.append(f"from {module} import {alias.name}")
        
        return {
            "total_imports": len(imports) + len(from_imports),
            "direct_imports": imports,
            "from_imports": from_imports,
            "import_complexity": "low" if len(imports) + len(from_imports) < 10 else "high"
        }
    
    def _analyze_code_patterns(self, tree: ast.Module, code: str) -> Dict[str, Any]:
        """Analyse des patterns de code"""
        
        patterns = {
            "async_functions": 0,
            "decorators_used": 0,
            "exception_handlers": 0,
            "list_comprehensions": 0,
            "lambda_functions": 0
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                patterns["async_functions"] += 1
            elif isinstance(node, ast.FunctionDef) and node.decorator_list:
                patterns["decorators_used"] += len(node.decorator_list)
            elif isinstance(node, ast.ExceptHandler):
                patterns["exception_handlers"] += 1
            elif isinstance(node, ast.ListComp):
                patterns["list_comprehensions"] += 1
            elif isinstance(node, ast.Lambda):
                patterns["lambda_functions"] += 1
        
        return patterns
    
    def _analyze_security_patterns(self, code: str) -> Dict[str, Any]:
        """Analyse de sécurité statique basique"""
        
        security_issues = []
        
        # Patterns de sécurité basiques
        dangerous_patterns = [
            (r'eval\s*\(', "Use of eval() function - security risk"),
            (r'exec\s*\(', "Use of exec() function - security risk"),
            (r'subprocess\.call\s*\(', "Subprocess call without shell=False"),
            (r'os\.system\s*\(', "Use of os.system() - security risk"),
            (r'input\s*\(.*\)', "Use of input() - potential injection risk")
        ]
        
        for pattern, description in dangerous_patterns:
            if re.search(pattern, code):
                security_issues.append({
                    "pattern": pattern,
                    "description": description,
                    "severity": "HIGH"
                })
        
        return {
            "security_issues": security_issues,
            "security_score": max(0, 100 - len(security_issues) * 20),
            "analysis_type": "static_security"
        }
    
    def _calculate_modern_metrics(self, tree: ast.Module, code: str) -> Dict[str, Any]:
        """Calcul métriques modernes"""
        
        lines = code.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            "total_lines": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "comment_lines": len([line for line in lines if line.strip().startswith('#')]),
            "blank_lines": len(lines) - len(non_empty_lines),
            "code_density": len(non_empty_lines) / len(lines) if lines else 0,
            "estimated_reading_time_minutes": len(non_empty_lines) / 50  # 50 lignes par minute
        }
    
    async def _merge_audit_results(self, traditional: Dict, llm_enhancement: Dict, 
                                 modern: Dict, file_path: str) -> Dict[str, Any]:
        """Fusion intelligente des résultats d'audit"""
        
        # Score composite intelligent
        base_score = traditional.get("quality_score", 0)
        llm_score = llm_enhancement.get("llm_analysis", {}).get("enhanced_score", base_score)
        security_score = modern.get("security_analysis", {}).get("security_score", 100)
        
        # Pondération: 40% traditionnel, 35% LLM, 25% sécurité
        composite_score = (base_score * 0.4 + llm_score * 0.35 + security_score * 0.25)
        
        # Issues consolidées
        all_issues = traditional.get("issues", [])
        
        # Ajouter issues LLM si disponibles
        llm_issues = llm_enhancement.get("llm_analysis", {}).get("quality_gate_recommendations", [])
        for issue in llm_issues:
            all_issues.append({
                "severity": "AI_RECOMMENDATION",
                "description": issue,
                "code": "LLM_ENHANCEMENT",
                "source": "ai_analysis"
            })
        
        # Ajouter issues sécurité
        security_issues = modern.get("security_analysis", {}).get("security_issues", [])
        all_issues.extend(security_issues)
        
        # Mise à jour métriques agent
        self.metrics["total_issues_found"] += len(all_issues)
        
        # Calcul score moyen
        current_avg = self.metrics["avg_quality_score"]
        files_count = self.metrics["files_audited"]
        self.metrics["avg_quality_score"] = (current_avg * (files_count - 1) + composite_score) / files_count
        
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "architecture": "nextgeneration_modern",
            "file_path": file_path,
            "timestamp": datetime.now().isoformat(),
            
            # Scores
            "quality_score": round(composite_score, 2),
            "traditional_score": base_score,
            "llm_enhanced_score": llm_score,
            "security_score": security_score,
            
            # Analyses détaillées
            "traditional_analysis": traditional,
            "llm_enhancement": llm_enhancement,
            "modern_analysis": modern,
            
            # Consolidation
            "all_issues": all_issues,
            "total_issues": len(all_issues),
            "issue_severity_breakdown": self._categorize_issues_by_severity(all_issues),
            
            # Recommandations
            "recommendations": self._generate_recommendations(composite_score, all_issues),
            "quality_gate_status": "PASS" if composite_score >= self.config["quality_threshold"] else "FAIL",
            
            # Métriques enrichies
            "enhanced_metrics": {
                **traditional.get("metrics", {}),
                **modern.get("modern_metrics", {}),
                "composite_score": composite_score,
                "ai_enhanced": True
            }
        }
    
    def _categorize_issues_by_severity(self, issues: List[Dict]) -> Dict[str, int]:
        """Catégorisation des issues par sévérité"""
        
        severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "AI_RECOMMENDATION": 0}
        
        for issue in issues:
            severity = issue.get("severity", "MEDIUM")
            if severity in severity_count:
                severity_count[severity] += 1
            else:
                severity_count["MEDIUM"] += 1
        
        return severity_count
    
    def _generate_recommendations(self, score: float, issues: List[Dict]) -> List[str]:
        """Génération de recommandations basées sur l'audit"""
        
        recommendations = []
        
        if score < 70:
            recommendations.append("🚨 CRITIQUE: Score qualité très faible - Review complète requise")
        elif score < 80:
            recommendations.append("⚠️ ATTENTION: Score qualité sous le seuil - Améliorations nécessaires")
        elif score >= 90:
            recommendations.append("✅ EXCELLENT: Code de haute qualité - Maintenir le niveau")
        
        # Recommandations spécifiques par type d'issue
        critical_issues = [i for i in issues if i.get("severity") == "CRITICAL"]
        if critical_issues:
            recommendations.append(f"🔴 {len(critical_issues)} issue(s) critique(s) à corriger immédiatement")
        
        security_issues = [i for i in issues if "security" in i.get("code", "").lower()]
        if security_issues:
            recommendations.append(f"🔒 {len(security_issues)} problème(s) de sécurité identifié(s)")
        
        ai_recommendations = [i for i in issues if i.get("severity") == "AI_RECOMMENDATION"]
        if ai_recommendations:
            recommendations.append(f"🤖 {len(ai_recommendations)} suggestion(s) IA pour amélioration")
        
        return recommendations
    
    async def batch_audit_moderne(self, file_paths: List[str]) -> Dict[str, Any]:
        """Audit en lot avec optimisations modernes"""
        
        self.logger.info(f"🔍 Batch audit moderne: {len(file_paths)} fichiers")
        
        results = []
        total_score = 0
        total_issues = 0
        
        for file_path in file_paths:
            try:
                audit_result = await self.audit_code_quality_moderne(file_path)
                results.append(audit_result)
                total_score += audit_result.get("quality_score", 0)
                total_issues += audit_result.get("total_issues", 0)
            except Exception as e:
                self.logger.error(f"❌ Batch audit failed for {file_path}: {e}")
                results.append({
                    "file_path": file_path,
                    "status": "error",
                    "error": str(e)
                })
        
        avg_score = total_score / len(file_paths) if file_paths else 0
        
        return {
            "batch_audit_summary": {
                "total_files": len(file_paths),
                "average_score": round(avg_score, 2),
                "total_issues": total_issues,
                "quality_gate_status": "PASS" if avg_score >= self.config["quality_threshold"] else "FAIL"
            },
            "detailed_results": results,
            "architecture": "nextgeneration_modern"
        }
    
    async def generate_quality_report_moderne(self, report_data: Dict) -> Dict[str, Any]:
        """Génération rapport qualité moderne avec insights"""
        
        return {
            "quality_report": {
                "agent_metrics": self.metrics,
                "configuration": self.config,
                "report_data": report_data,
                "architecture": "nextgeneration_modern"
            }
        }
    
    async def _save_execution_context(self, result: Dict, execution_time: int):
        """Sauvegarde contexte d'exécution"""
        
        if not self.context_store:
            return
        
        try:
            # Contexte working memory
            working_context = create_agent_context(
                agent_id=self.agent_id,
                context_type=ContextType.WORKING_MEMORY,
                data={
                    "last_execution": {
                        "result": result,
                        "execution_time_ms": execution_time,
                        "timestamp": datetime.now().isoformat()
                    },
                    "metrics": self.metrics,
                    "audit_cache": self.audit_cache,
                    "config": self.config
                }
            )
            
            await self.context_store.save_agent_context(working_context)
            
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to save execution context: {e}")
    
    async def _notify_audit_completion(self, audit_result: Dict):
        """Notification completion audit via MessageBus"""
        
        if not self.message_bus:
            return
        
        try:
            notification_envelope = create_envelope(
                task_id=f"audit_completion_{int(time.time())}",
                message_type=MessageType.TASK_COMPLETE,
                source_agent=self.agent_id,
                target_agent="system",
                payload={
                    "event": "audit_completed",
                    "agent_id": self.agent_id,
                    "file_path": audit_result.get("file_path"),
                    "quality_score": audit_result.get("quality_score"),
                    "quality_gate_status": audit_result.get("quality_gate_status"),
                    "total_issues": audit_result.get("total_issues", 0)
                }
            )
            
            await self.message_bus.publish(notification_envelope)
            
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to notify audit completion: {e}")
    
    # === COMPATIBILITY METHODS FOR LEGACY INTERFACE ===
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interface legacy synchrone pour compatibilité ShadowMode
        Wrapper autour de execute_async
        """
        
        try:
            # Convertir params legacy vers envelope moderne
            envelope = {
                "payload": {
                    "action": params.get("action", "audit_code_quality"),
                    "data": params.get("data", {}),
                    "file_path": params.get("file_path")
                }
            }
            
            # Exécuter de manière synchrone (pour compatibilité)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(self.execute_async(envelope))
                return result
            finally:
                loop.close()
                
        except Exception as e:
            self.logger.error(f"❌ Legacy execute error: {e}")
            return {
                "agent_id": self.agent_id,
                "status": "error",
                "error": str(e),
                "version": self.version,
                "compatibility_mode": True
            }
    
    async def audit_code_quality(self, file_path: str) -> Dict[str, Any]:
        """Interface legacy compatibility"""
        return await self.audit_code_quality_moderne(file_path)

# Factory function pour création d'instance
async def create_modern_agent_111(agent_id: str = "agent_111_auditeur_qualite") -> ModernAgent111AuditeurQualite:
    """Factory function pour création agent moderne"""
    
    agent = ModernAgent111AuditeurQualite(agent_id)
    
    # Initialiser avec services si disponibles
    try:
        llm_gateway = await create_llm_gateway()
        await agent.initialize_services(llm_gateway=llm_gateway)
    except Exception as e:
        print(f"⚠️ Services not available during creation: {e}")
    
    return agent

# Demo et tests
async def demo_modern_agent_111():
    """Démonstration agent moderne 111"""
    
    print("🚀 Modern Agent 111 - Auditeur Qualité Demo")
    print("=" * 60)
    
    try:
        # Créer agent moderne
        agent = await create_modern_agent_111()
        
        # Test 1: Audit simple
        print("\n🧪 Test 1: Audit Code Quality")
        
        test_envelope = {
            "payload": {
                "action": "audit_code_quality",
                "file_path": __file__,  # S'auditer lui-même
                "data": {"context": "demo_mode"}
            }
        }
        
        result = await agent.execute_async(test_envelope)
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            audit_result = result['result']
            print(f"Quality Score: {audit_result.get('quality_score', 0)}/100")
            print(f"Total Issues: {audit_result.get('total_issues', 0)}")
            print(f"Quality Gate: {audit_result.get('quality_gate_status', 'UNKNOWN')}")
        
        # Test 2: Compatibility Legacy
        print("\n🧪 Test 2: Legacy Compatibility")
        
        legacy_params = {
            "action": "audit_universal_quality",
            "file_path": __file__,
            "data": {"mode": "legacy_compat"}
        }
        
        legacy_result = agent.execute(legacy_params)
        print(f"Legacy Status: {legacy_result['status']}")
        print(f"Compatibility: {legacy_result.get('compatibility_mode', False)}")
        
        # Test 3: Métriques
        print("\n📊 Agent Metrics")
        print(f"Files audited: {agent.metrics['files_audited']}")
        print(f"Average quality score: {agent.metrics['avg_quality_score']:.2f}")
        
        print("\n✅ Demo completed successfully")
        print(f"Agent Version: {agent.version}")
        print(f"Architecture: NextGeneration Modern")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

# Alias pour compatibilité avec validateur
class ModernAgent111(ModernAgent111AuditeurQualite):
    """Alias pour validation Phase 1"""
    pass

# Autres alias
Agent111Modern = ModernAgent111AuditeurQualite
AuditeurQualiteModern = ModernAgent111AuditeurQualite

if __name__ == "__main__":
    asyncio.run(demo_modern_agent_111())