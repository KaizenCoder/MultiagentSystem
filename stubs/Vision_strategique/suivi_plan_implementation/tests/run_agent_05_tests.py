#!/usr/bin/env python3
"""
Script d'exécution des tests de migration Agent 05
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Point d'entrée principal"""
    # Configuration environnement
    os.environ["PYTHONPATH"] = str(Path(__file__).parent)
    os.environ["TEST_ENV"] = "validation"
    os.environ["LOG_LEVEL"] = "INFO"
    
    # Chemin du fichier de test
    test_file = Path(__file__).parent / "test_agent_05_migration_final.py"
    
    if not test_file.exists():
        print(f"❌ Fichier de test non trouvé: {test_file}")
        sys.exit(1)
    
    print(f"🧪 Exécution des tests Agent 05 depuis {test_file}")
    print("=" * 60)
    
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
            print("✅ Tests Agent 05 terminés avec succès")
        else:
            print(f"❌ Tests Agent 05 échoués (code: {result.returncode})")
            
        return result.returncode
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution des tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())