#!/usr/bin/env python3
"""
Configurateur pour l'équipe de maintenance des agents.
Permet de choisir quels agents utiliser et de lancer des missions ciblées.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime

def check_agent_availability():
    """Vérifie quels agents sont disponibles."""
    agents_dir = Path("agent_factory_implementation/agents")
    
    available_agents = {
        "base": {},
        "extended": {}
    }
    
    # Agents de base (obligatoires)
    base_agents = {
        "01_analyseur": "agent_MAINTENANCE_01_analyseur_structure.py",
        "02_evaluateur": "agent_MAINTENANCE_02_evaluateur_utilite.py", 
        "03_adaptateur": "agent_MAINTENANCE_03_adaptateur_code.py",
        "04_testeur": "agent_MAINTENANCE_04_testeur_anti_faux_agents.py",
        "05_documenteur": "agent_MAINTENANCE_05_documenteur_peer_reviewer.py",
        "06_validateur": "agent_MAINTENANCE_06_validateur_final.py"
    }
    
    # Agents étendus (optionnels)
    extended_agents = {
        "07_dependances": "agent_MAINTENANCE_07_gestionnaire_dependances.py",
        "08_performance": "agent_MAINTENANCE_08_optimiseur_performance.py"
    }
    
    # Vérification des agents de base
    for agent_key, filename in base_agents.items():
        filepath = agents_dir / filename
        available_agents["base"][agent_key] = {
            "filename": filename,
            "available": filepath.exists(),
            "path": str(filepath)
        }
    
    # Vérification des agents étendus
    for agent_key, filename in extended_agents.items():
        filepath = agents_dir / filename
        available_agents["extended"][agent_key] = {
            "filename": filename,
            "available": filepath.exists(),
            "path": str(filepath)
        }
    
    return available_agents

def display_agent_status(availability):
    """Affiche le statut des agents disponibles."""
    print("\n" + "="*60)
    print("🔍 ÉTAT DE L'ÉQUIPE DE MAINTENANCE")
    print("="*60)
    
    print("\n📋 AGENTS DE BASE (obligatoires):")
    all_base_ok = True
    for agent_key, info in availability["base"].items():
        status = "✅" if info["available"] else "❌"
        print(f"  {status} {agent_key.replace('_', ' ').title()}")
        if not info["available"]:
            all_base_ok = False
    
    print(f"\n⚡ AGENTS ÉTENDUS (optionnels):")
    extended_count = 0
    for agent_key, info in availability["extended"].items():
        status = "✅" if info["available"] else "❌"
        print(f"  {status} {agent_key.replace('_', ' ').title()}")
        if info["available"]:
            extended_count += 1
    
    print(f"\n📊 RÉSUMÉ:")
    base_available = sum(1 for info in availability["base"].values() if info["available"])
    print(f"  • Agents de base : {base_available}/{len(availability['base'])}")
    print(f"  • Agents étendus : {extended_count}/{len(availability['extended'])}")
    
    if all_base_ok:
        print(f"  • 🎉 Équipe de base complète et opérationnelle!")
        if extended_count > 0:
            print(f"  • ⚡ Mode étendu disponible avec {extended_count} agent(s) supplémentaire(s)")
    else:
        print(f"  • ⚠️  Agents manquants - équipe incomplète")
    
    return all_base_ok, extended_count

def choose_mission_mode():
    """Permet à l'utilisateur de choisir le mode de mission."""
    print("\n" + "="*60)
    print("🎯 CHOIX DU MODE DE MISSION")
    print("="*60)
    
    print("\n1. 📋 Mode STANDARD")
    print("   • Utilise uniquement les agents de base")
    print("   • Rapide et efficace pour la maintenance courante")
    print("   • Pipeline : Analyse → Évaluation → Adaptation → Test → Documentation → Validation")
    
    print("\n2. ⚡ Mode ÉTENDU")
    print("   • Utilise tous les agents disponibles")
    print("   • Analyse approfondie avec optimisations")
    print("   • Pipeline : Analyse → Évaluation → Dépendances → Adaptation → Performance → Test → Documentation → Validation")
    
    print("\n3. 🎛️  Mode PERSONNALISÉ")
    print("   • Choisir manuellement les agents à utiliser")
    print("   • Contrôle fin du processus de maintenance")
    
    while True:
        choice = input("\n➤ Votre choix (1/2/3) : ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        print("❌ Choix invalide. Veuillez entrer 1, 2 ou 3.")

def choose_target_directory():
    """Permet de choisir le répertoire cible."""
    print("\n" + "="*60)
    print("📁 CHOIX DU RÉPERTOIRE CIBLE")
    print("="*60)
    
    default_dir = "agent_factory_implementation/agents"
    print(f"\nRépertoire par défaut : {default_dir}")
    
    if os.path.exists(default_dir):
        py_files = [f for f in os.listdir(default_dir) if f.endswith('.py')]
        print(f"📊 Fichiers Python trouvés : {len(py_files)}")
        if py_files:
            print("📋 Exemples de fichiers :")
            for f in sorted(py_files)[:5]:
                print(f"  • {f}")
            if len(py_files) > 5:
                print(f"  ... et {len(py_files) - 5} autres")
    else:
        print("⚠️  Répertoire par défaut non trouvé")
    
    while True:
        user_input = input(f"\n➤ Répertoire cible (Entrée pour '{default_dir}') : ").strip()
        
        target_dir = user_input if user_input else default_dir
        
        if os.path.exists(target_dir):
            return target_dir
        else:
            print(f"❌ Le répertoire '{target_dir}' n'existe pas.")
            print("💡 Créer le répertoire? (y/n)")
            create = input("➤ ").strip().lower()
            if create in ['y', 'yes', 'o', 'oui']:
                try:
                    os.makedirs(target_dir, exist_ok=True)
                    print(f"✅ Répertoire créé : {target_dir}")
                    return target_dir
                except Exception as e:
                    print(f"❌ Erreur lors de la création : {e}")

async def run_maintenance_mission(mode, target_directory, availability):
    """Lance la mission de maintenance."""
    print("\n" + "="*60)
    print("🚀 LANCEMENT DE LA MISSION")
    print("="*60)
    
    try:
        # Configuration du chemin d'importation
        project_root = Path(__file__).resolve().parents[0]
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        # Import du système de logging
        try:
            from core import logging_manager
            print("✅ Système de logging initialisé")
        except ImportError as e:
            print(f"⚠️  Logging non disponible : {e}")
            import logging
            logging.basicConfig(level=logging.INFO)

        # Import de l'architecture
        from agent_factory_implementation.core.agent_factory_architecture import Task, Result
        
        # Choix du chef d'équipe selon le mode
        if mode == "1":  # Standard
            from agent_factory_implementation.agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_MAINTENANCE_00_chef_equipe_coordinateur as create_chef
            print("📋 Mode standard sélectionné")
            chef_equipe = create_chef(target_path=target_directory, workspace_path=".")
            task_type = "maintenance_complete"
            
        elif mode == "2":  # Étendu
            try:
                from agent_factory_implementation.agents.agent_MAINTENANCE_00_chef_equipe_coordinateur_extended import create_agent_MAINTENANCE_00_chef_equipe_coordinateur_extended as create_chef_extended
                print("⚡ Mode étendu sélectionné")
                chef_equipe = create_chef_extended(target_path=target_directory, workspace_path=".", extended_mode=True)
                task_type = "maintenance_extended"
            except ImportError:
                print("⚠️  Chef d'équipe étendu non disponible, basculement en mode standard")
                from agent_factory_implementation.agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_MAINTENANCE_00_chef_equipe_coordinateur as create_chef
                chef_equipe = create_chef(target_path=target_directory, workspace_path=".")
                task_type = "maintenance_complete"
        
        # Création et exécution de la tâche
        mission_task = Task(
            type=task_type,
            params={
                "description": f"Mission de maintenance en mode {['', 'standard', 'étendu', 'personnalisé'][int(mode)]}",
                "target_directory": target_directory,
                "report_filename": f"rapport_maintenance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            }
        )
        
        print(f"🔄 Exécution en cours...")
        print(f"📁 Répertoire : {target_directory}")
        
        # Exécution de la mission
        result = await chef_equipe.execute_task(mission_task)
        
        # Traitement du résultat
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if result.success:
            report_path = f"rapport_maintenance_SUCCESS_{timestamp}.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(result.data, f, indent=4, ensure_ascii=False)
            
            print(f"\n🎉 MISSION RÉUSSIE!")
            print(f"📄 Rapport détaillé : {report_path}")
            
            # Affichage du résumé
            if "summary" in result.data:
                summary = result.data["summary"]
                print(f"\n📊 RÉSUMÉ DE LA MISSION:")
                print(f"  • Fichiers traités : {summary.get('total_files_processed', 0)}")
                print(f"  • Succès : {summary.get('successful_files', 0)}")
                print(f"  • Échecs : {summary.get('failed_files', 0)}")
                print(f"  • Taux de réussite : {summary.get('success_rate', 0):.1f}%")
                
                if "performance_metrics" in summary:
                    perf = summary["performance_metrics"]
                    print(f"  • Score performance moyen : {perf.get('average_score', 0):.1f}/100")
        
        else:
            report_path = f"rapport_maintenance_ECHEC_{timestamp}.json"
            error_data = {
                "error": result.error,
                "timestamp": timestamp,
                "mode": mode,
                "target_directory": target_directory
            }
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(error_data, f, indent=4, ensure_ascii=False)
            
            print(f"\n❌ MISSION ÉCHOUÉE")
            print(f"📄 Rapport d'erreur : {report_path}")
            print(f"🔍 Erreur : {result.error}")

    except Exception as e:
        print(f"\n💥 ERREUR CRITIQUE : {e}")
        import traceback
        traceback.print_exc()

def main():
    """Point d'entrée principal du configurateur."""
    print("🔧 CONFIGURATEUR D'ÉQUIPE DE MAINTENANCE")
    print("=" * 60)
    
    # Vérification de la disponibilité des agents
    availability = check_agent_availability()
    all_base_ok, extended_count = display_agent_status(availability)
    
    if not all_base_ok:
        print("\n❌ Impossible de continuer : agents de base manquants.")
        print("💡 Assurez-vous que tous les fichiers d'agents sont présents.")
        return 1
    
    # Choix du mode
    mode = choose_mission_mode()
    
    # Choix du répertoire
    target_directory = choose_target_directory()
    
    print(f"\n🎯 CONFIGURATION CHOISIE:")
    print(f"  • Mode : {['', 'Standard', 'Étendu', 'Personnalisé'][int(mode)]}")
    print(f"  • Répertoire : {target_directory}")
    
    # Confirmation
    confirm = input("\n➤ Lancer la mission? (y/n) : ").strip().lower()
    if confirm not in ['y', 'yes', 'o', 'oui']:
        print("❌ Mission annulée.")
        return 0
    
    # Lancement de la mission
    try:
        asyncio.run(run_maintenance_mission(mode, target_directory, availability))
        return 0
    except KeyboardInterrupt:
        print("\n⏹️  Mission interrompue par l'utilisateur.")
        return 1
    except Exception as e:
        print(f"\n💥 Erreur lors du lancement : {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())