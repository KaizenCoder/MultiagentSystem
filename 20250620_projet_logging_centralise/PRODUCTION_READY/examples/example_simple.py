#!/usr/bin/env python3
"""
Exemple simple d'utilisation du système de logging centralisé NextGeneration
"""

import sys
import os

# Ajouter le chemin vers core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.logging_manager_optimized import LoggingManager


def exemple_basique():
    """Exemple d'utilisation basique"""
    print("🚀 EXEMPLE BASIQUE - LOGGING CENTRALISÉ")
    print("=" * 50)
    
    # 1. Initialisation du manager
    manager = LoggingManager()
    
    # 2. Configuration simple
    config = {
        'logger_name': 'mon.application',
        'log_level': 'INFO'
    }
    
    # 3. Création du logger
    logger = manager.get_logger(custom_config=config)
    
    # 4. Utilisation
    logger.info("🎯 Application démarrée avec succès")
    logger.warning("⚠️ Ceci est un avertissement")
    logger.error("❌ Erreur simulée", extra={'user_id': 123, 'action': 'test'})
    
    print("✅ Messages envoyés avec succès!")
    return logger


def exemple_avance():
    """Exemple d'utilisation avancée"""
    print("\n🔧 EXEMPLE AVANCÉ - CONFIGURATION PERSONNALISÉE")
    print("=" * 50)
    
    manager = LoggingManager()
    
    # Configuration avancée (utilise les paramètres supportés)
    config_avance = {
        'logger_name': 'production.api',
        'log_level': 'DEBUG',
        'log_dir': './logs_production',
        'max_file_size': 10485760,  # 10MB en bytes
        'backup_count': 5
    }
    
    logger = manager.get_logger(custom_config=config_avance)
    
    # Utilisation avec contexte
    logger.debug("🔍 Debug: Démarrage du processus")
    logger.info("📊 API endpoint appelé", extra={
        'endpoint': '/api/users',
        'method': 'GET',
        'response_time': 0.145
    })
    
    # Simulation d'erreur avec traceback
    try:
        raise ValueError("Erreur simulée pour démonstration")
    except Exception as e:
        logger.exception("💥 Exception capturée")
    
    print("✅ Configuration avancée testée!")
    return logger


def exemple_multiple_loggers():
    """Exemple avec plusieurs loggers"""
    print("\n🎭 EXEMPLE MULTIPLE LOGGERS")
    print("=" * 50)
    
    manager = LoggingManager()
    
    # Logger pour l'API
    api_logger = manager.get_logger(custom_config={
        'logger_name': 'nextgen.api',
        'log_level': 'INFO'
    })
    
    # Logger pour la base de données
    db_logger = manager.get_logger(custom_config={
        'logger_name': 'nextgen.database',
        'log_level': 'DEBUG'
    })
    
    # Logger pour la sécurité
    security_logger = manager.get_logger(custom_config={
        'logger_name': 'nextgen.security',
        'log_level': 'WARNING'
    })
    
    # Utilisation des différents loggers
    api_logger.info("🌐 Requête API reçue")
    db_logger.debug("🗄️ Connexion à la base de données")
    security_logger.warning("🔒 Tentative de connexion suspecte")
    
    print("✅ Loggers multiples configurés!")
    return [api_logger, db_logger, security_logger]


def exemple_performance():
    """Test de performance"""
    print("\n⚡ TEST DE PERFORMANCE")
    print("=" * 50)
    
    import time
    
    manager = LoggingManager()
    logger = manager.get_logger(custom_config={
        'logger_name': 'performance.test',
        'log_level': 'INFO'
    })
    
    # Test de performance
    start_time = time.time()
    for i in range(100):
        logger.info(f"Message de performance {i}")
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time_ms = (total_time / 100) * 1000
    
    print(f"📊 100 messages envoyés en {total_time:.3f}s")
    print(f"⚡ Performance moyenne: {avg_time_ms:.2f}ms par message")
    
    if avg_time_ms < 5.0:
        print("✅ Performance excellente!")
    else:
        print("⚠️ Performance acceptable")
    
    return logger


def main():
    """Fonction principale"""
    print("🎯 DÉMONSTRATION SYSTÈME LOGGING CENTRALISÉ NEXTGENERATION")
    print("=" * 70)
    
    try:
        # Exemples
        exemple_basique()
        exemple_avance()
        exemple_multiple_loggers()
        exemple_performance()
        
        print("\n🎉 DÉMONSTRATION TERMINÉE AVEC SUCCÈS!")
        print("=" * 70)
        print("📖 Consultez le README.md pour plus d'informations")
        print("🔧 Configurations disponibles dans config/")
        print("🧪 Tests complets dans tests/")
        
    except Exception as e:
        print(f"❌ Erreur pendant la démonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 