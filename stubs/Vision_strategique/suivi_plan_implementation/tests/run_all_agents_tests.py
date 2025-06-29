#!/usr/bin/env python3
"""
Script d'exécution de tous les tests de migration des agents
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def run_agent_tests(agent_file, agent_name):
    """Exécute les tests pour un agent spécifique"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTS {agent_name}")
    print(f"{'='*60}")
    
    test_file = Path(__file__).parent / agent_file
    
    if not test_file.exists():
        print(f"❌ Fichier de test non trouvé: {test_file}")
        return False
    
    try:
        # Exécution avec pytest
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            str(test_file), 
            "-v", 
            "--tb=short",
            "--log-cli-level=INFO"
        ], check=False, capture_output=False)
        
        if result.returncode == 0:
            print(f"✅ Tests {agent_name} terminés avec succès")
            return True
        else:
            print(f"❌ Tests {agent_name} échoués (code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution des tests {agent_name}: {e}")
        return False

def main():
    """Point d'entrée principal"""
    print("🚀 LANCEMENT DES TESTS DE MIGRATION - TOUS LES AGENTS")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Répertoire: {Path(__file__).parent}")
    
    # Configuration environnement
    os.environ["PYTHONPATH"] = str(Path(__file__).parent)
    os.environ["TEST_ENV"] = "validation"
    os.environ["LOG_LEVEL"] = "INFO"
    
    # Agents à tester
    agents_tests = [
        ("test_agent_05_migration_final.py", "AGENT 05 - TESTING"),
        ("test_agent_111_audit.py", "AGENT 111 - AUDIT"),
        ("test_agent_00_coordination.py", "AGENT 00 - COORDINATION"),
        ("test_agent_109_factory.py", "AGENT 109 - FACTORY")
    ]
    
    # Exécution des tests
    results = {}
    start_time = datetime.now()
    
    for test_file, agent_name in agents_tests:
        success = run_agent_tests(test_file, agent_name)
        results[agent_name] = success
    
    end_time = datetime.now()
    total_duration = end_time - start_time
    
    # Rapport final
    print(f"\n{'='*60}")
    print("📊 RAPPORT FINAL DE MIGRATION")
    print(f"{'='*60}")
    
    success_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    print(f"⏱️  Durée totale: {total_duration}")
    print(f"📈 Taux de succès global: {success_count}/{total_count} ({success_count/total_count:.1%})")
    print()
    
    for agent_name, success in results.items():
        status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        print(f"  {status} - {agent_name}")
    
    print()
    
    if success_count == total_count:
        print("🎉 TOUS LES AGENTS VALIDÉS POUR LA PRODUCTION")
        print("✅ Migration NextGeneration terminée avec succès")
        return 0
    else:
        print("⚠️  CERTAINS AGENTS NÉCESSITENT DES CORRECTIONS")
        print("❌ Migration NextGeneration incomplète")
        return 1

if __name__ == "__main__":
    sys.exit(main())