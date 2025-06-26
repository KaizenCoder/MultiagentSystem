import os
import shutil
import tempfile
from pathlib import Path
import pytest
import sys
import importlib

# On ajoute le chemin des agents pour l'import
AGENTS_DIR = Path(__file__).parent.parent / 'agents'
sys.path.insert(0, str(AGENTS_DIR))

from agent_meta_strategique_scheduler import AgentMetaStrategiqueScheduler
from core.agent_factory_architecture import Task

@pytest.fixture
def temp_workspace():
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

def test_scheduler_universel_with_agent_111_auditeur_qualite(temp_workspace):
    # On passe une tâche reconnue par l'agent (type=execute_mission)
    task = Task(type="execute_mission", params={"mission_data": {"test": True}})
    scheduler = AgentMetaStrategiqueScheduler(
        workspace_root=temp_workspace,
        agent_class_name="Agent111AuditeurQualite",
        agent_module_path="agents.agent_111_auditeur_qualite",
        task_method="execute_task",
        task_params={"task": task}
    )
    # On exécute une analyse quotidienne (async compatible)
    import asyncio
    asyncio.run(scheduler.execute_daily_analysis())
    # Vérifie qu'un artefact a été généré
    artefacts_dir = temp_workspace / 'logs' / 'agents' / 'meta_strategique_scheduler' / 'artefacts'
    artefacts = list(artefacts_dir.glob('artefact_*.json'))
    assert len(artefacts) > 0, "Aucun artefact généré par le scheduler universel avec Agent111AuditeurQualite !"
    # Fermeture explicite des handlers du logger pour éviter le PermissionError
    for handler in scheduler.logger.handlers:
        handler.close()
        scheduler.logger.removeHandler(handler)

def test_scheduler_generates_report(temp_workspace):
    # On instancie le scheduler avec un workspace temporaire
    scheduler = AgentMetaStrategiqueScheduler(workspace_root=temp_workspace)
    # On exécute l'analyse quotidienne (async compatible)
    import asyncio
    asyncio.run(scheduler.execute_daily_analysis())
    # Vérifie qu'un rapport a été généré
    reports_dir = temp_workspace / 'logs' / 'agents' / 'meta_strategique' / 'reports'
    reports = list(reports_dir.glob('REVUE_STRATEGIQUE_*.md'))
    assert len(reports) > 0, "Aucun rapport stratégique généré par le scheduler !"

def test_scheduler_generate_strategic_report_with_agent_111_auditeur_qualite(temp_workspace):
    # On passe une tâche de génération de rapport stratégique
    task = Task(type="generate_strategic_report", params={"test_param": 42})
    scheduler = AgentMetaStrategiqueScheduler(
        workspace_root=temp_workspace,
        agent_class_name="Agent111AuditeurQualite",
        agent_module_path="agents.agent_111_auditeur_qualite",
        task_method="execute_task",
        task_params={"task": task}
    )
    import asyncio
    asyncio.run(scheduler.execute_daily_analysis())
    # Vérifie qu'un rapport a été généré dans le bon dossier
    reports_dir = temp_workspace / 'logs' / 'agents' / 'agent_111_auditeur_qualite' / 'reports'
    reports = list(reports_dir.glob('RAPPORT_STRATEGIQUE_*.md'))
    assert len(reports) > 0, "Aucun rapport stratégique généré par l'agent 111 auditeur qualité !" 