#!/usr/bin/env python3
"""
Test de validation final pour les corrections SQLAlchemy PostgreSQL
Test avec la configuration Docker correcte
"""

import sys
import os
import json
from logging_manager_optimized import LoggingManager
from datetime import datetime
import time

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# LoggingManager NextGeneration - Tests
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={
            "logger_name": "test_validation_corrections",
            "log_level": "DEBUG",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": False,  # Tests synchrones
            "console_output": True
        })

def test_sqlalchemy_corrections():
    """Test spcifique des corrections SQLAlchemy"""
    
    logger.info(" Test des corrections SQLAlchemy - Models PostgreSQL")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {},
        "success_count": 0,
        "total_tests": 0
    }
    
    # Test 1: Import des modules SQLAlchemy
    try:
        from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Boolean, Index, Float, text
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import relationship
        results["tests"]["sqlalchemy_imports"] = {"status": "SUCCESS", "message": "Tous les imports SQLAlchemy russis"}
        results["success_count"] += 1
        logger.info("[CHECK] Imports SQLAlchemy russis")
    except Exception as e:
        results["tests"]["sqlalchemy_imports"] = {"status": "FAILED", "error": str(e)}
        logger.error(f"[CROSS] chec imports SQLAlchemy: {e}")
    results["total_tests"] += 1
    
    # Test 2: Import du models.py corrig
    try:
        sys.path.append("C:\\Dev\\nextgeneration")
        from memory_api.app.db.models import Base, AgentSession, MemoryItem
        results["tests"]["models_import"] = {"status": "SUCCESS", "message": "Import des modles russi"}
        results["success_count"] += 1
        logger.info("[CHECK] Import des modles corrigs russi")
    except Exception as e:
        results["tests"]["models_import"] = {"status": "FAILED", "error": str(e)}
        logger.error(f"[CROSS] chec import modles: {e}")
    results["total_tests"] += 1
    
    # Test 3: Vrification de l'attribut session_metadata
    try:
        session = AgentSession()
        if hasattr(session, 'session_metadata'):
            results["tests"]["metadata_attribute"] = {"status": "SUCCESS", "message": "Attribut session_metadata trouv"}
            results["success_count"] += 1
            logger.info("[CHECK] Attribut session_metadata prsent")
        else:
            results["tests"]["metadata_attribute"] = {"status": "FAILED", "error": "Attribut session_metadata manquant"}
            logger.error("[CROSS] Attribut session_metadata manquant")
    except Exception as e:
        results["tests"]["metadata_attribute"] = {"status": "FAILED", "error": str(e)}
        logger.error(f"[CROSS] Erreur vrification metadata: {e}")
    results["total_tests"] += 1
    
    # Test 4: Connexion PostgreSQL Docker
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        # Connexion Docker standard (port 5432)
        DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/nextgen_db"
        engine = create_engine(DATABASE_URL)
        
        # Test de connexion
        connection = engine.connect()
        connection.close()
        
        results["tests"]["postgres_connection"] = {"status": "SUCCESS", "message": "Connexion PostgreSQL russie"}
        results["success_count"] += 1
        logger.info("[CHECK] Connexion PostgreSQL Docker russie")
        
    except Exception as e:
        results["tests"]["postgres_connection"] = {"status": "FAILED", "error": str(e)}
        logger.warning(f" Connexion PostgreSQL: {e}")
    results["total_tests"] += 1
    
    # Test 5: Cration des tables
    try:
        if 'engine' in locals():
            Base.metadata.create_all(engine)
            results["tests"]["table_creation"] = {"status": "SUCCESS", "message": "Tables cres sans erreur"}
            results["success_count"] += 1
            logger.info("[CHECK] Cration des tables russie")
        else:
            results["tests"]["table_creation"] = {"status": "SKIPPED", "message": "Pas de connexion DB"}
    except Exception as e:
        results["tests"]["table_creation"] = {"status": "FAILED", "error": str(e)}
        logger.error(f"[CROSS] chec cration tables: {e}")
    results["total_tests"] += 1
    
    # Calcul du score
    success_rate = (results["success_count"] / results["total_tests"]) * 100
    results["success_rate"] = success_rate
    
    logger.info(f"[CHART] Score final: {results['success_count']}/{results['total_tests']} ({success_rate:.1f}%)")
    
    # Sauvegarde du rapport
    report_file = f"C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\tests\\validation_corrections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"[CLIPBOARD] Rapport sauvegard: {report_file}")
    
    return results

if __name__ == "__main__":
    results = test_sqlalchemy_corrections()
    
    # Affichage rsum
    print("\n" + "="*60)
    print("[TARGET] RSUM VALIDATION CORRECTIONS SQLALCHEMY")
    print("="*60)
    
    for test_name, test_result in results["tests"].items():
        status = test_result["status"]
        icon = "[CHECK]" if status == "SUCCESS" else "[CROSS]" if status == "FAILED" else ""
        print(f"{icon} {test_name}: {status}")
        if "message" in test_result:
            print(f"    {test_result['message']}")
        if "error" in test_result:
            print(f"    [CROSS] {test_result['error']}")
    
    print(f"\n Score global: {results['success_count']}/{results['total_tests']} ({results['success_rate']:.1f}%)")
    
    if results['success_rate'] >= 80:
        print(" CORRECTIONS VALIDES - Les modifications SQLAlchemy sont fonctionnelles!")
    elif results['success_rate'] >= 60:
        print("[CHECK] CORRECTIONS PARTIELLES - Les problmes SQLAlchemy principaux sont rsolus")
    else:
        print(" CORRECTIONS  COMPLTER - Des problmes persistent")
