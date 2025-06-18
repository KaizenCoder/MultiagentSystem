"""
Service de chiffrement pour protger les donnes sensibles.

Ce module fournit des utilitaires pour :
- Chiffrement/dchiffrement des donnes sensibles
- Gnration de cls scurises
- Hachage scuris des mots de passe
"""

import base64
import hashlib
import secrets
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionService:
    """Service de chiffrement pour les donnes sensibles."""
    
    def __init__(self, key: Optional[bytes] = None):
        """
        Initialise le service de chiffrement.
        
        Args:
            key: Cl de chiffrement (gnre automatiquement si None)
        """
        if key:
            self.cipher = Fernet(key)
        else:
            # Gnrer une nouvelle cl
            self.cipher = Fernet(Fernet.generate_key())
    
    @staticmethod
    def generate_key() -> bytes:
        """
        Gnre une nouvelle cl de chiffrement.
        
        Returns:
            bytes: Cl de chiffrement
        """
        return Fernet.generate_key()
    
    @staticmethod
    def derive_key_from_password(password: str, salt: Optional[bytes] = None) -> tuple[bytes, bytes]:
        """
        Drive une cl de chiffrement  partir d'un mot de passe.
        
        Args:
            password: Mot de passe
            salt: Salt (gnr automatiquement si None)
            
        Returns:
            tuple: (cl, salt)
        """
        if salt is None:
            salt = secrets.token_bytes(32)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def encrypt_data(self, data: str) -> str:
        """
        Chiffre des donnes.
        
        Args:
            data: Donnes  chiffrer
            
        Returns:
            str: Donnes chiffres (base64)
        """
        encrypted_data = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Dchiffre des donnes.
        
        Args:
            encrypted_data: Donnes chiffres (base64)
            
        Returns:
            str: Donnes dchiffres
        """
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = self.cipher.decrypt(encrypted_bytes)
        return decrypted_data.decode()
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """
        Chiffre des donnes sensibles (alias pour encrypt_data).
        
        Args:
            data: Donnes sensibles  chiffrer
            
        Returns:
            str: Donnes chiffres
        """
        return self.encrypt_data(data)
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """
        Dchiffre des donnes sensibles (alias pour decrypt_data).
        
        Args:
            encrypted_data: Donnes chiffres
            
        Returns:
            str: Donnes dchiffres
        """
        return self.decrypt_data(encrypted_data)


class SecureHasher:
    """Utilitaires pour le hachage scuris."""
    
    @staticmethod
    def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[str, str]:
        """
        Hache un mot de passe de manire scurise.
        
        Args:
            password: Mot de passe  hacher
            salt: Salt (gnr automatiquement si None)
            
        Returns:
            tuple: (hash, salt) en format base64
        """
        if salt is None:
            salt = secrets.token_bytes(32)
        
        # Utiliser PBKDF2 avec SHA-256
        pwdhash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000  # 100k iterations
        )
        
        return (
            base64.urlsafe_b64encode(pwdhash).decode('ascii'),
            base64.urlsafe_b64encode(salt).decode('ascii')
        )
    
    @staticmethod
    def verify_password(password: str, hash_b64: str, salt_b64: str) -> bool:
        """
        Vrifie un mot de passe contre son hash.
        
        Args:
            password: Mot de passe  vrifier
            hash_b64: Hash en base64
            salt_b64: Salt en base64
            
        Returns:
            bool: True si le mot de passe est correct
        """
        try:
            salt = base64.urlsafe_b64decode(salt_b64.encode('ascii'))
            stored_hash = base64.urlsafe_b64decode(hash_b64.encode('ascii'))
            
            pwdhash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                100000
            )
            
            return secrets.compare_digest(pwdhash, stored_hash)
        except Exception:
            return False
    
    @staticmethod
    def hash_data(data: str) -> str:
        """
        Hache des donnes avec SHA-256.
        
        Args:
            data: Donnes  hacher
            
        Returns:
            str: Hash en hexadcimal
        """
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Gnre un token scuris.
        
        Args:
            length: Longueur du token en bytes
            
        Returns:
            str: Token en base64
        """
        token_bytes = secrets.token_bytes(length)
        return base64.urlsafe_b64encode(token_bytes).decode()


# Service global par dfaut (utilise une cl gnre)
default_encryption_service = EncryptionService()


def get_encryption_service(key: Optional[bytes] = None) -> EncryptionService:
    """
    Obtient une instance du service de chiffrement.
    
    Args:
        key: Cl de chiffrement (utilise le service par dfaut si None)
        
    Returns:
        EncryptionService: Instance du service
    """
    if key:
        return EncryptionService(key)
    return default_encryption_service 