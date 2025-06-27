#!/usr/bin/env python3
"""
Script de migration automatisée du logging uniforme.
Applique le pattern standard à tous les agents non conformes.
"""
import os
import re
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

def backup_file(file_path: Path) -> str:
    """Crée une sauvegarde du fichier original."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"
    shutil.copy2(file_path, backup_path)
    return backup_path

def detect_agent_info(content: str, file_name: str) -> Dict[str, str]:
    """Détecte les informations spécifiques de l'agent pour personnaliser le logging."""
    
    # Déterminer le type d'agent
    if "MAINTENANCE" in file_name:
        agent_role = "maintenance"
    elif "POSTGRESQL" in file_name:
        agent_role = "postgresql"
    elif "FASTAPI" in file_name:
        agent_role = "fastapi"
    elif "ARCHITECTURE" in file_name:
        agent_role = "architecture"
    elif "SECURITY" in file_name:
        agent_role = "security"
    elif "MONITORING" in file_name:
        agent_role = "monitoring"
    elif "STORAGE" in file_name:
        agent_role = "storage"
    elif "coordinateur" in file_name.lower():
        agent_role = "coordinateur"
    elif "architecte" in file_name.lower():
        agent_role = "architecte"
    elif "configuration" in file_name.lower():
        agent_role = "configuration"
    elif "securite" in file_name.lower():
        agent_role = "securite"
    elif "testeur" in file_name.lower() or "test" in file_name.lower():
        agent_role = "test"
    elif "auditeur" in file_name.lower() or "audit" in file_name.lower():
        agent_role = "audit"
    elif "documenteur" in file_name.lower() or "documentation" in file_name.lower():
        agent_role = "documentation"
    else:
        agent_role = "general"
    
    # Extraire l'ID agent du nom de fichier
    agent_match = re.search(r'agent_(\w+)', file_name)
    agent_id_suffix = agent_match.group(1) if agent_match else "unknown"
    
    # Extraire agent_type du fichier de classe
    agent_type_match = re.search(r'agent_type\s*=\s*["\']([^"\']+)["\']', content)
    agent_type = agent_type_match.group(1) if agent_type_match else agent_role
    
    return {
        "agent_role": agent_role,
        "agent_id_suffix": agent_id_suffix,
        "agent_type": agent_type,
        "config_name": agent_role
    }

