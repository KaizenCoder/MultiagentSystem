from typing import Dict, Any
from orchestrator.app.graph.state import AgentState

class Supervisor:
    """Agent superviseur qui coordonne les tâches entre les agents spécialisés."""
    
    def create_plan(self, state: AgentState) -> AgentState:
        """CORRECTIF 5: Crée un plan de tâche basé sur la description - CORRECTION IA-1 ajout testing."""
        task_description = state.get("task_description", "")
        
        # CORRECTION IA-1: Ajout reconnaissance tâches testing
        if any(keyword in task_description.lower() for keyword in ["test", "testing", "unit test", "pytest", "unittest"]):
            plan = "Create comprehensive tests using testing agent"
            state["next"] = "testing"
        elif "code" in task_description.lower() or "python" in task_description.lower() or "generate" in task_description.lower():
            plan = "Generate code solution using code_generation agent, then document with documentation agent"
            state["next"] = "code_generation"
        elif "documentation" in task_description.lower() or "doc" in task_description.lower():
            plan = "Create documentation using documentation agent"
            state["next"] = "documentation"
        else:
            # Plan par défaut
            plan = "Analyze task and determine appropriate agent for execution"
            state["next"] = "code_generation"
        
        state["plan"] = plan
        state["task_status"] = "in_progress"
        return state
    
    def route(self, state: AgentState) -> Dict[str, Any]:
        """Détermine le prochain agent à exécuter basé sur l'état actuel."""
        
        # Si c'est la première fois, créer un plan
        if not state.get("plan"):
            state = self.create_plan(state)
        
        # Vérifier si on a des résultats à analyser
        results = state.get("results", {})
        
        # Si on a des résultats de génération de code mais pas de documentation
        if "code_generation" in results and "documentation" not in results:
            state["next"] = "documentation"
        # Si on a tous les résultats nécessaires, terminer
        elif "code_generation" in results and "documentation" in results:
            state["next"] = "finish"
        # Si on a seulement la documentation, terminer
        elif "documentation" in results and "code_generation" not in results:
            state["next"] = "finish"
        # Par défaut, commencer par la génération de code
        else:
            state["next"] = "code_generation"
        
        return state

# Instance globale du superviseur
supervisor = Supervisor() 