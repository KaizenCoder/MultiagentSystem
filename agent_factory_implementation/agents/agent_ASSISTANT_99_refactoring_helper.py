#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AGENT ASSISTANT 99 - HELPER DE REFACTORING
==========================================

RÔLE: Assister l'opérateur humain dans les tâches de refactoring complexes et à grande échelle.
MISSION: Automatiser les opérations de recherche, remplacement, exécution de scripts et validation.

CAPACITÉS:
- Exécution de recherches de motifs (grep) sur l'ensemble du projet.
- Exécution de remplacements en masse (sed-like) sur des fichiers ciblés.
- Lancement de scripts de test ou de migration.
- Sauvegarde automatique des fichiers avant modification.
- Rapport détaillé des opérations effectuées.

CONTRAINTES:
- DOIT obtenir une confirmation explicite (simulée ici) avant d'appliquer des modifications destructrices.
- DOIT logger chaque action avec précision.
- DOIT opérer de manière idempotente lorsque c'est possible.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
import json

# Assurer que le module de logging est accessible
try:
    # Chemin relatif de ce fichier à la racine du projet pour trouver le module de logging
    project_root_for_import = Path(__file__).resolve().parents[2]
    # Ajout de la racine du projet au sys.path pour les imports directs comme 'from core import ...'
    if str(project_root_for_import) not in sys.path:
    sys.path.insert(0, str(project_root_for_import))
    from core import logging_manager
except ImportError as e:
    print(f"Erreur critique: Impossible d'importer le logging_manager. Vérifiez que 'core' est à la racine. Erreur: {e}")
    # Fallback sur le logging standard si le manager n'est pas disponible
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.warning("Utilisation du logging standard de Python.")
    logging_manager = None


