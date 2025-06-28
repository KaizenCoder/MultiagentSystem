#!/usr/bin/env python3
"""
Script de validation de la migration du logging uniforme.
Analyse tous les agents pour vérifier la conformité au système de logging centralisé.
"""
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

def analyze_agent_file(file_path: Path) -> Dict[str, Any]:
    """Analyse un fichier agent pour vérifier la conformité du logging."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {
            "file_name": file_path.name,
            "error": f"Erreur lecture fichier: {str(e)}",
            "status": "ERREUR"
        }
    
    results = {
        "file_name": file_path.name,
        "file_size": len(content),
        "logging_manager_import": False,
        "get_logger_call": False,
        "fallback_present": False,
        "metadata_present": False,
        "custom_config_present": False,
        "logger_name_pattern": False,
        "log_dir_pattern": False,
        "status": "NON_CONFORME",
        "score": 0
    }
    
    # Vérifier l'import du LoggingManager
    if re.search(r'from\s+core\.manager\s+import\s+LoggingManager', content):
        results["logging_manager_import"] = True
        results["score"] += 1
    
    # Vérifier l'appel à get_logger
    if re.search(r'logging_manager\.get_logger\(', content):
        results["get_logger_call"] = True
        results["score"] += 1
    
    # Vérifier la présence du fallback
    if re.search(r'except\s+ImportError.*self\.logger\s*=\s*logging\.getLogger', content, re.DOTALL):
        results["fallback_present"] = True
        results["score"] += 1
    
    # Vérifier la présence des métadonnées
    if re.search(r'"metadata":\s*{', content):
        results["metadata_present"] = True
        results["score"] += 1
    
    # Vérifier custom_config
    if re.search(r'custom_config\s*=\s*{', content):
        results["custom_config_present"] = True
        results["score"] += 1
    
    # Vérifier pattern logger_name
    if re.search(r'"logger_name":\s*f?"nextgen\.', content):
        results["logger_name_pattern"] = True
        results["score"] += 1
    
    # Vérifier pattern log_dir
    if re.search(r'"log_dir":\s*f?"logs/', content):
        results["log_dir_pattern"] = True
        results["score"] += 1
    
    # Déterminer le statut global
    total_checks = 7
    if results["score"] == total_checks:
        results["status"] = "CONFORME"
    elif results["score"] >= total_checks * 0.7:
        results["status"] = "PARTIELLEMENT_CONFORME"
    else:
        results["status"] = "NON_CONFORME"
    
    # Calculer pourcentage
    results["conformity_percentage"] = round((results["score"] / total_checks) * 100, 1)
    
    return results

def analyze_maintenance_agents(agents_dir: Path) -> List[Dict[str, Any]]:
    """Analyse spécifique des agents MAINTENANCE (déjà conformes)."""
    maintenance_agents = []
    for file_path in agents_dir.glob("agent_MAINTENANCE_*.py"):
        if file_path.is_file():
            maintenance_agents.append(analyze_agent_file(file_path))
    return maintenance_agents

def analyze_regular_agents(agents_dir: Path) -> List[Dict[str, Any]]:
    """Analyse des agents réguliers (non-MAINTENANCE)."""
    regular_agents = []
    for file_path in agents_dir.glob("agent_*.py"):
        if file_path.is_file() and "MAINTENANCE" not in file_path.name:
            regular_agents.append(analyze_agent_file(file_path))
    return regular_agents

def generate_migration_plan(non_compliant_agents: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Génère un plan de migration basé sur les priorités."""
    plan = {
        "priority_high": [],
        "priority_medium": [],
        "priority_low": []
    }
    
    for agent in non_compliant_agents:
        filename = agent["file_name"]
        
        # Agents prioritaires
        if any(x in filename for x in ["01_coordinateur", "02_architecte", "03_specialiste", "04_expert"]):
            plan["priority_high"].append(filename)
        # Agents spécialisés
        elif any(x in filename for x in ["POSTGRESQL", "FASTAPI", "ARCHITECTURE", "SECURITY"]):
            plan["priority_medium"].append(filename)
        # Autres agents
        else:
            plan["priority_low"].append(filename)
    
    return plan

