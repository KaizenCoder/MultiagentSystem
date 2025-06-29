#!/usr/bin/env python3
"""
📊 Agent Logger Advanced - NextGeneration v5.3.0
Version enterprise Wave 4 avec logging intelligent IA

Migration Pattern: MONITORING + LLM_ENHANCED + OBSERVABILITY
Author: Claude Sonnet 4
Date: 30 Juin 2025
"""

import asyncio
import json
import logging
import logging.handlers
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import re
import statistics
from collections import defaultdict, deque
import traceback

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

class LogLevel(str, Enum):
    """Niveaux de log étendus"""
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"

class LogCategory(str, Enum):
    """Catégories de logs"""
    SYSTEM = "SYSTEM"
    SECURITY = "SECURITY"
    PERFORMANCE = "PERFORMANCE"
    BUSINESS = "BUSINESS"
    AUDIT = "AUDIT"
    DEBUG = "DEBUG"

@dataclass
class LogEntry:
    """Entrée de log enrichie"""
    timestamp: datetime
    level: LogLevel
    category: LogCategory
    agent_id: str
    message: str
    context: Dict[str, Any]
    correlation_id: Optional[str] = None
    trace_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class LogAnalysis:
    """Analyse de logs"""
    patterns_detected: List[str]
    anomalies: List[Dict[str, Any]]
    recommendations: List[str]
    severity_score: float
    trend: str

