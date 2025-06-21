#!/usr/bin/env python3
"""
[TARGET] Orchestrateur Phase 1 - Analyse Parallle Cloud
[ROBOT] Coordination: Agent Alpha (Claude Sonnet 4) + Agent Beta (Gemini 2.5)
[LIGHTNING] Phase 1 Refactoring NextGeneration - Cloud APIs
"""

import os
import json
import asyncio
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

# Import des agents cloud
from agent_analyzer_alpha_claude_sonnet4 import AgentAnalyzerAlphaClaudeSonnet4
from agent_analyzer_beta_gemini25 import AgentAnalyzerBetaGemini25

@dataclass
class PhaseResults:
    """Rsultats consolids Phase 1"""
    alpha_results: Dict[str, Any]
    beta_results: Dict[str, Any]
    consolidated_analysis: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    next_steps: List[str]

class OrchestratorPhase1AnalysisCloud:
    """
    [TARGET] Orchestrateur Phase 1 - Analyse Parallle Cloud
    
    Mission:
    - Coordination excution parallle Agent Alpha + Beta
    - Validation environnement cloud
    - Consolidation des rsultats croiss
    - Gnration recommandations Phase 2
    """
    
    def __init__(self):
        self.name = "Orchestrateur Phase 1 - Cloud Analysis"
        self.phase = "PHASE_1_ANALYSIS"
        self.models = {
            "alpha": "Claude Sonnet 4",
            "beta": "Gemini 2.5"
        }
        
        # Agents cloud
        self.agent_alpha = None
        self.agent_beta = None
        
        # Configuration
        self.workspace = Path("refactoring_workspace")
        self.results_dir = self.workspace / "results" / "phase1_cloud"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Fichiers god mode  analyser
        self.target_files = [
            "orchestrator/app/main.py",
            "orchestrator/app/agents/advanced_coordination.py", 
            "orchestrator/app/performance/redis_cluster_manager.py",
            "orchestrator/app/observability/monitoring.py"
        ]
        
        print(f" {self.name} initialis")
        print(f"[ROBOT] Modles: Alpha={self.models['alpha']}, Beta={self.models['beta']}")
        print(f"[FOLDER] Workspace: {self.workspace}")

    async def validate_cloud_environment(self) -> bool:
        """
        [SEARCH] Validation de l'environnement cloud
        """
        print("\n[SEARCH] Validation environnement cloud...")
        
        try:
            # Vrification cls API
            api_keys = {
                "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
                "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY")
            }
            
            missing_keys = [key for key, value in api_keys.items() if not value]
            
            if missing_keys:
                print(f"[CROSS] Cls API manquantes: {', '.join(missing_keys)}")
                print("[BULB] Configurez les variables d'environnement:")
                for key in missing_keys:
                    print(f"   export {key}=votre_cl_api")
                return False
            
            print("[CHECK] Cls API configures")
            
            # Vrification fichiers cibles
            missing_files = [f for f in self.target_files if not os.path.exists(f)]
            
            if missing_files:
                print(f"[CROSS] Fichiers manquants: {missing_files}")
                return False
            
            print(f"[CHECK] {len(self.target_files)} fichiers cibles trouvs")
            
            # Initialisation des agents
            try:
                self.agent_alpha = AgentAnalyzerAlphaClaudeSonnet4()
                self.agent_beta = AgentAnalyzerBetaGemini25()
                print("[CHECK] Agents cloud initialiss")
                
                return True
                
            except Exception as e:
                print(f"[CROSS] Erreur initialisation agents: {str(e)}")
                return False
                
        except Exception as e:
            print(f"[CROSS] Erreur validation environnement: {str(e)}")
            return False

    async def execute_parallel_analysis(self) -> PhaseResults:
        """
        [ROCKET] Excution analyse parallle Alpha + Beta
        """
        print(f"\n[ROCKET] Dmarrage analyse parallle - {len(self.target_files)} fichiers")
        
        start_time = time.time()
        alpha_results = {}
        beta_results = {}
        
        try:
            # Excution parallle pour chaque fichier
            for file_path in self.target_files:
                print(f"\n[CHART] Analyse parallle: {file_path}")
                
                # Lancement simultan Alpha + Beta
                alpha_task = asyncio.create_task(
                    self.agent_alpha.analyze_file_deep(file_path)
                )
                beta_task = asyncio.create_task(
                    self.agent_beta.analyze_file_fast(file_path)
                )
                
                # Attente rsultats parallles
                alpha_result, beta_result = await asyncio.gather(
                    alpha_task, beta_task, return_exceptions=True
                )
                
                # Gestion des erreurs
                if isinstance(alpha_result, Exception):
                    print(f" Erreur Agent Alpha: {str(alpha_result)}")
                    alpha_result = {"error": str(alpha_result), "file_path": file_path}
                
                if isinstance(beta_result, Exception):
                    print(f" Erreur Agent Beta: {str(beta_result)}")
                    beta_result = {"error": str(beta_result), "file_path": file_path}
                
                alpha_results[file_path] = alpha_result
                beta_results[file_path] = beta_result
                
                print(f"[CHECK] Analyse termine: {file_path}")
            
            # Consolidation des rsultats
            consolidated = await self._consolidate_results(alpha_results, beta_results)
            
            # Gnration recommandations
            recommendations = await self._generate_recommendations(consolidated)
            
            # Prochaines tapes
            next_steps = self._generate_next_steps(consolidated, recommendations)
            
            execution_time = time.time() - start_time
            print(f"\n[TARGET] Phase 1 termine en {execution_time:.2f}s")
            
            results = PhaseResults(
                alpha_results=alpha_results,
                beta_results=beta_results,
                consolidated_analysis=consolidated,
                recommendations=recommendations,
                next_steps=next_steps
            )
            
            # Sauvegarde des rsultats
            await self._save_results(results)
            
            return results
            
        except Exception as e:
            print(f"[CROSS] Erreur analyse parallle: {str(e)}")
            raise

    async def _consolidate_results(self, alpha_results: Dict, beta_results: Dict) -> Dict[str, Any]:
        """
         Consolidation des rsultats Alpha + Beta
        """
        print("\n Consolidation des analyses...")
        
        consolidated = {
            "timestamp": datetime.now().isoformat(),
            "agents": {
                "alpha": self.models["alpha"],
                "beta": self.models["beta"]
            },
            "files_analyzed": len(self.target_files),
            "cross_analysis": {}
        }
        
        for file_path in self.target_files:
            alpha_data = alpha_results.get(file_path, {})
            beta_data = beta_results.get(file_path, {})
            
            # Consolidation par fichier
            file_analysis = {
                "file_path": file_path,
                "alpha_insights": {
                    "complexity_level": alpha_data.get("summary", {}).get("complexity_level", "UNKNOWN"),
                    "god_class_score": alpha_data.get("summary", {}).get("god_class_score", 0),
                    "recommendations_count": len(alpha_data.get("recommendations", []))
                },
                "beta_insights": {
                    "refactoring_urgency": beta_data.get("summary", {}).get("refactoring_urgency", "UNKNOWN"),
                    "critical_functions": beta_data.get("summary", {}).get("critical_functions", 0),
                    "quick_wins": beta_data.get("summary", {}).get("quick_wins", 0)
                },
                "consensus": self._build_consensus(alpha_data, beta_data)
            }
            
            consolidated["cross_analysis"][file_path] = file_analysis
        
        return consolidated

    def _build_consensus(self, alpha_data: Dict, beta_data: Dict) -> Dict[str, Any]:
        """
         Construction du consensus Alpha + Beta
        """
        alpha_summary = alpha_data.get("summary", {})
        beta_summary = beta_data.get("summary", {})
        
        # Priorit consensus
        alpha_priority = alpha_summary.get("refactoring_priority", "FAIBLE")
        beta_urgency = beta_summary.get("refactoring_urgency", "FAIBLE")
        
        priority_scores = {"FAIBLE": 1, "MODRE": 2, "LEVE": 3, "CRITIQUE": 4}
        consensus_score = max(
            priority_scores.get(alpha_priority, 1),
            priority_scores.get(beta_urgency, 1)
        )
        
        consensus_priority = {v: k for k, v in priority_scores.items()}[consensus_score]
        
        # Effort consensus
        alpha_effort = alpha_summary.get("estimated_effort", "2-8 heures")
        beta_quick_wins = beta_summary.get("quick_wins", 0)
        
        return {
            "priority": consensus_priority,
            "confidence": "HIGH" if alpha_data and beta_data else "LOW",
            "effort_estimate": alpha_effort,
            "quick_wins_available": beta_quick_wins > 0,
            "action_recommended": consensus_score >= 3
        }

    async def _generate_recommendations(self, consolidated: Dict) -> List[Dict[str, Any]]:
        """
        [BULB] Gnration des recommandations consolides
        """
        print("\n[BULB] Gnration recommandations consolides...")
        
        recommendations = []
        
        for file_path, analysis in consolidated["cross_analysis"].items():
            consensus = analysis["consensus"]
            
            if consensus["action_recommended"]:
                recommendation = {
                    "file": file_path,
                    "priority": consensus["priority"],
                    "confidence": consensus["confidence"],
                    "action": "REFACTOR_IMMEDIATE" if consensus["priority"] == "CRITIQUE" else "REFACTOR_PLANNED",
                    "rationale": f"Consensus {self.models['alpha']} + {self.models['beta']}: {consensus['priority']}",
                    "effort": consensus["effort_estimate"],
                    "quick_wins": consensus["quick_wins_available"],
                    "next_phase": "PHASE_2_EXTRACTION" if consensus["quick_wins_available"] else "PHASE_2_PLANNING"
                }
                recommendations.append(recommendation)
        
        # Tri par priorit
        priority_order = {"CRITIQUE": 4, "LEVE": 3, "MODRE": 2, "FAIBLE": 1}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 1), reverse=True)
        
        return recommendations

    def _generate_next_steps(self, consolidated: Dict, recommendations: List) -> List[str]:
        """
        [TARGET] Gnration des prochaines tapes
        """
        next_steps = []
        
        if not recommendations:
            next_steps.append(" Aucun refactoring urgent requis")
            next_steps.append("[CHART] Monitoring continu recommand")
            return next_steps
        
        critical_files = [r for r in recommendations if r["priority"] == "CRITIQUE"]
        high_files = [r for r in recommendations if r["priority"] == "LEVE"]
        
        if critical_files:
            next_steps.append(f" URGENT: {len(critical_files)} fichier(s) critique(s)")
            next_steps.append("[LIGHTNING] Dmarrer Phase 2 immdiatement")
            
        if high_files:
            next_steps.append(f" IMPORTANT: {len(high_files)} fichier(s) prioritaire(s)")
            next_steps.append("[CLIPBOARD] Planifier Phase 2 cette semaine")
        
        quick_wins = sum(1 for r in recommendations if r["quick_wins"])
        if quick_wins:
            next_steps.append(f"[TARGET] {quick_wins} quick win(s) identifi(s)")
            next_steps.append("[LIGHTNING] Commencer par les extractions simples")
        
        next_steps.append("[CHART] Prparer backlog Phase 2")
        next_steps.append(" Configurer tests de rgression")
        
        return next_steps

    async def _save_results(self, results: PhaseResults):
        """
         Sauvegarde des rsultats
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Rsultats JSON complets
        json_file = self.results_dir / f"phase1_cloud_results_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(results), f, indent=2, ensure_ascii=False)
        
        # Rapport Markdown excutif
        md_file = self.results_dir / f"phase1_cloud_rapport_{timestamp}.md"
        await self._generate_markdown_report(results, md_file)
        
        print(f" Rsultats sauvegards:")
        print(f"   [DOCUMENT] JSON: {json_file}")
        print(f"   [CLIPBOARD] Rapport: {md_file}")

    async def _generate_markdown_report(self, results: PhaseResults, output_file: Path):
        """
        [CLIPBOARD] Gnration rapport Markdown
        """
        recommendations = results.recommendations
        
        report = f"""# [CHART] Rapport Phase 1 - Analyse Cloud

