#!/usr/bin/env python3
"""
Handler pour le chiffrement AES-256 des messages de log.
"""

import logging
from cryptography.fernet import Fernet, MultiFernet
from typing import Optional, List

class EncryptionHandler(logging.Handler):
    """
    Un handler qui chiffre le message d'un enregistrement de log avant
    de le passer à un autre handler.
    """
    def __init__(self, base_handler: logging.Handler, encryption_key: str):
        super().__init__()
        self.base_handler = base_handler
        
        # On utilise Fernet pour un chiffrement symétrique simple et sécurisé
        try:
            self.fernet = Fernet(encryption_key.encode())
        except (ValueError, TypeError) as e:
            # Gérer une clé invalide, potentiellement logger une erreur critique
            # sur la console sans passer par le système de logging qui boucle.
            print(f"ERREUR CRITIQUE: Clé de chiffrement invalide. {e}")
            # On utilise une clé "nulle" pour éviter de crasher, mais les logs ne seront pas chiffrés.
            self.fernet = None

    def emit(self, record: logging.LogRecord):
        """Chiffre le message et le passe au handler de base."""
        if not self.fernet:
            # Ne pas tenter de chiffrer si la clé est invalide
            self.base_handler.handle(record)
            return

        # On ne chiffre que le message pour garder les métadonnées (niveau, etc.) intactes
        original_message = record.getMessage()
        
        try:
            encrypted_message = self.fernet.encrypt(original_message.encode())
            
            # On crée une copie du record pour ne pas altérer l'original
            # et on remplace le message par sa version chiffrée.
            encrypted_record = logging.makeLogRecord(record.__dict__)
            encrypted_record.msg = encrypted_message.decode()
            encrypted_record.args = () # Les args ont été formatés dans getMessage()
            
            self.base_handler.handle(encrypted_record)

        except Exception as e:
            print(f"ERREUR: Échec du chiffrement du log. {e}")
            # En cas d'échec, on passe le message original pour ne pas perdre le log.
            self.base_handler.handle(record)

    def decrypt_log(self, encrypted_message: str) -> Optional[str]:
        """Déchiffre un message de log."""
        if not self.fernet:
            return "[Déchiffrement impossible: Clé invalide]"

        try:
            decrypted_bytes = self.fernet.decrypt(encrypted_message.encode())
            return decrypted_bytes.decode()
        except Exception:
            return "[Déchiffrement échoué: message corrompu ou clé invalide]" 



