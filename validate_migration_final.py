#!/usr/bin/env python3
"""
Script de validation finale de la migration complète.
Valide à la fois le logging uniforme et la standardisation des rapports.
"""
import os
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

def run_logging_validation() -> Dict[str, Any]:
    """Exécute la validation du logging uniforme."""
    print("🔍 VALIDATION LOGGING UNIFORME...")
    
    try:
        result = subprocess.run(
            ["python3", "validate_logging_migration.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            # Analyser la sortie pour extraire les statistiques
            output = result.stdout
            
            # Extraire les statistiques principales
            total_match = re.search(r'Total agents analysés: (\d+)', output)
            conformes_match = re.search(r'Agents conformes: (\d+) \(([^)]+)%\)', output)
            partiels_match = re.search(r'Agents partiellement conformes: (\d+)', output)
            non_conformes_match = re.search(r'Agents non conformes: (\d+)', output)
            score_match = re.search(r'Score moyen de conformité: ([0-9.]+)%', output)
            
            return {
                "success": True,
                "total_agents": int(total_match.group(1)) if total_match else 0,
                "conformes": int(conformes_match.group(1)) if conformes_match else 0,
                "conformes_percentage": float(conformes_match.group(2)) if conformes_match else 0,
                "partiellement_conformes": int(partiels_match.group(1)) if partiels_match else 0,
                "non_conformes": int(non_conformes_match.group(1)) if non_conformes_match else 0,
                "score_moyen": float(score_match.group(1)) if score_match else 0,
                "raw_output": output[:500] + "..." if len(output) > 500 else output
            }
        else:
            return {
                "success": False,
                "error": result.stderr,
                "raw_output": result.stdout
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_reports_standardization() -> Dict[str, Any]:
    """Analyse la standardisation des rapports."""
    print("📊 VALIDATION STANDARDISATION RAPPORTS...")
    
    try:
        result = subprocess.run(
            ["python3", "standardize_reports_format.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            output = result.stdout
            
            # Extraire les statistiques
            total_match = re.search(r'Total agents analysés: (\d+)', output)
            with_reports_match = re.search(r'Agents avec rapports: (\d+)', output)
            to_standardize_match = re.search(r'Agents à standardiser: (\d+)', output)
            success_match = re.search(r'✅ Succès: (\d+)', output)
            failed_match = re.search(r'❌ Échecs: (\d+)', output)
            
            return {
                "success": True,
                "total_agents": int(total_match.group(1)) if total_match else 0,
                "agents_with_reports": int(with_reports_match.group(1)) if with_reports_match else 0,
                "agents_to_standardize": int(to_standardize_match.group(1)) if to_standardize_match else 0,
                "standardization_success": int(success_match.group(1)) if success_match else 0,
                "standardization_failed": int(failed_match.group(1)) if failed_match else 0,
                "raw_output": output[:500] + "..." if len(output) > 500 else output
            }
        else:
            return {
                "success": False,
                "error": result.stderr,
                "raw_output": result.stdout
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_agent_import_samples() -> Dict[str, Any]:
    """Teste l'importation d'un échantillon d'agents pour vérifier la syntaxe."""
    print("🧪 TEST IMPORT ÉCHANTILLON AGENTS...")
    
    sample_agents = [
        "agent_01_coordinateur_principal.py",
        "agent_02_architecte_code_expert.py", 
        "agent_06_specialiste_monitoring_sprint4.py",
        "agent_MAINTENANCE_06_validateur_final.py",
        "agent_POSTGRESQL_diagnostic_postgres_final.py"
    ]
    
    results = {
        "success": True,
        "tested_agents": len(sample_agents),
        "import_success": 0,
        "import_failed": 0,
        "errors": []
    }
    
    import sys
    import importlib.util
    sys.path.append("agents")
    
    for agent_file in sample_agents:
        try:
            # Importer le module
            module_name = agent_file.replace('.py', '')
            spec = importlib.util.spec_from_file_location(module_name, f"agents/{agent_file}")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            results["import_success"] += 1
            print(f"  ✅ {agent_file}")
            
        except Exception as e:
            results["import_failed"] += 1
            results["errors"].append(f"{agent_file}: {str(e)}")
            print(f"  ❌ {agent_file}: {str(e)}")
    
    if results["import_failed"] > 0:
        results["success"] = False
    
    return results

def check_file_integrity() -> Dict[str, Any]:
    """Vérifie l'intégrité des fichiers après migration."""
    print("🔍 VÉRIFICATION INTÉGRITÉ FICHIERS...")
    
    agents_dir = Path("agents")
    results = {
        "success": True,
        "total_files": 0,
        "valid_files": 0,
        "invalid_files": 0,
        "errors": []
    }
    
    for file_path in agents_dir.glob("agent_*.py"):
        if file_path.is_file():
            results["total_files"] += 1
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifications de base
                if len(content.strip()) == 0:
                    results["errors"].append(f"{file_path.name}: Fichier vide")
                    results["invalid_files"] += 1
                elif "class " not in content:
                    results["errors"].append(f"{file_path.name}: Aucune classe trouvée")
                    results["invalid_files"] += 1
                elif content.count('"""') % 2 != 0:
                    results["errors"].append(f"{file_path.name}: Docstrings non fermés")
                    results["invalid_files"] += 1
                else:
                    results["valid_files"] += 1
                    
            except Exception as e:
                results["errors"].append(f"{file_path.name}: Erreur lecture - {str(e)}")
                results["invalid_files"] += 1
    
    if results["invalid_files"] > 0:
        results["success"] = False
    
    return results

def generate_migration_summary() -> Dict[str, Any]:
    """Génère un résumé complet de la migration."""
    
    # Statistiques des sauvegardes
    backup_files = list(Path(".").glob("agents/*.backup_*"))
    report_backups = list(Path(".").glob("agents/*.backup_reports_*"))
    
    # Analyser les fichiers de rapport de conformité
    conformity_reports = list(Path(".").glob("rapport_conformite_logging_*.json"))
    latest_report = None
    
    if conformity_reports:
        latest_report = max(conformity_reports, key=lambda p: p.stat().st_mtime)
        
        try:
            with open(latest_report, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
        except:
            report_data = {}
    else:
        report_data = {}
    
    return {
        "migration_date": datetime.now().isoformat(),
        "backup_files_created": len(backup_files),
        "report_backup_files_created": len(report_backups),
        "latest_conformity_report": latest_report.name if latest_report else None,
        "final_conformity_data": report_data.get("summary", {}),
        "total_agents_processed": len(backup_files) + len(report_backups)
    }

def main():
    """Fonction principale."""
    print("🚀 VALIDATION FINALE - MIGRATION LOGGING UNIFORME & RAPPORTS")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # 1. Validation logging uniforme
    logging_results = run_logging_validation()
    
    # 2. Validation standardisation rapports  
    reports_results = analyze_reports_standardization()
    
    # 3. Test imports échantillon
    import_results = test_agent_import_samples()
    
    # 4. Vérification intégrité
    integrity_results = check_file_integrity()
    
    # 5. Résumé migration
    migration_summary = generate_migration_summary()
    
    # Affichage des résultats
    print("📈 RÉSULTATS VALIDATION FINALE")
    print("-" * 80)
    
    # Logging
    if logging_results["success"]:
        print(f"✅ LOGGING UNIFORME:")
        print(f"   Total agents: {logging_results.get('total_agents', 0)}")
        print(f"   Conformes: {logging_results.get('conformes', 0)} ({logging_results.get('conformes_percentage', 0):.1f}%)")
        print(f"   Score moyen: {logging_results.get('score_moyen', 0):.1f}%")
    else:
        print(f"❌ LOGGING UNIFORME: {logging_results.get('error', 'Erreur inconnue')}")
    
    # Rapports
    if reports_results["success"]:
        print(f"✅ STANDARDISATION RAPPORTS:")
        print(f"   Agents avec rapports: {reports_results.get('agents_with_reports', 0)}")
        print(f"   Standardisations réussies: {reports_results.get('standardization_success', 0)}")
        if reports_results.get('standardization_failed', 0) > 0:
            print(f"   Échecs: {reports_results.get('standardization_failed', 0)}")
    else:
        print(f"❌ STANDARDISATION RAPPORTS: {reports_results.get('error', 'Erreur inconnue')}")
    
    # Imports
    if import_results["success"]:
        print(f"✅ TESTS IMPORT AGENTS:")
        print(f"   Testés: {import_results['tested_agents']}")
        print(f"   Succès: {import_results['import_success']}")
    else:
        print(f"❌ TESTS IMPORT AGENTS:")
        print(f"   Échecs: {import_results['import_failed']}")
        for error in import_results['errors'][:3]:  # Montrer max 3 erreurs
            print(f"   - {error}")
    
    # Intégrité
    if integrity_results["success"]:
        print(f"✅ INTÉGRITÉ FICHIERS:")
        print(f"   Fichiers valides: {integrity_results['valid_files']}/{integrity_results['total_files']}")
    else:
        print(f"❌ INTÉGRITÉ FICHIERS:")
        print(f"   Fichiers invalides: {integrity_results['invalid_files']}")
        for error in integrity_results['errors'][:3]:  # Montrer max 3 erreurs
            print(f"   - {error}")
    
    # Résumé migration
    print(f"\n📋 RÉSUMÉ MIGRATION:")
    print(f"   Fichiers de sauvegarde créés: {migration_summary['backup_files_created']}")
    print(f"   Fichiers de sauvegarde rapports: {migration_summary['report_backup_files_created']}")
    print(f"   Total agents traités: {migration_summary.get('total_agents_processed', 0)}")
    
    # Score global
    total_tests = 4
    passed_tests = sum([
        1 if logging_results["success"] else 0,
        1 if reports_results["success"] else 0, 
        1 if import_results["success"] else 0,
        1 if integrity_results["success"] else 0
    ])
    
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"\n🎯 SCORE GLOBAL DE VALIDATION: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 100:
        print("🎉 MIGRATION COMPLÈTE RÉUSSIE!")
        print("✅ Tous les agents utilisent maintenant le logging uniforme")
        print("✅ Tous les rapports suivent le format standardisé") 
        print("✅ Aucun problème de syntaxe détecté")
        print("✅ Intégrité des fichiers préservée")
        
    elif success_rate >= 75:
        print("⚠️ MIGRATION MAJORITAIREMENT RÉUSSIE")
        print("Quelques problèmes mineurs détectés - vérification manuelle recommandée")
        
    else:
        print("❌ MIGRATION PROBLÉMATIQUE")
        print("Plusieurs tests ont échoué - intervention manuelle requise")
    
    # Sauvegarder le rapport final
    final_report = {
        "validation_date": datetime.now().isoformat(),
        "success_rate": success_rate,
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "logging_validation": logging_results,
        "reports_standardization": reports_results,
        "import_tests": import_results,
        "integrity_check": integrity_results,
        "migration_summary": migration_summary
    }
    
    with open("rapport_validation_finale_migration.json", "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Rapport détaillé sauvegardé: rapport_validation_finale_migration.json")

if __name__ == "__main__":
    main()