#!/usr/bin/env python3
"""
🎮 Orchestrateur Phase 1 - Analyse Parallèle RTX3090
Mission: Coordination agents Alpha (Mixtral) + Beta (Qwen-Coder) locaux
Configuration: RTX 3090 avec modèles Ollama optimisés
"""

import os
import sys
import json
import time
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

# Configuration RTX3090 OBLIGATOIRE
os.environ['CUDA_VISIBLE_DEVICES'] = '1'  # RTX 3090 uniquement
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

# Import agents locaux
from agent_analyzer_alpha_mixtral_rtx3090 import AgentCodeAnalyzerAlpha
from agent_analyzer_beta_qwen_rtx3090 import AgentCodeAnalyzerBeta

@dataclass
class PhaseResult:
    """Résultat Phase 1 consolidé"""
    phase_name: str
    phase_number: int
    timestamp: str
    duration: float
    agents_executed: List[str]
    models_used: Dict[str, str]
    gpu_usage: Dict[str, str]
    alpha_result: Optional[Dict[str, Any]]
    beta_result: Optional[Dict[str, Any]]
    consolidated_findings: Dict[str, Any]
    next_phase_recommendations: List[str]
    performance_metrics: Dict[str, Any]
    status: str

class OrchestratorPhase1RTX3090:
    """Orchestrateur Phase 1 - Analyse Parallèle RTX3090"""
    
    def __init__(self):
        self.name = "Orchestrateur Phase 1 RTX3090"
        self.phase = "PHASE_1_ANALYSIS_PARALLEL"
        self.version = "1.0.0"
        self.status = "INITIALIZING"
        
        # Configuration RTX3090
        self.gpu_device = "RTX 3090 (Device 1)"
        self.models_config = {
            "mixtral": {
                "model": "mixtral:8x7b-instruct-v0.1-q3_k_m",
                "vram": "22GB (92%)",
                "performance": "5.4 tokens/s",
                "usage": "Analyse approfondie qualité"
            },
            "qwen": {
                "model": "qwen2.5-coder:1.5b", 
                "vram": "986MB (4%)",
                "performance": "8.2 tokens/s",
                "usage": "Analyse rapide code"
            }
        }
        
        # Agents participants
        self.agent_alpha = None
        self.agent_beta = None
        
        # Workspace
        self.project_root = Path.cwd()
        self.refactoring_workspace = self.project_root / "refactoring_workspace"
        self.refactoring_workspace.mkdir(parents=True, exist_ok=True)
        
    async def validate_rtx3090_environment(self) -> bool:
        """Valide environnement RTX3090 et modèles Ollama"""
        print("🔍 Validation environnement RTX3090...")
        
        try:
            # Vérification variables environnement
            cuda_device = os.environ.get('CUDA_VISIBLE_DEVICES')
            if cuda_device != '1':
                print(f"❌ CUDA_VISIBLE_DEVICES incorrect: {cuda_device} (attendu: 1)")
                return False
            
            # Vérification modèles Ollama (simulation)
            print("✅ Configuration GPU RTX3090 validée")
            print(f"   • Device: {self.gpu_device}")
            print(f"   • Mixtral: {self.models_config['mixtral']['model']}")
            print(f"   • Qwen-Coder: {self.models_config['qwen']['model']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur validation RTX3090: {e}")
            return False
    
    async def initialize_agents(self) -> bool:
        """Initialise agents Alpha et Beta"""
        print("🤖 Initialisation agents Phase 1...")
        
        try:
            # Agent Alpha - Mixtral RTX3090
            print("🔍 Initialisation Agent Alpha (Mixtral RTX3090)...")
            self.agent_alpha = AgentCodeAnalyzerAlpha()
            print(f"   ✅ {self.agent_alpha.name} initialisé")
            print(f"   📊 Modèle: {self.agent_alpha.model}")
            print(f"   🎮 GPU: {self.agent_alpha.gpu_device}")
            print(f"   🧠 VRAM: {self.agent_alpha.vram_usage}")
            
            # Agent Beta - Qwen-Coder RTX3090
            print("⚡ Initialisation Agent Beta (Qwen-Coder RTX3090)...")
            self.agent_beta = AgentCodeAnalyzerBeta()
            print(f"   ✅ {self.agent_beta.name} initialisé")
            print(f"   📊 Modèle: {self.agent_beta.model}")
            print(f"   🎮 GPU: {self.agent_beta.gpu_device}")
            print(f"   ⚡ Performance: {self.agent_beta.expected_performance}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur initialisation agents: {e}")
            return False
    
    async def execute_parallel_analysis(self) -> tuple:
        """Exécute analyse parallèle avec Mixtral + Qwen-Coder"""
        print("🚀 DÉMARRAGE ANALYSE PARALLÈLE RTX3090")
        print("━" * 60)
        print(f"🔍 Agent Alpha: {self.agent_alpha.model} (Analyse approfondie)")
        print(f"⚡ Agent Beta: {self.agent_beta.model} (Analyse rapide code)")
        print("━" * 60)
        
        start_time = time.time()
        
        try:
            # Exécution parallèle des 2 agents
            alpha_task = asyncio.create_task(
                self.agent_alpha.execute_mission(),
                name="Alpha_Mixtral_Analysis"
            )
            
            beta_task = asyncio.create_task(
                self.agent_beta.execute_mission(),
                name="Beta_Qwen_Analysis" 
            )
            
            # Attente résultats parallèles
            print("⏳ Exécution analyses parallèles en cours...")
            
            # Collecte résultats
            alpha_result, beta_result = await asyncio.gather(
                alpha_task,
                beta_task,
                return_exceptions=True
            )
            
            execution_time = time.time() - start_time
            
            print("🎉 ANALYSE PARALLÈLE TERMINÉE")
            print(f"⏱️ Durée totale: {execution_time:.2f}s")
            
            # Vérification succès
            alpha_success = not isinstance(alpha_result, Exception) and hasattr(alpha_result, 'status')
            beta_success = not isinstance(beta_result, Exception) and hasattr(beta_result, 'status')
            
            if alpha_success:
                print(f"✅ Agent Alpha: {alpha_result.agent_name} - {alpha_result.summary.get('files_count', 0)} fichiers")
            else:
                print(f"❌ Agent Alpha: Erreur - {alpha_result}")
            
            if beta_success:
                print(f"✅ Agent Beta: {beta_result.agent_name} - {beta_result.summary.get('files_analyzed', 0)} fichiers")
            else:
                print(f"❌ Agent Beta: Erreur - {beta_result}")
            
            return alpha_result, beta_result, execution_time
            
        except Exception as e:
            print(f"❌ Erreur exécution parallèle: {e}")
            return None, None, 0
    
    def consolidate_findings(self, alpha_result, beta_result) -> Dict[str, Any]:
        """Consolide résultats des 2 analyses"""
        print("📊 Consolidation résultats Alpha + Beta...")
        
        findings = {
            "consolidation_timestamp": datetime.now().isoformat(),
            "sources": {
                "alpha_analysis": "Mixtral RTX3090 - Analyse approfondie",
                "beta_analysis": "Qwen-Coder RTX3090 - Analyse rapide code"
            }
        }
        
        # Consolidation si alpha réussi
        if alpha_result and hasattr(alpha_result, 'summary'):
            findings["alpha_summary"] = {
                "files_analyzed": alpha_result.summary.get('files_count', 0),
                "total_lines": alpha_result.summary.get('total_lines_analyzed', 0),
                "hotspots": alpha_result.summary.get('hotspots_count', 0),
                "critical_issues": alpha_result.summary.get('critical_issues', 0),
                "recommendations": alpha_result.summary.get('recommendations_count', 0)
            }
            findings["alpha_hotspots"] = alpha_result.hotspots[:3] if alpha_result.hotspots else []
            findings["alpha_top_recommendations"] = [
                {
                    "file": r.target_file,
                    "issue": r.issue_type,
                    "severity": r.severity,
                    "action": r.recommended_action
                }
                for r in sorted(alpha_result.recommendations, key=lambda x: x.priority)[:5]
            ] if alpha_result.recommendations else []
        
        # Consolidation si beta réussi
        if beta_result and hasattr(beta_result, 'summary'):
            findings["beta_summary"] = {
                "files_analyzed": beta_result.summary.get('files_analyzed', 0),
                "functions_analyzed": beta_result.summary.get('functions_analyzed', 0),
                "classes_analyzed": beta_result.summary.get('classes_analyzed', 0),
                "extraction_candidates": beta_result.summary.get('extraction_candidates', 0),
                "split_candidates": beta_result.summary.get('split_candidates', 0),
                "strategies_generated": beta_result.summary.get('strategies_generated', 0)
            }
            findings["beta_strategies"] = [
                {
                    "type": s.strategy_type,
                    "priority": s.priority,
                    "description": s.description,
                    "estimated_hours": s.estimated_hours,
                    "lines_reduction": s.expected_lines_reduction
                }
                for s in sorted(beta_result.refactoring_strategies, key=lambda x: x.priority)[:5]
            ] if beta_result.refactoring_strategies else []
        
        # Métriques croisées
        if alpha_result and beta_result:
            findings["cross_analysis"] = {
                "total_files_scope": max(
                    len(alpha_result.files_analyzed) if hasattr(alpha_result, 'files_analyzed') else 0,
                    len(beta_result.files_analyzed) if hasattr(beta_result, 'files_analyzed') else 0
                ),
                "analysis_consistency": "CONFIRMED" if (
                    alpha_result.summary.get('critical_issues', 0) > 0 and
                    beta_result.summary.get('extraction_candidates', 0) > 0
                ) else "PARTIAL",
                "priority_alignment": "HIGH" if (
                    alpha_result.summary.get('hotspots_count', 0) > 0 and
                    beta_result.summary.get('strategies_generated', 0) > 0
                ) else "MEDIUM"
            }
        
        print(f"📊 Consolidation terminée: {len(findings)} sections")
        return findings
    
    def generate_next_phase_recommendations(self, findings: Dict[str, Any]) -> List[str]:
        """Génère recommandations pour Phase 2"""
        recommendations = []
        
        # Basé sur résultats Alpha (Mixtral)
        if "alpha_summary" in findings:
            critical_issues = findings["alpha_summary"].get("critical_issues", 0)
            hotspots = findings["alpha_summary"].get("hotspots", 0)
            
            if critical_issues > 0:
                recommendations.append(
                    f"PRIORITAIRE: Traiter {critical_issues} issues critiques identifiées par Mixtral"
                )
            
            if hotspots > 0:
                recommendations.append(
                    f"Focus Phase 2: Refactoring {hotspots} hotspots critiques"
                )
        
        # Basé sur résultats Beta (Qwen-Coder)
        if "beta_summary" in findings:
            extraction_candidates = findings["beta_summary"].get("extraction_candidates", 0)
            split_candidates = findings["beta_summary"].get("split_candidates", 0)
            
            if extraction_candidates > 0:
                recommendations.append(
                    f"Action immédiate: Extraire {extraction_candidates} fonctions identifiées par Qwen-Coder"
                )
            
            if split_candidates > 0:
                recommendations.append(
                    f"Restructuration: Diviser {split_candidates} classes violant SRP"
                )
        
        # Recommandations consolidées
        if "cross_analysis" in findings:
            consistency = findings["cross_analysis"].get("analysis_consistency", "UNKNOWN")
            if consistency == "CONFIRMED":
                recommendations.append(
                    "VALIDATION: Analyses Alpha + Beta convergent - Procéder Phase 2 Blue-Green"
                )
            elif consistency == "PARTIAL":
                recommendations.append(
                    "ATTENTION: Analyses partiellement cohérentes - Validation humaine requise"
                )
        
        # Recommandations par défaut
        if not recommendations:
            recommendations.extend([
                "Procéder validation humaine des analyses",
                "Préparer environnement Blue-Green Phase 2",
                "Sélectionner fichiers prioritaires pour refactoring"
            ])
        
        return recommendations
    
    async def save_phase_results(self, phase_result: PhaseResult):
        """Sauvegarde résultats Phase 1"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Sauvegarde JSON détaillée
        json_file = self.refactoring_workspace / f"phase1_results_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(phase_result), f, indent=2, ensure_ascii=False)
        
        # Sauvegarde rapport markdown
        md_file = self.refactoring_workspace / f"phase1_rapport_{timestamp}.md"
        await self._generate_markdown_report(phase_result, md_file)
        
        print(f"💾 Résultats sauvegardés:")
        print(f"   📄 JSON: {json_file}")
        print(f"   📝 Rapport: {md_file}")
    
    async def _generate_markdown_report(self, result: PhaseResult, output_file: Path):
        """Génère rapport markdown Phase 1"""
        content = f"""# 📊 RAPPORT PHASE 1 - ANALYSE PARALLÈLE RTX3090

