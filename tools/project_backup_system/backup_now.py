#!/usr/bin/env python3
"""
Script backup immdiat NextGeneration
"""

import sys
from pathlib import Path
from datetime import datetime

# Ajout du chemin agents
sys.path.append('agents')
from agent_backup_engine import BackupEngineAgent

def main():
    print("[ROCKET] BACKUP IMMDIAT NEXTGENERATION")
    print("=" * 50)
    
    # Configuration backup
    source_path = Path('C:/Dev/nextgeneration')
    project_name = 'nextgeneration'
    base_backup_dir = Path('E:/DEV_BACKUP')
    
    # Cration du rpertoire projet
    project_backup_dir = base_backup_dir / project_name
    project_backup_dir.mkdir(parents=True, exist_ok=True)
    
    backup_name = f'backup_{project_name}_{datetime.now().strftime("%Y%m%d_%H%M")}.zip'
    destination_path = project_backup_dir / backup_name
    
    print(f'[FOLDER] Source: {source_path}')
    print(f' Destination: {destination_path}')
    print()
    
    # Vrification source existe
    if not source_path.exists():
        print(f'[CROSS] Erreur: Source inexistante {source_path}')
        return False
    
    # Cration rpertoire destination si ncessaire
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Cration agent backup
    agent = BackupEngineAgent()
    
    # Exclusions par dfaut pour projet dveloppement
    exclusions = [
        '.git',
        '__pycache__',
        'node_modules',
        '*.tmp',
        '*.log',
        '.env',
        'chroma_db',
        'logs'
    ]
    
    print(f'[CLIPBOARD] Exclusions: {", ".join(exclusions)}')
    print()
    
    # Excution backup
    print(" Compression en cours...")
    result = agent.create_optimized_backup(
        source_path,
        destination_path,
        exclusions=exclusions,
        project_name='nextgeneration'
    )
    
    print()
    print("[CHART] RSULTATS BACKUP")
    print("=" * 30)
    
    if result.success:
        print(f'[CHECK] Statut: SUCCS')
        print(f'[CHART] Fichiers sauvegards: {result.files_count}')
        print(f' Taux compression: {result.compression_ratio:.1f}%')
        print(f' Dure: {result.duration:.2f} secondes')
        print(f' Intgrit vrifie: {"[CHECK]" if result.integrity_verified else "[CROSS]"}')
        print(f'[FOLDER] Archive cre: {destination_path}')
        print(f' Taille archive: {destination_path.stat().st_size / (1024*1024):.1f} MB')
        print()
        print(" BACKUP NEXTGENERATION TERMIN AVEC SUCCS!")
        return True
    else:
        print(f'[CROSS] Statut: CHEC')
        print(f' Erreur: {result.error_message}')
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 