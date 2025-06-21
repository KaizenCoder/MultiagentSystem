#!/usr/bin/env python3
"""
Coordinateur quipe Tools - Apex_VBA_FRAMEWORK
Partie du systme NextGeneration - Orchestrateur d'agents pour importation d'outils

Mission: Analyser et importer les outils utiles depuis Apex_VBA_FRAMEWORK
quipe: 6 agents spcialiss avec modles cloud (Claude, GPT-4, Gemini)
"""

import os
import sys
import json
import sys
from pathlib import Path
from core import logging_manager
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import subprocess

# Configuration NextGeneration
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR
while not (PROJECT_ROOT / ".git").exists() and PROJECT_ROOT.parent != PROJECT_ROOT:
    PROJECT_ROOT = PROJECT_ROOT.parent

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(PROJECT_ROOT / "logs" / "tools_integration" / "coordinateur_apex.log"),
        logging.StreamHandler()
    ]
)

class CoordinateurEquipeToolsApex:
    """Coordinateur pour l'quipe d'agents d'importation d'outils Apex_VBA_FRAMEWORK"""
    
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.source_dir = Path("G:/Dev/Apex_VBA_FRAMEWORK/tools")
        self.target_dir = self.project_root / "tools" / "excel_vba_tools_launcher"
        self.logs_dir = self.project_root / "logs" / "tools_integration"
        self.reports_dir = self.project_root / "reports" / "tools_integration"
        
        # Crer les rpertoires ncessaires
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # LoggingManager NextGeneration - Tool/Utility
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = logging_manager.get_logger(custom_config={
            "logger_name": "CoordinateurEquipeToolsApex",
            "log_level": "INFO",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": True
        })
        self.mission_id = f"APEX_INTEGRATION_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Mtriques de mission
        self.mission_metrics = {
            "mission_id": self.mission_id,
            "start_time": datetime.now().isoformat(),
            "source_directory": str(self.source_dir),
            "target_directory": str(self.target_dir),
            "phases_completed": 0,
            "total_phases": 6,
            "agents_deployed": 0,
            "tools_analysed": 0,
            "tools_selected": 0,
            "tools_adapted": 0,
            "tools_tested": 0,
            "docs_created": 0,
            "git_operations": False,
            "status": "in_progress"
        }
    
    def verifier_prerequis(self) -> bool:
        """Vrification des prrequis avant dmarrage"""
        self.logger.info("[SEARCH] Vrification des prrequis...")
        
        # Vrifier que le rpertoire source existe
        if not self.source_dir.exists():
            self.logger.error(f"[CROSS] Rpertoire source introuvable: {self.source_dir}")
            return False
        
        # Vrifier Git
        try:
            result = subprocess.run(["git", "status"], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                self.logger.info("[CHECK] Git repository valide")
            else:
                self.logger.warning(" Git repository invalide")
        except Exception as e:
            self.logger.warning(f" Git non disponible: {e}")
        
        self.logger.info("[CHECK] Prrequis valids")
        return True
    
    def phase1_analyse_structure(self) -> Dict[str, Any]:
        """Phase 1: Analyse de structure avec Agent 1 (Claude Sonnet 4)"""
        self.logger.info("[CHART] Phase 1: Analyse de structure (Claude Sonnet 4)")
        
        try:
            from agent_1_analyseur_structure import AgentAnalyseurStructure
            agent = AgentAnalyseurStructure(str(self.source_dir))
            
            # Analyser spcifiquement les outils Apex_VBA_FRAMEWORK
            resultats = agent.analyser_structure_apex(str(self.source_dir))
            
            # Mettre  jour les mtriques
            self.mission_metrics["tools_analysed"] = resultats.get("total_tools", 0)
            self.mission_metrics["phases_completed"] = 1
            self.mission_metrics["agents_deployed"] += 1
            
            self.logger.info(f"[CHECK] Phase 1 termine - {resultats.get('total_tools', 0)} outils analyss")
            return resultats
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur Phase 1: {e}")
            raise
    
    def phase2_evaluation_utilite(self, phase1_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 2: valuation d'utilit avec Agent 2 (GPT-4 Turbo)"""
        self.logger.info("[TARGET] Phase 2: valuation d'utilit (GPT-4 Turbo)")
        
        try:
            from agent_2_evaluateur_utilite import AgentEvaluateurUtilite
            agent = AgentEvaluateurUtilite()
            
            # valuer les outils Apex_VBA_FRAMEWORK pour NextGeneration
            resultats = agent.evaluer_outils_apex(phase1_data)
            
            # Mettre  jour les mtriques
            self.mission_metrics["tools_selected"] = len(resultats.get("outils_selectionnes", []))
            self.mission_metrics["phases_completed"] = 2
            self.mission_metrics["agents_deployed"] += 1
            
            self.logger.info(f"[CHECK] Phase 2 termine - {len(resultats.get('outils_selectionnes', []))} outils slectionns")
            return resultats
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur Phase 2: {e}")
            raise
    
    def phase3_adaptation_code(self, phase2_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: Adaptation de code avec Agent 3 (Claude Sonnet 4)"""
        self.logger.info("[TOOL] Phase 3: Adaptation de code (Claude Sonnet 4)")
        
        try:
            from agent_3_adaptateur_code import AgentAdaptateurCode
            agent = AgentAdaptateurCode(str(self.source_dir), str(self.target_dir))
            
            # Adapter les outils slectionns pour NextGeneration
            resultats = agent.adapter_outils_apex(phase2_data)
            
            # Mettre  jour les mtriques
            self.mission_metrics["tools_adapted"] = len(resultats.get("outils_adaptes", []))
            self.mission_metrics["phases_completed"] = 3
            self.mission_metrics["agents_deployed"] += 1
            
            self.logger.info(f"[CHECK] Phase 3 termine - {len(resultats.get('outils_adaptes', []))} outils adapts")
            return resultats
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur Phase 3: {e}")
            raise
    
    def phase4_tests_integration(self, phase3_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 4: Tests d'intgration avec Agent 4 (GPT-4 Turbo)"""
        self.logger.info(" Phase 4: Tests d'intgration (GPT-4 Turbo)")
        
        try:
            from agent_4_testeur_integration import AgentTesteurIntegration
            agent = AgentTesteurIntegration(str(self.target_dir))
            
            # Tester l'intgration des outils adapts
            resultats = agent.tester_integration_apex(phase3_data)
            
            # Mettre  jour les mtriques
            self.mission_metrics["tools_tested"] = len(resultats.get("outils_testes", []))
            self.mission_metrics["phases_completed"] = 4
            self.mission_metrics["agents_deployed"] += 1
            
            self.logger.info(f"[CHECK] Phase 4 termine - {len(resultats.get('outils_testes', []))} outils tests")
            return resultats
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur Phase 4: {e}")
            raise
    
    def phase5_documentation(self, phase4_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 5: Documentation avec Agent 5 (Gemini 2.0 Flash)"""
        self.logger.info(" Phase 5: Documentation (Gemini 2.0 Flash)")
        
        try:
            from agent_5_documenteur import AgentDocumenteur
            agent = AgentDocumenteur(str(self.target_dir))
            
            # Gnrer la documentation pour les outils Apex
            resultats = agent.generer_documentation_apex(phase4_data)
            
            # Mettre  jour les mtriques
            self.mission_metrics["docs_created"] = len(resultats.get("docs_generees", []))
            self.mission_metrics["phases_completed"] = 5
            self.mission_metrics["agents_deployed"] += 1
            
            self.logger.info(f"[CHECK] Phase 5 termine - {len(resultats.get('docs_generees', []))} docs cres")
            return resultats
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur Phase 5: {e}")
            raise
    
    def phase6_validation_finale(self, phase5_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 6: Validation finale avec Agent 6 (Claude Sonnet 4)"""
        self.logger.info("[CHECK] Phase 6: Validation finale (Claude Sonnet 4)")
        
        try:
            from agent_6_validateur_final import AgentValidateurFinal
            agent = AgentValidateurFinal(str(self.target_dir))
            
            # Validation finale et oprations Git
            resultats = agent.validate_and_commit(phase5_data, self.mission_metrics)
            
            # Mettre  jour les mtriques
            self.mission_metrics["git_operations"] = resultats.get("git_success", False)
            self.mission_metrics["phases_completed"] = 6
            self.mission_metrics["agents_deployed"] += 1
            
            self.logger.info("[CHECK] Phase 6 termine - Validation et Git effectus")
            return resultats
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur Phase 6: {e}")
            raise
    
    def generer_rapport_final(self) -> str:
        """Gnration du rapport final de mission"""
        self.mission_metrics["end_time"] = datetime.now().isoformat()
        self.mission_metrics["status"] = "completed"
        
        # Calculer la dure
        start_time = datetime.fromisoformat(self.mission_metrics["start_time"])
        end_time = datetime.fromisoformat(self.mission_metrics["end_time"])
        duration = (end_time - start_time).total_seconds()
        self.mission_metrics["duration_seconds"] = duration
        
        # Fichier de rapport
        rapport_file = self.reports_dir / f"{self.mission_id}_FINAL_REPORT.json"
        
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(self.mission_metrics, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"[CLIPBOARD] Rapport final gnr: {rapport_file}")
        return str(rapport_file)
    
    def executer_mission(self) -> bool:
        """Excution complte de la mission d'importation d'outils Apex_VBA_FRAMEWORK"""
        try:
            self.logger.info(f"[ROCKET] Dmarrage mission {self.mission_id}")
            
            # Vrification prrequis
            if not self.verifier_prerequis():
                return False
            
            # Excution des phases
            phase1_data = self.phase1_analyse_structure()
            phase2_data = self.phase2_evaluation_utilite(phase1_data)
            phase3_data = self.phase3_adaptation_code(phase2_data)
            phase4_data = self.phase4_tests_integration(phase3_data)
            phase5_data = self.phase5_documentation(phase4_data)
            phase6_data = self.phase6_validation_finale(phase5_data)
            
            # Rapport final
            self.generer_rapport_final()
            
            self.logger.info("[CHECK] Mission termine avec succs")
            return True
            
        except Exception as e:
            self.logger.error(f"[CROSS] chec mission: {e}")
            self.mission_metrics["status"] = "failed"
            self.mission_metrics["error"] = str(e)
            self.generer_rapport_final()
            return False

def main():
    """Point d'entre principal"""
    parser = argparse.ArgumentParser(description="Coordinateur quipe Tools - Apex_VBA_FRAMEWORK")
    parser.add_argument("--verbose", action="store_true", help="Logs dtaills")
    parser.add_argument("--dry-run", action="store_true", help="Simulation sans modifications")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Excution de la mission
    coordinateur = CoordinateurEquipeToolsApex()
    success = coordinateur.executer_mission()
    
    if success:
        print(f" Mission Apex_VBA_FRAMEWORK Tools Integration termine avec succs!")
        return 0
    else:
        print(f"[CROSS] chec de la mission Apex_VBA_FRAMEWORK Tools Integration")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 



