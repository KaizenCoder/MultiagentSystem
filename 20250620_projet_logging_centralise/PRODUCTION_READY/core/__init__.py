#!/usr/bin/env python3
"""
NextGeneration Logging Centralisé - Core Package
Version Production Ready 1.0.0

Ce package contient les composants principaux du système de logging centralisé.
"""

from .logging_manager_optimized import LoggingManager

__version__ = "1.0.0"
__author__ = "NextGeneration Team"
__description__ = "Système de logging centralisé enterprise-grade"

# Export principal
__all__ = ["LoggingManager"]

# Configuration par défaut
DEFAULT_CONFIG = {
    "logger_name": "nextgen.default",
    "log_level": "INFO",
    "enable_console": True,
    "enable_file": True,
    "enable_rotation": True
}

def get_default_logger():
    """
    Retourne un logger avec la configuration par défaut.
    
    Returns:
        logging.Logger: Logger configuré
    """
    manager = LoggingManager()
    return manager.get_logger(custom_config=DEFAULT_CONFIG)

def quick_setup(app_name: str, log_level: str = "INFO"):
    """
    Configuration rapide pour une application.
    
    Args:
        app_name (str): Nom de l'application
        log_level (str): Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        logging.Logger: Logger configuré pour l'application
    """
    config = DEFAULT_CONFIG.copy()
    config["logger_name"] = f"nextgen.{app_name}"
    config["log_level"] = log_level
    
    manager = LoggingManager()
    return manager.get_logger(custom_config=config) 