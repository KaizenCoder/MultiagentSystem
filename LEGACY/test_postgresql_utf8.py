# Test PostgreSQL UTF-8 - Script de Reproduction du Problème
# Pour accompagner PROMPT_POSTGRESQL_EXPERT_HELP_2025.md

import psycopg2
import sys
import locale
import os
from datetime import datetime

print("=" * 60)
print("🔍 TEST POSTGRESQL UTF-8 - DIAGNOSTIC COMPLET")
print("=" * 60)

# Informations système
print(f"📅 Date du test : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"🐍 Python version : {sys.version}")
print(f"📦 psycopg2 version : {psycopg2.__version__}")
print(f"💻 Plateforme : {sys.platform}")
print(f"🌐 System encoding : {sys.getdefaultencoding()}")
print(f"🏳️ Locale : {locale.getlocale()}")
print(f"📝 Preferred encoding : {locale.getpreferredencoding()}")
print(f"🌍 LANG : {os.environ.get('LANG', 'Not set')}")
print(f"🌍 LC_ALL : {os.environ.get('LC_ALL', 'Not set')}")
print()

# Configuration de test
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres',
    'database': 'nextgeneration',
    'client_encoding': 'utf8'
}

print("🔧 Configuration PostgreSQL :")
for key, value in POSTGRES_CONFIG.items():
    if key == 'password':
        print(f"   {key}: {'*' * len(value)}")
    else:
        print(f"   {key}: {value}")
print()

# Test de connexion
print("🚀 DÉBUT DU TEST DE CONNEXION")
print("-" * 40)

try:
    print("1️⃣ Tentative de connexion PostgreSQL...")
    
    # Connexion avec tous les paramètres d'encodage possibles
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    print("✅ Connexion établie avec succès !")
    
    # Test de base
    print("2️⃣ Test de requête simple...")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 as test_value")
    result = cursor.fetchone()
    print(f"✅ Requête réussie : {result}")
    
    # Test version PostgreSQL
    print("3️⃣ Test version PostgreSQL...")
    cursor.execute("SELECT version()")
    version = cursor.fetchone()
    print(f"✅ Version PostgreSQL : {version[0][:50]}...")
    
    # Test encodage
    print("4️⃣ Test paramètres d'encodage...")
    cursor.execute("SHOW server_encoding")
    server_enc = cursor.fetchone()[0]
    cursor.execute("SHOW client_encoding") 
    client_enc = cursor.fetchone()[0]
    cursor.execute("SHOW lc_messages")
    lc_messages = cursor.fetchone()[0]
    
    print(f"✅ Server encoding : {server_enc}")
    print(f"✅ Client encoding : {client_enc}")
    print(f"✅ LC_MESSAGES : {lc_messages}")
    
    # Test caractères français
    print("5️⃣ Test caractères français...")
    cursor.execute("SELECT 'Café français avec accents éàù' as test_french")
    french_test = cursor.fetchone()[0]
    print(f"✅ Test français : {french_test}")
    
    # Fermeture propre
    cursor.close()
    conn.close()
    print()
    print("🎉 TOUS LES TESTS RÉUSSIS !")
    print("✅ PostgreSQL UTF-8 fonctionne parfaitement")
    
except Exception as e:
    print(f"❌ ERREUR DÉTECTÉE !")
    print(f"❌ Type d'erreur : {type(e).__name__}")
    print(f"❌ Message : {e}")
    
    # Analyse détaillée de l'erreur
    if hasattr(e, 'args') and e.args:
        print(f"❌ Arguments : {e.args}")
    
    if isinstance(e, UnicodeDecodeError):
        print(f"❌ Encoding : {e.encoding}")
        print(f"❌ Object : {e.object}")
        print(f"❌ Start : {e.start}")
        print(f"❌ End : {e.end}")
        print(f"❌ Reason : {e.reason}")
        
        # Analyse du byte problématique
        if hasattr(e, 'object') and e.start < len(e.object):
            problem_byte = e.object[e.start]
            print(f"❌ Byte problématique : 0x{problem_byte:02x} ({chr(problem_byte) if 32 <= problem_byte <= 126 else 'non-printable'})")
    
    print()
    print("🔍 DIAGNOSTIC :")
    print("   - Erreur au niveau de la connexion PostgreSQL")
    print("   - Problème d'encodage UTF-8 vs CP1252")
    print("   - Locale Windows française incompatible")
    print("   - Solution requise : Configuration PostgreSQL ou psycopg2")

print()
print("=" * 60)
print("📄 Rapport généré pour PROMPT_POSTGRESQL_EXPERT_HELP_2025.md")
print("🆘 Merci de partager ce rapport avec un expert PostgreSQL !")
print("=" * 60) 



