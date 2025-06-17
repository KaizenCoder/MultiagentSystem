#!/usr/bin/env python3
"""
Script de démarrage simple pour l'orchestrateur (mode développement)
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
    """Vérifier que les dépendances sont installées"""
    try:
        import fastapi
        import uvicorn
        import langchain
        print("✅ Dépendances FastAPI installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendances manquantes: {e}")
        return False

def start_orchestrator():
    """Démarrer l'orchestrateur en mode développement"""
    print("🚀 Démarrage de l'orchestrateur...")
    print(f"📍 Port: {ORCHESTRATOR_PORT}")
    print(f"📁 Répertoire: {ORCHESTRATOR_DIR}")
    print("⏹️  Utilisez Ctrl+C pour arrêter")
    print("-" * 50)
    
    try:
        # Changer vers le répertoire orchestrator
        os.chdir(ORCHESTRATOR_DIR)
        
        # Configurer PYTHONPATH pour inclure le répertoire parent
        env = os.environ.copy()
        project_root = str(Path(__file__).parent)
        env['PYTHONPATH'] = project_root + os.pathsep + env.get('PYTHONPATH', '')
        
        # Démarrer uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", str(ORCHESTRATOR_PORT),
            "--reload",
            "--log-level", "info"
        ]        
        process = subprocess.Popen(cmd, env=env)
        
        # Attendre et gérer l'arrêt
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n⏹️  Arrêt de l'orchestrateur...")
            process.terminate()
            process.wait()
            print("✅ Orchestrateur arrêté")
            
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return False
    
    return True

def main():
    """Fonction principale"""
    print("🎛️  DÉMARRAGE ORCHESTRATEUR - MODE DÉVELOPPEMENT")
    print("=" * 60)
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("\n💡 Installez les dépendances avec:")
        print("   cd orchestrator && pip install -r requirements.txt")
        return False
    
    # Vérifier le fichier .env
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Fichier .env manquant")
        print("💡 Copiez env.example vers .env et configurez vos clés API")
        return False
    
    print("✅ Configuration trouvée")
    
    # Démarrer l'orchestrateur
    return start_orchestrator()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Arrêt demandé par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)
