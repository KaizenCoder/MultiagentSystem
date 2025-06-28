# tests/test_agent_lecteur_workflow.py
import unittest
from pathlib import Path
import sys
import os
import logging

# Ajout du répertoire parent au path pour résoudre les imports locaux
# Cela suppose que le script de test est dans un sous-répertoire de 'tests/'
# et que 'agents/' est au même niveau que 'tests/'
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent # CORRECTION: Un seul .parent pour remonter à la racine du projet
sys.path.append(str(project_root))

from agents.cartographie_assistants.agent_lecteur_workflow import AgentLecteurWorkflow

class TestAgentLecteurWorkflow(unittest.TestCase):
    """
    Tests unitaires pour AgentLecteurWorkflow.
    """
    test_workflow_file_path = Path("temp_test_workflow_for_unittest.md")

    @classmethod
    def setUpClass(cls):
        """Crée un fichier workflow de test avant tous les tests."""
        workflow_content = [
            "# WORKFLOW DE TEST\n",
            "- [x] agent_01_termine.py - Description de l'agent 01\n",
            "- [ ] agent_02_afaire.py\n",
            "  - [X] agent_03_termine_majuscule_indent.py - Indenté\n", # Test indentation et X majuscule
            "Ligne invalide\n",
            "- [ ] agent_04_nom_complexe-avec-tirets_v2.py - Un nom plus complexe\n",
            "-    [ ] agent_05_espaces_avant.py\n", # Test avec espaces avant
            "- [x]agent_06_pas_despace_apres_checkbox.py\n", # Test sans espace après checkbox
            "- agent_07_sans_checkbox.py\n", # Ne doit pas matcher
            "-[] agent_08_checkbox_vide_incorrecte.py\n", # Ne doit pas matcher
            "- [y] agent_09_checkbox_invalide.py\n" # Ne doit pas matcher
        ]
        with open(cls.test_workflow_file_path, "w", encoding="utf-8") as f:
            f.writelines(workflow_content)

    @classmethod
    def tearDownClass(cls):
        """Supprime le fichier workflow de test après tous les tests."""
        if cls.test_workflow_file_path.exists():
            cls.test_workflow_file_path.unlink()

    def setUp(self):
        """Initialise l'agent avant chaque test."""
        self.agent = AgentLecteurWorkflow(workflow_file_path=str(self.test_workflow_file_path))
        self.agent.startup()

    def tearDown(self):
        """Arrête l'agent après chaque test."""
        self.agent.shutdown()

    def test_health_check(self):
        """Teste la méthode health_check."""
        health = self.agent.health_check()
        self.assertEqual(health["status"], "OK")
        self.assertEqual(health["agent_id"], "agent_lecteur_workflow")
        self.assertIn("version", health)

    def test_analyser_workflow_direct_call(self):
        """Teste directement la méthode analyser_workflow."""
        results = self.agent.analyser_workflow()
        self.assertEqual(len(results), 6) # Attend 6 agents valides

        # Vérifications spécifiques
        self.assertEqual(results[0]["nom_agent"], "agent_01_termine.py")
        self.assertEqual(results[0]["statut_interprete"], "Terminé")
        self.assertEqual(results[0]["description"], "Description de l'agent 01")

        self.assertEqual(results[1]["nom_agent"], "agent_02_afaire.py")
        self.assertEqual(results[1]["statut_interprete"], "À faire")
        self.assertEqual(results[1]["description"], "")

        self.assertEqual(results[2]["nom_agent"], "agent_03_termine_majuscule_indent.py")
        self.assertEqual(results[2]["statut_interprete"], "Terminé")
        
        self.assertEqual(results[5]["nom_agent"], "agent_06_pas_despace_apres_checkbox.py")
        self.assertEqual(results[5]["statut_interprete"], "Terminé")


    def test_execute_task_analyser_workflow(self):
        """Teste l'action analyser_workflow via execute_task."""
        task_details = {
            "action": "analyser_workflow",
            "params": {"workflow_file_path": str(self.test_workflow_file_path)}
        }
        response = self.agent.execute_task(task_details)
        
        self.assertEqual(response["status"], "succès")
        self.assertIsInstance(response["data"], list)
        self.assertEqual(len(response["data"]), 6)

        # Vérification d'un élément
        agent_data_example = next(item for item in response["data"] if item["nom_agent"] == "agent_04_nom_complexe-avec-tirets_v2.py")
        self.assertEqual(agent_data_example["statut_interprete"], "À faire")
        self.assertEqual(agent_data_example["description"], "Un nom plus complexe")

    def test_execute_task_fichier_inexistant(self):
        """Teste l'action analyser_workflow avec un fichier qui n'existe pas."""
        task_details = {
            "action": "analyser_workflow",
            "params": {"workflow_file_path": "fichier_qui_n_existe_pas.md"}
        }
        response = self.agent.execute_task(task_details)
        self.assertEqual(response["status"], "succès") # La méthode retourne succès mais data est vide
        self.assertEqual(len(response["data"]), 0)
        self.assertIn("n'existe pas", response["message"])


    def test_execute_task_chemin_non_fourni(self):
        """Teste l'action analyser_workflow sans chemin de fichier, ni dans params ni à l'init."""
        agent_sans_chemin = AgentLecteurWorkflow() # Pas de chemin à l'init
        task_details = {
            "action": "analyser_workflow",
            "params": {} # Pas de chemin dans les params
        }
        response = agent_sans_chemin.execute_task(task_details)
        self.assertEqual(response["status"], "erreur")
        self.assertIn("Paramètre 'workflow_file_path' manquant", response["message"])

    def test_interpret_status(self):
        """Teste la méthode _interpret_status."""
        self.assertEqual(self.agent._interpret_status("x"), "Terminé")
        self.assertEqual(self.agent._interpret_status("X"), "Terminé")
        self.assertEqual(self.agent._interpret_status(" "), "À faire")
        self.assertEqual(self.agent._interpret_status(""), "À faire") # Cas où la regex capturerait un espace vide

if __name__ == '__main__':
    # Création du répertoire de logs de test s'il n'existe pas
    # logs_test_dir = project_root / "logs" / "tests_cartographie"
    # logs_test_dir.mkdir(parents=True, exist_ok=True)
    # logging.basicConfig(filename=logs_test_dir / 'test_agent_lecteur_workflow.log', level=logging.DEBUG)
    
    # Pour exécution directe, on simplifie le logging vers la console
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    unittest.main() 