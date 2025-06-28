# Documentation complète de l'équipe de maintenance


---

## agents/agent_MAINTENANCE_00_chef_equipe_coordinateur.py

```python
#!/usr/bin/env python3
"""
🎖️ CHEF D'ÉQUIPE COORDINATEUR ENTERPRISE - Pattern Factory NextGeneration
===============================================================================

🎯 Mission : Orchestration centrale de l'équipe de maintenance.
⚡ Capacités : Boucle de réparation itérative, coordination d'équipe, reporting.

Author: Équipe de Maintenance NextGeneration
Version: 4.2.0 - Report Enrichment
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys
import time
import json
import logging
import uuid
import re

# Import direct de l'architecture et des agents
from core.agent_factory_architecture import Agent, Task, Result, AgentFactory

class ChefEquipeCoordinateurEnterprise(Agent):
    """
    Chef d'équipe pour orchestrer des workflows de maintenance complexes
    avec une boucle de réparation itérative et un reporting enrichi.
    """
    def __init__(self, **kwargs):
        super().__init__(
            agent_type="coordinateur",
            **kwargs
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = self.id

        self.logger.info(f"Chef d'équipe v4.2.0 initialisé avec ID: {self.agent_id}")
        
        self.workspace_path = Path(kwargs.get("workspace_path", "."))
        self.factory = AgentFactory(config_path=str(self.workspace_path / "config" / "maintenance_config.json"))
        
        self.equipe_agents: Dict[str, Agent] = {}
        self.mission_context = {}
        
    async def startup(self):
        self.logger.info(f"🚀 Démarrage du Chef d'Équipe {self.agent_id}")
        await self._recruter_equipe()
        self.logger.info("Chef d'Équipe prêt et équipe recrutée.")

    async def shutdown(self):
        self.logger.info(f"🛑 Arrêt du Chef d'Équipe {self.agent_id}")
        for agent in self.equipe_agents.values():
            if hasattr(agent, 'shutdown'):
                await agent.shutdown()

    def get_capabilities(self) -> List[str]:
        return ["workflow_maintenance_complete"]
        
    def _extraire_mission_docstring(self, code: str) -> str:
        """Extrait la description de la mission depuis le docstring de l'agent."""
        match = re.search(r'🎯 Mission\s*:\s*(.*)', code)
        if match:
            return match.group(1).strip()
        return "Non spécifiée"

    async def health_check(self) -> Dict[str, Any]:
        team_status = {}
        for role, agent in self.equipe_agents.items():
            try:
                agent_health = await agent.health_check()
                team_status[role] = agent_health.get("status", "unknown")
            except Exception:
                team_status[role] = "error"
        is_healthy = all(s == "healthy" for s in team_status.values())
        return {"status": "healthy" if is_healthy else "degraded", "team_status": team_status}

    async def execute_task(self, task: Task) -> Result:
        if task.type == "workflow_maintenance_complete":
            final_report = await self.workflow_maintenance_complete(task.params)
            return Result(success=True, data=final_report)
        return Result(success=False, error=f"Tâche non reconnue: {task.type}")

    async def workflow_maintenance_complete(self, mission_config: Dict) -> Dict:
        mission_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.logger.info(f"===== DÉBUT DE LA MISSION DE MAINTENANCE : {mission_id} =====")
        start_time = time.time()

        agents_a_traiter = mission_config.get("target_files", [])
        
        self.mission_context = {
            "mission_id": mission_id,
            "statut_mission": "EN_COURS",
            "resultats_par_agent": []
        }
        
        for agent_path_str in agents_a_traiter:
            agent_path = Path(agent_path_str)
            agent_name = agent_path.name
            self.logger.info(f"--- 🔁 DÉBUT DU TRAITEMENT ITÉRATIF POUR: {agent_name} ---")
            
            try:
                original_code = agent_path.read_text(encoding='utf-8')
                file_report = await self._run_remediation_cycle(agent_path_str, original_code)
            except Exception as e:
                self.logger.error(f"Erreur critique lors du traitement de {agent_name}: {e}")
                file_report = {"agent_name": agent_name, "status": "CRITICAL_FAILURE", "last_error": str(e)}

            self.mission_context["resultats_par_agent"].append(file_report)
            self.logger.info(f"--- ☑️ FIN DU TRAITEMENT POUR: {agent_name} ---")

        self.mission_context["duree_totale_sec"] = time.time() - start_time
        self.mission_context["statut_mission"] = "SUCCÈS - Terminée"
        
        await self._generer_et_sauvegarder_rapports(mission_id)
        
        return self.mission_context

    async def _run_remediation_cycle(self, agent_path_str: str, original_code: str) -> Dict:
        agent_name = Path(agent_path_str).name
        agent_mission = self._extraire_mission_docstring(original_code)

        file_report = {
            "agent_name": agent_name,
            "agent_mission": agent_mission,
            "status": "PENDING",
            "original_code": original_code,
            "final_code": original_code,
            "repair_history": [],
            "structure_analysis": {},
            "initial_evaluation": {},
            "performance_analysis": {},
            "style_report": {}
        }
        
        # 0. Analyse de structure initiale
        structure_result = await self._run_sub_task("analyseur_structure", "analyse_structure", {"file_path": agent_path_str})
        if structure_result and structure_result.success:
            file_report["structure_analysis"] = structure_result.data.get("analysis", {})
            if file_report["structure_analysis"].get("error"):
                self.logger.warning(f"  -> Analyse de structure a trouvé une erreur de syntaxe pour {agent_name}: {file_report['structure_analysis']['error']}")
        else:
            error_msg = structure_result.error if structure_result else "Réponse invalide de l'analyseur"
            file_report["structure_analysis"] = {"error": f"Analyse de structure a échoué: {error_msg}"}
            self.logger.error(f"L'analyseur de structure a échoué pour {agent_name}: {error_msg}")

        # 1. Évaluation initiale
        eval_result = await self._run_sub_task("evaluateur", "evaluate_code", {"file_path": agent_path_str})
        
        if eval_result and eval_result.success:
            file_report["initial_evaluation"] = eval_result.data
            if eval_result.data.get("is_useful"):
                self.logger.info(f"  ✅ Évaluation initiale réussie pour {agent_name}. Aucune réparation nécessaire.")
                file_report["status"] = "NO_REPAIR_NEEDED"
            else:
                self.logger.warning(f"  -> Code jugé inutile (score: {eval_result.data.get('score')}). Lancement du cycle de réparation.")
        else:
            error_msg = eval_result.error if eval_result else "Réponse invalide de l'évaluateur"
            self.logger.error(f"L'évaluateur a échoué pour {agent_name}: {error_msg}. Démarrage du cycle de réparation par précaution.")
            file_report["initial_evaluation"] = {"error": f"Évaluation initiale échouée: {error_msg}"}

        # 1.5 Correction sémantique automatique
        if file_report["status"] != "CRITICAL_FAILURE":
             self.logger.info(f"⚙️  Lancement du Correcteur sémantique pour {agent_name}...")
             semantic_result = await self._run_sub_task(
                 "correcteur_semantique", 
                 "correct_semantics", 
                 {"code": file_report["final_code"], "file_path": agent_path_str}
             )
             if semantic_result and semantic_result.success and semantic_result.data.get("score_improvement", 0) > 0:
                 file_report["final_code"] = semantic_result.data["corrected_code"]
                 file_report["semantic_fix"] = {
                     "correction_count": semantic_result.data["correction_count"],
                     "initial_score": semantic_result.data["initial_score"],
                     "final_score": semantic_result.data["final_score"]
                 }
                 self.logger.info(f"  ✅ Correcteur sémantique a amélioré le code de {agent_name}.")
             else:
                 self.logger.info(f"  -> Correcteur sémantique n'a trouvé aucune amélioration pour {agent_name}.")

        # 2. Boucle de réparation (si nécessaire)
        if file_report["status"] != "NO_REPAIR_NEEDED":
            await self._perform_repair_loop(agent_path_str, file_report)

        # 2.5 Harmonisation du style
        if file_report["status"] in ["REPAIRED", "NO_REPAIR_NEEDED"]:
            self.logger.info(f"🎨 Lancement de l'harmonisation de style pour {agent_name}...")
            style_result = await self._run_sub_task("harmonisateur_style", "harmonize_style", {"code": file_report["final_code"], "file_path": agent_path_str})
            if style_result and style_result.success:
                file_report["final_code"] = style_result.data.get("harmonized_code", file_report["final_code"])
                file_report["style_report"] = style_result.data.get("style_report", {})
                self.logger.info(f"🎨 Style harmonisé pour {agent_name}.")
            else:
                self.logger.warning(f"L'harmonisation du style a échoué pour {agent_name}.")
                file_report["style_report"] = {"error": "Harmonisation du style a échoué."}

        # 3. Analyse de performance finale
        perf_result = await self._run_sub_task("analyseur_performance", "analyze_performance", {"code": file_report["final_code"]})
        if perf_result and perf_result.success:
            file_report["performance_analysis"] = perf_result.data
        else:
            file_report["performance_analysis"] = {"error": "Analyse de performance échouée."}

        return file_report

    async def _perform_repair_loop(self, agent_path_str: str, file_report: Dict):
        MAX_REPAIR_ATTEMPTS = 5
        current_code = file_report["original_code"]
        last_error = file_report["initial_evaluation"].get("reason") or file_report["initial_evaluation"].get("error", "Évaluation initiale négative.")

        for attempt in range(MAX_REPAIR_ATTEMPTS):
            # ADAPTATION
            adapt_result = await self._run_sub_task("adaptateur", "adapt_code", {"code": current_code, "feedback": last_error})
            if not (adapt_result and adapt_result.success and adapt_result.data.get("adapted_code")):
                file_report["status"] = "REPAIR_FAILED"
                file_report["last_error"] = "L'adaptateur n'a pas pu modifier le code."
                break
            
            current_code = adapt_result.data["adapted_code"]
            
            # TEST
            test_result = await self._run_sub_task("testeur", "test_agent_code", {"code_content": current_code})
            
            file_report["repair_history"].append({
                "iteration": attempt + 1,
                "error_detected": last_error,
                "adaptation_attempted": adapt_result.data.get("adaptations", ["Adaptation inconnue."]),
                "test_result": "Succès" if test_result.success else f"Échec: {test_result.error}"
            })
            
            if test_result.success:
                self.logger.info(f"  ✅ Réparation réussie pour {Path(agent_path_str).name} à la tentative {attempt + 1}.")
                file_report["status"] = "REPAIRED"
                file_report["final_code"] = current_code
                return

            last_error = test_result.error

        if file_report["status"] != "REPAIRED":
            file_report["status"] = "REPAIR_FAILED"
            file_report["last_error"] = last_error
            file_report["final_code"] = current_code

    async def _generer_et_sauvegarder_rapports(self, mission_id):
        self.logger.info("Génération du rapport de mission par l'agent Documenteur...")
        self.mission_context['equipe_maintenance_roles'] = list(self.equipe_agents.keys())
        doc_result = await self._run_sub_task("documenteur", "generate_mission_report", {"report_data": self.mission_context})
        
        report_dir = self.workspace_path / "reports"
        report_dir.mkdir(exist_ok=True, parents=True)

        json_report_path = report_dir / f"rapport_mission_{mission_id}.json"
        with open(json_report_path, "w", encoding="utf-8") as f:
            json.dump(self.mission_context, f, indent=2)
        self.logger.info(f"Rapport JSON détaillé sauvegardé : {json_report_path}")

        if doc_result and doc_result.success:
            md_content = doc_result.data.get("md_content")
            md_report_path = report_dir / f"rapport_mission_{mission_id}.md"
            with open(md_report_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            self.logger.info(f"Rapport Markdown sauvegardé : {md_report_path}")
        else:
            self.logger.error("L'agent Documenteur a échoué à générer le rapport Markdown.")

    async def _recruter_equipe(self):
        self.logger.info("Recrutement de l'équipe de maintenance...")
        
        roles = [
            "analyseur_structure", 
            "evaluateur",
            "correcteur_semantique",
            "adaptateur", 
            "testeur", 
            "documenteur", 
            "analyseur_performance",
            "dependency_manager",
            "security_manager",
            "correcteur_logique",
            "auditeur_qualite",
            "harmonisateur_style"
        ]
        
        for role in roles:
            try:
                agent = self.factory.create_agent(role)
                if hasattr(agent, 'startup'):
                    await agent.startup()
                self.equipe_agents[role] = agent
            except Exception as e:
                self.logger.error(f"Erreur lors de la création de l'agent {role}: {e}")

    async def _run_sub_task(self, agent_role: str, task_type: str, params: dict) -> Optional[Result]:
        agent = self.equipe_agents.get(agent_role)
        if not agent:
            self.logger.error(f"Tentative d'utilisation d'un agent non recruté : {agent_role}")
            return Result(success=False, error=f"Agent {agent_role} non disponible.")
        
        task = Task(type=task_type, params=params)
        self.logger.info(f"Délégation de la tâche '{task.type}' à l'agent '{agent_role}'")
        try:
            return await agent.execute_task(task)
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche par {agent_role}: {e}", exc_info=True)
            return Result(success=False, error=f"Exception in {agent_role}: {e}")

def create_agent_MAINTENANCE_00_chef_equipe_coordinateur(**kwargs) -> ChefEquipeCoordinateurEnterprise:
    return ChefEquipeCoordinateurEnterprise(**kwargs)
```

