#!/usr/bin/env python3
"""
🧪 TESTS AGENTS RÉELS AUTONOMES
Agent Factory Pattern - Sprint 4

Tests de validation pour les agents autonomes
"""

import asyncio
import sys
import time
from pathlib import Path

# Ajouter le répertoire agents au path
AGENTS_DIR = Path(__file__).parent / "agents"
sys.path.insert(0, str(AGENTS_DIR))

async def test_agent_08_performance():
    """Test Agent 08 - Performance Optimizer"""
    print("🧪 Test Agent 08 - Performance Optimizer")
    print("-" * 40)
    
    try:
        from real_agent_08_performance_optimizer import RealAgent08PerformanceOptimizer
        
        # Créer agent
        agent = RealAgent08PerformanceOptimizer()
        print(f"✅ Agent créé: {agent.agent_name} v{agent.version}")
        
        # Test compression
        test_data = {
            "id": "test_template_001",
            "name": "Test Template",
            "version": "1.0.0",
            "config": {"param1": "value1", "param2": "value2"}
        }
        
        compressed = await agent.compress_template(test_data)
        print(f"✅ Compression OK: {len(compressed)} bytes")
        
        # Test traitement template
        result = await agent.process_template_request(test_data)
        print(f"✅ Traitement template: {result['processing_time_ms']:.1f}ms")
        
        # Test collecte métriques
        state = await agent.collect_performance_metrics()
        if state:
            print(f"✅ Métriques collectées: CPU={state.cpu_usage:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test Agent 08: {e}")
        return False

async def test_agent_12_backup():
    """Test Agent 12 - Backup Manager"""
    print("\n🧪 Test Agent 12 - Backup Manager")
    print("-" * 40)
    
    try:
        from real_agent_12_backup_manager import RealAgent12BackupManager
        
        # Créer agent
        agent = RealAgent12BackupManager()
        print(f"✅ Agent créé: {agent.agent_name} v{agent.version}")
        
        # Test création backup
        metadata = await agent.create_backup(
            backup_type="test",
            description="Test backup validation"
        )
        
        if metadata:
            print(f"✅ Backup créé: {metadata.backup_id}")
            print(f"   - Fichiers: {metadata.file_count}")
            print(f"   - Taille: {metadata.total_size_bytes/1024:.1f}KB")
            print(f"   - Checksum: {metadata.checksum_sha256[:16]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test Agent 12: {e}")
        return False

async def test_integration():
    """Test intégration agents"""
    print("\n🧪 Test Intégration Multi-Agents")
    print("-" * 40)
    
    try:
        from real_agent_08_performance_optimizer import RealAgent08PerformanceOptimizer
        from real_agent_12_backup_manager import RealAgent12BackupManager
        
        # Créer agents
        agent08 = RealAgent08PerformanceOptimizer()
        agent12 = RealAgent12BackupManager()
        
        print("✅ Agents créés")
        
        # Test parallèle
        tasks = [
            agent08.collect_performance_metrics(),
            agent12.create_backup("integration", "Test intégration")
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = sum(1 for r in results if not isinstance(r, Exception))
        print(f"✅ Tâches parallèles: {success_count}/{len(tasks)} réussies")
        
        return success_count == len(tasks)
        
    except Exception as e:
        print(f"❌ Erreur test intégration: {e}")
        return False

async def main():
    """Tests principaux"""
    print("🚀 TESTS AGENTS RÉELS AUTONOMES")
    print("=" * 50)
    
    # Vérifier dépendances
    try:
        import psutil
        import zstandard
        import prometheus_client
        print("✅ Dépendances OK")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        return
    
    # Tests
    results = []
    
    # Test Agent 08
    results.append(await test_agent_08_performance())
    
    # Test Agent 12
    results.append(await test_agent_12_backup())
    
    # Test intégration
    results.append(await test_integration())
    
    # Résultats
    print("\n📊 RÉSULTATS TESTS")
    print("=" * 30)
    
    success_count = sum(results)
    total_tests = len(results)
    
    print(f"✅ Tests réussis: {success_count}/{total_tests}")
    print(f"📈 Taux de réussite: {success_count/total_tests*100:.1f}%")
    
    if success_count == total_tests:
        print("\n🎉 TOUS LES TESTS PASSÉS!")
        print("✅ Les agents réels sont fonctionnels")
    else:
        print("\n⚠️ Certains tests ont échoué")
        print("🔧 Vérifiez les logs pour plus de détails")

if __name__ == "__main__":
    asyncio.run(main()) 



