#!/usr/bin/env python3
"""
🔧 VALIDATION TRANSFORMATION ÉQUIPE DE MAINTENANCE
=================================================

Script de validation pour la transformation de l'équipe de maintenance
en intégrant les fonctionnalités avancées identifiées.

Mission: Valider et planifier la transformation vers une équipe de maintenance intelligente

Author: Équipe NextGeneration
Version: 1.0.0
Created: 2025-06-20
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Configuration PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "agent_factory_implementation"))

@dataclass
class ValidationResult:
    """Résultat de validation d'un composant"""
    component: str
    status: str  # "OK", "WARNING", "ERROR"
    score: float  # 0-100
    issues: List[str]
    recommendations: List[str]
    capabilities_found: List[str]
    capabilities_missing: List[str]

@dataclass
class TransformationPlan:
    """Plan de transformation pour l'équipe de maintenance"""
    current_state: Dict[str, Any]
    target_state: Dict[str, Any]
    transformation_steps: List[Dict[str, Any]]
    estimated_effort: str
    priority_order: List[str]
    dependencies: Dict[str, List[str]]

class MaintenanceTeamValidator:
    """Validateur pour la transformation de l'équipe de maintenance"""
    
    def __init__(self):
        self.validation_results: List[ValidationResult] = []
        self.current_agents = {
            "agent_01_analyseur_structure": "agent_factory_implementation/agents/agent_MAINTENANCE_01_analyseur_structure.py",
            "agent_02_evaluateur_utilite": "agent_factory_implementation/agents/agent_MAINTENANCE_02_evaluateur_utilite.py", 
            "agent_03_adaptateur_code": "agent_factory_implementation/agents/agent_MAINTENANCE_03_adaptateur_code.py",
            "agent_04_testeur_anti_faux": "agent_factory_implementation/agents/agent_MAINTENANCE_04_testeur_anti_faux_agents.py"
        }
        
        # Fonctionnalités cibles identifiées
        self.target_capabilities = {
            "analyse_structurelle": [
                "ast_analysis_advanced",
                "intelligent_classification", 
                "complexity_scoring",
                "multi_language_support",
                "utility_indicators_detection",
                "recursive_directory_analysis",
                "metadata_extraction",
                "dependency_mapping"
            ],
            "evaluation_utilite": [
                "weighted_evaluation_system",
                "conflict_detection",
                "redundancy_identification", 
                "nextgen_compliance_scoring",
                "intelligent_prioritization",
                "value_added_metrics",
                "integration_ease_assessment",
                "maintenance_burden_evaluation"
            ],
            "adaptation_code": [
                "code_transformation",
                "pattern_factory_migration",
                "template_generation",
                "assisted_integration",
                "sync_to_async_conversion",
                "automatic_imports_addition",
                "class_restructuring",
                "mandatory_methods_generation"
            ],
            "validation_conformite": [
                "fake_agent_detection",
                "async_sync_validation",
                "pattern_factory_compliance",
                "compliance_scoring",
                "advanced_static_analysis",
                "suspicious_patterns_detection",
                "mandatory_methods_validation",
                "import_validation"
            ],
            "template_system": [
                "configurable_templates",
                "domain_specialization",
                "standardized_configuration",
                "enriched_metadata",
                "automatic_agent_generation",
                "template_validation",
                "configuration_management"
            ]
        }
    
    async def validate_current_state(self) -> Dict[str, ValidationResult]:
        """Validation de l'état actuel de l'équipe de maintenance"""
        print("🔍 VALIDATION ÉTAT ACTUEL DE L'ÉQUIPE DE MAINTENANCE")
        print("=" * 60)
        
        results = {}
        
        for agent_name, agent_path in self.current_agents.items():
            print(f"\n📊 Validation {agent_name}...")
            result = await self._validate_single_agent(agent_name, agent_path)
            results[agent_name] = result
            self.validation_results.append(result)
            
            # Affichage résultat
            status_icon = "✅" if result.status == "OK" else "⚠️" if result.status == "WARNING" else "❌"
            print(f"   {status_icon} Status: {result.status} (Score: {result.score:.1f}%)")
            print(f"   📈 Capacités trouvées: {len(result.capabilities_found)}")
            print(f"   📉 Capacités manquantes: {len(result.capabilities_missing)}")
            
            if result.issues:
                print(f"   🚨 Problèmes: {len(result.issues)}")
                for issue in result.issues[:2]:  # Limiter l'affichage
                    print(f"      - {issue}")
        
        return results
    
    async def _validate_single_agent(self, agent_name: str, agent_path: str) -> ValidationResult:
        """Validation d'un agent individuel"""
        try:
            file_path = Path(agent_path)
            if not file_path.exists():
                return ValidationResult(
                    component=agent_name,
                    status="ERROR",
                    score=0.0,
                    issues=[f"Fichier non trouvé: {agent_path}"],
                    recommendations=["Créer l'agent manquant"],
                    capabilities_found=[],
                    capabilities_missing=[]
                )
            
            # Lire le code source
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Analyser les capacités
            capabilities_found = []
            capabilities_missing = []
            issues = []
            recommendations = []
            
            # Déterminer le domaine de l'agent
            domain = self._determine_agent_domain(agent_name)
            target_caps = self.target_capabilities.get(domain, [])
            
            # Vérifier les capacités présentes
            for capability in target_caps:
                if self._check_capability_present(source_code, capability):
                    capabilities_found.append(capability)
                else:
                    capabilities_missing.append(capability)
            
            # Vérifier la conformité Pattern Factory
            pattern_factory_issues = self._check_pattern_factory_compliance(source_code)
            issues.extend(pattern_factory_issues)
            
            # Vérifier la structure async/sync
            async_issues = self._check_async_compliance(source_code)
            issues.extend(async_issues)
            
            # Calculer le score
            score = self._calculate_agent_score(capabilities_found, target_caps, issues)
            
            # Déterminer le status
            if score >= 80:
                status = "OK"
            elif score >= 60:
                status = "WARNING" 
            else:
                status = "ERROR"
            
            # Générer des recommandations
            recommendations = self._generate_recommendations(capabilities_missing, issues)
            
            return ValidationResult(
                component=agent_name,
                status=status,
                score=score,
                issues=issues,
                recommendations=recommendations,
                capabilities_found=capabilities_found,
                capabilities_missing=capabilities_missing
            )
            
        except Exception as e:
            return ValidationResult(
                component=agent_name,
                status="ERROR",
                score=0.0,
                issues=[f"Erreur validation: {str(e)}"],
                recommendations=["Corriger les erreurs de validation"],
                capabilities_found=[],
                capabilities_missing=[]
            )
    
    def _determine_agent_domain(self, agent_name: str) -> str:
        """Détermine le domaine d'un agent"""
        if "analyseur" in agent_name or "structure" in agent_name:
            return "analyse_structurelle"
        elif "evaluateur" in agent_name or "utilite" in agent_name:
            return "evaluation_utilite"
        elif "adaptateur" in agent_name or "code" in agent_name:
            return "adaptation_code"
        elif "testeur" in agent_name or "faux" in agent_name:
            return "validation_conformite"
        else:
            return "template_system"
    
    def _check_capability_present(self, source_code: str, capability: str) -> bool:
        """Vérifie si une capacité est présente dans le code"""
        # Mapping des capacités vers des patterns de code
        capability_patterns = {
            "ast_analysis_advanced": ["ast.parse", "ast.walk", "ast.FunctionDef"],
            "intelligent_classification": ["classify", "categorize", "tool_type"],
            "complexity_scoring": ["complexity_score", "calculate_complexity"],
            "weighted_evaluation_system": ["evaluation_criteria", "weight", "pondér"],
            "conflict_detection": ["detect_conflicts", "redundancies", "similarity"],
            "pattern_factory_compliance": ["Pattern Factory", "Agent", "async def"],
            "fake_agent_detection": ["fake_agent", "sync_violations", "FAUX AGENT"],
            "code_transformation": ["transform", "convert", "migrate"],
            "template_generation": ["template", "generate", "create_agent"]
        }
        
        patterns = capability_patterns.get(capability, [capability.replace("_", " ")])
        return any(pattern.lower() in source_code.lower() for pattern in patterns)
    
    def _check_pattern_factory_compliance(self, source_code: str) -> List[str]:
        """Vérifie la conformité Pattern Factory"""
        issues = []
        
        if "from core.agent_factory_architecture import" not in source_code:
            issues.append("Import Pattern Factory manquant")
        
        if "class Agent" not in source_code and "Agent)" not in source_code:
            issues.append("Héritage Agent manquant")
        
        required_methods = ["startup", "shutdown", "health_check", "execute_task"]
        for method in required_methods:
            if f"async def {method}" not in source_code:
                issues.append(f"Méthode async {method}() manquante")
        
        return issues
    
    def _check_async_compliance(self, source_code: str) -> List[str]:
        """Vérifie la conformité async/sync"""
        issues = []
        
        # Détecter await dans fonctions non-async
        import re
        await_in_sync = re.findall(r'def\s+(\w+)\s*\([^)]*\):[^{]*await\s+', source_code, re.DOTALL)
        for func_name in await_in_sync:
            issues.append(f"await dans fonction sync: {func_name}()")
        
        return issues
    
    def _calculate_agent_score(self, capabilities_found: List[str], target_caps: List[str], issues: List[str]) -> float:
        """Calcule le score d'un agent"""
        if not target_caps:
            return 100.0
        
        # Score basé sur les capacités
        capability_score = (len(capabilities_found) / len(target_caps)) * 80
        
        # Pénalité pour les problèmes
        issue_penalty = min(len(issues) * 10, 30)
        
        return max(0.0, capability_score - issue_penalty)
    
    def _generate_recommendations(self, missing_capabilities: List[str], issues: List[str]) -> List[str]:
        """Génère des recommandations"""
        recommendations = []
        
        if missing_capabilities:
            recommendations.append(f"Implémenter {len(missing_capabilities)} capacités manquantes")
        
        if issues:
            recommendations.append(f"Corriger {len(issues)} problèmes identifiés")
        
        return recommendations
    
    def generate_transformation_plan(self, validation_results: Dict[str, ValidationResult]) -> TransformationPlan:
        """Génère le plan de transformation"""
        print("\n🚀 GÉNÉRATION DU PLAN DE TRANSFORMATION")
        print("=" * 50)
        
        # État actuel
        current_state = {
            "total_agents": len(validation_results),
            "agents_ok": len([r for r in validation_results.values() if r.status == "OK"]),
            "agents_warning": len([r for r in validation_results.values() if r.status == "WARNING"]),
            "agents_error": len([r for r in validation_results.values() if r.status == "ERROR"]),
            "average_score": sum(r.score for r in validation_results.values()) / len(validation_results),
            "total_capabilities_found": sum(len(r.capabilities_found) for r in validation_results.values()),
            "total_capabilities_missing": sum(len(r.capabilities_missing) for r in validation_results.values())
        }
        
        # État cible
        target_state = {
            "total_agents": 6,  # 4 existants + 2 nouveaux (orchestrateur + template manager)
            "agents_ok": 6,
            "average_score": 95.0,
            "new_capabilities": [
                "orchestration_intelligente",
                "template_management_avance",
                "auto_healing_agents",
                "predictive_maintenance",
                "continuous_validation"
            ]
        }
        
        # Étapes de transformation
        transformation_steps = [
            {
                "step": 1,
                "name": "Correction des Problèmes Critiques",
                "description": "Corriger tous les problèmes Pattern Factory et async/sync",
                "effort": "2-3 jours",
                "priority": "HIGH"
            },
            {
                "step": 2, 
                "name": "Enrichissement des Capacités Existantes",
                "description": "Ajouter les capacités manquantes aux agents existants",
                "effort": "1 semaine",
                "priority": "HIGH"
            },
            {
                "step": 3,
                "name": "Création Agent Orchestrateur",
                "description": "Créer un agent orchestrateur pour coordonner l'équipe",
                "effort": "3-4 jours",
                "priority": "MEDIUM"
            },
            {
                "step": 4,
                "name": "Système de Templates Avancé",
                "description": "Implémenter le système de templates configurables",
                "effort": "1 semaine",
                "priority": "MEDIUM"
            },
            {
                "step": 5,
                "name": "Validation et Tests Intégrés",
                "description": "Tests complets et validation de l'équipe transformée",
                "effort": "2-3 jours",
                "priority": "HIGH"
            }
        ]
        
        # Ordre de priorité
        priority_order = [
            "agent_04_testeur_anti_faux",  # Critique pour la validation
            "agent_01_analyseur_structure",  # Base pour tout le reste
            "agent_02_evaluateur_utilite",  # Évaluation intelligente
            "agent_03_adaptateur_code",  # Transformation
            "agent_orchestrateur_maintenance",  # Nouveau - coordination
            "agent_template_manager"  # Nouveau - gestion templates
        ]
        
        # Dépendances
        dependencies = {
            "agent_02_evaluateur_utilite": ["agent_01_analyseur_structure"],
            "agent_03_adaptateur_code": ["agent_01_analyseur_structure", "agent_04_testeur_anti_faux"],
            "agent_orchestrateur_maintenance": ["agent_01_analyseur_structure", "agent_02_evaluateur_utilite"],
            "agent_template_manager": ["agent_04_testeur_anti_faux"]
        }
        
        return TransformationPlan(
            current_state=current_state,
            target_state=target_state,
            transformation_steps=transformation_steps,
            estimated_effort="2-3 semaines",
            priority_order=priority_order,
            dependencies=dependencies
        )
    
    def generate_validation_report(self, validation_results: Dict[str, ValidationResult], 
                                 transformation_plan: TransformationPlan) -> Dict[str, Any]:
        """Génère le rapport de validation complet"""
        print("\n📊 GÉNÉRATION DU RAPPORT DE VALIDATION")
        print("=" * 45)
        
        # Statistiques globales
        total_issues = sum(len(r.issues) for r in validation_results.values())
        total_recommendations = sum(len(r.recommendations) for r in validation_results.values())
        
        report = {
            "validation_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_agents_validated": len(validation_results),
                "average_score": transformation_plan.current_state["average_score"],
                "total_issues_found": total_issues,
                "total_recommendations": total_recommendations,
                "overall_status": self._determine_overall_status(validation_results)
            },
            "agent_details": {
                name: asdict(result) for name, result in validation_results.items()
            },
            "transformation_plan": asdict(transformation_plan),
            "next_actions": self._generate_next_actions(validation_results, transformation_plan),
            "success_metrics": {
                "current_readiness": f"{transformation_plan.current_state['average_score']:.1f}%",
                "target_readiness": f"{transformation_plan.target_state['average_score']:.1f}%",
                "improvement_needed": f"{transformation_plan.target_state['average_score'] - transformation_plan.current_state['average_score']:.1f} points"
            }
        }
        
        return report
    
    def _determine_overall_status(self, validation_results: Dict[str, ValidationResult]) -> str:
        """Détermine le status global de l'équipe"""
        scores = [r.score for r in validation_results.values()]
        avg_score = sum(scores) / len(scores)
        
        if avg_score >= 80:
            return "READY_FOR_TRANSFORMATION"
        elif avg_score >= 60:
            return "NEEDS_IMPROVEMENTS"
        else:
            return "CRITICAL_ISSUES"
    
    def _generate_next_actions(self, validation_results: Dict[str, ValidationResult], 
                             transformation_plan: TransformationPlan) -> List[str]:
        """Génère les prochaines actions à effectuer"""
        actions = []
        
        # Actions basées sur les problèmes critiques
        critical_agents = [name for name, result in validation_results.items() if result.status == "ERROR"]
        if critical_agents:
            actions.append(f"🚨 URGENT: Corriger {len(critical_agents)} agents en erreur")
        
        # Actions basées sur le plan de transformation
        actions.append("🔧 Démarrer l'étape 1: Correction des problèmes critiques")
        actions.append("📋 Préparer les templates pour les nouveaux agents")
        actions.append("🧪 Mettre en place les tests de validation continue")
        
        return actions

