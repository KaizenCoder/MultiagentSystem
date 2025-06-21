#!/usr/bin/env python3
"""
Script de création de base PostgreSQL UTF-8 compatible
Basé sur la solution technique recommandée par l'expert
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

def create_utf8_database():
    """Créer une base PostgreSQL UTF-8 avec locale C compatible"""
    
    print("🎯 SOLUTION UTF-8 DÉFINITIVE - CRÉATION BASE COMPATIBLE")
    print("=" * 60)
    
    # Paramètres de connexion à la base par défaut
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'SecurePostgresPassword2024!',
        'database': 'postgres'  # Connexion à la base par défaut
    }
    
    try:
        print("🔌 Connexion à PostgreSQL...")
        
        # Connexion à la base postgres par défaut
        conn = psycopg2.connect(**conn_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Connexion réussie à la base par défaut")
        
        # Vérifier si la base existe déjà
        cursor.execute("""
            SELECT 1 FROM pg_database 
            WHERE datname = 'nextgeneration_utf8'
        """)
        
        if cursor.fetchone():
            print("⚠️  Base nextgeneration_utf8 existe déjà")
            
            # Demander confirmation pour la recréer
            response = input("Voulez-vous la recréer ? (y/N): ")
            if response.lower() == 'y':
                print("🗑️  Suppression de l'ancienne base...")
                
                # Fermer les connexions existantes
                cursor.execute("""
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = 'nextgeneration_utf8'
                    AND pid <> pg_backend_pid()
                """)
                
                # Supprimer la base
                cursor.execute("DROP DATABASE nextgeneration_utf8")
                print("✅ Ancienne base supprimée")
            else:
                print("❌ Opération annulée")
                return False
        
        # Créer la nouvelle base avec les paramètres UTF-8 corrects
        print("🏗️  Création de la base nextgeneration_utf8...")
        
        create_db_sql = """
            CREATE DATABASE nextgeneration_utf8
            WITH 
                ENCODING 'UTF8'
                LC_COLLATE='C'
                LC_CTYPE='C'
                TEMPLATE=template0
        """
        
        cursor.execute(create_db_sql)
        print("✅ Base nextgeneration_utf8 créée avec succès !")
        
        cursor.close()
        conn.close()
        
        # Test de connexion à la nouvelle base
        print("\n🧪 Test de connexion à la nouvelle base...")
        
        test_conn_params = conn_params.copy()
        test_conn_params['database'] = 'nextgeneration_utf8'
        
        test_conn = psycopg2.connect(**test_conn_params)
        test_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        test_cursor = test_conn.cursor()
        
        # Tests de vérification
        print("🔍 Vérification des paramètres UTF-8...")
        
        # Test 1: Encodage
        test_cursor.execute("SHOW server_encoding")
        server_encoding = test_cursor.fetchone()[0]
        print(f"   Server encoding: {server_encoding}")
        
        test_cursor.execute("SHOW client_encoding")
        client_encoding = test_cursor.fetchone()[0]
        print(f"   Client encoding: {client_encoding}")
        
        # Test 2: Locale
        test_cursor.execute("SHOW lc_collate")
        lc_collate = test_cursor.fetchone()[0]
        print(f"   LC_COLLATE: {lc_collate}")
        
        test_cursor.execute("SHOW lc_ctype")
        lc_ctype = test_cursor.fetchone()[0]
        print(f"   LC_CTYPE: {lc_ctype}")
        
        # Test 3: Version (le test qui échouait avant)
        print("\n🎯 Test critique: SELECT version()...")
        test_cursor.execute("SELECT version()")
        version = test_cursor.fetchone()[0]
        print(f"✅ Version récupérée: {version[:50]}...")
        
        # Test 4: Test avec caractères français
        print("\n🇫🇷 Test caractères français...")
        test_cursor.execute("SELECT 'Test UTF-8: éàüç' as test_french")
        french_test = test_cursor.fetchone()[0]
        print(f"✅ Test français: {french_test}")
        
        test_cursor.close()
        test_conn.close()
        
        print("\n" + "=" * 60)
        print("🎉 SUCCÈS ! Base PostgreSQL UTF-8 opérationnelle !")
        print("=" * 60)
        print("\n📋 Prochaines étapes:")
        print("1. Modifier memory_api/app/db/session.py")
        print("2. Changer POSTGRES_DB='nextgeneration_utf8'")
        print("3. Relancer les tests PostgreSQL")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        print("\n🔧 Vérifications à effectuer:")
        print("- PostgreSQL est-il démarré ?")
        print("- Mot de passe correct ?")
        print("- Permissions administrateur ?")
        return False

def update_session_config():
    """Mettre à jour la configuration pour utiliser la nouvelle base"""
    
    print("\n🔧 Mise à jour de la configuration...")
    
    # Lire le fichier session.py
    session_file = "app/db/session.py"
    
    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer le nom de la base
        old_db = 'postgres_db = os.getenv("POSTGRES_DB", "nextgeneration")'
        new_db = 'postgres_db = os.getenv("POSTGRES_DB", "nextgeneration_utf8")'
        
        if old_db in content:
            content = content.replace(old_db, new_db)
            
            with open(session_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Configuration mise à jour !")
            print(f"   Base par défaut: nextgeneration_utf8")
            return True
        else:
            print("⚠️  Configuration déjà à jour ou pattern non trouvé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur mise à jour config: {e}")
        return False

if __name__ == "__main__":
    print("🚀 RÉSOLUTION DÉFINITIVE PROBLÈME UTF-8 POSTGRESQL")
    print("Basé sur l'analyse technique de l'expert")
    print()
    
    # Étape 1: Créer la base UTF-8
    if create_utf8_database():
        print()
        
        # Étape 2: Mettre à jour la configuration
        update_config = input("Mettre à jour la configuration automatiquement ? (Y/n): ")
        if update_config.lower() != 'n':
            update_session_config()
        
        print("\n🎯 MISSION ACCOMPLIE !")
        print("Le problème UTF-8 devrait être résolu définitivement.")
        
    else:
        print("\n❌ Échec de la création de base")
        sys.exit(1) 



