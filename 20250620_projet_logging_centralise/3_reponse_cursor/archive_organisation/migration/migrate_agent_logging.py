#!/usr/bin/env python3
"""
SCRIPT DE MIGRATION AUTOMATISÉ - LoggingManager NextGeneration
Migre automatiquement les agents vers le nouveau système de logging centralisé

Usage:
    python migrate_agent_logging.py --file <chemin_fichier> --agent-type <type>
    python migrate_agent_logging.py --batch <fichier_liste> --agent-type <type>
    python migrate_agent_logging.py --all --dry-run

Types d'agents supportés: standard, coordinateur, outil, performance, security
"""

import argparse
import shutil
import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class LoggingMigrator:
    """Migrateur automatisé vers LoggingManager NextGeneration"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.migration_log = []
        self.errors = []
        self.success_count = 0
        self.total_count = 0
        
        # Templates de configuration par type d'agent
        self.agent_configs = {
            "standard": {
                "template": """
        # LoggingManager NextGeneration - Agent Standard
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="{agent_name}",
            role="ai_processor",
            domain="{domain}",
            async_enabled=True
        )""",
                "import": "import sys
from pathlib import Path
from core import logging_manager"
            },
            
            "coordinateur": {
                "template": """
        # LoggingManager NextGeneration - Coordinateur
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = logging_manager.get_logger(custom_config={{
            "logger_name": "{agent_name}",
            "log_level": "INFO",
            "elasticsearch_enabled": True,
            "encryption_enabled": True,
            "async_enabled": True,
            "alerting_enabled": True
        }})""",
                "import": "import sys
from pathlib import Path
from core import logging_manager"
            },
            
            "outil": {
                "template": """
        # LoggingManager NextGeneration - Outil
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = logging_manager.get_logger(custom_config={{
            "logger_name": "{agent_name}",
            "log_level": "INFO",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": True
        }})""",
                "import": "import sys
from pathlib import Path
from core import logging_manager"
            },
            
            "performance": {
                "template": """
        # LoggingManager NextGeneration - Performance
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = logging_manager.get_logger(custom_config={{
            "logger_name": "{agent_name}",
            "log_level": "INFO",
            "elasticsearch_enabled": True,
            "encryption_enabled": False,
            "async_enabled": True,
            "high_throughput": True
        }})""",
                "import": "import sys
from pathlib import Path
from core import logging_manager"
            },
            
            "security": {
                "template": """
        # LoggingManager NextGeneration - Sécurité
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = logging_manager.get_logger(custom_config={{
            "logger_name": "{agent_name}",
            "log_level": "INFO",
            "elasticsearch_enabled": True,
            "encryption_enabled": True,
            "async_enabled": True,
            "audit_enabled": True
        }})""",
                "import": "import sys
from pathlib import Path
from core import logging_manager"
            }
        }
    
    def detect_agent_type_from_file(self, file_path: str) -> str:
        """Détecte automatiquement le type d'agent selon le chemin/contenu"""
        
        path_lower = file_path.lower()
        
        # Détection par chemin
        if "coordinateur" in path_lower or "coordination" in path_lower:
            return "coordinateur"
        elif "security" in path_lower or "secure" in path_lower:
            return "security"
        elif "performance" in path_lower or "optimization" in path_lower:
            return "performance"
        elif "tools/" in path_lower or "outil" in path_lower:
            return "outil"
        elif "orchestrator" in path_lower:
            return "coordinateur"  # Orchestrateur = coordinateur
        else:
            return "standard"  # Par défaut
    
    def create_backup(self, file_path: str) -> str:
        """Crée une sauvegarde du fichier original"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.backup_{timestamp}"
        
        if not self.dry_run:
            shutil.copy2(file_path, backup_path)
            
        self.log(f"✅ Backup créé: {backup_path}")
        return backup_path
    
    def extract_agent_info(self, content: str, file_path: str) -> Dict[str, str]:
        """Extrait les informations de l'agent depuis le contenu"""
        
        # Extraction du nom de classe (agent name)
        class_match = re.search(r'class\s+(\w+)', content)
        if class_match:
            agent_name = class_match.group(1)
        else:
            # Fallback sur le nom de fichier
            agent_name = Path(file_path).stem
        
        # Détection du domaine basé sur le fichier
        if "nlp" in file_path.lower() or "natural" in file_path.lower():
            domain = "natural_language"
        elif "performance" in file_path.lower():
            domain = "performance"
        elif "security" in file_path.lower():
            domain = "security"
        elif "coordination" in file_path.lower():
            domain = "orchestration"
        elif "monitoring" in file_path.lower():
            domain = "monitoring"
        else:
            domain = "general"
        
        return {
            "agent_name": agent_name,
            "domain": domain
        }
    
    def migrate_imports(self, content: str) -> str:
        """Migre les imports de logging"""
        
        # Remplacer import logging
        content = re.sub(
            r'^import logging$',
            'import sys
from pathlib import Path
from core import logging_manager',
            content,
            flags=re.MULTILINE
        )
        
        # Remplacer from logging import ...
        content = re.sub(
            r'^from logging import.*$',
            'import sys
from pathlib import Path
from core import logging_manager',
            content,
            flags=re.MULTILINE
        )
        
        return content
    
    def migrate_logger_initialization(self, content: str, agent_type: str, agent_info: Dict) -> str:
        """Migre l'initialisation du logger"""
        
        config_template = self.agent_configs[agent_type]["template"]
        new_logger_init = config_template.format(**agent_info).strip()
        
        # Patterns d'ancien logger à remplacer
        old_patterns = [
            r'self\.logger\s*=\s*logging\.getLogger\([^)]*\)',
            r'logger\s*=\s*logging\.getLogger\([^)]*\)',
            r'self\.logger\s*=\s*logging\.getLogger\(__name__\)',
            r'logger\s*=\s*logging\.getLogger\(__name__\)'
        ]
        
        for pattern in old_patterns:
            content = re.sub(pattern, new_logger_init, content, flags=re.MULTILINE)
        
        return content
    
    def migrate_basic_config(self, content: str) -> str:
        """Supprime les logging.basicConfig (remplacé par LoggingManager)"""
        
        # Supprimer logging.basicConfig avec gestion multi-lignes
        content = re.sub(
            r'logging\.basicConfig\([^)]*\)\s*',
            '# Configuration logging gérée par LoggingManager NextGeneration\n',
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        return content
    
    def migrate_file(self, file_path: str, agent_type: Optional[str] = None) -> bool:
        """Migre un fichier vers le nouveau système de logging"""
        
        self.total_count += 1
        
        try:
            # Vérification existence fichier
            if not os.path.exists(file_path):
                self.error(f"❌ Fichier introuvable: {file_path}")
                return False
            
            # Détection automatique du type d'agent si non spécifié
            if not agent_type:
                agent_type = self.detect_agent_type_from_file(file_path)
            
            self.log(f"🔄 Migration {agent_type}: {file_path}")
            
            # Lecture du contenu
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Vérification si déjà migré
            if "LoggingManager" in original_content:
                self.log(f"⚠️  Déjà migré: {file_path}")
                return True
            
            # Création du backup
            backup_path = self.create_backup(file_path)
            
            # Extraction infos agent
            agent_info = self.extract_agent_info(original_content, file_path)
            
            # Migration étape par étape
            migrated_content = original_content
            
            # 1. Migration des imports
            migrated_content = self.migrate_imports(migrated_content)
            
            # 2. Migration initialisation logger
            migrated_content = self.migrate_logger_initialization(
                migrated_content, agent_type, agent_info
            )
            
            # 3. Migration basicConfig
            migrated_content = self.migrate_basic_config(migrated_content)
            
            # Écriture du fichier migré
            if not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(migrated_content)
            
            self.log(f"✅ Migration réussie: {file_path}")
            self.success_count += 1
            return True
            
        except Exception as e:
            self.error(f"❌ Erreur migration {file_path}: {e}")
            return False
    
    def migrate_batch(self, file_list: List[str], agent_type: str) -> Dict:
        """Migre une liste de fichiers"""
        
        results = {
            "success": [],
            "errors": [],
            "total": len(file_list)
        }
        
        self.log(f"🚀 Début migration batch - {len(file_list)} fichiers")
        
        for file_path in file_list:
            if self.migrate_file(file_path, agent_type):
                results["success"].append(file_path)
            else:
                results["errors"].append(file_path)
        
        return results
    
    def generate_report(self) -> str:
        """Génère un rapport de migration"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = f"""
# RAPPORT DE MIGRATION LOGGING NEXTGENERATION
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Mode: {"DRY RUN" if self.dry_run else "PRODUCTION"}

## RÉSULTATS
- Total fichiers traités: {self.total_count}
- Migrations réussies: {self.success_count}
- Erreurs: {len(self.errors)}
- Taux de succès: {(self.success_count/self.total_count*100) if self.total_count > 0 else 0:.1f}%

## LOGS DE MIGRATION
{chr(10).join(self.migration_log)}

## ERREURS
{chr(10).join(self.errors) if self.errors else "Aucune erreur"}

---
Migration générée par LoggingManager NextGeneration
"""
        
        report_path = f"migration_report_{timestamp}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report_path
    
    def log(self, message: str):
        """Ajoute un message au log de migration"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.migration_log.append(log_entry)
        print(log_entry)
    
    def error(self, message: str):
        """Ajoute une erreur au log"""
        self.errors.append(message)
        self.log(message)

def load_file_list(list_file: str) -> List[str]:
    """Charge une liste de fichiers depuis un fichier texte"""
    with open(list_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def get_critical_files() -> List[str]:
    """Retourne la liste des fichiers critiques à migrer en priorité"""
    return [
        # 🏗️ ARCHITECTURE CORE - PRIORITÉ ABSOLUE
        "agent_factory_implementation/core/agent_factory_architecture.py",  # ⚡ Pattern Factory Core - 21 occurrences logging
        
        # Coordination centrale
        "agent_factory_implementation/agents/agent_01_coordinateur_principal.py",
        "coordinateur_equipe_tools_apex.py", 
        "coordinateur_equipe_tools.py",
        "20250620_transformation_equipe_maintenance/agent_equipe_maintenance/agent_MAINTENANCE_00_chef_equipe_coordinateur.py",
        
        # Orchestration système
        "orchestrator/app/main.py",
        "orchestrator/app/agents/advanced_coordination.py",
        "orchestrator/app/agents/advanced_statistics.py",
        "orchestrator/app/core/task_manager.py",
        "orchestrator/app/monitoring/system_monitor.py",
        
        # API critiques
        "memory_api/app/main.py",
        "memory_api/app/core/memory_manager.py", 
        "memory_api/app/api/endpoints.py",
        
        # Agents spécialisés critiques
        "agents/agent_02_architecte_code_expert.py",
        "agents/agent_03_specialiste_configuration.py",
        "agents/agent_04_analyste_performance.py"
    ]

def main():
    parser = argparse.ArgumentParser(description="Migration vers LoggingManager NextGeneration")
    
    # Arguments principaux
    parser.add_argument('--file', help='Fichier unique à migrer')
    parser.add_argument('--batch', help='Fichier contenant liste de fichiers à migrer')
    parser.add_argument('--critical', action='store_true', help='Migrer les fichiers critiques')
    parser.add_argument('--all', action='store_true', help='Migrer tous les fichiers détectés')
    
    # Configuration
    parser.add_argument('--agent-type', 
                       choices=['standard', 'coordinateur', 'outil', 'performance', 'security'],
                       help='Type d\'agent (détection auto si omis)')
    parser.add_argument('--dry-run', action='store_true', help='Simulation sans modification')
    parser.add_argument('--report', help='Chemin du rapport de migration')
    
    args = parser.parse_args()
    
    # Initialisation du migrateur
    migrator = LoggingMigrator(dry_run=args.dry_run)
    
    if args.dry_run:
        migrator.log("🔍 MODE DRY RUN - Aucune modification ne sera effectuée")
    
    try:
        # Migration fichier unique
        if args.file:
            migrator.migrate_file(args.file, args.agent_type)
        
        # Migration batch
        elif args.batch:
            file_list = load_file_list(args.batch)
            migrator.migrate_batch(file_list, args.agent_type or 'standard')
        
        # Migration fichiers critiques
        elif args.critical:
            critical_files = get_critical_files()
            migrator.migrate_batch(critical_files, 'coordinateur')
        
        # Migration complète (à implémenter avec prudence)
        elif args.all:
            migrator.log("⚠️  Migration complète non implémentée pour sécurité")
            migrator.log("   Utilisez --critical ou --batch à la place")
        
        else:
            parser.print_help()
            return
        
        # Génération du rapport
        report_path = migrator.generate_report()
        migrator.log(f"📊 Rapport généré: {report_path}")
        
        # Résumé final
        if migrator.success_count > 0:
            migrator.log(f"🎉 Migration terminée: {migrator.success_count}/{migrator.total_count} réussies")
        else:
            migrator.log("❌ Aucune migration réussie")
    
    except KeyboardInterrupt:
        migrator.log("⚠️  Migration interrompue par l'utilisateur")
    except Exception as e:
        migrator.error(f"❌ Erreur fatale: {e}")

if __name__ == "__main__":
    main() 



