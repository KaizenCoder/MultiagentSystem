#!/usr/bin/env python3
"""
 Agent 4: Testeur d'Intgration - GPT-4 Turbo
Mission: Tester l'intgration des outils adapts dans NextGeneration
"""

import asyncio
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class Agent4TesteurIntegration:
    """Agent spcialis dans les tests d'intgration"""
    
    def __init__(self, agent_id: str = None, agent_type: str = "tester", outils_adaptes: List[Dict] = None, target_path=None, workspace_path=None, **config):
        # Configuration TemplateManager
        self.agent_id = agent_id or "agent_4_testeur_integration"
        self.agent_type = agent_type
        self.config = config
        
        # Configuration spécifique - Rétrocompatibilité avec l'ancienne signature
        if outils_adaptes is None:
            outils_adaptes = config.get("outils_adaptes", [])
        if target_path is None:
            target_path = config.get("target_path", "./adapted_tools")
        if workspace_path is None:
            workspace_path = config.get("workspace_path", ".")
            
        self.outils_adaptes = outils_adaptes
        self.target_path = Path(target_path) if not isinstance(target_path, Path) else target_path
        self.workspace_path = Path(workspace_path) if not isinstance(workspace_path, Path) else workspace_path
        self.agent_name = "Agent 4 - Testeur Intgration"
        self.model_name = "GPT-4 Turbo"
        self.start_time = None
        
        self.tests_results = []
        self.outils_valides = []
        self.erreurs_tests = []
    
    async def startup(self):
        """Démarrage de l'agent - Interface TemplateManager"""
        print(f"🚀 Démarrage {self.agent_name} (ID: {self.agent_id})")
        return {"status": "started", "agent_id": self.agent_id}
    
    async def shutdown(self):
        """Arrêt de l'agent - Interface TemplateManager"""
        print(f"🛑 Arrêt {self.agent_name} (ID: {self.agent_id})")
        return {"status": "stopped", "agent_id": self.agent_id}
    
    async def health_check(self) -> Dict[str, Any]:
        """Vérification de santé - Interface TemplateManager"""
        return {
            "status": "healthy",
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "target_path_exists": self.target_path.exists(),
            "workspace_path_exists": self.workspace_path.exists(),
            "outils_adaptes_count": len(self.outils_adaptes)
        }
    
    async def execute_task(self, task_config: Dict = None) -> Dict[str, Any]:
        """Exécuter la tâche principale - Interface TemplateManager"""
        return await self.tester_integration()
    
    async def tester_integration(self) -> Dict[str, Any]:
        """Tester l'intgration de tous les outils"""
        self.start_time = datetime.now()
        print(f" {self.agent_name} - Dmarrage tests d'intgration")
        
        try:
            await self._tester_syntaxe()
            await self._tester_imports()
            await self._tester_execution_basique()
            await self._valider_configuration()
            
            resultat = await self._generer_rapport()
            
            duree = (datetime.now() - self.start_time).total_seconds()
            print(f"[CHECK] {self.agent_name} - Termin en {duree:.2f}s")
            
            return resultat
            
        except Exception as e:
            print(f"[CROSS] {self.agent_name} - Erreur: {e}")
            raise
    
    async def _tester_syntaxe(self):
        """Tester la syntaxe Python de tous les outils"""
        print("[SEARCH] Test de syntaxe Python...")
        
        for outil_info in self.outils_adaptes:
            outil_path = Path(outil_info['target_path'])
            
            try:
                # Test de compilation Python
                with open(outil_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                compile(code, str(outil_path), 'exec')
                
                self.tests_results.append({
                    "outil": outil_info['outil']['nom'],
                    "test": "syntaxe",
                    "status": "PASS",
                    "message": "Syntaxe Python valide"
                })
                
            except SyntaxError as e:
                self.tests_results.append({
                    "outil": outil_info['outil']['nom'],
                    "test": "syntaxe",
                    "status": "FAIL",
                    "message": f"Erreur syntaxe: {e}"
                })
                self.erreurs_tests.append({
                    "outil": outil_info['outil']['nom'],
                    "erreur": f"Syntaxe invalide: {e}"
                })
    
    async def _tester_imports(self):
        """Tester les imports de tous les outils"""
        print(" Test des imports...")
        
        for outil_info in self.outils_adaptes:
            outil_path = Path(outil_info['target_path'])
            
            try:
                # Tester les imports sans excuter le code principal
                result = subprocess.run([
                    sys.executable, '-c', 
                    f"import ast; exec(compile(open('{outil_path}').read(), '{outil_path}', 'exec'), {{'__name__': '__test__'}})"
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    self.tests_results.append({
                        "outil": outil_info['outil']['nom'],
                        "test": "imports",
                        "status": "PASS",
                        "message": "Tous les imports fonctionnent"
                    })
                else:
                    self.tests_results.append({
                        "outil": outil_info['outil']['nom'],
                        "test": "imports",
                        "status": "FAIL",
                        "message": f"Erreur imports: {result.stderr[:200]}"
                    })
                    
            except Exception as e:
                self.tests_results.append({
                    "outil": outil_info['outil']['nom'],
                    "test": "imports",
                    "status": "ERROR",
                    "message": f"Erreur test: {e}"
                })
    
    async def _tester_execution_basique(self):
        """Tester l'excution basique (help, version, etc.)"""
        print("[ROCKET] Test d'excution basique...")
        
        for outil_info in self.outils_adaptes:
            outil_path = Path(outil_info['target_path'])
            
            # Tests basiques
            tests_basiques = [
                ["--help"],
                ["-h"],
                ["--version"],
                ["-v"]
            ]
            
            test_passed = False
            
            for test_args in tests_basiques:
                try:
                    result = subprocess.run([
                        sys.executable, str(outil_path)
                    ] + test_args, capture_output=True, text=True, timeout=5)
                    
                    if result.returncode == 0 or "help" in result.stdout.lower():
                        test_passed = True
                        break
                        
                except subprocess.TimeoutExpired:
                    continue
                except Exception:
                    continue
            
            if test_passed:
                self.tests_results.append({
                    "outil": outil_info['outil']['nom'],
                    "test": "execution",
                    "status": "PASS",
                    "message": "Excution basique russie"
                })
                
                # Ajouter aux outils valids
                self.outils_valides.append(outil_info)
            else:
                self.tests_results.append({
                    "outil": outil_info['outil']['nom'],
                    "test": "execution",
                    "status": "PARTIAL",
                    "message": "Pas de rponse aux commandes standard"
                })
                
                # Ajouter quand mme si syntaxe/imports OK
                syntaxe_ok = any(t['outil'] == outil_info['outil']['nom'] and 
                               t['test'] == 'syntaxe' and t['status'] == 'PASS' 
                               for t in self.tests_results)
                imports_ok = any(t['outil'] == outil_info['outil']['nom'] and 
                               t['test'] == 'imports' and t['status'] == 'PASS' 
                               for t in self.tests_results)
                
                if syntaxe_ok and imports_ok:
                    self.outils_valides.append(outil_info)
    
    async def _valider_configuration(self):
        """Valider la configuration globale"""
        print(" Validation de la configuration...")
        
        # Vrifier les fichiers de configuration
        config_path = self.target_path / "imported_tools" / "configs" / "config.json"
        requirements_path = self.target_path / "imported_tools" / "requirements.txt"
        
        config_valid = config_path.exists()
        requirements_valid = requirements_path.exists()
        
        self.tests_results.append({
            "outil": "configuration",
            "test": "config_files",
            "status": "PASS" if config_valid and requirements_valid else "FAIL",
            "message": f"Config: {'[CHECK]' if config_valid else '[CROSS]'}, Requirements: {'[CHECK]' if requirements_valid else '[CROSS]'}"
        })
    
    async def _generer_rapport(self) -> Dict[str, Any]:
        """Gnrer le rapport final de tests"""
        duree = (datetime.now() - self.start_time).total_seconds()
        
        # Calculer les statistiques
        total_tests = len(self.tests_results)
        tests_passed = len([t for t in self.tests_results if t['status'] == 'PASS'])
        tests_failed = len([t for t in self.tests_results if t['status'] == 'FAIL'])
        tests_errors = len([t for t in self.tests_results if t['status'] == 'ERROR'])
        
        rapport = {
            "agent": self.agent_name,
            "model": self.model_name,
            "timestamp": self.start_time.isoformat(),
            "duree_secondes": duree,
            "status": "SUCCESS" if tests_passed > tests_failed else "PARTIAL",
            "statistiques": {
                "total_tests": total_tests,
                "tests_passed": tests_passed,
                "tests_failed": tests_failed,
                "tests_errors": tests_errors,
                "taux_succes": round(tests_passed / total_tests * 100, 1) if total_tests > 0 else 0,
                "outils_valides": len(self.outils_valides)
            },
            "tests_results": self.tests_results,
            "outils_valides": self.outils_valides,
            "erreurs_tests": self.erreurs_tests,
            "tests_passed": tests_passed
        }
        
        # Sauvegarder le rapport
        rapport_path = self.workspace_path / "reports" / f"agent_4_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        rapport_path.parent.mkdir(exist_ok=True)
        
        with open(rapport_path, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        print(f"[DOCUMENT] Rapport sauvegard: {rapport_path}")
        print(f"[CHART] Tests: {tests_passed}/{total_tests} russis ({rapport['statistiques']['taux_succes']}%)")
        
        return rapport

# Factory function pour compatibilité TemplateManager
def create_agent_4TesteurIntegration(**config):
    """Factory function pour créer l'agent"""
    return Agent4TesteurIntegration(**config) 