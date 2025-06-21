#!/usr/bin/env python3
"""
Script d'organisation automatique des fichiers
Nettoie le désordre créé par Cursor
"""

import os
import shutil
from pathlib import Path

def organiser_fichiers():
    """Organise tous les fichiers selon leur type"""
    
    print("🗂️  ORGANISATION AUTOMATIQUE DES FICHIERS")
    print("=" * 50)
    
    # Répertoire de base
    base_dir = Path(".")
    archive_dir = base_dir / "archive_organisation"
    
    # Règles d'organisation
    regles = {
        "tests": [
            "test_*.py",
            "test_*.json"
        ],
        "rapports": [
            "*report*.md",
            "*RAPPORT*.md",
            "migration_report_*.md"
        ],
        "config": [
            "*config*.py",
            "*CONFIG*.json"
        ],
        "migration": [
            "migrate_*.py",
            "*MIGRATION*.md"
        ],
        "planning": [
            "PLAN_*.md",
            "*PLAN*.md",
            "ACTION*.md",
            "*PROMPT*.md"
        ],
        "documentation": [
            "DOCUMENTATION_*.md",
            "*OPTIMISATION*.md",
            "*SECURITE*.md",
            "ANALYSE_*.md",
            "CATALOGUE_*.md",
            "LISTE_*.md",
            "CONTEXTE_*.md"
        ],
        "backups": [
            "*.backup*",
            "*backup*.py"
        ],
        "core_deprecated": [
            "agent_coordinateur_integrated.py",
            "orchestrateur_*.py",
            "template_manager_*.py",
            "integration_agent_*.py",
            "fix_*.py",
            "*ROLLBACK*.md",
            "*CONFIRMATION*.md",
            "GOLDEN_SOURCE*.md",
            "SCRIPTS_*.md"
        ]
    }
    
    # Compteurs
    moved_files = 0
    errors = 0
    
    # Parcourir tous les fichiers
    for fichier in base_dir.glob("*.*"):
        if fichier.is_file() and fichier.name not in ["organiser_fichiers.py", "logging_manager_optimized.py"]:
            
            # Déterminer la catégorie
            categorie_trouvee = None
            for categorie, patterns in regles.items():
                for pattern in patterns:
                    if fichier.match(pattern):
                        categorie_trouvee = categorie
                        break
                if categorie_trouvee:
                    break
            
            # Déplacer le fichier
            if categorie_trouvee:
                try:
                    destination = archive_dir / categorie_trouvee / fichier.name
                    shutil.move(str(fichier), str(destination))
                    print(f"✅ {fichier.name} → {categorie_trouvee}/")
                    moved_files += 1
                except Exception as e:
                    print(f"❌ Erreur {fichier.name}: {e}")
                    errors += 1
    
    print(f"\n📊 RÉSULTATS:")
    print(f"✅ Fichiers déplacés: {moved_files}")
    print(f"❌ Erreurs: {errors}")
    
    # Créer un index des fichiers organisés
    creer_index(archive_dir)

def creer_index(archive_dir):
    """Crée un index des fichiers organisés"""
    
    index_content = """# 📂 INDEX DES FICHIERS ORGANISÉS
*Créé automatiquement par organiser_fichiers.py*

## 📋 Structure d'organisation

"""
    
    for subdir in sorted(archive_dir.iterdir()):
        if subdir.is_dir():
            files = list(subdir.glob("*.*"))
            if files:
                index_content += f"### 📁 {subdir.name}/ ({len(files)} fichiers)\n"
                for file in sorted(files):
                    index_content += f"- `{file.name}`\n"
                index_content += "\n"
    
    index_content += """## 🎯 Fichiers principaux conservés
- `logging_manager_optimized.py` - **GOLDEN SOURCE principale**
- `nextgeneration_golden_source/` - **Sources de référence**
- `config/` - **Configuration système**
- `logs/` - **Logs d'exécution**
- `reports_equipe_agents/` - **Rapports agents actifs**

## 🚨 Action recommandée
En fin de session, vous pouvez supprimer `archive_organisation/` pour nettoyer.
"""
    
    with open(archive_dir / "INDEX_ORGANISATION.md", "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print(f"📄 Index créé: {archive_dir}/INDEX_ORGANISATION.md")

if __name__ == "__main__":
    organiser_fichiers() 