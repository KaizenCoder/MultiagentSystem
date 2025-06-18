import os
import argparse

def get_project_tree(root_path, exclude_dirs, exclude_files):
    """Génère une arborescence de projet formatée."""
    tree_lines = ["."]
    for root, dirs, files in os.walk(root_path):
        # Exclure les répertoires spécifiés
        dirs[:] = [d for d in dirs if d not in exclude_dirs and os.path.join(root, d) not in exclude_dirs]
        
        level = root.replace(root_path, '').count(os.sep)
        indent = '│   ' * (level)
        
        for i, d in enumerate(sorted(dirs)):
            sub_indent = '└── ' if i == len(dirs) - 1 and not files else '├── '
            tree_lines.append(f"{indent}{sub_indent}{d}")
            
        for i, f in enumerate(sorted(files)):
            if f not in exclude_files:
                sub_indent = '└── ' if i == len(files) - 1 else '├── '
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

def main(template_file, output_file):
    """Fonction principale pour générer le document."""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Éléments à exclure
    exclude_dirs = ['.git', '__pycache__', 'node_modules', '.vscode', 'chroma_db']
    exclude_files = [
        '.DS_Store', 'PITCH_NEXTGENERATION.md', 'PITCH_NEXTGENERATION_FINAL.md',
        os.path.basename(__file__)
    ]
    
    # Lire le modèle de base
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Générer et insérer l'arborescence
    print("Génération de l'arborescence du projet...")
    project_tree = get_project_tree(root_dir, exclude_dirs, exclude_files)
    tree_placeholder = "L'arborescence complète du projet sera insérée ici"
    content = content.replace(tree_placeholder, f"```\n{project_tree}\n```")

    # Générer et insérer le contenu des fichiers
    print("Intégration du codebase...")
    codebase_content = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file in exclude_files:
                continue
            
            file_path = os.path.join(root, file)
            codebase_content.append(get_file_content_as_markdown(file_path, root_dir))

    codebase_placeholder = "(Le contenu des fichiers sera inséré ici)"
    content = content.replace(codebase_placeholder, "\n".join(codebase_content))

    # Écrire le fichier final
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"🎉 Document final généré avec succès : {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Générateur de document de présentation pour NextGeneration.")
    parser.add_argument(
        '--template', 
        default='PITCH_NEXTGENERATION.md', 
        help='Fichier modèle à utiliser.'
    )
    parser.add_argument(
        '--output', 
        default='PITCH_NEXTGENERATION_FINAL.md', 
        help='Fichier de sortie à générer.'
    )
    args = parser.parse_args()
    main(args.template, args.output) 