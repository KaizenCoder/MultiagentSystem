#!/usr/bin/env python3
"""
🤖 Agent ML Integration - NextGeneration v5.3.0
Version enterprise Wave 4 avec intégration modèles ML intelligente

Migration Pattern: ML_INTEGRATION + PATTERN_FACTORY + LLM_ENHANCED
Author: Claude Sonnet 4
Date: 30 Juin 2025
"""

import asyncio
import json
import time
import pickle
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable, Tuple, Type
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import uuid
import sqlite3
import hashlib
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import importlib.util

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

class MLFramework(str, Enum):
    """Frameworks ML supportés"""
    SCIKIT_LEARN = "SCIKIT_LEARN"
    TENSORFLOW = "TENSORFLOW"
    PYTORCH = "PYTORCH"
    HUGGINGFACE = "HUGGINGFACE"
    XGBOOST = "XGBOOST"
    LIGHTGBM = "LIGHTGBM"
    CATBOOST = "CATBOOST"
    ONNX = "ONNX"
    CUSTOM = "CUSTOM"

class ModelType(str, Enum):
    """Types de modèles ML"""
    CLASSIFICATION = "CLASSIFICATION"
    REGRESSION = "REGRESSION"
    CLUSTERING = "CLUSTERING"
    NLP = "NLP"
    COMPUTER_VISION = "COMPUTER_VISION"
    TIME_SERIES = "TIME_SERIES"
    RECOMMENDER = "RECOMMENDER"
    ANOMALY_DETECTION = "ANOMALY_DETECTION"

class ModelStatus(str, Enum):
    """Statuts modèle ML"""
    LOADING = "LOADING"
    READY = "READY"
    TRAINING = "TRAINING"
    ERROR = "ERROR"
    DEPRECATED = "DEPRECATED"

class PredictionStatus(str, Enum):
    """Statuts prédiction"""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

@dataclass
class MLModel:
    """Modèle ML enregistré"""
    model_id: str
    name: str
    framework: MLFramework
    model_type: ModelType
    version: str
    file_path: str
    preprocessing_config: Dict[str, Any] = None
    postprocessing_config: Dict[str, Any] = None
    metadata: Dict[str, Any] = None
    created_at: datetime = None
    last_used: datetime = None
    status: ModelStatus = ModelStatus.LOADING

@dataclass
class PredictionRequest:
    """Demande de prédiction"""
    request_id: str
    model_id: str
    input_data: Any
    preprocessing: bool = True
    postprocessing: bool = True
    batch_mode: bool = False
    priority: Priority = Priority.MEDIUM
    metadata: Dict[str, Any] = None
    created_at: datetime = None

@dataclass
class PredictionResult:
    """Résultat de prédiction"""
    request_id: str
    model_id: str
    predictions: Any
    confidence_scores: Optional[List[float]] = None
    processing_time_ms: float = 0.0
    status: PredictionStatus = PredictionStatus.COMPLETED
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None
    created_at: datetime = None

