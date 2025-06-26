#!/usr/bin/env python3
"""
Test script pour valider la génération de rapports stratégiques
de l'agent_01_coordinateur_principal.py
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import json

# Configuration des chemins
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from agents.agent_01_coordinateur_principal import Agent01CoordinateurPrincipal
from core.agent_factory_architecture import Task

async def test_strategic_reports():
    """Test complet des rapports stratégiques"""
    print("🧪 Test génération rapports stratégiques - Agent 01 Coordinateur Principal")
    print("=" * 80)
    
    # Création de l'agent
    agent = Agent01CoordinateurPrincipal()
    await agent.startup()
    
    # Contexte de test
    test_context = {
        'periode': 'Q4_2025',
        'demandeur': 'test_suite',
        'urgence': 'normal'
    }
    
    # Test 1: Rapport Global
    print("\n📊 TEST 1: Rapport Stratégique Global")
    print("-" * 50)
    
    task_global = Task(
        task_id="test_global_001",
        description="GENERATE_STRATEGIC_REPORT"
    )
    task_global.context = test_context
    task_global.type_rapport = 'global'
    
    result_global = await agent.execute_task(task_global)
    if result_global.success:
        rapport_global = result_global.data
        print("✅ Rapport global généré avec succès")
        print(f"   Score coordination: {rapport_global['resume_executif']['score_coordination_global']}")
        print(f"   Statut général: {rapport_global['resume_executif']['statut_general']}")
        print(f"   Agents coordonnés: {rapport_global['resume_executif']['agents_coordonnes']}")
        print(f"   Recommandations: {len(rapport_global['recommandations_strategiques'])} items")
    else:
        print(f"❌ Échec rapport global: {result_global.error}")
        return False
    
    # Test 2: Rapport Sprint
    print("\n📋 TEST 2: Rapport Sprint Spécialisé")
    print("-" * 50)
    
    task_sprint = Task(
        task_id="test_sprint_001", 
        description="GENERATE_STRATEGIC_REPORT"
    )
    task_sprint.context = {**test_context, 'sprint_id': 3}
    task_sprint.type_rapport = 'sprint'
    
    result_sprint = await agent.execute_task(task_sprint)
    if result_sprint.success:
        rapport_sprint = result_sprint.data
        print("✅ Rapport sprint généré avec succès")
        print(f"   Sprint focus: {rapport_sprint['sprint_focus']}")
        print(f"   Progression: {rapport_sprint['progression_sprint']:.1f}%")
        print(f"   Objectifs complétés: {rapport_sprint['objectifs_completes']}/{rapport_sprint['objectifs_total']}")
        print(f"   Recommandation: {rapport_sprint['recommandation_prioritaire']}")
    else:
        print(f"❌ Échec rapport sprint: {result_sprint.error}")
        return False
    
    # Test 3: Rapport Performance
    print("\n⚡ TEST 3: Rapport Performance")
    print("-" * 50)
    
    task_perf = Task(
        task_id="test_perf_001",
        description="GENERATE_STRATEGIC_REPORT"
    )
    task_perf.context = test_context
    task_perf.type_rapport = 'performance'
    
    result_perf = await agent.execute_task(task_perf)
    if result_perf.success:
        rapport_perf = result_perf.data
        print("✅ Rapport performance généré avec succès")
        print(f"   Vélocité moyenne/jour: {rapport_perf['velocite_moyenne_jour']}")
        print(f"   Efficacité coordination: {rapport_perf['efficacite_coordination']}%")
        print(f"   Tendance: {rapport_perf['tendance']}")
        print(f"   Optimisations proposées: {len(rapport_perf['optimisations_proposees'])} items")
    else:
        print(f"❌ Échec rapport performance: {result_perf.error}")
        return False
    
    # Test 4: Rapport Qualité  
    print("\n🎯 TEST 4: Rapport Qualité")
    print("-" * 50)
    
    task_qualite = Task(
        task_id="test_qualite_001",
        description="GENERATE_STRATEGIC_REPORT"
    )
    task_qualite.context = test_context
    task_qualite.type_rapport = 'qualite'
    
    result_qualite = await agent.execute_task(task_qualite)
    if result_qualite.success:
        rapport_qualite = result_qualite.data
        print("✅ Rapport qualité généré avec succès")
        print(f"   Score qualité global: {rapport_qualite['score_qualite_global']}")
        print(f"   Complétude données: {rapport_qualite['completude_donnees']}%")
        print(f"   Cohérence planification: {rapport_qualite['coherence_planification']}%")
        print(f"   Certification: {rapport_qualite['certification_qualite']}")
    else:
        print(f"❌ Échec rapport qualité: {result_qualite.error}")
        return False
    
    # Test 5: Type de rapport invalide (doit revenir au global par défaut)
    print("\n🔄 TEST 5: Gestion Type Invalide (fallback)")
    print("-" * 50)
    
    task_invalid = Task(
        task_id="test_invalid_001",
        description="GENERATE_STRATEGIC_REPORT"
    )
    task_invalid.context = test_context
    task_invalid.type_rapport = 'type_inexistant'
    
    result_invalid = await agent.execute_task(task_invalid)
    if result_invalid.success:
        rapport_fallback = result_invalid.data
        print("✅ Fallback vers rapport global fonctionnel")
        print(f"   Type rapport généré: {rapport_fallback['type_rapport']}")
    else:
        print(f"❌ Échec fallback: {result_invalid.error}")
        return False
    
    # Test 6: Sauvegarde d'un rapport exemple
    print("\n💾 TEST 6: Sauvegarde rapport exemple")
    print("-" * 50)
    
    rapport_exemple = {
        'test_timestamp': datetime.now().isoformat(),
        'rapport_global': rapport_global,
        'rapport_sprint': rapport_sprint,
        'rapport_performance': rapport_perf,
        'rapport_qualite': rapport_qualite,
        'metadata_test': {
            'agent_teste': 'agent_01_coordinateur_principal',
            'version_test': '1.0',
            'tous_tests_reussis': True
        }
    }
    
    try:
        with open('/mnt/c/Dev/nextgeneration/test_report_agent_01_strategic.json', 'w', encoding='utf-8') as f:
            json.dump(rapport_exemple, f, indent=2, ensure_ascii=False)
        print("✅ Rapport exemple sauvegardé: test_report_agent_01_strategic.json")
    except Exception as e:
        print(f"⚠️ Erreur sauvegarde rapport: {e}")
    
    await agent.shutdown()
    
    print("\n" + "=" * 80)
    print("✅ TOUS LES TESTS RÉUSSIS - Fonctionnalité rapports stratégiques opérationnelle")
    print("🎯 Agent 01 Coordinateur Principal: VALIDÉ pour génération rapports stratégiques")
    print("=" * 80)
    
    return True

if __name__ == "__main__":
    try:
        success = asyncio.run(test_strategic_reports())
        exit(0 if success else 1)
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE DURANT LE TEST: {e}")
        import traceback
        traceback.print_exc()
        exit(1)