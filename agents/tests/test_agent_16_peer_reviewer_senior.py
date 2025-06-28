#!/usr/bin/env python3
"""
Tests unitaires et d'intégration pour Agent 16 - Peer Reviewer Senior
Validation conformité Pattern Factory et fonctionnalités
"""

import unittest
import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

# Ajouter le chemin parent pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_16_peer_reviewer_senior import PeerReviewerSeniorAgent
from core.agent_factory_architecture import Task, Result

class TestAgent16PeerReviewerSenior(unittest.TestCase):
    """Tests pour l'Agent 16 - Peer Reviewer Senior"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.agent = PeerReviewerSeniorAgent()
        
    def tearDown(self):
        """Nettoyage après chaque test"""
        # Nettoyage asynchrone des handlers de log
        asyncio.run(self.agent.shutdown())
        
    def test_agent_initialization(self):
        """Test initialisation agent conforme Pattern Factory"""
        # Vérifier attributs Pattern Factory
        self.assertEqual(self.agent.type, "peer_reviewer_senior")
        self.assertIsNotNone(self.agent.id)
        self.assertTrue(self.agent.id.startswith("peer_reviewer_senior_"))
        self.assertEqual(self.agent.name, "Agent 16 - Peer Reviewer Senior")
        self.assertIsInstance(self.agent.created_at, datetime)
        
        # Vérifier capacités
        capabilities = self.agent.get_capabilities()
        self.assertIsInstance(capabilities, list)
        self.assertIn("code_review", capabilities)
        self.assertIn("quality_assessment", capabilities)
        
    def test_health_check(self):
        """Test health check asynchrone"""
        async def run_health_check():
            health = await self.agent.health_check()
            self.assertIsInstance(health, dict)
            self.assertEqual(health["status"], "healthy")
            self.assertIn("agent", health)
            self.assertIn("timestamp", health)
            
        asyncio.run(run_health_check())
        
    def test_startup_shutdown(self):
        """Test lifecycle startup/shutdown"""
        async def run_lifecycle():
            # Test startup
            await self.agent.startup()
            
            # Test shutdown
            await self.agent.shutdown()
            
        asyncio.run(run_lifecycle())
        
    def test_execute_task_code_review(self):
        """Test exécution tâche code_review"""
        task = Task(type="code_review", params={"target": "agent_02"})
        result = self.agent.execute_task(task)
        
        # Vérifier résultat
        self.assertIsInstance(result, Result)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)
        self.assertIsInstance(result.data, dict)
        
        # Vérifier structure résultat
        data = result.data
        self.assertIn("status", data)
        self.assertIn("architecture_review", data)
        self.assertIn("conformity_validation", data)
        self.assertIn("quality_assessment", data)
        self.assertIn("performance", data)
        
    def test_execute_task_quality_assessment(self):
        """Test exécution tâche quality_assessment"""
        task = Task(type="quality_assessment")
        result = self.agent.execute_task(task)
        
        # Vérifier résultat
        self.assertIsInstance(result, Result)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)
        
    def test_execute_task_unsupported(self):
        """Test tâche non supportée"""
        task = Task(type="unsupported_task")
        result = self.agent.execute_task(task)
        
        # Vérifier échec
        self.assertIsInstance(result, Result)
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
        self.assertIn("non supporté", result.error)
        
    def test_can_handle_task(self):
        """Test vérification capacité à traiter les tâches"""
        # Tâches supportées
        task1 = Task(type="code_review")
        task2 = Task(type="quality_assessment")
        self.assertTrue(self.agent.can_handle(task1))
        self.assertTrue(self.agent.can_handle(task2))
        
        # Tâche non supportée
        task3 = Task(type="unknown_task")
        self.assertFalse(self.agent.can_handle(task3))
        
    def test_review_metrics_calculation(self):
        """Test calcul des métriques de review"""
        # Exécuter une review pour générer des métriques
        task = Task(type="code_review")
        result = self.agent.execute_task(task)
        
        # Vérifier métriques présentes
        self.assertTrue(result.success)
        performance = result.data["performance"]
        
        self.assertIn("duration_seconds", performance)
        self.assertIn("elements_reviewed", performance)
        self.assertIn("architecture_score", performance)
        self.assertIn("conformity_score", performance)
        self.assertIn("overall_quality", performance)
        
    def test_report_generation(self):
        """Test génération rapport senior"""
        # Exécuter mission complète
        result = self.agent.run_senior_review_mission()
        
        # Vérifier rapport généré
        self.assertIsInstance(result, dict)
        self.assertIn("final_report", result)
        
        # Si un rapport est généré, vérifier qu'il existe
        if result["final_report"]:
            report_path = Path(result["final_report"])
            self.assertTrue(report_path.exists())
            
            # Vérifier contenu basique
            content = report_path.read_text(encoding='utf-8')
            self.assertIn("PEER REVIEW SENIOR", content)
            self.assertIn("Agent 16", content)
            
    def test_direct_run_method(self):
        """Test méthode run directe"""
        result = self.agent.run("review senior mission")
        
        # Vérifier résultat
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        
class TestAgent16Integration(unittest.TestCase):
    """Tests d'intégration avec simulation CLI"""
    
    def setUp(self):
        """Configuration pour tests d'intégration"""
        self.agent = PeerReviewerSeniorAgent()
        
    def tearDown(self):
        """Nettoyage après tests d'intégration"""
        asyncio.run(self.agent.shutdown())
        
    def test_cli_simulation(self):
        """Simulation complète d'utilisation CLI"""
        # Simuler args CLI
        task_prompt = "Effectuer review senior architecture code expert"
        
        # Exécuter comme en CLI
        result = self.agent.run(task_prompt)
        
        # Vérifier succès
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        
        # Vérifier que le status indique un succès
        status = result.get("status", "")
        self.assertTrue("SUCCÈS" in status or "SUCCESS" in status)
        
    def test_async_operations_compatibility(self):
        """Test compatibilité opérations asynchrones"""
        async def run_async_operations():
            # Test startup
            await self.agent.startup()
            
            # Test health check
            health = await self.agent.health_check()
            self.assertEqual(health["status"], "healthy")
            
            # Test exécution synchrone dans contexte async
            task = Task(type="code_review")
            result = self.agent.execute_task(task)
            self.assertTrue(result.success)
            
            # Test shutdown
            await self.agent.shutdown()
            
        asyncio.run(run_async_operations())
        
    def test_error_handling_robustness(self):
        """Test robustesse gestion d'erreurs"""
        # Test avec task malformée
        try:
            result = self.agent.execute_task(None)
            # Si on arrive ici, vérifier que l'erreur est gérée proprement
            self.assertFalse(result.success)
        except:
            # Une exception est acceptable pour des inputs invalides
            pass
            
        # Test avec paramètres invalides
        task = Task(type="code_review", params={"invalid_param": "test"})
        result = self.agent.execute_task(task)
        # L'agent doit gérer gracieusement les paramètres invalides
        self.assertIsInstance(result, Result)

def run_tests():
    """Exécute tous les tests et génère un rapport"""
    print("🧪 DÉMARRAGE DES TESTS - Agent 16 Peer Reviewer Senior")
    print("=" * 60)
    
    # Créer suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajouter tests unitaires
    suite.addTest(loader.loadTestsFromTestCase(TestAgent16PeerReviewerSenior))
    suite.addTest(loader.loadTestsFromTestCase(TestAgent16Integration))
    
    # Exécuter tests avec verbose output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Générer rapport
    print("\n" + "=" * 60)
    print("📊 RAPPORT DE TESTS")
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    print(f"Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"Taux de succès: {success_rate:.1f}%")
    
    if result.failures:
        print(f"\n❌ ÉCHECS ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\n')[0] if 'AssertionError: ' in traceback else 'Échec assertion'}")
    
    if result.errors:
        print(f"\n🔥 ERREURS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\n')[-2] if traceback else 'Erreur inconnue'}")
    
    if result.wasSuccessful():
        print("\n✅ TOUS LES TESTS RÉUSSIS")
        print("🎯 Agent 16 - Peer Reviewer Senior VALIDÉ")
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("⚠️ Révision requise avant validation")
    
    print("=" * 60)
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)