#!/usr/bin/env python3
"""
📊 Agent Analytics Engine - NextGeneration v5.3.0
Version enterprise Wave 4 avec BI temps réel intelligent

Migration Pattern: ANALYTICS_ENGINE + REAL_TIME_BI + LLM_ENHANCED
Author: Claude Sonnet 4
Date: 30 Juin 2025
"""

import asyncio
import json
import time
import hashlib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable, Generator, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import statistics
from collections import defaultdict, deque
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
    """Types de métriques analytics"""
    COUNT = "COUNT"
    SUM = "SUM"
    AVERAGE = "AVERAGE"
    MEDIAN = "MEDIAN"
    MIN = "MIN"
    MAX = "MAX"
    PERCENTILE = "PERCENTILE"
    VARIANCE = "VARIANCE"
    CORRELATION = "CORRELATION"
    TREND = "TREND"
    PREDICTION = "PREDICTION"

class VisualizationType(str, Enum):
    """Types de visualisation"""
    LINE_CHART = "LINE_CHART"
    BAR_CHART = "BAR_CHART"
    PIE_CHART = "PIE_CHART"
    HEATMAP = "HEATMAP"
    SCATTER_PLOT = "SCATTER_PLOT"
    HISTOGRAM = "HISTOGRAM"
    BOX_PLOT = "BOX_PLOT"
    TREEMAP = "TREEMAP"
    GAUGE = "GAUGE"
    TABLE = "TABLE"

class AggregationLevel(str, Enum):
    """Niveaux d'agrégation temporelle"""
    REAL_TIME = "REAL_TIME"  # Seconde
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    QUARTER = "QUARTER"
    YEAR = "YEAR"

@dataclass
class MetricDefinition:
    """Définition métrique analytics"""
    metric_id: str
    name: str
    description: str
    metric_type: MetricType
    data_source: str
    calculation_formula: str
    dimensions: List[str]
    filters: Optional[Dict[str, Any]] = None
    refresh_interval_seconds: int = 60
    aggregation_level: AggregationLevel = AggregationLevel.HOUR

@dataclass
class Dashboard:
    """Dashboard de visualisation"""
    dashboard_id: str
    name: str
    description: str
    metrics: List[str]  # Liste des metric_id
    layout: Dict[str, Any]
    refresh_interval_seconds: int = 300
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class AnalyticsQuery:
    """Requête analytics"""
    query_id: str
    metric_id: str
    filters: Dict[str, Any]
    time_range: Dict[str, str]  # start_time, end_time
    aggregation: Optional[str] = None
    group_by: Optional[List[str]] = None
    limit: Optional[int] = None

@dataclass
class AnalyticsResult:
    """Résultat analytics"""
    query_id: str
    metric_id: str
    data: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    generated_at: datetime
    execution_time_ms: float
    cache_hit: bool = False

