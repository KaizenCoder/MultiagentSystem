#!/usr/bin/env python3
"""
Tests Unitaires - Adaptateur de Code Optimisé
===========================================

Tests pour valider les optimisations LibCST et le cache intelligent.

Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
"""

import pytest
import asyncio
from pathlib import Path
import sys
import time

# Configuration du chemin d'importation
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from agents.agent_MAINTENANCE_03_adaptateur_code import AgentMAINTENANCE03AdaptateurCode
from core.agent_factory_architecture import Task, Result

@pytest.fixture
async def adaptateur():
    """Fixture pour l'adaptateur de code"""
    agent = AgentMAINTENANCE03AdaptateurCode()
    yield agent
    await agent.cleanup()

@pytest.mark.asyncio
async def test_optimized_pass_insertion(adaptateur):
    """Test l'insertion optimisée de 'pass'"""
    code = """
def test_function():
    if True:
    
    try:
        
    except Exception:
    """
    
    task = Task(
        task_type="adapt",
        params={
            "code": code,
            "error_type": "syntax",
            "feedback": "Empty blocks need pass statement"
        }
    )
    
    result = await adaptateur.execute_task(task)
    assert result.success
    assert "pass" in result.data["adapted_code"]
    assert result.data["metrics"]["total_time"] < 1.0  # Performance check

@pytest.mark.asyncio
async def test_import_optimization(adaptateur):
    """Test l'optimisation des imports"""
    code = """
def process_data(items: List[str]) -> Optional[Dict]:
    path = Path('test.txt')
    return None
"""
    
    task = Task(
        task_type="adapt",
        params={
            "code": code,
            "error_type": "undefined",
            "feedback": "Missing imports"
        }
    )
    
    result = await adaptateur.execute_task(task)
    assert result.success
    adapted_code = result.data["adapted_code"]
    assert "from typing import List, Optional, Dict" in adapted_code
    assert "from pathlib import Path" in adapted_code

@pytest.mark.asyncio
async def test_cache_efficiency(adaptateur):
    """Test l'efficacité du cache"""
    code = "print('test')"
    
    # Première exécution
    task = Task(
        task_type="adapt",
        params={"code": code, "error_type": "syntax"}
    )
    
    start_time = time.time()
    result1 = await adaptateur.execute_task(task)
    first_execution = time.time() - start_time
    
    # Deuxième exécution (devrait utiliser le cache)
    start_time = time.time()
    result2 = await adaptateur.execute_task(task)
    second_execution = time.time() - start_time
    
    assert second_execution < first_execution
    assert result2.data["metrics"]["cache_hits"] > 0

@pytest.mark.asyncio
async def test_indentation_error_handling(adaptateur):
    """Test la gestion des erreurs d'indentation"""
    code = """
def test():
   print("wrong indent")
  print("another wrong indent")
    """
    
    task = Task(
        task_type="adapt",
        params={
            "code": code,
            "error_type": "indentation",
            "feedback": "Inconsistent indentation"
        }
    )
    
    result = await adaptateur.execute_task(task)
    assert result.success
    assert "print(" in result.data["adapted_code"]
    assert len(result.data["adaptations"]) > 0

@pytest.mark.asyncio
async def test_transformation_pipeline_metrics(adaptateur):
    """Test les métriques du pipeline de transformation"""
    code = """
class TestClass:
    def empty_method():
    
    def another_empty():
        if True:
    """
    
    task = Task(
        task_type="adapt",
        params={"code": code, "error_type": "syntax"}
    )
    
    result = await adaptateur.execute_task(task)
    assert result.success
    assert "metrics" in result.data
    assert "total_time" in result.data["metrics"]
    assert "cache_hits" in result.data["metrics"]

@pytest.mark.asyncio
async def test_error_handling(adaptateur):
    """Test la gestion des erreurs"""
    task = Task(
        task_type="adapt",
        params={"code": None, "error_type": "syntax"}
    )
    
    result = await adaptateur.execute_task(task)
    assert not result.success
    assert "erreur" in result.error.lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 