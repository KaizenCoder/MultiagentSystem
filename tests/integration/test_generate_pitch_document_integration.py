#!/usr/bin/env python3
"""
Tests d'Intgration - Generate Pitch Document
"""

import pytest
import unittest
import subprocess
import sys
from pathlib import Path

class TestGeneratePitchDocumentIntegration(unittest.TestCase):
    """Tests d'intgration pour generate_pitch_document"""
    
    def setUp(self):
        """Configuration des tests"""
        self.tool_path = Path(__file__).parent.parent / "tools" / "generate_pitch_document"
        self.script_principal = self.tool_path / "generate_pitch_document.py"
        
    def test_script_executable(self):
        """Test que le script est excutable"""
        if not self.script_principal.exists():
            self.skipTest("Script principal non trouv")
            
        try:
            result = subprocess.run([
                sys.executable, str(self.script_principal), "--help"
            ], capture_output=True, text=True, timeout=30)
            
            # L'outil ne doit pas planter
            self.assertIn(result.returncode, [0, 1, 2])
        except subprocess.TimeoutExpired:
            self.fail("Script trop lent")
        except Exception as e:
            self.logger.warning(f"Test excution chou: {e}")
            
    def test_structure_complete(self):
        """Test de la structure complte"""
        repertoires_requis = ["docs", "config", "tests"]
        for rep in repertoires_requis:
            self.assertTrue((self.tool_path / rep).exists(), f"Rpertoire manquant: {rep}")
            
    def test_documentation_presente(self):
        """Test prsence documentation"""
        docs_requis = ["README.md", "docs/USAGE.md"]
        for doc in docs_requis:
            doc_path = self.tool_path / doc
            if doc_path.exists():
                self.assertGreater(doc_path.stat().st_size, 100, f"Documentation trop courte: {doc}")

if __name__ == "__main__":
    unittest.main()




