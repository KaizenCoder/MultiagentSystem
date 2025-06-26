import os
import ast
import uuid
import logging
import re
import importlib.util
import tokenize
import io
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import List, Dict, Any, Tuple
import asyncio
import json
import textwrap

# --- Blocs d'import pour Pattern Factory ---
try:
    from core.agent_factory_architecture import Agent, Task, Result, TaskStatus
except ImportError:
    # En cas d'exécution CLI, ajouter le chemin parent
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.agent_factory_architecture import Agent, Task, Result, TaskStatus

# --- Configuration du Logging ---
LOG_DIR = "logs/agents"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, "agent_MAINTENANCE_12_correcteur_semantique.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s] %(message)s'))
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s: [%(funcName)s] %(message)s'))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# --- Fonctions utilitaires ---
def _safe_rename(source: str, mapping: dict[str, str]) -> str:
    """Renomme uniquement les identifiants de type NAME, en ignorant les chaînes et commentaires."""
    if not mapping: return source
    result = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            tok_type, tok_val, start, end, line = tok
            if tok_type == tokenize.NAME and tok_val in mapping:
                tok = (tok_type, mapping[tok_val], start, end, line)
            result.append(tok)
        return tokenize.untokenize(result)
    except tokenize.TokenError:
        logger.warning("Tokenize a échoué, retour au renommage par regex (moins sûr).")
        for target, suggestion in mapping.items():
            source = re.sub(r'\b' + re.escape(target) + r'\b', suggestion, source)
        return source

def _sort_imports_block(import_lines: List[str]) -> List[str]:
    std_libs = set(sys.stdlib_module_names)
    buckets = {'std': set(), 'third': set(), 'local': set()}
    for line_content in import_lines:
        try:
            root = line_content.split()[1].split('.')[0]
            if root in std_libs: buckets['std'].add(line_content)
            elif root.startswith('core') or root.startswith('agents'): buckets['local'].add(line_content)
            else: buckets['third'].add(line_content)
        except IndexError: continue
    output = []
    for key in ('std', 'third', 'local'):
        if buckets[key]:
            output.extend(sorted(list(buckets[key]))); output.append('')
    return output[:-1] if output else []

def _find_header_end(lines: list[str]) -> int:
    last_import_line = 0
    in_docstring = False
    for i, line_content in enumerate(lines):
        s_line = line_content.strip()
        if i == 0 and s_line.startswith('#!'): continue
        if s_line.startswith(('"""', "'''")) and s_line.count(s_line[:3]) == 1: in_docstring = not in_docstring
        if in_docstring: continue
        if s_line.startswith(('import ', 'from ')): last_import_line = i
    return last_import_line + 1

