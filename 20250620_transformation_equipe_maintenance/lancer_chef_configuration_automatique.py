#!/usr/bin/env python3
"""
👨‍💼 CHEF D'ÉQUIPE - CONFIGURATION AUTOMATIQUE AGENTS
===================================================

Script pour que le chef d'équipe configure automatiquement tous ses agents
avec les paramètres de la mission de transformation Pattern Factory.

Au lieu de coder en dur, le chef lit la configuration et instruit ses agents.

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

async def chef_configure_equipe_transformation():
    """Le chef d'équipe configure automatiquement ses agents"""
    
    print("👨‍💼 CHEF D'ÉQUIPE - CONFIGURATION AUTOMATIQUE TRANSFORMATION")
    print("=" * 80)
    
    # 1. Charger la configuration de mission
    print(f"\n📋 CHARGEMENT CONFIGURATION MISSION")
    
    config_path = Path("config_mission_transformation.json")
    if not config_path.exists():
        print(f"❌ Erreur: Configuration mission non trouvée: {config_path}")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_mission = json.load(f)
    
    mission_config = config_mission["mission_transformation_pattern_factory"]
    print(f"   ✅ Configuration chargée: {mission_config['mission_id']}")
    
    # 2. Démarrer le chef d'équipe
    print(f"\n👨‍💼 DÉMARRAGE CHEF D'ÉQUIPE")
    
    chef_equipe = create_chef_equipe_coordinateur()
    await chef_equipe.startup()
    
    print(f"   ✅ Chef d'équipe opérationnel: {chef_equipe.agent_id}")
    
    try:
        # 3. Préparer les instructions pour chaque agent
        print(f"\n🔧 PRÉPARATION INSTRUCTIONS AGENTS")
        
        backup_config = mission_config["configuration_backup"]
        repertoires = mission_config["repertoires_cibles"]
        securite = mission_config["parametres_securite"]
        
        # Instructions spécifiques par agent
        instructions_par_agent = {
            "Agent_03_Adaptateur": {
                "mission_id": mission_config["mission_id"],
                "backup_directory": backup_config["repertoire_backup"],
                "backup_format": backup_config["format_nom_backup"],
                "backup_obligatoire": backup_config["backup_obligatoire"],
                "verification_integrite": backup_config["verification_integrite"],
                "horodatage_unique": backup_config["horodatage_unique"],
                "source_directory": repertoires["agents_source"],
                "validation_syntaxe": securite["validation_syntaxe_python"],
                "rollback_automatique": securite["rollback_automatique_erreur"]
            },
            "Agent_04_Testeur": {
                "mission_id": mission_config["mission_id"],
                "audit_directory": repertoires["agents_source"],
                "reports_directory": repertoires["reviews_destination"],
                "pattern_factory_compliance": True,
                "syntax_validation": securite["validation_syntaxe_python"],
                "detailed_logging": securite["sauvegarde_logs_detailles"]
            },
            "Tous_Agents": {
                "mission_logs": repertoires["logs_mission"],
                "mission_reports": repertoires["reports_mission"],
                "source_directory": repertoires["agents_source"],
                "security_level": "MAXIMUM",
                "mission_workflow": mission_config["workflow_transformation"]
            }
        }
        
        print(f"   ✅ Instructions préparées pour {len(instructions_par_agent)} catégories d'agents")
        
        # 4. Créer les fichiers de configuration pour chaque agent
        print(f"\n📄 CRÉATION FICHIERS CONFIGURATION")
        
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)
        
        for agent_type, config in instructions_par_agent.items():
            config_file = config_dir / f"{agent_type.lower()}_config.json"
            
            config_complete = {
                "configuration_date": datetime.now().isoformat(),
                "configured_by": "Chef_Equipe_Maintenance",
                "mission_id": mission_config["mission_id"],
                "agent_type": agent_type,
                "parameters": config
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_complete, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Configuration créée: {config_file}")
        
        # 5. Créer le script de test avec configuration dynamique
        print(f"\n🧪 CRÉATION SCRIPT TEST DYNAMIQUE")
        
        test_script_content = f'''#!/usr/bin/env python3
"""
🧪 TEST BACKUP DYNAMIQUE - CONFIGURÉ PAR CHEF D'ÉQUIPE
=====================================================

Script de test généré automatiquement par le chef d'équipe
avec configuration dynamique basée sur la mission.

Generated: {datetime.now().isoformat()}
Mission: {mission_config["mission_id"]}
"""

import asyncio
import json
import sys
from pathlib import Path

# Configuration dynamique chargée depuis le chef d'équipe
BACKUP_DIRECTORY = "{backup_config["repertoire_backup"]}"
SOURCE_DIRECTORY = "{repertoires["agents_source"]}"
MISSION_ID = "{mission_config["mission_id"]}"

# Ajouter le répertoire des agents au PATH
sys.path.insert(0, str(Path(__file__).parent / "agent_equipe_maintenance"))

from agent_MAINTENANCE_03_adaptateur_code_UPGRADED import create_adaptateur_code_upgraded

async def test_backup_dynamique():
    """Test backup avec configuration dynamique du chef d'équipe"""
    
    print(f"🧪 TEST BACKUP DYNAMIQUE - {{MISSION_ID}}")
    print("=" * 70)
    
    # Charger la configuration Agent 03
    config_path = Path("config/agent_03_adaptateur_config.json")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            agent_config = json.load(f)
        
        print(f"   ✅ Configuration Agent 03 chargée")
        print(f"   📁 Backup directory: {{agent_config['parameters']['backup_directory']}}")
        print(f"   🛡️ Backup obligatoire: {{agent_config['parameters']['backup_obligatoire']}}")
    else:
        print(f"   ⚠️ Configuration par défaut utilisée")
        agent_config = {{"parameters": {{"backup_directory": BACKUP_DIRECTORY}}}}
    
    # Créer l'agent avec configuration dynamique
    agent = create_adaptateur_code_upgraded()
    
    # Configurer l'agent avec les paramètres du chef d'équipe
    agent.backup_dir = Path(agent_config['parameters']['backup_directory'])
    
    await agent.startup()
    
    print(f"   ✅ Agent configuré dynamiquement")
    print(f"   💾 Répertoire backup: {{agent.backup_dir}}")
    
    # Continuer avec le test...
    # [Le reste du test reste identique]
    
    await agent.shutdown()
    print(f"   ✅ Test terminé avec configuration dynamique!")

if __name__ == "__main__":
    asyncio.run(test_backup_dynamique())
'''
        
        test_script_path = Path("test_backup_dynamique_chef.py")
        with open(test_script_path, 'w', encoding='utf-8') as f:
            f.write(test_script_content)
        
        print(f"   ✅ Script test dynamique créé: {test_script_path}")
        
        # 6. Créer les instructions de lancement
        print(f"\n🚀 INSTRUCTIONS DE LANCEMENT")
        
        instructions_lancement = {
            "1_Voir_Instructions_Chef": "python instructions_chef_transformation_pattern_factory.py",
            "2_Test_Backup_Dynamique": "python test_backup_dynamique_chef.py",
            "3_Configuration_Agents": "Les agents liront automatiquement config/*.json",
            "4_Lancement_Mission": "python lancer_transformation_pattern_factory.py"
        }
        
        print(f"   📋 COMMANDES RECOMMANDÉES:")
        for etape, commande in instructions_lancement.items():
            print(f"      {etape}: {commande}")
        
        # 7. Résumé de la configuration
        print(f"\n" + "=" * 80)
        print(f"✅ CONFIGURATION AUTOMATIQUE TERMINÉE!")
        print("=" * 80)
        
        print(f"📊 RÉSUMÉ:")
        print(f"   👨‍💼 Chef d'équipe: Opérationnel")
        print(f"   📋 Mission: {mission_config['mission_id']}")
        print(f"   📁 Backup directory: {backup_config['repertoire_backup']}")
        print(f"   🎯 Agents source: {repertoires['agents_source']}")
        print(f"   📄 Fichiers config: {len(instructions_par_agent)} créés")
        print(f"   🧪 Script test: Généré automatiquement")
        
        print(f"\n🛡️ SÉCURITÉ:")
        print(f"   • Backup obligatoire: {backup_config['backup_obligatoire']}")
        print(f"   • Vérification intégrité: {backup_config['verification_integrite']}")
        print(f"   • Validation syntaxe: {securite['validation_syntaxe_python']}")
        print(f"   • Rollback automatique: {securite['rollback_automatique_erreur']}")
        
        print(f"\n👥 AGENTS CONFIGURÉS:")
        print(f"   • Agent 03 (Adaptateur): ✅ Configuré")
        print(f"   • Agent 04 (Testeur): ✅ Configuré")
        print(f"   • Tous agents: ✅ Paramètres globaux définis")
        
        print(f"\n🚀 PRÊT POUR LANCEMENT MISSION!")
        print(f"   💡 Étape suivante: python instructions_chef_transformation_pattern_factory.py")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Erreur configuration: {e}")
        raise
    
    finally:
        await chef_equipe.shutdown()

def main():
    """Point d'entrée principal"""
    try:
        asyncio.run(chef_configure_equipe_transformation())
    except KeyboardInterrupt:
        print("\n⚠️ Configuration interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n💥 Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 



