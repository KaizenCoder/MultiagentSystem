#!/usr/bin/env python3
"""
Contournement problème encodage psycopg2 Windows
Solution: Utiliser SQLAlchemy avec options spécifiques
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

def connect_postgres_safe():
    """Connexion PostgreSQL sécurisée avec gestion encodage"""
    
    # Configuration forcée
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    try:
        # URL de connexion avec options
        DATABASE_URL = (
            "postgresql://postgres:postgres@localhost:5432/nextgen_db"
            "?client_encoding=utf8&application_name=nextgen"
        )
        
        # Moteur SQLAlchemy avec options spécifiques
        engine = create_engine(
            DATABASE_URL,
            poolclass=NullPool,
            echo=False,
            connect_args={
                "options": "-c client_encoding=utf8 -c timezone=UTC"
            }
        )
        
        return engine
        
    except Exception as e:
        print(f"Erreur connexion: {e}")
        return None

if __name__ == "__main__":
    engine = connect_postgres_safe()
    if engine:
        print("✅ Connexion PostgreSQL réussie")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database()"))
            print(f"Base: {result.fetchone()[0]}")
    else:
        print("❌ Échec connexion")
