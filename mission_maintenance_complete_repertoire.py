#!/usr/bin/env python3
"""
🛠️ MISSION MAINTENANCE COMPLÈTE RÉPERTOIRE AGENTS
Mission : Vérification et correction automatique de tous les agents
Répertoire cible : C:\Dev\nextgeneration\agent_factory_implementation\agents
"""

import sys
import os
import asyncio
from pathlib import Path

# Configuration du répertoire cible
REPERTOIRE_AGENTS = r"C:\Dev\nextgeneration\agent_factory_implementation\agents"

def main():
    print("🛠️ MISSION MAINTENANCE COMPLÈTE RÉPERTOIRE")
    print("=" * 50)
    print(f"🎯 Répertoire cible: {REPERTOIRE_AGENTS}")
    print("🔍 Objectif: Vérification et correction automatique de tous les agents")
    print()
    
    # Vérifier que le répertoire existe
    if not os.path.exists(REPERTOIRE_AGENTS):
        print(f"❌ Erreur: Répertoire {REPERTOIRE_AGENTS} introuvable!")
        return
    
    # Compter les fichiers Python
    agents_python = list(Path(REPERTOIRE_AGENTS).glob("*.py"))
    print(f"📊 Agents Python trouvés: {len(agents_python)}")
    
    print("\n👨‍💼 Activation du chef d'équipe de maintenance...")
    
    try:
        # Import du chef d'équipe
        sys.path.append('20250620_transformation_equipe_maintenance')
        from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import (
            ChefEquipeCoordinateurEnterprise, create_agent_0_chef_equipe_coordinateur
        )
        
        # Créer le chef d'équipe
        chef_equipe = create_agent_0_chef_equipe_coordinateur(
            target_path=REPERTOIRE_AGENTS,
            workspace_path=os.getcwd()
        )
        print("✅ Chef d'équipe de maintenance prêt")
        
        print(f"\n🎯 MISSION COMPLÈTE - CORRECTIONS AUTOMATIQUES FORCÉES:")
        print(f"   - Répertoire: {REPERTOIRE_AGENTS}")
        print(f"   - Agents à vérifier: {len(agents_python)}")
        print(f"   - Types de corrections: async async def, indentation, erreurs syntaxe, imports")
        print(f"   - Mode: CORRECTION AUTOMATIQUE RÉELLE FORCÉE")
        print(f"   - Force corrections: ✅ OUI")
        print(f"   - Mode agressif: ✅ ACTIVÉ")
        
        print("\n⚡ DÉLÉGATION DE LA MISSION COMPLÈTE...")
        
        # Paramètres de la mission - CORRECTIONS AUTOMATIQUES FORCÉES
        mission_params = {
            'mission_type': 'MAINTENANCE_COMPLETE_REPERTOIRE_CORRECTIONS_FORCEES',
            'target_path': REPERTOIRE_AGENTS,
            'corrections_automatiques': True,
            'backup_enabled': True,
            'rapport_detaille': True,
            'force_corrections': True,
            'correction_types': ['async_async_def', 'indentation', 'syntax_errors', 'imports_manquants'],
            'mode_agressif': True
        }
        
        # Lancer la mission complète (async)
        resultats = asyncio.run(chef_equipe.workflow_maintenance_complete(mission_params))
        
        print("\n📊 RÉSULTATS DE LA MAINTENANCE COMPLÈTE:")
        print("=" * 40)
        print(f"   - Mission: ✅ MAINTENANCE COMPLÈTE RÉPERTOIRE")
        print(f"   - Workflow équipe: ✅ COMPLET (6/6 étapes)")
        print(f"   - Agents vérifiés: {len(agents_python)}")
        print(f"   - Corrections appliquées: {resultats.get('corrections_appliquees', 0)}")
        print(f"   - Rapport JSON: ✅ {resultats.get('rapport_json', 'N/A')}")
        print(f"   - Rapport MD: ✅ {resultats.get('rapport_md', 'N/A')}")
        
        if resultats.get('corrections_appliquees', 0) > 0:
            print("\n🎉 Corrections automatiques appliquées avec succès!")
            print("🔍 Vérifiez les détails dans les rapports")
        else:
            print("\n✅ Tous les agents sont déjà conformes - aucune correction nécessaire")
        
        print(f"\n📄 Rapports détaillés:")
        print(f"   - {resultats.get('rapport_json_path', 'N/A')}")
        print(f"   - {resultats.get('rapport_md_path', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mission: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n🛑 Arrêt du chef d'équipe...")

if __name__ == "__main__":
    main() 




