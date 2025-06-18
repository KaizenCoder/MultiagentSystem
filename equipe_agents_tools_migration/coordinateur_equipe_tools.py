#!/usr/bin/env python3
"""
[TARGET] Coordinateur quipe Tools Migration - NextGeneration
Mission: Analyser, copier et adapter les outils de SuperWhisper_V6 vers NextGeneration

quipe d'agents spcialiss:
- Agent 1: Analyseur de Structure (Claude Sonnet 4)
- Agent 2: valuateur d'Utilit (GPT-4 Turbo)
- Agent 3: Adaptateur de Code (Claude Sonnet 4)
- Agent 4: Testeur d'Intgration (GPT-4 Turbo)
- Agent 5: Documenteur (Gemini 2.0 Flash)
- Agent 6: Validateur Final (Claude Sonnet 4)

Date: 18 juin 2025
Modles: Cloud uniquement (Claude, GPT-4, Gemini)
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess
import shutil
import os

class CoordinateurEquipeTools:
    """Coordinateur pour l'quipe de migration des outils"""
    
    def __init__(self):
        self.workspace_path = Path(__file__).parent
        self.source_path = Path("C:/Dev/SuperWhisper_V6/tools")
        self.target_path = Path(__file__).parent.parent / "tools"
        self.logs_path = self.workspace_path / "logs"
        self.reports_path = self.workspace_path / "reports"
        
        # Crer les rpertoires ncessaires
        self.logs_path.mkdir(exist_ok=True)
        self.reports_path.mkdir(exist_ok=True)
        
        # Configuration logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.logs_path / 'coordinateur_tools.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Mtriques de mission
        self.mission_start_time = None
        self.mission_end_time = None
        self.agents_results = {}
        self.tools_analyzed = 0
        self.tools_copied = 0
        self.tools_adapted = 0
        
    async def demarrer_mission(self):
        """Dmarrer la mission de migration des outils"""
        self.mission_start_time = datetime.now()
        self.logger.info("[ROCKET] DMARRAGE MISSION TOOLS MIGRATION")
        
        try:
            # Phase 1: Analyse de structure
            self.logger.info("[CHART] Phase 1: Analyse de structure")
            await self._executer_agent_1_analyseur()
            
            # Phase 2: valuation d'utilit
            self.logger.info("[SEARCH] Phase 2: valuation d'utilit")
            await self._executer_agent_2_evaluateur()
            
            # Phase 3: Adaptation de code
            self.logger.info("[TOOL] Phase 3: Adaptation de code")
            await self._executer_agent_3_adaptateur()
            
            # Phase 4: Tests d'intgration
            self.logger.info(" Phase 4: Tests d'intgration")
            await self._executer_agent_4_testeur()
            
            # Phase 5: Documentation
            self.logger.info(" Phase 5: Documentation")
            await self._executer_agent_5_documenteur()
            
            # Phase 6: Validation finale
            self.logger.info("[CHECK] Phase 6: Validation finale")
            await self._executer_agent_6_validateur()
            
            # Gnration du rapport final
            await self._generer_rapport_final()
            
            # Commit et push si succs
            if self._mission_reussie():
                await self._commit_et_push()
            
            self.mission_end_time = datetime.now()
            self.logger.info("[TARGET] MISSION TERMINE AVEC SUCCS")
            
        except Exception as e:
            self.logger.error(f"[CROSS] ERREUR MISSION: {e}")
            raise
    
    async def _executer_agent_1_analyseur(self):
        """Agent 1: Analyseur de Structure (Claude Sonnet 4)"""
        from .agent_1_analyseur_structure import Agent1AnalyseurStructure
        
        agent = Agent1AnalyseurStructure(
            source_path=self.source_path,
            workspace_path=self.workspace_path
        )
        
        result = await agent.analyser_structure()
        self.agents_results['agent_1'] = result
        self.tools_analyzed = result.get('tools_count', 0)
        
        self.logger.info(f"[CHECK] Agent 1 termin: {self.tools_analyzed} outils analyss")
    
    async def _executer_agent_2_evaluateur(self):
        """Agent 2: valuateur d'Utilit (GPT-4 Turbo)"""
        from .agent_2_evaluateur_utilite import Agent2EvaluateurUtilite
        
        agent = Agent2EvaluateurUtilite(
            analyse_structure=self.agents_results['agent_1'],
            workspace_path=self.workspace_path
        )
        
        result = await agent.evaluer_utilite()
        self.agents_results['agent_2'] = result
        
        self.logger.info(f"[CHECK] Agent 2 termin: {len(result.get('outils_utiles', []))} outils slectionns")
    
    async def _executer_agent_3_adaptateur(self):
        """Agent 3: Adaptateur de Code (Claude Sonnet 4)"""
        from .agent_3_adaptateur_code import Agent3AdaptateurCode
        
        agent = Agent3AdaptateurCode(
            outils_selectionnes=self.agents_results['agent_2']['outils_utiles'],
            source_path=self.source_path,
            target_path=self.target_path,
            workspace_path=self.workspace_path
        )
        
        result = await agent.adapter_outils()
        self.agents_results['agent_3'] = result
        self.tools_copied = result.get('tools_copied', 0)
        self.tools_adapted = result.get('tools_adapted', 0)
        
        self.logger.info(f"[CHECK] Agent 3 termin: {self.tools_copied} copis, {self.tools_adapted} adapts")
    
    async def _executer_agent_4_testeur(self):
        """Agent 4: Testeur d'Intgration (GPT-4 Turbo)"""
        from .agent_4_testeur_integration import Agent4TesteurIntegration
        
        agent = Agent4TesteurIntegration(
            outils_adaptes=self.agents_results['agent_3']['outils_adaptes'],
            target_path=self.target_path,
            workspace_path=self.workspace_path
        )
        
        result = await agent.tester_integration()
        self.agents_results['agent_4'] = result
        
        self.logger.info(f"[CHECK] Agent 4 termin: {result.get('tests_passed', 0)} tests russis")
    
    async def _executer_agent_5_documenteur(self):
        """Agent 5: Documenteur (Gemini 2.0 Flash)"""
        from .agent_5_documenteur import Agent5Documenteur
        
        agent = Agent5Documenteur(
            outils_finalises=self.agents_results['agent_4']['outils_valides'],
            target_path=self.target_path,
            workspace_path=self.workspace_path
        )
        
        result = await agent.documenter_outils()
        self.agents_results['agent_5'] = result
        
        self.logger.info(f"[CHECK] Agent 5 termin: {result.get('docs_created', 0)} documentations cres")
    
    async def _executer_agent_6_validateur(self):
        """Agent 6: Validateur Final (Claude Sonnet 4)"""
        from .agent_6_validateur_final import Agent6ValidateurFinal
        
        agent = Agent6ValidateurFinal(
            resultats_equipe=self.agents_results,
            target_path=self.target_path,
            workspace_path=self.workspace_path
        )
        
        result = await agent.valider_mission()
        self.agents_results['agent_6'] = result
        
        self.logger.info(f"[CHECK] Agent 6 termin: Mission {result.get('status', 'UNKNOWN')}")
    
    async def _generer_rapport_final(self):
        """Gnrer le rapport final de mission"""
        duree_mission = (self.mission_end_time or datetime.now()) - self.mission_start_time
        
        rapport = {
            "mission": "Tools Migration SuperWhisper_V6  NextGeneration",
            "date": self.mission_start_time.isoformat(),
            "duree_mission": str(duree_mission),
            "duree_secondes": duree_mission.total_seconds(),
            "equipe_agents": [
                {"agent": "Agent 1", "modele": "Claude Sonnet 4", "role": "Analyseur Structure"},
                {"agent": "Agent 2", "modele": "GPT-4 Turbo", "role": "valuateur Utilit"},
                {"agent": "Agent 3", "modele": "Claude Sonnet 4", "role": "Adaptateur Code"},
                {"agent": "Agent 4", "modele": "GPT-4 Turbo", "role": "Testeur Intgration"},
                {"agent": "Agent 5", "modele": "Gemini 2.0 Flash", "role": "Documenteur"},
                {"agent": "Agent 6", "modele": "Claude Sonnet 4", "role": "Validateur Final"}
            ],
            "metriques": {
                "outils_analyses": self.tools_analyzed,
                "outils_copies": self.tools_copied,
                "outils_adaptes": self.tools_adapted,
                "source_path": str(self.source_path),
                "target_path": str(self.target_path)
            },
            "resultats_agents": self.agents_results,
            "mission_reussie": self._mission_reussie(),
            "recommendations": self._generer_recommendations()
        }
        
        # Sauvegarder le rapport
        rapport_path = self.reports_path / f"rapport_mission_tools_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(rapport_path, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"[DOCUMENT] Rapport final gnr: {rapport_path}")
        return rapport
    
    def _mission_reussie(self) -> bool:
        """Vrifier si la mission est russie"""
        return (
            self.agents_results.get('agent_6', {}).get('status') == 'SUCCESS' and
            self.tools_copied > 0 and
            self.tools_adapted > 0
        )
    
    def _generer_recommendations(self) -> List[str]:
        """Gnrer des recommandations bases sur les rsultats"""
        recommendations = []
        
        if self.tools_copied == 0:
            recommendations.append("Aucun outil copi - Vrifier les critres de slection")
        
        if self.tools_adapted < self.tools_copied:
            recommendations.append("Certains outils non adapts - Vrifier les erreurs d'adaptation")
        
        if not self._mission_reussie():
            recommendations.append("Mission non russie - Analyser les logs d'erreur")
        
        return recommendations
    
    async def _commit_et_push(self):
        """Commit et push des changements si la mission est russie"""
        try:
            # Git add
            subprocess.run(['git', 'add', '.'], check=True, cwd=Path(__file__).parent.parent)
            
            # Git commit
            commit_message = f" Migration Outils SuperWhisper_V6  NextGeneration - {self.tools_copied} outils copis, {self.tools_adapted} adapts - Mission russie par quipe d'agents cloud"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True, cwd=Path(__file__).parent.parent)
            
            # Git push
            subprocess.run(['git', 'push'], check=True, cwd=Path(__file__).parent.parent)
            
            self.logger.info("[CHECK] Commit et push GitHub russis")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"[CROSS] Erreur commit/push: {e}")

# Point d'entre
if __name__ == "__main__":
    async def main():
        coordinateur = CoordinateurEquipeTools()
        await coordinateur.demarrer_mission()
    
    asyncio.run(main()) 