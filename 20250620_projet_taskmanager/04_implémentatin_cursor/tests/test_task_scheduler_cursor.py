#!/usr/bin/env python3
"""
Test Task Scheduler Cursor - Validation complète
Tests d'intégration pour l'ordonnanceur TaskMaster NextGeneration
"""

import asyncio
import json
import os
import sqlite3
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import du module à tester
from task_scheduler_cursor import TaskSchedulerCursor, RTX3090Optimizer, PostgreSQLManager

class TestRTX3090Optimizer(unittest.TestCase):
    """Tests pour l'optimiseur GPU RTX3090"""
    
    def setUp(self):
        self.optimizer = RTX3090Optimizer()
    
    def test_gpu_availability_check(self):
        """Test détection GPU"""
        # Le test dépend de la présence réelle du GPU
        status = self.optimizer.get_gpu_status()
        self.assertIn('available', status)
        self.assertIn('load', status)
        self.assertIn('temperature', status)
    
    def test_optimal_conditions_logic(self):
        """Test logique conditions optimales"""
        # Mock du statut GPU
        with patch.object(self.optimizer, 'get_gpu_status') as mock_status:
            # GPU optimal
            mock_status.return_value = {
                'available': True,
                'load': 50,
                'temperature': 70,
                'memory_used': 1000
            }
            self.assertTrue(self.optimizer.is_optimal_for_task())
            
            # GPU occupé
            mock_status.return_value = {
                'available': True,
                'load': 90,
                'temperature': 85,
                'memory_used': 2000
            }
            self.assertFalse(self.optimizer.is_optimal_for_task())
            
            # GPU indisponible
            mock_status.return_value = {
                'available': False,
                'load': 0,
                'temperature': 0,
                'memory_used': 0
            }
            self.assertFalse(self.optimizer.is_optimal_for_task())

class TestPostgreSQLManager(unittest.TestCase):
    """Tests pour le gestionnaire PostgreSQL/SQLite"""
    
    def setUp(self):
        # Utiliser un fichier SQLite temporaire pour les tests
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, 'test_scheduler.db')
        
        # Créer un manager avec base de test
        self.manager = PostgreSQLManager()
        self.manager.sqlite_path = self.test_db_path
        self.manager.pg_available = False  # Forcer SQLite pour les tests
        self.manager._ensure_sqlite_db()
    
    def tearDown(self):
        # Nettoyer les fichiers temporaires
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        os.rmdir(self.temp_dir)
    
    def test_sqlite_database_creation(self):
        """Test création base SQLite"""
        self.assertTrue(os.path.exists(self.test_db_path))
        
        # Vérifier structure table
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='task_queue'")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'task_queue')
    
    def test_add_task_to_queue(self):
        """Test ajout tâche"""
        mission = "Test mission d'intégration"
        priority = 8
        
        task_id = self.manager.add_task_to_queue(mission, priority)
        
        self.assertIsInstance(task_id, int)
        self.assertGreater(task_id, 0)
        
        # Vérifier en base
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT mission, priority FROM task_queue WHERE id = ?", (task_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertEqual(result[0], mission)
        self.assertEqual(result[1], priority)
    
    def test_get_next_task_priority(self):
        """Test récupération par priorité"""
        # Ajouter plusieurs tâches avec priorités différentes
        tasks = [
            ("Tâche basse priorité", 3),
            ("Tâche haute priorité", 9),
            ("Tâche moyenne priorité", 5)
        ]
        
        for mission, priority in tasks:
            self.manager.add_task_to_queue(mission, priority)
        
        # La prochaine tâche doit être celle de priorité 9
        next_task = self.manager.get_next_task()
        self.assertIsNotNone(next_task)
        self.assertEqual(next_task['priority'], 9)
        self.assertEqual(next_task['mission'], "Tâche haute priorité")
    
    def test_update_task_status(self):
        """Test mise à jour statut"""
        task_id = self.manager.add_task_to_queue("Test update", 5)
        
        # Marquer comme en cours
        self.manager.update_task_status(task_id, 'running')
        
        # Vérifier
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM task_queue WHERE id = ?", (task_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertEqual(result[0], 'running')
        
        # Marquer comme terminé
        result_data = '{"status": "completed", "confidence": 0.95}'
        self.manager.update_task_status(task_id, 'completed', result_data)
        
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT status, result FROM task_queue WHERE id = ?", (task_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertEqual(result[0], 'completed')
        self.assertEqual(result[1], result_data)
    
    def test_queue_statistics(self):
        """Test statistiques file d'attente"""
        # Ajouter des tâches avec différents statuts
        task1 = self.manager.add_task_to_queue("Tâche 1", 5)
        task2 = self.manager.add_task_to_queue("Tâche 2", 5)
        task3 = self.manager.add_task_to_queue("Tâche 3", 5)
        
        self.manager.update_task_status(task1, 'completed')
        self.manager.update_task_status(task2, 'failed', error="Test error")
        # task3 reste 'pending'
        
        stats = self.manager.get_queue_stats()
        
        self.assertEqual(stats['pending'], 1)
        self.assertEqual(stats['completed'], 1)
        self.assertEqual(stats['failed'], 1)
        self.assertEqual(stats['total'], 3)

