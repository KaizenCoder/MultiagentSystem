#!/usr/bin/env python3
"""
🧪 TEST ÉQUIPE DE MAINTENANCE TRANSFORMÉE
Test complet des 4 agents de maintenance avec leurs nouvelles capacités avancées
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys

# Import des agents transformés
from agents.agent_MAINTENANCE_01_analyseur_structure import create_agent_analyseur_structure
from agents.agent_MAINTENANCE_02_evaluateur_utilite import create_agent_evaluateur_utilite  
from agents.agent_MAINTENANCE_03_adaptateur_code import create_agent_3_adaptateur_code
from agents.agent_MAINTENANCE_04_testeur_anti_faux_agents import create_agent_testeur_anti_faux

async def test_agent_01_transforme():
    """Test de l'Agent 01 - Analyseur Structure transformé"""
    print("\n🔬 TEST AGENT 01 - ANALYSEUR STRUCTURE TRANSFORMÉ")
    print("=" * 60)
    
    agent = create_agent_analyseur_structure()
    
    try:
        await agent.startup()
        
        # Test des nouvelles capacités
        capabilities = agent.get_capabilities()
        print(f"📋 Capacités totales: {len(capabilities)}")
        
        nouvelles_capacites = [cap for cap in capabilities if cap in [
            "advanced_ast_analysis", "intelligent_classification", 
            "dependency_graph_analysis", "code_quality_metrics",
            "security_analysis", "enterprise_readiness_assessment"
        ]]
        
        print(f"🆕 Nouvelles capacités avancées: {len(nouvelles_capacites)}")
        for cap in nouvelles_capacites:
            print(f"   ✅ {cap}")
        
        # Test health check
        health = await agent.health_check()
        print(f"🏥 Health: {health['status']}")
        
        await agent.shutdown()
        
        return {
            "agent": "01_analyseur_structure",
            "status": "SUCCESS",
            "nouvelles_capacites": len(nouvelles_capacites),
            "total_capacites": len(capabilities)
        }
        
    except Exception as e:
        await agent.shutdown()
        return {
            "agent": "01_analyseur_structure", 
            "status": "ERROR",
            "error": str(e)
        }

async def test_agent_02_transforme():
    """Test de l'Agent 02 - Évaluateur Utilité transformé"""
    print("\n🔬 TEST AGENT 02 - ÉVALUATEUR UTILITÉ TRANSFORMÉ")
    print("=" * 60)
    
    agent = create_agent_evaluateur_utilite()
    
    try:
        await agent.startup()
        
        # Test des nouvelles capacités
        capabilities = agent.get_capabilities()
        print(f"📋 Capacités totales: {len(capabilities)}")
        
        nouvelles_capacites = [cap for cap in capabilities if cap in [
            "weighted_evaluation_system", "intelligent_conflict_detection",
            "redundancy_analysis", "business_value_assessment", 
            "roi_calculation", "risk_assessment",
            "technology_stack_compatibility", "compliance_assessment"
        ]]
        
        print(f"🆕 Nouvelles capacités avancées: {len(nouvelles_capacites)}")
        for cap in nouvelles_capacites:
            print(f"   ✅ {cap}")
        
        # Test health check
        health = await agent.health_check()
        print(f"🏥 Health: {health['status']}")
        
        await agent.shutdown()
        
        return {
            "agent": "02_evaluateur_utilite",
            "status": "SUCCESS", 
            "nouvelles_capacites": len(nouvelles_capacites),
            "total_capacites": len(capabilities)
        }
        
    except Exception as e:
        await agent.shutdown()
        return {
            "agent": "02_evaluateur_utilite",
            "status": "ERROR",
            "error": str(e)
        }

