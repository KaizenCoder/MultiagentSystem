#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
[TARGET] ORCHESTRATEUR PHASE 2 - ARCHITECTURE NEXTGENERATION
Coordination des Agents Alpha & Beta pour cration d'architecture modulaire

Mission: Orchestrer la Phase 2 du refactoring NextGeneration
- Coordination Agent Architect Alpha (Claude)
- Coordination Agent Architect Beta (GPT-4)
- Validation croise des plans architecturaux
- Gnration du plan architectural final
- Prparation Phase 3 (Implmentation)

Statut: ACTIF - Phase 2 Architecture
"""

import os
import json
import datetime
import asyncio
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import sys

# Imports des agents
sys.path.append(str(Path(__file__).parent))
from agent_architect_alpha_claude_sonnet4 import AgentArchitectAlphaClaude
from agent_architect_beta_gpt4 import AgentArchitectBetaGPT4

@dataclass
class Phase2Results:
    """Rsultats complets Phase 2"""
    timestamp: str
    duration_seconds: float
    alpha_plans: Dict[str, Any]
    beta_alternatives: Dict[str, Any]
    consensus_recommendations: Dict[str, Any]
    final_architecture_plan: Dict[str, Any]
    next_phase_ready: bool
    success: bool

class OrchestratorPhase2Architecture:
    """
    [TARGET] Orchestrateur Phase 2 - Architecture
    
    Responsabilits:
    - Coordination agents Alpha/Beta
    - Validation croise plans
    - Gnration consensus architectural
    - Prparation Phase 3
    """
    
    def __init__(self):
        self.workspace_path = Path(__file__).parent.parent
        self.results_path = self.workspace_path / "refactoring_workspace" / "results" / "phase2_architecture"
        self.results_path.mkdir(parents=True, exist_ok=True)
        
        # Initialiser agents
        self.agent_alpha = AgentArchitectAlphaClaude()
        self.agent_beta = AgentArchitectBetaGPT4()
        
        # Fichiers god mode cibles
        self.god_mode_files = [
            "orchestrator/app/main.py",
            "orchestrator/app/agents/advanced_coordination.py", 
            "orchestrator/app/performance/redis_cluster_manager.py",
            "orchestrator/app/observability/monitoring.py"
        ]
        
        # Mtriques objectifs
        self.target_metrics = {
            "orchestrator/app/main.py": {"current": 1990, "target": 100},
            "orchestrator/app/agents/advanced_coordination.py": {"current": 779, "target": 150},
            "orchestrator/app/performance/redis_cluster_manager.py": {"current": 738, "target": 150},
            "orchestrator/app/observability/monitoring.py": {"current": 709, "target": 150}
        }

    async def execute_phase2_complete(self) -> Phase2Results:
        """
        [ROCKET] Excuter Phase 2 complte - Architecture
        """
        start_time = time.time()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("[CONSTRUCTION] DMARRAGE PHASE 2 - ARCHITECTURE MODULAIRE")
        print("=" * 60)
        
        try:
            # 1. Analyse Architecture Alpha (Claude)
            print("\n[SEARCH] TAPE 1: Analyse Architecture Alpha (Claude Sonnet 4)")
            alpha_plans = await self.agent_alpha.create_complete_architecture()
            
            if not alpha_plans:
                raise Exception("chec analyse Alpha")
            
            print(f"[CHECK] Alpha: {len(alpha_plans)} plans architecturaux crs")
            
            # 2. Analyse Architecture Beta (GPT-4)
            print("\n[SEARCH] TAPE 2: Architecture Alternative Beta (GPT-4)")
            beta_alternatives = await self.agent_beta.create_alternative_architectures()
            
            if not beta_alternatives:
                raise Exception("chec analyse Beta")
            
            print(f"[CHECK] Beta: {len(beta_alternatives)} architectures alternatives cres")
            
            # 3. Validation croise
            print("\n TAPE 3: Validation Croise Alpha  Beta")
            cross_validation = await self.perform_cross_validation(alpha_plans, beta_alternatives)
            
            # 4. Consensus architectural
            print("\n[TARGET] TAPE 4: Gnration Consensus Architectural")
            consensus = await self.generate_architectural_consensus(alpha_plans, beta_alternatives, cross_validation)
            
            # 5. Plan architectural final
            print("\n[CLIPBOARD] TAPE 5: Plan Architectural Final")
            final_plan = await self.create_final_architectural_plan(consensus)
            
            # Calcul dure
            duration = time.time() - start_time
            
            # Crer rsultats
            results = Phase2Results(
                timestamp=timestamp,
                duration_seconds=duration,
                alpha_plans={k: asdict(v) for k, v in alpha_plans.items()},
                beta_alternatives={k: asdict(v) for k, v in beta_alternatives.items()},
                consensus_recommendations=consensus,
                final_architecture_plan=final_plan,
                next_phase_ready=True,
                success=True
            )
            
            # Sauvegarder rsultats
            await self.save_phase2_results(results)
            
            # Rapport final
            await self.generate_phase2_report(results)
            
            print(f"\n PHASE 2 TERMINE AVEC SUCCS!")
            print(f" Dure: {duration:.2f} secondes")
            print(f"[CHART] Plans crs: {len(alpha_plans)}")
            print(f" Alternatives: {len(beta_alternatives)}")
            
            return results
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"\n[CROSS] CHEC PHASE 2: {e}")
            
            # Rsultats d'chec
            results = Phase2Results(
                timestamp=timestamp,
                duration_seconds=duration,
                alpha_plans={},
                beta_alternatives={},
                consensus_recommendations={},
                final_architecture_plan={},
                next_phase_ready=False,
                success=False
            )
            
            await self.save_phase2_results(results)
            return results

    async def perform_cross_validation(self, alpha_plans: Dict, beta_alternatives: Dict) -> Dict[str, Any]:
        """
         Validation croise Alpha  Beta
        """
        validation_results = {}
        
        for file_path in self.god_mode_files:
            print(f"  [SEARCH] Validation croise: {Path(file_path).name}")
            
            alpha_plan = alpha_plans.get(file_path)
            beta_alt = beta_alternatives.get(file_path)
            
            if alpha_plan and beta_alt:
                # Comparer approches
                comparison = {
                    "alpha_approach": {
                        "patterns": alpha_plan.patterns_applied,
                        "modules_count": len(alpha_plan.modules_to_extract),
                        "risk_level": alpha_plan.risk_level,
                        "effort_hours": alpha_plan.estimated_effort_hours
                    },
                    "beta_approach": {
                        "patterns": beta_alt.patterns_suggested,
                        "recommendation_score": beta_alt.recommendation_score,
                        "risk_assessment": beta_alt.risk_assessment,
                        "optimizations": beta_alt.optimization_opportunities
                    },
                    "compatibility": self._assess_compatibility(alpha_plan, beta_alt),
                    "recommendation": self._get_recommendation(alpha_plan, beta_alt)
                }
                
                validation_results[file_path] = comparison
                print(f"    [CHECK] Validation: {comparison['recommendation']}")
        
        return validation_results

    def _assess_compatibility(self, alpha_plan, beta_alt) -> str:
        """valuer compatibilit des approches"""
        # Logique simple de compatibilit
        alpha_patterns = set(alpha_plan.patterns_applied)
        beta_patterns = set(beta_alt.patterns_suggested)
        
        overlap = len(alpha_patterns.intersection(beta_patterns))
        total = len(alpha_patterns.union(beta_patterns))
        
        compatibility_score = overlap / total if total > 0 else 0
        
        if compatibility_score > 0.7:
            return "HAUTE"
        elif compatibility_score > 0.4:
            return "MOYENNE"
        else:
            return "FAIBLE"

    def _get_recommendation(self, alpha_plan, beta_alt) -> str:
        """Obtenir recommandation base sur plans"""
        # Prioriser Alpha si effort raisonnable
        if alpha_plan.estimated_effort_hours <= 16 and alpha_plan.risk_level in ["FAIBLE", "MOYEN"]:
            return "SUIVRE_ALPHA"
        
        # Considrer Beta si score lev
        if beta_alt.recommendation_score >= 8:
            return "CONSIDRER_BETA"
        
        # Approche hybride par dfaut
        return "APPROCHE_HYBRIDE"

    async def generate_architectural_consensus(self, alpha_plans: Dict, beta_alternatives: Dict, validation: Dict) -> Dict[str, Any]:
        """
        [TARGET] Gnrer consensus architectural
        """
        consensus = {
            "global_strategy": "Approche modulaire SRP avec validation croise",
            "priority_order": [],
            "patterns_consensus": {},
            "implementation_roadmap": {},
            "risk_mitigation": {}
        }
        
        # Prioriser fichiers par impact/effort
        priority_files = []
        for file_path in self.god_mode_files:
            alpha_plan = alpha_plans.get(file_path)
            if alpha_plan:
                impact_score = self.target_metrics[file_path]["current"] - self.target_metrics[file_path]["target"]
                effort_score = alpha_plan.estimated_effort_hours
                priority = impact_score / effort_score if effort_score > 0 else 0
                
                priority_files.append({
                    "file": file_path,
                    "priority_score": priority,
                    "recommendation": validation.get(file_path, {}).get("recommendation", "SUIVRE_ALPHA")
                })
        
        # Trier par priorit
        priority_files.sort(key=lambda x: x["priority_score"], reverse=True)
        consensus["priority_order"] = priority_files
        
        # Patterns consensus
        all_patterns = set()
        for plan in alpha_plans.values():
            all_patterns.update(plan.patterns_applied)
        
        consensus["patterns_consensus"] = {
            "core_patterns": list(all_patterns),
            "architecture_style": "Clean Architecture avec SRP",
            "migration_pattern": "Blue-Green Deployment"
        }
        
        return consensus

    async def create_final_architectural_plan(self, consensus: Dict[str, Any]) -> Dict[str, Any]:
        """
        [CLIPBOARD] Crer plan architectural final
        """
        final_plan = {
            "version": "2.0",
            "created": datetime.datetime.now().isoformat(),
            "strategy": consensus["global_strategy"],
            "execution_phases": {
                "phase_3": "Route Extraction & Services Creation",
                "phase_4": "Repository Pattern Implementation", 
                "phase_5": "Testing & Validation",
                "phase_6": "Documentation & Deployment"
            },
            "priority_execution": consensus["priority_order"],
            "target_metrics": self.target_metrics,
            "patterns_to_implement": consensus["patterns_consensus"]["core_patterns"],
            "success_criteria": {
                "lines_reduction": "~85% rduction totale",
                "modularity": "SRP respect  100%",
                "test_coverage": "> 90%",
                "performance": "Maintenue ou amliore"
            }
        }
        
        return final_plan

    async def save_phase2_results(self, results: Phase2Results):
        """
         Sauvegarder rsultats Phase 2
        """
        # JSON complet
        json_path = self.results_path / f"phase2_architecture_results_{results.timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(results), f, indent=2, ensure_ascii=False)
        
        print(f"[CHART] Rsultats sauvegards: {json_path}")

    async def generate_phase2_report(self, results: Phase2Results):
        """
        [CLIPBOARD] Gnrer rapport Phase 2
        """
        success_icon = "[CHECK]" if results.success else "[CROSS]"
        
        report = f"""# [CONSTRUCTION] Rapport Phase 2 - Architecture Modulaire

