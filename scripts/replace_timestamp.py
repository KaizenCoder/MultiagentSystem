# scripts/replace_timestamp.py
import sys
import datetime
from pathlib import Path

def replace_timestamp_in_file(file_path_str: str):
    """
    Remplace toutes les occurrences de 'YYYY-MM-DD HH:MM:SS' 
    par la date et l'heure actuelles dans le fichier spécifié.
    """
    file_path = Path(file_path_str)
    placeholder = "YYYY-MM-DD HH:MM:SS"
    
    if not file_path.exists() or not file_path.is_file():
        print(f"Erreur : Le fichier '{file_path_str}' n'existe pas ou n'est pas un fichier valide.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if placeholder not in content:
            print(f"Information : Le placeholder '{placeholder}' n'a pas été trouvé dans '{file_path_str}'. Aucune modification effectuée.")
            return

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_content = content.replace(placeholder, now_str)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Succès : Les placeholders dans '{file_path_str}' ont été remplacés par '{now_str}'.")

    except Exception as e:
        print(f"Erreur lors du traitement du fichier '{file_path_str}': {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python replace_timestamp.py <chemin_vers_le_fichier_markdown>")
        sys.exit(1)
    
    target_file = sys.argv[1]
    replace_timestamp_in_file(target_file) 