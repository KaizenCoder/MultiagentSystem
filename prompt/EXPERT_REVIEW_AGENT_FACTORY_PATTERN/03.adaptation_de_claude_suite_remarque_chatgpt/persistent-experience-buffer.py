from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, JSON, DateTime, Float, Integer, Index
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timedelta
import asyncio
from typing import Dict, Any, List, Optional
import uuid
from dataclasses import dataclass, asdict
import numpy as np

Base = declarative_base()

# === Modle TimescaleDB ===

class ExperienceORM(Base):
    """Experience stocke dans TimescaleDB"""
    __tablename__ = "experiences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(String, nullable=False, index=True)
    task_type = Column(String, nullable=False, index=True)
    strategy_used = Column(String, nullable=False)
    outcome = Column(String, nullable=False)  # success, partial, failure
    input_features = Column(JSON)
    performance_metrics = Column(JSON)
    context = Column(JSON)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Index composites pour les requtes frquentes
    __table_args__ = (
        Index('idx_agent_timestamp', 'agent_id', 'timestamp'),
        Index('idx_task_timestamp', 'task_type', 'timestamp'),
        Index('idx_strategy_outcome', 'strategy_used', 'outcome'),
    )

# === Experience Buffer Persistant ===

class PersistentExperienceBuffer:
    """Buffer d'expriences avec persistance TimescaleDB et cache local"""
    
    def __init__(
        self,
        db_url: str,
        cache_size: int = 1000,
        write_batch_size: int = 100,
        write_interval_seconds: int = 5
    ):
        self.engine = create_async_engine(
            db_url,
            pool_size=20,
            max_overflow=40,
            pool_pre_ping=True
        )
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        
        # Cache local thread-safe
        self.local_cache: List[Experience] = []
        self.cache_lock = asyncio.Lock()
        self.cache_size = cache_size
        
        # Write batching
        self.write_queue: List[Experience] = []
        self.write_lock = asyncio.Lock()
        self.write_batch_size = write_batch_size
        self.write_interval = write_interval_seconds
        
        # Stats
        self.stats = {
            "total_experiences": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "db_writes": 0,
            "db_reads": 0
        }
        
        # Background tasks
        self._writer_task = None
        self._cache_refresh_task = None
    
    async def initialize(self):
        """Initialise la base et dmarre les tches de fond"""
        # Crer les tables
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
            # Activer TimescaleDB
            await conn.execute(
                "SELECT create_hypertable('experiences', 'timestamp', "
                "chunk_time_interval => INTERVAL '1 day', "
                "if_not_exists => TRUE);"
            )
            
            # Compression automatique aprs 7 jours
            await conn.execute(
                "SELECT add_compression_policy('experiences', "
                "INTERVAL '7 days', if_not_exists => TRUE);"
            )
        
        # Dmarrer les tches de fond
        self._writer_task = asyncio.create_task(self._batch_writer())
        self._cache_refresh_task = asyncio.create_task(self._cache_refresher())
        
        # Charger le cache initial
        await self._refresh_cache()
    
    async def add_experience(self, experience: Experience):
        """Ajoute une exprience avec write-through cache"""
        async with self.write_lock:
            self.write_queue.append(experience)
            
            # Si la queue est pleine, forcer l'criture
            if len(self.write_queue) >= self.write_batch_size:
                await self._flush_write_queue()
        
        # Mise  jour du cache local
        async with self.cache_lock:
            self.local_cache.append(experience)
            
            # Maintenir la taille du cache (LRU)
            if len(self.local_cache) > self.cache_size:
                self.local_cache.pop(0)
        
        self.stats["total_experiences"] += 1
    
    async def get_experiences_for_learning(
        self,
        agent_id: Optional[str] = None,
        task_type: Optional[str] = None,
        min_experiences: int = 100,
        lookback_days: int = 30
    ) -> List[Experience]:
        """Rcupre les expriences avec cache intelligent"""
        
        # Tentative depuis le cache
        cached_results = await self._get_from_cache(
            agent_id, task_type, lookback_days
        )
        
        if len(cached_results) >= min_experiences:
            self.stats["cache_hits"] += 1
            return cached_results
        
        self.stats["cache_misses"] += 1
        
        # Requte  la base
        async with self.async_session() as session:
            query = session.query(ExperienceORM)
            
            # Filtres
            cutoff_date = datetime.utcnow() - timedelta(days=lookback_days)
            query = query.filter(ExperienceORM.timestamp > cutoff_date)
            
            if agent_id:
                query = query.filter(ExperienceORM.agent_id == agent_id)
            if task_type:
                query = query.filter(ExperienceORM.task_type == task_type)
            
            # Ordre et limite
            query = query.order_by(ExperienceORM.timestamp.desc())
            query = query.limit(min_experiences * 2)  # Marge de scurit
            
            # Excution
            result = await session.execute(query)
            experiences_orm = result.scalars().all()
        
        self.stats["db_reads"] += 1
        
        # Conversion en objets Experience
        experiences = [
            self._orm_to_experience(exp_orm) 
            for exp_orm in experiences_orm
        ]
        
        # Mise  jour du cache
        await self._update_cache_with_db_results(experiences)
        
        return experiences[:min_experiences] if len(experiences) >= min_experiences else experiences
    
    async def get_aggregated_metrics(
        self,
        group_by: str = "task_type",
        time_bucket: str = "1 hour",
        lookback_hours: int = 24
    ) -> List[Dict[str, Any]]:
        """Requtes d'agrgation TimescaleDB optimises"""
        
        async with self.async_session() as session:
            # Utilisation des fonctions TimescaleDB
            query = f"""
                SELECT 
                    time_bucket('{time_bucket}', timestamp) AS bucket,
                    {group_by},
                    COUNT(*) as total_count,
                    SUM(CASE WHEN outcome = 'success' THEN 1 ELSE 0 END) as success_count,
                    AVG((performance_metrics->>'processing_time')::float) as avg_processing_time,
                    PERCENTILE_CONT(0.95) WITHIN GROUP (
                        ORDER BY (performance_metrics->>'processing_time')::float
                    ) as p95_processing_time
                FROM experiences
                WHERE timestamp > NOW() - INTERVAL '{lookback_hours} hours'
                GROUP BY bucket, {group_by}
                ORDER BY bucket DESC, {group_by}
            """
            
            result = await session.execute(query)
            rows = result.fetchall()
        
        return [
            {
                "timestamp": row[0],
                group_by: row[1],
                "total_count": row[2],
                "success_count": row[3],
                "success_rate": row[3] / row[2] if row[2] > 0 else 0,
                "avg_processing_time": row[4],
                "p95_processing_time": row[5]
            }
            for row in rows
        ]
    
    async def _batch_writer(self):
        """Tche de fond pour criture batch"""
        while True:
            await asyncio.sleep(self.write_interval)
            
            async with self.write_lock:
                if self.write_queue:
                    await self._flush_write_queue()
    
    async def _flush_write_queue(self):
        """crit le batch en base"""
        if not self.write_queue:
            return
        
        batch = self.write_queue.copy()
        self.write_queue.clear()
        
        async with self.async_session() as session:
            # Conversion en ORM
            orm_objects = [
                ExperienceORM(
                    agent_id=exp.agent_id,
                    task_type=exp.task_type,
                    strategy_used=exp.strategy_used,
                    outcome=exp.outcome,
                    input_features=exp.input_features,
                    performance_metrics=exp.performance_metrics,
                    context=exp.context,
                    timestamp=exp.timestamp
                )
                for exp in batch
            ]
            
            # Bulk insert
            session.add_all(orm_objects)
            await session.commit()
        
        self.stats["db_writes"] += len(batch)
    
    async def _cache_refresher(self):
        """Rafrachit priodiquement le cache"""
        while True:
            await asyncio.sleep(300)  # 5 minutes
            await self._refresh_cache()
    
    async def _refresh_cache(self):
        """Charge les expriences rcentes dans le cache"""
        async with self.async_session() as session:
            # Dernires N expriences
            query = session.query(ExperienceORM)\
                .order_by(ExperienceORM.timestamp.desc())\
                .limit(self.cache_size)
            
            result = await session.execute(query)
            experiences_orm = result.scalars().all()
        
        experiences = [
            self._orm_to_experience(exp_orm)
            for exp_orm in experiences_orm
        ]
        
        async with self.cache_lock:
            self.local_cache = experiences
    
    async def _get_from_cache(
        self,
        agent_id: Optional[str],
        task_type: Optional[str],
        lookback_days: int
    ) -> List[Experience]:
        """Recherche dans le cache local"""
        cutoff_date = datetime.utcnow() - timedelta(days=lookback_days)
        
        async with self.cache_lock:
            filtered = []
            for exp in self.local_cache:
                if exp.timestamp < cutoff_date:
                    continue
                if agent_id and exp.agent_id != agent_id:
                    continue
                if task_type and exp.task_type != task_type:
                    continue
                filtered.append(exp)
        
        return filtered
    
    async def _update_cache_with_db_results(self, experiences: List[Experience]):
        """Met  jour le cache avec les rsultats de la DB"""
        async with self.cache_lock:
            # Fusionner intelligemment
            existing_ids = {exp.timestamp for exp in self.local_cache}
            
            for exp in experiences:
                if exp.timestamp not in existing_ids:
                    self.local_cache.append(exp)
            
            # Trier par timestamp et maintenir la taille
            self.local_cache.sort(key=lambda x: x.timestamp, reverse=True)
            self.local_cache = self.local_cache[:self.cache_size]
    
    def _orm_to_experience(self, orm: ExperienceORM) -> Experience:
        """Convertit ORM en dataclass Experience"""
        return Experience(
            agent_id=orm.agent_id,
            task_type=orm.task_type,
            input_features=orm.input_features,
            strategy_used=orm.strategy_used,
            outcome=orm.outcome,
            performance_metrics=orm.performance_metrics,
            timestamp=orm.timestamp,
            context=orm.context or {}
        )
    
    async def cleanup_old_data(self, retention_days: int = 90):
        """Nettoie les donnes anciennes"""
        async with self.async_session() as session:
            cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
            
            # Suppression avec TimescaleDB drop_chunks (plus efficace)
            await session.execute(
                f"SELECT drop_chunks('experiences', older_than => INTERVAL '{retention_days} days');"
            )
            await session.commit()
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Retourne les statistiques dtailles"""
        async with self.async_session() as session:
            # Stats globales
            total_count = await session.execute(
                "SELECT COUNT(*) FROM experiences"
            )
            total = total_count.scalar()
            
            # Stats par agent
            agent_stats = await session.execute("""
                SELECT 
                    agent_id,
                    COUNT(*) as experience_count,
                    AVG(CASE WHEN outcome = 'success' THEN 1 ELSE 0 END) as success_rate
                FROM experiences
                WHERE timestamp > NOW() - INTERVAL '7 days'
                GROUP BY agent_id
            """)
            
            # Stats par stratgie
            strategy_stats = await session.execute("""
                SELECT 
                    strategy_used,
                    COUNT(*) as usage_count,
                    AVG(CASE WHEN outcome = 'success' THEN 1 ELSE 0 END) as success_rate,
                    AVG((performance_metrics->>'processing_time')::float) as avg_time
                FROM experiences
                WHERE timestamp > NOW() - INTERVAL '7 days'
                GROUP BY strategy_used
            """)
        
        return {
            "total_experiences": total,
            "cache_stats": self.stats,
            "agent_performance": [
                {
                    "agent_id": row[0],
                    "experience_count": row[1],
                    "success_rate": float(row[2])
                }
                for row in agent_stats
            ],
            "strategy_performance": [
                {
                    "strategy": row[0],
                    "usage_count": row[1],
                    "success_rate": float(row[2]),
                    "avg_processing_time": float(row[3]) if row[3] else 0
                }
                for row in strategy_stats
            ]
        }

# === Optimiseur Incrmental avec SGD ===

from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

class IncrementalStrategyOptimizer:
    """Optimiseur incrmental utilisant SGD pour viter le retraining complet"""
    
    def __init__(self, model_dir: str = "./models"):
        self.models: Dict[str, SGDClassifier] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.feature_stats: Dict[str, Dict[str, Any]] = {}
        self.model_dir = model_dir
        self.model_lock = asyncio.Lock()
        
        # Crer le rpertoire des modles
        os.makedirs(model_dir, exist_ok=True)
    
    async def learn_incremental(
        self,
        experiences: List[Experience],
        task_type: str,
        batch_size: int = 32
    ):
        """Apprentissage incrmental par mini-batch"""
        if len(experiences) < 10:
            return
        
        async with self.model_lock:
            # Charger ou crer le modle
            if task_type not in self.models:
                await self._load_or_create_model(task_type)
            
            model = self.models[task_type]
            scaler = self.scalers[task_type]
            
            # Prparer les donnes par batch
            for i in range(0, len(experiences), batch_size):
                batch = experiences[i:i + batch_size]
                X_batch, y_batch = self._prepare_batch(batch)
                
                # Normalisation incrmentale
                X_scaled = scaler.partial_fit(X_batch).transform(X_batch)
                
                # Apprentissage incrmental
                model.partial_fit(X_scaled, y_batch, classes=[0, 1])
            
            # Sauvegarder priodiquement
            if len(experiences) > 100:
                await self._save_model(task_type)
            
            # Mise  jour des stats
            self._update_feature_importance(task_type, model)
    
    async def predict_strategy(
        self,
        task_type: str,
        input_features: Dict[str, Any],
        available_strategies: List[str]
    ) -> Tuple[str, float]:
        """Prdit la meilleure stratgie avec score de confiance"""
        
        async with self.model_lock:
            if task_type not in self.models:
                # Pas de modle, stratgie par dfaut
                return available_strategies[0], 0.5
            
            model = self.models[task_type]
            scaler = self.scalers[task_type]
            
            # Tester chaque stratgie
            best_strategy = None
            best_score = -1
            
            for strategy in available_strategies:
                # Features avec la stratgie
                features_with_strategy = {
                    **input_features,
                    "strategy": strategy
                }
                
                # Prparer et prdire
                X = self._extract_features(features_with_strategy).reshape(1, -1)
                X_scaled = scaler.transform(X)
                
                # Probabilit de succs
                prob_success = model.predict_proba(X_scaled)[0][1]
                
                if prob_success > best_score:
                    best_score = prob_success
                    best_strategy = strategy
        
        return best_strategy, best_score
    
    async def _load_or_create_model(self, task_type: str):
        """Charge un modle existant ou en cre un nouveau"""
        model_path = os.path.join(self.model_dir, f"{task_type}_model.pkl")
        scaler_path = os.path.join(self.model_dir, f"{task_type}_scaler.pkl")
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            # Charger le modle existant
            self.models[task_type] = joblib.load(model_path)
            self.scalers[task_type] = joblib.load(scaler_path)
        else:
            # Crer un nouveau modle
            self.models[task_type] = SGDClassifier(
                loss="log_loss",
                penalty="l2",
                alpha=0.0001,
                max_iter=1,  # Important pour l'incrmental
                warm_start=True,
                learning_rate="adaptive",
                eta0=0.01
            )
            self.scalers[task_type] = StandardScaler()
    
    async def _save_model(self, task_type: str):
        """Sauvegarde le modle et le scaler"""
        model_path = os.path.join(self.model_dir, f"{task_type}_model.pkl")
        scaler_path = os.path.join(self.model_dir, f"{task_type}_scaler.pkl")
        
        joblib.dump(self.models[task_type], model_path)
        joblib.dump(self.scalers[task_type], scaler_path)
    
    def _prepare_batch(
        self,
        experiences: List[Experience]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Prpare un batch pour l'entranement"""
        X = []
        y = []
        
        for exp in experiences:
            features_dict = {
                **exp.input_features,
                "strategy": exp.strategy_used
            }
            X.append(self._extract_features(features_dict))
            y.append(1 if exp.outcome == "success" else 0)
        
        return np.array(X), np.array(y)
    
    def _extract_features(self, data: Dict[str, Any]) -> np.ndarray:
        """Extraction de features robuste"""
        # Liste ordonne des features
        feature_keys = sorted(data.keys())
        features = []
        
        for key in feature_keys:
            value = data[key]
            
            if isinstance(value, (int, float)):
                features.append(float(value))
            elif isinstance(value, bool):
                features.append(1.0 if value else 0.0)
            elif isinstance(value, str):
                # Hash stable pour les catgories
                features.append(hash(value) % 10000 / 10000.0)
            else:
                # Valeur par dfaut pour types non supports
                features.append(0.0)
        
        return np.array(features)
    
    def _update_feature_importance(
        self,
        task_type: str,
        model: SGDClassifier
    ):
        """Met  jour l'importance des features"""
        if hasattr(model, 'coef_'):
            # Coefficients comme proxy d'importance
            importance = np.abs(model.coef_[0])
            
            # Normaliser
            if importance.sum() > 0:
                importance = importance / importance.sum()
            
            self.feature_stats[task_type] = {
                "importance": importance.tolist(),
                "n_features": len(importance),
                "last_updated": datetime.utcnow()
            }

