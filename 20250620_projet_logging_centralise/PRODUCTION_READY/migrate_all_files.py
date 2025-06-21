#!/usr/bin/env python3
"""
MIGRATION AUTOMATIQUE - 849 FICHIERS PYTHON
Migre TOUS les scripts du workspace vers le logging centralisé NextGeneration

Auteur: NextGeneration Team
Version: 2.0.0
Date: 2025-06-21
"""

import os
import re
import shutil
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime

class NextGenMigrationTool:
    """Outil de migration automatique pour le logging centralisé"""
    
    def __init__(self, workspace_root: str, production_ready_path: str):
        self.workspace_root = Path(workspace_root)
        self.production_ready_path = Path(production_ready_path)
        self.stats = {
            'total_files': 0,
            'migrated': 0,
            'errors': 0,
            'skipped': 0,
            'categories': {}
        }
        self.migration_log = []
        
    def scan_all_python_files(self, category_filter: str = None) -> List[Path]:
        """Scanne tous les fichiers Python du workspace"""
        python_files = []
        for file_path in self.workspace_root.rglob("*.py"):
            if not self._should_skip_file(file_path):
                if category_filter is None or self._get_file_category(file_path) == category_filter:
                    python_files.append(file_path)
        return python_files
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Détermine si un fichier doit être ignoré"""
        skip_patterns = [
            'PRODUCTION_READY',
            '__pycache__',
            '.git',
            'venv',
            'env',
            '.pytest_cache',
            'node_modules',
            '.backup',
            'migrate_all_files.py'  # Ne pas migrer ce script
        ]
        return any(pattern in str(file_path) for pattern in skip_patterns)
    
    def analyze_file(self, file_path: Path) -> Dict[str, any]:
        """Analyse un fichier pour déterminer le type de migration"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {'error': str(e), 'needs_migration': False}
        
        analysis = {
            'has_logging_import': 'import logging' in content,
            'has_basicconfig': 'logging.basicConfig' in content,
            'has_getlogger': 'logging.getLogger' in content,
            'has_logging_manager': 'logging_manager_optimized' in content,
            'needs_migration': False,
            'migration_type': 'none',
            'category': self._get_file_category(file_path),
            'file_size': len(content),
            'lines_count': len(content.split('\n'))
        }
        
        # Détermine le type de migration nécessaire
        if analysis['has_basicconfig'] or (analysis['has_getlogger'] and not analysis['has_logging_manager']):
            analysis['needs_migration'] = True
            if analysis['has_basicconfig']:
                analysis['migration_type'] = 'basicconfig'
            else:
                analysis['migration_type'] = 'getlogger'
        elif analysis['has_logging_manager']:
            analysis['migration_type'] = 'already_using_manager'
        
        return analysis
    
    def _get_file_category(self, file_path: Path) -> str:
        """Détermine la catégorie du fichier"""
        path_str = str(file_path).lower()
        
        if 'agent' in path_str:
            return 'agents'
        elif 'tools' in path_str:
            return 'tools'
        elif 'scripts' in path_str:
            return 'scripts'
        elif 'orchestrator' in path_str:
            return 'orchestrator'
        elif 'tests' in path_str or 'test_' in file_path.name:
            return 'tests'
        elif 'docs' in path_str:
            return 'docs'
        elif 'memory_api' in path_str:
            return 'memory_api'
        elif 'monitoring' in path_str:
            return 'monitoring'
        else:
            return 'autres'
    
    def migrate_file(self, file_path: Path, analysis: Dict, dry_run: bool = False) -> bool:
        """Migre un fichier vers le logging centralisé"""
        try:
            # Backup du fichier original
            backup_path = file_path.with_suffix(f'.py.backup_migration_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            
            if not dry_run:
                shutil.copy2(file_path, backup_path)
            
            # Lecture du contenu
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Migration selon le type
            if analysis['migration_type'] == 'basicconfig':
                new_content = self._migrate_basicconfig(content, analysis['category'], file_path)
            elif analysis['migration_type'] == 'getlogger':
                new_content = self._migrate_getlogger(content, analysis['category'], file_path)
            else:
                return False
            
            # Écriture du nouveau contenu
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            # Log de la migration
            log_entry = {
                'file': str(file_path.relative_to(self.workspace_root)),
                'category': analysis['category'],
                'migration_type': analysis['migration_type'],
                'backup': str(backup_path.relative_to(self.workspace_root)) if not dry_run else 'dry_run',
                'timestamp': datetime.now().isoformat()
            }
            self.migration_log.append(log_entry)
            
            return True
            
        except Exception as e:
            error_msg = f"❌ Erreur migration {file_path.relative_to(self.workspace_root)}: {e}"
            print(error_msg)
            self.migration_log.append({
                'file': str(file_path.relative_to(self.workspace_root)),
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return False
    
    def _migrate_basicconfig(self, content: str, category: str, file_path: Path) -> str:
        """Migre un fichier utilisant logging.basicConfig"""
        lines = content.split('\n')
        new_lines = []
        imports_added = False
        basicconfig_replaced = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            line_stripped = line.strip()
            
            # Ajouter les imports nécessaires après les imports existants
            if (line_stripped.startswith('import ') or line_stripped.startswith('from ')) and not imports_added:
                # Collecter tous les imports
                import_lines = []
                while i < len(lines) and (lines[i].strip().startswith(('import ', 'from ')) or lines[i].strip() == ''):
                    import_lines.append(lines[i])
                    i += 1
                
                # Ajouter les imports existants
                new_lines.extend(import_lines)
                
                # Ajouter nos imports
                new_lines.extend([
                    '',
                    '# Migration vers logging centralisé NextGeneration',
                    'import sys',
                    'import os',
                    f'sys.path.append(r"{self.production_ready_path.absolute()}")',
                    'from core.logging_manager_optimized import LoggingManager',
                    ''
                ])
                imports_added = True
                continue
            
            # Remplacer logging.basicConfig
            elif 'logging.basicConfig' in line_stripped and not basicconfig_replaced:
                indent = line[:len(line) - len(line.lstrip())]
                
                # Extraire le niveau de log si présent
                log_level = 'INFO'
                if 'level=logging.DEBUG' in line:
                    log_level = 'DEBUG'
                elif 'level=logging.WARNING' in line:
                    log_level = 'WARNING'
                elif 'level=logging.ERROR' in line:
                    log_level = 'ERROR'
                
                new_lines.extend([
                    f'{indent}# Migration: Ancien logging.basicConfig remplacé',
                    f'{indent}# {line_stripped}',
                    f'{indent}manager = LoggingManager()',
                    f'{indent}logger = manager.get_logger(custom_config={{',
                    f'{indent}    "logger_name": "{category}.{file_path.stem}",',
                    f'{indent}    "log_level": "{log_level}",',
                    f'{indent}    "console_enabled": True,',
                    f'{indent}    "file_enabled": True',
                    f'{indent}}})'
                ])
                basicconfig_replaced = True
            
            # Remplacer logging.getLogger
            elif 'logging.getLogger' in line_stripped:
                # Remplacer par logger déjà créé
                new_line = re.sub(r'logging\.getLogger\([^)]*\)', 'logger', line)
                new_lines.append(new_line)
            
            else:
                new_lines.append(line)
            
            i += 1
        
        return '\n'.join(new_lines)
    
    def _migrate_getlogger(self, content: str, category: str, file_path: Path) -> str:
        """Migre un fichier utilisant logging.getLogger sans basicConfig"""
        return self._migrate_basicconfig(content, category, file_path)
    
    def run_migration(self, category_filter: str = None, dry_run: bool = False) -> Dict:
        """Exécute la migration complète"""
        print("🚀 DÉMARRAGE MIGRATION MASSIVE - NEXTGENERATION LOGGING")
        print("=" * 70)
        
        if dry_run:
            print("🔍 MODE DRY RUN - Aucun fichier ne sera modifié")
        
        if category_filter:
            print(f"📂 Filtrage par catégorie: {category_filter}")
        
        # 1. Scanner tous les fichiers
        python_files = self.scan_all_python_files(category_filter)
        self.stats['total_files'] = len(python_files)
        
        print(f"📊 {len(python_files)} fichiers Python trouvés")
        print("-" * 70)
        
        # 2. Analyser et migrer chaque fichier
        for file_path in python_files:
            analysis = self.analyze_file(file_path)
            category = analysis['category']
            
            if category not in self.stats['categories']:
                self.stats['categories'][category] = {'total': 0, 'migrated': 0, 'errors': 0}
            
            self.stats['categories'][category]['total'] += 1
            
            if analysis['needs_migration']:
                success = self.migrate_file(file_path, analysis, dry_run)
                if success:
                    self.stats['migrated'] += 1
                    self.stats['categories'][category]['migrated'] += 1
                    status = "🔍 Analysé" if dry_run else "✅ Migré"
                    print(f"{status}: {file_path.relative_to(self.workspace_root)} ({analysis['migration_type']})")
                else:
                    self.stats['errors'] += 1
                    self.stats['categories'][category]['errors'] += 1
                    print(f"❌ Erreur: {file_path.relative_to(self.workspace_root)}")
            else:
                self.stats['skipped'] += 1
                if analysis['migration_type'] == 'already_using_manager':
                    print(f"⏭️ Déjà migré: {file_path.relative_to(self.workspace_root)}")
                else:
                    print(f"⏭️ Pas de logging: {file_path.relative_to(self.workspace_root)}")
        
        return self.stats
    
    def generate_report(self) -> str:
        """Génère un rapport détaillé de la migration"""
        report = []
        report.append("📊 RAPPORT DE MIGRATION NEXTGENERATION LOGGING")
        report.append("=" * 70)
        report.append(f"📁 Total fichiers scannés: {self.stats['total_files']}")
        report.append(f"✅ Fichiers migrés: {self.stats['migrated']}")
        report.append(f"❌ Erreurs: {self.stats['errors']}")
        report.append(f"⏭️ Ignorés: {self.stats['skipped']}")
        
        if self.stats['migrated'] + self.stats['errors'] > 0:
            success_rate = (self.stats['migrated'] / (self.stats['migrated'] + self.stats['errors'])) * 100
            report.append(f"🎯 TAUX DE RÉUSSITE: {success_rate:.1f}%")
        
        report.append("\n📂 DÉTAIL PAR CATÉGORIE:")
        for category, data in sorted(self.stats['categories'].items()):
            report.append(f"  {category:15} - Total: {data['total']:3d} | Migrés: {data['migrated']:3d} | Erreurs: {data['errors']:3d}")
        
        return '\n'.join(report)
    
    def save_migration_log(self, log_file: str = None):
        """Sauvegarde le log de migration"""
        if log_file is None:
            log_file = f"migration_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        import json
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                'migration_stats': self.stats,
                'migration_log': self.migration_log,
                'timestamp': datetime.now().isoformat(),
                'workspace_root': str(self.workspace_root),
                'production_ready_path': str(self.production_ready_path)
            }, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Log de migration sauvegardé: {log_file}")

def main():
    parser = argparse.ArgumentParser(description='Migration automatique vers logging centralisé NextGeneration')
    parser.add_argument('--workspace', '-w', default=r"C:\Dev\nextgeneration", 
                       help='Chemin vers le workspace NextGeneration')
    parser.add_argument('--production-ready', '-p', 
                       default=r"C:\Dev\nextgeneration\20250620_projet_logging_centralise\PRODUCTION_READY",
                       help='Chemin vers PRODUCTION_READY')
    parser.add_argument('--category', '-c', choices=['agents', 'tools', 'scripts', 'orchestrator', 'tests', 'docs', 'memory_api', 'monitoring', 'autres'],
                       help='Migrer seulement une catégorie spécifique')
    parser.add_argument('--dry-run', '-d', action='store_true',
                       help='Mode dry run - analyser sans modifier')
    parser.add_argument('--log-file', '-l', help='Fichier de log personnalisé')
    
    args = parser.parse_args()
    
    # Configuration
    workspace_root = args.workspace
    production_ready_path = args.production_ready
    
    # Vérifications
    if not Path(workspace_root).exists():
        print(f"❌ Workspace non trouvé: {workspace_root}")
        return 1
    
    if not Path(production_ready_path).exists():
        print(f"❌ PRODUCTION_READY non trouvé: {production_ready_path}")
        return 1
    
    # Lancement de la migration
    migrator = NextGenMigrationTool(workspace_root, production_ready_path)
    stats = migrator.run_migration(args.category, args.dry_run)
    
    # Rapport final
    print("\n" + "=" * 70)
    print(migrator.generate_report())
    
    # Sauvegarde du log
    migrator.save_migration_log(args.log_file)
    
    # Conseils post-migration
    if not args.dry_run and stats['migrated'] > 0:
        print("\n🎯 PROCHAINES ÉTAPES:")
        print("1. Tester quelques scripts migrés")
        print("2. Exécuter: python tests/test_production_ready.py")
        print("3. En cas de problème, restaurer depuis les fichiers .backup_migration_*")
    
    return 0

if __name__ == "__main__":
    exit(main()) 