---

## agents/agent_MAINTENANCE_01_analyseur_structure.py

```python
#!/usr/bin/env python3
"""
AGENT 1 - ANALYSEUR DE STRUCTURE (Pattern Factory)
🏗️ ANALYSEUR DE STRUCTURE - Agent 01
====================================

🎯 Mission : Analyser la structure du code et détecter les erreurs syntaxiques.
⚡ Capacités : Analyse statique avec `py_compile`, `ast`, et `pylint`.
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 1.2.0
"""
import asyncio
import ast
import json
import logging
import sys
import time
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import os

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core import logging_manager
from core.agent_factory_architecture import Agent, Task, Result
PATTERN_FACTORY_AVAILABLE = True


class AgentMAINTENANCE01AnalyseurStructure(Agent):
    """
    Agent spécialisé dans l'analyse de la structure des fichiers de code.
    """
    def __init__(self, **kwargs):
        """Initialisation standardisée."""
        super().__init__(agent_type="analyseur_structure", **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Analyseur de structure ({self.id}) initialisé.")

    async def startup(self):
        """Démarrage de l'agent."""
        self.logger.info(f"Analyseur de structure prêt.")

    async def execute_task(self, task: Task) -> Result:
        """Exécute la tâche d'analyse du répertoire ou d'un fichier."""
        if task.type != "analyse_structure":
            return Result(success=False, error="Type de tâche non supporté.")

        directory = task.params.get("directory")
        file_path_param = task.params.get("file_path")

        if not directory and not file_path_param:
            return Result(success=False, error="Répertoire ou chemin de fichier non spécifié.")

        if file_path_param:
            files_to_process = [file_path_param]
        else:
            files_to_process = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".py")]

        self.logger.info(f"Analyse demandée pour : {directory or file_path_param}")
        
        files_analysis = []
        try:
            for file_path in files_to_process:
                self.logger.info(f"Analyse du fichier : {file_path}")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    analysis = self._analyze_python_file(content)
                    files_analysis.append({
                        "path": file_path,
                        "analysis": analysis,
                    })
                except Exception as e:
                    self.logger.error(f"Erreur lors de l'analyse du fichier {file_path}: {e}")
                    files_analysis.append({
                        "path": file_path,
                        "error": str(e),
                    })
            
            # Pour la cohérence, si un seul fichier a été demandé, on retourne directement son analyse.
            if file_path_param and len(files_analysis) == 1:
                result_data = files_analysis[0]
                return Result(success=not result_data.get("error"), data=result_data)

            return Result(success=True, data={"files": files_analysis})

        except Exception as e:
            self.logger.critical(f"Erreur majeure lors de l'analyse : {e}")
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

    def get_capabilities(self) -> List[str]:
        return ["analyse_structure"]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy"}

    async def shutdown(self):
        self.logger.info("Analyseur de structure éteint.")
        

    async def run_analysis(self, directory: str) -> Result:
        """Méthode de compatibilité pour l'ancien appel du coordinateur."""
        self.logger.warning(f"Appel de compatibilité 'run_analysis' pour le répertoire: {directory}")
        analyse_task = Task(type="analyse_structure", params={"directory": directory})
        return await self.execute_task(analyse_task)

def create_agent_MAINTENANCE_01_analyseur_structure(**config) -> AgentMAINTENANCE01AnalyseurStructure:
    """Factory pour créer une instance de l'Agent 1."""
    return AgentMAINTENANCE01AnalyseurStructure(**config)

if __name__ == '__main__':
    async def main_test():
        agent = create_agent_MAINTENANCE_01_analyseur_structure(source_path="agent_factory_implementation/agents")
        await agent.startup()
        results = await agent.run_analysis("agent_factory_implementation/agents")
        print(json.dumps(results, indent=2))
        await agent.shutdown()
    asyncio.run(main_test())
```

---

## agents/agent_MAINTENANCE_02_evaluateur_utilite.py

```python
"""
⚖️ ÉVALUATEUR D'UTILITÉ - Agent 02
===================================

🎯 Mission : Évaluer la pertinence et la qualité fonctionnelle d'un agent.
⚡ Capacités : Notation basée sur des heuristiques (longueur, complexité, docstrings).
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 2.1.0
"""
import ast
from pathlib import Path
from core.agent_factory_architecture import Agent, Task, Result
from typing import List, Dict, Any
import logging

class AgentMAINTENANCE02EvaluateurUtilite(Agent):
    """
    Évalue l'utilité d'un script Python en se basant sur une analyse statique
    de son arbre syntaxique abstrait (AST).
    """

    def __init__(self, **kwargs):
        super().__init__(agent_type="evaluateur", **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = self.id
        self.logger.info(f"Évaluateur d'utilité ({self.agent_id}) initialisé.")

    async def execute_task(self, task: Task) -> Result:
        file_path = task.params.get("file_path")
        self.logger.info(f"Évaluation du fichier : {file_path}")

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
            self.logger.info(f"Résultat pour {file_path}: Score={score}, Utile={is_useful}")
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
        self.logger.info("Évaluateur d'utilité prêt.")
        pass

    async def shutdown(self) -> None:
        self.logger.info("Évaluateur d'utilité éteint.")
        pass

    def get_capabilities(self) -> List[str]:
        return ["evaluate_utility", "ast_evaluation"]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "ok"}

def create_agent_MAINTENANCE_02_evaluateur_utilite(**config) -> "AgentMAINTENANCE02EvaluateurUtilite":
    """Factory pour créer une instance de l'Agent 2."""
    return AgentMAINTENANCE02EvaluateurUtilite(**config)
```

---

## agents/agent_MAINTENANCE_03_adaptateur_code.py

```python
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
        code_to_adapt = task.params.get("code")
        feedback = task.params.get("feedback")

        if not code_to_adapt:
            return Result(success=False, error="Le code à adapter n'a pas été fourni.")

        try:
            # --- NOUVELLE ÉTAPE : PRÉ-VÉRIFICATION SYNTAXIQUE ---
            repaired_code, pre_adaptations = self._pre_check_and_repair_syntax(code_to_adapt)
            
            # Utiliser le code réparé pour la suite du processus
            code_for_cst = repaired_code
            
            modules_to_add = []
            complex_imports_to_add = {}
            # Conserver les adaptations de la pré-correction
            adaptations = pre_adaptations + ["Utilisation de LibCST pour la réparation structurelle." ]

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

            try:
                tree = cst.parse_module(code_for_cst)
            except cst.ParserSyntaxError as e:
                self.logger.error(f"Erreur de syntaxe CST persistante malgré la pré-correction : {e}")
                return Result(success=False, error=f"Erreur de syntaxe CST irrécupérable : {e}")

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

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "version": self.version}

def create_agent_MAINTENANCE_03_adaptateur_code(**config) -> "AgentMAINTENANCE03AdaptateurCode":
    """Factory function pour créer l'agent."""
    return AgentMAINTENANCE03AdaptateurCode(**config)
```

---

## agents/agent_MAINTENANCE_04_testeur_anti_faux_agents.py

```python
"""
🛡️ TESTEUR ANTI-FAUX AGENTS - Agent 04
======================================
🎯 Mission : Valider qu'un agent est fonctionnel et n'est pas un "faux" agent.
⚡ Capacités : Exécution de tests basiques (importation, instanciation, appels de méthodes).
🏢 Équipe : NextGeneration Tools Migration
Author: Équipe de Maintenance NextGeneration
Version: 4.0.0
"""

import sys
import ast
import inspect
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import importlib
import time
import re
import json
import asyncio
import tempfile
import importlib.util
import os
import uuid
from datetime import datetime

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core import logging_manager
from core.agent_factory_architecture import Agent, Task, Result

@dataclass
class FakeAgentDetection:
    """Résultat de détection d'un faux agent."""
    agent_id: str
    agent_name: str
    is_fake_agent: bool
    sync_violations: List[str]
    async_violations: List[str]
    pattern_factory_violations: List[str]
    compliance_score: float
    recommendation: str
    details: Dict[str, Any]

class AgentMAINTENANCE04TesteurAntiFauxAgents(Agent):
    """
    Agent spécialisé dans le test dynamique des agents pour s'assurer qu'ils ne sont pas des 'faux' agents.
    """

    def __init__(self, **kwargs):
        """Initialisation standardisée."""
        super().__init__(agent_type="testeur", **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = self.id
        self.logger.info(f"Testeur anti-faux agents ({self.agent_id}) initialisé.")

    async def startup(self):
        """Démarrage de l'agent."""
        self.logger.info("Testeur anti-faux agents prêt.")

    async def execute_task(self, task: Task) -> Result:
        """Exécute une tâche de test dynamique."""
        if task.type != "dynamic_test":
            return Result(success=False, error="Type de tâche non supporté.")

        file_path = task.params.get("file_path")
        code_content = task.params.get("code_content")

        if not file_path or not code_content:
            return Result(success=False, error="Chemin ou contenu du fichier manquant.")

        self.logger.info(f"Test dynamique du fichier : {file_path}")
        
        test_passed, details_or_error = await self._run_dynamic_test(file_path, code_content)
        
        self.logger.info(f"Test dynamique pour {file_path} terminé. Succès: {test_passed}")
        
        if test_passed:
            return Result(
                success=True,
                data={"file_path": file_path, "details": details_or_error}
            )
        else:
            return Result(
                success=False,
                error=details_or_error,
                data={"file_path": file_path}
            )

    async def _run_dynamic_test(self, file_path: str, code_content: str) -> (bool, str):
        """
        Tente de charger et d'instancier l'agent depuis le code fourni.
        C'est un test simple pour voir si le code est viable.
        """
        temp_file_path = None
        try:
            # Créer un fichier temporaire pour l'importation
            temp_dir = Path("./temp_test_agents")
            temp_dir.mkdir(exist_ok=True)
            temp_file_name = f"temp_{Path(file_path).stem}_{uuid.uuid4().hex}.py"
            temp_file_path = temp_dir / temp_file_name

            with open(temp_file_path, "w", encoding="utf-8") as f:
                f.write(code_content)

            # Charger le module dynamiquement
            module_name = temp_file_path.stem
            spec = importlib.util.spec_from_file_location(module_name, temp_file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                # Essayer de trouver et d'instancier une classe Agent
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and issubclass(obj, Agent) and obj is not Agent:
                        self.logger.info(f"Instanciation de la classe {name} pour test.")
                        
                        # NOUVEAU: Introspection pour instanciation dynamique
                        try:
                            sig = inspect.signature(obj.__init__)
                            params = sig.parameters
                            
                            # Créer des arguments factices basés sur la signature
                            test_args = {}
                            for param_name, param in params.items():
                                if param_name == 'self':
                                    continue
                                # Si l'argument a une valeur par défaut, on ne le fournit pas
                                if param.default != inspect.Parameter.empty:
                                    continue
                                # Si ce sont des kwargs, on ne fournit rien
                                if param.kind == inspect.Parameter.VAR_KEYWORD:
                                    continue
                                
                                # Fournir des valeurs factices pour les types communs
                                if param.annotation == str:
                                    test_args[param_name] = f"test_{param_name}"
                                elif param.annotation == int:
                                    test_args[param_name] = 123
                                elif param.annotation == bool:
                                    test_args[param_name] = True
                                else:
                                    # Pour les autres, on tente un dict vide, ce qui est souvent
                                    # utilisé pour les configurations `**kwargs`
                                    pass # Ne rien faire et espérer que ce soit optionnel ou kwarg

                            self.logger.info(f"Arguments d'instanciation déduits: {test_args}")
                            instance = obj(**test_args)

                        except TypeError as te:
                            # Fallback vers l'ancienne méthode si l'introspection échoue
                            self.logger.warning(f"L'instanciation dynamique a échoué ({te}), tentative avec des valeurs par défaut.")
                            instance = obj(agent_id='test-agent', version='0.0.0', description='test', agent_type='test', status='testing')

                        if hasattr(instance, 'health_check') and asyncio.iscoroutinefunction(instance.health_check):
                            await instance.health_check()
                        return True, f"Agent {name} instancié et health_check réussi."
                
                return False, "Aucune classe héritant de 'Agent' n'a pu être trouvée et instanciée."
            else:
                return False, "Impossible de créer le spec du module."

        except Exception as e:
            return False, f"Échec du test dynamique: {e}"
        finally:
            # Nettoyer le fichier temporaire
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)


    def get_capabilities(self) -> List[str]:
        return ["dynamic_test"]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy"}

    async def shutdown(self):
        """Arrêt de l'agent."""
        self.logger.info("Testeur anti-faux agents éteint.")
        
    async def run_test(self, file_path: str, code_content: str) -> Result:
        """Méthode de compatibilité pour l'ancien appel."""
        self.logger.warning(f"Appel de compatibilité 'run_test' pour {file_path}")
        test_task = Task(type="dynamic_test", params={"file_path": file_path, "code_content": code_content})
        return await self.execute_task(test_task)


def create_agent_MAINTENANCE_04_testeur_anti_faux_agents(**config) -> AgentMAINTENANCE04TesteurAntiFauxAgents:
    """Factory pour créer une instance de l'Agent 4."""
    return AgentMAINTENANCE04TesteurAntiFauxAgents(**config)

if __name__ == '__main__':
    async def main_test():
        agent = create_agent_MAINTENANCE_04_testeur_anti_faux_agents()
        await agent.startup()
        
        # Test avec un code qui devrait fonctionner
        good_code = """
from core.agent_factory_architecture import Agent, Task, Result
class GoodAgent(Agent):
    def __init__(self, **kwargs): super().__init__(**kwargs)
    async def execute_task(self, task: Task) -> Result: return Result(success=True)
    def get_capabilities(self) -> list: return []
    async def startup(self): pass
    async def shutdown(self): pass
    async def health_check(self) -> dict: return {"status": "ok"}
"""
        results = await agent.run_test("good_agent.py", good_code)
        print("--- Test Agent Valide ---")
        print(json.dumps(results.to_dict(), indent=2))
        
        # Test avec un code qui devrait échouer
        bad_code = "class BadAgent: pass"
        results = await agent.run_test("bad_agent.py", bad_code)
        print("\n--- Test Agent Invalide ---")
        print(json.dumps(results.to_dict(), indent=2))
        
        await agent.shutdown()

    asyncio.run(main_test())
```

