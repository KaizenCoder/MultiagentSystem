"""
Production Database Performance Optimizer
Handles PostgreSQL connection pooling, read replicas, backup automation, and performance tuning.
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum

import asyncpg
import psycopg2
from psycopg2 import pool
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from ..config import config
from ..observability.monitoring import monitoring_manager


logger = logging.getLogger(__name__)


class DatabaseRole(Enum):
    """Database role types"""
    PRIMARY = "primary"
    READ_REPLICA = "read_replica"
    ANALYTICS = "analytics"
    BACKUP = "backup"


class ConnectionType(Enum):
    """Connection pool types"""
    WRITE = "write"
    READ = "read"
    ANALYTICS = "analytics"


@dataclass
class DatabaseConfig:
    """Database connection configuration"""
    host: str
    port: int
    database: str
    username: str
    password: str
    role: DatabaseRole
    max_connections: int = 20
    min_connections: int = 5
    connection_timeout: int = 30
    command_timeout: int = 60
    ssl_mode: str = "require"
    application_name: str = "orchestrator"


@dataclass
class PerformanceMetrics:
    """Database performance metrics"""
    active_connections: int
    idle_connections: int
    total_connections: int
    avg_query_time: float
    slow_queries_count: int
    cache_hit_ratio: float
    buffer_hit_ratio: float
    index_usage_ratio: float
    table_bloat_ratio: float
    last_vacuum: Optional[datetime]
    last_analyze: Optional[datetime]


class PgBouncerManager:
    """Manages PgBouncer connection pooling"""
    
    def __init__(self, config_path: str = "/etc/pgbouncer/pgbouncer.ini"):
        self.config_path = config_path
        self.admin_user = getattr(config, "PGBOUNCER_ADMIN_USER", "postgres")
        self.admin_password = getattr(config, "PGBOUNCER_ADMIN_PASSWORD", None)
        self.listen_port = int(getattr(config, "PGBOUNCER_PORT", "6432"))
        
    async def generate_config(self, databases: List[DatabaseConfig]) -> str:
        """Generate PgBouncer configuration"""
        config_content = f"""
[databases]
"""
        
        for db in databases:
            pool_size = min(db.max_connections, 25) if db.role == DatabaseRole.PRIMARY else 10
            config_content += f"""
{db.database}_{db.role.value} = host={db.host} port={db.port} dbname={db.database} pool_size={pool_size}
"""
        
        config_content += f"""

[pgbouncer]
listen_port = {self.listen_port}
listen_addr = 0.0.0.0
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
admin_users = {self.admin_user}
stats_users = {self.admin_user}

# Pool settings
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 5

# Connection limits
max_db_connections = 50
max_user_connections = 50

# Timeouts
server_connect_timeout = 15
server_login_retry = 15
query_timeout = 900
query_wait_timeout = 120
client_idle_timeout = 0
server_idle_timeout = 600
server_lifetime = 3600
server_reset_query = DISCARD ALL

# Logging
log_connections = 1
log_disconnections = 1
log_pooler_errors = 1

# Security
ignore_startup_parameters = extra_float_digits

