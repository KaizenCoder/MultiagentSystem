
# Configuration SQLite pour dveloppement NextGeneration
DATABASE_URL = "sqlite:///./nextgen_dev.db"

# Pour tests
import os
from sqlalchemy import create_engine
from memory_api.app.db.models import Base

def get_test_engine():
    """Moteur SQLite pour tests"""
    engine = create_engine("sqlite:///./test_nextgen.db", echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_dev_engine():
    """Moteur SQLite pour dveloppement"""
    engine = create_engine("sqlite:///./nextgen_dev.db", echo=False)
    Base.metadata.create_all(engine)
    return engine




