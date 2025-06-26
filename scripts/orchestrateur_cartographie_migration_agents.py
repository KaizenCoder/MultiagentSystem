import asyncio
import sys
from pathlib import Path
import logging
import json
from datetime import datetime

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger("OrchestrateurCartographiePostgreSQL")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    # Import des agents PostgreSQL
    from agents.agent_POSTGRESQL_diagnostic_postgres_final import AgentDiagnosticPostgreSQL
    from agents.agent_POSTGRESQL_docker_specialist import AgentPostgreSQLDocker
    from agents.agent_POSTGRESQL_documentation_manager import AgentPostgreSQLDocumentation
    from agents.agent_POSTGRESQL_resolution_finale import AgentPostgreSQLResolution
    from agents.agent_POSTGRESQL_sqlalchemy_fixer import AgentSQLAlchemyFixer
    from agents.agent_POSTGRESQL_testing_specialist import PostgreSQLTestingSpecialist
    from agents.agent_POSTGRESQL_web_researcher import PostgreSQLWebResearcherAgent
    from agents.agent_POSTGRESQL_windows_postgres import AgentWindowsPostgreSQL
    from agents.agent_POSTGRESQL_workspace_organizer import AgentPostgreSQLWorkspace
    
    # Agents de support
    from agents.agent_111_auditeur_qualite import Agent111AuditeurQualite
    from agents.agent_110_documentaliste_expert import Agent110DocumentalisteExpert
    from agents.agent_14_specialiste_workspace import Agent14SpecialisteWorkspace
    from agents.agent_05_maitre_tests_validation import Agent05MaitreTests
    
    # Agents de cartographie
    from agents.cartographie_assistants.agent_cartographe_principal import AgentCartographePrincipal
    from agents.cartographie_assistants.agent_analyseur_code_python import AgentAnalyseurCodePython
    from agents.cartographie_assistants.agent_analyseur_documentation_markdown import AgentAnalyseurDocumentationMarkdown
    from agents.cartographie_assistants.agent_comparateur_synchroniseur import AgentComparateurSynchroniseur
    from agents.cartographie_assistants.agent_lecteur_workflow import AgentLecteurWorkflow

except ImportError as e:
    log.error(f"Erreur d'importation des agents : {e}")
    sys.exit(1)

class OrchestrateurCartographiePostgreSQL:
    """
    Orchestrateur spécialisé pour la cartographie des agents PostgreSQL.
    Coordonne l'analyse, la validation et la documentation des agents
    PostgreSQL selon SUIVI_MIGRATION_AGENTS.md.
    """

    def __init__(self):
        self.agents = {}
        self.suivi_migration_path = PROJECT_ROOT / "agents_migration_workspace" / "SUIVI_MIGRATION_AGENTS.md"
        self.reports_path = PROJECT_ROOT / "reports" / "cartographie_postgresql"
        self.reports_path.mkdir(parents=True, exist_ok=True)

    def initialiser_agents(self):
        """Initialise les agents nécessaires pour la cartographie PostgreSQL."""
        try:
            # Agents PostgreSQL principaux
            self.agents["diagnostic"] = AgentDiagnosticPostgreSQL()
            self.agents["docker"] = AgentPostgreSQLDocker()
            self.agents["documentation"] = AgentPostgreSQLDocumentation()
            self.agents["resolution"] = AgentPostgreSQLResolution()
            self.agents["sqlalchemy"] = AgentSQLAlchemyFixer()
            self.agents["testing"] = PostgreSQLTestingSpecialist()
            self.agents["web_researcher"] = PostgreSQLWebResearcherAgent()
            self.agents["windows"] = AgentWindowsPostgreSQL()
            self.agents["workspace"] = AgentPostgreSQLWorkspace()

            # Agents de support
            self.agents["auditeur_qualite"] = Agent111AuditeurQualite()
            self.agents["documentaliste"] = Agent110DocumentalisteExpert()
            self.agents["specialiste_workspace"] = Agent14SpecialisteWorkspace()
            self.agents["maitre_tests"] = Agent05MaitreTests()
            
            # Agents de cartographie
            self.agents["cartographe"] = AgentCartographePrincipal()
            self.agents["analyseur_code"] = AgentAnalyseurCodePython()
            self.agents["analyseur_doc"] = AgentAnalyseurDocumentationMarkdown()
            self.agents["comparateur"] = AgentComparateurSynchroniseur()
            self.agents["lecteur_workflow"] = AgentLecteurWorkflow()

            log.info("Agents initialisés avec succès")

        except Exception as e:
            log.error(f"Erreur lors de l'initialisation des agents : {e}")
            raise

    def analyser_suivi_migration(self):
        """Analyse le fichier SUIVI_MIGRATION_AGENTS.md pour les agents PostgreSQL."""
        try:
            workflow = self.agents["lecteur_workflow"].analyser_fichier(self.suivi_migration_path)
            log.info("Analyse du fichier de suivi terminée")
            return workflow
        except Exception as e:
            log.error(f"Erreur lors de l'analyse du suivi : {e}")
            raise

    def cartographier_agents_postgresql(self):
        """Cartographie complète des agents PostgreSQL."""
        try:
            # Analyse du workflow de migration
            workflow = self.analyser_suivi_migration()
            
            # Cartographie des agents PostgreSQL
            resultats = {}
            for agent_name, agent in self.agents.items():
                if agent_name in ["diagnostic", "docker", "documentation", "resolution", 
                                "sqlalchemy", "testing", "web_researcher", "windows", "workspace"]:
                    # Analyse du code
                    code_analysis = self.agents["analyseur_code"].analyser_agent(agent)
                    
                    # Analyse de la documentation
                    doc_analysis = self.agents["analyseur_doc"].analyser_documentation(agent)
                    
                    # Tests et validation
                    test_results = self.agents["maitre_tests"].executer_tests(agent)
                    
                    # Audit qualité
                    audit_results = self.agents["auditeur_qualite"].auditer_agent(agent)
                    
                    resultats[agent_name] = {
                        "code_analysis": code_analysis,
                        "doc_analysis": doc_analysis,
                        "test_results": test_results,
                        "audit_results": audit_results
                    }
            
            # Comparaison et synchronisation
            rapport_final = self.agents["comparateur"].comparer_resultats(resultats, workflow)
            
            # Génération documentation
            self.agents["documentaliste"].generer_documentation(rapport_final)
            
            return rapport_final
            
        except Exception as e:
            log.error(f"Erreur lors de la cartographie : {e}")
            raise

    def executer_cartographie(self):
        """Point d'entrée principal pour l'exécution de la cartographie."""
        try:
            # Initialisation des agents
            self.initialiser_agents()
            
            # Cartographie des agents
            rapport = self.cartographier_agents_postgresql()
            
            # Sauvegarde du rapport
            rapport_path = self.reports_path / f"cartographie_postgresql_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(rapport_path, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, ensure_ascii=False, indent=2)
            
            log.info(f"Cartographie terminée. Rapport sauvegardé : {rapport_path}")
            return rapport
            
        except Exception as e:
            log.error(f"Erreur lors de l'exécution : {e}")
            raise

if __name__ == "__main__":
    try:
        orchestrateur = OrchestrateurCartographiePostgreSQL()
        orchestrateur.executer_cartographie()
    except Exception as e:
        log.error(f"Erreur fatale : {e}")
        sys.exit(1) 