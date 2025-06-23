#!/usr/bin/env python3
"""
Script de correction prcis pour models.py
Correction manuelle et cible des problmes SQLAlchemy identifis
"""

import re
import os
from datetime import datetime

def main():
    """Correction prcise des modles SQLAlchemy"""
    models_file = "C:\\Dev\\nextgeneration\\memory_api\\app\\db\\models.py"
    
    print(f"[TOOL] Lecture du fichier: {models_file}")
    
    # Lire le contenu
    with open(models_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"[DOCUMENT] Taille originale: {len(content)} caractres")
    
    # Corrections cibles
    corrections = 0
    
    # 1. Corriger le conflit d'attribut metadata
    if 'metadata = Column(' in content:
        content = content.replace('metadata = Column(', 'session_metadata = Column(')
        corrections += 1
        print("[CHECK] Correction 1: Attribut metadata renomm en session_metadata")
    
    # 2. Ajouter text() pour les fonctions SQL brutes
    if 'text("' not in content and 'from sqlalchemy' in content:
        # Ajouter text  l'import
        content = content.replace(
            'from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Boolean, Index, Float',
            'from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Boolean, Index, Float, text'
        )
        corrections += 1
        print("[CHECK] Correction 2: Import de text() ajout")
    
    # 3. Vrifier et corriger la syntaxe de base
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # viter les doublons de session_ rpts
        if 'session_    session_' in line:
            # Corriger la ligne
            line = re.sub(r'session_\s+session_\s+session_\s+session_\s+session_', '', line)
            if 'metadata' in line:
                line = '    session_metadata = Column(JSONB)'
            corrections += 1
            print(f"[CHECK] Correction 3: Ligne corrige - {line.strip()}")
        
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Crer backup avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\backups\\original_files\\models_backup_{timestamp}.py"
    
    print(f" Cration backup: {backup_file}")
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # crire le fichier corrig
    print(f"[TOOL] Application des corrections: {models_file}")
    with open(models_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[CHECK] {corrections} corrections appliques avec succs")
    print(f"[CHART] Nouvelle taille: {len(content)} caractres")
    
    # Crer rapport
    rapport = {
        'timestamp': datetime.now().isoformat(),
        'fichier': models_file,
        'corrections_appliquees': corrections,
        'backup_localisation': backup_file,
        'taille_avant': len(content),
        'taille_apres': len(content)
    }
    
    print(f"[CHART] Rapport: {rapport}")

if __name__ == "__main__":
    main()




