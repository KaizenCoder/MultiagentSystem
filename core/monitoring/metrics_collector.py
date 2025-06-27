"""
Collecteur de Métriques Avancées
NextGeneration Maintenance Team - Advanced Metrics Collection

Système de collecte de métriques en temps réel avec:
- Métriques détaillées par agent
- Détection d'anomalies automatique
- Alertes intelligentes
- Analytics de performance
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
import asyncio
from collections import deque
import psutil
import os
from functools import wraps

@dataclass
class AgentMetrics:
    """Métriques détaillées par agent"""
    agent_id: str
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    average_duration: float = 0.0
    min_duration: float = float('inf')
    max_duration: float = 0.0
    last_execution_time: float = 0.0
    peak_memory_usage: float = 0.0
    current_memory_usage: float = 0.0
    error_rate: float = 0.0
    throughput_per_minute: float = 0.0
    recent_durations: deque = field(default_factory=lambda: deque(maxlen=100))
    
    def __post_init__(self):
        """Initialisation après création"""
        if not hasattr(self, 'recent_durations') or self.recent_durations is None:
            self.recent_durations = deque(maxlen=100)

class AdvancedMetricsCollector:
    """Collecteur de métriques avec analytics en temps réel"""
    
    def __init__(self):
        self.metrics: Dict[str, AgentMetrics] = {}
        self.performance_history: List[Dict] = []
        self.alerts_config = {
            "high_error_rate": 0.15,      # 15% d'erreurs
            "slow_response": 30.0,         # 30s de réponse
            "high_memory": 500 * 1024 * 1024  # 500MB
        }
        self.active_alerts = set()
        self._start_time = time.time()
        self._running = False
    
    async def startup(self):
        """Démarrage du collecteur de métriques"""
        self._running = True
        self._start_time = time.time()
        print("🚀 AdvancedMetricsCollector démarré")
    
    async def shutdown(self):
        """Arrêt du collecteur de métriques"""
        self._running = False
        print("🛑 AdvancedMetricsCollector arrêté")
    
    def record_execution(self, agent_id: str, duration: float, 
                        success: bool, memory_usage: float = 0, 
                        task_type: str = "unknown"):
        """Enregistrement enrichi avec détection d'anomalies"""
        
        if agent_id not in self.metrics:
            self.metrics[agent_id] = AgentMetrics(agent_id=agent_id)
        
        metrics = self.metrics[agent_id]
        metrics.total_executions += 1
        
        # Mise à jour des compteurs
        if success:
            metrics.successful_executions += 1
        else:
            metrics.failed_executions += 1
        
        # Calcul des durées
        metrics.recent_durations.append(duration)
        metrics.min_duration = min(metrics.min_duration, duration)
        metrics.max_duration = max(metrics.max_duration, duration)
        
        # Moyenne mobile pondérée (plus de poids aux récentes)
        if len(metrics.recent_durations) > 1:
            recent_avg = sum(metrics.recent_durations) / len(metrics.recent_durations)
            metrics.average_duration = (metrics.average_duration * 0.7 + recent_avg * 0.3)
        else:
            metrics.average_duration = duration
        
        # Métriques mémoire
        metrics.current_memory_usage = memory_usage
        metrics.peak_memory_usage = max(metrics.peak_memory_usage, memory_usage)
        
        # Calcul du taux d'erreur
        metrics.error_rate = metrics.failed_executions / metrics.total_executions
        
        # Throughput (exécutions par minute)
        current_time = time.time()
        metrics.last_execution_time = current_time
        recent_executions = sum(1 for h in self.performance_history[-60:] 
                               if h.get("agent_id") == agent_id and 
                               current_time - h.get("timestamp", 0) <= 60)
        metrics.throughput_per_minute = recent_executions
        
        # Historique pour analytics
        self.performance_history.append({
            "agent_id": agent_id,
            "timestamp": current_time,
            "duration": duration,
            "success": success,
            "memory_usage": memory_usage,
            "task_type": task_type,
            "error_rate": metrics.error_rate,
            "throughput": metrics.throughput_per_minute
        })
        
        # Limitation de l'historique (garder 1000 dernières entrées)
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]
        
        # Détection d'alertes
        self._check_alerts(agent_id, metrics)
    
    def _check_alerts(self, agent_id: str, metrics: AgentMetrics):
        """Détection proactive d'anomalies"""
        alerts = []
        
        # Taux d'erreur élevé
        if metrics.error_rate > self.alerts_config["high_error_rate"]:
            alert_key = f"{agent_id}_high_error_rate"
            if alert_key not in self.active_alerts:
                alerts.append({
                    "type": "HIGH_ERROR_RATE",
                    "agent_id": agent_id,
                    "current_rate": f"{metrics.error_rate:.2%}",
                    "threshold": f"{self.alerts_config['high_error_rate']:.2%}",
                    "severity": "WARNING"
                })
                self.active_alerts.add(alert_key)
        
        # Réponse lente
        if metrics.average_duration > self.alerts_config["slow_response"]:
            alert_key = f"{agent_id}_slow_response"
            if alert_key not in self.active_alerts:
                alerts.append({
                    "type": "SLOW_RESPONSE",
                    "agent_id": agent_id,
                    "current_duration": f"{metrics.average_duration:.1f}s",
                    "threshold": f"{self.alerts_config['slow_response']}s",
                    "severity": "WARNING"
                })
                self.active_alerts.add(alert_key)
        
        # Usage mémoire élevé
        if metrics.current_memory_usage > self.alerts_config["high_memory"]:
            alert_key = f"{agent_id}_high_memory"
            if alert_key not in self.active_alerts:
                alerts.append({
                    "type": "HIGH_MEMORY_USAGE",
                    "agent_id": agent_id,
                    "current_memory": f"{metrics.current_memory_usage / 1024 / 1024:.1f}MB",
                    "threshold": f"{self.alerts_config['high_memory'] / 1024 / 1024:.1f}MB",
                    "severity": "CRITICAL"
                })
                self.active_alerts.add(alert_key)
        
        # Envoi des alertes
        for alert in alerts:
            self._send_alert(alert)
    
    def _send_alert(self, alert: Dict):
        """Envoi d'alerte (intégration Slack/Teams/Email)"""
        severity_emoji = {"WARNING": "⚠️", "CRITICAL": "🚨", "INFO": "ℹ️"}
        emoji = severity_emoji.get(alert["severity"], "📊")
        
        message = (f"{emoji} **ALERTE {alert['type']}**\n"
                  f"Agent: {alert['agent_id']}\n"
                  f"Valeur actuelle: {alert.get('current_rate', alert.get('current_duration', alert.get('current_memory')))}\n"
                  f"Seuil: {alert['threshold']}")
        
        # Pour l'instant, affichage console (à étendre avec Slack/Teams)
        print(f"🚨 ALERTE: {message}")
    
    def get_dashboard_data(self) -> Dict:
        """Données pour dashboard de monitoring"""
        total_executions = sum(m.total_executions for m in self.metrics.values())
        total_successes = sum(m.successful_executions for m in self.metrics.values())
        global_success_rate = (total_successes / total_executions * 100) if total_executions > 0 else 0
        
        return {
            "global_metrics": {
                "total_executions": total_executions,
                "global_success_rate": f"{global_success_rate:.1f}%",
                "active_agents": len(self.metrics),
                "active_alerts": len(self.active_alerts),
                "uptime": f"{(time.time() - self._start_time) / 3600:.1f}h"
            },
            "agent_metrics": {
                agent_id: {
                    "success_rate": f"{(m.successful_executions / m.total_executions * 100):.1f}%" if m.total_executions > 0 else "0%",
                    "avg_duration": f"{m.average_duration:.2f}s",
                    "throughput": f"{m.throughput_per_minute:.1f}/min",
                    "memory_usage": f"{m.current_memory_usage / 1024 / 1024:.1f}MB",
                    "status": "🟢" if m.error_rate < 0.05 else "🟡" if m.error_rate < 0.15 else "🔴"
                }
                for agent_id, m in self.metrics.items()
            },
            "recent_performance": self.performance_history[-20:],  # 20 dernières exécutions
            "alerts": list(self.active_alerts)
        }
    
    def get_agent_metrics(self, agent_id: str) -> Optional[AgentMetrics]:
        """Récupère les métriques d'un agent spécifique"""
        return self.metrics.get(agent_id)
    
    def reset_alerts(self, agent_id: Optional[str] = None):
        """Reset des alertes pour un agent ou tous"""
        if agent_id:
            alerts_to_remove = [alert for alert in self.active_alerts if alert.startswith(agent_id)]
            for alert in alerts_to_remove:
                self.active_alerts.discard(alert)
        else:
            self.active_alerts.clear()
    
    def export_metrics(self) -> Dict:
        """Export complet des métriques pour sauvegarde/analyse"""
        return {
            "timestamp": time.time(),
            "metrics": {
                agent_id: {
                    "agent_id": m.agent_id,
                    "total_executions": m.total_executions,
                    "successful_executions": m.successful_executions,
                    "failed_executions": m.failed_executions,
                    "average_duration": m.average_duration,
                    "min_duration": m.min_duration,
                    "max_duration": m.max_duration,
                    "error_rate": m.error_rate,
                    "throughput_per_minute": m.throughput_per_minute,
                    "recent_durations": list(m.recent_durations)
                }
                for agent_id, m in self.metrics.items()
            },
            "performance_history": self.performance_history,
            "active_alerts": list(self.active_alerts)
        }

