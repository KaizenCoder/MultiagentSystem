#!/usr/bin/env python3
"""
🔍 SYSTÈME VALIDATION INTER-AGENT
Utilisation capacité audit cross-agent pour validation continue en conditions réelles

Architecture: Agents s'auditent mutuellement pour validation croisée
Processus: Amélioration continue développement par audit inter-agent
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'agents'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'agents' / 'modern'))

class InterAgentValidationSystem:
    """
    🔍 Système Validation Inter-Agent NextGeneration
    
    Orchestrateur pour validation croisée agents en conditions réelles:
    - Agent 111 (AUDIT) → Valide autres agents  
    - Agent 05 (TESTING) → Teste fonctionnalités autres agents
    - Agent 00 (COORDINATION) → Orchestre workflows inter-agents
    - Agent 109 (FACTORY) → Génère templates validation
    
    Amélioration processus développement par audit continu inter-agent
    """
    
    def __init__(self):
        self.validation_session_id = f"inter_agent_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.loaded_agents = {}
        self.validation_matrix = {}
        self.improvement_recommendations = []
        
        # Configuration validation croisée
        self.validation_pairs = [
            {"auditor": "agent_111", "target": "agent_05", "type": "quality_audit"},
            {"auditor": "agent_05", "target": "agent_111", "type": "functional_test"},
            {"auditor": "agent_00", "target": "agent_05", "type": "coordination_test"},
            {"auditor": "agent_00", "target": "agent_111", "type": "workflow_audit"},
            {"auditor": "agent_109", "target": "agent_05", "type": "pattern_validation"},
            {"auditor": "agent_109", "target": "agent_111", "type": "template_audit"},
            {"auditor": "agent_111", "target": "agent_00", "type": "coordination_audit"},
            {"auditor": "agent_111", "target": "agent_109", "type": "factory_audit"}
        ]
        
    async def initialize_agent_ecosystem(self):
        """Charge tous les agents Phase 1 pour validation croisée"""
        
        print("🔧 Initialisation Écosystème Agents Phase 1")
        print("=" * 60)
        
        try:
            # Agent 111 - Auditeur
            print("📋 Chargement Agent 111 (AUDIT)...")
            from agent_111_auditeur_qualite_modern import ModernAgent111AuditeurQualite
            
            self.loaded_agents["agent_111"] = ModernAgent111AuditeurQualite(
                agent_id="agent_111_validation_ecosystem"
            )
            await self.loaded_agents["agent_111"].initialize_services()
            print("✅ Agent 111 chargé")
            
            # Agent 05 - Testeur
            print("🧪 Chargement Agent 05 (TESTING)...")
            from agent_05_maitre_tests_validation_modern_fixed import ModernAgent05MaitreTestsValidation
            
            self.loaded_agents["agent_05"] = ModernAgent05MaitreTestsValidation(
                agent_id="agent_05_validation_ecosystem"
            )
            await self.loaded_agents["agent_05"].startup()
            print("✅ Agent 05 chargé")
            
            # Agent 00 - Coordinateur
            print("🎖️ Chargement Agent 00 (COORDINATION)...")
            from agent_00_chef_equipe_coordinateur_modern import ModernAgent00ChefEquipeCoordinateur
            
            self.loaded_agents["agent_00"] = ModernAgent00ChefEquipeCoordinateur(
                agent_id="agent_00_validation_ecosystem"
            )
            await self.loaded_agents["agent_00"].startup()
            print("✅ Agent 00 chargé")
            
            # Agent 109 - Factory
            print("🏭 Chargement Agent 109 (FACTORY)...")
            from agent_109_pattern_factory_modern import ModernAgent109PatternFactory
            
            self.loaded_agents["agent_109"] = ModernAgent109PatternFactory(
                agent_id="agent_109_validation_ecosystem"
            )
            await self.loaded_agents["agent_109"].startup()
            print("✅ Agent 109 chargé")
            
            print(f"\n🎉 Écosystème complet: {len(self.loaded_agents)} agents chargés")
            return True
            
        except Exception as e:
            print(f"❌ Erreur initialisation écosystème: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def execute_cross_validation_matrix(self) -> Dict[str, Any]:
        """Exécute matrice validation croisée complète"""
        
        print(f"\n🔍 DÉBUT VALIDATION CROISÉE: {self.validation_session_id}")
        print("=" * 70)
        
        validation_results = {
            "session_id": self.validation_session_id,
            "validation_start": datetime.now().isoformat(),
            "ecosystem_agents": list(self.loaded_agents.keys()),
            "validation_pairs": self.validation_pairs,
            "cross_validations": {},
            "validation_matrix": {},
            "ecosystem_health": {},
            "improvement_plan": {}
        }
        
        try:
            # Phase 1: Validation Croisée par Paires
            print("\n📊 Phase 1: Validation Croisée par Paires")
            cross_validation_results = await self._execute_pairwise_validations()
            validation_results["cross_validations"] = cross_validation_results
            
            # Phase 2: Matrice Compatibilité Inter-Agent
            print("\n🔗 Phase 2: Matrice Compatibilité Inter-Agent")
            compatibility_matrix = await self._build_compatibility_matrix(cross_validation_results)
            validation_results["validation_matrix"] = compatibility_matrix
            
            # Phase 3: Santé Écosystème Global
            print("\n🏥 Phase 3: Santé Écosystème Global")
            ecosystem_health = await self._assess_ecosystem_health(compatibility_matrix)
            validation_results["ecosystem_health"] = ecosystem_health
            
            # Phase 4: Plan Amélioration Continue
            print("\n💡 Phase 4: Plan Amélioration Continue")
            improvement_plan = await self._generate_improvement_plan(validation_results)
            validation_results["improvement_plan"] = improvement_plan
            
            validation_results["validation_end"] = datetime.now().isoformat()
            validation_results["validation_status"] = "SUCCESS"
            
            print(f"\n✅ VALIDATION CROISÉE TERMINÉE: {validation_results['validation_status']}")
            
        except Exception as e:
            validation_results["validation_status"] = "ERROR"
            validation_results["error"] = str(e)
            print(f"❌ Erreur validation croisée: {e}")
        
        return validation_results
    
    async def _execute_pairwise_validations(self) -> Dict[str, Any]:
        """Exécute toutes les validations par paires"""
        
        pairwise_results = {}
        
        for i, pair in enumerate(self.validation_pairs, 1):
            auditor_id = pair["auditor"]
            target_id = pair["target"]
            validation_type = pair["type"]
            
            print(f"  🔍 Validation {i}/{len(self.validation_pairs)}: {auditor_id} → {target_id} ({validation_type})")
            
            try:
                validation_result = await self._execute_single_validation(
                    auditor_id, target_id, validation_type
                )
                
                pair_key = f"{auditor_id}_to_{target_id}"
                pairwise_results[pair_key] = {
                    "auditor": auditor_id,
                    "target": target_id,
                    "validation_type": validation_type,
                    "result": validation_result,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Affichage résultat
                success = validation_result.get("success", False)
                score = validation_result.get("compatibility_score", 0)
                status_emoji = "✅" if success else "⚠️"
                print(f"    {status_emoji} Score: {score:.2f} - {'SUCCESS' if success else 'PARTIAL'}")
                
            except Exception as e:
                print(f"    ❌ Erreur validation {auditor_id} → {target_id}: {e}")
                pairwise_results[f"{auditor_id}_to_{target_id}"] = {
                    "auditor": auditor_id,
                    "target": target_id,
                    "validation_type": validation_type,
                    "result": {"success": False, "error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
        
        return pairwise_results
    
    async def _execute_single_validation(self, auditor_id: str, target_id: str, validation_type: str) -> Dict[str, Any]:
        """Exécute une validation individuelle entre deux agents"""
        
        auditor_agent = self.loaded_agents[auditor_id]
        target_agent = self.loaded_agents[target_id]
        
        # Configuration task selon type validation
        if validation_type == "quality_audit":
            # Agent 111 audite qualité
            task_envelope = {
                "payload": {
                    "action": "audit_code_quality",
                    "data": {
                        "target_agent_id": target_id,
                        "audit_scope": "comprehensive",
                        "inter_agent_mode": True
                    }
                }
            }
            
        elif validation_type == "functional_test":
            # Agent 05 teste fonctionnalités
            task_envelope = {
                "type": "inter_agent_test",
                "params": {
                    "target_agent_id": target_id,
                    "test_type": "functional_validation",
                    "inter_agent_mode": True
                }
            }
            
        elif validation_type == "coordination_test":
            # Agent 00 teste coordination
            task_envelope = {
                "type": "coordination_validation",
                "params": {
                    "action": "coordinate_team",
                    "target_agent_id": target_id,
                    "validation_mode": True
                }
            }
            
        elif validation_type == "workflow_audit":
            # Agent 00 audite workflow
            task_envelope = {
                "type": "workflow_validation",
                "params": {
                    "action": "workflow_maintenance_complete",
                    "target_agent_id": target_id,
                    "audit_mode": True
                }
            }
            
        elif validation_type == "pattern_validation":
            # Agent 109 valide patterns
            task_envelope = {
                "type": "pattern_audit",
                "params": {
                    "action": "validate_template",
                    "target_agent_id": target_id,
                    "pattern_compliance": True
                }
            }
            
        elif validation_type == "template_audit":
            # Agent 109 audite templates
            task_envelope = {
                "type": "template_validation",
                "params": {
                    "action": "create_pattern",
                    "target_agent_id": target_id,
                    "audit_generation": True
                }
            }
            
        elif validation_type in ["coordination_audit", "factory_audit"]:
            # Agent 111 audite coordination/factory
            task_envelope = {
                "payload": {
                    "action": "audit_universal_quality",
                    "data": {
                        "target_agent_id": target_id,
                        "specialized_audit": validation_type,
                        "inter_agent_mode": True
                    }
                }
            }
        
        else:
            task_envelope = {"payload": {"action": "default_validation"}}
        
        # Exécution validation
        if auditor_id == "agent_111":
            result = await auditor_agent.execute_async(task_envelope)
        elif auditor_id in ["agent_05", "agent_00", "agent_109"]:
            result = await auditor_agent.execute_async(task_envelope)
        else:
            result = {"success": False, "error": "Unknown auditor type"}
        
        # Calcul score compatibilité
        compatibility_score = self._calculate_compatibility_score(result, validation_type)
        
        return {
            "success": result.get("success", False) if isinstance(result, dict) else getattr(result, 'success', False),
            "validation_type": validation_type,
            "auditor_result": result,
            "compatibility_score": compatibility_score,
            "inter_agent_communication": True,
            "real_conditions": True
        }
    
    def _calculate_compatibility_score(self, result: Any, validation_type: str) -> float:
        """Calcule score compatibilité basé sur résultat"""
        
        if isinstance(result, dict):
            success = result.get("success", False)
            has_data = bool(result.get("result") or result.get("data"))
            no_errors = "error" not in result
        else:
            success = getattr(result, 'success', False)
            has_data = bool(getattr(result, 'data', None))
            no_errors = not getattr(result, 'error', None)
        
        # Score base
        base_score = 0.0
        if success:
            base_score += 0.5
        if has_data:
            base_score += 0.3
        if no_errors:
            base_score += 0.2
        
        # Bonus selon type validation
        if validation_type in ["quality_audit", "factory_audit", "coordination_audit"]:
            # Audits critiques
            base_score *= 1.1
        elif validation_type in ["functional_test", "pattern_validation"]:
            # Tests fonctionnels
            base_score *= 1.05
        
        return min(base_score, 1.0)
    
    async def _build_compatibility_matrix(self, cross_validations: Dict) -> Dict[str, Any]:
        """Construit matrice compatibilité inter-agent"""
        
        agents = list(self.loaded_agents.keys())
        matrix = {}
        
        # Initialiser matrice
        for agent in agents:
            matrix[agent] = {}
            for other_agent in agents:
                if agent == other_agent:
                    matrix[agent][other_agent] = 1.0  # Self-compatibility
                else:
                    matrix[agent][other_agent] = 0.0
        
        # Remplir matrice avec résultats validation
        for pair_key, validation in cross_validations.items():
            if validation["result"].get("success"):
                auditor = validation["auditor"]
                target = validation["target"]
                score = validation["result"].get("compatibility_score", 0.0)
                
                # Score directionnel auditor → target
                matrix[auditor][target] = score
        
        # Calculer statistiques matrice
        total_pairs = len(agents) * (len(agents) - 1)  # Exclude self-pairs
        successful_pairs = sum(
            1 for agent in agents for other in agents 
            if agent != other and matrix[agent][other] > 0.5
        )
        
        matrix_stats = {
            "compatibility_matrix": matrix,
            "total_agent_pairs": total_pairs,
            "successful_pairs": successful_pairs,
            "compatibility_rate": (successful_pairs / total_pairs * 100) if total_pairs > 0 else 0,
            "average_compatibility": sum(
                matrix[agent][other] for agent in agents for other in agents if agent != other
            ) / total_pairs if total_pairs > 0 else 0
        }
        
        return matrix_stats
    
    async def _assess_ecosystem_health(self, compatibility_matrix: Dict) -> Dict[str, Any]:
        """Évalue santé globale écosystème agents"""
        
        matrix = compatibility_matrix["compatibility_matrix"]
        agents = list(self.loaded_agents.keys())
        
        # Santé individuelle agents
        agent_health = {}
        for agent in agents:
            # Score santé = moyenne compatibilité avec autres agents
            others_scores = [matrix[agent][other] for other in agents if other != agent]
            incoming_scores = [matrix[other][agent] for other in agents if other != agent]
            
            agent_health[agent] = {
                "outgoing_compatibility": sum(others_scores) / len(others_scores) if others_scores else 0,
                "incoming_compatibility": sum(incoming_scores) / len(incoming_scores) if incoming_scores else 0,
                "bidirectional_health": (
                    sum(others_scores) + sum(incoming_scores)
                ) / (len(others_scores) + len(incoming_scores)) if (others_scores or incoming_scores) else 0,
                "health_status": "EXCELLENT" if sum(others_scores) / len(others_scores) > 0.8 else 
                              "GOOD" if sum(others_scores) / len(others_scores) > 0.6 else
                              "NEEDS_IMPROVEMENT"
            }
        
        # Santé écosystème global
        ecosystem_health = {
            "individual_agents": agent_health,
            "ecosystem_metrics": {
                "total_compatibility_rate": compatibility_matrix["compatibility_rate"],
                "average_cross_compatibility": compatibility_matrix["average_compatibility"],
                "successful_interactions": compatibility_matrix["successful_pairs"],
                "total_possible_interactions": compatibility_matrix["total_agent_pairs"]
            },
            "ecosystem_status": (
                "EXCELLENT" if compatibility_matrix["compatibility_rate"] > 80 else
                "GOOD" if compatibility_matrix["compatibility_rate"] > 60 else
                "NEEDS_IMPROVEMENT"
            ),
            "critical_patterns": {
                "most_compatible_agent": max(agent_health.keys(), key=lambda x: agent_health[x]["bidirectional_health"]),
                "least_compatible_agent": min(agent_health.keys(), key=lambda x: agent_health[x]["bidirectional_health"]),
                "best_interaction_pair": self._find_best_interaction_pair(matrix, agents),
                "problematic_interactions": self._find_problematic_interactions(matrix, agents)
            }
        }
        
        return ecosystem_health
    
    def _find_best_interaction_pair(self, matrix: Dict, agents: List[str]) -> Dict[str, Any]:
        """Trouve la meilleure paire d'interaction"""
        
        best_score = 0
        best_pair = None
        
        for agent1 in agents:
            for agent2 in agents:
                if agent1 != agent2:
                    # Score bidirectionnel
                    score = (matrix[agent1][agent2] + matrix[agent2][agent1]) / 2
                    if score > best_score:
                        best_score = score
                        best_pair = (agent1, agent2)
        
        return {
            "agent_1": best_pair[0] if best_pair else None,
            "agent_2": best_pair[1] if best_pair else None,
            "bidirectional_score": best_score,
            "recommendation": f"Use {best_pair[0]} ↔ {best_pair[1]} as template for inter-agent cooperation" if best_pair else None
        }
    
    def _find_problematic_interactions(self, matrix: Dict, agents: List[str]) -> List[Dict[str, Any]]:
        """Trouve interactions problématiques"""
        
        problematic = []
        
        for agent1 in agents:
            for agent2 in agents:
                if agent1 != agent2:
                    score = matrix[agent1][agent2]
                    if score < 0.5:  # Seuil problématique
                        problematic.append({
                            "auditor": agent1,
                            "target": agent2,
                            "compatibility_score": score,
                            "issue_level": "CRITICAL" if score < 0.2 else "MODERATE",
                            "recommended_action": f"Improve {agent1} → {agent2} interaction protocol"
                        })
        
        return problematic[:5]  # Top 5 problèmes
    
    async def _generate_improvement_plan(self, validation_results: Dict) -> Dict[str, Any]:
        """Génère plan amélioration basé sur validation croisée"""
        
        ecosystem_health = validation_results["ecosystem_health"]
        compatibility_matrix = validation_results["validation_matrix"]
        
        improvement_plan = {
            "immediate_actions": [],
            "short_term_improvements": [],
            "long_term_strategy": [],
            "development_process_updates": [],
            "continuous_validation_protocol": {}
        }
        
        # Actions immédiates basées sur santé écosystème
        ecosystem_status = ecosystem_health["ecosystem_status"]
        if ecosystem_status == "NEEDS_IMPROVEMENT":
            improvement_plan["immediate_actions"].extend([
                "🚨 URGENT: Fix critical agent interactions below 50% compatibility",
                "🔧 Review and standardize inter-agent communication protocols",
                "📋 Implement immediate compatibility patches for problematic pairs"
            ])
        elif ecosystem_status == "GOOD":
            improvement_plan["immediate_actions"].extend([
                "📈 Optimize good interactions to reach excellent level",
                "🔍 Focus on weak interaction points for quick wins"
            ])
        else:  # EXCELLENT
            improvement_plan["immediate_actions"].extend([
                "🎉 Maintain excellent ecosystem health",
                "🚀 Use as template for Wave 1 inter-agent validation"
            ])
        
        # Améliorations court terme
        problematic_interactions = ecosystem_health["critical_patterns"]["problematic_interactions"]
        if problematic_interactions:
            improvement_plan["short_term_improvements"].extend([
                f"🔧 Fix {len(problematic_interactions)} problematic interactions identified",
                "📚 Create inter-agent compatibility guidelines",
                "🧪 Implement automated compatibility testing"
            ])
        
        best_pair = ecosystem_health["critical_patterns"]["best_interaction_pair"]
        if best_pair["agent_1"]:
            improvement_plan["short_term_improvements"].append(
                f"📋 Use {best_pair['agent_1']} ↔ {best_pair['agent_2']} as golden template (score: {best_pair['bidirectional_score']:.2f})"
            )
        
        # Stratégie long terme
        compatibility_rate = compatibility_matrix["compatibility_rate"]
        improvement_plan["long_term_strategy"] = [
            f"🎯 Target: Achieve >90% inter-agent compatibility (current: {compatibility_rate:.1f}%)",
            "🏗️ Build automated inter-agent validation into CI/CD pipeline",
            "🔄 Establish continuous ecosystem health monitoring",
            "📊 Create inter-agent performance benchmarks for Wave 2+3"
        ]
        
        # Mise à jour processus développement
        improvement_plan["development_process_updates"] = [
            "✅ OBLIGATOIRE: Validation inter-agent avant déploiement",
            "🔍 Audit croisé systématique pour chaque nouvel agent",
            "📋 Matrice compatibilité mise à jour à chaque migration",
            "🎯 Seuil minimum 70% compatibilité pour validation",
            "🔄 Tests inter-agent automatisés en conditions réelles"
        ]
        
        # Protocole validation continue
        improvement_plan["continuous_validation_protocol"] = {
            "frequency": "Daily for active development, Weekly for stable agents",
            "mandatory_pairs": [
                "All new agents must pass validation with existing agents",
                "Critical pairs must maintain >80% compatibility",
                "Any agent modification triggers re-validation"
            ],
            "escalation_process": [
                "Compatibility <50%: BLOCK deployment",
                "Compatibility 50-70%: REVIEW required", 
                "Compatibility >70%: APPROVED with monitoring"
            ],
            "automation_targets": [
                "Automated inter-agent test execution",
                "Real-time compatibility monitoring",
                "Predictive compatibility analysis for new features"
            ]
        }
        
        return improvement_plan

