from typing import Dict, Any
from ..graph.state import AgentState

class Supervisor:
    """Agent superviseur qui coordonne les tches entre les agents spcialiss."""
    
    def create_plan(self, state: AgentState) -> AgentState:
        """CORRECTIF 5: Cre un plan de tche bas sur la description - CORRECTION IA-1 ajout testing."""
        task_description = state.get("task_description", "")
        
        # CORRECTION IA-1: Ajout reconnaissance tches testing
        if "diagnose" in task_description.lower() and "postgresql" in task_description.lower():
            plan = "Diagnose PostgreSQL health and common issues."
            state["next"] = "diag_postgresql"
        elif any(keyword in task_description.lower() for keyword in ["test", "testing", "unit test", "pytest", "unittest"]):
            plan = "Create comprehensive tests using testing agent"
            state["next"] = "testing"
        elif any(keyword in task_description.lower() for keyword in ["gemini", "rapid", "prototype", "quick", "fast"]):
            plan = "Use Gemini for rapid prototyping and quick analysis"
            state["next"] = "gemini_rapid"
        elif "code" in task_description.lower() or "python" in task_description.lower() or "generate" in task_description.lower():
            plan = "Generate code solution using code_generation agent, then document with documentation agent"
            state["next"] = "code_generation"
        elif "documentation" in task_description.lower() or "doc" in task_description.lower():
            plan = "Create documentation using documentation agent"
            state["next"] = "documentation"
        else:
            # Plan par dfaut
            plan = "Analyze task and determine appropriate agent for execution"
            state["next"] = "code_generation"
        
        state["plan"] = plan
        state["task_status"] = "in_progress"
        return state
    
    def route(self, state: AgentState) -> Dict[str, Any]:
        """Dtermine le prochain agent  excuter bas sur l'tat actuel."""
        
        # Si c'est la premire fois, crer un plan. Le plan dfinit la premire tape dans "next".
        if not state.get("plan"):
            return self.create_plan(state)
        
        # Analyser les rsultats pour dcider de la prochaine tape.
        results = state.get("results", {})
        
        # Fin de flux pour les tches de diagnostic, test ou Gemini rapide.
        if "diag_postgresql" in results or "testing" in results or "gemini_rapid" in results:
            state["next"] = "finish"
            return state
        
        # Flux de travail Code -> Documentation
        if "code_generation" in results and "documentation" not in results:
            state["next"] = "documentation"
            return state

        # Si la documentation est termine (avec ou sans code), le flux est termin.
        if "documentation" in results:
            state["next"] = "finish"
            return state
        
        # Si aucune condition de routage n'est remplie, on suppose que l'on continue avec le plan
        # initialement dfini, ou que le worker a chou. La boucle retournera au superviseur.
        return state

# Instance globale du superviseur
supervisor = Supervisor() 