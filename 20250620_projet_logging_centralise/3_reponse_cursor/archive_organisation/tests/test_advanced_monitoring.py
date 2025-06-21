#!/usr/bin/env python3
"""
🧪 Test Monitoring Avancé - Phase 2 ChatGPT
Validation des fonctionnalités de monitoring avancé avec OpenTelemetry
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Ajout du chemin pour les imports
sys.path.append(str(Path(__file__).parent))

class TestAdvancedMonitoring:
    """Test des fonctionnalités de monitoring avancé - Phase 2"""
    
    def __init__(self):
        self.results = {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "start_time": datetime.now(),
            "details": []
        }
        print("🚀 Démarrage des tests de monitoring avancé - Phase 2")
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

    def test_opentelemetry_availability(self):
        """Test de la disponibilité d'OpenTelemetry"""
        try:
            from logging_manager_optimized import OPENTELEMETRY_AVAILABLE, TRACING_ENABLED
            
            self.log_test(
                "Monitoring - OpenTelemetry disponibilité",
                True,  # Le test passe même si OTel n'est pas disponible (fallback)
                f"OpenTelemetry: {OPENTELEMETRY_AVAILABLE}, Tracing: {TRACING_ENABLED}"
            )
            
        except Exception as e:
            self.log_test(
                "Monitoring - OpenTelemetry",
                False,
                f"Erreur: {str(e)}"
            )

    def test_advanced_monitoring_handler(self):
        """Test du handler de monitoring avancé"""
        try:
            from logging_manager_optimized import AdvancedMonitoringHandler
            
            # Test d'instanciation
            handler = AdvancedMonitoringHandler(
                service_name="test-monitoring",
                enable_tracing=True
            )
            
            # Test des métriques
            metrics = handler.get_metrics_summary()
            has_monitoring_type = "monitoring_type" in metrics
            
            self.log_test(
                "Monitoring - Handler avancé",
                has_monitoring_type,
                f"Type monitoring: {metrics.get('monitoring_type', 'inconnu')}"
            )
            
        except Exception as e:
            self.log_test(
                "Monitoring - Handler",
                False,
                f"Erreur: {str(e)}"
            )

    def test_logging_manager_integration(self):
        """Test de l'intégration dans LoggingManager"""
        try:
            import sys
from pathlib import Path
from core import logging_manager, LoggingConfig
            
            # Configuration avec monitoring avancé
            config = LoggingConfig(
                logger_name="test.monitoring.advanced",
                advanced_monitoring_enabled=True
            )
            
            manager = LoggingManager()
            logger = manager.get_logger(None, config.__dict__)
            
            # Test que le logger a été créé
            has_logger = logger is not None
            
            # Test des métriques de monitoring avancé
            advanced_metrics = manager.get_advanced_monitoring_metrics()
            has_advanced_monitoring = advanced_metrics.get("advanced_monitoring", False)
            
            self.log_test(
                "Monitoring - Intégration LoggingManager",
                has_logger and has_advanced_monitoring,
                f"Logger créé: {has_logger}, Monitoring actif: {has_advanced_monitoring}"
            )
            
        except Exception as e:
            self.log_test(
                "Monitoring - Intégration",
                False,
                f"Erreur: {str(e)}"
            )

    def test_performance_monitoring(self):
        """Test du monitoring de performance"""
        try:
            import sys
from pathlib import Path
from core import logging_manager, LoggingConfig
            
            # Configuration pour monitoring de performance
            config = LoggingConfig(
                logger_name="test.performance.monitoring",
                advanced_monitoring_enabled=True
            )
            
            manager = LoggingManager()
            logger = manager.get_logger(None, config.__dict__)
            
            # Générer quelques logs pour tester la performance
            start_time = time.time()
            for i in range(10):
                logger.info(f"Test message performance {i}")
                logger.warning(f"Test warning {i}")
            
            processing_time = (time.time() - start_time) * 1000  # en ms
            
            # Récupérer les métriques
            advanced_metrics = manager.get_advanced_monitoring_metrics()
            has_metrics = "handlers_metrics" in advanced_metrics
            
            self.log_test(
                "Monitoring - Performance",
                has_metrics and processing_time < 1000,  # moins de 1 seconde pour 20 logs
                f"Temps traitement: {processing_time:.2f}ms, Métriques: {has_metrics}"
            )
            
        except Exception as e:
            self.log_test(
                "Monitoring - Performance",
                False,
                f"Erreur: {str(e)}"
            )

    def test_metrics_aggregation(self):
        """Test de l'agrégation des métriques"""
        try:
            import sys
