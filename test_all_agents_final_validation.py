#!/usr/bin/env python3
"""
Script de validation finale - Test de tous les agents après installation des dépendances
Valide que tous les agents dans le répertoire 'agents' sont fonctionnels
"""

import os
import sys
import importlib.util
import traceback
from pathlib import Path
import json
from datetime import datetime

def test_agent_import(agent_file):
    """Test d'import d'un agent spécifique."""
    try:
        # Créer un nom de module unique
        module_name = agent_file.stem
        
        # Charger le module
        spec = importlib.util.spec_from_file_location(module_name, agent_file)
        if spec is None:
            return False, "Impossible de créer spec pour le module"
            
        module = importlib.util.module_from_spec(spec)
        
        # Tenter l'import
        spec.loader.exec_module(module)
        
        return True, "Import réussi"
        
    except Exception as e:
        return False, str(e)

def validate_all_agents():
    """Valide tous les agents du répertoire agents/"""
    
    agents_dir = Path("agents")
    if not agents_dir.exists():
        print("❌ Répertoire 'agents' non trouvé")
        return False
    
    # Lister tous les fichiers .py dans agents/
    agent_files = list(agents_dir.glob("*.py"))
    agent_files = [f for f in agent_files if not f.name.startswith("__")]
    
    if not agent_files:
        print("❌ Aucun agent trouvé dans le répertoire 'agents'")
        return False
    
    print(f"🔍 VALIDATION DE {len(agent_files)} AGENTS")
    print("=" * 60)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "total_agents": len(agent_files),
        "success_count": 0,
        "failed_count": 0,
        "success_agents": [],
        "failed_agents": [],
        "details": {}
    }
    
    for agent_file in sorted(agent_files):
        agent_name = agent_file.name
        print(f"\n📝 Test: {agent_name}")
        
        success, message = test_agent_import(agent_file)
        
        results["details"][agent_name] = {
            "success": success,
            "message": message
        }
        
        if success:
            print(f"✅ {agent_name}: {message}")
            results["success_count"] += 1
            results["success_agents"].append(agent_name)
        else:
            print(f"❌ {agent_name}: {message}")
            results["failed_count"] += 1
            results["failed_agents"].append(agent_name)
    
    # Statistiques finales
    success_rate = (results["success_count"] / results["total_agents"]) * 100
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS VALIDATION FINALE")
    print("=" * 60)
    print(f"✅ Agents fonctionnels: {results['success_count']}/{results['total_agents']}")
    print(f"❌ Agents en échec: {results['failed_count']}/{results['total_agents']}")
    print(f"📈 Taux de succès: {success_rate:.1f}%")
    
    if results["failed_count"] > 0:
        print(f"\n⚠️ Agents en échec:")
        for agent in results["failed_agents"]:
            error_msg = results["details"][agent]["message"]
            print(f"  - {agent}: {error_msg[:80]}...")
    
    # Sauvegarder le rapport
    report_path = Path("reports/validation_finale_agents.json")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Rapport détaillé: {report_path}")
    
    # Vérifier si objectif atteint
    if success_rate == 100.0:
        print("\n🎉 OBJECTIF ATTEINT: Tous les agents sont fonctionnels!")
        return True
    else:
        print(f"\n⚠️ Objectif non atteint: {results['failed_count']} agents nécessitent encore des corrections")
        return False

if __name__ == "__main__":
    print("🚀 VALIDATION FINALE DES AGENTS NEXTGENERATION")
    print("Vérification que tous les agents du répertoire 'agents' sont fonctionnels")
    print("=" * 80)
    
    # Changer vers le répertoire du projet
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Ajouter le répertoire agents au path
    agents_path = script_dir / "agents"
    sys.path.insert(0, str(agents_path))
    
    success = validate_all_agents()
    
    if success:
        print("\n✅ MISSION ACCOMPLIE: Tous les agents sont fonctionnels")
        sys.exit(0)
    else:
        print("\n❌ MISSION EN COURS: Des corrections supplémentaires sont nécessaires")
        sys.exit(1)