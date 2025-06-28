#!/usr/bin/env python3
"""
📋 INSTRUCTIONS POUR LE CHEF D'ÉQUIPE MAINTENANCE
==============================================

Instructions détaillées pour l'analyse du répertoire agent_factory_implementation/agents
par l'équipe de maintenance complète.

Author: Coordinateur Projet
Version: 1.0.0
Created: 2025-01-20
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire des agents au PATH
sys.path.insert(0, str(Path(__file__).parent / "agent_equipe_maintenance"))

from agent_MAINTENANCE_00_chef_equipe_coordinateur import ChefEquipeCoordinateurEnterprise

async def donner_instructions_chef_equipe():
    """Donner les instructions complètes au chef d'équipe maintenance"""
    
    print("📋 TRANSMISSION D'INSTRUCTIONS AU CHEF D'ÉQUIPE MAINTENANCE")
    print("=" * 70)
    
    # Configuration pour le chef d'équipe
    config_mission = {
        "target_path": "../agent_factory_implementation/agents",
        "workspace_path": ".",
        "safe_mode": True,  # IMPORTANT: Pas de modification des agents
        "rapport_detaille": True,
        "timeout": 600,  # 10 minutes par agent
        "max_agents_parallel": 4
    }
    
    # Créer le chef d'équipe
    chef_equipe = ChefEquipeCoordinateurEnterprise(**config_mission)
    
    print(f"\n🎖️ Chef d'équipe créé: {chef_equipe.agent_id}")
    print(f"📂 Répertoire cible: {config_mission['target_path']}")
    print(f"🔒 Mode sécurisé: {config_mission['safe_mode']} (pas de modification)")
    
    # Instructions détaillées pour le chef d'équipe
    instructions = {
        "mission_principale": {
            "objectif": "Analyser TOUS les agents du répertoire agent_factory_implementation/agents",
            "contrainte_critique": "AUCUNE MODIFICATION des agents - DIAGNOSTIC UNIQUEMENT",
            "destination_rapports": "agent_factory_implementation/agents/reviews",
            "type_analyse": "Conformité Pattern Factory et qualité du code"
        },
        
        "taches_equipe": {
            "agent_01_analyseur": {
                "mission": "Analyser la structure de chaque agent",
                "focus": [
                    "Imports Pattern Factory",
                    "Héritage classe Agent", 
                    "Méthodes obligatoires (startup, shutdown, health_check, execute_task)",
                    "Architecture générale",
                    "Erreurs syntaxe Python"
                ]
            },
            
            "agent_02_evaluateur": {
                "mission": "Évaluer l'utilité et la conformité",
                "focus": [
                    "Score de conformité Pattern Factory",
                    "Qualité du code",
                    "Respect des bonnes pratiques",
                    "Fonctionnalités implémentées",
                    "Niveau de maturité"
                ]
            },
            
            "agent_03_adaptateur": {
                "mission": "Analyser les besoins d'adaptation (SANS MODIFIER)",
                "focus": [
                    "Recommandations de migration",
                    "Problèmes identifiés",
                    "Solutions proposées",
                    "Priorités de correction",
                    "Effort estimé"
                ]
            },
            
            "agent_04_testeur": {
                "mission": "Tester et valider (nouvelles fonctionnalités Pattern Factory)",
                "focus": [
                    "Détection faux agents",
                    "Problèmes de conformité",
                    "Erreurs critiques",
                    "Tests de fonctionnement",
                    "Rapport de validation"
                ]
            },
            
            "agent_05_documenteur": {
                "mission": "Documenter les analyses et résultats",
                "focus": [
                    "Documentation des agents analysés",
                    "Guides d'utilisation",
                    "Schémas d'architecture",
                    "Documentation consolidée",
                    "Index de documentation"
                ]
            },
            
            "agent_06_validateur_final": {
                "mission": "Validation finale de la mission d'analyse",
                "focus": [
                    "Validation globale des résultats",
                    "Contrôle qualité des rapports",
                    "Tests d'intégrité",
                    "Évaluation mission globale",
                    "Certification finale"
                ]
            }
        },
        
        "deliverables": {
            "repertoire_sortie": "agent_factory_implementation/agents/reviews",
            "format_rapports": "JSON et Markdown",
            "nomenclature": "agent_[nom]_analysis_[timestamp]",
            "consolidation": "rapport_global_equipe_maintenance_[timestamp]"
        },
        
        "contraintes_operationnelles": {
            "mode_lecture_seule": True,
            "pas_de_modification_code": True,
            "sauvegarde_automatique": True,
            "logs_detailles": True,
            "gestion_erreurs": "Continue même en cas d'erreur sur un agent"
        }
    }
    
    print("\n📋 INSTRUCTIONS DÉTAILLÉES TRANSMISES:")
    print("=" * 50)
    
    print(f"\n🎯 MISSION PRINCIPALE:")
    print(f"   • Objectif: {instructions['mission_principale']['objectif']}")
    print(f"   • Contrainte: {instructions['mission_principale']['contrainte_critique']}")
    print(f"   • Destination: {instructions['mission_principale']['destination_rapports']}")
    
    print(f"\n👥 RÉPARTITION ÉQUIPE:")
    for agent_nom, agent_config in instructions['taches_equipe'].items():
        print(f"   📋 {agent_nom}:")
        print(f"      Mission: {agent_config['mission']}")
        print(f"      Focus: {len(agent_config['focus'])} points d'analyse")
    
    print(f"\n📊 LIVRABLES ATTENDUS:")
    print(f"   • Répertoire: {instructions['deliverables']['repertoire_sortie']}")
    print(f"   • Format: {instructions['deliverables']['format_rapports']}")
    print(f"   • Consolidation: Rapport global de l'équipe")
    
    print(f"\n🔒 CONTRAINTES:")
    print(f"   • Mode lecture seule: {instructions['contraintes_operationnelles']['mode_lecture_seule']}")
    print(f"   • Pas de modification: {instructions['contraintes_operationnelles']['pas_de_modification_code']}")
    
    # Démarrer le chef d'équipe
    print(f"\n🚀 DÉMARRAGE DU CHEF D'ÉQUIPE...")
    await chef_equipe.startup()
    
    # Vérifier l'état de santé
    health = await chef_equipe.health_check()
    print(f"🏥 État santé: {health['status']}")
    
    # Créer une tâche personnalisée pour cette mission
    mission_task = {
        "task_id": "analyse_factory_agents_diagnostic_only",
        "description": "Analyse complète agents factory - DIAGNOSTIC UNIQUEMENT",
        "instructions": instructions,
        "config": config_mission
    }
    
    print(f"\n⚡ LANCEMENT DE LA MISSION...")
    print("   Le chef d'équipe va maintenant coordonner son équipe")
    print("   pour analyser tous les agents du répertoire factory.")
    print("   Rapports disponibles dans: agent_factory_implementation/agents/reviews")
    
    try:
        # Exécuter la mission
        resultats = await chef_equipe.execute_task(mission_task)
        
        print(f"\n✅ MISSION TERMINÉE!")
        print(f"📊 Résultats: {resultats.get('status', 'Inconnu')}")
        
        if resultats.get('success'):
            print(f"🎯 Agents analysés: {resultats.get('agents_analyses', 'N/A')}")
            print(f"📋 Rapports générés: {resultats.get('rapports_generes', 'N/A')}")
        else:
            print(f"⚠️ Problème rencontré: {resultats.get('error', 'Erreur inconnue')}")
    
    except Exception as e:
        print(f"❌ Erreur durant la mission: {e}")
    
    finally:
        # Arrêt propre du chef d'équipe
        await chef_equipe.shutdown()
        print(f"\n🛑 Chef d'équipe arrêté proprement")
    
    print(f"\n" + "=" * 70)
    print("📋 INSTRUCTIONS TRANSMISES ET MISSION LANCÉE")
    print("🔍 Consultez agent_factory_implementation/agents/reviews pour les résultats")
    print("=" * 70)

def main():
    """Point d'entrée principal"""
    try:
        asyncio.run(donner_instructions_chef_equipe())
    except KeyboardInterrupt:
        print("\n⚠️ Mission interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors de la transmission des instructions: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 



