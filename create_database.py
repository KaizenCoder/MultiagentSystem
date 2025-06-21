#!/usr/bin/env python3
# Création de la base de données nextgeneration

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

print("🗄️ Création de la base de données nextgeneration...")

try:
    # Connexion à la base système
    conn = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='postgres',
        database='postgres'
    )
    
    # Mode autocommit pour CREATE DATABASE
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Vérifier si la base existe déjà
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'nextgeneration'")
    exists = cursor.fetchone()
    
    if exists:
        print("✅ Base de données 'nextgeneration' existe déjà")
    else:
        # Créer la base de données
        cursor.execute("CREATE DATABASE nextgeneration")
        print("✅ Base de données 'nextgeneration' créée avec succès")
    
    cursor.close()
    conn.close()
    
    # Test de connexion à la nouvelle base
    print("🔍 Test de connexion à la base nextgeneration...")
    test_conn = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='postgres',
        database='nextgeneration'
    )
    
    test_cursor = test_conn.cursor()
    test_cursor.execute("SELECT version()")
    version = test_cursor.fetchone()[0]
    print(f"✅ Connexion réussie : {version[:50]}...")
    
    test_cursor.close()
    test_conn.close()
    
    print()
    print("🎉 BASE DE DONNÉES NEXTGENERATION PRÊTE !")
    
except Exception as e:
    print(f"❌ Erreur : {e}") 