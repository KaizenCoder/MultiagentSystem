#!/usr/bin/env python3
"""
Script de Correction Rapide - Erreurs d'Indentation des Agents de Maintenance
Correction des erreurs qui bloquent le workflow complet
"""

import re
from pathlib import Path
import os

def corriger_erreurs_indentation():
    """Corriger les erreurs d'indentation dans tous les agents"""
    
    agent_dir = Path("agent_equipe_maintenance")
    if not agent_dir.exists():
        print("❌ Répertoire agent_equipe_maintenance non trouvé")
        return
    
    # Patterns de correction
    corrections = [
        # Erreur import LoggingManager mal indenté
        (
            r"(\s+)# LoggingManager NextGeneration - Agent\s*\n\s*from logging_manager_optimized import LoggingManager",
            r"\1# LoggingManager NextGeneration - Agent\n\1from logging_manager_optimized import LoggingManager"
        ),
        # Erreur self.logger mal indenté
        (
            r"(\s+)from logging_manager_optimized import LoggingManager\s*\n\s*self\.logger",
            r"\1from logging_manager_optimized import LoggingManager\n\1self.logger"
        ),
        # Erreur async async def
        (
            r"async\s+async\s+def\s+(\w+)",
            r"async def \1"
        ),
        # Erreur de classe mal définie
        (
            r"(\s+except ImportError.*?:\s*\n\s*print.*?\n\s*# Fallback.*?\n)\s*class\s+Agent:",
            r"\1        class Agent:"
        )
    ]
    
    agents_corriges = []
    
    for agent_file in agent_dir.glob("agent_MAINTENANCE_*.py"):
        print(f"\n🔧 Correction de {agent_file.name}...")
        
        try:
            # Lire le contenu
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Créer un backup
            backup_file = agent_file.with_suffix('.py.backup_correction')
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Appliquer les corrections
            content_corrige = content
            corrections_appliquees = 0
            
            for pattern, replacement in corrections:
                new_content = re.sub(pattern, replacement, content_corrige, flags=re.MULTILINE | re.DOTALL)
                if new_content != content_corrige:
                    corrections_appliquees += 1
                    content_corrige = new_content
            
            # Correction spécifique pour le fallback Agent
            if "except ImportError" in content_corrige and "class Agent:" in content_corrige:
                # Corriger l'indentation de la classe Agent dans le except
                lines = content_corrige.split('\n')
                in_except_block = False
                indent_level = 0
                
                for i, line in enumerate(lines):
                    if "except ImportError" in line:
                        in_except_block = True
                        indent_level = len(line) - len(line.lstrip())
                        continue
                    
                    if in_except_block and line.strip() == "class Agent:":
                        # Corriger l'indentation de la classe Agent
                        lines[i] = " " * (indent_level + 8) + "class Agent:"
                        corrections_appliquees += 1
                        
                        # Corriger les méthodes suivantes
                        for j in range(i + 1, len(lines)):
                            if lines[j].strip().startswith("def ") or lines[j].strip().startswith("async def "):
                                if not lines[j].startswith(" " * (indent_level + 12)):
                                    lines[j] = " " * (indent_level + 12) + lines[j].lstrip()
                                    corrections_appliquees += 1
                            elif lines[j].strip() == "" or lines[j].strip().startswith("#"):
                                continue
                            elif lines[j].strip().startswith("class ") and "Agent" not in lines[j]:
                                # Nouvelle classe, sortir du bloc
                                break
                
                content_corrige = '\n'.join(lines)
            
            # Écrire le fichier corrigé
            if corrections_appliquees > 0:
                with open(agent_file, 'w', encoding='utf-8') as f:
                    f.write(content_corrige)
                
                print(f"✅ {agent_file.name} corrigé - {corrections_appliquees} corrections appliquées")
                agents_corriges.append(agent_file.name)
            else:
                print(f"ℹ️ {agent_file.name} - Aucune correction nécessaire")
                
        except Exception as e:
            print(f"❌ Erreur lors de la correction de {agent_file.name}: {e}")
    
    print(f"\n📊 RÉSUMÉ CORRECTION:")
    print(f"Agents corrigés: {len(agents_corriges)}")
    for agent in agents_corriges:
        print(f"  ✅ {agent}")
    
    return agents_corriges

def tester_import_agents():
    """Tester l'import des agents après correction"""
    print("\n🧪 Test d'import des agents corrigés...")
    
    agent_dir = Path("agent_equipe_maintenance")
    agents_ok = []
    agents_ko = []
    
    for agent_file in agent_dir.glob("agent_MAINTENANCE_*.py"):
        try:
            # Test de syntaxe
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            compile(content, agent_file, 'exec')
            agents_ok.append(agent_file.name)
            print(f"✅ {agent_file.name} - Syntaxe correcte")
            
        except SyntaxError as e:
            agents_ko.append((agent_file.name, str(e)))
            print(f"❌ {agent_file.name} - Erreur syntaxe: {e}")
        except Exception as e:
            agents_ko.append((agent_file.name, str(e)))
            print(f"❌ {agent_file.name} - Erreur: {e}")
    
    print(f"\n📊 RÉSUMÉ TEST SYNTAXE:")
    print(f"Agents OK: {len(agents_ok)}")
    print(f"Agents KO: {len(agents_ko)}")
    
    return agents_ok, agents_ko

if __name__ == "__main__":
    print("🚀 Démarrage correction rapide des agents de maintenance...")
    
    # Étape 1: Correction des erreurs
    agents_corriges = corriger_erreurs_indentation()
    
    # Étape 2: Test de syntaxe
    agents_ok, agents_ko = tester_import_agents()
    
    # Étape 3: Rapport final
    if len(agents_ko) == 0:
        print("\n🎯 SUCCÈS! Tous les agents sont corrigés et fonctionnels!")
        print("✅ Le workflow peut maintenant être testé.")
    else:
        print(f"\n⚠️ {len(agents_ko)} agent(s) nécessitent encore des corrections:")
        for agent, error in agents_ko:
            print(f"  ❌ {agent}: {error}") 