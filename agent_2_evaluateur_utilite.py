#!/usr/bin/env python3
"""
Agent 2 - valuateur d'Utilit (GPT-4 Turbo)
Mission: valuer l'utilit des outils analyss pour NextGeneration

Responsabilits:
- Analyser les rsultats de l'Agent 1
- Appliquer des critres d'valuation pondrs
- Dtecter les conflits et redondances
- Slectionner les outils les plus utiles
- Prioriser l'ordre d'intgration
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

class AgentEvaluateurUtilite:
    """Agent spcialis dans l'valuation d'utilit avec GPT-4 Turbo"""
    
    def __init__(self):
        self.logger = logging.getLogger("Agent2_EvaluateurUtilite")
        
        # Critres d'valuation avec pondration
        self.evaluation_criteria = {
            "technical_relevance": 0.30,      # Pertinence technique pour NextGeneration
            "architecture_compatibility": 0.25, # Compatibilit avec l'architecture existante
            "added_value": 0.20,              # Valeur ajoute par rapport aux outils existants
            "integration_ease": 0.15,         # Facilit d'intgration
            "maintenance_burden": 0.10        # Charge de maintenance
        }
        
        # Mots-cls NextGeneration pour valuer la pertinence
        self.nextgen_keywords = {
            "high_priority": ["agent", "orchestrator", "api", "monitoring", "performance", "security"],
            "medium_priority": ["database", "logging", "config", "utility", "automation"],
            "low_priority": ["gui", "desktop", "windows", "macos", "specific"]
        }
        
    def evaluate_tools_utility(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """valuation complte de l'utilit des outils analyss"""
        self.logger.info("[TARGET] Dmarrage valuation utilit des outils")
        
        tools = analysis_data.get("tools", [])
        if not tools:
            self.logger.warning(" Aucun outil  valuer")
            return {"selected_tools": [], "rejected_tools": [], "evaluation_summary": {}}
            
        # valuation de chaque outil
        evaluated_tools = []
        for tool in tools:
            evaluation = self.evaluate_single_tool(tool)
            evaluated_tools.append(evaluation)
            
        # Tri par score d'utilit
        evaluated_tools.sort(key=lambda x: x["utility_score"], reverse=True)
        
        # Dtection des conflits et redondances
        conflict_analysis = self.detect_conflicts_and_redundancies(evaluated_tools)
        
        # Slection finale des outils
        selection_results = self.select_tools(evaluated_tools, conflict_analysis)
        
        # Gnration du rapport d'valuation
        evaluation_summary = self.generate_evaluation_summary(evaluated_tools, selection_results)
        
        results = {
            "selected_tools": selection_results["selected"],
            "rejected_tools": selection_results["rejected"],
            "conflicted_tools": conflict_analysis["conflicts"],
            "evaluation_summary": evaluation_summary,
            "total_evaluated": len(evaluated_tools)
        }
        
        self.logger.info(f"[CHECK] valuation termine: {len(results['selected_tools'])} outils slectionns")
        return results
        
    def evaluate_single_tool(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """valuation dtaille d'un outil unique"""
        evaluation = tool.copy()
        
        # Calcul des scores pour chaque critre
        scores = {}
        scores["technical_relevance"] = self.evaluate_technical_relevance(tool)
        scores["architecture_compatibility"] = self.evaluate_architecture_compatibility(tool)
        scores["added_value"] = self.evaluate_added_value(tool)
        scores["integration_ease"] = self.evaluate_integration_ease(tool)
        scores["maintenance_burden"] = self.evaluate_maintenance_burden(tool)
        
        # Calcul du score d'utilit pondr
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
        """valuation de la pertinence technique (0-100)"""
        score = 0
        
        # Score bas sur le type d'outil
        tool_type = tool.get("tool_type", "unknown")
        type_scores = {
            "api": 90, "monitoring": 85, "automation": 80, "security": 85,
            "data": 75, "utility": 70, "network": 75, "file": 65,
            "conversion": 60, "generation": 55, "unknown": 30
        }
        score += type_scores.get(tool_type, 30)
        
        # Bonus pour les mots-cls NextGeneration
        name_lower = tool.get("name", "").lower()
        docstring_lower = (tool.get("docstring") or "").lower()
        
        for keyword in self.nextgen_keywords["high_priority"]:
            if keyword in name_lower or keyword in docstring_lower:
                score += 15
                
        for keyword in self.nextgen_keywords["medium_priority"]:
            if keyword in name_lower or keyword in docstring_lower:
                score += 8
                
        # Malus pour les mots-cls de faible priorit
        for keyword in self.nextgen_keywords["low_priority"]:
            if keyword in name_lower or keyword in docstring_lower:
                score -= 20
                
        # Bonus pour les indicateurs d'utilit
        utility_indicators = tool.get("utility_indicators", [])
        if "async_capable" in utility_indicators:
            score += 10
        if "has_logging" in utility_indicators:
            score += 8
        if "configurable" in utility_indicators:
            score += 5
            
        return max(0, min(100, score))
        
    def evaluate_architecture_compatibility(self, tool: Dict[str, Any]) -> float:
        """valuation de la compatibilit architecturale (0-100)"""
        score = 70  # Score de base
        
        # Bonus pour les patterns architecturaux compatibles
        imports = tool.get("imports", [])
        
        compatible_libs = ["fastapi", "pydantic", "asyncio", "pathlib", "logging"]
        for lib in compatible_libs:
            if any(lib in imp for imp in imports):
                score += 8
                
        # Bonus pour la structure oriente objet
        if tool.get("classes", []):
            score += 10
            
        # Bonus pour les fonctions async
        if any(f.get("is_async", False) for f in tool.get("functions", [])):
            score += 12
            
        # Malus pour les dpendances problmatiques
        problematic_libs = ["tkinter", "pygame", "win32", "pywin32"]
        for lib in problematic_libs:
            if any(lib in imp for imp in imports):
                score -= 25
                
        return max(0, min(100, score))
        
    def evaluate_added_value(self, tool: Dict[str, Any]) -> float:
        """valuation de la valeur ajoute (0-100)"""
        score = 50  # Score de base
        
        # Bonus pour la complexit (outils sophistiqus)
        complexity = tool.get("complexity_score", 0)
        if complexity > 50:
            score += 20
        elif complexity > 25:
            score += 10
            
        # Bonus pour les fonctionnalits multiples
        functions_count = len(tool.get("functions", []))
        if functions_count > 10:
            score += 15
        elif functions_count > 5:
            score += 8
            
        # Bonus pour la documentation
        if tool.get("docstring"):
            score += 10
            
        # Bonus pour les utilitaires spcialiss
        utility_indicators = tool.get("utility_indicators", [])
        if "cli_interface" in utility_indicators:
            score += 12
        if "executable_script" in utility_indicators:
            score += 8
            
        return max(0, min(100, score))
        
    def evaluate_integration_ease(self, tool: Dict[str, Any]) -> float:
        """valuation de la facilit d'intgration (0-100)"""
        score = 60  # Score de base
        
        # Bonus pour les petits outils (plus faciles  intgrer)
        lines_count = tool.get("lines_count", 0)
        if lines_count < 100:
            score += 20
        elif lines_count < 300:
            score += 10
        elif lines_count > 1000:
            score -= 15
            
        # Bonus pour peu de dpendances
        imports_count = len(tool.get("imports", []))
        if imports_count < 5:
            score += 15
        elif imports_count < 10:
            score += 8
        elif imports_count > 20:
            score -= 10
            
        # Bonus pour les outils bien structurs
        if tool.get("utility_indicators", []):
            if "documented" in tool["utility_indicators"]:
                score += 12
            if "configurable" in tool["utility_indicators"]:
                score += 8
                
        return max(0, min(100, score))
        
    def evaluate_maintenance_burden(self, tool: Dict[str, Any]) -> float:
        """valuation de la charge de maintenance (0-100, 100 = faible charge)"""
        score = 70  # Score de base
        
        # Malus pour la complexit leve
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
            
        # Malus pour les dpendances externes nombreuses
        external_deps = [imp for imp in tool.get("imports", []) 
                        if not imp.startswith(("os", "sys", "json", "re", "time"))]
        if len(external_deps) > 15:
            score -= 20
        elif len(external_deps) > 8:
            score -= 10
            
        return max(0, min(100, score))
        
    def detect_conflicts_and_redundancies(self, evaluated_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Dtection des conflits et redondances entre outils"""
        conflicts = []
        redundancies = []
        
        # Grouper par type d'outil
        tools_by_type = {}
        for tool in evaluated_tools:
            tool_type = tool.get("tool_type", "unknown")
            if tool_type not in tools_by_type:
                tools_by_type[tool_type] = []
            tools_by_type[tool_type].append(tool)
            
        # Dtecter les redondances dans chaque type
        for tool_type, tools in tools_by_type.items():
            if len(tools) > 1:
                # Trier par score d'utilit
                sorted_tools = sorted(tools, key=lambda x: x["utility_score"], reverse=True)
                
                # Le premier est gard, les autres sont considrs comme redondants
                best_tool = sorted_tools[0]
                redundant_tools = sorted_tools[1:]
                
                for redundant in redundant_tools:
                    redundancies.append({
                        "redundant_tool": redundant["name"],
                        "better_alternative": best_tool["name"],
                        "type": tool_type,
                        "score_difference": best_tool["utility_score"] - redundant["utility_score"]
                    })
                    
        # Dtecter les conflits potentiels (noms similaires, fonctionnalits overlapping)
        for i, tool1 in enumerate(evaluated_tools):
            for tool2 in evaluated_tools[i+1:]:
                similarity = self.calculate_tool_similarity(tool1, tool2)
                if similarity > 0.7:  # Seuil de similarit
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
        """Calcul de la similarit entre deux outils"""
        similarity_score = 0
        
        # Similarit des noms
        name1 = tool1.get("name", "").lower()
        name2 = tool2.get("name", "").lower()
        
        # Simple comparaison de mots communs
        words1 = set(name1.split("_"))
        words2 = set(name2.split("_"))
        
        if words1 and words2:
            common_words = words1.intersection(words2)
            similarity_score += len(common_words) / max(len(words1), len(words2)) * 0.4
            
        # Similarit des types
        if tool1.get("tool_type") == tool2.get("tool_type"):
            similarity_score += 0.3
            
        # Similarit des imports
        imports1 = set(tool1.get("imports", []))
        imports2 = set(tool2.get("imports", []))
        
        if imports1 and imports2:
            common_imports = imports1.intersection(imports2)
            similarity_score += len(common_imports) / max(len(imports1), len(imports2)) * 0.3
            
        return similarity_score
        
    def select_tools(self, evaluated_tools: List[Dict[str, Any]], 
                    conflict_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Slection finale des outils  intgrer"""
        
        # Seuil de score pour la slection
        SELECTION_THRESHOLD = 60.0
        
        selected = []
        rejected = []
        
        # Outils redondants  viter
        redundant_names = {r["redundant_tool"] for r in conflict_analysis["redundancies"]}
        
        for tool in evaluated_tools:
            tool_name = tool["name"]
            utility_score = tool["utility_score"]
            
            # Critres de slection
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
        """Dtermination de la priorit d'intgration"""
        if utility_score >= 80:
            return "HIGH"
        elif utility_score >= 65:
            return "MEDIUM"
        elif utility_score >= 50:
            return "LOW"
        else:
            return "SKIP"
            
    def generate_recommendation(self, utility_score: float, scores: Dict[str, float]) -> str:
        """Gnration d'une recommandation base sur les scores"""
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
        """Gnration du rsum d'valuation"""
        
        # Statistiques gnrales
        total_tools = len(evaluated_tools)
        selected_count = len(selection_results["selected"])
        rejected_count = len(selection_results["rejected"])
        
        # Rpartition par score
        score_distribution = {
            "excellent": len([t for t in evaluated_tools if t["utility_score"] >= 80]),
            "good": len([t for t in evaluated_tools if 60 <= t["utility_score"] < 80]),
            "average": len([t for t in evaluated_tools if 40 <= t["utility_score"] < 60]),
            "poor": len([t for t in evaluated_tools if t["utility_score"] < 40])
        }
        
        # Rpartition par type d'outil slectionn
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
    
    def evaluer_outils_apex(self, phase1_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        valuation spcialise des outils Apex_VBA_FRAMEWORK pour NextGeneration
        
        Args:
            phase1_data: Donnes d'analyse de la phase 1
            
        Returns:
            Dict contenant les outils slectionns et leur valuation
        """
        self.logger.info("[TARGET] valuation spcialise outils Apex_VBA_FRAMEWORK")
        
        outils_selectionnes = []
        evaluations_detaillees = []
        
        # Rcuprer les outils analyss
        detailed_analysis = phase1_data.get("detailed_analysis", {})
        
        # valuer les outils Python (priorit haute pour NextGeneration)
        python_tools = detailed_analysis.get("python_tools", [])
        for tool in python_tools:
            score = self._evaluer_outil_apex_python(tool)
            
            evaluation = {
                "name": tool["name"],
                "path": tool["path"],
                "type": "python",
                "apex_subdir": tool.get("apex_subdir", "unknown"),
                "score_total": score["total"],
                "scores_detail": score,
                "selected": score["total"] >= 75.0,  # Seuil pour slection
                "priority": self._calculer_priorite_apex(tool, score["total"])
            }
            
            evaluations_detaillees.append(evaluation)
            
            if evaluation["selected"]:
                outils_selectionnes.append(evaluation)
        
        # valuer les outils PowerShell (priorit moyenne)
        powershell_tools = detailed_analysis.get("powershell_tools", [])
        for tool in powershell_tools:
            score = self._evaluer_outil_apex_powershell(tool)
            
            evaluation = {
                "name": tool["name"],
                "path": tool["path"],
                "type": "powershell",
                "apex_subdir": tool.get("apex_subdir", "unknown"),
                "score_total": score["total"],
                "scores_detail": score,
                "selected": score["total"] >= 70.0,  # Seuil plus bas pour PowerShell
                "priority": self._calculer_priorite_apex(tool, score["total"])
            }
            
            evaluations_detaillees.append(evaluation)
            
            if evaluation["selected"]:
                outils_selectionnes.append(evaluation)
        
        # valuer les outils Batch (priorit basse)
        batch_tools = detailed_analysis.get("batch_tools", [])
        for tool in batch_tools:
            score = self._evaluer_outil_apex_batch(tool)
            
            evaluation = {
                "name": tool["name"],
                "path": tool["path"],
                "type": "batch",
                "apex_subdir": tool.get("apex_subdir", "unknown"),
                "score_total": score["total"],
                "scores_detail": score,
                "selected": score["total"] >= 65.0,  # Seuil encore plus bas pour Batch
                "priority": self._calculer_priorite_apex(tool, score["total"])
            }
            
            evaluations_detaillees.append(evaluation)
            
            if evaluation["selected"]:
                outils_selectionnes.append(evaluation)
        
        # Trier par score dcroissant
        outils_selectionnes.sort(key=lambda x: x["score_total"], reverse=True)
        
        # Limiter  10 outils maximum pour viter la surcharge
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
            "evaluator_model": "GPT-4 Turbo"
        }
        
        self.logger.info(f"[CHECK] valuation Apex termine: {len(outils_selectionnes)} outils slectionns")
        return resultats
    
    def _evaluer_outil_apex_python(self, tool: Dict[str, Any]) -> Dict[str, float]:
        """valuation spcialise pour un outil Python d'Apex"""
        scores = {}
        
        # Pertinence technique (30%)
        scores["pertinence_technique"] = self._score_pertinence_apex_python(tool) * 0.30
        
        # Compatibilit architecture NextGeneration (25%)
        scores["compatibilite_architecture"] = self._score_compatibilite_apex(tool) * 0.25
        
        # Valeur ajoute (20%)
        scores["valeur_ajoutee"] = self._score_valeur_ajoutee_apex(tool) * 0.20
        
        # Facilit d'intgration (15%)
        scores["facilite_integration"] = self._score_facilite_integration_apex(tool) * 0.15
        
        # Maintenance et volutivit (10%)
        scores["maintenance"] = self._score_maintenance_apex(tool) * 0.10
        
        scores["total"] = sum(scores.values())
        return scores
    
    def _evaluer_outil_apex_powershell(self, tool: Dict[str, Any]) -> Dict[str, float]:
        """valuation spcialise pour un outil PowerShell d'Apex"""
        scores = {}
        
        # Adaptation des critres pour PowerShell
        scores["pertinence_technique"] = self._score_pertinence_powershell(tool) * 0.35
        scores["compatibilite_architecture"] = 60.0 * 0.20  # Score fixe plus bas
        scores["valeur_ajoutee"] = self._score_valeur_ajoutee_apex(tool) * 0.25
        scores["facilite_integration"] = 50.0 * 0.15  # Plus difficile  intgrer
        scores["maintenance"] = 70.0 * 0.05  # Maintenance plus complexe
        
        scores["total"] = sum(scores.values())
        return scores
    
    def _evaluer_outil_apex_batch(self, tool: Dict[str, Any]) -> Dict[str, float]:
        """valuation spcialise pour un outil Batch d'Apex"""
        scores = {}
        
        # Adaptation des critres pour Batch
        scores["pertinence_technique"] = self._score_pertinence_batch(tool) * 0.40
        scores["compatibilite_architecture"] = 40.0 * 0.15  # Score fixe bas
        scores["valeur_ajoutee"] = self._score_valeur_ajoutee_apex(tool) * 0.30
        scores["facilite_integration"] = 30.0 * 0.10  # Trs difficile  intgrer
        scores["maintenance"] = 50.0 * 0.05  # Maintenance limite
        
        scores["total"] = sum(scores.values())
        return scores
    
    def _score_pertinence_apex_python(self, tool: Dict[str, Any]) -> float:
        """Score de pertinence technique pour Python Apex"""
        score = 50.0  # Score de base
        
        # Bonus pour les outils d'automatisation
        if "automation" in tool.get("name", "").lower():
            score += 20.0
        
        # Bonus pour les outils de monitoring
        if "monitor" in tool.get("name", "").lower():
            score += 15.0
        
        # Bonus pour les gnrateurs
        if "generat" in tool.get("name", "").lower():
            score += 15.0
        
        # Bonus pour les outils Excel (spcificit Apex)
        if "excel" in tool.get("apex_subdir", "").lower():
            score += 25.0
        
        # Bonus pour la complexit
        complexity = tool.get("complexity_score", 0)
        if complexity > 20:
            score += 10.0
        elif complexity > 10:
            score += 5.0
        
        return min(score, 100.0)
    
    def _score_pertinence_powershell(self, tool: Dict[str, Any]) -> float:
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
    
    def _score_pertinence_batch(self, tool: Dict[str, Any]) -> float:
        """Score de pertinence pour Batch"""
        score = 30.0  # Score de base bas
        
        # Bonus pour les outils de build/dploiement
        if any(keyword in tool.get("name", "").lower() 
               for keyword in ["build", "deploy", "install", "setup"]):
            score += 25.0
        
        return min(score, 100.0)
    
    def _score_compatibilite_apex(self, tool: Dict[str, Any]) -> float:
        """Score de compatibilit avec NextGeneration pour outils Apex"""
        score = 60.0  # Score de base
        
        # Bonus pour les outils dans certains rpertoires Apex
        apex_subdir = tool.get("apex_subdir", "").lower()
        
        if apex_subdir in ["python", "automation", "monitoring"]:
            score += 20.0
        elif apex_subdir in ["excel", "generators", "utilities"]:
            score += 15.0
        elif apex_subdir in ["migration", "workflow"]:
            score += 10.0
        
        return min(score, 100.0)
    
    def _score_valeur_ajoutee_apex(self, tool: Dict[str, Any]) -> float:
        """Score de valeur ajoute spcifique  Apex"""
        score = 50.0
        
        # Valeur ajoute base sur le rpertoire Apex
        apex_subdir = tool.get("apex_subdir", "").lower()
        
        # Outils d'Excel automation (trs utiles)
        if "excel" in apex_subdir:
            score += 30.0
        
        # Outils de gnration de code
        if "generat" in apex_subdir:
            score += 25.0
        
        # Outils d'automatisation
        if "automation" in apex_subdir:
            score += 20.0
        
        return min(score, 100.0)
    
    def _score_facilite_integration_apex(self, tool: Dict[str, Any]) -> float:
        """Score de facilit d'intgration pour outils Apex"""
        score = 70.0  # Score de base pour Python
        
        # Malus selon le type
        if tool.get("type") == "powershell":
            score -= 20.0
        elif tool.get("type") == "batch":
            score -= 40.0
        
        return max(score, 10.0)
    
    def _score_maintenance_apex(self, tool: Dict[str, Any]) -> float:
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
    
    def _calculer_priorite_apex(self, tool: Dict[str, Any], score_total: float) -> str:
        """Calcul de la priorit pour un outil Apex"""
        if score_total >= 85.0:
            return "HIGH"
        elif score_total >= 75.0:
            return "MEDIUM"
        elif score_total >= 65.0:
            return "LOW"
        else:
            return "SKIP"

# Test de l'agent si excut directement
if __name__ == "__main__":
    import sys
    
    # Test avec des donnes simules
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