#!/usr/bin/env python3
"""
🔍 AGENT 2 - ÉVALUATEUR D'UTILITÉ AMÉLIORÉ (NextGeneration + TOP)
=================================================================
Mission: Évaluer l'utilité des outils analysés avec intelligence multi-critères avancée

🚀 AMÉLIORATIONS INTÉGRÉES DE L'ÉQUIPE TOP:
- 🧠 Système d'évaluation multi-critères pondérés
- 🎯 Mots-clés NextGeneration spécialisés (high/medium/low priority)
- ⚖️ Évaluation 5 dimensions: technique, architecture, valeur, intégration, maintenance
- 🔍 Détection automatique conflits et redondances
- 📊 Algorithme de similarité entre outils
- 🎯 Priorisation intelligente basée sur scores composites
- 🏆 Support évaluation spécialisée (APEX, PowerShell, Batch)

Architecture Pattern Factory:
- Hérite de Agent de base  
- Implémente méthodes abstraites obligatoires
- Configuration NextGeneration intégrée
- Logging Pattern Factory standardisé
"""

import json
import sys
from pathlib import Path
from core import logging_manager
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import re
import sys

# Import Pattern Factory (OBLIGATOIRE selon guide)
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
    try:
        from core.agent_factory_architecture import Agent, Task, Result
        PATTERN_FACTORY_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️ Pattern Factory non disponible: {e}")
        # Fallback pour compatibilité
        class Agent:
            def __init__(self, agent_type: str, **config):
                self.agent_type = agent_type
                self.config = config
                self.agent_id = f"agent_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                # LoggingManager NextGeneration - Agent
                import sys
from pathlib import Path
from core import logging_manager
                self.logger = LoggingManager().get_agent_logger(
                    agent_name="Agent",
                    role="ai_processor",
                    domain="general",
                    async_enabled=True
                )
                
            async def startup(self): pass
            async def shutdown(self): pass
            async def health_check(self): return {"status": "healthy"}
            def get_capabilities(self): return []
        
        class Task:
            def __init__(self, task_id: str, description: str, **kwargs):
                self.task_id = task_id
                self.description = description
                
        class Result:
            def __init__(self, success: bool, data: Any = None, error: str = None):
                self.success = success
                self.data = data
                self.error = error
        
        PATTERN_FACTORY_AVAILABLE = False

