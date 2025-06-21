#!/usr/bin/env python3
"""
Exemple d'utilisation basique - NextGeneration Logging
=====================================================

Cet exemple montre comment utiliser le système NextGeneration 
pour des cas d'usage simples et courants.
"""

import sys
import os

# Ajouter le chemin parent pour l'import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logging_manager_nextgen import NextGenLoggingManager, get_logger, get_agent_logger, log_performance

def example_basic_logging():
    """Exemple 1: Logging basique"""
    print("🔹 Exemple 1: Logging basique")
    
    # Obtenir un logger simple
    logger = get_logger("mon_application")
    
    # Messages de différents niveaux
    logger.debug("Message de debug - détails techniques")
    logger.info("Application démarrée avec succès")
    logger.warning("Attention: configuration par défaut utilisée")
    logger.error("Erreur de connexion à la base de données")
    logger.critical("Erreur critique: mémoire insuffisante")
    
    print("✅ Logging basique terminé\n")

def example_agent_logging():
    """Exemple 2: Logging pour agent IA"""
    print("🔹 Exemple 2: Logging pour agent IA")
    
    # Logger spécialisé pour agent
    agent_logger = get_agent_logger(
        agent_name="MonAgentIA",
        role="ai_processor",
        domain="nlp",
        agent_id="agent_001"
    )
    
    # Messages spécialisés agent
    agent_logger.info("🤖 Agent IA initialisé")
    agent_logger.info("📝 Traitement du document: rapport_mensuel.pdf")
    agent_logger.warning("⚠️ Confiance faible pour cette prédiction: 0.65")
    agent_logger.info("✅ Traitement terminé - 1,234 tokens analysés")
    
    print("✅ Logging agent IA terminé\n")

def example_performance_monitoring():
    """Exemple 3: Monitoring de performance"""
    print("🔹 Exemple 3: Monitoring de performance")
    
    logger = get_logger("performance_app")
    
    # Mesurer une opération
    with log_performance("traitement_donnees", logger):
        # Simulation d'une opération
        import time
        time.sleep(0.1)
        logger.info("Traitement de 10,000 enregistrements")
    
    # Mesurer une autre opération
    with log_performance("requete_api", logger):
        time.sleep(0.05)
        logger.info("Appel API externe réussi")
    
    print("✅ Monitoring de performance terminé\n")

def example_custom_configuration():
    """Exemple 4: Configuration personnalisée"""
    print("🔹 Exemple 4: Configuration personnalisée")
    
    manager = NextGenLoggingManager()
    
    # Configuration personnalisée
    custom_config = {
        "logger_name": "mon_service_critique",
        "log_level": "DEBUG",
        "async_enabled": True,
        "elasticsearch_enabled": True,
        "encryption_enabled": True,
        "alerting_enabled": True,
        "sensitive_data_masking": True,
        "metadata": {
            "service": "payment_processor",
            "version": "2.1.0",
            "environment": "production"
        }
    }
    
    logger = manager.get_logger(custom_config=custom_config)
    
    # Test avec données sensibles (seront chiffrées automatiquement)
    logger.info("Utilisateur connecté: john.doe@company.com")
    logger.warning("Tentative de connexion avec token invalide: abc123...")
    logger.info("Transaction validée pour le montant: 150.00 EUR")
    
    print("✅ Configuration personnalisée terminée\n")

def example_error_handling():
    """Exemple 5: Gestion d'erreurs avancée"""
    print("🔹 Exemple 5: Gestion d'erreurs avancée")
    
    logger = get_logger("error_handling_app")
    
    try:
        # Simulation d'une erreur
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.error(f"Erreur de division par zéro: {e}")
        logger.debug(f"Stack trace complète", exc_info=True)
    
    try:
        # Simulation d'une autre erreur
        data = {"key": "value"}
        value = data["missing_key"]
    except KeyError as e:
        logger.error(f"Clé manquante dans les données: {e}")
        logger.info("Utilisation de la valeur par défaut")
    
    # Erreur critique
    logger.critical("Système en état critique - arrêt imminent")
    
    print("✅ Gestion d'erreurs terminée\n")

def example_metrics_collection():
    """Exemple 6: Collecte de métriques"""
    print("🔹 Exemple 6: Collecte de métriques")
    
    manager = NextGenLoggingManager()
    logger = get_logger("metrics_app")
    
    # Générer quelques logs pour les métriques
    for i in range(10):
        logger.info(f"Traitement élément {i+1}/10")
        if i % 3 == 0:
            logger.warning(f"Avertissement pour élément {i+1}")
        if i == 7:
            logger.error("Erreur temporaire - retry automatique")
    
    # Obtenir les métriques
    metrics = manager.get_metrics()
    
    print("📊 Métriques collectées:")
    print(f"   • Total logs: {metrics['core_metrics']['total_logs']}")
    print(f"   • Logs INFO: {metrics['core_metrics']['logs_per_level']['INFO']}")
    print(f"   • Logs WARNING: {metrics['core_metrics']['logs_per_level']['WARNING']}")
    print(f"   • Logs ERROR: {metrics['core_metrics']['logs_per_level']['ERROR']}")
    print(f"   • Loggers actifs: {metrics['system_health']['active_loggers']}")
    print(f"   • Usage mémoire: {metrics['system_health']['memory_usage_mb']:.1f} MB")
    
    print("✅ Collecte de métriques terminée\n")

def example_multiple_loggers():
    """Exemple 7: Gestion de multiples loggers"""
    print("🔹 Exemple 7: Multiples loggers spécialisés")
    
    # Logger pour l'API
    api_logger = get_logger("api_service")
    
    # Logger pour la base de données
    db_logger = get_logger("database_service")
    
    # Logger pour l'authentification
    auth_logger = get_logger("auth_service")
    
    # Simulation d'activité
    api_logger.info("🌐 Serveur API démarré sur le port 8080")
    db_logger.info("🗄️ Connexion à la base de données établie")
    auth_logger.info("🔐 Service d'authentification initialisé")
    
    # Simulation d'une requête
    api_logger.info("📥 Requête reçue: GET /api/users")
    auth_logger.info("🔍 Validation du token JWT")
    db_logger.debug("🔎 Exécution requête: SELECT * FROM users")
    db_logger.info("📤 Résultats retournés: 25 utilisateurs")
    api_logger.info("📤 Réponse envoyée: 200 OK")
    
    print("✅ Multiples loggers terminé\n")

def main():
    """Fonction principale - exécute tous les exemples"""
    print("🚀 NextGeneration Logging - Exemples d'utilisation")
    print("=" * 60)
    
    # Exécuter tous les exemples
    example_basic_logging()
    example_agent_logging()
    example_performance_monitoring()
    example_custom_configuration()
    example_error_handling()
    example_metrics_collection()
    example_multiple_loggers()
    
    print("🎉 Tous les exemples terminés avec succès!")
    print("\n📋 Résumé:")
    print("   • Logging basique ✅")
    print("   • Agents IA ✅")
    print("   • Performance monitoring ✅")
    print("   • Configuration personnalisée ✅")
    print("   • Gestion d'erreurs ✅")
    print("   • Collecte de métriques ✅")
    print("   • Multiples loggers ✅")
    
    print("\n🔍 Vérifiez les fichiers de logs dans le répertoire 'logs/'")
    print("📊 Les métriques sont sauvegardées dans 'logs/metrics.json'")

if __name__ == "__main__":
    main() 



