#!/usr/bin/env python3
"""
Tests de Charge - Adaptateur de Code Optimisé
===========================================

Tests de performance et de charge pour valider :
- La scalabilité du pipeline LibCST
- L'efficacité du cache Redis
- La gestion mémoire sous charge

Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
"""

import pytest
import asyncio
from pathlib import Path
import sys
import time
import psutil
import asyncio
import random
import string
from typing import List, Dict
import gc
import logging

# Configuration du chemin d'importation
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from agents.agent_MAINTENANCE_03_adaptateur_code import AgentMAINTENANCE03AdaptateurCode
from core.agent_factory_architecture import Task, Result

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_test_code(size: int = 1000) -> str:
    """Génère du code Python de test avec la taille spécifiée"""
    templates = [
        "def function_{i}():\n    pass\n",
        "class Class_{i}:\n    def method_{i}(self):\n        pass\n",
        "try:\n    x_{i} = 1\nexcept Exception:\n    pass\n",
        "if True:\n    var_{i} = 'test'\n",
        "async def async_func_{i}():\n    await asyncio.sleep(0)\n"
    ]
    
    code_parts = []
    while len(''.join(code_parts)) < size:
        template = random.choice(templates)
        i = len(code_parts)
        code_parts.append(template.format(i=i))
    
    return ''.join(code_parts)

def get_memory_usage() -> float:
    """Retourne l'utilisation mémoire en MB"""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024

@pytest.fixture
async def adaptateur():
    """Fixture pour l'adaptateur de code"""
    agent = AgentMAINTENANCE03AdaptateurCode()
    yield agent
    await agent.cleanup()
    gc.collect()  # Force garbage collection

async def run_batch(adaptateur, batch_size: int, code_size: int) -> Dict:
    """Exécute un batch de tâches"""
    tasks = []
    for _ in range(batch_size):
        code = generate_test_code(code_size)
        task = Task(
            task_type="adapt",
            params={
                "code": code,
                "error_type": random.choice(["syntax", "indentation", "undefined"]),
                "feedback": "Test load"
            }
        )
        tasks.append(adaptateur.execute_task(task))
    
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    duration = time.time() - start_time
    
    success_count = sum(1 for r in results if r.success)
    cache_hits = sum(r.data["metrics"]["cache_hits"] for r in results if r.success)
    
    return {
        "duration": duration,
        "success_rate": success_count / batch_size * 100,
        "cache_hits": cache_hits,
        "avg_time": duration / batch_size
    }

@pytest.mark.asyncio
async def test_concurrent_load(adaptateur):
    """Test de charge avec exécution concurrente"""
    batch_sizes = [10, 20, 50]
    code_sizes = [1000, 5000, 10000]
    
    logger.info("🔄 Démarrage test de charge concurrent...")
    initial_memory = get_memory_usage()
    
    for batch_size in batch_sizes:
        for code_size in code_sizes:
            logger.info(f"📊 Test batch={batch_size}, code_size={code_size}")
            
            metrics = await run_batch(adaptateur, batch_size, code_size)
            current_memory = get_memory_usage()
            memory_diff = current_memory - initial_memory
            
            logger.info(
                f"✓ Durée: {metrics['duration']:.2f}s, "
                f"Succès: {metrics['success_rate']:.1f}%, "
                f"Cache: {metrics['cache_hits']}, "
                f"Mémoire: {memory_diff:.1f}MB"
            )
            
            # Validations
            assert metrics["success_rate"] > 90, "Taux de succès trop faible"
            assert metrics["avg_time"] < 2.0, "Temps moyen trop élevé"
            assert memory_diff < 500, "Consommation mémoire trop élevée"
            
            # Pause pour stabilisation
            await asyncio.sleep(1)
            gc.collect()

@pytest.mark.asyncio
async def test_cache_efficiency_under_load(adaptateur):
    """Test d'efficacité du cache sous charge"""
    logger.info("🔄 Test efficacité cache sous charge...")
    
    # Génération code avec motifs répétitifs
    base_code = generate_test_code(1000)
    variants = []
    for i in range(20):
        variant = base_code.replace("pass", f"pass  # variant {i}")
        variants.append(variant)
    
    # Premier passage - remplissage cache
    tasks = []
    for code in variants:
        task = Task(
            task_type="adapt",
            params={"code": code, "error_type": "syntax"}
        )
        tasks.append(adaptateur.execute_task(task))
    
    results1 = await asyncio.gather(*tasks)
    
    # Deuxième passage - devrait utiliser le cache
    tasks = []
    for code in variants:
        task = Task(
            task_type="adapt",
            params={"code": code, "error_type": "syntax"}
        )
        tasks.append(adaptateur.execute_task(task))
    
    results2 = await asyncio.gather(*tasks)
    
    # Analyse résultats
    cache_hits = sum(r.data["metrics"]["cache_hits"] for r in results2 if r.success)
    logger.info(f"✓ Cache hits: {cache_hits}")
    
    assert cache_hits > len(variants) * 0.8, "Taux de cache hits trop faible"

@pytest.mark.asyncio
async def test_memory_stability(adaptateur):
    """Test stabilité mémoire sur longue durée"""
    logger.info("🔄 Test stabilité mémoire...")
    
    initial_memory = get_memory_usage()
    iterations = 5
    batch_size = 30
    
    for i in range(iterations):
        logger.info(f"📊 Itération {i+1}/{iterations}")
        metrics = await run_batch(adaptateur, batch_size, 5000)
        
        current_memory = get_memory_usage()
        memory_diff = current_memory - initial_memory
        
        logger.info(f"✓ Mémoire: {memory_diff:.1f}MB")
        assert memory_diff < 200, f"Fuite mémoire détectée: {memory_diff:.1f}MB"
        
        # Nettoyage entre itérations
        gc.collect()
        await asyncio.sleep(1)

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 