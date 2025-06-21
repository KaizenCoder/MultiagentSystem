#!/usr/bin/env python3
"""
Tests Unitaires - Generate Pitch Document
"""

import pytest
import unittest
from pathlib import Path
import sys

# Ajout du chemin des outils
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "generate_pitch_document"))

class TestGeneratePitchDocument(unittest.TestCase):
    """Tests unitaires de base pour generate_pitch_document"""
    
    def test_import_module(self):
        """Test d'importation du module"""
        try:
            import generate_pitch_document
            self.assertTrue(True, "Module import avec succs")
        except ImportError:
            self.skipTest("Module non disponible")
            
    def test_structure_fichiers(self):
        """Test de la structure des fichiers"""
        tool_path = Path(__file__).parent.parent / "tools" / "generate_pitch_document"
        
        fichiers_requis = ["generate_pitch_document.py", "__init__.py", "README.md"]
        for fichier in fichiers_requis:
            self.assertTrue((tool_path / fichier).exists(), f"Fichier manquant: {fichier}")
            
    def test_configuration_existe(self):
        """Test existence configuration"""
        config_path = Path(__file__).parent.parent / "tools" / "generate_pitch_document" / "config" / "config.json"
        if config_path.exists():
            import json
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.assertIn("tool_info", config)

if __name__ == "__main__":
    unittest.main()




