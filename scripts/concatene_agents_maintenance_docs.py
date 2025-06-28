import os
from pathlib import Path

# Liste des fichiers à concaténer (relatifs à la racine du projet)
FILES = [
    "agents/agent_MAINTENANCE_00_chef_equipe_coordinateur.py",
    "agents/agent_MAINTENANCE_01_analyseur_structure.py",
    "agents/agent_MAINTENANCE_02_evaluateur_utilite.py",
    "agents/agent_MAINTENANCE_03_adaptateur_code.py",
    "agents/agent_MAINTENANCE_04_testeur_anti_faux_agents.py",
    "agents/agent_MAINTENANCE_05_documenteur_peer_reviewer.py",
    "agents/agent_MAINTENANCE_06_correcteur_logique_metier.py",
    "agents/agent_MAINTENANCE_06_validateur_final.py",
    "agents/agent_MAINTENANCE_07_gestionnaire_dependances.py",
    "agents/agent_MAINTENANCE_08_analyseur_performance.py",
    "agents/agent_MAINTENANCE_09_analyseur_securite.py",
    "agents/agent_MAINTENANCE_10_auditeur_qualite_normes.py",
    "agents/agent_MAINTENANCE_11_harmonisateur_style.py",
    "agents/agent_MAINTENANCE_12_correcteur_semantique.py",
    "SOP_MAINTENANCE_TEAM.md",
    "run_maintenance.py",
    "PROCEDURE_EQUIPE_MAINTENANCE.md",
]

OUTPUT_MD = "AGENTS_MAINTENANCE_TEAM_FULL.md"


def main():
    with open(OUTPUT_MD, "w", encoding="utf-8") as out:
        out.write(f"# Documentation complète de l'équipe de maintenance\n\n")
        for file_path in FILES:
            path = Path(file_path)
            if not path.exists():
                out.write(f"\n---\n\n## {file_path}\n\n**Fichier introuvable.**\n")
                continue
            out.write(f"\n---\n\n## {file_path}\n\n")
            if file_path.endswith('.py'):
                out.write(f"```python\n")
            elif file_path.endswith('.md'):
                out.write(f"<!-- Markdown natif -->\n")
            with open(file_path, "r", encoding="utf-8") as f:
                out.write(f.read())
            if file_path.endswith('.py'):
                out.write(f"\n```")
            out.write("\n")
    print(f"Fichier concaténé généré : {OUTPUT_MD}")

if __name__ == "__main__":
    main() 