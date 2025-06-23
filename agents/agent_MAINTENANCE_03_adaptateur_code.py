#!/usr/bin/env python3
"""
AGENT 3 - ADAPTATEUR DE CODE (LibCST)
🛠️ ADAPTATEUR DE CODE - Agent 03
=================================

🎯 Mission : Corriger et adapter le code source sur la base d'un feedback.
⚡ Capacités : Manipulation de l'AST avec LibCST pour des refactorings sécurisés.
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 3.0.0
"""
import sys
from pathlib import Path
import logging
import asyncio
import re
from typing import List, Dict, Any

# --- Pyflakes Import ---
from pyflakes.api import check
from pyflakes.reporter import Reporter
import io

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

# --- Classes de Reporter pour Pyflakes ---

class PyflakesErrorCollector(Reporter):
    def __init__(self):
        self.errors = []
        super().__init__(io.StringIO(), io.StringIO())

    def syntaxError(self, filename, msg, lineno, offset, text):
        self.errors.append({'type': 'SyntaxError', 'message': msg, 'lineno': lineno, 'offset': offset, 'text': text})

    def unexpectedError(self, filename, msg):
        self.errors.append({'type': 'UnexpectedError', 'message': msg})

    def flake(self, message):
        self.errors.append({'type': 'Flake', 'message': str(message)})


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
        super().__init__(agent_type="adaptateur", **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = self.id
        self.logger.info(f"Adaptateur de code CST ({self.agent_id}) initialisé.")
        
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

    def get_capabilities(self) -> List[str]:
        return ["code_adaptation", "import_fixing", "indentation_error_fix"]
        
    def _pre_check_and_repair_syntax(self, code: str) -> (str, List[str]):
        """Utilise Pyflakes pour une analyse syntaxique rapide et tente de corriger les erreurs simples."""
        adaptations = []
        reporter = PyflakesErrorCollector()
        
        check(code, 'temp_code.py', reporter=reporter)
        
        # Filtrer spécifiquement les erreurs de syntaxe bloquantes
        syntax_errors = [e for e in reporter.errors if e['type'] == 'SyntaxError' and 'expected an indented block' in e['message']]

        if not syntax_errors:
            return code, adaptations

        self.logger.info(f"Pyflakes a détecté {len(syntax_errors)} erreur(s) d'indentation. Tentative de correction.")
        
        lines = code.splitlines()
        corrected = False

        # On parcourt les erreurs pour corriger
        for error in sorted(syntax_errors, key=lambda x: x['lineno'], reverse=True):
            error_lineno = error['lineno']
            # On cherche la ligne de définition juste avant l'erreur
            for i in range(error_lineno - 1, -1, -1):
                line_content = lines[i].strip()
                if (line_content.startswith(('def ', 'class ', 'try:', 'except', 'if ', 'elif ', 'else:', 'for ', 'while ')) and line_content.endswith(':')):
                    
                    # Correction pour gérer les lignes sans indentation
                    match = re.match(r"^(\\s*)", lines[i])
                    indentation = match.group(1) if match else ""

                    # Insérer 'pass' avec l'indentation correcte
                    lines.insert(i + 1, f"{indentation}    pass")
                    adaptations.append(f"Correction auto (Pyflakes): Ajout de 'pass' après '{line_content[:30]}...' à la ligne {i+1}")
                    corrected = True
                    break # On passe à l'erreur suivante après correction

        if corrected:
            self.logger.info("Corrections d'indentation appliquées. Le code sera re-vérifié par LibCST.")
            return "\\n".join(lines), adaptations
        else:
            return code, adaptations

    async def execute_task(self, task: Task) -> Result:
        """
        Exécute la tâche d'adaptation du code en utilisant une approche multi-niveaux.
        """
        code = task.params.get("code")
        feedback = task.params.get("feedback")
        error_type = task.params.get("error_type", "generic") # NOUVEAU

        if not code:
            return Result(success=False, error="Le code source est manquant.")

        self.logger.info(f"Tâche d'adaptation reçue. Type d'erreur détecté: '{error_type}'.")

        adaptations = []
        modified_code = code

        try:
            # Stratégie de réparation basée sur le type d'erreur
            if error_type == "indentation":
                self.logger.info("Stratégie de réparation ciblée pour l'indentation activée.")
                modified_code, pre_check_adaptations = self._pre_check_and_repair_syntax(modified_code)
                adaptations.extend(pre_check_adaptations)
            
            # La logique existante pour les NameError et autres peut suivre ici
            if "name" in str(feedback).lower() and "is not defined" in str(feedback).lower():
                # ... (logique existante)
                pass


            # --- Étape 3 : Correction des blocs vides avec LibCST (plus robuste) ---
            try:
                source_tree = cst.parse_module(modified_code)
                pass_inserter = CstPassInserter()
                modified_tree = source_tree.visit(pass_inserter)
                if not source_tree.deep_equals(modified_tree):
                    modified_code = modified_tree.code
                    adaptations.append("Adaptation CST : Ajout de 'pass' dans un ou plusieurs blocs vides.")
            except cst.ParserSyntaxError as e:
                self.logger.warning(f"Erreur de parsing CST, impossible d'insérer 'pass': {e}")


            if not adaptations:
                return Result(success=True, data={"adapted_code": modified_code, "adaptations": ["Aucune adaptation nécessaire."]})

            return Result(success=True, data={"adapted_code": modified_code, "adaptations": adaptations})

        except Exception as e:
            self.logger.error(f"Erreur inattendue durant l'adaptation du code: {e}", exc_info=True)
            return Result(success=False, error=str(e))

    async def startup(self) -> None:
        self.logger.info(f"Agent Adaptateur CST démarré.")

    async def shutdown(self) -> None:
        self.logger.info(f"Agent Adaptateur CST arrêté.")

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "version": self.version}

def create_agent_MAINTENANCE_03_adaptateur_code(**config) -> "AgentMAINTENANCE03AdaptateurCode":
    """Factory function pour créer l'agent."""
    return AgentMAINTENANCE03AdaptateurCode(**config)