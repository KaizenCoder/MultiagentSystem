"""
Moniteur de Régression pour Migration NextGeneration
Assure la détection précoce des régressions pendant la migration des agents.
"""
from typing import Dict, List, Optional, Tuple
import asyncio
import logging
from datetime import datetime, timedelta
import json

from .shadow_mode_validator import ShadowModeValidator, ValidationResult, ActivationDecision
from .context_store import ContextStore, create_agent_context
from .message_bus_a2a import MessageBusA2A, Envelope

logger = logging.getLogger(__name__)

class RegressionMonitor:
    """Moniteur de régression pour la migration des agents."""
    
    def __init__(
        self,
        shadow_validator: ShadowModeValidator,
        context_store: ContextStore,
        message_bus: MessageBusA2A,
        config: Dict
    ):
        self.shadow_validator = shadow_validator
        self.context_store = context_store
        self.message_bus = message_bus
        self.config = config
        
        # Métriques de performance par agent
        self.agent_metrics: Dict[str, Dict] = {}
        
        # Seuils d'alerte configurables
        self.alert_thresholds = {
            "similarity_threshold": 0.999,  # 99.9% similarité minimum
            "performance_degradation": 0.15,  # Max 15% dégradation
            "error_rate_increase": 0.05,    # Max 5% augmentation erreurs
            "latency_increase": 0.20,       # Max 20% augmentation latence
        }
        
        # État de santé des agents
        self.agent_health: Dict[str, str] = {}
        
    async def start_monitoring(self, agent_ids: List[str]):
        """Démarre le monitoring des agents spécifiés."""
        logger.info(f"🔍 Démarrage monitoring pour {len(agent_ids)} agents")
        
        # Initialisation des métriques baseline
        await self._initialize_baseline_metrics(agent_ids)
        
        # Démarrage des tâches de monitoring
        monitoring_tasks = [
            self._monitor_agent(agent_id) for agent_id in agent_ids
        ]
        
        await asyncio.gather(*monitoring_tasks)
        
    async def _initialize_baseline_metrics(self, agent_ids: List[str]):
        """Initialise les métriques de référence pour chaque agent."""
        for agent_id in agent_ids:
            baseline = await self._collect_agent_baseline(agent_id)
            self.agent_metrics[agent_id] = {
                "baseline": baseline,
                "current": baseline.copy(),
                "history": []
            }
            logger.info(f"📊 Baseline établie pour {agent_id}")
            
    async def _collect_agent_baseline(self, agent_id: str) -> Dict:
        """Collecte les métriques de référence pour un agent."""
        # Exécution de tests standard pour établir baseline
        test_results = await self._run_standard_tests(agent_id)
        
        return {
            "success_rate": test_results["success_rate"],
            "avg_latency": test_results["avg_latency"],
            "error_rate": test_results["error_rate"],
            "throughput": test_results["throughput"],
            "memory_usage": test_results["memory_usage"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    async def _monitor_agent(self, agent_id: str):
        """Monitore un agent spécifique en continu."""
        while True:
            try:
                # Collecte des métriques actuelles
                current_metrics = await self._collect_current_metrics(agent_id)
                
                # Analyse des régressions
                regressions = self._analyze_regressions(
                    agent_id, 
                    self.agent_metrics[agent_id]["baseline"],
                    current_metrics
                )
                
                # Mise à jour des métriques
                self.agent_metrics[agent_id]["current"] = current_metrics
                self.agent_metrics[agent_id]["history"].append(current_metrics)
                
                # Gestion des régressions détectées
                if regressions:
                    await self._handle_regressions(agent_id, regressions)
                    
                # Mise à jour état de santé
                self._update_agent_health(agent_id, regressions)
                
                # Sauvegarde des métriques dans ContextStore
                await self._save_metrics_to_context(agent_id)
                
            except Exception as e:
                logger.error(f"❌ Erreur monitoring {agent_id}: {str(e)}")
                
            # Attente avant prochain cycle
            await asyncio.sleep(60)  # Monitoring toutes les minutes
            
    async def _collect_current_metrics(self, agent_id: str) -> Dict:
        """Collecte les métriques actuelles d'un agent."""
        # Exécution shadow pour collecter métriques
        validation_result = await self.shadow_validator.dual_execution(
            agent_id,
            Envelope(
                type="HEALTH_CHECK",
                payload={"timestamp": datetime.utcnow().isoformat()}
            )
        )
        
        return {
            "success_rate": validation_result.success_rate,
            "avg_latency": validation_result.latency,
            "error_rate": validation_result.error_rate,
            "throughput": validation_result.throughput,
            "memory_usage": validation_result.memory_usage,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    def _analyze_regressions(
        self, 
        agent_id: str,
        baseline: Dict,
        current: Dict
    ) -> List[Dict]:
        """Analyse les régressions potentielles."""
        regressions = []
        
        # Vérification des métriques clés
        if current["success_rate"] < baseline["success_rate"] * (1 - self.alert_thresholds["performance_degradation"]):
            regressions.append({
                "type": "SUCCESS_RATE_DEGRADATION",
                "severity": "HIGH",
                "details": {
                    "baseline": baseline["success_rate"],
                    "current": current["success_rate"]
                }
            })
            
        if current["error_rate"] > baseline["error_rate"] * (1 + self.alert_thresholds["error_rate_increase"]):
            regressions.append({
                "type": "ERROR_RATE_INCREASE",
                "severity": "HIGH",
                "details": {
                    "baseline": baseline["error_rate"],
                    "current": current["error_rate"]
                }
            })
            
        if current["avg_latency"] > baseline["avg_latency"] * (1 + self.alert_thresholds["latency_increase"]):
            regressions.append({
                "type": "LATENCY_DEGRADATION",
                "severity": "MEDIUM",
                "details": {
                    "baseline": baseline["avg_latency"],
                    "current": current["avg_latency"]
                }
            })
            
        return regressions
        
    async def _handle_regressions(self, agent_id: str, regressions: List[Dict]):
        """Gère les régressions détectées."""
        logger.warning(f"⚠️ Régressions détectées pour {agent_id}")
        
        # Création contexte de régression
        regression_context = create_agent_context(
            agent_id=agent_id,
            context_type="REGRESSION_ALERT",
            data={
                "regressions": regressions,
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": self.agent_metrics[agent_id]["current"]
            }
        )
        
        # Sauvegarde dans ContextStore
        await self.context_store.save_agent_context(regression_context)
        
        # Notification via MessageBus
        await self.message_bus.publish(
            Envelope(
                type="REGRESSION_ALERT",
                payload={
                    "agent_id": agent_id,
                    "regressions": regressions,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        )
        
        # Rollback automatique si régression critique
        if any(r["severity"] == "HIGH" for r in regressions):
            logger.error(f"🔴 Régression critique détectée pour {agent_id}")
            await self._trigger_rollback(agent_id)
            
    async def _trigger_rollback(self, agent_id: str):
        """Déclenche le rollback d'un agent."""
        logger.warning(f"⚠️ Déclenchement rollback pour {agent_id}")
        
        try:
            # Désactivation agent moderne
            await self.shadow_validator.rollback_agent(agent_id)
            
            # Notification rollback
            await self.message_bus.publish(
                Envelope(
                    type="AGENT_ROLLBACK",
                    payload={
                        "agent_id": agent_id,
                        "timestamp": datetime.utcnow().isoformat(),
                        "reason": "CRITICAL_REGRESSION"
                    }
                )
            )
            
            # Mise à jour état
            self.agent_health[agent_id] = "ROLLED_BACK"
            
        except Exception as e:
            logger.error(f"❌ Erreur rollback {agent_id}: {str(e)}")
            
    def _update_agent_health(self, agent_id: str, regressions: List[Dict]):
        """Met à jour l'état de santé d'un agent."""
        if not regressions:
            self.agent_health[agent_id] = "HEALTHY"
        elif any(r["severity"] == "HIGH" for r in regressions):
            self.agent_health[agent_id] = "CRITICAL"
        else:
            self.agent_health[agent_id] = "WARNING"
            
    async def _save_metrics_to_context(self, agent_id: str):
        """Sauvegarde les métriques dans ContextStore."""
        metrics_context = create_agent_context(
            agent_id=agent_id,
            context_type="MONITORING_METRICS",
            data={
                "metrics": self.agent_metrics[agent_id],
                "health": self.agent_health[agent_id],
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        await self.context_store.save_agent_context(metrics_context)
        
    async def get_agent_health_report(self, agent_id: str) -> Dict:
        """Génère un rapport de santé pour un agent."""
        metrics = self.agent_metrics.get(agent_id, {})
        health = self.agent_health.get(agent_id, "UNKNOWN")
        
        return {
            "agent_id": agent_id,
            "health_status": health,
            "current_metrics": metrics.get("current", {}),
            "baseline_metrics": metrics.get("baseline", {}),
            "regression_count": len([h for h in metrics.get("history", []) if h.get("regressions")]),
            "last_updated": datetime.utcnow().isoformat()
        }
        
    async def get_global_health_report(self) -> Dict:
        """Génère un rapport de santé global."""
        return {
            "total_agents": len(self.agent_metrics),
            "health_summary": {
                "HEALTHY": len([h for h in self.agent_health.values() if h == "HEALTHY"]),
                "WARNING": len([h for h in self.agent_health.values() if h == "WARNING"]),
                "CRITICAL": len([h for h in self.agent_health.values() if h == "CRITICAL"]),
                "ROLLED_BACK": len([h for h in self.agent_health.values() if h == "ROLLED_BACK"])
            },
            "timestamp": datetime.utcnow().isoformat()
        } 