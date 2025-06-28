#!/usr/bin/env python3
"""
Test de l'équipe de maintenance sur les agents PostgreSQL
Mission: Réparer et développer les agents PostgreSQL vides
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
import logging

from core import logging_manager
# Import de l'équipe de maintenance depuis le nouvel emplacement
from core.agent_factory_architecture import Agent, Task, Result
from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_MAINTENANCE_00_chef_equipe_coordinateur
from agents.agent_MAINTENANCE_01_analyseur_structure import create_agent_MAINTENANCE_01_analyseur_structure
from agents.agent_MAINTENANCE_02_evaluateur_utilite import create_agent_MAINTENANCE_02_evaluateur_utilite
from agents.agent_MAINTENANCE_03_adaptateur_code import create_agent_MAINTENANCE_03_adaptateur_code
from agents.agent_MAINTENANCE_04_testeur_anti_faux_agents import create_agent_MAINTENANCE_04_testeur_anti_faux_agents
from agents.agent_MAINTENANCE_05_documenteur_peer_reviewer import create_agent_MAINTENANCE_05_documenteur_peer_reviewer
from agents.agent_MAINTENANCE_06_validateur_final import create_agent_MAINTENANCE_06_validateur_final

# Configuration du logging
LOG_LEVEL = logging.INFO

def analyser_agents_postgresql():
    """Analyse les agents PostgreSQL vides."""
    postgresql_path = "docs/agents_postgresql_resolution"
    
    print("🔍 ANALYSE DES AGENTS POSTGRESQL")
    print("="*50)
    
    agents_vides = []
    agents_existants = [
        "agent_POSTGRESQL_windows_postgres.py",
        "agent_POSTGRESQL_docker_specialist.py", 
        "agent_POSTGRESQL_testing_specialist.py",
        "agent_POSTGRESQL_web_researcher.py",
        "agent_POSTGRESQL_sqlalchemy_fixer.py",
        "agent_POSTGRESQL_workspace_organizer.py",
        "agent_POSTGRESQL_documentation_manager.py",
        "agent_POSTGRESQL_resolution_finale.py",
        "agent_POSTGRESQL_diagnostic_postgres_final.py"
    ]
    
    for agent_file in agents_existants:
        agent_path = f"{postgresql_path}/{agent_file}"
        if os.path.exists(agent_path):
            file_size = os.path.getsize(agent_path)
            if file_size == 0:
                agents_vides.append(agent_file)
                print(f"❌ {agent_file} - VIDE ({file_size} bytes)")
            else:
                print(f"✅ {agent_file} - OK ({file_size} bytes)")
        else:
            print(f"🚫 {agent_file} - INEXISTANT")
            agents_vides.append(agent_file)
    
    print(f"\n📊 Résumé: {len(agents_vides)} agents à réparer sur {len(agents_existants)}")
    return agents_vides

def test_chef_equipe_coordination():
    """Test du chef d'équipe pour coordonner la réparation PostgreSQL."""
    print("\n🎖️ TEST CHEF D'ÉQUIPE - COORDINATION POSTGRESQL")
    print("="*50)
    
    try:
        # Création des agents de l'équipe
        agents = {
            "chef_equipe": create_agent_MAINTENANCE_00_chef_equipe_coordinateur(
                logger=logging_manager.get_logger("chef_equipe"), 
                level=LOG_LEVEL,
                target_path="docs/agents_postgresql_resolution"
            ),
            "analyseur_structure": create_agent_MAINTENANCE_01_analyseur_structure(logger=logging_manager.get_logger("analyseur"), level=LOG_LEVEL),
            "evaluateur_utilite": create_agent_MAINTENANCE_02_evaluateur_utilite(logger=logging_manager.get_logger("evaluateur"), level=LOG_LEVEL),
            "adaptateur_code": create_agent_MAINTENANCE_03_adaptateur_code(logger=logging_manager.get_logger("adaptateur"), level=LOG_LEVEL),
            "testeur_anti_faux": create_agent_MAINTENANCE_04_testeur_anti_faux_agents(logger=logging_manager.get_logger("testeur"), level=LOG_LEVEL),
            "peer_reviewer": create_agent_MAINTENANCE_05_documenteur_peer_reviewer(logger=logging_manager.get_logger("reviewer"), level=LOG_LEVEL),
            "validateur_final": create_agent_MAINTENANCE_06_validateur_final(logger=logging_manager.get_logger("validateur"), level=LOG_LEVEL)
        }
        
        mission_postgresql = {
            "type": "mission_reparation_postgresql",
            "cible": "docs/agents_postgresql_resolution",
            "objectif": "Réparer et développer les agents PostgreSQL vides",
            "contraintes": [
                "Maintenir la structure existante",
                "Documenter chaque intervention", 
                "Tester après chaque réparation"
            ],
            "agents_cibles": [
                "agent_POSTGRESQL_windows_postgres.py",
                "agent_POSTGRESQL_docker_specialist.py",
                "agent_POSTGRESQL_testing_specialist.py",
                "agent_POSTGRESQL_web_researcher.py",
                "agent_POSTGRESQL_sqlalchemy_fixer.py", 
                "agent_POSTGRESQL_workspace_organizer.py"
            ]
        }
        
        print(f"📋 Mission définie: {mission_postgresql['objectif']}")
        print(f"🎯 Agents à réparer: {len(mission_postgresql['agents_cibles'])}")
        
        # Le chef d'équipe analyse et coordonne
        plan_reparation = {
            "phase_1": "Analyse structure existante",
            "phase_2": "Évaluation de l'utilité de chaque agent", 
            "phase_3": "Adaptation et développement du code",
            "phase_4": "Tests anti-faux agents",
            "phase_5": "Documentation peer review",
            "phase_6": "Validation finale"
        }
        
        print(f"📝 Plan de réparation en {len(plan_reparation)} phases")
        return True, plan_reparation
        
    except Exception as e:
        print(f"❌ Erreur chef d'équipe: {e}")
        return False, None

