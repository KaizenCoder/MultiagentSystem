#!/usr/bin/env python3
"""
Handler pour l'affichage des logs sur la console (stdout).
"""

import logging
from ..logging_core import LoggingConfig

class ConsoleHandler:
    """Gère la création d'un handler de console."""

    @staticmethod
    def create(config: LoggingConfig) -> logging.Handler:
        """
        Crée et configure un handler pour la sortie console.

        Args:
            config (LoggingConfig): La configuration du logger.

        Returns:
            logging.Handler: Le handler de console configuré.
        """
        console_handler = logging.StreamHandler()
        
        formatter = logging.Formatter(config.format_string)
        console_handler.setFormatter(formatter)
        
        console_handler.setLevel(config.log_level)
        
        return console_handler 



