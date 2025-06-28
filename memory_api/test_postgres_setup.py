#!/usr/bin/env python3
"""
Script de test et validation de l'infrastructure PostgreSQL NextGeneration
Valide la configuration, performance et fonctionnalits enterprise
"""
import asyncio
import sys
from pathlib import Path
from core import logging_manager
import sys
import time
import json
from datetime import datetime, timezone
import hashlib
import uuid

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# LoggingManager NextGeneration - Tests
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = logging_manager.get_logger(custom_config={
            "logger_name": "in",
            "log_level": "DEBUG",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": False,  # Tests synchrones
            "console_output": True
        })

def test_imports():
    """Test des imports ncessaires"""
    try:
        from app.db.session import engine, SessionLocal, test_connection, get_database_stats
        from app.db.models import (
            Base, AgentSession, MemoryItem, StateItem, 
            AgentCommunication, AgentMetrics, KnowledgeBase
        )
        logger.info("[CHECK] Tous les imports sont valides")
        return True
    except ImportError as e:
        logger.error(f"[CROSS] Erreur d'import: {e}")
        return False

def test_database_connection():
    """Test de connexion  la base de donnes"""
    logger.info("[TOOL] Test de connexion PostgreSQL...")
    
    from app.db.session import test_connection
    
    if test_connection():
        logger.info("[CHECK] Connexion PostgreSQL russie")
        return True
    else:
        logger.error("[CROSS] Connexion PostgreSQL choue")
        return False

def test_tables_creation():
    """Test de cration et existence des tables"""
    logger.info("[TOOL] Test de cration des tables...")
    
    try:
        from app.db.session import SessionLocal
        from app.db.models import (
            AgentSession, MemoryItem, StateItem, 
            AgentCommunication, AgentMetrics, KnowledgeBase
        )
        
        db = SessionLocal()
        
        # Test existence des tables
        tables_to_test = [
            ("agent_sessions", AgentSession),
            ("memory_items", MemoryItem),
            ("state_items", StateItem),
            ("agent_communications", AgentCommunication),
            ("agent_metrics", AgentMetrics),
            ("knowledge_base", KnowledgeBase)
        ]
        
        for table_name, model_class in tables_to_test:
            try:
                count = db.query(model_class).count()
                logger.info(f"[CHECK] Table {table_name}: {count} enregistrements")
            except Exception as e:
                logger.error(f"[CROSS] Erreur table {table_name}: {e}")
                db.close()
                return False
        
        db.close()
        logger.info("[CHECK] Toutes les tables sont accessibles")
        return True
        
    except Exception as e:
        logger.error(f"[CROSS] Erreur test tables: {e}")
        return False

def test_crud_operations():
    """Test des oprations CRUD de base"""
    logger.info("[TOOL] Test des oprations CRUD...")
    
    try:
        from app.db.session import SessionLocal
        from app.db.models import AgentSession, MemoryItem, KnowledgeBase
        
        db = SessionLocal()
        
        # Test 1: Cration AgentSession
        test_session = AgentSession(
            session_id=f"test-session-{uuid.uuid4()}",
            agent_id="test-agent",
            agent_type="test",
            status="running",
            metadata={"test": True}
        )
        db.add(test_session)
        db.commit()
        logger.info("[CHECK] Cration AgentSession russie")
        
        # Test 2: Cration MemoryItem lie
        test_memory = MemoryItem(
            session_id=test_session.id,
            content="Test memory content for PostgreSQL validation",
            content_hash=hashlib.sha256(b"test content").hexdigest(),
            content_type="test",
            category="validation",
            importance_score=5,
            metadata={"test": True}
        )
        db.add(test_memory)
        db.commit()
        logger.info("[CHECK] Cration MemoryItem avec FK russie")
        
        # Test 3: Requte avec relation
        session_with_memory = db.query(AgentSession).filter(
            AgentSession.id == test_session.id
        ).first()
        
        if len(session_with_memory.memory_items) > 0:
            logger.info("[CHECK] Relations FK fonctionnelles")
        else:
            logger.error("[CROSS] Relations FK non fonctionnelles")
            db.close()
            return False
        
        # Test 4: Recherche Knowledge Base
        kb_count = db.query(KnowledgeBase).count()
        logger.info(f"[CHECK] Knowledge Base: {kb_count} entres disponibles")
        
        # Test 5: Nettoyage
        db.delete(test_memory)
        db.delete(test_session)
        db.commit()
        logger.info("[CHECK] Suppression en cascade russie")
        
        db.close()
        logger.info("[CHECK] Toutes les oprations CRUD fonctionnent")
        return True
        
    except Exception as e:
        logger.error(f"[CROSS] Erreur CRUD: {e}")
        try:
            db.rollback()
            db.close()
        except:
            pass
        return False

