#!/usr/bin/env python3
"""
TEST ADAPTATEUR v4.2.0 - PRIORITÉS HAUTES
==========================================

Test des nouvelles fonctionnalités prioritaires :
1. Extension du système de classification d'erreurs
2. Auto-découverte des imports
3. Validation multi-niveaux

Author: Équipe NextGeneration  
Version: Test v4.2.0
"""

import asyncio
import sys
import tempfile
from pathlib import Path
from datetime import datetime

# Configuration du chemin
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from agents.agent_MAINTENANCE_03_adaptateur_code import (
        AgentMAINTENANCE03AdaptateurCode, 
        ErrorType, 
        ErrorClassification,
        ImportDiscovery,
        ValidationResult
    )
    from core.agent_factory_architecture import Task, Result
except ImportError as e:
    print(f"❌ Erreur import: {e}")
    sys.exit(1)

class TestAdaptateurV42:
    """Test des fonctionnalités v4.2.0 - Priorités Hautes"""
    
    def __init__(self):
        self.adaptateur = AgentMAINTENANCE03AdaptateurCode(id="test_v42")
        
    async def test_classification_etendue(self) -> bool:
        """Test 1: Classification d'erreurs étendue"""
        print("\n🔍 TEST 1: Classification d'erreurs étendue")
        
        test_cases = [
            (IndentationError("expected an indented block"), ErrorType.INDENTATION),
            (NameError("name 'Path' is not defined"), ErrorType.NAME),
            (TypeError("unsupported operand type(s)"), ErrorType.TYPE_ERROR),
            (AttributeError("'str' object has no attribute 'append'"), ErrorType.ATTRIBUTE_ERROR),
            (ValueError("invalid literal"), ErrorType.VALUE_ERROR),
            (ModuleNotFoundError("No module named 'nonexistent'"), ErrorType.MODULE_NOT_FOUND),
            (SyntaxError("invalid syntax"), ErrorType.SYNTAX)
        ]
        
        success_count = 0
        
        for error, expected_type in test_cases:
            try:
                classification = self.adaptateur.classify_error_extended(error)
                
                if classification.error_type == expected_type:
                    print(f"✅ {error.__class__.__name__} → {expected_type.value} (confiance: {classification.confidence_score:.2f})")
                    success_count += 1
                else:
                    print(f"❌ {error.__class__.__name__} → {classification.error_type.value} (attendu: {expected_type.value})")
                    
                # Vérification des suggestions
                if classification.suggested_fixes:
                    print(f"   💡 Suggestions: {len(classification.suggested_fixes)} proposées")
                    
            except Exception as e:
                print(f"❌ Erreur classification {error.__class__.__name__}: {e}")
        
        success_rate = success_count / len(test_cases)
        print(f"📊 Résultat: {success_count}/{len(test_cases)} classifications réussies ({success_rate*100:.1f}%)")
        
        return success_rate >= 0.8  # 80% minimum requis
    
    async def test_auto_decouverte_imports(self) -> bool:
        """Test 2: Auto-découverte des imports"""
        print("\n🔍 TEST 2: Auto-découverte des imports")
        
        try:
            # Test découverte sur le projet actuel
            discoveries = self.adaptateur.discover_project_imports(PROJECT_ROOT)
            
            print(f"✅ Découverte terminée: {len(discoveries)} imports trouvés")
            
            # Vérification de quelques imports communs attendus
            expected_imports = ["Path", "logging", "asyncio", "sys"]
            found_imports = 0
            
            for expected in expected_imports:
                if expected in discoveries:
                    discovery = discoveries[expected]
                    print(f"✅ {expected}: {discovery.import_statement} (confiance: {discovery.confidence:.2f}, usage: {discovery.usage_count})")
                    found_imports += 1
                else:
                    print(f"⚠️  {expected}: non trouvé dans la découverte")
            
            # Test du cache
            if self.adaptateur._import_discovery_cache:
                print(f"✅ Cache d'imports populé: {len(self.adaptateur._import_discovery_cache)} éléments")
            else:
                print("❌ Cache d'imports vide")
                return False
            
            # Validation des données de découverte
            valid_discoveries = 0
            for name, discovery in list(discoveries.items())[:5]:  # Test sur 5 premiers
                if (discovery.confidence > 0 and 
                    discovery.usage_count > 0 and 
                    discovery.import_statement and
                    discovery.source_files):
                    valid_discoveries += 1
            
            print(f"📊 Résultat: {found_imports}/{len(expected_imports)} imports attendus trouvés")
            print(f"📊 Qualité: {valid_discoveries}/5 découvertes valides testées")
            
            return found_imports >= 2 and valid_discoveries >= 4  # Critères minimum
            
        except Exception as e:
            print(f"❌ Erreur auto-découverte: {e}")
            return False
    
    async def test_validation_multi_niveaux(self) -> bool:
        """Test 3: Validation multi-niveaux"""
        print("\n🔍 TEST 3: Validation multi-niveaux")
        
        test_codes = [
            # Code valide
            {
                "code": """
def hello_world():
    print("Hello, World!")
    return True
""",
                "expected_syntax": True,
                "expected_semantic": True,
                "description": "Code Python valide"
            },
            
            # Erreur de syntaxe
            {
                "code": """
def broken_function(
    print("Missing closing parenthesis")
""",
                "expected_syntax": False,
                "expected_semantic": False,
                "description": "Erreur de syntaxe (parenthèse manquante)"
            },
            
            # Code avec convention PEP8 incorrecte
            {
                "code": """
def BadFunctionName():
    MyVariable = "test"
    return MyVariable
""",
                "expected_syntax": True,
                "expected_semantic": True,  # Sémantiquement correct malgré le style
                "description": "Convention PEP8 incorrecte"
            },
            
            # Import inexistant
            {
                "code": """
import nonexistent_module
from another_fake_module import something

def test():
    return True
""",
                "expected_syntax": True,
                "expected_semantic": True,
                "description": "Imports inexistants"
            }
        ]
        
        success_count = 0
        
        for i, test_case in enumerate(test_codes, 1):
            try:
                validation = self.adaptateur.validate_multi_level(test_case["code"])
                
                syntax_ok = validation.syntax_valid == test_case["expected_syntax"]
                semantic_ok = validation.semantic_valid == test_case["expected_semantic"]
                
                print(f"\n--- Test {i}: {test_case['description']} ---")
                print(f"Syntaxe: {'✅' if syntax_ok else '❌'} {validation.syntax_valid} (attendu: {test_case['expected_syntax']})")
                print(f"Sémantique: {'✅' if semantic_ok else '❌'} {validation.semantic_valid} (attendu: {test_case['expected_semantic']})")
                print(f"Compilation: {'✅' if validation.compilation_successful else '❌'} {validation.compilation_successful}")
                print(f"Imports: {'✅' if validation.import_resolution else '❌'} {validation.import_resolution}")
                print(f"Score confiance: {validation.confidence_score:.2f}")
                
                if validation.issues:
                    print(f"Issues ({len(validation.issues)}): {validation.issues}")
                if validation.warnings:
                    print(f"Warnings ({len(validation.warnings)}): {validation.warnings}")
                
                if syntax_ok and semantic_ok:
                    success_count += 1
                    print("✅ Test validé")
                else:
                    print("❌ Test échoué")
                
            except Exception as e:
                print(f"❌ Erreur validation test {i}: {e}")
        
        success_rate = success_count / len(test_codes)
        print(f"\n📊 Résultat: {success_count}/{len(test_codes)} validations réussies ({success_rate*100:.1f}%)")
        
        return success_rate >= 0.75  # 75% minimum requis
    
    async def test_integration_complete(self) -> bool:
        """Test 4: Intégration complète des nouvelles fonctionnalités"""
        print("\n🔍 TEST 4: Intégration complète v4.2.0")
        
        # Code de test avec erreur NameError corrigible
        test_code = """
def test_function():
    # Erreur : Path n'est pas importé
    my_path = Path("/tmp/test")
    return my_path.exists()

class TestClass:
    def method(self):
        return "test"
"""
        
        try:
            # Simulation d'une erreur NameError
            name_error = NameError("name 'Path' is not defined")
            
            # Préparation de la tâche avec les nouvelles options
            task = Task(
                id="test_integration",
                params={
                    "code": test_code,
                    "feedback": name_error,
                    "error_type": "name",  # Sera re-classifié automatiquement
                    "use_import_discovery": True,
                    "validate_result": True
                }
            )
            
            # Exécution de la tâche
            await self.adaptateur.startup()
            result = await self.adaptateur.execute_task(task)
            
            if result.success:
                print("✅ Tâche exécutée avec succès")
                
                data = result.data
                adapted_code = data.get("adapted_code", "")
                adaptations = data.get("adaptations", [])
                classification = data.get("error_classification")
                validation_pre = data.get("validation_pre")
                validation_post = data.get("validation_post")
                
                print(f"✅ Adaptations appliquées: {len(adaptations)}")
                for adaptation in adaptations:
                    print(f"   → {adaptation}")
                
                # Vérification classification
                if classification:
                    print(f"✅ Classification: {classification['error_type']} (confiance: {classification['confidence_score']:.2f})")
                
                # Vérification validation
                if validation_pre and validation_post:
                    improvement = validation_post['confidence_score'] - validation_pre['confidence_score']
                    print(f"✅ Amélioration qualité: {improvement:+.2f} points")
                    print(f"   Score pré: {validation_pre['confidence_score']:.2f}")
                    print(f"   Score post: {validation_post['confidence_score']:.2f}")
                
                # Vérification que l'import a été ajouté
                if "from pathlib import Path" in adapted_code or "import pathlib" in adapted_code:
                    print("✅ Import Path ajouté automatiquement")
                else:
                    print("⚠️  Import Path non détecté dans le code adapté")
                
                # Test de compilation du code adapté
                try:
                    compile(adapted_code, '<string>', 'exec')
                    print("✅ Code adapté compile sans erreur")
                    return True
                except SyntaxError as e:
                    print(f"❌ Code adapté ne compile pas: {e}")
                    return False
            else:
                print(f"❌ Échec exécution tâche: {result.error}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur test intégration: {e}")
            return False
        finally:
            await self.adaptateur.shutdown()

