#!/usr/bin/env python3
"""
Tests CLI pour validation des agents PostgreSQL harmonisés
Mission: Validation du périmètre POSTGRESQL après harmonisation
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Ajout du chemin racine pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from agents.agent_POSTGRESQL_diagnostic_postgres_final import AgentPostgresqlDiagnosticPostgresFinal
from agents.agent_POSTGRESQL_docker_specialist import AgentPostgresqlDockerSpecialist
from agents.agent_POSTGRESQL_documentation_manager import AgentPostgresqlDocumentationManager
from agents.agent_POSTGRESQL_resolution_finale import AgentPostgresqlResolutionFinale
from agents.agent_POSTGRESQL_sqlalchemy_fixer import AgentPostgresqlSQLAlchemyFixer
from agents.agent_POSTGRESQL_testing_specialist import AgentPostgresqlTestingSpecialist
from agents.agent_POSTGRESQL_web_researcher import AgentPostgresqlWebResearcher
from agents.agent_POSTGRESQL_windows_postgres import AgentPostgresqlWindowsPostgres
from agents.agent_POSTGRESQL_workspace_organizer import AgentPostgresqlWorkspaceOrganizer
from core.agent_factory_architecture import Task

class TestsAgentsPostgreSQL:
    """Tests de validation des agents PostgreSQL harmonisés"""
    
    def __init__(self):
        self.workspace_root = Path(__file__).parent.parent
        self.rapport_tests = {
            "timestamp": datetime.now().isoformat(),
            "mission": "Validation harmonisation périmètre POSTGRESQL",
            "agents_testes": [],
            "tests_reussis": 0,
            "tests_echoues": 0,
            "status": "EN_COURS"
        }
        
    async def test_agent_diagnostic(self):
        """Test de l'agent diagnostic PostgreSQL final"""
        print("\n🔍 Test Agent Diagnostic PostgreSQL Final...")
        try:
            agent = AgentPostgresqlDiagnosticPostgresFinal(self.workspace_root)
            
            # Test health check
            health = await agent.health_check()
            assert health["status"] == "healthy", "Health check échoué"
            
            # Test capacités
            capabilities = agent.get_capabilities()
            assert "diagnostic_conteneur" in capabilities, "Capacité diagnostic_conteneur manquante"
            
            # Test task diagnostic_complet
            task = Task(type="diagnostic_complet", params={})
            result = await agent.execute_task(task)
            
            self.rapport_tests["agents_testes"].append({
                "agent": "diagnostic_postgres_final",
                "health_check": health["status"],
                "capabilities_count": len(capabilities),
                "test_result": result.success,
                "status": "✅ VALIDE" if result.success else "❌ ÉCHEC"
            })
            
            if result.success:
                self.rapport_tests["tests_reussis"] += 1
                print("✅ Agent Diagnostic PostgreSQL - VALIDÉ")
            else:
                self.rapport_tests["tests_echoues"] += 1
                print(f"❌ Agent Diagnostic PostgreSQL - ÉCHEC: {result.error}")
                
        except Exception as e:
            self.rapport_tests["tests_echoues"] += 1
            print(f"❌ Agent Diagnostic PostgreSQL - ERREUR: {e}")
    
    async def test_agent_docker(self):
        """Test de l'agent Docker specialist"""
        print("\n🐳 Test Agent Docker Specialist...")
        try:
            agent = AgentPostgresqlDockerSpecialist(self.workspace_root)
            
            # Test health check
            health = await agent.health_check()
            assert health["status"] == "healthy", "Health check échoué"
            
            # Test capacités
            capabilities = agent.get_capabilities()
            assert "inspect_container" in capabilities, "Capacité inspect_container manquante"
            
            self.rapport_tests["agents_testes"].append({
                "agent": "docker_specialist",
                "health_check": health["status"],
                "capabilities_count": len(capabilities),
                "status": "✅ VALIDE"
            })
            
            self.rapport_tests["tests_reussis"] += 1
            print("✅ Agent Docker Specialist - VALIDÉ")
                
        except Exception as e:
            self.rapport_tests["tests_echoues"] += 1
            print(f"❌ Agent Docker Specialist - ERREUR: {e}")
    
    async def test_agent_web_researcher(self):
        """Test de l'agent Web Researcher"""
        print("\n🌐 Test Agent Web Researcher...")
        try:
            agent = AgentPostgresqlWebResearcher(self.workspace_root)
            
            # Test health check
            health = await agent.health_check()
            assert health["status"] == "healthy", "Health check échoué"
            
            # Test capacités
            capabilities = agent.get_capabilities()
            assert "recherche_github" in capabilities, "Capacité recherche_github manquante"
            
            # Test task recherche_github
            task = Task(type="recherche_github", params={})
            result = await agent.execute_task(task)
            
            self.rapport_tests["agents_testes"].append({
                "agent": "web_researcher",
                "health_check": health["status"],
                "capabilities_count": len(capabilities),
                "test_result": result.success,
                "status": "✅ VALIDE" if result.success else "❌ ÉCHEC"
            })
            
            if result.success:
                self.rapport_tests["tests_reussis"] += 1
                print("✅ Agent Web Researcher - VALIDÉ")
            else:
                self.rapport_tests["tests_echoues"] += 1
                print(f"❌ Agent Web Researcher - ÉCHEC: {result.error}")
                
        except Exception as e:
            self.rapport_tests["tests_echoues"] += 1
            print(f"❌ Agent Web Researcher - ERREUR: {e}")
    
    async def test_tous_les_agents(self):
        """Test de tous les agents PostgreSQL"""
        print("🚀 DÉMARRAGE TESTS AGENTS POSTGRESQL HARMONISÉS")
        print("=" * 60)
        
        # Tests individuels
        await self.test_agent_diagnostic()
        await self.test_agent_docker()
        await self.test_agent_web_researcher()
        
        # Tests rapides pour les autres agents
        agents_restants = [
            ("documentation_manager", AgentPostgresqlDocumentationManager),
            ("resolution_finale", AgentPostgresqlResolutionFinale),
            ("sqlalchemy_fixer", AgentPostgresqlSQLAlchemyFixer),
            ("testing_specialist", AgentPostgresqlTestingSpecialist),
            ("windows_postgres", AgentPostgresqlWindowsPostgres),
            ("workspace_organizer", AgentPostgresqlWorkspaceOrganizer)
        ]
        
        for agent_name, agent_class in agents_restants:
            print(f"\n📋 Test Agent {agent_name}...")
            try:
                agent = agent_class(self.workspace_root)
                health = await agent.health_check()
                capabilities = agent.get_capabilities()
                
                self.rapport_tests["agents_testes"].append({
                    "agent": agent_name,
                    "health_check": health["status"],
                    "capabilities_count": len(capabilities),
                    "status": "✅ VALIDE"
                })
                
                self.rapport_tests["tests_reussis"] += 1
                print(f"✅ Agent {agent_name} - VALIDÉ")
                
            except Exception as e:
                self.rapport_tests["tests_echoues"] += 1
                print(f"❌ Agent {agent_name} - ERREUR: {e}")
                self.rapport_tests["agents_testes"].append({
                    "agent": agent_name,
                    "status": f"❌ ERREUR: {e}"
                })
        
        # Rapport final
        self.generer_rapport_final()
    
    def generer_rapport_final(self):
        """Génération du rapport final de tests"""
        total_tests = self.rapport_tests["tests_reussis"] + self.rapport_tests["tests_echoues"]
        pourcentage_reussite = (self.rapport_tests["tests_reussis"] / total_tests * 100) if total_tests > 0 else 0
        
        self.rapport_tests["status"] = "SUCCESS" if self.rapport_tests["tests_echoues"] == 0 else "PARTIAL_SUCCESS"
        self.rapport_tests["pourcentage_reussite"] = pourcentage_reussite
        
        print("\n" + "=" * 60)
        print("📊 RAPPORT FINAL - TESTS AGENTS POSTGRESQL")
        print("=" * 60)
        print(f"✅ Tests réussis: {self.rapport_tests['tests_reussis']}")
        print(f"❌ Tests échoués: {self.rapport_tests['tests_echoues']}")
        print(f"📈 Taux de réussite: {pourcentage_reussite:.1f}%")
        print(f"🎯 Status global: {self.rapport_tests['status']}")
        
        # Sauvegarde du rapport JSON
        rapport_file = self.workspace_root / "tests" / "rapport_tests_postgresql.json"
        rapport_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(rapport_file, "w", encoding="utf-8") as f:
            json.dump(self.rapport_tests, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rapport sauvegardé: {rapport_file}")

async def main():
    """Point d'entrée principal des tests"""
    tests = TestsAgentsPostgreSQL()
    await tests.test_tous_les_agents()

if __name__ == "__main__":
    asyncio.run(main())
