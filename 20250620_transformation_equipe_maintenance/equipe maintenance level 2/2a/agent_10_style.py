import ast
import re
import keyword
from typing import List, Dict, Any, Tuple
from agent_factory_implementation.core.agent_factory_architecture import Agent, Task, Result

class AgentMAINTENANCE10HarmonisateurStyle(Agent):
    """
    Agent chargé d'harmoniser et d'améliorer le style du code Python :
    - Applique les règles PEP 8
    - Normalise les noms de variables et fonctions
    - Harmonise les docstrings
    - Corrige l'indentation et l'espacement
    - Organise les imports selon les standards
    - Améliore la lisibilité générale du code
    """
    
    def __init__(self, agent_id="agent_MAINTENANCE_10_harmonisateur_style", version="1.0", description="Harmonise le style et la présentation du code Python.", status="enabled"):
        super().__init__(agent_id, version, description, "style_harmonizer", status)
        
        # Règles de style PEP 8
        self.pep8_rules = {
            'max_line_length': 88,  # Plus moderne que 79, compatible avec black
            'max_function_length': 50,
            'max_class_length': 200,
            'indent_size': 4,
            'blank_lines_top_level': 2,
            'blank_lines_method': 1
        }
        
        # Patterns de naming conventions
        self.naming_patterns = {
            'function': re.compile(r'^[a-z_][a-z0-9_]*$'),
            'variable': re.compile(r'^[a-z_][a-z0-9_]*$'),
            'constant': re.compile(r'^[A-Z_][A-Z0-9_]*$'),
            'class': re.compile(r'^[A-Z][a-zA-Z0-9]*$'),
            'module': re.compile(r'^[a-z_][a-z0-9_]*$')
        }
        
        # Mots-clés à éviter comme noms de variables
        self.avoid_names = set(keyword.kwlist + [
            'l', 'O', 'I',  # Confondables avec 1, 0, 1
            'data', 'info', 'temp', 'tmp',  # Trop génériques
        ])
        
        # Templates de docstrings
        self.docstring_templates = {
            'function': '"""\n    {description}\n    \n    Args:\n        {args}\n    \n    Returns:\n        {returns}\n    """',
            'class': '"""\n    {description}\n    \n    Attributes:\n        {attributes}\n    """',
            'module': '"""\n{description}\n\n{details}\n"""'
        }

    async def startup(self):
        await super().startup()
        self.log("Harmonisateur de style prêt. Chargement des règles PEP 8...")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "harmonize_style":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni.")

        self.log(f"🎨 Harmonisation du style pour : {file_path}")

        try:
            # Analyse du style actuel
            style_analysis = self._analyze_current_style(code)
            
            # Application des corrections de style
            harmonized_code = self._harmonize_code(code)
            
            # Vérification des améliorations
            improvements = self._calculate_improvements(code, harmonized_code)
            
            # Génération du rapport de style
            style_report = {
                "file_path": file_path,
                "original_style_score": style_analysis["style_score"],
                "harmonized_style_score": self._calculate_style_score(harmonized_code),
                "issues_found": style_analysis["issues"],
                "corrections_applied": improvements["corrections"],
                "suggestions": improvements["suggestions"],
                "statistics": {
                    "lines_before": len(code.splitlines()),
                    "lines_after": len(harmonized_code.splitlines()),
                    "improvements_count": len(improvements["corrections"])
                }
            }

            self.log(f"🎨 Harmonisation terminée pour {file_path} - Score: {style_analysis['style_score']:.1f} → {style_report['harmonized_style_score']:.1f}")
            
            return Result(success=True, data={
                "harmonized_code": harmonized_code,
                "style_report": style_report,
                "significant_improvement": style_report["harmonized_style_score"] > style_report["original_style_score"] + 10
            })

        except Exception as e:
            self.log(f"Erreur lors de l'harmonisation du style de {file_path}: {e}", level="error")
            return Result(success=False, error=str(e))

    def _analyze_current_style(self, code: str) -> Dict[str, Any]:
        """Analyse le style actuel du code."""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            # Analyse des noms
            naming_issues = self._check_naming_conventions(tree)
            issues.extend(naming_issues)
            
            # Analyse des docstrings
            docstring_issues = self._check_docstrings(tree)
            issues.extend(docstring_issues)
            
            # Analyse de la structure
            structure_issues = self._check_code_structure(tree, code)
            issues.extend(structure_issues)
            
        except SyntaxError as e:
            issues.append({
                'type': 'syntax_error',
                'severity': 'HIGH',
                'description': f'Erreur de syntaxe: {e}',
                'line': getattr(e, 'lineno', 0)
            })
        
        # Analyse du formatage
        formatting_issues = self._check_formatting(code)
        issues.extend(formatting_issues)
        
        # Calcul du score de style
        style_score = self._calculate_style_score(code)
        
        return {
            "style_score": style_score,
            "issues": issues,
            "total_issues": len(issues)
        }

    def _check_naming_conventions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Vérifie les conventions de nommage."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not self.naming_patterns['function'].match(node.name):
                    issues.append({
                        'type': 'naming_function',
                        'severity': 'MEDIUM',
                        'description': f"Nom de fonction '{node.name}' non conforme à PEP 8",
                        'suggestion': f"Utiliser snake