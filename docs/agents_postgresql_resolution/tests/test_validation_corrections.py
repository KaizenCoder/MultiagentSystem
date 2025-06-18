#!/usr/bin/env python3
"""
Test de validation final pour les corrections SQLAlchemy PostgreSQL
Test avec la configuration Docker correcte
"""

import sys
import os
import json
import logging
from datetime import datetime
import time

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_sqlalchemy_corrections():
    """Test spécifique des corrections SQLAlchemy"""
    
    logger.info("🧪 Test des corrections SQLAlchemy - Models PostgreSQL")
    
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
        results["tests"]["sqlalchemy_imports"] = {"status": "SUCCESS", "message": "Tous les imports SQLAlchemy réussis"}
        results["success_count"] += 1
        logger.info("✅ Imports SQLAlchemy réussis")
    except Exception as e:
        results["tests"]["sqlalchemy_imports"] = {"status": "FAILED", "error": str(e)}
        logger.error(f"❌ Échec imports SQLAlchemy: {e}")
    results["total_tests"] += 1
    
    # Test 2: Import du models.py corrigé
    try:
        sys.path.append("C:\\Dev\\nextgeneration")
        from memory_api.app.db.models import Base, AgentSession, MemoryItem
        results["tests"]["models_import"] = {"status": "SUCCESS", "message": "Import des modèles réussi"}
        results["success_count"] += 1
        logger.info("✅ Import des modèles corrigés réussi")
    except Exception as e:
        results["tests"]["models_import"] = {"status": "FAILED", "error": str(e)}
        logger.error(f"❌ Échec import modèles: {e}")
    results["total_tests"] += 1
    
    # Test 3: Vérification de l'attribut session_metadata
    try:
        session = AgentSession()
        if hasattr(session, 'session_metadata'):
            results["tests"]["metadata_attribute"] = {"status": "SUCCESS", "message": "Attribut session_metadata trouvé"}
            results["success_count"] += 1
            logger.info("✅ Attribut session_metadata présent")
        else:
            results["tests"]["metadata_attribute"] = {"status": "FAILED", "error": "Attribut session_metadata manquant"}
            logger.error("❌ Attribut session_metadata manquant")
    except Exception as e:
        results["tests"]["metadata_attribute"] = {"status": "FAILED", "error": str(e)}
        logger.error(f"❌ Erreur vérification metadata: {e}")
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
        
        results["tests"]["postgres_connection"] = {"status": "SUCCESS", "message": "Connexion PostgreSQL réussie"}
        results["success_count"] += 1
        logger.info("✅ Connexion PostgreSQL Docker réussie")
        
    except Exception as e:
        results["tests"]["postgres_connection"] = {"status": "FAILED", "error": str(e)}
        logger.warning(f"⚠️ Connexion PostgreSQL: {e}")
    results["total_tests"] += 1
    
    # Test 5: Création des tables
    try:
        if 'engine' in locals():
            Base.metadata.create_all(engine)
            results["tests"]["table_creation"] = {"status": "SUCCESS", "message": "Tables créées sans erreur"}
            results["success_count"] += 1
            logger.info("✅ Création des tables réussie")
        else:
            results["tests"]["table_creation"] = {"status": "SKIPPED", "message": "Pas de connexion DB"}
    except Exception as e:
        results["tests"]["table_creation"] = {"status": "FAILED", "error": str(e)}
        logger.error(f"❌ Échec création tables: {e}")
    results["total_tests"] += 1
    
    # Calcul du score
    success_rate = (results["success_count"] / results["total_tests"]) * 100
    results["success_rate"] = success_rate
    
    logger.info(f"📊 Score final: {results['success_count']}/{results['total_tests']} ({success_rate:.1f}%)")
    
    # Sauvegarde du rapport
    report_file = f"C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\tests\\validation_corrections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"📋 Rapport sauvegardé: {report_file}")
    
    return results

if __name__ == "__main__":
    results = test_sqlalchemy_corrections()
    
    # Affichage résumé
    print("\n" + "="*60)
    print("🎯 RÉSUMÉ VALIDATION CORRECTIONS SQLALCHEMY")
    print("="*60)
    
    for test_name, test_result in results["tests"].items():
        status = test_result["status"]
        icon = "✅" if status == "SUCCESS" else "❌" if status == "FAILED" else "⏭️"
        print(f"{icon} {test_name}: {status}")
        if "message" in test_result:
            print(f"   → {test_result['message']}")
        if "error" in test_result:
            print(f"   → ❌ {test_result['error']}")
    
    print(f"\n🏆 Score global: {results['success_count']}/{results['total_tests']} ({results['success_rate']:.1f}%)")
    
    if results['success_rate'] >= 80:
        print("🎉 CORRECTIONS VALIDÉES - Les modifications SQLAlchemy sont fonctionnelles!")
    elif results['success_rate'] >= 60:
        print("✅ CORRECTIONS PARTIELLES - Les problèmes SQLAlchemy principaux sont résolus")
    else:
        print("⚠️ CORRECTIONS À COMPLÉTER - Des problèmes persistent")
