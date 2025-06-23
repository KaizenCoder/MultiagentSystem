import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

try:
    from agent_111_auditeur_qualite_sprint3 import Agent111AuditeurQualiteSprint3
    agent = Agent111AuditeurQualiteSprint3()
    print(f"[OK] Import et initialisation réussis : {agent}")
except Exception as e:
    print(f"[ERREUR] {e}") 