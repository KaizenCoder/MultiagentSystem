#!/usr/bin/env python3
"""
Tests de validation pour l'architecture modulaire de logging.
"""

import os
import sys
import time
import tempfile
import unittest
import logging
from pathlib import Path
from cryptography.fernet import Fernet
from unittest.mock import patch, MagicMock
import shutil

# Ajouter la racine du projet au sys.path pour permettre les imports absolus
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# Importer depuis notre nouvelle architecture
from core import logging_manager, LoggingConfig
from core.handlers.async_handler import AsyncLogHandler, CompositeHandler
from core.handlers.encryption_handler import EncryptionHandler

def find_base_handlers(handler):
    """Trouve récursivement les handlers de base dans une chaîne de wrappers."""
    if isinstance(handler, CompositeHandler):
        handlers = []
        for h in handler.handlers:
            handlers.extend(find_base_handlers(h))
        return handlers
    elif hasattr(handler, 'base_handler'):
        return find_base_handlers(handler.base_handler)
    else:
        return [handler]

class TestModularArchitecture(unittest.TestCase):
    """Tests de la nouvelle architecture de logging modulaire."""
    
    def setUp(self):
        """Setup pour chaque test."""
        self.temp_dir = tempfile.mkdtemp()
        # On s'assure que chaque test a une instance fraîche du manager
        # en réinitialisant son état interne si nécessaire (pour les tests avancés)
        # Pour l'instant, le singleton suffit.
    
    def tearDown(self):
        """Cleanup après chaque test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_01_singleton_instance(self):
        """Test 1: L'instance `logging_manager` est bien un singleton."""
        from core import logging_manager as lm1
        from core import logging_manager as lm2
        self.assertIs(lm1, lm2, "L'instance importée devrait être la même (singleton).")

    def test_02_logger_creation_with_default_config(self):
        """Test 2: Création d'un logger avec la config par défaut."""
        logger = logging_manager.get_logger('default')
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, 'nextgen.default')

        base_handlers = find_base_handlers(logger.handlers[0])
        self.assertEqual(len(base_handlers), 2, "Devrait avoir un handler console et un handler fichier.")

    def test_03_logger_creation_with_custom_config(self):
        """Test 3: Création d'un logger avec une configuration ad-hoc."""
        custom_config = {
            'logger_name': 'test.custom',
            'log_level': 'DEBUG',
            'log_dir': self.temp_dir,
            'console_enabled': True,
            'file_enabled': True
        }
        
        logger = logging_manager.get_logger('custom_logger_test', custom_config=custom_config)
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, 'test.custom')

        base_handlers = find_base_handlers(logger.handlers[0])
        self.assertTrue(any(isinstance(h, logging.StreamHandler) for h in base_handlers))
    
    def test_04_performance_benchmark(self):
        """Test 4: Performance de base < 0.1ms par message."""
        # Note: 0.02ms est l'objectif en production avec async. 
        # 0.1ms est une cible raisonnable pour les tests synchrones.
        logger = logging_manager.get_logger('performance', custom_config={
            'logger_name': 'test.performance',
            'console_enabled': False, 
            'file_enabled': False
        })
        
        message_count = 1000
        start_time = time.perf_counter()
        for i in range(message_count):
            logger.info(f"Message de performance {i}")
        end_time = time.perf_counter()
        
        duration = end_time - start_time
        avg_latency_ms = (duration / message_count) * 1000
        
        print(f"\n[Benchmark] Latence moyenne sur {message_count} messages: {avg_latency_ms:.4f} ms")
        self.assertLess(avg_latency_ms, 0.1, "La latence moyenne devrait être inférieure à 0.1ms")

    def test_05_file_creation(self):
        """Test 5: Création correcte du fichier de log."""
        config = {
            'logger_name': 'test.filecreation',
            'log_level': 'INFO',
            'log_dir': self.temp_dir,
            'console_enabled': False,
            'file_enabled': True,
            'filename_pattern': '{component}.log' # Pattern simple pour le test
        }
        
        logger = logging_manager.get_logger('file_creation_test', custom_config=config)
        logger.info("Ce message doit se trouver dans un fichier.")
        
        # Le handler de fichier peut avoir un délai
        time.sleep(0.1)
        
        log_file = Path(self.temp_dir) / 'test.filecreation.log'
        
        # Note : à cause du glob, le fichier de test peut être difficile à prédire
        # On va chercher un fichier qui correspond au pattern
        files = list(Path(self.temp_dir).glob("*.log"))
        self.assertTrue(len(files) > 0, "Aucun fichier de log n'a été créé.")
        
        # On vérifie que le message est bien dans le premier fichier trouvé
        content = files[0].read_text()
        self.assertIn("Ce message doit se trouver dans un fichier.", content)

    def test_06_async_handler_wrapping(self):
        """Test 6: Le mode asynchrone encapsule bien les autres handlers."""
        async_config = {
            'logger_name': 'test.async',
            'log_level': 'INFO',
            'log_dir': self.temp_dir,
            'console_enabled': True,
            'file_enabled': True,
            'async_enabled': True # Activation du mode asynchrone
        }
        
        logger = logging_manager.get_logger('async_test', custom_config=async_config)
        
        # Le logger ne doit avoir qu'un seul handler : le wrapper asynchrone
        self.assertEqual(len(logger.handlers), 1, "Le logger asynchrone ne doit avoir qu'un seul handler wrapper.")
        
        # Et ce handler doit être de type AsyncLogHandler
        from core.handlers.async_handler import AsyncLogHandler
        self.assertIsInstance(logger.handlers[0], AsyncLogHandler, "Le handler doit être un AsyncLogHandler.")

    def test_07_encryption_handler(self):
        """Test 7: Le chiffrement AES-256 fonctionne correctement."""
        secret_message = "Ceci est un message top secret."
        key = Fernet.generate_key()

        encryption_config = {
            'logger_name': 'test.encryption',
            'log_level': 'INFO',
            'log_dir': self.temp_dir,
            'console_enabled': False,
            'file_enabled': True,
            'filename_pattern': 'encrypted_logs.log',
            'encryption_enabled': True,
            'encryption_config': {
                'key': key.decode()
            }
        }
        
        logger = logging_manager.get_logger('encryption_test', custom_config=encryption_config)
        logger.info(secret_message)

        # Attendre que le log soit écrit
        time.sleep(0.1)

        # 1. Lire le fichier et vérifier que le contenu N'EST PAS le message original
        log_file = Path(self.temp_dir) / 'encrypted_logs.log'
        self.assertTrue(log_file.exists(), "Le fichier de log chiffré n'a pas été créé.")
        
        encrypted_content = log_file.read_text()
        self.assertNotIn(secret_message, encrypted_content, "Le message secret ne devrait pas être en clair dans le fichier.")

        # 2. Déchiffrer le contenu pour vérifier l'intégrité
        # On extrait le message chiffré (qui est après le formatage du log)
        encrypted_part = encrypted_content.split(' - ')[-1].strip()
        
        fernet = Fernet(key)
        decrypted_message = fernet.decrypt(encrypted_part.encode()).decode()
        
        self.assertEqual(secret_message, decrypted_message, "Le message déchiffré ne correspond pas à l'original.")

    @patch('core.manager.LoggingManager.get_logger')
    def test_09_utility_methods(self, mock_get_logger):
        """Test 9: Les méthodes utilitaires fonctionnent correctement."""
        # 1. Test de get_audit_logger
        mock_audit_logger = MagicMock()
        mock_get_logger.return_value = mock_audit_logger
        
        audit_logger = logging_manager.get_audit_logger()
        
        # Vérifier que get_logger a été appelé avec la bonne config
        mock_get_logger.assert_called_with('audit', custom_config={
            'logger_name': 'nextgen.audit',
            'log_level': 'INFO',
            'file_enabled': True,
            'filename_pattern': 'audit.log',
            'console_enabled': False,
            'encryption_enabled': True
        })
        self.assertIs(audit_logger, mock_audit_logger)

        # 2. Test de log_performance
        mock_perf_logger = MagicMock()
        # On fait en sorte que l'appel pour 'performance' retourne notre mock
        mock_get_logger.side_effect = lambda name, custom_config=None: mock_perf_logger if name == 'performance' else MagicMock()

        logging_manager.log_performance("Test op", 0.12345)
        
        mock_perf_logger.info.assert_called_once_with(
            "Test op - Temps d'exécution: 0.1235s",
            extra={'category': 'performance'}
        )


def run_modular_validation():
    """Lance les tests de validation pour l'architecture modulaire."""
    print("🚀 VALIDATION DE L'ARCHITECTURE MODULAIRE")
    print("=" * 50)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestModularArchitecture)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ TOUS LES TESTS DE L'ARCHITECTURE MODULAIRE SONT RÉUSSIS !")
        return True
    else:
        print("❌ ÉCHECS DÉTECTÉS DANS L'ARCHITECTURE MODULAIRE.")
        return False


if __name__ == "__main__":
    success = run_modular_validation()
    sys.exit(0 if success else 1) 



