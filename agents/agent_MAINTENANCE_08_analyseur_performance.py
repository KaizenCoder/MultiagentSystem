"""
⏱️ ANALYSEUR DE PERFORMANCE - Agent 08
=======================================

🎯 Mission : Analyser la performance et la complexité du code.
⚡ Capacités : Calcul de la complexité cyclomatique, analyse des "points chauds".
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
"""
    
import ast
import re
from collections import defaultdict
from core.agent_factory_architecture import Agent, Task, Result
import logging
from tools.universal_audit_report import generate_universal_audit_md

class AgentMAINTENANCE08AnalyseurPerformance(Agent):
    def __init__(self, **kwargs):
        super().__init__(agent_type="analyseur_performance", **kwargs)
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={
                    "logger_name": f"nextgen.maintenance.analyseur_performance.{self.id}",
                    "log_dir": "logs/maintenance/analyseur",
                    "metadata": {
                        "agent_type": "MAINTENANCE_08_analyseur_performance",
                        "agent_role": "analyseur_performance",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = self.id
        
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
        self.logger.info("Optimiseur de performance prêt.")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "optimize_performance":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni.")

        self.logger.info(f"Analyse de performance pour : {file_path}")

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

            self.logger.info(f"Analyse de performance terminée pour {file_path} - Score: {performance_score}/100")
            
            # Génération du rapport universel (en plus du rapport classique)
            output_md_universal = f"reports/audits/{file_path.replace('.', '_')}_performance_audit_universal.md"
            generate_universal_audit_md(report, agent_type="performance", output_path=output_md_universal, extra={"auditeur": "AgentMAINTENANCE08AnalyseurPerformance"})
            self.logger.info(f"Rapport Markdown universel généré : {output_md_universal}")

            return Result(success=True, data={
                "performance_report": report,
                "needs_optimization": performance_score < 70
            })

        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse de performance de {file_path}: {e}")
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
        """Détecte les boucles de recherche booléenne."""
        if len(loop_node.body) == 1 and isinstance(loop_node.body[0], ast.If):
            if_node = loop_node.body[0]
            if len(if_node.body) == 1 and isinstance(if_node.body[0], ast.Break):
                return True
        return False

    def _has_accumulation_pattern(self, func_node: ast.AST) -> bool:
        """Détecte les patterns d'accumulation simples."""
        for node in ast.walk(func_node):
            if isinstance(node, ast.For):
                for item in node.body:
                    if isinstance(item, ast.Expr) and isinstance(item.value, ast.Call):
                        call = item.value
                        if isinstance(call.func, ast.Attribute) and call.func.attr == 'append':
                            return True
        return False

    def _calculate_performance_score(self, complexity: dict, antipatterns: list, optimizations: list) -> int:
        """Calcule un score de performance global."""
        score = 100
        
        # Pénalité pour complexité
        score -= complexity["cyclomatic_complexity"] * 0.5
        score -= complexity["nested_loops"] * 5
        
        # Pénalité pour anti-patterns
        score -= len(antipatterns) * 3
        
        # Bonus pour potentiel d'optimisation (négatif)
        score -= len(optimizations) * 2
        
        return max(0, int(score))

    def _generate_optimization_suggestions(self, code: str, antipatterns: list, optimizations: list) -> list:
        """Génère des suggestions de code optimisé."""
        suggestions = []
        
        for ap in antipatterns:
            suggestions.append(f"Ligne {ap['line']}: {ap['issue']}. Suggestion: {ap['suggestion']}")
            
        for opt in optimizations:
            suggestions.append(f"Optimisation possible: {opt['suggestion']} (Impact: {opt['impact']})")
        
        return suggestions

    async def shutdown(self) -> None:
        """Arrête l'agent."""
        await super().shutdown()
        self.logger.info("Optimiseur de performance éteint.")

    def get_capabilities(self) -> list[str]:
        return ["optimize_performance"]

    async def health_check(self) -> dict:
        return {"status": "healthy", "version": "1.0"}

def create_agent_MAINTENANCE_08_analyseur_performance(**config) -> "AgentMAINTENANCE08AnalyseurPerformance":
    """Factory pour créer une instance de l'analyseur de performance."""
    return AgentMAINTENANCE08AnalyseurPerformance(**config)

async def main():
    # Création de l'agent
    security_agent = AgentMAINTENANCE08AnalyseurPerformance()
    await security_agent.startup()

    # Code à analyser
    sample_code = """
import os
import pickle

password = "my_super_secret_password"
api_key = 'hf_1234567890abcdef1234567890abcdef'

def execute_command(user_input):
    os.system(f"echo {user_input}")

def deserialize_data(data):
    return pickle.loads(data)

def dynamic_exec(code_str):
    exec(code_str)
"""

    # Création de la tâche
    task = Task(
        type="optimize_performance",
        params={"code": sample_code, "file_path": "example.py"}
    )

    # Exécution de la tâche
    result = await security_agent.execute_task(task)

    # Affichage des résultats
    if result.success:
        report = result.data['performance_report']
        print("--- Rapport de Performance ---")
        print(f"Fichier: {report['file_path']}")
        print(f"Score de performance: {report['performance_score']}/100")
        print(f"Complexité cyclomatique: {report['complexity_analysis']['cyclomatic_complexity']}")
        print(f"Anti-patterns détectés: {len(report['antipatterns_detected'])}")
        print(f"Optimisations suggérées: {len(report['optimizations_suggested'])}")
        # Génération du rapport universel (en plus du rapport classique)
        output_md_universal = f"reports/audits/{report['file_path'].replace('.', '_')}_performance_audit_universal.md"
        generate_universal_audit_md(report, agent_type="performance", output_path=output_md_universal, extra={"auditeur": "AgentMAINTENANCE08AnalyseurPerformance"})
        print(f"Rapport Markdown universel généré : {output_md_universal}")
        with open(output_md_universal, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("Erreur lors de l'analyse de performance :", result.error)

    await security_agent.shutdown()