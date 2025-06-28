#!/usr/bin/env python3
"""
📋 TRANSMISSION DE MISSION - CHEF D'ÉQUIPE DE MAINTENANCE
=========================================================

🎯 Mission : Transmission explicite au Chef d'Équipe de Maintenance pour prise en charge
         des agents du répertoire 'agent_factory_experts_team'

📊 Contexte : Suite à l'analyse complète du projet TaskMaster NextGeneration,
           l'équipe de maintenance transformée doit maintenant prendre en charge
           les agents experts pour tests, maintenance et orchestration.

🚀 Action : Lancement du workflow de maintenance automatisé sur les agents cibles

Author: Assistant IA - Analyse & Transmission
Created: 2025-01-21
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
import sys

# Configuration des chemins
PROJET_ROOT = Path(__file__).parent
EQUIPE_MAINTENANCE_PATH = PROJET_ROOT / "20250620_transformation_equipe_maintenance" / "agent_equipe_maintenance"
AGENTS_CIBLES_PATH = PROJET_ROOT / "agent_factory_experts_team"

# Import du chef d'équipe
sys.path.insert(0, str(EQUIPE_MAINTENANCE_PATH))

async def transmettre_mission_chef_equipe():
    """
    🎖️ Transmission de mission au Chef d'Équipe de Maintenance
    """
    print("="*80)
    print("🎖️ TRANSMISSION DE MISSION - CHEF D'ÉQUIPE DE MAINTENANCE")
    print("="*80)
    
    # 1. Analyse du répertoire cible
    print(f"\n📂 Analyse du répertoire cible: {AGENTS_CIBLES_PATH}")
    
    if not AGENTS_CIBLES_PATH.exists():
        print(f"❌ ERREUR: Répertoire cible introuvable: {AGENTS_CIBLES_PATH}")
        return
    
    # Inventaire des agents experts
    agents_experts = []
    for fichier in AGENTS_CIBLES_PATH.iterdir():
        if fichier.is_file() and fichier.name.endswith('.py') and 'expert' in fichier.name:
            agents_experts.append(fichier.name)
    
    print(f"✅ {len(agents_experts)} agents experts identifiés:")
    for i, agent in enumerate(agents_experts, 1):
        print(f"   {i:02d}. {agent}")
    
    # 2. Préparation des données de mission
    mission_data = {
        "timestamp": datetime.now().isoformat(),
        "mission_type": "maintenance_agents_experts",
        "target_directory": str(AGENTS_CIBLES_PATH),
        "agents_a_traiter": agents_experts,
        "workflows_requis": [
            "analyser_equipe_complete",
            "evaluer_utilite_equipe", 
            "adapter_code_agents",
            "tester_integration",
            "documenter_equipe",
            "validation_finale"
        ],
        "priorite": "HAUTE",
        "objectifs": [
            "Vérifier la conformité au Pattern Factory",
            "Tester l'intégration et la performance",
            "Mettre à jour la documentation si nécessaire",
            "Valider la robustesse des agents experts",
            "Générer un rapport de maintenance complet"
        ]
    }
    
    # 3. Sauvegarde de la mission
    mission_file = PROJET_ROOT / f"mission_maintenance_experts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(mission_file, 'w', encoding='utf-8') as f:
        json.dump(mission_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📋 Mission sauvegardée: {mission_file.name}")
    
    # 4. Import et lancement du chef d'équipe
    print(f"\n🎖️ Chargement du Chef d'Équipe de Maintenance...")
    
    try:
        from agent_MAINTENANCE_00_chef_equipe_coordinateur import ChefEquipeCoordinateur
        
        # Configuration spécialisée pour les agents experts
        config_chef = {
            "target_path": str(AGENTS_CIBLES_PATH),
            "workspace_path": str(PROJET_ROOT),
            "safe_mode": True,
            "rapport_detaille": True,
            "max_agents_parallel": 4,  # Limitation pour stabilité
            "timeout": 600  # 10 minutes par workflow
        }
        
        print("✅ Chef d'Équipe chargé avec succès")
        print(f"🎯 Configuration:")
        print(f"   - Cible: {config_chef['target_path']}")
        print(f"   - Mode sécurisé: {config_chef['safe_mode']}")
        print(f"   - Agents parallèles max: {config_chef['max_agents_parallel']}")
        
        # Initialisation du chef
        chef_equipe = ChefEquipeCoordinateur(**config_chef)
        await chef_equipe.startup()
        
        print(f"\n🚀 LANCEMENT DE LA MISSION DE MAINTENANCE")
        print(f"📊 Agents experts à traiter: {len(agents_experts)}")
        print(f"⏱️  Début: {datetime.now().strftime('%H:%M:%S')}")
        
        # Lancement du workflow complet
        resultats = await chef_equipe.workflow_maintenance_complete()
        
        print(f"\n✅ MISSION TERMINÉE")
        print(f"⏱️  Fin: {datetime.now().strftime('%H:%M:%S')}")
        print(f"📊 Statut: {resultats.get('status', 'INCONNU')}")
        
        # Sauvegarde des résultats
        resultats_file = PROJET_ROOT / f"resultats_maintenance_experts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(resultats_file, 'w', encoding='utf-8') as f:
            json.dump(resultats, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Résultats sauvegardés: {resultats_file.name}")
        
        # Arrêt propre
        await chef_equipe.shutdown()
        
        return {
            "status": "SUCCESS",
            "mission_file": str(mission_file),
            "resultats_file": str(resultats_file),
            "agents_traites": len(agents_experts),
            "resultats": resultats
        }
        
    except ImportError as e:
        print(f"❌ ERREUR: Impossible de charger le Chef d'Équipe: {e}")
        print(f"💡 Vérifiez que le fichier agent_MAINTENANCE_00_chef_equipe_coordinateur.py existe")
        return {"status": "ERROR", "error": str(e)}
        
    except Exception as e:
        print(f"❌ ERREUR lors de l'exécution: {e}")
        return {"status": "ERROR", "error": str(e)}

async def main():
    """Point d'entrée principal"""
    print("🎯 TaskMaster NextGeneration - Transmission Mission Chef d'Équipe")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        resultats = await transmettre_mission_chef_equipe()
        
        if resultats["status"] == "SUCCESS":
            print(f"\n🎊 TRANSMISSION RÉUSSIE!")
            print(f"✅ {resultats['agents_traites']} agents experts traités")
            print(f"📋 Fichiers générés:")
            print(f"   - Mission: {Path(resultats['mission_file']).name}")
            print(f"   - Résultats: {Path(resultats['resultats_file']).name}")
        else:
            print(f"\n❌ ÉCHEC DE LA TRANSMISSION")
            print(f"🔍 Erreur: {resultats.get('error', 'Inconnue')}")
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"\n💥 Erreur critique: {e}")

if __name__ == "__main__":
    asyncio.run(main())