# === Cot et Quota LLM ===

class LLMCostTracker:
    """Tracker de cots et quotas LLM"""
    
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url)
        self.pricing = {
            "gpt-4": {"prompt": 0.03, "completion": 0.06},  # per 1K tokens
            "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
            "claude-2": {"prompt": 0.008, "completion": 0.024}
        }
        self.quotas: Dict[str, float] = {}  # workspace -> budget EUR
        self.usage_lock = asyncio.Lock()
    
    async def track_usage(
        self,
        agent_id: str,
        workspace: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int
    ) -> Dict[str, float]:
        """Enregistre l'utilisation et vrifie les quotas"""
        
        # Calcul du cot
        cost = self._calculate_cost(model, prompt_tokens, completion_tokens)
        
        async with self.usage_lock:
            # Vrifier le quota
            remaining_budget = self.quotas.get(workspace, 100.0)  # 100 par dfaut
            
            if cost > remaining_budget:
                raise Exception(f"Budget exceeded for workspace {workspace}")
            
            # Mise  jour du quota
            self.quotas[workspace] = remaining_budget - cost
            
            # Enregistrement en base
            await self._record_usage(
                agent_id, workspace, model,
                prompt_tokens, completion_tokens, cost
            )
        
        return {
            "cost": cost,
            "remaining_budget": self.quotas[workspace],
            "usage_percentage": (100.0 - self.quotas[workspace]) / 100.0
        }
    
    def _calculate_cost(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int
    ) -> float:
        """Calcule le cot en EUR"""
        if model not in self.pricing:
            model = "gpt-3.5-turbo"  # Dfaut
        
        prices = self.pricing[model]
        prompt_cost = (prompt_tokens / 1000) * prices["prompt"]
        completion_cost = (completion_tokens / 1000) * prices["completion"]
        
        return prompt_cost + completion_cost
    
    async def _record_usage(
        self,
        agent_id: str,
        workspace: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float
    ):
        """Enregistre l'utilisation en base"""
        async with self.engine.begin() as conn:
            await conn.execute("""
                INSERT INTO llm_usage 
                (agent_id, workspace, model, prompt_tokens, completion_tokens, cost_eur, timestamp)
                VALUES ($1, $2, $3, $4, $5, $6, NOW())
            """, agent_id, workspace, model, prompt_tokens, completion_tokens, cost)
    
    async def get_usage_report(
        self,
        workspace: str,
        lookback_days: int = 30
    ) -> Dict[str, Any]:
        """Gnre un rapport d'utilisation"""
        async with self.engine.begin() as conn:
            result = await conn.execute(f"""
                SELECT 
                    DATE_TRUNC('day', timestamp) as day,
                    SUM(prompt_tokens) as total_prompt_tokens,
                    SUM(completion_tokens) as total_completion_tokens,
                    SUM(cost_eur) as total_cost,
                    COUNT(DISTINCT agent_id) as unique_agents
                FROM llm_usage
                WHERE workspace = $1 
                AND timestamp > NOW() - INTERVAL '{lookback_days} days'
                GROUP BY day
                ORDER BY day DESC
            """, workspace)
            
            daily_usage = result.fetchall()
        
        return {
            "workspace": workspace,
            "daily_usage": [
                {
                    "date": row[0],
                    "prompt_tokens": row[1],
                    "completion_tokens": row[2],
                    "cost_eur": float(row[3]),
                    "unique_agents": row[4]
                }
                for row in daily_usage
            ],
            "total_cost": sum(row[3] for row in daily_usage),
            "remaining_budget": self.quotas.get(workspace, 100.0)
        }

