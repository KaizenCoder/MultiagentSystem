#!/usr/bin/env python3
"""
📊 Agent Monitoring Ops - NextGeneration v5.3.0
Version enterprise Wave 4 avec observabilité opérationnelle intelligente

Migration Pattern: OBSERVABILITY + ALERTING + LLM_ENHANCED
Author: Claude Sonnet 4
Date: 30 Juin 2025
"""

import asyncio
import json
import time
import hashlib
import psutil
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import threading
import queue
import uuid
import sqlite3

# Imports NextGeneration Architecture
try:
    from core.services import (
        LLMGatewayHybrid, create_llm_gateway,
        MessageBusA2A, create_envelope, MessageType, Priority,
        OptimizedContextStore, create_agent_context, ContextType
    )
    from core.agent_factory_architecture import Task, Result
except ImportError:
    # Fallback pour développement isolé
    print("⚠️ NextGeneration services not available - running in development mode")
    class Task:
        def __init__(self, task_type, params=None):
            self.type = task_type
            self.params = params or {}
    
    class Result:
        def __init__(self, success, data=None, error=None, metrics=None):
            self.success = success
            self.data = data
            self.error = error
            self.metrics = metrics or {}

class MetricType(str, Enum):
    """Types de métriques monitoring"""
    SYSTEM = "SYSTEM"
    APPLICATION = "APPLICATION"
    BUSINESS = "BUSINESS"
    PERFORMANCE = "PERFORMANCE"
    SECURITY = "SECURITY"
    CUSTOM = "CUSTOM"

class AlertSeverity(str, Enum):
    """Niveaux de sévérité alertes"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class MonitoringStatus(str, Enum):
    """Statuts monitoring"""
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"
    MAINTENANCE = "MAINTENANCE"

@dataclass
class MetricDefinition:
    """Définition métrique monitoring"""
    metric_id: str
    name: str
    description: str
    metric_type: MetricType
    unit: str
    collection_interval_seconds: int
    retention_days: int
    thresholds: Dict[str, float]
    tags: Dict[str, str] = None
    aggregation_functions: List[str] = None

@dataclass
class MetricValue:
    """Valeur métrique collectée"""
    metric_id: str
    timestamp: datetime
    value: float
    tags: Dict[str, str] = None
    metadata: Dict[str, Any] = None

@dataclass
class Alert:
    """Alerte monitoring"""
    alert_id: str
    metric_id: str
    severity: AlertSeverity
    title: str
    description: str
    value: float
    threshold: float
    condition: str
    triggered_at: datetime
    resolved_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    tags: Dict[str, str] = None

@dataclass
class ServiceHealth:
    """Santé service"""
    service_name: str
    status: MonitoringStatus
    last_check: datetime
    response_time_ms: float
    error_rate: float
    availability_percentage: float
    dependencies: List[str] = None
    metadata: Dict[str, Any] = None

class IntelligentAnomalyDetector:
    """Détecteur d'anomalies intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.baseline_models = {}
        self.anomaly_patterns = {}
        self.learning_window = 1440  # 24h en minutes
    
    async def detect_anomalies(self, metric_id: str, 
                             recent_values: List[MetricValue]) -> List[Dict[str, Any]]:
        """Détection d'anomalies avec IA"""
        anomalies = []
        
        if len(recent_values) < 10:
            return anomalies
        
        # Détection statistique de base
        values = [v.value for v in recent_values]
        mean = statistics.mean(values)
        std_dev = statistics.stdev(values) if len(values) > 1 else 0
        
        # Détection outliers statistiques
        for i, metric_value in enumerate(recent_values[-5:]):  # 5 dernières valeurs
            z_score = abs(metric_value.value - mean) / max(std_dev, 0.1)
            
            if z_score > 3:  # Seuil 3 sigma
                anomalies.append({
                    "type": "statistical_outlier",
                    "metric_id": metric_id,
                    "timestamp": metric_value.timestamp,
                    "value": metric_value.value,
                    "expected_range": [mean - 2*std_dev, mean + 2*std_dev],
                    "z_score": z_score,
                    "severity": "HIGH" if z_score > 4 else "MEDIUM"
                })
        
        # Enhancement IA si disponible
        if self.llm_gateway and len(recent_values) >= 20:
            try:
                ai_anomalies = await self.llm_gateway.process_request(
                    "Detect anomalies in monitoring data using intelligent analysis",
                    context={
                        "role": "monitoring_anomaly_expert",
                        "metric_id": metric_id,
                        "recent_values": [asdict(v) for v in recent_values[-20:]],
                        "statistical_anomalies": anomalies,
                        "baseline_stats": {"mean": mean, "std_dev": std_dev},
                        "task": "anomaly_detection_analysis"
                    }
                )
                
                if ai_anomalies.get("success"):
                    ai_detected = ai_anomalies.get("anomalies", [])
                    anomalies.extend(ai_detected)
                    
            except Exception as e:
                self.logger = logging.getLogger(f"AnomalyDetector_{id(self)}")
                self.logger.warning(f"⚠️ Erreur détection IA: {e}")
        
        return anomalies
    
    async def predict_metric_trends(self, metric_id: str, 
                                  historical_data: List[MetricValue]) -> Dict[str, Any]:
        """Prédiction tendances métriques"""
        if len(historical_data) < 50:
            return {"prediction_available": False}
        
        # Analyse tendance basique
        values = [v.value for v in historical_data[-50:]]
        timestamps = [v.timestamp for v in historical_data[-50:]]
        
        # Calcul tendance simple
        x = list(range(len(values)))
        y = values
        
        # Corrélation pour tendance
        correlation = 0
        if len(x) > 1:
            mean_x = sum(x) / len(x)
            mean_y = sum(y) / len(y)
            
            numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
            denominator_x = sum((x[i] - mean_x) ** 2 for i in range(len(x)))
            denominator_y = sum((y[i] - mean_y) ** 2 for i in range(len(y)))
            
            if denominator_x > 0 and denominator_y > 0:
                correlation = numerator / (denominator_x * denominator_y) ** 0.5
        
        trend_direction = "increasing" if correlation > 0.1 else "decreasing" if correlation < -0.1 else "stable"
        
        prediction = {
            "prediction_available": True,
            "trend_direction": trend_direction,
            "trend_strength": abs(correlation),
            "current_value": values[-1],
            "predicted_value_1h": values[-1] * (1 + correlation * 0.1),
            "confidence": min(abs(correlation), 0.9)
        }
        
        # Enhancement IA pour prédictions avancées
        if self.llm_gateway:
            try:
                ai_prediction = await self.llm_gateway.process_request(
                    "Predict metric trends using advanced analysis",
                    context={
                        "role": "monitoring_prediction_expert",
                        "metric_id": metric_id,
                        "historical_data": [asdict(v) for v in historical_data[-30:]],
                        "basic_prediction": prediction,
                        "task": "metric_trend_prediction"
                    }
                )
                
                if ai_prediction.get("success"):
                    ai_pred = ai_prediction.get("prediction", {})
                    prediction.update(ai_pred)
                    
            except Exception:
                pass
        
        return prediction

