#!/usr/bin/env python3
"""
Test de structure et syntaxe pour agent_MAINTENANCE_00_chef_equipe_coordinateur.py
Validation indépendante des dépendances externes.
"""
import ast
import sys
from pathlib import Path

def test_agent_structure():
    """Analyse la structure du fichier agent sans l'exécuter."""
    print("=" * 80)
    print("🧪 TEST STRUCTURE AGENT MAINTENANCE 00 - CHEF D'ÉQUIPE COORDINATEUR")
    print("=" * 80)
    
    agent_file = Path("agents/agent_MAINTENANCE_00_chef_equipe_coordinateur.py")
    
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
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        
        print(f"✅ Classes trouvées: {classes}")
        print(f"✅ Fonctions trouvées: {len(functions)} (principales: {[f for f in functions if not f.startswith('_')][:5]})")
        
        # Vérifications critiques
        success_count = 0
        total_checks = 6
        
        # 1. Classe principale présente
        if "ChefEquipeCoordinateurEnterprise" in classes:
            print("✅ Classe ChefEquipeCoordinateurEnterprise trouvée")
            success_count += 1
        else:
            print("❌ Classe principale manquante")
        
        # 2. Fonction factory présente
        if "create_agent_MAINTENANCE_00_chef_equipe_coordinateur" in functions:
            print("✅ Fonction factory trouvée")
            success_count += 1
        else:
            print("❌ Fonction factory manquante")
        
        # 3. Méthodes Pattern Factory
        required_methods = ["startup", "shutdown", "execute_task", "health_check", "get_capabilities"]
        
        # Parser les méthodes de la classe principale
        class_methods = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "ChefEquipeCoordinateurEnterprise":
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_methods.append(item.name)
        
        missing_methods = [m for m in required_methods if m not in class_methods]
        if not missing_methods:
            print("✅ Toutes les méthodes Pattern Factory présentes")
            success_count += 1
        else:
            print(f"❌ Méthodes manquantes: {missing_methods}")
        
        # 4. Import Pattern Factory
        if any("agent_factory_architecture" in imp for imp in imports):
            print("✅ Import Pattern Factory détecté")
            success_count += 1
        else:
            print("❌ Import Pattern Factory manquant")
        
        # 5. Vérification version et docstring
        version_found = "Version:" in code and "4.3.0" in code
        if version_found:
            print("✅ Version 4.3.0 trouvée")
            success_count += 1
        else:
            print("❌ Version attendue non trouvée")
        
        # 6. Structure async
        async_methods = []
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                async_methods.append(node.name)
        
        required_async = ["startup", "shutdown", "execute_task", "health_check"]
        async_ok = all(method in async_methods for method in required_async)
        if async_ok:
            print("✅ Méthodes async correctement définies")
            success_count += 1
        else:
            print(f"❌ Méthodes async manquantes: {[m for m in required_async if m not in async_methods]}")
        
        # Résumé
        print("\n" + "=" * 80)
        print(f"📊 RÉSULTATS: {success_count}/{total_checks} vérifications réussies")
        
        if success_count == total_checks:
            print("🎉 STRUCTURE PARFAITE - Agent conforme Pattern Factory")
            return True
        elif success_count >= 4:
            print("✅ STRUCTURE CORRECTE - Agent majoritairement conforme")
            return True
        else:
            print("❌ STRUCTURE DÉFAILLANTE - Agent non conforme")
            return False
            
    except SyntaxError as e:
        print(f"❌ Erreur de syntaxe: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur analyse: {e}")
        return False

if __name__ == "__main__":
    success = test_agent_structure()
    print(f"\n🏁 Test terminé: {'RÉUSSI' if success else 'ÉCHEC'}")
    sys.exit(0 if success else 1)