# === Exemple d'utilisation complte ===

async def example_usage():
    """Exemple avec tous les composants intgrs"""
    
    # Initialisation
    db_url = "postgresql+asyncpg://user:pass@localhost/timescaledb"
    
    # Buffer persistant
    buffer = PersistentExperienceBuffer(
        db_url=db_url,
        cache_size=2000,
        write_batch_size=50,
        write_interval_seconds=2
    )
    await buffer.initialize()
    
    # Optimiseur incrmental
    optimizer = IncrementalStrategyOptimizer(model_dir="./agent_models")
    
    # Tracker de cots
    cost_tracker = LLMCostTracker(db_url)
    cost_tracker.quotas["workspace-1"] = 50.0  # 50 de budget
    
    # Simulation d'utilisation
    for i in range(100):
        # Crer une exprience
        exp = Experience(
            agent_id="agent-001",
            task_type="text_processing",
            input_features={
                "text_length": np.random.randint(100, 1000),
                "complexity": np.random.choice(["low", "medium", "high"]),
                "priority": np.random.choice([1, 2, 3])
            },
            strategy_used=np.random.choice(["fast", "balanced", "thorough"]),
            outcome=np.random.choice(["success", "failure"], p=[0.8, 0.2]),
            performance_metrics={
                "processing_time": np.random.uniform(0.1, 2.0),
                "memory_usage_mb": np.random.uniform(50, 200)
            },
            timestamp=datetime.utcnow()
        )
        
        # Ajouter au buffer
        await buffer.add_experience(exp)
        
        # Track LLM usage
        if i % 10 == 0:
            usage = await cost_tracker.track_usage(
                agent_id="agent-001",
                workspace="workspace-1",
                model="gpt-3.5-turbo",
                prompt_tokens=np.random.randint(100, 500),
                completion_tokens=np.random.randint(50, 200)
            )
            print(f"LLM usage: {usage}")
        
        # Apprentissage incrmental priodique
        if i % 20 == 0:
            experiences = await buffer.get_experiences_for_learning(
                task_type="text_processing",
                min_experiences=20
            )
            
            if experiences:
                await optimizer.learn_incremental(
                    experiences,
                    "text_processing",
                    batch_size=10
                )
                
                # Prdiction
                best_strategy, confidence = await optimizer.predict_strategy(
                    "text_processing",
                    {"text_length": 500, "complexity": "medium", "priority": 2},
                    ["fast", "balanced", "thorough"]
                )
                print(f"Best strategy: {best_strategy} (confidence: {confidence:.2f})")
    
    # Statistiques finales
    stats = await buffer.get_statistics()
    print(f"\nBuffer statistics: {stats}")
    
    # Mtriques agrges
    metrics = await buffer.get_aggregated_metrics(
        group_by="strategy_used",
        time_bucket="10 minutes",
        lookback_hours=1
    )
    print(f"\nAggregated metrics: {metrics}")
    
    # Rapport de cots
    cost_report = await cost_tracker.get_usage_report("workspace-1", 30)
    print(f"\nCost report: {cost_report}")

if __name__ == "__main__":
    asyncio.run(example_usage())



