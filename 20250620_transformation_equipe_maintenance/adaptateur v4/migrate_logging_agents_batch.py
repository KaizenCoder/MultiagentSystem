#!/usr/bin/env python3
"""
SCRIPT MIGRATION LOGGING AUTOMATIQUE - AGENTS MAINTENANCE
=========================================================

Script pour automatiser la migration du système de logging des agents
de maintenance vers le LoggingManager unifié.

Author: Migration Team NextGeneration
Version: 1.0.0
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration des agents restants à migrer
AGENTS_TO_MIGRATE = [
    "agent_MAINTENANCE_02_evaluateur_utilite.py",
    "agent_MAINTENANCE_03_adaptateur_code.py", 
    "agent_MAINTENANCE_04_testeur_anti_faux_agents.py",
    "agent_MAINTENANCE_07_gestionnaire_dependances.py",
    "agent_MAINTENANCE_08_analyseur_performance.py",
    "agent_MAINTENANCE_11_harmonisateur_style.py",
    "agent_MAINTENANCE_12_correcteur_semantique.py"
]

# Mapping des rôles pour la configuration
AGENT_ROLES = {
    "02": "evaluateur_utilite",
    "03": "adaptateur_code", 
    "04": "testeur_anti_faux_agents",
    "07": "gestionnaire_dependances",
    "08": "analyseur_performance",
    "11": "harmonisateur_style",
    "12": "correcteur_semantique"
}

# Mapping des répertoires de logs
LOG_DIRS = {
    "02": "evaluateur",
    "03": "adaptateur",
    "04": "testeur", 
    "07": "gestionnaire",
    "08": "analyseur",
    "11": "harmonisateur",
    "12": "correcteur"
}

def migrate_agent_logging(agent_file: Path) -> bool:
    """
    Migre un agent spécifique vers le système de logging unifié.
    
    Args:
        agent_file: Chemin vers le fichier agent à migrer
        
    Returns:
        bool: True si la migration a réussi, False sinon
    """
    try:
        # Extraction du numéro d'agent
        match = re.search(r'agent_MAINTENANCE_(\d+)', agent_file.name)
        if not match:
            print(f"❌ Impossible d'extraire le numéro d'agent de {agent_file.name}")
            return False
            
        agent_num = match.group(1)
        agent_role = AGENT_ROLES.get(agent_num, f"maintenance_{agent_num}")
        log_dir = LOG_DIRS.get(agent_num, f"agent_{agent_num}")
        
        # Lecture du contenu
        content = agent_file.read_text(encoding='utf-8')
        
        # Vérification si déjà migré
        if "from core.manager import LoggingManager" in content:
            print(f"✅ {agent_file.name} déjà migré")
            return True
            
        # Pattern de remplacement
        old_pattern = r'self\.logger = logging\.getLogger\(.*?\)'
        
        new_logging_config = f'''# ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={{
                    "logger_name": f"nextgen.maintenance.{agent_role}.{{self.id}}",
                    "log_dir": "logs/maintenance/{log_dir}",
                    "metadata": {{
                        "agent_type": "MAINTENANCE_{agent_num}_{agent_role}",
                        "agent_role": "{agent_role}",
                        "system": "nextgeneration"
                    }}
                }}
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)'''
        
        # Remplacement
        new_content = re.sub(old_pattern, new_logging_config, content)
        
        if new_content == content:
            print(f"⚠️  Aucun pattern de logging trouvé dans {agent_file.name}")
            return False
            
        # Sauvegarde
        agent_file.write_text(new_content, encoding='utf-8')
        print(f"✅ {agent_file.name} migré avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur migration {agent_file.name}: {e}")
        return False

def main():
    """Point d'entrée principal du script de migration."""
    print("🚀 MIGRATION AUTOMATIQUE LOGGING AGENTS MAINTENANCE")
    print("=" * 60)
    
    # Répertoire des agents
    agents_dir = Path(__file__).parent / "agents"
    
    if not agents_dir.exists():
        print(f"❌ Répertoire agents non trouvé: {agents_dir}")
        return False
        
    # Migration par lot
    success_count = 0
    total_count = len(AGENTS_TO_MIGRATE)
    
    for agent_filename in AGENTS_TO_MIGRATE:
        agent_file = agents_dir / agent_filename
        
        if not agent_file.exists():
            print(f"⚠️  Agent non trouvé: {agent_file}")
            continue
            
        print(f"\n🔧 Migration: {agent_filename}")
        if migrate_agent_logging(agent_file):
            success_count += 1
    
    # Rapport final
    print(f"\n{'=' * 60}")
    print(f"📊 RAPPORT MIGRATION FINALE")
    print(f"{'=' * 60}")
    print(f"✅ Agents migrés: {success_count}/{total_count}")
    print(f"📊 Taux de succès: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print(f"🎉 MIGRATION COMPLÈTE RÉUSSIE!")
        print(f"   Tous les agents MAINTENANCE utilisent maintenant le LoggingManager unifié")
        return True
    else:
        print(f"⚠️  Migration partielle. Vérification manuelle requise.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)