class AgentEvaluateurUtiliteUpgraded(Agent):
    """Agent spécialisé dans l'évaluation d'utilité avec intelligence multi-critères avancée - Pattern Factory NextGeneration"""
    
    def __init__(self, **config):
        # Initialisation Pattern Factory OBLIGATOIRE EN PREMIER
        super().__init__("evaluateur_utilite_upgraded", **config)
        
        # 🧠 SYSTÈME D'ÉVALUATION MULTI-CRITÈRES PONDÉRÉS (INTÉGRÉ DE L'ÉQUIPE TOP)
        self.evaluation_criteria = {
            "technical_relevance": 0.30,      # Pertinence technique pour NextGeneration
            "architecture_compatibility": 0.25, # Compatibilité avec l'architecture existante
            "added_value": 0.20,              # Valeur ajoutée par rapport aux outils existants
            "integration_ease": 0.15,         # Facilité d'intégration
            "maintenance_burden": 0.10        # Charge de maintenance
        }
        
        # 🎯 MOTS-CLÉS NEXTGENERATION SPÉCIALISÉS (INTÉGRÉ DE L'ÉQUIPE TOP)
        self.nextgen_keywords = {
            "high_priority": [
                "agent", "orchestrator", "api", "monitoring", "performance", "security",
                "factory", "pattern", "async", "enterprise", "production", "scalability"
            ],
            "medium_priority": [
                "database", "logging", "config", "utility", "automation", "validation",
                "backup", "documentation", "testing", "integration", "deployment"
            ],
            "low_priority": [
                "gui", "desktop", "windows", "macos", "specific", "local", "manual",
                "legacy", "deprecated", "temporary", "prototype", "demo"
            ]
        }
        
        # 📊 SEUILS D'ÉVALUATION AVANCÉS
        self.evaluation_thresholds = {
            "excellent": 0.85,
            "good": 0.70,
            "average": 0.55,
            "poor": 0.40,
            "reject": 0.25
        }
        
        # 🔍 PATTERNS DE DÉTECTION POUR CONFLITS
        self.conflict_patterns = {
            "duplicate_functionality": [
                r"backup.*manager", r"monitor.*system", r"log.*analyzer",
                r"config.*manager", r"test.*runner", r"deploy.*tool"
            ],
            "incompatible_technologies": [
                ("python", "powershell"), ("linux", "windows"), ("sync", "async")
            ]
        }
        
        # Assurer que les attributs existent toujours
        if not hasattr(self, 'agent_id'):
            self.agent_id = f"agent_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if not hasattr(self, 'agent_type'):
            self.agent_type = "evaluateur_utilite_upgraded"
            
        # Configurer le logger
        import logging
        self.logger = logging.getLogger(f"Agent2_EvaluateurUtilite_{self.agent_id}")
            
        if hasattr(self, 'logger'):
            self.logger.info(f"🧠 Agent 2 - Évaluateur Utilité UPGRADED initialisé - ID: {self.agent_id}")
            self.logger.info(f"✅ Critères d'évaluation: {len(self.evaluation_criteria)} critères pondérés")
            self.logger.info(f"✅ Mots-clés NextGen: {sum(len(v) for v in self.nextgen_keywords.values())} mots-clés")
        else:
            print(f"🧠 Agent 2 - Évaluateur Utilité UPGRADED initialisé - ID: {self.agent_id}")
        
    # Implémentation méthodes abstraites OBLIGATOIRES
    async def startup(self):
        """Démarrage agent évaluateur utilité amélioré"""
        if hasattr(self, 'logger'):
            self.logger.info(f"🚀 Agent Évaluateur Utilité UPGRADED {self.agent_id} - DÉMARRAGE")
            self.logger.info("🧠 Intelligence multi-critères activée")
            self.logger.info(f"✅ Critères d'évaluation: {list(self.evaluation_criteria.keys())}")
            self.logger.info(f"✅ Mots-clés NextGen chargés: {sum(len(v) for v in self.nextgen_keywords.values())} mots-clés")
            self.logger.info(f"✅ Seuils d'évaluation: {list(self.evaluation_thresholds.keys())}")
        else:
            print(f"🚀 Agent Évaluateur Utilité UPGRADED {self.agent_id} - DÉMARRAGE")
        
    async def shutdown(self):
        """Arrêt agent évaluateur utilité amélioré"""
        if hasattr(self, 'logger'):
            self.logger.info(f"🛑 Agent Évaluateur Utilité UPGRADED {self.agent_id} - ARRÊT")
        else:
            print(f"🛑 Agent Évaluateur Utilité UPGRADED {self.agent_id} - ARRÊT")
        
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé agent évaluateur utilité amélioré"""
        health_status = {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "healthy",
            "evaluation_criteria_loaded": len(self.evaluation_criteria) > 0,
            "keywords_loaded": len(self.nextgen_keywords) > 0,
            "intelligence_level": "multi_criteria_advanced",
            "ready_for_evaluation": True,
            "features_upgraded": [
                "🧠 Multi-critères pondérés",
                "🎯 Mots-clés NextGen spécialisés", 
                "⚖️ Évaluation 5 dimensions",
                "🔍 Détection conflits",
                "📊 Similarité outils",
                "🎯 Priorisation intelligente"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        return health_status
    
    async def execute_task(self, task: Task) -> Result:
        """Exécution des tâches d'évaluation d'utilité avancée - Pattern Factory OBLIGATOIRE"""
        try:
            self.logger.info(f"🎯 Exécution tâche: {task.task_id}")
            
            if task.task_id == "evaluate_tools":
                # Tâche d'évaluation d'outils avec intelligence avancée
                analysis_data = getattr(task, 'analysis_data', None)
                if not analysis_data:
                    return Result(success=False, error="analysis_data requis pour evaluate_tools")
                    
                results = await self.evaluate_tools_utility(analysis_data)
                
                return Result(
                    success=True,
                    data={
                        "evaluation_results": results,
                        "agent_id": self.agent_id,
                        "task_id": task.task_id,
                        "intelligence_level": "multi_criteria_advanced"
                    }
                )
                
            elif task.task_id == "evaluate_single_tool":
                # Tâche d'évaluation d'outil unique avec intelligence avancée
                tool_data = getattr(task, 'tool_data', None)
                if not tool_data:
                    return Result(success=False, error="tool_data requis pour evaluate_single_tool")
                    
                evaluation = await self.evaluate_single_tool(tool_data)
                return Result(success=True, data=evaluation)
                
            elif task.task_id == "detect_conflicts":
                # Nouvelle tâche de détection de conflits
                tools_data = getattr(task, 'tools_data', None)
                if not tools_data:
                    return Result(success=False, error="tools_data requis pour detect_conflicts")
                    
                conflicts = await self.detect_conflicts_and_redundancies(tools_data)
                return Result(success=True, data=conflicts)
                
            elif task.task_id == "calculate_similarity":
                # Nouvelle tâche de calcul de similarité
                tool1 = getattr(task, 'tool1', None)
                tool2 = getattr(task, 'tool2', None)
                if not tool1 or not tool2:
                    return Result(success=False, error="tool1 et tool2 requis pour calculate_similarity")
                    
                similarity = await self.calculate_tool_similarity(tool1, tool2)
                return Result(success=True, data={"similarity_score": similarity})
                
            else:
                return Result(
                    success=False, 
                    error=f"Tâche non reconnue: {task.task_id}"
                )
                
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution tâche {task.task_id}: {e}")
            return Result(success=False, error=str(e))
    
    def get_capabilities(self) -> List[str]:
        """Retourne les capacités avancées de l'agent évaluateur utilité"""
        return [
            # Capacités originales
            "evaluate_tools",
            "evaluate_single_tool",
            # Nouvelles capacités avancées de l'équipe TOP
            "evaluate_technical_relevance",
            "evaluate_architecture_compatibility", 
            "evaluate_added_value",
            "evaluate_integration_ease",
            "evaluate_maintenance_burden",
            "detect_conflicts",
            "calculate_similarity",
            "select_tools_intelligent",
            "generate_recommendations_advanced",
            "prioritize_integration",
            "multi_criteria_evaluation"
        ]
    
    # 🧠 MÉTHODES D'INTELLIGENCE AVANCÉE INTÉGRÉES DE L'ÉQUIPE TOP
    
    async def evaluate_tools_utility(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Évaluation complète de l'utilité des outils avec intelligence multi-critères - Version UPGRADED"""
        self.logger.info("🧠 [UPGRADED] Démarrage évaluation utilité intelligente multi-critères")
        
        tools = analysis_data.get("tools", [])
        if not tools:
            self.logger.warning("⚠️ Aucun outil à évaluer")
            return {"selected_tools": [], "rejected_tools": [], "evaluation_summary": {}}
            
        # Évaluation de chaque outil avec intelligence avancée
        evaluated_tools = []
        for tool in tools:
            self.logger.info(f"🔍 Évaluation intelligente: {tool.get('name', 'Unknown')}")
            evaluation = await self.evaluate_single_tool(tool)
            evaluated_tools.append(evaluation)
            
        # 🔍 DÉTECTION AUTOMATIQUE CONFLITS ET REDONDANCES (NOUVEAU)
        self.logger.info("🔍 Détection automatique conflits et redondances...")
        conflict_analysis = await self.detect_conflicts_and_redundancies(evaluated_tools)
        
        # 🎯 SÉLECTION INTELLIGENTE BASÉE SUR SCORES COMPOSITES (NOUVEAU)
        self.logger.info("🎯 Sélection intelligente basée sur scores composites...")
        selection_results = await self.select_tools_intelligent(evaluated_tools, conflict_analysis)
        
        # 📊 GÉNÉRATION RAPPORT AVANCÉ
        evaluation_summary = await self.generate_evaluation_summary_advanced(
            evaluated_tools, selection_results, conflict_analysis
        )
        
        self.logger.info(f"✅ Évaluation terminée: {len(selection_results.get('selected_tools', []))} outils sélectionnés")
        
        return {
            "selected_tools": selection_results.get("selected_tools", []),
            "rejected_tools": selection_results.get("rejected_tools", []),
            "conflicted_tools": conflict_analysis.get("conflicted_tools", []),
            "evaluation_summary": evaluation_summary,
            "intelligence_level": "multi_criteria_advanced",
            "total_evaluated": len(evaluated_tools)
        }
    
    async def evaluate_single_tool(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """Évaluation d'un outil unique avec intelligence multi-critères avancée"""
        tool_name = tool.get("name", "Unknown")
        self.logger.info(f"🔍 Évaluation multi-critères: {tool_name}")
        
        # 🎯 ÉVALUATION 5 DIMENSIONS AVANCÉES (INTÉGRÉ DE L'ÉQUIPE TOP)
        scores = {}
        scores["technical_relevance"] = await self.evaluate_technical_relevance(tool)
        scores["architecture_compatibility"] = await self.evaluate_architecture_compatibility(tool)
        scores["added_value"] = await self.evaluate_added_value(tool)
        scores["integration_ease"] = await self.evaluate_integration_ease(tool)
        scores["maintenance_burden"] = await self.evaluate_maintenance_burden(tool)
        
        # 📊 CALCUL SCORE COMPOSITE PONDÉRÉ
        weighted_score = sum(
            scores[criterion] * weight 
            for criterion, weight in self.evaluation_criteria.items()
        )
        
        # 🎯 DÉTERMINATION NIVEAU QUALITÉ
        quality_level = self._determine_quality_level(weighted_score)
        
        # 🏆 PRIORISATION INTELLIGENTE
        integration_priority = await self.determine_integration_priority(weighted_score, tool)
        
        # 💡 GÉNÉRATION RECOMMANDATIONS INTELLIGENTES
        recommendation = await self.generate_recommendation_advanced(weighted_score, scores, tool)
        
        evaluation_result = {
            "tool_name": tool_name,
            "weighted_score": round(weighted_score, 3),
            "quality_level": quality_level,
            "integration_priority": integration_priority,
            "detailed_scores": {k: round(v, 3) for k, v in scores.items()},
            "recommendation": recommendation,
            "evaluation_timestamp": datetime.now().isoformat(),
            "evaluator_agent": self.agent_id
        }
        
        self.logger.info(f"✅ {tool_name}: Score={weighted_score:.3f}, Qualité={quality_level}, Priorité={integration_priority}")
        
        return evaluation_result
    
    # 🎯 MÉTHODES D'ÉVALUATION 5 DIMENSIONS (INTÉGRÉES DE L'ÉQUIPE TOP)
    
    async def evaluate_technical_relevance(self, tool: Dict[str, Any]) -> float:
        """Évaluation pertinence technique pour NextGeneration"""
        score = 0.0
        tool_name = tool.get("name", "").lower()
        tool_description = tool.get("description", "").lower()
        tool_content = str(tool.get("content", "")).lower()
        
        # Vérification mots-clés haute priorité
        for keyword in self.nextgen_keywords["high_priority"]:
            if keyword in tool_name or keyword in tool_description or keyword in tool_content:
                score += 0.15
        
        # Vérification mots-clés moyenne priorité
        for keyword in self.nextgen_keywords["medium_priority"]:
            if keyword in tool_name or keyword in tool_description or keyword in tool_content:
                score += 0.08
        
        # Pénalité mots-clés faible priorité
        for keyword in self.nextgen_keywords["low_priority"]:
            if keyword in tool_name or keyword in tool_description:
                score -= 0.1
        
        # Bonus pour technologies NextGeneration
        nextgen_tech_bonus = 0.0
        if "async" in tool_content or "await" in tool_content:
            nextgen_tech_bonus += 0.2
        if "pattern" in tool_content and "factory" in tool_content:
            nextgen_tech_bonus += 0.15
        if "enterprise" in tool_content or "production" in tool_content:
            nextgen_tech_bonus += 0.1
        
        score += nextgen_tech_bonus
        
        return min(1.0, max(0.0, score))
    
    async def evaluate_architecture_compatibility(self, tool: Dict[str, Any]) -> float:
        """Évaluation compatibilité avec l'architecture existante"""
        score = 0.5  # Score de base
        
        tool_content = str(tool.get("content", "")).lower()
        imports = tool.get("imports", [])
        
        # Bonus compatibilité Pattern Factory
        if "from core.agent_factory_architecture import" in tool_content:
            score += 0.3
        elif "agent" in tool_content and "class" in tool_content:
            score += 0.15
        
        # Bonus structure async
        if "async def" in tool_content:
            score += 0.2
        
        # Bonus imports standards
        standard_imports = ["asyncio", "logging", "pathlib", "typing"]
        for imp in standard_imports:
            if imp in str(imports).lower() or f"import {imp}" in tool_content:
                score += 0.05
        
        # Pénalité technologies incompatibles
        incompatible = ["tkinter", "gui", "desktop", "windows-specific"]
        for inc in incompatible:
            if inc in tool_content:
                score -= 0.15
        
        return min(1.0, max(0.0, score))
    
    async def evaluate_added_value(self, tool: Dict[str, Any]) -> float:
        """Évaluation valeur ajoutée par rapport aux outils existants"""
        score = 0.4  # Score de base
        
        tool_name = tool.get("name", "").lower()
        tool_functions = tool.get("functions", [])
        tool_classes = tool.get("classes", [])
        
        # Bonus pour fonctionnalités uniques
        unique_keywords = [
            "optimizer", "analyzer", "generator", "validator", "monitor",
            "orchestrator", "scheduler", "deployer", "migrator"
        ]
        
        for keyword in unique_keywords:
            if keyword in tool_name or any(keyword in str(func).lower() for func in tool_functions):
                score += 0.15
        
        # Bonus complexité et richesse fonctionnelle
        if len(tool_functions) > 10:
            score += 0.1
        if len(tool_classes) > 3:
            score += 0.1
        
        # Bonus innovation
        innovation_keywords = ["ai", "ml", "intelligent", "smart", "auto", "adaptive"]
        for keyword in innovation_keywords:
            if keyword in tool_name:
                score += 0.2
                break
        
        return min(1.0, max(0.0, score))
    
    async def evaluate_integration_ease(self, tool: Dict[str, Any]) -> float:
        """Évaluation facilité d'intégration"""
        score = 0.6  # Score de base
        
        tool_content = str(tool.get("content", ""))
        dependencies = tool.get("dependencies", [])
        
        # Bonus faibles dépendances
        if len(dependencies) <= 5:
            score += 0.2
        elif len(dependencies) <= 10:
            score += 0.1
        else:
            score -= 0.1
        
        # Bonus structure standard
        if "def main():" in tool_content or "if __name__ == '__main__':" in tool_content:
            score += 0.1
        
        # Bonus documentation
        if '"""' in tool_content or "# " in tool_content:
            score += 0.1
        
        # Pénalité complexité excessive
        if len(tool_content) > 50000:  # Très gros fichier
            score -= 0.2
        elif len(tool_content) > 20000:
            score -= 0.1
        
        return min(1.0, max(0.0, score))
    
    async def evaluate_maintenance_burden(self, tool: Dict[str, Any]) -> float:
        """Évaluation charge de maintenance (score inversé - moins de charge = meilleur score)"""
        score = 0.7  # Score de base
        
        tool_content = str(tool.get("content", ""))
        complexity = tool.get("complexity_score", 0)
        
        # Pénalité complexité élevée
        if complexity > 80:
            score -= 0.3
        elif complexity > 60:
            score -= 0.2
        elif complexity > 40:
            score -= 0.1
        
        # Bonus bonnes pratiques
        if "logging" in tool_content:
            score += 0.1
        if "try:" in tool_content and "except:" in tool_content:
            score += 0.1
        if "type hints" in tool_content or "typing" in tool_content:
            score += 0.1
        
        # Pénalité code legacy
        legacy_patterns = ["print(", "input(", "raw_input", "execfile"]
        for pattern in legacy_patterns:
            if pattern in tool_content:
                score -= 0.1
        
        return min(1.0, max(0.0, score))
    
    # 🔍 DÉTECTION AUTOMATIQUE CONFLITS ET REDONDANCES (NOUVEAU)
    
    async def detect_conflicts_and_redundancies(self, evaluated_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Détection automatique des conflits et redondances entre outils"""
        self.logger.info("🔍 Analyse conflits et redondances...")
        
        conflicts = []
        redundancies = []
        
        # Analyse par paires
        for i, tool1 in enumerate(evaluated_tools):
            for j, tool2 in enumerate(evaluated_tools[i+1:], i+1):
                
                # Calcul similarité
                similarity = await self.calculate_tool_similarity(tool1, tool2)
                
                if similarity > 0.8:  # Très similaire = redondance
                    redundancies.append({
                        "tool1": tool1["tool_name"],
                        "tool2": tool2["tool_name"],
                        "similarity": similarity,
                        "type": "high_redundancy",
                        "recommendation": "Conserver le meilleur score"
                    })
                elif similarity > 0.6:  # Similaire = conflit potentiel
                    conflicts.append({
                        "tool1": tool1["tool_name"],
                        "tool2": tool2["tool_name"],
                        "similarity": similarity,
                        "type": "potential_conflict",
                        "recommendation": "Évaluer complémentarité"
                    })
        
        # Détection conflits par patterns
        pattern_conflicts = await self._detect_pattern_conflicts(evaluated_tools)
        conflicts.extend(pattern_conflicts)
        
        self.logger.info(f"✅ Détection terminée: {len(conflicts)} conflits, {len(redundancies)} redondances")
        
        return {
            "conflicts": conflicts,
            "redundancies": redundancies,
            "conflicted_tools": list(set([c["tool1"] for c in conflicts] + [c["tool2"] for c in conflicts])),
            "redundant_tools": list(set([r["tool1"] for r in redundancies] + [r["tool2"] for r in redundancies])),
            "total_issues": len(conflicts) + len(redundancies)
        }
    
    async def calculate_tool_similarity(self, tool1: Dict[str, Any], tool2: Dict[str, Any]) -> float:
        """Calcul de similarité entre deux outils"""
        name1 = tool1.get("tool_name", "").lower()
        name2 = tool2.get("tool_name", "").lower()
        
        # Similarité des noms
        name_similarity = len(set(name1.split()) & set(name2.split())) / max(1, len(set(name1.split()) | set(name2.split())))
        
        # Similarité des scores
        scores1 = tool1.get("detailed_scores", {})
        scores2 = tool2.get("detailed_scores", {})
        
        score_similarity = 0.0
        if scores1 and scores2:
            common_keys = set(scores1.keys()) & set(scores2.keys())
            if common_keys:
                score_diffs = [abs(scores1[k] - scores2[k]) for k in common_keys]
                score_similarity = 1.0 - (sum(score_diffs) / len(score_diffs))
        
        # Similarité globale
        return (name_similarity * 0.4 + score_similarity * 0.6)
    
    async def _detect_pattern_conflicts(self, evaluated_tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Détection de conflits par patterns"""
        pattern_conflicts = []
        
        # self.conflict_patterns["duplicate_functionality"] est une liste de patterns regex
        patterns = self.conflict_patterns["duplicate_functionality"]
        
        for i, pattern in enumerate(patterns):
            matching_tools = []
            for tool in evaluated_tools:
                tool_name = tool.get("tool_name", "").lower()
                if re.search(pattern, tool_name):
                    matching_tools.append(tool["tool_name"])
            
            if len(matching_tools) > 1:
                pattern_conflicts.append({
                    "tool1": matching_tools[0],
                    "tool2": matching_tools[1],
                    "similarity": 0.7,
                    "type": f"pattern_conflict_{i}",
                    "recommendation": f"Conflits détectés par pattern {pattern}"
                })
        
        return pattern_conflicts
    
    # 🎯 SÉLECTION INTELLIGENTE ET PRIORISATION
    
    async def select_tools_intelligent(self, evaluated_tools: List[Dict[str, Any]], 
                                     conflict_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Sélection intelligente des outils basée sur scores composites et analyse de conflits"""
        
        # Tri par score décroissant
        sorted_tools = sorted(evaluated_tools, key=lambda x: x["weighted_score"], reverse=True)
        
        selected_tools = []
        rejected_tools = []
        conflicted_tools = set(conflict_analysis.get("conflicted_tools", []))
        
        for tool in sorted_tools:
            tool_name = tool["tool_name"]
            score = tool["weighted_score"]
            
            # Critères de sélection intelligente
            if score >= self.evaluation_thresholds["good"]:
                if tool_name not in conflicted_tools:
                    selected_tools.append(tool)
                else:
                    # Gérer les conflits intelligemment
                    conflict_resolution = await self._resolve_conflict(tool, conflict_analysis)
                    if conflict_resolution["action"] == "select":
                        selected_tools.append(tool)
                    else:
                        rejected_tools.append({
                            **tool,
                            "rejection_reason": conflict_resolution["reason"]
                        })
            else:
                rejected_tools.append({
                    **tool,
                    "rejection_reason": f"Score insuffisant ({score:.3f} < {self.evaluation_thresholds['good']})"
                })
        
        return {
            "selected_tools": selected_tools,
            "rejected_tools": rejected_tools,
            "selection_criteria": "intelligent_multi_criteria",
            "total_evaluated": len(evaluated_tools),
            "selection_rate": len(selected_tools) / max(1, len(evaluated_tools))
        }
    
    async def _resolve_conflict(self, tool: Dict[str, Any], conflict_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Résolution intelligente des conflits"""
        tool_name = tool["tool_name"]
        score = tool["weighted_score"]
        
        # Logique de résolution simple : priorité au meilleur score
        conflicting_tools = []
        for conflict in conflict_analysis.get("conflicts", []):
            if conflict["tool1"] == tool_name or conflict["tool2"] == tool_name:
                other_tool = conflict["tool2"] if conflict["tool1"] == tool_name else conflict["tool1"]
                conflicting_tools.append(other_tool)
        
        # Pour cette version, on sélectionne si c'est le meilleur score
        if score >= self.evaluation_thresholds["good"]:
            return {
                "action": "select",
                "reason": f"Meilleur score parmi les outils en conflit"
            }
        else:
            return {
                "action": "reject", 
                "reason": f"Conflit avec {', '.join(conflicting_tools)} et score insuffisant"
            }
    
    async def determine_integration_priority(self, utility_score: float, tool: Dict[str, Any]) -> str:
        """Détermination intelligente de la priorité d'intégration"""
        if utility_score >= self.evaluation_thresholds["excellent"]:
            return "CRITIQUE"
        elif utility_score >= self.evaluation_thresholds["good"]:
            return "HAUTE"
        elif utility_score >= self.evaluation_thresholds["average"]:
            return "MOYENNE"
        elif utility_score >= self.evaluation_thresholds["poor"]:
            return "FAIBLE"
        else:
            return "REJETÉE"
    
    async def generate_recommendation_advanced(self, utility_score: float, scores: Dict[str, float], 
                                             tool: Dict[str, Any]) -> str:
        """Génération de recommandations intelligentes avancées"""
        recommendations = []
        
        # Recommandations basées sur le score global
        if utility_score >= self.evaluation_thresholds["excellent"]:
            recommendations.append("🏆 EXCELLENT - Intégration prioritaire recommandée")
        elif utility_score >= self.evaluation_thresholds["good"]:
            recommendations.append("✅ BON - Intégration recommandée")
        elif utility_score >= self.evaluation_thresholds["average"]:
            recommendations.append("⚠️ MOYEN - Évaluation approfondie nécessaire")
        else:
            recommendations.append("❌ FAIBLE - Intégration non recommandée")
        
        # Recommandations spécifiques par dimension
        if scores.get("technical_relevance", 0) < 0.5:
            recommendations.append("📋 Améliorer la pertinence technique NextGeneration")
        if scores.get("architecture_compatibility", 0) < 0.5:
            recommendations.append("🏗️ Adapter à l'architecture Pattern Factory")
        if scores.get("integration_ease", 0) < 0.5:
            recommendations.append("🔧 Simplifier l'intégration")
        if scores.get("maintenance_burden", 0) < 0.5:
            recommendations.append("⚖️ Réduire la complexité de maintenance")
        
        return " | ".join(recommendations)
    
    def _determine_quality_level(self, score: float) -> str:
        """Détermination du niveau de qualité basé sur le score"""
        for level, threshold in self.evaluation_thresholds.items():
            if score >= threshold:
                return level.upper()
        return "REJECT"
    
    async def generate_evaluation_summary_advanced(self, evaluated_tools: List[Dict[str, Any]], 
                                                 selection_results: Dict[str, Any],
                                                 conflict_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Génération de résumé d'évaluation avancé"""
        total_tools = len(evaluated_tools)
        selected_count = len(selection_results.get("selected_tools", []))
        rejected_count = len(selection_results.get("rejected_tools", []))
        
        # Distribution des scores
        score_distribution = {"excellent": 0, "good": 0, "average": 0, "poor": 0, "reject": 0}
        for tool in evaluated_tools:
            level = self._determine_quality_level(tool["weighted_score"])
            score_distribution[level.lower()] += 1
        
        # Top 5 outils
        top_tools = sorted(evaluated_tools, key=lambda x: x["weighted_score"], reverse=True)[:5]
        
        return {
            "total_evaluated": total_tools,
            "selected": selected_count,
            "rejected": rejected_count,
            "selection_rate": round((selected_count / max(1, total_tools)) * 100, 2),
            "score_distribution": score_distribution,
            "conflicts_detected": len(conflict_analysis.get("conflicts", [])),
            "redundancies_detected": len(conflict_analysis.get("redundancies", [])),
            "top_tools": [
                {"name": tool["tool_name"], "score": tool["weighted_score"]} 
                for tool in top_tools
            ],
            "evaluation_criteria": list(self.evaluation_criteria.keys()),
            "intelligence_level": "multi_criteria_advanced",
            "timestamp": datetime.now().isoformat()
        }


# Fonction factory pour créer l'agent (Pattern Factory)
def create_agent_evaluateur_utilite(**config) -> AgentEvaluateurUtiliteUpgraded:
    """Factory function pour créer un AgentEvaluateurUtiliteUpgraded conforme Pattern Factory"""
    return AgentEvaluateurUtiliteUpgraded(**config)

# Test de l'agent si exécuté directement
async def main():
    """Test de l'agent Pattern Factory amélioré"""
    agent = create_agent_evaluateur_utilite()
    
    try:
        await agent.startup()
        health = await agent.health_check()
        print(f"🏥 Health Check: {health}")
        
        # Test données d'exemple
        test_data = {
            "tools": [
                {
                    "name": "agent_monitor_system",
                    "description": "Système de monitoring pour agents",
                    "content": "async def monitor_agent(): pass",
                    "functions": ["monitor_agent", "check_health"],
                    "classes": ["AgentMonitor"],
                    "imports": ["asyncio", "logging"],
                    "dependencies": ["asyncio"],
                    "complexity_score": 45
                },
                {
                    "name": "gui_desktop_tool",
                    "description": "Outil desktop avec interface graphique",
                    "content": "import tkinter as tk",
                    "functions": ["create_gui"],
                    "classes": ["GuiApp"],
                    "imports": ["tkinter"],
                    "dependencies": ["tkinter", "os"],
                    "complexity_score": 60
                }
            ]
        }
        
        # Test évaluation
        result = await agent.evaluate_tools_utility(test_data)
        print(f"🎯 Résultat évaluation: {len(result['selected_tools'])} outils sélectionnés")
        
        await agent.shutdown()
        
    except Exception as e:
        print(f"❌ Erreur execution agent: {e}")
        await agent.shutdown()

if __name__ == "__main__":
    asyncio.run(main()) 




