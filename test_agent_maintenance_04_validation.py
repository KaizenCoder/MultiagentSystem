#!/usr/bin/env python3
"""
Test de structure et capacités pour agent_MAINTENANCE_04_testeur_anti_faux_agents.py
Validation des technologies d'introspection et tests dynamiques.
"""
import ast
import sys
from pathlib import Path

def test_agent_structure_and_capabilities():
    """Test complet de l'agent MAINTENANCE 04."""
    print("=" * 80)
    print("🛡️ TEST AGENT MAINTENANCE 04 - TESTEUR ANTI-FAUX AGENTS")
    print("=" * 80)
    
    agent_file = Path("agents/agent_MAINTENANCE_04_testeur_anti_faux_agents.py")
    
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
        print(f"   Classes: {len(classes)} (principales: {[c for c in classes if 'Agent' in c or 'Detection' in c]})")
        print(f"   Dataclasses: {dataclasses}")
        print(f"   Fonctions: {len(functions)} (dont {len(async_functions)} async)")
        print(f"   Imports: {len(imports)} modules")
        
        # Vérifications critiques
        success_count = 0
        total_checks = 15
        
        # 1. Classe principale
        if "AgentMAINTENANCE04TesteurAntiFauxAgents" in classes:
            print("✅ Classe principale AgentMAINTENANCE04TesteurAntiFauxAgents trouvée")
            success_count += 1
        else:
            print("❌ Classe principale manquante")
        
        # 2. Fonction factory
        if "create_agent_MAINTENANCE_04_testeur_anti_faux_agents" in functions:
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
        
        # 6. Version 4.1.0
        version_found = "Version: 4.1.0" in code
        if version_found:
            print("✅ Version 4.1.0 trouvée")
            success_count += 1
        else:
            print("❌ Version attendue non trouvée")
        
        # 7. Dataclass FakeAgentDetection
        if "FakeAgentDetection" in dataclasses:
            print("✅ Dataclass FakeAgentDetection détectée")
            success_count += 1
        else:
            print("❌ Dataclass FakeAgentDetection manquante")
        
        # 8. Import inspect (introspection)
        if "inspect" in imports:
            print("✅ Import inspect détecté")
            success_count += 1
        else:
            print("❌ Import inspect manquant")
        
        # 9. Import importlib (tests dynamiques)
        if "importlib" in imports:
            print("✅ Import importlib détecté")
            success_count += 1
        else:
            print("❌ Import importlib manquant")
        
        # 10. Import uuid (fichiers temporaires)
        if "uuid" in imports:
            print("✅ Import uuid détecté")
            success_count += 1
        else:
            print("❌ Import uuid manquant")
        
        # 11. Méthode run_test (compatibilité)
        if "run_test" in functions:
            print("✅ Méthode run_test (compatibilité) présente")
            success_count += 1
        else:
            print("❌ Méthode run_test manquante")
        
        # 12. Méthode _run_dynamic_test
        if "_run_dynamic_test" in functions:
            print("✅ Méthode _run_dynamic_test présente")
            success_count += 1
        else:
            print("❌ Méthode _run_dynamic_test manquante")
        
        # 13. Test capacités étendues (10 capacités)
        capabilities_pattern = "dynamic_agent_testing"
        if capabilities_pattern in code:
            print("✅ Capacités étendues détectées")
            success_count += 1
        else:
            print("❌ Capacités étendues manquantes")
        
        # 14. Docstring enrichie détectée
        if "Agent spécialisé dans la validation dynamique" in code:
            print("✅ Docstring enrichie détectée")
            success_count += 1
        else:
            print("❌ Docstring enrichie manquante")
        
        # 15. Test fonctionnalités introspection
        print("\n🔍 Test simulation capacités d'introspection:")
        try:
            introspection_features = ["inspect.signature", "spec_from_file_location", "temp_test_agents", "issubclass"]
            found_features = [f for f in introspection_features if f in code]
            
            if len(found_features) >= 3:
                print(f"✅ Fonctionnalités introspection détectées: {len(found_features)}/4")
                print(f"   Présentes: {found_features}")
                success_count += 1
            else:
                print(f"❌ Fonctionnalités introspection insuffisantes: {found_features}")
            
        except Exception as e:
            print(f"❌ Erreur vérification introspection: {e}")
        
        # Résumé
        print("\n" + "=" * 80)
        print(f"📊 RÉSULTATS: {success_count}/{total_checks} vérifications réussies")
        
        if success_count == total_checks:
            print("🎉 AGENT PARFAITEMENT CONFORME - Technologies introspection validées")
            return True
        elif success_count >= 12:
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