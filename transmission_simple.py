#!/usr/bin/env python3
"""
🎖️ TRANSMISSION DIRECTE - CHEF D'ÉQUIPE DE MAINTENANCE
=====================================================

🎯 Version simplifiée pour transmission rapide de mission
📂 Cible: agent_factory_experts_team
⚡ Exécution directe sans blocage

Author: Assistant IA - Version simplifiée
Created: 2025-01-21
"""

import sys
import json
from pathlib import Path
from datetime import datetime

def main():
    print("🎖️ TRANSMISSION MISSION CHEF D'ÉQUIPE - VERSION SIMPLIFIÉE")
    print("="*60)
    
    # Chemins
    projet_root = Path.cwd()
    agents_cibles = projet_root / "agent_factory_experts_team"
    equipe_maintenance = projet_root / "20250620_transformation_equipe_maintenance" / "agent_equipe_maintenance"
    
    print(f"📂 Projet: {projet_root}")
    print(f"🎯 Cibles: {agents_cibles}")
    print(f"🎖️ Équipe: {equipe_maintenance}")
    
    # Vérifications rapides
    if not agents_cibles.exists():
        print("❌ Répertoire agent_factory_experts_team introuvable")
        return False
        
    if not equipe_maintenance.exists():
        print("❌ Équipe de maintenance introuvable")
        return False
    
    # Inventaire des agents experts
    agents_experts = []
    for fichier in agents_cibles.iterdir():
        if fichier.is_file() and fichier.name.endswith('.py'):
            if any(mot in fichier.name.lower() for mot in ['expert', 'coordinateur']):
                agents_experts.append(fichier.name)
    
    print(f"\n✅ {len(agents_experts)} agents experts trouvés:")
    for i, agent in enumerate(agents_experts, 1):
        print(f"   {i:02d}. {agent}")
    
    # Création de la mission simplifiée
    mission = {
        "timestamp": datetime.now().isoformat(),
        "type": "maintenance_agents_experts",
        "cible": str(agents_cibles),
        "agents": agents_experts,
        "status": "READY_FOR_TRANSMISSION"
    }
    
    # Sauvegarde
    mission_file = f"mission_experts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(mission_file, 'w', encoding='utf-8') as f:
        json.dump(mission, f, indent=2, ensure_ascii=False)
    
    print(f"\n📋 Mission créée: {mission_file}")
    
    # Instructions pour le chef d'équipe
    print(f"\n🎖️ INSTRUCTIONS POUR LE CHEF D'ÉQUIPE:")
    print(f"   1. Charger la configuration cible: {agents_cibles}")
    print(f"   2. Exécuter les workflows de maintenance sur {len(agents_experts)} agents")
    print(f"   3. Générer le rapport final")
    
    # Script de commande direct
    script_commande = f"""
# COMMANDE DIRECTE POUR LE CHEF D'ÉQUIPE
# Exécuter dans le répertoire: {equipe_maintenance}

import sys
sys.path.append(r"{equipe_maintenance}")

from agent_MAINTENANCE_00_chef_equipe_coordinateur import ChefEquipeCoordinateur

# Configuration pour agents experts
config = {{
    "target_path": r"{agents_cibles}",
    "workspace_path": r"{projet_root}",
    "safe_mode": True,
    "rapport_detaille": True
}}

# Lancement
chef = ChefEquipeCoordinateur(**config)
resultats = chef.execute_task()
print("Maintenance terminée:", resultats)
"""
    
    script_file = f"commande_chef_equipe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_commande)
    
    print(f"\n🚀 Script de commande généré: {script_file}")
    print(f"\n✅ TRANSMISSION PRÊTE - Le chef d'équipe peut maintenant agir")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n🎊 TRANSMISSION RÉUSSIE!")
        else:
            print(f"\n❌ ÉCHEC DE LA TRANSMISSION")
    except Exception as e:
        print(f"\n💥 Erreur: {e}")




