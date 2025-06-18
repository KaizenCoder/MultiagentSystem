#!/usr/bin/env python3
"""
🎯 Agent Analyzer Beta - Gemini 2.5
⚡ Analyse rapide orientée code avec Gemini 2.5
🚀 Phase 1 Refactoring NextGeneration - Cloud API
"""

import os
import ast
import json
import asyncio
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
import google.generativeai as genai

# Configuration .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv non installé, utilisation variables système")

@dataclass
class CodePattern:
    """Pattern de code détecté"""
    name: str
    location: str
    type: str  # ANTI_PATTERN, SMELL, VIOLATION
    severity: str  # HIGH, MEDIUM, LOW
    description: str

@dataclass
class FunctionAnalysis:
    """Analyse d'une fonction"""
    name: str
    line_start: int
    line_end: int
    parameters_count: int
    complexity_score: float
    size_category: str  # SMALL, MEDIUM, LARGE, HUGE
    responsibilities: List[str]

@dataclass
class ClassAnalysis:
    """Analyse d'une classe"""
    name: str
    line_start: int
    line_end: int
    methods_count: int
    attributes_count: int
    god_class_score: float
    responsibilities: List[str]
    srp_violations: List[str]

@dataclass
class CodeSmells:
    """Code smells détectés"""
    long_methods: List[str]
    large_classes: List[str]
    parameter_lists: List[str]
    duplicate_code: List[str]
    dead_code: List[str]

@dataclass
class RefactoringStrategy:
    """Stratégie de refactoring"""
    target: str
    strategy: str  # EXTRACT, SPLIT, MERGE, MOVE, RENAME
    rationale: str
    steps: List[str]
    estimated_effort: str

