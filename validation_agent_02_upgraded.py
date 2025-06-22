#!/usr/bin/env python3
"""
🧪 VALIDATION AGENT 02 UPGRADED - Test Complet Fonctionnalités TOP
================================================================
Mission: Valider toutes les fonctionnalités avancées intégrées de l'équipe TOP
dans l'Agent 02 - Évaluateur Utilité UPGRADED

🎯 Tests à effectuer:
- ✅ Intelligence multi-critères pondérés
- ✅ Mots-clés NextGeneration spécialisés
- ✅ Évaluation 5 dimensions
- ✅ Détection conflits et redondances
- ✅ Algorithme similarité outils
- ✅ Priorisation intelligente
- ✅ Génération recommandations avancées
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys

# Import de l'agent UPGRADED
sys.path.insert(0, str(Path(__file__).parent))
from agents.agent_MAINTENANCE_02_evaluateur_utilite_UPGRADED import (
    AgentEvaluateurUtiliteUpgraded, create_agent_evaluateur_utilite_upgraded
)

class ValidationAgent02Upgraded:
    """Validateur complet pour Agent 02 UPGRADED"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {
            "timestamp": self.timestamp,
            "tests_passed": 0,
            "tests_failed": 0,
            "tests_details": []
        }
        
        # Données de test sophistiquées
        self.test_data_advanced = {
            "tools": [
                {
                    "name": "agent_orchestrator_enterprise",
                    "description": "Enterprise orchestrator for agent factory pattern",
                    "content": """
                    async def orchestrate_agents():
                        import asyncio
                        from core.agent_factory_architecture import Agent
                        # Advanced orchestration logic
                        await agent.startup()
                        return await agent.execute_task()
                    """,
                    "functions": ["orchestrate_agents", "manage_lifecycle", "monitor_performance"],
                    "classes": ["EnterpriseOrchestrator", "AgentManager"],
                    "imports": ["asyncio", "logging", "core.agent_factory_architecture"],
                    "dependencies": ["asyncio", "typing", "pathlib"],
                    "complexity_score": 35
                },
                {
                    "name": "gui_desktop_legacy_tool",
                    "description": "Legacy desktop GUI tool for manual operations",
                    "content": """
                    import tkinter as tk
                    from tkinter import messagebox
                    
                    def create_gui():
                        root = tk.Tk()
                        root.mainloop()
                    """,
                    "functions": ["create_gui", "show_dialog"],
                    "classes": ["GuiApplication"],
                    "imports": ["tkinter"],
                    "dependencies": ["tkinter", "os"],
                    "complexity_score": 65
                },
                {
                    "name": "monitoring_system_production",
                    "description": "Production monitoring system with async capabilities",
                    "content": """
                    async def monitor_system():
                        import asyncio
                        import logging
                        # Production monitoring
                        while True:
                            await asyncio.sleep(1)
                            await check_health()
                    """,
                    "functions": ["monitor_system", "check_health", "send_alerts"],
                    "classes": ["ProductionMonitor", "HealthChecker"],
                    "imports": ["asyncio", "logging", "prometheus_client"],
                    "dependencies": ["asyncio", "prometheus_client"],
                    "complexity_score": 42
                },
                {
                    "name": "backup_manager_utility",
                    "description": "Backup management utility for system maintenance",
                    "content": """
                    def backup_files():
                        import shutil
                        import os
                        # Backup logic
                        shutil.copy2(source, destination)
                    """,
                    "functions": ["backup_files", "restore_files", "validate_backup"],
                    "classes": ["BackupManager"],
                    "imports": ["shutil", "os", "pathlib"],
                    "dependencies": ["shutil", "pathlib"],
                    "complexity_score": 28
                }
            ]
        }
    
    async def run_complete_validation(self):
        """Exécution complète de la validation"""
        print("🧪 VALIDATION AGENT 02 UPGRADED - FONCTIONNALITÉS TOP")
        print("=" * 80)
        print(f"📅 Timestamp: {self.timestamp}")
        print()
        
        # Création de l'agent
        agent = create_agent_evaluateur_utilite_upgraded()
        
        try:
            # Tests de base
            await self._test_agent_startup(agent)
            await self._test_health_check(agent)
            await self._test_capabilities(agent)
            
            # Tests fonctionnalités avancées
            await self._test_multi_criteria_evaluation(agent)
            await self._test_nextgen_keywords_detection(agent)
            await self._test_five_dimensions_evaluation(agent)
            await self._test_conflict_detection(agent)
            await self._test_similarity_algorithm(agent)
            await self._test_intelligent_prioritization(agent)
            await self._test_advanced_recommendations(agent)
            
            # Test intégration complète
            await self._test_complete_integration(agent)
            
            await agent.shutdown()
            
        except Exception as e:
            print(f"❌ Erreur validation: {e}")
            await agent.shutdown()
        
        # Affichage résultats
        self._display_results()
        
        return self.results
    
    async def _test_agent_startup(self, agent):
        """Test démarrage agent"""
        test_name = "Agent Startup"
        try:
            await agent.startup()
            self._record_success(test_name, "Agent démarré avec succès")
        except Exception as e:
            self._record_failure(test_name, f"Erreur démarrage: {e}")
    
    async def _test_health_check(self, agent):
        """Test health check"""
        test_name = "Health Check"
        try:
            health = await agent.health_check()
            
            required_fields = ["agent_id", "status", "intelligence_level", "features_upgraded"]
            missing_fields = [field for field in required_fields if field not in health]
            
            if not missing_fields and health.get("status") == "healthy":
                self._record_success(test_name, f"Health check OK - {len(health.get('features_upgraded', []))} features")
            else:
                self._record_failure(test_name, f"Champs manquants: {missing_fields}")
                
        except Exception as e:
            self._record_failure(test_name, f"Erreur health check: {e}")
    
    async def _test_capabilities(self, agent):
        """Test capacités agent"""
        test_name = "Capabilities Check"
        try:
            capabilities = agent.get_capabilities()
            
            expected_capabilities = [
                "evaluate_tools", "evaluate_single_tool", "detect_conflicts",
                "calculate_similarity", "multi_criteria_evaluation"
            ]
            
            missing_caps = [cap for cap in expected_capabilities if cap not in capabilities]
            
            if not missing_caps:
                self._record_success(test_name, f"{len(capabilities)} capacités disponibles")
            else:
                self._record_failure(test_name, f"Capacités manquantes: {missing_caps}")
                
        except Exception as e:
            self._record_failure(test_name, f"Erreur capacités: {e}")
    
    async def _test_multi_criteria_evaluation(self, agent):
        """Test système évaluation multi-critères"""
        test_name = "Multi-Criteria Evaluation"
        try:
            # Test évaluation outil unique
            tool = self.test_data_advanced["tools"][0]  # Agent orchestrator
            evaluation = await agent.evaluate_single_tool(tool)
            
            required_fields = ["weighted_score", "detailed_scores", "quality_level", "integration_priority"]
            missing_fields = [field for field in required_fields if field not in evaluation]
            
            # Vérifier 5 dimensions
            expected_dimensions = [
                "technical_relevance", "architecture_compatibility", "added_value",
                "integration_ease", "maintenance_burden"
            ]
            detailed_scores = evaluation.get("detailed_scores", {})
            missing_dimensions = [dim for dim in expected_dimensions if dim not in detailed_scores]
            
            if not missing_fields and not missing_dimensions:
                score = evaluation.get("weighted_score", 0)
                self._record_success(test_name, f"Évaluation multi-critères OK - Score: {score:.3f}")
            else:
                self._record_failure(test_name, f"Champs/dimensions manquants: {missing_fields + missing_dimensions}")
                
        except Exception as e:
            self._record_failure(test_name, f"Erreur évaluation multi-critères: {e}")
    
    async def _test_nextgen_keywords_detection(self, agent):
        """Test détection mots-clés NextGeneration"""
        test_name = "NextGen Keywords Detection"
        try:
            # Test avec outil high priority (agent, orchestrator, enterprise)
            high_priority_tool = self.test_data_advanced["tools"][0]
            evaluation_high = await agent.evaluate_single_tool(high_priority_tool)
            
            # Test avec outil low priority (gui, desktop, legacy)
            low_priority_tool = self.test_data_advanced["tools"][1]
            evaluation_low = await agent.evaluate_single_tool(low_priority_tool)
            
            score_high = evaluation_high.get("weighted_score", 0)
            score_low = evaluation_low.get("weighted_score", 0)
            
            # L'outil high priority devrait avoir un meilleur score
            if score_high > score_low:
                self._record_success(test_name, f"Détection keywords OK - High: {score_high:.3f} > Low: {score_low:.3f}")
            else:
                self._record_failure(test_name, f"Détection keywords échouée - High: {score_high:.3f} <= Low: {score_low:.3f}")
                
        except Exception as e:
            self._record_failure(test_name, f"Erreur détection keywords: {e}")
    
    async def _test_five_dimensions_evaluation(self, agent):
        """Test évaluation 5 dimensions"""
        test_name = "Five Dimensions Evaluation"
        try:
            tool = self.test_data_advanced["tools"][0]
            
            # Test chaque dimension individuellement
            technical_score = await agent.evaluate_technical_relevance(tool)
            architecture_score = await agent.evaluate_architecture_compatibility(tool)
            value_score = await agent.evaluate_added_value(tool)
            integration_score = await agent.evaluate_integration_ease(tool)
            maintenance_score = await agent.evaluate_maintenance_burden(tool)
            
            dimensions_scores = [
                technical_score, architecture_score, value_score,
                integration_score, maintenance_score
            ]
            
            # Vérifier que tous les scores sont dans [0, 1]
            valid_scores = all(0 <= score <= 1 for score in dimensions_scores)
            
            if valid_scores:
                avg_score = sum(dimensions_scores) / len(dimensions_scores)
                self._record_success(test_name, f"5 dimensions OK - Moyenne: {avg_score:.3f}")
            else:
                self._record_failure(test_name, f"Scores invalides: {dimensions_scores}")
                
        except Exception as e:
            self._record_failure(test_name, f"Erreur 5 dimensions: {e}")
    
    async def _test_conflict_detection(self, agent):
        """Test détection conflits et redondances"""
        test_name = "Conflict Detection"
        try:
            # Évaluer tous les outils
            evaluated_tools = []
            for tool in self.test_data_advanced["tools"]:
                evaluation = await agent.evaluate_single_tool(tool)
                evaluated_tools.append(evaluation)
            
            # Détecter conflits
            conflict_analysis = await agent.detect_conflicts_and_redundancies(evaluated_tools)
            
            required_fields = ["conflicts", "redundancies", "conflicted_tools", "total_issues"]
            missing_fields = [field for field in required_fields if field not in conflict_analysis]
            
            if not missing_fields:
                total_issues = conflict_analysis.get("total_issues", 0)
                self._record_success(test_name, f"Détection conflits OK - {total_issues} issues détectées")
            else:
                self._record_failure(test_name, f"Champs manquants: {missing_fields}")
                
        except Exception as e:
            self._record_failure(test_name, f"Erreur détection conflits: {e}")
    
    async def _test_similarity_algorithm(self, agent):
        """Test algorithme similarité"""
        test_name = "Similarity Algorithm"
        try:
            tool1 = {"tool_name": "monitoring_system_production", "detailed_scores": {"technical_relevance": 0.8}}
            tool2 = {"tool_name": "monitoring_system_backup", "detailed_scores": {"technical_relevance": 0.75}}
            tool3 = {"tool_name": "gui_desktop_app", "detailed_scores": {"technical_relevance": 0.3}}
            
            # Test similarité
            similarity_high = await agent.calculate_tool_similarity(tool1, tool2)  # Similaires
            similarity_low = await agent.calculate_tool_similarity(tool1, tool3)   # Différents
            
            # La similarité entre outils similaires devrait être plus élevée
            if similarity_high > similarity_low:
                self._record_success(test_name, f"Algorithme similarité OK - High: {similarity_high:.3f} > Low: {similarity_low:.3f}")
            else:
                self._record_failure(test_name, f"Algorithme similarité échoué - High: {similarity_high:.3f} <= Low: {similarity_low:.3f}")
                
        except Exception as e:
            self._record_failure(test_name, f"Erreur algorithme similarité: {e}")
    
    async def _test_intelligent_prioritization(self, agent):
        """Test priorisation intelligente"""
        test_name = "Intelligent Prioritization"
        try:
            # Test avec différents scores
            high_score_tool = {"weighted_score": 0.9}
            medium_score_tool = {"weighted_score": 0.7}
            low_score_tool = {"weighted_score": 0.4}
            
            priority_high = await agent.determine_integration_priority(0.9, high_score_tool)
            priority_medium = await agent.determine_integration_priority(0.7, medium_score_tool)
            priority_low = await agent.determine_integration_priority(0.4, low_score_tool)
            
            expected_priorities = ["CRITIQUE", "HAUTE", "FAIBLE"]
            actual_priorities = [priority_high, priority_medium, priority_low]
            
            if actual_priorities == expected_priorities:
                self._record_success(test_name, f"Priorisation OK - {actual_priorities}")
            else:
                self._record_failure(test_name, f"Priorisation incorrecte - Attendu: {expected_priorities}, Obtenu: {actual_priorities}")
                
        except Exception as e:
            self._record_failure(test_name, f"Erreur priorisation: {e}")
    
    async def _test_advanced_recommendations(self, agent):
        """Test génération recommandations avancées"""
        test_name = "Advanced Recommendations"
        try:
            scores = {
                "technical_relevance": 0.9,
                "architecture_compatibility": 0.8,
                "added_value": 0.7,
                "integration_ease": 0.6,
                "maintenance_burden": 0.5
            }
            tool = {"name": "test_tool"}
            
            recommendation = await agent.generate_recommendation_advanced(0.8, scores, tool)
            
            # Vérifier que la recommandation contient des éléments attendus
            expected_elements = ["EXCELLENT", "BON", "MOYEN", "FAIBLE"]
            has_quality_level = any(element in recommendation for element in expected_elements)
            
            if has_quality_level and len(recommendation) > 10:
                self._record_success(test_name, f"Recommandations OK - Longueur: {len(recommendation)}")
            else:
                self._record_failure(test_name, f"Recommandations insuffisantes: {recommendation}")
                
        except Exception as e:
            self._record_failure(test_name, f"Erreur recommandations: {e}")
    
    async def _test_complete_integration(self, agent):
        """Test intégration complète"""
        test_name = "Complete Integration"
        try:
            # Test évaluation complète avec toutes les fonctionnalités
            results = await agent.evaluate_tools_utility(self.test_data_advanced)
            
            required_fields = [
                "selected_tools", "rejected_tools", "conflicted_tools", 
                "evaluation_summary", "intelligence_level", "total_evaluated"
            ]
            missing_fields = [field for field in required_fields if field not in results]
            
            intelligence_level = results.get("intelligence_level")
            total_evaluated = results.get("total_evaluated", 0)
            
            if not missing_fields and intelligence_level == "multi_criteria_advanced" and total_evaluated > 0:
                self._record_success(test_name, f"Intégration complète OK - {total_evaluated} outils évalués")
            else:
                self._record_failure(test_name, f"Intégration incomplète - Champs manquants: {missing_fields}")
                
        except Exception as e:
            self._record_failure(test_name, f"Erreur intégration complète: {e}")
    
    def _record_success(self, test_name: str, details: str):
        """Enregistrer succès test"""
        self.results["tests_passed"] += 1
        self.results["tests_details"].append({
            "test": test_name,
            "status": "PASS",
            "details": details
        })
        print(f"✅ {test_name}: {details}")
    
    def _record_failure(self, test_name: str, details: str):
        """Enregistrer échec test"""
        self.results["tests_failed"] += 1
        self.results["tests_details"].append({
            "test": test_name,
            "status": "FAIL", 
            "details": details
        })
        print(f"❌ {test_name}: {details}")
    
    def _display_results(self):
        """Affichage résultats finaux"""
        print("\n" + "=" * 80)
        print("🎯 RÉSULTATS VALIDATION AGENT 02 UPGRADED")
        print("=" * 80)
        
        total_tests = self.results["tests_passed"] + self.results["tests_failed"]
        success_rate = (self.results["tests_passed"] / max(1, total_tests)) * 100
        
        print(f"📊 Tests exécutés: {total_tests}")
        print(f"✅ Tests réussis: {self.results['tests_passed']}")
        print(f"❌ Tests échoués: {self.results['tests_failed']}")
        print(f"🎯 Taux de réussite: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🏆 VALIDATION EXCELLENTE - Agent 02 UPGRADED opérationnel!")
        elif success_rate >= 75:
            print("✅ VALIDATION BONNE - Agent 02 UPGRADED fonctionnel avec améliorations mineures")
        elif success_rate >= 50:
            print("⚠️ VALIDATION PARTIELLE - Agent 02 UPGRADED nécessite corrections")
        else:
            print("❌ VALIDATION ÉCHOUÉE - Agent 02 UPGRADED nécessite révision majeure")
        
        print(f"\n📅 Rapport sauvegardé: validation_agent_02_upgraded_{self.timestamp}.json")
        
        # Sauvegarde rapport
        with open(f"validation_agent_02_upgraded_{self.timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

async def main():
    """Exécution validation complète"""
    validator = ValidationAgent02Upgraded()
    results = await validator.run_complete_validation()
    
    print(f"\n🎪 VALIDATION TERMINÉE - Consultez le rapport détaillé!")
    return results

if __name__ == "__main__":
    asyncio.run(main()) 