# Décorateur pour instrumentation automatique
def monitor_performance(metrics_collector: Optional[AdvancedMetricsCollector] = None):
    """Décorateur pour monitoring automatique des performances"""
    
    # Collecteur global par défaut
    if metrics_collector is None:
        if not hasattr(monitor_performance, '_default_collector'):
            monitor_performance._default_collector = AdvancedMetricsCollector()
        metrics_collector = monitor_performance._default_collector
    
    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(self, *args, **kwargs):
                # Métriques de début
                start_time = time.time()
                process = psutil.Process(os.getpid())
                start_memory = process.memory_info().rss
                
                success = False
                task_type = "unknown"
                
                # Extraction du type de tâche si disponible
                if args and hasattr(args[0], 'type'):
                    task_type = args[0].type
                elif kwargs.get('task') and hasattr(kwargs['task'], 'type'):
                    task_type = kwargs['task'].type
                
                try:
                    result = await func(self, *args, **kwargs)
                    success = result.success if hasattr(result, 'success') else True
                    return result
                except Exception as e:
                    success = False
                    raise
                finally:
                    # Calcul des métriques finales
                    duration = time.time() - start_time
                    end_memory = process.memory_info().rss
                    memory_used = end_memory - start_memory
                    
                    # Enregistrement
                    agent_id = getattr(self, 'agent_id', self.__class__.__name__)
                    metrics_collector.record_execution(
                        agent_id=agent_id,
                        duration=duration,
                        success=success,
                        memory_usage=memory_used,
                        task_type=task_type
                    )
            
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(self, *args, **kwargs):
                # Métriques de début
                start_time = time.time()
                process = psutil.Process(os.getpid())
                start_memory = process.memory_info().rss
                
                success = False
                task_type = "unknown"
                
                # Extraction du type de tâche si disponible
                if args and hasattr(args[0], 'type'):
                    task_type = args[0].type
                
                try:
                    result = func(self, *args, **kwargs)
                    success = result.success if hasattr(result, 'success') else True
                    return result
                except Exception as e:
                    success = False
                    raise
                finally:
                    # Calcul des métriques finales
                    duration = time.time() - start_time
                    end_memory = process.memory_info().rss
                    memory_used = end_memory - start_memory
                    
                    # Enregistrement
                    agent_id = getattr(self, 'agent_id', self.__class__.__name__)
                    metrics_collector.record_execution(
                        agent_id=agent_id,
                        duration=duration,
                        success=success,
                        memory_usage=memory_used,
                        task_type=task_type
                    )
            
            return sync_wrapper
    
    return decorator

