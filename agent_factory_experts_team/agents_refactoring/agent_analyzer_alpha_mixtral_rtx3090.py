#!/usr/bin/env python3
"""
[SEARCH] Agent Code Analyzer Alpha - Refactoring NextGeneration
Mission: Analyse approfondie fichiers god mode avec Mixtral RTX3090 local
Modle: mixtral:8x7b-instruct-v0.1-q3_k_m (RTX3090) - Qualit maximum
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
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Configuration RTX3090 OBLIGATOIRE
os.environ['CUDA_VISIBLE_DEVICES'] = '1'  # RTX 3090 uniquement
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

@dataclass
class CodeMetrics:
    """Mtriques complexit code"""
    file_path: str
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    functions_count: int
    classes_count: int
    cyclomatic_complexity: int
    coupling_score: float
    cohesion_score: float
    maintainability_index: float

@dataclass
class DependencyGraph:
    """Graphe dpendances"""
    file_path: str
    imports: List[str]
    internal_deps: List[str]
    external_deps: List[str]
    circular_deps: List[str]
    coupling_level: str  # LOW, MEDIUM, HIGH, CRITICAL

@dataclass
class RefactoringRecommendation:
    """Recommandation refactoring"""
    target_file: str
    issue_type: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    description: str
    recommended_action: str
    estimated_effort: str
    priority: int

@dataclass
class AnalysisResult:
    """Rsultat analyse complte"""
    timestamp: str
    agent_name: str
    model_used: str
    gpu_used: str
    files_analyzed: List[str]
    metrics: List[CodeMetrics]
    dependencies: List[DependencyGraph]
    recommendations: List[RefactoringRecommendation]
    hotspots: List[str]
    summary: Dict[str, Any]

class AgentCodeAnalyzerAlpha:
    """Agent analyseur code Alpha - Mixtral RTX3090"""
    
    def __init__(self):
        self.name = "Agent Code Analyzer Alpha"
        self.model = "mixtral:8x7b-instruct-v0.1-q3_k_m"  # RTX3090 Local
        self.mission = "Analyse approfondie fichiers god mode avec Mixtral RTX3090"
        self.version = "1.0.0"
        self.status = "INITIALIZING"
        
        # Configuration RTX3090
        self.ollama_url = "http://localhost:11434"
        self.gpu_device = "RTX 3090 (Device 1)"
        self.vram_usage = "92%"  # Mixtral utilise quasi-toute la VRAM
        self.expected_performance = "5.4 tokens/s"
        
        # Fichiers god mode  analyser
        self.project_root = Path.cwd()
        self.target_files = [
            "orchestrator/app/main.py",
            "orchestrator/app/agents/advanced_coordination.py",
            "orchestrator/app/performance/redis_cluster_manager.py", 
            "orchestrator/app/observability/monitoring.py"
        ]
        
        # Configuration analyse
        self.analysis_depth = "DEEP"  # Profondeur maximale avec Mixtral
        self.include_ast_analysis = True
        self.include_dependency_analysis = True
        self.include_complexity_metrics = True
        
    async def analyze_file_structure(self, file_path: Path) -> CodeMetrics:
        """Analyse structure et mtriques fichier"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            total_lines = len(lines)
            
            code_lines = 0
            comment_lines = 0
            blank_lines = 0
            
            for line in lines:
                line_stripped = line.strip()
                if not line_stripped:
                    blank_lines += 1
                elif line_stripped.startswith('#'):
                    comment_lines += 1
                else:
                    code_lines += 1
            
            # Analyse AST pour fonctions/classes
            try:
                tree = ast.parse(content)
                functions_count = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
                classes_count = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            except:
                functions_count = len(re.findall(r'^\s*def\s+\w+', content, re.MULTILINE))
                classes_count = len(re.findall(r'^\s*class\s+\w+', content, re.MULTILINE))
            
            # Complexit cyclomatique (approximation)
            cyclomatic_complexity = self._calculate_cyclomatic_complexity(content)
            
            # Scores approximatifs (seront affins par Mixtral)
            coupling_score = min(10.0, len(re.findall(r'import\s+\w+|from\s+\w+', content)) / 10)
            cohesion_score = max(1.0, 10.0 - (functions_count / classes_count if classes_count > 0 else functions_count / 10))
            
            # Index maintenabilit (approximation)
            maintainability_index = max(0, 100 - (total_lines / 100) - (cyclomatic_complexity / 10))
            
            return CodeMetrics(
                file_path=str(file_path),
                total_lines=total_lines,
                code_lines=code_lines,
                comment_lines=comment_lines,
                blank_lines=blank_lines,
                functions_count=functions_count,
                classes_count=classes_count,
                cyclomatic_complexity=cyclomatic_complexity,
                coupling_score=coupling_score,
                cohesion_score=cohesion_score,
                maintainability_index=maintainability_index
            )
            
        except Exception as e:
            print(f"[CROSS] Erreur analyse structure {file_path}: {e}")
            return None
    
    def _calculate_cyclomatic_complexity(self, content: str) -> int:
        """Calcule complexit cyclomatique approximative"""
        # Mots-cls augmentant complexit
        complexity_keywords = [
            r'\bif\b', r'\belif\b', r'\belse\b', r'\bwhile\b', 
            r'\bfor\b', r'\btry\b', r'\bexcept\b', r'\bwith\b',
            r'\band\b', r'\bor\b', r'\?', r'\breturn\b'
        ]
        
        complexity = 1  # Base
        for keyword in complexity_keywords:
            complexity += len(re.findall(keyword, content, re.IGNORECASE))
        
        return complexity
    
    async def analyze_dependencies(self, file_path: Path) -> DependencyGraph:
        """Analyse dpendances fichier"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extraction imports
            imports = re.findall(r'(?:from\s+(\S+)\s+)?import\s+([^\n#]+)', content)
            all_imports = []
            
            for from_module, import_items in imports:
                if from_module:
                    all_imports.append(f"from {from_module} import {import_items.strip()}")
                else:
                    all_imports.append(f"import {import_items.strip()}")
            
            # Classification dpendances
            internal_deps = []
            external_deps = []
            
            for imp in all_imports:
                if any(x in imp for x in ['orchestrator', '.app', 'app.']):
                    internal_deps.append(imp)
                else:
                    external_deps.append(imp)
            
            # Dtection dpendances circulaires (approximation)
            circular_deps = []
            if 'from .app' in content and 'from orchestrator.app' in content:
                circular_deps.append("Potentielle dpendance circulaire dtecte")
            
            # Niveau coupling
            total_deps = len(all_imports)
            if total_deps > 30:
                coupling_level = "CRITICAL"
            elif total_deps > 20:
                coupling_level = "HIGH"
            elif total_deps > 10:
                coupling_level = "MEDIUM"
            else:
                coupling_level = "LOW"
            
            return DependencyGraph(
                file_path=str(file_path),
                imports=all_imports,
                internal_deps=internal_deps,
                external_deps=external_deps,
                circular_deps=circular_deps,
                coupling_level=coupling_level
            )
            
        except Exception as e:
            print(f"[CROSS] Erreur analyse dpendances {file_path}: {e}")
            return None
    
    async def analyze_with_mixtral(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyse approfondie avec Mixtral RTX3090"""
        print(f"[SEARCH] Analyse Mixtral RTX3090: {file_path}")
        
        # Prompt spcialis pour analyse code
        prompt = f"""
Tu es un expert analyste de code utilisant Mixtral-8x7B sur RTX 3090.
Mission: Analyse approfondie pour refactoring architectural.

FICHIER  ANALYSER: {file_path}
TAILLE: {len(file_content)} caractres

CONTENU DU FICHIER:
```python
{file_content[:3000]}{'...' if len(file_content) > 3000 else ''}
```

ANALYSE REQUISE:

1. **COMPLEXIT ET STRUCTURE**
   - Complexit cyclomatique dtaille
   - Violations du Single Responsibility Principle
   - Couplage et cohsion
   - Points de douleur maintenabilit

2. **REFACTORING OPPORTUNITS**
   - Fonctions/classes candidates  l'extraction
   - Responsabilits  sparer
   - Patterns d'architecture recommands
   - Priorits de refactoring

3. **DPENDANCES ET ARCHITECTURE**
   - Dpendances problmatiques
   - Inversions de contrle possibles
   - Abstractions manquantes
   - Dcouplage recommand

4. **RECOMMANDATIONS CONCRTES**
   - Actions prioritaires (1-3)
   - Estimation effort (heures)
   - Risques identifis
   - Bnfices attendus

Fournis une analyse JSON structure avec mtriques prcises.
"""

        try:
            # Appel Mixtral RTX3090
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.2,  # Analyse prcise
                            "top_p": 0.9,
                            "num_ctx": 8192,  # Contexte large pour Mixtral
                            "num_gpu": 1
                        }
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    analysis = result.get("response", "")
                    
                    # Extraction mtriques depuis rponse Mixtral
                    return {
                        "file_path": file_path,
                        "mixtral_analysis": analysis,
                        "analysis_quality": "DEEP",
                        "model_performance": {
                            "model": self.model,
                            "gpu": self.gpu_device,
                            "vram_usage": self.vram_usage
                        }
                    }
                else:
                    raise Exception(f"Erreur Ollama: {response.status_code}")
                    
        except Exception as e:
            print(f"[CROSS] Erreur analyse Mixtral {file_path}: {e}")
            return {
                "file_path": file_path,
                "mixtral_analysis": f"Erreur analyse: {e}",
                "analysis_quality": "FAILED"
            }
    
    def generate_refactoring_recommendations(self, metrics: CodeMetrics, deps: DependencyGraph, mixtral_analysis: str) -> List[RefactoringRecommendation]:
        """Gnre recommandations refactoring"""
        recommendations = []
        
        # Recommandations bases sur mtriques
        if metrics.total_lines > 500:
            recommendations.append(RefactoringRecommendation(
                target_file=metrics.file_path,
                issue_type="TAILLE_FICHIER",
                severity="HIGH",
                description=f"Fichier trop volumineux: {metrics.total_lines} lignes",
                recommended_action="Diviser en modules spcialiss selon SRP",
                estimated_effort="2-3 jours",
                priority=1
            ))
        
        if metrics.functions_count > 20:
            recommendations.append(RefactoringRecommendation(
                target_file=metrics.file_path,
                issue_type="TROP_FONCTIONS", 
                severity="MEDIUM",
                description=f"Trop de fonctions: {metrics.functions_count}",
                recommended_action="Regrouper fonctions par domaine",
                estimated_effort="1-2 jours",
                priority=2
            ))
        
        if metrics.cyclomatic_complexity > 50:
            recommendations.append(RefactoringRecommendation(
                target_file=metrics.file_path,
                issue_type="COMPLEXITE_ELEVEE",
                severity="CRITICAL",
                description=f"Complexit cyclomatique: {metrics.cyclomatic_complexity}",
                recommended_action="Simplifier logique, extraire fonctions",
                estimated_effort="3-5 jours",
                priority=1
            ))
        
        # Recommandations dpendances
        if deps.coupling_level in ["HIGH", "CRITICAL"]:
            recommendations.append(RefactoringRecommendation(
                target_file=deps.file_path,
                issue_type="COUPLAGE_FORT",
                severity="HIGH" if deps.coupling_level == "HIGH" else "CRITICAL",
                description=f"Couplage {deps.coupling_level}: {len(deps.imports)} imports",
                recommended_action="Introduire dependency injection, abstractions",
                estimated_effort="2-4 jours",
                priority=1 if deps.coupling_level == "CRITICAL" else 2
            ))
        
        # Tri par priorit
        recommendations.sort(key=lambda x: x.priority)
        
        return recommendations
    
    def identify_hotspots(self, all_metrics: List[CodeMetrics]) -> List[str]:
        """Identifie hotspots critiques"""
        hotspots = []
        
        for metrics in all_metrics:
            score = 0
            issues = []
            
            # Scoring hotspots
            if metrics.total_lines > 1000:
                score += 3
                issues.append(f"Fichier norme ({metrics.total_lines} lignes)")
            
            if metrics.cyclomatic_complexity > 100:
                score += 3
                issues.append(f"Complexit extrme ({metrics.cyclomatic_complexity})")
            
            if metrics.functions_count > 30:
                score += 2
                issues.append(f"Trop de fonctions ({metrics.functions_count})")
            
            if metrics.maintainability_index < 20:
                score += 2
                issues.append(f"Maintenabilit faible ({metrics.maintainability_index:.1f})")
            
            if score >= 5:  # Hotspot critique
                hotspot = f" HOTSPOT CRITIQUE: {metrics.file_path} (Score: {score})"
                hotspot += f"\n   Issues: {', '.join(issues)}"
                hotspots.append(hotspot)
        
        return hotspots
    
    async def execute_mission(self) -> AnalysisResult:
        """Excute mission analyse Alpha avec Mixtral RTX3090"""
        print(f"[ROCKET] {self.name} - Dmarrage analyse Mixtral RTX3090")
        print(f" GPU: {self.gpu_device}")
        print(f"[ROBOT] Modle: {self.model}")
        print(f"[CHART] VRAM attendue: {self.vram_usage}")
        
        try:
            self.status = "ACTIVE"
            start_time = time.time()
            
            all_metrics = []
            all_dependencies = []
            all_mixtral_analyses = []
            files_analyzed = []
            
            # Analyse chaque fichier god mode
            for target_file in self.target_files:
                file_path = self.project_root / target_file
                
                if not file_path.exists():
                    print(f" Fichier introuvable: {file_path}")
                    continue
                
                print(f"[SEARCH] Analyse: {target_file}")
                
                # Analyse structure
                metrics = await self.analyze_file_structure(file_path)
                if metrics:
                    all_metrics.append(metrics)
                
                # Analyse dpendances
                deps = await self.analyze_dependencies(file_path)
                if deps:
                    all_dependencies.append(deps)
                
                # Analyse Mixtral RTX3090
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    mixtral_analysis = await self.analyze_with_mixtral(content, str(target_file))
                    all_mixtral_analyses.append(mixtral_analysis)
                    
                except Exception as e:
                    print(f"[CROSS] Erreur lecture {file_path}: {e}")
                
                files_analyzed.append(str(target_file))
                
                # Pause entre analyses pour viter surcharge
                await asyncio.sleep(1)
            
            # Gnration recommandations globales
            all_recommendations = []
            for i, metrics in enumerate(all_metrics):
                if i < len(all_dependencies):
                    deps = all_dependencies[i]
                    mixtral_analysis = all_mixtral_analyses[i]["mixtral_analysis"] if i < len(all_mixtral_analyses) else ""
                    
                    recommendations = self.generate_refactoring_recommendations(metrics, deps, mixtral_analysis)
                    all_recommendations.extend(recommendations)
            
            # Identification hotspots
            hotspots = self.identify_hotspots(all_metrics)
            
            # Summary global
            total_lines = sum(m.total_lines for m in all_metrics)
            avg_complexity = sum(m.cyclomatic_complexity for m in all_metrics) / len(all_metrics) if all_metrics else 0
            critical_issues = len([r for r in all_recommendations if r.severity == "CRITICAL"])
            
            summary = {
                "files_count": len(files_analyzed),
                "total_lines_analyzed": total_lines,
                "average_complexity": round(avg_complexity, 1),
                "critical_issues": critical_issues,
                "recommendations_count": len(all_recommendations),
                "hotspots_count": len(hotspots),
                "analysis_duration": round(time.time() - start_time, 2),
                "model_performance": {
                    "model": self.model,
                    "gpu": self.gpu_device,
                    "expected_tokens_per_sec": self.expected_performance
                }
            }
            
            # Rsultat final
            result = AnalysisResult(
                timestamp=datetime.now().isoformat(),
                agent_name=self.name,
                model_used=self.model,
                gpu_used=self.gpu_device,
                files_analyzed=files_analyzed,
                metrics=all_metrics,
                dependencies=all_dependencies,
                recommendations=all_recommendations,
                hotspots=hotspots,
                summary=summary
            )
            
            self.status = "SUCCESS"
            
            print(f" Analyse Alpha Mixtral TERMINE")
            print(f"[CHART] {len(files_analyzed)} fichiers, {total_lines:,} lignes analyses")
            print(f" {len(hotspots)} hotspots critiques identifis")
            print(f" {critical_issues} issues critiques dtects")
            print(f" Dure: {summary['analysis_duration']}s")
            
            return result
            
        except Exception as e:
            self.status = "FAILED"
            print(f"[CROSS] chec analyse Alpha: {e}")
            
            # Rsultat d'erreur
            return AnalysisResult(
                timestamp=datetime.now().isoformat(),
                agent_name=self.name,
                model_used=self.model,
                gpu_used=self.gpu_device,
                files_analyzed=[],
                metrics=[],
                dependencies=[],
                recommendations=[],
                hotspots=[],
                summary={"error": str(e), "status": "FAILED"}
            )
    
    def save_analysis_report(self, result: AnalysisResult, output_file: str = None):
        """Sauvegarde rapport analyse"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"refactoring_workspace/analysis_alpha_mixtral_{timestamp}.json"
        
        # Conversion en dict pour JSON
        result_dict = asdict(result)
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)
        
        print(f"[DOCUMENT] Rapport sauvegard: {output_path}")

if __name__ == "__main__":
    # Test agent analyzer alpha
    agent = AgentCodeAnalyzerAlpha()
    
    async def main():
        result = await agent.execute_mission()
        agent.save_analysis_report(result)
        
        print(f"\n[CHART] RSULTAT ANALYSE ALPHA MIXTRAL:")
        print(f"Status: {agent.status}")
        print(f"Modle: {result.model_used}")
        print(f"GPU: {result.gpu_used}")
        print(f"Fichiers: {len(result.files_analyzed)}")
        print(f"Hotspots: {len(result.hotspots)}")
        print(f"Recommandations: {len(result.recommendations)}")
    
    asyncio.run(main()) 