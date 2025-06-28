#!/usr/bin/env python3
"""
Test simple de connexion PostgreSQL avec variables d'environnement
"""
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def test_connection_direct():
    """Test de connexion directe avec psycopg2"""
    try:
        # Paramètres de connexion
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'user': 'postgres',
            'password': 'SecurePostgresPassword2024!',
            'database': 'nextgeneration',
            'client_encoding': 'UTF8'
        }
        
        print("🔍 Test connexion PostgreSQL directe...")
        print(f"   Host: {conn_params['host']}:{conn_params['port']}")
        print(f"   Database: {conn_params['database']}")
        print(f"   User: {conn_params['user']}")
        
        # Connexion
        conn = psycopg2.connect(**conn_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = conn.cursor()
        
        # Test 1: Version PostgreSQL
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Version PostgreSQL: {version.split()[1]}")
        
        # Test 2: Encodage
        cursor.execute("SHOW server_encoding;")
        server_encoding = cursor.fetchone()[0]
        print(f"✅ Server encoding: {server_encoding}")
        
        cursor.execute("SHOW client_encoding;")
        client_encoding = cursor.fetchone()[0]
        print(f"✅ Client encoding: {client_encoding}")
        
        # Test 3: Base de données
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()[0]
        print(f"✅ Base de données: {current_db}")
        
        # Test 4: Tables existantes
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"✅ Tables trouvées: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎯 RÉSULTAT: Connexion PostgreSQL RÉUSSIE !")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False

def test_sqlalchemy_connection():
    """Test avec SQLAlchemy"""
    try:
        from sqlalchemy import create_engine, text
        
        # URL de connexion
        database_url = "postgresql://postgres:SecurePostgresPassword2024!@localhost:5432/nextgeneration"
        
        print("\n🔍 Test connexion SQLAlchemy...")
        
        # Moteur avec paramètres UTF-8
        engine = create_engine(
            database_url,
            connect_args={
                "client_encoding": "utf8",
                "application_name": "NextGeneration_Test"
            },
            echo=False
        )
        
        # Test connexion
        with engine.connect() as conn:
            # Test simple
            result = conn.execute(text("SELECT 1 as test"))
            test_value = result.scalar()
            print(f"✅ Test simple: {test_value}")
            
            # Test encodage
            result = conn.execute(text("SELECT 'Test UTF-8: éàü' as test_utf8"))
            utf8_test = result.scalar()
            print(f"✅ Test UTF-8: {utf8_test}")
            
        print("🎯 RÉSULTAT: SQLAlchemy connexion RÉUSSIE !")
        return True
        
    except Exception as e:
        print(f"❌ ERREUR SQLAlchemy: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TEST CONNEXION POSTGRESQL NEXTGENERATION")
    print("=" * 50)
    
    # Test 1: Connexion directe
    success1 = test_connection_direct()
    
    # Test 2: SQLAlchemy
    success2 = test_sqlalchemy_connection()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("✅ TOUS LES TESTS RÉUSSIS - PostgreSQL opérationnel !")
        exit(0)
    else:
        print("❌ ÉCHEC - Corrections nécessaires")
        exit(1) 



