"""
Tests unitaires pour le module encryption.py
Objectif : 85% couverture (49% → 85%)
Sprint 2.2 - Tests & Qualité
"""

import pytest
import base64
import secrets
from unittest.mock import patch, Mock
from cryptography.fernet import Fernet, InvalidToken

from orchestrator.app.security.encryption import (
    EncryptionService,
    SecureHasher,
    get_encryption_service
)


@pytest.mark.unit
class TestEncryptionService:
    """Tests pour la classe EncryptionService."""
    
    @pytest.fixture
    def encryption_service(self):
        """Fixture pour service de chiffrement avec clé fixe."""
        # Utiliser une clé fixe pour tests reproductibles
        key = Fernet.generate_key()
        return EncryptionService(key)
    
    @pytest.fixture
    def encryption_service_auto_key(self):
        """Fixture pour service avec clé auto-générée."""
        return EncryptionService()
    
    def test_initialization_with_key(self):
        """Test initialisation avec clé fournie."""
        key = Fernet.generate_key()
        service = EncryptionService(key)
        
        assert service.cipher is not None
        assert isinstance(service.cipher, Fernet)
    
    def test_initialization_without_key(self, encryption_service_auto_key):
        """Test initialisation avec clé auto-générée."""
        service = encryption_service_auto_key
        
        assert service.cipher is not None
        assert isinstance(service.cipher, Fernet)
    
    def test_generate_key(self):
        """Test génération de clé."""
        key = EncryptionService.generate_key()
        
        assert isinstance(key, bytes)
        assert len(key) == 44  # Taille standard d'une clé Fernet en base64
        
        # Vérifier que deux clés générées sont différentes
        key2 = EncryptionService.generate_key()
        assert key != key2
    
    def test_derive_key_from_password_with_salt(self):
        """Test dérivation de clé avec salt fourni."""
        password = "test_password"
        salt = secrets.token_bytes(32)
        
        key, returned_salt = EncryptionService.derive_key_from_password(password, salt)
        
        assert isinstance(key, bytes)
        assert isinstance(returned_salt, bytes)
        assert returned_salt == salt
        assert len(key) == 44  # Clé Fernet en base64
    
    def test_derive_key_from_password_without_salt(self):
        """Test dérivation de clé avec salt auto-généré."""
        password = "test_password"
        
        key, salt = EncryptionService.derive_key_from_password(password)
        
        assert isinstance(key, bytes)
        assert isinstance(salt, bytes)
        assert len(salt) == 32  # Taille du salt
        assert len(key) == 44   # Clé Fernet en base64
    
    def test_derive_key_reproducible(self):
        """Test que la dérivation est reproductible avec même salt."""
        password = "test_password"
        salt = secrets.token_bytes(32)
        
        key1, _ = EncryptionService.derive_key_from_password(password, salt)
        key2, _ = EncryptionService.derive_key_from_password(password, salt)
        
        assert key1 == key2
    
    def test_encrypt_decrypt_data(self, encryption_service):
        """Test chiffrement et déchiffrement de données."""
        service = encryption_service
        original_data = "Données sensibles à chiffrer"
        
        # Chiffrement
        encrypted_data = service.encrypt_data(original_data)
        
        assert isinstance(encrypted_data, str)
        assert encrypted_data != original_data
        assert len(encrypted_data) > len(original_data)  # Overhead du chiffrement
        
        # Déchiffrement
        decrypted_data = service.decrypt_data(encrypted_data)
        
        assert decrypted_data == original_data
    
    def test_encrypt_empty_string(self, encryption_service):
        """Test chiffrement de chaîne vide."""
        service = encryption_service
        
        encrypted = service.encrypt_data("")
        decrypted = service.decrypt_data(encrypted)
        
        assert decrypted == ""
    
    def test_encrypt_unicode_data(self, encryption_service):
        """Test chiffrement de données Unicode."""
        service = encryption_service
        unicode_data = "Données avec émojis 🔒🛡️ et caractères spéciaux àéîôù"
        
        encrypted = service.encrypt_data(unicode_data)
        decrypted = service.decrypt_data(encrypted)
        
        assert decrypted == unicode_data
    
    def test_encrypt_large_data(self, encryption_service):
        """Test chiffrement de grandes quantités de données."""
        service = encryption_service
        large_data = "A" * 10000  # 10KB de données
        
        encrypted = service.encrypt_data(large_data)
        decrypted = service.decrypt_data(encrypted)
        
        assert decrypted == large_data
    
    def test_decrypt_invalid_data(self, encryption_service):
        """Test déchiffrement de données invalides."""
        service = encryption_service
        
        with pytest.raises(Exception):  # Peut être InvalidToken ou autre
            service.decrypt_data("invalid_encrypted_data")
    
    def test_decrypt_corrupted_data(self, encryption_service):
        """Test déchiffrement de données corrompues."""
        service = encryption_service
        original_data = "Test data"
        
        encrypted = service.encrypt_data(original_data)
        
        # Corrompre les données
        corrupted = encrypted[:-1] + "X"
        
        with pytest.raises(Exception):
            service.decrypt_data(corrupted)
    
    def test_encrypt_sensitive_data_alias(self, encryption_service):
        """Test que encrypt_sensitive_data est un alias."""
        service = encryption_service
        data = "Données sensibles"
        
        encrypted1 = service.encrypt_data(data)
        encrypted2 = service.encrypt_sensitive_data(data)
        
        # Les résultats peuvent être différents (random IV)
        # mais les deux doivent se déchiffrer correctement
        assert service.decrypt_data(encrypted1) == data
        assert service.decrypt_sensitive_data(encrypted2) == data
    
    def test_decrypt_sensitive_data_alias(self, encryption_service):
        """Test que decrypt_sensitive_data est un alias."""
        service = encryption_service
        data = "Données sensibles"
        
        encrypted = service.encrypt_data(data)
        
        decrypted1 = service.decrypt_data(encrypted)
        decrypted2 = service.decrypt_sensitive_data(encrypted)
        
        assert decrypted1 == decrypted2 == data
    
    def test_different_services_different_results(self):
        """Test que différents services produisent des résultats différents."""
        service1 = EncryptionService()
        service2 = EncryptionService()
        
        data = "Same data"
        
        encrypted1 = service1.encrypt_data(data)
        encrypted2 = service2.encrypt_data(data)
        
        # Clés différentes = résultats différents
        assert encrypted1 != encrypted2
        
        # Mais chaque service peut déchiffrer ses propres données
        assert service1.decrypt_data(encrypted1) == data
        assert service2.decrypt_data(encrypted2) == data
        
        # Et ne peut pas déchiffrer les données de l'autre
        with pytest.raises(Exception):
            service1.decrypt_data(encrypted2)
        with pytest.raises(Exception):
            service2.decrypt_data(encrypted1)


