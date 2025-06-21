#!/usr/bin/env python3
"""
🔧 CORRECTION POSTGRESQL UTF-8 - CURSOR TASKMASTER NEXTGENERATION
Solution experte pour résoudre UnicodeDecodeError sur Windows français
Adapté à la configuration du projet 20250620_projet_taskmanager
"""

import os
import shutil
import time
import re
import logging
from datetime import datetime
from pathlib import Path

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PostgreSQLUTF8Fixer:
    """Correcteur PostgreSQL UTF-8 pour environnement Windows français"""
    
    def __init__(self):
        # Chemins PostgreSQL standard Windows
        self.pg_conf_path = Path(r"C:\Program Files\PostgreSQL\17\data\postgresql.conf")
        self.backup_dir = Path(__file__).parent / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Service PostgreSQL Windows
        self.service_name = "postgresql-x64-17"
        
        # Configuration TaskMaster
        self.project_root = Path(__file__).parent.parent
        
    def create_backup(self):
        """Crée une sauvegarde sécurisée de postgresql.conf"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"postgresql.conf.backup_{timestamp}"
        
        try:
            shutil.copy2(self.pg_conf_path, backup_file)
            logger.info(f"✅ Sauvegarde créée : {backup_file}")
            return backup_file
        except Exception as e:
            logger.error(f"❌ Erreur création sauvegarde : {e}")
            raise
    
    def check_current_config(self):
        """Vérifie la configuration actuelle de lc_messages"""
        try:
            with open(self.pg_conf_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Recherche lc_messages actuel
            lc_messages_match = re.search(r"lc_messages\s*=\s*'([^']*)'", content)
            
            if lc_messages_match:
                current_locale = lc_messages_match.group(1)
                logger.info(f"📋 Configuration actuelle : lc_messages = '{current_locale}'")
                
                if current_locale == "C":
                    logger.info("✅ lc_messages déjà configuré correctement")
                    return True, current_locale
                else:
                    logger.warning(f"⚠️ lc_messages = '{current_locale}' → Risque UnicodeDecodeError")
                    return False, current_locale
            else:
                logger.warning("⚠️ lc_messages non trouvé dans la configuration")
                return False, None
                
        except Exception as e:
            logger.error(f"❌ Erreur lecture configuration : {e}")
            raise
    
    def apply_utf8_fix(self):
        """Applique la correction UTF-8 (lc_messages = 'C')"""
        try:
            # Lecture configuration actuelle
            with open(self.pg_conf_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            
            # Pattern pour trouver et remplacer lc_messages
            pattern = r"lc_messages\s*=\s*'.*?'"
            replacement = "lc_messages = 'C'"
            
            if re.search(pattern, content):
                # Remplacer lc_messages existant
                content = re.sub(pattern, replacement, content)
                logger.info("🔄 lc_messages existant remplacé par 'C'")
            else:
                # Ajouter lc_messages = 'C' si absent
                content += f"\n# UTF-8 Fix pour Windows français - TaskMaster NextGeneration\nlc_messages = 'C'\n"
                logger.info("➕ lc_messages = 'C' ajouté à la configuration")
            
            # Écriture configuration modifiée
            with open(self.pg_conf_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if content != original_content:
                logger.info("✅ Configuration PostgreSQL mise à jour avec succès")
                return True
            else:
                logger.info("ℹ️ Aucune modification nécessaire")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur application correction : {e}")
            raise
    
    def restart_postgresql_service(self):
        """Redémarre le service PostgreSQL avec gestion d'erreurs"""
        try:
            logger.info("🔄 Redémarrage du service PostgreSQL...")
            
            # Arrêt du service
            logger.info("⏹️ Arrêt du service PostgreSQL...")
            stop_result = os.system(f"net stop {self.service_name}")
            
            if stop_result != 0:
                logger.warning("⚠️ Erreur arrêt service - Tentative de forcer...")
                os.system(f"sc stop {self.service_name}")
            
            # Attente sécurité
            time.sleep(3)
            
            # Démarrage du service
            logger.info("▶️ Démarrage du service PostgreSQL...")
            start_result = os.system(f"net start {self.service_name}")
            
            if start_result == 0:
                logger.info("✅ Service PostgreSQL redémarré avec succès")
                return True
            else:
                logger.error("❌ Erreur redémarrage service PostgreSQL")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur redémarrage service : {e}")
            return False
    
    def validate_fix(self):
        """Valide que la correction UTF-8 fonctionne"""
        try:
            # Import des modules TaskMaster
            import sys
            sys.path.append(str(self.project_root.parent.parent / "memory_api"))
            
            from memory_api.app.db.session import SessionLocal, warn_if_bad_locale
            from sqlalchemy import text
            
            logger.info("🧪 Validation de la correction UTF-8...")
            
            # Test connexion
            db = SessionLocal()
            
            # Test 1: Vérification lc_messages
            result = db.execute(text("SHOW lc_messages"))
            locale = result.scalar()
            
            if locale == "C":
                logger.info("✅ Test 1 : lc_messages = 'C' (correct)")
            else:
                logger.warning(f"⚠️ Test 1 : lc_messages = '{locale}' (risque UTF-8)")
                return False
            
            # Test 2: Caractères français
            test_text = "Test caractères français : éàèùç âêîôû"
            result = db.execute(text("SELECT :text AS test_francais"), {"text": test_text})
            returned_text = result.scalar()
            
            if returned_text == test_text:
                logger.info("✅ Test 2 : Caractères français préservés")
            else:
                logger.error("❌ Test 2 : Caractères français corrompus")
                return False
            
            # Test 3: Fonction warn_if_bad_locale
            warn_if_bad_locale(db)
            
            db.close()
            logger.info("🎉 Validation UTF-8 réussie - PostgreSQL 100% opérationnel")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur validation : {e}")
            return False
    
    def generate_report(self, success, backup_file=None):
        """Génère un rapport de la correction"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
# 📋 RAPPORT CORRECTION POSTGRESQL UTF-8 - TASKMASTER NEXTGENERATION

## Informations
- **Date** : {timestamp}
- **Projet** : 20250620_projet_taskmanager
- **Répertoire** : 04_implémentatin_cursor
- **Statut** : {'✅ SUCCÈS' if success else '❌ ÉCHEC'}

## Configuration
- **PostgreSQL** : {self.pg_conf_path}
- **Service** : {self.service_name}
- **Sauvegarde** : {backup_file if backup_file else 'Non créée'}

## Résultat
- **Correction appliquée** : {'Oui' if success else 'Non'}
- **Service redémarré** : {'Oui' if success else 'Non'}
- **Validation UTF-8** : {'Réussie' if success else 'Échouée'}

## Impact TaskMaster NextGeneration
- **Base de données** : {'PostgreSQL UTF-8 opérationnel' if success else 'Problème persistant'}
- **Architecture** : {'Production ready' if success else 'Fallback SQLite requis'}

---
*Rapport généré automatiquement par fix_postgresql_utf8_cursor.py*
"""
        
        report_file = Path(__file__).parent / f"rapport_correction_utf8_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info(f"📄 Rapport généré : {report_file}")
        except Exception as e:
            logger.error(f"❌ Erreur génération rapport : {e}")
    
    def run_complete_fix(self):
        """Exécute la correction complète PostgreSQL UTF-8"""
        logger.info("🔧 CORRECTION POSTGRESQL UTF-8 - TASKMASTER NEXTGENERATION")
        logger.info("=" * 70)
        
        success = False
        backup_file = None
        
        try:
            # Étape 1: Vérification configuration actuelle
            logger.info("📋 Étape 1 : Vérification configuration actuelle")
            is_correct, current_locale = self.check_current_config()
            
            if is_correct:
                logger.info("✅ Configuration déjà correcte - Validation uniquement")
                success = self.validate_fix()
            else:
                # Étape 2: Sauvegarde
                logger.info("💾 Étape 2 : Création sauvegarde sécurisée")
                backup_file = self.create_backup()
                
                # Étape 3: Application correction
                logger.info("🔧 Étape 3 : Application correction UTF-8")
                fix_applied = self.apply_utf8_fix()
                
                if fix_applied:
                    # Étape 4: Redémarrage service
                    logger.info("🔄 Étape 4 : Redémarrage service PostgreSQL")
                    restart_success = self.restart_postgresql_service()
                    
                    if restart_success:
                        # Attente stabilisation
                        logger.info("⏳ Attente stabilisation service...")
                        time.sleep(5)
                        
                        # Étape 5: Validation
                        logger.info("🧪 Étape 5 : Validation correction UTF-8")
                        success = self.validate_fix()
                    else:
                        logger.error("❌ Échec redémarrage - Correction non validée")
                else:
                    logger.error("❌ Échec application correction")
            
        except Exception as e:
            logger.error(f"❌ Erreur critique : {e}")
            success = False
        
        finally:
            # Génération rapport
            self.generate_report(success, backup_file)
            
            if success:
                logger.info("🎉 CORRECTION POSTGRESQL UTF-8 RÉUSSIE !")
                logger.info("✅ TaskMaster NextGeneration prêt pour 100% opérationnel")
            else:
                logger.error("❌ CORRECTION POSTGRESQL UTF-8 ÉCHOUÉE")
                logger.info("💡 Vérifiez les droits administrateur et la configuration")
        
        return success

