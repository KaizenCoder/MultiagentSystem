import unittest
import asyncio
import tempfile
import shutil
from datetime import datetime
from cli_taskmaster_cursor import TaskMasterCLI
from dashboard_taskmaster_cursor import TaskMasterDashboard
from validator_sessions_cursor import SessionValidator
from task_scheduler_cursor import TaskSchedulerCursor

class TestTaskMasterEndToEnd(unittest.TestCase):
    """Test end-to-end avancé TaskMaster Cursor"""

    def setUp(self):
        # Préparer un environnement temporaire
        self.temp_dir = tempfile.mkdtemp()
        # TODO: Rediriger les chemins de base de données et logs vers self.temp_dir
        self.cli = TaskMasterCLI()
        self.scheduler = TaskSchedulerCursor()
        self.validator = SessionValidator()
        self.dashboard = TaskMasterDashboard()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_multi_user_and_robustness(self):
        """Simule plusieurs utilisateurs, interruptions, saturation file d'attente"""
        async def scenario():
            # 1. Lancer plusieurs tâches en parallèle (multi-utilisateurs)
            missions = [f"Mission E2E {i}" for i in range(20)]
            tasks = [self.cli.launch_single_task(mission=m) for m in missions]
            results = await asyncio.gather(*tasks)
            self.assertEqual(len(results), 20)

            # 2. Saturer la file d'attente
            for i in range(100):
                await self.cli.launch_single_task(mission=f"Saturation {i}")

            # 3. Arrêter puis relancer le scheduler (interruption)
            self.scheduler.stop()
            await asyncio.sleep(1)
            # Simuler une reprise
            # (TODO: relancer proprement le scheduler si besoin)

            # 4. Vérifier qu'aucune tâche n'est perdue
            stats = self.scheduler.db_manager.get_queue_stats()
            self.assertGreaterEqual(stats['total'], 120)

            # 5. Vérifier les statuts
            for status in ['pending', 'running', 'completed', 'failed']:
                self.assertIn(status, stats)

            # 6. Validation finale
            validation = await self.validator.run_full_validation()
            self.assertTrue(validation['score'] >= 8)  # Score minimal à ajuster

        asyncio.run(scenario())

if __name__ == "__main__":
    unittest.main() 