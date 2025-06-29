#!/usr/bin/env python3
"""
🔄 Agent Data Pipeline - NextGeneration v5.3.0
Version enterprise Wave 4 avec pipeline ETL intelligent

Migration Pattern: DATA_PROCESSING + ETL_AUTOMATION + LLM_ENHANCED
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
from typing import Dict, List, Optional, Any, Union, Callable, Generator
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import statistics
from collections import defaultdict, deque
import threading
import queue
import uuid

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

class DataFormat(str, Enum):
    """Formats de données supportés"""
    JSON = "JSON"
    CSV = "CSV"
    PARQUET = "PARQUET"
    AVRO = "AVRO"
    XML = "XML"
    EXCEL = "EXCEL"
    DATABASE = "DATABASE"

class TransformationType(str, Enum):
    """Types de transformations"""
    FILTER = "FILTER"
    MAP = "MAP"
    AGGREGATE = "AGGREGATE"
    JOIN = "JOIN"
    SPLIT = "SPLIT"
    MERGE = "MERGE"
    CLEAN = "CLEAN"
    ENRICH = "ENRICH"
    ML_PREDICTION = "ML_PREDICTION"

class PipelineStatus(str, Enum):
    """Statuts du pipeline"""
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

@dataclass
class DataSource:
    """Source de données"""
    source_id: str
    name: str
    format: DataFormat
    connection_string: str
    schema: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    last_sync: Optional[datetime] = None

@dataclass
class TransformationStep:
    """Étape de transformation"""
    step_id: str
    name: str
    transformation_type: TransformationType
    parameters: Dict[str, Any]
    ml_enhanced: bool = False
    dependencies: List[str] = None
    timeout_seconds: int = 300

@dataclass
class PipelineJob:
    """Job de pipeline"""
    job_id: str
    name: str
    sources: List[DataSource]
    transformations: List[TransformationStep]
    destination: DataSource
    schedule_cron: Optional[str] = None
    priority: int = 1
    retry_count: int = 3
    created_at: datetime = None
    status: PipelineStatus = PipelineStatus.IDLE

@dataclass
class ExecutionMetrics:
    """Métriques d'exécution"""
    job_id: str
    start_time: datetime
    end_time: Optional[datetime]
    records_processed: int
    records_successful: int
    records_failed: int
    bytes_processed: int
    execution_time_ms: float
    memory_peak_mb: float
    cpu_usage_percent: float