class TestTaskSchedulerCursor(unittest.TestCase):
    """Tests pour l'ordonnanceur principal"""
    
    def setUp(self):
        # Créer un scheduler avec base temporaire
        self.temp_dir = tempfile.mkdtemp()
        self.scheduler = TaskSchedulerCursor()
        self.scheduler.db_manager.sqlite_path = os.path.join(self.temp_dir, 'test_scheduler.db')
        self.scheduler.db_manager.pg_available = False
        self.scheduler.db_manager._ensure_sqlite_db()
    
    def tearDown(self):
        # Nettoyer
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_add_mission(self):
        """Test ajout mission"""
        mission = "Mission de test TaskScheduler"
        priority = 7
        
        task_id = self.scheduler.add_mission(mission, priority)
        
        self.assertIsInstance(task_id, int)
        self.assertGreater(task_id, 0)
    
    def test_infrastructure_validation(self):
        """Test validation infrastructure"""
        is_valid, issues = self.scheduler.validate_infrastructure()
        
        # Le résultat dépend de l'environnement, mais la fonction doit retourner des types corrects
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(issues, list)
        
        # Vérifier que les répertoires sont créés
        for dir_name in ['logs', 'data', 'reports']:
            self.assertTrue(Path(dir_name).exists())
    
    def test_missions_file_creation(self):
        """Test création fichier missions"""
        test_file = os.path.join(self.temp_dir, 'test_missions.json')
        
        created_file = self.scheduler.create_example_missions_file(test_file)
        
        self.assertEqual(created_file, test_file)
        self.assertTrue(os.path.exists(test_file))
        
        # Vérifier contenu
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIn('missions', data)
        self.assertIsInstance(data['missions'], list)
        self.assertGreater(len(data['missions']), 0)
        
        # Vérifier structure première mission
        first_mission = data['missions'][0]
        self.assertIn('mission', first_mission)
        self.assertIn('priority', first_mission)
    
    def test_missions_from_file_loading(self):
        """Test chargement missions depuis fichier"""
        test_file = os.path.join(self.temp_dir, 'test_load_missions.json')
        
        # Créer fichier test
        test_missions = {
            "missions": [
                {"mission": "Mission test 1", "priority": 8},
                {"mission": "Mission test 2", "priority": 6},
                "Mission test 3 (string simple)"
            ]
        }
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_missions, f)
        
        # Charger
        task_ids = self.scheduler.add_missions_from_file(test_file)
        
        self.assertEqual(len(task_ids), 3)
        self.assertTrue(all(isinstance(tid, int) for tid in task_ids))
    
    def test_status_reporting(self):
        """Test rapport de statut"""
        # Ajouter quelques tâches
        self.scheduler.add_mission("Test status 1", 5)
        self.scheduler.add_mission("Test status 2", 8)
        
        status = self.scheduler.get_status()
        
        # Vérifier structure
        required_keys = ['scheduler', 'queue', 'gpu', 'system', 'stats', 'database']
        for key in required_keys:
            self.assertIn(key, status)
        
        # Vérifier données queue
        self.assertGreaterEqual(status['queue']['pending'], 2)
        self.assertGreaterEqual(status['queue']['total'], 2)
        
        # Vérifier stats
        self.assertIn('tasks_processed', status['stats'])
        self.assertIn('start_time', status['stats'])
    
    async def test_task_execution_simulation(self):
        """Test simulation exécution tâche"""
        # Créer une tâche simulée
        task = {
            'id': 1,
            'mission': 'Mission de test exécution',
            'priority': 5,
            'status': 'pending'
        }
        
        # Exécuter
        success, result = await self.scheduler.execute_task(task)
        
        self.assertTrue(success)
        self.assertIsInstance(result, str)
        
        # Vérifier que le résultat est du JSON valide
        result_data = json.loads(result)
        self.assertIn('status', result_data)
        self.assertIn('execution_time', result_data)
        self.assertEqual(result_data['status'], 'completed')

