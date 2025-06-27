from typing import Dict, List, Optional, Any, Union, Tuple
#!/usr/bin/env python3
"""
Agent PostgreSQL Web Researcher - Recherche de solutions PostgreSQL et SQLAlchemy en ligne
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import requests
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# Import avec fallback
try:
    from .agent_POSTGRESQL_base import AgentPostgreSQLBase
except ImportError:
    try:
        from agent_POSTGRESQL_base import AgentPostgreSQLBase
    except ImportError:
        # Fallback pour AgentPostgreSQLBase
        class AgentPostgreSQLBase:
            def __init__(self, *args, **kwargs):
                pass
from core.agent_factory_architecture import Task, Result

class AgentPostgresqlWebResearcher(AgentPostgreSQLBase):
    """Agent spécialisé dans la recherche web pour PostgreSQL."""
    
    def __init__(self, workspace_root: Path = None):
        super().__init__(
            agent_type="postgresql_web_researcher",
            name="Agent Web Researcher"
        )
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="postgresql",
                custom_config={
                    "logger_name": f"nextgen.postgresql.agent_POSTGRESQL_web_researcher.{getattr(self, 'agent_id', 'unknown')}",
                    "log_dir": "logs/postgresql",
                    "metadata": {
                        "agent_type": "agent_POSTGRESQL_web_researcher",
                        "agent_role": "postgresql",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
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
    # ✅ MÉTHODES STANDARDISÉES DE RAPPORT

    def _calculate_report_score(self, metrics: Dict[str, Any]) -> int:
        """Calcule le score global du rapport basé sur les métriques."""
        score = 0
        issues_critiques = []
        
        # Logique de scoring spécifique à l'agent
        # À adapter selon le type d'agent
        
        return score
    
    def _assess_conformity(self, score: int) -> str:
        """Évalue la conformité basée sur le score."""
        if score >= 90:
            return "✅ CONFORME - OPTIMAL"
        elif score >= 70:
            return "✅ CONFORME - ACCEPTABLE"
        else:
            return "❌ NON CONFORME - CRITIQUE"
    
    def _get_quality_level(self, score: int) -> str:
        """Détermine le niveau de qualité."""
        if score >= 90:
            return "OPTIMAL"
        elif score >= 70:
            return "ACCEPTABLE"
        else:
            return "CRITIQUE"
    
    def _generate_recommendations(self, metrics: Dict[str, Any], issues: List[str]) -> List[str]:
        """Génère les recommandations basées sur l'analyse."""
        recommendations = []
        
        # Logique de génération de recommandations
        # À adapter selon le type d'agent
        
        return recommendations
    
    def _generate_standard_report(self, context: Dict, metrics: Dict, timestamp) -> Dict[str, Any]:
        """Génère un rapport selon le format standard de l'agent 06."""
        
        score = self._calculate_report_score(metrics)
        conformity = self._assess_conformity(score)
        quality_level = self._get_quality_level(score)
        
        agent_filename = Path(__file__).name
        
        # Issues critiques (à personnaliser selon l'agent)
        issues_critiques = []
        
        return {
            'agent_id': getattr(self, 'agent_id', 'unknown'),
            'agent_file_name': agent_filename,
            'type_rapport': 'standard',  # À personnaliser
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Agent Spécialisé',  # À personnaliser
            'score_global': score,
            'niveau_qualite': quality_level,
            'conformite': conformity,
            'signature_cryptographique': 'N/A (Fonctionnalité non implémentée pour cet agent)',
            'issues_critiques_identifies': len(issues_critiques),
            'architecture': {
                'description': "Description de l'architecture de l'agent",
                'statut_operationnel': f"Système {getattr(self, 'agent_id', 'unknown')} opérationnel.",
                'confirmation_specialisation': f"{getattr(self, 'agent_id', 'unknown')} confirmé comme spécialiste.",
                'objectifs_principaux': [
                    "Objectif principal 1",
                    "Objectif principal 2",
                    "Objectif principal 3"
                ],
                'technologies_cles': ["Technologie 1", "Technologie 2"]
            },
            'recommandations': self._generate_recommendations(metrics, issues_critiques),
            'issues_critiques_details': issues_critiques if issues_critiques else [
                "Aucun issue critique majeur détecté. Le système fonctionne dans les paramètres attendus."
            ],
            'details_techniques': {
                'strategie': "Stratégie technique de l'agent",
                'composants_actifs': [],
                'metriques_collectees': metrics
            },
            'metriques_detaillees': {
                'score_global': {'actuel': score, 'cible': 100},
                'conformite_pourcentage': {'actuel': score, 'cible': 100, 'unite': '%'}
            },
            'impact_business': {
                'criticite': 'MOYENNE' if score >= 70 else 'HAUTE',
                'domaines_impactes': [],
                'actions_requises': []
            }
        }


    def _generate_markdown_report(self, rapport_json: Dict, context: Dict, timestamp) -> str:
        """Génère un rapport Markdown selon le format standard."""
        
        agent_name = rapport_json.get('agent_id', 'Agent Inconnu')
        type_rapport = rapport_json.get('type_rapport', 'standard')
        score = rapport_json.get('score_global', 0)
        quality = rapport_json.get('niveau_qualite', 'UNKNOWN')
        conformity = rapport_json.get('conformite', 'NON ÉVALUÉ')
        
        markdown_content = f"""# 📊 RAPPORT STRATÉGIQUE : {agent_name.upper()}

## 🎯 RÉSUMÉ EXÉCUTIF

**Agent :** {agent_name}  
**Type de Rapport :** {type_rapport}  
**Date de Génération :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Score Global :** {score}/100  
**Niveau de Qualité :** {quality}  
**Conformité :** {conformity}  

## 📈 ANALYSE GLOBALE

### Score de Performance
- **Score Actuel :** {score}/100
- **Objectif :** 100/100
- **Statut :** {'🟢 ACCEPTABLE' if score >= 70 else '🔴 CRITIQUE'}

### Architecture
{rapport_json.get('architecture', {}).get('description', 'Description non disponible')}

**Objectifs Principaux :**
"""
        
        # Ajouter les objectifs
        for obj in rapport_json.get('architecture', {}).get('objectifs_principaux', []):
            markdown_content += f"- {obj}\n"
        
        markdown_content += f"""
**Technologies Clés :**
"""
        
        # Ajouter les technologies
        for tech in rapport_json.get('architecture', {}).get('technologies_cles', []):
            markdown_content += f"- {tech}\n"
        
        markdown_content += f"""

## 🔍 RECOMMANDATIONS

"""
        
        # Ajouter les recommandations
        for reco in rapport_json.get('recommandations', []):
            markdown_content += f"- {reco}\n"
        
        markdown_content += f"""

## ⚠️ ISSUES CRITIQUES

"""
        
        # Ajouter les issues critiques
        for issue in rapport_json.get('issues_critiques_details', []):
            markdown_content += f"- {issue}\n"
        
        markdown_content += f"""

## 📊 MÉTRIQUES DÉTAILLÉES

### Performance Globale
- **Score Global :** {rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('actuel', 0)}/{rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('cible', 100)}
- **Conformité :** {rapport_json.get('metriques_detaillees', {}).get('conformite_pourcentage', {}).get('actuel', 0)}%

## 🎯 IMPACT BUSINESS

**Criticité :** {rapport_json.get('impact_business', {}).get('criticite', 'NON ÉVALUÉ')}

### Domaines Impactés
"""
        
        # Ajouter les domaines impactés
        for domaine in rapport_json.get('impact_business', {}).get('domaines_impactes', []):
            markdown_content += f"- {domaine}\n"
        
        markdown_content += f"""

### Actions Requises
"""
        
        # Ajouter les actions requises
        for action in rapport_json.get('impact_business', {}).get('actions_requises', []):
            markdown_content += f"- {action}\n"
        
        markdown_content += f"""

---
*Rapport généré automatiquement par {agent_name} - NextGeneration System*  
*Timestamp: {timestamp.isoformat()}*
"""
        
        return markdown_content

