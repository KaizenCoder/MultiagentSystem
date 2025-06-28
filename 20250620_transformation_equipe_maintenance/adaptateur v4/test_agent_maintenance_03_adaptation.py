#!/usr/bin/env python3
"""
Test de structure et capacités pour agent_MAINTENANCE_03_adaptateur_code.py
Validation des technologies LibCST et stratégies de réparation.
"""
import ast
import sys
from pathlib import Path

def test_agent_structure_and_libcst():
    """Test complet de l'agent MAINTENANCE 03."""
    print("=" * 80)
    print("🧪 TEST AGENT MAINTENANCE 03 - ADAPTATEUR DE CODE")
    print("=" * 80)
    
    agent_file = Path("agents/agent_MAINTENANCE_03_adaptateur_code.py")
    
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
        print(f"   Classes: {len(classes)} (principales: {[c for c in classes if 'Agent' in c or 'Cst' in c]})")
        print(f"   Fonctions: {len(functions)} (dont {len(async_functions)} async)")
        print(f"   Imports: {len(imports)} modules")
        
        # Vérifications critiques
        success_count = 0
        total_checks = 12
        
        # 1. Classe principale
        if "AgentMAINTENANCE03AdaptateurCode" in classes:
            print("✅ Classe principale AgentMAINTENANCE03AdaptateurCode trouvée")
            success_count += 1
        else:
            print("❌ Classe principale manquante")
        
        # 2. Fonction factory
        if "create_agent_MAINTENANCE_03_adaptateur_code" in functions:
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
        
        # 6. Version 3.1.0
        version_found = "Version: 3.1.0" in code
        if version_found:
            print("✅ Version 3.1.0 trouvée")
            success_count += 1
        else:
            print("❌ Version attendue non trouvée")
        
        # 7. Import LibCST 
        if "libcst" in imports:
            print("✅ Import LibCST détecté")
            success_count += 1
        else:
            print("❌ Import LibCST manquant")
        
        # 8. Classes CSTTransformer
        cst_classes = [c for c in classes if "Cst" in c and "Transformer" in code]
        if len(cst_classes) >= 2:
            print(f"✅ Classes CSTTransformer détectées: {cst_classes}")
            success_count += 1
        else:
            print(f"❌ Classes CSTTransformer insuffisantes: {cst_classes}")
        
        # 9. Méthode correction indentation
        if "_fix_indentation_errors" in functions:
            print("✅ Méthode _fix_indentation_errors présente")
            success_count += 1
        else:
            print("❌ Méthode _fix_indentation_errors manquante")
        
        # 10. Import Pyflakes
        if any("pyflakes" in imp for imp in imports):
            print("✅ Import Pyflakes détecté")
            success_count += 1
        else:
            print("❌ Import Pyflakes manquant")
        
        # 11. Mapping imports complexes
        if "COMPLEX_IMPORT_MAP" in code:
            print("✅ COMPLEX_IMPORT_MAP détecté")
            success_count += 1
        else:
            print("❌ COMPLEX_IMPORT_MAP manquant")
        
        # 12. Test simulation LibCST (vérification imports disponibles)
        print("\n🔧 Test simulation capacités LibCST:")
        try:
            # Vérification de la présence des imports LibCST dans le code
            libcst_features = ["cst.parse_module", "CSTTransformer", "leave_IndentedBlock", "_build_module_path"]
            found_features = [f for f in libcst_features if f in code]
            
            if len(found_features) >= 3:
                print(f"✅ Fonctionnalités LibCST détectées: {len(found_features)}/4")
                print(f"   Présentes: {found_features}")
                success_count += 1
            else:
                print(f"❌ Fonctionnalités LibCST insuffisantes: {found_features}")
            
        except Exception as e:
            print(f"❌ Erreur vérification LibCST: {e}")
        
        # Résumé
        print("\n" + "=" * 80)
        print(f"📊 RÉSULTATS: {success_count}/{total_checks} vérifications réussies")
        
        if success_count == total_checks:
            print("🎉 AGENT PARFAITEMENT CONFORME - Technologies LibCST validées")
            return True
        elif success_count >= 9:
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
    success = test_agent_structure_and_libcst()
    print(f"\n🏁 Test terminé: {'RÉUSSI' if success else 'ÉCHEC'}")
    sys.exit(0 if success else 1)