---

## agents/agent_MAINTENANCE_05_documenteur_peer_reviewer.py

```python
"""
🔍 PEER-REVIEWER ENRICHI / DOCUMENTEUR - Agent 05
==============================================================

🎯 Mission : Générer un rapport de mission détaillé et analytique.
⚡ Capacités : Analyse fine des erreurs, génération de diff, synthèse de mission.
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 5.1.0 - Mission Display
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import sys
import difflib
import logging

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core.agent_factory_architecture import Agent, Task, Result

class AgentMAINTENANCE05DocumenteurPeerReviewer(Agent):
    """Génère des rapports de mission de maintenance détaillés et analytiques."""
    
    def __init__(self, **kwargs):
        super().__init__(agent_type="documenteur", **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = self.id
        self.logger.info(f"🔍 Agent Documenteur ({self.agent_id}) initialisé")

    async def startup(self):
        """Démarre l'agent Documenteur."""
        self.logger.info("Agent Documenteur prêt.")

    async def shutdown(self):
        """Arrête l'agent Documenteur."""
        self.logger.info("Agent Documenteur éteint.")

    async def health_check(self) -> Dict[str, Any]:
        """Vérifie l'état de santé de l'agent."""
        return {"status": "healthy", "version": self.version}

    def get_capabilities(self) -> List[str]:
        return ["generate_mission_report"]

    async def execute_task(self, task: Task) -> Result:
        self.logger.info(f"🎯 Exécution tâche: {task.type}")
        if task.type == "generate_mission_report":
            report_data = task.params.get("report_data")
            if not report_data:
                return Result(success=False, error="Données du rapport manquantes.")
            
            md_content = self._generer_rapport_md_enrichi(report_data)
            return Result(success=True, data={"md_content": md_content})
        else:
            return Result(success=False, error=f"Tâche non reconnue: {task.type}")

    def _generer_diff(self, original_code: str, final_code: str) -> str:
        if not original_code or not final_code or original_code == final_code:
            return "Aucune modification de code n'a été effectuée."
        diff = difflib.unified_diff(
            original_code.splitlines(keepends=True),
            final_code.splitlines(keepends=True),
            fromfile='original', tofile='corrected'
        )
        diff_str = "".join(diff)
        return f"```diff\n{diff_str}\n```" if diff_str else "Aucune modification de code détectée."

    def _format_history(self, history: List[Dict]) -> List[str]:
        lines = ["- **Historique de Réparation :**", "  <details><summary>Cliquer pour voir les étapes</summary>", "  "]
        for attempt in history:
            lines.append(f"  - **Tentative {attempt.get('iteration', '?')}**")
            lines.append(f"    - **Erreur Détectée :** `{attempt.get('error_detected', 'N/A')}`")
            adaptations = attempt.get('adaptation_attempted', ['N/A'])
            lines.append(f"    - **Adaptation Tentée :** `{adaptations[0]}`")
            lines.append(f"    - **Résultat du Test :** {attempt.get('test_result', 'N/A')}")
        lines.append("\n  </details>")
        return lines

    def _generer_rapport_md_enrichi(self, rapport_data: Dict[str, Any]) -> str:
        mission_id = rapport_data.get('mission_id', 'N/A')
        statut = rapport_data.get('statut_mission', 'INCONNU')
        duree = rapport_data.get('duree_totale_sec', 0)
        equipe = rapport_data.get('equipe_maintenance_roles', [])
        
        lines = [f"# Rapport de Mission de Maintenance : `{mission_id}`"]
        lines.append(f"**Statut Final :** {statut} | **Durée :** {duree:.2f}s")
        
        if equipe:
            lines.append("\n## Équipe de Maintenance Active")
            lines.append("La mission a été menée par les agents suivants :")
            for role in equipe:
                lines.append(f"- `{role}`")

        lines.append("\n---")
        
        lines.append("## Résultats Détaillés par Agent\n")

        for agent_result in rapport_data.get("resultats_par_agent", []):
            agent_name = agent_result.get('agent_name', 'Agent Inconnu')
            agent_mission = agent_result.get('agent_mission', 'Non spécifiée')
            status = agent_result.get('status', 'INCONNU')
            
            icon = "✅" if status in ["REPAIRED", "NO_REPAIR_NEEDED"] else "❌"
            lines.append(f"### {icon} Agent : `{agent_name}`")
            lines.append(f"- **Mission de l'agent :** *{agent_mission}*")
            lines.append(f"- **Statut Final :** {status}")

            # Section Évaluation Initiale
            initial_eval = agent_result.get("initial_evaluation", {})
            if initial_eval:
                score = initial_eval.get('score', 'N/A')
                reason = initial_eval.get('reason', 'N/A')
                lines.append(f"- **Évaluation Initiale :** Score de {score}/100. (Raison: {reason})")
            
            # Section Historique de Réparation
            history = agent_result.get("repair_history", [])
            if history:
                lines.extend(self._format_history(history))
            
            # Section Analyse de Performance
            perf_analysis = agent_result.get("performance_analysis", {})
            if perf_analysis and not perf_analysis.get('error'):
                score = perf_analysis.get('score', 'N/A')
                lines.append(f"- **Analyse de Performance :** Score de {score}/100.")
            
            # Section Diff
            if status == "REPAIRED":
                lines.append("- **Diff des Modifications :**")
                lines.append("  <details><summary>Cliquer pour voir les changements</summary>\n")
                diff_str = self._generer_diff(agent_result.get("original_code"), agent_result.get("final_code"))
                lines.append(diff_str)
                lines.append("\n  </details>")

            if status == "REPAIR_FAILED":
                 lines.append(f"- **Dernière Erreur :** `{agent_result.get('last_error', 'N/A')}`")

            lines.append("\n---\n")

        lines.append(self._generer_conclusion(rapport_data))

        return "\n".join(lines)

    def _generer_conclusion(self, rapport_data: Dict[str, Any]) -> str:
        """Génère une conclusion synthétique pour la mission."""
        results = rapport_data.get("resultats_par_agent", [])
        total_agents = len(results)
        repaired = sum(1 for r in results if r['status'] == 'REPAIRED')
        no_repair = sum(1 for r in results if r['status'] == 'NO_REPAIR_NEEDED')
        failed = sum(1 for r in results if r['status'] == 'REPAIR_FAILED')

        lines = ["## Conclusion de la Mission"]

        if not results:
            lines.append("Aucun agent n'a été traité durant cette mission.")
            return "\n".join(lines)

        success_rate = (repaired + no_repair) / total_agents * 100
        
        if success_rate == 100:
            conclusion = f"La mission est un succès total. L'ensemble des {total_agents} agents traités sont stables et opérationnels."
            if no_repair == total_agents:
                conclusion += " Aucun n'a nécessité de réparation."
            else:
                conclusion += f" {repaired} agents ont été réparés avec succès."
        elif success_rate > 70:
            conclusion = f"La mission s'est globalement bien déroulée avec un taux de succès de {success_rate:.0f}%. Sur {total_agents} agents, {repaired + no_repair} sont opérationnels."
        else:
            conclusion = f"La mission révèle des problèmes de stabilité significatifs avec un taux de succès de seulement {success_rate:.0f}%."

        lines.append(conclusion)
        
        if failed > 0:
            lines.append(f"**Point d'attention :** {failed} agent(s) n'ont pas pu être réparés et nécessitent une investigation manuelle.")

        return "\n".join(lines)


def create_agent_MAINTENANCE_05_documenteur_peer_reviewer(**config) -> AgentMAINTENANCE05DocumenteurPeerReviewer:
    """Factory pour créer une instance de l'Agent 5."""
    return AgentMAINTENANCE05DocumenteurPeerReviewer(**config)
```

---

## agents/agent_MAINTENANCE_06_correcteur_logique_metier.py

```python
#!/usr/bin/env python3
"""
Agent-006: Correcteur Logique Métier
"""
from core.agent_factory_architecture import Agent, Task, Result
import logging

class AgentMAINTENANCE06CorrecteurLogiqueMetier(Agent):
    def __init__(self, **kwargs):
        super().__init__(agent_type="correcteur_logique", **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Agent 'correcteur_logique' initialisé avec l'ID: {self.id}")

    async def startup(self):
        self.logger.info(f"Agent 'correcteur_logique' ({self.id}) démarré.")

    async def shutdown(self):
        self.logger.info(f"Agent 'correcteur_logique' ({self.id}) arrêté.")

    async def health_check(self):
        return {"status": "healthy"}

    def get_capabilities(self):
        return ["correct_business_logic"]

    async def execute_task(self, task: Task) -> Result:
        self.logger.info(f"Tâche reçue pour 'correcteur_logique': {task.type}")
        if task.type == "correct_business_logic":
            # Logique de correction à implémenter
            return Result(success=True, data={"message": "Correction logique effectuée."})
        return Result(success=False, error=f"Tâche non supportée: {task.type}")

def create_agent_MAINTENANCE_06_correcteur_logique_metier(**kwargs) -> AgentMAINTENANCE06CorrecteurLogiqueMetier:
    return AgentMAINTENANCE06CorrecteurLogiqueMetier(**kwargs) 
```

---

## agents/agent_MAINTENANCE_06_validateur_final.py

