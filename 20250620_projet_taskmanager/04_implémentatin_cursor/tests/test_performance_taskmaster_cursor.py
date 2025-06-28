import unittest
import time
import psutil
import tempfile
import shutil
from task_scheduler_cursor import TaskSchedulerCursor

class TestTaskMasterPerformance(unittest.TestCase):
    """Test de performance avancé TaskMaster Cursor"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.scheduler = TaskSchedulerCursor()
        # TODO: Rediriger les chemins de base de données/logs vers self.temp_dir

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_stress_and_resource_usage(self):
        """Stress test prolongé et monitoring ressources"""
        num_tasks = 1000
        start_time = time.time()

        # Ajout massif de tâches
        for i in range(num_tasks):
            self.scheduler.add_mission(f"PerfTest {i}", priority=i%10)

        add_time = time.time() - start_time
        print(f"Ajout de {num_tasks} tâches en {add_time:.2f}s")

        # Monitoring ressources
        process = psutil.Process()
        cpu_usages = []
        mem_usages = []
        t0 = time.time()
        duration = 60  # secondes de stress test
        treated = 0
        while time.time() - t0 < duration:
            task = self.scheduler.db_manager.get_next_task()
            if not task:
                break
            self.scheduler.db_manager.update_task_status(task['id'], 'completed')
            treated += 1
            cpu_usages.append(process.cpu_percent(interval=0.1))
            mem_usages.append(process.memory_info().rss / 1024 / 1024)  # en Mo

        print(f"Tâches traitées en {duration}s : {treated}")
        print(f"CPU moyen : {sum(cpu_usages)/len(cpu_usages):.2f}%")
        print(f"Mémoire max : {max(mem_usages):.2f} Mo")
        # Détection fuite mémoire
        self.assertLess(max(mem_usages) - min(mem_usages), 100, "Fuite mémoire suspectée")

if __name__ == "__main__":
    unittest.main() 