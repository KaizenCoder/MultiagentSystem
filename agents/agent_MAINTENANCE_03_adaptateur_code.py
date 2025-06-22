#!/usr/bin/env python3
"""
AGENT 3 - ADAPTATEUR DE CODE (LibCST)
"""
import sys
from pathlib import Path
import logging
import asyncio
import re
from typing import List, Dict, Any

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core.agent_factory_architecture import Agent, Task, Result
import libcst as cst

# --- Fonctions et Classes de Transformation CST ---

class CstPassInserter(cst.CSTTransformer):
    """
    Un CSTTransformer qui insère 'pass' dans les blocs de code vides.
    C'est une approche plus robuste que le traitement de texte.
    """
    def leave_IndentedBlock(self, original_node: cst.IndentedBlock, updated_node: cst.IndentedBlock) -> cst.IndentedBlock:
        if not updated_node.body:
            return updated_node.with_changes(body=[cst.SimpleStatementLine(body=[cst.Pass()])])
        return updated_node

    def leave_Try(self, original_node: cst.Try, updated_node: cst.Try) -> cst.Try:
        if not updated_node.body.body:
            new_body = updated_node.body.with_changes(body=[cst.SimpleStatementLine(body=[cst.Pass()])])
            updated_node = updated_node.with_changes(body=new_body)
        
        if not updated_node.handlers:
            new_handler = cst.ExceptHandler(
                body=cst.IndentedBlock(body=[cst.SimpleStatementLine(body=[cst.Pass()])]),
                type=cst.Name("Exception")
            )
            return updated_node.with_changes(handlers=[new_handler])
        return updated_node

class CstImportAdder(cst.CSTTransformer):
    """
    Un CSTTransformer qui ajoute des imports simples (`import module`)
    en évitant les doublons.
    """
    def __init__(self, modules_to_add: List[str]):
        self.modules_to_add = modules_to_add

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
        existing_imports = set()
        for stmt in updated_node.body:
            if isinstance(stmt, cst.SimpleStatementLine) and isinstance(stmt.body[0], cst.Import):
                for alias in stmt.body[0].names:
                    existing_imports.add(alias.name.value)
        
        new_imports = []
        for module in self.modules_to_add:
            if module not in existing_imports:
                new_imports.append(
                    cst.SimpleStatementLine(
                        body=[cst.Import(names=[cst.ImportAlias(name=cst.Name(module))])]
                    )
                )

        if not new_imports:
            return updated_node
            
        insert_idx = 0
        if len(updated_node.body) > 0:
            first_stmt = updated_node.body[0]
            if isinstance(first_stmt, cst.SimpleStatementLine) and \
               isinstance(first_stmt.body[0], cst.Expr) and \
               isinstance(first_stmt.body[0].value, cst.SimpleString):
                insert_idx = 1
                
        body_list = list(updated_node.body)
        body_list[insert_idx:insert_idx] = new_imports
        return updated_node.with_changes(body=tuple(body_list))

def _build_module_path(path: str) -> cst.BaseExpression:
    """
    Construit une arborescence CST pour un chemin de module avec des points (ex: 'a.b.c').
    Ceci est la CORRECTION CLÉ pour le bug de `libcst`.
    """
    parts = path.split('.')
    if not all(part.isidentifier() for part in parts):
        raise ValueError(f"Chemin de module invalide: {path}")

    node = cst.Name(value=parts[0])
    for part in parts[1:]:
        node = cst.Attribute(value=node, attr=cst.Name(value=part))
    return node

class CstComplexImportAdder(cst.CSTTransformer):
    """
    Un CSTTransformer qui ajoute des imports 'from ... import ...'
    en évitant les doublons et en gérant les chemins de modules complexes.
    """
    def __init__(self, from_module: str, names_to_import: List[str]):
        self.from_module = from_module
        self.names_to_import = names_to_import

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
        existing_imports = set()
        for stmt in updated_node.body:
            if isinstance(stmt, cst.SimpleStatementLine) and isinstance(stmt.body[0], cst.ImportFrom):
                module_node = stmt.body[0].module
                module_str = ""
                try:
                    module_str = updated_node.code_for_node(module_node)
                except Exception:
                    pass

                if module_str == self.from_module:
                    if isinstance(stmt.body[0].names, cst.ImportStar):
                        return updated_node
                    for alias in stmt.body[0].names:
                        existing_imports.add(alias.name.value)
        
        new_names_to_import = [name for name in self.names_to_import if name not in existing_imports]

        if not new_names_to_import:
            return updated_node

        # *** LA CORRECTION EST ICI ***
        # Utilisation de la fonction helper pour construire le chemin du module.
        new_import_statement = cst.SimpleStatementLine(
            body=[cst.ImportFrom(
                module=_build_module_path(self.from_module), # <-- C'ÉTAIT L'ERREUR
                names=[cst.ImportAlias(name=cst.Name(name)) for name in new_names_to_import]
            )]
        )

        insert_idx = 0
        if len(updated_node.body) > 0:
            first_stmt = updated_node.body[0]
            if isinstance(first_stmt, cst.SimpleStatementLine) and \
               isinstance(first_stmt.body[0], cst.Expr) and \
               isinstance(first_stmt.body[0].value, cst.SimpleString):
                insert_idx = 1
                
        body_list = list(updated_node.body)
        body_list.insert(insert_idx, new_import_statement)
        return updated_node.with_changes(body=tuple(body_list))