# Instance globale pour usage simple
global_metrics_collector = AdvancedMetricsCollector()

def get_global_metrics() -> AdvancedMetricsCollector:
    """Récupère l'instance globale du collecteur de métriques"""
    return global_metrics_collector

# Exemple d'usage
if __name__ == "__main__":
    # Test du collecteur
    collector = AdvancedMetricsCollector()
    
    # Simulation de quelques exécutions
    import random
    
    for i in range(10):
        agent_id = f"agent_{random.randint(1, 3)}"
        duration = random.uniform(1, 5)
        success = random.choice([True, True, True, False])  # 75% succès
        memory = random.randint(100, 200) * 1024 * 1024  # 100-200MB
        
        collector.record_execution(agent_id, duration, success, memory)
    
    # Affichage du dashboard
    dashboard = collector.get_dashboard_data()
    print("📊 Dashboard Métriques:")
    print(f"Total exécutions: {dashboard['global_metrics']['total_executions']}")
    print(f"Taux de succès global: {dashboard['global_metrics']['global_success_rate']}")
    print(f"Agents actifs: {dashboard['global_metrics']['active_agents']}")
    
    print("\n🔍 Métriques par agent:")
    for agent_id, metrics in dashboard['agent_metrics'].items():
        print(f"  {agent_id}: {metrics['status']} {metrics['success_rate']} - {metrics['avg_duration']}") 