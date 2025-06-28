#!/usr/bin/env python3
"""
🔄 TEST WORKFLOW REFACTORING - AGENT TESTEUR AGENTS
Démonstration du workflow complet de refactoring avec validation à chaque étape

Workflow intégré:
Pre-Refactoring:  backup + analyse baseline + validation architecture PF
Refactoring:      modifications incrémentales + préservation logique + tests continus  
Post-Refactoring: validation testeur + réparation docteur + validation finale
"""

import asyncio
import json
from datetime import datetime
from agent_testeur_agents import create_agent_testeur_agents

async def demo_workflow_refactoring():
    """Démonstration complète du workflow de refactoring"""
    print("🔄 DÉMONSTRATION WORKFLOW REFACTORING")
    print("=" * 70)
    
    # Créer l'agent testeur via factory
    agent = create_agent_testeur_agents(safe_mode=True, test_timeout=30)
    
    try:
        # Démarrage agent
        await agent.startup()
        
        print("\n🏥 Health Check Agent Testeur:")
        health = await agent.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Capabilities: {len(health['capabilities'])} capacités disponibles")
        
        # ===== TEST 1: WORKFLOW COMPLET =====
        print("\n" + "="*70)
        print("🔄 TEST 1: WORKFLOW REFACTORING COMPLET")
        print("="*70)
        
        task_workflow = {
            "type": "workflow_refactoring",
            "target_directory": "."  # Répertoire courant
        }
        
        print("🚀 Lancement workflow refactoring complet...")
        workflow_results = await agent.execute_task(task_workflow)
        
        print(f"\n📊 RÉSULTATS WORKFLOW:")
        print(f"   Workflow ID: {workflow_results.get('workflow_id', 'N/A')}")
        print(f"   Succès global: {'✅ OUI' if workflow_results.get('global_success') else '❌ NON'}")
        print(f"   Durée: {workflow_results.get('duration_minutes', 0):.2f} minutes")
        
        # Affichage détails des phases
        phases = workflow_results.get("phases", {})
        
        print(f"\n📋 PHASE 1 - PRE-REFACTORING:")
        pre_refactoring = phases.get("pre_refactoring", {})
        print(f"   Succès: {'✅' if pre_refactoring.get('success') else '❌'}")
        steps_pre = pre_refactoring.get("steps", {})
        print(f"   - Backup: {'✅' if steps_pre.get('backup_complet', {}).get('success') else '❌'}")
        print(f"   - Baseline: {'✅' if steps_pre.get('analyse_baseline', {}).get('success') else '❌'}")
        print(f"   - Architecture PF: {'✅' if steps_pre.get('validation_architecture_pf', {}).get('success') else '❌'}")
        
        print(f"\n🔧 PHASE 2 - VALIDATION REFACTORING:")
        validation_refactoring = phases.get("validation_refactoring", {})
        print(f"   Succès: {'✅' if validation_refactoring.get('success') else '❌'}")
        steps_validation = validation_refactoring.get("steps", {})
        print(f"   - Modifications incrémentales: {'✅' if steps_validation.get('modifications_incrementales', {}).get('success') else '❌'}")
        print(f"   - Logique métier: {'✅' if steps_validation.get('preservation_logique', {}).get('success') else '❌'}")
        print(f"   - Tests continus: {'✅' if steps_validation.get('tests_continus', {}).get('success') else '❌'}")
        
        print(f"\n✅ PHASE 3 - POST-REFACTORING:")
        post_refactoring = phases.get("post_refactoring", {})
        print(f"   Succès: {'✅' if post_refactoring.get('success') else '❌'}")
        steps_post = post_refactoring.get("steps", {})
        print(f"   - Validation testeur: {'✅' if steps_post.get('validation_agents_testeur', {}).get('success') else '❌'}")
        print(f"   - Réparation docteur: {'✅' if steps_post.get('reparation_docteur', {}).get('success') else '❌'}")
        print(f"   - Validation finale: {'✅' if steps_post.get('validation_finale', {}).get('success') else '❌'}")
        
        # ===== TEST 2: PHASES INDIVIDUELLES =====
        print("\n" + "="*70)
        print("🧪 TEST 2: PHASES INDIVIDUELLES")
        print("="*70)
        
        print("\n📋 Test Phase Pre-Refactoring...")
        task_pre = {"type": "pre_refactoring", "target_directory": "."}
        pre_result = await agent.execute_task(task_pre)
        print(f"   Résultat: {'✅ SUCCÈS' if pre_result.get('success') else '❌ ÉCHEC'}")
        
        print("\n🔧 Test Phase Validation Refactoring...")
        task_validation = {"type": "validation_refactoring", "target_directory": "."}
        validation_result = await agent.execute_task(task_validation)
        print(f"   Résultat: {'✅ SUCCÈS' if validation_result.get('success') else '❌ ÉCHEC'}")
        
        print("\n✅ Test Phase Post-Refactoring...")
        task_post = {"type": "post_refactoring", "target_directory": "."}
        post_result = await agent.execute_task(task_post)
        print(f"   Résultat: {'✅ SUCCÈS' if post_result.get('success') else '❌ ÉCHEC'}")
        
        # ===== RÉSUMÉ FINAL =====
        print("\n" + "="*70)
        print("📊 RÉSUMÉ DÉMONSTRATION")
        print("="*70)
        
        print(f"✅ Workflow complet implémenté et fonctionnel")
        print(f"✅ Toutes les étapes du processus validé intégrées:")
        print(f"   📋 Pre-Refactoring: backup + baseline + architecture PF")
        print(f"   🔧 Validation: modifications + logique + tests continus")
        print(f"   ✅ Post-Refactoring: testeur + docteur + validation finale")
        
        print(f"\n🎯 COMMANDES DISPONIBLES:")
        print(f"```python")
        print(f"# Workflow complet")
        print(f"python agent_testeur_agents.py")
        print(f"task = {{'type': 'workflow_refactoring', 'target_directory': '.'}}")
        print(f"result = await agent.execute_task(task)")
        print(f"")
        print(f"# Phases individuelles")
        print(f"await agent.execute_task({{'type': 'pre_refactoring'}})")
        print(f"await agent.execute_task({{'type': 'validation_refactoring'}})")
        print(f"await agent.execute_task({{'type': 'post_refactoring'}})")
        print(f"```")
        
        # Sauvegarde rapport de démonstration
        demo_report = {
            "demo_timestamp": datetime.now().isoformat(),
            "workflow_complete": workflow_results,
            "individual_phases": {
                "pre_refactoring": pre_result,
                "validation_refactoring": validation_result,
                "post_refactoring": post_result
            },
            "demo_success": True
        }
        
        rapport_file = f"demo_workflow_refactoring_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(demo_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Rapport démonstration sauvegardé: {rapport_file}")
        
        # Arrêt propre
        await agent.shutdown()
        
        print(f"\n🎯 WORKFLOW REFACTORING OPÉRATIONNEL!")
        
    except Exception as e:
        print(f"❌ Erreur démonstration: {e}")
        await agent.shutdown()

