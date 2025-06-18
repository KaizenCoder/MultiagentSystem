#!/usr/bin/env python3
"""
Script de correction automatique SQLAlchemy
Fichier cible: C:\Dev\nextgeneration\docs\agents_postgresql_resolution\agent_web_researcher.py
Généré par: Agent SQLAlchemy Fixer
Date: 2025-06-18T01:34:02.555999
"""

import shutil
from pathlib import Path

def appliquer_corrections():
    """Applique les corrections SQLAlchemy au fichier"""
    
    fichier_original = Path(r"C:\Dev\nextgeneration\docs\agents_postgresql_resolution\agent_web_researcher.py")
    fichier_backup = Path(__file__).parent.parent.parent / "backups" / "original_files" / fichier_original.name
    
    # 1. Backup du fichier original
    fichier_backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(fichier_original, fichier_backup)
    print(f"✅ Backup créé: {fichier_backup}")
    
    # 2. Lecture du contenu
    with open(fichier_original, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # 3. Application des corrections
    contenu_corrige = contenu
    corrections_appliquees = 0
    

    # Correction ligne 137: Renommage pour éviter conflit avec SQLAlchemy metadata
    contenu_corrige = contenu_corrige.replace(
        r"""metadata = Column(String)""",
        r"""    session_metadata = Column(String)"""
    )
    corrections_appliquees += 1

    # Correction ligne 143: Renommage pour éviter conflit avec SQLAlchemy metadata
    contenu_corrige = contenu_corrige.replace(
        r"""model_metadata = Column(String)""",
        r"""    model_session_metadata = Column(String)"""
    )
    corrections_appliquees += 1

    # Correction ligne 159: Ajout text() pour SQLAlchemy 2.x compatibility
    contenu_corrige = contenu_corrige.replace(
        r"""result = connection.execute("SELECT 1")""",
        r"""result = connection.execute(text("SELECT 1"))"""
    )
    corrections_appliquees += 1

    # Correction ligne 214: Ajout text() pour SQLAlchemy 2.x compatibility
    contenu_corrige = contenu_corrige.replace(
        r"""result = conn.execute("SELECT * FROM table")""",
        r"""result = conn.execute(text("SELECT * FROM table"))"""
    )
    corrections_appliquees += 1

    # Correction ligne 345: Renommage pour éviter conflit avec SQLAlchemy metadata
    contenu_corrige = contenu_corrige.replace(
        r"""metadata = Column(JSON)  # ❌ Conflit avec SQLAlchemy""",
        r"""    session_metadata = Column(JSON)  # ❌ Conflit avec SQLAlchemy"""
    )
    corrections_appliquees += 1

    # Correction ligne 349: Renommage pour éviter conflit avec SQLAlchemy metadata
    contenu_corrige = contenu_corrige.replace(
        r"""session_metadata = Column(JSON)  # ✅ OK""",
        r"""    session_session_metadata = Column(JSON)  # ✅ OK"""
    )
    corrections_appliquees += 1

    # Correction ligne 365: Ajout text() pour SQLAlchemy 2.x compatibility
    contenu_corrige = contenu_corrige.replace(
        r"""result = conn.execute("SELECT 1 as test_value")  # ❌""",
        r"""result = conn.execute(text("SELECT 1 as test_value"))  # ❌"""
    )
    corrections_appliquees += 1

    # Correction ligne 586: Ajout text() pour SQLAlchemy 2.x compatibility
    contenu_corrige = contenu_corrige.replace(
        r"""# Remplacer: conn.execute("SELECT 1")""",
        r"""# Remplacer: conn.execute(text("SELECT 1"))"""
    )
    corrections_appliquees += 1

    
    # 4. Vérification des corrections
    if corrections_appliquees > 0:
        # Sauvegarde du fichier corrigé
        with open(fichier_original, 'w', encoding='utf-8') as f:
            f.write(contenu_corrige)
        print(f"✅ {corrections_appliquees} corrections appliquées à {fichier_original}")
        
        # Création d'un rapport de correction
        rapport_correction = {
            "timestamp": "2025-06-18T01:34:02.555999",
            "fichier": str(fichier_original),
            "corrections_appliquees": corrections_appliquees,
            "backup_localisation": str(fichier_backup)
        }
        
        return rapport_correction
    else:
        print("ℹ️ Aucune correction nécessaire")
        return None

def restaurer_backup():
    """Restaure le fichier depuis le backup"""
    fichier_original = Path(r"C:\Dev\nextgeneration\docs\agents_postgresql_resolution\agent_web_researcher.py")
    fichier_backup = Path(__file__).parent.parent.parent / "backups" / "original_files" / fichier_original.name
    
    if fichier_backup.exists():
        shutil.copy2(fichier_backup, fichier_original)
        print(f"✅ Fichier restauré depuis backup: {fichier_backup}")
        return True
    else:
        print(f"❌ Backup non trouvé: {fichier_backup}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--restore":
        restaurer_backup()
    else:
        rapport = appliquer_corrections()
        if rapport:
            print(f"\n📊 Rapport: {rapport}")
        else:
            print("\n🎯 Aucune action requise")
