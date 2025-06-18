#!/usr/bin/env python3
"""
Test PostgreSQL avec SQLAlchemy et gestion d'encodage
"""

import os
import sys

def test_postgres_sqlalchemy():
    """Test PostgreSQL avec SQLAlchemy"""
    
    print("🔧 TEST POSTGRESQL AVEC SQLALCHEMY")
    print("="*45)
    
    try:
        print("1️⃣ Configuration environnement...")
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        os.environ['PYTHONUTF8'] = '1'
        print("   ✅ Variables d'environnement configurées")
        
        print("\n2️⃣ Import SQLAlchemy...")
        from sqlalchemy import create_engine, text
        from sqlalchemy.pool import NullPool
        print("   ✅ SQLAlchemy importé")
        
        print("\n3️⃣ Création moteur SQLAlchemy...")
        # Utiliser une URL avec options d'encodage explicites
        DATABASE_URL = (
            "postgresql://postgres:postgres@localhost:5432/nextgen_db"
            "?client_encoding=utf8&application_name=nextgen_test"
        )
        
        engine = create_engine(
            DATABASE_URL,
            poolclass=NullPool,
            echo=False,
            connect_args={
                "options": "-c client_encoding=utf8"
            }
        )
        print("   ✅ Moteur SQLAlchemy créé")
        
        print("\n4️⃣ Test connexion...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), version()"))
            row = result.fetchone()
            db_name, version = row[0], row[1]
            print(f"   ✅ Base: {db_name}")
            print(f"   ✅ Version: {version[:60]}...")
            
            # Test encodage
            result = conn.execute(text("SHOW server_encoding"))
            server_enc = result.fetchone()[0]
            result = conn.execute(text("SHOW client_encoding"))
            client_enc = result.fetchone()[0]
            print(f"   ✅ Encodage serveur: {server_enc}")
            print(f"   ✅ Encodage client: {client_enc}")
        
        print("\n5️⃣ Test avec modèles corrigés...")
        sys.path.append("C:\\Dev\\nextgeneration")
        from memory_api.app.db.models import Base, AgentSession, MemoryItem
        
        # Test création des tables
        Base.metadata.create_all(engine)
        print("   ✅ Tables créées avec succès")
        
        # Test insertion simple
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Créer une session d'agent de test
        test_session = AgentSession(
            session_id="test_validation_final",
            agent_id="validator",
            agent_type="testing",
            session_metadata={"test": True, "encoding": "utf-8"}
        )
        session.add(test_session)
        session.commit()
        
        # Vérifier insertion
        count = session.query(AgentSession).count()
        session.close()
        
        print(f"   ✅ Données insérées et vérifiées ({count} sessions)")
        
        print("\n🎉 POSTGRESQL AVEC SQLALCHEMY FONCTIONNE!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur SQLAlchemy: {e}")
        print(f"   Type d'erreur: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_postgres_sqlalchemy()
    if success:
        print("\n✅ PostgreSQL + SQLAlchemy opérationnels")
        print("   Les modèles corrigés fonctionnent parfaitement!")
    else:
        print("\n⚠️ Problèmes SQLAlchemy détectés")
