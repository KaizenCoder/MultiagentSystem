#!/usr/bin/env python3
"""
Agent 6 - Validateur Final
Partie du systme NextGeneration - quipe d'agents pour importation d'outils

Mission: Validation finale de l'intgration des outils et oprations Git
Modle: Claude Sonnet 4 (validation et oprations critiques)
"""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class AgentValidateurFinal:
    """Agent 6 - Validateur Final pour l'importation d'outils SuperWhisper_V6"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.tools_dir = self.project_root / "tools" / "imported_tools"
        self.reports_dir = self.project_root / "reports" / "tools_integration"
        
        # Configuration logging
        self.logger = logging.getLogger("Agent6_ValidateurFinal")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def valider_integration_complete(self, rapport_phases: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validation finale de l'intgration complte
        
        Args:
            rapport_phases: Rapports de toutes les phases prcdentes
            
        Returns:
            Dict contenant le rsultat de validation et actions Git
        """
        self.logger.info("[SEARCH] Dmarrage validation finale de l'intgration")
        
        validation_result = {
            "timestamp": datetime.now().isoformat(),
            "agent": "Agent6_ValidateurFinal",
            "model": "Claude Sonnet 4",
            "validation_checks": {},
            "git_operations": {},
            "final_status": "unknown",
            "recommendations": []
        }
        
        try:
            # 1. Validation structure des outils
            structure_valid = self._valider_structure_outils()
            validation_result["validation_checks"]["structure"] = structure_valid
            
            # 2. Validation cohrence des rapports
            coherence_valid = self._valider_coherence_rapports(rapport_phases)
            validation_result["validation_checks"]["coherence"] = coherence_valid
            
            # 3. Validation configuration
            config_valid = self._valider_configuration()
            validation_result["validation_checks"]["configuration"] = config_valid
            
            # 4. Validation documentation
            docs_valid = self._valider_documentation()
            validation_result["validation_checks"]["documentation"] = docs_valid
            
            # 5. Dterminer si intgration est russie
            integration_success = all([
                structure_valid["status"] == "success",
                coherence_valid["status"] == "success", 
                config_valid["status"] == "success",
                docs_valid["status"] == "success"
            ])
            
            validation_result["final_status"] = "success" if integration_success else "partial"
            
            # 6. Oprations Git si succs
            if integration_success:
                git_result = self._executer_operations_git()
                validation_result["git_operations"] = git_result
                
                if git_result["status"] == "success":
                    validation_result["final_status"] = "complete_success"
                    self.logger.info("[CHECK] Intgration complte avec succs Git")
                else:
                    validation_result["final_status"] = "success_no_git"
                    self.logger.warning(" Intgration russie mais chec Git")
            else:
                self.logger.warning(" Intgration partielle - pas d'oprations Git")
            
            # 7. Gnrer recommandations
            validation_result["recommendations"] = self._generer_recommandations(validation_result)
            
            self.logger.info(f"[CHECK] Validation termine - Status: {validation_result['final_status']}")
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur validation finale: {str(e)}")
            validation_result["final_status"] = "error"
            validation_result["error"] = str(e)
        
        return validation_result
    
    def _valider_structure_outils(self) -> Dict[str, Any]:
        """Valide la structure des outils imports"""
        self.logger.info("[SEARCH] Validation structure des outils")
        
        result = {
            "status": "unknown",
            "tools_found": 0,
            "categories": [],
            "missing_files": [],
            "issues": []
        }
        
        try:
            if not self.tools_dir.exists():
                result["status"] = "error"
                result["issues"].append("Rpertoire tools/imported_tools n'existe pas")
                return result
            
            # Compter les outils par catgorie
            categories = [d for d in self.tools_dir.iterdir() if d.is_dir() and d.name != "__pycache__"]
            result["categories"] = [cat.name for cat in categories]
            
            total_tools = 0
            for category in categories:
                tools_in_cat = [f for f in category.glob("*.py") if f.name != "__init__.py"]
                total_tools += len(tools_in_cat)
            
            result["tools_found"] = total_tools
            
            # Vrifier fichiers essentiels
            essential_files = [
                self.tools_dir / "tools_config.json",
                self.tools_dir / "run_tool.py",
                self.tools_dir / "requirements.txt",
                self.tools_dir / "README.md"
            ]
            
            for file_path in essential_files:
                if not file_path.exists():
                    result["missing_files"].append(str(file_path.relative_to(self.project_root)))
            
            if result["missing_files"]:
                result["status"] = "warning"
                result["issues"].append(f"Fichiers manquants: {len(result['missing_files'])}")
            else:
                result["status"] = "success"
            
            self.logger.info(f"[CHART] Structure: {total_tools} outils, {len(categories)} catgories")
            
        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Erreur validation structure: {str(e)}")
        
        return result
    
    def _valider_coherence_rapports(self, rapport_phases: Dict[str, Any]) -> Dict[str, Any]:
        """Valide la cohrence entre les rapports des phases"""
        self.logger.info("[SEARCH] Validation cohrence des rapports")
        
        result = {
            "status": "unknown",
            "phases_completed": 0,
            "tools_consistency": True,
            "issues": []
        }
        
        try:
            phases_attendues = ["phase1", "phase2", "phase3", "phase4", "phase5"]
            phases_trouvees = [p for p in phases_attendues if p in rapport_phases]
            result["phases_completed"] = len(phases_trouvees)
            
            # Vrifier cohrence nombre d'outils
            if "phase1" in rapport_phases and "phase3" in rapport_phases:
                tools_analysed = rapport_phases["phase1"].get("tools_analysed", 0)
                tools_adapted = rapport_phases["phase3"].get("tools_adapted", 0)
                
                if tools_adapted > tools_analysed:
                    result["tools_consistency"] = False
                    result["issues"].append("Plus d'outils adapts que analyss")
            
            # Vrifier statuts des phases
            phases_success = all(
                rapport_phases.get(phase, {}).get("status") == "success" 
                for phase in phases_trouvees
            )
            
            if phases_success and result["tools_consistency"]:
                result["status"] = "success"
            elif len(phases_trouvees) >= 3:
                result["status"] = "warning"
                result["issues"].append("Phases incompltes mais minimum atteint")
            else:
                result["status"] = "error"
                result["issues"].append("Trop peu de phases compltes")
            
            self.logger.info(f"[CHART] Cohrence: {len(phases_trouvees)}/5 phases, cohrent: {result['tools_consistency']}")
            
        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Erreur validation cohrence: {str(e)}")
        
        return result
    
    def _valider_configuration(self) -> Dict[str, Any]:
        """Valide la configuration des outils"""
        self.logger.info("[SEARCH] Validation configuration")
        
        result = {
            "status": "unknown",
            "config_valid": False,
            "launcher_valid": False,
            "requirements_valid": False,
            "issues": []
        }
        
        try:
            # Vrifier tools_config.json
            config_file = self.tools_dir / "tools_config.json"
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                    
                    if "tools" in config_data and "metadata" in config_data:
                        result["config_valid"] = True
                    else:
                        result["issues"].append("Configuration JSON incomplte")
                except json.JSONDecodeError:
                    result["issues"].append("Configuration JSON invalide")
            else:
                result["issues"].append("Fichier configuration manquant")
            
            # Vrifier run_tool.py
            launcher_file = self.tools_dir / "run_tool.py"
            if launcher_file.exists() and launcher_file.stat().st_size > 100:
                result["launcher_valid"] = True
            else:
                result["issues"].append("Lanceur invalide ou manquant")
            
            # Vrifier requirements.txt
            req_file = self.tools_dir / "requirements.txt"
            if req_file.exists():
                try:
                    with open(req_file, 'r', encoding='utf-8') as f:
                        requirements = f.read().strip()
                    
                    if requirements:
                        result["requirements_valid"] = True
                    else:
                        result["issues"].append("Requirements vide")
                except Exception:
                    result["issues"].append("Erreur lecture requirements")
            else:
                result["issues"].append("Requirements manquant")
            
            # Statut global
            if all([result["config_valid"], result["launcher_valid"], result["requirements_valid"]]):
                result["status"] = "success"
            elif result["config_valid"] or result["launcher_valid"]:
                result["status"] = "warning"
            else:
                result["status"] = "error"
            
            self.logger.info(f" Config: {result['config_valid']}, Launcher: {result['launcher_valid']}, Req: {result['requirements_valid']}")
            
        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Erreur validation config: {str(e)}")
        
        return result
    
    def _valider_documentation(self) -> Dict[str, Any]:
        """Valide la documentation gnre"""
        self.logger.info("[SEARCH] Validation documentation")
        
        result = {
            "status": "unknown",
            "docs_found": 0,
            "readme_valid": False,
            "issues": []
        }
        
        try:
            # Compter les fichiers de documentation
            doc_files = list(self.tools_dir.glob("**/*.md"))
            result["docs_found"] = len(doc_files)
            
            # Vrifier README principal
            readme_file = self.tools_dir / "README.md"
            if readme_file.exists():
                try:
                    with open(readme_file, 'r', encoding='utf-8') as f:
                        readme_content = f.read()
                    
                    if len(readme_content) > 200 and "NextGeneration" in readme_content:
                        result["readme_valid"] = True
                    else:
                        result["issues"].append("README trop court ou incomplet")
                except Exception:
                    result["issues"].append("Erreur lecture README")
            else:
                result["issues"].append("README principal manquant")
            
            # Statut bas sur la documentation
            if result["readme_valid"] and result["docs_found"] >= 3:
                result["status"] = "success"
            elif result["readme_valid"] or result["docs_found"] >= 1:
                result["status"] = "warning"
            else:
                result["status"] = "error"
            
            self.logger.info(f" Documentation: {result['docs_found']} fichiers, README: {result['readme_valid']}")
            
        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Erreur validation docs: {str(e)}")
        
        return result
    
    def _executer_operations_git(self) -> Dict[str, Any]:
        """Excute les oprations Git (add, commit, push)"""
        self.logger.info(" Excution oprations Git")
        
        result = {
            "status": "unknown",
            "operations": [],
            "commit_hash": None,
            "issues": []
        }
        
        try:
            os.chdir(self.project_root)
            
            # 1. Git add des nouveaux outils
            add_cmd = ["git", "add", "tools/imported_tools/"]
            add_result = subprocess.run(add_cmd, capture_output=True, text=True)
            
            result["operations"].append({
                "command": "git add",
                "success": add_result.returncode == 0,
                "output": add_result.stdout if add_result.returncode == 0 else add_result.stderr
            })
            
            if add_result.returncode != 0:
                result["issues"].append(f"chec git add: {add_result.stderr}")
                result["status"] = "error"
                return result
            
            # 2. Vrifier s'il y a des changements  commiter
            status_cmd = ["git", "status", "--porcelain", "tools/imported_tools/"]
            status_result = subprocess.run(status_cmd, capture_output=True, text=True)
            
            if not status_result.stdout.strip():
                result["status"] = "no_changes"
                result["issues"].append("Aucun changement  commiter")
                return result
            
            # 3. Git commit
            commit_message = f"feat: Import outils SuperWhisper_V6 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            commit_cmd = ["git", "commit", "-m", commit_message]
            commit_result = subprocess.run(commit_cmd, capture_output=True, text=True)
            
            result["operations"].append({
                "command": "git commit",
                "success": commit_result.returncode == 0,
                "output": commit_result.stdout if commit_result.returncode == 0 else commit_result.stderr
            })
            
            if commit_result.returncode != 0:
                result["issues"].append(f"chec git commit: {commit_result.stderr}")
                result["status"] = "error"
                return result
            
            # Extraire hash du commit
            if "commit" in commit_result.stdout.lower():
                lines = commit_result.stdout.split('\n')
                for line in lines:
                    if line.strip().startswith('['):
                        # Format: [branch hash] message
                        parts = line.split(']')[0].split()
                        if len(parts) >= 2:
                            result["commit_hash"] = parts[1]
                        break
            
            # 4. Git push
            push_cmd = ["git", "push"]
            push_result = subprocess.run(push_cmd, capture_output=True, text=True)
            
            result["operations"].append({
                "command": "git push",
                "success": push_result.returncode == 0,
                "output": push_result.stdout if push_result.returncode == 0 else push_result.stderr
            })
            
            if push_result.returncode != 0:
                result["issues"].append(f"chec git push: {push_result.stderr}")
                result["status"] = "partial"  # Commit OK mais push KO
            else:
                result["status"] = "success"
            
            self.logger.info(f"[CHECK] Git: Add , Commit  ({result['commit_hash']}), Push: {push_result.returncode == 0}")
            
        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Erreur oprations Git: {str(e)}")
            self.logger.error(f"[CROSS] Erreur Git: {str(e)}")
        
        return result
    
    def _generer_recommandations(self, validation_result: Dict[str, Any]) -> List[str]:
        """Gnre des recommandations bases sur les rsultats de validation"""
        recommendations = []
        
        # Recommandations bases sur le statut final
        if validation_result["final_status"] == "complete_success":
            recommendations.append("[CHECK] Intgration complte russie - Outils prts  l'utilisation")
            recommendations.append("[TOOL] Excuter 'pip install -r tools/imported_tools/requirements.txt' pour installer les dpendances")
            recommendations.append(" Consulter tools/imported_tools/README.md pour guide d'utilisation")
        
        elif validation_result["final_status"] == "success_no_git":
            recommendations.append(" Intgration russie mais oprations Git choues")
            recommendations.append(" Effectuer manuellement: git add tools/imported_tools/ && git commit -m 'Import outils' && git push")
        
        elif validation_result["final_status"] == "partial":
            recommendations.append(" Intgration partielle - Vrifier les problmes signals")
            
            # Recommandations spcifiques par type de problme
            checks = validation_result.get("validation_checks", {})
            
            if checks.get("structure", {}).get("status") != "success":
                recommendations.append("[TOOL] Corriger la structure des outils imports")
            
            if checks.get("configuration", {}).get("status") != "success":
                recommendations.append(" Vrifier et corriger la configuration (tools_config.json, run_tool.py)")
            
            if checks.get("documentation", {}).get("status") != "success":
                recommendations.append(" Complter la documentation manquante")
        
        else:
            recommendations.append("[CROSS] Intgration choue - Relancer le processus aprs correction des erreurs")
        
        # Recommandations gnrales
        recommendations.append(" Tester les outils imports avant utilisation en production")
        recommendations.append("[CHART] Consulter le rapport dtaill pour plus d'informations")
        
        return recommendations
    
    def validate_and_commit(self, phase5_data: Dict[str, Any], mission_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interface de compatibilit avec le coordinateur
        
        Args:
            phase5_data: Donnes de la phase 5 (documentation)
            mission_metrics: Mtriques de la mission complte
            
        Returns:
            Dict contenant les rsultats de validation et oprations Git
        """
        # Construire le rapport des phases  partir des mtriques
        rapport_phases = {
            "phase1": {
                "status": "success",
                "tools_analysed": mission_metrics.get("total_tools_analysed", 0)
            },
            "phase2": {
                "status": "success", 
                "tools_selected": mission_metrics.get("total_tools_selected", 0)
            },
            "phase3": {
                "status": "success",
                "tools_adapted": mission_metrics.get("total_tools_adapted", 0)
            },
            "phase4": {
                "status": "success",
                "tools_tested": mission_metrics.get("total_tools_tested", 0)
            },
            "phase5": {
                "status": "success",
                "docs_created": phase5_data.get("docs_created", 0)
            }
        }
        
        return self.valider_integration_complete(rapport_phases)

def main():
    """Point d'entre principal pour tests"""
    import tempfile
    
    # Test avec rpertoire temporaire
    with tempfile.TemporaryDirectory() as temp_dir:
        agent = AgentValidateurFinal(temp_dir)
        
        # Test de validation avec rapport factice
        rapport_test = {
            "phase1": {"status": "success", "tools_analysed": 5},
            "phase3": {"status": "success", "tools_adapted": 3}
        }
        
        result = agent.valider_integration_complete(rapport_test)
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main() 