#!/usr/bin/env python3
"""
🩺 TEST RÉPARATION ÉQUIPE POSTGRESQL
Test de réparation de l'équipe d'agents PostgreSQL avec l'agent docteur en mode production

Mission:
1. Analyser l'équipe PostgreSQL (score actuel: 38.4/100)
2. Appliquer le workflow de refactoring avec agent docteur
3. Valider les réparations effectuées
4. Mesurer l'amélioration des scores
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from agent_testeur_agents import create_agent_testeur_agents

async def test_reparation_equipe_postgresql():
    """Test de réparation complète de l'équipe PostgreSQL"""
    print("🩺 TEST RÉPARATION ÉQUIPE POSTGRESQL - NEXTGENERATION")
    print("=" * 70)
    
    # Répertoire de l'équipe PostgreSQL
    equipe_dir = Path("docs/agents_postgresql_resolution/agent team")
    
    if not equipe_dir.exists():
        print("❌ Répertoire équipe PostgreSQL non trouvé")
        return
    
    print(f"📁 Répertoire équipe: {equipe_dir}")
    agents_postgresql = list(equipe_dir.glob("agent_*.py"))
    print(f"📊 {len(agents_postgresql)} agents PostgreSQL à réparer")
    
    # ===== ÉTAPE 1: BASELINE AVANT RÉPARATION =====
    print("\n" + "="*70)
    print("📊 ÉTAPE 1: BASELINE AVANT RÉPARATION")
    print("="*70)
    
    testeur = create_agent_testeur_agents(safe_mode=True, test_timeout=30)
    
    try:
        await testeur.startup()
        
        # Mesure baseline
        print("🔍 Mesure des scores avant réparation...")
        scores_avant = {}
        
        for i, agent_file in enumerate(agents_postgresql, 1):
            print(f"   [{i}/{len(agents_postgresql)}] Test: {agent_file.name}")
            test_result = await testeur.tester_agent(str(agent_file))
            scores_avant[agent_file.name] = test_result.get('score_global', 0)
        
        score_moyen_avant = sum(scores_avant.values()) / len(scores_avant)
        print(f"\n📈 Score moyen AVANT réparation: {score_moyen_avant:.1f}/100")
        
        # ===== ÉTAPE 2: WORKFLOW REFACTORING AVEC DOCTEUR =====
        print("\n" + "="*70)
        print("🩺 ÉTAPE 2: WORKFLOW REFACTORING AVEC AGENT DOCTEUR")
        print("="*70)
        
        # Configuration tâche de refactoring
        task_refactoring = {
            'type': 'workflow_refactoring',
            'target_directory': str(equipe_dir),
            'agents_to_repair': [str(f) for f in agents_postgresql],
            'baseline_scores': scores_avant,
            'repair_mode': 'production'  # Mode production avec agent docteur
        }
        
        print("🚀 Lancement workflow refactoring...")
        print(f"   📁 Répertoire cible: {equipe_dir}")
        print(f"   🩺 Mode réparation: PRODUCTION")
        print(f"   📊 Score baseline: {score_moyen_avant:.1f}/100")
        
        # Exécution du workflow complet
        workflow_result = await testeur.execute_task(task_refactoring)
        
        print(f"\n✅ Workflow terminé!")
        print(f"   🎯 Succès global: {'✅' if workflow_result.get('success', False) else '❌'}")
        
        # Détails des phases
        phases = workflow_result.get('phases_results', {})
        
        print(f"\n📋 RÉSULTATS PAR PHASE:")
        for phase_name, phase_result in phases.items():
            success = phase_result.get('success', False)
            duration = phase_result.get('duration', 0)
            print(f"   {phase_name}: {'✅' if success else '❌'} ({duration:.1f}s)")
        
        # Détails réparation docteur
        post_refactoring = phases.get('post_refactoring', {})
        reparation_docteur = post_refactoring.get('reparation_docteur', {})
        
        if reparation_docteur:
            print(f"\n🩺 RÉPARATION DOCTEUR:")
            print(f"   🎯 Réparation nécessaire: {'✅' if reparation_docteur.get('repair_needed', False) else '❌'}")
            print(f"   🔧 Agents réparés: {reparation_docteur.get('agents_repaired', 0)}")
            print(f"   ✅ Réparations réussies: {reparation_docteur.get('repairs_successful', 0)}")
            print(f"   ❌ Réparations échouées: {reparation_docteur.get('repairs_failed', 0)}")
        
        # ===== ÉTAPE 3: VALIDATION APRÈS RÉPARATION =====
        print("\n" + "="*70)
        print("✅ ÉTAPE 3: VALIDATION APRÈS RÉPARATION")
        print("="*70)
        
        print("🔍 Mesure des scores après réparation...")
        scores_apres = {}
        
        for i, agent_file in enumerate(agents_postgresql, 1):
            print(f"   [{i}/{len(agents_postgresql)}] Re-test: {agent_file.name}")
            test_result = await testeur.tester_agent(str(agent_file))
            scores_apres[agent_file.name] = test_result.get('score_global', 0)
        
        score_moyen_apres = sum(scores_apres.values()) / len(scores_apres)
        print(f"\n📈 Score moyen APRÈS réparation: {score_moyen_apres:.1f}/100")
        
        # ===== ÉTAPE 4: ANALYSE AMÉLIORATION =====
        print("\n" + "="*70)
        print("📊 ÉTAPE 4: ANALYSE AMÉLIORATION")
        print("="*70)
        
        amelioration_globale = score_moyen_apres - score_moyen_avant
        pourcentage_amelioration = (amelioration_globale / score_moyen_avant) * 100 if score_moyen_avant > 0 else 0
        
        print(f"📈 AMÉLIORATION GLOBALE:")
        print(f"   📊 Score avant: {score_moyen_avant:.1f}/100")
        print(f"   📊 Score après: {score_moyen_apres:.1f}/100")
        print(f"   📈 Amélioration: {amelioration_globale:+.1f} points")
        print(f"   📊 Pourcentage: {pourcentage_amelioration:+.1f}%")
        
        # Analyse par agent
        print(f"\n🔍 AMÉLIORATION PAR AGENT:")
        
        agents_ameliores = 0
        agents_degrades = 0
        
        for agent_name in scores_avant.keys():
            avant = scores_avant[agent_name]
            apres = scores_apres[agent_name]
            diff = apres - avant
            
            if diff > 0:
                agents_ameliores += 1
                status = "📈"
            elif diff < 0:
                agents_degrades += 1
                status = "📉"
            else:
                status = "➡️"
            
            print(f"   {status} {agent_name.replace('.py', '')}")
            print(f"      {avant:.1f} → {apres:.1f} ({diff:+.1f})")
        
        print(f"\n📊 BILAN AGENTS:")
        print(f"   📈 Améliorés: {agents_ameliores}/{len(agents_postgresql)}")
        print(f"   📉 Dégradés: {agents_degrades}/{len(agents_postgresql)}")
        print(f"   ➡️ Inchangés: {len(agents_postgresql) - agents_ameliores - agents_degrades}/{len(agents_postgresql)}")
        
        await testeur.shutdown()
        
        # ===== RAPPORT FINAL =====
        print("\n" + "="*70)
        print("📄 GÉNÉRATION RAPPORT RÉPARATION")
        print("="*70)
        
        rapport_reparation = {
            "test_timestamp": datetime.now().isoformat(),
            "equipe_reparee": "Agents PostgreSQL Resolution",
            "nombre_agents": len(agents_postgresql),
            "workflow_result": workflow_result,
            "scores_avant": scores_avant,
            "scores_apres": scores_apres,
            "statistiques_amelioration": {
                "score_moyen_avant": score_moyen_avant,
                "score_moyen_apres": score_moyen_apres,
                "amelioration_globale": amelioration_globale,
                "pourcentage_amelioration": pourcentage_amelioration,
                "agents_ameliores": agents_ameliores,
                "agents_degrades": agents_degrades
            },
            "evaluation_finale": {
                "reparation_reussie": amelioration_globale > 0,
                "score_acceptable": score_moyen_apres >= 60,
                "pret_integration": score_moyen_apres >= 60 and agents_ameliores >= len(agents_postgresql) * 0.7
            }
        }
        
        # Sauvegarde rapport
        rapport_file = f"reparation_equipe_postgresql_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(rapport_reparation, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Rapport sauvegardé: {rapport_file}")
        
        # ===== CONCLUSION =====
        print("\n" + "="*70)
        print("🎯 CONCLUSION - RÉPARATION ÉQUIPE POSTGRESQL")
        print("="*70)
        
        if amelioration_globale > 0:
            print("✅ RÉPARATION RÉUSSIE!")
            print(f"   📈 Amélioration: {amelioration_globale:+.1f} points")
            print(f"   📊 {agents_ameliores} agents améliorés")
        else:
            print("❌ RÉPARATION INSUFFISANTE")
            print(f"   📉 Dégradation: {amelioration_globale:.1f} points")
        
        if score_moyen_apres >= 60:
            print("🚀 ÉQUIPE PRÊTE POUR INTÉGRATION NEXTGENERATION!")
        elif score_moyen_apres >= 40:
            print("⚠️ ÉQUIPE EN COURS D'AMÉLIORATION - Nouvelles réparations recommandées")
        else:
            print("🔧 ÉQUIPE NÉCESSITE RÉPARATIONS SUPPLÉMENTAIRES")
        
        # Recommandations finales
        print(f"\n💡 RECOMMANDATIONS:")
        if amelioration_globale > 0:
            print("   1. Poursuivre l'intégration des agents améliorés")
            print("   2. Appliquer les mêmes réparations aux agents similaires")
            print("   3. Documenter les corrections apportées")
        else:
            print("   1. Analyser les causes d'échec de la réparation")
            print("   2. Ajuster les paramètres de l'agent docteur")
            print("   3. Répéter le processus avec configuration optimisée")
        
        return rapport_reparation
        
    except Exception as e:
        print(f"❌ Erreur test réparation: {e}")
        if 'testeur' in locals():
            await testeur.shutdown()
        return None

if __name__ == "__main__":
    print("🩺 TEST RÉPARATION ÉQUIPE POSTGRESQL - NEXTGENERATION")
    print("Mission: Réparation complète avec agent docteur en mode production")
    print("=" * 70)
    
    asyncio.run(test_reparation_equipe_postgresql()) 