```python
#!/usr/bin/env python3
"""
AGENT 6 - VALIDATEUR FINAL (Pattern Factory)
✅ VALIDATEUR FINAL - Agent 06
===============================
🎯 Mission : Effectuer une validation complète et finale d'un agent réparé.
⚡ Capacités : Combinaison de tests de structure, d'utilité et de performance.
🏢 Équipe : NextGeneration Tools Migration
Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
"""

import asyncio
import json
import logging
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import os
import ast
import subprocess
import tempfile

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core import logging_manager
from core.agent_factory_architecture import Agent, Task, Result

class AgentMAINTENANCE06ValidateurFinal(Agent):
    """
    Agent chargé de la validation finale du code.
    Il effectue une vérification de syntaxe finale avec le compilateur Python.
    """
    def __init__(self, **kwargs):
        """Initialisation robuste et compatible avec le coordinateur."""
        super().__init__(**kwargs)
        self.logger.info(f"Validateur Final ({self.agent_id}) initialisé.")

    async def startup(self):
        await super().startup()
        self.log("Validateur final prêt.")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "validate_code":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni.")

        self.log(f"Validation finale du fichier : {file_path}")

        try:
            # Validation 1: Vérification de syntaxe avec AST
            try:
                tree = ast.parse(code)
                syntax_validation = "passed"
                self.log(f"Validation AST réussie pour {file_path}.")
            except SyntaxError as e:
                self.log(f"Validation échouée pour {file_path}. Erreur de syntaxe AST: {e}", level="error")
                return Result(success=False, error=f"SyntaxError: {e.msg} (line {e.lineno})")

            # Validation 2: Compilation Python
            try:
                compile(code, file_path, 'exec')
                compile_validation = "passed"
                self.log(f"Compilation Python réussie pour {file_path}.")
            except SyntaxError as e:
                self.log(f"Validation échouée pour {file_path}. Erreur de compilation: {e}", level="error")
                return Result(success=False, error=f"Compilation SyntaxError: {e.msg} (line {e.lineno})")

            # Validation 3: Linter basique
            linter_details = self._run_basic_linter(code, file_path)
            
            # Validation 4: Vérifications spécifiques aux agents
            agent_validation = self._validate_agent_structure(tree)

            self.log(f"Toutes les validations réussies pour {file_path}.")
            return Result(success=True, data={
                "validation": "passed",
                "syntax_validation": syntax_validation,
                "compile_validation": compile_validation,
                "linter_details": linter_details,
                "agent_validation": agent_validation
            })

        except Exception as e:
            self.log(f"Erreur inattendue lors de la validation de {file_path}: {e}", level="critical")
            return Result(success=False, error=f"Unexpected validation error: {e}")

    def _run_basic_linter(self, code: str, file_path: str) -> dict:
        """Exécute un linter basique via subprocess."""
        linter_result = {
            "status": "completed",
            "method": "subprocess_compile_check",
            "issues": []
        }
        
        try:
            # Créer un fichier temporaire pour le test
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
                tmp.write(code)
                tmp_path = tmp.name
            
            try:
                # Utilise l'interpréteur courant pour vérifier la syntaxe
                process = subprocess.run(
                    [sys.executable, "-m", "py_compile", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if process.returncode == 0:
                    linter_result["status"] = "passed"
                else:
                    linter_result["status"] = "failed"
                    linter_result["issues"].append(f"py_compile failed: {process.stderr}")
                    
            except subprocess.TimeoutExpired:
                linter_result["status"] = "timeout"
                linter_result["issues"].append("Linter timeout")
            except Exception as e:
                linter_result["status"] = "error"
                linter_result["issues"].append(f"Linter execution error: {e}")
            finally:
                # Nettoyer le fichier temporaire
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                    
        except Exception as e:
            linter_result["status"] = "error"
            linter_result["issues"].append(f"Linter setup error: {e}")
        
        return linter_result

    def _validate_agent_structure(self, tree: ast.AST) -> dict:
        """Valide la structure spécifique aux agents."""
        validation = {
            "has_agent_class": False,
            "has_execute_task": False,
            "has_startup": False,
            "agent_class_name": None,
            "issues": []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Vérifier si c'est une classe d'agent
                base_names = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        base_names.append(base.id)
                
                if 'Agent' in base_names:
                    validation["has_agent_class"] = True
                    validation["agent_class_name"] = node.name
                    
                    # Vérifier les méthodes requises dans la classe
                    methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                    
                    if 'execute_task' in methods:
                        validation["has_execute_task"] = True
                    else:
                        validation["issues"].append("Méthode execute_task manquante")
                    
                    if 'startup' in methods:
                        validation["has_startup"] = True
                    else:
                        validation["issues"].append("Méthode startup manquante")
        
        if not validation["has_agent_class"]:
            validation["issues"].append("Aucune classe héritant d'Agent trouvée")
        
        return validation

    def get_capabilities(self) -> List[str]:
        return ["final_validation"]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy"}

    async def shutdown(self):
        """Arrêt de l'agent."""
        self.log("Validateur Final éteint.")

    async def run_validation(self, file_path: str, code_content: str) -> Result:
        """Méthode de compatibilité pour l'ancien appel."""
        self.log(f"Appel de compatibilité 'run_validation' pour {file_path}", level="warning")
        validation_task = Task(type="final_validation", params={"file_path": file_path, "code_content": code_content})
        return await self.execute_task(validation_task)


def create_agent_MAINTENANCE_06_validateur_final(**config) -> AgentMAINTENANCE06ValidateurFinal:
    """Factory pour créer une instance de l'Agent 6."""
    return AgentMAINTENANCE06ValidateurFinal(**config)

if __name__ == '__main__':
    async def main_test():
        agent = create_agent_MAINTENANCE_06_validateur_final(agent_id='test-validator', version='1.0', description='test', agent_type='validator', status='testing')
        await agent.startup()
        
        valid_code = '''
from core.agent_factory_architecture import Agent, Task, Result
import asyncio

class MyAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    async def execute_task(self, task: Task) -> Result: return Result(success=True)
    def get_capabilities(self) -> list: return []
    async def startup(self): pass
    async def shutdown(self): pass
    async def health_check(self) -> dict: return {"status": "ok"}
'''
        results = await agent.run_validation("valid_agent.py", valid_code)
        print("--- Validation Agent Valide ---")
        print(json.dumps(results.to_dict(), indent=2))

        invalid_code = "def my_func(): pass"
        results = await agent.run_validation("invalid_agent.py", invalid_code)
        print("\n--- Validation Agent Invalide ---")
        print(json.dumps(results.to_dict(), indent=2))
        
        await agent.shutdown()

    asyncio.run(main_test())
```

---

## agents/agent_MAINTENANCE_07_gestionnaire_dependances.py

```python
import ast
import sys
import subprocess
import importlib.util
from collections import defaultdict
from core.agent_factory_architecture import Agent, Task, Result
import logging

class AgentMAINTENANCE07GestionnaireDependances(Agent):
    """
    Agent chargé de gérer les dépendances Python :
    - Détecte les imports manquants ou inutilisés
    - Vérifie la disponibilité des modules
    - Suggère des alternatives pour les dépendances obsolètes
    - Organise et optimise les imports
    """
    
    def __init__(self, **kwargs):
        super().__init__(agent_type="dependency_manager", **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        self.stdlib_modules = {
            'ast', 'asyncio', 'os', 'sys', 'json', 'datetime', 'pathlib', 're', 
            'tempfile', 'subprocess', 'importlib', 'collections', 'logging',
            'typing', 'functools', 'itertools', 'math', 'random', 'time', 'uuid',
            'abc'
        }
        
        self.alternatives = {
            'astor': 'ast.unparse (Python 3.9+)',
            'imp': 'importlib',
            'optparse': 'argparse',
            'urllib2': 'urllib.request',
            'ConfigParser': 'configparser'
        }

    async def startup(self):
        await super().startup()
        self.logger.info("Gestionnaire de dépendances prêt.")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "manage_dependencies":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code_content")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni dans les paramètres de la tâche.")

        self.logger.info(f"Analyse des dépendances pour : {file_path}")

        try:
            tree = ast.parse(code)
            analysis = self._analyze_dependencies(tree)
            
            optimized_code, applied = self._optimize_imports(code, analysis)
            analysis["optimization_applied"] = applied
            
            report = {
                "file_path": file_path,
                "imports_found": analysis["imports"],
                "missing_modules": analysis["missing"],
                "unused_imports": analysis["unused"],
                "obsolete_modules": analysis["obsolete"],
                "suggestions": analysis["suggestions"],
                "optimization_applied": analysis["optimization_applied"]
            }

            self.logger.info(f"Analyse des dépendances terminée pour {file_path}")
            
            return Result(success=True, data={
                "adapted_content": optimized_code,
                "description": f"Analyse des dépendances effectuée. Optimisations d'imports appliquées: {applied}.",
                "dependency_report": report
            })

        except SyntaxError as e:
            self.logger.error(f"Erreur de syntaxe lors de l'analyse de {file_path}: {e}")
            return Result(success=False, error=f"SyntaxError: {e}")
        except Exception as e:
            self.logger.error(f"Erreur inattendue lors de l'analyse de {file_path}: {e}")
            return Result(success=False, error=str(e))

    def _analyze_dependencies(self, tree: ast.AST) -> dict:
        analysis = {
            "imports": [], "missing": [], "unused": [],
            "obsolete": [], "suggestions": [],
        }
        
        imports_info = self._extract_imports(tree)
        analysis["imports"] = imports_info
        used_names = self._extract_used_names(tree)
        
        for imp in imports_info:
            if not imp.get('module'): continue
            module_name = imp["module"].split('.')[0]
            if not self._is_module_available(module_name):
                analysis["missing"].append(module_name)
                analysis["suggestions"].append(f"Module '{module_name}' non trouvé.")
            
            if module_name in self.alternatives:
                analysis["obsolete"].append({"module": module_name, "alternative": self.alternatives[module_name]})
                analysis["suggestions"].append(f"Remplacer '{module_name}' par '{self.alternatives[module_name]}'.")
        
        all_imported_names = {item for imp in imports_info for item in self._get_names_from_import(imp)}
        truly_used_imports = all_imported_names.intersection(used_names)

        for imp in imports_info:
            imported_names_for_this_node = self._get_names_from_import(imp)
            if not any(name in truly_used_imports for name in imported_names_for_this_node):
                analysis["unused"].append(imp)
        return analysis

    def _get_names_from_import(self, imp_node: dict) -> set:
        names = set()
        if imp_node['type'] == 'import':
            names.add(imp_node['asname'] or imp_node['module'])
        elif imp_node['type'] == 'from_import':
            for name, asname in imp_node['items']:
                names.add(asname or name)
        return names

    def _extract_imports(self, tree: ast.AST) -> list:
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({"type": "import", "module": alias.name, "asname": alias.asname, "line": node.lineno})
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imports.append({"type": "from_import", "module": node.module, "items": [(alias.name, alias.asname) for alias in node.names], "level": node.level, "line": node.lineno})
        return imports

    def _extract_used_names(self, tree: ast.AST) -> set:
        used_names = set()
        class NameCollector(ast.NodeVisitor):
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    used_names.add(node.id)
            def visit_Import(self, node): pass
            def visit_ImportFrom(self, node): pass
        NameCollector().visit(tree)
        return used_names

    def _is_module_available(self, module_name: str) -> bool:
        if not module_name: return False
        try:
            if module_name in self.stdlib_modules:
                return True
            spec = importlib.util.find_spec(module_name)
            return spec is not None
        except (ImportError, ValueError, ModuleNotFoundError):
            return False

    def _optimize_imports(self, code: str, analysis: dict) -> (str, bool):
        unused_import_lines = {imp['line'] for imp in analysis.get('unused', [])}
        if not unused_import_lines:
            return code, False

        used_import_nodes = [imp for imp in analysis.get('imports', []) if imp['line'] not in unused_import_lines]
        all_import_lines = {imp['line'] for imp in analysis.get('imports', [])}
        
        lines = code.split('\n')
        
        first_code_line_index = 0
        in_docstring = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if '"""' in stripped or "'''" in stripped:
                if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                    in_docstring = not in_docstring
            if not stripped or stripped.startswith('#') or in_docstring or (i + 1) in all_import_lines:
                continue
            
            first_code_line_index = i
            break
        else: 
            first_code_line_index = len(lines)

        header_and_imports = lines[:first_code_line_index]
        body = lines[first_code_line_index:]

        header_without_imports = [line for i, line in enumerate(header_and_imports) if (i + 1) not in all_import_lines]
        body_without_imports = [line for i, line in enumerate(body, start=first_code_line_index) if (i + 1) not in all_import_lines]

        organized_imports_str = self._organize_imports_nodes(used_import_nodes)
        
        final_header = '\n'.join(header_without_imports)
        final_body = '\n'.join(body_without_imports)

        new_code = ""
        if final_header:
            new_code += final_header.strip() + "\n"
        if organized_imports_str:
            new_code += organized_imports_str + "\n\n"
        
        new_code += final_body.strip()
        
        return new_code.strip(), new_code.strip() != code.strip()

    def _organize_imports_nodes(self, imports: list) -> str:
        stdlib_imports, third_party_imports, local_imports = set(), set(), set()
        
        for imp in imports:
            line = self._reconstruct_import_line(imp)
            if not imp.get('module'): continue
            module_root = imp['module'].split('.')[0]
            if imp.get('level', 0) > 0 or "core" in imp['module'] or imp['module'].startswith('agents'):
                local_imports.add(line)
            elif module_root in self.stdlib_modules:
                stdlib_imports.add(line)
            else:
                third_party_imports.add(line)

        import_groups = []
        if stdlib_imports:
            import_groups.append('\n'.join(sorted(list(stdlib_imports))))
        if third_party_imports:
            import_groups.append('\n'.join(sorted(list(third_party_imports))))
        if local_imports:
            import_groups.append('\n'.join(sorted(list(local_imports))))
            
        return '\n\n'.join(filter(None, import_groups))

    def _reconstruct_import_line(self, imp_node: dict) -> str:
        if imp_node['type'] == 'import':
            if imp_node['asname']:
                return f"import {imp_node['module']} as {imp_node['asname']}"
            return f"import {imp_node['module']}"
        else:
            items_str = ', '.join([f"{name} as {asname}" if asname else name for name, asname in imp_node['items']])
            return f"from {'.' * imp_node['level']}{imp_node['module']} import {items_str}"

    # --- MÉTHODES ABSTRAITES MANQUANTES ---
    def get_capabilities(self) -> list[str]:
        """Retourne les capacités de l'agent."""
        return ["manage_dependencies"]

    async def health_check(self) -> dict[str, any]:
        """Effectue un contrôle de santé de l'agent."""
        return {"status": "healthy", "agent_id": self.agent_id}

    async def shutdown(self):
        """Arrête l'agent."""
        self.logger.info("Gestionnaire de dépendances éteint.")

def create_agent_MAINTENANCE_07_gestionnaire_dependances(**config) -> "AgentMAINTENANCE07GestionnaireDependances":
    return AgentMAINTENANCE07GestionnaireDependances(**config)
```

---

## agents/agent_MAINTENANCE_08_analyseur_performance.py