class AgentAssistant99RefactoringHelper:
    """Agent assistant pour les tâches de refactoring."""

    def __init__(self, project_root: Path):
    self.name = "Agent 99 - Assistant de Refactoring"
    self.role = "assistant"
    self.domain = "refactoring_automation"
    self.project_root = project_root
    self.backup_dir = self.project_root / "backups_docteur" / f"refactoring_helper_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    if logging_manager:
        self.logger = logging_manager.get_logger(
            'refactoring_helper',
            custom_config={
                'logger_name': "AgentAssistant99RefactoringHelper",
                'console_enabled': True,
                'file_enabled': True,
                'file_path': f'logs/refactoring_helper_{datetime.now().strftime("%Y%m%d")}.log'
            }
        )
    else:
        self.logger = logger

    self.metrics = {
        "files_scanned": 0,
        "files_matched": 0,
        "files_edited": 0,
        "backups_created": 0,
        "scripts_executed": 0,
        "operations_failed": 0,
    }
    self._initialize_workspace()

    def _initialize_workspace(self):
        """Prépare l'environnement de travail de l'agent (ex: dossier de backup)."""
    self.logger.info(f"Initialisation du workspace pour {self.name}.")
    try:
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Le répertoire de backup est prêt : {self.backup_dir}")
    except Exception as e:
        self.logger.error(f"Impossible de créer le répertoire de backup : {e}")
        raise

    def _backup_file(self, file_path: Path):
        """Crée une copie de sauvegarde d'un fichier avant de le modifier."""
    try:
        relative_path = file_path.relative_to(self.project_root)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(file_path, backup_path)
        self.metrics["backups_created"] += 1
        self.logger.info(f"Backup créé pour {file_path} -> {backup_path}")
    except Exception as e:
        self.logger.error(f"Échec de la sauvegarde du fichier {file_path}: {e}")
        self.metrics["operations_failed"] += 1

    def _run_command(self, command: List[str], cwd: str) -> Tuple[bool, str, str]:
        """Exécute une commande shell et retourne le succès, stdout et stderr."""
    self.logger.info(f"Exécution de la commande : {' '.join(command)}")
    try:
            # Pour PowerShell, il est plus sûr d'encoder la commande
        if command[0] == 'powershell':
            encoded_command = subprocess.list2cmdline(command)
            process = subprocess.run(
                encoded_command,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                check=False
            )
        else:
             process = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                check=False
            )
            
        if process.returncode != 0:
            self.logger.warning(f"La commande a terminé avec un code d'erreur {process.returncode}.")
            if process.stderr:
                self.logger.warning(f"Stderr: {process.stderr.strip()}")
        return process.returncode == 0, process.stdout.strip(), process.stderr.strip()
    except FileNotFoundError:
        self.logger.error(f"Commande non trouvée : {command[0]}. Assurez-vous qu'elle est dans le PATH.")
        self.metrics["operations_failed"] += 1
        return False, "", f"Commande non trouvée: {command[0]}"
    except Exception as e:
        self.logger.error(f"Erreur inattendue lors de l'exécution de la commande: {e}")
        self.metrics["operations_failed"] += 1
        return False, "", str(e)

    def find_files_with_pattern(self, pattern: str, search_path: str = ".") -> List[Path]:
        """Trouve des fichiers contenant un motif (grep-like)."""
    self.logger.info(f"Recherche du motif '{pattern}' dans '{search_path}'")
        
        # PowerShell est le shell de l'utilisateur, on l'utilise pour la compatibilité
        # Le `.` pour le chemin est relatif au CWD de la commande
    full_search_path = self.project_root / search_path
    ps_command = f'Select-String -Path "{full_search_path}\\*" -Pattern "{pattern}" -SimpleMatch | Select-Object -ExpandProperty Path -Unique'
    command = ['powershell', '-Command', ps_command]
        
    success, stdout, stderr = self._run_command(command, cwd=str(self.project_root))
        
    if not success and "Select-String : Cannot find path" not in stderr:
             # Ignore l'erreur si c'est juste qu'aucun fichier ne correspond
        self.logger.error(f"La recherche de fichiers a échoué. Stderr: {stderr}")
        return []

    files = [Path(p) for p in stdout.splitlines() if p]
    self.metrics["files_matched"] = len(files)
    self.logger.info(f"{len(files)} fichiers trouvés contenant le motif.")
    return files

    def mass_replace_in_files(self, files: List[Path], old_text: str, new_text: str):
        """Effectue un remplacement de texte en masse sur une liste de fichiers."""
    self.logger.info(f"Début du remplacement en masse de '{old_text}' par '{new_text}'.")
    for file_path in files:
        self.logger.info(f"Traitement du fichier : {file_path}")
        if not file_path.exists():
            self.logger.warning(f"Le fichier {file_path} n'existe pas, il a peut-être été déplacé ou supprimé.")
            continue

        self._backup_file(file_path)
        try:
                # Échapper les apostrophes pour PowerShell
            old_text_ps = old_text.replace("'", "''")
            new_text_ps = new_text.replace("'", "''")

            ps_command = f"(Get-Content -Path '{file_path}' -Raw -Encoding utf8) -replace '{old_text_ps}', '{new_text_ps}' | Set-Content -Path '{file_path}' -Encoding utf8"
            command = ['powershell', '-Command', ps_command]

            success, _, stderr = self._run_command(command, cwd=str(self.project_root))

            if success:
                self.logger.info(f"Remplacement réussi dans {file_path}.")
                self.metrics["files_edited"] += 1
            else:
                self.logger.error(f"Échec du remplacement dans {file_path}. Stderr: {stderr}")
                self.metrics["operations_failed"] += 1
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement du fichier {file_path}: {e}")
            self.metrics["operations_failed"] += 1

    def run_script(self, script_path: str, args: List[str] = None) -> bool:
        """Exécute un script Python ou shell."""
    self.logger.info(f"Tentative d'exécution du script : {script_path}")
    script_path_obj = self.project_root / script_path
    if not script_path_obj.exists():
        self.logger.error(f"Le script {script_path_obj} n'a pas été trouvé.")
        self.metrics["operations_failed"] += 1
        return False

    if script_path.endswith(".py"):
        command = [sys.executable, str(script_path_obj)] + (args or [])
    elif script_path.endswith(".ps1"):
         command = ['powershell', '-File', str(script_path_obj)] + (args or [])
    elif script_path.endswith(".sh"):
        command = ['bash', str(script_path_obj)] + (args or [])
    else:
        self.logger.error(f"Type de script non supporté : {script_path}")
        return False

    success, stdout, stderr = self._run_command(command, cwd=str(self.project_root))
    self.logger.info(f"Sortie du script '{script_path}':\n{stdout}")
    if not success:
        self.logger.error(f"Erreur du script '{script_path}':\n{stderr}")
    self.metrics["scripts_executed"] += 1
    return success

    def get_final_report(self) -> Dict[str, Any]:
        """Génère un rapport final sur les opérations effectuées."""
    report = {
        "agent_name": self.name,
        "end_time": datetime.now().isoformat(),
        "metrics": self.metrics,
        "status": "completed" if self.metrics["operations_failed"] == 0 else "completed_with_errors"
    }
    self.logger.info(f"Rapport final : {json.dumps(report, indent=2)}")
    return report