def find_init_method(content: str) -> tuple:
    """Trouve la méthode __init__ et retourne sa position."""
    
    # Recherche de différents patterns d'initialisation
    patterns = [
        r'(\s*def __init__\(self[^)]*\):\s*\n)',
        r'(\s*def __init__\([^)]*\):\s*\n)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            init_start = match.end()
            
            # Trouver la fin de la méthode __init__
            lines = content[init_start:].split('\n')
            init_end = init_start
            indent_level = None
            
            for i, line in enumerate(lines):
                if line.strip() == '':
                    continue
                    
                current_indent = len(line) - len(line.lstrip())
                
                if indent_level is None:
                    indent_level = current_indent
                elif current_indent <= 4 and line.strip() and not line.strip().startswith('#'):
                    # Fin de la méthode __init__
                    init_end = init_start + sum(len(l) + 1 for l in lines[:i])
                    break
                    
            if init_end == init_start:
                # Prendre tout le reste si pas de fin détectée
                init_end = len(content)
            
            return match.group(1), init_start, init_end
    
    return None, -1, -1

def generate_logging_code(agent_info: Dict[str, str]) -> str:
    """Génère le code de logging uniforme personnalisé."""
    
    return f'''        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="{agent_info['config_name']}",
                custom_config={{
                    "logger_name": f"nextgen.{agent_info['agent_role']}.{agent_info['agent_id_suffix']}.{{self.agent_id if hasattr(self, 'agent_id') else self.id if hasattr(self, 'id') else 'unknown'}}",
                    "log_dir": "logs/{agent_info['agent_role']}",
                    "metadata": {{
                        "agent_type": "{agent_info['agent_id_suffix']}",
                        "agent_role": "{agent_info['agent_role']}",
                        "system": "nextgeneration"
                    }}
                }}
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
'''

def migrate_agent_file(file_path: Path) -> bool:
    """Migre un fichier agent vers le logging uniforme."""
    
    try:
        # Lire le contenu
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si déjà migré
        if 'MIGRATION SYSTÈME LOGGING UNIFIÉ' in content:
            print(f"✅ {file_path.name} - Déjà migré")
            return True
        
        # Détecter les informations de l'agent
        agent_info = detect_agent_info(content, file_path.name)
        
        # Trouver la méthode __init__
        init_signature, init_start, init_end = find_init_method(content)
        
        if init_start == -1:
            print(f"❌ {file_path.name} - Méthode __init__ non trouvée")
            return False
        
        # Créer une sauvegarde
        backup_path = backup_file(file_path)
        print(f"💾 {file_path.name} - Sauvegarde créée: {Path(backup_path).name}")
        
        # Trouver le point d'insertion (après super().__init__ ou au début de __init__)
        init_content = content[init_start:init_end]
        lines = init_content.split('\n')
        
        insertion_point = 0
        for i, line in enumerate(lines):
            if 'super().__init__' in line or 'super().__init__(' in line:
                # Insérer après l'appel super()
                insertion_point = i + 1
                break
            elif line.strip() and not line.strip().startswith('#'):
                # Premier ligne non vide non commentaire
                insertion_point = i
                break
        
        # Générer le code de logging
        logging_code = generate_logging_code(agent_info)
        
        # Insérer le code
        lines.insert(insertion_point, logging_code)
        new_init_content = '\n'.join(lines)
        
        # Reconstruire le fichier
        new_content = content[:init_start] + new_init_content + content[init_end:]
        
        # Écrire le nouveau contenu
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ {file_path.name} - Migration réussie")
        return True
        
    except Exception as e:
        print(f"❌ {file_path.name} - Erreur: {str(e)}")
        return False

def main():
    """Fonction principale."""
    print("🚀 MIGRATION AUTOMATISÉE LOGGING UNIFORME")
    print("=" * 60)
    
    # Lire le rapport de conformité le plus récent
    reports = list(Path('.').glob('rapport_conformite_logging_*.json'))
    if not reports:
        print("❌ Aucun rapport de conformité trouvé. Exécutez validate_logging_migration.py d'abord.")
        return
    
    latest_report = max(reports, key=lambda p: p.stat().st_mtime)
    
    with open(latest_report, 'r', encoding='utf-8') as f:
        report_data = json.load(f)
    
    # Récupérer les agents non conformes
    non_compliant = []
    for result in report_data['detailed_results']:
        if result.get('status') in ['NON_CONFORME', 'PARTIELLEMENT_CONFORME']:
            non_compliant.append(result['file_name'])
    
    print(f"📊 {len(non_compliant)} agents à migrer")
    
    # Agents à exclure (déjà migrés manuellement ou problématiques)
    exclude_files = {
        'agent_01_coordinateur_principal.py',
        'agent_02_architecte_code_expert.py', 
        'agent_03_specialiste_configuration.py',
        'agent_04_expert_securite_crypto.py'
    }
    
    # Filtrer les agents à migrer
    agents_to_migrate = [f for f in non_compliant if f not in exclude_files]
    
    print(f"🎯 {len(agents_to_migrate)} agents dans la file de migration")
    
    # Statistiques
    success_count = 0
    failed_count = 0
    
    # Migrer par priorité
    agents_dir = Path("agents")
    
    # Priorité HAUTE d'abord
    high_priority = [f for f in agents_to_migrate 
                    if any(x in f for x in ["05_maitre", "06_specialiste"])]
    
    # Priorité MOYENNE
    medium_priority = [f for f in agents_to_migrate 
                      if any(x in f for x in ["POSTGRESQL", "FASTAPI", "ARCHITECTURE", "SECURITY"])]
    
    # Le reste
    remaining = [f for f in agents_to_migrate 
                if f not in high_priority and f not in medium_priority]
    
    # Traitement par ordre de priorité
    for priority_name, priority_list in [
        ("HAUTE", high_priority), 
        ("MOYENNE", medium_priority), 
        ("BASSE", remaining)
    ]:
        if priority_list:
            print(f"\n🎯 PRIORITÉ {priority_name} ({len(priority_list)} agents)")
            print("-" * 40)
            
            for filename in priority_list:
                file_path = agents_dir / filename
                if file_path.exists():
                    if migrate_agent_file(file_path):
                        success_count += 1
                    else:
                        failed_count += 1
                else:
                    print(f"❌ {filename} - Fichier non trouvé")
                    failed_count += 1
    
    # Résumé final
    print(f"\n📈 RÉSUMÉ MIGRATION")
    print("-" * 40)
    print(f"✅ Succès: {success_count}")
    print(f"❌ Échecs: {failed_count}")
    print(f"📊 Total traité: {success_count + failed_count}")
    
    if success_count > 0:
        print(f"\n🔍 Relancez validate_logging_migration.py pour vérifier les résultats!")

if __name__ == "__main__":
    main()