async def main():
    """Point d'entrée système validation inter-agent"""
    
    try:
        validator = InterAgentValidationSystem()
        
        # Initialisation écosystème
        if not await validator.initialize_agent_ecosystem():
            print("❌ Échec initialisation écosystème")
            return {"error": "ecosystem_initialization_failed"}
        
        # Exécution validation croisée complète
        validation_results = await validator.execute_cross_validation_matrix()
        
        # Sauvegarde résultats
        results_file = Path(__file__).parent.parent / "reports" / f"inter_agent_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results_file.parent.mkdir(exist_ok=True)
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(validation_results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 70)
        print("📊 RÉSUMÉ VALIDATION INTER-AGENT")
        print("=" * 70)
        
        ecosystem_health = validation_results.get("ecosystem_health", {})
        ecosystem_metrics = ecosystem_health.get("ecosystem_metrics", {})
        
        print(f"Agents Écosystème: {len(validation_results.get('ecosystem_agents', []))}")
        print(f"Validations Croisées: {len(validation_results.get('cross_validations', {}))}")
        print(f"Taux Compatibilité: {ecosystem_metrics.get('total_compatibility_rate', 0):.1f}%")
        print(f"Interactions Réussies: {ecosystem_metrics.get('successful_interactions', 0)}/{ecosystem_metrics.get('total_possible_interactions', 0)}")
        print(f"Status Écosystème: {ecosystem_health.get('ecosystem_status', 'UNKNOWN')}")
        
        critical_patterns = ecosystem_health.get("critical_patterns", {})
        print(f"Agent Plus Compatible: {critical_patterns.get('most_compatible_agent', 'N/A')}")
        print(f"Meilleure Paire: {critical_patterns.get('best_interaction_pair', {}).get('agent_1', 'N/A')} ↔ {critical_patterns.get('best_interaction_pair', {}).get('agent_2', 'N/A')}")
        
        improvement_plan = validation_results.get("improvement_plan", {})
        immediate_actions = improvement_plan.get("immediate_actions", [])
        
        print(f"\n💡 Actions Immédiates ({len(immediate_actions)}):")
        for action in immediate_actions[:3]:
            print(f"  {action}")
        
        print(f"\n📄 Rapport détaillé: {results_file}")
        
        if validation_results.get("validation_status") == "SUCCESS":
            ecosystem_status = ecosystem_health.get("ecosystem_status", "UNKNOWN")
            if ecosystem_status == "EXCELLENT":
                print("\n🎉 ÉCOSYSTÈME EXCELLENT - Inter-agent validation opérationnelle")
                print("✅ Processus développement validé par audit croisé")
                print("🚀 Ready for Wave 1 avec validation inter-agent continue")
            elif ecosystem_status == "GOOD":
                print("\n👍 ÉCOSYSTÈME BON - Améliorations recommandées")
                print("⚠️ Processus développement à optimiser")
            else:
                print("\n⚠️ ÉCOSYSTÈME À AMÉLIORER - Actions requises")
                print("🔧 Processus développement nécessite corrections")
        else:
            print("\n⚠️ Validation partielle - Voir rapport détaillé")
        
        return validation_results
        
    except Exception as e:
        print(f"❌ Erreur validation inter-agent: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    asyncio.run(main())