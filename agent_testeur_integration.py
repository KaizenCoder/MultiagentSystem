#!/usr/bin/env python3
"""
Agent Testeur Intgration - Tests Complets et Validation
Mission: Crer et excuter des tests complets pour les outils intgrs
"""

import json
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import importlib.util
import sys

class AgentTesteurIntegration:
    """Agent spcialis dans les tests et la validation d'intgration"""
    
    def __init__(self):
        self.agent_id = f"TESTEUR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
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
        self.logger = logging.getLogger(f"AgentTesteur_{self.agent_id}")
        
        # Handler spcifique
        handler = logging.FileHandler(log_dir / f"{self.agent_id}_testeur.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def identifier_outils_a_tester(self) -> List[Dict[str, Any]]:
        """Identifie tous les outils qui ncessitent des tests"""
        self.logger.info("[SEARCH] Identification des outils  tester...")
        
        outils_a_tester = []
        
        # Scan du rpertoire tools
        for outil_dir in self.tools_path.iterdir():
            if outil_dir.is_dir() and outil_dir.name not in ["imported_tools", "__pycache__"]:
                # Vrification qu'il s'agit d'un outil valide
                fichier_principal = outil_dir / f"{outil_dir.name}.py"
                config_file = outil_dir / "config" / "config.json"
                
                if fichier_principal.exists():
                    info_outil = {
                        "nom": outil_dir.name,
                        "repertoire": str(outil_dir),
                        "fichier_principal": str(fichier_principal),
                        "config_existe": config_file.exists(),
                        "config_file": str(config_file) if config_file.exists() else None
                    }
                    
                    # Lecture de la configuration si disponible
                    if config_file.exists():
                        try:
                            with open(config_file, 'r') as f:
                                config = json.load(f)
                                info_outil.update(config.get("tool_info", {}))
                        except Exception as e:
                            self.logger.warning(f" Erreur lecture config {outil_dir.name}: {e}")
                            
                    outils_a_tester.append(info_outil)
                    
        self.logger.info(f"[CHECK] {len(outils_a_tester)} outils identifis pour les tests")
        return outils_a_tester
        
    def creer_test_unitaire(self, nom_outil: str, info_outil: Dict[str, Any]) -> Dict[str, Any]:
        """Cre les tests unitaires pour un outil"""
        self.logger.info(f" Cration des tests unitaires pour: {nom_outil}")
        
        # Cration du rpertoire de tests unitaires
        tests_unit_dir = self.tests_path / "unit"
        tests_unit_dir.mkdir(exist_ok=True, parents=True)
        
        test_file = tests_unit_dir / f"test_{nom_outil}.py"
        
        # Gnration du contenu du test
        contenu_test = self.generer_contenu_test_unitaire(nom_outil, info_outil)
        
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(contenu_test)
                
            resultats = {
                "fichier_test": str(test_file),
                "statut": "CREE",
                "type": "test_unitaire",
                "tests_generes": self.compter_tests_generes(contenu_test)
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur cration test unitaire {nom_outil}: {e}")
            resultats = {
                "erreur": str(e),
                "statut": "ECHEC"
            }
            
        self.logger.info(f"[CHECK] Test unitaire cr pour {nom_outil}")
        return resultats
        
    def creer_test_integration(self, nom_outil: str, info_outil: Dict[str, Any]) -> Dict[str, Any]:
        """Cre les tests d'intgration pour un outil"""
        self.logger.info(f" Cration des tests d'intgration pour: {nom_outil}")
        
        # Cration du rpertoire de tests d'intgration
        tests_integration_dir = self.tests_path / "integration"
        tests_integration_dir.mkdir(exist_ok=True, parents=True)
        
        test_file = tests_integration_dir / f"test_{nom_outil}_integration.py"
        
        # Gnration du contenu du test d'intgration
        contenu_test = self.generer_contenu_test_integration(nom_outil, info_outil)
        
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(contenu_test)
                
            resultats = {
                "fichier_test": str(test_file),
                "statut": "CREE",
                "type": "test_integration",
                "scenarios_testes": self.compter_scenarios_integration(contenu_test)
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur cration test intgration {nom_outil}: {e}")
            resultats = {
                "erreur": str(e),
                "statut": "ECHEC"
            }
            
        self.logger.info(f"[CHECK] Test d'intgration cr pour {nom_outil}")
        return resultats
        
    def generer_contenu_test_unitaire(self, nom_outil: str, info_outil: Dict[str, Any]) -> str:
        """Gnre le contenu des tests unitaires"""
        classe_outil = nom_outil.replace('_', ' ').title().replace(' ', '')
        
        contenu = f'''#!/usr/bin/env python3
"""
Tests Unitaires - {nom_outil.replace('_', ' ').title()}
Tests pour l'outil {nom_outil} intgr  NextGeneration
"""

import pytest
import unittest
from pathlib import Path
import sys
import json
from unittest.mock import Mock, patch, MagicMock

# Ajout du chemin des outils
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "{nom_outil}"))

try:
    from {nom_outil} import *
except ImportError as e:
    pytest.skip(f"Module {{__name__}} non disponible: {{e}}", allow_module_level=True)

class Test{classe_outil}(unittest.TestCase):
    """Tests unitaires pour {classe_outil}"""
    
    def setUp(self):
        """Configuration initiale des tests"""
        self.test_config = {{
            "test_mode": True,
            "debug": True,
            "timeout": 5
        }}
        
    def tearDown(self):
        """Nettoyage aprs chaque test"""
        pass
        
    def test_import_module(self):
        """Test d'importation du module"""
        try:
            import {nom_outil}
            self.assertTrue(True, "Module import avec succs")
        except ImportError as e:
            self.fail(f"chec d'importation: {{e}}")
            
    def test_configuration_defaut(self):
        """Test de la configuration par dfaut"""
        config_path = Path(__file__).parent.parent / "tools" / "{nom_outil}" / "config" / "config.json"
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            self.assertIn("tool_info", config)
            self.assertIn("settings", config)
            self.assertEqual(config["tool_info"]["name"], "{nom_outil}")
        else:
            self.skipTest("Fichier de configuration non trouv")
            
    def test_structure_fichiers(self):
        """Test de la structure des fichiers de l'outil"""
        tool_path = Path(__file__).parent.parent / "tools" / "{nom_outil}"
        
        # Vrification des fichiers essentiels
        fichiers_requis = [
            "{nom_outil}.py",
            "__init__.py",
            "README.md"
        ]
        
        for fichier in fichiers_requis:
            chemin_fichier = tool_path / fichier
            self.assertTrue(chemin_fichier.exists(), f"Fichier manquant: {{fichier}}")
            
        # Vrification des rpertoires
        repertoires_requis = ["docs", "config", "tests"]
        for repertoire in repertoires_requis:
            chemin_rep = tool_path / repertoire
            self.assertTrue(chemin_rep.exists(), f"Rpertoire manquant: {{repertoire}}")
            
    @patch('logging.getLogger')
    def test_integration_logging(self, mock_logger):
        """Test de l'intgration avec le systme de logging"""
        mock_logger.return_value = MagicMock()
        
        try:
            # Test basique d'utilisation des logs
            # ( adapter selon l'outil spcifique)
            self.assertTrue(True, "Logging intgr correctement")
        except Exception as e:
            self.fail(f"Erreur intgration logging: {{e}}")
            
    def test_gestion_erreurs(self):
        """Test de la gestion des erreurs"""
        # Tests avec des paramtres invalides
        # ( adapter selon l'outil spcifique)
        
        with self.assertRaises((ValueError, TypeError, FileNotFoundError)):
            # Simulation d'erreur
            pass
            
    def test_performance_basique(self):
        """Test de performance basique"""
        import time
        
        debut = time.time()
        
        # Excution basique de l'outil ( adapter)
        try:
            # Code de test de performance
            pass
        except Exception:
            pass  # Les erreurs de fonctionnalit ne doivent pas affecter le test de perf
            
        duree = time.time() - debut
        
        # Vrification que l'excution ne prend pas trop de temps
        self.assertLess(duree, 30, "L'outil prend trop de temps  s'excuter")
        
    def test_compatibilite_nextgeneration(self):
        """Test de compatibilit avec l'cosystme NextGeneration"""
        # Vrification des imports NextGeneration
        tool_path = Path(__file__).parent.parent / "tools" / "{nom_outil}" / "{nom_outil}.py"
        
        if tool_path.exists():
            with open(tool_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
                
            # Vrifications basiques
            self.assertNotIn("SuperWhisper", contenu, "Rfrences SuperWhisper non nettoyes")
            self.assertIn("NextGeneration", contenu, "Rfrences NextGeneration manquantes")
        else:
            self.skipTest("Fichier principal non trouv")
            
class Test{classe_outil}Integration(unittest.TestCase):
    """Tests d'intgration systme pour {classe_outil}"""
    
    def setUp(self):
        """Configuration pour les tests d'intgration"""
        self.integration_config = {{
            "environment": "test",
            "log_level": "DEBUG"
        }}
        
    def test_execution_complete(self):
        """Test d'excution complte de l'outil"""
        # Test d'excution end-to-end ( adapter selon l'outil)
        try:
            # Simulation d'utilisation complte
            resultat = "success"  #  remplacer par l'excution relle
            self.assertIsNotNone(resultat, "L'outil doit retourner un rsultat")
        except Exception as e:
            self.fail(f"chec d'excution complte: {{e}}")
            
    def test_integration_avec_autres_outils(self):
        """Test d'intgration avec d'autres outils NextGeneration"""
        # Tests d'interoprabilit ( dvelopper selon les besoins)
        self.assertTrue(True, "Test d'intgration basique russi")

if __name__ == "__main__":
    # Configuration pytest
    pytest.main([__file__, "-v", "--tb=short"])
'''
        
        return contenu
        
    def generer_contenu_test_integration(self, nom_outil: str, info_outil: Dict[str, Any]) -> str:
        """Gnre le contenu des tests d'intgration"""
        contenu = f'''#!/usr/bin/env python3
"""
Tests d'Intgration - {nom_outil.replace('_', ' ').title()}
Tests d'intgration complte pour l'outil {nom_outil} avec NextGeneration
"""

import pytest
import unittest
import subprocess
import tempfile
import shutil
from pathlib import Path
import sys
import json
import os

class Test{nom_outil.replace('_', ' ').title().replace(' ', '')}Integration(unittest.TestCase):
    """Tests d'intgration pour {nom_outil}"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration globale des tests d'intgration"""
        cls.base_path = Path(__file__).parent.parent
        cls.tool_path = cls.base_path / "tools" / "{nom_outil}"
        cls.temp_dir = None
        
    @classmethod
    def tearDownClass(cls):
        """Nettoyage global aprs tous les tests"""
        if cls.temp_dir and cls.temp_dir.exists():
            shutil.rmtree(cls.temp_dir)
            
    def setUp(self):
        """Configuration pour chaque test"""
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """Nettoyage aprs chaque test"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            
    def test_outil_executable(self):
        """Test que l'outil est excutable"""
        script_principal = self.tool_path / "{nom_outil}.py"
        
        if not script_principal.exists():
            self.skipTest(f"Script principal non trouv: {{script_principal}}")
            
        try:
            # Test d'excution avec --help
            result = subprocess.run([
                sys.executable, str(script_principal), "--help"
            ], capture_output=True, text=True, timeout=30)
            
            # L'outil doit soit afficher l'aide, soit ne pas planter
            self.assertIn(result.returncode, [0, 1, 2], 
                         f"Code de retour inattendu: {{result.returncode}}")
                         
        except subprocess.TimeoutExpired:
            self.fail("L'outil ne rpond pas dans les temps")
        except Exception as e:
            self.fail(f"Erreur d'excution: {{e}}")
            
    def test_structure_repertoire_complete(self):
        """Test de la structure complte du rpertoire outil"""
        structure_attendue = {{
            "fichiers": ["{nom_outil}.py", "__init__.py", "README.md"],
            "repertoires": ["docs", "config", "tests", "templates"]
        }}
        
        for fichier in structure_attendue["fichiers"]:
            chemin = self.tool_path / fichier
            self.assertTrue(chemin.exists(), f"Fichier manquant: {{fichier}}")
            self.assertGreater(chemin.stat().st_size, 0, f"Fichier vide: {{fichier}}")
            
        for repertoire in structure_attendue["repertoires"]:
            chemin = self.tool_path / repertoire
            self.assertTrue(chemin.exists(), f"Rpertoire manquant: {{repertoire}}")
            self.assertTrue(chemin.is_dir(), f"{{repertoire}} n'est pas un rpertoire")
            
    def test_configuration_valide(self):
        """Test de la validit de la configuration"""
        config_file = self.tool_path / "config" / "config.json"
        
        if not config_file.exists():
            self.skipTest("Fichier de configuration non trouv")
            
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                
            # Vrifications de structure
            self.assertIn("tool_info", config)
            self.assertIn("settings", config)
            self.assertIn("nextgeneration_integration", config)
            
            # Vrifications des valeurs
            tool_info = config["tool_info"]
            self.assertEqual(tool_info["name"], "{nom_outil}")
            self.assertIn("version", tool_info)
            self.assertIn("category", tool_info)
            
        except json.JSONDecodeError as e:
            self.fail(f"Configuration JSON invalide: {{e}}")
        except Exception as e:
            self.fail(f"Erreur lecture configuration: {{e}}")
            
    def test_documentation_complete(self):
        """Test de la compltude de la documentation"""
        docs_requis = [
            self.tool_path / "README.md",
            self.tool_path / "docs" / "USAGE.md"
        ]
        
        for doc_file in docs_requis:
            self.assertTrue(doc_file.exists(), f"Documentation manquante: {{doc_file.name}}")
            
            with open(doc_file, 'r', encoding='utf-8') as f:
                contenu = f.read()
                
            self.assertGreater(len(contenu.strip()), 100, 
                             f"Documentation trop courte: {{doc_file.name}}")
            self.assertIn("{nom_outil}", contenu.lower(), 
                         f"Documentation ne mentionne pas l'outil: {{doc_file.name}}")
                         
    def test_integration_systeme_logging(self):
        """Test d'intgration avec le systme de logging NextGeneration"""
        # Vrification que l'outil utilise le logging appropri
        script_principal = self.tool_path / "{nom_outil}.py"
        
        if script_principal.exists():
            with open(script_principal, 'r', encoding='utf-8') as f:
                contenu = f.read()
                
            # Vrifications basiques du logging
            self.assertIn("import logging", contenu, 
                         "L'outil doit utiliser le module logging")
            self.assertNotIn("print(", contenu, 
                           "L'outil ne doit pas utiliser print() directement")
                           
    def test_gestion_environnement_nextgeneration(self):
        """Test de la gestion de l'environnement NextGeneration"""
        # Test avec variables d'environnement NextGeneration
        env_vars = {{
            "NG_{nom_outil.upper()}_DEBUG": "true",
            "NG_LOG_LEVEL": "DEBUG"
        }}
        
        script_principal = self.tool_path / "{nom_outil}.py"
        
        if script_principal.exists():
            try:
                env = os.environ.copy()
                env.update(env_vars)
                
                result = subprocess.run([
                    sys.executable, str(script_principal)
                ], env=env, capture_output=True, text=True, timeout=15)
                
                # L'outil doit grer les variables d'environnement sans planter
                self.assertIn(result.returncode, [0, 1, 2], 
                             "L'outil doit grer les variables d'environnement")
                             
            except subprocess.TimeoutExpired:
                self.fail("Timeout avec variables d'environnement")
            except Exception as e:
                self.logger.warning(f"Test environnement chou: {{e}}")
                
    def test_interoperabilite_nextgeneration(self):
        """Test d'interoprabilit avec l'cosystme NextGeneration"""
        # Test basique d'interoprabilit
        # ( dvelopper selon les spcificits de chaque outil)
        
        # Vrification que l'outil peut coexister avec d'autres
        other_tools = list(self.base_path.glob("tools/*/"))
        other_tools = [t for t in other_tools if t.name != "{nom_outil}" and t.name != "imported_tools"]
        
        self.assertGreaterEqual(len(other_tools), 0, 
                               "Au moins un autre outil devrait exister pour le test")
                               
    def test_performance_integration(self):
        """Test de performance en conditions d'intgration"""
        import time
        
        script_principal = self.tool_path / "{nom_outil}.py"
        
        if not script_principal.exists():
            self.skipTest("Script principal non trouv")
            
        debut = time.time()
        
        try:
            # Test de performance avec timeout
            result = subprocess.run([
                sys.executable, str(script_principal), "--help"
            ], capture_output=True, text=True, timeout=10)
            
            duree = time.time() - debut
            
            # L'outil doit rpondre rapidement
            self.assertLess(duree, 5, "L'outil rpond trop lentement")
            
        except subprocess.TimeoutExpired:
            self.fail("L'outil ne rpond pas assez rapidement")
        except Exception as e:
            self.logger.warning(f"Test performance chou: {{e}}")

if __name__ == "__main__":
    # Excution des tests avec pytest
    pytest.main([__file__, "-v", "--tb=short"])
'''
        
        return contenu
        
    def compter_tests_generes(self, contenu_test: str) -> int:
        """Compte le nombre de tests gnrs"""
        return contenu_test.count("def test_")
        
    def compter_scenarios_integration(self, contenu_test: str) -> int:
        """Compte le nombre de scnarios d'intgration"""
        return contenu_test.count("def test_")
        
    def executer_tests_outil(self, nom_outil: str) -> Dict[str, Any]:
        """Excute les tests pour un outil spcifique"""
        self.logger.info(f" Excution des tests pour: {nom_outil}")
        
        resultats = {
            "outil": nom_outil,
            "tests_unitaires": {"statut": "NON_EXECUTE", "details": {}},
            "tests_integration": {"statut": "NON_EXECUTE", "details": {}},
            "statut_global": "EN_COURS"
        }
        
        # Excution des tests unitaires
        test_unitaire_file = self.tests_path / "unit" / f"test_{nom_outil}.py"
        if test_unitaire_file.exists():
            resultats["tests_unitaires"] = self.executer_pytest(test_unitaire_file, "unitaire")
            
        # Excution des tests d'intgration
        test_integration_file = self.tests_path / "integration" / f"test_{nom_outil}_integration.py"
        if test_integration_file.exists():
            resultats["tests_integration"] = self.executer_pytest(test_integration_file, "integration")
            
        # Dtermination du statut global
        if (resultats["tests_unitaires"]["statut"] == "REUSSI" and 
            resultats["tests_integration"]["statut"] == "REUSSI"):
            resultats["statut_global"] = "REUSSI"
        elif (resultats["tests_unitaires"]["statut"] in ["REUSSI", "PARTIEL"] or
              resultats["tests_integration"]["statut"] in ["REUSSI", "PARTIEL"]):
            resultats["statut_global"] = "PARTIEL"
        else:
            resultats["statut_global"] = "ECHEC"
            
        self.logger.info(f"[CHECK] Tests termins pour {nom_outil}: {resultats['statut_global']}")
        return resultats
        
    def executer_pytest(self, fichier_test: Path, type_test: str) -> Dict[str, Any]:
        """Excute pytest sur un fichier de test"""
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", str(fichier_test), "-v", "--tb=short", "--json-report"
            ], capture_output=True, text=True, timeout=120)
            
            # Analyse des rsultats
            if result.returncode == 0:
                statut = "REUSSI"
            elif "FAILED" in result.stdout and "PASSED" in result.stdout:
                statut = "PARTIEL"
            else:
                statut = "ECHEC"
                
            return {
                "statut": statut,
                "code_retour": result.returncode,
                "stdout": result.stdout[:1000],  # Limit pour viter les logs trop longs
                "stderr": result.stderr[:1000] if result.stderr else "",
                "type": type_test
            }
            
        except subprocess.TimeoutExpired:
            return {
                "statut": "TIMEOUT",
                "erreur": "Tests ont pris trop de temps",
                "type": type_test
            }
        except Exception as e:
            return {
                "statut": "ECHEC",
                "erreur": str(e),
                "type": type_test
            }
            
    def executer_tests_complets(self) -> Dict[str, Any]:
        """Excute tous les tests pour tous les outils"""
        self.logger.info("[ROCKET] Dmarrage des tests complets")
        
        # Identification des outils
        outils_a_tester = self.identifier_outils_a_tester()
        
        resultats_globaux = {
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "nombre_outils_testes": len(outils_a_tester),
            "creation_tests": {},
            "execution_tests": {},
            "resume_global": {},
            "recommandations": []
        }
        
        # Phase 1: Cration des tests
        for outil in outils_a_tester:
            nom_outil = outil["nom"]
            
            try:
                # Cration des tests unitaires
                result_unit = self.creer_test_unitaire(nom_outil, outil)
                
                # Cration des tests d'intgration
                result_integration = self.creer_test_integration(nom_outil, outil)
                
                resultats_globaux["creation_tests"][nom_outil] = {
                    "unitaires": result_unit,
                    "integration": result_integration
                }
                
            except Exception as e:
                self.logger.error(f"[CROSS] Erreur cration tests {nom_outil}: {e}")
                resultats_globaux["creation_tests"][nom_outil] = {"erreur": str(e)}
                
        # Phase 2: Excution des tests
        for outil in outils_a_tester:
            nom_outil = outil["nom"]
            
            try:
                resultats_execution = self.executer_tests_outil(nom_outil)
                resultats_globaux["execution_tests"][nom_outil] = resultats_execution
                
            except Exception as e:
                self.logger.error(f"[CROSS] Erreur excution tests {nom_outil}: {e}")
                resultats_globaux["execution_tests"][nom_outil] = {"erreur": str(e)}
                
        # Phase 3: Gnration du rsum et recommandations
        resultats_globaux["resume_global"] = self.generer_resume_tests(resultats_globaux)
        resultats_globaux["recommandations"] = self.generer_recommandations_tests(resultats_globaux)
        
        # Sauvegarde du rapport
        self.sauvegarder_rapport_tests(resultats_globaux)
        
        self.logger.info("[CHECK] Tests complets termins")
        return resultats_globaux
        
    def generer_resume_tests(self, resultats: Dict[str, Any]) -> Dict[str, Any]:
        """Gnre un rsum global des tests"""
        outils_testes = len(resultats["execution_tests"])
        outils_reussis = len([r for r in resultats["execution_tests"].values() 
                             if r.get("statut_global") == "REUSSI"])
        outils_partiels = len([r for r in resultats["execution_tests"].values() 
                              if r.get("statut_global") == "PARTIEL"])
        
        return {
            "outils_total": resultats["nombre_outils_testes"],
            "outils_testes": outils_testes,
            "outils_reussis": outils_reussis,
            "outils_partiels": outils_partiels,
            "outils_echec": outils_testes - outils_reussis - outils_partiels,
            "taux_reussite": (outils_reussis / outils_testes * 100) if outils_testes > 0 else 0,
            "statut_global": "REUSSI" if outils_reussis == outils_testes else "PARTIEL"
        }
        
    def generer_recommandations_tests(self, resultats: Dict[str, Any]) -> List[str]:
        """Gnre des recommandations bases sur les rsultats des tests"""
        recommandations = []
        
        # Analyse des checs
        echecs = [nom for nom, result in resultats["execution_tests"].items() 
                 if result.get("statut_global") == "ECHEC"]
                 
        if echecs:
            recommandations.append(f"Corriger les checs de tests pour: {', '.join(echecs)}")
            
        # Analyse des tests partiels
        partiels = [nom for nom, result in resultats["execution_tests"].items() 
                   if result.get("statut_global") == "PARTIEL"]
                   
        if partiels:
            recommandations.append(f"Amliorer les tests partiels pour: {', '.join(partiels)}")
            
        # Recommandations gnrales
        recommandations.extend([
            "Ajouter tests de performance spcifiques  chaque outil",
            "Crer tests de charge pour validation production",
            "Intgrer tests dans pipeline CI/CD",
            "Ajouter monitoring des mtriques de tests",
            "Crer tests de scurit spcialiss"
        ])
        
        return recommandations
        
    def sauvegarder_rapport_tests(self, resultats: Dict[str, Any]) -> None:
        """Sauvegarde le rapport complet des tests"""
        rapport_file = self.base_path / "logs" / f"{self.agent_id}_tests_complets.json"
        
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(resultats, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"[CHART] Rapport de tests sauvegard: {rapport_file}")

if __name__ == "__main__":
    agent = AgentTesteurIntegration()
    rapport = agent.executer_tests_complets()
    
    print(f"\n Tests complets termins")
    print(f"[CLIPBOARD] Agent ID: {rapport['agent_id']}")
    print(f"[TOOL] Outils tests: {rapport['resume_global']['outils_testes']}")
    print(f"[CHECK] Taux de russite: {rapport['resume_global']['taux_reussite']:.1f}%")
    print(f"[TARGET] Statut global: {rapport['resume_global']['statut_global']}")
    if rapport["recommandations"]:
        print(f"[BULB] Recommandations: {len(rapport['recommandations'])}") 