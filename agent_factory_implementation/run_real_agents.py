#!/usr/bin/env python3
"""
🚀 LANCEUR AGENTS RÉELS AUTONOMES
Agent Factory Pattern - Sprint 4

Script pour démarrer et gérer les agents autonomes réels
"""

import asyncio
import signal
import sys
from pathlib import Path
from typing import List, Dict, Any, Union
from logging_manager_optimized import LoggingManager
from datetime import datetime
import json

# Ajouter le répertoire agents au path
AGENTS_DIR = Path(__file__).parent / "agents"
sys.path.insert(0, str(AGENTS_DIR))

# Import des agents réels
try:
    from real_agent_08_performance_optimizer import RealAgent08PerformanceOptimizer
    from real_agent_12_backup_manager import RealAgent12BackupManager
    from real_agent_06_specialiste_monitoring import RealAgent06SpecialisteMonitoring
    from real_agent_15_testeur_specialise import RealAgent15TesteurSpecialise
except ImportError as e:
    print(f"❌ Erreur import agents: {e}")
    sys.exit(1)

class AgentManager:
    """Gestionnaire d'agents autonomes"""
    
    def __init__(self):
        self.agents: Dict[str, Union[
            RealAgent08PerformanceOptimizer, 
            RealAgent12BackupManager,
            RealAgent06SpecialisteMonitoring,
            RealAgent15TesteurSpecialise
            ]] = {}
        self.tasks: Dict[str, asyncio.Task] = {}
        self.shutdown_event = asyncio.Event()
        self.running = True
        self.logger = self._setup_logging()
        
        # Signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logging(self):
        """Configuration logging"""
        # LoggingManager NextGeneration - Agent
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="AgentManager",
            role="ai_processor",
            domain="general",
            async_enabled=True
        )s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(f"agent_manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
            ]
        )
        return logging.getLogger("AgentManager")
    
    def _signal_handler(self, signum, frame):
        """Gestionnaire signaux pour arrêt propre"""
        self.logger.info(f"🛑 Signal {signum} reçu - Arrêt agents...")
        self.running = False
        self.shutdown_event.set()
        
        # Sur Windows, déclencher l'arrêt asyncio
        if sys.platform == 'win32':
            try:
                # Créer une tâche d'arrêt si on a une boucle active
                loop = asyncio.get_running_loop()
                if loop and not loop.is_closed():
                    asyncio.create_task(self.shutdown_all())
            except RuntimeError:
                # Pas de boucle active, arrêt normal
                pass
    
    async def start_agent(self, agent_class, agent_name: str):
        """Démarre un agent"""
        try:
            self.logger.info(f"🚀 Démarrage {agent_name}...")
            agent = agent_class()
            self.agents[agent_name] = agent
            
            # Démarrer agent en tâche asynchrone
            task = asyncio.create_task(agent.run())
            return task
            
        except Exception as e:
            self.logger.error(f"❌ Erreur démarrage {agent_name}: {e}")
            return None
    
    async def monitor_agents(self):
        """Surveillance agents"""
        while self.running:
            try:
                # Status des agents
                active_agents = []
                for name, agent in self.agents.items():
                    if hasattr(agent, 'status'):
                        active_agents.append(f"{name}:{agent.status}")
                
                if active_agents:
                    self.logger.info(f"📊 Agents actifs: {', '.join(active_agents)}")
                
                await asyncio.sleep(30)  # Vérification toutes les 30s
                
            except Exception as e:
                self.logger.error(f"❌ Erreur monitoring: {e}")
                await asyncio.sleep(10)
    
    async def start_agents(self):
        """Démarre tous les agents configurés."""
        agent_classes = {
            "Agent08_Performance": RealAgent08PerformanceOptimizer,
            "Agent12_Backup": RealAgent12BackupManager,
            "Agent06_Monitoring": RealAgent06SpecialisteMonitoring,
            "Agent15_Testing": RealAgent15TesteurSpecialise
        }

        for name, agent_class in agent_classes.items():
            try:
                agent = agent_class()
                self.agents[name] = agent
                task = asyncio.create_task(agent.run())
                self.tasks[name] = task
            except Exception as e:
                self.logger.error(f"❌ Erreur démarrage {name}: {e}")
    
    async def run_agents(self):
        """Point d'entrée principal"""
        self.logger.info("🚀 DÉMARRAGE GESTIONNAIRE AGENTS RÉELS")
        self.logger.info("=" * 60)
        
        try:
            # Démarrer agents
            await self.start_agents()
            
            self.logger.info(f"✅ {len(self.tasks)} tâches démarrées")
            
            # Monitoring
            monitor_task = asyncio.create_task(self.monitor_agents())
            self.tasks["monitor"] = monitor_task
            
            # Attendre arrêt
            await asyncio.gather(*self.tasks.values(), return_exceptions=True)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution: {e}")
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Arrêt propre"""
        self.logger.info("🛑 Arrêt gestionnaire en cours...")
        
        try:
            # Arrêter tous les agents
            for name, agent in self.agents.items():
                if hasattr(agent, 'shutdown'):
                    try:
                        await agent.shutdown()
                        self.logger.info(f"✅ Agent {name} arrêté")
                    except Exception as e:
                        self.logger.error(f"❌ Erreur arrêt {name}: {e}")
            
            self.logger.info("✅ Gestionnaire arrêté proprement")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur arrêt: {e}")

    async def shutdown_all(self):
        """Arrêt propre de tous les agents"""
        self.logger.info("🛑 Arrêt gestionnaire en cours...")
        
        try:
            # Arrêter tous les agents
            for name, agent in self.agents.items():
                if hasattr(agent, 'shutdown'):
                    try:
                        await agent.shutdown()
                        self.logger.info(f"✅ Agent {name} arrêté")
                    except Exception as e:
                        self.logger.error(f"❌ Erreur arrêt {name}: {e}")
            
            self.logger.info("✅ Gestionnaire arrêté proprement")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur arrêt: {e}")

async def main():
    """Point d'entrée principal du script."""
    print("🚀 DÉMARRAGE DU SYSTÈME D'AGENTS AUTONOMES 🚀")
    manager = AgentManager()
    
    # Gestion des signaux d'arrêt - Compatible Windows
    if sys.platform != 'win32':
        # Unix/Linux - utiliser add_signal_handler
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(manager.shutdown_all()))
    else:
        # Windows - utiliser signal.signal (déjà configuré dans AgentManager.__init__)
        print("🪟 Mode Windows détecté - Signal handlers configurés")

    try:
        await manager.start_agents()
        await manager.monitor_agents()
    except (asyncio.CancelledError, KeyboardInterrupt):
        manager.logger.info("🛑 Interruption détectée - Arrêt en cours...")
        await manager.shutdown_all()
    except Exception as e:
        manager.logger.error(f"❌ Erreur inattendue: {e}")
        await manager.shutdown_all()
    finally:
        manager.logger.info("🏁 Système d'agents arrêté.")

if __name__ == "__main__":
    # Vérifier dépendances
    try:
        import psutil
        import zstandard
        import prometheus_client
        import aiofiles
        import watchdog
        import git
        print("✅ Toutes les dépendances sont disponibles")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("📦 Installer avec: pip install psutil zstandard prometheus-client aiofiles watchdog GitPython")
        sys.exit(1)
    
    asyncio.run(main()) 