async def test_agent_03_transforme():
    """Test de l'Agent 03 - Adaptateur Code transformé"""
    print("\n🔬 TEST AGENT 03 - ADAPTATEUR CODE TRANSFORMÉ")
    print("=" * 60)
    
    agent = create_agent_3_adaptateur_code()
    
    try:
        await agent.startup()
        
        # Test des nouvelles capacités
        capabilities = agent.get_capabilities()
        print(f"📋 Capacités totales: {len(capabilities)}")
        
        nouvelles_capacites = [cap for cap in capabilities if cap in [
            "ast_transformation", "code_modernization",
            "pattern_factory_conversion", "async_await_transformation",
            "import_optimization", "docstring_generation",
            "error_handling_injection", "logging_integration",
            "type_hint_addition", "code_quality_improvement"
        ]]
        
        print(f"🆕 Nouvelles capacités avancées: {len(nouvelles_capacites)}")
        for cap in nouvelles_capacites:
            print(f"   ✅ {cap}")
        
        # Test health check
        health = await agent.health_check()
        print(f"🏥 Health: {health['status']}")
        
        # Test d'une transformation simple
        test_code = """
def hello_world():
    print("Hello World")
    return True
"""
        
        transformation_result = await agent.code_modernization(test_code)
        print(f"🔄 Test transformation: {transformation_result['modernization_score']:.1f}%")
        
        await agent.shutdown()
        
        return {
            "agent": "03_adaptateur_code",
            "status": "SUCCESS",
            "nouvelles_capacites": len(nouvelles_capacites),
            "total_capacites": len(capabilities),
            "transformation_test": transformation_result['modernization_score']
        }
        
    except Exception as e:
        await agent.shutdown()
        return {
            "agent": "03_adaptateur_code",
            "status": "ERROR", 
            "error": str(e)
        }

async def test_agent_04_transforme():
    """Test Agent 04 - Testeur Anti-Faux Transformé"""
    print("\n🔬 TEST AGENT 04 - TESTEUR ANTI-FAUX TRANSFORMÉ")
    print("=" * 60)
    
    try:
        agent = create_agent_testeur_anti_faux()
        
        await agent.startup()
        
        # Test des capacités
        capabilities = agent.get_capabilities()
        nouvelles_capacites = [
            "async_sync_validation",
            "compliance_scoring",
            "advanced_static_analysis", 
            "suspicious_patterns_detection",
            "mandatory_methods_validation",
            "import_validation",
            "enterprise_grade_validation",
            "security_patterns_detection"
        ]
        
        nouvelles_validees = [cap for cap in nouvelles_capacites if cap in capabilities]
        
        print(f"📋 Capacités totales: {len(capabilities)}")
        print(f"🆕 Nouvelles capacités avancées: {len(nouvelles_validees)}")
        for cap in nouvelles_validees:
            print(f"   ✅ {cap}")
        
        # Test health check
        health = await agent.health_check()
        print(f"🏥 Health: {health.get('status', 'unknown')}")
        
        await agent.shutdown()
        
        return {
            "agent_id": health.get("agent_id", "unknown"),
            "status": "SUCCESS",
            "capabilities": len(capabilities),
            "nouvelles_capacites": len(nouvelles_validees),
            "health": health.get('status', 'unknown')
        }
        
    except Exception as e:
        print(f"❌ ERREUR Agent 04: {e}")
        return {
            "agent_id": "agent_04_error", 
            "status": "ERROR",
            "error": str(e),
            "capabilities": 0,
            "nouvelles_capacites": 0,
            "health": "error"
        }

