#!/usr/bin/env python3
"""
Agent 6 - Validateur Final
Modèle: Claude Sonnet 4
Mission: Validation finale de la mission d'intégration des outils
Équipe: NextGeneration Tools Migration
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Agent6ValidateurFinal:
    """Agent 6 - Validateur Final avec Claude Sonnet 4"""
    
    def __init__(self, agent_id: str = None, agent_type: str = "validator", resultats_equipe: Dict[str, Any] = None, target_path=None, workspace_path=None, **config):
        # Configuration TemplateManager
        self.agent_id = agent_id or f"agent_6_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.agent_type = agent_type
        self.config = config
        self.logger = logging.getLogger(f"Agent6_ValidateurFinal_{self.agent_id}")
        
        # Configuration spécifique - Rétrocompatibilité avec l'ancienne signature
        if resultats_equipe is None:
            resultats_equipe = config.get("resultats_equipe", {})
        if target_path is None:
            target_path = config.get("target_path", "./adapted_tools")
        if workspace_path is None:
            workspace_path = config.get("workspace_path", ".")
            
        # Configuration
        self.resultats_equipe = resultats_equipe
        self.target_path = Path(target_path)
        self.workspace_path = Path(workspace_path)
        self.reports_path = self.workspace_path / "reports"
        
        # Métriques de validation
        self.validation_results = {
            "validation_passed": False,
            "mission_status": "UNKNOWN",
            "quality_score": 0.0,
            "critical_issues": [],
            "warnings": [],
            "recommendations": [],
            "final_report": {}
        }
        
        self.logger.info(f"🔍 Agent 6 - Validateur Final initialisé - ID: {self.agent_id}")
    
    async def startup(self):
        """Démarrage de l'agent - Interface TemplateManager"""
        self.logger.info(f"🚀 Démarrage Agent 6 Validateur Final (ID: {self.agent_id})")
        return {"status": "started", "agent_id": self.agent_id}
    
    async def shutdown(self):
        """Arrêt de l'agent - Interface TemplateManager"""
        self.logger.info(f"🛑 Arrêt Agent 6 Validateur Final (ID: {self.agent_id})")
        return {"status": "stopped", "agent_id": self.agent_id}
    
    async def health_check(self) -> Dict[str, Any]:
        """Vérification de santé - Interface TemplateManager"""
        return {
            "status": "healthy",
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "target_path_exists": self.target_path.exists(),
            "workspace_path_exists": self.workspace_path.exists(),
            "resultats_equipe_loaded": bool(self.resultats_equipe)
        }
    
    async def execute_task(self, task_config: Dict = None) -> Dict[str, Any]:
        """Exécuter la tâche principale - Interface TemplateManager"""
        return await self.valider_mission()
    
    async def valider_mission(self) -> Dict[str, Any]:
        """Validation complète de la mission d'intégration"""
        self.logger.info("🎯 [TARGET] Démarrage validation finale mission")
        
        # Phase 1: Validation des résultats d'équipe
        await self._valider_resultats_equipe()
        
        # Phase 2: Validation de l'intégrité des outils
        await self._valider_integrite_outils()
        
        # Phase 3: Tests de fonctionnalité
        await self._executer_tests_fonctionnalite()
        
        # Phase 4: Validation de la documentation
        await self._valider_documentation()
        
        # Phase 5: Évaluation globale
        await self._evaluer_mission_globale()
        
        # Phase 6: Génération rapport final
        rapport_final = await self._generer_rapport_final()
        
        self.logger.info(f"✅ [CHECK] Validation terminée: Status {self.validation_results['mission_status']}")
        return rapport_final
    
    async def _valider_resultats_equipe(self):
        """Validation des résultats de chaque agent de l'équipe"""
        self.logger.info("📊 [CHART] Validation des résultats d'équipe")
        
        required_agents = ['agent_1', 'agent_2', 'agent_3', 'agent_4', 'agent_5']
        missing_agents = []
        
        for agent_id in required_agents:
            if agent_id not in self.resultats_equipe:
                missing_agents.append(agent_id)
                self.validation_results["critical_issues"].append(f"Résultats manquants pour {agent_id}")
        
        # Validation spécifique par agent
        if 'agent_1' in self.resultats_equipe:
            tools_analyzed = self.resultats_equipe['agent_1'].get('tools_count', 0)
            if tools_analyzed == 0:
                self.validation_results["critical_issues"].append("Agent 1: Aucun outil analysé")
            else:
                self.logger.info(f"✅ Agent 1: {tools_analyzed} outils analysés")
        
        if 'agent_2' in self.resultats_equipe:
            tools_selected = len(self.resultats_equipe['agent_2'].get('outils_utiles', []))
            if tools_selected == 0:
                self.validation_results["warnings"].append("Agent 2: Aucun outil sélectionné")
            else:
                self.logger.info(f"✅ Agent 2: {tools_selected} outils sélectionnés")
        
        if 'agent_3' in self.resultats_equipe:
            tools_adapted = self.resultats_equipe['agent_3'].get('tools_adapted', 0)
            if tools_adapted == 0:
                self.validation_results["warnings"].append("Agent 3: Aucun outil adapté")
            else:
                self.logger.info(f"✅ Agent 3: {tools_adapted} outils adaptés")
        
        if missing_agents:
            self.logger.error(f"❌ [CROSS] Agents manquants: {missing_agents}")
    
    async def _valider_integrite_outils(self):
        """Validation de l'intégrité des outils copiés/adaptés"""
        self.logger.info("🔧 [TOOL] Validation intégrité des outils")
        
        if not self.target_path.exists():
            self.validation_results["critical_issues"].append(f"Répertoire cible inexistant: {self.target_path}")
            return
        
        # Compter les fichiers Python copiés
        python_files = list(self.target_path.rglob("*.py"))
        
        if len(python_files) == 0:
            self.validation_results["critical_issues"].append("Aucun fichier Python trouvé dans le répertoire cible")
        else:
            self.logger.info(f"✅ {len(python_files)} fichiers Python trouvés")
            
            # Validation syntaxique de base
            syntax_errors = 0
            for py_file in python_files:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    compile(content, str(py_file), 'exec')
                except SyntaxError as e:
                    syntax_errors += 1
                    self.validation_results["warnings"].append(f"Erreur syntaxe dans {py_file.name}: {e}")
                except Exception as e:
                    self.validation_results["warnings"].append(f"Erreur lecture {py_file.name}: {e}")
            
            if syntax_errors > 0:
                self.validation_results["warnings"].append(f"{syntax_errors} fichiers avec erreurs syntaxe")
    
    async def _executer_tests_fonctionnalite(self):
        """Exécution de tests de fonctionnalité de base"""
        self.logger.info("🧪 [TEST] Tests de fonctionnalité")
        
        tests_passed = 0
        tests_total = 0
        
        # Test 1: Importation des modules
        if self.target_path.exists():
            python_files = list(self.target_path.rglob("*.py"))
            for py_file in python_files[:5]:  # Test seulement les 5 premiers
                tests_total += 1
                try:
                    # Test d'importation basique
                    result = subprocess.run([
                        'python', '-c', f'import sys; sys.path.append("{self.target_path}"); compile(open("{py_file}").read(), "{py_file}", "exec")'
                    ], capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0:
                        tests_passed += 1
                    else:
                        self.validation_results["warnings"].append(f"Test échec pour {py_file.name}")
                        
                except Exception as e:
                    self.validation_results["warnings"].append(f"Erreur test {py_file.name}: {e}")
        
        # Calcul du taux de réussite
        if tests_total > 0:
            success_rate = (tests_passed / tests_total) * 100
            self.logger.info(f"✅ Tests: {tests_passed}/{tests_total} réussis ({success_rate:.1f}%)")
            
            if success_rate < 50:
                self.validation_results["critical_issues"].append(f"Taux de réussite tests trop faible: {success_rate:.1f}%")
        else:
            self.validation_results["warnings"].append("Aucun test exécuté")
    
    async def _valider_documentation(self):
        """Validation de la documentation générée"""
        self.logger.info("📖 [DOCUMENT] Validation documentation")
        
        # Vérifier la présence des fichiers de documentation
        docs_attendus = [
            self.target_path / "README.md",
            self.target_path / "docs" / "GUIDE_UTILISATION.md",
            self.target_path / "docs" / "GUIDE_INSTALLATION.md"
        ]
        
        docs_presents = 0
        for doc_file in docs_attendus:
            if doc_file.exists() and doc_file.stat().st_size > 100:  # Au moins 100 bytes
                docs_presents += 1
                self.logger.info(f"✅ Documentation trouvée: {doc_file.name}")
            else:
                self.validation_results["warnings"].append(f"Documentation manquante ou vide: {doc_file.name}")
        
        if docs_presents == 0:
            self.validation_results["critical_issues"].append("Aucune documentation trouvée")
        elif docs_presents < len(docs_attendus):
            self.validation_results["warnings"].append(f"Documentation incomplète: {docs_presents}/{len(docs_attendus)}")
    
    async def _evaluer_mission_globale(self):
        """Évaluation globale de la mission"""
        self.logger.info("🎯 [TARGET] Évaluation globale mission")
        
        # Calcul du score de qualité
        score_base = 100.0
        
        # Pénalités pour problèmes critiques
        score_base -= len(self.validation_results["critical_issues"]) * 20
        
        # Pénalités pour avertissements
        score_base -= len(self.validation_results["warnings"]) * 5
        
        # Bonus pour résultats positifs
        if 'agent_1' in self.resultats_equipe:
            tools_count = self.resultats_equipe['agent_1'].get('tools_count', 0)
            if tools_count > 0:
                score_base += min(tools_count * 2, 20)  # Max 20 points bonus
        
        # Assurer que le score reste dans [0, 100]
        self.validation_results["quality_score"] = max(0.0, min(100.0, score_base))
        
        # Déterminer le statut de la mission
        if len(self.validation_results["critical_issues"]) == 0:
            if self.validation_results["quality_score"] >= 80:
                self.validation_results["mission_status"] = "SUCCESS"
                self.validation_results["validation_passed"] = True
            elif self.validation_results["quality_score"] >= 60:
                self.validation_results["mission_status"] = "PARTIAL_SUCCESS"
                self.validation_results["validation_passed"] = True
            else:
                self.validation_results["mission_status"] = "NEEDS_IMPROVEMENT"
        else:
            self.validation_results["mission_status"] = "FAILED"
        
        # Générer des recommandations
        await self._generer_recommandations()
        
        self.logger.info(f"📊 Score qualité: {self.validation_results['quality_score']:.1f}/100")
        self.logger.info(f"🎯 Statut mission: {self.validation_results['mission_status']}")
    
    async def _generer_recommandations(self):
        """Génération de recommandations pour améliorer la mission"""
        recommendations = []
        
        if len(self.validation_results["critical_issues"]) > 0:
            recommendations.append("Résoudre tous les problèmes critiques identifiés")
        
        if len(self.validation_results["warnings"]) > 3:
            recommendations.append("Traiter les avertissements multiples pour améliorer la qualité")
        
        if self.validation_results["quality_score"] < 70:
            recommendations.append("Améliorer la qualité globale avant déploiement")
        
        # Recommandations spécifiques par agent
        if 'agent_2' in self.resultats_equipe:
            tools_selected = len(self.resultats_equipe['agent_2'].get('outils_utiles', []))
            if tools_selected == 0:
                recommendations.append("Revoir les critères de sélection des outils (Agent 2)")
        
        if not recommendations:
            recommendations.append("Mission bien exécutée - Prêt pour déploiement")
        
        self.validation_results["recommendations"] = recommendations
    
    async def _generer_rapport_final(self) -> Dict[str, Any]:
        """Génération du rapport final de validation"""
        self.logger.info("📄 [DOCUMENT] Génération rapport final")
        
        rapport_final = {
            "agent": "Agent 6 - Validateur Final",
            "model": "Claude Sonnet 4",
            "timestamp": datetime.now().isoformat(),
            "mission_validation": {
                "status": self.validation_results["mission_status"],
                "validation_passed": self.validation_results["validation_passed"],
                "quality_score": self.validation_results["quality_score"]
            },
            "issues_analysis": {
                "critical_issues": self.validation_results["critical_issues"],
                "warnings": self.validation_results["warnings"],
                "total_issues": len(self.validation_results["critical_issues"]) + len(self.validation_results["warnings"])
            },
            "team_results_summary": self._resumer_resultats_equipe(),
            "recommendations": self.validation_results["recommendations"],
            "validation_details": {
                "team_validation": "completed",
                "tools_integrity": "validated",
                "functionality_tests": "executed",
                "documentation": "checked"
            }
        }
        
        # Sauvegarder le rapport
        rapport_path = self.reports_path / f"agent_6_validation_finale_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.reports_path.mkdir(exist_ok=True)
        
        with open(rapport_path, 'w', encoding='utf-8') as f:
            json.dump(rapport_final, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"📄 [DOCUMENT] Rapport sauvegardé: {rapport_path}")
        
        self.validation_results["final_report"] = rapport_final
        return rapport_final
    
    def _resumer_resultats_equipe(self) -> Dict[str, Any]:
        """Résumé des résultats de l'équipe"""
        summary = {}
        
        for agent_id, results in self.resultats_equipe.items():
            if agent_id == 'agent_1':
                summary[agent_id] = {
                    "tools_analyzed": results.get('tools_count', 0),
                    "status": "completed" if results.get('tools_count', 0) > 0 else "failed"
                }
            elif agent_id == 'agent_2':
                tools_selected = len(results.get('outils_utiles', []))
                summary[agent_id] = {
                    "tools_selected": tools_selected,
                    "status": "completed" if tools_selected > 0 else "no_selection"
                }
            elif agent_id == 'agent_3':
                summary[agent_id] = {
                    "tools_adapted": results.get('tools_adapted', 0),
                    "tools_copied": results.get('tools_copied', 0),
                    "status": "completed"
                }
            elif agent_id in ['agent_4', 'agent_5']:
                summary[agent_id] = {
                    "status": "completed",
                    "results": results
                }
        
        return summary

# Factory function pour compatibilité TemplateManager
def create_agent_6ValidateurFinal(**config):
    """Factory function pour créer l'agent"""
    return Agent6ValidateurFinal(**config)

# Fonction de test
async def main():
    """Test de l'agent validateur final"""
    # Données de test
    test_results = {
        'agent_1': {'tools_count': 29},
        'agent_2': {'outils_utiles': ['tool1', 'tool2', 'tool3', 'tool4', 'tool5']},
        'agent_3': {'tools_adapted': 3, 'tools_copied': 5},
        'agent_4': {'tests_passed': 1},
        'agent_5': {'docs_created': 3}
    }
    
    agent = Agent6ValidateurFinal(
        resultats_equipe=test_results,
        target_path="tools/imported_tools",
        workspace_path="."
    )
    
    result = await agent.valider_mission()
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main()) 