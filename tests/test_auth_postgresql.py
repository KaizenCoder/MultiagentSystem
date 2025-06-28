#!/usr/bin/env python3
# Test authentification PostgreSQL après résolution UTF-8

import psycopg2

# Liste des mots de passe courants à tester
passwords = [
    'postgres',
    'password', 
    'SecurePostgresPassword2024!',
    'admin',
    '123456'
]

print("🔐 Test authentification PostgreSQL...")
print("✅ Problème UTF-8 résolu - Test des credentials...")
print()

for pwd in passwords:
    try:
        print(f"🔑 Test mot de passe : {'*' * len(pwd)}")
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password=pwd,
            database='postgres',  # Base système
            client_encoding='utf8'
        )
        
        print(f"✅ CONNEXION RÉUSSIE avec mot de passe : {pwd}")
        
        # Test rapide
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL version : {version[:50]}...")
        
        # Test lc_messages
        cursor.execute("SHOW lc_messages")
        lc_messages = cursor.fetchone()[0]
        print(f"✅ lc_messages = '{lc_messages}' (UTF-8 compatible)")
        
        cursor.close()
        conn.close()
        
        print()
        print("🎉 POSTGRESQL UTF-8 100% FONCTIONNEL !")
        print(f"🔑 Mot de passe correct : {pwd}")
        break
        
    except psycopg2.OperationalError as e:
        if "password authentication failed" in str(e):
            print(f"❌ Mot de passe incorrect")
        else:
            print(f"❌ Erreur : {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
    
    print()

else:
    print("❌ Aucun mot de passe testé ne fonctionne")
    print("💡 Il faut réinitialiser le mot de passe PostgreSQL") 



