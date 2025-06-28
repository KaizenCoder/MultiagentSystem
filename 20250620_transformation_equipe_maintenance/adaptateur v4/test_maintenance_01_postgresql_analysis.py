#!/usr/bin/env python3
"""
Test d'analyse des agents PostgreSQL avec agent_MAINTENANCE_01_analyseur_structure.py
Validation des capacités d'analyse en conditions réelles.
"""
import ast
import sys
import json
from pathlib import Path
from datetime import datetime

def analyze_postgresql_agents_with_ast():
    """Analyse des agents PostgreSQL en simulant l'agent MAINTENANCE 01."""
    print("=" * 80)
    print("🔍 ANALYSE AGENTS POSTGRESQL VIA AGENT MAINTENANCE 01")
    print("=" * 80)
    
    # Agents PostgreSQL identifiés
    postgresql_agents = [
        "agent_POSTGRESQL_base.py",
        "agent_POSTGRESQL_diagnostic_postgres_final.py", 
        "agent_POSTGRESQL_docker_specialist.py",
        "agent_POSTGRESQL_documentation_manager.py",
        "agent_POSTGRESQL_resolution_finale.py",
        "agent_POSTGRESQL_sqlalchemy_fixer.py",
        "agent_POSTGRESQL_sqlalchemy_fixer_new.py",
        "agent_POSTGRESQL_testing_specialist.py",
        "agent_POSTGRESQL_web_researcher.py",
        "agent_POSTGRESQL_windows_postgres.py",
        "agent_POSTGRESQL_workspace_organizer.py"
    ]
    
    agents_dir = Path("agents")
    analysis_results = []
    
    for agent_name in postgresql_agents:
        agent_path = agents_dir / agent_name
        print(f"\n🔎 Analyse de: {agent_name}")
        
        if not agent_path.exists():
            print(f"   ❌ Fichier non trouvé: {agent_path}")
            analysis_results.append({
                "path": str(agent_path),
                "error": "Fichier non trouvé"
            })
            continue
        
        try:
            # Lecture du fichier (comme le ferait l'agent MAINTENANCE 01)
            with open(agent_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Analyse AST (simulation de _analyze_python_file)
            analysis = analyze_python_file_ast(content)
            
            # Affichage résumé
            if "error" in analysis:
                print(f"   ❌ Erreur syntaxique: {analysis['error']}")
            else:
                print(f"   ✅ Classes: {len(analysis['classes'])}")
                print(f"   ✅ Fonctions: {len(analysis['functions'])}")
                print(f"   ✅ Imports: {len(analysis['imports'])}")
                print(f"   ✅ Async: {analysis['has_async']}")
                
                # Vérifications Pattern Factory
                pf_score = check_pattern_factory_compliance(analysis, content)
                print(f"   📊 Score Pattern Factory: {pf_score}/5")
            
            analysis_results.append({
                "path": str(agent_path),
                "analysis": analysis
            })
            
        except Exception as e:
            print(f"   ❌ Erreur lors de l'analyse: {e}")
            analysis_results.append({
                "path": str(agent_path),
                "error": str(e)
            })
    
    # Génération du rapport consolidé
    generate_consolidated_report(analysis_results)
    
    return analysis_results

def analyze_python_file_ast(code: str) -> dict:
    """
    Simulation exacte de la méthode _analyze_python_file de l'agent MAINTENANCE 01.
    """
    analysis_report = {
        "imports": [],
        "classes": [],
        "functions": [],
        "has_async": False,
    }
    
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    analysis_report["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    analysis_report["imports"].append(node.module)
            elif isinstance(node, ast.ClassDef):
                analysis_report["classes"].append(node.name)
            elif isinstance(node, ast.FunctionDef):
                analysis_report["functions"].append(node.name)
            elif isinstance(node, ast.AsyncFunctionDef):
                analysis_report["functions"].append(f"async {node.name}")
                analysis_report["has_async"] = True
    except SyntaxError as e:
        return {"error": f"SyntaxError: {e}"}
    
    return analysis_report

def check_pattern_factory_compliance(analysis, code_content):
    """Vérifie la conformité Pattern Factory."""
    score = 0
    
    # 1. Présence d'une classe principale
    if analysis.get("classes"):
        score += 1
    
    # 2. Méthodes async requises
    required_async = ["async startup", "async execute_task", "async health_check", "async shutdown"]
    async_found = [f for f in analysis.get("functions", []) if f in required_async]
    if len(async_found) >= 3:
        score += 1
    
    # 3. Import Pattern Factory
    if any("agent_factory_architecture" in imp for imp in analysis.get("imports", [])):
        score += 1
    
    # 4. Fonction factory
    factory_functions = [f for f in analysis.get("functions", []) if f.startswith("create_agent")]
    if factory_functions:
        score += 1
    
    # 5. get_capabilities
    if "get_capabilities" in analysis.get("functions", []):
        score += 1
    
    return score

def generate_consolidated_report(results):
    """Génère un rapport consolidé de l'analyse."""
    print("\n" + "=" * 80)
    print("📊 RAPPORT CONSOLIDÉ D'ANALYSE")
    print("=" * 80)
    
    total_agents = len(results)
    successful_analyses = sum(1 for r in results if "analysis" in r)
    error_count = total_agents - successful_analyses
    
    print(f"📈 Statistiques globales:")
    print(f"   Total agents analysés: {total_agents}")
    print(f"   Analyses réussies: {successful_analyses}")
    print(f"   Erreurs: {error_count}")
    
    if successful_analyses > 0:
        # Analyse des patterns
        all_classes = []
        all_functions = []
        async_agents = 0
        pf_scores = []
        
        for result in results:
            if "analysis" in result:
                analysis = result["analysis"]
                all_classes.extend(analysis.get("classes", []))
                all_functions.extend(analysis.get("functions", []))
                if analysis.get("has_async", False):
                    async_agents += 1
                
                # Score PF
                code_path = Path(result["path"])
                if code_path.exists():
                    with open(code_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    pf_score = check_pattern_factory_compliance(analysis, content)
                    pf_scores.append(pf_score)
        
        print(f"\n📋 Analyse des patterns:")
        print(f"   Classes uniques trouvées: {len(set(all_classes))}")
        print(f"   Fonctions uniques: {len(set(all_functions))}")
        print(f"   Agents avec async: {async_agents}/{successful_analyses}")
        
        if pf_scores:
            avg_pf_score = sum(pf_scores) / len(pf_scores)
            print(f"   Score Pattern Factory moyen: {avg_pf_score:.1f}/5")
    
    # Sauvegarde du rapport JSON
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "agent_analyzer": "MAINTENANCE_01_analyseur_structure v1.3.0",
        "total_agents": total_agents,
        "successful_analyses": successful_analyses,
        "detailed_results": results
    }
    
    report_path = Path("reports") / f"postgresql_agents_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Rapport détaillé sauvegardé: {report_path}")
    
    # Agents problématiques
    error_agents = [r for r in results if "error" in r]
    if error_agents:
        print(f"\n⚠️  Agents nécessitant attention:")
        for agent in error_agents:
            print(f"   ❌ {Path(agent['path']).name}: {agent['error']}")

if __name__ == "__main__":
    try:
        results = analyze_postgresql_agents_with_ast()
        print(f"\n🎉 Analyse terminée avec succès!")
        print(f"🔍 {len(results)} agents PostgreSQL analysés par l'agent MAINTENANCE 01")
    except Exception as e:
        print(f"\n❌ Erreur critique: {e}")
        sys.exit(1)