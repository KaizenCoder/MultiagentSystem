import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

try:
    from agent_analyse_solution_chatgpt import AgentAnalyseSolutionChatGPT
    agent = AgentAnalyseSolutionChatGPT()
    print(f"[OK] Import et initialisation réussis : {agent}")
except Exception as e:
    print(f"[ERREUR] {e}") 