## {success_icon} Vue d'Ensemble

**Date:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Dure:** {results.duration_seconds:.2f} secondes  
**Statut:** {'SUCCS' if results.success else 'CHEC'}  
**Plans Alpha:** {len(results.alpha_plans)}  
**Alternatives Beta:** {len(results.beta_alternatives)}

## [CHART] Rsultats Dtaills

### [TARGET] Plans Architecturaux Alpha (Claude)
{self._format_alpha_summary(results.alpha_plans)}

###  Alternatives Beta (GPT-4)
{self._format_beta_summary(results.beta_alternatives)}

## [TARGET] Plan Architectural Final

{self._format_final_plan(results.final_architecture_plan)}

## [ROCKET] Prochaines tapes

{'1. [CHECK] Phase 2 Architecture termine' if results.success else '1. [CROSS] Phase 2  reprendre'}
2.  Crer agents Phase 3 (Route Extractor, Services Creator)
3.  Dmarrer implmentation main.py (priorit absolue)
4.  Tests de rgression continus

---
*Gnr par Orchestrateur Phase 2 Architecture*
"""
        
        report_path = self.results_path / f"phase2_architecture_rapport_{results.timestamp}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[CLIPBOARD] Rapport sauvegard: {report_path}")

    def _format_alpha_summary(self, alpha_plans: Dict) -> str:
        """Formater rsum Alpha"""
        if not alpha_plans:
            return "Aucun plan Alpha gnr"
        
        total_current = sum(plan.get('current_lines', 0) for plan in alpha_plans.values())
        total_target = sum(plan.get('target_lines', 0) for plan in alpha_plans.values())
        reduction = ((total_current - total_target) / total_current * 100) if total_current > 0 else 0
        
        return f"""
