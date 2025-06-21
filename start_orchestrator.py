#!/usr/bin/env python3
"""
Script de dmarrage simple pour l'orchestrateur (mode dveloppement)
Alternative au Docker Compose pour tests rapides
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

# Configuration
ORCHESTRATOR_PORT = 8003
ORCHESTRATOR_DIR = Path(__file__).parent / "orchestrator"

def check_dependencies():
    """Vrifier que les dpendances sont installes"""
    try:
        import fastapi
        import uvicorn
        import langchain
        print("[CHECK] Dpendances FastAPI installes")
        return True
    except ImportError as e:
        print(f"[CROSS] Dpendances manquantes: {e}")
        return False

def start_orchestrator():
    """Dmarrer l'orchestrateur en mode dveloppement"""
    print("[ROCKET] Dmarrage de l'orchestrateur...")
    print(f" Port: {ORCHESTRATOR_PORT}")
    print(f"[FOLDER] Rpertoire: {ORCHESTRATOR_DIR}")
    print("  Utilisez Ctrl+C pour arrter")
    print("-" * 50)
    
    try:
        # Changer vers le rpertoire orchestrator
        os.chdir(ORCHESTRATOR_DIR)
        
        # Configurer PYTHONPATH pour inclure le rpertoire parent
        env = os.environ.copy()
        project_root = str(Path(__file__).parent)
        env['PYTHONPATH'] = project_root + os.pathsep + env.get('PYTHONPATH', '')
        
        # Dmarrer uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", str(ORCHESTRATOR_PORT),
            "--reload",
            "--log-level", "info"
        ]        
        process = subprocess.Popen(cmd, env=env)
        
        # Attendre et grer l'arrt
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n  Arrt de l'orchestrateur...")
            process.terminate()
            process.wait()
            print("[CHECK] Orchestrateur arrt")
            
    except Exception as e:
        print(f"[CROSS] Erreur lors du dmarrage: {e}")
        return False
    
    return True

def main():
    """Fonction principale"""
    print("  DMARRAGE ORCHESTRATEUR - MODE DVELOPPEMENT")
    print("=" * 60)
    
    # Vrifier les dpendances
    if not check_dependencies():
        print("\n[BULB] Installez les dpendances avec:")
        print("   cd orchestrator && pip install -r requirements.txt")
        return False
    
    # Vrifier le fichier .env
    env_file = Path(".env")
    if not env_file.exists():
        print("[CROSS] Fichier .env manquant")
        print("[BULB] Copiez env.example vers .env et configurez vos cls API")
        return False
    
    print("[CHECK] Configuration trouve")
    
    # Dmarrer l'orchestrateur
    return start_orchestrator()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n  Arrt demand par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n[CROSS] Erreur inattendue: {e}")
        sys.exit(1)




