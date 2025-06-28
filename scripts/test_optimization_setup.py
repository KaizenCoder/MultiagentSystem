#!/usr/bin/env python3
"""
Script de Test - Setup Optimisations Équipe Maintenance
NextGeneration - Validation Infrastructure

Ce script teste et valide tous les composants d'optimisation :
- Configuration centralisée
- Collecteur de métriques
- Circuit breaker
- Cache intelligent
- Intégration complète
"""

import asyncio
import time
import random
from pathlib import Path

# Configuration du logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_configuration():
    """Test de la configuration centralisée"""
    print("🔧 Test Configuration Centralisée")
    print("-" * 50)
    
    try:
        from core.monitoring.config_manager import MaintenanceConfig
        
        # Chargement de la configuration
        config = MaintenanceConfig.from_yaml('config/maintenance_optimization_config.yaml')
        print(f"✅ Configuration chargée: {len(config.team_config)} agents")
        
        # Validation
        validation = config.validate_configuration()
        print(f"✅ Validation: {len(validation['errors'])} erreurs, {len(validation['warnings'])} avertissements")
        
        # Test d'accès aux configurations
        chef_config = config.get_agent_config("chef_equipe")
        print(f"✅ Config Chef d'Équipe: parallélisme={chef_config.parallel_processing}, sémaphore={chef_config.semaphore_limit}")
        
        # Configuration globale
        global_config = config.global_settings
        print(f"✅ Config Globale: cache_ttl={global_config.cache_ttl}, monitoring={global_config.performance_monitoring}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur configuration: {e}")
        return False