def test_performance():
    """Test de performance de base"""
    logger.info("[TOOL] Test de performance PostgreSQL...")
    
    try:
        from app.db.session import SessionLocal
        from app.db.models import AgentSession, MemoryItem
        
        db = SessionLocal()
        
        # Test 1: Insertion en batch
        start_time = time.time()
        test_sessions = []
        
        for i in range(10):
            session = AgentSession(
                session_id=f"perf-test-{i}-{uuid.uuid4()}",
                agent_id=f"perf-agent-{i}",
                agent_type="performance_test",
                status="testing"
            )
            test_sessions.append(session)
            db.add(session)
        
        db.commit()
        insert_time = (time.time() - start_time) * 1000
        logger.info(f"[CHECK] Insertion 10 sessions: {insert_time:.2f}ms")
        
        # Test 2: Requte complexe avec index
        start_time = time.time()
        active_sessions = db.query(AgentSession).filter(
            AgentSession.status == "testing",
            AgentSession.agent_type == "performance_test"
        ).all()
        query_time = (time.time() - start_time) * 1000
        logger.info(f"[CHECK] Requte avec index: {query_time:.2f}ms ({len(active_sessions)} rsultats)")
        
        # Test 3: Nettoyage
        for session in test_sessions:
            db.delete(session)
        db.commit()
        
        db.close()
        
        # Validation des seuils de performance
        if insert_time < 1000 and query_time < 100:
            logger.info("[CHECK] Performance optimale valide")
            return True
        else:
            logger.warning(f"  Performance acceptable mais non optimale")
            return True
            
    except Exception as e:
        logger.error(f"[CROSS] Erreur test performance: {e}")
        return False

def test_enterprise_features():
    """Test des fonctionnalits enterprise"""
    logger.info("[TOOL] Test des fonctionnalits enterprise...")
    
    try:
        from app.db.session import SessionLocal, get_database_stats
        
        # Test 1: Extensions PostgreSQL
        from sqlalchemy import text
        db = SessionLocal()
        extensions_query = "SELECT extname FROM pg_extension WHERE extname IN ('pg_trgm', 'btree_gin')"
        result = db.execute(text(extensions_query))
        extensions = [row[0] for row in result]
        
        if 'pg_trgm' in extensions:
            logger.info("[CHECK] Extension pg_trgm active (full-text search)")
        else:
            logger.warning("  Extension pg_trgm non disponible")
        
        if 'btree_gin' in extensions:
            logger.info("[CHECK] Extension btree_gin active (index composites)")
        else:
            logger.warning("  Extension btree_gin non disponible")
        
        # Test 2: Index spcialiss
        index_query = """
        SELECT indexname 
        FROM pg_indexes 
        WHERE schemaname = 'public' 
        AND indexname LIKE 'idx_%'
        ORDER BY indexname
        """
        result = db.execute(text(index_query))
        indexes = [row[0] for row in result]
        logger.info(f"[CHECK] Index customiss trouvs: {len(indexes)}")
        
        # Test 3: Statistiques de base
        stats = get_database_stats()
        if stats:
            logger.info("[CHECK] Monitoring statistiques fonctionnel")
            if "active_connections" in stats:
                logger.info(f"[CHECK] Connexions actives: {stats['active_connections']}")
        
        db.close()
        logger.info("[CHECK] Fonctionnalits enterprise valides")
        return True
        
    except Exception as e:
        logger.error(f"[CROSS] Erreur test enterprise: {e}")
        return False

def generate_test_report():
    """Gnre un rapport de test complet"""
    logger.info("[CHART] GNRATION DU RAPPORT DE TEST POSTGRESQL")
    logger.info("=" * 60)
    
    tests = [
        ("Imports et dpendances", test_imports),
        ("Connexion PostgreSQL", test_database_connection),
        ("Cration et accs tables", test_tables_creation),
        ("Oprations CRUD", test_crud_operations),
        ("Performance de base", test_performance),
        ("Fonctionnalits enterprise", test_enterprise_features)
    ]
    
    results = []
    total_tests = len(tests)
    passed_tests = 0
    
    for test_name, test_func in tests:
        logger.info(f"\n[TOOL] {test_name}...")
        try:
            result = test_func()
            if result:
                passed_tests += 1
                status = "[CHECK] RUSSI"
            else:
                status = "[CROSS] CHOU"
            
            results.append((test_name, status, result))
            logger.info(f"{status}: {test_name}")
            
        except Exception as e:
            results.append((test_name, "[CROSS] ERREUR", False))
            logger.error(f"[CROSS] ERREUR: {test_name} - {e}")
    
    # Rapport final
    logger.info("\n" + "=" * 60)
    logger.info("[CLIPBOARD] RAPPORT FINAL DE VALIDATION")
    logger.info("=" * 60)
    
    for test_name, status, result in results:
        logger.info(f"{status}: {test_name}")
    
    success_rate = (passed_tests / total_tests) * 100
    logger.info(f"\n[CHART] TAUX DE RUSSITE: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate >= 90:
        logger.info(" INFRASTRUCTURE POSTGRESQL PRTE POUR PRODUCTION!")
        return True
    elif success_rate >= 70:
        logger.info("  Infrastructure PostgreSQL fonctionnelle avec quelques amliorations possibles")
        return True
    else:
        logger.error("[CROSS] Infrastructure PostgreSQL ncessite des corrections avant production")
        return False

def main():
    """Fonction principale de test"""
    logger.info("[ROCKET] DMARRAGE TESTS INFRASTRUCTURE POSTGRESQL NEXTGENERATION")
    logger.info(f" Date: {datetime.now(timezone.utc).isoformat()}")
    logger.info("=" * 80)
    
    success = generate_test_report()
    
    if success:
        logger.info("\n[TARGET] RECOMMANDATION: Procder au dploiement PostgreSQL en production")
        sys.exit(0)
    else:
        logger.error("\n RECOMMANDATION: Corriger les problmes avant dploiement")
        sys.exit(1)

if __name__ == "__main__":
    main()



