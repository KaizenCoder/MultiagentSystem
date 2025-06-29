# Database Session Management
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
import logging

logger = logging.getLogger(__name__)

# Configuration PostgreSQL pour NextGeneration
def get_database_url():
    """Construit l'URL de la base de données"""
    # Variables d'environnement pour PostgreSQL
    postgres_user = os.getenv("POSTGRES_USER", "postgres")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")
    postgres_host = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    postgres_db = os.getenv("POSTGRES_DB", "agent_memory")
    
    # URL PostgreSQL
    postgresql_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
    
    # Fallback SQLite pour développement
    fallback_url = "sqlite:///./memory.db"
    
    # Priorité : DATABASE_URL > PostgreSQL > SQLite
    database_url = os.getenv("DATABASE_URL", postgresql_url)
    
    logger.info(f"Database URL configured: {database_url.split('@')[0]}@***")
    return database_url

DATABASE_URL = get_database_url()

# Configuration moteur selon le type de base avec optimisations enterprise
if DATABASE_URL.startswith("postgresql"):
    # Configuration PostgreSQL enterprise-grade
    engine = create_engine(
        DATABASE_URL,
        # Pool settings pour haute charge
        pool_size=25,               # Connexions permanentes
        max_overflow=50,            # Connexions supplémentaires en pic
        pool_pre_ping=True,         # Test connexions avant usage
        pool_recycle=7200,          # Renouveler connexions toutes les 2h
        
        # Performance settings
        echo=False,                 # SQL logging (True pour debug)
        echo_pool=False,           # Pool logging
        
        # Connection args pour PostgreSQL
        connect_args={
            "application_name": "NextGeneration_MemoryAPI",
            "options": "-c default_transaction_isolation=read_committed -c timezone=UTC",
            "connect_timeout": 10,
            "command_timeout": 30,
        },
        
        # Execution options
        execution_options={
            "isolation_level": "READ_COMMITTED",
            "autocommit": False
        }
    )
    
    logger.info("✅ PostgreSQL engine configured for enterprise production")
else:
    # Configuration SQLite pour développement
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
        echo=False,
        connect_args={"timeout": 20}
    )
    
    logger.info("⚠️  SQLite engine configured for development only")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Générateur de session de base de données avec gestion d'erreurs avancée"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

async def get_async_db():
    """Version async du générateur de session (pour future implémentation)"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Async database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def test_connection():
    """Test de connexion à la base de données avec diagnostics avancés"""
    try:
        db = SessionLocal()
        
        # Test de base
        result = db.execute("SELECT 1 as test_value")
        test_value = result.scalar()
        
        if test_value != 1:
            raise Exception("Basic query test failed")
            
        # Test PostgreSQL spécifique si applicable
        if DATABASE_URL.startswith("postgresql"):
            # Test version PostgreSQL
            version_result = db.execute("SELECT version()")
            pg_version = version_result.scalar()
            logger.info(f"PostgreSQL version: {pg_version.split(' ')[1]}")
            
            # Test extensions disponibles
            extensions_result = db.execute("SELECT extname FROM pg_extension ORDER BY extname")
            extensions = [row[0] for row in extensions_result]
            logger.info(f"Available extensions: {', '.join(extensions)}")
            
            # Test performance
            import time
            start_time = time.time()
            db.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
            query_time = (time.time() - start_time) * 1000
            logger.info(f"Query performance: {query_time:.2f}ms")
        
        db.close()
        logger.info("✅ Database connection successful with full diagnostics")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        try:
            db.close()
        except:
            pass
        return False

def get_database_stats():
    """Statistiques de la base de données pour monitoring"""
    try:
        db = SessionLocal()
        stats = {}
        
        if DATABASE_URL.startswith("postgresql"):
            # Stats PostgreSQL
            stats_query = """
            SELECT 
                schemaname,
                tablename,
                n_tup_ins as inserts,
                n_tup_upd as updates,
                n_tup_del as deletes,
                n_live_tup as live_tuples,
                n_dead_tup as dead_tuples
            FROM pg_stat_user_tables 
            ORDER BY n_live_tup DESC
            """
            
            result = db.execute(stats_query)
            table_stats = []
            for row in result:
                table_stats.append({
                    "schema": row[0],
                    "table": row[1], 
                    "inserts": row[2],
                    "updates": row[3],
                    "deletes": row[4],
                    "live_tuples": row[5],
                    "dead_tuples": row[6]
                })
            
            stats["table_statistics"] = table_stats
            
            # Connection stats
            conn_query = "SELECT count(*) as active_connections FROM pg_stat_activity WHERE state = 'active'"
            conn_result = db.execute(conn_query)
            stats["active_connections"] = conn_result.scalar()
            
        db.close()
        return stats
        
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return {}