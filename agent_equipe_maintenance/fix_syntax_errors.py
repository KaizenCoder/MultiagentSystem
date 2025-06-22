#!/usr/bin/env python3
"""
🔧 CORRECTEUR AUTOMATIQUE SYNTAX - Équipe Maintenance NextGeneration
===============================================================

Mission: Corriger automatiquement les erreurs syntaxe critiques
- Éliminer 'async async def'
- Corriger les imports Pattern Factory
- Standardiser l'indentation
- Valider la syntaxe Python

Author: Expert Maintenance
Version: 1.0.0
"""

import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import shutil
from datetime import datetime

class SyntaxCorrector:
    """Correcteur automatique de syntax pour l'équipe maintenance"""
    
    def __init__(self):
        self.corrections_applied = []
        self.errors_found = []
        
    def fix_all_agents(self, directory: str = ".") -> Dict[str, any]:
        """Correction complète de tous les agents"""
        print("🔧 DÉMARRAGE CORRECTION AUTOMATIQUE SYNTAX")
        print("=" * 60)
        
        target_dir = Path(directory)
        agent_files = list(target_dir.glob("agent_MAINTENANCE_*.py"))
        
        results = {
            "files_processed": 0,
            "files_corrected": 0,
            "total_corrections": 0,
            "corrections_by_file": {},
            "errors_found": []
        }
        
        for agent_file in agent_files:
            print(f"\n🔍 Analyse: {agent_file.name}")
            
            try:
                corrections = self.fix_single_file(agent_file)
                results["files_processed"] += 1
                
                if corrections["corrections_applied"]:
                    results["files_corrected"] += 1
                    results["total_corrections"] += len(corrections["corrections_applied"])
                    results["corrections_by_file"][agent_file.name] = corrections
                    print(f"✅ {len(corrections['corrections_applied'])} corrections appliquées")
                else:
                    print(f"ℹ️ Aucune correction nécessaire")
                    
            except Exception as e:
                error_msg = f"Erreur {agent_file.name}: {e}"
                results["errors_found"].append(error_msg)
                print(f"❌ {error_msg}")
        
        print(f"\n📊 RÉSUMÉ CORRECTIONS:")
        print(f"   📁 Fichiers traités: {results['files_processed']}")
        print(f"   ✅ Fichiers corrigés: {results['files_corrected']}")
        print(f"   🔧 Total corrections: {results['total_corrections']}")
        
        return results
    
    def fix_single_file(self, file_path: Path) -> Dict[str, any]:
        """Correction d'un fichier unique"""
        
        # Lire le contenu original
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        corrections_applied = []
        
        # 1. CORRECTION: async async def
        if 'async async def' in content:
            content = re.sub(r'async\s+async\s+def', 'async def', content)
            corrections_applied.append("✅ Correction 'async async def' → 'async def'")
        
        # 2. CORRECTION: Import Pattern Factory manquant
        if 'from agent_factory_implementation' not in content and 'from core.agent_factory_architecture' not in content:
            import_block = '''
# Import Pattern Factory (OBLIGATOIRE selon guide)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
    try:
        from core.agent_factory_architecture import Agent, Task, Result
        PATTERN_FACTORY_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️ Pattern Factory non disponible: {e}")
        
        # Fallback pour compatibilité
        class Agent:
            def __init__(self, agent_type: str, **config):
                self.agent_id = f"agent_{int(time.time())}"
                self.agent_type = agent_type
                self.config = config
                
            async def startup(self): pass
            async def shutdown(self): pass
            async def health_check(self): return {"status": "healthy"}
            def get_capabilities(self): return []
        
        class Task:
            def __init__(self, task_id: str, description: str, **kwargs):
                self.task_id = task_id
                self.description = description
                
        class Result:
            def __init__(self, success: bool, data: any = None, error: str = None):
                self.success = success
                self.data = data
                self.error = error
        
        PATTERN_FACTORY_AVAILABLE = False

'''
            # Insérer après les commentaires d'en-tête
            lines = content.split('\n')
            insert_position = 0
            
            # Trouver la fin des commentaires d'en-tête
            in_header = True
            for i, line in enumerate(lines):
                if in_header and (line.strip().startswith('"""') or line.strip().startswith("'''")):
                    # Début ou fin de docstring
                    if line.count('"""') == 2 or line.count("'''") == 2:
                        insert_position = i + 1
                        break
                    else:
                        in_header = not in_header
                elif not in_header and (line.strip().endswith('"""') or line.strip().endswith("'''")):
                    insert_position = i + 1
                    break
                elif not line.strip().startswith('#') and not line.strip().startswith('"""') and not line.strip().startswith("'''") and line.strip():
                    insert_position = i
                    break
            
            lines.insert(insert_position, import_block)
            content = '\n'.join(lines)
            corrections_applied.append("✅ Ajout import Pattern Factory complet")
        
        # 3. CORRECTION: Indentation standardisée
        lines = content.split('\n')
        corrected_lines = []
        
        for line in lines:
            # Convertir tabs en espaces
            if '\t' in line:
                line = line.expandtabs(4)
                
            # Corriger les sur-indentations communes
            if line.startswith('        ') and line.strip():
                # Vérifier si c'est une sur-indentation ou normal
                stripped = line.strip()
                if (stripped.startswith('async def ') or 
                    stripped.startswith('def ') or
                    stripped.startswith('class ') or
                    stripped.startswith('return ') or
                    stripped.startswith('raise ') or
                    stripped in ['pass', 'break', 'continue']):
                    line = '    ' + stripped  # Réduire à 4 espaces
                    
            corrected_lines.append(line)
        
        if corrected_lines != content.split('\n'):
            content = '\n'.join(corrected_lines)
            corrections_applied.append("✅ Standardisation indentation (4 espaces)")
        
        # 4. VALIDATION: Vérifier syntaxe Python
        try:
            ast.parse(content)
            syntax_valid = True
        except SyntaxError as e:
            syntax_valid = False
            corrections_applied.append(f"⚠️ Erreur syntaxe résiduelle: {e}")
        
        # 5. SAUVEGARDE: Si des corrections ont été appliquées
        if corrections_applied and content != original_content:
            # Backup du fichier original
            backup_path = file_path.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py')
            shutil.copy2(file_path, backup_path)
            
            # Sauvegarder le fichier corrigé
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            corrections_applied.append(f"💾 Backup créé: {backup_path.name}")
        
        return {
            "file_path": str(file_path),
            "corrections_applied": corrections_applied,
            "syntax_valid": syntax_valid,
            "backup_created": len(corrections_applied) > 0 and content != original_content
        }

def main():
    """Point d'entrée principal"""
    corrector = SyntaxCorrector()
    
    # Argument en ligne de commande pour le répertoire
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    
    results = corrector.fix_all_agents(directory)
    
    print(f"\n🎯 MISSION CORRECTION TERMINÉE")
    print(f"Status: {'✅ SUCCÈS' if results['files_corrected'] > 0 else 'ℹ️ RIEN À CORRIGER'}")
    
    return 0 if len(results['errors_found']) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())





