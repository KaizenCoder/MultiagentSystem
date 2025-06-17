"""
Service de chiffrement pour protéger les données sensibles.

Ce module fournit des utilitaires pour :
- Chiffrement/déchiffrement des données sensibles
- Génération de clés sécurisées
- Hachage sécurisé des mots de passe
"""

import base64
import hashlib
import secrets
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionService:
    """Service de chiffrement pour les données sensibles."""
    
    def __init__(self, key: Optional[bytes] = None):
        """
        Initialise le service de chiffrement.
        
        Args:
            key: Clé de chiffrement (générée automatiquement si None)
        """
        if key:
            self.cipher = Fernet(key)
        else:
            # Générer une nouvelle clé
            self.cipher = Fernet(Fernet.generate_key())
    
    @staticmethod
    def generate_key() -> bytes:
        """
        Génère une nouvelle clé de chiffrement.
        
        Returns:
            bytes: Clé de chiffrement
        """
        return Fernet.generate_key()
    
    @staticmethod
    def derive_key_from_password(password: str, salt: Optional[bytes] = None) -> tuple[bytes, bytes]:
        """
        Dérive une clé de chiffrement à partir d'un mot de passe.
        
        Args:
            password: Mot de passe
            salt: Salt (généré automatiquement si None)
            
        Returns:
            tuple: (clé, salt)
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
        Chiffre des données.
        
        Args:
            data: Données à chiffrer
            
        Returns:
            str: Données chiffrées (base64)
        """
        encrypted_data = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Déchiffre des données.
        
        Args:
            encrypted_data: Données chiffrées (base64)
            
        Returns:
            str: Données déchiffrées
        """
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = self.cipher.decrypt(encrypted_bytes)
        return decrypted_data.decode()
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """
        Chiffre des données sensibles (alias pour encrypt_data).
        
        Args:
            data: Données sensibles à chiffrer
            
        Returns:
            str: Données chiffrées
        """
        return self.encrypt_data(data)
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """
        Déchiffre des données sensibles (alias pour decrypt_data).
        
        Args:
            encrypted_data: Données chiffrées
            
        Returns:
            str: Données déchiffrées
        """
        return self.decrypt_data(encrypted_data)


class SecureHasher:
    """Utilitaires pour le hachage sécurisé."""
    
    @staticmethod
    def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[str, str]:
        """
        Hache un mot de passe de manière sécurisée.
        
        Args:
            password: Mot de passe à hacher
            salt: Salt (généré automatiquement si None)
            
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
        Vérifie un mot de passe contre son hash.
        
        Args:
            password: Mot de passe à vérifier
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
        Hache des données avec SHA-256.
        
        Args:
            data: Données à hacher
            
        Returns:
            str: Hash en hexadécimal
        """
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Génère un token sécurisé.
        
        Args:
            length: Longueur du token en bytes
            
        Returns:
            str: Token en base64
        """
        token_bytes = secrets.token_bytes(length)
        return base64.urlsafe_b64encode(token_bytes).decode()


# Service global par défaut (utilise une clé générée)
default_encryption_service = EncryptionService()


def get_encryption_service(key: Optional[bytes] = None) -> EncryptionService:
    """
    Obtient une instance du service de chiffrement.
    
    Args:
        key: Clé de chiffrement (utilise le service par défaut si None)
        
    Returns:
        EncryptionService: Instance du service
    """
    if key:
        return EncryptionService(key)
    return default_encryption_service 