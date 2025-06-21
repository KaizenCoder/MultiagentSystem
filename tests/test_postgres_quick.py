#!/usr/bin/env python3
"""
Test rapide de connectivit PostgreSQL
"""

import os
import sys

def test_postgres_connectivity():
    """Test simple de connectivit PostgreSQL"""
    
    print(" TEST CONNECTIVIT POSTGRESQL")
    print("="*40)
    
    # Configuration variables d'environnement pour viter l'erreur d'encodage
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    try:
        print("1 Test import psycopg2...")
        import psycopg2
        print("   [CHECK] psycopg2 import")
        
        print("\n2 Test connexion PostgreSQL...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="nextgen_db", 
            user="postgres",
            password="postgres"
        )
        print("   [CHECK] Connexion tablie")
        
        print("\n3 Test requte simple...")
        cursor = conn.cursor()
        cursor.execute("SELECT current_database(), version();")
        db_name, version = cursor.fetchone()
        print(f"   [CHECK] Base: {db_name}")
        print(f"   [CHECK] Version: {version[:60]}...")
        
        print("\n4 Test encodage...")
        cursor.execute("SHOW server_encoding;")
        server_encoding = cursor.fetchone()[0]
        cursor.execute("SHOW client_encoding;")
        client_encoding = cursor.fetchone()[0]
        print(f"   [CHECK] Encodage serveur: {server_encoding}")
        print(f"   [CHECK] Encodage client: {client_encoding}")
        
        cursor.close()
        conn.close()
        
        print("\n POSTGRESQL FONCTIONNE PARFAITEMENT!")
        return True
        
    except Exception as e:
        print(f"\n[CROSS] Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_postgres_connectivity()
    if success:
        print("\n[CHECK] PostgreSQL est oprationnel et prt  l'emploi")
    else:
        print("\n Problmes de connectivit dtects")




