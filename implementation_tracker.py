#!/usr/bin/env python3
"""
SUIVI D'IMPLÉMENTATION NEXTGENERATION
===================================

Script de suivi et validation de l'implémentation des agents
avec critères stricts et monitoring détaillé.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
import sys

# Ajout des chemins pour les imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "core"))

from core.logging_manager import get_logger
from tests.test_implementations import TestImplementations

class ImplementationTracker:
    """Gestionnaire de suivi d'implémentation"""
    
    def __init__(self):
        self.logger = get_logger()
        self.config = self._load_config()
        self.test_impl = TestImplementations()
        self.start_time = datetime.now()
        
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration"""
        config_file = Path(__file__).parent / "config" / "implementation_config.json"
        try:
            with open(config_file) as f:
                return json.load(f)
        except Exception as e:
            self.logger.log_error("system", f"Erreur chargement config: {e}")
            return {}
    
    async def validate_phase(self, phase_id: str) -> bool:
        """Valide une phase d'implémentation"""
        phase_config = self.config["implementation_phases"].get(phase_id)
        if not phase_config:
            self.logger.log_error("system", f"Phase {phase_id} non trouvée")
            return False
        
        self.logger.log_test_start(
            "system",
            "phase_validation",
            {"phase": phase_id, "config": phase_config}
        )
        
        # Vérification durée minimale
        duration = datetime.now() - self.start_time
        if duration.days < phase_config["duration_days"]:
            self.logger.log_warning(
                "system",
                f"Durée insuffisante: {duration.days} jours vs {phase_config['duration_days']} requis"
            )
            return False
        
        # Validation de chaque agent
        success = True
        for agent_id in phase_config["agents"]:
            agent_success = await self._validate_agent(
                agent_id,
                phase_config["validation_criteria"]
            )
            if not agent_success:
                success = False
        
        return success
    
    async def _validate_agent(
        self,
        agent_id: str,
        criteria: Dict[str, float]
    ) -> bool:
        """Valide un agent selon les critères"""
        self.logger.log_test_start(
            agent_id,
            "agent_validation",
            {"criteria": criteria}
        )
        
        try:
            # Test matrix
            matrix_success = await self.test_impl.run_matrix_test(agent_id, 1.5)
            if not matrix_success:
                self.logger.log_error(
                    agent_id,
                    "Échec validation matrix"
                )
                return False
            
            # Test monitoring
            monitoring_precision = await self.test_impl.check_monitoring_precision(agent_id)
            if monitoring_precision < criteria["monitoring_precision"]:
                self.logger.log_error(
                    agent_id,
                    f"Précision monitoring insuffisante: {monitoring_precision}% vs {criteria['monitoring_precision']}% requis"
                )
                return False
            
            # Test messages
            message_success = await self.test_impl.send_test_message(agent_id)
            if not message_success:
                self.logger.log_error(
                    agent_id,
                    "Échec envoi message"
                )
                return False
            
            # Test optimisation
            baseline = await self.test_impl.measure_baseline_performance(agent_id)
            optimized = await self.test_impl.measure_optimized_performance(agent_id)
            improvement = ((baseline - optimized) / baseline) * 100
            
            if improvement < criteria["optimization_improvement"]:
                self.logger.log_error(
                    agent_id,
                    f"Optimisation insuffisante: {improvement}% vs {criteria['optimization_improvement']}% requis"
                )
                return False
            
            self.logger.log_test_result(
                agent_id,
                "agent_validation",
                True,
                time.time() - self.start_time,
                {
                    "matrix_success": matrix_success,
                    "monitoring_precision": monitoring_precision,
                    "message_success": message_success,
                    "optimization_improvement": improvement
                }
            )
            
            return True
            
        except Exception as e:
            self.logger.log_error(
                agent_id,
                f"Erreur validation: {e}",
                str(e)
            )
            return False
    
    def generate_report(self) -> Dict[str, Any]:
        """Génère un rapport de suivi"""
        return {
            "timestamp": datetime.now().isoformat(),
            "duration_days": (datetime.now() - self.start_time).days,
            "metrics": self.logger.get_global_summary(),
            "phases": {
                phase_id: {
                    "name": phase_config["name"],
                    "agents": phase_config["agents"],
                    "status": "completed" if self.logger.get_agent_summary(phase_config["agents"][0])["success_rate"] >= 95 else "in_progress"
                }
                for phase_id, phase_config in self.config["implementation_phases"].items()
            }
        }
    
    def save_report(self, report: Dict[str, Any]) -> None:
        """Sauvegarde le rapport"""
        report_file = Path(__file__).parent / "reports" / f"implementation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        # Génération version Markdown
        md_file = report_file.with_suffix(".md")
        with open(md_file, "w") as f:
            f.write("# Rapport de Suivi d'Implémentation NextGeneration\n\n")
            f.write(f"Date: {report['timestamp']}\n")
            f.write(f"Durée: {report['duration_days']} jours\n\n")
            
            f.write("## État des Phases\n\n")
            for phase_id, phase in report["phases"].items():
                f.write(f"### {phase['name']}\n")
                f.write(f"- Status: {phase['status']}\n")
                f.write("- Agents:\n")
                for agent in phase["agents"]:
                    agent_metrics = self.logger.get_agent_summary(agent)
                    f.write(f"  * {agent}: {agent_metrics['success_rate']:.1f}% succès\n")
                f.write("\n")
            
            f.write("## Métriques Globales\n\n")
            metrics = report["metrics"]
            f.write(f"- Tests totaux: {metrics['total_tests']}\n")
            f.write(f"- Taux de succès: {metrics['success_rate']:.1f}%\n")
            f.write(f"- Avertissements: {metrics['total_warnings']}\n")
            f.write(f"- Erreurs: {metrics['total_errors']}\n")

async def main():
    """Point d'entrée principal"""
    tracker = ImplementationTracker()
    
    # Validation Phase 1
    phase1_success = await tracker.validate_phase("phase_1")
    if phase1_success:
        print("✅ Phase 1 validée")
    else:
        print("❌ Phase 1 non validée")
    
    # Validation Phase 2
    phase2_success = await tracker.validate_phase("phase_2")
    if phase2_success:
        print("✅ Phase 2 validée")
    else:
        print("❌ Phase 2 non validée")
    
    # Génération et sauvegarde rapport
    report = tracker.generate_report()
    tracker.save_report(report)
    
    return 0 if phase1_success and phase2_success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 