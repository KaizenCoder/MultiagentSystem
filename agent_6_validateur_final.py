#!/usr/bin/env python3
"""
Agent 6 - Validateur Final
Partie du système NextGeneration - Équipe d'agents pour importation d'outils

Mission: Validation finale de l'intégration des outils et opérations Git
Modèle: Claude Sonnet 4 (validation et opérations critiques)
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
        Validation finale de l'intégration complète
        
        Args:
            rapport_phases: Rapports de toutes les phases précédentes
            
        Returns:
            Dict contenant le résultat de validation et actions Git
        """
        self.logger.info("🔍 Démarrage validation finale de l'intégration")
        
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
            
            # 2. Validation cohérence des rapports
            coherence_valid = self._valider_coherence_rapports(rapport_phases)
            validation_result["validation_checks"]["coherence"] = coherence_valid
            
            # 3. Validation configuration
            config_valid = self._valider_configuration()
            validation_result["validation_checks"]["configuration"] = config_valid
            
            # 4. Validation documentation
            docs_valid = self._valider_documentation()
            validation_result["validation_checks"]["documentation"] = docs_valid
            
            # 5. Déterminer si intégration est réussie
            integration_success = all([
                structure_valid["status"] == "success",
                coherence_valid["status"] == "success", 
                config_valid["status"] == "success",
                docs_valid["status"] == "success"
            ])
            
            validation_result["final_status"] = "success" if integration_success else "partial"
            
            # 6. Opérations Git si succès
            if integration_success:
                git_result = self._executer_operations_git()
                validation_result["git_operations"] = git_result
                
                if git_result["status"] == "success":
                    validation_result["final_status"] = "complete_success"
                    self.logger.info("✅ Intégration complète avec succès Git")
                else:
                    validation_result["final_status"] = "success_no_git"
                    self.logger.warning("⚠️ Intégration réussie mais échec Git")
            else:
                self.logger.warning("⚠️ Intégration partielle - pas d'opérations Git")
            
            # 7. Générer recommandations
            validation_result["recommendations"] = self._generer_recommandations(validation_result)
            
            self.logger.info(f"✅ Validation terminée - Status: {validation_result['final_status']}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur validation finale: {str(e)}")
            validation_result["final_status"] = "error"
            validation_result["error"] = str(e)
        
        return validation_result
    
    def _valider_structure_outils(self) -> Dict[str, Any]:
        """Valide la structure des outils importés"""
        self.logger.info("🔍 Validation structure des outils")
        
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
                result["issues"].append("Répertoire tools/imported_tools n'existe pas")
                return result
            
            # Compter les outils par catégorie
            categories = [d for d in self.tools_dir.iterdir() if d.is_dir() and d.name != "__pycache__"]
            result["categories"] = [cat.name for cat in categories]
            
            total_tools = 0
            for category in categories:
                tools_in_cat = [f for f in category.glob("*.py") if f.name != "__init__.py"]
                total_tools += len(tools_in_cat)
            
            result["tools_found"] = total_tools
            
            # Vérifier fichiers essentiels
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
            
            self.logger.info(f"📊 Structure: {total_tools} outils, {len(categories)} catégories")
            
        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Erreur validation structure: {str(e)}")
        
        return result
    
    def _valider_coherence_rapports(self, rapport_phases: Dict[str, Any]) -> Dict[str, Any]:
        """Valide la cohérence entre les rapports des phases"""
        self.logger.info("🔍 Validation cohérence des rapports")
        
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
            
            # Vérifier cohérence nombre d'outils
            if "phase1" in rapport_phases and "phase3" in rapport_phases:
                tools_analysed = rapport_phases["phase1"].get("tools_analysed", 0)
                tools_adapted = rapport_phases["phase3"].get("tools_adapted", 0)
                
                if tools_adapted > tools_analysed:
                    result["tools_consistency"] = False
                    result["issues"].append("Plus d'outils adaptés que analysés")
            
            # Vérifier statuts des phases
            phases_success = all(
                rapport_phases.get(phase, {}).get("status") == "success" 
                for phase in phases_trouvees
            )
            
            if phases_success and result["tools_consistency"]:
                result["status"] = "success"
            elif len(phases_trouvees) >= 3:
                result["status"] = "warning"
                result["issues"].append("Phases incomplètes mais minimum atteint")
            else:
                result["status"] = "error"
                result["issues"].append("Trop peu de phases complétées")
            
            self.logger.info(f"📊 Cohérence: {len(phases_trouvees)}/5 phases, cohérent: {result['tools_consistency']}")
            
        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Erreur validation cohérence: {str(e)}")
        
        return result
    
    def _valider_configuration(self) -> Dict[str, Any]:
        """Valide la configuration des outils"""
        self.logger.info("🔍 Validation configuration")
        
        result = {
            "status": "unknown",
            "config_valid": False,
            "launcher_valid": False,
            "requirements_valid": False,
            "issues": []
        }
        
        try:
            # Vérifier tools_config.json
            config_file = self.tools_dir / "tools_config.json"
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                    
                    if "tools" in config_data and "metadata" in config_data:
                        result["config_valid"] = True
                    else:
                        result["issues"].append("Configuration JSON incomplète")
                except json.JSONDecodeError:
                    result["issues"].append("Configuration JSON invalide")
            else:
                result["issues"].append("Fichier configuration manquant")
            
            # Vérifier run_tool.py
            launcher_file = self.tools_dir / "run_tool.py"
            if launcher_file.exists() and launcher_file.stat().st_size > 100:
                result["launcher_valid"] = True
            else:
                result["issues"].append("Lanceur invalide ou manquant")
            
            # Vérifier requirements.txt
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
            
            self.logger.info(f"⚙️ Config: {result['config_valid']}, Launcher: {result['launcher_valid']}, Req: {result['requirements_valid']}")
            
        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Erreur validation config: {str(e)}")
        
        return result
    
    def _valider_documentation(self) -> Dict[str, Any]:
        """Valide la documentation générée"""
        self.logger.info("🔍 Validation documentation")
        
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
            
            # Vérifier README principal
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
            
            # Statut basé sur la documentation
            if result["readme_valid"] and result["docs_found"] >= 3:
                result["status"] = "success"
            elif result["readme_valid"] or result["docs_found"] >= 1:
                result["status"] = "warning"
            else:
                result["status"] = "error"
            
            self.logger.info(f"📚 Documentation: {result['docs_found']} fichiers, README: {result['readme_valid']}")
            
        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Erreur validation docs: {str(e)}")
        
        return result
    
    def _executer_operations_git(self) -> Dict[str, Any]:
        """Exécute les opérations Git (add, commit, push)"""
        self.logger.info("🔄 Exécution opérations Git")
        
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
                result["issues"].append(f"Échec git add: {add_result.stderr}")
                result["status"] = "error"
                return result
            
            # 2. Vérifier s'il y a des changements à commiter
            status_cmd = ["git", "status", "--porcelain", "tools/imported_tools/"]
            status_result = subprocess.run(status_cmd, capture_output=True, text=True)
            
            if not status_result.stdout.strip():
                result["status"] = "no_changes"
                result["issues"].append("Aucun changement à commiter")
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
                result["issues"].append(f"Échec git commit: {commit_result.stderr}")
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
                result["issues"].append(f"Échec git push: {push_result.stderr}")
                result["status"] = "partial"  # Commit OK mais push KO
            else:
                result["status"] = "success"
            
            self.logger.info(f"✅ Git: Add ✓, Commit ✓ ({result['commit_hash']}), Push: {push_result.returncode == 0}")
            
        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Erreur opérations Git: {str(e)}")
            self.logger.error(f"❌ Erreur Git: {str(e)}")
        
        return result
    
    def _generer_recommandations(self, validation_result: Dict[str, Any]) -> List[str]:
        """Génère des recommandations basées sur les résultats de validation"""
        recommendations = []
        
        # Recommandations basées sur le statut final
        if validation_result["final_status"] == "complete_success":
            recommendations.append("✅ Intégration complète réussie - Outils prêts à l'utilisation")
            recommendations.append("🔧 Exécuter 'pip install -r tools/imported_tools/requirements.txt' pour installer les dépendances")
            recommendations.append("📖 Consulter tools/imported_tools/README.md pour guide d'utilisation")
        
        elif validation_result["final_status"] == "success_no_git":
            recommendations.append("⚠️ Intégration réussie mais opérations Git échouées")
            recommendations.append("🔄 Effectuer manuellement: git add tools/imported_tools/ && git commit -m 'Import outils' && git push")
        
        elif validation_result["final_status"] == "partial":
            recommendations.append("⚠️ Intégration partielle - Vérifier les problèmes signalés")
            
            # Recommandations spécifiques par type de problème
            checks = validation_result.get("validation_checks", {})
            
            if checks.get("structure", {}).get("status") != "success":
                recommendations.append("🔧 Corriger la structure des outils importés")
            
            if checks.get("configuration", {}).get("status") != "success":
                recommendations.append("⚙️ Vérifier et corriger la configuration (tools_config.json, run_tool.py)")
            
            if checks.get("documentation", {}).get("status") != "success":
                recommendations.append("📚 Compléter la documentation manquante")
        
        else:
            recommendations.append("❌ Intégration échouée - Relancer le processus après correction des erreurs")
        
        # Recommandations générales
        recommendations.append("🧪 Tester les outils importés avant utilisation en production")
        recommendations.append("📊 Consulter le rapport détaillé pour plus d'informations")
        
        return recommendations
    
    def validate_and_commit(self, phase5_data: Dict[str, Any], mission_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interface de compatibilité avec le coordinateur
        
        Args:
            phase5_data: Données de la phase 5 (documentation)
            mission_metrics: Métriques de la mission complète
            
        Returns:
            Dict contenant les résultats de validation et opérations Git
        """
        # Construire le rapport des phases à partir des métriques
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
    """Point d'entrée principal pour tests"""
    import tempfile
    
    # Test avec répertoire temporaire
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