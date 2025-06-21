#!/usr/bin/env python3
"""
Handler pour envoyer les logs à une instance Elasticsearch.
"""

import logging
import datetime
from elasticsearch import Elasticsearch, exceptions
from typing import Dict, Any

class ElasticsearchHandler(logging.Handler):
    """
    Un handler qui formate les logs en JSON et les envoie à Elasticsearch.
    """
    def __init__(self, es_hosts: list, index_name_pattern: str = "nextgen-logs-%Y.%m.%d"):
        super().__init__()
        self.index_name_pattern = index_name_pattern
        try:
            self.es_client = Elasticsearch(hosts=es_hosts)
            # Tenter une connexion pour valider rapidement la configuration
            if not self.es_client.ping():
                raise ConnectionError("Ping vers Elasticsearch a échoué.")
        except exceptions.ConnectionError as e:
            print(f"ERREUR CRITIQUE: Impossible de se connecter à Elasticsearch: {e}")
            self.es_client = None

    def get_index_name(self) -> str:
        """Génère le nom de l'index basé sur la date actuelle."""
        return datetime.datetime.now().strftime(self.index_name_pattern)

    def format_record(self, record: logging.LogRecord) -> Dict[str, Any]:
        """Formate l'enregistrement de log en un dictionnaire JSON."""
        log_document = {
            "@timestamp": datetime.datetime.fromtimestamp(record.created).isoformat(),
            "message": record.getMessage(),
            "level": record.levelname,
            "logger_name": record.name,
            "category": getattr(record, 'category', 'general'),
            "details": {
                "process": record.process,
                "thread": record.thread,
                "filename": record.filename,
                "lineno": record.lineno,
            }
        }
        return log_document

    def emit(self, record: logging.LogRecord):
        """Envoie le log formaté à Elasticsearch."""
        if not self.es_client:
            return

        log_document = self.format_record(record)
        index_name = self.get_index_name()

        try:
            self.es_client.index(index=index_name, document=log_document)
        except exceptions.ElasticsearchException as e:
            print(f"ERREUR: Échec de l'envoi du log à Elasticsearch: {e}")

    def close(self):
        """Ferme le client Elasticsearch."""
        if self.es_client:
            try:
                self.es_client.close()
            except Exception as e:
                print(f"ERREUR lors de la fermeture du client Elasticsearch: {e}")
        super().close() 