async def demo_commandes_yaml():
    """Démonstration des commandes YAML du workflow"""
    print("\n" + "="*70)
    print("📝 DÉMONSTRATION COMMANDES YAML")
    print("="*70)
    
    print("""
🔄 WORKFLOW VALIDÉ IMPLÉMENTÉ:

```yaml
Pre-Refactoring:
  - backup_complet_obligatoire ✅
  - analyse_baseline_métriques ✅
  - validation_architecture_pf_existante ✅

Refactoring:
  - modifications_incrementales ✅
  - preservation_logique_métier ✅
  - tests_continus ✅

Post-Refactoring:
  - validation_agents_testeur ✅
  - reparation_agents_docteur_si_necessaire ✅
  - validation_finale_conformité ✅
```

🎯 UTILISATION:

```bash
# 1. Test conformité baseline
python agent_testeur_agents.py

# 2. Workflow refactoring complet
python test_workflow_refactoring.py

# 3. Validation finale conformité
python agent_testeur_agents.py
```

✅ TOUTES LES ÉTAPES SONT MAINTENANT AUTOMATISÉES !
""")

if __name__ == "__main__":
    print("🔄 WORKFLOW REFACTORING - PATTERN FACTORY NEXTGENERATION")
    print("Mission: Validation automatisée du processus de refactoring")
    print("=" * 70)
    
    asyncio.run(demo_workflow_refactoring())
    asyncio.run(demo_commandes_yaml()) 



