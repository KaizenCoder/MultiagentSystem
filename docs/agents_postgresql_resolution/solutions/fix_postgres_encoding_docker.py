#!/usr/bin/env python3
"""
Correction définitive du problème d'encodage PostgreSQL 
Reconfiguration du conteneur Docker avec encodage UTF-8
"""

import subprocess
import time
import json
from datetime import datetime

def fix_postgres_encoding_docker():
    """Correction encodage PostgreSQL via Docker"""
    
    print("🐳 CORRECTION ENCODAGE POSTGRESQL DOCKER")
    print("="*50)
    
    steps = []
    
    # Étape 1: Arrêter le conteneur actuel
    print("\n1️⃣ Arrêt conteneur PostgreSQL actuel...")
    try:
        result = subprocess.run(['docker', 'stop', 'agent_postgres_nextgen'], 
                              capture_output=True, text=True, check=True)
        print("   ✅ Conteneur arrêté")
        steps.append({"step": "stop_container", "status": "SUCCESS"})
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️ Arrêt conteneur: {e}")
        steps.append({"step": "stop_container", "status": "WARNING", "error": str(e)})
    
    # Étape 2: Supprimer le conteneur
    print("\n2️⃣ Suppression conteneur...")
    try:
        result = subprocess.run(['docker', 'rm', 'agent_postgres_nextgen'], 
                              capture_output=True, text=True, check=True)
        print("   ✅ Conteneur supprimé")
        steps.append({"step": "remove_container", "status": "SUCCESS"})
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️ Suppression conteneur: {e}")
        steps.append({"step": "remove_container", "status": "WARNING", "error": str(e)})
    
    # Étape 3: Créer fichier Docker Compose avec encodage UTF-8
    print("\n3️⃣ Création configuration Docker Compose UTF-8...")
    
    docker_compose_utf8 = """version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: agent_postgres_nextgen_utf8
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: nextgen_db
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --lc-collate=C --lc-ctype=C"
      LC_ALL: C.UTF-8
      LANG: C.UTF-8
    ports:
      - "5432:5432"
    volumes:
      - postgres_data_utf8:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d nextgen_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    command: >
      postgres 
      -c log_statement=all
      -c log_destination=stderr
      -c logging_collector=off
      -c client_encoding=UTF8
      -c default_text_search_config=pg_catalog.english

volumes:
  postgres_data_utf8:
    driver: local

networks:
  default:
    name: agent_network_nextgen_utf8
"""
    
    compose_file = "C:\\Dev\\nextgeneration\\docker-compose.utf8.yml"
    with open(compose_file, 'w', encoding='utf-8') as f:
        f.write(docker_compose_utf8)
    
    print(f"   ✅ Configuration UTF-8 créée: {compose_file}")
    steps.append({"step": "create_utf8_config", "status": "SUCCESS", "file": compose_file})
    
    # Étape 4: Démarrer PostgreSQL avec configuration UTF-8
    print("\n4️⃣ Démarrage PostgreSQL UTF-8...")
    
    try:
        result = subprocess.run(
            ['docker-compose', '-f', compose_file, 'up', '-d'],
            capture_output=True, text=True, check=True,
            cwd="C:\\Dev\\nextgeneration"
        )
        print("   ✅ PostgreSQL UTF-8 démarré")
        steps.append({"step": "start_utf8_postgres", "status": "SUCCESS"})
        
        # Attendre que PostgreSQL soit prêt
        print("   ⏳ Attente initialisation PostgreSQL...")
        time.sleep(15)
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Échec démarrage: {e}")
        steps.append({"step": "start_utf8_postgres", "status": "FAILED", "error": str(e)})
        return steps
    
    # Étape 5: Test connexion avec encodage UTF-8
    print("\n5️⃣ Test connexion PostgreSQL UTF-8...")
    
    try:
        import psycopg2
        
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="nextgen_db",
            user="postgres",
            password="postgres",
            options="-c client_encoding=UTF8"
        )
        
        cursor = conn.cursor()
        cursor.execute("SHOW server_encoding;")
        encoding = cursor.fetchone()[0]
        
        cursor.execute("SHOW client_encoding;") 
        client_encoding = cursor.fetchone()[0]
        
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        print(f"   ✅ Connexion réussie")
        print(f"   📊 Encodage serveur: {encoding}")
        print(f"   📊 Encodage client: {client_encoding}")
        print(f"   📊 Version: {version[:50]}...")
        
        steps.append({
            "step": "test_utf8_connection",
            "status": "SUCCESS",
            "server_encoding": encoding,
            "client_encoding": client_encoding,
            "version": version
        })
        
    except Exception as e:
        print(f"   ❌ Échec test connexion: {e}")
        steps.append({"step": "test_utf8_connection", "status": "FAILED", "error": str(e)})
    
    # Étape 6: Test création tables avec models corrigés
    print("\n6️⃣ Test création tables avec models SQLAlchemy...")
    
    try:
        import sys
        sys.path.append("C:\\Dev\\nextgeneration")
        
        from sqlalchemy import create_engine
        from memory_api.app.db.models import Base
        
        engine = create_engine(
            "postgresql://postgres:postgres@localhost:5432/nextgen_db",
            client_encoding='utf8'
        )
        
        Base.metadata.create_all(engine)
        
        print("   ✅ Tables créées sans erreur d'encodage")
        steps.append({"step": "create_tables_utf8", "status": "SUCCESS"})
        
    except Exception as e:
        print(f"   ❌ Échec création tables: {e}")
        steps.append({"step": "create_tables_utf8", "status": "FAILED", "error": str(e)})
    
    # Résumé
    print("\n" + "="*50)
    print("📊 RÉSUMÉ CORRECTION ENCODAGE")
    print("="*50)
    
    success_count = sum(1 for s in steps if s["status"] == "SUCCESS")
    total_count = len(steps)
    
    for i, step in enumerate(steps, 1):
        status = step["status"]
        icon = "✅" if status == "SUCCESS" else "❌" if status == "FAILED" else "⚠️"
        print(f"{icon} {i}. {step['step']}: {status}")
    
    print(f"\n🏆 Score: {success_count}/{total_count} étapes réussies")
    
    # Sauvegarde rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rapport_path = f"C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\solutions\\docker_utf8_fix_{timestamp}.json"
    
    rapport = {
        "timestamp": datetime.now().isoformat(),
        "steps": steps,
        "success_count": success_count,
        "total_count": total_count,
        "success_rate": (success_count / total_count) * 100
    }
    
    with open(rapport_path, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    print(f"📋 Rapport sauvegardé: {rapport_path}")
    
    if rapport["success_rate"] >= 80:
        print("\n🎉 ENCODAGE RÉSOLU - PostgreSQL UTF-8 fonctionnel!")
    elif rapport["success_rate"] >= 60:
        print("\n✅ ENCODAGE PARTIELLEMENT RÉSOLU - Tests supplémentaires requis")
    else:
        print("\n⚠️ PROBLÈMES PERSISTANTS - Intervention manuelle requise")
    
    return rapport

if __name__ == "__main__":
    resultat = fix_postgres_encoding_docker()
