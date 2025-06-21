#!/usr/bin/env python3
"""
🔒 Test Sécurité Renforcée - Phase 3 ChatGPT
Validation de la rotation automatique des clés de chiffrement et détection améliorée
"""

import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

# Ajout du chemin pour les imports
sys.path.append(str(Path(__file__).parent))

class TestEnhancedSecurity:
    """Test des fonctionnalités de sécurité renforcée - Phase 3"""
    
    def __init__(self):
        self.results = {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "start_time": datetime.now(),
            "details": []
        }
        print("🔒 Démarrage des tests de sécurité renforcée - Phase 3")
        print("=" * 65)
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log un résultat de test"""
        self.results["tests_run"] += 1
        if success:
            self.results["tests_passed"] += 1
            status = "✅ PASS"
        else:
            self.results["tests_failed"] += 1
            status = "❌ FAIL"
            
        self.results["details"].append({
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"{status} {test_name}")
        if details:
            print(f"   📝 {details}")

    def test_enhanced_encryption_handler(self):
        """Test du handler de chiffrement renforcé"""
        try:
            from logging_manager_optimized import EncryptionHandler
            import logging
            
            # Créer un handler de base mock
            class MockHandler:
                def __init__(self):
                    self.records = []
                def emit(self, record):
                    self.records.append(record)
                def setFormatter(self, formatter):
                    pass
            
            mock_handler = MockHandler()
            
            # Test d'instanciation avec rotation
            encryption_handler = EncryptionHandler(
                mock_handler,
                "test_key_for_encryption_validation",
                key_rotation_hours=1,  # Rotation rapide pour test
                max_keys_history=3
            )
            
            # Vérifier l'initialisation
            has_keys_history = hasattr(encryption_handler, '_keys_history')
            has_security_metrics = hasattr(encryption_handler, '_security_metrics')
            
            self.log_test(
                "Sécurité - Handler chiffrement renforcé",
                has_keys_history and has_security_metrics,
                f"Historique clés: {has_keys_history}, Métriques: {has_security_metrics}"
            )
            
        except Exception as e:
            self.log_test(
                "Sécurité - Handler renforcé",
                False,
                f"Erreur: {str(e)}"
            )

    def test_sensitive_data_detection(self):
        """Test de la détection améliorée de données sensibles"""
        try:
            from logging_manager_optimized import EncryptionHandler
            import logging
            
            class MockHandler:
                def __init__(self):
                    self.records = []
                def emit(self, record):
                    self.records.append(record)
                def setFormatter(self, formatter):
                    pass
            
            mock_handler = MockHandler()
            encryption_handler = EncryptionHandler(mock_handler, "test_key_12345678901234567890123456")
            
            # Créer des records de test
            test_cases = [
                ("Normal log message", False),
                ("User password is secret123", True),
                ("API token: abc123def456", True),
                ("User email: test@example.com", True),
                ("Server IP: 192.168.1.100", True),
                ("Regular info message", False)
            ]
            
            detection_results = []
            for message, expected in test_cases:
                record = logging.LogRecord(
                    name="test.security",
                    level=logging.INFO,
                    pathname="test.py",
                    lineno=1,
                    msg=message,
                    args=(),
                    exc_info=None
                )
                
                is_sensitive = encryption_handler._is_sensitive(record)
                detection_results.append(is_sensitive == expected)
            
            accuracy = sum(detection_results) / len(detection_results) * 100
            
            self.log_test(
                "Sécurité - Détection données sensibles",
                accuracy >= 80,  # Au moins 80% de précision
                f"Précision détection: {accuracy:.1f}% ({sum(detection_results)}/{len(detection_results)})"
            )
            
        except Exception as e:
            self.log_test(
                "Sécurité - Détection sensible",
                False,
                f"Erreur: {str(e)}"
            )

    def test_key_rotation_mechanism(self):
        """Test du mécanisme de rotation des clés"""
        try:
            from logging_manager_optimized import EncryptionHandler
            import logging
            
            class MockHandler:
                def __init__(self):
                    self.records = []
                def emit(self, record):
                    self.records.append(record)
                def setFormatter(self, formatter):
                    pass
            
            mock_handler = MockHandler()
            
            # Handler avec rotation très rapide pour test
            encryption_handler = EncryptionHandler(
                mock_handler,
                "test_key_12345678901234567890123456",
                key_rotation_hours=0.0001,  # 0.0001h = 0.36s
                max_keys_history=3
            )
            
            # Vérifier l'état initial
            initial_keys_count = len(encryption_handler._keys_history)
            initial_key_id = encryption_handler._keys_history[0]["key_id"]
            
            # Attendre suffisamment pour dépasser le seuil de rotation
            time.sleep(0.5)  # 500ms > 0.0001h * 3600s = 0.36s
            
            # Créer plusieurs logs sensibles pour déclencher la vérification de rotation
            for i in range(5):
                record = logging.LogRecord(
                    name="test.security",
                    level=logging.INFO,
                    pathname="test.py",
                    lineno=1,
                    msg=f"password: secret{i}",
                    args=(),
                    exc_info=None
                )
                encryption_handler.emit(record)
                
                # Vérifier après chaque émission
                if len(encryption_handler._keys_history) > initial_keys_count:
                    break
            
            # Vérifier si rotation a eu lieu
            after_keys_count = len(encryption_handler._keys_history)
            current_key_id = encryption_handler._keys_history[encryption_handler._current_key_index]["key_id"]
            
            rotation_occurred = (after_keys_count > initial_keys_count or 
                               current_key_id != initial_key_id)
            
            # Debug info
            time_since_rotation = (datetime.now() - encryption_handler._last_rotation).total_seconds()
            should_rotate = encryption_handler._should_rotate_key()
            
            self.log_test(
                "Sécurité - Mécanisme rotation clés",
                rotation_occurred,
                f"Clés avant: {initial_keys_count}, après: {after_keys_count}, rotation: {rotation_occurred}, temps: {time_since_rotation:.3f}s, should_rotate: {should_rotate}"
            )
            
        except Exception as e:
            self.log_test(
                "Sécurité - Rotation clés",
                False,
                f"Erreur: {str(e)}"
            )

    def test_security_metrics(self):
        """Test des métriques de sécurité"""
        try:
            from logging_manager_optimized import EncryptionHandler
            import logging
            
            class MockHandler:
                def __init__(self):
                    self.records = []
                def emit(self, record):
                    self.records.append(record)
                def setFormatter(self, formatter):
                    pass
            
            mock_handler = MockHandler()
            encryption_handler = EncryptionHandler(
                mock_handler,
                "test_key_12345678901234567890123456"
            )
            
            # Simuler quelques opérations de chiffrement
            for i in range(5):
                record = logging.LogRecord(
                    name="test.security",
                    level=logging.INFO,
                    pathname="test.py",
                    lineno=1,
                    msg=f"password: secret{i}",
                    args=(),
                    exc_info=None
                )
                encryption_handler.emit(record)
            
            # Récupérer les métriques
            metrics = encryption_handler.get_security_metrics()
            
            # Vérifier la structure des métriques
            required_keys = [
                "encryption_operations", "sensitive_logs_encrypted", 
                "current_key_id", "rotation_policy"
            ]
            has_required_keys = all(key in metrics for key in required_keys)
            
            # Vérifier que les opérations ont été comptées
            operations_counted = metrics.get("encryption_operations", 0) >= 5
            
            self.log_test(
                "Sécurité - Métriques sécurité",
                has_required_keys and operations_counted,
                f"Clés requises: {has_required_keys}, Opérations: {metrics.get('encryption_operations', 0)}"
            )
            
        except Exception as e:
            self.log_test(
                "Sécurité - Métriques",
                False,
                f"Erreur: {str(e)}"
            )

    def test_logging_manager_integration(self):
        """Test de l'intégration dans LoggingManager"""
        try:
            from logging_manager_optimized import LoggingManager, LoggingConfig
            
            # Configuration avec chiffrement renforcé
            config = LoggingConfig(
                logger_name="test.security.enhanced",
                encryption_enabled=True,
                encryption_key="test_key_12345678901234567890123456",
                key_rotation_hours=24,
                max_keys_history=5,
                enhanced_sensitive_detection=True
            )
            
            manager = LoggingManager()
            logger = manager.get_logger(None, config.__dict__)
            
            # Test que le logger a été créé
            has_logger = logger is not None
            
            # Test des métriques de sécurité
            security_metrics = manager.get_security_metrics()
            has_enhanced_security = security_metrics.get("enhanced_security", False)
            
            self.log_test(
                "Sécurité - Intégration LoggingManager",
                has_logger and has_enhanced_security,
                f"Logger créé: {has_logger}, Sécurité renforcée: {has_enhanced_security}"
            )
            
        except Exception as e:
            self.log_test(
                "Sécurité - Intégration",
                False,
                f"Erreur: {str(e)}"
            )

    def test_encryption_decryption_cycle(self):
        """Test du cycle complet chiffrement/déchiffrement"""
        try:
            from logging_manager_optimized import EncryptionHandler
            import logging
            
            class MockHandler:
                def __init__(self):
                    self.records = []
                def emit(self, record):
                    self.records.append(record)
                def setFormatter(self, formatter):
                    pass
            
            mock_handler = MockHandler()
            encryption_handler = EncryptionHandler(
                mock_handler,
                "test_key_12345678901234567890123456"
            )
            
            # Message sensible original
            original_message = "User password is supersecret123"
            
            # Créer et émettre un log sensible
            record = logging.LogRecord(
                name="test.security",
                level=logging.INFO,
                pathname="test.py",
                lineno=1,
                msg=original_message,
                args=(),
                exc_info=None
            )
            
            encryption_handler.emit(record)
            
            # Récupérer le message chiffré
            encrypted_record = mock_handler.records[0]
            encrypted_message = encrypted_record.msg
            
            # Vérifier que le message a été chiffré
            is_encrypted = encrypted_message.startswith("[ENCRYPTED:")
            
            # Tenter de déchiffrer
            if is_encrypted:
                decrypted = encryption_handler.decrypt_log(encrypted_message)
                decryption_successful = decrypted == original_message
            else:
                decryption_successful = False
            
            self.log_test(
                "Sécurité - Cycle chiffrement/déchiffrement",
                is_encrypted and decryption_successful,
                f"Chiffré: {is_encrypted}, Déchiffrement: {decryption_successful}"
            )
            
        except Exception as e:
            self.log_test(
                "Sécurité - Cycle complet",
                False,
                f"Erreur: {str(e)}"
            )

    def generate_report(self):
        """Génère le rapport final"""
        end_time = datetime.now()
        duration = (end_time - self.results["start_time"]).total_seconds()
        
        success_rate = (self.results["tests_passed"] / self.results["tests_run"] * 100) if self.results["tests_run"] > 0 else 0
        
        print("\n" + "=" * 65)
        print("🔒 RÉSUMÉ DES TESTS SÉCURITÉ RENFORCÉE - PHASE 3")
        print("=" * 65)
        print(f"✅ Tests réussis: {self.results['tests_passed']}")
        print(f"❌ Tests échoués: {self.results['tests_failed']}")
        print(f"📈 Taux de réussite: {success_rate:.1f}%")
        print(f"⏱️  Durée: {duration:.2f}s")
        
        # Sauvegarde du rapport
        report_file = Path(__file__).parent / f"test_report_enhanced_security_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            **self.results,
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "success_rate": success_rate
        }
        
        # Convertir start_time en string pour JSON
        if "start_time" in report_data:
            report_data["start_time"] = report_data["start_time"].isoformat()
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Rapport sauvegardé: {report_file}")
        
        # Statut final
        if self.results["tests_failed"] == 0:
            print("\n🎊 TOUS LES TESTS DE SÉCURITÉ RENFORCÉE RÉUSSIS !")
            print("✅ Phase 3 - Sécurité renforcée validée avec succès")
        else:
            print(f"\n⚠️  {self.results['tests_failed']} test(s) échoué(s)")
            print("🔧 Corrections nécessaires pour validation complète Phase 3")

    def run_all_tests(self):
        """Exécute tous les tests de sécurité renforcée"""
        print("🔍 Démarrage des tests de sécurité renforcée...")
        
        self.test_enhanced_encryption_handler()
        self.test_sensitive_data_detection()
        self.test_key_rotation_mechanism()
        self.test_security_metrics()
        self.test_logging_manager_integration()
        self.test_encryption_decryption_cycle()
        
        self.generate_report()

def main():
    """Fonction principale"""
    tester = TestEnhancedSecurity()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 