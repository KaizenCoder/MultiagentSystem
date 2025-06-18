#!/usr/bin/env python3
"""
Agent 4 - Testeur d'Intégration (GPT-4 Turbo)
Mission: Tester l'intégration des outils adaptés dans NextGeneration

Responsabilités:
- Tester la syntaxe des fichiers adaptés
- Vérifier les imports et dépendances
- Tester l'exécution basique des outils
- Valider la configuration NextGeneration
- Générer un rapport de tests détaillé
"""

import os
import sys
import ast
import json
import logging
import subprocess
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional

class AgentTesteurIntegration:
    """Agent spécialisé dans les tests d'intégration avec GPT-4 Turbo"""
    
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
        """Test complet des outils intégrés"""
        self.logger.info("🧪 Démarrage tests d'intégration")
        
        adapted_tools = adaptation_data.get("adapted_tools", [])
        if not adapted_tools:
            self.logger.warning("⚠️ Aucun outil à tester")
            return {"tested_tools": [], "test_summary": {}}
            
        tested_tools = []
        test_failures = []
        
        # Tester chaque outil adapté
        for tool in adapted_tools:
            try:
                test_results = self.test_single_tool(tool)
                tested_tools.append(test_results)
                
                if test_results["overall_status"] == "PASS":
                    self.logger.info(f"✅ Tests réussis: {tool['name']}")
                else:
                    self.logger.warning(f"⚠️ Tests partiels: {tool['name']}")
                    
            except Exception as e:
                error_msg = f"Erreur test {tool['name']}: {e}"
                self.logger.error(error_msg)
                test_failures.append(error_msg)
                
        # Tests globaux (configuration, structure)
        global_tests = self.run_global_tests()
        
        # Génération du rapport de tests
        test_summary = self.generate_test_summary(tested_tools, global_tests, test_failures)
        
        results = {
            "tested_tools": tested_tools,
            "global_tests": global_tests,
            "test_failures": test_failures,
            "test_summary": test_summary
        }
        
        self.logger.info(f"✅ Tests terminés: {len(tested_tools)} outils testés")
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
        
        # Test 3: Test d'exécution basique
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
                
            # Parse AST pour vérifier la syntaxe
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
                
            # Détermination du statut
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
        """Test d'exécution basique"""
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
                        test_result["details"].append(f"Exécution réussie avec argument: {arg}")
                        break
                        
                except subprocess.TimeoutExpired:
                    test_result["errors"].append(f"Timeout avec argument: {arg}")
                except Exception as e:
                    test_result["errors"].append(f"Erreur exécution avec {arg}: {e}")
                    
            # Test d'exécution sans arguments
            if not execution_successful:
                try:
                    result = subprocess.run(
                        [sys.executable, str(tool_path)],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    # Considérer comme succès si pas d'erreur fatale
                    if result.returncode in [0, 1, 2]:  # Codes de retour acceptables
                        execution_successful = True
                        test_result["details"].append("Exécution basique réussie")
                        
                except subprocess.TimeoutExpired:
                    test_result["errors"].append("Timeout exécution sans arguments")
                except Exception as e:
                    test_result["errors"].append(f"Erreur exécution: {e}")
                    
            # Détermination du score et statut
            if execution_successful:
                test_result["status"] = "PASS"
                test_result["score"] = 100
            else:
                test_result["status"] = "FAIL"
                test_result["score"] = 0
                
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["errors"].append(f"Erreur test exécution: {e}")
            
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
            
            # Vérifier la présence des éléments NextGeneration
            checks = [
                ("NextGeneration Tool", 20, "En-tête NextGeneration présent"),
                ("SCRIPT_DIR", 15, "Variable SCRIPT_DIR définie"),
                ("PROJECT_ROOT", 15, "Variable PROJECT_ROOT définie"),
                ("logging.getLogger", 15, "Logger NextGeneration configuré"),
                ("sys.path.insert", 10, "Python path configuré"),
                ("Auto-détection du projet", 15, "Auto-détection projet présente"),
                ("Configuration NextGeneration", 10, "Section configuration présente")
            ]
            
            for check_text, points, description in checks:
                if check_text in content:
                    score += points
                    test_result["details"].append(f"✅ {description}")
                else:
                    test_result["errors"].append(f"❌ {description} manquant")
                    
            test_result["score"] = min(score, max_score)
            
            # Détermination du statut
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
            
            # Vérifier l'existence du fichier
            if tool_path.exists():
                score += 30
                test_result["details"].append("Fichier outil existe")
            else:
                test_result["errors"].append("Fichier outil introuvable")
                
            # Vérifier la taille du fichier
            if tool_path.exists():
                file_size = tool_path.stat().st_size
                if file_size > 0:
                    score += 20
                    test_result["details"].append(f"Taille fichier: {file_size} bytes")
                else:
                    test_result["errors"].append("Fichier vide")
                    
            # Vérifier les permissions
            if tool_path.exists():
                if os.access(tool_path, os.R_OK):
                    score += 20
                    test_result["details"].append("Permissions lecture OK")
                else:
                    test_result["errors"].append("Permissions lecture manquantes")
                    
            # Vérifier la structure du répertoire parent
            parent_dir = tool_path.parent
            if (parent_dir / "__init__.py").exists():
                score += 15
                test_result["details"].append("Répertoire catégorie correctement structuré")
            else:
                test_result["errors"].append("__init__.py manquant dans catégorie")
                
            # Vérifier l'encodage
            if tool_path.exists():
                try:
                    with open(tool_path, 'r', encoding='utf-8') as f:
                        f.read()
                    score += 15
                    test_result["details"].append("Encodage UTF-8 valide")
                except UnicodeDecodeError:
                    test_result["errors"].append("Problème encodage fichier")
                    
            test_result["score"] = score
            
            # Détermination du statut
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
        """Tests globaux de l'intégration"""
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
            
            # Vérifier tools_config.json
            config_file = self.target_path / "tools_config.json"
            if config_file.exists():
                score += 50
                test_result["details"].append("Fichier tools_config.json présent")
                
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
                
            # Vérifier run_tool.py
            launcher_file = self.target_path / "run_tool.py"
            if launcher_file.exists():
                score += 25
                test_result["details"].append("Script lanceur présent")
            else:
                test_result["errors"].append("Script lanceur manquant")
                
            test_result["score"] = score
            test_result["status"] = "PASS" if score >= 75 else ("PARTIAL" if score >= 50 else "FAIL")
            
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["errors"].append(f"Erreur test configuration globale: {e}")
            
        return test_result
        
    def test_directory_structure(self) -> Dict[str, Any]:
        """Test de la structure des répertoires"""
        test_result = {
            "name": "Directory Structure",
            "status": "UNKNOWN",
            "score": 0,
            "details": [],
            "errors": []
        }
        
        try:
            score = 0
            
            # Vérifier l'existence du répertoire principal
            if self.target_path.exists():
                score += 30
                test_result["details"].append("Répertoire principal existe")
            else:
                test_result["errors"].append("Répertoire principal manquant")
                return test_result
                
            # Compter les catégories créées
            categories = [d for d in self.target_path.iterdir() if d.is_dir()]
            if categories:
                score += 40
                test_result["details"].append(f"{len(categories)} catégories créées")
                
                # Vérifier les __init__.py
                init_count = 0
                for cat_dir in categories:
                    if (cat_dir / "__init__.py").exists():
                        init_count += 1
                        
                if init_count == len(categories):
                    score += 30
                    test_result["details"].append("Tous les __init__.py présents")
                else:
                    test_result["errors"].append(f"{len(categories) - init_count} __init__.py manquants")
            else:
                test_result["errors"].append("Aucune catégorie créée")
                
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
                test_result["details"].append("Fichier requirements.txt présent")
                
                # Compter les dépendances
                with open(req_file, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    
                test_result["details"].append(f"{len(lines)} dépendances listées")
            else:
                test_result["score"] = 50  # Pas critique si pas de dépendances
                test_result["status"] = "PARTIAL"
                test_result["details"].append("Aucune dépendance externe détectée")
                
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["errors"].append(f"Erreur test requirements: {e}")
            
        return test_result
        
    def calculate_overall_score(self, tests: Dict[str, Any]) -> int:
        """Calcul du score global pondéré"""
        total_score = 0
        
        for test_name, test_result in tests.items():
            if test_name in self.test_categories:
                weight = self.test_categories[test_name]["weight"]
                score = test_result.get("score", 0)
                total_score += score * weight
                
        return int(total_score)
        
    def determine_overall_status(self, tests: Dict[str, Any]) -> str:
        """Détermination du statut global"""
        critical_failures = []
        
        for test_name, test_result in tests.items():
            if test_name in self.test_categories:
                is_critical = self.test_categories[test_name]["critical"]
                status = test_result.get("status", "UNKNOWN")
                
                if is_critical and status == "FAIL":
                    critical_failures.append(test_name)
                    
        if critical_failures:
            return "FAIL"
            
        # Compter les succès
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
        """Génération du résumé des tests"""
        
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

# Test de l'agent si exécuté directement
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        target_path = "tools/imported_tools"
        
    # Test avec des données simulées
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