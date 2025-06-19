#!/usr/bin/env python3
"""
🩺 DOCTEUR AGENTS DEV - RÉPARATION SPÉCIALISÉE
Réparation des agents dans C:\Dev\agents avec l'Agent Docteur
"""

import asyncio
import json
from pathlib import Path
from agent_docteur_reparation import create_agent_docteur_reparation

async def main():
    """Réparation spécialisée des agents dans C:\Dev\agents"""
    print("🩺 DOCTEUR AGENTS DEV - RÉPARATION PATTERN FACTORY")
    print("=" * 70)
    
    # Répertoire des agents à réparer
    agents_dir = Path(r"C:\Dev\agents")
    
    if not agents_dir.exists():
        print("❌ Répertoire C:\\Dev\\agents non trouvé")
        return
    
    # Créer l'agent docteur
    docteur = create_agent_docteur_reparation(
        backup_enabled=True,
        repair_mode="aggressive",
        max_agents=10
    )
    
    try:
        # Démarrage
        await docteur.startup()
        
        # Santé
        health = await docteur.health_check()
        print(f"🏥 Agent Docteur: {health['status']}")
        print(f"💾 Backup: {'On' if health.get('backup_enabled', True) else 'Off'}")
        print(f"🔧 Mode: {health.get('repair_mode', 'normal')}")
        print()
        
        # Lister les agents à réparer
        agent_files = list(agents_dir.glob("agent_*.py"))
        
        if not agent_files:
            print("❌ Aucun agent Python trouvé dans C:\\Dev\\agents")
            return
        
        print(f"📁 Agents à réparer: {len(agent_files)}")
        for agent_file in agent_files:
            print(f"   - {agent_file.name}")
        print()
        
        # Réparation de chaque agent
        resultats_reparation = {}
        
        for i, agent_file in enumerate(agent_files, 1):
            print(f"🩺 [{i}/{len(agent_files)}] Réparation: {agent_file.name}")
            print("-" * 50)
            
            # Diagnostic et réparation
            resultat = await docteur.reparer_agent(str(agent_file))
            resultats_reparation[agent_file.name] = resultat
            
            # Affichage résumé
            success = resultat.get("success", False)
            status = "✅" if success else "❌"
            message = resultat.get("message", "N/A")
            
            print(f"  {status} Réparation: {message}")
            
            if success:
                modifications = resultat.get("modifications_applied", [])
                print(f"    📝 Modifications: {len(modifications)}")
                
                for mod in modifications[:3]:  # Max 3 pour lisibilité
                    print(f"      • {mod}")
            
            if "diagnostic" in resultat:
                diagnostic = resultat["diagnostic"]
                problemes = diagnostic.get("problemes_detectes", 0)
                print(f"    🔍 Problèmes détectés: {problemes}")
            
            print()
        
        # Résumé global
        print("=" * 70)
        print("📊 RÉSUMÉ RÉPARATIONS")
        print("=" * 70)
        
        total_agents = len(resultats_reparation)
        reparations_reussies = sum(1 for r in resultats_reparation.values() 
                                  if r.get("success", False))
        
        print(f"📈 Agents traités: {total_agents}")
        print(f"✅ Réparations réussies: {reparations_reussies}")
        print(f"🎯 Taux de succès: {reparations_reussies/total_agents*100:.1f}%")
        
        # Détails des réparations
        for nom_agent, resultat in resultats_reparation.items():
            if resultat.get("success"):
                modifications = len(resultat.get("modifications_applied", []))
                print(f"  ✅ {nom_agent}: {modifications} corrections")
            else:
                error = resultat.get("error", "Erreur inconnue")
                print(f"  ❌ {nom_agent}: {error}")
        
        # Sauvegarde rapport
        rapport = {
            "timestamp": docteur.agent_id,
            "repertoire_traite": str(agents_dir),
            "statistiques": {
                "total_agents": total_agents,
                "reparations_reussies": reparations_reussies,
                "taux_succes": reparations_reussies/total_agents*100
            },
            "resultats_detailles": resultats_reparation
        }
        
        rapport_file = f"rapport_reparations_dev_{docteur.agent_id}.json"
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Rapport réparations: {rapport_file}")
        
        # Arrêt propre
        await docteur.shutdown()
        
        print("\n🎯 RÉPARATIONS TERMINÉES!")
        
    except Exception as e:
        print(f"❌ Erreur durant réparations: {e}")
        await docteur.shutdown()

if __name__ == "__main__":
    asyncio.run(main()) 