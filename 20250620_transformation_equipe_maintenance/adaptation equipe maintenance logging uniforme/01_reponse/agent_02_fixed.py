import re
from core.agent_factory_architecture import Agent, Task, Result

class AgentMAINTENANCE02EvaluateurUtilite(Agent):
    """
    Agent chargé d'évaluer l'utilité et la pertinence d'un fichier de code.
    Il vérifie si le code est un placeholder, un vrai agent, ou vide.
    """
    def __init__(self, agent_id="agent_MAINTENANCE_02_evaluateur_utilite", version="1.0", description="Évalue l'utilité d'un fichier de code.", status="enabled"):
        super().__init__(agent_id, version, description, "evaluator", status)
        # Regex pour détecter les signes de code "placeholder" ou non-implémenté
        self.placeholder_patterns = [
            re.compile(r'^\s*pass\s*$', re.MULTILINE),
            re.compile(r'raise\s+NotImplementedError'),
            re.compile(r'#\s*TODO', re.IGNORECASE),
            re.compile(r'return\s+None', re.IGNORECASE)
        ]

    async def startup(self):
        await super().startup()
        self.log("Évaluateur d'utilité prêt.")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "evaluate_utility":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        if code is None:
            return Result(success=False, error="Code non fourni.")

        self.log(f"Évaluation du fichier : {file_path}")

        # 1. Vérifier si le code est vide ou ne contient que des commentaires/espaces
        stripped_code = re.sub(r'#.*|\s', '', code)
        if not stripped_code:
            self.log(f"Fichier {file_path} est vide ou ne contient pas de code fonctionnel.")
            return Result(success=False, error="Le code est vide.", data={"evaluation": "empty"})

        # 2. Vérifier les patterns de code placeholder
        placeholder_score = 0
        for pattern in self.placeholder_patterns:
            if pattern.search(code):
                placeholder_score += 1
        
        # 3. Vérifier la complexité (très basique)
        num_lines = len([line for line in code.splitlines() if line.strip()])
        num_functions = code.count("def ")
        num_classes = code.count("class ")

        # Heuristique simple pour décider
        if num_lines < 10 and num_functions < 2 and placeholder_score > 0:
            self.log(f"Fichier {file_path} semble être un placeholder.")
            return Result(success=False, error="Le code est un placeholder.", data={"evaluation": "placeholder", "score": placeholder_score})

        # Si aucune condition d'inutilité n'est remplie
        self.log(f"Fichier {file_path} semble être un agent utile.")
        return Result(success=True, data={
            "evaluation": "useful", 
            "lines": num_lines, 
            "functions": num_functions,
            "classes": num_classes,
            "placeholder_score": placeholder_score
        })
