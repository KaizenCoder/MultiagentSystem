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
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import aiofiles
import logging

# Configuration
AGENT_ROOT = Path(__file__).parent
PROJECT_ROOT = AGENT_ROOT.parent
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Import dynamique pour éviter les problèmes de chemin
try:
    from core import logging_manager
except ImportError:
    sys.path.append(str(PROJECT_ROOT.parent))
    from core import logging_manager


@dataclass
class TestRunState:
    """Représente l'état d'une session de test."""
    timestamp: datetime
    test_type: str  # "load", "regression", "security"
    tests_executed: int
    tests_passed: int
    average_duration_ms: float
    status: str  # "COMPLETED", "FAILED"

class RealAgent15TesteurSpecialise:
    """
    🚀 AGENT 15 RÉEL - TESTEUR SPÉCIALISÉ AUTONOME
    """
    
    def __init__(self):
        self.agent_id = "real_agent_15"
        self.agent_name = "Testeur Spécialisé (Autonome)"
        self.version = "1.0.0"
        self.status = "INITIALIZING"
        
        self.running = True
        self.shutdown_event = asyncio.Event()
        self.loop = None
        
        self.test_history = []
        
        self._setup_logging()
        
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info(f"🚀 {self.agent_name} initialisé")

    def _setup_logging(self):
        """Configuration du logging pour l'agent."""
        log_file = LOGS_DIR / f"{self.agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
        )
        self.logger = logging.getLogger(__name__) # Utilisation standard

    def _signal_handler(self, signum, frame):
        """Gestionnaire de signaux pour un arrêt propre."""
        self.logger.info(f"🛑 Signal {signum} reçu - Arrêt en cours...")
        self.running = False
        self.shutdown_event.set()

    async def _simulate_test_run(self, test_type: str) -> TestRunState:
        """Simule l'exécution d'une série de tests."""
        self.logger.info(f"🔬 Démarrage des tests de type '{test_type}'...")
        await asyncio.sleep(random.uniform(1, 3))  # Durée de la session de test réduite
        
        num_tests = random.randint(5, 20)
        passes = random.randint(int(num_tests * 0.8), num_tests)
        avg_duration = random.uniform(50, 200)
        
        state = TestRunState(
            timestamp=datetime.now(),
            test_type=test_type,
            tests_executed=num_tests,
            tests_passed=passes,
            average_duration_ms=avg_duration,
            status="COMPLETED" if passes / num_tests > 0.9 else "FAILED"
        )
        
        self.logger.info(f"✅ Tests '{test_type}' terminés: {passes}/{num_tests} passés.")
        self.test_history.append(state)
        return state

    async def testing_loop(self):
        """Boucle principale de tests continus."""
        self.logger.info("🔄 Démarrage de la boucle de tests")
        while self.running:
            try:
                test_types = ["load", "regression", "security"]
                random.shuffle(test_types)
                
                for test_type in test_types:
                    if not self.running: 
                        break
                    await self._simulate_test_run(test_type)
                    await asyncio.sleep(random.uniform(1, 5)) # Intervalle réduit
                
                # Sauvegarde plus fréquente pour le test
                await self.save_testing_report()

            except Exception as e:
                self.logger.error(f"❌ Erreur dans la boucle de tests: {e}", exc_info=True)
                await asyncio.sleep(10)

    async def save_testing_report(self):
        """Sauvegarde le rapport de tests."""
        if not self.test_history:
            return
        
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
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la sauvegarde du rapport: {e}", exc_info=True)

    async def run(self):
        """Point d'entrée principal de l'agent."""
        self.logger.info(f"🚀 Démarrage de {self.agent_name}")
        self.status = "RUNNING"
        
        try:
            await self.testing_loop()
        except asyncio.CancelledError:
            self.logger.info("Tâche principale annulée.")
        except Exception as e:
            self.logger.error(f"❌ Erreur d'exécution de l'agent: {e}", exc_info=True)
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Arrêt propre de l'agent."""
        self.logger.info("🛑 Arrêt de l'agent en cours...")
        self.status = "SHUTTING_DOWN"
        await self.save_testing_report()
        self.status = "STOPPED"
        self.logger.info("✅ Agent arrêté proprement")

async def main():
    agent = RealAgent15TesteurSpecialise()
    try:
        await agent.run()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
    finally:
        agent.running = False
        await agent.shutdown()

if __name__ == "__main__":
    asyncio.run(main())