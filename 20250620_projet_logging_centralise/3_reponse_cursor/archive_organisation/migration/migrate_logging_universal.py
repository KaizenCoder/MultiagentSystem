#!/usr/bin/env python3
"""
SCRIPT DE MIGRATION UNIVERSEL - LoggingManager NextGeneration
Migre automatiquement TOUS les scripts Python vers le nouveau système de logging centralisé

Usage:
    python migrate_logging_universal.py --file <chemin_fichier> --script-type <type>
    python migrate_logging_universal.py --batch <fichier_liste> --script-type <type>
    python migrate_logging_universal.py --all --dry-run

Types de scripts supportés: agent, template, orchestrator, test, core, api, tool
"""

import argparse
import shutil
import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class UniversalLoggingMigrator:
    """Migrateur automatisé universel vers LoggingManager NextGeneration"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.migration_log = []
        self.errors = []
        self.success_count = 0
        self.total_count = 0
        
        # Templates de configuration par type de script
        self.script_configs = {
            "agent": {
                "template": """
        # LoggingManager NextGeneration - Agent
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="{script_name}",
            role="ai_processor",
            domain="{domain}",
            async_enabled=True
        )""",
                "import": "from logging_manager_optimized import LoggingManager"
            },
            
            "template": {
                "template": """
        # LoggingManager NextGeneration - Template Manager
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={{
            "logger_name": "{script_name}",
            "log_level": "INFO",
            "elasticsearch_enabled": True,
            "encryption_enabled": False,
            "async_enabled": True,
            "structured_logging": True
        }})""",
                "import": "from logging_manager_optimized import LoggingManager"
            },
            
            "orchestrator": {
                "template": """
        # LoggingManager NextGeneration - Orchestrateur
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={{
            "logger_name": "{script_name}",
            "log_level": "INFO",
            "elasticsearch_enabled": True,
            "encryption_enabled": True,
            "async_enabled": True,
            "alerting_enabled": True,
            "high_throughput": True
        }})""",
                "import": "from logging_manager_optimized import LoggingManager"
            },
            
            "test": {
                "template": """
        # LoggingManager NextGeneration - Tests
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={{
            "logger_name": "{script_name}",
            "log_level": "DEBUG",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": False,  # Tests synchrones
            "console_output": True
        }})""",
                "import": "from logging_manager_optimized import LoggingManager"
            },
            
            "core": {
                "template": """
        # LoggingManager NextGeneration - Core System
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={{
            "logger_name": "{script_name}",
            "log_level": "INFO",
            "elasticsearch_enabled": True,
            "encryption_enabled": True,
            "async_enabled": True,
            "audit_enabled": True,
            "high_throughput": True
        }})""",
                "import": "from logging_manager_optimized import LoggingManager"
            },
            
            "api": {
                "template": """
        # LoggingManager NextGeneration - API
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={{
            "logger_name": "{script_name}",
            "log_level": "INFO",
            "elasticsearch_enabled": True,
            "encryption_enabled": False,
            "async_enabled": True,
            "request_tracking": True
        }})""",
                "import": "from logging_manager_optimized import LoggingManager"
            },
            
            "tool": {
                "template": """
        # LoggingManager NextGeneration - Tool/Utility
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={{
            "logger_name": "{script_name}",
            "log_level": "INFO",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": True
        }})""",
                "import": "from logging_manager_optimized import LoggingManager"
            }
        }
    
    def detect_script_type_from_file(self, file_path: str) -> str:
        """Détecte automatiquement le type de script selon le chemin/contenu"""
        
        path_lower = file_path.lower()
        filename = Path(file_path).name.lower()
        
        # Détection par nom de fichier
        if filename.startswith("test_"):
            return "test"
        elif "template_manager" in filename:
            return "template"
        elif "orchestrat" in filename:
            return "orchestrator"
        elif "agent_coordinateur" in filename:
            return "orchestrator"
        elif filename.startswith("agent_") or "agent" in path_lower:
            return "agent"
        elif "logging_manager" in filename:
            return "core"
        elif "api" in path_lower or "endpoint" in path_lower:
            return "api"
        elif "tool" in path_lower or "util" in path_lower:
            return "tool"
        elif "core" in path_lower or "factory" in path_lower:
            return "core"
        else:
            return "tool"  # Par défaut
    
    def get_all_python_files_with_logging(self) -> List[str]:
        """Trouve tous les fichiers Python utilisant le logging dans le workspace"""
        
        python_files = []
        workspace_root = Path("../../")  # Remonte au workspace root
        
        # Patterns de logging à rechercher
        logging_patterns = [
            r'import logging',
            r'from logging import',
            r'logging\.getLogger',
            r'logging\.basicConfig',
            r'logger\s*=.*logging'
        ]
        
        for py_file in workspace_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Vérifie si le fichier utilise le logging standard
                for pattern in logging_patterns:
                    if re.search(pattern, content):
                        # Exclut les fichiers déjà migrés
                        if "logging_manager_optimized" not in content:
                            python_files.append(str(py_file.relative_to(workspace_root)))
                        break
            except Exception as e:
                self.error(f"Erreur lecture {py_file}: {e}")
        
        return python_files
    
    def create_backup(self, file_path: str) -> str:
        """Crée une sauvegarde du fichier original"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.backup_{timestamp}"
        
        if not self.dry_run:
            shutil.copy2(file_path, backup_path)
            
        self.log(f"✅ Backup créé: {backup_path}")
        return backup_path
    
    def extract_script_info(self, content: str, file_path: str) -> Dict[str, str]:
        """Extrait les informations du script depuis le contenu"""
        
        # Extraction du nom de classe ou fonction principale
        class_match = re.search(r'class\s+(\w+)', content)
        if class_match:
            script_name = class_match.group(1)
        else:
            # Fallback sur le nom de fichier
            script_name = Path(file_path).stem
        
        # Détection du domaine basé sur le fichier
        if "nlp" in file_path.lower() or "natural" in file_path.lower():
            domain = "natural_language"
        elif "performance" in file_path.lower():
            domain = "performance"
        elif "security" in file_path.lower():
            domain = "security"
        elif "coordination" in file_path.lower() or "orchestrat" in file_path.lower():
            domain = "orchestration"
        elif "monitoring" in file_path.lower():
            domain = "monitoring"
        elif "template" in file_path.lower():
            domain = "template_management"
        elif "test" in file_path.lower():
            domain = "testing"
        elif "api" in file_path.lower():
            domain = "api"
        else:
            domain = "general"
        
        return {
            "script_name": script_name,
            "domain": domain
        }
    
    def migrate_imports(self, content: str) -> str:
        """Migre les imports de logging"""
        
        # Remplacer import logging
        content = re.sub(
            r'^import logging$',
            'from logging_manager_optimized import LoggingManager',
            content,
            flags=re.MULTILINE
        )
        
        # Remplacer from logging import ...
        content = re.sub(
            r'^from logging import.*$',
            'from logging_manager_optimized import LoggingManager',
            content,
            flags=re.MULTILINE
        )
        
        return content
    
    def migrate_logger_initialization(self, content: str, script_type: str, script_info: Dict) -> str:
        """Migre l'initialisation du logger"""
        
        config_template = self.script_configs[script_type]["template"]
        new_logger_init = config_template.format(**script_info).strip()
        
        # Patterns d'ancien logger à remplacer
        old_patterns = [
            r'self\.logger\s*=\s*logging\.getLogger\([^)]*\)',
            r'logger\s*=\s*logging\.getLogger\([^)]*\)',
            r'self\.logger\s*=\s*logging\.getLogger\(__name__\)',
            r'logger\s*=\s*logging\.getLogger\(__name__\)',
            r'logging\.basicConfig\([^)]*\)'
        ]
        
        # Remplace le premier pattern trouvé
        for pattern in old_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, new_logger_init, content, count=1)
                break
        
        return content
    
    def migrate_file(self, file_path: str, script_type: Optional[str] = None) -> bool:
        """Migre un fichier vers LoggingManager NextGeneration"""
        
        try:
            self.total_count += 1
            
            # Chemin absolu
            abs_path = Path("../../") / file_path if not Path(file_path).is_absolute() else Path(file_path)
            
            if not abs_path.exists():
                self.error(f"❌ Fichier non trouvé: {file_path}")
                return False
            
            # Lecture du contenu
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérification si déjà migré
            if "logging_manager_optimized" in content:
                self.log(f"⚠️ Déjà migré: {file_path}")
                return True
            
            # Détection automatique du type si non spécifié
            if not script_type:
                script_type = self.detect_script_type_from_file(str(abs_path))
            
            self.log(f"🔄 Migration {file_path} (type: {script_type})")
            
            # Création backup
            if not self.dry_run:
                self.create_backup(str(abs_path))
            
            # Extraction des informations du script
            script_info = self.extract_script_info(content, str(abs_path))
            
            # Migration des imports
            content = self.migrate_imports(content)
            
            # Migration de l'initialisation du logger
            content = self.migrate_logger_initialization(content, script_type, script_info)
            
            # Écriture du fichier migré
            if not self.dry_run:
                with open(abs_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            self.success_count += 1
            self.log(f"✅ Migration réussie: {file_path}")
            return True
            
        except Exception as e:
            self.error(f"❌ Erreur migration {file_path}: {e}")
            return False
    
    def migrate_all_discovered(self) -> Dict:
        """Migre tous les fichiers Python découverts utilisant le logging"""
        
        self.log("🔍 Découverte automatique des fichiers Python avec logging...")
        
        files_to_migrate = self.get_all_python_files_with_logging()
        
        self.log(f"📋 {len(files_to_migrate)} fichiers découverts")
        
        results = {
            "total": len(files_to_migrate),
            "success": 0,
            "errors": 0,
            "files": []
        }
        
        for file_path in files_to_migrate:
            script_type = self.detect_script_type_from_file(file_path)
            success = self.migrate_file(file_path, script_type)
            
            results["files"].append({
                "file": file_path,
                "type": script_type,
                "success": success
            })
            
            if success:
                results["success"] += 1
            else:
                results["errors"] += 1
        
        return results
    
    def generate_report(self) -> str:
        """Génère un rapport de migration"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"migration_report_universal_{timestamp}.md"
        
        report = f"""# 📊 RAPPORT MIGRATION UNIVERSELLE - {timestamp}

## 🎯 RÉSULTATS GLOBAUX

- **Total fichiers traités** : {self.total_count}
- **Migrations réussies** : {self.success_count}
- **Erreurs** : {len(self.errors)}
- **Taux de réussite** : {(self.success_count/self.total_count*100) if self.total_count > 0 else 0:.1f}%

## ✅ SUCCÈS

{chr(10).join(self.migration_log)}

## ❌ ERREURS

{chr(10).join(self.errors) if self.errors else "Aucune erreur"}

---
Rapport généré le {datetime.now().isoformat()}
"""
        
        if not self.dry_run:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
        
        return report_path
    
    def log(self, message: str):
        """Enregistre un message de log"""
        print(message)
        self.migration_log.append(message)
    
    def error(self, message: str):
        """Enregistre une erreur"""
        print(message)
        self.errors.append(message)

def main():
    """Point d'entrée principal"""
    
    parser = argparse.ArgumentParser(
        description="Migration universelle vers LoggingManager NextGeneration"
    )
    
    parser.add_argument("--file", help="Fichier à migrer")
    parser.add_argument("--script-type", 
                       choices=["agent", "template", "orchestrator", "test", "core", "api", "tool"],
                       help="Type de script")
    parser.add_argument("--all", action="store_true", 
                       help="Migrer tous les fichiers découverts automatiquement")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Mode simulation (pas de modifications)")
    
    args = parser.parse_args()
    
    migrator = UniversalLoggingMigrator(dry_run=args.dry_run)
    
    if args.all:
        print("🚀 MIGRATION UNIVERSELLE - TOUS LES FICHIERS PYTHON")
        results = migrator.migrate_all_discovered()
        
        print(f"\n📊 RÉSULTATS FINAUX:")
        print(f"✅ Succès: {results['success']}")
        print(f"❌ Erreurs: {results['errors']}")
        print(f"📋 Total: {results['total']}")
        
    elif args.file:
        print(f"🔄 MIGRATION FICHIER: {args.file}")
        success = migrator.migrate_file(args.file, args.script_type)
        
        if success:
            print("✅ Migration réussie!")
        else:
            print("❌ Migration échouée!")
    
    else:
        parser.print_help()
        return
    
    # Génération du rapport
    report_path = migrator.generate_report()
    print(f"\n📄 Rapport généré: {report_path}")

if __name__ == "__main__":
    main() 