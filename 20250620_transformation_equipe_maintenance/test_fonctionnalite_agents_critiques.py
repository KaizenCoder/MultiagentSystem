#!/usr/bin/env python3
"""
🔍 TEST FONCTIONNALITÉ AGENTS "CRITIQUES"
=======================================
Vérifie si les agents identifiés comme critiques dans le rapport sont vraiment non-fonctionnels
"""

import sys
import importlib.util
from pathlib import Path
import traceback

def tester_import_agent(agent_path: str) -> dict:
    """Teste si un agent peut être importé et instancié"""
    try:
        # Convertir chemin relatif vers absolu
        if agent_path.startswith('../'):
            agent_path = str(Path(__file__).parent / agent_path)
        
        agent_file = Path(agent_path)
        if not agent_file.exists():
            return {
                "agent": agent_file.name,
                "import_success": False,
                "error": f"Fichier non trouvé: {agent_path}",
                "functional": False
            }
        
        # Tenter l'import
        spec = importlib.util.spec_from_file_location("test_agent", agent_file)
        module = importlib.util.module_from_spec(spec)
        
        print(f"📁 Test import: {agent_file.name}")
        spec.loader.exec_module(module)
        
        # Chercher les classes dans le module
        classes_trouvees = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and not attr_name.startswith('_'):
                classes_trouvees.append(attr_name)
        
        return {
            "agent": agent_file.name,
            "import_success": True,
            "error": None,
            "functional": True,
            "classes_found": classes_trouvees,
            "module_attrs": len(dir(module))
        }
        
    except SyntaxError as e:
        return {
            "agent": Path(agent_path).name,
            "import_success": False,
            "error": f"ERREUR SYNTAXE: {e}",
            "functional": False,
            "syntax_error_line": getattr(e, 'lineno', 'Unknown'),
            "syntax_error_text": getattr(e, 'text', 'Unknown').strip() if getattr(e, 'text', None) else 'Unknown'
        }
        
    except Exception as e:
        return {
            "agent": Path(agent_path).name,
            "import_success": False,
            "error": f"ERREUR: {type(e).__name__}: {e}",
            "functional": False,
            "traceback": traceback.format_exc()
        }

def main():
    print("🔍 TEST FONCTIONNALITÉ AGENTS SUPPOSÉS CRITIQUES")
    print("=" * 50)
    
    # Agents identifiés comme critiques dans le rapport
    agents_critiques = [
        "../agent_factory_implementation/agents/agent_01_coordinateur_principal.py",
        "../agent_factory_implementation/agents/agent_02_architecte_code_expert.py", 
        "../agent_factory_implementation/agents/agent_04_expert_securite_crypto.py",
        "../agent_factory_implementation/agents/agent_05_maitre_tests_validation.py"
    ]
    
    resultats = []
    
    for agent_path in agents_critiques:
        print(f"\n🧪 Test: {Path(agent_path).name}")
        print("-" * 40)
        
        resultat = tester_import_agent(agent_path)
        resultats.append(resultat)
        
        if resultat["functional"]:
            print(f"✅ FONCTIONNEL - Import réussi")
            print(f"   Classes trouvées: {resultat.get('classes_found', [])}")
        else:
            print(f"❌ NON-FONCTIONNEL - {resultat['error']}")
            if 'syntax_error_line' in resultat:
                print(f"   Ligne erreur: {resultat['syntax_error_line']}")
                print(f"   Texte erreur: {resultat['syntax_error_text']}")
    
    print("\n📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    fonctionnels = [r for r in resultats if r["functional"]]
    non_fonctionnels = [r for r in resultats if not r["functional"]]
    
    print(f"✅ Agents fonctionnels: {len(fonctionnels)}/{len(resultats)}")
    for agent in fonctionnels:
        print(f"   - {agent['agent']}")
    
    print(f"❌ Agents non-fonctionnels: {len(non_fonctionnels)}/{len(resultats)}")
    for agent in non_fonctionnels:
        print(f"   - {agent['agent']}: {agent['error']}")
    
    # Conclusion
    if len(non_fonctionnels) == 0:
        print(f"\n🎉 SURPRISE ! Tous les agents sont fonctionnels !")
        print("   Le rapport d'audit contenait peut-être des erreurs.")
    elif len(non_fonctionnels) < len(resultats):
        print(f"\n⚠️ MITIGÉ: {len(non_fonctionnels)} agents vraiment défaillants sur {len(resultats)}")
    else:
        print(f"\n💥 CRITIQUE: Tous les agents sont effectivement non-fonctionnels")
    
    return resultats

if __name__ == "__main__":
    main() 



