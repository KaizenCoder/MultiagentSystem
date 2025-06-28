#!/usr/bin/env python3
"""
Script de correction automatique SQLAlchemy
Fichier cible: C:\Dev\nextgeneration\docs\agents_postgresql_resolution\agent_sqlalchemy_fixer.py
Gnr par: Agent SQLAlchemy Fixer
Date: 2025-06-18T01:34:02.554998
"""

import shutil
from pathlib import Path

def appliquer_corrections():
    """Applique les corrections SQLAlchemy au fichier"""
    
    fichier_original = Path(r"C:\Dev\nextgeneration\docs\agents_postgresql_resolution\agent_sqlalchemy_fixer.py")
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
    

    # Correction ligne 465: Renommage pour viter conflit avec SQLAlchemy metadata
    contenu_corrige = contenu_corrige.replace(
        r"""**Problme :** `metadata = Column(...)` entre en conflit avec SQLAlchemy""",
        r"""**Problme :** `session_metadata = Column(...)` entre en conflit avec SQLAlchemy"""
    )
    corrections_appliquees += 1

    # Correction ligne 470: Renommage pour viter conflit avec SQLAlchemy metadata
    contenu_corrige = contenu_corrige.replace(
        r"""metadata = Column(JSON)""",
        r"""    session_metadata = Column(JSON)"""
    )
    corrections_appliquees += 1

    # Correction ligne 474: Renommage pour viter conflit avec SQLAlchemy metadata
    contenu_corrige = contenu_corrige.replace(
        r"""session_metadata = Column(JSON)""",
        r"""    session_session_metadata = Column(JSON)"""
    )
    corrections_appliquees += 1

    # Correction ligne 482: Ajout text() pour SQLAlchemy 2.x compatibility
    contenu_corrige = contenu_corrige.replace(
        r"""result = conn.execute("SELECT 1 as test_value")""",
        r"""result = conn.execute(text("SELECT 1 as test_value"))"""
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
            "timestamp": "2025-06-18T01:34:02.554998",
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
    fichier_original = Path(r"C:\Dev\nextgeneration\docs\agents_postgresql_resolution\agent_sqlalchemy_fixer.py")
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




