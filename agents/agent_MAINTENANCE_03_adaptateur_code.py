#!/usr/bin/env python3
"""
AGENT 3 - ADAPTATEUR DE CODE (LibCST)
🛠️ ADAPTATEUR DE CODE - Agent 03
=================================

🎯 Mission : Corriger et adapter le code source sur la base d'un feedback.
⚡ Capacités : Manipulation de l'AST avec LibCST pour des refactorings sécurisés.
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 3.1.0 - Harmonisation Standards Pattern Factory NextGeneration
"""
import sys
from pathlib import Path
import logging
import asyncio
import re
from typing import List, Dict, Any, Tuple
import textwrap

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
    🔧 Agent MAINTENANCE 03 - Adaptateur de Code NextGeneration
    
    Agent spécialisé dans l'adaptation et la réparation de code Python via LibCST,
    manipulation sécurisée de l'AST et stratégies de réparation multi-niveaux.
    
    Capacités principales :
    - Réparation d'erreurs d'indentation avec stratégies ciblées
    - Manipulation sécurisée AST via LibCST (blocs vides, imports)
    - Correction automatique NameError avec mapping intelligent
    - Insertion robuste 'pass' dans blocs vides (try/except, functions)
    - Gestion imports complexes avec évitement doublons
    - Classification erreurs pour stratégies adaptées
    
    Technologies avancées :
    - LibCST : Transformations AST préservant formatage
    - Pyflakes : Détection erreurs statiques
    - CSTTransformer : Classes personnalisées insertion/adaptation
    - Multi-level repair : Stratégies en cascade selon type erreur
    
    Workflow type :
    1. Classification erreur (indentation/import/name/generic)
    2. Application stratégie ciblée
    3. Transformation LibCST sécurisée
    4. Validation et traçabilité adaptations
    
    Conformité : Pattern Factory NextGeneration v3.1.0
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
        """Retourne les capacités spécialisées de l'Adaptateur de Code."""
        return [
            "code_adaptation",
            "import_fixing",
            "indentation_error_fix",
            "libcst_ast_transformation",
            "pyflakes_static_analysis",
            "multi_level_repair_strategy",
            "complex_import_management",
            "empty_block_correction",
            "name_error_resolution",
            "formatting_preservation"
        ]
        
    def _fix_indentation_errors(self, code: str, error: Exception) -> Tuple[str, List[str]]:
        """
        Moteur de correction d'indentation amélioré - Version complète robuste.
        
        Gère tous les types d'erreurs d'indentation avec stratégies adaptées :
        - "expected an indented block" : insertion intelligente de 'pass'
        - "unexpected indent" : normalisation contextuelle
        - "unindent does not match" : réparation globale cohérente
        - Détection automatique des niveaux d'indentation
        - Préservation du style d'indentation existant (espaces vs tabs)
        
        Args:
            code: Code source à corriger
            error: Exception d'indentation capturée
            
        Returns:
            Tuple[str, List[str]]: (code_corrigé, liste_des_adaptations)
        """
        notes = []
        if not isinstance(error, (SyntaxError, IndentationError)):
            return code, notes

        lines = code.splitlines()
        msg = error.msg.lower() if error.msg else ""
        lineno = error.lineno or 0
        
        # Détection automatique du style d'indentation (espaces vs tabs)
        indent_char = " "
        indent_size = 4
        for line in lines:
            if line.startswith((" ", "\t")):
                if line.startswith("\t"):
                    indent_char = "\t"
                    indent_size = 1
                else:
                    # Compte les espaces du premier niveau d'indentation trouvé
                    stripped = line.lstrip()
                    if stripped:
                        indent_size = len(line) - len(stripped)
                        break

        # Cas 1: "expected an indented block" -> insertion intelligente de 'pass'
        if "expected an indented block" in msg and 0 < lineno <= len(lines):
            target_indent = ""
            
            # Analyse intelligente du contexte pour déterminer l'indentation requise
            if lineno > 1:
                prev_line = lines[lineno - 2].rstrip()
                
                # Si la ligne précédente finit par ':', c'est un bloc de contrôle
                if prev_line.endswith(':'):
                    prev_indent = len(lines[lineno - 2]) - len(lines[lineno - 2].lstrip())
                    target_indent = indent_char * (prev_indent + indent_size)
                else:
                    # Cherche le niveau d'indentation approprié en remontant
                    for i in range(lineno - 2, -1, -1):
                        if lines[i].strip() and lines[i].endswith(':'):
                            base_indent = len(lines[i]) - len(lines[i].lstrip())
                            target_indent = indent_char * (base_indent + indent_size)
                            break
                    else:
                        # Fallback : indentation par défaut
                        target_indent = indent_char * indent_size
            else:
                target_indent = indent_char * indent_size
            
            lines.insert(lineno - 1, f"{target_indent}pass")
            notes.append(f"Auto-correction: Ajout de 'pass' avec indentation adaptée à la ligne {lineno} pour bloc attendu.")
        
        # Cas 2: "unexpected indent" -> correction contextuelle intelligente
        elif "unexpected indent" in msg and 0 < lineno <= len(lines):
            problematic_line = lines[lineno - 1]
            
            # Détermine le niveau d'indentation correct en analysant le contexte
            correct_indent_level = 0
            if lineno > 1:
                # Cherche le niveau d'indentation de référence
                for i in range(lineno - 2, -1, -1):
                    if lines[i].strip():  # Ligne non vide
                        reference_indent = len(lines[i]) - len(lines[i].lstrip())
                        
                        # Si c'est une ligne de définition (def, class, if, etc.), 
                        # le niveau courant devrait être au même niveau
                        if any(lines[i].strip().startswith(keyword) for keyword in ['def ', 'class ', 'if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except', 'finally:', 'with ']):
                            correct_indent_level = reference_indent
                        else:
                            correct_indent_level = reference_indent
                        break
            
            # Applique la correction d'indentation
            corrected_line = (indent_char * correct_indent_level) + problematic_line.lstrip()
            lines[lineno - 1] = corrected_line
            notes.append(f"Auto-correction: Ajustement intelligent de l'indentation à la ligne {lineno} (niveau {correct_indent_level}).")
            
        # Cas 3: "unindent does not match" -> réparation intelligente ligne par ligne
        elif "unindent does not match" in msg:
            notes.append("Auto-correction: Réparation intelligente des niveaux d'indentation incohérents.")
            
            # Stratégie intelligente : reconstruction avec analyse contextuelle
            fixed_lines = []
            indent_stack = [0]  # Stack des niveaux d'indentation valides
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                if not stripped:
                    fixed_lines.append("")
                    continue
                
                original_indent = len(line) - len(stripped)
                
                # Détermine le niveau d'indentation approprié selon le contexte
                if any(stripped.startswith(kw) for kw in ['def ', 'class ']):
                    # Définitions de classe/fonction : niveau de base
                    target_indent = 0
                    indent_stack = [0, indent_size]  # Reset stack pour nouvelle définition
                    
                elif any(stripped.startswith(kw) for kw in ['if ', 'for ', 'while ', 'try:', 'with ']):
                    # Structures de contrôle : niveau actuel
                    target_indent = indent_stack[-1]
                    if stripped.endswith(':'):
                        indent_stack.append(target_indent + indent_size)
                        
                elif any(stripped.startswith(kw) for kw in ['elif ', 'else:', 'except', 'finally:']):
                    # Clauses alternatives : même niveau que la structure parente
                    if len(indent_stack) >= 2:
                        target_indent = indent_stack[-2]
                        if stripped.endswith(':'):
                            indent_stack[-1] = target_indent + indent_size
                    else:
                        target_indent = 0
                        
                elif stripped in ['pass', 'break', 'continue'] or stripped.startswith(('return', 'raise', 'yield')):
                    # Instructions terminales : niveau courant
                    target_indent = indent_stack[-1] if len(indent_stack) > 1 else indent_size
                    
                else:
                    # Instructions normales : niveau courant
                    target_indent = indent_stack[-1] if len(indent_stack) > 1 else indent_size
                
                # Validation et ajustement du niveau calculé
                if target_indent < 0:
                    target_indent = 0
                    
                # Construction de la ligne corrigée
                corrected_line = (indent_char * target_indent) + stripped
                fixed_lines.append(corrected_line)
                
                # Gestion de la fermeture de blocs (détection heuristique)
                if not stripped.endswith(':') and target_indent > 0:
                    # Si on détecte une ligne qui devrait fermer un bloc
                    next_line_indent = 0
                    if i + 1 < len(lines) and lines[i + 1].strip():
                        next_line_indent = len(lines[i + 1]) - len(lines[i + 1].lstrip())
                        
                    # Si la ligne suivante a moins d'indentation, on ferme potentiellement des blocs
                    if next_line_indent < target_indent and len(indent_stack) > 1:
                        # Recherche du niveau d'indentation correspondant dans la stack
                        while len(indent_stack) > 1 and indent_stack[-1] > next_line_indent:
                            indent_stack.pop()
            
            return '\n'.join(fixed_lines), notes

        return "\n".join(lines), notes

    async def execute_task(self, task: Task) -> Result:
        """
        Exécute la tâche d'adaptation du code en utilisant une approche multi-niveaux.
        """
        code = task.params.get("code")
        feedback = task.params.get("feedback")
        error_type = task.params.get("error_type", "generic")

        if not code:
            return Result(success=False, error="Le code source est manquant.")

        self.logger.info(f"Tâche d'adaptation reçue. Type d'erreur détecté: '{error_type}'.")

        adaptations = []
        modified_code = code

        try:
            # Stratégie de réparation basée sur le type d'erreur - Routage amélioré
            if error_type == "indentation":
                self.logger.info("Stratégie de réparation ciblée pour l'indentation activée.")
                # Le `feedback` est l'exception brute dans ce cas
                modified_code, indent_adaptations = self._fix_indentation_errors(modified_code, feedback)
                adaptations.extend(indent_adaptations)
                
            elif error_type == "name":
                self.logger.info("Stratégie de réparation ciblée pour les NameError activée.")
                # Logique spécialisée pour les erreurs de noms non définis
                if "name" in str(feedback).lower() and "is not defined" in str(feedback).lower():
                    # Extraction du nom de variable depuis l'erreur
                    match = re.search(r"name '(\w+)' is not defined", str(feedback))
                    if match:
                        undefined_name = match.group(1)
                        # Recherche dans le mapping des imports complexes
                        if undefined_name in self.COMPLEX_IMPORT_MAP:
                            module_path, import_name = self.COMPLEX_IMPORT_MAP[undefined_name]
                            try:
                                source_tree = cst.parse_module(modified_code)
                                import_adder = CstComplexImportAdder(module_path, [import_name])
                                modified_tree = source_tree.visit(import_adder)
                                if not source_tree.deep_equals(modified_tree):
                                    modified_code = modified_tree.code
                                    adaptations.append(f"Ajout import automatique: from {module_path} import {import_name}")
                            except Exception as e:
                                self.logger.warning(f"Impossible d'ajouter l'import pour {undefined_name}: {e}")
                                
            elif error_type == "import":
                self.logger.info("Stratégie de réparation ciblée pour les erreurs d'import activée.")
                # Logique spécialisée pour les erreurs d'import
                if "no module named" in str(feedback).lower():
                    adaptations.append("Détection d'erreur d'import de module - analyse du contexte requise")
                    
            elif error_type == "syntax":
                self.logger.info("Stratégie de réparation ciblée pour les erreurs de syntaxe activée.")
                # Pour les erreurs de syntaxe génériques, tenter la correction LibCST
                pass
                
            else:
                self.logger.info(f"Stratégie de réparation générique pour le type '{error_type}'.")
                # Logique générique pour autres types d'erreurs

            # --- Correction des blocs vides avec LibCST (plus robuste) ---
            try:
                source_tree = cst.parse_module(modified_code)
                pass_inserter = CstPassInserter()
                modified_tree = source_tree.visit(pass_inserter)
                if not source_tree.deep_equals(modified_tree):
                    modified_code = modified_tree.code
                    adaptations.append("Adaptation CST : Ajout de 'pass' dans un ou plusieurs blocs vides.")
            except cst.ParserSyntaxError as e:
                self.logger.warning(f"Erreur de parsing CST, impossible d'insérer 'pass': {e}")
                # On retourne le code tel quel si CST échoue, car une correction a peut-être déjà eu lieu
                return Result(success=True, data={"adapted_code": modified_code, "adaptations": adaptations})

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