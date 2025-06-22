import ast
from pathlib import Path
from core.agent_factory_architecture import Agent, Task, Result
from typing import List, Dict, Any

class AgentMAINTENANCE02EvaluateurUtilite(Agent):
    """
    Évalue l'utilité d'un script Python en se basant sur une analyse statique
    de son arbre syntaxique abstrait (AST).
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger.info(f"Évaluateur d'utilité ({self.agent_id}) initialisé.")

    async def execute_task(self, task: Task) -> Result:
        file_path = task.params.get("file_path")
        self.log(f"Évaluation du fichier : {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            self.logger.error(f"Impossible de lire le fichier {file_path}: {e}")
            return Result(success=False, error=f"Erreur de lecture du fichier: {e}")

        try:
            tree = ast.parse(code)
            score = self._evaluate_ast(tree)
            min_score = self.config.get("min_score_for_usefulness", 15) if hasattr(self, 'config') else 15
            is_useful = score >= min_score
            self.log(f"Résultat pour {file_path}: Score={score}, Utile={is_useful}")
            return Result(
                success=True, 
                data={"score": score, "is_useful": is_useful, "details": "Évaluation réussie"}
            )
        except SyntaxError as e:
            self.logger.error(f"Impossible d'évaluer le script {file_path}, erreur de syntaxe: {e}")
            return Result(
                success=True, 
                data={"score": 0, "is_useful": False, "details": f"Erreur de syntaxe: {e}"}
            )

    def _evaluate_ast(self, tree):
        score = 0
        has_class = False
        has_function = False

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                score += 1 * len(node.names)
            elif isinstance(node, ast.ImportFrom):
                score += 1 * len(node.names)
            elif isinstance(node, ast.FunctionDef):
                score += 5
                has_function = True
                if node.body:
                    score += len(node.body)
            elif isinstance(node, ast.ClassDef):
                score += 10
                has_class = True
                if node.body:
                    score += len(node.body)
            elif isinstance(node, ast.Call):
                score += 1
            elif isinstance(node, ast.Try):
                score += 2
            elif isinstance(node, (ast.If, ast.For, ast.While)):
                score += 2

        if has_class and has_function:
            score += 5
            
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                score -= 5
            if isinstance(node, ast.ClassDef) and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                score -= 5

        return max(0, score)

    async def startup(self) -> None:
        self.log("Évaluateur d'utilité prêt.")
        pass

    async def shutdown(self) -> None:
        self.log("Évaluateur d'utilité éteint.")
        pass

    def get_capabilities(self) -> List[str]:
        return ["evaluate_utility", "ast_evaluation"]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "ok"}

def create_agent_MAINTENANCE_02_evaluateur_utilite(**config) -> "AgentMAINTENANCE02EvaluateurUtilite":
    """Factory pour créer une instance de l'Agent 2."""
    return AgentMAINTENANCE02EvaluateurUtilite(**config)