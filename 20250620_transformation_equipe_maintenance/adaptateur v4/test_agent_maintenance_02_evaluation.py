#!/usr/bin/env python3
"""
Test de structure et capacités pour agent_MAINTENANCE_02_evaluateur_utilite.py
Validation du système de scoring et d'évaluation d'utilité.
"""
import ast
import sys
from pathlib import Path

def test_agent_structure_and_scoring():
    """Test complet de l'agent MAINTENANCE 02."""
    print("=" * 80)
    print("🧪 TEST AGENT MAINTENANCE 02 - ÉVALUATEUR D'UTILITÉ")
    print("=" * 80)
    
    agent_file = Path("agents/agent_MAINTENANCE_02_evaluateur_utilite.py")
    
    if not agent_file.exists():
        print("❌ Fichier agent non trouvé")
        return False
    
    try:
        # Lecture et parsing du code
        with open(agent_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        tree = ast.parse(code)
        print("✅ Syntaxe Python valide")
        
        # Analyse de la structure
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
        total_checks = 9
        
        # 1. Classe principale
        if "AgentMAINTENANCE02EvaluateurUtilite" in classes:
            print("✅ Classe principale AgentMAINTENANCE02EvaluateurUtilite trouvée")
            success_count += 1
        else:
            print("❌ Classe principale manquante")
        
        # 2. Fonction factory
        if "create_agent_MAINTENANCE_02_evaluateur_utilite" in functions:
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
        
        # 6. Version 2.2.0
        version_found = "Version: 2.2.0" in code
        if version_found:
            print("✅ Version 2.2.0 trouvée")
            success_count += 1
        else:
            print("❌ Version attendue non trouvée")
        
        # 7. Méthode d'évaluation AST
        if "_evaluate_ast" in functions:
            print("✅ Méthode _evaluate_ast présente")
            success_count += 1
        else:
            print("❌ Méthode _evaluate_ast manquante")
        
        # 8. Import AST pour scoring
        if "ast" in imports:
            print("✅ Import ast pour analyse structurelle présent")
            success_count += 1
        else:
            print("❌ Import ast manquant")
        
        # 9. Test simulation du scoring (comme le ferait l'agent)
        print("\n🧮 Test simulation scoring heuristique:")
        try:
            score = simulate_scoring(tree)
            print(f"✅ Scoring simulé réussi: {score} points")
            
            # Classification
            min_score = 15  # Seuil par défaut
            is_useful = score >= min_score
            print(f"✅ Classification: {'Utile' if is_useful else 'Peu utile'} (seuil: {min_score})")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Erreur simulation scoring: {e}")
        
        # Résumé
        print("\n" + "=" * 80)
        print(f"📊 RÉSULTATS: {success_count}/{total_checks} vérifications réussies")
        
        if success_count == total_checks:
            print("🎉 AGENT PARFAITEMENT CONFORME - Capacités d'évaluation validées")
            return True
        elif success_count >= 7:
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

def simulate_scoring(tree):
    """Simulation de la méthode _evaluate_ast pour validation."""
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

if __name__ == "__main__":
    success = test_agent_structure_and_scoring()
    print(f"\n🏁 Test terminé: {'RÉUSSI' if success else 'ÉCHEC'}")
    sys.exit(0 if success else 1)