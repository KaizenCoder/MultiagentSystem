#!/usr/bin/env python3
"""
Script de correction des erreurs de syntaxe dans les agents.
Corrige les problèmes créés par le script de migration automatique.
"""
import re
import shutil
from pathlib import Path
from datetime import datetime

def backup_file(file_path: Path) -> str:
    """Crée une sauvegarde du fichier."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_syntax_{timestamp}"
    shutil.copy2(file_path, backup_path)
    return backup_path

def fix_postgresql_agents():
    """Corrige les agents POSTGRESQL avec problèmes de syntaxe."""
    agents_dir = Path("agents")
    postgresql_files = list(agents_dir.glob("agent_POSTGRESQL_*.py"))
    
    print(f"🔧 CORRECTION AGENTS POSTGRESQL ({len(postgresql_files)} fichiers)")
    
    for file_path in postgresql_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier si le problème est présent
            if "super().__init__(\n        \n        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ" in content:
                backup_path = backup_file(file_path)
                print(f"💾 {file_path.name} - Sauvegarde: {Path(backup_path).name}")
                
                # Pattern pour corriger l'insertion mal placée
                pattern = r'(def __init__\([^)]*\):\s*\n\s*super\(\).__init__\(\s*)\n\s*# ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ.*?self\.logger = logging\.getLogger\(self\.__class__\.__name__\)\s*\n\s*(.*?\))'
                
                # Remplacer par la version corrigée
                replacement = r'\1\2\n        \n        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ\n        try:\n            from core.manager import LoggingManager\n            logging_manager = LoggingManager()\n            self.logger = logging_manager.get_logger(\n                config_name="postgresql",\n                custom_config={\n                    "logger_name": f"nextgen.postgresql.{file_path.stem}.{{self.agent_id if hasattr(self, \'agent_id\') else \'unknown\'}}",\n                    "log_dir": "logs/postgresql",\n                    "metadata": {\n                        "agent_type": "' + file_path.stem + '",\n                        "agent_role": "postgresql",\n                        "system": "nextgeneration"\n                    }\n                }\n            )\n        except ImportError:\n            # Fallback en cas d\'indisponibilité du LoggingManager\n            self.logger = logging.getLogger(self.__class__.__name__)'
                
                fixed_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                
                if fixed_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    print(f"✅ {file_path.name} - Corrigé")
                else:
                    print(f"⚠️ {file_path.name} - Pattern non trouvé, correction manuelle nécessaire")
            else:
                print(f"✅ {file_path.name} - Déjà correct")
                
        except Exception as e:
            print(f"❌ {file_path.name} - Erreur: {str(e)}")

def fix_indentation_errors():
    """Corrige les erreurs d'indentation dans les agents."""
    agents_dir = Path("agents")
    
    # Agents avec problèmes d'indentation identifiés
    problematic_agents = [
        "agent_109_specialiste_planes.py",
        "agent_110_documentaliste_expert.py", 
        "agent_111_auditeur_qualite.py",
        "agent_14_specialiste_workspace.py",
        "agent_16_peer_reviewer_senior.py",
        "agent_FASTAPI_23_orchestration_enterprise.py",
        "agent_META_AUDITEUR_UNIVERSEL.py",
        "agent_orchestrateur_audit.py",
        "agent_STORAGE_24_enterprise_manager.py",
        "agent_testeur_agents.py",
        "agent_testeur_agents_complet.py",
        "agent_test_models_integration.py",
        "agent_test_models_integration_clean.py"
    ]
    
    print(f"\n🔧 CORRECTION ERREURS INDENTATION ({len(problematic_agents)} fichiers)")
    
    for filename in problematic_agents:
        file_path = agents_dir / filename
        if not file_path.exists():
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            backup_path = backup_file(file_path)
            print(f"💾 {filename} - Sauvegarde: {Path(backup_path).name}")
            
            fixed_lines = []
            for i, line in enumerate(lines):
                # Vérifier les fonctions vides
                if re.match(r'\s*def\s+\w+\([^)]*\):\s*$', line):
                    fixed_lines.append(line)
                    # Vérifier si la ligne suivante est vide ou commence une autre définition
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        if (next_line.strip() == '' or 
                            next_line.strip().startswith('def ') or
                            next_line.strip().startswith('class ') or
                            not next_line.startswith('    ')):
                            fixed_lines.append('        pass  # TODO: Implémenter\n')
                    else:
                        fixed_lines.append('        pass  # TODO: Implémenter\n')
                # Vérifier les blocs try vides
                elif re.match(r'\s*try:\s*$', line):
                    fixed_lines.append(line)
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        if (next_line.strip() == '' or
                            not next_line.startswith('    ')):
                            fixed_lines.append('        pass  # TODO: Implémenter\n')
                else:
                    fixed_lines.append(line)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)
                
            print(f"✅ {filename} - Corrigé")
            
        except Exception as e:
            print(f"❌ {filename} - Erreur: {str(e)}")