async def main():
    """Fonction principale de validation"""
    print("🔧 VALIDATION TRANSFORMATION ÉQUIPE DE MAINTENANCE")
    print("=" * 60)
    print("🎯 Mission: Valider et planifier la transformation intelligente")
    print()
    
    validator = MaintenanceTeamValidator()
    
    try:
        # 1. Validation de l'état actuel
        validation_results = await validator.validate_current_state()
        
        # 2. Génération du plan de transformation
        transformation_plan = validator.generate_transformation_plan(validation_results)
        
        # 3. Génération du rapport complet
        report = validator.generate_validation_report(validation_results, transformation_plan)
        
        # 4. Affichage des résultats
        print("\n🎯 RÉSULTATS DE LA VALIDATION")
        print("=" * 40)
        print(f"📊 Score moyen actuel: {report['validation_summary']['average_score']:.1f}%")
        print(f"🎯 Score cible: {transformation_plan.target_state['average_score']:.1f}%")
        print(f"📈 Amélioration nécessaire: {report['success_metrics']['improvement_needed']}")
        print(f"⏱️  Effort estimé: {transformation_plan.estimated_effort}")
        print(f"🚦 Status global: {report['validation_summary']['overall_status']}")
        
        print("\n🚀 PROCHAINES ACTIONS PRIORITAIRES:")
        for i, action in enumerate(report['next_actions'][:3], 1):
            print(f"   {i}. {action}")
        
        # 5. Sauvegarde du rapport
        report_file = Path("validation_transformation_rapport.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rapport sauvegardé: {report_file}")
        
        # 6. Verdict final
        if report['validation_summary']['overall_status'] == "READY_FOR_TRANSFORMATION":
            print("\n✅ VERDICT: ÉQUIPE PRÊTE POUR LA TRANSFORMATION")
            return True
        elif report['validation_summary']['overall_status'] == "NEEDS_IMPROVEMENTS":
            print("\n⚠️  VERDICT: AMÉLIORATIONS NÉCESSAIRES AVANT TRANSFORMATION")
            return False
        else:
            print("\n❌ VERDICT: PROBLÈMES CRITIQUES - CORRECTION URGENTE REQUISE")
            return False
        
    except Exception as e:
        print(f"\n💥 ERREUR CRITIQUE: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 



