import os
import argparse
import json
from typing import List, Dict

def get_project_tree(root_path, exclude_dirs, exclude_files, include_only=None):
    """Gnre une arborescence de projet formate."""
    tree_lines = ["."]
    for root, dirs, files in os.walk(root_path):
        # Filtrer selon include_only si spcifi
        if include_only:
            dirs[:] = [d for d in dirs if any(pattern in os.path.join(root, d) for pattern in include_only)]
        
        # Exclure les rpertoires spcifis
        dirs[:] = [d for d in dirs if d not in exclude_dirs and os.path.join(root, d) not in exclude_dirs]
        
        level = root.replace(root_path, '').count(os.sep)
        indent = '   ' * (level)
        
        for i, d in enumerate(sorted(dirs)):
            sub_indent = ' ' if i == len(dirs) - 1 and not files else ' '
            tree_lines.append(f"{indent}{sub_indent}{d}")
            
        for i, f in enumerate(sorted(files)):
            if f not in exclude_files:
                # Filtrer les fichiers selon include_only si spcifi
                if include_only and not any(pattern in os.path.join(root, f) for pattern in include_only):
                    continue
                sub_indent = ' ' if i == len(files) - 1 else ' '
                tree_lines.append(f"{indent}{sub_indent}{f}")
    return "\n".join(tree_lines)

def get_file_content_as_markdown(file_path, root_path):
    """Lit un fichier et le retourne dans un bloc de code markdown."""
    relative_path = os.path.relpath(file_path, root_path)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        lang = os.path.splitext(file_path)[1].lstrip('.')
        if not lang:
            lang = 'text'

        return f"""
<details>
<summary><code>{relative_path.replace(os.sep, '/')}</code></summary>

```{lang}
{content}
```
</details>
"""
    except Exception as e:
        return f"\n<details><summary><code>{relative_path.replace(os.sep, '/')}</code> (Erreur de lecture)</summary>\n\n```text\nImpossible de lire le fichier: {e}\n```\n\n</details>"

def should_include_file(file_path, include_patterns, root_path):
    """Vrifie si un fichier doit tre inclus selon les patterns."""
    if not include_patterns:
        return True
    
    relative_path = os.path.relpath(file_path, root_path)
    return any(pattern in relative_path for pattern in include_patterns)

def main(template_file, output_file, mode='selective', include_patterns=None, config_file=None):
    """Fonction principale pour gnrer le document."""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Charger la configuration si fournie
    if config_file and os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            include_patterns = config.get('include_patterns', include_patterns)
            mode = config.get('mode', mode)
    
    # lments  exclure par dfaut
    exclude_dirs = ['.git', '__pycache__', 'node_modules', '.vscode', 'chroma_db']
    exclude_files = [
        '.DS_Store', 'PITCH_NEXTGENERATION.md', 'PITCH_NEXTGENERATION_FINAL.md',
        os.path.basename(__file__)
    ]
    
    # Configuration selon le mode
    if mode == 'minimal':
        # Mode minimal : seulement les fichiers essentiels
        include_patterns = include_patterns or [
            'agent_factory_experts_team/',
            'coordinateur_equipe_experts.py',
            'expert_claude_architecture.py',
            'expert_chatgpt_robustesse.py',
            'README.md',
            'requirements.txt'
        ]
    elif mode == 'full':
        # Mode complet : tout le codebase
        include_patterns = None
    else:
        # Mode slectif : patterns personnaliss
        pass
    
    # Lire le modle de base
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Gnrer et insrer l'arborescence
    print(f"Gnration de l'arborescence du projet (mode: {mode})...")
    project_tree = get_project_tree(root_dir, exclude_dirs, exclude_files, include_patterns)
    tree_placeholder = "L'arborescence complte du projet sera insre ici"
    content = content.replace(tree_placeholder, f"```\n{project_tree}\n```")

    # Gnrer et insrer le contenu des fichiers
    print("Intgration du codebase...")
    codebase_content = []
    files_included = 0
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file in exclude_files:
                continue
            
            file_path = os.path.join(root, file)
            
            # Vrifier si le fichier doit tre inclus
            if not should_include_file(file_path, include_patterns, root_dir):
                continue
                
            codebase_content.append(get_file_content_as_markdown(file_path, root_dir))
            files_included += 1

    codebase_placeholder = "(Le contenu des fichiers sera insr ici)"
    content = content.replace(codebase_placeholder, "\n".join(codebase_content))

    # Ajouter les mtadonnes de gnration
    metadata = f"""
<!-- Mtadonnes de gnration -->
<!-- Mode: {mode} -->
<!-- Fichiers inclus: {files_included} -->
<!-- Patterns: {include_patterns if include_patterns else 'Tous les fichiers'} -->

"""
    content = metadata + content

    # crire le fichier final
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f" Document final gnr avec succs : {output_file}")
    print(f"[CHART] Mode: {mode} | Fichiers inclus: {files_included}")

def create_config_template():
    """Cre un template de configuration."""
    config_template = {
        "mode": "selective",
        "include_patterns": [
            "agent_factory_experts_team/",
            "coordinateur_equipe_experts.py",
            "expert_claude_architecture.py",
            "expert_chatgpt_robustesse.py",
            "README.md"
        ],
        "description": "Configuration pour gnration slective du pitch Agent Factory"
    }
    
    with open('pitch_config.json', 'w', encoding='utf-8') as f:
        json.dump(config_template, f, indent=2, ensure_ascii=False)
    print(" Template de configuration cr : pitch_config.json")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Gnrateur de document de prsentation pour NextGeneration.")
    parser.add_argument(
        '--template', 
        default='PITCH_NEXTGENERATION.md', 
        help='Fichier modle  utiliser.'
    )
    parser.add_argument(
        '--output', 
        default='PITCH_NEXTGENERATION_FINAL.md', 
        help='Fichier de sortie  gnrer.'
    )
    parser.add_argument(
        '--mode',
        choices=['minimal', 'selective', 'full'],
        default='selective',
        help='Mode de gnration : minimal (fichiers essentiels), selective (patterns personnaliss), full (tout le codebase)'
    )
    parser.add_argument(
        '--include',
        nargs='*',
        help='Patterns de fichiers/dossiers  inclure (mode selective)'
    )
    parser.add_argument(
        '--config',
        help='Fichier de configuration JSON'
    )
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='Crer un template de configuration'
    )
    
    args = parser.parse_args()
    
    if args.create_config:
        create_config_template()
    else:
        main(args.template, args.output, args.mode, args.include, args.config) 