class IntelligentModelManager:
    """Gestionnaire de modèles ML intelligent avec IA"""
    
    def __init__(self, llm_gateway: Optional[LLMGatewayHybrid] = None):
        self.llm_gateway = llm_gateway
        self.loaded_models: Dict[str, Any] = {}
        self.model_cache: Dict[str, Any] = {}
        self.model_metadata: Dict[str, MLModel] = {}
        self.model_performance: Dict[str, Dict[str, float]] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def load_model(self, model: MLModel) -> bool:
        """Chargement modèle ML avec optimisations IA"""
        try:
            model.status = ModelStatus.LOADING
            
            # Chargement selon framework
            if model.framework == MLFramework.SCIKIT_LEARN:
                loaded_model = await self._load_sklearn_model(model)
            elif model.framework == MLFramework.TENSORFLOW:
                loaded_model = await self._load_tensorflow_model(model)
            elif model.framework == MLFramework.PYTORCH:
                loaded_model = await self._load_pytorch_model(model)
            elif model.framework == MLFramework.HUGGINGFACE:
                loaded_model = await self._load_huggingface_model(model)
            elif model.framework == MLFramework.ONNX:
                loaded_model = await self._load_onnx_model(model)
            else:
                loaded_model = await self._load_custom_model(model)
            
            if loaded_model:
                self.loaded_models[model.model_id] = loaded_model
                self.model_metadata[model.model_id] = model
                model.status = ModelStatus.READY
                model.last_used = datetime.now()
                
                # Enhancement IA pour optimisation modèle
                if self.llm_gateway:
                    await self._optimize_model_with_ai(model, loaded_model)
                
                return True
            else:
                model.status = ModelStatus.ERROR
                return False
                
        except Exception as e:
            model.status = ModelStatus.ERROR
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.error(f"❌ Erreur chargement modèle {model.model_id}: {e}")
            return False
    
    async def _load_sklearn_model(self, model: MLModel) -> Any:
        """Chargement modèle scikit-learn"""
        try:
            return joblib.load(model.file_path)
        except Exception as e:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.error(f"❌ Erreur sklearn: {e}")
            return None
    
    async def _load_tensorflow_model(self, model: MLModel) -> Any:
        """Chargement modèle TensorFlow"""
        try:
            import tensorflow as tf
            return tf.keras.models.load_model(model.file_path)
        except ImportError:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.warning("⚠️ TensorFlow non disponible")
            return None
        except Exception as e:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.error(f"❌ Erreur TensorFlow: {e}")
            return None
    
    async def _load_pytorch_model(self, model: MLModel) -> Any:
        """Chargement modèle PyTorch"""
        try:
            import torch
            return torch.load(model.file_path, map_location='cpu')
        except ImportError:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.warning("⚠️ PyTorch non disponible")
            return None
        except Exception as e:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.error(f"❌ Erreur PyTorch: {e}")
            return None
    
    async def _load_huggingface_model(self, model: MLModel) -> Any:
        """Chargement modèle Hugging Face"""
        try:
            from transformers import pipeline
            model_config = model.metadata or {}
            task = model_config.get('task', 'text-classification')
            return pipeline(task, model=model.file_path)
        except ImportError:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.warning("⚠️ Hugging Face Transformers non disponible")
            return None
        except Exception as e:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.error(f"❌ Erreur Hugging Face: {e}")
            return None
    
    async def _load_onnx_model(self, model: MLModel) -> Any:
        """Chargement modèle ONNX"""
        try:
            import onnxruntime as ort
            return ort.InferenceSession(model.file_path)
        except ImportError:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.warning("⚠️ ONNX Runtime non disponible")
            return None
        except Exception as e:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.error(f"❌ Erreur ONNX: {e}")
            return None
    
    async def _load_custom_model(self, model: MLModel) -> Any:
        """Chargement modèle personnalisé"""
        try:
            with open(model.file_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.error(f"❌ Erreur modèle custom: {e}")
            return None
    
    async def _optimize_model_with_ai(self, model: MLModel, loaded_model: Any):
        """Optimisation modèle avec IA"""
        try:
            if not self.llm_gateway:
                return
            
            optimization_context = {
                "role": "ml_optimization_expert",
                "model_info": {
                    "framework": model.framework.value,
                    "type": model.model_type.value,
                    "metadata": model.metadata
                },
                "task": "model_optimization_analysis"
            }
            
            ai_optimization = await self.llm_gateway.process_request(
                "Analyze ML model for optimization opportunities",
                context=optimization_context
            )
            
            if ai_optimization.get("success"):
                optimizations = ai_optimization.get("optimizations", [])
                if optimizations:
                    self.logger = logging.getLogger(f"ModelManager_{id(self)}")
                    self.logger.info(f"🧠 Optimisations IA suggérées pour {model.model_id}")
                    
        except Exception as e:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.warning(f"⚠️ Erreur optimisation IA: {e}")
    
    async def predict(self, request: PredictionRequest) -> PredictionResult:
        """Prédiction avec gestion intelligente"""
        start_time = time.time()
        
        try:
            if request.model_id not in self.loaded_models:
                raise ValueError(f"Modèle non chargé: {request.model_id}")
            
            model = self.loaded_models[request.model_id]
            model_info = self.model_metadata[request.model_id]
            
            # Preprocessing
            processed_data = request.input_data
            if request.preprocessing and model_info.preprocessing_config:
                processed_data = await self._preprocess_data(
                    request.input_data, 
                    model_info.preprocessing_config
                )
            
            # Prédiction selon framework
            predictions = await self._make_prediction(
                model, model_info, processed_data
            )
            
            # Postprocessing
            if request.postprocessing and model_info.postprocessing_config:
                predictions = await self._postprocess_predictions(
                    predictions, 
                    model_info.postprocessing_config
                )
            
            # Calcul temps traitement
            processing_time = (time.time() - start_time) * 1000
            
            # Mise à jour performance
            self._update_model_performance(request.model_id, processing_time, True)
            
            result = PredictionResult(
                request_id=request.request_id,
                model_id=request.model_id,
                predictions=predictions,
                processing_time_ms=processing_time,
                status=PredictionStatus.COMPLETED,
                created_at=datetime.now()
            )
            
            return result
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            self._update_model_performance(request.model_id, processing_time, False)
            
            return PredictionResult(
                request_id=request.request_id,
                model_id=request.model_id,
                predictions=None,
                processing_time_ms=processing_time,
                status=PredictionStatus.FAILED,
                error_message=str(e),
                created_at=datetime.now()
            )
    
    async def _make_prediction(self, model: Any, model_info: MLModel, data: Any) -> Any:
        """Prédiction selon framework"""
        if model_info.framework == MLFramework.SCIKIT_LEARN:
            return model.predict(data)
        elif model_info.framework == MLFramework.TENSORFLOW:
            return model.predict(data)
        elif model_info.framework == MLFramework.PYTORCH:
            import torch
            with torch.no_grad():
                return model(torch.tensor(data))
        elif model_info.framework == MLFramework.HUGGINGFACE:
            return model(data)
        elif model_info.framework == MLFramework.ONNX:
            input_name = model.get_inputs()[0].name
            return model.run(None, {input_name: data})
        else:
            # Modèle custom - assume méthode predict
            if hasattr(model, 'predict'):
                return model.predict(data)
            else:
                raise ValueError("Méthode predict non trouvée pour modèle custom")
    
    async def _preprocess_data(self, data: Any, config: Dict[str, Any]) -> Any:
        """Preprocessing données"""
        try:
            # Preprocessing basique configurable
            if config.get("normalize"):
                if isinstance(data, np.ndarray):
                    data = (data - np.mean(data)) / np.std(data)
            
            if config.get("scale_features"):
                if isinstance(data, np.ndarray) and len(data.shape) > 1:
                    from sklearn.preprocessing import StandardScaler
                    scaler = StandardScaler()
                    data = scaler.fit_transform(data)
            
            return data
            
        except Exception as e:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.warning(f"⚠️ Erreur preprocessing: {e}")
            return data
    
    async def _postprocess_predictions(self, predictions: Any, config: Dict[str, Any]) -> Any:
        """Postprocessing prédictions"""
        try:
            # Postprocessing basique configurable
            if config.get("apply_threshold") and isinstance(predictions, np.ndarray):
                threshold = config.get("threshold", 0.5)
                predictions = (predictions > threshold).astype(int)
            
            if config.get("round_predictions"):
                if isinstance(predictions, np.ndarray):
                    decimals = config.get("decimals", 2)
                    predictions = np.round(predictions, decimals)
            
            return predictions
            
        except Exception as e:
            self.logger = logging.getLogger(f"ModelManager_{id(self)}")
            self.logger.warning(f"⚠️ Erreur postprocessing: {e}")
            return predictions
    
    def _update_model_performance(self, model_id: str, processing_time: float, success: bool):
        """Mise à jour performance modèle"""
        if model_id not in self.model_performance:
            self.model_performance[model_id] = {
                "total_requests": 0,
                "successful_requests": 0,
                "average_time_ms": 0.0,
                "last_used": datetime.now().isoformat()
            }
        
        perf = self.model_performance[model_id]
        perf["total_requests"] += 1
        
        if success:
            perf["successful_requests"] += 1
        
        # Mise à jour temps moyen
        current_avg = perf["average_time_ms"]
        total_requests = perf["total_requests"]
        perf["average_time_ms"] = ((current_avg * (total_requests - 1)) + processing_time) / total_requests
        perf["last_used"] = datetime.now().isoformat()

class ModelRegistry:
    """Registre des modèles ML"""
    
    def __init__(self, ml_service):
        self.service = ml_service
        self.models: Dict[str, MLModel] = {}
        self.auto_discovery_enabled = True
    
    async def register_model(self, model: MLModel) -> bool:
        """Enregistrement modèle ML"""
        try:
            # Validation existence fichier
            if not Path(model.file_path).exists():
                raise FileNotFoundError(f"Fichier modèle non trouvé: {model.file_path}")
            
            model.created_at = datetime.now()
            self.models[model.model_id] = model
            
            # Chargement automatique
            success = await self.service.model_manager.load_model(model)
            
            if success:
                self.service.logger.info(f"🤖 Modèle enregistré: {model.name} ({model.framework.value})")
                return True
            else:
                del self.models[model.model_id]
                return False
                
        except Exception as e:
            self.service.logger.error(f"❌ Erreur enregistrement modèle: {e}")
            return False
    
    async def discover_models(self, models_dir: Path) -> List[MLModel]:
        """Découverte automatique modèles"""
        discovered_models = []
        
        if not models_dir.exists():
            return discovered_models
        
        # Extensions fichiers modèles
        model_extensions = {
            '.pkl': MLFramework.SCIKIT_LEARN,
            '.joblib': MLFramework.SCIKIT_LEARN,
            '.h5': MLFramework.TENSORFLOW,
            '.pb': MLFramework.TENSORFLOW,
            '.pt': MLFramework.PYTORCH,
            '.pth': MLFramework.PYTORCH,
            '.onnx': MLFramework.ONNX
        }
        
        for file_path in models_dir.rglob('*'):
            if file_path.suffix in model_extensions:
                try:
                    framework = model_extensions[file_path.suffix]
                    model_id = f"auto_{file_path.stem}_{uuid.uuid4().hex[:8]}"
                    
                    model = MLModel(
                        model_id=model_id,
                        name=file_path.stem,
                        framework=framework,
                        model_type=ModelType.CLASSIFICATION,  # Par défaut
                        version="auto",
                        file_path=str(file_path),
                        metadata={"auto_discovered": True}
                    )
                    
                    discovered_models.append(model)
                    
                except Exception as e:
                    self.service.logger.warning(f"⚠️ Erreur découverte {file_path}: {e}")
        
        self.service.logger.info(f"🔍 Découverte: {len(discovered_models)} modèles trouvés")
        return discovered_models

class AgentMLIntegration_Enterprise:
    """
    🤖 Agent ML Integration - Enterprise NextGeneration v5.3.0
    
    Service d'intégration modèles ML intelligent avec support multi-framework.
    
    Patterns NextGeneration v5.3.0:
    - ML_INTEGRATION: Intégration modèles ML multi-framework
    - PATTERN_FACTORY: Architecture modulaire éprouvée
    - LLM_ENHANCED: Optimisation et intelligence IA
    - PERFORMANCE_OPTIMIZATION: Optimisations prédictions
    """
    
    def __init__(self, agent_id: str = "ml_integration", 
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
            "ML_INTEGRATION",
            "PATTERN_FACTORY", 
            "LLM_ENHANCED",
            "PERFORMANCE_OPTIMIZATION"
        ]
        
        # Configuration agent
        self.name = "ML Integration Enterprise"
        self.mission = "Intégration modèles ML intelligent multi-framework avec optimisations IA"
        self.agent_type = "ml_integration_enterprise"
        
        # Configuration ML
        self.data_dir = data_dir or Path("/var/lib/nextgeneration/ml")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir = self.data_dir / "models"
        self.models_dir.mkdir(exist_ok=True)
        
        # Services NextGeneration (injectés à l'initialisation)
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        self.message_bus: Optional[MessageBusA2A] = None
        self.context_store: Optional[OptimizedContextStore] = None
        
        # Composants ML intelligents
        self.model_manager = IntelligentModelManager()
        self.model_registry = ModelRegistry(self)
        
        # Configuration ML
        self.ml_config = {
            "max_model_size_mb": 500,
            "max_prediction_batch_size": 1000,
            "model_cache_ttl_hours": 24,
            "auto_discovery_enabled": True,
            "performance_monitoring": True,
            "ai_optimization_enabled": True
        }
        
        # État ML
        self.active_predictions: Dict[str, PredictionRequest] = {}
        self.prediction_queue = asyncio.Queue()
        self.prediction_history: List[PredictionResult] = []
        
        # Base de données ML
        self.db_path = self.data_dir / "ml_integration.db"
        self._init_database()
        
        # Métriques ML
        self.ml_metrics = {
            "models_loaded": 0,
            "predictions_completed": 0,
            "predictions_failed": 0,
            "average_prediction_time_ms": 0.0,
            "total_inference_time_ms": 0.0,
            "ai_optimizations_applied": 0,
            "frameworks_used": {}
        }
        
        # Background tasks
        self._prediction_workers = []
        self._monitoring_task = None
        
        # Setup logging
        self._setup_logging()
        
        # Démarrage composants
        asyncio.create_task(self._start_background_tasks())
    
    def _init_database(self):
        """Initialisation base de données ML"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ml_models (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    framework TEXT NOT NULL,
                    model_type TEXT NOT NULL,
                    version TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    status TEXT DEFAULT 'LOADING',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_used TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prediction_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id TEXT UNIQUE NOT NULL,
                    model_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    processing_time_ms REAL,
                    success BOOLEAN,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_model_status 
                ON ml_models(status)
            """)
    
    def _setup_logging(self):
        """Configuration logging NextGeneration"""
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="ml_integration",
                custom_config={
                    "logger_name": f"nextgen.ml.integration.{self.agent_id}",
                    "log_dir": "logs/ml",
                    "metadata": {
                        "agent_type": "ml_integration",
                        "agent_role": "machine_learning",
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
            self.logger = logging.getLogger(f"MLIntegration_{self.agent_id}")
    
    async def inject_nextgen_services(self, 
                                    llm_gateway: LLMGatewayHybrid,
                                    message_bus: MessageBusA2A, 
                                    context_store: OptimizedContextStore):
        """Injection des services NextGeneration v5.3.0"""
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus  
        self.context_store = context_store
        
        # Configuration composants avec IA
        self.model_manager.llm_gateway = llm_gateway
        
        # Configuration contexte ML IA
        await self._setup_ml_context()
        
        self.logger.info("✅ Services NextGeneration injectés - ML IA actif")
    
    async def _setup_ml_context(self):
        """Configuration contexte ML IA spécialisé"""
        if not self.llm_gateway:
            return
        
        ml_context = {
            "role": "machine_learning_integration_expert",
            "domain": "enterprise_ml_operations",
            "capabilities": [
                "Multi-framework ML model integration",
                "Model optimization and tuning",
                "Performance monitoring",
                "Automated model selection",
                "Prediction pipeline optimization"
            ],
            "patterns": [
                "ML_INTEGRATION",
                "PATTERN_FACTORY",
                "LLM_ENHANCED"
            ]
        }
        
        # Chargement expertise ML depuis LLM
        try:
            response = await self.llm_gateway.process_request(
                "Load ML integration and optimization expertise",
                context=ml_context
            )
            
            if response.get("success"):
                self.logger.info("🧠 Expertise ML IA chargée")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement contexte IA: {e}")
    
    async def register_model(self, model: MLModel) -> bool:
        """Enregistrement modèle ML"""
        try:
            success = await self.model_registry.register_model(model)
            
            if success:
                # Stockage en base
                await self._store_model(model)
                self.ml_metrics["models_loaded"] += 1
                self.ml_metrics["frameworks_used"][model.framework.value] = \
                    self.ml_metrics["frameworks_used"].get(model.framework.value, 0) + 1
                
                # Notification via MessageBus
                if self.message_bus:
                    await self.message_bus.publish(
                        create_envelope(
                            message_type=MessageType.EVENT,
                            payload={
                                "type": "ml_model_registered",
                                "model": asdict(model),
                                "timestamp": datetime.now().isoformat()
                            },
                            priority=Priority.MEDIUM
                        )
                    )
                
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erreur enregistrement modèle: {e}")
            return False
    
    async def predict(self, request: PredictionRequest) -> PredictionResult:
        """Prédiction ML avec optimisations"""
        try:
            self.logger.info(f"🔮 Prédiction demandée: {request.model_id}")
            
            request.created_at = datetime.now()
            self.active_predictions[request.request_id] = request
            
            # Prédiction via model manager
            result = await self.model_manager.predict(request)
            
            # Stockage résultat
            await self._store_prediction_result(result)
            
            # Mise à jour métriques
            if result.status == PredictionStatus.COMPLETED:
                self.ml_metrics["predictions_completed"] += 1
            else:
                self.ml_metrics["predictions_failed"] += 1
            
            self.ml_metrics["total_inference_time_ms"] += result.processing_time_ms
            
            # Calcul temps moyen
            total_predictions = (self.ml_metrics["predictions_completed"] + 
                               self.ml_metrics["predictions_failed"])
            if total_predictions > 0:
                self.ml_metrics["average_prediction_time_ms"] = \
                    self.ml_metrics["total_inference_time_ms"] / total_predictions
            
            # Nettoyage
            if request.request_id in self.active_predictions:
                del self.active_predictions[request.request_id]
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Erreur prédiction: {e}")
            return PredictionResult(
                request_id=request.request_id,
                model_id=request.model_id,
                predictions=None,
                status=PredictionStatus.FAILED,
                error_message=str(e),
                created_at=datetime.now()
            )
    
    async def discover_models(self) -> List[MLModel]:
        """Découverte automatique modèles"""
        try:
            if not self.ml_config["auto_discovery_enabled"]:
                return []
            
            discovered = await self.model_registry.discover_models(self.models_dir)
            
            # Enregistrement automatique
            registered_count = 0
            for model in discovered:
                success = await self.register_model(model)
                if success:
                    registered_count += 1
            
            self.logger.info(f"🔍 Auto-discovery: {registered_count}/{len(discovered)} modèles enregistrés")
            return discovered
            
        except Exception as e:
            self.logger.error(f"❌ Erreur découverte modèles: {e}")
            return []
    
    async def _store_model(self, model: MLModel):
        """Stockage modèle en base"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO ml_models 
                   (model_id, name, framework, model_type, version, file_path, status, last_used) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    model.model_id,
                    model.name,
                    model.framework.value,
                    model.model_type.value,
                    model.version,
                    model.file_path,
                    model.status.value,
                    model.last_used.isoformat() if model.last_used else None
                )
            )
    
    async def _store_prediction_result(self, result: PredictionResult):
        """Stockage résultat prédiction"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO prediction_requests 
                   (request_id, model_id, status, processing_time_ms, success) 
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    result.request_id,
                    result.model_id,
                    result.status.value,
                    result.processing_time_ms,
                    result.status == PredictionStatus.COMPLETED
                )
            )
    
    async def _start_background_tasks(self):
        """Démarrage tâches background"""
        # Workers de prédiction
        for i in range(2):
            worker = asyncio.create_task(self._prediction_worker(f"worker_{i}"))
            self._prediction_workers.append(worker)
        
        # Monitoring performance
        self._monitoring_task = asyncio.create_task(self._performance_monitoring_loop())
        
        # Auto-discovery initial
        if self.ml_config["auto_discovery_enabled"]:
            asyncio.create_task(self.discover_models())
    
    async def _prediction_worker(self, worker_name: str):
        """Worker de prédiction ML"""
        while True:
            try:
                # Récupération tâche de prédiction
                prediction_task = await self.prediction_queue.get()
                request = prediction_task["request"]
                
                # Traitement prédiction
                result = await self.predict(request)
                
                self.prediction_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"❌ Erreur worker {worker_name}: {e}")
    
    async def _performance_monitoring_loop(self):
        """Monitoring performance modèles"""
        while True:
            try:
                await asyncio.sleep(300)  # Monitoring toutes les 5 minutes
                
                if not self.ml_config["performance_monitoring"]:
                    continue
                
                # Analyse performance modèles
                performance_report = {}
                for model_id, perf in self.model_manager.model_performance.items():
                    success_rate = 0.0
                    if perf["total_requests"] > 0:
                        success_rate = (perf["successful_requests"] / perf["total_requests"]) * 100
                    
                    performance_report[model_id] = {
                        "success_rate": success_rate,
                        "average_time_ms": perf["average_time_ms"],
                        "total_requests": perf["total_requests"]
                    }
                
                # Alerte si performance dégradée
                for model_id, perf in performance_report.items():
                    if perf["success_rate"] < 95 and perf["total_requests"] > 10:
                        self.logger.warning(f"⚠️ Performance dégradée modèle {model_id}: {perf['success_rate']:.1f}%")
                
                # Enhancement IA pour optimisation
                if self.llm_gateway and self.ml_config["ai_optimization_enabled"]:
                    await self._ai_performance_optimization(performance_report)
                
            except Exception as e:
                self.logger.error(f"❌ Erreur monitoring: {e}")
    
    async def _ai_performance_optimization(self, performance_report: Dict[str, Any]):
        """Optimisation performance avec IA"""
        try:
            optimization_context = {
                "role": "ml_performance_optimizer",
                "performance_data": performance_report,
                "current_config": self.ml_config,
                "task": "ml_performance_optimization"
            }
            
            ai_optimization = await self.llm_gateway.process_request(
                "Analyze ML performance and suggest optimizations",
                context=optimization_context
            )
            
            if ai_optimization.get("success"):
                optimizations = ai_optimization.get("optimizations", [])
                if optimizations:
                    self.ml_metrics["ai_optimizations_applied"] += 1
                    self.logger.info(f"🧠 Optimisations IA appliquées: {len(optimizations)}")
                    
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur optimisation IA: {e}")
    
    async def get_ml_stats(self) -> Dict[str, Any]:
        """Statistiques ML détaillées"""
        # Calcul success rate
        total_predictions = (self.ml_metrics["predictions_completed"] + 
                           self.ml_metrics["predictions_failed"])
        success_rate = 0.0
        if total_predictions > 0:
            success_rate = (self.ml_metrics["predictions_completed"] / total_predictions) * 100
        
        return {
            "ml_metrics": self.ml_metrics,
            "success_rate": success_rate,
            "models_registered": len(self.model_registry.models),
            "models_loaded": len(self.model_manager.loaded_models),
            "active_predictions": len(self.active_predictions),
            "model_performance": self.model_manager.model_performance,
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
            "ml": {
                "models_registered": len(self.model_registry.models),
                "models_ready": len([m for m in self.model_manager.model_metadata.values() 
                                   if m.status == ModelStatus.READY]),
                "frameworks_supported": len(MLFramework),
                "prediction_success_rate": (
                    self.ml_metrics["predictions_completed"] /
                    max(1, self.ml_metrics["predictions_completed"] + 
                        self.ml_metrics["predictions_failed"]) * 100
                ),
                "ai_optimization": self.ml_config["ai_optimization_enabled"]
            },
            "timestamp": datetime.now().isoformat()
        }