async def test_equipe_collaborative():
    """Test de collaboration entre les agents transformés"""
    print("\n🔬 TEST COLLABORATION ÉQUIPE TRANSFORMÉE")
    print("=" * 60)
    
    try:
        # Créer tous les agents
        agent_01 = create_agent_analyseur_structure()
        agent_02 = create_agent_evaluateur_utilite()
        agent_03 = create_agent_3_adaptateur_code()
        agent_04 = create_agent_testeur_anti_faux()
        
        # Démarrer tous les agents
        await asyncio.gather(
            agent_01.startup(),
            agent_02.startup(), 
            agent_03.startup(),
            agent_04.startup()
        )
        
        print("✅ Tous les agents démarrés")
        
        # Test de santé collective
        health_checks = await asyncio.gather(
            agent_01.health_check(),
            agent_02.health_check(),
            agent_03.health_check(), 
            agent_04.health_check()
        )
        
        healthy_agents = sum(1 for health in health_checks if health['status'] == 'healthy')
        print(f"🏥 Agents en bonne santé: {healthy_agents}/4")
        
        # Calcul des capacités totales de l'équipe
        all_capabilities = []
        for agent in [agent_01, agent_02, agent_03, agent_04]:
            all_capabilities.extend(agent.get_capabilities())
        
        unique_capabilities = len(set(all_capabilities))
        total_capabilities = len(all_capabilities)
        
        print(f"🎯 Capacités uniques de l'équipe: {unique_capabilities}")
        print(f"📊 Capacités totales: {total_capabilities}")
        
        # Arrêter tous les agents
        await asyncio.gather(
            agent_01.shutdown(),
            agent_02.shutdown(),
            agent_03.shutdown(),
            agent_04.shutdown()
        )
        
        return {
            "test": "equipe_collaborative",
            "status": "SUCCESS",
            "agents_healthy": healthy_agents,
            "capacites_uniques": unique_capabilities,
            "capacites_totales": total_capabilities
        }
        
    except Exception as e:
        return {
            "test": "equipe_collaborative",
            "status": "ERROR",
            "error": str(e)
        }

async def main():
    """Test principal de l'équipe de maintenance transformée"""
    print("🚀 TEST COMPLET - ÉQUIPE DE MAINTENANCE TRANSFORMÉE")
    print("=" * 80)
    print(f"📅 Timestamp: {datetime.now().isoformat()}")
    print(f"🎯 Objectif: Valider la transformation avec nouvelles capacités avancées")
    
    # Exécuter tous les tests
    results = await asyncio.gather(
        test_agent_01_transforme(),
        test_agent_02_transforme(), 
        test_agent_03_transforme(),
        test_agent_04_transforme(),
        test_equipe_collaborative()
    )
    
    # Analyse des résultats
    print("\n📊 RÉSULTATS FINAUX")
    print("=" * 80)
    
    success_count = sum(1 for result in results if result['status'] == 'SUCCESS')
    total_nouvelles_capacites = sum(result.get('nouvelles_capacites', 0) for result in results if 'nouvelles_capacites' in result)
    total_capacites = sum(result.get('total_capacites', 0) for result in results if 'total_capacites' in result)
    
    print(f"✅ Tests réussis: {success_count}/5 ({success_count/5*100:.1f}%)")
    print(f"🆕 Nouvelles capacités ajoutées: {total_nouvelles_capacites}")
    print(f"📋 Capacités totales: {total_capacites}")
    
    if success_count == 5:
        print("\n🎉 TRANSFORMATION COMPLÈTE RÉUSSIE!")
        print("   ✅ Tous les agents de maintenance sont transformés")
        print("   ✅ Nouvelles capacités avancées intégrées")
        print("   ✅ Équipe prête pour la production")
        
        transformation_summary = {
            "transformation_status": "COMPLETED",
            "agents_transformed": 4,
            "tests_passed": f"{success_count}/5",
            "nouvelles_capacites": total_nouvelles_capacites,
            "capacites_totales": total_capacites,
            "timestamp": datetime.now().isoformat(),
            "next_phase": "DÉPLOIEMENT_PRODUCTION"
        }
        
    else:
        print(f"\n⚠️ TRANSFORMATION PARTIELLE ({success_count}/5)")
        print("   🔧 Corrections nécessaires sur les agents en échec")
        
        transformation_summary = {
            "transformation_status": "PARTIAL",
            "agents_transformed": success_count - 1,  # -1 pour le test collaboratif
            "tests_passed": f"{success_count}/5", 
            "issues": [result for result in results if result['status'] == 'ERROR'],
            "timestamp": datetime.now().isoformat(),
            "next_phase": "CORRECTIONS_REQUISES"
        }
    
    # Sauvegarder le rapport
    with open('rapport_transformation_equipe_maintenance.json', 'w', encoding='utf-8') as f:
        json.dump({
            "summary": transformation_summary,
            "detailed_results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Rapport sauvegardé: rapport_transformation_equipe_maintenance.json")
    
    return transformation_summary

if __name__ == "__main__":
    asyncio.run(main()) 