class IntelligentInsightsEngine:
    """Moteur d'insights intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.pattern_cache = {}
        self.anomaly_thresholds = {}
        self.trend_models = {}
    
    async def generate_insights(self, data: List[Dict[str, Any]], 
                              metric_def: MetricDefinition) -> Dict[str, Any]:
        """Génération insights intelligents"""
        insights = {
            "basic_stats": self._calculate_basic_stats(data),
            "trends": self._detect_trends(data),
            "anomalies": self._detect_anomalies(data, metric_def),
            "patterns": self._identify_patterns(data),
            "ai_insights": []
        }
        
        # Enhancement IA si disponible
        if self.llm_gateway and data:
            try:
                ai_insights = await self.llm_gateway.process_request(
                    "Generate intelligent business insights from analytics data",
                    context={
                        "role": "business_intelligence_expert",
                        "metric": asdict(metric_def),
                        "data_sample": data[-10:] if len(data) > 10 else data,
                        "basic_insights": insights,
                        "task": "business_insights_generation"
                    }
                )
                
                if ai_insights.get("success"):
                    insights["ai_insights"] = ai_insights.get("insights", [])
                    insights["recommendations"] = ai_insights.get("recommendations", [])
                    insights["predictions"] = ai_insights.get("predictions", {})
                    
            except Exception as e:
                insights["ai_insights"].append(f"Erreur IA insights: {e}")
        
        return insights
    
    def _calculate_basic_stats(self, data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calcul statistiques de base"""
        if not data:
            return {}
        
        # Extraction valeurs numériques
        numeric_fields = {}
        for record in data:
            for key, value in record.items():
                if isinstance(value, (int, float)):
                    if key not in numeric_fields:
                        numeric_fields[key] = []
                    numeric_fields[key].append(value)
        
        stats = {}
        for field, values in numeric_fields.items():
            if values:
                stats[f"{field}_mean"] = np.mean(values)
                stats[f"{field}_median"] = np.median(values)
                stats[f"{field}_std"] = np.std(values)
                stats[f"{field}_min"] = np.min(values)
                stats[f"{field}_max"] = np.max(values)
        
        return stats
    
    def _detect_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Détection tendances"""
        trends = {}
        
        if len(data) < 3:
            return trends
        
        # Tri par timestamp si disponible
        sorted_data = sorted(data, key=lambda x: x.get('timestamp', ''))
        
        # Analyse tendance pour chaque champ numérique
        for field in ['value', 'count', 'amount']:  # Champs communs
            values = [record.get(field) for record in sorted_data 
                     if record.get(field) is not None and isinstance(record.get(field), (int, float))]
            
            if len(values) >= 3:
                # Calcul tendance simple (régression linéaire basique)
                x = np.arange(len(values))
                y = np.array(values)
                
                slope = np.corrcoef(x, y)[0, 1] if len(values) > 1 else 0
                
                if slope > 0.1:
                    trends[field] = {"direction": "increasing", "strength": abs(slope)}
                elif slope < -0.1:
                    trends[field] = {"direction": "decreasing", "strength": abs(slope)}
                else:
                    trends[field] = {"direction": "stable", "strength": abs(slope)}
        
        return trends
    
    def _detect_anomalies(self, data: List[Dict[str, Any]], 
                         metric_def: MetricDefinition) -> List[Dict[str, Any]]:
        """Détection anomalies"""
        anomalies = []
        
        if len(data) < 5:  # Pas assez de données
            return anomalies
        
        # Détection anomalies par IQR
        for field in ['value', 'count', 'amount']:
            values = [record.get(field) for record in data 
                     if record.get(field) is not None and isinstance(record.get(field), (int, float))]
            
            if len(values) >= 5:
                Q1 = np.percentile(values, 25)
                Q3 = np.percentile(values, 75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                for i, record in enumerate(data):
                    value = record.get(field)
                    if (value is not None and 
                        isinstance(value, (int, float)) and 
                        (value < lower_bound or value > upper_bound)):
                        
                        anomalies.append({
                            "index": i,
                            "field": field,
                            "value": value,
                            "expected_range": [lower_bound, upper_bound],
                            "severity": "high" if abs(value - np.mean(values)) > 2 * np.std(values) else "medium"
                        })
        
        return anomalies
    
    def _identify_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identification patterns"""
        patterns = {}
        
        if len(data) < 10:
            return patterns
        
        # Pattern temporel (si timestamp disponible)
        timestamps = [record.get('timestamp') for record in data if record.get('timestamp')]
        if timestamps:
            # Analyse distribution temporelle
            hours = [datetime.fromisoformat(ts.replace('Z', '')).hour 
                    for ts in timestamps if isinstance(ts, str)]
            
            if hours:
                hour_counts = defaultdict(int)
                for hour in hours:
                    hour_counts[hour] += 1
                
                peak_hour = max(hour_counts, key=hour_counts.get)
                patterns["peak_hour"] = peak_hour
                patterns["hourly_distribution"] = dict(hour_counts)
        
        # Pattern valeurs récurrentes
        for field in ['category', 'status', 'type']:
            values = [record.get(field) for record in data if record.get(field)]
            if values:
                value_counts = defaultdict(int)
                for value in values:
                    value_counts[value] += 1
                
                patterns[f"{field}_distribution"] = dict(value_counts)
        
        return patterns

