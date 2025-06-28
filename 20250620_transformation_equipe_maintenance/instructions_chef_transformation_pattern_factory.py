#!/usr/bin/env python3
"""
🎯 INSTRUCTIONS CHEF D'ÉQUIPE - TRANSFORMATION PATTERN FACTORY
=============================================================

Instructions complètes pour le chef d'équipe maintenance pour :
1. Configurer la mission de transformation
2. Coordonner son équipe avec les bons paramètres
3. Superviser la transformation sécurisée

Author: Équipe Maintenance NextGeneration
Version: 1.0.0
Created: 2025-01-20
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire des agents au PATH
sys.path.insert(0, str(Path(__file__).parent / "agent_equipe_maintenance"))

from agent_MAINTENANCE_00_chef_equipe_coordinateur import create_chef_equipe_coordinateur

async def instruire_chef_transformation():
    """Instructions complètes pour le chef d'équipe"""
    
    print("🎯 INSTRUCTIONS CHEF D'ÉQUIPE - TRANSFORMATION PATTERN FACTORY")
    print("=" * 80)
    
    # 1. Charger la configuration de mission
    print(f"\n📋 PHASE 1: CHARGEMENT CONFIGURATION MISSION")
    
    config_path = Path("config_mission_transformation.json")
    if not config_path.exists():
        print(f"❌ Erreur: Configuration mission non trouvée: {config_path}")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_mission = json.load(f)
    
    mission_config = config_mission["mission_transformation_pattern_factory"]
    print(f"   ✅ Configuration chargée: {mission_config['mission_id']}")
    print(f"   📅 Date création: {mission_config['date_creation']}")
    print(f"   🎯 Statut: {mission_config['statut']}")
    
    # 2. Créer et configurer le chef d'équipe
    print(f"\n👨‍💼 PHASE 2: CONFIGURATION CHEF D'ÉQUIPE")
    
    chef_equipe = create_chef_equipe_coordinateur()
    await chef_equipe.startup()
    
    print(f"   ✅ Chef d'équipe démarré: {chef_equipe.agent_id}")
    
    # 3. Instructions de configuration des répertoires
    print(f"\n📁 PHASE 3: CONFIGURATION RÉPERTOIRES")
    
    backup_config = mission_config["configuration_backup"]
    repertoires = mission_config["repertoires_cibles"]
    
    instructions_repertoires = {
        "backup_directory": backup_config["repertoire_backup"],
        "source_directory": repertoires["agents_source"],
        "reviews_directory": repertoires["reviews_destination"],
        "logs_directory": repertoires["logs_mission"],
        "reports_directory": repertoires["reports_mission"]
    }
    
    print(f"   📊 INSTRUCTIONS RÉPERTOIRES POUR L'ÉQUIPE:")
    for key, value in instructions_repertoires.items():
        print(f"      • {key}: {value}")
    
    # 4. Instructions de configuration de sécurité
    print(f"\n🛡️ PHASE 4: CONFIGURATION SÉCURITÉ")
    
    securite_config = mission_config["parametres_securite"]
    
    instructions_securite = {
        "backup_obligatoire_avant_modification": backup_config["backup_obligatoire"],
        "verification_integrite_backup": backup_config["verification_integrite"],
        "validation_syntaxe_python": securite_config["validation_syntaxe_python"],
        "rollback_automatique": securite_config["rollback_automatique_erreur"],
        "logs_detailles": securite_config["sauvegarde_logs_detailles"]
    }
    
    print(f"   🔒 INSTRUCTIONS SÉCURITÉ POUR L'ÉQUIPE:")
    for key, value in instructions_securite.items():
        print(f"      • {key}: {value}")
    
    # 5. Configuration des agents de l'équipe
    print(f"\n👥 PHASE 5: CONFIGURATION ÉQUIPE")
    
    agents_config = mission_config["agents_equipe_maintenance"]
    
    # Instructions pour chaque agent
    instructions_agents = {
        "Agent 03 (Adaptateur)": {
            "backup_directory": backup_config["repertoire_backup"],
            "backup_format": backup_config["format_nom_backup"],
            "force_backup": backup_config["backup_obligatoire"],
            "verify_integrity": backup_config["verification_integrite"]
        },
        "Agent 04 (Testeur)": {
            "audit_directory": repertoires["agents_source"],
            "reports_directory": repertoires["reviews_destination"],
            "pattern_factory_compliance": True,
            "syntax_validation": securite_config["validation_syntaxe_python"]
        },
        "Tous les agents": {
            "source_directory": repertoires["agents_source"],
            "mission_logs": repertoires["logs_mission"],
            "mission_reports": repertoires["reports_mission"]
        }
    }
    
    print(f"   🔧 INSTRUCTIONS SPÉCIFIQUES PAR AGENT:")
    for agent, config in instructions_agents.items():
        print(f"      📋 {agent}:")
        for param, value in config.items():
            print(f"         • {param}: {value}")
    
    # 6. Workflow de transformation
    print(f"\n🔄 PHASE 6: WORKFLOW TRANSFORMATION")
    
    workflow = mission_config["workflow_transformation"]
    
    print(f"   📋 WORKFLOW RECOMMANDÉ:")
    for phase, description in workflow.items():
        print(f"      {phase}: {description}")
    
    # 7. Critères de validation
    print(f"\n✅ PHASE 7: CRITÈRES VALIDATION")
    
    criteres = mission_config["criteres_transformation"]
    
    print(f"   📊 CRITÈRES OBLIGATOIRES:")
    print(f"      • Score conformité minimum: {criteres['score_conformite_minimum']}%")
    print(f"      • Corrections critiques:")
    for correction in criteres["corrections_critiques_obligatoires"]:
        print(f"        - {correction}")
    print(f"      • Validations requises:")
    for validation in criteres["validations_requises"]:
        print(f"        - {validation}")
    
    # 8. Statistiques cibles
    print(f"\n📈 PHASE 8: OBJECTIFS MISSION")
    
    stats = mission_config["statistiques_cibles"]
    
    print(f"   🎯 OBJECTIFS À ATTEINDRE:")
    print(f"      • Agents total: {stats['agents_total_detectes']}")
    print(f"      • Agents conformes actuels: {stats['agents_conformes_actuels']}")
    print(f"      • Agents à transformer: {stats['agents_non_conformes']}")
    print(f"      • Objectif conformité: {stats['objectif_conformite']}")
    print(f"      • Score cible: {stats['score_conformite_cible']}%")
    
    # 9. Commandes de lancement
    print(f"\n🚀 PHASE 9: COMMANDES PRÊTES")
    
    commandes = {
        "Test backup un agent": "python test_backup_et_un_agent.py",
        "Test transformation un agent": "python test_transformation_un_agent.py",
        "Analyse complète agents": "python lancer_mission_analyse_factory_direct.py",
        "Transformation massive": "python lancer_transformation_pattern_factory.py"
    }
    
    print(f"   💻 COMMANDES DISPONIBLES:")
    for nom, commande in commandes.items():
        print(f"      • {nom}: {commande}")
    
    # 10. Instructions finales au chef
    print(f"\n" + "=" * 80)
    print(f"👨‍💼 INSTRUCTIONS FINALES POUR LE CHEF D'ÉQUIPE")
    print("=" * 80)
    
    instructions_finales = [
        "1. Configurer tous les agents avec les paramètres ci-dessus",
        "2. Vérifier que les répertoires de backup sont accessibles",
        "3. Tester le système de backup sur un agent d'abord",
        "4. Coordonner l'équipe selon le workflow recommandé",
        "5. Superviser chaque phase de transformation",
        "6. Valider les résultats avant passage à l'étape suivante",
        "7. Maintenir les logs détaillés de toutes les opérations",
        "8. Assurer la sécurité des données à chaque étape"
    ]
    
    for instruction in instructions_finales:
        print(f"   {instruction}")
    
    print(f"\n🛡️ SÉCURITÉ PRIORITAIRE:")
    print(f"   • BACKUP OBLIGATOIRE avant toute modification")
    print(f"   • VALIDATION SYNTAXE après chaque transformation")
    print(f"   • ROLLBACK AUTOMATIQUE en cas d'erreur")
    print(f"   • LOGS DÉTAILLÉS de toutes les opérations")
    
    print(f"\n✅ CHEF D'ÉQUIPE PRÊT À COORDONNER LA MISSION!")
    print("=" * 80)
    
    # Arrêt propre
    await chef_equipe.shutdown()

def main():
    """Point d'entrée principal"""
    try:
        asyncio.run(instruire_chef_transformation())
    except KeyboardInterrupt:
        print("\n⚠️ Instructions interrompues par l'utilisateur")
    except Exception as e:
        print(f"\n💥 Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 