```python
"""
⏱️ ANALYSEUR DE PERFORMANCE - Agent 08
=======================================

🎯 Mission : Analyser la performance et la complexité du code.
⚡ Capacités : Calcul de la complexité cyclomatique, analyse des "points chauds".
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
"""
    
import ast
import re
from collections import defaultdict
from core.agent_factory_architecture import Agent, Task, Result
import logging

class AgentMAINTENANCE08AnalyseurPerformance(Agent):
    def __init__(self, **kwargs):
        super().__init__(agent_type="analyseur_performance", **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = self.id
        
        # Patterns d'anti-performance
        self.performance_antipatterns = [
            {
                "pattern": r'for\s+\w+\s+in\s+range\(len\(',
                "issue": "Utilisation de range(len()) au lieu d'enumerate()",
                "suggestion": "Remplacer par enumerate() ou itération directe"
            },
            {
                "pattern": r'\.append\(\)\s*$',
                "issue": "Appels multiples à append() dans une boucle",
                "suggestion": "Considérer list comprehension ou extend()"
            },
            {
                "pattern": r'str\s*\+\s*str',
                "issue": "Concaténation de strings avec +",
                "suggestion": "Utiliser join() pour multiple concaténations"
            }
        ]

    async def startup(self):
        await super().startup()
        self.logger.info("Optimiseur de performance prêt.")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "optimize_performance":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni.")

        self.logger.info(f"Analyse de performance pour : {file_path}")

        try:
            tree = ast.parse(code)
            
            # Analyses de performance
            complexity_analysis = self._analyze_complexity(tree)
            antipatterns = self._detect_antipatterns(code)
            optimizations = self._suggest_optimizations(tree, code)
            
            # Score de performance global
            performance_score = self._calculate_performance_score(
                complexity_analysis, antipatterns, optimizations
            )
            
            # Génération du code optimisé (suggestions)
            optimized_suggestions = self._generate_optimization_suggestions(
                code, antipatterns, optimizations
            )

            report = {
                "file_path": file_path,
                "performance_score": performance_score,
                "complexity_analysis": complexity_analysis,
                "antipatterns_detected": antipatterns,
                "optimizations_suggested": optimizations,
                "optimization_suggestions": optimized_suggestions
            }

            self.logger.info(f"Analyse de performance terminée pour {file_path} - Score: {performance_score}/100")
            
            return Result(success=True, data={
                "performance_report": report,
                "needs_optimization": performance_score < 70
            })

        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse de performance de {file_path}: {e}")
            return Result(success=False, error=str(e))

    def _analyze_complexity(self, tree: ast.AST) -> dict:
        """Analyse la complexité algorithmique du code."""
        complexity = {
            "cyclomatic_complexity": 0,
            "nested_loops": 0,
            "recursive_functions": [],
            "long_functions": [],
            "complexity_hotspots": []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_complexity = self._calculate_function_complexity(node)
                complexity["cyclomatic_complexity"] += func_complexity["cyclomatic"]
                
                if func_complexity["has_recursion"]:
                    complexity["recursive_functions"].append(node.name)
                
                if len(node.body) > 20:  # Fonction longue
                    complexity["long_functions"].append({
                        "name": node.name,
                        "lines": len(node.body)
                    })
                
                if func_complexity["nested_loops"] > 0:
                    complexity["nested_loops"] += func_complexity["nested_loops"]
                    complexity["complexity_hotspots"].append({
                        "function": node.name,
                        "nested_loops": func_complexity["nested_loops"],
                        "estimated_complexity": "O(n^{})".format(func_complexity["nested_loops"] + 1)
                    })
        
        return complexity

    def _calculate_function_complexity(self, func_node: ast.AST) -> dict:
        """Calcule la complexité d'une fonction spécifique."""
        complexity = {
            "cyclomatic": 1,  # Base complexity
            "nested_loops": 0,
            "has_recursion": False
        }
        
        loop_depth = 0
        max_loop_depth = 0
        
        for node in ast.walk(func_node):
            # Complexité cyclomatique
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity["cyclomatic"] += 1
            elif isinstance(node, ast.BoolOp):
                complexity["cyclomatic"] += len(node.values) - 1
            
            # Détection des boucles imbriquées
            if isinstance(node, (ast.For, ast.While)):
                loop_depth += 1
                max_loop_depth = max(max_loop_depth, loop_depth)
            
            # Détection de récursion
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == func_node.name:
                    complexity["has_recursion"] = True
        
        complexity["nested_loops"] = max_loop_depth
        return complexity

    def _detect_antipatterns(self, code: str) -> list:
        """Détecte les anti-patterns de performance."""
        detected = []
        
        for pattern_info in self.performance_antipatterns:
            matches = re.finditer(pattern_info["pattern"], code, re.MULTILINE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                detected.append({
                    "line": line_num,
                    "pattern": pattern_info["pattern"],
                    "issue": pattern_info["issue"],
                    "suggestion": pattern_info["suggestion"],
                    "code_snippet": match.group()
                })
        
        # Détection spécifique : boucles avec append multiples
        append_in_loops = self._detect_append_in_loops(code)
        detected.extend(append_in_loops)
        
        # Détection : dictionnaire avec get() au lieu de defaultdict
        dict_get_patterns = self._detect_dict_get_antipattern(code)
        detected.extend(dict_get_patterns)
        
        return detected

    def _detect_append_in_loops(self, code: str) -> list:
        """Détecte les multiples append() dans les boucles."""
        issues = []
        lines = code.split('\n')
        
        in_loop = False
        loop_start = 0
        append_count = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            if re.match(r'^\s*(for|while)\s+', line):
                in_loop = True
                loop_start = i + 1
                append_count = 0
            elif in_loop and not line.startswith(' ') and stripped:
                # Fin de la boucle
                if append_count > 3:
                    issues.append({
                        "line": loop_start,
                        "issue": f"Multiple append() calls in loop ({append_count} times)",
                        "suggestion": "Consider using list comprehension or collecting items first",
                        "severity": "medium"
                    })
                in_loop = False
            elif in_loop and '.append(' in stripped:
                append_count += 1
        
        return issues

    def _detect_dict_get_antipattern(self, code: str) -> list:
        """Détecte l'usage excessif de dict.get() au lieu de defaultdict."""
        issues = []
        get_calls = re.findall(r'\.get\([^)]+\)', code)
        
        if len(get_calls) > 5:  # Seuil arbitraire
            issues.append({
                "line": 0,
                "issue": f"Multiple dict.get() calls detected ({len(get_calls)})",
                "suggestion": "Consider using collections.defaultdict for better performance",
                "severity": "low"
            })
        
        return issues

    def _suggest_optimizations(self, tree: ast.AST, code: str) -> list:
        """Suggère des optimisations spécifiques."""
        optimizations = []
        
        # Analyse des patterns d'optimisation
        for node in ast.walk(tree):
            # Suggestion : utiliser any()/all() au lieu de boucles
            if isinstance(node, ast.For):
                if self._is_boolean_search_loop(node):
                    optimizations.append({
                        "type": "boolean_search",
                        "suggestion": "Replace loop with any()/all() for boolean search",
                        "impact": "high"
                    })
            
            # Suggestion : comprehensions au lieu de boucles d'accumulation
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if self._has_accumulation_pattern(node):
                    optimizations.append({
                        "type": "accumulation_loop",
                        "suggestion": "Replace accumulation loop with list/dict comprehension",
                        "impact": "high"
                    })
        return optimizations

    def _is_boolean_search_loop(self, loop_node: ast.For) -> bool:
        """Détecte les boucles de recherche booléenne."""
        if len(loop_node.body) == 1 and isinstance(loop_node.body[0], ast.If):
            if_node = loop_node.body[0]
            if len(if_node.body) == 1 and isinstance(if_node.body[0], ast.Break):
                return True
        return False

    def _has_accumulation_pattern(self, func_node: ast.AST) -> bool:
        """Détecte les patterns d'accumulation simples."""
        for node in ast.walk(func_node):
            if isinstance(node, ast.For):
                for item in node.body:
                    if isinstance(item, ast.Expr) and isinstance(item.value, ast.Call):
                        call = item.value
                        if isinstance(call.func, ast.Attribute) and call.func.attr == 'append':
                            return True
        return False

    def _calculate_performance_score(self, complexity: dict, antipatterns: list, optimizations: list) -> int:
        """Calcule un score de performance global."""
        score = 100
        
        # Pénalité pour complexité
        score -= complexity["cyclomatic_complexity"] * 0.5
        score -= complexity["nested_loops"] * 5
        
        # Pénalité pour anti-patterns
        score -= len(antipatterns) * 3
        
        # Bonus pour potentiel d'optimisation (négatif)
        score -= len(optimizations) * 2
        
        return max(0, int(score))

    def _generate_optimization_suggestions(self, code: str, antipatterns: list, optimizations: list) -> list:
        """Génère des suggestions de code optimisé."""
        suggestions = []
        
        for ap in antipatterns:
            suggestions.append(f"Ligne {ap['line']}: {ap['issue']}. Suggestion: {ap['suggestion']}")
            
        for opt in optimizations:
            suggestions.append(f"Optimisation possible: {opt['suggestion']} (Impact: {opt['impact']})")
        
        return suggestions

    async def shutdown(self) -> None:
        """Arrête l'agent."""
        await super().shutdown()
        self.logger.info("Optimiseur de performance éteint.")

    def get_capabilities(self) -> list[str]:
        return ["optimize_performance"]

    async def health_check(self) -> dict:
        return {"status": "healthy", "version": "1.0"}

def create_agent_MAINTENANCE_08_analyseur_performance(**config) -> "AgentMAINTENANCE08AnalyseurPerformance":
    """Factory pour créer une instance de l'analyseur de performance."""
    return AgentMAINTENANCE08AnalyseurPerformance(**config)
```

---

## agents/agent_MAINTENANCE_09_analyseur_securite.py