**Lignes totales:** {total_current:,}  {total_target:,} (-{reduction:.1f}%)  
**Fichiers traits:** {len(alpha_plans)}  
**Patterns identifis:** {self._count_unique_patterns(alpha_plans)}
"""

    def _format_beta_summary(self, beta_alternatives: Dict) -> str:
        """Formater rsum Beta"""
        if not beta_alternatives:
            return "Aucune alternative Beta gnre"
        
        avg_score = sum(alt.get('recommendation_score', 0) for alt in beta_alternatives.values()) / len(beta_alternatives)
        
        return f"""
**Alternatives cres:** {len(beta_alternatives)}  
**Score moyen:** {avg_score:.1f}/10  
**Patterns alternatifs:** {self._count_beta_patterns(beta_alternatives)}
"""

    def _format_final_plan(self, final_plan: Dict) -> str:
        """Formater plan final"""
        if not final_plan:
            return "Plan final non gnr"
        
        return f"""
**Stratgie:** {final_plan.get('strategy', 'Non dfinie')}  
**Prochaine phase:** {final_plan.get('execution_phases', {}).get('phase_3', 'Non dfinie')}  
**Fichier prioritaire:** {final_plan.get('priority_execution', [{}])[0].get('file', 'Non dfini') if final_plan.get('priority_execution') else 'Non dfini'}
"""

    def _count_unique_patterns(self, alpha_plans: Dict) -> int:
        """Compter patterns uniques Alpha"""
        patterns = set()
        for plan in alpha_plans.values():
            patterns.update(plan.get('patterns_applied', []))
        return len(patterns)

    def _count_beta_patterns(self, beta_alternatives: Dict) -> int:
        """Compter patterns Beta"""
        patterns = set()
        for alt in beta_alternatives.values():
            patterns.update(alt.get('patterns_suggested', []))
        return len(patterns)

# [TARGET] EXECUTION PRINCIPALE
async def main():
    """
    [ROCKET] Point d'entre principal Orchestrateur Phase 2
    """
    print("[TARGET] ORCHESTRATEUR PHASE 2 - ARCHITECTURE NEXTGENERATION")
    print("=" * 60)
    
    orchestrator = OrchestratorPhase2Architecture()
    
    try:
        # Excuter Phase 2 complte
        results = await orchestrator.execute_phase2_complete()
        
        if results.success:
            print("\n PHASE 2 ARCHITECTURE TERMINE AVEC SUCCS!")
            print("[TARGET] Prt pour Phase 3 - Implmentation")
            return results
        else:
            print("\n CHEC PHASE 2 ARCHITECTURE")
            return None
        
    except Exception as e:
        print(f"\n[CROSS] ERREUR ORCHESTRATEUR: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    # Vrifications environnement
    required_keys = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY']
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"[CROSS] Cls API manquantes: {', '.join(missing_keys)}")
        sys.exit(1)
    
    # Excution asynchrone
    result = asyncio.run(main())
    
    if result and result.success:
        print(" Orchestrateur Phase 2 termin avec succs!")
        sys.exit(0)
    else:
        print(" chec Orchestrateur Phase 2")
        sys.exit(1) 