# --- Factory Function ---
def create_agent(config: Dict[str, Any]) -> "AgentAssistant99RefactoringHelper":
    """Factory pour créer une instance de l'agent assistant."""
    project_root = config.get("project_root")
    if not project_root:
    raise ValueError("La configuration doit contenir 'project_root'.")
    return AgentAssistant99RefactoringHelper(project_root=Path(project_root))


def run_refactoring_task(agent: AgentAssistant99RefactoringHelper, old_import: str, new_import: str, old_call: str, new_call: str):
    """Exécute une tâche de refactoring complète: imports et appels de méthode."""
    
    agent.logger.info("="*50)
    agent.logger.info("ÉTAPE 1: Remplacement des imports")
    agent.logger.info("="*50)

    target_files_import = agent.find_files_with_pattern(
    pattern=old_import,
    search_path="."
    )
    if target_files_import:
    agent.mass_replace_in_files(
        files=target_files_import,
        old_text=old_import,
        new_text=new_import
    )
    else:
    agent.logger.info("Aucun fichier trouvé avec l'ancienne importation. Passage à l'étape suivante.")

    agent.logger.info("="*50)
    agent.logger.info("ÉTAPE 2: Remplacement des appels de méthode")
    agent.logger.info("="*50)

    target_files_call = agent.find_files_with_pattern(
    pattern=old_call,
    search_path="."
    )
    if target_files_call:
    agent.mass_replace_in_files(
        files=target_files_call,
        old_text=old_call,
        new_text=new_call
    )
    else:
    agent.logger.info("Aucun fichier trouvé avec l'ancien appel de méthode.")


# --- Exemple d'utilisation ---
if __name__ == '__main__':
    print("Démonstration de l'Agent Assistant de Refactoring")

    project_root_path = Path(__file__).resolve().parents[2]
    print(f"Racine du projet détectée : {project_root_path}")

    agent_config = {"project_root": project_root_path}
    helper_agent = create_agent(agent_config)

    # Tâche 1 : Remplacer l'ancien LoggingManager
    run_refactoring_task(
    agent=helper_agent,
    old_import="from logging_manager_optimized import LoggingManager",
    new_import="from core import logging_manager",
    old_call="LoggingManager().get_logger",
    new_call="logging_manager.get_logger"
    )
    
    # Valider avec la suite de tests principale
    helper_agent.logger.info("="*50)
    helper_agent.logger.info("VALIDATION: Exécution de la suite de tests principale")
    helper_agent.logger.info("="*50)
    helper_agent.run_script("tests/logging/test_production_ready.py")

    # Générer le rapport final
    final_report = helper_agent.get_final_report()
    
    report_path = Path(__file__).parent / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(final_report, f, indent=2)
        
    print(f"\nOpération terminée. Rapport de refactoring généré : {report_path}") 