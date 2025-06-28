#!/usr/bin/env python3
"""
[TARGET] Agent Analyzer Alpha - Claude Sonnet 4
[SEARCH] Analyse approfondie des fichiers god mode avec Claude Sonnet 4
[LIGHTNING] Phase 1 Refactoring NextGeneration - Cloud API
"""

import os
import ast
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import anthropic

# Configuration .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print(" python-dotenv non install, utilisation variables systme")

@dataclass
class CodeMetrics:
    """Mtriques de complexit du code"""
    lines_of_code: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    nesting_depth: int
    number_of_functions: int
    number_of_classes: int
    god_class_score: float

@dataclass
class DependencyGraph:
    """Graphe des dpendances"""
    imports: List[str]
    internal_dependencies: List[str]
    external_dependencies: List[str]
    circular_dependencies: List[str]
    coupling_score: float

@dataclass
class RefactoringRecommendation:
    """Recommandations de refactoring"""
    priority: str  # HIGH, MEDIUM, LOW
    type: str  # EXTRACT_CLASS, EXTRACT_METHOD, SPLIT_FILE, etc.
    description: str
    impact: str
    effort: str
    affected_lines: List[int]

class AgentAnalyzerAlphaClaudeSonnet4:
    """
    [TARGET] Agent Analyzer Alpha - Claude Sonnet 4
    
    Mission:
    - Analyse approfondie avec AST
    - Mtriques de complexit avances
    - Dtection des hotspots critiques
    - Recommandations architecturales
    """
    
    def __init__(self):
        self.name = "Agent Analyzer Alpha - Claude Sonnet 4"
        self.model = "claude-3-5-sonnet-20241022"
        self.capabilities = [
            "Analyse AST Python",
            "Mtriques complexit",
            "Dtection god classes",
            "Recommandations architecturales",
            "Analyse dpendances"
        ]
        
        # Configuration Claude Sonnet 4 avec .env
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY manquante dans .env")
            
        self.client = anthropic.Anthropic(api_key=api_key)
        
        # Paramtres optimiss
        self.max_tokens = 4000
        self.temperature = 0.1  # Prcision maximale
        
        self.workspace = Path("refactoring_workspace")
        self.results_dir = self.workspace / "results" / "alpha_claude"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[ROBOT] {self.name} initialis avec Claude Sonnet 4")
        print(f" Modle: {self.model}")
        print(f" Cl API: {'[CHECK]' if api_key else '[CROSS]'}")
        print(f"[FOLDER] Workspace: {self.workspace}")

    async def analyze_file_deep(self, file_path: str) -> Dict[str, Any]:
        """
        [SEARCH] Analyse approfondie d'un fichier avec Claude Sonnet 4
        """
        print(f"\n[SEARCH] Agent Alpha - Analyse approfondie: {file_path}")
        
        try:
            # Lecture du fichier
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"[CHART] Taille fichier: {len(content)} caractres")
            
            # Analyse AST
            ast_analysis = self._analyze_ast(content)
            
            # Mtriques avec Claude Sonnet 4
            metrics = await self._calculate_metrics_claude(content, file_path)
            
            # Analyse des dpendances
            dependencies = self._analyze_dependencies(content)
            
            # Dtection des hotspots
            hotspots = await self._detect_hotspots_claude(content, file_path)
            
            # Recommandations Claude Sonnet 4
            recommendations = await self._generate_recommendations_claude(
                content, file_path, ast_analysis, metrics, dependencies
            )
            
            result = {
                "agent": self.name,
                "model": self.model,
                "file_path": file_path,
                "timestamp": datetime.now().isoformat(),
                "ast_analysis": ast_analysis,
                "metrics": asdict(metrics),
                "dependencies": asdict(dependencies),
                "hotspots": hotspots,
                "recommendations": [asdict(r) for r in recommendations],
                "summary": {
                    "god_class_score": metrics.god_class_score,
                    "complexity_level": self._get_complexity_level(metrics.cyclomatic_complexity),
                    "refactoring_priority": self._get_refactoring_priority(metrics, len(recommendations)),
                    "estimated_effort": self._estimate_effort(metrics, len(recommendations))
                }
            }
            
            # Sauvegarde
            output_file = self.results_dir / f"alpha_analysis_{Path(file_path).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"[CHECK] Analyse Alpha termine - Rsultats: {output_file}")
            return result
            
        except Exception as e:
            print(f"[CROSS] Erreur analyse Alpha: {str(e)}")
            return {"error": str(e), "file_path": file_path}

    def _analyze_ast(self, content: str) -> Dict[str, Any]:
        """Analyse AST dtaille"""
        try:
            tree = ast.parse(content)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "args_count": len(node.args.args),
                        "is_async": isinstance(node, ast.AsyncFunctionDef)
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods_count": len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.ImportFrom):
                        imports.append(f"from {node.module}")
                    else:
                        imports.extend([alias.name for alias in node.names])
            
            return {
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "total_nodes": len(list(ast.walk(tree)))
            }
            
        except Exception as e:
            return {"error": f"AST analysis failed: {str(e)}"}

    async def _calculate_metrics_claude(self, content: str, file_path: str) -> CodeMetrics:
        """Calcul des mtriques avec Claude Sonnet 4"""
        try:
            prompt = f"""
Analysez ce code Python et calculez les mtriques de complexit:

Fichier: {file_path}

```python
{content[:3000]}...
```

Calculez et retournez en JSON:
1. lines_of_code (lignes effectives)
2. cyclomatic_complexity (complexit cyclomatique)
3. cognitive_complexity (complexit cognitive)
4. nesting_depth (profondeur max imbrication)
5. number_of_functions
6. number_of_classes
7. god_class_score (0-1, 1=god class critique)

Format JSON strict requis.
"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse de la rponse JSON
            response_text = response.content[0].text
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            metrics_data = json.loads(response_text[json_start:json_end])
            
            return CodeMetrics(**metrics_data)
            
        except Exception as e:
            print(f" Mtriques par dfaut (erreur Claude): {str(e)}")
            lines = len([l for l in content.split('\n') if l.strip()])
            return CodeMetrics(
                lines_of_code=lines,
                cyclomatic_complexity=min(50, lines // 10),
                cognitive_complexity=min(40, lines // 12),
                nesting_depth=5,
                number_of_functions=content.count('def '),
                number_of_classes=content.count('class '),
                god_class_score=min(1.0, lines / 1000)
            )

    def _analyze_dependencies(self, content: str) -> DependencyGraph:
        """Analyse des dpendances"""
        try:
            tree = ast.parse(content)
            
            imports = []
            internal_deps = []
            external_deps = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                        if alias.name.startswith(('app.', 'orchestrator.')):
                            internal_deps.append(alias.name)
                        else:
                            external_deps.append(alias.name)
                            
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(f"from {node.module}")
                        if node.module.startswith(('app.', 'orchestrator.')):
                            internal_deps.append(node.module)
                        else:
                            external_deps.append(node.module)
            
            # Dtection circulaire simple
            circular_deps = []
            for dep in internal_deps:
                if dep.count('.') > 2:  # Heuristique simple
                    circular_deps.append(dep)
            
            coupling_score = len(internal_deps) / max(1, len(imports))
            
            return DependencyGraph(
                imports=imports,
                internal_dependencies=internal_deps,
                external_dependencies=external_deps,
                circular_dependencies=circular_deps,
                coupling_score=coupling_score
            )
            
        except Exception as e:
            return DependencyGraph([], [], [], [], 0.0)

    async def _detect_hotspots_claude(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Dtection des hotspots avec Claude Sonnet 4"""
        try:
            prompt = f"""
Analysez ce code Python et identifiez les hotspots problmatiques:

Fichier: {file_path}

```python
{content[:4000]}...
```

Identifiez en JSON les hotspots:
- Fonctions trop longues (>50 lignes)
- Classes god (>500 lignes)
- Complexit cyclomatique leve
- Code dupliqu
- Violations SOLID

Format: [{"type": "...", "location": "line X", "severity": "HIGH/MEDIUM/LOW", "description": "..."}]
"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start >= 0 and json_end > json_start:
                return json.loads(response_text[json_start:json_end])
            else:
                return []
                
        except Exception as e:
            print(f" Hotspots par dfaut: {str(e)}")
            return [{"type": "analysis_error", "severity": "LOW", "description": str(e)}]

    async def _generate_recommendations_claude(self, content: str, file_path: str, 
                                             ast_analysis: Dict, metrics: CodeMetrics, 
                                             dependencies: DependencyGraph) -> List[RefactoringRecommendation]:
        """Gnration des recommandations avec Claude Sonnet 4"""
        try:
            context = f"""