class AgentAnalyzerBetaGemini25:
    """
    🎯 Agent Analyzer Beta - Gemini 2.5
    
    Mission:
    - Analyse rapide orientée code
    - Détection des patterns et smells
    - Extraction des fonctions/classes
    - Stratégies de refactoring immédiat
    """
    
    def __init__(self):
        self.name = "Agent Analyzer Beta - Gemini 2.5"
        self.model = "gemini-2.0-flash-exp"  # Gemini 2.5
        self.capabilities = [
            "Analyse rapide de code",
            "Détection patterns",
            "Code smells detection",
            "Extraction suggestions",
            "Stratégies refactoring"
        ]
        
        # Configuration Gemini 2.5 avec .env
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY manquante dans .env")
            
        genai.configure(api_key=api_key)
        self.model_instance = genai.GenerativeModel(self.model)
        
        # Paramètres optimisés pour vitesse
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.2,  # Cohérence vs créativité
            top_p=0.8,
            top_k=40,
            max_output_tokens=3000
        )
        
        self.workspace = Path("refactoring_workspace")
        self.results_dir = self.workspace / "results" / "beta_gemini"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🤖 {self.name} initialisé avec Gemini 2.5")
        print(f"⚙️ Modèle: {self.model}")
        print(f"🔑 Clé API: {'✅' if api_key else '❌'}")
        print(f"📁 Workspace: {self.workspace}")

    async def analyze_file_fast(self, file_path: str) -> Dict[str, Any]:
        """
        ⚡ Analyse rapide d'un fichier avec Gemini 2.5
        """
        print(f"\n⚡ Agent Beta - Analyse rapide: {file_path}")
        
        try:
            # Lecture du fichier
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"📊 Taille fichier: {len(content)} caractères")
            
            # Analyse patterns rapide
            patterns = await self._detect_patterns_gemini(content, file_path)
            
            # Analyse fonctions/classes
            functions = self._analyze_functions_fast(content)
            classes = self._analyze_classes_fast(content)
            
            # Détection code smells
            smells = await self._detect_code_smells_gemini(content, file_path)
            
            # Stratégies de refactoring
            strategies = await self._generate_strategies_gemini(
                content, file_path, functions, classes, smells
            )
            
            result = {
                "agent": self.name,
                "model": self.model,
                "file_path": file_path,
                "timestamp": datetime.now().isoformat(),
                "patterns": [asdict(p) for p in patterns],
                "functions": [asdict(f) for f in functions],
                "classes": [asdict(c) for c in classes],
                "smells": asdict(smells),
                "strategies": [asdict(s) for s in strategies],
                "summary": {
                    "total_patterns": len(patterns),
                    "critical_functions": len([f for f in functions if f.complexity_score > 0.8]),
                    "god_classes": len([c for c in classes if c.god_class_score > 0.7]),
                    "refactoring_urgency": self._calculate_urgency(patterns, functions, classes),
                    "quick_wins": len([s for s in strategies if "EXTRACT" in s.strategy])
                }
            }
            
            # Sauvegarde
            output_file = self.results_dir / f"beta_analysis_{Path(file_path).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Analyse Beta terminée - Résultats: {output_file}")
            return result
            
        except Exception as e:
            print(f"❌ Erreur analyse Beta: {str(e)}")
            return {"error": str(e), "file_path": file_path}

    async def _detect_patterns_gemini(self, content: str, file_path: str) -> List[CodePattern]:
        """Détection de patterns avec Gemini 2.5"""
        try:
            prompt = f"""
Analysez ce code Python et détectez les patterns problématiques:

Fichier: {file_path}

```python
{content[:4000]}
```

Détectez en JSON les patterns:
- God Object/Class
- Long Method
- Large Class
- Data Class
- Feature Envy
- Shotgun Surgery
- Duplicated Code

Format JSON strict:
[
  {{
    "name": "God Class",
    "location": "line 45-150",
    "type": "ANTI_PATTERN",
    "severity": "HIGH",
    "description": "Classe avec trop de responsabilités"
  }}
]
"""

            response = await self.model_instance.generate_content_async(
                prompt,
                generation_config=self.generation_config
            )
            
            response_text = response.text
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start >= 0 and json_end > json_start:
                patterns_data = json.loads(response_text[json_start:json_end])
                return [CodePattern(**pattern) for pattern in patterns_data]
            else:
                return []
                
        except Exception as e:
            print(f"⚠️ Patterns par défaut: {str(e)}")
            return [
                CodePattern(
                    name="Large File",
                    location=f"line 1-{len(content.split('\\n'))}",
                    type="SMELL",
                    severity="MEDIUM",
                    description=f"Fichier volumineux ({len(content)} caractères)"
                )
            ]

    def _analyze_functions_fast(self, content: str) -> List[FunctionAnalysis]:
        """Analyse rapide des fonctions"""
        try:
            tree = ast.parse(content)
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 10
                    params_count = len(node.args.args)
                    
                    # Score de complexité basique
                    complexity = min(1.0, (lines / 20) + (params_count / 5))
                    
                    # Catégorie de taille
                    if lines > 50:
                        size_cat = "HUGE"
                    elif lines > 25:
                        size_cat = "LARGE"
                    elif lines > 10:
                        size_cat = "MEDIUM"
                    else:
                        size_cat = "SMALL"
                    
                    # Responsabilités estimées (keywords)
                    func_content = ast.get_source_segment(content, node) or ""
                    responsibilities = []
                    if "request" in func_content.lower():
                        responsibilities.append("HTTP handling")
                    if "database" in func_content.lower() or "db" in func_content.lower():
                        responsibilities.append("Database access")
                    if "validate" in func_content.lower():
                        responsibilities.append("Validation")
                    if "log" in func_content.lower():
                        responsibilities.append("Logging")
                    
                    functions.append(FunctionAnalysis(
                        name=node.name,
                        line_start=node.lineno,
                        line_end=node.end_lineno if hasattr(node, 'end_lineno') else node.lineno + 10,
                        parameters_count=params_count,
                        complexity_score=complexity,
                        size_category=size_cat,
                        responsibilities=responsibilities
                    ))
            
            return functions
            
        except Exception as e:
            print(f"⚠️ Analyse fonctions échouée: {str(e)}")
            return []

    def _analyze_classes_fast(self, content: str) -> List[ClassAnalysis]:
        """Analyse rapide des classes"""
        try:
            tree = ast.parse(content)
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 50
                    
                    methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                    attributes = [n for n in node.body if isinstance(n, ast.Assign)]
                    
                    # Score god class
                    god_score = min(1.0, (lines / 200) + (len(methods) / 15))
                    
                    # Responsabilités (analyse basique)
                    class_content = ast.get_source_segment(content, node) or ""
                    responsibilities = []
                    srp_violations = []
                    
                    if "request" in class_content.lower() and "database" in class_content.lower():
                        responsibilities.extend(["HTTP handling", "Database access"])
                        srp_violations.append("Mixing HTTP and DB concerns")
                    
                    if len(methods) > 10:
                        srp_violations.append("Too many methods (>10)")
                    
                    classes.append(ClassAnalysis(
                        name=node.name,
                        line_start=node.lineno,
                        line_end=node.end_lineno if hasattr(node, 'end_lineno') else node.lineno + 50,
                        methods_count=len(methods),
                        attributes_count=len(attributes),
                        god_class_score=god_score,
                        responsibilities=responsibilities,
                        srp_violations=srp_violations
                    ))
            
            return classes
            
        except Exception as e:
            print(f"⚠️ Analyse classes échouée: {str(e)}")
            return []

    async def _detect_code_smells_gemini(self, content: str, file_path: str) -> CodeSmells:
        """Détection code smells avec Gemini 2.5"""
        try:
            prompt = f"""
Analysez ce code Python et détectez les code smells:

```python
{content[:3000]}
```

Identifiez en JSON:
- long_methods: méthodes >30 lignes
- large_classes: classes >200 lignes  
- parameter_lists: fonctions >5 paramètres
- duplicate_code: code dupliqué
- dead_code: code mort/inutilisé

Format JSON:
{{
  "long_methods": ["method_name (line X)"],
  "large_classes": ["class_name (line X)"],
  "parameter_lists": ["function_name (X params)"],
  "duplicate_code": ["pattern description"],
  "dead_code": ["unused_item"]
}}
"""

            response = await self.model_instance.generate_content_async(
                prompt,
                generation_config=self.generation_config
            )
            
            response_text = response.text
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                smells_data = json.loads(response_text[json_start:json_end])
                return CodeSmells(**smells_data)
            else:
                return CodeSmells([], [], [], [], [])
                
        except Exception as e:
            print(f"⚠️ Code smells par défaut: {str(e)}")
            # Détection basique
            lines = content.split('\n')
            long_methods = []
            large_classes = []
            
            in_method = False
            method_start = 0
            method_name = ""
            
            for i, line in enumerate(lines):
                if re.match(r'\s*def\s+(\w+)', line):
                    if in_method and i - method_start > 30:
                        long_methods.append(f"{method_name} (line {method_start})")
                    
                    match = re.match(r'\s*def\s+(\w+)', line)
                    method_name = match.group(1)
                    method_start = i
                    in_method = True
                    
                elif re.match(r'class\s+(\w+)', line):
                    # Estimation basique classe
                    if i > 0 and i < len(lines) - 200:
                        large_classes.append(f"class at line {i}")
            
            return CodeSmells(
                long_methods=long_methods,
                large_classes=large_classes,
                parameter_lists=[],
                duplicate_code=[],
                dead_code=[]
            )

    async def _generate_strategies_gemini(self, content: str, file_path: str,
                                        functions: List[FunctionAnalysis],
                                        classes: List[ClassAnalysis],
                                        smells: CodeSmells) -> List[RefactoringStrategy]:
        """Génération stratégies avec Gemini 2.5"""
        try:
            context = f"""
Fichier: {file_path}
Fonctions: {len(functions)} ({len([f for f in functions if f.size_category in ['LARGE', 'HUGE']])} grandes)
Classes: {len(classes)} ({len([c for c in classes if c.god_class_score > 0.7])} god classes)
Smells: {len(smells.long_methods)} méthodes longues, {len(smells.large_classes)} classes volumineuses
"""

            prompt = f"""
Générez des stratégies de refactoring pour ce code:

{context}

```python
{content[:2000]}
```

Retournez en JSON des stratégies prioritaires:
[
  {{
    "target": "Nom classe/méthode",
    "strategy": "EXTRACT_METHOD|EXTRACT_CLASS|SPLIT_FILE|MOVE_METHOD",
    "rationale": "Pourquoi cette stratégie",
    "steps": ["Étape 1", "Étape 2", "Étape 3"],
    "estimated_effort": "2-4 heures"
  }}
]

Focalisez sur les quick wins et extractions simples.
"""

            response = await self.model_instance.generate_content_async(
                prompt,
                generation_config=self.generation_config
            )
            
            response_text = response.text
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start >= 0 and json_end > json_start:
                strategies_data = json.loads(response_text[json_start:json_end])
                return [RefactoringStrategy(**strategy) for strategy in strategies_data]
            else:
                return []
                
        except Exception as e:
            print(f"⚠️ Stratégies par défaut: {str(e)}")
            strategies = []
            
            # Stratégies basées sur l'analyse
            for func in functions:
                if func.size_category in ['LARGE', 'HUGE']:
                    strategies.append(RefactoringStrategy(
                        target=func.name,
                        strategy="EXTRACT_METHOD",
                        rationale=f"Fonction {func.size_category.lower()} ({func.line_end - func.line_start} lignes)",
                        steps=[
                            "Identifier les blocs logiques",
                            "Extraire en méthodes privées",
                            "Tester après extraction"
                        ],
                        estimated_effort="2-4 heures"
                    ))
            
            for cls in classes:
                if cls.god_class_score > 0.7:
                    strategies.append(RefactoringStrategy(
                        target=cls.name,
                        strategy="EXTRACT_CLASS",
                        rationale=f"God class ({cls.methods_count} méthodes)",
                        steps=[
                            "Grouper méthodes par responsabilité",
                            "Extraire classes spécialisées",
                            "Refactorer les dépendances"
                        ],
                        estimated_effort="8-16 heures"
                    ))
            
            return strategies

    def _calculate_urgency(self, patterns: List[CodePattern], 
                          functions: List[FunctionAnalysis],
                          classes: List[ClassAnalysis]) -> str:
        """Calcul urgence refactoring"""
        high_patterns = len([p for p in patterns if p.severity == "HIGH"])
        huge_functions = len([f for f in functions if f.size_category == "HUGE"])
        god_classes = len([c for c in classes if c.god_class_score > 0.8])
        
        if high_patterns > 3 or god_classes > 1 or huge_functions > 2:
            return "CRITIQUE"
        elif high_patterns > 1 or god_classes > 0 or huge_functions > 1:
            return "ÉLEVÉE"
        elif len(patterns) > 5:
            return "MODÉRÉE"
        else:
            return "FAIBLE"

async def main():
    """Test de l'agent Beta Gemini 2.5"""
    agent = AgentAnalyzerBetaGemini25()
    
    # Test sur un fichier god mode
    test_file = "orchestrator/app/main.py"
    if os.path.exists(test_file):
        result = await agent.analyze_file_fast(test_file)
        print(f"\n✅ Test Beta terminé: {len(result.get('strategies', []))} stratégies")
    else:
        print(f"❌ Fichier test non trouvé: {test_file}")

if __name__ == "__main__":
    asyncio.run(main()) 