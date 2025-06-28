#!/usr/bin/env python3
"""
Test de structure et capacités pour agent_MAINTENANCE_06_correcteur_logique_metier.py
Validation des technologies d'analyse AST, patterns métier et correction logique.
"""
import ast
import sys
from pathlib import Path

def test_agent_structure_and_capabilities():
    """Test complet de l'agent MAINTENANCE 06."""
    print("=" * 80)
    print("🔧 TEST AGENT MAINTENANCE 06 - CORRECTEUR LOGIQUE MÉTIER")
    print("=" * 80)
    
    agent_file = Path("agents/agent_MAINTENANCE_06_correcteur_logique_metier.py")
    
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
        print(f"   Classes: {len(classes)} (principales: {[c for c in classes if 'Agent' in c or 'Logic' in c]})")
        print(f"   Dataclasses: {dataclasses}")
        print(f"   Fonctions: {len(functions)} (dont {len(async_functions)} async)")
        print(f"   Imports: {len(imports)} modules")
        
        # Vérifications critiques
        success_count = 0
        total_checks = 16
        
        # 1. Classe principale
        if "AgentMAINTENANCE06CorrecteurLogiqueMetier" in classes:
            print("✅ Classe principale AgentMAINTENANCE06CorrecteurLogiqueMetier trouvée")
            success_count += 1
        else:
            print("❌ Classe principale manquante")
        
        # 2. Fonction factory
        if "create_agent_MAINTENANCE_06_correcteur_logique_metier" in functions:
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
        
        # 6. Version 6.1.0
        version_found = "Version: 6.1.0" in code
        if version_found:
            print("✅ Version 6.1.0 trouvée")
            success_count += 1
        else:
            print("❌ Version attendue non trouvée")
        
        # 7. Dataclass LogicIssue
        if "LogicIssue" in dataclasses:
            print("✅ Dataclass LogicIssue détectée")
            success_count += 1
        else:
            print("❌ Dataclass LogicIssue manquante")
        
        # 8. Import ast (analyse AST)
        if "ast" in imports:
            print("✅ Import ast détecté")
            success_count += 1
        else:
            print("❌ Import ast manquant")
        
        # 9. Import inspect (introspection)
        if "inspect" in imports:
            print("✅ Import inspect détecté")
            success_count += 1
        else:
            print("❌ Import inspect manquant")
        
        # 10. Méthodes de gestion des tâches
        task_handlers = ["_handle_business_logic_correction", "_handle_pattern_validation", "_handle_logic_analysis", "_handle_compliance_audit"]
        found_handlers = [h for h in task_handlers if h in functions]
        if len(found_handlers) >= 3:
            print(f"✅ Handlers de tâches détectés: {len(found_handlers)}/4")
            success_count += 1
        else:
            print(f"❌ Handlers de tâches insuffisants: {found_handlers}")
        
        # 11. Méthodes d'analyse métier
        analysis_methods = ["_analyze_business_logic", "_validate_business_patterns", "_detect_logic_inconsistencies"]
        found_analysis = [m for m in analysis_methods if m in async_functions or f"async {m}" in functions]
        if len(found_analysis) >= 2:
            print(f"✅ Méthodes d'analyse métier détectées: {len(found_analysis)}/3")
            success_count += 1
        else:
            print(f"❌ Méthodes d'analyse métier insuffisantes: {found_analysis}")
        
        # 12. Configuration patterns métier
        if "business_patterns" in code and "anti_patterns" in code:
            print("✅ Configuration patterns métier détectée")
            success_count += 1
        else:
            print("❌ Configuration patterns métier manquante")
        
        # 13. Test capacités étendues (10 capacités)
        capabilities_pattern = "correct_business_logic"
        extended_caps = ["validate_business_patterns", "detect_logic_inconsistencies", "audit_business_compliance"]
        if capabilities_pattern in code and all(cap in code for cap in extended_caps):
            print("✅ Capacités étendues détectées")
            success_count += 1
        else:
            print("❌ Capacités étendues manquantes")
        
        # 14. Docstring enrichie détectée
        if "Agent spécialisé dans la correction et validation de la logique métier" in code:
            print("✅ Docstring enrichie détectée")
            success_count += 1
        else:
            print("❌ Docstring enrichie manquante")
        
        # 15. Méthodes auxiliaires
        aux_methods = ["_generate_corrections", "_categorize_by_severity", "_audit_business_compliance"]
        found_aux = [m for m in aux_methods if m in async_functions or f"async {m}" in functions or m in functions]
        if len(found_aux) >= 2:
            print(f"✅ Méthodes auxiliaires détectées: {len(found_aux)}/3")
            success_count += 1
        else:
            print(f"❌ Méthodes auxiliaires insuffisantes: {found_aux}")
        
        # 16. Test fonctionnalités logique métier avancées
        print("\n🔍 Test simulation capacités logique métier:")
        try:
            logic_features = ["ast.parse", "ast.walk", "LogicIssue", "business_patterns", "severity"]
            found_features = [f for f in logic_features if f in code]
            
            if len(found_features) >= 4:
                print(f"✅ Fonctionnalités logique métier détectées: {len(found_features)}/5")
                print(f"   Présentes: {found_features}")
                success_count += 1
            else:
                print(f"❌ Fonctionnalités logique métier insuffisantes: {found_features}")
            
        except Exception as e:
            print(f"❌ Erreur vérification logique métier: {e}")
        
        # Résumé
        print("\n" + "=" * 80)
        print(f"📊 RÉSULTATS: {success_count}/{total_checks} vérifications réussies")
        
        if success_count == total_checks:
            print("🎉 AGENT PARFAITEMENT CONFORME - Technologies logique métier validées")
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