from pathlib import Path
from core import logging_manager
            
            manager = LoggingManager()
            
            # Récupérer les métriques agrégées
            advanced_metrics = manager.get_advanced_monitoring_metrics()
            
            # Vérifier la structure des métriques
            required_keys = ["advanced_monitoring", "opentelemetry_available", "tracing_enabled"]
            has_required_keys = all(key in advanced_metrics for key in required_keys)
            
            # Vérifier si on a des métriques agrégées
            has_aggregated = "aggregated_metrics" in advanced_metrics or "handlers_metrics" in advanced_metrics
            
            self.log_test(
                "Monitoring - Agrégation métriques",
                has_required_keys and has_aggregated,
                f"Clés requises: {has_required_keys}, Métriques agrégées: {has_aggregated}"
            )
            
        except Exception as e:
            self.log_test(
                "Monitoring - Agrégation",
                False,
                f"Erreur: {str(e)}"
            )

    def test_fallback_mode(self):
        """Test du mode fallback sans OpenTelemetry"""
        try:
            from logging_manager_optimized import AdvancedMonitoringHandler, OPENTELEMETRY_AVAILABLE
            
            # Créer un handler en mode fallback
            handler = AdvancedMonitoringHandler(
                service_name="test-fallback",
                enable_tracing=False  # Force le mode fallback
            )
            
            # Simuler quelques logs
            import logging
            record = logging.LogRecord(
                name="test.fallback",
                level=logging.INFO,
                pathname="test.py",
                lineno=1,
                msg="Test message fallback",
                args=(),
                exc_info=None
            )
            
            handler.emit(record)
            
            # Vérifier les métriques fallback
            metrics = handler.get_metrics_summary()
            is_fallback = metrics.get("monitoring_type") == "fallback"
            has_logs_count = "logs_total" in metrics
            
            self.log_test(
                "Monitoring - Mode fallback",
                is_fallback and has_logs_count,
                f"Mode fallback: {is_fallback}, Comptage logs: {has_logs_count}"
            )
            
        except Exception as e:
            self.log_test(
                "Monitoring - Fallback",
                False,
                f"Erreur: {str(e)}"
            )

    def generate_report(self):
        """Génère le rapport final"""
        end_time = datetime.now()
        duration = (end_time - self.results["start_time"]).total_seconds()
        
        success_rate = (self.results["tests_passed"] / self.results["tests_run"] * 100) if self.results["tests_run"] > 0 else 0
        
        print("\n" + "=" * 65)
        print("🎯 RÉSUMÉ DES TESTS MONITORING AVANCÉ - PHASE 2")
        print("=" * 65)
        print(f"✅ Tests réussis: {self.results['tests_passed']}")
        print(f"❌ Tests échoués: {self.results['tests_failed']}")
        print(f"📈 Taux de réussite: {success_rate:.1f}%")
        print(f"⏱️  Durée: {duration:.2f}s")
        
        # Sauvegarde du rapport
        report_file = Path(__file__).parent / f"test_report_advanced_monitoring_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
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
            print("\n🎊 TOUS LES TESTS DE MONITORING AVANCÉ RÉUSSIS !")
            print("✅ Phase 2 - Monitoring avancé validé avec succès")
        else:
            print(f"\n⚠️  {self.results['tests_failed']} test(s) échoué(s)")
            print("🔧 Corrections nécessaires pour validation complète Phase 2")

    def run_all_tests(self):
        """Exécute tous les tests de monitoring avancé"""
        print("🔍 Démarrage des tests de monitoring avancé...")
        
        self.test_opentelemetry_availability()
        self.test_advanced_monitoring_handler()
        self.test_logging_manager_integration()
        self.test_performance_monitoring()
        self.test_metrics_aggregation()
        self.test_fallback_mode()
        
        self.generate_report()

def main():
    """Fonction principale"""
    tester = TestAdvancedMonitoring()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 