class IntelligentDataCleaner:
    """Nettoyeur de données intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.cleaning_patterns = {
            "email_validation": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            "phone_normalization": r'[\+]?[1-9]?[0-9]{7,15}',
            "date_standardization": [
                "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S"
            ],
            "currency_cleaning": r'[\$€£¥₹]?[\d,]+\.?\d*'
        }
        self.ml_models = {}
    
    async def clean_dataset(self, data: pd.DataFrame, 
                           schema: Dict[str, Any]) -> pd.DataFrame:
        """Nettoyage intelligent dataset avec IA"""
        self.logger = logging.getLogger(f"DataCleaner_{id(self)}")
        
        # Nettoyage basique règles
        cleaned_data = data.copy()
        
        # Suppression doublons
        initial_count = len(cleaned_data)
        cleaned_data = cleaned_data.drop_duplicates()
        duplicates_removed = initial_count - len(cleaned_data)
        
        # Nettoyage valeurs manquantes
        cleaned_data = await self._handle_missing_values(cleaned_data, schema)
        
        # Normalisation formats
        cleaned_data = await self._normalize_data_formats(cleaned_data, schema)
        
        # Enhancement IA si disponible
        if self.llm_gateway:
            try:
                ai_suggestions = await self.llm_gateway.process_request(
                    "Analyze data quality and suggest cleaning improvements",
                    context={
                        "role": "data_quality_expert",
                        "dataset_info": {
                            "columns": list(cleaned_data.columns),
                            "dtypes": {col: str(dtype) for col, dtype in cleaned_data.dtypes.items()},
                            "shape": cleaned_data.shape,
                            "missing_count": cleaned_data.isnull().sum().to_dict()
                        },
                        "schema": schema,
                        "task": "data_quality_analysis"
                    }
                )
                
                if ai_suggestions.get("success"):
                    improvements = ai_suggestions.get("improvements", [])
                    cleaned_data = await self._apply_ai_improvements(cleaned_data, improvements)
                    
            except Exception as e:
                self.logger.warning(f"⚠️ Erreur enhancement IA nettoyage: {e}")
        
        return cleaned_data
    
    async def _handle_missing_values(self, data: pd.DataFrame, 
                                   schema: Dict[str, Any]) -> pd.DataFrame:
        """Gestion valeurs manquantes intelligente"""
        result = data.copy()
        
        for column in result.columns:
            if result[column].isnull().any():
                col_type = schema.get("columns", {}).get(column, {}).get("type", "string")
                
                if col_type in ["int", "float", "numeric"]:
                    # Remplacement par médiane pour numériques
                    result[column].fillna(result[column].median(), inplace=True)
                elif col_type == "datetime":
                    # Interpolation pour dates
                    result[column] = pd.to_datetime(result[column], errors='coerce')
                    result[column].fillna(method='ffill', inplace=True)
                else:
                    # Mode pour catégorielles
                    mode_val = result[column].mode()
                    if not mode_val.empty:
                        result[column].fillna(mode_val[0], inplace=True)
        
        return result
    
    async def _normalize_data_formats(self, data: pd.DataFrame, 
                                    schema: Dict[str, Any]) -> pd.DataFrame:
        """Normalisation formats de données"""
        result = data.copy()
        
        for column in result.columns:
            col_info = schema.get("columns", {}).get(column, {})
            col_type = col_info.get("type", "string")
            
            if col_type == "email":
                result[column] = result[column].str.lower().str.strip()
            elif col_type == "phone":
                result[column] = result[column].str.replace(r'[^\d+]', '', regex=True)
            elif col_type == "currency":
                result[column] = result[column].str.replace(r'[^\d.]', '', regex=True)
                result[column] = pd.to_numeric(result[column], errors='coerce')
        
        return result
    
    async def _apply_ai_improvements(self, data: pd.DataFrame, 
                                   improvements: List[Dict]) -> pd.DataFrame:
        """Application améliorations suggérées par IA"""
        result = data.copy()
        
        for improvement in improvements:
            try:
                if improvement.get("type") == "outlier_removal":
                    column = improvement.get("column")
                    if column in result.columns:
                        Q1 = result[column].quantile(0.25)
                        Q3 = result[column].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        result = result[(result[column] >= lower_bound) & 
                                      (result[column] <= upper_bound)]
                
                elif improvement.get("type") == "standardization":
                    column = improvement.get("column")
                    if column in result.columns and result[column].dtype in ['float64', 'int64']:
                        result[column] = (result[column] - result[column].mean()) / result[column].std()
                
            except Exception:
                continue
        
        return result

class MLEnhancedTransformer:
    """Transformateur avec enhancement ML"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.ml_models = {}
        self.prediction_cache = {}
    
    async def transform_with_ml(self, data: pd.DataFrame, 
                              transformation: TransformationStep) -> pd.DataFrame:
        """Transformation avec enhancement ML"""
        if not transformation.ml_enhanced:
            return await self._basic_transform(data, transformation)
        
        try:
            # Transformation de base
            result = await self._basic_transform(data, transformation)
            
            # Enhancement ML si IA disponible
            if self.llm_gateway:
                ml_enhancement = await self.llm_gateway.process_request(
                    "Enhance data transformation with ML predictions",
                    context={
                        "role": "ml_data_engineer",
                        "transformation": asdict(transformation),
                        "data_sample": result.head(10).to_dict() if len(result) > 0 else {},
                        "task": "ml_data_transformation"
                    }
                )
                
                if ml_enhancement.get("success"):
                    result = await self._apply_ml_enhancements(result, ml_enhancement)
            
            return result
            
        except Exception as e:
            self.logger = logging.getLogger(f"MLTransformer_{id(self)}")
            self.logger.error(f"❌ Erreur transformation ML: {e}")
            return await self._basic_transform(data, transformation)
    
    async def _basic_transform(self, data: pd.DataFrame, 
                             transformation: TransformationStep) -> pd.DataFrame:
        """Transformations de base"""
        params = transformation.parameters
        
        if transformation.transformation_type == TransformationType.FILTER:
            condition = params.get("condition", "True")
            return data.query(condition) if condition != "True" else data
        
        elif transformation.transformation_type == TransformationType.MAP:
            column = params.get("column")
            function = params.get("function")
            if column and function:
                data[column] = data[column].apply(eval(function))
        
        elif transformation.transformation_type == TransformationType.AGGREGATE:
            group_by = params.get("group_by", [])
            agg_functions = params.get("aggregations", {})
            if group_by and agg_functions:
                return data.groupby(group_by).agg(agg_functions).reset_index()
        
        elif transformation.transformation_type == TransformationType.CLEAN:
            # Nettoyage automatique
            cleaner = IntelligentDataCleaner(self.llm_gateway)
            schema = params.get("schema", {})
            return await cleaner.clean_dataset(data, schema)
        
        return data
    
    async def _apply_ml_enhancements(self, data: pd.DataFrame, 
                                   enhancement: Dict) -> pd.DataFrame:
        """Application enhancements ML"""
        result = data.copy()
        
        # Ajout prédictions si disponibles
        predictions = enhancement.get("predictions", {})
        for column, values in predictions.items():
            if len(values) == len(result):
                result[f"predicted_{column}"] = values
        
        # Ajout scores de confiance
        confidence_scores = enhancement.get("confidence_scores", [])
        if len(confidence_scores) == len(result):
            result["ml_confidence"] = confidence_scores
        
        return result