class AgentMAINTENANCE03AdaptateurCode(Agent):
    """
    Agent qui utilise LibCST pour une réparation de code robuste et multi-niveaux.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger.info(f"Adaptateur de code CST v{self.version} ({self.agent_id}) initialisé.")
        
        self.COMPLEX_IMPORT_MAP = {
            "Path": ("pathlib", "Path"),
            "datetime": ("datetime", "datetime"),
            "Optional": ("typing", "Optional"),
            "List": ("typing", "List"),
            "Dict": ("typing", "Dict"),
            "Any": ("typing", "Any"),
            "Agent": ("core.agent_factory_architecture", "Agent"),
            "Task": ("core.agent_factory_architecture", "Task"),
            "Result": ("core.agent_factory_architecture", "Result"),
        }

    async def execute_task(self, task: Task) -> Result:
        code_to_adapt = task.params.get("code")
        feedback = task.params.get("feedback")

        if not code_to_adapt:
            return Result(success=False, error="Le code à adapter n'a pas été fourni.")

        try:
            modules_to_add = []
            complex_imports_to_add = {}
            adaptations = ["Utilisation de LibCST pour la réparation structurelle."]

            if feedback:
                match = re.search(r"name '(\w+)' is not defined", feedback)
                if match:
                    name = match.group(1)
                    self.logger.info(f"Détection d'un 'NameError' via feedback pour : '{name}'.")

                    if name in self.COMPLEX_IMPORT_MAP:
                        module, import_name = self.COMPLEX_IMPORT_MAP[name]
                        if module not in complex_imports_to_add:
                            complex_imports_to_add[module] = []
                        if import_name not in complex_imports_to_add[module]:
                            complex_imports_to_add[module].append(import_name)
                        adaptations.append(f"Ajout de l'import complexe : from {module} import {import_name}")
                    else:
                        if name not in modules_to_add:
                            modules_to_add.append(name)
                        adaptations.append(f"Ajout de l'import simple : {name}")

            tree = cst.parse_module(code_to_adapt)
            modified_tree = tree

            if complex_imports_to_add:
                for module, names in complex_imports_to_add.items():
                    complex_import_adder = CstComplexImportAdder(module, names)
                    modified_tree = modified_tree.visit(complex_import_adder)

            if modules_to_add:
                import_adder = CstImportAdder(modules_to_add)
                modified_tree = modified_tree.visit(import_adder)
            
            pass_inserter = CstPassInserter()
            modified_tree = modified_tree.visit(pass_inserter)
            
            final_code = modified_tree.code
            return Result(success=True, data={"code": final_code, "adaptations": adaptations})

        except cst.ParserSyntaxError as e:
            self.logger.error(f"Erreur de syntaxe CST irrécupérable : {e}")
            return Result(success=False, error=f"Erreur de syntaxe CST : {e}")
        except Exception as e:
            self.logger.error(f"Erreur inattendue lors de l'adaptation CST: {e}")
            return Result(success=False, error=f"Erreur inattendue dans l'adaptateur CST : {e}")

    async def startup(self) -> None:
        self.logger.info(f"Agent Adaptateur CST démarré.")

    async def shutdown(self) -> None:
        self.logger.info(f"Agent Adaptateur CST arrêté.")

    def get_capabilities(self) -> list[str]:
        return ["code_adaptation", "syntax_repair", "name_error_fix"]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "version": self.version}

def create_agent_MAINTENANCE_03_adaptateur_code(**config) -> "AgentMAINTENANCE03AdaptateurCode":
    """Factory function pour créer l'agent."""
    return AgentMAINTENANCE03AdaptateurCode(**config)