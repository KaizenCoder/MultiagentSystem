#!/usr/bin/env python3
"""
Système de fallback pour dotenv
Fournit une alternative si python-dotenv n'est pas installé
"""

import os
from pathlib import Path

def load_dotenv(dotenv_path=None):
    """
    Charge les variables d'environnement depuis un fichier .env
    Fallback simple si python-dotenv n'est pas disponible
    """
    
    # Déterminer le chemin du fichier .env
    if dotenv_path is None:
        # Chercher .env dans le répertoire courant et les parents
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            env_file = parent / ".env"
            if env_file.exists():
                dotenv_path = env_file
                break
    
    if dotenv_path is None:
        return False  # Pas de fichier .env trouvé
    
    try:
        with open(dotenv_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Ignorer les commentaires et lignes vides
                if not line or line.startswith('#'):
                    continue
                
                # Parser KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Supprimer les guillemets si présents
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # Définir la variable d'environnement
                    os.environ[key] = value
        
        return True
        
    except Exception:
        return False

# Import conditionnel de dotenv
try:
    from dotenv import load_dotenv as _original_load_dotenv
    load_dotenv = _original_load_dotenv
except ImportError:
    # Utiliser notre fallback
    pass
