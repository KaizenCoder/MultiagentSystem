#!/usr/bin/env python3
"""
Script qui analyse la structure d'un répertoire recursivement et crée un fichier .txt
où les fichiers sont regroupés par type (extension).
"""

import os
import sys
from collections import defaultdict
from datetime import datetime

def analyze_directory(root_path):
    """
    Analyse recursivement un répertoire et regroupe les fichiers par extension.
    
    Args:
        root_path (str): Chemin du répertoire à analyser
        
    Returns:
        dict: Dictionnaire où les clés sont les extensions et les valeurs sont les listes de chemins de fichiers
    """
    if not os.path.isdir(root_path):
        print(f"Erreur: {root_path} n'est pas un répertoire valide.")
        sys.exit(1)
    
    files_by_type = defaultdict(list)
    
    # Parcourir récursivement le répertoire
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            # Obtenir le chemin complet du fichier
            full_path = os.path.join(dirpath, filename)
            
            # Extraire l'extension du fichier (en minuscules pour uniformiser)
            _, extension = os.path.splitext(filename)
            extension = extension.lower()
            
            if extension:
                # Si le fichier a une extension, l'ajouter sans le point initial
                files_by_type[extension[1:]].append(full_path)
            else:
                # Pour les fichiers sans extension
                files_by_type["sans_extension"].append(full_path)
    
    return files_by_type

def create_report(files_by_type, output_file, analyzed_dir):
    """
    Crée un fichier rapport contenant les fichiers regroupés par type.
    
    Args:
        files_by_type (dict): Dictionnaire des fichiers regroupés par extension
        output_file (str): Chemin du fichier de sortie
        analyzed_dir (str): Chemin du répertoire analysé
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Rapport d'analyse de répertoire\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Répertoire analysé: {os.path.abspath(analyzed_dir)}\n")
        f.write("-" * 80 + "\n\n")
        
        # Nombre total de types de fichiers
        f.write(f"Nombre total de types de fichiers: {len(files_by_type)}\n\n")
        
        # Trier les extensions par nombre de fichiers (ordre décroissant)
        sorted_types = sorted(files_by_type.items(), key=lambda x: len(x[1]), reverse=True)
        
        # Écrire les informations pour chaque type de fichier
        for extension, file_paths in sorted_types:
            f.write(f"Type: {extension}\n")
            f.write(f"Nombre de fichiers: {len(file_paths)}\n")
            f.write("-" * 40 + "\n")
            
            # Écrire le chemin de chaque fichier
            for file_path in sorted(file_paths):
                f.write(f"  {file_path}\n")
            
            f.write("\n")

def main():
    # Vérifier si un argument de ligne de commande est fourni
    if len(sys.argv) < 2:
        print("Usage: python analyze_directory.py <directory_path> [output_file]")
        print("Si output_file n'est pas spécifié, le résultat sera enregistré dans 'analyse_repertoire.txt'")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    
    # Définir le fichier de sortie
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = "analyse_repertoire.txt"
    
    print(f"Analyse du répertoire '{directory_path}'...")
    files_by_type = analyze_directory(directory_path)
    
    print(f"Création du rapport dans '{output_file}'...")
    create_report(files_by_type, output_file, directory_path)
    
    print(f"Analyse terminée. {sum(len(files) for files in files_by_type.values())} fichiers trouvés, "
          f"regroupés en {len(files_by_type)} types différents.")
    print(f"Rapport enregistré dans '{os.path.abspath(output_file)}'")

if __name__ == "__main__":
    main()




