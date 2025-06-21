#!/usr/bin/env python3
"""
[LIGHTNING] Agent Code Analyzer Beta - Refactoring NextGeneration 
Mission: Analyse rapide et oriente code avec Qwen-Coder RTX3090 local
Modle: qwen2.5-coder:1.5b (RTX3090) - Spcialiste code ultra-rapide
"""

import os
import sys
import json
import ast
import re
import time
import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict

# Configuration RTX3090 OBLIGATOIRE
os.environ['CUDA_VISIBLE_DEVICES'] = '1'  # RTX 3090 uniquement
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

@dataclass
class CodePattern:
    """Pattern code dtect"""
    file_path: str
    pattern_type: str
    line_number: int
    description: str
    severity: str
    refactoring_suggestion: str

@dataclass
class FunctionAnalysis:
    """Analyse fonction spcifique"""
    function_name: str
    file_path: str
    start_line: int
    end_line: int
    complexity: int
    parameters_count: int
    lines_count: int
    responsibilities: List[str]
    extraction_candidate: bool
    suggested_module: str

@dataclass
class ClassAnalysis:
    """Analyse classe spcifique"""
    class_name: str
    file_path: str
    start_line: int
    end_line: int
    methods_count: int
    properties_count: int
    responsibilities: List[str]
    srp_violations: List[str]
    split_suggestions: List[str]

@dataclass
class CodeSmells:
    """Code smells dtects"""
    file_path: str
    long_methods: List[str]
    god_classes: List[str] 
    duplicate_code: List[str]
    complex_conditionals: List[str]
    deep_nesting: List[str]
    magic_numbers: List[str]

@dataclass
class RefactoringStrategy:
    """Stratgie refactoring"""
    target_file: str
    strategy_type: str  # EXTRACT_MODULE, SPLIT_CLASS, EXTRACT_FUNCTION, etc.
    priority: int
    description: str
    steps: List[str]
    estimated_hours: float
    risk_level: str
    expected_lines_reduction: int

@dataclass
class BetaAnalysisResult:
    """Rsultat analyse Beta Qwen-Coder"""
    timestamp: str
    agent_name: str
    model_used: str
    gpu_used: str
    files_analyzed: List[str]
    code_patterns: List[CodePattern]
    functions_analysis: List[FunctionAnalysis]
    classes_analysis: List[ClassAnalysis]
    code_smells: List[CodeSmells]
    refactoring_strategies: List[RefactoringStrategy]
    performance_metrics: Dict[str, Any]
    summary: Dict[str, Any]