@pytest.mark.unit
class TestSecureHasher:
    """Tests pour la classe SecureHasher."""
    
    def test_hash_password_with_salt(self):
        """Test hachage de mot de passe avec salt fourni."""
        password = "test_password"
        salt = secrets.token_bytes(32)
        salt_b64 = base64.urlsafe_b64encode(salt).decode('ascii')
        
        hash_b64, returned_salt_b64 = SecureHasher.hash_password(password, salt)
        
        assert isinstance(hash_b64, str)
        assert isinstance(returned_salt_b64, str)
        assert returned_salt_b64 == salt_b64
        assert len(hash_b64) > 0
        assert hash_b64 != password
    
    def test_hash_password_without_salt(self):
        """Test hachage de mot de passe avec salt auto-généré."""
        password = "test_password"
        
        hash_b64, salt_b64 = SecureHasher.hash_password(password)
        
        assert isinstance(hash_b64, str)
        assert isinstance(salt_b64, str)
        assert len(hash_b64) > 0
        assert len(salt_b64) > 0
        assert hash_b64 != password
        assert salt_b64 != password
    
    def test_hash_password_reproducible(self):
        """Test que le hachage est reproductible avec même salt."""
        password = "test_password"
        salt = secrets.token_bytes(32)
        
        hash1, _ = SecureHasher.hash_password(password, salt)
        hash2, _ = SecureHasher.hash_password(password, salt)
        
        assert hash1 == hash2
    
    def test_hash_password_different_salts(self):
        """Test que des salts différents produisent des hashs différents."""
        password = "test_password"
        
        hash1, salt1 = SecureHasher.hash_password(password)
        hash2, salt2 = SecureHasher.hash_password(password)
        
        assert hash1 != hash2
        assert salt1 != salt2
    
    def test_verify_password_correct(self):
        """Test vérification de mot de passe correct."""
        password = "test_password"
        hash_b64, salt_b64 = SecureHasher.hash_password(password)
        
        result = SecureHasher.verify_password(password, hash_b64, salt_b64)
        
        assert result is True
    
    def test_verify_password_incorrect(self):
        """Test vérification de mot de passe incorrect."""
        password = "test_password"
        wrong_password = "wrong_password"
        hash_b64, salt_b64 = SecureHasher.hash_password(password)
        
        result = SecureHasher.verify_password(wrong_password, hash_b64, salt_b64)
        
        assert result is False
    
    def test_verify_password_invalid_hash(self):
        """Test vérification avec hash invalide."""
        password = "test_password"
        invalid_hash = "invalid_hash"
        salt_b64 = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('ascii')
        
        result = SecureHasher.verify_password(password, invalid_hash, salt_b64)
        
        assert result is False
    
    def test_verify_password_invalid_salt(self):
        """Test vérification avec salt invalide."""
        password = "test_password"
        hash_b64, _ = SecureHasher.hash_password(password)
        invalid_salt = "invalid_salt"
        
        result = SecureHasher.verify_password(password, hash_b64, invalid_salt)
        
        assert result is False
    
    def test_verify_password_empty_inputs(self):
        """Test vérification avec entrées vides."""
        assert SecureHasher.verify_password("", "", "") is False
        assert SecureHasher.verify_password("password", "", "") is False
        assert SecureHasher.verify_password("", "hash", "salt") is False
    
    def test_hash_data_sha256(self):
        """Test hachage de données avec SHA-256."""
        data = "Test data to hash"
        
        hash_hex = SecureHasher.hash_data(data)
        
        assert isinstance(hash_hex, str)
        assert len(hash_hex) == 64  # SHA-256 produit 64 caractères hex
        assert hash_hex != data
        
        # Test reproductibilité
        hash_hex2 = SecureHasher.hash_data(data)
        assert hash_hex == hash_hex2
    
    def test_hash_data_different_inputs(self):
        """Test hachage de données différentes."""
        data1 = "First data"
        data2 = "Second data"
        
        hash1 = SecureHasher.hash_data(data1)
        hash2 = SecureHasher.hash_data(data2)
        
        assert hash1 != hash2
    
    def test_hash_data_empty_string(self):
        """Test hachage de chaîne vide."""
        hash_hex = SecureHasher.hash_data("")
        
        assert isinstance(hash_hex, str)
        assert len(hash_hex) == 64
        # Hash SHA-256 de chaîne vide est connu
        assert hash_hex == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    
    def test_hash_data_unicode(self):
        """Test hachage de données Unicode."""
        unicode_data = "Données avec émojis 🔒 et caractères spéciaux àéîôù"
        
        hash_hex = SecureHasher.hash_data(unicode_data)
        
        assert isinstance(hash_hex, str)
        assert len(hash_hex) == 64
    
    def test_generate_secure_token_default_length(self):
        """Test génération de token sécurisé avec longueur par défaut."""
        token = SecureHasher.generate_secure_token()
        
        assert isinstance(token, str)
        # Base64 encoding d'un token de 32 bytes
        assert len(token) >= 40  # Au moins 40 caractères pour 32 bytes
    
    def test_generate_secure_token_custom_length(self):
        """Test génération de token sécurisé avec longueur personnalisée."""
        length = 64
        token = SecureHasher.generate_secure_token(length)
        
        assert isinstance(token, str)
        # Base64 encoding d'un token de 64 bytes
        assert len(token) >= 80  # Au moins 80 caractères pour 64 bytes
    
    def test_generate_secure_token_uniqueness(self):
        """Test que les tokens générés sont uniques."""
        tokens = [SecureHasher.generate_secure_token() for _ in range(100)]
        
        # Tous les tokens doivent être uniques
        assert len(set(tokens)) == 100
    
    def test_generate_secure_token_small_length(self):
        """Test génération de token avec petite longueur."""
        token = SecureHasher.generate_secure_token(1)
        
        assert isinstance(token, str)
        assert len(token) >= 1


