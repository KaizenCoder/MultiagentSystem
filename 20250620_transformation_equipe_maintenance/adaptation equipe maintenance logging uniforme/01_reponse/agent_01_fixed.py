import os
import ast
from core.agent_factory_architecture import Agent, Task, Result

class AgentMAINTENANCE01AnalyseurStructure(Agent):
    """
    Agent chargé d'analyser la structure des fichiers d'un répertoire donné.
    """
    def __init__(self, agent_id="agent_MAINTENANCE_01_analyseur_structure", version="1.0", description="Analyse la structure des fichiers d'un répertoire.", status="enabled"):
        super().__init__(agent_id, version, description, "analyser", status)

    async def startup(self):
        """Initialise l'agent et ses dépendances."""
        await super().startup()
        self.log("Analyseur de structure prêt.")

    async def execute_task(self, task: Task) -> Result:
        """Exécute la tâche d'analyse du répertoire."""
        if task.type != "analyse_structure":
            return Result(success=False, error="Type de tâche non supporté.")

        directory = task.params.get("directory")
        if not directory or not os.path.isdir(directory):
            return Result(success=False, error=f"Répertoire invalide ou non spécifié: {directory}")

        self.log(f"Analyse du répertoire : {directory}")
        files_analysis = []
        try:
            for filename in os.listdir(directory):
                if filename.endswith(".py") and filename.startswith("agent_MAINTENANCE_"):
                    file_path = os.path.join(directory, filename)
                    self.log(f"Analyse du fichier : {file_path}")
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        analysis = self._analyze_python_file(content)
                        files_analysis.append({
                            "path": file_path,
                            "content": content,
                            "analysis": analysis,
                        })
                    except Exception as e:
                        self.log(f"Erreur lors de l'analyse du fichier {file_path}: {e}", level="error")
                        files_analysis.append({
                            "path": file_path,
                            "content": None,
                            "error": str(e),
                        })

            return Result(success=True, data={"files": files_analysis})

        except Exception as e:
            self.log(f"Erreur majeure lors de l'analyse du répertoire {directory}: {e}", level="critical")
            return Result(success=False, error=str(e))

    def _analyze_python_file(self, code: str) -> dict:
        """
        Analyse le contenu d'un fichier Python pour en extraire la structure de base.
        """
        analysis_report = {
            "imports": [],
            "classes": [],
            "functions": [],
            "has_async": False,
        }
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis_report["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis_report["imports"].append(node.module)
                elif isinstance(node, ast.ClassDef):
                    analysis_report["classes"].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    analysis_report["functions"].append(node.name)
                elif isinstance(node, ast.AsyncFunctionDef):
                    analysis_report["functions"].append(f"async {node.name}")
                    analysis_report["has_async"] = True
        except SyntaxError as e:
            return {"error": f"SyntaxError: {e}"}

        return analysis_report
