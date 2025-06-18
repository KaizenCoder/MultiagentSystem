#!/usr/bin/env python3
"""
NextGeneration Tool - monitor_phase3
Adapté depuis SuperWhisper V6 pour NextGeneration

Configuration NextGeneration:
- Portable: Fonctionne depuis n'importe quel répertoire du projet
- Auto-détection du projet root
- Logging intégré NextGeneration
- Configuration centralisée

Usage:
    python monitor_phase3.py [args]
    
Ou depuis n'importe où dans NextGeneration:
    python tools/imported_tools/monitoring/monitor_phase3.py [args]
"""

import os
import sys
from pathlib import Path

# === Configuration NextGeneration ===
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR

# Auto-détection du projet NextGeneration
while PROJECT_ROOT.parent != PROJECT_ROOT:
    if (PROJECT_ROOT / "orchestrator").exists() or (PROJECT_ROOT / "memory_api").exists():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent

# Ajout du projet au Python path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Configuration logging NextGeneration
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("NextGen.monitor_phase3")

# === Fin Configuration NextGeneration ===

Monitoring Phase 3 - SuperWhisper V6 TTS
Surveillance en temps réel des métriques de performance
 Dashboard des optimisations Phase 3

 CONFIGURATION GPU: RTX 3090 (CUDA:1) OBLIGATOIRE
"""

import os
import sys
import pathlib

# =============================================================================
#  PORTABILITÉ AUTOMATIQUE - EXÉCUTABLE DEPUIS N'IMPORTE OÙ
# =============================================================================
def _setup_portable_environment():
    """Configure l'environnement pour exécution portable"""
    # Déterminer le répertoire racine du projet
    current_file = pathlib.Path(str(SCRIPT_DIR / Path(__file__).name)).resolve()
    
    # Chercher le répertoire racine (contient .git ou marqueurs projet)
    project_root = current_file
    for parent in current_file.parents:
        if any((parent / marker).exists() for marker in ['.git', 'pyproject.toml', 'requirements.txt', '.taskmaster']):
            project_root = parent
            break
    
    # Ajouter le projet root au Python path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Changer le working directory vers project root
    os.chdir(project_root)
    
    # Configuration GPU RTX 3090 obligatoire
    os.environ['CUDA_VISIBLE_DEVICES'] = '1'        # RTX 3090 24GB EXCLUSIVEMENT
    os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'  # Ordre stable des GPU
    
    logger.info(f" GPU Configuration: RTX 3090 (CUDA:1) forcée")
    logger.info(f" Project Root: {project_root}")
    logger.info(f" Working Directory: {os.getcwd()}")
    
    return project_root

# Initialiser l'environnement portable
_PROJECT_ROOT = _setup_portable_environment()

# Maintenant imports normaux...

import asyncio
import logging
import time
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import deque
import threading

# =============================================================================
#  CONFIGURATION CRITIQUE GPU - RTX 3090 UNIQUEMENT 
# =============================================================================
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:1024'

logger.info(" GPU Configuration: RTX 3090 (CUDA:1) forcée")
logger.info(f" CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES')}")

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Import du système TTS
try:
    from TTS.tts_manager import UnifiedTTSManager
    from TTS.utils_audio import is_valid_wav, get_wav_info
    import yaml
    TTS_AVAILABLE = True
except ImportError as e:
    logger.info(f" Système TTS non disponible: {e}")
    TTS_AVAILABLE = False

