#!/usr/bin/env python3
"""
🎯 Orchestrateur Phase 1 - Analyse Parallèle Cloud
🤖 Coordination: Agent Alpha (Claude Sonnet 4) + Agent Beta (Gemini 2.5)
⚡ Phase 1 Refactoring NextGeneration - Cloud APIs
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
    """Résultats consolidés Phase 1"""
    alpha_results: Dict[str, Any]
    beta_results: Dict[str, Any]
    consolidated_analysis: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    next_steps: List[str]

class OrchestratorPhase1AnalysisCloud:
    """
    🎯 Orchestrateur Phase 1 - Analyse Parallèle Cloud
    
    Mission:
    - Coordination exécution parallèle Agent Alpha + Beta
    - Validation environnement cloud
    - Consolidation des résultats croisés
    - Génération recommandations Phase 2
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
        
        # Fichiers god mode à analyser
        self.target_files = [
            "orchestrator/app/main.py",
            "orchestrator/app/agents/advanced_coordination.py", 
            "orchestrator/app/performance/redis_cluster_manager.py",
            "orchestrator/app/observability/monitoring.py"
        ]
        
        print(f"🎮 {self.name} initialisé")
        print(f"🤖 Modèles: Alpha={self.models['alpha']}, Beta={self.models['beta']}")
        print(f"📁 Workspace: {self.workspace}")

    async def validate_cloud_environment(self) -> bool:
        """
        🔍 Validation de l'environnement cloud
        """
        print("\n🔍 Validation environnement cloud...")
        
        try:
            # Vérification clés API
            api_keys = {
                "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
                "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY")
            }
            
            missing_keys = [key for key, value in api_keys.items() if not value]
            
            if missing_keys:
                print(f"❌ Clés API manquantes: {', '.join(missing_keys)}")
                print("💡 Configurez les variables d'environnement:")
                for key in missing_keys:
                    print(f"   export {key}=votre_clé_api")
                return False
            
            print("✅ Clés API configurées")
            
            # Vérification fichiers cibles
            missing_files = [f for f in self.target_files if not os.path.exists(f)]
            
            if missing_files:
                print(f"❌ Fichiers manquants: {missing_files}")
                return False
            
            print(f"✅ {len(self.target_files)} fichiers cibles trouvés")
            
            # Initialisation des agents
            try:
                self.agent_alpha = AgentAnalyzerAlphaClaudeSonnet4()
                self.agent_beta = AgentAnalyzerBetaGemini25()
                print("✅ Agents cloud initialisés")
                
                return True
                
            except Exception as e:
                print(f"❌ Erreur initialisation agents: {str(e)}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur validation environnement: {str(e)}")
            return False

    async def execute_parallel_analysis(self) -> PhaseResults:
        """
        🚀 Exécution analyse parallèle Alpha + Beta
        """
        print(f"\n🚀 Démarrage analyse parallèle - {len(self.target_files)} fichiers")
        
        start_time = time.time()
        alpha_results = {}
        beta_results = {}
        
        try:
            # Exécution parallèle pour chaque fichier
            for file_path in self.target_files:
                print(f"\n📊 Analyse parallèle: {file_path}")
                
                # Lancement simultané Alpha + Beta
                alpha_task = asyncio.create_task(
                    self.agent_alpha.analyze_file_deep(file_path)
                )
                beta_task = asyncio.create_task(
                    self.agent_beta.analyze_file_fast(file_path)
                )
                
                # Attente résultats parallèles
                alpha_result, beta_result = await asyncio.gather(
                    alpha_task, beta_task, return_exceptions=True
                )
                
                # Gestion des erreurs
                if isinstance(alpha_result, Exception):
                    print(f"⚠️ Erreur Agent Alpha: {str(alpha_result)}")
                    alpha_result = {"error": str(alpha_result), "file_path": file_path}
                
                if isinstance(beta_result, Exception):
                    print(f"⚠️ Erreur Agent Beta: {str(beta_result)}")
                    beta_result = {"error": str(beta_result), "file_path": file_path}
                
                alpha_results[file_path] = alpha_result
                beta_results[file_path] = beta_result
                
                print(f"✅ Analyse terminée: {file_path}")
            
            # Consolidation des résultats
            consolidated = await self._consolidate_results(alpha_results, beta_results)
            
            # Génération recommandations
            recommendations = await self._generate_recommendations(consolidated)
            
            # Prochaines étapes
            next_steps = self._generate_next_steps(consolidated, recommendations)
            
            execution_time = time.time() - start_time
            print(f"\n🎯 Phase 1 terminée en {execution_time:.2f}s")
            
            results = PhaseResults(
                alpha_results=alpha_results,
                beta_results=beta_results,
                consolidated_analysis=consolidated,
                recommendations=recommendations,
                next_steps=next_steps
            )
            
            # Sauvegarde des résultats
            await self._save_results(results)
            
            return results
            
        except Exception as e:
            print(f"❌ Erreur analyse parallèle: {str(e)}")
            raise

    async def _consolidate_results(self, alpha_results: Dict, beta_results: Dict) -> Dict[str, Any]:
        """
        🔄 Consolidation des résultats Alpha + Beta
        """
        print("\n🔄 Consolidation des analyses...")
        
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
        🤝 Construction du consensus Alpha + Beta
        """
        alpha_summary = alpha_data.get("summary", {})
        beta_summary = beta_data.get("summary", {})
        
        # Priorité consensus
        alpha_priority = alpha_summary.get("refactoring_priority", "FAIBLE")
        beta_urgency = beta_summary.get("refactoring_urgency", "FAIBLE")
        
        priority_scores = {"FAIBLE": 1, "MODÉRÉE": 2, "ÉLEVÉE": 3, "CRITIQUE": 4}
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
        💡 Génération des recommandations consolidées
        """
        print("\n💡 Génération recommandations consolidées...")
        
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
        
        # Tri par priorité
        priority_order = {"CRITIQUE": 4, "ÉLEVÉE": 3, "MODÉRÉE": 2, "FAIBLE": 1}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 1), reverse=True)
        
        return recommendations

    def _generate_next_steps(self, consolidated: Dict, recommendations: List) -> List[str]:
        """
        🎯 Génération des prochaines étapes
        """
        next_steps = []
        
        if not recommendations:
            next_steps.append("🎉 Aucun refactoring urgent requis")
            next_steps.append("📊 Monitoring continu recommandé")
            return next_steps
        
        critical_files = [r for r in recommendations if r["priority"] == "CRITIQUE"]
        high_files = [r for r in recommendations if r["priority"] == "ÉLEVÉE"]
        
        if critical_files:
            next_steps.append(f"🚨 URGENT: {len(critical_files)} fichier(s) critique(s)")
            next_steps.append("⚡ Démarrer Phase 2 immédiatement")
            
        if high_files:
            next_steps.append(f"⚠️ IMPORTANT: {len(high_files)} fichier(s) prioritaire(s)")
            next_steps.append("📋 Planifier Phase 2 cette semaine")
        
        quick_wins = sum(1 for r in recommendations if r["quick_wins"])
        if quick_wins:
            next_steps.append(f"🎯 {quick_wins} quick win(s) identifié(s)")
            next_steps.append("⚡ Commencer par les extractions simples")
        
        next_steps.append("📊 Préparer backlog Phase 2")
        next_steps.append("🧪 Configurer tests de régression")
        
        return next_steps

    async def _save_results(self, results: PhaseResults):
        """
        💾 Sauvegarde des résultats
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Résultats JSON complets
        json_file = self.results_dir / f"phase1_cloud_results_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(results), f, indent=2, ensure_ascii=False)
        
        # Rapport Markdown exécutif
        md_file = self.results_dir / f"phase1_cloud_rapport_{timestamp}.md"
        await self._generate_markdown_report(results, md_file)
        
        print(f"💾 Résultats sauvegardés:")
        print(f"   📄 JSON: {json_file}")
        print(f"   📋 Rapport: {md_file}")

    async def _generate_markdown_report(self, results: PhaseResults, output_file: Path):
        """
        📋 Génération rapport Markdown
        """
        recommendations = results.recommendations
        
        report = f"""# 📊 Rapport Phase 1 - Analyse Cloud

