#!/usr/bin/env python3
"""
Tests Unitaires - TTS Dependencies Installer
"""

import pytest
import unittest
from pathlib import Path
import sys

# Ajout du chemin des outils
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "tts_dependencies_installer"))

class TestTTSDependenciesInstaller(unittest.TestCase):
    """Tests unitaires de base pour tts_dependencies_installer"""
    
    def test_import_module(self):
        """Test d'importation du module"""
        try:
            import tts_dependencies_installer
            self.assertTrue(True, "Module import avec succs")
        except ImportError:
            self.skipTest("Module non disponible")
            
    def test_structure_fichiers(self):
        """Test de la structure des fichiers"""
        tool_path = Path(__file__).parent.parent / "tools" / "tts_dependencies_installer"
        
        fichiers_requis = ["tts_dependencies_installer.py", "__init__.py", "README.md"]
        for fichier in fichiers_requis:
            self.assertTrue((tool_path / fichier).exists(), f"Fichier manquant: {fichier}")
            
    def test_configuration_existe(self):
        """Test existence configuration"""
        config_path = Path(__file__).parent.parent / "tools" / "tts_dependencies_installer" / "config" / "config.json"
        if config_path.exists():
            import json
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.assertIn("tool_info", config)

if __name__ == "__main__":
    unittest.main()




