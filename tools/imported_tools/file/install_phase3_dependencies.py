#!/usr/bin/env python3
"""
NextGeneration Tool - install_phase3_dependencies
Adapté depuis SuperWhisper V6 pour NextGeneration

Configuration NextGeneration:
- Portable: Fonctionne depuis n'importe quel répertoire du projet
- Auto-détection du projet root
- Logging intégré NextGeneration
- Configuration centralisée

Usage:
    python install_phase3_dependencies.py [args]
    
Ou depuis n'importe où dans NextGeneration:
    python tools/imported_tools/file/install_phase3_dependencies.py [args]
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
logger = logging.getLogger("NextGen.install_phase3_dependencies")

# === Fin Configuration NextGeneration ===

"""
Installation des Dépendances Phase 3 - SuperWhisper V6 TTS
Installation automatique du binding Python Piper et autres optimisations
Prérequis pour les optimisations de performance

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

import subprocess
import logging
from pathlib import Path

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

class Phase3DependencyInstaller:
    """
    Installateur des dépendances Phase 3
    
     COMPOSANTS INSTALLÉS:
    1. Binding Python Piper (piper-tts)
    2. Dépendances audio (wave, asyncio)
    3. Outils de performance (psutil, memory_profiler)
    4. Validation de l'environnement GPU
    """
    
    def __init__(self):
        self.python_executable = sys.executable
        self.installation_log = []
        
        logger.info(" Phase 3 Dependency Installer initialisé")
        logger.info(f" Python: {self.python_executable}")
    
    def run_installation(self):
        """Exécution complète de l'installation"""
        logger.info("\n" + "="*80)
        logger.info(" INSTALLATION DÉPENDANCES PHASE 3")
        logger.info("="*80)
        
        try:
            # 1. Vérification de l'environnement
            self._check_environment()
            
            # 2. Installation du binding Python Piper
            self._install_piper_binding()
            
            # 3. Installation des dépendances audio
            self._install_audio_dependencies()
            
            # 4. Installation des outils de performance
            self._install_performance_tools()
            
            # 5. Validation finale
            self._validate_installation()
            
            # 6. Rapport final
            self._generate_report()
            
        except Exception as e:
            logger.info(f" Erreur installation: {e}")
            self._generate_error_report(e)
    
    def _check_environment(self):
        """Vérification de l'environnement système"""
        logger.info("\n VÉRIFICATION ENVIRONNEMENT")
        logger.info("-" * 50)
        
        # Version Python
        python_version = sys.version_info
        logger.info(f" Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version < (3, 8):
            raise RuntimeError("Python 3.8+ requis pour Phase 3")
        
        # Vérification pip
        try:
            import pip
            logger.info(f" pip: {pip.__version__}")
        except ImportError:
            raise RuntimeError("pip non disponible")
        
        # Vérification GPU (optionnelle)
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                logger.info(f" GPU: {gpu_name}")
            else:
                logger.info(" CUDA non disponible (mode CPU)")
        except ImportError:
            logger.info(" PyTorch non installé (GPU optionnel)")
        
        logger.info(" Environnement validé")
    
    def _install_piper_binding(self):
        """Installation du binding Python Piper"""
        logger.info("\n INSTALLATION BINDING PYTHON PIPER")
        logger.info("-" * 50)
        
        # Tentative d'installation via pip
        piper_packages = [
            'piper-tts',           # Package principal
            'piper-phonemize',     # Phonémisation
            'onnxruntime-gpu',     # Runtime ONNX GPU
        ]
        
        for package in piper_packages:
            try:
                logger.info(f" Installation {package}...")
                result = subprocess.run(
                    [self.python_executable, '-m', 'pip', 'install', package],
                    capture_output=True,
                    text=True,
                    check=True
                )
                logger.info(f" {package} installé avec succès")
                self.installation_log.append(f"SUCCESS: {package}")
                
            except subprocess.CalledProcessError as e:
                logger.info(f" Échec installation {package}: {e}")
                logger.info(f"   Sortie: {e.stdout}")
                logger.info(f"   Erreur: {e.stderr}")
                self.installation_log.append(f"FAILED: {package} - {e}")
                
                # Tentative alternative pour piper-tts
                if package == 'piper-tts':
                    logger.info(" Tentative installation alternative...")
                    self._install_piper_alternative()
    
    def _install_piper_alternative(self):
        """Installation alternative de Piper (compilation depuis source)"""
        logger.info(" Installation alternative Piper depuis source...")
        
        # Instructions pour installation manuelle
        logger.info("""
 INSTALLATION MANUELLE PIPER:

1. Télécharger les binaires Piper:
   https://github.com/rhasspy/piper/releases

2. Extraire dans le dossier piper/ du projet

3. Installer les dépendances Python:
   pip install onnxruntime-gpu numpy

4. Tester avec:
   python test_phase3_optimisations.py

 Le binding Python natif est optionnel.
   Le système utilisera le fallback CLI si indisponible.
        """)
        
        self.installation_log.append("INFO: Instructions manuelles Piper fournies")
    
    def _install_audio_dependencies(self):
        """Installation des dépendances audio"""
        logger.info("\n INSTALLATION DÉPENDANCES AUDIO")
        logger.info("-" * 50)
        
        audio_packages = [
            'wave',                # Manipulation WAV (built-in)
            'pydub',              # Manipulation audio avancée
            'soundfile',          # Lecture/écriture audio
        ]
        
        for package in audio_packages:
            if package == 'wave':
                logger.info(f" {package} (built-in Python)")
                continue
                
            try:
                logger.info(f" Installation {package}...")
                subprocess.run(
                    [self.python_executable, '-m', 'pip', 'install', package],
                    capture_output=True,
                    text=True,
                    check=True
                )
                logger.info(f" {package} installé")
                self.installation_log.append(f"SUCCESS: {package}")
                
            except subprocess.CalledProcessError as e:
                logger.info(f" Échec {package}: {e}")
                self.installation_log.append(f"FAILED: {package}")
    
    def _install_performance_tools(self):
        """Installation des outils de performance"""
        logger.info("\n INSTALLATION OUTILS PERFORMANCE")
        logger.info("-" * 50)
        
        perf_packages = [
            'psutil',             # Monitoring système
            'memory-profiler',    # Profiling mémoire
            'pyyaml',            # Configuration YAML
        ]
        
        for package in perf_packages:
            try:
                logger.info(f" Installation {package}...")
                subprocess.run(
                    [self.python_executable, '-m', 'pip', 'install', package],
                    capture_output=True,
                    text=True,
                    check=True
                )
                logger.info(f" {package} installé")
                self.installation_log.append(f"SUCCESS: {package}")
                
            except subprocess.CalledProcessError as e:
                logger.info(f" Échec {package}: {e}")
                self.installation_log.append(f"FAILED: {package}")
    
    def _validate_installation(self):
        """Validation de l'installation"""
        logger.info("\n VALIDATION INSTALLATION")
        logger.info("-" * 50)
        
        # Test des imports critiques
        test_imports = [
            ('yaml', 'Configuration YAML'),
            ('asyncio', 'Programmation asynchrone'),
            ('threading', 'Threading (built-in)'),
            ('collections', 'Collections (built-in)'),
            ('hashlib', 'Hashing (built-in)'),
            ('wave', 'Audio WAV (built-in)'),
        ]
        
        for module, description in test_imports:
            try:
                __import__(module)
                logger.info(f" {module}: {description}")
            except ImportError:
                logger.info(f" {module}: {description} - MANQUANT")
        
        # Test optionnel du binding Piper
        try:
            import piper
            logger.info(" piper: Binding Python natif disponible")
        except ImportError:
            logger.info(" piper: Binding Python non disponible (fallback CLI sera utilisé)")
        
        # Test des composants Phase 3
        try:
            sys.path.insert(0, str(Path.cwd()))
            from TTS.utils_audio import is_valid_wav
            logger.info(" TTS.utils_audio: Utilitaires audio disponibles")
        except ImportError as e:
            logger.info(f" TTS.utils_audio: {e}")
    
    def _generate_report(self):
        """Génération du rapport d'installation"""
        logger.info("\n" + "="*80)
        logger.info(" RAPPORT INSTALLATION PHASE 3")
        logger.info("="*80)
        
        # Comptage des succès/échecs
        successes = [log for log in self.installation_log if log.startswith('SUCCESS')]
        failures = [log for log in self.installation_log if log.startswith('FAILED')]
        
        logger.info(f" Succès: {len(successes)}")
        logger.info(f" Échecs: {len(failures)}")
        logger.info()
        
        if failures:
            logger.info(" ÉCHECS D'INSTALLATION:")
            for failure in failures:
                logger.info(f"   {failure}")
            logger.info()
        
        # Instructions post-installation
        logger.info(" PROCHAINES ÉTAPES:")
        logger.info("1. Exécuter: python test_phase3_optimisations.py")
        logger.info("2. Vérifier les performances avec les nouveaux handlers")
        logger.info("3. Activer piper_native_optimized dans config/tts.yaml")
        logger.info("4. Tester avec des textes longs (5000+ caractères)")
        logger.info()
        
        # Statut global
        if len(failures) == 0:
            logger.info(" Installation Phase 3 COMPLÈTE!")
        elif len(failures) <= 2:
            logger.info(" Installation Phase 3 PARTIELLE (fonctionnalités limitées)")
        else:
            logger.info(" Installation Phase 3 ÉCHOUÉE (révision requise)")
    
    def _generate_error_report(self, error):
        """Génération du rapport d'erreur"""
        logger.info("\n" + "="*80)
        logger.info(" RAPPORT D'ERREUR INSTALLATION")
        logger.info("="*80)
        
        logger.info(f"Erreur: {error}")
        logger.info()
        logger.info(" SOLUTIONS POSSIBLES:")
        logger.info("1. Vérifier la connexion Internet")
        logger.info("2. Mettre à jour pip: python -m pip install --upgrade pip")
        logger.info("3. Installer manuellement: pip install piper-tts")
        logger.info("4. Utiliser un environnement virtuel")
        logger.info("5. Vérifier les permissions d'écriture")
        logger.info()
        logger.info(" Support: Consulter la documentation SuperWhisper V6")


def main():
    """Point d'entrée principal"""
    installer = Phase3DependencyInstaller()
    installer.run_installation()


if __name__ == "__main__":
    main() 