## 🎯 Vue d'Ensemble

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Agents:** {self.models['alpha']} + {self.models['beta']}  
**Fichiers analysés:** {len(self.target_files)}  
**Recommandations:** {len(recommendations)}

## 🚨 Résultats Critiques

"""
        
        # Recommandations par priorité
        for priority in ["CRITIQUE", "ÉLEVÉE", "MODÉRÉE"]:
            priority_recs = [r for r in recommendations if r["priority"] == priority]
            if priority_recs:
                report += f"\n### 🔥 Priorité {priority} ({len(priority_recs)})\n\n"
                for rec in priority_recs:
                    report += f"- **{rec['file']}**\n"
                    report += f"  - Action: {rec['action']}\n"
                    report += f"  - Effort: {rec['effort']}\n"
                    report += f"  - Quick wins: {'✅' if rec['quick_wins'] else '❌'}\n\n"
        
        # Prochaines étapes
        report += "\n## 🎯 Prochaines Étapes\n\n"
        for step in results.next_steps:
            report += f"- {step}\n"
        
        # Détails techniques
        report += "\n## 🔧 Détails Techniques\n\n"
        for file_path, analysis in results.consolidated_analysis["cross_analysis"].items():
            report += f"### 📁 {file_path}\n\n"
            report += f"- **Complexité Alpha:** {analysis['alpha_insights']['complexity_level']}\n"
            report += f"- **Urgence Beta:** {analysis['beta_insights']['refactoring_urgency']}\n"
            report += f"- **Consensus:** {analysis['consensus']['priority']}\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)

async def main():
    """Point d'entrée principal"""
    orchestrator = OrchestratorPhase1AnalysisCloud()
    
    try:
        # Validation environnement
        if not await orchestrator.validate_cloud_environment():
            print("❌ Validation environnement échouée")
            return False
        
        # Exécution Phase 1
        results = await orchestrator.execute_parallel_analysis()
        
        # Affichage résultats
        print(f"\n🎉 PHASE 1 TERMINÉE AVEC SUCCÈS!")
        print(f"📊 {len(results.recommendations)} recommandations générées")
        print(f"🎯 Prochaines étapes: {len(results.next_steps)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur Phase 1: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(main()) 