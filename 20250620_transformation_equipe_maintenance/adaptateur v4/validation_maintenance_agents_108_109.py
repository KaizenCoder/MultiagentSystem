#!/usr/bin/env python3
"""
VALIDATION MAINTENANCE AGENTS 108 & 109
=======================================

Script de validation pour tester la qualité de l'implémentation 
du nouvel orchestrateur et des modifications de l'agent adaptateur v4.3.0
sur les agents spécifiés.

Agents cibles:
- agent_108_performance_optimizer.py
- agent_109_pattern_factory_version.py

Author: Équipe NextGeneration
Version: Validation v1.0.0
"""

import asyncio
import sys
import time
from pathlib import Path
from datetime import datetime

# Configuration du chemin
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from agents.agent_MAINTENANCE_03_adaptateur_code import AgentMAINTENANCE03AdaptateurCode
    from core.agent_factory_architecture import Task, Result
except ImportError as e:
    print(f"❌ Erreur import: {e}")
    sys.exit(1)

class ValidationMaintenanceAgents:
    """Validation de la maintenance des agents 108 et 109"""
    
    def __init__(self):
        self.adaptateur = AgentMAINTENANCE03AdaptateurCode(
            id="validation_108_109",
            pattern_confidence_threshold=0.75,
            enable_pattern_learning=True
        )
        
        # Chemins des agents cibles
        self.agent_108_path = PROJECT_ROOT / "agents" / "agent_108_performance_optimizer.py"
        self.agent_109_path = PROJECT_ROOT / "agents" / "agent_109_pattern_factory_version.py"
    
    async def analyze_agent_quality(self, agent_path: Path) -> Dict[str, Any]:
        """Analyse la qualité d'un agent avec l'adaptateur v4.3.0"""
        print(f"\n📊 ANALYSE QUALITÉ: {agent_path.name}")
        print("="*60)
        
        if not agent_path.exists():
            return {"error": f"Agent non trouvé: {agent_path}"}
        
        try:
            # Lecture du code de l'agent
            code_content = agent_path.read_text(encoding='utf-8')
            print(f"✅ Agent chargé: {len(code_content):,} caractères")
            print(f"✅ Lignes de code: {len(code_content.split(''))}")
            
            # Test de la validation multi-niveaux
            validation_result = self.adaptateur.validate_multi_level(code_content)
            
            print(f"\n🔍 RÉSULTATS VALIDATION MULTI-NIVEAUX:")
            print(f"   Syntaxe valide: {'✅' if validation_result.syntax_valid else '❌'} {validation_result.syntax_valid}")
            print(f"   Sémantique valide: {'✅' if validation_result.semantic_valid else '❌'} {validation_result.semantic_valid}")
            print(f"   Compilation réussie: {'✅' if validation_result.compilation_successful else '❌'} {validation_result.compilation_successful}")
            print(f"   Résolution imports: {'✅' if validation_result.import_resolution else '❌'} {validation_result.import_resolution}")
            print(f"   Score confiance: {validation_result.confidence_score:.2f}/1.0")
            
            if validation_result.issues:
                print(f"\n⚠️  Issues détectées ({len(validation_result.issues)}):")
                for i, issue in enumerate(validation_result.issues[:5], 1):
                    print(f"   {i}. {issue}")
                if len(validation_result.issues) > 5:
                    print(f"   ... et {len(validation_result.issues) - 5} autres")
            
            if validation_result.warnings:
                print(f"\n💡 Warnings ({len(validation_result.warnings)}):")
                for i, warning in enumerate(validation_result.warnings[:3], 1):
                    print(f"   {i}. {warning}")
                if len(validation_result.warnings) > 3:
                    print(f"   ... et {len(validation_result.warnings) - 3} autres")
            
            # Analyse des patterns d'indentation (si applicable)
            if not validation_result.syntax_valid:
                print(f"\n🔧 ANALYSE PATTERNS D'INDENTATION:")
                pattern_analysis = self.adaptateur.analyze_indentation_pattern(
                    code_content, 
                    "analyse préventive"
                )
                print(f"   Pattern type: {pattern_analysis['pattern_type']}")
                print(f"   Style indentation: {pattern_analysis['indentation_style']}")
                print(f"   Niveau indentation: {pattern_analysis['indentation_level']}")
                print(f"   Score complexité: {pattern_analysis['complexity_score']:.2f}")
            
            return {
                "agent_path": str(agent_path),
                "agent_name": agent_path.name,
                "code_length": len(code_content),
                "lines_count": len(code_content.split('\n')),
                "validation_result": validation_result.__dict__,
                "overall_score": validation_result.confidence_score,
                "needs_maintenance": validation_result.confidence_score < 0.8 or len(validation_result.issues) > 0,
                "chromadb_enabled": self.adaptateur.chroma_patterns.enabled,
                "postgresql_enabled": self.adaptateur.pg_analytics.enabled
            }
            
        except Exception as e:
            print(f"❌ Erreur analyse agent: {e}")
            return {"error": str(e), "agent_path": str(agent_path)}
    
    async def test_adaptateur_improvements(self, agent_path: Path) -> Dict[str, Any]:
        """Test des améliorations de l'adaptateur v4.3.0 sur un agent"""
        print(f"\n🚀 TEST AMÉLIORATIONS v4.3.0: {agent_path.name}")
        print("="*60)
        
        if not agent_path.exists():
            return {"error": f"Agent non trouvé: {agent_path}"}
        
        try:
            code_content = agent_path.read_text(encoding='utf-8')
            
            # Simulation d'une tâche d'adaptation v4.3.0
            task = Task(
                id=f"test_v43_{agent_path.stem}",
                params={
                    "code": code_content,
                    "feedback": "Analyse qualité code agent",
                    "error_type": "generic",
                    "use_import_discovery": True,
                    "validate_result": True,
                    # Nouvelles options v4.3.0
                    "use_pattern_learning": True,
                    "enable_analytics": True
                }
            )
            
            # Exécution avec mesure du temps
            start_time = time.time()
            await self.adaptateur.startup()
            result = await self.adaptateur.execute_task(task)
            processing_time = time.time() - start_time
            
            if result.success:
                data = result.data
                
                print(f"✅ Traitement réussi en {processing_time:.3f}s")
                print(f"✅ Adaptations: {len(data.get('adaptations', []))}")
                
                # Nouvelles métriques v4.3.0
                advanced_confidence = data.get("advanced_confidence_score", 0)
                patterns_found = data.get("patterns_found", 0)
                patterns_used = data.get("patterns_used", 0)
                chromadb_enabled = data.get("chromadb_enabled", False)
                postgresql_enabled = data.get("postgresql_enabled", False)
                pattern_learning_used = data.get("pattern_learning_used", False)
                
                print(f"\n📊 MÉTRIQUES v4.3.0:")
                print(f"   Score confiance avancé: {advanced_confidence:.2f}")
                print(f"   Patterns trouvés: {patterns_found}")
                print(f"   Patterns utilisés: {patterns_used}")
                print(f"   ChromaDB actif: {'✅' if chromadb_enabled else '❌'}")
                print(f"   PostgreSQL actif: {'✅' if postgresql_enabled else '❌'}")
                print(f"   Apprentissage patterns: {'✅' if pattern_learning_used else '❌'}")
                
                validation_pre = data.get("validation_pre", {})
                validation_post = data.get("validation_post", {})
                
                if validation_pre and validation_post:
                    pre_score = validation_pre.get("confidence_score", 0)
                    post_score = validation_post.get("confidence_score", 0)
                    improvement = post_score - pre_score
                    
                    print(f"\n📈 AMÉLIORATION QUALITÉ:")
                    print(f"   Score pré: {pre_score:.2f}")
                    print(f"   Score post: {post_score:.2f}")
                    print(f"   Amélioration: {improvement:+.2f} points")
                
                return {
                    "success": True,
                    "processing_time": processing_time,
                    "adaptations_count": len(data.get('adaptations', [])),
                    "advanced_confidence": advanced_confidence,
                    "patterns_metrics": {
                        "found": patterns_found,
                        "used": patterns_used,
                        "learning_used": pattern_learning_used
                    },
                    "databases_status": {
                        "chromadb": chromadb_enabled,
                        "postgresql": postgresql_enabled
                    },
                    "quality_improvement": improvement if 'improvement' in locals() else 0
                }
            else:
                print(f"❌ Échec traitement: {result.error}")
                return {"success": False, "error": result.error}
                
        except Exception as e:
            print(f"❌ Erreur test améliorations: {e}")
            return {"error": str(e)}
        finally:
            await self.adaptateur.shutdown()
    
    async def validate_agent_architecture_compliance(self, agent_path: Path) -> Dict[str, Any]:
        """Valide la conformité architecturale d'un agent"""
        print(f"\n🏗️  VALIDATION CONFORMITÉ ARCHITECTURALE: {agent_path.name}")
        print("="*60)
        
        if not agent_path.exists():
            return {"error": f"Agent non trouvé: {agent_path}"}
        
        try:
            code_content = agent_path.read_text(encoding='utf-8')
            
            # Vérifications architecturales
            compliance_checks = {
                "has_agent_import": "from core.agent_factory_architecture import Agent" in code_content,
                "has_task_import": "Task" in code_content,
                "has_result_import": "Result" in code_content,
                "has_async_methods": "async def" in code_content,
                "has_startup_method": "def startup(" in code_content or "async def startup(" in code_content,
                "has_shutdown_method": "def shutdown(" in code_content or "async def shutdown(" in code_content,
                "has_execute_task": "def execute_task(" in code_content or "async def execute_task(" in code_content,
                "has_health_check": "def health_check(" in code_content or "async def health_check(" in code_content,
                "has_get_capabilities": "def get_capabilities(" in code_content,
                "has_docstring": '"""' in code_content[:500] or "'''" in code_content[:500],
                "has_logging": "import logging" in code_content or "self.logger" in code_content,
                "has_error_handling": "try:" in code_content and "except" in code_content
            }
            
            passed_checks = sum(1 for check in compliance_checks.values() if check)
            total_checks = len(compliance_checks)
            compliance_score = passed_checks / total_checks
            
            print(f"📋 RÉSULTATS CONFORMITÉ ({passed_checks}/{total_checks}):")
            for check_name, passed in compliance_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name.replace('_', ' ').title()}")
            
            print(f"\n🎯 Score conformité: {compliance_score:.2f} ({compliance_score*100:.1f}%)")
            
            # Recommandations
            if compliance_score < 1.0:
                print(f"\n💡 RECOMMANDATIONS:")
                for check_name, passed in compliance_checks.items():
                    if not passed:
                        recommendations = {
                            "has_agent_import": "Ajouter: from core.agent_factory_architecture import Agent",
                            "has_async_methods": "Utiliser des méthodes async pour startup, shutdown, execute_task",
                            "has_startup_method": "Implémenter la méthode startup()",
                            "has_shutdown_method": "Implémenter la méthode shutdown()",
                            "has_execute_task": "Implémenter la méthode execute_task()",
                            "has_health_check": "Implémenter la méthode health_check()",
                            "has_get_capabilities": "Implémenter la méthode get_capabilities()",
                            "has_docstring": "Ajouter une docstring descriptive en début de classe",
                            "has_logging": "Ajouter système de logging avec self.logger",
                            "has_error_handling": "Ajouter gestion d'erreurs avec try/except"
                        }
                        print(f"   • {recommendations.get(check_name, check_name)}")
            
            return {
                "agent_path": str(agent_path),
                "compliance_checks": compliance_checks,
                "compliance_score": compliance_score,
                "passed_checks": passed_checks,
                "total_checks": total_checks,
                "needs_architecture_update": compliance_score < 0.8
            }
            
        except Exception as e:
            print(f"❌ Erreur validation conformité: {e}")
            return {"error": str(e)}
    
    async def run_complete_validation(self) -> Dict[str, Any]:
        """Exécute la validation complète des deux agents"""
        print("🚀 VALIDATION COMPLÈTE MAINTENANCE AGENTS 108 & 109")
        print("="*70)
        print(f"🎯 Validation de l'implémentation Orchestrateur + Adaptateur v4.3.0")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        results = {
            "validation_timestamp": datetime.now().isoformat(),
            "adaptateur_version": "4.3.0",
            "agents_tested": [],
            "overall_assessment": {}
        }
        
        agents_to_test = [
            ("agent_108_performance_optimizer.py", self.agent_108_path),
            ("agent_109_pattern_factory_version.py", self.agent_109_path)
        ]
        
        for agent_name, agent_path in agents_to_test:
            print(f"\n{'='*70}")
            print(f"🧪 VALIDATION AGENT: {agent_name}")
            print(f"{'='*70}")
            
            agent_results = {
                "agent_name": agent_name,
                "agent_path": str(agent_path),
                "tests": {}
            }
            
            # Test 1: Analyse qualité
            print(f"\n1️⃣  TEST ANALYSE QUALITÉ")
            quality_analysis = await self.analyze_agent_quality(agent_path)
            agent_results["tests"]["quality_analysis"] = quality_analysis
            
            # Test 2: Améliorations adaptateur v4.3.0
            print(f"\n2️⃣  TEST AMÉLIORATIONS v4.3.0")
            improvements_test = await self.test_adaptateur_improvements(agent_path)
            agent_results["tests"]["adaptateur_improvements"] = improvements_test
            
            # Test 3: Conformité architecturale
            print(f"\n3️⃣  TEST CONFORMITÉ ARCHITECTURALE")
            compliance_check = await self.validate_agent_architecture_compliance(agent_path)
            agent_results["tests"]["architecture_compliance"] = compliance_check
            
            results["agents_tested"].append(agent_results)
        
        # Évaluation globale
        print(f"\n{'='*70}")
        print(f"📊 ÉVALUATION GLOBALE")
        print(f"{'='*70}")
        
        total_agents = len(results["agents_tested"])
        successful_tests = 0
        total_quality_score = 0
        total_compliance_score = 0
        
        for agent_result in results["agents_tested"]:
            tests = agent_result["tests"]
            
            # Score qualité
            quality_test = tests.get("quality_analysis", {})
            if "overall_score" in quality_test:
                total_quality_score += quality_test["overall_score"]
                
            # Score conformité
            compliance_test = tests.get("architecture_compliance", {})
            if "compliance_score" in compliance_test:
                total_compliance_score += compliance_test["compliance_score"]
            
            # Test améliorations réussi
            improvements_test = tests.get("adaptateur_improvements", {})
            if improvements_test.get("success", False):
                successful_tests += 1
        
        avg_quality_score = total_quality_score / total_agents if total_agents > 0 else 0
        avg_compliance_score = total_compliance_score / total_agents if total_agents > 0 else 0
        success_rate = successful_tests / total_agents if total_agents > 0 else 0
        
        results["overall_assessment"] = {
            "total_agents_tested": total_agents,
            "successful_adaptateur_tests": successful_tests,
            "success_rate": success_rate,
            "average_quality_score": avg_quality_score,
            "average_compliance_score": avg_compliance_score,
            "adaptateur_v43_functional": success_rate > 0.5,
            "overall_validation_passed": avg_quality_score > 0.7 and avg_compliance_score > 0.7
        }
        
        print(f"✅ Agents testés: {total_agents}")
        print(f"✅ Tests adaptateur réussis: {successful_tests}/{total_agents} ({success_rate*100:.1f}%)")
        print(f"✅ Score qualité moyen: {avg_quality_score:.2f}")
        print(f"✅ Score conformité moyen: {avg_compliance_score:.2f}")
        print(f"✅ Adaptateur v4.3.0 fonctionnel: {'✅' if results['overall_assessment']['adaptateur_v43_functional'] else '❌'}")
        print(f"✅ Validation globale: {'✅ SUCCÈS' if results['overall_assessment']['overall_validation_passed'] else '❌ ÉCHEC'}")
        
        return results

async def main():
    """Point d'entrée principal"""
    try:
        validator = ValidationMaintenanceAgents()
        results = await validator.run_complete_validation()
        
        # Sauvegarde des résultats
        report_file = PROJECT_ROOT / f"validation_report_agents_108_109_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            import json
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n📄 Rapport sauvegardé: {report_file}")
        except Exception as e:
            print(f"⚠️  Erreur sauvegarde rapport: {e}")
        
        # Retour du code de sortie
        overall_passed = results["overall_assessment"]["overall_validation_passed"]
        return 0 if overall_passed else 1
        
    except KeyboardInterrupt:
        print("\n⚠️ Validation interrompue par l'utilisateur")
        return 130
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))