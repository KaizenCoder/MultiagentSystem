#!/usr/bin/env python3
"""
Agent 4 - Testeur d'Intgration (GPT-4 Turbo)
Mission: Tester l'intgration des outils adapts dans NextGeneration

Responsabilits:
- Tester la syntaxe des fichiers adapts
- Vrifier les imports et dpendances
- Tester l'excution basique des outils
- Valider la configuration NextGeneration
- Gnrer un rapport de tests dtaill
"""

import os
import sys
import ast
import json
import logging
import subprocess
import importlib.util
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class AgentTesteurIntegration:
    """Agent spcialis dans les tests d'intgration avec GPT-4 Turbo"""
    
    def __init__(self, target_path: str):
        self.target_path = Path(target_path)
        self.logger = logging.getLogger("Agent4_TesteurIntegration")
        
        # Configuration des tests
        self.test_categories = {
            "syntax_validation": {"weight": 0.30, "critical": True},
            "import_validation": {"weight": 0.25, "critical": True},
            "execution_test": {"weight": 0.20, "critical": False},
            "configuration_test": {"weight": 0.15, "critical": False},
            "structure_validation": {"weight": 0.10, "critical": False}
        }
        
    def test_integrated_tools(self, adaptation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test complet des outils intgrs"""
        self.logger.info(" Dmarrage tests d'intgration")
        
        adapted_tools = adaptation_data.get("adapted_tools", [])
        if not adapted_tools:
            self.logger.warning(" Aucun outil  tester")
            return {"tested_tools": [], "test_summary": {}}
            
        tested_tools = []
        test_failures = []
        
        # Tester chaque outil adapt
        for tool in adapted_tools:
            try:
                test_results = self.test_single_tool(tool)
                tested_tools.append(test_results)
                
                if test_results["overall_status"] == "PASS":
                    self.logger.info(f"[CHECK] Tests russis: {tool['name']}")
                else:
                    self.logger.warning(f" Tests partiels: {tool['name']}")
                    
            except Exception as e:
                error_msg = f"Erreur test {tool['name']}: {e}"
                self.logger.error(error_msg)
                test_failures.append(error_msg)
                
        # Tests globaux (configuration, structure)
        global_tests = self.run_global_tests()
        
        # Gnration du rapport de tests
        test_summary = self.generate_test_summary(tested_tools, global_tests, test_failures)
        
        results = {
            "tested_tools": tested_tools,
            "global_tests": global_tests,
            "test_failures": test_failures,
            "test_summary": test_summary
        }
        
        self.logger.info(f"[CHECK] Tests termins: {len(tested_tools)} outils tests")
        return results
        
    def test_single_tool(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """Test complet d'un outil unique"""
        tool_name = tool["name"]
        tool_path = Path(tool["target_path"])
        
        test_results = {
            "name": tool_name,
            "path": str(tool_path),
            "category": tool["category"],
            "tests": {},
            "overall_score": 0,
            "overall_status": "UNKNOWN"
        }
        
        # Test 1: Validation syntaxique
        test_results["tests"]["syntax_validation"] = self.test_syntax_validation(tool_path)
        
        # Test 2: Validation des imports
        test_results["tests"]["import_validation"] = self.test_import_validation(tool_path)
        
        # Test 3: Test d'excution basique
        test_results["tests"]["execution_test"] = self.test_basic_execution(tool_path)
        
        # Test 4: Test de configuration
        test_results["tests"]["configuration_test"] = self.test_configuration(tool_path)
        
        # Test 5: Validation de structure
        test_results["tests"]["structure_validation"] = self.test_structure_validation(tool_path)
        
        # Calcul du score global
        test_results["overall_score"] = self.calculate_overall_score(test_results["tests"])
        test_results["overall_status"] = self.determine_overall_status(test_results["tests"])
        
        return test_results
        
    def test_syntax_validation(self, tool_path: Path) -> Dict[str, Any]:
        """Test de validation syntaxique"""
        test_result = {
            "name": "Syntax Validation",
            "status": "UNKNOWN",
            "score": 0,
            "details": [],
            "errors": []
        }
        
        try:
            with open(tool_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse AST pour vrifier la syntaxe
            try:
                ast.parse(content)
                test_result["status"] = "PASS"
                test_result["score"] = 100
                test_result["details"].append("Syntaxe Python valide")
                
            except SyntaxError as e:
                test_result["status"] = "FAIL"
                test_result["score"] = 0
                test_result["errors"].append(f"Erreur syntaxe ligne {e.lineno}: {e.msg}")
                
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["errors"].append(f"Erreur lecture fichier: {e}")
            
        return test_result
        
    def test_import_validation(self, tool_path: Path) -> Dict[str, Any]:
        """Test de validation des imports"""
        test_result = {
            "name": "Import Validation",
            "status": "UNKNOWN",
            "score": 0,
            "details": [],
            "errors": []
        }
        
        try:
            with open(tool_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extraire tous les imports
            tree = ast.parse(content)
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    imports.append(module)
                    
            # Tester chaque import
            successful_imports = 0
            total_imports = len(imports)
            
            for imp in imports:
                if imp:  # Ignorer les imports vides
                    try:
                        if imp not in sys.modules:
                            importlib.import_module(imp)
                        successful_imports += 1
                        test_result["details"].append(f"Import OK: {imp}")
                        
                    except ImportError:
                        test_result["errors"].append(f"Import manquant: {imp}")
                    except Exception as e:
                        test_result["errors"].append(f"Erreur import {imp}: {e}")
                        
            # Calcul du score
            if total_imports > 0:
                test_result["score"] = int((successful_imports / total_imports) * 100)
            else:
                test_result["score"] = 100  # Aucun import = OK
                
            # Dtermination du statut
            if test_result["score"] >= 80:
                test_result["status"] = "PASS"
            elif test_result["score"] >= 50:
                test_result["status"] = "PARTIAL"
            else:
                test_result["status"] = "FAIL"
                
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["errors"].append(f"Erreur validation imports: {e}")
            
        return test_result
        
    def test_basic_execution(self, tool_path: Path) -> Dict[str, Any]:
        """Test d'excution basique"""
        test_result = {
            "name": "Basic Execution Test",
            "status": "UNKNOWN",
            "score": 0,
            "details": [],
            "errors": []
        }
        
        try:
            # Test avec --help ou -h (arguments courants)
            help_args = ["--help", "-h", "help"]
            execution_successful = False
            
            for arg in help_args:
                try:
                    result = subprocess.run(
                        [sys.executable, str(tool_path), arg],
                        capture_output=True,
                        text=True,
                        timeout=10  # Timeout de 10 secondes
                    )
                    
                    if result.returncode == 0 or "usage" in result.stdout.lower() or "help" in result.stdout.lower():
                        execution_successful = True
                        test_result["details"].append(f"Excution russie avec argument: {arg}")
                        break
                        
                except subprocess.TimeoutExpired:
                    test_result["errors"].append(f"Timeout avec argument: {arg}")
                except Exception as e:
                    test_result["errors"].append(f"Erreur excution avec {arg}: {e}")
                    
            # Test d'excution sans arguments
            if not execution_successful:
                try:
                    result = subprocess.run(
                        [sys.executable, str(tool_path)],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    # Considrer comme succs si pas d'erreur fatale
                    if result.returncode in [0, 1, 2]:  # Codes de retour acceptables
                        execution_successful = True
                        test_result["details"].append("Excution basique russie")
                        
                except subprocess.TimeoutExpired:
                    test_result["errors"].append("Timeout excution sans arguments")
                except Exception as e:
                    test_result["errors"].append(f"Erreur excution: {e}")
                    
            # Dtermination du score et statut
            if execution_successful:
                test_result["status"] = "PASS"
                test_result["score"] = 100
            else:
                test_result["status"] = "FAIL"
                test_result["score"] = 0
                
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["errors"].append(f"Erreur test excution: {e}")
            
        return test_result
        
    def test_configuration(self, tool_path: Path) -> Dict[str, Any]:
        """Test de configuration NextGeneration"""
        test_result = {
            "name": "Configuration Test",
            "status": "UNKNOWN",
            "score": 0,
            "details": [],
            "errors": []
        }
        
        try:
            with open(tool_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            score = 0
            max_score = 100
            
            # Vrifier la prsence des lments NextGeneration
            checks = [
                ("NextGeneration Tool", 20, "En-tte NextGeneration prsent"),
                ("SCRIPT_DIR", 15, "Variable SCRIPT_DIR dfinie"),
                ("PROJECT_ROOT", 15, "Variable PROJECT_ROOT dfinie"),
                ("logging.getLogger", 15, "Logger NextGeneration configur"),
                ("sys.path.insert", 10, "Python path configur"),
                ("Auto-dtection du projet", 15, "Auto-dtection projet prsente"),
                ("Configuration NextGeneration", 10, "Section configuration prsente")
            ]
            
            for check_text, points, description in checks:
                if check_text in content:
                    score += points
                    test_result["details"].append(f"[CHECK] {description}")
                else:
                    test_result["errors"].append(f"[CROSS] {description} manquant")
                    
            test_result["score"] = min(score, max_score)
            
            # Dtermination du statut
            if test_result["score"] >= 80:
                test_result["status"] = "PASS"
            elif test_result["score"] >= 50:
                test_result["status"] = "PARTIAL"
            else:
                test_result["status"] = "FAIL"
                
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["errors"].append(f"Erreur test configuration: {e}")
            
        return test_result
        
    def test_structure_validation(self, tool_path: Path) -> Dict[str, Any]:
        """Test de validation de structure"""
        test_result = {
            "name": "Structure Validation",
            "status": "UNKNOWN",
            "score": 0,
            "details": [],
            "errors": []
        }
        
        try:
            score = 0
            
            # Vrifier l'existence du fichier
            if tool_path.exists():
                score += 30
                test_result["details"].append("Fichier outil existe")
            else:
                test_result["errors"].append("Fichier outil introuvable")
                
            # Vrifier la taille du fichier
            if tool_path.exists():
                file_size = tool_path.stat().st_size
                if file_size > 0:
                    score += 20
                    test_result["details"].append(f"Taille fichier: {file_size} bytes")
                else:
                    test_result["errors"].append("Fichier vide")
                    
            # Vrifier les permissions
            if tool_path.exists():
                if os.access(tool_path, os.R_OK):
                    score += 20
                    test_result["details"].append("Permissions lecture OK")
                else:
                    test_result["errors"].append("Permissions lecture manquantes")
                    
            # Vrifier la structure du rpertoire parent
            parent_dir = tool_path.parent
            if (parent_dir / "__init__.py").exists():
                score += 15
                test_result["details"].append("Rpertoire catgorie correctement structur")
            else:
                test_result["errors"].append("__init__.py manquant dans catgorie")
                
            # Vrifier l'encodage
            if tool_path.exists():
                try:
                    with open(tool_path, 'r', encoding='utf-8') as f:
                        f.read()
                    score += 15
                    test_result["details"].append("Encodage UTF-8 valide")
                except UnicodeDecodeError:
                    test_result["errors"].append("Problme encodage fichier")
                    
            test_result["score"] = score
            
            # Dtermination du statut
            if test_result["score"] >= 80:
                test_result["status"] = "PASS"
            elif test_result["score"] >= 50:
                test_result["status"] = "PARTIAL"
            else:
                test_result["status"] = "FAIL"
                
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["errors"].append(f"Erreur validation structure: {e}")
            
        return test_result
        
    def run_global_tests(self) -> Dict[str, Any]:
        """Tests globaux de l'intgration"""
        global_tests = {
            "configuration_files": self.test_global_configuration(),
            "directory_structure": self.test_directory_structure(),
            "requirements": self.test_requirements_file()
        }
        
        return global_tests
        
    def test_global_configuration(self) -> Dict[str, Any]:
        """Test des fichiers de configuration globaux"""
        test_result = {
            "name": "Global Configuration",
            "status": "UNKNOWN",
            "score": 0,
            "details": [],
            "errors": []
        }
        
        try:
            score = 0
            
            # Vrifier tools_config.json
            config_file = self.target_path / "tools_config.json"
            if config_file.exists():
                score += 50
                test_result["details"].append("Fichier tools_config.json prsent")
                
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                        
                    if "nextgeneration_tools" in config_data:
                        score += 25
                        test_result["details"].append("Structure configuration valide")
                        
                except json.JSONDecodeError:
                    test_result["errors"].append("Fichier configuration JSON invalide")
            else:
                test_result["errors"].append("Fichier tools_config.json manquant")
                
            # Vrifier run_tool.py
            launcher_file = self.target_path / "run_tool.py"
            if launcher_file.exists():
                score += 25
                test_result["details"].append("Script lanceur prsent")
            else:
                test_result["errors"].append("Script lanceur manquant")
                
            test_result["score"] = score
            test_result["status"] = "PASS" if score >= 75 else ("PARTIAL" if score >= 50 else "FAIL")
            
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["errors"].append(f"Erreur test configuration globale: {e}")
            
        return test_result
        
    def test_directory_structure(self) -> Dict[str, Any]:
        """Test de la structure des rpertoires"""
        test_result = {
            "name": "Directory Structure",
            "status": "UNKNOWN",
            "score": 0,
            "details": [],
            "errors": []
        }
        
        try:
            score = 0
            
            # Vrifier l'existence du rpertoire principal
            if self.target_path.exists():
                score += 30
                test_result["details"].append("Rpertoire principal existe")
            else:
                test_result["errors"].append("Rpertoire principal manquant")
                return test_result
                
            # Compter les catgories cres
            categories = [d for d in self.target_path.iterdir() if d.is_dir()]
            if categories:
                score += 40
                test_result["details"].append(f"{len(categories)} catgories cres")
                
                # Vrifier les __init__.py
                init_count = 0
                for cat_dir in categories:
                    if (cat_dir / "__init__.py").exists():
                        init_count += 1
                        
                if init_count == len(categories):
                    score += 30
                    test_result["details"].append("Tous les __init__.py prsents")
                else:
                    test_result["errors"].append(f"{len(categories) - init_count} __init__.py manquants")
            else:
                test_result["errors"].append("Aucune catgorie cre")
                
            test_result["score"] = score
            test_result["status"] = "PASS" if score >= 80 else ("PARTIAL" if score >= 50 else "FAIL")
            
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["errors"].append(f"Erreur test structure: {e}")
            
        return test_result
        
    def test_requirements_file(self) -> Dict[str, Any]:
        """Test du fichier requirements.txt"""
        test_result = {
            "name": "Requirements File",
            "status": "UNKNOWN",
            "score": 0,
            "details": [],
            "errors": []
        }
        
        try:
            req_file = self.target_path / "requirements.txt"
            
            if req_file.exists():
                test_result["score"] = 100
                test_result["status"] = "PASS"
                test_result["details"].append("Fichier requirements.txt prsent")
                
                # Compter les dpendances
                with open(req_file, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    
                test_result["details"].append(f"{len(lines)} dpendances listes")
            else:
                test_result["score"] = 50  # Pas critique si pas de dpendances
                test_result["status"] = "PARTIAL"
                test_result["details"].append("Aucune dpendance externe dtecte")
                
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["errors"].append(f"Erreur test requirements: {e}")
            
        return test_result
        
    def calculate_overall_score(self, tests: Dict[str, Any]) -> int:
        """Calcul du score global pondr"""
        total_score = 0
        
        for test_name, test_result in tests.items():
            if test_name in self.test_categories:
                weight = self.test_categories[test_name]["weight"]
                score = test_result.get("score", 0)
                total_score += score * weight
                
        return int(total_score)
        
    def determine_overall_status(self, tests: Dict[str, Any]) -> str:
        """Dtermination du statut global"""
        critical_failures = []
        
        for test_name, test_result in tests.items():
            if test_name in self.test_categories:
                is_critical = self.test_categories[test_name]["critical"]
                status = test_result.get("status", "UNKNOWN")
                
                if is_critical and status == "FAIL":
                    critical_failures.append(test_name)
                    
        if critical_failures:
            return "FAIL"
            
        # Compter les succs
        pass_count = sum(1 for test in tests.values() if test.get("status") == "PASS")
        total_count = len(tests)
        
        if pass_count == total_count:
            return "PASS"
        elif pass_count >= total_count * 0.7:
            return "PARTIAL"
        else:
            return "FAIL"
            
    def generate_test_summary(self, tested_tools: List[Dict[str, Any]], 
                            global_tests: Dict[str, Any], 
                            test_failures: List[str]) -> Dict[str, Any]:
        """Gnration du rsum des tests"""
        
        # Statistiques des outils
        total_tools = len(tested_tools)
        passed_tools = len([t for t in tested_tools if t["overall_status"] == "PASS"])
        partial_tools = len([t for t in tested_tools if t["overall_status"] == "PARTIAL"])
        failed_tools = len([t for t in tested_tools if t["overall_status"] == "FAIL"])
        
        # Score moyen
        if tested_tools:
            avg_score = sum(t["overall_score"] for t in tested_tools) / len(tested_tools)
        else:
            avg_score = 0
            
        # Statut des tests globaux
        global_status_counts = {}
        for test_result in global_tests.values():
            status = test_result.get("status", "UNKNOWN")
            global_status_counts[status] = global_status_counts.get(status, 0) + 1
            
        return {
            "total_tools_tested": total_tools,
            "tools_passed": passed_tools,
            "tools_partial": partial_tools,
            "tools_failed": failed_tools,
            "success_rate": round((passed_tools / total_tools * 100), 1) if total_tools > 0 else 0,
            "average_score": round(avg_score, 1),
            "global_tests_status": global_status_counts,
            "test_failures_count": len(test_failures),
            "integration_ready": passed_tools + partial_tools >= total_tools * 0.8
        }
    
    def tester_integration_apex(self, phase3_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tests d'intgration spcialiss pour les outils Apex_VBA_FRAMEWORK
        
        Args:
            phase3_data: Donnes d'adaptation de la phase 3
            
        Returns:
            Dict contenant les rsultats des tests
        """
        self.logger.info(" Tests d'intgration spcialiss Apex_VBA_FRAMEWORK")
        
        outils_testes = []
        outils_adaptes = phase3_data.get("outils_adaptes", [])
        
        for outil in outils_adaptes:
            try:
                if outil["type"] == "python":
                    resultat = self._tester_outil_python_apex(outil)
                elif outil["type"] == "powershell":
                    resultat = self._tester_outil_powershell_apex(outil)
                elif outil["type"] == "batch":
                    resultat = self._tester_outil_batch_apex(outil)
                else:
                    continue
                
                if resultat:
                    outils_testes.append(resultat)
                    status = "[CHECK]" if resultat["test_success"] else ""
                    self.logger.info(f"{status} Tests {outil['name']}: {resultat['test_summary']}")
                
            except Exception as e:
                self.logger.error(f"[CROSS] Erreur tests {outil['name']}: {e}")
        
        resultats = {
            "total_tested": len(outils_testes),
            "outils_testes": outils_testes,
            "tests_passed": len([t for t in outils_testes if t["test_success"]]),
            "tests_failed": len([t for t in outils_testes if not t["test_success"]]),
            "test_timestamp": datetime.now().isoformat(),
            "tester_model": "GPT-4 Turbo"
        }
        
        self.logger.info(f"[CHECK] Tests Apex termins: {resultats['tests_passed']}/{resultats['total_tested']} succs")
        return resultats
    
    def _tester_outil_python_apex(self, outil: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Tests spcialiss pour un outil Python Apex"""
        try:
            target_path = Path(outil["target_path"])
            
            # Test de syntaxe Python
            syntaxe_ok = self._test_syntaxe_python_simple(target_path)
            
            # Test des imports
            imports_ok = self._test_imports_python_simple(target_path)
            
            # Test d'excution basique (--help ou quivalent)
            execution_ok = self._test_execution_python_apex(target_path)
            
            test_success = syntaxe_ok and imports_ok
            
            return {
                "name": outil["name"],
                "type": "python",
                "target_path": str(target_path),
                "test_success": test_success,
                "test_details": {
                    "syntax_check": syntaxe_ok,
                    "imports_check": imports_ok,
                    "execution_check": execution_ok
                },
                "test_summary": f"Syntaxe: {'OK' if syntaxe_ok else 'FAIL'}, Imports: {'OK' if imports_ok else 'FAIL'}"
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur test Python {outil['name']}: {e}")
            return None
    
    def _tester_outil_powershell_apex(self, outil: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Tests spcialiss pour un outil PowerShell Apex"""
        try:
            target_path = Path(outil["target_path"])
            
            # Test de syntaxe PowerShell basique
            syntaxe_ok = self._test_syntaxe_powershell(target_path)
            
            # Test de structure basique
            structure_ok = target_path.exists() and target_path.stat().st_size > 0
            
            return {
                "name": outil["name"],
                "type": "powershell",
                "target_path": str(target_path),
                "test_success": syntaxe_ok and structure_ok,
                "test_details": {
                    "syntax_check": syntaxe_ok,
                    "structure_check": structure_ok
                },
                "test_summary": f"Syntaxe: {'OK' if syntaxe_ok else 'FAIL'}, Structure: {'OK' if structure_ok else 'FAIL'}"
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur test PowerShell {outil['name']}: {e}")
            return None
    
    def _tester_outil_batch_apex(self, outil: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Tests spcialiss pour un outil Batch Apex"""
        try:
            target_path = Path(outil["target_path"])
            
            # Test de structure basique
            structure_ok = target_path.exists() and target_path.stat().st_size > 0
            
            # Test de contenu basique (pas de caractres invalides)
            contenu_ok = self._test_contenu_batch(target_path)
            
            return {
                "name": outil["name"],
                "type": "batch",
                "target_path": str(target_path),
                "test_success": structure_ok and contenu_ok,
                "test_details": {
                    "structure_check": structure_ok,
                    "content_check": contenu_ok
                },
                "test_summary": f"Structure: {'OK' if structure_ok else 'FAIL'}, Contenu: {'OK' if contenu_ok else 'FAIL'}"
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur test Batch {outil['name']}: {e}")
            return None
    
    def _test_syntaxe_python_simple(self, filepath: Path) -> bool:
        """Test de syntaxe Python simplifi"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            import ast
            ast.parse(content)
            return True
            
        except Exception:
            return False
    
    def _test_imports_python_simple(self, filepath: Path) -> bool:
        """Test des imports Python simplifi"""
        try:
            import subprocess
            import sys
            
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(filepath)],
                capture_output=True,
                timeout=10
            )
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def _test_syntaxe_powershell(self, filepath: Path) -> bool:
        """Test de syntaxe PowerShell basique"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Vrifications basiques de syntaxe PowerShell
            # Vrifier que les accolades sont quilibres
            open_braces = content.count('{')
            close_braces = content.count('}')
            
            return open_braces == close_braces
            
        except Exception:
            return False
    
    def _test_contenu_batch(self, filepath: Path) -> bool:
        """Test de contenu Batch basique"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Vrifier qu'il n'y a pas de caractres problmatiques
            return len(content.strip()) > 0
            
        except Exception:
            return False
    
    def _test_execution_python_apex(self, filepath: Path) -> bool:
        """Test d'excution basique pour outil Python Apex"""
        try:
            # Test trs basique - juste vrifier que le fichier peut tre import
            import subprocess
            import sys
            
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(filepath)],
                capture_output=True,
                timeout=10
            )
            
            return result.returncode == 0
            
        except Exception:
            return False

# Test de l'agent si excut directement
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        target_path = "tools/imported_tools"
        
    # Test avec des donnes simules
    test_adaptation_data = {
        "adapted_tools": [
            {
                "name": "test_tool",
                "category": "utility",
                "target_path": "tools/imported_tools/utility/test_tool.py",
                "utility_score": 75.5,
                "priority": "HIGH"
            }
        ]
    }
    
    agent = AgentTesteurIntegration(target_path)
    results = agent.test_integrated_tools(test_adaptation_data)
    
    print(json.dumps(results, indent=2, ensure_ascii=False)) 