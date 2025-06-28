#!/usr/bin/env python3
"""
Test simplifié pour valider la structure du code agent_01_coordinateur_principal.py
"""

import ast
import sys
from pathlib import Path

def test_agent_syntax():
    """Test de validation syntaxique et structurelle"""
    print("🧪 Test syntaxique agent_01_coordinateur_principal.py")
    print("=" * 60)
    
    agent_path = Path("agents/agent_01_coordinateur_principal.py")
    
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
            '_collecter_metriques_coordination',
            '_generer_rapport_global',
            '_generer_rapport_sprint',
            '_generer_rapport_performance',
            '_generer_rapport_qualite'
        ]
        
        methods_found = []
        for method in required_methods:
            if f"async def {method}" in content:
                methods_found.append(method)
                print(f"✅ Méthode {method} trouvée")
            else:
                print(f"❌ Méthode {method} manquante")
        
        # Vérification intégration execute_task
        if "GENERATE_STRATEGIC_REPORT" in content:
            print("✅ Intégration execute_task trouvée")
        else:
            print("❌ Intégration execute_task manquante")
        
        success_rate = len(methods_found) / len(required_methods)
        print(f"\n📊 Taux de réussite: {success_rate*100:.1f}%")
        
        if success_rate >= 1.0:
            print("🎯 VALIDATION RÉUSSIE - Toutes les fonctionnalités ajoutées")
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
    print("\n📈 Analyse métriques du code")
    print("-" * 40)
    
    agent_path = Path("agents/agent_01_coordinateur_principal.py")
    
    try:
        with open(agent_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        
        # Compter les lignes de méthodes stratégiques
        strategic_lines = 0
        in_strategic_method = False
        
        for line in lines:
            if 'generer_rapport_strategique' in line or '_generer_rapport_' in line or '_collecter_metriques_' in line:
                in_strategic_method = True
            elif line.strip().startswith('async def ') and in_strategic_method:
                in_strategic_method = False
            elif line.strip().startswith('def ') and in_strategic_method:
                in_strategic_method = False
                
            if in_strategic_method:
                strategic_lines += 1
        
        print(f"📝 Lignes totales: {total_lines}")
        print(f"🎯 Lignes fonctionnalité stratégique: ~{strategic_lines}")
        print(f"📊 Pourcentage ajouté: ~{(strategic_lines/total_lines)*100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur analyse métriques: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Validation agent_01_coordinateur_principal - Rapports Stratégiques")
    print("=" * 80)
    
    syntax_ok = test_agent_syntax()
    metrics_ok = analyze_code_metrics()
    
    if syntax_ok and metrics_ok:
        print("\n✅ VALIDATION COMPLÈTE RÉUSSIE")
        print("🎯 Agent 01 prêt pour tests fonctionnels")
        exit(0)
    else:
        print("\n❌ VALIDATION ÉCHOUÉE")
        exit(1)