#!/usr/bin/env python3
"""
🚀 LANCEUR MISSION ANALYSE FACTORY AGENTS
========================================

Script simple pour lancer l'analyse du répertoire agent_factory_implementation/agents
par l'équipe de maintenance.

Author: Coordinateur Projet
Version: 1.0.0
Created: 2025-01-20
"""

import os
import sys
from pathlib import Path

def main():
    """Lancer la mission d'analyse"""
    
    print("🚀 LANCEMENT MISSION ANALYSE FACTORY AGENTS")
    print("=" * 50)
    
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
    
    print(f"\n📋 INSTRUCTIONS POUR LE CHEF D'ÉQUIPE MAINTENANCE:")
    print("=" * 50)
    
    print(f"🎯 MISSION:")
    print(f"   • Analyser TOUS les agents du répertoire agent_factory_implementation/agents")
    print(f"   • AUCUNE MODIFICATION des agents - DIAGNOSTIC UNIQUEMENT")
    print(f"   • Placer les rapports dans agent_factory_implementation/agents/reviews")
    
    print(f"\n👥 ÉQUIPE MOBILISÉE:")
    print(f"   • Agent 01 - Analyseur Structure")
    print(f"   • Agent 02 - Évaluateur Utilité") 
    print(f"   • Agent 03 - Adaptateur Code (analyse seulement)")
    print(f"   • Agent 04 - Testeur Anti-Faux-Agents (nouvelles fonctionnalités)")
    print(f"   • Agent 05 - Documenteur (documentation complète)")
    print(f"   • Agent 06 - Validateur Final (certification mission)")
    
    print(f"\n🔒 CONTRAINTES:")
    print(f"   • Mode lecture seule activé")
    print(f"   • Pas de modification du code source")
    print(f"   • Sauvegarde automatique des rapports")
    
    print(f"\n⚡ LANCEMENT...")
    
    try:
        # Lancer le script d'instructions
        os.system("python instructions_chef_equipe_analyse_factory.py")
        
    except KeyboardInterrupt:
        print("\n⚠️ Mission interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du lancement: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 



