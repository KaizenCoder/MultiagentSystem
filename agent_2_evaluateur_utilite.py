#!/usr/bin/env python3
"""
Agent 2 - Évaluateur d'Utilité (GPT-4 Turbo)
Mission: Évaluer l'utilité des outils analysés pour NextGeneration

Responsabilités:
- Analyser les résultats de l'Agent 1
- Appliquer des critères d'évaluation pondérés
- Détecter les conflits et redondances
- Sélectionner les outils les plus utiles
- Prioriser l'ordre d'intégration
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

class AgentEvaluateurUtilite:
    """Agent spécialisé dans l'évaluation d'utilité avec GPT-4 Turbo"""
    
    def __init__(self):
        self.logger = logging.getLogger("Agent2_EvaluateurUtilite")
        
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
        
    def evaluate_tools_utility(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Évaluation complète de l'utilité des outils analysés"""
        self.logger.info("🎯 Démarrage évaluation utilité des outils")
        
        tools = analysis_data.get("tools", [])
        if not tools:
            self.logger.warning("⚠️ Aucun outil à évaluer")
            return {"selected_tools": [], "rejected_tools": [], "evaluation_summary": {}}
            
        # Évaluation de chaque outil
        evaluated_tools = []
        for tool in tools:
            evaluation = self.evaluate_single_tool(tool)
            evaluated_tools.append(evaluation)
            
        # Tri par score d'utilité
        evaluated_tools.sort(key=lambda x: x["utility_score"], reverse=True)
        
        # Détection des conflits et redondances
        conflict_analysis = self.detect_conflicts_and_redundancies(evaluated_tools)
        
        # Sélection finale des outils
        selection_results = self.select_tools(evaluated_tools, conflict_analysis)
        
        # Génération du rapport d'évaluation
        evaluation_summary = self.generate_evaluation_summary(evaluated_tools, selection_results)
        
        results = {
            "selected_tools": selection_results["selected"],
            "rejected_tools": selection_results["rejected"],
            "conflicted_tools": conflict_analysis["conflicts"],
            "evaluation_summary": evaluation_summary,
            "total_evaluated": len(evaluated_tools)
        }
        
        self.logger.info(f"✅ Évaluation terminée: {len(results['selected_tools'])} outils sélectionnés")
        return results
        
    def evaluate_single_tool(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """Évaluation détaillée d'un outil unique"""
        evaluation = tool.copy()
        
        # Calcul des scores pour chaque critère
        scores = {}
        scores["technical_relevance"] = self.evaluate_technical_relevance(tool)
        scores["architecture_compatibility"] = self.evaluate_architecture_compatibility(tool)
        scores["added_value"] = self.evaluate_added_value(tool)
        scores["integration_ease"] = self.evaluate_integration_ease(tool)
        scores["maintenance_burden"] = self.evaluate_maintenance_burden(tool)
        
        # Calcul du score d'utilité pondéré
        utility_score = sum(
            scores[criterion] * weight 
            for criterion, weight in self.evaluation_criteria.items()
        )
        
        evaluation.update({
            "criterion_scores": scores,
            "utility_score": round(utility_score, 2),
            "recommendation": self.generate_recommendation(utility_score, scores),
            "integration_priority": self.determine_integration_priority(utility_score, tool)
        })
        
        return evaluation
        
    def evaluate_technical_relevance(self, tool: Dict[str, Any]) -> float:
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
        
    def evaluate_architecture_compatibility(self, tool: Dict[str, Any]) -> float:
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
        
    def evaluate_added_value(self, tool: Dict[str, Any]) -> float:
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
        
    def evaluate_integration_ease(self, tool: Dict[str, Any]) -> float:
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
        
    def evaluate_maintenance_burden(self, tool: Dict[str, Any]) -> float:
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
        
    def detect_conflicts_and_redundancies(self, evaluated_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                similarity = self.calculate_tool_similarity(tool1, tool2)
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
        
    def calculate_tool_similarity(self, tool1: Dict[str, Any], tool2: Dict[str, Any]) -> float:
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
        
    def select_tools(self, evaluated_tools: List[Dict[str, Any]], 
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
        
    def determine_integration_priority(self, utility_score: float, tool: Dict[str, Any]) -> str:
        """Détermination de la priorité d'intégration"""
        if utility_score >= 80:
            return "HIGH"
        elif utility_score >= 65:
            return "MEDIUM"
        elif utility_score >= 50:
            return "LOW"
        else:
            return "SKIP"
            
    def generate_recommendation(self, utility_score: float, scores: Dict[str, float]) -> str:
        """Génération d'une recommandation basée sur les scores"""
        if utility_score >= 75:
            return "STRONGLY_RECOMMENDED"
        elif utility_score >= 60:
            return "RECOMMENDED"
        elif utility_score >= 45:
            return "CONDITIONAL"
        else:
            return "NOT_RECOMMENDED"
            
    def generate_evaluation_summary(self, evaluated_tools: List[Dict[str, Any]], 
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

# Test de l'agent si exécuté directement
if __name__ == "__main__":
    import sys
    
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
    
    agent = AgentEvaluateurUtilite()
    results = agent.evaluate_tools_utility(test_data)
    
    print(json.dumps(results, indent=2, ensure_ascii=False)) 