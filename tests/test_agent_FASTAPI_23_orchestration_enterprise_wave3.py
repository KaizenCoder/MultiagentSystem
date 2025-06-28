#!/usr/bin/env python3
"""
🧪 TESTS EXHAUSTIFS - Agent FastAPI Orchestration Enterprise NextGeneration Wave 3
================================================================================

Suite de tests validation NON-RÉGRESSION ABSOLUE pour agent_FASTAPI_23_orchestration_enterprise

🎯 Objectif : Garantir 100% des fonctionnalités préservées + nouvelles capacités
⚡ Scope : 36+ tests couvrant toutes les capacités et patterns

Author: Équipe de Maintenance NextGeneration
Version: 5.3.0 - Wave 3 Enterprise Pillar
Updated: 2025-06-28 - Tests Validation Migration
"""

import asyncio
import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import sys
import time

# Configuration robuste du chemin d'importation
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from agents.agent_FASTAPI_23_orchestration_enterprise import (
    Agent23FastAPIOrchestrationEnterprise,
    create_agent_23_enterprise,
    FastAPIMetrics,
    FastAPIIssue,
    __version__,
    __agent_name__,
    __wave_version__,
    __nextgen_patterns__
)
from core.agent_factory_architecture import Agent, Task, Result

class TestAgent23FastAPIOrchestrationEnterprise:
    """🧪 Tests exhaustifs Agent FastAPI Orchestration Enterprise"""

    @pytest.fixture
    def temp_workspace(self):
        """🗂️ Workspace temporaire pour tests"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def agent_config(self, temp_workspace):
        """⚙️ Configuration agent pour tests"""
        return {
            'workspace_dir': str(temp_workspace),
            'authentication': {'provider': 'oauth2', 'jwt_secret': 'test_secret'},
            'rate_limiting': {'requests_per_minute': 1000},
            'documentation': {'openapi_version': '3.0.0'},
            'monitoring': {'prometheus_enabled': True},
            'security': {'headers_enabled': True}
        }

    @pytest.fixture
    async def agent(self, agent_config):
        """🤖 Instance agent pour tests"""
        agent = create_agent_23_enterprise(**agent_config)
        await agent.startup()
        yield agent
        await agent.shutdown()

    # === Tests de Base - Conformité Pattern Factory ===

    def test_agent_creation_basic(self):
        """✅ Test 1: Création agent de base"""
        agent = create_agent_23_enterprise()
        assert agent is not None
        assert isinstance(agent, Agent23FastAPIOrchestrationEnterprise)
        assert isinstance(agent, Agent)
        assert agent.agent_version == __version__
        assert agent.agent_name == __agent_name__

    def test_agent_metadata_nextgeneration(self):
        """✅ Test 2: Métadonnées NextGeneration"""
        agent = create_agent_23_enterprise()
        assert agent.wave_version == __wave_version__
        assert agent.nextgen_patterns == __nextgen_patterns__
        assert "LLM_ENHANCED" in agent.nextgen_patterns
        assert "ENTERPRISE_READY" in agent.nextgen_patterns
        assert "PATTERN_FACTORY" in agent.nextgen_patterns

    def test_agent_capabilities_complete(self):
        """✅ Test 3: Capacités complètes"""
        agent = create_agent_23_enterprise()
        capabilities = agent.get_capabilities()
        
        # Capacités de base préservées
        base_capabilities = [
            "authentication_setup", "rate_limiting_config", "api_documentation",
            "monitoring_setup", "security_enhancement", "performance_optimization"
        ]
        for cap in base_capabilities:
            assert cap in capabilities, f"Capacité de base manquante: {cap}"
        
        # Nouvelles capacités NextGeneration
        nextgen_capabilities = [
            "fastapi_patterns_analysis", "architecture_optimization",
            "middleware_orchestration", "enterprise_security_audit"
        ]
        for cap in nextgen_capabilities:
            assert cap in capabilities, f"Capacité NextGeneration manquante: {cap}"
        
        # Minimum 12 capacités
        assert len(capabilities) >= 12

    def test_features_initialization(self, agent_config):
        """✅ Test 4: Initialisation features"""
        agent = create_agent_23_enterprise(**agent_config)
        assert len(agent.features) == 5
        feature_names = [f.__class__.__name__ for f in agent.features]
        expected_features = [
            "AuthenticationFeature", "RateLimitingFeature", 
            "DocumentationFeature", "MonitoringFeature", "SecurityFeature"
        ]
        for expected in expected_features:
            assert expected in feature_names

    def test_metrics_initialization(self):
        """✅ Test 5: Initialisation métriques"""
        agent = create_agent_23_enterprise()
        assert isinstance(agent.metrics, FastAPIMetrics)
        assert agent.metrics.authentication_score == 0.0
        assert agent.metrics.overall_orchestration_score == 0.0
        assert agent.metrics.apis_configured == 0

    # === Tests Lifecycle - Startup/Shutdown ===

    @pytest.mark.asyncio
    async def test_startup_sequence(self, agent_config, temp_workspace):
        """✅ Test 6: Séquence démarrage"""
        agent = create_agent_23_enterprise(**agent_config)
        
        # État initial
        assert agent.status != "running"
        
        # Démarrage
        start_time = time.time()
        await agent.startup()
        startup_time = time.time() - start_time
        
        # Validation post-startup
        assert agent.status == "running"
        assert startup_time < 2.0  # Démarrage rapide
        
        # Validation environnement
        assert agent.workspace_dir.exists()
        assert agent.reports_dir.exists()
        
        await agent.shutdown()

    @pytest.mark.asyncio
    async def test_shutdown_sequence(self, agent):
        """✅ Test 7: Séquence arrêt"""
        assert agent.status == "running"
        
        await agent.shutdown()
        assert agent.status == "stopped"

    @pytest.mark.asyncio
    async def test_startup_reports_generation(self, agent_config, temp_workspace):
        """✅ Test 8: Génération rapports démarrage"""
        agent = create_agent_23_enterprise(**agent_config)
        await agent.startup()
        
        # Vérification existence rapports
        reports_dir = temp_workspace / 'reports' / 'agents'
        startup_reports = list(reports_dir.glob('startup_agent23_*.json'))
        assert len(startup_reports) >= 1
        
        # Validation contenu rapport
        with open(startup_reports[0], 'r') as f:
            report = json.load(f)
        
        assert 'agent_info' in report
        assert 'startup_metrics' in report
        assert report['agent_info']['version'] == __version__
        
        await agent.shutdown()

    # === Tests Exécution Tâches - Capacités de Base ===

    @pytest.mark.asyncio
    async def test_authentication_setup_task(self, agent):
        """✅ Test 9: Tâche authentication_setup"""
        task = Task(type="authentication_setup", params={"provider": "oauth2"})
        result = await agent.execute_task(task)
        
        assert result.success
        assert result.agent_id == agent.id
        assert "execution_time_ms" in result.metrics
        assert result.metrics["llm_enhanced"] is True

    @pytest.mark.asyncio
    async def test_rate_limiting_config_task(self, agent):
        """✅ Test 10: Tâche rate_limiting_config"""
        task = Task(type="rate_limiting_config", params={"limit": 100})
        result = await agent.execute_task(task)
        
        assert result.success
        assert result.agent_id == agent.id
        assert "wave_version" in result.metrics

    @pytest.mark.asyncio
    async def test_api_documentation_task(self, agent):
        """✅ Test 11: Tâche api_documentation"""
        task = Task(type="api_documentation", params={"format": "openapi"})
        result = await agent.execute_task(task)
        
        assert result.success
        assert "nextgen_patterns" in result.metrics

    @pytest.mark.asyncio
    async def test_monitoring_setup_task(self, agent):
        """✅ Test 12: Tâche monitoring_setup"""
        task = Task(type="monitoring_setup", params={"prometheus": True})
        result = await agent.execute_task(task)
        
        assert result.success

    @pytest.mark.asyncio
    async def test_security_enhancement_task(self, agent):
        """✅ Test 13: Tâche security_enhancement"""
        task = Task(type="security_enhancement", params={"level": "high"})
        result = await agent.execute_task(task)
        
        assert result.success

    @pytest.mark.asyncio
    async def test_performance_optimization_task(self, agent):
        """✅ Test 14: Tâche performance_optimization"""
        task = Task(type="performance_optimization", params={"target": "latency"})
        result = await agent.execute_task(task)
        
        assert result.success

    # === Tests Capacités NextGeneration LLM Enhanced ===

    @pytest.mark.asyncio
    async def test_fastapi_patterns_analysis(self, agent):
        """✅ Test 15: Analyse patterns FastAPI"""
        task = Task(type="fastapi_patterns_analysis", params={"target": "test_api"})
        result = await agent.execute_task(task)
        
        assert result.success
        assert "patterns_detected" in result.data
        assert "recommendations" in result.data
        assert "score" in result.data
        assert isinstance(result.data["score"], (int, float))
        assert result.data["score"] > 0

    @pytest.mark.asyncio
    async def test_architecture_optimization(self, agent):
        """✅ Test 16: Optimisation architecture"""
        task = Task(type="architecture_optimization", params={"scope": "microservices"})
        result = await agent.execute_task(task)
        
        assert result.success
        assert "microservices_patterns" in result.data
        assert "performance_improvements" in result.data
        assert "scalability_enhancements" in result.data

    @pytest.mark.asyncio
    async def test_middleware_orchestration(self, agent):
        """✅ Test 17: Orchestration middleware"""
        task = Task(type="middleware_orchestration", params={"type": "security"})
        result = await agent.execute_task(task)
        
        assert result.success
        assert "security_middleware" in result.data
        assert "monitoring_middleware" in result.data
        assert "performance_middleware" in result.data

    @pytest.mark.asyncio
    async def test_enterprise_security_audit(self, agent):
        """✅ Test 18: Audit sécurité enterprise"""
        task = Task(type="enterprise_security_audit", params={"level": "comprehensive"})
        result = await agent.execute_task(task)
        
        assert result.success
        assert "security_score" in result.data
        assert "recommendations" in result.data
        assert "compliance_status" in result.data
        assert result.data["security_score"] > 0

    @pytest.mark.asyncio
    async def test_health_check_orchestration(self, agent):
        """✅ Test 19: Orchestration health checks"""
        task = Task(type="health_check_orchestration", params={"type": "comprehensive"})
        result = await agent.execute_task(task)
        
        assert result.success
        assert "endpoints" in result.data
        assert "checks" in result.data
        assert "monitoring" in result.data

    # === Tests LLM Enhancement ===

    @pytest.mark.asyncio
    async def test_llm_task_enhancement(self, agent):
        """✅ Test 20: Enhancement LLM des tâches"""
        task = Task(type="authentication_setup", params={"provider": "oauth2"})
        enhanced_task = await agent._enhance_task_with_llm(task)
        
        assert enhanced_task.type == task.type
        assert "llm_context" in enhanced_task.params
        assert "hints" in enhanced_task.params["llm_context"]
        assert len(enhanced_task.params["llm_context"]["hints"]) > 0

    @pytest.mark.asyncio
    async def test_llm_context_loading(self, agent):
        """✅ Test 21: Chargement contexte LLM"""
        assert "fastapi_patterns" in agent.llm_context
        assert "enterprise_standards" in agent.llm_context
        assert "optimization_areas" in agent.llm_context
        assert len(agent.llm_context["fastapi_patterns"]) > 0

    # === Tests Métriques et Monitoring ===

    @pytest.mark.asyncio
    async def test_metrics_update(self, agent):
        """✅ Test 22: Mise à jour métriques"""
        initial_score = agent.metrics.authentication_score
        
        task = Task(type="authentication_setup", params={})
        await agent.execute_task(task)
        
        assert agent.metrics.authentication_score > initial_score

    @pytest.mark.asyncio
    async def test_analysis_history_tracking(self, agent):
        """✅ Test 23: Suivi historique analyses"""
        initial_count = len(agent.analysis_history)
        
        task = Task(type="fastapi_patterns_analysis", params={})
        await agent.execute_task(task)
        
        assert len(agent.analysis_history) > initial_count

    @pytest.mark.asyncio
    async def test_health_check_comprehensive(self, agent):
        """✅ Test 24: Health check complet"""
        health = await agent.health_check()
        
        # Champs obligatoires
        required_fields = [
            "agent_id", "agent_name", "agent_version", "wave_version",
            "status", "features_count", "orchestration_metrics",
            "compliance_score", "nextgen_patterns", "overall_health"
        ]
        for field in required_fields:
            assert field in health, f"Champ health check manquant: {field}"
        
        # Validation valeurs
        assert health["agent_version"] == __version__
        assert health["wave_version"] == __wave_version__
        assert health["features_count"] == 5
        assert health["overall_health"] in ["EXCELLENT", "GOOD", "WARNING", "CRITICAL"]

    # === Tests Gestion Erreurs ===

    @pytest.mark.asyncio
    async def test_unsupported_task_handling(self, agent):
        """✅ Test 25: Gestion tâche non supportée"""
        task = Task(type="unsupported_task_type", params={})
        result = await agent.execute_task(task)
        
        assert not result.success
        assert "non supportée" in result.error

    @pytest.mark.asyncio
    async def test_invalid_parameters_handling(self, agent):
        """✅ Test 26: Gestion paramètres invalides"""
        task = Task(type="authentication_setup", params=None)
        result = await agent.execute_task(task)
        
        # Doit gérer gracieusement les paramètres None
        assert isinstance(result, Result)

    @pytest.mark.asyncio
    async def test_exception_handling_in_execution(self, agent):
        """✅ Test 27: Gestion exceptions exécution"""
        # Test avec paramètres causant une erreur potentielle
        task = Task(type="fastapi_patterns_analysis", params={"invalid": object()})
        result = await agent.execute_task(task)
        
        # Doit retourner un résultat même en cas d'erreur
        assert isinstance(result, Result)

    # === Tests Features Integration ===

    @pytest.mark.asyncio
    async def test_features_can_handle_dispatch(self, agent):
        """✅ Test 28: Dispatch vers features appropriées"""
        task = Task(type="authentication_setup", params={})
        
        # Au moins une feature doit pouvoir traiter cette tâche
        handling_features = [f for f in agent.features if f.can_handle(task)]
        assert len(handling_features) >= 1

    @pytest.mark.asyncio
    async def test_features_stub_mode_handling(self, agent):
        """✅ Test 29: Gestion mode stub features"""
        # Test que l'agent fonctionne même avec features en mode stub
        assert agent.features_missing is True  # En mode test, features manquantes
        
        task = Task(type="authentication_setup", params={})
        result = await agent.execute_task(task)
        
        # Doit réussir même en mode stub
        assert result.success

    # === Tests Performance ===

    @pytest.mark.asyncio
    async def test_execution_performance(self, agent):
        """✅ Test 30: Performance exécution"""
        task = Task(type="fastapi_patterns_analysis", params={})
        
        start_time = time.time()
        result = await agent.execute_task(task)
        execution_time = (time.time() - start_time) * 1000
        
        assert result.success
        assert execution_time < 1000  # Moins de 1 seconde
        assert "execution_time_ms" in result.metrics

    @pytest.mark.asyncio
    async def test_concurrent_execution(self, agent):
        """✅ Test 31: Exécution concurrente"""
        tasks = [
            Task(type="authentication_setup", params={"concurrent": i})
            for i in range(3)
        ]
        
        results = await asyncio.gather(*[
            agent.execute_task(task) for task in tasks
        ])
        
        assert len(results) == 3
        assert all(r.success for r in results)

    # === Tests Rapports et Persistence ===

    @pytest.mark.asyncio
    async def test_shutdown_reports_generation(self, agent_config, temp_workspace):
        """✅ Test 32: Génération rapports arrêt"""
        agent = create_agent_23_enterprise(**agent_config)
        await agent.startup()
        
        # Exécuter quelques tâches pour avoir des données
        task = Task(type="fastapi_patterns_analysis", params={})
        await agent.execute_task(task)
        
        await agent.shutdown()
        
        # Vérification existence rapports
        reports_dir = temp_workspace / 'reports' / 'agents'
        shutdown_reports = list(reports_dir.glob('shutdown_agent23_*.json'))
        assert len(shutdown_reports) >= 1

    @pytest.mark.asyncio
    async def test_metrics_persistence(self, agent_config, temp_workspace):
        """✅ Test 33: Persistence métriques"""
        agent = create_agent_23_enterprise(**agent_config)
        await agent.startup()
        
        # Exécuter quelques tâches
        tasks = [
            Task(type="authentication_setup", params={}),
            Task(type="fastapi_patterns_analysis", params={})
        ]
        for task in tasks:
            await agent.execute_task(task)
        
        await agent.shutdown()
        
        # Vérification sauvegarde métriques
        reports_dir = temp_workspace / 'reports' / 'agents'
        metrics_files = list(reports_dir.glob('metrics_agent23_*.json'))
        assert len(metrics_files) >= 1

    # === Tests Conformité NextGeneration ===

    def test_dataclasses_structure(self):
        """✅ Test 34: Structure dataclasses"""
        # Test FastAPIMetrics
        metrics = FastAPIMetrics()
        assert hasattr(metrics, 'authentication_score')
        assert hasattr(metrics, 'overall_orchestration_score')
        
        # Test FastAPIIssue
        issue = FastAPIIssue(
            severity="HIGH",
            category="security",
            description="Test issue",
            recommendation="Fix test"
        )
        assert issue.to_dict() is not None

    def test_version_compliance(self):
        """✅ Test 35: Conformité version"""
        agent = create_agent_23_enterprise()
        assert agent.agent_version == "5.3.0"
        assert "Wave 3" in agent.wave_version
        assert float(agent.compliance_score.rstrip('%')) >= 90.0

    @pytest.mark.asyncio
    async def test_enterprise_readiness(self, agent):
        """✅ Test 36: Préparation enterprise"""
        health = await agent.health_check()
        
        # Vérifications enterprise
        assert health["enterprise_ready"] is True
        assert health["features_count"] >= 5
        assert "orchestration_metrics" in health
        assert len(agent.get_capabilities()) >= 12

    # === Test Intégration Complète ===

    @pytest.mark.asyncio
    async def test_complete_workflow_integration(self, agent):
        """✅ Test 37: Intégration workflow complète"""
        # Séquence complète représentative
        workflow_tasks = [
            Task(type="authentication_setup", params={"provider": "oauth2"}),
            Task(type="fastapi_patterns_analysis", params={"target": "complete_api"}),
            Task(type="enterprise_security_audit", params={"level": "comprehensive"}),
            Task(type="architecture_optimization", params={"scope": "full"}),
            Task(type="health_check_orchestration", params={"type": "complete"})
        ]
        
        results = []
        for task in workflow_tasks:
            result = await agent.execute_task(task)
            results.append(result)
            assert result.success, f"Tâche {task.type} échouée: {result.error}"
        
        # Vérification santé finale
        health = await agent.health_check()
        assert health["overall_health"] in ["EXCELLENT", "GOOD"]
        
        # Vérification métriques progression
        assert agent.metrics.overall_orchestration_score > 0

    # === Test Régression Legacy ===

    @pytest.mark.asyncio
    async def test_legacy_compatibility_preservation(self, agent):
        """✅ Test 38: Préservation compatibilité legacy"""
        # Test que toutes les capacités de base de la v2.0.0 sont préservées
        legacy_capabilities = [
            "authentication_setup", "rate_limiting_config", "api_documentation",
            "monitoring_setup", "security_enhancement", "performance_optimization"
        ]
        
        current_capabilities = agent.get_capabilities()
        for legacy_cap in legacy_capabilities:
            assert legacy_cap in current_capabilities, f"Capacité legacy perdue: {legacy_cap}"
        
        # Test exécution des tâches legacy
        for cap in legacy_capabilities:
            task = Task(type=cap, params={"legacy_test": True})
            result = await agent.execute_task(task)
            assert result.success, f"Capacité legacy {cap} non fonctionnelle"


def run_validation_suite():
    """🧪 Exécution suite validation complète"""
    print("🧪 === SUITE VALIDATION AGENT FASTAPI 23 NEXTGENERATION ===")
    print(f"🎯 Version testée: {__version__}")
    print(f"🌊 Wave: {__wave_version__}")
    print(f"📊 Tests prévus: 38+ tests exhaustifs")
    print()
    
    # Exécution des tests
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-x",  # Stop au premier échec
        "--color=yes"
    ])
    
    if exit_code == 0:
        print("\n✅ === TOUS LES TESTS VALIDÉS ===")
        print("🎉 NON-RÉGRESSION ABSOLUE confirmée")
        print("🚀 Agent NextGeneration Wave 3 prêt production")
    else:
        print("\n❌ === ÉCHECS DÉTECTÉS ===")
        print("⚠️ Validation NON-RÉGRESSION échouée")
        print("🔧 Corrections requises avant déploiement")
    
    return exit_code


if __name__ == "__main__":
    exit_code = run_validation_suite()
    sys.exit(exit_code)