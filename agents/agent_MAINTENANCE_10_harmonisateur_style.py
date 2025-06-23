import ast
import re
import keyword
from typing import List, Dict, Any, Tuple

# --- Configuration Robuste du Chemin d'Importation ---
import sys
from pathlib import Path
try:
    import black
except ImportError:
    black = None

try:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core.agent_factory_architecture import Agent, Task, Result

class AgentMAINTENANCE10HarmonisateurStyle(Agent):
    """
    Agent chargé d'harmoniser le style du code Python en utilisant l'outil Black.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_id="agent_MAINTENANCE_10_harmonisateur_style"
        self.version="1.1" # Version incrémentée pour l'activation
        self.description="Harmonise le style du code Python en utilisant Black."
        self.agent_type = "style_harmonizer"
        self.black_available = black is not None
        
        # Règles de style PEP 8
        self.pep8_rules = {
            'max_line_length': 88,
            'max_function_length': 50,
            'max_class_length': 200,
            'indent_size': 4,
            'blank_lines_top_level': 2,
            'blank_lines_method': 1
        }
        
        self.naming_patterns = {
            'function': re.compile(r'^[a-z_][a-z0-9_]*$'),
            'variable': re.compile(r'^[a-z_][a-z0-9_]*$'),
            'constant': re.compile(r'^[A-Z_][A-Z0-9_]*$'),
            'class': re.compile(r'^[A-Z][a-zA-Z0-9]*$'),
            'module': re.compile(r'^[a-z_][a-z0-9_]*$')
        }
        
        self.avoid_names = set(keyword.kwlist + ['l', 'O', 'I', 'data', 'info', 'temp', 'tmp'])
        
        self.docstring_templates = {
            'function': '"""\\n    {description}\\n    \\n    Args:\\n        {args}\\n    \\n    Returns:\\n        {returns}\\n    """',
            'class': '"""\\n    {description}\\n    \\n    Attributes:\\n        {attributes}\\n    """',
            'module': '"""\\n{description}\\n\\n{details}\\n"""'
        }

    async def startup(self):
        await super().startup()
        if not self.black_available:
            self.log("La bibliothèque 'black' n'est pas installée. L'agent ne pourra pas formater le code.", level="warning")
        self.log("Harmonisateur de style (Black) prêt.")

    async def shutdown(self):
        await super().shutdown()
        self.log("Harmonisateur de style arrêté.")

    def get_capabilities(self) -> List[str]:
        return ["style_harmonization"]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy" if self.black_available else "degraded", "version": self.version, "dependencies": {"black": self.black_available}}

    async def execute_task(self, task: Task) -> Result:
        if task.type != "harmonize_style":
            return Result(success=False, error="Type de tâche non supporté.")

        if not self.black_available:
            return Result(success=False, error="La dépendance 'black' n'est pas installée.")

        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni.")

        self.log(f"🎨 Application de Black sur : {file_path}")

        try:
            # Configuration de Black
            mode = black.Mode(line_length=88)
            
            # Formatage du code
            formatted_code = black.format_str(code, mode=mode)
            
            code_changed = code != formatted_code
            
            style_report = {
                "file_path": file_path,
                "formatter": "black",
                "code_changed": code_changed,
                "summary": "Le code a été reformaté." if code_changed else "Aucune modification de formatage nécessaire."
            }

            self.log(f"🎨 Formatage terminé pour {file_path}. Changements appliqués: {code_changed}")
            
            return Result(success=True, data={
                "harmonized_code": formatted_code,
                "style_report": style_report
            })

        except black.NothingChanged:
            return Result(success=True, data={
                "harmonized_code": code,
                "style_report": {
                    "file_path": file_path,
                    "formatter": "black",
                    "code_changed": False,
                    "summary": "Aucune modification de formatage nécessaire."
                }
            })
        except Exception as e:
            self.log(f"Erreur lors du formatage avec Black sur {file_path}: {e}", level="error")
            return Result(success=False, error=str(e))

def create_agent_MAINTENANCE_10_harmonisateur_style(**kwargs) -> AgentMAINTENANCE10HarmonisateurStyle:
    return AgentMAINTENANCE10HarmonisateurStyle(**kwargs) 