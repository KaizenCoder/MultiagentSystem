#!/usr/bin/env python3
"""
🔍 Agent Analyse Solution ChatGPT - NextGeneration v5.3.0
Version enterprise Wave 3 avec benchmarking intelligent IA

Migration Pattern: BENCHMARKING_INTELLIGENCE + LLM_ENHANCED + RESEARCH
Author: Claude Sonnet 4
Date: 29 Juin 2025
"""

import os
import sys
import json
import re
import asyncio
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import logging
import hashlib
import statistics

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
    from agents.agent_analyse_solution_chatgpt import AgentAnalyseSolutionChatGPT as LegacyAgent
except ImportError:
    class LegacyAgent:
        def __init__(self, *args, **kwargs):
            self.version = "1.0.0"
            self.name = "Analyse Solution Legacy"

class SolutionAnalyzer:
    """Analyseur de solutions intelligent avec benchmarking IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.analysis_patterns = {
            "architecture": r"class\s+\w+|def\s+\w+|import\s+\w+",
            "api_calls": r"requests\.|http\.|api\.|fetch\(",
            "data_processing": r"json\.|pandas\.|numpy\.|data",
            "ai_integration": r"openai\.|anthropic\.|llm\.|gpt\.|claude",
            "error_handling": r"try:|except:|raise|Error"
        }
    
    async def analyze_solution_architecture(self, solution_path: str) -> Dict[str, Any]:
        """Analyse architecture solution avec IA"""
        path = Path(solution_path)
        
        analysis = {
            "path": str(path),
            "type": "unknown",
            "components": [],
            "patterns": {},
            "quality_score": 0.0,
            "recommendations": []
        }
        
        if not path.exists():
            analysis["error"] = "Path does not exist"
            return analysis
        
        # Analyse fichiers
        if path.is_file():
            analysis.update(await self._analyze_single_file(path))
        elif path.is_dir():
            analysis.update(await self._analyze_directory(path))
        
        # Enhancement IA
        if self.llm_gateway:
            try:
                ai_analysis = await self.llm_gateway.process_request(
                    f"Analyze solution architecture: {solution_path}",
                    context={
                        "role": "solution_architect",
                        "analysis": analysis,
                        "task": "comprehensive_solution_analysis"
                    }
                )
                
                if ai_analysis.get("success"):
                    enhancement = ai_analysis.get("enhancement", {})
                    analysis.update(enhancement)
                    
            except Exception as e:
                # Log but continue
                pass
        
        return analysis
    
    async def _analyze_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyse fichier individuel"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            return {
                "type": "file",
                "size_bytes": len(content.encode('utf-8')),
                "lines": len(content.splitlines()),
                "extension": file_path.suffix,
                "patterns": self._detect_patterns(content),
                "complexity": self._calculate_complexity(content)
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _analyze_directory(self, dir_path: Path) -> Dict[str, Any]:
        """Analyse répertoire complet"""
        components = []
        total_lines = 0
        file_types = {}
        
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    lines = len(content.splitlines())
                    total_lines += lines
                    
                    ext = file_path.suffix or "no_extension"
                    file_types[ext] = file_types.get(ext, 0) + 1
                    
                    components.append({
                        "file": str(file_path.relative_to(dir_path)),
                        "lines": lines,
                        "type": ext,
                        "patterns": self._detect_patterns(content)
                    })
                    
                except Exception:
                    # Skip unreadable files
                    pass
        
        return {
            "type": "directory",
            "components": components,
            "total_files": len(components),
            "total_lines": total_lines,
            "file_types": file_types,
            "complexity": self._calculate_directory_complexity(components)
        }
    
    def _detect_patterns(self, content: str) -> Dict[str, int]:
        """Détection patterns dans le code"""
        detected = {}
        
        for pattern_name, pattern_regex in self.analysis_patterns.items():
            matches = re.findall(pattern_regex, content, re.IGNORECASE)
            detected[pattern_name] = len(matches)
        
        return detected
    
    def _calculate_complexity(self, content: str) -> float:
        """Calcul complexité fichier"""
        lines = content.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Facteurs de complexité
        complexity_factors = {
            "lines": len(non_empty_lines) * 0.1,
            "functions": len(re.findall(r'def\s+\w+', content)) * 2,
            "classes": len(re.findall(r'class\s+\w+', content)) * 3,
            "imports": len(re.findall(r'import\s+\w+|from\s+\w+', content)) * 0.5,
            "conditionals": len(re.findall(r'if\s+|elif\s+|else:', content)) * 1,
            "loops": len(re.findall(r'for\s+|while\s+', content)) * 1.5
        }
        
        return sum(complexity_factors.values())
    
    def _calculate_directory_complexity(self, components: List[Dict]) -> float:
        """Calcul complexité répertoire"""
        if not components:
            return 0.0
        
        total_complexity = sum(comp.get("complexity", 0) for comp in components)
        return total_complexity / len(components)

class BenchmarkingEngine:
    """Moteur de benchmarking intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.benchmark_criteria = {
            "performance": ["execution_time", "memory_usage", "throughput"],
            "quality": ["maintainability", "readability", "testability"],
            "architecture": ["modularity", "scalability", "flexibility"],
            "innovation": ["ai_integration", "modern_patterns", "best_practices"]
        }
    
    async def benchmark_solution(self, solution_analysis: Dict[str, Any], 
                               reference_solutions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Benchmarking solution avec IA comparative"""
        benchmark = {
            "solution": solution_analysis["path"],
            "scores": {},
            "comparisons": [],
            "ranking": "unknown",
            "recommendations": []
        }
        
        # Calcul scores par critère
        for category, criteria in self.benchmark_criteria.items():
            category_score = await self._calculate_category_score(
                solution_analysis, category, criteria
            )
            benchmark["scores"][category] = category_score
        
        # Score global
        benchmark["overall_score"] = statistics.mean(benchmark["scores"].values())
        
        # Comparaisons avec références
        if reference_solutions:
            benchmark["comparisons"] = await self._compare_with_references(
                solution_analysis, reference_solutions
            )
        
        # Ranking intelligent avec IA
        if self.llm_gateway:
            try:
                ranking_analysis = await self.llm_gateway.process_request(
                    "Provide intelligent solution ranking and recommendations",
                    context={
                        "role": "solution_benchmarking_expert",
                        "benchmark": benchmark,
                        "task": "intelligent_ranking_analysis"
                    }
                )
                
                if ranking_analysis.get("success"):
                    benchmark["ranking"] = ranking_analysis.get("ranking", "unknown")
                    benchmark["recommendations"] = ranking_analysis.get("recommendations", [])
                    
            except Exception as e:
                # Log but continue
                pass
        
        return benchmark
    
    async def _calculate_category_score(self, analysis: Dict[str, Any], 
                                      category: str, criteria: List[str]) -> float:
        """Calcul score par catégorie"""
        scores = []
        
        for criterion in criteria:
            score = await self._calculate_criterion_score(analysis, criterion)
            scores.append(score)
        
        return statistics.mean(scores) if scores else 0.0
    
    async def _calculate_criterion_score(self, analysis: Dict[str, Any], 
                                       criterion: str) -> float:
        """Calcul score par critère"""
        # Scores basiques selon patterns détectés
        patterns = analysis.get("patterns", {})
        
        if criterion == "ai_integration":
            return min(patterns.get("ai_integration", 0) * 20, 100)
        elif criterion == "maintainability":
            complexity = analysis.get("complexity", 0)
            return max(100 - complexity, 0)
        elif criterion == "modularity":
            components = len(analysis.get("components", []))
            return min(components * 10, 100)
        elif criterion == "modern_patterns":
            return min(patterns.get("architecture", 0) * 15, 100)
        else:
            # Score par défaut
            return 75.0
    
    async def _compare_with_references(self, solution: Dict[str, Any], 
                                     references: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Comparaison avec solutions de référence"""
        comparisons = []
        
        for ref in references:
            comparison = {
                "reference": ref.get("name", "Unknown"),
                "similarities": [],
                "differences": [],
                "advantage_score": 0.0
            }
            
            # Comparaison patterns
            solution_patterns = solution.get("patterns", {})
            ref_patterns = ref.get("patterns", {})
            
            for pattern in set(solution_patterns.keys()) | set(ref_patterns.keys()):
                sol_count = solution_patterns.get(pattern, 0)
                ref_count = ref_patterns.get(pattern, 0)
                
                if sol_count > ref_count:
                    comparison["similarities"].append(f"Better {pattern} usage")
                elif sol_count < ref_count:
                    comparison["differences"].append(f"Less {pattern} usage")
                else:
                    comparison["similarities"].append(f"Similar {pattern} usage")
            
            # Score avantage
            solution_complexity = solution.get("complexity", 0)
            ref_complexity = ref.get("complexity", 0)
            
            if solution_complexity < ref_complexity:
                comparison["advantage_score"] = 1.0 - (solution_complexity / ref_complexity)
            else:
                comparison["advantage_score"] = -(solution_complexity / ref_complexity - 1.0)
            
            comparisons.append(comparison)
        
        return comparisons

class AgentAnalyseSolutionChatGPT_Enterprise:
    """
    🔍 Agent Analyse Solution ChatGPT - Enterprise NextGeneration v5.3.0
    
    Analyseur et benchmarking intelligent de solutions avec IA contextuelle.
    
    Patterns NextGeneration v5.3.0:
    - BENCHMARKING_INTELLIGENCE: Benchmarking intelligent automatisé
    - LLM_ENHANCED: Intelligence IA pour analyse comparative
    - RESEARCH: Recherche et analyse solutions avancée
    - PATTERN_FACTORY: Architecture modulaire éprouvée
    """
    
    def __init__(self, agent_id: str = "analyse_solution_chatgpt"):
        # Métadonnées NextGeneration v5.3.0
        self.agent_id = agent_id
        self.version = "5.3.0"
        self.wave_version = "Wave 3 - Benchmarking Intelligence FINAL"
        self.migration_status = "modern_active"
        self.compatibility_mode = True
        
        # Patterns NextGeneration appliqués
        self.__version__ = "5.3.0"
        self.__wave_version__ = "Wave 3 - Benchmarking Intelligence FINAL"
        self.__nextgen_patterns__ = [
            "BENCHMARKING_INTELLIGENCE",
            "LLM_ENHANCED",
            "RESEARCH",
            "PATTERN_FACTORY"
        ]
        
        # Configuration agent
        self.name = "Analyse Solution Benchmarking Enterprise"
        self.mission = "Analyse et benchmarking intelligent solutions avec IA"
        self.agent_type = "solution_analyzer_enterprise"
        
        # Services NextGeneration (injectés à l'initialisation)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Moteurs d'analyse intelligents
        self.solution_analyzer = SolutionAnalyzer()
        self.benchmarking_engine = BenchmarkingEngine()
        
        # Configuration analyse
        self.analysis_config = {
            "deep_analysis": True,
            "benchmark_enabled": True,
            "ai_enhancement": True,
            "cache_results": True,
            "parallel_processing": True
        }
        
        # Métriques d'analyse
        self.analysis_metrics = {
            "solutions_analyzed": 0,
            "benchmarks_completed": 0,
            "average_score": 0.0,
            "processing_time_avg": 0.0
        }
        
        # Cache intelligent
        self.analysis_cache = {}
        self.benchmark_cache = {}
        
        # Intelligence contextuelle
        self.analysis_context = {
            "domain_expertise": [],
            "learned_patterns": {},
            "quality_benchmarks": {},
            "best_practices": []
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
                config_name="analysis",
                custom_config={
                    "logger_name": f"nextgen.analysis.solution_chatgpt.{self.agent_id}",
                    "log_dir": "logs/analysis",
                    "metadata": {
                        "agent_type": "analyse_solution_chatgpt",
                        "agent_role": "analysis",
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
            self.logger = logging.getLogger(f"SolutionAnalyzer_{self.agent_id}")
    
    async def inject_nextgen_services(self, 
                                    llm_gateway: LLMGatewayHybrid,
                                    message_bus: MessageBusA2A, 
                                    context_store: OptimizedContextStore):
        """Injection des services NextGeneration v5.3.0"""
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus  
        self.context_store = context_store
        
        # Configuration analyseurs avec IA
        self.solution_analyzer.llm_gateway = llm_gateway
        self.benchmarking_engine.llm_gateway = llm_gateway
        
        # Configuration contexte analyse IA
        await self._setup_analysis_context()
        
        self.logger.info("✅ Services NextGeneration injectés - Analyse IA active")
    
    async def _setup_analysis_context(self):
        """Configuration contexte analyse IA spécialisé"""
        if not self.llm_gateway:
            return
        
        analysis_context = {
            "role": "solution_analysis_expert",
            "domain": "software_solution_benchmarking",
            "capabilities": [
                "Solution architecture analysis",
                "Intelligent benchmarking", 
                "Comparative solution analysis",
                "Quality assessment",
                "Performance evaluation"
            ],
            "patterns": [
                "BENCHMARKING_INTELLIGENCE",
                "RESEARCH",
                "LLM_ENHANCED"
            ]
        }
        
        # Chargement expertise analyse depuis LLM
        try:
            response = await self.llm_gateway.process_request(
                "Load solution analysis expertise",
                context=analysis_context
            )
            
            if response.get("success"):
                self.analysis_context["domain_expertise"] = response.get("expertise", [])
                self.logger.info("🧠 Expertise analyse IA chargée")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement contexte IA: {e}")
    
    async def analyze_solution_comprehensive(self, solution_path: str, 
                                           compare_with: List[str] = None) -> Dict[str, Any]:
        """Analyse complète solution avec benchmarking IA"""
        start_time = datetime.now()
        
        self.logger.info(f"🔍 Analyse complète solution: {solution_path}")
        
        # Cache check
        cache_key = self._generate_cache_key(solution_path)
        if cache_key in self.analysis_cache and self.analysis_config["cache_results"]:
            self.logger.info("📋 Résultat depuis cache")
            return self.analysis_cache[cache_key]
        
        result = {
            "solution_path": solution_path,
            "analysis": {},
            "benchmark": {},
            "recommendations": [],
            "quality_assessment": {},
            "performance_metrics": {}
        }
        
        # 1. Analyse architecture
        result["analysis"] = await self.solution_analyzer.analyze_solution_architecture(
            solution_path
        )
        
        # 2. Benchmarking
        if self.analysis_config["benchmark_enabled"]:
            reference_solutions = []
            if compare_with:
                for ref_path in compare_with:
                    ref_analysis = await self.solution_analyzer.analyze_solution_architecture(ref_path)
                    reference_solutions.append(ref_analysis)
            
            result["benchmark"] = await self.benchmarking_engine.benchmark_solution(
                result["analysis"], reference_solutions
            )
        
        # 3. Assessment qualité IA
        if self.llm_gateway:
            try:
                quality_assessment = await self.llm_gateway.process_request(
                    "Provide comprehensive quality assessment",
                    context={
                        "role": "quality_assessment_expert",
                        "analysis": result["analysis"],
                        "benchmark": result["benchmark"],
                        "task": "holistic_quality_evaluation"
                    }
                )
                
                if quality_assessment.get("success"):
                    result["quality_assessment"] = quality_assessment.get("assessment", {})
                    result["recommendations"] = quality_assessment.get("recommendations", [])
                    
            except Exception as e:
                self.logger.warning(f"⚠️ Erreur assessment IA: {e}")
        
        # 4. Métriques performance
        execution_time = (datetime.now() - start_time).total_seconds()
        result["performance_metrics"] = {
            "analysis_time_seconds": execution_time,
            "cache_hit": False,
            "ai_enhancement_used": self.llm_gateway is not None
        }
        
        # Mise à jour métriques
        self.analysis_metrics["solutions_analyzed"] += 1
        self.analysis_metrics["processing_time_avg"] = (
            (self.analysis_metrics["processing_time_avg"] * 
             (self.analysis_metrics["solutions_analyzed"] - 1) + execution_time) /
            self.analysis_metrics["solutions_analyzed"]
        )
        
        if result["benchmark"].get("overall_score"):
            self.analysis_metrics["average_score"] = (
                (self.analysis_metrics["average_score"] * 
                 (self.analysis_metrics["solutions_analyzed"] - 1) + 
                 result["benchmark"]["overall_score"]) /
                self.analysis_metrics["solutions_analyzed"]
            )
        
        # Cache result
        if self.analysis_config["cache_results"]:
            self.analysis_cache[cache_key] = result
        
        return result
    
    def _generate_cache_key(self, solution_path: str) -> str:
        """Génération clé cache intelligente"""
        path_hash = hashlib.md5(solution_path.encode()).hexdigest()
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"{path_hash}_{timestamp}"
    
    async def compare_solutions_batch(self, solution_paths: List[str]) -> Dict[str, Any]:
        """Comparaison batch de solutions"""
        self.logger.info(f"📊 Comparaison batch: {len(solution_paths)} solutions")
        
        comparison_result = {
            "solutions": [],
            "rankings": [],
            "best_practices": [],
            "overall_insights": {}
        }
        
        # Analyse de toutes les solutions
        for solution_path in solution_paths:
            analysis = await self.analyze_solution_comprehensive(solution_path)
            comparison_result["solutions"].append(analysis)
        
        # Ranking intelligent
        solutions_with_scores = [
            (sol, sol["benchmark"].get("overall_score", 0))
            for sol in comparison_result["solutions"]
            if sol["benchmark"].get("overall_score")
        ]
        
        sorted_solutions = sorted(solutions_with_scores, key=lambda x: x[1], reverse=True)
        
        comparison_result["rankings"] = [
            {
                "rank": i + 1,
                "solution": sol[0]["solution_path"],
                "score": sol[1],
                "key_strengths": sol[0]["recommendations"][:3]
            }
            for i, sol in enumerate(sorted_solutions)
        ]
        
        # Insights globaux IA
        if self.llm_gateway:
            try:
                insights = await self.llm_gateway.process_request(
                    "Generate overall insights from solution comparison",
                    context={
                        "role": "solution_comparison_analyst",
                        "solutions": comparison_result["solutions"],
                        "rankings": comparison_result["rankings"],
                        "task": "strategic_insights_generation"
                    }
                )
                
                if insights.get("success"):
                    comparison_result["overall_insights"] = insights.get("insights", {})
                    comparison_result["best_practices"] = insights.get("best_practices", [])
                    
            except Exception as e:
                self.logger.warning(f"⚠️ Erreur insights IA: {e}")
        
        return comparison_result
    
    async def get_analysis_metrics(self) -> Dict[str, Any]:
        """Métriques analyse temps réel"""
        return {
            "analysis_metrics": self.analysis_metrics,
            "cache_status": {
                "analysis_cache_size": len(self.analysis_cache),
                "benchmark_cache_size": len(self.benchmark_cache)
            },
            "configuration": self.analysis_config,
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
            "analysis": {
                "solutions_analyzed": self.analysis_metrics["solutions_analyzed"],
                "average_score": self.analysis_metrics["average_score"],
                "processing_time_avg": self.analysis_metrics["processing_time_avg"]
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function pour compatibilité
def create_analyse_solution_chatgpt(**config) -> AgentAnalyseSolutionChatGPT_Enterprise:
    """Factory function pour créer l'agent"""
    return AgentAnalyseSolutionChatGPT_Enterprise(**config)

# Test standalone
async def main():
    """Test de l'agent Analyse Solution"""
    print("🔍 Test Agent Analyse Solution ChatGPT NextGeneration v5.3.0")
    
    agent = create_analyse_solution_chatgpt(agent_id="test_analysis")
    
    # Health check
    health = await agent.health_check()
    print(f"🏥 Health: {health['status']}")
    
    # Test analyse solution
    analysis = await agent.analyze_solution_comprehensive("/mnt/c/Dev/nextgeneration/agents")
    print(f"📊 Analysis: Score={analysis['benchmark'].get('overall_score', 0):.1f}")
    print(f"⚡ Analysis time: {analysis['performance_metrics']['analysis_time_seconds']:.2f}s")
    
    # Métriques
    metrics = await agent.get_analysis_metrics()
    print(f"📈 Solutions analyzed: {metrics['analysis_metrics']['solutions_analyzed']}")

if __name__ == "__main__":
    asyncio.run(main())