async def test_metrics_collector():
    """Test du collecteur de métriques"""
    print("\n📊 Test Collecteur de Métriques")
    print("-" * 50)
    
    try:
        from core.monitoring.metrics_collector import AdvancedMetricsCollector, monitor_performance
        
        # Création du collecteur
        collector = AdvancedMetricsCollector()
        print("✅ Collecteur créé")
        
        # Simulation d'exécutions
        for i in range(10):
            agent_id = f"agent_test_{random.randint(1, 3)}"
            duration = random.uniform(0.5, 3.0)
            success = random.choice([True, True, True, False])  # 75% succès
            memory = random.randint(50, 150) * 1024 * 1024  # 50-150MB
            
            collector.record_execution(agent_id, duration, success, memory, f"task_{i}")
        
        print("✅ 10 exécutions simulées enregistrées")
        
        # Dashboard
        dashboard = collector.get_dashboard_data()
        print(f"✅ Dashboard: {dashboard['global_metrics']['total_executions']} exécutions")
        print(f"   Taux de succès: {dashboard['global_metrics']['global_success_rate']}")
        print(f"   Agents actifs: {dashboard['global_metrics']['active_agents']}")
        
        # Test du décorateur
        @monitor_performance(collector)
        async def test_function(self):
            await asyncio.sleep(0.1)
            return {"result": "success"}
        
        # Simulation d'une classe agent
        class TestAgent:
            def __init__(self):
                self.agent_id = "test_agent_decorator"
        
        test_agent = TestAgent()
        result = await test_function(test_agent)
        print("✅ Décorateur @monitor_performance testé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur métriques: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_circuit_breaker():
    """Test du circuit breaker"""
    print("\n🔄 Test Circuit Breaker")
    print("-" * 50)
    
    try:
        from core.monitoring.circuit_breaker import CircuitBreaker, CircuitBreakerOpenException
        
        # Création du circuit breaker
        cb = CircuitBreaker(failure_threshold=3, timeout_seconds=2)
        print("✅ Circuit breaker créé")
        
        # Fonction de test qui échoue parfois
        async def test_function():
            if random.random() < 0.6:  # 60% d'échec
                raise Exception("Erreur simulée")
            return "Succès"
        
        # Test avec échecs
        success_count = 0
        failure_count = 0
        circuit_open_count = 0
        
        for i in range(15):
            try:
                result = await cb.call(test_function)
                success_count += 1
                print(f"   ✅ Appel {i+1}: {result}")
            except CircuitBreakerOpenException:
                circuit_open_count += 1
                print(f"   🚨 Appel {i+1}: Circuit ouvert")
            except Exception:
                failure_count += 1
                print(f"   ❌ Appel {i+1}: Échec")
            
            await asyncio.sleep(0.1)
        
        # Métriques
        metrics = cb.get_metrics()
        print(f"✅ Métriques: {success_count} succès, {failure_count} échecs, {circuit_open_count} circuit ouvert")
        print(f"   Disponibilité: {metrics['availability']:.1f}%")
        print(f"   Score fiabilité: {metrics['reliability_score']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur circuit breaker: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_cache():
    """Test du cache intelligent"""
    print("\n💾 Test Cache Intelligent")
    print("-" * 50)
    
    try:
        from core.monitoring.cache_manager import IntelligentCache, cached
        
        # Création du cache (mode mémoire pour les tests)
        cache = IntelligentCache(enable_redis=False, max_memory_items=100)
        print("✅ Cache créé (mode mémoire)")
        
        # Test basique
        await cache.set("test_key", {"data": "test_value", "timestamp": time.time()})
        result = await cache.get("test_key")
        print(f"✅ Test basique: {result is not None}")
        
        # Test avec namespace
        await cache.set("user:123", {"name": "John", "role": "tester"}, namespace="users")
        user = await cache.get("user:123", namespace="users")
        print(f"✅ Test namespace: {user['name'] if user else 'None'}")
        
        # Simulation de charge pour tester le hit rate
        for i in range(50):
            await cache.set(f"key_{i}", f"value_{i}")
            
            # Quelques récupérations pour générer des hits
            if i % 5 == 0 and i > 0:
                await cache.get(f"key_{i-2}")
                await cache.get(f"key_{i-1}")
        
        print("✅ 50 opérations de cache simulées")
        
        # Statistiques
        stats = cache.get_stats()
        print(f"   Hit rate: {stats['hit_rate']}")
        print(f"   Items en mémoire: {stats['memory_items']}")
        print(f"   Temps d'accès moyen: {stats['avg_access_time_ms']:.2f}ms")
        
        # Test du décorateur @cached
        @cached(ttl=60, namespace="functions")
        async def expensive_function(param):
            await asyncio.sleep(0.1)  # Simulation calcul coûteux
            return f"result_for_{param}"
        
        # Premier appel (miss)
        start = time.time()
        result1 = await expensive_function("test")
        time1 = time.time() - start
        
        # Deuxième appel (hit)
        start = time.time()
        result2 = await expensive_function("test")
        time2 = time.time() - start
        
        speedup = time1/time2 if time2 > 0 else float('inf')
        print(f"✅ Décorateur @cached: {time1:.3f}s vs {time2:.3f}s (speedup: {speedup:.1f}x)")
        
        # État de santé
        health = cache.get_health_status()
        print(f"✅ Santé du cache: {health['health_status']} (Score: {health['health_score']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur cache: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_integration():
    """Test d'intégration complète"""
    print("\n🚀 Test d'Intégration Complète")
    print("-" * 50)
    
    try:
        from core.monitoring.config_manager import MaintenanceConfig
        from core.monitoring.metrics_collector import AdvancedMetricsCollector
        from core.monitoring.circuit_breaker import CircuitBreaker
        from core.monitoring.cache_manager import IntelligentCache
        
        # Chargement de la configuration
        config = MaintenanceConfig.from_yaml('config/maintenance_optimization_config.yaml')
        
        # Initialisation des composants
        metrics = AdvancedMetricsCollector()
        cache = IntelligentCache(enable_redis=False)
        
        # Configuration des circuit breakers par agent
        circuit_breakers = {}
        for agent_name, agent_config in config.team_config.items():
            circuit_breakers[agent_name] = CircuitBreaker(
                failure_threshold=agent_config.circuit_breaker_threshold,
                timeout_seconds=agent_config.timeout_seconds
            )
        
        print(f"✅ Intégration: {len(circuit_breakers)} circuit breakers configurés")
        
        # Simulation d'un workflow d'agent
        async def simulate_agent_workflow(agent_name: str):
            """Simule le workflow d'un agent avec tous les composants"""
            
            # Récupération de la configuration
            agent_config = config.get_agent_config(agent_name)
            cb = circuit_breakers[agent_name]
            
            # Simulation de tâche avec cache
            cache_key = f"agent_task_{agent_name}_{time.time()}"
            
            # Vérification cache
            cached_result = await cache.get(cache_key, namespace="agent_tasks")
            if cached_result:
                metrics.record_execution(agent_name, 0.01, True, 1024*1024, "cached_task")
                return cached_result
            
            # Exécution avec circuit breaker
            async def agent_task():
                # Simulation de travail
                await asyncio.sleep(random.uniform(0.1, 0.5))
                
                # Simulation d'échec parfois
                if random.random() < 0.2:  # 20% d'échec
                    raise Exception(f"Erreur simulée dans {agent_name}")
                
                return {"status": "success", "agent": agent_name, "timestamp": time.time()}
            
            try:
                start_time = time.time()
                result = await cb.call(agent_task)
                duration = time.time() - start_time
                
                # Mise en cache du résultat
                await cache.set(cache_key, result, ttl=300, namespace="agent_tasks")
                
                # Enregistrement des métriques
                metrics.record_execution(agent_name, duration, True, random.randint(1, 5)*1024*1024, "workflow_task")
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                metrics.record_execution(agent_name, duration, False, random.randint(1, 3)*1024*1024, "workflow_task")
                raise
        
        # Simulation de plusieurs agents en parallèle
        agent_names = list(config.team_config.keys())[:5]  # Test avec 5 agents
        tasks = [simulate_agent_workflow(name) for name in agent_names]
        
        print(f"🚀 Simulation de {len(tasks)} agents en parallèle...")
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Analyse des résultats
        successful = sum(1 for r in results if not isinstance(r, Exception))
        failed = len(results) - successful
        
        print(f"✅ Résultats: {successful} succès, {failed} échecs")
        
        # Dashboard global
        dashboard = metrics.get_dashboard_data()
        print(f"✅ Métriques globales:")
        print(f"   Total exécutions: {dashboard['global_metrics']['total_executions']}")
        print(f"   Taux de succès: {dashboard['global_metrics']['global_success_rate']}")
        print(f"   Agents actifs: {dashboard['global_metrics']['active_agents']}")
        
        # Statistiques de cache
        cache_stats = cache.get_stats()
        print(f"✅ Cache: {cache_stats['hit_rate']} hit rate, {cache_stats['memory_items']} items")
        
        # États des circuit breakers
        healthy_circuits = sum(1 for cb in circuit_breakers.values() if cb.get_state()['state'] == 'closed')
        print(f"✅ Circuit breakers: {healthy_circuits}/{len(circuit_breakers)} en état sain")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur intégration: {e}")
        import traceback
        traceback.print_exc()
        return False

async def run_all_tests():
    """Exécute tous les tests"""
    print("🧪 TESTS D'OPTIMISATION - ÉQUIPE MAINTENANCE NEXTGENERATION")
    print("=" * 70)
    
    results = []
    
    # Tests individuels
    results.append(("Configuration", test_configuration()))
    results.append(("Métriques", await test_metrics_collector()))
    results.append(("Circuit Breaker", await test_circuit_breaker()))
    results.append(("Cache", await test_cache()))
    results.append(("Intégration", await test_integration()))
    
    # Résumé
    print("\n" + "=" * 70)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHEC"
        print(f"{status:10} | {test_name}")
        if result:
            passed += 1
    
    print("-" * 70)
    print(f"TOTAL: {passed}/{total} tests réussis ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("🚀 Infrastructure d'optimisation prête pour l'implémentation!")
        print("\n📋 Prochaines étapes:")
        print("  1. Implémentation du Chef d'Équipe parallèle")
        print("  2. Optimisation de l'Adaptateur Code avec cache")
        print("  3. Tests de performance en conditions réelles")
        print("  4. Monitoring et alertes en production")
    else:
        print(f"\n⚠️ {total-passed} test(s) ont échoué - Correction nécessaire avant implémentation")
    
    return passed == total

if __name__ == "__main__":
    # Exécution des tests
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1) 