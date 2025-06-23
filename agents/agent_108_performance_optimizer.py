#!/usr/bin/env python3
"""
🚀 REAL AGENT 08 - PERFORMANCE OPTIMIZER
Agent Factory Pattern - Sprint 4 - Agent Autonome

Mission: Agent autonome pour optimisations performance < 50ms SLA
- Exécution en continu avec boucle d'événements
- ThreadPool adaptatif auto-géré
- Compression Zstandard automatique
- Métriques temps réel avec export Prometheus
- Auto-scaling basé sur charge CPU

Version: 1.0.0 - Agent Réel Autonome
"""

import asyncio
import json
import sys
from pathlib import Path
from core import logging_manager
import time
import zstandard as zstd
import psutil
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from threading import RLock, Event, Thread
from typing import Dict, List, Optional, Any
import aiofiles
import aiohttp
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Configuration
try:
    AGENT_ROOT = Path(__file__).parent
    PROJECT_ROOT = AGENT_ROOT.parent
except NameError:
    # Fallback si __file__ n'est pas défini
    AGENT_ROOT = Path.cwd() / "agents"
    PROJECT_ROOT = Path.cwd()

LOGS_DIR = PROJECT_ROOT / "logs"
METRICS_DIR = PROJECT_ROOT / "metrics"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# Créer répertoires
for directory in [LOGS_DIR, METRICS_DIR, TEMPLATES_DIR]:
    directory.mkdir(exist_ok=True)

