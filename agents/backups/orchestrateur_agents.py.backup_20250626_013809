import os
import shutil
from pathlib import Path
import sys

AGENTS_DIR = Path('agents')
BACKUP_DIR = Path('backups/agents')
SUIVI_MD = Path('agents/WORKFLOW_SUIVI_AGENTS.md')
SYNTHESE_MD = Path('agents/SYNTHESE_SUIVI_AGENTS.md')

# 1. Lister tous les agents Python du dossier agents/
def list_agents():
    return [f for f in AGENTS_DIR.glob('*.py') if f.is_file()]

# 2. Découper la liste en 3 lots équilibrés
def assign_agents(agents, n_ia=3):
    lots = [[] for _ in range(n_ia)]
    for i, agent in enumerate(agents):
        lots[i % n_ia].append(agent)
    return lots

# 3. Fonction pour renseigner le tableau de suivi markdown
def update_suivi_md(agent, tache, ia, statut, backup_path='', rapport_path='', commentaires='', validation='⬜'):
    # Charge le markdown existant
    if SUIVI_MD.exists():
        lines = SUIVI_MD.read_text(encoding='utf-8').splitlines()
    else:
        lines = []
    # Cherche la ligne de l'agent
    idx = None
    for i, line in enumerate(lines):
        if line.startswith(f'| {agent} '):
            idx = i
            break
    # Construit la nouvelle ligne
    new_line = f'| {agent} | {tache} | {ia} | {statut} | {backup_path} | {rapport_path} | {commentaires} | {validation} |'
    if idx is not None:
        lines[idx] = new_line
    else:
        # Ajoute après l'en-tête
        for i, line in enumerate(lines):
            if line.startswith('|-------'):
                lines.insert(i+1, new_line)
                break
    # Sauvegarde
    SUIVI_MD.write_text('\n'.join(lines), encoding='utf-8')

# 4. Préparer la structure pour l'appel aux IA (à compléter)
def traiter_lot(lot, ia_num):
    for agent_path in lot:
        # Exemple : renseigner le suivi pour chaque agent au début
        update_suivi_md(
            agent=agent_path.name,
            tache='À définir',
            ia=f'IA {ia_num}',
            statut='À faire',
            backup_path=f'[backup]({BACKUP_DIR / agent_path.name})',
            rapport_path='',
            commentaires='',
            validation='⬜'
        )
        # TODO : Appeler la logique de l'IA correspondante
        # TODO : Gérer backup, modif, test, rapport, validation, commit

# 5. Synthèse automatique du tableau de suivi
def synthese_suivi():
    if not SUIVI_MD.exists():
        print("Aucun tableau de suivi trouvé.")
        return
    lines = SUIVI_MD.read_text(encoding='utf-8').splitlines()
    data = []
    for line in lines:
        if line.startswith('|') and not line.startswith('|---'):
            parts = [p.strip() for p in line.strip('|').split('|')]
            if len(parts) >= 8 and parts[0] != 'Agent':
                data.append({
                    'agent': parts[0],
                    'tache': parts[1],
                    'ia': parts[2],
                    'statut': parts[3],
                    'backup': parts[4],
                    'rapport': parts[5],
                    'commentaires': parts[6],
                    'validation': parts[7],
                })
    # Synthèse par IA
    synth_ia = {}
    for row in data:
        ia = row['ia']
        synth_ia.setdefault(ia, {'total': 0, 'statuts': {}})
        synth_ia[ia]['total'] += 1
        synth_ia[ia]['statuts'][row['statut']] = synth_ia[ia]['statuts'].get(row['statut'], 0) + 1
    # Synthèse par tâche
    synth_tache = {}
    for row in data:
        tache = row['tache']
        synth_tache.setdefault(tache, 0)
        synth_tache[tache] += 1
    # Synthèse par statut
    synth_statut = {}
    for row in data:
        statut = row['statut']
        synth_statut.setdefault(statut, 0)
        synth_statut[statut] += 1
    # Affichage
    print("\n--- Synthèse par IA ---")
    for ia, d in synth_ia.items():
        print(f"{ia} : {d['total']} agents")
        for s, n in d['statuts'].items():
            print(f"  - {s} : {n}")
    print("\n--- Synthèse par type de tâche ---")
    for t, n in synth_tache.items():
        print(f"{t} : {n}")
    print("\n--- Synthèse par statut ---")
    for s, n in synth_statut.items():
        print(f"{s} : {n}")
    # Optionnel : sauvegarde dans un fichier markdown
    md = ["# SYNTHESE SUIVI AGENTS\n"]
    md.append("## Par IA\n")
    for ia, d in synth_ia.items():
        md.append(f"- {ia} : {d['total']} agents")
        for s, n in d['statuts'].items():
            md.append(f"    - {s} : {n}")
    md.append("\n## Par type de tâche\n")
    for t, n in synth_tache.items():
        md.append(f"- {t} : {n}")
    md.append("\n## Par statut\n")
    for s, n in synth_statut.items():
        md.append(f"- {s} : {n}")
    SYNTHESE_MD.write_text('\n'.join(md), encoding='utf-8')
    print(f"\nSynthèse sauvegardée dans {SYNTHESE_MD}")

if __name__ == '__main__':
    if '--synthese' in sys.argv:
        synthese_suivi()
    else:
        agents = list_agents()
        lots = assign_agents(agents)
        for i, lot in enumerate(lots):
            traiter_lot(lot, ia_num=i+1)
        print('Tableau de suivi initialisé et lots attribués.') 