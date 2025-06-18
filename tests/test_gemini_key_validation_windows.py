#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Validation des Cls API Gemini - Version Windows
Compatible avec l'encodage Windows (cp1252)
"""

import os
import sys
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime

# Chargement du fichier .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Si python-dotenv n'est pas install, on essaie de charger manuellement
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

# Configuration pour Windows
if sys.platform.startswith('win'):
    # Forcer l'encodage UTF-8 pour la sortie console
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def test_google_genai_import() -> Tuple[bool, str]:
    """Test d'importation de google.generativeai."""
    try:
        import google.generativeai as genai
        return True, "Module google.generativeai disponible"
    except ImportError as e:
        return False, f"Module manquant: {str(e)}"

def get_api_keys() -> Dict[str, Optional[str]]:
    """Rcupre les cls API depuis les variables d'environnement."""
    keys = {
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY')
    }
    return keys

def test_gemini_connection(api_key: str) -> Tuple[bool, str, List[str]]:
    """Test de connexion avec une cl API Gemini."""
    try:
        import google.generativeai as genai
        
        # Configuration de la cl API
        genai.configure(api_key=api_key)
        
        # Test de liste des modles
        models = list(genai.list_models())
        model_names = [model.name for model in models]
        
        if models:
            return True, f"{len(models)} modeles Gemini disponibles", model_names
        else:
            return False, "Aucun modele disponible", []
            
    except Exception as e:
        return False, f"Erreur de connexion: {str(e)}", []

def test_gemini_generation(api_key: str) -> Tuple[bool, str]:
    """Test de gnration de contenu avec Gemini."""
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        
        # Test avec le modle le plus rapide
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test simple
        response = model.generate_content("Dis bonjour en franais")
        
        if response.text:
            return True, f"Generation reussie: {response.text[:50]}..."
        else:
            return False, "Reponse vide"
            
    except Exception as e:
        return False, f"Erreur de generation: {str(e)}"

def validate_environment() -> Dict[str, bool]:
    """Valide l'environnement complet."""
    validation = {}
    
    # Test Python
    validation['python_version'] = sys.version_info >= (3, 8)
    
    # Test des variables d'environnement
    keys = get_api_keys()
    validation['has_google_key'] = bool(keys['GOOGLE_API_KEY'])
    validation['has_gemini_key'] = bool(keys['GEMINI_API_KEY'])
    validation['has_any_key'] = validation['has_google_key'] or validation['has_gemini_key']
    
    # Test d'importation
    import_ok, _ = test_google_genai_import()
    validation['google_genai_available'] = import_ok
    
    return validation

def generate_detailed_report(results: Dict) -> str:
    """Gnre un rapport dtaill des tests."""
    report = []
    report.append("=" * 60)
    report.append("RAPPORT DETAILLE DE VALIDATION GEMINI")
    report.append("=" * 60)
    report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Environnement
    report.append("ENVIRONNEMENT:")
    validation = results.get('validation', {})
    report.append(f"  Python >= 3.8: {'OK' if validation.get('python_version') else 'ECHEC'}")
    report.append(f"  google.generativeai: {'OK' if validation.get('google_genai_available') else 'ECHEC'}")
    report.append("")
    
    # Cls API
    report.append("CLES API:")
    report.append(f"  GOOGLE_API_KEY: {'PRESENTE' if validation.get('has_google_key') else 'MANQUANTE'}")
    report.append(f"  GEMINI_API_KEY: {'PRESENTE' if validation.get('has_gemini_key') else 'MANQUANTE'}")
    report.append("")
    
    # Tests de connexion
    report.append("TESTS DE CONNEXION:")
    for key_name, test_result in results.get('connection_tests', {}).items():
        status = "REUSSI" if test_result['success'] else "ECHEC"
        report.append(f"  {key_name}: {status}")
        if test_result['success']:
            report.append(f"    Modeles: {test_result['model_count']}")
        else:
            report.append(f"    Erreur: {test_result['message']}")
    report.append("")
    
    # Tests de gnration
    report.append("TESTS DE GENERATION:")
    for key_name, test_result in results.get('generation_tests', {}).items():
        status = "REUSSI" if test_result['success'] else "ECHEC"
        report.append(f"  {key_name}: {status}")
        if not test_result['success']:
            report.append(f"    Erreur: {test_result['message']}")
    report.append("")
    
    # Recommandations
    report.append("RECOMMANDATIONS:")
    if not validation.get('google_genai_available'):
        report.append("  - Installer google-generativeai: pip install google-generativeai")
    
    if not validation.get('has_any_key'):
        report.append("  - Configurer au moins une cle API dans .env")
        report.append("  - GOOGLE_API_KEY=votre-cle-google")
        report.append("  - GEMINI_API_KEY=votre-cle-gemini")
    
    working_keys = [k for k, v in results.get('connection_tests', {}).items() if v['success']]
    if working_keys:
        report.append(f"  - Utiliser la cle fonctionnelle: {working_keys[0]}")
        report.append("  - Integrer dans l'orchestrateur")
    
    report.append("")
    report.append("=" * 60)
    
    return "\n".join(report)

