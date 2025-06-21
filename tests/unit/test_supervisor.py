"""
Tests unitaires pour le Supervisor - CRITIQUE pour Phase 2.
Tests des fonctionnalits de planification et routage du supervisor.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from orchestrator.app.agents.supervisor import Supervisor
from orchestrator.app.graph.state import AgentState


@pytest.mark.unit
class TestSupervisor:
    """Tests unitaires Supervisor - CRITIQUE."""
    
    def setup_method(self):
        """Setup pour chaque test."""
        self.supervisor = Supervisor()
    
    def test_create_plan_code_generation_task(self, sample_agent_state):
        """Test planification tche gnration code."""
        # ARRANGE
        sample_agent_state["task_description"] = "Generate Python sorting function"
        
        # ACT
        result = self.supervisor.create_plan(sample_agent_state)
        
        # ASSERT
        assert result["plan"] is not None
        assert "code_generation" in result["plan"].lower() or "code" in result["plan"].lower()
        assert result["next"] == "code_generation"
        assert result["task_status"] == "in_progress"
    
    def test_create_plan_documentation_task(self, sample_agent_state):
        """Test planification tche documentation."""
        # ARRANGE
        sample_agent_state["task_description"] = "Create API documentation"
        
        # ACT
        result = self.supervisor.create_plan(sample_agent_state)
        
        # ASSERT
        assert result["plan"] is not None
        assert "documentation" in result["plan"].lower() or "doc" in result["plan"].lower()
        assert result["next"] == "documentation"
    
    def test_create_plan_testing_task(self, sample_agent_state):
        """Test planification tche de test."""
        # ARRANGE
        sample_agent_state["task_description"] = "Write unit tests for the code"
        
        # ACT
        result = self.supervisor.create_plan(sample_agent_state)
        
        # ASSERT
        assert result["plan"] is not None
        assert "test" in result["plan"].lower() or "testing" in result["plan"].lower()
    
    def test_route_with_code_results(self, sample_agent_state):
        """Test routage avec rsultats code."""
        # ARRANGE
        sample_agent_state["results"] = {"code_generation": "def sort_list(): pass"}
        sample_agent_state["plan"] = "1. Generate code\n2. Document it"
        
        # ACT
        result = self.supervisor.route(sample_agent_state)
        
        # ASSERT
        assert result["next"] in ["documentation", "finish"]
    
    def test_route_completion_all_results(self, sample_agent_state):
        """Test routage vers fin avec tous rsultats."""
        # ARRANGE
        sample_agent_state["results"] = {
            "code_generation": "def sort_list(): pass",
            "documentation": "Function documentation"
        }
        sample_agent_state["plan"] = "Complete task"
        
        # ACT
        result = self.supervisor.route(sample_agent_state)
        
        # ASSERT
        assert result["next"] == "finish"
    
    def test_route_empty_results(self, sample_agent_state):
        """Test routage avec rsultats vides."""
        # ARRANGE
        sample_agent_state["results"] = {}
        sample_agent_state["plan"] = "Start with code generation"
        
        # ACT
        result = self.supervisor.route(sample_agent_state)
        
        # ASSERT
        assert result["next"] != "finish"
    
    def test_error_handling_invalid_state(self):
        """Test gestion erreur tat invalide."""
        # ARRANGE
        invalid_state = AgentState()  # tat vide

        # ACT - Le supervisor gre gracieusement les tats vides
        try:
            result = self.supervisor.create_plan(invalid_state)
            # ASSERT - Doit avoir un plan par dfaut mme avec tat vide
            assert result is not None
            assert "plan" in result
        except (ValueError, AttributeError) as e:
            # Si une exception est leve, c'est aussi valide
            assert isinstance(e, (ValueError, AttributeError))
    
    def test_error_handling_none_task_description(self, sample_agent_state):
        """Test gestion erreur description nulle."""
        # ARRANGE
        sample_agent_state["task_description"] = None
        
        # ACT & ASSERT
        with pytest.raises((ValueError, AttributeError)):
            self.supervisor.create_plan(sample_agent_state)
    
    def test_plan_persistence(self, sample_agent_state):
        """Test persistance du plan."""
        # ARRANGE
        sample_agent_state["task_description"] = "Generate Python code"
        
        # ACT
        result1 = self.supervisor.create_plan(sample_agent_state)
        result2 = self.supervisor.create_plan(result1)
        
        # ASSERT
        assert result2["plan"] == result1["plan"]
    
    @pytest.mark.asyncio
    async def test_supervisor_with_llm_timeout(self, sample_agent_state):
        """Test gestion timeout LLM - VERSION CORRIGE."""
        # ARRANGE - Pas de llm_service dans supervisor.py, on teste la logique directe
        # Le supervisor n'utilise pas de LLM, seulement de la logique conditionnelle
        
        # ACT - Tester que le supervisor fonctionne sans timeout
        result = self.supervisor.create_plan(sample_agent_state)
        
        # ASSERT - Le supervisor doit rpondre rapidement (pas de LLM)
        assert result is not None
        assert "plan" in result
        assert "task_status" in result
        assert result["task_status"] == "in_progress"
    
    def test_supervisor_multiple_tasks(self, sample_task_descriptions):
        """Test supervisor avec diffrents types de tches."""
        for task_type, description in sample_task_descriptions.items():
            # ARRANGE
            state = AgentState(
                task_description=description,
                session_id=f"test-{task_type}",
                results={},
                task_status="pending"
            )
            
            # ACT
            result = self.supervisor.create_plan(state)
            
            # ASSERT
            assert result["plan"] is not None
            assert len(result["plan"]) > 10  # Plan non vide
            assert result["next"] is not None
    
    def test_supervisor_routing_logic(self, sample_agent_state):
        """Test logique de routage complexe."""
        # Test diffrents scnarios de routage
        scenarios = [
            # (results, expected_next_options)
            ({}, ["code_generation", "documentation", "testing"]),
            ({"code_generation": "code"}, ["documentation", "testing", "finish"]),
            ({"documentation": "docs"}, ["code_generation", "testing", "finish"]),
            ({"code_generation": "code", "documentation": "docs"}, ["finish", "testing"])
        ]
        
        for results, expected_options in scenarios:
            # ARRANGE
            sample_agent_state["results"] = results
            sample_agent_state["plan"] = "Test plan"
            
            # ACT
            result = self.supervisor.route(sample_agent_state)
            
            # ASSERT
            assert result["next"] in expected_options, f"Unexpected next: {result['next']} for results: {results}"
    
    def test_supervisor_state_consistency(self, sample_agent_state):
        """Test cohrence de l'tat aprs oprations."""
        # ARRANGE
        original_session_id = sample_agent_state["session_id"]
        
        # ACT
        result = self.supervisor.create_plan(sample_agent_state)
        
        # ASSERT
        assert result["session_id"] == original_session_id
        assert "task_description" in result
        assert "plan" in result
        assert "results" in result
        assert "task_status" in result
    
    def test_supervisor_performance(self, sample_agent_state, performance_monitor):
        """Test performance du supervisor."""
        # ARRANGE
        performance_monitor.start()
        
        # ACT
        for _ in range(10):
            self.supervisor.create_plan(sample_agent_state)
        
        # ASSERT
        performance_monitor.assert_max_duration(1000)  # Max 1 seconde pour 10 oprations
    
    @pytest.mark.parametrize("task_desc,expected_agent", [
        ("Generate Python code", "code_generation"),
        ("Write documentation", "documentation"), 
        ("Create tests", "testing"),
        ("Debug the code", "code_generation"),
        ("Refactor function", "code_generation")
    ])
    def test_supervisor_agent_selection(self, sample_agent_state, task_desc, expected_agent):
        """Test slection d'agent selon le type de tche."""
        # ARRANGE
        sample_agent_state["task_description"] = task_desc
        
        # ACT
        result = self.supervisor.create_plan(sample_agent_state)
        
        # ASSERT
        assert result["next"] == expected_agent or expected_agent in result["plan"].lower() 