class PipelineExecutor:
    """Exécuteur de pipeline intelligent"""
    
    def __init__(self, data_pipeline_agent):
        self.agent = data_pipeline_agent
        self.transformer = MLEnhancedTransformer(data_pipeline_agent.llm_gateway)
        self.cleaner = IntelligentDataCleaner(data_pipeline_agent.llm_gateway)
        self.execution_queue = asyncio.Queue()
        self.active_jobs = {}
    
    async def execute_pipeline(self, job: PipelineJob) -> ExecutionMetrics:
        """Exécution pipeline complète"""
        start_time = datetime.now()
        job_id = job.job_id
        
        metrics = ExecutionMetrics(
            job_id=job_id,
            start_time=start_time,
            end_time=None,
            records_processed=0,
            records_successful=0,
            records_failed=0,
            bytes_processed=0,
            execution_time_ms=0,
            memory_peak_mb=0,
            cpu_usage_percent=0
        )
        
        try:
            self.agent.logger.info(f"🔄 Démarrage pipeline: {job.name}")
            job.status = PipelineStatus.RUNNING
            self.active_jobs[job_id] = job
            
            # Chargement des sources
            data_frames = {}
            for source in job.sources:
                df = await self._load_data_source(source)
                data_frames[source.source_id] = df
                metrics.records_processed += len(df)
                metrics.bytes_processed += df.memory_usage(deep=True).sum()
            
            # Exécution transformations
            final_data = None
            for i, transformation in enumerate(job.transformations):
                self.agent.logger.info(f"🔄 Étape {i+1}: {transformation.name}")
                
                # Sélection données d'entrée
                if i == 0:
                    input_data = list(data_frames.values())[0]  # Premier DataFrame
                else:
                    input_data = final_data
                
                # Transformation
                final_data = await self.transformer.transform_with_ml(input_data, transformation)
                metrics.records_successful += len(final_data)
            
            # Sauvegarde destination
            if final_data is not None and not final_data.empty:
                await self._save_to_destination(final_data, job.destination)
                self.agent.logger.info(f"✅ Pipeline complété: {len(final_data)} records")
            else:
                raise Exception("Aucune donnée à sauvegarder")
            
            job.status = PipelineStatus.COMPLETED
            
        except Exception as e:
            self.agent.logger.error(f"❌ Erreur pipeline {job.name}: {e}")
            job.status = PipelineStatus.FAILED
            metrics.records_failed = metrics.records_processed
            
        finally:
            end_time = datetime.now()
            metrics.end_time = end_time
            metrics.execution_time_ms = (end_time - start_time).total_seconds() * 1000
            
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
        
        return metrics
    
    async def _load_data_source(self, source: DataSource) -> pd.DataFrame:
        """Chargement source de données"""
        if source.format == DataFormat.CSV:
            return pd.read_csv(source.connection_string)
        elif source.format == DataFormat.JSON:
            return pd.read_json(source.connection_string)
        elif source.format == DataFormat.PARQUET:
            return pd.read_parquet(source.connection_string)
        elif source.format == DataFormat.EXCEL:
            return pd.read_excel(source.connection_string)
        else:
            # Simulation pour autres formats
            return pd.DataFrame()
    
    async def _save_to_destination(self, data: pd.DataFrame, destination: DataSource):
        """Sauvegarde vers destination"""
        if destination.format == DataFormat.CSV:
            data.to_csv(destination.connection_string, index=False)
        elif destination.format == DataFormat.JSON:
            data.to_json(destination.connection_string, orient='records')
        elif destination.format == DataFormat.PARQUET:
            data.to_parquet(destination.connection_string)