class CorrecteurSemantique(Agent):
    """Agent 12 - Correcteur Sémantique (v6.5-SOP)"""
    COMMON_IMPORTS = {
        'Path': 'from pathlib import Path', 'Dict': 'from typing import Dict', 'List': 'from typing import List',
        'Result': 'from core.agent_factory_architecture import Result', 'Task': 'from core.agent_factory_architecture import Task',
        'TaskStatus': 'from core.agent_factory_architecture import TaskStatus', 'Agent': 'from core.agent_factory_architecture import Agent',
    }

    def __init__(self, agent_name="CorrecteurSemantique", **kwargs):
        super().__init__(agent_type="correcteur_semantique", **kwargs)
        self.agent_name = agent_name
        self.type = "correcteur_semantique"
        self.logger = logging.getLogger(self.__class__.__name__)
        self.enable_auto_rename = kwargs.get('enable_auto_rename', True)
        self.max_iterations = kwargs.get('max_iterations', 3)

    async def startup(self): self.logger.info(f"Agent {self.agent_name} (v6.5-SOP) démarré. Auto-rename: {'ON' if self.enable_auto_rename else 'OFF'}")
    async def shutdown(self): self.logger.info(f"Agent {self.agent_name} arrêté.")
    def get_capabilities(self) -> List[str]: return ["correct_semantics"]
    async def health_check(self) -> Dict[str, Any]: return {"status": "ok", "timestamp": datetime.now().isoformat()}

    def execute_task(self, task: Task) -> Result:
        correction_id = f"corr-{uuid.uuid4()}"
        self.logger.info(f"[{correction_id}] Début de l'analyse sémantique pour la tâche de type '{task.type}'")
        try:
            # Adaptation à la structure de Task du framework
            if 'code' not in task.params:
                return Result(success=False, error="Le paramètre 'code' est manquant dans la tâche.")
            
            original_code = task.params['code']
            metrics = self._gather_metrics(original_code)
            initial_score = self._calculate_score(metrics)
            self.logger.info(f"[{correction_id}] Score initial : {initial_score:.2f}/100")
            current_code, all_corrections = original_code, []
            for i in range(self.max_iterations):
                self.logger.info(f"[{correction_id}] Itération {i + 1}/{self.max_iterations}")
                metrics = self._gather_metrics(current_code)
                corrections_this_iter, score_improvement = self._generate_corrections(metrics)
                if not corrections_this_iter: self.logger.info(f"[{correction_id}] Plus de corrections trouvées."); break
                new_code, all_corrections = self._apply_corrections(current_code, corrections_this_iter), all_corrections + corrections_this_iter
                new_metrics = self._gather_metrics(new_code)
                if self._calculate_score(new_metrics) <= self._calculate_score(metrics):
                    self.logger.warning(f"[{correction_id}] Le score n'a pas augmenté, arrêt des itérations.")
                    break
                current_code = new_code
            final_score = self._calculate_score(self._gather_metrics(current_code))
            score_improvement = final_score - initial_score
            msg = f"Analyse terminée. {len(all_corrections)} corrections. Amélioration: {score_improvement:.2f} pts."
            
            # Adaptation à la structure de Result du framework
            return Result(success=True, data={
                "correction_id": correction_id, "initial_score": initial_score, "final_score": final_score,
                "score_improvement": score_improvement, "correction_count": len(all_corrections),
                "corrected_code": current_code if score_improvement > 0 else original_code,
                "message": msg
            })
        except Exception as e:
            self.logger.critical(f"[{correction_id}] Erreur inattendue : {e}", exc_info=True)
            return Result(success=False, error=f"Erreur inattendue : {e}")

    def _apply_corrections(self, code: str, corrections: List[Dict[str, Any]]) -> str:
        code = self._apply_renames(code, [c for c in corrections if c['type'] == 'rename'])
        code = self._apply_imports(code, [c for c in corrections if c['type'] == 'add_import'])
        code = self._apply_docstrings(code, [c for c in corrections if c['type'] == 'add_docstring'])
        return code

    def _apply_renames(self, code: str, corrections: List[Dict]) -> str:
        if not corrections or not self.enable_auto_rename: return code
        mapping = {c['target']: c['suggestion'] for c in corrections}
        return _safe_rename(code, mapping)
        
    def _apply_imports(self, code: str, corrections: List[Dict]) -> str:
        if not corrections: return code + '\r\n'
        lines = code.split('\r\n')
        existing_imports = {line.strip() for line in lines if line.strip().startswith(('import ', 'from '))}
        imports_to_add = {c['suggestion'] for c in corrections} - existing_imports
        if not imports_to_add: return '\r\n'.join(lines) + '\r\n'
        sorted_new_imports = _sort_imports_block(list(imports_to_add))
        insert_pos = _find_header_end(lines)
        blank = [''] if lines and insert_pos < len(lines) and lines[insert_pos].strip() else []
        lines[insert_pos:insert_pos] = sorted_new_imports + blank
        return '\r\n'.join(lines) + '\r\n'

    def _apply_docstrings(self, code: str, corrections: List[Dict]) -> str:
        if not corrections: return code
        lines = code.splitlines() # Handles \n and \r\n
        # Separate module docstring from others
        module_doc_correction_obj = None
        other_doc_corrections = []
        for c in corrections:
            if c.get('type') == 'add_docstring': # Ensure we only process docstring corrections
                if c.get('target') == 'module':
                    module_doc_correction_obj = c
                else:
                    other_doc_corrections.append(c)

        # Apply module docstring first if present
        if module_doc_correction_obj:
            suggestion = module_doc_correction_obj["suggestion"]
            # Ensure it's a valid triple-quoted string
            if not (suggestion.startswith('"""') and suggestion.endswith('"""')) and \
               not (suggestion.startswith("'''") and suggestion.endswith("'''")):
                suggestion = f'"""{suggestion}"""'

            start_index = 0
            if lines and lines[0].startswith('#!'): # Handle shebang
                start_index = 1
            
            has_existing_module_doc = False
            if len(lines) > start_index:
                line_to_check = lines[start_index].strip()
                if line_to_check.startswith('"""') or line_to_check.startswith("'''"): # Basic check
                    if (line_to_check.count('"""') % 2 == 0 and line_to_check.count('"""') > 0) or \
                       (line_to_check.count("'''") % 2 == 0 and line_to_check.count("'''") > 0) or \
                       (line_to_check.count('"""') == 1 and not line_to_check.endswith('"""')) or \
                       (line_to_check.count("'''") == 1 and not line_to_check.endswith("'''")):
                        has_existing_module_doc = True
            
            if not has_existing_module_doc:
                lines.insert(start_index, suggestion)
                if start_index + 1 < len(lines) and lines[start_index+1].strip() != "" and not lines[start_index+1].strip().startswith('#'):
                     lines.insert(start_index + 1, "")
                elif start_index + 1 == len(lines):
                     lines.insert(start_index + 1, "")


        current_code_for_ast = "\n".join(lines) # ast.parse expects \n newlines
        try:
            current_ast = ast.parse(current_code_for_ast)
        except SyntaxError as e:
            self.logger.error(f"Syntax error after module docstring (or before func/class docstrings): {e}. Code snippet:\n{current_code_for_ast[:500]}")
            return "\n".join(lines) # Return current lines (which use \n now)

        node_map = {}
        for node in ast.walk(current_ast):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if hasattr(node, 'name'): 
                    node_map[node.name] = node
        
        sorted_other_corrections = sorted(
            [c for c in other_doc_corrections if c.get('target') in node_map], # Filter for existing targets
            key=lambda c: node_map[c['target']].lineno,
            reverse=True
        )

        for cor in sorted_other_corrections:
            target_name = cor['target']
            node = node_map[target_name] 

            if ast.get_docstring(node, clean=False): # Check if docstring already exists in AST
                continue

            line_idx_in_ast_lines = node.lineno - 1 

            if 0 <= line_idx_in_ast_lines < len(lines):
                original_line_content = lines[line_idx_in_ast_lines]
                
                leading_whitespace = ""
                for char_idx, char_in_line in enumerate(original_line_content):
                    if not char_in_line.isspace():
                        leading_whitespace = original_line_content[:char_idx]
                        break
                else: 
                    leading_whitespace = "" # Should not happen for a def/class line
                    
                docstring_indent = leading_whitespace + '    ' # Standard 4-space indent

                suggestion = cor["suggestion"]
                if not (suggestion.startswith('"""') and suggestion.endswith('"""')) and \
                   not (suggestion.startswith("'''") and suggestion.endswith("'''")):
                    suggestion = f'"""{suggestion}"""' # Ensure triple quotes
                
                lines.insert(line_idx_in_ast_lines + 1, docstring_indent + suggestion)
        
        return "\n".join(lines)

    def _gather_metrics(self, code: str) -> Dict[str, Any]:
        tree = ast.parse(code)
        metrics = {"nodes": [], "used_names": set(), "defined_names": set(), "imported_names": set(), "tree": tree}
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.Assign)): metrics["nodes"].append(node)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names: metrics["imported_names"].add(alias.asname or alias.name)
            elif isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Load): metrics["used_names"].add(node.id)
                else: metrics["defined_names"].add(node.id)
        return metrics

    def _calculate_score(self, metrics: Dict[str, Any]) -> float:
        """Calcule un score de qualité sémantique basé sur les métriques."""
        # Note: Cette logique est une ébauche.
        # Idéalement, le score serait plus nuancé.
        corrections, _ = self._generate_corrections(metrics)
        num_violations = len(corrections)
        return max(0, 100 - num_violations * 5)

    def _generate_corrections(self, metrics: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], float]:
        """Génère une liste de corrections basées sur les métriques du code."""
        corrections, violations = [], []
        SNAKE = re.compile(r'^[a-z_][a-z0-9_]*$')
        PASCAL = re.compile(r'^[A-Z][a-zA-Z0-9]*$')

        if not ast.get_docstring(metrics["tree"]):
            violations.append({
                "type": "add_docstring", 
                "target": "module", 
                "suggestion": '"""TODO: Module docstring."""', 
                "line": 0
            })

        for node in metrics["nodes"]:
            if isinstance(node, ast.ClassDef):
                if not PASCAL.match(node.name):
                    violations.append({"type": "rename", "target": node.name, "suggestion": self._to_pascal_case(node.name), "line": node.lineno})
                if not ast.get_docstring(node):
                    violations.append({"type": "add_docstring", "target": node.name, "suggestion": '"""TODO: Class docstring."""', "line": node.lineno})
            
            elif isinstance(node, ast.FunctionDef):
                # Les méthodes "dunder" comme __init__ sont valides en snake_case
                if not node.name.startswith('__') and not SNAKE.match(node.name):
                    violations.append({"type": "rename", "target": node.name, "suggestion": self._to_snake_case(node.name), "line": node.lineno})
                if not ast.get_docstring(node):
                    violations.append({"type": "add_docstring", "target": node.name, "suggestion": '"""TODO: Function docstring."""', "line": node.lineno})

        for v in violations:
            if v['type'] == 'add_docstring':
                corrections.append(v)
        
        score_improvement = len(violations) * 5.0
        return corrections, score_improvement

    def _to_snake_case(self, name: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name); return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    def _to_pascal_case(self, name: str) -> str:
        return ''.join(x.title() for x in name.split('_') if x)
    def _to_upper_case(self, name: str) -> str:
        return name.upper()

