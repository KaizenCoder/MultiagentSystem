#!/usr/bin/env python3
"""
🚀 LANCEUR DIRECT MISSION ANALYSE FACTORY AGENTS
===============================================

Script de lancement direct qui évite les problèmes d'imports relatifs
en lançant chaque agent individuellement.

Author: Coordinateur Projet
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
    """Lancer la mission d'analyse directement"""
    
    print("🚀 LANCEMENT DIRECT MISSION ANALYSE FACTORY AGENTS")
    print("=" * 60)
    
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
    
    # Créer le répertoire de rapports si nécessaire
    reviews_dir = target_dir / "reviews"
    reviews_dir.mkdir(exist_ok=True)
    print(f"✅ Répertoire rapports: {reviews_dir.resolve()}")
    
    # Ajouter le répertoire des agents au PATH
    sys.path.insert(0, str(current_dir / "agent_equipe_maintenance"))
    
    print(f"\n📋 MISSION DIRECTE:")
    print(f"   • Analyser TOUS les agents du répertoire agent_factory_implementation/agents")
    print(f"   • AUCUNE MODIFICATION des agents - DIAGNOSTIC UNIQUEMENT")
    print(f"   • Placer les rapports dans agent_factory_implementation/agents/reviews")
    
    print(f"\n⚡ LANCEMENT AGENTS INDIVIDUELS...")
    
    mission_results = {
        "mission_id": f"analyse_factory_direct_{int(time.time())}",
        "timestamp_debut": datetime.now().isoformat(),
        "target_directory": str(target_dir.resolve()),
        "reports_directory": str(reviews_dir.resolve()),
        "agents_executed": [],
        "results": {},
        "status": "en_cours"
    }
    
    try:
        # Agent 04 - Testeur Anti-Faux-Agents (avec nouvelles fonctionnalités)
        print(f"\n🧪 LANCEMENT AGENT 04 - TESTEUR ANTI-FAUX-AGENTS...")
        
        from agent_MAINTENANCE_04_testeur_anti_faux_agents import ImprovedEnterpriseAgentTester
        
        # Créer et configurer l'agent 04
        agent_04 = ImprovedEnterpriseAgentTester()
        
        print(f"   🆔 Agent ID: {agent_04.agent_id}")
        print(f"   🎯 Agents à tester: {len(agent_04.agents_to_test) if hasattr(agent_04, 'agents_to_test') else 'N/A'}")
        
        # Démarrer l'agent
        asyncio.run(agent_04.startup())
        
        # Lancer l'audit Pattern Factory sur le répertoire cible
        print(f"   🔍 Lancement audit Pattern Factory...")
        audit_results = agent_04.run_pattern_factory_audit(str(target_dir))
        
        mission_results["agents_executed"].append("agent_04_testeur_anti_faux")
        mission_results["results"]["agent_04"] = {
            "agent_id": agent_04.agent_id,
            "audit_results": audit_results,
            "status": "complete",
            "timestamp": datetime.now().isoformat()
        }
        
        # Afficher résultats
        print(f"   📊 RÉSULTATS AGENT 04:")
        print(f"      📂 Répertoire scanné: {audit_results.get('directory_scanned', 'N/A')}")
        print(f"      🔍 Agents trouvés: {audit_results.get('agents_found', 0)}")
        print(f"      ✅ Agents analysés: {audit_results.get('agents_analyzed', 0)}")
        
        summary = audit_results.get('conformity_summary', {})
        print(f"      📋 CONFORMITÉ:")
        print(f"         ✅ Conformes: {summary.get('compliant', 0)}")
        print(f"         ⚠️  Partiellement conformes: {summary.get('partially_compliant', 0)}")
        print(f"         ❌ Non-conformes: {summary.get('non_compliant', 0)}")
        print(f"         🚨 Erreurs critiques: {summary.get('critical_errors', 0)}")
        
        # Afficher problèmes critiques
        critical_issues = audit_results.get('critical_issues', [])
        if critical_issues:
            print(f"      🚨 PROBLÈMES CRITIQUES:")
            for issue in critical_issues[:3]:  # Afficher max 3 problèmes
                print(f"         • {issue}")
            if len(critical_issues) > 3:
                print(f"         ... et {len(critical_issues) - 3} autres problèmes")
        
        # Afficher recommandations
        recommendations = audit_results.get('recommendations', [])
        if recommendations:
            print(f"      💡 RECOMMANDATIONS:")
            for rec in recommendations[:2]:  # Afficher max 2 recommandations
                print(f"         • {rec}")
        
        # Arrêter l'agent proprement
        asyncio.run(agent_04.shutdown())
        print(f"   ✅ Agent 04 terminé et arrêté proprement")
        
        # Résumé final
        mission_results.update({
            "status": "complete",
            "timestamp_fin": datetime.now().isoformat(),
            "summary": {
                "total_agents_found": audit_results.get('agents_found', 0),
                "total_agents_analyzed": audit_results.get('agents_analyzed', 0),
                "conformity_summary": summary,
                "critical_issues_count": len(critical_issues),
                "recommendations_count": len(recommendations)
            }
        })
        
        # Sauvegarder résultats mission
        mission_file = reviews_dir / f"mission_directe_results_{int(time.time())}.json"
        with open(mission_file, 'w', encoding='utf-8') as f:
            json.dump(mission_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n" + "=" * 60)
        print(f"✅ MISSION DIRECTE TERMINÉE AVEC SUCCÈS!")
        print(f"📊 RÉSUMÉ:")
        print(f"   🔍 Agents trouvés: {audit_results.get('agents_found', 0)}")
        print(f"   ✅ Agents analysés: {audit_results.get('agents_analyzed', 0)}")
        print(f"   📋 Conformité: {summary.get('compliant', 0)} conformes / {audit_results.get('agents_analyzed', 0)} total")
        print(f"   🚨 Problèmes critiques: {len(critical_issues)}")
        print(f"📁 Rapports sauvegardés dans: {reviews_dir}")
        print(f"📋 Résultats mission: {mission_file}")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⚠️ Mission interrompue par l'utilisateur")
        mission_results["status"] = "interrupted"
    except Exception as e:
        print(f"\n❌ Erreur lors de la mission: {e}")
        mission_results["status"] = "error"
        mission_results["error"] = str(e)
        sys.exit(1)

if __name__ == "__main__":
    main() 