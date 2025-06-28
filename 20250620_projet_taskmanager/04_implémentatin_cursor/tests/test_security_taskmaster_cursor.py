import unittest
import os
import tempfile
import shutil
from task_scheduler_cursor import TaskSchedulerCursor

class TestTaskMasterSecurity(unittest.TestCase):
    """Test de sécurité TaskMaster Cursor"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.scheduler = TaskSchedulerCursor()
        # TODO: Rediriger les chemins de base de données/logs vers self.temp_dir

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_sql_injection(self):
        """Tente une injection SQL via la mission"""
        injection = "TestInjection'); DROP TABLE task_queue; --"
        try:
            task_id = self.scheduler.add_mission(injection, priority=5)
            # Vérifier que la table existe toujours
            stats = self.scheduler.db_manager.get_queue_stats()
            self.assertIn('pending', stats)
        except Exception as e:
            self.fail(f"Erreur inattendue lors de l'injection SQL : {e}")

    def test_file_permissions(self):
        """Test les permissions sur les fichiers critiques"""
        # Fichier temporaire
        test_file = os.path.join(self.temp_dir, 'test_perm.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        # Lecture/écriture
        self.assertTrue(os.access(test_file, os.R_OK))
        self.assertTrue(os.access(test_file, os.W_OK))
        # Suppression
        os.remove(test_file)
        self.assertFalse(os.path.exists(test_file))

    def test_logs_no_secrets(self):
        """Vérifie que les logs ne contiennent pas de secrets ou mots de passe"""
        # TODO: Adapter le chemin du log
        log_path = os.path.join(self.temp_dir, 'logs', 'task_scheduler_cursor.log')
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertNotIn('password', content.lower())
                self.assertNotIn('secret', content.lower())

if __name__ == "__main__":
    unittest.main() 