Fichier: {file_path}
Mtriques: LOC={metrics.lines_of_code}, CC={metrics.cyclomatic_complexity}, Classes={metrics.number_of_classes}
Dpendances: {len(dependencies.internal_dependencies)} internes, couplage={dependencies.coupling_score:.2f}
AST: {len(ast_analysis.get('functions', []))} fonctions, {len(ast_analysis.get('classes', []))} classes
"""

            prompt = f"""
Gnrez des recommandations de refactoring pour ce code:

{context}

```python
{content[:3000]}...
```

Retournez en JSON une liste de recommandations:
[
  {
    "priority": "HIGH|MEDIUM|LOW",
    "type": "EXTRACT_CLASS|EXTRACT_METHOD|SPLIT_FILE|REDUCE_COMPLEXITY|...",
    "description": "Description claire",
    "impact": "Impact business/technique",
    "effort": "Estimation effort (heures)",
    "affected_lines": [numros de lignes]
  }
]

Focalisez sur les patterns god class, SRP violations, complexit excessive.
"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start >= 0 and json_end > json_start:
                recommendations_data = json.loads(response_text[json_start:json_end])
                return [RefactoringRecommendation(**rec) for rec in recommendations_data]
            else:
                return []
                
        except Exception as e:
            print(f" Recommandations par dfaut: {str(e)}")
            return [
                RefactoringRecommendation(
                    priority="HIGH",
                    type="SPLIT_FILE",
                    description=f"Fichier trop volumineux ({metrics.lines_of_code} lignes)",
                    impact="Amliore la maintenabilit",
                    effort="4-8 heures",
                    affected_lines=list(range(1, min(100, metrics.lines_of_code)))
                )
            ]

    def _get_complexity_level(self, complexity: int) -> str:
        """Niveau de complexit"""
        if complexity > 20:
            return "TRS LEVE"
        elif complexity > 10:
            return "LEVE"
        elif complexity > 5:
            return "MODRE"
        else:
            return "FAIBLE"

    def _get_refactoring_priority(self, metrics: CodeMetrics, rec_count: int) -> str:
        """Priorit de refactoring"""
        if metrics.god_class_score > 0.8 or metrics.cyclomatic_complexity > 25:
            return "CRITIQUE"
        elif metrics.god_class_score > 0.6 or metrics.cyclomatic_complexity > 15:
            return "LEVE"
        elif metrics.god_class_score > 0.4 or rec_count > 3:
            return "MODRE"
        else:
            return "FAIBLE"

    def _estimate_effort(self, metrics: CodeMetrics, rec_count: int) -> str:
        """Estimation effort"""
        base_hours = (metrics.lines_of_code // 100) + (rec_count * 2)
        
        if base_hours > 40:
            return "40+ heures (plusieurs sprints)"
        elif base_hours > 20:
            return "20-40 heures (1-2 sprints)"
        elif base_hours > 8:
            return "8-20 heures (1 sprint)"
        else:
            return "2-8 heures (quelques jours)"

async def main():
    """Test de l'agent Alpha Claude Sonnet 4"""
    agent = AgentAnalyzerAlphaClaudeSonnet4()
    
    # Test sur un fichier god mode
    test_file = "orchestrator/app/main.py"
    if os.path.exists(test_file):
        result = await agent.analyze_file_deep(test_file)
        print(f"\n[CHECK] Test Alpha termin: {len(result.get('recommendations', []))} recommandations")
    else:
        print(f"[CROSS] Fichier test non trouv: {test_file}")

if __name__ == "__main__":
    asyncio.run(main()) 



