"""
Modles SQLAlchemy pour PostgreSQL - NextGeneration Memory API
Enterprise-grade models for multi-agent system
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Boolean, Index, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime, timezone

Base = declarative_base()

class AgentSession(Base):
    """Table des sessions d'agents - Enterprise optimized"""
    __tablename__ = "agent_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    agent_id = Column(String(255), nullable=False, index=True)
    agent_type = Column(String(100), nullable=False, index=True)  # supervisor, code_generation, documentation, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True, index=True)
    status = Column(String(50), default="running", index=True)  # running, paused, completed, failed
    total_tokens_used = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    session_metadata = Column(JSONB)
    
    # Relations
    memory_items = relationship("MemoryItem", back_populates="session", cascade="all, delete-orphan")
    state_items = relationship("StateItem", back_populates="session", cascade="all, delete-orphan")
    
    # Index composite pour performance
    __table_args__ = (
        Index('idx_agent_session_active_created', 'is_active', 'created_at'),
        Index('idx_agent_session_type_status', 'agent_type', 'status'),
    )

class MemoryItem(Base):
    """Table des lments de mmoire - Enterprise optimized"""
    __tablename__ = "memory_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("agent_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), index=True)  # SHA256 pour dduplication
    content_type = Column(String(100), default="text", index=True)  # text, code, analysis, error, result
    category = Column(String(100), index=True)  # task, plan, reflection, communication
    importance_score = Column(Integer, default=1, index=True)  # 1-10 pour priorit
    token_count = Column(Integer, default=0)
    embeddings_vector = Column(JSONB)  # Pour recherche smantique
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    accessed_at = Column(DateTime(timezone=True), server_default=func.now())
    access_count = Column(Integer, default=0)
    is_archived = Column(Boolean, default=False, index=True)
    session_metadata = Column(JSONB)
    
    # Relations
    session = relationship("AgentSession", back_populates="memory_items")
    
    # Index pour performance
    __table_args__ = (
        Index('idx_memory_item_session_created', 'session_id', 'created_at'),
        Index('idx_memory_item_type_importance', 'content_type', 'importance_score'),
        Index('idx_memory_item_category_archived', 'category', 'is_archived'),
        Index('idx_memory_item_hash_unique', 'content_hash', 'session_id', unique=True),
    )

class StateItem(Base):
    """Table des tats d'agents - Enterprise optimized"""
    __tablename__ = "state_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("agent_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    key = Column(String(255), nullable=False, index=True)
    value = Column(JSONB, nullable=False)
    data_type = Column(String(50), default="json", index=True)  # json, string, int, config, checkpoint
    namespace = Column(String(100), index=True)  # workflow, memory, config, metrics
    version = Column(Integer, default=1)
    is_encrypted = Column(Boolean, default=False)
    ttl_expires_at = Column(DateTime(timezone=True))  # Pour expiration automatique
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    session = relationship("AgentSession", back_populates="state_items")
    
    # Index pour performance
    __table_args__ = (
        Index('idx_state_item_session_key', 'session_id', 'key', unique=True),
        Index('idx_state_item_namespace_type', 'namespace', 'data_type'),
        Index('idx_state_item_ttl', 'ttl_expires_at'),
    )

class AgentCommunication(Base):
    """Table des communications inter-agents - Enterprise optimized"""
    __tablename__ = "agent_communications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_agent = Column(String(255), nullable=False, index=True)
    to_agent = Column(String(255), nullable=False, index=True)
    session_id = Column(String(255), index=True)  # Pour regrouper les communications par session
    conversation_id = Column(UUID(as_uuid=True), index=True)  # Pour chaner les messages
    parent_message_id = Column(UUID(as_uuid=True), ForeignKey("agent_communications.id"))
    message_type = Column(String(100), nullable=False, index=True)  # task, result, error, query, response
    subject = Column(String(500))  # Sujet du message
    message_content = Column(JSONB, nullable=False)
    priority = Column(String(20), default="normal", index=True)  # low, normal, high, critical, urgent
    status = Column(String(20), default="sent", index=True)  # sent, delivered, read, processed, failed, expired
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    delivered_at = Column(DateTime(timezone=True))
    processed_at = Column(DateTime(timezone=True))
    response_time_ms = Column(Integer)  # Temps de rponse en millisecondes
    session_metadata = Column(JSONB)
    
    # Relations
    replies = relationship("AgentCommunication", backref="parent", remote_side=[id])
    
    # Index pour performance
    __table_args__ = (
        Index('idx_agent_comm_from_to_created', 'from_agent', 'to_agent', 'created_at'),
        Index('idx_agent_comm_status_priority', 'status', 'priority'),
        Index('idx_agent_comm_conversation', 'conversation_id', 'created_at'),
        Index('idx_agent_comm_session_type', 'session_id', 'message_type'),
    )

