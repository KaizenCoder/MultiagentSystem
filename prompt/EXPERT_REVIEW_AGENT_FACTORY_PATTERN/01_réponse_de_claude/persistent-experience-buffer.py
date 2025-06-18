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

# === Modèle TimescaleDB ===

class ExperienceORM(Base):
    """Experience stockée dans TimescaleDB"""
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
    
    # Index composites pour les requêtes fréquentes
    __table_args__ = (
        Index('idx_agent_timestamp', 'agent_id', 'timestamp'),
        Index('idx_task_timestamp', 'task_type', 'timestamp'),
        Index('idx_strategy_outcome', 'strategy_used', 'outcome'),
    )

# === Experience Buffer Persistant ===

class PersistentExperienceBuffer:
    """Buffer d'expériences avec persistance TimescaleDB et cache local"""
    
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
        """Initialise la base et démarre les tâches de fond"""
        # Créer les tables
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
            # Activer TimescaleDB
            await conn.execute(
                "SELECT create_hypertable('experiences', 'timestamp', "
                "chunk_time_interval => INTERVAL '1 day', "
                "if_not_exists => TRUE);"
            )
            
            # Compression automatique après 7 jours
            await conn.execute(
                "SELECT add_compression_policy('experiences', "
                "INTERVAL '7 days', if_not_exists => TRUE);"
            )
        
        # Démarrer les tâches de fond
        self._writer_task = asyncio.create_task(self._batch_writer())
        self._cache_refresh_task = asyncio.create_task(self._cache_refresher())
        
        # Charger le cache initial
        await self._refresh_cache()
    
    async def add_experience(self, experience: Experience):
        """Ajoute une expérience avec write-through cache"""
        async with self.write_lock:
            self.write_queue.append(experience)
            
            # Si la queue est pleine, forcer l'écriture
            if len(self.write_queue) >= self.write_batch_size:
                await self._flush_write_queue()
        
        # Mise à jour du cache local
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
        """Récupère les expériences avec cache intelligent"""
        
        # Tentative depuis le cache
        cached_results = await self._get_from_cache(
            agent_id, task_type, lookback_days
        )
        
        if len(cached_results) >= min_experiences:
            self.stats["cache_hits"] += 1
            return cached_results
        
        self.stats["cache_misses"] += 1
        
        # Requête à la base
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
            query = query.limit(min_experiences * 2)  # Marge de sécurité
            
            # Exécution
            result = await session.execute(query)
            experiences_orm = result.scalars().all()
        
        self.stats["db_reads"] += 1
        
        # Conversion en objets Experience
        experiences = [
            self._orm_to_experience(exp_orm) 
            for exp_orm in experiences_orm
        ]
        
        # Mise à jour du cache
        await self._update_cache_with_db_results(experiences)
        
        return experiences[:min_experiences] if len(experiences) >= min_experiences else experiences
    
    async def get_aggregated_metrics(
        self,
        group_by: str = "task_type",
        time_bucket: str = "1 hour",
        lookback_hours: int = 24
    ) -> List[Dict[str, Any]]:
        """Requêtes d'agrégation TimescaleDB optimisées"""
        
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
        """Tâche de fond pour écriture batch"""
        while True:
            await asyncio.sleep(self.write_interval)
            
            async with self.write_lock:
                if self.write_queue:
                    await self._flush_write_queue()
    
    async def _flush_write_queue(self):
        """Écrit le batch en base"""
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
        """Rafraîchit périodiquement le cache"""
        while True:
            await asyncio.sleep(300)  # 5 minutes
            await self._refresh_cache()
    
    async def _refresh_cache(self):
        """Charge les expériences récentes dans le cache"""
        async with self.async_session() as session:
            # Dernières N expériences
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
        """Met à jour le cache avec les résultats de la DB"""
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
        """Nettoie les données anciennes"""
        async with self.async_session() as session:
            cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
            
            # Suppression avec TimescaleDB drop_chunks (plus efficace)
            await session.execute(
                f"SELECT drop_chunks('experiences', older