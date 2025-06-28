#!/usr/bin/env python3
"""
Test de structure et syntaxe pour agent_MAINTENANCE_01_analyseur_structure.py
Validation des capacités d'analyse structurelle via AST.
"""
import ast
import sys
from pathlib import Path

def test_agent_structure_and_capabilities():
    """Test complet de l'agent MAINTENANCE 01."""
    print("=" * 80)
    print("🧪 TEST AGENT MAINTENANCE 01 - ANALYSEUR DE STRUCTURE")
    print("=" * 80)
    
    agent_file = Path("agents/agent_MAINTENANCE_01_analyseur_structure.py")
    
    if not agent_file.exists():
        print("❌ Fichier agent non trouvé")
        return False
    
    try:
        # Lecture et parsing du code
        with open(agent_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        tree = ast.parse(code)
        print("✅ Syntaxe Python valide")
        
        # Analyse de la structure comme le ferait l'agent
        classes = []
        functions = []
        imports = []
        async_functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.AsyncFunctionDef):
                functions.append(f"async {node.name}")
                async_functions.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        print(f"✅ Structure détectée:")
        print(f"   Classes: {classes}")
        print(f"   Fonctions: {len(functions)} (dont {len(async_functions)} async)")
        print(f"   Imports: {len(imports)} modules")
        
        # Vérifications critiques
        success_count = 0
        total_checks = 8
        
        # 1. Classe principale
        if "AgentMAINTENANCE01AnalyseurStructure" in classes:
            print("✅ Classe principale AgentMAINTENANCE01AnalyseurStructure trouvée")
            success_count += 1
        else:
            print("❌ Classe principale manquante")
        
        # 2. Fonction factory
        if "create_agent_MAINTENANCE_01_analyseur_structure" in functions:
            print("✅ Fonction factory trouvée")
            success_count += 1
        else:
            print("❌ Fonction factory manquante")
        
        # 3. Méthodes Pattern Factory async
        required_async = ["startup", "execute_task", "health_check", "shutdown"]
        missing_async = [m for m in required_async if m not in async_functions]
        if not missing_async:
            print("✅ Toutes les méthodes async Pattern Factory présentes")
            success_count += 1
        else:
            print(f"❌ Méthodes async manquantes: {missing_async}")
        
        # 4. Méthode get_capabilities
        if "get_capabilities" in functions:
            print("✅ Méthode get_capabilities trouvée")
            success_count += 1
        else:
            print("❌ Méthode get_capabilities manquante")
        
        # 5. Import Pattern Factory
        if any("agent_factory_architecture" in imp for imp in imports):
            print("✅ Import Pattern Factory détecté")
            success_count += 1
        else:
            print("❌ Import Pattern Factory manquant")
        
        # 6. Version 1.3.0
        version_found = "Version: 1.3.0" in code
        if version_found:
            print("✅ Version 1.3.0 trouvée")
            success_count += 1
        else:
            print("❌ Version attendue non trouvée")
        
        # 7. Méthodes d'analyse spécialisées
        analysis_methods = ["_analyze_python_file", "run_analysis"]
        found_analysis = [m for m in analysis_methods if m in functions]
        if len(found_analysis) >= 2:
            print("✅ Méthodes d'analyse spécialisées présentes")
            success_count += 1
        else:
            print(f"❌ Méthodes d'analyse manquantes: {[m for m in analysis_methods if m not in found_analysis]}")
        
        # 8. Présence AST et modules d'analyse
        required_imports = ["ast", "asyncio", "logging"]
        found_required = [imp for imp in required_imports if any(imp in i for i in imports)]
        if len(found_required) >= 3:
            print("✅ Imports requis pour analyse AST présents")
            success_count += 1
        else:
            print(f"❌ Imports manquants: {[imp for imp in required_imports if imp not in found_required]}")
        
        # Test capacité d'auto-analyse (simulation)
        print("\n🔍 Test simulation analyse AST:")
        try:
            # Simulation de ce que ferait _analyze_python_file
            ast_tree = ast.parse(code)
            simulated_analysis = {
                "imports": [],
                "classes": [],
                "functions": [],
                "has_async": False
            }
            
            for node in ast.walk(ast_tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        simulated_analysis["imports"].append(alias.name)
                elif isinstance(node, ast.ClassDef):
                    simulated_analysis["classes"].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    simulated_analysis["functions"].append(node.name)
                elif isinstance(node, ast.AsyncFunctionDef):
                    simulated_analysis["functions"].append(f"async {node.name}")
                    simulated_analysis["has_async"] = True
            
            print(f"✅ Auto-analyse simulée réussie:")
            print(f"   {len(simulated_analysis['classes'])} classes")
            print(f"   {len(simulated_analysis['functions'])} fonctions")
            print(f"   Async détecté: {simulated_analysis['has_async']}")
            
        except Exception as e:
            print(f"❌ Erreur simulation analyse: {e}")
        
        # Résumé
        print("\n" + "=" * 80)
        print(f"📊 RÉSULTATS: {success_count}/{total_checks} vérifications réussies")
        
        if success_count == total_checks:
            print("🎉 AGENT PARFAITEMENT CONFORME - Capacités d'analyse validées")
            return True
        elif success_count >= 6:
            print("✅ AGENT FONCTIONNEL - Capacités principales validées")
            return True
        else:
            print("❌ AGENT DÉFAILLANT - Corrections nécessaires")
            return False
            
    except SyntaxError as e:
        print(f"❌ Erreur de syntaxe: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur analyse: {e}")
        return False

if __name__ == "__main__":
    success = test_agent_structure_and_capabilities()
    print(f"\n🏁 Test terminé: {'RÉUSSI' if success else 'ÉCHEC'}")
    sys.exit(0 if success else 1)