@pytest.mark.unit
class TestEncryptionServiceIntegration:
    """Tests d'intégration pour EncryptionService."""
    
    def test_encrypt_decrypt_with_derived_key(self):
        """Test chiffrement/déchiffrement avec clé dérivée."""
        password = "strong_password_123"
        key, salt = EncryptionService.derive_key_from_password(password)
        
        service = EncryptionService(key)
        data = "Données sensibles à protéger"
        
        encrypted = service.encrypt_data(data)
        decrypted = service.decrypt_data(encrypted)
        
        assert decrypted == data
    
    def test_multiple_encryption_cycles(self):
        """Test plusieurs cycles de chiffrement/déchiffrement."""
        service = EncryptionService()
        original_data = "Test data for multiple cycles"
        
        # 10 cycles
        current_data = original_data
        for _ in range(10):
            encrypted = service.encrypt_data(current_data)
            current_data = service.decrypt_data(encrypted)
        
        assert current_data == original_data
    
    def test_password_and_encryption_integration(self):
        """Test intégration hachage de mot de passe et chiffrement."""
        password = "user_password"
        sensitive_data = "User sensitive information"
        
        # Hacher le mot de passe
        pwd_hash, salt = SecureHasher.hash_password(password)
        
        # Utiliser le mot de passe pour dériver une clé de chiffrement
        enc_key, enc_salt = EncryptionService.derive_key_from_password(password)
        
        # Chiffrer les données sensibles
        service = EncryptionService(enc_key)
        encrypted_data = service.encrypt_data(sensitive_data)
        
        # Vérifier le mot de passe
        assert SecureHasher.verify_password(password, pwd_hash, salt)
        
        # Déchiffrer les données
        decrypted_data = service.decrypt_data(encrypted_data)
        assert decrypted_data == sensitive_data