class TestIntegrationTaskScheduler(unittest.TestCase):
    """Tests d'intégration complets"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.scheduler = TaskSchedulerCursor()
        self.scheduler.db_manager.sqlite_path = os.path.join(self.temp_dir, 'integration_test.db')
        self.scheduler.db_manager.pg_available = False
        self.scheduler.db_manager._ensure_sqlite_db()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    async def test_full_workflow(self):
        """Test workflow complet : ajout -> traitement -> rapport"""
        # 1. Ajouter des missions
        missions = [
            ("Mission critique", 9),
            ("Mission normale", 5),
            ("Mission basse", 2)
        ]
        
        task_ids = []
        for mission, priority in missions:
            task_id = self.scheduler.add_mission(mission, priority)
            task_ids.append(task_id)
        
        # 2. Vérifier file d'attente
        stats_before = self.scheduler.db_manager.get_queue_stats()
        self.assertEqual(stats_before['pending'], 3)
        self.assertEqual(stats_before['total'], 3)
        
        # 3. Traiter une tâche (simulation rapide)
        with patch.object(self.scheduler, 'execute_task') as mock_execute:
            mock_execute.return_value = (True, '{"status": "completed", "confidence": 0.95}')
            
            # Traiter max 1 tâche
            await self.scheduler.process_queue(max_tasks=1, timeout=10)
        
        # 4. Vérifier résultats
        stats_after = self.scheduler.db_manager.get_queue_stats()
        self.assertEqual(stats_after['pending'], 2)  # 2 restantes
        self.assertEqual(stats_after['completed'], 1)  # 1 terminée
        
        # 5. Vérifier que la tâche de priorité 9 a été traitée en premier
        completed_task = self.scheduler.db_manager._get_next_task_sqlite()
        # La prochaine doit être priorité 5 (la priorité 9 a été traitée)
        self.assertEqual(completed_task['priority'], 5)
        
        # 6. Générer rapport
        report_path = self.scheduler.generate_report()
        self.assertTrue(os.path.exists(report_path))
        
        # Vérifier contenu rapport
        with open(report_path, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        self.assertIn('Task Scheduler Cursor', report_content)
        self.assertIn('Tâches traitées:', report_content)
        self.assertIn('File d\'Attente', report_content)

def run_performance_test():
    """Test de performance basique"""
    print("\n🚀 Test de Performance Task Scheduler")
    print("=" * 50)
    
    # Créer scheduler temporaire
    temp_dir = tempfile.mkdtemp()
    scheduler = TaskSchedulerCursor()
    scheduler.db_manager.sqlite_path = os.path.join(temp_dir, 'perf_test.db')
    scheduler.db_manager.pg_available = False
    scheduler.db_manager._ensure_sqlite_db()
    
    try:
        # Test ajout masse
        start_time = time.time()
        num_tasks = 100
        
        for i in range(num_tasks):
            scheduler.add_mission(f"Mission performance {i}", priority=i % 10)
        
        add_time = time.time() - start_time
        
        # Test récupération
        start_time = time.time()
        retrieved_tasks = 0
        
        while True:
            task = scheduler.db_manager.get_next_task()
            if not task:
                break
            retrieved_tasks += 1
            scheduler.db_manager.update_task_status(task['id'], 'completed')
            
            if retrieved_tasks >= 10:  # Limiter pour le test
                break
        
        retrieve_time = time.time() - start_time
        
        # Statistiques
        stats = scheduler.db_manager.get_queue_stats()
        
        print(f"📊 Résultats Performance:")
        print(f"  - Ajout {num_tasks} tâches: {add_time:.3f}s ({num_tasks/add_time:.1f} tâches/s)")
        print(f"  - Traitement {retrieved_tasks} tâches: {retrieve_time:.3f}s ({retrieved_tasks/retrieve_time:.1f} tâches/s)")
        print(f"  - File d'attente finale: {stats['total']} tâches")
        print(f"  - Répartition: {stats['pending']} pending, {stats['completed']} completed")
        
    finally:
        # Nettoyer
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

async def run_integration_demo():
    """Démonstration d'intégration complète"""
    print("\n🎭 Démonstration Task Scheduler Cursor")
    print("=" * 50)
    
    # Créer scheduler temporaire
    temp_dir = tempfile.mkdtemp()
    scheduler = TaskSchedulerCursor()
    scheduler.db_manager.sqlite_path = os.path.join(temp_dir, 'demo.db')
    scheduler.db_manager.pg_available = False
    scheduler.db_manager._ensure_sqlite_db()
    
    try:
        print("1. 📝 Création fichier missions d'exemple...")
        missions_file = os.path.join(temp_dir, 'demo_missions.json')
        scheduler.create_example_missions_file(missions_file)
        print(f"   ✅ Créé: {missions_file}")
        
        print("\n2. 📥 Chargement missions depuis fichier...")
        task_ids = scheduler.add_missions_from_file(missions_file)
        print(f"   ✅ Chargé: {len(task_ids)} missions")
        
        print("\n3. 📊 Statut initial...")
        status = scheduler.get_status()
        print(f"   - File d'attente: {status['queue']['pending']} tâches en attente")
        print(f"   - GPU disponible: {status['gpu']['available']}")
        print(f"   - Base de données: {'PostgreSQL' if status['database']['postgresql'] else 'SQLite'}")
        
        print("\n4. 🚀 Traitement des tâches (simulation)...")
        
        # Mock de l'exécution pour la démo
        original_execute = scheduler.execute_task
        
        async def mock_execute(task):
            print(f"   🔄 Traitement: {task['mission'][:40]}...")
            await asyncio.sleep(0.1)  # Simulation rapide
            return True, f'{{"status": "completed", "task_id": {task["id"]}}}'
        
        scheduler.execute_task = mock_execute
        
        # Traiter 3 tâches
        await scheduler.process_queue(max_tasks=3, timeout=30)
        
        print("\n5. 📈 Statut final...")
        final_status = scheduler.get_status()
        print(f"   - Tâches traitées: {final_status['stats']['tasks_processed']}")
        print(f"   - Succès: {final_status['stats']['tasks_successful']}")
        print(f"   - Restantes: {final_status['queue']['pending']}")
        
        print("\n6. 📄 Génération rapport...")
        report_path = scheduler.generate_report()
        print(f"   ✅ Rapport: {report_path}")
        
        # Afficher extrait du rapport
        with open(report_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:15]  # Premières lignes
        
        print("\n📋 Extrait du rapport:")
        for line in lines:
            print(f"   {line.rstrip()}")
        
        print("\n✅ Démonstration terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur démonstration: {e}")
        
    finally:
        # Nettoyer
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    print("🧪 Task Scheduler Cursor - Suite de Tests")
    print("=" * 60)
    
    # Tests unitaires
    print("\n1. 🔬 Tests Unitaires")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Test de performance
    run_performance_test()
    
    # Démonstration intégration
    print("\n3. 🎭 Démonstration Intégration")
    asyncio.run(run_integration_demo())
    
    print("\n🎉 Tous les tests terminés!") 



