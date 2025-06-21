#!/usr/bin/env python3
"""
🧪 TEST POSTGRESQL UTF-8 - CURSOR TASKMASTER NEXTGENERATION
Validation complète de la résolution UnicodeDecodeError
Adapté à la configuration du projet 20250620_projet_taskmanager
"""

import sys
import logging
import traceback
from datetime import datetime
from pathlib import Path

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PostgreSQLUTF8Tester:
    """Testeur PostgreSQL UTF-8 pour environnement TaskMaster NextGeneration"""
    
    def __init__(self):
        # Configuration TaskMaster
        self.project_root = Path(__file__).parent.parent
        self.memory_api_path = self.project_root.parent.parent / "memory_api"
        
        # Ajout du chemin memory_api au PYTHONPATH
        sys.path.insert(0, str(self.memory_api_path))
        
        # Résultats des tests
        self.test_results = {
            "connexion_basique": {"status": False, "details": "", "error": ""},
            "verification_locale": {"status": False, "details": "", "error": ""},
            "caracteres_francais": {"status": False, "details": "", "error": ""},
            "sqlalchemy_integration": {"status": False, "details": "", "error": ""},
            "session_taskmaster": {"status": False, "details": "", "error": ""}
        }
    
    def test_connexion_basique(self):
        """Test 1: Connexion PostgreSQL basique"""
        logger.info("🧪 Test 1 : Connexion PostgreSQL basique")
        
        try:
            import psycopg2
            
            # Connexion directe PostgreSQL
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="nextgeneration",
                user="postgres",
                password="postgres"
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            
            # Test requête simple
            cursor.execute("SELECT 1 as test_value;")
            test_value = cursor.fetchone()[0]
            
            if test_value == 1:
                self.test_results["connexion_basique"]["status"] = True
                self.test_results["connexion_basique"]["details"] = f"PostgreSQL {version.split(' ')[1]}"
                logger.info(f"✅ Test 1 : Connexion réussie - {version.split(' ')[1]}")
            else:
                raise Exception("Test value incorrect")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            self.test_results["connexion_basique"]["error"] = str(e)
            logger.error(f"❌ Test 1 : Connexion échouée - {e}")
    
    def test_verification_locale(self):
        """Test 2: Vérification lc_messages = 'C'"""
        logger.info("🧪 Test 2 : Vérification lc_messages")
        
        try:
            from sqlalchemy import create_engine, text
            
            # Configuration identique à TaskMaster
            DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/nextgeneration?client_encoding=utf8"
            engine = create_engine(DATABASE_URL)
            
            with engine.connect() as conn:
                result = conn.execute(text("SHOW lc_messages"))
                lc_messages = result.scalar()
                
                if lc_messages == "C":
                    self.test_results["verification_locale"]["status"] = True
                    self.test_results["verification_locale"]["details"] = f"lc_messages = '{lc_messages}' (UTF-8 compatible)"
                    logger.info(f"✅ Test 2 : lc_messages = 'C' (correct)")
                else:
                    self.test_results["verification_locale"]["details"] = f"lc_messages = '{lc_messages}' (risque UTF-8)"
                    logger.warning(f"⚠️ Test 2 : lc_messages = '{lc_messages}' (risque UTF-8)")
                    
        except Exception as e:
            self.test_results["verification_locale"]["error"] = str(e)
            logger.error(f"❌ Test 2 : Vérification locale échouée - {e}")
    
    def test_caracteres_francais(self):
        """Test 3: Caractères français UTF-8"""
        logger.info("🧪 Test 3 : Caractères français UTF-8")
        
        try:
            from sqlalchemy import create_engine, text
            
            DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/nextgeneration?client_encoding=utf8"
            engine = create_engine(DATABASE_URL)
            
            # Test avec caractères accentués français
            test_texts = [
                "Test caractères français : éàèùç âêîôû",
                "Développement spécialisé en français",
                "PostgreSQL configuré pour l'encodage UTF-8",
                "TaskMaster NextGenération opérationnel"
            ]
            
            with engine.connect() as conn:
                for i, test_text in enumerate(test_texts):
                    result = conn.execute(text("SELECT :text AS test_francais"), {"text": test_text})
                    returned_text = result.scalar()
                    
                    if returned_text != test_text:
                        raise Exception(f"Caractères corrompus pour le texte {i+1}")
                
                self.test_results["caracteres_francais"]["status"] = True
                self.test_results["caracteres_francais"]["details"] = f"{len(test_texts)} textes français validés"
                logger.info(f"✅ Test 3 : {len(test_texts)} textes français préservés")
                
        except Exception as e:
            self.test_results["caracteres_francais"]["error"] = str(e)
            logger.error(f"❌ Test 3 : Caractères français échoué - {e}")
    
    def test_sqlalchemy_integration(self):
        """Test 4: Intégration SQLAlchemy TaskMaster"""
        logger.info("🧪 Test 4 : Intégration SQLAlchemy TaskMaster")
        
        try:
            from memory_api.app.db.session import get_db, warn_if_bad_locale
            from sqlalchemy import text
            
            # Test générateur de session
            db = next(get_db())
            
            # Test requête simple
            result = db.execute(text("SELECT 'SQLAlchemy TaskMaster OK' AS test"))
            message = result.scalar()
            
            if message == "SQLAlchemy TaskMaster OK":
                # Test fonction warn_if_bad_locale
                warn_if_bad_locale(db)
                
                self.test_results["sqlalchemy_integration"]["status"] = True
                self.test_results["sqlalchemy_integration"]["details"] = "Intégration SQLAlchemy fonctionnelle"
                logger.info("✅ Test 4 : SQLAlchemy intégration réussie")
            else:
                raise Exception("Message de test incorrect")
            
            db.close()
            
        except Exception as e:
            self.test_results["sqlalchemy_integration"]["error"] = str(e)
            logger.error(f"❌ Test 4 : SQLAlchemy intégration échouée - {e}")
    
    def test_session_taskmaster(self):
        """Test 5: Session TaskMaster complète"""
        logger.info("🧪 Test 5 : Session TaskMaster complète")
        
        try:
            from memory_api.app.db.session import test_connection, get_database_stats
            
            # Test fonction test_connection
            connection_success = test_connection()
            
            if connection_success:
                # Test statistiques base de données
                try:
                    stats = get_database_stats()
                    stats_available = True
                except:
                    stats_available = False
                
                self.test_results["session_taskmaster"]["status"] = True
                self.test_results["session_taskmaster"]["details"] = f"Connexion OK, Stats: {'Disponibles' if stats_available else 'Non disponibles'}"
                logger.info("✅ Test 5 : Session TaskMaster fonctionnelle")
            else:
                raise Exception("test_connection() a échoué")
                
        except Exception as e:
            self.test_results["session_taskmaster"]["error"] = str(e)
            logger.error(f"❌ Test 5 : Session TaskMaster échouée - {e}")
    
    def run_all_tests(self):
        """Exécute tous les tests PostgreSQL UTF-8"""
        logger.info("🧪 TESTS POSTGRESQL UTF-8 - TASKMASTER NEXTGENERATION")
        logger.info("=" * 70)
        
        # Exécution séquentielle des tests
        test_methods = [
            self.test_connexion_basique,
            self.test_verification_locale,
            self.test_caracteres_francais,
            self.test_sqlalchemy_integration,
            self.test_session_taskmaster
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                logger.error(f"❌ Erreur critique dans {test_method.__name__}: {e}")
                logger.debug(traceback.format_exc())
        
        return self.analyze_results()
    
    def analyze_results(self):
        """Analyse les résultats des tests"""
        logger.info("📊 ANALYSE DES RÉSULTATS")
        logger.info("-" * 50)
        
        passed_tests = 0
        total_tests = len(self.test_results)
        
        for test_name, result in self.test_results.items():
            status_icon = "✅" if result["status"] else "❌"
            logger.info(f"{status_icon} {test_name}: {result['details'] if result['status'] else result['error']}")
            
            if result["status"]:
                passed_tests += 1
        
        success_rate = (passed_tests / total_tests) * 100
        
        logger.info("-" * 50)
        logger.info(f"📈 RÉSULTATS FINAUX : {passed_tests}/{total_tests} tests réussis ({success_rate:.1f}%)")
        
        if passed_tests == total_tests:
            logger.info("🎉 POSTGRESQL UTF-8 : 100% OPÉRATIONNEL")
            logger.info("✅ Problème UnicodeDecodeError DÉFINITIVEMENT RÉSOLU")
            logger.info("✅ TaskMaster NextGeneration prêt pour production")
            return True
        else:
            logger.warning("⚠️ POSTGRESQL UTF-8 : Problèmes détectés")
            logger.info("💡 Vérifiez la configuration et exécutez fix_postgresql_utf8_cursor.py")
            return False
    
    def generate_test_report(self, overall_success):
        """Génère un rapport détaillé des tests"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# 📋 RAPPORT TESTS POSTGRESQL UTF-8 - TASKMASTER NEXTGENERATION

## Informations
- **Date** : {timestamp}
- **Projet** : 20250620_projet_taskmanager
- **Répertoire** : 04_implémentatin_cursor
- **Statut global** : {'✅ SUCCÈS' if overall_success else '❌ ÉCHEC'}

## Résultats détaillés

"""
        
        for test_name, result in self.test_results.items():
            status = "✅ RÉUSSI" if result["status"] else "❌ ÉCHOUÉ"
            details = result["details"] if result["status"] else result["error"]
            
            report += f"""### {test_name}
- **Statut** : {status}
- **Détails** : {details}

"""
        
        # Recommandations
        if overall_success:
            report += """## Recommandations
✅ **PostgreSQL UTF-8 opérationnel** - Aucune action requise
✅ **TaskMaster NextGeneration prêt** pour production
✅ **Architecture robuste** avec PostgreSQL enterprise

"""
        else:
            failed_tests = [name for name, result in self.test_results.items() if not result["status"]]
            report += f"""## Recommandations
❌ **Tests échoués** : {', '.join(failed_tests)}
💡 **Action requise** : Exécuter `fix_postgresql_utf8_cursor.py`
⚠️ **Fallback** : Utiliser SQLite si PostgreSQL non résolu

"""
        
        report += """## Configuration TaskMaster
- **Base de données** : PostgreSQL 17.5 + SQLite fallback
- **Encodage** : UTF-8 natif
- **Monitoring** : Vérification automatique lc_messages

---
*Rapport généré automatiquement par test_postgresql_utf8_cursor.py*
"""
        
        report_file = Path(__file__).parent / f"rapport_tests_utf8_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info(f"📄 Rapport généré : {report_file}")
        except Exception as e:
            logger.error(f"❌ Erreur génération rapport : {e}")

def main():
    """Point d'entrée principal"""
    print("🧪 TESTS POSTGRESQL UTF-8 - CURSOR TASKMASTER NEXTGENERATION")
    print("=" * 70)
    print("📁 Projet : 20250620_projet_taskmanager/04_implémentatin_cursor")
    print("🎯 Objectif : Validation résolution UnicodeDecodeError")
    print()
    
    # Confirmation utilisateur
    response = input("Lancer les tests PostgreSQL UTF-8 ? (o/N) : ")
    if response.lower() not in ['o', 'oui', 'y', 'yes']:
        print("❌ Tests annulés par l'utilisateur")
        return False
    
    # Exécution tests
    tester = PostgreSQLUTF8Tester()
    success = tester.run_all_tests()
    
    # Génération rapport
    tester.generate_test_report(success)
    
    print()
    print("=" * 70)
    if success:
        print("🎉 TESTS RÉUSSIS - POSTGRESQL UTF-8 OPÉRATIONNEL")
        print("✅ TaskMaster NextGeneration prêt pour production")
        print("✅ Problème UnicodeDecodeError définitivement résolu")
    else:
        print("❌ TESTS ÉCHOUÉS - PROBLÈMES DÉTECTÉS")
        print("💡 Exécutez fix_postgresql_utf8_cursor.py pour corriger")
        print("📄 Consultez le rapport généré pour plus de détails")
    
    input("Appuyez sur Entrée pour terminer...")
    return success

if __name__ == "__main__":
    main() 