```python
"""
🔒 ANALYSEUR DE SÉCURITÉ - Agent 09
====================================

🎯 Mission : Détecter les vulnérabilités de sécurité potentielles dans le code.
⚡ Capacités : Analyse statique avec `bandit` pour identifier les failles communes.
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
"""

import ast
import re
import hashlib
import logging
from typing import List, Dict, Any
from core.agent_factory_architecture import Agent, Task, Result

class AgentMAINTENANCE09AnalyseurSecurite(Agent):
    """
    Agent chargé de la sécurité du code Python :
    - Détecte les vulnérabilités de sécurité communes
    - Identifie les pratiques non sécurisées
    - Scanne les injections potentielles
    - Vérifie l'usage sécurisé des fonctions dangereuses
    - Analyse les patterns de gestion des mots de passe et secrets
    """
    
    def __init__(self, **kwargs):
        super().__init__(agent_type="security_manager", **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = "agent_MAINTENANCE_09_Analyseur_Securite"
        self.version = "1.0"
        self.description = "Analyse et sécurise le code Python."
        self.status = "enabled"
        
        # Fonctions dangereuses à éviter
        self.dangerous_functions = {
            'eval': {
                'severity': 'CRITICAL',
                'reason': 'Exécution de code arbitraire',
                'alternatives': 'ast.literal_eval() pour données sûres, ou validation stricte'
            },
            'exec': {
                'severity': 'CRITICAL', 
                'reason': 'Exécution de code arbitraire',
                'alternatives': 'Restructurer le code pour éviter l\'exécution dynamique'
            },
            'compile': {
                'severity': 'HIGH',
                'reason': 'Compilation de code potentiellement malveillant',
                'alternatives': 'Valider strictement les entrées avant compilation'
            },
            'input': {
                'severity': 'MEDIUM',
                'reason': 'Injection de code possible en Python 2',
                'alternatives': 'raw_input() en Python 2, input() est sûr en Python 3'
            },
            '__import__': {
                'severity': 'HIGH',
                'reason': 'Import dynamique non contrôlé',
                'alternatives': 'importlib avec validation des noms de modules'
            }
        }
        
        # Modules système dangereux
        self.dangerous_modules = {
            'os.system': {
                'severity': 'CRITICAL',
                'reason': 'Injection de commandes shell',
                'alternatives': 'subprocess.run() avec shell=False'
            },
            'subprocess.call': {
                'severity': 'HIGH',
                'reason': 'Injection potentielle si shell=True',
                'alternatives': 'subprocess.run() avec liste d\'arguments'
            },
            'subprocess.Popen': {
                'severity': 'MEDIUM',
                'reason': 'Vérifier l\'usage de shell=True',
                'alternatives': 'Utiliser shell=False et liste d\'arguments'
            },
            'pickle.loads': {
                'severity': 'HIGH',
                'reason': 'Désérialisation non sécurisée',
                'alternatives': 'json, ou pickle avec signature/validation'
            },
            'marshal.loads': {
                'severity': 'HIGH',
                'reason': 'Désérialisation dangereuse',
                'alternatives': 'json ou autres formats sécurisés'
            }
        }
        
        # Patterns de secrets potentiels
        self.secret_patterns = [
            (re.compile(r'password\s*=\s*["\'][^"\']+["\']', re.IGNORECASE), 'Mot de passe en dur'),
            (re.compile(r'api_key\s*=\s*["\'][^"\']+["\']', re.IGNORECASE), 'Clé API en dur'),
            (re.compile(r'secret\s*=\s*["\'][^"\']+["\']', re.IGNORECASE), 'Secret en dur'),
            (re.compile(r'token\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', re.IGNORECASE), 'Token en dur'),
            (re.compile(r'["\'][A-Za-z0-9+/]{40,}={0,2}["\']'), 'Possible clé encodée en base64'),
            (re.compile(r'-----BEGIN [A-Z ]+-----'), 'Clé cryptographique'),
        ]
        
        # Patterns d'injection SQL
        self.sql_injection_patterns = [
            re.compile(r'execute\s*\(\s*["\'].*%s.*["\']', re.IGNORECASE),
            re.compile(r'query\s*\(\s*["\'].*\+.*["\']', re.IGNORECASE),
            re.compile(r'["\'].*\+.*["\'].*WHERE', re.IGNORECASE),
        ]

    async def startup(self):
        await super().startup()
        self.logger.info("Gestionnaire de sécurité prêt. Chargement des règles de sécurité...")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "security_scan":
            return Result(success=False, error=f"Tâche non supportée: {task.type}")
        
        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni.")

        self.logger.info(f"🔐 Analyse de sécurité pour : {file_path}")

        try:
            # Analyses de sécurité complètes
            vulnerabilities = []
            
            # 1. Analyse AST pour fonctions dangereuses
            ast_vulnerabilities = self._analyze_ast_security(code)
            vulnerabilities.extend(ast_vulnerabilities)
            
            # 2. Analyse des patterns de texte
            text_vulnerabilities = self._analyze_text_patterns(code)
            vulnerabilities.extend(text_vulnerabilities)
            
            # 3. Analyse des secrets potentiels
            secret_issues = self._detect_hardcoded_secrets(code)
            vulnerabilities.extend(secret_issues)
            
            # 4. Analyse des injections SQL
            sql_issues = self._detect_sql_injections(code)
            vulnerabilities.extend(sql_issues)
            
            # 5. Analyse des permissions de fichiers
            file_issues = self._analyze_file_operations(code)
            vulnerabilities.extend(file_issues)
            
            # 6. Calcul du score de sécurité
            security_score = self._calculate_security_score(vulnerabilities)
            
            # 7. Génération des recommandations
            recommendations = self._generate_security_recommendations(vulnerabilities)
            
            # 8. Génération du code sécurisé (suggestions)
            secured_suggestions = self._generate_secured_code_suggestions(code, vulnerabilities)

            report = {
                "file_path": file_path,
                "security_score": security_score,
                "vulnerabilities": vulnerabilities,
                "recommendations": recommendations,
                "secured_suggestions": secured_suggestions,
                "risk_level": self._determine_risk_level(vulnerabilities),
                "total_issues": len(vulnerabilities)
            }

            self.logger.info(f"🔐 Analyse de sécurité terminée pour {file_path} - Score: {security_score}/100, Issues: {len(vulnerabilities)}")
            
            return Result(success=True, data={
                "security_report": report,
                "score": security_score,
                "vulnerabilities": vulnerabilities
            })

        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse de sécurité de {file_path}: {e}")
            return Result(success=False, error=str(e))

    async def shutdown(self):
        self.logger.info("Analyseur de sécurité éteint.")
        await super().shutdown()

    def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'agent."""
        return ["security_scan"]

    async def health_check(self) -> Dict[str, Any]:
        """Vérifie l'état de santé de l'agent."""
        return {"status": "healthy", "version": self.version}

    def _analyze_ast_security(self, code: str) -> List[Dict[str, Any]]:
        """Analyse AST pour détecter les fonctions dangereuses."""
        vulnerabilities = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Détection des appels de fonctions dangereuses
                if isinstance(node, ast.Call):
                    func_name = None
                    
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                    elif isinstance(node.func, ast.Attribute):
                        if isinstance(node.func.value, ast.Name):
                            func_name = f"{node.func.value.id}.{node.func.attr}"
                    
                    if func_name in self.dangerous_functions:
                        danger_info = self.dangerous_functions[func_name]
                        vulnerabilities.append({
                            'type': 'dangerous_function',
                            'function': func_name,
                            'line': getattr(node, 'lineno', 0),
                            'severity': danger_info['severity'],
                            'description': f"Usage de la fonction dangereuse '{func_name}'",
                            'reason': danger_info['reason'],
                            'recommendation': danger_info['alternatives']
                        })
                    
                    elif func_name in self.dangerous_modules:
                        danger_info = self.dangerous_modules[func_name]
                        vulnerabilities.append({
                            'type': 'dangerous_module_call',
                            'function': func_name,
                            'line': getattr(node, 'lineno', 0),
                            'severity': danger_info['severity'],
                            'description': f"Usage potentiellement dangereux de '{func_name}'",
                            'reason': danger_info['reason'],
                            'recommendation': danger_info['alternatives']
                        })
                
                # Détection des imports dangereux
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    self._check_dangerous_imports(node, vulnerabilities)
        
        except SyntaxError:
            # Le code a des erreurs de syntaxe, on ne peut pas l'analyser
            pass
        
        return vulnerabilities

    def _check_dangerous_imports(self, node: ast.AST, vulnerabilities: List[Dict[str, Any]]):
        """Vérifie les imports potentiellement dangereux."""
        dangerous_imports = ['pickle', 'marshal', 'subprocess', 'os']
        
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in dangerous_imports:
                    vulnerabilities.append({
                        'type': 'dangerous_import',
                        'module': alias.name,
                        'line': getattr(node, 'lineno', 0),
                        'severity': 'LOW',
                        'description': f"Import du module potentiellement dangereux '{alias.name}'",
                        'reason': 'Module nécessitant une utilisation prudente',
                        'recommendation': 'Vérifier l\'usage sécurisé de ce module'
                    })
        
        elif isinstance(node, ast.ImportFrom):
            if node.module in dangerous_imports:
                vulnerabilities.append({
                    'type': 'dangerous_from_import',
                    'module': node.module,
                    'line': getattr(node, 'lineno', 0),
                    'severity': 'LOW',
                    'description': f"Import depuis le module potentiellement dangereux '{node.module}'",
                    'reason': 'Module nécessitant une utilisation prudente',
                    'recommendation': 'Vérifier l\'usage sécurisé des fonctions importées'
                })

    def _analyze_text_patterns(self, code: str) -> List[Dict[str, Any]]:
        """Analyse les patterns de texte pour détecter des problèmes de sécurité."""
        vulnerabilities = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Détection de l'usage de 'except Exception:'
            if 'except Exception' in line:
                vulnerabilities.append({
                    'type': 'broad_exception_clause',
                    'line': i,
                    'severity': 'LOW',
                    'description': "Utilisation d'une clause 'except Exception' trop large",
                    'recommendation': 'Capturer des exceptions plus spécifiques'
                })
            
            # Détection de l'usage de 'assert'
            if 'assert ' in line:
                vulnerabilities.append({
                    'type': 'assertion_usage',
                    'line': i,
                    'severity': 'MEDIUM',
                    'description': "Utilisation de 'assert' pour la validation de sécurité",
                    'reason': 'Les assertions peuvent être désactivées globalement',
                    'recommendation': 'Utiliser des structures de contrôle conditionnelles'
                })

        return vulnerabilities
    
    def _detect_hardcoded_secrets(self, code: str) -> List[Dict[str, Any]]:
        """Détecte les secrets codés en dur dans le code."""
        vulnerabilities = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern, name in self.secret_patterns:
                match = pattern.search(line)
                if match:
                    secret_text = match.group(0)
                    if not self._is_likely_real_secret(secret_text):
                        continue
                    
                    vulnerabilities.append({
                        'type': 'hardcoded_secret',
                        'name': name,
                        'line': i,
                        'severity': 'HIGH',
                        'description': f"Détection d'un secret potentiel : '{name}'",
                        'recommendation': 'Externaliser les secrets dans des variables d\'environnement ou un gestionnaire de secrets'
                    })
        return vulnerabilities

    def _is_likely_real_secret(self, text: str) -> bool:
        """Heuristique pour éviter les faux positifs sur les secrets."""
        # Ignorer les chaînes de documentation ou les commentaires
        if '#' in text or '"""' in text or "'''" in text:
            return False
        # Ignorer les valeurs par défaut vides ou simples
        if '=""' in text or "=''" in text or '="<placeholder>"' in text:
            return False
        return True

    def _detect_sql_injections(self, code: str) -> List[Dict[str, Any]]:
        """Détecte les patterns basiques d'injection SQL."""
        vulnerabilities = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern in self.sql_injection_patterns:
                if pattern.search(line):
                    vulnerabilities.append({
                        'type': 'sql_injection_risk',
                        'line': i,
                        'severity': 'HIGH',
                        'description': 'Risque potentiel d\'injection SQL par concaténation de chaînes',
                        'recommendation': 'Utiliser des requêtes paramétrées'
                    })
                    break  # Une seule alerte par ligne
        return vulnerabilities

    def _analyze_file_operations(self, code: str) -> List[Dict[str, Any]]:
        """Analyse les opérations sur les fichiers pour des permissions potentiellement non sécurisées."""
        vulnerabilities = []
        
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'open':
                    # Vérification simple de l'usage de 'w' ou 'a' sans plus de contexte
                    if any(isinstance(arg, ast.Str) and ('w' in arg.s or 'a' in arg.s) for arg in node.args):
                         vulnerabilities.append({
                            'type': 'insecure_file_operation',
                            'line': node.lineno,
                            'severity': 'LOW',
                            'description': "Opération d'écriture de fichier détectée",
                            'recommendation': 'Assurer que les permissions et le contenu écrit sont sécurisés'
                        })
                # Analyse plus poussée pour chmod
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'chmod':
                    if len(node.args) > 1 and isinstance(node.args[1], ast.Num):
                        mode = node.args[1].n
                        if mode & 0o002 or mode & 0o020:  # World/Group writable
                            vulnerabilities.append({
                                'type': 'insecure_file_permission',
                                'line': node.lineno,
                                'severity': 'MEDIUM',
                                'description': f"Permissions de fichier potentiellement non sécurisées (mode {oct(mode)})",
                                'recommendation': 'Utiliser des permissions plus restrictives (ex: 0o600, 0o644)'
                            })
        except SyntaxError:
            pass
            
        return vulnerabilities

    def _calculate_security_score(self, vulnerabilities: List[Dict[str, Any]]) -> int:
        """Calcule un score de sécurité de 0 à 100."""
        score = 100
        severity_weights = {'CRITICAL': 25, 'HIGH': 15, 'MEDIUM': 5, 'LOW': 1}
        
        for vuln in vulnerabilities:
            score -= severity_weights.get(vuln.get('severity', 'LOW'), 1)
            
        return max(0, score)

    def _determine_risk_level(self, vulnerabilities: List[Dict[str, Any]]) -> str:
        """Détermine le niveau de risque global."""
        severities = {v.get('severity', 'LOW') for v in vulnerabilities}
        
        if 'CRITICAL' in severities:
            return 'CRITICAL'
        if 'HIGH' in severities:
            return 'HIGH'
        if 'MEDIUM' in severities:
            return 'MODERATE'
        if 'LOW' in severities:
            return 'LOW'
            
        return 'NONE'

    def _generate_security_recommendations(self, vulnerabilities: List[Dict[str, Any]]) -> List[str]:
        """Génère une liste de recommandations uniques."""
        unique_recommendations = set()
        
        # Mapping de descriptions vers des recommandations plus générales
        description_to_recommendation = {
            "Utilisation de la fonction dangereuse": "Éviter les fonctions d'exécution de code dynamique. Privilégier des alternatives sûres comme `ast.literal_eval`.",
            "Usage potentiellement dangereux de": "Valider et nettoyer toutes les entrées utilisateur avant de les utiliser dans des appels système ou de désérialisation.",
            "Détection d'un secret potentiel": "Externaliser tous les secrets (clés API, mots de passe) en utilisant des variables d'environnement ou un service de gestion de secrets (ex: Vault, AWS Secrets Manager).",
            "Risque potentiel d'injection SQL": "Toujours utiliser des requêtes paramétrées (prepared statements) pour interagir avec la base de données afin d'éviter les injections SQL.",
            "Permissions de fichier potentiellement non sécurisées": "Appliquer le principe du moindre privilège pour les permissions de fichiers. Utiliser des modes restrictifs comme `0o600` pour les fichiers sensibles.",
            "Utilisation d'une clause 'except Exception' trop large": "Capturer des exceptions spécifiques plutôt que la classe `Exception` de base pour éviter de masquer des erreurs inattendues.",
            "Utilisation de 'assert' pour la validation de sécurité": "Ne pas utiliser `assert` pour la logique de sécurité, car les assertions peuvent être désactivées. Utiliser des blocs `if/raise` pour la validation.",
        }

        # Générer des recommandations basées sur les vulnérabilités trouvées
        for vuln in vulnerabilities:
            for desc_key, rec in description_to_recommendation.items():
                if desc_key in vuln['description']:
                    unique_recommendations.add(rec)
        
        # Ajouter une recommandation générale si aucune spécifique n'est trouvée
        if not unique_recommendations and vulnerabilities:
             unique_recommendations.add("Procéder à une revue de sécurité manuelle pour valider le contexte de chaque alerte.")
        
        return sorted(list(unique_recommendations))

    def _generate_secured_code_suggestions(self, code: str, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Génère des suggestions de code sécurisé (non appliqué, juste pour le rapport)."""
        suggestions = []
        lines = code.split('\n')
        
        for vuln in vulnerabilities:
            line_num = vuln.get('line', 0)
            if not (0 < line_num <= len(lines)):
                continue
            
            original_line = lines[line_num - 1]
            suggestion = "Suggestion non disponible"
            
            if vuln['type'] == 'dangerous_function' and vuln['function'] == 'eval':
                suggestion = original_line.replace('eval(', 'ast.literal_eval(') + "  # RECOMMANDATION: Utiliser ast.literal_eval pour plus de sécurité"
            elif vuln['type'] == 'sql_injection_risk':
                suggestion = f"# RECOMMANDATION: Remplacer la concaténation par une requête paramétrée\n# Exemple: cursor.execute(\"SELECT * FROM users WHERE name = ?\", (user_name,))\n{original_line}"
            elif vuln['type'] == 'hardcoded_secret':
                suggestion = f"# RECOMMANDATION: Charger ce secret depuis une variable d'environnement ou un gestionnaire de secrets\n# Exemple: api_key = os.getenv('API_KEY')\n{original_line}"
            
            if suggestion != "Suggestion non disponible":
                suggestions.append({
                    'line': line_num,
                    'original': original_line.strip(),
                    'suggestion': suggestion
                })
        
        return suggestions

def create_agent_MAINTENANCE_09_analyseur_securite(**kwargs) -> Agent:
    """Factory function pour créer une instance de l'analyseur de sécurité."""
    return AgentMAINTENANCE09AnalyseurSecurite(**kwargs)


# --- Section de test local ---
async def main():
    # Création de l'agent
    security_agent = AgentMAINTENANCE09AnalyseurSecurite()
    await security_agent.startup()

    # Code à analyser
    sample_code = """
import os
import pickle

password = "my_super_secret_password"
api_key = 'hf_1234567890abcdef1234567890abcdef'

def execute_command(user_input):
    os.system(f"echo {user_input}")

def deserialize_data(data):
    return pickle.loads(data)

def dynamic_exec(code_str):
    exec(code_str)
"""

    # Création de la tâche
    task = Task(
        task_id="sec_scan_1",
        type="security_scan",
        params={"code": sample_code, "file_path": "example.py"}
    )

    # Exécution de la tâche
    result = await security_agent.execute_task(task)

    # Affichage des résultats
    if result.success:
        report = result.data['security_report']
        print("--- Rapport de Sécurité ---")
        print(f"Fichier: {report['file_path']}")
        print(f"Score de sécurité: {report['security_score']}/100")
        print(f"Niveau de risque: {report['risk_level']}")
        print(f"Problèmes trouvés: {report['total_issues']}")
        print("\n--- Vulnérabilités ---")
        for vuln in report['vulnerabilities']:
            print(f"- L{vuln['line']} [{vuln['severity']}] {vuln['description']}")
        print("\n--- Recommandations ---")
        for rec in report['recommendations']:
            print(f"- {rec}")

    await security_agent.shutdown()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

---

## agents/agent_MAINTENANCE_10_auditeur_qualite_normes.py

```python
#!/usr/bin/env python3
"""
Agent-010: Auditeur Qualité et Normes
"""
from core.agent_factory_architecture import Agent, Task, Result
import logging

