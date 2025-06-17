#!/usr/bin/env python3
"""
Script d'initialisation de la base PostgreSQL NextGeneration
Crée les tables et données de base nécessaires
"""
import asyncio
import logging
from sqlalchemy import text
from app.db.session import engine, SessionLocal, test_connection
from app.db.models import Base, AgentSession, MemoryItem, StateItem, AgentCommunication, AgentMetrics, KnowledgeBase
import sys
import os

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Crée toutes les tables dans la base de données"""
    try:
        logger.info("🔧 Création des tables PostgreSQL...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables créées avec succès")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur création tables: {e}")
        return False

def create_indexes():
    """Crée les index de performance avancés"""
    try:
        db = SessionLocal()
        logger.info("🔧 Création des index de performance avancés...")
        
        # Extensions PostgreSQL nécessaires
        extensions = [
            "CREATE EXTENSION IF NOT EXISTS pg_trgm",  # Pour recherche full-text
            "CREATE EXTENSION IF NOT EXISTS btree_gin",  # Pour index composites
            "CREATE EXTENSION IF NOT EXISTS pg_stat_statements",  # Pour monitoring
        ]
        
        # Index de performance spécialisés (sans CONCURRENTLY pour init)
        performance_indexes = [
            # Memory Items - Recherche et performance
            "CREATE INDEX IF NOT EXISTS idx_memory_content_hash ON memory_items(content_hash)",
            "CREATE INDEX IF NOT EXISTS idx_memory_category_importance ON memory_items(category, importance_score DESC)",
            "CREATE INDEX IF NOT EXISTS idx_memory_access_pattern ON memory_items(accessed_at DESC, access_count DESC)",
            
            # Agent Sessions - Monitoring et administration
            "CREATE INDEX IF NOT EXISTS idx_session_type_status ON agent_sessions(agent_type, status, created_at)",
            "CREATE INDEX IF NOT EXISTS idx_session_activity ON agent_sessions(last_activity DESC) WHERE is_active = true",
            "CREATE INDEX IF NOT EXISTS idx_session_cost_tracking ON agent_sessions(total_cost DESC, total_tokens_used DESC)",
            
            # State Items - Gestion d'état performante
            "CREATE INDEX IF NOT EXISTS idx_state_namespace_ttl ON state_items(namespace, ttl_expires_at) WHERE ttl_expires_at IS NOT NULL",
            "CREATE INDEX IF NOT EXISTS idx_state_version_tracking ON state_items(key, version DESC)",
            
            # Agent Communications - Routing et performance
            "CREATE INDEX IF NOT EXISTS idx_comm_routing ON agent_communications(to_agent, status, priority, created_at)",
            "CREATE INDEX IF NOT EXISTS idx_comm_performance ON agent_communications(response_time_ms DESC) WHERE response_time_ms IS NOT NULL",
            "CREATE INDEX IF NOT EXISTS idx_comm_retry_management ON agent_communications(retry_count, status) WHERE retry_count > 0",
            
            # Agent Metrics - Analytics et reporting
            "CREATE INDEX IF NOT EXISTS idx_metrics_analytics ON agent_metrics(metric_category, timestamp DESC, numeric_value)",
            "CREATE INDEX IF NOT EXISTS idx_metrics_performance_tracking ON agent_metrics(agent_type, metric_name, timestamp DESC)",
            
            # Knowledge Base - Recherche sémantique et qualité
            "CREATE INDEX IF NOT EXISTS idx_knowledge_quality ON knowledge_base(quality_score DESC, usage_count DESC)",
            "CREATE INDEX IF NOT EXISTS idx_knowledge_verification ON knowledge_base(is_verified, is_public, category)",
            "CREATE INDEX IF NOT EXISTS idx_knowledge_content_search ON knowledge_base USING gin(to_tsvector('french', title || ' ' || coalesce(summary, '')))",
        ]
        
        # Création des extensions d'abord
        for ext_sql in extensions:
            try:
                db.execute(text(ext_sql))
                db.commit()
                logger.info(f"✅ Extension activée: {ext_sql.split('IF NOT EXISTS ')[1]}")
            except Exception as e:
                logger.warning(f"⚠️  Extension ignorée: {e}")
                db.rollback()
        
        # Création des index de performance
        for index_sql in performance_indexes:
            try:
                db.execute(text(index_sql))
                db.commit()
                index_name = index_sql.split('idx_')[1].split(' ')[0] if 'idx_' in index_sql else "custom_index"
                logger.info(f"✅ Index créé: {index_name}")
            except Exception as e:
                logger.warning(f"⚠️  Index ignoré: {e}")
                db.rollback()
        
        db.close()
        logger.info("✅ Index de performance avancés créés")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur création index: {e}")
        return False

def insert_initial_data():
    """Insert les données initiales nécessaires"""
    try:
        db = SessionLocal()
        logger.info("🔧 Insertion des données initiales...")
        
        # Données de base enterprise pour le système NextGeneration
        import hashlib
        
        initial_knowledge = [
            {
                "title": "Architecture NextGeneration Multi-Agent Enterprise",
                "content": "Le système NextGeneration utilise une architecture multi-agent avancée avec IA-1 (Tests & Qualité) et IA-2 (Architecture & Production). Communication via journaux structurés, Memory API PostgreSQL centralisée, et orchestration LangGraph avec superviseur intelligent.",
                "summary": "Architecture multi-agent enterprise avec IA-1, IA-2, PostgreSQL et LangGraph",
                "category": "architecture",
                "subcategory": "system_design",
                "tags": ["multi-agent", "ia-1", "ia-2", "orchestrateur", "enterprise", "postgresql"],
                "source": "NextGeneration Documentation",
                "author": "System",
                "language": "fr",
                "confidence_score": 10,
                "quality_score": 9.5,
                "is_verified": True,
                "is_public": True,
                "version": "2.0"
            },
            {
                "title": "Standards Communication Inter-Agents Enterprise",
                "content": "Format standardisé: PHASE4-[IA]-[SPRINT]-[TÂCHE]-[SOUS-TÂCHE]. Messages critiques avec réponse < 2h. Journal quotidien obligatoire avec références croisées. Support PostgreSQL pour persistance et recherche avancée.",
                "summary": "Protocoles de communication standardisés pour agents IA",
                "category": "communication",
                "subcategory": "protocols",
                "tags": ["standards", "journaux", "communication", "persistance", "recherche"],
                "source": "Communication Guidelines v2.0",
                "author": "IA-1",
                "confidence_score": 10,
                "quality_score": 10.0,
                "is_verified": True,
                "version": "2.1"
            },
            {
                "title": "Configuration GPU RTX 3090 Ollama Production",
                "content": "Modèles recommandés: Mixtral-8x7B (26GB), Qwen-Coder-32B (19GB), Llama3:8B (6.6GB), Nous-Hermes-2 (4.1GB). Configuration CUDA_VISIBLE_DEVICES=1 pour RTX 3090. Optimisations mémoire et performance pour production.",
                "summary": "Configuration optimale RTX 3090 pour modèles LLM en production",
                "category": "configuration",
                "subcategory": "hardware",
                "tags": ["gpu", "rtx3090", "ollama", "modeles", "production", "performance"],
                "source": "Hardware Configuration Guide",
                "author": "IA-2",
                "confidence_score": 9,
                "quality_score": 9.0,
                "is_verified": True,
                "version": "1.5"
            },
            {
                "title": "PostgreSQL Enterprise Configuration NextGeneration",
                "content": "Configuration PostgreSQL 16 optimisée: 200 connexions max, shared_buffers 256MB, effective_cache_size 1GB. Index GIN pour JSONB, pg_trgm pour full-text. Modèles SQLAlchemy avec relations CASCADE et contraintes enterprise.",
                "summary": "Configuration PostgreSQL optimisée pour système multi-agent",
                "category": "database",
                "subcategory": "postgresql",
                "tags": ["postgresql", "optimisation", "enterprise", "sqlalchemy", "index", "performance"],
                "source": "Database Architecture Guide",
                "author": "IA-2",
                "confidence_score": 10,
                "quality_score": 9.8,
                "is_verified": True,
                "version": "1.0"
            },
            {
                "title": "Agents Spécialisés NextGeneration Roadmap",
                "content": "8 agents spécialisés proposés: DocumentationAgent, CodeReviewAgent, ArchitectureAgent, SecurityAgent, PerformanceAgent, TestingAgent, DeploymentAgent, AnalyticsAgent. Intégration supervisor avec coordination avancée et Memory API PostgreSQL.",
                "summary": "Roadmap agents spécialisés pour extension système multi-agent",
                "category": "roadmap",
                "subcategory": "agents",
                "tags": ["agents", "specialises", "roadmap", "documentation", "security", "performance"],
                "source": "Agent Specialization Plan",
                "author": "Claude",
                "confidence_score": 8,
                "quality_score": 8.5,
                "is_verified": False,
                "version": "1.0"
            }
        ]
        
        # Calcul automatique des hash pour éviter les doublons
        for kb_data in initial_knowledge:
            content_to_hash = f"{kb_data['title']}{kb_data['content']}"
            kb_data['content_hash'] = hashlib.sha256(content_to_hash.encode()).hexdigest()
        
        for kb_data in initial_knowledge:
            kb_item = KnowledgeBase(**kb_data)
            db.add(kb_item)
        
        db.commit()
        db.close()
        logger.info("✅ Données initiales insérées")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur insertion données: {e}")
        return False

def verify_installation():
    """Vérifie que l'installation est correcte"""
    try:
        db = SessionLocal()
        logger.info("🔧 Vérification de l'installation...")
        
        # Test de comptage des tables
        tables_count = {
            "agent_sessions": db.query(AgentSession).count(),
            "memory_items": db.query(MemoryItem).count(),
            "state_items": db.query(StateItem).count(),
            "agent_communications": db.query(AgentCommunication).count(),
            "agent_metrics": db.query(AgentMetrics).count(),
            "knowledge_base": db.query(KnowledgeBase).count(),
        }
        
        logger.info("📊 État des tables:")
        for table, count in tables_count.items():
            logger.info(f"   {table}: {count} enregistrements")
        
        db.close()
        logger.info("✅ Installation vérifiée avec succès")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur vérification: {e}")
        return False

def main():
    """Fonction principale d'initialisation"""
    logger.info("🚀 INITIALISATION POSTGRESQL NEXTGENERATION")
    logger.info("=" * 50)
    
    # 1. Test de connexion
    if not test_connection():
        logger.error("❌ Connexion à PostgreSQL échouée")
        logger.info("💡 Vérifiez que PostgreSQL est démarré (docker-compose up postgres)")
        sys.exit(1)
    
    # 2. Création des tables
    if not create_tables():
        logger.error("❌ Création des tables échouée")
        sys.exit(1)
    
    # 3. Création des index
    if not create_indexes():
        logger.warning("⚠️  Certains index n'ont pas pu être créés")
    
    # 4. Insertion des données initiales
    if not insert_initial_data():
        logger.warning("⚠️  Insertion des données initiales échouée")
    
    # 5. Vérification
    if not verify_installation():
        logger.error("❌ Vérification finale échouée")
        sys.exit(1)
    
    logger.info("🎉 INITIALISATION POSTGRESQL TERMINÉE AVEC SUCCÈS!")
    logger.info("💡 La Memory API est prête à utiliser PostgreSQL")

if __name__ == "__main__":
    main()
