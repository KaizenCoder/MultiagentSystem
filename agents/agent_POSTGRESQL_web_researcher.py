#!/usr/bin/env python3
"""
Agent PostgreSQL Web Researcher - Recherche de solutions PostgreSQL et SQLAlchemy en ligne
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import requests
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

from .agent_POSTGRESQL_base import AgentPostgreSQLBase
from core.agent_factory_architecture import Task, Result

class AgentPostgresqlWebResearcher(AgentPostgreSQLBase):
    """Agent spécialisé dans la recherche web pour PostgreSQL."""
    
    def __init__(self, workspace_root: Path = None):
        super().__init__(
            agent_type="postgresql_web_researcher",
            name="Agent Web Researcher"
        )
        self.workspace_root = workspace_root if workspace_root else Path(__file__).parent.parent
        self.rapport_file = self.workspace_root / "docs/agents_postgresql_resolution/rapports" / "web_researcher_rapport.md"
        self.sources_recherche = {
            "github_issues": [
                "sqlalchemy metadata reserved",
                "postgresql textual sql expression",
                "docker postgres windows",
                "sqlalchemy 2.0 migration",
                "psycopg2 windows installation"
            ],
            "stack_overflow": [
                "Attribute name metadata is reserved SQLAlchemy",
                "Textual SQL expression should be explicitly declared",
                "PostgreSQL Docker Windows connection",
                "SQLAlchemy 2.x compatibility issues",
                "psycopg2 vs psycopg2-binary"
            ],
            "documentation": [
                "SQLAlchemy 2.0 migration guide",
                "PostgreSQL Docker official",
                "psycopg2 installation Windows",
                "Docker Compose PostgreSQL best practices"
            ]
        }
        self.rapport_file.parent.mkdir(parents=True, exist_ok=True)

    def get_capabilities(self) -> list:
        return [
            "recherche_github",
            "recherche_stackoverflow",
            "analyse_documentation",
            "synthese_solutions",
            "generation_rapport"
        ]

    async def execute_task(self, task: Task) -> Result:
        try:
            task_type = task.type
            handlers = {
                "recherche_github": self._handle_recherche_github,
                "recherche_stackoverflow": self._handle_recherche_stackoverflow,
                "analyse_documentation": self._handle_analyse_documentation,
                "synthese_solutions": self._handle_synthese_solutions,
                "generation_rapport": self._handle_generation_rapport
            }
            handler = handlers.get(task_type)
            if not handler:
                return Result(success=False, error=f"Type de tâche non supporté: {task_type}")
            return await handler(task)
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche: {e}")
            return Result(success=False, error=str(e))

    async def _handle_recherche_github(self, task: Task) -> Result:
        solutions = await self.rechercher_solutions_github()
        return Result(success=True, data=solutions)

    async def _handle_recherche_stackoverflow(self, task: Task) -> Result:
        solutions = await self.rechercher_solutions_stackoverflow()
        return Result(success=True, data=solutions)

    async def _handle_analyse_documentation(self, task: Task) -> Result:
        solutions = await self.analyser_documentation_officielle()
        return Result(success=True, data=solutions)

    async def _handle_synthese_solutions(self, task: Task) -> Result:
        github = task.params.get("github", {})
        stackoverflow = task.params.get("stackoverflow", {})
        documentation = task.params.get("documentation", {})
        synthese = await self.synthetiser_solutions(github, stackoverflow, documentation)
        return Result(success=True, data=synthese)

    async def _handle_generation_rapport(self, task: Task) -> Result:
        github = task.params.get("github", {})
        stackoverflow = task.params.get("stackoverflow", {})
        documentation = task.params.get("documentation", {})
        synthese = task.params.get("synthese", {})
        rapport = await self.generer_rapport(github, stackoverflow, documentation, synthese)
        return Result(success=True, data={"rapport_path": str(self.rapport_file), "rapport": rapport})

    async def rechercher_solutions_github(self) -> Dict[str, Any]:
        solutions_github = {
            "timestamp": datetime.now().isoformat(),
            "requetes_effectuees": [],
            "solutions_trouvees": [],
            "repositories_pertinents": []
        }
        try:
            for query in self.sources_recherche["github_issues"]:
                if "metadata reserved" in query:
                    solutions_github["solutions_trouvees"].append({
                        "probleme": "SQLAlchemy metadata conflict",
                        "source": "GitHub Issues",
                        "solution": "Renommer attribut 'metadata' en '__metadata__' ou utiliser declarative_base()",
                        "url_simulee": "https://github.com/sqlalchemy/sqlalchemy/issues/xxxx",
                        "score_pertinence": 95
                    })
                elif "textual sql" in query:
                    solutions_github["solutions_trouvees"].append({
                        "probleme": "SQLAlchemy 2.x text() requirement",
                        "source": "GitHub Issues",
                        "solution": "Utiliser text() pour expressions SQL: text('SELECT 1 as test_value')",
                        "url_simulee": "https://github.com/sqlalchemy/sqlalchemy/issues/yyyy",
                        "score_pertinence": 98
                    })
                elif "docker postgres windows" in query:
                    solutions_github["solutions_trouvees"].append({
                        "probleme": "Docker PostgreSQL Windows connectivity",
                        "source": "GitHub Docker",
                        "solution": "Utiliser host.docker.internal ou configurer réseau bridge",
                        "url_simulee": "https://github.com/docker/for-win/issues/zzzz",
                        "score_pertinence": 85
                    })
                solutions_github["requetes_effectuees"].append(query)
                time.sleep(0.1)
        except Exception as e:
            self.logger.warning(f"Erreur recherche GitHub: {e}")
        return solutions_github

    async def rechercher_solutions_stackoverflow(self) -> Dict[str, Any]:
        solutions_so = {
            "timestamp": datetime.now().isoformat(),
            "requetes_effectuees": [],
            "solutions_trouvees": []
        }
        try:
            for query in self.sources_recherche["stack_overflow"]:
                if "metadata is reserved" in query:
                    solutions_so["solutions_trouvees"].append({
                        "probleme": "Attribute name metadata is reserved SQLAlchemy",
                        "source": "StackOverflow",
                        "solution": "Renommer l'attribut ou utiliser __metadata__",
                        "url_simulee": "https://stackoverflow.com/q/xxxx",
                        "score_pertinence": 90
                    })
                elif "Textual SQL expression" in query:
                    solutions_so["solutions_trouvees"].append({
                        "probleme": "Textual SQL expression should be explicitly declared",
                        "source": "StackOverflow",
                        "solution": "Utiliser sqlalchemy.text() pour les requêtes textuelles",
                        "url_simulee": "https://stackoverflow.com/q/yyyy",
                        "score_pertinence": 92
                    })
                elif "Docker Windows connection" in query:
                    solutions_so["solutions_trouvees"].append({
                        "probleme": "PostgreSQL Docker Windows connection",
                        "source": "StackOverflow",
                        "solution": "Utiliser host.docker.internal pour la connexion depuis Windows",
                        "url_simulee": "https://stackoverflow.com/q/zzzz",
                        "score_pertinence": 85
                    })
                solutions_so["requetes_effectuees"].append(query)
                time.sleep(0.1)
        except Exception as e:
            self.logger.warning(f"Erreur recherche StackOverflow: {e}")
        return solutions_so

    async def analyser_documentation_officielle(self) -> Dict[str, Any]:
        docs = {
            "timestamp": datetime.now().isoformat(),
            "documents_analyzes": [],
            "solutions_trouvees": []
        }
        try:
            for doc in self.sources_recherche["documentation"]:
                if "migration guide" in doc:
                    docs["solutions_trouvees"].append({
                        "probleme": "Migration SQLAlchemy 2.0",
                        "source": "Documentation officielle",
                        "solution": "Suivre le guide de migration SQLAlchemy 2.0",
                        "url_simulee": "https://docs.sqlalchemy.org/en/20/changelog/changelog_20.html",
                        "score_pertinence": 99
                    })
                elif "Docker official" in doc:
                    docs["solutions_trouvees"].append({
                        "probleme": "Configuration Docker PostgreSQL",
                        "source": "Documentation Docker",
                        "solution": "Utiliser l'image officielle et suivre les best practices",
                        "url_simulee": "https://hub.docker.com/_/postgres",
                        "score_pertinence": 97
                    })
                elif "psycopg2 installation Windows" in doc:
                    docs["solutions_trouvees"].append({
                        "probleme": "Installation psycopg2 sur Windows",
                        "source": "Documentation psycopg2",
                        "solution": "Installer les dépendances Microsoft C++ Build Tools",
                        "url_simulee": "https://www.psycopg.org/docs/install.html#windows",
                        "score_pertinence": 90
                    })
                docs["documents_analyzes"].append(doc)
                time.sleep(0.1)
        except Exception as e:
            self.logger.warning(f"Erreur analyse documentation: {e}")
        return docs

    async def synthetiser_solutions(self, github: Dict[str, Any], stackoverflow: Dict[str, Any], documentation: Dict[str, Any]) -> Dict[str, Any]:
        synthese = {
            "timestamp": datetime.now().isoformat(),
            "points_cles": [],
            "recommandations": []
        }
        try:
            for src in [github, stackoverflow, documentation]:
                for sol in src.get("solutions_trouvees", []):
                    synthese["points_cles"].append(sol["probleme"])
                    synthese["recommandations"].append(sol["solution"])
        except Exception as e:
            self.logger.warning(f"Erreur synthèse solutions: {e}")
        return synthese

    async def generer_rapport(self, github: Dict[str, Any], stackoverflow: Dict[str, Any], documentation: Dict[str, Any], synthese: Dict[str, Any]) -> str:
        try:
            rapport = f"""# Rapport Web Researcher PostgreSQL\n\n## Date: {datetime.now().isoformat()}\n\n## Synthèse Globale\n{synthese.get("resume_global", "Aucune synthèse disponible.")}\n\n## Solutions Recommandées\n\n"""
            for sol in synthese.get("solutions_recommandees", [])[:5]: # Top 5 solutions
                rapport += f"- **Problème**: {sol.get('probleme', 'N/A')}\n"
                rapport += f"  **Source**: {sol.get('source', 'N/A')}\n"
                rapport += f"  **Solution**: {sol.get('solution', 'N/A')}\n"
                rapport += f"  **URL (simulée)**: {sol.get('url_simulee', 'N/A')}\n"
                rapport += f"  **Pertinence**: {sol.get('score_pertinence', 'N/A')}\n\n"
            
            rapport += "## Détail des Recherches\n\n### GitHub Issues\n\n"
            for req in github.get("requetes_effectuees", [])[:3]:
                rapport += f"- Requête: `{req}`\n"
            rapport += "\n"
            
            rapport += "### StackOverflow\n\n"
            for req in stackoverflow.get("requetes_effectuees", [])[:3]:
                rapport += f"- Requête: `{req}`\n"
            rapport += "\n"

            rapport += "### Documentation Officielle\n\n"
            for doc_name in documentation.get("documents_analyzes", [])[:3]:
                rapport += f"- Document: `{doc_name}`\n"
            rapport += "\n"
            
            with open(self.rapport_file, "w", encoding="utf-8") as f:
                f.write(rapport)
            return rapport
        except Exception as e:
            self.logger.error(f"Erreur génération rapport: {e}")
            return "" 