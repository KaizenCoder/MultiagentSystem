#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 AGENT GÉNÉRATEUR DE BUNDLE - NEXTGENERATION
Création d'un fichier de synthèse complet du code source.

Inspiré par SuperWhisper_V6 et adapté à l'écosystème NextGeneration.
"""

import os
import sys
import argparse
import logging
from pathlib import Path
import datetime

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Constantes ---
PROJECT_ROOT = Path(__file__).parent.parent.parent
TARGET_FILE_NAME = "CODE-SOURCE.md"
DEFAULT_OUTPUT_FILE = PROJECT_ROOT / TARGET_FILE_NAME

# Dossiers et fichiers à exclure
EXCLUDE_DIRS = {
    '.git', '__pycache__', 'node_modules', 'dist', 'build', 'logs', 
    'backups', 'chroma_db', '.vscode', '.idea', 'agent_factory_implementation'
}
EXCLUDE_FILES = {
    TARGET_FILE_NAME, 'CODE-SOURCE.md.backup', '.gitignore'
}
EXCLUDE_EXTENSIONS = {
    '.pyc', '.pyo', '.pyd', '.log', '.tmp', '.DS_Store', '.db', '.bak'
}

class CodeBundler:
    """Génère un bundle complet du code source du projet."""

    def __init__(self, start_path: Path, output_file: Path, dry_run: bool = False):
        self.start_path = start_path
        self.output_file = output_file
        self.dry_run = dry_run
        self.file_count = 0
        self.total_lines = 0

    def _should_exclude(self, path: Path) -> bool:
        """Vérifie si un fichier ou dossier doit être exclu."""
        if any(d in path.parts for d in EXCLUDE_DIRS):
            return True
        if path.name in EXCLUDE_FILES:
            return True
        if path.suffix in EXCLUDE_EXTENSIONS:
            return True
        return False

    def bundle_source_code(self):
        """Parcourt le projet et génère le fichier de synthèse."""
        logger.info(f"🚀 Démarrage de la génération du bundle de code source...")
        logger.info(f"Répertoire analysé : {self.start_path}")
        logger.info(f"Fichier de sortie : {self.output_file}")

        if self.dry_run:
            logger.info("🧪 MODE SIMULATION (DRY-RUN) ACTIVÉ. Aucune modification ne sera écrite.")

        content_parts = [self._generate_header()]

        for root, _, files in os.walk(self.start_path):
            root_path = Path(root)
            if self._should_exclude(root_path):
                continue

            for file_name in sorted(files):
                file_path = root_path / file_name
                if self._should_exclude(file_path):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()
                    
                    relative_path = file_path.relative_to(self.start_path)
                    
                    content_parts.append(f"\n---\n\n"
                                       f"## 📄 `{relative_path}`\n\n"
                                       f"```\n"
                                       f"{file_content}\n"
                                       f"```\n")
                    self.file_count += 1
                    self.total_lines += len(file_content.splitlines())
                    logger.debug(f"Inclusion du fichier : {relative_path}")

                except Exception as e:
                    logger.warning(f"⚠️ Impossible de lire le fichier {file_path}: {e}")

        final_content = "".join(content_parts)
        
        if not self.dry_run:
            self._write_output(final_content)
        
        self._log_summary()

    def _generate_header(self) -> str:
        """Génère l'en-tête du fichier de synthèse."""
        now = datetime.datetime.now()
        header = (f"# 📦 BUNDLE CODE SOURCE - NEXTGENERATION\n\n"
                  f"**Généré le** : {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
                  f"**Projet** : {self.start_path.name}\n"
                  f"**Total fichiers inclus** : [sera mis à jour]\n"
                  f"**Total lignes incluses** : [sera mis à jour]\n\n"
                  f"Ce document est une compilation automatisée de tous les fichiers sources pertinents du projet NextGeneration. "
                  f"Il est généré pour faciliter les revues de code, l'archivage et la transmission d'informations.\n")
        return header

    def _write_output(self, content: str):
        """Écrit le contenu final dans le fichier de sortie."""
        try:
            # Remplacer les placeholders dans l'en-tête
            content = content.replace("[sera mis à jour]", str(self.file_count), 1)
            content = content.replace("[sera mis à jour]", str(self.total_lines), 1)

            # Créer un backup si le fichier existe
            if self.output_file.exists():
                backup_path = self.output_file.with_suffix('.md.backup')
                self.output_file.rename(backup_path)
                logger.info(f"🛡️ Backup de l'ancien fichier créé : {backup_path}")

            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✅ Fichier de synthèse généré avec succès : {self.output_file}")
            logger.info(f"Taille du fichier : {os.path.getsize(self.output_file) / 1024:.2f} KB")

        except Exception as e:
            logger.error(f"❌ Erreur lors de l'écriture du fichier de sortie : {e}")

    def _log_summary(self):
        """Affiche un résumé de l'opération."""
        logger.info("\n--- RÉSUMÉ DE L'OPÉRATION ---\n")
        logger.info(f"📊 Nombre total de fichiers inclus : {self.file_count}")
        logger.info(f"📈 Nombre total de lignes de code : {self.total_lines}")
        logger.info("\n🎉 Opération terminée !")

def main():
    """Fonction principale pour exécuter le script depuis la ligne de commande."""
    parser = argparse.ArgumentParser(description="Générateur de Bundle de Code Source pour NextGeneration.")
    parser.add_argument(
        "--output",
        type=str,
        default=str(DEFAULT_OUTPUT_FILE),
        help=f"Chemin du fichier de sortie. Défaut : {DEFAULT_OUTPUT_FILE}"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Exécute le script en mode simulation sans écrire de fichier."
    )
    args = parser.parse_args()

    bundler = CodeBundler(
        start_path=PROJECT_ROOT,
        output_file=Path(args.output),
        dry_run=args.dry_run
    )
    bundler.bundle_source_code()

if __name__ == "__main__":
    main() 