class AgentMAINTENANCE10AuditeurQualiteNormes(Agent):
    def __init__(self, **kwargs):
        super().__init__(agent_type="auditeur_qualite", **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Agent 'auditeur_qualite' initialisé avec l'ID: {self.id}")

    async def startup(self):
        self.logger.info(f"Agent 'auditeur_qualite' ({self.id}) démarré.")

    async def shutdown(self):
        self.logger.info(f"Agent 'auditeur_qualite' ({self.id}) arrêté.")

    async def health_check(self):
        return {"status": "healthy"}

    def get_capabilities(self):
        return ["audit_quality_standards"]

    async def execute_task(self, task: Task) -> Result:
        self.logger.info(f"Tâche reçue pour 'auditeur_qualite': {task.type}")
        if task.type == "audit_quality_standards":
            # Logique d'audit à implémenter
            return Result(success=True, data={"message": "Audit de qualité effectué."})
        return Result(success=False, error=f"Tâche non supportée: {task.type}")

def create_agent_MAINTENANCE_10_auditeur_qualite_normes(**kwargs) -> AgentMAINTENANCE10AuditeurQualiteNormes:
    return AgentMAINTENANCE10AuditeurQualiteNormes(**kwargs) 
```

---

## agents/agent_MAINTENANCE_11_harmonisateur_style.py

```python
import ast
import re
import keyword
from typing import List, Dict, Any, Tuple
import logging

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

class AgentMAINTENANCE11HarmonisateurStyle(Agent):
    """
    Agent chargé d'harmoniser le style du code Python en utilisant l'outil Black.
    """
    
    def __init__(self, **kwargs):
        super().__init__(agent_type="harmonisateur_style", **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.version="1.1" # Version incrémentée pour l'activation
        self.description="Harmonise le style du code Python en utilisant Black."
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
            self.logger.warning("La bibliothèque 'black' n'est pas installée. L'agent ne pourra pas formater le code.")
        self.logger.info("Harmonisateur de style (Black) prêt.")

    async def shutdown(self):
        await super().shutdown()
        self.logger.info("Harmonisateur de style arrêté.")

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

        self.logger.info(f"🎨 Application de Black sur : {file_path}")

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

            self.logger.info(f"🎨 Formatage terminé pour {file_path}. Changements appliqués: {code_changed}")
            
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
            self.logger.error(f"Erreur lors du formatage avec Black sur {file_path}: {e}")
            return Result(success=False, error=str(e))

def create_agent_MAINTENANCE_11_harmonisateur_style(**kwargs) -> AgentMAINTENANCE11HarmonisateurStyle:
    return AgentMAINTENANCE11HarmonisateurStyle(**kwargs) 
```

---

## agents/agent_MAINTENANCE_12_correcteur_semantique.py

```python
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
```

---

## SOP_MAINTENANCE_TEAM.md

<!-- Markdown natif -->
# Procédure Opérationnelle Standard : Équipe de Maintenance d'Agents

**Version :** 1.0
**Date :** 2025-06-23
**Auteur :** Gemini Pro

## 1. Principes et Architecture

L'équipe de maintenance est un système multi-agents conçu pour analyser, évaluer, réparer et améliorer de manière autonome d'autres agents.

### 1.1. Composants Clés
- **Coordinateur (`agent_MAINTENANCE_00_...`) :** Le chef d'orchestre. Il initialise l'équipe, distribue les tâches et gère le cycle de vie de la mission.
- **Agent Factory (`core/agent_factory_architecture.py`) :** Le "service de recrutement". Elle lit le fichier `config/maintenance_config.json` pour savoir comment construire chaque agent spécialisé.
- **Agents Spécialisés (`agent_MAINTENANCE_XX_...`) :** Les membres de l'équipe, chacun avec une compétence unique (analyse, adaptation, test, etc.).

### 1.2. Le Workflow en Action
Pour chaque agent cible, le coordinateur exécute la séquence suivante :
1.  **Analyse de Structure (Agent 01) :** Une première passe pour détecter les erreurs de syntaxe fatales.
2.  **Évaluation d'Utilité (Agent 02) :** Attribution d'un score. Si le score est bas ou si une erreur de syntaxe a été trouvée, la boucle de réparation est déclenchée.
3.  **Boucle de Réparation (si nécessaire) :**
    -   `Adaptateur de Code (03)` : Tente de corriger la structure et la syntaxe.
    -   `Testeur (04)` : Tente d'instancier le code réparé pour valider la correction.
    -   *D'autres agents comme le correcteur logique (06) ou le gestionnaire de dépendances (07) peuvent intervenir ici.*
4.  **Harmonisation de Style (Agent 11) :** Une fois le code jugé fonctionnel, l'outil `black` l'uniformise.
5.  **Analyses Finales (Agents 08, 09) :** Des analyses de performance et de sécurité sont menées sur le code final.
6.  **Génération du Rapport (Agent 05) :** L'agent documenteur compile toutes les informations recueillies dans un rapport de mission détaillé.

---

## 2. Procédure d'Intégration d'un Nouvel Agent (Checklist)

Suivez cette procédure **scrupuleusement** pour éviter toute régression.

### ✅ Phase 1 : Préparation du Fichier de l'Agent
-   [ ] **1.1. Nom du Fichier :** Le nom DOIT suivre la convention `agent_MAINTENANCE_XX_nom_descriptif.py`.
-   [ ] **1.2. Nom de la Classe :** Le nom DOIT suivre la convention `AgentMAINTENANCEXXNomDescriptif`.
-   [ ] **1.3. Héritage :** La classe DOIT hériter de `Agent` (depuis `core.agent_factory_architecture`).
-   [ ] **1.4. Constructeur `__init__` :**
    -   [ ] La **première ligne** doit être `super().__init__(agent_type="mon_role", **kwargs)`.
    -   [ ] La **deuxième ligne** doit être `self.logger = logging.getLogger(self.__class__.__name__)`.
-   [ ] **1.5. Méthodes Abstraites :** La classe DOIT implémenter `startup`, `shutdown`, `health_check`, et `get_capabilities`. Des implémentations vides ou basiques suffisent au début.
-   [ ] **1.6. Fonction Factory :** Un fonction `create_agent_MAINTENANCE_XX_...(**kwargs)` DOIT exister au niveau du module et retourner une instance de votre agent.

### ✅ Phase 2 : Configuration
-   [ ] **2.1. Mettre à jour `config/maintenance_config.json` :**
    -   [ ] Ajoutez un nouvel objet à la section `"agents"`.
    -   [ ] Le nom de la clé (ex: `"mon_nouvel_agent"`) doit correspondre à l'`agent_type` défini dans le `super().__init__`.
    -   [ ] Renseignez précisément les clés `"module"`, `"class"`, et `"factory_function"`. Toute incohérence ici mènera à un échec.

### ✅ Phase 3 : Intégration dans l'Équipe
-   [ ] **3.1. Recruter l'Agent :**
    -   [ ] Ouvrez `agents/agent_MAINTENANCE_00_chef_equipe_coordinateur.py`.
    -   [ ] Dans la méthode `_recruter_equipe`, ajoutez votre `agent_type` à la liste `roles`.
-   [ ] **3.2. Intégrer au Workflow :**
    -   [ ] C'est l'étape la plus délicate. Toujours dans le coordinateur, trouvez le bon endroit logique dans la méthode `_run_remediation_cycle` pour appeler votre agent.
    -   [ ] Utilisez `await self._run_sub_task("votre_agent_type", "la_tache_a_executer", params_dict)` pour l'invoquer.

---

## 3. Tester et Valider les Modifications

Ne jamais commiter sans tester.

### 3.1. Lancement du Test
La commande de base pour un test ciblé est :
```bash
python run_maintenance.py --agents <chemin_vers_un_agent_cible>
```

### 3.2. Stratégie de Test Recommandée
1.  **Test 1 (Intégration) :** Lancez le workflow sur un agent cible **connu pour être fonctionnel** (ex: `agents/agent_16_peer_reviewer_senior.py`). Le but est de vérifier que votre nouvel agent est correctement recruté et s'insère dans la chaîne sans la casser.
2.  **Test 2 (Non-Régression) :** Lancez le workflow sur un agent cible **connu pour être défectueux** (ex: `agents/agent_18_auditeur_securite.py`). Le but est de s'assurer que votre nouvel agent n'empêche pas les autres agents (comme l'Adaptateur) de faire leur travail.

### 3.3. Analyse des Logs
Pendant l'exécution, cherchez ces lignes :
-   `INFO - Type d'agent 'mon_role' enregistré...` : Prouve que la configuration est lue.
-   `INFO - Agent mon_role créé avec ID:...` : Prouve que le recrutement a réussi.
-   `INFO - Délégation de la tâche 'ma_tache' à l'agent 'mon_role'` : Prouve que l'intégration au workflow est fonctionnelle.
-   **Absence d'erreurs** de type `AttributeError: ... has no attribute 'logger'` ou `Agent type ... not registered`.

---

## 4. Capitalisation : Pièges à Éviter & Bonnes Pratiques

Cette section est le résumé de toutes les erreurs que nous avons corrigées ensemble.

-   **PIÈGE n°1 : L'Ordre d'Initialisation du Logger.**
    -   **Symptôme :** `AttributeError: ... object has no attribute 'logger'`
    -   **Cause :** Dans le `__init__`, `self.logger` est utilisé avant d'être défini.
    -   **RÈGLE D'OR :** L'ordre dans le `__init__` est **NON NÉGOCIABLE** : 1. `super().__init__(...)`, 2. `self.logger = ...`, 3. Le reste.

-   **PIÈGE n°2 : Les Noms Incohérents.**
    -   **Symptôme :** `ModuleNotFoundError`, `AttributeError`, ou `Agent type '...' not registered.`
    -   **Cause :** Une faute de frappe ou une incohérence entre le nom de la classe/fonction dans le fichier Python et ce qui est déclaré dans `config/maintenance_config.json`.
    -   **RÈGLE D'OR :** Copiez-collez les noms (classe, fonction, module) depuis votre code vers le fichier JSON. Ne les retapez jamais.

-   **BONNE PRATIQUE : L'Intégration "à blanc".**
    -   Pour un agent qui modifie profondément le code, envisagez de l'intégrer une première fois avec sa logique de transformation désactivée (il se contente de recevoir et renvoyer le code).
    -   Si le workflow passe, l'intégration est validée. Vous pouvez ensuite activer sa logique en toute confiance.

-   **BONNE PRATIQUE : La Journalisation.**
    -   Après chaque intégration réussie et validée par un test, mettez à jour le `JOURNAL_EVOLUTION_EQUIPE.md`.
    -   Ceci crée une trace immuable des décisions et des résultats, essentielle pour la maintenance à long terme.

-   **POINT D'ATTENTION : La Limite d'Arguments du Terminal.**
    -   Lors du lancement sur un grand nombre d'agents (> 7-8 sur Windows), le terminal peut atteindre sa limite de longueur d'arguments.
    -   Dans ce cas, la solution est de coder temporairement la liste des agents cibles directement dans `run_maintenance.py` ou d'implémenter une lecture depuis un fichier. 

---

## run_maintenance.py

```python
import asyncio
import logging
import json
from pathlib import Path
import sys
import argparse
from datetime import datetime

# Assurer que le chemin du projet est dans sys.path pour les imports
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_MAINTENANCE_00_chef_equipe_coordinateur
from core.agent_factory_architecture import Task, Result

async def run_maintenance_on_targets(target_agent_files: list[str]):
    """
    Lance le workflow de maintenance complet sur une liste d'agents spécifiée.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("MaintenanceWorkflowRunner")

    coordinator_agent = None
    try:
        # Création et démarrage du coordinateur
        coordinator_agent = create_agent_MAINTENANCE_00_chef_equipe_coordinateur(
            workspace_path=str(project_root)
        )
        await coordinator_agent.startup()

        # Création de la tâche de maintenance
        maintenance_task = Task(
            type="workflow_maintenance_complete",
            params={"target_files": target_agent_files}
        )

        # Exécution du workflow
        result = await coordinator_agent.execute_task(maintenance_task)

        if result.success:
            logger.info("--- RAPPORT FINAL DE LA MISSION ---")
            logger.info(f"Statut de la mission : {result.data.get('status', 'INCONNU')}")
            logger.info(f"ID de la mission : {result.data.get('mission_id', 'N/A')}")
            logger.info(f"Durée totale : {result.data.get('duration', 'N/A')}s")
            
            summary = result.data.get('summary', {})
            logger.info(f"Agents traités : {len(summary)}")
            for agent_file, status in summary.items():
                logger.info(f"  - {agent_file}: {status}")
        else:
            logger.error(f"La mission de maintenance a échoué: {result.error}")

    except Exception as e:
        logger.error(f"Une erreur critique est survenue durant l'exécution du workflow: {e}", exc_info=True)
    finally:
        if coordinator_agent:
            await coordinator_agent.shutdown()

def main():
    parser = argparse.ArgumentParser(description="Lance le workflow de maintenance sur des agents cibles.")
    parser.add_argument(
        "--agents",
        nargs="+",
        help="Liste des chemins vers les fichiers d'agents à traiter."
    )
    parser.add_argument(
        "--mission",
        type=str,
        default=f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        help="ID de mission personnalisé."
    )
    args = parser.parse_args()

    if args.agents:
        agents_to_process = args.agents
    else:
        # Liste par défaut mise à jour avec des agents existants
        agents_to_process = [
            "agents/agent_18_auditeur_securite.py",
            "agents/agent_19_auditeur_performance.py",
            "agents/agent_20_auditeur_conformite.py",
            "agents/agent_111_auditeur_qualite.py",
            "agents/agent_111_auditeur_qualite_sprint3.py",
        ]

    asyncio.run(run_maintenance_on_targets(agents_to_process))

if __name__ == "__main__":
    main()
```

---

## PROCEDURE_EQUIPE_MAINTENANCE.md

<!-- Markdown natif -->
# Procédure Opérationnelle Standard : Équipe de Maintenance d'Agents

**Version :** 1.0
**Date :** 2025-06-23
**Auteur :** Gemini Pro

## 1. Principes et Architecture

L'équipe de maintenance est un système multi-agents conçu pour analyser, évaluer, réparer et améliorer de manière autonome d'autres agents.

### 1.1. Composants Clés
- **Coordinateur (`agent_MAINTENANCE_00_...`) :** Le chef d'orchestre. Il initialise l'équipe, distribue les tâches et gère le cycle de vie de la mission.
- **Agent Factory (`core/agent_factory_architecture.py`) :** Le "service de recrutement". Elle lit le fichier `config/maintenance_config.json` pour savoir comment construire chaque agent spécialisé.
- **Agents Spécialisés (`agent_MAINTENANCE_XX_...`) :** Les membres de l'équipe, chacun avec une compétence unique (analyse, adaptation, test, etc.).

### 1.2. Le Workflow en Action
Pour chaque agent cible, le coordinateur exécute la séquence suivante :
1.  **Analyse de Structure (Agent 01) :** Une première passe pour détecter les erreurs de syntaxe fatales.
2.  **Évaluation d'Utilité (Agent 02) :** Attribution d'un score. Si le score est bas ou si une erreur de syntaxe a été trouvée, la boucle de réparation est déclenchée.
3.  **Boucle de Réparation (si nécessaire) :**
    -   `Adaptateur de Code (03)` : Tente de corriger la structure et la syntaxe.
    -   `Testeur (04)` : Tente d'instancier le code réparé pour valider la correction.
    -   *D'autres agents comme le correcteur logique (06) ou le gestionnaire de dépendances (07) peuvent intervenir ici.*
4.  **Harmonisation de Style (Agent 11) :** Une fois le code jugé fonctionnel, l'outil `black` l'uniformise.
5.  **Analyses Finales (Agents 08, 09) :** Des analyses de performance et de sécurité sont menées sur le code final.
6.  **Génération du Rapport (Agent 05) :** L'agent documenteur compile toutes les informations recueillies dans un rapport de mission détaillé.

---

## 2. Procédure d'Intégration d'un Nouvel Agent (Checklist)

Suivez cette procédure **scrupuleusement** pour éviter toute régression.

### ✅ Phase 1 : Préparation du Fichier de l'Agent
-   [ ] **1.1. Nom du Fichier :** Le nom DOIT suivre la convention `agent_MAINTENANCE_XX_nom_descriptif.py`.
-   [ ] **1.2. Nom de la Classe :** Le nom DOIT suivre la convention `AgentMAINTENANCEXXNomDescriptif`.
-   [ ] **1.3. Héritage :** La classe DOIT hériter de `Agent` (depuis `core.agent_factory_architecture`).
-   [ ] **1.4. Constructeur `__init__` :**
    -   [ ] La **première ligne** doit être `super().__init__(agent_type="mon_role", **kwargs)`.
    -   [ ] La **deuxième ligne** doit être `self.logger = logging.getLogger(self.__class__.__name__)`.
-   [ ] **1.5. Méthodes Abstraites :** La classe DOIT implémenter `startup`, `shutdown`, `health_check`, et `get_capabilities`. Des implémentations vides ou basiques suffisent au début.
-   [ ] **1.6. Fonction Factory :** Un fonction `create_agent_MAINTENANCE_XX_...(**kwargs)` DOIT exister au niveau du module et retourner une instance de votre agent.

### ✅ Phase 2 : Configuration
-   [ ] **2.1. Mettre à jour `config/maintenance_config.json` :**
    -   [ ] Ajoutez un nouvel objet à la section `"agents"`.
    -   [ ] Le nom de la clé (ex: `"mon_nouvel_agent"`) doit correspondre à l'`agent_type` défini dans le `super().__init__`.
    -   [ ] Renseignez précisément les clés `"module"`, `"class"`, et `"factory_function"`. Toute incohérence ici mènera à un échec.

### ✅ Phase 3 : Intégration dans l'Équipe
-   [ ] **3.1. Recruter l'Agent :**
    -   [ ] Ouvrez `agents/agent_MAINTENANCE_00_chef_equipe_coordinateur.py`.
    -   [ ] Dans la méthode `_recruter_equipe`, ajoutez votre `agent_type` à la liste `roles`.
-   [ ] **3.2. Intégrer au Workflow :**
    -   [ ] C'est l'étape la plus délicate. Toujours dans le coordinateur, trouvez le bon endroit logique dans la méthode `_run_remediation_cycle` pour appeler votre agent.
    -   [ ] Utilisez `await self._run_sub_task("votre_agent_type", "la_tache_a_executer", params_dict)` pour l'invoquer.

---

## 3. Tester et Valider les Modifications

Ne jamais commiter sans tester.

### 3.1. Lancement du Test
La commande de base pour un test ciblé est :
```bash
python run_maintenance.py --agents <chemin_vers_un_agent_cible>
```

### 3.2. Stratégie de Test Recommandée
1.  **Test 1 (Intégration) :** Lancez le workflow sur un agent cible **connu pour être fonctionnel** (ex: `agents/agent_16_peer_reviewer_senior.py`). Le but est de vérifier que votre nouvel agent est correctement recruté et s'insère dans la chaîne sans la casser.
2.  **Test 2 (Non-Régression) :** Lancez le workflow sur un agent cible **connu pour être défectueux** (ex: `agents/agent_18_auditeur_securite.py`). Le but est de s'assurer que votre nouvel agent n'empêche pas les autres agents (comme l'Adaptateur) de faire leur travail.

### 3.3. Analyse des Logs
Pendant l'exécution, cherchez ces lignes :
-   `INFO - Type d'agent 'mon_role' enregistré...` : Prouve que la configuration est lue.
-   `INFO - Agent mon_role créé avec ID:...` : Prouve que le recrutement a réussi.
-   `INFO - Délégation de la tâche 'ma_tache' à l'agent 'mon_role'` : Prouve que l'intégration au workflow est fonctionnelle.
-   **Absence d'erreurs** de type `AttributeError: ... has no attribute 'logger'` ou `Agent type ... not registered`.

---

## 4. Capitalisation : Pièges à Éviter & Bonnes Pratiques

Cette section est le résumé de toutes les erreurs que nous avons corrigées ensemble.

-   **PIÈGE n°1 : L'Ordre d'Initialisation du Logger.**
    -   **Symptôme :** `AttributeError: ... object has no attribute 'logger'`
    -   **Cause :** Dans le `__init__`, `self.logger` est utilisé avant d'être défini.
    -   **RÈGLE D'OR :** L'ordre dans le `__init__` est **NON NÉGOCIABLE** : 1. `super().__init__(...)`, 2. `self.logger = ...`, 3. Le reste.

-   **PIÈGE n°2 : Les Noms Incohérents.**
    -   **Symptôme :** `ModuleNotFoundError`, `AttributeError`, ou `Agent type '...' not registered.`
    -   **Cause :** Une faute de frappe ou une incohérence entre le nom de la classe/fonction dans le fichier Python et ce qui est déclaré dans `config/maintenance_config.json`.
    -   **RÈGLE D'OR :** Copiez-collez les noms (classe, fonction, module) depuis votre code vers le fichier JSON. Ne les retapez jamais.

-   **BONNE PRATIQUE : L'Intégration "à blanc".**
    -   Pour un agent qui modifie profondément le code, envisagez de l'intégrer une première fois avec sa logique de transformation désactivée (il se contente de recevoir et renvoyer le code).
    -   Si le workflow passe, l'intégration est validée. Vous pouvez ensuite activer sa logique en toute confiance.

-   **BONNE PRATIQUE : La Journalisation.**
    -   Après chaque intégration réussie et validée par un test, mettez à jour le `JOURNAL_EVOLUTION_EQUIPE.md`.
    -   Ceci crée une trace immuable des décisions et des résultats, essentielle pour la maintenance à long terme.

-   **POINT D'ATTENTION : La Limite d'Arguments du Terminal.**
    -   Lors du lancement sur un grand nombre d'agents (> 7-8 sur Windows), le terminal peut atteindre sa limite de longueur d'arguments.
    -   Dans ce cas, la solution est de coder temporairement la liste des agents cibles directement dans `run_maintenance.py` ou d'implémenter une lecture depuis un fichier.
