#!/usr/bin/env python3
"""
Handler pour l'écriture des logs dans des fichiers avec rotation et compression.
"""

import logging
import logging.handlers
import gzip
import shutil
from pathlib import Path
from typing import Optional
from ..logging_core import LoggingConfig
from datetime import datetime

class CompressingRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """
    Handler de rotation qui compresse le fichier de log après la rotation.
    """
    def __init__(self, *args, compression_enabled=True, **kwargs):
        self.compression_enabled = compression_enabled
        super().__init__(*args, **kwargs)

    def doRollover(self):
        """Effectue la rotation et la compression."""
        super().doRollover()
        if not self.compression_enabled:
            return

        log_path = Path(self.baseFilename).parent
        for f in log_path.glob(f"{Path(self.baseFilename).name}.*"):
            if not f.name.endswith(".gz"):
                self._compress_file(f)

    def _compress_file(self, filepath: Path):
        """Compresse un fichier avec gzip."""
        try:
            with open(filepath, 'rb') as f_in:
                with gzip.open(f"{filepath}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            filepath.unlink()  # Supprime le fichier source
        except Exception as e:
            # Gérer l'erreur, par exemple, en loggant sur la console
            print(f"Erreur de compression: {e}")

class FileHandler:
    """Gère la création d'un handler de fichier."""

    @staticmethod
    def create(config: LoggingConfig) -> Optional[logging.Handler]:
        """
        Crée et configure un handler pour les fichiers de log.

        Args:
            config (LoggingConfig): La configuration du logger.

        Returns:
            Optional[logging.Handler]: Le handler de fichier, ou None si désactivé.
        """
        if not config.file_enabled:
            return None

        log_dir = Path(config.log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Remplacer les placeholders dans le nom de fichier
        filename = config.filename_pattern.format(
            component=config.logger_name.split('.')[-1],
            date=datetime.now().strftime('%Y-%m-%d')
        )
        log_file = log_dir / filename

        handler = CompressingRotatingFileHandler(
            filename=log_file,
            maxBytes=config.max_file_size,
            backupCount=config.backup_count,
            encoding='utf-8',
            compression_enabled=config.compression_enabled
        )
        
        formatter = logging.Formatter(config.format_string)
        handler.setFormatter(formatter)
        handler.setLevel(config.log_level)
        
        return handler 



