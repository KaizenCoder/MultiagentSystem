#!/usr/bin/env python3
"""
Test de Workflow Formel - TaskMaster Final
==========================================

Tests d'intégration pour valider le workflow complet du TaskMaster Final
selon la méthodologie M-T-D du PLAN_ACTION_TASKMASTER_FINAL.md

Date: 2025-06-26
Objectif: Validation de non-régression fonctionnelle de bout en bout
"""

import unittest
import asyncio
import sys
import os
from pathlib import Path
import tempfile
import shutil
import logging

# Ajout du chemin vers le répertoire agents
AGENTS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "agents"
sys.path.insert(0, str(AGENTS_DIR))

from taskmaster_final import TaskMasterFinal

class TestTaskMasterFinalWorkflow(unittest.TestCase):
    """Tests de workflow complet pour TaskMaster Final"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.taskmaster = TaskMasterFinal(agent_id="test_workflow_001")
        # Utilisation d'un répertoire temporaire pour les tests
        self.temp_dir = Path(tempfile.mkdtemp())
        self.taskmaster.work_dir = self.temp_dir
        self.taskmaster.log_dir = self.temp_dir / "logs"
        self.taskmaster.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Reconfiguration du logger pour les tests
        self.taskmaster.log_file = self.taskmaster.log_dir / "test_taskmaster_final.log"
        
    def tearDown(self):
        """Nettoyage après chaque test"""
        # Nettoyage des ressources
        if hasattr(self.taskmaster, 'agents'):
            for agent_name, agent_data in self.taskmaster.agents.items():
                if 'instance' in agent_data:
                    agent_instance = agent_data['instance']
                    if hasattr(agent_instance, 'shutdown'):
                        agent_instance.shutdown()
        
        # Suppression du répertoire temporaire
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_01_agent_discovery(self):
        """Test 1: Découverte des agents"""
        async def run_test():
            await self.taskmaster.startup()
            
            # Vérification que les agents cibles sont découverts
            self.assertIn("agent_13_specialiste_documentation", self.taskmaster.agents)
            self.assertIn("agent_14_specialiste_workspace", self.taskmaster.agents)
            self.assertIn("agent_16_peer_reviewer_senior", self.taskmaster.agents)
            
            # Vérification des capacités
            agent_13 = self.taskmaster.agents["agent_13_specialiste_documentation"]
            self.assertIn("documentation_generation", agent_13["capabilities"])
            
            agent_14 = self.taskmaster.agents["agent_14_specialiste_workspace"]
            self.assertIn("workspace_creation", agent_14["capabilities"])
            
            agent_16 = self.taskmaster.agents["agent_16_peer_reviewer_senior"]
            self.assertIn("code_review", agent_16["capabilities"])
            
            await self.taskmaster.shutdown()
        
        asyncio.run(run_test())
    
    def test_02_workspace_creation_mission(self):
        """Test 2: Mission de création de workspace"""
        async def run_test():
            await self.taskmaster.startup()
            
            # Mission de création de workspace
            mission = "J'ai besoin de créer un workspace pour mon projet."
            result = await self.taskmaster.execute_mission(mission)
            
            # Vérifications
            self.assertIsNotNone(result)
            self.assertNotEqual(result.get("status"), "error")
            self.assertNotEqual(result.get("status"), "critical_error")
            
            await self.taskmaster.shutdown()
        
        asyncio.run(run_test())
    
    def test_03_documentation_mission(self):
        """Test 3: Mission de documentation"""
        async def run_test():
            await self.taskmaster.startup()
            
            # Mission de documentation
            mission = "Peux-tu générer de la documentation pour ce projet ?"
            result = await self.taskmaster.execute_mission(mission)
            
            # Vérifications
            self.assertIsNotNone(result)
            self.assertNotEqual(result.get("status"), "error")
            self.assertNotEqual(result.get("status"), "critical_error")
            
            await self.taskmaster.shutdown()
        
        asyncio.run(run_test())
    
    def test_04_code_review_mission(self):
        """Test 4: Mission de revue de code"""
        async def run_test():
            await self.taskmaster.startup()
            
            # Mission de revue de code
            mission = "Peux-tu me faire une revue de code (code_review) ?"
            result = await self.taskmaster.execute_mission(mission)
            
            # Vérifications
            self.assertIsNotNone(result)
            self.assertNotEqual(result.get("status"), "error")
            self.assertNotEqual(result.get("status"), "critical_error")
            
            await self.taskmaster.shutdown()
        
        asyncio.run(run_test())
    
    def test_05_complex_workflow_mission(self):
        """Test 5: Mission complexe - Workflow complet"""
        async def run_test():
            await self.taskmaster.startup()
            
            # Mission complexe combinant création de workspace et documentation
            mission = "Crée un workspace pour un projet et documente-le."
            result = await self.taskmaster.execute_mission(mission)
            
            # Vérifications du workflow complet
            self.assertIsNotNone(result)
            self.assertNotEqual(result.get("status"), "error")
            self.assertNotEqual(result.get("status"), "critical_error")
            
            # Vérification que le fichier de log a été créé
            self.assertTrue(self.taskmaster.log_file.exists())
            
            # Vérification du contenu du log
            log_content = self.taskmaster.log_file.read_text(encoding='utf-8')
            self.assertIn("Mission terminée", log_content)
            
            await self.taskmaster.shutdown()
        
        asyncio.run(run_test())
    
    def test_06_error_handling(self):
        """Test 6: Gestion d'erreurs pour mission invalide"""
        async def run_test():
            await self.taskmaster.startup()
            
            # Mission avec mots-clés non reconnus
            mission = "Fais quelque chose de complètement impossible et non supporté."
            result = await self.taskmaster.execute_mission(mission)
            
            # Vérifications de la gestion d'erreur
            self.assertIsNotNone(result)
            self.assertEqual(result.get("status"), "error")
            self.assertIn("No suitable agent found", result.get("message", ""))
            
            await self.taskmaster.shutdown()
        
        asyncio.run(run_test())

if __name__ == '__main__':
    # Configuration du logging pour les tests
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Exécution des tests
    unittest.main(verbosity=2)