"""
Ce __init__.py transforme le répertoire 'core' en un package Python.

Il expose une instance unique (singleton) du LoggingManager,
le rendant facilement accessible dans toute l'application via :

from core import logging_manager
"""
from .manager import LoggingManager
from .logging_core import LoggingConfig, LogLevel

# Instance unique du manager de logging, accessible globalement.
# C'est le point d'entrée principal pour la bibliothèque de logging.
logging_manager = LoggingManager()

# Rendre les classes de configuration et les enums accessibles
__all__ = [
    "logging_manager",
    "LoggingConfig",
    "LogLevel"
] 