def main() -> int:
    """Fonction principale de validation."""
    print("VALIDATION DES CLES API GEMINI")
    print("=" * 40)
    
    # Validation de l'environnement
    print("1. Validation de l'environnement...")
    validation = validate_environment()
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'validation': validation,
        'connection_tests': {},
        'generation_tests': {}
    }
    
    # Test d'importation
    import_ok, import_msg = test_google_genai_import()
    print(f"   google.generativeai: {'OK' if import_ok else 'ECHEC'}")
    if not import_ok:
        print(f"   Erreur: {import_msg}")
        print("\nInstaller avec: pip install google-generativeai")
        return 1
    
    # Rcupration des cls
    print("\n2. Verification des cles API...")
    keys = get_api_keys()
    
    available_keys = {}
    for key_name, key_value in keys.items():
        if key_value:
            available_keys[key_name] = key_value
            print(f"   {key_name}: PRESENTE")
        else:
            print(f"   {key_name}: MANQUANTE")
    
    if not available_keys:
        print("\nAucune cle API trouvee!")
        print("Configurer dans .env:")
        print("GOOGLE_API_KEY=votre-cle-google")
        print("GEMINI_API_KEY=votre-cle-gemini")
        return 1
    
    # Tests de connexion
    print("\n3. Tests de connexion...")
    working_keys = []
    
    for key_name, key_value in available_keys.items():
        print(f"   Test {key_name}...")
        success, message, models = test_gemini_connection(key_value)
        
        results['connection_tests'][key_name] = {
            'success': success,
            'message': message,
            'model_count': len(models) if success else 0,
            'models': models if success else []
        }
        
        if success:
            working_keys.append(key_name)
            print(f"      REUSSI - {message}")
        else:
            print(f"      ECHEC - {message}")
    
    if not working_keys:
        print("\nAucune cle fonctionnelle!")
        return 1
    
    # Tests de gnration
    print("\n4. Tests de generation...")
    for key_name in working_keys:
        key_value = available_keys[key_name]
        print(f"   Test generation {key_name}...")
        
        success, message = test_gemini_generation(key_value)
        
        results['generation_tests'][key_name] = {
            'success': success,
            'message': message
        }
        
        if success:
            print(f"      REUSSI - {message}")
        else:
            print(f"      ECHEC - {message}")
    
    # Rsultats finaux
    print("\n" + "=" * 40)
    if working_keys:
        print("RESULTAT: Au moins une cle Gemini fonctionne!")
        print(f"Cles fonctionnelles: {', '.join(working_keys)}")
        
        # Comptage des modles
        total_models = sum(
            results['connection_tests'][key]['model_count'] 
            for key in working_keys
        )
        print(f"Modeles disponibles: {total_models}")
        
        print("\nProchaines etapes:")
        print("1. Consulter: GUIDE_FOURNISSEURS_MODELES_ORCHESTRATEUR.md")
        print("2. Experimenter: python test_gemini_rapide.py")
        print("3. Integrer dans l'orchestrateur")
        
        # Sauvegarde du rapport
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"gemini_validation_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\nRapport sauvegarde: {report_file}")
        
        # Rapport dtaill
        detailed_report = generate_detailed_report(results)
        report_txt_file = f"gemini_validation_report_{timestamp}.txt"
        
        with open(report_txt_file, 'w', encoding='utf-8') as f:
            f.write(detailed_report)
        
        print(f"Rapport detaille: {report_txt_file}")
        
        return 0
    else:
        print("RESULTAT: Aucune cle Gemini fonctionnelle")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nInterrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        sys.exit(1) 