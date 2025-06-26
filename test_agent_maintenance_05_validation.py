#!/usr/bin/env python3
"""
Test de structure et capacités pour agent_MAINTENANCE_05_documenteur_peer_reviewer.py
Validation des technologies d'audit Flake8, AST et génération rapports.
"""
import ast
import sys
from pathlib import Path

def test_agent_structure_and_capabilities():
    """Test complet de l'agent MAINTENANCE 05."""
    print("=" * 80)
    print("📋 TEST AGENT MAINTENANCE 05 - DOCUMENTEUR PEER REVIEWER")
    print("=" * 80)
    
    agent_file = Path("agents/agent_MAINTENANCE_05_documenteur_peer_reviewer.py")
    
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
        dataclasses = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
                # Détection dataclass
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
                        dataclasses.append(node.name)
                    elif isinstance(decorator, ast.Attribute) and decorator.attr == "dataclass":
                        dataclasses.append(node.name)
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
        print(f"   Classes: {len(classes)} (principales: {[c for c in classes if 'Agent' in c or 'Quality' in c]})")
        print(f"   Dataclasses: {dataclasses}")
        print(f"   Fonctions: {len(functions)} (dont {len(async_functions)} async)")
        print(f"   Imports: {len(imports)} modules")
        
        # Vérifications critiques
        success_count = 0
        total_checks = 16
        
        # 1. Classe principale
        if "AgentMAINTENANCE05DocumenteurPeerReviewer" in classes:
            print("✅ Classe principale AgentMAINTENANCE05DocumenteurPeerReviewer trouvée")
            success_count += 1
        else:
            print("❌ Classe principale manquante")
        
        # 2. Fonction factory
        if "create_agent_MAINTENANCE_05_documenteur_peer_reviewer" in functions:
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
        
        # 6. Version 5.2.0
        version_found = "Version: 5.2.0" in code
        if version_found:
            print("✅ Version 5.2.0 trouvée")
            success_count += 1
        else:
            print("❌ Version attendue non trouvée")
        
        # 7. Dataclass UniversalQualityIssue
        if "UniversalQualityIssue" in dataclasses:
            print("✅ Dataclass UniversalQualityIssue détectée")
            success_count += 1
        else:
            print("❌ Dataclass UniversalQualityIssue manquante")
        
        # 8. Import difflib (génération diff)
        if "difflib" in imports:
            print("✅ Import difflib détecté")
            success_count += 1
        else:
            print("❌ Import difflib manquant")
        
        # 9. Import subprocess (Flake8 async)
        if "subprocess" in imports:
            print("✅ Import subprocess détecté")
            success_count += 1
        else:
            print("❌ Import subprocess manquant")
        
        # 10. Import ast (analyse AST)
        if "ast" in imports:
            print("✅ Import ast détecté")
            success_count += 1
        else:
            print("❌ Import ast manquant")
        
        # 11. Méthode audit_universal_quality (check in async functions)
        if "audit_universal_quality" in async_functions or "async audit_universal_quality" in functions:
            print("✅ Méthode audit_universal_quality présente")
            success_count += 1
        else:
            print("❌ Méthode audit_universal_quality manquante")
        
        # 12. Méthode _run_flake8 (check in async functions)
        if "_run_flake8" in async_functions or "async _run_flake8" in functions:
            print("✅ Méthode _run_flake8 présente")
            success_count += 1
        else:
            print("❌ Méthode _run_flake8 manquante")
        
        # 13. Méthode _perform_ast_audit (check in async functions)
        if "_perform_ast_audit" in async_functions or "async _perform_ast_audit" in functions:
            print("✅ Méthode _perform_ast_audit présente")
            success_count += 1
        else:
            print("❌ Méthode _perform_ast_audit manquante")
        
        # 14. Test capacités étendues (10 capacités)
        capabilities_pattern = "generate_mission_report"
        if capabilities_pattern in code and "audit_universal_quality" in code:
            print("✅ Capacités étendues détectées")
            success_count += 1
        else:
            print("❌ Capacités étendues manquantes")
        
        # 15. Docstring enrichie détectée
        if "Agent spécialisé dans la génération de rapports de mission" in code:
            print("✅ Docstring enrichie détectée")
            success_count += 1
        else:
            print("❌ Docstring enrichie manquante")
        
        # 16. Test fonctionnalités audit avancées
        print("\n🔍 Test simulation capacités audit:")
        try:
            audit_features = ["create_subprocess_shell", "_has_module_docstring_manual", "UniversalQualityIssue", "difflib.unified_diff"]
            found_features = [f for f in audit_features if f in code]
            
            if len(found_features) >= 3:
                print(f"✅ Fonctionnalités audit détectées: {len(found_features)}/4")
                print(f"   Présentes: {found_features}")
                success_count += 1
            else:
                print(f"❌ Fonctionnalités audit insuffisantes: {found_features}")
            
        except Exception as e:
            print(f"❌ Erreur vérification audit: {e}")
        
        # Résumé
        print("\n" + "=" * 80)
        print(f"📊 RÉSULTATS: {success_count}/{total_checks} vérifications réussies")
        
        if success_count == total_checks:
            print("🎉 AGENT PARFAITEMENT CONFORME - Technologies audit validées")
            return True
        elif success_count >= 13:
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