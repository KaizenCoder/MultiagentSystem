#!/usr/bin/env python3
"""
Script de Migration NextGeneration - Golden Source
=================================================

Migre automatiquement du logging Python standard vers NextGeneration.
Version propre et sécurisée basée sur la Golden Source.

Usage:
    python migrate_to_nextgen.py --file script.py
    python migrate_to_nextgen.py --directory /path/to/project
    python migrate_to_nextgen.py --batch files_list.txt
"""

import argparse
import ast
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class NextGenMigrator:
    """Migrateur propre vers NextGeneration"""
    
    def __init__(self, backup_enabled: bool = True, dry_run: bool = False):
        self.backup_enabled = backup_enabled
        self.dry_run = dry_run
        self.stats = {
            "files_processed": 0,
            "files_migrated": 0,
            "files_skipped": 0,
            "errors": 0,
            "backups_created": 0
        }
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def detect_script_type(self, filepath: str, content: str) -> str:
        """Détecte le type de script pour configuration appropriée"""
        
        filename = os.path.basename(filepath).lower()
        
        # Détection par nom de fichier
        if "agent" in filename:
            return "agent"
        elif "orchestrat" in filename:
            return "orchestrator"
        elif "template" in filename:
            return "template"
        elif "test" in filename:
            return "test"
        elif filename in ["logging_manager", "core", "factory"]:
            return "core"
        elif "api" in filename or "server" in filename:
            return "api"
        else:
            return "default"
    
    def analyze_logging_usage(self, content: str) -> Dict[str, any]:
        """Analyse l'usage du logging dans le fichier"""
        
        analysis = {
            "has_logging_import": False,
            "has_basicconfig": False,
            "has_getlogger": False,
            "logger_names": [],
            "logging_calls": 0,
            "needs_migration": False
        }
        
        lines = content.split('\n')
        
        for line in lines:
            line_stripped = line.strip()
            
            # Imports logging
            if re.match(r'^import\s+logging', line_stripped):
                analysis["has_logging_import"] = True
            elif re.match(r'^from\s+logging', line_stripped):
                analysis["has_logging_import"] = True
            
            # basicConfig
            if "logging.basicConfig" in line_stripped:
                analysis["has_basicconfig"] = True
            
            # getLogger
            if "logging.getLogger" in line_stripped:
                analysis["has_getlogger"] = True
                # Extraire le nom du logger
                match = re.search(r'logging\.getLogger\(["\']([^"\']+)["\']', line_stripped)
                if match:
                    analysis["logger_names"].append(match.group(1))
            
            # Appels de logging
            if re.search(r'\.(debug|info|warning|error|critical)\(', line_stripped):
                analysis["logging_calls"] += 1
        
        # Déterminer si migration nécessaire
        analysis["needs_migration"] = (
            analysis["has_logging_import"] and 
            (analysis["has_getlogger"] or analysis["logging_calls"] > 0)
        )
        
        return analysis
    
    def generate_nextgen_import(self, script_type: str, analysis: Dict[str, any]) -> str:
        """Génère l'import NextGeneration approprié"""
        
        if script_type == "agent":
            return """# NextGeneration Logging - Agent Configuration
from logging_manager_nextgen import get_agent_logger

# Configuration automatique pour agent IA
logger = get_agent_logger(
    agent_name=__name__.split('.')[-1],
    role="ai_processor",
    domain="general",
    async_enabled=True
)"""
        
        elif script_type == "orchestrator":
            return """# NextGeneration Logging - Orchestrator Configuration
from logging_manager_nextgen import NextGenLoggingManager

# Configuration pour orchestrateur
_manager = NextGenLoggingManager()
logger = _manager.get_logger(custom_config={
    "logger_name": __name__,
    "log_level": "INFO",
    "async_enabled": True,
    "elasticsearch_enabled": True,
    "encryption_enabled": True,
    "alerting_enabled": True,
    "high_throughput": True
})"""
        
        elif script_type == "core":
            return """# NextGeneration Logging - Core System Configuration
from logging_manager_nextgen import NextGenLoggingManager

# Configuration pour système core
_manager = NextGenLoggingManager()
logger = _manager.get_logger(custom_config={
    "logger_name": __name__,
    "log_level": "DEBUG",
    "async_enabled": True,
    "elasticsearch_enabled": True,
    "encryption_enabled": True,
    "audit_enabled": True,
    "advanced_monitoring_enabled": True
})"""
        
        else:  # default, test, api, template
            return """# NextGeneration Logging - Standard Configuration
from logging_manager_nextgen import get_logger

# Configuration standard NextGeneration
logger = get_logger(__name__)"""
    
    def migrate_file_content(self, content: str, filepath: str) -> Tuple[str, bool]:
        """Migre le contenu d'un fichier vers NextGeneration"""
        
        try:
            # Analyser le fichier
            analysis = self.analyze_logging_usage(content)
            
            if not analysis["needs_migration"]:
                return content, False
            
            # Détecter le type de script
            script_type = self.detect_script_type(filepath, content)
            
            # Générer le nouveau contenu
            lines = content.split('\n')
            new_lines = []
            nextgen_import_added = False
            
            for i, line in enumerate(lines):
                line_stripped = line.strip()
                
                # Remplacer les imports logging
                if re.match(r'^import\s+logging', line_stripped):
                    if not nextgen_import_added:
                        new_lines.append(self.generate_nextgen_import(script_type, analysis))
                        nextgen_import_added = True
                    # Commenter l'ancien import
                    new_lines.append(f"# {line}  # Remplacé par NextGeneration")
                    continue
                
                elif re.match(r'^from\s+logging', line_stripped):
                    if not nextgen_import_added:
                        new_lines.append(self.generate_nextgen_import(script_type, analysis))
                        nextgen_import_added = True
                    # Commenter l'ancien import
                    new_lines.append(f"# {line}  # Remplacé par NextGeneration")
                    continue
                
                # Remplacer basicConfig
                elif "logging.basicConfig" in line_stripped:
                    new_lines.append(f"# {line}  # Configuration gérée par NextGeneration")
                    continue
                
                # Remplacer getLogger
                elif "logging.getLogger" in line_stripped:
                    # Garder la ligne mais commentée pour référence
                    new_lines.append(f"# {line}  # Remplacé par configuration NextGeneration")
                    continue
                
                else:
                    new_lines.append(line)
            
            # Si aucun import NextGen ajouté, l'ajouter au début
            if not nextgen_import_added and analysis["needs_migration"]:
                # Trouver où insérer (après docstring/commentaires)
                insert_index = 0
                for i, line in enumerate(new_lines):
                    if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('"""'):
                        insert_index = i
                        break
                
                nextgen_import = self.generate_nextgen_import(script_type, analysis)
                new_lines.insert(insert_index, nextgen_import)
                new_lines.insert(insert_index + 1, "")
            
            new_content = '\n'.join(new_lines)
            
            # Validation syntaxique
            try:
                ast.parse(new_content)
                return new_content, True
            except SyntaxError as e:
                print(f"⚠️ Erreur syntaxe après migration {filepath}: {e}")
                return content, False
                
        except Exception as e:
            print(f"❌ Erreur migration {filepath}: {e}")
            return content, False
    
    def create_backup(self, filepath: str) -> bool:
        """Crée un backup du fichier original"""
        try:
            if not self.backup_enabled:
                return True
                
            backup_path = f"{filepath}.backup_{self.timestamp}"
            shutil.copy2(filepath, backup_path)
            self.stats["backups_created"] += 1
            return True
            
        except Exception as e:
            print(f"❌ Erreur création backup {filepath}: {e}")
            return False
    
    def migrate_file(self, filepath: str) -> bool:
        """Migre un fichier vers NextGeneration"""
        
        self.stats["files_processed"] += 1
        
        try:
            # Lire le fichier
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Migrer le contenu
            new_content, migrated = self.migrate_file_content(original_content, filepath)
            
            if not migrated:
                print(f"⏭️ Aucune migration nécessaire: {filepath}")
                self.stats["files_skipped"] += 1
                return True
            
            if self.dry_run:
                print(f"🔍 [DRY-RUN] Migrerait: {filepath}")
                self.stats["files_migrated"] += 1
                return True
            
            # Créer backup
            if not self.create_backup(filepath):
                return False
            
            # Écrire le nouveau contenu
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Migré avec succès: {filepath}")
            self.stats["files_migrated"] += 1
            return True
            
        except Exception as e:
            print(f"❌ Erreur migration {filepath}: {e}")
            self.stats["errors"] += 1
            return False
    
    def migrate_directory(self, directory: str, recursive: bool = True) -> List[str]:
        """Migre tous les fichiers Python d'un répertoire"""
        
        migrated_files = []
        directory_path = Path(directory)
        
        if not directory_path.exists():
            print(f"❌ Répertoire non trouvé: {directory}")
            return migrated_files
        
        # Trouver tous les fichiers Python
        pattern = "**/*.py" if recursive else "*.py"
        python_files = list(directory_path.glob(pattern))
        
        print(f"🔍 Découvert {len(python_files)} fichiers Python dans {directory}")
        
        for file_path in python_files:
            # Ignorer les backups existants
            if ".backup_" in str(file_path):
                continue
                
            if self.migrate_file(str(file_path)):
                migrated_files.append(str(file_path))
        
        return migrated_files
    
    def print_summary(self):
        """Affiche le résumé de la migration"""
        print("\n" + "="*60)
        print("📊 RÉSUMÉ DE LA MIGRATION NEXTGENERATION")
        print("="*60)
        print(f"📁 Fichiers traités: {self.stats['files_processed']}")
        print(f"✅ Fichiers migrés: {self.stats['files_migrated']}")
        print(f"⏭️ Fichiers ignorés: {self.stats['files_skipped']}")
        print(f"❌ Erreurs: {self.stats['errors']}")
        print(f"💾 Backups créés: {self.stats['backups_created']}")
        
        if self.stats['files_migrated'] > 0:
            print(f"\n🎉 Migration réussie!")
            if self.backup_enabled:
                print(f"🔄 Rollback possible avec les fichiers .backup_{self.timestamp}")
        
        if self.stats['errors'] > 0:
            print(f"\n⚠️ {self.stats['errors']} erreurs détectées - vérifiez les logs")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Migration vers NextGeneration Logging System"
    )
    
    parser.add_argument(
        "--file", 
        help="Fichier unique à migrer"
    )
    parser.add_argument(
        "--directory", 
        help="Répertoire à migrer (récursif)"
    )
    parser.add_argument(
        "--batch", 
        help="Fichier contenant la liste des fichiers à migrer"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Simulation sans modification des fichiers"
    )
    parser.add_argument(
        "--no-backup", 
        action="store_true",
        help="Désactiver la création de backups"
    )
    
    args = parser.parse_args()
    
    if not any([args.file, args.directory, args.batch]):
        parser.print_help()
        return
    
    # Initialiser le migrateur
    migrator = NextGenMigrator(
        backup_enabled=not args.no_backup,
        dry_run=args.dry_run
    )
    
    print("🚀 NextGeneration Migration Tool - Golden Source")
    print("="*50)
    
    if args.dry_run:
        print("🔍 MODE DRY-RUN - Aucune modification ne sera effectuée")
    
    # Exécuter la migration
    if args.file:
        print(f"📄 Migration fichier unique: {args.file}")
        migrator.migrate_file(args.file)
    
    elif args.directory:
        print(f"📁 Migration répertoire: {args.directory}")
        migrator.migrate_directory(args.directory)
    
    elif args.batch:
        print(f"📋 Migration par batch: {args.batch}")
        try:
            with open(args.batch, 'r') as f:
                files = [line.strip() for line in f if line.strip()]
            
            for file_path in files:
                migrator.migrate_file(file_path)
                
        except Exception as e:
            print(f"❌ Erreur lecture batch: {e}")
    
    # Afficher le résumé
    migrator.print_summary()

if __name__ == "__main__":
    main() 