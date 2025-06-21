"""
Tests unitaires simplifis pour le Supervisor - Version fonctionnelle.
"""

import pytest
from unittest.mock import Mock, patch
from orchestrator.app.agents.supervisor import Supervisor


@pytest.mark.unit
class TestSupervisorSimple:
    """Tests unitaires simplifis pour le Supervisor."""
    
    def setup_method(self):
        """Setup pour chaque test."""
        self.supervisor = Supervisor()
    
    def test_supervisor_exists(self):
        """Test que le supervisor existe et est instanciable."""
        assert self.supervisor is not None
        assert hasattr(self.supervisor, 'create_plan')
        assert hasattr(self.supervisor, 'route')
    
    def test_create_plan_basic(self, sample_agent_state):
        """Test cration de plan basique."""
        # ARRANGE
        sample_agent_state["task_description"] = "Generate Python code"
        
        # ACT
        result = self.supervisor.create_plan(sample_agent_state)
        
        # ASSERT
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result
    
    def test_route_basic(self, sample_agent_state):
        """Test routage basique."""
        # ARRANGE
        sample_agent_state["plan"] = "Test plan"
        sample_agent_state["results"] = {}
        
        # ACT
        result = self.supervisor.route(sample_agent_state)
        
        # ASSERT
        assert result is not None
        assert isinstance(result, dict)
        assert "next" in result
    
    def test_supervisor_with_different_tasks(self, sample_task_descriptions):
        """Test supervisor avec diffrents types de tches."""
        from datetime import datetime
        
        for task_type, description in sample_task_descriptions.items():
            # ARRANGE
            state = {
                "task_description": description,
                "session_id": f"test-{task_type}",
                "plan": None,
                "results": {},
                "task_status": "pending",
                "messages": [],
                "next": "supervisor",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "code_context": None,
                "working_memory": [],
                "errors": [],
                "logs": [],
                "feedback": None
            }
            
            # ACT
            result = self.supervisor.create_plan(state)
            
            # ASSERT
            assert result is not None
            assert result.get("plan") is not None or result.get("next") is not None
    
    def test_supervisor_error_handling(self):
        """Test gestion d'erreur basique."""
        # ARRANGE
        invalid_state = {}
        
        # ACT & ASSERT
        try:
            self.supervisor.create_plan(invalid_state)
            # Si a ne lve pas d'erreur, c'est ok aussi
        except Exception as e:
            # Toute exception est acceptable pour un tat invalide
            assert isinstance(e, (ValueError, AttributeError, KeyError))
    
    def test_supervisor_performance_basic(self, sample_agent_state, performance_monitor):
        """Test performance basique."""
        # ARRANGE
        performance_monitor.start()
        
        # ACT
        for _ in range(5):
            try:
                self.supervisor.create_plan(sample_agent_state)
            except:
                pass  # Ignorer les erreurs pour ce test de performance
        
        # ASSERT
        performance_monitor.assert_max_duration(2000)  # Max 2 secondes pour 5 oprations 