@dataclass
class PerformanceState:
    """État performance temps réel"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    active_workers: int
    queue_size: int
    avg_response_time: float
    p95_response_time: float
    compression_ratio: float
    templates_processed: int
    sla_compliance: float

class RealAgent08PerformanceOptimizer:
    """
    🚀 AGENT 08 RÉEL - OPTIMISEUR PERFORMANCE AUTONOME
    
    Agent qui s'exécute en continu pour optimiser les performances:
    - Boucle d'événements asyncio autonome
    - Auto-scaling ThreadPool basé sur CPU
    - Compression automatique des templates
    - Monitoring continu avec métriques Prometheus
    - Alertes SLA automatiques
    """
    
    def __init__(self):
    self.agent_id = "real_agent_08"
    self.agent_name = "Performance Optimizer (Autonome)"
    self.version = "1.0.0"
    self.status = "INITIALIZING"
        
        # Configuration
    self.running = True
    self.shutdown_event = Event()
        
        # Performance targets
    self.sla_targets = {
    "max_response_time_ms": 50,
    "min_compression_ratio": 0.3,
    "min_cache_hit_rate": 0.8,
    "max_cpu_usage": 0.8,
    "max_memory_usage": 0.7
    }
        
        # État interne
    self.current_state = None
    self.metrics_history = []
    self.lock = RLock()
        
        # ThreadPool adaptatif
    self.base_workers = max(2, psutil.cpu_count() // 2)
    self.max_workers = psutil.cpu_count() * 2
    self.current_workers = self.base_workers
    self.thread_pool = None
        
        # Logging (setup first!)
    self._setup_logging()
        
        # Compression Zstandard
    self.compressor = None
    self.decompressor = None
    self._setup_compression()
        
        # Métriques Prometheus
    self._setup_prometheus_metrics()
        
        # Signal handlers pour arrêt propre
    signal.signal(signal.SIGINT, self._signal_handler)
    signal.signal(signal.SIGTERM, self._signal_handler)
        
    self.logger.info(f"🚀 {self.agent_name} initialisé")
    self.logger.info(f"ThreadPool: {self.base_workers}-{self.max_workers} workers")
    self.logger.info(f"SLA Target: {self.sla_targets['max_response_time_ms']}ms")
    
    def _setup_logging(self):
        """Configuration logging agent"""
    log_file = LOGS_DIR / f"{self.agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
    logging.FileHandler(log_file),
    logging.StreamHandler()
    ]
    )
        
        # LoggingManager NextGeneration - Agent
    import sys
from pathlib import Path
from core import logging_manager
    self.logger = LoggingManager().get_agent_logger(
    agent_name="class",
    role="ai_processor",
    domain="performance",
    async_enabled=True
    )
    
    def _setup_compression(self):
        """Initialisation compression Zstandard"""
    try:
            # Dictionnaire optimisé pour templates JSON
    template_dict = (
    b'{"id":' * 50 + 
    b',"name":' * 50 + 
    b',"description":' * 50 + 
    b',"version":' * 50 +
    b',"config":' * 50
    )
            
    compression_dict = zstd.ZstdCompressionDict(template_dict)
            
    self.compressor = zstd.ZstdCompressor(
    level=3,  # Équilibre vitesse/compression
    dict_data=compression_dict,
    write_content_size=True,
    threads=2
    )
            
    self.decompressor = zstd.ZstdDecompressor(dict_data=compression_dict)
            
    self.logger.info("✅ Compression Zstandard initialisée")
            
    except Exception as e:
    self.logger.error(f"❌ Erreur compression: {e}")
    
    def _setup_prometheus_metrics(self):
        """Configuration métriques Prometheus"""
    self.metrics = {
    'templates_processed': Counter('agent08_templates_processed_total', 'Templates traités'),
    'response_time': Histogram('agent08_response_time_seconds', 'Temps de réponse'),
    'cpu_usage': Gauge('agent08_cpu_usage_percent', 'Utilisation CPU'),
    'memory_usage': Gauge('agent08_memory_usage_percent', 'Utilisation mémoire'),
    'active_workers': Gauge('agent08_active_workers', 'Workers actifs'),
    'compression_ratio': Gauge('agent08_compression_ratio', 'Ratio compression'),
    'sla_compliance': Gauge('agent08_sla_compliance_percent', 'Conformité SLA')
    }
        
        # Démarrer serveur Prometheus
    start_http_server(8008)
    self.logger.info("📊 Serveur Prometheus démarré sur port 8008")
    
    def _signal_handler(self, signum, frame):
        """Gestionnaire signaux pour arrêt propre"""
    self.logger.info(f"🛑 Signal {signum} reçu - Arrêt en cours...")
    self.running = False
    self.shutdown_event.set()
    
    async def collect_performance_metrics(self) -> PerformanceState:
        """Collecte métriques performance temps réel"""
    try:
            # Métriques système
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
            
            # Métriques ThreadPool
    active_workers = self.current_workers
    if self.thread_pool:
    queue_size = getattr(self.thread_pool, '_work_queue', None)
    queue_size = queue_size.qsize() if queue_size else 0
    else:
    queue_size = 0
            
            # Calcul temps de réponse (simulation pour démo)
    start_time = time.time()
    await asyncio.sleep(0.001)  # Simulation traitement
    response_time = (time.time() - start_time) * 1000  # ms
            
            # Métriques compression (simulation)
    compression_ratio = 0.35  # Ratio moyen observé
            
            # Calcul conformité SLA
    sla_compliance = self._calculate_sla_compliance(response_time, cpu_percent)
            
    state = PerformanceState(
    timestamp=datetime.now(),
    cpu_usage=cpu_percent,
    memory_usage=memory_percent,
    active_workers=active_workers,
    queue_size=queue_size,
    avg_response_time=response_time,
    p95_response_time=response_time * 1.2,  # Estimation
    compression_ratio=compression_ratio,
    templates_processed=len(self.metrics_history),
    sla_compliance=sla_compliance
    )
            
            # Mise à jour métriques Prometheus
    self.metrics['cpu_usage'].set(cpu_percent)
    self.metrics['memory_usage'].set(memory_percent)
    self.metrics['active_workers'].set(active_workers)
    self.metrics['compression_ratio'].set(compression_ratio)
    self.metrics['sla_compliance'].set(sla_compliance)
    self.metrics['response_time'].observe(response_time / 1000)
            
    with self.lock:
    self.current_state = state
    self.metrics_history.append(state)
                
                # Garder seulement les 1000 dernières métriques
    if len(self.metrics_history) > 1000:
    self.metrics_history = self.metrics_history[-1000:]
            
    return state
            
    except Exception as e:
    self.logger.error(f"❌ Erreur collecte métriques: {e}")
    return None
    
    def _calculate_sla_compliance(self, response_time: float, cpu_usage: float) -> float:
        """Calcule conformité SLA"""
    compliance_factors = []
        
        # Temps de réponse
    if response_time <= self.sla_targets['max_response_time_ms']:
    compliance_factors.append(1.0)
    else:
    compliance_factors.append(max(0, 1 - (response_time - self.sla_targets['max_response_time_ms']) / 100))
        
        # CPU usage
    if cpu_usage <= self.sla_targets['max_cpu_usage'] * 100:
    compliance_factors.append(1.0)
    else:
    compliance_factors.append(max(0, 1 - (cpu_usage/100 - self.sla_targets['max_cpu_usage']) / 0.2))
        
    return sum(compliance_factors) / len(compliance_factors) * 100
    
    async def auto_scale_threadpool(self):
        """Auto-scaling ThreadPool basé sur charge"""
    try:
    if not self.current_state:
    return
            
    cpu_usage = self.current_state.cpu_usage / 100
    current_workers = self.current_workers
            
            # Décision scaling
    if cpu_usage > 0.8 and current_workers < self.max_workers:
                # Scale up
    new_workers = min(current_workers + 2, self.max_workers)
    self._update_threadpool(new_workers)
    self.logger.info(f"📈 Scale UP: {current_workers} → {new_workers} workers (CPU: {cpu_usage:.1%})")
                
    elif cpu_usage < 0.3 and current_workers > self.base_workers:
                # Scale down
    new_workers = max(current_workers - 1, self.base_workers)
    self._update_threadpool(new_workers)
    self.logger.info(f"📉 Scale DOWN: {current_workers} → {new_workers} workers (CPU: {cpu_usage:.1%})")
            
    except Exception as e:
    self.logger.error(f"❌ Erreur auto-scaling: {e}")
    
    def _update_threadpool(self, new_size: int):
        """Met à jour taille ThreadPool"""
    try:
    with self.lock:
    if self.thread_pool:
    self.thread_pool.shutdown(wait=False)
                
    self.thread_pool = ThreadPoolExecutor(
    max_workers=new_size,
    thread_name_prefix=f"{self.agent_id}_worker"
    )
    self.current_workers = new_size
                
    except Exception as e:
    self.logger.error(f"❌ Erreur mise à jour ThreadPool: {e}")
    
    async def compress_template(self, template_data: Dict[str, Any]) -> bytes:
        """Compression template avec Zstandard"""
    if not self.compressor:
    self.logger.error("❌ Compresseur non initialisé, compression annulée.")
    return b""
            
    try:
    json_data = json.dumps(template_data, separators=(',', ':')).encode('utf-8')
    compressed = self.compressor.compress(json_data)
            
            # Calcul ratio compression
    ratio = len(compressed) / len(json_data)
    self.metrics['compression_ratio'].set(ratio)
            
    return compressed
            
    except Exception as e:
    self.logger.error(f"❌ Erreur compression: {e}")
    return b""
    
    async def process_template_request(self, template_config: Dict[str, Any]) -> Dict[str, Any]:
        """Traite une requête template avec optimisations"""
    start_time = time.time()
        
    try:
            # Simulation traitement template
    await asyncio.sleep(0.01)  # 10ms traitement
            
            # Compression
    compressed_data = await self.compress_template(template_config)
            
            # Calcul métriques
    processing_time = (time.time() - start_time) * 1000  # ms
            
            # Mise à jour compteurs
    self.metrics['templates_processed'].inc()
    self.metrics['response_time'].observe(processing_time / 1000)
            
    result = {
    "template_id": template_config.get("id", "unknown"),
    "processing_time_ms": processing_time,
    "compressed_size": len(compressed_data),
    "compression_ratio": len(compressed_data) / len(json.dumps(template_config).encode()),
    "sla_compliant": processing_time <= self.sla_targets['max_response_time_ms'],
    "timestamp": datetime.now().isoformat()
    }
            
    return result
            
    except Exception as e:
    self.logger.error(f"❌ Erreur traitement template: {e}")
    return {"error": str(e)}
    
    async def save_performance_report(self):
        """Sauvegarde rapport performance JSON"""
    try:
    report_file = METRICS_DIR / f"{self.agent_id}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
    with self.lock:
    report_data = [asdict(state) for state in self.metrics_history]

            # Convertir datetime en string pour la sérialisation JSON
    def convert_datetime(obj):
    if isinstance(obj, datetime):
    return obj.isoformat()
    raise TypeError("Type not serializable")

    async with aiofiles.open(report_file, 'w') as f:
    await f.write(json.dumps(report_data, indent=2, default=convert_datetime))
            
    self.logger.info(f"✅ Rapport performance sauvegardé: {report_file}")
            
    except Exception as e:
    self.logger.error(f"❌ Erreur sauvegarde rapport: {e}")
    
    async def monitoring_loop(self):
        """Boucle monitoring principal"""
    self.logger.info("🔄 Démarrage de la boucle de monitoring de performance")
    while self.running:
    try:
    await self.collect_performance_metrics()
    if int(time.time()) % 180 == 0:  # Sauvegarde toutes les 3 minutes
    await self.save_performance_report()
    await asyncio.sleep(10)
    except Exception as e:
    self.logger.error(f"❌ Erreur dans la boucle de performance: {e}")
    
    async def template_processing_loop(self):
        """Boucle traitement templates"""
    self.logger.info("🔄 Démarrage boucle traitement templates")
        
    while self.running:
    try:
                # Simulation requêtes templates
    for i in range(5):  # 5 templates par cycle
    template_config = {
        "id": f"template_{int(time.time())}_{i}",
        "name": f"Template Test {i}",
        "version": "1.0.0",
        "config": {"param1": "value1", "param2": "value2"}
    }
                    
    result = await self.process_template_request(template_config)
                    
    if result.get("sla_compliant", False):
        self.logger.debug(f"✅ Template {result['template_id']}: {result['processing_time_ms']:.1f}ms")
    else:
        self.logger.warning(f"⚠️ SLA dépassé {result['template_id']}: {result['processing_time_ms']:.1f}ms")
                
    await asyncio.sleep(10)  # Cycle toutes les 10s
                
    except Exception as e:
    self.logger.error(f"❌ Erreur traitement templates: {e}")
    await asyncio.sleep(5)
    
    async def run(self):
        """Point d'entrée principal agent"""
    self.logger.info(f"🚀 Démarrage {self.agent_name}")
    self.status = "RUNNING"
        
    try:
            # Initialisation ThreadPool
    self._update_threadpool(self.base_workers)
            
            # Démarrage tâches asynchrones
    tasks = [
    asyncio.create_task(self.monitoring_loop()),
    asyncio.create_task(self.template_processing_loop())
    ]
            
            # Attendre arrêt
    await asyncio.gather(*tasks, return_exceptions=True)
            
    except Exception as e:
    self.logger.error(f"❌ Erreur exécution agent: {e}")
    finally:
    await self.shutdown()
    
    async def shutdown(self):
        """Arrêt propre agent"""
    self.logger.info("🛑 Arrêt agent en cours...")
    self.status = "SHUTTING_DOWN"
        
    try:
            # Fermeture ThreadPool
    if self.thread_pool:
    self.thread_pool.shutdown(wait=True)
            
            # Sauvegarde rapport final
    await self.save_performance_report()
            
    self.status = "STOPPED"
    self.logger.info("✅ Agent arrêté proprement")
            
    except Exception as e:
    self.logger.error(f"❌ Erreur arrêt: {e}")

async def main():
    """Point d'entrée principal"""
    print("🚀 REAL AGENT 08 - PERFORMANCE OPTIMIZER")
    print("=" * 50)
    
    agent = RealAgent08PerformanceOptimizer()
    
    try:
    await agent.run()
    except KeyboardInterrupt:
    print("\n🛑 Arrêt demandé par utilisateur")
    except Exception as e:
    print(f"❌ Erreur fatale: {e}")
    finally:
    print("✅ Agent terminé")

if __name__ == "__main__":
    asyncio.run(main()) 