class AgentCodeAnalyzerBeta:
    """Agent analyseur code Beta - Qwen-Coder RTX3090"""
    
    def __init__(self):
        self.name = "Agent Code Analyzer Beta"
        self.model = "qwen2.5-coder:1.5b"  # RTX3090 Local ultra-rapide
        self.mission = "Analyse rapide et oriente code avec Qwen-Coder RTX3090"
        self.version = "1.0.0"
        self.status = "INITIALIZING"
        
        # Configuration RTX3090
        self.ollama_url = "http://localhost:11434"
        self.gpu_device = "RTX 3090 (Device 1)"
        self.vram_usage = "4%"  # Qwen-Coder trs lger
        self.expected_performance = "8.2 tokens/s"
        
        # Fichiers god mode  analyser
        self.project_root = Path.cwd()
        self.target_files = [
            "orchestrator/app/main.py",
            "orchestrator/app/agents/advanced_coordination.py",
            "orchestrator/app/performance/redis_cluster_manager.py",
            "orchestrator/app/observability/monitoring.py"
        ]
        
        # Configuration analyse rapide et spcialise
        self.analysis_focus = "CODE_QUALITY"  # Focus sur qualit code
        self.extraction_threshold = 15  # Seuil extraction fonction (lignes)
        self.complexity_threshold = 10  # Seuil complexit critique
        self.class_methods_threshold = 20  # Seuil split classe
        
        # Patterns code  dtecter
        self.code_patterns = {
            "god_function": r"def\s+\w+\(.*?\):",
            "nested_if": r"if\s+.*:\s*\n\s+if\s+.*:",
            "magic_number": r"\b(?<![\w.])\d{2,}\b",
            "long_parameter_list": r"def\s+\w+\([^)]{50,}\):",
            "duplicate_try_except": r"try:\s*\n.*?except.*?:\s*\n.*?try:\s*\n.*?except"
        }
    
    async def analyze_ast_structure(self, file_path: Path) -> Tuple[List[FunctionAnalysis], List[ClassAnalysis]]:
        """Analyse AST dtaille pour fonctions et classes"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            lines = content.split('\n')
            
            functions_analysis = []
            classes_analysis = []
            
            # Analyse fonctions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_analysis = await self._analyze_function(node, lines, str(file_path))
                    if func_analysis:
                        functions_analysis.append(func_analysis)
                
                elif isinstance(node, ast.ClassDef):
                    class_analysis = await self._analyze_class(node, lines, str(file_path))
                    if class_analysis:
                        classes_analysis.append(class_analysis)
            
            return functions_analysis, classes_analysis
            
        except Exception as e:
            print(f"[CROSS] Erreur analyse AST {file_path}: {e}")
            return [], []
    
    async def _analyze_function(self, node: ast.FunctionDef, lines: List[str], file_path: str) -> FunctionAnalysis:
        """Analyse dtaille fonction"""
        start_line = node.lineno
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 10
        
        # Calcul complexit cyclomatique
        complexity = 1  # Base
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        # Nombre paramtres
        parameters_count = len(node.args.args)
        
        # Nombre lignes
        lines_count = end_line - start_line + 1
        
        # Dtection responsabilits (approximation)
        func_content = '\n'.join(lines[start_line-1:end_line])
        responsibilities = []
        
        if 'db.' in func_content or 'query' in func_content:
            responsibilities.append("DATABASE")
        if 'request' in func_content or 'response' in func_content:
            responsibilities.append("HTTP")
        if 'log' in func_content or 'print' in func_content:
            responsibilities.append("LOGGING")
        if 'validate' in func_content or 'check' in func_content:
            responsibilities.append("VALIDATION")
        if 'transform' in func_content or 'convert' in func_content:
            responsibilities.append("TRANSFORMATION")
        
        # Candidat extraction ?
        extraction_candidate = (
            lines_count > self.extraction_threshold or 
            complexity > self.complexity_threshold or
            len(responsibilities) > 1
        )
        
        # Module suggr
        suggested_module = self._suggest_module_for_function(node.name, responsibilities)
        
        return FunctionAnalysis(
            function_name=node.name,
            file_path=file_path,
            start_line=start_line,
            end_line=end_line,
            complexity=complexity,
            parameters_count=parameters_count,
            lines_count=lines_count,
            responsibilities=responsibilities,
            extraction_candidate=extraction_candidate,
            suggested_module=suggested_module
        )
    
    async def _analyze_class(self, node: ast.ClassDef, lines: List[str], file_path: str) -> ClassAnalysis:
        """Analyse dtaille classe"""
        start_line = node.lineno
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 50
        
        # Comptage mthodes et proprits
        methods_count = 0
        properties_count = 0
        
        for child in node.body:
            if isinstance(child, ast.FunctionDef):
                if child.name.startswith('_') and not child.name.startswith('__'):
                    properties_count += 1
                else:
                    methods_count += 1
        
        # Dtection responsabilits classe
        class_content = '\n'.join(lines[start_line-1:end_line])
        responsibilities = []
        
        if any(word in class_content for word in ['database', 'query', 'sql']):
            responsibilities.append("DATABASE")
        if any(word in class_content for word in ['request', 'response', 'api']):
            responsibilities.append("HTTP_API")
        if any(word in class_content for word in ['validate', 'check', 'verify']):
            responsibilities.append("VALIDATION")
        if any(word in class_content for word in ['log', 'monitor', 'metric']):
            responsibilities.append("MONITORING")
        if any(word in class_content for word in ['cache', 'redis', 'storage']):
            responsibilities.append("CACHING")
        if any(word in class_content for word in ['config', 'setting', 'env']):
            responsibilities.append("CONFIGURATION")
        
        # Violations SRP
        srp_violations = []
        if len(responsibilities) > 2:
            srp_violations.append(f"Multiple responsabilits: {', '.join(responsibilities)}")
        if methods_count > self.class_methods_threshold:
            srp_violations.append(f"Trop de mthodes: {methods_count}")
        
        # Suggestions split
        split_suggestions = []
        if "DATABASE" in responsibilities and len(responsibilities) > 1:
            split_suggestions.append(f"{node.name}Repository (responsabilit DATABASE)")
        if "HTTP_API" in responsibilities and len(responsibilities) > 1:
            split_suggestions.append(f"{node.name}Controller (responsabilit HTTP_API)")
        if "VALIDATION" in responsibilities and len(responsibilities) > 1:
            split_suggestions.append(f"{node.name}Validator (responsabilit VALIDATION)")
        
        return ClassAnalysis(
            class_name=node.name,
            file_path=file_path,
            start_line=start_line,
            end_line=end_line,
            methods_count=methods_count,
            properties_count=properties_count,
            responsibilities=responsibilities,
            srp_violations=srp_violations,
            split_suggestions=split_suggestions
        )
    
    def _suggest_module_for_function(self, func_name: str, responsibilities: List[str]) -> str:
        """Suggre module appropri pour fonction"""
        if "DATABASE" in responsibilities:
            return "repositories"
        elif "HTTP" in responsibilities:
            return "controllers" 
        elif "VALIDATION" in responsibilities:
            return "validators"
        elif "TRANSFORMATION" in responsibilities:
            return "transformers"
        elif "LOGGING" in responsibilities:
            return "utils"
        else:
            return "services"
    
    async def detect_code_patterns(self, file_path: Path) -> List[CodePattern]:
        """Dtection patterns code problmatiques"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            patterns = []
            
            # Pattern: God Function (fonction trop longue)
            current_func = None
            func_start = 0
            func_lines = 0
            
            for i, line in enumerate(lines):
                if re.match(r'^\s*def\s+\w+', line):
                    # Fin fonction prcdente
                    if current_func and func_lines > 30:
                        patterns.append(CodePattern(
                            file_path=str(file_path),
                            pattern_type="GOD_FUNCTION",
                            line_number=func_start,
                            description=f"Fonction {current_func} trop longue: {func_lines} lignes",
                            severity="HIGH",
                            refactoring_suggestion="Diviser en fonctions plus petites"
                        ))
                    
                    # Nouvelle fonction
                    current_func = re.search(r'def\s+(\w+)', line).group(1)
                    func_start = i + 1
                    func_lines = 0
                
                if current_func:
                    func_lines += 1
            
            # Pattern: Nesting profond
            for i, line in enumerate(lines):
                indent_level = (len(line) - len(line.lstrip())) // 4
                if indent_level > 4:
                    patterns.append(CodePattern(
                        file_path=str(file_path),
                        pattern_type="DEEP_NESTING",
                        line_number=i + 1,
                        description=f"Nesting trop profond: niveau {indent_level}",
                        severity="MEDIUM",
                        refactoring_suggestion="Extraire mthodes, simplifier logique"
                    ))
            
            # Pattern: Magic Numbers
            for i, line in enumerate(lines):
                magic_numbers = re.findall(r'\b(?<![\w.])\d{2,}\b', line)
                for number in magic_numbers:
                    if number not in ['100', '200', '404', '500']:  # Exclus codes HTTP courants
                        patterns.append(CodePattern(
                            file_path=str(file_path),
                            pattern_type="MAGIC_NUMBER",
                            line_number=i + 1,
                            description=f"Magic number dtect: {number}",
                            severity="LOW",
                            refactoring_suggestion="Remplacer par constante nomme"
                        ))
            
            return patterns
            
        except Exception as e:
            print(f"[CROSS] Erreur dtection patterns {file_path}: {e}")
            return []
    
    async def detect_code_smells(self, file_path: Path) -> CodeSmells:
        """Dtection code smells"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Long methods
            long_methods = []
            current_method = None
            method_lines = 0
            
            for line in lines:
                if re.match(r'^\s*def\s+\w+', line):
                    if current_method and method_lines > 20:
                        long_methods.append(f"{current_method} ({method_lines} lignes)")
                    
                    current_method = re.search(r'def\s+(\w+)', line).group(1)
                    method_lines = 0
                
                method_lines += 1
            
            # God classes (approximation)
            god_classes = []
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods_count = len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                    if methods_count > 15:
                        god_classes.append(f"{node.name} ({methods_count} mthodes)")
            
            # Duplicate code (approximation simple)
            duplicate_code = []
            line_counts = {}
            for i, line in enumerate(lines):
                stripped = line.strip()
                if len(stripped) > 10 and not stripped.startswith('#'):
                    if stripped in line_counts:
                        line_counts[stripped].append(i + 1)
                    else:
                        line_counts[stripped] = [i + 1]
            
            for line, occurrences in line_counts.items():
                if len(occurrences) > 2:
                    duplicate_code.append(f"Ligne duplique {len(occurrences)} fois: {line[:50]}...")
            
            # Complex conditionals
            complex_conditionals = []
            for i, line in enumerate(lines):
                if 'if' in line and (' and ' in line or ' or ' in line):
                    complexity = line.count(' and ') + line.count(' or ') + 1
                    if complexity > 3:
                        complex_conditionals.append(f"Ligne {i+1}: condition complexe ({complexity} clauses)")
            
            # Deep nesting
            deep_nesting = []
            for i, line in enumerate(lines):
                indent = (len(line) - len(line.lstrip())) // 4
                if indent > 4:
                    deep_nesting.append(f"Ligne {i+1}: nesting niveau {indent}")
            
            # Magic numbers
            magic_numbers = []
            for i, line in enumerate(lines):
                numbers = re.findall(r'\b\d{2,}\b', line)
                for num in numbers:
                    if num not in ['100', '200', '404', '500']:
                        magic_numbers.append(f"Ligne {i+1}: {num}")
            
            return CodeSmells(
                file_path=str(file_path),
                long_methods=long_methods[:5],  # Top 5
                god_classes=god_classes,
                duplicate_code=duplicate_code[:5],  # Top 5
                complex_conditionals=complex_conditionals[:5],  # Top 5
                deep_nesting=deep_nesting[:5],  # Top 5
                magic_numbers=magic_numbers[:5]  # Top 5
            )
            
        except Exception as e:
            print(f"[CROSS] Erreur dtection code smells {file_path}: {e}")
            return CodeSmells(str(file_path), [], [], [], [], [], [])
    
    async def analyze_with_qwen_coder(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyse spcialise code avec Qwen-Coder RTX3090"""
        print(f"[LIGHTNING] Analyse Qwen-Coder RTX3090: {file_path}")
        
        # Prompt spcialis pour analyse code rapide
        prompt = f"""
Tu es Qwen-Coder, expert dveloppeur ultra-rapide sur RTX 3090.
Mission: Analyse code rapide pour refactoring immdiat.

FICHIER: {file_path}
TAILLE: {len(file_content)} caractres

CODE  ANALYSER:
```python
{file_content[:2000]}{'...' if len(file_content) > 2000 else ''}
```

ANALYSE RAPIDE REQUISE:

1. **EXTRACTION DE FONCTIONS**
   - Fonctions candidates extraction (>15 lignes)
   - Blocs code rptitifs
   - Logique mtier  isoler

2. **SPLIT DE CLASSES** 
   - Classes trop larges (>20 mthodes)
   - Responsabilits multiples dtectes
   - Violations Single Responsibility

3. **REFACTORING IMMDIAT**
   - Top 3 actions prioritaires
   - Gains estims (lignes rduites)
   - Modules cibles suggrs

4. **CODE PATTERNS**
   - Anti-patterns dtects
   - Best practices manquantes
   - Optimisations rapides

Fournis rponse JSON concise et actionnable.
"""

        try:
            # Appel Qwen-Coder RTX3090 
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.1,  # Code prcis
                            "top_p": 0.9,
                            "num_ctx": 4096,  # Contexte adapt
                            "num_gpu": 1
                        }
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    analysis = result.get("response", "")
                    
                    return {
                        "file_path": file_path,
                        "qwen_analysis": analysis,
                        "analysis_speed": "ULTRA_FAST",
                        "model_performance": {
                            "model": self.model,
                            "gpu": self.gpu_device,
                            "vram_usage": self.vram_usage,
                            "expected_tokens_per_sec": self.expected_performance
                        }
                    }
                else:
                    raise Exception(f"Erreur Ollama: {response.status_code}")
                    
        except Exception as e:
            print(f"[CROSS] Erreur analyse Qwen-Coder {file_path}: {e}")
            return {
                "file_path": file_path,
                "qwen_analysis": f"Erreur analyse: {e}",
                "analysis_speed": "FAILED"
            }
    
    def generate_refactoring_strategies(self, 
                                     functions: List[FunctionAnalysis],
                                     classes: List[ClassAnalysis],
                                     patterns: List[CodePattern],
                                     smells: CodeSmells) -> List[RefactoringStrategy]:
        """Gnre stratgies refactoring prioritaires"""
        strategies = []
        
        # Stratgie 1: Extraction fonctions
        extraction_candidates = [f for f in functions if f.extraction_candidate]
        if extraction_candidates:
            total_lines_reduction = sum(f.lines_count for f in extraction_candidates)
            strategies.append(RefactoringStrategy(
                target_file=extraction_candidates[0].file_path,
                strategy_type="EXTRACT_FUNCTIONS",
                priority=1,
                description=f"Extraire {len(extraction_candidates)} fonctions voluminoses/complexes",
                steps=[
                    "1. Identifier responsabilits de chaque fonction",
                    "2. Crer modules spcialiss (services, repositories, utils)",
                    "3. Extraire fonctions vers modules appropris",
                    "4. Mettre  jour imports et dpendances"
                ],
                estimated_hours=len(extraction_candidates) * 0.5,
                risk_level="LOW",
                expected_lines_reduction=int(total_lines_reduction * 0.3)
            ))
        
        # Stratgie 2: Split classes
        split_candidates = [c for c in classes if c.srp_violations]
        if split_candidates:
            strategies.append(RefactoringStrategy(
                target_file=split_candidates[0].file_path,
                strategy_type="SPLIT_CLASSES",
                priority=2,
                description=f"Diviser {len(split_candidates)} classes violant SRP",
                steps=[
                    "1. Analyser responsabilits de chaque classe",
                    "2. Crer classes spcialises par responsabilit",
                    "3. Extraire mthodes vers nouvelles classes",
                    "4. Implmenter composition/injection dpendances"
                ],
                estimated_hours=len(split_candidates) * 2.0,
                risk_level="MEDIUM",
                expected_lines_reduction=sum(c.methods_count for c in split_candidates) * 10
            ))
        
        # Stratgie 3: Nettoyage code smells
        total_smells = (len(smells.long_methods) + len(smells.complex_conditionals) + 
                       len(smells.deep_nesting) + len(smells.magic_numbers))
        if total_smells > 5:
            strategies.append(RefactoringStrategy(
                target_file=smells.file_path,
                strategy_type="CLEAN_CODE_SMELLS",
                priority=3,
                description=f"Nettoyer {total_smells} code smells dtects",
                steps=[
                    "1. Simplifier mthodes longues",
                    "2. Extraire conditions complexes",
                    "3. Rduire nesting avec early returns",
                    "4. Remplacer magic numbers par constantes"
                ],
                estimated_hours=total_smells * 0.2,
                risk_level="LOW",
                expected_lines_reduction=total_smells * 2
            ))
        
        # Tri par priorit
        strategies.sort(key=lambda x: x.priority)
        
        return strategies
    
    async def execute_mission(self) -> BetaAnalysisResult:
        """Excute mission analyse Beta avec Qwen-Coder RTX3090"""
        print(f"[ROCKET] {self.name} - Dmarrage analyse Qwen-Coder RTX3090")
        print(f" GPU: {self.gpu_device}")
        print(f"[ROBOT] Modle: {self.model}")
        print(f"[LIGHTNING] Performance attendue: {self.expected_performance}")
        
        try:
            self.status = "ACTIVE"
            start_time = time.time()
            
            all_functions = []
            all_classes = []
            all_patterns = []
            all_smells = []
            all_qwen_analyses = []
            files_analyzed = []
            
            # Analyse rapide chaque fichier
            for target_file in self.target_files:
                file_path = self.project_root / target_file
                
                if not file_path.exists():
                    print(f" Fichier introuvable: {file_path}")
                    continue
                
                print(f"[LIGHTNING] Analyse rapide: {target_file}")
                
                # Analyse AST
                functions, classes = await self.analyze_ast_structure(file_path)
                all_functions.extend(functions)
                all_classes.extend(classes)
                
                # Dtection patterns
                patterns = await self.detect_code_patterns(file_path)
                all_patterns.extend(patterns)
                
                # Dtection code smells
                smells = await self.detect_code_smells(file_path)
                all_smells.append(smells)
                
                # Analyse Qwen-Coder RTX3090
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    qwen_analysis = await self.analyze_with_qwen_coder(content, str(target_file))
                    all_qwen_analyses.append(qwen_analysis)
                    
                except Exception as e:
                    print(f"[CROSS] Erreur lecture {file_path}: {e}")
                
                files_analyzed.append(str(target_file))
                
                # Pause courte (Qwen-Coder est rapide)
                await asyncio.sleep(0.5)
            
            # Gnration stratgies refactoring
            refactoring_strategies = []
            for i, file_analyzed in enumerate(files_analyzed):
                file_functions = [f for f in all_functions if f.file_path.endswith(file_analyzed)]
                file_classes = [c for c in all_classes if c.file_path.endswith(file_analyzed)]
                file_patterns = [p for p in all_patterns if p.file_path.endswith(file_analyzed)]
                file_smells = all_smells[i] if i < len(all_smells) else CodeSmells("", [], [], [], [], [], [])
                
                strategies = self.generate_refactoring_strategies(
                    file_functions, file_classes, file_patterns, file_smells
                )
                refactoring_strategies.extend(strategies)
            
            # Mtriques performance
            analysis_duration = time.time() - start_time
            performance_metrics = {
                "analysis_duration": round(analysis_duration, 2),
                "files_per_second": round(len(files_analyzed) / analysis_duration, 2),
                "model": self.model,
                "gpu": self.gpu_device,
                "vram_usage": self.vram_usage,
                "tokens_per_second": self.expected_performance
            }
            
            # Summary
            extraction_candidates = len([f for f in all_functions if f.extraction_candidate])
            split_candidates = len([c for c in all_classes if c.srp_violations])
            total_patterns = len(all_patterns)
            
            summary = {
                "files_analyzed": len(files_analyzed),
                "functions_analyzed": len(all_functions),
                "classes_analyzed": len(all_classes), 
                "extraction_candidates": extraction_candidates,
                "split_candidates": split_candidates,
                "patterns_detected": total_patterns,
                "strategies_generated": len(refactoring_strategies),
                "analysis_speed": "ULTRA_FAST",
                "performance": performance_metrics
            }
            
            # Rsultat final
            result = BetaAnalysisResult(
                timestamp=datetime.now().isoformat(),
                agent_name=self.name,
                model_used=self.model,
                gpu_used=self.gpu_device,
                files_analyzed=files_analyzed,
                code_patterns=all_patterns,
                functions_analysis=all_functions,
                classes_analysis=all_classes,
                code_smells=all_smells,
                refactoring_strategies=refactoring_strategies,
                performance_metrics=performance_metrics,
                summary=summary
            )
            
            self.status = "SUCCESS"
            
            print(f" Analyse Beta Qwen-Coder TERMINE")
            print(f"[LIGHTNING] {len(files_analyzed)} fichiers analyss en {analysis_duration:.1f}s")
            print(f"[TOOL] {extraction_candidates} fonctions candidates extraction")
            print(f" {split_candidates} classes candidates split")
            print(f"[TARGET] {len(refactoring_strategies)} stratgies gnres")
            
            return result
            
        except Exception as e:
            self.status = "FAILED"
            print(f"[CROSS] chec analyse Beta: {e}")
            
            # Rsultat d'erreur
            return BetaAnalysisResult(
                timestamp=datetime.now().isoformat(),
                agent_name=self.name,
                model_used=self.model,
                gpu_used=self.gpu_device,
                files_analyzed=[],
                code_patterns=[],
                functions_analysis=[],
                classes_analysis=[],
                code_smells=[],
                refactoring_strategies=[],
                performance_metrics={"error": str(e)},
                summary={"error": str(e), "status": "FAILED"}
            )
    
    def save_analysis_report(self, result: BetaAnalysisResult, output_file: str = None):
        """Sauvegarde rapport analyse"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"refactoring_workspace/analysis_beta_qwen_{timestamp}.json"
        
        # Conversion en dict pour JSON
        result_dict = asdict(result)
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)
        
        print(f"[DOCUMENT] Rapport sauvegard: {output_path}")

if __name__ == "__main__":
    # Test agent analyzer beta
    agent = AgentCodeAnalyzerBeta()
    
    async def main():
        result = await agent.execute_mission()
        agent.save_analysis_report(result)
        
        print(f"\n[CHART] RSULTAT ANALYSE BETA QWEN-CODER:")
        print(f"Status: {agent.status}")
        print(f"Modle: {result.model_used}")
        print(f"GPU: {result.gpu_used}")
        print(f"Fichiers: {len(result.files_analyzed)}")
        print(f"Fonctions: {len(result.functions_analysis)}")
        print(f"Classes: {len(result.classes_analysis)}")
        print(f"Stratgies: {len(result.refactoring_strategies)}")
    
    asyncio.run(main()) 



