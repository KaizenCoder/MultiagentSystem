#!/usr/bin/env python3
"""
Délégation Correction Agent 3 - WindowsPath Error
Transmission des instructions au chef d'équipe selon le pattern établi
"""

import asyncio
import sys
from pathlib import Path
from agent_0_chef_equipe_coordinateur import Agent0ChefEquipeCoordinateur

async def deleguer_correction_agent_3():
    """Déléguer la correction de l'Agent 3 au chef d'équipe"""
    print("🎖️ DÉLÉGATION CORRECTION AGENT 3")
    print("=== TRANSMISSION INSTRUCTIONS CHEF D'ÉQUIPE ===\n")
    
    # Initialiser le chef d'équipe
    chef = Agent0ChefEquipeCoordinateur()
    await chef.startup()
    
    # Instructions détaillées pour la correction Agent 3
    instructions_correction = {
        "mission": "CORRECTION_AGENT_3_WINDOWSPATH_ERROR",
        "probleme_identifie": "'WindowsPath' object is not iterable",
        "agent_cible": "agent_3_adaptateur_code.py",
        "workflow_etape": "ÉTAPE 3/6: Adaptation Code",
        
        "phases_correction": {
            "phase_diagnostic": {
                "action": "Analyser agent_3_adaptateur_code.py",
                "objectif": "Identifier la ligne causant l'erreur WindowsPath",
                "focus": "Rechercher les boucles for sur des objets Path",
                "agent_responsable": "Agent 1 (Analyseur Structure)"
            },
            
            "phase_correction": {
                "action": "Corriger l'itération WindowsPath",
                "corrections_requises": [
                    "Convertir WindowsPath en liste si nécessaire",
                    "Ajouter vérification isinstance(path, Path)",
                    "Implémenter gestion appropriée des chemins",
                    "Ajouter try/except pour robustesse"
                ],
                "agent_responsable": "Agent 2 (Évaluateur Utilité)"
            },
            
            "phase_validation": {
                "action": "Tester la correction Agent 3",
                "tests_requis": [
                    "Test avec chemins Windows",
                    "Test itération sur Path objects",
                    "Validation workflow ÉTAPE 3/6",
                    "Intégration complète workflow"
                ],
                "agent_responsable": "Équipe complète"
            }
        },
        
        "contraintes": [
            "Maintenir compatibilité TemplateManager existant",
            "Préserver interfaces Agent 3",
            "Respecter pattern Path/WindowsPath",
            "Assurer continuité workflow"
        ],
        
        "livrables_attendus": [
            "Agent 3 corrigé et fonctionnel",
            "Tests de validation réussis",
            "Workflow ÉTAPE 3/6 opérationnelle",
            "Rapport de correction détaillé"
        ]
    }
    
    print("📋 INSTRUCTIONS TRANSMISES AU CHEF D'ÉQUIPE:")
    print(f"🎯 Mission: {instructions_correction['mission']}")
    print(f"🔍 Problème: {instructions_correction['probleme_identifie']}")
    print(f"📁 Agent cible: {instructions_correction['agent_cible']}")
    print(f"⚙️ Étape workflow: {instructions_correction['workflow_etape']}")
    
    print("\n🔄 PHASES DE CORRECTION:")
    for phase, details in instructions_correction['phases_correction'].items():
        print(f"  {phase.upper()}:")
        print(f"    - Action: {details['action']}")
        print(f"    - Responsable: {details['agent_responsable']}")
    
    try:
        # Transmettre les instructions au chef d'équipe
        print("\n🚀 TRANSMISSION AU CHEF D'ÉQUIPE...")
        
        # Exécuter mission spécifique de correction
        result = await chef.executer_mission_specifique(
            mission_type="correction_agent_3",
            instructions=instructions_correction,
            agents_requis=["agent_1", "agent_2"],
            workflow_id=f"correction_agent_3_{chef.agent_id.split('_')[-1]}"
        )
        
        print(f"✅ DÉLÉGATION RÉUSSIE")
        print(f"📊 Workflow ID: {result.get('workflow_id', 'N/A')}")
        print(f"🎯 Status: {result.get('status', 'N/A')}")
        
        if result.get('instructions_manuelles'):
            print(f"\n📋 INSTRUCTIONS MANUELLES DU CHEF D'ÉQUIPE:")
            for instruction in result['instructions_manuelles']:
                print(f"   • {instruction}")
        
        return result
        
    except Exception as e:
        print(f"❌ ERREUR DÉLÉGATION: {e}")
        
        # Instructions manuelles de fallback
        print(f"\n📋 INSTRUCTIONS MANUELLES DE FALLBACK:")
        print(f"Le chef d'équipe doit corriger l'Agent 3 :")
        print(f"1. DIAGNOSTIC: Analyser agent_3_adaptateur_code.py")
        print(f"2. IDENTIFIER: Ligne avec 'WindowsPath' object is not iterable")
        print(f"3. CORRIGER: Convertir Path en liste ou itérable approprié")
        print(f"4. TESTER: Valider ÉTAPE 3/6 du workflow")
        print(f"5. VALIDER: Workflow complet fonctionnel")
        
        return {
            "status": "instructions_manuelles_fournies",
            "mission": instructions_correction['mission'],
            "instructions_fallback": True
        }
    
    finally:
        await chef.shutdown()

if __name__ == "__main__":
    print("🚀 Démarrage délégation correction Agent 3")
    result = asyncio.run(deleguer_correction_agent_3())
    
    if result.get('status') in ['success', 'instructions_manuelles_fournies']:
        print(f"\n🎉 DÉLÉGATION TERMINÉE AVEC SUCCÈS")
        sys.exit(0)
    else:
        print(f"\n❌ DÉLÉGATION ÉCHOUÉE")
        sys.exit(1) 