# Performance
application_name_add_host = 1
"""
        return config_content
    
    async def restart_pgbouncer(self) -> bool:
        """Restart PgBouncer service"""
        try:
            import subprocess
            result = subprocess.run(
                ["systemctl", "restart", "pgbouncer"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info("PgBouncer restarted successfully")
                return True
            else:
                logger.error(f"Failed to restart PgBouncer: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error restarting PgBouncer: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get PgBouncer statistics"""
        try:
            conn = await asyncpg.connect(
                host="localhost",
                port=self.listen_port,
                user=self.admin_user,
                password=self.admin_password,
                database="pgbouncer"
            )
            
            # Get pool stats
            pools = await conn.fetch("SHOW POOLS")
            stats = await conn.fetch("SHOW STATS")
            servers = await conn.fetch("SHOW SERVERS")
            
            await conn.close()
            
            return {
                "pools": [dict(row) for row in pools],
                "stats": [dict(row) for row in stats],
                "servers": [dict(row) for row in servers],
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error getting PgBouncer stats: {e}")
            return {}


class DatabaseConnectionManager:
    """Manages database connections with pooling and load balancing"""
    
    def __init__(self):
        self.primary_config: Optional[DatabaseConfig] = None
        self.read_replicas: List[DatabaseConfig] = []
        self.analytics_db: Optional[DatabaseConfig] = None
        
        self.connection_pools: Dict[str, Any] = {}
        self.async_engines: Dict[str, Any] = {}
        
        self.pgbouncer = PgBouncerManager()
        self.performance_metrics: Dict[str, PerformanceMetrics] = {}
        
        self._setup_from_config()
    
    def _setup_from_config(self):
        """Setup database configurations from environment"""
        # Primary database
        primary_host = getattr(config, "DB_PRIMARY_HOST", "localhost")
        primary_port = int(getattr(config, "DB_PRIMARY_PORT", "5432"))
        database = getattr(config, "DB_NAME", "orchestrator")
        username = getattr(config, "DB_USERNAME", "postgres")
        password = getattr(config, "DB_PASSWORD", None)
        
        self.primary_config = DatabaseConfig(
            host=primary_host,
            port=primary_port,
            database=database,
            username=username,
            password=password,
            role=DatabaseRole.PRIMARY,
            max_connections=int(getattr(config, "DB_MAX_CONNECTIONS", "20"))
        )
        
        # Read replicas
        replica_hosts = getattr(config, "DB_REPLICA_HOSTS", "").split(",")
        for i, host in enumerate(replica_hosts):
            if host.strip():
                replica_config = DatabaseConfig(
                    host=host.strip(),
                    port=primary_port,
                    database=database,
                    username=username,
                    password=password,
                    role=DatabaseRole.READ_REPLICA,
                    max_connections=int(getattr(config, "DB_REPLICA_MAX_CONNECTIONS", "15"))
                )
                self.read_replicas.append(replica_config)
        
        # Analytics database
        analytics_host = getattr(config, "DB_ANALYTICS_HOST", None)
        if analytics_host:
            self.analytics_db = DatabaseConfig(
                host=analytics_host,
                port=int(getattr(config, "DB_ANALYTICS_PORT", str(primary_port))),
                database=getattr(config, "DB_ANALYTICS_NAME", f"{database}_analytics"),
                username=username,
                password=password,
                role=DatabaseRole.ANALYTICS,
                max_connections=int(getattr(config, "DB_ANALYTICS_MAX_CONNECTIONS", "10"))
            )
    
    async def initialize(self):
        """Initialize all database connections"""
        try:
            # Initialize primary connection
            if self.primary_config:
                await self._create_connection_pool(self.primary_config, ConnectionType.WRITE)
            
            # Initialize read replicas
            for replica in self.read_replicas:
                await self._create_connection_pool(replica, ConnectionType.READ)
            
            # Initialize analytics database
            if self.analytics_db:
                await self._create_connection_pool(self.analytics_db, ConnectionType.ANALYTICS)
            
            # Setup PgBouncer
            await self._setup_pgbouncer()
            
            logger.info("Database connection manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database connections: {e}")
            raise
    
    async def _create_connection_pool(self, db_config: DatabaseConfig, conn_type: ConnectionType):
        """Create connection pool for a database"""
        pool_name = f"{db_config.role.value}_{conn_type.value}"
        
        # Async engine for SQLAlchemy
        database_url = f"postgresql+asyncpg://{db_config.username}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}"
        
        engine = create_async_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=db_config.max_connections,
            max_overflow=db_config.max_connections // 2,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={
                "server_settings": {
                    "application_name": db_config.application_name,
                    "jit": "off"  # Disable JIT for consistency
                }
            }
        )
        
        self.async_engines[pool_name] = engine
        
        # AsyncPG connection pool for direct queries
        pool = await asyncpg.create_pool(
            host=db_config.host,
            port=db_config.port,
            user=db_config.username,
            password=db_config.password,
            database=db_config.database,
            min_size=db_config.min_connections,
            max_size=db_config.max_connections,
            command_timeout=db_config.command_timeout,
            server_settings={
                "application_name": db_config.application_name
            }
        )
        
        self.connection_pools[pool_name] = pool
        
        logger.info(f"Created connection pool for {pool_name}")
    
    async def _setup_pgbouncer(self):
        """Setup PgBouncer configuration"""
        try:
            all_databases = []
            if self.primary_config:
                all_databases.append(self.primary_config)
            all_databases.extend(self.read_replicas)
            if self.analytics_db:
                all_databases.append(self.analytics_db)
            
            if all_databases:
                config_content = await self.pgbouncer.generate_config(all_databases)
                
                # Write configuration (in production, this would be mounted)
                with open("/tmp/pgbouncer.ini", "w") as f:
                    f.write(config_content)
                
                logger.info("PgBouncer configuration generated")
                
        except Exception as e:
            logger.error(f"Failed to setup PgBouncer: {e}")
    
    async def get_connection(self, connection_type: ConnectionType = ConnectionType.READ) -> asyncpg.Connection:
        """Get database connection based on type"""
        if connection_type == ConnectionType.WRITE:
            pool_name = f"{DatabaseRole.PRIMARY.value}_{ConnectionType.WRITE.value}"
        elif connection_type == ConnectionType.ANALYTICS:
            pool_name = f"{DatabaseRole.ANALYTICS.value}_{ConnectionType.ANALYTICS.value}"
        else:
            # Load balance across read replicas
            if self.read_replicas:
                replica = self.read_replicas[hash(time.time()) % len(self.read_replicas)]
                pool_name = f"{replica.role.value}_{ConnectionType.READ.value}"
            else:
                # Fallback to primary for reads
                pool_name = f"{DatabaseRole.PRIMARY.value}_{ConnectionType.WRITE.value}"
        
        pool = self.connection_pools.get(pool_name)
        if not pool:
            raise ValueError(f"No connection pool available for {pool_name}")
        
        return await pool.acquire()
    
    async def release_connection(self, connection: asyncpg.Connection, connection_type: ConnectionType = ConnectionType.READ):
        """Release database connection back to pool"""
        if connection_type == ConnectionType.WRITE:
            pool_name = f"{DatabaseRole.PRIMARY.value}_{ConnectionType.WRITE.value}"
        elif connection_type == ConnectionType.ANALYTICS:
            pool_name = f"{DatabaseRole.ANALYTICS.value}_{ConnectionType.ANALYTICS.value}"
        else:
            # Find the correct read replica pool
            if self.read_replicas:
                replica = self.read_replicas[0]  # Simplified for release
                pool_name = f"{replica.role.value}_{ConnectionType.READ.value}"
            else:
                pool_name = f"{DatabaseRole.PRIMARY.value}_{ConnectionType.WRITE.value}"
        
        pool = self.connection_pools.get(pool_name)
        if pool:
            await pool.release(connection)
    
    async def get_performance_metrics(self, database_role: DatabaseRole = DatabaseRole.PRIMARY) -> PerformanceMetrics:
        """Get performance metrics for a database"""
        pool_name = f"{database_role.value}_{'write' if database_role == DatabaseRole.PRIMARY else 'read'}"
        pool = self.connection_pools.get(pool_name)
        
        if not pool:
            raise ValueError(f"No connection pool for {database_role}")
        
        try:
            conn = await pool.acquire()
            
            # Get connection stats
            connection_stats = await conn.fetch("""
                SELECT 
                    count(*) as total_connections,
                    count(*) FILTER (WHERE state = 'active') as active_connections,
                    count(*) FILTER (WHERE state = 'idle') as idle_connections
                FROM pg_stat_activity 
                WHERE datname = current_database()
            """)
            
            # Get query performance
            query_stats = await conn.fetch("""
                SELECT 
                    avg(mean_exec_time) as avg_query_time,
                    sum(calls) FILTER (WHERE mean_exec_time > 1000) as slow_queries_count
                FROM pg_stat_statements 
                WHERE dbid = (SELECT oid FROM pg_database WHERE datname = current_database())
            """)
            
            # Get cache hit ratios
            cache_stats = await conn.fetch("""
                SELECT 
                    round(100.0 * sum(blks_hit) / (sum(blks_hit) + sum(blks_read)), 2) as buffer_hit_ratio
                FROM pg_stat_database 
                WHERE datname = current_database()
            """)
            
            # Get index usage
            index_stats = await conn.fetch("""
                SELECT 
                    round(100.0 * sum(idx_tup_read) / (sum(seq_tup_read) + sum(idx_tup_read)), 2) as index_usage_ratio
                FROM pg_stat_user_tables
            """)
            
            # Get last vacuum/analyze
            maintenance_stats = await conn.fetch("""
                SELECT 
                    max(last_vacuum) as last_vacuum,
                    max(last_analyze) as last_analyze
                FROM pg_stat_user_tables
            """)
            
            await pool.release(conn)
            
            # Build metrics
            conn_row = connection_stats[0] if connection_stats else {}
            query_row = query_stats[0] if query_stats else {}
            cache_row = cache_stats[0] if cache_stats else {}
            index_row = index_stats[0] if index_stats else {}
            maint_row = maintenance_stats[0] if maintenance_stats else {}
            
            metrics = PerformanceMetrics(
                active_connections=conn_row.get('active_connections', 0),
                idle_connections=conn_row.get('idle_connections', 0),
                total_connections=conn_row.get('total_connections', 0),
                avg_query_time=float(query_row.get('avg_query_time') or 0),
                slow_queries_count=query_row.get('slow_queries_count', 0),
                cache_hit_ratio=95.0,  # Default high value
                buffer_hit_ratio=float(cache_row.get('buffer_hit_ratio') or 95.0),
                index_usage_ratio=float(index_row.get('index_usage_ratio') or 90.0),
                table_bloat_ratio=5.0,  # Would need complex query
                last_vacuum=maint_row.get('last_vacuum'),
                last_analyze=maint_row.get('last_analyze')
            )
            
            self.performance_metrics[database_role.value] = metrics
            
            # Update monitoring metrics
            await monitoring_manager.record_metric(
                "database_active_connections", 
                metrics.active_connections,
                {"role": database_role.value}
            )
            await monitoring_manager.record_metric(
                "database_avg_query_time", 
                metrics.avg_query_time,
                {"role": database_role.value}
            )
            await monitoring_manager.record_metric(
                "database_buffer_hit_ratio", 
                metrics.buffer_hit_ratio,
                {"role": database_role.value}
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting performance metrics for {database_role}: {e}")
            raise
    
    async def optimize_database(self, database_role: DatabaseRole = DatabaseRole.PRIMARY) -> Dict[str, Any]:
        """Run database optimization commands"""
        pool_name = f"{database_role.value}_{'write' if database_role == DatabaseRole.PRIMARY else 'read'}"
        pool = self.connection_pools.get(pool_name)
        
        if not pool or database_role != DatabaseRole.PRIMARY:
            return {"error": "Can only optimize primary database"}
        
        try:
            conn = await pool.acquire()
            results = {}
            
            # Run VACUUM ANALYZE
            await conn.execute("VACUUM ANALYZE")
            results['vacuum_analyze'] = "completed"
            
            # Update statistics
            await conn.execute("ANALYZE")
            results['analyze'] = "completed"
            
            # Reindex if needed (only for small tables)
            small_tables = await conn.fetch("""
                SELECT schemaname, tablename 
                FROM pg_tables 
                WHERE schemaname = 'public' 
                AND pg_total_relation_size(schemaname||'.'||tablename) < 100000000
            """)
            
            for table in small_tables:
                await conn.execute(f"REINDEX TABLE {table['schemaname']}.{table['tablename']}")
            
            results['reindex_count'] = len(small_tables)
            
            await pool.release(conn)
            
            logger.info(f"Database optimization completed: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error optimizing database: {e}")
            return {"error": str(e)}
    
    async def backup_database(self, database_role: DatabaseRole = DatabaseRole.PRIMARY) -> Dict[str, Any]:
        """Create database backup"""
        if database_role != DatabaseRole.PRIMARY:
            return {"error": "Can only backup primary database"}
        
        try:
            import subprocess
            
            config = self.primary_config
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            backup_file = f"/data/backups/db_backup_{timestamp}.sql"
            
            # Create backup directory
            import os
            os.makedirs("/data/backups", exist_ok=True)
            
            # Run pg_dump
            cmd = [
                "pg_dump",
                f"--host={config.host}",
                f"--port={config.port}",
                f"--username={config.username}",
                f"--dbname={config.database}",
                "--verbose",
                "--clean",
                "--no-owner",
                "--no-privileges",
                f"--file={backup_file}"
            ]
            
            env = os.environ.copy()
            env['PGPASSWORD'] = config.password
            
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            if result.returncode == 0:
                # Compress backup
                subprocess.run(["gzip", backup_file], timeout=300)
                
                return {
                    "status": "success",
                    "backup_file": f"{backup_file}.gz",
                    "timestamp": timestamp,
                    "size_mb": os.path.getsize(f"{backup_file}.gz") / 1024 / 1024
                }
            else:
                logger.error(f"Backup failed: {result.stderr}")
                return {"error": result.stderr}
                
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return {"error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive database health check"""
        health_status = {
            "status": "healthy",
            "databases": {},
            "pgbouncer": {},
            "timestamp": datetime.utcnow()
        }
        
        # Check all database connections
        for pool_name, pool in self.connection_pools.items():
            try:
                conn = await pool.acquire()
                await conn.fetchval("SELECT 1")
                await pool.release(conn)
                
                health_status["databases"][pool_name] = {
                    "status": "healthy",
                    "pool_size": pool.get_size(),
                    "free_connections": pool.get_idle_size()
                }
                
            except Exception as e:
                health_status["databases"][pool_name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                health_status["status"] = "degraded"
        
        # Check PgBouncer
        try:
            pgbouncer_stats = await self.pgbouncer.get_stats()
            if pgbouncer_stats:
                health_status["pgbouncer"] = {
                    "status": "healthy",
                    "stats": pgbouncer_stats
                }
            else:
                health_status["pgbouncer"] = {"status": "unavailable"}
                
        except Exception as e:
            health_status["pgbouncer"] = {
                "status": "unhealthy", 
                "error": str(e)
            }
        
        return health_status
    
    async def close(self):
        """Close all database connections"""
        for pool in self.connection_pools.values():
            await pool.close()
        
        for engine in self.async_engines.values():
            await engine.dispose()
        
        logger.info("Database connection manager closed")


# Global instance
database_manager = DatabaseConnectionManager()

def get_database_manager() -> DatabaseConnectionManager:
    """Get the global database manager instance"""
    return database_manager

async def initialize_database_manager():
    """Initialize the database manager"""
    try:
        await database_manager.initialize()
        logger.info("Database manager initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database manager: {e}")
        return False
