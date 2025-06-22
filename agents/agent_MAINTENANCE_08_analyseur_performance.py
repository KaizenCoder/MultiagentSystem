import ast
import re
from collections import defaultdict
from core.agent_factory_architecture import Agent, Task, Result

class AgentMAINTENANCE08AnalyseurPerformance(Agent):
    """
    Agent chargé d'optimiser les performances du code :
    - Détecte les anti-patterns de performance
    - Suggère des optimisations
    - Analyse la complexité algorithmique
    - Identifie les goulots d'étranglement potentiels
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Patterns d'anti-performance
        self.performance_antipatterns = [
            {
                "pattern": r'for\s+\w+\s+in\s+range\(len\(',
                "issue": "Utilisation de range(len()) au lieu d'enumerate()",
                "suggestion": "Remplacer par enumerate() ou itération directe"
            },
            {
                "pattern": r'\.append\(\)\s*$',
                "issue": "Appels multiples à append() dans une boucle",
                "suggestion": "Considérer list comprehension ou extend()"
            },
            {
                "pattern": r'str\s*\+\s*str',
                "issue": "Concaténation de strings avec +",
                "suggestion": "Utiliser join() pour multiple concaténations"
            }
        ]

    async def startup(self):
        await super().startup()
        self.log("Optimiseur de performance prêt.")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "optimize_performance":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni.")

        self.log(f"Analyse de performance pour : {file_path}")

        try:
            tree = ast.parse(code)
            
            # Analyses de performance
            complexity_analysis = self._analyze_complexity(tree)
            antipatterns = self._detect_antipatterns(code)
            optimizations = self._suggest_optimizations(tree, code)
            
            # Score de performance global
            performance_score = self._calculate_performance_score(
                complexity_analysis, antipatterns, optimizations
            )
            
            # Génération du code optimisé (suggestions)
            optimized_suggestions = self._generate_optimization_suggestions(
                code, antipatterns, optimizations
            )

            report = {
                "file_path": file_path,
                "performance_score": performance_score,
                "complexity_analysis": complexity_analysis,
                "antipatterns_detected": antipatterns,
                "optimizations_suggested": optimizations,
                "optimization_suggestions": optimized_suggestions
            }

            self.log(f"Analyse de performance terminée pour {file_path} - Score: {performance_score}/100")
            
            return Result(success=True, data={
                "performance_report": report,
                "needs_optimization": performance_score < 70
            })

        except Exception as e:
            self.log(f"Erreur lors de l'analyse de performance de {file_path}: {e}", level="error")
            return Result(success=False, error=str(e))

    def _analyze_complexity(self, tree: ast.AST) -> dict:
        """Analyse la complexité algorithmique du code."""
        complexity = {
            "cyclomatic_complexity": 0,
            "nested_loops": 0,
            "recursive_functions": [],
            "long_functions": [],
            "complexity_hotspots": []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_complexity = self._calculate_function_complexity(node)
                complexity["cyclomatic_complexity"] += func_complexity["cyclomatic"]
                
                if func_complexity["has_recursion"]:
                    complexity["recursive_functions"].append(node.name)
                
                if len(node.body) > 20:  # Fonction longue
                    complexity["long_functions"].append({
                        "name": node.name,
                        "lines": len(node.body)
                    })
                
                if func_complexity["nested_loops"] > 0:
                    complexity["nested_loops"] += func_complexity["nested_loops"]
                    complexity["complexity_hotspots"].append({
                        "function": node.name,
                        "nested_loops": func_complexity["nested_loops"],
                        "estimated_complexity": "O(n^{})".format(func_complexity["nested_loops"] + 1)
                    })
        
        return complexity

    def _calculate_function_complexity(self, func_node: ast.AST) -> dict:
        """Calcule la complexité d'une fonction spécifique."""
        complexity = {
            "cyclomatic": 1,  # Base complexity
            "nested_loops": 0,
            "has_recursion": False
        }
        
        loop_depth = 0
        max_loop_depth = 0
        
        for node in ast.walk(func_node):
            # Complexité cyclomatique
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity["cyclomatic"] += 1
            elif isinstance(node, ast.BoolOp):
                complexity["cyclomatic"] += len(node.values) - 1
            
            # Détection des boucles imbriquées
            if isinstance(node, (ast.For, ast.While)):
                loop_depth += 1
                max_loop_depth = max(max_loop_depth, loop_depth)
            
            # Détection de récursion
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == func_node.name:
                    complexity["has_recursion"] = True
        
        complexity["nested_loops"] = max_loop_depth
        return complexity

    def _detect_antipatterns(self, code: str) -> list:
        """Détecte les anti-patterns de performance."""
        detected = []
        
        for pattern_info in self.performance_antipatterns:
            matches = re.finditer(pattern_info["pattern"], code, re.MULTILINE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                detected.append({
                    "line": line_num,
                    "pattern": pattern_info["pattern"],
                    "issue": pattern_info["issue"],
                    "suggestion": pattern_info["suggestion"],
                    "code_snippet": match.group()
                })
        
        # Détection spécifique : boucles avec append multiples
        append_in_loops = self._detect_append_in_loops(code)
        detected.extend(append_in_loops)
        
        # Détection : dictionnaire avec get() au lieu de defaultdict
        dict_get_patterns = self._detect_dict_get_antipattern(code)
        detected.extend(dict_get_patterns)
        
        return detected

    def _detect_append_in_loops(self, code: str) -> list:
        """Détecte les multiples append() dans les boucles."""
        issues = []
        lines = code.split('\n')
        
        in_loop = False
        loop_start = 0
        append_count = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            if re.match(r'^\s*(for|while)\s+', line):
                in_loop = True
                loop_start = i + 1
                append_count = 0
            elif in_loop and not line.startswith(' ') and stripped:
                # Fin de la boucle
                if append_count > 3:
                    issues.append({
                        "line": loop_start,
                        "issue": f"Multiple append() calls in loop ({append_count} times)",
                        "suggestion": "Consider using list comprehension or collecting items first",
                        "severity": "medium"
                    })
                in_loop = False
            elif in_loop and '.append(' in stripped:
                append_count += 1
        
        return issues

    def _detect_dict_get_antipattern(self, code: str) -> list:
        """Détecte l'usage excessif de dict.get() au lieu de defaultdict."""
        issues = []
        get_calls = re.findall(r'\.get\([^)]+\)', code)
        
        if len(get_calls) > 5:  # Seuil arbitraire
            issues.append({
                "line": 0,
                "issue": f"Multiple dict.get() calls detected ({len(get_calls)})",
                "suggestion": "Consider using collections.defaultdict for better performance",
                "severity": "low"
            })
        
        return issues

    def _suggest_optimizations(self, tree: ast.AST, code: str) -> list:
        """Suggère des optimisations spécifiques."""
        optimizations = []
        
        # Analyse des patterns d'optimisation
        for node in ast.walk(tree):
            # Suggestion : utiliser any()/all() au lieu de boucles
            if isinstance(node, ast.For):
                if self._is_boolean_search_loop(node):
                    optimizations.append({
                        "type": "boolean_search",
                        "suggestion": "Replace loop with any()/all() for boolean search",
                        "impact": "high"
                    })
            
            # Suggestion : comprehensions au lieu de boucles d'accumulation
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if self._has_accumulation_pattern(node):
                    optimizations.append({
                        "type": "accumulation_loop",
                        "suggestion": "Replace accumulation loop with list/dict comprehension",
                        "impact": "high"
                    })
        return optimizations

    def _is_boolean_search_loop(self, loop_node: ast.For) -> bool:
        """Vérifie si une boucle est une recherche de booléen."""
        if len(loop_node.body) == 1 and isinstance(loop_node.body[0], ast.If):
            if_node = loop_node.body[0]
            if len(if_node.body) == 1 and isinstance(if_node.body[0], ast.Break):
                return True
        return False

    def _has_accumulation_pattern(self, func_node: ast.AST) -> bool:
        """Vérifie si une fonction a un pattern d'accumulation."""
        has_init = False
        has_append = False
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Assign):
                if isinstance(node.value, (ast.List, ast.Dict)):
                    has_init = True
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == 'append':
                    has_append = True
        
        return has_init and has_append
        
    def _calculate_performance_score(self, complexity: dict, antipatterns: list, optimizations: list) -> int:
        """Calcule un score de performance global."""
        score = 100
        
        # Pénalités pour la complexité
        score -= complexity["cyclomatic_complexity"]
        score -= complexity["nested_loops"] * 10
        score -= len(complexity["recursive_functions"]) * 5
        score -= len(complexity["long_functions"]) * 2
        
        # Pénalités pour les anti-patterns
        score -= len(antipatterns) * 5
        
        # Bonus pour les opportunités d'optimisation
        score += len(optimizations) * 2
        
        return max(0, min(100, score))

    def _generate_optimization_suggestions(self, code: str, antipatterns: list, optimizations: list) -> list:
        """Génère des suggestions de code optimisé."""
        suggestions = []
        
        for anti_pattern in antipatterns:
            suggestions.append(f"Line {anti_pattern['line']}: {anti_pattern['suggestion']}")
            
        for opt in optimizations:
            suggestions.append(f"Opportunity: {opt['suggestion']}")
            
        return suggestions

    async def shutdown(self) -> None:
        await super().shutdown()
        self.log("Optimiseur de performance éteint.")

    def get_capabilities(self) -> list[str]:
        return ["optimize_performance"]

    async def health_check(self) -> dict:
        return {"status": "healthy"}

def create_agent_MAINTENANCE_08_analyseur_performance(**config) -> "AgentMAINTENANCE08AnalyseurPerformance":
    """Factory function to create an instance of the agent."""
    return AgentMAINTENANCE08AnalyseurPerformance(**config)