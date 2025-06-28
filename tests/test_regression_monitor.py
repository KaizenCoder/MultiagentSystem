"""
Tests pour le Moniteur de Régression
Valide la détection et gestion des régressions pendant la migration.
"""
import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, AsyncMock

from core.services.regression_monitor import RegressionMonitor
from core.services.shadow_mode_validator import ShadowModeValidator, ValidationResult
from core.services.context_store import ContextStore
from core.services.message_bus_a2a import MessageBusA2A, Envelope

@pytest.fixture
async def regression_monitor():
    """Fixture pour le moniteur de régression."""
    # Mocks des dépendances
    shadow_validator = AsyncMock(spec=ShadowModeValidator)
    context_store = AsyncMock(spec=ContextStore)
    message_bus = AsyncMock(spec=MessageBusA2A)
    
    config = {
        "monitoring": {
            "interval_seconds": 60,
            "thresholds": {
                "similarity": 0.999,
                "performance_degradation": 0.15,
                "error_rate_increase": 0.05,
                "latency_increase": 0.20
            }
        }
    }
    
    monitor = RegressionMonitor(
        shadow_validator=shadow_validator,
        context_store=context_store,
        message_bus=message_bus,
        config=config
    )
    
    return monitor

@pytest.mark.asyncio
async def test_baseline_metrics_collection(regression_monitor):
    """Test la collecte des métriques baseline."""
    # Configuration du mock
    test_agent_id = "agent_111_auditeur_qualite"
    baseline_metrics = {
        "success_rate": 0.95,
        "avg_latency": 150,
        "error_rate": 0.02,
        "throughput": 100,
        "memory_usage": 256
    }
    
    regression_monitor._run_standard_tests = AsyncMock(
        return_value=baseline_metrics
    )
    
    # Test initialisation baseline
    await regression_monitor._initialize_baseline_metrics([test_agent_id])
    
    # Vérifications
    assert test_agent_id in regression_monitor.agent_metrics
    assert regression_monitor.agent_metrics[test_agent_id]["baseline"]["success_rate"] == 0.95
    assert regression_monitor.agent_metrics[test_agent_id]["baseline"]["avg_latency"] == 150

@pytest.mark.asyncio
async def test_regression_detection(regression_monitor):
    """Test la détection des régressions."""
    test_agent_id = "agent_111_auditeur_qualite"
    
    # Configuration baseline
    baseline = {
        "success_rate": 0.95,
        "avg_latency": 150,
        "error_rate": 0.02,
        "throughput": 100,
        "memory_usage": 256
    }
    
    # Métriques dégradées
    current = {
        "success_rate": 0.75,  # Dégradation significative
        "avg_latency": 200,    # Augmentation latence
        "error_rate": 0.08,    # Augmentation erreurs
        "throughput": 80,
        "memory_usage": 300
    }
    
    # Test analyse régressions
    regressions = regression_monitor._analyze_regressions(
        test_agent_id,
        baseline,
        current
    )
    
    # Vérifications
    assert len(regressions) == 3  # Doit détecter 3 régressions
    assert any(r["type"] == "SUCCESS_RATE_DEGRADATION" for r in regressions)
    assert any(r["type"] == "ERROR_RATE_INCREASE" for r in regressions)
    assert any(r["type"] == "LATENCY_DEGRADATION" for r in regressions)

@pytest.mark.asyncio
async def test_automatic_rollback(regression_monitor):
    """Test le rollback automatique sur régression critique."""
    test_agent_id = "agent_111_auditeur_qualite"
    
    # Simulation régression critique
    critical_regression = [{
        "type": "SUCCESS_RATE_DEGRADATION",
        "severity": "HIGH",
        "details": {
            "baseline": 0.95,
            "current": 0.70
        }
    }]
    
    # Test gestion régression
    await regression_monitor._handle_regressions(test_agent_id, critical_regression)
    
    # Vérifications
    regression_monitor.shadow_validator.rollback_agent.assert_called_once_with(test_agent_id)
    assert regression_monitor.agent_health[test_agent_id] == "ROLLED_BACK"
    
    # Vérification notification
    regression_monitor.message_bus.publish.assert_called_with(
        pytest.approx({
            "type": "AGENT_ROLLBACK",
            "payload": {
                "agent_id": test_agent_id,
                "reason": "CRITICAL_REGRESSION"
            }
        }, rel=1e-9)
    )

@pytest.mark.asyncio
async def test_health_reporting(regression_monitor):
    """Test la génération des rapports de santé."""
    test_agent_id = "agent_111_auditeur_qualite"
    
    # Configuration état test
    regression_monitor.agent_metrics[test_agent_id] = {
        "baseline": {
            "success_rate": 0.95,
            "avg_latency": 150
        },
        "current": {
            "success_rate": 0.90,
            "avg_latency": 160
        },
        "history": []
    }
    regression_monitor.agent_health[test_agent_id] = "HEALTHY"
    
    # Test rapport individuel
    report = await regression_monitor.get_agent_health_report(test_agent_id)
    assert report["agent_id"] == test_agent_id
    assert report["health_status"] == "HEALTHY"
    assert "current_metrics" in report
    assert "baseline_metrics" in report
    
    # Test rapport global
    global_report = await regression_monitor.get_global_health_report()
    assert global_report["total_agents"] == 1
    assert global_report["health_summary"]["HEALTHY"] == 1

@pytest.mark.asyncio
async def test_metrics_persistence(regression_monitor):
    """Test la persistance des métriques dans ContextStore."""
    test_agent_id = "agent_111_auditeur_qualite"
    
    # Configuration métriques test
    regression_monitor.agent_metrics[test_agent_id] = {
        "baseline": {
            "success_rate": 0.95,
            "avg_latency": 150
        },
        "current": {
            "success_rate": 0.90,
            "avg_latency": 160
        },
        "history": []
    }
    regression_monitor.agent_health[test_agent_id] = "HEALTHY"
    
    # Test sauvegarde métriques
    await regression_monitor._save_metrics_to_context(test_agent_id)
    
    # Vérification appel ContextStore
    regression_monitor.context_store.save_agent_context.assert_called_once()
    saved_context = regression_monitor.context_store.save_agent_context.call_args[0][0]
    assert saved_context.agent_id == test_agent_id
    assert saved_context.context_type == "MONITORING_METRICS"
    assert "metrics" in saved_context.data
    assert "health" in saved_context.data 