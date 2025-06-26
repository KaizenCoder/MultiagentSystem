#!/usr/bin/env python3
"""
Script de lancement de missions pour tous les agents PostgreSQL
"""
import asyncio
from pathlib import Path
from .agent_POSTGRESQL_diagnostic_postgres_final import AgentPostgresqlDiagnosticPostgresFinal
from .agent_POSTGRESQL_docker_specialist import AgentPostgresqlDockerSpecialist
from .agent_POSTGRESQL_documentation_manager import AgentPostgresqlDocumentationManager
from .agent_POSTGRESQL_resolution_finale import AgentPostgresqlResolutionFinale
from .agent_POSTGRESQL_sqlalchemy_fixer import AgentPostgresqlSQLAlchemyFixer
from .agent_POSTGRESQL_testing_specialist import AgentPostgresqlTestingSpecialist
from .agent_POSTGRESQL_web_researcher import AgentPostgresqlWebResearcher
from .agent_POSTGRESQL_windows_postgres import AgentPostgresqlWindowsPostgres
from .agent_POSTGRESQL_workspace_organizer import AgentPostgresqlWorkspaceOrganizer
from core.agent_factory_architecture import Task

async def run_all_agents():
    workspace = Path(__file__).parent.parent
    agents = [
        AgentPostgresqlDiagnosticPostgresFinal(workspace),
        AgentPostgresqlDockerSpecialist(workspace),
        AgentPostgresqlDocumentationManager(workspace),
        AgentPostgresqlResolutionFinale(workspace),
        AgentPostgresqlSQLAlchemyFixer(workspace),
        AgentPostgresqlTestingSpecialist(workspace),
        AgentPostgresqlWebResearcher(workspace),
        AgentPostgresqlWindowsPostgres(workspace),
        AgentPostgresqlWorkspaceOrganizer(workspace)
    ]
    missions = [
        Task(type="diagnostic_conteneur", params={}),
        Task(type="inspect_container", params={}),
        Task(type="generate_report", params={}),
        Task(type="propose_solution", params={"problem_id": "test"}),
        Task(type="diagnose_sqlalchemy", params={"models_path": "models/"}),
        Task(type="create_test_suite", params={}),
        Task(type="recherche_github", params={}),
        Task(type="diagnostiquer_windows", params={}),
        Task(type="analyser_structure_workspace", params={})
    ]
    rapports = []
    for agent, mission in zip(agents, missions):
        result = await agent.execute_task(mission)
        rapport_path = getattr(agent, "rapport_file", None)
        if rapport_path and Path(rapport_path).exists():
            with open(rapport_path, "r", encoding="utf-8") as f:
                rapport = f.read()
        else:
            rapport = str(result.data) if result.success else result.error
        rapports.append({"agent": agent.name, "rapport": rapport})
    return rapports

if __name__ == "__main__":
    rapports = asyncio.run(run_all_agents())
    for r in rapports:
        print(f"\n===== Rapport de {r['agent']} =====\n{r['rapport']}\n") 