class AgentMetrics(Base):
    """Table des mtriques d'agents - Enterprise optimized"""
    __tablename__ = "agent_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(String(255), nullable=False, index=True)
    agent_type = Column(String(100), index=True)  # supervisor, worker, specialist
    metric_name = Column(String(255), nullable=False, index=True)
    metric_category = Column(String(100), index=True)  # performance, quality, cost, usage
    metric_value = Column(JSONB, nullable=False)  # Flexible pour diffrents types
    numeric_value = Column(Float)  # Pour requtes numriques rapides
    unit = Column(String(50))  # ms, count, mb, tokens, etc.
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    session_id = Column(String(255), index=True)
    task_id = Column(String(255), index=True)
    duration_ms = Column(Integer)  # Dure de la mtrique si applicable
    status = Column(String(50), default="active")  # active, archived, error
    session_metadata = Column(JSONB)
    
    # Index pour performance et analytics
    __table_args__ = (
        Index('idx_agent_metrics_agent_name_time', 'agent_id', 'metric_name', 'timestamp'),
        Index('idx_agent_metrics_category_time', 'metric_category', 'timestamp'),
        Index('idx_agent_metrics_session_task', 'session_id', 'task_id'),
        Index('idx_agent_metrics_numeric_value', 'metric_name', 'numeric_value'),
        Index('idx_agent_metrics_type_status', 'agent_type', 'status'),
    )

class KnowledgeBase(Base):
    """Table de la base de connaissances - Enterprise optimized"""
    __tablename__ = "knowledge_base"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), unique=True, index=True)  # Pour viter les doublons
    summary = Column(Text)  # Rsum pour recherche rapide
    category = Column(String(100), index=True)  # documentation, best_practice, pattern, architecture, etc.
    subcategory = Column(String(100), index=True)  # Plus de granularit
    tags = Column(JSONB)  # Liste de tags pour recherche
    source = Column(String(255), index=True)  # Source du document
    author = Column(String(255))  # Auteur/Agent crateur
    language = Column(String(10), default="fr", index=True)  # Langue du contenu
    confidence_score = Column(Integer, default=5, index=True)  # 1-10
    quality_score = Column(Float, default=5.0)  # Score de qualit plus prcis
    usage_count = Column(Integer, default=0)  # Nombre d'utilisations
    last_accessed = Column(DateTime(timezone=True))
    is_verified = Column(Boolean, default=False, index=True)  # Contenu vrifi
    is_public = Column(Boolean, default=True, index=True)  # Visibilit
    version = Column(String(20), default="1.0")
    embeddings_vector = Column(JSONB)  # Vecteurs pour recherche smantique
    related_documents = Column(JSONB)  # IDs de documents lis
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    session_metadata = Column(JSONB)
    
    # Index pour recherche et performance
    __table_args__ = (
        Index('idx_knowledge_category_score', 'category', 'confidence_score'),
        Index('idx_knowledge_source_verified', 'source', 'is_verified'),
        Index('idx_knowledge_tags_gin', 'tags', postgresql_using='gin'),  # Index GIN pour JSONB
        Index('idx_knowledge_public_category', 'is_public', 'category'),
        Index('idx_knowledge_quality_usage', 'quality_score', 'usage_count'),
        Index('idx_knowledge_title_trgm', 'title', postgresql_using='gin', postgresql_ops={'title': 'gin_trgm_ops'}),  # Full-text search
    )




