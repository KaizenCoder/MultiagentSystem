#!/usr/bin/env python3
"""
Test Quick Fix - Validation rapide du logging manager
"""

import time
import tempfile
from logging_manager_optimized import LoggingManager

def test_basic_functionality():
    """Test basique pour identifier le problème"""
    print("🔧 Test rapide du système de logging...")
    
    try:
        # Test 1: Initialisation
        print("1️⃣ Initialisation LoggingManager...")
        manager = LoggingManager()
        print("   ✅ LoggingManager initialisé")
        
        # Test 2: Configuration simple
        print("2️⃣ Configuration simple...")
        test_config = {
            "logger_name": "test.simple",
            "log_level": "INFO",
            "log_dir": tempfile.mkdtemp(),
            "console_enabled": True,
            "file_enabled": True,
            "elasticsearch_enabled": False,  # Désactivé pour test rapide
            "encryption_enabled": False,      # Désactivé pour test rapide
            "async_enabled": False           # Désactivé pour test rapide
        }
        print("   ✅ Configuration créée")
        
        # Test 3: Création logger
        print("3️⃣ Création logger...")
        logger = manager.get_logger(custom_config=test_config)
        print("   ✅ Logger créé")
        
        # Test 4: Log simple
        print("4️⃣ Envoi message simple...")
        logger.info("Test message simple")
        print("   ✅ Message envoyé")
        
        # Test 5: Performance
        print("5️⃣ Test performance (10 messages)...")
        start = time.time()
        for i in range(10):
            logger.info(f"Message performance {i}")
        duration = (time.time() - start) * 1000
        print(f"   ✅ Performance: {duration:.2f}ms pour 10 messages")
        
        print("\n🎉 SUCCÈS: Système fonctionnel!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_basic_functionality() 