#!/usr/bin/env python3
"""
Script de vérification de la syntaxe de tous les agents de maintenance.
Utilise ce script pour identifier et corriger rapidement les erreurs de syntaxe.
"""

import os
import sys
import ast
import re
from pathlib import Path

def check_syntax(file_path):
    """Vérifie la syntaxe d'un fichier Python."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérification des patterns problématiques
        problems = []
        
        # Vérifier le double async
        if 'async async def' in content:
            problems.append("Double 'async' détecté")
        
        # Vérifier les imports manquants communs
        if 'from core.agent_factory_architecture import' not in content:
            if 'class Agent' not in content and 'Agent' in content:
                problems.append("Import de Agent potentiellement manquant")
        
        # Tentative de compilation
        try:
            ast.parse(content)
            syntax_ok = True
        except SyntaxError as e:
            syntax_ok = False
            problems.append(f"SyntaxError ligne {e.lineno}: {e.msg}")
        
        return syntax_ok, problems, content
    
    except Exception as e:
        return False, [f"Erreur de lecture: {e}"], ""

def fix_common_issues(content):
    """Corrige les problèmes de syntaxe communs."""
    # Correction du double async
    content = re.sub(r'async\s+async\s+def', 'async def', content)
    
    # Autres corrections peuvent être ajoutées ici
    
    return content

def main():
    print("🔍 Vérification de la syntaxe des agents de maintenance...")
    print("=" * 60)
    
    # Répertoire des agents
    agents_dir = Path("agent_factory_implementation/agents")
    
    if not agents_dir.exists():
        print(f"❌ Répertoire non trouvé : {agents_dir}")
        return 1
    
    # Recherche des fichiers d'agents
    agent_files = list(agents_dir.glob("agent_MAINTENANCE_*.py"))
    
    if not agent_files:
        print(f"❌ Aucun fichier d'agent trouvé dans {agents_dir}")
        return 1
    
    print(f"📁 Trouvé {len(agent_files)} fichier(s) d'agent(s)")
    print()
    
    all_ok = True
    fixed_files = []
    
    for file_path in sorted(agent_files):
        print(f"🔎 Vérification : {file_path.name}")
        
        syntax_ok, problems, content = check_syntax(file_path)
        
        if syntax_ok and not problems:
            print(f"  ✅ OK")
        else:
            all_ok = False
            print(f"  ❌ Problème(s) détecté(s) :")
            for problem in problems:
                print(f"     - {problem}")
            
            # Tentative de correction automatique
            if 'async async def' in content or any('Double' in p for p in problems):
                print(f"  🔧 Tentative de correction automatique...")
                
                fixed_content = fix_common_issues(content)
                
                # Vérifier si la correction a fonctionné
                try:
                    ast.parse(fixed_content)
                    print(f"  ✅ Correction réussie")
                    
                    # Sauvegarder la correction
                    backup_path = file_path.with_suffix('.py.backup')
                    file_path.rename(backup_path)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    fixed_files.append(file_path.name)
                    print(f"  💾 Fichier corrigé, backup : {backup_path.name}")
                    
                except SyntaxError:
                    print(f"  ❌ Correction automatique échouée")
        
        print()
    
    # Résumé
    print("=" * 60)
    if all_ok:
        print("🎉 Tous les fichiers sont syntaxiquement corrects !")
    else:
        print("⚠️  Des problèmes ont été détectés.")
        if fixed_files:
            print(f"🔧 Fichiers automatiquement corrigés : {', '.join(fixed_files)}")
            print("💡 Relancez ce script pour vérifier les corrections.")
    
    # Test d'import rapide
    print("\n🧪 Test d'import rapide...")
    try:
        sys.path.insert(0, str(agents_dir))
        
        # Tenter d'importer le chef d'équipe
        from agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_MAINTENANCE_00_chef_equipe_coordinateur
        print("✅ Import du chef d'équipe réussi")
        
        return 0 if all_ok else 1
        
    except ImportError as e:
        print(f"❌ Erreur d'import : {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
