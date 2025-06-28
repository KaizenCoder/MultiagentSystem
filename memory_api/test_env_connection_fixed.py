#!/usr/bin/env python3
"""
Test connexion PostgreSQL avec gestion encodage Windows
"""
import os
import sys
import locale

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    
    # Définir locale en UTF-8
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        except:
            pass

def test_connection_with_encoding():
    """Test avec gestion explicite de l'encodage"""
    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        
        # Paramètres de connexion avec encodage explicite
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'user': 'postgres',
            'password': 'SecurePostgresPassword2024!',
            'database': 'nextgeneration'
        }
        
        print("Test connexion PostgreSQL avec encodage force...")
        
        # Connexion
        conn = psycopg2.connect(**conn_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        conn.set_client_encoding('UTF8')
        
        cursor = conn.cursor()
        
        # Test 1: Version (sans caractères spéciaux)
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        # Nettoyer la chaîne pour éviter les problèmes d'encodage
        version_clean = version.split()[0:2]  # Prendre seulement "PostgreSQL" et version
        print(f"Version: {' '.join(version_clean)}")
        
        # Test 2: Encodage
        cursor.execute("SHOW server_encoding;")
        server_encoding = cursor.fetchone()[0]
        print(f"Server encoding: {server_encoding}")
        
        cursor.execute("SHOW client_encoding;")
        client_encoding = cursor.fetchone()[0]
        print(f"Client encoding: {client_encoding}")
        
        # Test 3: Base de données
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()[0]
        print(f"Base de donnees: {current_db}")
        
        # Test 4: Test simple
        cursor.execute("SELECT 1 as test_value;")
        test_value = cursor.fetchone()[0]
        print(f"Test simple: {test_value}")
        
        # Test 5: Tables
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        table_count = cursor.fetchone()[0]
        print(f"Nombre de tables: {table_count}")
        
        cursor.close()
        conn.close()
        
        print("\nRESULTAT: Connexion PostgreSQL REUSSIE !")
        return True
        
    except Exception as e:
        print(f"\nERREUR: {str(e)}")
        # Afficher plus de détails sur l'erreur
        import traceback
        traceback.print_exc()
        return False

def test_sqlalchemy_fixed():
    """Test SQLAlchemy avec encodage corrigé"""
    try:
        from sqlalchemy import create_engine, text
        
        # URL avec paramètres d'encodage
        database_url = "postgresql://postgres:SecurePostgresPassword2024!@localhost:5432/nextgeneration?client_encoding=utf8"
        
        print("\nTest SQLAlchemy avec encodage corrige...")
        
        # Moteur avec paramètres UTF-8 renforcés
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
            print(f"Test simple: {test_value}")
            
            # Test sans caractères spéciaux
            result = conn.execute(text("SELECT 'Test OK' as test_string"))
            string_test = result.scalar()
            print(f"Test string: {string_test}")
            
        print("RESULTAT: SQLAlchemy connexion REUSSIE !")
        return True
        
    except Exception as e:
        print(f"ERREUR SQLAlchemy: {str(e)}")
        return False

if __name__ == "__main__":
    print("TEST CONNEXION POSTGRESQL - VERSION CORRIGEE")
    print("=" * 50)
    
    # Afficher info système
    print(f"Plateforme: {sys.platform}")
    print(f"Encodage prefere: {locale.getpreferredencoding()}")
    
    # Test 1: Connexion directe
    success1 = test_connection_with_encoding()
    
    # Test 2: SQLAlchemy
    success2 = test_sqlalchemy_fixed()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("TOUS LES TESTS REUSSIS - PostgreSQL operationnel !")
        exit(0)
    else:
        print("ECHEC - Corrections necessaires")
        exit(1) 