def fix_specific_syntax_errors():
    """Corrige des erreurs de syntaxe spécifiques."""
    agents_dir = Path("agents")
    
    # agent_MAINTENANCE_00_chef_equipe_coordinateur_parallel.py
    file_path = agents_dir / "agent_MAINTENANCE_00_chef_equipe_coordinateur_parallel.py"
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            backup_path = backup_file(file_path)
            print(f"💾 {file_path.name} - Sauvegarde: {Path(backup_path).name}")
            
            # Corriger les problèmes de syntaxe évidents
            # Remplacer les caractères problématiques
            fixed_content = content.replace('"""', '"""').replace('"""', '"""')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
                
            print(f"✅ {file_path.name} - Corrigé")
            
        except Exception as e:
            print(f"❌ {file_path.name} - Erreur: {str(e)}")
    
    # agent_MONITORING_25_production_enterprise.py - problème d'indentation
    file_path = agents_dir / "agent_MONITORING_25_production_enterprise.py"
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            backup_path = backup_file(file_path)
            print(f"💾 {file_path.name} - Sauvegarde: {Path(backup_path).name}")
            
            # Corriger l'indentation problématique ligne 47
            if len(lines) > 46:
                line_47 = lines[46]
                if line_47.strip() and not line_47.startswith('    ') and not line_47.startswith('#'):
                    lines[46] = '    ' + line_47.lstrip()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
                
            print(f"✅ {file_path.name} - Corrigé")
            
        except Exception as e:
            print(f"❌ {file_path.name} - Erreur: {str(e)}")

def fix_f_string_error():
    """Corrige l'erreur f-string dans agent_03_specialiste_configuration.py."""
    file_path = Path("agents/agent_03_specialiste_configuration.py")
    if not file_path.exists():
        return
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        backup_path = backup_file(file_path)
        print(f"💾 {file_path.name} - Sauvegarde: {Path(backup_path).name}")
        
        # Chercher et corriger les f-strings problématiques
        # Pattern pour f-strings avec expressions trop imbriquées
        pattern = r'f"[^"]*\{[^}]*\{[^}]*\}[^}]*\}"'
        
        def fix_nested_fstring(match):
            # Simplifier les f-strings trop complexes
            return match.group(0).replace('{', '{{').replace('}', '}}')
        
        fixed_content = re.sub(pattern, fix_nested_fstring, content)
        
        # Si pas de changement, chercher les lignes problématiques autour de la ligne 493
        if fixed_content == content:
            lines = content.split('\n')
            for i in range(max(0, 490), min(len(lines), 500)):
                if 'f"' in lines[i] and lines[i].count('{') > lines[i].count('}'):
                    # Corriger en utilisant .format() au lieu de f-string
                    lines[i] = lines[i].replace('f"', '"').replace('{', '{0}')
                    break
            fixed_content = '\n'.join(lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
            
        print(f"✅ {file_path.name} - Corrigé")
        
    except Exception as e:
        print(f"❌ {file_path.name} - Erreur: {str(e)}")

def main():
    """Fonction principale."""
    print("🔧 CORRECTION ERREURS SYNTAXE AGENTS")
    print("=" * 50)
    
    # 1. Corriger agents POSTGRESQL
    fix_postgresql_agents()
    
    # 2. Corriger erreurs d'indentation
    fix_indentation_errors()
    
    # 3. Corriger erreurs spécifiques
    print(f"\n🔧 CORRECTION ERREURS SPÉCIFIQUES")
    fix_specific_syntax_errors()
    
    # 4. Corriger erreur f-string
    print(f"\n🔧 CORRECTION ERREUR F-STRING")
    fix_f_string_error()
    
    print(f"\n✅ CORRECTION TERMINÉE!")
    print("Relancez le test d'import pour vérifier les corrections.")

if __name__ == "__main__":
    main()