class AgentDataPipeline_Enterprise:
    """
    🔄 Agent Data Pipeline - Enterprise NextGeneration v5.3.0
    
    Pipeline ETL intelligent avec transformation ML et nettoyage automatique.
    
    Patterns NextGeneration v5.3.0:
    - DATA_PROCESSING: Pipeline ETL haute performance
    - ETL_AUTOMATION: Automatisation complète extraction-transformation-chargement
    - LLM_ENHANCED: Intelligence IA pour nettoyage et transformations
    - PATTERN_FACTORY: Architecture modulaire éprouvée
    """
    
    def __init__(self, agent_id: str = "data_pipeline", 
                 pipeline_root: Path = None):
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
            "DATA_PROCESSING",
            "ETL_AUTOMATION",
            "LLM_ENHANCED",
            "PATTERN_FACTORY"
        ]
        
        # Configuration agent
        self.name = "Data Pipeline Enterprise"
        self.mission = "Pipeline ETL intelligent avec ML et nettoyage automatique"
        self.agent_type = "data_pipeline_enterprise"
        
        # Configuration pipeline
        self.pipeline_root = pipeline_root or Path("/var/lib/nextgeneration/pipelines")
        self.pipeline_root.mkdir(parents=True, exist_ok=True)
        
        # Services NextGeneration (injectés à l'initialisation)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Composants pipeline
        self.executor = PipelineExecutor(self)
        
        # Configuration pipeline
        self.pipeline_config = {
            "max_parallel_jobs": 5,
            "default_timeout_seconds": 1800,
            "retry_attempts": 3,
            "memory_limit_mb": 2048,
            "cache_enabled": True,
            "ml_enhancement_enabled": True
        }
        
        # État pipeline
        self.registered_jobs: Dict[str, PipelineJob] = {}
        self.job_history: List[ExecutionMetrics] = []
        self.data_sources: Dict[str, DataSource] = {}
        
        # Métriques pipeline
        self.pipeline_metrics = {
            "jobs_executed": 0,
            "jobs_successful": 0,
            "jobs_failed": 0,
            "total_records_processed": 0,
            "average_execution_time_ms": 0.0,
            "data_quality_score": 0.0,
            "ml_predictions_count": 0
        }
        
        # Scheduler
        self._scheduler_task = None
        
        # Setup logging
        self._setup_logging()
        
        # Démarrage background tasks
        asyncio.create_task(self._start_background_tasks())
    
    def _setup_logging(self):
        """Configuration logging NextGeneration"""
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="pipeline",
                custom_config={
                    "logger_name": f"nextgen.data.pipeline.{self.agent_id}",
                    "log_dir": "logs/pipeline",
                    "metadata": {
                        "agent_type": "data_pipeline",
                        "agent_role": "data_processing",
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
            self.logger = logging.getLogger(f"DataPipeline_{self.agent_id}")
    
    async def inject_nextgen_services(self, 
                                    llm_gateway: LLMGatewayHybrid,
                                    message_bus: MessageBusA2A, 
                                    context_store: OptimizedContextStore):
        """Injection des services NextGeneration v5.3.0"""
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus  
        self.context_store = context_store
        
        # Configuration composants avec IA
        self.executor.transformer.llm_gateway = llm_gateway
        self.executor.cleaner.llm_gateway = llm_gateway
        
        # Configuration contexte pipeline IA
        await self._setup_pipeline_context()
        
        self.logger.info("✅ Services NextGeneration injectés - Pipeline IA actif")
    
    async def _setup_pipeline_context(self):
        """Configuration contexte pipeline IA spécialisé"""
        if not self.llm_gateway:
            return
        
        pipeline_context = {
            "role": "data_pipeline_expert",
            "domain": "enterprise_data_processing",
            "capabilities": [
                "ETL pipeline orchestration",
                "Intelligent data cleaning",
                "ML-enhanced transformations",
                "Data quality analysis",
                "Performance optimization"
            ],
            "patterns": [
                "DATA_PROCESSING",
                "ETL_AUTOMATION",
                "LLM_ENHANCED"
            ]
        }
        
        # Chargement expertise pipeline depuis LLM
        try:
            response = await self.llm_gateway.process_request(
                "Load data pipeline expertise",
                context=pipeline_context
            )
            
            if response.get("success"):
                self.logger.info("🧠 Expertise pipeline IA chargée")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement contexte IA: {e}")
    
    async def register_job(self, job: PipelineJob) -> bool:
        """Enregistrement job pipeline"""
        try:
            self.registered_jobs[job.job_id] = job
            self.logger.info(f"🔄 Job enregistré: {job.name} ({job.job_id})")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur enregistrement job: {e}")
            return False
    
    async def execute_job(self, job_id: str) -> Optional[ExecutionMetrics]:
        """Exécution job pipeline"""
        if job_id not in self.registered_jobs:
            self.logger.error(f"❌ Job non trouvé: {job_id}")
            return None
        
        job = self.registered_jobs[job_id]
        
        try:
            metrics = await self.executor.execute_pipeline(job)
            
            # Mise à jour métriques globales
            self.pipeline_metrics["jobs_executed"] += 1
            
            if job.status == PipelineStatus.COMPLETED:
                self.pipeline_metrics["jobs_successful"] += 1
            else:
                self.pipeline_metrics["jobs_failed"] += 1
            
            self.pipeline_metrics["total_records_processed"] += metrics.records_processed
            self._update_average_execution_time(metrics.execution_time_ms)
            
            # Stockage historique
            self.job_history.append(metrics)
            
            # Notification via MessageBus
            if self.message_bus:
                await self.message_bus.publish(
                    create_envelope(
                        message_type=MessageType.STATUS,
                        payload={
                            "type": "pipeline_job_completed",
                            "job_id": job_id,
                            "status": job.status.value,
                            "metrics": asdict(metrics),
                            "timestamp": datetime.now().isoformat()
                        },
                        priority=Priority.MEDIUM
                    )
                )
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution job {job_id}: {e}")
            return None
    
    async def add_data_source(self, source: DataSource) -> bool:
        """Ajout source de données"""
        try:
            self.data_sources[source.source_id] = source
            self.logger.info(f"🗄️ Source ajoutée: {source.name} ({source.format.value})")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur ajout source: {e}")
            return False
    
    async def _start_background_tasks(self):
        """Démarrage tâches background"""
        self._scheduler_task = asyncio.create_task(self._pipeline_scheduler())
    
    async def _pipeline_scheduler(self):
        """Scheduler jobs pipeline avec cron"""
        while True:
            try:
                await asyncio.sleep(60)  # Vérification chaque minute
                
                current_time = datetime.now()
                
                for job_id, job in self.registered_jobs.items():
                    if (job.schedule_cron and 
                        job.status == PipelineStatus.IDLE and
                        self._should_run_job(job, current_time)):
                        
                        asyncio.create_task(self.execute_job(job_id))
                        
            except Exception as e:
                self.logger.error(f"❌ Erreur scheduler: {e}")
    
    def _should_run_job(self, job: PipelineJob, current_time: datetime) -> bool:
        """Vérification si job doit être exécuté"""
        # Simulation scheduler cron simple
        # En production: utiliser croniter ou APScheduler
        return True  # Simplification pour démo
    
    def _update_average_execution_time(self, execution_time_ms: float):
        """Mise à jour temps exécution moyen"""
        count = self.pipeline_metrics["jobs_executed"]
        avg = self.pipeline_metrics["average_execution_time_ms"]
        
        self.pipeline_metrics["average_execution_time_ms"] = (
            (avg * (count - 1) + execution_time_ms) / count
        )
    
    async def get_pipeline_stats(self) -> Dict[str, Any]:
        """Statistiques pipeline détaillées"""
        success_rate = 0.0
        if self.pipeline_metrics["jobs_executed"] > 0:
            success_rate = (
                self.pipeline_metrics["jobs_successful"] / 
                self.pipeline_metrics["jobs_executed"] * 100
            )
        
        return {
            "pipeline_metrics": self.pipeline_metrics,
            "success_rate": success_rate,
            "registered_jobs": len(self.registered_jobs),
            "data_sources": len(self.data_sources),
            "active_jobs": len(self.executor.active_jobs),
            "job_history_count": len(self.job_history),
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
            "pipeline": {
                "jobs_registered": len(self.registered_jobs),
                "jobs_executed": self.pipeline_metrics["jobs_executed"],
                "success_rate": (
                    self.pipeline_metrics["jobs_successful"] / 
                    max(1, self.pipeline_metrics["jobs_executed"]) * 100
                ),
                "records_processed": self.pipeline_metrics["total_records_processed"]
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function pour compatibilité
def create_data_pipeline(**config) -> AgentDataPipeline_Enterprise:
    """Factory function pour créer l'agent"""
    return AgentDataPipeline_Enterprise(**config)

# Test standalone
async def main():
    """Test de l'agent Data Pipeline"""
    print("🔄 Test Agent Data Pipeline NextGeneration v5.3.0")
    
    agent = create_data_pipeline(agent_id="test_pipeline")
    
    # Health check
    health = await agent.health_check()
    print(f"🏥 Health: {health['status']}")
    
    # Ajout source données
    source = DataSource(
        source_id="source_1",
        name="Données clients",
        format=DataFormat.CSV,
        connection_string="/tmp/clients.csv"
    )
    await agent.add_data_source(source)
    
    # Création destination
    destination = DataSource(
        source_id="dest_1",
        name="Données nettoyées",
        format=DataFormat.PARQUET,
        connection_string="/tmp/clients_clean.parquet"
    )
    
    # Création job pipeline
    job = PipelineJob(
        job_id=str(uuid.uuid4()),
        name="Nettoyage clients",
        sources=[source],
        transformations=[
            TransformationStep(
                step_id="clean_1",
                name="Nettoyage données",
                transformation_type=TransformationType.CLEAN,
                parameters={"schema": {"columns": {}}},
                ml_enhanced=True
            )
        ],
        destination=destination,
        created_at=datetime.now()
    )
    
    # Enregistrement et exécution
    await agent.register_job(job)
    print(f"🔄 Job créé: {job.name}")
    
    # Statistiques
    stats = await agent.get_pipeline_stats()
    print(f"📊 Jobs enregistrés: {stats['registered_jobs']}")

if __name__ == "__main__":
    asyncio.run(main())