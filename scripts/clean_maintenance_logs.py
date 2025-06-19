#!/usr/bin/env python3
"""
🧹 NETTOYAGE LOGS MAINTENANCE
Script utilitaire pour nettoyer les logs de maintenance anciens

Usage:
    python scripts/clean_maintenance_logs.py --days 30    # Nettoyer logs > 30 jours
    python scripts/clean_maintenance_logs.py --archive    # Archiver au lieu de supprimer
    python scripts/clean_maintenance_logs.py --dry-run    # Simulation sans suppression
"""

import argparse
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import json

def clean_maintenance_logs(days_old: int = 30, archive: bool = False, dry_run: bool = False):
    """Nettoie les logs de maintenance anciens"""
    
    logs_root = Path("logs/maintenance")
    if not logs_root.exists():
        print("❌ Répertoire logs/maintenance non trouvé")
        return
    
    cutoff_date = datetime.now() - timedelta(days=days_old)
    archive_dir = Path("logs/archive") if archive else None
    
    if archive and not dry_run:
        archive_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🧹 NETTOYAGE LOGS MAINTENANCE")
    print(f"📅 Suppression logs antérieurs au: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Mode: {'Archive' if archive else 'Suppression'}")
    print(f"🔍 Mode: {'Simulation' if dry_run else 'Réel'}")
    print("=" * 60)
    
    total_files = 0
    total_size = 0
    cleaned_files = 0
    cleaned_size = 0
    
    # Parcourir tous les fichiers dans logs/maintenance
    for file_path in logs_root.rglob("*.json"):
        if file_path.is_file():
            total_files += 1
            file_size = file_path.stat().st_size
            total_size += file_size
            
            # Vérifier âge du fichier
            file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            if file_mtime < cutoff_date:
                cleaned_files += 1
                cleaned_size += file_size
                
                relative_path = file_path.relative_to(logs_root.parent)
                print(f"🗑️  {relative_path} ({file_size:,} bytes, {file_mtime.strftime('%Y-%m-%d')})")
                
                if not dry_run:
                    if archive:
                        # Archiver le fichier
                        archive_path = archive_dir / file_path.relative_to(logs_root)
                        archive_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(file_path), str(archive_path))
                    else:
                        # Supprimer le fichier
                        file_path.unlink()
    
    # Nettoyer aussi les backups anciens
    backups_dir = Path("backups_docteur")
    if backups_dir.exists():
        for backup_file in backups_dir.glob("*.backup"):
            if backup_file.is_file():
                total_files += 1
                file_size = backup_file.stat().st_size
                total_size += file_size
                
                file_mtime = datetime.fromtimestamp(backup_file.stat().st_mtime)
                
                if file_mtime < cutoff_date:
                    cleaned_files += 1
                    cleaned_size += file_size
                    
                    print(f"🗑️  {backup_file} ({file_size:,} bytes, {file_mtime.strftime('%Y-%m-%d')})")
                    
                    if not dry_run:
                        if archive:
                            archive_path = archive_dir / backup_file.name
                            shutil.move(str(backup_file), str(archive_path))
                        else:
                            backup_file.unlink()
    
    # Résumé
    print("=" * 60)
    print(f"📊 RÉSUMÉ:")
    print(f"   Total fichiers analysés: {total_files}")
    print(f"   Taille totale: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
    print(f"   Fichiers {'à nettoyer' if dry_run else 'nettoyés'}: {cleaned_files}")
    print(f"   Espace {'libérable' if dry_run else 'libéré'}: {cleaned_size:,} bytes ({cleaned_size/1024/1024:.1f} MB)")
    
    if dry_run:
        print(f"💡 Exécutez sans --dry-run pour effectuer le nettoyage")
    elif archive:
        print(f"📁 Fichiers archivés dans: {archive_dir}")
    else:
        print(f"✅ Nettoyage terminé")

def show_logs_stats():
    """Affiche les statistiques des logs de maintenance"""
    logs_root = Path("logs/maintenance")
    if not logs_root.exists():
        print("❌ Répertoire logs/maintenance non trouvé")
        return
    
    print(f"📊 STATISTIQUES LOGS MAINTENANCE")
    print("=" * 50)
    
    total_files = 0
    total_size = 0
    stats_by_agent = {}
    
    for agent_dir in logs_root.iterdir():
        if agent_dir.is_dir():
            agent_files = 0
            agent_size = 0
            
            for file_path in agent_dir.glob("*.json"):
                if file_path.is_file():
                    agent_files += 1
                    file_size = file_path.stat().st_size
                    agent_size += file_size
                    total_files += 1
                    total_size += file_size
            
            if agent_files > 0:
                stats_by_agent[agent_dir.name] = {
                    "files": agent_files,
                    "size": agent_size
                }
    
    # Affichage par agent
    for agent_name, stats in sorted(stats_by_agent.items()):
        print(f"🎯 {agent_name.capitalize():<12}: {stats['files']:>3} fichiers, {stats['size']:>8,} bytes ({stats['size']/1024/1024:.1f} MB)")
    
    print("-" * 50)
    print(f"📈 TOTAL         : {total_files:>3} fichiers, {total_size:>8,} bytes ({total_size/1024/1024:.1f} MB)")
    
    # Recommandations
    if total_size > 50 * 1024 * 1024:  # > 50 MB
        print(f"⚠️  Taille importante détectée - Considérer nettoyage")
    
    if total_files > 100:
        print(f"⚠️  Nombreux fichiers détectés - Considérer archivage")

def main():
    parser = argparse.ArgumentParser(description="🧹 Nettoyage logs maintenance NextGeneration")
    parser.add_argument("--days", type=int, default=30, help="Âge en jours pour nettoyage (défaut: 30)")
    parser.add_argument("--archive", action="store_true", help="Archiver au lieu de supprimer")
    parser.add_argument("--dry-run", action="store_true", help="Simulation sans modification")
    parser.add_argument("--stats", action="store_true", help="Afficher statistiques seulement")
    
    args = parser.parse_args()
    
    if args.stats:
        show_logs_stats()
    else:
        clean_maintenance_logs(
            days_old=args.days,
            archive=args.archive,
            dry_run=args.dry_run
        )

if __name__ == "__main__":
    main() 