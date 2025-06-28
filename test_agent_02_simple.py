#!/usr/bin/env python3
"""
Test simplifié pour valider la structure du code agent_02_architecte_code_expert.py
"""

import ast
import sys
from pathlib import Path

def test_agent_syntax():
    """Test de validation syntaxique et structurelle"""
    print("🧪 Test syntaxique agent_02_architecte_code_expert.py")
    print("=" * 60)
    
    agent_path = Path("agents/agent_02_architecte_code_expert.py")
    
    if not agent_path.exists():
        print("❌ Fichier agent non trouvé")
        return False
    
    try:
        # Test syntaxique
        with open(agent_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        ast.parse(content)
        print("✅ Syntaxe Python valide")
        
        # Vérification présence des méthodes requises
        required_methods = [
            'generer_rapport_strategique',
            '_collecter_metriques_architecture',
            '_generer_rapport_architecture',
            '_generer_rapport_integration',
            '_generer_rapport_qualite_code',
            '_generer_rapport_performance_expert'
        ]
        
        methods_found = []
        for method in required_methods:
            if f"async def {method}" in content:
                methods_found.append(method)
                print(f"✅ Méthode {method} trouvée")
            else:
                print(f"❌ Méthode {method} manquante")
        
        # Vérification intégration execute_task
        if "generate_strategic_report" in content:
            print("✅ Intégration execute_task trouvée")
        else:
            print("❌ Intégration execute_task manquante")
        
        # Vérification spécialisation architecture
        specializations = [
            'architecture_strategique',
            'integration_code_expert', 
            'qualite_code_expert',
            'performance_integration_expert'
        ]
        
        spec_found = []
        for spec in specializations:
            if spec in content:
                spec_found.append(spec)
                print(f"✅ Spécialisation {spec} trouvée")
        
        success_rate = len(methods_found) / len(required_methods)
        spec_rate = len(spec_found) / len(specializations)
        
        print(f"\n📊 Taux de réussite méthodes: {success_rate*100:.1f}%")
        print(f"🏗️ Taux spécialisations architecture: {spec_rate*100:.1f}%")
        
        if success_rate >= 1.0 and spec_rate >= 1.0:
            print("🎯 VALIDATION RÉUSSIE - Toutes les fonctionnalités architecture ajoutées")
            return True
        else:
            print("⚠️ VALIDATION PARTIELLE - Certaines fonctionnalités manquantes")
            return False
            
    except SyntaxError as e:
        print(f"❌ Erreur syntaxique: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def analyze_code_metrics():
    """Analyse des métriques du code ajouté"""
    print("\n📈 Analyse métriques du code architecture")
    print("-" * 40)
    
    agent_path = Path("agents/agent_02_architecte_code_expert.py")
    
    try:
        with open(agent_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        
        # Compter les lignes de méthodes stratégiques
        strategic_lines = 0
        in_strategic_method = False
        
        for line in lines:
            if 'generer_rapport_strategique' in line or '_generer_rapport_' in line or '_collecter_metriques_architecture' in line:
                in_strategic_method = True
            elif line.strip().startswith('async def ') and in_strategic_method:
                in_strategic_method = False
            elif line.strip().startswith('def ') and in_strategic_method:
                in_strategic_method = False
                
            if in_strategic_method:
                strategic_lines += 1
        
        # Vérifications spécifiques architecture
        architecture_keywords = ['architecture', 'integration', 'expert_scripts', 'pattern_factory', 'modularity_score']
        arch_count = sum(1 for line in lines for keyword in architecture_keywords if keyword in line.lower())
        
        print(f"📝 Lignes totales: {total_lines}")
        print(f"🏗️ Lignes fonctionnalité architecture: ~{strategic_lines}")
        print(f"📊 Pourcentage ajouté: ~{(strategic_lines/total_lines)*100:.1f}%")
        print(f"🔧 Références architecture: {arch_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur analyse métriques: {e}")
        return False

def test_architecture_specialization():
    """Test spécifique aux spécialisations architecture"""
    print("\n🏛️ Test spécialisations architecture")
    print("-" * 40)
    
    agent_path = Path("agents/agent_02_architecte_code_expert.py")
    
    try:
        with open(agent_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Tests spécialisations
        tests = {
            'Métriques architecture': 'architecture_health' in content,
            'Scripts experts': 'expert_scripts' in content,
            'Pattern Factory': 'pattern_factory_compliance' in content,
            'Modularité': 'modularity_score' in content,
            'Intégration code expert': 'integration_code_expert' in content,
            'Performance expert': 'performance_integration_expert' in content,
            'Support async': 'async_support' in content,
            'Gestion erreurs': 'error_handling' in content
        }
        
        passed = 0
        for test_name, result in tests.items():
            status = "✅" if result else "❌"
            print(f"{status} {test_name}")
            if result:
                passed += 1
        
        success_rate = passed / len(tests)
        print(f"\n🎯 Score spécialisation architecture: {success_rate*100:.1f}%")
        
        return success_rate >= 0.8
        
    except Exception as e:
        print(f"❌ Erreur test spécialisations: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Validation agent_02_architecte_code_expert - Rapports Stratégiques Architecture")
    print("=" * 80)
    
    syntax_ok = test_agent_syntax()
    metrics_ok = analyze_code_metrics()
    spec_ok = test_architecture_specialization()
    
    if syntax_ok and metrics_ok and spec_ok:
        print("\n✅ VALIDATION COMPLÈTE RÉUSSIE")
        print("🏗️ Agent 02 Architecture prêt pour tests fonctionnels")
        exit(0)
    else:
        print("\n❌ VALIDATION ÉCHOUÉE")
        exit(1)