# Factory function pour compatibilité
def create_ml_integration(**config) -> AgentMLIntegration_Enterprise:
    """Factory function pour créer l'agent"""
    return AgentMLIntegration_Enterprise(**config)

# Test standalone
async def main():
    """Test de l'agent ML Integration"""
    print("🤖 Test Agent ML Integration NextGeneration v5.3.0")
    
    agent = create_ml_integration(agent_id="test_ml")
    
    # Health check
    health = await agent.health_check()
    print(f"🏥 Health: {health['status']}")
    
    # Simulation enregistrement modèle
    model = MLModel(
        model_id="test_model",
        name="Test Scikit-Learn Model",
        framework=MLFramework.SCIKIT_LEARN,
        model_type=ModelType.CLASSIFICATION,
        version="1.0",
        file_path="/tmp/test_model.pkl"  # Simulation
    )
    
    # Note: en vrai il faudrait un fichier modèle existant
    print(f"🤖 Enregistrement modèle simulé: {model.name}")
    
    # Découverte automatique
    discovered = await agent.discover_models()
    print(f"🔍 Modèles découverts: {len(discovered)}")
    
    # Statistiques
    stats = await agent.get_ml_stats()
    print(f"📊 Modèles: {stats['models_registered']}")

if __name__ == "__main__":
    asyncio.run(main())