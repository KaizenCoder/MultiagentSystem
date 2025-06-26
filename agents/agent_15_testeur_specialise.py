#!/usr/bin/env python3
"""
🚀 REAL AGENT 15 - TESTEUR SPÉCIALISÉ (AUTONOME)
Agent Factory Pattern - Sprint 4 - Agent Autonome

Mission: Exécuter des tests spécialisés de manière continue.
- Simule des tests de charge, de régression et de sécurité.
- Génère des rapports sur les résultats des tests.
"""

import asyncio
import sys
from pathlib import Path
import signal
import random
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
import aiofiles
import logging
from typing import List, Dict, Any, Optional

# Import des classes du Pattern Factory
from core.agent_factory_architecture import Agent, Task, Result, TaskStatus as FactoryTaskStatus, Priority as FactoryPriority

# Configuration
AGENT_ROOT = Path(__file__).parent
PROJECT_ROOT = AGENT_ROOT.parent
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Utilisation de la configuration du LoggingManager global si disponible
try:
    from core.logging_manager import LoggingManager
    log = LoggingManager().get_logger(__name__)
except ImportError:
    # Fallback pour un logging basique si le manager n'est pas dispo
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    log = logging.getLogger(__name__)


@dataclass
class TestRunState:
    """Représente l'état d'une session de test."""
    timestamp: datetime
    test_type: str  # "load", "regression", "security"
    tests_executed: int
    tests_passed: int
    average_duration_ms: float
    status: str  # "COMPLETED", "FAILED"

