#!/usr/bin/env python3
"""
Coordinateur d'équipe NextGeneration - Mission SuperWhisper Tools Integration
Orchestrateur autonome pour l'analyse et l'intégration d'outils externes

Équipe d'agents spécialisés :
- Agent 1 : Analyseur de structure (Claude Sonnet 4)
- Agent 2 : Évaluateur d'utilité (GPT-4 Turbo)  
- Agent 3 : Adaptateur de code (Claude Sonnet 4)
- Agent 4 : Testeur d'intégration (GPT-4 Turbo)
- Agent 5 : Documenteur (Gemini 2.0 Flash)
- Agent 6 : Validateur final (Claude Sonnet 4)
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Configuration des chemins
SOURCE_PATH = r"C:\Dev\SuperWhisper_V6\tools"
TARGET_PATH = "tools/imported_tools"
PROJECT_ROOT = Path(__file__).parent.absolute()

class CoordinateurEquipeTools:
    """Coordinateur principal pour la mission d'intégration des outils SuperWhisper"""
    
    def __init__(self):
        self.mission_start = datetime.now()
        self.mission_id = f"SUPERWHISPER_INTEGRATION_{self.mission_start.strftime('%Y%m%d_%H%M%S')}"
        self.agents_results = {}
        self.mission_metrics = {
            "tools_analyzed": 0,
            "tools_selected": 0,
            "tools_integrated": 0,
            "tools_tested": 0,
            "documentation_created": 0,
            "git_operations": 0,
            "total_duration": 0,
            "model_usage": {}
        }
        
        # Configuration logging
        self.setup_logging()
        
        # Vérification des prérequis
        self.verify_prerequisites()
        
    def setup_logging(self):
        """Configuration du système de logging"""
        log_dir = PROJECT_ROOT / "logs" / "tools_integration"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"{self.mission_id}.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger("CoordinateurEquipeTools")
        
    def verify_prerequisites(self):
        """Vérification des prérequis de la mission"""
        self.logger.info("🔍 Vérification des prérequis...")
        
        # Vérifier l'existence du répertoire source
        if not os.path.exists(SOURCE_PATH):
            raise FileNotFoundError(f"Répertoire source introuvable: {SOURCE_PATH}")
            
        # Créer le répertoire cible
        target_dir = PROJECT_ROOT / TARGET_PATH
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Vérifier Git
        try:
            subprocess.run(["git", "status"], capture_output=True, check=True)
            self.logger.info("✅ Git repository valide")
        except subprocess.CalledProcessError:
            self.logger.warning("⚠️ Pas de repository Git - opérations Git désactivées")
            
        self.logger.info("✅ Prérequis validés")
        
    def execute_mission(self):
        """Exécution de la mission complète"""
        self.logger.info(f"🚀 Démarrage mission {self.mission_id}")
        
        try:
            # Phase 1: Analyse de structure
            phase1_results = self.execute_phase_1()
            
            # Phase 2: Évaluation d'utilité
            phase2_results = self.execute_phase_2(phase1_results)
            
            # Phase 3: Adaptation de code
            phase3_results = self.execute_phase_3(phase2_results)
            
            # Phase 4: Tests d'intégration
            phase4_results = self.execute_phase_4(phase3_results)
            
            # Phase 5: Documentation
            phase5_results = self.execute_phase_5(phase4_results)
            
            # Phase 6: Validation finale
            phase6_results = self.execute_phase_6(phase5_results)
            
            # Génération du rapport final
            self.generate_mission_report()
            
            self.logger.info("✅ Mission terminée avec succès")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur mission: {e}")
            self.generate_error_report(str(e))
            raise
            
    def execute_phase_1(self) -> Dict[str, Any]:
        """Phase 1: Analyse de structure avec Agent Claude Sonnet 4"""
        self.logger.info("📊 Phase 1: Analyse de structure (Claude Sonnet 4)")
        
        from agent_1_analyseur_structure import AgentAnalyseurStructure
        
        agent = AgentAnalyseurStructure(SOURCE_PATH)
        start_time = time.time()
        
        results = agent.analyze_tools_structure()
        
        execution_time = time.time() - start_time
        self.mission_metrics["model_usage"]["claude_sonnet_4_phase1"] = execution_time
        self.mission_metrics["tools_analyzed"] = len(results.get("tools", []))
        
        self.agents_results["phase1"] = {
            "agent": "Agent 1 - Analyseur Structure",
            "model": "Claude Sonnet 4",
            "execution_time": execution_time,
            "results": results
        }
        
        self.logger.info(f"✅ Phase 1 terminée - {len(results.get('tools', []))} outils analysés")
        return results
        
    def execute_phase_2(self, phase1_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 2: Évaluation d'utilité avec Agent GPT-4 Turbo"""
        self.logger.info("🎯 Phase 2: Évaluation d'utilité (GPT-4 Turbo)")
        
        from agent_2_evaluateur_utilite import AgentEvaluateurUtilite
        
        agent = AgentEvaluateurUtilite()
        start_time = time.time()
        
        results = agent.evaluate_tools_utility(phase1_data)
        
        execution_time = time.time() - start_time
        self.mission_metrics["model_usage"]["gpt4_turbo_phase2"] = execution_time
        self.mission_metrics["tools_selected"] = len(results.get("selected_tools", []))
        
        self.agents_results["phase2"] = {
            "agent": "Agent 2 - Évaluateur Utilité",
            "model": "GPT-4 Turbo",
            "execution_time": execution_time,
            "results": results
        }
        
        self.logger.info(f"✅ Phase 2 terminée - {len(results.get('selected_tools', []))} outils sélectionnés")
        return results
        
    def execute_phase_3(self, phase2_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: Adaptation de code avec Agent Claude Sonnet 4"""
        self.logger.info("🔧 Phase 3: Adaptation de code (Claude Sonnet 4)")
        
        from agent_3_adaptateur_code import AgentAdaptateurCode
        
        agent = AgentAdaptateurCode(SOURCE_PATH, TARGET_PATH)
        start_time = time.time()
        
        results = agent.adapt_selected_tools(phase2_data)
        
        execution_time = time.time() - start_time
        self.mission_metrics["model_usage"]["claude_sonnet_4_phase3"] = execution_time
        self.mission_metrics["tools_integrated"] = len(results.get("adapted_tools", []))
        
        self.agents_results["phase3"] = {
            "agent": "Agent 3 - Adaptateur Code",
            "model": "Claude Sonnet 4",
            "execution_time": execution_time,
            "results": results
        }
        
        self.logger.info(f"✅ Phase 3 terminée - {len(results.get('adapted_tools', []))} outils adaptés")
        return results
        
    def execute_phase_4(self, phase3_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 4: Tests d'intégration avec Agent GPT-4 Turbo"""
        self.logger.info("🧪 Phase 4: Tests d'intégration (GPT-4 Turbo)")
        
        from agent_4_testeur_integration import AgentTesteurIntegration
        
        agent = AgentTesteurIntegration(TARGET_PATH)
        start_time = time.time()
        
        results = agent.test_integrated_tools(phase3_data)
        
        execution_time = time.time() - start_time
        self.mission_metrics["model_usage"]["gpt4_turbo_phase4"] = execution_time
        self.mission_metrics["tools_tested"] = len(results.get("tested_tools", []))
        
        self.agents_results["phase4"] = {
            "agent": "Agent 4 - Testeur Intégration",
            "model": "GPT-4 Turbo",
            "execution_time": execution_time,
            "results": results
        }
        
        self.logger.info(f"✅ Phase 4 terminée - {len(results.get('tested_tools', []))} outils testés")
        return results
        
    def execute_phase_5(self, phase4_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 5: Documentation avec Agent Gemini 2.0 Flash"""
        self.logger.info("📚 Phase 5: Documentation (Gemini 2.0 Flash)")
        
        from agent_5_documenteur import AgentDocumenteur
        
        agent = AgentDocumenteur(TARGET_PATH)
        start_time = time.time()
        
        results = agent.generate_documentation(phase4_data)
        
        execution_time = time.time() - start_time
        self.mission_metrics["model_usage"]["gemini_2_flash_phase5"] = execution_time
        self.mission_metrics["documentation_created"] = len(results.get("documentation_files", []))
        
        self.agents_results["phase5"] = {
            "agent": "Agent 5 - Documenteur",
            "model": "Gemini 2.0 Flash",
            "execution_time": execution_time,
            "results": results
        }
        
        self.logger.info(f"✅ Phase 5 terminée - {len(results.get('documentation_files', []))} docs créées")
        return results
        
    def execute_phase_6(self, phase5_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 6: Validation finale avec Agent Claude Sonnet 4"""
        self.logger.info("✅ Phase 6: Validation finale (Claude Sonnet 4)")
        
        from agent_6_validateur_final import AgentValidateurFinal
        
        agent = AgentValidateurFinal(TARGET_PATH)
        start_time = time.time()
        
        results = agent.validate_and_commit(phase5_data, self.mission_metrics)
        
        execution_time = time.time() - start_time
        self.mission_metrics["model_usage"]["claude_sonnet_4_phase6"] = execution_time
        self.mission_metrics["git_operations"] = results.get("git_operations", 0)
        
        self.agents_results["phase6"] = {
            "agent": "Agent 6 - Validateur Final",
            "model": "Claude Sonnet 4",
            "execution_time": execution_time,
            "results": results
        }
        
        self.logger.info("✅ Phase 6 terminée - Validation et Git effectués")
        return results
        
    def generate_mission_report(self):
        """Génération du rapport de mission final"""
        self.mission_metrics["total_duration"] = (datetime.now() - self.mission_start).total_seconds()
        
        report = {
            "mission_id": self.mission_id,
            "timestamp": self.mission_start.isoformat(),
            "duration_seconds": self.mission_metrics["total_duration"],
            "source_path": SOURCE_PATH,
            "target_path": TARGET_PATH,
            "metrics": self.mission_metrics,
            "agents_results": self.agents_results,
            "success": True
        }
        
        # Sauvegarde du rapport
        reports_dir = PROJECT_ROOT / "reports" / "tools_integration"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = reports_dir / f"{self.mission_id}_FINAL_REPORT.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"📋 Rapport final généré: {report_file}")
        
    def generate_error_report(self, error_message: str):
        """Génération du rapport d'erreur"""
        error_report = {
            "mission_id": self.mission_id,
            "timestamp": self.mission_start.isoformat(),
            "error": error_message,
            "partial_results": self.agents_results,
            "success": False
        }
        
        reports_dir = PROJECT_ROOT / "reports" / "tools_integration"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        error_file = reports_dir / f"{self.mission_id}_ERROR_REPORT.json"
        with open(error_file, 'w', encoding='utf-8') as f:
            json.dump(error_report, f, indent=2, ensure_ascii=False)
            
        self.logger.error(f"📋 Rapport d'erreur généré: {error_file}")

def main():
    """Point d'entrée principal"""
    try:
        coordinateur = CoordinateurEquipeTools()
        coordinateur.execute_mission()
        print("🎉 Mission SuperWhisper Tools Integration terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mission: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 