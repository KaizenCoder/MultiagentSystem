#!/usr/bin/env python3
"""
🔧 CORRECTEUR AUTOMATIQUE - PYTHONPATH pour tous les agents
Mission: Corriger le PYTHONPATH dans tous les agents de C:\Dev\agents
"""

import os
import sys
from pathlib import Path
import re

def fix_pythonpath_in_agent(agent_file):
    """Corriger le PYTHONPATH dans un fichier agent"""
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern à rechercher
        old_pattern = r'sys\.path\.insert\(0, str\(Path\(__file__\)\.parent\)\)'
        
        # Nouveau pattern avec le bon chemin
        new_pattern = '''sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, r"C:\\Dev\\nextgeneration")  # CORRECTION PYTHONPATH'''
        
        # Remplacer si le pattern existe
        if re.search(old_pattern, content):
            # Vérifier si la correction n'est pas déjà présente
            if "C:\\Dev\\nextgeneration" not in content:
                content = re.sub(old_pattern, new_pattern, content)
                
                # Sauvegarder
                with open(agent_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True, "Corrigé"
            else:
                return False, "Déjà corrigé"
        else:
            return False, "Pattern non trouvé"
            
    except Exception as e:
        return False, f"Erreur: {e}"

def main():
    """Fonction principale"""
    print("🔧 CORRECTEUR AUTOMATIQUE - PYTHONPATH AGENTS")
    print("=" * 60)
    
    agents_dir = Path("C:/Dev/agents")
    
    if not agents_dir.exists():
        print(f"❌ Répertoire non trouvé: {agents_dir}")
        return
    
    # Trouver tous les fichiers .py
    agent_files = list(agents_dir.glob("*.py"))
    
    print(f"📂 Répertoire: {agents_dir}")
    print(f"🔍 Agents trouvés: {len(agent_files)}")
    print()
    
    corrected = 0
    already_fixed = 0
    errors = 0
    
    for agent_file in agent_files:
        if agent_file.name.startswith("agent_"):
            success, message = fix_pythonpath_in_agent(agent_file)
            
            if success:
                print(f"✅ {agent_file.name}: {message}")
                corrected += 1
            elif "Déjà corrigé" in message:
                print(f"🔄 {agent_file.name}: {message}")
                already_fixed += 1
            else:
                print(f"❌ {agent_file.name}: {message}")
                errors += 1
    
    print()
    print("📊 RÉSUMÉ:")
    print(f"✅ Agents corrigés: {corrected}")
    print(f"🔄 Déjà corrigés: {already_fixed}")
    print(f"❌ Erreurs: {errors}")
    print(f"📈 Total traités: {corrected + already_fixed + errors}")
    
    if corrected > 0:
        print()
        print("🎉 CORRECTION TERMINÉE!")
        print("Tous les agents peuvent maintenant importer agent_factory_architecture!")

if __name__ == "__main__":
    main() 



