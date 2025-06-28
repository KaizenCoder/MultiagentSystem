#!/usr/bin/env python3
"""
Script de test pour l'Agent 05
"""
import os
import sys
import pytest

if __name__ == "__main__":
    # Ajout du répertoire de tests au PYTHONPATH
    test_dir = os.path.join(os.path.dirname(__file__), "tests", "migration")
    sys.path.insert(0, test_dir)
    
    # Configuration environnement
    os.environ["TEST_ENV"] = "validation"
    os.environ["LOG_LEVEL"] = "INFO"
    
    # Exécution des tests
    pytest.main(["-v", os.path.join(test_dir, "test_agent_05_migration.py")]) 