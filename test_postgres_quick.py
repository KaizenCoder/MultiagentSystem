#!/usr/bin/env python3
"""
Test rapide de connectivité PostgreSQL
"""

import os
import sys

def test_postgres_connectivity():
    """Test simple de connectivité PostgreSQL"""
    
    print("🧪 TEST CONNECTIVITÉ POSTGRESQL")
    print("="*40)
    
    # Configuration variables d'environnement pour éviter l'erreur d'encodage
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    try:
        print("1️⃣ Test import psycopg2...")
        import psycopg2
        print("   ✅ psycopg2 importé")
        
        print("\n2️⃣ Test connexion PostgreSQL...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="nextgen_db", 
            user="postgres",
            password="postgres"
        )
        print("   ✅ Connexion établie")
        
        print("\n3️⃣ Test requête simple...")
        cursor = conn.cursor()
        cursor.execute("SELECT current_database(), version();")
        db_name, version = cursor.fetchone()
        print(f"   ✅ Base: {db_name}")
        print(f"   ✅ Version: {version[:60]}...")
        
        print("\n4️⃣ Test encodage...")
        cursor.execute("SHOW server_encoding;")
        server_encoding = cursor.fetchone()[0]
        cursor.execute("SHOW client_encoding;")
        client_encoding = cursor.fetchone()[0]
        print(f"   ✅ Encodage serveur: {server_encoding}")
        print(f"   ✅ Encodage client: {client_encoding}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 POSTGRESQL FONCTIONNE PARFAITEMENT!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_postgres_connectivity()
    if success:
        print("\n✅ PostgreSQL est opérationnel et prêt à l'emploi")
    else:
        print("\n⚠️ Problèmes de connectivité détectés")
