from core.agent_factory_architecture import Agent, Task, Result
import ast

class AgentMAINTENANCE05DocumenteurPeerReviewer(Agent):
    """
    Agent chargé d'ajouter ou de mettre à jour la documentation (docstrings)
    et de réaliser une "peer review" algorithmique simple.
    """
    def __init__(self, agent_id="agent_MAINTENANCE_05_documenteur_peer_reviewer", version="1.0", description="Documente le code et effectue une peer review.", status="enabled"):
        super().__init__(agent_id, version, description, "documenter", status)

    async def startup(self):
        await super().startup()
        self.log("Documenteur / Peer Reviewer prêt.")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "document_code":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni.")

        self.log(f"Documentation et peer review pour : {file_path}")

        try:
            tree = ast.parse(code)
            
            # Peer review simple
            review_issues = self._peer_review(tree)
            if review_issues:
                self.log(f"Problèmes de peer review trouvés dans {file_path}: {review_issues}", level="warning")

            # Ajout/Mise à jour des docstrings
            documented_tree = self._add_docstrings(tree)
            
            # Utiliser ast.unparse si disponible, sinon retourner le code original
            try:
                documented_code = ast.unparse(documented_tree)
            except AttributeError:
                # Pour Python < 3.9, on retourne le code original avec juste la review
                documented_code = code
                self.log("AST.unparse non disponible, docstrings non ajoutés automatiquement", level="warning")

            return Result(success=True, data={
                "documented_code": documented_code,
                "review_issues": review_issues
            })

        except Exception as e:
            self.log(f"Erreur lors de la documentation de {file_path}: {e}", level="error")
            return Result(success=False, error=str(e))

    def _add_docstrings(self, tree: ast.AST) -> ast.AST:
        """Ajoute des docstrings basiques là où ils manquent."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    self.log(f"Ajout d'un docstring placeholder pour '{node.name}'")
                    placeholder_docstring = ast.Expr(value=ast.Constant(value=f"Documentation pour {node.name}"))
                    node.body.insert(0, placeholder_docstring)
        
        ast.fix_missing_locations(tree)
        return tree

    def _peer_review(self, tree: ast.AST) -> list:
        """
        Effectue des vérifications simples sur le code.
        - Nom des variables trop courts
        - Fonctions trop longues
        """
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.arg) and len(node.arg) < 2 and node.arg not in ['e', 'f', 'x', 'y', 'i', 'j']:
                issues.append(f"Argument name '{node.arg}' is very short.")
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and len(node.id) < 2 and node.id not in ['e', 'f', 'x', 'y', 'i', 'j']:
                issues.append(f"Variable name '{node.id}' is very short.")
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if len(node.body) > 30:
                    issues.append(f"Function '{node.name}' is quite long ({len(node.body)} statements).")
        return issues