async def run_complete_test_suite():
    """Exécute la suite complète de tests v4.2.0"""
    print("🚀 SUITE DE TESTS - Adaptateur v4.2.0 Priorités Hautes")
    print("="*70)
    
    tester = TestAdaptateurV42()
    
    tests = [
        ("Classification Étendue", tester.test_classification_etendue),
        ("Auto-découverte Imports", tester.test_auto_decouverte_imports),
        ("Validation Multi-niveaux", tester.test_validation_multi_niveaux),
        ("Intégration Complète", tester.test_integration_complete)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 EXÉCUTION: {test_name}")
        print(f"{'='*50}")
        
        try:
            success = await test_func()
            results.append((test_name, success))
            status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
            print(f"\n{status}: {test_name}")
            
        except Exception as e:
            print(f"\n❌ ERREUR FATALE: {test_name} - {e}")
            results.append((test_name, False))
    
    # Rapport final
    print("\n" + "="*70)
    print("📊 RAPPORT FINAL - ADAPTATEUR v4.2.0")
    print("="*70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSÉ" if success else "❌ ÉCHEC"
        print(f"{status:10} | {test_name}")
    
    print("="*70)
    print(f"RÉSULTAT GLOBAL: {passed}/{total} tests réussis ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 VALIDATION COMPLÈTE: Adaptateur v4.2.0 prêt pour production!")
        print("✅ Toutes les priorités hautes implémentées et validées")
        return True
    else:
        print("⚠️  VALIDATION PARTIELLE: Corrections nécessaires")
        print("❌ Certaines priorités hautes nécessitent des ajustements")
        return False

async def main():
    """Point d'entrée principal"""
    try:
        success = await run_complete_test_suite()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrompus par l'utilisateur")
        return 130
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))