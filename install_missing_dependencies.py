#!/usr/bin/env python3
"""
Script d'installation automatique des dépendances manquantes.
Installe toutes les dépendances nécessaires pour les agents.
"""
import subprocess
import sys

def install_package(package):
    """Installe un package Python via pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installé avec succès")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Échec installation {package}")
        return False

def main():
    """Installe toutes les dépendances manquantes."""
    print("📦 INSTALLATION DÉPENDANCES MANQUANTES")
    print("=" * 50)
    
    # Liste des dépendances requises
    required_packages = [
        "python-dotenv",
        "hvac", 
        "aiofiles",
        "pyflakes",
        "pytest",
        "docker",
        "requests",
        "beautifulsoup4",
        "pydantic",
        "rich",
        "asyncio-mqtt"
    ]
    
    success_count = 0
    for package in required_packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 RÉSULTATS:")
    print(f"✅ Installés: {success_count}/{len(required_packages)}")
    
    if success_count == len(required_packages):
        print("🎉 Toutes les dépendances sont installées!")
    else:
        print("⚠️ Certaines dépendances ont échoué")

if __name__ == "__main__":
    main()