## [TARGET] Vue d'Ensemble

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Agents:** {self.models['alpha']} + {self.models['beta']}  
**Fichiers analyss:** {len(self.target_files)}  
**Recommandations:** {len(recommendations)}

##  Rsultats Critiques

"""
        
        # Recommandations par priorit
        for priority in ["CRITIQUE", "LEVE", "MODRE"]:
            priority_recs = [r for r in recommendations if r["priority"] == priority]
            if priority_recs:
                report += f"\n###  Priorit {priority} ({len(priority_recs)})\n\n"
                for rec in priority_recs:
                    report += f"- **{rec['file']}**\n"
                    report += f"  - Action: {rec['action']}\n"
                    report += f"  - Effort: {rec['effort']}\n"
                    report += f"  - Quick wins: {'[CHECK]' if rec['quick_wins'] else '[CROSS]'}\n\n"
        
        # Prochaines tapes
        report += "\n## [TARGET] Prochaines tapes\n\n"
        for step in results.next_steps:
            report += f"- {step}\n"
        
        # Dtails techniques
        report += "\n## [TOOL] Dtails Techniques\n\n"
        for file_path, analysis in results.consolidated_analysis["cross_analysis"].items():
            report += f"### [FOLDER] {file_path}\n\n"
            report += f"- **Complexit Alpha:** {analysis['alpha_insights']['complexity_level']}\n"
            report += f"- **Urgence Beta:** {analysis['beta_insights']['refactoring_urgency']}\n"
            report += f"- **Consensus:** {analysis['consensus']['priority']}\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)

async def main():
    """Point d'entre principal"""
    orchestrator = OrchestratorPhase1AnalysisCloud()
    
    try:
        # Validation environnement
        if not await orchestrator.validate_cloud_environment():
            print("[CROSS] Validation environnement choue")
            return False
        
        # Excution Phase 1
        results = await orchestrator.execute_parallel_analysis()
        
        # Affichage rsultats
        print(f"\n PHASE 1 TERMINE AVEC SUCCS!")
        print(f"[CHART] {len(results.recommendations)} recommandations gnres")
        print(f"[TARGET] Prochaines tapes: {len(results.next_steps)}")
        
        return True
        
    except Exception as e:
        print(f"[CROSS] Erreur Phase 1: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(main()) 



