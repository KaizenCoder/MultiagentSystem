#!/usr/bin/env python3
"""
📁 SCRIPT DE CRÉATION DES RÉPERTOIRES
====================================

Script utilitaire pour créer automatiquement les répertoires nécessaires
au système de refactorisation et suivi des agents Pattern Factory.

Répertoires créés :
- agents/backups/ : Stockage des sauvegardes avant modification
- agents/logs/ : Journaux de développement pour chaque agent
"""

import os
from pathlib import Path

def create_directories():
    """Crée les répertoires nécessaires pour le système de refactorisation"""
    
    # Répertoires à créer
    directories = [
        "agents/backups",
        "agents/logs"
    ]
    
    created_dirs = []
    
    for directory in directories:
        dir_path = Path(directory)
        
        try:
            # Créer le répertoire avec tous les parents nécessaires
            dir_path.mkdir(parents=True, exist_ok=True)
            
            if dir_path.exists():
                created_dirs.append(str(dir_path))
                print(f"✅ Répertoire créé/vérifié : {dir_path}")
            else:
                print(f"❌ Échec création : {dir_path}")
                
        except Exception as e:
            print(f"❌ Erreur création {dir_path}: {e}")
    
    # Résumé
    print(f"\n📊 Résumé :")
    print(f"   - Répertoires créés/vérifiés : {len(created_dirs)}")
    for dir_name in created_dirs:
        print(f"     • {dir_name}")
    
    # Créer des fichiers .gitkeep pour préserver les répertoires vides
    for directory in directories:
        gitkeep_file = Path(directory) / ".gitkeep"
        try:
            gitkeep_file.touch(exist_ok=True)
            print(f"📝 Fichier .gitkeep créé : {gitkeep_file}")
        except Exception as e:
            print(f"⚠️ Impossible de créer .gitkeep dans {directory}: {e}")
    
    return created_dirs

if __name__ == "__main__":
    print("🚀 Création des répertoires pour le système de refactorisation...")
    print("=" * 60)
    
    created = create_directories()
    
    print("\n" + "=" * 60)
    print(f"✅ Script terminé. {len(created)} répertoires prêts.") 