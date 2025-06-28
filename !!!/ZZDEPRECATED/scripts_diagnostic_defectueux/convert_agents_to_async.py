#!/usr/bin/env python3
"""
🔧 CONVERSION AUTOMATIQUE AGENTS SYNC → ASYNC
============================================

🎯 Mission : Convertir automatiquement tous les agents de sync vers async
⚠️ Correction architecture suite découverte incohérence core

Author: Équipe Architecture Core
Version: 1.0.0 - Correction Urgente
Created: 2025-06-19 19h35
"""

import os
import re
import glob
from pathlib import Path
from typing import List, Dict, Tuple

class AgentAsyncConverter:
    """🔧 Convertisseur automatique sync → async pour agents"""
    
    def __init__(self, agents_dir: str = "."):
        self.agents_dir = Path(agents_dir)
        self.converted_count = 0
        self.errors = []
        
    def convert_all_agents(self) -> Dict[str, any]:
        """🚀 Convertit tous les agents Python du dossier"""
        
        print("🔧 CONVERSION AGENTS SYNC → ASYNC EN COURS...")
        
        # Trouver tous les fichiers agents Python
        agent_files = list(self.agents_dir.glob("agent_*.py"))
        
        results = {
            "total_files": len(agent_files),
            "converted": 0,
            "errors": [],
            "files_processed": []
        }
        
        for agent_file in agent_files:
            try:
                if self.convert_agent_file(agent_file):
                    results["converted"] += 1
                    results["files_processed"].append(str(agent_file.name))
                    print(f"✅ Converti: {agent_file.name}")
                else:
                    print(f"⏭️ Ignoré: {agent_file.name} (déjà async ou pas d'agent)")
                    
            except Exception as e:
                error_msg = f"❌ Erreur {agent_file.name}: {str(e)}"
                results["errors"].append(error_msg)
                print(error_msg)
        
        return results
    
    def convert_agent_file(self, file_path: Path) -> bool:
        """🔧 Convertit un fichier agent spécifique"""
        
        # Lire le contenu
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si c'est un agent valide
        if not self._is_valid_agent_file(content):
            return False
            
        # Vérifier si déjà async
        if self._is_already_async(content):
            return False
        
        # Effectuer les conversions
        new_content = self._apply_async_conversions(content)
        
        # Sauvegarder si modifié
        if new_content != content:
            # Backup original
            backup_path = file_path.with_suffix('.py.sync_backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Écrire version async
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
            
        return False
    
    def _is_valid_agent_file(self, content: str) -> bool:
        """🔍 Vérifie si le fichier contient un agent valide"""
        
        # Rechercher patterns d'agent
        patterns = [
            r'class.*Agent.*:',
            r'def execute_task\(',
            r'from.*agent_factory_architecture.*import',
            r'Agent\(',
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
                
        return False
    
    def _is_already_async(self, content: str) -> bool:
        """🔍 Vérifie si l'agent est déjà async"""
        
        # Rechercher async execute_task
        if re.search(r'async\s+def\s+execute_task', content):
            return True
            
        return False
    
    def _apply_async_conversions(self, content: str) -> str:
        """🔧 Applique toutes les conversions sync → async"""
        
        new_content = content
        
        # 1. Convertir execute_task sync → async
        new_content = re.sub(
            r'(\s+)def\s+execute_task\s*\(',
            r'\1async def execute_task(',
            new_content
        )
        
        # 2. Convertir startup sync → async (si présent et pas déjà async)
        new_content = re.sub(
            r'(\s+)def\s+startup\s*\(',
            r'\1async def startup(',
            new_content
        )
        
        # 3. Convertir shutdown sync → async (si présent et pas déjà async)
        new_content = re.sub(
            r'(\s+)def\s+shutdown\s*\(',
            r'\1async def shutdown(',
            new_content
        )
        
        # 4. Convertir health_check sync → async (si présent et pas déjà async)
        new_content = re.sub(
            r'(\s+)def\s+health_check\s*\(',
            r'\1async def health_check(',
            new_content
        )
        
        # 5. Ajouter imports asyncio si nécessaire
        if 'import asyncio' not in new_content and 'async def' in new_content:
            # Trouver la section imports
            import_section = re.search(r'(import.*?\n)+', new_content)
            if import_section:
                new_content = new_content.replace(
                    import_section.group(0),
                    import_section.group(0) + 'import asyncio\n'
                )
            else:
                # Ajouter au début si pas d'imports trouvés
                new_content = 'import asyncio\n' + new_content
        
        # 6. Convertir time.sleep() → await asyncio.sleep()
        new_content = re.sub(
            r'time\.sleep\(',
            'await asyncio.sleep(',
            new_content
        )
        
        # 7. Ajouter commentaire de conversion
        conversion_comment = '''
# 🔧 CONVERTI AUTOMATIQUEMENT SYNC → ASYNC
# Date: 2025-06-19 19h35 - Correction architecture Pattern Factory
# Raison: Harmonisation async/sync avec core/agent_factory_architecture.py
'''
        
        if '# 🔧 CONVERTI AUTOMATIQUEMENT' not in new_content:
            # Ajouter après les imports
            lines = new_content.split('\n')
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('"""') and '"""' in line[3:]:
                    insert_pos = i + 1
                    break
                elif line.strip().endswith('"""') and i > 0:
                    insert_pos = i + 1
                    break
            
            lines.insert(insert_pos, conversion_comment)
            new_content = '\n'.join(lines)
        
        return new_content
    
    def generate_conversion_report(self, results: Dict) -> str:
        """📊 Génère un rapport de conversion"""
        
        report = f"""
# 📊 RAPPORT CONVERSION AGENTS SYNC → ASYNC

**Date :** 19 juin 2025 - 19h35  
**Mission :** Correction architecture Pattern Factory  

## 📈 RÉSULTATS

- **Fichiers analysés :** {results['total_files']}
- **Fichiers convertis :** {results['converted']}
- **Taux de conversion :** {(results['converted']/results['total_files']*100):.1f}%
- **Erreurs :** {len(results['errors'])}

## ✅ FICHIERS CONVERTIS

"""
        
        for file_name in results['files_processed']:
            report += f"- ✅ {file_name}\n"
        
        if results['errors']:
            report += "\n## ❌ ERREURS\n\n"
            for error in results['errors']:
                report += f"- {error}\n"
        
        report += f"""
## 🔧 CONVERSIONS APPLIQUÉES

1. **execute_task** : `def` → `async def`
2. **startup** : `def` → `async def` 
3. **shutdown** : `def` → `async def`
4. **health_check** : `def` → `async def`
5. **time.sleep()** : → `await asyncio.sleep()`
6. **Import asyncio** : Ajouté automatiquement
7. **Backup** : Fichiers originaux sauvés (.sync_backup)

## 🎯 ÉTAPES SUIVANTES

1. ✅ Architecture core corrigée
2. ✅ Agents convertis en async
3. 🔄 Tests d'intégration async
4. 🔄 Validation performance
5. 🔄 Certification déploiement
"""
        
        return report


def main():
    """🚀 Point d'entrée principal"""
    
    print("🔧 DÉMARRAGE CONVERSION AGENTS SYNC → ASYNC")
    print("=" * 50)
    
    # Initialiser convertisseur
    converter = AgentAsyncConverter(".")
    
    # Effectuer conversion
    results = converter.convert_all_agents()
    
    # Générer rapport
    report = converter.generate_conversion_report(results)
    
    # Sauvegarder rapport
    with open("../RAPPORT_CONVERSION_ASYNC.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\n" + "=" * 50)
    print(f"🎉 CONVERSION TERMINÉE !")
    print(f"📊 {results['converted']}/{results['total_files']} agents convertis")
    print(f"📄 Rapport: RAPPORT_CONVERSION_ASYNC.md")
    
    if results['errors']:
        print(f"⚠️ {len(results['errors'])} erreurs à vérifier manuellement")
    
    return results


if __name__ == "__main__":
    main() 