def main():
    """Point d'entrée principal"""
    print("🔧 CORRECTION POSTGRESQL UTF-8 - CURSOR TASKMASTER NEXTGENERATION")
    print("=" * 70)
    print("⚠️  ATTENTION : Ce script nécessite des droits administrateur")
    print("📁 Projet : 20250620_projet_taskmanager/04_implémentatin_cursor")
    print()
    
    # Vérification droits administrateur
    try:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("❌ ERREUR : Droits administrateur requis")
            print("💡 Exécutez ce script en tant qu'Administrateur")
            input("Appuyez sur Entrée pour continuer...")
            return False
    except:
        print("⚠️ Impossible de vérifier les droits administrateur")
    
    # Confirmation utilisateur
    response = input("Continuer avec la correction PostgreSQL UTF-8 ? (o/N) : ")
    if response.lower() not in ['o', 'oui', 'y', 'yes']:
        print("❌ Correction annulée par l'utilisateur")
        return False
    
    # Exécution correction
    fixer = PostgreSQLUTF8Fixer()
    success = fixer.run_complete_fix()
    
    print()
    print("=" * 70)
    if success:
        print("🎉 MISSION ACCOMPLIE - POSTGRESQL UTF-8 OPÉRATIONNEL")
        print("✅ TaskMaster NextGeneration prêt pour production")
    else:
        print("❌ CORRECTION ÉCHOUÉE - VÉRIFIEZ LES LOGS")
        print("💡 Consultez le rapport généré pour plus de détails")
    
    input("Appuyez sur Entrée pour terminer...")
    return success

if __name__ == "__main__":
    main() 