class Phase3Monitor:
    """
    Monitoring en temps réel des performances Phase 3
    
     MÉTRIQUES SURVEILLÉES:
    1. Latence de synthèse (ms)
    2. Débit de traitement (chars/ms)
    3. Taux de cache hit (%)
    4. Utilisation mémoire (MB)
    5. Backends utilisés
    6. Erreurs et fallbacks
    """
    
    def __init__(self, monitoring_duration_minutes=5):
        self.monitoring_duration = monitoring_duration_minutes
        self.tts_manager = None
        self.metrics = {
            'synthesis_times': deque(maxlen=100),
            'cache_hits': deque(maxlen=100),
            'cache_misses': deque(maxlen=100),
            'backend_usage': {},
            'errors': deque(maxlen=50),
            'throughput': deque(maxlen=100),
            'audio_sizes': deque(maxlen=100)
        }
        self.start_time = None
        self.running = False
        
        # Textes de test variés
        self.test_texts = [
            "Bonjour, test de performance.",
            "SuperWhisper V6 est un assistant vocal avancé.",
            "Les optimisations Phase 3 améliorent significativement les performances du système TTS.",
            "L'intelligence artificielle conversationnelle représente l'avenir des interactions homme-machine.",
            """SuperWhisper V6 intègre des technologies de pointe pour offrir une expérience utilisateur 
            exceptionnelle avec des temps de réponse optimisés et une qualité audio remarquable.""",
            "Test de cache - message récurrent.",  # Pour tester le cache
            "Test de cache - message récurrent.",  # Répétition pour cache hit
        ]
        
        logger.info(" Phase 3 Monitor initialisé")
        logger.info(f" Durée monitoring: {monitoring_duration_minutes} minutes")
        logger.info(f" {len(self.test_texts)} textes de test préparés")
    
    async def start_monitoring(self):
        """Démarrage du monitoring en temps réel"""
        logger.info("\n" + "="*80)
        logger.info(" DÉMARRAGE MONITORING PHASE 3")
        logger.info("="*80)
        
        if not TTS_AVAILABLE:
            logger.info(" Système TTS non disponible")
            return
        
        try:
            # Initialisation du TTS Manager
            await self._initialize_tts_manager()
            
            # Démarrage du monitoring
            self.start_time = time.time()
            self.running = True
            
            logger.info(f"\n Monitoring démarré pour {self.monitoring_duration} minutes")
            logger.info(" Métriques collectées en temps réel...")
            logger.info(" Appuyez sur Ctrl+C pour arrêter\n")
            
            # Boucle de monitoring
            await self._monitoring_loop()
            
        except KeyboardInterrupt:
            logger.info("\n Monitoring interrompu par l'utilisateur")
        except Exception as e:
            logger.info(f" Erreur monitoring: {e}")
            logging.exception("Erreur détaillée:")
        finally:
            self.running = False
            if self.tts_manager:
                await self.tts_manager.cleanup()
            
            # Génération du rapport final
            self._generate_monitoring_report()
    
    async def _initialize_tts_manager(self):
        """Initialisation du TTS Manager"""
        logger.info(" Initialisation TTS Manager...")
        
        # Chargement de la configuration
        config_path = Path("config/tts.yaml")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        start_time = time.perf_counter()
        self.tts_manager = UnifiedTTSManager(config)
        init_time = (time.perf_counter() - start_time) * 1000
        
        logger.info(f" TTS Manager initialisé en {init_time:.1f}ms")
    
    async def _monitoring_loop(self):
        """Boucle principale de monitoring"""
        test_count = 0
        last_report_time = time.time()
        
        while self.running:
            # Vérification du temps écoulé
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= (self.monitoring_duration * 60):
                logger.info(f"\n Durée de monitoring atteinte ({self.monitoring_duration} min)")
                break
            
            try:
                # Sélection d'un texte de test
                text = self.test_texts[test_count % len(self.test_texts)]
                test_count += 1
                
                # Test de synthèse
                await self._perform_synthesis_test(text, test_count)
                
                # Rapport périodique (toutes les 30 secondes)
                if time.time() - last_report_time >= 30:
                    self._print_live_metrics()
                    last_report_time = time.time()
                
                # Pause entre les tests
                await asyncio.sleep(2)
                
            except Exception as e:
                self.metrics['errors'].append({
                    'timestamp': datetime.now().isoformat(),
                    'error': str(e),
                    'test_count': test_count
                })
                logger.info(f" Erreur test #{test_count}: {e}")
                await asyncio.sleep(1)
    
    async def _perform_synthesis_test(self, text, test_count):
        """Exécution d'un test de synthèse avec collecte de métriques"""
        start_time = time.perf_counter()
        
        try:
            # Synthèse
            tts_result = await self.tts_manager.synthesize(text)
            synthesis_time = (time.perf_counter() - start_time) * 1000
            
            # Extraction des données audio
            if hasattr(tts_result, 'audio_data'):
                audio_data = tts_result.audio_data
            else:
                audio_data = tts_result
            
            # Collecte des métriques
            self.metrics['synthesis_times'].append(synthesis_time)
            self.metrics['throughput'].append(len(text) / synthesis_time if synthesis_time > 0 else 0)
            self.metrics['audio_sizes'].append(len(audio_data))
            
            # Détection cache hit (temps très rapide)
            if synthesis_time < 10:  # <10ms = probablement cache hit
                self.metrics['cache_hits'].append(test_count)
            else:
                self.metrics['cache_misses'].append(test_count)
            
            # Backend utilisé (estimation basée sur la latence)
            backend = self._estimate_backend_used(synthesis_time)
            if backend in self.metrics['backend_usage']:
                self.metrics['backend_usage'][backend] += 1
            else:
                self.metrics['backend_usage'][backend] = 1
            
            # Affichage en temps réel
            cache_status = " HIT" if synthesis_time < 10 else " MISS"
            logger.info(f"Test #{test_count:3d}: {synthesis_time:6.1f}ms | {len(text):3d} chars | {cache_status} | {backend}")
            
        except Exception as e:
            self.metrics['errors'].append({
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'test_count': test_count,
                'text_length': len(text)
            })
            raise
    
    def _estimate_backend_used(self, synthesis_time):
        """Estimation du backend utilisé basée sur la latence"""
        if synthesis_time < 10:
            return "cache"
        elif synthesis_time < 100:
            return "piper_native_optimized"
        elif synthesis_time < 500:
            return "piper_native"
        elif synthesis_time < 1500:
            return "piper_cli"
        elif synthesis_time < 3000:
            return "sapi_french"
        else:
            return "unknown"
    
    def _print_live_metrics(self):
        """Affichage des métriques en temps réel"""
        elapsed = time.time() - self.start_time
        
        logger.info("\n" + "="*60)
        logger.info(f" MÉTRIQUES LIVE - {elapsed/60:.1f} min écoulées")
        logger.info("="*60)
        
        # Métriques de latence
        if self.metrics['synthesis_times']:
            times = list(self.metrics['synthesis_times'])
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            logger.info(f" Latence: {avg_time:.1f}ms (min: {min_time:.1f}ms, max: {max_time:.1f}ms)")
        
        # Métriques de cache
        total_hits = len(self.metrics['cache_hits'])
        total_misses = len(self.metrics['cache_misses'])
        total_requests = total_hits + total_misses
        if total_requests > 0:
            hit_rate = (total_hits / total_requests) * 100
            logger.info(f" Cache: {hit_rate:.1f}% hit rate ({total_hits}/{total_requests})")
        
        # Métriques de débit
        if self.metrics['throughput']:
            throughputs = list(self.metrics['throughput'])
            avg_throughput = sum(throughputs) / len(throughputs)
            logger.info(f" Débit: {avg_throughput:.3f} chars/ms")
        
        # Backends utilisés
        if self.metrics['backend_usage']:
            logger.info(" Backends:")
            for backend, count in self.metrics['backend_usage'].items():
                percentage = (count / sum(self.metrics['backend_usage'].values())) * 100
                logger.info(f"   {backend}: {count} ({percentage:.1f}%)")
        
        # Erreurs
        error_count = len(self.metrics['errors'])
        if error_count > 0:
            logger.info(f" Erreurs: {error_count}")
        
        logger.info()
    
    def _generate_monitoring_report(self):
        """Génération du rapport final de monitoring"""
        logger.info("\n" + "="*80)
        logger.info(" RAPPORT FINAL MONITORING PHASE 3")
        logger.info("="*80)
        
        total_duration = time.time() - self.start_time if self.start_time else 0
        total_tests = len(self.metrics['synthesis_times'])
        
        logger.info(f" Durée totale: {total_duration/60:.1f} minutes")
        logger.info(f" Tests effectués: {total_tests}")
        logger.info(f" Fréquence: {total_tests/(total_duration/60):.1f} tests/min")
        logger.info()
        
        # Analyse des performances
        if self.metrics['synthesis_times']:
            times = list(self.metrics['synthesis_times'])
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            logger.info(" PERFORMANCES:")
            logger.info(f"   Latence moyenne: {avg_time:.1f}ms")
            logger.info(f"   Latence minimale: {min_time:.1f}ms")
            logger.info(f"   Latence maximale: {max_time:.1f}ms")
            
            # Percentiles
            sorted_times = sorted(times)
            p50 = sorted_times[len(sorted_times)//2]
            p95 = sorted_times[int(len(sorted_times)*0.95)]
            logger.info(f"   P50: {p50:.1f}ms")
            logger.info(f"   P95: {p95:.1f}ms")
            logger.info()
        
        # Analyse du cache
        total_hits = len(self.metrics['cache_hits'])
        total_misses = len(self.metrics['cache_misses'])
        total_requests = total_hits + total_misses
        
        if total_requests > 0:
            hit_rate = (total_hits / total_requests) * 100
            logger.info(" CACHE:")
            logger.info(f"   Taux de hit: {hit_rate:.1f}%")
            logger.info(f"   Hits: {total_hits}")
            logger.info(f"   Misses: {total_misses}")
            logger.info()
        
        # Analyse des backends
        if self.metrics['backend_usage']:
            logger.info(" BACKENDS UTILISÉS:")
            total_backend_calls = sum(self.metrics['backend_usage'].values())
            for backend, count in sorted(self.metrics['backend_usage'].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_backend_calls) * 100
                logger.info(f"   {backend}: {count} ({percentage:.1f}%)")
            logger.info()
        
        # Analyse du débit
        if self.metrics['throughput']:
            throughputs = list(self.metrics['throughput'])
            avg_throughput = sum(throughputs) / len(throughputs)
            max_throughput = max(throughputs)
            logger.info(" DÉBIT:")
            logger.info(f"   Débit moyen: {avg_throughput:.3f} chars/ms")
            logger.info(f"   Débit maximal: {max_throughput:.3f} chars/ms")
            logger.info()
        
        # Analyse des erreurs
        error_count = len(self.metrics['errors'])
        if error_count > 0:
            logger.info(" ERREURS:")
            logger.info(f"   Total: {error_count}")
            logger.info(f"   Taux d'erreur: {(error_count/total_tests)*100:.1f}%")
            
            # Dernières erreurs
            recent_errors = list(self.metrics['errors'])[-3:]
            for error in recent_errors:
                logger.info(f"   - {error['timestamp']}: {error['error']}")
            logger.info()
        
        # Validation des objectifs Phase 3
        logger.info(" OBJECTIFS PHASE 3:")
        
        # Objectif latence
        if self.metrics['synthesis_times']:
            avg_time = sum(self.metrics['synthesis_times']) / len(self.metrics['synthesis_times'])
            latency_ok = avg_time < 1000  # <1s acceptable
            logger.info(f"   Latence <1s: {'' if latency_ok else ''} ({avg_time:.1f}ms)")
        
        # Objectif cache
        cache_ok = hit_rate > 10 if total_requests > 0 else False  # >10% hit rate
        logger.info(f"   Cache efficace: {'' if cache_ok else ''} ({hit_rate:.1f}%)")
        
        # Objectif stabilité
        stability_ok = error_count < (total_tests * 0.05)  # <5% erreurs
        logger.info(f"   Stabilité >95%: {'' if stability_ok else ''} ({((total_tests-error_count)/total_tests)*100:.1f}%)")
        
        logger.info("\n Monitoring Phase 3 terminé!")
        
        # Sauvegarde des métriques
        self._save_metrics_to_file()
    
    def _save_metrics_to_file(self):
        """Sauvegarde des métriques dans un fichier JSON"""
        try:
            metrics_data = {
                'timestamp': datetime.now().isoformat(),
                'duration_minutes': (time.time() - self.start_time) / 60 if self.start_time else 0,
                'total_tests': len(self.metrics['synthesis_times']),
                'synthesis_times': list(self.metrics['synthesis_times']),
                'cache_hits': len(self.metrics['cache_hits']),
                'cache_misses': len(self.metrics['cache_misses']),
                'backend_usage': dict(self.metrics['backend_usage']),
                'errors': list(self.metrics['errors']),
                'throughput': list(self.metrics['throughput']),
                'audio_sizes': list(self.metrics['audio_sizes'])
            }
            
            # Sauvegarde
            metrics_file = Path(f"monitoring_phase3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(metrics_file, 'w', encoding='utf-8') as f:
                json.dump(metrics_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f" Métriques sauvegardées: {metrics_file}")
            
        except Exception as e:
            logger.info(f" Erreur sauvegarde métriques: {e}")

async def main():
    """Point d'entrée principal"""
    logger.info(" SuperWhisper V6 - Monitoring Phase 3")
    logger.info(" Surveillance en temps réel des performances TTS")
    
    # Durée de monitoring (par défaut 5 minutes)
    duration = 5
    
    monitor = Phase3Monitor(monitoring_duration_minutes=duration)
    await monitor.start_monitoring()

if __name__ == "__main__":
    asyncio.run(main()) 