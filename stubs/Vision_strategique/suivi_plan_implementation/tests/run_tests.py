#!/usr/bin/env python3
"""
Script d'exécution des tests de migration
"""
import os
import sys
import pytest
from pathlib import Path

def main():
    """Point d'entrée principal"""
    # Configuration environnement
    os.environ["PYTHONPATH"] = str(Path(__file__).parent)
    os.environ["TEST_ENV"] = "validation"
    os.environ["LOG_LEVEL"] = "INFO"
    
    # Exécution des tests
    test_file = Path(__file__).parent / "test_agent_05_migration.py"
    if not test_file.exists():
        print(f"❌ Fichier de test non trouvé: {test_file}")
        sys.exit(1)
        
    print(f"🧪 Exécution des tests depuis {test_file}")
    sys.exit(pytest.main(["-v", str(test_file)]))

if __name__ == "__main__":
    main() 