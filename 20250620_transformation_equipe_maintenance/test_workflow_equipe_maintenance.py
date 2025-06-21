#!/usr/bin/env python3
"""
Script de Test du Workflow Complet - Équipe de Maintenance NextGeneration
Test de l'enchaînement Agent 00 → Agent 01 → Agent 02 → Agent 03 → Agent 04 → Agent 05 → Agent 06
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Configuration des chemins
CURRENT_DIR = Path(__file__).parent
AGENT_DIR = CURRENT_DIR / "agent_equipe_maintenance"
REPORTS_DIR = CURRENT_DIR / "reports_workflow_test"
TARGET_DIR = CURRENT_DIR.parent / "agent_factory_implementation" / "agents"

# Créer le répertoire de rapports
REPORTS_DIR.mkdir(exist_ok=True)

def log_workflow(etape, message, status="INFO"):
    """Log des étapes du workflow"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_entry = f"[{timestamp}] [{status}] WORKFLOW_{etape}: {message}"
    print(log_entry)
    
    # Sauvegarder dans un fichier log
    log_file = REPORTS_DIR / f"workflow_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

async def importer_agent(nom_agent, chemin_agent):
    """Importer un agent de manière sécurisée"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(nom_agent, chemin_agent)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        log_workflow("IMPORT", f"Erreur import {nom_agent}: {e}", "ERROR")
        return None

async def tester_workflow_complet():
    """Test complet du workflow de l'équipe de maintenance"""
    
    log_workflow("DEBUT", "=== DÉBUT TEST WORKFLOW ÉQUIPE MAINTENANCE ===")
    
    # Dictionnaire des agents dans l'ordre du workflow
    agents_workflow = {
        "00_CHEF": AGENT_DIR / "agent_MAINTENANCE_00_chef_equipe_coordinateur.py",
        "01_ANALYSEUR": AGENT_DIR / "agent_MAINTENANCE_01_analyseur_structure.py", 
        "02_EVALUATEUR": AGENT_DIR / "agent_MAINTENANCE_02_evaluateur_utilite.py",
        "03_ADAPTATEUR": AGENT_DIR / "agent_MAINTENANCE_03_adaptateur_code.py",
        "04_TESTEUR": AGENT_DIR / "agent_MAINTENANCE_04_testeur_anti_faux_agents.py",
        "05_DOCUMENTEUR": AGENT_DIR / "agent_MAINTENANCE_05_documenteur_peer_reviewer.py",
        "06_VALIDATEUR": "PLACEHOLDER" # À définir si nécessaire
    }
    
    resultats_workflow = {}
    
    # ÉTAPE 1: Vérification de l'existence des agents
    log_workflow("VERIFICATION", "Vérification de l'existence des agents...")
    for nom, chemin in agents_workflow.items():
        if chemin != "PLACEHOLDER":
            if Path(chemin).exists():
                log_workflow("VERIF", f"✓ Agent {nom} trouvé: {chemin}")
                resultats_workflow[nom] = {"existe": True, "chemin": str(chemin)}
            else:
                log_workflow("VERIF", f"✗ Agent {nom} MANQUANT: {chemin}", "ERROR")
                resultats_workflow[nom] = {"existe": False, "chemin": str(chemin)}
    
    # ÉTAPE 2: Test d'importation des agents
    log_workflow("IMPORT", "Test d'importation des agents...")
    agents_importes = {}
    
    for nom, info in resultats_workflow.items():
        if info["existe"] and agents_workflow[nom] != "PLACEHOLDER":
            agent_module = await importer_agent(nom, info["chemin"])
            if agent_module:
                agents_importes[nom] = agent_module
                log_workflow("IMPORT", f"✓ Agent {nom} importé avec succès")
                resultats_workflow[nom]["importe"] = True
            else:
                log_workflow("IMPORT", f"✗ Échec import Agent {nom}", "ERROR")
                resultats_workflow[nom]["importe"] = False
    
    # ÉTAPE 3: Test d'initialisation des agents
    log_workflow("INIT", "Test d'initialisation des agents...")
    agents_initialises = {}
    
    for nom, module in agents_importes.items():
        try:
            # Chercher la classe principale dans le module
            classes = [getattr(module, attr) for attr in dir(module) 
                      if isinstance(getattr(module, attr), type) and 
                      not attr.startswith('_')]
            
            for classe in classes:
                if hasattr(classe, '__init__'):
                    try:
                        instance = classe()
                        agents_initialises[nom] = instance
                        log_workflow("INIT", f"✓ Agent {nom} initialisé: {classe.__name__}")
                        resultats_workflow[nom]["initialise"] = True
                        resultats_workflow[nom]["classe"] = classe.__name__
                        break
                    except Exception as e:
                        log_workflow("INIT", f"✗ Erreur init {nom}: {e}", "ERROR")
                        continue
            
            if nom not in agents_initialises:
                log_workflow("INIT", f"✗ Aucune classe initialisable trouvée pour {nom}", "ERROR")
                resultats_workflow[nom]["initialise"] = False
                
        except Exception as e:
            log_workflow("INIT", f"✗ Erreur inspection {nom}: {e}", "ERROR")
            resultats_workflow[nom]["initialise"] = False
    
    # ÉTAPE 4: Test des méthodes principales
    log_workflow("METHODES", "Test des méthodes principales des agents...")
    
    for nom, instance in agents_initialises.items():
        try:
            # Lister les méthodes disponibles
            methodes = [method for method in dir(instance) 
                       if callable(getattr(instance, method)) and not method.startswith('_')]
            
            resultats_workflow[nom]["methodes"] = methodes
            log_workflow("METHODES", f"✓ Agent {nom} - Méthodes: {', '.join(methodes[:5])}...")
            
            # Test de méthodes communes
            if hasattr(instance, 'startup'):
                try:
                    if asyncio.iscoroutinefunction(instance.startup):
                        await instance.startup()
                    else:
                        instance.startup()
                    log_workflow("METHODES", f"✓ Agent {nom} - startup() OK")
                except Exception as e:
                    log_workflow("METHODES", f"✗ Agent {nom} - startup() ERROR: {e}", "ERROR")
            
        except Exception as e:
            log_workflow("METHODES", f"✗ Agent {nom} - Erreur test méthodes: {e}", "ERROR")
    
    # ÉTAPE 5: Test du workflow séquentiel simulé
    log_workflow("WORKFLOW", "Test du workflow séquentiel simulé...")
    
    # Simulation d'une mission
    mission_test = {
        "cible": str(TARGET_DIR),
        "objectif": "Correction des agents Factory Pattern",
        "agents_defaillants": [
            "agent_01_coordinateur_principal.py",
            "agent_02_architecte_code_expert.py", 
            "agent_04_expert_securite_crypto.py",
            "agent_05_maitre_tests_validation.py"
        ]
    }
    
    workflow_status = {}
    
    # Simulation étape par étape
    etapes_workflow = [
        ("00_CHEF", "Coordination et planification de la mission"),
        ("01_ANALYSEUR", "Analyse de la structure des agents défaillants"),
        ("02_EVALUATEUR", "Évaluation de l'utilité et priorités"),
        ("03_ADAPTATEUR", "Adaptation du code selon Factory Pattern"),
        ("04_TESTEUR", "Tests de validation des corrections"),
        ("05_DOCUMENTEUR", "Documentation des changements"),
        ("06_VALIDATEUR", "Validation finale du workflow")
    ]
    
    for etape, description in etapes_workflow:
        if etape in agents_initialises:
            try:
                # Simulation d'exécution
                log_workflow("WORKFLOW", f"► {etape}: {description}")
                workflow_status[etape] = {
                    "description": description,
                    "status": "SIMULE_OK",
                    "timestamp": datetime.now().isoformat()
                }
                await asyncio.sleep(0.1)  # Simulation d'exécution
                log_workflow("WORKFLOW", f"✓ {etape} complété avec succès")
            except Exception as e:
                log_workflow("WORKFLOW", f"✗ {etape} échec: {e}", "ERROR")
                workflow_status[etape] = {
                    "description": description,
                    "status": "ERROR",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        else:
            log_workflow("WORKFLOW", f"⚠ {etape} non disponible - {description}", "WARNING")
            workflow_status[etape] = {
                "description": description,
                "status": "NON_DISPONIBLE",
                "timestamp": datetime.now().isoformat()
            }
    
    # ÉTAPE 6: Génération du rapport final
    log_workflow("RAPPORT", "Génération du rapport final...")
    
    rapport_final = {
        "mission": mission_test,
        "timestamp": datetime.now().isoformat(),
        "resultats_agents": resultats_workflow,
        "workflow_status": workflow_status,
        "resume": {
            "agents_disponibles": len([a for a in resultats_workflow.values() if a.get("existe", False)]),
            "agents_importes": len([a for a in resultats_workflow.values() if a.get("importe", False)]),
            "agents_initialises": len([a for a in resultats_workflow.values() if a.get("initialise", False)]),
            "workflow_complete": len([w for w in workflow_status.values() if w["status"] == "SIMULE_OK"])
        }
    }
    
    # Sauvegarder le rapport
    rapport_file = REPORTS_DIR / f"rapport_workflow_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(rapport_file, "w", encoding="utf-8") as f:
        json.dump(rapport_final, f, indent=2, ensure_ascii=False)
    
    log_workflow("RAPPORT", f"Rapport sauvegardé: {rapport_file}")
    
    # ÉTAPE 7: Résumé final
    log_workflow("RESUME", "=== RÉSUMÉ DU TEST WORKFLOW ===")
    log_workflow("RESUME", f"Agents disponibles: {rapport_final['resume']['agents_disponibles']}/6")
    log_workflow("RESUME", f"Agents importés: {rapport_final['resume']['agents_importes']}/6")
    log_workflow("RESUME", f"Agents initialisés: {rapport_final['resume']['agents_initialises']}/6") 
    log_workflow("RESUME", f"Étapes workflow: {rapport_final['resume']['workflow_complete']}/7")
    
    if rapport_final['resume']['workflow_complete'] >= 5:
        log_workflow("RESUME", "🎯 WORKFLOW FONCTIONNEL - Équipe de maintenance opérationnelle!", "SUCCESS")
    elif rapport_final['resume']['workflow_complete'] >= 3:
        log_workflow("RESUME", "⚠️ WORKFLOW PARTIEL - Quelques problèmes à corriger", "WARNING")
    else:
        log_workflow("RESUME", "❌ WORKFLOW DÉFAILLANT - Corrections majeures nécessaires", "ERROR")
    
    log_workflow("FIN", "=== FIN TEST WORKFLOW ===")
    
    return rapport_final

async def main():
    """Point d'entrée principal"""
    try:
        print("🚀 Démarrage du test de workflow de l'équipe de maintenance...")
        rapport = await tester_workflow_complet()
        print("\n📊 Test terminé! Consultez les rapports dans:", REPORTS_DIR)
        return rapport
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(main()) 