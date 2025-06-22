#!/usr/bin/env python3
"""
🔍 PEER-REVIEWER ENRICHI / DOCUMENTEUR - Agent 05
==============================================================

🎯 Mission : Générer un rapport de mission détaillé et analytique.
⚡ Capacités : Analyse fine des erreurs, génération de diff, synthèse de mission.
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 5.0.1 - Abstract Method Fix
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import sys
import difflib

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
        super().__init__(**kwargs)
        self.logger.info(f"🔍 Agent Documenteur v{self.version} initialisé - ID: {self.agent_id}")

    async def startup(self):
        """Démarre l'agent Documenteur."""
        self.log("Agent Documenteur prêt.")

    async def shutdown(self):
        """Arrête l'agent Documenteur."""
        self.log("Agent Documenteur éteint.")

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
        
        lines = [f"# Rapport de Mission de Maintenance : `{mission_id}`"]
        lines.append(f"**Statut Final :** {statut} | **Durée :** {duree:.2f}s")
        lines.append("\n---")
        
        lines.append("## Résultats Détaillés par Agent\n")

        for agent_result in rapport_data.get("resultats_par_agent", []):
            agent_name = agent_result.get('agent_name', 'Agent Inconnu')
            status = agent_result.get('status', 'INCONNU')
            
            icon = "✅" if status in ["REPAIRED", "NO_REPAIR_NEEDED"] else "❌"
            lines.append(f"### {icon} Agent : `{agent_name}`")
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

        return "\n".join(lines)


def create_agent_MAINTENANCE_05_documenteur_peer_reviewer(**config) -> AgentMAINTENANCE05DocumenteurPeerReviewer:
    """Factory pour créer une instance de l'Agent 5."""
    return AgentMAINTENANCE05DocumenteurPeerReviewer(**config)