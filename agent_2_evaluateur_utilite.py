#!/usr/bin/env python3
"""
🔍 AGENT 2 - ÉVALUATEUR D'UTILITÉ (GPT-4 TURBO)
Mission: Évaluer l'utilité des outils analysés pour NextGeneration

Architecture Pattern Factory:
- Hérite de Agent de base  
- Implémente méthodes abstraites obligatoires
- Configuration NextGeneration intégrée
- Logging Pattern Factory standardisé

Responsabilités:
- Analyser les résultats de l'Agent 1
- Appliquer des critères d'évaluation pondérés
- Détecter les conflits et redondances
- Sélectionner les outils les plus utiles
- Prioriser l'ordre d'intégration
"""

import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

# Import Pattern Factory (OBLIGATOIRE selon guide)
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Pattern Factory non disponible: {e}")
    # Fallback pour compatibilité
    class Agent:
        def __init__(self, agent_type: str, **config):
            self.agent_id = f"agent_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.agent_type = agent_type
            self.config = config
            self.logger = logging.getLogger(f"Agent2_EvaluateurUtilite")
            
        async def startup(self): pass
        async def shutdown(self): pass
        async def health_check(self): return {"status": "healthy"}
    
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

class AgentEvaluateurUtilite(Agent):
    """Agent spécialisé dans l'évaluation d'utilité avec GPT-4 Turbo - Pattern Factory NextGeneration"""
    
    def __init__(self, **config):
        # Initialisation Pattern Factory
        super().__init__("evaluateur_utilite", **config)
        
        # Critères d'évaluation avec pondération
        self.evaluation_criteria = {
            "technical_relevance": 0.30,      # Pertinence technique pour NextGeneration
            "architecture_compatibility": 0.25, # Compatibilité avec l'architecture existante
            "added_value": 0.20,              # Valeur ajoutée par rapport aux outils existants
            "integration_ease": 0.15,         # Facilité d'intégration
            "maintenance_burden": 0.10        # Charge de maintenance
        }
        
        # Mots-clés NextGeneration pour évaluer la pertinence
        self.nextgen_keywords = {
            "high_priority": ["agent", "orchestrator", "api", "monitoring", "performance", "security"],
            "medium_priority": ["database", "logging", "config", "utility", "automation"],
            "low_priority": ["gui", "desktop", "windows", "macos", "specific"]
        }
        
        # Configuration logging Pattern Factory
        self.logger.info(f"🔍 Agent 2 - Évaluateur Utilité initialisé - ID: {self.agent_id}")
        
    # Implémentation méthodes abstraites OBLIGATOIRES
    async def startup(self):
        """Démarrage agent évaluateur utilité"""
        self.logger.info(f"🚀 Agent Évaluateur Utilité {self.agent_id} - DÉMARRAGE")
        
        # Vérifications de démarrage
        self.logger.info(f"✅ Critères d'évaluation configurés: {len(self.evaluation_criteria)} critères")
        self.logger.info(f"✅ Mots-clés NextGeneration chargés: {sum(len(v) for v in self.nextgen_keywords.values())} mots-clés")
        
    async def shutdown(self):
        """Arrêt agent évaluateur utilité"""
        self.logger.info(f"🛑 Agent Évaluateur Utilité {self.agent_id} - ARRÊT")
        
        # Nettoyage des ressources si nécessaires
        
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé agent évaluateur utilité"""
        health_status = {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "healthy",
            "evaluation_criteria_loaded": len(self.evaluation_criteria) > 0,
            "keywords_loaded": len(self.nextgen_keywords) > 0,
            "ready_for_evaluation": True,
            "timestamp": datetime.now().isoformat()
        }
        
        return health_status
    
    # Méthodes métier (logique existante adaptée)
    async def evaluate_tools_utility(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Évaluation complète de l'utilité des outils analysés - Version Pattern Factory"""
        self.logger.info("🎯 [TARGET] Démarrage évaluation utilité des outils")
        
        tools = analysis_data.get("tools", [])
        if not tools:
            self.logger.warning("⚠️ Aucun outil à évaluer")
            return {"selected_tools": [], "rejected_tools": [], "evaluation_summary": {}}
            
        # Évaluation de chaque outil
        evaluated_tools = []
        for tool in tools:
            evaluation = await self.evaluate_single_tool(tool)
            evaluated_tools.append(evaluation)
            
        # Tri par score d'utilité
        evaluated_tools.sort(key=lambda x: x["utility_score"], reverse=True)
        
        # Détection des conflits et redondances
        conflict_analysis = await self.detect_conflicts_and_redundancies(evaluated_tools)
        
        # Sélection finale des outils
        selection_results = await self.select_tools(evaluated_tools, conflict_analysis)
        
        # Génération du rapport d'évaluation
        evaluation_summary = await self.generate_evaluation_summary(evaluated_tools, selection_results)
        
        results = {
            "selected_tools": selection_results["selected"],
            "rejected_tools": selection_results["rejected"],
            "conflicted_tools": conflict_analysis["conflicts"],
            "evaluation_summary": evaluation_summary,
            "total_evaluated": len(evaluated_tools)
        }
        
        self.logger.info(f"✅ [CHECK] Évaluation terminée: {len(results['selected_tools'])} outils sélectionnés")
        return results
        
    async def evaluate_single_tool(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """Évaluation détaillée d'un outil unique"""
        evaluation = tool.copy()
        
        # Calcul des scores pour chaque critère
        scores = {}
        scores["technical_relevance"] = await self.evaluate_technical_relevance(tool)
        scores["architecture_compatibility"] = await self.evaluate_architecture_compatibility(tool)
        scores["added_value"] = await self.evaluate_added_value(tool)
        scores["integration_ease"] = await self.evaluate_integration_ease(tool)
        scores["maintenance_burden"] = await self.evaluate_maintenance_burden(tool)
        
        # Calcul du score d'utilité pondéré
        utility_score = sum(
            scores[criterion] * weight 
            for criterion, weight in self.evaluation_criteria.items()
        )
        
        evaluation.update({
            "criterion_scores": scores,
            "utility_score": round(utility_score, 2),
            "recommendation": await self.generate_recommendation(utility_score, scores),
            "integration_priority": await self.determine_integration_priority(utility_score, tool)
        })
        
        return evaluation
        
    async def evaluate_technical_relevance(self, tool: Dict[str, Any]) -> float:
        """Évaluation de la pertinence technique (0-100)"""
        score = 0
        
        # Score basé sur le type d'outil
        tool_type = tool.get("tool_type", "unknown")
        type_scores = {
            "api": 90, "monitoring": 85, "automation": 80, "security": 85,
            "data": 75, "utility": 70, "network": 75, "file": 65,
            "conversion": 60, "generation": 55, "unknown": 30
        }
        score += type_scores.get(tool_type, 30)
        
        # Bonus pour les mots-clés NextGeneration
        name_lower = tool.get("name", "").lower()
        docstring_lower = (tool.get("docstring") or "").lower()
        
        for keyword in self.nextgen_keywords["high_priority"]:
            if keyword in name_lower or keyword in docstring_lower:
                score += 15
                
        for keyword in self.nextgen_keywords["medium_priority"]:
            if keyword in name_lower or keyword in docstring_lower:
                score += 8
                
        # Malus pour les mots-clés de faible priorité
        for keyword in self.nextgen_keywords["low_priority"]:
            if keyword in name_lower or keyword in docstring_lower:
                score -= 20
                
        # Bonus pour les indicateurs d'utilité
        utility_indicators = tool.get("utility_indicators", [])
        if "async_capable" in utility_indicators:
            score += 10
        if "has_logging" in utility_indicators:
            score += 8
        if "configurable" in utility_indicators:
            score += 5
            
        return max(0, min(100, score))
        
    async def evaluate_architecture_compatibility(self, tool: Dict[str, Any]) -> float:
        """Évaluation de la compatibilité architecturale (0-100)"""
        score = 70  # Score de base
        
        # Bonus pour les patterns architecturaux compatibles
        imports = tool.get("imports", [])
        
        compatible_libs = ["fastapi", "pydantic", "asyncio", "pathlib", "logging"]
        for lib in compatible_libs:
            if any(lib in imp for imp in imports):
                score += 8
                
        # Bonus pour la structure orientée objet
        if tool.get("classes", []):
            score += 10
            
        # Bonus pour les fonctions async
        if any(f.get("is_async", False) for f in tool.get("functions", [])):
            score += 12
            
        # Malus pour les dépendances problématiques
        problematic_libs = ["tkinter", "pygame", "win32", "pywin32"]
        for lib in problematic_libs:
            if any(lib in imp for imp in imports):
                score -= 25
                
        return max(0, min(100, score))
        
    async def evaluate_added_value(self, tool: Dict[str, Any]) -> float:
        """Évaluation de la valeur ajoutée (0-100)"""
        score = 50  # Score de base
        
        # Bonus pour la complexité (outils sophistiqués)
        complexity = tool.get("complexity_score", 0)
        if complexity > 50:
            score += 20
        elif complexity > 25:
            score += 10
            
        # Bonus pour les fonctionnalités multiples
        functions_count = len(tool.get("functions", []))
        if functions_count > 10:
            score += 15
        elif functions_count > 5:
            score += 8
            
        # Bonus pour la documentation
        if tool.get("docstring"):
            score += 10
            
        # Bonus pour les utilitaires spécialisés
        utility_indicators = tool.get("utility_indicators", [])
        if "cli_interface" in utility_indicators:
            score += 12
        if "executable_script" in utility_indicators:
            score += 8
            
        return max(0, min(100, score))
        
    async def evaluate_integration_ease(self, tool: Dict[str, Any]) -> float:
        """Évaluation de la facilité d'intégration (0-100)"""
        score = 60  # Score de base
        
        # Bonus pour les petits outils (plus faciles à intégrer)
        lines_count = tool.get("lines_count", 0)
        if lines_count < 100:
            score += 20
        elif lines_count < 300:
            score += 10
        elif lines_count > 1000:
            score -= 15
            
        # Bonus pour peu de dépendances
        imports_count = len(tool.get("imports", []))
        if imports_count < 5:
            score += 15
        elif imports_count < 10:
            score += 8
        elif imports_count > 20:
            score -= 10
            
        # Bonus pour les outils bien structurés
        if tool.get("utility_indicators", []):
            if "documented" in tool["utility_indicators"]:
                score += 12
            if "configurable" in tool["utility_indicators"]:
                score += 8
                
        return max(0, min(100, score))
        
    async def evaluate_maintenance_burden(self, tool: Dict[str, Any]) -> float:
        """Évaluation de la charge de maintenance (0-100, 100 = faible charge)"""
        score = 70  # Score de base
        
        # Malus pour la complexité élevée
        complexity = tool.get("complexity_score", 0)
        if complexity > 100:
            score -= 30
        elif complexity > 50:
            score -= 15
            
        # Bonus pour la documentation
        if tool.get("docstring"):
            score += 15
            
        utility_indicators = tool.get("utility_indicators", [])
        if "functions_documented" in utility_indicators:
            score += 10
            
        # Malus pour les dépendances externes nombreuses
        external_deps = [imp for imp in tool.get("imports", []) 
                        if not imp.startswith(("os", "sys", "json", "re", "time"))]
        if len(external_deps) > 15:
            score -= 20
        elif len(external_deps) > 8:
            score -= 10
            
        return max(0, min(100, score))
        
    async def detect_conflicts_and_redundancies(self, evaluated_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Détection des conflits et redondances entre outils"""
        conflicts = []
        redundancies = []
        
        # Grouper par type d'outil
        tools_by_type = {}
        for tool in evaluated_tools:
            tool_type = tool.get("tool_type", "unknown")
            if tool_type not in tools_by_type:
                tools_by_type[tool_type] = []
            tools_by_type[tool_type].append(tool)
            
        # Détecter les redondances dans chaque type
        for tool_type, tools in tools_by_type.items():
            if len(tools) > 1:
                # Trier par score d'utilité
                sorted_tools = sorted(tools, key=lambda x: x["utility_score"], reverse=True)
                
                # Le premier est gardé, les autres sont considérés comme redondants
                best_tool = sorted_tools[0]
                redundant_tools = sorted_tools[1:]
                
                for redundant in redundant_tools:
                    redundancies.append({
                        "redundant_tool": redundant["name"],
                        "better_alternative": best_tool["name"],
                        "type": tool_type,
                        "score_difference": best_tool["utility_score"] - redundant["utility_score"]
                    })
                    
        # Détecter les conflits potentiels (noms similaires, fonctionnalités overlapping)
        for i, tool1 in enumerate(evaluated_tools):
            for tool2 in evaluated_tools[i+1:]:
                similarity = await self.calculate_tool_similarity(tool1, tool2)
                if similarity > 0.7:  # Seuil de similarité
                    conflicts.append({
                        "tool1": tool1["name"],
                        "tool2": tool2["name"],
                        "similarity_score": similarity,
                        "conflict_type": "high_similarity"
                    })
                    
        return {
            "conflicts": conflicts,
            "redundancies": redundancies
        }
        
    async def calculate_tool_similarity(self, tool1: Dict[str, Any], tool2: Dict[str, Any]) -> float:
        """Calcul de la similarité entre deux outils"""
        similarity_score = 0
        
        # Similarité des noms
        name1 = tool1.get("name", "").lower()
        name2 = tool2.get("name", "").lower()
        
        # Simple comparaison de mots communs
        words1 = set(name1.split("_"))
        words2 = set(name2.split("_"))
        
        if words1 and words2:
            common_words = words1.intersection(words2)
            similarity_score += len(common_words) / max(len(words1), len(words2)) * 0.4
            
        # Similarité des types
        if tool1.get("tool_type") == tool2.get("tool_type"):
            similarity_score += 0.3
            
        # Similarité des imports
        imports1 = set(tool1.get("imports", []))
        imports2 = set(tool2.get("imports", []))
        
        if imports1 and imports2:
            common_imports = imports1.intersection(imports2)
            similarity_score += len(common_imports) / max(len(imports1), len(imports2)) * 0.3
            
        return similarity_score
        
    async def select_tools(self, evaluated_tools: List[Dict[str, Any]], 
                    conflict_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Sélection finale des outils à intégrer"""
        
        # Seuil de score pour la sélection
        SELECTION_THRESHOLD = 60.0
        
        selected = []
        rejected = []
        
        # Outils redondants à éviter
        redundant_names = {r["redundant_tool"] for r in conflict_analysis["redundancies"]}
        
        for tool in evaluated_tools:
            tool_name = tool["name"]
            utility_score = tool["utility_score"]
            
            # Critères de sélection
            if (utility_score >= SELECTION_THRESHOLD and 
                tool_name not in redundant_names):
                selected.append(tool)
            else:
                rejection_reason = []
                if utility_score < SELECTION_THRESHOLD:
                    rejection_reason.append(f"score_too_low_{utility_score}")
                if tool_name in redundant_names:
                    rejection_reason.append("redundant")
                    
                tool["rejection_reason"] = rejection_reason
                rejected.append(tool)
                
        return {
            "selected": selected,
            "rejected": rejected
        }
        
    async def determine_integration_priority(self, utility_score: float, tool: Dict[str, Any]) -> str:
        """Détermination de la priorité d'intégration"""
        if utility_score >= 80:
            return "HIGH"
        elif utility_score >= 65:
            return "MEDIUM"
        elif utility_score >= 50:
            return "LOW"
        else:
            return "SKIP"
            
    async def generate_recommendation(self, utility_score: float, scores: Dict[str, float]) -> str:
        """Génération d'une recommandation basée sur les scores"""
        if utility_score >= 75:
            return "STRONGLY_RECOMMENDED"
        elif utility_score >= 60:
            return "RECOMMENDED"
        elif utility_score >= 45:
            return "CONDITIONAL"
        else:
            return "NOT_RECOMMENDED"
            
    async def generate_evaluation_summary(self, evaluated_tools: List[Dict[str, Any]], 
                                  selection_results: Dict[str, Any]) -> Dict[str, Any]:
        """Génération du résumé d'évaluation"""
        
        # Statistiques générales
        total_tools = len(evaluated_tools)
        selected_count = len(selection_results["selected"])
        rejected_count = len(selection_results["rejected"])
        
        # Répartition par score
        score_distribution = {
            "excellent": len([t for t in evaluated_tools if t["utility_score"] >= 80]),
            "good": len([t for t in evaluated_tools if 60 <= t["utility_score"] < 80]),
            "average": len([t for t in evaluated_tools if 40 <= t["utility_score"] < 60]),
            "poor": len([t for t in evaluated_tools if t["utility_score"] < 40])
        }
        
        # Répartition par type d'outil sélectionné
        selected_by_type = {}
        for tool in selection_results["selected"]:
            tool_type = tool.get("tool_type", "unknown")
            selected_by_type[tool_type] = selected_by_type.get(tool_type, 0) + 1
            
        return {
            "total_evaluated": total_tools,
            "selected_count": selected_count,
            "rejected_count": rejected_count,
            "selection_rate": round(selected_count / total_tools * 100, 1) if total_tools > 0 else 0,
            "score_distribution": score_distribution,
            "selected_by_type": selected_by_type,
            "average_score_selected": round(
                sum(t["utility_score"] for t in selection_results["selected"]) / selected_count, 1
            ) if selected_count > 0 else 0
        }
    
    # Méthodes spécialisées Apex (conservées avec adaptations async)
    async def evaluer_outils_apex(self, phase1_data: Dict[str, Any]) -> Dict[str, Any]:
        """Évaluation spécialisée des outils Apex_VBA_FRAMEWORK pour NextGeneration - Version Pattern Factory"""
        self.logger.info("🎯 [TARGET] Évaluation spécialisée outils Apex_VBA_FRAMEWORK")
        
        outils_selectionnes = []
        evaluations_detaillees = []
        
        # Récupérer les outils analysés
        detailed_analysis = phase1_data.get("detailed_analysis", {})
        
        # Évaluer les outils Python (priorité haute pour NextGeneration)
        python_tools = detailed_analysis.get("python_tools", [])
        for tool in python_tools:
            score = await self._evaluer_outil_apex_python(tool)
            
            evaluation = {
                "name": tool["name"],
                "path": tool["path"],
                "type": "python",
                "apex_subdir": tool.get("apex_subdir", "unknown"),
                "score_total": score["total"],
                "scores_detail": score,
                "selected": score["total"] >= 75.0,  # Seuil pour sélection
                "priority": await self._calculer_priorite_apex(tool, score["total"])
            }
            
            evaluations_detaillees.append(evaluation)
            
            if evaluation["selected"]:
                outils_selectionnes.append(evaluation)
        
        # Évaluer les outils PowerShell (priorité moyenne)
        powershell_tools = detailed_analysis.get("powershell_tools", [])
        for tool in powershell_tools:
            score = await self._evaluer_outil_apex_powershell(tool)
            
            evaluation = {
                "name": tool["name"],
                "path": tool["path"],
                "type": "powershell",
                "apex_subdir": tool.get("apex_subdir", "unknown"),
                "score_total": score["total"],
                "scores_detail": score,
                "selected": score["total"] >= 70.0,  # Seuil plus bas pour PowerShell
                "priority": await self._calculer_priorite_apex(tool, score["total"])
            }
            
            evaluations_detaillees.append(evaluation)
            
            if evaluation["selected"]:
                outils_selectionnes.append(evaluation)
        
        # Évaluer les outils Batch (priorité basse)
        batch_tools = detailed_analysis.get("batch_tools", [])
        for tool in batch_tools:
            score = await self._evaluer_outil_apex_batch(tool)
            
            evaluation = {
                "name": tool["name"],
                "path": tool["path"],
                "type": "batch",
                "apex_subdir": tool.get("apex_subdir", "unknown"),
                "score_total": score["total"],
                "scores_detail": score,
                "selected": score["total"] >= 65.0,  # Seuil encore plus bas pour Batch
                "priority": await self._calculer_priorite_apex(tool, score["total"])
            }
            
            evaluations_detaillees.append(evaluation)
            
            if evaluation["selected"]:
                outils_selectionnes.append(evaluation)
        
        # Trier par score décroissant
        outils_selectionnes.sort(key=lambda x: x["score_total"], reverse=True)
        
        # Limiter à 10 outils maximum pour éviter la surcharge
        outils_selectionnes = outils_selectionnes[:10]
        
        resultats = {
            "total_evaluated": len(evaluations_detaillees),
            "total_selected": len(outils_selectionnes),
            "outils_selectionnes": outils_selectionnes,
            "evaluations_completes": evaluations_detaillees,
            "selection_criteria": {
                "python_threshold": 75.0,
                "powershell_threshold": 70.0,
                "batch_threshold": 65.0,
                "max_selection": 10
            },
            "evaluation_timestamp": datetime.now().isoformat(),
            "evaluator_model": "GPT-4 Turbo - Pattern Factory"
        }
        
        self.logger.info(f"✅ [CHECK] Évaluation Apex terminée: {len(outils_selectionnes)} outils sélectionnés")
        return resultats
    
    async def _evaluer_outil_apex_python(self, tool: Dict[str, Any]) -> Dict[str, float]:
        """Évaluation spécialisée pour un outil Python d'Apex"""
        scores = {}
        
        # Pertinence technique (30%)
        scores["pertinence_technique"] = await self._score_pertinence_apex_python(tool) * 0.30
        
        # Compatibilité architecture NextGeneration (25%)
        scores["compatibilite_architecture"] = await self._score_compatibilite_apex(tool) * 0.25
        
        # Valeur ajoutée (20%)
        scores["valeur_ajoutee"] = await self._score_valeur_ajoutee_apex(tool) * 0.20
        
        # Facilité d'intégration (15%)
        scores["facilite_integration"] = await self._score_facilite_integration_apex(tool) * 0.15
        
        # Maintenance et évolutivité (10%)
        scores["maintenance"] = await self._score_maintenance_apex(tool) * 0.10
        
        scores["total"] = sum(scores.values())
        return scores
    
    async def _evaluer_outil_apex_powershell(self, tool: Dict[str, Any]) -> Dict[str, float]:
        """Évaluation spécialisée pour un outil PowerShell d'Apex"""
        scores = {}
        
        # Adaptation des critères pour PowerShell
        scores["pertinence_technique"] = await self._score_pertinence_powershell(tool) * 0.35
        scores["compatibilite_architecture"] = 60.0 * 0.20  # Score fixe plus bas
        scores["valeur_ajoutee"] = await self._score_valeur_ajoutee_apex(tool) * 0.25
        scores["facilite_integration"] = 50.0 * 0.15  # Plus difficile à intégrer
        scores["maintenance"] = 70.0 * 0.05  # Maintenance plus complexe
        
        scores["total"] = sum(scores.values())
        return scores
    
    async def _evaluer_outil_apex_batch(self, tool: Dict[str, Any]) -> Dict[str, float]:
        """Évaluation spécialisée pour un outil Batch d'Apex"""
        scores = {}
        
        # Adaptation des critères pour Batch
        scores["pertinence_technique"] = await self._score_pertinence_batch(tool) * 0.40
        scores["compatibilite_architecture"] = 40.0 * 0.15  # Score fixe bas
        scores["valeur_ajoutee"] = await self._score_valeur_ajoutee_apex(tool) * 0.30
        scores["facilite_integration"] = 30.0 * 0.10  # Très difficile à intégrer
        scores["maintenance"] = 50.0 * 0.05  # Maintenance limitée
        
        scores["total"] = sum(scores.values())
        return scores
    
    async def _score_pertinence_apex_python(self, tool: Dict[str, Any]) -> float:
        """Score de pertinence technique pour Python Apex"""
        score = 50.0  # Score de base
        
        # Bonus pour les outils d'automatisation
        if "automation" in tool.get("name", "").lower():
            score += 20.0
        
        # Bonus pour les outils de monitoring
        if "monitor" in tool.get("name", "").lower():
            score += 15.0
        
        # Bonus pour les générateurs
        if "generat" in tool.get("name", "").lower():
            score += 15.0
        
        # Bonus pour les outils Excel (spécificité Apex)
        if "excel" in tool.get("apex_subdir", "").lower():
            score += 25.0
        
        # Bonus pour la complexité
        complexity = tool.get("complexity_score", 0)
        if complexity > 20:
            score += 10.0
        elif complexity > 10:
            score += 5.0
        
        return min(score, 100.0)
    
    async def _score_pertinence_powershell(self, tool: Dict[str, Any]) -> float:
        """Score de pertinence pour PowerShell"""
        score = 40.0  # Score de base plus bas
        
        # Bonus pour les outils d'administration
        if any(keyword in tool.get("name", "").lower() 
               for keyword in ["admin", "manage", "config", "setup"]):
            score += 20.0
        
        # Bonus pour les outils de migration
        if "migration" in tool.get("apex_subdir", "").lower():
            score += 15.0
        
        return min(score, 100.0)
    
    async def _score_pertinence_batch(self, tool: Dict[str, Any]) -> float:
        """Score de pertinence pour Batch"""
        score = 30.0  # Score de base bas
        
        # Bonus pour les outils de build/déploiement
        if any(keyword in tool.get("name", "").lower() 
               for keyword in ["build", "deploy", "install", "setup"]):
            score += 25.0
        
        return min(score, 100.0)
    
    async def _score_compatibilite_apex(self, tool: Dict[str, Any]) -> float:
        """Score de compatibilité avec NextGeneration pour outils Apex"""
        score = 60.0  # Score de base
        
        # Bonus pour les outils dans certains répertoires Apex
        apex_subdir = tool.get("apex_subdir", "").lower()
        
        if apex_subdir in ["python", "automation", "monitoring"]:
            score += 20.0
        elif apex_subdir in ["excel", "generators", "utilities"]:
            score += 15.0
        elif apex_subdir in ["migration", "workflow"]:
            score += 10.0
        
        return min(score, 100.0)
    
    async def _score_valeur_ajoutee_apex(self, tool: Dict[str, Any]) -> float:
        """Score de valeur ajoutée spécifique à Apex"""
        score = 50.0
        
        # Valeur ajoutée basée sur le répertoire Apex
        apex_subdir = tool.get("apex_subdir", "").lower()
        
        # Outils d'Excel automation (très utiles)
        if "excel" in apex_subdir:
            score += 30.0
        
        # Outils de génération de code
        if "generat" in apex_subdir:
            score += 25.0
        
        # Outils d'automatisation
        if "automation" in apex_subdir:
            score += 20.0
        
        return min(score, 100.0)
    
    async def _score_facilite_integration_apex(self, tool: Dict[str, Any]) -> float:
        """Score de facilité d'intégration pour outils Apex"""
        score = 70.0  # Score de base pour Python
        
        # Malus selon le type
        if tool.get("type") == "powershell":
            score -= 20.0
        elif tool.get("type") == "batch":
            score -= 40.0
        
        return max(score, 10.0)
    
    async def _score_maintenance_apex(self, tool: Dict[str, Any]) -> float:
        """Score de maintenance pour outils Apex"""
        score = 70.0
        
        # Ajustement selon le type d'outil
        if tool.get("type") == "python":
            score += 10.0
        elif tool.get("type") == "powershell":
            score -= 10.0
        elif tool.get("type") == "batch":
            score -= 20.0
        
        return max(score, 30.0)
    
    async def _calculer_priorite_apex(self, tool: Dict[str, Any], score_total: float) -> str:
        """Calcul de la priorité pour un outil Apex"""
        if score_total >= 85.0:
            return "HIGH"
        elif score_total >= 75.0:
            return "MEDIUM"
        elif score_total >= 65.0:
            return "LOW"
        else:
            return "SKIP"

# Fonction factory pour créer l'agent (Pattern Factory)
def create_agent_evaluateur_utilite(**config) -> AgentEvaluateurUtilite:
    """Factory function pour créer un Agent Évaluateur Utilité conforme Pattern Factory"""
    return AgentEvaluateurUtilite(**config)

# Test de l'agent si exécuté directement
async def main():
    """Test de l'agent Pattern Factory"""
    # Test avec des données simulées
    test_data = {
        "tools": [
            {
                "name": "api_monitor",
                "tool_type": "monitoring",
                "functions": [{"name": "check_health", "is_async": True}],
                "classes": [],
                "imports": ["asyncio", "requests"],
                "complexity_score": 45,
                "utility_indicators": ["async_capable", "has_logging"],
                "docstring": "API monitoring tool for health checks"
            }
        ]
    }
    
    # Créer l'agent via factory
    agent = create_agent_evaluateur_utilite()
    
    try:
        # Démarrage Pattern Factory
        await agent.startup()
        
        # Vérification santé
        health = await agent.health_check()
        print(f"🏥 Health Check: {health}")
        
        # Exécution mission
        results = await agent.evaluate_tools_utility(test_data)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
        # Arrêt propre
        await agent.shutdown()
        
    except Exception as e:
        print(f"❌ Erreur execution agent: {e}")
        await agent.shutdown()

if __name__ == "__main__":
    asyncio.run(main())

# Fonction factory pour créer l'agent (Pattern Factory)
def create_agent_2EvaluateurUtilite(**config):
    """Factory function pour créer un Agent 2EvaluateurUtilite conforme Pattern Factory"""

    async def execute_task(self, task: Any) -> Any:
        """Exécution d'une tâche spécifique - Méthode abstraite obligatoire"""
        try:
            self.logger.info(f"📋 Exécution tâche: {task}")
            # Logique métier à adapter
            return {"success": True, "result": "Task executed"}
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution tâche: {e}")
            return {"error": str(e)}


    def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'agent - Méthode abstraite obligatoire"""
        return ["basic_capability"]

    return Agent2EvaluateurUtilite(**config)

# Fonction factory pour créer l'agent (Pattern Factory)
def create_agent_2EvaluateurUtilite(**config):
    """Factory function pour créer un Agent 2EvaluateurUtilite conforme Pattern Factory"""
    return Agent2EvaluateurUtilite(**config)

# Fonction factory pour créer l'agent (Pattern Factory)
def create_agent_2EvaluateurUtilite(**config):
    """Factory function pour créer un Agent 2EvaluateurUtilite conforme Pattern Factory"""
    return Agent2EvaluateurUtilite(**config)

# Fonction factory pour créer l'agent (Pattern Factory)
def create_agent_2EvaluateurUtilite(**config):
    """Factory function pour créer un Agent 2EvaluateurUtilite conforme Pattern Factory"""
    return Agent2EvaluateurUtilite(**config)