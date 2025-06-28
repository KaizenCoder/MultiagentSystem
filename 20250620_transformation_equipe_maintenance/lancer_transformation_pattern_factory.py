#!/usr/bin/env python3
"""
🏭 LANCEUR TRANSFORMATION PATTERN FACTORY
==========================================

Script qui utilise l'Agent 03 Upgraded pour transformer automatiquement
les agents non-conformes détectés par l'Agent 04.

Workflow:
1. Utilise les rapports d'audit de l'Agent 04
2. Lance l'Agent 03 Upgraded pour les transformations
3. Valide les transformations effectuées
4. Génère un rapport consolidé

Author: Équipe Maintenance NextGeneration
Version: 1.0.0
Created: 2025-01-20
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from datetime import datetime

def main():
    """Lancer la transformation Pattern Factory avec l'Agent 03 Upgraded"""
    
    print("🏭 LANCEUR TRANSFORMATION PATTERN FACTORY")
    print("=" * 70)
    
    # Vérifier que nous sommes dans le bon répertoire
    current_dir = Path.cwd()
    if not (current_dir / "agent_equipe_maintenance").exists():
        print("❌ Erreur: Veuillez lancer ce script depuis le répertoire 20250620_transformation_equipe_maintenance")
        sys.exit(1)
    
    # Vérifier que le répertoire cible existe
    target_dir = Path("../agent_factory_implementation/agents")
    if not target_dir.exists():
        print(f"❌ Erreur: Répertoire cible non trouvé: {target_dir}")
        print("   Vérifiez que le répertoire agent_factory_implementation/agents existe")
        sys.exit(1)
    
    print(f"✅ Répertoire cible trouvé: {target_dir.resolve()}")
    
    # Chercher le rapport d'audit le plus récent de l'Agent 04
    reports_dir = target_dir / "reviews"
    if not reports_dir.exists():
        print(f"❌ Erreur: Aucun rapport d'audit trouvé dans: {reports_dir}")
        print("   Lancez d'abord l'Agent 04 pour générer un rapport d'audit")
        sys.exit(1)
    
    # Trouver le rapport d'audit Pattern Factory le plus récent
    audit_reports = list(reports_dir.glob("pattern_factory_audit_*.json"))
    if not audit_reports:
        print(f"❌ Erreur: Aucun rapport Pattern Factory trouvé dans: {reports_dir}")
        print("   Lancez d'abord l'Agent 04 avec lancer_mission_analyse_factory_direct.py")
        sys.exit(1)
    
    # Prendre le rapport le plus récent
    latest_audit_report = max(audit_reports, key=lambda p: p.stat().st_mtime)
    print(f"✅ Rapport d'audit trouvé: {latest_audit_report}")
    
    # Ajouter le répertoire des agents au PATH
    sys.path.insert(0, str(current_dir / "agent_equipe_maintenance"))
    
    print(f"\n📋 MISSION TRANSFORMATION:")
    print(f"   • Rapport d'audit: {latest_audit_report.name}")
    print(f"   • Répertoire cible: {target_dir}")
    print(f"   • Agent utilisé: Agent 03 Adaptateur Code Upgraded")
    
    print(f"\n⚡ LANCEMENT TRANSFORMATION...")
    
    mission_results = {
        "mission_id": f"transformation_pattern_factory_{int(time.time())}",
        "timestamp_debut": datetime.now().isoformat(),
        "audit_report_used": str(latest_audit_report),
        "target_directory": str(target_dir.resolve()),
        "transformation_results": {},
        "status": "en_cours"
    }
    
    try:
        # Importer et créer l'Agent 03 Upgraded
        print(f"\n🔧 DÉMARRAGE AGENT 03 UPGRADED...")
        
        from agent_MAINTENANCE_03_adaptateur_code import create_adaptateur_code_upgraded
        
        # Créer et configurer l'agent
        agent_03 = create_adaptateur_code_upgraded()
        
        print(f"   🆔 Agent ID: {agent_03.agent_id}")
        
        # Démarrer l'agent
        asyncio.run(agent_03.startup())
        
        # Lancer la transformation basée sur le rapport d'audit
        print(f"   🔄 Lancement transformation basée sur rapport d'audit...")
        
        transformation_results = asyncio.run(
            agent_03.transform_from_audit_report(
                str(latest_audit_report),
                str(target_dir)
            )
        )
        
        mission_results["transformation_results"] = transformation_results
        
        # Afficher résultats
        print(f"   📊 RÉSULTATS TRANSFORMATION:")
        
        summary = transformation_results.get('summary', {})
        print(f"      📂 Agents traités: {summary.get('agents_processed', 0)}")
        print(f"      ✅ Agents transformés: {summary.get('agents_transformed', 0)}")
        print(f"      📈 Taux de succès: {summary.get('success_rate', 0):.1f}%")
        
        # Afficher détails des transformations
        agents_processed = transformation_results.get('agents_processed', [])
        
        print(f"\n   📋 DÉTAIL TRANSFORMATIONS:")
        transformations_success = 0
        transformations_failed = 0
        
        for agent_transform in agents_processed:
            agent_file = agent_transform.get('agent_file', 'Unknown')
            final_status = agent_transform.get('final_status', 'unknown')
            original_status = agent_transform.get('original_status', 'unknown')
            
            if final_status == "transformed":
                print(f"      ✅ {agent_file}: {original_status} → transformé")
                transformations_success += 1
            elif final_status == "failed":
                print(f"      ❌ {agent_file}: {original_status} → échec")
                transformations_failed += 1
            elif final_status == "error":
                error = agent_transform.get('error', 'Erreur inconnue')
                print(f"      💥 {agent_file}: {original_status} → erreur ({error[:50]}...)")
                transformations_failed += 1
            else:
                print(f"      ⚠️  {agent_file}: {original_status} → {final_status}")
        
        # Afficher erreurs rencontrées
        errors_encountered = transformation_results.get('errors_encountered', [])
        if errors_encountered:
            print(f"\n   🚨 ERREURS RENCONTRÉES ({len(errors_encountered)}):")
            for error in errors_encountered[:3]:  # Afficher max 3 erreurs
                agent = error.get('agent', 'Unknown')
                error_msg = error.get('error', 'Erreur inconnue')
                print(f"      • {agent}: {error_msg[:60]}...")
            if len(errors_encountered) > 3:
                print(f"      ... et {len(errors_encountered) - 3} autres erreurs")
        
        # Arrêter l'agent proprement
        asyncio.run(agent_03.shutdown())
        print(f"   ✅ Agent 03 Upgraded terminé et arrêté proprement")
        
        # Résumé final
        mission_results.update({
            "status": "complete",
            "timestamp_fin": datetime.now().isoformat(),
            "summary": {
                "total_agents_found": summary.get('total_agents', 0),
                "agents_processed": summary.get('agents_processed', 0),
                "agents_transformed": summary.get('agents_transformed', 0),
                "transformations_success": transformations_success,
                "transformations_failed": transformations_failed,
                "success_rate": summary.get('success_rate', 0)
            }
        })
        
        # Sauvegarder résultats mission
        mission_file = reports_dir / f"mission_transformation_results_{int(time.time())}.json"
        with open(mission_file, 'w', encoding='utf-8') as f:
            json.dump(mission_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n" + "=" * 70)
        print(f"✅ TRANSFORMATION PATTERN FACTORY TERMINÉE!")
        print(f"📊 RÉSUMÉ FINAL:")
        print(f"   🔍 Agents trouvés: {summary.get('total_agents', 0)}")
        print(f"   🔧 Agents traités: {summary.get('agents_processed', 0)}")
        print(f"   ✅ Transformations réussies: {transformations_success}")
        print(f"   ❌ Transformations échouées: {transformations_failed}")
        print(f"   📈 Taux de succès: {summary.get('success_rate', 0):.1f}%")
        print(f"📁 Rapports sauvegardés dans: {reports_dir}")
        print(f"📋 Résultats mission: {mission_file}")
        
        if summary.get('success_rate', 0) >= 80:
            print(f"🎉 EXCELLENT! Taux de succès élevé!")
        elif summary.get('success_rate', 0) >= 60:
            print(f"👍 BON! Taux de succès acceptable")
        else:
            print(f"⚠️  Taux de succès faible - Révision recommandée")
        
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n⚠️ Transformation interrompue par l'utilisateur")
        mission_results["status"] = "interrupted"
    except Exception as e:
        print(f"\n❌ Erreur lors de la transformation: {e}")
        mission_results["status"] = "error"
        mission_results["error"] = str(e)
        
        # Tenter de sauvegarder les résultats partiels
        try:
            mission_file = reports_dir / f"mission_transformation_error_{int(time.time())}.json"
            with open(mission_file, 'w', encoding='utf-8') as f:
                json.dump(mission_results, f, indent=2, ensure_ascii=False)
            print(f"📋 Résultats partiels sauvegardés: {mission_file}")
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main() 



