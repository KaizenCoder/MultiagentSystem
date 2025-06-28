#!/usr/bin/env python3
"""
Migration Pilote - Agent 05 Maître Tests & Validation
Premier agent pilote de la Phase 1 : validation du pattern de migration NextGeneration

Objectifs:
- Valider le pattern de migration legacy → moderne
- Tester ShadowModeValidator avec >99.9% parité
- Documenter les insights pour migration en masse
- Établir les métriques de référence
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
import logging

# Add core to Python path
sys.path.insert(0, str(Path(__file__).parent / 'core'))
sys.path.insert(0, str(Path(__file__).parent / 'agents'))

async def migration_agent_05_pilot():
    """
    Migration pilote de l'Agent 05 avec validation ShadowMode complète
    """
    
    print("🚀 Phase 1 - Migration Pilote Agent 05")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Agent Target: agent_05_maitre_tests_validation")
    print(f"Migration Pattern: Legacy → NextGeneration Modern")
    
    migration_results = {
        "agent_id": "agent_05_maitre_tests_validation",
        "migration_start": datetime.now().isoformat(),
        "phase": "Phase 1 Pilot",
        "pattern_validation": {},
        "shadow_mode_results": {},
        "performance_comparison": {},
        "recommendations": []
    }
    
    # === ÉTAPE 1: CRÉATION INFRASTRUCTURE SHADOW MODE ===
    print("\n📋 Étape 1: Infrastructure ShadowMode")
    
    try:
        from core.services import (
            create_shadow_validator, ShadowModeConfig,
            create_llm_gateway, create_message_bus, create_context_store,
            GatewayConfig, ContextStoreConfig
        )
        
        # Configuration ShadowMode pour migration pilote
        shadow_config = ShadowModeConfig(
            similarity_threshold_activate=0.999,  # 99.9% parité requise
            similarity_threshold_acceptable=0.95,
            enable_auto_activation=False,  # Manuel pour pilote
            comparison_sample_size=5,
            voice_request_bypass=True
        )
        
        # Services NextGeneration (mode test sans Redis)
        from core.services.llm_gateway_hybrid import LLMGatewayHybrid
        
        # Configuration test sans dépendances externes
        gateway_config = GatewayConfig()
        gateway_config.redis_url = None  # Disable Redis for testing
        
        # Create gateway without Redis
        llm_gateway = LLMGatewayHybrid(gateway_config)
        # Skip initialization to avoid Redis connection
        llm_gateway.metrics = {
            "requests_total": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0,
            "avg_latency": 0.0
        }
        
        from core.services.message_bus_a2a import MessageBusConfig
        
        # Configuration MessageBus pour test (memory backend)
        bus_config = MessageBusConfig()
        bus_config.default_backend = "memory"
        bus_config.enable_legacy_bridge = True
        
        message_bus = await create_message_bus(bus_config)
        
        # ShadowModeValidator
        validator = await create_shadow_validator(
            shadow_config, llm_gateway, message_bus, None
        )
        
        print("✅ Infrastructure ShadowMode créée")
        migration_results["pattern_validation"]["infrastructure"] = "success"
        
    except Exception as e:
        print(f"❌ Erreur infrastructure: {e}")
        migration_results["pattern_validation"]["infrastructure"] = f"error: {e}"
        return migration_results
    
    # === ÉTAPE 2: CHARGEMENT AGENTS LEGACY ET MODERNE ===
    print("\n📋 Étape 2: Chargement Agents")
    
    try:
        # Agent Legacy
        print("📦 Chargement agent legacy...")
        sys.path.append(str(Path(__file__).parent / 'agents'))
        
        # Mock agent legacy pour démonstration
        class MockLegacyAgent05:
            def __init__(self):
                self.agent_id = "agent_05_maitre_tests_validation"
                self.version = "1.0.0-legacy"
                
            def execute(self, params):
                """Interface legacy simulée"""
                return {
                    "agent_id": self.agent_id,
                    "type_rapport": "auto_evaluation_tests",
                    "timestamp": datetime.now().isoformat(),
                    "version_agent": self.version,
                    "executive_summary": {
                        "score_global": 87,
                        "niveau_qualite": "BON",
                        "conformite": "✅ CONFORME",
                        "issues_critiques": 1
                    },
                    "resultats_tests": {
                        "total_tests": 65,
                        "tests_reussis": 64,
                        "tests_echoues": 1,
                        "taux_reussite": 98.5,
                        "temps_execution_ms": 1200
                    },
                    "recommandations": [
                        "Investiguer l'échec de test unitaire dans module X",
                        "Améliorer couverture tests pour atteindre 100%"
                    ],
                    "architecture": "legacy_pattern_factory"
                }
        
        legacy_agent = MockLegacyAgent05()
        print(f"✅ Agent legacy chargé: {legacy_agent.version}")
        
        # Agent Moderne
        print("🔬 Chargement agent moderne...")
        from agents.modern.agent_05_maitre_tests_validation_modern_fixed import create_agent_05_maitre_tests_validation as create_modern_agent_05
        
        modern_agent = create_modern_agent_05()
        if hasattr(modern_agent, 'startup'):
            await modern_agent.startup()
        print(f"✅ Agent moderne chargé: {modern_agent.version}")
        
        migration_results["pattern_validation"]["agents_loaded"] = "success"
        
    except Exception as e:
        print(f"❌ Erreur chargement agents: {e}")
        migration_results["pattern_validation"]["agents_loaded"] = f"error: {e}"
        return migration_results
    
    # === ÉTAPE 3: ENREGISTREMENT SHADOW MODE ===
    print("\n📋 Étape 3: Enregistrement ShadowMode")
    
    try:
        validator.register_legacy_agent("agent_05_maitre_tests_validation", legacy_agent)
        validator.register_modern_agent("agent_05_maitre_tests_validation", modern_agent)
        
        print("✅ Agents enregistrés dans ShadowMode")
        migration_results["pattern_validation"]["shadow_registration"] = "success"
        
    except Exception as e:
        print(f"❌ Erreur enregistrement: {e}")
        migration_results["pattern_validation"]["shadow_registration"] = f"error: {e}"
        return migration_results
    
    # === ÉTAPE 4: TESTS DE COMPARAISON SHADOW MODE ===
    print("\n📋 Étape 4: Tests Comparaison ShadowMode")
    
    shadow_comparisons = []
    
    try:
        from core.services import create_envelope, MessageType, Priority
        
        # Test Case 1: Analyse standard
        print("\n🧪 Test 1: Analyse Tests Standard")
        
        test_envelope_1 = create_envelope(
            task_id="pilot_test_001",
            message_type=MessageType.TASK_START,
            source_agent="migration_pilot",
            target_agent="agent_05_maitre_tests_validation",
            payload={
                "action": "analyze_tests",
                "type_rapport": "tests",
                "data": {"context": "migration_validation"}
            }
        )
        
        comparison_1 = await validator.dual_execution("agent_05_maitre_tests_validation", test_envelope_1)
        shadow_comparisons.append(comparison_1)
        
        print(f"  Similarity Score: {comparison_1.similarity_score:.3f}")
        print(f"  Validation Result: {comparison_1.validation_result.value}")
        print(f"  Activation Decision: {comparison_1.activation_decision.value}")
        print(f"  Legacy Time: {comparison_1.legacy_result.execution_time_ms}ms")
        print(f"  Modern Time: {comparison_1.modern_result.execution_time_ms}ms")
        
        # Test Case 2: Rapport validation
        print("\n🧪 Test 2: Rapport Validation")
        
        test_envelope_2 = create_envelope(
            task_id="pilot_test_002",
            message_type=MessageType.TASK_START,
            source_agent="migration_pilot",
            target_agent="agent_05_maitre_tests_validation",
            payload={
                "action": "analyze_tests",
                "type_rapport": "validation",
                "data": {"depth": "comprehensive"}
            }
        )
        
        comparison_2 = await validator.dual_execution("agent_05_maitre_tests_validation", test_envelope_2)
        shadow_comparisons.append(comparison_2)
        
        print(f"  Similarity Score: {comparison_2.similarity_score:.3f}")
        print(f"  Validation Result: {comparison_2.validation_result.value}")
        
        # Test Case 3: Rapport performance
        print("\n🧪 Test 3: Rapport Performance")
        
        test_envelope_3 = create_envelope(
            task_id="pilot_test_003",
            message_type=MessageType.TASK_START,
            source_agent="migration_pilot",
            target_agent="agent_05_maitre_tests_validation",
            payload={
                "action": "analyze_tests",
                "type_rapport": "performance",
                "data": {"metrics_focus": "execution_time"}
            }
        )
        
        comparison_3 = await validator.dual_execution("agent_05_maitre_tests_validation", test_envelope_3)
        shadow_comparisons.append(comparison_3)
        
        print(f"  Similarity Score: {comparison_3.similarity_score:.3f}")
        print(f"  Validation Result: {comparison_3.validation_result.value}")
        
        migration_results["shadow_mode_results"]["tests_completed"] = len(shadow_comparisons)
        migration_results["shadow_mode_results"]["comparisons"] = [
            {
                "test_id": comp.legacy_result.metadata.get("test_id", f"test_{i+1}"),
                "similarity_score": comp.similarity_score,
                "validation_result": comp.validation_result.value,
                "activation_decision": comp.activation_decision.value,
                "performance_improvement": (
                    comp.legacy_result.execution_time_ms - comp.modern_result.execution_time_ms
                ) / max(comp.legacy_result.execution_time_ms, 1) * 100
            }
            for i, comp in enumerate(shadow_comparisons)
        ]
        
        print("✅ Tests de comparaison terminés")
        
    except Exception as e:
        print(f"❌ Erreur tests comparaison: {e}")
        migration_results["shadow_mode_results"]["error"] = str(e)
        return migration_results
    
    # === ÉTAPE 5: ANALYSE DES RÉSULTATS ===
    print("\n📋 Étape 5: Analyse Résultats")
    
    try:
        # Métriques de migration
        similarity_scores = [comp.similarity_score for comp in shadow_comparisons]
        avg_similarity = sum(similarity_scores) / len(similarity_scores)
        
        legacy_times = [comp.legacy_result.execution_time_ms for comp in shadow_comparisons]
        modern_times = [comp.modern_result.execution_time_ms for comp in shadow_comparisons]
        
        avg_legacy_time = sum(legacy_times) / len(legacy_times) if legacy_times else 1
        avg_modern_time = sum(modern_times) / len(modern_times) if modern_times else 1
        performance_improvement = (avg_legacy_time - avg_modern_time) / max(avg_legacy_time, 1) * 100
        
        migration_results["performance_comparison"] = {
            "average_similarity_score": round(avg_similarity, 4),
            "similarity_threshold_met": avg_similarity >= 0.999,
            "average_legacy_time_ms": round(avg_legacy_time, 2),
            "average_modern_time_ms": round(avg_modern_time, 2),
            "performance_improvement_percent": round(performance_improvement, 2),
            "tests_passed": len([c for c in shadow_comparisons if c.validation_result.value in ["identical", "similar"]]),
            "total_tests": len(shadow_comparisons)
        }
        
        # Status de migration
        migration_status = "SUCCESS" if avg_similarity >= 0.999 else "NEEDS_REVIEW"
        
        print(f"\n📊 Résultats Migration Pilote:")
        print(f"  Average Similarity: {avg_similarity:.4f}")
        print(f"  Threshold Met (>99.9%): {avg_similarity >= 0.999}")
        print(f"  Performance Improvement: {performance_improvement:.1f}%")
        print(f"  Migration Status: {migration_status}")
        
        migration_results["migration_status"] = migration_status
        
    except Exception as e:
        print(f"❌ Erreur analyse: {e}")
        migration_results["analysis_error"] = str(e)
    
    # === ÉTAPE 6: RECOMMANDATIONS ===
    print("\n📋 Étape 6: Recommandations")
    
    recommendations = []
    
    if avg_similarity >= 0.999:
        recommendations.append("✅ Migration réussie - Pattern validé pour agents similaires")
        recommendations.append("✅ ShadowMode validation efficace - Prêt pour Phase 2")
    elif avg_similarity >= 0.95:
        recommendations.append("⚠️ Similarité acceptable mais nécessite review manuelle")
        recommendations.append("🔧 Ajuster pattern de migration avant généralisation")
    else:
        recommendations.append("❌ Migration échoue critères - Revoir architecture moderne")
        recommendations.append("🔧 Analyser différences structurelles legacy vs moderne")
    
    if performance_improvement > 0:
        recommendations.append(f"📈 Amélioration performance de {performance_improvement:.1f}% validée")
    else:
        recommendations.append("⚠️ Performance dégradée - Optimiser agent moderne")
    
    recommendations.append("📚 Documenter pattern pour agents de type TESTING")
    recommendations.append("🔄 Préparer migration Agent 111 (prochain pilote)")
    
    migration_results["recommendations"] = recommendations
    
    for rec in recommendations:
        print(f"  {rec}")
    
    # === FINALISATION ===
    migration_results["migration_end"] = datetime.now().isoformat()
    migration_results["duration_seconds"] = (
        datetime.fromisoformat(migration_results["migration_end"]) - 
        datetime.fromisoformat(migration_results["migration_start"])
    ).total_seconds()
    
    print(f"\n🎉 Migration Pilote Agent 05 Terminée")
    print(f"Status: {migration_results['migration_status']}")
    print(f"Durée: {migration_results['duration_seconds']:.1f}s")
    
    # Sauvegarde résultats
    results_file = Path(__file__).parent / "reports" / f"migration_pilot_agent_05_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(migration_results, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Résultats sauvegardés: {results_file}")
    
    return migration_results

# Fonction principale
async def main():
    """Point d'entrée principal"""
    
    try:
        results = await migration_agent_05_pilot()
        
        # Summary pour tracking
        print("\n" + "="*60)
        print("📊 SUMMARY - Migration Pilote Agent 05")
        print("="*60)
        
        print(f"Migration Status: {results.get('migration_status', 'UNKNOWN')}")
        print(f"Tests Completed: {results.get('shadow_mode_results', {}).get('tests_completed', 0)}")
        
        perf = results.get('performance_comparison', {})
        print(f"Similarity Score: {perf.get('average_similarity_score', 0):.4f}")
        print(f"Performance Gain: {perf.get('performance_improvement_percent', 0):.1f}%")
        
        return results
        
    except Exception as e:
        print(f"❌ Migration pilote échoué: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    asyncio.run(main())