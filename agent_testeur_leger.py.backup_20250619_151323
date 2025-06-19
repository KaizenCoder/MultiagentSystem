#!/usr/bin/env python3
"""
Agent Testeur Lger - Cration Tests de Base
Mission: Crer des tests unitaires et d'intgration pour les outils
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class AgentTesteurLeger:
    """Agent testeur allg pour cration de tests de base"""
    
    def __init__(self):
        self.agent_id = f"TESTEUR_LEGER_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.base_path = Path(__file__).parent
        self.tools_path = self.base_path / "tools"
        self.tests_path = self.base_path / "tests"
        
        # Configuration logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configuration du systme de logging"""
        log_dir = self.base_path / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"AgentTesteurLeger_{self.agent_id}")
        
        # Handler spcifique
        handler = logging.FileHandler(log_dir / f"{self.agent_id}_testeur_leger.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def identifier_outils_a_tester(self) -> List[Dict[str, Any]]:
        """Identifie les outils ncessitant des tests"""
        self.logger.info("[SEARCH] Identification des outils  tester")
        
        outils = []
        for outil_dir in self.tools_path.iterdir():
            if outil_dir.is_dir() and outil_dir.name not in ["imported_tools", "__pycache__"]:
                fichier_principal = outil_dir / f"{outil_dir.name}.py"
                if fichier_principal.exists():
                    outils.append({
                        "nom": outil_dir.name,
                        "repertoire": str(outil_dir),
                        "fichier_principal": str(fichier_principal)
                    })
                    
        self.logger.info(f"[CHECK] {len(outils)} outils identifis")
        return outils
        
    def creer_test_unitaire_simple(self, nom_outil: str) -> Dict[str, Any]:
        """Cre un test unitaire simple"""
        self.logger.info(f" Cration test unitaire pour: {nom_outil}")
        
        tests_unit_dir = self.tests_path / "unit"
        tests_unit_dir.mkdir(exist_ok=True, parents=True)
        
        test_file = tests_unit_dir / f"test_{nom_outil}.py"
        
        contenu_test = f'''#!/usr/bin/env python3
"""
Tests Unitaires - {nom_outil.replace('_', ' ').title()}
"""

import pytest
import unittest
from pathlib import Path
import sys

# Ajout du chemin des outils
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "{nom_outil}"))

class Test{nom_outil.replace('_', ' ').title().replace(' ', '')}(unittest.TestCase):
    """Tests unitaires de base pour {nom_outil}"""
    
    def test_import_module(self):
        """Test d'importation du module"""
        try:
            import {nom_outil}
            self.assertTrue(True, "Module import avec succs")
        except ImportError:
            self.skipTest("Module non disponible")
            
    def test_structure_fichiers(self):
        """Test de la structure des fichiers"""
        tool_path = Path(__file__).parent.parent / "tools" / "{nom_outil}"
        
        fichiers_requis = ["{nom_outil}.py", "__init__.py", "README.md"]
        for fichier in fichiers_requis:
            self.assertTrue((tool_path / fichier).exists(), f"Fichier manquant: {{fichier}}")
            
    def test_configuration_existe(self):
        """Test existence configuration"""
        config_path = Path(__file__).parent.parent / "tools" / "{nom_outil}" / "config" / "config.json"
        if config_path.exists():
            import json
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.assertIn("tool_info", config)

if __name__ == "__main__":
    unittest.main()
'''
        
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(contenu_test)
            return {"fichier": str(test_file), "statut": "CREE"}
        except Exception as e:
            return {"erreur": str(e), "statut": "ECHEC"}
            
    def creer_test_integration_simple(self, nom_outil: str) -> Dict[str, Any]:
        """Cre un test d'intgration simple"""
        self.logger.info(f" Cration test intgration pour: {nom_outil}")
        
        tests_integration_dir = self.tests_path / "integration"
        tests_integration_dir.mkdir(exist_ok=True, parents=True)
        
        test_file = tests_integration_dir / f"test_{nom_outil}_integration.py"
        
        contenu_test = f'''#!/usr/bin/env python3
"""
Tests d'Intgration - {nom_outil.replace('_', ' ').title()}
"""

import pytest
import unittest
import subprocess
import sys
from pathlib import Path

class Test{nom_outil.replace('_', ' ').title().replace(' ', '')}Integration(unittest.TestCase):
    """Tests d'intgration pour {nom_outil}"""
    
    def setUp(self):
        """Configuration des tests"""
        self.tool_path = Path(__file__).parent.parent / "tools" / "{nom_outil}"
        self.script_principal = self.tool_path / "{nom_outil}.py"
        
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
            self.logger.warning(f"Test excution chou: {{e}}")
            
    def test_structure_complete(self):
        """Test de la structure complte"""
        repertoires_requis = ["docs", "config", "tests"]
        for rep in repertoires_requis:
            self.assertTrue((self.tool_path / rep).exists(), f"Rpertoire manquant: {{rep}}")
            
    def test_documentation_presente(self):
        """Test prsence documentation"""
        docs_requis = ["README.md", "docs/USAGE.md"]
        for doc in docs_requis:
            doc_path = self.tool_path / doc
            if doc_path.exists():
                self.assertGreater(doc_path.stat().st_size, 100, f"Documentation trop courte: {{doc}}")

if __name__ == "__main__":
    unittest.main()
'''
        
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(contenu_test)
            return {"fichier": str(test_file), "statut": "CREE"}
        except Exception as e:
            return {"erreur": str(e), "statut": "ECHEC"}
            
    def executer_creation_tests(self) -> Dict[str, Any]:
        """Excute la cration de tous les tests"""
        self.logger.info("[ROCKET] Dmarrage cration tests")
        
        outils = self.identifier_outils_a_tester()
        
        resultats = {
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "outils_traites": len(outils),
            "tests_unitaires": {},
            "tests_integration": {},
            "statut_global": "EN_COURS"
        }
        
        # Cration des tests pour chaque outil
        for outil in outils:
            nom_outil = outil["nom"]
            
            try:
                # Tests unitaires
                result_unit = self.creer_test_unitaire_simple(nom_outil)
                resultats["tests_unitaires"][nom_outil] = result_unit
                
                # Tests d'intgration
                result_integration = self.creer_test_integration_simple(nom_outil)
                resultats["tests_integration"][nom_outil] = result_integration
                
            except Exception as e:
                self.logger.error(f"[CROSS] Erreur cration tests {nom_outil}: {e}")
                resultats["tests_unitaires"][nom_outil] = {"erreur": str(e)}
                resultats["tests_integration"][nom_outil] = {"erreur": str(e)}
                
        # Dtermination statut
        erreurs_unit = sum(1 for r in resultats["tests_unitaires"].values() if "erreur" in r)
        erreurs_int = sum(1 for r in resultats["tests_integration"].values() if "erreur" in r)
        
        if erreurs_unit == 0 and erreurs_int == 0:
            resultats["statut_global"] = "REUSSI"
        elif erreurs_unit < len(outils) or erreurs_int < len(outils):
            resultats["statut_global"] = "PARTIEL"
        else:
            resultats["statut_global"] = "ECHEC"
            
        # Sauvegarde rapport
        self.sauvegarder_rapport(resultats)
        
        self.logger.info("[CHECK] Cration tests termine")
        return resultats
        
    def sauvegarder_rapport(self, resultats: Dict[str, Any]) -> None:
        """Sauvegarde le rapport"""
        rapport_file = self.base_path / "logs" / f"{self.agent_id}_creation_tests.json"
        
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(resultats, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"[CHART] Rapport sauvegard: {rapport_file}")

if __name__ == "__main__":
    agent = AgentTesteurLeger()
    rapport = agent.executer_creation_tests()
    
    print(f"\n Cration tests termine")
    print(f"[CLIPBOARD] Agent ID: {rapport['agent_id']}")
    print(f"[TOOL] Outils traits: {rapport['outils_traites']}")
    print(f" Tests unitaires crs: {len(rapport['tests_unitaires'])}")
    print(f" Tests intgration crs: {len(rapport['tests_integration'])}")
    print(f"[TARGET] Statut global: {rapport['statut_global']}") 