def main():
    """Fonction principale."""
    print("🔍 DÉBUT DE L'ANALYSE DE CONFORMITÉ LOGGING UNIFORME")
    print("=" * 60)
    
    agents_dir = Path("agents")
    if not agents_dir.exists():
        print(f"❌ Erreur: Le répertoire {agents_dir} n'existe pas!")
        return
    
    # Analyser les agents MAINTENANCE (référence)
    print("📊 Analyse des agents MAINTENANCE (référence)...")
    maintenance_results = analyze_maintenance_agents(agents_dir)
    
    # Analyser les agents réguliers
    print("📊 Analyse des agents réguliers...")
    regular_results = analyze_regular_agents(agents_dir)
    
    # Combiner tous les résultats
    all_results = maintenance_results + regular_results
    
    # Générer des statistiques
    total = len(all_results)
    conformes = sum(1 for r in all_results if r.get("status") == "CONFORME")
    partiellement_conformes = sum(1 for r in all_results if r.get("status") == "PARTIELLEMENT_CONFORME")
    non_conformes = sum(1 for r in all_results if r.get("status") == "NON_CONFORME")
    
    print(f"\n📈 STATISTIQUES GLOBALES")
    print(f"Total agents analysés: {total}")
    print(f"Agents conformes: {conformes} ({conformes/total*100:.1f}%)")
    print(f"Agents partiellement conformes: {partiellement_conformes} ({partiellement_conformes/total*100:.1f}%)")
    print(f"Agents non conformes: {non_conformes} ({non_conformes/total*100:.1f}%)")
    
    # Score moyen de conformité
    avg_score = sum(r.get("conformity_percentage", 0) for r in all_results) / total if total > 0 else 0
    print(f"Score moyen de conformité: {avg_score:.1f}%")
    
    # Analyser les agents MAINTENANCE
    maintenance_conformes = sum(1 for r in maintenance_results if r.get("status") == "CONFORME")
    if maintenance_results:
        print(f"\n🔧 AGENTS MAINTENANCE")
        print(f"Total: {len(maintenance_results)}")
        print(f"Conformes: {maintenance_conformes} ({maintenance_conformes/len(maintenance_results)*100:.1f}%)")
    
    # Analyser les agents réguliers
    regular_conformes = sum(1 for r in regular_results if r.get("status") == "CONFORME")
    if regular_results:
        print(f"\n⚙️ AGENTS RÉGULIERS")
        print(f"Total: {len(regular_results)}")
        print(f"Conformes: {regular_conformes} ({regular_conformes/len(regular_results)*100:.1f}%)")
    
    # Détails des agents non conformes
    non_compliant = [r for r in all_results if r.get("status") in ["NON_CONFORME", "PARTIELLEMENT_CONFORME"]]
    
    if non_compliant:
        print(f"\n❌ AGENTS À MIGRER ({len(non_compliant)})")
        print("-" * 60)
        
        for r in sorted(non_compliant, key=lambda x: x.get("conformity_percentage", 0)):
            status_icon = "⚠️" if r.get("status") == "PARTIELLEMENT_CONFORME" else "❌"
            print(f"{status_icon} {r['file_name']} ({r.get('conformity_percentage', 0)}%)")
            
            missing = []
            if not r.get("logging_manager_import"): missing.append("Import LoggingManager")
            if not r.get("get_logger_call"): missing.append("Appel get_logger")
            if not r.get("fallback_present"): missing.append("Fallback ImportError")
            if not r.get("metadata_present"): missing.append("Métadonnées")
            if not r.get("custom_config_present"): missing.append("Custom config")
            if not r.get("logger_name_pattern"): missing.append("Pattern logger_name")
            if not r.get("log_dir_pattern"): missing.append("Pattern log_dir")
            
            if missing:
                print(f"   Manque: {', '.join(missing)}")
    
    # Générer plan de migration
    migration_plan = generate_migration_plan(non_compliant)
    
    print(f"\n🎯 PLAN DE MIGRATION")
    print("-" * 60)
    print(f"Priorité HAUTE ({len(migration_plan['priority_high'])} agents):")
    for agent in migration_plan['priority_high']:
        print(f"  • {agent}")
    
    print(f"\nPriorité MOYENNE ({len(migration_plan['priority_medium'])} agents):")
    for agent in migration_plan['priority_medium']:
        print(f"  • {agent}")
    
    print(f"\nPriorité BASSE ({len(migration_plan['priority_low'])} agents):")
    for agent in migration_plan['priority_low']:
        print(f"  • {agent}")
    
    # Sauvegarder le rapport complet
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"rapport_conformite_logging_{timestamp}.json"
    
    report_data = {
        "timestamp": timestamp,
        "summary": {
            "total_agents": total,
            "conformant_agents": conformes,
            "partially_conformant_agents": partiellement_conformes,
            "non_conformant_agents": non_conformes,
            "average_conformity_score": avg_score
        },
        "maintenance_agents": {
            "total": len(maintenance_results),
            "conformant": maintenance_conformes,
            "results": maintenance_results
        },
        "regular_agents": {
            "total": len(regular_results),
            "conformant": regular_conformes,
            "results": regular_results
        },
        "migration_plan": migration_plan,
        "detailed_results": all_results
    }
    
    with open(report_filename, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Rapport détaillé sauvegardé: {report_filename}")
    print(f"🏁 Analyse terminée!")

if __name__ == "__main__":
    main()