def create_agent(**kwargs) -> CorrecteurSemantique:
    """Fonction factory pour créer une instance de l'agent."""
    return CorrecteurSemantique(**kwargs)

if __name__ == '__main__':
    async def main():
        logger.info("=== DÉMONSTRATION DE L'AGENT CORRECTEUR SÉMANTIQUE V6.5-SOP ===")
        agent = CorrecteurSemantique(enable_auto_rename=True)
        await agent.startup()
        test_code = textwrap.dedent('''\
            import os
            class my_calculator:
                def calculateSum(self, x, y):
                    some_value = x + y
                    return some_value
            api_key = "secret_key"
            def anotherFunction():
                my_list = []
                a_task = Task(1, "d", {})
                return my_list
            ''')
        task = Task(type="correct_semantics", params={"code": test_code})
        result = agent.execute_task(task) # execute_task is synchronous
        
        print(f"\nRésultat: {'Succès' if result.success else 'Échec'}")
        if result.success and result.data:
            print(f"Message: {result.data.get('message')}")
            if result.data.get('score_improvement', 0) > 0:
                print("\n--- CODE CORRIGÉ ---")
                print(result.data['corrected_code'])
                print("--- FIN DU CODE ---")
        elif result.error:
            print(f"Erreur: {result.error}")
            
        await agent.shutdown()

    asyncio.run(main())