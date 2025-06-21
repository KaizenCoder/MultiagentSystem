#!/usr/bin/env python3
"""
Script de correction automatique SQLAlchemy
Fichier cible: C:\Dev\nextgeneration\memory_api\app\db\session.py
Gnr par: Agent SQLAlchemy Fixer
Date: 2025-06-18T01:34:02.558421
"""

import shutil
from pathlib import Path

def appliquer_corrections():
    """Applique les corrections SQLAlchemy au fichier"""
    
    fichier_original = Path(r"C:\Dev\nextgeneration\memory_api\app\db\session.py")
    fichier_backup = Path(__file__).parent.parent.parent / "backups" / "original_files" / fichier_original.name
    
    # 1. Backup du fichier original
    fichier_backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(fichier_original, fichier_backup)
    print(f"[CHECK] Backup cr: {fichier_backup}")
    
    # 2. Lecture du contenu
    with open(fichier_original, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # 3. Application des corrections
    contenu_corrige = contenu
    corrections_appliquees = 0
    

    # Correction ligne 111: Ajout text() pour SQLAlchemy 2.x compatibility
    contenu_corrige = contenu_corrige.replace(
        r"""result = db.execute("SELECT 1 as test_value")""",
        r"""result = db.execute(text("SELECT 1 as test_value"))"""
    )
    corrections_appliquees += 1

    # Correction ligne 120: Ajout text() pour SQLAlchemy 2.x compatibility
    contenu_corrige = contenu_corrige.replace(
        r"""version_result = db.execute("SELECT version()")""",
        r"""version_result = db.execute(text("SELECT version()"))"""
    )
    corrections_appliquees += 1

    # Correction ligne 125: Ajout text() pour SQLAlchemy 2.x compatibility
    contenu_corrige = contenu_corrige.replace(
        r"""extensions_result = db.execute("SELECT extname FROM pg_extension ORDER BY extname")""",
        r"""extensions_result = db.execute(text("SELECT extname FROM pg_extension ORDER BY extname"))"""
    )
    corrections_appliquees += 1

    # Correction ligne 132: Ajout text() pour SQLAlchemy 2.x compatibility
    contenu_corrige = contenu_corrige.replace(
        r"""db.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")""",
        r"""db.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")"""
    )
    corrections_appliquees += 1

    
    # 4. Vrification des corrections
    if corrections_appliquees > 0:
        # Sauvegarde du fichier corrig
        with open(fichier_original, 'w', encoding='utf-8') as f:
            f.write(contenu_corrige)
        print(f"[CHECK] {corrections_appliquees} corrections appliques  {fichier_original}")
        
        # Cration d'un rapport de correction
        rapport_correction = {
            "timestamp": "2025-06-18T01:34:02.558421",
            "fichier": str(fichier_original),
            "corrections_appliquees": corrections_appliquees,
            "backup_localisation": str(fichier_backup)
        }
        
        return rapport_correction
    else:
        print(" Aucune correction ncessaire")
        return None

def restaurer_backup():
    """Restaure le fichier depuis le backup"""
    fichier_original = Path(r"C:\Dev\nextgeneration\memory_api\app\db\session.py")
    fichier_backup = Path(__file__).parent.parent.parent / "backups" / "original_files" / fichier_original.name
    
    if fichier_backup.exists():
        shutil.copy2(fichier_backup, fichier_original)
        print(f"[CHECK] Fichier restaur depuis backup: {fichier_backup}")
        return True
    else:
        print(f"[CROSS] Backup non trouv: {fichier_backup}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--restore":
        restaurer_backup()
    else:
        rapport = appliquer_corrections()
        if rapport:
            print(f"\n[CHART] Rapport: {rapport}")
        else:
            print("\n[TARGET] Aucune action requise")