class RealAgent15TesteurSpecialise(Agent):
    """
    🚀 AGENT 15 RÉEL - TESTEUR SPÉCIALISÉ AUTONOME
    Implémente l'interface Agent du Pattern Factory.
    """
    
    def __init__(self, **kwargs):
        super().__init__(agent_type="testing", **kwargs)
        self.agent_id = self.id # Utilise l'ID généré par l'Agent de base
        self.agent_name = "Testeur Spécialisé (Autonome)"
        self.version = "1.0.0"
        self.status = "INITIALIZING"
        self.capabilities = ["testing"]
        
        self.running = True
        self.shutdown_event = asyncio.Event()
        self.loop = None
        
        self.test_history = []
        
        self.logger = log # Utilise le logger centralisé
        
        # Enregistrement des gestionnaires de signaux (si exécuté directement)
        # signal.signal(signal.SIGINT, self._signal_handler)
        # signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info(f"🚀 {self.agent_name} initialisé (Factory Compatible)")

    # Suppression de _setup_logging car le logger est centralisé
    # def _setup_logging(self):
    #     """Configuration du logging pour l'agent."""
    #     log_file = LOGS_DIR / f"{self.agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    #     logging.basicConfig(
    #         level=logging.INFO,
    #         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #         handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
    #     )
    #     self.logger = logging.getLogger(__name__) # Utilisation standard

    # Méthodes abstraites à implémenter pour la compatibilité Factory
    async def execute_task(self, task: Task) -> Result:
        """
        ⚙️ Exécute une tâche spécifique de test.
        """
        self.logger.info(f"Exécution de la tâche Factory: {task.type} (ID: {task.id})")
        try:
            if task.type == "run_test_suite":
                test_type = task.params.get("test_type", "all")
                await self._run_test_suite_logic(test_type)
                return Result(success=True, data={"message": f"Suite de tests {test_type} exécutée."})
            
            elif task.type == "generate_test_report":
                report_path = await self.save_testing_report()
                return Result(success=True, data={"report_path": str(report_path)})

            else:
                self.logger.warning(f"Type de tâche non supporté: {task.type}")
                return Result(success=False, error=f"Type de tâche non supporté: {task.type}", error_code="UNSUPPORTED_TASK_TYPE")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche {task.type}: {e}", exc_info=True)
            return Result(success=False, error=str(e), error_code="TASK_EXECUTION_ERROR")

    def get_capabilities(self) -> List[str]:
        """
        📋 Retourne la liste des capacités de l'agent (types de tâches supportés).
        """
        return self.capabilities

    async def startup(self) -> None:
        """
        🚀 Initialise l'agent et prépare ses ressources.
        """
        self.logger.info(f"Agent {self.agent_name} (ID: {self.agent_id}) démarré.")
        self.status = "RUNNING"
        # Démarrer la boucle de tests en arrière-plan si nécessaire
        # asyncio.create_task(self.testing_loop())

    async def shutdown(self) -> None:
        """
        🛑 Arrêt propre de l'agent.
        """
        self.logger.info(f"Agent {self.agent_name} (ID: {self.agent_id}) s'arrête...")
        self.status = "SHUTTING_DOWN"
        await self.save_testing_report() # S'assurer que les rapports sont sauvegardés avant l'arrêt
        self.status = "STOPPED"
        self.logger.info(f"Agent {self.agent_name} (ID: {self.agent_id}) arrêté proprement.")

    async def health_check(self) -> Dict[str, Any]:
        """
        💖 Vérifie l'état de santé de l'agent.
        """
        # Simule une vérification de santé. En production, cela interagirait avec les sous-systèmes.
        if self.running and self.status == "RUNNING":
            return {"status": "healthy", "timestamp": datetime.now().isoformat(), "agent_id": self.agent_id}
        else:
            return {"status": "unhealthy", "timestamp": datetime.now().isoformat(), "agent_id": self.agent_id, "reason": "Agent not running or stopped"}

    async def _run_test_suite_logic(self, test_type: str):
        """
        Logique pour exécuter une suite de tests spécifique.
        Cela peut être étendu pour appeler différents simulateurs ou des outils de test réels.
        """
        self.logger.info(f"Exécution de la suite de tests de type: {test_type}")
        if test_type == "all":
            test_types_to_run = ["load", "regression", "security"]
        else:
            test_types_to_run = [test_type]

        for t_type in test_types_to_run:
            if not self.running: break
            await self._simulate_test_run(t_type)
            await asyncio.sleep(random.uniform(0.5, 2)) # Petites pauses entre les types de tests

    # Le reste des méthodes existantes (_signal_handler, _simulate_test_run, testing_loop, save_testing_report)
    # reste inchangé mais la boucle principale sera déclenchée via execute_task.

    def _signal_handler(self, signum, frame):
        """Gestionnaire de signaux pour un arrêt propre."""
        self.logger.info(f"🛑 Signal {signum} reçu - Arrêt en cours...")
        self.running = False
        self.shutdown_event.set()

    async def _simulate_test_run(self, test_type: str) -> TestRunState:
        """Simule l'exécution d'une série de tests."""
        self.logger.info(f"🔬 Démarrage des tests de type '{test_type}'...")
        await asyncio.sleep(random.uniform(0.5, 1.5))  # Durée de la session de test réduite pour Factory
        
        num_tests = random.randint(3, 10) # Moins de tests pour un run Factory rapide
        passes = random.randint(int(num_tests * 0.7), num_tests)
        avg_duration = random.uniform(20, 100)
        
        state = TestRunState(
            timestamp=datetime.now(),
            test_type=test_type,
            tests_executed=num_tests,
            tests_passed=passes,
            average_duration_ms=avg_duration,
            status="COMPLETED" if passes / num_tests >= 0.9 else "FAILED"
        )
        
        self.logger.info(f"✅ Tests '{test_type}' terminés: {passes}/{num_tests} passés. Statut: {state.status}")
        self.test_history.append(state)
        return state

    # La boucle `testing_loop` n'est plus le point d'entrée principal et sera appelée via execute_task si besoin.
    # async def testing_loop(self):
    #     """Boucle principale de tests continus."""
    #     self.logger.info("🔄 Démarrage de la boucle de tests")
    #     while self.running:
    #         try:
    #             test_types = ["load", "regression", "security"]
    #             random.shuffle(test_types)
    #             
    #             for test_type in test_types:
    #                 if not self.running: 
    #                     break
    #                 await self._simulate_test_run(test_type)
    #                 await asyncio.sleep(random.uniform(1, 5)) # Intervalle réduit
    #             
    #             # Sauvegarde plus fréquente pour le test
    #             await self.save_testing_report()

    #         except Exception as e:
    #             self.logger.error(f"❌ Erreur dans la boucle de tests: {e}", exc_info=True)
    #             await asyncio.sleep(10)

    async def save_testing_report(self):
        """Sauvegarde le rapport de tests."""
        if not self.test_history:
            self.logger.info("Aucun historique de tests à sauvegarder.")
            return None
        
        report_file = REPORTS_DIR / f"{self.agent_id}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError("Type not serializable")

        try:
            async with aiofiles.open(report_file, 'w') as f:
                report_data = [asdict(state) for state in self.test_history]
                await f.write(json.dumps(report_data, indent=2, default=convert_datetime))
            self.logger.info(f"✅ Rapport de tests sauvegardé: {report_file}")
            self.test_history = [] # Clear history after saving
            return report_file
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la sauvegarde du rapport: {e}", exc_info=True)
            return None

    # La méthode `run` n'est plus le point d'entrée principal pour l'exécution continue.
    # async def run(self):
    #     """Point d'entrée principal de l'agent."""
    #     self.logger.info(f"🚀 Démarrage de {self.agent_name}")
    #     self.status = "RUNNING"
    #     
    #     try:
    #         await self.testing_loop()
    #     except asyncio.CancelledError:
    #         self.logger.info("Tâche principale annulée.")
    #     except Exception as e:
    #         self.logger.error(f"❌ Erreur d'exécution de l'agent: {e}", exc_info=True)
    #     finally:
    #         await self.shutdown()

# Le bloc d'exécution direct est supprimé pour le Pattern Factory
# async def main():
#     agent = RealAgent15TesteurSpecialise()
#     try:
#         await agent.run()
#     except KeyboardInterrupt:
#         print("\n🛑 Arrêt demandé par l'utilisateur")
#     finally:
#         agent.running = False
#         await agent.shutdown()

# if __name__ == "__main__":
#     asyncio.run(main())