class IntelligentLogAnalyzer:
    """Analyseur de logs intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.pattern_cache = {}
        self.anomaly_detectors = {
            "error_spike": self._detect_error_spike,
            "performance_degradation": self._detect_performance_degradation,
            "security_threat": self._detect_security_threat,
            "resource_exhaustion": self._detect_resource_exhaustion
        }
        
        # Fenêtres temporelles pour analyse
        self.time_windows = {
            "1min": deque(maxlen=60),
            "5min": deque(maxlen=300),
            "15min": deque(maxlen=900),
            "1hour": deque(maxlen=3600)
        }
        
        # Patterns de détection
        self.detection_patterns = {
            "sql_injection": r"(union|select|insert|update|delete|drop)\s+.*\s+(from|into|where)",
            "path_traversal": r"\.\./|\.\.\\",
            "memory_leak": r"memory|heap|allocation|OutOfMemory",
            "deadlock": r"deadlock|lock timeout|waiting for lock",
            "crash": r"segfault|core dump|fatal error|crashed"
        }
    
    async def analyze_logs(self, logs: List[LogEntry], 
                          time_range: Optional[timedelta] = None) -> LogAnalysis:
        """Analyse intelligente des logs"""
        analysis = LogAnalysis(
            patterns_detected=[],
            anomalies=[],
            recommendations=[],
            severity_score=0.0,
            trend="stable"
        )
        
        # Filtrage temporel
        if time_range:
            cutoff = datetime.now() - time_range
            logs = [log for log in logs if log.timestamp >= cutoff]
        
        if not logs:
            return analysis
        
        # Analyse patterns basiques
        for pattern_name, pattern_regex in self.detection_patterns.items():
            for log in logs:
                if re.search(pattern_regex, log.message, re.IGNORECASE):
                    if pattern_name not in analysis.patterns_detected:
                        analysis.patterns_detected.append(pattern_name)
        
        # Détection anomalies
        for detector_name, detector_func in self.anomaly_detectors.items():
            anomalies = detector_func(logs)
            analysis.anomalies.extend(anomalies)
        
        # Calcul score sévérité
        error_count = sum(1 for log in logs if log.level in [LogLevel.ERROR, LogLevel.CRITICAL])
        analysis.severity_score = min(100, error_count * 10)
        
        # Analyse tendance
        if len(logs) > 10:
            recent_errors = sum(1 for log in logs[-10:] if log.level in [LogLevel.ERROR, LogLevel.CRITICAL])
            older_errors = sum(1 for log in logs[:-10] if log.level in [LogLevel.ERROR, LogLevel.CRITICAL])
            
            if recent_errors > older_errors * 1.5:
                analysis.trend = "degrading"
            elif recent_errors < older_errors * 0.5:
                analysis.trend = "improving"
        
        # Enhancement IA si disponible
        if self.llm_gateway:
            try:
                ai_analysis = await self.llm_gateway.process_request(
                    "Analyze logs for patterns and recommendations",
                    context={
                        "role": "log_analysis_expert",
                        "logs_summary": {
                            "total": len(logs),
                            "errors": error_count,
                            "patterns": analysis.patterns_detected,
                            "time_range": str(time_range) if time_range else "all"
                        },
                        "task": "intelligent_log_analysis"
                    }
                )
                
                if ai_analysis.get("success"):
                    enhancement = ai_analysis.get("analysis", {})
                    analysis.recommendations.extend(
                        enhancement.get("recommendations", [])
                    )
                    
            except Exception:
                pass
        
        # Recommandations basiques si pas d'IA
        if not analysis.recommendations:
            if analysis.severity_score > 50:
                analysis.recommendations.append("High error rate detected - investigate immediately")
            if "memory_leak" in analysis.patterns_detected:
                analysis.recommendations.append("Potential memory leak - monitor heap usage")
            if "security_threat" in [a["type"] for a in analysis.anomalies]:
                analysis.recommendations.append("Security anomaly detected - review access logs")
        
        return analysis
    
    def _detect_error_spike(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        """Détection pics d'erreurs"""
        anomalies = []
        
        # Groupement par minute
        error_counts = defaultdict(int)
        for log in logs:
            if log.level in [LogLevel.ERROR, LogLevel.CRITICAL]:
                minute = log.timestamp.replace(second=0, microsecond=0)
                error_counts[minute] += 1
        
        if error_counts:
            avg_errors = statistics.mean(error_counts.values())
            std_errors = statistics.stdev(error_counts.values()) if len(error_counts) > 1 else 0
            
            for minute, count in error_counts.items():
                if count > avg_errors + 2 * std_errors:
                    anomalies.append({
                        "type": "error_spike",
                        "timestamp": minute,
                        "count": count,
                        "severity": "high",
                        "description": f"Error spike: {count} errors in 1 minute"
                    })
        
        return anomalies
    
    def _detect_performance_degradation(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        """Détection dégradation performance"""
        anomalies = []
        
        # Recherche temps de réponse dans les logs
        response_times = []
        for log in logs:
            if "response_time" in log.context:
                response_times.append((log.timestamp, log.context["response_time"]))
        
        if len(response_times) > 10:
            # Comparaison première moitié vs seconde moitié
            mid = len(response_times) // 2
            first_half_avg = statistics.mean([rt[1] for rt in response_times[:mid]])
            second_half_avg = statistics.mean([rt[1] for rt in response_times[mid:]])
            
            if second_half_avg > first_half_avg * 1.5:
                anomalies.append({
                    "type": "performance_degradation",
                    "timestamp": response_times[mid][0],
                    "metric": "response_time",
                    "change": f"{((second_half_avg / first_half_avg - 1) * 100):.1f}% increase",
                    "severity": "medium"
                })
        
        return anomalies
    
    def _detect_security_threat(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        """Détection menaces sécurité"""
        anomalies = []
        
        # Détection tentatives authentification échouées
        failed_auth = defaultdict(int)
        for log in logs:
            if "authentication" in log.message.lower() and "failed" in log.message.lower():
                if "ip" in log.context:
                    failed_auth[log.context["ip"]] += 1
        
        for ip, count in failed_auth.items():
            if count > 5:
                anomalies.append({
                    "type": "security_threat",
                    "subtype": "brute_force_attempt",
                    "source": ip,
                    "count": count,
                    "severity": "critical",
                    "description": f"Multiple failed authentication attempts from {ip}"
                })
        
        return anomalies
    
    def _detect_resource_exhaustion(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        """Détection épuisement ressources"""
        anomalies = []
        
        # Recherche indicateurs épuisement
        resource_patterns = {
            "memory": r"memory.*exhausted|out of memory|heap.*full",
            "disk": r"disk.*full|no space left|storage.*exhausted",
            "connections": r"connection.*limit|too many connections|pool.*exhausted"
        }
        
        for resource, pattern in resource_patterns.items():
            for log in logs:
                if re.search(pattern, log.message, re.IGNORECASE):
                    anomalies.append({
                        "type": "resource_exhaustion",
                        "resource": resource,
                        "timestamp": log.timestamp,
                        "severity": "critical",
                        "description": f"{resource.capitalize()} exhaustion detected"
                    })
                    break
        
        return anomalies

class StructuredLogger:
    """Logger structuré avec enrichissement contextuel"""
    
    def __init__(self, agent_id: str, log_dir: Path):
        self.agent_id = agent_id
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration handlers
        self.handlers = {}
        self._setup_handlers()
        
        # Context enrichissement
        self.global_context = {
            "agent_id": agent_id,
            "node": "nextgen-001",
            "environment": "production"
        }
        
        # Buffer pour batch logging
        self.log_buffer = []
        self.buffer_size = 100
        self.flush_interval = 5.0
        self._start_flush_timer()
    
    def _setup_handlers(self):
        """Configuration handlers de logging"""
        # Handler fichier JSON structuré
        json_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / f"{self.agent_id}_structured.json",
            maxBytes=100*1024*1024,  # 100MB
            backupCount=10
        )
        json_handler.setFormatter(self._get_json_formatter())
        self.handlers["json"] = json_handler
        
        # Handler fichier texte lisible
        text_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / f"{self.agent_id}_readable.log",
            maxBytes=50*1024*1024,  # 50MB
            backupCount=5
        )
        text_handler.setFormatter(self._get_text_formatter())
        self.handlers["text"] = text_handler
        
        # Handler syslog pour intégration enterprise
        try:
            syslog_handler = logging.handlers.SysLogHandler(address="/dev/log")
            syslog_handler.setFormatter(self._get_syslog_formatter())
            self.handlers["syslog"] = syslog_handler
        except Exception:
            # Syslog non disponible
            pass
    
    def _get_json_formatter(self):
        """Formatter JSON structuré"""
        class JsonFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                    "module": record.module,
                    "function": record.funcName,
                    "line": record.lineno
                }
                
                # Ajout contexte
                if hasattr(record, "context"):
                    log_data["context"] = record.context
                
                # Ajout exception si présente
                if record.exc_info:
                    log_data["exception"] = self.formatException(record.exc_info)
                
                return json.dumps(log_data)
        
        return JsonFormatter()
    
    def _get_text_formatter(self):
        """Formatter texte lisible"""
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def _get_syslog_formatter(self):
        """Formatter syslog"""
        return logging.Formatter(
            f'nextgen[{self.agent_id}]: %(levelname)s %(message)s'
        )
    
    def _start_flush_timer(self):
        """Démarrage timer flush buffer"""
        async def flush_periodically():
            while True:
                await asyncio.sleep(self.flush_interval)
                self.flush_buffer()
        
        asyncio.create_task(flush_periodically())
    
    async def log(self, level: LogLevel, category: LogCategory, 
                  message: str, context: Optional[Dict[str, Any]] = None,
                  correlation_id: Optional[str] = None):
        """Log structuré avec contexte"""
        entry = LogEntry(
            timestamp=datetime.now(),
            level=level,
            category=category,
            agent_id=self.agent_id,
            message=message,
            context={**self.global_context, **(context or {})},
            correlation_id=correlation_id,
            trace_id=context.get("trace_id") if context else None
        )
        
        # Ajout au buffer
        self.log_buffer.append(entry)
        
        # Flush si buffer plein
        if len(self.log_buffer) >= self.buffer_size:
            self.flush_buffer()
        
        # Log immédiat si critique
        if level in [LogLevel.CRITICAL, LogLevel.FATAL]:
            self._write_log_entry(entry)
    
    def flush_buffer(self):
        """Flush buffer vers handlers"""
        for entry in self.log_buffer:
            self._write_log_entry(entry)
        
        self.log_buffer.clear()
    
    def _write_log_entry(self, entry: LogEntry):
        """Écriture entrée vers handlers"""
        # Création LogRecord compatible
        record = logging.LogRecord(
            name=f"{self.agent_id}.{entry.category.value}",
            level=getattr(logging, entry.level.value),
            pathname="",
            lineno=0,
            msg=entry.message,
            args=(),
            exc_info=None
        )
        
        # Ajout contexte
        record.context = entry.context
        
        # Envoi vers handlers
        for handler in self.handlers.values():
            handler.emit(record)

