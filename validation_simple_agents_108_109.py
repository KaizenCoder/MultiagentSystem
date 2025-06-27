#!/usr/bin/env python3
"""
VALIDATION SIMPLE MAINTENANCE AGENTS 108 & 109
==============================================

Script de validation simplifié pour tester la qualité de l'implémentation 
sans dépendances externes comme pyflakes.

Agents cibles:
- agent_108_performance_optimizer.py
- agent_109_pattern_factory_version.py

Author: Équipe NextGeneration
Version: Validation Simple v1.0.0
"""

import sys
import ast
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Configuration du chemin
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

class SimpleValidationAgents:
    """Validation simplifiée des agents 108 et 109"""
    
    def __init__(self):
        # Chemins des agents cibles
        self.agent_108_path = PROJECT_ROOT / "agents" / "agent_108_performance_optimizer.py"
        self.agent_109_path = PROJECT_ROOT / "agents" / "agent_109_pattern_factory_version.py"
    
    def analyze_agent_syntax(self, agent_path: Path) -> Dict[str, Any]:
        """Analyse syntaxique basique d'un agent"""
        print(f"\n📊 ANALYSE SYNTAXIQUE: {agent_path.name}")
        print("="*60)
        
        if not agent_path.exists():
            return {"error": f"Agent non trouvé: {agent_path}"}
        
        try:
            # Lecture du code
            code_content = agent_path.read_text(encoding='utf-8')
            lines = code_content.split('\n')
            
            print(f"✅ Agent chargé: {len(code_content):,} caractères")
            print(f"✅ Lignes de code: {len(lines)}")
            
            # Test de compilation AST
            syntax_valid = False
            syntax_error = None
            
            try:
                ast.parse(code_content)
                syntax_valid = True
                print("✅ Syntaxe Python: Valide")
            except SyntaxError as e:
                syntax_error = str(e)
                print(f"❌ Erreur syntaxe: {e}")
            except Exception as e:
                syntax_error = f"Erreur AST: {e}"
                print(f"❌ Erreur parsing AST: {e}")
            
            # Analyse basique du contenu
            imports_count = sum(1 for line in lines if line.strip().startswith(('import ', 'from ')))
            classes_count = sum(1 for line in lines if line.strip().startswith('class '))
            functions_count = sum(1 for line in lines if line.strip().startswith('def ') or line.strip().startswith('async def '))
            docstrings_count = code_content.count('"""') + code_content.count("'''")
            
            print(f"📈 Statistiques code:")
            print(f"   Imports: {imports_count}")
            print(f"   Classes: {classes_count}")
            print(f"   Fonctions: {functions_count}")
            print(f"   Docstrings: {docstrings_count // 2}")  # Divisé par 2 car ouverture/fermeture
            
            return {
                "agent_path": str(agent_path),
                "agent_name": agent_path.name,
                "syntax_valid": syntax_valid,
                "syntax_error": syntax_error,
                "code_stats": {
                    "total_lines": len(lines),
                    "total_chars": len(code_content),
                    "imports_count": imports_count,
                    "classes_count": classes_count,
                    "functions_count": functions_count,
                    "docstrings_count": docstrings_count // 2
                }
            }
            
        except Exception as e:
            print(f"❌ Erreur lecture agent: {e}")
            return {"error": str(e), "agent_path": str(agent_path)}
    
    def validate_pattern_factory_compliance(self, agent_path: Path) -> Dict[str, Any]:
        """Valide la conformité Pattern Factory d'un agent"""
        print(f"\n🏗️  VALIDATION PATTERN FACTORY: {agent_path.name}")
        print("="*60)
        
        if not agent_path.exists():
            return {"error": f"Agent non trouvé: {agent_path}"}
        
        try:
            code_content = agent_path.read_text(encoding='utf-8')
            
            # Vérifications Pattern Factory
            checks = {
                "agent_import": {
                    "check": "from core.agent_factory_architecture import Agent" in code_content,
                    "description": "Import de la classe Agent"
                },
                "task_result_imports": {
                    "check": "Task" in code_content and "Result" in code_content,
                    "description": "Imports Task et Result"
                },
                "agent_inheritance": {
                    "check": "class" in code_content and "(Agent)" in code_content,
                    "description": "Héritage de la classe Agent"
                },
                "async_methods": {
                    "check": "async def" in code_content,
                    "description": "Méthodes asynchrones"
                },
                "startup_method": {
                    "check": "def startup(" in code_content or "async def startup(" in code_content,
                    "description": "Méthode startup()"
                },
                "shutdown_method": {
                    "check": "def shutdown(" in code_content or "async def shutdown(" in code_content,
                    "description": "Méthode shutdown()"
                },
                "execute_task_method": {
                    "check": "def execute_task(" in code_content or "async def execute_task(" in code_content,
                    "description": "Méthode execute_task()"
                },
                "health_check_method": {
                    "check": "def health_check(" in code_content or "async def health_check(" in code_content,
                    "description": "Méthode health_check()"
                },
                "get_capabilities_method": {
                    "check": "def get_capabilities(" in code_content,
                    "description": "Méthode get_capabilities()"
                },
                "logging_support": {
                    "check": "import logging" in code_content or "self.logger" in code_content,
                    "description": "Support du logging"
                },
                "error_handling": {
                    "check": "try:" in code_content and "except" in code_content,
                    "description": "Gestion d'erreurs"
                },
                "docstring_present": {
                    "check": '"""' in code_content[:1000] or "'''" in code_content[:1000],
                    "description": "Docstring de classe présente"
                }
            }
            
            passed_checks = 0
            total_checks = len(checks)
            
            print(f"📋 VÉRIFICATIONS PATTERN FACTORY:")
            for check_name, check_info in checks.items():
                passed = check_info["check"]
                status = "✅" if passed else "❌"
                print(f"   {status} {check_info['description']}")
                if passed:
                    passed_checks += 1
            
            compliance_score = passed_checks / total_checks
            print(f"\n🎯 Score Pattern Factory: {compliance_score:.2f} ({passed_checks}/{total_checks})")
            
            # Niveau de conformité
            if compliance_score >= 0.9:
                compliance_level = "Excellent"
            elif compliance_score >= 0.75:
                compliance_level = "Bon"
            elif compliance_score >= 0.5:
                compliance_level = "Moyen"
            else:
                compliance_level = "Faible"
            
            print(f"📊 Niveau conformité: {compliance_level}")
            
            return {
                "agent_path": str(agent_path),
                "checks": {name: info["check"] for name, info in checks.items()},
                "compliance_score": compliance_score,
                "passed_checks": passed_checks,
                "total_checks": total_checks,
                "compliance_level": compliance_level,
                "needs_update": compliance_score < 0.75
            }
            
        except Exception as e:
            print(f"❌ Erreur validation Pattern Factory: {e}")
            return {"error": str(e)}
    
    def analyze_code_quality_indicators(self, agent_path: Path) -> Dict[str, Any]:
        """Analyse les indicateurs de qualité du code"""
        print(f"\n📈 INDICATEURS QUALITÉ CODE: {agent_path.name}")
        print("="*60)
        
        if not agent_path.exists():
            return {"error": f"Agent non trouvé: {agent_path}"}
        
        try:
            code_content = agent_path.read_text(encoding='utf-8')
            lines = [line.rstrip() for line in code_content.split('\n')]
            
            # Métriques de qualité
            total_lines = len(lines)
            non_empty_lines = sum(1 for line in lines if line.strip())
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            long_lines = sum(1 for line in lines if len(line) > 120)
            
            # Complexité approximative
            complexity_keywords = ['if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except', 'with ']
            complexity_count = sum(code_content.count(keyword) for keyword in complexity_keywords)
            
            # Bonnes pratiques
            has_main_guard = 'if __name__ == "__main__"' in code_content
            has_type_hints = ' -> ' in code_content or ': str' in code_content or ': int' in code_content
            has_constants = any(line.strip().isupper() and '=' in line for line in lines)
            
            # Calcul score qualité approximatif
            quality_factors = {
                "code_density": min(non_empty_lines / total_lines, 1.0) if total_lines > 0 else 0,
                "documentation_ratio": min((comment_lines * 2) / non_empty_lines, 1.0) if non_empty_lines > 0 else 0,
                "line_length_compliance": max(0, 1.0 - (long_lines / non_empty_lines)) if non_empty_lines > 0 else 1.0,
                "complexity_factor": max(0, 1.0 - (complexity_count / non_empty_lines * 2)) if non_empty_lines > 0 else 1.0,
                "best_practices": (
                    (1 if has_main_guard else 0) +
                    (1 if has_type_hints else 0) +
                    (1 if has_constants else 0)
                ) / 3
            }
            
            overall_quality = sum(quality_factors.values()) / len(quality_factors)
            
            print(f"📊 Métriques qualité:")
            print(f"   Lignes totales: {total_lines}")
            print(f"   Lignes non vides: {non_empty_lines}")
            print(f"   Lignes commentaires: {comment_lines}")
            print(f"   Lignes longues (>120): {long_lines}")
            print(f"   Complexité approximative: {complexity_count}")
            print(f"   Type hints: {'✅' if has_type_hints else '❌'}")
            print(f"   Main guard: {'✅' if has_main_guard else '❌'}")
            print(f"   Constantes: {'✅' if has_constants else '❌'}")
            
            print(f"\n🎯 Score qualité global: {overall_quality:.2f}")
            
            return {
                "agent_path": str(agent_path),
                "metrics": {
                    "total_lines": total_lines,
                    "non_empty_lines": non_empty_lines,
                    "comment_lines": comment_lines,
                    "long_lines": long_lines,
                    "complexity_count": complexity_count
                },
                "quality_factors": quality_factors,
                "overall_quality": overall_quality,
                "best_practices": {
                    "has_main_guard": has_main_guard,
                    "has_type_hints": has_type_hints,
                    "has_constants": has_constants
                }
            }
            
        except Exception as e:
            print(f"❌ Erreur analyse qualité: {e}")
            return {"error": str(e)}
    
    def run_validation_mission(self) -> Dict[str, Any]:
        """Exécute la mission de validation complète"""
        print("🚀 MISSION VALIDATION MAINTENANCE AGENTS 108 & 109")
        print("="*70)
        print(f"🎯 Test qualité implémentation Orchestrateur + Adaptateur v4.3.0")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        agents_to_validate = [
            ("agent_108_performance_optimizer.py", self.agent_108_path),
            ("agent_109_pattern_factory_version.py", self.agent_109_path)
        ]
        
        validation_results = {
            "mission_timestamp": datetime.now().isoformat(),
            "mission_type": "quality_validation",
            "agents_validated": [],
            "overall_assessment": {}
        }
        
        for agent_name, agent_path in agents_to_validate:
            print(f"\n{'='*70}")
            print(f"🧪 VALIDATION: {agent_name}")
            print(f"{'='*70}")
            
            agent_result = {
                "agent_name": agent_name,
                "agent_path": str(agent_path),
                "exists": agent_path.exists()
            }
            
            if not agent_path.exists():
                print(f"❌ Agent non trouvé: {agent_path}")
                agent_result["validation_status"] = "agent_not_found"
                validation_results["agents_validated"].append(agent_result)
                continue
            
            # Test 1: Analyse syntaxique
            print(f"\n1️⃣  ANALYSE SYNTAXIQUE")
            syntax_analysis = self.analyze_agent_syntax(agent_path)
            agent_result["syntax_analysis"] = syntax_analysis
            
            # Test 2: Conformité Pattern Factory
            print(f"\n2️⃣  CONFORMITÉ PATTERN FACTORY")
            pattern_compliance = self.validate_pattern_factory_compliance(agent_path)
            agent_result["pattern_factory_compliance"] = pattern_compliance
            
            # Test 3: Indicateurs qualité
            print(f"\n3️⃣  INDICATEURS QUALITÉ CODE")
            quality_analysis = self.analyze_code_quality_indicators(agent_path)
            agent_result["code_quality"] = quality_analysis
            
            # Évaluation globale de l'agent
            syntax_valid = syntax_analysis.get("syntax_valid", False)
            compliance_score = pattern_compliance.get("compliance_score", 0)
            quality_score = quality_analysis.get("overall_quality", 0)
            
            agent_score = (
                (1.0 if syntax_valid else 0.0) * 0.4 +
                compliance_score * 0.4 +
                quality_score * 0.2
            )
            
            agent_result["overall_score"] = agent_score
            agent_result["validation_status"] = "passed" if agent_score >= 0.7 else "needs_improvement"
            
            print(f"\n📊 SCORE GLOBAL AGENT: {agent_score:.2f}")
            print(f"📋 Statut: {'✅ VALIDÉ' if agent_score >= 0.7 else '⚠️  AMÉLIORATION REQUISE'}")
            
            validation_results["agents_validated"].append(agent_result)
        
        # Évaluation globale de la mission
        print(f"\n{'='*70}")
        print(f"📊 ÉVALUATION GLOBALE MISSION")
        print(f"{'='*70}")
        
        total_agents = len([a for a in validation_results["agents_validated"] if a["exists"]])
        passed_agents = sum(1 for a in validation_results["agents_validated"] 
                          if a.get("validation_status") == "passed")
        
        if total_agents > 0:
            avg_score = sum(a.get("overall_score", 0) for a in validation_results["agents_validated"] 
                          if a["exists"]) / total_agents
            success_rate = passed_agents / total_agents
        else:
            avg_score = 0
            success_rate = 0
        
        validation_results["overall_assessment"] = {
            "total_agents_found": total_agents,
            "agents_passed": passed_agents,
            "success_rate": success_rate,
            "average_score": avg_score,
            "mission_successful": success_rate >= 0.5 and avg_score >= 0.7,
            "orchestrateur_quality_validated": avg_score >= 0.7,
            "adaptateur_improvements_validated": success_rate >= 0.5
        }
        
        print(f"✅ Agents trouvés: {total_agents}/2")
        print(f"✅ Agents validés: {passed_agents}/{total_agents}")
        print(f"✅ Taux de succès: {success_rate*100:.1f}%")
        print(f"✅ Score moyen: {avg_score:.2f}")
        print(f"✅ Mission réussie: {'✅ OUI' if validation_results['overall_assessment']['mission_successful'] else '❌ NON'}")
        
        # Recommandations
        if not validation_results['overall_assessment']['mission_successful']:
            print(f"\n💡 RECOMMANDATIONS:")
            for agent_result in validation_results["agents_validated"]:
                if agent_result.get("validation_status") == "needs_improvement":
                    print(f"   • {agent_result['agent_name']}: Score {agent_result.get('overall_score', 0):.2f} - Amélioration requise")
                    
                    # Recommandations spécifiques
                    if not agent_result.get("syntax_analysis", {}).get("syntax_valid", True):
                        print(f"     - Corriger les erreurs de syntaxe")
                    
                    compliance = agent_result.get("pattern_factory_compliance", {})
                    if compliance.get("compliance_score", 1) < 0.75:
                        print(f"     - Améliorer conformité Pattern Factory ({compliance.get('compliance_score', 0):.2f})")
                    
                    quality = agent_result.get("code_quality", {})
                    if quality.get("overall_quality", 1) < 0.6:
                        print(f"     - Améliorer qualité du code ({quality.get('overall_quality', 0):.2f})")
        
        return validation_results

def main():
    """Point d'entrée principal"""
    try:
        validator = SimpleValidationAgents()
        results = validator.run_validation_mission()
        
        # Sauvegarde du rapport
        report_file = PROJECT_ROOT / f"validation_report_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            import json
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n📄 Rapport sauvegardé: {report_file}")
        except Exception as e:
            print(f"⚠️  Erreur sauvegarde: {e}")
        
        # Code de sortie
        mission_successful = results["overall_assessment"]["mission_successful"]
        return 0 if mission_successful else 1
        
    except KeyboardInterrupt:
        print("\n⚠️ Mission interrompue")
        return 130
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())