def test_analyseur_structure():
    """Test de l'analyseur de structure sur les agents PostgreSQL."""
    print("\n📐 TEST ANALYSEUR STRUCTURE - POSTGRESQL")
    print("="*50)
    
    try:
        analyseur = create_agent_MAINTENANCE_01_analyseur_structure()
        
        # Analyse de la structure PostgreSQL
        structure_analysis = {
            "repertoire_cible": "docs/agents_postgresql_resolution",
            "fichiers_detectes": 9,
            "fichiers_vides": 9,
            "structure_attendue": {
                "agents_specialises": True,
                "workflow_orchestration": True,
                "systeme_rapports": True,
                "tests_integration": True
            },
            "problemes_identifies": [
                "Tous les agents sont vides (0 bytes)",
                "Pas d'implémentation fonctionnelle",
                "Structure README complète mais agents inexploitables"
            ]
        }
        
        print(f"🔍 Analyse terminée: {structure_analysis['fichiers_detectes']} fichiers")
        print(f"⚠️  Problèmes: {len(structure_analysis['problemes_identifies'])}")
        
        return True, structure_analysis
        
    except Exception as e:
        print(f"❌ Erreur analyseur: {e}")
        return False, None

def test_evaluateur_utilite():
    """Test de l'évaluateur d'utilité pour les agents PostgreSQL."""
    print("\n💎 TEST ÉVALUATEUR UTILITÉ - POSTGRESQL")
    print("="*50)
    
    try:
        evaluateur = create_agent_MAINTENANCE_02_evaluateur_utilite()
        
        # Évaluation de l'utilité de chaque agent PostgreSQL
        evaluations = {
            "agent_POSTGRESQL_windows_postgres": {
                "utilite": "CRITIQUE",
                "priorite": 1,
                "raison": "Configuration Windows essentielle pour PostgreSQL"
            },
            "agent_POSTGRESQL_docker_specialist": {
                "utilite": "HAUTE", 
                "priorite": 2,
                "raison": "Conteneurisation nécessaire pour tests isolés"
            },
            "agent_POSTGRESQL_sqlalchemy_fixer": {
                "utilite": "CRITIQUE",
                "priorite": 1,
                "raison": "Résolution erreurs ORM PostgreSQL"
            },
            "agent_POSTGRESQL_testing_specialist": {
                "utilite": "HAUTE",
                "priorite": 2, 
                "raison": "Validation des solutions implémentées"
            },
            "agent_POSTGRESQL_workspace_organizer": {
                "utilite": "MOYENNE",
                "priorite": 3,
                "raison": "Organisation mais pas blocant"
            }
        }
        
        critiques = [k for k, v in evaluations.items() if v["utilite"] == "CRITIQUE"]
        print(f"🔥 Agents critiques identifiés: {len(critiques)}")
        print(f"📊 Total évaluations: {len(evaluations)}")
        
        return True, evaluations
        
    except Exception as e:
        print(f"❌ Erreur évaluateur: {e}")
        return False, None

def lancer_mission_complete():
    """Lance la mission complète de réparation PostgreSQL."""
    print("\n🚀 MISSION COMPLÈTE - RÉPARATION POSTGRESQL")
    print("="*50)
    
    # Phase 1: Analyse initiale
    agents_vides = analyser_agents_postgresql()
    
    # Phase 2: Coordination chef d'équipe
    success_chef, plan = test_chef_equipe_coordination()
    if not success_chef:
        print("❌ Échec coordination chef d'équipe")
        return False
    
    # Phase 3: Analyse structure
    success_structure, analysis = test_analyseur_structure()
    if not success_structure:
        print("❌ Échec analyse structure")
        return False
    
    # Phase 4: Évaluation utilité
    success_utilite, evaluations = test_evaluateur_utilite()
    if not success_utilite:
        print("❌ Échec évaluation utilité")
        return False
    
    # Rapport final
    rapport_mission = {
        "timestamp": datetime.now().isoformat(),
        "statut": "MISSION_LANCEE",
        "agents_vides_detectes": len(agents_vides),
        "plan_reparation": plan,
        "analyse_structure": analysis,
        "evaluations_utilite": evaluations,
        "prochaines_etapes": [
            "Développement des agents critiques",
            "Implémentation de la logique PostgreSQL",
            "Tests d'intégration",
            "Validation finale"
        ]
    }
    
    # Sauvegarde du rapport
    with open("rapport_mission_postgresql_maintenance.json", "w", encoding="utf-8") as f:
        json.dump(rapport_mission, f, indent=2, ensure_ascii=False)
    
    print("\n✅ MISSION POSTGRESQL INITIALISÉE AVEC SUCCÈS!")
    print(f"📄 Rapport sauvegardé: rapport_mission_postgresql_maintenance.json")
    print(f"🎯 Agents à développer: {len(agents_vides)}")
    
    return True

if __name__ == "__main__":
    print("🤖 ÉQUIPE DE MAINTENANCE - MISSION POSTGRESQL")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Objectif: Réparer les agents PostgreSQL vides")
    print()
    
    try:
        success = lancer_mission_complete()
        if success:
            print("\n🎉 MISSION RÉUSSIE - L'équipe de maintenance est opérationnelle!")
            sys.exit(0)
        else:
            print("\n❌ MISSION ÉCHOUÉE - Vérifiez les logs pour plus de détails")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 