class AlertManager:
    """Gestionnaire d'alertes intelligent"""
    
    def __init__(self, monitoring_agent):
        self.agent = monitoring_agent
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_rules: Dict[str, Dict] = {}
        self.notification_channels = []
        self.alert_cooldown = 300  # 5 minutes
    
    async def evaluate_alerts(self, metric_value: MetricValue, 
                            metric_def: MetricDefinition):
        """Évaluation alertes pour métrique"""
        if not metric_def.thresholds:
            return
        
        alerts_triggered = []
        
        # Évaluation seuils
        for threshold_name, threshold_value in metric_def.thresholds.items():
            condition_met = False
            severity = AlertSeverity.MEDIUM
            
            if threshold_name == "critical_max" and metric_value.value > threshold_value:
                condition_met = True
                severity = AlertSeverity.CRITICAL
            elif threshold_name == "warning_max" and metric_value.value > threshold_value:
                condition_met = True
                severity = AlertSeverity.HIGH
            elif threshold_name == "critical_min" and metric_value.value < threshold_value:
                condition_met = True
                severity = AlertSeverity.CRITICAL
            elif threshold_name == "warning_min" and metric_value.value < threshold_value:
                condition_met = True
                severity = AlertSeverity.HIGH
            
            if condition_met:
                alert_id = f"{metric_value.metric_id}_{threshold_name}"
                
                # Vérification cooldown
                if not self._is_alert_in_cooldown(alert_id):
                    alert = Alert(
                        alert_id=alert_id,
                        metric_id=metric_value.metric_id,
                        severity=severity,
                        title=f"{metric_def.name} {threshold_name} exceeded",
                        description=f"Metric {metric_def.name} value {metric_value.value} exceeds threshold {threshold_value}",
                        value=metric_value.value,
                        threshold=threshold_value,
                        condition=threshold_name,
                        triggered_at=datetime.now(),
                        tags=metric_value.tags
                    )
                    
                    alerts_triggered.append(alert)
                    self.active_alerts[alert_id] = alert
        
        # Envoi notifications
        for alert in alerts_triggered:
            await self._send_alert_notifications(alert)
    
    def _is_alert_in_cooldown(self, alert_id: str) -> bool:
        """Vérification cooldown alerte"""
        if alert_id in self.active_alerts:
            last_alert = self.active_alerts[alert_id]
            time_since = (datetime.now() - last_alert.triggered_at).total_seconds()
            return time_since < self.alert_cooldown
        return False
    
    async def _send_alert_notifications(self, alert: Alert):
        """Envoi notifications alerte"""
        self.agent.logger.warning(f"🚨 Alert: {alert.title}")
        
        # Notification via MessageBus
        if self.agent.message_bus:
            priority = Priority.CRITICAL if alert.severity == AlertSeverity.CRITICAL else Priority.HIGH
            
            await self.agent.message_bus.publish(
                create_envelope(
                    message_type=MessageType.ALERT,
                    payload={
                        "type": "monitoring_alert",
                        "alert": asdict(alert),
                        "timestamp": datetime.now().isoformat()
                    },
                    priority=priority
                )
            )
    
    async def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acquittement alerte"""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].acknowledged_at = datetime.now()
            self.agent.logger.info(f"✅ Alert acknowledged: {alert_id} by {acknowledged_by}")
            return True
        return False
    
    async def resolve_alert(self, alert_id: str) -> bool:
        """Résolution alerte"""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].resolved_at = datetime.now()
            self.agent.logger.info(f"✅ Alert resolved: {alert_id}")
            return True
        return False

class SystemMetricsCollector:
    """Collecteur métriques système"""
    
    def __init__(self):
        self.collection_interval = 60  # secondes
        self.last_collection = {}
    
    async def collect_system_metrics(self) -> List[MetricValue]:
        """Collection métriques système"""
        now = datetime.now()
        metrics = []
        
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics.append(MetricValue(
                metric_id="system.cpu.usage_percent",
                timestamp=now,
                value=cpu_percent,
                tags={"host": "localhost"}
            ))
            
            # Mémoire
            memory = psutil.virtual_memory()
            metrics.append(MetricValue(
                metric_id="system.memory.usage_percent",
                timestamp=now,
                value=memory.percent,
                tags={"host": "localhost"}
            ))
            
            metrics.append(MetricValue(
                metric_id="system.memory.available_gb",
                timestamp=now,
                value=memory.available / (1024**3),
                tags={"host": "localhost"}
            ))
            
            # Disque
            disk = psutil.disk_usage('/')
            metrics.append(MetricValue(
                metric_id="system.disk.usage_percent",
                timestamp=now,
                value=disk.percent,
                tags={"host": "localhost", "mount": "/"}
            ))
            
            # Réseau
            network = psutil.net_io_counters()
            if "network.bytes_sent" in self.last_collection:
                time_diff = (now - self.last_collection["network.bytes_sent"]["time"]).total_seconds()
                bytes_sent_rate = (network.bytes_sent - self.last_collection["network.bytes_sent"]["value"]) / time_diff
                
                metrics.append(MetricValue(
                    metric_id="system.network.bytes_sent_per_sec",
                    timestamp=now,
                    value=bytes_sent_rate,
                    tags={"host": "localhost"}
                ))
            
            self.last_collection["network.bytes_sent"] = {"value": network.bytes_sent, "time": now}
            
        except Exception as e:
            logging.getLogger("SystemMetricsCollector").error(f"❌ Erreur collection métriques: {e}")
        
        return metrics
    
    async def collect_application_metrics(self, application: str) -> List[MetricValue]:
        """Collection métriques application"""
        # Simulation métriques application
        now = datetime.now()
        
        metrics = [
            MetricValue(
                metric_id=f"app.{application}.response_time_ms",
                timestamp=now,
                value=150 + (hash(str(now)) % 100),  # Simulation
                tags={"app": application}
            ),
            MetricValue(
                metric_id=f"app.{application}.error_rate_percent",
                timestamp=now,
                value=max(0, 2 + (hash(str(now)) % 5) - 3),  # Simulation 0-4%
                tags={"app": application}
            )
        ]
        
        return metrics

class AgentMonitoringOps_Enterprise:
    """
    📊 Agent Monitoring Ops - Enterprise NextGeneration v5.3.0
    
    Monitoring opérationnel intelligent avec observabilité avancée et détection anomalies IA.
    
    Patterns NextGeneration v5.3.0:
    - OBSERVABILITY: Monitoring complet système et applications
    - ALERTING: Alertes intelligentes avec IA
    - LLM_ENHANCED: Détection anomalies et prédictions IA
    - PATTERN_FACTORY: Architecture modulaire éprouvée
    """
    
    def __init__(self, agent_id: str = "monitoring_ops", 
                 data_dir: Path = None):
        # Métadonnées NextGeneration v5.3.0
        self.agent_id = agent_id
        self.version = "5.3.0"
        self.wave_version = "Wave 4 - Extensions Core"
        self.migration_status = "modern_active"
        self.compatibility_mode = True
        
        # Patterns NextGeneration appliqués
        self.__version__ = "5.3.0"
        self.__wave_version__ = "Wave 4 - Extensions Core"
        self.__nextgen_patterns__ = [
            "OBSERVABILITY",
            "ALERTING",
            "LLM_ENHANCED",
            "PATTERN_FACTORY"
        ]
        
        # Configuration agent
        self.name = "Monitoring Ops Enterprise"
        self.mission = "Observabilité opérationnelle intelligente avec détection anomalies IA"
        self.agent_type = "monitoring_enterprise"
        
        # Configuration monitoring
        self.data_dir = data_dir or Path("/var/lib/nextgeneration/monitoring")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Services NextGeneration (injectés à l'initialisation)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Composants monitoring intelligents
        self.anomaly_detector = IntelligentAnomalyDetector()
        self.alert_manager = AlertManager(self)
        self.metrics_collector = SystemMetricsCollector()
        
        # Configuration monitoring
        self.monitoring_config = {
            "collection_interval_seconds": 60,
            "anomaly_detection_enabled": True,
            "ai_predictions_enabled": True,
            "alert_cooldown_seconds": 300,
            "retention_days": 30,
            "auto_resolution_enabled": True
        }
        
        # État monitoring
        self.metric_definitions: Dict[str, MetricDefinition] = {}
        self.metric_values: Dict[str, List[MetricValue]] = {}
        self.service_health: Dict[str, ServiceHealth] = {}
        
        # Base de données métriques
        self.db_path = self.data_dir / "monitoring.db"
        self._init_database()
        
        # Métriques monitoring
        self.monitoring_metrics = {
            "metrics_collected": 0,
            "alerts_triggered": 0,
            "anomalies_detected": 0,
            "predictions_generated": 0,
            "system_health_score": 100.0,
            "alert_response_time_avg_seconds": 0.0
        }
        
        # Background tasks
        self._collection_task = None
        self._analysis_task = None
        self._health_check_task = None
        
        # Setup logging
        self._setup_logging()
        
        # Définition métriques par défaut
        self._setup_default_metrics()
        
        # Démarrage background tasks
        asyncio.create_task(self._start_background_tasks())
    
    def _init_database(self):
        """Initialisation base de données monitoring"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS metric_values (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    value REAL NOT NULL,
                    tags TEXT,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id TEXT UNIQUE NOT NULL,
                    metric_id TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    title TEXT NOT NULL,
                    triggered_at TEXT NOT NULL,
                    resolved_at TEXT,
                    acknowledged_at TEXT
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_metric_timestamp 
                ON metric_values(metric_id, timestamp)
            """)
    
    def _setup_logging(self):
        """Configuration logging NextGeneration"""
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="monitoring",
                custom_config={
                    "logger_name": f"nextgen.monitoring.ops.{self.agent_id}",
                    "log_dir": "logs/monitoring",
                    "metadata": {
                        "agent_type": "monitoring_ops",
                        "agent_role": "observability",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(f"MonitoringOps_{self.agent_id}")
    
    def _setup_default_metrics(self):
        """Configuration métriques par défaut"""
        default_metrics = [
            MetricDefinition(
                metric_id="system.cpu.usage_percent",
                name="CPU Usage",
                description="System CPU usage percentage",
                metric_type=MetricType.SYSTEM,
                unit="percent",
                collection_interval_seconds=60,
                retention_days=30,
                thresholds={"warning_max": 80.0, "critical_max": 95.0}
            ),
            MetricDefinition(
                metric_id="system.memory.usage_percent",
                name="Memory Usage",
                description="System memory usage percentage",
                metric_type=MetricType.SYSTEM,
                unit="percent",
                collection_interval_seconds=60,
                retention_days=30,
                thresholds={"warning_max": 85.0, "critical_max": 95.0}
            ),
            MetricDefinition(
                metric_id="system.disk.usage_percent",
                name="Disk Usage",
                description="System disk usage percentage",
                metric_type=MetricType.SYSTEM,
                unit="percent",
                collection_interval_seconds=300,
                retention_days=30,
                thresholds={"warning_max": 80.0, "critical_max": 90.0}
            )
        ]
        
        for metric in default_metrics:
            self.metric_definitions[metric.metric_id] = metric
    
    async def inject_nextgen_services(self, 
                                    llm_gateway: LLMGatewayHybrid,
                                    message_bus: MessageBusA2A, 
                                    context_store: OptimizedContextStore):
        """Injection des services NextGeneration v5.3.0"""
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus  
        self.context_store = context_store
        
        # Configuration composants avec IA
        self.anomaly_detector.llm_gateway = llm_gateway
        
        # Configuration contexte monitoring IA
        await self._setup_monitoring_context()
        
        self.logger.info("✅ Services NextGeneration injectés - Monitoring IA actif")
    
    async def _setup_monitoring_context(self):
        """Configuration contexte monitoring IA spécialisé"""
        if not self.llm_gateway:
            return
        
        monitoring_context = {
            "role": "monitoring_observability_expert",
            "domain": "enterprise_monitoring_operations",
            "capabilities": [
                "System monitoring and alerting",
                "Anomaly detection and analysis",
                "Performance trend prediction",
                "Root cause analysis",
                "Intelligent alerting"
            ],
            "patterns": [
                "OBSERVABILITY",
                "ALERTING",
                "LLM_ENHANCED"
            ]
        }
        
        # Chargement expertise monitoring depuis LLM
        try:
            response = await self.llm_gateway.process_request(
                "Load monitoring operations expertise",
                context=monitoring_context
            )
            
            if response.get("success"):
                self.logger.info("🧠 Expertise monitoring IA chargée")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement contexte IA: {e}")
    
    async def register_metric(self, metric_def: MetricDefinition) -> bool:
        """Enregistrement métrique monitoring"""
        try:
            self.metric_definitions[metric_def.metric_id] = metric_def
            self.metric_values[metric_def.metric_id] = []
            self.logger.info(f"📊 Métrique enregistrée: {metric_def.name}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur enregistrement métrique: {e}")
            return False
    
    async def collect_metric(self, metric_value: MetricValue) -> bool:
        """Collection valeur métrique"""
        try:
            metric_id = metric_value.metric_id
            
            # Stockage en mémoire
            if metric_id not in self.metric_values:
                self.metric_values[metric_id] = []
            
            self.metric_values[metric_id].append(metric_value)
            
            # Limitation taille mémoire
            max_memory_values = 1440  # 24h à 1 minute
            if len(self.metric_values[metric_id]) > max_memory_values:
                self.metric_values[metric_id] = self.metric_values[metric_id][-max_memory_values:]
            
            # Stockage base de données
            await self._store_metric_to_db(metric_value)
            
            # Évaluation alertes
            if metric_id in self.metric_definitions:
                await self.alert_manager.evaluate_alerts(
                    metric_value, 
                    self.metric_definitions[metric_id]
                )
            
            # Détection anomalies si activée
            if (self.monitoring_config["anomaly_detection_enabled"] and 
                len(self.metric_values[metric_id]) >= 20):
                anomalies = await self.anomaly_detector.detect_anomalies(
                    metric_id, 
                    self.metric_values[metric_id][-50:]
                )
                
                if anomalies:
                    self.monitoring_metrics["anomalies_detected"] += len(anomalies)
                    await self._handle_anomalies(anomalies)
            
            self.monitoring_metrics["metrics_collected"] += 1
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur collection métrique: {e}")
            return False
    
    async def _store_metric_to_db(self, metric_value: MetricValue):
        """Stockage métrique en base"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO metric_values 
                   (metric_id, timestamp, value, tags, metadata) 
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    metric_value.metric_id,
                    metric_value.timestamp.isoformat(),
                    metric_value.value,
                    json.dumps(metric_value.tags or {}),
                    json.dumps(metric_value.metadata or {})
                )
            )
    
    async def _handle_anomalies(self, anomalies: List[Dict[str, Any]]):
        """Gestion anomalies détectées"""
        for anomaly in anomalies:
            self.logger.warning(f"🔍 Anomalie détectée: {anomaly['type']} sur {anomaly['metric_id']}")
            
            # Notification anomalie
            if self.message_bus:
                await self.message_bus.publish(
                    create_envelope(
                        message_type=MessageType.ALERT,
                        payload={
                            "type": "monitoring_anomaly",
                            "anomaly": anomaly,
                            "timestamp": datetime.now().isoformat()
                        },
                        priority=Priority.MEDIUM
                    )
                )
    
    async def get_metric_history(self, metric_id: str, 
                               hours_back: int = 24) -> List[MetricValue]:
        """Récupération historique métrique"""
        start_time = datetime.now() - timedelta(hours=hours_back)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """SELECT * FROM metric_values 
                   WHERE metric_id = ? AND timestamp >= ? 
                   ORDER BY timestamp""",
                (metric_id, start_time.isoformat())
            )
            
            rows = cursor.fetchall()
            
            return [
                MetricValue(
                    metric_id=row["metric_id"],
                    timestamp=datetime.fromisoformat(row["timestamp"]),
                    value=row["value"],
                    tags=json.loads(row["tags"]) if row["tags"] else None,
                    metadata=json.loads(row["metadata"]) if row["metadata"] else None
                )
                for row in rows
            ]
    
    async def _start_background_tasks(self):
        """Démarrage tâches background"""
        self._collection_task = asyncio.create_task(self._metrics_collection_loop())
        self._analysis_task = asyncio.create_task(self._analysis_loop())
        self._health_check_task = asyncio.create_task(self._health_check_loop())
    
    async def _metrics_collection_loop(self):
        """Boucle collection métriques"""
        while True:
            try:
                interval = self.monitoring_config["collection_interval_seconds"]
                await asyncio.sleep(interval)
                
                # Collection métriques système
                system_metrics = await self.metrics_collector.collect_system_metrics()
                for metric in system_metrics:
                    await self.collect_metric(metric)
                
                # Collection métriques applications
                # En production: découverte automatique applications
                for app in ["nextgeneration", "webapp"]:
                    app_metrics = await self.metrics_collector.collect_application_metrics(app)
                    for metric in app_metrics:
                        await self.collect_metric(metric)
                        
            except Exception as e:
                self.logger.error(f"❌ Erreur collection métriques: {e}")
    
    async def _analysis_loop(self):
        """Boucle analyse et prédictions"""
        while True:
            try:
                await asyncio.sleep(300)  # Analyse toutes les 5 minutes
                
                if not self.monitoring_config["ai_predictions_enabled"]:
                    continue
                
                # Génération prédictions pour métriques clés
                for metric_id in ["system.cpu.usage_percent", "system.memory.usage_percent"]:
                    if metric_id in self.metric_values:
                        history = await self.get_metric_history(metric_id, hours_back=24)
                        if len(history) >= 50:
                            prediction = await self.anomaly_detector.predict_metric_trends(
                                metric_id, history
                            )
                            
                            if prediction.get("prediction_available"):
                                self.monitoring_metrics["predictions_generated"] += 1
                                self.logger.info(f"🔮 Prédiction {metric_id}: {prediction['trend_direction']}")
                                
            except Exception as e:
                self.logger.error(f"❌ Erreur analyse: {e}")
    
    async def _health_check_loop(self):
        """Boucle health check services"""
        while True:
            try:
                await asyncio.sleep(120)  # Health check toutes les 2 minutes
                
                # Calcul score santé système global
                health_score = await self._calculate_system_health_score()
                self.monitoring_metrics["system_health_score"] = health_score
                
                if health_score < 70:
                    self.logger.warning(f"⚠️ System health degraded: {health_score}%")
                    
            except Exception as e:
                self.logger.error(f"❌ Erreur health check: {e}")
    
    async def _calculate_system_health_score(self) -> float:
        """Calcul score santé système"""
        scores = []
        
        # Score CPU
        if "system.cpu.usage_percent" in self.metric_values:
            recent_cpu = self.metric_values["system.cpu.usage_percent"][-5:]
            if recent_cpu:
                avg_cpu = sum(m.value for m in recent_cpu) / len(recent_cpu)
                cpu_score = max(0, 100 - avg_cpu)
                scores.append(cpu_score)
        
        # Score mémoire
        if "system.memory.usage_percent" in self.metric_values:
            recent_memory = self.metric_values["system.memory.usage_percent"][-5:]
            if recent_memory:
                avg_memory = sum(m.value for m in recent_memory) / len(recent_memory)
                memory_score = max(0, 100 - avg_memory)
                scores.append(memory_score)
        
        # Score alertes actives
        active_alerts = len([a for a in self.alert_manager.active_alerts.values() 
                           if not a.resolved_at])
        alert_penalty = min(active_alerts * 10, 50)
        alert_score = max(0, 100 - alert_penalty)
        scores.append(alert_score)
        
        return sum(scores) / len(scores) if scores else 100.0
    
    async def get_monitoring_dashboard(self) -> Dict[str, Any]:
        """Dashboard monitoring complet"""
        active_alerts = [a for a in self.alert_manager.active_alerts.values() 
                        if not a.resolved_at]
        
        recent_anomalies = []
        # Récupération anomalies récentes (simulation)
        
        return {
            "system_health": {
                "score": self.monitoring_metrics["system_health_score"],
                "status": "HEALTHY" if self.monitoring_metrics["system_health_score"] > 80 else "WARNING"
            },
            "metrics": {
                "total_collected": self.monitoring_metrics["metrics_collected"],
                "metrics_tracked": len(self.metric_definitions),
                "collection_rate": f"{self.monitoring_metrics['metrics_collected'] / max(1, time.time() - self._start_time):.1f}/s" if hasattr(self, '_start_time') else "N/A"
            },
            "alerts": {
                "active_count": len(active_alerts),
                "total_triggered": self.monitoring_metrics["alerts_triggered"],
                "recent_alerts": [asdict(a) for a in active_alerts[-5:]]
            },
            "anomalies": {
                "detected_count": self.monitoring_metrics["anomalies_detected"],
                "recent_anomalies": recent_anomalies[-5:]
            },
            "predictions": {
                "generated_count": self.monitoring_metrics["predictions_generated"],
                "ai_enabled": self.monitoring_config["ai_predictions_enabled"]
            },
            "timestamp": datetime.now().isoformat()
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check NextGeneration"""
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "status": "healthy",
            "patterns": self.__nextgen_patterns__,
            "services": {
                "llm_gateway": self.llm_gateway is not None,
                "message_bus": self.message_bus is not None,
                "context_store": self.context_store is not None
            },
            "monitoring": {
                "metrics_tracked": len(self.metric_definitions),
                "active_alerts": len([a for a in self.alert_manager.active_alerts.values() if not a.resolved_at]),
                "system_health_score": self.monitoring_metrics["system_health_score"],
                "anomaly_detection": self.monitoring_config["anomaly_detection_enabled"],
                "ai_predictions": self.monitoring_config["ai_predictions_enabled"]
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function pour compatibilité
def create_monitoring_ops(**config) -> AgentMonitoringOps_Enterprise:
    """Factory function pour créer l'agent"""
    return AgentMonitoringOps_Enterprise(**config)

# Test standalone
async def main():
    """Test de l'agent Monitoring Ops"""
    print("📊 Test Agent Monitoring Ops NextGeneration v5.3.0")
    
    agent = create_monitoring_ops(agent_id="test_monitoring")
    agent._start_time = time.time()
    
    # Health check
    health = await agent.health_check()
    print(f"🏥 Health: {health['status']}")
    
    # Collection métrique test
    test_metric = MetricValue(
        metric_id="system.cpu.usage_percent",
        timestamp=datetime.now(),
        value=75.5,
        tags={"host": "test-server"}
    )
    
    success = await agent.collect_metric(test_metric)
    print(f"📊 Métrique collectée: {success}")
    
    # Attente collection automatique
    await asyncio.sleep(2)
    
    # Dashboard
    dashboard = await agent.get_monitoring_dashboard()
    print(f"📊 Métriques trackées: {dashboard['metrics']['metrics_tracked']}")
    print(f"🏥 Score santé: {dashboard['system_health']['score']:.1f}%")

if __name__ == "__main__":
    asyncio.run(main())