class RealTimeProcessor:
    """Processeur temps réel pour métriques"""
    
    def __init__(self, analytics_engine):
        self.engine = analytics_engine
        self.real_time_buffers = defaultdict(deque)
        self.buffer_max_size = 1000
        self.processing_queue = asyncio.Queue()
        self.aggregation_cache = {}
    
    async def process_real_time_event(self, event: Dict[str, Any]):
        """Traitement événement temps réel"""
        timestamp = event.get('timestamp', datetime.now().isoformat())
        source = event.get('source', 'unknown')
        
        # Ajout au buffer
        buffer_key = f"{source}_{timestamp[:16]}"  # Minute precision
        self.real_time_buffers[buffer_key].append(event)
        
        # Limitation taille buffer
        if len(self.real_time_buffers[buffer_key]) > self.buffer_max_size:
            self.real_time_buffers[buffer_key].popleft()
        
        # Déclenchement agrégation si nécessaire
        await self._trigger_aggregation_if_needed(source, timestamp)
    
    async def _trigger_aggregation_if_needed(self, source: str, timestamp: str):
        """Déclenchement agrégation selon seuils"""
        current_minute = timestamp[:16]  # YYYY-MM-DDTHH:MM
        
        # Vérification seuil événements
        events_count = sum(len(buffer) for key, buffer in self.real_time_buffers.items() 
                          if key.startswith(source) and key.endswith(current_minute))
        
        if events_count >= 100:  # Seuil arbitraire
            await self._aggregate_minute_data(source, current_minute)
    
    async def _aggregate_minute_data(self, source: str, minute: str):
        """Agrégation données minute"""
        relevant_buffers = [buffer for key, buffer in self.real_time_buffers.items() 
                           if key.startswith(source) and key.endswith(minute)]
        
        all_events = []
        for buffer in relevant_buffers:
            all_events.extend(list(buffer))
        
        if all_events:
            # Calcul métriques agrégées
            aggregated = {
                'timestamp': minute,
                'source': source,
                'event_count': len(all_events),
                'metrics': self._calculate_aggregated_metrics(all_events)
            }
            
            # Stockage cache
            cache_key = f"{source}_{minute}"
            self.aggregation_cache[cache_key] = aggregated
            
            # Notification si configurée
            if self.engine.message_bus:
                await self.engine.message_bus.publish(
                    create_envelope(
                        message_type=MessageType.DATA,
                        payload={
                            "type": "real_time_aggregation",
                            "data": aggregated,
                            "timestamp": datetime.now().isoformat()
                        },
                        priority=Priority.HIGH
                    )
                )
    
    def _calculate_aggregated_metrics(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcul métriques agrégées"""
        metrics = {}
        
        # Métriques de base
        numeric_fields = {}
        for event in events:
            for key, value in event.items():
                if isinstance(value, (int, float)):
                    if key not in numeric_fields:
                        numeric_fields[key] = []
                    numeric_fields[key].append(value)
        
        for field, values in numeric_fields.items():
            if values:
                metrics[f"{field}_sum"] = sum(values)
                metrics[f"{field}_avg"] = np.mean(values)
                metrics[f"{field}_count"] = len(values)
        
        return metrics

class QueryOptimizer:
    """Optimiseur de requêtes analytics"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.query_cache = {}
        self.execution_stats = defaultdict(list)
    
    async def optimize_query(self, query: AnalyticsQuery) -> AnalyticsQuery:
        """Optimisation requête avec IA"""
        optimized_query = query
        
        # Optimisations basiques
        optimized_query = self._apply_basic_optimizations(query)
        
        # Enhancement IA si disponible
        if self.llm_gateway:
            try:
                ai_optimization = await self.llm_gateway.process_request(
                    "Optimize analytics query for performance",
                    context={
                        "role": "query_optimization_expert",
                        "query": asdict(query),
                        "execution_history": self.execution_stats.get(query.metric_id, [])[-5:],
                        "task": "query_performance_optimization"
                    }
                )
                
                if ai_optimization.get("success"):
                    suggestions = ai_optimization.get("optimizations", [])
                    optimized_query = self._apply_ai_optimizations(optimized_query, suggestions)
                    
            except Exception:
                pass
        
        return optimized_query
    
    def _apply_basic_optimizations(self, query: AnalyticsQuery) -> AnalyticsQuery:
        """Optimisations de base"""
        optimized = query
        
        # Limitation automatique si pas de limite
        if not optimized.limit or optimized.limit > 10000:
            optimized.limit = 10000
        
        # Simplification filtres
        if optimized.filters:
            # Suppression filtres vides
            optimized.filters = {k: v for k, v in optimized.filters.items() 
                               if v is not None and v != ""}
        
        return optimized
    
    def _apply_ai_optimizations(self, query: AnalyticsQuery, 
                               suggestions: List[Dict]) -> AnalyticsQuery:
        """Application optimisations IA"""
        optimized = query
        
        for suggestion in suggestions:
            if suggestion.get("type") == "limit_reduction":
                new_limit = suggestion.get("value")
                if new_limit and new_limit < optimized.limit:
                    optimized.limit = new_limit
            
            elif suggestion.get("type") == "filter_optimization":
                new_filters = suggestion.get("filters", {})
                optimized.filters.update(new_filters)
        
        return optimized

class AgentAnalyticsEngine_Enterprise:
    """
    📊 Agent Analytics Engine - Enterprise NextGeneration v5.3.0
    
    Moteur analytics BI temps réel avec insights IA et visualisations intelligentes.
    
    Patterns NextGeneration v5.3.0:
    - ANALYTICS_ENGINE: Moteur analytics haute performance
    - REAL_TIME_BI: Business Intelligence temps réel
    - LLM_ENHANCED: Insights et optimisations IA
    - PATTERN_FACTORY: Architecture modulaire éprouvée
    """
    
    def __init__(self, agent_id: str = "analytics_engine", 
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
            "ANALYTICS_ENGINE",
            "REAL_TIME_BI",
            "LLM_ENHANCED",
            "PATTERN_FACTORY"
        ]
        
        # Configuration agent
        self.name = "Analytics Engine Enterprise"
        self.mission = "BI temps réel avec insights IA et analytics intelligence"
        self.agent_type = "analytics_enterprise"
        
        # Configuration analytics
        self.data_dir = data_dir or Path("/var/lib/nextgeneration/analytics")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Services NextGeneration (injectés à l'initialisation)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Composants analytics intelligents
        self.insights_engine = IntelligentInsightsEngine()
        self.real_time_processor = RealTimeProcessor(self)
        self.query_optimizer = QueryOptimizer()
        
        # Configuration analytics
        self.analytics_config = {
            "cache_ttl_seconds": 300,
            "max_concurrent_queries": 10,
            "real_time_buffer_size": 1000,
            "auto_insights_enabled": True,
            "ml_predictions_enabled": True,
            "performance_optimization": True
        }
        
        # État analytics
        self.metrics: Dict[str, MetricDefinition] = {}
        self.dashboards: Dict[str, Dashboard] = {}
        self.query_cache: Dict[str, AnalyticsResult] = {}
        
        # Base de données locale pour stockage
        self.db_path = self.data_dir / "analytics.db"
        self._init_database()
        
        # Métriques performance
        self.analytics_metrics = {
            "queries_executed": 0,
            "queries_cached": 0,
            "cache_hit_rate": 0.0,
            "average_query_time_ms": 0.0,
            "real_time_events_processed": 0,
            "insights_generated": 0,
            "dashboards_active": 0
        }
        
        # Background tasks
        self._cache_cleanup_task = None
        self._real_time_task = None
        
        # Setup logging
        self._setup_logging()
        
        # Démarrage background tasks
        asyncio.create_task(self._start_background_tasks())
    
    def _init_database(self):
        """Initialisation base de données analytics"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analytics_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    data TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_metric_timestamp 
                ON analytics_data(metric_id, timestamp)
            """)
    
    def _setup_logging(self):
        """Configuration logging NextGeneration"""
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="analytics",
                custom_config={
                    "logger_name": f"nextgen.analytics.engine.{self.agent_id}",
                    "log_dir": "logs/analytics",
                    "metadata": {
                        "agent_type": "analytics_engine",
                        "agent_role": "business_intelligence",
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
            self.logger = logging.getLogger(f"AnalyticsEngine_{self.agent_id}")
    
    async def inject_nextgen_services(self, 
                                    llm_gateway: LLMGatewayHybrid,
                                    message_bus: MessageBusA2A, 
                                    context_store: OptimizedContextStore):
        """Injection des services NextGeneration v5.3.0"""
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus  
        self.context_store = context_store
        
        # Configuration composants avec IA
        self.insights_engine.llm_gateway = llm_gateway
        self.query_optimizer.llm_gateway = llm_gateway
        
        # Configuration contexte analytics IA
        await self._setup_analytics_context()
        
        self.logger.info("✅ Services NextGeneration injectés - Analytics IA actif")
    
    async def _setup_analytics_context(self):
        """Configuration contexte analytics IA spécialisé"""
        if not self.llm_gateway:
            return
        
        analytics_context = {
            "role": "business_intelligence_expert",
            "domain": "enterprise_analytics_engine",
            "capabilities": [
                "Real-time business intelligence",
                "Intelligent insights generation",
                "Query optimization",
                "Anomaly detection",
                "Predictive analytics"
            ],
            "patterns": [
                "ANALYTICS_ENGINE",
                "REAL_TIME_BI",
                "LLM_ENHANCED"
            ]
        }
        
        # Chargement expertise analytics depuis LLM
        try:
            response = await self.llm_gateway.process_request(
                "Load analytics engine expertise",
                context=analytics_context
            )
            
            if response.get("success"):
                self.logger.info("🧠 Expertise analytics IA chargée")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement contexte IA: {e}")
    
    async def register_metric(self, metric: MetricDefinition) -> bool:
        """Enregistrement métrique analytics"""
        try:
            self.metrics[metric.metric_id] = metric
            self.logger.info(f"📊 Métrique enregistrée: {metric.name}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur enregistrement métrique: {e}")
            return False
    
    async def execute_query(self, query: AnalyticsQuery) -> Optional[AnalyticsResult]:
        """Exécution requête analytics avec optimisation"""
        start_time = time.time()
        
        try:
            # Vérification cache
            cache_key = self._generate_cache_key(query)
            if cache_key in self.query_cache:
                cached_result = self.query_cache[cache_key]
                # Vérification fraîcheur
                if (datetime.now() - cached_result.generated_at).total_seconds() < self.analytics_config["cache_ttl_seconds"]:
                    self.analytics_metrics["queries_cached"] += 1
                    cached_result.cache_hit = True
                    return cached_result
            
            # Optimisation requête
            optimized_query = await self.query_optimizer.optimize_query(query)
            
            # Exécution requête
            result_data = await self._execute_optimized_query(optimized_query)
            
            # Génération insights si activé
            insights = {}
            if self.analytics_config["auto_insights_enabled"] and result_data:
                metric_def = self.metrics.get(query.metric_id)
                if metric_def:
                    insights = await self.insights_engine.generate_insights(result_data, metric_def)
                    self.analytics_metrics["insights_generated"] += 1
            
            # Création résultat
            execution_time = (time.time() - start_time) * 1000
            result = AnalyticsResult(
                query_id=query.query_id,
                metric_id=query.metric_id,
                data=result_data,
                metadata={"insights": insights, "optimization_applied": True},
                generated_at=datetime.now(),
                execution_time_ms=execution_time,
                cache_hit=False
            )
            
            # Mise en cache
            self.query_cache[cache_key] = result
            
            # Mise à jour métriques
            self.analytics_metrics["queries_executed"] += 1
            self._update_average_query_time(execution_time)
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution requête: {e}")
            return None
    
    async def _execute_optimized_query(self, query: AnalyticsQuery) -> List[Dict[str, Any]]:
        """Exécution requête optimisée"""
        # Simulation exécution requête sur base de données
        # En production: intégration avec vraie base analytics
        
        # Récupération depuis SQLite local
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Construction requête SQL basique
            sql = "SELECT * FROM analytics_data WHERE metric_id = ?"
            params = [query.metric_id]
            
            # Ajout filtres temporels
            if query.time_range:
                if query.time_range.get("start_time"):
                    sql += " AND timestamp >= ?"
                    params.append(query.time_range["start_time"])
                if query.time_range.get("end_time"):
                    sql += " AND timestamp <= ?"
                    params.append(query.time_range["end_time"])
            
            # Limitation
            if query.limit:
                sql += f" LIMIT {query.limit}"
            
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()
            
            # Conversion en dictionnaires
            result = []
            for row in rows:
                data = json.loads(row["data"])
                data["id"] = row["id"]
                data["timestamp"] = row["timestamp"]
                result.append(data)
        
        return result
    
    async def store_analytics_data(self, metric_id: str, 
                                 timestamp: str, data: Dict[str, Any]) -> bool:
        """Stockage données analytics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO analytics_data (metric_id, timestamp, data) VALUES (?, ?, ?)",
                    (metric_id, timestamp, json.dumps(data))
                )
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur stockage données: {e}")
            return False
    
    async def create_dashboard(self, dashboard: Dashboard) -> bool:
        """Création dashboard"""
        try:
            dashboard.created_at = datetime.now()
            dashboard.updated_at = datetime.now()
            self.dashboards[dashboard.dashboard_id] = dashboard
            self.analytics_metrics["dashboards_active"] = len(self.dashboards)
            self.logger.info(f"📊 Dashboard créé: {dashboard.name}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur création dashboard: {e}")
            return False
    
    async def _start_background_tasks(self):
        """Démarrage tâches background"""
        self._cache_cleanup_task = asyncio.create_task(self._cache_cleanup_loop())
        self._real_time_task = asyncio.create_task(self._real_time_processing_loop())
    
    async def _cache_cleanup_loop(self):
        """Nettoyage cache périodique"""
        while True:
            try:
                await asyncio.sleep(300)  # 5 minutes
                
                now = datetime.now()
                expired_keys = []
                
                for key, result in self.query_cache.items():
                    if (now - result.generated_at).total_seconds() > self.analytics_config["cache_ttl_seconds"]:
                        expired_keys.append(key)
                
                for key in expired_keys:
                    del self.query_cache[key]
                
                if expired_keys:
                    self.logger.info(f"🧹 Cache nettoyé: {len(expired_keys)} entrées expirées")
                
                # Mise à jour cache hit rate
                total_queries = self.analytics_metrics["queries_executed"]
                cached_queries = self.analytics_metrics["queries_cached"]
                if total_queries > 0:
                    self.analytics_metrics["cache_hit_rate"] = (cached_queries / total_queries) * 100
                    
            except Exception as e:
                self.logger.error(f"❌ Erreur nettoyage cache: {e}")
    
    async def _real_time_processing_loop(self):
        """Boucle traitement temps réel"""
        while True:
            try:
                await asyncio.sleep(1)  # Traitement chaque seconde
                
                # Traitement buffer temps réel
                if hasattr(self.real_time_processor, 'processing_queue'):
                    try:
                        event = self.real_time_processor.processing_queue.get_nowait()
                        await self.real_time_processor.process_real_time_event(event)
                        self.analytics_metrics["real_time_events_processed"] += 1
                    except asyncio.QueueEmpty:
                        pass
                    
            except Exception as e:
                self.logger.error(f"❌ Erreur traitement temps réel: {e}")
    
    def _generate_cache_key(self, query: AnalyticsQuery) -> str:
        """Génération clé cache"""
        query_str = json.dumps(asdict(query), sort_keys=True, default=str)
        return hashlib.md5(query_str.encode()).hexdigest()
    
    def _update_average_query_time(self, execution_time_ms: float):
        """Mise à jour temps requête moyen"""
        count = self.analytics_metrics["queries_executed"]
        avg = self.analytics_metrics["average_query_time_ms"]
        
        self.analytics_metrics["average_query_time_ms"] = (
            (avg * (count - 1) + execution_time_ms) / count
        )
    
    async def get_analytics_stats(self) -> Dict[str, Any]:
        """Statistiques analytics détaillées"""
        return {
            "analytics_metrics": self.analytics_metrics,
            "metrics_count": len(self.metrics),
            "dashboards_count": len(self.dashboards),
            "cache_size": len(self.query_cache),
            "real_time_buffers": len(self.real_time_processor.real_time_buffers),
            "patterns": self.__nextgen_patterns__,
            "version": self.version,
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
            "analytics": {
                "metrics_registered": len(self.metrics),
                "dashboards_active": len(self.dashboards),
                "queries_executed": self.analytics_metrics["queries_executed"],
                "cache_hit_rate": self.analytics_metrics["cache_hit_rate"],
                "insights_generated": self.analytics_metrics["insights_generated"]
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function pour compatibilité
def create_analytics_engine(**config) -> AgentAnalyticsEngine_Enterprise:
    """Factory function pour créer l'agent"""
    return AgentAnalyticsEngine_Enterprise(**config)

# Test standalone
async def main():
    """Test de l'agent Analytics Engine"""
    print("📊 Test Agent Analytics Engine NextGeneration v5.3.0")
    
    agent = create_analytics_engine(agent_id="test_analytics")
    
    # Health check
    health = await agent.health_check()
    print(f"🏥 Health: {health['status']}")
    
    # Création métrique
    metric = MetricDefinition(
        metric_id="user_activity",
        name="Activité utilisateurs",
        description="Nombre d'utilisateurs actifs",
        metric_type=MetricType.COUNT,
        data_source="user_events",
        calculation_formula="COUNT(DISTINCT user_id)",
        dimensions=["date", "platform"]
    )
    await agent.register_metric(metric)
    
    # Stockage données test
    await agent.store_analytics_data(
        "user_activity",
        datetime.now().isoformat(),
        {"user_id": "123", "platform": "web", "action": "login"}
    )
    
    # Requête analytics
    query = AnalyticsQuery(
        query_id=str(uuid.uuid4()),
        metric_id="user_activity",
        filters={"platform": "web"},
        time_range={"start_time": (datetime.now() - timedelta(days=1)).isoformat()}
    )
    
    result = await agent.execute_query(query)
    if result:
        print(f"📊 Résultat: {len(result.data)} records")
    
    # Statistiques
    stats = await agent.get_analytics_stats()
    print(f"📊 Métriques: {stats['metrics_count']}")

if __name__ == "__main__":
    asyncio.run(main())