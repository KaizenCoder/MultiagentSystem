#!/usr/bin/env python3
"""
Handler pour envoyer les logs à une instance Elasticsearch.
"""

import logging
import datetime
import os
from elasticsearch import Elasticsearch, exceptions
from typing import Dict, Any
from dotenv import load_dotenv, find_dotenv

class ElasticsearchHandler(logging.Handler):
    """
    Un handler qui formate les logs en JSON et les envoie à Elasticsearch.
    """
    def __init__(self, es_hosts: list, index_name_pattern: str = "nextgen-logs-%Y.%m.%d"):
        super().__init__()
        self.index_name_pattern = index_name_pattern
        self.es_client = None

        env_path = find_dotenv(usecwd=True)
        if env_path:
            print(f"INFO: ElasticsearchHandler - Fichier .env trouvé à: {env_path}. Chargement des variables.")
            load_dotenv(dotenv_path=env_path)
        else:
            print(f"INFO: ElasticsearchHandler - Aucun fichier .env trouvé dans le répertoire courant ou les répertoires parents.")

        api_key_value = os.environ.get("ELASTIC_SEARCH_API_KEY")
        client_params: Dict[str, Any] = {"hosts": es_hosts}

        if api_key_value:
            print(f"INFO: ElasticsearchHandler - Clé API ELASTIC_SEARCH_API_KEY trouvée dans l'environnement. Tentative de connexion avec clé API.")
            client_params["api_key"] = api_key_value
        else:
            print(f"INFO: ElasticsearchHandler - Clé API ELASTIC_SEARCH_API_KEY non trouvée dans l'environnement. Tentative de connexion sans clé API.")

        try:
            temp_client = Elasticsearch(**client_params)
            
            if temp_client.ping():
                print(f"INFO: ElasticsearchHandler - Ping vers Elasticsearch ({es_hosts}) réussi.")
                self.es_client = temp_client
                if api_key_value:
                    print("INFO: ElasticsearchHandler - Connexion à Elasticsearch établie AVEC clé API.")
                else:
                    print("INFO: ElasticsearchHandler - Connexion à Elasticsearch établie SANS clé API.")
            else:
                print(f"AVERTISSEMENT: ElasticsearchHandler - Ping vers Elasticsearch ({es_hosts}) a échoué bien que le client ait été initialisé. L'envoi des logs sera désactivé.")
                self.es_client = None
        except exceptions.AuthenticationException as e:
            print(f"ERREUR D'AUTHENTIFICATION: ElasticsearchHandler - Impossible de s'authentifier auprès d'Elasticsearch ({es_hosts}): {e}")
            if api_key_value:
                print("ERREUR D'AUTHENTIFICATION: ElasticsearchHandler - La clé API ELASTIC_SEARCH_API_KEY pourrait être incorrecte ou ne pas avoir les permissions nécessaires.")
            self.es_client = None
        except exceptions.ConnectionError as e:
            print(f"ERREUR DE CONNEXION: ElasticsearchHandler - Impossible de se connecter à Elasticsearch ({es_hosts}): {e}")
            self.es_client = None
        except Exception as e:
            print(f"ERREUR INATTENDUE: ElasticsearchHandler - Erreur lors de l'initialisation du client Elasticsearch ({es_hosts}): {e}")
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
            print(f"ERREUR: ElasticsearchHandler - Échec de l'envoi du log à Elasticsearch: {e}")

    def close(self):
        """Ferme le client Elasticsearch."""
        if self.es_client:
            try:
                self.es_client.close()
                print("INFO: ElasticsearchHandler - Client Elasticsearch fermé proprement.")
            except Exception as e:
                print(f"ERREUR: ElasticsearchHandler - Erreur lors de la fermeture du client Elasticsearch: {e}")
        super().close() 