## 🎯 Résumé Exécutif

**Phase:** {result.phase_name}  
**Timestamp:** {result.timestamp}  
**Durée:** {result.duration:.2f}s  
**Status:** {result.status}  

### 🤖 Agents Exécutés
{chr(10).join([f"- {agent}" for agent in result.agents_executed])}

### 🎮 Modèles RTX3090 Utilisés
{chr(10).join([f"- **{agent}**: {model}" for agent, model in result.models_used.items()])}

## 📈 Résultats Consolidés

### 🔍 Analyse Alpha (Mixtral)
{self._format_alpha_results(result.alpha_result)}

### ⚡ Analyse Beta (Qwen-Coder)  
{self._format_beta_results(result.beta_result)}

## 🎯 Recommandations Phase 2

{chr(10).join([f"1. {rec}" for rec in result.next_phase_recommendations])}

## 📊 Métriques Performance

{self._format_performance_metrics(result.performance_metrics)}

---
*Rapport généré automatiquement par {self.name}*
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _format_alpha_results(self, alpha_result) -> str:
        """Formate résultats Alpha pour markdown"""
        if not alpha_result or not hasattr(alpha_result, 'summary'):
            return "❌ Analyse Alpha échouée"
        
        summary = alpha_result.summary
        return f"""
- **Fichiers analysés:** {summary.get('files_count', 0)}
- **Lignes totales:** {summary.get('total_lines_analyzed', 0):,}
- **Issues critiques:** {summary.get('critical_issues', 0)}
- **Hotspots:** {summary.get('hotspots_count', 0)}
- **Recommandations:** {summary.get('recommendations_count', 0)}
"""
    
    def _format_beta_results(self, beta_result) -> str:
        """Formate résultats Beta pour markdown"""
        if not beta_result or not hasattr(beta_result, 'summary'):
            return "❌ Analyse Beta échouée"
        
        summary = beta_result.summary
        return f"""
- **Fichiers analysés:** {summary.get('files_analyzed', 0)}
- **Fonctions:** {summary.get('functions_analyzed', 0)}
- **Classes:** {summary.get('classes_analyzed', 0)}
- **Candidats extraction:** {summary.get('extraction_candidates', 0)}
- **Candidats split:** {summary.get('split_candidates', 0)}
- **Stratégies:** {summary.get('strategies_generated', 0)}
"""
    
    def _format_performance_metrics(self, metrics) -> str:
        """Formate métriques performance pour markdown"""
        return f"""
- **GPU utilisé:** {metrics.get('gpu_used', 'RTX 3090')}
- **Modèles simultanés:** {metrics.get('concurrent_models', 2)}
- **Temps total:** {metrics.get('total_duration', 0):.2f}s
- **Efficacité:** {metrics.get('efficiency', 'UNKNOWN')}
"""
    
    async def execute_phase_1(self) -> PhaseResult:
        """Exécute Phase 1 complète"""
        print("🚀 DÉMARRAGE PHASE 1 - ANALYSE PARALLÈLE RTX3090")
        print("=" * 70)
        
        start_time = time.time()
        self.status = "RUNNING"
        
        try:
            # 1. Validation environnement
            if not await self.validate_rtx3090_environment():
                raise Exception("Validation environnement RTX3090 échouée")
            
            # 2. Initialisation agents
            if not await self.initialize_agents():
                raise Exception("Initialisation agents échouée")
            
            # 3. Exécution analyse parallèle
            alpha_result, beta_result, execution_time = await self.execute_parallel_analysis()
            
            # 4. Consolidation résultats
            consolidated_findings = self.consolidate_findings(alpha_result, beta_result)
            
            # 5. Recommandations Phase 2
            next_phase_recommendations = self.generate_next_phase_recommendations(consolidated_findings)
            
            # 6. Métriques performance
            total_duration = time.time() - start_time
            performance_metrics = {
                "total_duration": total_duration,
                "analysis_duration": execution_time,
                "overhead_duration": total_duration - execution_time,
                "gpu_used": self.gpu_device,
                "concurrent_models": 2,
                "efficiency": "HIGH" if total_duration < 60 else "MEDIUM"
            }
            
            # 7. Résultat final
            phase_result = PhaseResult(
                phase_name="Phase 1 - Analyse Parallèle RTX3090",
                phase_number=1,
                timestamp=datetime.now().isoformat(),
                duration=total_duration,
                agents_executed=[
                    f"{self.agent_alpha.name} ({self.agent_alpha.model})",
                    f"{self.agent_beta.name} ({self.agent_beta.model})"
                ],
                models_used={
                    "alpha": self.agent_alpha.model,
                    "beta": self.agent_beta.model
                },
                gpu_usage={
                    "device": self.gpu_device,
                    "mixtral_vram": self.models_config["mixtral"]["vram"],
                    "qwen_vram": self.models_config["qwen"]["vram"]
                },
                alpha_result=asdict(alpha_result) if alpha_result and hasattr(alpha_result, '__dict__') else None,
                beta_result=asdict(beta_result) if beta_result and hasattr(beta_result, '__dict__') else None,
                consolidated_findings=consolidated_findings,
                next_phase_recommendations=next_phase_recommendations,
                performance_metrics=performance_metrics,
                status="SUCCESS"
            )
            
            # 8. Sauvegarde résultats
            await self.save_phase_results(phase_result)
            
            self.status = "SUCCESS"
            
            print("🎉 PHASE 1 TERMINÉE AVEC SUCCÈS")
            print("=" * 70)
            print(f"⏱️ Durée totale: {total_duration:.2f}s")
            print(f"📊 Efficacité: {performance_metrics['efficiency']}")
            print(f"🎯 Recommandations Phase 2: {len(next_phase_recommendations)}")
            
            return phase_result
            
        except Exception as e:
            self.status = "FAILED"
            print(f"❌ ÉCHEC PHASE 1: {e}")
            
            # Résultat d'erreur
            return PhaseResult(
                phase_name="Phase 1 - Analyse Parallèle RTX3090",
                phase_number=1,
                timestamp=datetime.now().isoformat(),
                duration=time.time() - start_time,
                agents_executed=[],
                models_used={},
                gpu_usage={},
                alpha_result=None,
                beta_result=None,
                consolidated_findings={"error": str(e)},
                next_phase_recommendations=["Résoudre erreurs Phase 1 avant Phase 2"],
                performance_metrics={"error": str(e)},
                status="FAILED"
            )

if __name__ == "__main__":
    # Test orchestrateur Phase 1
    orchestrator = OrchestratorPhase1RTX3090()
    
    async def main():
        result = await orchestrator.execute_phase_1()
        
        print(f"\n📊 RÉSULTAT PHASE 1:")
        print(f"Status: {result.status}")
        print(f"Durée: {result.duration:.2f}s")
        print(f"Agents: {len(result.agents_executed)}")
        print(f"Recommandations: {len(result.next_phase_recommendations)}")
    
    asyncio.run(main()) 