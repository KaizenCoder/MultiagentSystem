#!/usr/bin/env python3
"""
🧪 Test d'Intégration ChatGPT Simplifié - Logging Centralisé NextGeneration
Version simplifiée pour éviter les blocages
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Ajout du chemin pour les imports
sys.path.append(str(Path(__file__).parent))

class TestChatGPTIntegrationSimple:
    """Classe de test simplifiée pour les améliorations ChatGPT"""
    
    def __init__(self):
        self.results = {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "start_time": datetime.now(),
            "details": []
        }
        print("🚀 Démarrage des tests d'intégration ChatGPT - Version Simplifiée")
        print("=" * 70)
        
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

    def test_imports_integration(self):
        """Test que tous les imports fonctionnent correctement"""
        try:
            import sys
from pathlib import Path
from core import logging_manager, LoggingConfig
            from template_manager_integrated import TemplateManagerIntegrated, TemplateMetrics
            from agent_coordinateur_integrated import Agent0ChefEquipeCoordinateur, AICoordinationEngine
            
            self.log_test(
                "Intégration - Imports modules principaux",
                True,
                "Tous les modules importés avec succès"
            )
            
            # Test d'instanciation basique
            manager = LoggingManager()
            config = LoggingConfig(logger_name="test.integration")
            
            self.log_test(
                "Intégration - Instanciation LoggingManager",
                True,
                "LoggingManager créé sans erreur"
            )
            
        except Exception as e:
            self.log_test(
                "Intégration - Imports et instanciation",
                False,
                f"Erreur: {str(e)}"
            )

    def test_chatgpt_features_presence(self):
        """Test de la présence des fonctionnalités ChatGPT"""
        try:
            from logging_manager_optimized import LoggingConfig
            
            # Test nouvelles options de configuration
            config = LoggingConfig(
                logger_name="test.chatgpt.features",
                elasticsearch_enabled=True,
                encryption_enabled=True,
                alerting_enabled=True,
                sensitive_data_masking=True
            )
            
            chatgpt_features = [
                hasattr(config, 'elasticsearch_enabled'),
                hasattr(config, 'encryption_enabled'),
                hasattr(config, 'alerting_enabled'),
                hasattr(config, 'sensitive_data_masking')
            ]
            
            self.log_test(
                "Intégration - Fonctionnalités ChatGPT présentes",
                all(chatgpt_features),
                f"Fonctionnalités détectées: {sum(chatgpt_features)}/4"
            )
            
        except Exception as e:
            self.log_test(
                "Intégration - Fonctionnalités ChatGPT",
                False,
                f"Erreur: {str(e)}"
            )

    def test_ai_coordination_engine(self):
        """Test du moteur d'IA de coordination"""
        try:
            from agent_coordinateur_integrated import AICoordinationEngine
            
            # Test d'instanciation
            ai_engine = AICoordinationEngine(
                agent_id="test_ai_engine",
                enabled=True,
                learning_mode=True,
                optimization_threshold=0.8
            )
            
            # Test des méthodes de base
            patterns = ai_engine.analyze_workflow_patterns()
            has_recommendations = "recommendations" in patterns
            has_confidence = "confidence" in patterns
            
            self.log_test(
                "Intégration - Moteur IA Coordination",
                has_recommendations and has_confidence,
                f"Analyse patterns: {has_recommendations}, Confiance: {has_confidence}"
            )
            
        except Exception as e:
            self.log_test(
                "Intégration - Moteur IA",
                False,
                f"Erreur: {str(e)}"
            )

    def test_template_manager_integration(self):
        """Test de l'intégration du TemplateManager"""
        try:
            template_file = Path(__file__).parent / "template_manager_integrated.py"
            
            if not template_file.exists():
                self.log_test(
                    "Intégration - TemplateManager fichier",
                    False,
                    "Fichier template_manager_integrated.py non trouvé"
                )
                return
            
            # Lire et vérifier le contenu
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les nouvelles fonctionnalités ChatGPT
            chatgpt_keywords = [
                "chatgpt_enhancements",
                "TemplateManagerIntegrated",
                "advanced_features",
                "namespace_analytics",
                "performance_insights"
            ]
            
            found_keywords = [kw for kw in chatgpt_keywords if kw in content]
            
            self.log_test(
                "Intégration - TemplateManager ChatGPT",
                len(found_keywords) >= 4,
                f"Mots-clés ChatGPT trouvés: {len(found_keywords)}/5"
            )
            
        except Exception as e:
            self.log_test(
                "Intégration - TemplateManager",
                False,
                f"Erreur: {str(e)}"
            )

    def test_logging_chatgpt_constants(self):
        """Test des constantes ChatGPT dans le logging"""
        try:
            import logging_manager_optimized as lmo
            
            # Vérifier les constantes ChatGPT
            constants = [
                hasattr(lmo, 'ELASTICSEARCH_BATCH_SIZE'),
                hasattr(lmo, 'ALERT_THRESHOLD_ERRORS'),
                hasattr(lmo, 'ALERT_THRESHOLD_CRITICAL'),
                hasattr(lmo, 'ENCRYPTION_KEY_LENGTH')
            ]
            
            self.log_test(
                "Intégration - Constantes ChatGPT Logging",
                all(constants),
                f"Constantes présentes: {sum(constants)}/4"
            )
            
        except Exception as e:
            self.log_test(
                "Intégration - Constantes Logging",
                False,
                f"Erreur: {str(e)}"
            )

    def test_file_completeness(self):
        """Test de la complétude des fichiers"""
        required_files = [
            "logging_manager_optimized.py",
            "template_manager_integrated.py",
            "agent_coordinateur_integrated.py"
        ]
        
        existing_files = []
        for filename in required_files:
            file_path = Path(__file__).parent / filename
            if file_path.exists():
                existing_files.append(filename)
        
        self.log_test(
            "Intégration - Fichiers requis complets",
            len(existing_files) == len(required_files),
            f"Fichiers présents: {len(existing_files)}/{len(required_files)}"
        )

    def generate_report(self):
        """Génère le rapport final"""
        end_time = datetime.now()
        duration = (end_time - self.results["start_time"]).total_seconds()
        
        success_rate = (self.results["tests_passed"] / self.results["tests_run"] * 100) if self.results["tests_run"] > 0 else 0
        
        print("\n" + "=" * 70)
        print("🎯 RÉSUMÉ DES TESTS D'INTÉGRATION CHATGPT - VERSION SIMPLIFIÉE")
        print("=" * 70)
        print(f"✅ Tests réussis: {self.results['tests_passed']}")
        print(f"❌ Tests échoués: {self.results['tests_failed']}")
        print(f"📈 Taux de réussite: {success_rate:.1f}%")
        print(f"⏱️  Durée: {duration:.2f}s")
        
        # Sauvegarde du rapport
        report_file = Path(__file__).parent / f"test_report_integration_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            **self.results,
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "success_rate": success_rate
        }
        
        # Convertir les datetime en strings pour JSON
        for detail in report_data["details"]:
            if "timestamp" in detail:
                # timestamp est déjà en isoformat, pas de conversion nécessaire
                pass
        
        # Convertir start_time en string
        if "start_time" in report_data:
            report_data["start_time"] = report_data["start_time"].isoformat()
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Rapport sauvegardé: {report_file}")
        
        # Statut final
        if self.results["tests_failed"] == 0:
            print("\n🎊 TOUS LES TESTS D'INTÉGRATION RÉUSSIS !")
            print("✅ Intégration ChatGPT validée avec succès")
        else:
            print(f"\n⚠️  {self.results['tests_failed']} test(s) échoué(s)")
            print("🔧 Corrections nécessaires avant validation complète")

    def run_all_tests(self):
        """Exécute tous les tests d'intégration"""
        print("🔍 Démarrage des tests d'intégration...")
        
        self.test_imports_integration()
        self.test_chatgpt_features_presence()
        self.test_ai_coordination_engine()
        self.test_template_manager_integration()
        self.test_logging_chatgpt_constants()
        self.test_file_completeness()
        
        self.generate_report()

def main():
    """Fonction principale"""
    tester = TestChatGPTIntegrationSimple()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 



