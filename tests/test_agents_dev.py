#!/usr/bin/env python3
"""
🧪 SCRIPT DE TEST SPÉCIALISÉ POUR AGENTS C:\Dev\agents
Test avec l'Agent Testeur d'Agents sur les agents spécifiques
"""

import asyncio
import json
from pathlib import Path
from agent_testeur_agents import create_agent_testeur_agents

async def main():
    """Test des agents dans C:\Dev\agents"""
    print("🧪 TEST AGENTS C:\\Dev\\agents - PATTERN FACTORY NEXTGENERATION")
    print("=" * 80)
    
    # Répertoire des agents à tester
    agents_dir = Path(r"C:\Dev\agents")
    
    if not agents_dir.exists():
        print("❌ Répertoire C:\\Dev\\agents non trouvé")
        return
    
    # Créer l'agent testeur
    agent_testeur = create_agent_testeur_agents(
        safe_mode=True, 
        test_timeout=30,
        max_concurrent_tests=5
    )
    
    try:
        # Démarrage
        await agent_testeur.startup()
        
        # Vérification santé du testeur
        health = await agent_testeur.health_check()
        print(f"🏥 Agent Testeur: {health['status']}")
        print(f"🔒 Mode sécurisé: {health['safe_mode']}")
        print(f"⏱️ Timeout: {health['test_timeout']}s")
        print()
        
        # Lister les agents Python dans le répertoire
        agent_files = list(agents_dir.glob("agent_*.py"))
        
        if not agent_files:
            print("❌ Aucun agent Python trouvé dans C:\\Dev\\agents")
            return
        
        print(f"📁 Agents trouvés: {len(agent_files)}")
        for agent_file in agent_files:
            print(f"   - {agent_file.name}")
        print()
        
        # Test de chaque agent individuellement
        resultats_detailles = {}
        
        for i, agent_file in enumerate(agent_files, 1):
            print(f"🧪 [{i}/{len(agent_files)}] Test: {agent_file.name}")
            print("-" * 60)
            
            # Test complet de l'agent
            resultat = await agent_testeur.tester_agent(str(agent_file))
            resultats_detailles[agent_file.name] = resultat
            
            # Affichage résumé
            if "tests" in resultat:
                tests = resultat["tests"]
                
                # Test syntaxe
                syntax = tests.get("syntax", {})
                status_syntax = "✅" if syntax.get("success") else "❌"
                print(f"  {status_syntax} Syntaxe: {syntax.get('message', 'N/A')}")
                
                # Test Pattern Factory
                pf = tests.get("pattern_factory", {})
                if pf:
                    level = pf.get("conformite_level", "ERREUR")
                    score = pf.get("score_global", 0)
                    
                    if level == "CONFORME_EXCELLENT":
                        status_pf = "🟢"
                    elif level == "CONFORME_STRICT":
                        status_pf = "🟡"
                    elif level == "CONFORME_PARTIEL":
                        status_pf = "🟠"
                    else:
                        status_pf = "🔴"
                    
                    print(f"  {status_pf} Pattern Factory: {level} ({score}%)")
                    
                    # Afficher recommandations critiques
                    recommendations = pf.get("recommendations", [])
                    critiques = [r for r in recommendations if r.startswith("CRITIQUE")]
                    if critiques:
                        print("      ⚠️ Points critiques:")
                        for critique in critiques[:3]:  # Max 3 pour éviter surcharge
                            print(f"         • {critique}")
                
                # Score global
                score_global = resultat.get("score_global", 0)
                status_global = "✅" if score_global >= 70 else "⚠️" if score_global >= 50 else "❌"
                print(f"  {status_global} Score Global: {score_global}/100")
                
            print()
        
        # Résumé global
        print("=" * 80)
        print("📊 RÉSUMÉ GLOBAL DES TESTS")
        print("=" * 80)
        
        # Statistiques
        total_agents = len(resultats_detailles)
        agents_conformes = 0
        scores = []
        
        conformite_distribution = {
            "CONFORME_EXCELLENT": 0,
            "CONFORME_STRICT": 0, 
            "CONFORME_PARTIEL": 0,
            "NON_CONFORME": 0
        }
        
        for nom_agent, resultat in resultats_detailles.items():
            if "tests" in resultat and "pattern_factory" in resultat["tests"]:
                pf = resultat["tests"]["pattern_factory"]
                level = pf.get("conformite_level", "NON_CONFORME")
                score = pf.get("score_global", 0)
                
                scores.append(score)
                
                if level in ["CONFORME_EXCELLENT", "CONFORME_STRICT"]:
                    agents_conformes += 1
                
                if level in conformite_distribution:
                    conformite_distribution[level] += 1
                else:
                    conformite_distribution["NON_CONFORME"] += 1
        
        # Affichage statistiques
        taux_conformite = (agents_conformes / total_agents * 100) if total_agents > 0 else 0
        score_moyen = sum(scores) / len(scores) if scores else 0
        
        print(f"📈 Agents testés: {total_agents}")
        print(f"✅ Agents conformes: {agents_conformes} ({taux_conformite:.1f}%)")
        print(f"🎯 Score Pattern Factory moyen: {score_moyen:.1f}%")
        print()
        
        print("📊 Distribution conformité:")
        for level, count in conformite_distribution.items():
            pourcentage = (count / total_agents * 100) if total_agents > 0 else 0
            if count > 0:
                if level == "CONFORME_EXCELLENT":
                    emoji = "🟢"
                elif level == "CONFORME_STRICT":
                    emoji = "🟡"
                elif level == "CONFORME_PARTIEL":
                    emoji = "🟠"
                else:
                    emoji = "🔴"
                print(f"  {emoji} {level}: {count} agents ({pourcentage:.1f}%)")
        
        # Recommandations générales
        print()
        print("🎯 RECOMMANDATIONS GÉNÉRALES:")
        
        if taux_conformite >= 80:
            print("  🎉 Excellent! La majorité des agents sont conformes Pattern Factory")
        elif taux_conformite >= 60:
            print("  👍 Bon niveau de conformité, quelques améliorations mineures")
        else:
            print("  ⚠️ Conformité Pattern Factory à améliorer de manière prioritaire")
        
        if score_moyen >= 85:
            print("  ✨ Score Pattern Factory excellent")
        elif score_moyen >= 70:
            print("  👌 Score Pattern Factory satisfaisant")
        else:
            print("  🔧 Score Pattern Factory nécessite des améliorations")
        
        # Sauvegarde rapport détaillé
        rapport_complet = {
            "timestamp": agent_testeur.test_results_cache.get("timestamp", ""),
            "repertoire_teste": str(agents_dir),
            "statistiques": {
                "total_agents": total_agents,
                "agents_conformes": agents_conformes,
                "taux_conformite": taux_conformite,
                "score_moyen": score_moyen,
                "distribution_conformite": conformite_distribution
            },
            "resultats_detailles": resultats_detailles
        }
        
        rapport_file = f"rapport_agents_dev_{agent_testeur.agent_id}.json"
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(rapport_complet, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Rapport détaillé sauvegardé: {rapport_file}")
        
        # Arrêt propre
        await agent_testeur.shutdown()
        
        print("\n🎯 TEST TERMINÉ AVEC SUCCÈS!")
        
    except Exception as e:
        print(f"❌ Erreur durant les tests: {e}")
        await agent_testeur.shutdown()

if __name__ == "__main__":
    asyncio.run(main()) 