@pytest.mark.unit
class TestEncryptionServiceGlobalInstance:
    """Tests pour l'instance globale d'EncryptionService."""
    
    def test_get_encryption_service_default(self):
        """Test récupération service par défaut."""
        service = get_encryption_service()
        
        assert isinstance(service, EncryptionService)
        assert service.cipher is not None
    
    def test_get_encryption_service_with_key(self):
        """Test récupération service avec clé spécifiée."""
        key = Fernet.generate_key()
        service = get_encryption_service(key)
        
        assert isinstance(service, EncryptionService)
        assert service.cipher is not None
    
    def test_get_encryption_service_singleton_behavior(self):
        """Test comportement singleton."""
        # Reset global instance pour ce test
        import orchestrator.app.security.encryption
        original_instance = getattr(orchestrator.app.security.encryption, '_encryption_service', None)
        
        try:
            orchestrator.app.security.encryption._encryption_service = None
            
            service1 = get_encryption_service()
            service2 = get_encryption_service()
            
            # Même instance retournée
            assert service1 is service2
            
        finally:
            # Restaurer l'instance originale
            if original_instance:
                orchestrator.app.security.encryption._encryption_service = original_instance


@pytest.mark.unit
class TestEncryptionEdgeCases:
    """Tests pour les cas limites."""
    
    def test_encryption_with_very_long_password(self):
        """Test dérivation de clé avec mot de passe très long."""
        very_long_password = "a" * 10000  # 10KB mot de passe
        
        key, salt = EncryptionService.derive_key_from_password(very_long_password)
        
        assert isinstance(key, bytes)
        assert isinstance(salt, bytes)
        assert len(key) == 44  # Toujours même longueur de clé
    
    def test_encryption_special_characters(self):
        """Test chiffrement avec caractères spéciaux."""
        special_data = "!@#$%^&*()_+-=[]{}|;':\",./<>?\n\t\r"
        
        service = EncryptionService()
        encrypted = service.encrypt_data(special_data)
        decrypted = service.decrypt_data(encrypted)
        
        assert decrypted == special_data
    
    def test_base64_padding_edge_cases(self):
        """Test cas limites de padding base64."""
        service = EncryptionService()
        
        # Données de différentes longueurs pour tester padding
        test_data = ["a", "ab", "abc", "abcd", "abcde"]
        
        for data in test_data:
            encrypted = service.encrypt_data(data)
            decrypted = service.decrypt_data(encrypted)
            assert decrypted == data
    
    def test_concurrent_encryption_safety(self):
        """Test sécurité en accès concurrent."""
        import threading
        
        service = EncryptionService()
        results = {}
        
        def encrypt_data(thread_id):
            data = f"Thread {thread_id} data"
            encrypted = service.encrypt_data(data)
            decrypted = service.decrypt_data(encrypted)
            results[thread_id] = (data, decrypted)
        
        # Lancer 10 threads concurrents
        threads = []
        for i in range(10):
            thread = threading.Thread(target=encrypt_data, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Attendre tous les threads
        for thread in threads:
            thread.join()
        
        # Vérifier que tous les résultats sont corrects
        for thread_id, (original, decrypted) in results.items():
            assert original == decrypted
    
    def test_memory_cleanup(self):
        """Test nettoyage mémoire après utilisation."""
        import gc
        
        # Créer et utiliser plusieurs services
        for _ in range(100):
            service = EncryptionService()
            data = "Test data for memory cleanup"
            encrypted = service.encrypt_data(data)
            decrypted = service.decrypt_data(encrypted)
            assert decrypted == data
        
        # Forcer le garbage collection
        gc.collect()
        
        # Ce test vérifie surtout qu'il n'y a pas de fuite mémoire évidente
        # L'assertion principale est que le code s'exécute sans erreur 