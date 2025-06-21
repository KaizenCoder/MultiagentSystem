#!/usr/bin/env python3
"""
🚀 REAL AGENT 06 - SPECIALISTE MONITORING (AUTONOME)
Agent Factory Pattern - Sprint 4 - Agent Autonome

Mission: Agent autonome pour le monitoring de l'infrastructure et des agents.
- Surveillance continue des métriques clés (CPU, mémoire, etc.)
- Simulation de la collecte de traces et de logs.
- Fournit un état de santé de base.
"""

import asyncio
from logging_manager_optimized import LoggingManager
import signal
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import psutil
import json
import aiofiles

# Configuration
AGENT_ROOT = Path(__file__).parent
PROJECT_ROOT = AGENT_ROOT.parent
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

@dataclass
class MonitoringState:
    """État du monitoring en temps réel"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    active_agents: int
    health_status: str

class RealAgent06SpecialisteMonitoring:
    """
    🚀 AGENT 06 RÉEL - SPÉCIALISTE MONITORING AUTONOME
    """
    
    def __init__(self):
        self.agent_id = "real_agent_06"
        self.agent_name = "Spécialiste Monitoring (Autonome)"
        self.version = "1.0.0"
        self.status = "INITIALIZING"
        
        self.running = True
        self.shutdown_event = asyncio.Event()
        self.loop = None
        
        self.current_state = None
        self.metrics_history = []
        
        self._setup_logging()
        
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info(f"🚀 {self.agent_name} initialisé")

    def _setup_logging(self):
        """Configuration du logging pour l'agent"""
        log_file = LOGS_DIR / f"{self.agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
        )
        # LoggingManager NextGeneration - Agent
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="class",
            role="ai_processor",
            domain="monitoring",
            async_enabled=True
        )

    def _signal_handler(self, signum, frame):
        """Gestionnaire de signaux pour un arrêt propre"""
        self.logger.info(f"🛑 Signal {signum} reçu - Arrêt en cours...")
        self.running = False
        self.shutdown_event.set()

    async def collect_monitoring_metrics(self) -> MonitoringState:
        """Collecte les métriques de monitoring."""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Simuler la découverte d'agents actifs
        active_agents = 2 # Agent 08 et 12, plus lui-même bientôt
        
        health_status = "healthy"
        if cpu_percent > 80 or memory_percent > 80:
            health_status = "degraded"

        state = MonitoringState(
            timestamp=datetime.now(),
            cpu_usage=cpu_percent,
            memory_usage=memory_percent,
            active_agents=active_agents,
            health_status=health_status
        )
        self.current_state = state
        self.metrics_history.append(state)
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
        return state

    async def monitoring_loop(self):
        """Boucle principale de monitoring."""
        self.logger.info("🔄 Démarrage de la boucle de monitoring")
        while self.running:
            try:
                state = await self.collect_monitoring_metrics()
                if int(time.time()) % 60 == 0: # Log toutes les minutes
                    self.logger.info(f"📊 État Monitoring: CPU={state.cpu_usage:.1f}%, Mem={state.memory_usage:.1f}%, Agents={state.active_agents}, Santé={state.health_status}")
                
                if int(time.time()) % 180 == 0: # Rapport toutes les 3 minutes
                    await self.save_monitoring_report()

                await asyncio.sleep(10)
            except Exception as e:
                self.logger.error(f"❌ Erreur dans la boucle de monitoring: {e}")
                await asyncio.sleep(30)

    async def save_monitoring_report(self):
        """Sauvegarde le rapport de monitoring."""
        report_file = REPORTS_DIR / f"{self.agent_id}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError("Type not serializable")

        try:
            async with aiofiles.open(report_file, 'w') as f:
                report_data = [asdict(state) for state in self.metrics_history]
                await f.write(json.dumps(report_data, indent=2, default=convert_datetime))
            self.logger.info(f"✅ Rapport de monitoring sauvegardé: {report_file}")
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la sauvegarde du rapport: {e}")

    async def run(self):
        """Point d'entrée principal de l'agent."""
        self.logger.info(f"🚀 Démarrage de {self.agent_name}")
        self.status = "RUNNING"
        self.loop = asyncio.get_running_loop()
        
        try:
            monitoring_task = asyncio.create_task(self.monitoring_loop())
            await asyncio.gather(monitoring_task, return_exceptions=True)
        except Exception as e:
            self.logger.error(f"❌ Erreur d'exécution de l'agent: {e}")
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Arrêt propre de l'agent."""
        self.logger.info("🛑 Arrêt de l'agent en cours...")
        self.status = "SHUTTING_DOWN"
        await self.save_monitoring_report()
        self.status = "STOPPED"
        self.logger.info("✅ Agent arrêté proprement")

async def main():
    agent = RealAgent06SpecialisteMonitoring()
    try:
        await agent.run()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")

if __name__ == "__main__":
    import time # Ajout de l'import time manquant
    asyncio.run(main()) 