class AgentLoggerAdvanced_Enterprise:
    """
    📊 Agent Logger Advanced - Enterprise NextGeneration v5.3.0
    
    Système de logging intelligent avec analyse IA temps réel.
    
    Patterns NextGeneration v5.3.0:
    - MONITORING: Observabilité avancée
    - LLM_ENHANCED: Analyse intelligente logs
    - OBSERVABILITY: Métriques et traces
    - PATTERN_FACTORY: Architecture modulaire
    """
    
    def __init__(self, agent_id: str = "logger_advanced", 
                 log_root: Path = None):
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
            "MONITORING",
            "LLM_ENHANCED",
            "OBSERVABILITY",
            "PATTERN_FACTORY"
        ]
        
        # Configuration agent
        self.name = "Logger Advanced Enterprise"
        self.mission = "Logging intelligent avec analyse IA temps réel"
        self.agent_type = "logging_enterprise"
        
        # Configuration logging
        self.log_root = log_root or Path("/var/log/nextgeneration")
        self.log_root.mkdir(parents=True, exist_ok=True)
        
        # Services NextGeneration (injectés à l'initialisation)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Composants logging
        self.log_analyzer = IntelligentLogAnalyzer()
        self.structured_logger = StructuredLogger(agent_id, self.log_root)
        
        # État logging
        self.log_store: List[LogEntry] = []
        self.analysis_cache = {}
        self.alert_thresholds = {
            "error_rate": 10.0,  # errors/minute
            "response_time": 1000,  # ms
            "memory_usage": 90.0,  # %
            "disk_usage": 85.0  # %
        }
        
        # Métriques logging
        self.logging_metrics = {
            "logs_processed": 0,
            "analyses_performed": 0,
            "anomalies_detected": 0,
            "alerts_triggered": 0,
            "average_analysis_time": 0.0
        }
        
        # Setup logging interne
        self._setup_logging()
    
    def _setup_logging(self):
        """Configuration logging NextGeneration"""
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="logging",
                custom_config={
                    "logger_name": f"nextgen.logging.advanced.{self.agent_id}",
                    "log_dir": "logs/logging",
                    "metadata": {
                        "agent_type": "logger_advanced",
                        "agent_role": "monitoring",
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
            self.logger = logging.getLogger(f"LoggerAdvanced_{self.agent_id}")
    
    async def inject_nextgen_services(self, 
                                    llm_gateway: LLMGatewayHybrid,
                                    message_bus: MessageBusA2A, 
                                    context_store: OptimizedContextStore):
        """Injection des services NextGeneration v5.3.0"""
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus  
        self.context_store = context_store
        
        # Configuration analyseur avec IA
        self.log_analyzer.llm_gateway = llm_gateway
        
        # Configuration contexte logging IA
        await self._setup_logging_context()
        
        self.logger.info("✅ Services NextGeneration injectés - Logging IA actif")
    
    async def _setup_logging_context(self):
        """Configuration contexte logging IA spécialisé"""
        if not self.llm_gateway:
            return
        
        logging_context = {
            "role": "observability_expert",
            "domain": "enterprise_logging_monitoring",
            "capabilities": [
                "Log pattern analysis",
                "Anomaly detection",
                "Performance monitoring",
                "Security threat detection",
                "Intelligent alerting"
            ],
            "patterns": [
                "MONITORING",
                "OBSERVABILITY",
                "LLM_ENHANCED"
            ]
        }
        
        # Chargement expertise logging depuis LLM
        try:
            response = await self.llm_gateway.process_request(
                "Load logging and monitoring expertise",
                context=logging_context
            )
            
            if response.get("success"):
                self.logger.info("🧠 Expertise logging IA chargée")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement contexte IA: {e}")
    
    async def log(self, level: Union[str, LogLevel], message: str,
                  category: Union[str, LogCategory] = LogCategory.SYSTEM,
                  context: Optional[Dict[str, Any]] = None,
                  correlation_id: Optional[str] = None):
        """Log avec enrichissement contextuel"""
        # Conversion types si nécessaire
        if isinstance(level, str):
            level = LogLevel(level.upper())
        if isinstance(category, str):
            category = LogCategory(category.upper())
        
        # Log structuré
        await self.structured_logger.log(
            level, category, message, context, correlation_id
        )
        
        # Stockage pour analyse
        entry = LogEntry(
            timestamp=datetime.now(),
            level=level,
            category=category,
            agent_id=self.structured_logger.agent_id,
            message=message,
            context=context or {},
            correlation_id=correlation_id
        )
        
        self.log_store.append(entry)
        
        # Limite stockage mémoire
        if len(self.log_store) > 10000:
            self.log_store = self.log_store[-5000:]
        
        # Métriques
        self.logging_metrics["logs_processed"] += 1
        
        # Analyse temps réel si critique
        if level in [LogLevel.ERROR, LogLevel.CRITICAL, LogLevel.FATAL]:
            await self._trigger_realtime_analysis(entry)
    
    async def _trigger_realtime_analysis(self, entry: LogEntry):
        """Déclenchement analyse temps réel"""
        # Analyse dernière minute
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        recent_logs = [
            log for log in self.log_store 
            if log.timestamp >= one_minute_ago
        ]
        
        analysis = await self.log_analyzer.analyze_logs(
            recent_logs, timedelta(minutes=1)
        )
        
        # Alerte si nécessaire
        if analysis.severity_score > 70 or analysis.anomalies:
            await self._send_alert(entry, analysis)
    
    async def _send_alert(self, entry: LogEntry, analysis: LogAnalysis):
        """Envoi alerte via MessageBus"""
        if not self.message_bus:
            return
        
        alert_payload = {
            "alert_type": "log_anomaly",
            "severity": "high" if analysis.severity_score > 80 else "medium",
            "trigger_entry": asdict(entry),
            "analysis": {
                "patterns": analysis.patterns_detected,
                "anomalies": analysis.anomalies,
                "recommendations": analysis.recommendations,
                "score": analysis.severity_score
            },
            "timestamp": datetime.now().isoformat()
        }
        
        await self.message_bus.publish(
            create_envelope(
                message_type=MessageType.ALERT,
                payload=alert_payload,
                priority=Priority.HIGH
            )
        )
        
        self.logging_metrics["alerts_triggered"] += 1
    
    async def analyze_logs(self, time_range: timedelta = timedelta(hours=1),
                          categories: Optional[List[LogCategory]] = None) -> Dict[str, Any]:
        """Analyse logs avec IA"""
        start_time = datetime.now()
        
        self.logger.info(f"📊 Analyse logs: {time_range}")
        
        # Filtrage logs
        cutoff = datetime.now() - time_range
        logs_to_analyze = [
            log for log in self.log_store
            if log.timestamp >= cutoff
        ]
        
        if categories:
            logs_to_analyze = [
                log for log in logs_to_analyze
                if log.category in categories
            ]
        
        # Analyse
        analysis = await self.log_analyzer.analyze_logs(
            logs_to_analyze, time_range
        )
        
        # Statistiques
        stats = self._calculate_statistics(logs_to_analyze)
        
        # Métriques
        execution_time = (datetime.now() - start_time).total_seconds()
        self.logging_metrics["analyses_performed"] += 1
        self.logging_metrics["anomalies_detected"] += len(analysis.anomalies)
        self._update_average_analysis_time(execution_time)
        
        return {
            "time_range": str(time_range),
            "logs_analyzed": len(logs_to_analyze),
            "statistics": stats,
            "analysis": asdict(analysis),
            "metrics": {
                "analysis_time_seconds": execution_time
            }
        }
    
    def _calculate_statistics(self, logs: List[LogEntry]) -> Dict[str, Any]:
        """Calcul statistiques logs"""
        if not logs:
            return {}
        
        # Distribution par niveau
        level_counts = defaultdict(int)
        for log in logs:
            level_counts[log.level.value] += 1
        
        # Distribution par catégorie
        category_counts = defaultdict(int)
        for log in logs:
            category_counts[log.category.value] += 1
        
        # Taux erreur
        error_count = sum(
            1 for log in logs 
            if log.level in [LogLevel.ERROR, LogLevel.CRITICAL, LogLevel.FATAL]
        )
        error_rate = (error_count / len(logs)) * 100 if logs else 0
        
        return {
            "total_logs": len(logs),
            "level_distribution": dict(level_counts),
            "category_distribution": dict(category_counts),
            "error_rate_percent": error_rate,
            "first_log": logs[0].timestamp.isoformat(),
            "last_log": logs[-1].timestamp.isoformat()
        }
    
    def _update_average_analysis_time(self, time: float):
        """Mise à jour temps analyse moyen"""
        count = self.logging_metrics["analyses_performed"]
        avg = self.logging_metrics["average_analysis_time"]
        
        self.logging_metrics["average_analysis_time"] = (
            (avg * (count - 1) + time) / count
        )
    
    async def export_logs(self, format: str = "json", 
                         time_range: Optional[timedelta] = None,
                         output_path: Optional[Path] = None) -> Dict[str, Any]:
        """Export logs dans différents formats"""
        if time_range:
            cutoff = datetime.now() - time_range
            logs_to_export = [
                log for log in self.log_store
                if log.timestamp >= cutoff
            ]
        else:
            logs_to_export = self.log_store
        
        if not output_path:
            output_path = self.log_root / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        
        if format == "json":
            data = [asdict(log) for log in logs_to_export]
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        
        elif format == "csv":
            import csv
            with open(output_path, 'w', newline='') as f:
                if logs_to_export:
                    writer = csv.DictWriter(f, fieldnames=asdict(logs_to_export[0]).keys())
                    writer.writeheader()
                    for log in logs_to_export:
                        writer.writerow(asdict(log))
        
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        return {
            "exported": True,
            "format": format,
            "logs_count": len(logs_to_export),
            "output_path": str(output_path),
            "file_size_bytes": output_path.stat().st_size
        }
    
    async def get_logging_metrics(self) -> Dict[str, Any]:
        """Métriques logging temps réel"""
        return {
            "logging_metrics": self.logging_metrics,
            "log_store_size": len(self.log_store),
            "alert_thresholds": self.alert_thresholds,
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
            "logging": {
                "logs_processed": self.logging_metrics["logs_processed"],
                "analyses_performed": self.logging_metrics["analyses_performed"],
                "alerts_triggered": self.logging_metrics["alerts_triggered"]
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function pour compatibilité
def create_logger_advanced(**config) -> AgentLoggerAdvanced_Enterprise:
    """Factory function pour créer l'agent"""
    return AgentLoggerAdvanced_Enterprise(**config)

# Test standalone
async def main():
    """Test de l'agent Logger Advanced"""
    print("📊 Test Agent Logger Advanced NextGeneration v5.3.0")
    
    agent = create_logger_advanced(agent_id="test_logger")
    
    # Health check
    health = await agent.health_check()
    print(f"🏥 Health: {health['status']}")
    
    # Test logging
    await agent.log(
        LogLevel.INFO,
        "Test log message",
        LogCategory.SYSTEM,
        context={"user": "test", "action": "login"}
    )
    
    await agent.log(
        LogLevel.ERROR,
        "Test error message",
        LogCategory.SECURITY,
        context={"ip": "192.168.1.100", "reason": "authentication failed"}
    )
    
    # Test analyse
    analysis = await agent.analyze_logs(timedelta(minutes=5))
    print(f"📊 Analysis: {analysis['logs_analyzed']} logs, {len(analysis['analysis']['anomalies'])} anomalies")
    
    # Métriques
    metrics = await agent.get_logging_metrics()
    print(f"📈 Logs processed: {metrics['logging_metrics']['logs_processed']}")

if __name__ == "__main__":
    asyncio.run(main())