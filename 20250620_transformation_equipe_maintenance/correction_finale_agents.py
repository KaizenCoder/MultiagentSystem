#!/usr/bin/env python3
"""
Correcteur Final - Résolution complète des erreurs d'indentation
Utilise une approche ligne par ligne pour corriger précisément les erreurs
"""

from pathlib import Path
import re

def corriger_agent_ligne_par_ligne(agent_file):
    """Corriger un agent ligne par ligne avec précision"""
    
    print(f"\n🔧 Correction précise de {agent_file.name}...")
    
    with open(agent_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Créer backup
    backup_file = agent_file.with_suffix('.py.backup_final')
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    corrections = 0
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Détecter le bloc except ImportError
        if "except ImportError" in line:
            except_indent = len(line) - len(line.lstrip())
            print(f"  📍 Bloc except ImportError détecté à la ligne {i+1}, indent={except_indent}")
            
            # Chercher la classe Agent dans ce bloc
            j = i + 1
            while j < len(lines):
                if lines[j].strip() == "class Agent:":
                    # Corriger l'indentation de la classe Agent
                    correct_indent = except_indent + 8
                    if len(lines[j]) - len(lines[j].lstrip()) != correct_indent:
                        lines[j] = " " * correct_indent + "class Agent:\n"
                        corrections += 1
                        print(f"  ✅ Ligne {j+1}: Classe Agent corrigée")
                    
                    # Corriger les méthodes de la classe Agent
                    k = j + 1
                    while k < len(lines):
                        current_line = lines[k]
                        stripped = current_line.strip()
                        
                        if stripped.startswith("def ") or stripped.startswith("async def "):
                            # Méthode de classe Agent
                            method_indent = correct_indent + 4
                            if len(current_line) - len(current_line.lstrip()) != method_indent:
                                lines[k] = " " * method_indent + stripped + "\n"
                                corrections += 1
                                print(f"  ✅ Ligne {k+1}: Méthode '{stripped[:20]}...' corrigée")
                        
                        elif stripped.startswith("self.") or stripped.startswith("from ") or stripped.startswith("import "):
                            # Corps de méthode ou import
                            body_indent = correct_indent + 8
                            if len(current_line) - len(current_line.lstrip()) != body_indent and stripped != "":
                                lines[k] = " " * body_indent + stripped + "\n"
                                corrections += 1
                                print(f"  ✅ Ligne {k+1}: Corps '{stripped[:15]}...' corrigé")
                        
                        elif stripped.startswith("class ") and "Agent" not in stripped:
                            # Nouvelle classe, sortir du bloc Agent
                            break
                        elif stripped == "" or stripped.startswith("#"):
                            # Ligne vide ou commentaire, ne pas toucher
                            pass
                        elif not stripped.startswith(" ") and stripped != "":
                            # Début d'un nouveau bloc, sortir
                            break
                        
                        k += 1
                    break
                elif lines[j].strip().startswith("class ") and "Agent" not in lines[j]:
                    # Autre classe, sortir du bloc except
                    break
                elif "PATTERN_FACTORY_AVAILABLE = False" in lines[j]:
                    # Fin du bloc except
                    break
                
                j += 1
        
        # Corriger les erreurs async async def
        if "async async def" in line:
            lines[i] = line.replace("async async def", "async def")
            corrections += 1
            print(f"  ✅ Ligne {i+1}: 'async async def' corrigé")
        
        i += 1
    
    # Sauvegarder le fichier corrigé
    with open(agent_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"  📊 {corrections} corrections appliquées à {agent_file.name}")
    return corrections

def tester_syntaxe_agent(agent_file):
    """Tester la syntaxe d'un agent spécifique"""
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        compile(content, agent_file, 'exec')
        print(f"  ✅ {agent_file.name} - Syntaxe correcte")
        return True
    except SyntaxError as e:
        print(f"  ❌ {agent_file.name} - Erreur ligne {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"  ❌ {agent_file.name} - Erreur: {e}")
        return False

def correction_finale_complete():
    """Correction finale complète de tous les agents"""
    
    print("🚀 CORRECTION FINALE - Résolution complète des erreurs d'indentation")
    
    agent_dir = Path("agent_equipe_maintenance")
    if not agent_dir.exists():
        print("❌ Répertoire agent_equipe_maintenance non trouvé")
        return
    
    agents_files = list(agent_dir.glob("agent_MAINTENANCE_*.py"))
    total_corrections = 0
    agents_corriges = []
    agents_finaux_ok = []
    
    # Phase 1: Correction ligne par ligne
    print("\n📝 PHASE 1: Correction ligne par ligne")
    for agent_file in agents_files:
        corrections = corriger_agent_ligne_par_ligne(agent_file)
        total_corrections += corrections
        if corrections > 0:
            agents_corriges.append(agent_file.name)
    
    # Phase 2: Test de syntaxe final
    print("\n🧪 PHASE 2: Test de syntaxe final")
    for agent_file in agents_files:
        if tester_syntaxe_agent(agent_file):
            agents_finaux_ok.append(agent_file.name)
    
    # Phase 3: Rapport final
    print(f"\n📊 RAPPORT FINAL:")
    print(f"Total corrections appliquées: {total_corrections}")
    print(f"Agents modifiés: {len(agents_corriges)}")
    print(f"Agents syntaxe OK: {len(agents_finaux_ok)}/{len(agents_files)}")
    
    if len(agents_finaux_ok) == len(agents_files):
        print("\n🎯 SUCCÈS TOTAL! Tous les agents sont maintenant fonctionnels!")
        print("✅ Le workflow de l'équipe de maintenance peut être testé.")
        return True
    else:
        print(f"\n⚠️ {len(agents_files) - len(agents_finaux_ok)} agent(s) nécessitent encore une intervention manuelle")
        return False

if __name__ == "__main__":
    success = correction_finale_complete()
    
    if success:
        print("\n🚀 Prêt pour le test du workflow!")
    else:
        print("\n⚠️ Corrections manuelles nécessaires avant le test du workflow.") 



