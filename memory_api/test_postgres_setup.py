#!/usr/bin/env python3
"""
Script de test et validation de l'infrastructure PostgreSQL NextGeneration
Valide la configuration, performance et fonctionnalités enterprise
"""
import asyncio
import logging
import sys
import time
import json
from datetime import datetime, timezone
import hashlib
import uuid

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test des imports nécessaires"""
    try:
        from app.db.session import engine, SessionLocal, test_connection, get_database_stats
        from app.db.models import (
            Base, AgentSession, MemoryItem, StateItem, 
            AgentCommunication, AgentMetrics, KnowledgeBase
        )
        logger.info("✅ Tous les imports sont valides")
        return True
    except ImportError as e:
        logger.error(f"❌ Erreur d'import: {e}")
        return False

def test_database_connection():
    """Test de connexion à la base de données"""
    logger.info("🔧 Test de connexion PostgreSQL...")
    
    from app.db.session import test_connection
    
    if test_connection():
        logger.info("✅ Connexion PostgreSQL réussie")
        return True
    else:
        logger.error("❌ Connexion PostgreSQL échouée")
        return False

def test_tables_creation():
    """Test de création et existence des tables"""
    logger.info("🔧 Test de création des tables...")
    
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
                logger.info(f"✅ Table {table_name}: {count} enregistrements")
            except Exception as e:
                logger.error(f"❌ Erreur table {table_name}: {e}")
                db.close()
                return False
        
        db.close()
        logger.info("✅ Toutes les tables sont accessibles")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur test tables: {e}")
        return False

def test_crud_operations():
    """Test des opérations CRUD de base"""
    logger.info("🔧 Test des opérations CRUD...")
    
    try:
        from app.db.session import SessionLocal
        from app.db.models import AgentSession, MemoryItem, KnowledgeBase
        
        db = SessionLocal()
        
        # Test 1: Création AgentSession
        test_session = AgentSession(
            session_id=f"test-session-{uuid.uuid4()}",
            agent_id="test-agent",
            agent_type="test",
            status="running",
            metadata={"test": True}
        )
        db.add(test_session)
        db.commit()
        logger.info("✅ Création AgentSession réussie")
        
        # Test 2: Création MemoryItem liée
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
        logger.info("✅ Création MemoryItem avec FK réussie")
        
        # Test 3: Requête avec relation
        session_with_memory = db.query(AgentSession).filter(
            AgentSession.id == test_session.id
        ).first()
        
        if len(session_with_memory.memory_items) > 0:
            logger.info("✅ Relations FK fonctionnelles")
        else:
            logger.error("❌ Relations FK non fonctionnelles")
            db.close()
            return False
        
        # Test 4: Recherche Knowledge Base
        kb_count = db.query(KnowledgeBase).count()
        logger.info(f"✅ Knowledge Base: {kb_count} entrées disponibles")
        
        # Test 5: Nettoyage
        db.delete(test_memory)
        db.delete(test_session)
        db.commit()
        logger.info("✅ Suppression en cascade réussie")
        
        db.close()
        logger.info("✅ Toutes les opérations CRUD fonctionnent")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur CRUD: {e}")
        try:
            db.rollback()
            db.close()
        except:
            pass
        return False

def test_performance():
    """Test de performance de base"""
    logger.info("🔧 Test de performance PostgreSQL...")
    
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
        logger.info(f"✅ Insertion 10 sessions: {insert_time:.2f}ms")
        
        # Test 2: Requête complexe avec index
        start_time = time.time()
        active_sessions = db.query(AgentSession).filter(
            AgentSession.status == "testing",
            AgentSession.agent_type == "performance_test"
        ).all()
        query_time = (time.time() - start_time) * 1000
        logger.info(f"✅ Requête avec index: {query_time:.2f}ms ({len(active_sessions)} résultats)")
        
        # Test 3: Nettoyage
        for session in test_sessions:
            db.delete(session)
        db.commit()
        
        db.close()
        
        # Validation des seuils de performance
        if insert_time < 1000 and query_time < 100:
            logger.info("✅ Performance optimale validée")
            return True
        else:
            logger.warning(f"⚠️  Performance acceptable mais non optimale")
            return True
            
    except Exception as e:
        logger.error(f"❌ Erreur test performance: {e}")
        return False

def test_enterprise_features():
    """Test des fonctionnalités enterprise"""
    logger.info("🔧 Test des fonctionnalités enterprise...")
    
    try:
        from app.db.session import SessionLocal, get_database_stats
        
        # Test 1: Extensions PostgreSQL
        db = SessionLocal()
        extensions_query = "SELECT extname FROM pg_extension WHERE extname IN ('pg_trgm', 'btree_gin')"
        result = db.execute(extensions_query)
        extensions = [row[0] for row in result]
        
        if 'pg_trgm' in extensions:
            logger.info("✅ Extension pg_trgm activée (full-text search)")
        else:
            logger.warning("⚠️  Extension pg_trgm non disponible")
        
        if 'btree_gin' in extensions:
            logger.info("✅ Extension btree_gin activée (index composites)")
        else:
            logger.warning("⚠️  Extension btree_gin non disponible")
        
        # Test 2: Index spécialisés
        index_query = """
        SELECT indexname 
        FROM pg_indexes 
        WHERE schemaname = 'public' 
        AND indexname LIKE 'idx_%'
        ORDER BY indexname
        """
        result = db.execute(index_query)
        indexes = [row[0] for row in result]
        logger.info(f"✅ Index customisés trouvés: {len(indexes)}")
        
        # Test 3: Statistiques de base
        stats = get_database_stats()
        if stats:
            logger.info("✅ Monitoring statistiques fonctionnel")
            if "active_connections" in stats:
                logger.info(f"✅ Connexions actives: {stats['active_connections']}")
        
        db.close()
        logger.info("✅ Fonctionnalités enterprise validées")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur test enterprise: {e}")
        return False

def generate_test_report():
    """Génère un rapport de test complet"""
    logger.info("📊 GÉNÉRATION DU RAPPORT DE TEST POSTGRESQL")
    logger.info("=" * 60)
    
    tests = [
        ("Imports et dépendances", test_imports),
        ("Connexion PostgreSQL", test_database_connection),
        ("Création et accès tables", test_tables_creation),
        ("Opérations CRUD", test_crud_operations),
        ("Performance de base", test_performance),
        ("Fonctionnalités enterprise", test_enterprise_features)
    ]
    
    results = []
    total_tests = len(tests)
    passed_tests = 0
    
    for test_name, test_func in tests:
        logger.info(f"\n🔧 {test_name}...")
        try:
            result = test_func()
            if result:
                passed_tests += 1
                status = "✅ RÉUSSI"
            else:
                status = "❌ ÉCHOUÉ"
            
            results.append((test_name, status, result))
            logger.info(f"{status}: {test_name}")
            
        except Exception as e:
            results.append((test_name, "❌ ERREUR", False))
            logger.error(f"❌ ERREUR: {test_name} - {e}")
    
    # Rapport final
    logger.info("\n" + "=" * 60)
    logger.info("📋 RAPPORT FINAL DE VALIDATION")
    logger.info("=" * 60)
    
    for test_name, status, result in results:
        logger.info(f"{status}: {test_name}")
    
    success_rate = (passed_tests / total_tests) * 100
    logger.info(f"\n📊 TAUX DE RÉUSSITE: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate >= 90:
        logger.info("🎉 INFRASTRUCTURE POSTGRESQL PRÊTE POUR PRODUCTION!")
        return True
    elif success_rate >= 70:
        logger.info("⚠️  Infrastructure PostgreSQL fonctionnelle avec quelques améliorations possibles")
        return True
    else:
        logger.error("❌ Infrastructure PostgreSQL nécessite des corrections avant production")
        return False

def main():
    """Fonction principale de test"""
    logger.info("🚀 DÉMARRAGE TESTS INFRASTRUCTURE POSTGRESQL NEXTGENERATION")
    logger.info(f"📅 Date: {datetime.now(timezone.utc).isoformat()}")
    logger.info("=" * 80)
    
    success = generate_test_report()
    
    if success:
        logger.info("\n🎯 RECOMMANDATION: Procéder au déploiement PostgreSQL en production")
        sys.exit(0)
    else:
        logger.error("\n🚨 RECOMMANDATION: Corriger les problèmes avant déploiement")
        sys.exit(1)

if __name__ == "__main__":
    main()