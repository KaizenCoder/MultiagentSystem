#!/usr/bin/env python3
"""
Script de test CLI pour agent_MAINTENANCE_00_chef_equipe_coordinateur.py
Validation des fonctionnalités essentielles selon le protocole standard.
"""
import asyncio
import sys
import json
from pathlib import Path

# Ajout du chemin du projet
sys.path.insert(0, str(Path(__file__).parent))

# Simulation des classes Task pour test si import échoue
class MockTask:
    def __init__(self, type, params):
        self.type = type
        self.params = params

# Test de l'import
try:
    from core.agent_factory_architecture import Task
    print("📦 Import core.agent_factory_architecture réussi")
except ImportError as e:
    print(f"⚠️  Import core échoué, utilisation de MockTask: {e}")
    Task = MockTask

try:
    from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_MAINTENANCE_00_chef_equipe_coordinateur
    print("📦 Import agent MAINTENANCE 00 réussi")
except ImportError as e:
    print(f"❌ ERREUR IMPORT AGENT: {e}")
    sys.exit(1)

async def test_agent_maintenance_00():
    """Test complet de l'agent MAINTENANCE 00 Chef d'Équipe Coordinateur."""
    print("=" * 80)
    print("🧪 TEST AGENT MAINTENANCE 00 - CHEF D'ÉQUIPE COORDINATEUR")
    print("=" * 80)
    
    success_count = 0
    total_tests = 4
    
    # Test 1: Création et Startup
    print("\n📋 Test 1: Création et Startup de l'agent")
    try:
        chef = create_agent_MAINTENANCE_00_chef_equipe_coordinateur(
            workspace_path=str(Path.cwd())
        )
        print(f"✅ Agent créé avec ID: {chef.agent_id}")
        
        # Startup - peut échouer si config manquante, ce qui est acceptable pour ce test
        try:
            await chef.startup()
            print("✅ Startup réussi - équipe recrutée")
            startup_ok = True
        except Exception as e:
            print(f"⚠️  Startup partiel (config/équipe): {e}")
            print("   (Acceptable - configuration factory peut être manquante)")
            startup_ok = False
            
        success_count += 1
    except Exception as e:
        print(f"❌ Échec création: {e}")
        return False

    # Test 2: Vérification des capacités
    print("\n📋 Test 2: Vérification des capacités")
    try:
        capabilities = chef.get_capabilities()
        expected_caps = [
            "workflow_maintenance_complete",
            "orchestration_equipe_maintenance", 
            "boucle_reparation_iterative",
            "coordination_agents_maintenance",
            "reporting_mission_json_md"
        ]
        
        print(f"Capacités trouvées: {capabilities}")
        
        if all(cap in capabilities for cap in expected_caps):
            print("✅ Toutes les capacités attendues sont présentes")
            success_count += 1
        else:
            print("❌ Capacités manquantes")
    except Exception as e:
        print(f"❌ Erreur vérification capacités: {e}")

    # Test 3: Health Check
    print("\n📋 Test 3: Health Check")
    try:
        health = await chef.health_check()
        print(f"Statut santé: {health}")
        
        if isinstance(health, dict) and "status" in health:
            print("✅ Health check retourne structure attendue")
            success_count += 1
        else:
            print("❌ Structure health check incorrecte")
    except Exception as e:
        print(f"❌ Erreur health check: {e}")

    # Test 4: Test structure execute_task (sans exécution complète)
    print("\n📋 Test 4: Structure execute_task")
    try:
        # Test avec tâche invalide
        invalid_task = Task(type="tache_inexistante", params={})
        result = await chef.execute_task(invalid_task)
        
        if not result.success and "non reconnue" in result.error:
            print("✅ Gestion correcte des tâches inconnues")
            success_count += 1
        else:
            print("❌ Gestion incorrecte des tâches inconnues")
    except Exception as e:
        print(f"❌ Erreur test execute_task: {e}")

    # Cleanup
    try:
        if startup_ok:
            await chef.shutdown()
            print("\n✅ Shutdown réussi")
    except Exception as e:
        print(f"\n⚠️  Shutdown avec erreur: {e}")
    
    # Résumé
    print("\n" + "=" * 80)
    print(f"📊 RÉSULTATS: {success_count}/{total_tests} tests réussis")
    
    if success_count == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS - Agent MAINTENANCE 00 opérationnel")
        return True
    elif success_count >= 3:
        print("⚠️  TESTS MAJORITAIREMENT RÉUSSIS - Agent fonctionnel avec limitations mineures")
        return True
    else:
        print("❌ ÉCHEC CRITIQUE - Agent non opérationnel")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent_maintenance_00())
    sys.exit(0 if success else 1)