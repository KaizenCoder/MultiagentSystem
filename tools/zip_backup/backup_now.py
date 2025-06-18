#!/usr/bin/env python3
"""
Script backup immédiat NextGeneration
"""

import sys
from pathlib import Path
from datetime import datetime

# Ajout du chemin agents
sys.path.append('agents')
from agent_backup_engine import BackupEngineAgent

def main():
    print("🚀 BACKUP IMMÉDIAT NEXTGENERATION")
    print("=" * 50)
    
    # Configuration backup
    source_path = Path('C:/Dev/nextgeneration')
    project_name = 'nextgeneration'
    base_backup_dir = Path('E:/DEV_BACKUP')
    
    # Création du répertoire projet
    project_backup_dir = base_backup_dir / project_name
    project_backup_dir.mkdir(parents=True, exist_ok=True)
    
    backup_name = f'backup_{project_name}_{datetime.now().strftime("%Y%m%d_%H%M")}.zip'
    destination_path = project_backup_dir / backup_name
    
    print(f'📁 Source: {source_path}')
    print(f'🗜️ Destination: {destination_path}')
    print()
    
    # Vérification source existe
    if not source_path.exists():
        print(f'❌ Erreur: Source inexistante {source_path}')
        return False
    
    # Création répertoire destination si nécessaire
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Création agent backup
    agent = BackupEngineAgent()
    
    # Exclusions par défaut pour projet développement
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
    
    print(f'📋 Exclusions: {", ".join(exclusions)}')
    print()
    
    # Exécution backup
    print("🗜️ Compression en cours...")
    result = agent.create_optimized_backup(
        source_path,
        destination_path,
        exclusions=exclusions,
        project_name='nextgeneration'
    )
    
    print()
    print("📊 RÉSULTATS BACKUP")
    print("=" * 30)
    
    if result.success:
        print(f'✅ Statut: SUCCÈS')
        print(f'📊 Fichiers sauvegardés: {result.files_count}')
        print(f'🗜️ Taux compression: {result.compression_ratio:.1f}%')
        print(f'⏱️ Durée: {result.duration:.2f} secondes')
        print(f'🔒 Intégrité vérifiée: {"✅" if result.integrity_verified else "❌"}')
        print(f'📁 Archive créée: {destination_path}')
        print(f'💾 Taille archive: {destination_path.stat().st_size / (1024*1024):.1f} MB')
        print()
        print("🎉 BACKUP NEXTGENERATION TERMINÉ AVEC SUCCÈS!")
        return True
    else:
        print(f'❌ Statut: ÉCHEC')
        print(f'🚫 Erreur: {result.error_message}')
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 