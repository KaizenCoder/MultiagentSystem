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

# --- Blocs d'import pour test en isolation ---
try:
    from core.agent_factory_architecture import Agent as AgentCore, Task, Result, TaskStatus as Status
except ImportError:
    # Ce bloc ne devrait plus jamais être atteint en production.
    # Il est conservé pour la lisibilité mais signale une erreur de configuration.
    logger.error("Échec de l'import des modules principaux depuis core.agent_factory_architecture. L'agent ne peut pas fonctionner.")
    raise

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
    for line in import_lines:
        try:
            root = line.split()[1].split('.')[0]
            if root in std_libs: buckets['std'].add(line)
            elif root.startswith('core') or root.startswith('agents'): buckets['local'].add(line)
            else: buckets['third'].add(line)
        except IndexError: continue
    output = []
    for key in ('std', 'third', 'local'):
        if buckets[key]:
            output.extend(sorted(list(buckets[key]))); output.append('')
    return output[:-1] if output else []

def _find_header_end(lines: list[str]) -> int:
    last_import_line = 0
    in_docstring = False
    for i, line in enumerate(lines):
        s_line = line.strip()
        if i == 0 and s_line.startswith('#!'): continue
        if s_line.startswith(('"""', "'''")) and s_line.count(s_line[:3]) == 1: in_docstring = not in_docstring
        if in_docstring: continue
        if s_line.startswith(('import ', 'from ')): last_import_line = i
    return last_import_line + 1

class CorrecteurSemantique(AgentCore):
    """Agent 12 - Correcteur Sémantique (v6.5-SOP)"""
    COMMON_IMPORTS = {
        'Path': 'from pathlib import Path', 'Dict': 'from typing import Dict', 'List': 'from typing import List',
        'Result': 'from core.models.result import Result', 'Task': 'from core.models.task import Task',
        'Status': 'from core.models.result import Status', 'AgentCore': 'from core.agent_core import AgentCore',
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

    async def execute_task(self, task: Task) -> Result:
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
                corrections_this_iter = self._generate_corrections(metrics)
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
        if not corrections: return code + '\n'
        lines = code.split('\n')
        existing_imports = {line.strip() for line in lines if line.strip().startswith(('import ', 'from '))}
        imports_to_add = {c['suggestion'] for c in corrections} - existing_imports
        if not imports_to_add: return '\n'.join(lines) + '\n'
        sorted_new_imports = _sort_imports_block(list(imports_to_add))
        insert_pos = _find_header_end(lines)
        blank = [''] if lines and insert_pos < len(lines) and lines[insert_pos].strip() else []
        lines[insert_pos:insert_pos] = sorted_new_imports + blank
        return '\n'.join(lines) + '\n'

    def _apply_docstrings(self, code: str, corrections: List[Dict]) -> str:
        if not corrections: return code
        lines = code.split('\n')
        for cor in sorted(corrections, key=lambda x: x['line'], reverse=True):
            line_idx = cor['line'] - 1
            if 0 <= line_idx < len(lines):
                indent = len(lines[line_idx]) - len(lines[line_idx].lstrip(' '))
                lines.insert(line_idx + 1, ' ' * (indent + 4) + cor["suggestion"])
        return '\n'.join(lines)

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
        return 100.0 - len(self._generate_corrections(metrics)) * 5

    def _generate_corrections(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        corrections, violations = [], []
        SNAKE, PASCAL, UPPER = re.compile(r'^[a-z_][a-z0-9_]*$'), re.compile(r'^[A-Z][a-zA-Z0-9]*$'), re.compile(r'^[A-Z_][A-Z0-9_]*$')
        for node in metrics["nodes"]:
            if isinstance(node, ast.ClassDef):
                if not PASCAL.match(node.name): violations.append({"type": "rename", "target": node.name, "suggestion": self._to_pascal_case(node.name), "line": node.lineno})
                if not ast.get_docstring(node): violations.append({"type": "add_docstring", "target": node.name, "suggestion": '"""TODO: Class docstring."""', "line": node.lineno})
            elif isinstance(node, ast.FunctionDef):
                if not node.name.startswith('__') and not SNAKE.match(node.name): violations.append({"type": "rename", "target": node.name, "suggestion": self._to_snake_case(node.name), "line": node.lineno})
                if not ast.get_docstring(node) and node.name != "__init__": violations.append({"type": "add_docstring", "target": node.name, "suggestion": '"""TODO: Function docstring."""', "line": node.lineno})
            elif isinstance(node, ast.Assign) and metrics.get("tree") and isinstance(metrics["tree"], ast.Module) and node in metrics["tree"].body:
                for target in node.targets:
                    if isinstance(target, ast.Name) and not UPPER.match(target.id): violations.append({"type": "rename", "target": target.id, "suggestion": self._to_upper_case(target.id), "line": node.lineno})
        corrections.extend(violations)
        undefined = metrics["used_names"] - metrics["defined_names"] - metrics["imported_names"] - set(dir(__builtins__))
        corrections.extend([{"type": "add_import", "target": name, "line": 0, "suggestion": self.COMMON_IMPORTS[name]} for name in undefined if name in self.COMMON_IMPORTS])
        return corrections

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
    logger.info("=== DÉMONSTRATION DE L'AGENT CORRECTEUR SÉMANTIQUE V6.5-SOP ===")
    agent = CorrecteurSemantique(enable_auto_rename=True)
    agent.startup()
    test_code = '''
import os
class my_calculator:
    def calculateSum(self, x, y):
        some_value = x + y
        return some_value
api_key = "secret_key"
def anotherFunction():
    my_list = List()
    a_task = Task(1, "d", {})
    return my_list
'''
    task = Task("demo-v6.5", "Appliquer toutes les corrections finales SOP", {"code": test_code})
    result = agent.execute_task(task)
    print(f"\nRésultat: {result.status} - {result.message}")
    if result.data and result.data.get('score_improvement', 0) > 0:
        print("\n--- CODE CORRIGÉ ---"); print(result.data['corrected_code']); print("--- FIN DU CODE ---")
    agent.shutdown()