#!/usr/bin/env python3
"""
Script de correction spécifique pour logging_manager_optimized.py
Corrige uniquement l'import en début de fichier
"""

import re

def fix_logging_manager():
    """Corrige spécifiquement le fichier logging_manager_optimized.py"""
    
    file_path = "logging_manager_optimized.py"
    
    try:
        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier s'il contient déjà l'import NextGeneration
        if "import sys
from pathlib import Path
from core import logging_manager" in content:
            print("✅ Fichier déjà migré correctement")
            return True
            
        # Rechercher la première ligne d'import
        lines = content.split('\n')
        
        # Trouver où insérer l'import NextGeneration
        insert_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                insert_index = i
                break
        
        if insert_index == -1:
            # Insérer après le docstring
            for i, line in enumerate(lines):
                if line.strip().endswith('"""') and i > 0:
                    insert_index = i + 1
                    break
        
        if insert_index == -1:
            insert_index = 0
        
        # Insérer l'import NextGeneration
        logging_import = """# LoggingManager NextGeneration - Core System
try:
    import sys
from pathlib import Path
from core import logging_manager
    # Configuration automatique pour le core system
    _core_logger = logging_manager.get_logger(custom_config={
        "logger_name": "LoggingManagerCore",
        "log_level": "INFO",
        "elasticsearch_enabled": True,
        "encryption_enabled": True,
        "async_enabled": True,
        "audit_enabled": True,
        "high_throughput": True
    })
except ImportError:
    # Fallback si pas encore initialisé
    import logging
    _core_logger = logging.getLogger("LoggingManagerCore")
"""
        
        lines.insert(insert_index, logging_import)
        
        # Réécrire le fichier
        new_content = '\n'.join(lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ {file_path} corrigé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction de {file_path}: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Correction spécifique du logging_manager_optimized.py...")
    success = fix_logging_manager()
    if success:
        print("🎉 Correction terminée avec succès !")
    else:
        print("💥 Échec de la correction") 



