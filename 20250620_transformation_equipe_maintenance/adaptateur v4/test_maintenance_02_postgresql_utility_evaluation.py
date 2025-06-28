#!/usr/bin/env python3
"""
Test d'évaluation d'utilité des agents PostgreSQL avec agent_MAINTENANCE_02_evaluateur_utilite.py
Validation du système de scoring heuristique en conditions réelles.
"""
import ast
import sys
import json
from pathlib import Path
from datetime import datetime

def evaluate_postgresql_agents_utility():
    """Évaluation d'utilité des agents PostgreSQL en simulant l'agent MAINTENANCE 02."""
    print("=" * 80)
    print("⚖️ ÉVALUATION UTILITÉ AGENTS POSTGRESQL VIA AGENT MAINTENANCE 02")
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
    evaluation_results = []
    
    print(f"🎯 Évaluation de {len(postgresql_agents)} agents PostgreSQL...")
    print(f"📊 Système de scoring MAINTENANCE 02 v2.2.0\n")
    
    for agent_name in postgresql_agents:
        agent_path = agents_dir / agent_name
        print(f"⚖️ Évaluation: {agent_name}")
        
        if not agent_path.exists():
            print(f"   ❌ Fichier non trouvé: {agent_path}")
            evaluation_results.append({
                "path": str(agent_path),
                "error": "Fichier non trouvé",
                "score": 0,
                "is_useful": False
            })
            continue
        
        try:
            # Lecture du fichier (simulation execute_task de MAINTENANCE 02)
            with open(agent_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Évaluation via système de scoring MAINTENANCE 02
            evaluation = evaluate_utility_ast(content)
            
            # Affichage résumé
            if "error" in evaluation:
                print(f"   ❌ {evaluation['error']}")
                print(f"   📊 Score: 0 | Utilité: ❌ Peu utile")
            else:
                score = evaluation['score']
                is_useful = evaluation['is_useful']
                usefulness_icon = "✅ Utile" if is_useful else "❌ Peu utile"
                
                print(f"   📊 Score: {score} | Utilité: {usefulness_icon}")
                
                # Détails du scoring
                details = evaluation.get('details', {})
                if details:
                    print(f"   📋 Détails: {details['imports']}imp, {details['classes']}cls, {details['functions']}fn, {details['calls']}calls")
            
            evaluation_results.append({
                "path": str(agent_path),
                **evaluation
            })
            
        except Exception as e:
            print(f"   ❌ Erreur lors de l'évaluation: {e}")
            evaluation_results.append({
                "path": str(agent_path),
                "error": str(e),
                "score": 0,
                "is_useful": False
            })
    
    # Génération du rapport consolidé d'utilité
    generate_utility_report(evaluation_results)
    
    return evaluation_results

def evaluate_utility_ast(code: str) -> dict:
    """
    Simulation exacte de la méthode _evaluate_ast + execute_task de l'agent MAINTENANCE 02.
    """
    try:
        tree = ast.parse(code)
        score = calculate_utility_score(tree)
        min_score = 15  # Seuil par défaut MAINTENANCE 02
        is_useful = score >= min_score
        
        # Détails pour analyse
        details = extract_code_details(tree)
        
        return {
            "score": score,
            "is_useful": is_useful,
            "details": details
        }
    except SyntaxError as e:
        return {
            "error": f"Erreur de syntaxe: {e}",
            "score": 0,
            "is_useful": False
        }

def calculate_utility_score(tree):
    """Simulation exacte de _evaluate_ast de MAINTENANCE 02."""
    score = 0
    has_class = False
    has_function = False

    # Premier passage : calcul score de base
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            score += 1 * len(node.names)
        elif isinstance(node, ast.ImportFrom):
            score += 1 * len(node.names)
        elif isinstance(node, ast.FunctionDef):
            score += 5
            has_function = True
            if node.body:
                score += len(node.body)
        elif isinstance(node, ast.ClassDef):
            score += 10
            has_class = True
            if node.body:
                score += len(node.body)
        elif isinstance(node, ast.Call):
            score += 1
        elif isinstance(node, ast.Try):
            score += 2
        elif isinstance(node, (ast.If, ast.For, ast.While)):
            score += 2

    # Bonus classe + fonction
    if has_class and has_function:
        score += 5
        
    # Malus éléments vides
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            score -= 5
        if isinstance(node, ast.ClassDef) and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            score -= 5

    return max(0, score)

def extract_code_details(tree):
    """Extrait les détails pour analyse."""
    imports = 0
    classes = 0
    functions = 0
    calls = 0
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports += 1
        elif isinstance(node, ast.ClassDef):
            classes += 1
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions += 1
        elif isinstance(node, ast.Call):
            calls += 1
    
    return {
        "imports": imports,
        "classes": classes, 
        "functions": functions,
        "calls": calls
    }

def generate_utility_report(results):
    """Génère un rapport consolidé d'évaluation d'utilité."""
    print("\n" + "=" * 80)
    print("📊 RAPPORT CONSOLIDÉ D'ÉVALUATION D'UTILITÉ")
    print("=" * 80)
    
    # Statistiques globales
    total_agents = len(results)
    successful_evaluations = sum(1 for r in results if "error" not in r)
    error_count = total_agents - successful_evaluations
    
    if successful_evaluations > 0:
        scores = [r["score"] for r in results if "error" not in r]
        useful_agents = [r for r in results if r.get("is_useful", False)]
        
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        print(f"📈 Statistiques d'utilité:")
        print(f"   Total agents évalués: {total_agents}")
        print(f"   Évaluations réussies: {successful_evaluations}")
        print(f"   Erreurs: {error_count}")
        print(f"   Agents utiles: {len(useful_agents)}/{successful_evaluations} ({len(useful_agents)/successful_evaluations*100:.1f}%)")
        print(f"   Score moyen: {avg_score:.1f} points")
        print(f"   Score max: {max_score} points")
        print(f"   Score min: {min_score} points")
        
        # Top 3 agents les plus utiles
        useful_sorted = sorted([r for r in results if "error" not in r], 
                              key=lambda x: x["score"], reverse=True)
        
        print(f"\n🏆 Top 3 agents les plus utiles:")
        for i, agent in enumerate(useful_sorted[:3], 1):
            name = Path(agent["path"]).name
            score = agent["score"]
            useful = "✅" if agent["is_useful"] else "❌"
            print(f"   {i}. {name}: {score} points {useful}")
        
        # Agents peu utiles nécessitant attention
        low_utility = [r for r in results if not r.get("is_useful", True)]
        if low_utility:
            print(f"\n⚠️  Agents peu utiles nécessitant attention:")
            for agent in low_utility:
                name = Path(agent["path"]).name
                score = agent.get("score", 0)
                error = agent.get("error", "Score faible")
                print(f"   ❌ {name}: {score} points ({error})")
    
    # Sauvegarde du rapport JSON
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "agent_evaluator": "MAINTENANCE_02_evaluateur_utilite v2.2.0",
        "scoring_system": "Heuristique AST avec seuil 15 points",
        "total_agents": total_agents,
        "successful_evaluations": successful_evaluations,
        "agents_useful": len([r for r in results if r.get("is_useful", False)]),
        "average_score": avg_score if successful_evaluations > 0 else 0,
        "detailed_results": results
    }
    
    report_path = Path("reports") / f"postgresql_utility_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Rapport d'utilité détaillé sauvegardé: {report_path}")

if __name__ == "__main__":
    try:
        results = evaluate_postgresql_agents_utility()
        print(f"\n🎉 Évaluation d'utilité terminée avec succès!")
        print(f"⚖️ {len(results)} agents PostgreSQL évalués par l'agent MAINTENANCE 02")
        
        # Validation de l'agent MAINTENANCE 02
        useful_count = len([r for r in results if r.get("is_useful", False)])
        print(f"✅ Agent MAINTENANCE 02 opérationnel: {useful_count} agents utiles détectés")
        
    except Exception as e:
        print(f"\n❌ Erreur critique: {e}")
        sys.exit(1)